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
  `legal_entity_id` int(11) NOT NULL,
  `domain_id` int(11) NOT NULL,
  `activation_date` timestamp NULL DEFAULT NULL,
  `organisation_id` int(11) NOT NULL,
  `count` int(11) NOT NULL,
  UNIQUE KEY(`legal_entity_id`, `domain_id`)
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
  UNIQUE KEY(`unit_id`, `client_id`, `legal_entity_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
CREATE TABLE `tbl_units_organizations` (
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
  UNIQUE KEY(`client_compliance_id`, `legal_entity_id`, `unit_id`, `domain_id`, `compliance_id`)
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
    UNIQUE KEY(`unit_id`, `domain_id`)
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
  `created_on` timestamp NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
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
  `is_active` tinyint(4) DEFAULT '1',
  `status_changed_on` timestamp NULL DEFAULT NULL,
  `is_disable` tinyint(4) DEFAULT '0',
  PRIMARY KEY (`user_id`),
  CONSTRAINT `category_fk2` FOREIGN KEY (`user_category_id`) REFERENCES `tbl_user_category` (`user_category_id`)
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
  `remarks` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`compliance_activity_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
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
CREATE TABLE `tbl_validity_date_settings` (
  `validity_date_id` int(11) NOT NULL AUTO_INCREMENT,
  `country_id` int(11) NOT NULL,
  `domain_id` int(11) NOT NULL,
  `days` int(11) NOT NULL,
  PRIMARY KEY (`validity_date_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
insert into tbl_audit_log values(0, 0);
INSERT INTO tbl_user_category VALUES(1, "Group Admin");
INSERT INTO tbl_user_category VALUES(2, "View Only");
INSERT INTO tbl_user_category VALUES(3, "Legal Entity Admin");
INSERT INTO tbl_user_category VALUES(4, "Domain Admin");
INSERT INTO tbl_user_category VALUES(5, "Client Executive");
INSERT INTO tbl_user_category VALUES(6, "Service Provider");
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
