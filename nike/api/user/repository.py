from schema.user import UserRequest
from models.model import User
from sqlalchemy.orm.session import Session
from utils.hash import Hash
from utils.kbn import FlgDelete
from utils.common import random_text
import helpers.jwt as jwt
from helpers import context


"""
Repository template
"""

from core import CommonRepository
from helpers import kbn
from fastapi.encoders import jsonable_encoder
import re

class UserRepository(CommonRepository):
    """
    Repository of user
    """


    def get_me(self):
        """
            # Get information user by cookie
            # Params:
            # Output:
            #   return: Data user
        """
        with self.session_factory_read() as session:
            user = context.user.value
            return session.query(User.username, User.email, User.token, User.role).filter(
                User.email == user["email"],
                User.flg_del == FlgDelete.OFF.value
            ).first()


    def get_user_by_email(self, email = None):
        """
            # Get information user by email
            # Params:
            #   @email: User email
            # Output:
            #   return: Data user
        """
        with self.session_factory_read() as session:
            return session.query(
                User.username, User.email, User.token, User.password, User.role
            ).filter(
                User.email == email,
                User.flg_del == FlgDelete.OFF.value
            ).first()

    # # Get all user
    # def get_all(db: Session):
    #     return db.query(User.username, User.email).filter(User.flg_del == FlgDelete.OFF.value).all()

    # # Get user by username
    # def get_by_username(db: Session, username: str):
    #     return db.query(User).filter(User.flg_del == FlgDelete.OFF.value, User.username == username).first()

    # Create new user
    def create(self, data):
        with self.session_factory() as session:
            data_token = {
                'username': data['username'],
                'email': data['email']
            }
            new_user = User(
                user_id=random_text(20),
                username = data['username'],
                email = data['email'],
                fullname = data['fullname'],
                role = data['role'],
                password = Hash.bcrypt(data['password']),
                token = jwt.hash_token(data_token)
            )

            session.add(new_user)
            session.commit()
            session.refresh(new_user)

            return jsonable_encoder(new_user)
