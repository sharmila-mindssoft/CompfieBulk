DROP PROCEDURE IF EXISTS `sp_bu_organization`;
DELIMITER //
CREATE PROCEDURE `sp_bu_organization`(
IN cId INT, dId INT
)
BEGIN
   SELECT organisation_id, organisation_name, is_active
   FROM tbl_organisation
   WHERE country_id = cId AND domain_id = dId;
END //
DELIMITER ;


DROP PROCEDURE IF EXISTS `sp_bu_statutory_nature`;
DELIMITER //
CREATE PROCEDURE `sp_bu_statutory_nature`(
IN cId INT
)
BEGIN
   SELECT statutory_nature_id, statutory_nature_name, is_active
   FROM tbl_statutory_natures
   WHERE country_id = cId;
END //
DELIMITER ;


DROP PROCEDURE IF EXISTS `sp_bu_geographies`;
DELIMITER //
CREATE PROCEDURE `sp_bu_geographies`(
IN cId INT
)
BEGIN
   SELECT geography_id,geography_name,parent_names,parent_ids,t1.is_active
   FROM tbl_geographies AS t1
   INNER JOIN tbl_geography_levels AS t2 ON t1.level_id = t2.level_id
   WHERE t2.country_id = cId;
END //
DELIMITER ;


DROP PROCEDURE IF EXISTS `sp_bu_compliance_frequency`;
DELIMITER //
CREATE PROCEDURE `sp_bu_compliance_frequency`()
BEGIN
   SELECT frequency_id, frequency FROM tbl_compliance_frequency;
END //
DELIMITER ;

DROP PROCEDURE IF EXISTS `sp_bu_compliance_repeat_type`;
DELIMITER //
CREATE PROCEDURE `sp_bu_compliance_repeat_type`()
BEGIN
   SELECT repeat_type_id, repeat_type FROM tbl_compliance_repeat_type;
END //
DELIMITER ;


DROP PROCEDURE IF EXISTS `sp_bu_compliance_duration_type`;
DELIMITER //
CREATE PROCEDURE `sp_bu_compliance_duration_type`()
BEGIN
   SELECT duration_type_id, duration_type FROM tbl_compliance_duration_type;
END //
DELIMITER ;


DROP PROCEDURE IF EXISTS `sp_bu_statutories`;
DELIMITER //
CREATE PROCEDURE `sp_bu_statutories`(
IN cId INT, dId INT
)
BEGIN
   SELECT t1.statutory_id, t1.statutory_name,
   t1.parent_ids, t1.parent_names FROM tbl_statutories AS t1
   INNER JOIN tbl_statutory_levels AS t2 ON t1.level_id = t2.level_id
   WHERE t2.country_id = cId AND t2.domain_id = dId;
END //
DELIMITER ;


DROP PROCEDURE IF EXISTS `sp_bu_statutory_level`;
DELIMITER //
CREATE PROCEDURE `sp_bu_statutory_level`(
IN cId INT, dId INT
)
BEGIN
   SELECT max(t.level_position) AS statu_level
   FROM tbl_statutory_levels AS t
   WHERE country_id = cId AND domain_id =dId;
END //
DELIMITER ;


DROP PROCEDURE IF EXISTS `sp_bu_get_levelposition`;
DELIMITER //
CREATE PROCEDURE `sp_bu_get_levelposition`(
IN cId INT, dId INT
)
BEGIN
   SELECT t.level_id, t.level_position  AS statu_level
   FROM tbl_statutory_levels AS t
   WHERE country_id = cId AND domain_id =dId;
END //
DELIMITER ;


