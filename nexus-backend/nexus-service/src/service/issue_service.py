from typing import List
import logging

from models.file_model import FilePynamoDBModel
from models.issue_model import IssueModel, IssuePynamoDBModel
from utils import utils
from workflow.issues.issue_graph import issue_graph
from uuid import uuid4
from service.jira_service import JiraService

logger = logging.getLogger()
logger.setLevel(logging.INFO)

class IssueService():

    def __init__(self):
        self.jira_services = {}  # Dictionary to store JiraService instances keyed by project_id

    def _get_jira_service(self, project_id: int) -> JiraService:
        # Create or retrieve a JiraService instance for the given project_id
        if project_id not in self.jira_services:
            self.jira_services[project_id] = JiraService(project_id=project_id)
        return self.jira_services[project_id]
    
    def draft_issues(self, article_ids: List[str], project_id: str) -> List[IssueModel]:
        """
        Draft issues from article ids given
        """
        # Get the file ids for text artifact for each file
        text_files = []
        for article_id in article_ids:
            file_model = FilePynamoDBModel.query(article_id).next()
            text_file_model = utils.get_text_artifact(file_model=file_model)
            logging.info(f"Found text artifact: {text_file_model.file_name}")
            text_files.append(text_file_model)
        
        # Call the issue graph to get requirements
        inputs = {"files": text_files}
        for output in issue_graph.stream(inputs):
            for key, value in output.items():
                # Log issue graph progress
                logging.info(f"Node '{key}':")
        
        requirements = value["requirements"]
        
        # Load and save requirements in table
        issues = []
        for requirement in requirements:
            additional_considerations = requirement["additional_considerations"]
            description = f"""
            {requirement['description']}

            Acceptance Criteria:
            {additional_considerations.get('acceptance criteria','')}

            Assumptions:
            {additional_considerations.get('assumptions', '')}

            Dependencies:
            {additional_considerations.get('dependencies','')}
            """
            issue = IssuePynamoDBModel(
                issue_id=str(uuid4()),
                project_id=project_id,
                summary=requirement["summary"],
                issue_type=requirement["issue_type"],
                description=description,
                priority=requirement["priority"],
                story_points=requirement["story_points"],
            )       
            issue.save()
            issues.append(issue.to_pydantic())

        return issues
    
    def get_all_issues(self, project_id: str) -> List[IssueModel]:
        result = IssuePynamoDBModel.scan(IssuePynamoDBModel.project_id == project_id)
        issues = [item.to_pydantic() for item in result]
        return issues
    
    def delete_issue(self, issue_id: str, project_id: str):
        try:
            issue_model = IssuePynamoDBModel.query(issue_id).next()
            issue_model.delete()
            return True
        except Exception as e:
            logging.error(e)
            return False
        
    def create_issue(self, issue_id: str, project_id: str):
        try:
            # Create Jira client
            try:
                logging.info("Creating jira client")
                jira = self._get_jira_service(project_id=project_id)
            except Exception as e:
                print(f"Failed to create Jira client: {e}")
                return None

            # Get issue model from DynamoDB
            try:
                issue_model = IssuePynamoDBModel.query(issue_id).next()
            except Exception as e:
                print(f"Failed to retrieve issue model from DynamoDB: {e}")
                return None

            # Prepare the issue data
            issue_dict = {
                'project': {'key': jira.project_key},
                'summary': issue_model.summary,
                'description': issue_model.description,
                'issuetype': {'name': issue_model.issue_type.capitalize()},
                'priority': {'name': issue_model.priority.capitalize()},
                'customfield_10016': issue_model.story_points
            }

            # Create the issue in Jira
            try:
                new_issue = jira.client.create_issue(fields=issue_dict)
                logging.info(f"Successfully created new issue in jira: {new_issue}")
            except Exception as e:
                print(f"Failed to create issue in Jira: {e}")
                return None

            # Construct the issue URL
            issue_url = f"{jira.project_url}/browse/{new_issue['key']}"

            # Create and save the new issue model in DynamoDB
            try:
                new_issue_model = IssuePynamoDBModel(
                    issue_id=str(new_issue['key']),
                    project_id=project_id,
                    summary=issue_model.summary,
                    issue_type=issue_model.issue_type,
                    description=issue_model.description,
                    priority=issue_model.priority,
                    story_points=issue_model.story_points,
                    is_staging=False,
                    issue_url=issue_url
                )
                new_issue_model.save()
            except Exception as e:
                print(f"Failed to save new issue model in DynamoDB: {e}")
                return None

            # Delete the old issue model
            try:
                issue_model.delete()
            except Exception as e:
                print(f"Failed to delete old issue model: {e}")
                return None

            return new_issue

        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None
