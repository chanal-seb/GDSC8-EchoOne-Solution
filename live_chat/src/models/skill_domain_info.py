from typing import Dict, List
from pydantic import BaseModel, Field


class SkillDomainInfo(BaseModel):
    domains: Dict[str, str]  # domain name -> short description

    def describe(self) -> str:
        return "\n".join([f"- {name}: {desc}" for name, desc in self.domains.items()])

    def get_names_bullet_list(self) -> str:
        return "\n".join([f"- {name}" for name, desc in self.domains.items()])


class ListSkillsDomains(BaseModel):
    required_skills_domains: List[str] = Field(
        default_factory=list,
        description="Dictionary listing domains attached to skills to required skills"
    )