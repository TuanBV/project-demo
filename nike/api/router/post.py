from fastapi import APIRouter, Depends
from schema.post import PostRequest, ListPostResponse
from post import PostService
from dependency_injector.wiring import inject, Provide
from containers import Container
from dto.response import Response
from helpers.response import ok
from helpers import context
from dependencies import authorized_user
from router.common import CommonRoute
from utils.kbn import ROLE
from decorators import permission

post_router = APIRouter(route_class=CommonRoute, prefix='/post', tags=['post'],
    responses={
        200: {
            "model": Response
        },
        401: {
            "model": Response[dict]
        },
        404: {
            "description": "No data",
            "model": Response[dict]
        },
        400: {
            "description": "API ERROR",
            "model": Response[dict]
        },
        500: {
            "description": "SYSTEM ERROR",
            "model": Response[dict]
        },
    },
)

@post_router.get('', responses={200:{"model": Response[ListPostResponse]}})
@inject
def get_all(post_service: PostService = Depends(Provide(Container.post_service))):
    """
        Get list post
    """
    data = post_service.get_all()
    payload = ListPostResponse(**data)
    response = ok(data=payload.dict())
    return response

@post_router.post('', tags=["post"], responses={200: {"model": Response}}, dependencies=[Depends(authorized_user)])
@permission([ROLE.ADMIN])
@inject
def add(request: PostRequest,
        post_service: PostService = Depends(Provide(Container.post_service))):
    """
        Add post
    """
    post_service.add(request.__dict__, context.user.value["username"])
    return ok()

# @post_router.get('/{post_id}', responses={200:{"model": Response[PostResponse]}})
# @inject
# def get_by_post_id(post_id: int,
#         post_service: PostService = Depends(Provide(Container.post_service))):
#     """
#         Get list post
#     """
#     data = post_service.get_by_post_id(post_id)
#     payload = PostResponse(**data)
#     response = ok(data=payload.__dict__)
#     return response

# @post_router.put('/{post_id}', responses={200:{"model": Response}}, dependencies=[Depends(authorized_user)])
# @permission([ROLE.ADMIN])
# @inject
# def update_post(post_id: int,
#         request: PostRequest,
#         post_service: PostService = Depends(Provide(Container.post_service))):
#     """
#         Update post
#     """
#     post_service.update(post_id, request.__dict__, context.user.value["username"])
#     return ok()

# @post_router.delete('/{post_id}', responses={200:{"model": Response}}, dependencies=[Depends(authorized_user)])
# @permission([ROLE.ADMIN])
# @inject
# def delete_post(post_id: int,
#         post_service: PostService = Depends(Provide(Container.post_service))):
#     """
#         Delete post
#     """
#     post_service.delete(post_id, context.user.value["username"])
#     return ok()

# @post_router.put('/{post_id}/active', responses={200:{"model": Response}}, dependencies=[Depends(authorized_user)])
# @permission([ROLE.ADMIN])
# @inject
# def active_post(post_id: int,
#         post_service: PostService = Depends(Provide(Container.post_service))):
#     """
#         Active post
#     """
#     post_service.active(post_id, context.user.value["username"])
#     return ok()



# PAGE_ID = '479577911913471'
# ACCESS_TOKEN = 'EAAQk42PWsioBOzzNZBJsYyHs3LukNY0HVwuuc1j2C4TSRNO4MpG1gbXxYO25mKZCVOw7RrvB4GyM590VZBxEpKby1hknaYgrTosbtpRZC9NbtUCQIY6W2q8tYnhlRxuIPmX2BT2FMUSs2u3ZCGHI6h9uZCbGVUNa2QYyogwBZAD2cZC52UwKPOLZCxNp0T2OyUZCmnXocIbCigrV9eLH1iatJt1348'
# FB_API_URL = f'https://graph.facebook.com/v22.0/{PAGE_ID}/feed'


# @post_router.post('', responses={200: {"model": Response[UserResponse]}})
# @inject
# async def create():
#     """
#         Post to facebook
#     """
#     payload = {
#         'message': 'message',
#         'access_token': 'EAAQk42PWsioBOZCW5NmrYdhkyEm47RYGBmVOQl4LbeO4E4AWEMTJyPA3DteLgOkjjEAVOD2qzZAUPXGNKR4pV8Nglg5huhUXt8e0JuMwRGSk9nyk9Jx7sxAehLZA1d7KGxXaUFcjDLNsNUBZBUWzf5mQgqxYaMFiRSrVUyxBISharwMow3smeZC3wtF8GgxMd3T8ZCsDQ1Vok1IlHjtW7mgJS8'
#     }

#     # Gọi API để lấy danh sách Fanpage
#     url_test = f"https://graph.facebook.com/v22.0/me/accounts?access_token=EAAQk42PWsioBO2g2EZBpZC0eevlmAN7daAQXHJzZBfI2jokWE4At3la9Pe9H6qKec1BlZBzm8PJRvQa241NFIv6Yy69PH9tHZAarGeWAyuitOv9kZCIBBG8qKriIYEuAyWgeR2eVIGSJUQNSyjF9k4xYkTRNFjhv2mIfpgiDiWiSrSNOSh086vzRDrUzYABE4YTAWGlxaZBmy32yEVt6AZDZD"
#     response1 = requests.get(url_test)
#     if response1.status_code == 200:
#         pages = response1.json()["data"]
#         for page in pages:
#             print(f"Page Name: {page['name']}")
#             print(f"Page ID: {page['id']}")
#             print(f"Page Access Token: {page['access_token']}")
#     else:
#         print("Lỗi:", response1.json())

#     response = requests.post(FB_API_URL, data=payload)
#     if response.status_code != 200:
#         raise HTTPException(status_code=response.status_code, detail=response.text)
#     return {"status": "success", "post_id": response.json().get('id')}

