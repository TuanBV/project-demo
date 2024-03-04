from fastapi import HTTPException, status
from models.model import Post, Comment
from utils.kbn import FlgDelete
from sqlalchemy.orm.session import Session
from schema.comment import CommentRequest
from logger import log
import datetime

# Get all comment
def get_all(db: Session, post_id: int):
    # Get post by post_id
    post = db.query(Post).filter(Post.id == post_id, Post.flg_del == FlgDelete.OFF.value).first()
    # Check not post then raise exception
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Not found post {id}.')
    # Return list post
    return db.query(Comment).filter(Comment.post_id == post_id, Comment.flg_del == FlgDelete.OFF.value).all()

# Create comment
def create(db: Session, request: CommentRequest, username: str):
    log('Instagram', username + ' comment has content "' + request.text + '"')
    # Check account login
    if (request.username != username):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Can login account.')
    # Create record
    new_comment = Comment(
        text = request.text,
        username = request.username,
        post_id = request.post_id,
        timestamp = datetime.datetime.now(),
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)

    return new_comment