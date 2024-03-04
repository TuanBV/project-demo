# Section 2: Get method

from fastapi import FastAPI
from enum import Enum
from typing import Optional, List

app = FastAPI()


@app.get('/hello')
def index():
    return {'message': 'Hello, world!'} 

@app.get('/blog/all')
def get_all_blog():
    return {'message': 'Get all blog!'}

class BlogType(str, Enum):
    short = 'short'
    story = 'story'
    howto = 'howto'


@app.get('/blog/type/{type}')
def get_blog_type(type: BlogType):
    return {'message': f'Blog type {type}'}


# @app.get('/blog/{id}')
# def get_blog_by_id(id):
#     return {'message': f'Blog with id {id}'}

@app.get('/blog/{id}')
def get_blog_by_id(id: int):
    return {'message': f'Blog with id {id}'}

@app.get('/blog/{id}/comment/{comment_id}')
def get_comment(id: int, comment_id: int, valid: bool=True, usename: Optional[str] = None):
    return {'message': f'blog_id is {id}, comment_id is {comment_id}, valid {valid}, usename is {usename}'}

# QUERY PARAMETERS
# Query parameters with type
# @app.get('/post/all')
# def get_post_all(page: int, page_size: int):
#     return {'message': f'Page {page} has {page_size} posts'}

# Default value for query parameters
# @app.get('/post/all')
# def get_post_all(page = 1, page_size = 10):
#     return {'message': f'Page {page} has {page_size} posts'}

# Options for query parameters
@app.get('/post/all')
def get_post_all(page: Optional[int] = 1, page_size: Optional[int] = 0):
    return {'message': f'Page {page} has {page_size} posts'}