DROP DATABASE IF EXISTS `JewelryApp`;
CREATE DATABASE `JewelryApp`;
USE JewelryApp;

DROP USER IF EXISTS 'seng401'@'localhost';
CREATE USER 'seng401'@'localhost' IDENTIFIED BY 'seng401';
GRANT ALL PRIVILEGES ON `JewlryApp`.* TO 'seng401'@'localhost' WITH GRANT OPTION;
FLUSH PRIVILEGES;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,    
    username VARCHAR(255) NOT NULL,       
    email VARCHAR(255) NOT NULL UNIQUE,    
    password VARCHAR(255) NOT NULL,        -- Ideally, password hashed on server side
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP 
);
