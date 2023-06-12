import os
import requests
import json
from pyuploadcare import Uploadcare, File


def super(key, img_url, scale, face_enhance):
    api_url = "https://stablediffusionapi.com/api/v3/super_resolution"
    payload = json.dumps({
        "key": key,
        "url": img_url,
        "scale": scale,
        "webhook": None,
        "face_enhance": face_enhance
    })

    response = requests.post(api_url, headers={'Content-Type': 'application/json'}, data=payload)
    response_data = response.json()

    link = response_data.get('output', 'No link found')

    return response_data, link

  
def upload_img(img_path):
  public_key = os.environ.get('UCARE_API_KEY_PUBLIC')
  secret_key = os.environ.get('UCARE_API_KEY_SECRET')
  uploadcare = Uploadcare(public_key, secret_key)
  with open(img_path, 'rb') as file_object:
      ucare_file = uploadcare.upload(file_object)
  return ucare_file


def download_img(url, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    response = requests.get(url, stream=True)

    if response.status_code == 200:
        with open(path, 'wb') as f:
            response.raw.decode_content = True
            shutil.copyfileobj(response.raw, f)
    else:
        print(f"Error downloading image: {response.status_code} - {response.text}")
