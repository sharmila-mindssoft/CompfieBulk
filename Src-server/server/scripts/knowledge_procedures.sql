-- --------------------------------------------------------------------------------
-- Returns Coutries that has been mapped with domain
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_country_mapped_list`;
DELIMITER //
CREATE PROCEDURE `sp_country_mapped_list`()
BEGIN
	SELECT country_id, country_name, is_active
	FROM tbl_countries
	WHERE country_id IN (
		SELECT DISTINCT country_id
		FROM tbl_statutory_levels
	);
END //
DELIMITER ;

-- --------------------------------------------------------------------------------
-- Returns Domains that has been mapped with country
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_domain_mapped_list`;
DELIMITER //
CREATE PROCEDURE `sp_domain_mapped_list`()
BEGIN
	SELECT domain_id, domain_name, is_active
	FROM tbl_domains
	WHERE domain_id in (
		SELECT distinct domain_id
		FROM tbl_statutory_levels
	);
END //
DELIMITER ;

-- --------------------------------------------------------------------------------
-- Returns Validity date for all country domain combinations
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_validitydays_settings_list`;
DELIMITER //
CREATE PROCEDURE `sp_validitydays_settings_list`()
BEGIN
	SELECT validity_days_id, country_id, domain_id, days
	FROM tbl_validity_days_settings;
END //
DELIMITER ;

-- --------------------------------------------------------------------------------
-- Returns all possible country domain combinations which are mapped during
-- Statutory level creation
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_statutorylevels_mappings`;
DELIMITER //
CREATE PROCEDURE `sp_statutorylevels_mappings`()
BEGIN
	SELECT country_id, domain_id
	FROM tbl_statutory_levels;
END //
DELIMITER ;

-- --------------------------------------------------------------------------------
-- To Save Validity date settings
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_validitydays_settings_save`;
DELIMITER //
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
END //
DELIMITER ;

-- --------------------------------------------------------------------------------
-- To check duplicate industry name
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_industry_master_checkduplicateindustry`;
DELIMITER //
CREATE PROCEDURE `sp_industry_master_checkduplicateindustry`(
in industryid int(11), in industryname varchar(50))
BEGIN
	if industryid = 0 then
		SELECT count(1) FROM tbl_industries WHERE industry_name = industryname;
	else
        SELECT count(1) FROM tbl_industries WHERE industry_name = industryname
        and industry_id != industryid;
	end if;
END //
DELIMITER ;


-- --------------------------------------------------------------------------------
-- To get industry name by its id
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_industry_master_getindusdtrybyid`;
DELIMITER //
CREATE PROCEDURE `sp_industry_master_getindusdtrybyid`(industryid int(11))
BEGIN
	SELECT industry_name FROM tbl_industries WHERE
    industry_id = industryid;
END //
DELIMITER ;


-- --------------------------------------------------------------------------------
-- To get industry details from its master
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_industry_master_getindustries`;
DELIMITER //
CREATE PROCEDURE `sp_industry_master_getindustries`()
BEGIN
	SELECT t1.country_id, t2.country_name, t1.domain_id, t3.domain_name,
		t1.industry_id, t1.industry_name, t1.is_active FROM tbl_industries t1
        INNER JOIN tbl_countries t2 on t1.country_id = t2.country_id INNER JOIN
        tbl_domains t3 on t1.domain_id = t3.domain_id;
END //
DELIMITER ;

-- --------------------------------------------------------------------------------
-- To save industry activity log in activity log table
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_industry_master_saveactivitylog`;
DELIMITER //
CREATE PROCEDURE `sp_industry_master_saveactivitylog`(
in activityLogId int(11), in userId int(11), in formId int(11),
in action varchar(500), in createdOn timestamp)
BEGIN
	INSERT INTO tbl_activity_log
    (activity_log_id, user_id, form_id, action, created_on)
    VALUES
	(activityLogId, userId, formId, action, createdOn);
END //
DELIMITER ;

-- --------------------------------------------------------------------------------
-- To save industry master details
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_industry_master_saveindustry`;
DELIMITER //
CREATE PROCEDURE `sp_industry_master_saveindustry`(
in countryid int(11), in domainid int(11), in industryname varchar(50),
in createdby int(11), in createdon timestamp)
BEGIN
	INSERT INTO tbl_industries
    (industry_name, country_id, domain_id, created_by, created_on)
    VALUES
	(industryname, countryid, domainid, createdby, createdon);
END //
DELIMITER ;

-- --------------------------------------------------------------------------------
-- To update industry master details
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_industry_master_updateindustry`;
DELIMITER //
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
END //
DELIMITER ;

-- --------------------------------------------------------------------------------
-- To update industry master status
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_industry_master_updatestatus`;
DELIMITER //
CREATE PROCEDURE `sp_industry_master_updatestatus`(
	in industryId int(11), in isActive tinyint(4), in updatedBy int(11))
BEGIN
	UPDATE tbl_industries
    SET
    is_active = isActive,
    updated_by = updatedBy
    WHERE
    industry_id = industryId;
END //
DELIMITER ;

-- --------------------------------------------------------------------------------
-- To check for dupliacte statutory nature name
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_statutory_nature_checkduplicatenature`;
DELIMITER //
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
END //
DELIMITER ;

-- --------------------------------------------------------------------------------
-- To -get statutory nature master details
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_statutory_nature_getstatutorynatures`;
DELIMITER //
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
END //
DELIMITER ;

