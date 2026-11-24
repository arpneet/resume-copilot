from .llm import call_llm_json
from .prompts import JOB_SYSTEM, PROFILE_SYSTEM
from .schemas import JobRequirements, Profile


def extract_profile(resume_text: str) -> Profile:
    data = call_llm_json(PROFILE_SYSTEM, f"RESUME:\n{resume_text}")
    return Profile(**data)  # Pydantic validates the structure


def extract_job(job_text: str) -> JobRequirements:
    data = call_llm_json(JOB_SYSTEM, f"JOB DESCRIPTION:\n{job_text}")
    return JobRequirements(**data)