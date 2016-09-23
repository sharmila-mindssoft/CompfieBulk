-- --------------------------------------------------------------------------------
-- Returns Coutries that has been mapped with domain
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_country_mapped_list`;
DELIMITER $$
CREATE PROCEDURE `sp_country_mapped_list`()
BEGIN
	SELECT country_id, country_name, is_active
	FROM tbl_countries
	WHERE country_id IN (
		SELECT DISTINCT country_id
		FROM tbl_statutory_levels
	);
END

-- --------------------------------------------------------------------------------
-- Returns Domains that has been mapped with country
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_domain_mapped_list`;
DELIMITER $$
CREATE PROCEDURE `sp_domain_mapped_list`()
BEGIN
	SELECT domain_id, domain_name, is_active
	FROM tbl_domains
	WHERE domain_id in (
		SELECT distinct domain_id
		FROM tbl_statutory_levels
	);
END

-- --------------------------------------------------------------------------------
-- Returns Validity date for all country domain combinations
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_validitydays_settings_list`;
DELIMITER $$
CREATE PROCEDURE `sp_validitydays_settings_list`()
BEGIN
	SELECT validity_days_id, country_id, domain_id, days
	FROM tbl_validity_days_settings;
END

-- --------------------------------------------------------------------------------
-- Returns all possible country domain combinations which are mapped during
-- Statutory level creation
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_statutorylevels_mappings`;
DELIMITER $$
CREATE PROCEDURE `sp_statutorylevels_mappings`()
BEGIN
	SELECT country_id, domain_id
	FROM tbl_statutory_levels;
END

-- --------------------------------------------------------------------------------
-- To Save Validity date settings
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_validitydays_settings_save`;
DELIMITER $$
CREATE PROCEDURE `sp_validitydays_settings_save`(
	IN validitydaysid INT(11), countryid INT(11), domainid INT(11),
	validitydays INT(11), createdby INT(11),
	createdon DATETIME, updatedby INT(11),
	updatedon DATETIME
)
BEGIN
	IF validitydaysid is null then
		INSERT INTO tbl_validity_days_settings
		(country_id, domain_id, days, created_by, created_on, updated_by, updated_on)
		VALUES
		(countryid, domainid, validitydays, createdby, createdon, updatedby, updatedon);
	ELSE
		Update tbl_validity_days_settings set days=validitydays,
		updated_on = updatedon, updated_by = updatedby
		WHERE validity_days_id = validitydaysid;
	END IF;
END

-- --------------------------------------------------------------------------------
-- To check duplicate industry name
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_industry_master_checkduplicateindustry`;
DELIMITER $$
CREATE PROCEDURE `sp_industry_master_checkduplicateindustry`(
in industryid int(11), in industryname varchar(50))
BEGIN
	if industryid = 0 then
		SELECT count(1) FROM tbl_industries WHERE industry_name = industryname;
	else
        SELECT count(1) FROM tbl_industries WHERE industry_name = industryname
        and industry_id != industryid;
	end if;
END


-- --------------------------------------------------------------------------------
-- To get industry name by its id
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_industry_master_getindusdtrybyid`;
DELIMITER $$
CREATE PROCEDURE `sp_industry_master_getindusdtrybyid`(industryid int(11))
BEGIN
	SELECT industry_name FROM tbl_industries WHERE
    industry_id = industryid;
END


-- --------------------------------------------------------------------------------
-- To get industry details from its master
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_industry_master_getindustries`;
DELIMITER $$
CREATE PROCEDURE `sp_industry_master_getindustries`()
BEGIN
	SELECT t1.country_id, t2.country_name, t1.domain_id, t3.domain_name,
		t1.industry_id, t1.industry_name, t1.is_active FROM tbl_industries t1
        INNER JOIN tbl_countries t2 on t1.country_id = t2.country_id INNER JOIN
        tbl_domains t3 on t1.domain_id = t3.domain_id;
END

-- --------------------------------------------------------------------------------
-- To save industry activity log in activity log table
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_industry_master_saveactivitylog`;
DELIMITER $$
CREATE PROCEDURE `sp_industry_master_saveactivitylog`(
in activityLogId int(11), in userId int(11), in formId int(11),
in action varchar(500), in createdOn timestamp)
BEGIN
	INSERT INTO tbl_activity_log
    (activity_log_id, user_id, form_id, action, created_on)
    VALUES
	(activityLogId, userId, formId, action, createdOn);
END

-- --------------------------------------------------------------------------------
-- To save industry master details
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_industry_master_saveindustry`;
DELIMITER $$
CREATE PROCEDURE `sp_industry_master_saveindustry`(
in countryid int(11), in domainid int(11), in industryname varchar(50),
in createdby int(11), in createdon timestamp)
BEGIN
	INSERT INTO tbl_industries
    (industry_name, country_id, domain_id, created_by, created_on)
    VALUES
	(industryname, countryid, domainid, createdby, createdon);
