
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
