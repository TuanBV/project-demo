from fastapi import APIRouter, Depends
from schema.user import UserRequest, UserResponse
from sqlalchemy.orm.session import Session
from db.database import get_db
from typing import List
import service.user as service_user

router = APIRouter(prefix='/user', tags=['user'])


@router.get('/all', response_model=List[UserResponse])
def get_all(db: Session = Depends(get_db)):
    return service_user.get_all(db)

@router.post('', response_model=UserResponse)
def create(request: UserRequest, db: Session = Depends(get_db)):
    return service_user.create(db, request)
