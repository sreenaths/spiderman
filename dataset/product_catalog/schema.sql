CREATE DATABASE IF NOT EXISTS `product_catalog`;

drop table if exists `product_catalog`.`Attribute_Definitions`;
CREATE TABLE IF NOT EXISTS `product_catalog`.`Attribute_Definitions` (
    `attribute_id` INT,
    `attribute_name` STRING,
    `attribute_data_type` STRING,
    PRIMARY KEY (`attribute_id`) DISABLE NOVALIDATE
);

drop table if exists `product_catalog`.`Catalogs`;
CREATE TABLE IF NOT EXISTS `product_catalog`.`Catalogs` (
    `catalog_id` INT,
    `catalog_name` STRING,
    `catalog_publisher` STRING,
    `date_of_publication` TIMESTAMP,
    `date_of_latest_revision` TIMESTAMP,
    PRIMARY KEY (`catalog_id`) DISABLE NOVALIDATE
);

drop table if exists `product_catalog`.`Catalog_Structure`;
CREATE TABLE IF NOT EXISTS `product_catalog`.`Catalog_Structure` (
    `catalog_level_number` INT,
    `catalog_id` INT NOT NULL,
    `catalog_level_name` STRING,
    PRIMARY KEY (`catalog_level_number`) DISABLE NOVALIDATE,
    FOREIGN KEY (`catalog_id`) REFERENCES `product_catalog`.`Catalogs` (`catalog_id`) DISABLE NOVALIDATE
);

drop table if exists `product_catalog`.`Catalog_Contents`;
CREATE TABLE IF NOT EXISTS `product_catalog`.`Catalog_Contents` (
    `catalog_entry_id` INT,
    `catalog_level_number` INT NOT NULL,
    `parent_entry_id` INT,
    `previous_entry_id` INT,
    `next_entry_id` INT,
    `catalog_entry_name` STRING,
    `product_stock_number` STRING,
    `price_in_dollars` DOUBLE,
    `price_in_euros` DOUBLE,
    `price_in_pounds` DOUBLE,
    `capacity` STRING,
    `length` STRING,
    `height` STRING,
    `width` STRING,
    PRIMARY KEY (`catalog_entry_id`) DISABLE NOVALIDATE,
    FOREIGN KEY (`catalog_level_number`) REFERENCES `product_catalog`.`Catalog_Structure` (`catalog_level_number`) DISABLE NOVALIDATE
);

drop table if exists `product_catalog`.`Catalog_Contents_Additional_Attributes`;
CREATE TABLE IF NOT EXISTS `product_catalog`.`Catalog_Contents_Additional_Attributes` (
    `catalog_entry_id` INT NOT NULL,
    `catalog_level_number` INT NOT NULL,
    `attribute_id` INT NOT NULL,
    `attribute_value` STRING NOT NULL,
    FOREIGN KEY (`catalog_level_number`) REFERENCES `product_catalog`.`Catalog_Structure` (`catalog_level_number`) DISABLE NOVALIDATE,
    FOREIGN KEY (`catalog_entry_id`) REFERENCES `product_catalog`.`Catalog_Contents` (`catalog_entry_id`) DISABLE NOVALIDATE
);
