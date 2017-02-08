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
CREATE TABLE `tbl_form_category` (
  `form_category_id` int(11) PRIMARY KEY NOT NULL,
  `form_id` int(11) NOT NULL,
  `user_category_id` int(11) NOT NULL,
  UNIQUE KEY(`form_id`,  `user_category_id`)
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
  PRIMARY KEY (`form_id`),
  CONSTRAINT `tbl_forms_ibfk_1` FOREIGN KEY (`form_type_id`) REFERENCES `tbl_form_type` (`form_type_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
CREATE TABLE `tbl_session_types` (
  `session_type_id` int(11) NOT NULL,
  `session_type` varchar(20) NOT NULL,
  PRIMARY KEY (`session_type_id`)
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
  `organisation_id` int(11) NOT NULL AUTO_INCREMENT,
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
  `total_view_licence` int(11) NOT NULL,
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
  UNIQUE KEY(`client_id`, `country_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
CREATE TABLE `tbl_units` (
  `unit_id` int(11) NOT NULL,
  `client_id` int(11) NOT NULL,
  `business_group_id` int(11) DEFAULT NULL,
  `legal_entity_id` int(11) NOT NULL,
  `division_id` int(11) DEFAULT NULL,
  `category_id` int(11) NOT NULL,
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
CREATE TABLE `tbl_user_groups` (
  `user_group_id` int(11) NOT NULL,
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
CREATE TABLE `tbl_user_group_forms` (
  `user_group_id` int(11) NOT NULL,
  `form_id` int(11) DEFAULT NULL,
  UNIQUE KEY (`user_group_id`, `form_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
CREATE TABLE `tbl_service_providers` (
  `service_provider_id` int(11) NOT NULL ,
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
  `address` varchar(500) DEFAULT NULL,
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
CREATE TABLE `tbl_user_login_details` (
  `user_id` int(11) NOT NULL,
  `user_category_id` int(11) NOT NULL,
  `username` varchar(20) DEFAULT NULL,
  `is_active` tinyint(4) DEFAULT '1',
  `password` varchar(50) DEFAULT NULL,
  UNIQUE KEY(`user_id`, `user_category_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
CREATE TABLE `tbl_user_login_history` (
  `user_id` int(11) NOT NULL,
  `ip` varchar(20) NOT NULL,
  `login_time` datetime DEFAULT NULL,
  `login_attempt` int(11) DEFAULT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
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
CREATE TABLE `tbl_email_verification` (
  `user_id` int(11) NOT NULL,
  `verification_code` varchar(50) NOT NULL,
  `verification_type_id` int(11) NOT NULL,
  `expiry_date` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
CREATE TABLE `tbl_activity_log` (
  `activity_log_id` int(11) NOT NULL AUTO_INCREMENT,
  `client_id` int(11) NOT NULL,
  `legal_entity_id` int(11) DEFAULT NULL,
  `unit_id` int(11) DEFAULT NULL,
  `user_category_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `form_id` int(11) NOT NULL,
  `action` varchar(500) NOT NULL,
  `created_on` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`activity_log_id`)
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
insert into tbl_audit_log values(0, 0);
INSERT INTO tbl_user_category VALUES(1, "Group Admin");
INSERT INTO tbl_user_category VALUES(2, "View Only");
INSERT INTO tbl_user_category VALUES(3, "Legal Entity Admin");
INSERT INTO tbl_user_category VALUES(4, "Domain Admin");
INSERT INTO tbl_user_category VALUES(5, "Client Executive");
INSERT INTO tbl_user_category VALUES(6, "Service Provider");
-- Form Type
INSERT INTO tbl_form_type VALUES(1, "Master");
INSERT INTO tbl_form_type VALUES(2, "Transaction");
INSERT INTO tbl_form_type VALUES(3, "Report");
INSERT INTO tbl_form_type VALUES(4, "My Accounts");
INSERT INTO tbl_form_type VALUES(5, "Dashboard");
-- Forms
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
INSERT INTO tbl_forms VALUES(18, 3, 'Domain Score Card', "/domain-wise-report", 18, null);
INSERT INTO tbl_forms VALUES(19, 3, 'Legal Entity Wise Score Card', "/legal-entity-wise-score-card", 19, null);
INSERT INTO tbl_forms VALUES(20, 3, 'Work Flow Score Card', "/work-flow-score-card", 20, null);
INSERT INTO tbl_forms VALUES(21, 3, 'Statutory Settings Unit Wise Report', "/statutory-settings-unit-wise-report", 21, null);
INSERT INTO tbl_forms VALUES(22, 3, 'Reassigned History Report', "/reassigned-history-report", 22, null);
INSERT INTO tbl_forms VALUES(23, 3, 'Risk Report', "/risk-report", 23, null);
INSERT INTO tbl_forms VALUES(24, 3, 'Unit List', "/unit-list", 24, null);
INSERT INTO tbl_forms VALUES(25, 3, 'Statutory Notification List', "/statutory-notification-list", 25, null);
INSERT INTO tbl_forms VALUES(26, 3, 'Service Provider Details', "/service-provider-details", 26, null);
INSERT INTO tbl_forms VALUES(27, 3, 'Audit Trail', "/audit-trail", 27, null);
INSERT INTO tbl_forms VALUES(28, 3, 'Login Trace', "/login-trace", 28, null);
INSERT INTO tbl_forms VALUES(29, 4, 'view-profile', "/view-profile", 29, null);
INSERT INTO tbl_forms VALUES(30, 4, 'Client View Profile', "/client-view-profile", 30, null);
INSERT INTO tbl_forms VALUES(31, 4, 'Change Password', "/change-password", 31, null);
INSERT INTO tbl_forms VALUES(32, 4, 'Client Settings', "/client-settings", 32, null);
INSERT INTO tbl_forms VALUES(33, 4, 'themes', "/themes", 33, null);
INSERT INTO tbl_forms VALUES(34, 5, 'Dashboard', "/dashboard", 34, null);
INSERT INTO tbl_forms VALUES(35, 2, 'Compliance Task Details', "/compliance-details", 35, null);
INSERT INTO tbl_forms VALUES(36, 4, 'Reminders', "/reminders", 36, null);
INSERT INTO tbl_forms VALUES(37, 4, 'Statutory Notifications', "/statutory-notifications", 37, null);
INSERT INTO tbl_forms VALUES(38, 4, 'Escalations', "/escalations", 38, null);
INSERT INTO tbl_forms VALUES(39, 4, 'Messages', "/messages", 39, null);


-- Group Admin Forms (form_category_id, form_id, user_category_id )
insert into tbl_form_category values (1, 1, 1);
insert into tbl_form_category values (2, 2, 1);
insert into tbl_form_category values (3, 3, 1);
insert into tbl_form_category values (4, 4, 1);
insert into tbl_form_category values (5, 5, 1);
insert into tbl_form_category values (6, 6, 1);
insert into tbl_form_category values (7, 7, 1);
insert into tbl_form_category values (8, 8, 1);
insert into tbl_form_category values (9, 9, 1);
insert into tbl_form_category values (10, 10, 1);
insert into tbl_form_category values (12, 12, 1);
insert into tbl_form_category values (13, 13, 1);
insert into tbl_form_category values (14, 14, 1);
insert into tbl_form_category values (15, 15, 1);
insert into tbl_form_category values (16, 16, 1);
insert into tbl_form_category values (17, 17, 1);
insert into tbl_form_category values (18, 18, 1);
insert into tbl_form_category values (19, 19, 1);
insert into tbl_form_category values (20, 20, 1);
insert into tbl_form_category values (21, 21, 1);
insert into tbl_form_category values (22, 22, 1);
insert into tbl_form_category values (23, 23, 1);
insert into tbl_form_category values (24, 24, 1);
insert into tbl_form_category values (25, 25, 1);
insert into tbl_form_category values (26, 26, 1);
insert into tbl_form_category values (27, 27, 1);
insert into tbl_form_category values (28, 28, 1);
insert into tbl_form_category values (29, 29, 1);
insert into tbl_form_category values (30, 30, 1);
insert into tbl_form_category values (31, 31, 1);
insert into tbl_form_category values (32, 32, 1);
insert into tbl_form_category values (33, 33, 1);
insert into tbl_form_category values (34, 34, 1);
insert into tbl_form_category values (148, 36, 1);
insert into tbl_form_category values (149, 37, 1);
insert into tbl_form_category values (150, 38, 1);
insert into tbl_form_category values (151, 39, 1);


-- legal Entity Admin Forms
insert into tbl_form_category values (35, 1, 3);
insert into tbl_form_category values (36, 2, 3);
insert into tbl_form_category values (37, 3, 3);
insert into tbl_form_category values (38, 4, 3);
insert into tbl_form_category values (39, 5, 3);
insert into tbl_form_category values (40, 6, 3);
insert into tbl_form_category values (41, 7, 3);
insert into tbl_form_category values (42, 8, 3);
insert into tbl_form_category values (43, 9, 3);
insert into tbl_form_category values (44, 10, 3);
insert into tbl_form_category values (45, 12, 3);
insert into tbl_form_category values (46, 13, 3);
insert into tbl_form_category values (47, 14, 3);
insert into tbl_form_category values (48, 15, 3);
insert into tbl_form_category values (49, 16, 3);
insert into tbl_form_category values (50, 17, 3);
insert into tbl_form_category values (51, 18, 3);
insert into tbl_form_category values (52, 19, 3);
insert into tbl_form_category values (53, 20, 3);
insert into tbl_form_category values (54, 21, 3);
insert into tbl_form_category values (55, 22, 3);
insert into tbl_form_category values (56, 23, 3);
insert into tbl_form_category values (57, 24, 3);
insert into tbl_form_category values (58, 25, 3);
insert into tbl_form_category values (59, 26, 3);
insert into tbl_form_category values (60, 27, 3);
insert into tbl_form_category values (61, 28, 3);
insert into tbl_form_category values (62, 29, 3);
insert into tbl_form_category values (63, 30, 3);
insert into tbl_form_category values (64, 31, 3);
insert into tbl_form_category values (65, 32, 3);
insert into tbl_form_category values (66, 33, 3);
insert into tbl_form_category values (67, 34, 3);
insert into tbl_form_category values (152, 36, 3);
insert into tbl_form_category values (153, 37, 3);
insert into tbl_form_category values (154, 38, 3);
insert into tbl_form_category values (155, 39, 3);

-- Domain Admin Forms
insert into tbl_form_category values (68, 3, 4);
insert into tbl_form_category values (69, 5, 4);
insert into tbl_form_category values (70, 7, 4);
insert into tbl_form_category values (71, 8, 4);
insert into tbl_form_category values (72, 9, 4);
insert into tbl_form_category values (73, 10, 4);
insert into tbl_form_category values (74, 12, 4);
insert into tbl_form_category values (75, 13, 4);
insert into tbl_form_category values (76, 14, 4);
insert into tbl_form_category values (77, 15, 4);
insert into tbl_form_category values (78, 16, 4);
insert into tbl_form_category values (79, 17, 4);
insert into tbl_form_category values (80, 18, 4);
insert into tbl_form_category values (81, 19, 4);
insert into tbl_form_category values (82, 20, 4);
insert into tbl_form_category values (83, 21, 4);
insert into tbl_form_category values (84, 22, 4);
insert into tbl_form_category values (85, 23, 4);
insert into tbl_form_category values (86, 24, 4);
insert into tbl_form_category values (87, 25, 4);
insert into tbl_form_category values (88, 26, 4);
insert into tbl_form_category values (89, 28, 4);
insert into tbl_form_category values (90, 29, 4);
insert into tbl_form_category values (91, 30, 4);
insert into tbl_form_category values (92, 31, 4);
insert into tbl_form_category values (93, 32, 4);
insert into tbl_form_category values (94, 33, 4);
insert into tbl_form_category values (95, 34, 4);
insert into tbl_form_category values (156, 36, 4);
insert into tbl_form_category values (157, 37, 4);
insert into tbl_form_category values (158, 38, 4);
insert into tbl_form_category values (159, 39, 4);

-- Inhouse Users Forms
insert into tbl_form_category values (96, 35, 5);
insert into tbl_form_category values (97, 11, 5);
insert into tbl_form_category values (98, 16, 5);
insert into tbl_form_category values (99, 17, 5);
insert into tbl_form_category values (100, 18, 5);
insert into tbl_form_category values (101, 19, 5);
insert into tbl_form_category values (102, 20, 5);
insert into tbl_form_category values (103, 24, 5);
insert into tbl_form_category values (104, 25, 5);
insert into tbl_form_category values (105, 29, 5);
insert into tbl_form_category values (106, 30, 5);
insert into tbl_form_category values (107, 31, 5);
insert into tbl_form_category values (108, 32, 5);
insert into tbl_form_category values (109, 33, 5);
insert into tbl_form_category values (110, 34, 5);
insert into tbl_form_category values (160, 36, 5);
insert into tbl_form_category values (161, 38, 5);
insert into tbl_form_category values (162, 39, 5);

-- Service Provider Forms
insert into tbl_form_category values (111, 35, 6);
insert into tbl_form_category values (112, 11, 6);
insert into tbl_form_category values (113, 16, 6);
insert into tbl_form_category values (114, 17, 6);
insert into tbl_form_category values (115, 18, 6);
insert into tbl_form_category values (116, 19, 6);
insert into tbl_form_category values (117, 20, 6);
insert into tbl_form_category values (118, 24, 6);
insert into tbl_form_category values (119, 26, 6);
insert into tbl_form_category values (120, 29, 6);
insert into tbl_form_category values (121, 30, 6);
insert into tbl_form_category values (122, 31, 6);
insert into tbl_form_category values (123, 32, 6);
insert into tbl_form_category values (124, 33, 6);
insert into tbl_form_category values (125, 34, 6);
insert into tbl_form_category values (163, 36, 6);
insert into tbl_form_category values (164, 38, 6);
insert into tbl_form_category values (165, 39, 6);

-- View Only Forms
insert into tbl_form_category values (126, 12, 2);
insert into tbl_form_category values (127, 13, 2);
insert into tbl_form_category values (128, 14, 2);
insert into tbl_form_category values (129, 15, 2);
insert into tbl_form_category values (130, 16, 2);
insert into tbl_form_category values (131, 17, 2);
insert into tbl_form_category values (132, 18, 2);
insert into tbl_form_category values (133, 19, 2);
insert into tbl_form_category values (134, 20, 2);
insert into tbl_form_category values (135, 21, 2);
insert into tbl_form_category values (136, 22, 2);
insert into tbl_form_category values (137, 23, 2);
insert into tbl_form_category values (138, 24, 2);
insert into tbl_form_category values (139, 25, 2);
insert into tbl_form_category values (140, 26, 2);
insert into tbl_form_category values (141, 28, 2);
insert into tbl_form_category values (142, 29, 2);
insert into tbl_form_category values (143, 30, 2);
insert into tbl_form_category values (144, 31, 2);
insert into tbl_form_category values (145, 32, 2);
insert into tbl_form_category values (146, 33, 2);
insert into tbl_form_category values (147, 34, 2);
-- tbl_session_types
INSERT INTO tbl_session_types VALUES(1, "web");
INSERT INTO tbl_session_types VALUES(2, "android");
INSERT INTO tbl_session_types VALUES(3, "ios");
INSERT INTO tbl_session_types VALUES(4, "blackberry");
-- tbl_verification_type
INSERT INTO tbl_verification_type VALUES(1, "Registraion");
INSERT INTO tbl_verification_type VALUES(2, "Reset Password");
INSERT INTO tbl_verification_type VALUES(3, "Data Download");
