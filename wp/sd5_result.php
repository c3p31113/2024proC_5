
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>スクレイピング結果</title>
    <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <div class="container">
        <h1>スクレイピング結果</h1>
        <table class="table table-bordered">
            <thead>
                <tr>
                    <th>作物リスト</th>
                    <th>人数</th>
                </tr>
            </thead>
            <tbody>
                <?php
                if ($result->num_rows > 0) {
                    // 各行のデータを出力
                    while ($row = $result->fetch_assoc()) {
                        $crop_list = json_decode($row['作物リスト'], true);
                        echo "<tr>";
                        echo "<td>";
                        foreach ($crop_list as $crop) {
                            echo "作物: " . htmlspecialchars($crop['crop']) . ", 面積: " . htmlspecialchars($crop['area']) . "a<br>";
                        }
                        echo "</td>";
                        echo "<td>" . htmlspecialchars($row['人数']) . "人</td>";
                        echo "</tr>";
                    }
                } else {
                    echo "<tr><td colspan='2'>データがありません。</td></tr>";
                }
                ?>
            </tbody>
        </table>
    </div>
    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.9.2/dist/umd/popper.min.js"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
</body>
</html>

<?php
// 接続を閉じる
$conn->close();
?>