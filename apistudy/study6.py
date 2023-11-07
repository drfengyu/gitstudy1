'''
Author:fengling
time:2023/10/
'''
import uuid
from datetime import datetime, time, timedelta
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Body, Cookie, Header

router = APIRouter(
    prefix="/study6",
    tags=["额外数据类型,Cookie参数,Header参数"],
)


@router.get("/getuuid/")
async def idget():
    return str(uuid.uuid4())


@router.put("/items/{item_id}")
async def read_items(
        item_id: UUID,
        start_datetime: Annotated[datetime | None, Body()] = None,
        end_datetime: Annotated[datetime | None, Body()] = None,
        repeat_at: Annotated[time | None, Body()] = None,
        process_after: Annotated[timedelta | None, Body()] = None,
):
    start_process = start_datetime + process_after
    duration = end_datetime - start_process
    return {
        "item_id": await idget(),
        "start_datetime": start_datetime,
        "end_datetime": end_datetime,
        "repeat_at": repeat_at,
        "process_after": process_after,
        "start_process": start_process,
        "duration": duration
    }


# 导入Cookie
@router.get("/cookie/")
async def input_cookie(ads_id: Annotated[str | None, Cookie()] = None):
    return {"ads_id": ads_id}


# 导入Header convert_underscores=False 禁用下划线到连字符的自动转换
@router.get("/headers/")
async def read_items(user_agent: Annotated[str | None, Header(convert_underscores=False)] = None):
    return {"User-Agent": user_agent}

# 重复的headers
@router.get("/moreheaders/")
async def moreheaders(x_token: Annotated[list[str] | None, Header()] = None):
    return {"X-Token values": x_token}

