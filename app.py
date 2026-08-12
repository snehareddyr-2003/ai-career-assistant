import streamlit as st
from google import genai
from dotenv import load_dotenv
from utils.pdf_reader import extract_text
import os
import re

from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.units import inch

def clean_ai_text(text):
    lines = text.split("\n")
    cleaned_lines = []

    for line in lines:

        if line.startswith("### "):
            line = "**" + line[4:] + "**"

        elif line.startswith("## "):
            line = "**" + line[3:] + "**"

        cleaned_lines.append(line)

    return "\n".join(cleaned_lines)


# Load environment variables
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error(
        "Gemini API key not found. "
        "Please check your .env file."
    )
    st.stop()

client = genai.Client(api_key=api_key)

# Page configuration
st.set_page_config(
    page_title="AI Career Assistant",
    page_icon="💼",
    layout="wide"
)


# Sidebar
st.sidebar.title("AI Career Assistant")

st.sidebar.write(
    "Your personal AI-powered career companion."
)

st.sidebar.divider()

st.sidebar.write("Features")

st.sidebar.write("• Resume Analysis")
st.sidebar.write("• Career Match")
st.sidebar.write("• Skill Gap Analysis")
st.sidebar.write("• Learning Roadmap")
st.sidebar.write("• Project Recommendations")
st.sidebar.write("• Interview Preparation")


# Main title
st.title("AI Career Assistant")

st.write(
    "Analyze your resume, find skill gaps, and create a personalized career roadmap."
)

st.divider()


# Resume upload
st.subheader("1. Upload Your Resume")

uploaded_file = st.file_uploader(
    "Upload your resume",
    type=["pdf"]
)


# Job description
st.subheader("2. Paste the Job Description")

job_description = st.text_area(
    "Job Description",
    height=250,
    placeholder="Paste the job description here..."
)


