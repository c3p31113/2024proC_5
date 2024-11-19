<?php
// データベースの接続設定
$servername = "localhost";//ホスト名（毎回変わる)
$username = "probc";//ユーザー名
$password = "probc";//パスワード
$dbname = "probc_sd5";//データベース名

//データベース接続
$conn = new mysqli($servername, $username, $password, $dbname);

//接続確認
if ($conn->connect_error) {
  die("接続失敗: " . $conn->connect_error);
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
  <link rel="stylesheet" href="css/input-contact.css">
</head>

<body>
  <header>
    <h1>書類作成補助システム</h1>
  </header>

  <div class="button-container">
    <div class="button-box" onclick="location.href='sd5_notification.html'">お知らせ</div>
    <div class="button-box" onclick="location.href='sd5_contact.html'">問い合わせ</div>
  </div>

  <main>
    <h1 class="page-header">問合せフォーム</h1>
    <form action="#" method="post">
      <div class="container">
        <div>お名前:<br><input class="field" type="text" name="text" /></div>
        <div>メールアドレス:<br><input class="field" type="email" name="email" /></div>
        <div>お問い合わせ内容:<br><textarea class="field" name="content" cols="30" rows="5"
            placeholder="問い合わせ内容を記入してください。"></textarea></div>
        <div class="send-button">
          <input class="in-send-button" type="submit" value="送信する">
        </div>
      </div>
    </form>
  </main>
  <footer>
    <button type="button" class="btn btn-secondary" onclick="location.href='sd5_login.html'">管理者ログイン</button>
  </footer>
</body>

</html>