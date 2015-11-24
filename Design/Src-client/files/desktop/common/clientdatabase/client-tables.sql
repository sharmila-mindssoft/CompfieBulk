DROP TABLE IF EXISTS `tbl_countries`;
CREATE TABLE `tbl_countries` (
  `country_id` int(11) NOT NULL,
  `country_name` varchar(50) DEFAULT NULL,
  `is_active` tinyint(4) DEFAULT '1',
  PRIMARY KEY (`country_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
DROP TABLE IF EXISTS `tbl_domains`;
CREATE TABLE `tbl_domains` (
  `domain_id` int(11) NOT NULL,
  `domain_name` varchar(50) NOT NULL,
  `is_active` tinyint(4) DEFAULT '1',
  PRIMARY KEY (`domain_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
DROP TABLE IF EXISTS `tbl_compliances`;
CREATE TABLE `tbl_compliances` (
  `compliance_id` int(11) NOT NULL,
  `statutory_mapping` varchar(500) DEFAULT NULL,
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
  `is_active` tinyint(4) DEFAULT NULL,
  `updated_on` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`compliance_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
DROP TABLE IF EXISTS `tbl_client_settings`;
CREATE TABLE `tbl_client_settings` (
  `country_ids` varchar(250) NOT NULL,
  `domain_ids` varchar(250) NOT NULL,
  `logo_url` varchar(200) DEFAULT NULL,
  `contract_from` date DEFAULT NULL,
  `contract_to` date DEFAULT NULL,
  `no_of_user_licence` int(11) DEFAULT NULL,
  `total_disk_space` float(11) DEFAULT NULL,
  `is_sms_subscribed` tinyint(4) DEFAULT NULL,
  `two_levels_of_approval` tinyint(4) DEFAULT NULL,
  `assignee_reminder` int(11) DEFAULT NULL,
  `escalation_reminder_in_advance` int(11) DEFAULT NULL,
  `escalation_reminder` int(11) DEFAULT NULL,
  `updated_by` int(11) DEFAULT NULL,
  `updated_on` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`domain_ids`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
DROP TABLE IF EXISTS `tbl_client_configurations`;
CREATE TABLE `tbl_client_configurations` (
  `country_id` int(11) DEFAULT NULL,
  `domain_id` int(11) DEFAULT NULL,
  `period_from` int(11) DEFAULT NULL,
  `period_to` int(11) DEFAULT NULL,
  `updated_by` int(11) DEFAULT NULL,
  `updated_on` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT `fk_client_configurations_countries` FOREIGN KEY (`country_id`) REFERENCES `tbl_countries` (`country_id`),
  CONSTRAINT `fk_client_configurations_domains` FOREIGN KEY (`domain_id`) REFERENCES `tbl_domains` (`domain_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
DROP TABLE IF EXISTS `tbl_business_groups`;
CREATE TABLE `tbl_business_groups` (
  `business_group_id` int(11) NOT NULL,
  `business_group_name` varchar(100) DEFAULT NULL,
  `created_by` int(11) DEFAULT NULL,
  `created_on` timestamp NULL DEFAULT NULL,
  `updated_by` int(11) DEFAULT NULL,
  `updated_on` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`business_group_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
DROP TABLE IF EXISTS `tbl_legal_entities`;
CREATE TABLE `tbl_legal_entities` (
  `legal_entity_id` int(11) NOT NULL,
  `legal_entity_name` varchar(100) DEFAULT NULL,
  `business_group_id` int(11) DEFAULT NULL,
  `created_by` int(11) DEFAULT NULL,
  `created_on` timestamp NULL DEFAULT NULL,
  `updated_by` int(11) DEFAULT NULL,
  `updated_on` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`legal_entity_id`),
  CONSTRAINT `fk_legal_entities_business_groups` FOREIGN KEY (`business_group_id`) REFERENCES `tbl_business_groups` (`business_group_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
DROP TABLE IF EXISTS `tbl_divisions`;
CREATE TABLE `tbl_divisions` (
  `division_id` int(11) NOT NULL,
  `division_name` varchar(100) DEFAULT NULL,
  `legal_entity_id` int(11) DEFAULT NULL,
  `business_group_id` int(11) DEFAULT NULL,
  `created_by` int(11) DEFAULT NULL,
  `created_on` timestamp NULL DEFAULT NULL,
  `updated_by` int(11) DEFAULT NULL,
  `updated_on` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`division_id`),
  CONSTRAINT `fk_divisions_business_groups` FOREIGN KEY (`business_group_id`) REFERENCES `tbl_business_groups` (`business_group_id`),
  CONSTRAINT `fk_divisions_legal_entities` FOREIGN KEY (`legal_entity_id`) REFERENCES `tbl_legal_entities` (`legal_entity_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
DROP TABLE IF EXISTS `tbl_units`;
CREATE TABLE `tbl_units` (
  `unit_id` int(11) NOT NULL,
  `division_id` int(11) DEFAULT NULL,
  `legal_entity_id` int(11) DEFAULT NULL,
  `business_group_id` int(11) DEFAULT NULL,
  `country_id` int(11) DEFAULT NULL,
  `geography` longtext,
  `unit_code` varchar(50) DEFAULT NULL,
  `unit_name` varchar(50) DEFAULT NULL,
  `industry_name` varchar(50) DEFAULT NULL,
  `address` varchar(500) DEFAULT NULL,
  `postal_code` int(11) DEFAULT NULL,
  `domain_ids` varchar(100) DEFAULT NULL,
  `is_active` tinyint(4) DEFAULT '1',
  PRIMARY KEY (`unit_id`),
  CONSTRAINT `fk_units_divisions` FOREIGN KEY (`division_id`) REFERENCES `tbl_divisions` (`division_id`),
  CONSTRAINT `fk_units_legel_entities` FOREIGN KEY (`legal_entity_id`) REFERENCES `tbl_legal_entities` (`legal_entity_id`),
  CONSTRAINT `fk_units_business_groups` FOREIGN KEY (`business_group_id`) REFERENCES `tbl_business_groups` (`business_group_id`),
  CONSTRAINT `fk_units_countries` FOREIGN KEY (`country_id`) REFERENCES `tbl_countries` (`country_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
DROP TABLE IF EXISTS `tbl_service_providers`;
CREATE TABLE `tbl_service_providers` (
  `service_provider_id` int(11) NOT NULL,
  `service_provider_name` varchar(50) DEFAULT NULL,
  `address` varchar(500) DEFAULT NULL,
  `contract_from` date DEFAULT NULL,
  `contract_to` date DEFAULT NULL,
  `contact_person` varchar(50) DEFAULT NULL,
  `contact_no` int(11) DEFAULT NULL,
  `is_active` tinyint(4) DEFAULT NULL,
  `created_by` int(11) DEFAULT NULL,
  `created_on` timestamp NULL DEFAULT NULL,
  `updated_by` int(11) DEFAULT NULL,
  `updated_on` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`service_provider_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
DROP TABLE IF EXISTS `tbl_client_user_groups`;
CREATE TABLE `tbl_client_user_groups` (
  `user_group_id` int(11) NOT NULL,
  `user_group_name` varchar(50) DEFAULT NULL,
  `form_type` varchar(20) DEFAULT NULL,
  `form_ids` longtext,
  `is_active` tinyint(4) DEFAULT '1',
  `created_by` int(11) DEFAULT NULL,
  `created_on` timestamp NULL DEFAULT NULL,
  `updated_by` int(11) DEFAULT NULL,
  `updated_on` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`user_group_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
DROP TABLE IF EXISTS `tbl_client_user_details`;
CREATE TABLE `tbl_client_user_details` (
  `user_id` int(11) NOT NULL,
  `email_id` varchar(100) DEFAULT NULL,
  `user_group_id` int(11) DEFAULT NULL,
  `employee_name` varchar(50) DEFAULT NULL,
  `employee_code` varchar(50) DEFAULT NULL,
  `contact_no` int(11) DEFAULT NULL,
  `seating_unit_id` int(11) DEFAULT NULL,
  `user_level` int(11) DEFAULT NULL,
  `country_ids` varchar(250) DEFAULT NULL,
  `domain_ids` varchar(250) DEFAULT NULL,
  `unit_ids` longtext,
  `is_admin` tinyint(4) DEFAULT '0',
  `is_service_provider` tinyint(4) DEFAULT NULL,
  `service_provider_id` int(11) DEFAULT NULL,
  `created_by` int(11) DEFAULT NULL,
  `created_on` timestamp NULL DEFAULT NULL,
  `updated_by` int(11) DEFAULT NULL,
  `updated_on` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`user_id`),
  CONSTRAINT `fk_client_user_details_client_user_groups` FOREIGN KEY (`user_group_id`) REFERENCES `tbl_client_user_groups` (`user_group_id`),
  CONSTRAINT `fk_client_user_details_service_providers` FOREIGN KEY (`service_provider_id`) REFERENCES `tbl_service_providers` (`service_provider_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
DROP TABLE IF EXISTS `tbl_assigned_compliances`;
CREATE TABLE `tbl_assigned_compliances` (
  `country_id` int(11) NOT NULL,
  `unit_id` int(11) DEFAULT NULL,
  `compliance_id` int(11) DEFAULT NULL,
  `trigger_before_days` longtext,
  `due_date` date DEFAULT NULL,
  `validity_date` date DEFAULT NULL,
  `assignee` int(11) DEFAULT NULL,
  `concurrence_person` int(11) DEFAULT NULL,
  `approval_person` int(11) DEFAULT NULL,
  `is_reassigned` tinyint(4) DEFAULT NULL,
  `is_active` tinyint(4) DEFAULT NULL,
  `created_by` int(11) DEFAULT NULL,
  `created_on` timestamp NULL DEFAULT NULL,
  `updated_by` int(11) DEFAULT NULL,
  `updated_on` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT `fk_assigned_compliances_countries` FOREIGN KEY (`country_id`) REFERENCES `tbl_countries` (`country_id`),
  CONSTRAINT `fk_assigned_compliances_units` FOREIGN KEY (`unit_id`) REFERENCES `tbl_units` (`unit_id`),
  CONSTRAINT `fk_assigned_compliances_compliances` FOREIGN KEY (`compliance_id`) REFERENCES `tbl_compliances` (`compliance_id`),
  CONSTRAINT `fk_assigned_compliances_assignee_client_user_details` FOREIGN KEY (`assignee`) REFERENCES `tbl_client_user_details` (`user_id`),
  CONSTRAINT `fk_assigned_compliances_concurrence_client_user_details` FOREIGN KEY (`concurrence_person`) REFERENCES `tbl_client_user_details` (`user_id`),
  CONSTRAINT `fk_assigned_compliances_approve_client_user_details` FOREIGN KEY (`approval_person`) REFERENCES `tbl_client_user_details` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
DROP TABLE IF EXISTS `tbl_reassigned_compliances_history`;
CREATE TABLE `tbl_reassigned_compliances_history` (
  `unit_id` int(11) NOT NULL,
  `compliance_id` int(11) DEFAULT NULL,
  `assignee` int(11) DEFAULT NULL,
  `reassigned_from` int(11) DEFAULT NULL,
  `reassigned_date` date DEFAULT NULL,
  `remarks` varchar(500) DEFAULT NULL,
  `created_by` int(11) DEFAULT NULL,
  `created_on` timestamp NULL DEFAULT NULL,
  `updated_by` int(11) DEFAULT NULL,
  `updated_on` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT `fk_rch_assignee_user_details` FOREIGN KEY (`assignee`) REFERENCES `tbl_client_user_details` (`user_id`),
  CONSTRAINT `fk_rch_reassigned_from_user_details` FOREIGN KEY (`reassigned_from`) REFERENCES `tbl_client_user_details` (`user_id`),
  CONSTRAINT `fk_rch_compliances` FOREIGN KEY (`compliance_id`) REFERENCES `tbl_compliances` (`compliance_id`),
  CONSTRAINT `fk_rch_units` FOREIGN KEY (`unit_id`) REFERENCES `tbl_units` (`unit_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
DROP TABLE IF EXISTS `tbl_compliance_history`;
CREATE TABLE `tbl_compliance_history` (
  `compliance_history_id` int(11) NOT NULL,
  `unit_id` int(11) DEFAULT NULL,
  `compliance_id` int(11) DEFAULT NULL,
  `start_date` date DEFAULT NULL,
  `due_date` date DEFAULT NULL,
  `completion_date` timestamp NULL DEFAULT NULL,
  `documents` longtext,
  `validity_date` date DEFAULT NULL,
  `next_due_date` date DEFAULT NULL,
  `remarks` varchar(500) DEFAULT NULL,
  `completed_by` int(11) DEFAULT NULL,
  `completed_on` timestamp NULL DEFAULT NULL,
  `concurrence_status` varchar(20) DEFAULT NULL,
  `concurred_by` int(11) DEFAULT NULL,
  `concurred_on` timestamp NULL DEFAULT NULL,
  `approve_status` varchar(20) DEFAULT NULL,
  `approved_by` int(11) DEFAULT NULL,
  `approved_on` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`compliance_history_id`),
  CONSTRAINT `fk_compliance_history_user_details` FOREIGN KEY (`completed_by`) REFERENCES `tbl_client_user_details` (`user_id`),
  CONSTRAINT `fk_compliance_history_compliances` FOREIGN KEY (`compliance_id`) REFERENCES `tbl_compliances` (`compliance_id`),
  CONSTRAINT `fk_compliance_history_units` FOREIGN KEY (`unit_id`) REFERENCES `tbl_units` (`unit_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
DROP TABLE IF EXISTS `tbl_compliance_activity_log`;
CREATE TABLE `tbl_compliance_activity_log` (
  `compliance_activity_id` int(11) NOT NULL,
  `unit_id` int(11) DEFAULT NULL,
  `compliance_id` int(11) DEFAULT NULL,
  `activity_date` date DEFAULT NULL,
  `activity_status` varchar(20) DEFAULT NULL,
  `compliance_status` varchar(20) DEFAULT NULL,
  `remarks` varchar(500) DEFAULT NULL,
  `updated_on` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`compliance_activity_id`),
  CONSTRAINT `fk_compliance_activity_log_compliances` FOREIGN KEY (`compliance_id`) REFERENCES `tbl_compliances` (`compliance_id`),
  CONSTRAINT `fk_compliance_activity_log_units` FOREIGN KEY (`unit_id`) REFERENCES `tbl_units` (`unit_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
DROP TABLE IF EXISTS `tbl_notifications_log`;
CREATE TABLE `tbl_notifications_log` (
  `notification_id` int(11) NOT NULL,
  `notification_type` varchar(20) DEFAULT NULL,
  `country_id` int(11) DEFAULT NULL,
  `domain_id` int(11) DEFAULT NULL,
  `business_group_id` int(11) DEFAULT NULL,
  `legal_entity_id` int(11) DEFAULT NULL,
  `division_id` int(11) DEFAULT NULL,
  `unit_id` int(11) DEFAULT NULL,
  `statutory_provision` varchar(250) DEFAULT NULL,
  `compliance_id` int(11) DEFAULT NULL,
  `assignee` int(11) DEFAULT NULL,
  `concurrence_person` int(11) DEFAULT NULL,
  `approval_person` int(11) DEFAULT NULL,
  `notification_text` longtext,
  `extra_details` longtext,
  `updated_on` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`notification_id`),
  CONSTRAINT `fk_notifications_log_countries` FOREIGN KEY (`country_id`) REFERENCES `tbl_countries` (`country_id`),
  CONSTRAINT `fk_notifications_log_domains` FOREIGN KEY (`domain_id`) REFERENCES `tbl_domains` (`domain_id`),
  CONSTRAINT `fk_notifications_log_business_groups` FOREIGN KEY (`business_group_id`) REFERENCES `tbl_business_groups` (`business_group_id`),
  CONSTRAINT `fk_notifications_log_legal_entities` FOREIGN KEY (`legal_entity_id`) REFERENCES `tbl_legal_entities` (`legal_entity_id`),
  CONSTRAINT `fk_notifications_log_divisions` FOREIGN KEY (`division_id`) REFERENCES `tbl_divisions` (`division_id`),
  CONSTRAINT `fk_notifications_log_units` FOREIGN KEY (`unit_id`) REFERENCES `tbl_units` (`unit_id`),
  CONSTRAINT `fk_notifications_log_compliances` FOREIGN KEY (`compliance_id`) REFERENCES `tbl_compliances` (`compliance_id`),
  CONSTRAINT `fk_notifications_log_assignee_units` FOREIGN KEY (`assignee`) REFERENCES `tbl_client_user_details` (`user_id`),
  CONSTRAINT `fk_notifications_log_concurrence_units` FOREIGN KEY (`concurrence_person`) REFERENCES `tbl_units` (`unit_id`),
  CONSTRAINT `fk_notifications_log_approve_units` FOREIGN KEY (`approval_person`) REFERENCES `tbl_units` (`unit_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
DROP TABLE IF EXISTS `tbl_notifications_status`;
CREATE TABLE `tbl_notifications_status` (
  `notification_id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `read_status` tinyint(4) DEFAULT NULL,
  `updated_on` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT `fk_notifications_status_notifications_log` FOREIGN KEY (`notification_id`) REFERENCES `tbl_notifications_log` (`notification_id`),
  CONSTRAINT `fk_notifications_status_user_details` FOREIGN KEY (`user_id`) REFERENCES `tbl_client_user_details` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;