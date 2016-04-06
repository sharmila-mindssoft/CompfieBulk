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
        statutory_notification_id,
        user_id, read_status)
    SELECT @notificationid, t1.user_id, 0
    FROM tbl_user_units t1 where t1.unit_id = @unitid;
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

DROP TRIGGER IF EXISTS `after_tbl_client_compliances_update`;
DELIMITER //
CREATE TRIGGER `after_tbl_client_compliances_update` AFTER UPDATE ON `tbl_client_compliances`
FOR EACH ROW BEGIN
	CALL procedure_to_update_version("compliance");
END
//
DELIMITER ;
