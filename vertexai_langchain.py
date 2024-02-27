from langchain_google_vertexai import VertexAI, VertexAIEmbeddings, ChatVertexAI
import vertexai
from pathlib import Path


vertexai.init(project = "totemic-veld-412608")
llm = VertexAI(model_name = "gemini-pro", 
               temperature = "0.0", 
               max_tokens = 100)

here = Path(__file__).parent






