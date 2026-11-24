from src.cover_letter import write_cover_letter
from src.extractor import extract_job, extract_profile
from src.matcher import match

resume = open("samples/sample_resume.txt").read()
job_text = open("samples/sample_job.txt").read()
profile = extract_profile(resume)
job = extract_job(job_text)
result = match(resume, profile, job)

out = write_cover_letter(resume, job_text, profile, job, result, company="Acme Corp")
print(out["letter"])
print("\nVERIFIED:", out["verified"], out["problems"])
assert "python" not in out["letter"].lower(), "PYTHON LEAKED!"
print("PASS: no Python in cover letter.")