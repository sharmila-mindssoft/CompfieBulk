USE `mirror_knowledge`;

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
# Admin
INSERT INTO tbl_forms VALUES(1, 4, 1,  'Country', '/knowledge/country-master', 1,  null);
INSERT INTO tbl_forms VALUES(2, 4, 1,  'Domain', '/knowledge/domain-master', 2, null);
INSERT INTO tbl_forms VALUES(3, 1, 1,  'User Group', '/knowledge/user-group-master', 3, null);
INSERT INTO tbl_forms VALUES(4, 1, 1,  'User', '/knowledge/user-master', 4, null);
# knowledge

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
# Techno
INSERT INTO tbl_forms VALUES(18, 3, 1, 'Client Master', '/knowledge/client-master', 18, null);
INSERT INTO tbl_forms VALUES(19, 3, 1, 'Client Unit', '/knowledge/client-unit', 19, null);
INSERT INTO tbl_forms VALUES(20, 3, 1, 'Client Profile', '/knowledge/client-profile', 20, null);
INSERT INTO tbl_forms VALUES(21, 3, 2, 'Assign Statutory', '/knowledge/assign-statutory', 21, null);
INSERT INTO tbl_forms VALUES(22, 3, 3, 'Client Details Report', '/knowledge/client-details-report', 22, null);
INSERT INTO tbl_forms VALUES(23, 3, 3, 'Assigned Statutory', '/knowledge/assigned-statutory-report', 23, null);
INSERT INTO tbl_forms VALUES(24, 3, 3, 'Compliance List', '/knowledge/compliance-task-list', 24, null);
INSERT INTO tbl_forms VALUES(25, 3, 3, 'Statutory Notifications List', '/knowledge/statutory-notifications-list', 25, null);

# common
INSERT INTO tbl_forms VALUES(26, 4, 3, 'Audit Trail', '/knowledge/audit-trail', 26, null);

-- mirror.client

-- DELETE FROM tbl_form_type;
INSERT INTO tbl_form_type VALUES(1, "Home");
INSERT INTO tbl_form_type VALUES(2, "Master");
INSERT INTO tbl_form_type VALUES(3, "Transaction");
INSERT INTO tbl_form_type VALUES(4, "Report");
INSERT INTO tbl_form_type VALUES(5, "Settings");

-- fields(form_id, form_type_id, form_name, form_url, form_order, parent_menu, is_admin)
INSERT INTO tbl_forms VALUES(1, 1, 'Dashboard', '/home', 1, null, 1);
INSERT INTO tbl_forms VALUES(2, 2, 'Service Provider', '/service-provider', 2, null, 1);
INSERT INTO tbl_forms VALUES(3, 2, 'User Privilege', '/client-user-privilege', 3, null, 1);
INSERT INTO tbl_forms VALUES(4, 2, 'User', '/client-user-master', 4, null, 1);
INSERT INTO tbl_forms VALUES(5, 2, 'Unit Closure', '/unit-closure', 5, null, 1);
INSERT INTO tbl_forms VALUES(6, 3, 'Statutory Settings', '/statutory-settings', 6, null, 1);
INSERT INTO tbl_forms VALUES(7, 3, 'Assign Compliance', '/assign-compliance', 7, null, 1);
INSERT INTO tbl_forms VALUES(8, 3, 'Reassign Compliance', '/reassign-compliance', 8, null, 1);
INSERT INTO tbl_forms VALUES(9, 3, 'Compliance Approval', '/compliance-approval', 9, null, 1);
INSERT INTO tbl_forms VALUES(10, 3, 'Completed Tasks - Current Year', '/completed-tasks-current-year', 10, null, 1);
INSERT INTO tbl_forms VALUES(11, 3, 'Compliance Task Details', '/compliance-task-details',11, null, 1);
INSERT INTO tbl_forms VALUES(12, 3, 'On Occurrence Compliances', '/on-occurrence-compliances', 12, null, 1);
INSERT INTO tbl_forms VALUES(13, 4, 'Compliance Details', '/compliance-details', 13, null, 1);
INSERT INTO tbl_forms VALUES(14, 4, 'Risk Report', '/risk-report', 14, null, 1);
INSERT INTO tbl_forms VALUES(15, 4, 'Service Provider wise Compliance', '/service-provider-wise-compliance', 15, "Compliance List", 1);
INSERT INTO tbl_forms VALUES(16, 4, 'Assignee wise Compliance', '/assignee-wise-compliance', 16, "Compliance List", 1);
INSERT INTO tbl_forms VALUES(17, 4, 'Unit wise Compliance', '/unit-wise-compliance', 17, "Compliance List", 1);
INSERT INTO tbl_forms VALUES(18, 4, 'Compliance Task Applicability Status', '/compliance-task-applicability-status', 18, null, 1);
INSERT INTO tbl_forms VALUES(19, 4, 'Unit Details', '/unit-details', 19, null, 1);
INSERT INTO tbl_forms VALUES(20, 4, 'Compliance Activity Report', '/compliance-activity-report', 20, null, 1);
INSERT INTO tbl_forms VALUES(21, 4, 'Reassigned History', '/reassigned-history', 21, null, 1);
INSERT INTO tbl_forms VALUES(22, 4, 'Statutory Notifications List', '/statutory-notifications-list', 22, null, 1);
INSERT INTO tbl_forms VALUES(23, 4, 'Login Trace', '/login-trace', 23, null, 1);
INSERT INTO tbl_forms VALUES(24, 4, 'Audit Trail', '/audit-trail', 24, null, 1);
INSERT INTO tbl_forms VALUES(25, 5, 'Settings', '/settings',  25, null, 1);
INSERT INTO tbl_forms VALUES(26, 5, 'View Profile', '/view-profile',  26, null, 1);
-- tbl_admin
-- username, password -- 123456
INSERT INTO tbl_admin  VALUES("admin", "e10adc3949ba59abbe56e057f20f883e");

-- DELETE FROM tbl_users
-- field user_id, user_group_id ,email_id ,password, employee_name,
-- employee_code, contact_no, address, designation, is_active, created_by, created_on, updated_by, updated_on


-- tbl_session_types
-- DELETE FROM tbl_session_types
-- values = session_type_id, snession_type
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

-- tbl_user_groups
-- INSERT INTO tbl_user_groups(user_group_id, form_category_id, user_group_name, form_ids, is_active) VALUES(1, 2, "knowledge", "5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16", 1);

-- --tbl_users
-- INSERT INTO tbl_users(user_id, user_group_id, email_id, password, employee_name, contact_no, designation, address, employee_code )
-- VALUES (1, 1, 'usha@mindssoft.com', 'e10adc3949ba59abbe56e057f20f883e', 'Test-user', "9876543210", "Manager", "KK Nagar", "TEST001")

-- tbl_user_sessions
-- INSERT INTO tbl_user_sessions(session_token, user_id, session_type_id) VALUES ("12c94b934d5f4b5ebebd4471d8b29cb8", 0, 1);
-- INSERT INTO tbl_user_sessions(session_token, user_id, session_type_id) VALUES ("b4c59894336c4ee3b598f5e4bd2b276b", 1, 1);

-- tbl_notification_types
INSERT INTO tbl_notification_types VALUES(1, "Notification");
INSERT INTO tbl_notification_types VALUES(2, "Reminder");
INSERT INTO tbl_notification_types VALUES(3, "Escalation");

-- Get Statutory Notifications Log



