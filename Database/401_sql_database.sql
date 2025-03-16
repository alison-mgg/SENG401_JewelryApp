-- DROP DATABASE IF EXISTS `401_sql_database`;
-- CREATE DATABASE `401_sql_database`;
-- USE 401_sql_database;

-- DROP USER IF EXISTS 'seng401'@'localhost';
-- CREATE USER 'seng401'@'localhost' IDENTIFIED BY 'seng401';
-- GRANT ALL PRIVILEGES ON `401_sql_database`.* TO 'seng401'@'localhost' WITH GRANT OPTION;
-- FLUSH PRIVILEGES;

-- CREATE TABLE users (
--     id INT AUTO_INCREMENT PRIMARY KEY,    
--     username VARCHAR(255) NOT NULL,       
--     email VARCHAR(255) NOT NULL UNIQUE,    
--     password VARCHAR(255) NOT NULL,        -- Ideally, password hashed on server side
--     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP 
-- );

-- Use the new AWS database
USE new-jewelry-dupe-db;

-- Create Users table
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,    
    username VARCHAR(255) NOT NULL,       
    email VARCHAR(255) NOT NULL UNIQUE,    
    password VARCHAR(255) NOT NULL,        -- Ideally, password hashed on server side
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert a test user:
INSERT INTO users (username, email, password) 
VALUES ('a', 'a@a.com', 'a');

-- Create chats table
CREATE TABLE chats (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) REFERENCES users(username),
    img_path TEXT NOT NULL,
    links TEXT NOT NULL,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

