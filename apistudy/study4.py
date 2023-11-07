'''
Author:fengling
time:2023/10/
'''
from typing import Union, List

from fastapi import APIRouter, Query
from pydantic.v1 import Required

router = APIRouter(
    prefix="/study4",
    tags=["查询参数和字符串校验"],
)


@router.get("/items/")
async def read_items(q: str | None = None):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# 额外的校验 q 不能大于50字符 使用Query作为默认值,设置max_length=50
@router.get("/items2/")
async def read_items2(q: Union[str, None] = Query(default=None, max_length=50)):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# 添加更多检验
@router.get("/items3/")
async def read_items3(q: Union[str, None] = Query(default=None, min_length=3, max_length=50)):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# 添加正则表达式
@router.get("/items4/")
async def read_items4(q: Union[str, None] = Query(default=None, min_length=3, max_length=50, pattern="^fixedquery$"), ):
    '''
    - ^:以该符号之后的字符开头,符号之前没有字符.
    - fixedquery:值精确地等于fixedquery.
    - $:到此结束,在fixedquery之后没有更多字符.
    :param q:
    :return:
    '''
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# 默认值
@router.get("/items5/")
async def read_items5(q: str = Query(default="fixedquery", min_length=3)):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# 声明为必须参数
@router.get("/items6/")
async def read_items6(q: str = Query(min_length=3)):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# 使用省略号(...)声明必需参数
@router.get("/items7/")
async def read_items7(q: str = Query(default=..., min_length=3)):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# 使用None声明必需参数
@router.get("/items8/")
async def read_items8(q: Union[str, None] = Query(default=..., min_length=3)):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# 使用Pydantic中的Required代替省略号 通常可以省略default参数
@router.get("/items9/")
async def read_items9(q: str = Query(default=Required, min_length=3)):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# 查询参数列表/多个值 接受多个值
@router.get("/items10/")
async def read_items10(q: Union[List[str], None] = Query(default=None)):
    query_items = {"q": q}
    return query_items


# 具有默认值的查询参数列表
@router.get("/items11/")
async def read_items11(q: Union[List[str], None] = Query(default=["foo", "bar"])):
    query_items = {"q": q}
    return query_items


# 使用list 代替List[str]
@router.get("/items12/")
async def read_items12(q: list = Query(default=[])):
    query_items = {"q": q}
    return query_items


# 声明更多元数据
# 添加title description
@router.get("/items13/")
async def read_items13(q: Union[str, None] = Query(default=None,
                                                   title="Query string",
                                                   description="Query string for the items to search in the database "
                                                               "that"
                                                               "have a good match",
                                                   min_length=3)):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# 别名参数
@router.get("/items14/")
async def read_items14(q: Union[str, None] = Query(default=None, alias="item-query")):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# 启用参数
@router.get("/items15/")
async def read_items15(q: Union[str, None] = Query(
    default=None,
    alias="item-query",
    title="Query string",
    description="Query string for the items to search in the database that have a good match",
    min_length=3,
    max_length=50,
    pattern="^fixedquery$",
    deprecated=True,
)):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results
