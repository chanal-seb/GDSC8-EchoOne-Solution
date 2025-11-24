JOB_EXTRACTION_PROMPT = """Extract detailed information from this job description in Brazil. Return a structured job profile with these fields:
- Title: The job title
- Job description: Short summary of the job
    - Don't focus on experience or skills, be focus on the main job activity and purpose.
    - Make sure description capture all main general information
    - Focus of additional details that are not already explained by the job title field
    - Keep it short (maximum approximately 15 words)
- Location: The city where the job is located. (Do no not mention state or country). Just use standard city name.
- Work type: The work arrangement ('onsite', 'remote', or 'hybrid')
    - onsite: Requires physical presence at the workplace
    - remote: Can be performed entirely from a distance
    - hybrid: Combines remote and onsite work
- Education level required: The minimum education level required (one of: Ensino Fundamental, Ensino Médio, Técnico, Tecnólogo, Graduação, Bacharelado, Licenciatura, Pós-graduação, Especialização, Mestrado, MBA, Doutorado)
- Years of experience required: The minimum years of experience needed (as a number)
- Required languages: Languages needed for the job :
    - Use strict formating for language name:
        - use english term
        - starting with Capital letter, the rest in lowercase letter
        - no location attribute (like Brasilian), just one word

Job description:
"""

DOMAIN_LABELING_PROMPT = """
You are an expert in skill taxonomy, training analysis and job description analysis.

From this jobs information:
{jobs_description}

Propose a name for the activity domain that categorizes the jobs group listed above. The name shall be generic enough to fit with all jobs but specific enough to capture the unique character of the group.

When creating the description, you must explicitly mention the primary industry sectors identified in the job data (e.g., Banking, Insurance).

Format the activity domain label using **Title Case** (capitalize the first letter of each word, the rest lowercase).

If you detect jobs that seem to be outliers in function, note them in the justification. However, if a job introduces a specific industry sector not present elsewhere, ensure this sector is captured in the description for completeness.

Return your reply with following fields:
- The activity domain name
- Short description of the activity domain
    - Make sure description capture all main general information
    - Focus of additional details that are not already explained by the domain title field
    - Keep it short (maximum approximately 15 words)
- The justification of your decision
"""

JOB_SUMMARY_PROMPT = """
You are an expert in jobs description summarization.
Your task is to compute a short description of following job description.
Don't focus on experience or skills, be focus on the main job activity and purpose.
Make sure description capture all valuable details.

When ready return the description without any explanation or additional text.
Just reply the description like it is.

Job description:
"""

ACTIVITY_DOMAIN_JOB_EXTRACTION_PROMPT = """
You are an expert in jobs activity domain taxonomy and job description analysis.

From this job information:
--- BEGIN JOB DESCRIPTION ---
{job_description}
--- END JOB DESCRIPTION ---

Extract the **activity domain** as much as possible coming from the following activity domains list:
{activities_domains}

# Guidelines (IMPORTANT !) :
1. You can only use activities domain from the provided list.
2. You can pick several activity domains. But don't be too much wide.
3. Use exact same domain name (Do not change any letter or caps).
4. If no matching domain is found in the provided lists, return an empty.
5. Return the list of domains. Don't add any explanation or additional text
"""

FIND_TRAINING_MATCHES_PROMPT = """
You are an expert in skill taxonomy, training analysis, and job description interpretation.

Your task is to identify which skill —among a predefined list—cover the skills required for the job described below.

# Job Description:
{job_description}

# Existing Skills:
{formatted_skills}

# Instructions:
- Carefully read the job description and compare it to the list of existing skills.
- If the job clearly mentions skills that align with one or more skills, respond with a list of skills with their required proficiency levels (Basic, Intermediate, or Advanced)
- If none of the skills match the job description, respond with an empty list:
   []
- Be conservative:
    - select only skills that clearly mentioned in the job description.
    - do not derived needed skills from vague competence description. (Hint: if no proficency level is defined(Basic, Intermediate, or Advanced), consider it is vague)
- Do NOT modify, rename, or create new skills.
- IMPORTANT:
   - You MUST use only the skills listed in 'Existing Skill Domains'.
   - NEVER infer or reuse skill names from the job description if they are not in the provided list (but select closer in the list).
   - If no match is found, return an empty list.

Respond with foowing fields :
- Required skills: Dictionary of skills with their required proficiency levels (Basic, Intermediate, or Advanced)
- rationale: Justification of the decision
"""

JOB_EXTRACTION_PROMPT_v1 = """Extract detailed information from this job description in Brazil. Return a structured job profile with these fields:
- Title: The job title
- Domain: The professional domain/sector (provide a detailed 3-8 word phrase describing the specific field, industry, and specialization).
- Location: The city where the job is located. (Do no not mention state or country). Just use standard city name.
- Work type: The work arrangement ('onsite', 'remote', or 'hybrid')
- Education level required: The minimum education level required (one of: Ensino Fundamental, Ensino Médio, Técnico, Tecnólogo, Graduação, Bacharelado, Licenciatura, Pós-graduação, Especialização, Mestrado, MBA, Doutorado)
- Years of experience required: The minimum years of experience needed (as a number)
- Required skills: Dictionary of skills with their required proficiency levels (Basic, Intermediate, or Advanced)
    - Use strict formating for skill name: 
        - starting with Capital letter, the rest in lowercase letter
- Required languages: Languages needed for the job :
    - Use strict formating for language name:
        - use english term
        - starting with Capital letter, the rest in lowercase letter
        - no location attribute (like Brasilian), just one word

Be precise in extracting skill levels - they are critical for matching. If a skill level isn't specified, assume 'Básico'.

For the domain field, don't just provide a single word like "technology" or "agriculture". Instead, extract a detailed phrase that captures both the broader industry and the specific specialization or focus area mentioned in the job description. For example:
- "Renewable solar energy development"
- "Digital marketing for e-commerce platforms"
- "Financial analysis for sustainable investments"
- "Software development for healthcare systems"
- "Urban landscape architecture and planning"

This detailed domain information will be crucial for accurate job matching.

For work type, determine if the job is:
- onsite: Requires physical presence at the workplace
- remote: Can be performed entirely from a distance
- hybrid: Combines remote and onsite work

Job description:
"""