-- --------------------------------------------------------------------------------
-- To get legal entities under a client for client units bulk upload
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_bu_legal_entities`;
DELIMITER //
CREATE PROCEDURE `sp_bu_legal_entities`(IN _client_id INT(11), _user_id INT(11))
BEGIN
  SELECT @u_cat_id := user_category_id
  FROM tbl_user_login_details
  WHERE user_id = _user_id;

  IF @u_cat_id = 5 THEN
    SELECT t2.legal_entity_id, t2.legal_entity_name, t2.is_closed, t2.is_approved,
    t2.country_id,
    (SELECT country_name FROM tbl_countries WHERE country_id=t2.country_id)
    AS country_name, t2.business_group_id,
    DATEDIFF(t2.contract_to,curdate()) AS le_contract_days,
    t3.user_id
    FROM tbl_user_clients AS t1 INNER JOIN tbl_legal_entities AS t2 ON
    t2.client_id = t1.client_id LEFT JOIN tbl_user_legalentity AS t3 ON
    t3.legal_entity_id = t2.legal_entity_id
    WHERE t1.client_id = _client_id AND t1.user_id = _user_id;
  END IF;
  IF @u_cat_id = 6 THEN
    SELECT t2.legal_entity_id, t2.legal_entity_name, t2.is_closed, t2.is_approved,
    t2.country_id, (SELECT country_name FROM tbl_countries WHERE country_id=
    t2.country_id) AS country_name, t2.business_group_id,
    DATEDIFF(t2.contract_to,curdate()) AS le_contract_days, t1.user_id
    FROM tbl_user_legalentity AS t1 INNER JOIN tbl_legal_entities AS t2 ON
    t2.client_id = t1.client_id AND t2.legal_entity_id = t1.legal_entity_id
    WHERE t1.client_id = _client_id AND t1.user_id = _user_id;
  END IF;
END //
DELIMITER ;

DROP PROCEDURE IF EXISTS `sp_user_details`;
DELIMITER //
CREATE PROCEDURE `sp_user_details`(
IN uId INT
)
BEGIN
   SELECT user_id, @_user_cat_id := t1.user_category_id AS user_category_id,
   employee_name, employee_code, email_id, contact_no,
   mobile_no, user_group_id, address, designation, is_active,
   user_category_name FROM tbl_users AS t1 INNER JOIN
   tbl_user_category AS t2 ON t1.user_category_id = t2.user_category_id
   WHERE t1.user_id = uId;

   SELECT country_id FROM tbl_user_countries WHERE user_id = uId;

   SELECT country_id, domain_id FROM tbl_user_domains WHERE user_id = uId;

   SELECT country_id, domain_id, child_user_id FROM tbl_user_mapping WHERE parent_user_id = uId;

   SELECT country_id, domain_id, parent_user_id FROM tbl_user_mapping WHERE child_user_id = uId;

   SELECT client_id FROM tbl_user_clients WHERE user_id = uId;

   SELECT client_id, legal_entity_id FROM tbl_user_legalentity WHERE user_id = uId;

   SELECT legal_entity_id, unit_id FROM tbl_user_units WHERE user_id = uId
   AND user_category_id = @_user_cat_id;
END //
DELIMITER ;


DROP PROCEDURE IF EXISTS `sp_bu_check_duplicate_compliance`;
DELIMITER //
CREATE PROCEDURE `sp_bu_check_duplicate_compliance`(
IN cid INT, did INT, provision VARCHAR(500),
taskname VARCHAR(150), mapping longtext
)
BEGIN
  SELECT t1.compliance_task FROM tbl_compliances AS t1
  INNER JOIN tbl_statutory_mappings AS t2
  ON t1.statutory_mapping_id = t2.statutory_mapping_id
  WHERE t1.country_id = cid AND t1.domain_id = did
  AND t1.statutory_provision = provision and
  t2.statutory_mapping = mapping
  AND t1.compliance_task = taskname;
END //
DELIMITER ;


DROP PROCEDURE IF EXISTS `sp_bu_get_matching_compliance`;
DELIMITER //
CREATE PROCEDURE `sp_bu_get_matching_compliance`(
IN cid INT, did INT
)
BEGIN
  SELECT t1.country_id, t1.domain_id, t2.statutory_mapping,
         t1.statutory_provision, t1.compliance_task

  FROM tbl_compliances AS t1
  INNER JOIN tbl_statutory_mappings AS t2
  ON t1.statutory_mapping_id = t2.statutory_mapping_id
  WHERE t1.country_id = cid AND t1.domain_id = did;
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
  FROM tbl_categories
  WHERE client_id = _client_id;
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
  FROM tbl_divisions
  WHERE client_id = _client_id;
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
  FROM tbl_geography_levels
  WHERE country_id IN (SELECT
  country_id FROM tbl_user_countries WHERE user_id =
  _user_id);
END //
DELIMITER ;


DROP PROCEDURE IF EXISTS `sp_bu_check_duplicate_task_id`;
DELIMITER //
CREATE PROCEDURE `sp_bu_check_duplicate_task_id`(
IN cid INT, did INT, provision VARCHAR(500),
taskname VARCHAR(150), mapping longtext, taskid VARCHAR(25)
)
BEGIN
  SELECT t1.task_id FROM tbl_compliances AS t1
  INNER JOIN tbl_statutory_mappings AS t2
  ON t1.statutory_mapping_id = t2.statutory_mapping_id
  WHERE t1.country_id = cid AND t1.domain_id = did
  AND t1.statutory_provision = provision and
  t2.statutory_mapping = mapping
  AND t1.compliance_task = taskname
  AND t1.task_id = taskid;
END //
DELIMITER ;


DROP PROCEDURE IF EXISTS `sp_bu_get_matching_taskids`;
DELIMITER //
CREATE PROCEDURE `sp_bu_get_matching_taskids`(
IN cid INT, did INT
)
BEGIN
  SELECT t1.country_id, t1.domain_id, t1.statutory_provision,
  t1.compliance_task, t2.statutory_mapping, t1.task_id
  FROM tbl_compliances AS t1
  INNER JOIN tbl_statutory_mappings AS t2
  ON t1.statutory_mapping_id = t2.statutory_mapping_id
  WHERE t1.country_id = cid AND t1.domain_id = did;
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
  is_active FROM tbl_geographies;
END //
DELIMITER ;


-- ----------------------------------------------------------------------------
-- To get the unit codes under a client group
-- ----------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_bu_unit_code`;
DELIMITER //
CREATE PROCEDURE `sp_bu_unit_code`(
  IN _client_id INT(11))
