from fastapi import APIRouter, Depends, UploadFile, File
from schema.post import PostRequest, PostResponse
from sqlalchemy.orm import Session
from db.database import get_db
from service import post as service_post
import string
import random
import shutil

router = APIRouter(prefix='/blog', tags=['blog'])

# Create a new post
@router.post('')
def create(request: PostRequest, db: Session = Depends(get_db)):
    return service_post.create(db, request)

# Get all post
@router.get('/all')
def get_all(db: Session = Depends(get_db)):
    return service_post.get_all(db)

# Delete post
@router.delete('/{id}')
def  delete(id: int, db: Session = Depends(get_db)):
    return service_post.delete(db, id)

# Update image
@router.post('/upload-image')
def update_image(image: UploadFile = File(...), db: Session = Depends(get_db)):
    letter = string.ascii_letters
    rand_str = ''.join(random.choice(letter) for i in range(6))
    new = f'_{rand_str}.'
    filename = new.join(image.filename.rsplit('.', 1))
    path = f'images/{filename}'
    with open(path, 'w+b') as buffer:
        shutil.copyfileobj(image.file, buffer)
    
    return {'filename': path}