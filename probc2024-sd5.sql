-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- ホスト: 127.0.0.1
-- 生成日時: 2024-11-02 12:18:16
-- サーバのバージョン： 10.4.32-MariaDB
-- PHP のバージョン: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- データベース: `probc2024-sd5`
--

-- --------------------------------------------------------

--
-- テーブルの構造 `フォーム`
--

CREATE TABLE `フォーム` (
  `ID` int(11) NOT NULL,
  `作物リスト` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`作物リスト`)),
  `人数` int(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- テーブルの構造 `作物`
--

CREATE TABLE `作物` (
  `ID` int(11) NOT NULL,
  `名前` text NOT NULL,
  `概要` text DEFAULT NULL,
  `詳細説明` text DEFAULT NULL,
  `作物カテゴリID` int(50) NOT NULL,
  `1a当たりの収穫量` int(50) NOT NULL,
  `1kg当たりの価格` int(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- テーブルの構造 `作物カテゴリ`
--

CREATE TABLE `作物カテゴリ` (
  `ID` int(11) NOT NULL,
  `カテゴリ名` text NOT NULL,
  `概要` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- テーブルの構造 `問い合わせフォーム`
--

CREATE TABLE `問い合わせフォーム` (
  `ID` int(11) NOT NULL,
  `メールアドレス` text NOT NULL,
  `フォーム内容` int(11) DEFAULT NULL,
  `タイトル` text NOT NULL,
  `内容` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- テーブルの構造 `管理者アカウント`
--

CREATE TABLE `管理者アカウント` (
  `ID` int(11) NOT NULL,
  `ユーザー名` text NOT NULL,
  `パスワード` text NOT NULL,
  `最終ログイン日時` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- ダンプしたテーブルのインデックス
--

--
-- テーブルのインデックス `フォーム`
--
ALTER TABLE `フォーム`
  ADD PRIMARY KEY (`ID`);

--
-- テーブルのインデックス `作物`
--
ALTER TABLE `作物`
  ADD PRIMARY KEY (`ID`);

--
-- テーブルのインデックス `作物カテゴリ`
--
ALTER TABLE `作物カテゴリ`
  ADD PRIMARY KEY (`ID`);

--
-- テーブルのインデックス `問い合わせフォーム`
--
ALTER TABLE `問い合わせフォーム`
  ADD PRIMARY KEY (`ID`),
  ADD KEY `フォーム内容` (`フォーム内容`);

--
-- テーブルのインデックス `管理者アカウント`
--
ALTER TABLE `管理者アカウント`
  ADD PRIMARY KEY (`ID`);

--
-- ダンプしたテーブルの AUTO_INCREMENT
--

--
-- テーブルの AUTO_INCREMENT `フォーム`
--
ALTER TABLE `フォーム`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT;

--
-- テーブルの AUTO_INCREMENT `作物`
--
ALTER TABLE `作物`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT;

--
-- テーブルの AUTO_INCREMENT `作物カテゴリ`
--
ALTER TABLE `作物カテゴリ`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT;

--
-- テーブルの AUTO_INCREMENT `問い合わせフォーム`
--
ALTER TABLE `問い合わせフォーム`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT;

--
-- テーブルの AUTO_INCREMENT `管理者アカウント`
--
ALTER TABLE `管理者アカウント`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT;

--
-- ダンプしたテーブルの制約
--

--
-- テーブルの制約 `作物`
--
ALTER TABLE `作物`
  ADD CONSTRAINT `作物_ibfk_1` FOREIGN KEY (`作物カテゴリID`) REFERENCES `作物カテゴリ` (`ID`);

--
-- テーブルの制約 `問い合わせフォーム`
--
ALTER TABLE `問い合わせフォーム`
  ADD CONSTRAINT `問い合わせフォーム_ibfk_1` FOREIGN KEY (`フォーム内容`) REFERENCES `フォーム` (`ID`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
