def screen_candidate(ats_score, minimum_score=60):
    """
    Determine whether a candidate passes
    the initial screening stage.
    """

    if ats_score >= minimum_score:
        return "SHORTLISTED"

    return "REJECTED"
