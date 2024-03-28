-- Dialect: MySQL | Database: local_govt_in_alabama | Table Count: 4

CREATE DATABASE IF NOT EXISTS `local_govt_in_alabama`;

DROP TABLE IF EXISTS `local_govt_in_alabama`.`Services`;
CREATE TABLE `local_govt_in_alabama`.`Services` (
    `Service_ID` INTEGER NOT NULL,
    `Service_Type_Code` CHAR(15) NOT NULL,
    PRIMARY KEY (`Service_ID`)
);

DROP TABLE IF EXISTS `local_govt_in_alabama`.`Participants`;
CREATE TABLE `local_govt_in_alabama`.`Participants` (
    `Participant_ID` INTEGER NOT NULL,
    `Participant_Type_Code` CHAR(15) NOT NULL,
    `Participant_Details` VARCHAR(255),
    PRIMARY KEY (`Participant_ID`)
);

DROP TABLE IF EXISTS `local_govt_in_alabama`.`Events`;
CREATE TABLE `local_govt_in_alabama`.`Events` (
    `Event_ID` INTEGER NOT NULL,
    `Service_ID` INTEGER NOT NULL,
    `Event_Details` VARCHAR(255),
    PRIMARY KEY (`Event_ID`),
    FOREIGN KEY (`Service_ID`) REFERENCES `local_govt_in_alabama`.`Services` (`Service_ID`)
);

DROP TABLE IF EXISTS `local_govt_in_alabama`.`Participants_in_Events`;
CREATE TABLE `local_govt_in_alabama`.`Participants_in_Events` (
    `Event_ID` INTEGER NOT NULL,
    `Participant_ID` INTEGER NOT NULL,
    PRIMARY KEY (`Event_ID`, `Participant_ID`),
    FOREIGN KEY (`Event_ID`) REFERENCES `local_govt_in_alabama`.`Events` (`Event_ID`),
    FOREIGN KEY (`Participant_ID`) REFERENCES `local_govt_in_alabama`.`Participants` (`Participant_ID`)
);
