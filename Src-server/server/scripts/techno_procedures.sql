-- --------------------------------------------------------------------------------
-- To get the list of groups with countries and number of legal entities
-- --------------------------------------------------------------------------------
DELIMITER $$
DROP PROCEDURE IF EXISTS `sp_client_groups_list`;
CREATE PROCEDURE `sp_client_groups_list`()
BEGIN
    select client_id, group_name,
    (
        select group_concat(country_name) from tbl_countries 
        where country_id in (
            select country_id from tbl_client_countries
            where client_id=client_id
        )
    ) as country_names,
    (
        select count(legal_entity_id) from tbl_legal_entities tle
        WHERE tle.client_id=tcg.client_id
    ) as no_of_legal_entities,
    (
        select sum(is_active) from tbl_legal_entities tle
        WHERE tle.client_id=tcg.client_id
    ) as is_active
    FROM tbl_client_groups tcg;
END

-- --------------------------------------------------------------------------------
-- To Fetch Active Countries List
-- --------------------------------------------------------------------------------
DELIMITER $$
DROP PROCEDURE IF EXISTS `sp_countries_for_user`;
CREATE PROCEDURE `sp_countries_for_user`(
    IN session_user INT(11)
)
BEGIN
    SELECT country_id, country_name, is_active
    FROM tbl_countries 
    WHERE is_active=1 and country_id in (
        SELECT country_id FROM tbl_user_countries
        WHERE user_id = session_user
    );
END

-- --------------------------------------------------------------------------------
-- To Fetch Active Domains List
-- --------------------------------------------------------------------------------
DELIMITER $$
DROP PROCEDURE IF EXISTS `sp_domains_for_user`;
CREATE PROCEDURE `sp_domains_for_user`(
    IN session_user INT(11)
)
BEGIN
    SELECT domain_id, domain_name, is_active
    FROM tbl_domains WHERE is_active=1 
    and domain_id in (
        SELECT domain_id FROM tbl_user_domains
        WHERE user_id=session_user
    );
END

-- --------------------------------------------------------------------------------
-- To Fetch active industry list
-- --------------------------------------------------------------------------------
DELIMITER $$
DROP PROCEDURE IF EXISTS `sp_industries_active_list`;
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
DROP PROCEDURE IF EXISTS `sp_business_groups_list`;
CREATE PROCEDURE `sp_business_groups_list`(
    IN client_id INT(11)
)
BEGIN
    SELECT business_group_id, business_group_name, client_id
    FROM tbl_business_groups
    WHERE client_id=client_id;
END

-- --------------------------------------------------------------------------------
-- To get countries of techno users
-- --------------------------------------------------------------------------------
DELIMITER $$
DROP PROCEDURE IF EXISTS `sp_user_countries_techno`;
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
DROP PROCEDURE IF EXISTS `sp_user_domains_techno`;
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
DROP PROCEDURE IF EXISTS `sp_client_group_save`;
CREATE PROCEDURE `sp_client_group_save`(
    IN groupname VARCHAR(50), email_id VARCHAR(100)
)
BEGIN
    INSERT INTO tbl_client_groups (group_name, group_admin)
    VALUES (groupname, email_id);
END


-- --------------------------------------------------------------------------------
-- To Save Business group
-- --------------------------------------------------------------------------------
DELIMITER $$
DROP PROCEDURE IF EXISTS `sp_business_group_save`;
CREATE PROCEDURE `sp_business_group_save`(
    IN businessgroupname VARCHAR(50), groupid INT(11),
    countryid INT(11),  session_user INT(11), current_time_stamp DATETIME
)
BEGIN
    INSERT INTO tbl_business_groups
    (
        client_id, country_id, business_group_name, created_by, created_on,
        updated_by, updated_on
    ) VALUES
    (
        groupid, countryid, businessgroupname, session_user, 
        current_time_stamp, session_user, current_time_stamp
    );
END

-- --------------------------------------------------------------------------------
-- Delete Client Countries
-- --------------------------------------------------------------------------------
DELIMITER $$
DROP PROCEDURE IF EXISTS `sp_client_countries_delete`;
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
DROP PROCEDURE IF EXISTS `sp_client_domains_delete`;
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
DROP PROCEDURE IF EXISTS `sp_user_clients_delete`;
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
DROP PROCEDURE IF EXISTS `sp_le_domain_industry_delete`;
CREATE PROCEDURE `sp_le_domain_industry_delete`(
    IN clientid INT(11)
)
BEGIN
    DELETE FROM tbl_legal_entity_domain_industry
    WHERE client_id=clientid;
END


