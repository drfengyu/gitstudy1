import uuid
from enum import Enum
from typing import Union

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel
from starlette.responses import JSONResponse, PlainTextResponse
from apistudy import study1, study2, study3, study4, study5, study6, study7, study8,study9
from apistudy.models.exceptions import UnicornException
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.encoders import jsonable_encoder

app = FastAPI()
app.include_router(study1.router)
app.include_router(study2.router)
app.include_router(study3.router)
app.include_router(study4.router)
app.include_router(study5.router)
app.include_router(study6.router)
app.include_router(study7.router)
app.include_router(study8.router)
app.include_router(study9.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


# 安装自定义异常处理器
# 假设要触发的自定义异常叫作 UnicornException。
#
# 且需要 FastAPI 实现全局处理该异常。
#
# 此时，可以用 @app.exception_handler() 添加自定义异常控制器：
@app.exception_handler(UnicornException)
async def unicorn_exception_handler(request: Request, exc: UnicornException):
    return JSONResponse(
        status_code=418,
        content={"message": f"Oops! {exc.name} did something. There goes a rainbow..."}
    )


# 覆盖默认异常处理器¶
# FastAPI 自带了一些默认异常处理器。
#
# 触发 HTTPException 或请求无效数据时，这些处理器返回默认的 JSON 响应结果。
#
# 不过，也可以使用自定义处理器覆盖默认异常处理器。
#
# 覆盖请求验证异常¶
# 请求中包含无效数据时，FastAPI 内部会触发 RequestValidationError。
#
# 该异常也内置了默认异常处理器。
#
# 覆盖默认异常处理器时需要导入 RequestValidationError，并用 @app.excption_handler(RequestValidationError) 装饰异常处理器。
#
# 这样，异常处理器就可以接收 Request 与异常。
# 例如，只为错误返回纯文本响应，而不是返回 JSON 格式的内容：
# from fastapi.responses import PlainTextResponse
# from starlette.exceptions import HTTPException as StarletteHTTPException
# raise HTTPException(status_code=418, detail="Nope! I don't like 3.")
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)


# 使用 RequestValidationError 的请求体¶
# RequestValidationError 包含其接收到的无效数据请求的 body 。
#
# 开发时，可以用这个请求体生成日志、调试错误，并返回给用户。
@app.exception_handler(RequestValidationError)
async def request_validation_exception_handler(request: Request, exc: RequestValidationError):
    # return PlainTextResponse(str(exc), status_code=400)
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )


# FastAPI 调用的就是 RequestValidationError 类，因此，如果在 response_model 中使用 Pydantic 模型，且数据有错误时，在日志中就会看到这个错误。
#
# 但客户端或用户看不到这个错误。反之，客户端接收到的是 HTTP 状态码为 500 的「内部服务器错误」。
#
# 这是因为在响应或代码（不是在客户端的请求里）中出现的 Pydantic ValidationError 是代码的 bug。
#
# 修复错误时，客户端或用户不能访问错误的内部信息，否则会造成安全隐患。
#
# 覆盖 HTTPException 错误处理器¶
# 同理，也可以覆盖 HTTPException 处理器。
#
@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, exc):
    print(f"OMG!An HTTP error!:{repr(exc)}")
    return await http_exception_handler(request, exc)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    print(f"OMG!The client sent invalid data!:{exc}")
    return await request_validation_exception_handler(request, exc)
