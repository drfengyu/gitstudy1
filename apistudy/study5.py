'''
Author:fengling
time:2023/10/
'''
from typing import Annotated

from fastapi import APIRouter, Path, Query

router = APIRouter(
    prefix="/study5",
    tags=["路径参数和数值校验"],
)


# 导入Path 声明元数据
@router.get("/items/{item_id}")
async def read_items(item_id: Annotated[int, Path(title="The ID of the item to get")],
                     q: Annotated[str | None, Query(alias="item-query")] = None, ):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results


# 按需对参数排序
@router.get("/items2/{item_id}")
async def read_items2(q: str, item_id: int = Path(title="The ID of the item to get")):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results


# 按需对参数排序的技巧 *作为第一个参数, 之后参数都作为关键字参数,即使没有默认值
@router.get("/items3/{item_id}")
async def read_items3(*, item_id: int = Path(title="The ID of the item to get"), q: str):
    results = {"item_Id": item_id}
    if q:
        results.update({"q": q})
    return results


# 数值校验
'''
ge=1:: 大于等于1的整数
gt:大于
le:小于等于
'''


@router.get("/items4/{item_id}")
async def read_items4(
        *, item_id: int = Path(title="The ID of the item to get", gt=0, le=1000),
        q: str,
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results


@router.get("/items5/{item_id}")
async def read_items5(*,
                      item_id: int = Path(title="The ID of the item to get", ge=0, le=1000),
                      q: str,
                      size: float = Query(gt=0, lt=10.5), ):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results
