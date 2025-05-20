import requests
from bs4 import BeautifulSoup

def fetch_ycombinator_jobs():
    url = "https://www.ycombinator.com/jobs"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    jobs = []
    for listing in soup.find_all('a', class_='JobPreview'):
        title_tag = listing.find('h2')
        company_tag = listing.find('h3')
        if not title_tag or not company_tag:
            continue

        title = title_tag.text.strip()
        company = company_tag.text.strip()
        link = "https://www.ycombinator.com" + listing["href"]

        if any(kw in title.lower() for kw in ["data", "ml", "ai", "machine", "science", "deep learning", "analytics"]):
            jobs.append({
                "title": title,
                "company": company,
                "location": "Remote or India (Check listing)",
                "link": link,
                "source": "Y Combinator"
            })

    return jobs
