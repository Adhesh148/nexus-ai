from typing import List, Optional
from typing_extensions import TypedDict
from langchain_core.documents import Document
from langchain.memory import ConversationBufferMemory

# Define State of Workflow Graph
class KnowledgeGraphState(TypedDict):
    """
    Represents the state of our graph.
    """
    project_id: str
    user_query: str
    result: str
    chat_history: ConversationBufferMemory
    relevant_files: Optional[List]
    