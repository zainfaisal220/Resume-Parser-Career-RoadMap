from pydantic import BaseModel, Field
from typing import List, Dict, Any

class SkillGapAnalysis(BaseModel):
    match_percentage: int = Field(
        ..., 
        description="The percentage alignment of the resume to the target job, between 0 and 100."
    )
    summary: str = Field(
        ..., 
        description="A high-level summary of the candidate's fit for the target job."
    )
    strengths: List[str] = Field(
        ..., 
        description="List of key strengths, matching skills, or experiences relevant to the target job."
    )
    gaps: List[str] = Field(
        ..., 
        description="List of key skill gaps, missing certifications, or experiences needed for the target job."
    )

class CertificationInfo(BaseModel):
    name: str = Field(..., description="Name of the certification.")
    source: str = Field(..., description="Provider or platform (e.g. AWS, Coursera, Udemy, Scrum.org).")
    importance: str = Field(..., description="Level of importance, e.g., 'High', 'Medium', 'Optional'.")

class ProjectRecommendation(BaseModel):
    title: str = Field(..., description="A recommended project title to build.")
    description: str = Field(..., description="Detailed explanation of the project, its goals, and what it demonstrates.")
    technologies_to_use: List[str] = Field(..., description="List of technologies, tools, or libraries to employ in this project.")

class Recommendation(BaseModel):
    certifications: List[CertificationInfo] = Field(
        ..., 
        description="Recommended certifications, courses, or training programs to help bridge the skill gaps."
    )
    projects: List[ProjectRecommendation] = Field(
        ..., 
        description="Recommended hands-on projects to build to showcase the required skills."
    )

class RoadmapPhase(BaseModel):
    month: str = Field(..., description="The month range for this phase, e.g., 'Month 1', 'Month 2-3'.")
    focus: str = Field(..., description="The main educational or project building focus of this phase.")
    tasks: List[str] = Field(..., description="Specific, actionable tasks to complete in this phase.")
    milestone: str = Field(..., description="A concrete target/milestone that should be achieved by the end of this phase.")

class ResumeAnalysisResponse(BaseModel):
    target_job: str = Field(..., description="The target job role the resume was analyzed against.")
    analysis: SkillGapAnalysis = Field(..., description="The skill gap and alignment analysis results.")
    recommendations: Recommendation = Field(..., description="Recommended actions, certifications, and projects.")
    roadmap: List[RoadmapPhase] = Field(..., description="A chronological 6-month roadmap divided into phases.")
