from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
import uvicorn

app = FastAPI()

"""===作業方法===
1.環境構築
2.実際に動かす
3.編集する

1.環境構築
このAPIはpython3.12で動作させるため、開発も3.12で行うことを想定するが、バージョン揃えは必須ではない(3.12前後で仕様の大きな変更はないため)
必要なパッケージを導入する↓
作業ディレクトリを2024proc_5にし、このコマンドを実行↓
pip install -r requirements.txt

2.実際に動かす
普通にこのapp.pyファイルをターミナルでpythonで実行すればそれだけでAPIサーバーとして起動する
INFO:     Uvicorn running on http://0.0.0.0:3000 (Press CTRL+C to quit)
というログが出れば、正常に起動している
実際にAPIリクエストを送る場合は、 http://127.0.0.1:3000 のURLを使う(試しにブラウザで開いてみてほしい)
URLの末尾にパスを追加する http://127.0.0.1:3000/v1/

3.編集する
@app.get("/") または @app.post("/") などを書いて、次の行に非同期関数を定義する
この際にget()かpost()かでRESTのメソッドが何かをしている
get()ならばこのパスにGETメソッドでAPIリクエストをした際の処理を記述することになる

この関数でオブジェクトを返り値にすると、それがwebAPIのJSON形式での返り値になる
@app.get("/test")
async def hoge():
    return {"hoge": "hoga"}

http://127.0.0.1:3000/test/

クエリパラメータは関数の引数で定義する
@app.get("/test")
async def hoge(number: int = 0):
    return {"hoge": number + 1}

http://127.0.0.1:3000/test/?number=2

編集を反映するにはfastAPIのプロセスを再起動する必要がある
"""


def main():
    uvicorn.run(app, host="0.0.0.0", port=3000, log_level="debug")
    # ここhostは0.0.0.0じゃないといけないらしい


@app.get("/")
async def get():
    return {"message": "hello world! access v1 directory"}


@app.get("/v1/")
async def get():
    return {"message": "this is v1 directory"}


@app.get("/v1/statusTest/")
async def get(number: int = 0):
    print(number)
    if number == 0:
        return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "ok!"})
    else:
        return JSONResponse(
            status_code=status.HTTP_418_IM_A_TEAPOT, content={"message": "I'm tea pot!"}
        )


if __name__ == "__main__":
    main()
