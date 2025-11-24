PERSONA_INITIAL_EXTRACTION_PROMPT = """From the interview conversation, extract the following fields and return a structured profile with these fields:
- Age: The person's age as a number.
    - if age is not given but you know user has below 16, set age = 10
    - if age is not given but you know user has at least 16 or above, set age = 20
- Location: The city where the person lives
- Interested by job: True if the person expresses interest in employment, even if they are undecided or considering other options.
- Interested by training: True if Person is interested to find a training. Even if not completely sure
- Goals: Their stated career or learning objectives.
    - Make sure to capture all meaningful informations that will help understand acticity domain or skills domain in relatiob to candidate profile or goal.

If the person is exploring career paths like comparing job vs training, consider this as interest in job and training

For any information not explicitly mentioned:
- If they're just seeking information rather than specific jobs/training, capture this in goals

Be precise and only extract information that's actually present or can be reasonably inferred. Don't invent details.

Conversation:
{conversation}
"""

LOCATION_NAME_REFACTORING = """
You are a location harmonization agent. Your task is to process a single persona's location string provided as "{location}".

Follow these rules:
1.Trim and clean the input string.
2.If the input contains a city followed by a country (e.g., "Fortaleza, Brazil"), extract and normalize the city name only.
3.VERY IMPORTANT : Normalize known aliases:
- "Rio" → "Rio de Janeiro"
- "Recife, Brazil" → "Recife"
- "Fortaleza, Brazil" → "Fortaleza"
4.If the input is empty, ambiguous (e.g., ":", "Brazil"), or not a valid city, return "Unknown".
5.Return a Python object of class LocationNameRefator with:
- renaming_needed = True if the name was changed or cleaned.
- renaming_needed = False if the input was already clean.
- name = "<standardized city name>" or "Unknown" if invalid.
- rationale = justification of your decision
"""

PERSONA_JOB_EXTRACTION_PROMPT = """
From the interview conversation, extract the following fields and return a structured profile with these fields:
- Open to relocate for work: Whether they've mentioned being willing to move for work (true/false)
- Work type preference: Their preferred work arrangement (onsite, remote, or hybrid)
- Education level: Their highest completed education level. PICK EXACT LABEL NAME FROM  : Ensino Fundamental, Ensino Médio, Técnico, Tecnólogo, Graduação, Bacharelado, Licenciatura, Pós-graduação, Especialização, Mestrado, MBA, Doutorado). IMPORTANT reuse exact same labels !
- Years of experience: Their professional experience in years (as an integer)
- Languages: Languages they speak
    - Use strict formating for language name:
        - use english term
        - starting with Capital letter, the rest in lowercase letter
        - no location attribute (like Brasilian), just one word
- Goals: Their stated career or learning objectives.
    - Knowing previous stated goal by user was : {previous_goal}
    - Make sure to capture all meaningful informations that will help understand acticity domain or skills domain in relation to candidate profile or goal.
- Target domains: Professional domains/sectors they're interested in.
    - It shall be from **ACTIVITIES DOMAINS LIST**
    - It shall use exact same names (Do not change any letter or caps)
    - If no match at all use UNKNOWN as single domain name

For any information not explicitly mentioned:
- If education level isn't specified, use "unknown" rather than guessing

Be precise and only extract information that's actually present or can be reasonably inferred. Don't invent details.

ACTIVITIES DOMAINS LIST:
{activities_domains}

Conversation:
{conversation}
"""

PERSONA_SKILL_DOMAINS_CLASSIFICATION_PROMPT = """
You are an expert in skill taxonomy, training analysis and candidate profile description analysis.

Your task is to evaluate whether the candidate is interesting by any of the existing skill domains based on the interview conversation.

# Existing Skill Domains:
{formatted_domains}

Each domain is represented as `'Domain Name'`.

# Instructions:
1. Carefully read the interview conversation and compare it to the domain list.
2. Do not modify or rename existing domains. Especially, do not replace And by and or And by and.
3. You are not authorized to create new skill domains.
- You MUST use only the domains listed above.
- Do NOT infer or map user interests to domains not explicitly listed.
4.Return a Python object of class ListOfStrs with:
- list_of_skills = List of skills persona shows interest in.
- rationale = justification of your decision
- interested_by_training = True by default
5.If the user explicitly states they are not interested in any of the listed trainings and expresses no interest in training in any other domain, return:
- interested_by_training = False
6.If the user explicitly states they are unsure about training in any of the listed domains and expresses no interest in training in any other domain, return:
- interested_by_training = False
7.If the user expresses interest in training outside the provided list, return:
- interested_by_training = True

Conversation:
{conversation}
"""

