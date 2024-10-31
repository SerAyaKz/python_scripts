import requests
from bs4 import BeautifulSoup
import time

base_url = 'https://www.enbek.kz'
search_url = '/ru/search/vacancy'
query_params = {
    'prof': 'водитель',
    'except[subsidized]': 'subsidized',
    'sort': 'date',
}

def fetch_vacancy_links(page_url):
    response = requests.get(page_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    vacancy_links = [base_url + a['href'] for a in soup.select('a.stretched[href]')]
    return vacancy_links

def fetch_vacancy_details(vacancy_url):
    try:
        response = requests.get(vacancy_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        skills_header = soup.find(string='Профессиональные навыки')
        qualities_header = soup.find(string='Личные качества')

        professional_skills = []
        personal_qualities = []

        if skills_header and skills_header.parent:
            skills_list = skills_header.parent.find_next('ul')
            professional_skills = [li.get_text(strip=True) for li in skills_list.find_all('li')] if skills_list else []

        if qualities_header and qualities_header.parent:
            qualities_list = qualities_header.parent.find_next('ul')
            personal_qualities = [li.get_text(strip=True) for li in qualities_list.find_all('li')] if qualities_list else []

        return {
            'url': vacancy_url,
            'professional_skills': professional_skills,
            'personal_qualities': personal_qualities
        }
    except Exception as e:
        print(f"Error processing {vacancy_url}: {e}")
        return None

def main():
    results = []
    page_number = 1
    while True:
        page_url = f"{base_url}{search_url}?page={page_number}&" + "&".join(f"{k}={v}" for k, v in query_params.items())
        vacancy_links = fetch_vacancy_links(page_url)
        if not vacancy_links or page_number == 3:
            break  
        for link in vacancy_links:
            details = fetch_vacancy_details(link)
            if details:
                results.append(details)
            time.sleep(1)  
        
        page_number += 1
        time.sleep(2)  

    return results

if __name__ == '__main__':
    vacancy_data = main()
    print(vacancy_data)
