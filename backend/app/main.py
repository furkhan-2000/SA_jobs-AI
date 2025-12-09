import uvicorn
from fastapi import FastAPI
from app.config import settings
from app.utils import setup_logging, logger
from app.jobs_router import router
from app.cron import start_scheduler

# initialize logging
setup_logging(settings.LOG_LEVEL)

app = FastAPI(title="KSA Jobs Master Backend", version="latest")

app.include_router(router, prefix="/jobs", tags=["jobs"])

@app.on_event("startup")
async def on_startup():
    logger.info("application startup")
    start_scheduler()

@app.get("/")
async def root():
    return {"status": f"KSA Jobs Backend running on port {settings.APP_PORT}"}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=settings.APP_PORT, log_level="info")
