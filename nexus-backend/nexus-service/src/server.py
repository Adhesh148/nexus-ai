import logging
import os

import uvicorn
from fastapi import FastAPI
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from langserve import add_routes

from config.config import config
from router.project_router import project_router
from router.knowledge_router import knowledge_router
from router.issue_router import issue_router
from router.release_router import release_router
from runnable.chat_runnable import ChatRunnable
from utils.utils import per_req_config_modifier

def init_routers(app_: FastAPI) -> None:
    app_.include_router(project_router, prefix=config.API_VERSION)
    app_.include_router(knowledge_router, prefix=config.API_VERSION)
    app_.include_router(issue_router, prefix=config.API_VERSION)
    app_.include_router(release_router, prefix=config.API_VERSION)

    add_routes(
        app_,
        ChatRunnable(),
        path=f"{config.API_VERSION}/chat",
        enabled_endpoints=["invoke"],
        per_req_config_modifier=per_req_config_modifier
    )

def make_middleware():
    middleware = [
        Middleware(
            CORSMiddleware,
            allow_origins=config.ORIGINS,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
            expose_headers=["*"],
        )
    ]

    return middleware

def create_app():
    app_ = FastAPI(
        title="nexus",
        description="Nexus AI Application",
        version="1.0.0",
        docs_url=None if config.ENVIRONMENT == "prod" else "/docs",
        redoc_url=None if config.ENVIRONMENT == "prod" else "/redoc",
        middleware=make_middleware()
    )

    init_routers(app_=app_)

    return app_

app = create_app()

if __name__ == "__main__":
    uvicorn.run(app="server:app",
                host="0.0.0.0",
                port=8181,
                reload=True,
                log_level="info")
    