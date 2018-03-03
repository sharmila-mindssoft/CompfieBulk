USE `compfie_knowledge_new`;

-- DELETE FROM tbl_form_type;
INSERT INTO tbl_form_type VALUES(1, "Master");
INSERT INTO tbl_form_type VALUES(2, "Transaction");
INSERT INTO tbl_form_type VALUES(3, "Report");
INSERT INTO tbl_form_type VALUES(4, "My Accounts");

-- DELETE FROM tbl_forms
-- fields(form_id, form_type_id, form_name, form_url, form_order, parent_menu)

-- mirror_knowledge
-- masters
INSERT INTO tbl_forms VALUES(1, 1, 'Country', '/knowledge/country-master', 1,  null);
INSERT INTO tbl_forms VALUES(2, 1, 'Domain', '/knowledge/domain-master', 2, null);
INSERT INTO tbl_forms VALUES(3, 1, 'User Privileges', '/knowledge/user-privileges', 3, null);
INSERT INTO tbl_forms VALUES(4, 1, 'Geography Level Master', '/knowledge/geography-level-master', 4, 'Geography');
INSERT INTO tbl_forms VALUES(5, 1, 'Geography Master', '/knowledge/geography-master', 5, 'Geography');
INSERT INTO tbl_forms VALUES(6, 1, 'Organization', '/knowledge/organization', 6, null);
INSERT INTO tbl_forms VALUES(7, 1, 'Statutory Nature Master', '/knowledge/statutory-nature', 7, 'Statutory');
INSERT INTO tbl_forms VALUES(8, 1, 'Statutory Level Master', '/knowledge/statutory-level-master', 8, 'Statutory');
INSERT INTO tbl_forms VALUES(9, 1, 'Validity Date Settings', '/knowledge/validity-date-settings', 9, null);

-- Transaction
INSERT INTO tbl_forms VALUES(10, 2, 'User Management', '/knowledge/user-management', 10, null);
INSERT INTO tbl_forms VALUES(11, 2, 'User Mapping', '/knowledge/user-mapping', 11, null);
INSERT INTO tbl_forms VALUES(12, 2, 'Reassign User Account ', '/knowledge/reassign-user-account', 12, null);
INSERT INTO tbl_forms VALUES(13, 2, 'Approve Client Group', '/knowledge/client-master-approval', 13, null);
INSERT INTO tbl_forms VALUES(14, 2, 'Group Admin Registraion Email', '/knowledge/group-admin-registration-email', 14, null);
INSERT INTO tbl_forms VALUES(15, 2, 'Statutory Mapping', '/knowledge/statutory-mapping', 15, null);
INSERT INTO tbl_forms VALUES(16, 2, 'Approve Statutory Mapping', '/knowledge/approve-statutory-mapping', 16, null);

INSERT INTO tbl_forms VALUES(17, 2, 'Client Group', '/knowledge/client-master', 17, null);

INSERT INTO tbl_forms VALUES(18, 2, 'Assign Legal Entity', '/knowledge/assign-legal-entity', 18, null);
INSERT INTO tbl_forms VALUES(19, 2, 'Assign Client Unit', '/knowledge/assign-client-unit', 19, null);

INSERT INTO tbl_forms VALUES(20, 2, 'Client Unit Approval', '/knowledge/client-unit-approval', 20, null);
INSERT INTO tbl_forms VALUES(21, 2, 'Legal Entity Closure', '/knowledge/legal-entity-closure', 21, null);
INSERT INTO tbl_forms VALUES(22, 2, 'Client Unit', '/knowledge/client-unit', 22, null);

INSERT INTO tbl_forms VALUES(23, 2, 'Assign Statutory', '/knowledge/assign-statutory', 23, null);
INSERT INTO tbl_forms VALUES(24, 2, 'Approve Assigned Statutory', '/knowledge/approve-assigned-statutory', 24, null);
INSERT INTO tbl_forms VALUES(25, 2, 'Configure Database Server', '/knowledge/configure-database-server', 25, null);
INSERT INTO tbl_forms VALUES(26, 2, 'Configure Application Server', '/knowledge/application-server', 26, null);
INSERT INTO tbl_forms VALUES(27, 2, 'Configure File Server', '/knowledge/configure-file-server', 27, null);
INSERT INTO tbl_forms VALUES(28, 2, 'Allocate Server', '/knowledge/allocate-database-environment', 28, null);
INSERT INTO tbl_forms VALUES(29, 2, 'Auto Deletion', '/knowledge/auto-deletion', 29, null);
INSERT INTO tbl_forms VALUES(50, 2, 'Form Authorization - IP Settings', '/knowledge/ip-settings', 50, null);

