from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.job_service import fetch_all_jobs
from app.utils import logger
import asyncio

scheduler = AsyncIOScheduler()

def start_scheduler():
    # schedule periodic job; we run it as fire-and-forget
    async def runner():
        try:
            await fetch_all_jobs()
        except Exception as e:
            logger.exception("cron initial run failed: %s", str(e))

    # run once on startup
    asyncio.create_task(runner())

    # schedule hourly
    scheduler.add_job(lambda: asyncio.create_task(fetch_all_jobs()), 'interval', hours=1, id="ingest_hourly")
    scheduler.start()
    logger.info("scheduler started (hourly ingestion)")
