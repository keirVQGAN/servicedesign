import base64
import os
import requests
import json
from datetime import datetime

def upload(folder_path, crop, api_key):
    upload_file_path = os.path.join(folder_path, 'upload.json')

    def read_upload_data():
        if os.path.exists(upload_file_path):
            with open(upload_file_path, 'r') as f:
                return json.load(f)
        return []

    def write_upload_data(upload_data):
        with open(upload_file_path, 'w') as f:
            json.dump(upload_data, f, indent=4)

    def upload_image(file_name):
        with open(os.path.join(folder_path, file_name), "rb") as img_file:
            base64_string = base64.b64encode(img_file.read()).decode()
        response = requests.post(
            "https://stablediffusionapi.com/api/v3/base64_crop",
            headers={'Content-Type': 'application/json'},
            data=json.dumps({
                "key": api_key,
                "image": f"data:image/png;base64,{base64_string}",
                "crop": str(crop).lower()
            })).json()
        return {
            'file_name': file_name,
            'link': response.get('link'),
            'request_id': response.get('request_id'),
            'upload_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

    upload_data = read_upload_data()
    image_files = [
        file_name for file_name in os.listdir(folder_path)
        if file_name.endswith(('.png', '.jpg', '.jpeg'))
           and os.path.getsize(os.path.join(folder_path, file_name)) <= 5 * 1024 * 1024
    ]
    new_upload_data = [
        upload_image(file_name) for file_name in image_files
        if file_name not in [img['file_name'] for img in upload_data]
    ]
    upload_data.extend(new_upload_data)
    write_upload_data(upload_data)

    return [img['link'] for img in new_upload_data]