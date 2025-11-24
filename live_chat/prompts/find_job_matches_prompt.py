FIND_JOB_MATCHES_PROMPT = """
You are a job advisor expert in matching jobs to candidate profiles.

Your task is to decide which jobs directly or partially support the candidate's goals.

Candidate goal:
{candidate_profile}

You are given a list of jobs:
{jobs}

For each job, select it if it fully or partially contributes to the candidate's goal, even if it does not cover all aspects.
Clearly explain how the job supports the goal, even if only partially.

Return the list of job IDs you have selected and rationale.
"""

FIND_JOB_MATCHES_PROMPT_v1 = """
You are a job advisor expert in matching jobs to candidate profile.
Your task is to decide which jobs directly supports the candidate's goals.

Candidate goal:
{candidate_profile}

You are given a list of jobs:

# Available jobs:
{jobs}

Decide if any job matches the candidate's goals.

Return the list of job IDs you have selected and rationale.
"""

FIND_TRAINING_MATCHES_PROMPT_v3 = """
Available trainings:
{trainings}

Candidate profile:
{candidate_profile}

Analyze the candidate profile and available trainings to return up to 4 training IDs that would best benefit this candidate. Consider the following factors in your selection:

1. Prioritize trainings that directly align with the candidate's stated goals and target domains.
2. Match the training level (Basic, Intermediate, Advanced) to the candidate's education and experience.
3. Ensure the selected trainings are highly relevant to the candidate's target industry or domain.
4. Consider the candidate's language preferences when selecting trainings.
5. Avoid recommending trainings that are only tangentially related to the candidate's profile or goals.

For each recommended training, provide:
1. The training ID
2. A brief explanation of its relevance to the candidate's profile and goals
3. A relevance score from 1-10, where 10 is extremely relevant and 1 is barely relevant

Return the result as a JSON object with this structure:
{
  "recommendations": [
    {
      "id": "tr001",
      "explanation": "This training...",
      "relevance_score": 9
    },
    ...
  ]
}
"""

FIND_TRAINING_MATCHES_PROMPT_v2 = """
Available trainings:
{trainings}

Candidate profile:
{candidate_profile}

Analyze the candidate profile and available trainings to return up to 4 training IDs that would best benefit this candidate. Consider the following factors in your selection:

1. Prioritize trainings that directly align with the candidate's stated goals and target domains.
2. Match the training level (Basic, Intermediate, Advanced) to the candidate's education and experience.
3. Ensure the selected trainings are highly relevant to the candidate's target industry or domain.
4. Consider the candidate's language preferences when selecting trainings.
5. Focus on practical, hands-on trainings if the candidate expresses interest in such experiences.
6. Avoid recommending trainings that are only tangentially related to the candidate's profile or goals.

Return the result as a JSON list of training IDs, like ["tr001", "tr002", "tr003", "tr004"].
"""

FIND_TRAINING_MATCHES_PROMPT_v1 = """
Available trainings:
{trainings}

Candidate profile:
{candidate_profile}

Analyze the candidate profile and available trainings to return up to 4 training IDs that would best benefit this candidate. Consider the following factors in your selection:

1. Match the training level (Basic, Intermediate, Advanced) to the candidate's education and experience.
2. Prioritize trainings that align with the candidate's stated goals and target domains.
3. Consider the candidate's language preferences when selecting trainings.
4. Focus on practical, hands-on trainings if the candidate expresses interest in such experiences.
5. Ensure the selected trainings are relevant to the candidate's target industry or domain.

Return the result as a JSON list of training IDs, like ["tr001", "tr002", "tr003", "tr004"].
"""