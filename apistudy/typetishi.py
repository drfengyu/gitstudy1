'''
Author:fengling
time:2023/10/
'''
# Fastapi学习 类型提示
from datetime import datetime
from typing import List, Tuple, Set, Dict

from pydantic import BaseModel, PositiveInt, ValidationError


# def get_full_name(first_name,last_name):
#     full_name=first_name.title()+" "+last_name.title()
#     return full_name
#
# print(get_full_name("john","doe"))

# Study
# 1.类型提示
def get_full_name(first_name: str, last_name: str):
    full_name = first_name.title() + " " + last_name.title()
    return full_name


print(get_full_name("john", "doe"))


# 2.错误检查
def get_name_with_age(name: str, age: int):
    name_with_age = name + "is the old" + str(age)
    return name_with_age


# 嵌套类型 可以使用 Python 的 typing 标准库来声明这些类型以及子类型。
# 定义一个str组成的list变量
def process_items(items: List[str]):
    for item in items:
        print(item.title())


# 元组和集合
def process_itemts(items_t: Tuple[int, int, str], items_s: Set[bytes]):
    return items_t, items_s


# 字典
def process_itemdict(prices: Dict[str, float]):
    for item_name, item_price in prices.items():
        print(item_name)
        print(item_price)


process_itemdict({"a": 123.4})


# 类作为类型
class Person:
    def __init__(self, name: str):
        self.name = name


def get_person_name(one_person: Person):
    return one_person.name


# Pydantic模型 用来执行数据校验的Python库

class Delivery(BaseModel):
    timestamp: datetime
    dimensions: Tuple[int, int]


m = Delivery(timestamp='2020-01-02T03:04:05Z', dimensions=['10', '20'])
print(repr(m.timestamp))
print(m.dimensions)

# 验证成功
class User(BaseModel):
    id: int
    name: str = 'John Doe'
    signup_ts: datetime | None
    tastes: dict[str, PositiveInt]  # 必须大于0

external_data={
    'id':123,
    'signup_ts':'2019-06-01 12:22',
    'tastes':{
        'wine':9,
        b'cheese':7,
        'cabbage':'1',
        },
}

user=User(**external_data)
print(user.id)
print(user.model_dump())

external_data={'id':'not an int','tastes':{}}
try:
    User(**external_data)
except ValidationError as e:
    print(e.errors())