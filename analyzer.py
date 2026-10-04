import json
import os
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# ---------------------------------------------------------------------------
# Skill Aliases & Canonical Mapping
# ---------------------------------------------------------------------------
SKILL_ALIASES = {
    "scikit-learn": ["scikit-learn", "scikit learn", "sklearn", "scikitlearn"],
    "machine learning": ["machine learning", "ml"],
    "deep learning": ["deep learning", "dl", "neural networks"],
    "power bi": ["power bi", "powerbi", "power-bi"],
    "tableau": ["tableau"],
    "excel": ["excel", "ms excel", "microsoft excel", "spreadsheets"],
    "node.js": ["node.js", "nodejs", "node js"],
    "react": ["react", "react.js", "reactjs"],
    "angular": ["angular", "angular.js", "angularjs"],
    "vue": ["vue", "vue.js", "vuejs"],
    "next.js": ["next.js", "nextjs"],
    "c++": ["c++", "cpp", "c plus plus"],
    "c#": ["c#", "csharp", "c sharp", ".net"],
    "sql": ["sql", "structured query language"],
    "mysql": ["mysql"],
    "postgresql": ["postgresql", "postgres"],
    "mongodb": ["mongodb", "mongo"],
    "rest api": ["rest api", "rest apis", "restful api", "restful apis", "rest web services", "restful"],
    "ui/ux": ["ui/ux", "ui ux", "ux/ui", "user interface", "user experience"],
    "ci/cd": ["ci/cd", "ci cd", "continuous integration", "continuous deployment"],
    "docker": ["docker", "containerization", "containers"],
    "kubernetes": ["kubernetes", "k8s"],
    "oop": ["oop", "object-oriented programming", "object oriented programming", "oops"],
    "data structures": ["data structures", "dsa"],
    "algorithms": ["algorithms"],
    "data analysis": ["data analysis", "data analytics"],
    "data visualization": ["data visualization", "data viz"],
    "fastapi": ["fastapi", "fast api"],
    "spring boot": ["spring boot", "springboot"],
    "tailwind css": ["tailwind css", "tailwind"],
    "stored procedures": ["stored procedures", "stored procedure", "stored procs"],
    "database design": ["database design", "database modeling", "schema design"],
    "project management": ["project management", "pmp", "scrum master"],
    "risk management": ["risk management"],
    "wireframing": ["wireframing", "wireframes"],
    "prototyping": ["prototyping", "prototypes"],
    "user research": ["user research", "usability testing"],
    "unit testing": ["unit testing", "pytest", "junit", "tdd"]
}


# ---------------------------------------------------------------------------
# Data Loaders
# ---------------------------------------------------------------------------
def load_skills():
    """Loads all skills from data/skills.json."""
    file_path = os.path.join(os.path.dirname(__file__), "data", "skills.json")
    if not os.path.exists(file_path):
        return []

    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    skills = []
    for category in data.values():
        skills.extend(category)

    # Return unique skills preserving order
    return list(dict.fromkeys(skills))


def load_job_roles():
    """Loads job role configurations from data/job_roles.json."""
    file_path = os.path.join(os.path.dirname(__file__), "data", "job_roles.json")
    if not os.path.exists(file_path):
        return {}

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


# ---------------------------------------------------------------------------
# Robust Skill Matcher
# ---------------------------------------------------------------------------
def check_skill_match(skill_name, text):
    """
    Checks if skill_name or its aliases exist in text using word boundaries.
    Avoids false positives for short acronyms like 'C' or 'R'.
    """
    if not skill_name or not text:
        return False

    norm_skill = skill_name.lower().strip()
    aliases = SKILL_ALIASES.get(norm_skill, [norm_skill])

    for alias in aliases:
        # Special handling for single-letter programming languages
        if alias == "c":
            if re.search(r"(?:^|[\s,/])C(?:[\s,/]|programming|language|\b)", text, re.IGNORECASE):
                if re.search(r"\b(C\s*[,/]\s*C\+\+|C\s+programming|C\s+language|ANSI\s+C)\b", text, re.IGNORECASE) or re.search(r"(?:Python|Java|SQL|C\+\+)\s*,\s*C\b", text):
                    return True
        elif alias == "r":
            if re.search(r"\b(R\s+programming|R\s+language|Python\s+and\s+R|Python\s*,\s*R|R\s*,\s*Python|R\s+scripting)\b", text, re.IGNORECASE):
                return True
        elif alias in ["c++", "c#"]:
            escaped = re.escape(alias)
            if re.search(r"(?:\b|^)" + escaped + r"(?:\b|\s|$|[,\.;])", text, re.IGNORECASE):
                return True
        else:
            escaped = re.escape(alias)
            escaped = escaped.replace(r"\ ", r"[\s\-]")
            pattern = r"\b" + escaped + r"\b"
            if re.search(pattern, text, re.IGNORECASE):
                return True

    return False


