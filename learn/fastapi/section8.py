#Section 8
"""
    Error handling
    Custom responses
    Headers
    Cookies
    Form data
    CORS
"""

"""
    ERROR HANDLING

    Notify a client of an error
    Raising an exception anywhere stops code from running
        Ex: raising error 404
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                detail='Not found')

    RESPONSE
    Add parameters: Headers, Cookies
    different types of response
        plain text
        xml
        html
        files
        streaming

    HEADERS
    Add headers in request function definition
        Ex:
            def func(customer_header: Optional[str] = Header(None))
    Automatic conversion between '_' to '-'
    List of header
        Ex:
            def func(customer_header: Optional[List[str]] = Header(None))
    Provide custom response headers
        Ex:
            def func(response: Response):
                response.headers['c-custom-header'] = 'abc'
    
    COOKIES
    Store information on the browser
    Can accepts str, list, dict, model etc
        Ex: response.set_cookie(key='test_cookie', value='test_cookie_value')

"""

from fastapi import FastAPI, Depends,Request, status
from typing import Optional
from db.database import engine
from models import user
from routers import router_user, router_article, router_product
from exceptions import CommonException
from fastapi.responses import JSONResponse, PlainTextResponse
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.include_router(router_user.router)
app.include_router(router_article.router)
app.include_router(router_product.router)
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