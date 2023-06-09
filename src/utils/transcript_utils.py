from docx import Document
from docx.shared import Pt
from pathlib import Path

def txt2docx(input_path):
    for txt_file in Path(input_path).rglob('*.txt'):
        if 'clean' in txt_file.name: continue

        docx_file = txt_file.with_suffix('.docx')
        document = Document()

        for i, line in enumerate(txt_file.read_text().strip().split('\n')):
            line = line.strip()
            if not line: continue

            p = document.add_paragraph()
            run = p.add_run(line[:-1] if line.endswith(':') else line)

            run.bold = line.endswith(':') or i == 0  # set bold if it's first line or ends with ':'
            run.font.name = 'Arial'
            run.font.size = Pt(12) if run.bold else Pt(10)
            p.paragraph_format.space_after = Pt(6)

        document.save(docx_file)

txt2docx('/content/servicedesign/output/tutorials')
