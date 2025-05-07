from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class PostRequest(BaseModel):
    """
        Model request of post
    """
    id: Optional[int] = None
    title: str
    content: str
    status: int

class Comment(BaseModel):
    text: str
    username: str
    timestamp: datetime

class User(BaseModel):
    username: str

class PostResponse(BaseModel):
    """
        Response post
    """
    id: int
    title: str
    content: str
    status: int
    flg_del: int

class ListPostResponse(BaseModel):
    """
        Response post
    """
    item: Optional[List[PostResponse]] = None
