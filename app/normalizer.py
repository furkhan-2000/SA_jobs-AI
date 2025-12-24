from typing import Dict

def _normalize_default(raw: Dict, source: str) -> Dict:
    """Default normalizer for common field names."""
    title = raw.get("title") or raw.get("jobTitle") or raw.get("name") or ""
    company = raw.get("company") or raw.get("company_name") or raw.get("companyName") or ""
    url = raw.get("url") or raw.get("jobUrl") or raw.get("link") or raw.get("apply_url") or ""
    description = raw.get("description") or raw.get("jobDescription") or ""
    job_type = raw.get("type") or raw.get("jobType") or raw.get("job_type") or ""
    industry = raw.get("industry") or raw.get("jobIndustry") or ""
    location = raw.get("location") or raw.get("jobGeo") or raw.get("candidate_required_location") or ""
    remote = raw.get("remote") if isinstance(raw.get("remote"), bool) else ("remote" in str(location).lower())
    pub_date = raw.get("pubDate") or raw.get("publication_date") or raw.get("date") or None

    return {
        "source": source,
        "title": str(title).strip(),
        "company": str(company).strip(),
        "url": str(url).strip(),
        "description": str(description).strip(),
        "jobType": str(job_type).strip(),
        "jobIndustry": str(industry).strip(),
        "location": str(location).strip(),
        "remote": bool(remote),
        "pubDate": pub_date,
    }

def normalize_adzuna(raw: Dict, source: str) -> Dict:
    """Normalizer for Adzuna API data."""
    # Start with default normalization
    normalized = _normalize_default(raw, source)
    
    # Override with Adzuna-specific fields
    normalized.update({
        "company": raw.get("company", {}).get("display_name", "") if isinstance(raw.get("company"), dict) else "",
        "location": raw.get("location", {}).get("display_name", "") if isinstance(raw.get("location"), dict) else "",
        "url": raw.get("redirect_url", normalized["url"]),
    })
    return normalized

def normalize_job(raw: Dict, source: str) -> Dict:
    """
    Factory function to select the correct normalizer based on the source
    and return a consistently shaped job dictionary.
    """
    normalizers = {
        "adzuna": normalize_adzuna,
        # Add other specific normalizers here if needed in the future
    }

    # Get the appropriate normalizer (defaults to _normalize_default)
    normalizer_func = normalizers.get(source, _normalize_default)

    # ALL normalizers now accept (raw, source)
    return normalizer_func(raw, source)