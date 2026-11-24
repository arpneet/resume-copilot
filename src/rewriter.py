from .llm import call_llm_json
from .prompts import REWRITE_SYSTEM
from .schemas import MatchResult, RewrittenBullet
from .verifier import verify


def rewrite_bullet(bullet: str, match_result: MatchResult) -> RewrittenBullet:
    have = [i.requirement for i in match_result.items if i.status == "matched"]
    missing = [i.requirement for i in match_result.items if i.status != "matched"]
    base = (
        f"ORIGINAL BULLET:\n{bullet}\n\n"
        f"JOB REQUIREMENTS THE CANDIDATE HAS:\n{have}\n\n"
        f"MISSING LIST (never mention):\n{missing}"
    )

    feedback = ""
    for _ in range(2):  # one attempt + one retry
        data = call_llm_json(REWRITE_SYSTEM, base + feedback)
        candidate = data.get("rewritten", "").strip()
        ok, problems = verify(bullet, candidate)
        if ok:
            return RewrittenBullet(original=bullet, rewritten=candidate, verified=True)
        feedback = f"\n\nYOUR LAST ATTEMPT WAS REJECTED: {problems}. Fix it."

    return RewrittenBullet(
        original=bullet,
        rewritten=bullet,  # safe fallback: keep the original
        verified=False,
        note="Rewrite failed fact-check; original kept.",
    )