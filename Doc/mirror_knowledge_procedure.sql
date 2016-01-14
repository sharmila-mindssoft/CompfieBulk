-- procedures
DELIMITER //
CREATE PROCEDURE sp_validate_session_token
(IN session_token VARCHAR(50))
BEGIN
	SELECT t1.user_id FROM tbl_user_sessions t1 WHERE t1.session_token = session_token;
END //
DELIMITER;

DELIMITER //
CREATE PROCEDURE sp_get_domains_for_user
(IN user_id int)
BEGIN
	IF (user_id > 0) THEN:
		SELECT distinct t1.domain_id, t1.domain_name, 
		t1.is_active FROM tbl_domains t1 
		INNER JOIN tbl_user_domains t2  ON 
		t1.domain_id = t2.domain_id WHERE t2.user_id = user_id;	
	ELSE
		SELECT distinct t1.domain_id, t1.domain_name, t1.is_active FROM tbl_domains t1;
	END IF;
END //
DELIMITER;

CREATE PROCEDURE  `sp_get_statutory_mapping_to_assign` ( IN  `p_domain_id` INT( 11 ) , IN  `p_industry_id` INT( 11 ) , IN  `p_geography_id` INT( 11 ) ) NOT DETERMINISTIC READS SQL DATA SQL SECURITY DEFINER SELECT t1.statutory_mapping_id, t4.statutory_id
FROM tbl_statutory_mappings t1
INNER JOIN tbl_statutory_industry t2 ON t1.statutory_mapping_id = t2.statutory_mapping_id
INNER JOIN tbl_statutory_geographies t3 ON t1.statutory_mapping_id = t3.statutory_mapping_id
INNER JOIN tbl_statutory_statutories t4 ON t1.statutory_mapping_id = t4.statutory_mapping_id
WHERE t1.domain_id = p_domain_id
AND t2.industry_id = p_industry_id
AND t3.geography_id
IN (
SELECT g.geography_id
FROM tbl_geographies g
WHERE g.geography_id = p_geography_id
OR g.parent_ids LIKE CONCAT(  '%', p_geography_id,  ',%' )
);

sp_get_units_with_location
SELECT t1.unit_id, t1.unit_code, t1.unit_name, t1.division_id,
    t1.legal_entity_id, t1.business_group_id,
    t1.client_id , t1.geography_id, t1.industry_id, t1.domain_ids,
    t3.parent_ids
FROM tbl_units t1
INNER JOIN tbl_user_clients t2 ON t1.client_id = t2.client_id
INNER JOIN tbl_geographies t3 ON t1.geography_id = t3.geography_id
WHERE t2.user_id = 2


