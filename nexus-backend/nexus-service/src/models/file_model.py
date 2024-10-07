from pydantic import BaseModel, Field
from typing import List

from pynamodb.attributes import UnicodeAttribute, BooleanAttribute, ListAttribute, MapAttribute
from pynamodb.models import Model


from config.config import config

class FileModel(BaseModel):
    file_id: str = Field(None, description="Unique ID of the file")
    project_id: str = Field(None, description="Unique ID of project")
    file_name: str = Field(None, description="Name of file")
    file_type: str = Field(None, description="Type of file")
    file_path: str = Field(None, description="File path")
    is_active: bool = Field(True, description="Is file active?")
    created_at: str = Field(None, description="File created timestamp")
    artifacts: List['FileModel'] = Field(default_factory=list, description="List of related file artifacts")

# Define DynamoDB classes
class ArtifactAttribute(MapAttribute):
    file_id = UnicodeAttribute()
    project_id = UnicodeAttribute()
    file_name = UnicodeAttribute()
    file_type = UnicodeAttribute()
    file_path = UnicodeAttribute()
    is_active = BooleanAttribute(default=True)
    created_at = UnicodeAttribute()

class FilePynamoDBModel(Model):
    """
    DynamoDB File Model
    """
    class Meta:
        table_name = "project_files"
        host = config.LOCALSTACK_URL
    
    file_id = UnicodeAttribute(hash_key=True)
    project_id = UnicodeAttribute()
    file_name = UnicodeAttribute()
    file_type = UnicodeAttribute()
    file_path = UnicodeAttribute()
    is_active = BooleanAttribute(default=True)
    created_at = UnicodeAttribute()
    artifacts = ListAttribute(of=ArtifactAttribute, default=list)

    def to_pydantic(self) -> FileModel:
        """Converts a PynamoDB model instance to a Pydantic model instance."""
        return FileModel(
            file_id=self.file_id,
            project_id=self.project_id,
            file_name=self.file_name,
            file_type=self.file_type,
            file_path=self.file_path,
            is_active=self.is_active,
            created_at=self.created_at,
            artifacts=[
                FileModel(**artifact.attribute_values) for artifact in self.artifacts
            ]
        )

