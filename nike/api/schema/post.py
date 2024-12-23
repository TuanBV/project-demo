from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class PostRequest(BaseModel):
    image_url: str
    image_url_type: str
    caption: str
    creator_id: int

class PostUpdateRequest(BaseModel):
    caption: str
    image_url: Optional[str] = None


class Comment(BaseModel):
    text: str
    username: str
    timestamp: datetime

    class Config():
        orm_mode = True

class User(BaseModel):
    username: str
    
    class Config():
        orm_mode = True

class PostResponse(BaseModel):
    id: int
    image_url: str
    image_url_type: str
    caption: str
    timestamp: datetime
    comment: List[Comment]
    user: User

    class Config():
        orm_mode = True
