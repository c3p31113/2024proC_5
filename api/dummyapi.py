from logging import getLogger
from fastapi import FastAPI, status, Request
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import uvicorn

PORT = 3000
RELOAD = True  # 編集しファイルを保存するたびにサーバーを自動再起動するか
LOGLEVEL = "info"  # "debug", "info", "warning", "error", "critical"

logger = getLogger("uvicorn.app")
app = FastAPI()
print = logger.info  # ポインタって素晴らしい

products = [  # TODO mariadbデータベースに接続
    {
        "id": 1,
        "name": "あんぽ柿",
        "summary": "品種は平核無柿、鉢屋柿など",
        "desc": None,
        "product_categories_ID": 1,
        "kg_per_1a": 78,
        "yen_per_kg": 240,
    },
    {
        "id": 2,
        "name": "いちご",
        "summary": "品種はとちおとめ、さちのか、など",
        "desc": None,
        "product_categories_ID": 2,
        "kg_per_1a": 78,
        "yen_per_kg": 240,
    },
    {
        "id": 3,
        "name": "いんげん",
        "summary": "品種はいちず、鴨川グリーンなど",
        "desc": None,
        "product_categories_ID": 2,
        "kg_per_1a": 78,
        "yen_per_kg": 240,
    },
    {
        "id": 4,
        "name": "きゅうり",
        "summary": "品種はアンコール10、パイロット2号、南極1号など",
        "desc": None,
        "product_categories_ID": 2,
        "kg_per_1a": 78,
        "yen_per_kg": 240,
    },
    {
        "id": 5,
        "name": "さくらんぼ",
        "summary": "品種は佐藤錦など",
        "desc": None,
        "product_categories_ID": 1,
        "kg_per_1a": 78,
        "yen_per_kg": 240,
    },
    {
        "id": 6,
        "name": "さやえんどう",
        "summary": "品種は姫みどり、ゆうさやなど",
        "desc": None,
        "product_categories_ID": 2,
        "kg_per_1a": 78,
        "yen_per_kg": 240,
    },
]

productCategories = [
    {"id": 1, "name": "果樹類", "summary": None},
    {"id": 2, "name": "野菜類", "summary": None},
    {"id": 3, "name": "きのこ類", "summary": None},
]


def main():
    uvicorn.run(
        "dummyapi:app",
        host="0.0.0.0",
        port=PORT,
        log_level=LOGLEVEL.lower(),
        reload=RELOAD,
        log_config="config/log_config.yaml",
    )


# TODO 出力したければoutputメソッドを呼ばないといけないことを考えると逆に面倒かもしれない
class Response(object):
    valid: bool
    message: str
    body: list | dict | str | int | bool | float | None = None

    def __init__(
        self,
        message: str,
        body: list | dict | str | int | bool | float | None = None,
        valid: bool = True,
    ) -> None:
        self.message = message
        self.valid = valid
        self.body = body

    def output(self) -> dict:
        return {"valid": self.valid, "message": self.message, "body": self.body}


@app.get("/")
def root(request: Request) -> JSONResponse:
    if request.client is None:
        return JSONResponse(
            Response("somehow you are non existant client", valid=False).output(),
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    logger.info(f"{request.client.host} has accessed to root")
    return JSONResponse(Response("this is dummy API").output())


@app.get("/v1/")
def v1(request: Request) -> JSONResponse:
    return JSONResponse(Response("this is dummy API, v1").output())


@app.get("/v1/products")
def getProducts(request: Request) -> JSONResponse:
    return JSONResponse(
        Response("this is dummy data and can be outdated", products).output(),
        media_type="charset=utf-8",
    )


@app.get("/v1/product")
def getProduct(request: Request, id: int | None = None):
    if request.client is None:
        return JSONResponse(
            Response("somehow you are non existant client", valid=False).output(),
            status_code=status.HTTP_400_BAD_REQUEST,
            media_type="charset=utf-8",
        )
    logger.info(f"{request.client.host} has accessed to product specifying {id}")
    if id is None:
        return JSONResponse(
            Response("error. specify ID", valid=False).output(),
            status_code=status.HTTP_400_BAD_REQUEST,
            media_type="charset=utf-8",
        )
    for product in products:
        if product["id"] == id:
            return JSONResponse(
                Response(
                    "query ok. this is dummy data and can be outdated", product
                ).output(),
                media_type="charset=utf-8",
            )
    return JSONResponse(
        Response(
            "specified product id wasn't found in the table", None, False
        ).output(),
        media_type="charset=utf-8",
    )


@app.get("/v1/productCategories")
def getProductCategories(request: Request):
    return JSONResponse(
        Response("this is dummy data and can be outdated", productCategories).output(),
        media_type="charset=utf-8",
    )


@app.get("/v1/productCategory")
def getProductCategory(request: Request, id: int | None = None):
    if request.client is None:
        return JSONResponse(
            Response("somehow you are non existant client", valid=False).output(),
            status_code=status.HTTP_400_BAD_REQUEST,
            media_type="charset=utf-8",
        )
    logger.info(f"{request.client.host} has accessed to product specifying {id}")
    if id is None:
        return JSONResponse(
            Response("error. specify ID", valid=False).output(),
            status_code=status.HTTP_400_BAD_REQUEST,
            media_type="charset=utf-8",
        )
    for productCategory in productCategories:
        if productCategory["id"] == id:
            return JSONResponse(
                Response(
                    "query ok. this is dummy data and can be outdated", productCategory
                ).output(),
                media_type="charset=utf-8",
            )
    return JSONResponse(
        Response(
            "specified product id wasn't found in the table", None, False
        ).output(),
        media_type="charset=utf-8",
    )


# TODO formのダミーPOST

if __name__ == "__main__":
    main()