BEGIN
  SELECT legal_entity_id, unit_code
  FROM tbl_units
  WHERE client_id = _client_id;
END //
DELIMITER ;


-- ----------------------------------------------------------------------------
-- To get the domains AND organization under client group with its alloted
-- unit count
-- ----------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_bu_domains_organization_unit_count`;
DELIMITER //
CREATE PROCEDURE `sp_bu_domains_organization_unit_count`(
  IN _client_id INT(11))
BEGIN
  SELECT t2.legal_entity_id, t2.domain_id, t2.organisation_id,
  (SELECT domain_name FROM tbl_domains WHERE domain_id = t2.domain_id)
  AS domain_name, (SELECT is_active FROM tbl_domains WHERE domain_id = t2.domain_id)
  AS domain_is_active, (SELECT organisation_name FROM tbl_organisation
  WHERE organisation_id = t2.organisation_id) AS organization_name,
  (SELECT is_active FROM tbl_organisation
  WHERE organisation_id = t2.organisation_id) AS organization_is_active,
  t2.count AS total_unit_count,count(t4.unit_id) AS created_units
  FROM tbl_legal_entities AS t1 INNER JOIN
  tbl_legal_entity_domains AS t2 ON
  t2.legal_entity_id = t1.legal_entity_id LEFT JOIN
  tbl_units AS t3 ON t3.client_id = t1.client_id AND
  t3.legal_entity_id = t1.legal_entity_id LEFT JOIN
  tbl_units_organizations AS t4 ON t4.domain_id = t2.domain_id
  AND t4.organisation_id = t2.organisation_id AND
  t4.unit_id = t3.unit_id
  WHERE t1.client_id = _client_id
  GROUP BY t1.legal_entity_id, t2.domain_id, t2.organisation_id, t2.count;
END //
DELIMITER ;


DROP PROCEDURE IF EXISTS `sp_bu_client_unit_geographies`;
DELIMITER //
CREATE PROCEDURE `sp_bu_client_unit_geographies`()
BEGIN
   SELECT geography_id,geography_name,parent_names,parent_ids,t1.is_active, t1.level_id
   FROM tbl_geographies AS t1
   INNER JOIN tbl_geography_levels AS t2 ON t1.level_id = t2.level_id;
END //
DELIMITER ;


-- --------------------------------------------------------------------------------
-- Assign Compliance bulk upload - procedures starts
-- --------------------------------------------------------------------------------

-- --------------------------------------------------------------------------------
-- To get the list of client info
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_client_info`;
DELIMITER //
CREATE PROCEDURE `sp_client_info`(
    IN uid INT(11)
)
BEGIN
    -- group details
    SELECT DISTINCT t1.client_id, t1.group_name, t1.is_active
    FROM tbl_client_groups AS t1
    INNER JOIN tbl_user_units AS t2
    ON t1.client_id = t2.client_id WHERE t2.user_id = uid;

    -- legal entity details
    SELECT DISTINCT t1.client_id, t1.legal_entity_id, t1.legal_entity_name
    FROM tbl_legal_entities AS t1
    INNER JOIN tbl_user_units AS t2
    ON t1.legal_entity_id = t2.legal_entity_id WHERE t2.user_id = uid AND t1.is_closed = 0;

    -- domains
    SELECT DISTINCT t1.domain_name, t3.domain_id, t3.legal_entity_id
    FROM tbl_domains AS t1
    INNER JOIN tbl_user_units AS t3 ON t1.domain_id = t3.domain_id
    INNER JOIN tbl_user_domains AS t4 ON t1.domain_id = t4.domain_id
    WHERE t3.user_id = uid AND t4.user_id = uid AND t1.is_active = 1;

    -- units
    SELECT t01.unit_id, t01.unit_code, t01.unit_name,
    t01.legal_entity_id, t01.client_id, group_concat(DISTINCT t02.domain_id) AS domain_ids
    FROM tbl_units AS t01
    INNER JOIN tbl_units_organizations AS t02 ON t01.unit_id = t02.unit_id
    INNER JOIN tbl_user_units AS t03 ON t01.unit_id = t03.unit_id
    WHERE t03.user_id = uid AND t01.is_closed = 0 AND t01.is_approved = 1
    GROUP BY t01.unit_id,t02.unit_id,t01.unit_code,
    t01.unit_name,t01.legal_entity_id, t01.client_id;

    -- check assigned units
    SELECT DISTINCT domain_id, unit_id FROM tbl_client_compliances
    WHERE is_approved < 5;