# Analyze button
if uploaded_file is not None:

    st.success("Resume uploaded successfully!")

    if st.button("Analyze Career Match", type="primary"):

        if not job_description.strip():

            st.warning("Please paste a job description first.")

        else:

            # Extract resume text
            try:
            
                resume_text = extract_text(uploaded_file)
            
            except Exception as e:
            
                st.error(
                    "Unable to read the uploaded resume. "
                    "Please make sure you uploaded a valid PDF."
                )
            
                st.stop()

            if not resume_text.strip():

                st.error("Could not extract text from this PDF.")

            else:

                # AI prompt
                prompt = f"""
You are an expert technical recruiter, career advisor,
and learning mentor.

Analyze the candidate's resume against the target job description.

IMPORTANT:
- Do not invent skills, experience, certifications, or projects.
- Only use information present in the resume.
- Be honest and practical.
- The candidate is a beginner/entry-level candidate.

Provide the following sections:

## 1. OVERALL JOB MATCH

Start this section exactly like this:

MATCH_SCORE: [number from 0 to 100]

Then provide:
- Match classification: Strong Match, Moderate Match, or Weak Match
- Brief explanation of the score

## 2. CURRENT STRENGTHS

List the skills from the resume that match the job.

## 3. SKILL GAPS

Identify important skills required by the job that are missing
or weak in the resume.

For every skill gap provide:
- Skill
- Priority: High, Medium, or Low
- Why it matters

## 4. LEARNING ROADMAP

Create a realistic 10-week beginner-friendly roadmap.

For every week provide:
- Week number
- Skill/topic
- What to learn
- Practical exercise
- Mini project
- Expected outcome

## 5. PROJECTS TO BUILD

Suggest 3 practical projects that would help the candidate
close the identified skill gaps.

For every project provide:
- Project name
- Skills practiced
- What the project should do
- Why it is useful for the target job

## 6. INTERVIEW PREPARATION

Give 10 technical interview topics based on the job
description and identified skill gaps.

## 7. FINAL RECOMMENDATION

Classify the candidate as:
- Strong Match
- Moderate Match
- Weak Match

Explain what the candidate should prioritize first.

-------------------------
CANDIDATE RESUME
-------------------------

{resume_text}

-------------------------
TARGET JOB DESCRIPTION
-------------------------

{job_description}
"""


                # Call Gemini
                try:
                
                    with st.spinner(
                        "Analyzing your career profile and creating your roadmap..."
                    ):

                        response = client.models.generate_content(
                            model="gemini-3.6-flash",
                            contents=prompt
                        )

                except Exception as e:
                
                    st.error(
                        "Unable to generate the career analysis. "
                        "Please check your internet connection or Gemini API configuration."
                    )

                    st.stop()


                # Get AI response
                result = response.text


                # Display results
                st.divider()

                st.subheader(
                    "AI Career Analysis & Learning Roadmap"
                )


                # Extract match score
                score_match = re.search(
                    r"MATCH_SCORE:\s*(\d+)",
                    result
                )

                if score_match:
                
                    score = int(score_match.group(1))

                    # Determine match classification
                    if score >= 80:
                        match_status = "Strong Match"

                    elif score >= 60:
                        match_status = "Moderate Match"

                    else:
                        match_status = "Weak Match"

                    # Dashboard metrics
                    col1, col2, col3 = st.columns(3)

                    with col1:
                        st.metric(
                            "Job Match Score",
                            f"{score}/100",
                            match_status
                        )

                    with col2:
                        st.metric(
                            "Learning Roadmap",
                            "10 Weeks",
                            "Personalized"
                        )

                    with col3:
                        st.metric(
                            "Projects",
                            "3",
                            "Recommended"
                        )

                    # Match status message
                    if score >= 80:
                        st.success("Strong Match")

                    elif score >= 60:
                        st.warning("Moderate Match")

                    else:
                        st.error("Weak Match")


                # Display the complete AI response
                st.markdown("## Career Analysis")
                # Find the Skill Gaps section
                skill_gap_start = "## 3. SKILL GAPS"
                skill_gap_end = "## 4. LEARNING ROADMAP"

                if skill_gap_start in result:

                    skill_gap = result.split(skill_gap_start, 1)[1]

                    if skill_gap_end in skill_gap:
                        skill_gap = skill_gap.split(skill_gap_end, 1)[0]

                    with st.expander("Skill Gap Analysis", expanded=True):
                        st.markdown("### Skills You Need to Develop")

                        # Try to extract the skill gap table from Gemini's response
                        lines = skill_gap.strip().split("\n")

                        table_lines = []

                        for line in lines:
                            if "|" in line:
                                table_lines.append(line)

                        if len(table_lines) >= 3:
                            table_text = "\n".join(table_lines)
                            st.markdown(table_text)

                        else:
                            st.markdown(skill_gap.strip())
                            
                # Learning Roadmap

                roadmap_start = "## 4. LEARNING ROADMAP"
                roadmap_end = "## 5. PROJECTS TO BUILD"

                if roadmap_start in result:
                
                    roadmap = result.split(roadmap_start, 1)[1]

                    if roadmap_end in roadmap:
                        roadmap = roadmap.split(roadmap_end, 1)[0]

                    with st.expander("10-Week Learning Roadmap", expanded=True):
                    
                        st.markdown(
                            "### Your Personalized 10-Week Learning Plan"
                        )

                        st.markdown(roadmap.strip())
                        
                # Projects to Build

                projects_start = "## 5. PROJECTS TO BUILD"
                projects_end = "## 6. INTERVIEW PREPARATION"

                if projects_start in result:
                
                    projects = result.split(projects_start, 1)[1]

                    if projects_end in projects:
                        projects = projects.split(projects_end, 1)[0]

                    with st.expander("Projects to Build", expanded=True):
                    
                        st.markdown(
                            "### Recommended Projects for Your Career"
                        )

                        st.markdown(projects.strip())
                        
                # Interview Preparation

                interview_start = "## 6. INTERVIEW PREPARATION"
                interview_end = "## 7. FINAL RECOMMENDATION"

                if interview_start in result:
                
                    interview = result.split(interview_start, 1)[1]

                    if interview_end in interview:
                        interview = interview.split(interview_end, 1)[0]

                    with st.expander("Interview Preparation", expanded=True):
                    
                        st.markdown(
                            "### Technical Topics to Prepare"
                        )

                        st.markdown(
                            clean_ai_text(interview.strip()),
                            unsafe_allow_html=False
                        )

                
                        
                # Final Recommendation

                recommendation_start = "## 7. FINAL RECOMMENDATION"

                if recommendation_start in result:
                
                    recommendation = result.split(
                        recommendation_start, 1
                    )[1]

                    with st.expander(
                        "Final Career Recommendation",
                        expanded=True
                    ):

                        st.markdown(
                            "### What You Should Prioritize"
                        )

                        st.markdown(recommendation.strip())
                        
                # Download Career Report

                st.divider()

                st.subheader("Download Your Career Report")

                # TXT download
                st.download_button(
                    label="Download TXT Report",
                    data=result,
                    file_name="AI_Career_Report.txt",
                    mime="text/plain"
                )


                # Create PDF report
                def create_pdf_report(text):
                
                    pdf_path = "AI_Career_Report.pdf"

                    doc = SimpleDocTemplate(
                        pdf_path,
                        pagesize=A4,
                        rightMargin=50,
                        leftMargin=50,
                        topMargin=50,
                        bottomMargin=50
                    )

                    styles = getSampleStyleSheet()

                    title_style = styles["Title"]
                    heading_style = styles["Heading2"]
                    body_style = styles["BodyText"]

                    story = []

                    # Report title
                    story.append(
                        Paragraph(
                            "AI Career Assistant",
                            title_style
                        )
                    )

                    story.append(
                        Paragraph(
                            "Personalized Career Analysis Report",
                            heading_style
                        )
                    )

                    story.append(Spacer(1, 20))

                    # Extract match score
                    score_match = re.search(
                        r"MATCH_SCORE:\s*(\d+)",
                        text
                    )

                    if score_match:
                    
                        score = score_match.group(1)

                        story.append(
                            Paragraph(
                                f"<b>Job Match Score: {score}/100</b>",
                                heading_style
                            )
                        )

                        story.append(Spacer(1, 15))

                    # Process AI response
                    lines = text.split("\n")

                    for line in lines:
                    
                        line = line.strip()

                        if not line:
                            story.append(Spacer(1, 8))
                            continue
                        
                        # Remove MATCH_SCORE from body
                        if line.startswith("MATCH_SCORE:"):
                            continue
                        
                        # Clean markdown
                        line = line.replace("**", "")
                        line = line.replace("### ", "")
                        line = line.replace("## ", "")

                        # Major numbered sections
                        if re.match(r"^[1-7]\.\s", line):
                        
                            story.append(
                                Paragraph(
                                    f"<b>{line}</b>",
                                    heading_style
                                )
                            )

                            story.append(Spacer(1, 8))

                        # Bullet points
                        elif line.startswith("- ") or line.startswith("* "):
                        
                            bullet_text = line[2:]

                            story.append(
                                Paragraph(
                                    f"• {bullet_text}",
                                    body_style
                                )
                            )

                        else:
                        
                            story.append(
                                Paragraph(
                                    line,
                                    body_style
                                )
                            )

                    doc.build(story)

                    return pdf_path


                # Generate PDF
                pdf_file = create_pdf_report(result)

                # PDF download
                with open(pdf_file, "rb") as file:
                
                    pdf_data = file.read()

                st.download_button(
                    label="Download PDF Report",
                    data=pdf_data,
                    file_name="AI_Career_Report.pdf",
                    mime="application/pdf"
                )
                
# Display the complete analysis below
                with st.expander("View Complete AI Analysis", expanded=False):
                    st.markdown(result)