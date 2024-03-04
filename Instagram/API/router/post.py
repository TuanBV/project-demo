from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from fastapi import BackgroundTasks
from schema.post import PostRequest, PostResponse, PostUpdateRequest
from schema.comment import CommentRequest
from schema.user import UserAuth
from sqlalchemy.orm.session import Session
from db.database import get_db
from auth.oauth2 import get_current_user
from typing import List
from fastapi.websockets import WebSocket, WebSocketState, WebSocketDisconnect
import service.post as service_post
import service.comment as service_comment
from logger import log, log_add_task
import random
import string
import shutil

router = APIRouter(prefix='/post', tags=['post'])

image_url_types = ['absolute', 'relative']

# Get all post
@router.get('/all', response_model=List[PostResponse])
def get_all(backgorund_task: BackgroundTasks, db: Session = Depends(get_db)):
    backgorund_task.add_task(log_add_task, 'Test add task write log')
    log('Instagram', 'Get all post.')
    return service_post.get_all(db)

# Create post
@router.post('', response_model=PostResponse)
def create(request: PostRequest, db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
    log('Instagram', 'Create new post.')
    # Check type of image
    if request.image_url_type not in image_url_types:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="Parameter image_url_type can only take values 'absolute' or 'relative'.")
    return service_post.create(db, request)

# Delete post
@router.delete('/{id}')
def delete(id: int, db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
    log('Instagram', 'Delete post - Id: ' + str(id))
    return service_post.delete(db, id, current_user.id)

# Update image
@router.post('/upload')
def upload_image(image: UploadFile = File(...), current_user: UserAuth = Depends(get_current_user)):
    letters = string.ascii_letters
    rand_str = ''.join(random.choice(letters) for i in range(6))
    new = f'_{rand_str}.'
    filename = new.join(image.filename.rsplit('.', 1))
    path = f'images/{filename}'

    # Write file
    with open(path, 'w+b') as buffer:
        shutil.copyfileobj(image.file, buffer)

    return {'filename': path}

# Update post
@router.put('/{id}')
def update(id: int, request: PostUpdateRequest, db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
    log('Instagram', 'Update post - Id: ' + str(id))
    return service_post.update(db, id, request, current_user.id)


contents = {}

@router.websocket('/chat')
async def chat_socket(websocket: WebSocket, db: Session = Depends(get_db)):
    await websocket.accept()
    
    # Create websocket for post
    for post in service_post.get_all(db):
        if post.id not in contents.keys():
            contents[post.id] = []
        contents[post.id].append(websocket)

    # Check state of websocket is CONNECTED
    while websocket.client_state == WebSocketState.CONNECTED:
        try:
            # Convert data to json
            data = await websocket.receive_json()
            # Get current_user by token of request
            current_user: UserAuth = get_current_user(data['token'], db)
            if current_user.username != data['username']:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Error authentication.')

            # Check websocket not in list contents then add in contents
            if str(websocket) not in str(contents.values()):
                contents[data['post_id']].append(websocket)

            # Create data request
            request = CommentRequest(
                text=data['text'],
                username=data['username'],
                post_id=data['post_id']
            )
            # Add comment in db
            service_comment.create(db, request, data['username'])
            # Delete websocket disconnected
            for content in contents[data['post_id']].copy():
                if content.client_state == WebSocketState.DISCONNECTED:
                    contents[data['post_id']].remove(content)
            # Send data to other websocket
            for content in contents[data['post_id']]:
                await content.send_json(data)
        except WebSocketDisconnect:
            pass
