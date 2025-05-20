import requests

def fetch_hackerearth_jobs():
    url = "https://www.hackerearth.com/challenges/api/hackerearth/jobs/"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        # Check content type before attempting to parse JSON
        if "application/json" not in response.headers.get("Content-Type", ""):
            print("⚠️ Unexpected content type from HackerEarth API.")
            return []

        jobs = response.json().get("jobs", [])
    except requests.RequestException as e:
        print(f"❌ Network error in fetch_hackerearth_jobs: {e}")
        return []
    except ValueError as e:
        print(f"❌ JSON decoding error in fetch_hackerearth_jobs: {e}")
        return []

    relevant = []
    keywords = ["data", "ml", "ai", "machine", "science", "analytics", "deep learning"]

    for job in jobs:
        title = job.get("title", "")
        if any(keyword in title.lower() for keyword in keywords):
            relevant.append({
                "title": title,
                "company": job.get("company", "Unknown"),
                "location": job.get("location", "Not specified"),
                "link": job.get("url", "#"),
                "source": "HackerEarth"
            })

    return relevant
