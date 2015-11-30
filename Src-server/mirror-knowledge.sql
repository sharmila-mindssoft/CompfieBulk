CREATE DATABASE  IF NOT EXISTS `mirror_knowledge`;
USE `mirror_knowledge`;

DROP TABLE IF EXISTS `tbl_forms`;
CREATE TABLE `tbl_forms` (
  `form_id` int(11) NOT NULL,
  `form_name` varchar(50) DEFAULT NULL,
  `form_url` varchar(50) DEFAULT NULL,
  `form_order` varchar(50) DEFAULT NULL,
  `form_type` varchar(20) DEFAULT NULL,
  `category` varchar(20) DEFAULT NULL,
  `admin_form` tinyint(4) DEFAULT NULL,
  `parent_menu` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`form_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tbl_user_groups`;
CREATE TABLE `tbl_user_groups` (
  `user_group_id` int(11) NOT NULL,
  `user_group_name` varchar(50) DEFAULT NULL,
  `form_type` varchar(20) DEFAULT NULL,
  `form_ids` varchar(250) DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT '1',
  `created_by` int(11) DEFAULT NULL,
  `created_on` int(11) Not NULL,
  `updated_by` int(11) DEFAULT NULL,
  `updated_on` int(11) Not NULL ,
  PRIMARY KEY (`user_group_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tbl_users`;
CREATE TABLE `tbl_users` (
  `user_id` int(11) NOT NULL,
  `username` varchar(100) DEFAULT NULL,
  `password` varchar(50) DEFAULT NULL,
  `client_id` int(11) DEFAULT NULL,
  `is_active` tinyint(4) DEFAULT '1',
  `created_by` int(11) DEFAULT NULL,
  `created_on` int(11) Not NULL,
  `updated_by` int(11) DEFAULT NULL,
  `updated_on` int(11) Not NULL ,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tbl_user_details`;
CREATE TABLE `tbl_user_details` (
  `user_id` int(11) NOT NULL,
  `email_id` varchar(100) DEFAULT NULL,
  `user_group_id` int(11) DEFAULT NULL,
  `form_type` varchar(20) DEFAULT NULL,
  `employee_name` varchar(50) DEFAULT NULL,
  `employee_code` varchar(50) DEFAULT NULL,
  `contact_no` varchar(20) DEFAULT NULL,
  `address` varchar(250) DEFAULT NULL,
  `designation` varchar(50) DEFAULT NULL,
  `domain_ids` varchar(50) DEFAULT NULL,
  `country_ids` varchar(50) DEFAULT NULL,
  `client_ids` varchar(50) DEFAULT NULL,
  `created_by` int(11) DEFAULT NULL,
  `created_on` int(11) Not NULL,
  `updated_by` int(11) DEFAULT NULL,
  `updated_on` int(11) Not NULL ,
  PRIMARY KEY (`user_id`),
  CONSTRAINT `fk_user_details_user_groups` FOREIGN KEY (`user_group_id`) REFERENCES `tbl_user_groups` (`user_group_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tbl_user_sessions`;
CREATE TABLE `tbl_user_sessions` (
  `session_id` varchar(50) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `login_time` int(11)  NULL DEFAULT NULL,
  PRIMARY KEY (`session_id`),
  CONSTRAINT `fk_user_sessions_users` FOREIGN KEY (`user_id`) REFERENCES `tbl_users` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tbl_countries`;
CREATE TABLE `tbl_countries` (
  `country_id` int(11) NOT NULL,
  `country_name` varchar(50) DEFAULT NULL,
  `is_active` tinyint(4) DEFAULT '1',
  `created_by` int(11) DEFAULT NULL,
  `created_on` int(11) Not NULL,
  `updated_by` int(11) DEFAULT NULL,
  `updated_on` int(11) Not NULL ,
  PRIMARY KEY (`country_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tbl_domains`;
CREATE TABLE `tbl_domains` (
  `domain_id` int(11) NOT NULL,
  `domain_name` varchar(50) NOT NULL,
  `is_active` tinyint(4) DEFAULT '1',
  `created_by` int(11) DEFAULT NULL,
  `created_on` int(11) Not NULL,
  `updated_by` int(11) DEFAULT NULL,
  `updated_on` int(11) Not NULL ,
  PRIMARY KEY (`domain_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tbl_industries`;
CREATE TABLE `tbl_industries` (
  `industry_id` int(11) NOT NULL,
  `industry_name` varchar(50) DEFAULT NULL,
  `is_active` tinyint(4) DEFAULT '1',
  `created_by` int(11) DEFAULT NULL,
  `created_on` int(11) Not NULL,
  `updated_by` int(11) DEFAULT NULL,
  `updated_on` int(11) Not NULL ,
  PRIMARY KEY (`industry_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tbl_statutory_natures`;
CREATE TABLE `tbl_statutory_natures` (
  `statutory_nature_id` int(11) NOT NULL,
  `statutory_nature_name` varchar(50) DEFAULT NULL,
  `is_active` tinyint(4) DEFAULT '1',
  `created_by` int(11) DEFAULT NULL,
  `created_on` int(11) Not NULL,
  `updated_by` int(11) DEFAULT NULL,
  `updated_on` int(11) Not NULL ,
  PRIMARY KEY (`statutory_nature_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tbl_statutory_levels`;
CREATE TABLE `tbl_statutory_levels` (
  `level_id` int(11) NOT NULL,
  `level_position` int(11) DEFAULT NULL,
  `level_name` varchar(50) DEFAULT NULL,
  `country_id` int(11) DEFAULT NULL,
  `domain_id` int(11) DEFAULT NULL,
  `is_active` tinyint(4) DEFAULT '1',
  `created_by` int(11) DEFAULT NULL,
  `created_on` int(11) Not NULL,
  `updated_by` int(11) DEFAULT NULL,
  `updated_on` int(11) Not NULL ,
  PRIMARY KEY (`level_id`),
  CONSTRAINT `fk_statutory_levels_countries` FOREIGN KEY (`country_id`) REFERENCES `tbl_countries` (`country_id`),
  CONSTRAINT `fk_statutory_levels_domains` FOREIGN KEY (`domain_id`) REFERENCES `tbl_domains` (`domain_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tbl_geography_levels`;
CREATE TABLE `tbl_geography_levels` (
  `level_id` int(11) NOT NULL,
  `level_position` int(11) DEFAULT NULL,
  `level_name` varchar(50) DEFAULT NULL,
  `country_id` int(11) DEFAULT NULL,
  `is_active` tinyint(4) DEFAULT '1',
  `created_by` int(11) DEFAULT NULL,
  `created_on` int(11) Not NULL,
  `updated_by` int(11) DEFAULT NULL,
  `updated_on` int(11) Not NULL ,
  PRIMARY KEY (`level_id`),
  CONSTRAINT `fk_geography_levels_countries` FOREIGN KEY (`country_id`) REFERENCES `tbl_countries` (`country_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tbl_geographies`;
CREATE TABLE `tbl_geographies` (
  `geography_id` int(11) NOT NULL,
  `geography_name` varchar(50) DEFAULT NULL,
  `level_id` int(11) DEFAULT NULL,
  `parent_ids` varchar(50) DEFAULT NULL,
  `is_active` tinyint(4) DEFAULT '1',
  `created_by` int(11) DEFAULT NULL,
  `created_on` int(11) Not NULL,
  `updated_by` int(11) DEFAULT NULL,
  `updated_on` int(11) Not NULL ,
  PRIMARY KEY (`geography_id`),
  KEY `GeographyLevels_idx` (`level_id`),
  CONSTRAINT `fk_geographies_geography_levels` FOREIGN KEY (`level_id`) REFERENCES `tbl_geography_levels` (`level_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tbl_statutory_mappings`;
CREATE TABLE `tbl_statutory_mappings` (
  `statutory_mapping_id` int(11) NOT NULL,
  `country_id` int(11) DEFAULT NULL,
  `domain_id` int(11) DEFAULT NULL,
  `industry_ids` varchar(50) DEFAULT NULL,
  `statutory_nature_id` int(11) DEFAULT NULL,
  `statutory_ids` varchar(50) DEFAULT NULL,
  `compliance_ids` varchar(50) DEFAULT NULL,
  `geography_ids` varchar(100) DEFAULT NULL,
  `approval_status` tinyint(4) DEFAULT '0',
  `is_active` tinyint(4) DEFAULT '1',
  `created_by` int(11) DEFAULT NULL,
  `created_on` int(11) Not NULL,
  `updated_by` int(11) DEFAULT NULL,
  `updated_on` int(11) Not NULL ,
  PRIMARY KEY (`statutory_mapping_id`),
  CONSTRAINT `fk_statutory_mappings_countries` FOREIGN KEY (`country_id`) REFERENCES `tbl_countries` (`country_id`),
  CONSTRAINT `fk_statutory_mappings_domains` FOREIGN KEY (`domain_id`) REFERENCES `tbl_domains` (`domain_id`),
  CONSTRAINT `fk_statutory_mappings_statutory_natures` FOREIGN KEY (`statutory_nature_id`) REFERENCES `tbl_statutory_natures` (`statutory_nature_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tbl_statutories`;
CREATE TABLE `tbl_statutories` (
  `statutory_id` int(11) NOT NULL,
  `statutory_name` varchar(50) DEFAULT NULL,
  `level_id` int(11) DEFAULT NULL,
  `parent_ids` varchar(50) DEFAULT NULL,
  `statutory_mapping_ids` varchar(50) DEFAULT NULL,
  `created_by` int(11) DEFAULT NULL,
  `created_on` int(11) Not NULL,
  `updated_by` int(11) DEFAULT NULL,
  `updated_on` int(11) Not NULL ,
  PRIMARY KEY (`statutory_id`),
  CONSTRAINT `fk_statutories_statutory_levels` FOREIGN KEY (`level_id`) REFERENCES `tbl_statutory_levels` (`level_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tbl_compliances`;
CREATE TABLE `tbl_compliances` (
  `compliance_id` int(11) NOT NULL,
  `statutory_provision` varchar(250) DEFAULT NULL,
  `compliance_task` varchar(100) DEFAULT NULL,
  `compliance_description` longtext,
  `document_name` varchar(100) DEFAULT NULL,
  `format_file` varchar(100) DEFAULT NULL,
  `penal_consequences` longtext,
  `compliance_frequency` varchar(20) DEFAULT NULL,
  `statutory_dates` longtext,
  `repeats_every` int(11) DEFAULT NULL,
  `repeats_type` varchar(20) DEFAULT NULL,
  `duration` int(11) DEFAULT NULL,
  `duration_type` varchar(20) DEFAULT NULL,
  `statutory_mapping_id` int(11) DEFAULT NULL,
  `is_active` tinyint(4) DEFAULT '1',
  `created_by` int(11) DEFAULT NULL,
  `created_on` int(11) Not NULL,
  `updated_by` int(11) DEFAULT NULL,
  `updated_on` int(11) Not NULL ,
  PRIMARY KEY (`compliance_id`),
  CONSTRAINT `fk_compliances_statutory_mappings` FOREIGN KEY (`statutory_mapping_id`) REFERENCES `tbl_statutory_mappings` (`statutory_mapping_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tbl_statutory_geographies`;
CREATE TABLE `tbl_statutory_geographies` (
  `statutory_mapping_id` int(11) NOT NULL,
  `geography_id` int(11) DEFAULT NULL,
  CONSTRAINT `fk_statutory_geographies_geographies` FOREIGN KEY (`geography_id`) REFERENCES `tbl_geographies` (`geography_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tbl_statutories_backup`;
CREATE TABLE `tbl_statutories_backup` (
  `statutory_backup_id` int(11) NOT NULL,
  `country_name` varchar(50) DEFAULT NULL,
  `domain_name` varchar(50) DEFAULT NULL,
  `industry_name` varchar(50) DEFAULT NULL,
  `statutory_nature` varchar(50) DEFAULT NULL,
  `statutory_provision` longtext,
  `applicable_location` longtext,
  PRIMARY KEY (`statutory_backup_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tbl_compliances_backup`;
CREATE TABLE `tbl_compliances_backup` (
  `statutory_backup_id` int(11) NOT NULL,
  `statutory_provision` varchar(250) DEFAULT NULL,
  `compliance_task` varchar(100) DEFAULT NULL,
  `compliance_description` longtext,
  `document_name` varchar(100) DEFAULT NULL,
  `format_file` varchar(100) DEFAULT NULL,
  `penal_consequences` longtext,
  `compliance_frequency` varchar(20) DEFAULT NULL,
  `statutory_dates` longtext,
  `repeats_every` int(11) DEFAULT NULL,
  `repeats_type` varchar(20) DEFAULT NULL,
  `duration` int(11) DEFAULT NULL,
  `duration_type` varchar(20) DEFAULT NULL,
  CONSTRAINT `fk_compliances_backup_statutories_backup` FOREIGN KEY (`statutory_backup_id`) REFERENCES `tbl_statutories_backup` (`statutory_backup_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tbl_client_groups`;
CREATE TABLE `tbl_client_groups` (
  `client_id` int(11) NOT NULL,
  `group_name` varchar(50) DEFAULT NULL,
  `incharge_persons` varchar(50) DEFAULT NULL,
  `is_active` tinyint(4) DEFAULT '1',
  `created_by` int(11) DEFAULT NULL,
  `created_on` int(11) Not NULL,
  `updated_by` int(11) DEFAULT NULL,
  `updated_on` int(11) Not NULL ,
  PRIMARY KEY (`client_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tbl_units`;
CREATE TABLE `tbl_units` (
  `client_id` int(11) NOT NULL,
  `unit_id` int(11) NOT NULL,
  `country_id` int(11) DEFAULT NULL,
  `geography_id` int(11) DEFAULT NULL,
  `unit_code` varchar(50) DEFAULT NULL,
  `unit_name` varchar(50) DEFAULT NULL,
  `industry_id` int(11) DEFAULT NULL,
  `is_active` tinyint(4) DEFAULT '1',
  `created_by` int(11) DEFAULT NULL,
  `created_on` int(11) Not NULL,
  `updated_by` int(11) DEFAULT NULL,
  `updated_on` int(11) Not NULL ,
  PRIMARY KEY (`unit_id`),
  CONSTRAINT `fk_units_client` FOREIGN KEY (`client_id`) REFERENCES `tbl_client_groups` (`client_id`),
  CONSTRAINT `fk_units_countries` FOREIGN KEY (`country_id`) REFERENCES `tbl_countries` (`country_id`),
  CONSTRAINT `fk_units_geographies` FOREIGN KEY (`geography_id`) REFERENCES `tbl_geographies` (`geography_id`),
  CONSTRAINT `fk_units_industries` FOREIGN KEY (`industry_id`) REFERENCES `tbl_industries` (`industry_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tbl_statutory_notifications_log`;
CREATE TABLE `tbl_statutory_notifications_log` (
  `statutory_notification_id` int(11) NOT NULL,
  `statutory_backup_id` int(11) DEFAULT NULL,
  `country_name` varchar(50) DEFAULT NULL,
  `domain_name` varchar(50) DEFAULT NULL,
  `industry_name` varchar(50) DEFAULT NULL,
  `statutory_nature` varchar(50) DEFAULT NULL,
  `statutory_provision` longtext,
  `applicable_location` longtext,
  `notification_text` longtext,
  `updated_on` int(11) Not NULL ,
  PRIMARY KEY (`statutory_notification_id`),
  CONSTRAINT `fk_statutory_notifications_log_statutories_backup` FOREIGN KEY (`statutory_backup_id`) REFERENCES `tbl_statutories_backup` (`statutory_backup_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tbl_statutory_notification_units`;
CREATE TABLE `tbl_statutory_notification_units` (
  `statutory_notification_id` int(11) NOT NULL,
  `client_id` int(11) DEFAULT NULL,
  `business_group_id` int(11) DEFAULT NULL,
  `legal_entity_id` int(11) DEFAULT NULL,
  `division_id` int(11) DEFAULT NULL,
  `unit_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`statutory_notification_id`),
  CONSTRAINT `fk_statutory_notification_units_client_groups` FOREIGN KEY (`client_id`) REFERENCES `tbl_client_groups` (`client_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tbl_statutory_notification_status`;
CREATE TABLE `tbl_statutory_notification_status` (
  `statutory_notification_id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `read_status` tinyint(4) DEFAULT NULL,
  PRIMARY KEY (`statutory_notification_id`),
  CONSTRAINT `fk_statutory_notification_status_log` FOREIGN KEY (`statutory_notification_id`) REFERENCES `tbl_statutory_notifications_log` (`statutory_notification_id`),
  CONSTRAINT `fk_statutory_notification_status_users` FOREIGN KEY (`user_id`) REFERENCES `tbl_users` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tbl_activity_log`;
CREATE TABLE `tbl_activity_log` (
  `activity_log_id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `form_id` int(11) DEFAULT NULL,
  `action` varchar(500) DEFAULT NULL,
  `ticker_text` varchar(500) DEFAULT NULL,
  `ticker_link` varchar(100) DEFAULT NULL,
  `created_on` int(11) Not NULL ,
  PRIMARY KEY (`activity_log_id`),
  CONSTRAINT `fk_activity_log_forms` FOREIGN KEY (`form_id`) REFERENCES `tbl_forms` (`form_id`),
  CONSTRAINT `fk_activity_log_users` FOREIGN KEY (`user_id`) REFERENCES `tbl_users` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tbl_activity_log_ticker_status`;
CREATE TABLE `tbl_activity_log_ticker_status` (
  `activity_log_id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `read_status` tinyint(4) DEFAULT NULL,
  PRIMARY KEY (`activity_log_id`),
  CONSTRAINT `fk_tbl_activity_log_ticker_status` FOREIGN KEY (`activity_log_id`) REFERENCES `tbl_activity_log` (`activity_log_id`),
  CONSTRAINT `fk_tbl_activity_log_ticker_status_users` FOREIGN KEY (`user_id`) REFERENCES `tbl_users` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tbl_client_saved_statutories`;
CREATE TABLE `tbl_client_saved_statutories` (
  `client_id` int(11) NOT NULL,
  `client_saved_statutory_id` int(11) NOT NULL,
  `country_id` int(11) DEFAULT NULL,
  `domain_id` int(11) DEFAULT NULL,
  `unit_ids` varchar(250) DEFAULT NULL,
  `client_compliance_id` int(11) NOT NULL,
  `geography_id` int(11) DEFAULT NULL,
  `created_by` int(11) DEFAULT NULL,
  `created_on` int(11) Not NULL,
  `updated_by` int(11) DEFAULT NULL,
  `updated_on` int(11) Not NULL ,
  PRIMARY KEY (`client_saved_statutory_id`,`client_compliance_id`),
  CONSTRAINT `fk_client_saved_statutories_client_groups` FOREIGN KEY (`client_id`) REFERENCES `tbl_client_groups` (`client_id`),
  CONSTRAINT `fk_client_saved_statutories_countries` FOREIGN KEY (`country_id`) REFERENCES `tbl_countries` (`country_id`),
  CONSTRAINT `fk_client_saved_statutories_domains` FOREIGN KEY (`domain_id`) REFERENCES `tbl_domains` (`domain_id`),
  CONSTRAINT `fk_client_saved_statutories_geographies` FOREIGN KEY (`geography_id`) REFERENCES `tbl_geographies` (`geography_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tbl_client_statutories`;
CREATE TABLE `tbl_client_statutories` (
  `client_id` int(11) NOT NULL,
  `client_statutory_id` int(11) NOT NULL,
  `country_id` int(11) DEFAULT NULL,
  `domain_id` int(11) DEFAULT NULL,
  `unit_id` int(11) DEFAULT NULL,
  `client_compliance_id` int(11) NOT NULL,
  `geography_id` int(11) DEFAULT NULL,
  `created_by` int(11) DEFAULT NULL,
  `created_on` int(11) Not NULL,
  `updated_by` int(11) DEFAULT NULL,
  `updated_on` int(11) Not NULL ,
  PRIMARY KEY (`client_statutory_id`,`client_compliance_id`),
  CONSTRAINT `fk_client_statutories_client_groups` FOREIGN KEY (`client_id`) REFERENCES `tbl_client_groups` (`client_id`),
  CONSTRAINT `fk_client_statutories_countries` FOREIGN KEY (`country_id`) REFERENCES `tbl_countries` (`country_id`),
  CONSTRAINT `fk_client_statutories_domains` FOREIGN KEY (`domain_id`) REFERENCES `tbl_domains` (`domain_id`),
  CONSTRAINT `fk_client_statutories_geographies` FOREIGN KEY (`geography_id`) REFERENCES `tbl_geographies` (`geography_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tbl_client_compliances`;
CREATE TABLE `tbl_client_compliances` (
  `client_compliance_id` int(11) NOT NULL,
  `statutory_id` int(11) DEFAULT NULL,
  `applicable` tinyint(4) DEFAULT NULL,
  `not_applicable_remarks` varchar(250) DEFAULT NULL,
  `compliance_id` int(11) DEFAULT NULL,
  `compliance_applicable` tinyint(4) DEFAULT NULL,
  `compliance_opted` tinyint(4) DEFAULT NULL,
  `compliance_remarks` varchar(250) DEFAULT NULL,
  `created_by` int(11) DEFAULT NULL,
  `created_on` int(11) Not NULL,
  `updated_by` int(11) DEFAULT NULL,
  `updated_on` int(11) Not NULL ,
  CONSTRAINT `fk_client_compliances_statutories` FOREIGN KEY (`statutory_id`) REFERENCES `tbl_statutories` (`statutory_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tbl_email_verification`;
CREATE TABLE IF NOT EXISTS `tbl_email_verification` (
  `user_id` int(11) NOT NULL,
  `verification_code` varchar(50) NOT NULL,
  PRIMARY KEY (`verification_code`),
  CONSTRAINT `fk_users` FOREIGN KEY (`user_id`) REFERENCES `tbl_users` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tbl_mobile_registration`;
CREATE TABLE IF NOT EXISTS `tbl_mobile_registration` (
  `user_id` int(11) NOT NULL,
  `registration_key` varchar(50) NOT NULL,
  PRIMARY KEY (`registration_key`),
  CONSTRAINT `fk_users` FOREIGN KEY (`user_id`) REFERENCES `tbl_users` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
