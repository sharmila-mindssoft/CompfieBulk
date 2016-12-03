-- IST time function
DROP FUNCTION IF EXISTS `current_ist_datetime`;
DELIMITER //
CREATE FUNCTION `current_ist_datetime`() RETURNS datetime
BEGIN
    DECLARE current_ist_date datetime;
    SET current_ist_date = convert_tz(utc_timestamp(),'+00:00','+05:30') ;

RETURN current_ist_date;
END //

DELIMITER ;

-- verify login

DROP PROCEDURE IF EXISTS `sp_verify_login`;
DELIMITER //
CREATE PROCEDURE `sp_verify_login`(
    IN uname VARCHAR(100), IN pword VARCHAR(100)
)
BEGIN
    SELECT user_id, username from tbl_user_login_details where username = uname and is_active = 1;
    SELECT @_user_id := user_id as user_id, @_user_category_id := user_category_id as user_category_id
    FROM tbl_user_login_details WHERE username = uname AND PASSWORD = pword AND is_active = 1;

    if @_user_category_id = 1 THEN
        SELECT T1.form_id, (select form_type from tbl_form_type where form_type_id = T1.form_type_id) as form_type,
        T1.form_name, T1.form_url,
        T1.form_order, T1.parent_menu FROM tbl_forms as T1
        INNER JOIN tbl_form_category as T2 ON T2.form_id = T1.form_id
        WHERE T2.category_id_1 = 1 ;

    elseif @_user_category_id = 2 THEN
        SELECT T1.form_id, (select form_type from tbl_form_type where form_type_id = T1.form_type_id) as form_type,
        T1.form_name, T1.form_url,
        T1.form_order, T1.parent_menu FROM tbl_forms as T1
        INNER JOIN tbl_form_category as T2 ON T2.form_id = T1.form_id
        WHERE T2.category_id_2 = 1 ;

    elseif @_user_category_id > 2 then
        SELECT T1.user_id, T1.user_category_id, T1.employee_code, T1.employee_name,
        T1.email_id, T1.contact_no, T1.mobile_no,
        T1.address, T1.designation, @_user_group_id := T1.user_group_id as user_group_id,
        (select ld.username from tbl_user_login_details ld where ld.user_id = T1.user_id) as user_name,
        (select tg.user_group_name from tbl_user_groups tg where tg.user_group_id = T1.user_group_id) as user_group_name
        FROM tbl_users as T1 WHERE T1.user_id = @_user_id;

        SELECT T1.form_id, (select form_type from tbl_form_type where form_type_id = T1.form_type_id) as form_type,
        T1.form_name, T1.form_url, T1.form_order, T1.parent_menu
        FROM tbl_forms as T1
        WHERE T1.form_id IN (select form_id from tbl_user_group_forms where user_group_id = @_user_group_id)
        OR T1.form_id IN (45, 46)
        OR T1.form_id IN (
                select case
                when @_user_category_id=3 and category_id_3 = 1 then 47
                when @_user_category_id=4 and category_id_4 = 1 then 47
                when @_user_category_id=5 and category_id_5 = 1 then 47
                when @_user_category_id=6 and category_id_6 = 1 then 47
                end as form_notify
                from tbl_form_category
                where form_id = 47
        );

    end if;
END //

DELIMITER ;

DROP PROCEDURE IF EXISTS `sp_save_login_failure`;
DELIMITER //
CREATE PROCEDURE `sp_save_login_failure`(
    IN userid INT(11), userip varchar(50), logintime varchar(50)
)
BEGIN
    SELECT @cnt := count(user_id), @_attempt := login_attempt from tbl_user_login_history where user_id = userid;
    if @cnt = 0 THEN
        INSERT INTO tbl_user_login_history(user_id, ip, login_time, login_attempt) values
        (userid, userip, logintime, 1);
    else
        UPDATE tbl_user_login_history set login_attempt = @_attempt + 1,
        ip = userip, login_time = logintime where user_id = userid;
    end if;
    SELECT user_id, login_attempt, login_time from tbl_user_login_history where user_id = userid;

END //

DELIMITER ;




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

    select t1.domain_id, t2.country_id, t2.country_name, t2.is_active
    from tbl_statutory_levels as t1, tbl_countries as t2
    where
    t2.country_id = t1.country_id;
END //
DELIMITER ;

-- --------------------------------------------------------------------------------
-- Returns Validity date for all country domain combinations
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_validitydays_settings_list`;
DELIMITER //
CREATE PROCEDURE `sp_validitydays_settings_list`()
BEGIN
    SELECT validity_date_id, country_id, domain_id, days
    FROM tbl_validity_date_settings;
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
        INSERT INTO tbl_validity_date_settings
        (country_id, domain_id, days, created_by, created_on, updated_by, updated_on)
        VALUES
        (countryid, domainid, validitydays, createdby, createdon, updatedby, updatedon);
    ELSE
        Update tbl_validity_date_settings set days=validitydays,
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
        SELECT count(1) FROM tbl_organisation WHERE organisation_name = industryname;
    else
        SELECT count(1) FROM tbl_organisation WHERE organisation_name = industryname
        and organisation_id != industryid;
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
    SELECT organisation_name FROM tbl_organisation WHERE
    organisation_id = industryid;
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
        t1.organisation_id as industry_id, t1.organisation_name as industry_name,
        t1.is_active FROM tbl_organisation t1
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
    INSERT INTO tbl_organisation
    (organisation_name, country_id, domain_id, created_by, created_on)
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
    UPDATE tbl_organisation
    SET
    organisation_name = industryName,
    country_id = countryId,
    domain_id = domainId,
    updated_by = updatedBy
    WHERE
    organisation_id = industryId;
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
    UPDATE tbl_organisation
    SET
    is_active = isActive,
    updated_by = updatedBy
    WHERE
    organisation_id = industryId;
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
CREATE procedure `sp_tbl_domains_for_user`(
    IN u_id INT(11)
)
BEGIN
    SELECT @u_cat_id := user_category_id from tbl_user_login_details where user_id = u_id;
    IF @u_cat_id > 2 THEN
        SELECT DISTINCT t1.domain_id, t1.domain_name, t1.is_active
        FROM tbl_domains t1
        INNER JOIN tbl_user_domains t2 on t1.domain_id = t2.domain_id
        WHERE t2.user_id = u_id
        ORDER BY t1.domain_name;
    ELSE
        SELECT domain_id, domain_name, is_active FROM tbl_domains
        ORDER BY domain_name;
    END IF;

    select c.country_id, c.country_name, d.domain_id from tbl_countries c inner join
        tbl_domain_countries d on c.country_id = d.country_id;

END //
DELIMITER ;
-- --------------------------------------------------------------------------------
-- To Get admin forms
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS sp_tbl_forms_getadminforms;

DELIMITER //
CREATE procedure `sp_tbl_forms_getadminforms`(
    IN fc_id INT(11)
)
BEGIN
    SELECT T01.form_id, T01.form_name, T01.form_url, T01.form_order, T01.parent_menu,
    T02.form_category, T03.form_type FROM tbl_forms T01
    INNER JOIN tbl_form_category T02 ON T02.form_category_id = T01.form_category_id
    INNER JOIN tbl_form_type T03 ON T03.form_type_id = T01.form_type_id
    WHERE T01.form_category_id = fc_id ORDER BY T01.form_order;
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
	IN _country_id int(11), IN _category_id int(11),
	IN _from_limit INT, IN _to_limit INT
)
BEGIN
	SELECT t1.user_id, t1.form_id, t1.action, t1.created_on
	FROM tbl_activity_log as t1, tbl_users as t2, tbl_user_countries as t3
	WHERE
		date(t1.created_on) >= _from_date
		AND date(t1.created_on) <= _to_date
		AND t1.form_id LIKE _form_id
		AND t1.user_id LIKE t2.user_id
		AND t3.user_id = t2.user_id
		AND t2.user_id LIKE _user_id
		AND t2.user_category_id LIKE _category_id
		ORDER BY t1.user_id ASC, DATE(t1.created_on) DESC
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
    IN _user_id INT, admin_user_type INT
)
BEGIN
    if _user_id = 0 then
        if admin_user_type = 0 then
            SELECT form_id as form_id FROM tbl_forms WHERE form_category_id = 1;
        else
            SELECT form_id as form_id FROM tbl_forms WHERE form_category_id = 2;
        end if;
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
            select country_id from tbl_legal_entities
            where client_id=client_id
        )
    ) as country_names,
    (
        select count(legal_entity_id) from tbl_legal_entities tle
        WHERE tle.client_id=tcg.client_id
    ) as no_of_legal_entities,
    is_active, is_approved, remarks
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
    IF session_user > 2 THEN
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
    select distinct(t1.legal_entity_id), t2.domain_id,
    (select domain_name from tbl_domains where
    domain_id = t2.domain_id) as domain_name, t2.organisation_id as industry_id,
    (select organisation_name from tbl_organisation where
    organisation_id = t2.organisation_id ) as industry_name,
    t2.count as unit_count
    from
    tbl_user_legalentity as t1,
    tbl_legal_entity_domains as t2
    where
    t2.legal_entity_id = t1.legal_entity_id and
    t1.user_id = session_user;
END //
DELIMITER ;

-- --------------------------------------------------------------------------------
-- To Fetch active industry list
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_industries_active_list`;
DELIMITER //
CREATE PROCEDURE `sp_industries_active_list`()
BEGIN
    SELECT organisation_id, organisation_name, is_active
    FROM tbl_organisation
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
    IN groupname VARCHAR(50),
    emailid VARCHAR(100),
    shortname varchar(50),
    no_of_view_licence int(11),
    session_user int(11)
)
BEGIN
    INSERT INTO tbl_client_groups (
    group_name, short_name, email_id, total_view_licence,
    is_active, status_changed_on, is_approved, created_by,
    created_on) VALUES (groupname, shortname, emailid,
    no_of_view_licence, 1, current_ist_datetime(),
    0, session_user, current_ist_datetime());
END//
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
    DELETE FROM tbl_legal_entity_domains
    WHERE legal_entity_id in (
        select legal_entity_id from tbl_legal_entities
        where client_id = clientid
    );
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
-- To get ids of legal entities which were inserted
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_legal_entity_name_by_id`;
DELIMITER //

CREATE PROCEDURE `sp_legal_entity_name_by_id`(
    IN entity_id INT(11)
)
BEGIN
    SELECT legal_entity_name
    FROM tbl_legal_entities
    WHERE legal_entity_id=entity_id;
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
    DELETE FROM tbl_client_configuration WHERE client_id=clientid;
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
        client_id, user_id,  email_id, employee_name, created_on,
        is_primary_admin, is_active
    ) VALUES (
        clientid, 0, username, "Admin", current_time_stamp, 1, 1
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
    SELECT group_name, short_name, email_id, total_view_licence
    FROM tbl_client_groups WHERE client_id=clientid;
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
    file_space_limit, total_licence
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
    select t1.client_id, t1.legal_entity_id, t2.domain_id
    from
    tbl_user_legalentity as t1,
    tbl_legal_entity_domains as t2
    where
    t2.legal_entity_id = t1.legal_entity_id and
    t1.client_id = clientid and
    t1.user_id = userId
    group by t1.user_id;
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
    SELECT country_id, domain_id, month_from, month_to
    FROM tbl_client_configuration WHERE client_id = clientid;
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
    SELECT legal_entity_id, domain_id, organisation_id, count,
    activation_date
    FROM tbl_legal_entity_domains WHERE legal_entity_id in (
        select legal_entity_id from tbl_legal_entities
        where client_id = clientid
    );
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
    SELECT country_id FROM tbl_legal_entities
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
    (notification, url, current_ist_datetime());
END //
DELIMITER ;

-- --------------------------------------------------------------------------------
-- To get the group of companies under user - client unit
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_tbl_unit_getuserclients`;
DELIMITER //
CREATE PROCEDURE `sp_tbl_unit_getuserclients`(in userId INT(11))
BEGIN
    DECLARE user_category INT(11);
    SELECT user_category_id INTO user_category
    FROM tbl_user_login_details WHERE user_id = userid;
    IF user_category in (1,2) then
        select client_id, group_name, is_active from tbl_client_groups
        order by group_name ASC;
    ELSEIF user_category = 5 then
        select client_id, group_name, is_active from tbl_client_groups
        where client_id in(
            SELECT client_id FROM tbl_user_clients WHERE
            user_id = userid
        ) order by group_name ASC;
    ELSEIF user_category = 6 then
        select client_id, group_name, is_active from tbl_client_groups
        where client_id in(
            SELECT client_id FROM tbl_legal_entities
            WHERE legal_entity_id in (
                SELECT legal_entity_id FROM tbl_user_legalentity WHERE
                user_id = userid
            )
        ) order by group_name ASC;
    ELSE
        select client_id, group_name, is_active from tbl_client_groups
        where client_id in (
            SELECT client_id FROM tbl_units
            WHERE unit_id in (
                SELECT unit_id FROM tbl_user_units WHERE
                user_id = userid
            )
        ) order by group_name ASC;
    END IF;
END //
DELIMITER ;


-- --------------------------------------------------------------------------------
-- To get the group of units count - client unit
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_tbl_unit_getunitcount`;
DELIMITER //
CREATE PROCEDURE `sp_tbl_unit_getunitcount`(in clientId INT(11))
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
CREATE PROCEDURE `sp_tbl_unit_getunitcode`(in unit_code_start_letter varchar(50),
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
CREATE PROCEDURE `sp_tbl_unit_getclientbusinessgroup`(in userId INT(11))
BEGIN
    DECLARE user_category INT(11);
    SELECT user_category_id INTO user_category FROM tbl_users WHERE user_id = userid;
    IF user_category in (1,2) then
        select business_group_id, business_group_name, client_id
        from tbl_business_groups order by business_group_name ASC;
    ELSEIF user_category = 5 then
        select business_group_id, business_group_name, client_id
        from tbl_business_groups WHERE client_id in (
            SELECT client_id FROM tbl_user_clients WHERE user_id=userid
        ) order by business_group_name ASC;
    ELSEIF user_category = 6 then
        select business_group_id, business_group_name, client_id
        from tbl_business_groups WHERE business_group_id in (
            SELECT business_group_id FROM tbl_legal_entities
            WHERE legal_entity_id in (
                SELECT legal_entity_id from tbl_user_legalentity
                WHERE user_id = userId
            )
        ) order by business_group_name ASC;
    ELSE
        select business_group_id, business_group_name, client_id
        from tbl_business_groups WHERE business_group_id in (
            SELECT business_group_id FROM tbl_units
            WHERE unit_id in (
                SELECT unit_id FROM tbl_user_units
                WHERE user_id = userid
            )
        ) order by business_group_name ASC;
    END IF;
END //
DELIMITER ;


-- --------------------------------------------------------------------------------
-- To get legal entity details of all clients under userid - client unit
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_tbl_unit_getclientlegalentity`;
DELIMITER //
CREATE PROCEDURE `sp_tbl_unit_getclientlegalentity`(in userId INT(11))
BEGIN
    DECLARE user_category INT(11);
    SELECT user_category_id INTO user_category
    FROM tbl_users WHERE user_id = userid;
    IF user_category in (1,2) then
        select legal_entity_id, legal_entity_name, business_group_id,
        client_id, country_id from tbl_legal_entities
        order by legal_entity_name ASC;
    ELSEIF user_category = 5 THEN
        select legal_entity_id, legal_entity_name, business_group_id,
        client_id, country_id from tbl_legal_entities
        WHERE client_id in (
            SELECT client_id FROM tbl_user_clients WHERE user_id=userid
        ) order by legal_entity_name ASC;
    ELSEIF user_category = 6 then
        select legal_entity_id, legal_entity_name, business_group_id,
        client_id, country_id from tbl_legal_entities
        WHERE legal_entity_id in (
            SELECT legal_entity_id FROM tbl_user_legalentity
            WHERE user_id=userid
        ) order by legal_entity_name ASC;
    ELSE
        select legal_entity_id, legal_entity_name, business_group_id,
        client_id, country_id from tbl_legal_entities
        WHERE legal_entity_id in (
            SELECT legal_entity_id FROM tbl_units WHERE unit_id in(
                SELECT unit_id FROM tbl_user_units
                WHERE user_id=userid
            )
        ) order by legal_entity_name ASC;
    END IF;
END //
DELIMITER ;

-- --------------------------------------------------------------------------------
-- To get division details of all clients under userid - client unit
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_tbl_unit_getclientdivision`;
DELIMITER //
CREATE PROCEDURE `sp_tbl_unit_getclientdivision`(in userId INT(11))
BEGIN
    DECLARE user_category INT(11);
    SELECT user_category_id INTO user_category
    FROM tbl_users WHERE user_id = userid;
    IF user_category in (1,2) then
        select division_id, division_name, legal_entity_id,
        business_group_id, client_id from tbl_divisions
        order by division_name ASC;
    ELSEIF user_category = 5 then
        select division_id, division_name, legal_entity_id,
        business_group_id, client_id from tbl_divisions
        where client_id in(
            SELECT client_id FROM tbl_user_clients WHERE
            user_id = userid
        ) order by division_name ASC;
    ELSEIF user_category = 6 then
        select division_id, division_name, legal_entity_id,
        business_group_id, client_id from tbl_divisions
        where legal_entity_id in(
            SELECT legal_entity_id FROM tbl_user_legalentity WHERE
            user_id = userid
        ) order by division_name ASC;
    ELSE
        select division_id, division_name, legal_entity_id,
        business_group_id, client_id from tbl_divisions
        where legal_entity_id in(
            SELECT division_id FROM tbl_units WHERE
            unit_id in (
                SELECT unit_id from tbl_user_units
                WHERE user_id = userid
            )
        ) order by division_name ASC;
    END IF;
END //
DELIMITER ;

-- --------------------------------------------------------------------------------
-- To get UNIT details of all clients under userid - client unit
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_tbl_unit_getunitdetailsforuser`;
DELIMITER //
CREATE PROCEDURE `sp_tbl_unit_getunitdetailsforuser`(in userId INT(11))
BEGIN
    select t2.unit_id, t2.client_id, t2.business_group_id,
    t2.legal_entity_id, t2.division_id,
    t2.geography_id, t2.unit_code,t2.country_id,
    t2.unit_name, t2.address, t2.postal_code,
    t2.is_approved, t2.is_closed as is_active,
    t4.legal_entity_name as l_entity,
    (select business_group_name from tbl_business_groups
        where business_group_id = t2.business_group_id) as b_group,
    (select division_name from tbl_divisions
        where division_id = t2.division_id) as division,
    (select category_name from tbl_categories
        where category_id = t2.category_id) as category_name,
    t9.short_name as group_name,
    t8.country_name, t2.category_id, t2.remarks
    from
    tbl_user_legalentity as t1,
    tbl_units as t2,
    tbl_legal_entities as t4,
    tbl_countries as t8,
    tbl_client_groups as t9
    where
    t9.client_id = t2.client_id and
    t8.country_id = t2.country_id and
    t4.legal_entity_id = t2.legal_entity_id and
    t2.legal_entity_id = t1.legal_entity_id and
    t2.client_id = t1.client_id and
    t1.user_id = userId
    group by group_name, b_group, l_entity, country_name
    order by group_name, b_group, l_entity, country_name;

    select t3.unit_id, t3.domain_id, t3.organisation_id
    from
    tbl_user_legalentity as t1,
    tbl_units as t2,
    tbl_units_organizations as t3
    where
    t3.unit_id = t2.unit_id and
    t2.legal_entity_id = t1.legal_entity_id and
    t2.client_id = t1.client_id and
    t1.user_id =userId;
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
    where country_id in (select t2.country_id from tbl_user_legalentity as t1,
    tbl_legal_entities as t2 where
    t2.legal_entity_id = t1.legal_entity_id and
    t2.client_id = t1.client_id and t1.user_id  = userId) order by level_position;
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
    and t2.country_id in (select t2.country_id from tbl_user_legalentity as t1,
    tbl_legal_entities as t2 where
    t2.legal_entity_id = t1.legal_entity_id and
    t2.client_id = t1.client_id and t1.user_id  = userId);
END //
DELIMITER ;


