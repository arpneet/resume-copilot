# resume-copilot
# AI Resume Tailoring & Job Matching Copilot

An AI app that tailors a resume to a specific job **without inventing experience**. Upload a resume and a job description, and it extracts skills, finds matches and gaps, rewrites bullet points, and drafts a cover letter. Every output is fact-checked against the original resume.

> [Add a screenshot or GIF of the app here]

## The core problem

LLMs are eager to please. Ask one to "tailor this resume to a Python job" and it will often quietly add Python, even if the candidate has never used it. That puts false claims on a resume, which can get a candidate rejected or fired. This project is built around one rule:

**If a skill isn't on the resume, the AI must never claim it.**

## Features

- Extracts skills, tools, education and experience into a structured profile
- Extracts must-have and nice-to-have requirements from a job description
- Matches requirements to the resume, with quoted evidence for every match
- Flags missing skills instead of hiding them
- Rewrites bullet points using only facts already in the original bullet
- Generates a job-specific cover letter from verified strengths only
- Shows original vs. tailored bullets side by side, with a fact-check status

## How I prevent hallucinations

No single check is trusted. There are several layers:

1. **Prompt constraints.** Every prompt says to use only facts from the resume, never add tools, skills or numbers, and never mention items on the MISSING list.
2. **Evidence-required matching.** The model must quote the resume line that proves each match. Plain code then checks the quote really exists in the resume text. If it doesn't, the match is automatically downgraded to "missing".
3. **Rule-based verifier.** After every rewrite, code compares the output to the original. Any skill or tool from a known vocabulary that appears in the rewrite but not the original, or any new number or percentage, is an automatic rejection. This layer is deterministic and doesn't depend on the model behaving.
4. **LLM judge.** A separate model call acts as a strict fact-checker, asking whether every claim in the rewrite is supported by the original.
5. **Retry, then safe fallback.** A rejected rewrite is retried once with feedback. If it fails again, the original bullet is kept unchanged and flagged.
6. **Structured outputs.** All model responses are parsed into Pydantic schemas, so malformed output fails loudly instead of flowing through.

## Architecture

```
Resume + Job description
        |
   parser.py        PDF / DOCX / TXT -> text
        |
   extractor.py     text -> Profile, JobRequirements (Pydantic)
        |
   matcher.py       requirements -> matched / partial / missing + evidence check
        |
   rewriter.py  <-> verifier.py     rewrite -> rule check -> LLM judge -> retry/fallback
        |
   cover_letter.py  strengths only -> letter -> same verification
        |
   app.py           Streamlit UI
```

## Tech stack

Python, Streamlit, Pydantic, Google Gemini API (swappable through a single `call_llm_json` function in `src/llm.py`), pdfplumber, python-docx, pytest.

## Setup

```bash
git clone https://github.com/<your-username>/resume-copilot.git
cd resume-copilot
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file in the project root:

```
GEMINI_API_KEY=your_key_here
```

Get a free key at [Google AI Studio](https://aistudio.google.com). Never commit `.env`; it is gitignored.

Run the app:

```bash
streamlit run app.py
```

## Tests

```bash
pytest
```

The verifier tests run offline and check that injected skills and numbers are caught.

## Limitations

- The rule-based skill check uses a vocabulary list (`SKILL_VOCAB` in `src/verifier.py`). Skills outside the list rely on the LLM judge.
- The LLM judge is another model call, so it can occasionally miss subtle embellishments such as "regularly" or "extensively".
- Free-tier API models can be slow or overloaded, so calls retry and fall back to other models.
- Evaluated on a small set of sample resumes, not a large benchmark.

## Future improvements

- Larger evaluation set with a hallucination-rate metric
- Expand the skill vocabulary and add synonym handling
- ATS keyword scoring
- Export tailored resume to DOCX/PDF

## Disclaimer

Sample data in `samples/` is fictional. This tool assists with drafting; always review output before sending it to an employer.

<img width="756" height="502" alt="image" src="https://github.com/user-attachments/assets/ccbf9494-ba6d-491c-b8ec-932f25c03d57" />
