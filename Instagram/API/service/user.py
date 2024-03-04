from schema.user import UserRequest
from models.model import User
from sqlalchemy.orm.session import Session
from utils.hash import hash256
from utils.kbn import FlgDelete

# Get all user
def get_all(db: Session):
    return db.query(User.username, User.email).filter(User.flg_del == FlgDelete.OFF.value).all()

# Get user by username
def get_by_username(db: Session, username: str):
    return db.query(User).filter(User.flg_del == FlgDelete.OFF.value, User.username == username).first()

# Add user
def create(db: Session, request: UserRequest):
    new_user = User(
        username = request.username,
        email = request.email,
        full_name = request.full_name,
        password = hash256(request.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user