PERSONA_SKILL_DOMAINS_CLASSIFICATION_PROMPT_ALT = """
You are an expert in skill taxonomy, training analysis and candidate profile description analysis.

Your task is to evaluate whether the candidate is interesting by any of the existing skill domains based on the interview conversation.

# Existing Skill Domains:
{formatted_domains}

Each domain is represented as `'Domain Name'`.

# Instructions:
1. Carefully read the interview conversation and compare it to the domain list.
2. Do not modify or rename existing domains.
3. IMPORTANT : you are not authorized to create new skill domain.
    - you MUST use skill domains listed in 'Existing Skill Domains' list exclusively
    - NEVER report a skill domain if it is not part of 'Existing Skill Domains' list
    - if you find no match return an empty list without reusing skill domain present in candidate profile
4.Return a Python object of class ListOfStrs with:
- list_of_strs = List of domain persona shows interest in.
- rationale = justification of your decision

FINAL INSTRUCTION : Analyse user feedback about user motivation to take trainings.
reply ['NOT_INTERESTED'] if all following conditions are met :
- user mention that he is not interested by any training in the proposed list or in any other domain

Conversation:
{conversation}
"""

PERSONA_ACTIVITY_DOMAINS_CLASSIFICATION_PROMPT = """
You are an expert in skill taxonomy, training analysis and candidate profile description analysis.

Your task is to evaluate whether the following candidate profile description matches any of the existing activity domains.

# Candidate profile:
{persona_description}

# Existing Activity Domains:
{formatted_domains}

Each domain is represented as `'Domain Name'`.

# Instructions:
1. Carefully read the candidate profile and compare it to the domain descriptions.
2. If the candiadate goal clearly fits within one or more domains, respond with formatted list:
   ['Domain Name A', 'Domain Name B', ...]
3. If the candiadate goal does **not** fit any existing domain, respond with empty list:
   []
4. Don't be too much conservative: if domains looks close, take it.
5. Do not modify or rename existing domains.
6. IMPORTANT : you are not authorized to create new activity domain.
    - you MUST use activity domains listed in 'Existing Activity Domains' list exclusively
    - NEVER report a activity domain present in candidadate if it is not part of 'Existing Activity Domains' list
    - if you find no match return an empty list without reusing any activity domain present in candiadate profile

Respond with the list of domains you have selected.
"""

PERSONA_JOBS_EXTRACTION_PROMPT = """
You are given :
- a list of jobs
- an interview conversation with a persona.

LIST OF AVALAIBLE JOBS:
{jobs_list}

From the conversation, extract the job ids (matching available jobs list) for which the user show interest.

# Guidelines (IMPORTANT !) :
1. Analyse user feedback about user motivation to find jobs.
    IMPORTANT :
        - If user is finally not interested by finding job (can seeking for training first or searching information only), reply with list_of_ids=['NOT_INTERESTED'] and do not perform following instructions.
        - If user is interested by jobs but not from the list, reply with list_of_ids=[]
2. Select only jobs user show interest in.
3. Use exact id label.
4. In the case you conclude user is 

Conversation:
{conversation}
"""

PERSONA_JOB_SKILLS_EXTRACTION_PROMPT = """
You are given :
- a list of required skills for a job application
- an interview conversation with a persona.

LIST OF AVALAIBLE SKILLS:
{skills_list}

From the conversation, extract the skill names (matching available skills list) and user current proficiency level (LIMITED TO None, Basic, Intermediate, or Advanced).

# Guidelines (IMPORTANT !) :
1. Extract only skills that persona gives feedback on and that are present in available skills list.
2. Use exact same skill name that provided in the available skills list. Do not change any letter or caps. Do not add formating characters.
3. Return only the skills and proficency level. Don't add any explanation or additional text (IMPORTANT)

Conversation:
{conversation}
"""

