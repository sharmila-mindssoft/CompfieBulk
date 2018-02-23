
DROP PROCEDURE IF EXISTS `sp_bu_organization`;

DELIMITER //

CREATE PROCEDURE `sp_bu_organization`(
IN cId INT, dId INT
)
BEGIN
   select organisation_id, organisation_name, is_active from tbl_organisation
   where country_id = cId and domain_id = dId;
END //

DELIMITER ;


DROP PROCEDURE IF EXISTS `sp_bu_statutory_nature`;

DELIMITER //

CREATE PROCEDURE `sp_bu_statutory_nature`(
IN cId INT
)
BEGIN
   select statutory_nature_id, statutory_nature_name, is_active from tbl_statutory_natures
   where country_id = cId;
END //

DELIMITER ;


DROP PROCEDURE IF EXISTS `sp_bu_geographies`;

DELIMITER //

CREATE PROCEDURE `sp_bu_geographies`(
IN cId INT
)
BEGIN
   select geography_id,geography_name,parent_names,parent_ids,t1.is_active from tbl_geographies as t1
   inner join tbl_geography_levels as t2 on t1.level_id = t2.level_id
   where t2.country_id = cId;
END //

DELIMITER ;

DROP PROCEDURE IF EXISTS `sp_bu_compliance_frequency`;

DELIMITER //

CREATE PROCEDURE `sp_bu_compliance_frequency`(
)
BEGIN
   select frequency_id, frequency from tbl_compliance_frequency;

END //

DELIMITER ;

DROP PROCEDURE IF EXISTS `sp_bu_compliance_repeat_type`;

DELIMITER //

CREATE PROCEDURE `sp_bu_compliance_repeat_type`(
)
BEGIN
   select repeat_type_id, repeat_type from tbl_compliance_repeat_type;
END //

DELIMITER ;

DROP PROCEDURE IF EXISTS `sp_bu_compliance_duration_type`;

DELIMITER //

CREATE PROCEDURE `sp_bu_compliance_duration_type`(
)
BEGIN
   select duration_type_id, duration_type from tbl_compliance_duration_type;
END //

DELIMITER ;


DROP PROCEDURE IF EXISTS `sp_bu_statutories`;

DELIMITER //

CREATE PROCEDURE `sp_bu_statutories`(
IN cId INT, dId INT
)
BEGIN
   select t1.statutory_id, t1.statutory_name,
   t1.parent_ids, t1.parent_names from tbl_statutories as t1
   inner join tbl_statutory_levels as t2 on t1.level_id = t2.level_id
   where t2.country_id = cId and t2.domain_id = dId;
END //

DELIMITER ;

-- --------------------------------------------------------------------------------
-- To get legal entities under a client for client units bulk upload
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_bu_legal_entities`;

DELIMITER //

CREATE PROCEDURE `sp_bu_legal_entities`(IN _client_id INT(11), _user_id INT(11))
BEGIN
  SELECT @u_cat_id := user_category_id from tbl_user_login_details where user_id = _user_id;
    IF @u_cat_id = 5 THEN
    SELECT t2.legal_entity_id, t2.legal_entity_name, t2.is_closed, t2.is_approved,
    t2.country_id, (select country_name from tbl_countries where country_id=
    t2.country_id) as country_name
    FROM tbl_user_clients as t1 INNER JOIN tbl_legal_entities as t2 ON
    t2.client_id = t1.client_id
    WHERE t1.client_id = _client_id and t1.user_id = _user_id;
  END IF;
  IF @u_cat_id = 6 THEN
    SELECT t2.legal_entity_id, t2.legal_entity_name, t2.is_closed, t2.is_approved,
    t2.country_id, (select country_name from tbl_countries where country_id=
    t2.country_id) as country_name
    FROM tbl_user_legalentity as t1 INNER JOIN tbl_legal_entities as t2 ON
    t2.client_id = t1.client_id
    WHERE t1.client_id = _client_id and t1.user_id = _user_id;
  END IF;
END //

DELIMITER ;

DROP PROCEDURE IF EXISTS `sp_user_details`;

DELIMITER //

CREATE PROCEDURE `sp_user_details`(
IN uId INT
)
BEGIN
   select user_id, @_user_cat_id := t1.user_category_id as user_category_id,
   employee_name, employee_code, email_id, contact_no,
   mobile_no, user_group_id, address, designation, is_active,
   user_category_name from tbl_users as t1 inner join
   tbl_user_category as t2 on t1.user_category_id = t2.user_category_id
   where t1.user_id = uId;

   select country_id from tbl_user_countries where user_id = uId;

   select country_id, domain_id from tbl_user_domains where user_id = uId;

   select country_id, domain_id, child_user_id from tbl_user_mapping where parent_user_id = uId;

   select country_id, domain_id, parent_user_id from tbl_user_mapping where child_user_id = uId;

   select client_id from tbl_user_clients where user_id = uId;

   select client_id, legal_entity_id from tbl_user_legalentity where user_id = uId;

   select legal_entity_id, unit_id from tbl_user_units where user_id = uId
   and user_category_id = @_user_cat_id;


END //

DELIMITER ;

-- --------------------------------------------------------------------------------
-- To get the categories under a client
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_bu_categories`;

