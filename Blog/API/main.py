from fastapi import FastAPI
from db.database import engine
from router import post
from model import database
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(post.router)

@app.get('/')
def hw():
    return 'Hello, world!'

database.Base.metadata.create_all(engine)

app.mount('/images', StaticFiles(directory='images'), name='images')

# Add middleware
origins = [
    'https://localhost:3000',
    'http://localhost:3000',
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)