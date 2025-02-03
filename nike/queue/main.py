from fastapi import FastAPI

tags_metadata = [
    {
        "name": "API",
        "description": "Queue for Project",
        "externalDocs": {
            "description": "docs",
            "url": "http://localhost:9000/docs/",
        },
    },
]

app = FastAPI(openapi_tags=tags_metadata, docs_url="/docs", redoc_url=None, openapi_url="/openapi.json")