-- --------------------------------------------------------------------------------
-- To update statutory nature master details
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_statutory_nature_updatestatutorynature`;
DELIMITER //
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
END //
DELIMITER ;

-- --------------------------------------------------------------------------------
-- To update statutory nature status
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS sp_statutory_nature_updatestatutorynaturestatus;
DELIMITER //
CREATE PROCEDURE `sp_statutory_nature_updatestatutorynaturestatus`(
in statutoryNatureId int(11), in updatedBy int(11), in isActive tinyint(4))
BEGIN
	update tbl_statutory_natures set
    is_active = isActive,
    updated_by = updatedBy
    where
    statutory_nature_id = statutoryNatureId;
END //
DELIMITER ;

-- --------------------------------------------------------------------------------
-- To get statutory nature details by its id
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS sp_statutory_natures_getnaturebyid;
DELIMITER //
CREATE PROCEDURE `sp_statutory_natures_getnaturebyid`(
	in statutoryNatureId int(11))
BEGIN
	SELECT statutory_nature_name FROM tbl_statutory_natures
    WHERE statutory_nature_id = statutoryNatureId;

END //
DELIMITER ;

-- --------------------------------------------------------------------------------
-- To save statutory nature details
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS sp_statutorynature_savestatutorynature;
DELIMITER //
CREATE PROCEDURE `sp_statutorynature_savestatutorynature`(
in statutoryNatureName varchar(50), in countryId int(11),
in createdBy int(11), in createdOn timestamp)
BEGIN
	INSERT INTO tbl_statutory_natures
    (statutory_nature_name, country_id, created_by, created_on)
    VALUES
    (statutoryNatureName, countryId, createdBy, createdOn);
END //
DELIMITER ;

-- --------------------------------------------------------------------------------
-- get domains data based on user domain settings
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS sp_tbl_domains_for_user;
DELIMITER //
CREATE procedure `sp_tbl_domains_for_user`(IN _user_id VARCHAR(11))
BEGIN
	IF _user_id > 0 THEN
		SELECT DISTINCT t1.domain_id, t1.domain_name, t1.is_active
		FROM tbl_domains t1
		INNER JOIN tbl_user_domains t2 on t1.domain_id = t2.domain_id
		WHERE t2.user_id LIKE _user_id
		ORDER BY t1.domain_name;
	ELSE
		SELECT domain_id, domain_name, is_active FROM tbl_domains
		ORDER BY domain_name;
	END IF;
END //
DELIMITER ;

-- --------------------------------------------------------------------------------
-- To Get admin forms
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS sp_tbl_forms_getadminforms;

DELIMITER //
CREATE procedure `sp_tbl_forms_getadminforms`()
BEGIN
	SELECT T01.form_id, T01.form_name, T01.form_url, T01.form_order, T01.parent_menu,
	T02.form_category, T03.form_type FROM tbl_forms T01
	INNER JOIN tbl_form_category T02 ON T02.form_category_id = T01.form_category_id
	INNER JOIN tbl_form_type T03 ON T03.form_type_id = T01.form_type_id
	WHERE T01.form_category_id = 1 ORDER BY T01.form_order;
END //
DELIMITER ;

-- --------------------------------------------------------------------------------
-- Audit trail report procedure, This has four result set which are Forms, Users, Activity-log and Activity-log total
-- --------------------------------------------------------------------------------

DROP PROCEDURE IF EXISTS sp_get_audit_trails;
DELIMITER //
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
END //
DELIMITER ;


-- --------------------------------------------------------------------------------
-- To get form_ids based on user settings
-- --------------------------------------------------------------------------------

DROP PROCEDURE IF EXISTS sp_tbl_forms_getuserformids;
DELIMITER //
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
END //
DELIMITER ;

DROP PROCEDURE IF EXISTS sp_tbl_forms_getforms;
DELIMITER //
CREATE PROCEDURE `sp_tbl_forms_getforms`()
BEGIN
	SELECT t1.form_id, t1.form_category_id, t2.form_category,
	t1.form_type_id, t3.form_type, t1.form_name, t1.form_url,
	t1.form_order, t1.parent_menu FROM tbl_forms t1
	INNER JOIN tbl_form_category t2 ON t2.form_category_id = t1.form_category_id
	INNER JOIN tbl_form_type t3 ON t3.form_type_id = t1.form_type_id WHERE
	t1.form_category_id != 1 ORDER BY t1.form_order;
END //
DELIMITER ;

DROP PROCEDURE IF EXISTS sp_tbl_user_group_getusergroupdetails;
DELIMITER //
CREATE PROCEDURE `sp_tbl_user_group_getusergroupdetails`()
BEGIN
	SELECT t1.user_group_id, t1.user_group_name, t1.form_category_id,
	t1.form_ids, t1.is_active, (select count(*) from tbl_users u where user_group_id = u.user_group_id)as count
	FROM tbl_user_groups t1 ORDER BY t1.user_group_name;

END //
DELIMITER ;

DROP PROCEDURE IF EXISTS sp_tbl_form_category_get;
DELIMITER //

CREATE PROCEDURE `sp_tbl_form_category_get`()
BEGIN
	SELECT form_category_id, form_category FROM tbl_form_category WHERE form_category_id in (2, 3);
END //
DELIMITER ;
-- ---------------------------------------------------------------------------------
-- To get the list of groups with countries and number of legal entities
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_client_groups_list`;
DELIMITER //
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
END //
DELIMITER ;

-- --------------------------------------------------------------------------------
-- To Fetch Active Countries List
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_countries_for_user`;
DELIMITER //
CREATE PROCEDURE `sp_countries_for_user`(
    IN session_user INT(11)
)
BEGIN
    IF session_user > 0 THEN
		SELECT country_id, country_name, is_active
		FROM tbl_countries
		WHERE country_id in (
			SELECT country_id FROM tbl_user_countries
			WHERE user_id = session_user
		) ORDER BY country_name;
	ELSE
		SELECT country_id, country_name, is_active
		FROM tbl_countries ORDER BY country_name;
    END IF;
END //
DELIMITER ;
-- --------------------------------------------------------------------------------
-- To Fetch Active Domains List
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_domains_for_user`;
DELIMITER //
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
END //
DELIMITER ;

-- --------------------------------------------------------------------------------
-- To Fetch active industry list
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_industries_active_list`;
DELIMITER //
CREATE PROCEDURE `sp_industries_active_list`()
BEGIN
    SELECT industry_id, industry_name, is_active
    FROM tbl_industries
    WHERE is_active=1;
END //
DELIMITER ;


-- --------------------------------------------------------------------------------
-- To Fetch Business groups list
-- --------------------------------------------------------------------------------

DROP PROCEDURE IF EXISTS `sp_business_groups_list`;
DELIMITER //
CREATE PROCEDURE `sp_business_groups_list`(
    IN client_id INT(11)
)
BEGIN
    SELECT business_group_id, business_group_name, client_id
    FROM tbl_business_groups
    WHERE client_id=client_id;

END //
DELIMITER ;


-- --------------------------------------------------------------------------------
-- To get countries of techno users
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_user_countries_techno`;
DELIMITER //
CREATE PROCEDURE `sp_user_countries_techno`()
BEGIN
    SELECT t1.country_id, t1.user_id
    FROM tbl_user_countries t1
    INNER JOIN tbl_users t2 ON t2.user_id = t1.user_id
    INNER JOIN tbl_user_groups t3 ON
    t2.user_group_id = t3.user_group_id
    AND t3.form_category_id = 3;
END //
DELIMITER ;

-- --------------------------------------------------------------------------------
-- To get domains of techno users
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_user_domains_techno`;
DELIMITER //
CREATE PROCEDURE `sp_user_domains_techno`()
BEGIN
    SELECT t1.domain_id, t1.user_id FROM tbl_user_domains t1
    INNER JOIN tbl_users t2 ON t2.user_id = t1.user_id
    INNER JOIN tbl_user_groups t3 ON
    t2.user_group_id = t3.user_group_id AND t3.form_category_id = 3;
END //
DELIMITER ;

-- --------------------------------------------------------------------------------
-- To Save Client Details
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_client_group_save`;
DELIMITER //
CREATE PROCEDURE `sp_client_group_save`(
    IN groupname VARCHAR(50), email_id VARCHAR(100)
)
BEGIN
    INSERT INTO tbl_client_groups (group_name, group_admin)
    VALUES (groupname, email_id);
