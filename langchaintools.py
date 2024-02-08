from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool, StructuredTool, tool
import requests

@tool
def context() -> str:
    """
    Load a context from a file.
    """
    #Github location url for the context file stored in the repository 
    repo_url = "https://raw.githubusercontent.com/firestorm98/Thesis/main/Input.txt"
    TOKEN = "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"
    headers = {
    "authorization": f"token {TOKEN}", 
    "Accept": "text/plain"
}
    context_file = requests.get(repo_url, headers=headers).text
       
    return context

