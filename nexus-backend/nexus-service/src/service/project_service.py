from uuid import uuid4
import logging

from models.project_model import ProjectPynamoDBModel, ProjectModel

logger = logging.getLogger()
logger.setLevel(logging.INFO)

class ProjectService():

    def __init__(self):
        pass

    def get_all_projects(self):
        project_models = ProjectPynamoDBModel.scan()
        return [model.to_pydantic() for model in project_models]
    
    def create_project(self, new_project: ProjectModel):
        project = ProjectPynamoDBModel(
            project_id = str(uuid4()),
            project_name = new_project.project_name,
            project_desc = new_project.project_desc
        )

        project.configs = new_project.configs

        project.save()
        logging.info(f"New project with id: {project.project_id} created successfully")
        logging.info(f"Config of saved project: {project.configs}")
        return project.to_pydantic()
    
if __name__ == "__main__":
    project_service = ProjectService()

    project_model = ProjectModel(
        project_id="101",
        project_name="Nexus AI",
        project_desc="AI powered centralized project management hub",
        configs={
            "jira": {
                "platform": "jira",
                "username": "adheshreghu@gmail.com",
                "url": "https://nexusai.atlassian.net",
                "token": "",
                "projectKey": "KAN"
            },
            "github": {
                "platform": "github",
                "token": "",
                "repoName": "Adhesh148/quellm"
            },
            "confluence": {
                "platform": "confluence",
                "username": "adheshreghu@gmail.com",
                "url": "https://nexusai.atlassian.net/wiki",
                "token": ""
            }
        }
    )

    project_service.create_project(project_model)
