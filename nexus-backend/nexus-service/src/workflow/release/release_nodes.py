from service.jira_service import JiraService
from models.release_model import TemplatePynamoDBModel

from workflow.release.determine_node import fields_determiner
from workflow.release.gather_node import gatherer
from workflow.release.combine_node import combiner
from workflow.release.refine_node import refiner

import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# ---------- NODES -------------
def load(state):
    """
    Load issues relevant to the release

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): New key added to state, documents, that contains retrieved documents
    """
    logging.info("[RELEASE-GRAPH] Loading Documents............")
    release_name = state["release_name"]
    project_id = state["project_id"]

    # Initialize jira service and get all jira issues of the release
    jira_service = JiraService(project_id=project_id)
    issues = jira_service.get_issues_for_release(release_name=release_name)

    return {"issues": issues}

def determine_fields(state):
    """
    Determines the important fields to be extracted based on the template 
    Eg:
    important_fields: [fixes, changes]
    """
    logging.info("[RELEASE-GRAPH] Determining Important fields ............")
    template_id = state["template_id"]
    template_model = TemplatePynamoDBModel.query(template_id).next()

    response = fields_determiner.invoke({"template_content": template_model.template_content}).content
    return {"required_fields_info": response}

def gather(state):
    """
    From the issues key gather the relevant information for the 
    """
    logging.info("[RELEASE-GRAPH] Gathering relevant information from each issue ............")
    issues = state["issues"]
    fields_info = state["required_fields_info"]

    gathered_info = {}
    for key in issues:
        issue_input = f"Issue: {key}\nSummary: {issues[key]['summary']}\nDescription: {issues[key]['description']}"
        response = gatherer.invoke({"issue_input": issue_input, "fields_info": fields_info}).content
        gathered_info['key'] = response
    
    return {"gathered_info": gathered_info}

def combine(state):
    """
    Combine all gathered info into a single template
    """
    logging.info("[RELEASE-GRAPH] Combining all gathered info and removing duplicates ............")

    gathered_info = state["gathered_info"]
    fields_info = state["required_fields_info"]

    combined_info = []
    for key, info in gathered_info.items():
        combined_info.append(f"Issue Key: {key}\n{info}")
    
    response = combiner.invoke({"extracted_info": combined_info, "fields_info": fields_info}).content
    return {"combined_info": response}

def refine(state):
    """
    Refines the combined information into the template format
    """
    logging.info("[RELEASE-GRAPH] Refining the combined information into the final release note ............")
    combined_info = state["combined_info"]
    template_id = state["template_id"]
    template_model = TemplatePynamoDBModel.query(template_id).next()

    response = refiner.invoke({"combined_info": combined_info, "template_content": template_model.template_content}).content
    return {"generated_release_note": response}


