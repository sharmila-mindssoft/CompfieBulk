USE `compfie_knowledge`;

-- DELETE FROM tbl_form_category;
INSERT INTO tbl_form_category VALUES(1, "IT Team");
INSERT INTO tbl_form_category VALUES(2, "Knowledge Team");
INSERT INTO tbl_form_category VALUES(3, "Techno Functional Team");
INSERT INTO tbl_form_category VALUES(4, "Common");

-- DELETE FROM tbl_form_type;
INSERT INTO tbl_form_type VALUES(1, "Master");
INSERT INTO tbl_form_type VALUES(2, "Transaction");
INSERT INTO tbl_form_type VALUES(3, "Report");
INSERT INTO tbl_form_type VALUES(4, "Settings");

-- DELETE FROM tbl_forms
-- fields(form_id, form_category_id, form_type_id, form_name, form_url, form_order, parent_menu)

-- mirror_knowledge
-- Admin
INSERT INTO tbl_forms VALUES(1, 4, 1,  'Country', '/knowledge/country-master', 1,  null);
INSERT INTO tbl_forms VALUES(2, 4, 1,  'Domain', '/knowledge/domain-master', 2, null);
INSERT INTO tbl_forms VALUES(3, 1, 1,  'User Group', '/knowledge/user-group-master', 3, null);
INSERT INTO tbl_forms VALUES(4, 1, 1,  'User', '/knowledge/user-master', 4, null);
-- knowledge

INSERT INTO tbl_forms VALUES(5, 2, 1, 'Geography Level Master', '/knowledge/geography-level-master', 5, 'Geography');
INSERT INTO tbl_forms VALUES(6, 2, 1, 'Geography Master', '/knowledge/geography-master', 6, 'Geography');
INSERT INTO tbl_forms VALUES(7, 2, 1, 'Industry Master', '/knowledge/industry-master', 7, null);
INSERT INTO tbl_forms VALUES(8, 2, 1, 'Statutory Nature Master', '/knowledge/statutory-nature-master', 8, 'Statutory');
INSERT INTO tbl_forms VALUES(9, 2, 1, 'Statutory Level Master', '/knowledge/statutory-level-master', 9, 'Statutory');
INSERT INTO tbl_forms VALUES(10, 2, 2, 'Statutory Mapping', '/knowledge/statutory-mapping', 10, null);
INSERT INTO tbl_forms VALUES(11, 2, 2, 'Approve Statutory Mapping', '/knowledge/approve-statutory-mapping', 11, null);
INSERT INTO tbl_forms VALUES(12, 2, 3, 'Statutory Mapping Report', '/knowledge/statutory-mapping-report', 12, null);
INSERT INTO tbl_forms VALUES(13, 2, 3, 'Country Report', '/knowledge/country-report', 13, 'Master');
INSERT INTO tbl_forms VALUES(14, 2, 3, 'Domain Report', '/knowledge/domain-report', 14, 'Master');
INSERT INTO tbl_forms VALUES(15, 2, 3, 'Geography Report', '/knowledge/geography-report', 15, 'Master');
INSERT INTO tbl_forms VALUES(16, 2, 3, 'Industry Report', '/knowledge/industry-report', 16, 'Master');
INSERT INTO tbl_forms VALUES(17, 2, 3, 'Statutory Nature Report', '/knowledge/statutory-nature-report', 17, 'Master');
-- Techno
INSERT INTO tbl_forms VALUES(18, 3, 1, 'Client Master', '/knowledge/client-master', 18, null);
INSERT INTO tbl_forms VALUES(19, 3, 1, 'Client Unit', '/knowledge/client-unit', 19, null);
INSERT INTO tbl_forms VALUES(20, 3, 1, 'Client Profile', '/knowledge/client-profile', 20, null);
INSERT INTO tbl_forms VALUES(21, 3, 2, 'Assign Statutory', '/knowledge/assign-statutory', 21, null);
INSERT INTO tbl_forms VALUES(22, 3, 3, 'Client Details Report', '/knowledge/client-details-report', 22, null);
INSERT INTO tbl_forms VALUES(23, 3, 3, 'Assigned Statutory', '/knowledge/assigned-statutory-report', 23, null);
INSERT INTO tbl_forms VALUES(24, 3, 3, 'Compliance List', '/knowledge/compliance-task-list', 24, null);
INSERT INTO tbl_forms VALUES(25, 3, 3, 'Statutory Notifications List', '/knowledge/statutory-notifications-list', 25, null);
-- common
INSERT INTO tbl_forms VALUES(26, 4, 3, 'Audit Trail', '/knowledge/audit-trail', 26, null);

-- tbl_admin
-- username, password -- 123456
INSERT INTO tbl_admin  VALUES("admin", "7ecfd14ba1b0d6800688a0a317a5a331");

-- tbl_session_types
INSERT INTO tbl_session_types VALUES(1, "web");
INSERT INTO tbl_session_types VALUES(2, "android");
INSERT INTO tbl_session_types VALUES(3, "ios");
INSERT INTO tbl_session_types VALUES(4, "blackberry");

-- tbl_compliance_duration_type
INSERT INTO tbl_compliance_duration_type VALUES(1, "Day(s)");
INSERT INTO tbl_compliance_duration_type VALUES(2, "Hour(s)");

-- tbl_compliance_repeat_type
INSERT INTO tbl_compliance_repeat_type VALUES(1, "Day(s)");
INSERT INTO tbl_compliance_repeat_type VALUES(2, "Month(s)");
INSERT INTO tbl_compliance_repeat_type VALUES(3, "Year(s)");

-- tbl_compliance_frequency
INSERT INTO tbl_compliance_frequency VALUES(1, "One Time");
INSERT INTO tbl_compliance_frequency VALUES(2, "Periodical");
INSERT INTO tbl_compliance_frequency VALUES(3, "Review");
INSERT INTO tbl_compliance_frequency VALUES(4, "On Occurrence");

-- tbl_machines
INSERT INTO `tbl_machines` (`machine_id`, `ip`, `port`, `client_ids`, `server_full`) VALUES
(1, '127.0.0.1', 8081, '1', 0);

-- tbl_database_server
INSERT INTO `tbl_database_server` (`ip`, `server_username`, `server_password`) VALUES
('127.0.0.1', 'root', '123456');