END //
DELIMITER ;

-- --------------------------------------------------------------------------------
-- To Save Business group
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_business_group_save`;
DELIMITER //
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
END //
DELIMITER ;

-- --------------------------------------------------------------------------------
-- Delete Client Countries
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_client_countries_delete`;
DELIMITER //
CREATE PROCEDURE `sp_client_countries_delete`(
    IN clientid INT(11)
)
BEGIN
    DELETE FROM tbl_client_countries WHERE client_id=clientid;
END //
DELIMITER ;

-- --------------------------------------------------------------------------------
-- Delete Client Domains
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_client_domains_delete`;
DELIMITER //
CREATE PROCEDURE `sp_client_domains_delete`(
    IN clientid INT(11)
)
BEGIN
    DELETE FROM tbl_client_domains WHERE client_id=clientid;
END //
DELIMITER ;

-- --------------------------------------------------------------------------------
-- Delete Incharge persons
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_user_clients_delete`;
DELIMITER //
CREATE PROCEDURE `sp_user_clients_delete`(
    IN clientid INT(11)
)
BEGIN
    DELETE FROM tbl_user_clients WHERE client_id=clientid;
END //
DELIMITER ;

-- --------------------------------------------------------------------------------
-- To delete organizations under client
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_le_domain_industry_delete`;
DELIMITER //

CREATE PROCEDURE `sp_le_domain_industry_delete`(
    IN clientid INT(11)
)
BEGIN
    DELETE FROM tbl_legal_entity_domain_industry
    WHERE client_id=clientid;
END //
DELIMITER ;

-- --------------------------------------------------------------------------------
-- To get ids of legal entities which were inserted
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_legal_entity_id_by_name`;
DELIMITER //

CREATE PROCEDURE `sp_legal_entity_id_by_name`(
    IN legal_entity_names TEXT
)
BEGIN
    SELECT legal_entity_id, legal_entity_name
    FROM tbl_legal_entities
    WHERE find_in_set(legal_entity_name, legal_entity_names);
END //
DELIMITER ;

-- --------------------------------------------------------------------------------
-- To delete client configurations of Client
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_client_configurations_delete`;
DELIMITER //
CREATE PROCEDURE `sp_client_configurations_delete`(
    IN clientid INT(11)
)
BEGIN
    DELETE FROM tbl_client_configurations WHERE client_id=clientid;
END //
DELIMITER ;

-- --------------------------------------------------------------------------------
-- To Save Client admin user
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_client_user_save_admin`;
DELIMITER //
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
END //
DELIMITER ;


-- --------------------------------------------------------------------------------
-- To Check for duplicate group name
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_client_group_is_duplicate_groupname`;
DELIMITER //
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
END //
DELIMITER ;


-- --------------------------------------------------------------------------------
-- To Check for dupliacte business group name
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_businessgroup_is_duplicate_businessgroupname`;
DELIMITER //
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
END //
DELIMITER ;


-- --------------------------------------------------------------------------------
-- To Check for dupliacte Legal entity name
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_legalentity_is_duplicate_legalentityname`;
DELIMITER //
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
END //
DELIMITER ;

-- --------------------------------------------------------------------------------
-- To Get Group name and admin email id by id
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_client_groups_details_by_id`;
DELIMITER //
CREATE PROCEDURE `sp_client_groups_details_by_id`(
    IN clientid INT(11)
)
BEGIN
    SELECT group_name, group_admin FROM tbl_client_groups
    WHERE client_id=clientid;
END //
DELIMITER ;

-- --------------------------------------------------------------------------------
-- To get Legal entity details by group id
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_legal_entity_details_by_group_id`;
DELIMITER //
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
END //
DELIMITER ;

-- --------------------------------------------------------------------------------
-- To get domains of client by legal entity
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_client_domains_by_group_id`;
DELIMITER //
CREATE PROCEDURE `sp_client_domains_by_group_id`(
    IN clientid INT(11)
)
BEGIN
    SELECT client_id, legal_entity_id, domain_id
    FROM tbl_client_domains WHERE client_id = clientid;
END //
DELIMITER ;

-- --------------------------------------------------------------------------------
-- To get incharge persons by group id
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_user_clients_by_group_id`;
DELIMITER //
CREATE PROCEDURE `sp_user_clients_by_group_id`(
    IN clientid INT(11)
)
BEGIN
    SELECT client_id, legal_entity_id, user_id
    FROM tbl_user_clients WHERE client_id = clientid;
END //
DELIMITER ;

-- --------------------------------------------------------------------------------
-- to get configurations of Client by group id
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_client_configuration_by_group_id`;
DELIMITER //
CREATE PROCEDURE `sp_client_configuration_by_group_id`(
    IN clientid INT(11)
)
BEGIN
    SELECT country_id, domain_id, period_from, period_to
    FROM tbl_client_configurations WHERE client_id = clientid;
END //
DELIMITER ;

-- --------------------------------------------------------------------------------
-- Get Organizations of Client
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_le_d_industry_by_group_id`;
DELIMITER //
CREATE PROCEDURE `sp_le_d_industry_by_group_id`(
    IN clientid INT(11)
)
BEGIN
    SELECT legal_entity_id, domain_id, industry_id, no_of_units
    FROM tbl_legal_entity_domain_industry WHERE client_id = clientid;
END //
DELIMITER ;

-- --------------------------------------------------------------------------------
-- To check whether the given client id is valid or not
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_client_groups_is_valid_group_id`;
DELIMITER //
CREATE PROCEDURE `sp_client_groups_is_valid_group_id`(
    IN clientid INT(11)
)
BEGIN
    SELECT count(client_id) as count FROM tbl_client_groups
    WHERE client_id=clientid;
END //
DELIMITER ;

-- --------------------------------------------------------------------------------
-- To get countries of a Client
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_client_countries_by_group_id`;
DELIMITER //
CREATE PROCEDURE `sp_client_countries_by_group_id`(
    IN group_id INT(11)
)
BEGIN
    SELECT country_id FROM tbl_client_countries
    WHERE client_id = group_id;
END //
DELIMITER ;

-- --------------------------------------------------------------------------------
-- To get number of client users
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_client_users_count`;
DELIMITER //
CREATE PROCEDURE `sp_client_users_count`(
    IN group_id INT(11), entity_id INT(11)
)
BEGIN
    SELECT count(user_id)+1 as count FROM tbl_client_users
    WHERE client_id = group_id and
    legal_entity_id = entity_id;
END //
DELIMITER ;


