from app.utils import async_get_json, logger
from app.config import settings
from typing import List, Any, Optional

class JobAPIClients:
    @staticmethod
    async def fetch_arbeitnow() -> List[Any]:
        """
        ArbeitNow - Free remote job API, no key required.
        Docs: https://arbeitnow.com/api
        """
        url = "https://www.arbeitnow.com/api/job-board-api"
        data = await async_get_json(url)

        if settings.DEBUG_MODE and data:
            logger.debug(f"ArbeitNow raw data sample: {data.get('data', [])[:1] if isinstance(data, dict) else []}")

        if isinstance(data, dict):
            return data.get("data", [])
        return []

    @staticmethod
    async def fetch_jobicy() -> List[Any]:
        """
        Jobicy - Free remote jobs API, no key required.
        Docs: https://jobicy.com/api
        """
        url = "https://jobicy.com/api/v2/remote-jobs"
        params = {"count": 50, "geo": "worldwide"}

        data = await async_get_json(url, params=params)

        if settings.DEBUG_MODE and data:
            logger.debug(f"Jobicy raw data sample: {data[:1] if isinstance(data, list) else []}")

        if isinstance(data, list):
            return data
        elif isinstance(data, dict):
            return data.get("jobs", []) or data.get("data", [])
        return []

    @staticmethod
    async def fetch_remotive() -> List[Any]:
        """
        Remotive - Free remote jobs API, no key required.
        Docs: https://remotive.com/api
        """
        url = "https://remotive.com/api/remote-jobs"
        params = {"limit": 50}

        data = await async_get_json(url, params=params)

        if settings.DEBUG_MODE and data:
            logger.debug(f"Remotive raw data sample: {data.get('jobs', [])[:1] if isinstance(data, dict) else []}")

        if isinstance(data, dict):
            return data.get("jobs", [])
        return []

    @staticmethod
    async def fetch_adzuna() -> List[Any]:
        """
        Adzuna - Job search API with location filtering.
        Docs: https://developer.adzuna.com/
        Requires: ADZUNA_APP_ID and ADZUNA_APP_KEY
        """
        app_id = settings.ADZUNA_APP_ID
        app_key = settings.ADZUNA_APP_KEY

        if not app_id or not app_key:
            logger.warning("Adzuna credentials missing")
            return []

        # Search in Saudi Arabia specifically
        url = f"https://api.adzuna.com/v1/api/jobs/sa/search/1"
        params = {
            "app_id": app_id,
            "app_key": app_key,
            "results_per_page": 50,
            "what": "software developer",  # Generic tech search
            "content-type": "application/json"
        }

        data = await async_get_json(url, params=params)

        if settings.DEBUG_MODE and data:
            logger.debug(f"Adzuna raw data sample: {data.get('results', [])[:1] if isinstance(data, dict) else []}")

        if isinstance(data, dict):
            return data.get("results", [])
        return []

    @staticmethod
    async def fetch_jooble() -> List[Any]:
        """
        Jooble - Job search API.
        Docs: https://jooble.org/api/about
        Requires: JOOBLE_KEY
        """
        key = settings.JOOBLE_KEY
        if not key:
            logger.warning("Jooble key missing")
            return []

        url = f"https://jooble.org/api/{key}"

        # Search for remote jobs and KSA jobs
        payload = {
            "keywords": "software developer remote",
            "location": "Saudi Arabia"
        }

        data = await async_get_json(
            url,
            method='POST',
            json=payload
        )

        if settings.DEBUG_MODE and data:
            logger.debug(f"Jooble raw data sample: {data.get('jobs', [])[:1] if isinstance(data, dict) else []}")

        if isinstance(data, dict):
            return data.get("jobs", [])
        return []

    @staticmethod
    async def fetch_careerjet() -> List[Any]:
        """
        Careerjet - Job search API.
        Docs: https://www.careerjet.com/partners/api/
        Requires: CAREERJET_KEY
        """
        key = settings.CAREERJET_KEY
        if not key:
            logger.warning("Careerjet key missing")
            return []

        url = "https://public.api.careerjet.net/search"
        params = {
            "affid": key,
            "user_ip": "127.0.0.1",  # Required by API
            "user_agent": "Mozilla/5.0",  # Required by API
            "locale_code": "en_SA",  # Saudi Arabia
            "keywords": "software developer",
            "location": "Saudi Arabia",
            "pagesize": 50,
            "page": 1
        }

        data = await async_get_json(url, params=params)

        if settings.DEBUG_MODE and data:
            logger.debug(f"Careerjet raw data sample: {data.get('jobs', [])[:1] if isinstance(data, dict) else []}")

        if isinstance(data, dict):
            return data.get("jobs", [])
        return []

    @staticmethod
    async def fetch_openweb_ninja() -> List[Any]:
        """
        OpenWebNinja (JSearch) - Job search API.
        NOTE: Currently disabled due to expired API key.
        """
        logger.info("OpenWebNinja API is disabled due to expired key. Skipping fetch.")
        return []


async def fetch_ai_search_results(query: str) -> Optional[Any]:
    """
    Calls the external AI microservice to get intelligent search results.

    Args:
        query: The user's search query.

    Returns:
        The JSON response from the AI service, or None if the service is
        not configured or the request fails.
    """
    if not settings.AI_SERVICE_URL:
        logger.debug("AI_SERVICE_URL not configured, skipping AI search.")
        return None

    logger.debug(f"Calling AI service with query: '{query}'")
    try:
        # We assume the AI service expects a POST request with a JSON body
        payload = {"query": query}
        ai_results = await async_get_json(
            f"{settings.AI_SERVICE_URL}/search",
            method='POST',
            json=payload,
            retries=1  # Fail faster for AI service
        )

        if not ai_results:
            logger.warning("AI service returned an empty or invalid response.")
            return None

        logger.debug("Successfully received response from AI service.")
        return ai_results

    except Exception as e:
        logger.error(f"An unexpected error occurred while calling the AI service: {e}")
        return None