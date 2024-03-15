from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate, MessagesPlaceholder
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from pathlib import Path
from typing import List, Sequence
from langchain_core.output_parsers import StrOutputParser
from langchain.globals import set_debug
from langgraph.graph import MessageGraph, END
import sys

set_debug(False)

def context_gen(file_name):
    Folder = "reflection_context"
    here = Path(locals().get('__file__', Folder)).resolve()
    parameter = (here / file_name).read_text()
    return parameter

def remove_code_fences(text):
    '''Removes code fences from the output.'''
    lines = text.split("\n")
    lines = [line for line in lines if not line.strip().startswith('```')]
    
    #Gets rid of first space empty space before the -filter line
    #lines[1] = lines[1].replace(' -', '-', 2)
    return "\n".join(lines)

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

#system message for reflection
refsystem = context_gen("ref_system.txt")

'''change the human variable to test different inputs'''
human = ("Select all boltholes and then select their corresponding edges.")

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

prompt = ChatPromptTemplate.from_messages([("system", system), MessagesPlaceholder(variable_name="messages"),])
chat = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.0)
generate = prompt | chat

yaml = ""
request = HumanMessage(content = human)
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
    #adjusting the other messages, I think adjusts the way in which they are sent to the llm
    cls_map = {"ai": HumanMessage, "human": AIMessage}
    translated = [messages[0]] + [cls_map[m.type](m.content) for m in messages[1:]]
    res = await reflect.ainvoke({"messages": translated})
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
    async for event in graph.astream(HumanMessage(content=human)):
        print(event)
          

        