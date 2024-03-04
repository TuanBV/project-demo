from fastapi import APIRouter, File, UploadFile
from fastapi.responses import FileResponse
import shutil

router = APIRouter(prefix='/file', tags=['file'])

# File
@router.post('/')
def get_file(file: bytes = File(...)):
    content = file.decode('utf-8')
    lines = content.split('\n')

    return {'lines': lines}

# Upload file
@router.post('/uploadfile')
def upload_file(file: UploadFile = File(...)):
    path = f'files/{file.filename}'
    with open(path, 'w+b') as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        'filename': file.filename,
        'type': file.content_type
    }

# Download file
@router.get('/download/{name}', response_class=FileResponse)
def download_file(name: str):
    path = f'files/{name}'
    return path