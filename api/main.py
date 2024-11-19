from datetime import timedelta
from typing import Any
from json import dumps, loads

from logging import getLogger, getLevelNamesMapping
from fastapi import FastAPI, status, Request, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from uvicorn import run as uvicornrun

from pydantic import BaseModel

from databases import literals as databaseliterals
from databases.accessor import connect, selectFrom, insertInto

import security.authenticate as auth


PORT = 3000
RELOAD = True  # 編集しファイルを保存するたびにサーバーを自動再起動するか
LOGLEVEL = "debug"  # "debug", "info", "warning", "error", "critical"

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
        log_level=getLevelNamesMapping()[LOGLEVEL.upper()],
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
EXCEPTION_REQUEST_FAILED_TO_PROCESS = HTTPException(
    detail="request was failed to process.",
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
)

RESPONSE_REQUEST_PROCESSED = APIResponse(
    message="request was processed successfully.", body=True
)
RESPONSE_NO_MATCH_IN_DB = APIResponse(
    message="specified id wasn't found in the table", body=False
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
    logger.debug(
        f"{request.client.host} has accessed to productCategory specifying {id}"
    )
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
    request: Request,
    id: int | None = None,
    current_admin: auth.Admin = Depends(auth.get_current_active_user),
) -> APIResponse:
    if request.client is None:
        raise EXCEPTION_BLANK_CLIENT_IP
    logger.debug(f"{request.client.host} has accessed to form specifying {id}")
    logger.info(f"{current_admin.username} has accessed to form specifying {id}")
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
    logger.debug(form)
    result = insertInto(
        connection,
        "form",
        ["product_array", "manpower"],
        [f"'{dumps(form["product_array"])}'", str(form["manpower"])],
    )
    connection.close()
    if result:
        return RESPONSE_REQUEST_PROCESSED
    else:
        raise EXCEPTION_REQUEST_FAILED_TO_PROCESS


@app.post("/v1/contact")
def postContact(request: Request, contact: dict = {}) -> APIResponse:
    if request.client is None:
        raise EXCEPTION_BLANK_CLIENT_IP
    logger.debug(f"{request.client.host} has posted to form with this query: {contact}")
    # if not type(contact["email_address"] is str or not type(form["title"] ))
    connection = connect()
    result = insertInto(
        connection,
        "contacts",
        [
            "email_address",
            "form_id",
            "title",
            "content",
        ],
        [
            contact["email_address"],
            contact["form_id"],
            contact["title"],
            contact["content"],
        ],
    )
    connection.close()
    logger.debug(contact)
    if result:
        return RESPONSE_REQUEST_PROCESSED
    else:
        raise EXCEPTION_REQUEST_FAILED_TO_PROCESS


@app.post("/v1/token")
async def login_for_access_token(
    request: Request, form_data: OAuth2PasswordRequestForm = Depends()
) -> auth.Token:
    admin = auth.authenticate_admin(form_data.username, form_data.password)
    if not admin:
        raise auth.EXCEPTION_INCORRECT_USER_OR_PASS
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": admin.username}, expires_delta=access_token_expires
    )
    return auth.Token(access_token=access_token, token_type="bearer")


@app.get("/admin/me", response_model=auth.Admin)
async def read_admin_me(
    current_admin: auth.Admin = Depends(auth.get_current_active_user),
):
    return current_admin


if __name__ == "__main__":
    main()