-- --------------------------------------------------------------------------------
-- To get client domains of all clients under userid - client unit
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_tbl_unit_getclientdomains`;
DELIMITER //
CREATE PROCEDURE `sp_tbl_unit_getclientdomains`(in userId INT(11),
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
        WHERE is_closed=0 and tu.legal_entity_id=tle.legal_entity_id
        and is_approved=0
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
        SELECT category_name FROM tbl_categories tcm
        WHERE tcm.category_id = tu.category_id
    ) as category_name,
    unit_id, unit_code, unit_name, address, postal_code,
    (
        SELECT geography_name FROM tbl_geographies tg
        WHERE tg.geography_id=tu.geography_id
    ) as geography_name
    FROM tbl_units tu
    WHERE is_closed=0 and is_approved=0
    and legal_entity_id=le_id;

    SELECT unit_id, (
        SELECT domain_name FROM tbl_domains td
        WHERE td.domain_id=tui.domain_id
    ) as domain_name, (
        SELECT organisation_name FROM tbl_organisation ti
        WHERE ti.organisation_id=tui.organisation_id
    ) as organisation_name
    FROM tbl_units_organizations tui WHERE unit_id in (
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
    SELECT client_id, group_name, email_id, count, client_countries, short_name
    FROM (
        SELECT client_id, group_name, email_id, short_name,
        (
            SELECT count(legal_entity_id) FROM tbl_legal_entities tle
            WHERE tle.client_id = tcg.client_id and is_active=1
        ) as count,
        (
            select group_concat(country_id) from tbl_countries
            where country_id in (
                select country_id from tbl_legal_entities
                where client_id=client_id
            )
        ) as client_countries
        FROM tbl_client_groups tcg
        WHERE is_approved != 1
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
    session_user INT(11)
)
BEGIN
    IF domainid IS NULL THEN
        INSERT INTO tbl_domains (
        domain_name, is_active,
        created_by, created_on) VALUES (
        domainname, 1, session_user, current_ist_datetime());
    ELSE
        UPDATE tbl_domains SET
        domain_name = domainname,
        updated_on = current_ist_datetime(), updated_by = session_user
        WHERE domain_id = domainid;
    END IF;
END //
DELIMITER ;

DROP PROCEDURE IF EXISTS `sp_domaincountries_delete`;
DELIMITER //
CREATE PROCEDURE `sp_domaincountries_delete`(
    IN d_id INT(11)
)
BEGIN
    DELETE FROM tbl_domain_countries where domain_id = d_id;
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
    FROM tbl_legal_entity_domains
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
DROP PROCEDURE IF EXISTS `sp_categorywise_forms_list`;
DELIMITER //
CREATE PROCEDURE `sp_categorywise_forms_list`()
BEGIN

    SELECT T1.form_id, (select form_type from tbl_form_type where form_type_id = T1.form_type_id) as form_type,
    T1.form_name, T1.form_url,
    T1.form_order, T1.parent_menu FROM tbl_forms as T1
    INNER JOIN tbl_form_category as T2 ON T2.form_id = T1.form_id
    WHERE T2.category_id_3 = 1 and T1.form_type_id != 4 ;

    SELECT T1.form_id, (select form_type from tbl_form_type where form_type_id = T1.form_type_id) as form_type,
    T1.form_name, T1.form_url,
    T1.form_order, T1.parent_menu FROM tbl_forms as T1
    INNER JOIN tbl_form_category as T2 ON T2.form_id = T1.form_id
    WHERE T2.category_id_4 = 1 and T1.form_type_id != 4 ;

    SELECT T1.form_id, (select form_type from tbl_form_type where form_type_id = T1.form_type_id) as form_type,
    T1.form_name, T1.form_url,
    T1.form_order, T1.parent_menu FROM tbl_forms as T1
    INNER JOIN tbl_form_category as T2 ON T2.form_id = T1.form_id
    WHERE T2.category_id_5 = 1 and T1.form_type_id != 4 ;

    SELECT T1.form_id, (select form_type from tbl_form_type where form_type_id = T1.form_type_id) as form_type,
    T1.form_name, T1.form_url,
    T1.form_order, T1.parent_menu FROM tbl_forms as T1
    INNER JOIN tbl_form_category as T2 ON T2.form_id = T1.form_id
    WHERE T2.category_id_6 = 1 and T1.form_type_id != 4 ;

    SELECT T1.form_id, (select form_type from tbl_form_type where form_type_id = T1.form_type_id) as form_type,
    T1.form_name, T1.form_url,
    T1.form_order, T1.parent_menu FROM tbl_forms as T1
    INNER JOIN tbl_form_category as T2 ON T2.form_id = T1.form_id
    WHERE T2.category_id_7 = 1 and T1.form_type_id != 4 ;

    SELECT T1.form_id, (select form_type from tbl_form_type where form_type_id = T1.form_type_id) as form_type,
    T1.form_name, T1.form_url,
    T1.form_order, T1.parent_menu FROM tbl_forms as T1
    INNER JOIN tbl_form_category as T2 ON T2.form_id = T1.form_id
    WHERE T2.category_id_8 = 1 and T1.form_type_id != 4 ;

END //
DELIMITER ;

-- --------------------------------------------------------------------------------
-- To get Knowledge and Techno form categories
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_usercategory_list`;
DELIMITER //
CREATE PROCEDURE `sp_usercategory_list` ()
BEGIN
    SELECT user_category_id, user_category_name
    FROM tbl_user_category where user_category_id > 2;
END //
DELIMITER ;

-- --------------------------------------------------------------------------------
-- To get Detailed list of user group
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_usergroup_detailed_list`;
DELIMITER //
CREATE PROCEDURE `sp_usergroup_detailed_list` ()
BEGIN
    SELECT ug.user_group_id, user_group_name, user_category_id,
    is_active, (SELECT count(user_id) FROM tbl_users u WHERE
    ug.user_group_id = u.user_group_id) AS count
    FROM tbl_user_groups ug ORDER BY user_category_id, user_group_name;

    SELECT T1.user_group_id, T1.form_id from tbl_user_group_forms as T1 INNER JOIN tbl_user_groups as T2
    ON T2.user_group_id = T1.user_group_id ;
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
    IN ug_id INT(11), u_cat_id INT(11), ug_name VARCHAR(50),
    session_user INT(11)
)
BEGIN
    IF ug_id IS NULL THEN
        INSERT INTO tbl_user_groups
        (user_category_id, user_group_name, is_active, created_by, created_on)
        VALUES (u_cat_id, ug_name, 1, session_user, current_ist_datetime());
    ELSE
        UPDATE tbl_user_groups SET user_category_id = u_cat_id,
        user_group_name = ug_name,
        updated_by = session_user, updated_on = current_ist_datetime()
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
    session_user INT(11)
)
BEGIN
    UPDATE tbl_user_groups set is_active = isactive,
    updated_by = session_user, updated_on = current_ist_datetime()
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
    SELECT user_group_id, user_category_id, user_group_name, is_active
    FROM tbl_user_groups ORDER BY user_group_name;

    SELECT user_category_id, user_category_name FROM tbl_user_category where user_category_id > 2;
END //
DELIMITER ;

-- --------------------------------------------------------------------------------
-- To get All User Details
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_user_detailed_list`;
DELIMITER //
CREATE PROCEDURE `sp_user_detailed_list`()
BEGIN
    SELECT T1.user_id, T1.user_category_id,
    (select user_category_name from tbl_user_category where user_category_id = T1.user_category_id) as user_category_name,
    T1.employee_name, T1.employee_code, T1.email_id,
    T1.user_group_id,
    T1.contact_no, T1.mobile_no, T1.address, T1.designation, T1.is_active, T1.is_disable,
    T2.username
    FROM tbl_users T1
    LEFT JOIN tbl_user_login_details T2 ON T1.user_id = T2.user_id
    WHERE T1.user_category_id > 2
    ORDER BY T1.employee_name;

    SELECT user_id, domain_id, country_id from tbl_user_domains;
    SELECT user_id, country_id from tbl_user_countries;

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

DELIMITER ;

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
DELIMITER ;

-- --------------------------------------------------------------------------------
-- To save / update user
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_users_save`;

DELIMITER //

CREATE PROCEDURE `sp_users_save`(
    IN u_cat_id INT(11), userid INT(11), emailid VARCHAR(100), ug_id INT(11),
    emp_name VARCHAR(50), emp_code VARCHAR(20),
    contactno VARCHAR(12), mobileno VARCHAR(15), addr TEXT, desig VARCHAR(50),
    session_user INT(11)
)
BEGIN
    IF userid IS NULL THEN
        INSERT INTO tbl_users (
            user_category_id, employee_name, employee_code, email_id,
            contact_no, mobile_no, user_group_id, address, designation,
            is_active, created_by, created_on
        )   VALUES (
            u_cat_id, emp_name, emp_code, emailid,
            contactno, mobileno, ug_id, addr, desig, 1, session_user, current_ist_datetime()
        );
    ELSE
        UPDATE tbl_users SET user_category_id=u_cat_id, email_id=emailid,
        employee_name=emp_name, user_group_id=ug_id,
        employee_code=emp_code, contact_no=contactno,
        mobile_no=mobileno, address=addr,
        designation = desig, updated_by=session_user,
        updated_on = current_ist_datetime() WHERE user_id=userid;

        UPDATE tbl_user_login_details set email_id = emailid,
        user_category_id=u_cat_id where user_id = userid;

    END IF;
END //
DELIMITER ;

-- --------------------------------------------------------------------------------
-- To Save verification token
-- --------------------------------------------------------------------------------

DROP PROCEDURE IF EXISTS `sp_tbl_email_verification_save`;

DELIMITER //

CREATE PROCEDURE `sp_tbl_email_verification_save`(
    IN u_id INT(11), r_token TEXT, t_type INT(11), e_date datetime
)
BEGIN
    INSERT INTO tbl_email_verification(user_id, verification_code, verification_type_id, expiry_date)
    VALUES (u_id, r_token, t_type, e_date);
END //
DELIMITER ;


-- --------------------------------------------------------------------------------
-- To Check the status of user group of the user
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_user_usergroup_status`;
DELIMITER //
CREATE PROCEDURE `sp_user_usergroup_status`(
    IN userid INT(11)
)
BEGIN
    select count(ug.user_group_id) as group_count from tbl_user_groups ug
    inner join tbl_users u on  ug.user_group_id = u.user_group_id
    where u.user_id = userid and ug.is_active = 1;
END //
DELIMITER ;

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
        updated_by =  session_user and status_changed_on = updated_time
        WHERE user_id = userid;

    SELECT @_isdisable:= is_disable from tbl_users WHERE user_id = userid;
    IF @_isdisable = 0 and isactive = 1 THEN
        SET @_val = 1;
    ELSE
        SET @_val = 0;
    END IF;
    UPDATE tbl_user_login_details set is_active = @_val
        where user_id = userid;
END //
DELIMITER ;



-- --------------------------------------------------------------------------------
-- To update the status of user
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_users_disable_status`;
DELIMITER //
CREATE PROCEDURE `sp_users_disable_status`(
    IN userid INT(11), isdisable TINYINT(4), session_user INT(11),
    updated_time TIMESTAMP
)
BEGIN
    UPDATE tbl_users set is_disable = isdisable,
        updated_by =  session_user and disabled_on = updated_time
        WHERE user_id = userid;
    SELECT @_isactive:= is_active from tbl_users WHERE user_id = userid;
    IF @_isactive = 1 and isdisable = 0 THEN
        SET @_val = 1;
    ELSE
        SET @_val = 0;
    END IF;
    UPDATE tbl_user_login_details set is_active = @_val
        where user_id = userid;
END //
DELIMITER ;

-- --------------------------------------------------------------------------------
-- To Get the name of employee by id
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_empname_by_id`;
DELIMITER //
CREATE PROCEDURE `sp_empname_by_id`(
    IN userid INT(11)
)
BEGIN
    SELECT concat(employee_code, " - ", employee_name) as empname
    FROM tbl_users
    WHERE user_id = userid;
END //
DELIMITER ;

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
DELIMITER ;

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
DELIMITER ;

-- --------------------------------------------------------------------------------
-- To get the form category of the admin user
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_admin_getformcategory`;
DELIMITER //
CREATE PROCEDURE `sp_admin_getformcategory`(
    IN uname VARCHAR(100)
)
BEGIN
    DECLARE fc_id INT(11);
    DECLARE utype INT(11);
    SELECT user_type into utype FROM tbl_admin WHERE username = uname;
    IF utype = 0 THEN
        SET fc_id = 1;
    ELSE
        SET fc_id = 2;
    END IF;
    SELECT fc_id;
END //
DELIMITER ;

-- --------------------------------------------------------------------------------
-- To get all database server details
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_databaseserver_list`;
DELIMITER //
CREATE PROCEDURE `sp_databaseserver_list`()
BEGIN
    SELECT database_server_name, database_ip, database_port,
    database_username, database_password, legal_entity_ids
    FROM tbl_database_server;
END //
DELIMITER ;

-- --------------------------------------------------------------------------------
-- To Check whether the db server name already exists or not
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_databaseserver_is_duplicate`;
DELIMITER //
CREATE PROCEDURE `sp_databaseserver_is_duplicate`(
    IN dbservername VARCHAR(50), ip_addr TEXT
)
BEGIN
    SELECT count(database_ip) as count FROM tbl_database_server
    WHERE database_server_name = dbservername and database_ip != ip_addr;
END //
DELIMITER ;

-- --------------------------------------------------------------------------------
-- To save or update Database server
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_databaseserver_save`;
DELIMITER //
CREATE PROCEDURE `sp_databaseserver_save`(
    IN dbservername VARCHAR(50), ipaddr VARCHAR(50),
    port_no INT(11), username VARCHAR(50), pwd VARCHAR(50)
)
BEGIN
    INSERT INTO tbl_database_server (
        database_server_name, database_ip, database_port, database_username, database_password
    ) VALUES (dbservername, ipaddr, port_no, username, pwd)
    ON DUPLICATE KEY UPDATE database_server_name = dbservername,
    database_username = username, database_password=pwd, database_port = port_no;
END //
DELIMITER ;

-- --------------------------------------------------------------------------------
-- To get all Machine  details
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_machines_list`;
DELIMITER //
CREATE PROCEDURE `sp_machines_list`()
BEGIN
    SELECT machine_id, machine_name, ip, port, legal_entity_ids
    FROM tbl_application_server;
END //
DELIMITER ;

-- --------------------------------------------------------------------------------
-- To Check whether the machine name already exists or not
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_machines_is_duplicate`;
DELIMITER //
CREATE PROCEDURE `sp_machines_is_duplicate`(
    IN machinename VARCHAR(50), machineid INT(11)
)
BEGIN
    IF machineid IS NULL THEN
        SELECT count(machine_id) as count FROM tbl_application_server
        WHERE machine_name = machinename;
    ELSE
        SELECT count(machine_id) as count FROM tbl_application_server
        WHERE machine_name = machinename and machine_id != machineid;
    END IF;
END //
DELIMITER ;

-- --------------------------------------------------------------------------------
-- To save or update Machine
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_machines_save`;
DELIMITER //
CREATE PROCEDURE `sp_machines_save`(
    IN machineid INT(11), machinename VARCHAR(50), ipaddr VARCHAR(50),
    port_no INT(11)
)
BEGIN
    IF machineid IS NULL THEN
        INSERT INTO tbl_application_server (
            machine_name, ip, port
        ) VALUES (machinename, ipaddr, port_no) ;

    ELSE
        UPDATE tbl_application_server SET machine_name = machinename,
        ip=ipaddr, port = port_no WHERE machine_id = machineid;
    END IF;
END //
DELIMITER ;

-- --------------------------------------------------------------------------------
-- To Get data for Allocate database environment
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_clientdatabase_list`;
DELIMITER //
CREATE PROCEDURE `sp_clientdatabase_list`()
BEGIN
    SELECT client_id, legal_entity_id, machine_id, database_ip
    FROM tbl_client_database;

    SELECT client_id, group_name FROM tbl_client_groups;

    SELECT legal_entity_id, legal_entity_name, client_id
    FROM tbl_legal_entities;

    SELECT machine_id, machine_name FROM tbl_machines;

    SELECT db_server_name, ip  FROM tbl_database_server;
END //
DELIMITER ;

-- --------------------------------------------------------------------------------
-- To Save or Update Client database details
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_clientdatabase_save`;
DELIMITER //
CREATE PROCEDURE `sp_clientdatabase_save`(
    IN clientid INT(11), le_id INT(11),
    db_server_ip VARCHAR(20), machineid INT(11)
)
BEGIN
    DECLARE port_no INT(11);
    DECLARE username VARCHAR(50);
    DECLARE pwd VARCHAR(50);
    DECLARE dbservername VARCHAR(50);
    DECLARE machine_ip VARCHAR(50);
    DECLARE machine_port INT(4);
    DECLARE shortname VARCHAR(20);
    SELECT port INTO port_no FROM tbl_database_server WHERE ip = db_server_ip;
    SELECT server_username INTO username FROM tbl_database_server WHERE ip = db_server_ip;
    SELECT server_password INTO pwd FROM tbl_database_server WHERE ip = db_server_ip;
    SELECT db_server_name INTO dbservername FROM tbl_database_server WHERE ip = db_server_ip;
    SELECT ip INTO machine_ip FROM tbl_machines WHERE machine_id = machineid;
    SELECT port INTO machine_port FROM tbl_machines WHERE machine_id = machineid;
    SELECT short_name INTO shortname FROM tbl_client_groups WHERE client_id=clientid;
    INSERT INTO tbl_client_database (
        client_id, legal_entity_id, machine_id, database_ip,
        database_port, database_username, database_password,
        database_name, server_ip, server_port, client_short_name
    ) VALUES (
        clientid, le_id, machineid, db_server_ip, port_no, username,
        pwd, dbservername, machine_ip, machine_port, shortname
    ) ON DUPLICATE KEY UPDATE machine_id=machineid,
    database_ip = db_server_ip, database_port=port_no,
    database_username=username, database_password=pwd,
    database_name=dbservername, server_ip=machine_ip,
    server_port=machine_port;
END //
DELIMITER ;

-- --------------------------------------------------------------------------------
-- To Get data for Configuring File Storage
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_clientfilestorage_list`;
DELIMITER //
CREATE PROCEDURE `sp_clientfilestorage_list`()
BEGIN
    SELECT client_id, legal_entity_id, machine_id
    FROM tbl_client_filestorage;

    SELECT client_id, group_name FROM tbl_client_groups;

    SELECT legal_entity_id, legal_entity_name, client_id
    FROM tbl_legal_entities;

    SELECT machine_id, machine_name FROM tbl_machines;
END //
DELIMITER ;

-- --------------------------------------------------------------------------------
-- To Update File storage server id for a legal entity
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_clientfilestorage_save`;
DELIMITER //
CREATE PROCEDURE `sp_clientfilestorage_save`(
    IN clientid INT(11), le_id INT(11), machineid INT(11)
)
BEGIN
    INSERT INTO tbl_client_filestorage
    (client_id, legal_entity_id, machine_id) VALUES
    (clientid, le_id, machineid) ON DUPLICATE KEY UPDATE
    machine_id=machineid;
END //
DELIMITER ;

-- --------------------------------------------------------------------------------
-- To Get data for Auto deletion form
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_unit_autodeletion_list`;
DELIMITER //
CREATE PROCEDURE `sp_unit_autodeletion_list`()
BEGIN
    SELECT client_id, group_name FROM tbl_client_groups;

    SELECT legal_entity_id, legal_entity_name, client_id,
    (
        SELECT count(unit_id) FROM tbl_units tu
        WHERE tu.legal_entity_id=tl.legal_entity_id
    ) as unit_count,
    (
        SELECT max(deletion_year) FROM tbl_unit_autodeletion tua
        WHERE tua.client_id=tl.client_id
        and tua.legal_entity_id = tl.legal_entity_id
    ) as deletion_period, is_active
    FROM tbl_legal_entities tl;

    SELECT unit_id, client_id, legal_entity_id, unit_code, unit_name,
    (
        SELECT deletion_year FROM tbl_unit_autodeletion tua
        WHERE tua.client_id=tu.client_id
        and tua.legal_entity_id = tu.legal_entity_id
    ) as deletion_year, address FROM tbl_units tu;
END //
DELIMITER ;

