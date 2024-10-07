from atlassian import Jira
from models.project_model import ProjectPynamoDBModel

import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

class JiraService:

    def __init__(self, project_id):
        logging.info(f"Retrieving JRIA secrets for project id: {project_id}")
        self._secrets = self.get_jira_secrets(project_id=project_id)
        self.project_key = self._secrets["JIRA_PROJECT_KEY"]
        self.project_url = self._secrets["JIRA_URL"]
        self.client = self.create_jira_client()

    def get_jira_secrets(self, project_id):
        project_model = ProjectPynamoDBModel.query(project_id).next()
        jira_config = project_model.configs["jira"]
        return {
            "JIRA_URL": jira_config["url"],
            "JIRA_USERNAME": jira_config["username"],
            "JIRA_PASSWORD": jira_config["token"],
            "JIRA_PROJECT_KEY": jira_config["projectKey"]
        }
    
    def create_jira_client(self):
        return Jira(
            url=self._secrets["JIRA_URL"],
            username=self._secrets["JIRA_USERNAME"],
            password=self._secrets["JIRA_PASSWORD"],
            cloud=True
        )
    
    def get_issues_for_release(self, release_name: str):
        logging.info(f"Getting issues for release: {release_name}")
        jql_query = f'project = {self.project_key} AND fixVersion = "{release_name}"'
        issues = self.client.jql(jql=jql_query)
        
        # Extract keys of the issues
        info = {}
        for issue in issues['issues']:
            info[issue['key']] = {
                'summary': issue['fields']['summary'],
                'description': issue['fields']['description'],
            }
        return info

if __name__ == '__main__':
    jira = JiraService(project_id=101)

    # versions = jira.client.get_project_versions(key=jira.project_key)
    # print(versions)

    # print(jira.get_project_releases())
    jql_query = f'project = KAN AND fixVersion = "release/0.1.0"'
    issues = jira.client.jql(jql=jql_query)
    for issue in issues['issues']:
         print(issue['key'])
