"""
Information API
"""
from containers import Container
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import routers
import helpers.const as env



tags_metadata = [
    {
        "name": "admin",
        "description": "Admin",
        "externalDocs": {
            "description": "docs",
            "url": env.URL_DOC,
        },
    },
    # {
    #     "name": "member",
    #     "description": "Member",
    #     "externalDocs": {
    #         "description": "docs",
    #         "url": env.URL_DOC,
    #     },
    # },
]


container = Container()
container.wire(packages=[routers])
app = FastAPI(openapi_tags=tags_metadata, docs_url="/api/v1/docs", redoc_url=None, openapi_url="/api/v1/openapi.json")
app.container = container

# Include child routers
app.include_router(routers.admin_routers)
# app.include_router(routers.member_routers)

origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
