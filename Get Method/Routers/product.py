from fastapi import APIRouter, Header, Cookie, Form
from fastapi.responses import Response, HTMLResponse, PlainTextResponse
from typing import Optional, List
from custom_log import log
import time

router = APIRouter(
    prefix='/product',
    tags=['product']
)

products = ['cheese', 'cake', 'french toast']

async def time_consuming_function():
    time.sleep(5)
    return True

@router.post('/new')
def create_product(name:str = Form(...)): #to use form, declare it as a parameter
    products.append(name)
    return products

@router.get('/')
async def get_all_products():
    log("MyAPI","Call to get all products yo")
    await time_consuming_function()
    data = ' '.join(products) #we have to convert to the data type we want to return since this is custom response, there is no automatic conversion
    response = Response(content=data, media_type='text/plain')
    response.set_cookie(key="test_cooksie", value="test_cooksie_value")
    return response

@router.get('/withheader')
def get_products(response: Response, custom_header:Optional[List[str]] = Header(None), 
                 test_cooksie: Optional[str] = Cookie(None)):
    if custom_header:
        response.headers['custom_response_header'] = ", ".join(custom_header)
    return {
        "data":products,
        "custom_header": custom_header,
        "test_cookie": test_cooksie
        }

@router.get('/{id}', responses={
    200:{"content":{"text/html":{"example":"<div>Product</div>"}},
    "description": "Returns HTML if product is found"},
    404:{"content":{"text/plain":{"example":"Where is the product sir?"}},
    "description": "Returns plain text if product not found"},
})
def get_product(id:int):
    if id>len(products)-1 or id<0:
        out = "Product not available sir..."
        return PlainTextResponse(content=out, media_type='text/plain', status_code=404)
    else:
        product = products[id]
        out = f"""
        <head>
            <style>
            .product {{
                width: 500px;
                height: 30px;
                border: 2px inset green;
                background-color: lightblue;
                text-align: center;
            }}
            </style>
        </head>
        <div class="product">{product}</div>
        """
        return HTMLResponse(content=out, media_type="text/html")