PERSONA_SKILLS_EXTRACTION_PROMPT_marche_pas = """
You are an advanced AI assistant specializing in skill extraction from text. Your task is to analyze a conversation and a corresponding list of skills to identify which skills a persona is interested in and their current proficiency level.

You will be given the following inputs:
- a list of required skills for a job application : [LIST OF AVAILABLE SKILLS]
- an interview conversation with a persona. : [CONVERSATION]

[LIST OF AVAILABLE SKILLS]:
{skills_list}
[END OF LIST OF AVAILABLE SKILLS]

[CONVERSATION]
{conversation}
[END OF CONVERSATION]

------------------
Follow the guidelines below with precision.
Your response must be generated by following this step-by-step process:
1. Identify the Primary Theme by Prioritizing Specific Goals:
    a. Prioritize Specificity (Crucial Rule): When analyzing the [CONVERSATION], you must prioritize specific, goal-oriented statements (e.g., "I want to learn about X," "I'm focused on Y") over broad, general expressions of interest (e.g., "everything sounds interesting," "all of them are great"). The specific goal is the true indicator of the persona's primary interest.
    b. Identify the primary theme keyword from the most specific goal-oriented statement.
    c. Strict Filtering: Use this primary theme keyword to strictly filter the [LIST OF AVAILABLE SKILLS]. Create a new, relevant sub-list that includes only the skills whose names contain this keyword.
    d. Edge Case: Only if the persona exclusively expresses broad interest without mentioning any specific domain or goal, should you use the full [LIST OF AVAILABLE SKILLS]. The presence of even one specific goal must trigger the filtering process.
2. Extract Interested Skills from the Relevant List:
    a. Using the filtered sub-list from Step 1, identify the specific skills for which the persona expresses interest.
    b. If the persona expresses general interest in the entire theme, you should select all skills from the filtered sub-list.
3. Determine Current Proficiency Level:
    a. For each skill selected in Step 2, determine the persona's current proficiency level. The only valid proficiency levels are: None, Basic, Intermediate, or Advanced.
4. Adhere to Strict Formatting Rules:
    a. Exact Naming: You must use the exact skill names as they appear in the original [LIST OF AVAILABLE SKILLS]. Do not alter capitalization, spelling, or add any formatting characters. Especially, do not replace And by and or And by and.
    b. Output Content: Your response must only contain the final extracted skills and their proficiency levels. Do not add any introductory text, explanations, apologies, or concluding remarks.
    c. Output Structure: Format the final output as a single Python dictionary, where keys are the skill name strings and values are the proficiency level strings.
"""

PERSONA_SKILLS_EXTRACTION_PROMPT_v1 = """
You are an advanced AI assistant specializing in skill extraction from text. Your task is to analyze a conversation and a corresponding list of skills to identify which skills a persona is interested in and their current proficiency level.

You will be given the following inputs:
- a list of required skills for a job application : [LIST OF AVAILABLE SKILLS]
- an interview conversation with a persona. : [CONVERSATION]

[LIST OF AVAILABLE SKILLS]:
{skills_list}

From the conversation, extract the skill names for which the persona is interested and their current proficiency level, limited to: None, Basic, Intermediate, or Advanced.

# Guidelines (IMPORTANT !) :
1. Extract only skills that persona express interest in and that are present in available skills list.
2. Use exact same skill name that provided in the available skills list. Do not change any letter or caps. Do not add formating characters.
3.If the user gives a targeted proficiency level, assume their current level is one level below.
4. Return only the skills and proficency level. Don't add any explanation or additional text (IMPORTANT)

Conversation:
{conversation}
"""

PERSONA_SKILLS_EXTRACTION_PROMPT = """
You are an advanced AI assistant specializing in skill extraction from text. Your task is to analyze a conversation and a corresponding list of skills to identify which skills a persona is interested in and their current proficiency level.

You will be given the following inputs:
- a list of required skills for a job application : [LIST OF AVAILABLE SKILLS]
- an interview conversation with a persona. : [CONVERSATION]

[LIST OF AVAILABLE SKILLS]:
{skills_list}
[END OF LIST OF AVAILABLE SKILLS]

[CONVERSATION]
{conversation}
[END OF CONVERSATION]

From the conversation, extract the skill names for which the persona is interested and their current proficiency level, limited to: None, Basic, Intermediate, or Advanced.

# Guidelines (IMPORTANT !) :
1. Analyse user feedback about user motivation to take trainings.
2. If the user expresses any hesitation, doubt, or explicitly says they do not need or want training (e.g., “I don’t need training yet”), you MUST set interested_by_training=False. Otherwise, set True.
3. Extract only skills that persona express interest in and that are present in available skills list.
4. Use exact same skill name that provided in the available skills list. Do not change any letter or caps. Do not add formating characters.
5. Return only the skills and proficency level. Don't add any explanation or additional text (IMPORTANT)
"""

