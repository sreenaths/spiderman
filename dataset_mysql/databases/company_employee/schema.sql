-- Dialect: MySQL | Database: company_employee | Table Count: 3

CREATE DATABASE IF NOT EXISTS `company_employee`;

DROP TABLE IF EXISTS `company_employee`.`people`;
CREATE TABLE `company_employee`.`people` (
    `People_ID` INT,
    `Age` INT,
    `Name` TEXT,
    `Nationality` TEXT,
    `Graduation_College` TEXT,
    PRIMARY KEY (`People_ID`)
);

DROP TABLE IF EXISTS `company_employee`.`company`;
CREATE TABLE `company_employee`.`company` (
    `Company_ID` INT,
    `Name` TEXT,
    `Headquarters` TEXT,
    `Industry` TEXT,
    `Sales_in_Billion` REAL,
    `Profits_in_Billion` REAL,
    `Assets_in_Billion` REAL,
    `Market_Value_in_Billion` REAL,
    PRIMARY KEY (`Company_ID`)
);

DROP TABLE IF EXISTS `company_employee`.`employment`;
CREATE TABLE `company_employee`.`employment` (
    `Company_ID` INT,
    `People_ID` INT,
    `Year_working` INT,
    PRIMARY KEY (`Company_ID`, `People_ID`),
    FOREIGN KEY (`People_ID`) REFERENCES `company_employee`.`people` (`People_ID`),
    FOREIGN KEY (`Company_ID`) REFERENCES `company_employee`.`company` (`Company_ID`)
);