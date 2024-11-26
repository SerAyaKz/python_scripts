import requests
import json

# API URL for the initial query
api_url = 'https://epvo.kz/api/rep/publication/applications'

# JSON payload for the initial request
payload = {
    "size": 30,
    "totalElements": 0,
    "totalPages": 0,
    "pageNumber": 0,
    "filter": {
        "repView": 1,
        "appStatuses": ["INCLUDED", "UPDATED"],
        "status": "APPROVED",
        "searchText": "Радиология",
        "actual": True,
        "actualUpdated": False,
        "applicationOfHrTraining": 1,
        "universityStatus": "ACTIVE",
        "langId": 2
    }
}

# Headers
headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'User-Agent': 'Mozilla/5.0'
}

# Send POST request
response = requests.post(api_url, headers=headers, json=payload)

# Initialize a list to store the details for each ID
all_details = []

# Check response status code
if response.status_code == 200:
    # Parse JSON response
    initial_data = response.json()
    print("Initial data fetched successfully!")

    # Extract IDs from the response data
    if 'dtoList' in initial_data:
        ids = [item['id'] for item in initial_data['dtoList']]
        # Base URL for fetching details for each ID
        details_url = 'https://epvo.kz/api/rep/publication/application/'

        # Loop over each ID and fetch details
        for id in ids:
            detail_response = requests.get(details_url + str(id), headers=headers)
            if detail_response.status_code == 200:
                detail_data = detail_response.json()
                all_details.append(detail_data)
            else:
                print(f"Failed to fetch details for ID {id}: Status Code {detail_response.status_code}")
    else:
        print("No 'dtoList' key found in the response")
else:
    print("Failed to fetch initial data: Status Code", response.status_code)

# After collecting all data, print the accumulated details
print("All fetched details:")
print(json.dumps(all_details, indent=4, ensure_ascii=False))
