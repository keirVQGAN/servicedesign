import openai
import tiktoken
import json
def chatbot(openai_key, system_prompt, user_message=None, count_tokens=False, chat=True):
    enc = tiktoken.get_encoding("cl100k_base")
    openai.api_key = openai_key
    messages = [{"role": "system", "content": system_prompt}]

    def get_prompt(input):
        context = list(messages)
        context.append({"role": "user", "content": input})
        return context

    def create_chat_completion(input):
        completion = openai.ChatCompletion.create(
            model="gpt-4",
            messages=get_prompt(input),
        )
        messages.append({"role": "assistant", "content": completion.choices[0].message.content})
        return completion.choices[0].message.content

    def count_used_tokens():
        token_count = len(enc.encode(" ".join([msg["content"] for msg in messages])))
        token_cost = token_count / 1000 * 0.002 # gpt-3.5-turbo cost
        return "🟡 Used tokens this round: " + str(token_count) + " (" + format(token_cost, '.5f') + " USD)"

    if chat:
        while True:
            user_input = input("You: ")

            if user_input.lower() == '**end':
                print("End of the chat.")
                return messages
            elif user_input.lower() == '**save':
                with open('chat_history.json', 'w') as f:
                    json.dump(messages, f, indent=4)
                print("Conversation history saved as 'chat_history.json'.")
                continue

            completion = create_chat_completion(user_input)
            print("Bot:", completion)
            if count_tokens:
                print(count_used_tokens())
    else:
        if user_message is None:
            raise ValueError("user_message must be provided when chatbot is set to False")
        completion = create_chat_completion(user_message)
        if count_tokens:
            print(count_used_tokens())
        return {'response': completion, 'token_usage': count_used_tokens()}
