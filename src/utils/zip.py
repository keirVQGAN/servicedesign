import os
import shutil

def zip(directory_path: str, output_filename: str):
    if os.path.exists(directory_path):
        shutil.make_archive(output_filename if output_filename.endswith(".zip") else output_filename + ".zip", 'zip', directory_path)
