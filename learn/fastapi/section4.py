#Section 3: Operation description

from fastapi import FastAPI, status, Response

app = FastAPI()

# Tags
@app.get(
        '/blog/all',
        tags=['blog']
    )
def get_all():
    return {'message': 'Get all blog'}


@app.get('/blog/{id}', status_code=status.HTTP_200_OK)
def get_blog(id: int, response: Response):
    """
        Simulate a GET request:
        - **id**: The id of the blog
    """
    if id < 5:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {'message': f'Blog not found id is {id}'}
    
    response.status_code = status.HTTP_200_OK
    return {'message': f'Blog with id {id}'}
# Summary and description
@app.get(
        '/post/all',
        tags=['post'],
        summary='Retrieve all posts',
        description='This is api call simulates fetch all post'
    )
def get_all():
    return {'message': 'Get all post'}


# Response description
@app.get(
        '/comment/all',
        tags=['comment'],
        response_description='This list is available comment'
    )
def get_all():
    return {'message': 'Get all comment'}

