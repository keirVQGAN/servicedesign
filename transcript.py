import os, shutil
from src.utils.path2ls import path2ls
from src.utils.clean_text import clean_text
from src.utils.docx2txt import docx2txt
from src.chatbot import chatbot
from src.save_tutorial import save_tutorial
from src.utils.zip_path import zip_path


def transcript(openai_key, call='tutorial'):
    transcripts_path = './inputs/tutorials/transcripts'
    students = path2ls(transcripts_path, '.docx')
    for student in students:
        docx_path = f'{transcripts_path}/{student}.docx'
        input = docx2txt(docx_path)
        folder_path = f'./output/tutorials/{student}'
        os.makedirs(folder_path, exist_ok=True)
        output = f'{folder_path}/{student}_clean.txt'
        shutil.copy(docx_path, folder_path)

        text = clean_text(input, output, student)
        if call == 'tutorial':
            system_prompt = f"Generate a detailed summary (Project Proposal tutorial auto-summary for a student {student} with tutor Dr Keir Williams) of a Service Design MA tutorial transcript. Begin with a summary of the conversation, followed by key points, insights from the tutor, potential challenges, connections to relevant theories, recommendations for further readings, resources mentioned, research questions with sub-questions, actionable steps for a final design-based research project proposal, reflections on progress, and areas for improvement. Provide a brief overview on using the document and note potential inaccuracies due to GPT-4 LLM generation."
            user_message = f"Provide a detailed summary (Project Proposal tutorial auto-summary for a student {student} with tutor Dr Keir Williams) of the tutorial transcript {text}. Start with a summary of the conversation, then include key points, insights from the tutor, potential challenges, connections to relevant theories, recommendations for further readings, resources mentioned, research questions, sub-questions, actionable steps for a final design-based research project proposal, reflections on progress, areas for improvement, a brief usage overview, and a note on GPT-4 LLM-generated content."

        if call == 'meeting':
            system_prompt = f"Summarize the work meeting between Keir Williams and a colleague called {student}. Provide the meeting's title, an overview, key points, and actions for both attendees."
            user_message = f"Summarize the meeting transcript {text}. Include the title, an overview, key points, and actions for Keir Williams and the other attendee."

        count_tokens = False
        chat = False

        response = chatbot(openai_key, system_prompt, user_message, count_tokens, chat)
        save_tutorial(response, student)
        print(f'Tutorial with {student} summarised successfully')
        outpath_zip = './output/tutorials'
    zip_path(outpath_zip, f'{output_zip}/tutorial_summaries')
    print(f'All transcripts summarised and saved to zip')