DELIMITER //

CREATE PROCEDURE `sp_bu_categories`(
  IN _client_id INT(11))
BEGIN
  SELECT legal_entity_id, division_id, category_id, category_name
  FROM tbl_categories WHERE client_id = _client_id;
END //

DELIMITER ;

-- --------------------------------------------------------------------------------
-- To get the divisions under a client
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_bu_divisions`;

DELIMITER //

CREATE PROCEDURE `sp_bu_divisions`(
  IN _client_id INT(11))
BEGIN
  SELECT legal_entity_id, division_id, division_name
  FROM tbl_divisions WHERE client_id = _client_id;
END //

DELIMITER ;

-- --------------------------------------------------------------------------------
-- To get the geography levels under a country of the user
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_bu_geography_levels`;

DELIMITER //

CREATE PROCEDURE `sp_bu_geography_levels`(
  IN _user_id INT(11))
BEGIN
  SELECT level_id, country_id, level_name, is_active
  FROM tbl_geography_levels where country_id IN (SELECT
  country_id from tbl_user_countries where user_id =
  _user_id);
END //

DELIMITER ;

-- --------------------------------------------------------------------------------
-- To get the geographies under a level
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_bu_unit_location`;

DELIMITER //

CREATE PROCEDURE `sp_bu_unit_location`()
BEGIN
  SELECT geography_id, level_id, parent_names,
  is_active from tbl_geographies;
END //

DELIMITER ;

-- --------------------------------------------------------------------------------
-- To get the unit codes under a client group
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_bu_unit_code`;

DELIMITER //

CREATE PROCEDURE `sp_bu_unit_code`(
  IN _client_id INT(11))
BEGIN
  SELECT legal_entity_id, unit_code from tbl_units
  WHERE client_id = _client_id;
END //

DELIMITER ;

-- -----------------------------------------------------------------------------------------------
-- To get the domains and organization under client group with its alloted unit count
-- -----------------------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_bu_domains_organization_unit_count`;

DELIMITER //

CREATE PROCEDURE `sp_bu_domains_organization_unit_count`(
  IN _client_id INT(11))
BEGIN
  SELECT t2.legal_entity_id, t2.domain_id, t2.organisation_id,
  (SELECT domain_name FROM tbl_domains WHERE domain_id = t2.domain_id)
  AS domain_name, (SELECT is_active FROM tbl_domains WHERE domain_id = t2.domain_id)
  AS domain_is_active, (SELECT organisation_name from tbl_organisation
  WHERE organisation_id = t2.organisation_id) AS organization_name,
  (SELECT is_active from tbl_organisation
  WHERE organisation_id = t2.organisation_id) AS organization_is_active,
  t2.count AS total_unit_count, (SELECT COUNT(*) FROM tbl_units_organizations
  WHERE domain_id = t2.domain_id AND organisation_id = t2.organisation_id)
  AS created_units
  FROM tbl_legal_entities as t1 INNER join
  tbl_legal_entity_domains as t2 ON
  t2.legal_entity_id = t1.legal_entity_id
  WHERE t1.client_id = _client_id;
END //

DELIMITER ;

DROP PROCEDURE IF EXISTS `sp_bu_client_unit_geographies`;

DELIMITER //

CREATE PROCEDURE `sp_bu_client_unit_geographies`()
BEGIN
   select geography_id,geography_name,parent_names,parent_ids,t1.is_active from tbl_geographies as t1
   inner join tbl_geography_levels as t2 on t1.level_id = t2.level_id;
END //

DELIMITER ;