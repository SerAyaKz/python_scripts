import requests
from collections import Counter
import json

def get_vacancies(query, area_id='40'):
    """
    Fetches vacancy data from the HH.ru API based on the query and area.
    
    Args:
        query (str): The search text for the vacancies (e.g., 'java').
        area_id (str): The region to search in (default is '40' for Kazakhstan).
    
    Returns:
        list: A list of vacancy data (dictionaries) from the API response.
    """
    url = 'https://api.hh.ru/vacancies'
    params = {
        'text': query,
        'area': area_id,
        'host': 'hh.kz',
        'period': 365,
        'resume_search_order': 'publication_time'
    }
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        return data.get('items', [])
    else:
        print(f"Error fetching data: {response.status_code}")
        return []

def extract_skills(vacancies):
    """
    Extracts key skills from a list of vacancies.
    
    Args:
        vacancies (list): List of vacancies as returned from the HH.ru API.
    
    Returns:
        dict: A dictionary mapping each skill to its frequency.
    """
    skill_counter = Counter()
    total_vacancies = len(vacancies)
    
    for vacancy in vacancies:
        vacancy_id = vacancy['id']
        # Get detailed vacancy data
        vacancy_detail_url = f"https://api.hh.ru/vacancies/{vacancy_id}"
        vacancy_detail = requests.get(vacancy_detail_url).json()
        
        # Extract key skills
        key_skills = vacancy_detail.get('key_skills', [])
        skill_names = [skill['name'] for skill in key_skills]
        
        # Update the skill counter
        skill_counter.update(skill_names)
    
    return skill_counter, total_vacancies

def filter_skills_by_freq(skills, total_vacancies, freq_threshold):
    """
    Filters skills that appear in at least freq_threshold percent of vacancies.
    
    Args:
        skills (dict): A dictionary with skills as keys and their frequencies as values.
        total_vacancies (int): The total number of vacancies processed.
        freq_threshold (float): The minimum percentage of vacancies a skill must appear in.
    
    Returns:
        dict: A dictionary with skills filtered by frequency and their relative frequency.
    """
    filtered_skills = {}
    for skill, count in skills.items():
        relative_freq = (count / total_vacancies) * 100
        if relative_freq >= freq_threshold:
            filtered_skills[skill] = relative_freq
    
    # Sort the skills by relative frequency in descending order
    return dict(sorted(filtered_skills.items(), key=lambda item: item[1], reverse=True))

def main(query, freq_threshold=10, area_id='40'):
    """
    Main function that fetches vacancies, processes skills, and filters by frequency.
    
    Args:
        query (str): The search text for vacancies.
        freq_threshold (float): The frequency threshold (in percentage) for filtering skills.
        area_id (str): The region to search in (default is '40' for Kazakhstan).
    
    Returns:
        str: A JSON formatted string with filtered skills and their relative frequencies.
    """
    # Step 1: Get vacancies based on the query
    vacancies = get_vacancies(query, area_id)
    
    # Step 2: Extract skills from the vacancies
    skill_counts, total_vacancies = extract_skills(vacancies)
    
    # Step 3: Filter skills by frequency threshold
    filtered_skills = filter_skills_by_freq(skill_counts, total_vacancies, freq_threshold)
    
    # Convert the result to a JSON-formatted string
    return json.dumps(filtered_skills, indent=4, ensure_ascii=False)

# https://api.hh.ru/openapi/redoc
if __name__ == '__main__':
    query = 'java'  # Replace with any other keyword
    freq_threshold = 10  # Filter skills that appear in at least 10% of the vacancies
    skills_json = main(query, freq_threshold)
    
    # Print the JSON output
    print(skills_json)
