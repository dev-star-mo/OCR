# this is where we create an api endpoint to do those db operations for articles
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.database import get_db # to get the db session
from schemas import ArticleBase, ArticleResponse # pydantic model to get data from user. this is where we get data from the user
from db import db_article # to access the create_user function we defined to create a new user in the db
from typing import List
from auth.oauth2 import get_current_user, oauth2_scheme
from schemas import UserBase

router = APIRouter(
    prefix='/article',
    tags=['articles']
)

#now we create endpoints to perform various operations in our db
#we expose functionality through our api to create and get articles
#create article endpoint
@router.post('/', response_model=ArticleResponse) #define the model to return response to user (articleresponse)
def create_article(request:ArticleBase, db:Session = Depends(get_db), current_user:UserBase = Depends(get_current_user)):
    return db_article.create_article(db, request)

#read article by id endpoint
@router.get('/{id}') #, response_model=ArticleResponse)
#instead of using token to authenticate, we can now use the user
def get_article(id:int, db:Session = Depends(get_db), current_user:UserBase = Depends(get_current_user)):
    return {"data":db_article.get_article(db, id),
            "user":current_user}