PERSONA_INTEREST_EXTRACTION_PROMPT = """
You are given :
- an interview conversation with a persona.

From the interview conversation, extract following information:
- Persona interest based on the following precise definitions:
    - Interested by job: 
        - False if user clearly mention is not interested by job
        - Do not set to False if user show interest but lack confidence
    - interested_by_training:
        - False if user clearly mention is not interested by training
        - Do not set to False if user show interest but lack confidence

SPECIAL CASES:
- If user reply in poetic way to answer, try to understand 'behind the line'

Return following fields :
- interested_by_job
- interested_by_training
- rationale = justification of your choice

Conversation:
{conversation}
"""

PERSONA_AGE_CONSOLIDATION = """
You are given :
- an interview conversation with a persona.

From the interview conversation, extract following information:
- Age
    - if user has Ensino Fundamental education level and user shows signs that is not telling truth, be severe, set age to 15
    - in other cases, set -1

Return following fields :
- age
- rationale = justification of your choice

Conversation:
{conversation}
"""

PERSONA_INTEREST_EXTRACTION_PROMPT_v1 = """
You are given :
- an interview conversation with a persona.

From the interview conversation, extract persona interest based on the following precise definitions:
- Interested by job: True only if the persona shows clear and direct interest in one or more of the specific jobs proposed in the conversation.
    - Set to False if the user rejects the proposals or only gathers information for comparison before moving on.
- interested_by_job_in_different_domain: True only if the persona makes a targeted request for a specific type of job not currently being discussed.
    - A targeted request indicates the user has a clear idea of an alternative role they want (e.g., "I wonder if there’s a job focused only on painting?").
    - Set this to False if the persona makes a broad, exploratory inquiry about a new domain. An exploratory inquiry is characterized by general questions like "What kinds of roles exist in X field?" or "What skills are needed to get into X?". In this case, the interest is in understanding a field, not yet in a specific job.
- interested_by_training: True if the persona asks about or expresses interest in training, courses, certifications, or expresses concern about skill gaps they would need to fill for a role.
    - This applies to interest in training for either the proposed jobs or for a different domain.

Return following fields :
- interested_by_job
- interested_by_job_in_different_domain
- interested_by_training
- ratioanle = justification of your choice

Conversation:
{conversation}
"""


PERSONA_DOMAIN_CONFIRMATION_PROMPT = """
You are given :
- an interview conversation with a persona.

From the interview conversation and based on the User feedback, analyse if targets domains selected by Assistant match User wish.

Return a single word OK or NOK (IMPORTANT)

Conversation:
{conversation}
"""

PERSONA_TRAINING_SKILLS_EXTRACTION_PROMPT = """
You are given :
- a list of available skills taught by trainings in the area of a persona interest
- an interview conversation with a persona.

LIST OF AVAILABLE SKILLS TAUGHT BY TRAININGS:
{skills_list}

Derived from the conversation the skills that directly contribute to persona goal.
For each skill selected, evaluate the current proficiency level(LIMITED TO None, Basic, Intermediate, or Advanced) of the persona from the interview.

# Guidelines (IMPORTANT !) :
1. Focus only on skills that are listed as available skills.
3. Use exact same skill name. Do not change any letter or caps. Do not add formating characters.
5. Return only the skills and proficency level. Don't add any explanation or additional text (IMPORTANT)

Conversation:
{conversation}
"""

