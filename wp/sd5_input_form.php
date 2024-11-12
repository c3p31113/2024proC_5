<!DOCTYPE html>
<html lang="ja">

<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>書類作成補助システム</title>
  <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
  <style>
    body {
      margin: 0;
      font-family: Arial, sans-serif;
    }

    header,
    footer {
      background-color: #ae5123;
      color: white;
      text-align: center;
      padding: 1rem;
    }

    header {
      position: fixed;
      width: 100%;
      top: 0;
      z-index: 1000;
    }

    header h1 {
      font-size: 2rem;
    }

    .button-container {
      display: flex;
      background-color: #8b4513;
      color: white;
      width: 100%;
      position: fixed;
      top: 4rem;
      z-index: 900;
    }

    .button-box {
      flex: 1;
      text-align: center;
      padding: 1rem 0;
      cursor: pointer;
      font-weight: bold;
      font-size: 1.5rem;
    }

    .button-box:hover {
      background-color: chocolate;
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

    main {
      margin-top: 8rem;
      padding: 1rem;
    }

    .record {
      display: flex;
      align-items: center;
      margin-bottom: 1rem;
    }

    .record label {
      margin-right: 0.5rem;
    }

    .record input,
    .record select {
      margin-right: 1rem;
    }
  </style>
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
    <div class="record">
      <label>作物</label>
      <label>面積</label>
    </div>
    <div class="record">
      <select name="crop1">
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
    </div>
    <div class="record">
      <select name="crop2">
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
    </div>
    <div class="record">
      <select name="crop3">
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
    </div>
    <div class="record">
      <select name="crop4">
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
    </div>
    <div class="record">
      <select name="crop5">
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
    </div>
    <div class="record">
      <label>労働人数:</label>
      <input type="number" name="labor" placeholder="労働人数">
    </div>
  </main>
  <footer>
    <button type="button" class="btn btn-secondary" onclick="location.href='sd5_login.html'">管理者ログイン</button>
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