-- --------------------------------------------------------------------------------
-- To delete Auto deletion details of all units under a legal entity
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_unitautodeletion_delete`;
DELIMITER //
CREATE PROCEDURE `sp_unitautodeletion_delete`(
    IN le_id INT(11)
)
BEGIN
    DELETE FROM tbl_unit_autodeletion
    WHERE legal_entity_id=le_id;
END //
DELIMITER ;

-- --------------------------------------------------------------------------------
-- To get the users under following type CC Managers, CC Users, Techno managers
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_users_type_wise`;
DELIMITER //
CREATE PROCEDURE `sp_users_type_wise`()
BEGIN
    SELECT user_id, is_active,
    concat(employee_code," - ", employee_name) as employee_name
    FROM tbl_users WHERE user_category_id=3;
    SELECT user_id, is_active,
    concat(employee_code," - ", employee_name) as employee_name
    FROM tbl_users WHERE user_category_id=4;
    SELECT user_id, is_active,
    concat(employee_code," - ", employee_name) as employee_name
    FROM tbl_users WHERE user_category_id=5;
    SELECT user_id, is_active,
    concat(employee_code," - ", employee_name) as employee_name
    FROM tbl_users WHERE user_category_id=6;
    SELECT user_id, is_active,
    concat(employee_code," - ", employee_name) as employee_name
    FROM tbl_users WHERE user_category_id=7;
    SELECT user_id, is_active,
    concat(employee_code," - ", employee_name) as employee_name
    FROM tbl_users WHERE user_category_id=8;
    SELECT user_id, country_id FROM tbl_user_countries;
    SELECT user_id, domain_id FROM tbl_user_domains;
END //
DELIMITER ;

-- --------------------------------------------------------------------------------
-- To get User mappings
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_usermappings_list`;
DELIMITER //
CREATE PROCEDURE `sp_usermappings_list`()
BEGIN
    select user_mapping_id, user_category_id, country_id, domain_id,
    parent_user_id, child_user_id from tbl_user_mapping;
END //
DELIMITER ;

-- --------------------------------------------------------------------------------
-- To get user category by user id
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_users_category_by_id`;
DELIMITER //
CREATE PROCEDURE `sp_users_category_by_id`(
    IN userid INT(11)
)
BEGIN
    SELECT user_category_id FROM tbl_users WHERE user_id=userid;
END //
DELIMITER ;

-- --------------------------------------------------------------------------------
-- Delete Mappings under a parent user
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_usermapping_delete`;
DELIMITER //
CREATE PROCEDURE `sp_usermapping_delete`(
    IN parent_userid INT(11)
)
BEGIN
    DELETE FROM tbl_user_mapping WHERE parent_user_id=parent_userid;
END //
DELIMITER ;

-- To get list of countries under client master group
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_countries_for_unit`;
DELIMITER //
CREATE PROCEDURE `sp_countries_for_unit`(IN session_user INT(11))
BEGIN
    select t4.country_id, t4.country_name, t3.business_group_id, t1.client_id
    from
    tbl_user_legalentity as t1,
    tbl_legal_entities as t2,
    tbl_business_groups as t3,
    tbl_countries as t4
    where
    t4.country_id = t2.country_id and
    t3.business_group_id = t2.business_group_id and
    t2.client_id = t1.client_id and
    t1.user_id = session_user;
END//
DELIMITER ;

-- --------------------------------------------------------------------------------
-- To get list of industries for client id for client unit
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_tbl_units_getindustries_for_legalentity`;
DELIMITER //
CREATE PROCEDURE `sp_tbl_units_getindustries_for_legalentity`(IN session_user INT(11))
BEGIN
    IF session_user > 0 THEN
        select t3.organisation_id, t3.organisation_name, t3.country_id, t3.domain_id,
                t3.is_active, t2.client_id, t2.no_of_units, t2.legal_entity_id
            from tbl_client_users as t1, tbl_legal_entity_domain_industry as t2,
                    tbl_organisation as t3
            where
                t3.organisation_id = t2.organisation_id and
                t2.client_id = t1.client_id and
                t1.user_id = session_user
            order by organisation_name;
    ELSE
        select t3.organisation_id, t3.organisation_name, t3.country_id, t3.domain_id,
                t3.is_active, t2.client_id, t2.no_of_units, t2.legal_entity_id
            from tbl_legal_entity_domain_industry as t2,
                    tbl_organisation as t3
            where
                t3.organisation_id = t2.organisation_id and
                t2.client_id in (select client_id from tbl_client_users)
            order by organisation_name;
   END IF;
DELIMITER ;

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
DELIMITER ;

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
DELIMITER ;

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
DELIMITER ;

-- --------------------------------------------------------------------------------
-- Get unit max id
-- -- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_tbl_units_max_unitid`;
DELIMITER //
CREATE PROCEDURE `sp_tbl_units_max_unitid`()
BEGIN
    select max(unit_id) as max_id from
    tbl_units;
END //
DELIMITER ;

-- --------------------------------------------------------------------------------
-- To get Unassigned units list
-- -- -----------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_userunits_list`;
DELIMITER //
CREATE PROCEDURE `sp_userunits_list`()
BEGIN
    select count(tu.unit_id) as total_units, tu.client_id,
    tu.legal_entity_id, domain_id, (
        SELECT domain_name from tbl_domains td
        WHERE td.domain_id=tud.domain_id
    ) as domain_name,(
        SELECT group_name FROM tbl_client_groups tcg
        WHERE tcg.client_id=tu.client_id
    ) as client_name,(
        SELECT count(unit_id) FROM tbl_user_units tuu
        WHERE tuu.domain_id=tud.domain_id and tuu.client_id=tu.client_id
    ) as assigned_units
    from tbl_units tu inner join tbl_unit_industries tud
    ON tu.unit_id = tud.unit_id group by client_id, domain_id;
END//
DELIMITER ;

-- --------------------------------------------------------------------------------
-- To get assigned units list
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_userunits_assigned_list`;
DELIMITER //
CREATE PROCEDURE `sp_userunits_assigned_list`(
    IN clientid INT(11), domainid INT(11)
)
BEGIN
    SELECT tuu.user_id,
    concat(employee_code,"-", employee_name) as employee_name,
    tuu.legal_entity_id, legal_entity_name,
    count(unit_id) as no_of_units,
    (
        SELECT business_group_name FROM tbl_business_groups tbg
        WHERE tbg.business_group_id=tle.business_group_id
    ) as business_group_name
    FROM tbl_user_units tuu
    INNER JOIN tbl_users tu ON tu.user_id = tuu.user_id
    INNER JOIN tbl_legal_entities tle ON tle.legal_entity_id=tuu.legal_entity_id
    WHERE tuu.client_id=clientid and domain_id=domainid
    group by user_id;
END //
DELIMITER ;

-- --------------------------------------------------------------------------------
-- To get assigned unit details list
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_userunits_assigned_details_list`;
DELIMITER //
CREATE PROCEDURE `sp_userunits_assigned_details_list`(
    IN u_id INT(11), le_id INT(11)
)
BEGIN
    select unit_id, (
        SELECT legal_entity_name FROM tbl_legal_entities tle
        WHERE tle.legal_entity_id=tu.legal_entity_id
    ) as legal_entity_name,(
        SELECT division_name FROM tbl_divisions td
        WHERE td.division_id=tu.division_id
    ) as division_name,(
        SELECT category_name FROM tbl_category_master tcm
        WHERE tcm.category_id=tu.category_id
    ) as category_name, unit_code, unit_name, address, (
        SELECT geography_name FROM tbl_geographies tgm
        WHERE tgm.geography_id = tu.geography_id
    ) as geography_name FROM tbl_units tu
    WHERE legal_entity_id = le_id and unit_id in (
        SELECT unit_id FROM tbl_user_units
        WHERE user_id=u_id and legal_entity_id= le_id
    );
    SELECT unit_id, (
        SELECT domain_name FROM tbl_domains td
        WHERE td.domain_id = tui.domain_id
    ) as domain_name, (
        SELECT industry_name FROM tbl_industries ti
        WHERE ti.industry_id = tui.industry_id
    ) as industry_name FROM tbl_unit_industries tui
    WHERE tui.unit_id in (
        SELECT unit_id FROM tbl_units tu WHERE tu.legal_entity_id=le_id
    );
END //
DELIMITER ;

-- --------------------------------------------------------------------------------
-- To get domain managers
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_users_domain_managers`;
DELIMITER //
CREATE PROCEDURE `sp_users_domain_managers`(
    IN session_user INT(11)
)
BEGIN
    SELECT user_id,
    concat(employee_code, "-", employee_name) as employee_name,
    is_active FROM tbl_users WHERE user_category_id=7 and
    user_id in (SELECT child_user_id FROM tbl_user_mapping
    WHERE parent_user_id=session_user);
END //
DELIMITER ;

-- --------------------------------------------------------------------------------
-- To get list of units under a client
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_units_list`;
DELIMITER //
CREATE PROCEDURE `sp_units_list`(
    IN clientid INT(11)
)
BEGIN
    SELECT tu.unit_id, unit_code, unit_name,
    address, (
        SELECT division_name FROM tbl_divisions td
        WHERE td.division_id=tu.division_id
    ) as division_name, (
        SELECT category_name FROM tbl_category_master tcm
        WHERE tcm.category_id=tu.category_id
    ) as category_name,legal_entity_id,(
        SELECT legal_entity_name FROM tbl_legal_entities tle
        WHERE tle.legal_entity_id=tu.legal_entity_id
    ) as legal_entity_name,
    business_group_id, is_active, (
        SELECT geography_name FROM tbl_geographies tg
        WHERE tg.geography_id = tu.geography_id
    ) as geography_name
    FROM tbl_units tu
    INNER JOIN tbl_unit_industries tui on tui.unit_id=tu.unit_id
    WHERE client_id=clientid and tui.domain_id=domainid and
    tu.unit_id not in (
        SELECT unit_id FROM tbl_user_units
        WHERE client_id=clientid
    )
    order by unit_name ASC;
    SELECT tui.unit_id, (
        SELECT domain_name FROM tbl_domains td
        WHERE td.domain_id = tui.domain_id
    ) as domain_name, (
        SELECT industry_name FROM tbl_industries ti
        WHERE ti.industry_id = tui.industry_id
    ) as industry_name FROM tbl_unit_industries tui
    WHERE tui.unit_id in (
        SELECT unit_id FROM tbl_units tu WHERE tu.client_id=clientid
    ) and tui.domain_id=domainid;
END //
DELIMITER ;

-- --------------------------------------------------------------------------------
-- To get list of business groups under a client
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_business_groups_by_client`;
DELIMITER //
CREATE PROCEDURE `sp_business_groups_by_client`(
    IN clientid INT(11)
)
BEGIN
    SELECT business_group_id, business_group_name, client_id
    FROM tbl_business_groups WHERE client_id=clientid;
END //
DELIMITER ;

-- --------------------------------------------------------------------------------
-- To get legal entities under a client
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_legal_entities_by_client`;
DELIMITER //
CREATE PROCEDURE `sp_legal_entities_by_client`(
    IN clientid INT(11)
)
BEGIN
    SELECT legal_entity_id, legal_entity_name, business_group_id,
    client_id FROM tbl_legal_entities WHERE client_id=clientid;
END //
DELIMITER ;

-- --------------------------------------------------------------------------------
-- To delete user units
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_userunits_delete`;
DELIMITER //
CREATE PROCEDURE `sp_userunits_delete`(
    IN userid INT(11)
)
BEGIN
    DELETE FROM tbl_user_units WHERE user_id=userid;
END //
DELIMITER ;

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
        tbl_categories where category_name = param;
    end if;
    if tableName = 'div_name' then
        select count(0) as div_name_cnt from
        tbl_divisions where division_name = param;
    end if;
END //
DELIMITER ;

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
END //
DELIMITER ;

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
    insert into tbl_categories
    (client_id, business_group_id, legal_entity_id, division_id,
    category_name, created_by, created_on)
    values
    (clientId, bg_id, le_id, div_id, categoryName, createdBy, createdOn);
END //
DELIMITER ;

-- --------------------------------------------------------------------------------
-- To get list of units
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_units_name_and_id`;
DELIMITER //
CREATE PROCEDURE `sp_units_name_and_id`(
)
BEGIN
    SELECT unit_id, unit_code, unit_name, address, division_id,
    legal_entity_id, business_group_id, client_id, is_closed as is_active
    FROM tbl_units;
END //
DELIMITER ;

-- --------------------------------------------------------------------------------
-- To get list of assigned legal entities
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_userlegalentities_assigned_list`;
DELIMITER //
CREATE PROCEDURE `sp_userlegalentities_assigned_list`()
BEGIN
    SELECT user_id, legal_entity_id FROM tbl_user_legalentity;
END //
DELIMITER ;

-- --------------------------------------------------------------------------------
-- To get list of assigned units
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_userunits_reassign_list`;
DELIMITER //
CREATE PROCEDURE `sp_userunits_reassign_list`()
BEGIN
    SELECT user_id, unit_id, domain_id FROM tbl_user_units;
END //
DELIMITER ;

-- --------------------------------------------------------------------------------
-- To get name of group/ legal entity/ Unit by ids
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_names_by_id`;
DELIMITER //
CREATE PROCEDURE `sp_names_by_id`(
    IN assigned_ids TEXT, user_type INT(11)
)
BEGIN
    IF user_type = 1 then
        SELECT group_name as name FROM tbl_client_groups
        WHERE find_in_set(assigned_ids, client_id);
    ELSEIF user_type = 2 then
        SELECT legal_entity_name as name FROM tbl_legal_entities
        WHERE find_in_set(assinged_ids, legal_entity_id);
    ELSE
        SELECT concat(unit_code, "-", unit_name) as name
        FROM tbl_units WHERE find_in_set(assigned_ids, unit_id);
    END IF;
END //
DELIMITER ;

-- --------------------------------------------------------------------------------
-- To save reassign user account history
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_reassignaccounthistory_save`;
DELIMITER //
CREATE PROCEDURE `sp_reassignaccounthistory_save`(
    IN old_user_id INT(11), new_user_id INT(11),
    reassigned_data_text TEXT, remark_text TEXT, session_user INT(11),
    current_time_stamp DATETIME
)
BEGIN
    INSERT INTO tbl_user_account_reassign_history
    (user_category_id, reassigned_from, reassigned_to, reassigned_data,
    remarks, assigned_by, assigned_on) values (
        (SELECT user_category_id
        FROM tbl_users WHERE user_id = old_user_id),
        old_user_id, new_user_id, reassigned_data_text, remark_text,
        session_user, current_time_stamp
    );
END //

-- -------------------------------------------------------------------------------------------
-- To get the list of groups with countries and number of legal entities assigned / unassigned
-- -------------------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_assign_legal_entities_list`;
DELIMITER //
CREATE PROCEDURE `sp_assign_legal_entities_list`()
BEGIN
    select client_id, group_name,
    (
        select group_concat(country_name) from tbl_countries
        where country_id in (
            select country_id from tbl_legal_entities
            where client_id=client_id
        )
    ) as country_names,
    (
        select count(legal_entity_id) from tbl_legal_entities tle
        WHERE tle.client_id=tcg.client_id
    ) as no_of_legal_entities,
    (
        select count(legal_entity_id) from tbl_user_legalentity tule
        WHERE tule.client_id=tcg.client_id group by tule.client_id
    ) as no_of_assigned_legal_entities

    FROM tbl_client_groups tcg;
END //
DELIMITER ;


-- ----------------------------------------------------
-- To get the unassigned legal entity details by client
-- ----------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_unassigned_legal_entity_details_by_group_id`;
DELIMITER //
CREATE PROCEDURE `sp_unassigned_legal_entity_details_by_group_id`(
    IN clientid INT(11)
)
BEGIN
    SELECT t1.legal_entity_id, t1.legal_entity_name,t2.business_group_name, t3.country_name, t3.country_id
    FROM tbl_legal_entities t1
    LEFT JOIN tbl_business_groups t2 on t1.business_group_id = t2.business_group_id
    INNER JOIN tbl_countries t3 on t1.country_id = t3.country_id
    LEFT JOIN tbl_user_legalentity t4 on t1.legal_entity_id = t4.legal_entity_id
    WHERE t1.client_id=clientid and t4.legal_entity_id is null;
END ;
DELIMITER ;

-- ------------------------
-- To get techno users list
-- ------------------------
DROP PROCEDURE IF EXISTS `sp_users_technouser_list`;
DELIMITER //
CREATE PROCEDURE `sp_users_technouser_list`(session_user INT(11))
BEGIN
    SELECT t1.child_user_id as user_id, t2.is_active,
    concat(t2.employee_code," - ", t2.employee_name) as employee_name
    from tbl_user_mapping t1
    INNER JOIN tbl_users t2 ON t1.child_user_id = t2.user_id
    WHERE t1.user_category_id=8 and t1.parent_user_id = session_user;
    SELECT user_id, country_id FROM tbl_user_countries;
    SELECT user_id, domain_id FROM tbl_user_domains;
END //
DELIMITER ;

-- --------------------------------------------------
-- To get the assigned legal entity details by client
-- --------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_assigned_legal_entity_details_by_group_id`;
DELIMITER //
CREATE PROCEDURE `sp_assigned_legal_entity_details_by_group_id`(
    IN clientid INT(11)
)
BEGIN
    SELECT t1.legal_entity_id, t1.legal_entity_name,t2.business_group_name, t3.country_name, t3.country_id
    FROM tbl_legal_entities t1
    LEFT JOIN tbl_business_groups t2 on t1.business_group_id = t2.business_group_id
    INNER JOIN tbl_countries t3 on t1.country_id = t3.country_id
    LEFT JOIN tbl_user_legalentity t4 on t1.legal_entity_id = t4.legal_entity_id
    WHERE t1.client_id=clientid and t4.legal_entity_id is not null;
END //
DELIMITER ;

-- --------------------------------------------------------------------------------
-- To get list of assigned units for reassigning
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_userclients_reassign_list`;
DELIMITER //
CREATE PROCEDURE `sp_userclients_reassign_list`()
BEGIN
    SELECT user_id, client_id FROM tbl_user_clients;
END //
DELIMITER ;


-- --------------------------------------------------------------------------------
-- To get list of client agreement details
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_client_agreement_details`;
DELIMITER //
CREATE PROCEDURE `sp_client_agreement_details`(
 IN countryid_ INT(11), IN clientid_ INT(11), IN businessgroupid_ INT(11),
 IN legalentityid_ INT(11), IN domainid_ INT(11), IN contractfrom_ VARCHAR(50),
 IN contractto_ VARCHAR(50), IN fromcount_ INT(11), IN pagecount_ INT(11), IN userid_ INT(11))
BEGIN
    DECLARE user_category INT(11);
    SELECT user_category_id INTO user_category
    FROM tbl_user_login_details WHERE user_id = userid_;

    select t1.legal_entity_id, t3.domain_id, t1.legal_entity_name, t1.total_licence, t1.file_space_limit, t1.contract_from, t1.used_licence, t1.used_file_space,
    t1.contract_to, t2.group_name, t2.email_id as groupadmin_email, t1.is_closed, t4.business_group_name,
    (select count(domain_id) from tbl_legal_entity_domains where legal_entity_id = t1.legal_entity_id) as domaincount,
    (select domain_name from tbl_domains where domain_id = t3.domain_id) as domain_name,
    (select sum(count) from tbl_legal_entity_domains where domain_id = t3.domain_id and legal_entity_id = t1.legal_entity_id) as domain_total_unit,
    t3.activation_date,
    (select count(o.unit_id) from tbl_units_organizations as o inner join tbl_units as u on o.unit_id = u.unit_id
    where u.legal_entity_id = t1.legal_entity_id and o.domain_id = t3.domain_id) as domain_used_unit,
    (select contact_no from tbl_client_users where user_category_id = 1 and client_id = t1.client_id and t1.legal_entity_id in (legal_entity_ids)) as le_admin_contactno,
    (select email_id from tbl_client_users where user_category_id = 1 and client_id = t1.client_id and t1.legal_entity_id in (legal_entity_ids)) as le_admin_email
    from tbl_legal_entities t1
    inner join tbl_client_groups t2 on t1.client_id = t2.client_id
    inner join tbl_legal_entity_domains t3 on t1.legal_entity_id = t3.legal_entity_id
    inner join tbl_business_groups t4 on t1.business_group_id = t4.business_group_id
    where
    t1.country_id = countryid_ and
    IF(clientid_ IS NOT NULL, t1.client_id = clientid_, 1) and
    IF(businessgroupid_ IS NOT NULL, t1.business_group_id = businessgroupid_, 1) and
    IF(domainid_ IS NOT NULL, t3.domain_id = domainid_,
    IF (user_category > 2,
    t3.domain_id in (select domain_id from tbl_user_domains
        WHERE user_id = userid_
    ), 1) and
    IF(contractfrom_ IS NOT NULL, t1.contract_from >= contractfrom_, 1) and
    IF(contractto_ IS NOT NULL, t1.contract_to <= contractto_, 1) and
    IF(legalentityid_ IS NOT NULL, t1.legal_entity_id = legalentityid_,
    IF (user_category = 5,
    t1.legal_entity_id in (select legal_entity_id from tbl_legal_entities
        WHERE client_id in (
            SELECT client_id FROM tbl_user_clients WHERE user_id = userid_
        )),
    IF (user_category = 6,
    t1.legal_entity_id in (SELECT legal_entity_id FROM tbl_user_legalentity
            WHERE user_id=userid_)
    ,
    IF (user_category = 7 OR user_category = 8,
    t1.legal_entity_id in (SELECT legal_entity_id FROM tbl_units WHERE unit_id in(
            SELECT unit_id FROM tbl_user_units
            WHERE user_id=userid_
        ))
    ,1
    )))))
    group by t3.legal_entity_id, t3.domain_id
    order by t1.legal_entity_name limit fromcount_, pagecount_;
