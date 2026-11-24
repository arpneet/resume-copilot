import streamlit as st

from src.cover_letter import write_cover_letter
from src.extractor import extract_job, extract_profile
from src.matcher import match
from src.parser import read_resume
from src.rewriter import rewrite_bullet

st.set_page_config(page_title="Resume Copilot", layout="wide")
st.title("AI Resume Tailoring & Job Matching Copilot")
st.caption("Every rewrite is fact-checked. It never adds skills you don't have.")

col1, col2 = st.columns(2)
with col1:
    uploaded = st.file_uploader("Resume (PDF, DOCX, or TXT)", type=["pdf", "docx", "txt"])
    pasted = st.text_area("...or paste resume text", height=200)
with col2:
    job_text = st.text_area("Job description", height=300)
company = st.text_input("Company name (optional)")

if st.button("Analyze", type="primary"):
    resume_text = read_resume(uploaded) if uploaded else pasted
    if not resume_text.strip() or not job_text.strip():
        st.error("Please provide both a resume and a job description.")
        st.stop()

    with st.spinner("Extracting skills and requirements..."):
        profile = extract_profile(resume_text)
        job = extract_job(job_text)
    with st.spinner("Matching..."):
        result = match(resume_text, profile, job)
    with st.spinner("Rewriting and fact-checking bullets..."):
        bullets = [rewrite_bullet(b, result)
                   for exp in profile.experiences for b in exp.bullets]
    with st.spinner("Writing cover letter..."):
        letter = write_cover_letter(resume_text, job_text, profile, job, result, company)

    st.session_state["out"] = dict(profile=profile, job=job, result=result,
                                   bullets=bullets, letter=letter)

out = st.session_state.get("out")
if out:
    tabs = st.tabs(["Skills", "Match & Gaps", "Suggestions", "Rewritten Bullets", "Cover Letter"])

    with tabs[0]:
        c1, c2 = st.columns(2)
        c1.subheader("From your resume")
        c1.write(", ".join(out["profile"].skills + out["profile"].tools) or "None found")
        c2.subheader("Job requires")
        c2.write("**Must have:** " + ", ".join(out["job"].must_have))
        c2.write("**Nice to have:** " + ", ".join(out["job"].nice_to_have))

    with tabs[1]:
        st.metric("Match score (must-haves)", f"{out['result'].score}%")
        icons = {"matched": "✅", "partial": "🟡", "missing": "❌"}
        for i in out["result"].items:
            st.write(f"{icons[i.status]} **{i.requirement}**")
            if i.evidence:
                st.caption(f"Evidence: \"{i.evidence}\"")

    with tabs[2]:
        gaps = [i for i in out["result"].items if i.status != "matched"]
        if not gaps:
            st.success("You cover every requirement.")
        for i in gaps:
            st.warning(
                f"**{i.requirement}** isn't clearly shown on your resume. "
                "If you genuinely have this experience, add it with a concrete example. "
                "If not, consider learning it. The tool will never add it for you."
            )

    with tabs[3]:
        for r in out["bullets"]:
            st.markdown(f"**Original:** {r.original}")
            st.markdown(f"**Tailored:** {r.rewritten}")
            st.caption("✅ Fact-checked" if r.verified else f"⚠️ {r.note}")
            st.divider()

    with tabs[4]:
        L = out["letter"]
        st.text_area("Cover letter", L["letter"], height=350)
        st.caption("✅ Fact-checked" if L["verified"] else f"⚠️ {L['problems']}")
        st.download_button("Download cover letter", L["letter"], file_name="cover_letter.txt")