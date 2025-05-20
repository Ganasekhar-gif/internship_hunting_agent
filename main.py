import json
import os
import argparse
import logging
from dotenv import load_dotenv

from scrapers.GSOC import fetch_gsoc_programs
from scrapers.code4govtech import fetch_code4govtech_programs
from scrapers.MLH import fetch_mlh_fellowship
from scrapers.KWoc import fetch_kwoc
from scrapers.DWoc import fetch_devscript_woc
from scrapers.Naukri import fetch_naukri_jobs
from scrapers.HackerEarth import fetch_hackerearth_jobs
from scrapers.YCombinator import fetch_ycombinator_jobs
from scrapers.AngelList import fetch_angellist_jobs
from scrapers.internshala import fetch_internshala_ds_internships
from scrapers.linkedin import fetch_linkedin_jobs

from agent import query_agent
from send_email import send_email

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# Load environment variables
load_dotenv()
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")

SEEN_JOBS_FILE = "seen_jobs.json"
FILTERED_JOBS_FILE = os.path.join("data", "filtered_jobs.json")

def load_seen_links():
    if os.path.exists(SEEN_JOBS_FILE):
        try:
            with open(SEEN_JOBS_FILE, "r") as f:
                return set(json.load(f))
        except json.JSONDecodeError:
            logging.warning("⚠️ seen_jobs.json is corrupted. Starting with empty seen links.")
    return set()

def save_seen_links(links):
    with open(SEEN_JOBS_FILE, "w") as f:
        json.dump(list(links), f)

def run_all_scrapers():
    all_results = []
    logging.info("🔍 Running Internship and Open Source Scrapers...")

    scrapers = [
        fetch_gsoc_programs,
        fetch_code4govtech_programs,
        fetch_mlh_fellowship,
        fetch_kwoc,
        fetch_devscript_woc,
        fetch_naukri_jobs,
        fetch_hackerearth_jobs,
        fetch_ycombinator_jobs,
        fetch_angellist_jobs,
        fetch_internshala_ds_internships,
        fetch_linkedin_jobs
    ]

    for scraper in scrapers:
        try:
            logging.info(f"🚀 Running: {scraper.__name__}")
            results = scraper()
            all_results.extend(results)
            logging.info(f"✅ {len(results)} results from {scraper.__name__}")
        except Exception as e:
            logging.error(f"❌ Error running {scraper.__name__}: {e}")

    logging.info(f"\n✅ Total opportunities found: {len(all_results)}")
    return all_results

def print_jobs(jobs):
    for i, job in enumerate(jobs, 1):
        print("-" * 60)
        print(f"#{i}")
        print(f"🎯 Title       : {job.get('title', 'N/A')}")
        print(f"🏢 Organization: {job.get('organization') or job.get('company', 'N/A')}")
        print(f"📍 Location    : {job.get('location', 'N/A')}")
        print(f"💰 Stipend     : {job.get('stipend', 'N/A')}")
        print(f"🔗 Link        : {job.get('link', '#')}")
        print(f"🌐 Source      : {job.get('source', 'N/A')}")

def job_key(job):
    # Create a robust deduplication key from title, organization/company, and location
    title = (job.get('title') or '').strip().lower()
    org = (job.get('organization') or job.get('company') or '').strip().lower()
    loc = (job.get('location') or '').strip().lower()
    return (title, org, loc)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--auto", action="store_true", help="Automatically filter with LLaMA 3 without user input")
    parser.add_argument("--query", type=str, default="remote data science internships", help="Query for LLaMA 3 filtering")
    args = parser.parse_args()

    jobs = run_all_scrapers()
    seen_links = load_seen_links()

    new_jobs = []
    seen_keys = set()
    duplicates_by_link = 0
    duplicates_by_key = 0

    for job in jobs:
        link = job.get("link")
        if not link:
            logging.warning(f"⚠️ Skipping job due to missing link: {job.get('title', 'Unknown Title')}")
            continue

        key = job_key(job)

        if link in seen_links:
            duplicates_by_link += 1
            continue  # Duplicate by link
        if key in seen_keys:
            duplicates_by_key += 1
            continue  # Duplicate by content key

        new_jobs.append(job)
        seen_keys.add(key)

    logging.info(f"Filtered out {duplicates_by_link} duplicates by link.")
    logging.info(f"Filtered out {duplicates_by_key} duplicates by job key.")
    logging.info(f"{len(new_jobs)} new jobs after deduplication.")

    if args.auto:
        logging.info(f"\n🤖 Running LLaMA 3 filter with query: {args.query}")
        filtered_jobs = query_agent(args.query, new_jobs)

        # Deduplicate filtered jobs again by link to be extra safe
        filtered_jobs_unique = []
        filtered_links_seen = set()
        for job in filtered_jobs:
            l = job.get("link")
            if l and l not in filtered_links_seen:
                filtered_jobs_unique.append(job)
                filtered_links_seen.add(l)

        filtered_jobs = filtered_jobs_unique

        print_jobs(filtered_jobs)

        if filtered_jobs:
            logging.info(f"\n📬 Sending {len(filtered_jobs)} filtered opportunities via email...")
            try:
                send_email(filtered_jobs, SENDER_EMAIL, SENDER_PASSWORD, RECEIVER_EMAIL)

                # Update seen links with filtered jobs links
                updated_links = seen_links.union({job["link"] for job in filtered_jobs})
                save_seen_links(updated_links)

                # Save filtered jobs to file
                os.makedirs("data", exist_ok=True)
                with open(FILTERED_JOBS_FILE, "w", encoding="utf-8") as f:
                    json.dump(filtered_jobs, f, ensure_ascii=False, indent=2)

                logging.info(f"💾 Filtered jobs saved to {FILTERED_JOBS_FILE}")

            except Exception as e:
                logging.error(f"❌ Failed to send email: {e}")
        else:
            logging.info("\n📭 No relevant jobs found. No email sent.")
    else:
        logging.info("\nℹ️  Use --auto to filter and send relevant jobs automatically.")
