import pdfplumber
from docx import Document


def read_resume(file) -> str:
    name = file.name.lower()
    if name.endswith(".pdf"):
        with pdfplumber.open(file) as pdf:
            return "\n".join(page.extract_text() or "" for page in pdf.pages)
    if name.endswith(".docx"):
        return "\n".join(p.text for p in Document(file).paragraphs)
    return file.read().decode("utf-8")