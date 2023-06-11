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


def download_img(image_urls, folder_path):
    os.makedirs(folder_path, exist_ok=True)
    print(f'Downloading images to {folder_path}')
    # If a single URL is provided, wrap it in a list
    if isinstance(image_urls, str):
        image_urls = [image_urls]
    
    for url in image_urls:
        try:
            response = requests.get(url)
            response.raise_for_status()
            filename = url.rsplit('/', 1)[-1]
            image_path = os.path.join(folder_path, filename)
            with open(image_path, 'wb') as file:
                file.write(response.content)
            print(f"Downloaded: {filename}")
        except requests.HTTPError as e:
            print(f"Failed to download: {url} - {e}")
        except Exception as e:
            print(f"Error occurred while downloading: {url} - {e}")
