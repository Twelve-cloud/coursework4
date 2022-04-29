CREATE DATABASE IF NOT EXISTS BrokerBase;
USE BrokerBase;

CREATE TABLE IF NOT EXISTS Account 
(
	ID INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
    AccountLogin 	VARCHAR(50)  CONSTRAINT ch_login    CHECK (AccountLogin REGEXP '^[:alpha:][[:alnum:]_]{4,14}[:alnum:]$') UNIQUE,
    AccountPassword VARCHAR(200) CONSTRAINT ch_password CHECK (AccountPassword REGEXP '^[:print:][[:print:]_]{98,198}[:print:]$'),
    Email 			VARCHAR(50)  CONSTRAINT ch_email    CHECK (Email REGEXP '^[:alpha:][[:alnum:]_]{5,15}[@][:alpha:]{2,10}[\.][:alpha:]{2,3}$') DEFAULT 'myemail@domen.com',
    Rolename		VARCHAR(50)  CONSTRAINT ch_rolename CHECK (Rolename IN ('BROKER', 'USER')) DEFAULT 'USER'
);

CREATE TABLE IF NOT EXISTS Company 
(
	ID INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
    CompanyName VARCHAR(50) CONSTRAINT ch_cname CHECK (CompanyName REGEXP '^[[:alnum:] "]{6,16}$') UNIQUE
);

CREATE TABLE IF NOT EXISTS Service
(
    ServiceName VARCHAR(50) CONSTRAINT ch_sname CHECK (ServiceName REGEXP '^[[:alnum:] "]{6,32}$'),
    ServicePrice DOUBLE(8, 2) NOT NULL,
    CompanyName VARCHAR(50),
    CONSTRAINT fkey_company FOREIGN KEY (CompanyName) REFERENCES Company(CompanyName) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT pkey_service PRIMARY KEY(ServiceName, CompanyName)
);

CREATE TABLE IF NOT EXISTS Request
(
    AccountID INT,
    CompanyName VARCHAR(50),
    Type VARCHAR(50) NOT NULL,
    ServicePrice DOUBLE(8, 2) NOT NULL,
    CONSTRAINT fkey_acc FOREIGN KEY(AccountID) REFERENCES Account(ID) ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT pkey_basket PRIMARY KEY (AccountID, CompanyName)
);

CREATE TABLE IF NOT EXISTS Stock
(
	AccountID INT,
	Symbol VARCHAR(5),
    BuyDate DATETIME DEFAULT NOW(),
    BuyPrice DOUBLE(8, 2) NOT NULL,
    CONSTRAINT fkey_owner FOREIGN KEY(AccountID) REFERENCES Account(ID) ON DELETE RESTRICT ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS DataPoint
(
	AccountID INT,
	x DATETIME DEFAULT NOW(),
    y DOUBLE(8, 2) NOT NULL,
    CONSTRAINT fkey_owner FOREIGN KEY(AccountID) REFERENCES Account(ID) ON DELETE RESTRICT ON UPDATE CASCADE
);
-- -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------