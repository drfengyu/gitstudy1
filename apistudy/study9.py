'''
Author:fengling
time:2023/10/
'''
from fastapi import APIRouter
from starlette import status

from apistudy.models.model import Item
from fastapi.encoders import jsonable_encoder

router = APIRouter(
    prefix="/study9",
    tags=["路径操作配置,JSON兼容编码器,请求体-更新数据"],
)


# status_code summary description参数
@router.post("/items/", response_model=Item,
             status_code=status.HTTP_201_CREATED,
             summary="Create an item",
             description="Create an item with all the information,name,"
                         "description,price,tax and a set of unique tags")
async def create_item(item: Item):
    return item


# tags参数
@router.get("/items2/", tags=["items"])
async def read_items():
    return [{"name": "Foo", "price": 42}]


@router.get("/users/", tags=["users"])
async def read_user():
    return [{"username": "johndoe"}]


# 文档字符串(docstring) 响应描述
@router.post("/items3/", response_model=Item, summary="Create an item",
             response_description="The created item")
async def create_item2(item: Item):
    '''
    Create an item with all the information:
    - **name**:each item must have a name
    - **description**:a long description
    - **price**:required
    - **tax**:if the item doesn't have tax,you can omit this
    - **tags**:a set of unique tag strings for this item
    '''
    return item


# 弃用路径参数
@router.get("/elements/", tags=["items"], deprecated=True)
async def real_elements():
    return [{"item_id": "Foo"}]


# 使用jsonable_encoder¶
# 让我们假设你有一个数据库名为fake_db，它只能接收与JSON兼容的数据。
#
# 例如，它不接收datetime这类的对象，因为这些对象与JSON不兼容。
#
# 因此，datetime对象必须将转换为包含ISO格式化的str类型对象。
#
# 同样，这个数据库也不会接收Pydantic模型（带有属性的对象），而只接收dict。
#
# 对此你可以使用jsonable_encoder。
#
# 它接收一个对象，比如Pydantic模型，并会返回一个JSON兼容的版本：
fake_db = {}


@router.put("/items/{id}")
def update_item(id: str, item: Item):
    json_compatible_item_data = jsonable_encoder(item)
    fake_db[id] = json_compatible_item_data


# 请求体-更新数据
# 把输入数据转换为以 JSON 格式存储的数据（比如，使用 NoSQL 数据库时），
# 可以使用 jsonable_encoder。例如，把 datetime 转换为 str。

items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}


# 用PUT更新数据
@router.put("/items2/{item_id}", response_model=Item)
async def update_item(item_id: str, item: Item):
    update_item_encoded = jsonable_encoder(item)
    items[item_id] = update_item_encoded
    return update_item_encoded


# 用PATCH进行部分更新
# 使用 Pydantic 的 exclude_unset 参数¶
# 更新部分数据时，可以在 Pydantic 模型的 .dict() 中使用 exclude_unset 参数。
#
# 比如，item.dict(exclude_unset=True)。
#
# 这段代码生成的 dict 只包含创建 item 模型时显式设置的数据，而不包括默认值。
#
# 然后再用它生成一个只含已设置（在请求中所发送）数据，且省略了默认值的 dict：
@router.patch("/items3/{item_id}", response_model=Item)
async def update_item2(item_id: str, item: Item):
    stored_item_data = items[item_id]
    stored_item_model = Item(**stored_item_data)
    update_data = item.dict(exclude_unset=True)
    updated_item = stored_item_model.copy(update=update_data)
    items[item_id] = jsonable_encoder(updated_item)
    return updated_item

# 简而言之，更新部分数据应：
#
# 使用 PATCH 而不是 PUT （可选，也可以用 PUT）；
# 提取存储的数据；
# 把数据放入 Pydantic 模型；
# 生成不含输入模型默认值的 dict （使用 exclude_unset 参数）；
# 只更新用户设置过的值，不用模型中的默认值覆盖已存储过的值。
# 为已存储的模型创建副本，用接收的数据更新其属性 （使用 update 参数）。
# 把模型副本转换为可存入数据库的形式（比如，使用 jsonable_encoder）。
# 这种方式与 Pydantic 模型的 .dict() 方法类似，但能确保把值转换为适配 JSON 的数据类型，例如， 把 datetime 转换为 str 。
# 把数据保存至数据库；
# 返回更新后的模型。
@router.get("/items4/{item_id}")
async def getitems(item_id: str):
    return items[item_id]
