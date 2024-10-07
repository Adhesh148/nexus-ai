from fastapi import APIRouter, Query
from typing import List
import logging

from service.release_service import ReleaseService
from models.release_model import ReleaseModel, TemplateModel

logger = logging.getLogger()
logger.setLevel(logging.INFO)

release_router = APIRouter(prefix="/release", tags=["Release"])
release_service = ReleaseService()

@release_router.get('/releases', response_model=List[ReleaseModel])
async def get_all_releases(session_id: str = Query(...), project_id: str = Query(...)): 
    logging.info(f"Recieved request to retrieve all releases for project: {project_id} and session: {session_id}")
    release_models = release_service.get_releases_for_project(project_id=project_id)

    return release_models

@release_router.get('/templates', response_model=List[TemplateModel])
async def get_all_templates(session_id: str = Query(...), project_id: str = Query(...)):
    logging.info(f"Recieved request to retrieve all templates for project: {project_id} and session: {session_id}")
    return release_service.get_all_templates(project_id=project_id)

@release_router.post('/create_template', response_model=TemplateModel)
async def create_template(template_info: TemplateModel, session_id: str = Query(...), project_id: str = Query(...)):
    logging.info(f"Recieved request to create new template for project: {project_id} and session: {session_id}")
    new_template = release_service.create_template(template_info=template_info, project_id=project_id)
    return new_template

@release_router.post('/create_release_note')
async def create_release_note(release_name: str = Query(...), template_id: str = Query(...), session_id: str = Query(...), project_id: str = Query(...)):
    logging.info(f"Recieved request to create release note for project: {project_id} and session: {session_id}")
    return release_service.create_release_note(project_id=project_id, release_name=release_name, template_id=template_id)

