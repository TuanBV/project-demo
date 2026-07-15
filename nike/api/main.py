from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from containers import Container
from settings import settings
import router

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


LANGUAGES = {
    "en": "English",
    "vi": "Vietnamese"
}

container = Container()
container.wire(packages=[router])
app = FastAPI(openapi_tags=tags_metadata, docs_url="/docs", redoc_url=None, openapi_url="/openapi.json")


@app.middleware("http")
async def add_cache_control_header(request, call_next):
    response = await call_next(request)
    if request.url.path.startswith("/upload"):
        response.headers["Cache-Control"] = "no-store"  # Hoặc "no-cache" tùy nhu cầu
    return response


app.mount("/upload", StaticFiles(directory="upload"), name="upload")
app.container = container

app.include_router(router.health_router)
app.include_router(router.user_router)
app.include_router(router.post_router)
app.include_router(router.category_router)
app.include_router(router.kind_router)
app.include_router(router.sale_router)
app.include_router(router.image_router)
app.include_router(router.product_router)
app.include_router(router.setting_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)
