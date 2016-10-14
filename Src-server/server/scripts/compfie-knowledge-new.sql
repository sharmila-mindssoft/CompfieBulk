CREATE DATABASE  IF NOT EXISTS `compfie_knowledge_new`;
USE `compfie_knowledge_new`;


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

DROP TABLE IF EXISTS `tbl_activity_log`;
CREATE TABLE `tbl_activity_log` (
  `activity_log_id` int(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `form_id` int(11) NOT NULL,
  `action` varchar(500) NOT NULL,
  `created_on` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tbl_user_category`;
CREATE TABLE `tbl_user_category` (
  `user_category_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_category_name` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`user_category_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tbl_form_category`;
CREATE TABLE `tbl_form_category` (
  `form_id` int(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `category_id_1` tinyint(2) DEFAULT 0,
  `category_id_2` tinyint(2) DEFAULT 0,
  `category_id_3` tinyint(2) DEFAULT 0,
  `category_id_4` tinyint(2) DEFAULT 0,
  `category_id_5` tinyint(2) DEFAULT 0,
  `category_id_6` tinyint(2) DEFAULT 0,
  `category_id_7` tinyint(2) DEFAULT 0,
  `category_id_8` tinyint(2) DEFAULT 0
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
  `form_type_id` int(11) NOT NULL,
  `form_name` varchar(50) NOT NULL,
  `form_url` varchar(50) NOT NULL,
  `form_order` int(11) NOT NULL,
  `parent_menu` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`form_id`),
  CONSTRAINT `tbl_forms_ibfk_1` FOREIGN KEY (`form_type_id`) REFERENCES `tbl_form_type` (`form_type_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tbl_user_groups`;
CREATE TABLE `tbl_user_groups` (
  `user_group_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_category_id` int(11) NOT NULL,
  `user_group_name` varchar(50) NOT NULL,
  `is_active` tinyint(4) DEFAULT '1',
  `created_by` int(11) DEFAULT NULL,
  `created_on` timestamp NULL DEFAULT NULL,
  `updated_by` int(11) DEFAULT NULL,
  `updated_on` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`user_group_id`),
  KEY `fk_tbl_user_category_user_category_id` (`user_category_id`),
  CONSTRAINT `fk_tbl_user_category_user_category_id` FOREIGN KEY (`user_category_id`) REFERENCES `tbl_user_category` (`user_category_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tbl_user_group_forms`;
CREATE TABLE `tbl_user_group_forms` (
  `user_group_id` int(11) NOT NULL AUTO_INCREMENT,
  `form_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`user_group_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tbl_countries`;
CREATE TABLE `tbl_countries` (
  `country_id` int(11) NOT NULL AUTO_INCREMENT,
  `country_name` varchar(50) NOT NULL,
  `is_active` tinyint(4) DEFAULT '1',
  `created_by` int(11) DEFAULT NULL,
  `created_on` timestamp NULL DEFAULT NULL,
  `updated_by` int(11) DEFAULT NULL,
  `updated_on` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`country_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tbl_domains`;
CREATE TABLE `tbl_domains` (
  `domain_id` int(11) NOT NULL AUTO_INCREMENT,
  `country_id` int(11) NOT NULL,
  `domain_name` varchar(50) NOT NULL,
  `is_active` tinyint(4) DEFAULT '1',
  `created_by` int(11) DEFAULT NULL,
  `created_on` timestamp NULL DEFAULT NULL,
  `updated_by` int(11) DEFAULT NULL,
  `updated_on` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`domain_id`),
  KEY `fk_domains_countries` (`country_id`),
  CONSTRAINT `fk_domains_countries` FOREIGN KEY (`country_id`) REFERENCES `tbl_countries` (`country_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


DROP TABLE IF EXISTS `tbl_users`;
CREATE TABLE `tbl_users` (
  `user_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_category_id` int(11) NOT NULL,
  `employee_name` varchar(50) NOT NULL,
  `employee_code` varchar(50) NOT NULL,
  `email_id` varchar(100) NOT NULL,
  `contact_no` varchar(20) DEFAULT NULL,
  `mobile_no` varchar(20) DEFAULT NULL,
  `user_group_id` int(11) NOT NULL,
  `address` varchar(250) DEFAULT NULL,
  `designation` varchar(50) DEFAULT NULL,
  `is_active` tinyint(4) DEFAULT '1',
  `status_changed_on` timestamp NULL DEFAULT NULL,
  `is_disable` tinyint(4) DEFAULT '0',
  `disabled_on` timestamp NULL DEFAULT NULL,
  `created_by` int(11) DEFAULT NULL,
  `created_on` timestamp NULL DEFAULT NULL,
  `updated_by` int(11) DEFAULT NULL,
  `updated_on` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`user_id`),
  KEY `fk_tbl_users_user_group_id` (`user_group_id`),
  CONSTRAINT `fk_tbl_users_user_category_id` FOREIGN KEY (`user_group_id`) REFERENCES `tbl_user_category` (`user_category_id`),
  CONSTRAINT `fk_tbl_users_user_group_id` FOREIGN KEY (`user_group_id`) REFERENCES `tbl_user_groups` (`user_group_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

-- user_login_details
DROP TABLE IF EXISTS `tbl_user_login_details`;
CREATE TABLE `tbl_user_login_details` (
  `user_id` int(11) NOT NULL,
  `user_category_id` int(11) NOT NULL,
  `email_id` varchar(100) NOT NULL,
  `username` varchar(20) DEFAULT NULL,
  `password` varchar(50) DEFAULT NULL,
  `is_active` tinyint(4) DEFAULT '1',
  `created_by` int(11) DEFAULT NULL,
  `created_on` timestamp NULL DEFAULT NULL,
  `updated_by` int(11) DEFAULT NULL,
  `updated_on` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`user_id`)
)ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tbl_user_countries`;
CREATE TABLE `tbl_user_countries` (
  `user_id` int(11) NOT NULL,
  `country_id` int(11) NOT NULL,
  `assigned_by` int(11) DEFAULT NULL,
  `assigned_on` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`country_id`,`user_id`),
  KEY `fk_tbl_users_countries_user_id` (`user_id`),
  CONSTRAINT `fk_tbl_user_countries_countries_id` FOREIGN KEY (`country_id`) REFERENCES `tbl_countries` (`country_id`),
  CONSTRAINT `fk_tbl_users_countries_user_id` FOREIGN KEY (`user_id`) REFERENCES `tbl_users` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


DROP TABLE IF EXISTS `tbl_user_domains`;
CREATE TABLE `tbl_user_domains` (
  `user_id` int(11) NOT NULL,
  `domain_id` int(11) NOT NULL,
  `assigned_by` int(11) DEFAULT NULL,
  `assigned_on` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`domain_id`,`user_id`),
  KEY `fk_tbl_users_domains_user_id` (`user_id`),
  CONSTRAINT `fk_tbl_user_domains_domain_id` FOREIGN KEY (`domain_id`) REFERENCES `tbl_domains` (`domain_id`),
  CONSTRAINT `fk_tbl_users_domains_user_id` FOREIGN KEY (`user_id`) REFERENCES `tbl_users` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tbl_user_login_history`;
CREATE TABLE `tbl_user_login_history` (
  `user_id` int(11) NOT NULL,
  `ip` varchar(20) NOT NULL,
  `login_time` datetime DEFAULT NULL,
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
  KEY `fk_tbl_user_sessions_id_1` (`session_type_id`),
  CONSTRAINT `fk_tbl_user_sessions_id_1` FOREIGN KEY (`session_type_id`) REFERENCES `tbl_session_types` (`session_type_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


DROP TABLE IF EXISTS `tbl_compliance_duration_type`;
CREATE TABLE `tbl_compliance_duration_type` (
  `duration_type_id` int(11) NOT NULL,
  `duration_type` varchar(20) NOT NULL,
  PRIMARY KEY (`duration_type_id`)
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


DROP TABLE IF EXISTS `tbl_approve_status`;
CREATE TABLE `tbl_approve_status` (
  `approve_status_id` int(11) NOT NULL,
  `approve_status` varchar(20) NOT NULL,
  PRIMARY KEY (`approve_status_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tbl_organisation`;
CREATE TABLE `tbl_organisation` (
  `organisation_id` int(11) NOT NULL AUTO_INCREMENT,
  `country_id` int(11) NOT NULL,
  `domain_id` int(11) NOT NULL,
  `organisation_name` varchar(50) NOT NULL,
  `is_active` tinyint(4) DEFAULT '1',
  `created_by` int(11) DEFAULT NULL,
  `created_on` timestamp NULL DEFAULT NULL,
  `updated_by` int(11) DEFAULT NULL,
  `updated_on` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`organisation_id`),
  KEY `fk_tbl_countries_country_id` (`country_id`),
  KEY `fk_tbl_domains_domain_id` (`domain_id`),
  CONSTRAINT `fk_tbl_countries_country_id` FOREIGN KEY (`country_id`) REFERENCES `tbl_countries` (`country_id`),
  CONSTRAINT `fk_tbl_domains_domain_id` FOREIGN KEY (`domain_id`) REFERENCES `tbl_domains` (`domain_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

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
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


DROP TABLE IF EXISTS `tbl_geography_levels`;
CREATE TABLE `tbl_geography_levels` (
  `level_id` int(11) NOT NULL AUTO_INCREMENT,
  `country_id` int(11) NOT NULL,
  `level_position` int(11) NOT NULL,
  `level_name` varchar(50) NOT NULL,
  `is_active` tinyint(4) DEFAULT '1',
  `created_by` int(11) DEFAULT NULL,
  `created_on` timestamp NULL DEFAULT NULL,
  `updated_by` int(11) DEFAULT NULL,
  `updated_on` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`level_id`),
  KEY `fk_geography_levels_countries` (`country_id`),
  CONSTRAINT `fk_geography_levels_countries` FOREIGN KEY (`country_id`) REFERENCES `tbl_countries` (`country_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


DROP TABLE IF EXISTS `tbl_geographies`;
CREATE TABLE `tbl_geographies` (
  `geography_id` int(11) NOT NULL AUTO_INCREMENT,
  `geography_name` varchar(50) NOT NULL,
  `level_id` int(11) NOT NULL,
  `parent_ids` varchar(50) DEFAULT NULL,
  `parent_names` longtext,
  `is_active` tinyint(4) DEFAULT '1',
  `created_by` int(11) DEFAULT NULL,
  `created_on` timestamp NULL DEFAULT NULL,
  `updated_by` int(11) DEFAULT NULL,
  `updated_on` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`geography_id`),
  KEY `fk_geographies_geography_levels` (`level_id`),
  CONSTRAINT `fk_geographies_geography_levels` FOREIGN KEY (`level_id`) REFERENCES `tbl_geography_levels` (`level_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tbl_statutory_levels`;
CREATE TABLE `tbl_statutory_levels` (
  `level_id` int(11) NOT NULL AUTO_INCREMENT,
  `country_id` int(11) NOT NULL,
  `domain_id` int(11) NOT NULL,
  `level_position` int(11) NOT NULL,
  `level_name` varchar(50) NOT NULL,
  `is_active` tinyint(4) DEFAULT '1',
  `created_by` int(11) DEFAULT NULL,
  `created_on` timestamp NULL DEFAULT NULL,
  `updated_by` int(11) DEFAULT NULL,
  `updated_on` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`level_id`),
  KEY `fk_statutory_levels_countries` (`country_id`),
  KEY `fk_statutory_levels_domains` (`domain_id`),
  CONSTRAINT `fk_statutory_levels_countries` FOREIGN KEY (`country_id`) REFERENCES `tbl_countries` (`country_id`),
  CONSTRAINT `fk_statutory_levels_domains` FOREIGN KEY (`domain_id`) REFERENCES `tbl_domains` (`domain_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


DROP TABLE IF EXISTS `tbl_statutories`;
CREATE TABLE `tbl_statutories` (
  `statutory_id` int(11) NOT NULL AUTO_INCREMENT,
  `level_id` int(11) NOT NULL,
  `statutory_name` varchar(100) NOT NULL,
  `parent_ids` varchar(50) DEFAULT NULL,
  `parent_names` longtext,
  `statutory_mapping_ids` varchar(50) DEFAULT NULL,
  `created_by` int(11) DEFAULT NULL,
  `created_on` timestamp NULL DEFAULT NULL,
  `updated_by` int(11) DEFAULT NULL,
  `updated_on` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`statutory_id`),
  KEY `fk_statutories_statutory_levels` (`level_id`),
  CONSTRAINT `fk_statutories_statutory_levels` FOREIGN KEY (`level_id`) REFERENCES `tbl_statutory_levels` (`level_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


DROP TABLE IF EXISTS `tbl_statutory_mappings`;
CREATE TABLE `tbl_statutory_mappings` (
  `statutory_mapping_id` int(11) NOT NULL AUTO_INCREMENT,
  `country_id` int(11) NOT NULL,
  `domain_id` int(11) NOT NULL,
  `statutory_nature_id` int(11) NOT NULL,
  `is_active` tinyint(4) DEFAULT '1',
  `is_approved` tinyint(4) DEFAULT '0',
  `remarks` varchar(500) DEFAULT NULL,
  `created_by` int(11) DEFAULT NULL,
  `created_on` timestamp NULL DEFAULT NULL,
  `updated_by` int(11) DEFAULT NULL,
  `updated_on` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`statutory_mapping_id`),
  KEY `fk_statutory_mappings_countries` (`country_id`),
  KEY `fk_statutory_mappings_domains` (`domain_id`),
  KEY `fk_statutory_mappings_statutory_natures` (`statutory_nature_id`),
  CONSTRAINT `fk_statutory_mappings_countries` FOREIGN KEY (`country_id`) REFERENCES `tbl_countries` (`country_id`),
  CONSTRAINT `fk_statutory_mappings_domains` FOREIGN KEY (`domain_id`) REFERENCES `tbl_domains` (`domain_id`),
  CONSTRAINT `fk_statutory_mappings_statutory_natures` FOREIGN KEY (`statutory_nature_id`) REFERENCES `tbl_statutory_natures` (`statutory_nature_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tbl_compliances`;
CREATE TABLE `tbl_compliances` (
  `compliance_id` int(11) NOT NULL AUTO_INCREMENT,
  `statutory_mapping_id` int(11) NOT NULL,
  `country_id` int(11) NOT NULL,
  `domain_id` int(11) NOT NULL,
  `statutory_provision` varchar(500) NOT NULL,
  `compliance_task` varchar(100) NOT NULL,
  `document_name` varchar(100) DEFAULT NULL,
  `compliance_description` longtext,
  `penal_consequences` longtext,
  `reference_link` varchar(500) DEFAULT NULL,
  `frequency_id` int(11) NOT NULL,
  `statutory_dates` longtext,
  `repeats_type_id` int(11) DEFAULT NULL,
  `duration_type_id` int(11) DEFAULT NULL,
  `repeats_every` int(11) DEFAULT NULL,
  `duration` int(11) DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT '1',
  `status_changed_on` timestamp NULL DEFAULT NULL,
  `is_approved` tinyint(1) DEFAULT '0',
  `approved_by` int(11) DEFAULT NULL,
  `approved_on` timestamp NULL DEFAULT NULL,
  `remarks` varchar(500) DEFAULT NULL,
  `format_file` longtext,
  `format_file_size` float DEFAULT NULL,
  `created_by` int(11) DEFAULT NULL,
  `created_on` timestamp NULL DEFAULT NULL,
  `updated_by` int(11) DEFAULT NULL,
  `updated_on` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`compliance_id`),
  KEY `fk_compliances_statutory_mappings` (`statutory_mapping_id`),
  KEY `fk_compliance_frequency_id` (`frequency_id`),
  CONSTRAINT `fk_compliance_frequency_id` FOREIGN KEY (`frequency_id`) REFERENCES `tbl_compliance_frequency` (`frequency_id`),
  CONSTRAINT `fk_compliances_statutory_mappings` FOREIGN KEY (`statutory_mapping_id`) REFERENCES `tbl_statutory_mappings` (`statutory_mapping_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tbl_mapped_industries`;
CREATE TABLE `tbl_mapped_industries` (
  `statutory_mapping_id` int(11) NOT NULL,
  `organisation_id` int(11) NOT NULL,
  `assigned_by` int(11) DEFAULT NULL,
  `assigned_on` timestamp NULL DEFAULT NULL,
  KEY `fk_tbl_mapped_industries_statutory_mapping_id` (`statutory_mapping_id`),
  KEY `fk_tbl_mapped_industries_organisation_id` (`organisation_id`),
  CONSTRAINT `fk_tbl_mapped_industries_organisation_id` FOREIGN KEY (`organisation_id`) REFERENCES `tbl_organisation` (`organisation_id`),
  CONSTRAINT `fk_tbl_mapped_industries_statutory_mapping_id` FOREIGN KEY (`statutory_mapping_id`) REFERENCES `tbl_statutory_mappings` (`statutory_mapping_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tbl_mapped_locations`;
CREATE TABLE `tbl_mapped_locations` (
  `statutory_mapping_id` int(11) NOT NULL,
  `geography_id` int(11) NOT NULL,
  `assigned_by` int(11) DEFAULT NULL,
  `assigned_on` timestamp NULL DEFAULT NULL,
  KEY `fk_tbl_mapped_locations_statutory_mapping_id` (`statutory_mapping_id`),
  KEY `fk_tbl_mapped_locations_geography_id` (`geography_id`),
  CONSTRAINT `fk_tbl_mapped_locations_geography_id` FOREIGN KEY (`geography_id`) REFERENCES `tbl_geographies` (`geography_id`),
  CONSTRAINT `fk_tbl_mapped_locations_statutory_mapping_id` FOREIGN KEY (`statutory_mapping_id`) REFERENCES `tbl_statutory_mappings` (`statutory_mapping_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


DROP TABLE IF EXISTS `tbl_mapped_statutories`;
CREATE TABLE `tbl_mapped_statutories` (
  `statutory_mapping_id` int(11) NOT NULL,
  `statutory_id` int(11) NOT NULL,
  `assigned_by` int(11) DEFAULT NULL,
  `assigned_on` timestamp NULL DEFAULT NULL,
  KEY `fk_tbl_mapped_statutories_statutory_mapping_id` (`statutory_mapping_id`),
  KEY `fk_tbl_mapped_statutories_statutory_id` (`statutory_id`),
  CONSTRAINT `fk_tbl_mapped_statutories_statutory_id` FOREIGN KEY (`statutory_id`) REFERENCES `tbl_statutories` (`statutory_id`),
  CONSTRAINT `fk_tbl_mapped_statutories_statutory_mapping_id` FOREIGN KEY (`statutory_mapping_id`) REFERENCES `tbl_statutory_mappings` (`statutory_mapping_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tbl_statutory_mappings_approved_history`;
CREATE TABLE `tbl_statutory_mappings_approved_history` (
  `statutory_mapping_id` int(11) NOT NULL,
  `compliance_id` int(11) NOT NULL,
  `approve_status_id` int(11) NOT NULL,
  `approved_by` int(11) DEFAULT NULL,
  `approved_on` timestamp NULL DEFAULT NULL,
  `remarks` varchar(500) DEFAULT NULL,
  KEY `fk_tbl_statutory_mappings_approved_history_statutory_mapping_id` (`statutory_mapping_id`),
  KEY `fk_tbl_statutory_mappings_approved_history_compliance_id` (`compliance_id`),
  CONSTRAINT `fk_tbl_statutory_mappings_approved_history_compliance_id` FOREIGN KEY (`compliance_id`) REFERENCES `tbl_compliances` (`compliance_id`),
  CONSTRAINT `fk_tbl_statutory_mappings_approved_history_statutory_mapping_id` FOREIGN KEY (`statutory_mapping_id`) REFERENCES `tbl_statutory_mappings` (`statutory_mapping_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


DROP TABLE IF EXISTS `tbl_compliance_update_history`;
CREATE TABLE `tbl_compliance_update_history` (
  `compliance_id` int(11) NOT NULL AUTO_INCREMENT,
  `statutory_mapping_id` int(11) NOT NULL,
  `country_id` int(11) NOT NULL,
  `domain_id` int(11) NOT NULL,
  `statutory_provision` varchar(500) NOT NULL,
  `compliance_task` varchar(100) NOT NULL,
  `document_name` varchar(100) DEFAULT NULL,
  `compliance_description` longtext,
  `penal_consequences` longtext,
  `reference_link` varchar(500) DEFAULT NULL,
  `frequency_id` int(11) NOT NULL,
  `statutory_dates` longtext,
  `repeats_type_id` int(11) DEFAULT NULL,
  `duration_type_id` int(11) DEFAULT NULL,
  `repeats_every` int(11) DEFAULT NULL,
  `duration` int(11) DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT '1',
  `status_changed_on` timestamp NULL DEFAULT NULL,
  `is_approved` tinyint(1) DEFAULT '0',
  `approved_by` int(11) DEFAULT NULL,
  `approved_on` timestamp NULL DEFAULT NULL,
  `remarks` varchar(500) DEFAULT NULL,
  `format_file` longtext,
  `format_file_size` float DEFAULT NULL,
  `statutory_nature_id` int(11) DEFAULT NULL,
  `organisation_ids` longtext,
  `statutory_ids` longtext,
  `geography_ids` longtext,
  `updated_by` int(11) DEFAULT NULL,
  `updated_on` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`compliance_id`),
  KEY `fk_tbl_compliance_update_history_statutory_mapping_id` (`statutory_mapping_id`),
  KEY `fk_tbl_compliance_update_history_frequency_id` (`frequency_id`),
  CONSTRAINT `fk_tbl_compliance_update_history_frequency_id` FOREIGN KEY (`frequency_id`) REFERENCES `tbl_compliance_frequency` (`frequency_id`),
  CONSTRAINT `fk_tbl_compliance_update_history_statutory_mapping_id` FOREIGN KEY (`statutory_mapping_id`) REFERENCES `tbl_statutory_mappings` (`statutory_mapping_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tbl_client_groups`;
CREATE TABLE `tbl_client_groups` (
  `client_id` int(11) NOT NULL AUTO_INCREMENT,
  `short_name` varchar(20) NOT NULL,
  `email_id` varchar(100) NOT NULL,
  `group_admin_username` varchar(20) NOT NULL,
  `total_view_licence` int(11) DEFAULT NULL,
  `is_active` tinyint(4) DEFAULT '1',
  `status_changed_on` timestamp NULL DEFAULT NULL,
  `is_approved` tinyint(4) DEFAULT '0',
  `approved_by` int(11) DEFAULT NULL,
  `approved_on` timestamp NULL DEFAULT NULL,
  `created_by` int(11) DEFAULT NULL,
  `created_on` timestamp NULL DEFAULT NULL,
  `updated_by` int(11) DEFAULT NULL,
  `updated_on` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`client_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tbl_business_groups`;
CREATE TABLE `tbl_business_groups` (
  `business_group_id` int(11) NOT NULL AUTO_INCREMENT,
  `client_id` int(11) NOT NULL,
  `business_group_name` varchar(100) NOT NULL,
  `created_by` int(11) NOT NULL,
  `created_on` timestamp NULL DEFAULT NULL,
  `updated_by` int(11) DEFAULT NULL,
  `updated_on` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`business_group_id`),
  KEY `fk_tbl_cg_bg` (`client_id`),
  CONSTRAINT `fk_tbl_cg_bg` FOREIGN KEY (`client_id`) REFERENCES `tbl_client_groups` (`client_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tbl_legal_entities`;
CREATE TABLE `tbl_legal_entities` (
  `legal_entity_id` int(11) NOT NULL AUTO_INCREMENT,
  `country_id` int(11) NOT NULL,
  `client_id` int(11) NOT NULL,
  `business_group_id` int(11) DEFAULT NULL,
  `legal_entity_name` varchar(100) DEFAULT NULL,
  `contract_from` date DEFAULT NULL,
  `contract_to` date DEFAULT NULL,
  `logo` varchar(200) DEFAULT NULL,
  `file_space_limit` float DEFAULT '0',
  `total_licence` int(11) DEFAULT '0',
  `is_closed` tinyint(4) DEFAULT '1',
  `closed_on` timestamp NULL DEFAULT NULL,
  `closed_by` int(11) DEFAULT NULL,
  `closed_remarks` varchar(500) DEFAULT NULL,
  `created_by` int(11) DEFAULT NULL,
  `created_on` timestamp NULL DEFAULT NULL,
  `updated_by` int(11) DEFAULT NULL,
  `updated_on` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `logo_size` float DEFAULT '0',
  PRIMARY KEY (`legal_entity_id`),
  KEY `tbl_legal_entities_client_id` (`client_id`),
  KEY `tbl_legal_entities_country_id` (`country_id`),
  CONSTRAINT `tbl_legal_entities_client_id` FOREIGN KEY (`client_id`) REFERENCES `tbl_client_groups` (`client_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `tbl_legal_entities_country_id` FOREIGN KEY (`country_id`) REFERENCES `tbl_countries` (`country_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tbl_legal_entity_domains`;
CREATE TABLE `tbl_legal_entity_domains` (
  `legal_entity_id` int(11) NOT NULL,
  `domain_id` int(11) NOT NULL,
  `activation_date` timestamp NULL DEFAULT NULL,
  `organisation_id` int(11) NOT NULL,
  `count` int(11) NOT NULL,
  `created_by` int(11) DEFAULT NULL,
  `created_on` timestamp NULL DEFAULT NULL,
  KEY `fk_tbl_legal_entity_domains_legal_entity_id` (`legal_entity_id`),
  KEY `fk_tbl_legal_entity_domains_domain_id` (`domain_id`),
  CONSTRAINT `fk_tbl_legal_entity_domains_domain_id` FOREIGN KEY (`domain_id`) REFERENCES `tbl_domains` (`domain_id`),
  CONSTRAINT `fk_tbl_legal_entity_domains_legal_entity_id` FOREIGN KEY (`legal_entity_id`) REFERENCES `tbl_legal_entities` (`legal_entity_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tbl_legal_entity_contract_history`;
CREATE TABLE `tbl_legal_entity_contract_history` (
  `legal_entity_id` int(11) NOT NULL AUTO_INCREMENT,
  `country_id` int(11) NOT NULL,
  `client_id` int(11) NOT NULL,
  `business_group_id` int(11) DEFAULT NULL,
  `legal_entity_name` varchar(100) DEFAULT NULL,
  `contract_from` date DEFAULT NULL,
  `contract_to` date DEFAULT NULL,
  `logo` varchar(200) DEFAULT NULL,
  `logo_size` float DEFAULT '0',
  `file_space_limit` float DEFAULT '0',
  `total_licence` int(11) DEFAULT '0',
  `is_closed` tinyint(4) DEFAULT '1',
  `closed_on` timestamp NULL DEFAULT NULL,
  `closed_by` int(11) DEFAULT NULL,
  `closed_remarks` varchar(500) DEFAULT NULL,
  `created_by` int(11) DEFAULT NULL,
  `created_on` timestamp NULL DEFAULT NULL,
  `updated_by` int(11) DEFAULT NULL,
  `updated_on` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`legal_entity_id`),
  KEY `tbl_legal_entity_contract_history_client_id` (`client_id`),
  KEY `tbl_legal_entity_contract_history_country_id` (`country_id`),
  CONSTRAINT `tbl_legal_entity_contract_history_client_id` FOREIGN KEY (`client_id`) REFERENCES `tbl_client_groups` (`client_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `tbl_legal_entity_contract_history_country_id` FOREIGN KEY (`country_id`) REFERENCES `tbl_countries` (`country_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tbl_legal_entity_domains_history`;
CREATE TABLE `tbl_legal_entity_domains_history` (
  `legal_entity_id` int(11) NOT NULL,
  `domain_id` int(11) NOT NULL,
  `activation_date` timestamp NULL DEFAULT NULL,
  `organisation_id` int(11) NOT NULL,
  `count` int(11) NOT NULL,
  `created_by` int(11) DEFAULT NULL,
  `created_on` timestamp NULL DEFAULT NULL,
  KEY `fk_tbl_legal_entity_domains_history_legal_entity_id` (`legal_entity_id`),
  KEY `fk_tbl_legal_entity_domains_history_domain_id` (`domain_id`),
  CONSTRAINT `fk_tbl_legal_entity_domains_history_domain_id` FOREIGN KEY (`domain_id`) REFERENCES `tbl_domains` (`domain_id`),
  CONSTRAINT `fk_tbl_legal_entity_domains_history_legal_entity_id` FOREIGN KEY (`legal_entity_id`) REFERENCES `tbl_legal_entities` (`legal_entity_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tbl_divisions`;
CREATE TABLE `tbl_divisions` (
  `client_id` int(11) NOT NULL,
  `division_id` int(11) NOT NULL AUTO_INCREMENT,
  `division_name` varchar(100) DEFAULT NULL,
  `legal_entity_id` int(11) DEFAULT NULL,
  `business_group_id` int(11) DEFAULT NULL,
  `created_by` int(11) DEFAULT NULL,
  `created_on` timestamp NULL DEFAULT NULL,
  `updated_by` int(11) DEFAULT NULL,
  `updated_on` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`division_id`),
  KEY `fk_divisions_business_groups` (`business_group_id`),
  KEY `fk_divisions_legal_entities` (`legal_entity_id`),
  KEY `fk_tbl_cg_div` (`client_id`),
  CONSTRAINT `fk_divisions_business_groups` FOREIGN KEY (`business_group_id`) REFERENCES `tbl_business_groups` (`business_group_id`),
  CONSTRAINT `fk_divisions_legal_entities` FOREIGN KEY (`legal_entity_id`) REFERENCES `tbl_legal_entities` (`legal_entity_id`),
  CONSTRAINT `fk_tbl_cg_div` FOREIGN KEY (`client_id`) REFERENCES `tbl_client_groups` (`client_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tbl_categories`;
CREATE TABLE `tbl_categories` (
  `category_id` int(11) NOT NULL AUTO_INCREMENT,
  `client_id` int(11) NOT NULL,
  `category_name` varchar(100) DEFAULT NULL,
  `legal_entity_id` int(11) DEFAULT NULL,
  `business_group_id` int(11) DEFAULT NULL,
  `division_id` int(11) DEFAULT NULL,
  `created_by` int(11) DEFAULT NULL,
  `created_on` timestamp NULL DEFAULT NULL,
  `updated_by` int(11) DEFAULT NULL,
  `updated_on` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`category_id`),
  KEY `fk_tbl_categories_business_groups` (`business_group_id`),
  KEY `fk_tbl_categories_legal_entities` (`legal_entity_id`),
  KEY `fk_tbl_categories_cg_div` (`client_id`),
  CONSTRAINT `fk_tbl_categories_business_groups` FOREIGN KEY (`business_group_id`) REFERENCES `tbl_business_groups` (`business_group_id`),
  CONSTRAINT `fk_tbl_categories_cg_div` FOREIGN KEY (`client_id`) REFERENCES `tbl_client_groups` (`client_id`),
  CONSTRAINT `fk_tbl_categories_legal_entities` FOREIGN KEY (`legal_entity_id`) REFERENCES `tbl_legal_entities` (`legal_entity_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tbl_client_configuration`;
CREATE TABLE `tbl_client_configuration` (
  `client_id` int(11) NOT NULL,
  `country_id` int(11) NOT NULL,
  `domain_id` int(11) NOT NULL,
  `month_from` int(11) NOT NULL,
  `month_to` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


DROP TABLE IF EXISTS `tbl_units`;
CREATE TABLE `tbl_units` (
  `unit_id` int(11) NOT NULL AUTO_INCREMENT,
  `client_id` int(11) NOT NULL,
  `business_group_id` int(11) DEFAULT NULL,
  `legal_entity_id` int(11) NOT NULL,
  `division_id` int(11) DEFAULT NULL,
  `category_id` int(11) NOT NULL,
  `country_id` int(11) NOT NULL,
  `domain_ids` longtext,
  `organisation_ids` longtext,
  `geography_id` int(11) NOT NULL,
  `unit_code` varchar(50) NOT NULL,
  `unit_name` varchar(50) NOT NULL,
  `address` varchar(250) NOT NULL,
  `postal_code` int(11) NOT NULL,
  `is_closed` tinyint(4) DEFAULT '1',
  `closed_on` timestamp NULL DEFAULT NULL,
  `closed_by` int(11) DEFAULT NULL,
  `closed_remarks` varchar(500) DEFAULT NULL,
  `is_approved` tinyint(1) DEFAULT '0',
  `approved_by` int(11) DEFAULT NULL,
  `approved_on` timestamp NULL DEFAULT NULL,
  `remarks` varchar(500) DEFAULT NULL,
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
  CONSTRAINT `fk_legal_entities_id` FOREIGN KEY (`legal_entity_id`) REFERENCES `tbl_legal_entities` (`legal_entity_id`),
  CONSTRAINT `fk_tbl_units_1` FOREIGN KEY (`client_id`) REFERENCES `tbl_client_groups` (`client_id`),
  CONSTRAINT `fk_units_category` FOREIGN KEY (`category_id`) REFERENCES `tbl_categories` (`category_id`),
  CONSTRAINT `fk_units_geographies` FOREIGN KEY (`geography_id`) REFERENCES `tbl_geographies` (`geography_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tbl_units_organizations`;
CREATE TABLE `tbl_units_organizations` (
  `unit_id` int(11) NOT NULL,
  `domain_id` int(11) NOT NULL,
  `organisation_id` int(11) DEFAULT NULL,
  KEY `fk_unit_id` (`unit_id`),
  KEY `fk_domain_id` (`domain_id`),
  KEY `fk_organisation_id` (`organisation_id`),
  CONSTRAINT `fk_unit_id` FOREIGN KEY (`unit_id`) REFERENCES `tbl_units` (`unit_id`),
  CONSTRAINT `fk_domain_id` FOREIGN KEY (`domain_id`) REFERENCES `tbl_domains` (`domain_id`),
  CONSTRAINT `fk_organisation_id` FOREIGN KEY (`organisation_id`) REFERENCES `tbl_organisation` (`organisation_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tbl_client_statutories`;
CREATE TABLE `tbl_client_statutories` (
  `client_statutory_id` int(11) NOT NULL AUTO_INCREMENT,
  `client_id` int(11) NOT NULL,
  `unit_id` int(11) NOT NULL,
  `status` tinyint(4) DEFAULT '1',
  `reason` varchar(500) DEFAULT NULL,
  `approved_by` int(11) DEFAULT NULL,
  `approved_on` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`client_statutory_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tbl_client_compliances`;
CREATE TABLE `tbl_client_compliances` (
  `client_compliance_id` int(11) NOT NULL AUTO_INCREMENT,
  `client_statutory_id` int(11) NOT NULL,
  `client_id` int(11) NOT NULL,
  `legal_entity_id` int(11) NOT NULL,
  `unit_id` int(11) NOT NULL,
  `domain_id` int(11) DEFAULT NULL,
  `statutory_id` int(11) DEFAULT NULL,
  `statutory_applicable_status` tinyint(4) DEFAULT '0',
  `remarks` varchar(500) DEFAULT NULL,
  `compliance_id` int(11) NOT NULL,
  `compliance_applicable_status` tinyint(4) DEFAULT '0',
  `is_saved` tinyint(4) DEFAULT '0',
  `saved_by` int(11) DEFAULT NULL,
  `saved_on` timestamp NULL DEFAULT NULL,
  `is_approved` tinyint(4) DEFAULT '0',
  `approved_by` int(11) DEFAULT NULL,
  `approved_on` timestamp NULL DEFAULT NULL,
  `is_submitted` tinyint(4) DEFAULT '0',
  `submitted_by` int(11) DEFAULT NULL,
  `submitted_on` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`client_compliance_id`,`compliance_id`),
  UNIQUE KEY `client_compliance_id_UNIQUE` (`client_compliance_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


DROP TABLE IF EXISTS `tbl_application_server`;
CREATE TABLE `tbl_application_server` (
  `machine_id` int(11) NOT NULL AUTO_INCREMENT,
  `machine_name` varchar(50) NOT NULL,
  `ip` varchar(20) NOT NULL,
  `port` int(11) NOT NULL,
  `legal_entity_ids` longtext,
  `created_by` int(11) DEFAULT NULL,
  `created_on` timestamp NULL DEFAULT NULL,
  `updated_by` int(11) DEFAULT NULL,
  `updated_on` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`machine_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tbl_database_server`;
CREATE TABLE `tbl_database_server` (
  `database_server_id` int(11) NOT NULL AUTO_INCREMENT,
  `database_server_name` varchar(50) NOT NULL,
  `database_ip` varchar(20) NOT NULL,
  `database_port` int(11) NOT NULL,
  `database_username` varchar(50) NOT NULL,
  `database_password` varchar(50) NOT NULL,
  `legal_entity_ids` longtext,
  `created_by` int(11) DEFAULT NULL,
  `created_on` timestamp NULL DEFAULT NULL,
  `updated_by` int(11) DEFAULT NULL,
  `updated_on` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`database_server_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tbl_auto_deletion`;
CREATE TABLE `tbl_auto_deletion` (
  `deletion_id` int(11) NOT NULL AUTO_INCREMENT,
  `client_id` int(11) NOT NULL,
  `legal_entity_id` int(11) NOT NULL,
  `unit_id` int(11) NOT NULL,
  `deletion_period` int(11) NOT NULL,
  `created_by` int(11) DEFAULT NULL,
  `created_on` timestamp NULL DEFAULT NULL,
  `updated_by` int(11) DEFAULT NULL,
  `updated_on` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`deletion_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tbl_file_server`;
CREATE TABLE `tbl_file_server` (
  `file_server_id` int(11) NOT NULL AUTO_INCREMENT,
  `file_server_name` varchar(50) NOT NULL,
  `ip` varchar(20) NOT NULL,
  `port` int(11) NOT NULL,
  `legal_entity_ids` longtext,
  `created_by` int(11) DEFAULT NULL,
  `created_on` timestamp NULL DEFAULT NULL,
  `updated_by` int(11) DEFAULT NULL,
  `updated_on` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`file_server_id`)
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

DROP TABLE IF EXISTS `tbl_client_database`;
CREATE TABLE `tbl_client_database` (
  `client_database_id` int(11) NOT NULL AUTO_INCREMENT,
  `client_id` int(11) NOT NULL,
  `legal_entity_id` int(11) NOT NULL,
  `machine_id` int(11) NOT NULL,
  `file_server_id` int(11) NOT NULL,
  `database_server_id` int(11) NOT NULL,
  `created_by` int(11) DEFAULT NULL,
  `created_on` timestamp NULL DEFAULT NULL,
  `updated_by` int(11) DEFAULT NULL,
  `updated_on` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`client_database_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tbl_verification_type`;
CREATE TABLE `tbl_verification_type` (
  `verification_type_id` int(11) NOT NULL AUTO_INCREMENT,
  `verification_type` varchar(50) NOT NULL,
  PRIMARY KEY (`verification_type_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tbl_email_verification`;
CREATE TABLE `tbl_email_verification` (
  `user_id` int(11) NOT NULL,
  `verification_code` varchar(50) NOT NULL,
  `verification_type_id` int(11) NOT NULL,
  `expiry_date` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`verification_code`),
  KEY `fk_tbl_email_verification_verification_type_id` (`verification_type_id`),
  CONSTRAINT `fk_tbl_email_verification_verification_type_id` FOREIGN KEY (`verification_type_id`) REFERENCES `tbl_verification_type` (`verification_type_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


DROP TABLE IF EXISTS `tbl_mobile_registration`;
CREATE TABLE `tbl_mobile_registration` (
  `registration_key` varchar(50) NOT NULL,
  `device_type_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`registration_key`),
  KEY `fk_tbl_session_type_id` (`device_type_id`),
  KEY `fk_tbl_user_id` (`user_id`),
  CONSTRAINT `fk_tbl_session_type_id` FOREIGN KEY (`device_type_id`) REFERENCES `tbl_session_types` (`session_type_id`),
  CONSTRAINT `fk_tbl_user_id` FOREIGN KEY (`user_id`) REFERENCES `tbl_users` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


DROP TABLE IF EXISTS `tbl_statutory_notifications`;
CREATE TABLE `tbl_statutory_notifications` (
  `notification_id` int(11) NOT NULL AUTO_INCREMENT,
  `notification_text` longtext,
  `compliance_id` int(11) NOT NULL,
  `created_by` int(11) DEFAULT NULL,
  `created_on` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`notification_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


DROP TABLE IF EXISTS `tbl_statutory_notifications_users`;
CREATE TABLE `tbl_statutory_notifications_users` (
  `notification_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `read_status` tinyint(1) DEFAULT '0',
  UNIQUE KEY `notification_id_UNIQUE` (`notification_id`),
  UNIQUE KEY `user_id_UNIQUE` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


DROP TABLE IF EXISTS `tbl_messages`;
CREATE TABLE `tbl_messages` (
  `message_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_category_id` int(11) NOT NULL,
  `message_text` longtext,
  `created_by` int(11) DEFAULT NULL,
  `created_on` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`message_id`),
  KEY `fk_tbl_messages_user_category_id` (`user_category_id`),
  CONSTRAINT `fk_tbl_messages_user_category_id` FOREIGN KEY (`user_category_id`) REFERENCES `tbl_user_category` (`user_category_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


DROP TABLE IF EXISTS `tbl_message_users`;
CREATE TABLE `tbl_message_users` (
  `message_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `read_status` tinyint(1) DEFAULT '0',
  UNIQUE KEY `message_id_UNIQUE` (`message_id`),
  UNIQUE KEY `user_id_UNIQUE` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tbl_user_mapping`;
CREATE TABLE `tbl_user_mapping` (
  `user_mapping_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_category_id` int(11) NOT NULL,
  `country_id` int(11) NOT NULL,
  `domain_id` int(11) NOT NULL,
  `parent_user_id` int(11) NOT NULL,
  `child_user_id` int(11) NOT NULL,
  `created_by` int(11) DEFAULT NULL,
  `created_on` timestamp NULL DEFAULT NULL,
  `updated_by` int(11) DEFAULT NULL,
  `updated_on` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`user_mapping_id`),
  UNIQUE KEY `user_category_id_UNIQUE` (`user_category_id`),
  UNIQUE KEY `country_id_UNIQUE` (`country_id`),
  UNIQUE KEY `domain_id_UNIQUE` (`domain_id`),
  UNIQUE KEY `parent_user_id_UNIQUE` (`parent_user_id`),
  UNIQUE KEY `child_user_id_UNIQUE` (`child_user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


DROP TABLE IF EXISTS `tbl_user_legalentity`;
CREATE TABLE `tbl_user_legalentity` (
  `user_id` int(11) NOT NULL,
  `user_category_id` int(11) NOT NULL,
  `client_id` int(11) DEFAULT NULL,
  `legal_entity_id` int(11) DEFAULT NULL,
  `assigned_by` int(11) DEFAULT NULL,
  `assigned_on` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


DROP TABLE IF EXISTS `tbl_user_units`;
CREATE TABLE `tbl_user_units` (
  `user_id` int(11) NOT NULL,
  `user_category_id` int(11) NOT NULL,
  `client_id` int(11) DEFAULT NULL,
  `legal_entity_id` int(11) DEFAULT NULL,
  `unit_id` int(11) DEFAULT NULL,
  `domain_id` int(11) DEFAULT NULL,
  `assigned_by` int(11) DEFAULT NULL,
  `assigned_on` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


DROP TABLE IF EXISTS `tbl_user_account_reassign_history`;
CREATE TABLE `tbl_user_account_reassign_history` (
  `user_account_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_category_id` int(11) NOT NULL,
  `reassigned_from` int(11) DEFAULT NULL,
  `reassigned_to` int(11) DEFAULT NULL,
  `reassinged_data` varchar(500) DEFAULT NULL,
  `remarks` varchar(500) DEFAULT NULL,
  `assigned_by` int(11) DEFAULT NULL,
  `assigned_on` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`user_account_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tbl_validity_date_settings`;
CREATE TABLE `tbl_validity_date_settings` (
  `validity_date_id` int(11) NOT NULL AUTO_INCREMENT,
  `country_id` int(11) NOT NULL,
  `domain_id` int(11) NOT NULL,
  `days` int(11) NOT NULL,
  `created_by` int(11) DEFAULT NULL,
  `created_on` timestamp NULL DEFAULT NULL,
  `updated_by` int(11) DEFAULT NULL,
  `updated_on` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`validity_date_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
