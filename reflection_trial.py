from langchain_openai import OpenAI
from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from pathlib import Path
from langchain_core.output_parsers import StrOutputParser

def context_gen(file_name):
    Folder = "VertexLang"
    here = Path(locals().get('__file__', Folder)).resolve()
    parameter = (here / file_name).read_text()
    return parameter

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

prompt = ChatPromptTemplate.from_messages([("system", system), few_shot_prompt, MessagesPlaceholder(variable_name="messages"),])
chat = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.5)
chain = prompt | chat

yaml = ""
request = HumanMessage(content = human)
for chunk in chain.stream({"messages": [request]}):
    print(chunk.content, end="")
    yaml += chunk.content
    