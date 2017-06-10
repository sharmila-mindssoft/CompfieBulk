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
    SELECT @_user_id := user_id as user_id, username, @_user_category_id := user_category_id as user_category_id from tbl_user_login_details where username = uname ;
    SELECT user_id, user_category_id
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
        T1.email_id, T1.contact_no, T1.mobile_no, T1.is_disable,
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
                when @_user_category_id=7 and category_id_7 = 1 then 47
                when @_user_category_id=8 and category_id_8 = 1 then 47
                end as form_notify
                from tbl_form_category
                where form_id = 47
        );

    end if;

    SELECT count(1) as m_count from tbl_messages m
    INNER JOIN tbl_message_users mu ON mu.message_id = m.message_id
    where m.user_category_id = @_user_category_id and mu.user_id = @_user_id and mu.read_status = 0;

    SELECT count(1) as s_count from tbl_statutory_notifications s
    INNER JOIN tbl_statutory_notifications_users su ON su.notification_id = s.notification_id
    AND su.user_id = @_user_id AND su.read_status = 0;

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
        WHERE validity_date_id = validitydaysid;
    END IF;
END //

DELIMITER ;

-- --------------------------------------------------------------------------------
-- To check duplicate industry name
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_industry_master_checkduplicateindustry`;

DELIMITER //

CREATE PROCEDURE `sp_industry_master_checkduplicateindustry`(
in industryid int(11), in industryname varchar(50), countryId int(11), domainId int(11))
BEGIN
    if industryid = 0 then
        SELECT count(1) FROM tbl_organisation WHERE organisation_name = industryname and
        country_id = countryId and domain_id = domainId;
    else
        SELECT count(1) FROM tbl_organisation WHERE organisation_name = industryname
        and organisation_id != industryid  and
        country_id = countryId and domain_id = domainId;
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
    in statutoryNatureId int(11),
    in countryId int(11)
)
BEGIN
    if statutoryNatureId = 0 then
        SELECT count(1) AS cnt FROM tbl_statutory_natures
        WHERE statutory_nature_name = statutoryNatureName
        AND country_id = countryId;
    else
        SELECT count(1) as cnt FROM tbl_statutory_natures
        WHERE statutory_nature_name = statutoryNatureName
        AND statutory_nature_id != statutoryNatureId and
        country_id = countryId;
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
    IN _category_id int(11), IN _from_limit INT, IN _to_limit INT
)
BEGIN
    if _category_id = 1 then
        SELECT t1.user_id, t1.user_category_id, t1.form_id, t1.action, t1.created_on
        FROM tbl_activity_log as t1 -- , tbl_users as t2
        WHERE
        date(t1.created_on) >= _from_date
        AND date(t1.created_on) <= _to_date
        AND COALESCE(t1.form_id,'') LIKE _form_id
        AND t1.user_id LIKE _user_id
        AND t1.user_category_id like _category_id
        -- AND t2.user_id LIKE _user_id
        -- AND t2.user_category_id in (1,2,3,4,5,6,7,8)
        -- ORDER BY t1.user_id ASC, DATE(t1.created_on) DESC
        ORDER BY t1.created_on DESC
        limit _from_limit, _to_limit;

        SELECT count(0) as total FROM tbl_activity_log
        WHERE
        date(created_on) >= _from_date
        AND date(created_on) <= _to_date
        AND user_id LIKE _user_id AND coalesce(form_id,'') LIKE _form_id
        AND user_category_id like _category_id;
    end if;

    if _category_id >= 2 then
        SELECT t1.user_id, t1.user_category_id, t1.form_id, t1.action, t1.created_on
    FROM tbl_activity_log as t1 -- , tbl_users as t2, tbl_user_countries as t3
    WHERE
        date(t1.created_on) >= _from_date
        AND date(t1.created_on) <= _to_date
        AND COALESCE(t1.form_id,'') LIKE _form_id
        AND t1.user_id LIKE _user_id
        AND t1.user_category_id like _category_id
        -- AND t3.user_id = t2.user_id
        -- AND t2.user_id LIKE _user_id
        -- AND t2.user_category_id LIKE _category_id
        -- ORDER BY t1.user_id ASC, DATE(t1.created_on) DESC
        ORDER BY t1.created_on DESC
        limit _from_limit, _to_limit;

        SELECT count(0) as total FROM tbl_activity_log
        WHERE
        date(created_on) >= _from_date
        AND date(created_on) <= _to_date
        AND user_id LIKE _user_id AND coalesce(form_id,'') LIKE _form_id
        AND user_category_id like _category_id;
    end if;
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

CREATE PROCEDURE `sp_client_groups_list`(
in userId INT(11)
)
BEGIN
    SELECT @u_cat_id := user_category_id from tbl_user_login_details where user_id = userId;

    SELECT
    tcg.client_id,
    tcg.group_name,
    tle.legal_entity_name,
    (SELECT
            country_name
        FROM
            tbl_countries
        WHERE
            country_id = tle.country_id) AS country_name,
    tle.is_closed,  tle.closed_on,
    tle.is_approved,
    tle.reason
    FROM
        tbl_legal_entities tle
            INNER JOIN
        tbl_client_groups tcg ON tcg.client_id = tle.client_id
            INNER JOIN
        tbl_user_clients tuc ON tuc.client_id = tcg.client_id
            AND
        IF (@u_cat_id > 2,
        tuc.user_id = userId, 1)
    ORDER BY tcg.group_name;
END //

DELIMITER ;

DROP PROCEDURE IF EXISTS `sp_reassign_client_groups_list`;

DELIMITER //

CREATE PROCEDURE `sp_reassign_client_groups_list`(
in userId INT(11)
)
BEGIN

    SELECT
    tcg.client_id,
    tcg.group_name
    FROM
        tbl_client_groups as tcg
    ORDER BY tcg.group_name;

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
    SELECT @u_cat_id := user_category_id from tbl_user_login_details where user_id = session_user;
    IF @u_cat_id > 2 THEN
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
    if(select @u_cg_id:=user_category_id from tbl_user_login_details where
    user_id = session_user) = 1 then
        select distinct(t1.legal_entity_id), t2.domain_id,
        (select domain_name from tbl_domains where
        domain_id = t2.domain_id) as domain_name, t2.organisation_id as industry_id,
        (select organisation_name from tbl_organisation where
        organisation_id = t2.organisation_id ) as industry_name,
        t2.count as unit_count
        from
        tbl_user_legalentity as t1 inner join tbl_user_mapping as t3 on
        t3.child_user_id = t1.user_id inner join tbl_legal_entity_domains as t2 on
        t2.legal_entity_id = t1.legal_entity_id and t2.domain_id = t3.domain_id
        group by t1.legal_entity_id, t2.domain_id, t2.organisation_id;
    end if;
    if(select @u_cg_id:=user_category_id from tbl_user_login_details where
    user_id = session_user) = 5 then
        select t4.legal_entity_id, t2.domain_id,
        (select domain_name from tbl_domains where
        domain_id = t2.domain_id) as domain_name, t2.organisation_id as industry_id,
        (select organisation_name from tbl_organisation where
        organisation_id = t2.organisation_id ) as industry_name,
        t2.count as unit_count
        from
        tbl_user_clients as t1 inner join tbl_legal_entities as t4 on
        t4.client_id = t1.client_id inner join tbl_legal_entity_domains as t2 on
        t2.legal_entity_id = t4.legal_entity_id
        where
           t1.user_id = session_user;
    end if;
    if(select @u_cg_id:=user_category_id from tbl_user_login_details where
    user_id = session_user) = 6 then
        select distinct(t1.legal_entity_id), t2.domain_id,
        (select domain_name from tbl_domains where
        domain_id = t2.domain_id) as domain_name, t2.organisation_id as industry_id,
        (select organisation_name from tbl_organisation where
        organisation_id = t2.organisation_id ) as industry_name,
        t2.count as unit_count
        from
        tbl_user_legalentity as t1 inner join tbl_user_mapping as t3 on
        t3.child_user_id = t1.user_id inner join tbl_legal_entity_domains as t2 on
        t2.legal_entity_id = t1.legal_entity_id and t2.domain_id = t3.domain_id
        where
           t1.user_id = session_user;
    end if;
    if(select @u_cg_id:=user_category_id from tbl_user_login_details where
    user_id = session_user) = 7 or 8 then
        select distinct(t1.legal_entity_id), t2.domain_id,
        (select domain_name from tbl_domains where
        domain_id = t2.domain_id) as domain_name, t2.organisation_id as industry_id,
        (select organisation_name from tbl_organisation where
        organisation_id = t2.organisation_id ) as industry_name,
        t2.count as unit_count
        from
        tbl_user_units as t1 inner join tbl_user_mapping as t3 on
        t3.child_user_id = t1.user_id inner join tbl_legal_entity_domains as t2 on
        t2.legal_entity_id = t1.legal_entity_id and t2.domain_id = t3.domain_id
        where
           t1.user_id = session_user;
    end if;
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
    IN clientid INT(11)
)
BEGIN
    SELECT bg.business_group_id, bg.business_group_name, bg.client_id, lg.country_id
    FROM tbl_business_groups bg
    INNER JOIN tbl_legal_entities lg on lg.client_id= bg.client_id and lg.business_group_id= bg.business_group_id
    WHERE bg.client_id=clientid
    group by bg.business_group_id;

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
        client_id, business_group_name, created_by, created_on,
        updated_by, updated_on
    ) VALUES
    (
        groupid, businessgroupname, session_user,
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
    IN legalentityid INT(11)
)
BEGIN
    DELETE FROM tbl_legal_entity_domains
    WHERE legal_entity_id = legalentityid;
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
-- To Check for duplicate group short name
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_client_group_is_duplicate_groupshortname`;

DELIMITER //


CREATE PROCEDURE `sp_client_group_is_duplicate_groupshortname`(
    IN groupshortname VARCHAR(50), clientid INT(11)
)
BEGIN
    IF clientid IS NULL THEN
        SELECT count(client_id) as count FROM tbl_client_groups
        WHERE short_name=groupshortname;
    ELSE
        SELECT count(client_id) as count FROM tbl_client_groups
        WHERE short_name=groupshortname and client_id != clientid;
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
    IN le_name VARCHAR(50), le_id INT(11), clientid INT(11), countryid INT(11)
)
BEGIN
    IF le_id IS NULL THEN
        SELECT count(legal_entity_id) as count FROM tbl_legal_entities
        WHERE legal_entity_name=le_name and client_id=clientid and country_id=countryid;
    ELSE
        SELECT count(legal_entity_id) as count FROM tbl_legal_entities
        WHERE legal_entity_name=le_name and client_id=clientid and  country_id=countryid
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
    file_space_limit, total_licence, is_closed, is_approved
    FROM tbl_legal_entities tle WHERE client_id=clientid;
END //

DELIMITER ;

-- --------------------------------------------------------------------------------
-- To get domains of client by legal entity
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_client_domains_by_group_id`;

DELIMITER //

CREATE PROCEDURE `sp_client_domains_by_group_id`(
    IN clientid INT(11), userId INT(11)
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
    find_in_set(entity_id, legal_entity_ids);
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
    SELECT used_file_space FROM tbl_legal_entities
    WHERE legal_entity_id=le_id;
END //

DELIMITER ;


-- --------------------------------------------------------------------------------
-- To Update Client Group
-- --------------------------------------------------------------------------------

DROP PROCEDURE IF EXISTS `sp_client_group_update`;

DELIMITER //

CREATE PROCEDURE `sp_client_group_update` (
    groupid INT(11), emailid VARCHAR(100), no_of_view_licence int(11), IN remarks VARCHAR(500)
)
BEGIN
    UPDATE tbl_client_groups set total_view_licence = no_of_view_licence,
    email_id = emailid, remarks = remarks
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
    select client_id, group_name as short_name from tbl_client_groups
    where client_id in
    (select t1.client_id from tbl_client_groups t1
    inner join tbl_user_legalentity t2 on t1.client_id = t2.client_id
    and t2.user_id = userId);
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
    FROM tbl_units WHERE unit_code like binary concat(unit_code_start_letter,'%') and
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
    SELECT user_category_id INTO user_category FROM tbl_user_login_details WHERE user_id = userid;
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
    FROM tbl_user_login_details WHERE user_id = userid;
    IF user_category in (1,2) then
        select legal_entity_id, legal_entity_name, business_group_id,
        client_id, country_id, DATEDIFF(contract_to,curdate()) as contract_days,
        is_approved from tbl_legal_entities
        where is_closed = 0
        order by legal_entity_name ASC;
    ELSEIF user_category = 5 THEN
        select legal_entity_id, legal_entity_name, business_group_id,
        client_id, country_id, DATEDIFF(contract_to,curdate()) as contract_days,
        is_approved from tbl_legal_entities
        WHERE client_id in (
            SELECT client_id FROM tbl_user_clients WHERE user_id=userid
        ) and is_closed = 0 order by legal_entity_name ASC;
    ELSEIF user_category = 6 then
        select legal_entity_id, legal_entity_name, business_group_id,
        client_id, country_id, DATEDIFF(contract_to,curdate()) as contract_days,
        is_approved from tbl_legal_entities
        WHERE legal_entity_id in (
            SELECT legal_entity_id FROM tbl_user_legalentity
            WHERE user_id=userid
        ) and is_closed = 0 order by legal_entity_name ASC;
    ELSE
        select legal_entity_id, legal_entity_name, business_group_id,
        client_id, country_id, DATEDIFF(contract_to,curdate()) as contract_days,
        is_approved from tbl_legal_entities
        WHERE legal_entity_id in (
            SELECT legal_entity_id FROM tbl_units WHERE unit_id in(
                SELECT unit_id FROM tbl_user_units
                WHERE user_id=userid
            )
        ) and is_closed = 0 order by legal_entity_name ASC;
    END IF;
END //

DELIMITER ;
-- -------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_get_reassign_legalentity`;

DELIMITER //

CREATE PROCEDURE `sp_get_reassign_legalentity`(in userId INT(11))
BEGIN
    DECLARE user_category INT(11);
    SELECT user_category_id INTO user_category
    FROM tbl_user_login_details WHERE user_id = userid;
    IF user_category in (1,2) then
        select legal_entity_id, legal_entity_name, business_group_id,
        client_id, country_id from tbl_legal_entities
        where is_closed = 0
        order by legal_entity_name ASC;
    ELSEIF user_category = 5 THEN
        select legal_entity_id, legal_entity_name, business_group_id,
        client_id, country_id from tbl_legal_entities
        WHERE client_id in (
            SELECT client_id FROM tbl_user_clients WHERE user_id=userid
        ) and is_closed = 0 order by legal_entity_name ASC;
    ELSEIF user_category = 6 then
        select legal_entity_id, legal_entity_name, business_group_id,
        client_id, country_id from tbl_legal_entities
        WHERE legal_entity_id in (
            SELECT legal_entity_id FROM tbl_user_legalentity
            WHERE user_id=userid
        ) and is_closed = 0 order by legal_entity_name ASC;
    ELSE
        select legal_entity_id, legal_entity_name, business_group_id,
        client_id, country_id from tbl_legal_entities
        WHERE legal_entity_id in (
            SELECT legal_entity_id FROM tbl_units WHERE unit_id in(
                SELECT unit_id FROM tbl_user_units
                WHERE user_id=userid
            )
        ) and is_closed = 0 order by legal_entity_name ASC;
    END IF;
    select distinct t1.legal_entity_id, t1.domain_id from tbl_legal_entity_domains as t1
        inner join tbl_legal_entities as t2 on t1.legal_entity_id = t2.legal_entity_id
        and t2.is_closed = 0 order by t2.legal_entity_name;
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
    t4.is_approved, t2.is_closed as is_active,
    t4.legal_entity_name as l_entity,
    (select business_group_name from tbl_business_groups
        where business_group_id = t2.business_group_id) as b_group,
    (select division_name from tbl_divisions
        where division_id = t2.division_id) as division,
    (select category_name from tbl_categories
        where category_id = t2.category_id) as category_name,
    t9.group_name,
    t8.country_name, t2.category_id, t2.remarks,
    count(t2.unit_id) as total_units,
    (select count(0) from tbl_units where client_id=t1.client_id and
    legal_entity_id=t1.legal_entity_id and is_closed=0) as total_active_units
    from
    tbl_user_legalentity as t1,
    tbl_units as t2,
    tbl_legal_entities as t4,
    tbl_countries as t8,
    tbl_client_groups as t9
    where
    t9.client_id = t2.client_id and
    t8.country_id = t2.country_id and
    t4.is_closed = 0 and
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

CREATE PROCEDURE `sp_units_approval_list`(in userId INT(11))
BEGIN
    SELECT tle.legal_entity_id, tle.legal_entity_name,
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
    count(unit_id) as unit_count
    FROM tbl_legal_entities tle
    inner join tbl_user_clients tuc on tuc.client_id = tle.client_id and tuc.user_id = userId
    INNER JOIN tbl_units tu on tu.legal_entity_id=tle.legal_entity_id
    WHERE tu.is_closed=0 and tu.is_approved=0 and tle.is_closed = 0
    group by tle.legal_entity_id, tle.legal_entity_name
    order by group_name;
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
    SELECT @u_cat_id := user_category_id from tbl_user_login_details where user_id = userid;
    INSERT INTO tbl_activity_log (user_category_id, user_id, form_id, action, created_on)
    VALUES (@u_cat_id, userid, formid, action_performed, action_performed_on);
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
    select distinct t1.client_id, t1.group_name, t1.short_name
    from tbl_client_groups as t1
    inner join tbl_legal_entities as t2 on t1.client_id = t2.client_id
    where t2.is_approved = 0 and t2.is_closed = 0;

    select distinct country_id, client_id from tbl_legal_entities
    where is_approved = 0 and is_closed = 0;

    SELECT t1.client_id, t1.group_name, t1.short_name, t1.email_id,
        t2.legal_entity_id, t2.legal_entity_name, t3.country_name
        from tbl_client_groups as t1
        INNER JOIN tbl_legal_entities as t2 on t1.client_id = t2.client_id
        INNER JOIN tbl_countries as t3 on t2.country_id = t3.country_id
        where t2.is_approved = 0 and t2.is_closed = 0
        order by t1.group_name, t3.country_name, t2.legal_entity_name;
END //

DELIMITER ;

DROP PROCEDURE IF EXISTS `sp_client_groups_legal_entity_info`;

DELIMITER //

CREATE PROCEDURE `sp_client_groups_legal_entity_info`(
    IN entity_id INT(11)
)
BEGIN

    select t1.legal_entity_id, t1.legal_entity_name,
    (select business_group_name from tbl_business_groups where business_group_id = t1.business_group_id)bg_name,
    t1.contract_from, t1.contract_to, t1.total_licence,
    t1.file_space_limit, t2.total_view_licence, t2.remarks,
    t3.legal_entity_name as o_legal_entity_name, t3.business_group_name as o_business_group_name,
    t3.contract_from as o_contract_from, t3.contract_to as o_contract_to,
    t3.file_space_limit as o_file_space_limit, t3.total_licence as o_total_licence,
    t4.total_view_licence as o_total_view_licence, t4.email_id as o_group_admin_email_id
    from tbl_legal_entities as t1
    inner join tbl_client_groups as t2 on t1.client_id = t2.client_id
    left join tbl_legal_entity_contract_history as t3 on t1.legal_entity_id = t3.legal_entity_id
    and t3.legal_entity_history_id =  (select max(legal_entity_history_id) from tbl_legal_entity_contract_history where legal_entity_id = t1.legal_entity_id)
    left join tbl_client_groups_history as t4 on t1.client_id = t4.client_id
    and t4.client_history_id =  (select max(client_history_id) from tbl_client_groups_history where client_id = t1.client_id)
    where t1.legal_entity_id = entity_id;

    select t1.legal_entity_id, t1.domain_id, t1.activation_date, t1.organisation_id, t1.count,
    t2.organisation_name, t3.domain_name, t4.count as o_count
    from tbl_legal_entity_domains as t1
    inner join tbl_organisation as t2 on t1.organisation_id = t2.organisation_id
    inner join tbl_domains as t3 on t1.domain_id = t3.domain_id
    left join tbl_legal_entity_domains_history as t4 on t1.legal_entity_id = t4.legal_entity_id and t1.domain_id = t4.domain_id
    and t4.le_domain_history_id =  (select max(le_domain_history_id) from tbl_legal_entity_domains_history where t1.legal_entity_id = legal_entity_id and t1.domain_id = domain_id)
    where t1.legal_entity_id = entity_id
    order by t3.domain_name, t2.organisation_name;

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
    FROM tbl_user_countries
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
    T2.username, IFNULL(DATEDIFF(current_ist_datetime(), T1.disabled_on), 0) as days_left,
    T1.disable_reason
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
    contactno VARCHAR(50), mobileno VARCHAR(50), addr TEXT, desig VARCHAR(50),
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
    updated_time TIMESTAMP, remarks varchar(500)
)
BEGIN
    UPDATE tbl_users set is_disable = isdisable,
        updated_by =  session_user, disabled_on = updated_time,
        disable_reason = remarks
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


DROP PROCEDURE IF EXISTS `sp_groupname_by_id`;

DELIMITER //

CREATE PROCEDURE `sp_groupname_by_id`(
    IN ctid INT(11)
)
BEGIN
    SELECT client_id, group_name FROM tbl_client_groups WHERE client_id = ctid;
END //

DELIMITER ;

DROP PROCEDURE IF EXISTS `sp_legalentityname_by_id`;

DELIMITER //

CREATE PROCEDURE `sp_legalentityname_by_id`(
    IN leid INT(11)
)
BEGIN
    SELECT legal_entity_id, legal_entity_name FROM tbl_legal_entities WHERE
    legal_entity_id = leid;
END //

DELIMITER ;

DROP PROCEDURE IF EXISTS `sp_unitname_by_id`;

DELIMITER //

CREATE PROCEDURE `sp_unitname_by_id`(
    IN uid INT(11)
)
BEGIN
    SELECT unit_id, unit_name FROM tbl_units WHERE
    unit_id = uid;
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
    SELECT database_server_id, database_server_name, database_ip, database_port,
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
    IN dbservername VARCHAR(50), dbserverid int(11)
)
BEGIN
    if dbserverid is null then
        SELECT count(database_server_id) as count FROM tbl_database_server
        WHERE database_server_name = dbservername;
    else
        SELECT count(database_server_id) as count FROM tbl_database_server
        WHERE database_server_name = dbservername and database_server_id != dbserverid;
    end if;
END //

DELIMITER ;

-- --------------------------------------------------------------------------------
-- To save or update Database server
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_databaseserver_save`;

DELIMITER //

CREATE PROCEDURE `sp_databaseserver_save`(
    IN dbserverid int(11), dbservername VARCHAR(50), ipaddr VARCHAR(50),
    port_no INT(11), username VARCHAR(50), pwd VARCHAR(50),
    _createdby int(11), _createdon timestamp
)
BEGIN
    if dbserverid is null then
         INSERT INTO tbl_database_server (
            database_server_name, database_ip, database_port,
            database_username, database_password, created_by, created_on
        ) VALUES (dbservername, ipaddr, port_no, username, pwd, _createdby, _createdon);
    else
        UPDATE tbl_database_server
            set database_server_name = dbservername, database_ip = ipaddr,
            database_port = port_no, database_username = username,
            database_password = pwd, updated_by = _createdby,
            updated_on = _createdon where database_server_id = dbserverid;
    end if;
END //

DELIMITER ;

-- --------------------------------------------------------------------------------
-- To get all Machine  details
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_machines_list`;

DELIMITER //

CREATE PROCEDURE `sp_machines_list`()
BEGIN
    SELECT machine_id, machine_name, ip, port, client_ids
    FROM tbl_application_server order by machine_name;
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
    port_no INT(11), _createdby int(11), _createdon timestamp
)
BEGIN
    IF machineid IS NULL THEN
        INSERT INTO tbl_application_server (
            machine_name, ip, port, created_by, created_on
        ) VALUES (machinename, ipaddr, port_no, _createdby, _createdon);

    ELSE
        UPDATE tbl_application_server SET machine_name = machinename,
        ip=ipaddr, port = port_no, updated_by = _createdby,
        updated_on = _createdon WHERE machine_id = machineid;
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
    select t2.client_database_id, t1.client_id, (select group_name from
    tbl_client_groups where client_id = t1.client_id) as group_name,
    t1.legal_entity_id, t1.legal_entity_name, t2.machine_id,
    (select machine_name from tbl_application_server where
    machine_id = t2.machine_id) as machine_name,
    t2.database_server_id,
    (select database_server_name from tbl_database_server
    where database_server_id = t2.database_server_id) as database_server_name,
    t2.client_database_server_id,
    (select database_server_name from tbl_database_server
    where database_server_id = t2.client_database_server_id) as client_database_server_name,
    t2.file_server_id, t1.is_approved,
    (select file_server_name from tbl_file_server
    where file_server_id = t2.file_server_id) as file_server_name, t1.is_created
    from tbl_legal_entities as t1 left join tbl_client_database as t2
    on t1.legal_entity_id = t2.legal_entity_id
    where t1.is_approved = 1;

    SELECT machine_id, machine_name, ip, port, client_ids FROM tbl_application_server;

    select database_server_id, database_server_name, database_ip, database_port,
    legal_entity_ids from tbl_database_server;

    SELECT file_server_id, file_server_name, ip, port, legal_entity_ids from
    tbl_file_server;
END //

DELIMITER ;

-- --------------------------------------------------------------------------------
-- To Save or Update Client database details
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_clientdatabase_save`;

DELIMITER //

CREATE PROCEDURE `sp_clientdatabase_save`(
    IN clientid INT(11), le_id INT(11), machineid INT(11), db_server_id int(11),
    le_db_server_id int(11), _f_s_id int(11), _cl_ids longtext, _le_ids longtext,
    _created_by int(11), _created_on timestamp
)
BEGIN
    if(select count(*) from tbl_client_database where client_id = clientid) > 0 then
        update tbl_client_database set machine_id = machineid,
        client_database_server_id = db_server_id where client_id = clientid;
    end if;

    insert into tbl_client_database
    (client_id, legal_entity_id, machine_id, file_server_id, database_server_id,
    client_database_server_id, created_by, created_on)
    values
    (clientid, le_id, machineid, _f_s_id, le_db_server_id, db_server_id, _created_by, _created_on);


    update tbl_application_server set client_ids = _cl_ids
    where machine_id = machineid;

    update tbl_database_server set legal_entity_ids = _le_ids
    where database_server_id = le_db_server_id;

    update tbl_file_server set legal_entity_ids = _le_ids
    where file_server_id = _f_s_id;

    update tbl_legal_entities set is_created = 1
    where legal_entity_id = le_id;
END //

DELIMITER ;

DROP PROCEDURE IF EXISTS `sp_clientdatabase_dbname_info_save`;

DELIMITER //

CREATE PROCEDURE `sp_clientdatabase_dbname_info_save`(
    IN csid int(11), dun varchar(100), dpwd varchar(100), dbowner int(11),
    dbname varchar(100), is_group int(1)
)
BEGIN
    insert into tbl_client_database_info(client_database_id, db_owner_id,
    database_username, database_password, database_name, is_group)
    values
    (csid, dbowner, dun, dpwd, dbname, is_group);

END //

DELIMITER ;



-- --------------------------------------------------------------------------------
-- Update Client Database Environment
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_clientdatabase_update`;

DELIMITER //

CREATE PROCEDURE `sp_clientdatabase_update`(
IN client_db_id int(11), clientid INT(11), le_id INT(11), machineid INT(11), db_server_id int(11),
    le_db_server_id int(11), _f_s_id int(11), _cl_ids longtext, _le_ids longtext,
    old_machineid INT(11), old_grp_d_s_id int(11), old_le_d_s_id int(11),
    old_le_f_s_id int(11), old_cl_ids longtext, old_grp_le_ids longtext,
    old_le_ids longtext, old_f_le_ids longtext, _created_by int(11), _created_on timestamp,
    _f_le_ids longtext, _le_le_ids longtext
)
BEGIN
    update tbl_client_database set client_id = clientid, legal_entity_id = le_id,
    machine_id = machineid, file_server_id = _f_s_id, database_server_id = le_db_server_id,
    client_database_server_id = db_server_id, updated_by = _created_by
    where client_database_id = client_db_id;

    update tbl_client_database set machine_id = machineid,
    client_database_server_id = db_server_id where client_id = clientid;

    update tbl_application_server set client_ids = _cl_ids
    where machine_id = machineid;

    update tbl_application_server set client_ids = old_cl_ids
    where machine_id = old_machineid;

    update tbl_database_server set legal_entity_ids = _le_ids
    where database_server_id = db_server_id;

    update tbl_database_server set legal_entity_ids = old_grp_le_ids
    where database_server_id = old_grp_d_s_id;

    update tbl_database_server set legal_entity_ids = _le_le_ids
    where database_server_id = le_db_server_id;

    update tbl_database_server set legal_entity_ids = old_le_ids
    where database_server_id = old_le_d_s_id;

    update tbl_file_server set legal_entity_ids = _f_le_ids
    where file_server_id = _f_s_id;

    update tbl_file_server set legal_entity_ids = old_f_le_ids
    where file_server_id = old_le_f_s_id;

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

    SELECT tl.legal_entity_id, tl.legal_entity_name, tl.client_id,
    (
        SELECT count(unit_id) FROM tbl_units tu
        WHERE tu.legal_entity_id=tl.legal_entity_id
    ) as unit_count,
    (
        SELECT max(deletion_period) FROM tbl_auto_deletion tua
        WHERE tua.client_id=tl.client_id
        and tua.legal_entity_id = tl.legal_entity_id
    ) as deletion_period, tl.is_closed
    FROM tbl_legal_entities tl where tl.is_approved = 1;

    SELECT tu.unit_id, tu.client_id, tu.legal_entity_id, tu.unit_code, tu.unit_name,
    (
        SELECT deletion_period FROM tbl_auto_deletion tua
        WHERE tua.client_id=tu.client_id
        and tua.legal_entity_id = tu.legal_entity_id and tua.unit_id = tu.unit_id
    ) as deletion_period, concat(address,' - ',postal_code) as address FROM tbl_units tu where tu.is_approved = 1;
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
    DELETE FROM tbl_auto_deletion
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
    SELECT u.user_id, u.is_active,
    concat(u.employee_code," - ", u.employee_name) as employee_name
    FROM tbl_users u inner join tbl_user_login_details ul on ul.user_id = u.user_id
    WHERE u.user_category_id=3 and u.is_disable = 0;

    SELECT u.user_id, u.is_active,
    concat(u.employee_code," - ", u.employee_name) as employee_name
    FROM tbl_users u inner join tbl_user_login_details ul on ul.user_id = u.user_id
    WHERE u.user_category_id=4 and u.is_disable = 0;

    SELECT u.user_id, u.is_active,
    concat(u.employee_code," - ", u.employee_name) as employee_name
    FROM tbl_users u inner join tbl_user_login_details ul on ul.user_id = u.user_id
    WHERE u.user_category_id=5 and u.is_disable = 0;

    SELECT u.user_id, u.is_active,
    concat(u.employee_code," - ", u.employee_name) as employee_name
    FROM tbl_users u inner join tbl_user_login_details ul on ul.user_id = u.user_id
    WHERE u.user_category_id=6 and u.is_disable = 0;

    SELECT u.user_id, u.is_active,
    concat(u.employee_code," - ", u.employee_name) as employee_name
    FROM tbl_users u inner join tbl_user_login_details ul on ul.user_id = u.user_id
    WHERE u.user_category_id=7 and u.is_disable = 0;

    SELECT u.user_id, u.is_active,
    concat(u.employee_code," - ", u.employee_name) as employee_name
    FROM tbl_users u inner join tbl_user_login_details ul on ul.user_id = u.user_id
    WHERE u.user_category_id=8 and u.is_disable = 0;

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
    IN parent_userid INT(11), IN c_id INT(11), IN d_id INT(11)
)
BEGIN
    DELETE FROM tbl_user_mapping WHERE parent_user_id=parent_userid and
    country_id = c_id and domain_id = d_id;
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
    tbl_user_legalentity as t1
    inner join tbl_legal_entities as t2 on t2.legal_entity_id = t1.legal_entity_id
    left join tbl_business_groups as t3 on t3.business_group_id = t2.business_group_id
    inner join tbl_countries as t4 on t4.country_id = t2.country_id
    where
    t1.user_id = session_user;

