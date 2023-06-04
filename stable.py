import os
from src.utils.sys_utils import mkdirs
from src.utils.json_utils import update_json_values, yaml2json, save_json_data
from src.utils.image_utils import upload_img, download_img
from src.utils.api_call import api_call

class stable:
    def __init__(self, api_call, prompt, image_file=None, init_image=False):
        self.api_call = api_call
        self.prompt = prompt
        self.image_file = image_file
        self.init_image = init_image
        self.in_path = os.environ.get('IN_PATH')
        self.out_path = os.environ.get('OUT_PATH')
        self.api_key = os.environ.get('STABLE_API_KEY')
        self.base_url = f'https://stablediffusionapi.com/api/v3/{self.api_call}'
        self.config_path = os.environ.get('CONFIG_PATH')
        self.config_file_path = os.path.join(self.config_path, 'stable', f'{self.api_call}.yml')

    def process(self):
        image_url = ""
        if self.init_image and self.image_file:
            image_path = os.path.join(self.in_path, 'images', 'init_images', self.image_file)
            image_url = upload_img(image_path)

        data = yaml2json(self.config_file_path)
        update_json_values(data, {'key': self.api_key, 'prompt': self.prompt, 'init_image': image_url})

        response = api_call(self.base_url, data)

        output_base_path = os.path.join(self.out_path, 'stable', str(response["id"]))
        mkdirs([os.path.join(output_base_path, dir) for dir in ['images', 'json']])

        json_files = ['call.json', 'response.json', 'master.json']
        for file_name, content in zip(json_files, [data, response, response]):
            file_path = os.path.join(output_base_path, 'json', f'{response["id"]}_{file_name}')
            save_json_data(content, file_path, append=(file_name == 'master.json'))

        download_img(response["output"], os.path.join(output_base_path, 'images'))