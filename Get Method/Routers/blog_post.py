from fastapi import APIRouter, Query, Body, Path
from pydantic import BaseModel
from typing import Optional, List, Dict

router = APIRouter(
    prefix='/blogs',
    tags=['blogs']
)

class Image(BaseModel):
     url: str
     alias: str

class BlogModel(BaseModel):
    title: str
    content: str
    published: Optional[bool]
    tags: List[str] = []
    metadata: Dict[str, str] = {'key1': 'value1'}
    image: Optional[Image] = None #image here is a custom data subtype

@router.post('/new/{id}')
def create_post(blog: BlogModel, id:int, version:int=0): #fastapi converts the json body to pydantic model. the request body is read and validated against the model
    return {'blog': blog}


#adding parameter metadata to query parameter
@router.post('/new/{id}/comments')
def create_comment(blog:BlogModel, id:int, comment_id:int = Query(None,
        title='ID of query comment', 
        description='Comment for query parameter',
        alias='commentId', #custom name for query parameter
        depracated=True ), #mark a query parameter as depracated. this is useful when you have rolled out dofferent versions of an api and want to show in the documentation that certain functionalities have been removed

        #... is ellipsis in python. it makes the body required even if a default value is provided. you can also do Body(Ellipsis) 
        #regex to only allow lowercase letters and spaces, * helps us have any number of letters and spaces
        content:str = Body(..., min_length=5, max_length=50, regex='^[a-z/s]*$'), #adding validation to body parameters
        
        version: Optional[List[str]] = Query(None) #optional list query parameter
        # we could also add title='Version', description='Version of the API'
        ): 
         

        return {'blog': blog,
            'id': id, 
            'comment_id': comment_id,
            'content': content,
            'version': version}

@router.post('/new/{id}/comments/{comment_id}')
def create_comment_path(
    blog:BlogModel, 
    id:int, 
    #path parameter validation
    comment_id:int = Path(..., title='ID of path comment', ge=1, le=2000) #ge: greater than equal to, le: less than equal to
    ):   

    return {'blog': blog,
        'id': id, 
        'comment_id': comment_id}

#depends example
def required_functionality():
    return {'message': 'This is required functionality'}