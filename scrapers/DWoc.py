import requests
from bs4 import BeautifulSoup

def fetch_devscript_woc():
    url = "https://winterofcode.devscript.tech/"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Normalize all visible text
        text = soup.get_text(separator=" ", strip=True).lower()
        status = "Open" if any(keyword in text for keyword in ["apply", "registration open", "join now", "register now"]) else "Closed"

        return [{
            "title": "DevScript Winter of Code",
            "organization": "DevScript",
            "status": status,
            "link": url,
            "source": "DevScript-WoC"
        }]
    
    except requests.RequestException as e:
        print(f"❌ Network error in fetch_devscript_woc: {e}")
        return []
    except Exception as e:
        print(f"❌ Unexpected error in fetch_devscript_woc: {e}")
        return []
