from .config import celery_app
from app.core.config import settings
import requests
from bs4 import BeautifulSoup

@celery_app.task
def fetch_filtered_data(visa_code):
    url = settings.GET_OCCUPATION_URL
    session = requests.Session()
    response = session.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    table = soup.find('table', class_='table-hover')
    data = []
    for row in table.find_all('tr'):
        cols = row.find_all('td')
        data.append([ele.text.strip() for ele in cols if ele])
    
    # filtered_data = soup.find_all(lambda tag: tag.name == "div" and str(visa_code) in tag.text)
    
    # data = [data.text for data in filtered_data]
    with open(f'data_visa_{visa_code}.txt', 'w') as f:
        for item in data:
            f.write(f"{item}\n")
    
    return f"Data fetched for visa {visa_code}"
