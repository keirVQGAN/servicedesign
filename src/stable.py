import requests
import yaml
import time

def stable(api_key=None, call=None, prompt=None, init_image=None, mask_image=None):
    if call == 'controlnet':
        url = 'https://stablediffusionapi.com/api/v5/controlnet'
        yaml_file = '/content/config/stable/controlnet.yml'
    else:
        url = f'https://stablediffusionapi.com/api/v3/{call}'
        yaml_file = f'./config/stable/{call}.yml'

    with open(yaml_file, 'r') as f:
        api_options = yaml.safe_load(f)

    api_options.update({
        'prompt': prompt,
        'key': api_key,
        'init_image': init_image or api_options.get('init_image'),
        'mask_image': mask_image or api_options.get('mask_image')
    })

    headers = {"Content-Type": "application/json"}
    response = requests.post(url=url, headers=headers, json=api_options)
    response_data = response.json()

    if response_data.get('status') == 'processing':
        eta = response_data.get('eta', 0)
        time.sleep(max(0, eta - 2))

        while True:
            system_load_response = requests.post('https://stablediffusionapi.com/api/v3/system_load', headers=headers, json={"key": api_key})
            system_load_data = system_load_response.json()

            if system_load_data.get('queue_num') == 0:
                break

            time.sleep(5)

    links = response_data.get('output', 'No link found')

    return response_data, links