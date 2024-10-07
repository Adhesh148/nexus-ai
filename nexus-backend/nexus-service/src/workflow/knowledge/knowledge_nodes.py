from typing import List
from langchain.memory import ConversationBufferMemory
import logging

from utils import utils
from models.file_model import FilePynamoDBModel
from workflow.knowledge.determine_node import determiner_chain, files_retriever_chain
from workflow.knowledge.direct_query_node import file_query_chain
from workflow.knowledge.vector_query_node import create_retriever, vector_query_chain
from langchain.retrievers import ContextualCompressionRetriever

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# ---------- NODES & EDGES -------------
def file_retriever_node(state):   
    """
    Loads the necesary files for user query

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): New key added to state, documents, that contains retrieved documents
    """
    logging.info("[KNOWLEDGE-GRAPH] File Retriever Node")
    project_id = state["project_id"]
    memory: ConversationBufferMemory = state["chat_history"]
    user_query = state["user_query"]

    # Get all project files
    project_files = FilePynamoDBModel.scan(FilePynamoDBModel.project_id == project_id)
    input_file_names = [file.file_name for file in project_files]

    file_retriever = files_retriever_chain()
    response = file_retriever.invoke({"user_query": user_query, "input_files": input_file_names, "chat_history": memory.buffer_as_messages[-10:]})
    logging.info(f"File Retriever result: {response['files']}")
    return {"relevant_files": response["files"]}

def direct_query(state):
    """
    This node directly queries the file for information on user query
    """
    logging.info("[KNOWLEDGE-GRAPH] Direct Query node")
    project_id = state["project_id"]
    user_query = state["user_query"]
    relevant_file_names = state["relevant_files"]

    all_file_models = FilePynamoDBModel.scan(FilePynamoDBModel.project_id == project_id)
    relevant_file_models = [file for file in all_file_models if file.file_name in relevant_file_names]
    relevant_text_artifacts = [utils.get_text_artifact(file) for file in relevant_file_models]

    # If image directly call model

    file_contents = ""
    for file in relevant_text_artifacts:
        documents = utils.load_documents(file)
        file_contents += f"{file.file_name}\n"  # Add filename once
        for doc in documents:
            file_contents += f"{doc.page_content}\n"  # Add document content

    result =  file_query_chain.invoke({"user_query": user_query, "file_contents": file_contents})
    logging.info(f"Direct query result: {result}")
    return {"result": result}

def vector_query(state):
    """
    This node does vector search to get relevant information
    """
    logging.info("[KNOWLEDGE-GRAPH] Vector Store Query node")
    user_query = state["user_query"]
    project_id = state["project_id"]
    
    retriever: ContextualCompressionRetriever = create_retriever(project_id=project_id)
    logging.info("Knowledge base retriever successfully created")
    documents = retriever.invoke(user_query)

    file_contents = ""
    for doc in documents:
        file_contents += f"{doc.page_content}\n"  # Add document content

    result = vector_query_chain.invoke({"user_query": user_query, "file_contents": file_contents})
    logging.info(f"Vector query result: {result}")
    return {"result": result}

# Edges
def determine_edge(state):   
    """
    Determine if you can directly load and query a particualar file in knowledge base or
    do a vector search to get relevant documents from vector store

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): New key added to state, documents, that contains retrieved documents
    """
    logging.info("[KNOWLEDGE-GRAPH] Determine node")
    project_id = state["project_id"]
    memory: ConversationBufferMemory = state["chat_history"]
    user_query = state["user_query"]

    # Get all project files
    project_files = FilePynamoDBModel.scan(FilePynamoDBModel.project_id == project_id)
    input_file_names = [file.file_name for file in project_files]

    determiner = determiner_chain()
    response = determiner.invoke({"user_query": user_query, "input_files": input_file_names, "chat_history": memory.buffer_as_messages[-10:]})

    if response["response"] == "YES":
        return "direct_query"
    else:
        return "vector_query"