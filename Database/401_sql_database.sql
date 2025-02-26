DROP DATABASE IF EXISTS `JewelryApp`;
CREATE DATABASE `JewelryApp`;
USE JewelryApp;

-- Figure out the drop user stuff
DROP USER IF EXISTS 'seng401'@'localhost';
CREATE USER 'seeng401'@'localhost' IDENTIFIED BY 'seng401';
GRANT ALL PRIVILEGES ON `JewelryApp`.* TO 'seng401'@'localhost' WITH GRANT OPTION;
FLUSH PRIVILEGES;

-- sign up / log in --


CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL
    -- password_hash VARCHAR(255) NOT NULL, -- Store hashed passwords
    
);

CREATE TABLE searchHistory(
    id INT AUTO_INCREMENT PRIMARY KEY,
    userId INT NOT NULL,
    imageUrl TEXT NOT NULL, -- Store uploaded image reference
    aiResponse JSON, -- Store AI-generated similar jewelry results
    searchedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (userId) REFERENCES users(id) ON DELETE CASCADE
);

