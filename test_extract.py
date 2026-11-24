from src.extractor import extract_job, extract_profile

resume = open("samples/sample_resume.txt").read()
job = open("samples/sample_job.txt").read()

print("PROFILE:")
print(extract_profile(resume).model_dump_json(indent=2))
print("\nJOB:")
print(extract_job(job).model_dump_json(indent=2))
