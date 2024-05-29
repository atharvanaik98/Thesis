import vertexai
from pathlib import Path
import urllib
from vertexai.preview.generative_models import GenerativeModel, ChatSession
vertexai.init(project = "simcenter-llm-trial")
def remove_code_fences(text):
    lines = text.split('\n')
    lines = [line for line in lines if not line.strip().startswith('```')]
    return '\n'.join(lines)

here = Path(__file__).parent
context = (here / "Input.txt").read_text()

model = GenerativeModel("gemini-pro")
chat = model.start_chat()
a = "Select all faces with radius less than 10"
b = "Select all faces with radius less than 5 and then select their corresponding edges"
c = "Select circular edges with a radius less than 6 and then select their adjacent edges"
d = "Select all faces in the lower half of the model that have a radius less than 10 that are blends"
e = "Select all faces in the xy plane that have a radius greater than 5mm"
f = "Sort all blends by their z position and then select the last two blends"
g = "Sort all boltholes by their radius and select all boltholes with the second highest radius"
h = "Select all flanges in the model"
i = "Select all struts in the model and then select their leading edges"
j = "Select all strut fillets in the aftmost section of the model"

human = f

chat.send_message(context)
#Input the prompt here
prompt = human

#Generate a response based on the prompt
response = chat.send_message(prompt)

print()
print(response)

print(remove_code_fences(response.text))
