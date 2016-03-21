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