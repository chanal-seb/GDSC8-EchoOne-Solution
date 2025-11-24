SKILL_LABELING_PROMPT = """
You are an expert in skill taxonomy, training analysis and job description analysis.

From this trainings information:
{trainings_description}

Find the a skill name that categorizes precisely the traingings group listed above.
It shall be enough generic to fit with all trainings of the group but also enough specific to capture the specificity of the group.

Format the skill label using **Title Case** (capitalize the first letter of each word, the rest lowercase).

Return your reply with following fields:
- The skill name
- The justification of your decision
"""

SKILL_DOMAIN_LABELING_PROMPT = """
You are an expert in skill taxonomy, training analysis and job description analysis.

From this trainings information:
{trainings_description}

Find the a skill domain name that categorizes precisely the traingings group listed above.
It shall be enough generic to fit with all trainings of the group but also enough specific to capture the specificity of the group.

Format the skill label using **Title Case** (capitalize the first letter of each word, the rest lowercase).

In case you detect outliers, make it not influence the skill domain name and write it in the justification field.

Return your reply with following fields:
- The skill domain name
- The justification of your decision
"""

TRAINING_EXTRACTION_PROMPT = """
Extract detailed information from training description. Return a structured training information with these fields:
- Title: The job title
- Skill description : A short description describing the **skill taught**.
    - have in mind the field Skill description will be used later for training classification : skill name and skill category
    - your task is not to anticipite identification of those classified labels but ease it later by extracting the needed information to support this.
- The **skill taught** (as a short, clear label) : a first proposition of the skill name acquired be the trainee.
- Level acquired : The **level** of the skill, chosen **exclusively** from this list: Basic, Intermediate, Advanced, UNKNOWN

Guidelines:
1. Do **not** include the level in the skill label itself.
2. Format the skill label using **Title Case** (capitalize the first letter of each word, the rest lowercase).

#TRAINING DESCRIPTION:
"""

EXTENDED_TRAINING_EXTRACTION_PROMPT_OPENTEXT = """
Analyze the following training description and classify its Subject Area according to the OpenText Taxonomy.
Return your answer in the following format:
[Subject Area][Subcategory]

Training Description:
{training_description}
"""

EXTENDED_TRAINING_EXTRACTION_PROMPT = """
You are an expert in skill taxonomy, training analysis and job description analysis.

From this training information:
{training_description}

Extract the **skill domain** as much as possible coming from the following skill domains list:
{skills_domains}

# Guidelines (IMPORTANT !) :
1. You can only use skill domain from the provided list.
2. You can pick only one skill
3. If several domains match, choose the one that best match the What of the training rather thatn the Where
    - For exemple if a training teaches "Basic Money Management for Hotel Reception", it shall be classified in "Accounting and Finance" (the What) category rather than "Hospitality Management" (the Where)
3. Use the exact same skill name. Do not change any letter or caps. Do not add formating characters.
4. If no matching domain is found in the provided lists, use **UNKNOWN** as the domain name.
5. Return only the skill domain or UNKNOWN. Don't add any explanation or additional text (IMPORTANT)
"""

EXTENDED_TRAINING_EXTRACTION_PROMPT_v2 = """
You are an expert in skill taxonomy, training analysis and job description analysis.

From this training information:
{training_description}

Extract the **skill domain** as much as possible coming from the following skill domains list:
{skills_domains}

# Guidelines (IMPORTANT !) :
1. You can only use skill domain from the provided list.
2. You can pick only one skill
3. Use the exact same skill name. Do not change any letter or caps. Do not add formating characters.
4. If no matching domain is found in the provided lists, use **UNKNOWN** as the domain name.
5. Do not select a domain if not precise enough (for exemple, food waste trainings shall not end in Environmental Management)
5. Return only the skill domain or UNKNOWN. Don't add any explanation or additional text (IMPORTANT)
"""


EXTENDED_TRAINING_EXTRACTION_PROMPT_v1 = """
You are an expert in skill taxonomy, training analysis and job description analysis.

From this training skills information:
{training_description}

Extract the **skill domain** as much as possible coming from the following skill domains list:
{skills_domains}

# Guidelines (IMPORTANT !) :
1. You can only use skill domain from the provided list.
2. You can pick only one skill
3. Use the exact same skill name. Do not change any letter or caps. Do not add formating characters.
4. If no matching domain is found in the provided lists, use **UNKNOWN** as the domain name.
5. Do not select a domain if not precise enough (for exemple, food waste trainings shall not end in Environmental Management)
5. Return only the skill domain or UNKNOWN. Don't add any explanation or additional text (IMPORTANT)
"""

FULL_TRAINING_EXTRACTION_PROMPT = """
Extract from the following training description:

1. The **skill taught** (as a short, clear label)
2. The **level** of the skill, chosen **exclusively** from this list: Basic, Intermediate, Advanced, Unknown
3. The **skill domain** as much as possible coming from the following skill domains list:
    - if no skill domain is matching, use **UNKNOWN**
4. The **activity domain** as much as possible coming from the following activity domains list:
    - if no activity domain is matching, use **UNKNOWN**

# Guidelines:
1. Do **not** include the level in the skill label itself.
2. Format the skill label using **Title Case** (capitalize the first letter of each word, the rest lowercase).
3. IMPORTANT ! When using a skill domain or activity domain from the provided lists, use the exact same domain name (Do not change any letter or caps).
4. If no matching domain is found in the provided lists, use **UNKNOWN** as the domain name.
5. IMPORTANT ! Always use existing skill domain or activity domain from the provided lists when possible.

# Skill domains:
{skills_domains}

# Activity domains:
{activities_domains}

# Training description:
{training_description}
"""

TRAINING_EXTRACTION_PROMPT_v2 = """
Extract detailed information from training description. Return a structured training information with these fields:
- Title: The job title
- Description keywords: a short summary to provide additional context.
- Skill acquired : The **skill taught** (as a short, clear label)
- Level acquired : The **level** of the skill, chosen **exclusively** from this list: Basic, Intermediate, Advanced, UNKNOWN

Guidelines:
1. Do **not** include the level in the skill label itself.
2. Format the skill label using **Title Case** (capitalize the first letter of each word, the rest lowercase).

#TRAINING DESCRIPTION:
"""


TRAINING_EXTRACTION_PROMPT_v1 = """
Extract from the following training description:

- The **skill taught** (as a short, clear label)
- The **level** of the skill, chosen **exclusively** from this list: Basic, Intermediate, Advanced, Unknown

Guidelines:
1. Do **not** include the level in the skill label itself.
2. Format the skill label using **Title Case** (capitalize the first letter of each word, the rest lowercase).
3. Avoid redundancy: merge similar concepts into a single skill label when appropriate.
4. Focus on the **core skill** being taught, not peripheral topics or tools unless they are central to the training.

Training description:
"""
