from models.file_model import FilePynamoDBModel, ArtifactAttribute
from prompts.chat_prompts import IMAGE_DESCRIPTION_PROMPT
from config.model_config import create_chat_model
from utils.utils import FileType

from langchain_core.messages import HumanMessage

from datetime import datetime
import logging
from pathlib import Path
import base64
import os
from uuid import uuid4

logger = logging.getLogger()
logger.setLevel(logging.INFO)

class ImageService:
    
    def __init__(self):
        self.vision_model = create_chat_model()

    def process_image_file(self, file: FilePynamoDBModel):
        """
        Preprocess the audio/video file and returns the preprocessed file
        """
        logging.info(f"Starting image processing for file: {file.file_name}")
        
        base64_image = self.encode_image(file.file_path)
        ts = datetime.now().strftime("%Y%m%dT%H%M%S")
        dest_file_name = Path(file.file_name).stem + f"_description_{ts}.txt"
        dest_file_path = os.path.join(file.file_path.strip(file.file_name), dest_file_name)

        # Create image description artifact
        image_description = self.get_image_description(base64_image)
        logging.info(f"Writing image description to {dest_file_path}")
        with open(dest_file_path, "w", encoding="utf-8") as f:
            f.write(image_description)

        description_artifact = ArtifactAttribute(
            file_id=str(uuid4()),
            project_id=file.project_id,
            file_name=dest_file_name,
            file_type=FileType.TEXT,
            file_path=dest_file_path,
            is_active=True,
            created_at=datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        )
        file.artifacts.append(description_artifact)
        file.save()
        return file

    @staticmethod
    def encode_image(image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    def get_image_description(self, image_data):
        """
        Creates image description of uploaded image
        """
        logging.info("Creating image description")
        message = HumanMessage(
            content=[
                {"type": "text", "text": IMAGE_DESCRIPTION_PROMPT},
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{image_data}"},
                },
            ],
        )

        response = self.vision_model.invoke([message])
        return response.content
        