END //

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
END //

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
        case when unitId is null then
            select count(*) as unit_code_cnt from
            tbl_units where
            unit_code = unitCode and
            client_id = clientId;
        else
            select count(*) as unit_code_cnt from
            tbl_units where
            unit_code = unitCode and
            client_id = clientId
            and unit_id != unitId;
        end case;
    else
        case when unitId is null then
            select count(*) as unit_name_cnt from
            tbl_units where
            unit_name = unitName and
            client_id = clientId;
        else
            select count(*) as unit_name_cnt from
            tbl_units where
            unit_name = unitName and
            client_id = clientId and
            unit_id != unitId;
        end case;
    end if;

END //

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
END //

DELIMITER ;

-- --------------------------------------------------------------------------------
-- check dupliaction of id for save units
-- --------------------------------------------------------------------------------

DROP PROCEDURE IF EXISTS `sp_tbl_units_check_unitgroupid`;

DELIMITER //

CREATE PROCEDURE `sp_tbl_units_check_unitgroupid`(in tableName varchar(50), param int(11))
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
    if tableName = 'le_closed' then
        select is_closed from
        tbl_legal_entities where legal_entity_id = param;
    end if;

END //

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

CREATE PROCEDURE `sp_userunits_list`( IN userid_ INT(11))
BEGIN
    SELECT @u_cat_id := user_category_id from tbl_user_login_details where user_id = userid_;
    IF @u_cat_id = 5 THEN
        select t1.client_id, count(distinct t2.unit_id) as total_units, t3.domain_id,
        count(distinct t4.unit_id) as assigned_units, (Select group_name from tbl_client_groups
        where client_id = t1.client_id) as client_name,
        (select domain_name from tbl_domains where domain_id = t3.domain_id)
        as domain_name, t2.legal_entity_id, (select legal_entity_name from tbl_legal_entities as tle
        where tle.legal_entity_id = t2.legal_entity_id) as legal_entity_name,
        (select business_group_name from tbl_business_groups where business_group_id =
        t2.business_group_id) as business_group_name
        from tbl_user_clients as t1 inner join tbl_units as t2
        on t2.client_id = t1.client_id and t2.is_approved = 1
        inner join tbl_units_organizations as t3
        on t3.unit_id = t2.unit_id left join tbl_user_units as t4 on
        t4.unit_id = t2.unit_id and t4.domain_id = t3.domain_id and
        t4.user_category_id=7
        where t1.user_id = userid_
        group by t1.client_id, t2.legal_entity_id, t3.domain_id
        order by domain_name;
    ELSE
        select count(distinct t1.unit_id) as total_units, t5.domain_id,
        t2.legal_entity_id, t1.client_id, t2.legal_entity_name,
        t3.business_group_name,(Select group_name from tbl_client_groups
        where client_id = t1.client_id) as client_name,
        (select domain_name from tbl_domains where domain_id = t5.domain_id)
        as domain_name, count(distinct tuu.unit_id) as assigned_units
        from
        tbl_user_units as t1 left join tbl_user_units as tuu on
        tuu.unit_id=t1.unit_id and tuu.user_category_id=8 and tuu.domain_id= t1.domain_id
        inner join tbl_legal_entities as t2
        on t2.client_id = t1.client_id and t2.legal_entity_id = t1.legal_entity_id and
        t2.is_closed = 0
        left join tbl_business_groups as t3 on t3.business_group_id = t2.business_group_id
        inner join tbl_units as t4 on t4.client_id = t1.client_id and t4.legal_entity_id = t2.legal_entity_id
        and t4.country_id = t2.country_id and t4.is_approved = 1 and t4.unit_id=t1.unit_id
        inner join tbl_units_organizations as t5 on t5.unit_id = t4.unit_id and t5.domain_id=t1.domain_id
        where
        t1.user_id = userid_ and t1.user_category_id = @u_cat_id
        group by t5.domain_id, t1.client_id, t2.legal_entity_id
         order by domain_name;
    END IF;
END //

DELIMITER ;

-- --------------------------------------------------------------------------------
-- To get assigned units list
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_userunits_assigned_list`;

DELIMITER //

CREATE PROCEDURE `sp_userunits_assigned_list`(
    IN clientid INT(11), domainid INT(11), legal_entity_id int(11), _userid int(11)
)
BEGIN
    SELECT @u_cat_id := user_category_id from tbl_user_login_details where user_id = _userid;
    IF @u_cat_id = 5 THEN
        SELECT tuu.user_id,
        concat(employee_code,"-", employee_name) as employee_name,
        tuu.legal_entity_id, legal_entity_name,
        count(tuu.unit_id) as no_of_units,
        (
            SELECT business_group_name FROM tbl_business_groups tbg
            WHERE tbg.business_group_id=tle.business_group_id
        ) as business_group_name, tuu.user_category_id,
        tuu.client_id, tuu.domain_id
        FROM tbl_user_units tuu
        INNER JOIN tbl_legal_entities tle ON tle.legal_entity_id=tuu.legal_entity_id
        inner join tbl_user_mapping tum on tum.country_id = tle.country_id and
        tum.domain_id = tuu.domain_id and tum.parent_user_id = _userid and
        tum.child_user_id = tuu.user_id
        INNER JOIN tbl_users tu ON tu.user_id = tum.child_user_id
        inner join tbl_units as tun on tun.unit_id = tuu.unit_id and tun.is_approved = 1
        WHERE tuu.client_id=clientid and tuu.domain_id=domainid and tuu.legal_entity_id = legal_entity_id
        and tuu.user_category_id = 7 group by user_id;
    ELSE
        SELECT tuu.user_id,
        concat(employee_code,"-", employee_name) as employee_name,
        tuu.legal_entity_id, legal_entity_name,
        count(tuu.unit_id) as no_of_units,
        (
            SELECT business_group_name FROM tbl_business_groups tbg
            WHERE tbg.business_group_id=tle.business_group_id
        ) as business_group_name, tuu.user_category_id,
        tuu.client_id, tuu.domain_id
        FROM tbl_user_units tuu
        INNER JOIN tbl_legal_entities tle ON tle.legal_entity_id=tuu.legal_entity_id
        inner join tbl_user_mapping tum on tum.country_id = tle.country_id and
        tum.domain_id = tuu.domain_id and tum.parent_user_id = _userid and
        tum.child_user_id = tuu.user_id
        INNER JOIN tbl_users tu ON tu.user_id = tum.child_user_id
        inner join tbl_units as tun on tun.unit_id= tuu.unit_id and tun.is_approved = 1
        WHERE tuu.client_id=clientid and tuu.domain_id=domainid and tuu.legal_entity_id = legal_entity_id
        and tuu.user_category_id = 8 group by tuu.user_id;
    END IF;
END //

DELIMITER ;

-- --------------------------------------------------------------------------------
-- To get assigned unit details list
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_userunits_assigned_details_list`;

DELIMITER //

CREATE PROCEDURE `sp_userunits_assigned_details_list`(
    IN u_id INT(11), le_id INT(11), cl_id int(11), d_id int(11)
)
BEGIN
     select unit_id, (
        SELECT legal_entity_name FROM tbl_legal_entities tle
        WHERE tle.legal_entity_id=tu.legal_entity_id
    ) as legal_entity_name,(
        SELECT division_name FROM tbl_divisions td
        WHERE td.division_id=tu.division_id
    ) as division_name,(
        SELECT category_name FROM tbl_categories tcm
        WHERE tcm.category_id=tu.category_id
    ) as category_name, unit_code, unit_name, address, (
        SELECT geography_name FROM tbl_geographies tgm
        WHERE tgm.geography_id = tu.geography_id
    ) as geography_name FROM tbl_units tu
    WHERE legal_entity_id = le_id and unit_id in (
        SELECT unit_id FROM tbl_user_units
        WHERE user_id=u_id and legal_entity_id= le_id and
        client_id=cl_id and domain_id=d_id
    ) and is_approved = 1;

    SELECT unit_id, (
        SELECT domain_name FROM tbl_domains td
        WHERE td.domain_id = tui.domain_id
    ) as domain_name, (
        SELECT organisation_name FROM tbl_organisation ti
        WHERE ti.organisation_id = tui.organisation_id
    ) as organisation_name FROM tbl_units_organizations tui
    WHERE tui.unit_id in (
        SELECT unit_id FROM tbl_user_units tu WHERE tu.legal_entity_id=le_id and
        tu.client_id=cl_id and tu.domain_id=d_id and user_id = u_id
    ) and tui.domain_id = d_id;
END //

DELIMITER ;

-- --------------------------------------------------------------------------------
-- To get domain managers
-- --------------------------------------------------------------------------------

DROP PROCEDURE IF EXISTS `sp_users_domain_managers`;

DELIMITER //

CREATE PROCEDURE `sp_users_domain_managers`(
    IN session_user INT(11), _d_id int(11), _cl_id int(11)
)
BEGIN
    select @catg_id:=user_category_id from tbl_users where user_id = session_user;

    if @catg_id = 5 then
        SELECT user_id,
        concat(employee_code, "-", employee_name) as employee_name,
        is_active, user_category_id FROM tbl_users WHERE
        user_category_id = 7 and
        user_id in (SELECT child_user_id FROM tbl_user_mapping
        WHERE parent_user_id=session_user and domain_id =_d_id) and is_active=1 and is_disable=0;

        SELECT t2.user_id, t1.legal_entity_id
        FROM
            tbl_legal_entities as t1 inner join tbl_user_domains as t2
            on t2.country_id = t1.country_id inner join tbl_users as t3
            on t3.user_id = t2.user_id
            WHERE
            t3.user_id in (SELECT child_user_id FROM tbl_user_mapping
            WHERE parent_user_id=session_user and domain_id =_d_id and country_id = t1.country_id)
            and t3.user_category_id = 7 and t3.is_active=1 and t3.is_disable=0 and
            t2.domain_id = _d_id and t1.client_id = _cl_id;
            -- group by t2.user_id;
    else
        SELECT user_id,
        concat(employee_code, "-", employee_name) as employee_name,
        is_active, user_category_id FROM tbl_users WHERE
        user_category_id = 8 and
        user_id in (SELECT child_user_id FROM tbl_user_mapping
        WHERE parent_user_id=session_user and domain_id =_d_id) and is_active=1 and is_disable=0;

        SELECT t2.user_id, t1.legal_entity_id
        FROM
            tbl_legal_entities as t1 inner join tbl_user_domains as t2
            on t2.country_id = t1.country_id inner join tbl_users as t3
            on t3.user_id = t2.user_id
            WHERE
            t3.user_id in (SELECT child_user_id FROM tbl_user_mapping
            WHERE parent_user_id=session_user and domain_id =_d_id and country_id = t1.country_id)
            and t3.user_category_id = 8 and t3.is_active=1 and t3.is_disable=0 and
            t2.domain_id = _d_id and t1.client_id = _cl_id;
            -- group by t2.user_id;
    end if;

END //

DELIMITER ;

-- --------------------------------------------------------------------------------
-- Routine DDL
-- Note: comments before and after the routine body will not be stored by the server
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_units_list`;

DELIMITER //

CREATE PROCEDURE `sp_units_list`(
    IN clientid INT(11), IN domainid INT(11), IN LegalEntityID int(11), IN userid INT(11)
)
BEGIN
    SELECT @u_cat_id := user_category_id from tbl_user_login_details where user_id = userid;
    IF @u_cat_id = 5 THEN
        SELECT tu.unit_id, unit_code, unit_name,
        address, (
            SELECT division_name FROM tbl_divisions td
            WHERE td.division_id=tu.division_id
        ) as division_name, (
            SELECT category_name FROM tbl_categories tcm
            WHERE tcm.category_id=tu.category_id
        ) as category_name,tu.legal_entity_id,(
            SELECT legal_entity_name FROM tbl_legal_entities tle
            WHERE tle.legal_entity_id=tu.legal_entity_id
        ) as legal_entity_name,
        business_group_id, is_closed, (
            SELECT geography_name FROM tbl_geographies tg
            WHERE tg.geography_id = tu.geography_id
        ) as geography_name
        FROM tbl_units tu
        INNER JOIN tbl_units_organizations tui on tui.unit_id=tu.unit_id and tu.is_approved=1
        left join tbl_user_clients uc ON uc.user_id = userid and uc.client_id= tu.client_id
        WHERE tu.client_id=clientid and tu.legal_entity_id = LegalEntityID
        and tui.domain_id=domainid and
        tu.unit_id not in (
            SELECT unit_id FROM tbl_user_units WHERE client_id=clientid and domain_id=domainid
        )
        group by tu.unit_id
        order by unit_name ASC;

        SELECT tui.unit_id, (SELECT domain_name FROM tbl_domains td WHERE td.domain_id = tui.domain_id)
            as domain_name, (SELECT organisation_name FROM tbl_organisation ti
            WHERE ti.organisation_id = tui.organisation_id) as organisation_name
        FROM tbl_units tu
        INNER JOIN tbl_units_organizations tui on tui.unit_id=tu.unit_id and tu.is_approved=1
        left join tbl_user_clients uc ON uc.user_id = userid and uc.client_id= tu.client_id
        WHERE tu.client_id=clientid and tu.legal_entity_id = LegalEntityID and tui.domain_id=domainid and
        tu.unit_id not in (
            SELECT unit_id FROM tbl_user_units WHERE client_id=clientid and domain_id=domainid
        );

    ELSE
        SELECT tu.unit_id, unit_code, unit_name,
        address, (
            SELECT division_name FROM tbl_divisions td
            WHERE td.division_id=tu.division_id
        ) as division_name, (
            SELECT category_name FROM tbl_categories tcm
            WHERE tcm.category_id=tu.category_id
        ) as category_name,tu.legal_entity_id,(
            SELECT legal_entity_name FROM tbl_legal_entities tle
            WHERE tle.legal_entity_id=tu.legal_entity_id
        ) as legal_entity_name,
        business_group_id, is_closed, (
            SELECT geography_name FROM tbl_geographies tg
            WHERE tg.geography_id = tu.geography_id
        ) as geography_name
        from tbl_user_units as tuu
        right join tbl_units as tu
        on tu.unit_id = tuu.unit_id and tu.legal_entity_id = LegalEntityID and
        tu.unit_id not in (select unit_id from tbl_user_units where user_id!=userid
        and user_category_id=8 and client_id=clientid and domain_id=domainid and
        legal_entity_id = LegalEntityID) and tu.is_approved=1
        INNER JOIN tbl_units_organizations tui on tui.unit_id=tu.unit_id and
        tui.domain_id=tuu.domain_id
        where
        tuu.user_id = userid and
        tuu.client_id=clientid and tuu.domain_id=domainid
        group by tu.unit_id
        order by unit_name ASC;


        SELECT t1.unit_id, (
            SELECT domain_name FROM tbl_domains td
            WHERE td.domain_id = t1.domain_id
        ) as domain_name, (
            SELECT organisation_name FROM tbl_organisation ti
            WHERE ti.organisation_id = t1.organisation_id
        ) as organisation_name
        from tbl_user_units as tuu
        right join tbl_units_organizations as t1
        on tuu.unit_id = t1.unit_id and
        tuu.unit_id not in (select unit_id from tbl_user_units where
        user_id!=userid and user_category_id=8 and client_id=clientid and
        domain_id=domainid and legal_entity_id = LegalEntityID)

        where
        tuu.user_id = userid and
        tuu.client_id=clientid and tuu.domain_id=domainid

        group by tuu.unit_id;


    END IF;

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
    client_id, country_id, DATEDIFF(contract_to,curdate()) as contract_days,
    is_approved FROM tbl_legal_entities WHERE client_id=clientid and
    is_closed = 0;
END //

DELIMITER ;

-- --------------------------------------------------------------------------------
-- To delete user units
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_userunits_delete`;

DELIMITER //

CREATE PROCEDURE `sp_userunits_delete`(
    IN unitId INT(11), domainIds varchar(50)
)
BEGIN
    if(select count(*) from tbl_user_units where unit_id=unitID and
    domain_id in (domainIds)) > 0 then
        DELETE FROM tbl_user_units WHERE unit_id=unitID and
        domain_id in (domainIds);
    end if;
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
    SELECT t01.unit_id, unit_code, unit_name, address, division_id,
    legal_entity_id, business_group_id, client_id, is_closed as is_active, group_concat(t02.domain_id) as domain_ids
    FROM tbl_units as t01
    INNER JOIN tbl_units_organizations as t02 on t01.unit_id = t02.unit_id
    group by t01.unit_id,t02.unit_id;
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
        WHERE find_in_set(assigned_ids, legal_entity_id);
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

DELIMITER ;

-- -------------------------------------------------------------------------------------------
-- To get the list of groups with countries and number of legal entities assigned / unassigned
-- -------------------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_assign_legal_entities_list`;

DELIMITER //

CREATE PROCEDURE `sp_assign_legal_entities_list`(in userId INT(11))
BEGIN
    select tcg.client_id, tcg.group_name,
    (
        select group_concat(country_name) from tbl_countries
        where country_id in (
            select country_id from tbl_legal_entities
            where client_id=tcg.client_id and is_closed = 0 and is_approved = 1
        )
    ) as country_names,
    (
        select count(legal_entity_id) from tbl_legal_entities tle
        WHERE tle.client_id=tcg.client_id and tle.is_closed = 0 and tle.is_approved = 1
    ) as no_of_legal_entities,
    (
        select count(tule.legal_entity_id) from tbl_user_legalentity tule
        inner join tbl_legal_entities tle on tle.legal_entity_id = tule.legal_entity_id
        WHERE tule.client_id=tcg.client_id and tle.is_closed = 0 and tle.is_approved = 1
        group by tule.client_id
    ) as no_of_assigned_legal_entities

    FROM tbl_client_groups tcg
    inner join tbl_user_clients tuc on tuc.client_id = tcg.client_id and tuc.user_id = userId
    where (
        select count(legal_entity_id) from tbl_legal_entities tle
        WHERE tle.client_id=tcg.client_id and tle.is_closed = 0 and tle.is_approved = 1
    ) > 0
    order by tcg.group_name;

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
    WHERE t1.client_id=clientid and t1.is_closed = 0 and t1.is_approved = 1 and t4.legal_entity_id is null
    order by t1.legal_entity_name;

    select distinct domain_id, legal_entity_id from tbl_legal_entity_domains;
END //

DELIMITER ;

-- ------------------------
-- To get techno users list
-- ------------------------
DROP PROCEDURE IF EXISTS `sp_users_technouser_list`;

DELIMITER //

CREATE PROCEDURE `sp_users_technouser_list`(session_user INT(11))
BEGIN
    SELECT distinct t1.child_user_id as user_id, t2.is_active,
        concat(t2.employee_code," - ", t2.employee_name) as employee_name
        from tbl_user_mapping t1
        INNER JOIN tbl_users t2 ON t1.child_user_id = t2.user_id AND t2.user_category_id = 6
        AND t2.is_active = 1 AND t2.is_disable = 0
        WHERE t1.parent_user_id = session_user;

    SELECT user_id, country_id FROM tbl_user_countries;

    SELECT user_id, domain_id FROM tbl_user_domains;

    select t1.country_id, t1.domain_id, t1.user_id
        from tbl_user_domains t1 inner join tbl_users as t
        on t.user_id = t1.user_id
        inner join tbl_user_mapping t2 on t.user_id = t2.child_user_id and t1.country_id = t2.country_id and t1.domain_id = t2.domain_id and t2.parent_user_id = session_user
        where t.is_active = 1 and t.is_disable = 0 and t.user_category_id = 6
        group by t1.country_id,t1.domain_id, t1.user_id
        order by t1.country_id, t1.domain_id, t1.user_id;
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
    SELECT t1.legal_entity_id, t1.legal_entity_name,t2.business_group_name, t3.country_name, t3.country_id,
    (select concat(employee_code, '-' ,employee_name) from tbl_users where user_id = t4.user_id) as employee_name
    FROM tbl_legal_entities t1
    LEFT JOIN tbl_business_groups t2 on t1.business_group_id = t2.business_group_id
    INNER JOIN tbl_countries t3 on t1.country_id = t3.country_id
    LEFT JOIN tbl_user_legalentity t4 on t1.legal_entity_id = t4.legal_entity_id
    WHERE t1.client_id=clientid and t1.is_closed = 0 and t1.is_approved = 1 and t4.legal_entity_id is not null
    order by t4.user_id, t1.legal_entity_name;
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
    (select count(distinct domain_id) from tbl_legal_entity_domains where legal_entity_id = t1.legal_entity_id and IF(domainid_ IS NOT NULL, domain_id = domainid_, 1)) as domaincount,
    (select domain_name from tbl_domains where domain_id = t3.domain_id) as domain_name,
    (select sum(count) from tbl_legal_entity_domains where domain_id = t3.domain_id and legal_entity_id = t1.legal_entity_id) as domain_total_unit,
    t3.activation_date,
    (select count(o.unit_id) from tbl_units_organizations as o inner join tbl_units as u on o.unit_id = u.unit_id
    where u.legal_entity_id = t1.legal_entity_id and o.domain_id = t3.domain_id) as domain_used_unit,
    (select contact_no from tbl_client_users where user_category_id = 3 and client_id = t1.client_id and t1.legal_entity_id in (legal_entity_ids)) as le_admin_contactno,
    (select email_id from tbl_client_users where user_category_id = 3 and client_id = t1.client_id and t1.legal_entity_id in (legal_entity_ids)) as le_admin_email
    from tbl_legal_entities t1
    inner join tbl_client_groups t2 on t1.client_id = t2.client_id
    inner join tbl_legal_entity_domains t3 on t1.legal_entity_id = t3.legal_entity_id
    left join tbl_business_groups t4 on t1.business_group_id = t4.business_group_id
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
    and t1.legal_entity_id in (select legal_entity_id from (SELECT t.legal_entity_id,
    @rownum := @rownum + 1 AS num
    FROM (select distinct legal_entity_id from tbl_legal_entities where country_id = countryid_) t,
    (SELECT @rownum := 0) r) as cnt
    where   cnt.num between fromcount_ and pagecount_)
    group by t3.legal_entity_id, t3.domain_id
    order by t1.legal_entity_name;
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

    select count(distinct t1.legal_entity_id) as total_record
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
    (select contact_no from tbl_client_users where user_category_id = 3 and client_id = t1.client_id and t1.legal_entity_id in (legal_entity_ids)) as le_admin_contactno,
    (select email_id from tbl_client_users where user_category_id = 3 and client_id = t1.client_id and t1.legal_entity_id in (legal_entity_ids)) as le_admin_email
    from tbl_legal_entities t1
    inner join tbl_client_groups t2 on t1.client_id = t2.client_id
    inner join tbl_legal_entity_domains t3 on t1.legal_entity_id = t3.legal_entity_id
    left join tbl_business_groups t4 on t1.business_group_id = t4.business_group_id
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
        IF(ts.parent_names = '', ts.statutory_name, SUBSTRING_INDEX(ts.parent_names, '>>', 1)) as statutory_name,
        tc.compliance_task,
        tc.compliance_description as description,
        SUBSTRING_INDEX(tsnl.notification_text,'remarks',-1) as notification_text,
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
        IF(statutoryid_ IS NOT NULL, (ts.statutory_id = statutoryid_  or ts.parent_ids in (statutoryid_)), 1) AND
        IF(fromdate_ IS NOT NULL, DATE(tsnl.created_on) >= fromdate_, 1) AND
        IF(todate_ IS NOT NULL, DATE(tsnl.created_on) <= todate_, 1)
    group by tc.statutory_mapping_id, tc.compliance_id
    order by tsnl.created_on desc
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
    SELECT COUNT(distinct tc.compliance_id) as total_record
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
    IF(statutoryid_ IS NOT NULL, (ts.statutory_id = statutoryid_  or ts.parent_ids in (statutoryid_)), 1) AND
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
    END IF ;

END //

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
-- To get list of client statutories assign statutotry procs
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_clientstatutories_list_count`;

DELIMITER //

CREATE PROCEDURE `sp_clientstatutories_list_count`(
    IN uid INT(11)
)

BEGIN
    select count(distinct t.client_statutory_id) as r_count
    from tbl_client_statutories as t
    inner join tbl_client_compliances as t1 on t1.client_statutory_id = t.client_statutory_id
    inner join tbl_user_units as t3 on t1.unit_id = t3.unit_id and t1.domain_id = t3.domain_id and t3.user_id = uid
    inner join tbl_units as t2 on t1.unit_id = t2.unit_id
    
    where t3.user_id = uid;
END //

DELIMITER ;

