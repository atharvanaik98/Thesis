import yaml
import vertexai
import requests
from pathlib import Path
from vertexai.preview.generative_models import GenerativeModel, Image

#initiate the vertex AI with project ID 
vertexai.init(project = "totemic-veld-412608")

#function definition to remove code fences from the printed output 
def remove_code_fences(text):
    lines = text.split('\n')
    lines = [line for line in lines if not line.strip().startswith('```')]
    return '\n'.join(lines)

#parent path definition
here = Path(__file__).parent

#Append the contents of the input file to a variable named context
context = (here / "Input.txt").read_text()
 
#provide the model with the image that needs to be analysed.
image_file = (here / "exhaust_case.jpg")
image = Image.load_from_file(image_file)

#select the generative model 
model = GenerativeModel("gemini-1.0-pro-vision")

#initiate interactive chat environment 
chat = model.start_chat()

#generate model config. Higher temperature prompts the model to generate more creative content. 
config = {
    "temperature": 0.0,
    "top_p": 1.0,
    "top_k": 20.0,
    "max_output_tokens": 200,
}

#Input the prompt here
while True: 
    prompt = input("Enter the description of the geometry you want to select: ")
    if prompt == str('cancel'):
        break 
    else: 
    #Generate a response based on the prompt
        response = model.generate_content([image, context, prompt], generation_config=config)

        print()
        #print model response
        print(response.text)

        response = response.text
        appendtoyaml(filepath, response)


