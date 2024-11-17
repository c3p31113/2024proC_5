from typing import Any
from json import dumps
from logging import getLogger
from fastapi import FastAPI, status, Request
from fastapi.responses import JSONResponse
from uvicorn import run as uvicornrun

from databases import literals as databaseliterals
from databases.accessor import connect, selectAllFrom, selectOneFrom, insertInto


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
    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
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
    content=APIResponse("specified id wasn't found in the table", None, False).output(),
    status_code=status.HTTP_200_OK,
    media_type="charset=utf-8",
)
RESPONSE_BLANK_QUERY = JSONResponse(
    content=APIResponse("query was blank.", None, False).output(),
    status_code=status.HTTP_400_BAD_REQUEST,
    media_type="charset=utf-8",
)
RESPONSE_REQUEST_PROCESSED = JSONResponse(
    content=APIResponse("request was processed successfully.").output(),
    status_code=status.HTTP_200_OK,
    media_type="charset=utf-8",
)
RESPONSE_REQUEST_INVALID = JSONResponse(
    content=APIResponse(
        "request form was invalid to read. check data structure"
    ).output(),
    status_code=status.HTTP_400_BAD_REQUEST,
    media_type="charset=utf-8",
)


@app.get("/")
def root(request: Request) -> JSONResponse:
    if request.client is None:
        return RESPONSE_BLANK_CLIENT_IP
    logger.debug(f"{request.client.host} has accessed to root")
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
    products = selectAllFrom(
        connection,
        databaseliterals.DATABASE_TABLE_PRODUCTS,
        ["*"],
    )
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
    logger.debug(f"{request.client.host} has accessed to product specifying {id}")
    if id is None:
        return RESPONSE_BLANK_QUERY
    connection = connect()
    product = selectOneFrom(
        connection, databaseliterals.DATABASE_TABLE_PRODUCTS, ["*"], f"ID = {id}"
    )
    if product is None:
        return RESPONSE_NO_MATCH_IN_DB
    connection.close()
    logger.debug(product)
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
        connection,
        databaseliterals.DATABASE_TABLE_PRODUCTCATEGORIES,
        ["*"],
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
    logger.debug(f"{request.client.host} has accessed to product specifying {id}")
    if id is None:
        return RESPONSE_BLANK_QUERY
    connection = connect()
    productCategory = selectOneFrom(
        connection,
        databaseliterals.DATABASE_TABLE_PRODUCTCATEGORIES,
        ["*"],
        f"ID = {id}",
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


@app.get("/v1/form")
def getForm(
    request: Request, id: int | None = None
) -> (
    JSONResponse
):  # TODO 認証が必要なようにする (そもそも認証システムがまだ用意されてない)
    if request.client is None:
        return RESPONSE_BLANK_CLIENT_IP
    logger.debug(f"{request.client.host} has accessed to product specifying {id}")
    if id is None:
        return RESPONSE_BLANK_QUERY
    connection = connect()
    form = selectOneFrom(
        connection, databaseliterals.DATABASE_TABLE_FORM, ["*"], f"ID = {id}"
    )
    if form is None:
        return RESPONSE_NO_MATCH_IN_DB
    connection.close()
    logger.debug(form)
    if form["ID"] == id:
        return JSONResponse(
            APIResponse("ok", form).output(),
            media_type="charset=utf-8",
        )
    return RESPONSE_NO_MATCH_IN_DB


@app.post("/v1/form")
def postForm(request: Request, form: dict = {}):  # TODO 未動作検証
    if request.client is None:
        return RESPONSE_BLANK_CLIENT_IP
    logger.debug(f"{request.client.host} has posted to form with this query: {form}")
    if not type(form["product_array"]) is list or not type(form["monpower"]) is int:
        return RESPONSE_REQUEST_INVALID
    connection = connect()
    insertInto(
        connection,
        "form",
        ["product_array", "manpower"],
        [dumps(form["product_array"]), form["manpower"]],
    )
    connection.close()
    logger.debug(form)
    return JSONResponse(
        APIResponse("request was processed successfully").output(),
        status_code=status.HTTP_200_OK,
        media_type="charset=utf-8",
    )


if __name__ == "__main__":
    main()
