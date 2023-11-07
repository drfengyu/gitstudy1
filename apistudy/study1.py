'''
Author:fengling
time:2023/10/
'''
from enum import Enum

from fastapi import APIRouter

from .models.model import ModelName

# FASTAPI 1.路径参数

router = APIRouter(
    prefix="/study1",
    tags=["路径参数"],
)


@router.get("/items/{item_id}")
async def read_item(item_id):
    return {"item_id": item_id}


# 1.1 有类型的路径参数
@router.get("/items2/{item_id}")
async def read_item2(item_id: int):
    return {"item_id": item_id}


# 顺序很重要
@router.get('/users/me')
async def read_user_me():
    return {"user_id": "the current user"}


@router.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}


# 预设值



@router.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "leCNN all the images"}
    return {"model_name": model_name, "message": "Have some residuals"}


# 路径参数
@router.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}
