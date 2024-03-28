-- Dialect: MySQL | Database: theme_gallery | Table Count: 3

CREATE DATABASE IF NOT EXISTS `theme_gallery`;

DROP TABLE IF EXISTS `theme_gallery`.`artist`;
CREATE TABLE `theme_gallery`.`artist` (
    `Artist_ID` INT,
    `Name` TEXT,
    `Country` TEXT,
    `Year_Join` INT,
    `Age` INT,
    PRIMARY KEY (`Artist_ID`)
);

DROP TABLE IF EXISTS `theme_gallery`.`exhibition`;
CREATE TABLE `theme_gallery`.`exhibition` (
    `Exhibition_ID` INT,
    `Year` INT,
    `Theme` TEXT,
    `Artist_ID` INT,
    `Ticket_Price` REAL,
    PRIMARY KEY (`Exhibition_ID`),
    FOREIGN KEY (`Artist_ID`) REFERENCES `theme_gallery`.`artist` (`Artist_ID`)
);

DROP TABLE IF EXISTS `theme_gallery`.`exhibition_record`;
CREATE TABLE `theme_gallery`.`exhibition_record` (
    `Exhibition_ID` INT,
    `Date` VARCHAR(50),
    `Attendance` INT,
    PRIMARY KEY (`Exhibition_ID`, `Date`),
    FOREIGN KEY (`Exhibition_ID`) REFERENCES `theme_gallery`.`exhibition` (`Exhibition_ID`)
);
