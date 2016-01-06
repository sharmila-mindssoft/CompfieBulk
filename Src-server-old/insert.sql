USE `mirror_knowledge`;

-- -- DELETE FROM tbl_forms;
-- INSERT INTO tbl_forms VALUES(1, 'User Group Master', '/user-group-e', 1, 'master', 'it', 0, null);
-- INSERT INTO tbl_forms VALUES(2, 'User Master', '/user-master', 2, 'master', 'it', 0, null);
-- INSERT INTO tbl_forms VALUES(3, 'Country Master', '/country-master', 3, 'master', 'it', 0, null);
-- INSERT INTO tbl_forms VALUES(4, 'Domain Master', '/domain-master', 4, 'master', 'it', 0, null);
-- INSERT INTO tbl_forms VALUES(5, 'Industry Master', 'industry-master', 5, 'master', 'knowledge', 0, null);
-- INSERT INTO tbl_forms VALUES(6, 'Geography Levels Master', 'geography-levels-master', 6, 'master', 'knowledge', 0, 'Geography');
-- INSERT INTO tbl_forms VALUES(7, 'Geography Master', 'geography-master', 7, 'master', 'knowledge', 0, 'Geography');
-- INSERT INTO tbl_forms VALUES(8, 'Statutory Nature Master', 'statutory-nature-master', 8, 'master', 'knowledge', 0, 'Statutory');
-- INSERT INTO tbl_forms VALUES(9, 'Statutory Levels Master', 'statutory-levels-master', 9, 'master', 'knowledge', 0, 'Statutory');
-- INSERT INTO tbl_forms VALUES(10, 'Client Master', 'client-master', 10, 'master', 'techno', 0, null);
-- INSERT INTO tbl_forms VALUES(11, 'Client Unit Creation', 'client-unit-creation', 11, 'master', 'techno', 0, null);
-- INSERT INTO tbl_forms VALUES(12, 'Client Profile', 'client-profile', 12, 'master', 'techno', 0, null);
-- INSERT INTO tbl_forms VALUES(13, 'Service Provider', 'service-provider', 13, 'master', 'client', 0, null);
-- INSERT INTO tbl_forms VALUES(14, 'User Privilege', 'user-privilege', 14, 'master', 'client', 0, null);
-- INSERT INTO tbl_forms VALUES(15, 'User', 'user', 15, 'master', 'client', 0, null);
-- INSERT INTO tbl_forms VALUES(16, 'Unit Closure', 'unit-closure', 16, 'master', 'client', 0, null);
-- INSERT INTO tbl_forms VALUES(17, 'Statutory Mapping', 'statutory-mapping', 17, 'transaction', 'knowledge', 0, null);
-- INSERT INTO tbl_forms VALUES(18, 'Approve Statutory Mapping', 'approve-statutory-mapping', 18, 'transaction', 'knowledge', 0, null);
-- INSERT INTO tbl_forms VALUES(19, 'Assign Statutory', 'assign-statutory', 19, 'transaction', 'techno', 0, null);
-- INSERT INTO tbl_forms VALUES(20, 'Statutory Settings', 'statutory-settings', 20, 'transaction', 'client', 0, null);
-- INSERT INTO tbl_forms VALUES(21, 'Assign Compliance', 'assign-compliance', 21, 'transaction', 'client', 0, null);
-- INSERT INTO tbl_forms VALUES(22, 'Reassign Compliance', 'reassign-compliance', 22, 'transaction', 'client', 0, null);
-- INSERT INTO tbl_forms VALUES(23, 'Compliance Approval', 'compliance-approval', 23, 'transaction', 'client', 0, null);
-- INSERT INTO tbl_forms VALUES(24, 'Completed Tasks - Current Year', 'completed-tasks-current-year', 24, 'transaction', 'client', 0, null);
-- INSERT INTO tbl_forms VALUES(25, 'Statutory Mapping Report', 'statutory-mapping-report', 25, 'report', 'knowledge', 0, null);
-- INSERT INTO tbl_forms VALUES(26, 'Country Report', 'country-report', 26, 'report', 'knowledge', 0, 'Master');
-- INSERT INTO tbl_forms VALUES(27, 'Domain Report', 'domain-report', 27, 'report', 'knowledge', 0, 'Master');
-- INSERT INTO tbl_forms VALUES(28, 'Geography Report', 'geography-report', 28, 'report', 'knowledge', 0, 'Master');
-- INSERT INTO tbl_forms VALUES(29, 'Industry Report', 'industry-report', 29, 'report', 'knowledge', 0, 'Master');
-- INSERT INTO tbl_forms VALUES(30, 'Statutory Nature Report', 'statutory-nature-report', 30, 'report', 'knowledge', 0, 'Master');
-- INSERT INTO tbl_forms VALUES(31, 'Client Details Report', 'client-details-report', 31, 'report', 'techno', 0, null);
-- INSERT INTO tbl_forms VALUES(32, 'Assigned Statutory', 'assigned-statutory', 32, 'report', 'techno', 0, null);
-- INSERT INTO tbl_forms VALUES(33, 'Compliance Task List', 'compliance-task-list', 33, 'report', 'techno', 0, null);
-- INSERT INTO tbl_forms VALUES(34, 'Statutory Notifications List', 'statutory-notifications-list', 34, 'report', 'techno', 0, null);
-- INSERT INTO tbl_forms VALUES(35, 'Charts', 'charts', 35, 'report', 'client', 0, null);
-- INSERT INTO tbl_forms VALUES(36, 'Compliance Details', 'compliance-details', 36, 'report', 'client', 0, null);
-- INSERT INTO tbl_forms VALUES(37, 'Risk Report', 'risk-report', 37, 'report', 'client', 0, null);
-- INSERT INTO tbl_forms VALUES(38, 'Service Provider wise Compliance', 'service-provider-wise-compliance', 38, 'report', 'client', 0, null);
-- INSERT INTO tbl_forms VALUES(39, 'Assignee wise Compliance', 'assignee-wise-compliance', 39, 'report', 'client', 0, null);
-- INSERT INTO tbl_forms VALUES(40, 'Unit wise Compliance', 'unit-wise-compliance', 40, 'report', 'client', 0, null);
-- INSERT INTO tbl_forms VALUES(41, 'Compliance Task Applicability Status', 'compliance-task-applicability-status', 41, 'report', 'client', 0, null);
-- INSERT INTO tbl_forms VALUES(42, 'Unit Details', 'unit-details', 42, 'report', 'client', 0, null);
-- INSERT INTO tbl_forms VALUES(43, 'Compliance Activity Report', 'compliance-activity-report', 43, 'report', 'client', 0, null);
-- INSERT INTO tbl_forms VALUES(44, 'Reassigned History', 'reassigned-history', 44, 'report', 'client', 0, null);
-- INSERT INTO tbl_forms VALUES(45, 'Statutory Notifications List', 'statutory-notifications-list', 45, 'report', 'client', 0, null);
-- INSERT INTO tbl_forms VALUES(46, 'Login Trace', 'login-trace', 46, 'report', 'client', 0, null);
-- INSERT INTO tbl_forms VALUES(47, 'Audit Trail', 'audit-trail', 47, 'report', 'common', 1, null);
-- INSERT INTO tbl_forms VALUES(48, 'Settings', 'settings', 48, 'setting', 'client', 1, null);


