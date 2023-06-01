import json
from datetime import datetime
import requests
from pathlib import Path


def save(response, output_folder):
    # Ensure output_folder is a Path object
    output_folder = Path(output_folder)
    output_folder.mkdir(parents=True, exist_ok=True)

    # Add the date and time to the response
    response['date_time'] = datetime.now().isoformat()

    # Save the response to a JSON file
    with (output_folder / 'response.json').open('w') as f:
        json.dump(response, f, indent=4)

    # Append the response to a master JSON file
    with (output_folder / 'master.json').open('a') as f:
        json.dump(response, f, indent=4)
        f.write('\n')

    # Save any images linked in the 'output' key of the response
    image_folder = output_folder / 'images'
    image_folder.mkdir(parents=True, exist_ok=True)

    image_urls = response.get('output', [])
    if isinstance(image_urls, str):
        image_urls = [image_urls]

    for url in image_urls:
        img_response = requests.get(url)
        filename = f"{response.get('id', 'image')}.jpg"
        prefix = 1
        while (image_folder / filename).exists():
            filename = f"{prefix}_{filename}"
            prefix += 1
        with (image_folder / filename).open('wb') as f:
            f.write(img_response.content)