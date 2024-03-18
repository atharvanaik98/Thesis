# %% [markdown]
# Import necessary packages

# %%
from langchain_openai import OpenAI
from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from pathlib import Path
from langchain_core.output_parsers import StrOutputParser
from langchain.output_parsers import PydanticToolsParser
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
human = ("select all struts")


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

    
system2 = context_gen("system2.txt")
prompt = ChatPromptTemplate.from_messages([("system", system2), ("human", human),])

chat = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.5)
chat_with_tools = chat.bind_tools([SubQuery])
parser = PydanticToolsParser(tools=[SubQuery])
query_analyzer = prompt | chat_with_tools | parser 
output = query_analyzer.invoke({}, {"tags": ["loop 001"]})
result = output[0].sub_query


# %%
system3 = context_gen("reflect1.txt")


reflect1 = ChatPromptTemplate.from_messages([("system", system3), ("human", result)])
chat = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.5)
output_parser = StrOutputParser()
chain2 = reflect1 | chat | output_parser
someoutput = chain2.invoke({})
print(someoutput)


# %%
prompt = ChatPromptTemplate.from_messages([("system", system), MessagesPlaceholder(variable_name="messages"),])
chat = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.0)
generate = prompt | chat

yaml = ""
request = HumanMessage(content = someoutput)
for chunk in generate.stream({"messages": [request]}):
    result = (remove_code_fences(chunk.content))
    print(result, end = "")
    yaml += result
    

reflection_prompt = ChatPromptTemplate.from_messages([("system", refsystem), few_shot_prompt, MessagesPlaceholder(variable_name="messages")])

reflect = reflection_prompt | chat 

reflectedyaml = ""
for chunk in reflect.stream({"messages": [request, HumanMessage(content=yaml)]}):
    result = remove_code_fences(chunk.content)
    print(result, end="")
    reflectedyaml += result

async def generation_node(state: Sequence[BaseMessage]) -> List[BaseMessage]:
    cls_map = {"ai": HumanMessage, "human": AIMessage}
    translated = [messages[0]] + [cls_map[m.type](m.content) for m in messages[1:]]
    res = await reflect.ainvoke({"messages": translated})
    print()
    print(res.content)  # Print the output
    return HumanMessage(content=res.content)

async def reflection_node(state: Sequence[BaseMessage]):
    return await reflect.ainvoke({"messages": state})


builder = MessageGraph()
builder.add_node("generate", generation_node)
builder.add_node("reflect", reflection_node)
builder.set_entry_point("generate")

def should_coninue(state: List[BaseMessage]):
    if len(state) > 6:
        return END  
    return generate


builder.add_conditional_edges("generate", should_coninue)
builder.add_edge("reflect", "generate")
graph = builder.compile()


async def main():
    async for event in graph.astream(HumanMessage(content=someoutput)):
        print(event)
     
