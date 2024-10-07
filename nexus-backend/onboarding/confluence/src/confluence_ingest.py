from opensearchpy import OpenSearch, RequestsHttpConnection
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import ConfluenceLoader
from langchain_community.vectorstores import OpenSearchVectorSearch
import numpy as np

import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Define properties
CONFLUENCE_PROPS = {
    "CONFLUENCE_USERNAME": "adheshreghu@gmail.com",
    "CONFLUENCE_TOKEN": "",
    "CONFLUENCE_URL": "https://nexusai.atlassian.net/wiki"
}

OPENSEARCH_PROPS = {
    "OPENSEARCH_URL": "http://localhost",
    "OPENSEARCH_PORT": 9200
}

OPENAI_PROPS = {
    "EMBEDDING_MODEL_ID": "text-embedding-3-large",
    "OPENAI_API_KEY": ""
}

def create_opensearch_client():
    opensearch_client = OpenSearch(
        hosts=[{'host': OPENSEARCH_PROPS["OPENSEARCH_URL"].replace("https://", "").replace("http://", ""), 'port': OPENSEARCH_PROPS["OPENSEARCH_PORT"]}],
        use_ssl=False,  # True when hosted
        verify_certs=False,
        ssl_assert_hostname=False,
        ssl_show_warn=False,
        connection_class=RequestsHttpConnection
    )
    return opensearch_client

def create_embedding_for_texts(embedding_model, texts, index_name):
    max_os_docs_per_put = 500
    db_shards = (len(texts) // max_os_docs_per_put) + 1
    shards = np.array_split(texts, db_shards)

    doc_search = OpenSearchVectorSearch(index_name=index_name, 
                                        embedding_function=embedding_model,
                                        opensearch_url=f"{OPENSEARCH_PROPS['OPENSEARCH_URL']}:{OPENSEARCH_PROPS['OPENSEARCH_PORT']}")
    
    for shard in shards:
        doc_search.add_documents(documents=shard)

def delete_existing_pages(opensearch_client, index_name, page_ids):
    logging.info(f"Deleting existing pages from index")
    response = opensearch_client.delete_by_query(
        index=index_name,
        body={
            "query": {
                "terms": {
                    "metadata.id": page_ids
                }
            }
        }
    )

    if response['deleted'] > 0:
        logging.info("Documents deleted successfully")
    else:
        logging.info("No documents deleted")

def ingest(project_id, space_key):
    # Define params
    SPLITTER_CHUNK_SIZE=1024
    SPLITTER_CHUNK_OVERLAP=100
    INDEX_NAME = f"confluence_{project_id}"

    # Create opensearch client
    opensearch_client = create_opensearch_client()

    # Load text-splitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=SPLITTER_CHUNK_SIZE, 
        chunk_overlap=SPLITTER_CHUNK_OVERLAP,
    )

    # Load embedding model
    embedding_model = OpenAIEmbeddings(
        model=OPENAI_PROPS["EMBEDDING_MODEL_ID"],
        api_key=OPENAI_PROPS["OPENAI_API_KEY"],
    )

    # Define confluence loader
    loader = ConfluenceLoader(
        url=CONFLUENCE_PROPS["CONFLUENCE_URL"],
        api_key=CONFLUENCE_PROPS["CONFLUENCE_TOKEN"],
        username=CONFLUENCE_PROPS["CONFLUENCE_USERNAME"],
        number_of_retries=3, min_retry_seconds=2, max_retry_seconds=10,
        confluence_kwargs={
            'timeout': 100
    })

    # Load all pages for that space
    documents = loader.load(space_key=space_key, include_attachments=False, limit=10)
    for doc in documents:
        logging.info(f"Load Document with Page ID: {doc.metadata['id']}, Page Title: {doc.metadata['title']}")

    page_ids = [doc.metadata['id'] for doc in documents]
    delete_existing_pages(opensearch_client=opensearch_client, index_name=INDEX_NAME, page_ids=page_ids)

    texts = text_splitter.split_documents(documents)
    logging.info(f"Split into {len(texts)} chunks of text")
    if texts:
        create_embedding_for_texts(embedding_model=embedding_model, texts=texts, index_name=INDEX_NAME)
        logging.info(f"{len(texts)} documents added to vector store for {space_key} to index {INDEX_NAME}")

if __name__ == "__main__":
    PROJECT_ID = 101
    SPACE_KEY = "nexusai"
    ingest(project_id=PROJECT_ID, space_key=SPACE_KEY)