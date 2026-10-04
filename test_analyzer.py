from analyzer import analyze_resume


resume = """
I am a Python developer with experience in Python,
SQL, Git, HTML and CSS.
"""


job_description = """
We are looking for a developer with Python,
SQL, Git and Machine Learning skills.
"""


result = analyze_resume(resume, job_description)


print("Resume Skills:")
print(result["resume_skills"])

print("\nRequired Skills:")
print(result["job_skills"])

print("\nMatching Skills:")
print(result["matching_skills"])

print("\nMissing Skills:")
print(result["missing_skills"])

print("\nMatch Score:")
print(result["match_score"], "%")