from typing import Dict, Any
from fastapi import Request
from models.file_model import FileModel, FilePynamoDBModel
from langchain_community.document_loaders import TextLoader, Docx2txtLoader, JSONLoader, CSVLoader, PyPDFLoader
import os
from enum import Enum

class FileType(str, Enum):
    IMAGE = "image"
    AV = "audio/video"
    TEXT = "text"

async def per_req_config_modifier(config: Dict[str, Any], request: Request) -> Dict[str, Any]:
    config = config.copy()
    configurable = config.get("configurable", {})

    session_id = configurable["session_id"] if configurable.get("session_id") else request.query_params.get("session_id")
    configurable["session_id"] = session_id
    
    project_id = configurable["project_id"] if configurable.get("project_id") else request.query_params.get("project_id")
    configurable["project_id"] = project_id
    
    config["configurable"] = configurable
    return config


def load_documents(file: FileModel):
        ext = os.path.splitext(file.file_name)[1][1:]
        if ext in ['docx', 'doc']:
            loader = Docx2txtLoader(file_path=file.file_path)
        elif ext in ['csv']:
            laoder = CSVLoader(file_path=file.file_path)
        elif ext in ['json']:
            loader = JSONLoader(file_path=file.file_path)
        elif ext in ['pdf']:
            loader = PyPDFLoader(file_path=file.file_path)
        else:
            loader = TextLoader(file_path=file.file_path)
        
        documents = loader.load()
        return documents

def get_text_artifact(file_model: FilePynamoDBModel) -> FileModel:
    """
    Get the text artifact file model for which we will run the embedding model and store in vector store
    """
    if file_model.file_type == FileType.TEXT:
        return file_model.to_pydantic()
    else:
        for artifact in file_model.artifacts:
            if artifact.file_type == FileType.TEXT:
                return FileModel(
                    file_id=artifact.file_id,
                    project_id=artifact.project_id,
                    file_name=artifact.file_name,
                    file_type=artifact.file_type,
                    file_path=artifact.file_path,
                    is_active=artifact.is_active,
                    created_at=artifact.created_at,
                    artifacts=[]
                )
    return None