-- Reports
INSERT INTO tbl_forms VALUES(30, 3, 'User Mapping Report', '/knowledge/user-mapping-report', 30, null);
INSERT INTO tbl_forms VALUES(31, 3, 'Country Report', '/knowledge/country-report', 31, 'Master');
INSERT INTO tbl_forms VALUES(32, 3, 'Domain Report', '/knowledge/domain-report', 32, 'Master');
INSERT INTO tbl_forms VALUES(33, 3, 'Geography Report', '/knowledge/geography-report', 33, 'Master');
INSERT INTO tbl_forms VALUES(34, 3, 'Organization Report', '/knowledge/organization-report', 34, 'Master');
INSERT INTO tbl_forms VALUES(35, 3, 'Statutory Nature Report', '/knowledge/statutory-nature-report', 35, 'Master');
INSERT INTO tbl_forms VALUES(36, 3, 'Statutory Mapping Report', '/knowledge/statutory-mapping-report', 36, null);
INSERT INTO tbl_forms VALUES(37, 3, 'Statutory Notification List', '/knowledge/statutory-notifications-list', 37, null);
INSERT INTO tbl_forms VALUES(38, 3, 'Client Agreement Master Report', '/knowledge/client-agreement-report', 38, null);
INSERT INTO tbl_forms VALUES(39, 3, 'Domain Wise Agreement Master Report', '/knowledge/domain-agreement-master-report', 39, null);
INSERT INTO tbl_forms VALUES(40, 3, 'Client Unit Details', '/knowledge/client-unit-details', 40, null);

INSERT INTO tbl_forms VALUES(42, 3, 'Statutory Settings Report', '/knowledge/statutory-setting-report', 42, null);
INSERT INTO tbl_forms VALUES(43, 3, 'Audit Trail Login Trace', '/knowledge/audit-trail-login-trace', 43, null);
INSERT INTO tbl_forms VALUES(48, 3, 'Group Admin Registration Email Report', '/knowledge/group-admin-registration-email-report', 48, NULL);
INSERT INTO tbl_forms VALUES(49, 3, 'Reassign User Report', '/knowledge/reassign-user-report', 49, NULL);
INSERT INTO tbl_forms VALUES(51, 3, 'Form Authorization - IP Settings Report', '/knowledge/ip-settings-report', 51, null);
INSERT INTO tbl_forms VALUES(52, 3, 'Allocate Server Report', '/knowledge/allocate-database-environment-report', 52, NULL);
INSERT INTO tbl_forms VALUES(53, 3, 'Client Audit Trail', '/knowledge/client-audit-trail', 53, NULL);
INSERT INTO tbl_forms VALUES(54, 3, 'Client Login Trace', '/knowledge/client-login-trace', 54, NULL);


-- My Account
INSERT INTO tbl_forms VALUES(44, 4, 'View Profile', '/knowledge/profile', 44, null);
INSERT INTO tbl_forms VALUES(45, 4, 'Change Password', '/knowledge/change-password', 45, null);
INSERT INTO tbl_forms VALUES(46, 4, 'Messages', '/knowledge/messages', 46, null);
INSERT INTO tbl_forms VALUES(47, 4, 'Statutory Notification', '/knowledge/statutory-notifications', 47, null);

