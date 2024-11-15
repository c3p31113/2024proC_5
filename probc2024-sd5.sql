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
/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */
;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */
;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */
;
/*!40101 SET NAMES utf8mb4 */
;
--
-- データベース: `probc2024-sd5`
--

-- --------------------------------------------------------
--
-- テーブルの構造 `form`
--

CREATE TABLE `form` (
  `ID` int(11) NOT NULL,
  `product_array` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`product_array`)),
  `manpower` int(50) NOT NULL
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_general_ci;
-- --------------------------------------------------------
--
-- テーブルの構造 `products`
--

CREATE TABLE `products` (
  `ID` int(11) NOT NULL,
  `name` text NOT NULL,
  `summary` text DEFAULT NULL,
  `desc` text DEFAULT NULL,
  `product_categories_ID` int(50) NOT NULL,
  `kg_per_1a` int(50) NOT NULL,
  `yen_per_1a` int(50) NOT NULL
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_general_ci;

--
-- テーブルのデータのダンプ `products`
--

INSERT INTO `products` (`ID`, `name`, `summary`, `desc`, `product_categories_ID`, `kg_per_1a`, `yen_per_1a`) VALUES
(1, 'あんぽ柿', '品種は平核無柿、蜂屋柿など', NULL, 1, 78, 240),
(2, 'いちご', '品種はとちおとめ、さちのか、など', NULL, 2, 218, 1190),
(3, 'いんげん', '品種はいちず、鴨川グリーンなど', NULL, 2, 72, 8678),
(4, 'きゅうり', '品種はアンコール10、パイロット2号、南極1号など', NULL, 2, 580, 233),
(5, 'さくらんぼ', '品種は佐藤錦など', NULL, 1, 2835, 40),
(6, 'さやえんどう', '品種は姫みどり、ゆうさやなど', NULL, 2, 43, 1157),
(7, 'しいたけ', NULL, NULL, 3, 822, 928),
(8, '春菊', NULL, NULL, 2, 119, 516),
(9, '西洋なし', '品種はラ・フランス、ル・レクチェ、ゼネラル・レクラークなど', NULL, 1, 157, 373),
(10, 'ニラ', '品種はワンダーグリーン、パワフルグリーンベルトなど', NULL, 2, 168, 546),
(11, '花わさび', NULL, NULL, 2, 0, 0),
(12, 'ピーマン', NULL, NULL, 2, 346, 346),
(13, 'ぶどう', '品種は巨峰、高尾など', NULL, 1, 94, 1062),
(14, '桃', '品種はあかつき、川中島白桃、ゆうぞらなど', NULL, 1, 158, 695),
(15, 'りんご', '品種は王林、ふじなど', NULL, 1, 159, 287);

-- --------------------------------------------------------
--
-- テーブルの構造 `product_categories`
--

CREATE TABLE `product_categories` (
  `ID` int(11) NOT NULL,
  `name` text NOT NULL,
  `summary` text DEFAULT NULL
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_general_ci;

--
-- テーブルのデータのダンプ `product_categories`
--

INSERT INTO `product_categories` (`ID`, `name`, `summary`) VALUES
(1, '果樹類', NULL),
(2, '野菜類', NULL),
(3, 'きのこ類', NULL);
-- --------------------------------------------------------
--
-- テーブルの構造 `contacts`
--

CREATE TABLE `contacts` (
  `ID` int(11) NOT NULL,
  `email_adrress` text NOT NULL,
  `form_id` int(11) DEFAULT NULL,
  `title` text NOT NULL,
  `content` text NOT NULL
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_general_ci;
-- --------------------------------------------------------
--
-- テーブルの構造 `admins`
--

CREATE TABLE `admins` (
  `ID` int(11) NOT NULL,
  `name` text NOT NULL,
  `password` text NOT NULL,
  `last_login_date` datetime DEFAULT NULL
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_general_ci;
--
-- ダンプしたテーブルのインデックス
--

--
-- テーブルのインデックス `form`
--
ALTER TABLE `form`
ADD PRIMARY KEY (`ID`);
--
-- テーブルのインデックス `products`
--
ALTER TABLE `products`
ADD PRIMARY KEY (`ID`);
--
-- テーブルのインデックス `product_categories`
--
ALTER TABLE `product_categories`
ADD PRIMARY KEY (`ID`);
--
-- テーブルのインデックス `contacts`
--
ALTER TABLE `contacts`
ADD PRIMARY KEY (`ID`),
  ADD KEY `form_id` (`form_id`);
--
-- テーブルのインデックス `admins`
--
ALTER TABLE `admins`
ADD PRIMARY KEY (`ID`);
--
-- ダンプしたテーブルの AUTO_INCREMENT
--

--
-- テーブルの AUTO_INCREMENT `form`
--
ALTER TABLE `form`
MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT;
--
-- テーブルの AUTO_INCREMENT `products`
--
ALTER TABLE `products`
MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT;
--
-- テーブルの AUTO_INCREMENT `product_categories`
--
ALTER TABLE `product_categories`
MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT;
--
-- テーブルの AUTO_INCREMENT `contacts`
--
ALTER TABLE `contacts`
MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT;
--
-- テーブルの AUTO_INCREMENT `admins`
--
ALTER TABLE `admins`
MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT;
--
-- ダンプしたテーブルの制約
--

--
-- テーブルの制約 `products`
--
ALTER TABLE `products`
ADD CONSTRAINT `products_ibfk_1` FOREIGN KEY (`product_categories_ID`) REFERENCES `product_categories` (`ID`);
--
-- テーブルの制約 `contacts`
--
ALTER TABLE `contacts`
ADD CONSTRAINT `contacts_ibfk_1` FOREIGN KEY (`form_id`) REFERENCES `form` (`ID`);
COMMIT;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */
;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */
;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */
;