def extract_skills(text):
    """Extracts all recognized skills from the given text."""
    if not text:
        return []

    skills = load_skills()
    found_skills = []

    for skill in skills:
        if check_skill_match(skill, text):
            found_skills.append(skill)

    return list(dict.fromkeys(found_skills))


# ---------------------------------------------------------------------------
# 1. Job Role Detection
# ---------------------------------------------------------------------------
def detect_job_role(job_description):
    """
    Detects the likely job role from the job description.
    Supports 16 roles. Returns 'General / Other' if no confident signal is detected.
    """
    if not job_description or not job_description.strip():
        return "General / Other"

    job_roles = load_job_roles()
    if not job_roles:
        return "General / Other"

    text_lower = job_description.lower()
    lines = [line.strip() for line in job_description.strip().split("\n") if line.strip()]
    first_few_lines = "\n".join(lines[:6]).lower()

    role_scores = {}

    for role_name, config in job_roles.items():
        score = 0
        aliases = config.get("aliases", []) + [role_name.lower()]

        for alias in aliases:
            alias_pattern = r"\b" + re.escape(alias) + r"\b"

            # Strong bonus if mentioned in title or first lines
            if re.search(alias_pattern, first_few_lines):
                score += 8.0
            elif re.search(alias_pattern, text_lower):
                score += 4.0

        # Correlation with role required skills
        req_skills = config.get("required_skills", [])
        for skill in req_skills:
            if check_skill_match(skill, text_lower):
                score += 1.5

        # Correlation with role preferred skills
        pref_skills = config.get("preferred_skills", [])
        for skill in pref_skills:
            if check_skill_match(skill, text_lower):
                score += 0.5

        role_scores[role_name] = score

    best_role, best_score = max(role_scores.items(), key=lambda item: item[1])

    # Confident threshold: at least a strong title or multiple skill hits
    if best_score >= 5.0:
        return best_role
    return "General / Other"


# ---------------------------------------------------------------------------
# 3. Job Description Extraction (Required vs Preferred)
# ---------------------------------------------------------------------------
def extract_jd_requirements(job_description, detected_role):
    """
    Extracts required and preferred skills from the actual job description.
    Actual JD text takes precedence over generic role definitions.
    """
    job_roles = load_job_roles()
    role_config = job_roles.get(detected_role, {})

    all_jd_skills = extract_skills(job_description)

    # Split text into required vs preferred zones if headings exist
    req_text = ""
    pref_text = ""
    current_mode = "general"

    for line in job_description.split("\n"):
        l_lower = line.lower().strip()
        if re.search(r"\b(preferred|nice to have|desired|bonus|plus|good to have)\b", l_lower):
            current_mode = "preferred"
        elif re.search(r"\b(required|must have|minimum qualifications|qualifications|requirements|essential|core skills)\b", l_lower):
            current_mode = "required"

        if current_mode == "required":
            req_text += line + "\n"
        elif current_mode == "preferred":
            pref_text += line + "\n"

    explicit_req_skills = extract_skills(req_text)
    explicit_pref_skills = extract_skills(pref_text)

    role_required = role_config.get("required_skills", [])
    role_preferred = role_config.get("preferred_skills", [])

    required_skills = []
    preferred_skills = []

    # 1. Skills explicitly under required headings
    for skill in explicit_req_skills:
        if skill not in required_skills:
            required_skills.append(skill)

    # 2. Skills matching role's required definition present in JD
    for skill in all_jd_skills:
        if skill in role_required and skill not in required_skills:
            required_skills.append(skill)

    # 3. Skills explicitly under preferred headings
    for skill in explicit_pref_skills:
        if skill not in required_skills and skill not in preferred_skills:
            preferred_skills.append(skill)

    # 4. Skills matching role's preferred definition present in JD
    for skill in all_jd_skills:
        if skill in role_preferred and skill not in required_skills and skill not in preferred_skills:
            preferred_skills.append(skill)

    # 5. Fallback for remaining skills found in JD
    for skill in all_jd_skills:
        if skill not in required_skills and skill not in preferred_skills:
            # Check if mentioned with "must" / "require" in surrounding text
            pattern_must = r"(?:must|require[ds]?|essential|proficiency in|experience in)\s+[^.\n]*?\b" + re.escape(skill) + r"\b"
            if re.search(pattern_must, job_description, re.IGNORECASE):
                required_skills.append(skill)
            else:
                preferred_skills.append(skill)

    # If no required skills were segregated, default all to required
    if not required_skills and preferred_skills:
        required_skills = preferred_skills
        preferred_skills = []

    # If role has default required skills, and none matched, add role defaults
    if not required_skills and role_required:
        required_skills = role_required[:4]

    return required_skills, preferred_skills


