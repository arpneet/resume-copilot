from pydantic import BaseModel, Field
from typing import List, Optional


class Experience(BaseModel):
    role: str
    company: str
    dates: Optional[str] = None
    bullets: List[str] = Field(default_factory=list)


class Profile(BaseModel):
    name: Optional[str] = None
    skills: List[str] = Field(default_factory=list)
    tools: List[str] = Field(default_factory=list)
    education: List[str] = Field(default_factory=list)
    certifications: List[str] = Field(default_factory=list)
    experiences: List[Experience] = Field(default_factory=list)


class JobRequirements(BaseModel):
    title: Optional[str] = None
    must_have: List[str] = Field(default_factory=list)
    nice_to_have: List[str] = Field(default_factory=list)
    years_experience: Optional[str] = None
    responsibilities: List[str] = Field(default_factory=list)