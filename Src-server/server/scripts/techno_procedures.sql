-- --------------------------------------------------------------------------------
-- To get the list of groups with countries and number of legal entities
-- --------------------------------------------------------------------------------
DELIMITER $$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_client_groups_list`()
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

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_countries_active_list`()
BEGIN
	SELECT country_id, country_name, is_active
	FROM tbl_countries 
	WHERE is_active=1;
END

-- --------------------------------------------------------------------------------
-- To Fetch Active Domains List
-- --------------------------------------------------------------------------------
DELIMITER $$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_domains_active_list`()
BEGIN
	SELECT domain_id, domain_name, is_active
	FROM tbl_domains WHERE is_active=1;
END

-- --------------------------------------------------------------------------------
-- To Fetch active industry list
-- --------------------------------------------------------------------------------
DELIMITER $$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_industries_active_list`()
BEGIN
	SELECT industry_id, industry_name, is_active
	FROM tbl_industries
	WHERE is_active=1;
END

-- --------------------------------------------------------------------------------
-- To Fetch Business groups list
-- --------------------------------------------------------------------------------
DELIMITER $$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_business_groups_list`(
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

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_user_countries_techno`()
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

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_user_domains_techno`()
BEGIN
	SELECT t1.domain_id, t1.user_id FROM tbl_user_domains t1
	INNER JOIN tbl_users t2 ON t2.user_id = t1.user_id 
	INNER JOIN tbl_user_groups t3 ON
	t2.user_group_id = t3.user_group_id AND t3.form_category_id = 3;
END