'''
Author:fengling
time:2023/10/
'''
from fastapi import APIRouter, Form, File, UploadFile, HTTPException, Request
from fastapi.responses import HTMLResponse
from starlette.responses import JSONResponse

from apistudy.models.exceptions import UnicornException
from apistudy.models.model import Item4

router = APIRouter(
    prefix="/study8",
    tags=["表单数据,请求文件,处理错误"],

)


@router.post("/login/")
async def login(username: str = Form(), password: str = Form()):
    return {"username": username}


# 请求文件 可选文件上传 设置额外元数据
@router.post("/file/")
async def create_file(file: bytes | None = File(default=None, description="A file read as bytes")):
    if not file:
        return {"message": "No file sent"}
    else:
        return {"file_size": len(file)}


@router.post("/uploadfile/")
async def create_upload_file(file: UploadFile | None = File(default=None, description="A file read as UploadFile"), ):
    if not file:
        return {"message": "No upload file sent"}
    else:
        return {"filename": file.filename}


@router.post("/files/")
async def create_files(files: list[bytes] = File(description="Multiple files as bytes")):
    return {"file_sizes": [len(file) for file in files]}


@router.post("/uploadfiles/")
async def create_upload_files(files: list[UploadFile] = File(description="Multiple files as UploadFile")):
    return {"filenames": [file.filename for file in files]}


'''
也可以使用 from starlette.responses import HTMLResponse。

fastapi.responses 其实与 starlette.responses 相同，只是为了方便开发者调用。
实际上，大多数 FastAPI 的响应都直接从 Starlette 调用。
'''


@router.get("/")
async def main():
    content = """
    <body>
    <form action="/study8/files/" enctype="multipart/form-data" method="post">
    <input name="files" type="file" multiple>
    <input type="submit">
    </form>
    <form action="/study8/uploadfiles/" enctype="multipart/form-data" method="post">
    <input name="files" type="file" multiple>
    <input type="submit">
    </form>
    <form action="/study8/files2/" enctype="multipart/form-data" method="post">
    <input name="file" type="file">
    <input name="fileb" type="file" multiple>
    <label>token:</label>
    <input name="token" type="text">
    <input type="submit">
    </form>
    </body>
    """
    return HTMLResponse(content=content)


@router.post("/files2/")
async def create_file(
        file: bytes = File(),
        fileb: UploadFile = File(),
        token: str = Form(),
):
    return {
        "file_size": len(file),
        "token": token,
        "fileb_content_type": fileb.content_type,
    }


# 使用HTTPException
# 向客户端返回HTTP错误响应,可以使用HTTPException

items = {"foo": "The Foo Wrestlers"}


@router.get("/items/{item_id}")
async def read_item(item_id: str):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item": items[item_id]}


# 添加自定义响应头
# 有些场景下要为 HTTP 错误添加自定义响应头。例如，出于某些方面的安全需要。
#
# 一般情况下可能不会需要在代码中直接使用响应头。
#
# 但对于某些高级应用场景，还是需要添加自定义响应头：
@router.get("/items-header/{item_id}")
async def read_item_header(item_id: str):
    if item_id not in items:
        raise HTTPException(
            status_code=404,
            detail="Item not found",
            headers={"X-Error": "There goes my error"},
        )
    return {"item": items[item_id]}


@router.get("/unicorns/{name}")
async def read_unicorn(name: str):
    if name == "yolo":
        raise UnicornException(name=name)
    return {"unicorn_name": name}


@router.get("/items2/{item_id}")
async def read_item(item_id: int):
    if item_id == 3:
        raise HTTPException(status_code=418, detail="Nope!I don't like 3.")
    return {"item_id": item_id}


@router.post("/items3/")
async def create_item(item: Item4):
    return item