-- bulk upload forms
INSERT INTO tbl_forms VALUES(55, 2, 'Statutory Mapping - Bulk Upload', '/knowledge/statutory-mapping-bu', 55, NULL);
INSERT INTO tbl_forms VALUES(56, 2, 'Rejected Statutory Mapping - Bulk Upload', '/knowledge/reject-statutory-mapping-bu', 56, NULL);
INSERT INTO tbl_forms VALUES(57, 2, 'Approve Statutory Mapping - Bulk Upload', '/knowledge/approve-statutory-mapping-bu', 57, NULL);
INSERT INTO tbl_forms VALUES(58, 2, 'Client Unit - Bulk Upload', '/knowledge/client-unit-bu', 58, NULL);
INSERT INTO tbl_forms VALUES(59, 2, 'Rejected Client Unit - Bulk Upload', '/knowledge/rejected-client-unit-bu', 59, NULL);
INSERT INTO tbl_forms VALUES(60, 2, 'Approve Client Unit - Bulk Upload', '/knowledge/approve-client-unit-bu', 60, NULL);
INSERT INTO tbl_forms VALUES(61, 2, 'Assign Statutory - Bulk Upload', '/knowledge/assign-statutory-bu', 61, NULL);
INSERT INTO tbl_forms VALUES(62, 2, 'Rejected Assign Statutory - Bulk Upload', '/knowledge/rejected-assign-statutory-bu', 62, NULL);
INSERT INTO tbl_forms VALUES(63, 2, 'Approve Assign Statutory - Bulk Upload', '/knowledge/approve-assign-statutory-bu', 63, NULL);

INSERT INTO tbl_forms VALUES(64, 3, 'Approved/Rejected Statutory Mapping Summary', '/knowledge/approved-rejected-statutory-mapping-summary', 64, NULL);
INSERT INTO tbl_forms VALUES(65, 3, 'Statutory Mapping Upload Summary', '/knowledge/statutory-mapping-upload-summary', 65, NULL);
INSERT INTO tbl_forms VALUES(66, 3, 'Client Unit Upload Summary', '/knowledge/client-unit-upload-summary', 66, NULL);
INSERT INTO tbl_forms VALUES(67, 3, 'Approved/Rejected Client Unit Summary', '/knowledge/approved-rejected-client-unit-summary', 67, NULL);
INSERT INTO tbl_forms VALUES(68, 3, 'Assign Statutory Upload Summary', '/knowledge/assign-statutory-upload-summary', 68, NULL);
INSERT INTO tbl_forms VALUES(69, 3, 'Approved/Rejected Assign Statutory Upload Summary', '/knowledge/approved-rejected-assign-statutory-summary', 69, NULL);
INSERT INTO tbl_forms VALUES(70, 3,	'Statutory Mapping - Bulk Upload Report',	'/knowledge/statutory-mapping-bulkupload-report', 70, NULL);
INSERT INTO tbl_forms VALUES(71, 3,	'Client Unit - Bulk Upload Report',	'/knowledge/client-unit-bulk-report-bu', 71, NULL);
INSERT INTO tbl_forms VALUES(72, 3, 'Assigned Statutory - Bulk Upload Report', '/knowledge/assigned-statutory-bulkupload-report', 72, NULL);





-- DELETE FROM tbl_form_category;
INSERT INTO tbl_user_category VALUES(1, "Compfie Admin");
INSERT INTO tbl_user_category VALUES(2, "Console Admin");
INSERT INTO tbl_user_category VALUES(3, "Knowledge Manager");
INSERT INTO tbl_user_category VALUES(4, "Knowledge Executive");
INSERT INTO tbl_user_category VALUES(5, "Techno Manager");
INSERT INTO tbl_user_category VALUES(6, "Techno Executive");
INSERT INTO tbl_user_category VALUES(7, "Domain Manager");
INSERT INTO tbl_user_category VALUES(8, "Domain Executive");

-- form_id, category_id_1, category_id_2, category_id_3, category_id_4, category_id_5, category_id_6, category_id_7, category_id_8
-- Masters
INSERT INTO tbl_form_category VALUES(1, 1, 0, 0, 0, 0, 0, 0, 0);
INSERT INTO tbl_form_category VALUES(2, 1, 0, 0, 0, 0, 0, 0, 0);
INSERT INTO tbl_form_category VALUES(3, 1, 0, 0, 0, 0, 0, 0, 0);
INSERT INTO tbl_form_category VALUES(4, 1, 0, 0, 0, 0, 0, 0, 0);
INSERT INTO tbl_form_category VALUES(5, 1, 0, 0, 0, 0, 0, 0, 0);
INSERT INTO tbl_form_category VALUES(6, 1, 0, 0, 0, 0, 0, 0, 0);
INSERT INTO tbl_form_category VALUES(7, 1, 0, 0, 0, 0, 0, 0, 0);
INSERT INTO tbl_form_category VALUES(8, 1, 0, 0, 0, 0, 0, 0, 0);
INSERT INTO tbl_form_category VALUES(9, 1, 0, 0, 0, 0, 0, 0, 0);