-- --------------------------------------------------------------------------------
-- To get list of client statutories assign statutotry procs
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_clientstatutories_list`;

DELIMITER //

CREATE PROCEDURE `sp_clientstatutories_list`(
    IN uid INT(11), IN fromcount INT(11), IN tocount INT(11)
)

BEGIN
    select distinct t.client_statutory_id, t.client_id, t2.legal_entity_id, t.unit_id, t1.domain_id, t2.unit_name, t2.unit_code,
    (select domain_name from tbl_domains where domain_id = t1.domain_id) as domain_name,
    (select country_name from tbl_countries where country_id = t2.country_id) as country_name,
    (select group_name from tbl_client_groups where client_id = t.client_id) as group_name,
    (select business_group_name from tbl_business_groups where business_group_id = t2.business_group_id) as business_group_name,
    (select legal_entity_name from tbl_legal_entities where legal_entity_id = t2.legal_entity_id) as legal_entity_name,
    (select division_name from tbl_divisions where division_id = t2.division_id) as division_name,
    (select category_name from tbl_categories where category_id = t2.category_id) as category_name,
    (select geography_name from tbl_geographies where geography_id = t2.geography_id) as geography_name ,
    t.status, t.reason,
    t4.is_edit
    from tbl_client_statutories as t
    inner join tbl_client_compliances as t1 on t1.client_statutory_id = t.client_statutory_id
    inner join tbl_user_units as t3 on t1.unit_id = t3.unit_id and t1.domain_id = t3.domain_id and t3.user_id = uid
    inner join tbl_units as t2 on t1.unit_id = t2.unit_id
    left join (select count(compliance_id) as is_edit,client_statutory_id,unit_id  from tbl_client_compliances where
     (is_approved < 5 or IFNULL(compliance_applicable_status,0) = 3 ) group by client_statutory_id,unit_id) as t4
     on t1.client_statutory_id = t4.client_statutory_id and t1.unit_id = t4.unit_id
    where t3.user_id = uid
    group by t.unit_id, t1.domain_id
    order by t.client_id, t2.unit_code
    limit fromcount, tocount;
END //

DELIMITER ;

DROP PROCEDURE IF EXISTS `sp_clientstatutories_approvelist`;

DELIMITER //

CREATE PROCEDURE `sp_clientstatutories_approvelist`(
    IN uid INT(11)
)
BEGIN

    select t1.client_statutory_id, t1.client_id, t2.legal_entity_id, t1.unit_id, t1.domain_id, t2.unit_name, t2.unit_code,
    (select domain_name from tbl_domains where domain_id = t1.domain_id) as domain_name,
    (select country_name from tbl_countries where country_id = t2.country_id) as country_name,
    (select group_name from tbl_client_groups where client_id = t1.client_id) as group_name,
    (select business_group_name from tbl_business_groups where business_group_id = t2.business_group_id) as business_group_name,
    (select legal_entity_name from tbl_legal_entities where legal_entity_id = t2.legal_entity_id) as legal_entity_name,
    (select division_name from tbl_divisions where division_id = t2.division_id) as division_name,
    (select category_name from tbl_categories where category_id = t2.category_id) as category_name,
    (select geography_name from tbl_geographies where geography_id = t2.geography_id) as geography_name ,
    t.status, t.reason
    from tbl_client_statutories as t
    inner join tbl_client_compliances as t1 on t.client_statutory_id = t1.client_statutory_id
    inner join tbl_units as t2 on t1.unit_id = t2.unit_id
    inner join tbl_user_units as t3 on t3.unit_id = t1.unit_id
    where t.status = 2 and t3.user_id = uid and t1.is_approved = 2
    group by t1.unit_id, t1.domain_id;

END //

DELIMITER ;


DROP PROCEDURE IF EXISTS `sp_clientstatutories_approvelist_count`;

DELIMITER //

CREATE PROCEDURE `sp_clientstatutories_approvelist_count`(
    IN unitid INT(11), domainid INT(11), cs_id INT(11)
)
BEGIN

    select count(1) as r_count from tbl_client_compliances t4
    inner join tbl_compliances as t5 on t5.compliance_id = t4.compliance_id
    where t4.is_approved = 2 and t5.is_approved in (2, 3) and
    t4.client_statutory_id = cs_id and t4.unit_id = unitid and t4.domain_id = domainid;

END //

DELIMITER ;


DROP PROCEDURE IF EXISTS `sp_clientstatutories_filters`;

DELIMITER //

CREATE PROCEDURE `sp_clientstatutories_filters`(
    IN uid INT(11)
)
BEGIN
    -- group details
    select distinct t1.client_id, t1.group_name, t1.short_name, t1.is_active
     from tbl_client_groups as t1
     inner join tbl_user_units as t2
     on t1.client_id = t2.client_id where t2.user_id = uid;

    -- legal entity details
    select distinct t1.client_id, t1.legal_entity_id, t1.legal_entity_name, t1.business_group_id
     from tbl_legal_entities as t1
     inner join tbl_user_units as t2
     on t1.legal_entity_id = t2.legal_entity_id where t2.user_id = uid;

    -- business group details
    select distinct t1.client_id, t1.business_group_id, t1.business_group_name
     from tbl_business_groups as t1
     inner join tbl_units as t2 on t1.business_group_id = t2.business_group_id
     inner join tbl_user_units as t3 on t2.unit_id = t3.unit_id
     where t3.user_id = uid;
    -- division
    select distinct t1.client_id, t1.division_id, t1.division_name, t1.legal_entity_id,
    t1.business_group_id
     from tbl_divisions as t1
     inner join tbl_units as t2 on t1.division_id = t2.division_id
     inner join tbl_user_units as t3 on t2.unit_id = t3.unit_id
     where t3.user_id = uid;
    -- category
    select distinct t1.client_id, t1.category_id, t1.category_name, t1.legal_entity_id,
    t1.business_group_id, t1.division_id
     from tbl_categories as t1
     inner join tbl_units as t2 on t1.category_id = t2.category_id
     inner join tbl_user_units as t3 on t2.unit_id = t3.unit_id
     where t3.user_id = uid;

    -- domains
    select distinct t1.domain_name, t3.domain_id, t3.legal_entity_id
     from tbl_domains as t1
     inner join tbl_user_units as t3 on t1.domain_id = t3.domain_id
     where t3.user_id = uid;


END //

DELIMITER ;


DROP PROCEDURE IF EXISTS `sp_clientstatutories_units`;

DELIMITER //

CREATE PROCEDURE `sp_clientstatutories_units`(
    IN uid INT(11), cid INT(11), bid varchar(10), lid int(11),
    divid varchar(11), catid varchar(11), domainid INT(11)
)
BEGIN
    select t1.unit_id, t1.unit_code, t1.unit_name, t1.address,t7.geography_name ,t6.client_statutory_id
    from tbl_units t1
    inner join tbl_units_organizations t2 on t1.unit_id = t2.unit_id
    inner join tbl_user_units t3 on t1.unit_id = t3.unit_id and t3.domain_id = t2.domain_id
    inner join tbl_compliances t4 on t1.country_id = t4.country_id and t2.domain_id = t4.domain_id
    inner join tbl_mapped_locations as t5 on t4.statutory_mapping_id = t5.statutory_mapping_id
    inner join tbl_geographies t7 on t5.geography_id = t7.geography_id
        and (t1.geography_id = t7.geography_id OR find_in_set(t1.geography_id,t7.parent_ids))
    inner join tbl_mapped_industries as t8 on t4.statutory_mapping_id = t8.statutory_mapping_id and t8.organisation_id = t2.organisation_id
    left join tbl_client_compliances t6 on t6.compliance_id = t4.compliance_id
        and t1.unit_id = t6.unit_id and t2.domain_id = t6.domain_id
    Where   t3.user_id = uid and t1.client_id = cid and t1.legal_entity_id = lid and t2.domain_id = domainid
        and t4.is_active = 1 and t4.is_approved in (2, 3)
        and t1.is_closed = 0 and t1.is_approved != 2
        and IFNULL(t1.business_group_id, 0) like bid and IFNULL(t1.division_id, 0) like divid
        and IFNULL(t1.category_id,0) like catid
        and t6.compliance_id is null and IFNULL(t6.is_approved,0) != 5
    group by t1.unit_id
    order by t1.unit_code, t1.unit_name;
END //

DELIMITER ;


DROP PROCEDURE IF EXISTS `sp_clientstatutories_compliance_count`;

DELIMITER //

CREATE PROCEDURE `sp_clientstatutories_compliance_count`(
    IN unitid text, domainid int(11)
)
BEGIN

    select count(distinct t1.compliance_id) as total, count(distinct t4.unit_id, t1.compliance_id) as u_total
    from tbl_compliances as t1
    inner join tbl_statutory_mappings as t on t1.statutory_mapping_id = t.statutory_mapping_id
    inner join tbl_mapped_industries as t2 on t1.statutory_mapping_id = t2.statutory_mapping_id
    inner join tbl_mapped_locations as t3 on t1.statutory_mapping_id = t3.statutory_mapping_id
    inner join tbl_units as t4 on t4.country_id = t1.country_id
    inner join tbl_units_organizations as t5 on t4.unit_id = t5.unit_id  and t5.domain_id = t1.domain_id
    and t5.organisation_id = t2.organisation_id
    left join tbl_client_compliances t6 on t6.compliance_id = t1.compliance_id
    and t4.unit_id = t6.unit_id and t.domain_id = t6.domain_id
    inner join (select a.geography_id,b.parent_ids,a.unit_id from tbl_units a
        inner join tbl_geographies b on a.geography_id = b.geography_id
        where find_in_set (a.unit_id, unitid)) t7 on t7.unit_id = t4.unit_id and t7.geography_id = t3.geography_id
        and (t4.geography_id = t7.geography_id or find_in_set(t4.geography_id,t7.parent_ids))

    where t1.is_active = 1 and t1.is_approved in (2, 3) and find_in_set(t4.unit_id, unitid) and t1.domain_id = domainid
    and IFNULL(t6.is_approved, 0) != 5;

END //
DELIMITER ;


DROP PROCEDURE IF EXISTS `sp_clientstatutories_compliance_new`;

DELIMITER //

CREATE PROCEDURE `sp_clientstatutories_compliance_new`(
    IN unitid text, domainid INT(11), fromcount INT(11), tocount INT(11)
)
BEGIN
    -- mapped statu names
    select t2.statutory_name, t1.statutory_id, IFNULL(t2.parent_ids, 0) as parent_ids, t2.parent_names, t1.statutory_mapping_id
    from tbl_mapped_statutories as t1 inner join tbl_statutories as t2
    on t1.statutory_id = t2.statutory_id
    inner join tbl_statutory_mappings as t3 on t1.statutory_mapping_id = t3.statutory_mapping_id
    inner join tbl_mapped_locations as t4 on t1.statutory_mapping_id = t4.statutory_mapping_id
    inner join (select a.geography_id,b.parent_ids,a.unit_id from tbl_units a
        inner join tbl_geographies b on a.geography_id = b.geography_id
        where find_in_set(a.unit_id, unitid)) t7 on (t4.geography_id = t7.geography_id or find_in_set(t4.geography_id,t7.parent_ids))
    order by TRIM(LEADING '[' FROM t3.statutory_mapping);

    -- mapped organistaion
    select distinct t2.organisation_name, t1.organisation_id, t1.statutory_mapping_id
    from tbl_mapped_industries as t1 inner join tbl_organisation as t2
    on t1.organisation_id = t2.organisation_id
    inner join tbl_statutory_mappings as t3 on t1.statutory_mapping_id = t3.statutory_mapping_id
    inner join tbl_mapped_locations as t4 on t1.statutory_mapping_id = t4.statutory_mapping_id
    inner join (select a.geography_id,b.parent_ids,a.unit_id from tbl_units a
        inner join tbl_geographies b on a.geography_id = b.geography_id
        where find_in_set(a.unit_id, unitid)) t7 on (t4.geography_id = t7.geography_id or find_in_set(t4.geography_id,t7.parent_ids))
    order by TRIM(LEADING '[' FROM t3.statutory_mapping);

    -- new and assigned compliance
    select distinct t1.statutory_mapping_id, t1.compliance_id,
    t1.compliance_task, t1.document_name,
    t1.compliance_description, t1.statutory_provision,
    t.statutory_mapping,
    t6.unit_id, t6.domain_id, t6.compliance_id as assigned_compid,
    t6.statutory_id, t6.statutory_applicable_status, t6.remarks,
    t6.compliance_applicable_status, t6.is_approved,
    t4.unit_id as c_unit_id
    from tbl_compliances as t1
    inner join tbl_statutory_mappings as t on t1.statutory_mapping_id = t.statutory_mapping_id
    inner join tbl_mapped_industries as t2 on t1.statutory_mapping_id = t2.statutory_mapping_id
    inner join tbl_mapped_locations as t3 on t1.statutory_mapping_id = t3.statutory_mapping_id
    inner join tbl_units as t4 on t4.country_id = t1.country_id
    inner join tbl_units_organizations as t5 on t4.unit_id = t5.unit_id  and t5.domain_id = t1.domain_id
    and t5.organisation_id = t2.organisation_id
    left join tbl_client_compliances t6 on t6.compliance_id = t1.compliance_id
    and t4.unit_id = t6.unit_id and t.domain_id = t6.domain_id
    inner join (select a.geography_id,b.parent_ids,a.unit_id from tbl_units a
            inner join tbl_geographies b on a.geography_id = b.geography_id
            where find_in_set(a.unit_id, unitid)) t7 on t7.unit_id = t4.unit_id and t7.geography_id = t3.geography_id
            and (t4.geography_id = t7.geography_id or find_in_set(t4.geography_id,t7.parent_ids))

     where t1.is_active = 1 and t1.is_approved in (2, 3) and find_in_set (t4.unit_id, unitid) and t1.domain_id = domainid
     and IFNULL(t6.is_approved, 0) != 5
    order by TRIM(LEADING '[' FROM t.statutory_mapping), t1.compliance_id, t4.unit_id
    limit fromcount, tocount;

END //

DELIMITER ;



DROP PROCEDURE IF EXISTS `sp_clientstatutories_compliance_to_approve`;

DELIMITER //

CREATE PROCEDURE `sp_clientstatutories_compliance_to_approve`(
    IN unitid INT(11), domainid INT(11), fromcount INT(11), tocount INT(11)
)
BEGIN
    -- unit location
    select @gid := geography_id from tbl_units where unit_id = unitid;
    -- mapped statu names
    select t2.statutory_name, t1.statutory_id, IFNULL(t2.parent_ids, 0) as parent_ids, t2.parent_names, t1.statutory_mapping_id
    from tbl_mapped_statutories as t1 inner join tbl_statutories as t2
    on t1.statutory_id = t2.statutory_id
    inner join tbl_statutory_mappings as t3 on t1.statutory_mapping_id = t3.statutory_mapping_id
    inner join tbl_mapped_locations as t4 on t1.statutory_mapping_id = t4.statutory_mapping_id
    where t4.geography_id IN
    (select geography_id from tbl_geographies where geography_id = @gid or find_in_set(geography_id,
    (select parent_ids from tbl_geographies where geography_id = @gid)))
    order by TRIM(LEADING '[' FROM t3.statutory_mapping);
    -- mapped organistaion
    select t2.organisation_name, t1.organisation_id, t1.statutory_mapping_id
    from tbl_mapped_industries as t1 inner join tbl_organisation as t2
    on t1.organisation_id = t2.organisation_id
    inner join tbl_statutory_mappings as t3 on t1.statutory_mapping_id = t3.statutory_mapping_id
    inner join tbl_mapped_locations as t4 on t1.statutory_mapping_id = t4.statutory_mapping_id
    where t4.geography_id IN
    (select geography_id from tbl_geographies where geography_id = @gid or find_in_set(geography_id,
    (select parent_ids from tbl_geographies where geography_id = @gid)))
    order by TRIM(LEADING '[' FROM t3.statutory_mapping);

    -- only assigned compliance
    select distinct t1.statutory_mapping_id, t1.compliance_id,
    t1.compliance_task, t1.document_name,
    t1.compliance_description, t1.statutory_provision,
    t.statutory_mapping,
    t6.unit_id, t6.domain_id, t6.compliance_id as assigned_compid,
    t6.statutory_id, t6.statutory_applicable_status, t6.remarks,
    t6.compliance_applicable_status, t6.is_approved
    from tbl_compliances as t1
    inner join tbl_statutory_mappings as t on t1.statutory_mapping_id = t.statutory_mapping_id
    inner join tbl_mapped_industries as t2 on t1.statutory_mapping_id = t2.statutory_mapping_id
    inner join tbl_mapped_locations as t3 on t1.statutory_mapping_id = t3.statutory_mapping_id
    inner join tbl_units as t4 on t4.country_id = t1.country_id
    inner join tbl_units_organizations as t5 on t4.unit_id = t5.unit_id  and t5.domain_id = t1.domain_id
    and t5.organisation_id = t2.organisation_id
    inner join tbl_client_compliances t6 on t6.compliance_id = t1.compliance_id
    and t4.unit_id = t6.unit_id and t.domain_id = t6.domain_id
     where t1.is_active = 1 and t1.is_approved in (2, 3) and t4.unit_id = unitid and t1.domain_id = domainid
     and IFNULL(t6.is_approved, 0) = 2
     order by TRIM(LEADING '[' FROM t.statutory_mapping), t4.unit_id
    limit fromcount, tocount;

END //

DELIMITER ;


DROP PROCEDURE IF EXISTS `sp_clientstatutories_compliance_edit`;

DELIMITER //

CREATE PROCEDURE `sp_clientstatutories_compliance_edit`(
    IN unitid INT(11), domainid INT(11), fromcount INT(11), tocount INT(11)
)
BEGIN

    -- unit location
    select @gid := geography_id from tbl_units where unit_id = unitid;

    -- mapped statu names
    select t2.statutory_name, t1.statutory_id, IFNULL(t2.parent_ids, 0) as parent_ids, t2.parent_names, t1.statutory_mapping_id
    from tbl_mapped_statutories as t1 inner join tbl_statutories as t2
    on t1.statutory_id = t2.statutory_id
    inner join tbl_statutory_mappings as t3 on t1.statutory_mapping_id = t3.statutory_mapping_id
    inner join tbl_mapped_locations as t4 on t1.statutory_mapping_id = t4.statutory_mapping_id
    where t4.geography_id IN
    (select geography_id from tbl_geographies where geography_id = @gid or find_in_set(geography_id,
    (select parent_ids from tbl_geographies where geography_id = @gid)));

    -- mapped organistaion
    select t2.organisation_name, t1.organisation_id, t1.statutory_mapping_id
    from tbl_mapped_industries as t1 inner join tbl_organisation as t2
    on t1.organisation_id = t2.organisation_id
    inner join tbl_statutory_mappings as t3 on t1.statutory_mapping_id = t3.statutory_mapping_id
    inner join tbl_mapped_locations as t4 on t1.statutory_mapping_id = t4.statutory_mapping_id
    where t4.geography_id IN
    (select geography_id from tbl_geographies where geography_id = @gid or find_in_set(geography_id,
    (select parent_ids from tbl_geographies where geography_id = @gid)));


    -- new and assigned compliance
    select distinct t1.statutory_mapping_id, t1.compliance_id,
    t1.compliance_task, t1.document_name,
    t1.compliance_description, t1.statutory_provision,
    t.statutory_mapping,
    t6.unit_id, t6.domain_id, t6.compliance_id as assigned_compid,
    t6.statutory_id, t6.statutory_applicable_status, t6.remarks,
    t6.compliance_applicable_status, t6.is_approved
    from tbl_compliances as t1
    inner join tbl_statutory_mappings as t on t1.statutory_mapping_id = t.statutory_mapping_id
    inner join tbl_mapped_industries as t2 on t1.statutory_mapping_id = t2.statutory_mapping_id
    inner join tbl_mapped_locations as t3 on t1.statutory_mapping_id = t3.statutory_mapping_id
    inner join tbl_units as t4 on t4.country_id = t1.country_id
    inner join tbl_units_organizations as t5 on t4.unit_id = t5.unit_id  and t5.domain_id = t1.domain_id
    and t5.organisation_id = t2.organisation_id
    left join tbl_client_compliances t6 on t6.compliance_id = t1.compliance_id
    and t4.unit_id = t6.unit_id and t.domain_id = t6.domain_id and t6.is_approved > 5
     where t1.is_active = 1 and t1.is_approved in (2, 3) and t4.unit_id = unitid and t1.domain_id = domainid
     and t3.geography_id IN
     (select geography_id from tbl_geographies where geography_id = @gid or find_in_set(geography_id,
        (select parent_ids from tbl_geographies where geography_id = @gid)))
    order by t.statutory_mapping, t4.unit_id
    limit fromcount, tocount;


    select count(distinct t1.compliance_id) as total
    from tbl_compliances as t1
    inner join tbl_statutory_mappings as t on t1.statutory_mapping_id = t.statutory_mapping_id
    inner join tbl_mapped_industries as t2 on t1.statutory_mapping_id = t2.statutory_mapping_id
    inner join tbl_mapped_locations as t3 on t1.statutory_mapping_id = t3.statutory_mapping_id
    inner join tbl_units as t4 on t4.country_id = t1.country_id
    inner join tbl_units_organizations as t5 on t4.unit_id = t5.unit_id  and t5.domain_id = t1.domain_id
    and t5.organisation_id = t2.organisation_id
    left join tbl_client_compliances t6 on t6.compliance_id = t1.compliance_id
    and t4.unit_id = t6.unit_id and t.domain_id = t6.domain_id and t6.is_approved > 5
     where t1.is_active = 1 and t1.is_approved in (2, 3) and t4.unit_id = unitid and t1.domain_id = domainid
     and t3.geography_id IN
     (select geography_id from tbl_geographies where geography_id = @gid or find_in_set(geography_id,
        (select parent_ids from tbl_geographies where geography_id = @gid)))
    order by t.statutory_mapping, t4.unit_id;


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

    select distinct t1.domain_id, t1.country_id, t3.domain_name, t3.is_active from
    tbl_domain_countries as t1
    inner join tbl_domains as t3 on t3.domain_id = t1.domain_id
    inner join tbl_statutory_levels as t4 on t3.domain_id = t4.domain_id
    and t1.country_id = t4.country_id
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
    order by t2.level_position, geography_name;
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
    order by t2.level_position, t1.statutory_name;


END //

DELIMITER ;

DROP PROCEDURE IF EXISTS `sp_tbl_statutory_mapping_list`;

DELIMITER //

CREATE PROCEDURE `sp_tbl_statutory_mapping_list`(
    IN userid INT(11), approvestatus varchar(1), activestatus varchar(1),
    fromcount INT(11), tocount INT(11)
)
BEGIN
    if approvestatus = 6 then
        set approvestatus = '%';
    end if;

    select t1.statutory_mapping_id, t2.country_id, t2.domain_id, t2.statutory_nature_id, t1.compliance_id, t1.compliance_task, t1.document_name,
    t1.is_active as c_is_active, t1.is_approved as c_is_approved, t1.remarks,
    t2.is_active, t2.is_approved,
    (select country_name from tbl_countries where country_id = t1.country_id) as country_name,
    (select domain_name from tbl_domains where domain_id = t1.domain_id) as domain_name,
    (select statutory_nature_name from tbl_statutory_natures where statutory_nature_id = t2.statutory_nature_id) as nature

    from tbl_compliances as t1
    inner join tbl_statutory_mappings as t2 on t1.statutory_mapping_id = t2.statutory_mapping_id
    inner join tbl_user_domains as t3 on t3.domain_id = t1.domain_id and
    t3.country_id = t1.country_id
    where t3.user_id = userid and t1.is_approved like approvestatus
    and t1.is_active like activestatus
    order by country_name, domain_name, t1.statutory_mapping_id, compliance_id
    limit fromcount, tocount;

    select distinct t1.statutory_mapping_id, t1.organisation_id,
    (select organisation_name from tbl_organisation where organisation_id = t1.organisation_id) as organisation_name
    from tbl_mapped_industries as t1
    inner join tbl_compliances as t2 on t1.statutory_mapping_id = t2.statutory_mapping_id
    inner join tbl_user_domains as t4 on t4.domain_id = t2.domain_id and
    t4.country_id = t2.country_id
    where t4.user_id = userid;

    select distinct t1.statutory_mapping_id, t1.statutory_id,
    t3.statutory_name, t3.parent_names
    from tbl_mapped_statutories as t1
    inner join tbl_compliances as t2 on t1.statutory_mapping_id = t2.statutory_mapping_id
    inner join tbl_statutories as t3 on t1.statutory_id = t3.statutory_id
    inner join tbl_user_domains as t4 on t4.domain_id = t2.domain_id  and
    t4.country_id = t2.country_id
    where t4.user_id = userid;

    select distinct t1.statutory_mapping_id, t1.geography_id,
    (select parent_names from tbl_geographies where geography_id = t1.geography_id) as geography_name
    from tbl_mapped_locations as t1
    inner join tbl_compliances as t2 on t1.statutory_mapping_id = t2.statutory_mapping_id
    inner join tbl_user_domains as t4 on t4.domain_id = t2.domain_id and
    t4.country_id = t2.country_id
    where t4.user_id = userid;

    select count( distinct t1.compliance_id) as total
    from tbl_compliances as t1
    inner join tbl_user_domains as t3 on t3.domain_id = t1.domain_id and
    t3.country_id = t1.country_id and t1.is_approved like approvestatus
    and t1.is_active like activestatus
    where t3.user_id = userid;

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
        tu.country_id, tu.division_id,
        td.division_name, tc.category_id,
        tc.category_name
        from
        tbl_units as tu
        left join tbl_divisions as td on
        td.division_id = tu.division_id
        left join tbl_categories as tc on tc.category_id = tu.category_id;
        -- where

        -- tu.unit_id in (select distinct(unit_id) from tbl_user_units);
    end if;

    if(userCatgId = 5)then
        select tu.unit_id, concat(tu.unit_code,' - ',tu.unit_name) as unit_name, tu.client_id,
        tu.business_group_id, tu.legal_entity_id,
        tu.country_id, td.division_id, td.division_name, tc.category_id,
        tc.category_name
        from
        tbl_user_clients as tuc inner join tbl_units as tu
        on tu.client_id = tuc.client_id
        left join tbl_divisions as td on
        td.division_id = tu.division_id
        left join tbl_categories as tc on tc.category_id = tu.category_id
        where
        tuc.user_id = userId;
    end if;
    if(userCatgId = 7 or userCatgId = 8)then
        select tu.unit_id, concat(tu.unit_code,' - ',tu.unit_name) as unit_name, tu.client_id,
        tu.business_group_id, tu.legal_entity_id,
        tu.country_id, td.division_id, td.division_name, tc.category_id,
        tc.category_name
        from
        tbl_user_units as tuu inner join tbl_units as tu
        on tu.unit_id = tuu.unit_id
        left join tbl_divisions as td on
        td.division_id = tu.division_id
        left join tbl_categories as tc on tc.category_id = tu.category_id
        where
        tuu.user_id = userId and tuu.user_category_id = userCatgId;
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
        select tcg.client_id, tcg.group_name as client_name, tle.legal_entity_id, tle.country_id,
        tle.business_group_id
        from
        tbl_client_groups as tcg inner join tbl_legal_entities as tle on
        tle.is_closed != 1 and tle.client_id = tcg.client_id
        where
        tcg.is_active = 1;
        -- tcg.is_approved = 1 and
    end if;
    if(userCatgId = 5)then
        select tcg.client_id, tcg.group_name as client_name, tle.legal_entity_id, tle.country_id,
        tle.business_group_id
        from
        tbl_user_clients as tuc inner join tbl_client_groups as tcg on
        tcg.is_active = 1 and tcg.client_id = tuc.client_id inner join
        tbl_legal_entities as tle on tle.is_closed != 1 and
        tle.client_id = tcg.client_id
        where
        -- tcg.is_approved = 1 and
        tuc.user_id = userId and tuc.user_category_id = userCatgId;
    end if;
    if(userCatgId = 6)then
        select tcg.client_id, tcg.group_name as client_name, tle.legal_entity_id, tle.country_id,
        tle.business_group_id
        from
        tbl_user_legalentity as tul inner join tbl_client_groups as tcg on
        tcg.is_active = 1 and tcg.client_id = tul.client_id inner join
        tbl_legal_entities as tle on tle.is_closed != 1 and
        tle.client_id = tcg.client_id
        where
        -- tcg.is_approved = 1 and
        tul.user_id = userId;
    end if;
    if(userCatgId = 7 or userCatgId = 8)then
        select tcg.client_id, tcg.group_name as client_name, tle.legal_entity_id, tle.country_id,
        tle.business_group_id
        from
        tbl_client_groups as tcg inner join tbl_legal_entities as tle on
        tle.is_closed != 1 and tle.client_id = tcg.client_id
        where
        -- tcg.is_approved = 1 and
        tcg.is_active = 1 and
        tcg.client_id in (select distinct(client_id) from tbl_user_units
        where user_id = userId);
    end if;

END //

DELIMITER ;

-- --------------------------------------------------------------------------------
-- user mapping report - report details/data
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_usermapping_report_details`;

DELIMITER //

CREATE PROCEDURE `sp_usermapping_report_details`(
    in userId int(11), clientId int(11), legalId int(11), counrtyId int(11),
    bgrp_id varchar(10), _divi_id varchar(11), _cg_id varchar(11), _unit_id varchar(11),
    IN fromcount_ INT(11), IN pagecount_ INT(11))
BEGIN
    SELECT @_user_category_id := user_category_id as user_category_id
    FROM tbl_user_login_details WHERE user_id = userId;

    if(@_user_category_id = 1)then
        select t4.unit_id, concat(t_mgr.employee_code,'-',t_mgr.employee_name) as techno_manager,
        concat(t_usr.employee_code,'-',t_usr.employee_name) as techno_user,
        (select concat(unit_code,'-',unit_name) from tbl_units where unit_id = t4.unit_id) as unit_name
        from
        tbl_user_legalentity as t1 inner join tbl_user_clients as t2
        on t2.client_id = t1.client_id
        inner join tbl_legal_entities as t3 on t3.client_id = t1.client_id and
        t3.legal_entity_id = t1.legal_entity_id
        inner join tbl_users as t_mgr on t_mgr.user_id = t2.user_id
        inner join tbl_users as t_usr on t_usr.user_id = t1.user_id
        inner join tbl_units as t4 on t4.client_id = t1.client_id and
        t4.legal_entity_id = t3.legal_entity_id and t4.country_id = t3.country_id
        where
        coalesce(t4.category_id,'') like _cg_id and coalesce(t4.division_id,'') like _divi_id and
        coalesce(t4.unit_id,'')like _unit_id and coalesce(t4.business_group_id,'') like bgrp_id and
        t3.country_id = counrtyId and
        coalesce(t3.business_group_id,'') like bgrp_id and
        t1.legal_entity_id = legalId and
        t1.client_id = clientId
        -- group by t1.user_id
        limit fromcount_, pagecount_;

        select t1.unit_id, concat(t2.employee_code,'-',t2.employee_name)as employee_name,
        t3.user_category_name,t1.domain_id
        from
        tbl_user_units as t1 inner join tbl_units as t4 on
        coalesce(t4.category_id,'') like _cg_id and coalesce(t4.division_id,'') like _divi_id and
        t4.unit_id = t1.unit_id and t4.country_id = counrtyId inner join
        tbl_users as t2 on t2.user_id = t1.user_id inner join
        tbl_user_category as t3 on t3.user_category_id = t1.user_category_id
        where
        coalesce(t1.unit_id,'') like _unit_id and
        t1.legal_entity_id =legalId and
        t1.client_id = clientId;

        select distinct(t3.domain_id),t3.domain_name,t3.is_active
        from
        tbl_user_units as t1 inner join tbl_units_organizations as t2 on
        t2.unit_id = t1.unit_id inner join tbl_domains as t3 on
        t3.domain_id = t2.domain_id
        where
        coalesce(t1.unit_id,'') like _unit_id and
        t1.legal_entity_id =legalId and
        t1.client_id = clientId
        order by t3.domain_name;

        select count(0) as total_count
        from
        tbl_user_legalentity as t1 inner join tbl_user_clients as t2
        on t2.client_id = t1.client_id
        inner join tbl_legal_entities as t3 on t3.client_id = t1.client_id and
        t3.legal_entity_id = t1.legal_entity_id
        inner join tbl_users as t_mgr on t_mgr.user_id = t2.user_id
        inner join tbl_users as t_usr on t_usr.user_id = t1.user_id
        inner join tbl_units as t4 on t4.client_id = t1.client_id and
        t4.legal_entity_id = t3.legal_entity_id and t4.country_id = t3.country_id
        where
        coalesce(t4.category_id,'') like _cg_id and coalesce(t4.division_id,'') like _divi_id and
        coalesce(t4.unit_id,'')like _unit_id and coalesce(t4.business_group_id,'') like bgrp_id and
        t3.country_id = counrtyId and
        coalesce(t3.business_group_id,'') like bgrp_id and
        t1.legal_entity_id = legalId and
        t1.client_id = clientId;
        -- group by t1.user_id

    elseif (@_user_category_id = 5)then
        select t4.unit_id, concat(t_mgr.employee_code,'-',t_mgr.employee_name) as techno_manager,
        concat(t_usr.employee_code,'-',t_usr.employee_name) as techno_user,
        (select concat(unit_code,'-',unit_name) from tbl_units where unit_id = t4.unit_id) as unit_name
        from
        tbl_user_legalentity as t1 inner join tbl_user_clients as t2
        on t2.client_id = t1.client_id
        inner join tbl_legal_entities as t3 on t3.client_id = t1.client_id and
        t3.legal_entity_id = t1.legal_entity_id
        inner join tbl_users as t_mgr on t_mgr.user_id = t2.user_id
        inner join tbl_users as t_usr on t_usr.user_id = t1.user_id
        inner join tbl_units as t4 on t4.client_id = t1.client_id and
        t4.legal_entity_id = t3.legal_entity_id and t4.country_id = t3.country_id
        where
        coalesce(t4.category_id,'') like _cg_id and coalesce(t4.division_id,'') like _divi_id and
        coalesce(t4.unit_id,'')like _unit_id and coalesce(t4.business_group_id,'') like bgrp_id and
        t3.country_id = counrtyId and
        coalesce(t3.business_group_id,'') like bgrp_id and
        t1.legal_entity_id = legalId and
        t1.client_id = clientId
        -- group by t1.user_id
        limit fromcount_, pagecount_;

        select t1.unit_id, concat(t2.employee_code,'-',t2.employee_name)as employee_name,
        t3.user_category_name,t1.domain_id
        from
        tbl_user_units as t1 inner join tbl_units as t4 on
        coalesce(t4.category_id,'') like _cg_id and
        coalesce(t4.division_id,'') like _divi_id and
        t4.unit_id = t1.unit_id inner join tbl_users as t2 on
        t2.user_id = t1.user_id inner join tbl_user_category as t3 on
        t3.user_category_id = t1.user_category_id
        where
        t4.country_id = counrtyId and
        coalesce(t1.unit_id,'') like _unit_id and
        t1.legal_entity_id =legalId and
        t1.client_id = clientId;

        select distinct(t3.domain_id),t3.domain_name,t3.is_active
        from
        tbl_user_units as t1 inner join tbl_units_organizations as t2 on
        t2.unit_id = t1.unit_id inner join tbl_domains as t3 on
        t3.domain_id = t2.domain_id
        where
        coalesce(t1.unit_id,'') like _unit_id and
        t1.legal_entity_id =legalId and
        t1.client_id = clientId
        order by t3.domain_name;

        select count(0) as total_count
        from
        tbl_user_legalentity as t1 inner join tbl_user_clients as t2
        on t2.client_id = t1.client_id
        inner join tbl_legal_entities as t3 on t3.client_id = t1.client_id and
        t3.legal_entity_id = t1.legal_entity_id
        inner join tbl_users as t_mgr on t_mgr.user_id = t2.user_id
        inner join tbl_users as t_usr on t_usr.user_id = t1.user_id
        inner join tbl_units as t4 on t4.client_id = t1.client_id and
        t4.legal_entity_id = t3.legal_entity_id and t4.country_id = t3.country_id
        where
        coalesce(t4.category_id,'') like _cg_id and coalesce(t4.division_id,'') like _divi_id and
        coalesce(t4.unit_id,'')like _unit_id and coalesce(t4.business_group_id,'') like bgrp_id and
        t3.country_id = counrtyId and
        coalesce(t3.business_group_id,'') like bgrp_id and
        t1.legal_entity_id = legalId and
        t1.client_id = clientId;
    elseif (@_user_category_id = 7)then
        select t4.unit_id, concat(t_mgr.employee_code,'-',t_mgr.employee_name) as techno_manager,
        concat(t_usr.employee_code,'-',t_usr.employee_name) as techno_user,
        (select concat(unit_code,'-',unit_name) from tbl_units where unit_id = t4.unit_id) as unit_name
        from
        tbl_user_units as t4 inner join tbl_units as t5 on
        t5.unit_id = t4.unit_id inner join tbl_user_clients as t2 on
        t2.client_id = t4.client_id
        inner join tbl_user_legalentity as t1 on t1.legal_entity_id = t4.legal_entity_id
        inner join tbl_users as t_mgr on t_mgr.user_id = t2.user_id
        inner join tbl_users as t_usr on t_usr.user_id = t1.user_id
        where
        coalesce(t5.category_id,'') like _cg_id and coalesce(t5.division_id,'') like _divi_id and
        t5.country_id = counrtyId and
        coalesce(t4.unit_id,'')like _unit_id and
        coalesce(t5.business_group_id,'') like bgrp_id and
        t4.user_id = userId and t4.user_category_id = 7 and
        t4.legal_entity_id = legalId and
        t4.client_id = clientId
        group by t4.unit_id
        limit fromcount_, pagecount_;

        select t1.unit_id, concat(t2.employee_code,'-',t2.employee_name)as employee_name,
        t3.user_category_name,t1.domain_id
        from
        tbl_user_units as t1 inner join tbl_units as t4 on
        coalesce(t4.category_id,'') like _cg_id and
        coalesce(t4.division_id,'') like _divi_id and
        t4.unit_id = t1.unit_id inner join tbl_users as t2 on
        t2.user_id = t1.user_id inner join tbl_user_category as t3 on
        t3.user_category_id = t1.user_category_id
        where
        t4.country_id = counrtyId and
        coalesce(t1.unit_id,'') like _unit_id and
        t1.legal_entity_id =legalId and
        t1.client_id = clientId;

        select distinct(t3.domain_id),t3.domain_name,t3.is_active
        from
        tbl_user_units as t1 inner join tbl_units_organizations as t2 on
        t2.unit_id = t1.unit_id inner join tbl_domains as t3 on
        t3.domain_id = t2.domain_id
        where
        coalesce(t1.unit_id,'') like _unit_id and
        t1.legal_entity_id =legalId and
        t1.client_id = clientId
        order by t3.domain_name;

        select count(0) as total_count
        from
        tbl_user_units as t4 inner join tbl_units as t5 on
        t5.unit_id = t4.unit_id inner join tbl_user_clients as t2 on
        t2.client_id = t4.client_id
        inner join tbl_user_legalentity as t1 on t1.legal_entity_id = t4.legal_entity_id
        inner join tbl_users as t_mgr on t_mgr.user_id = t2.user_id
        inner join tbl_users as t_usr on t_usr.user_id = t1.user_id
        where
        coalesce(t5.category_id,'') like _cg_id and coalesce(t5.division_id,'') like _divi_id and
        t5.country_id = counrtyId and
        coalesce(t4.unit_id,'')like _unit_id and
        coalesce(t5.business_group_id,'') like bgrp_id and
        t4.user_id = userId and t4.user_category_id = 7 and
        t4.legal_entity_id = legalId and
        t4.client_id = clientId
        group by t4.unit_id;

    end if;
END //

