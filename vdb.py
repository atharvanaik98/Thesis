from langchain_community.document_loaders import DirectoryLoader
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings


loader = DirectoryLoader("./Context_files")
docs = loader.load()

splitter = CharacterTextSplitter(chunk_size = 1000, chunk_overlap = 0)
split_docs = splitter.split(docs)

vectorstore = Chroma.from_documents(documents = split_docs, embedding=OpenAIEmbeddings())
retriever = vectorstore.as_retriever()
 
