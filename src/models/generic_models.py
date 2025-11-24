from pydantic import BaseModel, Field
from typing import List


class BooleanModel(BaseModel):
    istrue: bool = Field(default=False, description="value")


class BooleanModelWithRationale(BaseModel):
    istrue: bool = Field(default=False, description="value")
    rationale: str = Field(default="", description="retionale explanation")


class ListOfIds(BaseModel):
    list_of_ids: List[str] = Field(
        default_factory=list,
        description="List of IDs"
    )
    rationale: str = Field(default="", description="retionale explanation")


class ListOfStrs(BaseModel):
    list_of_strs: List[str] = Field(
        default_factory=list,
        description="List of strings"
    )
    rationale: str = Field(default="", description="retionale explanation")
