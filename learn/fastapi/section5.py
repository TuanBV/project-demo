from fastapi import FastAPI
from routers import blog, blog2

app = FastAPI()

app.include_router(blog.router)
app.include_router(blog2.router)

@app.get('/')
def index():
    return 'Hello World'