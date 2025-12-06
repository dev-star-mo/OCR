#this defines the structure of the database table using SQLAlchemy ORM. it is the mapping between the database table and the pydantic model we defined to get data from the user. basically its our model for db
#this is our sqlalchemy model
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship
from db.database import Base
from sqlalchemy import Column
from sqlalchemy.sql.sqltypes import Integer, String, Boolean


class Db_user(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True) #set as primary key. index is used to auto increment with every new entry
    username = Column(String)
    email = Column(String)
    password = Column(String)
    items = relationship("Db_article", back_populates='user')

class Db_article(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(String)
    published = Column(Boolean)
    user_id = Column(Integer, ForeignKey('users.id')) #foreign key to link to user table
    user = relationship("Db_user", back_populates='items')