import os
import json
from dotenv import load_dotenv
import google.generativeai as genai
from backend.schemas import ResumeAnalysisResponse

# Load environment variables
load_dotenv()

class AIService:
    def __init__(self):
        self.provider = os.getenv("AI_PROVIDER", "gemini").lower()
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.groq_api_key = os.getenv("GROQ_API_KEY")
        self.groq_model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
        
        # Configure Gemini if selected
        if self.provider == "gemini":
            if not self.gemini_api_key:
                raise ValueError("GEMINI_API_KEY is not set in environment variables.")
            genai.configure(api_key=self.gemini_api_key)
            
        # Configure OpenAI if selected
        elif self.provider == "openai":
            if not self.openai_api_key:
                raise ValueError("OPENAI_API_KEY is not set in environment variables.")
            try:
                from openai import OpenAI
            except ImportError:
                raise ImportError("openai package is not installed. Please run: pip install openai")
            self.openai_client = OpenAI(api_key=self.openai_api_key)
            
        # Configure Groq if selected
        elif self.provider == "groq":
            if not self.groq_api_key:
                raise ValueError("GROQ_API_KEY is not set in environment variables.")
            try:
                from groq import Groq
            except ImportError:
                raise ImportError("groq package is not installed. Please run: pip install groq")
            self.groq_client = Groq(api_key=self.groq_api_key)

    def analyze_resume(self, resume_text: str, target_job: str) -> ResumeAnalysisResponse:
        """
        Analyzes resume text against the target job using the configured LLM API.
        Returns a structured ResumeAnalysisResponse.
        """
        # Dynamically generate JSON schema from Pydantic model
        try:
            schema_dict = ResumeAnalysisResponse.model_json_schema()
        except AttributeError:
            schema_dict = ResumeAnalysisResponse.schema()
        schema_str = json.dumps(schema_dict, indent=2)

        system_instruction = (
            "You are an expert Career Coach and Tech Recruiter. Your task is to analyze the provided resume text "
            "against the target job role and output a detailed skill gap analysis, recommendations (certifications "
            "and projects), and a step-by-step 6-month learning/career roadmap.\n"
            f"You must return a JSON object that strictly adheres to this JSON schema:\n{schema_str}\n\n"
            "Do not include any markdown formatting like ```json ... ``` outside the output if using JSON mode, just return valid JSON matching the schema."
        )

        prompt = f"""
Target Job Role: {target_job}

Resume Text:
\"\"\"
{resume_text}
\"\"\"

Please analyze this resume and target job role, then generate:
1. The overall match percentage (0-100), a high-level summary of fit, strengths, and specific skill/experience gaps.
2. Certifications/courses that would help bridge these gaps.
3. Relevant hands-on project ideas to build.
4. A chronological 6-month roadmap divided into action phases.
"""

        if self.provider == "gemini":
            return self._analyze_with_gemini(system_instruction, prompt)
        elif self.provider == "openai":
            return self._analyze_with_openai(system_instruction, prompt)
        elif self.provider == "groq":
            return self._analyze_with_groq(system_instruction, prompt)
        else:
            raise ValueError(f"Unsupported AI provider: {self.provider}")

    def _analyze_with_gemini(self, system_instruction: str, prompt: str) -> ResumeAnalysisResponse:
        try:
            # We use gemini-1.5-flash as the fast, efficient model
            model = genai.GenerativeModel(
                model_name="gemini-1.5-flash",
                system_instruction=system_instruction
            )
            
            # Using structured outputs via JSON schema
            response = model.generate_content(
                prompt,
                generation_config=genai.GenerationConfig(
                    response_mime_type="application/json",
                    response_schema=ResumeAnalysisResponse
                )
            )
            
            # Parse response
            response_json = json.loads(response.text)
            return ResumeAnalysisResponse(**response_json)
            
        except Exception as e:
            # Fallback if the Pydantic response_schema is not supported by the environment version
            print(f"Gemini Structured Output error, attempting fallback: {str(e)}")
            try:
                model = genai.GenerativeModel(
                    model_name="gemini-1.5-flash",
                    system_instruction=system_instruction + "\nReturn a JSON object conforming to the ResumeAnalysisResponse schema."
                )
                response = model.generate_content(prompt)
                
                # Strip markdown code blocks if any
                text = response.text.strip()
                if text.startswith("```json"):
                    text = text[7:]
                if text.endswith("```"):
                    text = text[:-3]
                text = text.strip()
                
                response_json = json.loads(text)
                return ResumeAnalysisResponse(**response_json)
            except Exception as inner_e:
                raise RuntimeError(f"Gemini API call failed: {str(inner_e)}")

    def _analyze_with_openai(self, system_instruction: str, prompt: str) -> ResumeAnalysisResponse:
        try:
            # Call OpenAI with JSON mode
            response = self.openai_client.chat.completions.create(
                model="gpt-4o-mini",
                response_format={"type": "json_object"},
                messages=[
                    {"role": "system", "content": system_instruction + "\nYour output must be JSON matching the ResumeAnalysisResponse schema."},
                    {"role": "user", "content": prompt}
                ]
            )
            
            content = response.choices[0].message.content
            response_json = json.loads(content)
            return ResumeAnalysisResponse(**response_json)
        except Exception as e:
            raise RuntimeError(f"OpenAI API call failed: {str(e)}")

    def _analyze_with_groq(self, system_instruction: str, prompt: str) -> ResumeAnalysisResponse:
        try:
            # We use groq client chat completions API with JSON object response format
            response = self.groq_client.chat.completions.create(
                model=self.groq_model,
                response_format={"type": "json_object"},
                messages=[
                    {"role": "system", "content": system_instruction + "\nYour output must be JSON matching the ResumeAnalysisResponse schema."},
                    {"role": "user", "content": prompt}
                ]
            )
            content = response.choices[0].message.content
            response_json = json.loads(content)
            return ResumeAnalysisResponse(**response_json)
        except Exception as e:
            try:
                # Fallback to standard completion
                response = self.groq_client.chat.completions.create(
                    model=self.groq_model,
                    messages=[
                        {"role": "system", "content": system_instruction + "\nYour output must be JSON matching the ResumeAnalysisResponse schema."},
                        {"role": "user", "content": prompt}
                    ]
                )
                content = response.choices[0].message.content
                text = content.strip()
                if text.startswith("```json"):
                    text = text[7:]
                if text.endswith("```"):
                    text = text[:-3]
                text = text.strip()
                response_json = json.loads(text)
                return ResumeAnalysisResponse(**response_json)
            except Exception as inner_e:
                raise RuntimeError(f"Groq API call failed: {str(e)} / {str(inner_e)}")

print("AIService loaded successfully.")
