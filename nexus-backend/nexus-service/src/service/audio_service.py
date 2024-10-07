import ffmpeg
from uuid import uuid4
import logging
import os
from pathlib import Path
from datetime import datetime
from openai import OpenAI

from models.file_model import FilePynamoDBModel, ArtifactAttribute
from utils.utils import FileType
from config.model_config import create_transcription_model

logger = logging.getLogger()
logger.setLevel(logging.INFO)

class AudioService:

    def __init__(self):
        self.transcription_model: OpenAI = create_transcription_model()

    def preprocess_av_file(self, file: FilePynamoDBModel):
        """
        Preprocess the audio/video file and returns the preprocessed file
        """
        logging.info(f"Starting audio/video processing for file: {file.file_name}")
        
        ts = datetime.now().strftime("%Y%m%dT%H%M%S")
        dest_file_name = Path(file.file_name).stem + f"_pre_{ts}.mp3"
        
        dest_file_path = os.path.join(file.file_path.strip(file.file_name), dest_file_name)

        logging.info(f"Starting preprocessing task for file_path: {file.file_path}")
        input = ffmpeg.input(file.file_path)
        output = ffmpeg.output(input, dest_file_path, ab='32K', ac=1, ar='16000', af='silenceremove=1:0:-30dB')

        ffmpeg.run(output)

        # Create a new file model
        proprocessed_artifact = ArtifactAttribute(
            file_id=str(uuid4()),
            project_id=file.project_id,
            file_name=dest_file_name,
            file_type=FileType.AV,
            file_path=dest_file_path,
            is_active=True,
            created_at=datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        )
        file.artifacts.append(proprocessed_artifact)
        file.save()

        # Create transcription and update artifacts
        logging.info(f"Starting transcription task")
        transcription_file_name, transcription_file_path = self._create_transcription_file(audio_file_name=proprocessed_artifact.file_name,
                                                                        audio_file_path=proprocessed_artifact.file_path)
        
        transcription_artifact = ArtifactAttribute(
            file_id=str(uuid4()),
            project_id=file.project_id,
            file_name=transcription_file_name,
            file_type=FileType.TEXT,
            file_path=transcription_file_path,
            is_active=True,
            created_at=datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        )
        file.artifacts.append(transcription_artifact)
        file.save()
        return file

    def _create_transcription_file(self, audio_file_name, audio_file_path):
        try:
            logging.info(f"Started transcription for file from path: {audio_file_path}")
            with open(audio_file_path, "rb") as audio_file:
                transcription = self.transcription_model.audio.transcriptions.create(
                    model="whisper-1", 
                    file=audio_file
                )

                # Store the transcription
                ts = datetime.now().strftime("%Y%m%dT%H%M%S")
                dest_file_name = Path(audio_file_path).stem + f"_transcription_{ts}.txt"
                dest_file_path = os.path.join(audio_file_path.strip(audio_file_name), dest_file_name)

                with open(dest_file_path, "w", encoding="utf-8") as f:
                    f.write(transcription.text)

                return dest_file_name, dest_file_path
        except Exception as e:
            logging.error(f"Error during transcription process")
            raise