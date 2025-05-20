from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

def fetch_naukri_jobs():
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)

    driver.get("https://www.naukri.com/data-science-jobs")
    time.sleep(5)  # Wait for JavaScript to load

    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()

    jobs = []
    for card in soup.select(".jobTuple"):
        title = card.find("a", class_="title")
        company = card.find("a", class_="subTitle")
        location = card.find("li", class_="location")

        if title and company:
            jobs.append({
                "title": title.text.strip(),
                "company": company.text.strip(),
                "location": location.text.strip() if location else "Not specified",
                "link": title["href"],
                "source": "Naukri"
            })

    return jobs