-- --------------------------------------------------------------------------------
-- To get ids of legal entities which were inserted
-- --------------------------------------------------------------------------------
DELIMITER $$
DROP PROCEDURE IF EXISTS `sp_legal_entity_id_by_name`;
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
DROP PROCEDURE IF EXISTS `sp_client_configurations_delete`;
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
DROP PROCEDURE IF EXISTS `sp_client_user_save_admin`;
CREATE PROCEDURE `sp_client_user_save_admin`(
    IN clientid INT(11), username VARCHAR(100),
    current_time_stamp DATETIME
)
BEGIN
    INSERT INTO tbl_client_users (
        client_id, legal_entity_id, user_id,  email_id, employee_name, created_on,
        is_primary_admin, is_active
    ) VALUES (
        clientid, 0, 0, username, "Admin", current_time_stamp, 1, 1
    );
END

-- --------------------------------------------------------------------------------
-- To Check for duplicate group name
-- --------------------------------------------------------------------------------
DELIMITER $$
DROP PROCEDURE IF EXISTS `sp_client_group_is_duplicate_groupname`;
CREATE PROCEDURE `sp_client_group_is_duplicate_groupname`(
    IN groupname VARCHAR(50), clientid INT(11)
)
BEGIN
    IF clientid IS NULL THEN 
        SELECT count(client_id) as count FROM tbl_client_groups 
        WHERE group_name=groupname;
    ELSE
        SELECT count(client_id) as count FROM tbl_client_groups
        WHERE group_name=groupname and client_id != clientid;
    END IF;
END

-- --------------------------------------------------------------------------------
-- To Check for dupliacte business group name
-- --------------------------------------------------------------------------------
DELIMITER $$
DROP PROCEDURE IF EXISTS `sp_businessgroup_is_duplicate_businessgroupname`;
CREATE PROCEDURE `sp_businessgroup_is_duplicate_businessgroupname`(
    IN bg_name VARCHAR(50), bg_id INT(11), clientid INT(11)
)
BEGIN
    IF bg_id IS NULL THEN 
        SELECT count(business_group_id) as count FROM tbl_business_groups 
        WHERE business_group_name=bg_name and client_id=clientid;
    ELSE
        SELECT count(business_group_id) as count FROM tbl_business_groups
        WHERE business_group_name=bg_name and client_id=clientid
        and busienss_group_id = bg_id;
    END IF;
END

-- --------------------------------------------------------------------------------
-- To Check for dupliacte Legal entity name
-- --------------------------------------------------------------------------------
DELIMITER $$
DROP PROCEDURE IF EXISTS `sp_legalentity_is_duplicate_legalentityname`;
CREATE PROCEDURE `sp_legalentity_is_duplicate_legalentityname`(
    IN le_name VARCHAR(50), le_id INT(11), clientid INT(11)
)
BEGIN
    IF le_id IS NULL THEN 
        SELECT count(legal_entity_id) as count FROM tbl_legal_entities
        WHERE legal_entity_name=le_name and client_id=clientid;
    ELSE
        SELECT count(legal_entity_id) as count FROM tbl_legal_entities
        WHERE legal_entity_name=le_name and client_id=clientid
        and legal_entity_id != le_id;
    END IF;
END

-- --------------------------------------------------------------------------------
-- To Get Group name and admin email id by id
-- --------------------------------------------------------------------------------
DELIMITER $$
DROP PROCEDURE IF EXISTS `sp_client_groups_details_by_id`;
CREATE PROCEDURE `sp_client_groups_details_by_id`(
    IN clientid INT(11)
)
BEGIN
    SELECT group_name, group_admin FROM tbl_client_groups
    WHERE client_id=clientid;
END


-- --------------------------------------------------------------------------------
-- To get Legal entity details by group id
-- --------------------------------------------------------------------------------
DELIMITER $$
DROP PROCEDURE IF EXISTS `sp_legal_entity_details_by_group_id`;
CREATE PROCEDURE `sp_legal_entity_details_by_group_id`(
    IN clientid INT(11)
)
BEGIN
    SELECT legal_entity_id, country_id, business_group_id, 
    (
        SELECT business_group_name FROM tbl_business_groups tbg
        WHERE tbg.business_group_id=tle.business_group_id
    ) as business_group_name,
    legal_entity_name, contract_from, contract_to, logo,
    file_space_limit, total_licence, sms_subscription
    FROM tbl_legal_entities tle WHERE client_id=clientid;
END

-- --------------------------------------------------------------------------------
-- To get domains of client by legal entity
-- --------------------------------------------------------------------------------
DELIMITER $$
DROP PROCEDURE IF EXISTS `sp_client_domains_by_group_id`;
CREATE PROCEDURE `sp_client_domains_by_group_id`(
    IN clientid INT(11)
)
BEGIN
    SELECT client_id, legal_entity_id, domain_id
    FROM tbl_client_domains WHERE client_id = clientid;
END

