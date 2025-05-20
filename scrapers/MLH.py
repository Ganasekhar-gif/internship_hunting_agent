import requests
from bs4 import BeautifulSoup

def fetch_mlh_fellowship():
    url = "https://fellowship.mlh.io/"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    apply_button = soup.find("a", string=lambda s: s and any(k in s.lower() for k in ["apply", "join", "register"]))
    is_open = bool(apply_button and "disabled" not in apply_button.get("class", []))

    return [{
        "title": "MLH Fellowship",
        "organization": "Major League Hacking",
        "status": "Open" if is_open else "Closed",
        "link": apply_button["href"] if apply_button else url,
        "source": "MLH"
    }]
