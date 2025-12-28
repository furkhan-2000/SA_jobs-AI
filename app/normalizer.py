from typing import Dict


def _to_str_or_empty(value) -> str:
    """Converts a value to a stripped string, handling None by returning an empty string."""
    if value is None:
        return ""
    return str(value).strip()


def _normalize_default(raw: Dict, source: str) -> Dict:
    """Default normalizer for common field names."""
    title = raw.get("title") or raw.get("jobTitle") or raw.get("name")
    company = raw.get("company") or raw.get("company_name") or raw.get("companyName")
    url = raw.get("url") or raw.get("jobUrl") or raw.get("link") or raw.get("apply_url")
    description = raw.get("description") or raw.get("jobDescription")
    job_type = raw.get("type") or raw.get("jobType") or raw.get("job_type")
    industry = raw.get("industry") or raw.get("jobIndustry")
    location = raw.get("location") or raw.get("jobGeo") or raw.get("candidate_required_location")
    remote = raw.get("remote") if isinstance(raw.get("remote"), bool) else (location is not None and "remote" in _to_str_or_empty(location).lower())
    pub_date = raw.get("pubDate") or raw.get("publication_date") or raw.get("date") or None

    return {
        "source": source,
        "title": _to_str_or_empty(title),
        "company": _to_str_or_empty(company),
        "url": _to_str_or_empty(url),
        "description": _to_str_or_empty(description),
        "jobType": _to_str_or_empty(job_type),
        "jobIndustry": _to_str_or_empty(industry),
        "location": _to_str_or_empty(location),
        "remote": bool(remote),
        "pubDate": pub_date,
    }


def normalize_adzuna(raw: Dict, source: str) -> Dict:
    """Normalizer for Adzuna API data."""
    # Start with default normalization
    normalized = _normalize_default(raw, source)

    # Override with Adzuna-specific fields
    normalized.update({
        "company": (raw.get("company") or {}).get("display_name", ""),
        "location": (raw.get("location") or {}).get("display_name", ""),
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