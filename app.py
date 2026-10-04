import streamlit as st

from resume_parser import extract_resume_text
from analyzer import analyze_resume


# -----------------------------------------------------------------------------
# Page Configuration
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="ResumeAI - AI Resume Analyzer",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# Sample Resumes and Multi-Sector Job Descriptions
# -----------------------------------------------------------------------------
SAMPLE_RESUME_TEXT = """John Doe
Senior Software Engineer | Full-Stack & Python Developer
Email: john.doe@example.com | Phone: (555) 123-4567 | Portfolio: github.com/johndoe
Location: New York, NY | linkedin.com/in/johndoe

Summary:
Dedicated and results-oriented Software Engineer with 5+ years of experience designing, building,
and deploying scalable web applications, REST APIs, and data-driven systems. Strong proficiency in
Python, SQL, Docker, Git, and modern frontend frameworks.

Technical Skills:
- Languages: Python, JavaScript, Java, C++, SQL
- Frameworks & Web: Django, FastAPI, React, HTML, CSS
- Databases: PostgreSQL, MySQL, MongoDB, Redis
- Tools & Cloud: Git, GitHub, Docker, Kubernetes, Linux, VS Code
- Data & Analytics: Pandas, NumPy, Scikit-learn, Machine Learning

Professional Experience:
Senior Software Engineer | TechSphere Solutions (2021 - Present)
- Architected and maintained high-throughput microservices using Python and Django, handling 150k+ daily requests.
- Optimized PostgreSQL relational queries and database schemas, reducing latency by 35%.
- Built automated testing workflows with Git and containerized microservices using Docker.
- Collaborated with frontend engineers to integrate React, HTML, and CSS client dashboards.

Software Engineer | Innovate Analytics (2019 - 2021)
- Developed automated data cleaning and reporting workflows in Python, Pandas, and NumPy.
- Trained predictive classification models with Scikit-learn to optimize customer retention.
- Managed version control and continuous integration via Git and GitHub.

Projects:
- Microservices E-Commerce API: Built scalable Django REST APIs with PostgreSQL, Redis caching, and Docker.
- Predictive Analytics Pipeline: Machine Learning model predicting user churn using Scikit-learn and Pandas.

Education:
Bachelor of Science in Computer Science | State University of Technology (2015 - 2019)
GPA: 3.8 / 4.0

Certifications:
- Certified Docker Administrator
- Python Professional Developer Certificate
"""

SAMPLE_JDS = {
    "Python Developer": """Role: Senior Python Developer
Company: CloudScale Dynamics
Location: Remote / Hybrid

About the Role:
We are seeking an experienced Senior Python Developer to build and scale our backend microservices and data pipelines.

Requirements:
- 4+ years of professional backend development experience with Python.
- Strong proficiency in SQL, PostgreSQL, and database design.
- Hands-on experience building REST APIs with Django or FastAPI.
- Solid experience with Docker, Git, and Linux environments.

Preferred Qualifications:
- Experience with Redis caching and microservices architecture.
- Familiarity with Machine Learning workflows using Pandas or Scikit-learn.
- Bachelor's degree in Computer Science or Software Engineering.
""",
    "Data Analyst": """Role: Data Analyst
Company: Metro Analytics Group
Location: Chicago, IL / Hybrid

About the Role:
We are looking for a Data Analyst to translate complex business data into actionable insights, dashboards, and reports.

Requirements:
- 3+ years of experience in Data Analysis, SQL, and Excel.
- Demonstrated experience creating business dashboards and KPIs.
- Strong understanding of data cleaning and relational databases.

Preferred Qualifications:
- Experience with Power BI, Tableau, or Data Visualization tools.
- Proficiency in Python, Pandas, or R for statistical analysis.
- Degree in Statistics, Mathematics, Economics, or Business Analytics.
""",
    "Frontend Developer": """Role: Frontend Developer
Company: PixelCraft Media
Location: San Francisco, CA / Remote

About the Role:
We need a creative and detail-driven Frontend Developer to build responsive user interfaces and web applications.

Requirements:
- 3+ years of experience in HTML, CSS, JavaScript, and React.
- Deep understanding of Responsive Design and State Management.
- Experience consuming REST APIs and collaborative version control using Git.

Preferred Qualifications:
- Experience with TypeScript, Next.js, and Tailwind CSS.
- Familiarity with Figma wireframing and prototyping.
- Degree in Computer Science or Interactive Design.
"""
}

