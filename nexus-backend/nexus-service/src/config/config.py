from enum import Enum
from pydantic_settings import BaseSettings

class EnvironmentType(str, Enum):
    SANDBOX = "sandbox"
    PROD = "prod"
    
class BaseConfig(BaseSettings):
    class Config:
        case_sensitive = True

class Config(BaseConfig):
    DEBUG: int = 0
    DEFAULT_LOCALE: str = "en_US"
    ENVIRONMENT: str = EnvironmentType.SANDBOX
    PS_CHAT_API_KEY: str| None = ""
    OPENAI_API_KEY: str| None = ""
    ORIGINS: list[str] | str = ["http://localhost:8181", "http://localhost:3000"]
    LOCALSTACK_URL: str = "http://localhost:4566"
    API_VERSION:str = "/nexus/v1"
    OPENSEARCH_URL: str = "http://localhost:9200"
    KNOWLEDGE_BASE_ROOT_DIR: str = "C:/Users/adhreghu/Documents/Learning/howathon_2024/nexus/nexus-backend/nexus-service/src/.knowledge-base"
    ENCRYPTION_KEY: str = ""

config: Config = Config()