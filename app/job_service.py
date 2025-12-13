import hashlib
from typing import List, Dict, Callable, Iterable
from app.api_clients import JobAPIClients
from app.filters import filter_ksa_remote
from app.utils import logger
import asyncio

def _fingerprint(job: Dict) -> str:
    txt = (job.get("title","") or "") + "|" + (job.get("company","") or "") + "|" + (job.get("url","") or "")
    # use SHA256 instead of SHA1
    return hashlib.sha256(txt.encode("utf-8")).hexdigest()

def _normalize(raw: Dict, source: str) -> Dict:
    title = raw.get("title") or raw.get("jobTitle") or raw.get("name") or ""
    company = raw.get("company") or raw.get("company_name") or raw.get("companyName") or ""
    url = raw.get("url") or raw.get("jobUrl") or raw.get("link") or raw.get("apply_url") or ""
    description = raw.get("description") or raw.get("jobDescription") or ""
    job_type = raw.get("type") or raw.get("jobType") or raw.get("job_type") or ""
    industry = raw.get("industry") or raw.get("jobIndustry") or ""
    location = raw.get("location") or raw.get("jobGeo") or raw.get("candidate_required_location") or ""
    remote = raw.get("remote") if isinstance(raw.get("remote"), bool) else ("remote" in str(location).lower())
    pub_date = raw.get("pubDate") or raw.get("publication_date") or raw.get("date") or None
    return {
        "source": source,
        "title": str(title).strip(),
        "company": str(company).strip(),
        "url": str(url).strip(),
        "description": str(description).strip(),
        "jobType": str(job_type).strip(),
        "jobIndustry": str(industry).strip(),
        "location": str(location).strip(),
        "remote": bool(remote),
        "pubDate": pub_date
    }

async def _run_client(src_name: str, fn: Callable[[], Iterable[Dict]]) -> List[Dict]:
    try:
        raw = await fn()
        if not isinstance(raw, list):
            logger.warning(f"client {src_name} returned non-list; ignoring")
            return []
        kept = []
        for item in raw:
            try:
                if filter_ksa_remote(item):
                    kept.append(_normalize(item, src_name))
            except Exception as e:
                logger.exception(f"Normalization error for {src_name}: {e}")
        logger.info(f"client {src_name} -> raw={len(raw)} kept={len(kept)}")
        return kept
    except Exception as e:
        logger.exception(f"client {src_name} failed: {e}")
        return []

async def fetch_all_jobs() -> List[Dict]:
    clients = [
        ("arbeitnow", JobAPIClients.fetch_arbeitnow),
        ("jobicy", JobAPIClients.fetch_jobicy),
        ("remotive", JobAPIClients.fetch_remotive),
        ("adzuna", JobAPIClients.fetch_adzuna),
        ("jooble", JobAPIClients.fetch_jooble),
        ("careerjet", JobAPIClients.fetch_careerjet),
        ("openwebninja", JobAPIClients.fetch_openweb_ninja)
    ]
    tasks = [_run_client(name, fn) for name, fn in clients]
    results = await asyncio.gather(*tasks, return_exceptions=False)
    flattened: List[Dict] = []
    for r in results:
        flattened.extend(r)
    # dedupe by SHA256 fingerprint
    unique = {}
    for job in flattened:
        key = _fingerprint(job)
        if key not in unique:
            unique[key] = job
    logger.info(f"fetch_all_jobs: unique_count={len(unique)}")
    return list(unique.values())
