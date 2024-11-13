from logging import getLogger
from fastapi import FastAPI, status, Request
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import uvicorn

PORT = 3000
RELOAD = True  # 編集しファイルを保存するたびにサーバーを自動再起動するか
LOGLEVEL = "info"  # "debug", "info", "warning", "error", "critical"

"""===作業方法===
1.環境構築
2.実際に動かす
3.編集する

1.環境構築
このAPIはpython3.12で動作させるため、開発も3.12で行うことを想定するが、バージョン揃えは必須ではない(3.12前後で仕様の大きな変更はないため)
必要なパッケージを導入する↓
作業ディレクトリを2024proc_5にし、このコマンドを実行↓
pip install -r requirements.txt
もしかしたらこっちかも
python -m pip install -r requirements.txt

2.実際に動かす
普通にこのapp.pyファイルをターミナルでpythonで実行すればそれだけでAPIサーバーとして起動する
INFO:     Uvicorn running on http://0.0.0.0:3000 (Press CTRL+C to quit)
というログが出れば、正常に起動している
実際にAPIリクエストを送る場合は、 http://127.0.0.1:3000 のURLを使う(試しにブラウザで開いてみてほしい)
URLの末尾にパスを追加する http://127.0.0.1:3000/v1/

3.編集する
@app.get("/") または @app.post("/") などを書いて、次の行に関数を定義する
この際に@app.get()か@app.post()かでRESTのメソッドが何かを指定している
@app.get()ならばこのパスにGETメソッドでAPIリクエストをした際の処理を記述することになる

この関数でオブジェクトを返り値にすると、それがwebAPIのJSON形式での返り値になる
@app.get("/test")
def hoge():
    return {"hoge": "hoga"}

http://127.0.0.1:3000/test/

諸々の利便性から、返り値はdictやlistではなく、JSONResponseを用いると良い (優先度は低めなのでやらなくてもいい)
HTTPのステータスコードを設定できる
@app.get("/test")
def hoge() -> JSONResponse:
    return JSONResponse(status_code=status.HTTP_200_OK, content={"hoge": "hoga"})

http://127.0.0.1:3000/test/

クエリパラメータは関数の引数で定義する
@app.get("/test")
def hoge(number: int = 0):
    return {"hoge": number + 1}

http://127.0.0.1:3000/test/?number=2

編集を反映するにはfastAPIのプロセスを再起動する必要がある
RELOAD が True の場合は不要
"""

logger = getLogger("uvicorn.app")
app = FastAPI()
print = logger.info  # ポインタって素晴らしい


def main():
    uvicorn.run(
        "test:app",
        host="0.0.0.0",
        port=PORT,
        log_level=LOGLEVEL.lower(),
        reload=RELOAD,
        log_config="config/log_config.yaml",
    )


# http://127.0.0.1:3000/
@app.get("/")
def root() -> JSONResponse:
    logger.info("log test!")
    return JSONResponse({"message": "hello world! access v1 directory"})


# http://127.0.0.1:3000/v1/
@app.get("/v1/")
def v1() -> JSONResponse:
    return JSONResponse({"message": "this is v1 directory"})


# http://127.0.0.1:3000//v1/test/
@app.get("/v1/test/")
def v1_test() -> JSONResponse:
    return JSONResponse({})


# http://127.0.0.1:3000//v1/test/statusTest/
# http://127.0.0.1:3000//v1/test/statusTest?number=0
# http://127.0.0.1:3000//v1/test/statusTest?number=1
#
# クエリパラメータは関数の引数として宣言する
@app.get("/v1/test/statusTest/")
def v1_test_statustest(request: Request, number: int = 0) -> JSONResponse:
    if request.client is None:
        return JSONResponse(
            {"message": "somehow you are non existant client"},
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    client_host = request.client.host
    print(f"{client_host} {number}")
    if number == 0:
        return JSONResponse(
            {"message": "ok!", "number": number},
            status_code=status.HTTP_200_OK,
        )
    else:
        return JSONResponse(
            {"message": "I'm tea pot!", "number": number},
            status_code=status.HTTP_418_IM_A_TEAPOT,
        )


class Coffee(BaseModel):
    id: int
    taste: str
    amount: float


@app.post("/v1/test/posttest/")
def v1_test_posttest(request: Request, coffee: Coffee) -> JSONResponse:
    return JSONResponse(
        {
            "message": "ok!",
            "sent_query": {
                "id": coffee.id,
                "taste": coffee.taste,
                "amount": coffee.amount,
            },
        }
    )


@app.post("/v1/test/posttests/")
def v1_test_posttests(request: Request, coffees: list[Coffee]) -> JSONResponse:
    sentquery: list[dict] = []
    for coffee in coffees:
        sentquery.append(
            {
                "id": coffee.id,
                "taste": coffee.taste,
                "amount": coffee.amount,
            }
        )
    return JSONResponse({"message": "ok!", "sent_query": sentquery})


# http://127.0.0.1:3000/v1/test/items_
# http://127.0.0.1:3000/v1/test/items_1
# http://127.0.0.1:3000/v1/test/items_5
#
# 動的URL
@app.get("/v1/test/items_{number}")
def v1_test_items(request: Request, number: int = 0) -> JSONResponse:
    print(f"selected number was {number}")
    return JSONResponse({"message": "request ok!", "number": number})


if __name__ == "__main__":
    main()
