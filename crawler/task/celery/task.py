from . import celery
from app.core.config import settings
from bs4 import BeautifulSoup
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from app.core.config import settings



chrome_options = Options()  


@celery.task
def fetch_filtered_data(visa_code):
    url = settings.GET_OCCUPATION_URL
    html: str
    with Chrome(options=chrome_options) as browser:
        browser.get(url)
        html = browser.page_source
    
    soup = BeautifulSoup(html, 'html.parser')
    
    table = soup.find('table', class_='table-hover')
    
    data = []
    for row in table.find_all('tr'):
        cols = row.find_all('td')
        row = [ele.text.strip() for ele in cols if ele.text.strip() != 'undefined']
        
        
        if len(row) > 0 and contains_all_strings(row[2], visa_code):
            print("==================")
            print(row[2])
            print(visa_code)
            print("==================")

            data.append(row)
    
    
    with open(f'data_visa_{visa_code}.txt', 'w') as f:
        for item in data:
            f.write(f"{item}\n")
    
    return f"Data fetched for visa {visa_code}"


def contains_all_strings(text: str, filters: str):
    string_array = filters.split(" ")
    return all(substring.upper() in text.upper() for substring in string_array)