END//
DELIMITER ;


DROP PROCEDURE IF EXISTS `sp_know_executive_info`;
DELIMITER //
CREATE PROCEDURE `sp_know_executive_info`(
IN managerid INT
)
BEGIN
  SELECT t1.country_id, t1.domain_id, t1.child_user_id ,
    t2.employee_name, t2.employee_code
    FROM tbl_user_mapping AS t1
    INNER JOIN tbl_users AS t2 ON t2.user_id = t1.child_user_id
  WHERE t1.user_category_id = 3 AND t1.parent_user_id = managerid;
END //
DELIMITER ;


-- --------------------------------------------------------------------------------
-- To get the list of download assign compliance template
-- --------------------------------------------------------------------------------

DROP PROCEDURE IF EXISTS `sp_get_assign_statutory_compliance`;
DELIMITER //
CREATE PROCEDURE `sp_get_assign_statutory_compliance`(
    IN unitid text, domainid text
)
BEGIN
    SET SESSION group_concat_max_len = 1000000;

    -- mapped statu names
    SELECT t2.statutory_name, t1.statutory_id, IFNULL(t2.parent_ids, 0) AS parent_ids,
    t2.parent_names, t1.statutory_mapping_id
    FROM tbl_mapped_statutories AS t1
    INNER JOIN tbl_statutories AS t2 ON t1.statutory_id = t2.statutory_id
    INNER JOIN tbl_statutory_mappings AS t3 ON t1.statutory_mapping_id = t3.statutory_mapping_id
    INNER JOIN tbl_mapped_locations AS t4 ON t1.statutory_mapping_id = t4.statutory_mapping_id
    INNER JOIN (SELECT a.geography_id,b.parent_ids,a.unit_id FROM tbl_units a
      INNER JOIN tbl_geographies b ON a.geography_id = b.geography_id
      WHERE find_in_set(a.unit_id, unitid)) t7 ON
      (t4.geography_id = t7.geography_id OR find_in_set(t4.geography_id,t7.parent_ids))
    ORDER BY TRIM(LEADING '[' FROM t3.statutory_mapping);

    -- get compliances
    SELECT  DISTINCT t1.statutory_mapping_id, t1.compliance_id,
      (SELECT domain_name FROM tbl_domains WHERE domain_id = t1.domain_id) AS domain_name,
      (SELECT country_name FROM tbl_countries WHERE country_id = t1.country_id) AS country_name,
      GROUP_CONCAT(t7.organisation_name) AS organizations,
      t4.unit_code,
      t4.unit_name,
      (SELECT geography_name FROM tbl_geographies WHERE geography_id = t4.geography_id) AS location,
      SUBSTRING_INDEX(SUBSTRING_INDEX((TRIM(TRAILING '"]' FROM TRIM(LEADING '["' FROM t.statutory_mapping))),'>>',1),'>>',- 1) AS primary_legislation,
      SUBSTRING_INDEX(SUBSTRING_INDEX(CONCAT(TRIM(TRAILING '"]' FROM TRIM(LEADING '["' FROM t.statutory_mapping)),'>>'),'>>',2),'>>',- 1) AS secondary_legislation,
      t1.statutory_provision,
      t1.compliance_task AS compliance_task_name,
      t1.compliance_description,
      t6.unit_id,
      t6.domain_id,
      t4.unit_id AS c_unit_id,
      t1.domain_id
    FROM    tbl_compliances AS t1
      INNER JOIN
          tbl_statutory_mappings AS t ON t1.statutory_mapping_id = t.statutory_mapping_id
      INNER JOIN
          tbl_mapped_industries AS t2 ON t1.statutory_mapping_id = t2.statutory_mapping_id
      INNER JOIN
          tbl_mapped_locations AS t3 ON t1.statutory_mapping_id = t3.statutory_mapping_id
      INNER JOIN
          tbl_organisation AS t7 ON t2.organisation_id = t7.organisation_id
      INNER JOIN
          tbl_units AS t4 ON t4.country_id = t1.country_id
      INNER JOIN
          tbl_units_organizations AS t5 ON t4.unit_id = t5.unit_id AND t5.domain_id = t1.domain_id AND t5.organisation_id = t2.organisation_id
      LEFT JOIN
          tbl_client_compliances t6 ON t1.compliance_id = t6.compliance_id AND
          t4.unit_id = t6.unit_id AND t.domain_id = t6.domain_id
      INNER JOIN
          (SELECT a.geography_id, b.parent_ids, a.unit_id FROM tbl_units a
          INNER JOIN tbl_geographies b ON a.geography_id = b.geography_id
          WHERE
          FIND_IN_SET(a.unit_id, unitid)) t7 ON t7.unit_id = t4.unit_id
          AND t7.geography_id = t3.geography_id
          AND (t4.geography_id = t7.geography_id
          OR FIND_IN_SET(t4.geography_id, t7.parent_ids))
    WHERE t1.is_active = 1
      AND t1.is_approved IN (2 , 3)
      AND FIND_IN_SET(t4.unit_id, unitid)
      AND FIND_IN_SET(t1.domain_id, domainid)
      AND t6.unit_id IS NULL
    GROUP BY   t1.statutory_mapping_id , t1.compliance_id , t4.unit_id,
        t1.domain_id, t4.unit_code, t4.unit_name,
        t4.geography_id, t.statutory_mapping,
        t1.statutory_provision,
        t1.compliance_task ,
        t1.compliance_description,
        t6.unit_id,
        t6.domain_id,
        t4.unit_id,
        t1.domain_id
    ORDER BY TRIM(LEADING '[' FROM t.statutory_mapping) , t1.compliance_id , t4.unit_id;
