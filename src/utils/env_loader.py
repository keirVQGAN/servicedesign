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
