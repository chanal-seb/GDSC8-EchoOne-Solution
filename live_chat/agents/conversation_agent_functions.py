import sys
from pathlib import Path
from typing import List
import json
from ..models.job_info import JobInfo
from ..models.persona_info import(
    InterviewState
)

sys.path.append('..')

from live_chat.models.interview_info import(
    InterviewAgentMessage
)

from live_chat.prompts.interview_prompt import(
    INITIAL_INTERVIEW_PROMPT_REVERSE,
    JOB_EXTENSION_INTERVIEW_PROMPT,
    JOB_FEEDBACK_INTERVIEW_PROMPT,
    TRAINING_EXTENSION_INTERVIEW_PROMPT,
    TRAINING_SKILLS_EXTENSION_INTERVIEW_PROMPT,
    OPEN_DISCUSSION_PROMPT
)

from live_chat.my_utils import (
    read_json,
    get_agent
)

DATA_DIR = Path('../live_chat/data')

# Load jobs domains map data
filename = f"map_clusters_jobs_v4.json"
save_path = DATA_DIR / filename
jobs_map = read_json(save_path)
jobs_map_lower = {key.lower(): value for key, value in jobs_map.items()}

filename = f"final_jobs_v4.json"
save_path = DATA_DIR / filename
jobs_info_raw = read_json(save_path)
jobs_info = {job_id: JobInfo(**json.loads(job_info_str)) for job_id, job_info_str in jobs_info_raw.items()}

# Load trainings domains map data
filename = f"final_map_clusters_trainings_v7.json"
save_path = DATA_DIR / filename
trainings_map = read_json(save_path)
trainings_map_lower = {key.lower(): value for key, value in trainings_map.items()}


def get_agent_message_for_initial_interview(
    interview,
    model: str = "mistral-medium-latest",
    print_prompt = False
) -> InterviewAgentMessage:
    prompt = INITIAL_INTERVIEW_PROMPT_REVERSE
    interview_agent = get_agent(prompt, model_id=model)
    conversation_str = '\n'.join(interview)
    agent_response = interview_agent.structured_output(output_model=InterviewAgentMessage, prompt=conversation_str)
    return agent_response

def get_agent_message_for_job_extension_interview(
    interview,
    model: str = "mistral-medium-latest",
    print_prompt = False
) -> InterviewAgentMessage:
    domains_str = ""
    for domain in jobs_map:
        domains_str += f"  - {domain} : {jobs_map_lower[domain.lower()]['description']}" + "\n"

    prompt = JOB_EXTENSION_INTERVIEW_PROMPT.format(
        domains_str=domains_str
    )

    if print_prompt is True:
        print(prompt)

    if not interview:
        conversation_str = "No conversation history provided. Please provide a prompt."
    else:
        conversation_str = '\n'.join(interview)

    interview_agent = get_agent(prompt, model_id=model)
    agent_response = interview_agent.structured_output(output_model=InterviewAgentMessage, prompt=conversation_str)
    return agent_response

def get_agent_message_for_training_domain_interview(
    interview,
    model: str = "mistral-medium-latest",
    print_prompt = False
) -> InterviewAgentMessage:
    domains_str = ""
    for domain in trainings_map:
        domains_str += f"- {domain}" + "\n"

    prompt = TRAINING_EXTENSION_INTERVIEW_PROMPT.format(
        domains_str=domains_str
    )

    if print_prompt is True:
        print(prompt)

    if not interview:
        conversation_str = "No conversation history provided. Please provide a prompt."
    else:
        conversation_str = '\n'.join(interview)

    interview_agent = get_agent(prompt, model_id=model)
    agent_response = interview_agent.structured_output(output_model=InterviewAgentMessage, prompt=conversation_str)
    return agent_response