-- -- DELETE FROM tbl_users;
-- INSERT INTO tbl_users VALUES(1, "admin@compliance-mirror.com", "aparajitha_123_admin", null, 1, null, 1448455226, null, 1448455226);
-- INSERT INTO tbl_users VALUES(2, "dl@gmail.com", "dl", null, 1, null, 1448455226, null, 1448455226);

-- -- DELETE FROM tbl_user_groups;
-- INSERT INTO tbl_user_groups VALUES(1, "Administrator", "it", "1,2,3,4", 1, null, 1448455226, null, 1448455226);
-- INSERT INTO tbl_user_groups VALUES(2, "Knowledge", "knowledge", "5,6,7,8,9,17,25,26,27,28,29", 1, null, 1448455226, null, 1448455226);

-- -- DELETE FROM tbl_user_details;
-- INSERT INTO tbl_user_details VALUES(1, "admin@compliance-mirror.com", null, 1, 1, "it", "Administrator", "", null, null, null, null, null, null, 1, null, 1448455226, null, 1448455226);
-- INSERT INTO tbl_user_details VALUES(2, "dl@gmail.com", null, 1, 2, "knowledge", "Knowledge User", "", null, null, null, null, null, null, 1, null, 1448455226, null, 1448455226);

--DELETE FROM tbl_form_category;
INSERT INTO tbl_form_category VALUES(1, "IT Team");
INSERT INTO tbl_form_category VALUES(2, "Knowledge Team");
INSERT INTO tbl_form_category VALUES(3, "Techno Functional Team");
INSERT INTO tbl_form_category VALUES(4, "Common");

