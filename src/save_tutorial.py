import json
import os

def save_tutorial(response, student):

    folder_name = f'./output/tutorials/{student}'
    file_name = f'{folder_name}/{student}.json'
    # Load existing data or create an empty list
    try:
        with open(file_name, 'r') as file:
            existing_data = json.load(file)
            if not isinstance(existing_data, list):
                existing_data = []
    except (FileNotFoundError, json.JSONDecodeError):
        existing_data = []

    # Append response and save to json file
    existing_data.append(response)
    with open(file_name, 'w') as file:
        json.dump(existing_data, file, indent=4)

    # Save response text to txt file
    response_text = response['response']
    with open(f'{folder_name}/{student}.txt', 'w') as file:
        file.write(response_text)

    # Append response and student data to master_tutorials.json
    master_file = './output/tutorials/master_tutorials.json'

    try:
        with open(master_file, 'r') as file:
            master_data = json.load(file)
            if not isinstance(master_data, list):
                master_data = []
    except (FileNotFoundError, json.JSONDecodeError):
        master_data = []

    master_data.append({'student': student, 'response': response})
    with open(master_file, 'w') as file:
        json.dump(master_data, file, indent=4)
