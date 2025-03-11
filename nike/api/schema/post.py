from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class PostRequest(BaseModel):
    """
        Model request of post
    """
    title: str
    content: str
    start_date: str

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
    start_date: str
    flg_del: int

class ListPostResponse(BaseModel):
    """
        Response post
    """
    item: Optional[List[PostResponse]] = None