-- Transactions
INSERT INTO tbl_form_category VALUES(10, 1, 0, 0, 0, 0, 0, 0, 0);
INSERT INTO tbl_form_category VALUES(11, 1, 0, 0, 0, 0, 0, 0, 0);
INSERT INTO tbl_form_category VALUES(12, 1, 0, 0, 0, 0, 0, 0, 0);
INSERT INTO tbl_form_category VALUES(13, 1, 0, 0, 0, 0, 0, 0, 0);
INSERT INTO tbl_form_category VALUES(14, 1, 0, 0, 0, 0, 0, 0, 0);
INSERT INTO tbl_form_category VALUES(15, 0, 0, 0, 1, 0, 0, 0, 0);
INSERT INTO tbl_form_category VALUES(16, 0, 0, 1, 0, 0, 0, 0, 0);
INSERT INTO tbl_form_category VALUES(17, 0, 0, 0, 0, 1, 0, 0, 0);
INSERT INTO tbl_form_category VALUES(18, 0, 0, 0, 0, 1, 0, 0, 0);
INSERT INTO tbl_form_category VALUES(19, 0, 0, 0, 0, 1, 0, 1, 0);
INSERT INTO tbl_form_category VALUES(20, 0, 0, 0, 0, 1, 0, 0, 0);
INSERT INTO tbl_form_category VALUES(21, 0, 0, 0, 0, 1, 0, 0, 0);
INSERT INTO tbl_form_category VALUES(22, 0, 0, 0, 0, 0, 1, 0, 0);
INSERT INTO tbl_form_category VALUES(23, 0, 0, 0, 0, 0, 0, 0, 1);
INSERT INTO tbl_form_category VALUES(24, 0, 0, 0, 0, 0, 0, 1, 0);
INSERT INTO tbl_form_category VALUES(25, 0, 1, 0, 0, 0, 0, 0, 0);
INSERT INTO tbl_form_category VALUES(26, 0, 1, 0, 0, 0, 0, 0, 0);
INSERT INTO tbl_form_category VALUES(27, 0, 1, 0, 0, 0, 0, 0, 0);
INSERT INTO tbl_form_category VALUES(28, 0, 1, 0, 0, 0, 0, 0, 0);
INSERT INTO tbl_form_category VALUES(29, 0, 1, 0, 0, 0, 0, 0, 0);
INSERT INTO tbl_form_category VALUES(50, 0, 1, 0, 0, 0, 0, 0, 0);
-- Reports
INSERT INTO tbl_form_category VALUES(30, 1, 0, 0, 0, 1, 0, 1, 0);
INSERT INTO tbl_form_category VALUES(31, 1, 0, 0, 0, 0, 0, 0, 0);
INSERT INTO tbl_form_category VALUES(32, 1, 0, 0, 0, 0, 0, 0, 0);
INSERT INTO tbl_form_category VALUES(33, 1, 0, 0, 0, 0, 0, 0, 0);
INSERT INTO tbl_form_category VALUES(34, 1, 0, 0, 0, 0, 0, 0, 0);
INSERT INTO tbl_form_category VALUES(35, 1, 0, 0, 0, 0, 0, 0, 0);

