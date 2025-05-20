import requests
from bs4 import BeautifulSoup

def fetch_gsoc_programs():
    url = "https://summerofcode.withgoogle.com/programs/"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    programs = []

    for card in soup.find_all('gsoc-card', recursive=True):
        # Card content is rendered with JavaScript, so we need to use a fallback:
        # We will just provide a placeholder, in a real app you'd use Selenium or API.
        programs.append({
            "title": "Google Summer of Code",
            "status": "Use API or Selenium to check status",
            "link": "https://summerofcode.withgoogle.com"
        })

    return programs
