from app.utils import async_get_json, logger
from app.config import settings
from typing import List, Any

class JobAPIClients:
    """Async fetchers. Return list of raw job dicts or empty list."""

    @staticmethod
    async def fetch_arbeitnow() -> List[Any]:
        url = "https://www.arbeitnow.com/api/job-board-api"
        data = await async_get_json(url)
        if isinstance(data, dict):
            return data.get("data", []) or []
        if isinstance(data, list):
            return data
        return []

    @staticmethod
    async def fetch_jobicy() -> List[Any]:
        url = "https://jobicy.com/api/v2/remote-jobs"
        params = {"count":50, "geo":"emea"}
        data = await async_get_json(url, params=params)
        if isinstance(data, dict):
            return data.get("data", []) or []
        return []

    @staticmethod
    async def fetch_remotive() -> List[Any]:
        url = "https://remotive.com/api/remote-jobs"
        data = await async_get_json(url)
        if isinstance(data, dict):
            return data.get("jobs", []) or []
        return []

    @staticmethod
    async def fetch_adzuna() -> List[Any]:
        app_id = settings.ADZUNA_APP_ID
        app_key = settings.ADZUNA_APP_KEY
        # The /sa/ endpoint is 404. Use the main endpoint with a location query.
        url = f"https://api.adzuna.com/v1/api/jobs/gb/search/1" 
        params = {
            "app_id": app_id,
            "app_key": app_key,
            "results_per_page": 50,
            "where": "saudi arabia"
        }
        data = await async_get_json(url, params=params)
        if isinstance(data, dict):
            return data.get("results", []) or []
        return []

    @staticmethod
    async def fetch_jooble() -> List[Any]:
        key = settings.JOOBLE_KEY
        if not key or "bcf720ac" in key: # Check for placeholder
            logger.warning("Jooble key missing or is a placeholder")
            return []
        url = f"https://jooble.org/api/{key}"
        # Jooble requires a POST request with a JSON body
        json_data = {"keywords": "it software developer", "location": "Saudi Arabia"}
        data = await async_get_json(url, method='POST', json=json_data)
        if isinstance(data, dict):
            return data.get("jobs", []) or data.get("data", []) or []
        return []

    @staticmethod
    async def fetch_careerjet() -> List[Any]:
        key = settings.CAREERJET_KEY
        if not key or "6fde6cd" in key: # Check for placeholder
            logger.warning("Careerjet key missing or is a placeholder")
            return []
        # The old URL is 404. Use the new public API endpoint.
        url = "http://public.api.careerjet.net/search"
        params = {
            "affid": key,
            "location": "Saudi Arabia",
            "pagesize": 50,
            "user_ip": "127.0.0.1", # API requires these, even if placeholders
            "user_agent": "Mozilla/5.0"
        }
        data = await async_get_json(url, params=params)
        if isinstance(data, dict):
            return data.get("jobs", []) or []
        return []

    @staticmethod
    async def fetch_openweb_ninja() -> List[Any]:
        key = settings.OPENWEBNINJA_KEY
        if not key:
            logger.warning("OpenWebNinja key missing")
            return []
        url = "https://app.openwebninja.com/api/jsearch/search"
        headers = {"X-Api-Key": key}
        params = {"limit":50, "locale":"sa"}
        data = await async_get_json(url, headers=headers, params=params)
        if isinstance(data, dict):
            # common keys used by Ninja
            return data.get("results", []) or data.get("data", []) or data.get("jobs", []) or []
        return []
