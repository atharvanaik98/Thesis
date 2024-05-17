from pathlib import Path
from pyexpat import model

def context_gen(file_name):
    Folder = "Context_files"
    here = Path(locals().get('__file__', Folder)).resolve()
    parameter = (here / file_name).read_text()
    return parameter
def generate_yaml_ai(human_prompt):
    # Import necessary packages

    #add_package_path()
    
    from langchain_core.prompts import (
        ChatPromptTemplate,
        FewShotChatMessagePromptTemplate,
    )
    from langchain_openai import ChatOpenAI
    from langchain_mistralai.chat_models import ChatMistralAI
    from langchain_core.output_parsers import StrOutputParser
    from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate, MessagesPlaceholder, PromptTemplate
    from langchain_openai import ChatOpenAI
    
    from langchain_core.output_parsers import StrOutputParser
    from langchain.output_parsers import PydanticToolsParser, PydanticOutputParser
    from langchain_core.pydantic_v1 import BaseModel, Field, validator
    from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
    from typing import Sequence, List
    #from langgraph.graph import MessageGraph, END
    from langchain_community.document_loaders import DirectoryLoader
    from langchain_community.vectorstores import FAISS
    from langchain_text_splitters import CharacterTextSplitter
    from langchain_openai import OpenAIEmbeddings
    from langchain_mistralai import MistralAIEmbeddings
    from langchain_core.runnables import RunnablePassthrough
    from langgraph.graph import MessageGraph, END


    class analyzed_query(BaseModel):
        """Identifying whether a geometric feature is present in the database and stating the name of the feature"""
        answer: str= Field(description="YES or NO")
        features: List= Field(description="Name of the identified geometrical feature")

    class Response(BaseModel):
        """Listing the answer of whether the feature is present in the database and the name of the feature"""
        Response: List[analyzed_query]
    
    
    #chat = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.5)
    #show_message("Imported packages")
    chat = ChatMistralAI(model="mixtral-8x7B", temperature = 0)
    system1 = context_gen("system1.txt")

    #provides the few shot examples
    output_examples = context_gen("outputex.txt")

    #provides the input examples
    input_examples = context_gen("inputex.txt")

    #provides the database schema
    schema = context_gen("dataBaseSchema.txt")

    refsystem = context_gen("ref_system copy.txt")

    system3 = context_gen("system3.txt")

    system2 = context_gen("system2.txt")

    rag_prompt = context_gen("rag_prompt.txt")
    
    # Few shot prompts example template
    examples = [
        {"input": input_examples, "output": output_examples},
    ]

    example_prompt = ChatPromptTemplate.from_messages(
        [
            ("human", "{input}"),
            ("ai", "{output}"),
        ]
    )
    few_shot_prompt = FewShotChatMessagePromptTemplate(
    example_prompt=example_prompt,
    examples=examples,
)

    #show_message("Prompts created")
    parser = PydanticOutputParser(pydantic_object=analyzed_query)
    prompt = ChatPromptTemplate.from_messages([("system", rag_prompt + "Answer the user query. Wrap the output in `json` tags\n{format_instructions}",), ("human", human_prompt),]).partial(format_instructions=parser.get_format_instructions())
    chain = prompt | chat | parser
    feature_extractor = chain.invoke({}, {"tags": ["feature_extractor"]})
    extracted_features = str(feature_extractor.features)

    loader = DirectoryLoader("RAG")
    raw_docs = loader.load()
    textsplitter = CharacterTextSplitter(chunk_size=2000, chunk_overlap=0)
    docs = textsplitter.split_documents(raw_docs)
    db = FAISS.from_documents(docs, MistralAIEmbeddings())
    retriever = db.as_retriever()
    

    prompt_for_rag = ChatPromptTemplate.from_template("""You are an assistant that is an expert at RAG (Retrieval Augmented Generation). You have been tasked with looking for the definition of the word provided to you as input and generate a summary of the available information."
                You will use only the context provided to you.                                 
                Context:{context}
                Query_to_db:{query}""")
    rag_chain = ({"context": retriever, "query": RunnablePassthrough()}) | prompt_for_rag | chat | StrOutputParser()

    #Base prompt chain, generates the first yaml version with minimal context
    base_prompt = ChatPromptTemplate.from_messages([("system", system1), few_shot_prompt, MessagesPlaceholder(variable_name="messages")])
    yaml_generator = base_prompt | chat 
    rag_output = rag_chain.invoke(f"What is the definition of {extracted_features}?")
    print(rag_output)

    def chain_yes():
        chain = yaml_generator 
        yaml = chain.invoke({"messages": [HumanMessage(content = human_prompt)]}, {"tags": ["chain_yes"]})
        return yaml

    def chain_no():
        chain = yaml_generator 
        yaml = chain.invoke({"messages": [HumanMessage(content = f"Here is some additional context: {rag_output} along with the original user query: {human_prompt}")]})
        return yaml

    def decision_maker(response_obj: analyzed_query):
        for item in response_obj:
            if item == "YES":
                return chain_yes()
            elif item == "NO":
                return chain_no()

    model_output = []
    for answer in feature_extractor:
        model_output.append(decision_maker(answer))
    print(model_output)

    reflection_prompt = ChatPromptTemplate.from_messages([("system", refsystem), few_shot_prompt, ("ai", f"Here is some added context {rag_output}"), MessagesPlaceholder(variable_name="messages"), ])
    reflect = reflection_prompt | chat | StrOutputParser()
    feedback = reflect.invoke({"messages": [f"This is the YAML code you are supposed to provide feedback for: {model_output[0]}"]}, {"tags": ["feedback"]})
    
    
    final_generate = base_prompt | chat | StrOutputParser()
    output_yaml = final_generate.invoke({"messages": [f"Regenerate the YAML code based on the following feedback: {feedback}"]}, {"tags": ["final_generate"]})    
    print(model_output[0])
    print()
    print(feedback)
    print()
    print(output_yaml)


generate_yaml_ai("select all vanes")