from docx import Document
import os


def docx2txt(docx_path):
    doc = Document(docx_path)
    text = '\n'.join([paragraph.text for paragraph in doc.paragraphs])
    txt_path = os.path.splitext(docx_path)[0] + '.txt'

    with open(txt_path, 'w') as txt_file:
        txt_file.write(text)

    return txt_path
