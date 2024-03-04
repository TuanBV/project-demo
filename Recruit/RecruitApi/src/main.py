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
        "name": "Recruit API",
        "description": "API for Recruit Project",
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
app.include_router(routers.user_routers)
app.include_router(routers.recommender_routers)
app.include_router(routers.candidate_routers)
app.include_router(routers.position_routers)
app.include_router(routers.team_routers)
app.include_router(routers.template_routers)
app.include_router(routers.parameter_routers)
app.include_router(routers.offices_routers)
app.include_router(routers.mail_routers)
app.include_router(routers.candidate_confirm_routers)
app.include_router(routers.candidates_routers)
app.include_router(routers.meeting_room_routers)
app.include_router(routers.black_list_routers)
app.include_router(routers.candidate_pass_list_routers)
app.include_router(routers.staff_routers)

origins = [
  "http://localhost",
  "http://localhost:9000",
]

app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)
