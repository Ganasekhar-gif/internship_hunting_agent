import requests
from bs4 import BeautifulSoup

def fetch_kwoc():
    url = "https://kwoc.kossiitkgp.org/"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    # Normalize all visible text
    text = soup.get_text(separator=" ", strip=True).lower()

    status = "Open" if any(keyword in text for keyword in ["apply", "registration open", "join now", "register now"]) else "Closed"

    return [{
        "title": "Kharagpur Winter of Code (KWoC)",
        "organization": "KOSS IIT Kharagpur",
        "status": status,
        "link": url,
        "source": "KWoC"
    }]
