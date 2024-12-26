from typing import Optional, List
from pydantic import BaseModel, Field

class LoginRequest(BaseModel):
    """
        Model request login
    """
    email: str = Field(..., title="The username", min_length=1, max_length=256)
    password: str = Field(..., title="The password", min_length=8, max_length=64)
    role: Optional[int] = Field(title="The role", default=0)

class UserRequest(BaseModel):
    """
        Model request user
    """
    username: str = Field(..., title="The username", min_length=1, max_length=256)
    email: str = Field(..., title="The email", min_length=1, max_length=256)
    fullname: str = Field(..., title="The email", min_length=1, max_length=256)
    password: str = Field(..., examples=["Test123@"],
                        title="The password", min_length=8, max_length=64)
    role: Optional[int] = Field(default=0, title="Role user")


class UserResponse(BaseModel):
    """
        Response user
    """
    username: str
    email: str
    role: Optional[int] = Field(default=0, title="Role user")

class UserAuth(BaseModel):
    """
        Response of user
    """
    user_id: int
    username: str
    email: str

class ItemUser(BaseModel):
    """
        Model user of list user response
    """
    username: str
    email: str
    user_id: str
    flg_del: int

class ListUserResponse(BaseModel):
    """
        Response list user
    """
    item: List[Optional[ItemUser]]
