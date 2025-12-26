from typing import List, Dict, Callable, Iterable
from app.api_clients import JobAPIClients
from app.filters import filter_ksa_remote
from app.utils import logger
from app.normalizer import normalize_job
import asyncio
import hashlib
import time # Added import for time module

def _fingerprint(job: Dict) -> str:
    txt = (job.get("title","") or "") + "|" + (job.get("company","") or "") + "|" + (job.get("url","") or "")
    # use SHA256 instead of SHA1
    return hashlib.sha256(txt.encode("utf-8")).hexdigest()

async def _run_client(src_name: str, fn: Callable[[], Iterable[Dict]]) -> List[Dict]:
    try:
        start_time = time.monotonic() # Start timing
        raw = await fn()
        duration = (time.monotonic() - start_time) * 1000 # Calculate duration in ms
        logger.info(f"client {src_name} fetch completed in {duration:.2f} ms") # Log duration

        if not isinstance(raw, list):
            logger.warning(f"client {src_name} returned non-list; ignoring")
            return []
        kept = []
        for item in raw:
            try:
                if filter_ksa_remote(item):
                    kept.append(normalize_job(item, src_name))
            except Exception as e:
                logger.exception(f"Normalization error for {src_name} item: {e}")
        logger.info(f"client {src_name} processed {len(raw)} raw jobs, {len(kept)} jobs kept after filtering and normalization.")
        return kept
    except Exception as e:
        logger.exception(f"Error fetching or processing jobs for client {src_name}: {e}")
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
        
    # Add 'dedup_key' to each job and then deduplicate
    unique_jobs = {}
    for job in flattened:
        # The fingerprint serves as our unique identifier or "dedup_key"
        key = _fingerprint(job)
        if key not in unique_jobs:
            job['dedup_key'] = key  # Store the key in the job dictionary
            unique_jobs[key] = job
            
    logger.info(f"fetch_all_jobs: unique_count={len(unique_jobs)}")
    return list(unique_jobs.values())
