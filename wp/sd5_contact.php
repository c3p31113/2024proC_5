<!DOCTYPE html>
<html lang="ja">

<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>書類作成補助システム</title>
  <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
  <link rel="stylesheet" href="css/style.css">
  <link rel="stylesheet" href="css/login-contact.css">
</head>

<body>
  <header>
    <h1>書類作成補助システム</h1>
  </header>

  <div class="button-container">
    <div class="button-box" onclick="location.href='sd5_notification.html'">お知らせ</div>
    <div class="button-box" onclick="location.href='sd5_contact.php'">問い合わせ</div>
  </div>

  <main>
    <h1 class="page-header">問合せフォーム</h1>
    <form method="post">
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
    <button type="button" class="btn btn-secondary" onclick="location.href='sd5_login.php'">管理者ログイン</button>
  </footer>

</body>

</html>
