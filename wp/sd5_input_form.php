<?php
// データベース接続設定
$dbconfig = json_decode(file_get_contents("../config/dbconfig.json"), true);
$servername = $dbconfig["host"]; // ホスト名
$username = $dbconfig["user"]; // ユーザー名
$password = $dbconfig["password"]; // パスワード
$dbname = $dbconfig["database"]; // データベース名

// データベース接続
$conn = new mysqli($servername, $username, $password, $dbname);

// 接続確認
if ($conn->connect_error) {
  die("接続失敗: " . $conn->connect_error);
}

// フォームが送信されたとき
if ($_SERVER["REQUEST_METHOD"] == "POST") { //TODO webAPIはfastAPIで処理するので、phpでは書かない
  // フォームデータを取得
  $crop1 = $_POST['crop1'];
  $area1 = $_POST['area1'];
  $crop2 = $_POST['crop2'];
  $area2 = $_POST['area2'];
  $crop3 = $_POST['crop3'];
  $area3 = $_POST['area3'];
  $crop4 = $_POST['crop4'];
  $area4 = $_POST['area4'];
  $crop5 = $_POST['crop5'];
  $area5 = $_POST['area5'];
  $labor = $_POST['labor'];

  // 作物リストをJSON形式で保存
  $crop_list = json_encode([
    ['crop' => $crop1, 'area' => $area1],
    ['crop' => $crop2, 'area' => $area2],
    ['crop' => $crop3, 'area' => $area3],
    ['crop' => $crop4, 'area' => $area4],
    ['crop' => $crop5, 'area' => $area5]
  ]);

  // SQLクエリの準備
  $sql = "INSERT INTO フォーム (作物リスト, 人数) VALUES (?, ?)";

  // プリペアドステートメントを準備
  if ($stmt = $conn->prepare($sql)) {
    // パラメータをバインド
    $stmt->bind_param("si", $crop_list, $labor);

    // クエリを実行
    if ($stmt->execute()) {
      echo "<script>alert('データが保存されました。');</script>";
    } else {
      echo "<script>alert('データ保存に失敗しました。');</script>";
    }

    // ステートメントを閉じる
    $stmt->close();
  } else {
    echo "<script>alert('データベース接続に問題があります。');</script>";
  }
}

// 接続を閉じる
$conn->close();
?>

<!DOCTYPE html>
<html lang="ja">

<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>書類作成補助システム</title>
  <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
  <style>
    /* FIXME ほぼ同じ内容のcssが全ファイルに別々に書かれてる
    同じ内容を複数別の箇所に書いてると問題の温床なので、一つのファイルにまとめてそれを呼び出して欲しい
    */
    body {
      margin: 0;
      font-family: Arial, sans-serif;
    }

    header,
    footer {
      background-color: #ae5123;
      color: white;
      text-align: center;
      padding: 1.5rem;
    }

    header {
      position: fixed;
      width: 100%;
      top: 0;
      z-index: 1000;
    }

    header h1 {
      font-size: 2rem;
      cursor: pointer;
    }

    .button-container {
      display: flex;
      background-color: #8b4513;
      color: white;
      width: 100%;
      position: fixed;
      top: 5rem;
      z-index: 900;
    }

    .button-box {
      flex: 1;
      text-align: center;
      padding: 1.5rem 0;
      cursor: pointer;
      font-weight: bold;
      font-size: 1.5rem;
    }

    .button-box:hover {
      background-color: chocolate;
    }

    .content-container {
      display: flex;
      flex-direction: column;
      align-items: center;
      margin-top: 10rem;
      padding: 1.5rem;
    }

    .record-container {
      width: 100%;
      max-width: 800px;
      margin-bottom: 2rem;
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-wrap: nowrap;
    }

    .record-container label {
      margin-right: 0.5rem;
      width: 20%;
      text-align: center;
      font-size: 1.2rem;
      white-space: nowrap;
    }

    .record-container select,
    .record-container input {
      flex: 1;
      padding: 0.5rem;
      margin-right: 0.5rem;
    }

    .unit {
      font-weight: bold;
      white-space: nowrap;
    }

    .decide-button {
      position: fixed;
      bottom: 90px;
      right: 30px;
    }

    .decide-button button {
      font-size: 1.5rem;
      font-weight: bold;
      color: white;
      background-color: #ae5123;
      border: none;
      padding: 0.75rem 2rem;
      border-radius: 5px;
    }

    .decide-button button:hover {
      background-color: #8b4513;
    }

    .main-labels {
      display: flex;
      justify-content: space-between;
      width: 100%;
      max-width: 800px;
      font-size: 1.5rem;
    }

    footer {
      position: fixed;
      width: 100%;
      bottom: 0;
      display: flex;
      justify-content: flex-end;
      align-items: center;
      height: 60px;
      padding-right: 20px;
    }

    @media (max-width: 768px) {
      header h1 {
        font-size: 1.5rem;
      }

      .button-box {
        font-size: 1.2rem;
        padding: 1rem 0;
      }

      .record-container {
        flex-direction: column;
        align-items: flex-start;
      }

      .record-container label,
      .record-container select,
      .record-container input {
        width: 100%;
        margin-bottom: 0.5rem;
      }

      .decide-button button {
        font-size: 1.2rem;
        padding: 0.5rem 1.5rem;
      }

      footer {
        padding-right: 10px;
        height: 50px;
      }
    }
  </style>
</head>

