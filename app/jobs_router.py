from fastapi import APIRouter
from typing import Optional
from app.job_service import fetch_all_jobs
from app.api_clients import fetch_ai_search_results
from app.analytics import compute_analytics
from app.config import settings
from app.utils import logger

router = APIRouter()

@router.get("/")
async def get_jobs(query: Optional[str] = None):
    """
    Fetches jobs, attempting to use an AI search service if a query is provided.
    If AI search fails or is not used, it returns all KSA-relevant jobs,
    allowing the frontend to perform client-side filtering.
    """
    # Always fetch all jobs first, as this is our master list.
    try:
        all_jobs = await fetch_all_jobs()
        job_map = {job['dedup_key']: job for job in all_jobs}
    except Exception as e:
        logger.exception("get_jobs.fetch_all_jobs failed: %s", str(e))
        all_jobs = []
        job_map = {}

    # Attempt AI search if a query is provided
    if query and settings.AI_SERVICE_URL:
        logger.info(f"Initiating AI search with query: '{query}'")
        ai_results = await fetch_ai_search_results(query)

        if ai_results:
            # ASSUMPTION: AI returns a list of 'dedup_key's for the jobs it selected.
            # e.g., {"results": ["remotive-12345", "linkedin-67890"]}
            ai_job_keys = ai_results.get("results", [])
            
            # Filter the master list based on the keys returned by the AI
            filtered_jobs = [job_map[key] for key in ai_job_keys if key in job_map]
            
            logger.info(f"AI search successful. Found {len(filtered_jobs)} matching jobs.")
            stats = compute_analytics(filtered_jobs)
            return {
                "jobs": filtered_jobs,
                "stats": stats,
                "ai_powered": True
            }
        else:
            logger.warning("AI search failed or returned no results. Falling back to normal mode.")
    
    # Fallback case: No query, AI disabled, or AI failed.
    # Return all jobs and let the frontend handle filtering.
    stats = compute_analytics(all_jobs)
    return {
        "jobs": all_jobs,
        "stats": stats,
        "ai_powered": False
    }