INSERT INTO tbl_form_category VALUES(36, 1, 0, 1, 1, 1, 1, 1, 1);
INSERT INTO tbl_form_category VALUES(37, 1, 0, 1, 1, 1, 1, 1, 1);
INSERT INTO tbl_form_category VALUES(38, 1, 0, 0, 0, 1, 0, 1, 0);
INSERT INTO tbl_form_category VALUES(39, 1, 0, 0, 0, 1, 0, 1, 1);
INSERT INTO tbl_form_category VALUES(40, 1, 0, 0, 0, 1, 1, 1, 1);
INSERT INTO tbl_form_category VALUES(41, 1, 0, 0, 0, 1, 0, 1, 1);
INSERT INTO tbl_form_category VALUES(42, 1, 0, 0, 0, 1, 0, 1, 1);
INSERT INTO tbl_form_category VALUES(43, 1, 0, 0, 0, 0, 0, 0, 0);
INSERT INTO tbl_form_category VALUES(48, 1, 0, 0, 0, 0, 0, 0, 0);
INSERT INTO tbl_form_category VALUES(49, 1, 0, 0, 0, 0, 0, 0, 0);
INSERT INTO tbl_form_category VALUES(51, 0, 1, 0, 0, 0, 0, 0, 0);
INSERT INTO tbl_form_category VALUES(52, 0, 1, 0, 0, 0, 0, 0, 0);
INSERT INTO tbl_form_category VALUES(53, 1, 0, 0, 0, 0, 0, 0, 0);
INSERT INTO tbl_form_category VALUES(54, 1, 0, 0, 0, 0, 0, 0, 0);

-- My Accounts
INSERT INTO tbl_form_category VALUES(44, 0, 0, 1, 1, 1, 1, 1, 1);
INSERT INTO tbl_form_category VALUES(45, 1, 1, 1, 1, 1, 1, 1, 1);
INSERT INTO tbl_form_category VALUES(46, 1, 1, 1, 1, 1, 1, 1, 1);
INSERT INTO tbl_form_category VALUES(47, 1, 0, 1, 1, 1, 1, 1, 1);

-- bulk-upload forms
-- knoledge executive
INSERT INTO tbl_form_category VALUES(55, 0, 0, 0, 1, 0, 0, 0, 0);
INSERT INTO tbl_form_category VALUES(56, 0, 0, 0, 1, 0, 0, 0, 0);
-- knowledge manager
INSERT INTO tbl_form_category VALUES(57, 0, 0, 1, 0, 0, 0, 0, 0);

-- techno executive
INSERT INTO tbl_form_category VALUES(58, 0, 0, 0, 0, 0, 1, 0, 0);
INSERT INTO tbl_form_category VALUES(59, 0, 0, 0, 0, 0, 1, 0, 0);

-- techno manager
INSERT INTO tbl_form_category VALUES(60, 0, 0, 0, 0, 1, 0, 0, 0);

-- domain executive
INSERT INTO tbl_form_category VALUES(61, 0, 0, 0, 0, 0, 0, 0, 1);
INSERT INTO tbl_form_category VALUES(62, 0, 0, 0, 0, 0, 0, 0, 1);

-- manager
INSERT INTO tbl_form_category VALUES(63, 0, 0, 0, 0, 0, 0, 1, 0);

-- reports
INSERT INTO tbl_form_category VALUES(64, 0, 0, 1, 1, 0, 0, 0, 0);
INSERT INTO tbl_form_category VALUES(65, 0, 0, 0, 1, 0, 0, 0, 0);
INSERT INTO tbl_form_category VALUES(66, 0, 0, 0, 0, 0, 1, 0, 0);
INSERT INTO tbl_form_category VALUES(67, 0, 0, 0, 0, 1, 1, 0, 0);
INSERT INTO tbl_form_category VALUES(68, 0, 0, 0, 0, 0, 0, 0, 1);
INSERT INTO tbl_form_category VALUES(69, 0, 0, 0, 0, 0, 0, 1, 1);
INSERT INTO tbl_form_category VALUES(70, 0,	0, 1, 0, 0,	0, 0, 0);
INSERT INTO tbl_form_category VALUES(71, 0,	0, 0, 0, 1,	0, 0, 0);

-- tbl_user_login_details
-- user_id, user_category_id, username, password, is_active --- p@$$word@123
INSERT INTO tbl_user_login_details (user_id, user_category_id, email_id, username, password, is_active) VALUES(1, 1, "compfieadmin@compfie.com", "compfieadmin", "7ecfd14ba1b0d6800688a0a317a5a331", 1);
INSERT INTO tbl_user_login_details (user_id, user_category_id, email_id, username, password, is_active) VALUES(2, 2, "consoleadmin@compfie.com", "consoleadmin", "7ecfd14ba1b0d6800688a0a317a5a331", 1);


-- tbl_session_types
INSERT INTO tbl_session_types VALUES(1, "web");
INSERT INTO tbl_session_types VALUES(2, "android");
INSERT INTO tbl_session_types VALUES(3, "ios");

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

