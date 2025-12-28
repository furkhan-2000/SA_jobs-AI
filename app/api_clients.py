from app.utils import async_get_json, logger
from app.config import settings
from typing import List, Any, Optional # Added Optional

class JobAPIClients:
    @staticmethod
    async def fetch_arbeitnow() -> List[Any]:
        logger.warning("arbeitnow API client is not implemented.")
        return []

    @staticmethod
    async def fetch_jobicy() -> List[Any]:
        logger.warning("jobicy API client is not implemented.")
        return []

    @staticmethod
    async def fetch_remotive() -> List[Any]:
        logger.warning("remotive API client is not implemented.")
        return []

    @staticmethod
    async def fetch_adzuna() -> List[Any]:
        logger.warning("adzuna API client is not implemented.")
        return []

    @staticmethod
    async def fetch_jooble() -> List[Any]:
        logger.warning("jooble API client is not implemented.")
        return []

    @staticmethod
    async def fetch_careerjet() -> List[Any]:
        logger.warning("careerjet API client is not implemented.")
        return []

    @staticmethod
    async def fetch_openweb_ninja() -> List[Any]:
        logger.warning("OpenWebNinja API is disabled due to expired key. Skipping fetch.")
        return [] # Corrected indentation for this return
                                      
                                      
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
            f"{settings.AI_SERVICE_URL}/search", # Corrected to include /search endpoint
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
                   