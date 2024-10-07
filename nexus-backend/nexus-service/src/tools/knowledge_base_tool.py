from langchain_core.tools import BaseTool
from pydantic.v1 import Field, BaseModel
from langchain_core.callbacks import CallbackManagerForToolRun
from langchain.memory import ConversationBufferMemory

import logging
from typing import Optional, Type

from workflow.knowledge.knowledge_graph import knowledge_graph

logger = logging.getLogger()
logger.setLevel(logging.INFO)

class KnowledgeBaseToolInput(BaseModel):
    query: str = Field(description="query to search against knowledge base")

class KnowledgeBaseTool(BaseTool):
    """
    Tool that queries knowledge base documents
    """
    session_id: str = Field(exclude=True)
    project_id: str = Field(exclude=True)
    memory: ConversationBufferMemory = Field(exclude=True)
    description: str = Field(default="""Useful for answering queries or performing actions on documents in knowledge base
        ## Rules
        - Use `Knowledge Base` tool to search and retrieve information from Knoledge Base documents.
        - Always provide the source of the information when using the Knowledge Base tool.
        - Ignore irrevelant information from documents

        Examples:
        - Ask Knowledge Base, Summarize a document?
        - Ask Knowledge Base, Give key points in French for contents in ABC document.                   
    """)
    name: str = Field(default="KnowledgeBaseTool")
    args_schema: Type[BaseModel] = KnowledgeBaseToolInput

    def _run(
            self,
            query: str,
            run_manager: Optional[CallbackManagerForToolRun]
        ) -> str:
            logging.info(f"Starting knowledge base tool with query: {query}")

            logging.info(f"knowledge base tool called with memory: {self.memory}")
            inputs = {"project_id": self.project_id, "user_query": query, "chat_history": self.memory}

            for output in knowledge_graph.stream(inputs):
                for key, value in output.items():
                    pass
            return value["result"]
