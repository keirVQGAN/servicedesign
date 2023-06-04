import requests, json, os

def api_call(url, data):
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, json=data, headers=headers) if data else requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()  # Assuming the API returns JSON data
    else:
        print(f"API call failed with status code: {response.status_code}")
        return None
