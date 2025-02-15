-- 1. 사용자와 데이터베이스 생성
CREATE USER crypto_user WITH PASSWORD 'crypto_password';
CREATE DATABASE crypto_db;
GRANT ALL PRIVILEGES ON DATABASE crypto_db TO crypto_user;

-- 2. crypto_db에 연결하여 테이블 생성을 위한 스크립트
\c crypto_db

-- 3. 테이블 및 인덱스 생성
CREATE TABLE IF NOT EXISTS crypto_prices (
    time TIMESTAMP NOT NULL,
    product_id VARCHAR(15) NOT NULL,
    price DOUBLE PRECISION NOT NULL,
    timestamp TIMESTAMP NOT NULL
);

-- 시계열 데이터 최적화를 위한 인덱스
CREATE INDEX IF NOT EXISTS idx_crypto_prices_time ON crypto_prices(time);
CREATE INDEX IF NOT EXISTS idx_crypto_prices_product ON crypto_prices(product_id); 