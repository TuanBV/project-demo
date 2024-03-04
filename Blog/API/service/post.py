from fastapi import HTTPException, status
from schema.post import PostRequest
from sqlalchemy.orm.session import Session
import datetime
from model.database import Post
from common.kbn import FlgDelete

# Create new post
def create(db: Session, request: PostRequest):
    new_post = Post(
        image_url = request.image_url,
        title = request.title,
        content = request.content,
        regist_user = request.creator,
        regist_date = datetime.datetime.now(),
        flg_del = 0,
    )

    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

# Get all post
def get_all(db: Session):
    return db.query(Post).filter(Post.flg_del == FlgDelete.OFF.value).all()

# Delete post
def delete(db: Session, id: int):
    post = db.query(Post).filter(Post.id == id, Post.flg_del == FlgDelete.OFF.value)

    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Not found post {id}')
    post.update({
        Post.flg_del: FlgDelete.ON.value
    })
    db.commit()

# Update post
def update(db: Session, id: str, request: PostRequest):
    return 'ok'