DELIMITER ;

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

DELIMITER ;

-- --------------------------------------------------------------------------------
-- Get client groups based on user - report filter
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_client_groups_for_user`;

DELIMITER //


CREATE PROCEDURE `sp_client_groups_for_user`( IN u_id INT(11) )
BEGIN
    SELECT @u_cat_id := user_category_id from tbl_user_login_details where user_id = u_id;
    IF @u_cat_id <= 2 THEN
        SELECT t1.client_id, t1.group_name,t1.is_active, t1.is_approved
        FROM tbl_client_groups t1
        ORDER BY t1.group_name;
    END IF;

    IF @u_cat_id = 5 THEN
        SELECT t1.client_id, t1.group_name,t1.is_active, t1.is_approved
        FROM tbl_client_groups t1
        inner join tbl_user_clients t2 on t1.client_id = t2.client_id and t2.user_id = u_id
        ORDER BY t1.group_name;
    END IF;

    IF ( @u_cat_id = 7 or @u_cat_id = 8 ) THEN
        SELECT t1.client_id, t1.group_name,t1.is_active, t1.is_approved
        FROM tbl_client_groups t1
        where t1.client_id in (select distinct(client_id) from tbl_user_units
        where user_id = u_id)
        ORDER BY t1.group_name;
    END IF;

    select DISTINCT l.country_id, l.client_id from tbl_legal_entities l;
END //

DELIMITER ;

-- --------------------------------------------------------------------------------
-- Load Countries for client unit form
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_tbl_units_getCountries`;

DELIMITER //


CREATE PROCEDURE `sp_tbl_units_getCountries`(in clientId int(11), userId int(11))
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

END //

DELIMITER ;

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

END //

DELIMITER ;
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
END //

DELIMITER ;

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
END //

DELIMITER ;


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
        select t1.client_id, t1.group_name as short_name, t1.is_active, t2.country_id
        from tbl_client_groups as t1 inner join tbl_legal_entities as t2 on
        t2.client_id = t1.client_id inner join tbl_units as t3 on
        t3.client_id = t1.client_id order by t1.group_name asc;
    end if;
    if @u_cat_id = 5  THEN
        select t2.client_id, t2.group_name as short_name, t2.is_active, t3.country_id
        from tbl_user_clients as t1 inner join tbl_client_groups as t2
        on t2.client_id  = t1.client_id inner join tbl_legal_entities as t3 on
        t3.client_id = t2.client_id inner join tbl_units as t4 on
        t4.client_id = t1.client_id where
        t1.user_category_id = @u_cat_id and t1.user_id = _user_id;
    END IF;
    if @u_cat_id = 6  THEN
        select t3.client_id,t3.group_name as short_name,t3.is_active, t2.country_id
        from tbl_user_legalentity as t1 inner join tbl_legal_entities as t2 on
        t2.client_id = t1.client_id and t1.user_id = _user_id inner join
        tbl_client_groups as t3 where t3.client_id = t2.client_id
        order by t3.group_name asc;
    end if;
    if @u_cat_id = 7 or @u_cat_id = 8 THEN
        select t3.client_id,t3.group_name as short_name, t3.is_active, t2.country_id
        from tbl_user_units as t1 inner join tbl_legal_entities as t2 on
        t2.client_id = t1.client_id inner join tbl_client_groups as t3 on
        t3.client_id = t2.client_id where
        t1.user_category_id = @u_cat_id and t1.user_id = _user_id
        order by t3.group_name asc;
    end if;
END //

DELIMITER ;

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
        t2.legal_entity_id, t2.legal_entity_name, t2.country_id
        from tbl_client_groups as t1 inner join tbl_legal_entities as t2 on
        t2.client_id = t1.client_id left join tbl_business_groups as t3 on
        t3.business_group_id = t2.business_group_id inner join tbl_units as t4 on
        t4.client_id = t1.client_id and t4.legal_entity_id = t2.legal_entity_id
        order by t2.legal_entity_name asc;
    end if;
    if @u_cat_id = 5  THEN
        select t1.client_id, t3.legal_entity_id, t3.legal_entity_name, t4.business_group_id,
        t4.business_group_name, t3.country_id from tbl_user_clients as t1 inner join
        tbl_legal_entities as t3 on t3.client_id  = t1.client_id left join
        tbl_business_groups as t4 on t4.client_id = t1.client_id and
        t4.business_group_id = t3.business_group_id
        inner join tbl_units as t5 on t5.client_id = t1.client_id and
        t5.legal_entity_id = t3.legal_entity_id where
        t1.user_category_id = @u_cat_id and t1.user_id = _user_id
        order by t3.legal_entity_name asc;
    END IF;
    if @u_cat_id = 6  THEN
        select t1.client_id,t2.legal_entity_id,t2.legal_entity_name,
        t3.business_group_id, t3.business_group_name, t2.country_id
        from tbl_user_legalentity as t1 inner join tbl_legal_entities as t2 on
        t2.legal_entity_id = t1.legal_entity_id and t2.client_id = t1.client_id
        left join tbl_business_groups as t3 on t3.business_group_id = t2.business_group_id
        inner join tbl_units as t4 on t4.client_id = t1.client_id and
        t4.legal_entity_id = t2.legal_entity_id
        where t1.user_id = _user_id order by t2.legal_entity_name asc;
    end if;
    if @u_cat_id = 7 or @u_cat_id = 8 THEN
        select t1.client_id,t2.legal_entity_id,t2.legal_entity_name,
        t3.business_group_id, t3.business_group_name, t2.country_id
        from tbl_user_units as t1 inner join tbl_legal_entities as t2 on
        t2.legal_entity_id = t1.legal_entity_id and t2.client_id = t1.client_id
        left join tbl_business_groups as t3 on t3.business_group_id = t2.business_group_id
        where t1.user_category_id = @u_cat_id and t1.user_id = _user_id
        order by t2.legal_entity_name asc;
    end if;

END //

DELIMITER ;

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
        from tbl_client_groups as t1 inner join tbl_legal_entities as t2 on
        t2.client_id = t1.client_id inner join tbl_client_compliances as t3 on
        t3.legal_entity_id = t2.legal_entity_id and t3.client_id = t2.client_id
        inner join tbl_units as t4 on t4.unit_id = t3.unit_id
        order by t4.unit_name asc;
    end if;
    if @u_cat_id = 5  THEN
        select t1.client_id, t2.legal_entity_id, t3.unit_id, t4.unit_code, t4.unit_name
        from tbl_user_clients as t1 inner join tbl_legal_entities as t2 on
        t2.client_id  = t1.client_id inner join tbl_client_compliances as t3 on
        t3.client_id = t2.client_id inner join tbl_units as t4 on
        t4.unit_id = t3.unit_id and t3.legal_entity_id = t2.legal_entity_id
        where
        t1.user_category_id = @u_cat_id and t1.user_id = _user_id
        order by t4.unit_name asc;
    END IF;
    if @u_cat_id = 6  THEN
        select t1.client_id, t2.legal_entity_id, t3.unit_id, t4.unit_code, t4.unit_name
        from tbl_user_legalentity as t1 inner join tbl_legal_entities as t2 on
        t2.client_id = t1.client_id inner join tbl_client_compliances as t3 on
        t3.legal_entity_id = t2.legal_entity_id and t3.client_id = t2.client_id
        inner join tbl_units as t4 on t4.unit_id = t3.unit_id
        where t1.user_id = _user_id order by t4.unit_name asc;
    end if;
    if @u_cat_id = 7 or @u_cat_id = 8 THEN
        select t1.client_id, t2.legal_entity_id, t3.unit_id, t4.unit_code, t4.unit_name
        from tbl_user_units as t1 inner join tbl_legal_entities as t2 on
        t2.client_id = t1.client_id inner join tbl_client_compliances as t3 on
        t3.legal_entity_id = t2.legal_entity_id and t3.client_id = t2.client_id
        inner join tbl_units as t4 on t4.unit_id = t3.unit_id where
        t1.user_category_id = @u_cat_id and t1.user_id = _user_id order by t4.unit_name asc;
    end if;
END //

DELIMITER ;

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
        from tbl_client_groups as t1 inner join tbl_legal_entities as t2 on
        t2.client_id = t1.client_id inner join tbl_client_compliances as t3 on
        t3.legal_entity_id = t2.legal_entity_id and t3.client_id = t2.client_id
        inner join tbl_compliances as t4 on t4.compliance_id = t3.compliance_id
        inner join tbl_statutories as t5 on t5.statutory_id = t3.statutory_id;
    end if;
    if @u_cat_id = 5  THEN
        select t3.client_id, t3.legal_entity_id, t3.unit_id, t3.domain_id, t3.statutory_id,
        t4.compliance_id, t4.compliance_task, t4.document_name, t5.statutory_name
        from tbl_user_clients as t1 inner join tbl_legal_entities as t2 on
        t2.client_id  = t1.client_id inner join tbl_client_compliances as t3 on
        t3.legal_entity_id = t2.legal_entity_id and t3.client_id = t2.client_id
        inner join tbl_compliances as t4 on t4.compliance_id = t3.compliance_id
        inner join tbl_statutories as t5 on t5.statutory_id = t3.statutory_id
        where
        t1.user_category_id = @u_cat_id and t1.user_id = _user_id;
    END IF;
    if @u_cat_id = 6  THEN
        select t3.client_id, t3.legal_entity_id, t3.unit_id, t3.domain_id, t3.statutory_id,
        t4.compliance_id, t4.compliance_task, t4.document_name, t5.statutory_name
        from tbl_user_legalentity as t1 inner join tbl_legal_entities as t2 on
        t2.client_id = t1.client_id inner join tbl_client_compliances as t3 on
        t3.legal_entity_id = t2.legal_entity_id and t3.client_id = t2.client_id
        inner join tbl_compliances as t4 on t4.compliance_id = t3.compliance_id
        inner join tbl_statutories as t5 on t5.statutory_id = t3.statutory_id
        where t1.user_id = _user_id;
    end if;
    if @u_cat_id = 7 or @u_cat_id = 8 THEN
        select t3.client_id, t3.legal_entity_id, t3.unit_id, t3.domain_id, t3.statutory_id,
        t4.compliance_id, t4.compliance_task, t4.document_name, t5.statutory_name
        from tbl_user_units as t1 inner join tbl_legal_entities as t2 on
        t2.client_id = t1.client_id inner join tbl_client_compliances as t3 on
        t3.legal_entity_id = t2.legal_entity_id and t3.client_id = t2.client_id
        inner join tbl_compliances as t4 on t4.compliance_id = t3.compliance_id
        inner join tbl_statutories as t5 on t5.statutory_id = t3.statutory_id
        where t1.user_category_id = @u_cat_id and t1.user_id = _user_id;
    end if;
END //

DELIMITER ;

-- --------------------------------------------------------------------------------
-- Routine DDL
-- Note: comments before and after the routine body will not be stored by the server
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_statutory_setting_report_recordset`;

DELIMITER //


CREATE PROCEDURE `sp_statutory_setting_report_recordset`(
in _c_id int(11), _d_id varchar(11), _bg_id varchar(11), _le_id int(11), _u_id varchar(11),
_cl_id int(11), _st_id text, _cp_id text, _frm_cnt int(11), _pg_cnt int(11))
BEGIN

    select t1.unit_id, t1.unit_code, t1.unit_name, concat(t1.address,',',t1.postal_code) as address
    from
    tbl_client_compliances as t2 left join tbl_units as t1
    on t1.unit_id = t2.unit_id and t1.country_id = _c_id and
    coalesce(t1.business_group_id,'%') like _bg_id
    where
    -- coalesce(t2.compliance_id,'') like _cp_id and
    coalesce(t2.domain_id,'') like _d_id and
    t2.client_id = _cl_id and t2.legal_entity_id = _le_id and
    coalesce(t2.unit_id,'') like _u_id and
    t2.is_approved = 5 group by t1.unit_id;

    select t1.unit_id, t3.statutory_mapping_id, t3.statutory_mapping
    from
    tbl_client_compliances as t1 left join tbl_compliances as t2
    on t2.compliance_id = t1.compliance_id
    left join tbl_statutory_mappings as t3 on
    t3.statutory_mapping_id = t2.statutory_mapping_id
    where
    (coalesce(t3.statutory_mapping,'') like _st_id
    or t3.statutory_mapping like concat('%',_st_id, '%')) and
    (coalesce(t2.compliance_task,'') like _cp_id or
    t2.compliance_task like concat('%',_cp_id,'%')) and
    t2.country_id = _c_id and
    t1.is_approved = 5 and
    -- coalesce(t1.compliance_id,'') like _cp_id and
    coalesce(t1.domain_id,'') like _d_id and
    coalesce(t1.unit_id,'') like _u_id and
    t1.legal_entity_id = _le_id and t1.client_id = _cl_id
    group by t1.unit_id, t3.statutory_mapping_id;

    select t1.compliance_id, t1.client_compliance_id,
    t1.unit_id, t2.statutory_mapping_id, t2.statutory_provision, t2.compliance_task as c_task,
    t2.document_name, t1.remarks, t1.statutory_applicable_status as statutory_applicability_status,
    t1.compliance_opted_status as statutory_opted_status,
    (case when t1.updated_by is not null then (select email_id from tbl_users where
    user_id = t1.updated_by) else (select email_id from tbl_users where
    user_id = t1.submitted_by) end) as compfie_admin,
    (case when t1.updated_on is not null then DATE_FORMAT(t1.updated_on, '%d-%b-%Y')
    else DATE_FORMAT(t1.submitted_on, '%d-%b-%Y') end) as admin_update,
    (select email_id from tbl_client_users where user_id = t1.client_opted_by and
    client_id = _cl_id) as client_admin,
    DATE_FORMAT(t1.client_opted_on, '%d-%b-%Y') as client_update,
    (select tsn.statutory_nature_name from tbl_statutory_natures as tsn
    where tsn.statutory_nature_id = t3.statutory_nature_id) as statutory_nature_name
        from
    tbl_client_compliances as t1 left join tbl_compliances as t2 on
    t2.compliance_id = t1.compliance_id left join tbl_statutory_mappings as t3 on
    t3.statutory_mapping_id = t2.statutory_mapping_id
    where
    (coalesce(t3.statutory_mapping,'') like _st_id
    or t3.statutory_mapping like concat('%',_st_id, '%')) and
    (coalesce(t2.compliance_task,'') like _cp_id or
    t2.compliance_task like concat('%',_cp_id,'%')) and
    t2.country_id = _c_id and
    t1.is_approved = 5 and
    -- coalesce(t1.compliance_id,'') like _cp_id and
    coalesce(t1.domain_id,'') like _d_id and
    coalesce(t1.unit_id,'') like _u_id and
    t1.legal_entity_id = _le_id and t1.client_id = _cl_id
    group by t1.client_compliance_id limit _frm_cnt, _pg_cnt;

    select t1.unit_id, t1.statutory_id, t2.statutory_provision, t2.compliance_task as c_task,
    t2.document_name, t1.remarks, t1.statutory_applicable_status as statutory_applicability_status,
    t1.statutory_opted_status, 'user@compfie.com'  as compfie_admin,
    DATE_FORMAT(t1.updated_on, '%d-%b-%Y') as admin_update,
    (select email_id from tbl_users where user_id = t1.client_opted_by) as client_admin,
    DATE_FORMAT(t1.client_opted_on, '%d-%b-%Y') as client_update,
    (select tsn.statutory_nature_name from tbl_statutory_natures as tsn
    where tsn.statutory_nature_id = t3.statutory_nature_id) as statutory_nature_name
    from
    tbl_client_compliances as t1 left join tbl_compliances as t2 on
    t2.compliance_id = t1.compliance_id left join tbl_statutory_mappings as t3 on
    t3.statutory_mapping_id = t2.statutory_mapping_id
    where
    (coalesce(t3.statutory_mapping,'') like _st_id
    or t3.statutory_mapping like concat('%',_st_id, '%')) and
    (coalesce(t2.compliance_task,'') like _cp_id or
    t2.compliance_task like concat('%',_cp_id,'%')) and
    t2.country_id = _c_id and
    t1.is_approved = 5 and
    -- coalesce(t1.compliance_id,'') like _cp_id and
    coalesce(t1.domain_id,'') like _d_id and
    coalesce(t1.unit_id,'') like _u_id and
    t1.legal_entity_id = _le_id and t1.client_id = _cl_id
    group by t1.client_compliance_id;
END //

DELIMITER ;

-- --------------------------------------------------------------------------------
-- Group list with legal entity count for group admin registration email
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_groupadmin_registration_email_groupslist`;

DELIMITER //


CREATE PROCEDURE `sp_groupadmin_registration_email_groupslist`(
in _user_id int(11))
BEGIN
    select t3.client_id, t3.group_name, count(t2.legal_entity_id ) as
        no_of_legal_entities, t3.group_admin_username as ug_name,
        (select distinct email_id from tbl_client_groups where client_id = t3.client_id) as email_id,
        (select distinct user_id from tbl_client_users where client_id = t3.client_id and user_category_id = 1) as user_id,
        (select concat(employee_name,'-',(case when employee_code is null then
            '' else employee_code end)) from tbl_client_users where client_id = t3.client_id and user_category_id = 1) as emp_code_name,
        (select date_format(registration_sent_on, '%d-%b-%y') from tbl_group_admin_email_notification where
        client_id = t3.client_id and client_informed_id = (select max(client_informed_id)
        from tbl_group_admin_email_notification where client_id=t3.client_id)) as registration_email_date,
        (select date_format(registration_resend_on, '%d-%b-%y') from tbl_group_admin_email_notification where
        client_id = t3.client_id and client_informed_id = (select max(client_informed_id)
        from tbl_group_admin_email_notification where client_id=t3.client_id)) as resend_email_date,
        if ((select count(client_id) from tbl_group_admin_email_notification where client_id = t3.client_id ) = 0 ,
        (select max(is_new_data) from tbl_client_replication_status where is_group = 1 and client_id = t3.client_id), 0)as replication_status

        from
        tbl_user_clients as t1, tbl_legal_entities as t2, tbl_client_groups as t3
        where

        t3.client_id = t2.client_id and t2.client_id = t1.client_id and
        t2.is_created = 1
        group by t2.client_id order by t3.group_name;

        select t2.client_id, t3.country_id, t3.country_name
        from tbl_user_clients as t1, tbl_legal_entities as t2, tbl_countries as t3
        where t3.country_id = t2.country_id and t2.client_id = t1.client_id and
        t2.is_created = 1;
END //

DELIMITER ;

-- --------------------------------------------------------------------------------
-- Routine DDL
-- Note: comments before and after the routine body will not be stored by the server
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_groupadmin_registration_email_unitslist`;

DELIMITER //

CREATE PROCEDURE `sp_groupadmin_registration_email_unitslist`(
in _user_id int(11))
BEGIN
SELECT @u_cat_id := user_category_id from tbl_user_login_details where user_id = _user_id;

    if @u_cat_id = 1 then

        select t3.client_id, t2.legal_entity_id, t2.legal_entity_name,
        (select COUNT(unit_id) as a from tbl_units where client_id = t1.client_id and
        legal_entity_id = t2.legal_entity_id and country_id = t2.country_id and is_approved = 1) as unit_count,
        (select country_name from tbl_countries where country_id = t2.country_id) as
            country_name,
        (select count(*) from tbl_group_admin_email_notification where client_id =
            t2.client_id and legal_entity_id = t2.legal_entity_id and unit_sent_on is not null
            and unit_creation_informed=1)
        as unit_creation_informed,
        (select count(*) from tbl_group_admin_email_notification where client_id =
            t2.client_id and legal_entity_id = t2.legal_entity_id and statu_sent_on is not null
            and assign_statutory_informed=1)
        as statutory_assigned_informed,
        (select distinct email_id from tbl_client_groups where client_id = t1.client_id) as email_id,
        (select distinct user_id from tbl_client_users where client_id = t1.client_id  and user_category_id = 1) as user_id,
        'Group Admin' as emp_code_name,
        (select count(*) from tbl_client_statutories where client_id = t1.client_id and
            unit_id in (select unit_id from tbl_units where client_id = t1.client_id and
            legal_entity_id = t2.legal_entity_id and country_id = t2.country_id) and status = 3) as statutory_count
        from
        tbl_user_clients as t1, tbl_legal_entities as t2, tbl_client_groups as t3
        -- tbl_units as t4
        where
        t3.client_id = t2.client_id and
        t2.is_created = 1 and
        t2.client_id = t1.client_id order by t2.legal_entity_name;

    end if;

END //

DELIMITER ;

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

END //

DELIMITER ;

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

END //

DELIMITER ;

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
        as is_active, date_format(t3.closed_on, '%d-%b-%Y') as closed_on,
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

        select t3.unit_id, t4.domain_id, t4.organisation_id
        from
        tbl_user_clients as t1,
        tbl_units as t3, tbl_units_organizations as  t4
        where
        t4.unit_id =t3.unit_id and
        t3.client_id = t1.client_id;
        -- and t1.user_id = _u_id;
        -- group by t3.unit_id;
    end if;
    if @u_cat_id = 5  THEN
        select t3.country_id, t3.client_id, t3.legal_entity_id, t3.business_group_id,
        t3.unit_id, t3.unit_code, t3.unit_name, t3.address, t3.postal_code, t3.is_closed
        as is_active, date_format(t3.closed_on, '%d-%b-%Y') as closed_on,
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
        group by t3.unit_id
        order by t3.unit_name asc;

        select t3.unit_id, t4.domain_id, t4.organisation_id
        from
        tbl_user_clients as t1,
        tbl_units as t3, tbl_units_organizations as  t4
        where
        t4.unit_id =t3.unit_id and
        t3.client_id = t1.client_id
        and t1.user_id = _u_id;
        -- group by t3.unit_id;
    END IF;
    if @u_cat_id = 6  THEN
        select t3.country_id, t3.client_id, t3.legal_entity_id, t3.business_group_id,
        t3.unit_id, t3.unit_code, t3.unit_name, t3.address, t3.postal_code, t3.is_closed
        as is_active, date_format(t3.closed_on, '%d-%b-%Y') as closed_on,
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
        group by t3.unit_id
        order by t3.unit_name asc;

        select t3.unit_id, t4.domain_id, t4.organisation_id
        from
        tbl_user_legalentity as t1,
        tbl_units as t3, tbl_units_organizations as  t4
        where
        t4.unit_id =t3.unit_id and
        t3.legal_entity_id = t1.legal_entity_id
        and t1.user_id = _u_id;
        -- group by t3.unit_id;
    end if;
    if @u_cat_id = 7 or @u_cat_id = 8 THEN
        select t3.country_id, t3.client_id, t3.legal_entity_id, t3.business_group_id,
        t3.unit_id, t3.unit_code, t3.unit_name, t3.address, t3.postal_code, t3.is_closed
        as is_active, date_format(t3.closed_on, '%d-%b-%Y') as closed_on,
        date_format(t3.created_on, '%d-%b-%Y') as check_date,
        (select concat(employee_code,'-',employee_name) from tbl_users
        where user_id = t3.created_by)as emp_code_name,
        date_format(t3.created_on, '%d/%m/%Y') as created_on,
        (select division_name from tbl_divisions where
        division_id = t3.division_id) as division_name,
        (select category_name from tbl_categories where
        category_id = t3.category_id) as category_name
        from tbl_user_units as t1,tbl_units as t3 where
        t3.unit_id = t1.unit_id
        and user_id = _u_id and user_category_id = @u_cat_id
        group by t3.unit_id
        order by t3.unit_name asc;

        select t3.unit_id, t4.domain_id, t4.organisation_id
        from
        tbl_user_units as t1,
        tbl_units as t3, tbl_units_organizations as  t4
        where
        t4.unit_id =t3.unit_id and
        t3.unit_id = t1.unit_id
        and t1.user_id = _u_id and t1.user_category_id = @u_cat_id;
        -- group by t3.unit_id;

    end if;

END //

DELIMITER ;

-- --------------------------------------------------------------------------------
-- To get data for group admin registration report
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_group_admin_registration_email_report_data`;

DELIMITER //


CREATE PROCEDURE `sp_group_admin_registration_email_report_data`(
in _u_id int(11))
BEGIN
    SELECT @u_cat_id := user_category_id from tbl_user_login_details where user_id = _u_id;
    if @u_cat_id = 1 then
        select t2.client_id, t2.group_name, t2.is_active
        from
        tbl_user_clients as t1, tbl_client_groups as t2
        where
        t2.client_id = t1.client_id
        order by t2.group_name;

        select t1.client_id, t3.country_id, t3.country_name, t3.is_active
        from
        tbl_user_clients as t1, tbl_legal_entities as t2, tbl_countries as t3
        where
        t3.country_id = t2.country_id and
        t2.client_id = t1.client_id
        order by t3.country_name;

        select t2.client_id, t2.legal_entity_id, t2.legal_entity_name, count(t4.unit_id ) as
        unit_count, t2.country_id, (select country_name from tbl_countries where country_id =
        t2.country_id) as country_name, (select date_format(unit_sent_on, '%d-%b-%y %h:%i')
        from tbl_group_admin_email_notification where client_informed_id = (select max(client_informed_id)
        from tbl_group_admin_email_notification where client_id = t1.client_id and
        legal_entity_id = t2.legal_entity_id and unit_creation_informed=1)) as unit_email_date,
        (select date_format(statu_sent_on, '%d-%b-%y %h:%i') from tbl_group_admin_email_notification
        where client_informed_id = (select max(client_informed_id)
        from tbl_group_admin_email_notification where client_id = t1.client_id and
        legal_entity_id = t2.legal_entity_id and assign_statutory_informed=1)) as statutory_email_date,
        (select date_format(registration_sent_on, '%d-%b-%Y %h:%i %p') from tbl_group_admin_email_notification
        where client_informed_id = (select max(client_informed_id)
        from tbl_group_admin_email_notification where client_id = t1.client_id and
        registration_sent_by is not null)) as registration_email_date,
        (select date_format(registration_resend_on, '%d-%b-%y %h:%i') from tbl_group_admin_email_notification
        where client_informed_id = (select max(client_informed_id)
        from tbl_group_admin_email_notification where client_id = t1.client_id and
        registration_resend_by is not null)) as resend_email_date
        from
        tbl_user_clients as t1 inner join tbl_legal_entities as t2 on
        t2.client_id = t1.client_id left join tbl_units as t4 on
        t4.legal_entity_id = t2.legal_entity_id and
        t4.client_id = t2.client_id
        group by t1.client_id, t2.legal_entity_id
        order by t2.client_id,t2.legal_entity_name;
    end if;

END //

DELIMITER ;

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

    select user_category_id, user_id, concat(employee_code,' - ',employee_name) as
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

    select client_id, group_name as short_name, is_active
    from tbl_client_groups;

    select t1.user_id, t1.client_id, t1.legal_entity_id, t1.domain_id,
    t2.legal_entity_name, t2.business_group_id,
    (select business_group_name from tbl_business_groups
    where business_group_id = t2.business_group_id) as business_group_name,
    (select domain_name from tbl_domains where
    domain_id = t1.domain_id) as domain_name
    from
    tbl_legal_entities as t2 inner join tbl_user_units as t1
    on t2.client_id  = t1.client_id and
    t2.legal_entity_id = t1.legal_entity_id
    where
    t1.user_id in (select user_id from tbl_users)
    group by t1.user_id,t1.client_id,t1.legal_entity_id, t1.domain_id;

END //

DELIMITER ;

-- --------------------------------------------------------------------------------
-- To get reassign user report data
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_reassign_user_report_getdata`;

DELIMITER //


CREATE PROCEDURE `sp_reassign_user_report_getdata`(
in _u_id int(11), _u_cg_id int(11), _g_id varchar(50))
BEGIN
    if _u_cg_id = 5 then
        select t1.client_id, t2.group_name,
        date_format(t3.assigned_on, '%d-%b-%y') as assigned_on,
         (case when ((select user_category_id from tbl_user_login_details
                    where user_id = _u_id) = 1) then
            'Compfie Admin'
        else
            (select concat(employee_code,'-',employee_name)
                from tbl_users where user_id = reassigned_to) end) as emp_code_name,
        t3.remarks, (select count(*) from tbl_legal_entities where
        client_id = t1.client_id) as le_count, (select concat(employee_code,'-',
        employee_name) from tbl_users where user_id = reassigned_to) as
        reassigned_to, (select legal_entity_name from tbl_legal_entities where
        client_id =  t1.client_id limit 1) as legal_entity_name
        from
        tbl_user_clients as t1,
        tbl_client_groups as t2,
        tbl_user_account_reassign_history as t3

        where
        (t3.reassigned_to = _u_id or t3.reassigned_from = _u_id) and
        t3.reassigned_data = t1.client_id and
        t2.client_id = t1.client_id and
        COALESCE(t1.client_id,'') LIKE _g_id and
        t1.user_id = _u_id order by t3.assigned_on desc;

        select t2.client_id, t3.country_id, t3.country_name
        from tbl_user_clients as t1, tbl_legal_entities as t2, tbl_countries as t3
        where t3.country_id = t2.country_id and t2.client_id = t1.client_id and
        t1.user_id = _u_id order by t3.country_name;
    end if;
    if _u_cg_id =  6 then
        select t1.client_id, t2.group_name,
        date_format(t3.assigned_on, '%d-%b-%y') as assigned_on,
        (case when ((select user_category_id from tbl_user_login_details
                    where user_id = _u_id) = 1) then
            'Compfie Admin'
        else
            (select concat(employee_code,'-',employee_name)
                from tbl_users where user_id = reassigned_to) end) as emp_code_name,
        t3.remarks, (select count(*) from tbl_legal_entities where
        client_id = t1.client_id) as le_count, (select concat(employee_code,'-',
        employee_name) from tbl_users where user_id = reassigned_to) as
        reassigned_to, (select legal_entity_name from tbl_legal_entities
        where legal_entity_id = t1.legal_entity_id and t1.user_id=_u_id) as
        legal_entity_name
        from
        tbl_user_legalentity as t1,
        tbl_client_groups as t2,
        tbl_user_account_reassign_history as t3

        where
        (t3.reassigned_to = _u_id or t3.reassigned_from = _u_id) and
        t3.reassigned_data in (t1.legal_entity_id) and
        t2.client_id = t1.client_id and
        COALESCE(t1.client_id,'') LIKE _g_id and
        t1.user_id = _u_id order by t3.assigned_on desc;

        select t2.client_id, t3.country_id, t3.country_name
        from tbl_user_legalentity as t1, tbl_legal_entities as t2, tbl_countries as t3
        where t3.country_id = t2.country_id and t2.client_id = t1.client_id and
        COALESCE(t1.client_id,'') LIKE _g_id and t1.user_id = _u_id
        order by t3.country_name;
    end if;

END //

DELIMITER ;

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
    (select group_name from tbl_client_groups where client_id = t1.client_id) as
    group_name,
    (select business_group_name from tbl_business_groups where business_group_id =
    t2.business_group_id) as business_group_name,
    t2.legal_entity_name, (select country_name from tbl_countries where country_id =
    t2.country_id) as country_name
    from
    tbl_user_clients as t1, tbl_legal_entities as t2
    where
    t2.client_id  = t1.client_id and t1.user_id = _u_id
    order by group_name;
END //

DELIMITER ;

-- --------------------------------------------------------------------------------
-- To update closed details in legal entity table
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_legalentity_closure_save`;

DELIMITER //


