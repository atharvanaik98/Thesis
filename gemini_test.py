import vertexai
from pathlib import Path
import urllib
from vertexai.preview.generative_models import GenerativeModel, ChatSession
vertexai.init(project = "totemic-veld-412608")
def remove_code_fences(text):
    lines = text.split('\n')
    lines = [line for line in lines if not line.strip().startswith('```')]
    return '\n'.join(lines)

here = Path(__file__).parent
context = (here / "Input.txt").read_text()

model = GenerativeModel("gemini-pro")
chat = model.start_chat()

chat.send_message(context)
#Input the prompt here
prompt = input("Enter the description of the geometry you want to select: ")

#Generate a response based on the prompt
response = chat.send_message(prompt)

print()
print(remove_code_fences(response.text))
