# %% [markdown]
# Import necessary packages

# %%
from langchain_openai import OpenAI
from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate, MessagesPlaceholder, PromptTemplate
from langchain_openai import ChatOpenAI
from pathlib import Path
from langchain_core.output_parsers import StrOutputParser
from langchain.output_parsers import PydanticToolsParser, YamlOutputParser
import datetime
from typing import Literal, Optional, Tuple
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from langchain.globals import set_debug
from typing import List, Sequence
from langgraph.graph import MessageGraph, END


# %% [markdown]
# Function definitions

# %%
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
    print()
    return "\n".join(lines)

#invoke and run the model with the given prompt
def test_vertexai(few_shot_prompt):
    generate = ChatPromptTemplate.from_messages([("system", system), few_shot_prompt, ("human", human), ("ai", someoutput)])
    chat = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.5)
    #select an output parser
    output_parser = StrOutputParser()
    chain = generate | chat | output_parser
    result = chain.invoke({})
    print(remove_code_fences(result))
    print()
    return


# %% [markdown]
# Model Inputs

# %%
#create inputs to the model, telling it what needs to be done. 
#provides system message
system = context_gen("systemmsg.txt")

#provides the few shot examples
output_examples = context_gen("outputex.txt")

#provides the input examples
input_examples = context_gen("inputex.txt")

#provides the database schema
schema = context_gen("dataBaseSchema.txt")

refsystem = context_gen("ref_system copy.txt")


'''change the human variable to test different inputs'''
human = ("select all faces with radius less than 10mm in the xy plane")


# %% [markdown]
# Few shot prompts example template 

# %%
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


# %%
class SubQuery(BaseModel):
    '''Search for the geometric definition of a feature across the vector database'''

    sub_query: str = Field(
        ...,
        description="The text to be used as a sub-query in the prompt.",
    )   

#First input to the model, breaks query down and provides geometry definition

class YamlText(BaseModel):
    text: str = Field(SQLQuery = "Yaml Text printed one line at a time")
    


# %%
"""This model sends the user query to the LLM, which then breaks it down into smaller parts if there are words it does not understand"""

system2 = context_gen("system2.txt")
prompt = ChatPromptTemplate.from_messages([("system", system2), ("human", human),])

chat = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.5)
chat_with_tools = chat.bind_tools([SubQuery])
parser = PydanticToolsParser(tools=[SubQuery])
query_analyzer = prompt | chat_with_tools | parser 
output = query_analyzer.invoke({}, {"tags": ["loop 001"]})
result = output[0].sub_query


# %%
"""The next step is to generate a definition of the words it did not understand, based on the broken down query in the previous step"""

#get context file 
system3 = context_gen("reflect1.txt")

#chat prompt template for defining the words 
definer = ChatPromptTemplate.from_messages([("system", system3), ("human", result)])
chat = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.5)

#using string output parser as the output is a string
output_parser = StrOutputParser()
chain2 = definer | chat | output_parser
definition = chain2.invoke({}, {"tags":["loop 002"]})
print(definition)


# %%
"""This step generates an SQL query in YAML with a single shot prompt, based on a single example, emphasizing on basic requirements of the output"""

parser = StrOutputParser()
prompt = ChatPromptTemplate.from_messages([("system", system), MessagesPlaceholder(variable_name="messages")])
chat = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.5)
generate = prompt | chat 

#generates the output and appends it to the empty string stored in the yaml variable.
yaml = ""
request = HumanMessage(content = human)
for chunk in generate.stream({"messages": [request]}, {"tags": ["loop 003"]}):
    result = chunk.content
    yaml += result
    print(result, end="")    


# %%
"""The next step is to ask the model to carry out a self reflection on the output that it generated in the previous step and provide feedback on the same, after which it generates an improved output taking the same feedback into consideration."""

reflection_prompt = ChatPromptTemplate.from_messages([("system", refsystem), few_shot_prompt, ("ai", definition), MessagesPlaceholder(variable_name="messages"), ])

#the chat variable below can be changed if reflection needs to be used from a different LLM model. 
#chat = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.5)

#chain for the reflection prompt.
reflect = reflection_prompt | chat 

#generates the output and appends it to the empty string stored in the reflectedyaml variable.
reflectedyaml = ""
for chunk in reflect.stream({"messages": [request, HumanMessage(content=yaml)]}, {"tags": ["loop 004"]}):
    result = chunk.content
    print(result, end="")
    reflectedyaml += result



# %%
"""This section generates definitions of the reflection and generation nodes for the langgraph"""

async def generation_node(state: Sequence[BaseMessage]):
    return await generate.ainvoke({"messages": state})

async def reflection_node(messages: Sequence[BaseMessage]) -> List[BaseMessage]:
    cls_map = {"ai": HumanMessage, "human": AIMessage}
    translated = [messages[0]] + [cls_map[m.type](content = m.content) for m in messages[1:]]
    res = await reflect.ainvoke({"messages": translated})
    return HumanMessage(content=res.content)


# %%
"""Building the graph according to the nodes defined earlier, also contains a conditional node to iterate through multiple loops of the generation and reflection cycle to improve the output before printing final response"""
builder = MessageGraph()
builder.add_node("generate", generation_node)
builder.add_node("reflect", reflection_node)
builder.set_entry_point("generate")

#iteration function. Change the number of iterations as required.
def should_continue(state: List[BaseMessage]):
    if len(state) > 5:
        return END
    return "reflect"


#building and compiling the graph.
builder.add_conditional_edges("generate", should_continue)
builder.add_edge("reflect", "generate")
graph = builder.compile()
print()

#run the graph and trace the output using langsmith. 
async for event in graph.astream(HumanMessage(content=human)):
    print(event)
    print('---')
     


# %%



