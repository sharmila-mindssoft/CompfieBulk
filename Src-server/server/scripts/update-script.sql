SET FOREIGN_KEY_CHECKS = 0;

ALTER TABLE `compfie_knowledge`.`tbl_audit_log`
CHANGE COLUMN `audit_trail_id` `audit_trail_id` INT(11) NOT NULL AUTO_INCREMENT ;

ALTER TABLE `compfie_knowledge`.`tbl_user_groups`
CHANGE COLUMN `user_group_id` `user_group_id` INT(11) NOT NULL AUTO_INCREMENT ;

ALTER TABLE `compfie_knowledge`.`tbl_countries`
CHANGE COLUMN `country_id` `country_id` INT(11) NOT NULL AUTO_INCREMENT ;

ALTER TABLE `compfie_knowledge`.`tbl_domains`
CHANGE COLUMN `domain_id` `domain_id` INT(11) NOT NULL AUTO_INCREMENT ;

ALTER TABLE `compfie_knowledge`.`tbl_users`
CHANGE COLUMN `user_id` `user_id` INT(11) NOT NULL AUTO_INCREMENT ;

ALTER TABLE `compfie_knowledge`.`tbl_industries`
CHANGE COLUMN `industry_id` `industry_id` INT(11) NOT NULL AUTO_INCREMENT ;

ALTER TABLE `compfie_knowledge`.`tbl_statutory_natures`
CHANGE COLUMN `statutory_nature_id` `statutory_nature_id` INT(11) NOT NULL AUTO_INCREMENT ;

ALTER TABLE `compfie_knowledge`.`tbl_statutory_levels`
CHANGE COLUMN `level_id` `level_id` INT(11) NOT NULL AUTO_INCREMENT ;

ALTER TABLE `compfie_knowledge`.`tbl_geography_levels`
CHANGE COLUMN `level_id` `level_id` INT(11) NOT NULL AUTO_INCREMENT ;

ALTER TABLE `compfie_knowledge`.`tbl_geographies`
CHANGE COLUMN `geography_id` `geography_id` INT(11) NOT NULL AUTO_INCREMENT ;

ALTER TABLE `compfie_knowledge`.`tbl_statutory_mappings`
CHANGE COLUMN `statutory_mapping_id` `statutory_mapping_id` INT(11) NOT NULL AUTO_INCREMENT ;

ALTER TABLE `compfie_knowledge`.`tbl_statutories`
CHANGE COLUMN `statutory_id` `statutory_id` INT(11) NOT NULL AUTO_INCREMENT ;

ALTER TABLE `compfie_knowledge`.`tbl_compliances`
CHANGE COLUMN `compliance_id` `compliance_id` INT(11) NOT NULL AUTO_INCREMENT ;

ALTER TABLE `compfie_knowledge`.`tbl_statutories_backup`
CHANGE COLUMN `statutory_backup_id` `statutory_backup_id` INT(11) NOT NULL AUTO_INCREMENT ;

ALTER TABLE `compfie_knowledge`.`tbl_client_groups`
CHANGE COLUMN `client_id` `client_id` INT(11) NOT NULL AUTO_INCREMENT ;

ALTER TABLE `compfie_knowledge`.`tbl_client_configurations`
CHANGE COLUMN `client_config_id` `client_config_id` INT(11) NOT NULL AUTO_INCREMENT ;

ALTER TABLE `compfie_knowledge`.`tbl_business_groups`
CHANGE COLUMN `business_group_id` `business_group_id` INT(11) NOT NULL AUTO_INCREMENT ;

ALTER TABLE `compfie_knowledge`.`tbl_legal_entities`
CHANGE COLUMN `legal_entity_id` `legal_entity_id` INT(11) NOT NULL AUTO_INCREMENT ;

ALTER TABLE `compfie_knowledge`.`tbl_divisions`
CHANGE COLUMN `division_id` `division_id` INT(11) NOT NULL AUTO_INCREMENT ;

ALTER TABLE `compfie_knowledge`.`tbl_units`
CHANGE COLUMN `unit_id` `unit_id` INT(11) NOT NULL AUTO_INCREMENT ;

ALTER TABLE `compfie_knowledge`.`tbl_statutory_notifications_log`
CHANGE COLUMN `statutory_notification_id` `statutory_notification_id` INT(11) NOT NULL AUTO_INCREMENT ;

ALTER TABLE `compfie_knowledge`.`tbl_statutory_notifications_units`
CHANGE COLUMN `statutory_notification_unit_id` `statutory_notification_unit_id` INT(11) NOT NULL AUTO_INCREMENT ,
ADD PRIMARY KEY (`statutory_notification_unit_id`);

ALTER TABLE `compfie_knowledge`.`tbl_activity_log`
CHANGE COLUMN `activity_log_id` `activity_log_id` INT(11) NOT NULL AUTO_INCREMENT ;

ALTER TABLE `compfie_knowledge`.`tbl_notifications`
CHANGE COLUMN `notification_id` `notification_id` INT(11) NOT NULL AUTO_INCREMENT ;

ALTER TABLE `compfie_knowledge`.`tbl_client_statutories`
CHANGE COLUMN `client_statutory_id` `client_statutory_id` INT(11) NOT NULL AUTO_INCREMENT ;

ALTER TABLE `compfie_knowledge`.`tbl_client_compliances`
CHANGE COLUMN `client_compliance_id` `client_compliance_id` INT(11) NOT NULL AUTO_INCREMENT ;

