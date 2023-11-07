'''
Author:fengling
time:2023/10/
'''
from apistudy.models.model import UserIn, UserInDB


def fake_password_hasher(raw_password: str):
    return "supersecret" + raw_password


def fake_save_user(user_in: UserIn):
    hashed_password = fake_password_hasher(user_in.password)
    # 如果我们将 user_dict 这样的 dict 以 **user_dict 形式传递给一个函数（或类），
    # Python将对其进行「解包」。它会将 user_dict 的键和值作为关键字参数直接传递。
    # 然后添加额外的关键字参数 hashed_password=hashed_password
    user_in_db = UserInDB(**user_in.dict(), hashed_password=hashed_password)
    print("User saved! ..not really")
    return user_in_db



