USE `compfie_knowledge`;

-- DELETE FROM tbl_form_category;
INSERT INTO tbl_form_category VALUES(1, "IT Team");
INSERT INTO tbl_form_category VALUES(2, "Console Team");
INSERT INTO tbl_form_category VALUES(3, "Knowledge User");
INSERT INTO tbl_form_category VALUES(4, "Knowledge Manager");
INSERT INTO tbl_form_category VALUES(5, "Client Coordination Manager");
INSERT INTO tbl_form_category VALUES(6, "Client Coordination User");
INSERT INTO tbl_form_category VALUES(7, "Techno Functional Manager");
INSERT INTO tbl_form_category VALUES(8, "Techno Functional User");

-- DELETE FROM tbl_form_type;
INSERT INTO tbl_form_type VALUES(1, "Master");
INSERT INTO tbl_form_type VALUES(2, "Transaction");
INSERT INTO tbl_form_type VALUES(3, "Report");
INSERT INTO tbl_form_type VALUES(4, "Settings");

-- DELETE FROM tbl_forms
-- fields(form_id, form_category_id, form_type_id, form_name, form_url, form_order, parent_menu)

-- mirror_knowledge
-- Admin
INSERT INTO tbl_forms VALUES(1, 1, 1,  'Country', '/knowledge/country-master', 1,  null);
INSERT INTO tbl_forms VALUES(2, 1, 1,  'Domain', '/knowledge/domain-master', 2, null);
INSERT INTO tbl_forms VALUES(3, 1, 1, 'Geography Level Master', '/knowledge/geography-level-master', 3, 'Geography');
INSERT INTO tbl_forms VALUES(4, 1, 1, 'Geography Master', '/knowledge/geography-master', 4, 'Geography');
INSERT INTO tbl_forms VALUES(5, 1, 1, 'Organization Master', '/knowledge/industry-master', 5, null);
INSERT INTO tbl_forms VALUES(6, 1, 1, 'Statutory Nature Master', '/knowledge/statutory-nature-master', 6, 'Statutory');
INSERT INTO tbl_forms VALUES(7, 1, 1, 'Statutory Level Master', '/knowledge/statutory-level-master', 7, 'Statutory');
INSERT INTO tbl_forms VALUES(8, 1, 1,  'User Group', '/knowledge/user-group-master', 8, null);
INSERT INTO tbl_forms VALUES(9, 1, 1,  'User', '/knowledge/user-master', 9, null);
INSERT INTO tbl_forms VALUES(10, 1, 1,  'Techno User Mapping', '/knowledge/user-master', 10, null);
INSERT INTO tbl_forms VALUES(11, 1, 4, 'Validity Date Settings', '/knowledge/validity-date-settings', 11, null);

INSERT INTO tbl_forms VALUES(12, 1, 3, 'Country Report', '/knowledge/country-report', 12, 'Master');
INSERT INTO tbl_forms VALUES(13, 1, 3, 'Domain Report', '/knowledge/domain-report', 13, 'Master');
INSERT INTO tbl_forms VALUES(14, 1, 3, 'Geography Report', '/knowledge/geography-report', 14, 'Master');
INSERT INTO tbl_forms VALUES(15, 1, 3, 'Organization Report', '/knowledge/industry-report', 15, 'Master');
INSERT INTO tbl_forms VALUES(16, 1, 3, 'Statutory Nature Report', '/knowledge/statutory-nature-report', 16, 'Master');
INSERT INTO tbl_forms VALUES(17, 1, 3, 'Audit Trail', '/knowledge/audit-trail', 17, null);

INSERT INTO tbl_forms VALUES(18, 3, 2, 'Statutory Mapping', '/knowledge/statutory-mapping', 18, null);
INSERT INTO tbl_forms VALUES(19, 4, 2, 'Approve Statutory Mapping', '/knowledge/approve-statutory-mapping', 19, null);
INSERT INTO tbl_forms VALUES(20, 4, 3, 'Statutory Mapping Report', '/knowledge/statutory-mapping-report', 20, null);

-- CC Manager
INSERT INTO tbl_forms VALUES(21, 5, 1, 'Client Group Creation', '', 21, null);
INSERT INTO tbl_forms VALUES(22, 5, 1, 'Client Contract Renewal', '', 22, null);
INSERT INTO tbl_forms VALUES(23, 5, 1, 'Client Unit Approval', '', 23, null);
INSERT INTO tbl_forms VALUES(24, 5, 1, 'Assign Client Unit - Techno Manager', '', 24, null);
INSERT INTO tbl_forms VALUES(25, 5, 1, 'Client Unit Movement', '', 25, null);
INSERT INTO tbl_forms VALUES(26, 5, 1, 'Client Profile', '', 26, null);
INSERT INTO tbl_forms VALUES(27, 5, 1, 'Legal Entity Closure', '', 27, null);
-- CC User
INSERT INTO tbl_forms VALUES(28, 6, 1, 'Client Unit', '/knowledge/client-unit', 28, null);

-- Techno Manager
INSERT INTO tbl_forms VALUES(29, 7, 2, 'Assign Client Unit - Techno User', '/knowledge/assign-statutory', 29, null);
INSERT INTO tbl_forms VALUES(30, 7, 2, 'Approve Assigned Statutory', '/knowledge/assign-statutory', 30, null);
-- Techno User
INSERT INTO tbl_forms VALUES(31, 8, 2, 'Assign Statutory', '/knowledge/assign-statutory', 31, null);


INSERT INTO tbl_forms VALUES(32, 7, 3, 'Client Details Report', '/knowledge/client-details-report', 32, null);
INSERT INTO tbl_forms VALUES(33, 7, 3, 'Client Contract Details', '/knowledge/client-details-report', 33, null);

INSERT INTO tbl_forms VALUES(34, 7, 3, 'Assigned Statutory', '/knowledge/assigned-statutory-report', 34, null);
INSERT INTO tbl_forms VALUES(35, 7, 3, 'Compliance List', '/knowledge/compliance-task-list', 35, null);
INSERT INTO tbl_forms VALUES(36, 7, 3, 'Statutory Notifications List', '/knowledge/statutory-notifications-list', 36, null);
-- common



-- tbl_admin
-- email_id, username, password, user_type -- p@$$word@123
INSERT INTO tbl_admin (email_id, username, password, user_type)  VALUES("admin@compfie.com", "admin", "7ecfd14ba1b0d6800688a0a317a5a331", 0);
INSERT INTO tbl_admin (email_id, username, password, user_type)  VALUES("consoleadmin@compfie.com", "consoleadmin", "7ecfd14ba1b0d6800688a0a317a5a331", 1);