CREATE PROCEDURE `sp_legalentity_closure_save`(
in _u_id int(11), _le_id int(11), _is_cl tinyint(1), _cl_on timestamp, _rem varchar(500))
BEGIN
    if _is_cl = 1 then
        if((select (case when closed_on is not null then
        DATEDIFF(NOW(), closed_on) else 0 end) from tbl_legal_entities
        where legal_entity_id = _le_id) < 90)then

            update tbl_legal_entities
            set is_closed = _is_cl, closed_on = _cl_on, closed_by = _u_id,
            closed_remarks = _rem where
            legal_entity_id = _le_id;
        end if;
    else
        update tbl_legal_entities
        set is_closed = _is_cl, closed_on = _cl_on, closed_by = _u_id,
        closed_remarks = _rem where
        legal_entity_id = _le_id;
    end if;
    select @clientName := group_name from tbl_client_groups where
    client_id = (select client_id from tbl_legal_entities where
    legal_entity_id = _le_id);

    if _is_cl = 0 then
        INSERT INTO tbl_messages
        SET
        user_category_id = 6,
        message_heading = 'Legal Entity Closure',
        message_text = (select concat(@clientName,' & ',legal_entity_name,' ','has been activated')
        from tbl_legal_entities where legal_entity_id = _le_id),
        link = null, created_by = _u_id, created_on = _cl_on;
        set @msg_id := LAST_INSERT_ID();
        IF(select count(*) from tbl_user_legalentity where legal_entity_id = _le_id) > 0 THEN
            INSERT INTO tbl_message_users
            SET
            message_id = @msg_id,
            user_id = (select user_id from tbl_user_legalentity where legal_entity_id = _le_id);
        END IF;
        INSERT INTO tbl_messages
        SET
        user_category_id = 1,
        message_heading = 'Legal Entity Closure',
        message_text = (select concat(@clientName,' & ',legal_entity_name,' ','has been closed')
        from tbl_legal_entities where legal_entity_id = _le_id),
        link = null, created_by = _u_id, created_on = _cl_on;

        INSERT INTO tbl_message_users (message_id, user_id)
        select LAST_INSERT_ID(), user_id
             from tbl_user_login_details where user_id =
         (select user_id from tbl_user_login_details where user_category_id = 1 limit 1);
    else
        INSERT INTO tbl_messages
        SET
        user_category_id = 6,
        message_heading = 'Legal Entity Closure',
        message_text = (select concat(@clientName,' & ',legal_entity_name,' ','has been closed')
        from tbl_legal_entities where legal_entity_id = _le_id),
        link = null, created_by = _u_id, created_on = _cl_on;
        set @msg_id := LAST_INSERT_ID();
        IF(select count(*) from tbl_user_legalentity where legal_entity_id = _le_id) > 0 THEN
            INSERT INTO tbl_message_users
            SET
            message_id = @msg_id,
            user_id = (select user_id from tbl_user_legalentity where legal_entity_id = _le_id);
        END IF;
        INSERT INTO tbl_messages
        SET
        user_category_id = 1,
        message_heading = 'Legal Entity Closure',
        message_text = (select concat(@clientName,' & ',legal_entity_name,' ','has been closed')
        from tbl_legal_entities where legal_entity_id = _le_id),
        link = null, created_by = _u_id, created_on = _cl_on;

        INSERT INTO tbl_message_users (message_id, user_id)
        select LAST_INSERT_ID(), user_id
             from tbl_user_login_details where user_id =
         (select user_id from tbl_user_login_details where user_category_id = 1 limit 1);
    end if;

END //

DELIMITER ;

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

END //

DELIMITER ;

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
END //

DELIMITER ;

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

END //

DELIMITER ;

-- --------------------------------------------------------------------------------
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

END //

DELIMITER ;

-- --------------------------------------------------------------------------------
-- get knowledge users message list
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_get_messages`;

DELIMITER //


CREATE PROCEDURE `sp_get_messages`(
IN fromcount_ INT(11), IN pagecount_ INT(11), IN userid_ INT(11)
)
BEGIN

    SELECT @u_cat_id := user_category_id from tbl_user_login_details where user_id = userid_;

    SELECT m.message_id, m.message_heading, m.message_text, m.link, m.created_by,
    IF(uld.user_category_id <= 2, 'Compfie Admin',
    (SELECT concat(employee_code, ' - ', employee_name)
    from tbl_users where user_id = m.created_by)) as created_by,
    m.created_on
    from tbl_messages m
    INNER JOIN tbl_message_users mu ON mu.message_id = m.message_id
    INNER JOIN tbl_user_login_details uld ON uld.user_id = m.created_by
    where m.user_category_id = @u_cat_id and mu.user_id = userid_ and mu.read_status = 0
    order by created_on DESC limit pagecount_;

END //

DELIMITER ;

-- --------------------------------------------------------------------------------
-- update knowledge users message list read status
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_message_read_status`;

DELIMITER //

CREATE PROCEDURE `sp_message_read_status`(
    IN messageid_ INT(11), userid_ INT(11), readstatus_ TINYINT(2)
)
BEGIN
    UPDATE tbl_message_users set read_status = readstatus_
    WHERE message_id=messageid_ AND user_id = userid_;

END //

DELIMITER ;

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
    AND su.user_id = userid_ AND su.read_status = 0
    order by su.read_status DESC, s.created_on DESC limit pagecount_;

END //

DELIMITER ;

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

END //

DELIMITER ;

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

END //

DELIMITER ;

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

    SELECT form_id, form_name FROM tbl_forms;

    SELECT distinct(t1.user_id), t1.user_category_id,
    (select employee_name from tbl_users where user_id = t1.user_id) as employee_name,
    (select employee_code from tbl_users where user_id = t1.user_id) as employee_code,
    (select is_active from tbl_users where user_id = t1.user_id) as is_active
    FROM tbl_activity_log as t1;

    SELECT user_id, user_category_id, form_id, action, created_on FROM tbl_activity_log;
END//

DELIMITER ;

DROP PROCEDURE IF EXISTS `sp_tbl_geography_levels_getlist`;

DELIMITER //


CREATE PROCEDURE `sp_tbl_geography_levels_getlist`()
BEGIN
    select level_id, level_position, level_name, country_id from
    tbl_geography_levels order by level_position;

END //

DELIMITER ;
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

END //

DELIMITER ;
-- --------------------------------------------------------------------------------
-- Check levels in geography master
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_check_level_in_geographies`;

DELIMITER //


CREATE PROCEDURE `sp_check_level_in_geographies`(
    in levelId int(11))
BEGIN
    select count(*) as cnt from tbl_geographies where
    level_id = levelId;

END //

DELIMITER ;
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
END //

DELIMITER ;
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

DELIMITER ;
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
END //

DELIMITER ;


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
        (select repeat_type from tbl_compliance_repeat_type where repeat_type_id = t2.repeats_type_id) as repeat_type,
        (select duration_type from tbl_compliance_duration_type where duration_type_id = t2.duration_type_id) as duration_type,
        (select concat(employee_code, ' - ', employee_name) from tbl_users where user_id = t2.created_by) as created_by,
        (select concat(employee_code, ' - ', employee_name) from tbl_users where user_id = t2.updated_by) as updated_by,
        (select country_name from tbl_countries where country_id = t2.country_id) as country_name,
        (select domain_name from tbl_domains where domain_id = t2.domain_id) as domain_name
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
    IN userid INT(11), org_id INT(11), nature_id INT(11),
    countryid INT(11), domainid INT(11), knowledge_user_id INT(11),
    from_count INT(11), to_count INT(11)
)
BEGIN
    select * from (
    select @rownum := @rownum + 1 AS num, t.* from (
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
     and IF(nature_id IS NOT NULL,t1.statutory_nature_id = nature_id, 1)
     and IF(knowledge_user_id IS NOT NULL, IFNULL(t2.updated_by, t2.created_by) = knowledge_user_id, 1)
     and IFNULL(t2.updated_by, t2.created_by) in (
        select child_user_id from tbl_user_mapping where parent_user_id = userid and
        country_id = t1.country_id and domain_id = t1.domain_id
     ) order by t1.statutory_mapping_id) t,
     (SELECT @rownum := 0) r) as t01
      where t01.num between from_count and to_count;

    select distinct t.organisation_name, t1.statutory_mapping_id from tbl_organisation as t
    inner join tbl_mapped_industries as t1 on t1.organisation_id = t.organisation_id
    inner join tbl_compliances as t2 on t1.statutory_mapping_id = t2.statutory_mapping_id
    inner join tbl_user_domains as t3 on t3.country_id = t2.country_id and t3.domain_id = t2.domain_id
    where t2.is_approved = 1 and t3.user_id = userid
    and t2.country_id = countryid
    and t2.domain_id = domainid
    and IF(knowledge_user_id IS NOT NULL, IFNULL(t2.updated_by, t2.created_by) = knowledge_user_id, 1)
    and IF(org_id IS NOT NULL, t1.organisation_id = org_id, 1)
    and IFNULL(t2.updated_by, t2.created_by) in (
        select child_user_id from tbl_user_mapping where parent_user_id = userid
    ) order by t1.statutory_mapping_id ;

    select count(t1.statutory_mapping_id) as mapping_count
    from tbl_statutory_mappings as t1
    inner join tbl_compliances as t2 on t1.statutory_mapping_id = t2.statutory_mapping_id
    inner join tbl_statutory_natures as t4 on t1.statutory_nature_id = t4.statutory_nature_id
    inner join tbl_user_domains as t5 on t5.country_id = t2.country_id and t5.domain_id = t2.domain_id
    where t2.is_approved = 1 and t5.user_id = userid
    and t2.country_id = countryid
    and t2.domain_id = domainid
    and IF(knowledge_user_id IS NOT NULL, IFNULL(t2.updated_by, t2.created_by) = knowledge_user_id, 1)
    and IF(nature_id IS NOT NULL,t1.statutory_nature_id = nature_id, 1)
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
        (select repeat_type from tbl_compliance_repeat_type where repeat_type_id = t1.repeats_type_id) as repeat_type,
        (select duration_type from tbl_compliance_duration_type where duration_type_id = t1.duration_type_id) as duration_type
    FROM tbl_compliances as t1 inner join tbl_statutory_mappings as t2
    on t1.statutory_mapping_id = t2.statutory_mapping_id
    where t1.compliance_id = compid;

    SELECT distinct t1.geography_name, t1.parent_names from tbl_geographies as t1
    inner join tbl_mapped_locations as t2 on t2.geography_id = t1.geography_id
    inner join tbl_compliances as t3 on t3.statutory_mapping_id = t2.statutory_mapping_id
    where t3.compliance_id = compid;
END //

DELIMITER ;


DROP PROCEDURE IF EXISTS `sp_tbl_users_to_notify`;

DELIMITER //

CREATE PROCEDURE `sp_tbl_users_to_notify`(
    IN compid INT(11)
)
BEGIN

    select t1.user_id from tbl_user_login_details as t1
        left join tbl_user_domains as t2 on t1.user_id = t2.user_id
        inner join tbl_compliances as t3 on t2.domain_id = t3.domain_id and t2.country_id = t3.country_id
        and t3.compliance_id = compid
        where
        t1.is_active = 1 ;

    select user_id from tbl_user_login_details where user_category_id = 1 and is_active = 1;

END //

DELIMITER ;


DROP PROCEDURE IF EXISTS `sp_user_knowledge_executives`;

DELIMITER //

CREATE PROCEDURE `sp_user_knowledge_executives`(
    IN userid INT(11)
)
BEGIN
    select distinct child_user_id, concat(employee_code, '-', employee_name) as emp_name from  tbl_user_mapping
    inner join tbl_users on user_id = child_user_id and is_active = 1 and is_disable = 0
    where parent_user_id = userid ;


END //

DELIMITER ;

-- --------------------------------------------------------------------------------
-- Get domain user report data for reassign user report
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_reassign_user_report_domain_user_getdata`;

DELIMITER //

CREATE PROCEDURE `sp_reassign_user_report_domain_user_getdata`(
    IN _u_id int(11), _u_cg_id int(11), _g_id int(11), _bg_id varchar(50),
    _le_id int(11), _d_id int(11)
)
BEGIN
    if _u_cg_id = 7 or _u_cg_id = 8 then
        select t2.unit_id, t2.unit_code, t2.unit_name, t2.address, t2.postal_code,
        (Select geography_name from tbl_geographies where geography_id = t2.geography_id)
        as geography_name,
        date_format(t4.assigned_on, '%d-%b-%y') as unit_email_date,
        concat(t5.employee_code,'-',t5.employee_name) as emp_code_name,
        t4.remarks, (select group_name from tbl_client_groups where
        client_id=t1.client_id) as group_name,
        (select legal_entity_name from tbl_legal_entities where
        legal_entity_id=t1.legal_entity_id) as legal_entity_name,
        (select country_name from tbl_countries where country_id=
        t2.country_id)as country_name,(select group_concat(domain_name)
        from tbl_domains where domain_id = t3.domain_id)as domain_name,
        (select concat(employee_code,'-',employee_name) from tbl_users where
        user_id = _u_id)as domain_usr
        from
        tbl_user_units as t1,
        tbl_units as t2, tbl_units_organizations as t3,
        tbl_user_account_reassign_history as t4,
        tbl_users as t5
        where
        t5.user_id = t4.reassigned_to and
        (t4.reassigned_to = _u_id  or t4.reassigned_from = _u_id) and
        t4.reassigned_data = t1.unit_id and
        t3.domain_id = t1.domain_id and t3.unit_id = t2.unit_id and
        COALESCE(t2.business_group_id,'') LIKE _bg_id and
        t2.unit_id = t1.unit_id and
        t1.domain_id = _d_id and
        t1.legal_entity_id = _le_id and
        t1.client_id = _g_id and
        t1.user_id = _u_id and
        t1.user_category_id = _u_cg_id
        group by t4.user_account_id;

    end if;

END //

DELIMITER ;


DROP PROCEDURE IF EXISTS `sp_tbl_statutory_mapping_by_id`;

DELIMITER //

CREATE PROCEDURE `sp_tbl_statutory_mapping_by_id`(
    IN map_id INT(11), comp_id VARCHAR(50), fromcount int(11), tocount int(11)
)
BEGIN
    select t1.statutory_mapping_id, t2.compliance_id, t2.country_id, t2.domain_id, t2.document_name,
        t2.compliance_task, t2.is_active,
        t1.statutory_nature_id,
        t2.statutory_provision,
        t2.compliance_description, t2.penal_consequences, t2.reference_link, t2.frequency_id,
        t2.statutory_dates, t2.repeats_type_id, t2.repeats_every, t2.duration_type_id,
        t2.duration,t2.format_file, t2.format_file_size,
        (select frequency from tbl_compliance_frequency where frequency_id = t2.frequency_id) as freq_name,
        (select repeat_type from tbl_compliance_repeat_type where repeat_type_id = t2.repeats_type_id) as repeat_type,
        (select duration_type from tbl_compliance_duration_type where duration_type_id = t2.duration_type_id) as duration_type
     from tbl_statutory_mappings as t1
         inner join tbl_compliances as t2 on t1.statutory_mapping_id = t2.statutory_mapping_id
         inner join tbl_statutory_natures as t4 on t1.statutory_nature_id = t4.statutory_nature_id
     where t1.statutory_mapping_id = map_id and t2.compliance_id like comp_id
     limit fromcount, tocount;

     select distinct t1.organisation_id, t.organisation_name, t1.statutory_mapping_id from tbl_organisation as t
         inner join tbl_mapped_industries as t1 on t1.organisation_id = t.organisation_id
     where t1.statutory_mapping_id = map_id;

     SELECT distinct t2.geography_id, t1.geography_name, t1.level_id, t1.parent_names, t1.parent_names, t2.statutory_mapping_id from tbl_geographies as t1
        inner join tbl_mapped_locations as t2 on t2.geography_id = t1.geography_id
     where t2.statutory_mapping_id = map_id;

    SELECT distinct t1.parent_names, t1.statutory_name, t2.statutory_id
        from tbl_statutories as t1
        inner join tbl_mapped_statutories as t2 on t2.statutory_id = t1.statutory_id
    where t2.statutory_mapping_id = map_id;

    SELECT count(compliance_id) as is_assigned FROM tbl_client_compliances WHERE compliance_id = comp_id;

END //

DELIMITER ;


DROP PROCEDURE IF EXISTS `sp_tbl_unit_getunitdetailsforuser_edit`;

DELIMITER //

CREATE  PROCEDURE `sp_tbl_unit_getunitdetailsforuser_edit`(in clientid int(11),
in businessgroupid varchar(11),
in legalentityid int(11),
in countryid int(11),
in userId INT(11),
in start_cnt int(11),
in to_cnt int(11))
BEGIN
    if start_cnt = 0 and to_cnt = 0 then
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
        t9.group_name,
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
        t4.is_approved = 1 and
        t4.legal_entity_id = t2.legal_entity_id and
        t2.legal_entity_id = t1.legal_entity_id and
        t2.client_id = t1.client_id and
        t1.user_id = userId and
        t2.country_id = countryid and
        t2.legal_entity_id = legalentityid and
        t2.client_id = clientid and
        COALESCE(t2.business_group_id,'') like businessgroupid
        order by t2.unit_code asc;
    else
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
        t9.group_name,
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
        t4.is_approved = 1 and
        t4.legal_entity_id = t2.legal_entity_id and
        t2.legal_entity_id = t1.legal_entity_id and
        t2.client_id = t1.client_id and
        t1.user_id = userId and
        t2.country_id = countryid and
        t2.legal_entity_id = legalentityid and
        t2.client_id = clientid and
        COALESCE(t2.business_group_id,'') like businessgroupid
        order by t2.unit_code asc limit start_cnt, to_cnt;
    end if;

    select t3.unit_id, t3.domain_id, t3.organisation_id,
    (select count(*) from tbl_user_units where unit_id=t2.unit_id and
    domain_id = t3.domain_id) as assigned_count
    from
    tbl_user_legalentity as t1,
    tbl_units as t2,
    tbl_units_organizations as t3
    where
    t3.unit_id = t2.unit_id and
    t2.legal_entity_id = t1.legal_entity_id and
    t2.client_id = t1.client_id and
    t1.user_id =userId and
    t2.country_id = countryid and
    t1.legal_entity_id = legalentityid;
END //

DELIMITER ;


DROP PROCEDURE IF EXISTS `sp_save_geography_master`;

DELIMITER //

CREATE PROCEDURE `sp_save_geography_master`(
in _g_name varchar(50), _l_id int(11), _p_ids text, _p_names text,
_created_by int(11), _created_on timestamp)
BEGIN
    insert into tbl_geographies
    (geography_name, level_id, parent_ids, parent_names, created_by, created_on)
    values
    (_g_name, _l_id, _p_ids, _p_names, _created_by, _created_on);
END //

DELIMITER ;

DROP PROCEDURE IF EXISTS `sp_update_geography_master`;

DELIMITER //

CREATE  PROCEDURE `sp_update_geography_master`(
in _g_id int(11), _g_name varchar(50), _p_ids text, _p_names text, _updated_by int(11))
BEGIN
    update tbl_geographies
    set geography_name = _g_name,
    parent_ids = _p_ids,
    parent_names = _p_names,
    updated_by = _updated_by
    where
    geography_id = _g_id;
END //

DELIMITER ;


DROP PROCEDURE IF EXISTS `sp_get_geography_master`;

DELIMITER //

CREATE PROCEDURE `sp_get_geography_master`(
in _g_id int(11), _p_ids text)
BEGIN
    SELECT t1.geography_id, t1.geography_name, t1.parent_ids, t1.level_id,
        (select group_concat(geography_name separator ' >> ')
        from tbl_geographies where find_in_set(geography_id, t1.parent_ids) ) as  parent_names
    from tbl_geographies as t1 WHERE
    find_in_set(_g_id, t1.parent_ids);

END //

DELIMITER ;

DROP PROCEDURE IF EXISTS `sp_update_geographies_master_level`;

DELIMITER //

CREATE PROCEDURE `sp_update_geographies_master_level`(
in _g_id int(11), _l_id int(11), map_name text)
BEGIN
    UPDATE tbl_geographies as A inner join
    (select c.country_name, g.level_id from
    tbl_countries c inner join tbl_geography_levels g on
    c.country_id = g.country_id) as C ON A.level_id  = C.level_id
    set A.parent_names = concat(C.country_name, '>>', map_name)
    where A.geography_id = _g_id AND C.level_id = _l_id;
END //

DELIMITER ;


DROP PROCEDURE IF EXISTS `sp_check_geography_exists`;

DELIMITER //

CREATE PROCEDURE `sp_check_geography_exists`(
in _g_id int(11))
BEGIN
    select count(1) as stat_cnt from tbl_statutory_geographies where geography_id = _g_id;

    select count(0) as geo_cnt from tbl_geographies where FIND_IN_SET(_g_id, parent_ids);
END //

DELIMITER ;

DROP PROCEDURE IF EXISTS `sp_geography_update_status`;

DELIMITER //

CREATE PROCEDURE `sp_geography_update_status`(
in _g_id int(11), _status tinyint(4), _updated_by int(11))
BEGIN
    update tbl_geographies
    set is_active = _status,
    updated_by = _updated_by
    where geography_id = _g_id;
END //

DELIMITER ;

DROP PROCEDURE IF EXISTS `sp_get_geography_by_id`;

DELIMITER //

CREATE PROCEDURE `sp_get_geography_by_id`(
in _g_id int(11))
BEGIN
    SELECT geography_id, geography_name, level_id,
    parent_ids, parent_names, is_active
    FROM tbl_geographies WHERE geography_id = _g_id;
END //

DELIMITER ;


DROP PROCEDURE IF EXISTS `sp_user_clients_save`;

DELIMITER //

CREATE PROCEDURE `sp_user_clients_save`(
in userid int(11),
in clientid int(11)
)
BEGIN
    SELECT @u_cat_id := user_category_id from tbl_user_login_details where user_id = userid;
    insert into tbl_user_clients
    (user_id, user_category_id, client_id)
    values
    (userid, @u_cat_id, clientid);
END //

DELIMITER ;

DROP PROCEDURE IF EXISTS `sp_statutory_mapping_report_frequency`;

DELIMITER //

CREATE PROCEDURE `sp_statutory_mapping_report_frequency`()
BEGIN
    select frequency_id, frequency from
    tbl_compliance_frequency;
END //

DELIMITER ;


DROP PROCEDURE IF EXISTS `sp_approve_assigned_statutories_list`;

DELIMITER //

CREATE PROCEDURE `sp_approve_assigned_statutories_list`(
in _u_id int(11))
BEGIN
    SELECT @_user_category_id := user_category_id as user_category_id
    FROM tbl_user_login_details WHERE user_id = _u_id;

    if(@_user_category_id = 7)then
        select  t1.unit_id, t1.statutory_id, t1.domain_id,
        (select country_name from tbl_countries where country_id = t2.country_id)
        as country_name,
        (select group_name from tbl_client_groups where client_id = t1.client_id) as
        group_name,
        (select legal_entity_name from tbl_legal_entities where legal_entity_id = t1.legal_entity_id)
        as legal_entity_name,
        (select business_group_name from tbl_business_groups where
        business_group_id = t2.business_group_id) as business_group_name,
        (select division_name from tbl_divisions where division_id = t2.division_id)
        as division_name,
        (select category_name from tbl_categories where category_id = t2.category_id)
        as category_name,
        (select domain_name from tbl_domains where domain_id = t1.domain_id) as
        domain_name, concat(t2.unit_code,' - ',t2.unit_name) as unit_name
        from
        tbl_client_compliances as t1,
        tbl_units as t2
        where
        t2.unit_id = t1.unit_id and
        t1.unit_id = (select distinct(unit_id) from tbl_user_units
        where user_id = _u_id) and
        t1.is_saved = 1 AND t1.is_approved = 0;
    end if;
END //

DELIMITER ;


DROP PROCEDURE IF EXISTS `sp_get_user_categories_for_user`;

DELIMITER //

CREATE  PROCEDURE `sp_get_user_categories_for_user`(
in userid int(11)
)
BEGIN
    SELECT @u_cat_id := user_category_id from tbl_user_login_details where user_id = userid;
    IF @u_cat_id = 1 then
        SELECT user_category_id, user_category_name FROM tbl_user_category
        WHERE user_category_id in (5,6,7,8);
    ELSEIF @u_cat_id = 5 then
        SELECT user_category_id, user_category_name FROM tbl_user_category
        WHERE user_category_id in (6,7);
    ELSEIF @u_cat_id = 7 then
        SELECT user_category_id, user_category_name FROM tbl_user_category
        WHERE user_category_id in (8);
    END IF;
END //

DELIMITER ;


-- --------------------------------------------------------------------------------
-- Get user category id using userid
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_get_user_category_id_by_userid`;

DELIMITER //

CREATE  PROCEDURE `sp_get_user_category_id_by_userid`(
in userid_ int(11))
BEGIN
    select user_category_id
    from tbl_user_login_details
    where
    user_id = userid_;
END //

DELIMITER ;



DROP PROCEDURE IF EXISTS `sp_audit_trail_usercategory_list`;

DELIMITER //

CREATE PROCEDURE `sp_audit_trail_usercategory_list`()
BEGIN
    SELECT user_category_id, user_category_name
    FROM tbl_user_category where user_category_id >= 2
    or user_category_id = 1;
END //

DELIMITER ;

-- --------------------------------------------------------------------------------
-- Routine DDL
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_get_statutory_level_master`;

DELIMITER //

CREATE PROCEDURE `sp_get_statutory_level_master`()
BEGIN
    select level_id, level_name, level_position, country_id, domain_id
    from tbl_statutory_levels ORDER BY level_position;
END //

DELIMITER ;

-- --------------------------------------------------------------------------------
-- Routine DDL
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_get_statutory_level_count`;

DELIMITER //

CREATE PROCEDURE `sp_get_statutory_level_count`(
in levelId int(11))
BEGIN
    select count(*) as cnt from tbl_statutories where
    level_id = levelId;
END //

DELIMITER ;

-- --------------------------------------------------------------------------------
-- Routine DDL
-- Note: comments before and after the routine body will not be stored by the server
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_delete_statutory_level`;

DELIMITER //

CREATE PROCEDURE `sp_delete_statutory_level`(
in levelId int(11))
BEGIN
    delete from tbl_statutory_levels where level_id = levelId;
END //

DELIMITER ;

-- --------------------------------------------------------------------------------
-- Routine DDL
-- Note: comments before and after the routine body will not be stored by the server
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_insert_statutory_level`;

DELIMITER //

CREATE PROCEDURE `sp_insert_statutory_level`(
in _c_id int(11), _d_id int(11), _l_position int(11), _l_name varchar(50),
_created_by int(11), _created_on timestamp)
BEGIN
    insert into tbl_statutory_levels
    (country_id, domain_id, level_position, level_name, created_by, created_on)
    values
    (_c_id, _d_id, _l_position, _l_name, _created_by, _created_on);
END //

DELIMITER ;

-- --------------------------------------------------------------------------------
-- Routine DDL
-- Note: comments before and after the routine body will not be stored by the server
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_update_statutory_levels`;

DELIMITER //

CREATE PROCEDURE `sp_update_statutory_levels`(
in _position_name int(11),  _l_name varchar(50), _s_l_id int(11), _u_id int(11))
BEGIN
    update tbl_statutory_levels
    set level_position = _position_name,
    level_name = _l_name,
    updated_by = _u_id
    where level_id = _s_l_id;
END //

DELIMITER ;

-- --------------------------------------------
-- ---- reassign user accout user lists
-- -------------------------------------------

DROP PROCEDURE IF EXISTS `sp_tbl_users_techno_managers`;

DELIMITER //

CREATE PROCEDURE `sp_tbl_users_techno_managers`()

BEGIN
    select t1.country_id, t1.domain_id, t1.user_id
        from tbl_user_domains t1 inner join tbl_users as t
        on t.user_id = t1.user_id
        where t.is_active = 1 and t.is_disable = 0 and t.user_category_id = 5;

    select t1.user_id, t1.user_category_id, t1.employee_code, t1.employee_name
        from tbl_users as t1
        inner join tbl_user_login_details as t2 on t1.user_id = t2.user_id
        where t1.is_active = 1
        and t1.is_disable = 0
        and t1.user_category_id = 5
        group by user_id;
END //

DELIMITER ;


DROP PROCEDURE IF EXISTS `sp_tbl_users_techno_executive`;

DELIMITER //

CREATE PROCEDURE `sp_tbl_users_techno_executive`()

BEGIN
    select t1.country_id, t1.domain_id, t1.user_id, group_concat(distinct t2.parent_user_id) as parent_user_ids
        from tbl_user_domains t1 inner join tbl_users as t
        on t.user_id = t1.user_id
        left join tbl_user_mapping t2 on t.user_id = t2.child_user_id and t1.country_id = t2.country_id and t1.domain_id = t2.domain_id
        where t.is_active = 1 and t.is_disable = 0 and t.user_category_id = 6
        group by t1.country_id,t1.domain_id, t1.user_id
        order by t1.country_id, t1.domain_id, t1.user_id;

    select t1.user_id, t1.user_category_id, t1.employee_code, t1.employee_name
        from tbl_users as t1
        inner join tbl_user_login_details as t2 on t1.user_id = t2.user_id
        where t1.is_active = 1
        and t1.is_disable = 0
        and t1.user_category_id = 6
        group by user_id;

END //

DELIMITER ;


DROP PROCEDURE IF EXISTS `sp_tbl_users_domain_managers`;

DELIMITER //

CREATE PROCEDURE `sp_tbl_users_domain_managers`()

BEGIN

    select t1.country_id, t1.domain_id, t1.user_id, group_concat(distinct t2.parent_user_id) as parent_user_ids
        from tbl_user_domains t1 inner join tbl_users as t
        on t.user_id = t1.user_id
        left join tbl_user_mapping t2 on t.user_id = t2.child_user_id and t1.country_id = t2.country_id and t1.domain_id = t2.domain_id
        where t.is_active = 1 and t.is_disable = 0 and t.user_category_id = 7
        group by t1.country_id,t1.domain_id, t1.user_id
        order by t1.country_id, t1.domain_id, t1.user_id;

    select t1.user_id, t1.user_category_id, t1.employee_code, t1.employee_name
        from tbl_users as t1
        inner join tbl_user_login_details as t2 on t1.user_id = t2.user_id
        where t1.user_category_id = 7 and t1.is_active = 1
        and t1.is_disable = 0
        group by user_id;

    select t1.client_id, t1.legal_entity_id, t1.user_id from tbl_user_units as t1
        inner join tbl_users as t2 on t1.user_id = t2.user_id
        where t2.is_active = 1 and t2.is_disable = 0
        and t2.user_category_id = 7;

END //

DELIMITER ;


DROP PROCEDURE IF EXISTS `sp_tbl_users_domain_executive`;

DELIMITER //

CREATE PROCEDURE `sp_tbl_users_domain_executive`()

BEGIN

    select t1.country_id, t1.domain_id, t1.user_id, group_concat(distinct t2.parent_user_id) as parent_user_ids
        from tbl_user_domains t1 inner join tbl_users as t
        on t.user_id = t1.user_id
        left join tbl_user_mapping t2 on t.user_id = t2.child_user_id and t1.country_id = t2.country_id and t1.domain_id = t2.domain_id
        where t.is_active = 1 and t.is_disable = 0 and t.user_category_id = 8
        group by t1.country_id,t1.domain_id, t1.user_id
        order by t1.country_id, t1.domain_id, t1.user_id;

    select t1.user_id, t1.user_category_id, t1.employee_code, t1.employee_name
        from tbl_users as t1
        inner join tbl_user_login_details as t2 on t1.user_id = t2.user_id
        where t1.user_category_id = 8 and t1.is_active = 1
        and t1.is_disable = 0
        group by user_id;


    select t1.client_id, t1.legal_entity_id, t1.user_id from tbl_user_units as t1
        inner join tbl_users as t2 on t1.user_id = t2.user_id
        where t2.is_active = 1 and t2.is_disable = 0
        and t2.user_category_id = 8;

END //

DELIMITER ;


DROP PROCEDURE IF EXISTS `sp_tbl_users_techno_user_info`;

DELIMITER //

