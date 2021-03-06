DROP TABLE IF EXISTS `compfie_bulkupload`.`tbl_bulk_statutory_mapping_csv`;
CREATE TABLE `compfie_bulkupload`.`tbl_bulk_statutory_mapping_csv` (
  `csv_id` INT NOT NULL AUTO_INCREMENT,
  `country_id` INT NOT  NULL,
  `domain_id` INT NOT NULL,
  `country_name` varchar(50) NOT NULL,
  `domain_name` varchar(50) not null,
  `csv_name` VARCHAR(500) NOT NULL,
  `uploaded_by` INT NOT NULL,
  `uploaded_on` DATETIME NOT NULL,
  `total_records` INT NOT NULL,
  `total_documents` INT default 0,
  `uploaded_documents` INT default 0,
  `upload_status` TINYINT default 0,
  `approve_status` TINYINT default 0,
  `approved_on` DATETIME NULL,
  `approved_by` INT NULL,
  `rejected_on` DATETIME NULL,
  `rejected_by` INT NULL,
  `rejected_reason` VARCHAR(500) NULL,
  `total_rejected_records` INT default 0,
  `is_fully_rejected` TINYINT NULL,
  `rejected_file_name` VARCHAR(500) NULL,
  `rejected_file_download_count` INT NULL,
  `declined_count` INT DEFAULT NULL,
  `file_download_status` VARCHAR(50) Null,
  PRIMARY KEY (`csv_id`));

DROP TABLE IF EXISTS `compfie_bulkupload`.`tbl_bulk_statutory_mapping`;
CREATE TABLE `compfie_bulkupload`.`tbl_bulk_statutory_mapping` (
  `bulk_statutory_mapping_id` INT NOT NULL AUTO_INCREMENT,
  `csv_id` INT NOT NULL,
  `s_no` INT NOT NULL,
  `organization` text NOT NULL,
  `geography_location` text NOT NULL,
  `statutory_nature` varchar(50) not null,
  `statutory` text NOT NULL,
  `statutory_provision` varchar(500) not null,
  `compliance_task` varchar(100) not null,
  `compliance_document` varchar(100) null,
  `compliance_description` text not null,
  `penal_consequences` text null,
  `reference_link` varchar(500) null,
  `compliance_frequency` varchar(20) not null,
  `statutory_month` text  null,
  `statutory_date` text  null,
  `trigger_before` text  null,
  `repeats_every` INT  null,
  `repeats_type` varchar(20)  null,
  `repeat_by` varchar(5) default null,
  `duration` INT  null,
  `duration_type` varchar(20) null,
  `multiple_input` varchar(5) null,
  `format_file` text null,
  `task_id` VARCHAR(25) not null,
  `task_Type` VARCHAR(150) not null,
  `action` TINYINT null,
  `remarks` varchar(500) null,
  `format_upload_status` TINYINT null,
  `format_file_size` FLOAT DEFAULT '0',
  PRIMARY KEY (`bulk_statutory_mapping_id`),
  CONSTRAINT `fk_csv_id` FOREIGN KEY (`csv_id`) REFERENCES `tbl_bulk_statutory_mapping_csv` (`csv_id`));

DROP TABLE IF EXISTS `compfie_bulkupload`.`tbl_bulk_units_csv`;
CREATE TABLE `compfie_bulkupload`.`tbl_bulk_units_csv` (
  `csv_unit_id` INT NOT NULL AUTO_INCREMENT,
  `client_id` INT NOT NULL,
  `client_group` varchar(50) NOT NULL,
  `csv_name` varchar(100) NOT NULL,
  `uploaded_by` INT NOT NULL,
  `uploaded_on` datetime NOT NULL,
  `total_records` INT NOT NULL,
  `approve_status` tinyINT(4) DEFAULT '0',
  `approved_on` datetime DEFAULT NULL,
  `approved_by` INT DEFAULT NULL,
  `rejected_on` datetime DEFAULT NULL,
  `rejected_by` INT DEFAULT NULL,
  `rejected_reason` VARCHAR(500) NULL,
  `total_rejected_records` INT DEFAULT NULL,
  `is_fully_rejected` tinyINT(4) DEFAULT NULL,
  `rejected_file_name` varchar(500) DEFAULT NULL,
  `rejected_file_download_count` INT DEFAULT NULL,
  `declined_count` INT DEFAULT NULL,
  PRIMARY KEY (`csv_unit_id`));

