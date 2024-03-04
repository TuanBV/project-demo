from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from schema.post import PostRequest
from models.model import Post
from utils.kbn import FlgDelete
from sqlalchemy.orm.session import Session
from sqlalchemy import desc
import datetime

# Get all post
def get_all(db: Session):
    return db.query(Post).filter(Post.flg_del == FlgDelete.OFF.value).order_by(desc(Post.timestamp)).all()

# Create post
def create(db: Session, request: PostRequest):
    new_post = Post(
        image_url = request.image_url,
        image_url_type = request.image_url_type,
        caption = request.caption,
        timestamp = datetime.datetime.now(),
        user_id = request.creator_id,
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

# Update post
def update(db: Session, id: int, request: PostRequest, user_id: int):
    post = db.query(Post).filter(Post.id == id, Post.flg_del == FlgDelete.OFF.value)
    if request.image_url:
        post.update({
            Post.image_url: request.image_url,
        })
    post.update({
        Post.caption: request.caption,
        Post.user_id: user_id,
        Post.timestamp: datetime.datetime.now(),
    })
    db.commit()
    return 'ok'

# Delete post
def delete(db: Session, id: int, user_delete: int):
    # Generate SQL
    post = db.query(Post).filter(Post.id == id, Post.flg_del == FlgDelete.OFF.value)
    # Check has post
    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Not found post {id}.')
    # Check user create post then can delete post
    if post.first().user_id != user_delete:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Only post creator can delete post.')
    # Update flag delete 
    post.update({
        Post.flg_del: FlgDelete.ON.value,
    })
    db.commit()
    return 'ok'