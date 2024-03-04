# Section 6: Parameters
"""
    - Request body
    - Path and query parameters
    - Parameter metadata
    - Validators
    - Multiple values
    - Number validators
    - Complex subtypes
"""

from fastapi import FastAPI, Query, Body
from typing import Optional, List
from pydantic import BaseModel
app = FastAPI()

@app.get('/')
def get_all_blog():
    return {'message': 'Hello, world'}

"""
    REQUEST BODY
    - POST, PUT method
        (From pydantic import BaseModel)
    - Fastapi will convert to data
    - Note:
        + Read request body as JSON
        + Data validation
        + Data conversion
        + JSON schema
"""
class BlogModel(BaseModel):
    title: str
    content: str
    published: Optional[bool ]

@app.post('/blog', tags=['blog'])
def create_blog(blog: BlogModel):
    return blog

"""
    PARAMETER METADATA
    - Information displayed in docs
    - Using the Query, Path and Body imports
    Set default value:
        comment_id: int = Query(None)
    Add title and description of Query:
        comment_id: int = Query(None, title='Id of the comment', description='Description for the comment')
    Add alias(tên khác của param):
        comment_id: int = Query(None, alias='commentId')
    Add deprecated(Khi không sử dụng param nữa thì thêm 'deprecated=True' để người dùng nhận biết):
        comment_id: int = Query(None, alias='commentId', deprecated=True)
"""
@app.post('/blog/{id}/comment')
def create_comment(blog: BlogModel, id: int, comment_id: int = Query(None)):
    return {
        'blog_id': id,
        'blog': blog,
        'comment_id': comment_id
    }

"""
    VALIDATORS
    - Validate data passed to parameters
    - Provide a default value
        Ex: content: str = Body('Hello, world')
    - Require a value (non-optional parameter)
        Ex: content: str = Body(...)
            content: str = Body(Ellipsis)
    - Require minium length, maximum length:
        Ex: content: str = Body(..., min_length=5, max_length=100)
    - Regex validation
        Ex: content: str = Body(..., regex='^[a-zA-Z]*$')
        
"""
@app.post('/post/{id}/comment', tags=['post'])
def create_post(blog: BlogModel, id: int,
                   comment_id: int = Query(None, title='Id of the comment'),
                   content: str = Body(..., regex='^[a-zA-Z]*$')
                ):
    return {
        'blog_id': id,
        'blog': blog,
        'comment_id': comment_id,
        'content': content
    }

"""
    MULTIPLE VALUES
    For query parameters:
        Ex: '/blog/new/2/comment?commentID=4&v=1.0&v=1.1&v=1.2&v=3'
    Define an optional query parameter:
        Ex: v: Optional[List[str]] = Query(None)
    Provide default values:
        Ex: v: Optional[List[str]] = Query(['1.0', '1.1', '1.2', '1.3'])

"""
@app.post('/multiple/{id}/comment', tags=['multiple'])
def create_multiple(blog: BlogModel, id: int,
                   comment_id: int = Query(None, title='Id of the comment', ge = 5),
                   content: str = Body(..., regex='^[a-zA-Z]*$'),
                   v: Optional[List[str]] = Query(None),
                ):
    return {
        'blog_id': id,
        'blog': blog,
        'comment_id': comment_id,
        'content': content,
        'version': v,
    }

"""
    NUMBER VALIDATORS
    Greater than
        Ex: comment_id: int = Path(None, gt = 5)
    Greater than or equal to
        Ex: comment_id: int = Path(None, ge = 5)
    Less than
        Ex: comment_id: int = Path(None, lt = 5)
    Less than or equal to
        Ex: comment_id: int = Path(None, le = 5)

"""

"""
    COMPLEX SUBTYPES
    Pydantic models are not restricted to simple types
        Ex: tags: List[str] = []
    List, Set, Dict, Tuple
        Ex: metadata: Dict[str, str] = {'key': 'value'}
    Customer model subtypes
        Ex:
            class Image(BaseModel):
                url: str
                alias: str
            class BlogModel(BaseModel):
                image: Optional[Image] = None
            
"""