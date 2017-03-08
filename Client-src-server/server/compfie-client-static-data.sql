USE `compfie_knowledge_new`;

-- User Category
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
INSERT INTO tbl_forms VALUES(2, 1, 'User Privileges', "/client-user-privilege", 1, null);
INSERT INTO tbl_forms VALUES(3, 1, 'User Management', "/client-user-management", 1, null);
INSERT INTO tbl_forms VALUES(4, 1, 'Unit Closure', "/unit-closure", 1, null);

INSERT INTO tbl_forms VALUES(5, 2, 'Statutory Settings', "/statutory-settings", 1, null);
INSERT INTO tbl_forms VALUES(6, 2, 'Review Settings', "/review-settings", 1, null);
INSERT INTO tbl_forms VALUES(7, 2, 'Assign Compliance', "/assign-compliance", 1, null);
INSERT INTO tbl_forms VALUES(8, 2, 'Reassign Compliance', "/reassign-compliance", 1, null);
INSERT INTO tbl_forms VALUES(9, 2, 'Compliance Approval', "/compliance-approval", 1, null);
INSERT INTO tbl_forms VALUES(10, 2, 'Completed Task - Current Year', "/completed-tasks-current-year", 1, null);
INSERT INTO tbl_forms VALUES(11, 2, 'On Occurrence Compliances', "/on-occurrence-compliances", 1, null);
INSERT INTO tbl_forms VALUES(35, 2, 'Compliance Task Details', "/compliance-details", 1, null);

INSERT INTO tbl_forms VALUES(12, 3, 'Legal Entity Wise Report', "/legal-entity-wise-report", 1, null);
INSERT INTO tbl_forms VALUES(13, 3, 'Domain Wise Report', "/domain-wise-report", 1, null);
INSERT INTO tbl_forms VALUES(14, 3, 'Unit Wise Compliance', "/unit-wise-compliance", 1, null);
INSERT INTO tbl_forms VALUES(15, 3, 'Service Provider Wise Compliance', "/service-provider-wise-compliance", 1, null);
INSERT INTO tbl_forms VALUES(16, 3, 'User Wise Compliance', "/user-wise-compliance", 1, null);
INSERT INTO tbl_forms VALUES(17, 3, 'Status Report Consolidated', "/status-report-consolidated", 1, null);
INSERT INTO tbl_forms VALUES(18, 3, 'Domain Score Card', "/domain-score-card", 1, "Score Card");
INSERT INTO tbl_forms VALUES(19, 3, 'Legal Entity Wise Score Card', "/legal-entity-wise-score-card", 1, "Score Card");
INSERT INTO tbl_forms VALUES(20, 3, 'Work Flow Score Card', "/work-flow-score-card", 1, "Score Card");
INSERT INTO tbl_forms VALUES(21, 3, 'Statutory Settings Unit Wise Report', "/statutory-settings-unit-wise-report", 1, null);
INSERT INTO tbl_forms VALUES(22, 3, 'Reassigned History Report', "/reassigned-history-report", 1, null);
INSERT INTO tbl_forms VALUES(23, 3, 'Risk Report', "/risk-report", 1, null);
INSERT INTO tbl_forms VALUES(24, 3, 'Unit List', "/unit-list", 1, null);
INSERT INTO tbl_forms VALUES(25, 3, 'Statutory Notification List', "/statutory-notification-list", 1, null);
INSERT INTO tbl_forms VALUES(26, 3, 'Service Provider Details', "/service-provider-details", 1, null);
INSERT INTO tbl_forms VALUES(27, 3, 'Audit Trail', "/audit-trail", 1, null);
INSERT INTO tbl_forms VALUES(28, 3, 'Login Trace', "/login-trace", 1, null);

INSERT INTO tbl_forms VALUES(29, 4, 'view-profile', "/View Profile", 1, null);
INSERT INTO tbl_forms VALUES(30, 4, 'Client View Profile', "/client-view-profile", 1, null);
INSERT INTO tbl_forms VALUES(31, 4, 'Change Password', "/change-password", 1, null);
INSERT INTO tbl_forms VALUES(32, 4, 'Client Settings', "/client-settings", 1, null);
INSERT INTO tbl_forms VALUES(33, 4, 'themes', "/themes", 1, null);

INSERT INTO tbl_forms VALUES(34, 5, 'Dashboard', "/dashboard", 1, null);

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
.
.
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