-- tbl_session_types
INSERT INTO tbl_session_types VALUES(1, "web");
INSERT INTO tbl_session_types VALUES(2, "android");
INSERT INTO tbl_session_types VALUES(3, "ios");
INSERT INTO tbl_session_types VALUES(4, "blackberry");

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

-- tbl_machines
INSERT INTO `tbl_machines` (`machine_id`, `machine_name`, `ip`, `port`, `client_ids`, `server_full`) VALUES
(1, 'client server one', '127.0.0.1', 8081, '1', 0);

-- tbl_database_server
INSERT INTO `tbl_database_server` (`ip`, `db_server_name`, `port`, `server_username`, `server_password`) VALUES
('127.0.0.1', 'db server one', 3306, 'root', '123456');

-- triggers
-- DROP TRIGGER IF EXISTS `after_tbl_business_groups_insert`;
-- DELIMITER //
-- CREATE TRIGGER `after_tbl_business_groups_insert` AFTER INSERT ON `tbl_business_groups`
--  FOR EACH ROW BEGIN
--    SET @action = 0;


--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--         VALUES (@action,
--                 NEW.client_id,
--                 NEW.business_group_id,
--                 'business_group_name',
--                 NEW.business_group_name,
--                 'tbl_business_groups');
--     UPDATE tbl_client_replication_status set is_new_data = 1
--     WHERE client_id = NEW.client_id;
-- END
-- //
-- DELIMITER ;


-- DROP TRIGGER IF EXISTS `after_tbl_business_groups_update`;
-- DELIMITER //
-- CREATE TRIGGER `after_tbl_business_groups_update` AFTER UPDATE ON `tbl_business_groups`
--  FOR EACH ROW BEGIN
--    SET @action = 1;


--    IF OLD.business_group_name <> NEW.business_group_name THEN
--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--         VALUES (@action,
--                 NEW.client_id,
--                 NEW.business_group_id,
--                 'business_group_name',
--                 NEW.business_group_name,
--                 'tbl_business_groups');
--     UPDATE tbl_client_replication_status set is_new_data = 1
--     WHERE client_id = NEW.client_id;
--    END IF;

-- END
-- //
-- DELIMITER ;

-- --
-- -- Triggers `tbl_client_compliances`
-- --

-- DROP TRIGGER IF EXISTS `after_tbl_client_compliances_update`;
-- DELIMITER //
-- CREATE TRIGGER `after_tbl_client_compliances_update` AFTER UPDATE ON `tbl_client_compliances`
--  FOR EACH ROW BEGIN
--     SET @action = 0;
--     SET @submission_type = (SELECT t1.submission_type FROM tbl_client_statutories t1 WHERE t1.client_statutory_id = NEW.client_statutory_id);
--     SET @client_id = (SELECT t1.client_id FROM tbl_client_statutories t1 WHERE t1.client_statutory_id = NEW.client_statutory_id);

--    IF (@submission_type = 1) THEN
--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--         VALUES (@action,
--                 @client_id,
--                 NEW.client_compliance_id,
--                 'client_statutory_id',
--                 NEW.client_statutory_id,
--                 'tbl_client_compliances');
--    END IF;


--    IF (@submission_type = 1) THEN
--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--         VALUES (@action,
--                 @client_id,
--                 NEW.client_compliance_id,
--                 'compliance_id',
--                 NEW.compliance_id,
--                 'tbl_client_compliances');
--    END IF;


--    IF (@submission_type = 1) THEN
--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--         VALUES (@action,
--                 @client_id,
--                 NEW.client_compliance_id,
--                 'statutory_applicable',
--                 NEW.statutory_applicable,
--                 'tbl_client_compliances');
--    END IF;


--    IF (@submission_type = 1) THEN
--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--         VALUES (@action,
--                 @client_id,
--                 NEW.client_compliance_id,
--                 'statutory_opted',
--                 NEW.statutory_opted,
--                 'tbl_client_compliances');
--    END IF;


--    IF (@submission_type = 1) THEN
--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--         VALUES (@action,
--                 @client_id,
--                 NEW.client_compliance_id,
--                 'not_applicable_remarks',
--                 NEW.not_applicable_remarks,
--                 'tbl_client_compliances');
--    END IF;


--    IF (@submission_type = 1) THEN
--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--         VALUES (@action,
--                 @client_id,
--                 NEW.client_compliance_id,
--                 'compliance_applicable',
--                 NEW.compliance_applicable,
--                 'tbl_client_compliances');
--    END IF;


--    IF (@submission_type = 1) THEN
--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--         VALUES (@action,
--                 @client_id,
--                 NEW.client_compliance_id,
--                 'compliance_opted',
--                 NEW.compliance_opted,
--                 'tbl_client_compliances');
--    END IF;


--    IF (@submission_type = 1) THEN
--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--         VALUES (@action,
--                 @client_id,
--                 NEW.client_compliance_id,
--                 'compliance_remarks',
--                 NEW.compliance_remarks,
--                 'tbl_client_compliances');
--    END IF;


--    IF (@submission_type = 1) THEN
--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--         VALUES (@action,
--                 @client_id,
--                 NEW.client_compliance_id,
--                 'submitted_on',
--                 NEW.submitted_on,
--                 'tbl_client_compliances');
--    END IF;

--    IF (@submission_type = 1) THEN
--     UPDATE tbl_client_replication_status set is_new_data = 1
--     WHERE client_id = @client_id;
--    END IF;


-- END
-- //
-- DELIMITER ;


-- --
-- -- Triggers `tbl_client_configurations`
-- --
-- DROP TRIGGER IF EXISTS `after_tbl_client_configurations_insert`;
-- DELIMITER //
-- CREATE TRIGGER `after_tbl_client_configurations_insert` AFTER INSERT ON `tbl_client_configurations`
--  FOR EACH ROW BEGIN
--    SET @action = 0;

--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--         VALUES (@action,
--                 NEW.client_id,
--                 NEW.client_config_id,
--                 'country_id',
--                 NEW.country_id,
--                 'tbl_client_configurations');

--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--         VALUES (@action,
--                 NEW.client_id,
--                 NEW.client_config_id,
--                 'domain_id',
--                 NEW.domain_id,
--                 'tbl_client_configurations');

--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--         VALUES (@action,
--                 NEW.client_id,
--                 NEW.client_config_id,
--                 'period_from',
--                 NEW.period_from,
--                 'tbl_client_configurations');

--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--         VALUES (@action,
--                 NEW.client_id,
--                 NEW.client_config_id,
--                 'period_to',
--                 NEW.period_to,
--                 'tbl_client_configurations');

--     UPDATE tbl_client_replication_status set is_new_data = 1
--     WHERE client_id = NEW.client_id;

