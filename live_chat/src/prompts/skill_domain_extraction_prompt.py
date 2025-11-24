SKILL_DOMAIN_EXTRACTION_PROMPT = """
You are an expert in skill taxonomy, training analysis and job description analysis.

Your task is to analyze the following list of individual skills and construct a clean, structured list of skill domains.

Each domain should group related skills under a clear and general name, with a concise description that summarizes the scope of the domain.

# Input: List of skills
{skills}

# Instructions:
1. Group related skills into **generalized domains**. Avoid overly specific or fragmented domains.
2. Each domain should:
   - Have a **clear and concise name**.
   - Include a **short description** summarizing the types of skills it covers.
3. Do **not** create separate domains for different proficiency levels (e.g., beginner vs. intermediate). Instead, generalize the domain to cover the full scope.
4. Avoid redundancy: if multiple skills overlap, merge them into a single domain.
5. Aim to produce **around 20 to 30 domains**. This is not a strict limit, but a guideline to encourage clarity and manageability.
6. Return the result
"""

JOB_SKILL_DOMAINS_CLASSIFICATION_PROMPT = """
You are an expert in skill taxonomy, training analysis, and job description interpretation.

Your task is to identify which skill domains—among a predefined list—cover the skills required for the job described below.

# Job Description:
{job_description}

# Existing Skill Domains:
{formatted_domains}

Each domain is represented as a string: 'Domain Name'.

# Instructions:
1. Carefully read the job description and compare it to the list of existing domains.
2. If the job clearly mentions skills that align with one or more domains, respond with a list in the following format:
   ['Domain Name A', 'Domain Name B', ...]
3. If none of the domains match the job description, respond with an empty list:
   []
4. Be inclusive rather than overly conservative: if a domain appears reasonably close to the described skills, include it.
5. Do NOT modify, rename, or create new domains.
6. IMPORTANT:
   - You MUST use only the domains listed in 'Existing Skill Domains'.
   - NEVER infer or reuse domain names from the job description if they are not in the provided list.
   - If no match is found, return an empty list.

Respond with foowing fields :
- required_skills_domains : the final list of selected domains.
- rationale: Justification of the decision
"""

DOMAIN_MATCHING_PROMPT = """
You are an expert in skill taxonomy, training analysis and job description analysis.

Your task is to evaluate whether the following training description matches any of the existing skill domains.

# Training Description:
{training_description}

# Existing Skill Domains:
{formatted_domains}

Each domain is represented as `'Domain Name': 'Short description'`.

# Instructions:
1. Carefully read the training description and compare it to the domain descriptions.
2. If the training clearly fits within one or more domains, respond with:
   **OK** (`Domain Name A`, `Domain Name B`, ...)
3. If the training does **not** fit any existing domain, respond with:
   **NOK** (`Missing domain(s)`), and briefly suggest what domain(s) might be missing.
4. Be conservative: only match a domain if the training clearly falls within its scope.
5. Do not modify or rename existing domains.

Respond with only one line in the format:
**OK** (`...`) or **NOK** (`...`)
"""

SKILL_DOMAIN_EXTENSION_PROMPT = """
You are an expert in skill taxonomy, training analysis and job description analysis.

Your task is to analyze the following list of individual skills and construct a clean, structured list of skill domains.

Each domain should group related skills under a clear and general name, with a concise description that summarizes the scope of the domain.

# Input: List of Skills
{skills}

# Existing domains
{skill_domains}

# Instructions:
1. Group related skills into **generalized domains**. Avoid overly specific or fragmented domains.
2. Each domain should:
   - Have a **clear and concise name**.
   - Include a **short description** summarizing the types of skills it covers.
3. Do **not** create separate domains for different proficiency levels (e.g., beginner vs. intermediate). Instead, generalize the domain to cover the full scope.
4. Avoid redundancy: if multiple skills overlap, merge them into a single domain.
5. Inspire from existing domains for granularity level.
6. Return the added domains list

# IMPORTANT
- do not create new domains if one in existing domains exists already
"""

MATCH_SKILL_TO_DOMAIN_PROMPT = """
You are an expert in skill taxonomy, training analysis and job description analysis.

Your task it to match skill described below to a domain listed below.

# SKILL
{skill}

# DOMAINS LIST
{domains}

# Instructions:
1. Choose the nearest domain for the list
2. This is important that you make your possible to pick one domain.
3. If you are really block, use UNKNOWN
4. Return the domain you think is the best. Return only the domain, no additional text

# IMPORTANT
- use only domains present in the DOMAIN LIST section or UNKNWON.
"""

SKILL_DOMAIN_EXTRACTION_PROMPT_v1 = """

You are an expert in skill taxonomy and training analysis.

Your task is to analyze the following training description and update the current list of skill domains accordingly.

# Training Description:
{training_description}

# Current Skill Domains:
{current_domains}

Each domain is represented as a dictionary entry: `'domain_name': 'short description'`.

# Instructions:
1. Identify the skill domains covered by the training.
2. For each domain:
   - If the training clearly fits within an **existing domain**, do **not** modify the domain name or description unless the training introduces **new scope** that is **not already covered**.
   - If the training introduces a **new skill domain** that is not covered by any existing domain, create a **new domain** with a concise and clear name and description.
   - If the training partially overlaps with an existing domain but introduces **significant new scope**, you may **generalize** the domain. Only do this if the new scope cannot be reasonably included without a change.
3. Be conservative with updates: **do not rename or reword domains unless strictly necessary**.
4. Return the **updated list of domains**


# Tips:
- Prefer **general domains** that can cover multiple levels of expertise (e.g., beginner, intermediate, advanced).
- Do **not** create separate domains for different proficiency levels unless the scope is fundamentally different (e.g., tax law vs. accounting software).
- If multiple trainings target similar tools or workflows, group them under a single domain with a description that reflects the full scope.

# Important: Do not remove any existing domain from 'Current Skill Domains' list unless:
- It is clearly redundant with another domain that covers the same or broader scope.
- It is being merged into a more general domain that now includes its scope.
- If merging occurs, ensure the new domain name and description reflect the full scope of both domains.

Otherwise, retain all existing domains.
"""
