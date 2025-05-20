from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

def fetch_linkedin_jobs():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(options=options)

    # You need to be logged in (can save cookies for advanced use)
    driver.get("https://www.linkedin.com/jobs/search/?keywords=data%20science")
    time.sleep(5)

    jobs = []
    job_cards = driver.find_elements(By.CLASS_NAME, "base-card")

    for card in job_cards:
        try:
            title = card.find_element(By.CLASS_NAME, "base-search-card__title").text.strip()
            company = card.find_element(By.CLASS_NAME, "base-search-card__subtitle").text.strip()
            location = card.find_element(By.CLASS_NAME, "job-search-card__location").text.strip()
            link = card.find_element(By.CLASS_NAME, "base-card__full-link").get_attribute("href")

            jobs.append({
                "title": title,
                "company": company,
                "location": location,
                "link": link,
                "source": "LinkedIn"
            })
        except Exception:
            continue

    driver.quit()
    return jobs
