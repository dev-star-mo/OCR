from fastapi import status, Response, APIRouter, Depends
from Routers.blog_post import required_functionality
from enum import Enum
from typing import Optional

router = APIRouter(
    prefix='/blogs',
    tags=['blogs']
)

class blogType(str, Enum):
    short = 'short'
    long = 'long'

@router.get('/type/{type}', tags=['blog type'], summary = 'Get blog type', description = 'Get blog type short or long', response_description = 'The blog type retrieved successfully')
#blog description is used for providing info on the output response of outr API endpoint
def get_blog_type(type: blogType, response: Response): #validate type with Enum. validate what i get from the path
    response.status_code = status.HTTP_200_OK
    return {'message': f'My blog type is {type.value}'} #.value to get the value of the Enum

#query parameters
@router.get('/all', tags = ['all blogs'])
def get_all_blogs(pages: Optional[int] = None, readers=100, required_param:dict = Depends(required_functionality)):
    """
    This is a way to add bigger descriptions for your endpoints by setting them in the function
    - **pages**: pages will be in bold
    """
    return {'message': f'Blogs with {pages} or more pages have {readers} or more readers', 'depends param': required_param}

#combine path and query parameters
@router.get('/{id}/comments/{comment_id}', tags = ['all blogs'])
def get_blog_comment(id: int, comment_id: int, valid: bool, username: Optional[str] = None):
    return {'message': f'Blog id {id} has comment id {comment_id} with validity {valid} and username {username}'}

