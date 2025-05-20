import os
import json
import re
import json5  
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI client with Groq API
client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

def clean_job_data(job_data):
    """Ensure all job entries have consistent keys and are valid dictionaries."""
    cleaned = []
    for job in job_data:
        if isinstance(job, dict):
            job.setdefault("title", "N/A")
            job.setdefault("organization", job.get("company", "N/A"))
            job.setdefault("company", job.get("organization", "N/A"))
            job.setdefault("location", "N/A")
            job.setdefault("stipend", "N/A")
            job.setdefault("link", "#")
            job.setdefault("source", "N/A")
            cleaned.append(job)
    return cleaned

def pre_clean_output(output):
    """Attempt to correct minor LLM output issues before parsing."""
    # Replace single quotes with double quotes
    output = output.replace("'", '"')
    # Remove trailing commas
    output = re.sub(r',\s*([\]}])', r'\1', output)
    # Add quotes to unquoted keys (e.g., title: -> "title":)
    output = re.sub(r'([{,]\s*)(\w+)(\s*:\s*)', r'\1"\2"\3', output)
    return output

def extract_json_array(output):
    """Extract the first valid JSON list from the model's output."""
    match = re.search(r'\[\s*{[\s\S]*?}\s*]', output)
    return match.group(0) if match else None

def query_agent(user_query: str, job_data: list, max_results=20):
    short_data = clean_job_data(job_data[:40])

    prompt = f"""
You are an intelligent assistant helping a user find the most relevant internship and job opportunities.

Each opportunity is structured like this:
- title: title of the opportunity
- organization: name of the company or organization
- company: same as organization
- location: city or 'remote'
- stipend: 'unpaid', 'paid', or a specific amount
- link: application URL
- source: data source (e.g., Internshala, LinkedIn)

Your task:
From the input JSON list of jobs, return only the most relevant {max_results} entries for the user's query. 
Return the output as a **strict JSON list** of dictionaries in the **exact format below** and **nothing else**.

[ 
  {{
    "title": "...",
    "organization": "...",
    "company": "...",
    "location": "...",
    "stipend": "...",
    "link": "...",
    "source": "..."
  }},
  ...
]

IMPORTANT:
- DO NOT return markdown, explanation, or any notes.
- ONLY return a JSON list as shown above.
- NO comments, markdown syntax, or extra lines.

User Query: "{user_query}"
"""

    try:
        response = client.chat.completions.create(
            model=os.getenv("GROQ_MODEL"),
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": json.dumps(short_data)}
            ],
            temperature=0.3
        )

        raw_output = response.choices[0].message.content.strip()

        # Try direct parse
        try:
            parsed = json5.loads(raw_output)
            if isinstance(parsed, list):
                return clean_job_data(parsed)
        except Exception:
            pass

        # Pre-clean and retry parse
        cleaned_output = pre_clean_output(raw_output)
        try:
            parsed = json5.loads(cleaned_output)
            if isinstance(parsed, list):
                return clean_job_data(parsed)
        except Exception:
            pass

        # Fallback: extract JSON array and parse
        extracted = extract_json_array(raw_output)
        if not extracted:
            raise ValueError("No valid JSON array found in response.")

        extracted = pre_clean_output(extracted)
        parsed = json5.loads(extracted)
        return clean_job_data(parsed)

    except Exception as e:
        print("❌ Error parsing agent output:", e)
        print("🧠 Raw response:\n", raw_output)
        return []

# Entry point for CLI use
if __name__ == "__main__":
    print("\n🤖 Welcome to Internship Search Agent!")

    try:
        with open("data/jobs.json", "r", encoding="utf-8") as f:
            job_data = json.load(f)
    except FileNotFoundError:
        print("❌ Error: jobs.json not found. Run main.py first.")
        exit(1)

    user_query = input("💬 Enter your query (e.g. remote AI internships):\n> ").strip()

    print("\n🔍 Searching...\n")
    results = query_agent(user_query, job_data)

    if not results:
        print("⚠️ No results found or something went wrong.")
    else:
        for i, job in enumerate(results, 1):
            print("-" * 60)
            print(f"#{i}")
            print(f"🎯 Title       : {job.get('title', 'N/A')}")
            print(f"🏢 Organization: {job.get('organization', 'N/A')}")
            print(f"📍 Location    : {job.get('location', 'N/A')}")
            print(f"💰 Stipend     : {job.get('stipend', 'N/A')}")
            print(f"🔗 Link        : {job.get('link', '#')}")
            print(f"🌐 Source      : {job.get('source', 'N/A')}")
