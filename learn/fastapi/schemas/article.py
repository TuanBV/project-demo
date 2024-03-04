from pydantic import BaseModel
from typing import Optional

class Creator(BaseModel):
    id: int
    username: str
    class Config():
        orm_mode = True

class ArticleRequest(BaseModel):
    title: str
    content: str
    published: bool
    creator_id: int

class ArticleResponse(BaseModel):
    title: str
    content: str
    published: bool
    user: Optional[Creator] = []

    class Config():
        from_attributes = True