DROP TABLE IF EXISTS `compfie_bulkupload`.`tbl_bulk_units` ;
CREATE TABLE `compfie_bulkupload`.`tbl_bulk_units` (
  `bulk_unit_id` INT not null AUTO_INCREMENT,
  `csv_unit_id` INT not null,
  `legal_entity` varchar(100) not null,
  `division` varchar(100) not null,
  `category` varchar(100) not null,
  `geography_level` varchar(50) not null,
  `unit_location` text not null,
  `unit_code` varchar(50) not null,
  `unit_name` varchar(50) not null,
  `address` varchar(150) not null,
  `city` varchar(50) not null,
  `state` varchar(50) not null,
  `postalcode` varchar(25) not null,
  `domain` text not null,
  `organization` text not null,
  `action` TINYINT not null,
  `remarks` text null,
PRIMARY KEY (`bulk_unit_id`),
CONSTRAINT `fk_csv_unit_id` FOREIGN KEY (`csv_unit_id`) REFERENCES `tbl_bulk_units_csv` (`csv_unit_id`));

DROP TABLE IF EXISTS `compfie_bulkupload`.`tbl_download_assign_statutory_template`;
CREATE TABLE `compfie_bulkupload`.`tbl_download_assign_statutory_template` (
  `as_id` INT PRIMARY KEY AUTO_INCREMENT not null,
  `client_group` varchar(50) not null,
  `country` varchar(50) not null,
  `legal_entity` varchar(100) not null,
  `domain` text not null,
  `organization` text not null,
  `unit_code` varchar(50) not null,
  `unit_name` varchar(50) not null,
  `unit_location` text not null,
  `perimary_legislation` varchar(100) not null,
  `secondary_legislation` text not null,
  `statutory_provision` varchar(500) not null,
  `compliance_task_name` varchar(100) not null,
  `compliance_document` varchar(50) default null,
  `compliance_description` text not null
);

DROP TABLE IF EXISTS `compfie_bulkupload`.`tbl_bulk_assign_statutory_csv`;
CREATE TABLE `compfie_bulkupload`.`tbl_bulk_assign_statutory_csv` (
  `csv_assign_statutory_id` INT NOT NULL AUTO_INCREMENT,
  `client_id` INT NOT  NULL,
  `legal_entity_id` INT not null,
  `domain_ids` text not null,
  `legal_entity` VARCHAR(100) not null,
  `domain_names` text not null,
  `csv_name` VARCHAR(100) NOT NULL,
  `uploaded_by` INT NOT NULL,
  `uploaded_on` DATETIME NOT NULL,
  `total_records` INT NOT NULL,
  `approve_status` TINYINT default 0,
  `approved_on` DATETIME NULL,
  `approved_by` INT NULL,
  `rejected_on` DATETIME NULL,
  `rejected_by` INT NULL,
  `rejected_reason` VARCHAR(500) NULL,
  `total_rejected_records` INT NULL,
  `is_fully_rejected` TINYINT NULL,
  `rejected_file_name` VARCHAR(500) NULL,
  `rejected_file_download_count` INT NULL,
  `declined_count` INT DEFAULT NULL,
  PRIMARY KEY (`csv_assign_statutory_id`));

