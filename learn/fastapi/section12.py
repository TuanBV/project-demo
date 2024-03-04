# Section 12
"""
    Async await
        Functionality can be asynchronous
        We don't want to the execution to block
        await means the process can be paused
        async defines a function with suspendable points
    Templates
        (library: Jinja2)
    Middleware
        Function that intercepts the request and response
        Access to all related info
        Processing  before and after a request
            Ex:
                @app.middleware('http')
                async def add_middleware(request: Request, call_next):
                    ...
                    response = await call_next(request)
                    ...
                    return response

    Background tasks
        Functionality to be run after the call has been completed
        Can have access to to request and response and response
            Ex:
                @router.get('/{id}')
                def read_item(id: str, bt: BackgroundTasks):
                    bt.add_task(some_functionality, params)
    Websocket
        Two way communication (Giao tiếp 2 chiều)
        Keep connection open



"""


from fastapi import FastAPI, Depends,Request, status
from typing import Optional
from db.database import engine
from models import user
from routers import router_user, router_article, router_product, router_file
from auth import authentication
from templates import templates
from exceptions import CommonException
from fastapi.responses import JSONResponse, PlainTextResponse, HTMLResponse
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import time
from client import html
from fastapi.websockets import WebSocket

app = FastAPI()
app.include_router(templates.router)
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

# Websocket
@app.get('/websocket/chat')
async def chat_ws():
    return HTMLResponse(html)

clients = []
@app.websocket('/chat')
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)
    while True:
        data = await websocket.receive_text()
        for client in clients:
            await client.send_text(data)


# CommonException
@app.exception_handler(CommonException)
def common_exception_handler(request: Request, exc: CommonException):
    return JSONResponse(
        status_code=status.HTTP_418_IM_A_TEAPOT,
        content={'detail': exc.name}
    )
# Middleware
@app.middleware('http')
async def add_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    response.headers['duration'] = str(duration)
    return response

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

# Watch file template
app.mount('/templates/static', StaticFiles(directory='templates/static'), name='static')