CREATE DATABASE  IF NOT EXISTS `compfie_knowledge`;
USE `compfie_knowledge`;

DROP TABLE IF EXISTS `tbl_audit_log`;
CREATE TABLE `tbl_audit_log` (
  `audit_trail_id` int(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `tbl_name` varchar(100),
  `tbl_auto_id` int(10),
  `column_name` varchar(100),
  `value` longtext,
  `client_id` int(10),
  `action` varchar(20)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tbl_form_category`;
CREATE TABLE `tbl_form_category` (
  `form_category_id` int(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `form_category` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tbl_form_type`;
CREATE TABLE `tbl_form_type` (
  `form_type_id` int(11) NOT NULL,
  `form_type` varchar(20) NOT NULL,
  PRIMARY KEY (`form_type_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


DROP TABLE IF EXISTS `tbl_forms`;
CREATE TABLE `tbl_forms` (
  `form_id` int(11) NOT NULL,
  `form_category_id` int(11) NOT NULL,
  `form_type_id` int(11) NOT NULL,
  `form_name` varchar(50) NOT NULL,
  `form_url` varchar(50) NOT NULL,
  `form_order` int(11) NOT NULL,
  `parent_menu` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`form_id`),
  CONSTRAINT `fk_tbl_forms_1` FOREIGN KEY (`form_category_id`) REFERENCES `tbl_form_category` (`form_category_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `tbl_forms_ibfk_1` FOREIGN KEY (`form_type_id`) REFERENCES `tbl_form_type` (`form_type_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


DROP TABLE IF EXISTS `tbl_user_groups`;
CREATE TABLE `tbl_user_groups` (
  `user_group_id` int(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `form_category_id` int(11) DEFAULT NULL,
  `user_group_name` varchar(50) NOT NULL,
  `form_ids` varchar(250) NOT NULL,
  `is_active` tinyint(1) DEFAULT '1',
  `created_by` int(11) DEFAULT NULL,
  `created_on` timestamp NULL DEFAULT NULL,
  `updated_by` int(11) DEFAULT NULL,
  `updated_on` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  CONSTRAINT `fk_tbl_user_groups_1` FOREIGN KEY (`form_category_id`) REFERENCES `tbl_form_category` (`form_category_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tbl_admin`;

CREATE TABLE `tbl_admin` (
  `email_id` varchar(100) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL,
  `user_type` tinyint(4),
  `updated_on` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tbl_countries`;
CREATE TABLE `tbl_countries` (
  `country_id` int(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `country_name` varchar(50) NOT NULL,
  `is_active` tinyint(4) DEFAULT '1',
  `created_by` int(11) DEFAULT NULL,
  `created_on` timestamp NULL DEFAULT NULL,
  `updated_by` int(11) DEFAULT NULL,
  `updated_on` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tbl_domains`;
CREATE TABLE `tbl_domains` (
  `domain_id` int(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `domain_name` varchar(50) NOT NULL,
  `is_active` tinyint(4) DEFAULT '1',
  `created_by` int(11) DEFAULT NULL,
  `created_on` timestamp NULL DEFAULT NULL,
  `updated_by` int(11) DEFAULT NULL,
  `updated_on` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tbl_users`;
CREATE TABLE `tbl_users` (
  `user_id` int(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `user_group_id` int(11) NOT NULL,
  `email_id` varchar(100) NOT NULL,
  `password` varchar(50) DEFAULT NULL,
  `employee_name` varchar(50) NOT NULL,
  `employee_code` varchar(50) NOT NULL,
  `contact_no` varchar(20) DEFAULT NULL,
  `address` varchar(250) DEFAULT NULL,
  `designation` varchar(50) DEFAULT NULL,
  `is_active` tinyint(4) DEFAULT '1',
  `created_by` int(11) DEFAULT NULL,
  `created_on` timestamp NULL DEFAULT NULL,
  `updated_by` int(11) DEFAULT NULL,
  `updated_on` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  CONSTRAINT `fk_user_details_user_groups` FOREIGN KEY (`user_group_id`) REFERENCES `tbl_user_groups` (`user_group_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tbl_user_countries`;
CREATE TABLE `tbl_user_countries` (
  `user_id` int(11) NOT NULL,
  `country_id` int(11) NOT NULL,
  PRIMARY KEY (`country_id`,`user_id`),
  CONSTRAINT `fk_tbl_users_countries_user_id` FOREIGN KEY (`user_id`) REFERENCES `tbl_users` (`user_id`),
  CONSTRAINT `fk_tbl_user_countries_countries_id` FOREIGN KEY (`country_id`) REFERENCES `tbl_countries` (`country_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tbl_user_domains`;
CREATE TABLE `tbl_user_domains` (
  `user_id` int(11) NOT NULL,
  `domain_id` int(11) NOT NULL,
  PRIMARY KEY (`domain_id`,`user_id`),
  CONSTRAINT `fk_tbl_user_domains_domains_id` FOREIGN KEY (`domain_id`) REFERENCES `tbl_domains` (`domain_id`),
  CONSTRAINT `fk_tbl_user_domains_user_id` FOREIGN KEY (`user_id`) REFERENCES `tbl_users` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tbl_user_login_history`;
CREATE TABLE `tbl_user_login_history` (
  `user_id` INT(11) NOT NULL,
  `ip` varchar(20) NOT NULL,
  `login_time` DATETIME DEFAULT NULL,
  `login_attempt` int(11) DEFAULT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tbl_session_types`;
CREATE TABLE `tbl_session_types` (
  `session_type_id` int(11) NOT NULL,
  `session_type` varchar(20) NOT NULL,
  PRIMARY KEY (`session_type_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tbl_user_sessions`;
CREATE TABLE `tbl_user_sessions` (
  `session_token` varchar(50) NOT NULL,
  `user_id` int(11) NOT NULL,
  `session_type_id` int(11) DEFAULT NULL,
  `last_accessed_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`session_token`),
  CONSTRAINT `fk_tbl_user_sessions_id_1` FOREIGN KEY (`session_type_id`) REFERENCES `tbl_session_types` (`session_type_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tbl_industries`;
CREATE TABLE `tbl_industries` (
  `industry_id` int(11) NOT NULL AUTO_INCREMENT,
  `industry_name` varchar(50) NOT NULL,
  `country_id` int(11) NOT NULL,
  `domain_id` int(11) NOT NULL,
  `is_active` tinyint(4) DEFAULT '1',
  `created_by` int(11) DEFAULT NULL,
  `created_on` timestamp NULL DEFAULT NULL,
  `updated_by` int(11) DEFAULT NULL,
  `updated_on` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`industry_id`,`country_id`,`domain_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tbl_statutory_natures`;
CREATE TABLE `tbl_statutory_natures` (
  `statutory_nature_id` int(11) NOT NULL AUTO_INCREMENT,
  `statutory_nature_name` varchar(50) NOT NULL,
  `country_id` int(11) NOT NULL,
  `is_active` tinyint(4) DEFAULT '1',
  `created_by` int(11) DEFAULT NULL,
  `created_on` timestamp NULL DEFAULT NULL,
  `updated_by` int(11) DEFAULT NULL,
  `updated_on` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`statutory_nature_id`,`country_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tbl_statutory_levels`;
CREATE TABLE `tbl_statutory_levels` (
  `level_id` int(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `country_id` int(11) NOT NULL,
  `domain_id` int(11) NOT NULL,
  `level_position` int(11) NOT NULL,
  `level_name` varchar(50) NOT NULL,
  `is_active` tinyint(4) DEFAULT '1',
  `created_by` int(11) DEFAULT NULL,
  `created_on` timestamp NULL DEFAULT NULL,
  `updated_by` int(11) DEFAULT NULL,
  `updated_on` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  CONSTRAINT `fk_statutory_levels_countries` FOREIGN KEY (`country_id`) REFERENCES `tbl_countries` (`country_id`),
  CONSTRAINT `fk_statutory_levels_domains` FOREIGN KEY (`domain_id`) REFERENCES `tbl_domains` (`domain_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tbl_geography_levels`;
CREATE TABLE `tbl_geography_levels` (
  `level_id` int(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `country_id` int(11) NOT NULL,
  `level_position` int(11) NOT NULL,
  `level_name` varchar(50) NOT NULL,
  `is_active` tinyint(4) DEFAULT '1',
  `created_by` int(11) DEFAULT NULL,
  `created_on` timestamp NULL DEFAULT NULL,
  `updated_by` int(11) DEFAULT NULL,
  `updated_on` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  CONSTRAINT `fk_geography_levels_countries` FOREIGN KEY (`country_id`) REFERENCES `tbl_countries` (`country_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tbl_geographies`;
CREATE TABLE `tbl_geographies` (
  `geography_id` int(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `geography_name` varchar(50) NOT NULL,
  `level_id` int(11) NOT NULL,
  `parent_ids` varchar(50) DEFAULT NULL,
  `parent_names` longtext DEFAULT NULL,
  `is_active` tinyint(4) DEFAULT '1',
  `created_by` int(11) DEFAULT NULL,
  `created_on` timestamp NULL DEFAULT NULL,
  `updated_by` int(11) DEFAULT NULL,
  `updated_on` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  CONSTRAINT `fk_geographies_geography_levels` FOREIGN KEY (`level_id`) REFERENCES `tbl_geography_levels` (`level_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tbl_statutory_mappings`;
CREATE TABLE `tbl_statutory_mappings` (
  `statutory_mapping_id` int(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `country_id` int(11) NOT NULL,
  `domain_id` int(11) NOT NULL,
  `industry_ids` varchar(50) NOT NULL,
  `statutory_nature_id` int(11) NOT NULL,
  `statutory_ids` varchar(50) DEFAULT NULL,
  `compliance_ids` varchar(50) DEFAULT NULL,
  `geography_ids` varchar(100) NOT NULL,
  `approval_status` tinyint(4) DEFAULT 0,
  `rejected_reason` varchar(500) DEFAULT NULL,
  `is_active` tinyint(4) DEFAULT 1,
  `statutory_mapping` longtext DEFAULT NULL,
  `created_by` int(11) DEFAULT NULL,
  `created_on` timestamp NULL DEFAULT NULL,
  `updated_by` int(11) DEFAULT NULL,
  `updated_on` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  CONSTRAINT `fk_statutory_mappings_countries` FOREIGN KEY (`country_id`) REFERENCES `tbl_countries` (`country_id`),
  CONSTRAINT `fk_statutory_mappings_domains` FOREIGN KEY (`domain_id`) REFERENCES `tbl_domains` (`domain_id`),
  CONSTRAINT `fk_statutory_mappings_statutory_natures` FOREIGN KEY (`statutory_nature_id`) REFERENCES `tbl_statutory_natures` (`statutory_nature_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tbl_statutories`;
CREATE TABLE `tbl_statutories` (
  `statutory_id` int(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `level_id` int(11) NOT NULL,
  `statutory_name` varchar(100) NOT NULL,
  `parent_ids` varchar(50) DEFAULT NULL,
  `parent_names` longtext DEFAULT NULL,
  `statutory_mapping_ids` varchar(50) DEFAULT NULL,
  `created_by` int(11) DEFAULT NULL,
  `created_on` timestamp NULL DEFAULT NULL,
  `updated_by` int(11) DEFAULT NULL,
  `updated_on` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  CONSTRAINT `fk_statutories_statutory_levels` FOREIGN KEY (`level_id`) REFERENCES `tbl_statutory_levels` (`level_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tbl_compliance_frequency`;
CREATE TABLE `tbl_compliance_frequency` (
  `frequency_id` int(11) NOT NULL,
  `frequency` varchar(20) NOT NULL,
  PRIMARY KEY (`frequency_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tbl_compliance_repeat_type`;
CREATE TABLE `tbl_compliance_repeat_type` (
  `repeat_type_id` int(11) NOT NULL,
  `repeat_type` varchar(20) NOT NULL,
  PRIMARY KEY (`repeat_type_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tbl_compliance_duration_type`;
CREATE TABLE `tbl_compliance_duration_type` (
  `duration_type_id` int(11) NOT NULL,
  `duration_type` varchar(20) NOT NULL,
  PRIMARY KEY (`duration_type_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


DROP TABLE IF EXISTS `tbl_compliances`;
CREATE TABLE `tbl_compliances` (
  `compliance_id` int(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `statutory_mapping_id` int(11) NOT NULL,
  `domain_id` int(11) NOT NULL,
  `frequency_id` int(11) NOT NULL,
  `repeats_type_id` int(11) DEFAULT NULL,
  `duration_type_id` int(11) DEFAULT NULL,
  `statutory_provision` varchar(500) NOT NULL,
  `compliance_task` varchar(100) NOT NULL,
  `compliance_description` longtext,
  `document_name` varchar(100) DEFAULT NULL,
  `format_file` longtext,
  `format_file_size` float DEFAULT NULL,
  `penal_consequences` longtext,
  `statutory_dates` longtext,
  `repeats_every` int(11) DEFAULT NULL,
  `duration` int(11) DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT '1',
  `created_by` int(11) DEFAULT NULL,
  `created_on` timestamp DEFAULT '0000-00-00 00:00:00',
  `updated_by` int(11) DEFAULT NULL,
  `updated_on` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  KEY `fk_compliances_statutory_mappings` (`statutory_mapping_id`),
  KEY `fk_compliance_frequency_id` (`frequency_id`),
  CONSTRAINT `fk_compliances_statutory_mappings` FOREIGN KEY (`statutory_mapping_id`) REFERENCES `tbl_statutory_mappings` (`statutory_mapping_id`),
  CONSTRAINT `fk_compliance_frequency_id` FOREIGN KEY (`frequency_id`) REFERENCES `tbl_compliance_frequency` (`frequency_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


DROP TABLE IF EXISTS `tbl_statutories_backup`;
CREATE TABLE `tbl_statutories_backup` (
  `statutory_backup_id` int(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `statutory_mapping_id` int(11) NOT NULL,
  `country_name` varchar(50) NOT NULL,
  `domain_name` varchar(50) NOT NULL,
  `industry_name` longtext NOT NULL,
  `statutory_nature` varchar(50) NOT NULL,
  `statutory_provision` longtext,
  `applicable_location` longtext,
  `created_by` int(11) NOT NULL,
  `created_on` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  CONSTRAINT `fk_statutories_backup` FOREIGN KEY (`statutory_mapping_id`) REFERENCES `tbl_statutory_mappings` (`statutory_mapping_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tbl_compliances_backup`;
CREATE TABLE `tbl_compliances_backup` (
  `statutory_backup_id` int(11) NOT NULL,
  `frequency_id` int(11) NOT NULL,
  `repeats_type_id` int(11) DEFAULT NULL,
  `duration_type_id` int(11) DEFAULT NULL,
  `statutory_provision` varchar(250) NOT NULL,
  `compliance_task` varchar(100) DEFAULT NULL,
  `compliance_description` longtext,
  `document_name` varchar(100) DEFAULT NULL,
  `format_file` varchar(100) DEFAULT NULL,
  `format_file_size` float DEFAULT NULL,
  `penal_consequences` longtext,
  `statutory_dates` longtext,
  `repeats_every` int(11) DEFAULT NULL,
  `duration` int(11) DEFAULT NULL,
  CONSTRAINT `fk_compliances_backup_statutories_backup` FOREIGN KEY (`statutory_backup_id`) REFERENCES `tbl_statutories_backup` (`statutory_backup_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tbl_client_groups`;
CREATE TABLE `tbl_client_groups` (
  `client_id` int(11) NOT NULL AUTO_INCREMENT,
  `group_name` varchar(50) NOT NULL,
  `group_admin` varchar(50) NOT NULL,
  `view_licence` int(11) DEFAULT NULL,
  `approve_status` tinyint(4) DEFAULT '0',
  `remarks` text,
  `created_by` int(11) DEFAULT NULL,
  `created_on` timestamp NULL DEFAULT NULL,
  `updated_by` int(11) DEFAULT NULL,
  `updated_on` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`client_id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tbl_client_countries`;
CREATE TABLE `tbl_client_countries` (
  `client_id` int(11) NOT NULL,
  `country_id` int(11) NOT NULL,
  PRIMARY KEY (`client_id`,`country_id`),
  CONSTRAINT `fk_tbl_client_groups_id` FOREIGN KEY (`client_id`) REFERENCES `tbl_client_groups` (`client_id`),
  CONSTRAINT `fk_tbl_countries_id` FOREIGN KEY (`country_id`) REFERENCES `tbl_countries` (`country_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tbl_client_configurations`;
CREATE TABLE `tbl_client_configurations` (
  `client_config_id` int(11) NOT NULL AUTO_INCREMENT,
  `client_id` int(11) NOT NULL,
  `country_id` int(11) NOT NULL,
  `domain_id` int(11) NOT NULL,
  `period_from` tinyint(2) NOT NULL,
  `period_to` tinyint(2) NOT NULL,
  `updated_on` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `updated_by` int(11) DEFAULT NULL,
  PRIMARY Key (client_config_id, client_id, country_id, domain_id),
  CONSTRAINT `fk_tb_client_id_1` FOREIGN KEY (`client_id`) REFERENCES `tbl_client_groups` (`client_id`),
  CONSTRAINT `fk_tbl_countries_id_1` FOREIGN KEY (`country_id`) REFERENCES `tbl_countries` (`country_id`),
  CONSTRAINT `fk_tbl_domains_id_1` FOREIGN KEY (`domain_id`) REFERENCES `tbl_domains` (`domain_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tbl_business_groups`;
CREATE TABLE `tbl_business_groups` (
  `business_group_id` int(11) NOT NULL AUTO_INCREMENT,
  `client_id` int(11) NOT NULL,
  `country_id` int(11) NOT NULL,
  `business_group_name` varchar(100) NOT NULL,
  `created_by` int(11) NOT NULL,
  `created_on` timestamp NULL DEFAULT NULL,
  `updated_by` int(11) DEFAULT NULL,
  `updated_on` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`business_group_id`),
  KEY `fk_tbl_countries_bg` (`country_id`),
  KEY `fk_tbl_cg_bg` (`client_id`),
  CONSTRAINT `fk_tbl_countries` FOREIGN KEY (`country_id`) REFERENCES `tbl_countries` (`country_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_tbl_cg_bg` FOREIGN KEY (`client_id`) REFERENCES `tbl_client_groups` (`client_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;


DROP TABLE IF EXISTS `tbl_legal_entities`;
CREATE TABLE `tbl_legal_entities` (
  `legal_entity_id` int(11) NOT NULL AUTO_INCREMENT,
  `client_id` int(11) NOT NULL,
  `country_id` int(11) NOT NULL,
  `business_group_id` int(11) DEFAULT NULL,
  `legal_entity_name` varchar(100) DEFAULT NULL,
  `contract_from` date DEFAULT NULL,
  `contract_to` date DEFAULT NULL,
  `logo` varchar(200) DEFAULT NULL,
  `file_space_limit` float DEFAULT '0',
  `total_licence` int(11) DEFAULT '0',
  `sms_subscription` tinyint(4) DEFAULT '0',
  `is_active` tinyint(4) DEFAULT '1',
  `created_by` int(11) DEFAULT NULL,
  `created_on` timestamp NULL DEFAULT NULL,
  `updated_by` int(11) DEFAULT NULL,
  `updated_on` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`legal_entity_id`),
  KEY `fk_tbl_cg_le` (`client_id`),
  KEY `fk_tbl_country` (`country_id`),
  CONSTRAINT `fk_tbl_cg_le` FOREIGN KEY (`client_id`) REFERENCES `tbl_client_groups` (`client_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_tbl_country` FOREIGN KEY (`country_id`) REFERENCES `tbl_countries` (`country_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=38 DEFAULT CHARSET=latin1;


DROP TABLE IF EXISTS `tbl_legal_entity_domain_industry`;
CREATE TABLE `tbl_legal_entity_domain_industry` (
  `client_id` int(11) NOT NULL,
  `legal_entity_id` int(11) NOT NULL,
  `domain_id` int(11) NOT NULL,
  `industry_id` int(11) NOT NULL,
  `no_of_units` int(11) NOT NULL,
  `created_by` int(11) DEFAULT NULL,
  `created_on` timestamp NULL DEFAULT NULL,
  `updated_by` int(11) DEFAULT NULL,
  `updated_on` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`client_id`,`legal_entity_id`,`domain_id`,`industry_id`),
  KEY `fk_tbl_le` (`legal_entity_id`),
  KEY `fk_tbl_domain` (`domain_id`),
  KEY `fk_tbl_industry` (`industry_id`),
  CONSTRAINT `fk_tbl_legal_entity_domain_industry_1` FOREIGN KEY (`legal_entity_id`) REFERENCES `tbl_legal_entities` (`legal_entity_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_tbl_legal_entity_domain_industry_2` FOREIGN KEY (`client_id`) REFERENCES `tbl_client_groups` (`client_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_tbl_legal_entity_domain_industry_4` FOREIGN KEY (`industry_id`) REFERENCES `tbl_industries` (`industry_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


DROP TABLE IF EXISTS `tbl_divisions`;
CREATE TABLE `tbl_divisions` (
  `client_id` int(11) NOT NULL,
  `division_id` int(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `division_name` varchar(100) DEFAULT NULL,
  `legal_entity_id` int(11) DEFAULT NULL,
  `business_group_id` int(11) DEFAULT NULL,
  `created_by` int(11) DEFAULT NULL,
  `created_on` timestamp NULL DEFAULT NULL,
  `updated_by` int(11) DEFAULT NULL,
  `updated_on` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  CONSTRAINT `fk_divisions_business_groups` FOREIGN KEY (`business_group_id`) REFERENCES `tbl_business_groups` (`business_group_id`),
  CONSTRAINT `fk_divisions_legal_entities` FOREIGN KEY (`legal_entity_id`) REFERENCES `tbl_legal_entities` (`legal_entity_id`),
  CONSTRAINT `fk_tbl_cg_div` FOREIGN KEY (`client_id`) REFERENCES `tbl_client_groups` (`client_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tbl_category_master`;
CREATE TABLE `tbl_category_master` (
  `category_id` int(11) NOT NULL AUTO_INCREMENT,
  `client_id` int(11) NOT NULL,
  `business_group_id` int(11) DEFAULT NULL,
  `legal_entity_id` int(11) NOT NULL,
  `division_id` int(11) DEFAULT NULL,
  `category_name` varchar(50) DEFAULT NULL,
  `is_active` tinyint(4) DEFAULT NULL,
  `created_by` int(11) DEFAULT NULL,
  `created_on` timestamp NULL DEFAULT NULL,
  `updated_by` int(11) DEFAULT NULL,
  `updated_on` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`category_id`),
  KEY `fk_client_id` (`client_id`),
  KEY `fk_le_id` (`legal_entity_id`),
  CONSTRAINT `fk_tbl_category_master_2` FOREIGN KEY (`legal_entity_id`) REFERENCES `tbl_legal_entities` (`legal_entity_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_tbl_category_master_1` FOREIGN KEY (`client_id`) REFERENCES `tbl_client_groups` (`client_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


DROP TABLE IF EXISTS `tbl_units`;
CREATE TABLE `tbl_units` (
  `unit_id` int(11) NOT NULL AUTO_INCREMENT,
  `client_id` int(11) NOT NULL,
  `business_group_id` int(11) DEFAULT NULL,
  `legal_entity_id` int(11) NOT NULL,
  `division_id` int(11) DEFAULT NULL,
  `category_id` int(11) NOT NULL,
  `geography_id` int(11) NOT NULL,
  `unit_code` varchar(50) NOT NULL,
  `unit_name` varchar(50) NOT NULL,
  `address` varchar(250) NOT NULL,
  `postal_code` int(11) NOT NULL,
  `is_active` tinyint(4) DEFAULT '1',
  `approve_status` tinyint(4) DEFAULT NULL,
  `remarks` text,
  `created_by` int(11) DEFAULT NULL,
  `created_on` timestamp NULL DEFAULT NULL,
  `updated_by` int(11) DEFAULT NULL,
  `updated_on` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`unit_id`),
  KEY `fk_business_group_id` (`business_group_id`),
  KEY `fk_divisions_id` (`division_id`),
  KEY `fk_legal_entities_id` (`legal_entity_id`),
  KEY `fk_units_geographies` (`geography_id`),
  KEY `fk_tbl_units_1` (`client_id`),
  KEY `fk_units_countries_idx` (`category_id`),
  CONSTRAINT `fk_units_category` FOREIGN KEY (`category_id`) REFERENCES `tbl_category_master` (`category_id`),
  CONSTRAINT `fk_legal_entities_id` FOREIGN KEY (`legal_entity_id`) REFERENCES `tbl_legal_entities` (`legal_entity_id`),
  CONSTRAINT `fk_tbl_units_1` FOREIGN KEY (`client_id`) REFERENCES `tbl_client_groups` (`client_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_units_geographies` FOREIGN KEY (`geography_id`) REFERENCES `tbl_geographies` (`geography_id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=latin1;


DROP TABLE IF EXISTS `tbl_unit_approval_history`;
CREATE TABLE `tbl_unit_approval_history` (
  `unit_id` int(11) NOT NULL,
  `created_by` int(11) DEFAULT NULL,
  `created_on` timestamp NULL DEFAULT NULL,
  `approved_by` int(11) DEFAULT NULL,
  `approved_on` timestamp NULL DEFAULT NULL,
  `approve_status` tinyint(4) DEFAULT NULL,
  `remarks` text,
  PRIMARY KEY (`unit_id`),
  CONSTRAINT `fk_tbl_unit_approval_history_1` FOREIGN KEY (`unit_id`) REFERENCES `tbl_units` (`unit_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tbl_unit_industries`;
CREATE TABLE `tbl_unit_industries` (
  `unit_id` int(11) NOT NULL,
  `domain_id` int(11) NOT NULL,
  `industry_id` int(11) NOT NULL,
  PRIMARY KEY (`unit_id`,`domain_id`,`industry_id`),
  KEY `fk_domain_id` (`domain_id`),
  KEY `fk_industry_id` (`industry_id`),
  CONSTRAINT `fk_tbl_unit_industries_3` FOREIGN KEY (`industry_id`) REFERENCES `tbl_industries` (`industry_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_tbl_unit_industries_1` FOREIGN KEY (`unit_id`) REFERENCES `tbl_units` (`unit_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_tbl_unit_industries_2` FOREIGN KEY (`domain_id`) REFERENCES `tbl_domains` (`domain_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


DROP TABLE IF EXISTS `tbl_client_users`;
CREATE TABLE `tbl_client_users` (
  `client_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `seating_unit_id` int(11) DEFAULT NULL,
  `email_id` varchar(100) NOT NULL,
  `employee_name` varchar(50) NOT NULL,
  `employee_code` varchar(50) DEFAULT NULL,
  `contact_no` varchar(20) DEFAULT NULL,
  `created_on` timestamp NULL DEFAULT NULL,
  `is_admin` tinyint(1) NOT NULL DEFAULT '0',
  `is_primary_admin` tinyint(1) NOT NULL DEFAULT '0',
  `is_active` tinyint(1) NOT NULL,
  KEY `fk_tbl_client_users_cg` (`client_id`),
  CONSTRAINT `fk_tbl_client_users_cg` FOREIGN KEY (`client_id`) REFERENCES `tbl_client_groups` (`client_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;



DROP TABLE IF EXISTS `tbl_statutory_notifications_log`;
CREATE TABLE `tbl_statutory_notifications_log` (
  `statutory_notification_id` int(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `statutory_mapping_id` int(11) NOT NULL,
  `country_name` varchar(50) NOT NULL,
  `domain_name` varchar(50) NOT NULL,
  `industry_name` longtext NOT NULL,
  `statutory_nature` varchar(50) NOT NULL,
  `statutory_provision` longtext,
  `applicable_location` longtext,
  `notification_text` longtext,
  `updated_on` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  CONSTRAINT `fk_statutory_notifications_log_statutory_mapping` FOREIGN KEY (`statutory_mapping_id`) REFERENCES `tbl_statutory_mappings` (`statutory_mapping_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tbl_statutory_notifications_units`;
CREATE TABLE `tbl_statutory_notifications_units` (
  `statutory_notification_unit_id` int(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `statutory_notification_id` int(11) NOT NULL,
  `client_id` int(11) NOT NULL,
  `business_group_id` int(11) NULL DEFAULT NULL,
  `legal_entity_id` int(11) NOT  NULL,
  `division_id` int(11)  NULL DEFAULT NULL,
  `unit_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tbl_activity_log`;
CREATE TABLE `tbl_activity_log` (
  `activity_log_id` int(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `form_id` int(11) NOT NULL,
  `action` varchar(500) NOT NULL,
  `created_on` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tbl_notifications`;
CREATE TABLE `tbl_notifications` (
  `notification_id` int(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `notification_text` longtext DEFAULT NULL,
  `link` varchar(500) DEFAULT NULL,
  `created_on` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


DROP TABLE IF EXISTS `tbl_notifications_status`;
CREATE TABLE `tbl_notifications_status` (
  `notification_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `read_status` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`notification_id`, `user_id`),
  CONSTRAINT `fk_tbl_activity_log_ticker_status_users` FOREIGN KEY (`user_id`) REFERENCES `tbl_users` (`user_id`),
  CONSTRAINT `fk_tbl_notifications_ns` FOREIGN KEY (`notification_id`) REFERENCES `tbl_notifications` (`notification_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


DROP TABLE IF EXISTS `tbl_client_statutories`;
CREATE TABLE `tbl_client_statutories` (
  `client_statutory_id` int(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `client_id` int(11) NOT NULL,
  `geography_id` int(11) NOT NULL,
  `country_id` int(11) NOT NULL,
  `domain_id` int(11) NOT NULL,
  `submission_type` tinyint(4) NOT NULL,
  `unit_id` int(11) NOT NULL,
  `created_by` int(11) NOT NULL,
  `created_on` timestamp NULL DEFAULT NULL,
  `updated_by` int(11) DEFAULT NULL,
  `updated_on` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tbl_client_compliances`;
CREATE TABLE `tbl_client_compliances` (
  `client_compliance_id` int(11) NOT NULL AUTO_INCREMENT,
  `client_statutory_id` int(11) NOT NULL,
  `compliance_id` int(11) NOT NULL,
  `statutory_id` int(11) NOT NULL,
  `statutory_applicable` tinyint(4) DEFAULT NULL,
  `statutory_opted` tinyint(4) DEFAULT NULL,
  `not_applicable_remarks` varchar(500) DEFAULT NULL,
  `compliance_applicable` tinyint(4) DEFAULT NULL,
  `compliance_opted` tinyint(4) DEFAULT NULL,
  `compliance_remarks` varchar(500) DEFAULT NULL,
  `submitted_on` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `created_by` int(11) NOT NULL,
  `created_on` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `updated_by` int(11) DEFAULT NULL,
  `updated_on` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`client_statutory_id`, `compliance_id`),
  UNIQUE KEY `client_compliance_id_UNIQUE` (`client_compliance_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tbl_email_verification`;
CREATE TABLE `tbl_email_verification` (
  `user_id` int(11) NOT NULL,
  `verification_code` varchar(50) NOT NULL,
  PRIMARY KEY (`verification_code`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tbl_mobile_registration`;
CREATE TABLE `tbl_mobile_registration` (
  `registration_key` varchar(50) NOT NULL,
  `device_type_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`registration_key`),
  CONSTRAINT `fk_tbl_session_type_id` FOREIGN KEY (`device_type_id`) REFERENCES `tbl_session_types` (`session_type_id`),
  CONSTRAINT `fk_tbl_user_id` FOREIGN KEY (`user_id`) REFERENCES `tbl_users` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tbl_machines`;
CREATE TABLE `tbl_machines` (
  `machine_id` int(11) NOT NULL AUTO_INCREMENT,
  `machine_name` varchar(50) NOT NULL,
  `ip` varchar(20) NOT NULL,
  `port` int(11) NOT NULL,
  `client_ids` varchar(100) DEFAULT NULL,
  `server_full` tinyint(1) NOT NULL,
  PRIMARY KEY (`machine_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


DROP TABLE IF EXISTS `tbl_client_database`;
CREATE TABLE `tbl_client_database` (
  `client_id` int(11) NOT NULL,
  `machine_id` int(11) NOT NULL,
  `database_ip` varchar(20) NOT NULL,
  `database_port` int(11) NOT NULL,
  `database_username` varchar(50) NOT NULL,
  `database_password` varchar(50) NOT NULL,
  `client_short_name` varchar(20) NOT NULL,
  `database_name` varchar(50) NOT NULL,
  `server_ip` varchar(20) NOT NULL,
  `server_port` int(11) NOT NULL,
  PRIMARY KEY (`client_id`),
  CONSTRAINT `fk_tbl_client_group_id` FOREIGN KEY (`client_id`) REFERENCES `tbl_client_groups` (`client_id`),
  CONSTRAINT `fk_tbl_machines_id` FOREIGN KEY (`machine_id`) REFERENCES `tbl_machines` (`machine_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


DROP TABLE IF EXISTS `tbl_database_server`;
CREATE TABLE `tbl_database_server` (
  `db_server_name` varchar(50) NOT NULL,
  `ip` varchar(20) NOT NULL,
  `port` int(11) NOT NULL,
  `server_username` varchar(50) NOT NULL,
  `server_password` varchar(50) NOT NULL,
  `company_ids` varchar(50) NULL DEFAULT NULL,
  `length` int(11) NOT NULL DEFAULT 0,
  `server_full` tinyint(1) NOT NULL DEFAULT 0,
  PRIMARY KEY (`ip`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tbl_statutory_industry`;
CREATE TABLE `tbl_statutory_industry` (
  `statutory_mapping_id` int(11) NOT NULL,
  `industry_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tbl_statutory_geographies`;
CREATE TABLE `tbl_statutory_geographies` (
  `statutory_mapping_id` int(11) NOT NULL,
  `geography_id` int(11) NOT NULL,
  CONSTRAINT `fk_statutory_geographies_geographies` FOREIGN KEY (`geography_id`) REFERENCES `tbl_geographies` (`geography_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


DROP TABLE IF EXISTS `tbl_statutory_statutories`;
CREATE TABLE `tbl_statutory_statutories` (
  `statutory_mapping_id` int(11) NOT NULL,
  `statutory_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tbl_client_replication_status`;
CREATE TABLE `tbl_client_replication_status` (
  `client_id` int(11) NOT NULL,
  `is_new_data` tinyint(2) DEFAULT '1',
  `is_new_domain` tinyint(2) DEFAULT '0',
  `domain_id` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`client_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tbl_validity_days_settings`;
CREATE TABLE `tbl_validity_days_settings` (
  `validity_days_id` int(11) NOT NULL AUTO_INCREMENT,
  `country_id` int(11) DEFAULT NULL,
  `domain_id` int(11) DEFAULT NULL,
  `days` int(11) DEFAULT NULL,
  `created_by` int(11) DEFAULT NULL,
  `created_on` timestamp NULL DEFAULT NULL,
  `updated_by` int(11) DEFAULT NULL,
  `updated_on` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`validity_days_id`),
  KEY `fk_tbl_validity_days_settings_1_idx` (`country_id`),
  KEY `fk_tbl_validity_days_settings_2_idx` (`domain_id`),
  CONSTRAINT `fk_tbl_validity_days_settings_1` FOREIGN KEY (`country_id`) REFERENCES `tbl_countries` (`country_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_tbl_validity_days_settings_2` FOREIGN KEY (`domain_id`) REFERENCES `tbl_domains` (`domain_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tbl_client_domains`;
CREATE TABLE `tbl_client_domains` (
  `client_id` int(11) NOT NULL,
  `legal_entity_id` int(11) NOT NULL,
  `domain_id` int(11) NOT NULL,
  PRIMARY KEY (`client_id`,`legal_entity_id`,`domain_id`),
  KEY `fk_tbl_domains_client_domains_id` (`domain_id`),
  KEY `fk_tbl_domains_client_legal_entity_id` (`legal_entity_id`),
  CONSTRAINT `fk_tbl_client_domains_1` FOREIGN KEY (`legal_entity_id`) REFERENCES `tbl_legal_entities` (`legal_entity_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_tbl_client_groups_client_domains_id` FOREIGN KEY (`client_id`) REFERENCES `tbl_client_groups` (`client_id`),
  CONSTRAINT `fk_tbl_domains_client_domains_id` FOREIGN KEY (`domain_id`) REFERENCES `tbl_domains` (`domain_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tbl_user_clients`;
CREATE TABLE `tbl_user_clients` (
  `client_id` int(11) NOT NULL,
  `legal_entity_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`client_id`,`user_id`,`legal_entity_id`),
  KEY `fk_tbl_users_id` (`user_id`),
  KEY `fk_tbl_le_id` (`legal_entity_id`),
  CONSTRAINT `fk_tbl_le_id` FOREIGN KEY (`legal_entity_id`) REFERENCES `tbl_legal_entities` (`legal_entity_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_tbl_client_groups_user_clients_id` FOREIGN KEY (`client_id`) REFERENCES `tbl_client_groups` (`client_id`),
  CONSTRAINT `fk_tbl_users_id` FOREIGN KEY (`user_id`) REFERENCES `tbl_users` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;