-- --------------------------------------------------------------------------------
-- Returns Coutries that has been mapped with domain
-- --------------------------------------------------------------------------------
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
DELIMITER $$

CREATE PROCEDURE `sp_statutorylevels_mappings`()
BEGIN
	SELECT country_id, domain_id
	FROM tbl_statutory_levels;
END

-- --------------------------------------------------------------------------------
-- To Save Validity date settings
-- --------------------------------------------------------------------------------
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

CREATE PROCEDURE `sp_industry_master_checkduplicateindustry`(
in industryid int(11), industryname varchar(50))
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

CREATE PROCEDURE `sp_industry_master_getindusdtrybyid`(industryid int(11))
BEGIN
	SELECT industry_name FROM tbl_industries WHERE
    industry_id = industryid;
END


-- --------------------------------------------------------------------------------
-- To get industry details from its master
-- --------------------------------------------------------------------------------

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

CREATE PROCEDURE `sp_industry_master_saveactivitylog`(
activityLogId int(11), userId int(11), formId int(11),
action varchar(500), createdOn timestamp)
BEGIN
	INSERT INTO tbl_activity_log
    (activity_log_id, user_id, form_id, action, created_on)
    VALUES
	(activityLogId, userId, formId, action, createdOn);
END

-- --------------------------------------------------------------------------------
-- To save industry master details
-- --------------------------------------------------------------------------------

CREATE PROCEDURE `sp_industry_master_saveindustry`(
countryid int(11), domainid int(11), industryname varchar(50),
createdby int(11), createdon timestamp)
BEGIN
	INSERT INTO tbl_industries
    (industry_name, country_id, domain_id, created_by, created_on)
    VALUES
	(industryname, countryid, domainid, createdby, createdon);
END

-- --------------------------------------------------------------------------------
-- To update industry master details
-- --------------------------------------------------------------------------------

CREATE PROCEDURE `sp_industry_master_updateindustry`(
	industryId int(11), industryName varchar(50), countryId int(11),
    domainId int(11), updatedBy int(11)
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

CREATE PROCEDURE `sp_industry_master_updatestatus`(
	industryId int(11), isActive tinyint(4), updatedBy int(11))
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

CREATE PROCEDURE `sp_statutory_nature_checkduplicatenature`(
	statutoryNatureName varchar(50),
    statutoryNatureId int(11)
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

CREATE PROCEDURE `sp_statutory_nature_updatestatutorynature`(
IN statutoryNatureId int(11), statutoryNatureName varchAR(50),
countryId int(11), updatedBy int(11))
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

CREATE PROCEDURE `sp_statutory_nature_updatestatutorynaturestatus`(
statutoryNatureId int(11), updatedBy int(11), isActive tinyint(4))
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

CREATE PROCEDURE `sp_statutory_natures_getnaturebyid`(
	statutoryNatureId int(11))
BEGIN
	SELECT statutory_nature_name FROM tbl_statutory_natures
    WHERE statutory_nature_id = statutoryNatureId;

END

-- --------------------------------------------------------------------------------
-- To save statutory nature details
-- --------------------------------------------------------------------------------

CREATE PROCEDURE `sp_statutorynature_savestatutorynature`(
statutoryNatureName varchar(50), countryId int(11),
createdBy int(11), createdOn timestamp)
BEGIN
	INSERT INTO tbl_statutory_natures
    (statutory_nature_name, country_id, created_by, created_on)
    VALUES
    (statutoryNatureName, countryId, createdBy, createdOn);
END

-- --------------------------------------------------------------------------------
-- get domains data based on user domain settings
-- --------------------------------------------------------------------------------

DROP PROCEDURE sp_tbl_domains_for_user;
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

DROP PROCEDURE sp_tbl_forms_getadminforms;
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
