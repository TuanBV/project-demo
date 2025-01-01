from user import UserRepository
from schema.user import UserRequest
from models.model import User
from sqlalchemy.orm.session import Session
from helpers.common import checkpw
from utils.hash import hash256
from utils.common import random_text
from fastapi.encoders import jsonable_encoder
from core import CommonException
import helpers.jwt as jwt


class UserService:
    """
        User service
    """
    def __init__(self, user_repository: UserRepository):
        self.user_repo: UserRepository = user_repository

    def get_me(self):
        """
            # Get information user by cookie
            # Params:
            # Output:
            #   return: Data user
        """
        data = self.user_repo.get_me()
        if data:
            token = {
                "username": data.username,
                "email": data.email,
                "role": data.role.value
            }
            # Save token
            self.user_repo.update_token(data.email, jwt.hash_token(token))
            return {
                "username": data.username,
                "email": data.email,
                "token": jwt.hash_token(token),
                "role": data.role
            }

    def login(self, data):
        """
            # Login
            # Params:
            #   @data: email and password, role
            # Output:
            #   return: Data user
        """
        user_account = self.user_repo.get_user(data["email"], data["role"])
        if user_account and checkpw(data["password"], user_account.password):
            data["user"] = {
                "username": user_account.username,
                "email": user_account.email,
                "role": user_account.role.value
            }
            data["token"] = jwt.hash_token(data["user"])
            # Save token
            self.user_repo.update_token(data["email"], data["token"])
            return data

        raise CommonException(message="Email or password invalid")


    # Create new user
    def create(self, data):
        """
            # Create new user
            # Params:
            #   @data: information user
            # Output:
            #   return: Data user
        """
        return self.user_repo.create(data)


    # Get list user
    def get_list(self):
        """
            # Get list user
            # Params:
            # Output:
            #   return: List data user
        """
        return {"item": jsonable_encoder(self.user_repo.get_all())}

    # Change status user
    def change_status(self, user_id, status):
        """
            # Change status user
            # Params:
            # Output:
            #   return: Data user
        """
        user = self.user_repo.get_by_user_id(user_id)
        # Check if the user has changed status
        if user:
            self.user_repo.change_status(user_id, status)
            return True
        raise CommonException(message="User not found")
