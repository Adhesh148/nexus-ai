from fastapi import APIRouter, Query
from typing import List

from models.project_model import ProjectModel
from service.project_service import ProjectService

project_router = APIRouter(prefix="/projects", tags=["Projects"])
project_service = ProjectService()

@project_router.get("/all", response_model=List[ProjectModel])
async def get_projects():
    return project_service.get_all_projects()

@project_router.post("/create_project")
async def create_project(project: ProjectModel):
    new_project = project_service.create_project(project)
    return new_project