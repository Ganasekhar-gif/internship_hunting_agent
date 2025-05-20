import requests
from bs4 import BeautifulSoup

def fetch_internshala_ds_internships():
    url = "https://internshala.com/internships/data%20science-internship"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    internships = []
    for card in soup.find_all('div', class_='internship_meta'):
        title = card.find('a').text.strip()
        link = "https://internshala.com" + card.find('a')['href']
        location = card.find('a', class_='location_link')
        location = location.text.strip() if location else "Not specified"
        
        internships.append({
            'title': title,
            'location': location,
            'link': link
        })

    return internships

# Test the function
if __name__ == "__main__":
    for job in fetch_internshala_ds_internships():
        print(job)
