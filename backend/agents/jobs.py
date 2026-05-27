import os
import httpx
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent.parent / ".env")

async def fetch_jobs(query: str, location: str = "India") -> list:

    url = "https://jsearch.p.rapidapi.com/search"

    headers = {
        "x-rapidapi-key": os.getenv("JSEARCH_API_KEY"),
        "x-rapidapi-host": os.getenv("JSEARCH_API_HOST"),
    }

    params = {
        "query": f"{query} in {location}",
        "num_results": "5",
        "date_posted": "month",
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers, params=params, timeout=10)
            data = response.json()

        jobs = []
        for job in data.get("data", [])[:5]:
            jobs.append({
                "title": job.get("job_title"),
                "company": job.get("employer_name"),
                "location": job.get("job_city") or job.get("job_country"),
                "employment_type": job.get("job_employment_type"),
                "posted": job.get("job_posted_at_datetime_utc", "")[:10],
                "apply_link": job.get("job_apply_link"),
            })
        return jobs

    except Exception as e:
        print(f"Job fetch error: {e}")
        return []