--DELETE FROM tbl_form_type;
INSERT INTO tbl_form_type VALUES(1, "Master");
INSERT INTO tbl_form_type VALUES(2, "Transaction");
INSERT INTO tbl_form_type VALUES(3, "Report");
INSERT INTO tbl_form_type VALUES(4, "Settings");

--DELETE FROM tbl_forms
-- fields(form_id, form_category_id, form_type_id, form_name, form_url, form_order, parent_menu)

--mirror_knowledge
#Admin
INSERT INTO tbl_forms VALUES(1, 4, 1,  'Country', '/country-master', 1,  null);
INSERT INTO tbl_forms VALUES(2, 4, 1,  'Domain', '/domain-master', 2, null);
INSERT INTO tbl_forms VALUES(3, 1, 1,  'User Group', '/user-group-master', 3, null);
INSERT INTO tbl_forms VALUES(4, 1, 1,  'User', '/user-master', 4, null);
#knowledge
INSERT INTO tbl_forms VALUES(5, 2, 1, 'Geography Levels Master', '/geography-level-master', 5, 'Geography');
INSERT INTO tbl_forms VALUES(6, 2, 1, 'Geography Master', '/geography-master', 6, 'Geography');
INSERT INTO tbl_forms VALUES(7, 2, 1, 'Industry Master', '/industry-master', 7, null);
INSERT INTO tbl_forms VALUES(8, 2, 1, 'Statutory Nature Master', '/statutory-nature-master', 8, 'Statutory');
INSERT INTO tbl_forms VALUES(9, 2, 1, 'Statutory Levels Master', '/statutory-level-master', 9, 'Statutory');
INSERT INTO tbl_forms VALUES(10, 2, 2, 'Statutory Mapping', '/statutory-mapping', 10, null);
INSERT INTO tbl_forms VALUES(11, 2, 2, 'Approve Statutory Mapping', '/approve-statutory-mapping', 11, null);
INSERT INTO tbl_forms VALUES(12, 2, 3, 'Statutory Mapping Report', '/statutory-mapping-report', 12, null);
INSERT INTO tbl_forms VALUES(13, 2, 3, 'Country Report', '/country-report', 13, 'Master');
INSERT INTO tbl_forms VALUES(14, 2, 3, 'Domain Report', '/domain-report', 14, 'Master');
INSERT INTO tbl_forms VALUES(15, 2, 3, 'Geography Report', '/geography-report', 15, 'Master');
INSERT INTO tbl_forms VALUES(16, 2, 3, 'Industry Report', '/industry-report', 16, 'Master');
INSERT INTO tbl_forms VALUES(17, 2, 3, 'Statutory Nature Report', '/statutory-nature-report', 17, 'Master');
#Techno
INSERT INTO tbl_forms VALUES(18, 3, 1, 'Client Master', '/client-master', 18, null);
INSERT INTO tbl_forms VALUES(19, 3, 1, 'Client Unit Creation', '/client-unit-creation', 19, null);
INSERT INTO tbl_forms VALUES(20, 3, 1, 'Client Profile', '/client-profile', 20, null);
INSERT INTO tbl_forms VALUES(21, 3, 2, 'Assign Statutory', '/assign-statutory', 21, null);
INSERT INTO tbl_forms VALUES(22, 3, 3, 'Client Details Report', '/client-details-report', 22, null);
INSERT INTO tbl_forms VALUES(23, 3, 3, 'Assigned Statutory', '/assigned-statutory', 23, null);
INSERT INTO tbl_forms VALUES(24, 3, 3, 'Compliance List', '/compliance-task-list', 24, null);
INSERT INTO tbl_forms VALUES(25, 3, 3, 'Statutory Notifications List', '/statutory-notifications-list', 25, null);

#common
INSERT INTO tbl_forms VALUES(26, 4, 3, 'Audit Trail', '/audit-trail', 26, null);

--mirror.client

--DELETE FROM tbl_form_type;
INSERT INTO tbl_form_type VALUES(1, "Home");
INSERT INTO tbl_form_type VALUES(2, "Master");
INSERT INTO tbl_form_type VALUES(3, "Transaction");
INSERT INTO tbl_form_type VALUES(4, "Report");
INSERT INTO tbl_form_type VALUES(5, "Settings");

