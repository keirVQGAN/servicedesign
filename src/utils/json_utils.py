import os
import json
import yaml
from datetime import datetime
import re


def write_to_json(data, path):
    with open(path, 'w') as f:
        json.dump(data, f)

        
def append_to_json(data, path):
    with open(path, 'a') as f:
        json.dump(data, f)

        
def yaml2json(yaml_file):
    with open(yaml_file, 'r') as file:
        yaml_dict = yaml.safe_load(file)

    return yaml_dict


def get_json_value(input_data, key):
    if isinstance(input_data, str):  # Check if input_data is a string (assumed to be file path)
        with open(input_data, 'r') as file:
            data = json.load(file)
    elif isinstance(input_data, dict):  # Check if input_data is a dictionary
        data = input_data
    else:
        raise TypeError('Input data should be either a file path (string) or a dictionary.')

    return data.get(key)


def update_json_values(dictionary, updates):
    for key, new_value in updates.items():
        if key in dictionary:
            dictionary[key] = new_value
        else:
            return None
    return dictionary


def find_json_values(json_path_or_file, key):
    values = []

    def extract_values(obj, api_key):
        if isinstance(obj, dict):
            for k, v in obj.items():
                if k == api_key:
                    values.append(v)
                elif isinstance(v, (dict, list)):
                    extract_values(v, api_key)
        elif isinstance(obj, list):
            for item in obj:
                extract_values(item, api_key)

    if os.path.isfile(json_path_or_file):
        # It's a file
        with open(json_path_or_file, 'r') as f:
            try:
                data = json.load(f)
                extract_values(data, key)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error reading JSON from file {json_path_or_file}: {e}")
    elif os.path.isdir(json_path_or_file):
        # It's a directory
        for root, dirs, files in os.walk(json_path_or_file):
            for file in files:
                if file.endswith('.json'):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r') as f:
                        try:
                            data = json.load(f)
                            extract_values(data, key)
                        except (json.JSONDecodeError, IOError) as e:
                            print(f"Error reading JSON from file {file_path}: {e}")
    else:
        raise ValueError("The provided path does not exist or is not a file or directory.")

    return values


def save_json_data(data, filename, append=False, indent=4):
    try:
        data = [{'data': d, 'timestamp': datetime.now().isoformat()} for d in
                (data if isinstance(data, list) else [data])]
    except TypeError as e:
        raise TypeError("'data' must be a dictionary or a list of dictionaries.") from e

    if not append and os.path.exists(filename):
        base, ext = os.path.splitext(filename)
        match = re.match(r'(.*?)(\d+)$', base)
        if match:
            base, num = match.groups()
            num = int(num)
        else:
            num = 0
        filename = f"{base}{num}{ext}"
        while os.path.exists(filename):
            num += 1
            filename = f"{base}_{num}{ext}"

    existing = []

    if append and os.path.exists(filename) and os.path.getsize(filename) > 0:
        try:
            with open(filename, 'r') as f:
                existing = json.load(f)['data']
        except (IOError, ValueError) as e:
            raise IOError("Error reading from file.") from e

    data = [d for d in data if d not in existing]

    if existing:
        print('Dictionary already exists in json file.')
        data = existing + data  # Merge existing and new data

    try:
        with open(filename, 'w') as f:
            json.dump({'last_updated': datetime.now().isoformat(), 'data': data}, f, indent=indent)
    except IOError as e:
        raise IOError("Error writing to file.") from e
        
