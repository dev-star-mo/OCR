from fastapi import APIRouter
from fastapi.background import BackgroundTasks
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from schemas import ProductBase
from custom_log import log

router = APIRouter(
    prefix='/templates',
    tags=['templates']
)

templates = Jinja2Templates(directory="templates")

@router.post("/products/{id}", response_class=HTMLResponse)
def get_product_template(id:str, product:ProductBase, request:Request, 
                         bt:BackgroundTasks):
    bt.add_task(log_template_call, f"Product template called for id: {id}") #this is called after the return is sent
    return templates.TemplateResponse(
        "product.html",{
            "request": request,
            "id": id,
            "title":product.title,
            "description":product.description,
            "price":product.price
        }
    )

def log_template_call(message:str):
    log("template_logger", message)