-- --------------------------------------------------------------------------------
-- To get the used space of a legal entity
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_legal_entities_space_used`;
DELIMITER //
CREATE PROCEDURE `sp_legal_entities_space_used`(
    IN le_id INT(11)
)
BEGIN
    SELECT used_space FROM tbl_legal_entities
    WHERE legal_entity_id=le_id;
END //
DELIMITER ;


-- --------------------------------------------------------------------------------
-- To Update Client Group
-- --------------------------------------------------------------------------------

DROP PROCEDURE IF EXISTS `sp_client_group_update`;
DELIMITER //
CREATE PROCEDURE `sp_client_group_update` (
    IN groupname VARCHAR(50), groupid INT(11)
)
BEGIN
    UPDATE tbl_client_groups set group_name=groupname
    WHERE client_id=groupid;

END //
DELIMITER ;


-- --------------------------------------------------------------------------------
-- To Change the status of client
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_client_groups_change_status`;
DELIMITER //
CREATE PROCEDURE `sp_client_groups_change_status`(
    IN clientid INT(11), isactive bool
)
BEGIN
    UPDATE tbl_legal_entities set is_active = isactive
    WHERE client_id=clientid;
    SELECT group_name FROM tbl_client_groups
    WHERE client_id=clientid;
END //
DELIMITER ;


-- --------------------------------------------------------------------------------
-- To Notify the incharge person, that the legal entity is assigned to him
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_notifications_notify_incharge`;
DELIMITER //
CREATE PROCEDURE `sp_notifications_notify_incharge`(
    IN notification TEXT, url TEXT
)
BEGIN
    INSERT INTO tbl_notifications
    (notification_text, link, created_on) VALUES
    (notification, url, now());
END //
DELIMITER ;

-- --------------------------------------------------------------------------------
-- To get the group of companies under user - client unit
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_tbl_unit_getuserclients`;
DELIMITER //
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_tbl_unit_getuserclients`(in userId INT(11))
BEGIN
	select client_id, group_name from tbl_client_groups
    where client_id in
	(select t1.client_id from tbl_client_groups t1
    inner join tbl_user_clients t2 on t1.client_id = t2.client_id
	and t2.user_id = userId);
END //
DELIMITER ;


-- --------------------------------------------------------------------------------
-- To get the group of units count - client unit
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_tbl_unit_getunitcount`;
DELIMITER //
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_tbl_unit_getunitcount`(in clientId INT(11))
BEGIN
	select count(*) as units from tbl_units
    where client_id = clientId;
END //
DELIMITER ;

-- --------------------------------------------------------------------------------
-- To generate unit codes - client unit
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_tbl_unit_getunitcode`;
DELIMITER //
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_tbl_unit_getunitcode`(in unit_code_start_letter varchar(50),
			clientId INT(11))
BEGIN
	SELECT TRIM(LEADING unit_code_start_letter FROM unit_code) as code
	FROM tbl_units WHERE unit_code like binary 'unit_code_start_letter%' and
	CHAR_LENGTH(unit_code) = 7 and client_id=clientId;
END //
DELIMITER ;

-- --------------------------------------------------------------------------------
-- To get business group details of all clients under userid - client unit
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_tbl_unit_getclientbusinessgroup`;
DELIMITER //
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_tbl_unit_getclientbusinessgroup`(in userId INT(11))
BEGIN
	select business_group_id, business_group_name, client_id from tbl_business_groups
    where client_id in
	(select t1.client_id from tbl_client_groups t1
    inner join tbl_user_clients t2 on t1.client_id = t2.client_id
	and t2.user_id = userId) order by business_group_name ASC;
END //
DELIMITER ;


-- --------------------------------------------------------------------------------
-- To get legal entity details of all clients under userid - client unit
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_tbl_unit_getclientlegalentity`;
DELIMITER //
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_tbl_unit_getclientlegalentity`(in userId INT(11))
BEGIN
	select legal_entity_id, legal_entity_name, business_group_id, client_id from tbl_legal_entities
    where client_id in
	(select t1.client_id from tbl_client_groups t1
    inner join tbl_user_clients t2 on t1.client_id = t2.client_id
	and t2.user_id = userId) order by legal_entity_name ASC;
END //
DELIMITER ;

-- --------------------------------------------------------------------------------
-- To get division details of all clients under userid - client unit
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_tbl_unit_getclientdivision`;
DELIMITER //
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_tbl_unit_getclientdivision`(in userId INT(11))
BEGIN
	select division_id, division_name, legal_entity_id, business_group_id, client_id from tbl_divisions
    where client_id in
	(select t1.client_id from tbl_client_groups t1
    inner join tbl_user_clients t2 on t1.client_id = t2.client_id
	and t2.user_id = userId) order by division_name ASC;
END //
DELIMITER ;

-- --------------------------------------------------------------------------------
-- To get UNIT details of all clients under userid - client unit
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_tbl_unit_getunitdetailsforuser`;
DELIMITER //
CREATE PROCEDURE `sp_tbl_unit_getunitdetailsforuser`(in userId INT(11))
BEGIN
	select t1.unit_id, t1.client_id, t1.business_group_id,
    t1.legal_entity_id, t1.division_id,
	t1.geography_id, t1.unit_code,t1.country_id,
	t1.unit_name, t1.address, t1.postal_code,
	t1.approve_status, t1.is_active,
	t4.category_name,
	t6.domain_id as domain_ids, t6.industry_id as i_ids,
	(select business_group_name from tbl_business_groups where
    business_group_id = t1.business_group_id) as b_group,
    (select legal_entity_name from tbl_legal_entities where
    legal_entity_id = t1.legal_entity_id) as l_entity,
    (select division_name from tbl_divisions where
    division_id = t1.division_id) as division,
    (select group_name from tbl_client_groups where
    client_id = t1.client_id) as group_name
    from
    tbl_units as t1, tbl_user_clients as t2, tbl_user_countries as t3,
	tbl_category_master as t4,
	tbl_user_domains as t5, tbl_unit_industries as t6
    where
	t6.domain_id = t5.domain_id and
	t5.user_id = t2.user_id and
	t4.category_id = t1.category_id and
	t4.client_id = t1.client_id and
	t1.country_id = t3.country_id and
    t3.user_id = t2.user_id and
	t1.client_id = t2.client_id and
    t2.user_id = userId
	group by t1.unit_id
    order by group_name, b_group, l_entity, division;
END //
DELIMITER ;

