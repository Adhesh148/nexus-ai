from typing import List
from typing_extensions import TypedDict
from langchain_core.documents import Document
from models.file_model import FileModel

# Define State of Workflow Graph
class IssueGraphState(TypedDict):
    """
    Represents the state of our graph.

    Attributes:
        files: List of file IDs
        documents: list of documents
    """
    files: List[FileModel]
    documents: List[Document]
    requirements: List[dict]