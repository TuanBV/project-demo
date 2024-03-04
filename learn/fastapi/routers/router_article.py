from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas.article import ArticleRequest, ArticleResponse
from db.database import get_db
from typing import List
from service import article
from auth.oauth2 import get_user
router = APIRouter(prefix='/article', tags=['article'])

# Create article
@router.post('/', response_model=ArticleResponse)
def create_article(request: ArticleRequest, db: Session = Depends(get_db)):
    return article.create(db, request)

# Get article
# @router.get('/', response_model=List[ArticleResponse])
@router.get('/')
def get_article(db: Session = Depends(get_db), current_user: str = Depends(get_user)):
    return {
        'data': article.get_all_article(db),
        'current_user': current_user,
    }