END //
DELIMITER ;

-- --------------------------------------------------------------------------------
-- To get list of client agreement details record count
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_client_agreement_details_count`;
DELIMITER //
CREATE PROCEDURE `sp_client_agreement_details_count`(
 IN countryid_ INT(11), IN clientid_ INT(11), IN businessgroupid_ INT(11),
 IN legalentityid_ INT(11), IN domainid_ INT(11), IN contractfrom_ VARCHAR(50),
 IN contractto_ VARCHAR(50), IN userid_ INT(11))
BEGIN
    DECLARE user_category INT(11);
    SELECT user_category_id INTO user_category
    FROM tbl_user_login_details WHERE user_id = userid_;

    select count(t1.legal_entity_id) as total_record
    from tbl_legal_entities t1
    inner join tbl_legal_entity_domains t3 on t1.legal_entity_id = t3.legal_entity_id
    where
    t1.country_id = countryid_ and
    IF(clientid_ IS NOT NULL, t1.client_id = clientid_, 1) and
    IF(businessgroupid_ IS NOT NULL, t1.business_group_id = businessgroupid_, 1) and
    IF(domainid_ IS NOT NULL, t3.domain_id = domainid_,
    IF (user_category > 2,
    t3.domain_id in (select domain_id from tbl_user_domains
        WHERE user_id = userid_
    ), 1) and
    IF(contractfrom_ IS NOT NULL, t1.contract_from >= contractfrom_, 1) and
    IF(contractto_ IS NOT NULL, t1.contract_to <= contractto_, 1) and
    IF(legalentityid_ IS NOT NULL, t1.legal_entity_id = legalentityid_,
    IF (user_category = 5,
    t1.legal_entity_id in (select legal_entity_id from tbl_legal_entities
        WHERE client_id in (
            SELECT client_id FROM tbl_user_clients WHERE user_id = userid_
        )),
    IF (user_category = 6,
    t1.legal_entity_id in (SELECT legal_entity_id FROM tbl_user_legalentity
            WHERE user_id=userid_)
    ,
    IF (user_category = 7 OR user_category = 8,
    t1.legal_entity_id in (SELECT legal_entity_id FROM tbl_units WHERE unit_id in(
            SELECT unit_id FROM tbl_user_units
            WHERE user_id=userid_
        ))
    ,1
    )))));
END //
DELIMITER ;

-- --------------------------------------------------------------------------------
-- To get list of domainwise agreement details
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_domainwise_agreement_details`;
DELIMITER //
CREATE PROCEDURE `sp_domainwise_agreement_details`(
 IN countryid_ INT(11), IN clientid_ INT(11), IN businessgroupid_ INT(11),
 IN legalentityid_ INT(11), IN domainid_ INT(11), IN contractfrom_ VARCHAR(50),
 IN contractto_ VARCHAR(50), IN fromcount_ INT(11), IN pagecount_ INT(11),IN userid_ INT(11) )
BEGIN
    DECLARE user_category INT(11);
    SELECT user_category_id INTO user_category
    FROM tbl_user_login_details WHERE user_id = userid_;

    select t1.legal_entity_id, t3.domain_id, t1.legal_entity_name, t1.contract_from,
    t1.contract_to, t2.group_name, t2.email_id as groupadmin_email, t4.business_group_name,
    (select sum(count) from tbl_legal_entity_domains where domain_id = t3.domain_id and legal_entity_id = t1.legal_entity_id) as domain_total_unit,
    t3.activation_date,
    (select count(o.unit_id) from tbl_units_organizations as o inner join tbl_units as u on o.unit_id = u.unit_id
    where u.legal_entity_id = t1.legal_entity_id and o.domain_id = t3.domain_id) as domain_used_unit,
    (select contact_no from tbl_client_users where user_category_id = 1 and client_id = t1.client_id and t1.legal_entity_id in (legal_entity_ids)) as le_admin_contactno,
    (select email_id from tbl_client_users where user_category_id = 1 and client_id = t1.client_id and t1.legal_entity_id in (legal_entity_ids)) as le_admin_email
    from tbl_legal_entities t1
    inner join tbl_client_groups t2 on t1.client_id = t2.client_id
    inner join tbl_legal_entity_domains t3 on t1.legal_entity_id = t3.legal_entity_id
    inner join tbl_business_groups t4 on t1.business_group_id = t4.business_group_id
    where
    t1.country_id = countryid_ and t3.domain_id = domainid_ and
    IF(clientid_ IS NOT NULL, t1.client_id = clientid_, 1) and
    IF(businessgroupid_ IS NOT NULL, t1.business_group_id = businessgroupid_, 1) and
    IF(contractfrom_ IS NOT NULL, t1.contract_from >= contractfrom_, 1) and
    IF(contractto_ IS NOT NULL, t1.contract_to <= contractto_, 1) and
    IF(legalentityid_ IS NOT NULL, t1.legal_entity_id = legalentityid_,
    IF (user_category = 5,
    t1.legal_entity_id in (select legal_entity_id from tbl_legal_entities
        WHERE client_id in (
            SELECT client_id FROM tbl_user_clients WHERE user_id = userid_
        )),
    IF (user_category = 6,
    t1.legal_entity_id in (SELECT legal_entity_id FROM tbl_user_legalentity
            WHERE user_id=userid_)
    ,
    IF (user_category = 7 OR user_category = 8,
    t1.legal_entity_id in (SELECT legal_entity_id FROM tbl_units WHERE unit_id in(
            SELECT unit_id FROM tbl_user_units
            WHERE user_id=userid_
        ))
    ,1
    ))))
    group by t1.legal_entity_id
    order by t1.legal_entity_name limit fromcount_, pagecount_;
END //
DELIMITER ;

-- --------------------------------------------------------------------------------
-- To get list of domainwise agreement details record count
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_domainwise_agreement_details_count`;
DELIMITER //
CREATE PROCEDURE `sp_domainwise_agreement_details_count`(
 IN countryid_ INT(11), IN clientid_ INT(11), IN businessgroupid_ INT(11),
 IN legalentityid_ INT(11), IN domainid_ INT(11), IN contractfrom_ VARCHAR(50),
 IN contractto_ VARCHAR(50), IN userid_ INT(11))
BEGIN
    DECLARE user_category INT(11);
    SELECT user_category_id INTO user_category
    FROM tbl_user_login_details WHERE user_id = userid_;

    select count(distinct t1.legal_entity_id) as total_record
    from tbl_legal_entities t1
    inner join tbl_legal_entity_domains t3 on t1.legal_entity_id = t3.legal_entity_id
    where
    t1.country_id = countryid_ and t3.domain_id = domainid_ and
    IF(clientid_ IS NOT NULL, t1.client_id = clientid_, 1) and
    IF(businessgroupid_ IS NOT NULL, t1.business_group_id = businessgroupid_, 1) and
    IF(contractfrom_ IS NOT NULL, t1.contract_from >= contractfrom_, 1) and
    IF(contractto_ IS NOT NULL, t1.contract_to <= contractto_, 1) and
    IF(legalentityid_ IS NOT NULL, t1.legal_entity_id = legalentityid_,
    IF (user_category = 5,
    t1.legal_entity_id in (select legal_entity_id from tbl_legal_entities
        WHERE client_id in (
            SELECT client_id FROM tbl_user_clients WHERE user_id = userid_
        )),
    IF (user_category = 6,
    t1.legal_entity_id in (SELECT legal_entity_id FROM tbl_user_legalentity
            WHERE user_id=userid_)
    ,
    IF (user_category = 7 OR user_category = 8,
    t1.legal_entity_id in (SELECT legal_entity_id FROM tbl_units WHERE unit_id in(
            SELECT unit_id FROM tbl_user_units
            WHERE user_id=userid_
        ))
    ,1
    ))));
END //
DELIMITER ;

-- --------------------------------------------------------------------------------
-- To get list of statutory notification report details
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_statutory_notification_details`;
DELIMITER //
CREATE PROCEDURE `sp_statutory_notification_details`(
 countryid_ INT(11), domainid_ INT(11), statutoryid_ INT(11),
IN fromdate_ VARCHAR(50), IN todate_ VARCHAR(50),
IN fromcount_ INT(11), IN pagecount_ INT(11))
BEGIN
    SELECT
    ts.statutory_name,
    tc.compliance_task,
    tsnl.notification_text,
    tsnl.created_on
FROM
    tbl_statutory_notifications tsnl
        INNER JOIN
    tbl_compliances tc ON tc.compliance_id = tsnl.compliance_id
        INNER JOIN
    tbl_mapped_statutories tms ON tms.statutory_mapping_id = tc.statutory_mapping_id
        INNER JOIN
    tbl_statutories ts ON ts.statutory_id = tms.statutory_id
WHERE
    tc.country_id = countryid_ AND tc.domain_id = domainid_ AND
    IF(statutoryid_ IS NOT NULL, ts.statutory_id = statutoryid_, 1) AND
    IF(fromdate_ IS NOT NULL, tsnl.created_on >= fromdate_, 1) AND
    IF(todate_ IS NOT NULL, tsnl.created_on <= todate_, 1)
limit fromcount_, pagecount_;
END //
DELIMITER ;

-- --------------------------------------------------------------------------------
-- To get list of statutory notification details record count
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_statutory_notification_details_count`;
DELIMITER //
CREATE PROCEDURE `sp_statutory_notification_details_count`(
 countryid_ INT(11), domainid_ INT(11), statutoryid_ INT(11),
IN fromdate_ VARCHAR(50), IN todate_ VARCHAR(50))
BEGIN
    SELECT COUNT(tsnl.notification_id) as total_record
FROM
    tbl_statutory_notifications tsnl
        INNER JOIN
    tbl_compliances tc ON tc.compliance_id = tsnl.compliance_id
        INNER JOIN
    tbl_mapped_statutories tms ON tms.statutory_mapping_id = tc.statutory_mapping_id
        INNER JOIN
    tbl_statutories ts ON ts.statutory_id = tms.statutory_id
WHERE
    tc.country_id = countryid_ AND tc.domain_id = domainid_ AND
    IF(statutoryid_ IS NOT NULL, ts.statutory_id = statutoryid_, 1) AND
    IF(fromdate_ IS NOT NULL, tsnl.created_on >= fromdate_, 1) AND
    IF(todate_ IS NOT NULL, tsnl.created_on <= todate_, 1);
END //
DELIMITER ;

-- --------------------------------------------------------------------------------
-- To get list of level one statutory names
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_levelone_statutories`;
DELIMITER //
CREATE PROCEDURE `sp_levelone_statutories`()
BEGIN
    SELECT
        t1.statutory_id,
        t1.statutory_name,
        t2.country_id,
        t2.domain_id
    FROM
        tbl_statutories t1
            INNER JOIN
        tbl_statutory_levels t2 ON t1.level_id = t2.level_id
    WHERE
        t2.level_position = 1;
END //
DELIMITER ;

-- --------------------------------------------------------------------------------
-- To get organizationwise unit count details
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_organizationwise_unit_count`;
DELIMITER //
CREATE PROCEDURE `sp_organizationwise_unit_count`(IN legalentityid_ INT(11), IN domainid_ INT(11))
BEGIN
    select
    t1.organisation_id,
    t1.count as domain_total_unit,
    (select count(t4.unit_id) from tbl_units_organizations t4
    inner join tbl_units t5 on t4.unit_id = t5.unit_id and t5.legal_entity_id = legalentityid_
    where t4.domain_id = domainid_ and t4.organisation_id = t1.organisation_id
    ) as domain_used_unit,
    (select organisation_name from tbl_organisation where organisation_id = t1.organisation_id) as organization_name,
    (select domain_name from tbl_domains where domain_id = t1.domain_id) as domain_name
    from tbl_legal_entity_domains t1 where t1.legal_entity_id = legalentityid_ and t1.domain_id = domainid_;
END //
DELIMITER ;

-- --------------------------------------------------------------------------------
-- To get categories assigned to an user
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_categories_by_user`;
DELIMITER //
CREATE PROCEDURE `sp_categories_by_user`(
    IN userid INT(11)
)
BEGIN
    DECLARE user_category INT(11);
    SELECT user_category_id INTO user_category FROM tbl_users WHERE user_id = userid;
    IF user_category in (1,2) then
        SELECT category_id, category_name, division_id, legal_entity_id,
        business_group_id, client_id FROM tbl_categories
        Order by category_name ASC;
    ELSEIF user_category = 5 then
        SELECT category_id, category_name, division_id, legal_entity_id,
        business_group_id, client_id FROM tbl_categories
        WHERE client_id in (
            SELECT client_id FROM tbl_user_clients WHERE user_id=userid
        ) Order by category_name ASC;
    ELSEIF user_category = 6 then
        SELECT category_id, category_name, division_id, legal_entity_id,
        business_group_id, client_id FROM tbl_categories
        WHERE legal_entity_id in (
            SELECT legal_entity_id FROM tbl_user_legalentity
            WHERE user_id=userid
        ) Order by category_name ASC;
    ELSE
        SELECT category_id, category_name, division_id, legal_entity_id,
        business_group_id, client_id FROM tbl_categories
        WHERE category_id in (
            SELECT category_id FROM tbl_units
            WHERE category_id is not null and unit_id in (
                SELECT unit_id FROM tbl_user_units
                WHERE user_id = userid
            )
        ) Order by category_name ASC;
    END IF;
END //
DELIMITER ;


-- --------------------------------------------------------------------------------
-- To get units assigned to a user
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_units_by_user`;
DELIMITER //
CREATE PROCEDURE `sp_units_by_user`(IN userid INT(11))
BEGIN
    DECLARE user_category INT(11);
    SELECT user_category_id INTO user_category
    FROM tbl_users WHERE user_id = userid;
    IF user_category in (1,2) then
        SELECT unit_id, category_id, division_id, legal_entity_id,
        business_group_id, client_id, unit_code, unit_name,
        address, is_closed as is_active FROM tbl_units
        order by unit_name ASC;
    ELSEIF user_category = 5 THEN
        SELECT unit_id, category_id, division_id, legal_entity_id,
        business_group_id, client_id, unit_code, unit_name,
        address, is_closed as is_active FROM tbl_units
        WHERE client_id in (
            SELECT client_id FROM tbl_user_clients WHERE user_id=userid
        ) order by unit_name ASC;
    ELSEIF user_category = 6 then
        SELECT unit_id, category_id, division_id, legal_entity_id,
        business_group_id, client_id, unit_code, unit_name,
        address, is_closed as is_active FROM tbl_units
        WHERE legal_entity_id in (
            SELECT legal_entity_id FROM tbl_user_legalentity
            WHERE user_id=userid
        ) order by unit_name ASC;
    ELSE
        SELECT unit_id, category_id, division_id, legal_entity_id,
        business_group_id, client_id, unit_code, unit_name,
        address, is_closed as is_active FROM tbl_units
        WHERE unit_id in (
            SELECT unit_id FROM tbl_user_units
            WHERE user_id = userid
        ) order by unit_name ASC;
    END IF;
DELIMITER ;

-- --------------------------------------------------------------------------------
-- To verify token
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_validate_token`;

DELIMITER //
CREATE PROCEDURE `sp_validate_token`( IN token text)
BEGIN
    SELECT user_id, verification_code
    FROM tbl_email_verification
    WHERE expiry_date > current_ist_datetime() AND verification_code = token;
END //
DELIMITER ;

-- --------------------------------------------------------------------------------
-- To get details of units by unit ids to get common country, domain, organization,
-- and geography
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_unit_unit_organiation_details`;
DELIMITER //
CREATE PROCEDURE `sp_unit_unit_organiation_details`(
    IN unit_ids TEXT
)
BEGIN
    select unit_id, country_id, geography_id FROM tbl_units
    WHERE find_in_set(unit_id, unit_ids);
    select unit_id, domain_id, organisation_id FROM tbl_units_organizations
    WHERE find_in_set(unit_id, unit_ids);
END //
DELIMITER ;

-- --------------------------------------------------------------------------------
-- Note: comments before and after the routine body will not be stored by the server
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_compliances_by_unit_details`;
DELIMITER //
CREATE PROCEDURE `sp_compliances_by_unit_details`(
    IN domain_ids TEXT, country_ids TEXT, geography_ids TEXT,
    organisation_ids TEXT
)
BEGIN
    CREATE TEMPORARY TABLE statutory_mappings
    SELECT tsm.statutory_mapping_id from tbl_statutory_mappings tsm
    INNER JOIN tbl_mapped_industries tmi on (tsm.statutory_mapping_id=tmi.statutory_mapping_id)
    INNER JOIN tbl_mapped_locations tml on (tml.statutory_mapping_id=tsm.statutory_mapping_id)
    WHERE find_in_set(country_id, country_ids)
    and find_in_set(domain_id, domain_ids)
    and find_in_set(geography_id, geography_ids)
    and find_in_set(organisation_id, organisation_ids);

    SELECT compliance_id, statutory_provision, document_name, compliance_task,
    compliance_description, statutory_mapping_id
    FROM tbl_compliances WHERE  country_id in (1)
    and find_in_set(domain_id, domain_ids) and statutory_mapping_id in (
        SELECT statutory_mapping_id from statutory_mappings
    );
    SELECT statutory_mapping_id, statutory_name
    FROM tbl_mapped_statutories tms INNER JOIN tbl_statutories ts
    ON (tms.statutory_id = ts.statutory_id) INNER JOIN tbl_statutory_levels tsl
    ON (tsl.level_id = ts.level_id) WHERE level_position = 1 and
    statutory_mapping_id in (
        SELECT statutory_mapping_id from statutory_mappings
    );
    SELECT statutory_mapping_id, (
        select organisation_name FROM tbl_organisation torg
        WHERE torg.organisation_id= tmi.organisation_id
    ) as org_name  FROM tbl_mapped_industries tmi WHERE statutory_mapping_id in (
        SELECT statutory_mapping_id from statutory_mappings
    );
    SELECT statutory_mapping_id, (
        SELECT geography_name from tbl_geographies tgeo
        WHERE tgeo.geography_id = tml.geography_id
    ) as geography_name FROM tbl_mapped_locations tml
    WHERE statutory_mapping_id in (
        SELECT statutory_mapping_id from statutory_mappings
    );
    DROP TEMPORARY TABLE statutory_mappings;
END //
DELIMITER ;

-- --------------------------------------------------------------------------------
-- To get Client statutory ids by client id and unit id
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_clientstatutories_by_client_unit`;
DELIMITER //
CREATE PROCEDURE `sp_clientstatutories_by_client_unit`(
    IN clientid INT(11), unit_ids TEXT, compliance_ids TEXT
)
BEGIN
    SELECT compliance_id, domain_id FROM tbl_compliances
    WHERE find_in_set(compliance_id, compliance_ids);
    SELECT client_statutory_id, client_id, unit_id
    FROM tbl_client_statutories WHERE client_id = clientid
    AND find_in_set(unit_id, unit_ids)
    order by client_statutory_id DESC;
END //
DELIMITER ;

-- --------------------------------------------------------------------------------
-- To get list of client statutories
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_clientstatutories_list`;
DELIMITER //
CREATE PROCEDURE `sp_clientstatutories_list`()
BEGIN
    SELECT tcs.client_statutory_id, tcs.client_id, tcs.unit_id, tcs.status
    FROM tbl_client_statutories tcs;

    SELECT unit_id, tu.country_id, country_name, tu.client_id, group_name,
    tu.business_group_id, (SELECT business_group_name
    FROM tbl_business_groups tbg WHERE tbg.business_group_id=tu.business_group_id
    ) as business_group_name, tu.legal_entity_id, legal_entity_name,
    tu.division_id, (SELECT division_name
    FROM tbl_divisions td WHERE td.division_id=tu.division_id) as division_name,
    tu.category_id, (SELECT category_name FROM tbl_categories tc
    WHERE tc.category_id = tu.category_id) as category_name,
    tu.geography_id, geography_name,
    concat(tu.unit_code, " - ", tu.unit_name) as unit_name,
    (SELECT group_concat(domain_name) FROM tbl_domains td
    WHERE find_in_set(td.domain_id,tu.domain_ids)) as domain_name,
    domain_ids
    FROM tbl_units tu INNER JOIN tbl_countries tc
    ON (tc.country_id = tu.country_id) INNER JOIN tbl_legal_entities tle
    ON (tle.legal_entity_id = tu.legal_entity_id) INNER JOIN tbl_client_groups tcg
    ON tcg.client_id = tu.client_id INNER JOIN tbl_geographies tg
    ON tg.geography_id = tu.geography_id;
