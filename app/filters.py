import re
from typing import List
from app.utils import logger

KSA_LOCATION_KEYWORDS = (
    r"\bsaudi\b",
    r"\bksa\b", 
    r"\briyadh\b",
    r"\bjeddah\b",
    r"\bdammam\b",
    r"\bmecca\b",
    r"\bmedina\b",
    r"\bdhahran\b",
    r"\bkhobar\b",
    r"\btabuk\b",
    r"\babha\b"
)

REGIONAL_KEYWORDS = (
    r"\bgcc\b",
    r"\bmena\b",
    r"\bmiddle\s*east\b",
    r"\barabian\s*gulf\b",
    r"\bgulf\s*region\b"
)

REMOTE_KEYWORDS = (
    r"\bremote\b",
    r"\bworldwide\b",
    r"\banywhere\b",
    r"\bglobal\b",
    r"\bwork\s*from\s*home\b",
    r"\bwfh\b",
    r"\bfully\s*remote\b",
    r"\b100%\s*remote\b"
)


def _contains_keyword(text: str, keywords: tuple) -> bool:
    """
    Check if text contains any keyword using regex word boundaries.
    This prevents false positives like "arkansas" matching "ksa".
    
    Args:
        text: The text to search in
        keywords: Tuple of regex patterns to search for
    
    Returns:
        True if any pattern matches, False otherwise
    """
    if not text:
        return False
    
    try:
        return any(re.search(pattern, text, re.IGNORECASE) for pattern in keywords)
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
    
            if any(phrase in description for phrase in [
                "work remotely",
                "remote position",
                "remote role",
                "remote opportunity",
                "100% remote",
                "fully remote",
                "work from anywhere"
            ]):
                return True
        
        return False
        
    except Exception:
        logger.exception("filter_ksa_remote failed")
        # Fail safely - reject job if filtering fails
        return False