-- --------------------------------------------------------------------------------
-- To get geography level details of all clients under userid - client unit
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_geography_levels_getlevelsforusers`;
DELIMITER //
CREATE PROCEDURE `sp_geography_levels_getlevelsforusers`(in userId INT(11))
BEGIN
	select level_id, country_id, level_position, level_name
    from tbl_geography_levels
    where country_id in (select country_id from tbl_user_countries
    where user_id = userId) order by level_position;
END //
DELIMITER ;

-- --------------------------------------------------------------------------------
-- To get geography user mapping of all clients under userid - client unit
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_get_geographies_for_users_mapping`;
DELIMITER //
CREATE PROCEDURE `sp_get_geographies_for_users_mapping`(in userId INT(11))
BEGIN
	select t1.geography_id, t1.geography_name, t1.parent_names,
    t1.level_id,t1.parent_ids, t1.is_active, t2.country_id, t3.country_name
    from
    tbl_geographies as t1, tbl_geography_levels as t2,
    tbl_countries as t3
    where
    t1.level_id = t2.level_id and t2.country_id = t3.country_id
    and t2.country_id in (select country_id from tbl_user_countries
    where user_id  = userId);
END //
DELIMITER ;


-- --------------------------------------------------------------------------------
-- To get client domains of all clients under userid - client unit
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_tbl_unit_getclientdomains`;
DELIMITER //
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_tbl_unit_getclientdomains`(in userId INT(11),
	user_res int(11))
BEGIN
	if(user_res > 0)then
		select domain_id, domain_name, is_active from tbl_domains
		where domain_id in (select domain_id from tbl_client_domains
		where client_id in (select client_id from tbl_user_clients
		where user_id = userId)) and is_active =1
		order by domain_name ASC;
	else
		SELECT domain_id, domain_name, is_active FROM tbl_domains
		where domain_id in (select domain_id from tbl_user_domains
		WHERE user_id = userid) and is_active =1 order by domain_name asc;
	end if;
END
DELIMITER ;

-- --------------------------------------------------------------------------------
-- To get the list of techno users
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_users_techno`;
DELIMITER //
CREATE PROCEDURE `sp_users_techno`()
BEGIN
	SELECT user_id, concat(employee_code,'-',employee_name) as e_name,
	is_active FROM tbl_users
	WHERE user_group_id in (
		select user_group_id from tbl_user_groups
		where form_category_id = 3
	);
END //
DELIMITER ;

-- --------------------------------------------------------------------------------
-- To get list of units for approval
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_units_approval_list`;
DELIMITER //
CREATE PROCEDURE `sp_units_approval_list`()
BEGIN
	SELECT legal_entity_id, legal_entity_name,
	(
		SELECT country_name FROM tbl_countries tc
		WHERE tc.country_id = tle.country_id
	) as country_name,
	(
		SELECT business_group_name FROM tbl_business_groups tbg
		WHERE tbg.business_group_id = tle.business_group_id
	) as business_group_name,
	(
		SELECT group_name FROM tbl_client_groups tcg
		WHERE tcg.client_id = tle.client_id
	) as group_name,
	(
		SELECT count(unit_id) FROM tbl_units tu
		WHERE is_active=1 and tu.legal_entity_id=tle.legal_entity_id
		and approve_status=0
	) as unit_count FROM tbl_legal_entities tle;
END //
DELIMITER ;
-- --------------------------------------------------------------------------------
--  Get list of Units to be approved by legal entity id
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_units_approval_list_by_entity_id`;
DELIMITER //
CREATE PROCEDURE `sp_units_approval_list_by_entity_id`(
	IN le_id INT(11)
)
BEGIN
	SELECT
	(
		SELECT division_name FROM tbl_divisions td
		WHERE td.division_id = tu.division_id
	) as division_name,
	(
		SELECT category_name FROM tbl_category_master tcm
		WHERE tcm.category_id = tu.category_id
	) as category_name,
	unit_id, unit_code, unit_name, address, postal_code,
	(
		SELECT geography_name FROM tbl_geographies tg
		WHERE tg.geography_id=tu.geography_id
	) as geography_name
	FROM tbl_units tu
	WHERE is_active=1 and approve_status=0
	and legal_entity_id=le_id;

	SELECT unit_id, (
		SELECT domain_name FROM tbl_domains td
		WHERE td.domain_id=tui.domain_id
	) as domain_name, (
		SELECT industry_name FROM tbl_industries ti
		WHERE ti.industry_id=tui.industry_id
	) as industry_name
	FROM tbl_unit_industries tui WHERE unit_id in (
		SELECT unit_id FROM tbl_units
		WHERE legal_entity_id=le_id
	);
END //
DELIMITER ;

-- --------------------------------------------------------------------------------
-- To Save activities
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_activity_log_save`;
DELIMITER //
CREATE PROCEDURE `sp_activity_log_save`(
	IN userid INT(11), formid INT(11), action_performed TEXT,
	action_performed_on TIMESTAMP
)
BEGIN
	INSERT INTO tbl_activity_log (user_id, form_id, action, created_on)
	VALUES (userid, formid, action_performed, action_performed_on);
END //
DELIMITER ;


-- --------------------------------------------------------------------------------
-- Note: comments before and after the routine body will not be stored by the server
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_client_groups_approval_list`;
DELIMITER //
CREATE PROCEDURE `sp_client_groups_approval_list`(
	IN session_user INT(11)
)
BEGIN
	SELECT client_id, group_name, group_admin, count, client_countries
	FROM (
		SELECT client_id, group_name, group_admin,
		(
			SELECT count(legal_entity_id) FROM tbl_legal_entities tle
			WHERE tle.client_id = tcg.client_id and is_active=1
		) as count,
		(
			select group_concat(country_id) from tbl_countries
			where country_id in (
				select country_id from tbl_client_countries
				where client_id=client_id
			)
		) as client_countries
		FROM tbl_client_groups tcg
		WHERE approve_status != 1
	) a WHERE count > 0;
END //
DELIMITER ;

-- --------------------------------------------------------------------------------
-- To check whether the country name already exissts or not
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_countries_is_dupliacte`;
DELIMITER //
CREATE PROCEDURE `sp_countries_is_dupliacte`(
	IN countryname VARCHAR(50), countryid INT(11)
)
BEGIN
	IF countryid IS NULL THEN
        SELECT count(country_id) as count FROM tbl_countries
        WHERE country_name=countryname;
    ELSE
        SELECT count(country_id) as count FROM tbl_countries
        WHERE country_name=countryname and country_id != countryid;
    END IF;
END //
DELIMITER ;

-- --------------------------------------------------------------------------------
-- To Save / Update Country
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_countries_save`;
DELIMITER //
CREATE PROCEDURE `sp_countries_save`(
	IN countryid INT(11), countryname VARCHAR(50),
	session_user INT(11), updated_time TIMESTAMP
)
BEGIN
	IF countryid IS NULL THEN
		INSERT INTO tbl_countries
		(country_id, country_name, is_active, created_by,
		created_on, updated_by, updated_on)
		VALUES (countryid, countryname, 1, session_user, updated_time,
		session_user, updated_time);
	ELSE
		UPDATE tbl_countries SET country_name = countryname,
		updated_by = session_user, updated_on = updated_time
		WHERE country_id=countryid;
	END IF;
END //
DELIMITER ;

-- --------------------------------------------------------------------------------
-- To Get the country name by it's id
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_countries_by_id`;
DELIMITER //
CREATE PROCEDURE `sp_countries_by_id`(
	IN countryid INT(11)
)
BEGIN
	SELECT country_name FROM tbl_countries
	WHERE country_id = countryid;
