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
		SELECT distinct t1.domain_id, t1.domain_name, t1.is_active FROM tbl_domains t1 INNER JOIN tbl_user_domains t2  ON t1.domain_id = t2.domain_id WHERE t2.user_id = user_id;	
	ELSE
		SELECT distinct t1.domain_id, t1.domain_name, t1.is_active FROM tbl_domains t1;
	END IF;
END //
DELIMITER;
	
