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
config_path = ("C:\Onedrive\OneDrive - Chalmers\Thesis Files\Repo\Thesis\Config\config.yml")

#initiate guardrails for the model
config = RailsConfig.from_path(config_path)
rails = LLMRails(config)

#Github location url for the context file stored in the repository 
repo_url = "https://raw.githubusercontent.com/firestorm98/Thesis/main/Input.txt"
TOKEN = "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"
headers = {
    "authorization": f"token {TOKEN}", 
    "Accept": "text/plain"
}
"""async def generate_text():
    context = requests.get(repo_url, headers=headers).text
    prompt = input("Enter the description of the geometry you want to select: ")
    modelprep = await model.abatch([context, prompt])
    generated_text = modelprep[0]
    print(generated_text)

asyncio.run(generate_text())"""

response = rails.generate(messages=[{
    "role": "user",
    "content": input("Enter the description of the geometry you want to select: ")
}])

print(response)
