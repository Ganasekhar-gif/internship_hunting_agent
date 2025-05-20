import requests
from bs4 import BeautifulSoup

def fetch_code4govtech_programs():
    url = "https://codeforgovtech.in"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    programs = []

    # Focus on the "Our Projects" section if available
    # The main projects are usually inside cards with 'project' in the link and title
    project_sections = soup.find_all('a', href=True)
    for a_tag in project_sections:
        href = a_tag['href']
        title = a_tag.text.strip()

        # Filter based on presence of '/projects/' or GitHub
        if ('/projects/' in href or 'github.com' in href) and title:
            # Make the link absolute if it's relative
            if href.startswith('/'):
                href = url + href
            programs.append({
                "title": title,
                "link": href
            })

    return programs

# Test the function
if __name__ == "__main__":
    for program in fetch_code4govtech_programs():
        print(f"Title: {program['title']}")
        print(f"Link: {program['link']}")
        print("-" * 40)
