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
    <div class="button-box" onclick="location.href='sd5_contact.php'">問い合わせ</div>
  </div>

  <main>
    <h1 class="page-header">管理者メニュー</h1>
    <form action="#" method="post">
      <div class="container">
      </div>
    </form>
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
