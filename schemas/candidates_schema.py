from typing import Optional, Literal

from pydantic import BaseModel, EmailStr


class CandidateRegisterRequestSchema(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    career_level: Literal["Junior", "Senior", "Mid Level"]
    job_major: str
    years_of_experience: int
    degree_type: Literal["Bachelor", "Master", "High School"]
    skills: list
    nationality: str
    city: str
    salary: float
    gender: Literal["Male", "Female", "Not Specified"]


class CandidateRegisterResponseSchema(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    uuid: str
    career_level: Literal["Junior", "Senior", "Mid Level"]
    job_major: str
    years_of_experience: int
    degree_type: Literal["Bachelor", "Master", "High School"]
    skills: list
    nationality: str
    city: str
    salary: float
    gender: Literal["Male", "Female", "Not Specified"]


class UpdateCandidateRequestSchema(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    career_level: Optional[Literal["Junior", "Senior", "Mid Level"]] = None
    job_major: Optional[str] = None
    years_of_experience: Optional[int] = None
    degree_type: Literal["Bachelor", "Master", "High School"] = None
    skills: Optional[list] = None
    nationality: Optional[str] = None
    city: Optional[str] = None
    salary: Optional[float] = None
    gender: Optional[Literal["Male", "Female", "Not Specified"]] = None


class SearchParametersSchema(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    uuid: Optional[str] = None
    career_level: Optional[Literal["Junior", "Senior", "Mid Level"]] = None
    job_major: Optional[str] = None
    years_of_experience: Optional[int] = None
    degree_type: Literal["Bachelor", "Master", "High School"] = None
    skills: Optional[str] = None
    nationality: Optional[str] = None
    city: Optional[str] = None
    salary: Optional[float] = None
    gender: Optional[Literal["Male", "Female", "Not Specified"]] = None
