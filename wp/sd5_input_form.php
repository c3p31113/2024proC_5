<?php
// データベース接続設定
$servername = "localhost"; // ホスト名
$username = "probc"; // ユーザー名
$password = "probc"; // パスワード
$dbname = "probc_sd5"; // データベース名

// データベース接続
$conn = new mysqli($servername, $username, $password, $dbname);

// 接続確認
if ($conn->connect_error) {
  die("接続失敗: " . $conn->connect_error);
}

// フォームが送信されたとき
if ($_SERVER["REQUEST_METHOD"] == "POST") {
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
  $sql = "INSERT INTO form (product_categories, 人数) VALUES (?, ?)";

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

  // Pythonスクリプトを実行
  $command = escapeshellcmd("python3 agriculture_scraper.py '$crop_list' $labor");
  $output = shell_exec($command);

  echo "<pre>$output</pre>";
}

// 接続を閉じる
$conn->close();

// 作物のオプションを出力する関数
function renderCropOptions() {
  $crops = [
    "---", "あんぽ柿", "いちご", "いんげん", "きゅうり", "さくらんぼ",
    "さやえんどう", "しいたけ", "春菊", "西洋なし", "ニラ", "花わさび",
    "ピーマン", "ぶどう", "桃", "りんご"
  ];

  foreach ($crops as $crop) {
    echo "<option value=\"$crop\">$crop</option>";
  }
}
?>

<!DOCTYPE html>
<html lang="ja">

<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>書類作成補助システム</title>
  <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
  <link rel="stylesheet" href="css/style.css">
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
          <?php renderCropOptions(); ?>
        </select>
        <input type="number" name="area1" placeholder="面積">
        <span class="unit">a(アール)</span>
      </div>
      <div class="record-container">
        <select name="crop2">
          <?php renderCropOptions(); ?>
        </select>
        <input type="number" name="area2" placeholder="面積">
        <span class="unit">a(アール)</span>
      </div>
      <div class="record-container">
        <select name="crop3">
          <?php renderCropOptions(); ?>
        </select>
        <input type="number" name="area3" placeholder="面積">
        <span class="unit">a(アール)</span>
      </div>
      <div class="record-container">
        <select name="crop4">
          <?php renderCropOptions(); ?>
        </select>
        <input type="number" name="area4" placeholder="面積">
        <span class="unit">a(アール)</span>
      </div>
      <div class="record-container">
        <select name="crop5">
          <?php renderCropOptions(); ?>
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