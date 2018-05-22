--
-- Triggers `tbl_statutory_notifications_units`
--

DROP TRIGGER IF EXISTS `tbl_statutory_notifications_insert`;
DELIMITER //
CREATE TRIGGER `tbl_statutory_notifications_insert` AFTER INSERT ON `tbl_statutory_notifications`
 FOR EACH ROW BEGIN
    SET @notificationid = NEW.notification_id;
    INSERT INTO tbl_statutory_notifications_users (
    	notification_id, user_id, is_read)
    	select distinct @notificationid, t1.user_id, 0 from tbl_users as t1
        left join tbl_user_domains as t3 on t1.user_id = t3.user_id
        left join tbl_legal_entities as t4 on t3.legal_entity_id = t4.legal_entity_id
        left join tbl_compliances as t2
        on t3.domain_id = t2.domain_id and t4.country_id = t2.country_id and
        t2.compliance_id = new.compliance_id;
END
//
DELIMITER ;


DROP TRIGGER IF EXISTS `after_tbl_legal_entity_insert`;
DELIMITER //
CREATE TRIGGER `after_tbl_legal_entity_insert` AFTER INSERT ON `tbl_legal_entities`
 FOR EACH ROW BEGIN
    INSERT INTO tbl_le_replication_status(legal_entity_id) values(new.legal_entity_id);
    INSERT INTO tbl_reminder_settings(client_id, legal_entity_id)
    select client_id, new.legal_entity_id from tbl_client_groups ;
END
//
DELIMITER ;

DROP TRIGGER IF EXISTS `after_tbl_user_legal_entities_insert`;
DELIMITER //
CREATE TRIGGER `after_tbl_user_legal_entities_insert` AFTER INSERT ON `tbl_user_legal_entities`
 FOR EACH ROW BEGIN
    INSERT INTO tbl_le_user_replication_status(legal_entity_id, user_id, s_action)
    values(new.legal_entity_id, new.user_id, 1) on duplicate key update s_action = 1;
    UPDATE tbl_le_replication_status set user_data = 1
    where legal_entity_id = new.legal_entity_id;
END
//
DELIMITER ;

DROP TRIGGER IF EXISTS `after_tbl_user_legal_entities_delete`;
DELIMITER //
CREATE TRIGGER `after_tbl_user_legal_entities_delete` AFTER DELETE ON `tbl_user_legal_entities`
 FOR EACH ROW BEGIN
 if old.user_id is not null then
 INSERT INTO tbl_le_user_replication_status(legal_entity_id, user_id, s_action)
 values(old.legal_entity_id, old.user_id, 3) on duplicate key update s_action = 3;
 UPDATE tbl_le_replication_status set user_data = 1 where legal_entity_id = old.legal_entity_id;
 end if;
 END
 //
 DELIMITER ;


DROP TRIGGER IF EXISTS `after_tbl_reminder_settings_update`;
DELIMITER //

CREATE TRIGGER `after_tbl_reminder_settings_update` AFTER UPDATE ON `tbl_reminder_settings`
 FOR EACH ROW BEGIN
 insert into tbl_le_settings_replication_status(legal_entity_id, s_action)
 values(new.legal_entity_id, 1) on duplicate key update s_action = 1;
 UPDATE tbl_le_replication_status set settings_data = 1 where legal_entity_id = new.legal_entity_id;
 END
//
 DELIMITER ;



DROP TRIGGER IF EXISTS `after_tbl_users_status_update`;
DELIMITER //

CREATE TRIGGER `after_tbl_users_status_update` AFTER UPDATE ON `tbl_users`
 FOR EACH ROW BEGIN
    if ((old.is_active <> new.is_active) or (old.is_disable <> new.is_disable)) then
        INSERT INTO tbl_le_user_replication_status(legal_entity_id, user_id, s_action)
        select legal_entity_id, new.user_id, 1 from tbl_user_legal_entities where user_id = new.user_id
        on duplicate key update s_action = 1;
        
        UPDATE tbl_le_replication_status set user_data = 1
        where legal_entity_id in (select legal_entity_id from tbl_user_legal_entities where user_id = new.user_id);
    end if;

 END
//
 DELIMITER ;


DROP TRIGGER IF EXISTS `after_tbl_service_providers_insert`;
DELIMITER //

CREATE TRIGGER `after_tbl_service_providers_insert` AFTER INSERT ON `tbl_service_providers`
 FOR EACH ROW BEGIN
 insert into tbl_le_provider_replication_status(legal_entity_id, provider_id, s_action)
 select legal_entity_id, new.service_provider_id, 1 from tbl_legal_entities on duplicate key update s_action = 1;
 UPDATE tbl_le_replication_status set provider_data = 1 ;
 END
 //
 DELIMITER ;

DROP TRIGGER IF EXISTS `after_tbl_service_providers_update`;
DELIMITER //

CREATE TRIGGER `after_tbl_service_providers_update` AFTER UPDATE ON `tbl_service_providers`
 FOR EACH ROW BEGIN
 insert into tbl_le_provider_replication_status(legal_entity_id, provider_id, s_action)
 select legal_entity_id, new.service_provider_id, 1 from tbl_legal_entities on duplicate key update s_action = 1;
 UPDATE tbl_le_replication_status set provider_data = 1 ;
 END
//
DELIMITER ;

DROP TRIGGER IF EXISTS `after_tbl_user_groups_insert`;
DELIMITER //
CREATE TRIGGER `after_tbl_user_groups_insert` AFTER INSERT ON `tbl_user_groups`
 FOR EACH ROW BEGIN
 insert into tbl_le_user_groups_replication_status(legal_entity_id, user_group_id, s_action)
 select legal_entity_id, new.user_group_id, 1 from tbl_legal_entities on duplicate key update s_action = 0;
 UPDATE tbl_le_replication_status set privileges_data = 0 ;
 END
 //
 DELIMITER ;

DROP TRIGGER IF EXISTS `after_tbl_user_groups_update`;
DELIMITER //
CREATE TRIGGER `after_tbl_user_groups_update` AFTER UPDATE ON `tbl_user_groups`
 FOR EACH ROW BEGIN
 insert into tbl_le_user_groups_replication_status(legal_entity_id, user_group_id, s_action)
 select legal_entity_id, new.user_group_id, 1 from tbl_legal_entities on duplicate key update s_action = 1;
 UPDATE tbl_le_replication_status set privileges_data = 1 ;
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
