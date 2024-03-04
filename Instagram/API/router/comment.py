from fastapi import APIRouter, Depends
from db.database import get_db
from auth.oauth2 import get_current_user
from sqlalchemy.orm.session import Session
from schema.user import UserAuth
import service.comment as service_comment
from schema.comment import CommentRequest

router = APIRouter(prefix='/comment', tags=['comment'])

@router.get('/all/{post_id}')
def get_all(post_id: int, db: Session = Depends(get_db)):
    return service_comment.get_all(db, post_id)

@router.post('/{post_id}')
def create(request: CommentRequest, db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
    return service_comment.create(db, request, current_user.username)