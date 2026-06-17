import pdfplumber

required_skills = [
    "python",
    "sql",
    "react",
    "fastapi",
    "machine learning",
    "docker",
    "aws"
]

def analyze_resume(file_path):

    try:

        text = ""

        with pdfplumber.open(file_path) as pdf:

            for page in pdf.pages:

                page_text = page.extract_text()

                if page_text:
                    text += page_text.lower()

    except Exception as e:

        return {
            "score": 0,
            "skills_found": [],
            "missing_skills": [],
            "suggestions": [],
            "error": str(e)
        }

    skills_found = []
    score = 0

    for skill in required_skills:

        if skill in text:
            skills_found.append(skill)

    # Skills Score (50)
    score += int(
        (len(skills_found) / len(required_skills)) * 50
    )

    # Education Score (20)
    if "education" in text:
        score += 20

    # Projects Score (15)
    if "project" in text:
        score += 15

    # Experience Score (15)
    if "experience" in text:
        score += 15

    missing_skills = []

    for skill in required_skills:

        if skill not in skills_found:
            missing_skills.append(skill)

    suggestions = []

    for skill in missing_skills:
        suggestions.append(
            f"Add {skill} experience or project"
        )
    print("SKILLS FOUND:", skills_found)
    print("MISSING SKILLS:", missing_skills)
    print("SUGGESTIONS:", suggestions)
    return {
        "score": score,
        "skills_found": skills_found,
        "missing_skills": missing_skills,
        "suggestions": suggestions
    }