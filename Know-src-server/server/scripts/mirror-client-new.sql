CREATE TABLE `tbl_audit_log` (
  `audit_trail_id` int(11) DEFAULT 0,
  `domain_trail_id` int(11) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
CREATE TABLE `tbl_user_category` (
  `user_category_id` int(11) NOT NULL,
  `user_category_name` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`user_category_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
CREATE TABLE `tbl_verification_type` (
  `verification_type_id` int(11) NOT NULL,
  `verification_type` varchar(50) NOT NULL,
  PRIMARY KEY (`verification_type_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
CREATE TABLE `tbl_compliance_frequency` (
  `frequency_id` int(11) NOT NULL,
  `frequency` varchar(20) NOT NULL,
  PRIMARY KEY (`frequency_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
CREATE TABLE `tbl_compliance_repeat_type` (
  `repeat_type_id` int(11) NOT NULL,
  `repeat_type` varchar(20) NOT NULL,
  PRIMARY KEY (`repeat_type_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
CREATE TABLE `tbl_compliance_duration_type` (
  `duration_type_id` int(11) NOT NULL,
  `duration_type` varchar(20) NOT NULL,
  PRIMARY KEY (`duration_type_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
CREATE TABLE `tbl_countries` (
  `country_id` int(11) NOT NULL,
  `country_name` varchar(50) NOT NULL,
  `is_active` tinyint(4) DEFAULT '1',
  PRIMARY KEY (`country_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
CREATE TABLE `tbl_domains` (
  `domain_id` int(11) NOT NULL,
  `domain_name` varchar(50) NOT NULL,
  `is_active` tinyint(4) DEFAULT '1',
  PRIMARY KEY (`domain_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
CREATE TABLE `tbl_domain_countries` (
  `country_id` int(11) NOT NULL,
  `domain_id` int(11) NOT NULL,
  UNIQUE KEY (`country_id`, `domain_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
CREATE TABLE `tbl_organisation` (
  `organisation_id` int(11) NOT NULL,
  `country_id` int(11) NOT NULL,
  `domain_id` int(11) NOT NULL,
  `organisation_name` varchar(50) NOT NULL,
  `is_active` tinyint(4) DEFAULT '1',
  PRIMARY KEY (`organisation_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
CREATE TABLE `tbl_client_groups` (
  `client_id` int(11) NOT NULL,
  `group_name` varchar(50) NOT NULL,
  `short_name` varchar(20) NOT NULL,
  `email_id` varchar(100) NOT NULL,
  `total_view_licence` int(11) DEFAULT NULL,
  `licence_used` int(11) DEFAULT NULL,
  PRIMARY KEY (`client_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
CREATE TABLE `tbl_business_groups` (
  `business_group_id` int(11) NOT NULL,
  `business_group_name` varchar(100) NOT NULL,
  PRIMARY KEY (`business_group_id`),
  UNIQUE KEY(`business_group_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
CREATE TABLE `tbl_legal_entities` (
  `legal_entity_id` int(11) NOT NULL,
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
  `is_closed` tinyint(4) DEFAULT '0',
  `closed_on` timestamp NULL DEFAULT NULL,
  `closed_by` int(11) DEFAULT NULL,
  `closed_remarks` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`legal_entity_id`),
  UNIQUE KEY(`legal_entity_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
CREATE TABLE `tbl_legal_entity_domains` (
  `le_domain_id` int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `legal_entity_id` int(11) NOT NULL,
  `domain_id` int(11) NOT NULL,
  `activation_date` timestamp NULL DEFAULT NULL,
  `organisation_id` int(11) NOT NULL,
  `count` int(11) NOT NULL,
  UNIQUE KEY(`legal_entity_id`, `domain_id`, `organisation_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
CREATE TABLE `tbl_divisions` (
  `division_id` int(11) NOT NULL,
  `division_name` varchar(100) DEFAULT NULL,
  `legal_entity_id` int(11) DEFAULT NULL,
  `business_group_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`division_id`),
  UNIQUE KEY(`division_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
CREATE TABLE `tbl_categories` (
  `category_id` int(11) NOT NULL,
  `category_name` varchar(100) DEFAULT NULL,
  `legal_entity_id` int(11) NOT NULL,
  `business_group_id` int(11) DEFAULT NULL,
  `division_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`category_id`),
  UNIQUE KEY(`category_id`, `legal_entity_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
CREATE TABLE `tbl_client_configuration` (
  `cn_config_id` int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `client_id` int(11) NOT NULL,
  `country_id` int(11) NOT NULL,
  `domain_id` int(11) NOT NULL,
  `month_from` int(11) NOT NULL,
  `month_to` int(11) NOT NULL,
  UNIQUE KEY(`country_id`, `domain_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
CREATE TABLE `tbl_units` (
  `unit_id` int(11) NOT NULL,
  `client_id` int(11) NOT NULL,
  `business_group_id` int(11) DEFAULT NULL,
  `legal_entity_id` int(11) NOT NULL,
  `division_id` int(11) DEFAULT NULL,
  `category_id` int(11) DEFAULT NULL,
  `country_id` int(11) NOT NULL,
  `geography_name` longtext NOT NULL,
  `unit_code` varchar(50) NOT NULL,
  `unit_name` varchar(50) NOT NULL,
  `address` varchar(250) NOT NULL,
  `postal_code` int(11) NOT NULL,
  `is_closed` tinyint(4) DEFAULT '0',
  `closed_on` timestamp NULL DEFAULT NULL,
  `closed_by` int(11) DEFAULT NULL,
  `closed_remarks` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`unit_id`),
  UNIQUE KEY(`unit_id`, `client_id`, `legal_entity_id`),
  KEY `in_unit_id` (`unit_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
CREATE TABLE `tbl_units_organizations` (
  `unit_org_id` int(11) NOT NULL,
  `unit_id` int(11) NOT NULL,
  `domain_id` int(11) NOT NULL,
  `organisation_id` int(11) DEFAULT NULL,
  UNIQUE KEY (`unit_id`, `domain_id`, `organisation_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
CREATE TABLE `tbl_compliances` (
  `compliance_id` int(11) NOT NULL,
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
  `statutory_nature` varchar(50) DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT '1',
  `status_changed_on` timestamp NULL DEFAULT NULL,
  `format_file` longtext,
  `format_file_size` float DEFAULT NULL,
  `statutory_mapping` longtext,
  PRIMARY KEY (`compliance_id`),
  UNIQUE KEY(`compliance_id`, `country_id`, `domain_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
CREATE TABLE `tbl_mapped_industries` (
  `statutory_mapping_id` int(11) NOT NULL,
  `organisation_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
CREATE TABLE `tbl_client_compliances` (
  `client_compliance_id` int(11) NOT NULL,
  `legal_entity_id` int(11) NOT NULL,
  `unit_id` int(11) NOT NULL,
  `domain_id` int(11) DEFAULT NULL,
  `statutory_name` varchar(150) DEFAULT NULL,
  `statutory_applicable_status` tinyint(4) DEFAULT '0',
  `statutory_opted_status` tinyint(4) DEFAULT NULL,
  `remarks` varchar(500) DEFAULT NULL,
  `compliance_id` int(11) NOT NULL,
  `compliance_applicable_status` tinyint(4) DEFAULT '0',
  `compliance_opted_status` tinyint(4) DEFAULT NULL,
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
  UNIQUE KEY(`client_compliance_id`, `legal_entity_id`, `unit_id`, `domain_id`, `compliance_id`),
  KEY `tbl_client_compliances_indx` (`compliance_id`),
  KEY `in_unit_id` (`unit_id`),
  KEY `in_domain_id` (`domain_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
CREATE TABLE `tbl_client_statutories`(
    `client_statutory_id` int(11) NOT NULL,
    `unit_id` int(11) NOT NULL,
    `domain_id` int(11) NOT NULL,
    `updated_by` int(11) DEFAULT NULL,
    `updated_on` timestamp NULL DEFAULT NULL,
    `is_locked` tinyint(4) DEFAULT '0',
    `locked_on` timestamp NULL DEFAULT NULL,
    `locked_by` int(11) DEFAULT NULL,
    UNIQUE KEY(`unit_id`, `domain_id`),
    KEY `in_client_statutory_id` (`client_statutory_id`),
    KEY `in_unit_id` (`unit_id`),
    KEY `in_domain_id` (`domain_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
CREATE TABLE `tbl_statutory_notifications` (
  `notification_id` int(11) NOT NULL,
  `notification_text` longtext,
  `compliance_id` int(11) NOT NULL,
  `created_by` int(11) DEFAULT NULL,
  `created_on` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`notification_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
CREATE TABLE `tbl_statutory_notifications_users` (
  `notification_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `is_read` tinyint(4) DEFAULT '0',
  UNIQUE KEY(`notification_id`, `user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
CREATE TABLE `tbl_notification_types` (
  `notification_type_id` int(11) NOT NULL,
  `notification_type` varchar(20) NOT NULL,
  PRIMARY KEY (`notification_type_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
CREATE TABLE `tbl_notifications_log` (
  `notification_id` int(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `country_id` int(11) DEFAULT NULL,
  `domain_id` int(11) DEFAULT NULL,
  `business_group_id` int(11) DEFAULT NULL,
  `legal_entity_id` int(11) DEFAULT NULL,
  `division_id` int(11) DEFAULT NULL,
  `unit_id` int(11) DEFAULT NULL,
  `compliance_id` int(11) DEFAULT NULL,
  `assignee` int(11) DEFAULT NULL,
  `concurrence_person` int(11) DEFAULT NULL,
  `approval_person` int(11) DEFAULT NULL,
  `notification_type_id` int(11) DEFAULT NULL,
  `notification_text` longtext,
  `extra_details` longtext,
  `created_on` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
CREATE TABLE tbl_notifications_user_log(
  `notification_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `read_status` tinyint(4) DEFAULT '0',
  `updated_on` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
CREATE TABLE `tbl_service_providers` (
  `service_provider_id` int(11) NOT NULL AUTO_INCREMENT,
  `service_provider_name` varchar(50) NOT NULL,
  `short_name` varchar(20) NOT NULL,
  `contract_from` date NOT NULL,
  `contract_to` date NOT NULL,
  `contact_person` varchar(50) NOT NULL,
  `contact_no` varchar(20) NOT NULL,
  `email_id` varchar(100) NOT NULL,
  `mobile_no` varchar(20) DEFAULT NULL,
  `address` varchar(500) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL DEFAULT '1',
  `status_changed_by` int(11) DEFAULT NULL,
  `status_changed_on` timestamp NULL DEFAULT NULL,
  `is_blocked` tinyint(1) NOT NULL DEFAULT '0',
  `blocked_by` int(11) DEFAULT NULL,
  `blocked_on` timestamp NULL DEFAULT NULL,
  `remarks` varchar(500) DEFAULT NULL,
  `created_by` int(11) NOT NULL,
  `created_on` timestamp NULL DEFAULT NULL,
  `updated_by` int(11) NOT NULL,
  `updated_on` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`service_provider_id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=latin1;
CREATE TABLE `tbl_users` (
  `user_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_category_id` int(11) NOT NULL,
  `client_id` int(11) DEFAULT NULL,
  `seating_unit_id` int(11) DEFAULT NULL,
  `service_provider_id` int(11) DEFAULT NULL,
  `user_level` int(11) DEFAULT NULL,
  `user_group_id` int(11) DEFAULT NULL,
  `email_id` varchar(100) NOT NULL,
  `employee_name` varchar(50) DEFAULT NULL,
  `employee_code` varchar(50) DEFAULT NULL,
  `contact_no` varchar(20) DEFAULT NULL,
  `mobile_no` varchar(20) DEFAULT NULL,
  `is_service_provider` tinyint(4) DEFAULT '0',
  `is_active` tinyint(4) DEFAULT '1',
  `status_changed_on` timestamp NULL DEFAULT NULL,
  `is_disable` tinyint(4) DEFAULT '0',
  `remarks` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`user_id`),
  CONSTRAINT `category_fk2` FOREIGN KEY (`user_category_id`) REFERENCES `tbl_user_category` (`user_category_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
CREATE TABLE `tbl_user_legal_entities` (
  `user_id` int(11) NOT NULL,
  `legal_entity_id` int(11) NOT NULL,
  UNIQUE KEY (`user_id`, `legal_entity_id`)
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
CREATE TABLE `tbl_mobile_registration` (
  `registration_key` varchar(50) NOT NULL,
  `device_type_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`registration_key`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
CREATE TABLE `tbl_unit_closure` (
  `client_id` int(11) NOT NULL,
  `legal_entity_id` int(11) NOT NULL,
  `unit_id` int(11) NOT NULL,
  `is_closed` tinyint(4) DEFAULT '0',
  `closed_on` timestamp NULL DEFAULT NULL,
  `closed_by` int(11) DEFAULT NULL,
  `remarks` varchar(500) DEFAULT NULL,
  CONSTRAINT `legal_fk1` FOREIGN KEY (`legal_entity_id`) REFERENCES `tbl_legal_entities` (`legal_entity_id`),
  CONSTRAINT `unit_fk2` FOREIGN KEY (`unit_id`) REFERENCES `tbl_units` (`unit_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
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
CREATE TABLE `tbl_assign_compliances` (
  `legal_entity_id` int(11) NOT NULL,
  `country_id` int(11) NOT NULL,
  `domain_id` int(11) NOT NULL,
  `unit_id` int(11) NOT NULL,
  `compliance_id` int(11) NOT NULL,
  `statutory_dates` longtext NOT NULL,
  `repeats_type_id` int(11) DEFAULT NULL,
  `repeats_every` int(11) DEFAULT NULL,
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
  `is_active` tinyint(4) DEFAULT '1',
  CONSTRAINT `legalentity_fk1` FOREIGN KEY (`legal_entity_id`) REFERENCES `tbl_legal_entities` (`legal_entity_id`),
  CONSTRAINT `country_fk2` FOREIGN KEY (`country_id`) REFERENCES `tbl_countries` (`country_id`),
  CONSTRAINT `domain_fk3` FOREIGN KEY (`domain_id`) REFERENCES `tbl_domains` (`domain_id`),
  CONSTRAINT `unit_fk4` FOREIGN KEY (`unit_id`) REFERENCES `tbl_units` (`unit_id`),
  CONSTRAINT `compid_fk5` FOREIGN KEY (`compliance_id`) REFERENCES `tbl_compliances` (`compliance_id`),
  UNIQUE KEY(`unit_id`, `domain_id`, `compliance_id`, `assignee`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
CREATE TABLE `tbl_reassigned_compliances_history` (
  `reassign_history_id` int(11) NOT NULL AUTO_INCREMENT,
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
  PRIMARY KEY (`reassign_history_id`),
  CONSTRAINT `r_unit_fk1` FOREIGN KEY (`unit_id`) REFERENCES `tbl_units` (`unit_id`),
  CONSTRAINT `r_compliance_fk2` FOREIGN KEY (`compliance_id`) REFERENCES `tbl_compliances` (`compliance_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
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
  `occurrence_remarks` varchar(500) DEFAULT NULL,
  `remarks` varchar(500) DEFAULT NULL,
  `completed_by` int(11) NOT NULL,
  `completed_on` datetime DEFAULT NULL,
  `concurrence_status` varchar(20) DEFAULT NULL,
  `concurred_by` int(11) DEFAULT NULL,
  `concurred_on` datetime DEFAULT NULL,
  `approve_status` varchar(20) DEFAULT NULL,
  `approved_by` int(11) NOT NULL,
  `approved_on` datetime DEFAULT NULL,
  `current_status` tinyint(4) DEFAULT '0',
  PRIMARY KEY (`compliance_history_id`),
  CONSTRAINT `ch_unit_fk11` FOREIGN KEY (`unit_id`) REFERENCES `tbl_units` (`unit_id`),
  CONSTRAINT `ch_compliance_fk12` FOREIGN KEY (`compliance_id`) REFERENCES `tbl_compliances` (`compliance_id`),
  UNIQUE KEY(`unit_id`, `compliance_id`, `start_date`, `due_date`, `next_due_date`, `completed_by`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
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
CREATE TABLE `tbl_compliance_activity_log` (
  `compliance_activity_id` int(11) NOT NULL AUTO_INCREMENT,
  `unit_id` int(11) DEFAULT NULL,
  `compliance_id` int(11) DEFAULT NULL,
  `compliance_history_id` int(11) DEFAULT NULL,
  `activity_by` int(11) DEFAULT NULL,
  `activity_on` timestamp NULL DEFAULT NULL,
  `action` varchar(500) DEFAULT NULL,
  `remarks` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`compliance_activity_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
CREATE TABLE `tbl_compliance_status_chart_unitwise` (
  `legal_entity_id` int(11) NOT NULL,
  `country_id` int(11) NOT NULL,
  `domain_id` int(11) NOT NULL,
  `unit_id` int(11) NOT NULL,
  `complied_count` int(11) DEFAULT NULL,
  `delayed_count` int(11) DEFAULT NULL,
  `inprogress_count` int(11) DEFAULT NULL,
  `overdue_count` int(11) DEFAULT NULL,
  `chart_year` int(11) DEFAULT NULL,
  `month_from` int(11) DEFAULT NULL,
  `month_to` int(11) DEFAULT NULL,
  UNIQUE KEY(`legal_entity_id`, `country_id`, `domain_id`, `unit_id`, `chart_year`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
CREATE TABLE `tbl_compliance_status_chart_userwise` (
  `legal_entity_id` int(11) NOT NULL,
  `country_id` int(11) NOT NULL,
  `domain_id` int(11) NOT NULL,
  `unit_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `complied_count` int(11) DEFAULT NULL,
  `delayed_count` int(11) DEFAULT NULL,
  `inprogress_count` int(11) DEFAULT NULL,
  `overdue_count` int(11) DEFAULT NULL,
  `chart_year` int(11) DEFAULT NULL,
  `month_from` int(11) DEFAULT NULL,
  `month_to` int(11) DEFAULT NULL,
  UNIQUE KEY(`legal_entity_id`, `country_id`, `domain_id`, `unit_id`, `user_id`, `chart_year`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
CREATE TABLE `tbl_notcomplied_chart_unitwise` (
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
CREATE TABLE `tbl_notcomplied_chart_userwise` (
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
CREATE TABLE `tbl_compliance_applicability_chart` (
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
CREATE TABLE `tbl_calendar_view` (
  `legal_entity_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `year` int(11) NOT NULL,
  `month` int(11) NOT NULL,
  `date` int(11) NOT NULL,
  `due_date_count` int(11) DEFAULT NULL,
  `upcoming_count` int(11) DEFAULT NULL,
  UNIQUE KEY(`legal_entity_id`, `user_id`, `year`, `month`, `date`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
CREATE TABLE `tbl_validity_date_settings` (
  `validity_date_id` int(11) NOT NULL AUTO_INCREMENT,
  `country_id` int(11) NOT NULL,
  `domain_id` int(11) NOT NULL,
  `days` int(11) NOT NULL,
  PRIMARY KEY (`validity_date_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
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
CREATE TABLE `tbl_form_type` (
  `form_type_id` int(11) NOT NULL,
  `form_type` varchar(20) NOT NULL,
  PRIMARY KEY (`form_type_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
CREATE TABLE `tbl_forms` (
  `form_id` int(11) NOT NULL,
  `form_type_id` int(11) NOT NULL,
  `form_name` varchar(50) NOT NULL,
  `form_url` varchar(50) NOT NULL,
  `form_order` int(11) NOT NULL,
  `parent_menu` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`form_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
insert into tbl_audit_log values(0, 0);
INSERT INTO tbl_user_category VALUES(1, "Group Admin");
INSERT INTO tbl_user_category VALUES(2, "View Only");
INSERT INTO tbl_user_category VALUES(3, "Legal Entity Admin");
INSERT INTO tbl_user_category VALUES(4, "Domain Admin");
INSERT INTO tbl_user_category VALUES(5, "Client Executive");
INSERT INTO tbl_user_category VALUES(6, "Service Provider User");
-- tbl_compliance_duration_type
INSERT INTO tbl_compliance_duration_type VALUES(1, "Day(s)");
INSERT INTO tbl_compliance_duration_type VALUES(2, "Hour(s)");
INSERT INTO tbl_compliance_duration_type VALUES(3, "Month(s)");
-- tbl_compliance_repeat_type
INSERT INTO tbl_compliance_repeat_type VALUES(1, "Day(s)");
INSERT INTO tbl_compliance_repeat_type VALUES(2, "Month(s)");
INSERT INTO tbl_compliance_repeat_type VALUES(3, "Year(s)");
-- tbl_compliance_frequency
INSERT INTO tbl_compliance_frequency VALUES(1, "One Time");
INSERT INTO tbl_compliance_frequency VALUES(2, "Periodical");
INSERT INTO tbl_compliance_frequency VALUES(3, "Review");
INSERT INTO tbl_compliance_frequency VALUES(4, "Flexi Review");
INSERT INTO tbl_compliance_frequency VALUES(5, "On Occurrence");
INSERT INTO tbl_notification_types VALUES(1, "Notification");
INSERT INTO tbl_notification_types VALUES(2, "Reminder");
INSERT INTO tbl_notification_types VALUES(3, "Escalation");
INSERT INTO tbl_notification_types VALUES(4, "Messages");
INSERT INTO tbl_forms VALUES(1, 1, 'Service Provider', "/service-provider", 1, null);
INSERT INTO tbl_forms VALUES(2, 1, 'User Privileges', "/client-user-privilege", 2, null);
INSERT INTO tbl_forms VALUES(3, 1, 'User Management', "/client-user-management", 3, null);
INSERT INTO tbl_forms VALUES(4, 1, 'Unit Closure', "/unit-closure", 4, null);
INSERT INTO tbl_forms VALUES(5, 2, 'Statutory Settings', "/statutory-settings", 5, null);
INSERT INTO tbl_forms VALUES(6, 2, 'Review Settings', "/review-settings", 6, null);
INSERT INTO tbl_forms VALUES(7, 2, 'Assign Compliance', "/assign-compliance", 7, null);
INSERT INTO tbl_forms VALUES(8, 2, 'Reassign Compliance', "/reassign-compliance", 8, null);
INSERT INTO tbl_forms VALUES(9, 2, 'Compliance Approval', "/compliance-approval", 9, null);
INSERT INTO tbl_forms VALUES(10, 2, 'Completed Task - Current Year', "/completed-tasks-current-year", 10, null);
INSERT INTO tbl_forms VALUES(11, 2, 'On Occurrence Compliances', "/on-occurrence-compliances", 11, null);
INSERT INTO tbl_forms VALUES(12, 3, 'Legal Entity Wise Report', "/legal-entity-wise-report", 12, null);
INSERT INTO tbl_forms VALUES(13, 3, 'Domain Wise Report', "/domain-wise-report", 13, null);
INSERT INTO tbl_forms VALUES(14, 3, 'Unit Wise Compliance', "/unit-wise-compliance", 14, null);
INSERT INTO tbl_forms VALUES(15, 3, 'Service Provider Wise Compliance', "/service-provider-wise-compliance", 15, null);
INSERT INTO tbl_forms VALUES(16, 3, 'User Wise Compliance', "/user-wise-compliance", 16, null);
INSERT INTO tbl_forms VALUES(17, 3, 'Status Report Consolidated', "/status-report-consolidated", 17, null);
INSERT INTO tbl_forms VALUES(18, 3, 'Domain Score Card', "/domain-score-card", 18, "Score Card");
INSERT INTO tbl_forms VALUES(19, 3, 'Legal Entity Wise Score Card', "/legal-entity-wise-score-card", 19, "Score Card");
INSERT INTO tbl_forms VALUES(20, 3, 'Work Flow Score Card', "/work-flow-score-card", 20, "Score Card");
INSERT INTO tbl_forms VALUES(21, 3, 'Statutory Settings Unit Wise Report', "/statutory-settings-unit-wise-report", 21, null);
INSERT INTO tbl_forms VALUES(22, 3, 'Reassigned History Report', "/reassigned-history-report", 22, null);
INSERT INTO tbl_forms VALUES(23, 3, 'Risk Report', "/risk-report", 23, null);
INSERT INTO tbl_forms VALUES(24, 3, 'Unit List', "/unit-list", 24, null);
INSERT INTO tbl_forms VALUES(25, 3, 'Statutory Notification List', "/statutory-notification-list", 25, null);
INSERT INTO tbl_forms VALUES(26, 3, 'Service Provider Details', "/service-provider-details", 26, null);
INSERT INTO tbl_forms VALUES(27, 3, 'Audit Trail', "/audit-trail", 27, null);
INSERT INTO tbl_forms VALUES(28, 3, 'Login Trace', "/login-trace", 28, null);
INSERT INTO tbl_forms VALUES(29, 4, 'View Profile', "/view-profile", 29, null);
INSERT INTO tbl_forms VALUES(31, 4, 'Change Password', "/change-password", 31, null);
INSERT INTO tbl_forms VALUES(32, 4, 'Settings', "/settings", 32, null);
INSERT INTO tbl_forms VALUES(33, 4, 'Themes', "/themes", 33, null);
INSERT INTO tbl_forms VALUES(34, 5, 'Dashboard', "/dashboard", 34, null);
INSERT INTO tbl_forms VALUES(35, 2, 'Compliance Task Details', "/compliance-task-details", 35, null);
INSERT INTO tbl_forms VALUES(36, 4, 'Reminders', "/reminders", 36, null);
INSERT INTO tbl_forms VALUES(37, 4, 'Statutory Notifications', "/statutory-notifications", 37, null);
INSERT INTO tbl_forms VALUES(38, 4, 'Escalations', "/escalations", 38, null);
INSERT INTO tbl_forms VALUES(39, 4, 'Messages', "/messages", 39, null);