-- tbl_verification_type
INSERT INTO tbl_verification_type VALUES(1, "Registraion");
INSERT INTO tbl_verification_type VALUES(2, "Reset Password");
INSERT INTO tbl_verification_type VALUES(3, "Data Download");

-- tbl_client_forms

INSERT INTO tbl_client_forms(form_id, form_type_id, form_name, form_url, form_order, parent_menu) VALUES(1, 1, 'Service Provider', "/service-provider", 1, null);
INSERT INTO tbl_client_forms(form_id, form_type_id, form_name, form_url, form_order, parent_menu) VALUES(2, 1, 'User Privileges', "/client-user-privilege", 2, null);
INSERT INTO tbl_client_forms(form_id, form_type_id, form_name, form_url, form_order, parent_menu) VALUES(3, 1, 'User Management', "/client-user-management", 3, null);
INSERT INTO tbl_client_forms(form_id, form_type_id, form_name, form_url, form_order, parent_menu) VALUES(4, 1, 'Unit Closure', "/unit-closure", 4, null);
INSERT INTO tbl_client_forms(form_id, form_type_id, form_name, form_url, form_order, parent_menu) VALUES(5, 2, 'Statutory Settings', "/statutory-settings", 5, null);
INSERT INTO tbl_client_forms(form_id, form_type_id, form_name, form_url, form_order, parent_menu) VALUES(6, 2, 'Review Settings', "/review-settings", 6, null);
INSERT INTO tbl_client_forms(form_id, form_type_id, form_name, form_url, form_order, parent_menu) VALUES(7, 2, 'Assign Compliance', "/assign-compliance", 7, null);
INSERT INTO tbl_client_forms(form_id, form_type_id, form_name, form_url, form_order, parent_menu) VALUES(8, 2, 'Reassign Compliance', "/reassign-compliance", 8, null);
INSERT INTO tbl_client_forms(form_id, form_type_id, form_name, form_url, form_order, parent_menu) VALUES(9, 2, 'Compliance Approval', "/compliance-approval", 9, null);
INSERT INTO tbl_client_forms(form_id, form_type_id, form_name, form_url, form_order, parent_menu) VALUES(10, 2, 'Completed Task - Current Year', "/completed-tasks-current-year", 10, null);
INSERT INTO tbl_client_forms(form_id, form_type_id, form_name, form_url, form_order, parent_menu) VALUES(11, 2, 'On Occurrence Compliances', "/on-occurrence-compliances", 11, null);
INSERT INTO tbl_client_forms(form_id, form_type_id, form_name, form_url, form_order, parent_menu) VALUES(12, 3, 'Legal Entity Wise Report', "/legal-entity-wise-report", 12, null);
INSERT INTO tbl_client_forms(form_id, form_type_id, form_name, form_url, form_order, parent_menu) VALUES(13, 3, 'Domain Wise Report', "/domain-wise-report", 13, null);
INSERT INTO tbl_client_forms(form_id, form_type_id, form_name, form_url, form_order, parent_menu) VALUES(14, 3, 'Unit Wise Compliance', "/unit-wise-compliance", 14, null);
INSERT INTO tbl_client_forms(form_id, form_type_id, form_name, form_url, form_order, parent_menu) VALUES(15, 3, 'Service Provider Wise Compliance', "/service-provider-wise-compliance", 15, null);
INSERT INTO tbl_client_forms(form_id, form_type_id, form_name, form_url, form_order, parent_menu) VALUES(16, 3, 'User Wise Compliance', "/user-wise-compliance", 16, null);
INSERT INTO tbl_client_forms(form_id, form_type_id, form_name, form_url, form_order, parent_menu) VALUES(17, 3, 'Status Report Consolidated', "/status-report-consolidated", 17, null);
INSERT INTO tbl_client_forms(form_id, form_type_id, form_name, form_url, form_order, parent_menu) VALUES(18, 3, 'Domain Score Card', "/domain-score-card", 18, null);
INSERT INTO tbl_client_forms(form_id, form_type_id, form_name, form_url, form_order, parent_menu) VALUES(19, 3, 'Legal Entity Wise Score Card', "/legal-entity-wise-score-card", 19, null);
INSERT INTO tbl_client_forms(form_id, form_type_id, form_name, form_url, form_order, parent_menu) VALUES(20, 3, 'Work Flow Score Card', "/work-flow-score-card", 20, null);
INSERT INTO tbl_client_forms(form_id, form_type_id, form_name, form_url, form_order, parent_menu) VALUES(21, 3, 'Statutory Settings Unit Wise Report', "/statutory-settings-unit-wise-report", 21, null);
INSERT INTO tbl_client_forms(form_id, form_type_id, form_name, form_url, form_order, parent_menu) VALUES(22, 3, 'Reassigned History Report', "/reassigned-history-report", 22, null);
INSERT INTO tbl_client_forms(form_id, form_type_id, form_name, form_url, form_order, parent_menu) VALUES(23, 3, 'Risk Report', "/risk-report", 23, null);
INSERT INTO tbl_client_forms(form_id, form_type_id, form_name, form_url, form_order, parent_menu) VALUES(24, 3, 'Unit List', "/unit-list", 24, null);
INSERT INTO tbl_client_forms(form_id, form_type_id, form_name, form_url, form_order, parent_menu) VALUES(25, 3, 'Statutory Notification List', "/statutory-notification-list", 25, null);
INSERT INTO tbl_client_forms(form_id, form_type_id, form_name, form_url, form_order, parent_menu) VALUES(26, 3, 'Service Provider Details', "/service-provider-details", 26, null);
INSERT INTO tbl_client_forms(form_id, form_type_id, form_name, form_url, form_order, parent_menu) VALUES(27, 3, 'Audit Trail', "/audit-trail", 27, null);
INSERT INTO tbl_client_forms(form_id, form_type_id, form_name, form_url, form_order, parent_menu) VALUES(28, 3, 'Login Trace', "/login-trace", 28, null);
INSERT INTO tbl_client_forms(form_id, form_type_id, form_name, form_url, form_order, parent_menu) VALUES(29, 4, 'View Profile', "/view-profile", 29, null);
INSERT INTO tbl_client_forms(form_id, form_type_id, form_name, form_url, form_order, parent_menu) VALUES(31, 4, 'Change Password', "/change-password", 31, null);
INSERT INTO tbl_client_forms(form_id, form_type_id, form_name, form_url, form_order, parent_menu) VALUES(32, 4, 'Client Settings', "/client-settings", 32, null);
INSERT INTO tbl_client_forms(form_id, form_type_id, form_name, form_url, form_order, parent_menu) VALUES(33, 4, 'Themes', "/themes", 33, null);
INSERT INTO tbl_client_forms(form_id, form_type_id, form_name, form_url, form_order, parent_menu) VALUES(34, 5, 'Dashboard', "/dashboard", 34, null);
INSERT INTO tbl_client_forms(form_id, form_type_id, form_name, form_url, form_order, parent_menu) VALUES(35, 2, 'Compliance Task Details', "/compliance-task-details", 35, null);
INSERT INTO tbl_client_forms(form_id, form_type_id, form_name, form_url, form_order, parent_menu) VALUES(36, 4, 'Reminders', "/reminders", 36, null);
INSERT INTO tbl_client_forms(form_id, form_type_id, form_name, form_url, form_order, parent_menu) VALUES(37, 4, 'Statutory Notifications', "/statutory-notifications", 37, null);
INSERT INTO tbl_client_forms(form_id, form_type_id, form_name, form_url, form_order, parent_menu) VALUES(38, 4, 'Escalations', "/escalations", 38, null);
INSERT INTO tbl_client_forms(form_id, form_type_id, form_name, form_url, form_order, parent_menu) VALUES(39, 4, 'Messages', "/messages", 39, null);

INSERT INTO tbl_client_user_category VALUES(1, "Group Admin");
INSERT INTO tbl_client_user_category VALUES(2, "View Only");
INSERT INTO tbl_client_user_category VALUES(3, "Legal Entity Admin");
INSERT INTO tbl_client_user_category VALUES(4, "Domain Admin");
INSERT INTO tbl_client_user_category VALUES(5, "Client Executive");
INSERT INTO tbl_client_user_category VALUES(6, "Service Provider");