END//

DELIMITER ;


-- --------------------------------------------------------------------------------
-- To get the list of user legal entities
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_bu_as_user_legal_entities`;
DELIMITER //
CREATE PROCEDURE `sp_bu_as_user_legal_entities`(
    IN uid INT(11), client_id_ INT(11), country_id_ INT(11)
)
BEGIN
    -- legal entity details
    select distinct t1.client_id, t1.legal_entity_id, t1.legal_entity_name, t1.is_closed,
    t1.is_approved
    from tbl_legal_entities as t1
    inner join tbl_user_units as t2
    on t1.legal_entity_id = t2.legal_entity_id where t2.user_id = uid
    AND t1.country_id = country_id_ AND t1.client_id = client_id_;
END //
DELIMITER ;


DROP PROCEDURE IF EXISTS `sp_bu_as_user_groups`;
DELIMITER //
CREATE PROCEDURE `sp_bu_as_user_groups`(
   uid INT(11)
)
BEGIN
   -- group details
    SELECT DISTINCT t1.client_id, t1.group_name, t1.is_active
     FROM tbl_client_groups AS t1
     INNER JOIN tbl_user_units AS t2
     ON t1.client_id = t2.client_id WHERE t2.user_id = uid;
END //
DELIMITER ;


DROP PROCEDURE IF EXISTS `sp_bu_as_user_domains`;
DELIMITER //
CREATE PROCEDURE `sp_bu_as_user_domains`(
   uid INT(11)
)
BEGIN
   -- domains
    SELECT DISTINCT t1.domain_name, t1.domain_id, t1.is_active
     FROM tbl_domains AS t1
     INNER JOIN tbl_user_units AS t3 ON t1.domain_id = t3.domain_id
     WHERE t3.user_id = uid;
END //
DELIMITER ;


DROP PROCEDURE IF EXISTS `sp_bu_unit_code_and_name`;
DELIMITER //
CREATE PROCEDURE `sp_bu_unit_code_and_name`(
  IN legal_entity_id_ INT(11)
)
BEGIN
  SELECT legal_entity_id, unit_code, unit_name, unit_id, is_closed from
  tbl_units WHERE legal_entity_id = legal_entity_id_;
END //
DELIMITER ;


DROP PROCEDURE IF EXISTS `sp_bu_compliance_info`;
DELIMITER //
CREATE PROCEDURE `sp_bu_compliance_info`()
BEGIN
  SELECT compliance_id, statutory_provision, compliance_task, compliance_description,
  is_active FROM tbl_compliances;
END //
DELIMITER ;


-- --------------------------------------------------------------------------------
-- Assign Statutory bulk upload - procedures ends
-- --------------------------------------------------------------------------------

-- --------------------------------------------------------------------------------
-- To get the client id AND its responsible techno managers/ executives
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_techno_users_info`;
DELIMITER //
CREATE PROCEDURE `sp_techno_users_info`(
  IN _UserType INT(11), _UserId INT(11))
