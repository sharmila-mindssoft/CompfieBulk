DROP TABLE IF EXISTS `compfie_bulkupload`.`tbl_bulk_statutory_mapping_csv`;
CREATE TABLE `compfie_bulkupload`.`tbl_bulk_statutory_mapping_csv` (
  `csv_id` INT NOT NULL AUTO_INCREMENT,
  `country_id` INT NOT  NULL,
  `domain_id` INT NOT NULL,
  `country_name` varchar(100) NOT NULL,
  `domain_name` varchar(100) not null,
  `csv_name` VARCHAR(100) NOT NULL,
  `uploaded_by` VARCHAR(100) NOT NULL,
  `uploaded_on` DATETIME NOT NULL,
  `total_records` INT NOT NULL,
  `total_documents` INT NOT NULL,
  `uploaded_documents` INT NOT NULL,
  `upload_status` TINYINT default 0,
  `approve_status` TINYINT default 0,
  `approved_on` DATETIME NULL,
  `approved_by` VARCHAR(100) NULL,
  `rejected_on` DATETIME NULL,
  `rejected_by` VARCHAR(100) NULL,
  `rejected_reason` VARCHAR(500) NULL,
  `total_rejected_records` INT default 0,
  `is_fully_rejected` TINYINT NULL,
  `rejected_file_name` VARCHAR(500) NULL,
  `rejected_file_download_count` INT NULL,
  PRIMARY KEY (`csv_id`));

DROP TABLE IF EXISTS `compfie_bulkupload`.`tbl_bulk_statutory_mapping`;
CREATE TABLE `compfie_bulkupload`.`tbl_bulk_statutory_mapping` (
  `bulk_statutory_mapping_id` INT NOT NULL AUTO_INCREMENT,
  `csv_id` INT NOT NULL,
  `s_no` INT NOT NULL,
  `organization` longtext NOT NULL,
  `geography_location` longtext NOT NULL,
  `statutory_nature` varchar(50) not null,
  `statutory` longtext NOT NULL,
  `statutory_provision` varchar(500) not null,
  `compliance_task` varchar(100) not null,
  `compliance_document` varchar(100) null,
  `compliance_description` longtext not null,
  `penal_consequences` longtext null,
  `reference_link` longtext null,
  `compliance_frequency` longtext not null,
  `statutory_month` longtext  null,
  `statutory_date` longtext  null,
  `trigger_before` longtext  null,
  `repeats_every` longtext  null,
  `repeats_type` longtext  null,
  `repeat_by` TINYINT  null,
  `duration` INT  null,
  `duration_type` longtext null,
  `multiple_input` varchar(5) null,
  `format_file` longtext null,
  `action` TINYINT null,
  `remarks` longtext null,
  PRIMARY KEY (`bulk_statutory_mapping_id`));

DROP TABLE IF EXISTS `compfie_bulkupload`.`tbl_bulk_units_csv`;
CREATE TABLE `compfie_bulkupload`.`tbl_bulk_units_csv` (
  `csv_unit_id` INT NOT NULL AUTO_INCREMENT,
  `client_id` INT NOT  NULL,
  `client_group` INT NOT  NULL,
  `csv_name` VARCHAR(100) NOT NULL,
  `uploaded_by` VARCHAR(100) NOT NULL,
  `uploaded_on` DATETIME NOT NULL,
  `total_records` INT NOT NULL,
  `approve_status` TINYINT default 0,
  `approved_on` DATETIME NULL,
  `approved_by` VARCHAR(100) NULL,
  `rejected_on` DATETIME NULL,
  `rejected_by` VARCHAR(100) NULL,
  `total_rejected_records` INT NULL,
  `is_fully_rejected` TINYINT NULL,
  `rejected_file_name` VARCHAR(500) NULL,
  `rejected_file_download_count` INT NULL,
  PRIMARY KEY (`csv_unit_id`));

DROP TABLE IF EXISTS `compfie_bulkupload`.`tbl_bulk_units` ;
CREATE TABLE `compfie_bulkupload`.`tbl_bulk_units` (
  `bulk_unit_id` int not null,
  `csv_unit_id` int not null,
  `legal_entity` longtext not null,
  `division` longtext not null,
  `category` longtext not null,
  `geography_level` longtext not null,
  `unit_location` longtext not null,
  `unit_code` varchar(50) not null,
  `unit_name` varchar(50) not null,
  `address` longtext not null,
  `postalcode` int(11) not null,
  `domain` longtext not null,
  `organization` longtext not null,
  `action` TINYINT not null,
  `remarks` longtext not null,
PRIMARY KEY (`bulk_unit_id`));

