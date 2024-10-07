from fastapi import APIRouter, UploadFile, Query
from fastapi.responses import StreamingResponse
from typing import List
import logging

from service.file_processing_service import FileProcessingService
from service.knowledge_service import KnowledgeService
from models.file_model import FilePynamoDBModel

logger = logging.getLogger()
logger.setLevel(logging.INFO)

knowledge_service = KnowledgeService()
knowledge_router = APIRouter(prefix="/knowledge", tags=["Knowledge"])

@knowledge_router.post("/upload_files")
async def upload_files(files: List[UploadFile], session_id: str = Query(...), project_id: str = Query(...)):
    logging.info(f"Recieved request to upload files for project: {project_id} and session: {session_id}")

    # initialize file processing service
    file_processing_service = FileProcessingService(project_id=project_id)

    file_models = []
    for file in files:
        logging.info(f"Processing file {file.filename}")
        file_models.append(file_processing_service.process_file(file=file))

    return file_models

@knowledge_router.get("/files")
async def get_all_files(session_id: str = Query(...), project_id: str = Query(...)):
    logging.info(f"Recieved request to retrieve all files for project: {project_id} and session: {session_id}")

    result = FilePynamoDBModel.scan(FilePynamoDBModel.project_id == project_id)
    files = [item.to_pydantic() for item in result]
    return files

@knowledge_router.delete("/delete_file")
async def delete_file(file_id: str = Query(...), session_id: str = Query(...), project_id: str = Query(...)):
    logging.info(f"Recieved request to delete file: {file_id} for project: {project_id} and session: {session_id}")

    status = knowledge_service.delete_file(project_id=project_id, file_id=file_id)
    return status

@knowledge_router.get("/download_file")
async def download_file(file_id: str = Query(...), session_id: str = Query(...), project_id: str = Query(...)):
    logging.info(f"Recieved request to download file: {file_id} for project: {project_id} and session: {session_id}")

    file_stream, file_name = knowledge_service.download_file(file_id=file_id)
    
    # Return the streaming response
    return StreamingResponse(file_stream, media_type="application/x-zip-compressed", headers={
        "Content-Disposition": f"attachment; filename={file_name}.zip"
    })