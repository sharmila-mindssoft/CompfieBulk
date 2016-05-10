DROP TABLE IF EXISTS `tbl_audit_log`;
CREATE TABLE `tbl_audit_log` (
  `audit_trail_id` int(11) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
DROP TABLE IF EXISTS `tbl_form_type`;
CREATE TABLE `tbl_form_type` (
  `form_type_id` int(11) NOT NULL,
  `form_type` varchar(50) NOT NULL,
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
  `is_admin` tinyint(4) NOT NULL,
  PRIMARY KEY (`form_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
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
DROP TABLE IF EXISTS `tbl_compliance_frequency`;
CREATE TABLE `tbl_compliance_frequency` (
  `frequency_id` int(11) NOT NULL,
  `frequency` varchar(50) NOT NULL,
  PRIMARY KEY (`frequency_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
DROP TABLE IF EXISTS `tbl_compliance_repeat_type`;
CREATE TABLE `tbl_compliance_repeat_type` (
  `repeat_type_id` int(11) NOT NULL,
  `repeat_type` varchar(50) NOT NULL,
  PRIMARY KEY (`repeat_type_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
DROP TABLE IF EXISTS `tbl_compliance_duration_type`;
CREATE TABLE `tbl_compliance_duration_type` (
  `duration_type_id` int(11) NOT NULL,
  `duration_type` varchar(50) NOT NULL,
  PRIMARY KEY (`duration_type_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
DROP TABLE IF EXISTS `tbl_compliances`;
CREATE TABLE `tbl_compliances` (
  `compliance_id` int(11) NOT NULL,
  `domain_id` int(11) NOT NULL,
  `frequency_id` int(11) NOT NULL,
  `repeats_type_id` int(11) NOT NULL,
  `duration_type_id` int(11) NOT NULL,
  `statutory_mapping` varchar(500) NOT NULL,
  `statutory_provision` varchar(250) NOT NULL,
  `compliance_task` varchar(100) NOT NULL,
  `compliance_description` longtext NOT NULL,
  `document_name` varchar(100) DEFAULT NULL,
  `format_file` varchar(100) DEFAULT NULL,
  `format_file_size` float DEFAULT NULL,
  `penal_consequences` longtext DEFAULT NULL,
  `statutory_dates` longtext NOT NULL,
  `repeats_every` int(11)  NOT NULL,
  `duration` int(11)  NOT NULL,
  `is_active` tinyint(4) DEFAULT 1,
  PRIMARY KEY (`compliance_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
DROP TABLE IF EXISTS `tbl_client_groups`;
CREATE TABLE `tbl_client_groups` (
  `client_id` int(11) NOT NULL,
  `group_name` varchar(50) NOT NULL,
  `logo_url` varchar(200) NOT NULL,
  `logo_size` float(11) NOT NULL,
  `contract_from` date NOT NULL,
  `contract_to` date NOT NULL,
  `no_of_user_licence` int(11) NOT NULL,
  `total_disk_space` float(11) NOT NULL,
  `total_disk_space_used` float(11) DEFAULT 0.0,
  `url_short_name` varchar(20) DEFAULT NULL,
  `is_sms_subscribed` tinyint(1) DEFAULT 0,
  `two_levels_of_approval` tinyint(1) DEFAULT 1,
  `assignee_reminder` int(11) DEFAULT 7,
  `escalation_reminder_in_advance` int(11) DEFAULT 7,
  `escalation_reminder` int(11) DEFAULT 7,
  `updated_on` TIMESTAMP NOT NULL DEFAULT current_timestamp on update current_timestamp
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
DROP TABLE IF EXISTS `tbl_client_configurations`;
CREATE TABLE `tbl_client_configurations` (
  `client_config_id` int(11) NOT NULL,
  `country_id` int(11) NOT NULL,
  `domain_id` int(11) NOT NULL,
  `period_from` int(11) NOT NULL,
  `period_to` int(11) NOT NULL,
  PRIMARY KEY (`country_id`, `domain_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
DROP TABLE IF EXISTS `tbl_business_groups`;
CREATE TABLE `tbl_business_groups` (
  `business_group_id` int(11) NOT NULL,
  `business_group_name` varchar(100) NOT NULL,
  PRIMARY KEY (`business_group_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
DROP TABLE IF EXISTS `tbl_legal_entities`;
CREATE TABLE `tbl_legal_entities` (
  `legal_entity_id` int(11) NOT NULL,
  `business_group_id` int(11) DEFAULT NULL,
  `legal_entity_name` varchar(100) NOT NULL,
  PRIMARY KEY (`legal_entity_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
DROP TABLE IF EXISTS `tbl_divisions`;
CREATE TABLE `tbl_divisions` (
  `division_id` int(11) NOT NULL,
  `business_group_id` int(11) DEFAULT NULL,
  `legal_entity_id` int(11) NOT NULL,
  `division_name` varchar(100) NOT NULL,
  PRIMARY KEY (`division_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
DROP TABLE IF EXISTS `tbl_units`;
CREATE TABLE `tbl_units` (
  `unit_id` int(11) NOT NULL,
  `business_group_id` int(11) DEFAULT NULL,
  `legal_entity_id` int(11) NOT NULL,
  `division_id` int(11) DEFAULT NULL,
  `country_id` int(11) NOT NULL,
  `geography` longtext NOT NULL,
  `unit_code` varchar(50) NOT NULL,
  `unit_name` varchar(50) NOT NULL,
  `industry_name` varchar(50) NOT NULL,
  `address` varchar(500) NOT NULL,
  `postal_code` int(11) NOT NULL,
  `domain_ids` varchar(100) NOT NULL,
  `is_active` tinyint(1) DEFAULT '1',
  `is_closed` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`unit_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
DROP TABLE IF EXISTS `tbl_service_providers`;
CREATE TABLE `tbl_service_providers` (
  `service_provider_id` int(11) NOT NULL,
  `service_provider_name` varchar(50) NOT NULL,
  `address` varchar(500) DEFAULT NULL,
  `contract_from` date DEFAULT NULL,
  `contract_to` date DEFAULT NULL,
  `contact_person` varchar(50) DEFAULT NULL,
  `contact_no` varchar(20) DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT 1,
  `created_by` int(11) DEFAULT NULL,
  `created_on` timestamp NULL DEFAULT NULL,
  `updated_by` int(11) DEFAULT NULL,
  `updated_on` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`service_provider_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
DROP TABLE IF EXISTS `tbl_user_groups`;
CREATE TABLE `tbl_user_groups` (
  `user_group_id` int(11) NOT NULL,
  `user_group_name` varchar(50) DEFAULT NULL,
  `form_ids` longtext,
  `is_active` tinyint(4) DEFAULT '1',
  `created_by` int(11) DEFAULT NULL,
  `created_on` timestamp NULL DEFAULT NULL,
  `updated_by` int(11) DEFAULT NULL,
  `updated_on` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`user_group_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
DROP TABLE IF EXISTS `tbl_admin`;
CREATE TABLE `tbl_admin` (
  `admin_id` int(11) NOT NULL DEFAULT 0,
  `username` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
DROP TABLE IF EXISTS `tbl_users`;
CREATE TABLE `tbl_users` (
  `user_id` int(11) NOT NULL,
  `user_group_id` int(11) DEFAULT NULL,
  `service_provider_id` int(11) DEFAULT NULL,
  `email_id` varchar(100) NOT NULL,
  `password` varchar(50) NOT NULL,
  `employee_name` varchar(50) DEFAULT NULL,
  `employee_code` varchar(50) DEFAULT NULL,
  `contact_no` varchar(20) DEFAULT NULL,
  `seating_unit_id` int(11) DEFAULT NULL,
  `user_level` int(11) DEFAULT NULL,
  `is_admin` tinyint(4) DEFAULT 0,
  `is_primary_admin` tinyint(4) DEFAULT 0,
  `is_service_provider` tinyint(4) DEFAULT NULL,
  `is_active` tinyint(4) DEFAULT 1,
  `created_by` int(11) DEFAULT NULL,
  `created_on` timestamp NULL DEFAULT NULL,
  `updated_by` int(11) DEFAULT NULL,
  `updated_on` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
DROP TABLE IF EXISTS `tbl_user_countries`;
CREATE TABLE `tbl_user_countries` (
  `user_id` int(11) NOT NULL,
  `country_id` int(11) NOT NULL,
  PRIMARY KEY (`country_id`,`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
DROP TABLE IF EXISTS `tbl_user_domains`;
CREATE TABLE `tbl_user_domains` (
  `user_id` int(11) NOT NULL,
  `domain_id` int(11) NOT NULL,
  PRIMARY KEY (`domain_id`,`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
DROP TABLE IF EXISTS `tbl_user_units`;
CREATE TABLE `tbl_user_units` (
  `user_id` int(11) NOT NULL,
  `unit_id` int(11) NOT NULL,
  PRIMARY KEY (`unit_id`,`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
DROP TABLE IF EXISTS `tbl_user_login_history`;
CREATE TABLE `tbl_user_login_history` (
  `user_id` int(11) NOT NULL,
  `login_time` int(11) DEFAULT NULL,
  `logout_time` int(11) DEFAULT NULL,
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
  PRIMARY KEY (`session_token`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
DROP TABLE IF EXISTS `tbl_client_statutories`;
CREATE TABLE `tbl_client_statutories` (
  `client_statutory_id` int(11) NOT NULL,
  `geography` VARCHAR(50) NOT NULL,
  `country_id` int(11) NOT NULL,
  `domain_id` int(11) NOT NULL,
  `unit_id` int(11) NOT NULL,
  `is_new` tinyint(4) DEFAULT 0,
  PRIMARY KEY (`client_statutory_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
DROP TABLE IF EXISTS `tbl_client_compliances`;
CREATE TABLE `tbl_client_compliances` (
  `client_compliance_id` int(11) NOT  NULL,
  `client_statutory_id` int(11) NOT NULL,
  `compliance_id` int(11) NOT NULL,
  `statutory_applicable` tinyint(4) DEFAULT NULL,
  `statutory_opted` tinyint(4) DEFAULT NULL,
  `not_applicable_remarks` varchar(250) DEFAULT NULL,
  `compliance_applicable` tinyint(4) DEFAULT NULL,
  `compliance_opted` tinyint(4) DEFAULT NULL,
  `compliance_remarks` varchar(250) DEFAULT NULL,
  `submitted_on` timestamp NULL DEFAULT '0000-00-00 00:00:00',
  `created_by` int(11) DEFAULT NULL,
  `created_on` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `updated_by` int(11) DEFAULT NULL,
  `updated_on` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`client_compliance_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tbl_assigned_compliances`;
CREATE TABLE `tbl_assigned_compliances` (
  `country_id` int(11) NOT NULL,
  `unit_id` int(11) DEFAULT NULL,
  `compliance_id` int(11) DEFAULT NULL,
  `statutory_dates` longtext NOT NULL,
  `assignee` int(11) DEFAULT NULL,
  `concurrence_person` int(11) DEFAULT NULL,
  `approval_person` int(11) DEFAULT NULL,
  `trigger_before_days` int(11) DEFAULT NULL,
  `due_date` date DEFAULT NULL,
  `validity_date` date DEFAULT NULL,
  `is_reassigned` tinyint(4) DEFAULT NULL,
  `is_active` tinyint(4) DEFAULT 1,
  `created_by` int(11) DEFAULT NULL,
  `created_on` timestamp NULL DEFAULT NULL,
  `updated_by` int(11) DEFAULT NULL,
  `updated_on` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`unit_id`, `compliance_id`)
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
  `updated_on` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
DROP TABLE IF EXISTS `tbl_compliance_status`;
CREATE TABLE `tbl_compliance_status` (
  `compliance_status_id` int(11) NOT NULL,
  `compliance_status` varchar(20) NOT NULL,
  PRIMARY KEY (`compliance_status_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
DROP TABLE IF EXISTS `tbl_approval_status`;
CREATE TABLE `tbl_approval_status` (
  `approval_status_id` int(11) NOT NULL,
  `approval_status` varchar(20) NOT NULL,
  PRIMARY KEY (`approval_status_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
DROP TABLE IF EXISTS `tbl_compliance_history`;
CREATE TABLE `tbl_compliance_history` (
  `compliance_history_id` int(11) NOT NULL,
  `unit_id` int(11) DEFAULT NULL,
  `compliance_id` int(11) DEFAULT NULL,
  `start_date` datetime DEFAULT NULL,
  `due_date` datetime DEFAULT NULL,
  `completion_date` datetime DEFAULT NULL,
  `documents` longtext,
  `document_size` int(11) DEFAULT NULL,
  `validity_date` datetime DEFAULT NULL,
  `next_due_date` datetime DEFAULT NULL,
  `remarks` varchar(500) DEFAULT NULL,
  `completed_by` int(11) DEFAULT NULL,
  `completed_on` datetime DEFAULT NULL,
  `concurrence_status` varchar(20) DEFAULT NULL,
  `concurred_by` int(11) DEFAULT NULL,
  `concurred_on` datetime DEFAULT NULL,
  `approve_status` varchar(20) DEFAULT NULL,
  `approved_by` int(11) DEFAULT NULL,
  `approved_on` datetime DEFAULT NULL,
  PRIMARY KEY (`compliance_history_id`)
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
  `updated_on` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`compliance_activity_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
DROP TABLE IF EXISTS `tbl_activity_log`;
CREATE TABLE `tbl_activity_log` (
  `activity_log_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `form_id` int(11) NOT NULL,
  `action` varchar(500) NOT NULL,
  `created_on` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`activity_log_id`)
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
  PRIMARY KEY (`registration_key`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
DROP TABLE IF EXISTS `tbl_statutory_notifications_log`;
CREATE TABLE `tbl_statutory_notifications_log` (
  `statutory_notification_id` int(11) NOT NULL,
  `country_name` VARCHAR(50) NOT NULL,
  `domain_name` VARCHAR(50) NOT NULL,
  `industry_name` VARCHAR(50) NOT NULL,
  `statutory_nature` VARCHAR(50) NOT NULL,
  `statutory_provision` longtext,
  `applicable_location` longtext,
  `notification_text` longtext,
  `updated_on` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`statutory_notification_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
DROP TABLE IF EXISTS `tbl_statutory_notifications_units`;
CREATE TABLE `tbl_statutory_notifications_units` (
  `statutory_notification_unit_id` int(11) NOT NULL,
  `statutory_notification_id` int(11) NOT NULL,
  `business_group_id` int(11) NOT NULL,
  `legal_entity_id` int(11) NOT NULL,
  `division_id` int(11) NOT NULL,
  `unit_id` int(11) NOT NULL,
  PRIMARY KEY (`statutory_notification_id`, `business_group_id`, `legal_entity_id`, `division_id`, `unit_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
DROP TABLE IF EXISTS `tbl_statutory_notification_status`;
CREATE TABLE `tbl_statutory_notification_status` (
  `statutory_notification_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `read_status` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
DROP TABLE IF EXISTS `tbl_notification_type`;
CREATE TABLE `tbl_notification_types` (
  `notification_type_id` int(11) NOT NULL,
  `notification_type` varchar(20) NOT NULL,
  PRIMARY KEY (`notification_type_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
DROP TABLE IF EXISTS `tbl_notifications_log`;
CREATE TABLE `tbl_notifications_log` (
  `notification_id` int(11) NOT NULL,
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
  `created_on` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`notification_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
DROP TABLE IF EXISTS `tbl_notification_user_log`;
CREATE TABLE `tbl_notification_user_log` (
  `notification_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `read_status` tinyint(1) DEFAULT '0',
  `updated_on` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
DROP TABLE IF EXISTS `tbl_mobile_sync_versions`;
CREATE TABLE `tbl_mobile_sync_versions` (
  `unit_details_version` int(11) NOT NULL,
  `user_details_version` int(11) NOT NULL,
  `compliance_applicability_version` int(11) NOT NULL,
  `compliance_history_version` int(11) NOT NULL,
  `reassign_history_version` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
ALTER TABLE `tbl_compliances` ADD INDEX `ccompliance_id_domain_id_idx` (`compliance_id`, `domain_id`);
ALTER TABLE `tbl_client_statutories` ADD CONSTRAINT `fk_client_unit_id` FOREIGN KEY (`unit_id`) REFERENCES `tbl_units` (`unit_id`) ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE `tbl_client_statutories` ADD INDEX `country_idx` (`country_id`);
ALTER TABLE `tbl_client_statutories` ADD INDEX `domain_idx` (`domain_id`);
ALTER TABLE `tbl_client_compliances` ADD CONSTRAINT `fk_client_statutory_id` FOREIGN KEY (`client_statutory_id`) REFERENCES `tbl_client_statutories` (`client_statutory_id`) ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE `tbl_client_compliances` ADD CONSTRAINT `fk_compliance_id` FOREIGN KEY (`compliance_id`) REFERENCES `tbl_compliances` (`compliance_id`) ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE `tbl_assigned_compliances` ADD CONSTRAINT `fk_assign_compliance_id` FOREIGN KEY (`compliance_id`) REFERENCES `tbl_compliances` (`compliance_id`) ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE `tbl_assigned_compliances` ADD CONSTRAINT `fk_assign_unit_id` FOREIGN KEY (`unit_id`) REFERENCES `tbl_units` (`unit_id`) ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE `tbl_assigned_compliances` ADD UNIQUE INDEX `compliance_id_unit_id_idx` (`unit_id`, `compliance_id`);
ALTER TABLE `tbl_compliance_history` ADD CONSTRAINT `fk_history_compliance_id` FOREIGN KEY (`compliance_id`) REFERENCES `tbl_compliances` (`compliance_id`) ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE `tbl_compliance_history` ADD CONSTRAINT `fk_history_unit_id` FOREIGN KEY (`unit_id`) REFERENCES `tbl_units` (`unit_id`) ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE `tbl_compliance_history` ADD INDEX `hisoty_compliance_id_unit_id_idx` (`unit_id`, `compliance_id`);
ALTER TABLE `tbl_reassigned_compliances_history` ADD CONSTRAINT `fk_reassign_compliance_id` FOREIGN KEY (`compliance_id`) REFERENCES `tbl_compliances` (`compliance_id`) ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE `tbl_reassigned_compliances_history` ADD CONSTRAINT `fk_reassign_unit_id` FOREIGN KEY (`unit_id`) REFERENCES `tbl_units` (`unit_id`) ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE `tbl_reassigned_compliances_history` ADD INDEX `reassign_compliance_id_unit_id_idx` (`unit_id`, `compliance_id`);
ALTER TABLE `tbl_notifications_log` ADD CONSTRAINT `fk_notification_compliance_id` FOREIGN KEY (`compliance_id`) REFERENCES `tbl_compliances` (`compliance_id`) ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE `tbl_notifications_log` ADD CONSTRAINT `fk_notification_unit_id` FOREIGN KEY (`unit_id`) REFERENCES `tbl_units` (`unit_id`) ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE `tbl_notifications_log` ADD INDEX `notification_compliance_id_unit_id_idx` (`unit_id`, `compliance_id`);
ALTER TABLE `tbl_notification_user_log` ADD CONSTRAINT `fk_notification_id` FOREIGN KEY (`notification_id`) REFERENCES `tbl_notifications_log` (`notification_id`) ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE `tbl_statutory_notification_status` ADD CONSTRAINT `fk_statutory_notification_id` FOREIGN KEY (`statutory_notification_id`) REFERENCES `tbl_statutory_notifications_log` (`statutory_notification_id`) ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE `tbl_statutory_notification_status` ADD INDEX `user_id_idx` (`user_id`);
ALTER TABLE `tbl_statutory_notifications_units` ADD CONSTRAINT `fk_statutory_notify_unit_id` FOREIGN KEY (`statutory_notification_id`) REFERENCES `tbl_statutory_notifications_log` (`statutory_notification_id`) ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE `tbl_statutory_notifications_units` ADD CONSTRAINT `fk_notify_unit_id` FOREIGN KEY (`unit_id`) REFERENCES `tbl_units` (`unit_id`) ON DELETE NO ACTION ON UPDATE NO ACTION;
INSERT INTO tbl_audit_log VALUES(0);
INSERT INTO tbl_form_type VALUES(1, "Home");
INSERT INTO tbl_form_type VALUES(2, "Master");
INSERT INTO tbl_form_type VALUES(3, "Transaction");
INSERT INTO tbl_form_type VALUES(4, "Report");
INSERT INTO tbl_form_type VALUES(5, "Settings");
INSERT INTO tbl_forms VALUES(1, 1, 'Dashboard', '/home', 1, null, 0);
INSERT INTO tbl_forms VALUES(2, 2, 'Service Provider', '/service-provider', 2, null, 1);
INSERT INTO tbl_forms VALUES(3, 2, 'User Privilege', '/client-user-privilege', 3, null, 1);
INSERT INTO tbl_forms VALUES(4, 2, 'User', '/client-user-master', 4, null, 1);
INSERT INTO tbl_forms VALUES(5, 2, 'Unit Closure', '/unit-closure', 5, null, 1);
INSERT INTO tbl_forms VALUES(6, 3, 'Statutory Settings', '/statutory-settings', 6, null, 1);
INSERT INTO tbl_forms VALUES(7, 3, 'Assign Compliance', '/assign-compliance', 7, null, 1);
INSERT INTO tbl_forms VALUES(8, 3, 'Reassign Compliance', '/reassign-compliance', 8, null, 1);
INSERT INTO tbl_forms VALUES(9, 3, 'Compliance Approval', '/compliance-approval', 9, null, 0);
INSERT INTO tbl_forms VALUES(10, 3, 'Completed Tasks - Current Year', '/completed-tasks-current-year', 10, null, 0);
INSERT INTO tbl_forms VALUES(11, 3, 'Compliance Task Details', '/compliance-task-details',11, null, 0);
INSERT INTO tbl_forms VALUES(12, 3, 'On Occurrence Compliances', '/on-occurrence-compliances', 12, null, 0);
INSERT INTO tbl_forms VALUES(13, 4, 'Compliance Details', '/compliance-details', 13, null, 0);
INSERT INTO tbl_forms VALUES(14, 4, 'Risk Report', '/risk-report', 14, null, 0);
INSERT INTO tbl_forms VALUES(15, 4, 'Service Provider Wise Compliance', '/service-provider-wise-compliance', 15, "Compliance List", 0);
INSERT INTO tbl_forms VALUES(16, 4, 'Assignee Wise Compliance', '/assignee-wise-compliance', 16, "Compliance List", 0);
INSERT INTO tbl_forms VALUES(17, 4, 'Unit Wise Compliance', '/unit-wise-compliance', 17, "Compliance List", 0);
INSERT INTO tbl_forms VALUES(18, 4, 'Compliance Task Applicability Status', '/compliance-task-applicability-status', 18, null, 0);
INSERT INTO tbl_forms VALUES(19, 4, 'Unit Details', '/unit-details', 19, null, 0);
INSERT INTO tbl_forms VALUES(20, 4, 'Compliance Activity Report', '/compliance-activity-report', 20, null, 0);
INSERT INTO tbl_forms VALUES(21, 4, 'Reassigned History', '/reassigned-history', 21, null, 0);
INSERT INTO tbl_forms VALUES(22, 4, 'Statutory Notifications List', '/statutory-notifications-list', 22, null, 0);
INSERT INTO tbl_forms VALUES(23, 4, 'Login Trace', '/login-trace', 23, null, 1);
INSERT INTO tbl_forms VALUES(24, 4, 'Audit Trail', '/audit-trail', 24, null, 1);
INSERT INTO tbl_forms VALUES(25, 5, 'Settings', '/settings',  25, null, 1);
INSERT INTO tbl_forms VALUES(26, 5, 'View Profile', '/view-profile',  26, null, 0);
INSERT INTO tbl_session_types VALUES(1, "web");
INSERT INTO tbl_session_types VALUES(2, "android");
INSERT INTO tbl_session_types VALUES(3, "ios");
INSERT INTO tbl_session_types VALUES(4, "blackberry");
INSERT INTO tbl_compliance_duration_type VALUES(1, "Day(s)");
INSERT INTO tbl_compliance_duration_type VALUES(2, "Hour(s)");
INSERT INTO tbl_compliance_repeat_type VALUES(1, "Day(s)");
INSERT INTO tbl_compliance_repeat_type VALUES(2, "Month(s)");
INSERT INTO tbl_compliance_repeat_type VALUES(3, "Year(s)");
INSERT INTO tbl_compliance_frequency VALUES(1, "One Time");
INSERT INTO tbl_compliance_frequency VALUES(2, "Periodical");
INSERT INTO tbl_compliance_frequency VALUES(3, "Review");
INSERT INTO tbl_compliance_frequency VALUES(4, "On Occurrence");
INSERT INTO tbl_notification_types VALUES(1, "Notification");
INSERT INTO tbl_notification_types VALUES(2, "Reminder");
INSERT INTO tbl_notification_types VALUES(3, "Escalation");
DROP TRIGGER IF EXISTS `after_tbl_statutory_notifications_units_insert`;
INSERT INTO tbl_mobile_sync_versions VALUES(0, 0, 0, 0, 0);
ALTER TABLE `tbl_compliances` ADD INDEX `ccompliance_id_domain_id_idx` (`compliance_id`, `domain_id`);
ALTER TABLE `tbl_client_statutories` ADD CONSTRAINT `fk_client_unit_id` FOREIGN KEY (`unit_id`) REFERENCES `tbl_units` (`unit_id`) ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE `tbl_client_statutories` ADD INDEX `country_idx` (`country_id`);
ALTER TABLE `tbl_client_statutories` ADD INDEX `domain_idx` (`domain_id`);
ALTER TABLE `tbl_client_compliances` ADD CONSTRAINT `fk_client_statutory_id` FOREIGN KEY (`client_statutory_id`) REFERENCES `tbl_client_statutories` (`client_statutory_id`) ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE `tbl_client_compliances` ADD CONSTRAINT `fk_compliance_id` FOREIGN KEY (`compliance_id`) REFERENCES `tbl_compliances` (`compliance_id`) ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE `tbl_assigned_compliances` ADD CONSTRAINT `fk_assign_compliance_id` FOREIGN KEY (`compliance_id`) REFERENCES `tbl_compliances` (`compliance_id`) ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE `tbl_assigned_compliances` ADD CONSTRAINT `fk_assign_unit_id` FOREIGN KEY (`unit_id`) REFERENCES `tbl_units` (`unit_id`) ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE `tbl_assigned_compliances` ADD INDEX `compliance_id_unit_id_idx` (`unit_id`, `compliance_id`);
ALTER TABLE `tbl_compliance_history` ADD CONSTRAINT `fk_history_compliance_id` FOREIGN KEY (`compliance_id`) REFERENCES `tbl_compliances` (`compliance_id`) ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE `tbl_compliance_history` ADD CONSTRAINT `fk_history_unit_id` FOREIGN KEY (`unit_id`) REFERENCES `tbl_units` (`unit_id`) ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE `tbl_compliance_history` ADD INDEX `hisoty_compliance_id_unit_id_idx` (`unit_id`, `compliance_id`);
ALTER TABLE `tbl_reassigned_compliances_history` ADD CONSTRAINT `fk_reassign_compliance_id` FOREIGN KEY (`compliance_id`) REFERENCES `tbl_compliances` (`compliance_id`) ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE `tbl_reassigned_compliances_history` ADD CONSTRAINT `fk_reassign_unit_id` FOREIGN KEY (`unit_id`) REFERENCES `tbl_units` (`unit_id`) ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE `tbl_reassigned_compliances_history` ADD INDEX `reassign_compliance_id_unit_id_idx` (`unit_id`, `compliance_id`);
ALTER TABLE `tbl_notifications_log` ADD CONSTRAINT `fk_notification_compliance_id` FOREIGN KEY (`compliance_id`) REFERENCES `tbl_compliances` (`compliance_id`) ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE `tbl_notifications_log` ADD CONSTRAINT `fk_notification_unit_id` FOREIGN KEY (`unit_id`) REFERENCES `tbl_units` (`unit_id`) ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE `tbl_notifications_log` ADD INDEX `notification_compliance_id_unit_id_idx` (`unit_id`, `compliance_id`);
ALTER TABLE `tbl_notification_user_log` ADD CONSTRAINT `fk_notification_id` FOREIGN KEY (`notification_id`) REFERENCES `tbl_notifications_log` (`notification_id`) ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE `tbl_statutory_notification_status` ADD CONSTRAINT `fk_statutory_notification_id` FOREIGN KEY (`statutory_notification_id`) REFERENCES `tbl_statutory_notifications_log` (`statutory_notification_id`) ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE `tbl_statutory_notification_status` ADD INDEX `user_id_idx` (`user_id`);
ALTER TABLE `tbl_statutory_notifications_units` ADD CONSTRAINT `fk_statutory_notify_unit_id` FOREIGN KEY (`statutory_notification_id`) REFERENCES `tbl_statutory_notifications_log` (`statutory_notification_id`) ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE `tbl_statutory_notifications_units` ADD CONSTRAINT `fk_notify_unit_id` FOREIGN KEY (`unit_id`) REFERENCES `tbl_units` (`unit_id`) ON DELETE NO ACTION ON UPDATE NO ACTION;
SET GLOBAL connect_timeout=120000;
SET GLOBAL wait_timeout=120000;
SET GLOBAL max_connections = 5000;
