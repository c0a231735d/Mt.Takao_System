CREATE DATABASE IF NOT EXISTS main_db;
USE main_db;

-- ユーザ-アカウント用のテーブル
CREATE TABLE IF NOT EXISTS accounts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    state VARCHAR(10) DEFAULT 'passive' -- 無効：”passive”、有効”active”、待機”wait”
);

-- スタンプ用のテーブル
CREATE TABLE IF NOT EXISTS stamps (
    id INT AUTO_INCREMENT PRIMARY KEY,
    route_name VARCHAR(255) NOT NULL,
    qr_code VARCHAR(255) NOT NULL,
    is_peak BOOLEAN DEFAULT FALSE
);

INSERT INTO stamps (route_name, qr_code, is_peak) VALUES ('ルートA', 'QR_CODE_A1', FALSE);
INSERT INTO stamps (route_name, qr_code, is_peak) VALUES ('ルートA', 'QR_CODE_A2', TRUE);
INSERT INTO stamps (route_name, qr_code, is_peak) VALUES ('ルートB', 'QR_CODE_B1', FALSE);
INSERT INTO stamps (route_name, qr_code, is_peak) VALUES ('ルートB', 'QR_CODE_B2', TRUE);

-- 特典用のテーブル
CREATE TABLE IF NOT EXISTS gifts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    store_name VARCHAR(255) NOT NULL,
    item_id INT NOT NULL
);