-- --------------------------------------------------------------------------------
-- Returns Coutries that has been mapped with domain
-- --------------------------------------------------------------------------------
DELIMITER $$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_country_mapped_list`()
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

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_domain_mapped_list`()
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

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_validitydays_settings_list`()
BEGIN
	SELECT validity_days_id, country_id, domain_id, days
	FROM tbl_validity_days_settings;
END

-- --------------------------------------------------------------------------------
-- Returns all possible country domain combinations which are mapped during 
-- Statutory level creation
-- --------------------------------------------------------------------------------
DELIMITER $$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_statutorylevels_mappings`()
BEGIN
	SELECT country_id, domain_id 
	FROM tbl_statutory_levels;
END

-- --------------------------------------------------------------------------------
-- To Save Validity date settings
-- --------------------------------------------------------------------------------
DELIMITER $$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_validitydays_settings_save`(
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