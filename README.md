# AI Resume Parser & Career Roadmapper

This project is an AI-powered Career Coach web application that compares a PDF resume against a target job role to perform a detailed skill gap analysis and generates a personalized step-by-step 6-month career roadmap.

## Architecture

The project is structured with a FastAPI backend and a Streamlit frontend:

```
Resume Builder/
├── .env                  # API keys and configurations
├── requirements.txt      # Python dependencies
├── README.md             # Project documentation (this file)
├── backend/
│   ├── parser.py         # PDF text extractor using pypdf
│   ├── schemas.py        # Pydantic validation schemas
│   ├── ai_service.py     # Gemini & OpenAI LLM integrations
│   └── main.py           # FastAPI server and routes
└── frontend/
    └── app.py            # Streamlit dashboard UI
```

- **Backend (FastAPI)**: Extracts raw text from uploaded PDF resumes, constructs detailed, structured prompts, sends them to Gemini (or OpenAI) using modern JSON-schema validation, and exposes endpoints for analysis and health checking.
- **Frontend (Streamlit)**: Provides a visual dashboard to upload resumes, choose target job roles, view matching scores, strengths, and skill gaps side-by-side, and explore a structured vertical timeline of the 6-month career roadmap.

---

## Getting Started

### 1. Prerequisites
Ensure you have Python 3.9+ installed on your system.

### 2. Install Dependencies
Run the following command in the project root directory:
```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables
1. Duplicate the `.env.example` file and rename it to `.env`:
   ```bash
   copy .env.example .env
   ```
2. Open `.env` and fill in your Gemini API key:
   ```env
   AI_PROVIDER=gemini
   GEMINI_API_KEY=AIzaSy...   # Get this from https://aistudio.google.com/
   ```

*(Optional: To use OpenAI, set `AI_PROVIDER=openai` and specify your `OPENAI_API_KEY`.)*

### 4. Running the Application

For the application to function, you need to run **both** the backend and the frontend servers:

#### Start the FastAPI Backend:
From the project root directory, run:
```bash
uvicorn backend.main:app --reload
```
The backend server will start on [http://127.0.0.1:8000](http://127.0.0.1:8000). You can visit [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) to view the interactive OpenAPI documentation.

#### Start the Streamlit Frontend:
In a separate terminal window/tab from the project root directory, run:
```bash
streamlit run frontend/app.py
```
This will automatically launch the Streamlit frontend in your browser, typically at [http://localhost:8501](http://localhost:8501).

---

## How it Works

1. **Upload**: You upload a PDF resume.
2. **Parsing**: The backend parses the PDF text.
3. **AI Coach Analysis**: The backend forwards the text along with the target job to the AI model.
4. **Structured Mapping**: The AI models return structured JSON covering:
   - Match Score (0 - 100)
   - Professional summary of fit
   - Strengths and Gaps
   - Key Certification/Course suggestions
   - Project suggestions to build portfolio
   - Timeline Roadmap (Months 1 to 6)
5. **Interactive UI**: Streamlit displays this elegantly and lets you export the roadmap as a clean Markdown file.
