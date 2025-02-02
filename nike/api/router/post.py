from fastapi import APIRouter, Depends, HTTPException
from schema.user import UserRequest, UserResponse, LoginRequest, ListUserResponse, OfferRequest, OfferResponse
from user import UserService
from dependency_injector.wiring import inject, Provide
from containers import Container
from dto.response import Response
from helpers.response import (ok, make_cookie)
from helpers.cookie import get_user_cookie
from dependencies import authorized_user
from router.common import CommonRoute
from helpers import context
from typing import List
import requests

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

PAGE_ID = '479577911913471'
ACCESS_TOKEN = 'EAAQk42PWsioBOzzNZBJsYyHs3LukNY0HVwuuc1j2C4TSRNO4MpG1gbXxYO25mKZCVOw7RrvB4GyM590VZBxEpKby1hknaYgrTosbtpRZC9NbtUCQIY6W2q8tYnhlRxuIPmX2BT2FMUSs2u3ZCGHI6h9uZCbGVUNa2QYyogwBZAD2cZC52UwKPOLZCxNp0T2OyUZCmnXocIbCigrV9eLH1iatJt1348'
FB_API_URL = f'https://graph.facebook.com/v22.0/{PAGE_ID}/feed'


@post_router.post('', responses={200: {"model": Response[UserResponse]}})
@inject
async def create():
    """
        Post to facebook
    """
    payload = {
        'message': 'message',
        'access_token': 'EAAQk42PWsioBOZCW5NmrYdhkyEm47RYGBmVOQl4LbeO4E4AWEMTJyPA3DteLgOkjjEAVOD2qzZAUPXGNKR4pV8Nglg5huhUXt8e0JuMwRGSk9nyk9Jx7sxAehLZA1d7KGxXaUFcjDLNsNUBZBUWzf5mQgqxYaMFiRSrVUyxBISharwMow3smeZC3wtF8GgxMd3T8ZCsDQ1Vok1IlHjtW7mgJS8'
    }

    # Gọi API để lấy danh sách Fanpage
    url_test = f"https://graph.facebook.com/v22.0/me/accounts?access_token=EAAQk42PWsioBO2g2EZBpZC0eevlmAN7daAQXHJzZBfI2jokWE4At3la9Pe9H6qKec1BlZBzm8PJRvQa241NFIv6Yy69PH9tHZAarGeWAyuitOv9kZCIBBG8qKriIYEuAyWgeR2eVIGSJUQNSyjF9k4xYkTRNFjhv2mIfpgiDiWiSrSNOSh086vzRDrUzYABE4YTAWGlxaZBmy32yEVt6AZDZD"
    response1 = requests.get(url_test)
    print(url_test)
    if response1.status_code == 200:
        pages = response1.json()["data"]
        for page in pages:
            print(f"Page Name: {page['name']}")
            print(f"Page ID: {page['id']}")
            print(f"Page Access Token: {page['access_token']}")
    else:
        print("Lỗi:", response1.json())

    print(payload)
    response = requests.post(FB_API_URL, data=payload)
    print(response.json())
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    return {"status": "success", "post_id": response.json().get('id')}

    # return 'ok'
