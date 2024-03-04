from pydantic import BaseModel, Field

class UserRequest(BaseModel):
    username: str = Field(..., title="The username", min_length=1, max_length=256)
    email: str = Field(..., title="The email", min_length=1, max_length=256)
    full_name: str = Field(..., title="The email", min_length=1, max_length=256)
    password: str = Field(..., examples=["Test123@"], title="The password", min_length=8, max_length=64)


class UserResponse(BaseModel):
    username: str
    email: str

    class Config():
        orm_mode = True

class UserAuth(BaseModel):
    id: int
    username: str
    email: str