END //
DELIMITER ;

-- --------------------------------------------------------------------------------
-- To check whether transaction exists for a country before changing it's status
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_countries_is_transaction_exists`;
DELIMITER //
CREATE PROCEDURE `sp_countries_is_transaction_exists`(
	IN countryid INT(11)
)
BEGIN
	SELECT count(*) as count
	FROM tbl_statutory_mappings
	WHERE country_id = countryid;

	SELECT count(*) as count
	FROM tbl_client_countries
	WHERE country_id = countryid;
END //
DELIMITER ;

-- --------------------------------------------------------------------------------
-- To change the status of country
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_countries_change_status`;
DELIMITER //
CREATE PROCEDURE `sp_countries_change_status`(
	IN countryid INT(11), isactive TINYINT(2),
	session_user INT(11), updated_time TIMESTAMP
)
BEGIN
	UPDATE tbl_countries set is_active = isactive,
	updated_by = session_user, updated_on = updated_time
	WHERE country_id=countryid;
END //
DELIMITER ;

-- --------------------------------------------------------------------------------
-- To save/ update domain
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_domains_save`;
DELIMITER //
CREATE PROCEDURE `sp_domains_save`(
	IN domainid INT(11), domainname  VARCHAR(50),
	session_user INT(11), updatedon TIMESTAMP
)
BEGIN
	IF domainid IS NULL THEN
		INSERT INTO tbl_domains (
		domain_name, is_active, created_on,
		created_by, updated_on, updated_by) VALUES (
		domainname, 1, updatedon, session_user,
		updatedon, session_user);
	ELSE
		UPDATE tbl_domains SET domain_name=domainname,
		updated_on = updatedon, updated_by = session_user
		WHERE domain_id=domainid;
	END IF;
END //
DELIMITER ;

-- --------------------------------------------------------------------------------
-- To check whether the domain name already exists or not
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_domains_is_duplicate`;
DELIMITER //
CREATE PROCEDURE `sp_domains_is_duplicate`(
	IN domainname VARCHAR(50), domainid INT(11)
)
BEGIN
	IF domainid IS NULL THEN
        SELECT count(domain_id) as count FROM tbl_domains
        WHERE domain_name=domainname;
    ELSE
        SELECT count(domain_id) as count FROM tbl_domains
        WHERE domain_name=domainname and domain_id != domainid;
    END IF;
END //
DELIMITER ;

-- --------------------------------------------------------------------------------
-- To get domain name by it's id
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_domains_by_id`;
DELIMITER //
CREATE PROCEDURE `sp_domains_by_id`(
	IN domainid INT(11)
)
BEGIN
	SELECT domain_name FROM tbl_domains
	WHERE domain_id = domainid;
END //
DELIMITER ;

-- --------------------------------------------------------------------------------
-- To Check whether transaction exists for domain or not
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_domains_is_transaction_exists`;
DELIMITER //
CREATE PROCEDURE `sp_domains_is_transaction_exists`(
	IN domainid INT(11)
)
BEGIN
	SELECT count(*) AS count
	FROM tbl_statutory_mappings
	WHERE domain_id = domainid;

	SELECT count(*) AS count
	FROM tbl_client_domains
	WHERE domain_id = domainid;
END //
DELIMITER ;

-- --------------------------------------------------------------------------------
-- To change the status of domain
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_domains_change_status`;
DELIMITER //
CREATE PROCEDURE `sp_domains_change_status`(
	IN domainid INT(11), isactive TINYINT(2),
	session_user INT(11), updated_time TIMESTAMP
)
BEGIN
	UPDATE tbl_domains set is_active = isactive,
	updated_by = session_user, updated_on = updated_time
	WHERE domain_id=domainid;
END //
DELIMITER ;

-- --------------------------------------------------------------------------------
-- to get list of forms for User Group creation
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_forms_list`;
DELIMITER //
CREATE PROCEDURE `sp_forms_list`()
BEGIN
	SELECT tf.form_id, tf.form_category_id, tfc.form_category,
	tf.form_type_id, tft.form_type, tf.form_name, tf.form_url,
	tf.form_order, tf.parent_menu FROM tbl_forms tf LEFT JOIN
	tbl_form_category tfc ON (tf.form_category_id = tfc.form_category_id)
	LEFT JOIN tbl_form_type tft ON (tf.form_type_id = tft.form_type_id)
	WHERE tf.form_category_id in (3,4,7,8) order by tf.form_order;
END //
DELIMITER ;

-- --------------------------------------------------------------------------------
-- To get Knowledge and Techno form categories
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_formcategory_list`;
DELIMITER //
CREATE PROCEDURE `sp_formcategory_list` ()
BEGIN
	SELECT form_category_id, form_category
	FROM tbl_form_category
	WHERE form_category_id in (3,4,7,8);
END //
DELIMITER ;

-- --------------------------------------------------------------------------------
-- To get Detailed list of user group
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_usergroup_detailed_list`;
DELIMITER //
CREATE PROCEDURE `sp_usergroup_detailed_list` ()
BEGIN
	SELECT ug.user_group_id, user_group_name, form_category_id,
	form_ids, is_active, (SELECT count(user_id) FROM tbl_users u WHERE
	ug.user_group_id = u.user_group_id) AS count
	FROM tbl_user_groups ug ORDER BY user_group_name;
END //
DELIMITER ;

-- --------------------------------------------------------------------------------
-- To check whether the user group name already exists or not
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_usergroup_is_duplicate`;
DELIMITER //
CREATE PROCEDURE `sp_usergroup_is_duplicate`(
	IN ug_id INT(11), ug_name VARCHAR(50)
)
BEGIN
	IF ug_id IS NULL THEN
        SELECT count(user_group_id) as count FROM tbl_user_groups
        WHERE user_group_name=ug_name;
    ELSE
        SELECT count(user_group_id) as count FROM tbl_user_groups
        WHERE user_group_name=ug_name and user_group_id != ug_id;
    END IF;
END //
DELIMITER ;

-- --------------------------------------------------------------------------------
-- To Check whethere user exists under user group or not
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_usergroup_is_transaction_exists`;
DELIMITER //
CREATE PROCEDURE `sp_usergroup_is_transaction_exists`(
	IN ug_id INT(11)
)
BEGIN
	SELECT count(0) as count FROM tbl_users
	WHERE user_group_id = ug_id and is_active = 1;