# -----------------------------------------------------------------------------
# Custom Styling (Light theme, Purple accent, Rounded cards, Professional look)
# -----------------------------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }

    .stApp {
        background-color: #F8FAFC;
        color: #1E293B;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF;
        border-right: 1px solid #E2E8F0;
    }

    /* Sidebar Header */
    .sidebar-brand {
        padding: 4px 2px 18px 2px;
        border-bottom: 1px solid #F1F5F9;
        margin-bottom: 20px;
    }

    .brand-title {
        font-size: 26px;
        font-weight: 800;
        color: #7C3AED;
        letter-spacing: -0.6px;
        line-height: 1.1;
    }

    .brand-subtitle {
        font-size: 11px;
        font-weight: 700;
        color: #94A3B8;
        letter-spacing: 1.6px;
        text-transform: uppercase;
        margin-top: 4px;
    }

    /* Sidebar Navigation Buttons */
    [data-testid="stSidebar"] div.stButton {
        margin-bottom: 4px;
    }

    [data-testid="stSidebar"] div.stButton > button[kind="primary"] {
        background: #7C3AED !important;
        color: #FFFFFF !important;
        border: 1px solid #7C3AED !important;
        border-radius: 8px !important;
        font-size: 14px !important;
        font-weight: 600 !important;
        text-align: left !important;
        justify-content: flex-start !important;
        padding: 10px 16px !important;
        box-shadow: 0 2px 6px rgba(124, 58, 237, 0.25) !important;
    }

    [data-testid="stSidebar"] div.stButton > button:not([kind="primary"]) {
        background: transparent !important;
        color: #475569 !important;
        border: 1px solid transparent !important;
        border-radius: 8px !important;
        font-size: 14px !important;
        font-weight: 500 !important;
        text-align: left !important;
        justify-content: flex-start !important;
        padding: 10px 16px !important;
        box-shadow: none !important;
    }

    [data-testid="stSidebar"] div.stButton > button:not([kind="primary"]):hover {
        background: #F5F3FF !important;
        color: #7C3AED !important;
        border-color: #EDE9FE !important;
    }

    /* Sidebar Bottom Status */
    .status-card {
        background-color: #FAF5FF;
        border: 1px solid #EDE9FE;
        border-radius: 10px;
        padding: 14px 16px;
        margin-top: 40px;
    }

    .status-title {
        font-size: 11px;
        font-weight: 700;
        color: #7C3AED;
        letter-spacing: 1px;
        text-transform: uppercase;
    }

    .status-row {
        display: flex;
        align-items: center;
        gap: 8px;
        margin-top: 8px;
    }

    .status-dot {
        height: 8px;
        width: 8px;
        background-color: #10B981;
        border-radius: 50%;
        display: inline-block;
        box-shadow: 0 0 0 2px rgba(16, 185, 129, 0.2);
    }

    .status-text {
        font-size: 13px;
        font-weight: 600;
        color: #1E293B;
    }

    /* Main Content Headers */
    .dashboard-header {
        margin-bottom: 24px;
    }

    .dashboard-title {
        font-size: 30px;
        font-weight: 800;
        color: #1E293B;
        letter-spacing: -0.6px;
        margin-bottom: 4px;
    }

    .dashboard-subtitle {
        font-size: 15px;
        color: #64748B;
        margin-bottom: 0px;
    }

    /* Input Card Headers */
    .card-header-row {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 4px;
    }

    .card-title-text {
        font-size: 18px;
        font-weight: 700;
        color: #1E293B;
        margin: 0;
    }

    .card-subtext {
        font-size: 13px;
        color: #64748B;
        margin-bottom: 12px;
    }

    /* Main Area Primary Button (Analyze Resume) */
    div[data-testid="stMainBlockContainer"] div.stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #7C3AED 0%, #6D28D9 100%) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 10px !important;
        font-size: 16px !important;
        font-weight: 600 !important;
        padding: 12px 28px !important;
        box-shadow: 0 4px 14px rgba(124, 58, 237, 0.28) !important;
        transition: all 0.2s ease !important;
    }

    div[data-testid="stMainBlockContainer"] div.stButton > button[kind="primary"]:hover {
        background: linear-gradient(135deg, #6D28D9 0%, #5B21B6 100%) !important;
        box-shadow: 0 6px 20px rgba(124, 58, 237, 0.38) !important;
        transform: translateY(-1px);
    }

    /* Main Area Secondary Buttons */
    div[data-testid="stMainBlockContainer"] div.stButton > button:not([kind="primary"]) {
        border: 1px solid #E2E8F0 !important;
        border-radius: 8px !important;
        color: #4B5563 !important;
        font-weight: 500 !important;
        background-color: #FFFFFF !important;
        transition: all 0.15s ease !important;
    }

    div[data-testid="stMainBlockContainer"] div.stButton > button:not([kind="primary"]):hover {
        border-color: #7C3AED !important;
        color: #7C3AED !important;
        background-color: #FAF5FF !important;
    }

    /* Role Detection Banner */
    .role-banner {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-left: 5px solid #7C3AED;
        border-radius: 12px;
        padding: 20px 24px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
        margin-bottom: 24px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 16px;
    }

    .role-banner-left {
        display: flex;
        flex-direction: column;
        gap: 4px;
    }

    .role-banner-label {
        font-size: 12px;
        font-weight: 700;
        color: #7C3AED;
        letter-spacing: 1px;
        text-transform: uppercase;
    }

    .role-banner-title {
        font-size: 26px;
        font-weight: 800;
        color: #1E293B;
        letter-spacing: -0.4px;
    }

    .overall-score-box {
        display: flex;
        align-items: center;
        gap: 14px;
        background: #F5F3FF;
        border: 1px solid #DDD6FE;
        border-radius: 10px;
        padding: 10px 18px;
    }

    .overall-score-number {
        font-size: 34px;
        font-weight: 800;
        color: #6D28D9;
        line-height: 1;
    }

    .overall-score-meta {
        display: flex;
        flex-direction: column;
    }

    .overall-score-label {
        font-size: 11px;
        font-weight: 700;
        color: #6D28D9;
        letter-spacing: 0.5px;
        text-transform: uppercase;
    }

    .overall-score-sub {
        font-size: 11px;
        color: #64748B;
    }

    /* Metric Cards */
    .metric-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 18px 20px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
        margin-bottom: 16px;
    }

    .metric-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .metric-title {
        font-size: 13px;
        font-weight: 600;
        color: #64748B;
    }

    .metric-value {
        font-size: 36px;
        font-weight: 800;
        color: #7C3AED;
        margin: 8px 0 10px 0;
        line-height: 1;
    }

    .metric-bar-bg {
        width: 100%;
        height: 6px;
        background-color: #F1F5F9;
        border-radius: 9999px;
        overflow: hidden;
    }

    .metric-bar-fill {
        height: 100%;
        background: linear-gradient(90deg, #7C3AED 0%, #A78BFA 100%);
        border-radius: 9999px;
    }

    .metric-bar-fill-indigo {
        height: 100%;
        background: linear-gradient(90deg, #4F46E5 0%, #818CF8 100%);
        border-radius: 9999px;
    }

    .metric-bar-fill-emerald {
        height: 100%;
        background: linear-gradient(90deg, #059669 0%, #34D399 100%);
        border-radius: 9999px;
    }

    .metric-bar-fill-amber {
        height: 100%;
        background: linear-gradient(90deg, #D97706 0%, #FBBF24 100%);
        border-radius: 9999px;
    }

    /* Result Content Cards */
    .result-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 20px 22px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
        margin-bottom: 20px;
    }

    .result-card-title {
        font-size: 16px;
        font-weight: 700;
        color: #1E293B;
        margin-bottom: 12px;
    }

    /* Chips & Tags */
    .chips-container {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        margin-top: 4px;
    }

    .skill-chip {
        display: inline-flex;
        align-items: center;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: 500;
    }

    .chip-match {
        background-color: #ECFDF5;
        color: #065F46;
        border: 1px solid #A7F3D0;
    }

    .chip-missing-req {
        background-color: #FEF2F2;
        color: #991B1B;
        border: 1px solid #FECACA;
    }

    .chip-missing-pref {
        background-color: #FFFBEB;
        color: #92400E;
        border: 1px solid #FDE68A;
    }

    .chip-resume {
        background-color: #FAF5FF;
        color: #6B21A8;
        border: 1px solid #E9D5FF;
    }

    .chip-job {
        background-color: #F8FAFC;
        color: #334155;
        border: 1px solid #CBD5E1;
    }

    /* Section Checklist */
    .checklist-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
        gap: 10px;
        margin-top: 8px;
    }

    .check-item {
        display: flex;
        align-items: center;
        gap: 8px;
        padding: 8px 12px;
        border-radius: 8px;
        font-size: 13px;
        font-weight: 500;
    }

    .check-pass {
        background: #F0FDF4;
        color: #166534;
        border: 1px solid #BBF7D0;
    }

    .check-missing {
        background: #F8FAFC;
        color: #94A3B8;
        border: 1px solid #E2E8F0;
    }

    /* Evaluation details */
    .eval-row {
        display: flex;
        align-items: flex-start;
        gap: 12px;
        background: #F8FAFC;
        padding: 12px 16px;
        border-radius: 8px;
        margin-bottom: 8px;
        border-left: 3px solid #7C3AED;
    }

    .eval-icon {
        font-size: 16px;
        margin-top: 2px;
    }

    .eval-content {
        display: flex;
        flex-direction: column;
        gap: 2px;
    }

    .eval-title {
        font-size: 13px;
        font-weight: 700;
        color: #1E293B;
    }

    .eval-desc {
        font-size: 13px;
        color: #475569;
    }

    .empty-notice {
        font-size: 13px;
        color: #94A3B8;
        font-style: italic;
        margin-top: 4px;
    }

    /* Target Job Description & General Textarea Styling */
    div[data-testid="stTextArea"] div[data-baseweb="textarea"] {
        background-color: #FFFFFF !important;
        border: 1px solid #CBD5E1 !important;
        border-radius: 8px !important;
        transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
    }

    div[data-testid="stTextArea"] div[data-baseweb="textarea"]:focus-within {
        border-color: #7C3AED !important;
        box-shadow: 0 0 0 2px rgba(124, 58, 237, 0.2) !important;
    }

    div[data-testid="stTextArea"] textarea,
    textarea {
        background-color: #FFFFFF !important;
        color: #111827 !important;
        -webkit-text-fill-color: #111827 !important;
        caret-color: #111827 !important;
        font-size: 14px !important;
        line-height: 1.5 !important;
        border-radius: 8px !important;
    }

    div[data-testid="stTextArea"] textarea:focus,
    textarea:focus {
        background-color: #FFFFFF !important;
        color: #111827 !important;
        -webkit-text-fill-color: #111827 !important;
        outline: none !important;
    }

    div[data-testid="stTextArea"] textarea::placeholder,
    textarea::placeholder {
        color: #6B7280 !important;
        -webkit-text-fill-color: #6B7280 !important;
        opacity: 1 !important;
    }
</style>
""", unsafe_allow_html=True)



# -----------------------------------------------------------------------------
# 4. Streamlit session_state Management
# -----------------------------------------------------------------------------
if "current_page" not in st.session_state:
    st.session_state["current_page"] = "Dashboard"

if "resume_text" not in st.session_state:
    st.session_state["resume_text"] = SAMPLE_RESUME_TEXT

if "file_name" not in st.session_state:
    st.session_state["file_name"] = "sample_resume_john_doe.docx"

if "job_description_text" not in st.session_state:
    st.session_state["job_description_text"] = SAMPLE_JDS["Python Developer"]

if "use_sample_resume" not in st.session_state:
    st.session_state["use_sample_resume"] = True

if "analysis_result" not in st.session_state or st.session_state["analysis_result"] is None:
    # Run initial baseline analysis on session start so all tabs are populated immediately
    st.session_state["analysis_result"] = analyze_resume(
        st.session_state["resume_text"],
        st.session_state["job_description_text"]
    )


# -----------------------------------------------------------------------------
# 1. Left Sidebar Navigation
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <div class="brand-title">ResumeAI</div>
        <div class="brand-subtitle">ANALYZER & IMPROVER</div>
    </div>
    """, unsafe_allow_html=True)

    nav_items = [
        ("Dashboard", "📊"),
        ("Resume Analysis", "📄"),
        ("Job Match", "🎯"),
        ("Resume Improvement", "💡")
    ]

    for page_name, icon in nav_items:
        is_active = (st.session_state["current_page"] == page_name)
        button_label = f"{icon}  {page_name}"
        if st.button(
            button_label,
            key=f"nav_btn_{page_name}",
            use_container_width=True,
            type="primary" if is_active else "secondary"
        ):
            if st.session_state["current_page"] != page_name:
                st.session_state["current_page"] = page_name
                st.rerun()

    st.markdown("<div style='min-height: 180px;'></div>", unsafe_allow_html=True)

    st.markdown("""
    <div class="status-card">
        <div class="status-title">Application Status</div>
        <div class="status-row">
            <span class="status-dot"></span>
            <span class="status-text">Analyzer Ready</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# Core Helper: Execute Analysis & Update Session State
# -----------------------------------------------------------------------------
def trigger_analysis():
    if not st.session_state.get("resume_text", "").strip():
        st.warning("Please upload a resume or click 'Load Sample'.")
        return

    if not st.session_state.get("job_description_text", "").strip():
        st.warning("Please enter a target job description or choose a Sample JD.")
        return

    result = analyze_resume(
        st.session_state["resume_text"],
        st.session_state["job_description_text"]
    )
    st.session_state["analysis_result"] = result


# -----------------------------------------------------------------------------
# 10. Page View Helpers
# -----------------------------------------------------------------------------

def show_dashboard():
    """Renders the main Dashboard view with resume upload, job description input, and analysis results."""
    st.markdown("""
    <div class="dashboard-header">
        <div class="dashboard-title">AI Resume Analyzer</div>
        <div class="dashboard-subtitle">Analyze your resume and compare it with a target job description.</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown("""
        <div class="card-header-row">
            <span class="card-title-text">1. Resume Upload</span>
        </div>
        <div class="card-subtext">Upload your resume (PDF or DOCX)</div>
        """, unsafe_allow_html=True)

        uploaded_file = st.file_uploader(
            "Upload your resume",
            type=["pdf", "docx"],
            help="Drag and drop or browse your resume in PDF or DOCX format."
        )

        if uploaded_file is not None:
            if st.session_state.get("file_name") != uploaded_file.name:
                extracted = extract_resume_text(uploaded_file)
                if extracted and extracted != "Unsupported file format.":
                    st.session_state["resume_text"] = extracted
                    st.session_state["file_name"] = uploaded_file.name
                    st.session_state["use_sample_resume"] = False
                    st.rerun()

        sample_col1, sample_col2 = st.columns([1, 1])
        with sample_col1:
            if st.button("Load Sample", use_container_width=True):
                st.session_state["resume_text"] = SAMPLE_RESUME_TEXT
                st.session_state["file_name"] = "sample_resume_john_doe.docx"
                st.session_state["use_sample_resume"] = True
                st.rerun()

        with sample_col2:
            if st.session_state.get("use_sample_resume") and uploaded_file is None:
                if st.button("Clear Sample", use_container_width=True):
                    st.session_state["resume_text"] = ""
                    st.session_state["file_name"] = ""
                    st.session_state["use_sample_resume"] = False
                    st.rerun()

        if uploaded_file is not None:
            st.success(f"Attached File: {uploaded_file.name}")
        elif st.session_state.get("use_sample_resume"):
            st.info(f"Loaded Sample Resume: {st.session_state['file_name']}")
        elif not st.session_state.get("resume_text"):
            st.warning("No resume attached. Upload a file or click 'Load Sample'.")

    with col2:
        st.markdown("""
        <div class="card-header-row">
            <span class="card-title-text">2. Target Job Description</span>
        </div>
        <div class="card-subtext">Paste the target job description here</div>
        """, unsafe_allow_html=True)

        job_description_input = st.text_area(
            "Paste the job description here:",
            value=st.session_state.get("job_description_text", ""),
            height=168,
            placeholder="Paste required skills, responsibilities, and qualifications..."
        )
        st.session_state["job_description_text"] = job_description_input

        st.write("<span style='font-size: 12px; font-weight: 600; color: #64748B;'>Load Sample JDs:</span>", unsafe_allow_html=True)
        jd_btn_col1, jd_btn_col2, jd_btn_col3 = st.columns(3)
        with jd_btn_col1:
            if st.button("Python Dev", use_container_width=True):
                st.session_state["job_description_text"] = SAMPLE_JDS["Python Developer"]
                st.rerun()
        with jd_btn_col2:
            if st.button("Data Analyst", use_container_width=True):
                st.session_state["job_description_text"] = SAMPLE_JDS["Data Analyst"]
                st.rerun()
        with jd_btn_col3:
            if st.button("Frontend Dev", use_container_width=True):
                st.session_state["job_description_text"] = SAMPLE_JDS["Frontend Developer"]
                st.rerun()

    st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
    if st.button("Analyze Resume", type="primary", use_container_width=True):
        trigger_analysis()

    # Display Existing Results
    if st.session_state.get("analysis_result"):
        result = st.session_state["analysis_result"]

        st.markdown("<div style='margin-top: 36px; margin-bottom: 16px;'><h3 style='color: #1E293B; font-weight: 800; font-size: 22px; letter-spacing: -0.4px;'>Analysis Results</h3></div>", unsafe_allow_html=True)

        st.markdown(f"""
        <div class="role-banner">
            <div class="role-banner-left">
                <span class="role-banner-label">Detected Job Role</span>
                <span class="role-banner-title">{result['detected_role']}</span>
            </div>
            <div class="overall-score-box">
                <div class="overall-score-number">{result['overall_score']}%</div>
                <div class="overall-score-meta">
                    <span class="overall-score-label">Overall Match</span>
                    <span class="overall-score-sub">50% Req + 20% Pref + 20% TF-IDF + 10% Sections</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        m_col1, m_col2, m_col3, m_col4 = st.columns(4, gap="medium")

        with m_col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-header">
                    <span class="metric-title">Required Skills</span>
                </div>
                <div class="metric-value">{result['required_skill_score']}%</div>
                <div class="metric-bar-bg">
                    <div class="metric-bar-fill" style="width: {min(max(result['required_skill_score'], 0), 100)}%;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with m_col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-header">
                    <span class="metric-title">Preferred Skills</span>
                </div>
                <div class="metric-value">{result['preferred_skill_score']}%</div>
                <div class="metric-bar-bg">
                    <div class="metric-bar-fill-amber" style="width: {min(max(result['preferred_skill_score'], 0), 100)}%;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with m_col3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-header">
                    <span class="metric-title">TF-IDF Similarity</span>
                </div>
                <div class="metric-value">{result['text_similarity']}%</div>
                <div class="metric-bar-bg">
                    <div class="metric-bar-fill-indigo" style="width: {min(max(result['text_similarity'], 0), 100)}%;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with m_col4:
            sec_score = result['section_analysis']['score']
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-header">
                    <span class="metric-title">Section Completeness</span>
                </div>
                <div class="metric-value">{sec_score}%</div>
                <div class="metric-bar-bg">
                    <div class="metric-bar-fill-emerald" style="width: {min(max(sec_score, 0), 100)}%;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        sk_col1, sk_col2, sk_col3 = st.columns(3, gap="medium")

        with sk_col1:
            st.markdown('<div class="result-card">', unsafe_allow_html=True)
            st.markdown('<div class="result-card-title">Matching Skills</div>', unsafe_allow_html=True)
            if result["matching_skills"]:
                chips = "".join([f'<span class="skill-chip chip-match">✓ {s}</span>' for s in result["matching_skills"]])
                st.markdown(f'<div class="chips-container">{chips}</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="empty-notice">No overlapping skills detected.</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with sk_col2:
            st.markdown('<div class="result-card">', unsafe_allow_html=True)
            st.markdown('<div class="result-card-title">Missing Required Skills</div>', unsafe_allow_html=True)
            if result["missing_required_skills"]:
                chips = "".join([f'<span class="skill-chip chip-missing-req">✗ {s}</span>' for s in result["missing_required_skills"]])
                st.markdown(f'<div class="chips-container">{chips}</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="empty-notice">All required skills met!</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with sk_col3:
            st.markdown('<div class="result-card">', unsafe_allow_html=True)
            st.markdown('<div class="result-card-title">Missing Preferred Skills</div>', unsafe_allow_html=True)
            if result["missing_preferred_skills"]:
                chips = "".join([f'<span class="skill-chip chip-missing-pref">★ {s}</span>' for s in result["missing_preferred_skills"]])
                st.markdown(f'<div class="chips-container">{chips}</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="empty-notice">All preferred skills present!</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)


def show_resume_analysis():
    """Renders the Resume Analysis view detailing extracted text, detected skills, and section audit."""
    st.markdown("""
    <div class="dashboard-header">
        <div class="dashboard-title">Resume Analysis</div>
        <div class="dashboard-subtitle">In-depth audit of extracted content, detected competencies, and structural completeness.</div>
    </div>
    """, unsafe_allow_html=True)

    result = st.session_state.get("analysis_result")
    resume_text = st.session_state.get("resume_text", "")
    file_name = st.session_state.get("file_name", "Uploaded Resume")

    if not resume_text:
        st.warning("No resume has been uploaded or loaded yet. Go to the Dashboard to add your resume.")
        return

    word_count = len(resume_text.split())
    char_count = len(resume_text)

    # Top File Info & Completeness Metric
    col_info, col_score = st.columns([2, 1], gap="medium")

    with col_info:
        st.markdown(f"""
        <div class="result-card">
            <div class="result-card-title">Document Metadata</div>
            <div class="eval-row">
                <span class="eval-icon">📄</span>
                <div class="eval-content">
                    <span class="eval-title">File Name</span>
                    <span class="eval-desc">{file_name}</span>
                </div>
            </div>
            <div class="eval-row">
                <span class="eval-icon">📊</span>
                <div class="eval-content">
                    <span class="eval-title">Volume & Extent</span>
                    <span class="eval-desc">{word_count:,} words • {char_count:,} characters</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_score:
        completeness = result["section_analysis"]["score"] if result else 0.0
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-header">
                <span class="metric-title">Resume Completeness Score</span>
            </div>
            <div class="metric-value">{completeness}%</div>
            <div class="metric-bar-bg">
                <div class="metric-bar-fill-emerald" style="width: {min(max(completeness, 0), 100)}%;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Section Completeness Analysis
    st.markdown('<div class="result-card">', unsafe_allow_html=True)
    st.markdown('<div class="result-card-title">Resume Section Presence & Structural Audit</div>', unsafe_allow_html=True)

    if result and "section_analysis" in result:
        checklist_items = ""
        for sec, present in result["section_analysis"]["section_status"].items():
            if present:
                checklist_items += f'<div class="check-item check-pass">✓ {sec} (Detected)</div>'
            else:
                checklist_items += f'<div class="check-item check-missing">✗ {sec} (Not Found)</div>'
        st.markdown(f'<div class="checklist-grid">{checklist_items}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Skills Found in Resume
    st.markdown('<div class="result-card">', unsafe_allow_html=True)
    st.markdown('<div class="result-card-title">All Skills Detected in Resume</div>', unsafe_allow_html=True)
    skills = result["resume_skills"] if result else []
    if skills:
        chips = "".join([f'<span class="skill-chip chip-resume">• {s}</span>' for s in skills])
        st.markdown(f'<div class="chips-container">{chips}</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="empty-notice">No recognized technical skills detected in the current resume.</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Extracted Plain Text Preview
    with st.expander("📄 View Extracted Resume Text", expanded=False):
        st.text_area(
            "Extracted Resume Content",
            value=resume_text,
            height=280,
            disabled=True
        )


def show_job_match():
    """Renders the Job Match assessment view comparing requirements, skills, and qualifications."""
    st.markdown("""
    <div class="dashboard-header">
        <div class="dashboard-title">Job Match Assessment</div>
        <div class="dashboard-subtitle">Target role alignment, competency gap analysis, and requirement comparisons.</div>
    </div>
    """, unsafe_allow_html=True)

    result = st.session_state.get("analysis_result")
    job_desc = st.session_state.get("job_description_text", "")

    if not result:
        st.warning("No analysis has been performed yet. Visit the Dashboard and click 'Analyze Resume'.")
        return

    # Role & Score Banner
    st.markdown(f"""
    <div class="role-banner">
        <div class="role-banner-left">
            <span class="role-banner-label">Detected Job Role</span>
            <span class="role-banner-title">{result['detected_role']}</span>
        </div>
        <div class="overall-score-box">
            <div class="overall-score-number">{result['overall_score']}%</div>
            <div class="overall-score-meta">
                <span class="overall-score-label">Overall Match</span>
                <span class="overall-score-sub">Weighted Evaluation</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 3 Key Scores Row
    col_req, col_pref, col_tfidf = st.columns(3, gap="medium")

    with col_req:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-header">
                <span class="metric-title">Required Skills Match</span>
            </div>
            <div class="metric-value">{result['required_skill_score']}%</div>
            <div class="metric-bar-bg">
                <div class="metric-bar-fill" style="width: {min(max(result['required_skill_score'], 0), 100)}%;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_pref:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-header">
                <span class="metric-title">Preferred Skills Match</span>
            </div>
            <div class="metric-value">{result['preferred_skill_score']}%</div>
            <div class="metric-bar-bg">
                <div class="metric-bar-fill-amber" style="width: {min(max(result['preferred_skill_score'], 0), 100)}%;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_tfidf:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-header">
                <span class="metric-title">TF-IDF Text Similarity</span>
            </div>
            <div class="metric-value">{result['text_similarity']}%</div>
            <div class="metric-bar-bg">
                <div class="metric-bar-fill-indigo" style="width: {min(max(result['text_similarity'], 0), 100)}%;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Skills Comparison Cards
    sk_col1, sk_col2, sk_col3 = st.columns(3, gap="medium")

    with sk_col1:
        st.markdown('<div class="result-card">', unsafe_allow_html=True)
        st.markdown('<div class="result-card-title">Matching Skills</div>', unsafe_allow_html=True)
        if result["matching_skills"]:
            chips = "".join([f'<span class="skill-chip chip-match">✓ {s}</span>' for s in result["matching_skills"]])
            st.markdown(f'<div class="chips-container">{chips}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="empty-notice">No overlapping skills detected.</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with sk_col2:
        st.markdown('<div class="result-card">', unsafe_allow_html=True)
        st.markdown('<div class="result-card-title">Missing Required Skills</div>', unsafe_allow_html=True)
        if result["missing_required_skills"]:
            chips = "".join([f'<span class="skill-chip chip-missing-req">✗ {s}</span>' for s in result["missing_required_skills"]])
            st.markdown(f'<div class="chips-container">{chips}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="empty-notice">All required skills met!</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with sk_col3:
        st.markdown('<div class="result-card">', unsafe_allow_html=True)
        st.markdown('<div class="result-card-title">Missing Preferred Skills</div>', unsafe_allow_html=True)
        if result["missing_preferred_skills"]:
            chips = "".join([f'<span class="skill-chip chip-missing-pref">★ {s}</span>' for s in result["missing_preferred_skills"]])
            st.markdown(f'<div class="chips-container">{chips}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="empty-notice">All preferred skills present!</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Deep Analysis: Experience, Education, Projects
    st.markdown('<div class="result-card">', unsafe_allow_html=True)
    st.markdown('<div class="result-card-title">Role-Specific Qualification Comparison</div>', unsafe_allow_html=True)

    exp_data = result["experience_analysis"]
    edu_data = result["education_analysis"]
    proj_data = result["project_analysis"]

    st.markdown(f"""
    <div class="eval-row">
        <span class="eval-icon">💼</span>
        <div class="eval-content">
            <span class="eval-title">Experience Fit</span>
            <span class="eval-desc">{exp_data['status']}</span>
        </div>
    </div>
    <div class="eval-row">
        <span class="eval-icon">🎓</span>
        <div class="eval-content">
            <span class="eval-title">Education Analysis</span>
            <span class="eval-desc">{edu_data['status']}</span>
        </div>
    </div>
    <div class="eval-row">
        <span class="eval-icon">🛠️</span>
        <div class="eval-content">
            <span class="eval-title">Project Relevance ({proj_data['relevance_level']} Relevance)</span>
            <span class="eval-desc">{proj_data['summary']}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Target Job Description Text Box
    with st.expander("📋 Review Target Job Description", expanded=False):
        st.text_area(
            "Target Role Requirements",
            value=job_desc,
            height=220,
            disabled=True
        )


def show_resume_improvement():
    """Renders actionable recommendations, missing requirements, and improvement tips."""
    st.markdown("""
    <div class="dashboard-header">
        <div class="dashboard-title">Resume Improvement Recommendations</div>
        <div class="dashboard-subtitle">Actionable strategies to optimize your resume for applicant tracking systems (ATS) and target job roles.</div>
    </div>
    """, unsafe_allow_html=True)

    result = st.session_state.get("analysis_result")

    if not result:
        st.warning("No analysis has been run yet. Please go to the Dashboard and click 'Analyze Resume'.")
        return

    # Actionable Recommendations Engine Output
    st.markdown('<div class="result-card">', unsafe_allow_html=True)
    st.markdown(f'<div class="result-card-title">Priority Recommendations for {result["detected_role"]}</div>', unsafe_allow_html=True)

    recs = result.get("recommendations", [])
    if recs:
        for rec in recs:
            st.markdown(f"""
            <div class="eval-row">
                <span class="eval-icon">→</span>
                <div class="eval-content">
                    <span class="eval-title">[{rec['priority']} Priority] {rec['category']}</span>
                    <span class="eval-desc">{rec['message']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown('<div class="empty-notice">No major deficiencies identified. Resume strongly aligns with job requirements.</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Missing Required and Preferred Skills Breakdown
    col_mreq, col_mpref = st.columns(2, gap="medium")

    with col_mreq:
        st.markdown('<div class="result-card">', unsafe_allow_html=True)
        st.markdown('<div class="result-card-title">Missing Required Skills</div>', unsafe_allow_html=True)
        if result["missing_required_skills"]:
            st.markdown("<p style='font-size: 13px; color: #64748B;'>Critical keywords to incorporate into your experience bullets:</p>", unsafe_allow_html=True)
            chips = "".join([f'<span class="skill-chip chip-missing-req">✗ {s}</span>' for s in result["missing_required_skills"]])
            st.markdown(f'<div class="chips-container">{chips}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="empty-notice">None! All mandatory skills are present.</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_mpref:
        st.markdown('<div class="result-card">', unsafe_allow_html=True)
        st.markdown('<div class="result-card-title">Missing Preferred Skills</div>', unsafe_allow_html=True)
        if result["missing_preferred_skills"]:
            st.markdown("<p style='font-size: 13px; color: #64748B;'>Bonus skills that increase candidate competitiveness:</p>", unsafe_allow_html=True)
            chips = "".join([f'<span class="skill-chip chip-missing-pref">★ {s}</span>' for s in result["missing_preferred_skills"]])
            st.markdown(f'<div class="chips-container">{chips}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="empty-notice">None! All preferred competencies are covered.</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Structural Missing Sections
    missing_secs = result["section_analysis"]["missing_sections"]
    if missing_secs:
        st.markdown('<div class="result-card">', unsafe_allow_html=True)
        st.markdown('<div class="result-card-title">Structural Gaps (Missing Sections)</div>', unsafe_allow_html=True)
        st.markdown("<p style='font-size: 13px; color: #64748B;'>Consider adding these sections to improve ATS indexing:</p>", unsafe_allow_html=True)
        sec_chips = "".join([f'<span class="skill-chip chip-missing-req">✗ {sec}</span>' for sec in missing_secs])
        st.markdown(f'<div class="chips-container">{sec_chips}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Best Practice Guides
    col_tip1, col_tip2 = st.columns(2, gap="large")

    with col_tip1:
        st.markdown("""
        <div class="result-card">
            <div class="result-card-title">Experience & Project Enhancement</div>
            <div class="eval-row">
                <span class="eval-icon">★</span>
                <div class="eval-content">
                    <span class="eval-title">The XYZ Accomplishment Formula</span>
                    <span class="eval-desc">"Accomplished [X] as measured by [Y], by doing [Z]". Example: "Decreased build times by 40% by containerizing environments with Docker."</span>
                </div>
            </div>
            <div class="eval-row">
                <span class="eval-icon">★</span>
                <div class="eval-content">
                    <span class="eval-title">Lead with Strong Action Verbs</span>
                    <span class="eval-desc">Use impact verbs: Architected, Orchestrated, Optimized, Automated, Delivered.</span>
                </div>
            </div>
            <div class="eval-row">
                <span class="eval-icon">★</span>
                <div class="eval-content">
                    <span class="eval-title">Ground Every Claim</span>
                    <span class="eval-desc">Never invent fictional experience or metrics. Highlight genuine projects, coursework, or open-source deliverables.</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_tip2:
        st.markdown("""
        <div class="result-card">
            <div class="result-card-title">ATS Compliance Guidelines</div>
            <div class="eval-row">
                <span class="eval-icon">✓</span>
                <div class="eval-content">
                    <span class="eval-title">Single Column Clean Layout</span>
                    <span class="eval-desc">Avoid complex tables, multi-column sidebars, or floating text boxes that break ATS text extraction.</span>
                </div>
            </div>
            <div class="eval-row">
                <span class="eval-icon">✓</span>
                <div class="eval-content">
                    <span class="eval-title">Standard Section Headings</span>
                    <span class="eval-desc">Use standard headers: "Work Experience", "Education", "Technical Skills", "Projects", "Certifications".</span>
                </div>
            </div>
            <div class="eval-row">
                <span class="eval-icon">✓</span>
                <div class="eval-content">
                    <span class="eval-title">Keyword Contextualization</span>
                    <span class="eval-desc">Weave target technologies directly into project descriptions rather than keeping them in an isolated list.</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# Dispatcher: Render Current Selected Page
# -----------------------------------------------------------------------------
if st.session_state["current_page"] == "Dashboard":
    show_dashboard()
elif st.session_state["current_page"] == "Resume Analysis":
    show_resume_analysis()
elif st.session_state["current_page"] == "Job Match":
    show_job_match()
elif st.session_state["current_page"] == "Resume Improvement":
    show_resume_improvement()