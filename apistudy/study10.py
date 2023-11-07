'''
Author:fengling
time:2023/10/
'''
from fastapi import APIRouter, Depends

from apistudy.models.model import Cat, CommonQueryParams

router = APIRouter(
    prefix="/study10",
    tags=["依赖项"],
)


# 依赖项
# 1.创建依赖项
# 2.导入Depends
# 3.声明依赖项
async def common_parameters(
        q: str | None = None,
        skip: int = 0,
        limit: int = 100
):
    return {"q": q, "skip": skip, "limit": limit}


@router.get("/items/")
async def read_items(commons: dict = Depends(common_parameters)):
    return commons


@router.get("/users/")
async def read_users(commons: dict = Depends(common_parameters)):
    return commons


# 类作为依赖项
fluffy = Cat(name="Mr Fluffy")

fake_items_db = [{"item_name": "Foo", "item_name": "Bar", "item_name": "Baz"}]


@router.get("/items2/")
async def read_items(commons: CommonQueryParams = Depends()):
    response = {}
    if commons.q:
        response.update({"q": commons.q})
    items = fake_items_db[commons.skip:commons.skip + commons.limit]
    response.update({"items": items})
    return response