-- fields(form_id, form_type_id, form_name, form_url, form_order, parent_menu, is_admin)
INSERT INTO tbl_forms VALUES(1, 1, 'Dashboard', '/home', 1, null, 0);
INSERT INTO tbl_forms VALUES(2, 2, 'Service Provider', '/service-provider', 2, null, 1);
INSERT INTO tbl_forms VALUES(3, 2, 'User Privilege', '/user-privilege', 3, null, 1);
INSERT INTO tbl_forms VALUES(4, 2, 'User', '/user', 4, null, 1);
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
INSERT INTO tbl_forms VALUES(15, 4, 'Service Provider wise Compliance', '/service-provider-wise-compliance', 15, "Compliance List", 0);
INSERT INTO tbl_forms VALUES(16, 4, 'Assignee wise Compliance', '/assignee-wise-compliance', 16, "Compliance List", 0);
INSERT INTO tbl_forms VALUES(17, 4, 'Unit wise Compliance', '/unit-wise-compliance', 17, "Compliance List", 0);
INSERT INTO tbl_forms VALUES(18, 4, 'Compliance Task Applicability Status', '/compliance-task-applicability-status', 18, null, 0);
INSERT INTO tbl_forms VALUES(19, 4, 'Unit Details', '/unit-details', 19, null, 0);
INSERT INTO tbl_forms VALUES(20, 4, 'Compliance Activity Report', '/compliance-activity-report', 20, null, 0);
INSERT INTO tbl_forms VALUES(21, 4, 'Reassigned History', '/reassigned-history', 21, null, 0);
INSERT INTO tbl_forms VALUES(22, 4, 'Statutory Notifications List', '/statutory-notifications-list', 22, null, 0);
INSERT INTO tbl_forms VALUES(23, 4, 'Login Trace', '/login-trace', 23, null, 1);
INSERT INTO tbl_forms VALUES(24, 4, 'Audit Trail', '/audit-trail', 24, null, 1);
INSERT INTO tbl_forms VALUES(25, 4, 'Settings', '/settings',  25, null, 1);

--tbl_admin
-- username, password -- 123456
INSERT INTO tbl_admin  VALUES("admin", "e10adc3949ba59abbe56e057f20f883e");

--DELETE FROM tbl_users
--field user_id, user_group_id ,email_id ,password, employee_name, 
-- employee_code, contact_no, address, designation, is_active, created_by, created_on, updated_by, updated_on 


--tbl_session_types
--DELETE FROM tbl_session_types
-- values = session_type_id, session_type
INSERT INTO tbl_session_types VALUES(1, "web");
INSERT INTO tbl_session_types VALUES(2, "andoird");
INSERT INTO tbl_session_types VALUES(3, "ios");
INSERT INTO tbl_session_types VALUES(4, "blackberry");


--tbl_compliance_duration_type
INSERT INTO tbl_compliance_duration_type VALUES(1, "Day(s)");
INSERT INTO tbl_compliance_duration_type VALUES(2, "Hour(s)");

--tbl_compliance_repeat_type
INSERT INTO tbl_compliance_repeat_type VALUES(1, "Day(s)");
INSERT INTO tbl_compliance_repeat_type VALUES(2, "Month(s)");
INSERT INTO tbl_compliance_repeat_type VALUES(3, "Year(s)");

--tbl_compliance_frequency
INSERT INTO tbl_compliance_frequency VALUES(1, "One Time");
INSERT INTO tbl_compliance_frequency VALUES(2, "Periodical");
INSERT INTO tbl_compliance_frequency VALUES(3, "Review");
INSERT INTO tbl_compliance_frequency VALUES(4, "On Occurrence");

--tbl_user_groups
INSERT INTO tbl_user_groups(user_group_id, form_category_id, user_group_name, form_ids, is_active) VALUES(1, 2, "knowledge", "5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16", 1)

--tbl_users
INSERT INTO tbl_users(user_id, user_group_id, email_id, password, employee_name ) 
VALUES (1, 1, 'usha@mindssoft.com', 'e10adc3949ba59abbe56e057f20f883e', 'dummy')

--tbl_user_sessions
INSERT INTO tbl_user_sessions(session_token, user_id, session_type_id) VALUES ("12c94b934d5f4b5ebebd4471d8b29cb8", 0, 1);
INSERT INTO tbl_user_sessions(session_token, user_id, session_type_id) VALUES ("b4c59894336c4ee3b598f5e4bd2b276b", 1, 1);
