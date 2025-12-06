# this is where we create an api endpoint to do those db operations
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.database import get_db # to get the db session
from schemas import UserBase, UserResponse # pydantic model to get data from user. this is where we get data from the user
from db import db_user # to access the create_user function we defined to create a new user in the db
from typing import List

router = APIRouter(
    prefix='/user',
    tags=['users']
)

#now we create endpoints to perform various operations in our db

#create user endpoint
@router.post('/', response_model=UserResponse) #define the model to return response to user
def create_user(request:UserBase, db:Session = Depends(get_db)):
    #return(f'password: {request.password.len()}')
    return db_user.create_user(db, request)

#read all users endpoint
@router.get('/', response_model=List[UserResponse]) #we're returning a list of users
def get_all_users(db:Session = Depends(get_db)):
    return db_user.get_all_users(db) #calls the function we defined in db_user.py to get all users

#read user by id endpoint
@router.get('/{id}', response_model=UserResponse)
def get_user_by_id(id:int, db:Session = Depends(get_db)):
    return db_user.get_user_by_id(db, id)

#update user by id endpoint
@router.put('/{id}/update', response_model=UserResponse)
def update_user(id:int, request:UserBase, db:Session = Depends(get_db)):
    return db_user.update_user(db, id, request)

#delete user by id endpoint
@router.delete('/{id}/delete')
def delete_user(id:int, db:Session = Depends(get_db)):
    return db_user.delete_user(db, id)