END //
DELIMITER ;


-- --------------------------------------------------------------------------------
-- To get the assigned compliancees by client statutory id
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_clientstatutories_by_id`;
DELIMITER //
CREATE PROCEDURE `sp_clientstatutories_by_id`(
    IN cs_id INT(11)
)
BEGIN
    SELECT DISTINCT client_compliance_id, client_statutory_id, tcc.statutory_id,
    statutory_applicable_status, tcc.remarks, tcc.compliance_id,
    compliance_applicable_status, is_saved, is_submitted,
    statutory_provision, document_name, compliance_task,
    compliance_description, tc.statutory_mapping_id, statutory_name,
    (
        select group_concat(organisation_name) FROM tbl_organisation torg
        WHERE torg.organisation_id in ( SELECT organisation_id from
        tbl_mapped_industries tmi where tmi.statutory_mapping_id=tc.statutory_mapping_id)
    ) as organisation_name,
    (
        SELECT geography_name from tbl_geographies tgeo
        WHERE tgeo.geography_id in (
            SELECT geography_id FROM tbl_mapped_locations tml
            WHERE tgeo.geography_id=tml.geography_id
        )
    ) as geography_name
    FROM tbl_client_compliances tcc INNER JOIN tbl_compliances tc
    ON tc.compliance_id = tcc.compliance_id
    INNER JOIN tbl_statutories ts ON ts.statutory_id = tcc.statutory_id
    INNER JOIN tbl_mapped_locations tml ON tml.statutory_mapping_id = tc.statutory_mapping_id
    WHERE client_statutory_id=cs_id;
END //
DELIMITER ;

-- --------------------------------------------------------------------------------
-- To crate user login details
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_tbl_user_login_details_save`;
DELIMITER //
CREATE PROCEDURE `sp_tbl_user_login_details_save`(
    IN token text, uname varchar(50), pword text
)
BEGIN
    SELECT @uid := user_id FROM tbl_email_verification WHERE verification_code = token;
    SELECT @eid := email_id, @catid := user_category_id, @isactive := is_active
    FROM tbl_users WHERE user_id = @uid;
    INSERT INTO tbl_user_login_details(
    user_id, user_category_id, email_id, username, password, is_active, created_on)
        VALUES (@uid, @catid, @eid, uname, pword, @isactive, current_ist_datetime());

    DELETE FROM tbl_email_verification where verification_code = token;
END //
DELIMITER ;

--
-- update password
--

DROP PROCEDURE IF EXISTS `sp_tbl_user_login_details_update`;
DELIMITER //
CREATE PROCEDURE `sp_tbl_user_login_details_update`(
    IN uid INT(11), pword TEXT
)
BEGIN
    UPDATE tbl_user_login_details set password = pword WHERE user_id = uid;
    SELECT username FROM tbl_user_login_details WHERE user_id = uid;
END //
DELIMITER ;

--
-- Check username availability
--
DROP PROCEDURE IF EXISTS `sp_tbl_user_login_checkusername`;
DELIMITER //
CREATE PROCEDURE `sp_tbl_user_login_checkusername`(
    IN uname varchar(50)
)
BEGIN
    SELECT count(0) as uname from tbl_user_login_details where username = uname;
END //
DELIMITER ;

--
-- Statutory maping list
--
DROP PROCEDURE IF EXISTS `sp_tbl_statutory_mapping_getlist`;
DELIMITER //
CREATE PROCEDURE `sp_tbl_statutory_mapping_getlist`(
    IN approve_sts TINYINT(5)
)
BEGIN

    SELECT T1.statutory_mapping_id, T1.country_id,
    (select country_name from tbl_countries
        where country_id = T1.country_id) as country_name,
    T1.domain_id,
    (select domain_name from tbl_domains
        where domain_id = T1.domain_id) as domain_name,
    T1.statutory_nature_id,
    (select statutory_nature_name from tbl_statutory_natures
        where statutory_nature_id = T1.statutory_nature_id) as statutory_nature_name,
    T1.is_active,
    T1.is_approved, T1.remarks,
    T2.compliance_id, T2.statutory_provision, T2.compliance_task, T2.document_name,
    T2.is_active as comp_status, T2.is_approved as comp_approved,
    T2.remarks as remarks
    FROM tbl_statutory_mappings T1
    INNER JOIN tbl_compliances T2
    ON T1.statutory_mapping_id = T2.statutory_mapping_id
    WHERE T1.is_approved = approve_sts or T2.is_approved = approve_sts;

    SELECT T1.statutory_mapping_id, T1.organisation_id, T2.organisation_name
    FROM tbl_mapped_industries T1
    INNER JOIN tbl_organisation T2 ON T1.organisation_id = T2.organisation_id;

    SELECT T1.statutory_mapping_id, T1.statutory_id, T2.statutory_name
    FROM tbl_mapped_statutories as T1
    INNER JOIN tbl_statutories as T2 ON T1.statutory_id = T2.statutory_id;

END //
DELIMITER ;

--
-- statutory mapping master data
--
DROP PROCEDURE IF EXISTS `sp_tbl_statutory_mapping_masterdata`;
DELIMITER //
CREATE PROCEDURE `sp_tbl_statutory_mapping_masterdata`(
    IN userid INT(11)
)
BEGIN
    -- 0
    select t1.country_id, t1.country_name, t1.is_active from tbl_countries as t1
    inner join tbl_user_countries as t2 on t1.country_id = t2.country_id
    and t2.user_id = userid order by country_name;
    -- 1

    select t1.domain_id, t1.country_id, t3.domain_name, t3.is_active from
    tbl_domain_countries as t1
    inner join tbl_domains as t3 on t3.domain_id = t1.domain_id
    inner join tbl_user_domains as t2 on t2.domain_id = t1.domain_id
    and t2.country_id = t1.country_id
    and t2.user_id = userid
    order by domain_name;

    -- 2

    select t1.organisation_id, t1.country_id, t1.domain_id, t1.organisation_name,
    t1.is_active from tbl_organisation as t1
    inner join tbl_user_domains as t3 on t3.domain_id = t1.domain_id
    and t3.country_id = t1.country_id
    where t3.user_id = userid
    order by organisation_name;

    -- 3
    select t1.statutory_nature_id, t1.statutory_nature_name, t1.country_id,
    t1.is_active from tbl_statutory_natures as t1
    inner join tbl_user_countries as t2 on t2.country_id = t1.country_id and
    t2.user_id = userid
    order by statutory_nature_name;
    -- 4

    select t1.geography_id, t1.geography_name, t1.level_id,
    t1.parent_ids, t1.parent_names, t1.is_active, t2.country_id,
    t2.level_position
    from tbl_geographies as t1 inner join tbl_geography_levels as t2
    on t1.level_id = t2.level_id inner join tbl_user_countries t3 on
    t3.country_id = t2.country_id where t3.user_id = userid
    order by geography_name;
    -- 5
    select t1.level_id, t1.level_position, t1.level_name,
    t1.country_id from tbl_geography_levels as t1
    inner join tbl_user_countries as t2 on t2.country_id = t1.country_id
    where t2.user_id = userid
    order by t1.level_position;
    -- 6
    select t1.level_id, t1.level_position, t1.level_name,
    t1.country_id, t1.domain_id from tbl_statutory_levels as t1
    inner join tbl_user_domains as t3 on t3.domain_id = t1.domain_id
    and t3.country_id = t1.country_id
    where  t3.user_id = userid
    order by t1.level_position;
    -- 7
    select frequency_id, frequency from tbl_compliance_frequency;
    -- 8
    select repeat_type_id, repeat_type from tbl_compliance_repeat_type;
    -- 9
    select duration_type_id, duration_type from tbl_compliance_duration_type;
END //
DELIMITER ;


DROP PROCEDURE IF EXISTS `sp_tbl_statutory_masterdata`;
DELIMITER //

CREATE  PROCEDURE `sp_tbl_statutory_masterdata`(
in userid int(11))
BEGIN
    select distinct t1.statutory_id, t1.level_id, t1.statutory_name,
    t1.parent_ids, t1.parent_names, t2.country_id, t2.domain_id,
    t2.level_position
    from tbl_statutories as t1
    inner join tbl_statutory_levels as t2 on t2.level_id = t1.level_id
    inner join tbl_user_domains as t4 on t2.domain_id = t4.domain_id and
    t2.country_id = t4.country_id and t4.user_id = userid
    order by t1.statutory_name;


END //
DELIMITER ;

DROP PROCEDURE IF EXISTS `sp_tbl_statutory_mapping_list`;
DELIMITER //
CREATE PROCEDURE `sp_tbl_statutory_mapping_list`(
    IN userid INT(11), approvestatus varchar(1),
    fromcount INT(11), tocount INT(11)
)
BEGIN
    if approvestatus = 0 then
        set approvestatus = '%';
    end if;
    select t1.statutory_mapping_id, t1.country_id, t1.domain_id, t1.statutory_nature_id,
    t1.is_active, t1.is_approved, t1.remarks,
    (select country_name from tbl_countries where country_id = t1.country_id) as country_name,
    (select domain_name from tbl_domains where domain_id = t1.domain_id) as domain_name,
    (select statutory_nature_name from tbl_statutory_natures where statutory_nature_id = t1.statutory_nature_id) as nature
    from tbl_statutory_mappings as t1
    inner join tbl_user_domains as t3 on t3.domain_id = t1.domain_id and
    t3.country_id = t1.country_id
    where t3.user_id = userid and t1.is_approved like approvestatus
    order by country_name, domain_name
    limit fromcount, tocount;

    select t1.statutory_mapping_id, t1.compliance_id, t1.compliance_task, t1.document_name,
    t1.is_active, t1.is_approved, t1.remarks
    from tbl_compliances as t1
    inner join tbl_user_domains as t3 on t3.domain_id = t1.domain_id and
    t3.country_id = t1.country_id
    where t3.user_id = userid
    order by document_name, compliance_task and t1.is_approved like approvestatus;

    select t1.statutory_mapping_id, t1.organisation_id,
    (select organisation_name from tbl_organisation where organisation_id = t1.organisation_id) as organisation_name
    from tbl_mapped_industries as t1
    inner join tbl_statutory_mappings as t2 on t1.statutory_mapping_id = t2.statutory_mapping_id
    inner join tbl_user_domains as t4 on t4.domain_id = t2.domain_id and
    t4.country_id = t2.country_id
    where t4.user_id = userid and t2.is_approved = approvestatus;

    select t1.statutory_mapping_id, t1.statutory_id,
    (select parent_names from tbl_statutories where statutory_id = t1.statutory_id) as statutory_name
    from tbl_mapped_statutories as t1
    inner join tbl_statutory_mappings as t2 on t1.statutory_mapping_id = t2.statutory_mapping_id
    inner join tbl_user_domains as t4 on t4.domain_id = t2.domain_id  and
    t4.country_id = t2.country_id
    where t4.user_id = userid and t2.is_approved = approvestatus;

    select t1.statutory_mapping_id, t1.geography_id,
    (select parent_names from tbl_geographies where geography_id = t1.geography_id) as geography_name
    from tbl_mapped_locations as t1
    inner join tbl_statutory_mappings as t2 on t1.statutory_mapping_id = t2.statutory_mapping_id
    inner join tbl_user_domains as t4 on t4.domain_id = t2.domain_id and
    t4.country_id = t2.country_id
    where t4.user_id = userid and t2.is_approved = approvestatus;

    select count(t1.statutory_mapping_id) as total
    from tbl_statutory_mappings as t1
    inner join tbl_user_domains as t3 on t3.domain_id = t1.domain_id and
    t3.country_id = t1.country_id
    where t3.user_id = userid and t1.is_approved like approvestatus
    limit fromcount, tocount;

END //
DELIMITER ;

-- --------------------------------------------------------------------------------
-- Get user category details for user mappping report
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_get_user_category_details`;
DELIMITER //

CREATE  PROCEDURE `sp_get_user_category_details`(
in userId int(11))
BEGIN
    select tuc.user_category_id, tuc.user_category_name
    from tbl_user_login_details as tu, tbl_user_category as tuc
    where
    tuc.user_category_id = tu.user_category_id and
    tu.user_id = userId;
END //
DELIMITER ;

-- --------------------------------------------------------------------------------
-- Get countries for user mapping report - for user
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_countries_for_usermapping_report`;
DELIMITER //

CREATE PROCEDURE `sp_countries_for_usermapping_report`(
in userCatgId int(11), userId int(11))
BEGIN
    if(userCatgId = 1)then
        select country_id, country_name, is_active
        from tbl_countries where
        is_active = 1;
    end if;
    if(userCatgId = 5 or userCatgId = 6 or userCatgId = 7 or userCatgId = 8)then
        select country_id, country_name, is_active
        from tbl_countries
        where country_id in
        (select country_id from tbl_user_countries
            where user_id = userId) and is_active = 1;
    end if;
END //
DELIMITER ;


-- --------------------------------------------------------------------------------
-- Get business group details for user mapping report
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_usermapping_report_business_groups`;
DELIMITER //

CREATE PROCEDURE `sp_usermapping_report_business_groups`()
BEGIN
    select business_group_id, business_group_name
    from tbl_business_groups;
END //
DELIMITER ;

-- --------------------------------------------------------------------------------
-- Get legal entity details - user mapping report
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_usermapping_report_legal_entity`;
DELIMITER //

CREATE PROCEDURE `sp_usermapping_report_legal_entity`()
BEGIN
    select legal_entity_id, legal_entity_name, business_group_id
    from tbl_legal_entities;
END //
DELIMITER ;

-- --------------------------------------------------------------------------------
-- Get unit's details, divison, category - user mapping report
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_usermapping_report_unit_details`;
DELIMITER //

CREATE PROCEDURE `sp_usermapping_report_unit_details`(
in userCatgId int(11), userId int(11))
BEGIN
    if(userCatgId = 1)then
        select tu.unit_id, concat(tu.unit_code,' - ',tu.unit_name) as unit_name,tu.client_id,
        tu.business_group_id, tu.legal_entity_id,
        tu.country_id, td.division_id, td.division_name, tc.category_id,
        tc.category_name
        from
        tbl_units as tu,
        tbl_divisions as td,
        tbl_categories as tc
        where
        tc.category_id = tu.category_id and
        td.division_id = tu.division_id and
        tu.unit_id in (select distinct(unit_id) from tbl_user_units);
    end if;
    if(userCatgId = 5 or userCatgId = 6 or userCatgId = 7 or userCatgId = 8)then
        select tu.unit_id, concat(tu.unit_code,' - ',tu.unit_name) as unit_name, tu.client_id,
        tu.business_group_id, tu.legal_entity_id,
        tu.country_id, td.division_id, td.division_name, tc.category_id,
        tc.category_name
        from
        tbl_units as tu,
        tbl_divisions as td,
        tbl_categories as tc
        where
        tc.category_id = tu.category_id and
        td.division_id = tu.division_id and
        tu.unit_id in (select distinct(unit_id) from tbl_user_units
        where user_id = userId and user_category_id = userCatgId);
    end if;
END //
DELIMITER ;

-- --------------------------------------------------------------------------------
-- Get group detais -division, category, unit for user mapping report
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_usermapping_report_group_details`;
DELIMITER //

CREATE PROCEDURE `sp_usermapping_report_group_details`(
in userCatgId int(11), userId int(11))
BEGIN
    if(userCatgId = 1)then
        select tcg.client_id, tcg.short_name as client_name, tle.legal_entity_id, tle.country_id,
        tle.business_group_id
        from tbl_legal_entities as tle,
        tbl_client_groups as tcg
        where
        tcg.client_id = tle.client_id and
        tcg.is_approved = 1 and
        tcg.is_active = 1 and
        tle.is_closed != 1;
    end if;
    if(userCatgId = 5 or userCatgId = 6)then
        select tcg.client_id, tcg.short_name as client_name, tle.legal_entity_id, tle.country_id,
        tle.business_group_id
        from tbl_legal_entities as tle,
        tbl_client_groups as tcg
        where
        tcg.client_id = tle.client_id and
        tcg.is_approved = 1 and
        tcg.is_active = 1 and
        tle.created_by = userId and
        tle.is_closed != 1;
    end if;
    if(userCatgId = 7 or userCatgId = 8)then
        select tcg.client_id, tcg.short_name as client_name, tle.legal_entity_id, tle.country_id,
        tle.business_group_id
        from
        tbl_legal_entities as tle,
        tbl_client_groups as tcg
        where
        tcg.client_id = tle.client_id and
        tcg.is_approved = 1 and
        tcg.is_active = 1 and
        tle.is_closed != 1 and
        tle.client_id in (select distinct(client_id) from tbl_user_units
        where user_id = userId);
    end if;
END//
DELIMITER ;

