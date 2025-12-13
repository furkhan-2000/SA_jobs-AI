import asyncio
import orjson
from loguru import logger
from rich.console import Console
from typing import Any, Optional
import httpx
from app.config import settings

console = Console()

# configure loguru
logger.remove()
logger.add(lambda msg: console.print(msg, highlight=False), level=settings.LOG_LEVEL)
logger.add("ksa_jobs.log", rotation="10 MB", retention="7 days", level=settings.LOG_LEVEL)

# httpx AsyncClient singleton factory
_async_client: Optional[httpx.AsyncClient] = None

def get_httpx_client() -> httpx.AsyncClient:
    global _async_client
    if _async_client is None or _async_client.is_closed:
        _async_client = httpx.AsyncClient(timeout=settings.TIMEOUT)
    return _async_client

async def async_get_json(url: str, params: dict | None = None, headers: dict | None = None, retries: int | None = None) -> Any | None:
    retries = retries or settings.MAX_RETRIES
    client = get_httpx_client()
    last_exc = None
    for attempt in range(1, retries + 1):
        try:
            resp = await client.get(url, params=params, headers=headers)
            resp.raise_for_status()
            try:
                return orjson.loads(resp.content)
            except Exception:
                return resp.json()
        except Exception as e:
            last_exc = e
            logger.warning(f"async_get_json attempt {attempt} failed for {url}: {e}")
            await asyncio.sleep(min(2 ** attempt, 8))
    logger.error(f"async_get_json all attempts failed for {url}: {last_exc}")
    return None
