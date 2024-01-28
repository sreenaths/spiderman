CREATE DATABASE IF NOT EXISTS `twitter_1`;

drop table if exists `twitter_1`.`user_profiles`;
CREATE TABLE IF NOT EXISTS `twitter_1`.`user_profiles` (
    `uid` INT NOT NULL,
    `name` STRING,
    `email` STRING,
    `partitionid` INT,
    `followers` INT,
    PRIMARY KEY (`uid`) DISABLE NOVALIDATE
);

drop table if exists `twitter_1`.`follows`;
CREATE TABLE IF NOT EXISTS `twitter_1`.`follows` (
    `f1` INT NOT NULL,
    `f2` INT NOT NULL,
    PRIMARY KEY (`f1`, `f2`) DISABLE NOVALIDATE,
    FOREIGN KEY (`f2`) REFERENCES `twitter_1`.`user_profiles` (`uid`) DISABLE NOVALIDATE,
    FOREIGN KEY (`f1`) REFERENCES `twitter_1`.`user_profiles` (`uid`) DISABLE NOVALIDATE
);

drop table if exists `twitter_1`.`tweets`;
CREATE TABLE IF NOT EXISTS `twitter_1`.`tweets` (
    `id` BIGINT NOT NULL,
    `uid` INT NOT NULL,
    `text` CHAR(140) NOT NULL,
    `createdate` TIMESTAMP,
    PRIMARY KEY (`id`) DISABLE NOVALIDATE,
    FOREIGN KEY (`uid`) REFERENCES `twitter_1`.`user_profiles` (`uid`) DISABLE NOVALIDATE
);