-- END
-- //
-- DELIMITER ;
-- DROP TRIGGER IF EXISTS `after_tbl_client_configurations_update`;
-- DELIMITER //
-- CREATE TRIGGER `after_tbl_client_configurations_update` AFTER UPDATE ON `tbl_client_configurations`
--  FOR EACH ROW BEGIN
--    SET @action = 1;


--    IF OLD.country_id <> NEW.country_id THEN
--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--         VALUES (@action,
--                 NEW.client_id,
--                 NEW.client_config_id,
--                 'country_id',
--                 NEW.country_id,
--                 'tbl_client_configurations');
--    END IF;


--    IF OLD.domain_id <> NEW.domain_id THEN
--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--         VALUES (@action,
--                 NEW.client_id,
--                 NEW.client_config_id,
--                 'domain_id',
--                 NEW.domain_id,
--                 'tbl_client_configurations');
--    END IF;


--    IF OLD.period_from <> NEW.period_from THEN
--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--         VALUES (@action,
--                 NEW.client_id,
--                 NEW.client_config_id,
--                 'period_from',
--                 NEW.period_from,
--                 'tbl_client_configurations');
--    END IF;


--    IF OLD.period_to <> NEW.period_to THEN
--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--         VALUES (@action,
--                 NEW.client_id,
--                 NEW.client_config_id,
--                 'period_to',
--                 NEW.period_to,
--                 'tbl_client_configurations');
--    END IF;
--     UPDATE tbl_client_replication_status set is_new_data = 1
--     WHERE client_id = NEW.client_id;

-- END
-- //
-- DELIMITER ;


-- --
-- -- Triggers `tbl_client_groups`
-- --
-- DROP TRIGGER IF EXISTS `after_tbl_client_groups_insert`;
-- DELIMITER //
-- CREATE TRIGGER `after_tbl_client_groups_insert` AFTER INSERT ON `tbl_client_groups`
--  FOR EACH ROW BEGIN
--    SET @action = 0;
--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--         VALUES (@action,
--                 NEW.client_id,
--                 NEW.client_id,
--                 'group_name',
--                 NEW.group_name,
--                 'tbl_client_groups');
--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--         VALUES (@action,
--                 NEW.client_id,
--                 NEW.client_id,
--                 'logo_url',
--                 concat('logoooo', NEW.logo_url),
--                 'tbl_client_groups');
--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--         VALUES (@action,
--                 NEW.client_id,
--                 NEW.client_id,
--                 'logo_size',
--                 NEW.logo_size,
--                 'tbl_client_groups');
--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--         VALUES (@action,
--                 NEW.client_id,
--                 NEW.client_id,
--                 'contract_from',
--                 NEW.contract_from,
--                 'tbl_client_groups');


--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--         VALUES (@action,
--                 NEW.client_id,
--                 NEW.client_id,
--                 'contract_to',
--                 NEW.contract_to,
--                 'tbl_client_groups');


--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--         VALUES (@action,
--                 NEW.client_id,
--                 NEW.client_id,
--                 'no_of_user_licence',
--                 NEW.no_of_user_licence,
--                 'tbl_client_groups');


--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--         VALUES (@action,
--                 NEW.client_id,
--                 NEW.client_id,
--                 'total_disk_space',
--                 NEW.total_disk_space,
--                 'tbl_client_groups');


--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--         VALUES (@action,
--                 NEW.client_id,
--                 NEW.client_id,
--                 'total_disk_space_used',
--                 NEW.total_disk_space_used,
--                 'tbl_client_groups');


--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--         VALUES (@action,
--                 NEW.client_id,
--                 NEW.client_id,
--                 'is_sms_subscribed',
--                 NEW.is_sms_subscribed,
--                 'tbl_client_groups');


--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--         VALUES (@action,
--                 NEW.client_id,
--                 NEW.client_id,
--                 'url_short_name',
--                 NEW.url_short_name,
--                 'tbl_client_groups');

--     INSERT INTO tbl_client_replication_status (client_id, is_new_data) VALUES(NEW.client_id, 1);
-- END
-- //
-- DELIMITER ;

-- DROP TRIGGER IF EXISTS `after_tbl_client_groups_update`;
-- DELIMITER //
-- CREATE TRIGGER `after_tbl_client_groups_update` AFTER UPDATE ON `tbl_client_groups`
--  FOR EACH ROW BEGIN
--    SET @action = 1;
--    SET @save = 0;
--    IF OLD.group_name <> NEW.group_name THEN
--    SET @save = 1;
--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--         VALUES (@action,
--                 NEW.client_id,
--                 NEW.client_id,
--                 'group_name',
--                 NEW.group_name,
--                 'tbl_client_groups');
--    END IF;


--    IF OLD.logo_url <> NEW.logo_url THEN
--    SET @save = 1;
--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--         VALUES (@action,
--                 NEW.client_id,
--                 NEW.client_id,
--                 'logo_url',
--                 NEW.logo_url,
--                 'tbl_client_groups');
--    END IF;


--    IF OLD.logo_size <> NEW.logo_size THEN
--    SET @save = 1;
--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--         VALUES (@action,
--                 NEW.client_id,
--                 NEW.client_id,
--                 'logo_size',
--                 NEW.logo_size,
--                 'tbl_client_groups');
--    END IF;


--    IF OLD.contract_from <> NEW.contract_from THEN
--    SET @save = 1;
--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--         VALUES (@action,
--                 NEW.client_id,
--                 NEW.client_id,
--                 'contract_from',
--                 NEW.contract_from,
--                 'tbl_client_groups');
--    END IF;


--    IF OLD.contract_to <> NEW.contract_to THEN
--    SET @save = 1;
--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--         VALUES (@action,
--                 NEW.client_id,
--                 NEW.client_id,
--                 'contract_to',
--                 NEW.contract_to,
--                 'tbl_client_groups');
--    END IF;


--    IF OLD.no_of_user_licence <> NEW.no_of_user_licence THEN
--    SET @save = 1;
--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--         VALUES (@action,
--                 NEW.client_id,
--                 NEW.client_id,
--                 'no_of_user_licence',
--                 NEW.no_of_user_licence,
--                 'tbl_client_groups');
--    END IF;


--    IF OLD.total_disk_space <> NEW.total_disk_space THEN
--    SET @save = 1;
--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--         VALUES (@action,
--                 NEW.client_id,
--                 NEW.client_id,
--                 'total_disk_space',
--                 NEW.total_disk_space,
--                 'tbl_client_groups');
--    END IF;


--    IF OLD.total_disk_space_used <> NEW.total_disk_space_used THEN
--    SET @save = 1;
--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--         VALUES (@action,
--                 NEW.client_id,
--                 NEW.client_id,
--                 'total_disk_space_used',
--                 NEW.total_disk_space_used,
--                 'tbl_client_groups');
--    END IF;


