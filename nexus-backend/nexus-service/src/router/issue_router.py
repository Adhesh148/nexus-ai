from fastapi import APIRouter, Query
from typing import List
import logging

from service.issue_service import IssueService

logger = logging.getLogger()
logger.setLevel(logging.INFO)

issue_router = APIRouter(prefix="/issue", tags=["Issue"])
issue_service = IssueService()

@issue_router.post("/draft_issues")
async def draft_issues(article_ids: List[str], session_id: str = Query(...), project_id: str = Query(...)):
    logging.info(f"Recieved request to draft issues for articles:{article_ids}, project: {project_id} and session: {session_id}")
    issues = issue_service.draft_issues(article_ids=article_ids, project_id=project_id)
    return issues

@issue_router.get("/issues")
async def get_all_issues(session_id: str = Query(...), project_id: str = Query(...)):
    logging.info(f"Recieved request to retrieve all issues for project: {project_id} and session: {session_id}")

    return issue_service.get_all_issues(project_id=project_id)

@issue_router.delete("/delete_issue")
async def delete_issue(issue_id: str = Query(...), session_id: str = Query(...), project_id: str = Query(...)):
    logging.info(f"Recieved request to delete issue: {issue_id} for project: {project_id} and session: {session_id}")

    status = issue_service.delete_issue(issue_id=issue_id, project_id=project_id)
    return status

@issue_router.post("/create_issue")
async def create_issue(issue_id: str = Query(...), session_id: str = Query(...), project_id: str = Query(...)):
    logging.info(f"Recieved request to create issue: {issue_id} for project: {project_id} and session: {session_id}")

    new_issue = issue_service.create_issue(issue_id=issue_id, project_id=project_id)
    return new_issue
