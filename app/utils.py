import asyncio
import orjson
from loguru import logger
from rich.console import Console
from typing import Any, Optional
import httpx
from app.config import settings
import sys


console = Console()


# Configure loguru
log_level = "DEBUG" if settings.DEBUG_MODE else settings.LOG_LEVEL
logger.remove()  # Remove default handler
logger.add(
    sys.stderr,
    level=log_level,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
)  # Add a more detailed stderr handler

# Add file handler with more details in debug mode
file_log_config = {
    "rotation": "10 MB",
    "retention": "7 days",
    "level": log_level
}
if settings.DEBUG_MODE:
    file_log_config["backtrace"] = True
    file_log_config["diagnose"] = True

logger.add("ksa_jobs.log", **file_log_config)

# Intercept standard logging messages and redirect to loguru
logger.enable("app")  # Enable loguru for the 'app' module and its submodules


# httpx AsyncClient singleton factory
_async_client: Optional[httpx.AsyncClient] = None


def get_httpx_client() -> httpx.AsyncClient:
    global _async_client
    if _async_client is None or _async_client.is_closed:
        _async_client = httpx.AsyncClient(timeout=settings.TIMEOUT)
    return _async_client


async def close_httpx_client():
    global _async_client
    if _async_client is not None and not _async_client.is_closed:
        await _async_client.aclose()
        _async_client = None
        logger.info("httpx AsyncClient closed.")


async def async_get_json(
    url: str,
    method: str = "GET",
    params: dict | None = None,
    headers: dict | None = None,
    json: dict | None = None,
    retries: int | None = None
) -> Any | None:
    retries = retries or settings.MAX_RETRIES
    client = get_httpx_client()
    last_exc = None
    for attempt in range(1, retries + 1):
        try:
            if method.upper() == 'POST':
                resp = await client.post(url, params=params, headers=headers, json=json)
            else:
                resp = await client.get(url, params=params, headers=headers)

            resp.raise_for_status()
            try:
                return orjson.loads(resp.content)
            except Exception:
                return resp.json()
        except httpx.HTTPStatusError as e:  # Catch specific HTTP status errors
            last_exc = e
            logger.warning(
                f"async_get_json (method: {method}) attempt {attempt} failed for {url} with status {e.response.status_code}: {e}"
            )
            await asyncio.sleep(min(2 ** attempt, 8))
        except Exception as e:  # Catch other exceptions
            last_exc = e
            logger.warning(
                f"async_get_json (method: {method}) attempt {attempt} failed for {url}: {e}"
            )
            await asyncio.sleep(min(2 ** attempt, 8))
    logger.error(f"async_get_json (method: {method}) all attempts failed for {url}: {last_exc}")
    return None