<body>
  <header>
    <h1 onclick="location.href='sd5_home.html'">書類作成補助システム</h1>
  </header>
  <div class="button-container">
    <div class="button-box" onclick="location.href='sd5_notification.html'">お知らせ</div>
    <div class="button-box" onclick="location.href='sd5_contact.html'">問い合わせ</div>
  </div>
  <div class="content-container">
    <form method="POST">
      <div class="main-labels">
        <label>作物</label>
        <label>面積</label>
      </div>
      <div class="record-container">
        <select name="crop1">
          <!-- FIXME 同じ内容を複数回書いてると問題の温床なので直した方がいい
          このoption群を出力するphp関数を定義してそれを毎回呼び出す方がいいと思う -->
          <option value="---">---</option>
          <option value="あんぽ柿">あんぽ柿</option>
          <option value="いちご">いちご</option>
          <option value="いんげん">いんげん</option>
          <option value="きゅうり">きゅうり</option>
          <option value="さくらんぼ">さくらんぼ</option>
          <option value="さやえんどう">さやえんどう</option>
          <option value="しいたけ">しいたけ</option>
          <option value="春菊">春菊</option>
          <option value="西洋なし">西洋なし</option>
          <option value="ニラ">ニラ</option>
          <option value="花わさび">花わさび</option>
          <option value="ピーマン">ピーマン</option>
          <option value="ぶどう">ぶどう</option>
          <option value="桃">桃</option>
          <option value="りんご">りんご</option>
        </select>
        <input type="number" name="area1" placeholder="面積">
        <span class="unit">a(アール)</span>
      </div>
      <div class="record-container">
        <select name="crop2">
          <option value="---">---</option>
          <option value="あんぽ柿">あんぽ柿</option>
          <option value="いちご">いちご</option>
          <option value="いんげん">いんげん</option>
          <option value="きゅうり">きゅうり</option>
          <option value="さくらんぼ">さくらんぼ</option>
          <option value="さやえんどう">さやえんどう</option>
          <option value="しいたけ">しいたけ</option>
          <option value="春菊">春菊</option>
          <option value="西洋なし">西洋なし</option>
          <option value="ニラ">ニラ</option>
          <option value="花わさび">花わさび</option>
          <option value="ピーマン">ピーマン</option>
          <option value="ぶどう">ぶどう</option>
          <option value="桃">桃</option>
          <option value="りんご">りんご</option>
        </select>
        <input type="number" name="area2" placeholder="面積">
        <span class="unit">a(アール)</span>
      </div>
      <div class="record-container">
        <select name="crop3">
          <option value="---">---</option>
          <option value="あんぽ柿">あんぽ柿</option>
          <option value="いちご">いちご</option>
          <option value="いんげん">いんげん</option>
          <option value="きゅうり">きゅうり</option>
          <option value="さくらんぼ">さくらんぼ</option>
          <option value="さやえんどう">さやえんどう</option>
          <option value="しいたけ">しいたけ</option>
          <option value="春菊">春菊</option>
          <option value="西洋なし">西洋なし</option>
          <option value="ニラ">ニラ</option>
          <option value="花わさび">花わさび</option>
          <option value="ピーマン">ピーマン</option>
          <option value="ぶどう">ぶどう</option>
          <option value="桃">桃</option>
          <option value="りんご">りんご</option>
        </select>
        <input type="number" name="area3" placeholder="面積">
        <span class="unit">a(アール)</span>
      </div>
      <div class="record-container">
        <select name="crop4">
          <option value="---">---</option>
          <option value="あんぽ柿">あんぽ柿</option>
          <option value="いちご">いちご</option>
          <option value="いんげん">いんげん</option>
          <option value="きゅうり">きゅうり</option>
          <option value="さくらんぼ">さくらんぼ</option>
          <option value="さやえんどう">さやえんどう</option>
          <option value="しいたけ">しいたけ</option>
          <option value="春菊">春菊</option>
          <option value="西洋なし">西洋なし</option>
          <option value="ニラ">ニラ</option>
          <option value="花わさび">花わさび</option>
          <option value="ピーマン">ピーマン</option>
          <option value="ぶどう">ぶどう</option>
          <option value="桃">桃</option>
          <option value="りんご">りんご</option>
        </select>
        <input type="number" name="area4" placeholder="面積">
        <span class="unit">a(アール)</span>
      </div>
      <div class="record-container">
        <select name="crop5">
          <option value="---">---</option>
          <option value="あんぽ柿">あんぽ柿</option>
          <option value="いちご">いちご</option>
          <option value="いんげん">いんげん</option>
          <option value="きゅうり">きゅうり</option>
          <option value="さくらんぼ">さくらんぼ</option>
          <option value="さやえんどう">さやえんどう</option>
          <option value="しいたけ">しいたけ</option>
          <option value="春菊">春菊</option>
          <option value="西洋なし">西洋なし</option>
          <option value="ニラ">ニラ</option>
          <option value="花わさび">花わさび</option>
          <option value="ピーマン">ピーマン</option>
          <option value="ぶどう">ぶどう</option>
          <option value="桃">桃</option>
          <option value="りんご">りんご</option>
        </select>
        <input type="number" name="area5" placeholder="面積">
        <span class="unit">a(アール)</span>
      </div>
      <div class="record-container">
        <label for="labor">労働人数:</label>
        <input type="number" name="labor" placeholder="人数">
        <span class="unit">人</span>
      </div>
      <div class="decide-button">
        <button type="submit">決定</button>
      </div>
    </form>
  </div>
  <footer>
    <button type="button" class="btn btn-secondary" onclick="location.href='sd5_login.html'">管理者ログイン</button>
  </footer>
  <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.9.2/dist/umd/popper.min.js"></script>
  <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
</body>

</html>