-- --------------------------------------------------------------------------------
-- user mapping report - report details/data
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_usermapping_report_details`;
DELIMITER //

CREATE PROCEDURE `sp_usermapping_report_details`(
    in userId int(11), clientId int(11), legalId int(11), counrtyId int(11))
BEGIN
    SELECT @_user_category_id := user_category_id as user_category_id
    FROM tbl_users WHERE user_id = userId;

    if(userId = 1)then
        select t3.unit_id, t_mgr.employee_name as techno_manager,t_usr.employee_name as techno_user
        from
        tbl_user_legalentity as t1,tbl_legal_entities as t2,tbl_users as t_mgr,
        tbl_users as t_usr,tbl_user_units as t3
        where
        case when _unit_id <> 0 then t3.unit_id = _unit_id else
        t3.unit_id = t3.unit_id end and
        t3.client_id = t1.client_id and
        t3.legal_entity_id = t1.legal_entity_id and
        t_usr.user_id = t1.user_id and
        t_mgr.user_id = t2.created_by and
        case when bgrp_id <> 0 then t2.business_group_id = bgrp_id else
        t2.business_group_id = t2.business_group_id end and
        t2.country_id = counrtyId and
        t2.client_id = t1.client_id and
        t2.legal_entity_id = t1.legal_entity_id and
        t1.legal_entity_id = legalId and
        t1.client_id = clientId
        group by t1.user_id;

        select t1.unit_id, t2.employee_name, t3.user_category_name,t1.domain_id
        from
        tbl_user_units as t1,tbl_units as t4,tbl_users as t2,
        tbl_user_category as t3
        where
        t3.user_category_id = t1.user_category_id and
        t2.user_id = t1.user_id and
        case when _cg_id <> 0 then t4.category_id = _cg_id else
        t4.category_id = t4.category_id end and
        case when _divi_id <> 0 then t4.division_id = _divi_id else
        t4.division_id = t4.division_id end and
        t4.unit_id = t1.unit_id and
        t4.country_id = counrtyId and
        case when _unit_id <> 0 then t1.unit_id = _unit_id else
        t1.unit_id = t1.unit_id end and
        t1.legal_entity_id =legalId and
        t1.client_id = clientId;

        select distinct(t3.domain_id),t3.domain_name,t3.is_active
        from
        tbl_user_units as t1,tbl_units_organizations as t2,tbl_domains as t3
        where
        t3.domain_id = t2.domain_id and
        t2.unit_id = t1.unit_id and
        case when _unit_id <> 0 then t1.unit_id = _unit_id else
        t1.unit_id = t1.unit_id end and
        t1.legal_entity_id =legalId and
        t1.client_id = clientId
        order by t3.domain_name;
    elseif (@_user_category_id = 5)then
        select t3.unit_id, t_mgr.employee_name as techno_manager,t_usr.employee_name as techno_user
        from
        tbl_user_legalentity as t1,tbl_legal_entities as t2,tbl_users as t_mgr,
        tbl_users as t_usr,tbl_user_units as t3
        where
        case when _unit_id <> 0 then t3.unit_id = _unit_id else
        t3.unit_id = t3.unit_id end and
        t3.client_id = t1.client_id and
        t3.legal_entity_id = t1.legal_entity_id and
        t_usr.user_id = t1.user_id and
        t_mgr.user_id = t2.created_by and
        t2.created_by = userId and
        case when bgrp_id <> 0 then t2.business_group_id = bgrp_id else
        t2.business_group_id = t2.business_group_id end and
        t2.country_id = counrtyId and
        t2.client_id = t1.client_id and
        t2.legal_entity_id = t1.legal_entity_id and
        t1.legal_entity_id = legalId and
        t1.client_id = clientId
        group by t1.user_id;

        select t1.unit_id, t2.employee_name, t3.user_category_name,t1.domain_id
        from
        tbl_user_units as t1,tbl_units as t4,tbl_users as t2,
        tbl_user_category as t3
        where
        t3.user_category_id = t1.user_category_id and
        t2.user_id = t1.user_id and
        case when _cg_id <> 0 then t4.category_id = _cg_id else
        t4.category_id = t4.category_id end and
        case when _divi_id <> 0 then t4.division_id = _divi_id else
        t4.division_id = t4.division_id end and
        t4.unit_id = t1.unit_id and
        t4.country_id = counrtyId and
        case when _unit_id <> 0 then t1.unit_id = _unit_id else
        t1.unit_id = t1.unit_id end and
        t1.legal_entity_id =legalId and
        t1.client_id = clientId;

        select distinct(t3.domain_id),t3.domain_name,t3.is_active
        from
        tbl_user_units as t1,tbl_units_organizations as t2,tbl_domains as t3
        where
        t3.domain_id = t2.domain_id and
        t2.unit_id = t1.unit_id and
        case when _unit_id <> 0 then t1.unit_id = _unit_id else
        t1.unit_id = t1.unit_id end and
        t1.legal_entity_id =legalId and
        t1.client_id = clientId
        order by t3.domain_name;
    elseif (@_user_category_id = 7)then
        select t3.unit_id, t_mgr.employee_name as techno_manager,t_usr.employee_name as techno_user
        from
        tbl_user_legalentity as t1,tbl_legal_entities as t2,tbl_users as t_mgr,
        tbl_users as t_usr,tbl_user_units as t3
        where
        case when _unit_id <> 0 then t3.unit_id = _unit_id else
        t3.unit_id = t3.unit_id end and
        t3.client_id = t1.client_id and
        t3.legal_entity_id = t1.legal_entity_id and
        t_usr.user_id = t1.user_id and
        t_mgr.user_id = t2.created_by and
        case when bgrp_id <> 0 then t2.business_group_id = bgrp_id else
        t2.business_group_id = t2.business_group_id end and
        t2.country_id = counrtyId and
        t2.client_id = t1.client_id and
        t2.legal_entity_id = t1.legal_entity_id and
        t1.legal_entity_id = legalId and
        t1.client_id = clientId
        group by t1.user_id;

        select t1.unit_id, t2.employee_name, t3.user_category_name,t1.domain_id
        from
        tbl_user_units as t1,tbl_units as t4,tbl_users as t2,
        tbl_user_category as t3
        where
        t3.user_category_id = t1.user_category_id and
        t2.user_id = t1.user_id and
        case when _cg_id <> 0 then t4.category_id = _cg_id else
        t4.category_id = t4.category_id end and
        case when _divi_id <> 0 then t4.division_id = _divi_id else
        t4.division_id = t4.division_id end and
        t4.unit_id = t1.unit_id and
        t4.country_id = counrtyId and
        t1.user_id = userId and
        case when _unit_id <> 0 then t1.unit_id = _unit_id else
        t1.unit_id = t1.unit_id end and
        t1.legal_entity_id =legalId and
        t1.client_id = clientId;

        select distinct(t3.domain_id),t3.domain_name,t3.is_active
        from
        tbl_user_units as t1,tbl_units_organizations as t2,tbl_domains as t3
        where
        t3.domain_id = t2.domain_id and
        t2.unit_id = t1.unit_id and
        t1.user_id = userId and
        case when _unit_id <> 0 then t1.unit_id = _unit_id else
        t1.unit_id = t1.unit_id end and
        t1.legal_entity_id =legalId and
        t1.client_id = clientId
        order by t3.domain_name;
    end if;
END//
DELIMITER;

-- --------------------------------------------------------------------------------
-- Get country based on user - report filter
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_countries_for_user_filter`;
DELIMITER //

CREATE PROCEDURE `sp_countries_for_user_filter`( IN u_id INT(11) )
BEGIN
    SELECT @u_cat_id := user_category_id from tbl_user_login_details where user_id = u_id;
    IF @u_cat_id > 2 THEN
        SELECT DISTINCT t1.country_id, t1.country_name, t1.is_active
        FROM tbl_countries t1
        INNER JOIN tbl_user_countries t2 on t1.country_id = t2.country_id
        WHERE t2.user_id = u_id
        ORDER BY t1.country_name;
    ELSE
        SELECT country_id, country_name, is_active FROM tbl_countries
        ORDER BY country_name;
    END IF;
END //
DELIMITER;

- --------------------------------------------------------------------------------
-- Get client groups based on user - report filter
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_client_groups_for_user`;
DELIMITER //

CREATE PROCEDURE `sp_client_groups_for_user`( IN u_id INT(11) )
BEGIN
    SELECT @u_cat_id := user_category_id from tbl_user_login_details where user_id = u_id;
    IF @u_cat_id > 2 THEN
        SELECT DISTINCT t1.client_id, t1.group_name,
        (
            select group_concat(country_name) from tbl_countries
            where country_id in (
            select country_id from tbl_legal_entities
            where client_id=t1.client_id)
        ) as country_names,
        (
            select count(legal_entity_id) from tbl_legal_entities
            WHERE client_id=t1.client_id
        ) as no_of_legal_entities,
        t1.is_active, t1.is_approved, t1.remarks
        FROM tbl_client_groups t1
        INNER JOIN tbl_user_clients t2 on t1.client_id = t2.client_id
        WHERE t2.user_id = u_id
        ORDER BY t1.group_name;
    ELSE
        SELECT DISTINCT t1.client_id, t1.group_name,
        (
            select group_concat(country_name) from tbl_countries
            where country_id in (
            select country_id from tbl_legal_entities
            where client_id=t1.client_id)
        ) as country_names,
        (
            select count(legal_entity_id) from tbl_legal_entities
            WHERE client_id=t1.client_id
        ) as no_of_legal_entities,
        t1.is_active, t1.is_approved, t1.remarks
        FROM tbl_client_groups t1
        ORDER BY t1.group_name;
    END IF;

    select DISTINCT l.country_id, l.client_id from tbl_legal_entities l;
END //

-- --------------------------------------------------------------------------------
-- Load Countries for client unit form
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_tbl_units_getCountries`;
DELIMITER //

CREATE PROCEDURE `sp_tbl_units_getCountries`(
in clientId int(11))
BEGIN
    select t1.country_id
    from
    tbl_user_legalentity as tul,
    tbl_legal_entities as t1,
    tbl_business_groups as t2
    where
    t2.business_group_id = t1.business_group_id and
    t2.client_id = t1.client_id and
    t1.client_id  = tul.client_id and
    tul.client_id = clientID and
    tul.user_id = userId
    group by t2.business_group_id;
END//
DELIMITER;

-- --------------------------------------------------------------------------------
-- Get geography levels for client unit
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_tbl_unit_getgeographylevels`;
DELIMITER //

CREATE PROCEDURE `sp_tbl_unit_getgeographylevels`(in userId int(11))
BEGIN
    select level_id, country_id, level_position, level_name
    from tbl_geography_levels
    where country_id in (select t2.country_id from tbl_user_legalentity as t1,
    tbl_legal_entities as t2 where t2.client_id = t1.client_id and
    t2.legal_entity_id = t1.legal_entity_id and
    t1.user_id = userId) order by level_position;
END//
-- --------------------------------------------------------------------------------
-- Get geographies for client unit
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_tbl_unit_get_geographies`;
DELIMITER //

CREATE PROCEDURE `sp_tbl_unit_get_geographies`(in userId int(11))
BEGIN
    select tg.geography_id, tg.geography_name, tg.parent_names,
    tg.level_id,tg.parent_ids, tg.is_active, tgl.country_id
    from
    tbl_geographies as tg, tbl_geography_levels as tgl
    where
        t2.level_id = t1.level_id and t2.country_id in (select t2.country_id from
        tbl_user_legalentity as t1,
        tbl_legal_entities as t2 where t2.client_id = t1.client_id and
        t2.legal_entity_id = t1.legal_entity_id and
        t1.user_id = userId);
END//
DELIMITER;

-- --------------------------------------------------------------------------------
-- to delete the domains, organization under unit id
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_tbl_units_delete_unitorganizations`;
DELIMITER //

CREATE PROCEDURE `sp_tbl_units_delete_unitorganizations`(in
unitId int(11))
BEGIN
    delete from tbl_units_organizations
    where
    unit_id in (unitId);
END//
DELIMITER;


-- --------------------------------------------------------------------------------
-- To get client details for statutory settings report
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_statutory_setting_report_clientdetails`;
DELIMITER //

CREATE PROCEDURE `sp_statutory_setting_report_clientdetails`(
in _user_id int(11))
BEGIN
    SELECT @u_cat_id := user_category_id from tbl_user_login_details where user_id = _user_id;
    IF @u_cat_id = 1  THEN
        select t1.client_id, t1.short_name, t1.is_active, t2.country_id
        from tbl_client_groups as t1, tbl_legal_entities as t2
        where t2.client_id = t1.client_id order by t1.short_name asc;
    end if;
    if @u_cat_id = 5  THEN
        select t2.client_id, t2.short_name, t2.is_active, t3.country_id
        from tbl_user_clients as t1, tbl_client_groups as t2,
        tbl_legal_entities as t3 where t3.client_id = t2.client_id and
        t2.client_id  = t1.client_id and t1.user_category_id = @u_cat_id and
        t1.user_id = _user_id;
    END IF;
    if @u_cat_id = 6  THEN
        select t3.client_id,t3.short_name,t3.is_active, t2.country_id
        from tbl_user_legalentity as t1, tbl_legal_entities as t2,
        tbl_client_groups as t3 where t3.client_id = t2.client_id and
        t2.client_id = t1.client_id and t1.user_id = _user_id  order by t3.short_name asc;
    end if;
    if @u_cat_id = 7 or @u_cat_id = 8 THEN
        select t3.client_id,t3.short_name, t3.is_active, t2.country_id
        from tbl_user_units as t1, tbl_legal_entities as t2,
        tbl_client_groups as t3 where t3.client_id = t2.client_id and
        t2.client_id = t1.client_id and t1.user_category_id = @u_cat_id
        and t1.user_id = _user_id order by t3.short_name asc;
    end if;
END//
DELIMITER;

-- --------------------------------------------------------------------------------
-- To get business group, legal entity details for statutory settings report
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_statutory_setting_report_businessgroupdetails`;
DELIMITER //

CREATE PROCEDURE `sp_statutory_setting_report_businessgroupdetails`(in _user_id int(11))
BEGIN
    SELECT @u_cat_id := user_category_id from tbl_user_login_details where user_id = _user_id;
    IF @u_cat_id = 1  THEN
        select t1.client_id, t3.business_group_id, t3.business_group_name,
        t2.legal_entity_id, t2.legal_entity_name
        from tbl_client_groups as t1, tbl_legal_entities as t2,
        tbl_business_groups as t3 where t3.business_group_id = t2.business_group_id and
        t2.client_id = t1.client_id order by t3.business_group_name asc;
    end if;
    if @u_cat_id = 5  THEN
        select t1.client_id, t3.legal_entity_id, t3.legal_entity_name, t4.business_group_id,
        t4.business_group_name from tbl_user_clients as t1,
        tbl_legal_entities as t3, tbl_business_group as t4 where
        t4.business_group_id = t3.business_group_id and
        t3.client_id  = t1.client_id and
        t1.user_category_id = @u_cat_id and t1.user_id = _user_id
        order by t4.business_group_name asc;
    END IF;
    if @u_cat_id = 6  THEN
        select t1.client_id,t2.legal_entity_id,t2.legal_entity_name,
        t3.business_group_id, t3.business_group_name
        from tbl_user_legalentity as t1, tbl_legal_entities as t2,
        tbl_business_group as t3 where t3.business_group_id = t2.business_group_id and
        t2.legal_entity_id = t1.legal_entity_id and
        t2.client_id = t1.client_id and t1.user_id = _user_id
         order by t3.business_group_name asc;
    end if;
    if @u_cat_id = 7 or @u_cat_id = 8 THEN
        select t1.client_id,t2.legal_entity_id,t2.legal_entity_name,
        t3.business_group_id, t3.business_group_name
        from tbl_user_units as t1, tbl_legal_entities as t2,
        tbl_business_group as t3 where t3.business_group_id = t2.business_group_id and
        t2.legal_entity_id = t1.legal_entity_id and
        t2.client_id = t1.client_id and t1.user_category_id = @u_cat_id
        and t1.user_id = _user_id order by t3.business_group_name asc;
    end if;
END//
DELIMITER;

-- --------------------------------------------------------------------------------
-- Routine DDL
-- Note: comments before and after the routine body will not be stored by the server
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_statutory_setting_report_unitdetails`;
DELIMITER //

CREATE PROCEDURE `sp_statutory_setting_report_unitdetails`(in _user_id int(11))
BEGIN
    SELECT @u_cat_id := user_category_id from tbl_user_login_details where user_id = _user_id;
    IF @u_cat_id = 1  THEN
        select t3.client_id, t3.legal_entity_id, t3.unit_id, t4.unit_code, t4.unit_name
        from tbl_client_groups as t1, tbl_legal_entities as t2,
        tbl_client_compliances as t3, tbl_units as t4 where t4.unit_id = t3.unit_id and
        t3.legal_entity_id = t2.legal_entity_id and
        t3.client_id = t2.client_id and t2.client_id = t1.client_id
        order by t4.unit_name asc;
    end if;
    if @u_cat_id = 5  THEN
        select t1.client_id, t2.legal_entity_id, t3.unit_id, t4.unit_code, t4.unit_name
        from tbl_user_clients as t1, tbl_legal_entities as t2,
        tbl_client_compliances as t3, tbl_units as t4 where
        t4.unit_id = t3.unit_id and t3.legal_entity_id = t2.legal_entity_id and
        t3.client_id = t2.client_id and t2.client_id  = t1.client_id and
        t1.user_category_id = @u_cat_id and t1.user_id = _user_id
        order by t4.unit_name asc;
    END IF;
    if @u_cat_id = 6  THEN
        select t1.client_id, t2.legal_entity_id, t3.unit_id, t4.unit_code, t4.unit_name
        from tbl_user_legalentity as t1, tbl_legal_entities as t2,
        tbl_client_compliances as t3, tbl_units as t4 where
        t4.unit_id = t3.unit_id and
        t3.legal_entity_id = t2.legal_entity_id and t3.client_id = t2.client_id and
        t2.client_id = t1.client_id and t1.user_id = _user_id order by t4.unit_name asc;
    end if;
    if @u_cat_id = 7 or @u_cat_id = 8 THEN
        select t1.client_id, t2.legal_entity_id, t3.unit_id, t4.unit_code, t4.unit_name
        from tbl_user_units as t1, tbl_legal_entities as t2,
        tbl_client_compliances as t3, tbl_units as t4 where
        t4.unit_id = t3.unit_id and
        t3.legal_entity_id = t2.legal_entity_id and t3.client_id = t2.client_id and
        t2.client_id = t1.client_id and t1.user_category_id = @u_cat_id
        and t1.user_id = _user_id order by t4.unit_name asc;
    end if;
END//
DELIMITER;

-- --------------------------------------------------------------------------------
-- To get compliance name, statutory name under unit
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_statutory_setting_report_domains_compliances`;
DELIMITER //

CREATE PROCEDURE `sp_statutory_setting_report_domains_compliances`(in
_user_id int(11))
BEGIN
    SELECT @u_cat_id := user_category_id from tbl_user_login_details where user_id = _user_id;
    IF @u_cat_id = 1  THEN
        select t3.client_id, t3.legal_entity_id, t3.unit_id, t3.domain_id, t3.statutory_id,
        t4.compliance_id, t4.compliance_task, t4.document_name, t5.statutory_name
        from tbl_client_groups as t1, tbl_legal_entities as t2,
        tbl_client_compliances as t3, tbl_compliances as t4, tbl_statutories as t5
        where
        t5.statutory_id = t3.statutory_id and t4.compliance_id = t3.compliance_id and
        t3.legal_entity_id = t2.legal_entity_id and
        t3.client_id = t2.client_id and t2.client_id = t1.client_id;
    end if;
    if @u_cat_id = 5  THEN
        select t3.client_id, t3.legal_entity_id, t3.unit_id, t3.domain_id, t3.statutory_id,
        t4.compliance_id, t4.compliance_task, t4.document_name, t5.statutory_name
        from tbl_user_clients as t1, tbl_legal_entities as t2,
        tbl_client_compliances as t3, tbl_compliances as t4, tbl_statutories as t5 where
        t5.statutory_id = t3.statutory_id and
        t4.compliance_id = t3.compliance_id and t3.legal_entity_id = t2.legal_entity_id and
        t3.client_id = t2.client_id and t2.client_id  = t1.client_id and
        t1.user_category_id = @u_cat_id and t1.user_id = _user_id;
    END IF;
    if @u_cat_id = 6  THEN
        select t3.client_id, t3.legal_entity_id, t3.unit_id, t3.domain_id, t3.statutory_id,
        t4.compliance_id, t4.compliance_task, t4.document_name, t5.statutory_name
        from tbl_user_legalentity as t1, tbl_legal_entities as t2,
        tbl_client_compliances as t3, tbl_compliances as t4, tbl_statutories as t5 where
        t5.statutory_id = t3.statutory_id and t4.compliance_id = t3.compliance_id and
        t3.legal_entity_id = t2.legal_entity_id and t3.client_id = t2.client_id and
        t2.client_id = t1.client_id and t1.user_id = _user_id;
    end if;
    if @u_cat_id = 7 or @u_cat_id = 8 THEN
        select t3.client_id, t3.legal_entity_id, t3.unit_id, t3.domain_id, t3.statutory_id,
        t4.compliance_id, t4.compliance_task, t4.document_name, t5.statutory_name
        from tbl_user_units as t1, tbl_legal_entities as t2,
        tbl_client_compliances as t3, tbl_compliances as t4, tbl_statutories as t5 where
        t5.statutory_id = t3.statutory_id and t4.compliance_id = t3.compliance_id and
        t3.legal_entity_id = t2.legal_entity_id and t3.client_id = t2.client_id and
        t2.client_id = t1.client_id and t1.user_category_id = @u_cat_id
        and t1.user_id = _user_id;
    end if;
END//
DELIMITER;

-- --------------------------------------------------------------------------------
-- Routine DDL
-- Note: comments before and after the routine body will not be stored by the server
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_statutory_setting_report_recordset`;
DELIMITER //

CREATE PROCEDURE `sp_statutory_setting_report_recordset`(
in _c_id int(11), _d_id int(11), _bg_id int(11), _le_id int(11), _u_id int(11),
_cl_id int(11), _st_id int(11), _cp_id int(11))
BEGIN
    select t1.unit_id, t1.unit_code, t1.unit_name, t1.address
    from
    tbl_units as t1, tbl_client_compliances as t2
    where
    t2.is_approved = 1 and
    t2.unit_id = t1.unit_id and
    case when _u_id <> 0 then t1.unit_id = _u_id else t1.unit_id = t1.unit_id end and
    case when _bg_id <> 0 then t1.business_group_id = _bg_id else t1.business_group_id = t1.business_group_id end and
    t1.legal_entity_id = _le_id and t1.client_id = _cl_id and
    t1.country_id = _c_id
    group by t1.unit_id;

    select t1.unit_id, t3.statutory_id, t3.statutory_name
    from
    tbl_client_compliances as t1, tbl_statutories as t3
    where
    t3.statutory_id = t1.statutory_id and
    case when _st_id <> 0 then t1.statutory_id = _st_id else t1.statutory_id = t1.statutory_id end and
    case when _cp_id <> 0 then t1.compliance_id = _cp_id else t1.compliance_id = t1.compliance_id end and
    case when _d_id <> 0 then t1.domain_id = _d_id else t1.domain_id = t1.domain_id end and
    case when _u_id <> 0 then t1.unit_id = _u_id else t1.unit_id = t1.unit_id end and
    t1.legal_entity_id = _le_id and t1.client_id = _cl_id
    group by t3.statutory_id;

    select t1.unit_id, t1.statutory_id, t2.statutory_provision, t2.compliance_task as c_task,
    t2.document_name, t1.remarks, t1.statutory_applicable_status as statutory_applicability_status,
    t1.statutory_opted_status, 'user@compfie.com'  as compfie_admin,
    DATE_FORMAT(t1.updated_on, '%d/%m/%Y') as admin_update,
    (select email_id from tbl_users where user_id = t1.client_opted_by) as client_admin,
    DATE_FORMAT(t1.client_opted_on, '%d/%m/%Y') as client_update,
    (select tsn.statutory_nature_name from tbl_statutory_mappings as tsm, tbl_statutory_natures as tsn
    where tsn.statutory_nature_id = tsm.statutory_nature_id and
    tsm.statutory_mapping_id = t2.statutory_mapping_id) as statutory_nature_name
    from
    tbl_client_compliances as t1, tbl_compliances as t2
    where
    t2.compliance_id = t1.compliance_id and
    t2.country_id = _c_id and
    t1.is_approved = 1 and
    case when _st_id <> 0 then t1.statutory_id = _st_id else t1.statutory_id = t1.statutory_id end and
    case when _cp_id <> 0 then t1.compliance_id = _cp_id else t1.compliance_id = t1.compliance_id end and
    case when _d_id <> 0 then t1.domain_id = _d_id else t1.domain_id = t1.domain_id end and
    case when _u_id <> 0 then t1.unit_id = _u_id else t1.unit_id = t1.unit_id end and
    t1.legal_entity_id = _le_id and t1.client_id = _cl_id
    group by t2.compliance_id;
