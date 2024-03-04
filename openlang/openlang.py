# Import necessary packages
from langchain_openai import OpenAI
from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate
from langchain_openai import ChatOpenAI
from pathlib import Path
from langchain_core.output_parsers import StrOutputParser

# Function definitions

#function to call a path to the file and read it. 
def context_gen(file_name):
    Folder = "VertexLang"
    here = Path(locals().get('__file__', Folder)).resolve()
    parameter = (here / file_name).read_text()
    return parameter

#remove code fences from the output
def remove_code_fences(text):
    lines = text.split("\n")
    lines = [line for line in lines if not line.strip().startswith('```')]
    lines[0] = lines[0].replace(' -', '-', 1)
    return "\n".join(lines)

#invoke and run the model with the given prompt
def test_openai(few_shot_prompt):
    generate = ChatPromptTemplate.from_messages([("system", system), few_shot_prompt, ("human", human),])
    chat = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.5)
    #select an output parser
    output_parser = StrOutputParser()
    chain = generate | chat | output_parser
    result = chain.invoke({}, {"tags": ["loop 001"]})
    print(remove_code_fences(result))
    print()
    return

#Inputs to the model

#create inputs to the model, telling it what needs to be done. 
#provides system message
system = context_gen("systemmsg.txt")

#provides the few shot examples
output_examples = context_gen("outputex.txt")

#provides the input examples
input_examples = context_gen("inputex.txt")

#provides the database schema
schema = context_gen("dataBaseSchema.txt")

'''change the human variable to test different inputs'''
human = ("select the blend in the xz plane between the angle 45 and 90 and then select the connected blend")


# Few shot prompts example template 
examples = [
    {"input": input_examples, "output": output_examples},
]

example_prompt = ChatPromptTemplate.from_messages([
    ("human", "{input}"),
    ("ai", "{output}"),
]
)

few_shot_prompt = FewShotChatMessagePromptTemplate(
    example_prompt=example_prompt,
    examples=examples,
)

'''Function call to run the model'''
test_openai(few_shot_prompt)


