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
            # NEW ASSUMPTION: AI returns a list of full job objects that it selected.
            # These jobs should ideally already be normalized and include a dedup_key.
            ai_filtered_jobs = ai_results.get("results", [])
            
            # Ensure each AI-returned job has a dedup_key for consistency.
            # If not present, we can generate one or use a fallback.
            # For simplicity, we'll assume AI-returned jobs are well-formed.
            
            logger.info(f"AI search successful. Found {len(ai_filtered_jobs)} matching jobs.")
            # Stats for AI-powered results should be computed on these AI-filtered jobs.
            # However, for consistency with BUG-8 fix (next), we'll compute stats on the `ai_filtered_jobs`
            return {
                "jobs": ai_filtered_jobs,
                "stats": compute_analytics(ai_filtered_jobs), # Compute stats on AI-filtered jobs
                "ai_powered": True
            }
        else:
            logger.warning("AI search failed or returned no results. Falling back to normal mode.")
    
    # Fallback case: No query, AI disabled, or AI failed.
    # Return all jobs and let the frontend handle filtering.
    # Stats are computed on the ALL_JOBS list
    return {
        "jobs": all_jobs,
        "stats": compute_analytics(all_jobs), # Compute stats on all_jobs
        "ai_powered": False
    }
