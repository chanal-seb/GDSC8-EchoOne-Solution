import sys
from typing import List
from pathlib import Path

sys.path.append('..')

from live_chat.agents.agent_utils import matching_agent_process_jobs

from live_chat.models.persona_info import (
    InterviewState,
    UserInterview,
    PersonaInfo
)
from live_chat.agents.extraction_agents import (
    extract_initial_persona_info,
    extract_recommendation_type,
    extract_job_persona_info,
    extract_skill_domain_info
)

from live_chat.my_utils import (
    read_json
)

DATA_DIR = Path('../live_chat/data')

# Load jobs domains map data
filename = f"map_clusters_jobs_v4.json"
save_path = DATA_DIR / filename
jobs_map = read_json(save_path)
jobs_map_lower = {key.lower(): value for key, value in jobs_map.items()}


filename = f"skill_domains_v3.json"
save_path = DATA_DIR / filename
skills_map = read_json(save_path)

def parse_conversation_for_initial_interview(
    conversation: List[str],
    model: str = "mistral-medium-latest",  
    print_prompt: bool = False
) -> PersonaInfo:
    """
    Parses the initial interview conversation to extract persona information.
    """
    persona_info = extract_initial_persona_info(
        conversation,
        model=model,
        print_prompt=print_prompt
    )
    return persona_info

def parse_conversation_for_job_persona_info(
    userInterview: UserInterview,
    activities_domains: str,
    conversation: List[str],
    previous_goal: str,
    model: str = "mistral-medium-latest",
    print_prompt=False
) -> PersonaInfo:
    persona_info = userInterview.persona_info

    result = extract_recommendation_type(
        conversation=userInterview.interview,
        model=model,
        print_prompt=print_prompt
    )

    recommendation_type = result.recommendation_type
    if recommendation_type in ['jobs_trainings', 'trainings_only', 'awareness']:
        persona_info.recommendation_type = recommendation_type
    else:
        return persona_info

    result = extract_job_persona_info(
        activities_domains=activities_domains,
        conversation=conversation,
        previous_goal=previous_goal,
        model=model,
        print_prompt=print_prompt
    )

    persona_info.open_to_relocate_for_work = result.open_to_relocate_for_work
    persona_info.work_type_preference = result.work_type_preference
    persona_info.education_level = result.education_level
    persona_info.years_of_experience = result.years_of_experience
    persona_info.languages = result.languages
    persona_info.goals = result.goals
    persona_info.target_domains = result.target_domains

    if persona_info.education_level == 'Técnólogo':
        # print('Técnólogo renamed in Tecnólogo')
        persona_info.education_level = 'Tecnólogo'

    return persona_info

def parse_conversation(
    userInterview: UserInterview,
    verbose = False
) -> UserInterview:
    if userInterview.interview_state == InterviewState.INITIAL_INTERVIEW:
        persona_info = parse_conversation_for_initial_interview(userInterview.interview, print_prompt=False)
        userInterview.persona_info = persona_info
        if persona_info.recommendation_type == 'jobs_trainings':
            userInterview.interview_state = InterviewState.JOB_DOMAIN_INTERVIEW
        elif persona_info.recommendation_type == 'trainings_only':
            userInterview.interview_state = InterviewState.TRAINING_DOMAIN_INTERVIEW
        else:
            userInterview.interview_state = InterviewState.OPEN_DISCUSSION
    elif userInterview.interview_state == InterviewState.JOB_DOMAIN_INTERVIEW:
        domains_str = ""
        for domain in jobs_map:
            domains_str += f"  - {domain} : {jobs_map[domain]['description']}" + "\n"

        persona_info = parse_conversation_for_job_persona_info(
            userInterview,
            activities_domains=domains_str,
            conversation=userInterview.interview,
            previous_goal=userInterview.persona_info.goals,
            print_prompt=False
        )
        #print(persona_info)
        userInterview.persona_info = persona_info
        if persona_info.recommendation_type == 'jobs_trainings':
            result = matching_agent_process_jobs(0, userInterview.persona_info, verbose=verbose)
            #print(result)

            userInterview.interview_state = InterviewState.JOB_FEEDBACK_INTERVIEW
        elif persona_info.recommendation_type == 'trainings_only':
            userInterview.interview_state = InterviewState.TRAINING_DOMAIN_INTERVIEW
        else:
            userInterview.interview_state = InterviewState.OPEN_DISCUSSION
    elif userInterview.interview_state == InterviewState.TRAINING_DOMAIN_INTERVIEW:
        
        domains_str = ""
        for domain in skills_map['domains']:
            domains_str += f"  - {domain} : {skills_map['domains'][domain]}" + "\n"

        persona_info = userInterview.persona_info
        
        result = extract_skill_domain_info(
            formatted_domains=domains_str,
            interview=userInterview.interview
        )
        
        persona_info.skills_domains = result.list_of_skills
        userInterview.persona_info = persona_info
        userInterview.interview_state = InterviewState.TRAINING_FEEDBACK_INTERVIEW
    else:
        userInterview.interview_state = InterviewState.OPEN_DISCUSSION
    return userInterview