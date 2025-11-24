from typing import List
from pydantic import BaseModel, Field


class InterviewInfo(BaseModel):
    conversation_id: str = Field(default="", description="conversation_id")
    interview: List[str] = Field(
        default_factory=list,
        description="List messages"
    )

    def get_structured_interview(self) -> str:
        return "\n".join(self.interview)


# class InterviewInfo(BaseModel):
#     interview: List[str]
# 
#     def get_structured_interview(self) -> str:
#         return "\n".join(self.interview)


class InverviewQualityInfo(BaseModel):
    quality_level: str = Field(default="", description="Quality level of the interview (OK/NOK)")
    rationale: str = Field(default="", description="Short justification of quality level decision")


class InterviewAgentMessage(BaseModel):
    conversation_finished: bool = Field(default=True, description="Indicate if agent decide to close interview")
    message: str = Field(default="", description="Next message to send to user if conversation is not finished")
    