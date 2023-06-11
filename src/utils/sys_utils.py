import os
from pathlib import Path
from docx import Document
import zipfile


def docx2txt(docx_path):
    doc = Document(docx_path)
    text = '\n'.join([paragraph.text for paragraph in doc.paragraphs])
    txt_path = os.path.splitext(docx_path)[0] + '.txt'

    with open(txt_path, 'w') as txt_file:
        txt_file.write(text)

    return txt_path


def path2ls(folder_path, ext=''):
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
    

def zip_path(folder_path: str, output_filename: str, ext: str=None):
    with zipfile.ZipFile(output_filename.rstrip(".zip") + ".zip", 'w') as zipf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                if ext is None or file.endswith(ext):
                    zipf.write(os.path.join(root, file), arcname=os.path.relpath(os.path.join(root, file), folder_path))
    
