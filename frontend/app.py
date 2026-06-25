import os
import streamlit as st
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def generate_pdf_report(job_role, match_percentage, result):
    from fpdf import FPDF
    
    class PDFReport(FPDF):
        def header(self):
            # Title
            self.set_font('Helvetica', 'B', 15)
            self.set_text_color(0, 139, 229) # #008be5 (Cyan/Blue)
            self.cell(190, 10, 'AI Career Coach - Detailed Report', 0, 1, 'C')
            self.set_draw_color(0, 242, 254) # cyan line
            self.set_line_width(1)
            self.line(10, self.get_y(), 200, self.get_y())
            self.ln(5)

        def footer(self):
            self.set_y(-15)
            self.set_font('Helvetica', 'I', 8)
            self.set_text_color(128, 128, 128)
            self.cell(190, 10, f'Page {self.page_no()}', 0, 0, 'C')

    pdf = PDFReport()
    pdf.set_margin(10)
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Metadata Title
    pdf.set_font('Helvetica', 'B', 12)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(190, 8, f"Target Job: {job_role}", 0, 1, 'L')
    pdf.cell(190, 8, f"Match Score: {match_percentage}%", 0, 1, 'L')
    pdf.ln(5)
    
    # Summary
    pdf.set_font('Helvetica', 'B', 12)
    pdf.set_text_color(0, 139, 229)
    pdf.cell(190, 8, "1. Summary of Fit", 0, 1, 'L')
    pdf.set_font('Helvetica', '', 10)
    pdf.set_text_color(50, 50, 50)
    pdf.multi_cell(190, 5, result["analysis"]["summary"])
    pdf.ln(5)
    
    # Strengths
    pdf.set_font('Helvetica', 'B', 12)
    pdf.set_text_color(0, 139, 229)
    pdf.cell(190, 8, "2. Key Strengths & Assets", 0, 1, 'L')
    pdf.set_font('Helvetica', '', 10)
    pdf.set_text_color(50, 50, 50)
    for strength in result["analysis"]["strengths"]:
        pdf.multi_cell(190, 5, f"- {strength}")
    pdf.ln(5)
    
    # Skill Gaps
    pdf.set_font('Helvetica', 'B', 12)
    pdf.set_text_color(220, 53, 69) # Red color for gaps
    pdf.cell(190, 8, "3. Identified Skill Gaps", 0, 1, 'L')
    pdf.set_font('Helvetica', '', 10)
    pdf.set_text_color(50, 50, 50)
    for gap in result["analysis"]["gaps"]:
        pdf.multi_cell(190, 5, f"- {gap}")
    pdf.ln(5)
    
    # Certifications
    pdf.set_font('Helvetica', 'B', 12)
    pdf.set_text_color(0, 139, 229)
    pdf.cell(190, 8, "4. Recommended Certifications & Courses", 0, 1, 'L')
    pdf.set_font('Helvetica', '', 10)
    pdf.set_text_color(50, 50, 50)
    for cert in result["recommendations"]["certifications"]:
        pdf.multi_cell(190, 5, f"- {cert['name']} ({cert['source']}) - Importance: {cert['importance']}")
    pdf.ln(5)
    
    # Projects
    pdf.set_font('Helvetica', 'B', 12)
    pdf.set_text_color(0, 139, 229)
    pdf.cell(190, 8, "5. Recommended Portfolio Projects", 0, 1, 'L')
    for proj in result["recommendations"]["projects"]:
        pdf.set_font('Helvetica', 'B', 10)
        pdf.set_text_color(50, 50, 50)
        pdf.multi_cell(190, 5, f"* {proj['title']}")
        pdf.set_font('Helvetica', '', 9)
        pdf.set_text_color(80, 80, 80)
        pdf.multi_cell(190, 5, f"  Description: {proj['description']}")
        pdf.multi_cell(190, 5, f"  Technologies: {', '.join(proj['technologies_to_use'])}")
        pdf.ln(2)
    pdf.ln(3)
    
    # Roadmap
    pdf.set_font('Helvetica', 'B', 12)
    pdf.set_text_color(0, 139, 229)
    pdf.cell(190, 8, "6. Personalized 6-Month Roadmap", 0, 1, 'L')
    for phase in result["roadmap"]:
        pdf.set_font('Helvetica', 'B', 10)
        pdf.set_text_color(0, 139, 229)
        pdf.cell(190, 6, f"{phase['month']} - Focus: {phase['focus']}", 0, 1, 'L')
        pdf.set_font('Helvetica', '', 9)
        pdf.set_text_color(50, 50, 50)
        for task in phase["tasks"]:
            pdf.multi_cell(190, 5, f"  [ ] {task}")
        pdf.set_font('Helvetica', 'I', 9)
        pdf.set_text_color(100, 100, 100)
        pdf.multi_cell(190, 5, f"  Milestone: {phase['milestone']}")
        pdf.ln(3)

    return bytes(pdf.output())

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
    
    /* Fade-in animation definition */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(15px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Pulse glow animation definition */
    @keyframes neonGlow {
        0% { box-shadow: 0 0 10px rgba(0, 242, 254, 0.15); }
        50% { box-shadow: 0 0 25px rgba(0, 242, 254, 0.45); }
        100% { box-shadow: 0 0 10px rgba(0, 242, 254, 0.15); }
    }

    /* Force dark background and white/pale text colors */
    .stApp {
        background-color: #070b13 !important;
        color: #ffffff !important;
    }
    
    /* Headers formatting */
    .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6 {
        color: #ffffff !important;
        font-family: 'Outfit', sans-serif;
    }
    
    /* Regular text styling (spans excluded to prevent icon text bug) */
    .stApp p, .stApp label, .stApp li {
        color: #94a3b8 !important;
        font-family: 'Outfit', sans-serif;
    }
    
    /* Sidebar override to dark theme with subtle border */
    [data-testid="stSidebar"] {
        background-color: #0a0f1d !important;
        border-right: 1px solid rgba(0, 242, 254, 0.15) !important;
    }

    /* Elegant Title Banner (Dark background with glowing neon cyan borders) */
    .title-banner {
        background: linear-gradient(135deg, #0f172a 0%, #070b13 100%);
        border: 1px solid rgba(0, 242, 254, 0.25);
        color: white;
        padding: 2.5rem;
        border-radius: 16px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 0 20px rgba(0, 242, 254, 0.08);
        animation: fadeIn 0.8s ease-out;
    }
    
    .title-banner h1 {
        font-weight: 800;
        font-size: 2.8rem;
        margin-bottom: 0.5rem;
        color: #00f2fe !important;
        text-shadow: 0 0 15px rgba(0, 242, 254, 0.35);
    }
    
    .title-banner p {
        font-size: 1.2rem;
        opacity: 0.9;
        margin: 0;
        color: #94a3b8 !important;
    }
    
    /* Metrics / Match Score Circle with pulse animation */
    .score-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        background: #0a0f1d;
        border-radius: 50%;
        width: 160px;
        height: 160px;
        margin: 0 auto 1.5rem auto;
        border: 4px solid #00f2fe;
        box-shadow: 0 0 20px rgba(0, 242, 254, 0.2);
        animation: neonGlow 3s infinite ease-in-out;
    }
    
    .score-value {
        font-size: 3rem;
        font-weight: 800;
        color: #00f2fe !important;
        text-shadow: 0 0 12px rgba(0, 242, 254, 0.4);
    }
    
    .score-label {
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: #94a3b8 !important;
        font-weight: 600;
    }
    
    /* Custom cards for strengths and gaps with hover lift and glowing colors */
    .feature-card {
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 1rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        animation: fadeIn 0.6s ease-out;
    }
    .feature-card:hover {
        transform: translateY(-4px);
    }
    
    .strength-card {
        background-color: rgba(16, 185, 129, 0.06) !important;
        border: 1px solid rgba(16, 185, 129, 0.25) !important;
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.05);
    }
    .strength-card:hover {
        box-shadow: 0 6px 20px rgba(16, 185, 129, 0.18);
        border-color: rgba(16, 185, 129, 0.5) !important;
    }
    
    .gap-card {
        background-color: rgba(239, 68, 68, 0.06) !important;
        border: 1px solid rgba(239, 68, 68, 0.25) !important;
        box-shadow: 0 4px 15px rgba(239, 68, 68, 0.05);
    }
    .gap-card:hover {
        box-shadow: 0 6px 20px rgba(239, 68, 68, 0.18);
        border-color: rgba(239, 68, 68, 0.5) !important;
    }
    
    .card-title {
        font-weight: 600;
        font-size: 1.1rem;
        margin-bottom: 0.5rem;
        color: #ffffff !important;
    }
    
    /* Timeline styling */
    .timeline-item {
        border-left: 4px solid #00f2fe;
        padding-left: 1.5rem;
        padding-bottom: 2rem;
        position: relative;
        animation: fadeIn 0.7s ease-out;
    }
    
    .timeline-item::before {
        content: '';
        position: absolute;
        width: 16px;
        height: 16px;
        border-radius: 50%;
        background-color: #00f2fe;
        left: -10px;
        top: 4px;
        border: 3px solid #070b13;
        box-shadow: 0 0 10px rgba(0, 242, 254, 0.5);
    }
    
    .timeline-month {
        font-weight: 800;
        font-size: 1.3rem;
        color: #00f2fe !important;
        margin-bottom: 0.2rem;
        text-shadow: 0 0 8px rgba(0, 242, 254, 0.3);
    }
    
    .timeline-focus {
        font-weight: 600;
        font-size: 1.1rem;
        color: #ffffff !important;
        margin-bottom: 0.8rem;
    }
    
    .timeline-milestone {
        background-color: #0a0f1d;
        padding: 0.6rem 1rem;
        border-radius: 8px;
        font-size: 0.9rem;
        font-style: italic;
        color: #94a3b8;
        margin-top: 0.8rem;
        border-left: 3px solid #00f2fe;
        border: 1px solid rgba(0, 242, 254, 0.15);
    }

    /* Style override for Streamlit input controls */
    .stTextInput input, .stSelectbox [data-baseweb="select"] {
        background-color: #0a0f1d !important;
        color: #ffffff !important;
        border: 1px solid rgba(0, 242, 254, 0.2) !important;
        border-radius: 8px !important;
    }
    .stTextInput input:focus, .stSelectbox [data-baseweb="select"]:focus-within {
        border-color: #00f2fe !important;
        box-shadow: 0 0 10px rgba(0, 242, 254, 0.25) !important;
    }

    /* Style override for Streamlit file uploader drop zone */
    [data-testid="stFileUploaderDropzone"] {
        background-color: #0a0f1d !important;
        border: 2px dashed rgba(0, 242, 254, 0.25) !important;
        border-radius: 8px !important;
    }
    [data-testid="stFileUploaderDropzone"]:hover {
        border-color: #00f2fe !important;
        background-color: rgba(0, 242, 254, 0.02) !important;
    }

    /* Style override for Streamlit buttons with neon gradient and glow on hover */
    div.stButton > button, div.stDownloadButton > button {
        background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%) !important;
        color: #070b13 !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.6rem 1.2rem !important;
        font-weight: 800 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 0 12px rgba(0, 242, 254, 0.15) !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    /* Force nested elements (like paragraphs or icons) inside buttons to be dark for high contrast */
    div.stButton > button *, div.stDownloadButton > button * {
        color: #070b13 !important;
    }
    div.stButton > button:hover, div.stDownloadButton > button:hover {
        box-shadow: 0 0 22px rgba(0, 242, 254, 0.5) !important;
        transform: translateY(-2px) !important;
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
    
    # Generate PDF bytes
    try:
        pdf_bytes = generate_pdf_report(job_role, match_percentage, result)
        
        st.download_button(
            label="📥 Download Report as PDF (.pdf)",
            data=pdf_bytes,
            file_name=f"career_roadmap_{job_role.lower().replace(' ', '_')}.pdf",
            mime="application/pdf",
            use_container_width=True
        )
    except Exception as e:
        st.error(f"Failed to generate PDF: {str(e)}")

