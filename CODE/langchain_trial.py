#this secrtion indicates the import of the libraries
import asyncio
from langchain_google_vertexai import VertexAI
from langchain_core.prompts import PromptTemplate
import vertexai
from pathlib import Path
from nemoguardrails import LLMRails, RailsConfig

#selection of the model for generative content: 
vertexai.init(project = "totemic-veld-412608")
model = VertexAI(model_name = "gemini-pro")

#selection of config path 
config_path = Path.cwd() / "Config"

#initiate guardrails for the model
config = RailsConfig.from_path(str(config_path /"config.yml"))
rails = LLMRails(str(config_path / "rails/rails.co"))

#Github location url for the context file stored in the repository 
repo_url = "https://raw.githubusercontent.com/firestorm98/Thesis/main/Input.txt"
TOKEN = "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"
headers = {
    "authorization": f"token {TOKEN}", 
    "Accept": "text/plain"
}

def generate_async():
    prompt = str(config_path / "prompt/prompt.yml")
    messages = {"role": "user", "content": "I am a software engineer"}


response = rails.generate_async

print(response)
