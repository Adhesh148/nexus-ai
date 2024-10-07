from opensearchpy import OpenSearch, RequestsHttpConnection
from config.config import config
from models.file_model import FilePynamoDBModel

import zipfile
from typing import Generator, List, Tuple
import io

import logging
import os

logger = logging.getLogger()
logger.setLevel(logging.INFO)

class KnowledgeService():

    def __init__(self):
        self.opensearch_client = self.create_opensearch_client()

    def create_opensearch_client(self):
        opensearch_url = config.OPENSEARCH_URL.replace("https://", "").replace("http://", "").split(':')
        host = opensearch_url[0]
        port = opensearch_url[1]
        return OpenSearch(
            hosts=[{'host': host, 'port': port}],
            use_ssl=False,  # True when hosted
            verify_certs=False,
            ssl_assert_hostname=False,
            ssl_show_warn=False,
            connection_class=RequestsHttpConnection
        )

    def delete_file(self, project_id, file_id):
        try:
            # Get file model
            file_model = FilePynamoDBModel.query(file_id).next()

            # Delete from index
            index_name = f"knowledge_{project_id}"          # try storing this in some project specific config
            self.delete_file_from_opensearch(index_name=index_name, file_id=file_id)

            # Delete file and corresponding artifacts from local file system
            self.delete_file_from_disk(file_path=file_model.file_path)
            for item in file_model.artifacts:
                self.delete_file_from_disk(file_path=item.file_path)

            # Delete file model
            file_model.delete()
            return True
        except Exception as e:
            logging.error(e)
            return False

    @staticmethod
    def delete_file_from_disk(file_path):
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)  # Delete the file
                print(f"Deleted file: {file_path}")
            else:
                print(f"File does not exist: {file_path}")
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")
    
    def delete_file_from_opensearch(self, index_name, file_id):
        logging.info(f"Deleting existing pages from index")
        response = self.opensearch_client.delete_by_query(
            index=index_name,
            body={
                "query": {
                    "term": {
                        "metadata.file_id.keyword": str(file_id)
                    }
                }
            }
        )

        if response['deleted'] > 0:
            logging.info("Documents deleted successfully")
        else:
            logging.info("No documents deleted")

    @staticmethod
    def stream_zip_file(file_model) -> Generator[bytes, None, None]:
        zip_buffer = io.BytesIO()
        failed_files: List[Tuple[str, str]] = []
        
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
            # Add the main file
            try:
                with open(file_model.file_path, 'rb') as file:
                    zf.writestr(file_model.file_name, file.read())
            except Exception as e:
                logging.error(f"Failed to add main file {file_model.file_name}: {str(e)}")
                failed_files.append((file_model.file_name, str(e)))
            
            # Add artifacts
            for item in file_model.artifacts:
                try:
                    with open(item.file_path, 'rb') as file:
                        zf.writestr(item.file_name, file.read())
                except Exception as e:
                    logging.error(f"Failed to add artifact {item.file_name}: {str(e)}")
                    failed_files.append((item.file_name, str(e)))
        
        # Reset buffer position
        zip_buffer.seek(0)
        
        # Log summary of failed files
        if failed_files:
            logging.warning(f"Failed to add {len(failed_files)} file(s) to the zip archive:")
            for file_name, error in failed_files:
                logging.warning(f"  - {file_name}: {error}")
        
        # Yield the zip content in chunks
        while True:
            chunk = zip_buffer.read(8192)
            if not chunk:
                break
            yield chunk

    def download_file(self, file_id: str) -> Generator[bytes, None, None]:
        file_model = FilePynamoDBModel.get(file_id)
        if not file_model:
            raise ValueError(f"File with id {file_id} not found")
        
        logging.info(f"Downloaded file model: {file_model}")
        
        # Stream zip file generator
        return [self.stream_zip_file(file_model), file_model.file_name]