-- Use the new AWS database
USE `new-jewelry-dupe-db`;

-- Create Users table
CREATE TABLE IF NOT EXISTS users (
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
CREATE TABLE IF NOT EXISTS chats (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) REFERENCES users(username),
    img_path TEXT NOT NULL,
    response TEXT NOT NULL,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Drop the local database and user if they exist
DROP DATABASE IF EXISTS `401_sql_database`;
DROP USER IF EXISTS 'seng401'@'localhost';

-- Create the local database and user for local development
CREATE DATABASE `401_sql_database`;
CREATE USER 'seng401'@'localhost' IDENTIFIED BY 'seng401';
GRANT ALL PRIVILEGES ON `401_sql_database`.* TO 'seng401'@'localhost' WITH GRANT OPTION;
FLUSH PRIVILEGES;

-- Use the local database
USE `401_sql_database`;

-- Create Users table for local development
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,    
    username VARCHAR(255) NOT NULL,       
    email VARCHAR(255) NOT NULL UNIQUE,    
    password VARCHAR(255) NOT NULL,        -- Ideally, password hashed on server side
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP 
);

-- Insert a test user for local development
INSERT INTO users (username, email, password) 
VALUES ('a', 'a@a.com', 'a');

-- Create chats table for local development
CREATE TABLE IF NOT EXISTS chats (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) REFERENCES users(username),
    img_path TEXT NOT NULL,
    response TEXT NOT NULL,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

