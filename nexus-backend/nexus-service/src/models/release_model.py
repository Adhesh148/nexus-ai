from pydantic import BaseModel, Field

from pynamodb.attributes import UnicodeAttribute, BooleanAttribute, NumberAttribute
from pynamodb.models import Model

from config.config import config

class ReleaseModel(BaseModel):
    release_id: str = Field(None, description="Unique ID of the release")
    release_name: str = Field(None, description="Name of the release")
    project_id: str = Field(None, description="Unique ID of the project to which release belongs")

class TemplateModel(BaseModel):
    template_id: str = Field(None, description="Unique ID of the template")
    template_name: str = Field(None, description="Name of the template")
    project_id: str = Field(None, description="Unique ID of the project to which template belongs")
    template_content: str = Field(None, description="Content of the template")

class TemplatePynamoDBModel(Model):
    """
    DynamoDB Issue Model
    """
    class Meta:
        table_name = "project_templates"
        host = config.LOCALSTACK_URL
    
    template_id = UnicodeAttribute(hash_key=True)
    template_name = UnicodeAttribute()
    project_id = UnicodeAttribute()
    template_content = UnicodeAttribute()

    def to_pydantic(self) -> TemplateModel:
        """Converts a PynamoDB model instance to a Pydantic model instance."""
        return TemplateModel(
            template_id=self.template_id,
            template_name=self.template_name,
            project_id=self.project_id,
            template_content=self.template_content
        ) 
