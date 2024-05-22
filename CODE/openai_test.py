# %%
from openai import OpenAI 
from pathlib import Path

client = OpenAI()
def remove_code_fences(text):
    lines = text.split('\n')
    lines = [line for line in lines if not line.strip().startswith('```')]
    return '\n'.join(lines)

file_path = "C:\\tools\\git\\Thesis\\CODE\\Input.txt"
text = Path(file_path).read_text()

# Print the contents of the text file


def test_openai(human):
    completion = client.chat.completions.create(model = "gpt-3.5-turbo", messages = [
        {"role": "system", "content": text},
        {"role": "user", "content": str(human)}
    ]
        )
    print(remove_code_fences(completion.choices[0].message.content))
    return

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

human = a
test_openai(human)


