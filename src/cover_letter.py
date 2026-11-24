from .llm import call_llm_json
from .prompts import COVER_SYSTEM
from .schemas import JobRequirements, MatchResult, Profile
from .verifier import SKILL_VOCAB, _mentions, judge_check
import re


def _check(resume_text: str, job_text: str, letter: str) -> list[str]:
    problems = []
    # Any known skill in the letter must also appear in the resume
    for term in SKILL_VOCAB:
        if _mentions(letter, term) and not _mentions(resume_text, term):
            problems.append(f"skill not in resume: {term}")
    # Any number must appear in the resume or the job description
    num = r"\d+(?:\.\d+)?%?"
    allowed = set(re.findall(num, resume_text)) | set(re.findall(num, job_text))
    for n in set(re.findall(num, letter)) - allowed:
        problems.append(f"unsupported number: {n}")
    if not problems:
        ok, reason = judge_check(resume_text, letter)
        if not ok:
            problems.append(reason)
    return problems


def write_cover_letter(resume_text, job_text, profile: Profile,
                       job: JobRequirements, match_result: MatchResult,
                       company: str = "") -> dict:
    strengths = [i.requirement for i in match_result.items if i.status == "matched"]
    gaps = [i.requirement for i in match_result.items if i.status != "matched"]
    base = (
        f"CANDIDATE NAME: {profile.name}\nROLE: {job.title}\nCOMPANY: {company}\n\n"
        f"RESUME:\n{resume_text}\n\nSTRENGTHS:\n{strengths}\n\nGAPS (never mention):\n{gaps}"
    )
    feedback = ""
    for _ in range(2):
        letter = call_llm_json(COVER_SYSTEM, base + feedback).get("letter", "").strip()
        problems = _check(resume_text, job_text, letter)
        if not problems:
            return {"letter": letter, "verified": True, "problems": []}
        feedback = f"\n\nYOUR LAST DRAFT WAS REJECTED: {problems}. Fix it."
    return {"letter": letter, "verified": False, "problems": problems}