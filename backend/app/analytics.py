from collections import Counter
from typing import List, Dict

def compute_analytics(jobs: List[Dict]) -> Dict:
    total = len(jobs)
    per_company = Counter([j.get("company","Unknown") or "Unknown" for j in jobs])
    per_type = Counter([j.get("jobType","Unknown") or "Unknown" for j in jobs])
    per_location = Counter([j.get("location","Unknown") or "Unknown" for j in jobs])
    return {
        "total_jobs": total,
        "jobs_per_company": dict(per_company.most_common(50)),
        "jobs_per_type": dict(per_type.most_common(50)),
        "jobs_per_location": dict(per_location.most_common(50))
    }