PERSONA_EXTEND_SKILL_DOMAIN_PROMPT = """
You are an expert in skill taxonomy and job candidate profile analysis.

From this persona information:
{persona_description}

Extract **skills domains** link to the candidate goal from following skill domains list:
{skills_domains}

# Guidelines (IMPORTANT !) :
1. You can only use skill domain from the provided list.
2. You can pick several skills, but be sure it is strongly link to candidate goals.
3. Use exact same skill name. Do not change any letter or caps. Do not add formating characters.
4. If no matching domain is found in the provided lists, return an empty list.
5. Return only the skills domains. Don't add any explanation or additional text (IMPORTANT)

Return result in, python list format like [skill_domain_A, skill_domain_B, ...]
"""

PERSONA_EXTRACTION_PROMPT = """Extract the following information from this conversation with a young person in Brazil seeking career opportunities or training. Return a structured profile with these fields:

- Name: The person's name
- Age: The person's age as a number.
- Location: The city where the person lives. (Do no not mention state or country). Just use standard city name.
- Recommendation type: YOU MUST CHOOSE ONE of these three options based on the conversation context - do not return null:
    1. 'jobs_trainings' if ANY of these are true:
       - Person is actively looking for jobs
       - Person mentions wanting to apply for positions
       - Person asks about job opportunities
    2. 'trainings_only' if ANY of these are true:
       - Person focuses mainly on learning or courses
       - Person lacks required qualifications for their target role
       - Person explicitly mentions needing training
       - Person is still studying or completing education
    3. 'awareness' if ANY of these are true:
       - Person is just exploring or curious about the field
       - Person is too young for professional training
       - Person's questions are very general or preliminary
       - Person shows no clear direction or specific goals
    Even with limited information, you must select the most appropriate category based on available context. Default to 'awareness' if truly uncertain. 'jobs_trainings' has priority other 'trainings_only' is interested for a job.
- Open to relocate for work: Whether they've mentioned being willing to move for work (LIMITED TO true or false)
- Work type preference: Their preferred work arrangement (LIMITED TO onsite, remote, or hybrid)
- Education level: Their highest completed education level (one of and LIMITED TO: Ensino Fundamental, Ensino Médio, Técnico, Tecnólogo, Graduação, Bacharelado, Licenciatura, Pós-graduação, Especialização, Mestrado, MBA, Doutorado)
- Years of experience: Their professional experience in years (as an integer)
- Skills domains: Skills domains they're interested in.
    - It shall be from **SKILLS DOMAINS LIST**
    - It shall use exact same names (Do not change any letter or caps)
    - If no match at all use UNKNOWN as single domain name
    - IMPORTANT : reference only the domains that directly match with the person goal
- Skills: Dictionary of skills with their proficiency levels (LIMITED TO Basic, Intermediate, or Advanced). Example: {{"Python": "Advanced", "Data analysis": "Intermediate"}}
    - Use strict formating for skill name: 
        - starting with Capital letter, the rest in lowercase letter
        - make sure skill name is in english. If not, translate
- Languages: Languages they speak
    - Use strict formating for language name:
        - use english term
        - starting with Capital letter, the rest in lowercase letter
        - no location attribute (like Brasilian), just one word
- Target domains: Professional domains/sectors they're interested in.
    - It shall be from **ACTIVITIES DOMAINS LIST**
    - It shall use exact same names (Do not change any letter or caps)
    - If no match at all use UNKNOWN as single domain name
- Goals: Their stated career or learning objectives. Make sure to capture all meaningful informations, but limit up to 20 words.

ACTIVITIES DOMAINS LIST:
{activities_domains}

SKILLS DOMAINS LIST:
{skills_domains}

For any information not explicitly mentioned:
- If they're just seeking information rather than specific jobs/training, capture this in goals
- If work type isn't mentioned, infer from their skills and interests
- If education level isn't specified, use "unknown" rather than guessing
- If skills don't have explicit levels mentioned, default to "Basic"

Be precise and only extract information that's actually present or can be reasonably inferred. Don't invent details.

Conversation:
{conversation}
"""

