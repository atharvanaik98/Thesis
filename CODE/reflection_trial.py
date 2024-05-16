from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate, MessagesPlaceholder
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from pathlib import Path
from typing import List, Sequence
from langchain_core.output_parsers import StrOutputParser
from langchain.globals import set_debug
from langgraph.graph import MessageGraph, END
import asyncio


set_debug(False)

def context_gen(file_name):
    Folder = "Context_files"
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
system = context_gen("system1.txt")

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



reflection_prompt = ChatPromptTemplate.from_messages([("system", refsystem), few_shot_prompt, MessagesPlaceholder(variable_name="messages")])
reflect = reflection_prompt | chat 




async def generation_node(state: Sequence[BaseMessage]):
        return await generate.ainvoke({"messages": state}, {"tags": ["generation_chain"]})

async def reflection_node(state: Sequence[BaseMessage]) -> List[BaseMessage]:
        # Other messages we need to adjust
        cls_map = {"ai": HumanMessage, "human": AIMessage}
        # First message is the original user request. We hold it the same for all nodes
        translated = [state[0]] + [cls_map[msg.type](content=msg.content) for msg in state[1:]]
        res = await reflect.ainvoke({"messages": translated}, {"tags": ["reflection_chain"]})
        # We treat the output of this as human feedback for the generator
        return HumanMessage(content=res.content)



builder = MessageGraph()
builder.add_node("generate", generation_node)
builder.add_node("reflect", reflection_node)
builder.set_entry_point("generate")

def should_coninue(state: List[BaseMessage]):
    if len(state) > 2:
        return END  
    return generate


builder.add_conditional_edges("generate", should_coninue)
builder.add_edge("reflect", "generate")
graph = builder.compile()

async def process_events():
    async for event in graph.astream([HumanMessage(content=str(human))]):
        for key, value in event.items():
            if isinstance(value, dict):
                print(value.get('content'))
                print('---')
                print()
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):
                        print(item.get('content'))
                        print('---')
                        print()
                    else:
                        print(item.content)
                        print('---')
                        print()

    await process_events()

process_events()
