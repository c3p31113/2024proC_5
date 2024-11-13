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
-- --------------------------------------------------------
--
-- テーブルの構造 `product_categories`
--

CREATE TABLE `product_categories` (
  `ID` int(11) NOT NULL,
  `name` text NOT NULL,
  `summary` text DEFAULT NULL
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_general_ci;
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