DROP TABLE IF EXISTS `compfie_bulkupload`.`tbl_download_assign_statutory_template`;
CREATE TABLE `compfie_bulkupload`.`tbl_download_assign_statutory_template` (
  `as_id` INT PRIMARY KEY AUTO_INCREMENT not null,
  `client_group` longtext not null,
  `legal_entity` longtext not null,
  `domain` longtext not null,
  `organization` longtext not null,
  `unit_code` varchar(50) not null,
  `unit_name` varchar(50) not null,
  `unit_location` longtext not null,
  `perimary_legislation` longtext not null,
  `secondary_legislation` longtext not null,
  `statutory_provision` longtext not null,
  `compliance_task_name` longtext not null,
  `compliance_description` longtext not null
);

DROP TABLE IF EXISTS `compfie_bulkupload`.`tbl_bulk_assign_statutory_csv`;
CREATE TABLE `compfie_bulkupload`.`tbl_bulk_assign_statutory_csv` (
  `csv_assign_statutory_id` INT NOT NULL AUTO_INCREMENT,
  `client_id` INT NOT  NULL,
  `legal_entity_id` int not null,
  `domain_id` int not null,
  `legal_entity` longtext not null,
  `domain` longtext not null,
  `csv_name` VARCHAR(100) NOT NULL,
  `uploaded_by` VARCHAR(100) NOT NULL,
  `uploaded_on` DATETIME NOT NULL,
  `total_records` INT NOT NULL,
  `approve_status` TINYINT default 0,
  `approved_on` DATETIME NULL,
  `approved_by` VARCHAR(100) NULL,
  `rejected_on` DATETIME NULL,
  `rejected_by` VARCHAR(100) NULL,
  `total_rejected_records` INT NULL,
  `is_fully_rejected` TINYINT NULL,
  `rejected_file_name` VARCHAR(500) NULL,
  `rejected_file_download_count` INT NULL,
  PRIMARY KEY (`csv_assign_statutory_id`));

DROP TABLE IF EXISTS `compfie_bulkupload`.`tbl_bulk_assign_statutory`;
CREATE TABLE `compfie_bulkupload`.`tbl_bulk_assign_statutory` (
  `bulk_assign_statutory_id` int not null,
  `csv_assign_statutory_id` int not null,
  `client_group` longtext not null,
  `legal_entity` longtext not null,
  `domain` longtext not null,
  `organization` longtext not null,
  `unit_code` varchar(50) not null,
  `unit_name` varchar(50) not null,
  `unit_location` longtext not null,
  `perimary_legislation` longtext not null,
  `secondary_legislation` longtext not null,
  `statutory_provision` longtext not null,
  `compliance_task_name` longtext not null,
  `compliance_description` longtext not null,
  `statutory_applicable_status` TINYINT not null,
  `statytory_remarks` longtext null,
  `compliance_applicable_status` TINYINT not null,
  `action` TINYINT not null,
  `remarks` longtext not null,
PRIMARY KEY (`bulk_assign_statutory_id`));

DROP TABLE IF EXISTS `compfie_bulkupload`.`tbl_bulk_past_data_csv`;
CREATE TABLE `compfie_bulkupload`.`tbl_bulk_past_data_csv` (
  `csv_past_id` INT NOT NULL AUTO_INCREMENT,
  `client_id` INT NOT  NULL,
  `legal_entity_id` INT NOT  NULL,
  `domain_id` INT NOT  NULL,
  `unit_id_id` INT NOT NULL,
  `client_group` varchar(100) NOT NULL,
  `csv_name` VARCHAR(100) NOT NULL,
  `uploaded_by` VARCHAR(100) NOT NULL,
  `uploaded_on` DATETIME NOT NULL,
  `total_records` INT NOT NULL,
  `total_documents` INT NOT NULL,
  `uploaded_documents` INT NOT NULL,
  `upload_status` TINYINT default 0,
  PRIMARY KEY (`csv_past_id`));


DROP TABLE IF EXISTS `compfie_bulkupload`.`tbl_bulk_past_data`;
CREATE TABLE `compfie_bulkupload`.`tbl_bulk_past_data` (
  `bulk_past_data_id` int not null,
  `csv_past_id` int not null,
  `legal_entity` longtext not null,
  `domain` longtext not null,
  `unit_code` varchar(50) not null,
  `unit_name` varchar(50) not null,
  `perimary_legislation` longtext not null,
  `secondary_legislation` longtext not null,
  `compliance_task_name` longtext not null,
  `compliance_description` longtext not null,
  `compliance_frequency` longtext not null,
  `statutory_date` longtext not null,
  `due_date` DATETIME not null,
  `assignee` longtext not null,
  `completion_date` DATETIME not null,
  `document_name` longtext not null,
PRIMARY KEY (`bulk_past_data_id`));

