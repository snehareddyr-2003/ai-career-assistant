# AI Career Assistant

An AI-powered career assistant that analyzes a candidate's resume against a target job description, identifies skill gaps, and generates a personalized learning roadmap.

## Features

- Resume PDF upload and text extraction
- AI-powered career match analysis
- Job match score out of 100
- Current strengths identification
- Skill gap analysis with priorities
- Personalized 10-week learning roadmap
- Practical project recommendations
- Technical interview preparation
- Final career recommendation
- Downloadable TXT career report
- Downloadable PDF career report
- User-friendly Streamlit dashboard

## How It Works

1. Upload your resume in PDF format.
2. Paste the target job description.
3. Click **Analyze Career Match**.
4. The application extracts the resume content.
5. Gemini analyzes the resume against the job description.
6. The application displays the career analysis and learning roadmap.
7. Download the generated career report as TXT or PDF.

## Tech Stack

- Python
- Streamlit
- Google Gemini API
- Google GenAI Python SDK
- PyPDF2
- ReportLab
- python-dotenv
- Regular Expressions
- Git & GitHub

## Project Structure

```text
ai-career-assistant/
│
├── app.py
├── requirements.txt
├── .gitignore
│
└── utils/
    └── pdf_reader.py
```

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/snehareddyr-2003/ai-career-assistant.git
cd ai-career-assistant
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

Windows:

```bash
venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure the Gemini API key

Create a `.env` file in the project root:

```text
GEMINI_API_KEY=your_api_key_here
```

Do not upload the `.env` file or expose your API key publicly.

### 6. Run the application

```bash
streamlit run app.py
```

The application will open in your browser.

## Screenshots

### 1. Dashboard

Main interface for uploading a resume and entering the target job description.

![Dashboard](dashboard.png)

### 2. Career Analysis

Displays the AI-generated job match score and overall career analysis.

![Career Analysis](career-analysis.png)

### 3. Skill Gap Analysis

Identifies missing skills and prioritizes them based on the target role.

![Skill Gap Analysis](skill-gap-analysis.png)

### 4. Learning Roadmap

Provides a personalized learning roadmap based on the identified skill gaps.

![Learning Roadmap](learning-roadmap.png)

### 5. Projects Recommendation

Suggests practical projects to help the candidate improve the skills required for the target role.

![Projects Recommendation](projects-recommendation.png)

### 6. Interview Preparation

Provides personalized interview topics based on the target role and identified skill gaps.

![Interview Preparation](interview-preparation.png)

### 7. Career Report

Allows the user to download the complete AI-generated career analysis as a PDF report.

![Career Report](career-report.png)
