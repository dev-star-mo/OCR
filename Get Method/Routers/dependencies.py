from fastapi import APIRouter, Request, Depends
from custom_log import log

router = APIRouter(
    prefix='/dependencies',
    tags=['dependencies'],
    dependencies = [Depends(log)] #this will apply the log dependency to all endpoints in this router
)

# create dependency that will be depended in another dependency (multi level dependency)
def convert_params(request:Request, separator:str = '--'):
    out_params = [] #this function converts query parameters into a list of strings with key separator value format
    for key, value in request.query_params:
        out_params.append(f"{key} {separator} {value}")
    return out_params

#create function that will be depended on
def convert_headers(request:Request, separator:str = '--', params = Depends(convert_params)):
    out_headers = [] #this function converts headers into a list of strings with key separator value format.
    # i was confused about how the 2 dependencies interact here. so the convert_headers function depends on convert_params function. so when convert_headers is called, fastapi will first call convert_params to get the params value, then pass it to convert_headers
    #so in the return i get the list of headers as well as the list of params obtained from the convert_params function
    for key, value in request.headers:
        out_headers.append(f"{key} {separator} {value}")
    return {
        'headers': out_headers, 
        'params': params,
    }

@router.get('')
def get_items(headers = Depends(convert_headers), separator: str = '---'): # i can override the default separator value here. by including it here as parameter, it allows me to change the value of the separator (what i am depending on)
    #i can include the seperator in the parameters of the endpoint function or not
    return {'items': ['ana', 'bella', 'catalina'],
        'headers': headers}

@router.post('/new')
def create_item(headers = Depends(convert_headers)):
    return {'message': 'item created',
        'headers': headers}


class Account:
    def __init__(self, name:str, email:str):
        self.name = name
        self.email = email #here i am just creating a simple class to demonstrate class based dependencies. i am storing name and email attributes

@router.post('/user')
def create_user(name:str, email:str, password:str, account: Account = Depends(Account)):
    # here i am depending on the Account class. fastapi will automatically create an instance of the class when the endpoint is called by passing the name and email parameters to the class constructor
    return {
        "name": account.name,
        "email": account.email,
    }