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

def apply_search_filter(jobs: List[dict], keyword: str | None = None) -> List[dict]:
    if not jobs:
        return []
    res = jobs
    if keyword:
        k = keyword.lower()
        res = [j for j in res if k in (j.get("title","")+" "+j.get("company","")+" "+j.get("description","")).lower()]
    return res
