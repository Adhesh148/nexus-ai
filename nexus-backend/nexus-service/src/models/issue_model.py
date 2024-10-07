from pydantic import BaseModel, Field

from pynamodb.attributes import UnicodeAttribute, BooleanAttribute, NumberAttribute
from pynamodb.models import Model

from config.config import config

class IssueModel(BaseModel):
    issue_id: str = Field(None, description="Unique ID of the issue")
    project_id: str = Field(None, description="Unique ID of the project to which issue belongs")
    issue_type: str = Field(None, description="Type of issue like story or bug")
    summary: str = Field(None, description="Summary of the issue")
    description: str = Field(None, description="Detailed description of the issue")
    priority: str = Field(None, description="Priority of issue")
    story_points: int = Field(None, description="Story point estimate")
    is_active: bool = Field(True, description="Is issue active?")
    is_staging: bool = Field(True, description="Is issue active?")
    issue_url: str = Field(None, description="URL of the issue")

class IssuePynamoDBModel(Model):
    """
    DynamoDB Issue Model
    """
    class Meta:
        table_name = "project_issues"
        host = config.LOCALSTACK_URL
    
    issue_id = UnicodeAttribute(hash_key=True)
    project_id = UnicodeAttribute()
    issue_type = UnicodeAttribute()
    summary = UnicodeAttribute()
    description = UnicodeAttribute()
    priority = UnicodeAttribute()
    story_points = NumberAttribute()
    is_active = BooleanAttribute(default=True)
    is_staging = BooleanAttribute(default=True)
    issue_url = UnicodeAttribute(default="")

    def to_pydantic(self) -> IssueModel:
        """Converts a PynamoDB model instance to a Pydantic model instance."""
        return IssueModel(
            issue_id=self.issue_id,
            project_id=self.project_id,
            issue_type=self.issue_type,
            summary=self.summary,
            description=self.description,
            priority=self.priority,
            story_points=self.story_points,
            is_active=self.is_active,
            is_staging=self.is_staging,
            issue_url=self.issue_url
        )