
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
   select geography_id,geography_name,parent_names,parent_ids, is_active from tbl_geographies
   where country_id = cId;
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
   select tq.statutory_id, t1.statutory_name,
   t1.parent_ids, t1.parent_names from tbl_statutories as t1
   inner join tbl_statutory_levels as t2 on t1.level_id = t2.level_id
   where t2.country_id = cId and t2.domain_id = dId;
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
