import gradio as gr
import json
import yaml
import os
import openai
import time
from src.utils.txt2str import txt2str

openai.api_key = os.getenv('OPENAI_API_KEY')

def chatoracle(openai_key=None, system_prompt_file='./config/oracle/system_prompt.txt',
               yml_file='./config/chatbot/config_chat.yml'):
    system_prompt = txt2str(system_prompt_file) or load_system_prompt(yml_file)
    messages = [{"role": "system", "content": system_prompt}]
    questions_counter = 0

    def get_prompt(user_input):
        context = messages.copy()
        context.append({"role": "user", "content": user_input})
        return context

    def create_chat_completion(user_input):
        completion = openai.ChatCompletion.create(
            model="gpt-4",
            messages=get_prompt(user_input),
        )
        messages.append({"role": "assistant", "content": completion.choices[0].message.content})
        return completion.choices[0].message.content

    def save_chat_history_and_response(response):
        with open('chat_history.json', 'w') as f:
            json.dump(messages, f, indent=4)
        with open('final_response.txt', 'w') as f:
            f.write(response)

    def user(user_message, history):
        nonlocal questions_counter
        questions_counter += 1
        return "", history + [[user_message, None]]

    def bot(history):
        nonlocal questions_counter
        user_message = history[-1][0]
        completion = create_chat_completion(user_message)
        ai_message = completion.strip()

        history[-1][1] = ai_message

        if questions_counter == 4:  # Save after 3rd user question and the assistant's response
            save_chat_history_and_response(ai_message)

        for _ in ai_message:
            time.sleep(0.05)
            yield history

    with gr.Blocks(theme=gr.themes.Monochrome(), title="Oracle of All Beings") as demo:
        chatbot = gr.Chatbot()
        msg = gr.Textbox(placeholder="Please Press Enter To Begin...")
        clear = gr.Button("Clear")

        msg.submit(user, [msg, chatbot], [msg, chatbot], queue=False).then(
            bot, chatbot, chatbot
        )
        clear.click(lambda: None, None, chatbot, queue=False)

    demo.queue()
    demo.launch(share=True, debug=True)


def load_system_prompt(yml_file):
    with open(yml_file, 'r') as file:
        data = yaml.safe_load(file)
        return data['messages'][0]['content']


if __name__ == "__main__":
    openai_api_key = os.environ.get('OPENAI_API_KEY')
   

    chatoracle()
