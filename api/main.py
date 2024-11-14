from typing import Any
from json import load
from logging import getLogger
from fastapi import FastAPI, status, Request
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from uvicorn import run as uvicornrun
from mysql.connector import MySQLConnection, errors as MYSQLerrors
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


RESPONSE_FAILED_TO_CONNECT_DB = APIResponse(
    "couldn't connect to database", body=None, valid=False
).output()
RESPONSE_BLANK_CLIENT_IP = APIResponse(
    "somehow you are non-existance client. couldn't get your IP", body=None, valid=False
).output()


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


def selectfrom(
    connection: MySQLConnection,
    columns: str | list[str],
    table: str,
    where: str = "",
) -> list[dict[str, Any] | Any] | None:
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
        print("the table doesn't exist!")
        return
    result = cursor.fetchall()
    cursor.close()
    return result


@app.get("/")
def root(request: Request) -> JSONResponse:
    if request.client is None:
        return JSONResponse(
            RESPONSE_BLANK_CLIENT_IP,
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    logger.info(f"{request.client.host} has accessed to root")
    return JSONResponse(APIResponse("this is dummy API").output())


@app.get("/v1/")
def v1(request: Request) -> JSONResponse:
    return JSONResponse(APIResponse("this is dummy API, v1").output())


@app.get("/v1/products")
def getProducts(request: Request) -> JSONResponse:
    connection = connect()
    products = selectfrom(connection, "*", "products")
    connection.close()
    if products is None:
        return JSONResponse(
            RESPONSE_FAILED_TO_CONNECT_DB,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    return JSONResponse(
        APIResponse("ok", products).output(),
        media_type="charset=utf-8",
    )


@app.get("/v1/product")
def getProduct(request: Request, id: int | None = None):
    if request.client is None:
        return JSONResponse(
            RESPONSE_BLANK_CLIENT_IP,
            status_code=status.HTTP_400_BAD_REQUEST,
            media_type="charset=utf-8",
        )
    logger.info(f"{request.client.host} has accessed to product specifying {id}")
    if id is None:
        return JSONResponse(
            APIResponse("error. specify ID", valid=False).output(),
            status_code=status.HTTP_400_BAD_REQUEST,
            media_type="charset=utf-8",
        )
    connection = connect()
    product_raw = selectfrom(
        connection, "*", literals.DATABASE_TABLE_PRODUCTS, f"ID = {id}"
    )
    if product_raw is None:
        return JSONResponse(
            RESPONSE_FAILED_TO_CONNECT_DB,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    product = product_raw[0]
    connection.close()
    logger.info(product)
    if product is None:
        return JSONResponse(
            RESPONSE_FAILED_TO_CONNECT_DB,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    if product["ID"] == id:
        return JSONResponse(
            APIResponse("query ok", product).output(),
            media_type="charset=utf-8",
        )
    return JSONResponse(
        APIResponse(
            "specified product id wasn't found in the table", None, False
        ).output(),
        media_type="charset=utf-8",
    )


@app.get("/v1/productCategories")
def getProductCategories(request: Request):
    connection = connect()
    productCategories = selectfrom(
        connection, "*", literals.DATABASE_TABLE_PRODUCTCATEGORIES
    )
    connection.close()
    if productCategories is None:
        return JSONResponse(
            APIResponse("couldn't connect to database", valid=False).output(),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    return JSONResponse(
        APIResponse("ok", productCategories).output(),
        media_type="charset=utf-8",
    )


@app.get("/v1/productCategory")
def getProductCategory(request: Request, id: int | None = None):
    if request.client is None:
        return JSONResponse(
            APIResponse("somehow you are non existant client", valid=False).output(),
            status_code=status.HTTP_400_BAD_REQUEST,
            media_type="charset=utf-8",
        )
    logger.info(f"{request.client.host} has accessed to product specifying {id}")
    if id is None:
        return JSONResponse(
            APIResponse("error. specify ID", valid=False).output(),
            status_code=status.HTTP_400_BAD_REQUEST,
            media_type="charset=utf-8",
        )
    connection = connect()
    productCategory_raw = selectfrom(
        connection, "*", literals.DATABASE_TABLE_PRODUCTCATEGORIES, f"ID = {id}"
    )
    if productCategory_raw is None:
        return JSONResponse(
            APIResponse("couldn't connect to database", valid=False).output(),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    productCategory = productCategory_raw[0]
    connection.close()
    logger.info(productCategory)
    if productCategory["id"] == id:
        return JSONResponse(
            APIResponse(
                "query ok. this is dummy data and can be outdated", productCategory
            ).output(),
            media_type="charset=utf-8",
        )
    return JSONResponse(
        APIResponse(
            "specified product id wasn't found in the table", None, False
        ).output(),
        media_type="charset=utf-8",
    )


if __name__ == "__main__":
    main()
