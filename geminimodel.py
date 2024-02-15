from cgitb import text
import vertexai
import requests
from vertexai.preview.generative_models import GenerativeModel, ChatSession
from pathlib import Path
import yaml

def remove_code_fences(text):
    lines = text.split('\n')
    lines = [line for line in lines if not line.strip().startswith('```')]
    return '\n'.join(lines)

#Initiate vertexai project
vertexai.init(project = "totemic-veld-412608")


here = Path(__file__).parent
context = (here / "Input.txt").read_text()
filepath = (here / "query.txt")

model = GenerativeModel("gemini-pro")
chat = model.start_chat()

#push context to model
chat.send_message(context)

#Input the prompt here
prompt = input("Enter the description of the geometry you want to select: ")

#Generate a response based on the prompt
response = chat.send_message(prompt)

#print response based on prompt and context. 
print()
print(remove_code_fences(response.text))

with open (filepath, 'w') as text_file:
    text_file.write(response.text)
    text_file.close()

