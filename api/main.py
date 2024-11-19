from datetime import datetime, timedelta, timezone
from typing import Any
from json import dumps, loads

from logging import getLogger
from fastapi import FastAPI, status, Request, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
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

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def main():
    uvicornrun(
        "main:app",
        host="0.0.0.0",
        port=PORT,
        log_level=LOGLEVEL.lower(),
        reload=RELOAD,
        log_config="config/log_config.yaml",
    )


class APIResponse(BaseModel):
    message: str
    body: Any = None


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
    message="request was processed successfully.", body=True
)
RESPONSE_NO_MATCH_IN_DB = APIResponse(
    message="specified id wasn't found in the table", body=None
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
    form["product_array"] = loads(form["product_array"])
    logger.debug(form)
    if form["ID"] == id:
        return APIResponse(message="ok", body=form)
    return RESPONSE_NO_MATCH_IN_DB


@app.post("/v1/form")
def postForm(request: Request, form: dict = {}) -> APIResponse:
    if request.client is None:
        raise EXCEPTION_BLANK_CLIENT_IP
    logger.debug(f"{request.client.host} has posted to form with this query: {form}")
    if not type(form["product_array"]) is list or not type(form["manpower"]) is int:
        raise EXCEPTION_REQUEST_INVALID
    connection = connect()
    insertInto(
        connection,
        "form",
        ["product_array", "manpower"],
        [f"'{dumps(form["product_array"])}'", str(form["manpower"])],
    )
    connection.close()
    logger.debug(form)
    return RESPONSE_REQUEST_PROCESSED


@app.post("/v1/contact")
def postContact(request: Request, contact: dict = {}) -> APIResponse:
    if request.client is None:
        raise EXCEPTION_BLANK_CLIENT_IP
    logger.debug(f"{request.client.host} has posted to form with this query: {contact}")
    # if not type(contact["email_address"] is str or not type(form["title"] ))
    connection = connect()
    insertInto(
        connection,
        "contacts",
        ["email_address", "title", "content"],
        [contact["email_address"], contact["title"], contact["content"]],
    )
    connection.close()
    logger.debug(contact)
    return RESPONSE_REQUEST_PROCESSED


if __name__ == "__main__":
    main()