--    IF OLD.is_sms_subscribed <> NEW.is_sms_subscribed THEN
--    SET @save = 1;
--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--         VALUES (@action,
--                 NEW.client_id,
--                 NEW.client_id,
--                 'is_sms_subscribed',
--                 NEW.is_sms_subscribed,
--                 'tbl_client_groups');
--    END IF;


--    IF OLD.url_short_name <> NEW.url_short_name THEN
--    SET @save = 1;
--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--         VALUES (@action,
--                 NEW.client_id,
--                 NEW.client_id,
--                 'url_short_name',
--                 NEW.url_short_name,
--                 'tbl_client_groups');
--    END IF;

--     IF @save = 1 THEN
--         UPDATE tbl_client_replication_status set is_new_data = 1
--         WHERE client_id = NEW.client_id;
--     END IF;

-- END
-- //
-- DELIMITER ;


-- --
-- -- Triggers `tbl_client_statutories`
-- --

-- DROP TRIGGER IF EXISTS `after_tbl_client_statutories_update`;
-- DELIMITER //
-- CREATE TRIGGER `after_tbl_client_statutories_update` AFTER UPDATE ON `tbl_client_statutories`
--  FOR EACH ROW BEGIN
--    SET @action = 0;


--    IF (NEW.submission_type = 1)THEN

--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--   SELECT @action, NEW.client_id, NEW.client_statutory_id, 'geography', parent_names, 'tbl_client_statutories'  FROM tbl_geographies WHERE geography_id=NEW.geography_id;
--    END IF;




--    IF (NEW.submission_type = 1)THEN
--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--         VALUES (@action,
--                 NEW.client_id,
--                 NEW.client_statutory_id,
--                 'country_id',
--                 NEW.country_id,
--                 'tbl_client_statutories');
--    END IF;


--    IF (NEW.submission_type = 1)THEN
--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--         VALUES (@action,
--                 NEW.client_id,
--                 NEW.client_statutory_id,
--                 'domain_id',
--                 NEW.domain_id,
--                 'tbl_client_statutories');
--    END IF;


--    IF (NEW.submission_type = 1)THEN
--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--         VALUES (@action,
--                 NEW.client_id,
--                 NEW.client_statutory_id,
--                 'unit_id',
--                 NEW.unit_id,
--                 'tbl_client_statutories');
--    END IF;

--     UPDATE tbl_client_replication_status set is_new_data = 1
--     WHERE client_id = NEW.client_id;

-- END
-- //
-- DELIMITER ;


-- --
-- -- Triggers `tbl_compliances`
-- --
-- DROP TRIGGER IF EXISTS `after_tbl_compliances_insert`;
-- DELIMITER //
-- CREATE TRIGGER `after_tbl_compliances_insert` AFTER INSERT ON `tbl_compliances`
--  FOR EACH ROW BEGIN
--    SET @action = 0;

--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--   SELECT @action, 0, NEW.compliance_id,
--   'statutory_mapping', statutory_mapping,
--   'tbl_compliances' FROM tbl_statutory_mappings
--   WHERE statutory_mapping_id=NEW.statutory_mapping_id;

--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--         VALUES (@action,
--                 0,
--                 NEW.compliance_id,
--                 'domain_id',
--                 NEW.domain_id,
--                 'tbl_compliances');

--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--         VALUES (@action,
--                 0,
--                 NEW.compliance_id,
--                 'frequency_id',
--                 NEW.frequency_id,
--                 'tbl_compliances');

--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--         VALUES (@action,
--                 0,
--                 NEW.compliance_id,
--                 'repeats_type_id',
--                 NEW.repeats_type_id,
--                 'tbl_compliances');


--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--         VALUES (@action,
--                 0,
--                 NEW.compliance_id,
--                 'duration_type_id',
--                 NEW.duration_type_id,
--                 'tbl_compliances');


--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--         VALUES (@action,
--                 0,
--                 NEW.compliance_id,
--                 'statutory_provision',
--                 NEW.statutory_provision,
--                 'tbl_compliances');


--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--         VALUES (@action,
--                 0,
--                 NEW.compliance_id,
--                 'compliance_task',
--                 NEW.compliance_task,
--                 'tbl_compliances');


--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--         VALUES (@action,
--                 0,
--                 NEW.compliance_id,
--                 'compliance_description',
--                 NEW.compliance_description,
--                 'tbl_compliances');


--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--         VALUES (@action,
--                 0,
--                 NEW.compliance_id,
--                 'document_name',
--                 NEW.document_name,
--                 'tbl_compliances');


--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--         VALUES (@action,
--                 0,
--                 NEW.compliance_id,
--                 'format_file',
--                 NEW.format_file,
--                 'tbl_compliances');


--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--         VALUES (@action,
--                 0,
--                 NEW.compliance_id,
--                 'format_file_size',
--                 NEW.format_file_size,
--                 'tbl_compliances');


--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--         VALUES (@action,
--                 0,
--                 NEW.compliance_id,
--                 'penal_consequences',
--                 NEW.penal_consequences,
--                 'tbl_compliances');


--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--         VALUES (@action,
--                 0,
--                 NEW.compliance_id,
--                 'statutory_dates',
--                 NEW.statutory_dates,
--                 'tbl_compliances');


--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--         VALUES (@action,
--                 0,
--                 NEW.compliance_id,
--                 'repeats_every',
--                 NEW.repeats_every,
--                 'tbl_compliances');


--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--         VALUES (@action,
--                 0,
--                 NEW.compliance_id,
--                 'duration',
--                 NEW.duration,
--                 'tbl_compliances');


--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--         VALUES (@action,
--                 0,
--                 NEW.compliance_id,
--                 'is_active',
--                 NEW.is_active,
--                 'tbl_compliances');
--     UPDATE tbl_client_replication_status set is_new_data = 1 where
--     client_id in (select client_id from tbl_client_domains where domain_id = NEW.domain_id);
-- END
-- //
-- DELIMITER ;

-- DROP TRIGGER IF EXISTS `after_tbl_compliances_update`;
-- DELIMITER //
-- CREATE TRIGGER `after_tbl_compliances_update` AFTER UPDATE ON `tbl_compliances`
--  FOR EACH ROW BEGIN
--    SET @action = 1;
--    SET @issave = 0;
--    IF OLD.statutory_mapping_id <> NEW.statutory_mapping_id THEN
--    set @issave = 1;
--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--   SELECT @action, 0, NEW.compliance_id, 'statutory_mapping', statutory_mapping, 'tbl_compliances'  FROM tbl_statutory_mappings WHERE statutory_mapping_id=NEW.statutory_mapping_id;
--    END IF;
--    IF OLD.domain_id <> NEW.domain_id THEN
--    set @issave = 1;
--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--         VALUES (@action,
--                 0,
--                 NEW.compliance_id,
--                 'domain_id',
--                 NEW.domain_id,
--                 'tbl_compliances');
--    END IF;

