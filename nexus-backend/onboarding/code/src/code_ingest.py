from opensearchpy import OpenSearch, RequestsHttpConnection
from langchain.text_splitter import RecursiveCharacterTextSplitter, Language
from langchain_community.vectorstores import OpenSearchVectorSearch
from langchain_voyageai import VoyageAIEmbeddings
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import GithubFileLoader
import numpy as np

import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

OPENSEARCH_PROPS = {
    "OPENSEARCH_URL": "http://localhost",
    "OPENSEARCH_PORT": 9200
}

VOYAGE_MODEL_PROPS = {
    "MODEL_ID": "voyage-code-2",
    "API_KEY": ""
}

OPENAI_PROPS = {
    "EMBEDDING_MODEL_ID": "text-embedding-3-large",
    "OPENAI_API_KEY": ""
}

GITHUB_PROPS = {
    "ACCESS_TOKEN": "",
    "REPO_NAME": "Adhesh148/quellm",
    "GITHUB_API_URL": "https://api.github.com"
}

SPLITTER_CHUNK_SIZE=1024
SPLITTER_CHUNK_OVERLAP=100

SUPPORTED_FILE_TYPES = {
    Language.PYTHON: ('.py'),
    Language.MARKDOWN: ('.md'),
    Language.JAVA: ('.java'),
    Language.C: ('.c'),
    Language.CPP: ('.cpp'),
    Language.JS: ('.js', '.jsx'),
    Language.TS: ('.ts', '.tsx'),
    Language.GO: ('.go')
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

def delete_existing_files(opensearch_client, index_name, ids):
    logging.info(f"Deleting existing pages from index")
    response = opensearch_client.delete_by_query(
        index=index_name,
        body={
            "query": {
                "terms": {
                    "metadata.path.keyword": ids
                }
            }
        }
    )

    if response['deleted'] > 0:
        logging.info("Documents deleted successfully")
    else:
        logging.info("No documents deleted")

def create_embeddings_model():
    return OpenAIEmbeddings(
        model=OPENAI_PROPS["EMBEDDING_MODEL_ID"],
        api_key=OPENAI_PROPS["OPENAI_API_KEY"],
    )

def create_code_loader(file_types):
    return GithubFileLoader(
        repo=GITHUB_PROPS["REPO_NAME"],
        access_token=GITHUB_PROPS["ACCESS_TOKEN"],
        github_api_url=GITHUB_PROPS["GITHUB_API_URL"],
        file_filter=lambda file_path: file_path.endswith(file_types)
    )

def create_code_splitter(language):
    return RecursiveCharacterTextSplitter.from_language(language=language,
                                                        chunk_size=SPLITTER_CHUNK_SIZE,
                                                        chunk_overlap=SPLITTER_CHUNK_OVERLAP)

def create_embedding_for_chunks(embedding_model, chunks, index_name):
    max_os_docs_per_put = 500
    db_shards = (len(chunks) // max_os_docs_per_put) + 1
    shards = np.array_split(chunks, db_shards)

    doc_search = OpenSearchVectorSearch(index_name=index_name, 
                                        embedding_function=embedding_model,
                                        opensearch_url=f"{OPENSEARCH_PROPS['OPENSEARCH_URL']}:{OPENSEARCH_PROPS['OPENSEARCH_PORT']}")
    
    for shard in shards:
        doc_search.add_documents(documents=shard)

def ingest(project_id):
    """
    Runs ingestion flow for code files from github
    """
    INDEX_NAME = f"code_{project_id}"

    # Load embedding model
    embedding_model = create_embeddings_model()
    
    # Create opensearch client
    opensearch_client = create_opensearch_client()
        
    # Support for all code languages
    for lang in SUPPORTED_FILE_TYPES.keys():
        # Create code loader
        loader = create_code_loader(file_types=SUPPORTED_FILE_TYPES[lang])

        # Load code files and 
        documents = loader.load()
        logging.info(f"Found {len(documents)} files of type {lang}")
        for doc in documents:
            logging.info(f"Loaded document: {doc.metadata['path']}")

        ids = [doc.metadata['path'] for doc in documents]
        delete_existing_files(opensearch_client=opensearch_client, index_name=INDEX_NAME, ids=ids)
       
        # Load code-splitter
        if len(documents) > 0:
            code_splitter = create_code_splitter(language=lang)
            code_chunks = code_splitter.split_documents(documents)
            logging.info(f"Split into {len(code_chunks)} chunks of code")
            if code_chunks:
                create_embedding_for_chunks(embedding_model=embedding_model, chunks=code_chunks, index_name=INDEX_NAME)
                logging.info(f"{len(code_chunks)} documents added to vector store to index {INDEX_NAME}")


PROJECT_ID = 101    
ingest(project_id=PROJECT_ID)