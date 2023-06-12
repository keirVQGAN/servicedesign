#@title `response_processor.py`

from src.utils.json_utils import write_to_json, append_to_json, calculate_eta

from src.utils.sys_utils import mkdirs

import datetime, os, json

class ResponseProcessor:
    def __init__(self, response):
        self.response = response
        self.status = response['status']

    def process(self):
        self.process_success_status()
        if self.status == 'processing':
            return self.process_processing_status()
        elif self.status in ['error', 'failed']:
            return self.process_error_response()
        else:
            return "Invalid status", self.response, None

    def process_processing_status(self):
        directory = './output/images/json/'
        mkdirs(directory)

        keys = ['eta', 'fetch_result', 'id']
        processing_data = {key: self.response[key] for key in keys if key in self.response}
        processing_data['available'] = calculate_eta(self.response['eta'])

        append_to_json(processing_data, os.path.join(directory, 'processing.json'))

        return self.response['status'], self.response, os.path.join(directory, 'processing.json')

    def process_success_status(self):
        id_directory = f'./output/images/{self.response["id"]}/json/'
        master_directory = './output/images/json/'
        mkdirs(id_directory)
        mkdirs(master_directory)

        self.response['date_time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        write_to_json(self.response, os.path.join(id_directory, f'{self.response["id"]}.json'))
        append_to_json(self.response, os.path.join(master_directory, 'master.json'))

        return self.response['status'], self.response, os.path.join(id_directory, f'{self.response["id"]}.json')

    def process_error_response(self):
        status = self.response['status']
        message = self.response.get('message', '')
        tips = self.response.get('tips', '')

        print(f"Error: {status}")
        print(f"Message: {message}")
        print(f"Tips: {tips}")

        return status, self.response, None
