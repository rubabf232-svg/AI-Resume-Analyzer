# 📄 AI Resume Analyzer

An AI-assisted resume analysis web app built with Python and Streamlit.

The application compares a resume with a job description and provides:

- Resume text extraction from PDF/DOCX
- Skill detection
- Keyword match percentage
- Matched skills
- Missing skills
- AI-generated improvement suggestions
- JSON report download
- Rule-based fallback when no API key is available

## 🛠️ Tech Stack

- Python
- Streamlit
- Groq API
- PyPDF2
- python-docx
- python-dotenv

## 📁 Project Structure

```text
AI_Resume_Analyzer/
├── app.py
├── analyzer.py
├── resume_parser.py
├── requirements.txt
├── .env.example
└── README.md
```

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/AI-Resume-Analyzer.git
cd AI-Resume-Analyzer
```

### 2. Create a virtual environment

Windows:

```powershell
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

### 4. Configure the API key

Copy `.env.example` to `.env`:

```powershell
copy .env.example .env
```

Open `.env` and add your Groq API key:

```text
GROQ_API_KEY=your_actual_key
```

Never upload `.env` or your API key to GitHub.

### 5. Run

```powershell
streamlit run app.py
```

The application will open in your browser.

## 🔐 Privacy

Resume files may contain personal information. Use test/sample resumes when possible and avoid exposing private resumes or API keys in public repositories.

## ⚠️ Important

This project is an analysis/assistance tool. A keyword match score is not a hiring decision and should not be treated as one.

## 📌 GitHub Description

AI-powered resume analyzer that compares resumes with job descriptions, detects skills, identifies gaps, and generates improvement suggestions.

## 🏷️ Suggested Topics

```text
python
artificial-intelligence
resume-analyzer
streamlit
groq
nlp
career-tools
machine-learning
job-matching
```