BEGIN
  IF (_Usertype = 5) THEN
    SELECT t1.client_id AS group_id, t2.user_id, t3.employee_code, t3.employee_name
    FROM
      tbl_user_clients AS t1 INNER JOIN tbl_user_legalentity AS t2 ON
      t2.client_id = t1.client_id
      INNER JOIN tbl_users AS t3 ON t3.user_id = t2.user_id
    WHERE
      t1.user_id = _UserId;
  END IF;
  IF (_Usertype = 6) THEN
    SELECT t1.client_id AS group_id, t2.user_id, t3.employee_code, t3.employee_name
    FROM
      tbl_user_legalentity AS t1 INNER JOIN tbl_user_clients AS t2
      ON t2.client_id = t1.client_id
      INNER JOIN tbl_users AS t3 ON t3.user_id = t2.user_id
    WHERE
      t1.user_id = _UserId;
  END IF;
END //
DELIMITER ;


DROP PROCEDURE IF EXISTS `sp_domain_executive_info`;
DELIMITER //
CREATE PROCEDURE `sp_domain_executive_info`(
IN user_id INT
)
BEGIN
  SELECT DISTINCT t2.user_id, t2.employee_name, t2.employee_code
    FROM tbl_user_mapping AS t1
    INNER JOIN tbl_users AS t2 ON t2.user_id = t1.child_user_id
  WHERE t1.user_category_id = 7 AND t1.parent_user_id = user_id;
END //
DELIMITER ;


DROP PROCEDURE IF EXISTS `sp_bu_level_one_statutories`;
DELIMITER //
CREATE PROCEDURE `sp_bu_level_one_statutories`()
BEGIN
   SELECT t1.statutory_id, t1.statutory_name FROM tbl_statutories AS t1
   WHERE t1.parent_ids = '';
END //
DELIMITER ;


DROP PROCEDURE IF EXISTS `sp_bu_get_compliance_id_by_name`;
DELIMITER //
CREATE PROCEDURE `sp_bu_get_compliance_id_by_name`(
  IN c_task TEXT, c_desc TEXT, s_provision TEXT, country_id_ INT(11),
  domain_id_ INT(11), p_legislation INT(11), s_legislation TEXT
)
BEGIN
  SELECT distinct compliance_id from tbl_compliances as t1
  INNER JOIN tbl_mapped_statutories as t3 on t1.statutory_mapping_id = t3.statutory_mapping_id
  INNER JOIN tbl_statutories as t4 on t3.statutory_id = t4.statutory_id
  WHERE t1.domain_id = domain_id_ and t1.country_id = country_id_ and
  if(s_legislation != '',find_in_set(s_legislation,concat(t4.parent_ids,t4.statutory_id)),(t4.statutory_id = p_legislation and t4.parent_ids = '')) and
  statutory_provision = s_provision and
  compliance_task = c_task and
  compliance_description = c_desc;
END //
DELIMITER ;

