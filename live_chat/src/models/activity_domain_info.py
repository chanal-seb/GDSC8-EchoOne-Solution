from typing import Dict, List
from pydantic import BaseModel, Field


class ActivityDomainInfo(BaseModel):
    domains: Dict[str, str]  # domain name -> short description

    def describe(self) -> str:
        return "\n".join([f"- {name}: {desc}" for name, desc in self.domains.items()])

    def get_names_bullet_list(self) -> str:
        return "\n".join([f"- {name}" for name, desc in self.domains.items()])



class ListOfActivityDomains(BaseModel):
    domains: List[str] = Field(
        default_factory=list,
        description="List of Domains"
    )


class ActivityDomainLabelingReply(BaseModel):
    activity_domain_label: str = Field(default="", description="Activity domain label")
    description: str = Field(default="", description="Short description of the domain")
    rationale: str = Field(default="", description="Justification or comments")