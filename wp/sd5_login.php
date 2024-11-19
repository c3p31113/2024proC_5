<?php
// データベースの接続設定
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

// 成功メッセージ、エラーメッセージの初期化
$success_message = "";
$error_message = "";

// フォームが送信された場合
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // フォームからのデータを取得
    $id = $conn->real_escape_string($_POST['id']);
    $password = $conn->real_escape_string($_POST['password']);

    // SQL文の作成: IDとパスワードをデータベースで照合
    $sql = "SELECT * FROM admins WHERE name = '$id' AND password = '$password'";

    // SQL文の実行
    $result = $conn->query($sql);

    // 結果が1行だけあればログイン成功
    if ($result->num_rows == 1) {
        // ログイン成功後、test.htmlにリダイレクト
        header("Location: test.html");
        exit();
    } else {
        // ログイン失敗
        $error_message = "ログインができませんでした。IDとパスワードが正しいかどうかお確かめください。";
    }
}

// データベース接続を閉じる
$conn->close();
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
    <h1 class="page-header">管理者ログイン</h1>
    <form action="#" method="post">
      <div class="container">
        <div>ログインID:<br><input class="field" type="text" name="id" /></div>
        <div>パスワード:<br><input class="field" type="password" name="password" /></div>
        <div class="send-button">
          <input class="in-send-button" type="submit" value="ログイン">
        </div>
      </div>
    </form>

    <!-- エラーメッセージの表示 -->
    <?php if (!empty($error_message)): ?>
      <div class="alert alert-danger mt-3" role="alert">
        <?php echo $error_message; ?>
      </div>
    <?php endif; ?>
  </main>

  <footer>
  </footer>

  <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.9.2/dist/umd/popper.min.js"></script>
  <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
  <script>
    document.querySelector('header h1').addEventListener('click', function () {
      window.location.href = 'sd5_home.html';
    });
  </script>
</body>

</html>