-- --------------------------------------------------------------------------------
-- Client unit bulk upload - procedures starts
-- --------------------------------------------------------------------------------

-- --------------------------------------------------------------------------------
-- To get the list of client groups under the user
-- --------------------------------------------------------------------------------
-- --------------------------------------------------------------------------------
-- To get the list of client groups under the user
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_client_groups_for_client_unit_bulk_upload`;
DELIMITER //
CREATE PROCEDURE `sp_client_groups_for_client_unit_bulk_upload`(
    IN userId INT(11))
BEGIN
    SELECT @u_cat_id := user_category_id FROM tbl_user_login_details WHERE user_id = userId;
    IF @u_cat_id = 5 THEN
        SELECT t1.client_id, t1.group_name,t1.is_active, t1.is_approved
        FROM tbl_client_groups t1
        INNER JOIN tbl_user_clients t2 ON t1.client_id = t2.client_id AND t2.user_id = userId
        GROUP BY t1.group_name, t1.client_id, t1.is_active, t1.is_approved ORDER BY t1.group_name;
    END IF;
    IF @u_cat_id = 6 THEN
        SELECT t1.client_id, t1.group_name,t1.is_active, t1.is_approved
        FROM tbl_client_groups t1
        INNER JOIN tbl_user_legalentity t2 ON t1.client_id = t2.client_id AND t2.user_id = userId
        GROUP BY t1.group_name, t1.client_id, t1.is_active, t1.is_approved ORDER BY t1.group_name;

    END IF;
END//
DELIMITER ;


DROP PROCEDURE IF EXISTS `sp_bu_organization_all`;
DELIMITER //
CREATE PROCEDURE `sp_bu_organization_all`(
IN country_id_ INT(11)
)
BEGIN
   SELECT t1.domain_id, t1.organisation_id, t1.organisation_name, t1.is_active,
   (SELECT domain_name FROM tbl_domains WHERE domain_id = t1.domain_id) AS domain_name
   FROM tbl_organisation t1
   WHERE t1.country_id = country_id_;
END //
DELIMITER ;


-- --------------------------------------------------------------------------------
-- Client unit bulk upload - procedures ends
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_bu_chils_level_statutories`;
DELIMITER //
CREATE PROCEDURE `sp_bu_chils_level_statutories`()
BEGIN
   SELECT t1.statutory_id, t1.statutory_name FROM tbl_statutories AS t1
   WHERE t1.parent_ids != '';
END //
DELIMITER ;


DROP PROCEDURE IF EXISTS `sp_bu_check_duplicate_compliance_for_unit`;
DELIMITER //
CREATE PROCEDURE `sp_bu_check_duplicate_compliance_for_unit`(
IN domain_ INT, unit_ INT, compid_ INT
)
BEGIN
  SELECT compliance_id
  FROM tbl_client_compliances
  WHERE domain_id = domain_
  AND unit_id = unit_
  AND compliance_id = compid_;
END //
DELIMITER ;


DROP PROCEDURE IF EXISTS `sp_bu_user_by_unit_ids`;
DELIMITER //
CREATE PROCEDURE `sp_bu_user_by_unit_ids`(
    IN cat_id_ INT(11), IN unit_ids_ TEXT
)
BEGIN
    SELECT DISTINCT user_id FROM tbl_user_units
    WHERE user_category_id = cat_id_ AND FIND_IN_SET(unit_id, unit_ids_);
END //
DELIMITER ;


DROP PROCEDURE IF EXISTS `sp_bu_domain_executive_units`;
DELIMITER //
CREATE PROCEDURE `sp_bu_domain_executive_units`(
    IN uid_ INT(11), unit_ids_ TEXT
)
BEGIN
    SELECT DISTINCT t03.unit_id
    FROM tbl_user_units AS t03
    WHERE t03.user_id = uid_ AND FIND_IN_SET(t03.unit_id, unit_ids_);
END //
DELIMITER ;


DROP PROCEDURE IF EXISTS `sp_bu_get_mapped_knowledge_executives`;
DELIMITER //
CREATE PROCEDURE `sp_bu_get_mapped_knowledge_executives`(
    IN manager_id INT(11), IN countryid INT(11), IN domainid INT(11)
)
BEGIN
    SELECT DISTINCT child_user_id
    FROM  tbl_user_mapping
    INNER JOIN tbl_users ON user_id = child_user_id AND is_active = 1
    AND is_disable = 0 AND country_id = countryid AND domain_id = domainid
    WHERE parent_user_id = manager_id ;