def get_agent_message_for_job_feedback_interview(
    userInterview,
    model: str = "mistral-medium-latest",
    print_prompt = False
) -> InterviewAgentMessage:
    
    jobs_str = ""
    if len(userInterview.persona_info.proposed_job_ids) > 0:
        job_list_str = ""
        for job_id in userInterview.persona_info.proposed_job_ids:
            job_info = jobs_info[job_id]
            job_list_str += f"----- JOB {job_id} ------" + "\n"
            job_list_str += job_info.describe_for_interview()
            job_list_str += f"Required skills :" + "\n"
            # Assuming jobs_trainings_map is available in the scope
            # for training in jobs_trainings_map[job_id]:
            #     job_list_str += "- " + training + "\n"
            job_list_str += "\n"
        jobs_str = job_list_str
    else:
        jobs_str = "NO JOBS FOUND"

    prompt = JOB_FEEDBACK_INTERVIEW_PROMPT.format(
        goal=userInterview.persona_info.goals,
        jobs=jobs_str
    )

    if print_prompt is True:
        print(prompt)

    interview = userInterview.interview
    if not interview:
        conversation_str = "No conversation history provided. Please provide a prompt."
    else:
        conversation_str = '\n'.join(interview)

    interview_agent = get_agent(prompt, model_id=model)
    agent_response = interview_agent.structured_output(output_model=InterviewAgentMessage, prompt=conversation_str)
    return agent_response

def get_agent_message_for_training_feedback_interview(
    userInterview,
    model: str = "mistral-medium-latest",
    print_prompt = False
) -> InterviewAgentMessage:
    
    skill_domains = userInterview.persona_info.skills_domains
    
    skills_str = ""
    if len(skill_domains) > 0:
        for domain in skill_domains:
            for skill in trainings_map_lower[domain.lower()]:
                skills_str += f"- {domain} : {skill}" + "\n"
    else:
        skills_str = "NO SKILLS FOUND"

    prompt = TRAINING_SKILLS_EXTENSION_INTERVIEW_PROMPT.format(
        skills_str=skills_str
    )

    if print_prompt is True:
        print(prompt)

    interview = userInterview.interview
    if not interview:
        conversation_str = "No conversation history provided. Please provide a prompt."
    else:
        conversation_str = '\n'.join(interview)

    interview_agent = get_agent(prompt, model_id=model)
    agent_response = interview_agent.structured_output(output_model=InterviewAgentMessage, prompt=conversation_str)
    return agent_response

def get_agent_message_for_open_discussion(
    interview,
    model: str = "mistral-medium-latest",
    print_prompt = False
) -> InterviewAgentMessage:
    job_domains_str = ""
    for domain in jobs_map:
        job_domains_str += f"  - {domain} : {jobs_map[domain]['description']}" + "\n"

    skills_str = ""
    for domain in trainings_map:
        if domain.lower() in trainings_map_lower:
            for skill in trainings_map_lower[domain.lower()]:
                skills_str += f"- {domain} : {skill}" + "\n"

    prompt = OPEN_DISCUSSION_PROMPT.format(
        job_domains_str=job_domains_str,
        training_domains_and_skills_str=skills_str
    )

    if print_prompt is True:
        print(prompt)

    if not interview:
        conversation_str = "No conversation history provided. Please provide a prompt."
    else:
        conversation_str = '\n'.join(interview)

    interview_agent = get_agent(prompt, model_id=model)
    agent_response = interview_agent.structured_output(output_model=InterviewAgentMessage, prompt=conversation_str)
    return agent_response

def route_message_to_agent(
    userInterview,
    model: str = "mistral-medium-latest"
) -> InterviewAgentMessage:
    if userInterview.interview_state == InterviewState.INITIAL_INTERVIEW:
        agent_response = get_agent_message_for_initial_interview(userInterview.interview, model=model)
    elif userInterview.interview_state == InterviewState.JOB_DOMAIN_INTERVIEW:
        agent_response = get_agent_message_for_job_extension_interview(userInterview.interview, model=model)
    elif userInterview.interview_state == InterviewState.JOB_FEEDBACK_INTERVIEW:
        agent_response = get_agent_message_for_job_feedback_interview(userInterview, model=model)
    elif userInterview.interview_state == InterviewState.TRAINING_DOMAIN_INTERVIEW:
        agent_response = get_agent_message_for_training_domain_interview(userInterview.interview, model=model)
    elif userInterview.interview_state == InterviewState.TRAINING_FEEDBACK_INTERVIEW:
        agent_response = get_agent_message_for_training_feedback_interview(userInterview, model=model)
    elif userInterview.interview_state == InterviewState.OPEN_DISCUSSION:
        agent_response = get_agent_message_for_open_discussion(userInterview.interview, model=model)
    else:
        print(f"interview_state not supported : {userInterview.interview_state}")
        return None
    return agent_response