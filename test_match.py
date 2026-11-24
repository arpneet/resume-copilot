from src.extractor import extract_job, extract_profile
from src.matcher import match

resume = open("samples/sample_resume.txt").read()
job = open("samples/sample_job.txt").read()

result = match(resume, extract_profile(resume), extract_job(job))
for i in result.items:
    print(f"{i.status.upper():8} {i.requirement}  | {i.evidence}")
print("Score:", result.score)