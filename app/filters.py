import re
from typing import List

from app.utils import logger


KSA_LOCATION_KEYWORDS = (
    re.compile(r"\bsaudi\b", re.IGNORECASE),
    re.compile(r"\bksa\b", re.IGNORECASE),
    re.compile(r"\briyadh\b", re.IGNORECASE),
    re.compile(r"\bjeddah\b", re.IGNORECASE),
    re.compile(r"\bdammam\b", re.IGNORECASE),
    re.compile(r"\bmecca\b", re.IGNORECASE),
    re.compile(r"\bmedina\b", re.IGNORECASE),
    re.compile(r"\bdhahran\b", re.IGNORECASE),
    re.compile(r"\bkhobar\b", re.IGNORECASE),
    re.compile(r"\btabuk\b", re.IGNORECASE),
    re.compile(r"\babha\b", re.IGNORECASE)
)

REGIONAL_KEYWORDS = (
    re.compile(r"\bgcc\b", re.IGNORECASE),
    re.compile(r"\bmena\b", re.IGNORECASE),
    re.compile(r"\bmiddle\s*east\b", re.IGNORECASE),
    re.compile(r"\barabian\s*gulf\b", re.IGNORECASE),
    re.compile(r"\bgulf\s*region\b", re.IGNORECASE)
)

REMOTE_KEYWORDS = (
    re.compile(r"\bremote\b", re.IGNORECASE),
    re.compile(r"\bworldwide\b", re.IGNORECASE),
    re.compile(r"\banywhere\b", re.IGNORECASE),
    re.compile(r"\bglobal\b", re.IGNORECASE),
    re.compile(r"\bwork\s*from\s*home\b", re.IGNORECASE),
    re.compile(r"\bwfh\b", re.IGNORECASE),
    re.compile(r"\bfully\s*remote\b", re.IGNORECASE),
    re.compile(r"\b100%\s*remote\b", re.IGNORECASE)
)


def _contains_keyword(text: str, keywords: tuple) -> bool:
    """
    Check if text contains any pre-compiled regex keyword.

    Args:
        text: The text to search in
        keywords: Tuple of compiled regex patterns to search for

    Returns:
        True if any pattern matches, False otherwise
    """
    if not text:
        return False

    try:
        return any(pattern.search(text) for pattern in keywords)
    except Exception as e:
        logger.warning(f"Regex matching failed for text '{text[:50]}...': {e}")
        return False


def _extract_job_text_fields(raw_job: dict) -> tuple[str, str, str, str, str]:
    """Helper to safely extract and normalize job text fields."""
    loc_raw = (
        raw_job.get("location")
        or raw_job.get("candidate_required_location")
        or raw_job.get("jobGeo")
        or raw_job.get("jobLocation")
        or ""
    )
    if isinstance(loc_raw, dict):
        loc = (
            loc_raw.get("display_name") or loc_raw.get("name") or loc_raw.get("city") or ""
        )
        if not loc and "area" in loc_raw:
            area = loc_raw.get("area", [])
            if isinstance(area, list) and area:
                loc = " ".join(str(x) for x in area)
        if not loc:
            loc = loc_raw.get("country", "")
    else:
        loc = str(loc_raw)
    loc = loc.lower().strip()

    job_type = str(
        raw_job.get("jobType")
        or raw_job.get("type")
        or raw_job.get("job_type")
        or raw_job.get("employment_type")
        or raw_job.get("workType")
        or ""
    ).lower().strip()

    title = str(
        raw_job.get("title")
        or raw_job.get("jobTitle")
        or raw_job.get("name")
        or ""
    ).lower().strip()

    category = str(
        raw_job.get("category")
        or raw_job.get("jobCategory")
        or raw_job.get("jobIndustry")
        or ""
    ).lower().strip()

    description = str(
        raw_job.get("description")
        or raw_job.get("jobDescription")
        or ""
    ).lower().strip()
    description = description[:500] if description else ""

    return loc, job_type, title, category, description


def is_ksa_on_site_job(raw_job: dict) -> bool:
    """
    Determines if a job is primarily an 'On-site KSA' type.
    A job is considered On-site KSA if it strongly implies a KSA or regional location
    and does NOT strongly imply remote work.
    """
    loc, job_type, title, category, description = _extract_job_text_fields(raw_job)

    is_ksa_located = (_contains_keyword(loc, KSA_LOCATION_KEYWORDS) or
                      _contains_keyword(loc, REGIONAL_KEYWORDS))

    is_explicitly_remote = (
        raw_job.get("remote") is True or
        str(raw_job.get("remote")).lower() == "true" or
        _contains_keyword(loc, REMOTE_KEYWORDS) or
        _contains_keyword(job_type, REMOTE_KEYWORDS) or
        _contains_keyword(title, REMOTE_KEYWORDS) or
        _contains_keyword(description, REMOTE_KEYWORDS)
    )
    
    # It's "On-site KSA" if it's KSA-located AND NOT explicitly remote.
    return is_ksa_located and not is_explicitly_remote


def is_truly_remote_job(raw_job: dict) -> bool:
    """
    Determines if a job is a 'Remote' type.
    A job is considered Remote if it has a remote flag or strongly implies remote work.
    """
    loc, job_type, title, category, description = _extract_job_text_fields(raw_job)

    is_explicitly_remote = (
        raw_job.get("remote") is True or
        str(raw_job.get("remote")).lower() == "true" or
        _contains_keyword(loc, REMOTE_KEYWORDS) or
        _contains_keyword(job_type, REMOTE_KEYWORDS) or
        _contains_keyword(title, REMOTE_KEYWORDS) or
        _contains_keyword(description, REMOTE_KEYWORDS)
    )
    # If it's explicitly remote, classify it as Remote.
    return is_explicitly_remote


def filter_ksa_remote(raw_job: dict) -> bool:
    """
    Filter to show jobs that Saudi residents can apply to:
    1. Jobs located IN Saudi Arabia (on-site, hybrid, etc.)
    2. Jobs in GCC/MENA/Middle East region
    3. Remote jobs that can be done from anywhere (including Saudi Arabia)

    This uses word boundary matching to prevent false positives like:
    - "arkansas" matching "ksa"
    - "not saudi based" matching "saudi"

    Args:
        raw_job: Dictionary containing raw job data from API

    Returns:
        True if job should be shown to Saudi users, False otherwise
    """
    try:
        # A job is relevant if it's either KSA On-site OR Truly Remote
        return is_ksa_on_site_job(raw_job) or is_truly_remote_job(raw_job)

    except Exception:
        logger.exception("filter_ksa_remote failed")
        # Fail safely - reject job if filtering fails
        return False