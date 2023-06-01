import os
import shutil

def zip_folder(directory_path: str, output_filename: str):
    if os.path.exists(directory_path):
        shutil.make_archive(output_filename.rstrip(".zip"), 'zip', directory_path)
