ALTER TABLE `tbl_compliances` ADD INDEX `ccompliance_id_domain_id_idx` (`compliance_id`, `domain_id`);

ALTER TABLE `tbl_client_statutories` ADD CONSTRAINT `fk_client_unit_id` FOREIGN KEY (`unit_id`) REFERENCES `tbl_units` (`unit_id`) ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE `tbl_client_statutories` ADD INDEX `country_idx` (`country_id`);
ALTER TABLE `tbl_client_statutories` ADD INDEX `domain_idx` (`domain_id`);

ALTER TABLE `tbl_client_compliances` ADD CONSTRAINT `fk_client_statutory_id` FOREIGN KEY (`client_statutory_id`) REFERENCES `tbl_client_statutories` (`client_statutory_id`) ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE `tbl_client_compliances` ADD CONSTRAINT `fk_compliance_id` FOREIGN KEY (`compliance_id`) REFERENCES `tbl_compliances` (`compliance_id`) ON DELETE NO ACTION ON UPDATE NO ACTION;

ALTER TABLE `tbl_assigned_compliances` ADD CONSTRAINT `fk_assign_compliance_id` FOREIGN KEY (`compliance_id`) REFERENCES `tbl_compliances` (`compliance_id`) ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE `tbl_assigned_compliances` ADD CONSTRAINT `fk_assign_unit_id` FOREIGN KEY (`unit_id`) REFERENCES `tbl_units` (`unit_id`) ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE `tbl_assigned_compliances` ADD UNIQUE INDEX `compliance_id_unit_id_idx` (`unit_id`, `compliance_id`);

ALTER TABLE `tbl_compliance_history` ADD CONSTRAINT `fk_history_compliance_id` FOREIGN KEY (`compliance_id`) REFERENCES `tbl_compliances` (`compliance_id`) ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE `tbl_compliance_history` ADD CONSTRAINT `fk_history_unit_id` FOREIGN KEY (`unit_id`) REFERENCES `tbl_units` (`unit_id`) ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE `tbl_compliance_history` ADD INDEX `hisoty_compliance_id_unit_id_idx` (`unit_id`, `compliance_id`);

ALTER TABLE `tbl_reassigned_compliances_history` ADD CONSTRAINT `fk_reassign_compliance_id` FOREIGN KEY (`compliance_id`) REFERENCES `tbl_compliances` (`compliance_id`) ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE `tbl_reassigned_compliances_history` ADD CONSTRAINT `fk_reassign_unit_id` FOREIGN KEY (`unit_id`) REFERENCES `tbl_units` (`unit_id`) ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE `tbl_reassigned_compliances_history` ADD INDEX `reassign_compliance_id_unit_id_idx` (`unit_id`, `compliance_id`);

ALTER TABLE `tbl_notifications_log` ADD CONSTRAINT `fk_notification_compliance_id` FOREIGN KEY (`compliance_id`) REFERENCES `tbl_compliances` (`compliance_id`) ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE `tbl_notifications_log` ADD CONSTRAINT `fk_notification_unit_id` FOREIGN KEY (`unit_id`) REFERENCES `tbl_units` (`unit_id`) ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE `tbl_notifications_log` ADD INDEX `notification_compliance_id_unit_id_idx` (`unit_id`, `compliance_id`);


ALTER TABLE `tbl_notification_user_log` ADD CONSTRAINT `fk_notification_id` FOREIGN KEY (`notification_id`) REFERENCES `tbl_notifications_log` (`notification_id`) ON DELETE NO ACTION ON UPDATE NO ACTION;

ALTER TABLE `tbl_statutory_notification_status` ADD CONSTRAINT `fk_statutory_notification_id` FOREIGN KEY (`statutory_notification_id`) REFERENCES `tbl_statutory_notifications_log` (`statutory_notification_id`) ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE `tbl_statutory_notification_status` ADD INDEX `user_id_idx` (`user_id`);

ALTER TABLE `tbl_statutory_notifications_units` ADD CONSTRAINT `fk_statutory_notify_unit_id` FOREIGN KEY (`statutory_notification_id`) REFERENCES `tbl_statutory_notifications_log` (`statutory_notification_id`) ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE `tbl_statutory_notifications_units` ADD CONSTRAINT `fk_notify_unit_id` FOREIGN KEY (`unit_id`) REFERENCES `tbl_units` (`unit_id`) ON DELETE NO ACTION ON UPDATE NO ACTION;

ALTER IGNORE TABLE tbl_compliance_history
ADD UNIQUE INDEX idx2_compliancce_history (unit_id, compliance_id, start_date, due_date, next_due_date, completed_by);