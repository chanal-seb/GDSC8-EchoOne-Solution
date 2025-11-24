from pydantic import BaseModel, Field
from typing import List, Set, Optional, Dict
    
class InitialPersonaInfo(BaseModel):
    name: str = Field(default="", description="Persona's name")
    education_level: str = Field(default="", description="Highest education level completed")
    age: int = Field(default=25, description="Persona's age")
    location: str = Field(default="", description="Persona's city location")
    interested_by_job: bool = Field(default=False, description="Whether the persona is interested to find a job")
    interested_by_training: bool = Field(default=False, description="Whether the persona is interested to find a training")
    goals: str = Field(
        default="",
        description="Career or learning goals of the persona"
    )
    rationale: str = Field(default="", description="Justification of the decision")

class JobPersonaInfo(BaseModel):
    open_to_relocate_for_work: bool = Field(default=False, description="Whether the persona is open to relocate for work")
    work_type_preference: str = Field(
        default="",
        description="Preferred work type - 'onsite', 'remote', or 'hybrid'"
    )
    target_domains: List[str] = Field(
        default_factory=list,
        description="Professional domains/sectors the persona is interested in"
    )
    education_level: str = Field(default="", description="Highest education level completed")
    years_of_experience: int = Field(default=0, description="Years of professional experience")
    languages: List[str] = Field(
        default_factory=list,
        description="Languages the persona speaks"
    )
    goals: str = Field(
        default="",
        description="Career or learning goals of the persona"
    )

class PersonaInfo(BaseModel):
    """
    Enhanced structured profile of a job seeker with category preference
    """
    name: str = Field(default="", description="Persona's name")
    age: int = Field(default=25, description="Persona's age")
    location: str = Field(default="", description="Persona's city location")
    recommendation_type: Optional[str] = Field(
        default=None,
        description="Type of recommendation needed: 'jobs_trainings', 'trainings_only', or 'awareness'"
    )
    open_to_relocate_for_work: bool = Field(default=False, description="Whether the persona is open to relocate for work")
    work_type_preference: str = Field(
        default="",
        description="Preferred work type - 'onsite', 'remote', or 'hybrid'"
    )
    target_domains: List[str] = Field(
        default_factory=list,
        description="Professional domains/sectors the persona is interested in"
    )
    education_level: str = Field(default="", description="Highest education level completed")
    years_of_experience: int = Field(default=0, description="Years of professional experience")
    skills_domains: List[str] = Field(
        default_factory=list,
        description="Dictionary listing skills domains attached to person training plan"
    ) 
    skills: Dict[str, str] = Field(
        default_factory=dict,
        description="Dictionary mapping skills to proficiency levels (Basic, Intermediate, Advanced)"
    )
    languages: List[str] = Field(
        default_factory=list,
        description="Languages the persona speaks"
    )
    goals: str = Field(
        default="",
        description="Career or learning goals of the persona"
    )
    hard_filtered_jobs_ids: List[str] = Field(
        default_factory=list,
        description="List of job proposed to persona"
    ) 
    proposed_job_ids: List[str] = Field(
        default_factory=list,
        description="List of job proposed to persona"
    ) 

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
        normalized_level = self.education_level.lower()

        # Return the corresponding value or -1 if not found
        return education_hierarchy.get(normalized_level, -1)

    def get_skills_and_goal(self) -> str:
        skills_str = ', '.join([f'{skill}: {level}' for skill, level in self.skills.items()])
        description = [
            f"Skills: {skills_str}",
            f"Goals: {self.goals}"
        ]
        return "\n".join(description)

    def get_skills_str(self) -> str:
        skills_str = ''
        for skill, level in self.skills.items():
            skills_str += f"- {skill} : {level}" + "\n"

        return skills_str

    def describe(self) -> str:
        """Enhanced description that includes all relevant information for matching"""
        # Update this line to iterate through dictionary items instead of list items
        skills_str = ', '.join([f'{skill}: {level}' for skill, level in self.skills.items()])
        languages_str = ', '.join(self.languages)
        domains_str = ', '.join(self.target_domains)
        skills_domains_str = ', '.join(self.skills_domains)

        description = [
            f"Name: {self.name}",
            f"Age: {self.age}",
            f"Location: {self.location}",
            f"Recommendation type: {self.recommendation_type}",
            f"Open to relocate for work: {'Yes' if self.open_to_relocate_for_work else 'No'}",
            f"Work type preference: {self.work_type_preference}",
            f"Education level: {self.education_level}",
            f"Years of experience: {self.years_of_experience}",
            f"Skills Domains: {skills_domains_str}",
            f"Skills: {skills_str}",
            f"Languages: {languages_str}",
            f"Target domains: {domains_str}",
            f"Goals: {self.goals}"
        ]
    
        return "\n".join(description)

    def summarize_for_skill_domain_matching(self) -> str:
        domains_str = ', '.join(self.target_domains)

        description = [
            f"Target domains: {domains_str}",
            f"Goals: {self.goals}",
            f"Skills: {skills_str}"
        ]
    
        return "\n".join(description)

class PersonaSkills(BaseModel):
    skills: Dict[str, str] = Field(
        default_factory=dict,
        description="Dictionary mapping skills to proficiency levels (Basic, Intermediate, Advanced)"
    )
    interested_by_training: bool = Field(default=False, description="Whether the persona is interested to find a training")
    rationale: str = Field(default="", description="Justification of the decision")

class LoacationNameRefator(BaseModel):
    renaming_needed: bool = Field(default=False, description="Indicate if location rename is needed")    
    name: str = Field(default="", description="New location name")
    rationale: str = Field(default="", description="Justification of the decision")

class RecommendationAnalysis(BaseModel):
    interested_by_job: bool = Field(default=False, description="Whether the persona is interested to find a job")
    interested_by_job_in_different_domain: bool = Field(default=False, description="Whether the persona is interested to find a job in a different domain")
    interested_by_training: bool = Field(default=False, description="Whether the persona is interested to find a training")
    rationale: str = Field(default="", description="Justification of the decision")

class PersonaSkillsInterest(BaseModel):
    list_of_skills: List[str] = Field(
        default_factory=list,
        description="List of skills"
    )
    interested_by_training: bool = Field(default=False, description="Whether the persona is interested to find a training")
    rationale: str = Field(default="", description="Justification of the decision")
