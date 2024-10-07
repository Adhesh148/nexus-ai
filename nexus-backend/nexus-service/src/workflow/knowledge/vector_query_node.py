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
from langchain.prompts import PromptTemplate

import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def create_retriever(project_id):
        logging.info(f"Creating retriever for knowledge tool")
        # Retriever configuration
        metadata_field_info = [
            AttributeInfo(
                name="source",
                description="Source file name",
                type="string",
            ),
            AttributeInfo(
                name="file_id",
                description="Unique key of file",
                type="string",
            )
        ]
        document_content_description = "Knowledge Base for files and documents"
        
        # Load models
        embedding_model = create_embedding_model()
        chat_model = create_chat_model()

        # Intialize vector search store
        knowledge_index_name = f"knowledge_{project_id}"
        opensearch_vector_store = OpenSearchVectorSearch(
            index_name=knowledge_index_name,
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

        # Create compression retriver
        _filter = LLMChainFilter.from_llm(chat_model)
        compression_retriever = ContextualCompressionRetriever(
            base_compressor=_filter, base_retriever=ensemble_retriever
        )
        return compression_retriever


# LLM
llm = create_chat_model()

# prompt
template = """
You are an AI assistant tasked with answering questions or performing actions based solely on the content of specific files provided to you. 
Your role is to provide accurate information and assistance without introducing any external knowledge or making up information.

Instructions:
1. Carefully read and analyze the content of the provided file(s).
2. Address the user's query or perform the requested action using only the information present in the given file(s).
3. If the query cannot be fully answered or the action cannot be completely performed using the provided content, clearly state the limitations of what you can do based on the available information.
4. Do not introduce any external knowledge, make assumptions, or provide information that is not explicitly stated in or directly inferred from the given file content.
5. If asked about topics not covered in the file(s), politely explain that you don't have information on that topic in the provided content.
6. When quoting or referencing specific parts of the file(s), indicate the source clearly (e.g., "According to the project report...")
7. If the user asks for clarification or additional details, only elaborate using information from the provided file(s).

File Content:
{file_contents}

User Query:
{user_query}
"""

prompt = PromptTemplate(template=template, input_variables=["user_query", "file_contents"])

vector_query_chain = prompt | llm