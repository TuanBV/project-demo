from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session
from schemas.user import UserRequest, UserResponse
from db.database import get_db
from typing import List
from service import user

router = APIRouter(prefix='/user', tags=['user'])

# Get user
@router.get('/', response_model=List[UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    return user.get_all_users(db)

# Get user by id
@router.get('/{id_user}', response_model=UserResponse)
def get_all_users(id_user: int, db: Session = Depends(get_db)):
    return user.get_user_by_id(db, id_user)

# Create user
@router.post('/', response_model=UserResponse)
def create_user(request: UserRequest, db: Session = Depends(get_db)):
    return user.create_user(db, request)

# Update user
@router.put('/{id_user}')
def update_user(id_user: int, request: UserRequest, db: Session = Depends(get_db)):
    return user.update_user(db, id_user, request)


# Delete user
@router.delete('/{id_user}')
def delete_user(id_user: int, db: Session = Depends(get_db)):
    return user.delete_user(db, id_user)
