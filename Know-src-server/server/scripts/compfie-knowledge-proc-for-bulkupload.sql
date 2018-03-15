ALTER TABLE `compfie_knowledge_new`.`tbl_compliances`
ADD COLUMN `task_id` VARCHAR(25) NOT NULL AFTER `is_updated`,
ADD COLUMN `task_type` VARCHAR(150) NOT NULL AFTER `task_id`;


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
    t2.country_id) as country_name, t2.business_group_id
    FROM tbl_user_clients as t1 INNER JOIN tbl_legal_entities as t2 ON
    t2.client_id = t1.client_id
    WHERE t1.client_id = _client_id and t1.user_id = _user_id;
  END IF;
  IF @u_cat_id = 6 THEN
    SELECT t2.legal_entity_id, t2.legal_entity_name, t2.is_closed, t2.is_approved,
    t2.country_id, (select country_name from tbl_countries where country_id=
    t2.country_id) as country_name, t2.business_group_id
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

DROP PROCEDURE IF EXISTS `sp_bu_check_duplicate_compliance`;

DELIMITER //

CREATE PROCEDURE `sp_bu_check_duplicate_compliance`(
IN cid INT, did INT, provision VARCHAR(500),
taskname VARCHAR(150), mapping longtext
)
BEGIN

  select t1.compliance_task from tbl_compliances as t1
  inner join tbl_statutory_mappings as t2
  on t1.statutory_mapping_id = t2.statutory_mapping_id
  where t1.country_id = cid and t1.domain_id = did
  and t1.statutory_provision = provision and
  t2.statutory_mapping = mapping
  and t1.compliance_task = taskname;
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

DROP PROCEDURE IF EXISTS `sp_bu_check_duplicate_task_id`;

DELIMITER //

CREATE PROCEDURE `sp_bu_check_duplicate_task_id`(
IN cid INT, did INT, provision VARCHAR(500),
taskname VARCHAR(150), mapping longtext, taskid VARCHAR(25)
)
BEGIN

  select t1.task_id from tbl_compliances as t1
  inner join tbl_statutory_mappings as t2
  on t1.statutory_mapping_id = t2.statutory_mapping_id
  where t1.country_id = cid and t1.domain_id = did
  and t1.statutory_provision = provision and
  t2.statutory_mapping = mapping
  and t1.compliance_task = taskname
  and t1.task_id = taskid;
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
  WHERE domain_id = t2.domain_id AND organisation_id = t2.organisation_id and
  unit_id = t3.unit_id)
  AS created_units
  FROM tbl_legal_entities as t1 INNER join
  tbl_legal_entity_domains as t2 ON
  t2.legal_entity_id = t1.legal_entity_id left join
  tbl_units as t3 on t3.client_id = t1.client_id and
  t3.legal_entity_id = t1.legal_entity_id
  WHERE t1.client_id = _client_id;
END //

DELIMITER ;

DROP PROCEDURE IF EXISTS `sp_bu_client_unit_geographies`;

DELIMITER //

CREATE PROCEDURE `sp_bu_client_unit_geographies`()
BEGIN
   select geography_id,geography_name,parent_names,parent_ids,t1.is_active, t1.level_id from tbl_geographies as t1
   inner join tbl_geography_levels as t2 on t1.level_id = t2.level_id;
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
    select distinct t1.client_id, t1.group_name, t1.is_active
     from tbl_client_groups as t1
     inner join tbl_user_units as t2
     on t1.client_id = t2.client_id where t2.user_id = uid;

    -- legal entity details
    select distinct t1.client_id, t1.legal_entity_id, t1.legal_entity_name
     from tbl_legal_entities as t1
     inner join tbl_user_units as t2
     on t1.legal_entity_id = t2.legal_entity_id where t2.user_id = uid;

    -- domains
    select distinct t1.domain_name, t3.domain_id, t3.legal_entity_id
     from tbl_domains as t1
     inner join tbl_user_units as t3 on t1.domain_id = t3.domain_id
     where t3.user_id = uid;

    -- units
    SELECT t01.unit_id, t01.unit_code, t01.unit_name,
    t01.legal_entity_id, t01.client_id, group_concat(distinct t02.domain_id) as domain_ids
    FROM tbl_units as t01
    INNER JOIN tbl_units_organizations as t02 on t01.unit_id = t02.unit_id
    INNER JOIN tbl_user_units as t03 on t01.unit_id = t03.unit_id
    group by t01.unit_id,t02.unit_id;

END //

DELIMITER ;




DROP PROCEDURE IF EXISTS `sp_know_executive_info`;

DELIMITER //

CREATE PROCEDURE `sp_know_executive_info`(
IN managerid INT
)
BEGIN
  select t1.country_id, t1.domain_id, t1.child_user_id ,
    t2.employee_name, t2.employee_code
    from tbl_user_mapping as t1
    inner join tbl_users as t2 on t2.user_id = t1.child_user_id
  where t1.user_category_id = 3 and t1.parent_user_id = managerid;
END //

DELIMITER ;