END //
DELIMITER ;

-- --------------------------------------------------------------------------------
-- To Save / Update User Group
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_usergroup_save`;
DELIMITER //
CREATE PROCEDURE `sp_usergroup_save`(
	IN ug_id INT(11), ug_name VARCHAR(50), frm_cat_id INT(11),
	frm_ids TEXT, session_user INT(11), updated_time TIMESTAMP
)
BEGIN
	IF ug_id IS NULL THEN
		INSERT INTO tbl_user_groups
		(form_category_id, user_group_name, is_active,
		form_ids, created_by, created_on, updated_by, updated_on)
		VALUES (frm_cat_id, ug_name, 1, frm_ids, session_user,
		updated_time, session_user, updated_time);
	ELSE
		UPDATE tbl_user_groups SET form_category_id = frm_cat_id,
		user_group_name = ug_name, form_ids= frm_ids,
		updated_by = session_user, updated_on = updated_time
		WHERE user_group_id=ug_id;
	END IF;
END //
DELIMITER ;

-- --------------------------------------------------------------------------------
-- To Change the status of User group
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_usergroup_change_status`;
DELIMITER //
CREATE PROCEDURE `sp_usergroup_change_status`(
	IN ug_id INT(11), isactive TINYINT(2),
	session_user INT(11), updated_time TIMESTAMP
)
BEGIN
	UPDATE tbl_user_groups set is_active = isactive,
	updated_by = session_user, updated_on = updated_time
	WHERE user_group_id=ug_id;
END //
DELIMITER ;

-- --------------------------------------------------------------------------------
-- To get user group name by id
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_usergroup_by_id`;
DELIMITER //
CREATE PROCEDURE `sp_usergroup_by_id`(
	IN ug_id INT(11)
)
BEGIN
	SELECT user_group_name FROM tbl_user_groups
	WHERE user_group_id = ug_id;
END //
DELIMITER ;

-- --------------------------------------------------------------------------------
-- To Get countries configured  for a user
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_usercountries_by_userid`;
DELIMITER //
CREATE PROCEDURE `sp_usercountries_by_userid`(
	IN userid INT(11)
)
BEGIN
	SELECT country_id from tbl_user_countries
	WHERE user_id=userid;
END //
DELIMITER ;

-- --------------------------------------------------------------------------------
-- To get domains configured for a user
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_userdomains_by_userid`;
DELIMITER //
CREATE PROCEDURE `sp_userdomains_by_userid`(
	IN userid INT(11)
)
BEGIN
	SELECT domain_id FROM tbl_user_domains
	WHERE user_id = userid;
END //
DELIMITER ;


-- --------------------------------------------------------------------------------
-- To get only id, name and status of User group
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_usergroup_list`;
DELIMITER //
CREATE PROCEDURE `sp_usergroup_list`()
BEGIN
	SELECT user_group_id, user_group_name, is_active
	FROM tbl_user_groups ORDER BY user_group_name;
END //
DELIMITER ;

-- --------------------------------------------------------------------------------
-- To get All User Details
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_user_detailed_list`;
DELIMITER //
CREATE PROCEDURE `sp_user_detailed_list`()
BEGIN
	SELECT user_id, email_id, user_group_id, employee_name,
	employee_code, contact_no, address, designation, is_active
	FROM tbl_users
	ORDER BY employee_name;
END //
DELIMITER ;

-- --------------------------------------------------------------------------------
-- To check whether the email id already exists or not
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_user_is_duplicate_email`;
DELIMITER //
CREATE PROCEDURE `sp_user_is_duplicate_email`(
	IN emailid VARCHAR(100), userid INT(11)
)
BEGIN
	IF userid IS NULL THEN
        SELECT count(user_id) as count FROM tbl_users
        WHERE email_id=emailid;
    ELSE
        SELECT count(user_id) as count FROM tbl_users
        WHERE email_id=emailid and user_id != userid;
    END IF;
END //
DELIMITER;

-- --------------------------------------------------------------------------------
-- To check whether the employee code already exists or not
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_user_is_duplicate_employeecode`;
DELIMITER //
CREATE PROCEDURE `sp_user_is_duplicate_employeecode`(
	IN empcode VARCHAR(20), userid INT(11)
)
BEGIN
	IF userid IS NULL THEN
        SELECT count(user_id) as count FROM tbl_users
        WHERE employee_code=empcode;
    ELSE
        SELECT count(user_id) as count FROM tbl_users
        WHERE employee_code=empcode and user_id != userid;
    END IF;
END //
DELIMITER;

-- --------------------------------------------------------------------------------
-- To save / update user
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_users_save`;
DELIMITER //
CREATE PROCEDURE `sp_users_save`(
	IN userid INT(11), emailid VARCHAR(100), ug_id INT(11),
	pwd VARCHAR(50), emp_name VARCHAR(50), emp_code VARCHAR(20),
	contactno VARCHAR(12), addr TEXT, desig VARCHAR(50),
	session_user INT(11), created_time TIMESTAMP
)
BEGIN
	IF userid IS NULL THEN
		INSERT INTO tbl_users (
			email_id, user_group_id, password, employee_name, employee_code, contact_no,
			address, designation, is_active, created_by, created_on,
			updated_by, updated_on
		)	VALUES (
			emailid, ug_id, pwd, emp_name, emp_code, contactno, addr, desig,
			1, session_user, created_time, session_user, created_time
		);
	ELSE
		UPDATE tbl_users SET employee_name=emp_name, user_group_id=ug_id,
		employee_code=emp_code, contact_no=contactno, address=addr,
		designation = desig, updated_by=session_user,
		updated_on = created_time WHERE user_id=userid;
	END IF;
END //
DELIMITER;

-- --------------------------------------------------------------------------------
-- To Check the status of user group of the user
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_user_usergroup_status`;
DELIMITER //
CREATE PROCEDURE `sp_user_usergroup_status`(
	IN userid INT(11)
)
BEGIN
	select count(ug.user_group_id) from tbl_user_groups ug
	inner join tbl_users u on  ug.user_group_id = u.user_group_id
	where u.user_id = userid and ug.is_active = 1;
END //
DELIMITER;

-- --------------------------------------------------------------------------------
-- To update the status of user
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_users_change_status`;
DELIMITER //
CREATE PROCEDURE `sp_users_change_status`(
	IN userid INT(11), isactive TINYINT(4), session_user INT(11),
	updated_time TIMESTAMP
)
BEGIN
	UPDATE tbl_users set is_active = isactive,
	updated_by =  session_user and updated_on = updated_time
	WHERE user_id = userid;
END //
DELIMITER;

