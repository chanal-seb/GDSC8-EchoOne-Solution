import sys
from typing import List

sys.path.append('..')

from live_chat.my_utils import (
    get_agent
)

from live_chat.models.persona_info import (
    InitialPersonaInfo,
    JobPersonaInfo,
    PersonaInfo,
    PersonaSkillsInterest,
    LoacationNameRefator
)

from live_chat.prompts.persona_extraction_prompt import (
    PERSONA_INITIAL_EXTRACTION_PROMPT,
    PERSONA_INTEREST_EXTRACTION_PROMPT,
    PERSONA_JOB_EXTRACTION_PROMPT,
    PERSONA_SKILL_DOMAINS_CLASSIFICATION_PROMPT,
    LOCATION_NAME_REFACTORING
)

def location_name_refactoring(
    location: str,
    model: str = "mistral-small-latest",
    print_prompt=False
) -> LoacationNameRefator:

    prompt = LOCATION_NAME_REFACTORING.format(
        location=location
    )

    if print_prompt is True:
        print("\n" + "="*50)
        print(prompt)
        print("\n" + "="*50)

    # return None

    extraction_agent = get_agent(model_id=model, temperature=0.0)
    result = extraction_agent.structured_output(output_model=LoacationNameRefator, prompt=prompt)

    return result

def extract_initial_persona_info(
    conversation: List[str],
    model: str = "mistral-small-latest",
    print_prompt=False
) -> InitialPersonaInfo:
    """Extract persona info from conversation using Persona Extraction Agent"""
    text = '\n'.join(conversation)
    #print(text)

    prompt = PERSONA_INITIAL_EXTRACTION_PROMPT.format(
        conversation=text
    )

    if print_prompt is True:
        print(prompt)

    # return None

    extraction_agent = get_agent(model_id=model, temperature=0.0)
    result = extraction_agent.structured_output(output_model=InitialPersonaInfo, prompt=prompt)

    persona_info = PersonaInfo()
    persona_info.name = result.name
    persona_info.age = result.age
    persona_info.location = result.location
    persona_info.goals = result.goals
    
    result_location_name_refactoring = location_name_refactoring(
        persona_info.location,
        model="mistral-medium-latest",
        print_prompt=False
    )
    if result_location_name_refactoring.renaming_needed is True:
        persona_info.location = result.name

    persona_info.recommendation_type = 'awareness'
    if result.interested_by_training is True:
        persona_info.recommendation_type = 'trainings_only'
    if result.interested_by_job is True:
        persona_info.recommendation_type = 'jobs_trainings'
        
    return persona_info

def extract_recommendation_type(
    conversation: List[str],
    model: str = "mistral-small-latest",
    print_prompt=False
) -> InitialPersonaInfo:
    """Extract persona info from conversation using Persona Extraction Agent"""

    text = '\n'.join(conversation)

    prompt = PERSONA_INTEREST_EXTRACTION_PROMPT.format(
        conversation=text
    )

    if print_prompt is True:
        print(prompt)

    extraction_agent = get_agent(model_id=model, temperature=0.0)
    result = extraction_agent.structured_output(output_model=InitialPersonaInfo, prompt=prompt)

    if print_prompt is True:
        print(result)
        
    persona_info = PersonaInfo()
    persona_info.name = result.name
    persona_info.location = result.location
    persona_info.goals = result.goals
    persona_info.education_level = result.education_level
    
    result_location_name_refactoring = location_name_refactoring(
        persona_info.location,
        model="mistral-medium-latest",
        print_prompt=False
    )
    if result_location_name_refactoring.renaming_needed is True:
        persona_info.location = result.name

    persona_info.recommendation_type = 'awareness'
    if result.interested_by_training is True:
        persona_info.recommendation_type = 'trainings_only'
    if result.interested_by_job is True:
        persona_info.recommendation_type = 'jobs_trainings'

    return persona_info

def extract_job_persona_info(
    activities_domains: str,
    conversation: List[str],
    previous_goal: str,
    model: str = "mistral-small-latest",
    print_prompt=False
) -> JobPersonaInfo:
    """Extract persona info from conversation using Persona Extraction Agent"""
    text = '\n'.join(conversation)
    #print(text)

    prompt = PERSONA_JOB_EXTRACTION_PROMPT.format(
        activities_domains=activities_domains,
        conversation=text,
        previous_goal=previous_goal
    )

    if print_prompt is True:
        print("\n" + "="*50)
        print(prompt)
        print("\n" + "="*50)

    # return None

    extraction_agent = get_agent(model_id=model, temperature=0.0)
    result = extraction_agent.structured_output(output_model=JobPersonaInfo, prompt=prompt)

    return result

def extract_skill_domain_info(
    formatted_domains,
    interview,
    model: str = "mistral-small-latest",
    print_prompt: bool = False
) -> PersonaSkillsInterest:

    text = '\n'.join(interview)
    
    prompt = PERSONA_SKILL_DOMAINS_CLASSIFICATION_PROMPT.format(
        formatted_domains=formatted_domains,
        conversation=text
    )

    if print_prompt is True:
        print(prompt)
    
    extraction_agent = get_agent(model_id=model, temperature=0.0)
    result = extraction_agent.structured_output(output_model=PersonaSkillsInterest, prompt=prompt)

    return result