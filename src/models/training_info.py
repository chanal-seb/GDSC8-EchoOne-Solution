from pydantic import BaseModel, Field
from typing import Tuple, List


class TrainingInfo(BaseModel):
    """
    Structured training information
    """
    title: str = Field(default="", description="Training title")
    skill_description: str = Field(default="", description="Short description of the acquired skill")
    skill_acquired: str = Field(default="", description="Skill acquired")
    level_acquired: str = Field(default="", description="Level acquired(Basic, Intermediate, or Advanced)")
    skill_domain: str = Field(default="", description="The skill domain that best fits the training")

    def describe(self) -> str:
        """Enhanced description that includes all relevant training information"""

        description = [
            f"Title: {self.title}",
            f"Skill Description: {self.skill_description}",
            f"Skill Acquired: {self.skill_acquired}",
            f"Level Acquired: {self.level_acquired}",
            f"Skill Domains: {self.skill_domain}"
        ]

        return "\n".join(description)

    def describe_short(self) -> str:
        """Short description that includes minimal training information"""

        description = [
            f"Title: {self.title}",
            f"Skill Description: {self.skill_description}",
        ]

        return "\n".join(description)

    def summarize(self) -> str:
        summary = 'Format: Title / Skill Description / Skills Acquired\n'
        summary += f"{self.title} / {self.skill_description} / {self.skill_acquired}"

        return summary

    def summarize_for_matching(self, id='') -> str:
        description = [
            f"### Training Id: {id}",
            f"Skill Acquired: {self.skill_acquired}",
            f"Level Acquired: {self.level_acquired}"
        ]

        return "\n".join(description)

    def summarize_for_skill_acquired_labeling(self, id='') -> str:
        description = [
            f"### Training Id: {id}",
            f"Skill Description: {self.skill_description}"
        ]

        return "\n".join(description)

    def get_skill_acquired(self, id='') -> str:
        description = f"- Training Id: {id} - {self.skill_acquired} - {self.level_acquired}"

        return description
