import vertexai
import requests
from vertexai.preview.generative_models import GenerativeModel, ChatSession
vertexai.init(project = "totemic-veld-412608")

def remove_code_fences(text):
    lines = text.split('\n')
    lines = [line for line in lines if not line.strip().startswith('```')]
    return '\n'.join(lines)

repor_url = "https://raw.githubusercontent.com/firestorm98/Thesis/main/Input.txt"
TOKEN = "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"
headers = {
    "authorization": f"token {TOKEN}", 
    "Accept": "text/plain"

}
context = requests.get(repor_url, headers=headers)

model = GenerativeModel("gemini-pro")
chat = model.start_chat()

context = context.text
chat.send_message(context)

#Input the prompt here
prompt = input("Enter the description of the geometry you want to select: ")

    #Generate a response based on the prompt
response = chat.send_message(prompt)

print()
print(remove_code_fences(response.text))