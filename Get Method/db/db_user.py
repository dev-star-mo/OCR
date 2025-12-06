#here we will create a function to create a new user in the database. this will use the model we defined in models.py to do the orm mapping (dirty work of converting pydantic model to sql alchemy model [what we get from user to what we store in db])

from schemas import UserBase
from db.models import Db_user
from sqlalchemy.orm.session import Session
from db.hash import Hash
from fastapi import HTTPException, status

def create_user(db:Session, request:UserBase): # db is the session we will use to interact with the db, request is the pydantic model we will get from the user
    #we get the data in the formt of the request model, we need to convert it to the db model (defined in Db_user) to store it in the db
    new_user = Db_user(username=request.username, email=request.email, password=Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user) #to get the new data with the id assigned by the db. this helps our data get an id after being added to the db
    return new_user

def get_all_users(db:Session):
    return db.query(Db_user).all()

def get_user_by_id(db:Session, id:int):
    user = db.query(Db_user).filter(Db_user.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User with id {id} not found')
    return user

def get_user_by_username(db:Session, username:str):
    user = db.query(Db_user).filter(Db_user.username == username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User with username {username} not found')
    return user

def update_user(db:Session, id:int, request:UserBase):
    user = db.query(Db_user).filter(Db_user.id == id).first()
    if not user: #nonetype object has no attribute first if i use user.first()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User with id {id} not found')
    user.username = request.username
    user.email = request.email
    user.password = Hash.bcrypt(request.password)

    db.commit()
    db.refresh(user)
    return user

def delete_user(db:Session, id:int):
    user = db.query(Db_user).filter(Db_user.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User with id {id} not found')
    db.delete(user)
    db.commit()
    return 'KO'