END//
DELIMITER;

-- --------------------------------------------------------------------------------
-- Group list with legal entity count for group admin registration email
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_groupadmin_registration_email_groupslist`;
DELIMITER //

CREATE PROCEDURE `sp_groupadmin_registration_email_groupslist`(
in _user_id int(11))
BEGIN
    case when _user_id = 1 then
        SELECT @u_cat_id := user_category_id from tbl_users where user_id = _user_id;
        select t3.client_id, t3.short_name as group_name, count(t2.legal_entity_id ) as
        no_of_legal_entities, t3.group_admin_username as ug_name, t4.email_id as email_id,
        t4.user_id, concat(t4.employee_name,'-',(case when t4.employee_code is null then
            '' else t4.employee_code end)) as emp_code_name
        from
        tbl_user_clients as t1, tbl_legal_entities as t2, tbl_client_groups as t3,
        tbl_client_users as t4
        where
        t4.client_id = t3.client_id and
        t3.client_id = t2.client_id and t2.client_id = t1.client_id
        group by t2.client_id order by t3.short_name;

        select t2.client_id, t3.country_id, t3.country_name
        from tbl_user_clients as t1, tbl_legal_entities as t2, tbl_countries as t3
        where t3.country_id = t2.country_id and t2.client_id = t1.client_id;
    else
        SELECT @u_cat_id := user_category_id from tbl_users where user_id = _user_id;
        if @u_cat_id = 5 then
            select t3.client_id, t3.short_name as group_name, count(t2.legal_entity_id )
            as no_of_legal_entities, t3.group_admin_username as ug_name,
            t4.email_id as email_id, t4.user_id, concat(t4.employee_name,'-',(case when t4.employee_code is null then
            '' else t4.employee_code end)) as emp_code_name
            from
            tbl_user_clients as t1, tbl_legal_entities as t2, tbl_client_groups as t3,
            tbl_client_users as t4
            where
            t4.client_id = t3.client_id and
            t3.client_id = t2.client_id and t2.client_id = t1.client_id and
            t1.user_category_id = @u_cat_id and t1.user_id = _user_id
            group by t2.country_id order by t3.short_name;

            select t2.client_id, t3.country_id, t3.country_name
            from tbl_user_clients as t1, tbl_legal_entities as t2, tbl_countries as t3
            where t3.country_id = t2.country_id and t2.client_id = t1.client_id and
            t1.user_category_id = @u_cat_id and t1.user_id = _user_id;
        end if;
    end case;
END//
DELIMITER;

-- --------------------------------------------------------------------------------
-- Routine DDL
-- Note: comments before and after the routine body will not be stored by the server
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_groupadmin_registration_email_unitslist`;
DELIMITER //

CREATE PROCEDURE `sp_groupadmin_registration_email_unitslist`(
in _user_id int(11))
BEGIN
    case when _user_id = 1 then
        SELECT @u_cat_id := user_category_id from tbl_users where user_id = _user_id;
        select t3.client_id, t2.legal_entity_id, t2.legal_entity_name, count(t4.unit_id ) as
        unit_count, (select country_name from tbl_countries where country_id = t2.country_id) as
        country_name, (select unit_creation_informed from tbl_group_admin_email_notification where client_id =
        t2.client_id and legal_entity_id = t2.legal_entity_id) as unit_creation_informed,
        (select assign_statutory_informed from tbl_group_admin_email_notification where client_id =
        t2.client_id and legal_entity_id = t2.legal_entity_id) as statutory_assigned_informed,
        t5.email_id, t5.user_id, concat(t5.employee_name,'-',(case when t5.employee_code is null then
        '' else t5.employee_code end)) as emp_code_name,
        (select count(*) from tbl_client_statutories where client_id = t4.client_id and
        unit_id = t4.unit_id) as statutory_count
        from
        tbl_user_clients as t1, tbl_legal_entities as t2, tbl_client_groups as t3,
        tbl_units as t4, tbl_client_users as t5
        where
        t5.client_id = t3.client_id and
        t4.country_id = t2.country_id and t4.legal_entity_id = t2.legal_entity_id and
        t4.client_id = t3.client_id and t3.client_id = t2.client_id and
        t2.client_id = t1.client_id order by t2.legal_entity_name;
    else
        SELECT @u_cat_id := user_category_id from tbl_users where user_id = _user_id;
        if @u_cat_id = 5 then
            select t3.client_id, t2.legal_entity_id, t2.legal_entity_name, count(t4.unit_id ) as
            unit_count, (select country_name from tbl_countries where country_id = t2.country_id) as
            country_name, (select unit_creation_informed from tbl_group_admin_email_notification where client_id =
            t2.client_id and legal_entity_id = t2.legal_entity_id) as unit_creation_informed,
            (select assign_statutory_informed from tbl_group_admin_email_notification where client_id =
            t2.client_id and legal_entity_id = t2.legal_entity_id) as statutory_assigned_informed,
            t5.email_id, t5.user_id, concat(t5.employee_name,'-',(case when t5.employee_code is null then
            '' else t5.employee_code end)) as emp_code_name,
            (select count(*) from tbl_client_statutories where client_id = t4.client_id and
            unit_id = t4.unit_id) as statutory_count
            from
            tbl_user_clients as t1, tbl_legal_entities as t2, tbl_client_groups as t3,
            tbl_units as t4, tbl_client_users as t5
            where
            t5.client_id = t3.client_id and
            t4.country_id = t2.country_id and t4.legal_entity_id = t2.legal_entity_id and
            t4.client_id = t2.client_id and t3.client_id = t2.client_id and
            t2.client_id = t1.client_id and t1.user_category_id = @u_cat_id and
            t1.user_id = _user_id order by t2.legal_entity_name;
        end if;
    end case;
END//
DELIMITER;

-- --------------------------------------------------------------------------------
-- Insert while sending email for group admin registration email
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_tbl_groupadmin_email_notification_insert`;
DELIMITER //

CREATE PROCEDURE `sp_tbl_groupadmin_email_notification_insert`(
in _ins_mode varchar(10), _cl_id int(11), _le_id int(11), _admin_mail_id varchar(50),
_mode_creation tinyint, _mode_sent_on timestamp, _mode_sent_by int(11))
BEGIN
    if _ins_mode = 'unit' then
        insert into tbl_group_admin_email_notification
        (client_id, legal_entity_id, group_admin_email_id, unit_creation_informed,
        unit_sent_by, unit_sent_on)
        values
        (_cl_id, _le_id, _admin_mail_id, _mode_creation, _mode_sent_by, _mode_sent_on);
    end if;
    if _ins_mode = 'statutory' then
        insert into tbl_group_admin_email_notification
        (client_id, legal_entity_id, group_admin_email_id, assign_statutory_informed,
        statu_sent_by, statu_sent_on)
        values
        (_cl_id, _le_id, _admin_mail_id, _mode_creation, _mode_sent_by, _mode_sent_on);
    end if;
END//
DELIMITER;

-- --------------------------------------------------------------------------------
-- To save resend mail response from group admin registration email form
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_tbl_client_email_verification_save`;
DELIMITER //

CREATE PROCEDURE `sp_tbl_client_email_verification_save`(
    IN cl_id INT(11), e_id varchar(50), r_token TEXT, t_type INT(11), e_date datetime
)
BEGIN
    INSERT INTO tbl_client_email_verification(client_id, email_id, verification_code, verification_type_id, expiry_date)
    VALUES (cl_id, e_id, r_token, t_type, e_date);
END//
DELIMITER;

-- --------------------------------------------------------------------------------
-- To get filter data and report data of client details report
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_client_details_report_unitlist`;
DELIMITER //

CREATE PROCEDURE `sp_client_details_report_unitlist`(
in _u_id int(11))
BEGIN
    SELECT @u_cat_id := user_category_id from tbl_user_login_details where user_id = _u_id;
    IF @u_cat_id = 1  THEN
        select t3.country_id, t3.client_id, t3.legal_entity_id, t3.business_group_id,
        t3.unit_id, t3.unit_code, t3.unit_name, t3.address, t3.postal_code, t3.is_closed
        as is_active, date_format(t3.closed_on, '%d/%m/%Y') as closed_on,
        date_format(t3.created_on, '%d-%b-%Y') as check_date,
        (select concat(employee_code,'-',employee_name) from tbl_users
        where user_id = t3.created_by)as emp_code_name,
        date_format(t3.created_on, '%d/%m/%Y') as created_on,
        (select division_name from tbl_divisions where
        division_id = t3.division_id) as division_name,
        (select category_name from tbl_categories where
        category_id = t3.category_id) as category_name
        from tbl_client_groups as t1, tbl_legal_entities as t2,
        tbl_units as t3 where
        t3.legal_entity_id = t2.legal_entity_id and
        t3.client_id = t2.client_id and t2.client_id = t1.client_id
        order by t3.unit_name asc;
    end if;
    if @u_cat_id = 5  THEN
        select t3.country_id, t3.client_id, t3.legal_entity_id, t3.business_group_id,
        t3.unit_id, t3.unit_code, t3.unit_name, t3.address, t3.postal_code, t3.is_closed
        as is_active, date_format(t3.closed_on, '%d/%m/%Y') as closed_on,
        date_format(t3.created_on, '%d-%b-%Y') as check_date,
        (select concat(employee_code,'-',employee_name) from tbl_users
        where user_id = t3.created_by)as emp_code_name,
        date_format(t3.created_on, '%d/%m/%Y') as created_on,
        (select division_name from tbl_divisions where
        division_id = t3.division_id) as division_name,
        (select category_name from tbl_categories where
        category_id = t3.category_id) as category_name
        from tbl_user_clients as t1, tbl_legal_entities as t2,
        tbl_units as t3 where
        t3.legal_entity_id = t2.legal_entity_id and
        t3.client_id = t2.client_id and t2.client_id = t1.client_id
        and user_id = _u_id
        order by t3.unit_name asc;
    END IF;
    if @u_cat_id = 6  THEN
        select t3.country_id, t3.client_id, t3.legal_entity_id, t3.business_group_id,
        t3.unit_id, t3.unit_code, t3.unit_name, t3.address, t3.postal_code, t3.is_closed
        as is_active, date_format(t3.closed_on, '%d/%m/%Y') as closed_on,
        date_format(t3.created_on, '%d-%b-%Y') as check_date,
        (select concat(employee_code,'-',employee_name) from tbl_users
        where user_id = t3.created_by)as emp_code_name,
        date_format(t3.created_on, '%d/%m/%Y') as created_on,
        (select division_name from tbl_divisions where
        division_id = t3.division_id) as division_name,
        (select category_name from tbl_categories where
        category_id = t3.category_id) as category_name
        from tbl_user_legalentity as t1, tbl_legal_entities as t2,
        tbl_units as t3 where
        t3.legal_entity_id = t2.legal_entity_id and
        t3.client_id = t2.client_id and t2.client_id = t1.client_id
        and user_id = _u_id
        order by t3.unit_name asc;
    end if;
    if @u_cat_id = 7 or @u_cat_id = 8 THEN
        select t3.country_id, t3.client_id, t3.legal_entity_id, t3.business_group_id,
        t3.unit_id, t3.unit_code, t3.unit_name, t3.address, t3.postal_code, t3.is_closed
        as is_active, date_format(t3.closed_on, '%d/%m/%Y') as closed_on,
        date_format(t3.created_on, '%d-%b-%Y') as check_date,
        (select concat(employee_code,'-',employee_name) from tbl_users
        where user_id = t3.created_by)as emp_code_name,
        date_format(t3.created_on, '%d/%m/%Y') as created_on,
        (select division_name from tbl_divisions where
        division_id = t3.division_id) as division_name,
        (select category_name from tbl_categories where
        category_id = t3.category_id) as category_name
        from tbl_user_units as t1, tbl_legal_entities as t2,
        tbl_units as t3 where
        t3.legal_entity_id = t2.legal_entity_id and
        t3.client_id = t2.client_id and t2.client_id = t1.client_id
        and user_id = _u_id and user_category_id = @u_cat_id
        order by t3.unit_name asc;

    end if;

    select t3.unit_id, t3.domain_id, t3.organisation_id
    from
    tbl_units as t2, tbl_units_organizations as t3
    where
    t3.unit_id = t2.unit_id;
END//
DELIMITER;

-- --------------------------------------------------------------------------------
-- To get data for group admin registration report
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_group_admin_registration_email_report_data`;
DELIMITER //

CREATE PROCEDURE `sp_group_admin_registration_email_report_data`(
in _u_id int(11))
BEGIN
    if _u_id = 1 then
        select t2.client_id, t2.short_name as group_name, t2.is_active
        from
        tbl_user_clients as t1, tbl_client_groups as t2
        where
        t2.client_id = t1.client_id
        order by t2.short_name;

        select t1.client_id, t3.country_id, t3.country_name, t3.is_active
        from
        tbl_user_clients as t1, tbl_legal_entities as t2, tbl_countries as t3
        where
        t3.country_id = t2.country_id and
        t2.client_id = t1.client_id
        order by t3.country_name;

        select t2.client_id, t2.legal_entity_id, t2.legal_entity_name, count(t4.unit_id ) as
        unit_count, t2.country_id, (select country_name from tbl_countries where country_id =
        t2.country_id) as country_name, (select date_format(unit_sent_on, '%d/%m/%y %h:%i')
        from tbl_group_admin_email_notification where client_id = t2.client_id and
        legal_entity_id = t2.legal_entity_id) as unit_email_date,
        (select date_format(statu_sent_on, '%d/%m/%y %h:%i') from tbl_group_admin_email_notification
        where client_id = t2.client_id and legal_entity_id = t2.legal_entity_id) as
        statutory_email_date
        from
        tbl_user_clients as t1, tbl_legal_entities as t2, tbl_units as t4
        where
        t4.country_id = t2.country_id and t4.legal_entity_id = t2.legal_entity_id and
        t4.client_id = t2.client_id and
        t2.client_id = t1.client_id order by t2.legal_entity_name;
    end if;
END//
DELIMITER;

-- --------------------------------------------------------------------------------
-- get rreassign user report filters
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_reassignuser_report_usercategories`;
DELIMITER //

CREATE PROCEDURE `sp_reassignuser_report_usercategories`()
BEGIN
    select user_category_id, user_category_name from tbl_user_category
    where user_category_id > 2 and user_category_name != 'Knowledge Manager' and
    user_category_name != 'Knowledge Executive';

    select user_category_id, user_id, concat(employee_name,' - ',employee_code) as
    emp_code_name from tbl_users where is_active = 1;

    (select client_id, user_id from tbl_user_clients
    where user_id in
    (select user_id from tbl_users))
    union
    (select client_id, user_id from tbl_user_legalentity
    where user_id in
    (select user_id from tbl_users))
    union
    (select client_id, user_id from tbl_user_units
    where user_id in
    (select user_id from tbl_users));

    select client_id, short_name, is_active
    from tbl_client_groups;

END//
DELIMITER;

-- --------------------------------------------------------------------------------
-- To get reassign user report data
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_reassign_user_report_getdata`;
DELIMITER //

CREATE PROCEDURE `sp_reassign_user_report_getdata`(
in _u_id int(11), _u_cg_id int(11), _g_id int(11))
BEGIN
    if _u_cg_id = 5 then
        select t1.client_id, t2.short_name as group_name,
        date_format(t3.assigned_on, '%d-%b-%y') as assigned_on,
        concat(t4.employee_code,'-',t4.employee_name) as emp_code_name,
        t3.remarks, (select count(*) from tbl_legal_entities where
        client_id = t1.client_id) as le_count
        from
        tbl_user_clients as t1,
        tbl_client_groups as t2,
        tbl_user_account_reassign_history as t3,
        tbl_users as t4
        where
        t4.user_id = t3.assigned_by and
        t3.reassinged_data = t1.client_id and
        t2.client_id = t1.client_id and
        (case when _g_id <> 0 then t1.client_id = _g_id else t1.client_id = t1.client_id end) and
        t1.user_id = _u_id;

        select t2.client_id, t3.country_id, t3.country_name
        from tbl_user_clients as t1, tbl_legal_entities as t2, tbl_countries as t3
        where t3.country_id = t2.country_id and t2.client_id = t1.client_id and
        (case when _g_id <> 0 then t1.client_id = _g_id else t1.client_id = t1.client_id end) and
        t1.user_id = _u_id;
    end if;
    if _u_cg_id =  6 then
        select t1.client_id, t2.short_name as group_name,
        date_format(t3.assigned_on, '%d-%b-%y') as assigned_on,
        concat(t4.employee_code,'-',t4.employee_name) as emp_code_name,
        t3.remarks, (select count(*) from tbl_legal_entities where
        client_id = t1.client_id) as le_count
        from
        tbl_user_legalentity as t1,
        tbl_client_groups as t2,
        tbl_user_account_reassign_history as t3,
        tbl_users as t4
        where
        t4.user_id = t3.assigned_by and
        t3.reassinged_data = t1.client_id and
        t2.client_id = t1.client_id and
        (case when _g_id <> 0 then t1.client_id = _g_id else t1.client_id = t1.client_id end) and
        t1.user_id = _u_id;

        select t2.client_id, t3.country_id, t3.country_name
        from tbl_user_legalentity as t1, tbl_legal_entities as t2, tbl_countries as t3
        where t3.country_id = t2.country_id and t2.client_id = t1.client_id and
        (case when _g_id <> 0 then t1.client_id = _g_id else t1.client_id = t1.client_id end) and
        t1.user_id = _u_id;
    end if;
    if _u_cg_id = 7 or _u_cg_id = 8 then
        select t1.client_id, t2.short_name as group_name,
        date_format(t3.assigned_on, '%d-%b-%y') as assigned_on,
        concat(t4.employee_code,'-',t4.employee_name) as emp_code_name,
        t3.remarks, (select count(*) from tbl_legal_entities where
        client_id = t1.client_id) as le_count
        from
        tbl_user_units as t1,
        tbl_client_groups as t2,
        tbl_user_account_reassign_history as t3,
        tbl_users as t4
        where
        t4.user_id = t3.assigned_by and
        t3.reassinged_data = t1.unit_id and
        t2.client_id = t1.client_id and
        (case when _g_id <> 0 then t1.client_id = _g_id else t1.client_id = t1.client_id end) and
        t1.user_id = _u_id and
        t1.user_category_id = _u_cg_id;

        select t2.client_id, t3.country_id, t3.country_name
        from tbl_user_units as t1, tbl_legal_entities as t2, tbl_countries as t3
        where t3.country_id = t2.country_id and t2.client_id = t1.client_id and
        (case when _g_id <> 0 then t1.client_id = _g_id else t1.client_id = t1.client_id end) and
        t1.user_id = _u_id and t1.user_category_id = _u_cg_id;
    end if;
END//
DELIMITER;

-- --------------------------------------------------------------------------------
-- To get closed details legal entity table
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_legalenity_closure_list`;
DELIMITER //

CREATE PROCEDURE `sp_legalenity_closure_list`(
in _u_id int(11))
BEGIN
    select t1.client_id, t2.legal_entity_id, t2.is_closed as is_active, t2.closed_on,
    (case when t2.closed_on is not null then
    DATEDIFF(NOW(), t2.closed_on) else 0 end) as validity_days,
    (select short_name from tbl_client_groups where client_id = t1.client_id) as
    group_name,
    (select business_group_name from tbl_business_groups where business_group_id =
    t2.business_group_id) as business_group_name,
    t2.legal_entity_name, (select country_name from tbl_countries where country_id =
    t2.country_id) as country_name
    from
    tbl_user_clients as t1, tbl_legal_entities as t2
    where
    t2.client_id  = t1.client_id and t1.user_id = _u_id;
END//
DELIMITER;

-- --------------------------------------------------------------------------------
-- To update closed details in legal entity table
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_legalentity_closure_save`;
DELIMITER //

