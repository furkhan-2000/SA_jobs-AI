from typing import List
from app.utils import logger

KSA_LOCATION_KEYWORDS = ("saudi", "ksa", "riyadh", "jeddah", "dammam")
REMOTE_KEYWORDS = ("remote", "worldwide", "anywhere", "global")

def filter_ksa_remote(raw_job: dict) -> bool:
    try:
        loc = (raw_job.get("location") or raw_job.get("candidate_required_location") or raw_job.get("jobGeo") or "")
        loc = str(loc).lower()
        if any(k in loc for k in KSA_LOCATION_KEYWORDS):
            return True
        if raw_job.get("remote") is True:
            return True
        if any(k in loc for k in REMOTE_KEYWORDS):
            return True
    except Exception as e:
        logger.exception(f"filter_ksa_remote failed: {e}")
    return False

