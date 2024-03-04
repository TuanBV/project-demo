from pydantic import BaseModel
from typing import List

class Article(BaseModel):
    title: str
    content: str
    published: bool

    class Config():
        orm_mode = True


class UserRequest(BaseModel):
    username: str
    email: str
    password: str


class UserResponse(BaseModel):
    username: str
    email: str
    items: List[Article] = []

    class Config():
        from_attributes = True
