import os
import requests
from pyuploadcare import Uploadcare, File

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