DROP TABLE IF EXISTS `compfie_bulkupload`.`tbl_bulk_assign_statutory`;
CREATE TABLE `compfie_bulkupload`.`tbl_bulk_assign_statutory` (
  `bulk_assign_statutory_id` INT not null AUTO_INCREMENT,
  `csv_assign_statutory_id` INT not null,
  `client_group` VARCHAR(50) not null,
  `legal_entity` VARCHAR(100) not null,
  `domain` VARCHAR(50) not null,
  `organization` text not null,
  `unit_code` varchar(50) not null,
  `unit_name` varchar(50) not null,
  `unit_location` text not null,
  `perimary_legislation` VARCHAR(100) not null,
  `secondary_legislation` text null,
  `statutory_provision` VARCHAR(500) not null,
  `compliance_task_name` VARCHAR(200) not null,
  `compliance_description` text not null,
  `statutory_applicable_status` TINYINT not null,
  `statytory_remarks` VARCHAR(500) null,
  `compliance_applicable_status` TINYINT not null,
  `action` TINYINT null,
  `remarks` varchar(500) null,
PRIMARY KEY (`bulk_assign_statutory_id`),
CONSTRAINT `fk_csv_assign_statutory_id`
FOREIGN KEY (`csv_assign_statutory_id`)
REFERENCES `tbl_bulk_assign_statutory_csv` (`csv_assign_statutory_id`));

DROP TABLE IF EXISTS `compfie_bulkupload`.`tbl_bulk_past_data_csv`;
CREATE TABLE `compfie_bulkupload`.`tbl_bulk_past_data_csv` (
  `csv_past_id` INT NOT NULL AUTO_INCREMENT,
  `client_id` INT NOT  NULL,
  `legal_entity_id` INT NOT  NULL,
  `domain_id` INT NOT  NULL,
  `unit_id_id` INT NOT NULL,
  `client_group` varchar(50) NOT NULL,
  `csv_name` VARCHAR(100) NOT NULL,
  `uploaded_by` INT NOT NULL,
  `uploaded_on` DATETIME NOT NULL,
  `total_records` INT NOT NULL,
  `total_documents` INT NOT NULL,
  `uploaded_documents` INT NOT NULL,
  `upload_status` TINYINT default 0,
  `file_download_status` VARCHAR(50) NULL,
  PRIMARY KEY (`csv_past_id`));

DROP TABLE IF EXISTS `compfie_bulkupload`.`tbl_bulk_past_data`;
CREATE TABLE `compfie_bulkupload`.`tbl_bulk_past_data` (
  `bulk_past_data_id` INT not null AUTO_INCREMENT,
  `csv_past_id` INT not null,
  `legal_entity` VARCHAR(100) not null,
  `domain` VARCHAR(50) not null,
  `unit_code` varchar(50) not null,
  `unit_name` varchar(50) not null,
  `perimary_legislation` VARCHAR(100) not null,
  `secondary_legislation` text not null,
  `compliance_task_name` VARCHAR(100) not null,
  `compliance_description` text not null,
  `compliance_frequency` VARCHAR(20) not null,
  `statutory_date` text not null,
  `due_date` DATETIME not null,
  `assignee` VARCHAR(50) not null,
  `completion_date` DATETIME not null,
  `document_name` text not null,
  `document_upload_status` TINYINT null,
  `document_file_size` FLOAT DEFAULT '0',
PRIMARY KEY (`bulk_past_data_id`),
CONSTRAINT `fk_csv_past_id` FOREIGN KEY (`csv_past_id`) REFERENCES `tbl_bulk_past_data_csv` (`csv_past_id`));


ALTER TABLE `compfie_bulkupload`.`tbl_bulk_past_data`
ADD COLUMN `document_upload_status` TINYINT NULL AFTER `document_name`,
ADD COLUMN `document_file_size` FLOAT DEFAULT '0' AFTER `document_upload_status`;



ALTER TABLE `compfie_bulkupload`.`tbl_bulk_past_data_csv`
ADD COLUMN `file_download_status` VARCHAR(50) NULL AFTER `upload_status`;
