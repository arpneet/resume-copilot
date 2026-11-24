import re

from .llm import call_llm_json
from .prompts import MATCH_SYSTEM
from .schemas import JobRequirements, MatchItem, MatchResult, Profile


def _norm(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower()).strip()


def match(resume_text: str, profile: Profile, job: JobRequirements) -> MatchResult:
    requirements = job.must_have + job.nice_to_have
    user = (
        f"RESUME:\n{resume_text}\n\n"
        f"REQUIREMENTS:\n" + "\n".join(f"- {r}" for r in requirements)
    )
    data = call_llm_json(MATCH_SYSTEM, user)

    resume_norm = _norm(resume_text)
    items = []
    for raw in data.get("items", []):
        item = MatchItem(**raw)
        # Guardrail: a claimed match must quote text that really exists
        if item.status in ("matched", "partial"):
            if not item.evidence or _norm(item.evidence) not in resume_norm:
                item.status = "missing"
                item.reason = "Downgraded: evidence not found in resume."
                item.evidence = None
        items.append(item)

    must = set(job.must_have)
    must_items = [i for i in items if i.requirement in must] or items
    points = sum(1.0 if i.status == "matched" else 0.5 if i.status == "partial" else 0
                 for i in must_items)
    score = round(100 * points / len(must_items), 1) if must_items else 0.0
    return MatchResult(items=items, score=score)