ACTIVITY_DOMAIN_EXTRACTION_PROMPT = """
You are an expert in skill taxonomy and job description analysis.

Your task is to analyze the following list of jobs data and construct a clean, structured list of activity domains.

Each domain should group related skills under a clear and general name, with a concise description that summarizes the scope of the domain.

# Input: List of jobs data
{jobs_data}

# Instructions:
1. Group related skills into **generalized domains**. Avoid overly specific or fragmented domains.
2. Each domain should:
   - Have a **clear and concise name**.
   - Include a **short description** summarizing the types of skills it covers.
   - These could be for exemple : technology, healthcare, administration, trades, arts, renewable energy, sustainable agriculture, environmental consulting, green construction, waste management, agriculture, ...
3. Avoid redundancy: if multiple skills overlap, merge them into a single domain.
4. Aim to produce **around 10 to 20 domains**. This is not a strict limit, but a guideline to encourage clarity and manageability.
5. Return the result
"""

ACTIVITY_MATCHING_PROMPT = """
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

ACTIVITY_DOMAIN_EXTENSION_PROMPT = """
You are an expert in job taxonomy and activity domain classification.

Your task is to analyze the following list of job titles and construct a clean, structured list of **activity domains**.

Each domain should group related jobs under a **sector-level or industry-level name**, with a concise description that summarizes the scope of the domain.

# Input: List of Jobs
{jobs_data}

# Existing domains
{activities_domains}

# Instructions:
1. Group related jobs into **generalized activity domains**, representing **industries or sectors** (e.g., technology, healthcare, administration, trades, arts, renewable energy, agriculture, environmental consulting, green construction, waste management).
2. Each domain must:
   - Have a **clear and concise name** (e.g., "Healthcare", not "Medical Skills").
   - Include a **short description** summarizing the types of activities it covers.
3. Avoid creating domains based on **skills, competencies, or soft skills** (e.g., "Organizational Skills", "Interpersonal Skills" are NOT valid domains).
4. Avoid redundancy: if multiple activities overlap, merge them into a single domain.
5. Use the existing domains as reference for granularity and naming style.
6. Return only the **new domains** that are missing from the existing list.

# IMPORTANT
- Do NOT create new domains if one in the existing list already covers the jobs.
- Focus on **sectoral grouping**, not functional or behavioral traits.
"""

ACTIVITY_DOMAIN_EXTENSION_PROMPT_v1 = """
You are an expert in jobs activity domain taxonomy and job description analysis.

Your task is to analyze the following list of jobs information and construct a clean, structured list of activity domains.

Each domain should group related jobs under a clear and general name, with a concise description that summarizes the scope of the domain.
These could be for exemple : technology, healthcare, administration, trades, arts, renewable energy, sustainable agriculture, environmental consulting, green construction, waste management, agriculture, ...

# Input: List of Jobs
{jobs_data}

# Existing domains
{activities_domains}

# Instructions:
1. Group related jobs into **generalized domains**. Avoid overly specific or fragmented domains.
2. Each domain should:
   - Have a **clear and concise name**.
   - Include a **short description** summarizing the types of activities it covers.
4. Avoid redundancy: if multiple activities overlap, merge them into a single domain.
5. Inspire from existing domains for granularity level.
6. Return the added domains list

# IMPORTANT
- do not create new domains if one in existing domains exists already
"""