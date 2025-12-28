from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from .jobs_router import router as jobs_router
from .cron import start_scheduler
from .utils import logger, close_httpx_client
from .config import settings  # Import settings


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

    # Only expose details in debug mode
    if settings.DEBUG_MODE:
        content = {
            "error": "Internal Server Error",
            "details": str(exc),
            "path": str(request.url)
        }
    else:
        content = {
            "error": "Internal Server Error",
            "message": "An unexpected error occurred. Please try again later.",
            "path": str(request.url)
        }
    return JSONResponse(
        status_code=500,
        content=content,
    )


# --------------------------------------------------------
# Health Check Endpoint
# --------------------------------------------------------
@app.get("/health")
async def health_check():
    return {"status": "ok"}


# --------------------------------------------------------
# Routers
# --------------------------------------------------------
app.include_router(jobs_router, prefix="/jobs", tags=["Jobs"])


# --------------------------------------------------------
# Static Files Mount (Order Matters)
# --------------------------------------------------------
app.mount("/", StaticFiles(directory="public", html=True), name="public")


# --------------------------------------------------------
# Scheduler Startup
# --------------------------------------------------------
@app.on_event("startup")
async def startup_event():
    logger.info("Starting job scheduler...")
    start_scheduler()


# --------------------------------------------------------
# Shutdown Events
# --------------------------------------------------------
@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down httpx client...")
    await close_httpx_client()
