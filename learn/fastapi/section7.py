#Section 7: Database with SQLAlchemy
"""
    Dependencies quick intro
    Databases in FastAPI
    Create database and tables
    Write data
    Create and read
    Update and read
    Relationships
"""

"""
    DEPENDENCIES
    Depends
    Allow a function to depend (Phụ thuộc) on another function function(Phụ thuộc - Cho phép một function phục thuộc vào một function khác)
    Import functionality seamlessly
        Ex: req_param: dict = Depends(required_functionality)

"""

from fastapi import FastAPI, Depends
from typing import Optional
from db.database import engine
from models import user
from routers import router_user, router_article

app = FastAPI()
app.include_router(router_user.router)
app.include_router(router_article.router)
def required_functionality():
    return {'message': 'Learning FastAPI is important'}


@app.get('/blog/all')
def get_all_blog(page = 1, page_size: Optional[int] = None, req_parameter: dict = Depends(required_functionality)):
    return {'message': 'Get all blog', 'req': req_parameter}

"""
    CREATE USER DATA
    Database definition
    Model definition
    Create database
    Schema definition
    ORM functionality
    API functionality
"""
user.Base.metadata.create_all(engine)
"""
    PROCESS REVIEW
    Import required libraries: sqlalchemy, passlib, bcrypt
    Create database definition and run it in main.py
    Create database models(table)
    Create functionality to write to database
    Create schema
        Ex: Data from user: UserRequest
            Response to user: UserResponse
    Create APi operation

"""