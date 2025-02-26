DROP DATABASE IF EXISTS `JewelryApp`;
CREATE DATABASE `JewelryApp`;
USE JewelryApp;

-- Figure out the drop user stuff
DROP USER IF EXISTS 'seng401'@'localhost';
CREATE USER 'seeng401'@'localhost' IDENTIFIED BY 'seng401';
GRANT ALL PRIVILEGES ON `JewelryApp`.* TO 'seng401'@'localhost' WITH GRANT OPTION;
FLUSH PRIVILEGES;

-- sign up / log in --
CREATE TABLE GENUSER (
	Email VARCHAR(320) NOT NULL,
    Fname VARCHAR(30) NOT NULL,
    Lname VARCHAR(30) NOT NULL,
    PRIMARY KEY (Email)
);

CREATE TABLE RegisteredUser(
    Email   VARCHAR(320) NOT NULL,
    Fname  VARCHAR(30) NOT NULL,
    Lname  VARCHAR(30) NOT NULL,
    RegPassword VARCHAR(320) NOT NULL,
    PRIMARY KEY(Email) 
    -- seprate from gen user email until the table is made, where the genuser table also pulls regUsers
);

-- ------ Tables that will only be created through application use: 

INSERT INTO RegisteredUser(Email, Fname, Lname, RegPassword)  VALUES
('email@email.com', 'Fname', 'Lname', 'password');

-- To test generating user, table will actually only be populated through application use
INSERT INTO GenUser (Email, Fname, Lname) VALUES
('email1', 'First1', 'Last1'),
('email2', 'First2', 'Last2'),
('email3', 'First3', 'Last3'),
('email4', 'First4', 'Last4');
INSERT INTO GenUser( SELECT Email, Fname, Lname FROM RegisteredUser);
