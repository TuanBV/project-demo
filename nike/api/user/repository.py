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
from fastapi.encoders import jsonable_encoder

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
        with self.session_factory() as session:
            user = context.user.value
            data = session.query(User.username, User.email, User.token, User.role).filter(
                User.email == user["email"],
                User.flg_del == FlgDelete.OFF.value
            ).first()

            return data


    def get_user(self, email = None, role = 0):
        """
            # Get information user by email and role
            # Params:
            #   @email: Email user
            #   @role: Role user
            # Output:
            #   return: Data user
        """
        with self.session_factory_read() as session:
            return session.query(
                User.username, User.email, User.token, User.password, User.role
            ).filter(
                User.email == email,
                User.role == role,
                User.flg_del == FlgDelete.OFF.value
            ).first()


    def update_token(self, email = None, token = None):
        """
            # Update token by email
            # Params:
            #   @email: Email user
            #   @token: New token user
            # Output:
            #   return: 
        """
        with self.session_factory() as session:
            session.query(User).filter(
                User.email == email,
                User.flg_del == FlgDelete.OFF.value
            ).update({
                "token": token
            })
            session.commit()

    # Get list user
    def get_all(self):
        """
            # Get information user by email and role
            # Params:
            #   @email: Email user
            #   @role: Role user
            # Output:
            #   return: Data user
        """
        with self.session_factory_read() as session:
            return session.query(User).all()


    # Get user by user_id
    def get_by_user_id(self, user_id):
        """
            # Get user by user_id
            # Params:
            #   @user_id: User id
            # Output:
            #   return: Data user
        """
        with self.session_factory_read() as session:
            return session.query(User).filter(User.user_id == user_id).first()

    # Create new user
    def create(self, data):
        """
            # Create new user
            # Params:
            #   @data: Information user: username, email, role, password
            # Output:
            #   return: Data user
        """
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

    def change_status(self, user_id, status):
        """
            # Change status of user
            # Params:
            #   @user_id: User id
            #   @status: status
            # Output:
            #   return
        """
        with self.session_factory() as session:
            session.query(User).filter(User.user_id == user_id).update({
                "flg_del": status
            })
            session.commit()
