from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader, Docx2txtLoader, JSONLoader, CSVLoader, PyPDFLoader
from models.file_model import FileModel
from langchain_community.vectorstores import OpenSearchVectorSearch
import numpy as np
import logging
import os

from config.config import config
from config.model_config import create_embedding_model
from utils.utils import load_documents

logger = logging.getLogger()
logger.setLevel(logging.INFO)

class EmbeddingService:

    def __init__(self, project_id):
        self.embedding_model = create_embedding_model()
        self.project_id = project_id
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1024, 
            chunk_overlap=100,
        )
        self.index_name = f"knowledge_{project_id}"
        logging.info(f"Starting Embedding Service for project {project_id}")

    def create_embeddings(self, file: FileModel):
        logging.info(f"Loading file {file.file_name} into document")
        documents = load_documents(file=file)
        for document in documents:
            document.metadata.update(
                {
                    'file_id': file.file_id
                }
            )
        texts = self.text_splitter.split_documents(documents)
        if texts:
            logging.info("Creating embedding for document")
            self.create_embedding_for_texts(embedding_model=self.embedding_model, texts=texts, index_name=self.index_name)
    
    @staticmethod
    def create_embedding_for_texts(embedding_model, texts, index_name):
        max_os_docs_per_put = 500
        db_shards = (len(texts) // max_os_docs_per_put) + 1
        shards = np.array_split(texts, db_shards)

        logging.info("Creating entry in index")
        doc_search = OpenSearchVectorSearch(index_name=index_name, 
                                            embedding_function=embedding_model,
                                            opensearch_url=config.OPENSEARCH_URL)
        
        for shard in shards:
            doc_search.add_documents(documents=shard)