CREATE PROCEDURE `sp_legalentity_closure_save`(
in _u_id int(11), _le_id int(11), _is_cl tinyint(1), _cl_on timestamp, _rem varchar(500))
BEGIN
    update tbl_legal_entities
    set is_closed = _is_cl, closed_on = _cl_on, closed_by = _u_id,
    closed_remarks = _rem where
    legal_entity_id = _le_id;
END//
DELIMITER;

-- --------------------------------------------------------------------------------
-- To veryfy user password
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_verify_password`;
DELIMITER //

CREATE PROCEDURE `sp_verify_password`(
IN userid_ INT(11), password_ VARCHAR(50)
)
BEGIN
    SELECT
        count(u.user_id) as count
    FROM
        tbl_user_login_details u
    WHERE
        u.user_id = userid_ AND u.password = password_ AND u.is_active = 1;

END//
DELIMITER;

-- --------------------------------------------------------------------------------
-- Routine DDL
-- Note: comments before and after the routine body will not be stored by the server
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_geographymaster_report_data`;
DELIMITER //

CREATE PROCEDURE `sp_geographymaster_report_data`()
BEGIN
    SELECT t1.geography_id, t1.geography_name, t1.parent_names, t1.is_active,
    (select distinct country_id FROM tbl_geography_levels
    where level_id = t1.level_id) country_id,
         (select level_position FROM tbl_geography_levels
         where level_id = t1.level_id) position
         FROM tbl_geographies t1
         ORDER BY position, parent_names, geography_name;
END//
DELIMITER;

-- --------------------------------------------------------------------------------
-- Routine DDL
-- Note: comments before and after the routine body will not be stored by the server
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_geographymaster_geographies_list`;
DELIMITER //

CREATE PROCEDURE `sp_geographymaster_geographies_list`(
in countryId int(11))
BEGIN
    if countryId is not null then
        SELECT distinct t1.geography_id, t1.geography_name, t1.level_id,
        t1.parent_ids, t1.is_active, t2.country_id,
            (select country_name from tbl_countries where country_id = t2.country_id)
            as country_name, t2.level_position, t1.parent_names FROM tbl_geographies t1
            INNER JOIN tbl_geography_levels t2 on t1.level_id = t2.level_id
            AND t2.country_id=countryId
            ORDER BY country_name, level_position, geography_name;
    else
        SELECT distinct t1.geography_id, t1.geography_name, t1.level_id,
        t1.parent_ids, t1.is_active, t2.country_id,
            (select country_name from tbl_countries where country_id = t2.country_id)
            as country_name, t2.level_position, t1.parent_names FROM tbl_geographies t1
            INNER JOIN tbl_geography_levels t2 on t1.level_id = t2.level_id
            ORDER BY country_name, level_position, geography_name;
    end if;
END//
DELIMITER;

-- --------------------------------------------------------------------------------
<<<<<<< HEAD
-- update knowledge user view profile
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_update_profile`;
DELIMITER //

CREATE PROCEDURE `sp_update_profile`(
IN contactno_ VARCHAR(20), IN address_ VARCHAR(250),
    IN mobileno_ VARCHAR(20), IN emailid_ VARCHAR(100), IN userid_ INT(11)
)
BEGIN
    UPDATE tbl_users set contact_no = contactno_, address = address_,
    mobile_no = mobileno_, email_id = emailid_  WHERE user_id= userid_;
    UPDATE tbl_user_login_details set email_id = emailid_  WHERE user_id= userid_;
END//
DELIMITER;

-- --------------------------------------------------------------------------------
-- get knowledge users message list
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_get_messages`;
DELIMITER //

CREATE PROCEDURE `sp_get_messages`(
IN fromcount_ INT(11), IN pagecount_ INT(11), IN userid_ INT(11)
)
BEGIN
    SELECT @u_cat_id := user_category_id from tbl_user_login_details where user_id = 1;

    SELECT m.message_id, m.message_heading, m.message_text, m.link,
    (SELECT concat(employee_code, ' - ', employee_name)
    from tbl_users where user_id = m.created_by) as created_by,
    m.created_on
    from tbl_messages m INNER JOIN tbl_message_users mu ON mu.message_id = m.message_id
    AND mu.user_id = userid_
    where m.user_category_id = @u_cat_id
    order by created_on DESC limit pagecount_;
END//
DELIMITER;

-- --------------------------------------------------------------------------------
-- get knowledge users statutory notification list
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_get_statutory_notifications`;
DELIMITER //

CREATE PROCEDURE `sp_get_statutory_notifications`(
IN fromcount_ INT(11), IN pagecount_ INT(11), IN userid_ INT(11)
)
BEGIN
    SELECT s.notification_id, s.compliance_id, s.notification_text,
    (SELECT concat(employee_code, ' - ', employee_name)
    from tbl_users where user_id = s.created_by) as created_by,
    s.created_on, su.user_id, su.read_status
    from tbl_statutory_notifications s INNER JOIN tbl_statutory_notifications_users su ON su.notification_id = s.notification_id
    AND su.user_id = userid_
    order by su.read_status DESC, s.created_on DESC limit pagecount_;
END//
DELIMITER;

-- --------------------------------------------------------------------------------
-- update knowledge users statutory notification list read status
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_statutory_notification_read_status`;
DELIMITER //
CREATE PROCEDURE `sp_statutory_notification_read_status`(
    IN notificationid_ INT(11), userid_ INT(11), readstatus_ TINYINT(2)
)
BEGIN
    UPDATE tbl_statutory_notifications_users set read_status = readstatus_
    WHERE notification_id=notificationid_ AND user_id = userid_;
END //
DELIMITER ;

-- --------------------------------------------------------------------------------
-- Get Statutory level details
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_statutorymapping_report_levl1_list`;
DELIMITER //

CREATE PROCEDURE `sp_statutorymapping_report_levl1_list`()
BEGIN
	SELECT t1.statutory_id, t1.statutory_name, t1.level_id, t1.parent_ids, t2.country_id,
	t3.country_name, t2.domain_id, t4.domain_name FROM tbl_statutories t1
	INNER JOIN tbl_statutory_levels t2 on t1.level_id = t2.level_id
	INNER JOIN tbl_countries t3 on t2.country_id = t3.country_id
	INNER JOIN tbl_domains t4 on t2.domain_id = t4.domain_id
	WHERE t2.level_position=1;
END//
DELIMITER;

-- --------------------------------------------------------------------------------
-- Routine DDL
-- Note: comments before and after the routine body will not be stored by the server
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_statutorymapping_report_statutorymaster`;
DELIMITER //

CREATE PROCEDURE `sp_statutorymapping_report_statutorymaster`(
in statutoryId int(11))
BEGIN
	if statutoryId is not null then
		SELECT t1.statutory_id, t1.statutory_name, t1.level_id, t1.parent_ids, t2.country_id,
		t3.country_name, t2.domain_id, t4.domain_name FROM tbl_statutories t1
		INNER JOIN tbl_statutory_levels t2 on t1.level_id = t2.level_id
		INNER JOIN tbl_countries t3 on t2.country_id = t3.country_id
		INNER JOIN tbl_domains t4 on t2.domain_id = t4.domain_id
		where t1.statutory_id = statutoryId;
	else
		SELECT t1.statutory_id, t1.statutory_name, t1.level_id, t1.parent_ids, t2.country_id,
		t3.country_name, t2.domain_id, t4.domain_name FROM tbl_statutories t1
		INNER JOIN tbl_statutory_levels t2 on t1.level_id = t2.level_id
		INNER JOIN tbl_countries t3 on t2.country_id = t3.country_id
		INNER JOIN tbl_domains t4 on t2.domain_id = t4.domain_id;
	end if;
END//
DELIMITER;

-- --------------------------------------------------------------------------------
-- countries list for audir trail
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_countries_for_audit_trails`;
DELIMITER //

CREATE PROCEDURE `sp_countries_for_audit_trails`()
BEGIN
	select t1.user_id, t1.country_id,
	(select user_category_id from tbl_users where user_id = t1.user_id) as user_category_id,
	(select country_name from tbl_countries where country_id = t1.country_id) as country_name
	from
	tbl_user_countries as t1;

	SELECT form_id, form_name FROM tbl_forms WHERE form_id != 26;

	SELECT user_id, user_category_id, employee_name, employee_code, is_active
	FROM tbl_users;

	SELECT user_id, form_id, action, created_on FROM tbl_activity_log;
END//
DELIMITER;

DROP PROCEDURE IF EXISTS `sp_tbl_geography_levels_getlist`;
DELIMITER //

CREATE PROCEDURE `sp_tbl_geography_levels_getlist`()
BEGIN
    select level_id, level_position, level_name, country_id from
    tbl_geography_levels order by level_position;

END//
DELIMITER;

<<<<<<< HEAD
-- update knowledge user view profile
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_update_profile`;
DELIMITER //

CREATE PROCEDURE `sp_update_profile`(
IN contactno_ VARCHAR(20), IN address_ VARCHAR(250),
    IN mobileno_ VARCHAR(20), IN emailid_ VARCHAR(100), IN userid_ INT(11)
)
BEGIN
    UPDATE tbl_users set contact_no = contactno_, address = address_,
    mobile_no = mobileno_, email_id = emailid_  WHERE user_id= userid_;
    UPDATE tbl_user_login_details set email_id = emailid_  WHERE user_id= userid_;
END//
DELIMITER;

-- --------------------------------------------------------------------------------
-- Get geography levels from master
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_get_geography_levels`;
DELIMITER //

CREATE PROCEDURE `sp_get_geography_levels`()
BEGIN
    select level_id, level_name, level_position, country_id
    from tbl_geography_levels
    order by level_position;
END//
DELIMITER;
-- --------------------------------------------------------------------------------
-- Check levels in geography master
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_check_level_in_geographies`;
DELIMITER //

CREATE PROCEDURE `sp_check_level_in_geographies`(
    in levelId int(11))
BEGIN
    select count(*) from tbl_geographies where
    level_id = levelId;
END//
DELIMITER;
-- --------------------------------------------------------------------------------
-- delete level from geography level master
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_delete_geographylevel`;
DELIMITER //

CREATE PROCEDURE `sp_delete_geographylevel`(
    in levelId int(11))
BEGIN
    delete from tbl_geography_levels where
    level_id = levelId;
END//
DELIMITER;
-- --------------------------------------------------------------------------------
-- Save geography levels under country id
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_save_geographylevel_master`;
DELIMITER //

CREATE PROCEDURE `sp_save_geographylevel_master`(
    in _level_name varchar(50), _level_position int(11),
    _country_id int(11), _created_by int(11), _created_on datetime)
BEGIN
    insert into tbl_geography_levels
    (level_name, level_position, country_id, created_by, created_on)
    values
    (_level_name, _level_position, _country_id, _created_by, _created_on);

END //
DELIMITER;
-- --------------------------------------------------------------------------------
-- To update geography level under level id
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_update_geographylevel_master`;
DELIMITER //

CREATE PROCEDURE `sp_update_geographylevel_master`(
    in _level_id int(11), _level_name varchar(50), _level_position int(11),
    _updated_by int(11))
BEGIN
    update tbl_geography_levels
    set level_name  = _level_name, level_position = _level_position,
    updated_by = _updated_by where
    level_id = _level_id;
END//
DELIMITER;


DROP PROCEDURE IF EXISTS `sp_tbl_statutory_mapping_approve_list`;
DELIMITER //
CREATE PROCEDURE `sp_tbl_statutory_mapping_approve_list`(
    IN userid INT(11)
)
BEGIN

    select t1.statutory_mapping_id, t1.statutory_mapping, t2.compliance_id, t2.country_id, t2.domain_id, t2.document_name,
        t2.compliance_task, t2.is_active, t2.created_by, t2.created_on, t2.updated_by, t2.updated_on,
        t4.statutory_nature_name,
        t2.statutory_provision,
        t2.compliance_description, t2.penal_consequences, t2.reference_link, t2.frequency_id,
        t2.statutory_dates, t2.repeats_type_id, t2.repeats_every, t2.duration_type_id,
        t2.duration,
        (select frequency from tbl_compliance_frequency where frequency_id = t2.frequency_id) as freq_name,
        (select repeat_type from tbl_compliance_repeat_type where repeats_type_id = t2.repeats_type_id) as repeat_type,
        (select duration_type from tbl_compliance_duration_type where duration_type_id = t2.duration_type_id) as duration,
        (select concat(employee_code, ' - ', employee_name) from tbl_users where user_id = t2.created_by) as created_by,
        (select concat(employee_code, ' - ', employee_name) from tbl_users where user_id = t2.updated_by) as updated_by
     from tbl_statutory_mappings as t1
     inner join tbl_compliances as t2 on t1.statutory_mapping_id = t2.statutory_mapping_id
     inner join tbl_mapped_industries as t3 on t1.statutory_mapping_id = t3.statutory_mapping_id
     inner join tbl_statutory_natures as t4 on t1.statutory_nature_id = t4.statutory_nature_id
     inner join tbl_user_domains as t5 on t5.country_id = t2.country_id and t5.domain_id = t2.domain_id
     where t2.is_approved = 1 and t5.user_id = userid and IFNULL(t2.updated_by, t2.created_by) in (
        select child_user_id from tbl_user_mapping where parent_user_id = userid
     ) order by t1.statutory_mapping_id;

     select distinct t.organisation_name, t1.statutory_mapping_id from tbl_organisation as t
     inner join tbl_mapped_industries as t1 on t1.organisation_id = t.organisation_id
     inner join tbl_compliances as t2 on t1.statutory_mapping_id = t2.statutory_mapping_id
     inner join tbl_user_domains as t3 on t3.country_id = t2.country_id and t3.domain_id = t2.domain_id
     where t2.is_approved = 1 and t3.user_id = userid and  IFNULL(t2.updated_by, t2.created_by) in (
        select child_user_id from tbl_user_mapping where parent_user_id = userid
     ) order by t1.statutory_mapping_id;

     SELECT distinct t1.geography_name, t1.parent_names, t2.statutory_mapping_id from tbl_geographies as t1
        inner join tbl_mapped_locations as t2 on t2.geography_id = t1.geography_id
        inner join tbl_compliances as t3 on t3.statutory_mapping_id = t2.statutory_mapping_id
    inner join tbl_user_domains as t5 on t5.country_id = t3.country_id and t5.domain_id = t3.domain_id
    where t3.is_approved = 1 and t5.user_id = userid and IFNULL(t3.updated_by, t3.created_by) in (
        select child_user_id from tbl_user_mapping where parent_user_id = userid
     ) order by t3.statutory_mapping_id;


END //

DELIMITER ;




DROP PROCEDURE IF EXISTS `sp_tbl_statutory_mapping_approve_list_filter`;
DELIMITER //

CREATE PROCEDURE `sp_tbl_statutory_mapping_approve_list_filter`(
    IN userid INT(11), org_id VARCHAR(100), nature_id VARCHAR(100),
    countryid INT(11), domainid INT(11), knowledge_user_id VARCHAR(100)
)
BEGIN
    select distinct t1.statutory_mapping_id, t1.statutory_mapping, t2.compliance_id, t2.country_id, t2.domain_id, t2.document_name,
        t2.compliance_task, t2.is_active, t2.created_on, t2.updated_on,
        t4.statutory_nature_name,
        (select concat(employee_code, ' - ', employee_name) from tbl_users where user_id = t2.created_by) as created_by,
        (select concat(employee_code, ' - ', employee_name) from tbl_users where user_id = t2.updated_by) as updated_by
     from tbl_statutory_mappings as t1
     inner join tbl_compliances as t2 on t1.statutory_mapping_id = t2.statutory_mapping_id
     inner join tbl_statutory_natures as t4 on t1.statutory_nature_id = t4.statutory_nature_id
     inner join tbl_user_domains as t5 on t5.country_id = t2.country_id and t5.domain_id = t2.domain_id
     where t2.is_approved = 1 and t5.user_id = userid
     and t2.country_id = countryid
     and t2.domain_id = domainid
     and t1.statutory_nature_id like nature_id
     and IFNULL(t2.updated_by, t2.created_by) in (
        select child_user_id from tbl_user_mapping where parent_user_id = 4
     ) order by t1.statutory_mapping_id;

     select distinct t.organisation_name, t1.statutory_mapping_id from tbl_organisation as t
     inner join tbl_mapped_industries as t1 on t1.organisation_id = t.organisation_id
     inner join tbl_compliances as t2 on t1.statutory_mapping_id = t2.statutory_mapping_id
     inner join tbl_user_domains as t3 on t3.country_id = t2.country_id and t3.domain_id = t2.domain_id
     where t2.is_approved = 1 and t3.user_id = userid
     and t2.country_id = countryid
     and t2.domain_id = domainid
     and t1.organisation_id like org_id
     and IFNULL(t2.updated_by, t2.created_by) in (
        select child_user_id from tbl_user_mapping where parent_user_id = userid
     ) order by t1.statutory_mapping_id;

END //

DELIMITER ;


DROP PROCEDURE IF EXISTS `sp_tbl_statutory_mapping_compliance`;
DELIMITER //
CREATE PROCEDURE `sp_tbl_statutory_mapping_compliance`(
    IN compid INT(11)
)
BEGIN
    SELECT t1.compliance_id, t1.statutory_mapping_id, t1.country_id,
        t1.domain_id, t1.statutory_provision, t1.compliance_task, t1.document_name,
        t1.compliance_description, t1.penal_consequences, t1.reference_link, t1.frequency_id,
        t1.statutory_dates, t1.repeats_type_id, t1.repeats_every, t1.duration_type_id,
        t1.duration, t1.is_active,
        (select frequency from tbl_compliance_frequency where frequency_id = t1.frequency_id) as freq_name,
        (select repeat_type from tbl_compliance_repeat_type where repeats_type_id = t1.repeats_type_id) as repeat_type,
        (select duration_type from tbl_compliance_duration_type where duration_type_id = t1.duration_type_id) as duration
    FROM tbl_compliances as t1 inner join tbl_statutory_mappings as t2
    on t1.statutory_mapping_id = t2.statutory_mapping_id
    where t1.compliance_id = compid;

    SELECT t1.geography_name, t1.parent_names from tbl_geographies as t1
    inner join tbl_mapped_locations as t2 on t2.geography_id = t1.geography_id
    inner join tbl_compliances as t3 on t3.statutory_mapping_id = t2.statutory_mapping_id
    where t3.compliance_id = compid;
END //

DELIMITER ;


DROP PROCEDURE IF EXISTS `sp_tbl_statutory_mapping_approve`;
DELIMITER //
CREATE PROCEDURE `sp_tbl_statutory_mapping_approve`(
    IN compid INT(11), mapid INT(11), country VARCHAR(100), domain VARCHAR(100),
    nature VARCHAR(100), mapping TEXT, cname TEXT, asts INT(11), rmarks TEXT,
    isCommon tinyint(2), userid INT(11),
)
BEGIN

    IF isCommon = 0 then
        update tbl_compliances set is_approved = asts,
            approved_by = userid, approved_on = current_ist_datetime(),
            remarks = rmarks
        where compliance_id = compid;
    ELSE
        update tbl_compliances set is_approved = asts,
            approved_by = userid, approved_on = current_ist_datetime()
        where compliance_id = compid;

        update tbl_statutory_mappings set is_approved = asts,
            approved_by = userid,remarks = rmarks
        where compliance_id = compid;

        INSERT INTO tbl_messages(user_category_id, message_heading, message_text,
            link, updated_by, updated_on)
        values ()

    END IF;

END //

DELIMITER ;


DROP PROCEDURE IF EXISTS `sp_tbl_users_to_notify`;
DELIMITER //
CREATE PROCEDURE `sp_tbl_users_to_notify`(
    IN usercategoryid INT(11)
)
BEGIN

    select user_id from tbl_users where
    is_active = 1 and is_disable = 0 and
    user_category_id in (1, 3, 4, 5, 7, 8)

END //

DELIMITER ;


DROP PROCEDURE IF EXISTS `sp_user_knowledge_executives`;
DELIMITER //
CREATE PROCEDURE `sp_user_knowledge_executives`(
    IN userid INT(11)
)
BEGIN
    select child_user_id, concat(employee_code, '-', employee_name) as emp_name from  tbl_user_mapping
    inner join tbl_users on user_id = child_user_id and is_active = 1 and is_disable = 0
    where parent_user_id = userid ;


END //

DELIMITER ;
