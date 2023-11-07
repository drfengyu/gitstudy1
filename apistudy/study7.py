'''
Author:fengling
time:2023/10/
'''
from typing import Union

from fastapi import APIRouter, status

from .helpers.passwordhelper import fake_save_user
from .models.model import Item, UserIn, UserOut, PlaneItem, CarItem, Item3

router = APIRouter(
    prefix="/study7",
    tags=["响应模型,额外的模型,响应状态码"],
)


@router.post("/items/", response_model=Item)
async def create_item(item: Item):
    return item


@router.get("/items2/", response_model=list[Item])
async def read_items():
    return [
        {"name": "Portal Gun", "price": 42.0},
        {"name": "Plumbus", "price": 32.0},
    ]


# 返回与输入相同的数据
@router.post("/user/", response_model=UserOut)
async def create_user(user: UserIn):
    return user


# 响应模型编码参数
items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}


# 响应模型编码参数 response_model_exclude_unset=True 不会包含默认值,只有实际设置的值
@router.get("/items3/{item_id}", response_model=Item, response_model_exclude_unset=True)
async def read_item(item_id: str):
    return items[item_id]


# {"name", "description"} 语法创建一个具有这两个值的 set。
#
# 等同于 set(["name", "description"])。
@router.get("/items4/{item_id}/name", response_model=Item, response_model_include={"name", "description"}, )
async def read_item_name(item_id: str):
    return items[item_id]


@router.get("/items5/{item_id}/public", response_model=Item, response_model_exclude={"tax"})
async def read_item_public_data(item_id: str):
    return items[item_id]


# 总结
# 使用路径操作装饰器的 response_model 参数来定义响应模型，特别是确保私有数据被过滤掉。
#
# 使用 response_model_exclude_unset 来仅返回显式设定的值。

# 额外的模型
@router.post("/user2/", response_model=UserOut)
async def create_user2(user_in: UserIn):
    user_saved = fake_save_user(user_in)
    return user_saved


items2 = {
    "item1": {
        "description": "All my friends drive a low rider",
        "type": "car",
    },
    "item2": {
        "description": "Music is my aeroplane,it's my aeroplane",
        "type": "plane",
        "size": 5,
    }
}


# 定义一个 Union 类型时，首先包括最详细的类型，然后是不太详细的类型。
# 在下面的示例中，更详细的 PlaneItem 位于 Union[PlaneItem，CarItem] 中的 CarItem 之前。
@router.get("/items6/{item_id}", response_model=Union[PlaneItem, CarItem])
async def read_item2(item_id: str):
    return items2[item_id]


items3 = [
    {"name": "Foo", "description": "There comes my hero"},
    {"name": "Red", "description": "It's my aeroplane"},
]


# 模型列表
@router.get("/items7/", response_model=list[Item3])
async def read_item3():
    return items3


# 任意dict构成的响应
@router.get("/keyword-weights/", response_model=dict[str, float])
async def read_keyword_weights():
    return {"foo": 2.3, "bar": 3.4}


# 响应状态码
@router.post("/items8/", status_code=201)
async def create_item2(name: str):
    return {"name": name}


# 关于HTTP状态码
'''
在 HTTP 协议中，你将发送 3 位数的数字状态码作为响应的一部分。

这些状态码有一个识别它们的关联名称，但是重要的还是数字。

简而言之：

100 及以上状态码用于「消息」响应。你很少直接使用它们。具有这些状态代码的响应不能带有响应体。
200 及以上状态码用于「成功」响应。这些是你最常使用的。
200 是默认状态代码，它表示一切「正常」。
另一个例子会是 201，「已创建」。它通常在数据库中创建了一条新记录后使用。
一个特殊的例子是 204，「无内容」。此响应在没有内容返回给客户端时使用，因此该响应不能包含响应体。
300 及以上状态码用于「重定向」。具有这些状态码的响应可能有或者可能没有响应体，但 304「未修改」是个例外，该响应不得含有响应体。
400 及以上状态码用于「客户端错误」响应。这些可能是你第二常使用的类型。
一个例子是 404，用于「未找到」响应。
对于来自客户端的一般错误，你可以只使用 400。
500 及以上状态码用于服务器端错误。你几乎永远不会直接使用它们。当你的应用程序代码或服务器中的某些部分出现问题时，它将自动返回这些状态代码之一。
'''


# 记住名称的捷径
@router.post("/items9/", status_code=status.HTTP_201_CREATED)
async def create_item3(name: str):
    return {"name": name}
