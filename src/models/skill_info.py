from typing import Dict, List
from pydantic import BaseModel, Field


class SkillHarmonizationMap(BaseModel):
    harmonized_skills: Dict[str, str] = Field(
        default_factory=dict,
        description="Dictionary mapping training id to harmonized skill name"
    )


class SkillLabelingReply(BaseModel):
    skill_label: str = Field(default="", description="Skill label")
    rationale: str = Field(default="", description="Justification of the decision")


class SkillDomainLabelingReply(BaseModel):
    skill_domain_label: str = Field(default="", description="Skill domain label")
    rationale: str = Field(default="", description="Justification of the decision")
