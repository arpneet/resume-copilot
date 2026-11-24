import re

from .llm import call_llm_json
from .prompts import JUDGE_SYSTEM

# Extend this list over time. Any of these appearing in a rewrite
# but not in the original bullet is an automatic fail.
SKILL_VOCAB = [
    "python", "pandas", "numpy", "scikit-learn", "tensorflow", "pytorch",
    "sql", "mysql", "postgresql", "excel", "power bi", "tableau", "looker",
    "java", "javascript", "c++", "aws", "azure", "gcp", "spark", "hadoop",
    "snowflake", "dbt", "airflow", "git", "docker", "machine learning",
    "a/b testing", "google analytics", "salesforce", "jira",
]


def _mentions(text: str, term: str) -> bool:
    pattern = rf"(?<![\w+#]){re.escape(term)}(?![\w+#])"
    return re.search(pattern, text, re.I) is not None


def rule_check(original: str, rewritten: str) -> list[str]:
    problems = []
    for term in SKILL_VOCAB:
        if _mentions(rewritten, term) and not _mentions(original, term):
            problems.append(f"new skill/tool added: {term}")
    num = r"\d+(?:\.\d+)?%?"
    new_numbers = set(re.findall(num, rewritten)) - set(re.findall(num, original))
    for n in new_numbers:
        problems.append(f"new number added: {n}")
    return problems


def judge_check(original: str, rewritten: str) -> tuple[bool, str]:
    data = call_llm_json(
        JUDGE_SYSTEM, f"ORIGINAL:\n{original}\n\nREWRITTEN:\n{rewritten}"
    )
    return bool(data.get("supported")), data.get("reason", "")


def verify(original: str, rewritten: str) -> tuple[bool, list[str]]:
    problems = rule_check(original, rewritten)
    if problems:  # no need to spend an LLM call if the rules already fail
        return False, problems
    ok, reason = judge_check(original, rewritten)
    return ok, [] if ok else [reason]