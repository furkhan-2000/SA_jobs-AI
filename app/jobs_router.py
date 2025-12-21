from fastapi import APIRouter, Query
from app.job_service import fetch_all_jobs
from app.filters import apply_search_filter
from app.analytics import compute_analytics
from app.config import settings
from app.utils import logger
import asyncio

router = APIRouter()

@router.get("/")
async def get_jobs():
    # fetch (async) - note: in-memory only, no DB
    try:
        all_jobs = await fetch_all_jobs()
    except Exception as e:
        logger.exception("get_jobs.fetch_all_jobs failed: %s", str(e))
        all_jobs = []

    # Filtering and pagination are now handled by the frontend
    stats = compute_analytics(all_jobs)
    return {
        "count": len(all_jobs),
        "jobs": all_jobs,
        "stats": stats
    }
