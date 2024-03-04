#Section 5: Routers

from fastapi import APIRouter


router = APIRouter(prefix='/blog', tags=['blog'])

@router.get('/')
def get_all_blog():
    return {'message': f'Get all blog (Section 5)'}