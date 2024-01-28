CREATE DATABASE IF NOT EXISTS `restaurant_1`;

drop table if exists `restaurant_1`.`Student`;
CREATE TABLE IF NOT EXISTS `restaurant_1`.`Student` (
    `StuID` INT,
    `LName` STRING,
    `Fname` STRING,
    `Age` INT,
    `Sex` STRING,
    `Major` INT,
    `Advisor` INT,
    `city_code` STRING,
    PRIMARY KEY (`StuID`) DISABLE NOVALIDATE
);

drop table if exists `restaurant_1`.`Restaurant_Type`;
CREATE TABLE IF NOT EXISTS `restaurant_1`.`Restaurant_Type` (
    `ResTypeID` INT,
    `ResTypeName` STRING,
    `ResTypeDescription` STRING,
    PRIMARY KEY (`ResTypeID`) DISABLE NOVALIDATE
);

drop table if exists `restaurant_1`.`Restaurant`;
CREATE TABLE IF NOT EXISTS `restaurant_1`.`Restaurant` (
    `ResID` INT,
    `ResName` STRING,
    `Address` STRING,
    `Rating` INT,
    PRIMARY KEY (`ResID`) DISABLE NOVALIDATE
);

drop table if exists `restaurant_1`.`Type_Of_Restaurant`;
CREATE TABLE IF NOT EXISTS `restaurant_1`.`Type_Of_Restaurant` (
    `ResID` INT,
    `ResTypeID` INT,
    FOREIGN KEY (`ResTypeID`) REFERENCES `restaurant_1`.`Restaurant_Type` (`ResTypeID`) DISABLE NOVALIDATE,
    FOREIGN KEY (`ResID`) REFERENCES `restaurant_1`.`Restaurant` (`ResID`) DISABLE NOVALIDATE
);

drop table if exists `restaurant_1`.`Visits_Restaurant`;
CREATE TABLE IF NOT EXISTS `restaurant_1`.`Visits_Restaurant` (
    `StuID` INT,
    `ResID` INT,
    `Time` TIMESTAMP,
    `Spent` DECIMAL,
    FOREIGN KEY (`ResID`) REFERENCES `restaurant_1`.`Restaurant` (`ResID`) DISABLE NOVALIDATE,
    FOREIGN KEY (`StuID`) REFERENCES `restaurant_1`.`Student` (`StuID`) DISABLE NOVALIDATE
);
