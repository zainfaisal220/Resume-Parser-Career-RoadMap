import os
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from backend.parser import extract_text_from_pdf
from backend.ai_service import AIService
from backend.schemas import ResumeAnalysisResponse

# Load environment variables
load_dotenv()

app = FastAPI(
    title="AI Resume Parser & Career Roadmapper API",
    description="Backend API to extract text from resumes and perform skill gap analysis and roadmap generation using AI.",
    version="1.0.0"
)

# Allow CORS for streamlit frontend client
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For local development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize AI Service
try:
    ai_service = AIService()
except Exception as e:
    print(f"Warning: AIService initialization failed. Please set credentials in .env. Error: {str(e)}")
    ai_service = None

@app.get("/")
def read_root():
    """
    Root endpoint returning a welcome message.
    """
    return {
        "message": "Welcome to the AI Resume Parser & Career Roadmapper API!",
        "documentation": "/docs",
        "health": "/health"
    }

@app.get("/health")
def health_check():
    """
    Simple health check endpoint.
    """
    status_info = {
        "status": "healthy",
        "ai_provider": os.getenv("AI_PROVIDER", "gemini"),
        "ai_configured": False
    }
    
    if ai_service is not None:
        if status_info["ai_provider"] == "gemini" and os.getenv("GEMINI_API_KEY"):
            status_info["ai_configured"] = True
        elif status_info["ai_provider"] == "openai" and os.getenv("OPENAI_API_KEY"):
            status_info["ai_configured"] = True
        elif status_info["ai_provider"] == "groq" and os.getenv("GROQ_API_KEY"):
            status_info["ai_configured"] = True
            
    return status_info

@app.post("/api/analyze", response_model=ResumeAnalysisResponse)
async def analyze_resume(
    file: UploadFile = File(..., description="PDF Resume file"),
    target_job: str = Form(..., description="Target Job Role, e.g. Data Scientist")
):
    """
    Upload a PDF resume, parse it, run skill analysis against target job, and generate a 6-month roadmap.
    """
    global ai_service
    
    # Check if AI service is configured
    if ai_service is None:
        try:
            ai_service = AIService()
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"AI Service is not configured. Please set AI credentials in your .env file. Details: {str(e)}"
            )

    # Validate file format
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file format. Please upload a PDF file."
        )
        
    try:
        # Read file contents
        pdf_bytes = await file.read()
        
        # Extract text from PDF
        print(f"Extracting text from PDF: {file.filename}")
        resume_text = extract_text_from_pdf(pdf_bytes)
        
        # Analyze resume using AI Service
        print(f"Analyzing resume against target job: {target_job}")
        analysis_result = ai_service.analyze_resume(resume_text, target_job)
        
        return analysis_result
        
    except ValueError as ve:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ve)
        )
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred during processing: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    host = os.getenv("BACKEND_HOST", "127.0.0.1")
    port = int(os.getenv("BACKEND_PORT", "8000"))
    print(f"Starting backend server on {host}:{port}")
    uvicorn.run(app, host=host, port=port)
