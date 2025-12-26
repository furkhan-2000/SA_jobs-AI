from app.utils import async_get_json, logger
from app.config import settings
from typing import List, Any, Optional # Added Optional

class JobAPIClients:
    # ... (existing JobAPIClients class content) ...

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
                   