-- --------------------------------------------------------------------------------
-- To get the list of groups with countries and number of legal entities
-- --------------------------------------------------------------------------------
DELIMITER $$

CREATE PROCEDURE `sp_client_groups_list`()
BEGIN
select group_id, group_name,
(
	select group_concat(country_name) from tbl_countries 
	where country_id in (
		select country_id from tbl_client_countries
		where client_id=group_id
	)
),
(
	select count(legal_entity_id) from tbl_legal_entities tle
	WHERE tle.group_id=tcg.group_id
)
FROM tbl_client_groups tcg;
END

-- --------------------------------------------------------------------------------
-- To Fetch Active Countries List
-- --------------------------------------------------------------------------------
DELIMITER $$

CREATE PROCEDURE `sp_countries_active_list`()
BEGIN
	SELECT country_id, country_name, is_active
	FROM tbl_countries 
	WHERE is_active=1;
END

-- --------------------------------------------------------------------------------
-- To Fetch Active Domains List
-- --------------------------------------------------------------------------------
DELIMITER $$

CREATE PROCEDURE `sp_domains_active_list`()
BEGIN
	SELECT domain_id, domain_name, is_active
	FROM tbl_domains WHERE is_active=1;
END

-- --------------------------------------------------------------------------------
-- To Fetch active industry list
-- --------------------------------------------------------------------------------
DELIMITER $$

CREATE PROCEDURE `sp_industries_active_list`()
BEGIN
	SELECT industry_id, industry_name, is_active
	FROM tbl_industries
	WHERE is_active=1;
END

-- --------------------------------------------------------------------------------
-- To Fetch Business groups list
-- --------------------------------------------------------------------------------
DELIMITER $$

CREATE PROCEDURE `sp_business_groups_list`(
	IN client_id INT(11)
)
BEGIN
	SELECT business_group_id, business_group_name, group_id
	FROM tbl_business_groups
	WHERE group_id=client_id;
END

-- --------------------------------------------------------------------------------
-- To get countries of techno users
-- --------------------------------------------------------------------------------
DELIMITER $$

CREATE PROCEDURE `sp_user_countries_techno`()
BEGIN
	SELECT t1.country_id, t1.user_id 
	FROM tbl_user_countries t1
	INNER JOIN tbl_users t2 ON t2.user_id = t1.user_id
	INNER JOIN tbl_user_groups t3 ON 
	t2.user_group_id = t3.user_group_id
	AND t3.form_category_id = 3;
END

-- --------------------------------------------------------------------------------
-- To get domains of techno users
-- --------------------------------------------------------------------------------
DELIMITER $$

CREATE PROCEDURE `sp_user_domains_techno`()
BEGIN
	SELECT t1.domain_id, t1.user_id FROM tbl_user_domains t1
	INNER JOIN tbl_users t2 ON t2.user_id = t1.user_id 
	INNER JOIN tbl_user_groups t3 ON
	t2.user_group_id = t3.user_group_id AND t3.form_category_id = 3;
END

-- --------------------------------------------------------------------------------
-- To Save Client Details
-- --------------------------------------------------------------------------------
DELIMITER $$

CREATE PROCEDURE `sp_client_group_save`(
	IN groupname VARCHAR(50), email_id VARCHAR(100)
)
BEGIN
	INSERT INTO tbl_client_groups (group_name, group_admin)
	VALUES (groupname, email_id);
	SELECT group_id from tbl_client_groups where group_name=groupname;
END


-- --------------------------------------------------------------------------------
-- To Save Business group
-- --------------------------------------------------------------------------------
DELIMITER $$

CREATE PROCEDURE `sp_business_group_save`(
	IN businessgroupname VARCHAR(50), groupid INT(11),
	countryid INT(11),	session_user INT(11), current_time_stamp DATETIME
)
BEGIN
	INSERT INTO tbl_business_groups
	(
		group_id, country_id, business_group_name, created_by, created_on,
		updated_by, updated_on
	) VALUES
	(
		groupid, countryid, businessgroupname, session_user, 
		current_time_stamp, session_user, current_time_stamp
	);
	SELECT business_group_id FROM tbl_business_groups
	WHERE business_group_name=businessgroupname;
END

-- --------------------------------------------------------------------------------
-- Delete Client Countries
-- --------------------------------------------------------------------------------
DELIMITER $$

CREATE PROCEDURE `sp_client_countries_delete`(
	IN clientid INT(11)
)
BEGIN
	DELETE FROM tbl_client_countries WHERE client_id=clientid;
END


-- --------------------------------------------------------------------------------
-- Delete Client Domains
-- --------------------------------------------------------------------------------
DELIMITER $$

CREATE PROCEDURE `sp_client_domains_delete`(
	IN clientid INT(11)
)
BEGIN
	DELETE FROM tbl_client_domains WHERE client_id=clientid;
END

-- --------------------------------------------------------------------------------
-- Delete Incharge persons
-- --------------------------------------------------------------------------------
DELIMITER $$

CREATE PROCEDURE `sp_user_clients_delete`(
	IN clientid INT(11)
)
BEGIN
	DELETE FROM tbl_user_clients WHERE client_id=clientid;
END

-- --------------------------------------------------------------------------------
-- To delete organizations under client
-- --------------------------------------------------------------------------------
DELIMITER $$

CREATE PROCEDURE `sp_le_domain_industry_delete`(
	IN client_id INT(11)
)
BEGIN
	DELETE FROM tbl_legal_entity_domain_industry
	WHERE group_id=client_id;
END


-- --------------------------------------------------------------------------------
-- To get ids of legal entities which were inserted
-- --------------------------------------------------------------------------------
DELIMITER $$

CREATE PROCEDURE `sp_legal_entity_id_by_name`(
	IN legal_entity_names TEXT
)
BEGIN
	SELECT legal_entity_id, legal_entity_name
	FROM tbl_legal_entities
	WHERE find_in_set(legal_entity_name, legal_entity_names);
END


-- --------------------------------------------------------------------------------
-- To delete client configurations of Client
-- --------------------------------------------------------------------------------
DELIMITER $$

CREATE PROCEDURE `sp_client_configurations_delete`(
	IN clientid INT(11)
)
BEGIN
	DELETE FROM tbl_client_configurations WHERE client_id=clientid;
END

-- --------------------------------------------------------------------------------
-- To Save Client admin user
-- --------------------------------------------------------------------------------
DELIMITER $$

CREATE PROCEDURE `sp_client_user_save_admin`(
	IN clientid INT(11), username VARCHAR(100),
	current_time_stamp DATETIME
)
BEGIN
	INSERT INTO tbl_client_users (
		client_id, user_id,  email_id, employee_name, created_on,
		is_primary_admin, is_active
	) VALUES (
		clientid, 0, username, "Admin", current_time_stamp, 1, 1
	);
END