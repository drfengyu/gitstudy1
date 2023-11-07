'''
Author:fengling
time:2023/10/
'''
from typing import Union

from fastapi import APIRouter
from pydantic import BaseModel

from .models.model import QItem

# FastApi Study 2.查询参数

router = APIRouter(
    prefix="/study2",
    tags=["查询参数"],
)
fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


@router.get("/items/")
# 查询参数
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip:skip + limit]


# 可选参数 查询参数类型转换 bool
@router.get("/items2/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item


# 多个路径和查询参数
@router.get("/users/{user_id}/items/{item_id}")
async def read_user_item(user_id: int, item_id: str, q: Union[str, None] = None, short: bool = False):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item


# 必须查询参数 needy
@router.get("/item3/{item_id}")
async def read_useritem(item_id: str, needy: str, skip: int = 0, limit: Union[int, None] = None):
    item = {"item_id": item_id, "needy": needy, "skip": skip, "limit": limit}
    return item





# 类作为参数
@router.put("/items4/{item_id}")
def update_item(item_id: int, item: QItem):
    return {"item_name": item.name, "item_price": item.price, "item_id": item_id}
