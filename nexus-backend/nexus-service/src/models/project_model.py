from pydantic import BaseModel, Field, HttpUrl
from typing import Union, Optional, Dict
from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute
import json

from config.config import config
from models.encrypted_attribute import EncryptedUnicodeAttribute

"""
Define Pydantic and PynamoDB models
"""
# Base configuration model
class BaseConfig(BaseModel):
    platform: str  # Should be one of 'github', 'jira', or 'confluence'

# Specific configuration models extending BaseConfig
class GithubConfig(BaseConfig):
    platform: str = 'github'
    token: str
    repoName: str

class ConfluenceConfig(BaseConfig):
    platform: str = 'confluence'
    username: str
    url: HttpUrl
    token: str

class JiraConfig(BaseConfig):
    platform: str = 'jira'
    username: str
    url: HttpUrl
    token: str
    projectKey: str

# Project model including a list of configurations
class ProjectModel(BaseModel):
    project_id: str
    project_name: str
    project_desc: Optional[str] = None
    configs: Dict[str, Dict[str, Union[str, int]]]

    class Config:
        # Ensures that the enums are treated as strings in the model
        use_enum_values = True

class ProjectPynamoDBModel(Model):
    class Meta:
        table_name = 'projects'
        host = config.LOCALSTACK_URL

    project_id = UnicodeAttribute(hash_key=True)
    project_name = UnicodeAttribute()
    project_desc = UnicodeAttribute(null=True)
    _encrypted_configs = EncryptedUnicodeAttribute(encryption_key=config.ENCRYPTION_KEY)

    @property
    def configs(self) -> Dict[str, Dict[str, Union[str, int]]]:
        encrypted_data = self._encrypted_configs
        if encrypted_data:
            json_data = json.loads(encrypted_data)
            # Convert the list of configurations to a dictionary of configurations
            configs = {}
            for config_data in json_data:
                platform = config_data.get("platform")
                if platform:
                    configs[platform] = self._deserialize_config(config_data)
            return configs
        return {}

    @configs.setter
    def configs(self, value: Dict[str, Dict[str, Union[str, int]]]):
        # Convert the dictionary of configurations to a list of dictionaries
        config_list = []
        for platform, config in value.items():
            config_list.append(config)
        # Serialize configuration dictionaries to JSON
        json_data = json.dumps(config_list)
        self._encrypted_configs = json_data

    def _deserialize_config(self, data: Dict[str, Union[str, int]]) -> Dict[str, Union[str, int]]:
        platform = data.get("platform")
        if platform == 'github':
            return GithubConfig(**data).dict()
        elif platform == 'confluence':
            return ConfluenceConfig(**data).dict()
        elif platform == 'jira':
            return JiraConfig(**data).dict()
        else:
            raise ValueError(f"Unknown platform: {platform}")

    def to_pydantic(self) -> ProjectModel:
        """Converts a PynamoDB model instance to a Pydantic model instance."""
        return ProjectModel(
            project_id=self.project_id,
            project_name=self.project_name,
            project_desc=self.project_desc,
            configs={}
        )

