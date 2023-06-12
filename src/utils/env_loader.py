import os
from dotenv import load_dotenv
import shutil

def load_env_file(env_file_path, print_details=True):
    # Copy the .env file to the current directory
    shutil.copy(env_file_path, '.env')

    # Load the environment variables from the .env file
    load_dotenv()

    # Retrieve the values of the environment variables
    environment_variables = [
        'OPENAI_API_KEY',
        'STABLE_API_KEY',
        'UCARE_API_KEY_PUBLIC',
        'UCARE_API_KEY_SECRET',
        'OUT_PATH',
        'IN_PATH',
        'CONFIG_PATH'
    ]

    env_values = {var: os.getenv(var) for var in environment_variables}

    if print_details:
        print('Environment Variables:')
        for var, value in env_values.items():
            print(f'{var}: {value}')

    return env_values

if __name__ == "__main__":
    env_file_path = '/content/drive/MyDrive/oracle/.env'
    env_values = load_env_file(env_file_path)

    # Set variables based on the values in env_values dictionary
    openai_api_key = env_values['OPENAI_API_KEY']
    stable_api_key = env_values['STABLE_API_KEY']
    ucare_api_key_public = env_values['UCARE_API_KEY_PUBLIC']
    ucare_api_key_secret = env_values['UCARE_API_KEY_SECRET']
    out_path = env_values['OUT_PATH']
    in_path = env_values['IN_PATH']
    config_path = env_values['CONFIG_PATH']
