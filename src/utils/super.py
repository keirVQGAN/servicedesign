import requests
import json

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