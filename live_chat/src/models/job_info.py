import json
from pydantic import BaseModel, Field
from typing import List, Set, Dict, Optional


class JobInfo(BaseModel):
    """
    Structured job information for green jobs matching with work type distinction
    """
    title: str = Field(default="", description="Job title")
    domains: List[str] = Field(
        default_factory=list,
        description="Professional domains/sectors of the job"
    )
    location: str = Field(default="", description="City where the job is located")
    work_type: str = Field(
        default="", 
        description="Work arrangement: 'onsite', 'remote', or 'hybrid'"
    )
    education_level_required: str = Field(
        default="", 
        description="Minimum education level required (one of: Ensino Fundamental, Ensino Médio, Técnico, Tecnólogo, Graduação, Bacharelado, Licenciatura, Pós-graduação, Especialização, Mestrado, MBA, Doutorado)"
    )
    years_of_experience_required: int = Field(default=-1, description="Minimum years of experience required")
    required_skills: Dict[str, str] = Field(
        default_factory=dict,
        description="Dictionary mapping skills to required proficiency levels (Basic, Intermediate, or Advanced)"
    )
    required_skills_domains: List[str] = Field(
        default_factory=dict,
        description="Dictionary listing domains attached to skills to required skills"
    )
    required_languages: List[str] = Field(
        default_factory=set,
        description="Languages required for the job"
    )
    job_description: str = Field(default="", description="Short summary of the job")

    @property
    def is_remote(self) -> bool:
        """Helper property to check if job is remote or hybrid (for location matching)"""
        return self.work_type.lower() in ["remote", "hybrid"]


    def get_info_for_matching(self, id) -> str:
        description = [
            f"Job with ID: {id}",
            f"- Title: {self.title}",
            f"- Description: {self.job_description}"
        ]

        return "\n".join(description)


    def get_education_level_value(self) -> int:
        """
        Returns a numeric value corresponding to the education level.
        Higher values represent higher education levels.
        Returns -1 if the education level is not recognized.
        """
        education_hierarchy = {
            "ensino fundamental": 1,
            "ensino médio": 2,
            "técnico": 3,
            "tecnólogo": 4,
            "graduação": 5,
            "bacharelado": 6,
            "licenciatura": 7,
            "pós-graduação": 8,
            "especialização": 9,
            "mestrado": 10,
            "mba": 11,
            "doutorado": 12
        }

        # Normalize the education level (lowercase and remove accents)
        normalized_level = self.education_level_required.lower()

        # Return the corresponding value or -1 if not found
        return education_hierarchy.get(normalized_level, -1)

    def get_required_skills(self) -> str:
        skills_str = '\n'.join([f"- {skill}: {level}" for skill, level in self.required_skills.items()])
        return skills_str

    def summarize(self) -> str:
        skills_str = ', '.join([f"{skill}: {level}" for skill, level in self.required_skills.items()])

        summary = 'Format : Title / Skills Requested \n'
        summary += f"{self.title} / {skills_str}"

        return summary

    def describe(self) -> str:
        """Enhanced description that includes all relevant job information"""
        skills_str = ', '.join([f"{skill}: {level}" for skill, level in self.required_skills.items()])
        languages_str = ', '.join(self.required_languages)
        required_skills_domains_str = ', '.join(self.required_skills_domains)
        activity_domains_str = ', '.join(self.domains)

        description = [
            f"Title: {self.title}",
            f"Domains: {activity_domains_str}",
            f"Location: {self.location}",
            f"Work type: {self.work_type}",
            f"Education: {self.education_level_required}",
            f"Experience: {self.years_of_experience_required} years",
            f"Required skills domains: {required_skills_domains_str}",
            f"Required skills: {skills_str}",
            f"Required languages: {languages_str}"
        ]

        return "\n".join(description)

    def describe_for_interview(self) -> str:
        """Enhanced description that includes all relevant job information"""
        languages_str = ', '.join(self.required_languages)
        activity_domains_str = ', '.join(self.domains)

        description = [
            f"Title: {self.title}",
            f"Description: {self.job_description}",
            f"Domains: {activity_domains_str}",
            f"Location: {self.location}",
            f"Work type: {self.work_type}",
            f"Education: {self.education_level_required}",
            f"Experience: {self.years_of_experience_required} years",
            f"Required languages: {languages_str}"
        ]

        return "\n".join(description)
        
    def to_json_string(self) -> str:
        """
        Serialize the JobInfo object to a JSON string with proper formatting
        for storage in a JSON file.
        """
        # Create a dictionary with all the fields we want to include
        job_dict = {
            "title": self.title,
            "domains": self.domains,
            "location": self.location,
            "work_type": self.work_type,
            "education_level_required": self.education_level_required,
            "years_of_experience_required": self.years_of_experience_required,
            "required_skills": self.required_skills,
            "required_skills_domains": list(self.required_skills_domains),
            "required_languages": list(self.required_languages)
        }

        # Convert to JSON string without escaping non-ASCII characters
        return json.dumps(job_dict, ensure_ascii=False)

    @classmethod
    def serialize_job_table(cls, table: Dict[str, 'JobInfo']) -> Dict[str, str]:
        """
        Class method to serialize an entire table of JobInfo objects
        """
        return {job_id: job_info.to_json_string() for job_id, job_info in table.items()}


class JobInforequired_skills_domains(BaseModel):
    required_skills_domains: List[str] = Field(
        default_factory=list,
        description="Dictionary listing domains attached to skills to required skills"
    )
    rationale: str = Field(default="", description="Justification of the decision")

class JobInfoRequiredSkills(BaseModel):
    required_skills: Dict[str, str] = Field(
        default_factory=dict,
        description="Dictionary mapping skills to required proficiency levels (Basic, Intermediate, or Advanced)"
    )
    rationale: str = Field(default="", description="Justification of the decision")
