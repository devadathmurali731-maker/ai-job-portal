def calculate_ats_score(resume_text, required_skills):
    """
    Calculate a basic ATS score based on skill matching.
    """

    resume_text = resume_text.lower()

    if not required_skills:
        return 0.0

    matched_skills = 0

    for skill in required_skills:
        if skill.lower() in resume_text:
            matched_skills += 1

    score = (
        matched_skills / len(required_skills)
    ) * 100

    return round(score, 2)
