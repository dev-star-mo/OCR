# this is where we define pydantic models for user creation and response. model used to get data from user and return data to user.
#this is our user model
from pydantic import BaseModel
from typing import List

#this defines the article that will be used in the UserResponse model. not the one we get from the user
class Article(BaseModel):
    title: str
    content: str
    published: bool
    class Config():
        orm_mode = True

class UserBase(BaseModel):
    username: str
    email: str
    password: str

# define a model for the response without the password
class UserResponse(BaseModel):
    username: str
    email: str
    items: List[Article] = []  # List of articles associated with the user. we define the return type we want to give user (article), and define it up there
    class Config():
        orm_mode=True #this automates converting the data ffrom the sqlalchemy model to pydantic model (db model to response model that user sees)

#user inside article response
class User(BaseModel):
    id: int
    username: str
    class Config():
        orm_mode=True

#now we define the article model we will use to get data from the user, what we get from user
class ArticleBase(BaseModel):
    title: str
    content: str
    published: bool
    creator_id: int  # to link article to user

#now we define the article response model, what we return to the user
class ArticleResponse(BaseModel):
    title: str
    content: str
    published: bool
    user: User #this is not userbase or userresponse, its the data type we want included here to return to user
    class Config():
        orm_mode = True
# Config class with orm_mode = True tells pydantic to read data even if it is not a dict, but an ORM model (like SQLAlchemy model). 
#helps in converting sqlalchemy model to pydantic model (db model to user model)

class ProductBase(BaseModel): #schema to get product data from user in the endpoint for templates
    title:str
    description:str
    price:float