"""
FastAPI
"""
from containers import Container
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import routers
import helpers.const as env

tags_metadata = [
    {
        "name": "API",
        "description": "API for Project",
        "externalDocs": {
            "description": "docs",
            "url": env.URL_DOC,
        },
    },
]

container = Container()
container.wire(packages=[routers])
app = FastAPI(openapi_tags=tags_metadata, docs_url="/api/v1/docs", redoc_url=None, openapi_url="/api/v1/openapi.json")
app.mount("/upload", StaticFiles(directory="upload"), name="upload")
app.container = container

# Include child routers
app.include_router(routers.router_user)

origins = [
  "http://localhost",
  "http://localhost:9000",
]

# CORS
app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)