END

-- --------------------------------------------------------------------------------
-- To update industry master details
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_industry_master_updateindustry`;
DELIMITER $$
CREATE PROCEDURE `sp_industry_master_updateindustry`(
	in industryId int(11), in industryName varchar(50), in countryId int(11),
    in domainId int(11), in updatedBy int(11)
)
BEGIN
	UPDATE tbl_industries
    SET
    industry_name = industryName,
    country_id = countryId,
    domain_id = domainId,
    updated_by = updatedBy
    WHERE
    industry_id = industryId;
END

-- --------------------------------------------------------------------------------
-- To update industry master status
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_industry_master_updatestatus`;
DELIMITER $$
CREATE PROCEDURE `sp_industry_master_updatestatus`(
	in industryId int(11), in isActive tinyint(4), in updatedBy int(11))
BEGIN
	UPDATE tbl_industries
    SET
    is_active = isActive,
    updated_by = updatedBy
    WHERE
    industry_id = industryId;
END

-- --------------------------------------------------------------------------------
-- To check for dupliacte statutory nature name
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_statutory_nature_checkduplicatenature`;
DELIMITER $$
CREATE PROCEDURE `sp_statutory_nature_checkduplicatenature`(
	in statutoryNatureName varchar(50),
    in statutoryNatureId int(11)
)
BEGIN
	if statutoryNatureId = 0 then
		SELECT count(1) AS cnt FROM tbl_statutory_natures
        WHERE statutory_nature_name = statutoryNatureName;
	else
		SELECT count(1) as cnt FROM tbl_statutory_natures
        WHERE statutory_nature_name = statutoryNatureName
        AND statutory_nature_id != statutoryNatureId;
	END IF;
END

-- --------------------------------------------------------------------------------
-- To -get statutory nature master details
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_statutory_nature_getstatutorynatures`;
DELIMITER $$
CREATE PROCEDURE `sp_statutory_nature_getstatutorynatures`()
BEGIN
	SELECT t1.statutory_nature_id, t1.statutory_nature_name,
    t1.country_id, t2.country_name, t1.is_active
    FROM
    tbl_statutory_natures as t1,
    tbl_countries as t2
    WHERE
    t2.country_id = t1.country_id
    ORDER BY t1.statutory_nature_name;
END

