#Section 9: Working with file
"""
    File
        Declared similarly to Form fields
            Ex: def get_file(file: bytes = Files(...))
        Received as bytes
        Stored in memory

    UploadFile
        Provides mỏe functionality
        Stored in memory up to a certain size, the on disk
        Python file  like object

    Making files statically available
        Ex: app.mount('/files', StaticFiles(directory='files'), name='files')

    Downloading files
        Provide more logic around file access
        Provide security

"""


from fastapi import FastAPI, Depends,Request, status
from typing import Optional
from db.database import engine
from models import user
from routers import router_user, router_article, router_product, router_file
from exceptions import CommonException
from fastapi.responses import JSONResponse, PlainTextResponse
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from auth import authentication
from fastapi.staticfiles import StaticFiles


app = FastAPI()
app.include_router(authentication.router)
app.include_router(router_user.router)
app.include_router(router_article.router)
app.include_router(router_product.router)
app.include_router(router_file.router)
def required_functionality():
    return {'message': 'Learning FastAPI is important'}


@app.get('/blog/all')
def get_all_blog(page = 1, page_size: Optional[int] = None, req_parameter: dict = Depends(required_functionality)):
    return {'message': 'Get all blog', 'req': req_parameter}

# CommonException
@app.exception_handler(CommonException)
def common_exception_handler(request: Request, exc: CommonException):
    return JSONResponse(
        status_code=status.HTTP_418_IM_A_TEAPOT,
        content={'detail': exc.name}
    )

# HTTPException
# @app.exception_handler(HTTPException)
# def custom_handler(request: Request, exc: CommonException):
#     return PlainTextResponse(str(exc), status_code=status.HTTP_404_NOT_FOUND)

user.Base.metadata.create_all(engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)
# Watch static file
app.mount('/files', StaticFiles(directory='files'), name='files')