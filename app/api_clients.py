from app.utils import async_get_json, logger
from app.config import settings
from typing import List, Any

class JobAPIClients:
    """
    Async fetchers for job APIs.
    Focus: Global remote jobs that Saudis can apply to while residing in KSA.
    Returns list of raw job dicts or empty list.
    """

    @staticmethod
    async def fetch_arbeitnow() -> List[Any]:
        """
        Arbeitnow - European job board with remote positions.
        Returns jobs from all locations (we filter for remote/KSA later).
        """
        url = "https://www.arbeitnow.com/api/job-board-api"
        data = await async_get_json(url)
        
        if settings.DEBUG_MODE and data:
            logger.debug(f"Arbeitnow raw data: {data}")
        
        if isinstance(data, dict):
            return data.get("data", []) or []
        if isinstance(data, list):
            return data
        return []

    @staticmethod
    async def fetch_jobicy() -> List[Any]:
        """
        Jobicy - Remote jobs platform.
        CHANGED: Removed geo=emea filter to get ALL global remote jobs.
        """
        url = "https://jobicy.com/api/v2/remote-jobs"
        # FIXED: No geo filter - get all remote jobs globally
        params = {"count": 50}
        
        data = await async_get_json(url, params=params)
        
        if settings.DEBUG_MODE and data:
            logger.debug(f"Jobicy raw data: {data}")
        
        if isinstance(data, dict):
            jobs = data.get("jobs", []) or data.get("data", []) or []
            return jobs
        if isinstance(data, list):
            return data
        return []

    @staticmethod
    async def fetch_remotive() -> List[Any]:
        """
        Remotive - Remote-first job board.
        All jobs are remote by nature, perfect for global applicants.
        """
        url = "https://remotive.com/api/remote-jobs"
        data = await async_get_json(url)
        
        if settings.DEBUG_MODE and data:
            logger.debug(f"Remotive raw data: {data}")
        
        if isinstance(data, dict):
            return data.get("jobs", []) or []
        return []

    @staticmethod
    async def fetch_adzuna() -> List[Any]:
        """
        Adzuna - Job search aggregator.
        CHANGED: Search for 'remote' jobs instead of location-based search.
        Using GB endpoint but searching for remote positions globally.
        """
        app_id = settings.ADZUNA_APP_ID
        app_key = settings.ADZUNA_APP_KEY
        
        # FIXED: Search for remote jobs instead of Saudi Arabia location
        url = f"https://api.adzuna.com/v1/api/jobs/gb/search/1"
        params = {
            "app_id": app_id,
            "app_key": app_key,
            "results_per_page": 50,
            "what": "remote",  # Search keyword: "remote"
            "where": "worldwide"  # Look for worldwide remote jobs
        }
        
        data = await async_get_json(url, params=params)
        
        if settings.DEBUG_MODE and data:
            logger.debug(f"Adzuna raw data: {data}")
        
        if isinstance(data, dict):
            return data.get("results", []) or []
        return []

    @staticmethod
    async def fetch_jooble() -> List[Any]:
        """
        Jooble - Job search engine.
        Requires valid API key (currently placeholder).
        """
        key = settings.JOOBLE_KEY
        if not key or "bcf720ac" in key:
            logger.warning("Jooble key missing or is a placeholder")
            return []
        
        url = f"https://jooble.org/api/{key}"
        
        # CHANGED: Search for remote jobs globally, not location-specific
        json_data = {
            "keywords": "remote software developer engineer",
            "location": ""  # Empty = worldwide search
        }
        
        data = await async_get_json(url, method='POST', json=json_data)
        
        if settings.DEBUG_MODE and data:
            logger.debug(f"Jooble raw data: {data}")
        
        if isinstance(data, dict):
            return data.get("jobs", []) or data.get("data", []) or []
        return []

    @staticmethod
    async def fetch_careerjet() -> List[Any]:
        """
        Careerjet - Job search engine.
        Requires valid API key (currently placeholder).
        """
        key = settings.CAREERJET_KEY
        if not key or "6fde6cd" in key:
            logger.warning("Careerjet key missing or is a placeholder")
            return []
        
        # CHANGED: Search for remote jobs worldwide
        url = "http://public.api.careerjet.net/search"
        params = {
            "affid": key,
            "keywords": "remote",  # Search for remote jobs
            "location": "",  # Worldwide
            "pagesize": 50,
            "user_ip": "127.0.0.1",
            "user_agent": "Mozilla/5.0"
        }
        
        data = await async_get_json(url, params=params)
        
        if settings.DEBUG_MODE and data:
            logger.debug(f"Careerjet raw data: {data}")
        
        if isinstance(data, dict):
            return data.get("jobs", []) or []
        return []

    @staticmethod
    async def fetch_openweb_ninja() -> List[Any]:
        """
        OpenWebNinja (JSearch) - Job search API.
        Requires valid API key (currently expired - 401 errors).
        """
        key = settings.OPENWEBNINJA_KEY
        if not key:
            logger.warning("OpenWebNinja key missing")
            return []
        
        url = "https://app.openwebninja.com/api/jsearch/search"
        headers = {"X-Api-Key": key}
        
        # CHANGED: Search for remote jobs, not locale-specific
        params = {
            "limit": 50,
            "query": "remote software engineer",  # Search term
            "employment_types": "FULLTIME,PARTTIME,CONTRACTOR"
        }
        
        data = await async_get_json(url, headers=headers, params=params)
        
        if settings.DEBUG_MODE and data:
            logger.debug(f"OpenWebNinja raw data: {data}")
        
        if isinstance(data, dict):
            # Common response keys for JSearch API
            return (data.get("data", []) or 
                   data.get("results", []) or 
                   data.get("jobs", []) or [])
        return []