import logging
import os
import shutil
from uuid import uuid4
from datetime import datetime
from enum import Enum

from fastapi import UploadFile
from config.config import config
from models.file_model import FileModel, FilePynamoDBModel
from service.embedding_service import EmbeddingService
from service.audio_service import AudioService
from service.image_service import ImageService
from utils import utils
from utils.utils import FileType

logger = logging.getLogger()
logger.setLevel(logging.INFO)

class FileProcessingService():

    def __init__(self, project_id: str):
        self.project_id = project_id
        self.embedding_service = EmbeddingService(project_id=project_id)
        self.audio_service = AudioService()
        self.image_service = ImageService()

    def process_file(self, file: UploadFile) -> FileModel:
        logging.info(f"Started processing file: {file.filename}")

        # Store the file in local file system -- get file path
        file_path = self.write_to_disk(file, self.project_id)
        file_type = self.determine_file_type(file.filename)
        logging.info(f"Determined file type: {file_type}")
        file_model = FilePynamoDBModel(
            file_id=str(uuid4()),
            project_id=self.project_id,
            file_name=file.filename,
            file_type=file_type,
            file_path=file_path,
            is_active=True,
            created_at=datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            artifacts=[]
        )
        file_model.save()

        # Create file artifacts -- if needed and store in file system
        file_model = self.create_file_artifacts(file_model=file_model)

        # Create embeddings of the text based artifact for the file and store in vector store
        text_artifact_file = utils.get_text_artifact(file_model=file_model)
        self.embedding_service.create_embeddings(file=text_artifact_file)

        return file_model.to_pydantic()

    @staticmethod
    def write_to_disk(file: UploadFile, project_id):
        project_base_dir = f"{config.KNOWLEDGE_BASE_ROOT_DIR}/{project_id}/"
        os.makedirs(project_base_dir, exist_ok=True)

        file_location = os.path.join(project_base_dir, file.filename)
        logging.info(f"Writing file {file.filename} to location: {file_location}")
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        return file_location

    def create_file_artifacts(self, file_model: FilePynamoDBModel):
        """
        This function creates artifacts for uploaded file. For eg. uploaded image will have a
        description of the image as its artifact, similarly audio/video will have transcription document
        as its artifacts.
        Text documents generally do not generate additional artifacts -- but can have a compressed text as artifact if too long

        Save the file model with updated artifacts list
        """
        if file_model.file_type == FileType.AV:
            logging.info(f"Starting processing audio/video file: {file_model.file_name}")
            updated_file_model = self.audio_service.preprocess_av_file(file=file_model)
            return updated_file_model
        if file_model.file_type == FileType.IMAGE:
            logging.info(f"Starting processing for image file: {file_model.file_name}")
            updated_file_model = self.image_service.process_image_file(file=file_model)
            return updated_file_model
        return file_model

    @staticmethod
    def determine_file_type(file_name):
        """
        Determines the file type based on the file extension
        """
        file_extn = os.path.splitext(file_name)[-1][1:]
        logging.info(f"File extn is {file_extn}")
        if file_extn in ['jpg', 'jpeg', 'png', 'svg', 'gif']:
            return FileType.IMAGE
        elif file_extn in ['mp3', 'mp4', 'wav', 'm4a']:
            return FileType.AV
        return FileType.TEXT