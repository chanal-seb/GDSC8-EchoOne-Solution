FIND_TRAINING_MATCHES_PROMPT_BY_NAME = """
You are a job advisor expert in matching trainings to candidate profile.
Your task is to recommend trainings that directly support the following goal: {candidate_profile}
You know about a list of trainings, each associated with a specific skill.

Select only the trainings that are directly related to the goal above, based on the relevance of the acquired skill to the goal.

Return formated result as a JSON list of training IDs, like ["tr001", ...].

List of Trainings and Associated Skills:
{trainings} 
"""

CHECK_PERSONA_TRAINING_MATCH = """
You are a job advisor expert in matching trainings to candidate profiles.
Your task is to decide if a training directly supports the candidate's profile.

The candidate profile includes:
- A list of skills already acquired by the candidate, with current levels.
- The candidate's stated goal.

Candidate profile:
{candidate_profile}

You are given a training that provides a specific skill and level:
{training}

Decide if the training matches the profile according to the following rules:

A training matches only if **all** the following conditions are met:
1. The skill taught is directly aligned with the candidate's stated goal.
2. The skill taught level (Basic, Intermediate, Advanced) is exactly one level above the candidate's current level in the same skill domain.
    - if candidate as no level, propose Basic
    - if candidate as Basic level, propose Intermediate
    - ...
    - do not assume that a related skill qualifies the candidate for a higher level in a different skill domain. Each skill domain must be treated independently.
- Avoid recommending trainings that are only tangentially related to the candidate's goals(VERY IMPORTANT).


Return a JSON object with:
- "istrue": True if match or False if not
- "rationale": A short explanation of the decision, clearly referencing the rule(s) applied.
"""


FIND_TRAINING_MATCHES_PROMPT = """
You are a job advisor expert in matching trainings to candidate profile.
Your task is to decide which trainings directly supports the candidate's profile.

The candidate profile includes:
- A list of skills already acquired by the candidate, with current levels.
- The candidate's stated goal.

Candidate profile:
{candidate_profile}

You are given a list of training that provides specific skill and level:

# Available trainings:
{trainings}

Decide if the training matches the profile according to the following rules:

A training matches only if **all** the following conditions are met:
- The skill taught is directly aligned with the candidate's stated goal.
- The skill taught level (Basic, Intermediate, Advanced) is exactly one level above the candidate's current level in the same skill domain.
    - if candidate as no level, propose Basic
    - if candidate as Basic level, propose Intermediate
    - ...
    - do not assume that a related skill qualifies the candidate for a higher level in a different skill domain. Each skill domain must be treated independently.
- Avoid recommending trainings that are only tangentially related to the candidate's goals(VERY IMPORTANT).

Return the list of training IDs you have selected.
"""

FIND_TRAINING_MATCHES_FOR_JOB_PROMPT = """
You are a job advisor expert in matching trainings to candidate profile.
Your task is to decide which trainings directly supports the candidate's profile to apply for a job.

Candidate profile (list of skills already acquired by the candidate, with current levels):
{candidate_skills}

Job required skills with expected levels:
{job_skills}

# Available trainings with taught skills and acquired levels:
{trainings}

Training recommendations must follow a strict level-by-level progression:
- If the persona has no knowledge of a skill and the job requires Intermediate, suggest both Basic and Intermediate.
- If the persona has Basic and the job requires Advanced, suggest Intermediate and Advanced (if available).
- More generally: if the persona is at level p and the job requires r, you must propose all trainings available from p+1 to r.

Return the list of training IDs you have selected.
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