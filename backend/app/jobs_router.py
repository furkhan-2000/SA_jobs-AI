from fastapi import APIRouter, Query
from app.job_service import fetch_all_jobs
from app.filters import apply_search_filter
from app.analytics import compute_analytics
from app.config import settings
from app.utils import logger
import asyncio

router = APIRouter()

@router.get("/")
async def get_jobs(
    keyword: str | None = Query(None),
    job_type: str | None = Query(None),
    industry: str | None = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(settings.PAGE_SIZE, ge=1, le=100)
):
    # fetch (async) - note: in-memory only, no DB
    try:
        all_jobs = await fetch_all_jobs()
    except Exception as e:
        logger.exception("get_jobs.fetch_all_jobs failed: %s", str(e))
        all_jobs = []

    filtered = apply_search_filter(all_jobs, keyword, job_type, industry)
    total = len(filtered)
    start = (page - 1) * page_size
    page_items = filtered[start:start + page_size]
    stats = compute_analytics(filtered)
    return {
        "count": total,
        "page": page,
        "page_size": page_size,
        "jobs": page_items,
        "stats": stats
    }
