from langchain_core.tools import BaseTool
from langchain_community.vectorstores import OpenSearchVectorSearch
from pydantic.v1 import Field, BaseModel
from config.model_config import create_embedding_model, create_chat_model
from config.config import config
from langchain.chains.query_constructor.base import AttributeInfo
from langchain.retrievers.self_query.base import SelfQueryRetriever
from langchain.retrievers import EnsembleRetriever
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainFilter
from langchain_core.callbacks import CallbackManagerForToolRun

import logging
from typing import Optional, Type

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class ConfluenceToolInput(BaseModel):
    query: str = Field(description="query to search against confluence vector store")

class ConfluenceTool(BaseTool):
    """
    Tool that queries confluence documents 
    """
    session_id: str = Field(exclude=True)
    project_id: str = Field(exclude=True)
    description: str = Field(default="""Useful for answering queries related to current project. Confluence contains documents and wikis on the project
        ## Rules
        - Use `Docs` tool to search and retrieve information from Confluence.
        - Always provide the source of the information when using the Confluence tool.
        - Ignore irrevelant information from Confluence

        Examples:
        - Ask Docs what is the objective of Nexus project?
        - Ask Docs what is the architecture of the project?                    
    """)
    name: str = Field(default="Confluence")
    args_schema: Type[BaseModel] = ConfluenceToolInput

    def create_retriever(self):
        logging.info(f"Creating retriever for confluence tool")
        # Retriever configuration
        metadata_field_info = [
            AttributeInfo(
                name="title",
                description="Title of page",
                type="string",
            ),
            AttributeInfo(
                name="space.key",
                description="Unique key of spaces",
                type="string",
            ),
            AttributeInfo(
                name="space.name",
                description="Name of a confluence space",
                type="string",
            )
        ]
        document_content_description = "Knowledge Base for Confluence Documents"
        
        # Load models
        embedding_model = create_embedding_model()
        chat_model = create_chat_model()

        # Intialize vector search store
        confluence_index_name = f"confluence_{self.project_id}"
        opensearch_vector_store = OpenSearchVectorSearch(
            index_name=confluence_index_name,
            embedding_function=embedding_model,
            opensearch_url=config.OPENSEARCH_URL,
        )
        
        # Create retrievers
        opensearch_retriever = opensearch_vector_store.as_retriever(search_kwargs={"k": 10})
        self_query_retriever = SelfQueryRetriever.from_llm(
            chat_model, opensearch_vector_store, document_content_description, metadata_field_info, verbose=False, 
            search_kwargs={"k": 10}, fix_invalid=True
        )

        # Combine in ensemble
        ensemble_retriever = EnsembleRetriever(
            retrievers=[self_query_retriever, opensearch_retriever], weights=[0.5, 0.5]
        )
        return ensemble_retriever

    def _run(
            self,
            query: str,
            run_manager: Optional[CallbackManagerForToolRun]
    ) -> str:
        logging.info(f"Starting confluence tool with query: {query}")
        retriever = self.create_retriever()
        logging.info("Confluence retriever successfully created")
        docs = retriever.invoke(query)
        return docs