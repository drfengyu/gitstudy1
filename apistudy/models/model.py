'''
Author:fengling
time:2023/10/
'''
from datetime import datetime
from enum import Enum
from typing import Union

from pydantic import BaseModel, Field, HttpUrl, EmailStr


# 创建数据模型
class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


class QItem(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None


# Field的附加参数
class Item(BaseModel):
    name: str = Field(examples=["Foo"])
    description: str | None = Field(
        default=None, title="The description of the item",
        max_length=300,
        examples=["A very nice Item"]
    )
    price: float = Field(gt=0, description="The price must be greater than zero", examples=[20.5])
    tax: float | None = Field(default=None, examples=[3.0])
    tags: set[str] = set()


class User(BaseModel):
    username: str
    fullname: str | None = None


class Image(BaseModel):
    # url: str
    # 特殊的类型和校验
    url: HttpUrl
    name: str


class ShopItem(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    # tags: list = []
    # tags: list[str] = []
    tags: set[str] = set()
    # 定义子模型用作类型
    # images: Image | None = None
    # 带有一组子模型的属性
    images: list[Image] | None = None
    # 模式的额外信息 例子
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Foo",
                    "description": "A very nice Item",
                    "price": 35.4,
                    "tax": 3.2,
                    "tags": ["a", "v", "c"],
                    "images": [
                        {"url": "https://1.jpg", "name": "1"}
                    ]
                }
            ]
        }
    }


# 深度嵌套模型
class Offer(BaseModel):
    name: str
    description: str | None = None
    price: float
    items: list[ShopItem]


# 多个模型
class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None


class UserIn(BaseModel):
    # username: str
    password: str
    # email: EmailStr
    # full_name: Union[str, None] = None


class UserOut(BaseModel):
    # username: str
    # email: EmailStr
    # full_name: str | None = None
    pass


class UserInDB(BaseModel):
    # username: str
    hashed_password: str
    # email: EmailStr
    # full_name: str | None = None


# Union 或者 anyOf¶
# 你可以将一个响应声明为两种类型的 Union，这意味着该响应将是两种类型中的任何一种。
#
# 这将在 OpenAPI 中使用 anyOf 进行定义。
class BaseItem(BaseModel):
    description: str
    type: str


class CarItem(BaseItem):
    type: str = "car"


class PlaneItem(BaseItem):
    type: str = "plane"
    size: int


class Item3(BaseModel):
    name: str
    description: str


class Item4(BaseModel):
    title: str
    size: int


class Item5(BaseModel):
    title: str
    timestamp: datetime
    description: str | None = None


class Cat:
    def __init__(self, name: str):
        self.name = name


class CommonQueryParams:
    def __init__(self, q: str | None = None, skip: int = 0, limit: int = 100):
        self.q = q
        self.skip = skip
        self.limit = limit