CREATE PROCEDURE `sp_tbl_users_techno_user_info`(
    IN uid INT(11)
)
BEGIN

    select @cat_id := user_category_id from tbl_users where user_id = uid;
    if @cat_id = 5 then
        -- techno manager
        select distinct t1.client_id, t1.group_name,
            t2.legal_entity_id, t2.legal_entity_name,
            t2.country_id,
            (select country_name from tbl_countries where country_id = t2.country_id)as country_name,
            (select business_group_name from tbl_business_groups where IFNULL(business_group_id, 0) = t2.business_group_id) as bg_name,
            t4.user_id
            from tbl_client_groups as t1
            inner join tbl_legal_entities as t2 on t1.client_id = t2.client_id
            inner join tbl_user_clients as t3 on t1.client_id = t3.client_id
            inner join tbl_user_legalentity as t4 on t2.legal_entity_id = t4.legal_entity_id
            where t3.user_id = uid order by t1.group_name;

        select t1.legal_entity_id, t1.domain_id, t.domain_name
        from tbl_legal_entity_domains as t1
            inner join tbl_domains as t on t1.domain_id = t.domain_id
            inner join tbl_legal_entities as t2 on t1.legal_entity_id = t2.legal_entity_id
            inner join tbl_user_clients as t3 on t3.client_id = t2.client_id
            where t3.user_id = uid
            group by t1.legal_entity_id, t1.domain_id;
    else
        -- techno executive
        select distinct t1.client_id, t1.group_name,
            t2.legal_entity_id, t2.legal_entity_name, t2.country_id,
            (select country_name from tbl_countries where country_id = t2.country_id)as country_name,
            (select business_group_name from tbl_business_groups where IFNULL(business_group_id, 0) = t2.business_group_id) as bg_name,
            t3.user_id
            from tbl_client_groups as t1
            inner join tbl_legal_entities as t2 on t1.client_id = t2.client_id
            inner join tbl_user_legalentity as t3 on t2.legal_entity_id = t3.legal_entity_id
            where t3.user_id = uid order by t1.group_name;

        select t1.legal_entity_id, t1.domain_id, t.domain_name
            from tbl_legal_entity_domains as t1
            inner join tbl_domains as t on t1.domain_id = t.domain_id
            inner join tbl_user_legalentity as t2 on t1.legal_entity_id = t2.legal_entity_id
            where t2.user_id = uid
            group by t1.legal_entity_id, t1.domain_id;

    end if ;
END //

DELIMITER ;


DROP PROCEDURE IF EXISTS `sp_tbl_users_domain_user_info`;

DELIMITER //

CREATE PROCEDURE `sp_tbl_users_domain_user_info`(
    IN gt_id INT(11), le_id INT(11), did INT(11), uid INT(11)
)
BEGIN
    select distinct t1.unit_id, t1.unit_code, t1.unit_name, t1.address,
        t1.legal_entity_id, t3.legal_entity_name,
        (select geography_name from tbl_geographies where geography_id = t1.geography_id) as location,
        (select user_id from tbl_user_units where unit_id = t1.unit_id and domain_id = did and user_category_id = 8)as child_user
        from tbl_units as t1
        inner join tbl_user_units as t2 on t1.unit_id = t2.unit_id
        inner join tbl_legal_entities as t3 on t1.legal_entity_id = t3.legal_entity_id
        where t2.user_id = uid and t2.domain_id = did and t1.legal_entity_id = le_id
        and t1.client_id = gt_id and
        (select IFNULL(user_id, 0) from tbl_user_units where unit_id = t1.unit_id and domain_id = did and user_category_id = 8) != 0;



END //

DELIMITER ;


DROP PROCEDURE IF EXISTS `sp_tbl_users_replacement`;

DELIMITER //

CREATE PROCEDURE `sp_tbl_users_replacement`(
    IN cat_id INT(11), u_from_id INT(11), u_to_id INT(11), remarks VARCHAR(500),
    sessionuser INT(11)
)
BEGIN
    UPDATE tbl_user_mapping set parent_user_id = u_to_id
        where parent_user_id = u_from_id;

    INSERT INTO tbl_user_replacement_history(
        user_category_id, replaced_from, replaced_by, remarks,
        created_by, created_on
    ) values (cat_id, u_from_id, u_to_id, remarks, sessionuser, current_ist_datetime());

    IF cat_id = 5  THEN
        update tbl_user_clients set user_id = u_to_id where user_id = u_from_id
            and user_category_id = cat_id;
    ELSEIF cat_id = 7 THEN
        update tbl_user_units set user_id = u_to_id where user_id = u_from_id
            and user_category_id = cat_id;
    END IF;


END //

DELIMITER ;


-- --------------------------------------------------------------------------------
-- Configure File Server - gets list
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_file_server_list`;

DELIMITER //

CREATE PROCEDURE `sp_file_server_list`()
BEGIN
    select file_server_id, file_server_name, ip, port, legal_entity_ids
    from tbl_file_server order by file_server_name;
END //

DELIMITER ;

-- --------------------------------------------------------------------------------
-- Configure File Server - save/ update
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_file_server_entry`;

DELIMITER //

CREATE PROCEDURE `sp_file_server_entry`(
in f_s_id int(11), f_s_name varchar(50), f_s_ip varchar(50),
f_s_port int(11), _userid int(11), _created_on timestamp)
BEGIN
    if f_s_id is null then
        insert into tbl_file_server
        (file_server_name, ip, port, created_by, created_on)
        values
        (f_s_name, f_s_ip, f_s_port, _userid, _created_on);
    else
        update tbl_file_server
        set file_server_name = f_s_name,
        ip = f_s_ip, port = f_s_port,
        updated_by = _userid, updated_on = _created_on
        where
        file_server_id = f_s_id;
    end if;
END //

DELIMITER ;

-- --------------------------------------------------------------------------------
-- Configure File Server - Check for duplication of server name
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_file_server_is_duplicate`;

DELIMITER //

CREATE PROCEDURE `sp_file_server_is_duplicate`(
    IN fileservername VARCHAR(50), fileserverid INT(11)
)
BEGIN
    IF fileserverid IS NULL THEN
        SELECT count(file_server_id) as count FROM tbl_file_server
        WHERE file_server_name = fileservername;
    ELSE
        SELECT count(file_server_id) as count FROM tbl_file_server
        WHERE file_server_name = fileservername and file_server_id != fileserverid;
    END IF;
END //

DELIMITER ;

-- --------------------------------------------------------------------------------
-- Save Message for client unit
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_client_unit_messages_save`;

DELIMITER //

CREATE PROCEDURE `sp_client_unit_messages_save`(
in _u_id int(11), _link text, _client_id int(11), _le_id int(11),
    _g_id int(11), _u_code varchar(50), _created_on timestamp)
BEGIN
    select @cl_name := group_name from tbl_client_groups where client_id=_client_id;
    select @le_name := legal_entity_name from tbl_legal_entities where
    legal_entity_id = _le_id;
    select @u_location := geography_name from tbl_geographies where
    geography_id = _g_id;
    INSERT INTO tbl_messages
    SET
    user_category_id = (select user_category_id from tbl_user_login_details
    where user_id = (select user_id from tbl_user_clients where client_id = _client_id)),
    message_heading = 'Client Unit Added',
    message_text = (select concat(@cl_name,' & ',@le_name,' - ',@u_location,' & ',_u_code,
    ' has been created')),
    link = null, created_by = _u_id, created_on = _created_on;

    set @msg_id := LAST_INSERT_ID();

    INSERT INTO tbl_message_users
    SET
    message_id = @msg_id,
    user_id = (select user_id from tbl_user_clients where client_id = _client_id);

    INSERT INTO tbl_messages
    SET
    user_category_id = 1,
    message_heading = 'Client Unit Added',
    message_text = (select concat(@cl_name,' & ',@le_name,' - ',@u_location,' & ',_u_code,
    ' has been created')),
    link = null, created_by = _u_id, created_on = _created_on;

    set @msg_id := LAST_INSERT_ID();
    INSERT INTO tbl_message_users
    SET
    message_id = @msg_id,
    user_id = (select user_id from tbl_user_login_details where user_category_id = 1 limit 1);
END //

DELIMITER ;


-- --------------------------------------------------------------------------------
-- Update message for client unit
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_client_unit_messages_update`;

DELIMITER //

CREATE PROCEDURE `sp_client_unit_messages_update`(
in _u_id int(11), _link text, _client_id int(11), _le_id int(11),
    _unit_id int(11), _created_on timestamp)
BEGIN
    select @cl_name := group_name from tbl_client_groups where client_id=_client_id;
    select @le_name := legal_entity_name from tbl_legal_entities where
    legal_entity_id = _le_id;
    select @u_location := geography_name from tbl_geographies where
    geography_id = (select geography_id from tbl_units where unit_id = _unit_id);
    select @u_code := unit_code from tbl_units where unit_id=_unit_id;
    INSERT INTO tbl_messages
    SET
    user_category_id = (select user_category_id from tbl_user_login_details
    where user_id = (select user_id from tbl_user_clients where client_id = _client_id)),
    message_heading = 'Client Unit Updated',
    message_text = (select concat(@cl_name,' & ',@le_name,' - ',@u_location,' & ',@u_code,
    'has been updated')),
    link = _link, created_by = _u_id, created_on = _created_on;

    set @msg_id := LAST_INSERT_ID();

    INSERT INTO tbl_message_users
    SET
    message_id = @msg_id,
    user_id = (select user_id from tbl_user_clients where client_id = _client_id);

    INSERT INTO tbl_messages
    SET
    user_category_id = 1,
    message_heading = 'Client Unit Updated',
    message_text = (select concat(@cl_name,' & ',@le_name,' - ',@u_location,' & ',@u_code,
    'has been updated')),
    link = _link, created_by = _u_id, created_on = _created_on;

    set @msg_id := LAST_INSERT_ID();
    INSERT INTO tbl_message_users
    SET
    message_id = @msg_id,
    user_id = (select user_id from tbl_user_login_details where user_category_id = 1 limit 1);

    if (select count(*) from tbl_user_units where unit_id=_unit_id and user_category_id = 7) > 0 then
        INSERT INTO tbl_messages
        SET
        user_category_id = 7,
        message_heading = 'Client Unit Updated',
        message_text = (select concat(@cl_name,' & ',@le_name,' - ',@u_location,' & ',@u_code,
        'has been updated')),
        link = _link, created_by = _u_id, created_on = _created_on;

        set @msg_id := LAST_INSERT_ID();
        select @usr_id := user_id from tbl_user_units where user_category_id = 7 and unit_id = _unit_id;
        INSERT INTO tbl_message_users
        SET
        message_id = @msg_id,
        user_id = (select user_id from tbl_user_login_details where user_id = @usr_id);
    End if;
    if (select count(*) from tbl_user_units where unit_id=_unit_id and user_category_id = 8) > 0 then
        INSERT INTO tbl_messages
        SET
        user_category_id = 8,
        message_heading = 'Client Unit Updated',
        message_text = (select concat(@cl_name,' & ',@le_name,' - ',@u_location,' & ',@u_code,
        'has been updated')),
        link = _link, created_by = _u_id, created_on = _created_on;

        set @msg_id := LAST_INSERT_ID();
        select @usr_id := user_id from tbl_user_units where user_category_id = 8 and unit_id = _unit_id;
        INSERT INTO tbl_message_users
        SET
        message_id = @msg_id,
        user_id = (select user_id from tbl_user_login_details where user_id = @usr_id);
    End if;
END //

DELIMITER ;

-- --------------------------------------------------------------------------------
-- Save message of unit assigned to user - assign client unit
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_assign_client_unit_save`;

DELIMITER //

CREATE PROCEDURE `sp_assign_client_unit_save`(
in _user_id int(11), _unit_id int(11), _d_id int(11), _link text, _created_by int(11),
    _created_on timestamp)
BEGIN
    if(select ifnull(business_group_name,null) from tbl_business_groups where business_group_id =
    (select business_group_id from tbl_units where unit_id = _unit_id)) != '' then
        set @msg_txt := (select concat
        ((select group_name from tbl_client_groups where client_id =
        (select client_id from tbl_units where unit_id = _unit_id)),'-',
        (select ifnull(business_group_name,null) from tbl_business_groups where business_group_id =
        (select business_group_id from tbl_units where unit_id = _unit_id)),'-',
        (select legal_entity_name from tbl_legal_entities where legal_entity_id =
        (select legal_entity_id from tbl_units where unit_id = _unit_id)),'-',
        (select group_concat(organisation_name) from tbl_organisation where organisation_id in
        (select organisation_id from tbl_units_organizations where domain_id = _d_id and unit_id=_unit_id)),'-',
        (select concat(unit_code,'-',unit_name,' ','unit has been assigned')
        from tbl_units where unit_id = _unit_id)));
    else
        set @msg_txt := (select concat
        ((select group_name from tbl_client_groups where client_id =
        (select client_id from tbl_units where unit_id = _unit_id)),'-',
        (select legal_entity_name from tbl_legal_entities where legal_entity_id =
        (select legal_entity_id from tbl_units where unit_id = _unit_id)),'-',
        (select group_concat(organisation_name) from tbl_organisation where organisation_id in
        (select organisation_id from tbl_units_organizations where domain_id = _d_id and unit_id=_unit_id)),'-',
        (select concat(unit_code,'-',unit_name,' ','unit has been assigned')
        from tbl_units where unit_id = _unit_id)));
    end if;

    INSERT INTO tbl_messages
    SET
    user_category_id = (select user_category_id from tbl_user_login_details
    where user_id = _user_id),
    message_heading = 'Assign Client Unit',
    message_text = @msg_txt,
    link = _link, created_by = _created_by, created_on = _created_on;

    SET @msg_id := LAST_INSERT_ID();

    INSERT INTO tbl_message_users
    SET
    message_id = @msg_id,
    user_id = _user_id;

    select @compfie_id := user_id from tbl_user_login_details where user_category_id = 1 limit 1;

    INSERT INTO tbl_messages
    SET
    user_category_id = 1,
    message_heading = 'Assign Client Unit',
    message_text = @msg_txt,
    link = _link, created_by = _created_by, created_on = _created_on;

    SET @msg_id := LAST_INSERT_ID();

    INSERT INTO tbl_message_users(message_id, user_id, read_status) values(@msg_id, @compfie_id, 0);

END //

DELIMITER ;

-- --------------------------------------------------------------------------------
-- Save Notification message  - assign legal entity
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_assign_legal_entity_save_message`;

DELIMITER //

CREATE PROCEDURE `sp_assign_legal_entity_save_message`(
in _user_id int(11), _le_id int(11), _link text, _created_by int(11), _created_on timestamp)
BEGIN
    INSERT INTO tbl_messages
    SET
    user_category_id = (select user_category_id from tbl_user_login_details
    where user_id = _user_id),
    message_heading = 'Assign Legal Entity',
    message_text = (select concat(legal_entity_name,' ','has been assigned')
    from tbl_legal_entities where legal_entity_id = _le_id),
    link = _link, created_by = _created_by, created_on = _created_on;

    INSERT INTO tbl_message_users
    SET
    message_id = (select LAST_INSERT_ID()),
    user_id = _user_id;
END //

DELIMITER ;

-- --------------------------------------------------------------------------------
-- Allocate Database Environemnt - Get Details
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_allocate_db_environment_report_getdata`;

DELIMITER //

CREATE PROCEDURE `sp_allocate_db_environment_report_getdata`()
BEGIN
    select t1.client_id, (select group_name from tbl_client_groups where
    client_id = t1.client_id)as group_name, t1.legal_entity_id,
    (select legal_entity_name from tbl_legal_entities where legal_entity_id =
    t1.legal_entity_id) as legal_entity_name, t1.machine_id,
    (select machine_name from tbl_application_server where machine_id =
    t1.machine_id) as machine_name, t1.database_server_id, t1.client_database_server_id,
    (select database_server_name from tbl_database_server where
    database_server_id = t1.database_server_id) as db_server_name,
    (select database_server_name from tbl_database_server where database_server_id =
    client_database_server_id) as client_db_server_name,
    t1.file_server_id, (select file_server_name from tbl_file_server where
    file_server_id = t1.file_server_id) as file_server_name
    from
    tbl_client_database as t1;
END //

DELIMITER ;

-- --------------------------------------------------------------------------------
-- To Get data for IP Settings form
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_ip_settings_list`;

DELIMITER //

CREATE PROCEDURE `sp_ip_settings_list`()
BEGIN
    SELECT client_id, group_name FROM tbl_client_groups;

    SELECT form_id, form_name
    FROM tbl_client_forms where form_type_id = 2 order by form_order;

    SELECT ips.client_id, ips.form_id,
    (select group_name from tbl_client_groups where client_id = ips.client_id) as group_name
    FROM tbl_ip_settings ips group by ips.client_id order by group_name;
END //

DELIMITER ;

-- --------------------------------------------------------------------------------
-- To Get data for Client IP Details
-- --------------------------------------------------------------------------------

DROP PROCEDURE IF EXISTS `sp_group_ip_details`;

DELIMITER //

CREATE PROCEDURE `sp_group_ip_details`(
    IN c_id INT(11)
)
BEGIN
    SELECT form_id, ips, client_id FROM tbl_ip_settings where client_id = c_id;
END //

DELIMITER ;

-- --------------------------------------------------------------------------------
-- To delete IP Setting details of particular client
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_ip_settings_delete`;

DELIMITER //

CREATE PROCEDURE `sp_ip_settings_delete`(
    IN c_id INT(11)
)
BEGIN
    DELETE FROM tbl_ip_settings
    WHERE client_id=c_id;
END //

DELIMITER ;

-- --------------------------------------------------------------------------------
-- To get name of group
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_group_name_by_id`;

DELIMITER //


CREATE PROCEDURE `sp_group_name_by_id`(
    IN c_id INT(11)
)
BEGIN
    SELECT group_name
    FROM tbl_client_groups
    WHERE client_id=c_id;
END //

DELIMITER ;


-- --------------
-- statutory mapping report data
-- -------------
DROP PROCEDURE IF EXISTS `sp_tbl_statutory_mappings_reportdata`;

DELIMITER //

CREATE PROCEDURE `sp_tbl_statutory_mappings_reportdata`(
in cid int(11), did int(11), iid int(11), snid int(11), gid int(11),
l1sid int(11), fid int(11),  uid int(11), fcount int(11), tcount int(11)
)
BEGIN
    select @ucat := user_category_id from tbl_user_login_details where user_id = uid;
    IF @ucat = 1 THEN
        set @uid = '%';
    ELSE
        set @uid = uid;
    END IF;
    -- records count
    SELECT  count(distinct t2.compliance_id) as count
         FROM tbl_statutory_mappings t1
         INNER JOIN tbl_compliances t2
         ON t2.statutory_mapping_id = t1.statutory_mapping_id
         INNER JOIN tbl_mapped_industries t3
         ON t3.statutory_mapping_id = t1.statutory_mapping_id
         INNER JOIN tbl_mapped_locations t4
         ON t4.statutory_mapping_id = t1.statutory_mapping_id
         inner join tbl_mapped_statutories as ts
         on ts.statutory_mapping_id = t1.statutory_mapping_id
         INNER JOIN tbl_user_domains t5
         ON t5.domain_id = t1.domain_id and t5.country_id = t1.country_id
         and t5.user_id like @uid

         WHERE t2.is_approved in (2, 3) AND t2.is_active = 1 AND
         t1.country_id = cid
         and t1.domain_id = did
         and  IF(iid IS NOT NULL, t3.organisation_id = iid, 1)
         and  IF(gid IS NOT NULL, t4.geography_id = gid, 1)
         and IF(snid IS NOT NULL, t1.statutory_nature_id = snid, 1)
         and IF(l1sid IS NOT NULL, ts.statutory_id in (select statutory_id from tbl_statutories where statutory_id = l1sid OR find_in_set(l1sid, parent_ids)), 1)
         and IF(fid is not NULL, t2.frequency_id = fid, 1)
         ORDER BY t1.statutory_mapping, t2.frequency_id;

    -- records
    SELECT distinct t1.statutory_mapping_id, t1.country_id,
        (select country_name from tbl_countries
        where country_id = t1.country_id)
        country_name,  t1.domain_id,
        (select domain_name from tbl_domains
        where domain_id = t1.domain_id) domain_name,
        -- t1.industry_ids,
        t1.statutory_nature_id,
        (select statutory_nature_name from tbl_statutory_natures
        where statutory_nature_id = t1.statutory_nature_id)
        statutory_nature_name,  -- t1.statutory_ids, t1.geography_ids,
        t1.is_approved, t1.is_active, t1.statutory_mapping,
        t2.compliance_id, t2.statutory_provision,
        t2.compliance_task, t2.compliance_description,
        t2.document_name, t2.format_file, t2.format_file_size,
        t2.penal_consequences, t2.frequency_id,
        t2.statutory_dates, t2.repeats_every,
        t2.repeats_type_id, t2.duration, t2.duration_type_id,
        (select frequency from tbl_compliance_frequency where frequency_id = t2.frequency_id) as freq_name,
        (select repeat_type from tbl_compliance_repeat_type where repeat_type_id = t2.repeats_type_id) as repeat_type,
        (select duration_type from tbl_compliance_duration_type where duration_type_id = t2.duration_type_id) as duration_type
        FROM tbl_statutory_mappings t1
        INNER JOIN tbl_compliances t2
        ON t2.statutory_mapping_id = t1.statutory_mapping_id
        INNER JOIN tbl_mapped_industries t3
        ON t3.statutory_mapping_id = t1.statutory_mapping_id
        INNER JOIN tbl_mapped_locations t4
        ON t4.statutory_mapping_id = t1.statutory_mapping_id
        inner join tbl_mapped_statutories as ts
        on ts.statutory_mapping_id = t1.statutory_mapping_id
        INNER JOIN tbl_user_domains t5
        ON t5.domain_id = t1.domain_id and t5.country_id = t1.country_id
        and t5.user_id like @uid
        WHERE t2.is_approved in (2, 3)
        AND t2.is_active = 1 AND t1.country_id = cid
        and t1.domain_id = did
        and  IF(iid IS NOT NULL, t3.organisation_id = iid, 1)
        and  IF(gid IS NOT NULL, t4.geography_id = gid, 1)
        and  IF(snid IS NOT NULL, t1.statutory_nature_id = snid, 1)
        and  IF(l1sid IS NOT NULL, ts.statutory_id in (select statutory_id from tbl_statutories where statutory_id = l1sid OR find_in_set(l1sid, parent_ids)), 1)
        and  IF(fid is not NULL, t2.frequency_id = fid, 1)
        ORDER BY t1.statutory_mapping, t2.frequency_id
        limit fcount, tcount;

    -- organisation info
    select distinct t.organisation_id, t.organisation_name, t1.statutory_mapping_id from tbl_organisation as t
         inner join tbl_mapped_industries as t1 on t1.organisation_id = t.organisation_id
         inner join tbl_compliances as t2 on t1.statutory_mapping_id = t2.statutory_mapping_id
         inner join tbl_user_domains as t3 on t3.country_id = t2.country_id and t3.domain_id = t2.domain_id
         where t2.is_approved in (2,3) and t3.user_id like @uid
         and t2.country_id = cid
         and t2.domain_id = did
         and  IF(iid IS NOT NULL, t1.organisation_id = iid, 1)
        order by t1.statutory_mapping_id;

    -- geography info
    SELECT distinct t1.geography_id, t1.geography_name, t1.parent_names, t2.statutory_mapping_id from tbl_geographies as t1
            inner join tbl_mapped_locations as t2 on t2.geography_id = t1.geography_id
            inner join tbl_compliances as t3 on t3.statutory_mapping_id = t2.statutory_mapping_id
            inner join tbl_user_domains as t5 on t5.country_id = t3.country_id and t5.domain_id = t3.domain_id
            where t3.is_approved in(2,3) and t5.user_id like @uid
            and t3.country_id = cid
            and t3.domain_id = did
            and  IF(gid IS NOT NULL, t2.geography_id = gid, 1)
            order by t3.statutory_mapping_id;
END //

DELIMITER ;

-- --------------------------------------------------------------------------------
-- To Get data for IP Settings report filter
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_ip_settings_report_filter`;

DELIMITER //

CREATE PROCEDURE `sp_ip_settings_report_filter`()
BEGIN
    SELECT client_id, group_name FROM tbl_client_groups;

    SELECT form_id, form_name
    FROM tbl_client_forms where form_type_id = 2 order by form_order;
END //

DELIMITER ;

-- --------------------------------------------------------------------------------
-- To Get data for Client IP Details
-- --------------------------------------------------------------------------------

DROP PROCEDURE IF EXISTS `sp_ip_setting_details_report`;

DELIMITER //

CREATE PROCEDURE `sp_ip_setting_details_report`(
    IN c_id INT(11), IN ip_ VARCHAR(50), IN f_count INT(11), IN t_count INT(11)
)
BEGIN

    SELECT count(distinct client_id) as total_record FROM tbl_ip_settings
    where
    IF(c_id IS NOT NULL, client_id = c_id, 1) and
    IF(ip_ IS NOT NULL, ips = ip_, 1);

    SELECT t2.form_id,t2.client_id, t2.ips
    From tbl_ip_settings t2
    inner join (
    SELECT t.client_id,
           @rownum := @rownum + 1 AS num
    FROM (select distinct client_id from tbl_ip_settings order by client_id) t,
           (SELECT @rownum := 0) r
          ) t3 on t2.client_id = t3.client_id
    where
    IF(c_id IS NOT NULL, t2.client_id = c_id, 1) and
    IF(ip_ IS NOT NULL, t2.ips = ip_, 1) and
    t3.num between f_count and t_count
    order by t2.client_id;

    /*SELECT form_id, ips, client_id FROM tbl_ip_settings
    where
    IF(c_id IS NOT NULL, client_id = c_id, 1) and
    IF(ip_ IS NOT NULL, ips = ip_, 1)
    order by client_id
    limit f_count, t_count*/
END //

DELIMITER ;

-- -------------------
-- database server info
-- -------------------
DROP PROCEDURE IF EXISTS `sp_get_environment_byid`;

DELIMITER //

CREATE PROCEDURE `sp_get_environment_byid`(
in dsid int(11), asid int(11), fsid int(11))
BEGIN
    SELECT database_server_id, database_server_name,
        database_ip, database_port, database_username, database_password
    FROM tbl_database_server WHERE database_server_id = dsid;

    SELECT machine_id, machine_name, ip, port
    FROM tbl_application_server where machine_id = asid;

    SELECT file_server_id, file_server_name, ip, port
    FROM tbl_file_server WHERE file_server_id = fsid;
END //

DELIMITER ;

DROP PROCEDURE IF EXISTS `sp_tbl_client_groups_createdb_info`;

DELIMITER //

CREATE PROCEDURE `sp_tbl_client_groups_createdb_info`(
in gpid int(11), cdbid int(11), ledbid int(11))
BEGIN

    select group_name, short_name, email_id,
        (select IFNULL(count(client_id), 0) from tbl_client_database where client_id = gpid) as cnt
    from tbl_client_groups where client_id = gpid;

    SELECT database_server_id, database_server_name,
        database_ip, database_port, database_username, database_password
    FROM tbl_database_server WHERE database_server_id in (cdbid, ledbid);

END //

DELIMITER ;

-- Allocate Database Environemnt - Get Details
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_allocate_db_environment_report_getdata`;

DELIMITER //

CREATE PROCEDURE `sp_allocate_db_environment_report_getdata`()
BEGIN
    select t1.client_id, (select group_name from tbl_client_groups where
    client_id = t1.client_id)as group_name, t1.legal_entity_id,
    (select legal_entity_name from tbl_legal_entities where legal_entity_id =
    t1.legal_entity_id) as legal_entity_name, t1.machine_id,
    (select machine_name from tbl_application_server where machine_id =
    t1.machine_id) as machine_name, t1.database_server_id, t1.client_database_server_id,
    (select database_server_name from tbl_database_server where
    database_server_id = t1.database_server_id) as db_server_name,
    (select database_server_name from tbl_database_server where database_server_id =
    client_database_server_id) as client_db_server_name,
    t1.file_server_id, (select file_server_name from tbl_file_server where
    file_server_id = t1.file_server_id) as file_server_name
    from
    tbl_client_database as t1;
END //

DELIMITER ;

-- --------------------------------------------------------------------------------
-- To export user mapping report
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_usermapping_report_details_for_export`;

DELIMITER //

CREATE PROCEDURE `sp_usermapping_report_details_for_export`(
    in userId int(11), clientId int(11), legalId int(11), counrtyId int(11),
    bgrp_id varchar(10), _divi_id varchar(11), _cg_id varchar(11), _unit_id varchar(11))
BEGIN
    SELECT @_user_category_id := user_category_id as user_category_id
    FROM tbl_user_login_details WHERE user_id = userId;

    if(@_user_category_id = 1)then
        select t4.unit_id, concat(t_mgr.employee_code,'-',t_mgr.employee_name) as techno_manager,
        concat(t_usr.employee_code,'-',t_usr.employee_name) as techno_user,
        (select concat(unit_code,'-',unit_name) from tbl_units where unit_id = t4.unit_id) as unit_name,
        (select country_name from tbl_countries where country_id=counrtyId) as country_name,
        (select group_name from tbl_client_groups where client_id=clientId) as group_name,
        (select business_group_name from tbl_business_groups where business_group_id=
        t3.business_group_id) as business_group_name,
        (select legal_entity_name from tbl_legal_entities where legal_entity_id=
        legalId) as legal_entity_name,
        (select division_name from tbl_divisions where division_id=t4.division_id)
        as division_name,
        (select category_name from tbl_categories where category_id=t4.category_id)
        as category_name
        from
        tbl_user_legalentity as t1 inner join tbl_user_clients as t2
        on t2.client_id = t1.client_id
        inner join tbl_legal_entities as t3 on t3.client_id = t1.client_id and
        t3.legal_entity_id = t1.legal_entity_id
        inner join tbl_users as t_mgr on t_mgr.user_id = t2.user_id
        inner join tbl_users as t_usr on t_usr.user_id = t1.user_id
        inner join tbl_units as t4 on t4.client_id = t1.client_id and
        t4.legal_entity_id = t3.legal_entity_id and
        t4.country_id = t3.country_id
        where
        coalesce(t4.category_id,'') like _cg_id and coalesce(t4.division_id,'') like _divi_id and
        coalesce(t4.unit_id,'')like _unit_id and coalesce(t4.business_group_id,'') like bgrp_id and
        t3.country_id = counrtyId and
        coalesce(t3.business_group_id,'') like bgrp_id and
        t1.legal_entity_id = legalId and
        t1.client_id = clientId;
        -- group by t1.user_id


        select t1.unit_id, concat(t2.employee_code,'-',t2.employee_name)as employee_name,
        t3.user_category_name,t1.domain_id
        from
        tbl_user_units as t1,tbl_units as t4,tbl_users as t2,
        tbl_user_category as t3
        where
        t3.user_category_id = t1.user_category_id and
        t2.user_id = t1.user_id and
        coalesce(t4.category_id,'') like _cg_id and
        coalesce(t4.division_id,'') like _divi_id and
        t4.unit_id = t1.unit_id and
        t4.country_id = counrtyId and
        coalesce(t1.unit_id,'') like _unit_id and
        t1.legal_entity_id =legalId and
        t1.client_id = clientId;

        select distinct(t3.domain_id),t3.domain_name,t3.is_active
        from
        tbl_user_units as t1,tbl_units_organizations as t2,tbl_domains as t3
        where
        t3.domain_id = t2.domain_id and
        t2.unit_id = t1.unit_id and
        coalesce(t1.unit_id,'') like _unit_id and
        t1.legal_entity_id =legalId and
        t1.client_id = clientId
        order by t3.domain_name;
    elseif (@_user_category_id = 5)then
        select t4.unit_id, concat(t_mgr.employee_code,'-',t_mgr.employee_name) as techno_manager,
        concat(t_usr.employee_code,'-',t_usr.employee_name) as techno_user,
        (select concat(unit_code,'-',unit_name) from tbl_units where unit_id = t4.unit_id) as unit_name,
        (select country_name from tbl_countries where country_id=counrtyId) as country_name,
        (select group_name from tbl_client_groups where client_id=clientId) as group_name,
        (select business_group_name from tbl_business_groups where business_group_id=
        t3.business_group_id) as business_group_name,
        (select legal_entity_name from tbl_legal_entities where legal_entity_id=
        legalId) as legal_entity_name,
        (select division_name from tbl_divisions where division_id=t4.division_id)
        as division_name,
        (select category_name from tbl_categories where category_id=t4.category_id)
        as category_name
        from
        tbl_user_legalentity as t1 inner join tbl_user_clients as t2
        on t2.client_id = t1.client_id
        inner join tbl_legal_entities as t3 on t3.client_id = t1.client_id and
        t3.legal_entity_id = t1.legal_entity_id
        inner join tbl_users as t_mgr on t_mgr.user_id = t2.user_id
        inner join tbl_users as t_usr on t_usr.user_id = t1.user_id
        inner join tbl_units as t4 on t4.client_id = t1.client_id and
        t4.legal_entity_id = t3.legal_entity_id and
        t4.country_id = t3.country_id
        where
        coalesce(t4.category_id,'') like _cg_id and coalesce(t4.division_id,'') like _divi_id and
        coalesce(t4.unit_id,'')like _unit_id and coalesce(t4.business_group_id,'') like bgrp_id and
        t3.country_id = counrtyId and
        coalesce(t3.business_group_id,'') like bgrp_id and
        t1.legal_entity_id = legalId and
        t1.client_id = clientId;
        -- group by t1.user_id



        select t1.unit_id, concat(t2.employee_code,'-',t2.employee_name)as employee_name,
        t3.user_category_name,t1.domain_id
        from
        tbl_user_units as t1,tbl_units as t4,tbl_users as t2,
        tbl_user_category as t3
        where
        t3.user_category_id = t1.user_category_id and
        t2.user_id = t1.user_id and
        coalesce(t4.category_id,'') like _cg_id and
        coalesce(t4.division_id,'') like _divi_id and
        t4.unit_id = t1.unit_id and
        t4.country_id = counrtyId and
        coalesce(t1.unit_id,'') like _unit_id and
        t1.legal_entity_id =legalId and
        t1.client_id = clientId;

        select distinct(t3.domain_id),t3.domain_name,t3.is_active
        from
        tbl_user_units as t1,tbl_units_organizations as t2,tbl_domains as t3
        where
        t3.domain_id = t2.domain_id and
        t2.unit_id = t1.unit_id and
        coalesce(t1.unit_id,'') like _unit_id and
        t1.legal_entity_id =legalId and
        t1.client_id = clientId
        order by t3.domain_name;
    elseif (@_user_category_id = 7)then
        select t4.unit_id, concat(t_mgr.employee_name,'-',t_mgr.employee_name) as techno_manager,
        concat(t_usr.employee_code,'-',t_usr.employee_name) as techno_user,
        (select concat(unit_code,'-',unit_name) from tbl_units where unit_id = t4.unit_id) as unit_name,
        (select country_name from tbl_countries where country_id=counrtyId) as country_name,
        (select group_name from tbl_client_groups where client_id=clientId) as group_name,
        (select business_group_name from tbl_business_groups where business_group_id=
        t5.business_group_id) as business_group_name,
        (select legal_entity_name from tbl_legal_entities where legal_entity_id=
        legalId) as legal_entity_name,
        (select division_name from tbl_divisions where division_id=t5.division_id)
        as division_name,
        (select category_name from tbl_categories where category_id=t5.category_id)
        as category_name
        from
        tbl_user_units as t4 inner join tbl_units as t5 on
        t5.unit_id = t4.unit_id inner join tbl_user_clients as t2 on
        t2.client_id = t4.client_id
        inner join tbl_user_legalentity as t1 on t1.legal_entity_id = t4.legal_entity_id
        inner join tbl_users as t_mgr on t_mgr.user_id = t2.user_id
        inner join tbl_users as t_usr on t_usr.user_id = t1.user_id

        where
        coalesce(t5.category_id,'') like _cg_id and coalesce(t5.division_id,'') like _divi_id and
        t5.country_id = counrtyId and
        coalesce(t4.unit_id,'')like _unit_id and
        coalesce(t5.business_group_id,'') like bgrp_id and
        t4.user_id = userId and t4.user_category_id = 7 and
        t4.legal_entity_id = legalId and
        t4.client_id = clientId
        group by t4.unit_id;


        select t1.unit_id, concat(t2.employee_code,'-',t2.employee_name)as employee_name,
        t3.user_category_name,t1.domain_id
        from
        tbl_user_units as t1,tbl_units as t4,tbl_users as t2,
        tbl_user_category as t3
        where
        t3.user_category_id = t1.user_category_id and
        t2.user_id = t1.user_id and
        coalesce(t4.category_id,'') like _cg_id and
        coalesce(t4.division_id,'') like _divi_id and
        t4.unit_id = t1.unit_id and
        t4.country_id = counrtyId and
        coalesce(t1.unit_id,'') like _unit_id and
        t1.legal_entity_id =legalId and
        t1.client_id = clientId;

        select distinct(t3.domain_id),t3.domain_name,t3.is_active
        from
        tbl_user_units as t1,tbl_units_organizations as t2,tbl_domains as t3
        where
        t3.domain_id = t2.domain_id and
        t2.unit_id = t1.unit_id and
        coalesce(t1.unit_id,'') like _unit_id and
        t1.legal_entity_id =legalId and
        t1.client_id = clientId
        order by t3.domain_name;
    end if;
