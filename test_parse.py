from src.parser import read_resume

with open("samples/sample_resume.txt", "rb") as f:
    print(read_resume(f)[:500])
