import os
import streamlit as st
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Setup theme/page configuration
st.set_page_config(
    page_title="AI Resume Parser & Career Roadmapper",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Read backend URL from environment variables
BACKEND_URL = os.getenv("BACKEND_URL")
if not BACKEND_URL:
    BACKEND_HOST = os.getenv("BACKEND_HOST", "127.0.0.1")
    BACKEND_PORT = os.getenv("BACKEND_PORT", "8000")
    BACKEND_URL = f"http://{BACKEND_HOST}:{BACKEND_PORT}"


# Modern styling injection
st.markdown(
    """
    <style>
    /* Premium font style */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    
    /* Elegant Title Banner (Bright corporate blue gradient) */
    .title-banner {
        background: linear-gradient(135deg, #008be5 0%, #0c609c 100%);
        color: white;
        padding: 2.5rem;
        border-radius: 16px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
    }
    
    .title-banner h1 {
        font-weight: 800;
        font-size: 2.8rem;
        margin-bottom: 0.5rem;
        color: white !important;
    }
    
    .title-banner p {
        font-size: 1.2rem;
        opacity: 0.9;
        margin: 0;
    }
    
    /* Metrics / Match Score Circle */
    .score-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        background: #f0f4f8;
        border-radius: 50%;
        width: 160px;
        height: 160px;
        margin: 0 auto 1.5rem auto;
        border: 8px solid #008be5;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
    }
    
    .score-value {
        font-size: 3rem;
        font-weight: 800;
        color: #008be5;
    }
    
    .score-label {
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: #555;
        font-weight: 600;
    }
    
    /* Custom cards for strengths and gaps */
    .feature-card {
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.03);
    }
    
    .strength-card {
        background-color: #e6f4ea;
        border-left: 5px solid #137333;
    }
    
    .gap-card {
        background-color: #fce8e6;
        border-left: 5px solid #c5221f;
    }
    
    .card-title {
        font-weight: 600;
        font-size: 1.1rem;
        margin-bottom: 0.5rem;
        color: #202124;
    }
    
    /* Timeline styling */
    .timeline-item {
        border-left: 4px solid #008be5;
        padding-left: 1.5rem;
        padding-bottom: 2rem;
        position: relative;
    }
    
    .timeline-item::before {
        content: '';
        position: absolute;
        width: 16px;
        height: 16px;
        border-radius: 50%;
        background-color: #008be5;
        left: -10px;
        top: 4px;
        border: 3px solid white;
    }
    
    .timeline-month {
        font-weight: 800;
        font-size: 1.3rem;
        color: #0c609c;
        margin-bottom: 0.2rem;
    }
    
    .timeline-focus {
        font-weight: 600;
        font-size: 1.1rem;
        color: #333;
        margin-bottom: 0.8rem;
    }
    
    .timeline-milestone {
        background-color: #f1f3f4;
        padding: 0.6rem 1rem;
        border-radius: 8px;
        font-size: 0.9rem;
        font-style: italic;
        color: #5f6368;
        margin-top: 0.8rem;
        border-left: 3px solid #008be5;
    }

    /* Style override for Streamlit buttons */
    div.stButton > button {
        background-color: #008be5 !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.6rem 1.2rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05) !important;
    }
    div.stButton > button:hover {
        background-color: #0c609c !important;
        color: white !important;
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1) !important;
        transform: translateY(-1px) !important;
    }

    /* Download button specific override */
    div.stDownloadButton > button {
        background-color: #008be5 !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.6rem 1.2rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }
    div.stDownloadButton > button:hover {
        background-color: #0c609c !important;
        color: white !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title Banner
st.markdown(
    """
    <div class="title-banner">
        <h1>AI Career Roadmapper & Coach</h1>
        <p>Upload your resume, name your dream role, and receive a step-by-step roadmap to land the job!</p>
    </div>
    """,
    unsafe_allow_html=True
)

# Check backend health
backend_healthy = False
ai_configured = False
ai_provider = "gemini"

try:
    health_resp = requests.get(f"{BACKEND_URL}/health", timeout=3)
    if health_resp.status_code == 200:
        backend_healthy = True
        health_data = health_resp.json()
        ai_configured = health_data.get("ai_configured", False)
        ai_provider = health_data.get("ai_provider", "gemini")
except Exception:
    backend_healthy = False

# Sidebar Configuration
with st.sidebar:
    st.image("https://img.icons8.com/clouds/200/resume.png", width=120)
    
    st.markdown("### Suggested Roles")
    example_jobs = [
        "Select a role...",
        "Full Stack Developer",
        "Data Scientist",
        "Cloud Architect",
        "Product Manager",
        "Cybersecurity Analyst",
        "Machine Learning Engineer"
    ]
    selected_example = st.selectbox("Quick fill target job:", example_jobs)
    
    st.divider()
    

# Main input forms
col_form, col_info = st.columns([3, 2])

with col_form:
    st.markdown("### 📋 Enter Details & Upload Resume")
    
    # Input target job
    default_job = "" if selected_example == "Select a role..." else selected_example
    target_job = st.text_input(
        "What is your target job/role?",
        value=default_job,
        placeholder="e.g. Senior Machine Learning Engineer, Cloud Security Specialist"
    )
    
    # File Uploader
    uploaded_file = st.file_uploader("Upload your resume (PDF only)", type=["pdf"])
    
    # Run analysis trigger
    analyze_button = st.button("🚀 Analyze & Generate Roadmap", use_container_width=True)

with col_info:
    st.markdown("### 💡 How it works")
    st.info(
        "1. **Upload Resume**: Provide your current PDF resume containing skills and experience.\n"
        "2. **Specify Target Job**: Input the dream job you are working towards.\n"
        "3. **AI Gap Analysis**: Our engine compares your resume text with target job qualifications.\n"
        "4. **Career Roadmap**: We compile a tailored, chronological 6-month pathway complete with project prompts and core certifications."
    )

# Initialize session state for analysis results
if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None
if "analyzed_job" not in st.session_state:
    st.session_state.analyzed_job = ""

# Run logic
if analyze_button:
    if not backend_healthy:
        st.error("Cannot connect to backend API server. Please ensure the backend is running.")
    elif not target_job:
        st.warning("Please specify a Target Job role.")
    elif not uploaded_file:
        st.warning("Please upload a PDF resume file.")
    elif not ai_configured:
        st.error(f"API Key for '{ai_provider.upper()}' is missing in the backend `.env` configuration. Add your key and try again.")
    else:
        # Perform API call with a loader
        with st.spinner("🧠 AI Coach is parsing your resume and mapping your career... Please wait."):
            try:
                # Prepare payload
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
                data = {"target_job": target_job}
                
                # Make POST request to FastAPI
                response = requests.post(f"{BACKEND_URL}/api/analyze", files=files, data=data)
                
                if response.status_code == 200:
                    st.session_state.analysis_result = response.json()
                    st.session_state.analyzed_job = target_job
                    st.success("✅ Analysis completed successfully!")
                else:
                    err_msg = response.json().get("detail", "Unknown backend error occurred.")
                    st.error(f"Backend Server Error ({response.status_code}): {err_msg}")
                    st.session_state.analysis_result = None
                    st.session_state.analyzed_job = ""
            except Exception as e:
                st.error(f"Error communicating with backend API: {str(e)}")
                st.session_state.analysis_result = None
                st.session_state.analyzed_job = ""

# Display analysis results if they exist in session state
if st.session_state.analysis_result:
    result = st.session_state.analysis_result
    job_role = st.session_state.analyzed_job
    
    st.divider()
    
    # Layout analysis results
    st.markdown(f"## 🎯 Career Analysis for **{job_role}**")
    
    # 1. Match Score Metric
    match_percentage = result["analysis"]["match_percentage"]
    st.markdown(
        f"""
        <div class="score-container">
            <div class="score-value">{match_percentage}%</div>
            <div class="score-label">Match Score</div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Summary
    st.markdown("#### Summary of Fit")
    st.write(result["analysis"]["summary"])
    
    st.divider()
    
    # 2. Strengths and Gaps columns
    col_strengths, col_gaps = st.columns(2)
    
    with col_strengths:
        st.markdown(
            """
            <div class="feature-card strength-card">
                <div class="card-title">💪 Key Strengths & Assets</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        for strength in result["analysis"]["strengths"]:
            st.write(f"✅ {strength}")
            
    with col_gaps:
        st.markdown(
            """
            <div class="feature-card gap-card">
                <div class="card-title">⚠️ Identified Skill Gaps</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        for gap in result["analysis"]["gaps"]:
            st.write(f"🔍 {gap}")
            
    st.divider()
    
    # 3. Recommendations
    st.markdown("### 🏆 Recommended Action Items")
    
    rec_col1, rec_col2 = st.columns(2)
    
    with rec_col1:
        st.markdown("#### 🎓 Certifications & Courses")
        for cert in result["recommendations"]["certifications"]:
            with st.expander(f"⭐ **{cert['name']}**"):
                st.write(f"**Provider**: {cert['source']}")
                st.write(f"**Importance**: {cert['importance']}")
                
    with rec_col2:
        st.markdown("#### 🛠️ Portfolio Projects")
        for proj in result["recommendations"]["projects"]:
            with st.expander(f"💻 **{proj['title']}**"):
                st.write(f"**Description**: {proj['description']}")
                st.write(f"**Technologies to use**: {', '.join(proj['technologies_to_use'])}")
                
    st.divider()
    
    # 4. Roadmap Timeline
    st.markdown("### 📅 Personalized 6-Month Roadmap")
    
    for phase in result["roadmap"]:
        tasks_html = "".join([f"<li>{task}</li>" for task in phase["tasks"]])
        st.markdown(
            f"""
            <div class="timeline-item">
                <div class="timeline-month">{phase['month']}</div>
                <div class="timeline-focus">Focus: {phase['focus']}</div>
                <ul>{tasks_html}</ul>
                <div class="timeline-milestone">🏁 Milestone: {phase['milestone']}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    # 5. Export Report
    st.divider()
    st.markdown("### 💾 Export Report")
    
    # Compile Markdown
    md_report = f"# Career roadmap for {job_role}\n\n"
    md_report += f"**Match Score:** {match_percentage}%\n\n"
    md_report += f"## Summary of Fit\n{result['analysis']['summary']}\n\n"
    
    md_report += "## Strengths\n"
    for strength in result["analysis"]["strengths"]:
        md_report += f"- {strength}\n"
    md_report += "\n"
    
    md_report += "## Skill Gaps\n"
    for gap in result["analysis"]["gaps"]:
        md_report += f"- {gap}\n"
    md_report += "\n"
    
    md_report += "## Certifications\n"
    for cert in result["recommendations"]["certifications"]:
        md_report += f"- **{cert['name']}** ({cert['source']}) - Importance: {cert['importance']}\n"
    md_report += "\n"
    
    md_report += "## Projects\n"
    for proj in result["recommendations"]["projects"]:
        md_report += f"- **{proj['title']}**: {proj['description']} (Tech stack: {', '.join(proj['technologies_to_use'])})\n"
    md_report += "\n"
    
    md_report += "## 6-Month Roadmap\n"
    for phase in result["roadmap"]:
        md_report += f"### {phase['month']} - {phase['focus']}\n"
        for task in phase["tasks"]:
            md_report += f"- [ ] {task}\n"
        md_report += f"**Milestone:** {phase['milestone']}\n\n"
        
    st.download_button(
        label="📥 Download Report as Markdown (.md)",
        data=md_report,
        file_name=f"career_roadmap_{job_role.lower().replace(' ', '_')}.md",
        mime="text/markdown",
        use_container_width=True
    )