-- --------------------------------------------------------------------------------
-- To get the list of download assign compliance template
-- --------------------------------------------------------------------------------

DROP PROCEDURE IF EXISTS `sp_get_assign_statutory_compliance`;

DELIMITER //

CREATE PROCEDURE `sp_get_assign_statutory_compliance`(
    IN unitid text, domainid INT(11)
)
BEGIN
    SET SESSION group_concat_max_len = 1000000;
    SELECT  DISTINCT t1.statutory_mapping_id, t1.compliance_id,

            (SELECT domain_name FROM tbl_domains WHERE domain_id = t1.domain_id) AS domain_name,
            GROUP_CONCAT(t7.organisation_name) AS organizations,
            t4.unit_code,
            t4.unit_name,
            (SELECT geography_name FROM tbl_geographies WHERE geography_id = t4.geography_id) AS location,
            SUBSTRING_INDEX(SUBSTRING_INDEX((TRIM(TRAILING '"]' FROM TRIM(LEADING '["' FROM t.statutory_mapping))),'>>',1),'>>',- 1) AS primary_legislation,
            SUBSTRING_INDEX(SUBSTRING_INDEX(CONCAT(TRIM(TRAILING '"]' FROM TRIM(LEADING '["' FROM t.statutory_mapping)),'>>'),'>>',2),'>>',- 1) AS secondary_legislation,
            t1.statutory_provision,
            -- CONCAT(t1.document_name,' - ',t1.compliance_task) AS compliance_task_name,
            t1.compliance_task AS compliance_task_name,
            t1.compliance_description,
            t6.unit_id,
            t6.domain_id,
            -- t6.compliance_id AS assigned_compid,
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
    WHERE       t1.is_active = 1
                AND t1.is_approved IN (2 , 3)
                AND FIND_IN_SET(t4.unit_id, unitid)
                AND FIND_IN_SET(t1.domain_id, domainid)
                AND t6.unit_id IS NULL
    GROUP BY    t1.statutory_mapping_id , t1.compliance_id , t4.unit_id
    ORDER BY TRIM(LEADING '[' FROM t.statutory_mapping) , t1.compliance_id , t4.unit_id;

END //

DELIMITER ;

-- --------------------------------------------------------------------------------
-- To get the list of user legal entities
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_bu_as_user_legal_entities`;

DELIMITER //

CREATE PROCEDURE `sp_bu_as_user_legal_entities`(
    IN client_id INT(11), uid INT(11)
)
BEGIN
    -- legal entity details
    select distinct t1.client_id, t1.legal_entity_id, t1.legal_entity_name
     from tbl_legal_entities as t1
     inner join tbl_user_units as t2
     on t1.legal_entity_id = t2.legal_entity_id where t2.user_id = uid;
END //

DELIMITER ;


DROP PROCEDURE IF EXISTS `sp_bu_as_user_groups`;

DELIMITER //

CREATE PROCEDURE `sp_bu_as_user_groups`(
   uid INT(11)
)
BEGIN
   -- group details
    select distinct t1.client_id, t1.group_name, t1.is_active
     from tbl_client_groups as t1
     inner join tbl_user_units as t2
     on t1.client_id = t2.client_id where t2.user_id = uid;
END //

DELIMITER ;


DROP PROCEDURE IF EXISTS `sp_bu_as_user_domains`;

DELIMITER //

CREATE PROCEDURE `sp_bu_as_user_domains`(
   uid INT(11)
)
BEGIN
   -- domains
    select distinct t1.domain_name, t1.domain_id, t1.is_active
     from tbl_domains as t1
     inner join tbl_user_units as t3 on t1.domain_id = t3.domain_id
     where t3.user_id = uid;
END //

DELIMITER ;

DROP PROCEDURE IF EXISTS `sp_bu_unit_code_and_name`;

DELIMITER //

CREATE PROCEDURE `sp_bu_unit_code_and_name`(
  IN _client_id INT(11))
BEGIN
  SELECT legal_entity_id, unit_code, unit_name, unit_id from tbl_units
  WHERE client_id = _client_id;
END //

DELIMITER ;

DROP PROCEDURE IF EXISTS `sp_bu_compliance_info`;

DELIMITER //

CREATE PROCEDURE `sp_bu_compliance_info`()
BEGIN
  SELECT compliance_id, statutory_provision, compliance_task, compliance_description from tbl_compliances;
END //

DELIMITER ;

-- --------------------------------------------------------------------------------
-- Assign Statutory bulk upload - procedures ends
-- --------------------------------------------------------------------------------

-- --------------------------------------------------------------------------------
-- To get the client id and its responsible techno managers/ executives
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_techno_users_info`;

DELIMITER //

CREATE PROCEDURE `sp_techno_users_info`(
  IN _UserType INT(11), _UserId INT(11))
