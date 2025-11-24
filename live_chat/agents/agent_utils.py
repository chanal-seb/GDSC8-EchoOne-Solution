import sys
from pathlib import Path

sys.path.append('..')

from live_chat.models.generic_models import ListOfIds
from live_chat.models.job_info import JobInfo
from live_chat.models.persona_info import PersonaInfo
from live_chat.my_utils import (
    save_json,
    read_json,
    get_agent
)
from live_chat.prompts.find_job_matches_prompt import FIND_JOB_MATCHES_PROMPT

DATA_DIR = Path('../live_chat/data')

# Load jobs domains map data
filename = "map_clusters_jobs_v4.json"
save_path = DATA_DIR / filename
jobs_map = read_json(save_path)
jobs_map_lower = {key.lower(): value for key, value in jobs_map.items()}

# Load Jobs data
filename = f"final_jobs_v4.json"
jobs_save_path = DATA_DIR / filename
jobs_data = read_json(jobs_save_path)
jobs_info = {
    job_id: JobInfo.model_validate_json(data)
    for job_id, data in jobs_data.items()
}

def get_jobs_by_target_domains(persona_target_domains, jobs_map):
    jobs_ids = []

    for domain in persona_target_domains:
        for job_id in jobs_map_lower[domain.lower()]['job_ids']:
            jobs_ids.append(job_id)
    return jobs_ids

def hard_filter_jobs(persona_info, job_ids, jobs_info, verbose=False):
    filtered_job_ids = []

    for job_id in job_ids:
        if verbose is True:
            print(job_id)
        job_info = jobs_info[job_id]

        if job_info.work_type == 'onsite':
            if persona_info.open_to_relocate_for_work is False and job_info.location != persona_info.location:
                if verbose is True:
                    print(f"excluded because of location : {job_info.location} - {persona_info.location}")
                continue

        if verbose is True:
            print("Location OK")

        job_education_level = job_info.get_education_level_value()
        if job_education_level == -1:
            print(f"ERROR : job_education_level not recognized : {job_info.education_level_required}")

        persona_education_level = persona_info.get_education_level_value()
        if persona_education_level == -1:
            print(f"ERROR : persona_education_level not recognized : {persona_info.education_level}")

        if job_education_level > persona_education_level:
            if verbose is True:
                print(f"excluded because of education level : {job_education_level} - {persona_education_level}")
            continue

        if job_info.years_of_experience_required > persona_info.years_of_experience:
            if verbose is True:
                print(f"excluded because of experience : {job_info.years_of_experience_required} - {persona_info.years_of_experience}")
            continue

        is_language_match = False
        if len(persona_info.languages) > 0:
            for job_language in job_info.required_languages:
                for persona_language in persona_info.languages:
                    if job_language == persona_language:
                        is_language_match = True
            if is_language_match is False:
                if verbose is True:
                    print("excluded because of language")
                continue

        filtered_job_ids.append(job_id)
        
    return filtered_job_ids

def review_job_matches(
    persona_info: PersonaInfo,
    jobs_text: str,  # Pre-built context to avoid rebuilding
    model: str = "mistral-medium-latest",
    print_prompt=False
) -> ListOfIds:
    """Find suitable jobs for a persona using semantic matching"""

    prompt = FIND_JOB_MATCHES_PROMPT.format(
            candidate_profile=persona_info.goals,
            jobs=jobs_text
        )

    if print_prompt is True:
        print(prompt)

    # return []
    agent = get_agent(model_id=model, temperature=0.0)
    response = agent.structured_output(output_model=ListOfIds, prompt=prompt)

    # print(response)
    # Track cost
    # track_api_call(response, model)

    return response

def matching_agent_process_jobs(persona_id, persona_info, verbose=False):
    ###
    # Get jobs matching persona targeted activity domains
    ###
    print(persona_info.target_domains)
    filtered_jobs_ids = get_jobs_by_target_domains(persona_info.target_domains, jobs_map)
    if verbose is True:
        print(f"filtered_jobs_ids : {filtered_jobs_ids}")

    ###
    # Apply hard filters 
    ###
    hard_filtered_jobs_ids = hard_filter_jobs(persona_info, filtered_jobs_ids, jobs_info, verbose=verbose)
    if verbose is True:
        print(f"hard_filtered_jobs_ids : {hard_filtered_jobs_ids}")

    if len(hard_filtered_jobs_ids) == 0:
        # no jobs remaining
        selected_jobs_ids = []
        rationale = ''
    else:    
        ###
        # Review job list according to persona goal
        ###
        jobs_text = ""
        for job_id in hard_filtered_jobs_ids:
            jobs_text += jobs_info[job_id].get_info_for_matching(job_id) + "\n\n"
    
        result = review_job_matches(persona_info, jobs_text, print_prompt=verbose)
        selected_jobs_ids = result.list_of_ids
        rationale = result.rationale
    
    if verbose is True:
        print(f"selected_jobs_ids : {selected_jobs_ids}")
    
    return hard_filtered_jobs_ids, selected_jobs_ids, rationale
