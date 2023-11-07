'''
Author:fengling
time:2023/10/
'''
from typing import Annotated, List

from fastapi import APIRouter, Depends, Path, Body
from pydantic import BaseModel

from .models.model import Item, User, ShopItem, Offer, Image

# 3.请求体
router = APIRouter(
    prefix="/study3",
    tags=["请求体"],
    responses={404: {"description": "Not found"}}
)


# 声明为参数
@router.post("/items/")
async def create_item(item: Item):
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict


# 请求体+路径参数
@router.put('/items2/{item_id}')
async def create_item(item_id: int, item: Item):
    return {"item_id": item_id, **item.dict()}


# 请求体+路径参数+查询参数

@router.put("/items3/{item_id}")
async def create_item(item_id: int, item: Item, q: str | None = None):
    result = {"item_id": item_id, **item.dict()}
    if q:
        result.update({"q": q})
    return result


# 请求体-多个参数
# 混合使用Path,Query和请求体参数
@router.put("/items4/{item_id}")
async def update_item(
        item_id: Annotated[int, Path(title="The ID of the item to get", ge=0, le=1000)],
        q: str | None = None,
        item: Item | None = None,
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    if item:
        results.update({"item": item})
    return results


# 多个请求体参数
@router.put("/items5/{item_id}")
async def update_item(item_id: int, item: Item, user: User):
    results = {"item_id": item_id, "item": item, "user": user}
    return results


# 请求体中的单一值
@router.put("/items6/{item_id}")
async def update_item(item_id: int,
                      item: Item,
                      user: User,
                      importance: Annotated[int, Body()]):
    results = {"item_id": item_id, "item": item, "user": user, "importance": importance}
    return results


# 多个请求体参数和查询参数
@router.put("/items7/{item_id}")
async def update_item(
        *,
        item_id: int,
        item: Item,
        user: User,
        importance: Annotated[int, Body(gt=0)],
        q: str | None = None,
):
    results = {"item_id": item_id, "item": item, "user": user, "importance": importance}
    if q:
        results.update({"q": q})
    return results


# 嵌入单个请求体参数
@router.put("/items8/{item_id}")
async def update_item(item_id: int,
                      item: Annotated[
                          Item,
                          Body(examples=[{
                              "name":"egg",
                              "description":"A very nice egg",
                              "price":28.8,
                              "tax":2,
                          }
                          ],
                          ),
                      ]):
    results = {"item_id": item_id, "item": item}
    return results


# 请求体—字段
@router.put("/items9/{item_id}")
async def update_item(item_id: int, item: Annotated[Item, Body(embed=True)]):
    results = {"item_id": item_id, "item": item}
    return results


# 请求体-嵌套模型
@router.put("/items10/{item_id}")
async def update_item(item_id: int, item: ShopItem):
    results = {"item_id": item_id, "item": item}
    return results


@router.post("/offers/")
async def create_offer(offer: Offer):
    return offer


# 纯列表请求体
@router.post("/images/multiple/")
async def create_multiple_images(images: list[Image]):
    for image in images:
        print(image.url)
    return images


@router.post("/index-weights/")
async def create_index_weights(weights: dict[int, float]):
    return weights