END //

DELIMITER ;

-- --------------------------------------------------------------------------------
-- Export client details
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_client_details_report_export_unitlist`;

DELIMITER //

CREATE PROCEDURE `sp_client_details_report_export_unitlist`(
    in _user int(11), _country int(11), _client int(11), _legal int(11),
    _bgrp varchar(50), _domain varchar(50), _org varchar(50),
    _unit varchar(50), _from varchar(50), _to varchar(50),
    _status varchar(10)
)
BEGIN
    SELECT @u_cat_id := user_category_id from tbl_user_login_details where user_id = _user;

    IF @u_cat_id = 1 THEN
        select t3.country_id, t3.client_id, t3.legal_entity_id, t3.business_group_id,
        t3.unit_id, t3.unit_code, t3.unit_name, t3.address, t3.postal_code, t3.is_closed
        as is_active, date_format(t3.closed_on, '%d-%b-%Y') as closed_on,
        date_format(t3.created_on, '%d-%b-%Y') as check_date,
        (select concat(employee_code,'-',employee_name) from tbl_users
        where user_id = t3.created_by)as emp_code_name,
        date_format(t3.created_on, '%d/%m/%Y') as created_on,
        (select division_name from tbl_divisions where
        division_id = t3.division_id) as division_name,
        (select category_name from tbl_categories where
        category_id = t3.category_id) as category_name,
        (select country_name from tbl_countries where country_id = _country) as country_name,
        (select group_name from tbl_client_groups where client_id = t1.client_id) as group_name,
        (select business_group_name from tbl_business_groups where business_group_id =
        t2.business_group_id) as business_group_name,
        (select legal_entity_name from tbl_legal_entities where legal_entity_id =
        t2.legal_entity_id) as legal_entity_name,
        (select concat(employee_code,'-',employee_name) from tbl_users where
        user_id = (select user_id from tbl_user_clients where
        client_id = t1.client_id)) as techno_manager,
        DATEDIFF(now(),t3.closed_on) as closed_days
        from
        tbl_client_groups as t1 inner join tbl_legal_entities as t2
        on t1.client_id = t2.client_id
        inner join tbl_units as t3 on t3.client_id = t1.client_id and
        t2.legal_entity_id = t3.legal_entity_id
        -- t2.business_group_id = t3.business_group_id
        inner join tbl_units_organizations as t4 on t4.unit_id = t3.unit_id
        and coalesce(t4.domain_id,'') like _domain and
        coalesce(t4.organisation_id,'') like _org
        where
        (case when _status = '%' then coalesce(t3.is_closed,'') like _status
        when _status = "0" then t3.is_closed = 0
        when _status = "1" then (t3.is_closed  = 1 and DATEDIFF(NOW(),t3.closed_on) > 30)
        when _status = "2" then (t3.is_closed  = 1 and DATEDIFF(NOW(),t3.closed_on) <= 30)
        end) and
        IF(_from IS NOT NULL, t3.created_on >= _from, 1) and
        IF(_to IS NOT NULL, t3.created_on < DATE_ADD(_to,interval 1 DAY), 1) and
        coalesce(t3.unit_id,'') like _unit and
        coalesce(t2.business_group_id,'') like _bgrp and
        t2.legal_entity_id = _legal and t2.country_id = _country and
        t1.client_id = _client group by t3.unit_id
        order by t3.unit_name;
    END IF;
    if @u_cat_id = 5 THEN
        select t3.country_id, t3.client_id, t3.legal_entity_id, t3.business_group_id,
        t3.unit_id, t3.unit_code, t3.unit_name, t3.address, t3.postal_code, t3.is_closed
        as is_active, date_format(t3.closed_on, '%d-%b-%Y') as closed_on,
        date_format(t3.created_on, '%d-%b-%Y') as check_date,
        (select concat(employee_code,'-',employee_name) from tbl_users
        where user_id = t3.created_by)as emp_code_name,
        date_format(t3.created_on, '%d/%m/%Y') as created_on,
        (select division_name from tbl_divisions where
        division_id = t3.division_id) as division_name,
        (select category_name from tbl_categories where
        category_id = t3.category_id) as category_name,
        (select group_name from tbl_client_groups where client_id = t1.client_id) as group_name,
        (select business_group_name from tbl_business_groups where business_group_id =
        t2.business_group_id) as business_group_name,
        (select legal_entity_name from tbl_legal_entities where legal_entity_id =
        t2.legal_entity_id) as legal_entity_name,
        (select concat(employee_code,'-',employee_name) from tbl_users where
        user_id = t1.client_id) as techno_manager,
        DATEDIFF(NOW(),t3.closed_on) as closed_days
        from
        tbl_user_clients as t1 inner join tbl_legal_entities as t2
        on t1.client_id = t2.client_id
        inner join tbl_units as t3 on t2.client_id = t3.client_id and
        t3.client_id = t1.client_id and
        t2.legal_entity_id = t3.legal_entity_id
        -- t2.business_group_id = t3.business_group_id
        inner join tbl_units_organizations as t4 on t4.unit_id = t3.unit_id
        and coalesce(t4.domain_id,'') like _domain and
        coalesce(t4.organisation_id,'') like _org
        where
        (case when _status = '%' then coalesce(t3.is_closed,'') like _status
        when _status = "0" then t3.is_closed = 0
        when _status = "1" then (t3.is_closed  = 1 and DATEDIFF(NOW(),t3.closed_on) > 30)
        when _status = "2" then (t3.is_closed  = 1 and DATEDIFF(NOW(),t3.closed_on) <= 30)
        end) and
        IF(_from IS NOT NULL, t3.created_on >= _from, 1) and
        IF(_to IS NOT NULL, t3.created_on < DATE_ADD(_to,interval 1 DAY), 1) and
        coalesce(t3.unit_id,'') like _unit and
        coalesce(t2.business_group_id,'') like _bgrp and
        t2.legal_entity_id = _legal and t2.country_id = _country and
        t1.user_id = _user group by t3.unit_id order by t3.unit_name;
    END IF;
    if @u_cat_id = 6 THEN
        select t3.country_id, t3.client_id, t3.legal_entity_id, t3.business_group_id,
        t3.unit_id, t3.unit_code, t3.unit_name, t3.address, t3.postal_code, t3.is_closed
        as is_active, date_format(t3.closed_on, '%d-%b-%Y') as closed_on,
        date_format(t3.created_on, '%d-%b-%Y') as check_date,
        (select concat(employee_code,'-',employee_name) from tbl_users
        where user_id = t3.created_by)as emp_code_name,
        date_format(t3.created_on, '%d/%m/%Y') as created_on,
        (select division_name from tbl_divisions where
        division_id = t3.division_id) as division_name,
        (select category_name from tbl_categories where
        category_id = t3.category_id) as category_name,
        (select group_name from tbl_client_groups where client_id = t1.client_id) as group_name,
        (select business_group_name from tbl_business_groups where business_group_id =
        t2.business_group_id) as business_group_name,
        (select legal_entity_name from tbl_legal_entities where legal_entity_id =
        t2.legal_entity_id) as legal_entity_name,
        (select concat(employee_code,'-',employee_name) from tbl_users where
        user_id = (select user_id from tbl_user_clients where
        client_id = t1.client_id)) as techno_manager,
        DATEDIFF(NOW(),t3.closed_on) as closed_days
        from
        tbl_user_legalentity as t1 inner join tbl_legal_entities as t2
        on t1.client_id = t2.client_id
        inner join tbl_units as t3 on t2.client_id = t3.client_id and
        t3.client_id = t1.client_id and
        t2.legal_entity_id = t3.legal_entity_id
        -- t2.business_group_id = t3.business_group_id
        inner join tbl_units_organizations as t4 on t4.unit_id = t3.unit_id
        and coalesce(t4.domain_id,'') like _domain and
        coalesce(t4.organisation_id,'') like _org
        where
        (case when _status = '%' then coalesce(t3.is_closed,'') like _status
        when _status = "0" then t3.is_closed = 0
        when _status = "1" then (t3.is_closed  = 1 and DATEDIFF(NOW(),t3.closed_on) > 30)
        when _status = "2" then (t3.is_closed  = 1 and DATEDIFF(NOW(),t3.closed_on) <= 30)
        end) and
        IF(_from IS NOT NULL, t3.created_on >= _from, 1) and
        IF(_to IS NOT NULL, t3.created_on < DATE_ADD(_to,interval 1 DAY), 1) and
        coalesce(t3.unit_id,'') like _unit and
        coalesce(t2.business_group_id,'') like _bgrp and
        t2.legal_entity_id = _legal and t2.country_id = _country and
        t1.user_id = _user group by t3.unit_id order by t3.unit_name;
    END IF;
    if @u_cat_id = 7 or @u_cat_id = 8 THEN
        select t3.country_id, t3.client_id, t3.legal_entity_id, t3.business_group_id,
        t3.unit_id, t3.unit_code, t3.unit_name, t3.address, t3.postal_code, t3.is_closed
        as is_active, date_format(t3.closed_on, '%d-%b-%Y') as closed_on,
        date_format(t3.created_on, '%d-%b-%Y') as check_date,
        (select concat(employee_code,'-',employee_name) from tbl_users
        where user_id = t3.created_by)as emp_code_name,
        date_format(t3.created_on, '%d/%m/%Y') as created_on,
        (select division_name from tbl_divisions where
        division_id = t3.division_id) as division_name,
        (select category_name from tbl_categories where
        category_id = t3.category_id) as category_name,
        (select group_name from tbl_client_groups where client_id = t1.client_id) as group_name,
        (select business_group_name from tbl_business_groups where business_group_id =
        t2.business_group_id) as business_group_name,
        (select legal_entity_name from tbl_legal_entities where legal_entity_id =
        t2.legal_entity_id) as legal_entity_name,
        (select concat(employee_code,'-',employee_name) from tbl_users where
        user_id = (select user_id from tbl_user_clients where
        client_id = t1.client_id)) as techno_manager,
        DATEDIFF(NOW(),t3.closed_on) as closed_days
        from
        tbl_user_units as t1 inner join tbl_legal_entities as t2
        on t2.client_id = t1.client_id
        inner join tbl_units as t3 on t3.client_id = t2.client_id and
        t3.client_id = t1.client_id and
        t3.legal_entity_id = t1.legal_entity_id
        -- t3.business_group_id = t2.business_group_id
        and t3.unit_id = t1.unit_id
        inner join tbl_units_organizations as t4 on t4.unit_id = t3.unit_id
        and coalesce(t4.domain_id,'') like _domain and
        coalesce(t4.organisation_id,'') like _org
        where
        (case when _status = '%' then coalesce(t3.is_closed,'') like _status
        when _status = "0" then t3.is_closed = 0
        when _status = "1" then (t3.is_closed  = 1 and DATEDIFF(NOW(),t3.closed_on) > 30)
        when _status = "2" then (t3.is_closed  = 1 and DATEDIFF(NOW(),t3.closed_on) <= 30)
        end) and
        IF(_from IS NOT NULL, t3.created_on >= _from, 1) and
        IF(_to IS NOT NULL, t3.created_on < DATE_ADD(_to,interval 1 DAY), 1) and
        coalesce(t3.unit_id,'') like _unit and
        coalesce(t2.business_group_id,'') like _bgrp and
        t2.legal_entity_id = _legal and t2.country_id = _country and
        t1.user_id = _user and t1.user_category_id = @u_cat_id
        group by t3.unit_id
        order by t3.unit_name;
    END IF;
    select t3.unit_id, t3.domain_id, t3.organisation_id,
    (select domain_name from tbl_domains where domain_id = t3.domain_id) as
    domain_name,
    (select organisation_name from tbl_organisation where
    organisation_id = t3.organisation_id) as organisation_name,
    (select concat(employee_code,'-',employee_name) from tbl_users where
    user_id = (select user_id from tbl_user_units where unit_id = t2.unit_id and
    domain_id = t3.domain_id and user_category_id=7)) as domain_mgr
    from
    tbl_units as t2, tbl_units_organizations as t3
    where
    t3.unit_id = t2.unit_id and
    t2.country_id = _country and
    t2.legal_entity_id = _legal and
    t2.client_id = _client;

END //

DELIMITER ;

DROP PROCEDURE IF EXISTS `sp_get_country_domain_name`;

DELIMITER //

CREATE PROCEDURE `sp_get_country_domain_name`(in
    c_id int(11), d_id int(11))
BEGIN
    select country_name from tbl_countries where country_id = c_id;
    select domain_name from tbl_domains where domain_id = d_id;

END //

DELIMITER ;

-- -------------------
-- Forgot Password
-- -------------------
DROP PROCEDURE IF EXISTS `sp_forgot_password`;

DELIMITER //

CREATE PROCEDURE `sp_forgot_password`(
    IN username_ varchar(50)
)
BEGIN
    SELECT @_user_id := user_id as user_id,
           @_user_category_id := user_category_id as user_category_id
    FROM tbl_user_login_details
    where username = username_;

    IF @_user_id != '' and @_user_category_id = 1 THEN
        select u.user_id, u.email_id, 'Compfie Admin' as employee_name
        FROM tbl_user_login_details u
        where u.user_id = @_user_id;
    ELSEIF @_user_id != '' and @_user_category_id = 2 THEN
        select u.user_id, u.email_id, 'Console Admin' as employee_name
        FROM tbl_user_login_details u
        where u.user_id = @_user_id;
    ELSEIF @_user_id != '' and @_user_category_id > 2 THEN
        select u.user_id, u.email_id, us.employee_name
        FROM tbl_user_login_details u
        inner join  tbl_users us on u.user_id = us.user_id
        where u.user_id = @_user_id;
    END IF;
END //

DELIMITER ;


DROP PROCEDURE IF EXISTS `sp_tbl_statutory_mappings_country_domain`;

DELIMITER //

CREATE PROCEDURE `sp_tbl_statutory_mappings_country_domain`(in
    m_id int(11))
BEGIN
    select country_name, domain_name, statutory_mapping from tbl_statutory_mappings as t1
    inner join tbl_countries as t2 on t1.country_id = t2.country_id
    inner join tbl_domains as t3 on t1.domain_id = t3.domain_id
    where t1.statutory_mapping_id = m_id;
END //

DELIMITER ;

-- -------------
-- get user mapped id
-- --------------
DROP PROCEDURE IF EXISTS `sp_get_user_mapped_data`;

DELIMITER //

CREATE PROCEDURE `sp_get_user_mapped_data`(in
    u_id int(11))
BEGIN
    select count(user_mapping_id) as cnt from tbl_user_mapping where parent_user_id = u_id
    OR child_user_id = u_id;

END //

DELIMITER ;

-- -------------
-- get user mapped id
-- --------------
DROP PROCEDURE IF EXISTS `sp_check_user_mapping`;

DELIMITER //

CREATE PROCEDURE `sp_check_user_mapping`(in
    country_id_ int(11), domain_id_ int(11), p_user_id_ int(11), c_user_id_ int(11), u_cat_id_ int(11))
BEGIN

    if u_cat_id_ = 6  THEN
        select count(user_id) as cnt from tbl_user_legalentity as t1, tbl_legal_entities as t2
        where t1.legal_entity_id = t2.legal_entity_id and
        t1.user_id = c_user_id_  and t2.country_id = country_id_;
    end if;

    if u_cat_id_ = 7  THEN
        select count(user_id) as cnt from tbl_user_units as t1, tbl_units as t2
        where t1.unit_id = t2.unit_id and t1.domain_id = domain_id_ and
        t1.user_id = c_user_id_  and t2.country_id = country_id_ and
        t1.client_id in (select client_id from tbl_user_clients where user_id = p_user_id_);
    end if;

    if u_cat_id_ = 8 THEN
        select count(user_id) as cnt from tbl_user_units as t1, tbl_units as t2
        where t1.unit_id = t2.unit_id and t1.domain_id = domain_id_ and
        t1.user_id = c_user_id_  and t2.country_id = country_id_;
    end if;
END //

DELIMITER ;

-- --------------------------------------------------------------------------------
-- Routine DDL
-- Export Audit Trails
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_export_audit_trails`;

DELIMITER //

CREATE PROCEDURE `sp_export_audit_trails`(
    IN _from_date varchar(10), IN _to_date varchar(10),
    IN _user_id varchar(10), IN _form_id varchar(10),
    IN _category_id int(11))
BEGIN
    if _category_id = 1 then
        SELECT t1.user_id,
        (select concat(employee_name,'-',employee_code) from tbl_users where
        user_id = t1.user_id) as employee_name,
        (Select user_category_name from tbl_user_category where
        user_category_id = t1.user_category_id) as user_category_name,
        t1.user_category_id, t1.form_id, t1.action, t1.created_on,
        (select form_name from tbl_forms where form_id = t1.form_id) as
        form_name
        FROM tbl_activity_log as t1 -- , tbl_users as t2
        WHERE
        date(t1.created_on) >= _from_date
        AND date(t1.created_on) <= _to_date
        AND COALESCE(t1.form_id,'') LIKE _form_id
        AND t1.user_id LIKE _user_id
        AND t1.user_category_id like _category_id
        ORDER BY t1.created_on DESC;
    end if;

    if _category_id >= 2 then
        SELECT t1.user_id, t1.user_category_id, t1.form_id, t1.action, t1.created_on,
        (select concat(employee_name,'-',employee_code) from tbl_users where
        user_id = t1.user_id) as employee_name,
        (Select user_category_name from tbl_user_category where
        user_category_id = t1.user_category_id) as user_category_name,
        (select form_name from tbl_forms where form_id = t1.form_id) as
        form_name
    FROM tbl_activity_log as t1 -- , tbl_users as t2, tbl_user_countries as t3
    WHERE
        date(t1.created_on) >= _from_date
        AND date(t1.created_on) <= _to_date
        AND COALESCE(t1.form_id,'') LIKE _form_id
        AND t1.user_id LIKE _user_id
        AND t1.user_category_id like _category_id
        ORDER BY t1.created_on DESC;
    end if;
END //

DELIMITER ;

-- --------------------------------------------------------------------------------
-- Routine DDL
-- To Get All user id from category id
-- --------------------------------------------------------------------------------

DROP PROCEDURE IF EXISTS `sp_get_userid_from_admin`;

DELIMITER //

CREATE PROCEDURE `sp_get_userid_from_admin`()
BEGIN
    SELECT group_concat(user_id) as userids FROM tbl_user_login_details
    WHERE user_category_id = 1;
END //

DELIMITER ;

--
-- legal entity master data
--

DROP PROCEDURE IF EXISTS `sp_get_le_master_info`;

DELIMITER //

CREATE PROCEDURE `sp_get_le_master_info`(
    in cid int(11), le_id int(11)
)
BEGIN
    IF le_id is null then
        select distinct c.country_id, c.country_name from tbl_countries c ;

        select distinct d.domain_id, d.domain_name from tbl_domains d inner join tbl_legal_entity_domains as le
        on le.domain_id = d.domain_id
        inner join tbl_legal_entities as l on l.legal_entity_id = le.legal_entity_id
        where client_id = cid;

        select distinct d.domain_id, d.country_id from tbl_domain_countries d
        inner join tbl_legal_entity_domains as le
        on le.domain_id = d.domain_id
        inner join tbl_legal_entities as l on l.legal_entity_id = le.legal_entity_id
        where client_id = cid;

        select distinct o.organisation_id, o.organisation_name, o.country_id, o.domain_id , is_active
            from tbl_organisation as o
            inner join tbl_legal_entities as le on o.country_id = le.country_id
            inner join tbl_legal_entity_domains as led
            on o.domain_id = led.domain_id where client_id = cid;

    ELSE
        select distinct c.country_id, c.country_name from tbl_countries c inner join tbl_legal_entities as le
        on le.country_id = c.country_id where  client_id = cid and le.legal_entity_id = le_id;

        select distinct d.domain_id, d.domain_name from tbl_domains d inner join tbl_legal_entity_domains as le
        on le.domain_id = d.domain_id
        inner join tbl_legal_entities as l on l.legal_entity_id = le.legal_entity_id
        where  client_id = cid and le.legal_entity_id = le_id;

        select distinct d.domain_id, d.country_id from tbl_domain_countries d
        inner join tbl_legal_entity_domains as le
        on le.domain_id = d.domain_id
        inner join tbl_legal_entities as l on l.legal_entity_id = le.legal_entity_id
        where client_id = cid and le.legal_entity_id = le_id;

        select distinct o.organisation_id, o.organisation_name, o.country_id, o.domain_id , is_active
            from tbl_organisation as o
            inner join tbl_legal_entities as le on o.country_id = le.country_id
            inner join tbl_legal_entity_domains as led on o.domain_id = led.domain_id
            where client_id = cid and le.legal_entity_id = le_id;

        select client_id, group_name, short_name, email_id, total_view_licence from
            tbl_client_groups where client_id = cid;

        select client_id, country_id, domain_id, month_from, month_to
            from tbl_client_configuration where client_id = cid;

        select client_id, legal_entity_id, legal_entity_name, country_id,
            business_group_id, contract_from, contract_to, logo,
            logo_size, file_space_limit, total_licence from
                tbl_legal_entities where client_id = cid and legal_entity_id = le_id;

        select legal_entity_id, domain_id, activation_date,
        organisation_id, count from tbl_legal_entity_domains where
            legal_entity_id = le_id;


        select b.business_group_id, b.business_group_name from tbl_business_groups as b
        inner join tbl_legal_entities as l on b.business_group_id = l.business_group_id
        where l.legal_entity_id = le_id;


    END IF ;

END //

DELIMITER ;

-- --------------------------------------------------------------------------------
-- Routine DDL
-- Note: comments before and after the routine body will not be stored by the server
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_allocate_db_environment_report_export`;

DELIMITER //

CREATE PROCEDURE `sp_allocate_db_environment_report_export`(
in cl_id varchar(10), le_id varchar(10))
BEGIN
    select t1.client_id, (select group_name from tbl_client_groups where
    client_id = t1.client_id)as group_name, t1.legal_entity_id,
    (select legal_entity_name from tbl_legal_entities where legal_entity_id =
    t1.legal_entity_id) as legal_entity_name, t1.machine_id,
    (select machine_name from tbl_application_server where machine_id =
    t1.machine_id) as machine_name, (select concat(ip,":",port) from
    tbl_application_server where machine_id = t1.machine_id) as machine_ip_port,
    t1.database_server_id, t1.client_database_server_id,
    (select database_server_name from tbl_database_server where
    database_server_id = t1.database_server_id) as db_server_name,
    (select concat(database_ip,":",database_port) from tbl_database_server where
    database_server_id = t1.database_server_id) as db_s_ip_port,
    (select database_server_name from tbl_database_server where database_server_id =
    client_database_server_id) as client_db_server_name,
    (select concat(database_ip,":",database_port) from tbl_database_server where
    database_server_id = t1.client_database_server_id) as client_db_s_ip_port,
    t1.file_server_id, (select file_server_name from tbl_file_server where
    file_server_id = t1.file_server_id) as file_server_name,
    (select concat(ip,":",port) from tbl_file_server where
    file_server_id = t1.file_server_id) as file_s_ip_port
    from
    tbl_client_database as t1 where coalesce(t1.client_id,'') like cl_id and
    coalesce(t1.legal_entity_id,'') like le_id;
END //

DELIMITER ;

-- --------------------------------------------------------------------------------
-- Routine DDL
-- Note: comments before and after the routine body will not be stored by the server
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_get_created_server_details_byid`;

DELIMITER //

CREATE PROCEDURE `sp_get_created_server_details_byid`(
in _m_id int(11), _d_s_id int(11), _le_d_s_id int(11), _f_s_id int(11), _cl_id int(11),
_le_id int(11))
BEGIN
    SELECT database_server_id, database_server_name,
        database_ip, database_port,
    (select database_username from tbl_client_database_info where
    db_owner_id = _cl_id and is_group=1) as database_username,
    (select database_password from tbl_client_database_info where
    db_owner_id = _cl_id and is_group=1) as database_password
    FROM tbl_database_server WHERE database_server_id = _d_s_id;

    SELECT database_server_id, database_server_name,
        database_ip, database_port,
    (select database_username from tbl_client_database_info where
    db_owner_id = _le_id and is_group=0) as database_username,
    (select database_password from tbl_client_database_info where
    db_owner_id = _le_id and is_group=0) as database_password
    FROM tbl_database_server WHERE database_server_id = _le_d_s_id;

    SELECT machine_id, machine_name, ip, port
    FROM tbl_application_server where machine_id = _m_id;

    SELECT file_server_id, file_server_name, ip, port
    FROM tbl_file_server WHERE file_server_id = _f_s_id;
END //

DELIMITER ;

-- --------------------------------------------------------------------------------
-- Routine DDL
-- Note: update business group name
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_business_group_update`;

DELIMITER //

CREATE PROCEDURE `sp_business_group_update`(IN bg_id INT(11), bg_name VARCHAR(100))
BEGIN
    UPDATE tbl_business_groups SET
    business_group_name = bg_name
    WHERE business_group_id = bg_id;
END //

DELIMITER ;

-- --------------------------------------------------------------------------------
-- To Get data for Client IP Details Export
-- --------------------------------------------------------------------------------

DROP PROCEDURE IF EXISTS `sp_ip_setting_details_report_export`;

DELIMITER //

CREATE PROCEDURE `sp_ip_setting_details_report_export`(
    IN c_id INT(11), IN ip_ VARCHAR(50)
)
BEGIN
    SELECT t2.form_name, t1.ips, t3.group_name FROM tbl_ip_settings t1
    inner join tbl_client_forms t2 on t1.form_id = t2.form_id
    inner join tbl_client_groups t3 on t1.client_id = t3.client_id
    where
    IF(c_id IS NOT NULL, t1.client_id = c_id, 1) and
    IF(ip_ IS NOT NULL, t1.ips = ip_, 1)
    order by t1.client_id;
END //

DELIMITER ;

-- --------------------------------------------------------------------------------
-- Routine DDL
-- Note: comments before and after the routine body will not be stored by the server
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_export_statutory_setting_report_recordset`;

DELIMITER //

CREATE PROCEDURE `sp_export_statutory_setting_report_recordset`(
in _c_id int(11), _d_id varchar(11), _bg_id varchar(11), _le_id int(11), _u_id varchar(11),
_cl_id int(11), _st_id text, _cp_id text)
BEGIN
    select t1.unit_id, (select concat(unit_code,'-',unit_name) from tbl_units where unit_id =
    t1.unit_id) as unit_name, t1.statutory_id, (select statutory_name from tbl_statutories
    where statutory_id = t1.statutory_id) as statutory_name, (select country_name from tbl_countries
    where country_id=_c_id) as country_name, (select domain_name from tbl_domains where
    domain_id = t1.domain_id) as domain_name, (select legal_entity_name from tbl_legal_entities
    where legal_entity_id = _le_id) as legal_entity_name, (select group_name from tbl_client_groups
    where client_id=_cl_id) as group_name, (select statutory_mapping from tbl_statutory_mappings
    where statutory_mapping_id = t2.statutory_mapping_id) as s_m_name,
    t2.statutory_provision, t2.compliance_task as c_task,
    t2.document_name, t1.remarks, t1.statutory_applicable_status as statutory_applicability_status,
    t1.compliance_opted_status as statutory_opted_status,
    (case when t1.updated_by is not null then (select email_id from tbl_users where
    user_id = t1.updated_by) else (select email_id from tbl_users where
    user_id = t1.submitted_by) end) as compfie_admin,
    (case when t1.updated_on is not null then DATE_FORMAT(t1.updated_on, '%d-%b-%Y')
    else DATE_FORMAT(t1.submitted_on, '%d-%b-%Y') end) as admin_update,
    (select email_id from tbl_client_users where user_id = t1.client_opted_by and
    client_id = _cl_id) as client_admin,
    DATE_FORMAT(t1.client_opted_on, '%d-%b-%Y') as client_update,
    (select tsn.statutory_nature_name from tbl_statutory_mappings as tsm, tbl_statutory_natures as tsn
    where tsn.statutory_nature_id = tsm.statutory_nature_id and
    tsm.statutory_mapping_id = t2.statutory_mapping_id) as statutory_nature_name,
    (select business_group_name from tbl_business_groups where business_group_id=
    (select business_group_id from tbl_legal_entities where legal_entity_id = _le_id))
    as business_group_name, (select division_name from tbl_divisions where division_id=
    (select division_id from tbl_units where unit_id=t1.unit_id)) as division_name
    from
    tbl_client_compliances as t1 left join tbl_compliances as t2 on
    t2.compliance_id = t1.compliance_id
    where
    (coalesce(t2.compliance_task,'') like _cp_id or
    t2.compliance_task like concat('%',_cp_id,'%')) and
    t2.country_id = _c_id and
    t1.is_approved = 5 and
    coalesce(t1.statutory_id,'%') like _st_id and
    -- coalesce(t1.compliance_id,'%') like _cp_id and
    coalesce(t1.domain_id,'%') like _d_id and
    coalesce(t1.unit_id,'%') like _u_id and
    t1.legal_entity_id = _le_id and t1.client_id = _cl_id
    group by t1.client_compliance_id;
