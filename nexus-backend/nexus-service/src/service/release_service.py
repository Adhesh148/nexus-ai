from service.jira_service import JiraService
from models.release_model import ReleaseModel, TemplateModel, TemplatePynamoDBModel
from workflow.release.release_graph import release_graph

from typing import List
from uuid import uuid4
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

class ReleaseService():

    def __init__(self):
        self.jira_services = {}  # Dictionary to store JiraService instances keyed by project_id

    def _get_jira_service(self, project_id: int) -> JiraService:
        # Create or retrieve a JiraService instance for the given project_id
        if project_id not in self.jira_services:
            self.jira_services[project_id] = JiraService(project_id=project_id)
        return self.jira_services[project_id]

    def get_releases_for_project(self, project_id) -> List[ReleaseModel]:
        jira = self._get_jira_service(project_id)

        # Retrieve versions for the project
        versions = jira.client.get_project_versions(key=jira.project_key)
        
        # Create ReleaseModel instances from the retrieved versions
        release_models = [
            ReleaseModel(
                release_id=version['id'],
                release_name=version['name'],
                project_id=project_id  # Use the provided project_id
            )
            for version in versions
        ]
        
        return release_models
    
    def get_all_templates(self, project_id):
        result = TemplatePynamoDBModel.scan(TemplatePynamoDBModel.project_id == project_id)
        templates = [item.to_pydantic() for item in result]
        return templates
    
    def create_template(self, template_info: TemplateModel, project_id):
        try:
            # Create new template
            new_template_model = TemplatePynamoDBModel(
                template_id = str(uuid4()),
                template_name = template_info.template_name,
                template_content = template_info.template_content,
                project_id = project_id
            )
            new_template_model.save()

            return new_template_model.to_pydantic()
        except Exception as e:
            logging.error(f"Error while creating new template: {e}")

    def update_template(self, project_id, template_id):
        pass

    def create_release_note(self, project_id, release_name, template_id):
        inputs = {"release_name": release_name, "project_id": project_id, "template_id": template_id}
        for output in release_graph.stream(inputs):
            for key, value in output.items():
                logging.info(f"Node '{key}':")
    
        response = value["generated_release_note"]
        return response
