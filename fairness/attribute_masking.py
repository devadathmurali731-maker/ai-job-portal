"""
Personal attribute masking utilities.

Day 15:
Fairness, Normalization & Bias Reduction

Purpose:
Remove or mask non-essential direct identifiers before
downstream candidate evaluation.
"""

from typing import Any, Dict


DEFAULT_MASKED_FIELDS = {
    "name",
    "full_name",
    "candidate_name",
    "email",
    "email_address",
    "phone",
    "phone_number",
    "mobile",
    "mobile_number",
    "address",
    "street_address",
    "home_address",
    "linkedin",
    "linkedin_url",
    "github",
    "github_url",
    "portfolio",
    "portfolio_url",
    "website",
    "website_url",
    "photo",
    "photo_url",
}


def mask_value(value: Any) -> str:
    """
    Replace a sensitive/non-essential value with a standard mask.
    """

    if value is None:
        return ""

    return "[MASKED]"


def mask_personal_attributes(
    resume: Dict[str, Any],
    fields_to_mask=None,
) -> Dict[str, Any]:
    """
    Mask configured non-essential personal attributes.

    The original input dictionary is not modified.
    """

    if not isinstance(resume, dict):
        raise TypeError("resume must be a dictionary.")

    masked_fields = (
        DEFAULT_MASKED_FIELDS
        if fields_to_mask is None
        else set(fields_to_mask)
    )

    result = dict(resume)

    for field in masked_fields:
        if field in result:
            result[field] = mask_value(result[field])

    return result


def get_masked_fields(
    resume: Dict[str, Any],
    fields_to_mask=None,
):
    """
    Return the fields that were present and eligible for masking.
    """

    if not isinstance(resume, dict):
        raise TypeError("resume must be a dictionary.")

    masked_fields = (
        DEFAULT_MASKED_FIELDS
        if fields_to_mask is None
        else set(fields_to_mask)
    )

    return sorted(
        field
        for field in masked_fields
        if field in resume
    )