from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from db.database import get_db
from sqlalchemy.orm.session import Session
from models.model import User
from utils.hash import hash256
from utils.kbn import FlgDelete
from auth.oauth2 import create_token

router = APIRouter(tags=['authentication'])

@router.post('/login')
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # Get user by username
    user = db.query(User).filter(
        User.username == request.username,
        User.flg_del == FlgDelete.OFF.value
    ).first()
    # Check not user
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Invalid credentials.')
    # Check password
    if hash256(request.password) != user.password:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Incorrect password.')
    # Create token for headers
    token = create_token(data={'username': user.username})
    return {
        'access_token': token,
        'token_type': 'bearer',
        'user_id': user.id,
        'username': user.username,
    }
