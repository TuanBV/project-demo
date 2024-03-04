from fastapi import APIRouter, Header, Cookie, Form
from fastapi.responses import Response, HTMLResponse, PlainTextResponse
from typing import Optional
from log import log

router = APIRouter(prefix='/product', tags=['product'])

products = ['watch', 'camera', 'phone']

@router.post('/news')
def add_product(name: str = Form(...)):
    log('New', 'Call api new')
    products.append(name)
    return products

@router.get('/withheader')
def func(response: Response, custom_header: Optional[str] = Header(None), test_cookie: Optional[str] =Cookie(None)):
    return {
        'data': products,
        'header': custom_header,
        'cookie': test_cookie,
    }

# Plain text
@router.get('/')
def get_all_products():
    data = ' '.join(products)
    response = Response(content=data, media_type='text/plain')
    response.set_cookie(key='test_cookie', value='test_cookie_value')
    return response


# HTML
@router.get('/{id}', responses={
    200: {
        'content': {
            'text/html': {
                'example': '<div>Product</div>',
            }
        },
        'description': 'Return the HTML for an object'
    },
    404: {
        'content': {
            'text/plain': {
                'Product not available',
            }
        },
        'description': 'A clear text error message'
    },
})
def get_product_by_id(id: int):
    if id > len(products):
        out = 'Product not available'
        return PlainTextResponse(status_code=404, content=out, media_type='text/plain')
    product = products[id]
    out = f'''
        <head>
            <style>
                .product {{
                    width: 500px;
                    height: 500px;
                    color: red;
                }}
            </style>
        </head>
        <div class='product'>{product}</div>
    '''
    return HTMLResponse(content=out, media_type='text/html')

"""
    CORS

    Ex:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=['http://localhost:3000'],
            allow_credentials=True,
            allow_methods=['*'],
            allow_headers=['*'],
        )
"""