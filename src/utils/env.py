import os
from dotenv import load_dotenv
import shutil

def env_loader(env_file_path, print_details=True):
    # Copy the .env file to the current directory
    shutil.copy(env_file_path, '.env')

    # Load the environment variables from the .env file
    load_dotenv()

    # Retrieve the values of the environment variables
    openai_api_key = os.getenv('OPENAI_API_KEY')
    stable_api_key = os.getenv('STABLE_API_KEY')
    ucare_public = os.getenv('UCARE_API_KEY_PUBLIC')
    ucare_secret = os.getenv('UCARE_API_KEY_SECRET')
    out_path = os.getenv('OUT_PATH')
    in_path = os.getenv('IN_PATH')
    config_path = os.getenv('CONFIG_PATH')

    if print_details:
        print('Environment Variables:')
        print(f'OPENAI_API_KEY: {openai_api_key}')
        print(f'STABLE_API_KEY: {stable_api_key}')
        print(f'UCARE_API_KEY_PUBLIC: {ucare_public}')
        print(f'UCARE_API_KEY_SECRET: {ucare_secret}')
        print(f'OUT_PATH: {out_path}')
        print(f'IN_PATH: {in_path}')
        print(f'CONFIG_PATH: {config_path}')

    return openai_api_key, stable_api_key, ucare_public, ucare_secret, out_path, in_path, config_path
