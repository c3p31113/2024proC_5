from datetime import datetime, timedelta, timezone
from typing import Any
from json import dumps

from logging import getLogger
from fastapi import FastAPI, status, Request, Depends, HTTPException
from fastapi.responses import JSONResponse
from uvicorn import run as uvicornrun

from pydantic import BaseModel

from databases import literals as databaseliterals
from databases.accessor import connect, selectFrom, insertInto


PORT = 3000
RELOAD = True  # 編集しファイルを保存するたびにサーバーを自動再起動するか
LOGLEVEL = "info"  # "debug", "info", "warning", "error", "critical"

logger = getLogger("uvicorn.app")
app = FastAPI()
print = logger.info  # ポインタって素晴らしい


def main():
    uvicornrun(
        "main:app",
        host="0.0.0.0",
        port=PORT,
        log_level=LOGLEVEL.lower(),
        reload=RELOAD,
        log_config="config/log_config.yaml",
    )


# TODO 出力したければoutputメソッドを呼ばないといけないことを考えると逆に面倒かもしれない
class APIResponse(BaseModel):
    message: str
    valid: bool = True
    body: Any = None


MEDIA_JSON_UTF8 = "application/json; charset=utf-8"

EXCEPTION_FAILED_TO_CONNECT_DB = HTTPException(
    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
    detail="couldn't connect to database",
)
EXCEPTION_BLANK_CLIENT_IP = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="somehow you are non-existance client. couldn't get your IP",
)
EXCEPTION_BLANK_QUERY = HTTPException(
    detail="query was blank",
    status_code=status.HTTP_400_BAD_REQUEST,
)
EXCEPTION_REQUEST_INVALID = HTTPException(
    detail="request form was invalid to read. check data structure",
    status_code=status.HTTP_400_BAD_REQUEST,
)

RESPONSE_REQUEST_PROCESSED = APIResponse(
    valid=True, message="request was processed successfully.", body=None
)
RESPONSE_NO_MATCH_IN_DB = APIResponse(
    valid=True, message="specified id wasn't found in the table", body=None
)


@app.get("/")
def root(request: Request) -> APIResponse:
    if request.client is None:
        raise EXCEPTION_BLANK_CLIENT_IP
    logger.debug(f"{request.client.host} has accessed to root")
    test = {
        "valid": True,
        "message": "this is 2024proc sd5 API powered by fastAPI. check /docs page for documents",
        "body": None,
    }
    return APIResponse(**test)


@app.get("/v1/")
def v1(request: Request) -> APIResponse:
    return APIResponse(message="this is 2024proc sd5 API, version 1")


@app.get("/v1/products")
def getProducts(request: Request) -> APIResponse:
    if request.client is None:
        raise EXCEPTION_BLANK_CLIENT_IP
    connection = connect()
    products = selectFrom(
        connection,
        databaseliterals.DATABASE_TABLE_PRODUCTS,
        "*",
    )
    connection.close()
    if products is None:
        raise EXCEPTION_FAILED_TO_CONNECT_DB
    return APIResponse(message="ok", body=products)


@app.get("/v1/product")
def getProduct(request: Request, id: int | None = None) -> APIResponse:
    if request.client is None:
        raise EXCEPTION_BLANK_CLIENT_IP
    logger.debug(f"{request.client.host} has accessed to product specifying {id}")
    if id is None:
        raise EXCEPTION_BLANK_QUERY
    connection = connect()
    product = selectFrom(
        connection,
        databaseliterals.DATABASE_TABLE_PRODUCTS,
        "*",
        f"ID = {id}",
        True,
    )
    if product is None:
        return RESPONSE_NO_MATCH_IN_DB
    connection.close()
    logger.debug(product)
    if product is None:
        raise EXCEPTION_FAILED_TO_CONNECT_DB
    if product["ID"] == id:
        return APIResponse(message="ok", body=product)
    return RESPONSE_NO_MATCH_IN_DB


@app.get("/v1/productCategories")
def getProductCategories(request: Request) -> APIResponse:
    if request.client is None:
        raise EXCEPTION_BLANK_CLIENT_IP
    connection = connect()
    productCategories = selectFrom(
        connection,
        databaseliterals.DATABASE_TABLE_PRODUCTCATEGORIES,
        "*",
    )
    connection.close()
    if productCategories is None:
        raise EXCEPTION_FAILED_TO_CONNECT_DB
    return APIResponse(message="ok", body=productCategories)


@app.get("/v1/productCategory")
def getProductCategory(request: Request, id: int | None = None) -> APIResponse:
    if request.client is None:
        raise EXCEPTION_BLANK_CLIENT_IP
    logger.debug(f"{request.client.host} has accessed to product specifying {id}")
    if id is None:
        raise EXCEPTION_BLANK_QUERY
    connection = connect()
    productCategory = selectFrom(
        connection,
        databaseliterals.DATABASE_TABLE_PRODUCTCATEGORIES,
        "*",
        f"ID = {id}",
        True,
    )
    if productCategory is None:
        return RESPONSE_NO_MATCH_IN_DB
    connection.close()
    logger.info(productCategory)
    if productCategory["ID"] == id:
        return APIResponse(message="ok", body=productCategory)
    return RESPONSE_NO_MATCH_IN_DB


@app.get("/v1/form")
def getForm(
    request: Request, id: int | None = None
) -> (
    APIResponse
):  # TODO 認証が必要なようにする (そもそも認証システムがまだ用意されてない)
    if request.client is None:
        raise EXCEPTION_BLANK_CLIENT_IP
    logger.debug(f"{request.client.host} has accessed to product specifying {id}")
    if id is None:
        raise EXCEPTION_BLANK_QUERY
    connection = connect()
    form = selectFrom(
        connection,
        databaseliterals.DATABASE_TABLE_FORM,
        "*",
        f"ID = {id}",
        True,
    )
    if form is None:
        return RESPONSE_NO_MATCH_IN_DB
    connection.close()
    logger.debug(form)
    if form["ID"] == id:
        return APIResponse(body="ok", message=form)
    return RESPONSE_NO_MATCH_IN_DB


@app.post("/v1/form")
def postForm(request: Request, form: dict = {}) -> APIResponse:  # TODO 未動作検証
    if request.client is None:
        raise EXCEPTION_BLANK_CLIENT_IP
    logger.debug(f"{request.client.host} has posted to form with this query: {form}")
    if not type(form["product_array"]) is list or not type(form["monpower"]) is int:
        raise EXCEPTION_REQUEST_INVALID
    connection = connect()
    insertInto(
        connection,
        "form",
        ["product_array", "manpower"],
        [dumps(form["product_array"]), form["manpower"]],
    )
    connection.close()
    logger.debug(form)
    return APIResponse(message="request was processed successfully")


if __name__ == "__main__":
    main()