# ---------------------------------------------------------------------------
# 6. Resume Section Analysis
# ---------------------------------------------------------------------------
def analyze_sections(resume_text):
    """
    Checks whether key resume sections exist based on textual evidence.
    Returns detected sections, missing sections, and completeness score.
    """
    if not resume_text:
        return {
            "score": 0.0,
            "detected_sections": [],
            "missing_sections": ["Contact Information", "Summary/Profile", "Education", "Technical Skills", "Work Experience", "Projects", "Certifications", "Achievements"],
            "section_status": {}
        }

    sections_evidence = {
        "Contact Information": bool(
            re.search(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", resume_text) or
            re.search(r"(?:\+?\d{1,3}[\s-]?)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}", resume_text) or
            re.search(r"\b(linkedin\.com|github\.com)\b", resume_text, re.IGNORECASE)
        ),
        "Summary/Profile": bool(
            re.search(r"\b(summary|professional summary|executive summary|profile|about me|objective)\b", resume_text, re.IGNORECASE)
        ),
        "Education": bool(
            re.search(r"\b(education|academic|academics|degree|bachelor|master|b\.s\.|b\.tech|m\.s\.|phd|university|college|gpa)\b", resume_text, re.IGNORECASE)
        ),
        "Technical Skills": bool(
            re.search(r"\b(skills|technical skills|technologies|proficiencies|core competencies|tools)\b", resume_text, re.IGNORECASE)
        ),
        "Work Experience": bool(
            re.search(r"\b(experience|work experience|employment|work history|professional experience|internship)\b", resume_text, re.IGNORECASE)
        ),
        "Projects": bool(
            re.search(r"\b(projects|key projects|academic projects|personal projects|portfolio)\b", resume_text, re.IGNORECASE)
        ),
        "Certifications": bool(
            re.search(r"\b(certifications|certificates|certified|credentials|licenses)\b", resume_text, re.IGNORECASE)
        ),
        "Achievements": bool(
            re.search(r"\b(achievements|awards|honors|accomplishments|publications)\b", resume_text, re.IGNORECASE)
        )
    }

    # Section weights (core sections weighted higher)
    weights = {
        "Contact Information": 15,
        "Technical Skills": 20,
        "Work Experience": 25,
        "Education": 15,
        "Projects": 15,
        "Summary/Profile": 5,
        "Certifications": 2.5,
        "Achievements": 2.5
    }

    detected = [sec for sec, exists in sections_evidence.items() if exists]
    missing = [sec for sec, exists in sections_evidence.items() if not exists]

    score = sum(weights[sec] for sec in detected)

    return {
        "score": round(score, 1),
        "detected_sections": detected,
        "missing_sections": missing,
        "section_status": sections_evidence
    }


# ---------------------------------------------------------------------------
# 7. Experience Analysis
# ---------------------------------------------------------------------------
def analyze_experience(resume_text, job_description):
    """
    Extracts experience metrics from resume and compares with job description.
    Never invents years of experience.
    """
    if not resume_text:
        return {
            "status": "Experience evidence not found",
            "resume_years": None,
            "required_years": None,
            "has_internship": False,
            "has_work_experience": False,
            "experience_details": "No resume text provided."
        }

    # Detect explicit years of experience in resume (e.g. "5+ years of experience")
    resume_years_matches = re.findall(
        r"(\d+)\+?\s*(?:years?|yrs?)(?:\s+of)?\s+(?:professional\s+|relevant\s+|work\s+)?experience",
        resume_text,
        re.IGNORECASE
    )
    explicit_resume_years = max([int(y) for y in resume_years_matches]) if resume_years_matches else None

    # Detect year date ranges (e.g. 2019 - 2023 or 2021 - Present)
    date_ranges = re.findall(r"\b(20\d{2})\s*[-–to]+\s*(20\d{2}|present|current)\b", resume_text, re.IGNORECASE)
    estimated_range_years = 0
    if date_ranges:
        for start, end in date_ranges:
            start_yr = int(start)
            end_yr = 2026 if end.lower() in ["present", "current"] else int(end)
            diff = max(end_yr - start_yr, 1)
            estimated_range_years += diff

    resume_years = explicit_resume_years if explicit_resume_years is not None else (estimated_range_years if estimated_range_years > 0 else None)

    # Detect required years in JD (e.g. "3+ years")
    jd_years_matches = re.findall(
        r"(\d+)\+?\s*(?:years?|yrs?)(?:\s+of)?\s+(?:professional\s+|relevant\s+|backend\s+|engineering\s+|work\s+)?experience",
        job_description,
        re.IGNORECASE
    )
    required_years = max([int(y) for y in jd_years_matches]) if jd_years_matches else None

    has_internship = bool(re.search(r"\b(intern|internship|trainee|apprentice)\b", resume_text, re.IGNORECASE))
    has_work_exp = bool(re.search(r"\b(software engineer|developer|analyst|engineer|consultant|manager|specialist|lead|architect)\b", resume_text, re.IGNORECASE))

    # Determine status
    if required_years is not None:
        if resume_years is not None:
            if resume_years >= required_years:
                status = f"Meets experience requirement (~{resume_years} yrs found vs {required_years}+ yrs required)"
            else:
                status = f"Partially meets experience (~{resume_years} yrs found vs {required_years}+ yrs required)"
        elif has_internship or has_work_exp:
            status = f"Work experience present, but explicit {required_years}+ years duration not specified"
        else:
            status = "Experience evidence not found"
    else:
        if resume_years is not None:
            status = f"Detected ~{resume_years} years of relevant experience"
        elif has_work_exp or has_internship:
            status = "Professional experience detected (duration unquantified)"
        else:
            status = "Experience evidence not found"

    return {
        "status": status,
        "resume_years": resume_years,
        "required_years": required_years,
        "has_internship": has_internship,
        "has_work_experience": has_work_exp
    }


# ---------------------------------------------------------------------------
# 8. Project Analysis
# ---------------------------------------------------------------------------
def analyze_projects(resume_text, detected_role):
    """
    Identifies projects in resume and checks relevance to detected job role.
    """
    if not resume_text:
        return {
            "has_projects": False,
            "relevance_level": "None",
            "matched_keywords": [],
            "summary": "No project section or details detected."
        }

    has_projects = bool(re.search(r"\b(projects?|key projects|academic projects|portfolio)\b", resume_text, re.IGNORECASE))

    job_roles = load_job_roles()
    role_config = job_roles.get(detected_role, {})
    project_keywords = role_config.get("project_keywords", [])

    matched_keywords = []
    text_lower = resume_text.lower()

    for kw in project_keywords:
        if re.search(r"\b" + re.escape(kw.lower()) + r"\b", text_lower):
            matched_keywords.append(kw)

    if not has_projects and not matched_keywords:
        return {
            "has_projects": False,
            "relevance_level": "None",
            "matched_keywords": [],
            "summary": "No project section or project descriptions identified."
        }

    if len(matched_keywords) >= 2:
        relevance_level = "High"
        summary = f"Projects closely align with {detected_role} ({', '.join(matched_keywords[:4])})."
    elif len(matched_keywords) == 1:
        relevance_level = "Moderate"
        summary = f"Relevant project focus detected ({matched_keywords[0]})."
    else:
        relevance_level = "General"
        summary = "Projects detected, but they appear generalized rather than role-specialized."

    return {
        "has_projects": has_projects,
        "relevance_level": relevance_level,
        "matched_keywords": matched_keywords,
        "summary": summary
    }


# ---------------------------------------------------------------------------
# 9. Education Analysis
# ---------------------------------------------------------------------------
def analyze_education(resume_text, job_description):
    """
    Extracts education qualifications from resume and compares with job description.
    """
    if not resume_text:
        return {
            "status": "Education evidence not found",
            "detected_degree": None,
            "detected_field": None
        }

    # Extract degree level
    degrees = []
    if re.search(r"\b(ph\.?d|doctorate)\b", resume_text, re.IGNORECASE):
        degrees.append("Ph.D.")
    if re.search(r"\b(master'?s?|m\.?s\.?|m\.?tech|m\.?b\.?a)\b", resume_text, re.IGNORECASE):
        degrees.append("Master's")
    if re.search(r"\b(bachelor'?s?|b\.?s\.?|b\.?tech|b\.?e\.?|b\.?sc)\b", resume_text, re.IGNORECASE):
        degrees.append("Bachelor's")

    detected_degree = degrees[0] if degrees else None

    # Extract major / field of study
    fields = []
    field_patterns = [
        "Computer Science", "Information Technology", "Software Engineering",
        "Data Science", "Electrical Engineering", "Mathematics", "Statistics",
        "Business Analytics", "Information Systems", "Economics"
    ]
    for fp in field_patterns:
        if re.search(r"\b" + re.escape(fp) + r"\b", resume_text, re.IGNORECASE):
            fields.append(fp)
            break

    detected_field = fields[0] if fields else None

    # Check JD requirements
    jd_requires_degree = bool(re.search(r"\b(bachelor'?s?|master'?s?|degree in|b\.s|m\.s)\b", job_description, re.IGNORECASE))

    if detected_degree:
        field_str = f" in {detected_field}" if detected_field else ""
        if jd_requires_degree:
            status = f"Meets degree requirement: {detected_degree}{field_str}"
        else:
            status = f"Degree verified: {detected_degree}{field_str}"
    else:
        if jd_requires_degree:
            status = "Degree required by role, but explicit degree not verified in resume"
        else:
            status = "Education details unquantified / not found"

    return {
        "status": status,
        "detected_degree": detected_degree,
        "detected_field": detected_field
    }


# ---------------------------------------------------------------------------
# 10. Enhanced TF-IDF Cosine Similarity
# ---------------------------------------------------------------------------
def clean_for_tfidf(text):
    """Cleans text to focus on meaningful professional terms and eliminate boilerplate."""
    if not text:
        return ""

    # Remove emails, URLs, phone numbers
    text = re.sub(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", " ", text)
    text = re.sub(r"https?://\S+|www\.\S+", " ", text)
    text = re.sub(r"(?:\+?\d{1,3}[\s-]?)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}", " ", text)

    # Remove common non-technical resume boilerplate words
    boilerplate = [
        "resume", "curriculum", "vitae", "contact", "email", "phone", "address",
        "references", "available", "upon", "request", "page"
    ]
    words = text.split()
    filtered = [w for w in words if w.lower() not in boilerplate]

    return " ".join(filtered)


def calculate_text_similarity(resume_text, job_description):
    """
    Calculates TF-IDF cosine similarity between resume and job description.
    Uses n-grams and stop words to prioritize relevant terminology.
    """
    if not resume_text or not job_description:
        return 0.0

    clean_resume = clean_for_tfidf(resume_text)
    clean_jd = clean_for_tfidf(job_description)

    if not clean_resume.strip() or not clean_jd.strip():
        return 0.0

    try:
        vectorizer = TfidfVectorizer(
            stop_words="english",
            ngram_range=(1, 2),
            max_features=1500
        )
        tfidf_matrix = vectorizer.fit_transform([clean_resume, clean_jd])
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        return round(float(similarity) * 100, 2)
    except Exception:
        return 0.0


# ---------------------------------------------------------------------------
# Actionable Recommendations Engine
# ---------------------------------------------------------------------------
def generate_recommendations(missing_required, missing_preferred, exp_analysis, edu_analysis, section_analysis, detected_role):
    """Generates specific, role-tailored recommendations for resume enhancement."""
    recs = []

    # 1. Missing Required Skills
    if missing_required:
        top_req = missing_required[:3]
        recs.append({
            "priority": "High",
            "category": "Core Competencies",
            "message": f"Add project or coursework evidence for essential {detected_role} skills: {', '.join(top_req)}."
        })

    # 2. Missing Preferred Skills
    if missing_preferred:
        top_pref = missing_preferred[:3]
        recs.append({
            "priority": "Medium",
            "category": "Bonus Competencies",
            "message": f"Enhance competitiveness by mentioning preferred tools: {', '.join(top_pref)}."
        })

    # 3. Missing Sections
    missing_secs = section_analysis.get("missing_sections", [])
    if "Projects" in missing_secs:
        recs.append({
            "priority": "High",
            "category": "Structure",
            "message": f"Create a dedicated 'Projects' section highlighting real-world {detected_role} deliverables."
        })
    if "Certifications" in missing_secs:
        recs.append({
            "priority": "Low",
            "category": "Credentials",
            "message": f"Include recognized certifications relevant to {detected_role} (e.g. cloud or database credentials)."
        })

    # 4. Experience Gaps
    if "Partially meets" in exp_analysis.get("status", "") or exp_analysis.get("status") == "Experience evidence not found":
        recs.append({
            "priority": "Medium",
            "category": "Experience",
            "message": "Explicitly state your years of professional or internship experience and dates in the work experience section."
        })

    # 5. Fallback positive recommendation
    if not recs:
        recs.append({
            "priority": "Info",
            "category": "Optimization",
            "message": f"Excellent alignment with the {detected_role} profile. Tailor bullet points to quantify performance impact."
        })

    return recs


# ---------------------------------------------------------------------------
# 11. Main Analysis Function
# ---------------------------------------------------------------------------
def analyze_resume(resume_text, job_description):
    """
    Performs comprehensive job-specific resume analysis:
    - Job role detection
    - Required & preferred skill extraction from actual JD
    - Robust skill matching
    - Transparent weighted scoring
    - Resume section completeness
    - Experience & project relevance analysis
    - TF-IDF content similarity
    - Tailored recommendations
    """
    # 1. Job Role Detection
    detected_role = detect_job_role(job_description)

    # 2. Extract Skills from Resume
    resume_skills = extract_skills(resume_text)

    # 3. Extract Required & Preferred Skills from JD
    required_skills, preferred_skills = extract_jd_requirements(job_description, detected_role)

    # 4. Skill Matching
    matching_skills = [
        skill for skill in resume_skills
        if skill.lower() in [s.lower() for s in (required_skills + preferred_skills)]
    ]

    matching_required = [
        skill for skill in required_skills
        if skill.lower() in [s.lower() for s in resume_skills]
    ]

    missing_required_skills = [
        skill for skill in required_skills
        if skill.lower() not in [s.lower() for s in resume_skills]
    ]

    matching_preferred = [
        skill for skill in preferred_skills
        if skill.lower() in [s.lower() for s in resume_skills]
    ]

    missing_preferred_skills = [
        skill for skill in preferred_skills
        if skill.lower() not in [s.lower() for s in resume_skills]
    ]

    # 5. Scores Calculation
    if len(required_skills) > 0:
        required_skill_score = round((len(matching_required) / len(required_skills)) * 100, 2)
    else:
        required_skill_score = 100.0 if len(resume_skills) > 0 else 0.0

    if len(preferred_skills) > 0:
        preferred_skill_score = round((len(matching_preferred) / len(preferred_skills)) * 100, 2)
    else:
        preferred_skill_score = required_skill_score  # Fallback gracefully if no preferred skills defined

    # 6. Content Similarity (TF-IDF)
    text_similarity = calculate_text_similarity(resume_text, job_description)

    # 7. Section Completeness Analysis
    section_analysis = analyze_sections(resume_text)
    section_score = section_analysis["score"]

    # 8. Experience, Education & Project Analysis
    experience_analysis = analyze_experience(resume_text, job_description)
    education_analysis = analyze_education(resume_text, job_description)
    project_analysis = analyze_projects(resume_text, detected_role)

    # 9. Weighted Overall Score Calculation
    # Formula:
    #   50% Required Skill Match
    # + 20% Preferred Skill Match
    # + 20% TF-IDF Job Similarity
    # + 10% Resume Section Completeness
    overall_score = (
        0.50 * required_skill_score +
        0.20 * preferred_skill_score +
        0.20 * text_similarity +
        0.10 * section_score
    )
    overall_score = round(min(max(overall_score, 0.0), 100.0), 2)

    # 10. Recommendations
    recommendations = generate_recommendations(
        missing_required_skills,
        missing_preferred_skills,
        experience_analysis,
        education_analysis,
        section_analysis,
        detected_role
    )

    all_job_skills = list(dict.fromkeys(required_skills + preferred_skills))
    all_missing = list(dict.fromkeys(missing_required_skills + missing_preferred_skills))

    return {
        "detected_role": detected_role,
        "overall_score": overall_score,
        "required_skill_score": required_skill_score,
        "preferred_skill_score": preferred_skill_score,
        "text_similarity": text_similarity,
        "resume_skills": resume_skills,
        "required_skills": required_skills,
        "preferred_skills": preferred_skills,
        "matching_skills": matching_skills,
        "missing_required_skills": missing_required_skills,
        "missing_preferred_skills": missing_preferred_skills,
        "experience_analysis": experience_analysis,
        "education_analysis": education_analysis,
        "project_analysis": project_analysis,
        "section_analysis": section_analysis,
        "recommendations": recommendations,
        # Backward compatibility aliases
        "match_score": overall_score,
        "job_skills": all_job_skills,
        "missing_skills": all_missing
    }