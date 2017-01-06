DROP TABLE IF EXISTS `tbl_user_category`;
CREATE TABLE `tbl_user_category` (
  `user_category_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_category_name` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`user_category_id`)
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

DROP TABLE IF EXISTS `tbl_countries`;
CREATE TABLE `tbl_countries` (
  `country_id` int(11) NOT NULL AUTO_INCREMENT,
  `country_name` varchar(50) NOT NULL,
  `is_active` tinyint(4) DEFAULT '1',
  PRIMARY KEY (`country_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tbl_domains`;
CREATE TABLE `tbl_domains` (
  `domain_id` int(11) NOT NULL AUTO_INCREMENT,
  `domain_name` varchar(50) NOT NULL,
  `is_active` tinyint(4) DEFAULT '1',
  PRIMARY KEY (`domain_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tbl_domain_countries`;
CREATE TABLE `tbl_domain_countries` (
  `country_id` int(11) NOT NULL,
  `domain_id` int(11) NOT NULL,
  UNIQUE KEY (`country_id`, `domain_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tbl_organisation`;
CREATE TABLE `tbl_organisation` (
  `organisation_id` int(11) NOT NULL AUTO_INCREMENT,
  `country_id` int(11) NOT NULL,
  `domain_id` int(11) NOT NULL,
  `organisation_name` varchar(50) NOT NULL,
  `is_active` tinyint(4) DEFAULT '1',
  PRIMARY KEY (`organisation_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tbl_mapped_industries`;
CREATE TABLE `tbl_mapped_industries` (
  `statutory_mapping_id` int(11) NOT NULL,
  `organisation_id` int(11) NOT NULL,
  `assigned_by` int(11) DEFAULT NULL,
  `assigned_on` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tbl_client_groups`;
CREATE TABLE `tbl_client_groups` (
  `client_id` int(11) NOT NULL AUTO_INCREMENT,
  `group_name` varchar(50) NOT NULL,
  `short_name` varchar(20) NOT NULL,
  `email_id` varchar(100) NOT NULL,
  `group_admin_username` varchar(20) NOT NULL,
  `total_view_licence` int(11) DEFAULT NULL,
  `licence_used` int(11) DEFAULT NULL,
  PRIMARY KEY (`client_id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tbl_business_groups`;
CREATE TABLE `tbl_business_groups` (
  `business_group_id` int(11) NOT NULL,
  `client_id` int(11) NOT NULL,
  `business_group_name` varchar(100) NOT NULL,
  PRIMARY KEY (`business_group_id`),
  UNIQUE KEY(`business_group_id`, `client_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tbl_legal_entity`;
CREATE TABLE `tbl_legal_entity` (
  `legal_entity_id` int(11) NOT NULL AUTO_INCREMENT,
  `client_id` int(11) NOT NULL,
  `country_id` int(11) NOT NULL,
  `business_group_id` int(11) DEFAULT NULL,
  `legal_entity_name` varchar(100) DEFAULT NULL,
  `contract_from` date DEFAULT NULL,
  `contract_to` date DEFAULT NULL,
  `logo` varchar(200) DEFAULT NULL,
  `logo_size` float DEFAULT '0',
  `file_space_limit` float DEFAULT '0',
  `total_licence` int(11) DEFAULT '0',
  `used_file_space` float DEFAULT '0',
  `used_licence` int(11) DEFAULT '0',
  `is_closed` tinyint(4) DEFAULT '1',
  `closed_on` timestamp NULL DEFAULT NULL,
  `closed_by` int(11) DEFAULT NULL,
  `closed_remarks` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`legal_entity_id`),
  UNIQUE KEY(`legal_entity_id`, `client_id`)
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
  UNIQUE KEY(`legal_entity_id`, `domain_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tbl_divisions`;
CREATE TABLE `tbl_divisions` (
  `client_id` int(11) NOT NULL,
  `division_id` int(11) NOT NULL AUTO_INCREMENT,
  `division_name` varchar(100) DEFAULT NULL,
  `legal_entity_id` int(11) DEFAULT NULL,
  `business_group_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`division_id`),
  UNIQUE KEY(`division_id`, `client_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tbl_categories`;
CREATE TABLE `tbl_categories` (
  `category_id` int(11) NOT NULL AUTO_INCREMENT,
  `client_id` int(11) NOT NULL,
  `category_name` varchar(100) DEFAULT NULL,
  `legal_entity_id` int(11) NOT NULL,
  `business_group_id` int(11) DEFAULT NULL,
  `division_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`category_id`),
  UNIQUE KEY(`category_id`, `client_id`, `legal_entity_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tbl_client_configuration`;
CREATE TABLE `tbl_client_configuration` (
  `client_id` int(11) NOT NULL,
  `country_id` int(11) NOT NULL,
  `domain_id` int(11) NOT NULL,
  `month_from` int(11) NOT NULL,
  `month_to` int(11) NOT NULL,
  UNIQUE KEY(`client_id`, `country_id`)
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
  PRIMARY KEY (`unit_id`),
  UNIQUE KEY(`unit_id`, `client_id`, `legal_entity_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tbl_units_organizations`;
CREATE TABLE `tbl_units_organizations` (
  `unit_id` int(11) NOT NULL,
  `domain_id` int(11) NOT NULL,
  `organisation_id` int(11) DEFAULT NULL,
  UNIQUE KEY (`unit_id`, `domain_id`, `organisation_id`)
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
  `statutory_nature_id` int(11) DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT '1',
  `status_changed_on` timestamp NULL DEFAULT NULL,
  `format_file` longtext,
  `format_file_size` float DEFAULT NULL,
  `statutory_mapping` longtext,
  PRIMARY KEY (`compliance_id`),
  UNIQUE KEY(`compliance_id`, `country_id`, `domain_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tbl_client_compliances`;
CREATE TABLE `tbl_client_compliances` (
  `client_compliance_id` int(11) NOT NULL AUTO_INCREMENT,
  `client_id` int(11) NOT NULL,
  `legal_entity_id` int(11) NOT NULL,
  `unit_id` int(11) NOT NULL,
  `domain_id` int(11) DEFAULT NULL,
  `statutory_id` int(11) DEFAULT NULL,
  `statutory_applicable_status` tinyint(4) DEFAULT '0',
  `statutory_opted_status` tinyint(4) DEFAULT '0',
  `remarks` varchar(500) DEFAULT NULL,
  `compliance_id` int(11) NOT NULL,
  `compliance_applicable_status` tinyint(4) DEFAULT '0',
  `compliance_opted_status` tinyint(4) DEFAULT '0',
  `not_opted_remarks` varchar(500) DEFAULT NULL,
  `opted_by` int(11) DEFAULT NULL,
  `opted_on` timestamp NULL DEFAULT NULL,
  `is_new` tinyint(4) DEFAULT '0',
  `is_saved` tinyint(4) DEFAULT '0',
  `saved_by` int(11) DEFAULT NULL,
  `saved_on` timestamp NULL DEFAULT NULL,
  `is_submitted` tinyint(4) DEFAULT '0',
  `submitted_by` int(11) DEFAULT NULL,
  `submitted_on` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`client_compliance_id`),
  UNIQUE KEY(`unit_id`, `domain_id`, `compliance_id`)
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
  `is_read` tinyint(4) DEFAULT '0',
  UNIQUE KEY(`notification_id`, `user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
# replication tables ends

# client tables starts
DROP TABLE IF EXISTS `tbl_verification_type`;
CREATE TABLE `tbl_verification_type` (
  `verification_type_id` int(11) NOT NULL AUTO_INCREMENT,
  `verification_type` varchar(50) NOT NULL,
  PRIMARY KEY (`verification_type_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


DROP TABLE IF EXISTS `tbl_form_category`;
CREATE TABLE `tbl_form_category` (
  `form_category_id` int(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `form_id` int(11) NOT NULL,
  `user_category_id` int(11) NOT NULL,
  UNIQUE KEY(`form_id`,  `user_category_id`)
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

DROP TABLE IF EXISTS `tbl_session_types`;
CREATE TABLE `tbl_session_types` (
  `session_type_id` int(11) NOT NULL,
  `session_type` varchar(20) NOT NULL,
  PRIMARY KEY (`session_type_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tbl_user_groups`;
CREATE TABLE `tbl_user_groups` (
  `user_group_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_category_id` int(11) DEFAULT NULL,
  `user_group_name` varchar(50) DEFAULT NULL,
  `is_active` tinyint(4) DEFAULT '1',
  `status_changed_by` int(11) DEFAULT NULL,
  `status_changed_on` timestamp NULL DEFAULT NULL,
  `created_by` int(11) DEFAULT NULL,
  `created_on` timestamp NULL DEFAULT NULL,
  `updated_by` int(11) DEFAULT NULL,
  `updated_on` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`user_group_id`),
  CONSTRAINT `category_fk1` FOREIGN KEY (`user_category_id`) REFERENCES `tbl_user_category` (`user_category_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


DROP TABLE IF EXISTS `tbl_user_group_forms`;
CREATE TABLE `tbl_user_group_forms` (
  `user_group_id` int(11) NOT NULL,
  `form_id` int(11) DEFAULT NULL,
  UNIQUE KEY (`user_group_id`, `form_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tbl_service_providers`;
CREATE TABLE `tbl_service_providers` (
  `service_provider_id` int(11) NOT NULL AUTO_INCREMENT,
  `service_provider_name` varchar(50) NOT NULL,
  `address` varchar(500) DEFAULT NULL,
  `short_name` varchar(20) DEFAULT NULL,
  `contract_from` date DEFAULT NULL,
  `contract_to` date DEFAULT NULL,
  `contact_person` varchar(50) DEFAULT NULL,
  `contact_no` varchar(20) DEFAULT NULL,
  `mobile_no` varchar(20) DEFAULT NULL,
  `email_id` varchar(100) NOT NULL,
  `is_active` tinyint(1) DEFAULT '1',
  `status_changed_by` int(11) DEFAULT NULL,
  `status_changed_on` timestamp NULL DEFAULT NULL,
  `is_blocked` tinyint(1) DEFAULT '0',
  `blocked_by` int(11) DEFAULT NULL,
  `blocked_on` timestamp NULL DEFAULT NULL,
  `remarks` varchar(500) DEFAULT NULL,
  `created_by` int(11) DEFAULT NULL,
  `created_on` timestamp NULL DEFAULT NULL,
  `updated_by` int(11) DEFAULT NULL,
  `updated_on` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`service_provider_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tbl_users`;
CREATE TABLE `tbl_users` (
  `user_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_category_id` int(11) NOT NULL,
  `client_id` int(11) DEFAULT NULL,
  `user_group_id` int(11) DEFAULT NULL,
  `email_id` varchar(100) NOT NULL,
  `employee_name` varchar(50) DEFAULT NULL,
  `employee_code` varchar(50) DEFAULT NULL,
  `contact_no` varchar(20) DEFAULT NULL,
  `mobile_no` varchar(20) DEFAULT NULL,
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
  CONSTRAINT `category_fk2` FOREIGN KEY (`user_category_id`) REFERENCES `tbl_user_category` (`user_category_id`),
  CONSTRAINT `group_fk1` FOREIGN KEY (`user_group_id`) REFERENCES `tbl_user_groups` (`user_group_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tbl_user_login_details`;
CREATE TABLE `tbl_user_login_details` (
  `user_id` int(11) NOT NULL,
  `user_category_id` int(11) NOT NULL,
  `username` varchar(20) DEFAULT NULL,
  `is_active` tinyint(4) DEFAULT '1',
  `password` varchar(50) DEFAULT NULL,
  UNIQUE KEY(`user_id`, `user_category_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tbl_user_login_history`;
CREATE TABLE `tbl_user_login_history` (
  `user_id` int(11) NOT NULL,
  `ip` varchar(20) NOT NULL,
  `login_time` datetime DEFAULT NULL,
  `login_attempt` int(11) DEFAULT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tbl_user_sessions`;
CREATE TABLE `tbl_user_sessions` (
  `session_token` varchar(50) NOT NULL,
  `user_id` int(11) NOT NULL,
  `session_type_id` int(11) DEFAULT NULL,
  `last_accessed_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`session_token`),
  UNIQUE KEY(`user_id`, `session_type_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `tbl_user_domains` (
  `user_id` int(11) NOT NULL,
  `legal_entity_id` int(11) NOT NULL,
  `domain_id` int(11) NOT NULL,
  UNIQUE KEY (`user_id`, `legal_entity_id`, `domain_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `tbl_user_units` (
  `user_id` int(11) NOT NULL,
  `legal_entity_id` int(11) NOT NULL,
  `unit_id` int(11) NOT NULL,
  UNIQUE KEY (`user_id`, `legal_entity_id`, `unit_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tbl_mobile_registration`;
CREATE TABLE `tbl_mobile_registration` (
  `registration_key` varchar(50) NOT NULL,
  `device_type_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`registration_key`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tbl_email_verification`;
CREATE TABLE `tbl_email_verification` (
  `user_id` int(11) NOT NULL,
  `verification_code` varchar(50) NOT NULL,
  `verification_type_id` int(11) NOT NULL,
  `expiry_date` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tbl_unit_closure`;
CREATE TABLE `tbl_unit_closure` (
  `client_id` int(11) NOT NULL,
  `legal_entity_id` int(11) NOT NULL,
  `unit_id` int(11) NOT NULL,
  `is_closed` tinyint(4) DEFAULT '0',
  `closed_on` timestamp NULL DEFAULT NULL,
  `closed_by` int(11) DEFAULT NULL,
  `remarks` varchar(500) DEFAULT NULL,
  CONSTRAINT `legal_fk1` FOREIGN KEY (`legal_entity_id`) REFERENCES `tbl_legal_entity` (`legal_entity_id`),
  CONSTRAINT `unit_fk2` FOREIGN KEY (`unit_id`) REFERENCES `tbl_units` (`unit_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tbl_compliance_dates`;
CREATE TABLE `tbl_compliance_dates` (
  `legal_entity_id` int(11) NOT NULL,
  `compliance_id` int(11) NOT NULL,
  `frequency_id` int(11) NOT NULL,
  `unit_id` int(11) NOT NULL,
  `domain_id` int(11) NOT NULL,
  `old_statutory_date` longtext NOT NULL,
  `old_repeats_type_id` int(11) DEFAULT NULL,
  `old_repeats_every` int(11) DEFAULT NULL,
  `repeats_type_id` int(11) DEFAULT NULL,
  `repeats_every` int(11) DEFAULT NULL,
  `statutory_date` longtext NOT NULL,
  `trigger_before_days` int(11) DEFAULT NULL,
  `due_date` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tbl_compliance_dates`;
CREATE TABLE `tbl_compliance_dates_history` (
  `compliance_id` int(11) NOT NULL,
  `frequency_id` int(11) NOT NULL,
  `unit_id` int(11) NOT NULL,
  `domain_id` int(11) NOT NULL,
  `statutory_date` longtext NOT NULL,
  `repeats_type_id` int(11) DEFAULT NULL,
  `repeats_every` int(11) DEFAULT NULL,
  `updated_by` int(11) DEFAULT NULL,
  `updated_on` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


DROP TABLE IF EXISTS `tbl_assign_compliances`;
CREATE TABLE `tbl_assign_compliances` (
  `client_id` int(11) NOT NULL,
  `legal_entity_id` int(11) NOT NULL,
  `country_id` int(11) NOT NULL,
  `domain_id` int(11) NOT NULL,
  `unit_id` int(11) NOT NULL,
  `compliance_id` int(11) NOT NULL,
  `statutory_dates` longtext NOT NULL,
  `assignee` int(11) DEFAULT NULL,
  `assigned_by` int(11) DEFAULT NULL,
  `assigned_on` timestamp NULL DEFAULT NULL,
  `is_reassigned` tinyint(4) DEFAULT '0',
  `concurrence_person` int(11) DEFAULT NULL,
  `c_assigned_by` int(11) DEFAULT NULL,
  `c_assigned_on` timestamp NULL DEFAULT NULL,
  `c_is_reassigned` tinyint(4) DEFAULT '0',
  `approval_person` int(11) DEFAULT NULL,
  `a_assigned_by` int(11) DEFAULT NULL,
  `a_assigned_on` timestamp NULL DEFAULT NULL,
  `a_is_reassigned` tinyint(4) DEFAULT '0',
  `trigger_before_days` int(11) DEFAULT NULL,
  `due_date` date DEFAULT NULL,
  `validity_date` date DEFAULT NULL,
  CONSTRAINT `legalentity_fk1` FOREIGN KEY (`legal_entity_id`) REFERENCES `tbl_legal_entity` (`legal_entity_id`),
  CONSTRAINT `country_fk2` FOREIGN KEY (`country_id`) REFERENCES `tbl_countries` (`country_id`),
  CONSTRAINT `domain_fk3` FOREIGN KEY (`domain_id`) REFERENCES `tbl_domains` (`domain_id`),
  CONSTRAINT `unit_fk4` FOREIGN KEY (`unit_id`) REFERENCES `tbl_units` (`unit_id`),
  CONSTRAINT `compid_fk5` FOREIGN KEY (`compliance_id`) REFERENCES `tbl_compliances` (`compliance_id`),
  UNIQUE KEY(`unit_id`, `domain_id`, `compliance_id`, `assignee`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tbl_reassigned_compliances_history`;
CREATE TABLE `tbl_reassigned_compliances_history` (
  `reassign_history_id` int(11) NOT NULL,
  `client_id` int(11) NOT NULL,
  `legal_entity_id` int(11) NOT NULL,
  `unit_id` int(11) NOT NULL,
  `compliance_id` int(11) DEFAULT NULL,
  `old_assignee` int(11) DEFAULT NULL,
  `old_concurrer` int(11) DEFAULT NULL,
  `old_approver` int(11) DEFAULT NULL,
  `assignee` int(11) DEFAULT NULL,
  `concurrer` int(11) DEFAULT NULL,
  `approver` int(11) DEFAULT NULL,
  `remarks` varchar(500) DEFAULT NULL,
  `assigned_by` int(11) DEFAULT NULL,
  `assigned_on` timestamp NULL DEFAULT NULL,
  CONSTRAINT `r_unit_fk1` FOREIGN KEY (`unit_id`) REFERENCES `tbl_units` (`unit_id`),
  CONSTRAINT `r_compliance_fk2` FOREIGN KEY (`compliance_id`) REFERENCES `tbl_compliances` (`compliance_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tbl_compliance_history`;
CREATE TABLE `tbl_compliance_history` (
  `compliance_history_id` int(11) NOT NULL AUTO_INCREMENT,
  `legal_entity_id` int(11) NOT NULL,
  `unit_id` int(11) NOT NULL,
  `compliance_id` int(11) NOT NULL,
  `start_date` datetime NOT NULL,
  `due_date` datetime NOT NULL,
  `completion_date` datetime DEFAULT NULL,
  `documents` longtext,
  `document_size` int(11) DEFAULT NULL,
  `validity_date` datetime DEFAULT NULL,
  `next_due_date` datetime DEFAULT NULL,
  `remarks` varchar(500) DEFAULT NULL,
  `completed_by` int(11) NOT NULL,
  `completed_on` datetime DEFAULT NULL,
  `concurrence_status` varchar(20) DEFAULT NULL,
  `concurred_by` int(11) DEFAULT NULL,
  `concurred_on` datetime DEFAULT NULL,
  `approve_status` varchar(20) DEFAULT NULL,
  `approved_by` int(11) NOT NULL,
  `approved_on` datetime DEFAULT NULL,
  PRIMARY KEY (`compliance_history_id`),
  CONSTRAINT `ch_unit_fk11` FOREIGN KEY (`unit_id`) REFERENCES `tbl_units` (`unit_id`),
  CONSTRAINT `ch_compliance_fk12` FOREIGN KEY (`compliance_id`) REFERENCES `tbl_compliances` (`compliance_id`),
  UNIQUE KEY(`unit_id`, `compliance_id`, `start_date`, `due_date`, `next_due_date`, `completed_by`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tbl_activity_log`;
CREATE TABLE `tbl_activity_log` (
  `activity_log_id` int(11) NOT NULL AUTO_INCREMENT,
  `client_id` int(11) NOT NULL,
  `legal_entity_id` int(11) NOT NULL,
  `unit_id` int(11) NOT NULL,
  `user_category_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `form_id` int(11) NOT NULL,
  `action` varchar(500) NOT NULL,
  `created_on` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`activity_log_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tbl_compliance_activity_log`;
CREATE TABLE `tbl_compliance_activity_log` (
  `compliance_activity_id` int(11) NOT NULL AUTO_INCREMENT,
  `unit_id` int(11) DEFAULT NULL,
  `compliance_id` int(11) DEFAULT NULL,
  `compliance_history_id` int(11) DEFAULT NULL,
  `activity_date` date DEFAULT NULL,
  `activity_on` timestamp NULL DEFAULT NULL,
  `remarks` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`compliance_activity_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tbl_compliance_status_chart_unitwise`;
CREATE TABLE `tbl_compliance_status_chart_unitwise` (
  `client_id` int(11) NOT NULL,
  `legal_entity_id` int(11) NOT NULL,
  `country_id` int(11) NOT NULL,
  `domain_id` int(11) NOT NULL,
  `unit_id` int(11) NOT NULL,
  `complied` int(11) DEFAULT NULL,
  `delayed` int(11) DEFAULT NULL,
  `inprogress` int(11) DEFAULT NULL,
  `overdue` int(11) DEFAULT NULL,
  `chart_year` int(11) DEFAULT NULL,
  `month_from` int(11) DEFAULT NULL,
  `month_to` int(11) DEFAULT NULL,
  UNIQUE KEY(`legal_entity_id`, `country_id`, `domain_id`, `unit_id`, `chart_year`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tbl_compliance_status_chart_userwise`;
CREATE TABLE `tbl_compliance_status_chart_userwise` (
  `client_id` int(11) NOT NULL,
  `legal_entity_id` int(11) NOT NULL,
  `country_id` int(11) NOT NULL,
  `domain_id` int(11) NOT NULL,
  `unit_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `complied` int(11) DEFAULT NULL,
  `delayed` int(11) DEFAULT NULL,
  `inprogress` int(11) DEFAULT NULL,
  `overdue` int(11) DEFAULT NULL,
  `chart_year` int(11) DEFAULT NULL,
  `month_from` int(11) DEFAULT NULL,
  `month_to` int(11) DEFAULT NULL,
  UNIQUE KEY(`legal_entity_id`, `country_id`, `domain_id`, `unit_id`, `user_id`, `chart_year`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


DROP TABLE IF EXISTS `tbl_notcomplied_chart_unitwise`;
CREATE TABLE `tbl_notcomplied_chart_unitwise` (
  `client_id` int(11) NOT NULL,
  `legal_entity_id` int(11) NOT NULL,
  `country_id` int(11) NOT NULL,
  `domain_id` int(11) NOT NULL,
  `unit_id` int(11) NOT NULL,
  `below_30` int(11) DEFAULT NULL,
  `below_60` int(11) DEFAULT NULL,
  `below_90` int(11) DEFAULT NULL,
  `above_30` int(11) DEFAULT NULL,
  UNIQUE KEY(`legal_entity_id`, `country_id`, `domain_id`, `unit_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tbl_notcomplied_chart_userwise`;
CREATE TABLE `tbl_notcomplied_chart_userwise` (
  `client_id` int(11) NOT NULL,
  `legal_entity_id` int(11) NOT NULL,
  `country_id` int(11) NOT NULL,
  `domain_id` int(11) NOT NULL,
  `unit_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `below_30` int(11) DEFAULT NULL,
  `below_60` int(11) DEFAULT NULL,
  `below_90` int(11) DEFAULT NULL,
  `above_30` int(11) DEFAULT NULL,
  UNIQUE KEY(`legal_entity_id`, `country_id`, `domain_id`, `unit_id`, `user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


DROP TABLE IF EXISTS `tbl_compliance_applicability_chart`;
CREATE TABLE `tbl_compliance_applicability_chart` (
  `client_id` int(11) NOT NULL,
  `legal_entity_id` int(11) NOT NULL,
  `country_id` int(11) NOT NULL,
  `domain_id` int(11) NOT NULL,
  `unit_id` int(11) NOT NULL,
  `applicable_count` int(11) DEFAULT NULL,
  `not_applicable_count` int(11) DEFAULT NULL,
  `not_opted_count` int(11) DEFAULT NULL,
  `opted_count` int(11) DEFAULT NULL,
  UNIQUE KEY(`legal_entity_id`, `country_id`, `domain_id`, `unit_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


DROP TABLE IF EXISTS `tbl_reminder_settings`;
CREATE TABLE `tbl_reminder_settings` (
  `client_id` int(11) NOT NULL,
  `legal_entity_id` int(11) NOT NULL,
  `two_levels_of_approval` tinyint(1) DEFAULT '1',
  `assignee_reminder` int(11) DEFAULT '7',
  `escalation_reminder_in_advance` int(11) DEFAULT '7',
  `escalation_reminder` int(11) DEFAULT '7',
  `reassign_service_provider` int(11) DEFAULT '7',
  `created_by` int(11) DEFAULT NULL,
  `created_on` timestamp NULL DEFAULT NULL,
  `updated_by` int(11) DEFAULT NULL,
  `updated_on` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  UNIQUE KEY(`client_id`, `legal_entity_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
# client tables ends


DROP TABLE IF EXISTS `tbl_calender_view`;
CREATE TABLE `tbl_calender_view` (
  `legal_entity_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `year` int(11) NOT NULL,
  `month` int(11) NOT NULL,
  `date` int(11) NOT NULL,
  `due_date_count` int(11) DEFAULT NULL,
  `upcoming_count` int(11) DEFAULT NULL,
  UNIQUE KEY(`legal_entity_id`, `user_id`, `year`, `month`, `date`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
