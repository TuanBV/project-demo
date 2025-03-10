from fastapi import APIRouter, BackgroundTasks
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
from schemas.product import ProductRequest
from log import log

router = APIRouter(prefix='/templates', tags=['templates'])

templates = Jinja2Templates(directory='templates')

# @router.get('/products/{id}', response_class=HTMLResponse)
# def get_product(id: str, request: Request):
#     return templates.TemplateResponse(
#         'products.html',
#         {
#             'request': request,
#             'id': id,
#         }
#     )

@router.post('/products/{id}', response_class=HTMLResponse)
def get_product(id: str, product: ProductRequest, request: Request, bt: BackgroundTasks):
    bt.add_task(log_template_call, f"Template read for product with id {id}")
    return templates.TemplateResponse(
        'products.html',
        {
            'request': request,
            'id': id,
            'title': product.title,
            'description': product.description,
            'price': product.price,
        }
    )

def log_template_call(message: str):
    log('FastAPI', message)