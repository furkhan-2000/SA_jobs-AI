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
        loc_raw = (
            raw_job.get("location") or 
            raw_job.get("candidate_required_location") or 
            raw_job.get("jobGeo") or 
            raw_job.get("jobLocation") or
            ""
        )
        
        # Handle structured location objects (e.g., Adzuna returns dict)
        if isinstance(loc_raw, dict):
            # Try multiple possible keys for location
            loc = (
                loc_raw.get("display_name") or 
                loc_raw.get("name") or 
                loc_raw.get("city") or
                ""
            )
            
            # Fallback to area array if main location is empty
            if not loc and "area" in loc_raw:
                area = loc_raw.get("area", [])
                if isinstance(area, list) and area:
                    loc = " ".join(str(x) for x in area)
            
            # Last fallback: country
            if not loc:
                loc = loc_raw.get("country", "")
        else:
            loc = str(loc_raw)
        
        loc = loc.lower().strip()
        
        job_type = str(
            raw_job.get("jobType") or 
            raw_job.get("type") or 
            raw_job.get("job_type") or 
            raw_job.get("employment_type") or
            raw_job.get("workType") or
            ""
        ).lower().strip()
        
        title = str(
            raw_job.get("title") or 
            raw_job.get("jobTitle") or 
            raw_job.get("name") or 
            ""
        ).lower().strip()
        
        category = str(
            raw_job.get("category") or 
            raw_job.get("jobCategory") or
            raw_job.get("jobIndustry") or
            ""
        ).lower().strip()
        
        description = str(
            raw_job.get("description") or 
            raw_job.get("jobDescription") or
            ""
        ).lower().strip()
        
        # Take only first 500 chars of description to avoid performance issues
        description = description[:500] if description else ""
        
        if _contains_keyword(loc, KSA_LOCATION_KEYWORDS):
            return True
        
        if _contains_keyword(loc, REGIONAL_KEYWORDS):
            return True
        
        remote_flag = raw_job.get("remote")
        if remote_flag is True or str(remote_flag).lower() == "true":
            return True
        
        if _contains_keyword(loc, REMOTE_KEYWORDS):
            return True
        
        if _contains_keyword(job_type, REMOTE_KEYWORDS):
            return True
        
        if _contains_keyword(title, REMOTE_KEYWORDS):
            return True
        
        if _contains_keyword(category, REMOTE_KEYWORDS):
            return True
        
        if _contains_keyword(description, REMOTE_KEYWORDS):
            return True
        
        return False
        
    except Exception:
        logger.exception("filter_ksa_remote failed")
        # Fail safely - reject job if filtering fails
        return False