PERSONA_INITIAL_EXTRACTION_PROMPT_v1 = """From the interview conversation, extract the following fields and return a structured profile with these fields:
- Age: The person's age as a number.
- Location: The city where the person lives
- Recommendation type: YOU MUST CHOOSE ONE of these three options based on the conversation context - do not return null:
    1. 'jobs_trainings' if ANY of these are true:
       - Person is actively looking for jobs in Brasil
           - Person looking for abroad job shall not be classified as jobs_trainings
       - Person mentions wanting to apply for positions
       - Person asks about job opportunities
    2. 'trainings_only' if ANY of these are true:
       - Person focuses mainly on learning or courses
       - Person lacks required qualifications for their target role
       - Person explicitly mentions needing training
       - Person is still studying or completing education
    3. 'awareness' if ANY of these are true:
       - Person is just exploring or curious about the field
       - Person is too young for professional training
       - Person's questions are very general or preliminary
       - Person shows no clear direction or specific goals
    Even with limited information, you must select the most appropriate category based on available context. Default to 'awareness' if truly uncertain. 'jobs_trainings' has priority other 'trainings_only' is interested for a job.
- Open to relocate for work: Whether they've mentioned being willing to move for work (true/false)
- Work type preference: Their preferred work arrangement (onsite, remote, or hybrid)
- Education level: Their highest completed education level (one of: Ensino Fundamental, Ensino Médio, Técnico, Tecnólogo, Graduação, Bacharelado, Licenciatura, Pós-graduação, Especialização, Mestrado, MBA, Doutorado)
- Years of experience: Their professional experience in years (as an integer)
- Skills: Dictionary of skills with their proficiency levels (LIMITED TO Basic, Intermediate, or Advanced). Example: {{"Python": "Advanced", "Data analysis": "Intermediate"}}
    - Use strict formating for skill name: 
        - starting with Capital letter, the rest in lowercase letter
        - make sure skill name is in english. If not, translate
- Languages: Languages they speakBasic
    - Use strict formating for language name:
        - use english term
        - starting with Capital letter, the rest in lowercase letter
        - no location attribute (like Brasilian), just one word
- Target domains: Professional domains/sectors they're interested in.
    - It shall be from **ACTIVITIES DOMAINS LIST**
    - It shall use exact same names (Do not change any letter or caps)
    - If no match at all use UNKNOWN as single domain name
- Goals: Their stated career or learning objectives.
    - Make sure to capture all meaningful informations that will help understand acticity domain or skills domain in relatiob to candidate profile or goal.

Use default values for following information :
- Skills domains: empty list
- Activities domains : empty list
- Skills: empty list

For any information not explicitly mentioned:
- If they're just seeking information rather than specific jobs/training, capture this in goals
- If work type isn't mentioned, infer from their skills and interests
- If education level isn't specified, use "unknown" rather than guessing
- If skills don't have explicit levels mentioned, default to "Basic"

Be precise and only extract information that's actually present or can be reasonably inferred. Don't invent details.

Conversation:
{conversation}
"""

PERSONA_EXTRACTION_PROMPT_v1 = """Extract the following information from this conversation:
- Name
- Skills (as pairs of skill name and proficiency level)
- Location
- Age
- Years of experience
- Work type (one of: ['onsite', 'remote'])

If work type isn't explicitly mentioned, infer from their skills and interests.

Conversation:
"""

PERSONA_SKILL_DOMAINS_CLASSIFICATION_PROMPT_v1 = """
You are an expert in skill taxonomy, training analysis and candidate profile description analysis.

Your task is to evaluate whether the following candidate profile description matches any of the existing skill domains.

# Candidate profile:
{persona_description}

# Existing Skill Domains:
{formatted_domains}

Each domain is represented as `'Domain Name'`.

# Instructions:
1. Carefully read the candidate profile and compare it to the domain descriptions.
2. If the goal or skills list clearly fits within one or more domains, respond with formatted list:
   ['Domain Name A', 'Domain Name B', ...]
3. If the goal or skills lis **not** fit any existing domain, respond with empty list:
   []
4. Don't be too much conservative: if domains looks close, take it.
5. Do not modify or rename existing domains.
6. IMPORTANT : you are not authorized to create new skill domain.
    - you MUST use skill domains listed in 'Existing Skill Domains' list exclusively
    - NEVER report a skill domain present in candidate profile if it is not part of 'Existing Skill Domains' list
    - if you find no match return an empty list without reusing skill domain present in candidate profile

FINAL INSTRUCTION : Analyse user feedback about user motivation to take trainings. IMPORTANT : If user says he is not interested in trainings or show doubt to take any trainings at all, reply ['NOT_INTERESTED']

Respond with the list of domains you have selected.
"""