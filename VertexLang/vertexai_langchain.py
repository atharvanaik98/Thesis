from langchain_google_vertexai import VertexAI, VertexAIEmbeddings, ChatVertexAI
import vertexai
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_vertexai import ChatVertexAI
from pathlib import Path


vertexai.init(project = "totemic-veld-412608")
llm = VertexAI(model_name = "gemini-pro", 
               temperature = "0.0", 
               max_tokens = 100)
output_parser
here = Path(__file__).parent
system_message = (here / "Input.txt").read_text()


system = system_message
human = input("Enter geometry Description: ")
prompt = ChatPromptTemplate.from_messages([("system", system), ("human", human)])

chat = ChatVertexAI()

chain = prompt | chat
result = chain.invoke({})
print(result)





