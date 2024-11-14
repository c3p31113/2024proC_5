from typing import Any
from json import load
from logging import getLogger
from fastapi import FastAPI, status, Request
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from uvicorn import run as uvicornrun
from mysql.connector import MySQLConnection, errors as MYSQLerrors
from mysql.connector.cursor import MySQLCursor
import literals

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
class APIResponse(object):
    valid: bool
    message: str
    body: Any = None

    def __init__(
        self,
        message: str,
        body: Any = None,
        valid: bool = True,
    ) -> None:
        self.message = message
        self.valid = valid
        self.body = body

    def output(self) -> dict[str, Any]:
        return {"valid": self.valid, "message": self.message, "body": self.body}


RESPONSE_FAILED_TO_CONNECT_DB = JSONResponse(
    content=APIResponse(
        "couldn't connect to database", body=None, valid=False
    ).output(),
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    media_type="charset=utf-8",
)
RESPONSE_BLANK_CLIENT_IP = JSONResponse(
    content=APIResponse(
        "somehow you are non-existance client. couldn't get your IP",
        body=None,
        valid=False,
    ).output(),
    status_code=status.HTTP_400_BAD_REQUEST,
    media_type="charset=utf-8",
)
RESPONSE_NO_MATCH_IN_DB = JSONResponse(
    content=APIResponse(
        "specified product id wasn't found in the table", None, False
    ).output(),
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    media_type="charset=utf-8",
)
RESPONSE_BLANK_QUERY = JSONResponse(
    content=APIResponse("query was blank.", None, False).output(),
    status_code=status.HTTP_400_BAD_REQUEST,
    media_type="charset=utf-8",
)


def jsonload(filepath: str):
    with open(filepath, mode="r") as file:
        result = load(file)
    return result


def connect(configpath="./config/dbconfig.json"):
    config = jsonload(configpath)
    return MySQLConnection(
        host=config["host"],
        user=config["user"],
        password=config["password"],
        database=config["database"],
        collation="utf8mb4_general_ci",
    )


def selectFrom(
    connection: MySQLConnection, columns: str | list[str], table: str, where: str = ""
) -> MySQLCursor:
    cursor = connection.cursor(dictionary=True)
    if columns is str:
        query_columns = columns
    else:
        query_columns = " ".join(columns)
    if where != "":
        query = f"SELECT {query_columns} FROM {table} WHERE {where}"
    else:
        query = f"SELECT {query_columns} FROM {table}"
    try:
        cursor.execute(query)
    except MYSQLerrors.ProgrammingError:
        logger.error(f"query failed to run: {query}")
    return cursor


def selectAllFrom(
    connection: MySQLConnection,
    columns: str | list[str],
    table: str,
    where: str = "",
) -> list[dict[str, Any] | Any] | None:
    cursor = selectFrom(connection, columns, table, where)
    result = cursor.fetchall()
    cursor.close()
    return result


def selectOneFrom(
    connection: MySQLConnection,
    columns: str | list[str],
    table: str,
    where: str = "",
) -> dict[str, Any] | Any | None:
    cursor = selectFrom(connection, columns, table, where)
    result = cursor.fetchone()
    cursor.close()
    return result


@app.get("/")
def root(request: Request) -> JSONResponse:
    if request.client is None:
        return RESPONSE_BLANK_CLIENT_IP
    logger.info(f"{request.client.host} has accessed to root")
    return JSONResponse(
        APIResponse(
            "this is 2024proc sd5 API powered by fastAPI. check /docs page for documents"
        ).output()
    )


@app.get("/v1/")
def v1(request: Request) -> JSONResponse:
    return JSONResponse(APIResponse("this is 2024proc sd5 API, version 1").output())


@app.get("/v1/products")
def getProducts(request: Request) -> JSONResponse:
    if request.client is None:
        return RESPONSE_BLANK_CLIENT_IP
    connection = connect()
    products = selectAllFrom(connection, "*", "products")
    connection.close()
    if products is None:
        return RESPONSE_FAILED_TO_CONNECT_DB
    return JSONResponse(
        APIResponse("ok", products).output(),
        media_type="charset=utf-8",
    )


@app.get("/v1/product")
def getProduct(request: Request, id: int | None = None) -> JSONResponse:
    if request.client is None:
        return RESPONSE_BLANK_CLIENT_IP
    logger.info(f"{request.client.host} has accessed to product specifying {id}")
    if id is None:
        return RESPONSE_BLANK_QUERY
    connection = connect()
    product = selectOneFrom(
        connection, "*", literals.DATABASE_TABLE_PRODUCTS, f"ID = {id}"
    )
    if product is None:
        return RESPONSE_NO_MATCH_IN_DB
    connection.close()
    logger.info(product)
    if product is None:
        return RESPONSE_FAILED_TO_CONNECT_DB
    if product["ID"] == id:
        return JSONResponse(
            APIResponse("ok", product).output(),
            media_type="charset=utf-8",
        )
    return RESPONSE_NO_MATCH_IN_DB


@app.get("/v1/productCategories")
def getProductCategories(request: Request) -> JSONResponse:
    if request.client is None:
        return RESPONSE_BLANK_CLIENT_IP
    connection = connect()
    productCategories = selectAllFrom(
        connection, "*", literals.DATABASE_TABLE_PRODUCTCATEGORIES
    )
    connection.close()
    if productCategories is None:
        return RESPONSE_FAILED_TO_CONNECT_DB
    return JSONResponse(
        APIResponse("ok", productCategories).output(),
        media_type="charset=utf-8",
    )


@app.get("/v1/productCategory")
def getProductCategory(request: Request, id: int | None = None) -> JSONResponse:
    if request.client is None:
        return RESPONSE_BLANK_CLIENT_IP
    logger.info(f"{request.client.host} has accessed to product specifying {id}")
    if id is None:
        return RESPONSE_BLANK_QUERY
    connection = connect()
    productCategory = selectOneFrom(
        connection, "*", literals.DATABASE_TABLE_PRODUCTCATEGORIES, f"ID = {id}"
    )
    if productCategory is None:
        return RESPONSE_NO_MATCH_IN_DB
    connection.close()
    logger.info(productCategory)
    if productCategory["ID"] == id:
        return JSONResponse(
            APIResponse("ok", productCategory).output(),
            media_type="charset=utf-8",
        )
    return RESPONSE_NO_MATCH_IN_DB


if __name__ == "__main__":
    main()
