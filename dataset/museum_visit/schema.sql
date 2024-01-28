CREATE DATABASE IF NOT EXISTS `museum_visit`;

drop table if exists `museum_visit`.`museum`;
CREATE TABLE IF NOT EXISTS `museum_visit`.`museum` (
    `Museum_ID` INT,
    `Name` STRING,
    `Num_of_Staff` INT,
    `Open_Year` STRING,
    PRIMARY KEY (`Museum_ID`) DISABLE NOVALIDATE
);

drop table if exists `museum_visit`.`visitor`;
CREATE TABLE IF NOT EXISTS `museum_visit`.`visitor` (
    `ID` INT,
    `Name` STRING,
    `Level_of_membership` INT,
    `Age` INT,
    PRIMARY KEY (`ID`) DISABLE NOVALIDATE
);

drop table if exists `museum_visit`.`visit`;
CREATE TABLE IF NOT EXISTS `museum_visit`.`visit` (
    `Museum_ID` INT,
    `visitor_ID` INT,
    `Num_of_Ticket` INT,
    `Total_spent` DOUBLE,
    PRIMARY KEY (`Museum_ID`, `visitor_ID`) DISABLE NOVALIDATE,
    FOREIGN KEY (`visitor_ID`) REFERENCES `museum_visit`.`visitor` (`ID`) DISABLE NOVALIDATE,
    FOREIGN KEY (`Museum_ID`) REFERENCES `museum_visit`.`museum` (`Museum_ID`) DISABLE NOVALIDATE
);
