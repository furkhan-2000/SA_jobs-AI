from typing import List
from app.utils import logger

def filter_ksa_remote(raw_job: dict) -> bool:
    try:
        loc = (raw_job.get("location") or raw_job.get("candidate_required_location") or raw_job.get("jobGeo") or "")
        loc = str(loc).lower()
        if any(k in loc for k in ("saudi", "ksa", "riyadh", "jeddah", "dammam")):
            return True
        if raw_job.get("remote") is True:
            return True
        if "remote" in loc:
            return True
    except Exception as e:
        logger.exception(f"filter_ksa_remote failed: {e}")
    return False

