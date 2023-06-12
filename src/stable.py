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

    try:
        response_data = response.json()
    except json.JSONDecodeError:
        print(f"Failed to parse JSON from response. Status code: {response.status_code}, Response text: {response.text}")
        return None

    return response_data
