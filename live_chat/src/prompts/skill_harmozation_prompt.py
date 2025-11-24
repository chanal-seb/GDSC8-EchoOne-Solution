SKILL_HARMONIZATION_PROMPT = """
You are given a list of training programs in the are of {skill_domain_name}, each with a title, a set of keywords, and a skill name.

Your task is to harmonize the skill names by following these rules:
- Group trainings that teach the same specific skill (e.g., Financial Cost Analysis, Financial Reporting, Audit) under a single, consistent, and precise skill name, regardless of the level (e.g., Basic, Intermediate, Advanced).
- Do not rely solely on the original skill name. Instead, analyze the title and keywords to understand the actual skill being taught.
- Avoid vague or overly broad skill names like “Financial Skill” or “Advanced Skill.” Use clear, descriptive names that reflect the core skill (e.g., “Cost Analysis” instead of “Financial Skill”).
- Normalize variations in naming (e.g., “Corporate Financial Reporting” and “Financial Reporting” → “Financial Reporting”).
- Read between the lines: if two trainings clearly refer to the same skill but use different terms, harmonize them under one name.

Input Format:
Each training entry is structured as:
--- training <code> ---
- List with format Title / Short description
<Title> / <Short description>

Output Formtat:
List of harmonized skill names

List of trainings:
{trainings}
"""

SKILL_HARMONIZATION_PROMPT_v1 = """
You are given a list of training programs in the are of {skill_domain_name}, each with a title, a set of keywords, and a skill name.

Your task is to harmonize the skill names by following these rules:
- Group trainings that teach the same specific skill (e.g., Financial Cost Analysis, Financial Reporting, Audit) under a single, consistent, and precise skill name, regardless of the level (e.g., Basic, Intermediate, Advanced).
- Do not rely solely on the original skill name. Instead, analyze the title and keywords to understand the actual skill being taught.
- Avoid vague or overly broad skill names like “Financial Skill” or “Advanced Skill.” Use clear, descriptive names that reflect the core skill (e.g., “Cost Analysis” instead of “Financial Skill”).
- Normalize variations in naming (e.g., “Corporate Financial Reporting” and “Financial Reporting” → “Financial Reporting”).
- Read between the lines: if two trainings clearly refer to the same skill but use different terms, harmonize them under one name.

Input Format:
Each training entry is structured as:
--- training <code> ---
- List with format Title / Keywords / Skills Acquired
<Title> / <Keywords> / <Skill>

Output Formtat:
List of harmonized skill names

List of trainings:
{trainings}
"""