import os
from pathlib import Path


def path2ls(folder_path, ext='.*'):
    file_names = []
    for file in os.listdir(folder_path):
        if file.endswith(ext):
            file_name = os.path.splitext(file)[0]
            file_names.append(file_name)
    return file_names
  

def mkdirs(folders):
  for output_folder in folders:
    output_folder = Path(output_folder)
    output_folder.mkdir(parents=True, exist_ok=True)
    
