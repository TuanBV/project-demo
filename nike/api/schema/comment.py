from pydantic import BaseModel

class CommentRequest(BaseModel):
    text: str
    username: str
    post_id: int
