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
    $email = $conn->real_escape_string($_POST['email']);
    $title = $conn->real_escape_string($_POST['text']);
    $content = $conn->real_escape_string($_POST['content']);

    // SQL文の作成
    $sql = "INSERT INTO contacts (email_adrress, title, content) VALUES ('$email', '$title', '$content')";

    // SQL文の実行
    if ($conn->query($sql) === TRUE) {
        // 成功した場合、送信メッセージを表示
        $success_message = "正常に送信されました。";
    } else {
        // エラーが発生した場合
        $error_message = "エラー: " . $sql . "<br>" . $conn->error;
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
    <h1 class="page-header">問合せフォーム</h1>

    <!-- 成功メッセージを表示 -->
    <?php if (!empty($success_message)) : ?>
      <div class="alert alert-success" role="alert">
        <?php echo $success_message; ?>
      </div>
    <?php elseif (!empty($error_message)) : ?>
      <div class="alert alert-danger" role="alert">
        <?php echo $error_message; ?>
      </div>
    <?php endif; ?>

    <form action="sd5_contact.php" method="post">
      <div class="container">
        <div>メールアドレス:<br><input class="field" type="email" name="email" required /></div>
        <div>タイトル:<br><input class="field" type="text" name="text" required /></div>
        <div>お問い合わせ内容:<br><textarea class="field" name="content" cols="30" rows="5" placeholder="問い合わせ内容を記入してください。" required></textarea></div>
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
