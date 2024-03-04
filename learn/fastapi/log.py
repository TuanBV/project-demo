from fastapi.requests import Request

def log(tag='FastAPI', message='no message', request: Request = None):
    path = f"logs/log.txt"
    with open(path, 'w+')  as log:
        log.write(f'{tag} : {message}\n')
        log.write(f'\t {request.url}\n')