--    IF OLD.frequency_id <> NEW.frequency_id THEN
--    set @issave = 1;
--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--         VALUES (@action,
--                 0,
--                 NEW.compliance_id,
--                 'frequency_id',
--                 NEW.frequency_id,
--                 'tbl_compliances');
--    END IF;

--    IF OLD.repeats_type_id <> NEW.repeats_type_id THEN
--    set @issave = 1;
--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--         VALUES (@action,
--                 0,
--                 NEW.compliance_id,
--                 'repeats_type_id',
--                 NEW.repeats_type_id,
--                 'tbl_compliances');
--    END IF;

--    IF OLD.duration_type_id <> NEW.duration_type_id THEN
--    set @issave = 1;
--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--         VALUES (@action,
--                 0,
--                 NEW.compliance_id,
--                 'duration_type_id',
--                 NEW.duration_type_id,
--                 'tbl_compliances');
--    END IF;

--    IF OLD.statutory_provision <> NEW.statutory_provision THEN
--    set @issave = 1;
--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--         VALUES (@action,
--                 0,
--                 NEW.compliance_id,
--                 'statutory_provision',
--                 NEW.statutory_provision,
--                 'tbl_compliances');
--    END IF;

--    IF OLD.compliance_task <> NEW.compliance_task THEN
--    set @issave = 1;
--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--         VALUES (@action,
--                 0,
--                 NEW.compliance_id,
--                 'compliance_task',
--                 NEW.compliance_task,
--                 'tbl_compliances');
--    END IF;

--    IF OLD.compliance_description <> NEW.compliance_description THEN
--    set @issave = 1;
--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--         VALUES (@action,
--                 0,
--                 NEW.compliance_id,
--                 'compliance_description',
--                 NEW.compliance_description,
--                 'tbl_compliances');
--    END IF;

--    IF OLD.document_name <> NEW.document_name THEN
--    set @issave = 1;
--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--         VALUES (@action,
--                 0,
--                 NEW.compliance_id,
--                 'document_name',
--                 NEW.document_name,
--                 'tbl_compliances');
--    END IF;

--    IF OLD.format_file <> NEW.format_file THEN
--    set @issave = 1;
--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--         VALUES (@action,
--                 0,
--                 NEW.compliance_id,
--                 'format_file',
--                 NEW.format_file,
--                 'tbl_compliances');
--    END IF;

--    IF OLD.format_file_size <> NEW.format_file_size THEN
--    set @issave = 1;
--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--         VALUES (@action,
--                 0,
--                 NEW.compliance_id,
--                 'format_file_size',
--                 NEW.format_file_size,
--                 'tbl_compliances');
--    END IF;

--    IF OLD.penal_consequences <> NEW.penal_consequences THEN
--    set @issave = 1;
--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--         VALUES (@action,
--                 0,
--                 NEW.compliance_id,
--                 'penal_consequences',
--                 NEW.penal_consequences,
--                 'tbl_compliances');
--    END IF;

--    IF OLD.statutory_dates <> NEW.statutory_dates THEN
--    set @issave = 1;
--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--         VALUES (@action,
--                 0,
--                 NEW.compliance_id,
--                 'statutory_dates',
--                 NEW.statutory_dates,
--                 'tbl_compliances');
--    END IF;

--    IF OLD.repeats_every <> NEW.repeats_every THEN
--    set @issave = 1;
--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--         VALUES (@action,
--                 0,
--                 NEW.compliance_id,
--                 'repeats_every',
--                 NEW.repeats_every,
--                 'tbl_compliances');
--    END IF;

--    IF OLD.duration <> NEW.duration THEN
--    set @issave = 1;
--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--         VALUES (@action,
--                 0,
--                 NEW.compliance_id,
--                 'duration',
--                 NEW.duration,
--                 'tbl_compliances');
--    END IF;

--    IF OLD.is_active <> NEW.is_active THEN
--    set @issave = 1;
--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--         VALUES (@action,
--                 0,
--                 NEW.compliance_id,
--                 'is_active',
--                 NEW.is_active,
--                 'tbl_compliances');
--    END IF;

--    IF @issave = 1 THEN
--     UPDATE tbl_client_replication_status set is_new_data = 1 where
--     client_id in (select client_id from tbl_client_domains where domain_id = OLD.domain_id);
--    END IF ;



-- END
-- //
-- DELIMITER ;


-- --
-- -- Triggers `tbl_divisions`
-- --
-- DROP TRIGGER IF EXISTS `after_tbl_divisions_insert`;
-- DELIMITER //
-- CREATE TRIGGER `after_tbl_divisions_insert` AFTER INSERT ON `tbl_divisions`
--  FOR EACH ROW BEGIN
--    SET @action = 0;


--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--         VALUES (@action,
--                 NEW.client_id,
--                 NEW.division_id,
--                 'division_name',
--                 NEW.division_name,
--                 'tbl_divisions');

--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--         VALUES (@action,
--                 NEW.client_id,
--                 NEW.division_id,
--                 'business_group_id',
--                 NEW.business_group_id,
--                 'tbl_divisions');


--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--         VALUES (@action,
--                 NEW.client_id,
--                 NEW.division_id,
--                 'legal_entity_id',
--                 NEW.legal_entity_id,
--                 'tbl_divisions');

--     UPDATE tbl_client_replication_status set is_new_data = 1
--     WHERE client_id = NEW.client_id;

-- END
-- //
-- DELIMITER ;
-- DROP TRIGGER IF EXISTS `after_tbl_divisions_update`;
-- DELIMITER //
-- CREATE TRIGGER `after_tbl_divisions_update` AFTER UPDATE ON `tbl_divisions`
--  FOR EACH ROW BEGIN
--    SET @action = 1;


--    IF OLD.division_name <> NEW.division_name THEN
--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--         VALUES (@action,
--                 NEW.client_id,
--                 NEW.division_id,
--                 'division_name',
--                 NEW.division_name,
--                 'tbl_divisions');
--     UPDATE tbl_client_replication_status set is_new_data = 1
--     WHERE client_id = NEW.client_id;
--    END IF;

-- END
-- //
-- DELIMITER ;


