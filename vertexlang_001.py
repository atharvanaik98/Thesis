# Import necessary packages
from langchain_google_vertexai import ChatVertexAI
from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate
from pathlib import Path
from langchain_core.output_parsers import StrOutputParser
import vertexai
# Function definitions

#function to call a path to the file and read it. 
def context_gen(file_name):
    '''uses pathlib to pull files from the cloned repo and read them'''
    Folder = "VertexLang"
    here = Path(locals().get('__file__', Folder)).resolve()
    parameter = (here / file_name).read_text()
    return parameter

#remove code fences from the output
def remove_code_fences(text):
    '''Removes code fences from the output.'''
    lines = text.split("\n")
    lines = [line for line in lines if not line.strip().startswith('```')]
    
    #Gets rid of first space empty space before the -filter line
    lines[0] = lines[0].replace(' -', '-', 1)
    return "\n".join(lines)

#invoke and run the model with the given prompt
def test_vertexai(few_shot_prompt):
    '''Generate creates the prompt template, chat selects the model, and output_parser selects the output parser. Chain is the sequence of the model and the output parser. Result is the output of the model.'''
    
    #create prompt template
    generate = ChatPromptTemplate.from_messages([("system", system), few_shot_prompt, ("human", human),])
    
    #selects vertexAI through langchain, can be changed to openAI or any other model
    chat = ChatVertexAI(model_name="gemini-pro", temperature=0.5, convert_system_message_to_human=True)
    
    #select an output parser
    output_parser = StrOutputParser()
    
    #chain definition
    chain = generate | chat | output_parser
    result = chain.invoke({}, {"tags": ["loop 001"]})
    print(remove_code_fences(result))
    print()
    return

#create inputs to the model, telling it what needs to be done. 

#provides system message
system = context_gen("systemmsg.txt")

#provides the few shot examples
output_examples = context_gen("outputex.txt")

#provides the input examples
input_examples = context_gen("inputex.txt")

#provides the database schema
schema = context_gen("dataBaseSchema.txt")

#uses this input to generate the actual response
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
vertexai.init(project="simcenter-llm-trials")

while True:
    try:
        test_vertexai(few_shot_prompt)
    except 

