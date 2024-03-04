from sqlalchemy.orm.session import Session
from schemas.user import UserRequest
from models.user import User
from utils.hash import Hash
from fastapi import HTTPException, status
from exceptions import CommonException

# Create user
def create_user(db: Session, request: UserRequest):
    new_user = User(
        username = request.username,
        email = request.email,
        password = Hash.bcrypt(request.password),
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# Get all user
def get_all_users(db: Session):
    return db.query(User).all()

# Get user by username
def get_by_username(username: str, db: Session):
    return db.query(User).filter(User.username == username).first()

# Get user by id
def get_user_by_id(db: Session, id_user: int):
    return db.query(User).filter(User.id == id_user).first()

# Updater user
def update_user(db: Session, id_user: int, request_user: UserRequest):
    user = db.query(User).filter(User.id == id_user)
    # Error handler
    # Check not user
    if not user.first():
        raise CommonException('Not found user')
    user.update({
        User.username: request_user.username,
        User.password: Hash.bcrypt(request_user.password),
        User.email: request_user.email
    })
    db.commit()

# Delete user
def delete_user(db: Session, id_user: int):
    user = db.query(User).filter(User.id == id_user)
    # Error handling
    # Check not user
    if not user.first():
        # Raise error
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Not found user has {id_user}')

    user.delete()
    db.commit()
    return "ok"