-- Dialect: MySQL | Database: company_office | Table Count: 3

CREATE DATABASE IF NOT EXISTS `company_office`;

DROP TABLE IF EXISTS `company_office`.`buildings`;
CREATE TABLE `company_office`.`buildings` (
    `id` INT,
    `name` TEXT,
    `City` TEXT,
    `Height` INT,
    `Stories` INT,
    `Status` TEXT,
    PRIMARY KEY (`id`)
);

DROP TABLE IF EXISTS `company_office`.`Companies`;
CREATE TABLE `company_office`.`Companies` (
    `id` INT,
    `name` TEXT,
    `Headquarters` TEXT,
    `Industry` TEXT,
    `Sales_billion` REAL,
    `Profits_billion` REAL,
    `Assets_billion` REAL,
    `Market_Value_billion` TEXT,
    PRIMARY KEY (`id`)
);

DROP TABLE IF EXISTS `company_office`.`Office_locations`;
CREATE TABLE `company_office`.`Office_locations` (
    `building_id` INT,
    `company_id` INT,
    `move_in_year` INT,
    PRIMARY KEY (`building_id`, `company_id`),
    FOREIGN KEY (`company_id`) REFERENCES `company_office`.`Companies` (`id`),
    FOREIGN KEY (`building_id`) REFERENCES `company_office`.`buildings` (`id`)
);