-- --------------------------------------------------------------------------------
-- To get incharge persons by group id
-- --------------------------------------------------------------------------------
DELIMITER $$
DROP PROCEDURE IF EXISTS `sp_user_clients_by_group_id`;
CREATE PROCEDURE `sp_user_clients_by_group_id`(
    IN clientid INT(11)
)
BEGIN
    SELECT client_id, legal_entity_id, user_id
    FROM tbl_user_clients WHERE client_id = clientid;
END

-- --------------------------------------------------------------------------------
-- to get configurations of Client by group id
-- --------------------------------------------------------------------------------
DELIMITER $$
DROP PROCEDURE IF EXISTS `sp_client_configuration_by_group_id`;
CREATE PROCEDURE `sp_client_configuration_by_group_id`(
    IN clientid INT(11)
)
BEGIN
    SELECT country_id, domain_id, period_from, period_to
    FROM tbl_client_configurations WHERE client_id = clientid;
END

-- --------------------------------------------------------------------------------
-- Get Organizations of Client 
-- --------------------------------------------------------------------------------
DELIMITER $$
DROP PROCEDURE IF EXISTS `sp_le_d_industry_by_group_id`;
CREATE PROCEDURE `sp_le_d_industry_by_group_id`(
    IN clientid INT(11)
)
BEGIN
    SELECT legal_entity_id, domain_id, industry_id, no_of_units
    FROM tbl_legal_entity_domain_industry WHERE client_id = clientid;
END


-- --------------------------------------------------------------------------------
-- To check whether the given client id is valid or not
-- --------------------------------------------------------------------------------
DELIMITER $$
DROP PROCEDURE IF EXISTS `sp_client_groups_is_valid_group_id`;
CREATE PROCEDURE `sp_client_groups_is_valid_group_id`(
    IN clientid INT(11)
)
BEGIN
    SELECT count(client_id) as count FROM tbl_client_groups 
    WHERE client_id=clientid;
END


-- --------------------------------------------------------------------------------
-- To get countries of a Client
-- --------------------------------------------------------------------------------
DELIMITER $$
DROP PROCEDURE IF EXISTS `sp_client_countries_by_group_id`;
CREATE PROCEDURE `sp_client_countries_by_group_id`(
    IN group_id INT(11)
)
BEGIN
    SELECT country_id FROM tbl_client_countries
    WHERE client_id = group_id;
END

-- --------------------------------------------------------------------------------
-- To get number of client users
-- --------------------------------------------------------------------------------
DELIMITER $$
DROP PROCEDURE IF EXISTS `sp_client_users_count`;
CREATE PROCEDURE `sp_client_users_count`(
    IN group_id INT(11), entity_id INT(11)
)
BEGIN
    SELECT count(user_id)+1 as count FROM tbl_client_users
    WHERE client_id = group_id and
    legal_entity_id = entity_id;
END

-- --------------------------------------------------------------------------------
-- To get the used space of a legal entity
-- --------------------------------------------------------------------------------
DELIMITER $$
DROP PROCEDURE IF EXISTS `sp_legal_entities_space_used`;
CREATE PROCEDURE `sp_legal_entities_space_used`(
    IN le_id INT(11)
)
BEGIN
    SELECT used_space FROM tbl_legal_entities
    WHERE legal_entity_id=le_id;
END

-- --------------------------------------------------------------------------------
-- To Update Client Group
-- --------------------------------------------------------------------------------
DELIMITER $$
DROP PROCEDURE IF EXISTS `sp_client_group_update`;
CREATE PROCEDURE `sp_client_group_update` (
    IN groupname VARCHAR(50), groupid INT(11)
)
BEGIN
    UPDATE tbl_client_groups set group_name=groupname
    WHERE client_id=groupid;
END

-- --------------------------------------------------------------------------------
-- To Change the status of client
-- --------------------------------------------------------------------------------
DELIMITER $$
DROP PROCEDURE IF EXISTS `sp_client_groups_change_status`;
CREATE PROCEDURE `sp_client_groups_change_status`(
    IN clientid INT(11), isactive bool
)
BEGIN
    UPDATE tbl_legal_entities set is_active = isactive
    WHERE client_id=clientid;
    SELECT group_name FROM tbl_client_groups
    WHERE client_id=clientid;
END

-- --------------------------------------------------------------------------------
-- To Notify the incharge person, that the legal entity is assigned to him
-- --------------------------------------------------------------------------------
DELIMITER $$
DROP PROCEDURE IF EXISTS `sp_notifications_notify_incharge`;
CREATE PROCEDURE `sp_notifications_notify_incharge`(
    IN notification TEXT, url TEXT
)
BEGIN
    INSERT INTO tbl_notifications 
    (notification_text, link, created_on) VALUES
    (notification, url, now());
END