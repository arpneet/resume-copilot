from src.extractor import extract_job, extract_profile
from src.matcher import match
from src.rewriter import rewrite_bullet
from src.verifier import verify

# Test 1: the verifier must catch invention
ok, why = verify("Built dashboards in Power BI", "Built Python dashboards in Power BI")
print("Inject Python caught:", not ok, why)
ok, why = verify("Built dashboards in Power BI", "Built dashboards in Power BI, cutting reporting time 40%")
print("Inject number caught:", not ok, why)

# Test 2: full pipeline
resume = open("samples/sample_resume.txt").read()
job = open("samples/sample_job.txt").read()
profile = extract_profile(resume)
result = match(resume, profile, extract_job(job))

for exp in profile.experiences:
    for b in exp.bullets:
        r = rewrite_bullet(b, result)
        print(f"\nOLD: {r.original}\nNEW: {r.rewritten}\nVERIFIED: {r.verified}")
        assert "python" not in r.rewritten.lower(), "PYTHON LEAKED!"

print("\nPASS: no invented Python anywhere.")