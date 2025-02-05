from fastapi import FastAPI
from models import model
# from db.database import engine
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from containers import Container
import router
from task import add_task
from pydantic import BaseModel

tags_metadata = [
    {
        "name": "API",
        "description": "API for Project",
        "externalDocs": {
            "description": "docs",
            "url": "http://localhost:8000/docs/",
        },
    },
]

container = Container()
container.wire(packages=[router])
app = FastAPI(openapi_tags=tags_metadata, docs_url="/docs", redoc_url=None, openapi_url="/openapi.json")
app.mount("/upload", StaticFiles(directory="upload"), name="upload")
app.container = container

app.include_router(router.user_router)
app.include_router(router.post_router)

class TaskRequest(BaseModel):
    x: int
    y: int

@app.post("/task")
async def create_task(task: TaskRequest):
    print("--------------------------------")
    task_result = add_task.delay(task.x, task.y)
    print("--------------------------------111111")

    return {"task_id": task_result.id, "status": "Task added to queue"}

origins = [
    'https://localhost:5000',
    'http://localhost:5000',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


# model.Base.metadata.create_all(engine)
