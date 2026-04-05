CREATE DATABASE clientdb;

USE clientdb;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50),
    password VARCHAR(255)
);

CREATE TABLE clients (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    mobile VARCHAR(15),
    company VARCHAR(100),
    designation VARCHAR(100),
    address TEXT
);

INSERT INTO users (username, password)
VALUES ('admin', 'admin123');