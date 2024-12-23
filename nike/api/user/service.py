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
            return {
                "username": data.username,
                "email": data.email,
                "token": data.token,
                "role": data.role
            }

    def login(self, data):
        """
            # Login
            # Params:
            #   @data: email and password
            # Output:
            #   return: Data user
        """
        user_account = self.user_repo.get_user_by_email(data["email"])
        if user_account and checkpw(data["password"], user_account.password):
            data["user"] = {
                "username": user_account.username,
                "email": user_account.email,
                "role": user_account.role.value
            }
            data["token"] = jwt.hash_token(data["user"])
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
