from typing import List
from typing_extensions import TypedDict
from langchain_core.documents import Document
import logging
import json

from utils import utils
from models.file_model import FilePynamoDBModel, FileModel
from workflow.issues.gather_node import requirement_gatherer
from workflow.issues.refine_node import refinement_chain

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# ---------- NODES -------------
def load(state):
    """
    Load documents

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): New key added to state, documents, that contains retrieved documents
    """
    logging.info("[ISSUE-GRAPH] Loading Documents............")
    files: FileModel = state["files"]
    all_documents = []

    for file in files:
        # Load file model
        documents = utils.load_documents(file=file)
        all_documents.extend(documents)
    
    return {"documents": all_documents}

def gather_requirements(state):
    """
    Gather requirements

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): New key added to state, requirements, that contains requirements gathered from documents
    """
    logging.info("[ISSUE-GRAPH] Gathering Requirements...........")
    documents: List[Document] = state["documents"]

    # generate requirements
    all_requirements = []
    for document in documents:
        requirements = requirement_gatherer.invoke({"document_content": document.page_content})
        all_requirements.extend(requirements["requirements"])
    
    return {"documents": documents, "requirements": all_requirements}

def refine_requirements(state):
    """
    Refine requirements

   Args:
        state (dict): The current graph state

    Returns:
        state (dict): New key added to state, requirements, that contains requirements gathered from documents
    """
    logging.info("[ISSUE-GRAPH] Refining Requirements............")
    requirements: List[{}] = state["requirements"]
    requirements_list_string = json.dumps({"requirements": requirements}, indent=4)

    # Refine requirements
    response = refinement_chain.invoke({"requirements_list": requirements_list_string})
    return {"requirements": response["requirements"]}