from pathlib import Path
from IPython.display import Markdown, display

import time
from strands import Agent
from strands.models.mistral import MistralModel
import os
import sys
import json
import boto3
import requests
from collections import Counter

from typing import Dict, List, Optional, Tuple, TypeVar
from tqdm import tqdm

# AWS authentication
from botocore.auth import SigV4Auth
from botocore.awsrequest import AWSRequest

sys.path.append('..')

from src.utils import (
    save_json,
    read_json,
    load_file_content,
    get_job_paths,
    get_training_paths,
    sanity_check,
	chat_with_persona,
    track_api_call,  # Cost tracking from utils
    print_cost_summary,  # Cost summary from utils
    reset_cost_tracker  # Reset cost tracker from utils
)

from src.models.persona_info import PersonaInfo
from src.models.training_info import TrainingInfo
from src.models.skill_domain_info import SkillDomainInfo
from src.models.activity_domain_info import ActivityDomainInfo

from src.prompts.find_training_matches_prompt import(
    FIND_TRAINING_MATCHES_PROMPT,
    FIND_TRAINING_MATCHES_PROMPT_v1
)

def display_markdown_file(path: str) -> None:
    """Display a markdown file in Jupyter - nothing fancy"""
    p = Path(path)
    if not p.exists():
        print(f"File not found: {p}")
        return
    content = p.read_text(encoding='utf-8', errors='ignore')
    display(Markdown(content))


def call_mistral(prompt: str, model: str = "mistral-small-latest", temperature: float = 0.7) -> dict:
    """Call Mistral API and track what it costs us"""
    mistral_model = MistralModel(
        api_key=os.environ["MISTRAL_API_KEY"],
        model_id=model,
        stream=False,
        temperature=temperature
    )
    agent = Agent(model=mistral_model, callback_handler=None)
    start_time = time.time()

    try:
        response = agent(prompt)
        end_time = time.time()

        # Extract useful info
        result = {
            "content": response.message['content'][0]['text'],
            "model": model,
            "duration": end_time - start_time,
            "input_tokens": response.metrics.accumulated_usage['inputTokens'],
            "output_tokens": response.metrics.accumulated_usage['outputTokens'],
            "total_tokens": response.metrics.accumulated_usage['totalTokens']
        }

        return result

    except Exception as e:
        print(f"❌ API call failed: {e}")
        return None


def get_agent(
    system_prompt: str = "",
    model_id: str = "mistral-small-latest",
    temperature: float = 0.7
) -> Agent:
    """Create an AI agent with specific role and model"""
    model = MistralModel(
        api_key=os.environ["MISTRAL_API_KEY"],
        model_id=model_id,
        stream=False,
        temperature=temperature
    )
    return Agent(model=model, system_prompt=system_prompt, callback_handler=None)


def batch_extract(
    paths: List[Path],
    extract_func,
    save_path: Path,
    cache_period: int = 20,
    show_cost_every: int = 20,
    skills_domains: SkillDomainInfo = None,
    activities_domains: ActivityDomainInfo = None
):
    """Batch extract information with caching and cost tracking

    Args:
        paths: List of files to process
        extract_func: Function to extract info from each file
        save_path: Path to save extracted data
        cache_period: Save progress every N items
        show_cost_every: Display cost summary every N items
    """

    if not save_path.exists():
        save_json(save_path, {})

    extracted = read_json(save_path)

    print(f"Processing {len(paths)} files ({len(extracted)} already cached)")

    # Reset cost tracker for this batch operation
    if len(extracted) == 0:  # Only reset if starting fresh
        reset_cost_tracker()

    counter = 0
    new_items_processed = 0

    for path in tqdm(paths):
        id_ = path.stem
        if id_ not in extracted:
            try:
                if (extract_func.__name__ == "extract_extended_training_info"):
                    info = extract_func(
                        path,
                        skills_domains=skills_domains,
                        activities_domains=activities_domains
                    )
                else:
                    info = extract_func(path)
                extracted[id_] = info.model_dump_json()
                counter += 1
                new_items_processed += 1

                # Save progress periodically
                if counter % cache_period == 0:
                    save_json(save_path, extracted)

                # Show cost update periodically
                if new_items_processed > 0 and new_items_processed % show_cost_every == 0:
                    print(f"\n💰 Cost update after {new_items_processed} new items:")
                    print_cost_summary()
                    print()

            except Exception as e:
                print(f"Error processing {id_}: {e}")

    save_json(save_path, extracted)

    # Final cost summary if we processed any new items
    if new_items_processed > 0:
        print(f"\n✅ Processed {new_items_processed} new items")
        print_cost_summary()

    return extracted


def send_message_to_chat(
    message: str,
    persona_id: str,
    conversation_id: str = None
) -> Optional[Tuple[str, str]]:
    """Send message to persona API and get response"""
    url = "https://cygeoykm2i.execute-api.us-east-1.amazonaws.com/main/chat"

    session = boto3.Session(region_name='us-east-1')
    credentials = session.get_credentials()

    payload = {
        "persona_id": persona_id,
        "conversation_id": conversation_id,
        "message": message
    }

    request = AWSRequest(
        method='POST',
        url=url,
        data=json.dumps(payload),
        headers={'Content-Type': 'application/json'}
    )
    SigV4Auth(credentials, 'execute-api', 'us-east-1').add_auth(request)

    response = requests.request(
        method=request.method,
        url=request.url,
        headers=dict(request.headers),
        data=request.body
    )

    if response.status_code != 200:
        return None

    response_json = response.json()
    return response_json['response'], response_json['conversation_id']

def compute_stat_for_multi_items(list_data, label, include_values=False):
    # Initialize counters
    item_counts = Counter()
    value_counts = Counter() if include_values else None
    
    for list_key, list_content in list_data.items():
        try:
            # Parse the JSON string for each job
            job_data = json.loads(list_content)
            
            # Get the items
            items = job_data.get(label)
            
            if items is None:
                continue
                
            if isinstance(items, dict):
                # For dictionaries like required_skills with values
                for item, value in items.items():
                    item_counts[item] += 1
                    if include_values and value_counts is not None:
                        value_counts[value] += 1
            elif isinstance(items, list):
                # Special case for skill_acquired_and_level which is a list with [skill, level]
                if label == "skill_acquired_and_level" and len(items) >= 2:
                    skill, level = items[0], items[1]
                    item_counts[skill] += 1
                    if include_values and value_counts is not None:
                        value_counts[level] += 1
                else:
                    # For simple lists like required_languages
                    for item in items:
                        item_counts[item] += 1
        except (json.JSONDecodeError, AttributeError, TypeError) as e:
            # Skip this entry if there's an error parsing
            continue
    
    if include_values is True:
        return item_counts, value_counts

    return item_counts