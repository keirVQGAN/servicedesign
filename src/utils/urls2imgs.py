import os
import requests

def download_images(url_list, save_dir='./output/images/downloaded'):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    for i, url in enumerate(url_list):
        response = requests.get(url, stream=True)
        
        # check the response status
        if response.status_code == 200:
            # Open a local file with wb (write binary) permission.
            with open(os.path.join(save_dir, 'image'+str(i)+'.png'), 'wb') as f:
                for chunk in response.iter_content(1024):
                    if chunk:
                        f.write(chunk)
        else:
            print('Failed to download image at url', url)