BEGIN
  IF (_Usertype = 5) THEN
    SELECT t1.client_id as group_id, t2.user_id, t3.employee_code, t3.employee_name
    FROM
      tbl_user_clients AS t1 inner join tbl_user_legalentity as t2 on
      t2.client_id = t1.client_id
      inner join tbl_users as t3 on t3.user_id = t2.user_id
    where
      t1.user_id = _UserId;
  END IF;
  IF (_Usertype = 6) THEN
    select t1.client_id as group_id, t2.user_id, t3.employee_code, t3.employee_name
    from
      tbl_user_legalentity as t1 inner join tbl_user_clients as t2
      on t2.client_id = t1.client_id
      inner join tbl_users as t3 on t3.user_id = t2.user_id
    where
      t1.user_id = _UserId;
  END IF;
END //

DELIMITER ;

DROP PROCEDURE IF EXISTS `sp_usermapping_statutory_unit_details`;;
DELIMITER //
CREATE PROCEDURE `sp_usermapping_statutory_unit_details`(IN `userCatgId` int(11), IN `userId` int)
BEGIN
     if(userCatgId = 8)then
        select tu.unit_id, concat(tu.unit_code,' - ',tu.unit_name) as unit_name, tu.client_id,
        tu.business_group_id, tu.legal_entity_id,
        tu.country_id, td.division_id, td.division_name, tc.category_id,
        tc.category_name, tuu.domain_id
        from
        tbl_user_units as tuu inner join tbl_units as tu
        on tu.unit_id = tuu.unit_id
        left join tbl_divisions as td on
        td.division_id = tu.division_id
        left join tbl_categories as tc on tc.category_id = tu.category_id
        where
        tuu.user_id = userId and tuu.user_category_id = userCatgId
        group by tu.unit_id;
    end if;

    if(userCatgId = 1)then
        select tu.unit_id, concat(tu.unit_code,' - ',tu.unit_name) as unit_name,tu.client_id,
        tu.business_group_id, tu.legal_entity_id,
        tu.country_id, tu.division_id,
        td.division_name, tc.category_id,
        tc.category_name, tuu.domain_id
        from
        tbl_units as tu
        left join tbl_user_units as tuu on tu.unit_id = tuu.unit_id
        left join tbl_divisions as td on
        td.division_id = tu.division_id
        left join tbl_categories as tc on tc.category_id = tu.category_id
        group by tu.unit_id;
    end if;
END//
DELIMITER ;


DROP PROCEDURE IF EXISTS `sp_domain_executive_info`;

DELIMITER //

CREATE PROCEDURE `sp_domain_executive_info`(
IN user_id INT
)
BEGIN
  select distinct t1.child_user_id, t2.employee_name, t2.employee_code
    from tbl_user_mapping as t1
    inner join tbl_users as t2 on t2.user_id = t1.child_user_id
  where t1.user_category_id = 7 and t1.parent_user_id = user_id;
END //

DELIMITER ;


DROP PROCEDURE IF EXISTS `sp_bu_level_one_statutories`;

DELIMITER //

CREATE PROCEDURE `sp_bu_level_one_statutories`()
BEGIN
   select t1.statutory_id, t1.statutory_name from tbl_statutories as t1
   where t1.parent_ids = '';
END //

DELIMITER ;

DROP PROCEDURE IF EXISTS `sp_bu_get_compliance_id_by_name`;

DELIMITER //

CREATE PROCEDURE `sp_bu_get_compliance_id_by_name`(
IN c_task text, c_desc text)
BEGIN
   select compliance_id from tbl_compliances
   where compliance_task = c_task and compliance_description = c_desc;
END //

DELIMITER ;

-- --------------------------------------------------------------------------------
-- Client unit bulk upload - procedures starts
-- --------------------------------------------------------------------------------

-- --------------------------------------------------------------------------------
-- To get the list of client groups under the user
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_client_groups_for_client_unit_bulk_upload`;

DELIMITER //

CREATE PROCEDURE `sp_client_groups_for_client_unit_bulk_upload`(
    IN userId INT(11))
BEGIN
    SELECT @u_cat_id := user_category_id from tbl_user_login_details where user_id = userId;
    IF @u_cat_id = 5 THEN
        SELECT t1.client_id, t1.group_name,t1.is_active, t1.is_approved
        FROM tbl_client_groups t1
        inner join tbl_user_clients t2 on t1.client_id = t2.client_id and t2.user_id = userId
        GROUP BY t1.group_name ORDER BY t1.group_name;
    END IF;
    IF @u_cat_id = 6 THEN
        SELECT t1.client_id, t1.group_name,t1.is_active, t1.is_approved
        FROM tbl_client_groups t1
        inner join tbl_user_legalentity t2 on t1.client_id = t2.client_id and t2.user_id = userId
        GROUP BY t1.group_name ORDER BY t1.group_name;
    END IF;
END //

DELIMITER ;

DROP PROCEDURE IF EXISTS `sp_bu_organization_all`;

DELIMITER //

CREATE PROCEDURE `sp_bu_organization_all`()
BEGIN
   select organisation_id, organisation_name, is_active from tbl_organisation;
END //

DELIMITER ;

-- --------------------------------------------------------------------------------
-- Client unit bulk upload - procedures ends
-- --------------------------------------------------------------------------------


