--
-- Triggers `tbl_statutory_notifications_units`
--

DROP TRIGGER IF EXISTS `after_tbl_statutory_notifications_units_insert`;
DELIMITER //
CREATE TRIGGER `after_tbl_statutory_notifications_units_insert` AFTER INSERT ON `tbl_statutory_notifications_units`
 FOR EACH ROW BEGIN
    SET @notificationid = NEW.statutory_notification_id;
    SET @unitid = NEW.unit_id;

    INSERT INTO tbl_statutory_notification_status (
    	statutory_notification_id, user_id, read_status)
    	SELECT NEW.statutory_notification_id, t1.user_id, 0
     	FROM tbl_user_units t1 where t1.unit_id = NEW.unit_id;
    INSERT INTO tbl_statutory_notification_status (
    	statutory_notification_id,
    	user_id, read_status)
        SELECT NEW.statutory_notification_id, t1.admin_id, 0 FROM
        tbl_admin t1 where t1.admin_id != 0;
END
//
DELIMITER ;

DROP TRIGGER IF EXISTS `after_tbl_units_insert`;
DELIMITER //
CREATE TRIGGER `after_tbl_units_insert` AFTER INSERT ON `tbl_units`
FOR EACH ROW BEGIN
	CALL procedure_to_update_version("unit");
END
//
DELIMITER ;

DROP TRIGGER IF EXISTS `after_tbl_units_update`;
DELIMITER //
CREATE TRIGGER `after_tbl_units_update` AFTER UPDATE ON `tbl_units`
FOR EACH ROW BEGIN
	CALL procedure_to_update_version("unit");
END
//
DELIMITER ;

DROP TRIGGER IF EXISTS `after_tbl_users_update`;
DELIMITER //
CREATE TRIGGER `after_tbl_users_update` AFTER UPDATE ON `tbl_users`
FOR EACH ROW BEGIN
	CALL procedure_to_update_version("user");
END
//
DELIMITER ;

DROP TRIGGER IF EXISTS `after_tbl_users_insert`;
DELIMITER //
CREATE TRIGGER `after_tbl_users_insert` AFTER INSERT ON `tbl_users`
FOR EACH ROW BEGIN
	CALL procedure_to_update_version("user");
END
//
DELIMITER ;

DROP TRIGGER IF EXISTS `after_tbl_compliance_history_insert`;
DELIMITER //
CREATE TRIGGER `after_tbl_compliance_history_insert` AFTER INSERT ON `tbl_compliance_history`
FOR EACH ROW BEGIN
	CALL procedure_to_update_version("history");
END
//
DELIMITER ;

DROP TRIGGER IF EXISTS `after_tbl_compliance_history_update`;
DELIMITER //
CREATE TRIGGER `after_tbl_compliance_history_update` AFTER UPDATE ON `tbl_compliance_history`
FOR EACH ROW BEGIN
	CALL procedure_to_update_version("history");
END
//
DELIMITER ;


DROP TRIGGER IF EXISTS `after_tbl_client_compliances_insert`;
DELIMITER //
CREATE TRIGGER `after_tbl_client_compliances_insert` AFTER INSERT ON `tbl_client_compliances`
FOR EACH ROW BEGIN
	CALL procedure_to_update_version("compliance");
END
//
DELIMITER ;

DROP TRIGGER IF EXISTS `after_tbl_client_compliances_update`;
DELIMITER //
CREATE TRIGGER `after_tbl_client_compliances_update` AFTER UPDATE ON `tbl_client_compliances`
FOR EACH ROW BEGIN
	CALL procedure_to_update_version("compliance");
END
//
DELIMITER ;

DELIMITER //

CREATE PROCEDURE `procedure_to_update_version`(IN update_type VARCHAR(100))
BEGIN
	SET SQL_SAFE_UPDATES=0;
	case
	when update_type = 'unit' then
		SET @count = (SELECT unit_details_version+1 FROM tbl_mobile_sync_versions );
		update tbl_mobile_sync_versions set unit_details_version = @count;
	when update_type = 'user' then
		SET @count = (SELECT user_details_version+1 FROM tbl_mobile_sync_versions );
		update tbl_mobile_sync_versions set user_details_version = @count;
	when update_type = 'compliance' then
		SET @count = (SELECT compliance_applicability_version+1 FROM tbl_mobile_sync_versions );
		update tbl_mobile_sync_versions set compliance_applicability_version = @count;
	when update_type = 'history' then
		SET @count = (SELECT compliance_history_version+1 FROM tbl_mobile_sync_versions );
		update tbl_mobile_sync_versions set compliance_history_version = @count;
    end case;
    SET SQL_SAFE_UPDATES=1;
END
//
DELIMITER ;