-- --------------------------------------------------------------------------------
-- To Get the name of employee by id
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_users_change_status`;
DELIMITER //
CREATE PROCEDURE `sp_empname_by_id`(
	IN userid INT(11)
)
BEGIN
	SELECT concat(employee_code, " - ", employee_name) as empname
	FROM tbl_users
	WHERE user_id = userid;
END //
DELIMITER;

-- --------------------------------------------------------------------------------
-- To Delete user countries
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_usercountries_delete`;
DELIMITER //
CREATE PROCEDURE `sp_usercountries_delete`(
	IN userid INT(11)
)
BEGIN
	DELETE FROM tbl_user_countries WHERE user_id=userid;
END //
DELIMITER;

-- --------------------------------------------------------------------------------
-- To Delete user domains
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_userdomains_delete`;
DELIMITER //
CREATE PROCEDURE `sp_userdomains_delete`(
	IN userid INT(11)
)
BEGIN
	DELETE FROM tbl_user_domains WHERE user_id=userid;
END //
DELIMITER;

-- --------------------------------------------------------------------------------
-- To get list of countries under client master group
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_countries_for_unit`;
DELIMITER //
CREATE PROCEDURE `sp_countries_for_unit`(IN session_user INT(11))
BEGIN
	IF session_user > 0 THEN
		SELECT country_id, country_name, is_active FROM tbl_countries
		WHERE country_id in (
			SELECT country_id FROM tbl_client_countries
			where client_id in (
				select user_id from tbl_user_countries
				WHERE user_id = session_user))
					ORDER BY country_name;
	ELSE
		SELECT country_id, country_name, is_active
		FROM tbl_countries ORDER BY country_name;
    END IF;
END//
DELIMITER;

-- --------------------------------------------------------------------------------
-- To get list of industries for client id for client unit
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_tbl_units_getindustries_for_legalentity`;
DELIMITER //
CREATE PROCEDURE `sp_tbl_units_getindustries_for_legalentity`(IN session_user INT(11))
BEGIN
	IF session_user > 0 THEN
		select t3.industry_id, t3.industry_name, t3.country_id, t3.domain_id,
				t3.is_active, t2.client_id, t2.no_of_units, t2.legal_entity_id
			from tbl_client_users as t1, tbl_legal_entity_domain_industry as t2,
					tbl_industries as t3
			where
				t3.industry_id = t2.industry_id and
				t2.client_id = t1.client_id and
				t1.user_id = session_user
			order by industry_name;
	ELSE
		select t3.industry_id, t3.industry_name, t3.country_id, t3.domain_id,
				t3.is_active, t2.client_id, t2.no_of_units, t2.legal_entity_id
			from tbl_legal_entity_domain_industry as t2,
					tbl_industries as t3
			where
				t3.industry_id = t2.industry_id and
				t2.client_id in (select client_id from tbl_client_users)
			order by industry_name;
   END IF;
DELIMITER;

-- --------------------------------------------------------------------------------
-- To check dupliaction of unit code and unit name
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_tbl_units_checkduplication`;
DELIMITER //
CREATE PROCEDURE `sp_tbl_units_checkduplication`(in unitId int(11), unitCode varchar(50),
		unitName varchar(50), clientId int(11))
BEGIN
	if unitCode is not null then
		select count(*) as unit_code_cnt from
		tbl_units where
		unit_code = unitCode and
		client_id = clientId and
		unit_id != unitId;
	else
		select count(*) as unit_name_cnt from
		tbl_units where
		unit_name = unitName and
		client_id = clientId and
		unit_id != unitId;
	end if;
END
DELIMITER;

-- --------------------------------------------------------------------------------
-- Routine DDL
-- Note: comments before and after the routine body will not be stored by the server
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_tbl_units_check_unitId`;
DELIMITER //
CREATE PROCEDURE `sp_tbl_units_check_unitId`(in unitId int(11))
BEGIN
	select count(*) as unit_id_cnt from
	tbl_units where
	unit_id = unitId;
END
DELIMITER;

-- --------------------------------------------------------------------------------
-- check dupliaction of id for save units
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_tbl_units_check_unitgroupid`;
DELIMITER //
CREATE PROCEDURE `sp_tbl_units_check_unitgroupid`(
in tableName varchar(50), param int(11))
BEGIN
	if tableName = 'client_id' then
		select count(0) as client_cnt from
		tbl_client_groups where client_id = param;
	end if;
	if tableName = 'bg_id' then
		select count(0) as bg_cnt from
		tbl_business_groups where business_group_id = param;
	end if;
	if tableName = 'legal_entity_id' then
		select count(0) as le_cnt from
		tbl_legal_entities where legal_entity_id = param;
	end if;
	if tableName = 'division_id' then
		select count(0) as divi_cnt from
		tbl_divisions where division_id = param;
	end if;
END
DELIMITER;

-- --------------------------------------------------------------------------------
-- Get unit max id
-- -- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_tbl_units_max_unitid`;
DELIMITER //
CREATE PROCEDURE `sp_tbl_units_max_unitid`()
BEGIN
	select max(unit_id) as max_id from
	tbl_units;
END
DELIMITER;

-- --------------------------------------------------------------------------------
-- find dupliacte catofory name / division name for unit master
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_tbl_units_check_unitgroupname`;
DELIMITER //
CREATE PROCEDURE `sp_tbl_units_check_unitgroupname`(
in tableName varchar(50), param varchar(50))
BEGIN
	if tableName = 'catg_name' then
		select count(0) as catg_cnt from
		tbl_category_master where category_name = param;
	end if;
	if tableName = 'div_name' then
		select count(0) as div_name_cnt from
		tbl_divisions where division_name = param;
	end if;
END
DELIMITER;

-- --------------------------------------------------------------------------------
-- save new division from unit master form
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_tbl_units_save_division`;
DELIMITER //

CREATE PROCEDURE `sp_tbl_units_save_division`(
	in clientId int(11), bg_id int(11), le_id int(11),
	divisionName varchar(50), createdBy int(11),
	createdOn timestamp
	)
BEGIN
	insert into tbl_divisions
	(client_id, business_group_id, legal_entity_id, division_name,
	created_by, created_on)
	values
	(clientId, bg_id, le_id, divisionName, createdBy, createdOn);
END
DELIMITER;

-- --------------------------------------------------------------------------------
-- save new category added from unit master form
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_tbl_units_save_category`;
DELIMITER //

CREATE PROCEDURE `sp_tbl_units_save_category`(
	in clientId int(11), bg_id int(11), le_id int(11),
	div_id varchar(50), categoryName varchar(50), createdBy int(11),
	createdOn timestamp
	)
BEGIN
	insert into tbl_category_master
	(client_id, business_group_id, legal_entity_id, division_id,
	category_name, created_by, created_on)
	values
	(clientId, bg_id, le_id, div_id, categoryName, createdBy, createdOn);
END
DELIMITER;