from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import logging

from .jobs_router import router as jobs_router
from .cron import start_scheduler

# --------------------------------------------------------
# Logging Setup
# --------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

# --------------------------------------------------------
# FastAPI App Initialization
# --------------------------------------------------------
app = FastAPI(title="KSA Jobs API", version="1.0")

# --------------------------------------------------------
# CORS Middleware (Required for Frontend)
# --------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # allow all — replace with domain on production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------------------------------------------
# Logging Middleware (Each Request)
# --------------------------------------------------------
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Incoming request: {request.method} {request.url}")

    try:
        response = await call_next(request)
    except Exception as exc:
        logger.error(f"Unhandled exception: {exc}")
        raise

    logger.info(f"Completed request: {response.status_code}")
    return response

# --------------------------------------------------------
# Global Error Handler
# --------------------------------------------------------
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global error caught: {exc}")

    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "details": str(exc),
            "path": str(request.url)
        },
    )

# --------------------------------------------------------
# Routers
# --------------------------------------------------------
app.include_router(jobs_router, prefix="/jobs", tags=["Jobs"])

# --------------------------------------------------------
# Scheduler
# --------------------------------------------------------
@app.on_event("startup")
async def startup_event():
    logger.info("Starting job scheduler...")
    start_scheduler()

# --------------------------------------------------------
# Root Endpoint
# --------------------------------------------------------
@app.get("/")
async def root():
    return {"status": "alive", "service": "KSA Jobs Backend"}


# --------------------------------------------------------
# Run - for local debugging only
# --------------------------------------------------------
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