END //
DELIMITER ;


DROP PROCEDURE IF EXISTS `sp_bu_get_legal_entity_id_by_name`;
DELIMITER //
CREATE PROCEDURE `sp_bu_get_legal_entity_id_by_name`(
    IN client_id_ INT(11), country_id_ INT(11), legal_entity_name_ text
)
BEGIN
    SELECT legal_entity_id FROM tbl_legal_entities
    WHERE legal_entity_name = legal_entity_name_ AND client_id = client_id_
    AND country_id = country_id_;
END //
DELIMITER ;


DROP PROCEDURE IF EXISTS `sp_bu_get_country_by_legal_entity_id`;
DELIMITER //
CREATE PROCEDURE `sp_bu_get_country_by_legal_entity_id`(
    IN legal_entity_id_ INT(11)
)
BEGIN
    SELECT t1.country_id, t2.country_name
    FROM tbl_legal_entities t1
    INNER JOIN tbl_countries t2 ON t1.country_id = t2.country_id
    WHERE t1.legal_entity_id = legal_entity_id_;
END //
DELIMITER ;

-- Remove procedure
DROP PROCEDURE IF EXISTS `sp_usermapping_statutory_unit_details`;


DROP PROCEDURE IF EXISTS `sp_bu_is_valid_le`;
DELIMITER //
CREATE PROCEDURE `sp_bu_is_valid_le`(
    IN le_name VARCHAR(50), client_group_name VARCHAR(50)
)
BEGIN
  SELECT count(legal_entity_id) AS cnt FROM tbl_legal_entities
  WHERE legal_entity_name = le_name and client_id = (
    SELECT client_id from tbl_client_groups where group_name = client_group_name
  );
END //
DELIMITER ;

DROP PROCEDURE IF EXISTS `sp_bu_as_user_countries`;
DELIMITER //
CREATE PROCEDURE `sp_bu_as_user_countries`(
   uid INT(11), le_id INT(11)
)
BEGIN
  SELECT t1.country_id, t1.country_name, t1.is_active
  FROM tbl_countries t1
  INNER JOIN tbl_user_countries t2 ON t1.country_id = t2.country_id
  INNER JOIN tbl_legal_entities t3 ON t1.country_id = t3.country_id
  WHERE t2.user_id = uid AND t3.legal_entity_id = le_id;
END //
DELIMITER ;


DROP PROCEDURE IF EXISTS `sp_bu_get_group_id_by_name`;
DELIMITER //
CREATE PROCEDURE `sp_bu_get_group_id_by_name`(
    IN group_name_ text
)
BEGIN
    SELECT client_id FROM tbl_client_groups
    WHERE group_name = group_name_;
END //
DELIMITER ;

DROP PROCEDURE IF EXISTS `sp_bu_get_country_id_by_name`;
DELIMITER //
CREATE PROCEDURE `sp_bu_get_country_id_by_name`(
    IN country_name_ text
)
BEGIN
    SELECT country_id FROM tbl_countries
    WHERE country_name = country_name_;
END //
DELIMITER ;

DROP PROCEDURE IF EXISTS `sp_bu_countries`;
DELIMITER //

CREATE PROCEDURE `sp_bu_countries`(
IN _user_id INT(11))
BEGIN
  SELECT t1.country_id, t2.country_name, t2.is_active
  FROM tbl_user_countries as t1
  INNER JOIN tbl_countries as t2
  ON t2.country_id = t1.country_id
  WHERE t1.user_id = _user_id;
END //

DELIMITER ;

DROP PROCEDURE IF EXISTS `sp_bu_unit_location`;
DELIMITER //
CREATE PROCEDURE `sp_bu_unit_location`(
IN le_id INT(11)
)
BEGIN
   SELECT t1.unit_code, t2.geography_id, t2.geography_name, t2.is_active
   FROM tbl_units AS t1
   INNER JOIN tbl_geographies AS t2 ON t1.geography_id = t2.geography_id
   WHERE t1.legal_entity_id = le_id;
END //
DELIMITER ;

ALTER TABLE `tbl_compliances`
ADD COLUMN `task_id` VARCHAR(25) NOT NULL AFTER `is_updated`,
ADD COLUMN `task_type` VARCHAR(150) NOT NULL AFTER `task_id`;
