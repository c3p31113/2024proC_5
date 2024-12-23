# 2024年度プロジェクト演習C
## 5グループリポジトリ
<!-- <img src="https://img.shields.io/badge/any_text-you_like-blue" title="test"><br> -->
<img src="https://img.shields.io/badge/PHP_8.3-ccc?logo=php&style=flat">
<img src="https://img.shields.io/badge/Python_3.12-F9DC3E?logo=python&style=flat">
<img src="https://img.shields.io/badge/Apache_2.4-D22128?logo=apache&style=flat">
<img src="https://img.shields.io/badge/FastAPI_0.115.3-009688?logo=FastAPI&style=flat&logoColor=FFFFFF">
<!-- <img src="https://img.shields.io/badge/jQuery_3.7-0769AD.svg?logo=jquery&style=flat"> -->

<!-- ![エビフライトライアングル](http://i.imgur.com/Jjwsc.jpg "サンプル") -->
### 概要
- 文教大学湘南キャンパス、情報学部情報システム学科、プロジェクト演習グループ5(E)「福島県伊達市に向けた新規就農者向け書類作成補助システム開発プロジェクト」の開発リポジトリです
- 主な開発言語はPython、JavaScript

- 主要なファイル構造は以下の通りです
```
./
├── api/    fastapiサーバーが使用するカレントディレクトリ
│   ├── main.py    fasatpiの本体です
│   ├── make_doc.py    wordファイルを編集し出力します
│   ├── scraper/    スクレイピング関連
│   │   └── agriculture_scraper.py    スクレイピングの本体です
│   ├── security/    認証関連
│   │   └── authenticate.py    認証機能の本体です
│   └── accessor/    データベース関連
│       └── accessor.py    データベース接続の本体ファイルです
├── wp/    apacheサーバーが使用するカレントディレクトリ
├── tmp/
│   └── results/   make_docの実行結果のwordファイルが置かれます
├── config/
│   ├── dbconfig.json    データベースへの接続時に使用します
│   ├── httpd.conf    apacheサーバーコンフィグファイルです
│   ├── log_config.yaml    fastapiが使用するlogger用コンフィグです
│   ├── my.cnf    mariadbコンフィグファイルです
│   └── secretKey.txt    APIの認証機能で使用する秘密鍵です　1行の平文テキストです
└── server.bash    サーバーを起動、終了するバッチです
```

### 構築
- apacheサーバー、python環境、sqlサーバーの構築が必要です
#### apache
- コンフィグファイル(httpd.conf)の位置は、server.bash:4の apacheConfigFilePath 変数で指定されています
- PHPのバージョンは8.3です
- DocumentRootで./wpディレクトリを指定するようにしてください
- npmパッケージにはjqueryの型補完だけ入れている(しかも使ってない)ため、インストールする必要はありません
#### python
- バージョンは3.12です
- 特にserver.bashからの起動では、venvの使用を想定しています
- 必要なモジュールはrequirements.txtにまとめてあります
```shell
pip install -r requirements.txt
```
- ./api/main.py を実行するとサーバーが起動します
- フォアグラウンドで実行されます
- fastapiが使用するポートは3000です ./api/main.py:28 の PORT 変数で指定されています
#### mariadb
- コンフィグファイル(my.cnf)の位置は、 server.bash:5の mariadbConfigFilePath 変数で指定されています
- 実のところ実行環境ではコンフィグファイルの中身はほぼ空です　プロジェクト別でサーバーを全く別にしたかっただけなので、データベースが混ざらないようなら指定もいらないかも

### 実行
- bashが使用可能な環境であれば、server.bashを使用してサーバーの起動と終了が可能です
- server.bash で呼ばれるソフトウェア
  - tmux
  - awk
  - sed
  - ifconfig
  - curl
  - ps
  - tail
  - grep
- server.bashを利用せずにXAMPPを使用しても、apache用ディレクトリ(wp)を指定すればほぼほぼ動くと思います
- http://127.0.0.1/ webサイト本体です
- http://127.0.0.1:3000/docs/ fsatapiのドキュメントページです


### コンフィグファイルの構造
- db.config
```json
{
    "host": "localhost",
    "user": "#ユーザー名",
    "password": "#パスワード",
    "database": "#データベース名"
}
```
- log_config.yaml
```yaml
version: 1
disable_existing_loggers: false
formatters:
  default:
    format: '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    datefmt: '%Y-%m-%d %H:%M:%S'
handlers:
  console:
    class: logging.StreamHandler
    formatter: default
loggers:
  uvicorn:
    handlers:
    - console
    level: DEBUG
```
secretKey.txt
```
****************************************************************

```
秘密鍵は
```shell
openssl rand -hex 32 > ./secretKey.txt
```
で生成