END //

DELIMITER ;

-- --------------------------------------------------------------------------------
-- Routine DDL
-- Note: comments before and after the routine body will not be stored by the server
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_group_admin_registration_email_export_report_data`;

DELIMITER //

CREATE PROCEDURE `sp_group_admin_registration_email_export_report_data`(
in _u_id int(11), _cl_id int(11), _c_id varchar(10))
BEGIN
    SELECT @u_cat_id := user_category_id from tbl_user_login_details where user_id = _u_id;
    if @u_cat_id = 1 then
        select t2.client_id, (select group_name from tbl_client_groups where client_id =
        _cl_id) as client_name, t2.legal_entity_id, t2.legal_entity_name, count(t4.unit_id ) as
        unit_count, t2.country_id, (select country_name from tbl_countries where country_id =
        t2.country_id) as country_name, (select date_format(unit_sent_on, '%d-%b-%y %h:%i')
        from tbl_group_admin_email_notification where client_informed_id = (select max(client_informed_id)
        from tbl_group_admin_email_notification where client_id = t1.client_id and
        legal_entity_id = t2.legal_entity_id and unit_creation_informed=1)) as unit_email_date,
        (select date_format(statu_sent_on, '%d-%b-%y %h:%i') from tbl_group_admin_email_notification
        where client_informed_id = (select max(client_informed_id)
        from tbl_group_admin_email_notification where client_id = t1.client_id and
        legal_entity_id = t2.legal_entity_id and assign_statutory_informed=1)) as statutory_email_date,
        (select date_format(registration_sent_on, '%d-%b-%Y %h:%i %p') from tbl_group_admin_email_notification
        where client_informed_id = (select max(client_informed_id)
        from tbl_group_admin_email_notification where client_id = t1.client_id and
        registration_sent_by is not null)) as registration_email_date,
        (select business_group_name from tbl_business_groups where
        business_group_id = t2.business_group_id) as bg_name,
        (select date_format(registration_resend_on, '%d-%b-%y %h:%i') from tbl_group_admin_email_notification
        where client_informed_id = (select max(client_informed_id)
        from tbl_group_admin_email_notification where client_id = t1.client_id and
        registration_resend_by is not null)) as resend_email_date
        from
        tbl_user_clients as t1 inner join tbl_legal_entities as t2 on
        t2.client_id = t1.client_id left join tbl_units as t4 on
        t4.legal_entity_id = t2.legal_entity_id and
        t4.client_id = t2.client_id
        where t1.client_id = _cl_id and
        coalesce(t2.country_id, '%') like _c_id
        group by t1.client_id, t2.legal_entity_id
        order by t2.legal_entity_name;
    end if;

END //

DELIMITER ;


-- --------------------------------------------------------------------------------
-- Routine DDL
-- Note: comments before and after the routine body will not be stored by the server
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_get_client_audit_trails`;

DELIMITER //

CREATE PROCEDURE `sp_get_client_audit_trails`(
    IN _from_date varchar(10), IN _to_date varchar(10),
    IN _user_id varchar(10), IN _form_id varchar(10),
    IN _category_id varchar(11), IN _cl_id int(11),
    IN _le_id varchar(10), IN _unit_id varchar(10),
    IN _from_limit INT, IN _to_limit INT
)
BEGIN
    SELECT t1.user_id, t1.user_category_id, t1.form_id, t1.action, t1.created_on
    FROM tbl_client_activity_log as t1 -- , tbl_users as t2, tbl_user_countries as t3
    WHERE
        date(t1.created_on) >= _from_date
        AND date(t1.created_on) <= _to_date
        AND COALESCE(t1.form_id,'') LIKE _form_id
        AND COALESCE(t1.user_id, '') LIKE _user_id
        AND COALESCE(t1.user_category_id, '') like _category_id
        AND t1.client_id = _cl_id
        AND COALESCE(t1.legal_entity_id, '') like _le_id
        AND coalesce(t1.unit_id, '') like _unit_id
        -- AND t3.user_id = t2.user_id
        -- AND t2.user_id LIKE _user_id
        -- AND t2.user_category_id LIKE _category_id
        -- ORDER BY t1.user_id ASC, DATE(t1.created_on) DESC
        ORDER BY t1.created_on DESC
        limit _from_limit, _to_limit;

        SELECT count(0) as total FROM tbl_client_activity_log
        WHERE
        date(created_on) >= _from_date
        AND date(created_on) <= _to_date
        AND COALESCE(form_id,'') LIKE _form_id
        AND COALESCE(user_id, '') LIKE _user_id
        AND COALESCE(user_category_id, '') like _category_id
        AND client_id = _cl_id
        AND COALESCE(legal_entity_id, '') like _le_id
        AND coalesce(unit_id, '') like _unit_id;
END //

DELIMITER ;
-- --------------------------------------------------------------------------------
-- Routine DDL
-- Note: comments before and after the routine body will not be stored by the server
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_export_client_audit_trails`;

DELIMITER //

CREATE PROCEDURE `sp_export_client_audit_trails`(
    IN _from_date varchar(10), IN _to_date varchar(10),
    IN _user_id varchar(10), IN _form_id varchar(10),
    IN _category_id varchar(11), IN _cl_id int(11),
    IN _le_id varchar(11), IN _unit_id varchar(10)
)
BEGIN
    SELECT t1.user_id, t1.user_category_id, t1.form_id, t1.action, t1.created_on,
    (select concat(employee_name,'-',employee_code) from tbl_client_users where
    user_id = t1.user_id and client_id = t1.client_id) as employee_name,
    (Select user_category_name from tbl_client_user_category where
    user_category_id = t1.user_category_id) as user_category_name,
    (select form_name from tbl_client_forms where form_id = t1.form_id) as
    form_name, (select group_name from tbl_client_groups where client_id=_cl_id)
    as group_name,(select business_group_name from tbl_business_groups where
    business_group_id=(select business_group_id from tbl_units where unit_id=
    t1.unit_id)) as business_group_name,
    (select legal_entity_name from tbl_legal_entities where legal_entity_id=
    t1.legal_entity_id) as legal_entity_name,
    (select division_name from tbl_divisions where division_id = (select division_id
    from tbl_units where unit_id=t1.unit_id)) as division_name,
    (select category_name from tbl_categories where category_id = (select category_id
    from tbl_units where unit_id=t1.unit_id)) as category_name,
    (select concat(unit_code,'-',unit_name) from tbl_units where
    unit_id=t1.unit_id) as unit_name,
    (select unit_code from tbl_units where unit_id = (select seating_unit_id from
    tbl_client_users where client_id=_cl_id and user_id = t1.user_id)) as
    seating_id
    FROM tbl_client_activity_log as t1 -- , tbl_users as t2, tbl_user_countries as t3
    WHERE
        date(t1.created_on) >= _from_date
        AND date(t1.created_on) <= _to_date
        AND COALESCE(t1.form_id,'') LIKE _form_id
        AND COALESCE(t1.user_id, '') LIKE _user_id
        AND COALESCE(t1.user_category_id, '') like _category_id
        AND t1.client_id = _cl_id
        AND COALESCE(t1.legal_entity_id, '') like _le_id
        AND coalesce(t1.unit_id, '') like _unit_id
        -- AND t3.user_id = t2.user_id
        -- AND t2.user_id LIKE _user_id
        -- AND t2.user_category_id LIKE _category_id
        -- ORDER BY t1.user_id ASC, DATE(t1.created_on) DESC
        ORDER BY t1.created_on DESC;
END //

DELIMITER ;

-- --------------------------------------------------------------------------------
-- Routine DDL
-- Note: comments before and after the routine body will not be stored by the server
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_allocate_server_message_save`;

DELIMITER //

CREATE PROCEDURE `sp_allocate_server_message_save`(
in _u_id int(11), _link text, _client_id int(11), _le_id int(11), _le_name varchar(50), _created_on timestamp)
BEGIN
    select @grp_name := group_name from tbl_client_groups where client_id = _client_id;
    if _link = "Save" then
        set @msg_txt = concat("Server Allocated for ",@grp_name,"/",_le_name);
    else
        set @msg_txt = concat("Server Allocated for ",@grp_name, "/",_le_name," has been modified");
    end if;
    select @compfie_id := user_id from tbl_user_login_details where user_category_id = 1 limit 1;
    INSERT INTO tbl_messages
    SET
    user_category_id = 1,
    message_heading = 'Allocate Database Environment',
    message_text = @msg_txt,
    link = null, created_by = _u_id, created_on = _created_on;

    SET @msg_id := LAST_INSERT_ID();
    INSERT INTO tbl_message_users
    SET
    message_id = @msg_id,
    user_id = @compfie_id;

    INSERT INTO tbl_messages
    SET
    user_category_id = (select user_category_id from tbl_user_login_details
    where user_id = (select user_id from tbl_user_clients where client_id = _client_id)),
    message_heading = 'Allocate Database Environment',
    message_text = @msg_txt,
    link = null, created_by = _u_id, created_on = _created_on;

    SET @msg_id := LAST_INSERT_ID();
    INSERT INTO tbl_message_users
    SET
    message_id = @msg_id,
    user_id = (select user_id from tbl_user_clients where client_id = _client_id);

    if (select count(distinct user_id) as cnt from tbl_user_units where client_id = _client_id
    and legal_entity_id = _le_id and user_category_id = 7) > 0 then
        INSERT INTO tbl_messages
        SET
        user_category_id = 7,
        message_heading = 'Allocate Database Environment',
        message_text = @msg_txt,
        link = null, created_by = _u_id, created_on = _created_on;

        SET @msg_id := LAST_INSERT_ID();
        INSERT INTO tbl_message_users
        (message_id, user_id)
        select distinct @msg_id, t2.user_id
        from tbl_user_units as t2 where t2.user_id in (select distinct(user_id) from
        tbl_user_units where client_id = _client_id and
        legal_entity_id = _le_id and user_category_id = 7);
    end if;
END //

DELIMITER ;

DROP PROCEDURE IF EXISTS `sp_audit_trail_country_for_group`;

DELIMITER //

CREATE PROCEDURE `sp_audit_trail_country_for_group`(
    IN le_id int(11), IN ct_id int(11)
)
BEGIN
    INSERT INTO tbl_audit_log(action,
                            client_id,
                            legal_entity_id,
                            tbl_auto_id,
                            column_name,
                            value,
                            tbl_name)
    select 0, 0, 0, t1.country_id, 'country_name', t1.country_name, 'tbl_countries'
    from tbl_countries as t1
    inner join tbl_legal_entities as t2 on t1.country_id = t2.country_id
    where t2.legal_entity_id = le_id;

    UPDATE tbl_client_replication_status set is_new_data = 1 where
    client_id = ct_id and is_group = 1;

END //

DELIMITER ;

DROP PROCEDURE IF EXISTS `sp_tbl_units_update_division`;

DELIMITER //

CREATE PROCEDURE `sp_tbl_units_update_division`(
    in clientId int(11), bg_id int(11), le_id int(11),
    divisionName varchar(50), divId int(11), createdBy int(11),
    createdOn timestamp
    )
BEGIN
    update tbl_divisions set
    client_id = clientId, business_group_id = bg_id,
    legal_entity_id = le_id, division_name = divisionName,
    updated_by = createdBy, updated_on = createdOn
    where division_id = divId;
END //

DELIMITER ;

DROP PROCEDURE IF EXISTS `sp_tbl_units_update_category`;

DELIMITER //

CREATE PROCEDURE `sp_tbl_units_update_category`(
    in clientId int(11), bg_id int(11), le_id int(11),
    div_id varchar(50), categ_id int(11), categoryName varchar(50), createdBy int(11),
    createdOn timestamp
    )
BEGIN
    update tbl_categories set
    client_id = clientId, business_group_id = bg_id,
    legal_entity_id = le_id, division_id = div_id,
    category_name = categoryName,
    updated_by = createdBy, updated_on = createdOn
    where category_id = categ_id;
END //

DELIMITER ;


DROP PROCEDURE IF EXISTS `sp_tbl_user_isactive_disable`;

DELIMITER //

CREATE PROCEDURE `sp_tbl_user_isactive_disable`(_user_id INT(11))
BEGIN
    SELECT is_active, is_disable FROM tbl_users WHERE user_id = _user_id;
END //

DELIMITER ;

-- --------------------------------------------------------------------------------
-- To get list of domainwise agreement details export
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_domainwise_agreement_details_export`;

DELIMITER //

CREATE PROCEDURE `sp_domainwise_agreement_details_export`(
 IN countryid_ INT(11), IN clientid_ INT(11), IN businessgroupid_ INT(11),
 IN legalentityid_ INT(11), IN domainid_ INT(11), IN contractfrom_ VARCHAR(50),
 IN contractto_ VARCHAR(50), IN userid_ INT(11) )
BEGIN
    DECLARE user_category INT(11);
    SELECT user_category_id INTO user_category
    FROM tbl_user_login_details WHERE user_id = userid_;

    select t1.legal_entity_id, t3.domain_id, t1.legal_entity_name, t1.contract_from,
    t1.total_licence, t1.file_space_limit, t1.used_licence, t1.used_file_space,
    t1.contract_to, t2.group_name, t2.email_id as groupadmin_email, t4.business_group_name,
    (select sum(count) from tbl_legal_entity_domains where domain_id = t3.domain_id and legal_entity_id = t1.legal_entity_id) as domain_total_unit,
    t3.activation_date,
    (select count(o.unit_id) from tbl_units_organizations as o inner join tbl_units as u on o.unit_id = u.unit_id
    where u.legal_entity_id = t1.legal_entity_id and o.domain_id = t3.domain_id) as domain_used_unit,
    (select contact_no from tbl_client_users where user_category_id = 1 and client_id = t1.client_id and t1.legal_entity_id in (legal_entity_ids)) as groupadmin_contactno,
    (select contact_no from tbl_client_users where user_category_id = 3 and client_id = t1.client_id and t1.legal_entity_id in (legal_entity_ids)) as le_admin_contactno,
    (select email_id from tbl_client_users where user_category_id = 3 and client_id = t1.client_id and t1.legal_entity_id in (legal_entity_ids)) as le_admin_email
    from tbl_legal_entities t1
    inner join tbl_client_groups t2 on t1.client_id = t2.client_id
    inner join tbl_legal_entity_domains t3 on t1.legal_entity_id = t3.legal_entity_id
    left join tbl_business_groups t4 on t1.business_group_id = t4.business_group_id
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
    order by t1.legal_entity_name;

    select count(t1.unit_id) as count, t1.organisation_id, t2.legal_entity_id,
    (select organisation_name from tbl_organisation where organisation_id = t1.organisation_id) as organization_name
    from tbl_units_organizations t1
    inner join tbl_units t2 on t1.unit_id = t2.unit_id
    where t1.domain_id = domainid_ and t2.country_id = countryid_
    group by t2.legal_entity_id, t1.organisation_id
    order by t2.legal_entity_id, t1.organisation_id;

END //

DELIMITER ;

DROP PROCEDURE IF EXISTS `sp_forgot_password_old_pass_check`;

DELIMITER //

CREATE PROCEDURE `sp_forgot_password_old_pass_check`(_password TEXT, _user_id int(11))
BEGIN
    SELECT user_id FROM tbl_user_login_details
    WHERE password = _password and user_id =_user_id;
END //

DELIMITER ;
-- --------------------------------------------------------------------------------
-- To get list of client agreement details export
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_client_agreement_details_export`;

DELIMITER //

CREATE PROCEDURE `sp_client_agreement_details_export`(
 IN countryid_ INT(11), IN clientid_ INT(11), IN businessgroupid_ INT(11),
 IN legalentityid_ INT(11), IN domainid_ INT(11), IN contractfrom_ VARCHAR(50),
 IN contractto_ VARCHAR(50), IN userid_ INT(11))
BEGIN
    DECLARE user_category INT(11);
    SELECT user_category_id INTO user_category
    FROM tbl_user_login_details WHERE user_id = userid_;

    select t1.legal_entity_id, t3.domain_id, t1.legal_entity_name, t1.total_licence, t1.file_space_limit, t1.contract_from, t1.used_licence, t1.used_file_space,
    t1.contract_to, t2.group_name, t2.email_id as groupadmin_email, t1.is_closed, t4.business_group_name,
    (select count(distinct domain_id) from tbl_legal_entity_domains where legal_entity_id = t1.legal_entity_id and IF(domainid_ IS NOT NULL, domain_id = domainid_, 1)) as domaincount,
    (select domain_name from tbl_domains where domain_id = t3.domain_id) as domain_name,
    (select sum(count) from tbl_legal_entity_domains where domain_id = t3.domain_id and legal_entity_id = t1.legal_entity_id) as domain_total_unit,
    t3.activation_date,
    (select count(o.unit_id) from tbl_units_organizations as o inner join tbl_units as u on o.unit_id = u.unit_id
    where u.legal_entity_id = t1.legal_entity_id and o.domain_id = t3.domain_id) as domain_used_unit,
    (select contact_no from tbl_client_users where user_category_id = 1 and client_id = t1.client_id and t1.legal_entity_id in (legal_entity_ids)) as groupadmin_contactno,
    (select contact_no from tbl_client_users where user_category_id = 3 and client_id = t1.client_id and t1.legal_entity_id in (legal_entity_ids)) as le_admin_contactno,
    (select email_id from tbl_client_users where user_category_id = 3 and client_id = t1.client_id and t1.legal_entity_id in (legal_entity_ids)) as le_admin_email
    from tbl_legal_entities t1
    inner join tbl_client_groups t2 on t1.client_id = t2.client_id
    inner join tbl_legal_entity_domains t3 on t1.legal_entity_id = t3.legal_entity_id
    left join tbl_business_groups t4 on t1.business_group_id = t4.business_group_id
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
    order by t1.legal_entity_name;

    select count(t1.unit_id) as count, t1.organisation_id, t2.legal_entity_id, t1.domain_id,
    (select organisation_name from tbl_organisation where organisation_id = t1.organisation_id) as organization_name
    from tbl_units_organizations t1
    inner join tbl_units t2 on t1.unit_id = t2.unit_id
    where t2.country_id = countryid_
    group by t2.legal_entity_id, t1.domain_id, t1.organisation_id
    order by t2.legal_entity_id, t1.domain_id, t1.organisation_id;

END //

DELIMITER ;

-- --------------------------------------------------------------------------------
-- Routine DDL
-- Note: get Message nad Statutory Notification count for user
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_info_count`;

DELIMITER //

CREATE PROCEDURE `sp_info_count`(
in _u_id int(11))
BEGIN
    DECLARE user_category INT(11);
    SELECT user_category_id INTO user_category
    FROM tbl_user_login_details WHERE user_id = _u_id;

    SELECT count(1) as m_count from tbl_messages m
    INNER JOIN tbl_message_users mu ON mu.message_id = m.message_id
    where m.user_category_id = user_category and mu.user_id = _u_id and mu.read_status = 0;

    SELECT count(1) as s_count from tbl_statutory_notifications s
    INNER JOIN tbl_statutory_notifications_users su ON su.notification_id = s.notification_id
    AND su.user_id = _u_id AND su.read_status = 0;
END //

DELIMITER ;


-- --------------------------------------------------------------------------------
-- Routine DDL
-- Note: comments before and after the routine body will not be stored by the server
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_users_under_user_category`;

DELIMITER //

CREATE PROCEDURE `sp_users_under_user_category`(
in u_cg_id int(11))
BEGIN
    select user_id from tbl_user_login_details where
    user_category_id = u_cg_id;
END //

DELIMITER ;

-- --------------------------------------------------------------------------------
-- Routine DDL
-- Note: comments before and after the routine body will not be stored by the server
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_country_users_under_usercategory`;

DELIMITER //

CREATE PROCEDURE `sp_country_users_under_usercategory`(
    in u_cg_id int(11), c_id int(11))
BEGIN
    select user_id from tbl_user_countries where
    user_id in (select user_id from tbl_user_login_details
    where user_category_id = u_cg_id) and country_id = c_id;
END //

DELIMITER ;

-- --------------------------------------------------------------------------------
-- Routine DDL
-- Note: comments before and after the routine body will not be stored by the server
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_domain_users_under_usercategory`;

DELIMITER //

CREATE PROCEDURE `sp_domain_users_under_usercategory`(
    in u_cg_id int(11), d_id int(11))
BEGIN
    select distinct(user_id) from tbl_user_domains where
    user_id in (select user_id from tbl_user_login_details
    where user_category_id = u_cg_id) and domain_id = d_id;
END //

DELIMITER ;

-- --------------------------------------------------------------------------------
-- get techno_manager_id for particular client
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_get_techno_manager_id_by_client`;

DELIMITER //

CREATE PROCEDURE `sp_get_techno_manager_id_by_client`(
     cid int(11)
)
BEGIN
    select user_id from tbl_user_clients where user_category_id = 5 and client_id = cid limit 1;
END //

DELIMITER ;

-- --------------------------------------------------------------------------------
-- To Get the group name by it's id
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_group_by_id`;

DELIMITER //

CREATE PROCEDURE `sp_group_by_id`(
    IN groupid_ INT(11)
)
BEGIN
    SELECT group_name FROM tbl_client_groups
    WHERE client_id = groupid_;
END //

DELIMITER ;

-- --------------------------------------------------------------------------------
-- To Get the legal entity name by it's id
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_legal_entity_by_id`;

DELIMITER //

CREATE PROCEDURE `sp_legal_entity_by_id`(
    IN le_id_ INT(11)
)
BEGIN
    SELECT legal_entity_name FROM tbl_legal_entities
    WHERE legal_entity_id = le_id_;
END //

DELIMITER ;

-- --------------------------------------------------------------------------------
-- To Get user from tbl_user_units for particular Unit
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_user_by_unit_id`;

DELIMITER //

CREATE PROCEDURE `sp_user_by_unit_id`(
    IN cat_id_ INT(11), IN unit_id_ INT(11)
)
BEGIN
    SELECT user_id FROM tbl_user_units
    WHERE user_category_id = cat_id_ and unit_id = unit_id_;
END //

DELIMITER ;

-- -------------
-- get user transaction details count for user replacement
-- --------------
DROP PROCEDURE IF EXISTS `sp_check_user_replacement`;

DELIMITER //

CREATE PROCEDURE `sp_check_user_replacement`(
    IN cat_id INT(11), u_from_id INT(11))
BEGIN

    IF cat_id = 5 THEN
        select count(1) as cnt from tbl_user_clients where user_id = u_from_id
            and user_category_id = cat_id;
    ELSEIF cat_id = 7 THEN
        select count(1) as cnt from tbl_user_units where user_id = u_from_id
            and user_category_id = cat_id;
    END IF;

END //

DELIMITER ;

-- --------------------------------------------------

DROP PROCEDURE IF EXISTS `sp_get_country_based_users`;

DELIMITER //

CREATE PROCEDURE `sp_get_country_based_users`(
    IN geo_level_id int(11), user_cat_id int(11), proc_type tinyint(2),
    p_ids text
)
BEGIN
    if proc_type = 0 then
        select t1.user_id from tbl_users as t1
            inner join tbl_user_countries as t2 on t1.user_id = t2.user_id
            inner join tbl_geography_levels as t3 on t2.country_id = t3.country_id
            where t1.user_category_id = user_cat_id and t3.level_id = geo_level_id;
    else
        select t1.user_id from tbl_users as t1
            inner join tbl_user_countries as t2 on t1.user_id = t2.user_id
            inner join tbl_geography_levels as t3 on t2.country_id = t3.country_id
            inner join tbl_geographies as t4 on t3.level_id = t4.level_id
            where t1.user_category_id = user_cat_id and t4.geography_id = geo_level_id;
    end if;

    select t1.level_id, t2.level_name from tbl_geographies as t1
        inner join tbl_geography_levels as t2 on t1.level_id = t2.level_id
        where find_in_set(geography_id, p_ids) order by t2.level_position;

END //

DELIMITER ;


DROP PROCEDURE IF EXISTS `sp_verify_user_rights`;

DELIMITER //

CREATE PROCEDURE `sp_verify_user_rights`(
    IN userid int(11), callername text
)
BEGIN
    select @catid := user_category_id from tbl_users where user_id = userid;

    if @catid <= 2 THEN
        select t2.form_url from tbl_form_category as t1
            inner join tbl_forms as t2 on t1.form_id = t2.form_id where
            t1.user_category_id = 1
            and t2.form_url = callername;
    else
        select t3.form_url
            from tbl_users as t1
            inner join tbl_user_group_forms as t2 on t1.user_group_id = t2.user_group_id
            inner join tbl_forms as t3 on t2.form_id = t3.form_id
            where t1.user_id = userid and t3.form_url = callername;

    end if ;

END //

DELIMITER ;


-- --------------------------------------------------------------------------------
-- get techno_executive_id for particular client
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_get_techno_executive_id_by_unit`;

DELIMITER //

CREATE PROCEDURE `sp_get_techno_executive_id_by_unit`(
     unit_id_ int(11)
)
BEGIN
    select user_id from tbl_user_legalentity where legal_entity_id = (select legal_entity_id from tbl_units where unit_id = unit_id_);
END //

DELIMITER ;

-- --------------------------------------------------------------------------------
-- To Delete legal entity contract history details
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_legal_entity_contract_history_delete`;

DELIMITER //

CREATE PROCEDURE `sp_legal_entity_contract_history_delete`(
    IN le_id_ INT(11)
)
BEGIN
    DELETE FROM tbl_legal_entity_contract_history WHERE legal_entity_id = le_id_;
END //

DELIMITER ;

-- --------------------------------------------------------------------------------
-- To check delete legal entity domain transaction
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_legal_entity_domain_transaction_check`;

DELIMITER //

CREATE  PROCEDURE `sp_legal_entity_domain_transaction_check`(
clientid INT(11),
legalentityid INT(11),
domainid INT(11),
organizationid INT(11)
)
BEGIN
    SELECT COUNT(*) as count FROM tbl_units T01
    INNER JOIN tbl_units_organizations T02 ON T01.unit_id = T02.unit_id
    WHERE T01.client_id = clientid AND T01.legal_entity_id = legalentityid
    AND T02.domain_id = domainid AND T01.is_closed = 0
    AND if(organizationid IS NOT NULL,T02.organisation_id = organizationid,1);
END //

DELIMITER ;

-- --------------------------------------------------------------------------------
-- get domain_manager for particular client
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_get_domain_manager_id_by_legalentity`;

DELIMITER //

CREATE PROCEDURE `sp_get_domain_manager_id_by_legalentity`(
     cid_ int(11), le_id_ int(11)
)
BEGIN
    select distinct(user_id) from tbl_user_units where client_id = cid_ and user_category_id = 7 and
    IF(le_id_ IS NOT NULL, legal_entity_id = le_id_, 1) ;
END //

DELIMITER ;

-- --------------------------------------------------------------------------------
-- Routine DDL
-- Note: comments before and after the routine body will not be stored by the server
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_audit_trail_client_user_filters`;

DELIMITER //

CREATE PROCEDURE `sp_audit_trail_client_user_filters`()
BEGIN
    select client_id, group_name, is_active from tbl_client_groups;

    select client_id, business_group_id, legal_entity_id,
    legal_entity_name, country_id from tbl_legal_entities;

    SELECT form_id, form_name FROM tbl_client_forms where form_type_id != 3;

    SELECT t1.user_id, t1.user_category_id, t1.client_id,
    (Select user_category_name from tbl_client_user_category where
        user_category_id = t1.user_category_id) as user_category_name,
    IFNULL(concat(employee_code,' - ',employee_name),'Administrator')
    as employee_name, is_active from tbl_client_users as t1;
END //

DELIMITER ;

-- --------------------------------------------------------------------------------
-- Routine DDL
-- Note: comments before and after the routine body will not be stored by the server
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_get_le_db_server_details`;

DELIMITER //

CREATE PROCEDURE `sp_get_le_db_server_details`(
in _cl_id int(11), _le_id int(11))
BEGIN
    if _cl_id is null and _le_id is not null then
        select t1.client_database_id, t1.database_name, t1.database_username,
        t1.database_password, t3.database_ip, database_port
        from tbl_client_database_info as t1 inner join tbl_client_database as t2 on
        t2.client_database_id = t1.client_database_id inner join tbl_database_server as t3
        on t3.database_server_id = t2.database_server_id
        where t1.db_owner_id = _le_id and t1.is_group = 0;
    else
        select t1.client_database_id, t1.database_name, t1.database_username,
        t1.database_password, t3.database_ip, database_port
        from tbl_client_database_info as t1 inner join tbl_client_database as t2 on
        t2.client_database_id = t1.client_database_id inner join tbl_database_server as t3
        on t3.database_server_id = t2.client_database_server_id
        where t1.db_owner_id = _cl_id and t1.is_group = 1;
    end if;
END //

DELIMITER ;

-- --------------------------------------------------------------------------------
-- to check autodeletion records before delete
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_check_auto_deletion`;

DELIMITER //

CREATE PROCEDURE `sp_check_auto_deletion`(
    IN le_id INT(11)
)
BEGIN
    select count(1) as cnt FROM tbl_auto_deletion
    WHERE legal_entity_id=le_id;
END //

DELIMITER ;

-- --------------------------------------------------------------------------------
-- To Delete legal entity domain history details
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_legal_entity_domain_history_delete`;

DELIMITER //

CREATE PROCEDURE `sp_legal_entity_domain_history_delete`(
    IN le_id_ INT(11)
)
BEGIN
    DELETE FROM tbl_legal_entity_domains_history WHERE legal_entity_id = le_id_;
END //

DELIMITER ;

-- --------------------------------------------------------------------------------
-- To Delete client group history details
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_client_group_history_delete`;

DELIMITER //

CREATE PROCEDURE `sp_client_group_history_delete`(
    IN c_id_ INT(11)
)
BEGIN
    DELETE FROM tbl_client_groups_history WHERE client_id = c_id_ and
    (select count(1) FROM tbl_legal_entities WHERE client_id = c_id_ AND is_approved = 0) = 0;
END //

DELIMITER ;


-- --------------------------------------------------------------------------------
-- To Insert  Client Group date configuration
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_client_group_date_config_save`;

DELIMITER //

CREATE PROCEDURE `sp_client_group_date_config_save`(clientid INT(11),
countryid INT(11),
domainid INT(11),
monthfrom INT(11),
monthto INT(11),
updatedby INT(11),
updatedon timestamp)
BEGIN
    INSERT INTO tbl_client_configuration
    (client_id, country_id, domain_id, month_from, month_to, updated_by, updated_on)
    VALUES
    (clientid, countryid, domainid, monthfrom, monthto, updatedby, updatedon)
    ON DUPLICATE KEY UPDATE
    month_from = monthfrom, month_to = monthto, updated_by = updatedby, updated_on = updatedon;
END //

DELIMITER ;

-- --------------------------------------------------------------------------------
-- Routine DDL
-- Note: comments before and after the routine body will not be stored by the server
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_get_division_category_unit_count`;

DELIMITER //

CREATE PROCEDURE `sp_get_division_category_unit_count`(
in clientid int(11), in legalentityid int(11))
BEGIN
    select division_id, category_id, count(unit_id) as total_active_units from tbl_units
    where is_closed=0 and client_id = clientid and legal_entity_id=legalentityid
    group by division_id, category_id;
END //

DELIMITER ;