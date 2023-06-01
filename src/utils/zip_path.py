import os
import zipfile

def zip_path(folder_path: str, output_filename: str, ext: str=None):
    with zipfile.ZipFile(output_filename.rstrip(".zip") + ".zip", 'w') as zipf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                if ext is None or file.endswith(ext):
                    zipf.write(os.path.join(root, file), arcname=os.path.relpath(os.path.join(root, file), folder_path))