-- --------------------------------------------------------------------------------
-- To update statutory nature master details
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_statutory_nature_updatestatutorynature`;
DELIMITER $$
CREATE PROCEDURE `sp_statutory_nature_updatestatutorynature`(
IN statutoryNatureId int(11), in statutoryNatureName varchAR(50),
in countryId int(11), in updatedBy int(11))
BEGIN
	update tbl_statutory_natures set
    statutory_nature_name = statutoryNatureName,
    country_id = countryId,
    updated_by = updatedBy
    where
    statutory_nature_id = statutoryNatureId;
END

-- --------------------------------------------------------------------------------
-- To update statutory nature status
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS sp_statutory_nature_updatestatutorynaturestatus;
DELIMITER $$
CREATE PROCEDURE `sp_statutory_nature_updatestatutorynaturestatus`(
in statutoryNatureId int(11), in updatedBy int(11), in isActive tinyint(4))
BEGIN
	update tbl_statutory_natures set
    is_active = isActive,
    updated_by = updatedBy
    where
    statutory_nature_id = statutoryNatureId;
END

-- --------------------------------------------------------------------------------
-- To get statutory nature details by its id
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS sp_statutory_natures_getnaturebyid;
DELIMITER $$
CREATE PROCEDURE `sp_statutory_natures_getnaturebyid`(
	in statutoryNatureId int(11))
BEGIN
	SELECT statutory_nature_name FROM tbl_statutory_natures
    WHERE statutory_nature_id = statutoryNatureId;

END

-- --------------------------------------------------------------------------------
-- To save statutory nature details
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS sp_statutorynature_savestatutorynature;
DELIMITER $$
CREATE PROCEDURE `sp_statutorynature_savestatutorynature`(
in statutoryNatureName varchar(50), in countryId int(11),
in createdBy int(11), in createdOn timestamp)
BEGIN
	INSERT INTO tbl_statutory_natures
    (statutory_nature_name, country_id, created_by, created_on)
    VALUES
    (statutoryNatureName, countryId, createdBy, createdOn);
END

-- --------------------------------------------------------------------------------
-- get domains data based on user domain settings
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS sp_tbl_domains_for_user;
DELIMITER $$
CREATE procedure `sp_tbl_domains_for_user`(IN _user_id VARCHAR(11))
BEGIN
	SELECT DISTINCT t1.domain_id, t1.domain_name, t1.is_active FROM tbl_domains t1
    INNER JOIN tbl_user_domains t2 on t1.domain_id = t2.domain_id WHERE
    t1.is_active = 1 AND t2.user_id LIKE _user_id
	ORDER BY t1.domain_name;

END;

-- --------------------------------------------------------------------------------
-- To Get admin forms
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS sp_tbl_forms_getadminforms;

DELIMITER $$
CREATE procedure `sp_tbl_forms_getadminforms`()
BEGIN
	SELECT T01.form_id, T01.form_name, T01.form_url, T01.form_order, T01.parent_menu,
	T02.form_category, T03.form_type FROM tbl_forms T01
	INNER JOIN tbl_form_category T02 ON T02.form_category_id = T01.form_category_id
	INNER JOIN tbl_form_type T03 ON T03.form_type_id = T01.form_type_id
	WHERE T01.form_category_id = 1 ORDER BY T01.form_order;

END;


-- --------------------------------------------------------------------------------
-- Audit trail report procedure, This has four result set which are Forms, Users, Activity-log and Activity-log total
-- --------------------------------------------------------------------------------

DROP PROCEDURE sp_get_audit_trails;
DELIMITER $$
CREATE PROCEDURE `sp_get_audit_trails`(
	IN _from_date varchar(10), IN _to_date varchar(10),
	IN _user_id varchar(10), IN _form_id varchar(10),
	IN _from_limit INT, IN _to_limit INT
)
BEGIN
	SELECT form_id, form_name FROM tbl_forms WHERE form_id != 26;
	SELECT user_id, employee_name, employee_code, is_active
	FROM tbl_users;
	SELECT user_id, form_id, action, created_on
	FROM tbl_activity_log
	WHERE
		date(created_on) >= _from_date
		AND date(created_on) <= _to_date
		AND user_id LIKE _user_id AND form_id LIKE _form_id
		ORDER BY user_id ASC, DATE(created_on) DESC
		limit _from_limit, _to_limit;

	SELECT count(0) as total FROM tbl_activity_log
	WHERE
		date(created_on) >= _from_date
		AND date(created_on) <= _to_date
		AND user_id LIKE _user_id AND form_id LIKE _form_id;
END;


-- --------------------------------------------------------------------------------
-- To get form_ids based on user settings
-- --------------------------------------------------------------------------------

DROP PROCEDURE sp_tbl_forms_getuserformids;
DELIMITER $$
CREATE PROCEDURE `sp_tbl_forms_getuserformids`(
	IN _user_id INT
)
BEGIN
	if _user_id = 0 then
		SELECT form_id as form_id FROM tbl_forms WHERE form_category_id = 1;
	else
		SELECT t1.form_ids as form_id from tbl_user_groups t1
		INNER JOIN tbl_users t2 on t1.user_group_id = t2.user_group_id
		AND t2.user_id = _user_id;
	end if;
END;

DROP PROCEDURE sp_tbl_forms_getforms;
DELIMITER $$
CREATE PROCEDURE `sp_tbl_forms_getforms`()
BEGIN
	SELECT t1.form_id, t1.form_category_id, t2.form_category,
	t1.form_type_id, t3.form_type, t1.form_name, t1.form_url,
	t1.form_order, t1.parent_menu FROM tbl_forms t1
	INNER JOIN tbl_form_category t2 ON t2.form_category_id = t1.form_category_id
	INNER JOIN tbl_form_type t3 ON t3.form_type_id = t1.form_type_id WHERE
	t1.form_category_id != 1 ORDER BY t1.form_order;

END;

DROP PROCEDURE sp_tbl_user_group_getusergroupdetails;
DELIMITER $$
CREATE PROCEDURE `sp_tbl_user_group_getusergroupdetails`()
BEGIN
	SELECT t1.user_group_id, t1.user_group_name, t1.form_category_id,
	t1.form_ids, t1.is_active, (select count(*) from tbl_users u where user_group_id = u.user_group_id)as count,
	FROM tbl_user_groups t1 ORDER BY t1.user_group_name;

END;

DROP PROCEDURE sp_tbl_form_category_get;
DELIMITER $$
CREATE PROCEDURE `sp_tbl_form_category_get`()
BEGIN
	SELECT form_category_id, form_category FROM form_category_id in (2, 3);
END;
-----------------------------------------------------------------------------------
-- To get the list of groups with countries and number of legal entities
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_client_groups_list`;
DELIMITER $$
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
DROP PROCEDURE IF EXISTS `sp_countries_for_user`;
DELIMITER $$
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
DROP PROCEDURE IF EXISTS `sp_domains_for_user`;
DELIMITER $$
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
DROP PROCEDURE IF EXISTS `sp_industries_active_list`;
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
DROP PROCEDURE IF EXISTS `sp_business_groups_list`;
DELIMITER $$
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
DROP PROCEDURE IF EXISTS `sp_user_countries_techno`;
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
DROP PROCEDURE IF EXISTS `sp_user_domains_techno`;
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
DROP PROCEDURE IF EXISTS `sp_client_group_save`;
DELIMITER $$
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
DROP PROCEDURE IF EXISTS `sp_business_group_save`;
DELIMITER $$
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
DROP PROCEDURE IF EXISTS `sp_client_countries_delete`;
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
DROP PROCEDURE IF EXISTS `sp_client_domains_delete`;
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
DROP PROCEDURE IF EXISTS `sp_user_clients_delete`;
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
DROP PROCEDURE IF EXISTS `sp_le_domain_industry_delete`;
DELIMITER $$
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
DROP PROCEDURE IF EXISTS `sp_legal_entity_id_by_name`;
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
DROP PROCEDURE IF EXISTS `sp_client_configurations_delete`;
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
DROP PROCEDURE IF EXISTS `sp_client_user_save_admin`;
DELIMITER $$
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
DROP PROCEDURE IF EXISTS `sp_client_group_is_duplicate_groupname`;
DELIMITER $$
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
DROP PROCEDURE IF EXISTS `sp_businessgroup_is_duplicate_businessgroupname`;
DELIMITER $$
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
DROP PROCEDURE IF EXISTS `sp_legalentity_is_duplicate_legalentityname`;
DELIMITER $$
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
DROP PROCEDURE IF EXISTS `sp_client_groups_details_by_id`;
DELIMITER $$
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
DROP PROCEDURE IF EXISTS `sp_legal_entity_details_by_group_id`;
DELIMITER $$
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
DROP PROCEDURE IF EXISTS `sp_client_domains_by_group_id`;
DELIMITER $$
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
DROP PROCEDURE IF EXISTS `sp_user_clients_by_group_id`;
DELIMITER $$
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
DROP PROCEDURE IF EXISTS `sp_client_configuration_by_group_id`;
DELIMITER $$
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
DROP PROCEDURE IF EXISTS `sp_le_d_industry_by_group_id`;
DELIMITER $$
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
DROP PROCEDURE IF EXISTS `sp_client_groups_is_valid_group_id`;
DELIMITER $$
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
DROP PROCEDURE IF EXISTS `sp_client_countries_by_group_id`;
DELIMITER $$
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
DROP PROCEDURE IF EXISTS `sp_client_users_count`;
DELIMITER $$
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
DROP PROCEDURE IF EXISTS `sp_legal_entities_space_used`;
DELIMITER $$
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
DROP PROCEDURE IF EXISTS `sp_client_group_update`;
DELIMITER $$
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
DROP PROCEDURE IF EXISTS `sp_client_groups_change_status`;
DELIMITER $$
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
DROP PROCEDURE IF EXISTS `sp_notifications_notify_incharge`;
DELIMITER $$
CREATE PROCEDURE `sp_notifications_notify_incharge`(
    IN notification TEXT, url TEXT
)
BEGIN
    INSERT INTO tbl_notifications
    (notification_text, link, created_on) VALUES
    (notification, url, now());
END

-- --------------------------------------------------------------------------------
-- To get the list of techno users
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_users_techno`;
DELIMITER $$
CREATE PROCEDURE `sp_users_techno`()
BEGIN
	SELECT user_id, concat(employee_code,'-',employee_name) as e_name,
	is_active FROM tbl_users
	WHERE user_group_id in (
		select user_group_id from tbl_user_groups
		where form_category_id = 3
	);
END
