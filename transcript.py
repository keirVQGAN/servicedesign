import os
import shutil
from src.utils.path2ls import path2ls
from src.utils.clean_text import clean_text
from src.utils.docx2txt import docx2txt
from src.chatbot import chatbot
from src.save_tutorial import save_tutorial
from src.utils.zip_path import zip_path


def read_prompts(file_path):
    with open(file_path, 'r') as f:
        prompts = f.readlines()
    return prompts


def transcript(openai_key, call='tutorial', prompts_file='./config/transcripts/transcript_prompts.txt'):
    transcripts_path = './inputs/tutorials/transcripts'
    students = path2ls(transcripts_path, '.docx')
    prompts = read_prompts(prompts_file)

    for student in students:
        docx_path = f'{transcripts_path}/{student}.docx'
        input_text = docx2txt(docx_path)
        folder_path = f'./output/tutorials/{student}'
        os.makedirs(folder_path, exist_ok=True)
        output = f'{folder_path}/{student}_clean.txt'
        shutil.copy(docx_path, folder_path)

        text = clean_text(input_text, output, student)
        system_prompt = prompts[0].format(student=student, text=text)
        user_message = prompts[1].format(student=student, text=text)

        count_tokens = False
        chat = False
        print('Summarising Tutorial with {student}')
        response = chatbot(openai_key, system_prompt, user_message, count_tokens, chat)
        save_tutorial(response, student)
        print(f'Tutorial with {student} summarised successfully')

    outpath_zip = '/content/servicedesign/output/tutorials'
    outpath_zipfile = f'{outpath_zip}/tutorial_summaries'
    zip_path(outpath_zip, outpath_zipfile, '.txt')
    print(f'All transcripts summarised and saved to {outpath_zipfile}')

