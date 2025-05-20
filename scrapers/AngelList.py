from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

def fetch_angellist_jobs():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(options=options)

    driver.get("https://wellfound.com/jobs")
    time.sleep(5)

    jobs = []
    cards = driver.find_elements(By.CLASS_NAME, "styles_component__jvMpa")

    for card in cards[:10]:  # Limit to top 10 for performance
        try:
            title = card.find_element(By.CLASS_NAME, "styles_title__xW1F-").text.strip()
            company = card.find_element(By.CLASS_NAME, "styles_startupName__xBnvG").text.strip()
            location = card.find_element(By.CLASS_NAME, "styles_location__vUULr").text.strip()
            link = card.find_element(By.TAG_NAME, "a").get_attribute("href")

            jobs.append({
                "title": title,
                "company": company,
                "location": location,
                "link": link,
                "source": "AngelList"
            })
        except Exception:
            continue

    driver.quit()
    return jobs
