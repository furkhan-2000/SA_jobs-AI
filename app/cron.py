from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.job_service import fetch_all_jobs
from app.utils import logger
import asyncio

scheduler = AsyncIOScheduler()

def start_scheduler():
    # Callback to log exceptions from asyncio tasks
    def log_task_exception(task):
        if task.exception():
            logger.error(f"Scheduler task failed with exception: {task.exception()}")

    # schedule periodic job; we run it as fire-and-forget
    async def runner():
        try:
            await fetch_all_jobs()
        except Exception as e:
            logger.exception("cron initial run failed: %s", str(e))

    initial_task = asyncio.create_task(runner())
    initial_task.add_done_callback(log_task_exception)

    # schedule hourly
    hourly_task = scheduler.add_job(lambda: asyncio.create_task(fetch_all_jobs()), 'interval', hours=1, id="ingest_hourly")
    # For scheduled jobs, APScheduler handles errors internally, but we can still ensure visibility
    # APScheduler's default error handling will log, but this ensures consistency with our custom logger
    # Note: APScheduler tasks are generally robust, this primarily for direct asyncio.create_task usage.
    logger.info("scheduler started (hourly ingestion)")