-- --
-- -- Triggers `tbl_geographies`
-- --
-- DROP TRIGGER IF EXISTS `after_tbl_geographies_update`;
-- DELIMITER //
-- CREATE TRIGGER `after_tbl_geographies_update` AFTER UPDATE ON `tbl_geographies`
--  FOR EACH ROW BEGIN
--    SET @action = 1;
--    IF OLD.parent_names <> NEW.parent_names THEN
--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--   SELECT @action, @client_id := client_id, client_statutory_id, 'geography', NEW.parent_names, 'tbl_client_statutories'  FROM tbl_client_statutories WHERE geography_id=NEW.geography_id;
--     UPDATE tbl_client_replication_status set is_new_data = 1
--     WHERE client_id = @client_id;
--    END IF;
--    IF OLD.parent_names <> NEW.parent_names THEN
--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--   SELECT @action, @client_id := client_id, unit_id, 'geography', NEW.parent_names, 'tbl_units'  FROM tbl_units WHERE geography_id=NEW.geography_id;
--     UPDATE tbl_client_replication_status set is_new_data = 1
--     WHERE client_id = @client_id;
--    END IF;

-- END
-- //
-- DELIMITER ;

-- --
-- -- Triggers `tbl_industries`
-- --
-- DROP TRIGGER IF EXISTS `after_tbl_industries_update`;
-- DELIMITER //
-- CREATE TRIGGER `after_tbl_industries_update` AFTER UPDATE ON `tbl_industries`
--  FOR EACH ROW BEGIN
--    SET @action = 1;
--    IF OLD.industry_name <> NEW.industry_name THEN
--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--   SELECT @action, @client_id := client_id, unit_id, 'industry_name', NEW.industry_name, 'tbl_units'  FROM tbl_units WHERE industry_id=NEW.industry_id;
--   UPDATE tbl_client_replication_status set is_new_data = 1
--   WHERE client_id = @client_id;
--   END IF;

-- END
-- //
-- DELIMITER ;


-- --
-- -- Triggers `tbl_legal_entities`
-- --
-- DROP TRIGGER IF EXISTS `after_tbl_legal_entities_insert`;
-- DELIMITER //
-- CREATE TRIGGER `after_tbl_legal_entities_insert` AFTER INSERT ON `tbl_legal_entities`
--  FOR EACH ROW BEGIN
--    SET @action = 0;


--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--         VALUES (@action,
--                 NEW.client_id,
--                 NEW.legal_entity_id,
--                 'legal_entity_name',
--                 NEW.legal_entity_name,
--                 'tbl_legal_entities');

--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--         VALUES (@action,
--                 NEW.client_id,
--                 NEW.legal_entity_id,
--                 'business_group_id',
--                 NEW.business_group_id,
--                 'tbl_legal_entities');

--     UPDATE tbl_client_replication_status set is_new_data = 1
--     WHERE client_id = NEW.client_id;

-- END
-- //
-- DELIMITER ;
-- DROP TRIGGER IF EXISTS `after_tbl_legal_entities_update`;
-- DELIMITER //
-- CREATE TRIGGER `after_tbl_legal_entities_update` AFTER UPDATE ON `tbl_legal_entities`
--  FOR EACH ROW BEGIN
--    SET @action = 1;


--    IF OLD.legal_entity_name <> NEW.legal_entity_name THEN
--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--         VALUES (@action,
--                 NEW.client_id,
--                 NEW.legal_entity_id,
--                 'legal_entity_name',
--                 NEW.legal_entity_name,
--                 'tbl_legal_entities');
--     UPDATE tbl_client_replication_status set is_new_data = 1
--     WHERE client_id = NEW.client_id;
--    END IF;

-- END
-- //
-- DELIMITER ;

-- --
-- -- Triggers `tbl_statutory_mappings`
-- --
-- DROP TRIGGER IF EXISTS `after_tbl_statutory_mappings_update`;
-- DELIMITER //
-- CREATE TRIGGER `after_tbl_statutory_mappings_update` AFTER UPDATE ON `tbl_statutory_mappings`
--  FOR EACH ROW BEGIN
--    SET @action = 1;
--    IF OLD.statutory_mapping <> NEW.statutory_mapping THEN
--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--   SELECT @action, 0, compliance_id, 'statutory_mapping', NEW.statutory_mapping, 'tbl_compliances'  FROM tbl_compliances WHERE statutory_mapping_id=NEW.statutory_mapping_id;
--     UPDATE tbl_client_replication_status set is_new_data = 1 where
--     client_id in (select client_id from tbl_client_domains where domain_id = OLD.domain_id);
--   END IF;
-- END
-- //
-- DELIMITER ;


-- --
-- -- Triggers `tbl_statutory_notifications_log`
-- --
-- DROP TRIGGER IF EXISTS `after_tbl_statutory_notifications_log_insert`;
-- DELIMITER //
-- CREATE TRIGGER `after_tbl_statutory_notifications_log_insert` AFTER INSERT ON `tbl_statutory_notifications_log`
--  FOR EACH ROW BEGIN
--    SET @action = 0;
--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--         VALUES (@action,
--                 0,
--                 NEW.statutory_notification_id,
--                 'country_name',
--                 NEW.country_name,
--                 'tbl_statutory_notifications_log');
--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--         VALUES (@action,
--                 0,
--                 NEW.statutory_notification_id,
--                 'domain_name',
--                 NEW.domain_name,
--                 'tbl_statutory_notifications_log');
--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--         VALUES (@action,
--                 0,
--                 NEW.statutory_notification_id,
--                 'industry_name',
--                 NEW.industry_name,
--                 'tbl_statutory_notifications_log');
--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--         VALUES (@action,
--                 0,
--                 NEW.statutory_notification_id,
--                 'statutory_nature',
--                 NEW.statutory_nature,
--                 'tbl_statutory_notifications_log');
--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--         VALUES (@action,
--                 0,
--                 NEW.statutory_notification_id,
--                 'statutory_provision',
--                 NEW.statutory_provision,
--                 'tbl_statutory_notifications_log');
--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--         VALUES (@action,
--                 0,
--                 NEW.statutory_notification_id,
--                 'applicable_location',
--                 NEW.applicable_location,
--                 'tbl_statutory_notifications_log');
--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--         VALUES (@action,
--                 0,
--                 NEW.statutory_notification_id,
--                 'notification_text',
--                 NEW.notification_text,
--                 'tbl_statutory_notifications_log');


-- END
-- //
-- DELIMITER ;
-- DROP TRIGGER IF EXISTS `after_tbl_statutory_notifications_log_update`;
-- DELIMITER //
-- CREATE TRIGGER `after_tbl_statutory_notifications_log_update` AFTER UPDATE ON `tbl_statutory_notifications_log`
--  FOR EACH ROW BEGIN
--    SET @action = 1;
--    IF OLD.country_name <> NEW.country_name THEN
--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--         VALUES (@action,
--                 0,
--                 NEW.statutory_notification_id,
--                 'country_name',
--                 NEW.country_name,
--                 'tbl_statutory_notifications_log');
--    END IF;


--    IF OLD.domain_name <> NEW.domain_name THEN
--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--         VALUES (@action,
--                 0,
--                 NEW.statutory_notification_id,
--                 'domain_name',
--                 NEW.domain_name,
--                 'tbl_statutory_notifications_log');
--    END IF;


