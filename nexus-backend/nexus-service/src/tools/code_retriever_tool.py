from langchain_core.tools import BaseTool
from pydantic.v1 import Field, BaseModel
from langchain_core.callbacks import CallbackManagerForToolRun
from langchain.memory import ConversationBufferMemory
from langchain.chains.query_constructor.base import AttributeInfo
from langchain.retrievers.self_query.base import SelfQueryRetriever
from langchain.retrievers import EnsembleRetriever
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainFilter
from langchain_community.vectorstores import OpenSearchVectorSearch

from config.model_config import create_embedding_model, create_chat_model
from config.config import config

import logging
from typing import Optional, Type


logger = logging.getLogger()
logger.setLevel(logging.INFO)

class CodeRetrieverToolInput(BaseModel):
    query: str = Field(description="query to search against code repository")

class CodeRetrieverTool(BaseTool):
    """
    Tool that queries code repository (vector store)
    """
    session_id: str = Field(exclude=True)
    project_id: str = Field(exclude=True)
    memory: ConversationBufferMemory = Field(exclude=True)
    description: str = Field(default="""Useful for answering queries or performing actions on code repository
        ## Rules
        - Use `CodeRetreiver` tool to search and retrieve information from code vector store. Use this tool only when explicitly called using 'Ask Code'.
        - Always return the associated code for the query.
        - Always provide the source of the information when using the Code Retriever Tool (eg. source file name)
        - Ignore irrevelant information from code files

        Examples:
        - Ask Code, How does ABCService work?
        - Ask Code, Write test cases for XYZ module                 
    """)
    name: str = Field(default="CodeRetrieverTool")
    args_schema: Type[BaseModel] = CodeRetrieverToolInput

    def create_retriever(self):
        logging.info(f"Creating retriever for confluence tool")
        # Retriever configuration
        metadata_field_info = [
            AttributeInfo(
                name="path",
                description="Path of code file relative to project root",
                type="string",
            ),
            AttributeInfo(
                name="source",
                description="Remote source url of code file",
                type="string",
            )
        ]
        document_content_description = "Vector store for code files"
        
        # Load models
        embedding_model = create_embedding_model()
        chat_model = create_chat_model()

        # Intialize vector search store
        confluence_index_name = f"code_{self.project_id}"
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
            logging.info(f"Starting code retriever tool with query: {query}")
            retriever = self.create_retriever()
            logging.info("Code retriever successfully created")
            docs = retriever.invoke(query)
            return docs

