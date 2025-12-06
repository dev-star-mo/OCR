#this is where we define db operations related to articles like creating an article and getting an article from the db
#this is where we create articles in the db and get articles from the db

from sqlalchemy.orm.session import Session
from schemas import ArticleBase
from db.models import Db_article
from fastapi import HTTPException, status
from exceptions import StoryException

def create_article(db:Session, request:ArticleBase):
    if request.content.startswith('Story story'):
        raise StoryException('Recipe come')
    new_article = Db_article(title=request.title, 
        content = request.content, published=request.published, 
        user_id=request.creator_id)
    db.add(new_article)
    db.commit()
    db.refresh(new_article)
    return new_article

def get_article(db:Session, id:int):
    article = db.query(Db_article).filter(Db_article.id == id).first()
    if not article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
            detail=f'Article with id {id} not found')
    return article