--    IF OLD.industry_name <> NEW.industry_name THEN
--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--         VALUES (@action,
--                 0,
--                 NEW.statutory_notification_id,
--                 'industry_name',
--                 NEW.industry_name,
--                 'tbl_statutory_notifications_log');
--    END IF;


--    IF OLD.statutory_nature <> NEW.statutory_nature THEN
--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--         VALUES (@action,
--                 0,
--                 NEW.statutory_notification_id,
--                 'statutory_nature',
--                 NEW.statutory_nature,
--                 'tbl_statutory_notifications_log');
--    END IF;


--    IF OLD.statutory_provision <> NEW.statutory_provision THEN
--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--         VALUES (@action,
--                 0,
--                 NEW.statutory_notification_id,
--                 'statutory_provision',
--                 NEW.statutory_provision,
--                 'tbl_statutory_notifications_log');
--    END IF;

--    IF OLD.applicable_location <> NEW.applicable_location THEN
--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--         VALUES (@action,
--                 0,
--                 NEW.statutory_notification_id,
--                 'applicable_location',
--                 NEW.applicable_location,
--                 'tbl_statutory_notifications_log');
--    END IF;

--    IF OLD.notification_text <> NEW.notification_text THEN
--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--         VALUES (@action,
--                 0,
--                 NEW.statutory_notification_id,
--                 'notification_text',
--                 NEW.notification_text,
--                 'tbl_statutory_notifications_log');
--    END IF;

-- END
-- //
-- DELIMITER ;


-- --
-- -- Triggers `tbl_statutory_notifications_units`
-- --
-- DROP TRIGGER IF EXISTS `after_tbl_statutory_notifications_units_insert`;
-- DELIMITER //
-- CREATE TRIGGER `after_tbl_statutory_notifications_units_insert` AFTER INSERT ON `tbl_statutory_notifications_units`
--  FOR EACH ROW BEGIN
--    SET @action = 0;

--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--         VALUES (@action,
--                 NEW.client_id,
--                 NEW.statutory_notification_unit_id,
--                 'statutory_notification_id',
--                 NEW.statutory_notification_id,
--                 'tbl_statutory_notifications_units');


--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--         VALUES (@action,
--                 NEW.client_id,
--                 NEW.statutory_notification_unit_id,
--                 'business_group_id',
--                 NEW.business_group_id,
--                 'tbl_statutory_notifications_units');


--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--         VALUES (@action,
--                 NEW.client_id,
--                 NEW.statutory_notification_unit_id,
--                 'legal_entity_id',
--                 NEW.legal_entity_id,
--                 'tbl_statutory_notifications_units');


--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--         VALUES (@action,
--                 NEW.client_id,
--                 NEW.statutory_notification_unit_id,
--                 'division_id',
--                 NEW.division_id,
--                 'tbl_statutory_notifications_units');


--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--         VALUES (@action,
--                 NEW.client_id,
--                 NEW.statutory_notification_unit_id,
--                 'unit_id',
--                 NEW.unit_id,
--                 'tbl_statutory_notifications_units');

--     UPDATE tbl_client_replication_status set is_new_data = 1
--     WHERE client_id = NEW.client_id;

-- END
-- //
-- DELIMITER ;
-- DROP TRIGGER IF EXISTS `after_tbl_statutory_notifications_units_update`;
-- DELIMITER //
-- CREATE TRIGGER `after_tbl_statutory_notifications_units_update` AFTER UPDATE ON `tbl_statutory_notifications_units`
--  FOR EACH ROW BEGIN
--    SET @action = 1;


--    IF OLD.statutory_notification_id <> NEW.statutory_notification_id THEN
--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--         VALUES (@action,
--                 NEW.client_id,
--                 NEW.statutory_notification_unit_id,
--                 'statutory_notification_id',
--                 NEW.statutory_notification_id,
--                 'tbl_statutory_notifications_units');
--    END IF;


--    IF OLD.business_group_id <> NEW.business_group_id THEN
--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--         VALUES (@action,
--                 NEW.client_id,
--                 NEW.statutory_notification_unit_id,
--                 'business_group_id',
--                 NEW.business_group_id,
--                 'tbl_statutory_notifications_units');
--    END IF;


--    IF OLD.legal_entity_id <> NEW.legal_entity_id THEN
--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--         VALUES (@action,
--                 NEW.client_id,
--                 NEW.statutory_notification_unit_id,
--                 'legal_entity_id',
--                 NEW.legal_entity_id,
--                 'tbl_statutory_notifications_units');
--    END IF;


--    IF OLD.division_id <> NEW.division_id THEN
--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--         VALUES (@action,
--                 NEW.client_id,
--                 NEW.statutory_notification_unit_id,
--                 'division_id',
--                 NEW.division_id,
--                 'tbl_statutory_notifications_units');
--    END IF;


--    IF OLD.unit_id <> NEW.unit_id THEN
--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--         VALUES (@action,
--                 NEW.client_id,
--                 NEW.statutory_notification_unit_id,
--                 'unit_id',
--                 NEW.unit_id,
--                 'tbl_statutory_notifications_units');
--    END IF;

--    UPDATE tbl_client_replication_status set is_new_data = 1
--    WHERE client_id = NEW.client_id;

-- END
-- //
-- DELIMITER ;


-- --
-- -- Triggers `tbl_units`
-- --
-- DROP TRIGGER IF EXISTS `after_tbl_units_insert`;
-- DELIMITER //
-- CREATE TRIGGER `after_tbl_units_insert` AFTER INSERT ON `tbl_units`
--  FOR EACH ROW BEGIN
--    SET @action = 0;
--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--   SELECT @action, NEW.client_id, NEW.unit_id, 'industry_name', industry_name, 'tbl_units'  FROM tbl_industries WHERE industry_id=NEW.industry_id;

--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--   SELECT @action, NEW.client_id, NEW.unit_id, 'geography', parent_names, 'tbl_units'  FROM tbl_geographies WHERE geography_id=NEW.geography_id;

--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--         VALUES (@action,
--                 NEW.client_id,
--                 NEW.unit_id,
--                 'business_group_id',
--                 NEW.business_group_id,
--                 'tbl_units');
--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--         VALUES (@action,
--                 NEW.client_id,
--                 NEW.unit_id,
--                 'legal_entity_id',
--                 NEW.legal_entity_id,
--                 'tbl_units');

--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--         VALUES (@action,
--                 NEW.client_id,
--                 NEW.unit_id,
--                 'division_id',
--                 NEW.division_id,
--                 'tbl_units');

