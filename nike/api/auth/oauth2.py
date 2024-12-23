from fastapi.security import OAuth2PasswordBearer
from typing import Optional
from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi import HTTPException, status, Depends, BackgroundTasks
from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = '77407c7339a6c00544e51af1101c4abb4aea2a31157ca5f7dfd87da02a628107'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
        Create token
    """
    to_encode = data.copy()

    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    if expires_delta:
        expire = datetime.now() + expires_delta
    # Update time
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends()):
#     """
#         Get information fo user
#     """
#     credentials_exception = HTTPException(
#         status_code = status.HTTP_401_UNAUTHORIZED,
#         detail='Could not validate credentials.',
#         headers={'WWW-Authenticate': 'Bearer'} 
#     )
#     try:
#         # Decode token
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         # Get username
#         username: str = payload.get("username")
#         # Check username is None then raise exception
#         if username is None:
#             raise credentials_exception
#     except JWTError as exc:
#         raise credentials_exception from exc

#     # Get user by username get from token
#     user = service_user.get_by_username(db, username)
#     # Check username is None then raise exception
#     if user is None:
#         raise credentials_exception
#     return user