--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--         VALUES (@action,
--                 NEW.client_id,
--                 NEW.unit_id,
--                 'country_id',
--                 NEW.country_id,
--                 'tbl_units');
--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--         VALUES (@action,
--                 NEW.client_id,
--                 NEW.unit_id,
--                 'unit_code',
--                 NEW.unit_code,
--                 'tbl_units');
--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--         VALUES (@action,
--                 NEW.client_id,
--                 NEW.unit_id,
--                 'unit_name',
--                 NEW.unit_name,
--                 'tbl_units');
--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--         VALUES (@action,
--                 NEW.client_id,
--                 NEW.unit_id,
--                 'address',
--                 NEW.address,
--                 'tbl_units');

--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--         VALUES (@action,
--                 NEW.client_id,
--                 NEW.unit_id,
--                 'postal_code',
--                 NEW.postal_code,
--                 'tbl_units');
--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--         VALUES (@action,
--                 NEW.client_id,
--                 NEW.unit_id,
--                 'domain_ids',
--                 NEW.domain_ids,
--                 'tbl_units');
--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--         VALUES (@action,
--                 NEW.client_id,
--                 NEW.unit_id,
--                 'is_active',
--                 NEW.is_active,
--                 'tbl_units');

--     UPDATE tbl_client_replication_status set is_new_data = 1
--     WHERE client_id = NEW.client_id;

-- END
-- //
-- DELIMITER ;

-- DROP TRIGGER IF EXISTS `after_tbl_units_update`;
-- DELIMITER //
-- CREATE TRIGGER `after_tbl_units_update` AFTER UPDATE ON `tbl_units`
--  FOR EACH ROW BEGIN
--    SET @action = 1;
--    IF OLD.industry_id <> NEW.industry_id THEN
--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--   SELECT @action, NEW.client_id, NEW.unit_id, 'industry_name', industry_name, 'tbl_units'  FROM tbl_industries WHERE industry_id=NEW.industry_id;
--    END IF;

--    IF OLD.geography_id <> NEW.geography_id THEN

--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--   SELECT @action, NEW.client_id, NEW.unit_id, 'geography', parent_names, 'tbl_units'  FROM tbl_geographies WHERE geography_id=NEW.geography_id;
--    END IF;

--    IF OLD.business_group_id <> NEW.business_group_id THEN
--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--         VALUES (@action,
--                 NEW.client_id,
--                 NEW.unit_id,
--                 'business_group_id',
--                 NEW.business_group_id,
--                 'tbl_units');
--    END IF;

--    IF OLD.legal_entity_id <> NEW.legal_entity_id THEN
--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--         VALUES (@action,
--                 NEW.client_id,
--                 NEW.unit_id,
--                 'legal_entity_id',
--                 NEW.legal_entity_id,
--                 'tbl_units');
--    END IF;

--    IF OLD.division_id <> NEW.division_id THEN
--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--         VALUES (@action,
--                 NEW.client_id,
--                 NEW.unit_id,
--                 'division_id',
--                 NEW.division_id,
--                 'tbl_units');
--    END IF;

--    IF OLD.country_id <> NEW.country_id THEN
--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--         VALUES (@action,
--                 NEW.client_id,
--                 NEW.unit_id,
--                 'country_id',
--                 NEW.country_id,
--                 'tbl_units');
--    END IF;

--    IF OLD.unit_code <> NEW.unit_code THEN
--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--         VALUES (@action,
--                 NEW.client_id,
--                 NEW.unit_id,
--                 'unit_code',
--                 NEW.unit_code,
--                 'tbl_units');
--    END IF;

--    IF OLD.unit_name <> NEW.unit_name THEN
--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--         VALUES (@action,
--                 NEW.client_id,
--                 NEW.unit_id,
--                 'unit_name',
--                 NEW.unit_name,
--                 'tbl_units');
--    END IF;

--    IF OLD.address <> NEW.address THEN
--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--         VALUES (@action,
--                 NEW.client_id,
--                 NEW.unit_id,
--                 'address',
--                 NEW.address,
--                 'tbl_units');
--    END IF;

--    IF OLD.postal_code <> NEW.postal_code THEN
--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--         VALUES (@action,
--                 NEW.client_id,
--                 NEW.unit_id,
--                 'postal_code',
--                 NEW.postal_code,
--                 'tbl_units');
--    END IF;

--    IF OLD.domain_ids <> NEW.domain_ids THEN
--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--         VALUES (@action,
--                 NEW.client_id,
--                 NEW.unit_id,
--                 'domain_ids',
--                 NEW.domain_ids,
--                 'tbl_units');
--    END IF;

--    IF OLD.is_active <> NEW.is_active THEN
--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--         VALUES (@action,
--                 NEW.client_id,
--                 NEW.unit_id,
--                 'is_active',
--                 NEW.is_active,
--                 'tbl_units');
--    END IF;

--     UPDATE tbl_client_replication_status set is_new_data = 1
--     WHERE client_id = NEW.client_id;

-- END
-- //
-- DELIMITER ;


-- --
-- -- Trigger after_tbl_countries_update
-- --

-- DROP TRIGGER IF EXISTS `after_tbl_countries_update`;
-- DELIMITER //
-- CREATE TRIGGER `after_tbl_countries_update` AFTER UPDATE ON `tbl_countries`
--  FOR EACH ROW BEGIN
--    SET @action = 1;

--    IF OLD.country_name <> NEW.country_name THEN
--    INSERT INTO tbl_audit_log(action,
--                             client_id,
--                             tbl_auto_id,
--                             column_name,
--                             value,
--                             tbl_name)
--         VALUES (@action,
--                 0,
--                 NEW.country_id,
--                 'country_name',
--                 NEW.country_name,
--                 "tbl_countries"
--                 );
--     END IF;
--     UPDATE tbl_client_replication_status set is_new_data = 1 where
--     client_id in (select client_id from tbl_client_countries where country_id = NEW.country_id);
-- END
-- //
-- DELIMITER ;

-- --
-- -- Trigger after_tbl_domains_update
-- --

-- DROP TRIGGER IF EXISTS `after_tbl_domains_update`;
-- DELIMITER //
-- CREATE TRIGGER `after_tbl_domains_update` AFTER UPDATE ON `tbl_domains`
--  FOR EACH ROW BEGIN
--    SET @action = 1;

--    IF OLD.domain_name <> NEW.domain_name THEN
--    INSERT INTO tbl_audit_log(action,
--                             client_id,
--                             tbl_auto_id,
--                             column_name,
--                             value,
--                             tbl_name)
--         VALUES (@action,
--                 0,
--                 NEW.domain_id,
--                 'domain_name',
--                 NEW.domain_name,
--                 "tbl_domains"
--                 );
--     UPDATE tbl_client_replication_status set is_new_data = 1 where
--     client_id in (select client_id from tbl_client_domains where domain_id = NEW.domain_id);
--     END IF;
-- END
-- //
-- DELIMITER ;
