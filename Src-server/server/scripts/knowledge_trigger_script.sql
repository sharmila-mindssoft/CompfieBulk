-- CREATE TABLE tbl_audit_log
-- (
--    audit_trail_id   int(10) PRIMARY KEY NOT NULL AUTO_INCREMENT,
--    tbl_name         varchar(100),
--    tbl_auto_id      int(10),
--    column_name      varchar(100),
--    value            varchar(1000),
--    client_id        int(10),
--    action           varchar(20)
-- );

--
-- Triggers `tbl_business_groups`
--
DROP TRIGGER IF EXISTS `after_tbl_business_groups_insert`;
DELIMITER //
CREATE TRIGGER `after_tbl_business_groups_insert` AFTER INSERT ON `tbl_business_groups`
 FOR EACH ROW BEGIN
   SET @action = 0;


   INSERT INTO tbl_audit_log(action,
                             client_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                NEW.client_id,
                NEW.business_group_id,
                'business_group_name',
                NEW.business_group_name,
                'tbl_business_groups');

END
//
DELIMITER ;


DROP TRIGGER IF EXISTS `after_tbl_business_groups_update`;
DELIMITER //
CREATE TRIGGER `after_tbl_business_groups_update` AFTER UPDATE ON `tbl_business_groups`
 FOR EACH ROW BEGIN
   SET @action = 1;


   IF OLD.business_group_name <> NEW.business_group_name THEN
   INSERT INTO tbl_audit_log(action,
                             client_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                NEW.client_id,
                NEW.business_group_id,
                'business_group_name',
                NEW.business_group_name,
                'tbl_business_groups');
   END IF;

END
//
DELIMITER ;

--
-- Triggers `tbl_client_compliances`
--
DROP TRIGGER IF EXISTS `after_tbl_client_compliances_insert`;
-- DELIMITER //
-- CREATE TRIGGER `after_tbl_client_compliances_insert` AFTER INSERT ON `tbl_client_compliances`
--  FOR EACH ROW BEGIN
--    SET @action = 0;


--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--         VALUES (@action,
--                 0,
--                 NEW.client_compliance_id,
--                 'client_statutory_id',
--                 NEW.client_statutory_id,
--                 'tbl_client_compliances');


--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--         VALUES (@action,
--                 0,
--                 NEW.client_compliance_id,
--                 'compliance_id',
--                 NEW.compliance_id,
--                 'tbl_client_compliances');


--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--         VALUES (@action,
--                 0,
--                 NEW.client_compliance_id,
--                 'statutory_applicable',
--                 NEW.statutory_applicable,
--                 'tbl_client_compliances');


--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--         VALUES (@action,
--                 0,
--                 NEW.client_compliance_id,
--                 'statutory_opted',
--                 NEW.statutory_opted,
--                 'tbl_client_compliances');


--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--         VALUES (@action,
--                 0,
--                 NEW.client_compliance_id,
--                 'not_applicable_remarks',
--                 NEW.not_applicable_remarks,
--                 'tbl_client_compliances');


--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--         VALUES (@action,
--                 0,
--                 NEW.client_compliance_id,
--                 'compliance_applicable',
--                 NEW.compliance_applicable,
--                 'tbl_client_compliances');


--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--         VALUES (@action,
--                 0,
--                 NEW.client_compliance_id,
--                 'compliance_opted',
--                 NEW.compliance_opted,
--                 'tbl_client_compliances');


--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--         VALUES (@action,
--                 0,
--                 NEW.client_compliance_id,
--                 'compliance_remarks',
--                 NEW.compliance_remarks,
--                 'tbl_client_compliances');


--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--         VALUES (@action,
--                 0,
--                 NEW.client_compliance_id,
--                 'submitted_on',
--                 NEW.submitted_on,
--                 'tbl_client_compliances');

-- END
-- //
-- DELIMITER ;

DROP TRIGGER IF EXISTS `after_tbl_client_compliances_update`;
DELIMITER //
CREATE TRIGGER `after_tbl_client_compliances_update` AFTER UPDATE ON `tbl_client_compliances`
 FOR EACH ROW BEGIN
    SET @action = 1;
    SET @submission_type = (SELECT IFNULL(t1.submission_type, 0) FROM tbl_client_statutories t1 WHERE t1.client_statutory_id = NEW.client_statutory_id);


   IF (OLD.client_statutory_id <> NEW.client_statutory_id and @submission_type = 1) THEN
   INSERT INTO tbl_audit_log(action,
                             client_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                0,
                NEW.client_compliance_id,
                'client_statutory_id',
                NEW.client_statutory_id,
                'tbl_client_compliances');
   END IF;


   IF (OLD.compliance_id <> NEW.compliance_id and @submission_type = 1) THEN
   INSERT INTO tbl_audit_log(action,
                             client_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                0,
                NEW.client_compliance_id,
                'compliance_id',
                NEW.compliance_id,
                'tbl_client_compliances');
   END IF;


   IF (OLD.statutory_applicable <> NEW.statutory_applicable and @submission_type = 1) THEN
   INSERT INTO tbl_audit_log(action,
                             client_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                0,
                NEW.client_compliance_id,
                'statutory_applicable',
                NEW.statutory_applicable,
                'tbl_client_compliances');
   END IF;


   IF (OLD.statutory_opted <> NEW.statutory_opted and @submission_type = 1) THEN
   INSERT INTO tbl_audit_log(action,
                             client_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                0,
                NEW.client_compliance_id,
                'statutory_opted',
                NEW.statutory_opted,
                'tbl_client_compliances');
   END IF;


   IF (OLD.not_applicable_remarks <> NEW.not_applicable_remarks and @submission_type = 1) THEN
   INSERT INTO tbl_audit_log(action,
                             client_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                0,
                NEW.client_compliance_id,
                'not_applicable_remarks',
                NEW.not_applicable_remarks,
                'tbl_client_compliances');
   END IF;


   IF (OLD.compliance_applicable <> NEW.compliance_applicable and @submission_type = 1) THEN
   INSERT INTO tbl_audit_log(action,
                             client_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                0,
                NEW.client_compliance_id,
                'compliance_applicable',
                NEW.compliance_applicable,
                'tbl_client_compliances');
   END IF;


   IF (OLD.compliance_opted <> NEW.compliance_opted and @submission_type = 1) THEN
   INSERT INTO tbl_audit_log(action,
                             client_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                0,
                NEW.client_compliance_id,
                'compliance_opted',
                NEW.compliance_opted,
                'tbl_client_compliances');
   END IF;


   IF (OLD.compliance_remarks <> NEW.compliance_remarks and @submission_type = 1) THEN
   INSERT INTO tbl_audit_log(action,
                             client_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                0,
                NEW.client_compliance_id,
                'compliance_remarks',
                NEW.compliance_remarks,
                'tbl_client_compliances');
   END IF;


   IF (OLD.submitted_on <> NEW.submitted_on and @submission_type = 1) THEN
   INSERT INTO tbl_audit_log(action,
                             client_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                0,
                NEW.client_compliance_id,
                'submitted_on',
                NEW.submitted_on,
                'tbl_client_compliances');
   END IF;

END
//
DELIMITER ;


--
-- Triggers `tbl_client_configurations`
--
DROP TRIGGER IF EXISTS `after_tbl_client_configurations_insert`;
DELIMITER //
CREATE TRIGGER `after_tbl_client_configurations_insert` AFTER INSERT ON `tbl_client_configurations`
 FOR EACH ROW BEGIN
   SET @action = 0;


   INSERT INTO tbl_audit_log(action,
                             client_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                NEW.client_id,
                NEW.client_config_id,
                'country_id',
                NEW.country_id,
                'tbl_client_configurations');


   INSERT INTO tbl_audit_log(action,
                             client_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                NEW.client_id,
                NEW.client_config_id,
                'domain_id',
                NEW.domain_id,
                'tbl_client_configurations');


   INSERT INTO tbl_audit_log(action,
                             client_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                NEW.client_id,
                NEW.client_config_id,
                'period_from',
                NEW.period_from,
                'tbl_client_configurations');


   INSERT INTO tbl_audit_log(action,
                             client_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                NEW.client_id,
                NEW.client_config_id,
                'period_to',
                NEW.period_to,
                'tbl_client_configurations');

END
//
DELIMITER ;
DROP TRIGGER IF EXISTS `after_tbl_client_configurations_update`;
DELIMITER //
CREATE TRIGGER `after_tbl_client_configurations_update` AFTER UPDATE ON `tbl_client_configurations`
 FOR EACH ROW BEGIN
   SET @action = 1;


   IF OLD.country_id <> NEW.country_id THEN
   INSERT INTO tbl_audit_log(action,
                             client_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                NEW.client_id,
                NEW.client_config_id,
                'country_id',
                NEW.country_id,
                'tbl_client_configurations');
   END IF;


   IF OLD.domain_id <> NEW.domain_id THEN
   INSERT INTO tbl_audit_log(action,
                             client_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                NEW.client_id,
                NEW.client_config_id,
                'domain_id',
                NEW.domain_id,
                'tbl_client_configurations');
   END IF;


   IF OLD.period_from <> NEW.period_from THEN
   INSERT INTO tbl_audit_log(action,
                             client_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                NEW.client_id,
                NEW.client_config_id,
                'period_from',
                NEW.period_from,
                'tbl_client_configurations');
   END IF;


   IF OLD.period_to <> NEW.period_to THEN
   INSERT INTO tbl_audit_log(action,
                             client_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                NEW.client_id,
                NEW.client_config_id,
                'period_to',
                NEW.period_to,
                'tbl_client_configurations');
   END IF;

END
//
DELIMITER ;


--
-- Triggers `tbl_client_groups`
--
DROP TRIGGER IF EXISTS `after_tbl_client_groups_insert`;
DELIMITER //
CREATE TRIGGER `after_tbl_client_groups_insert` AFTER INSERT ON `tbl_client_groups`
 FOR EACH ROW BEGIN
   SET @action = 0;


   INSERT INTO tbl_audit_log(action,
                             client_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                NEW.client_id,
                NEW.client_id,
                'group_name',
                NEW.group_name,
                'tbl_client_groups');


   INSERT INTO tbl_audit_log(action,
                             client_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                NEW.client_id,
                NEW.client_id,
                'logo_url',
                NEW.logo_url,
                'tbl_client_groups');


   INSERT INTO tbl_audit_log(action,
                             client_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                NEW.client_id,
                NEW.client_id,
                'logo_size',
                NEW.logo_size,
                'tbl_client_groups');


   INSERT INTO tbl_audit_log(action,
                             client_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                NEW.client_id,
                NEW.client_id,
                'contract_from',
                NEW.contract_from,
                'tbl_client_groups');


   INSERT INTO tbl_audit_log(action,
                             client_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                NEW.client_id,
                NEW.client_id,
                'contract_to',
                NEW.contract_to,
                'tbl_client_groups');


   INSERT INTO tbl_audit_log(action,
                             client_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                NEW.client_id,
                NEW.client_id,
                'no_of_user_licence',
                NEW.no_of_user_licence,
                'tbl_client_groups');


   INSERT INTO tbl_audit_log(action,
                             client_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                NEW.client_id,
                NEW.client_id,
                'total_disk_space',
                NEW.total_disk_space,
                'tbl_client_groups');


   INSERT INTO tbl_audit_log(action,
                             client_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                NEW.client_id,
                NEW.client_id,
                'total_disk_space_used',
                NEW.total_disk_space_used,
                'tbl_client_groups');


   INSERT INTO tbl_audit_log(action,
                             client_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                NEW.client_id,
                NEW.client_id,
                'is_sms_subscribed',
                NEW.is_sms_subscribed,
                'tbl_client_groups');


   INSERT INTO tbl_audit_log(action,
                             client_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                NEW.client_id,
                NEW.client_id,
                'url_short_name',
                NEW.url_short_name,
                'tbl_client_groups');

END
//
DELIMITER ;
DROP TRIGGER IF EXISTS `after_tbl_client_groups_update`;
DELIMITER //
CREATE TRIGGER `after_tbl_client_groups_update` AFTER UPDATE ON `tbl_client_groups`
 FOR EACH ROW BEGIN
   SET @action = 1;


   IF OLD.group_name <> NEW.group_name THEN
   INSERT INTO tbl_audit_log(action,
                             client_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                NEW.client_id,
                NEW.client_id,
                'group_name',
                NEW.group_name,
                'tbl_client_groups');
   END IF;


   IF OLD.logo_url <> NEW.logo_url THEN
   INSERT INTO tbl_audit_log(action,
                             client_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                NEW.client_id,
                NEW.client_id,
                'logo_url',
                NEW.logo_url,
                'tbl_client_groups');
   END IF;


   IF OLD.logo_size <> NEW.logo_size THEN
   INSERT INTO tbl_audit_log(action,
                             client_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                NEW.client_id,
                NEW.client_id,
                'logo_size',
                NEW.logo_size,
                'tbl_client_groups');
   END IF;


   IF OLD.contract_from <> NEW.contract_from THEN
   INSERT INTO tbl_audit_log(action,
                             client_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                NEW.client_id,
                NEW.client_id,
                'contract_from',
                NEW.contract_from,
                'tbl_client_groups');
   END IF;


   IF OLD.contract_to <> NEW.contract_to THEN
   INSERT INTO tbl_audit_log(action,
                             client_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                NEW.client_id,
                NEW.client_id,
                'contract_to',
                NEW.contract_to,
                'tbl_client_groups');
   END IF;


   IF OLD.no_of_user_licence <> NEW.no_of_user_licence THEN
   INSERT INTO tbl_audit_log(action,
                             client_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                NEW.client_id,
                NEW.client_id,
                'no_of_user_licence',
                NEW.no_of_user_licence,
                'tbl_client_groups');
   END IF;


   IF OLD.total_disk_space <> NEW.total_disk_space THEN
   INSERT INTO tbl_audit_log(action,
                             client_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                NEW.client_id,
                NEW.client_id,
                'total_disk_space',
                NEW.total_disk_space,
                'tbl_client_groups');
   END IF;


   IF OLD.total_disk_space_used <> NEW.total_disk_space_used THEN
   INSERT INTO tbl_audit_log(action,
                             client_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                NEW.client_id,
                NEW.client_id,
                'total_disk_space_used',
                NEW.total_disk_space_used,
                'tbl_client_groups');
   END IF;


   IF OLD.is_sms_subscribed <> NEW.is_sms_subscribed THEN
   INSERT INTO tbl_audit_log(action,
                             client_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                NEW.client_id,
                NEW.client_id,
                'is_sms_subscribed',
                NEW.is_sms_subscribed,
                'tbl_client_groups');
   END IF;


   IF OLD.url_short_name <> NEW.url_short_name THEN
   INSERT INTO tbl_audit_log(action,
                             client_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                NEW.client_id,
                NEW.client_id,
                'url_short_name',
                NEW.url_short_name,
                'tbl_client_groups');
   END IF;

END
//
DELIMITER ;


--
-- Triggers `tbl_client_statutories`
--
DROP TRIGGER IF EXISTS `after_tbl_client_statutories_insert`;
-- DELIMITER //
-- CREATE TRIGGER `after_tbl_client_statutories_insert` AFTER INSERT ON `tbl_client_statutories`
--  FOR EACH ROW BEGIN
--    SET @action = 0;



--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--   SELECT @action, NEW.client_id, NEW.client_statutory_id, 'geography', parent_names, 'tbl_client_statutories'  FROM tbl_geographies WHERE geography_id=NEW.geography_id;




--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--         VALUES (@action,
--                 NEW.client_id,
--                 NEW.client_statutory_id,
--                 'country_id',
--                 NEW.country_id,
--                 'tbl_client_statutories');


--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--         VALUES (@action,
--                 NEW.client_id,
--                 NEW.client_statutory_id,
--                 'domain_id',
--                 NEW.domain_id,
--                 'tbl_client_statutories');


--    INSERT INTO tbl_audit_log(action,
--                              client_id,
--                              tbl_auto_id,
--                              column_name,
--                              value,
--                              tbl_name)
--         VALUES (@action,
--                 NEW.client_id,
--                 NEW.client_statutory_id,
--                 'unit_id',
--                 NEW.unit_id,
--                 'tbl_client_statutories');

-- END
-- //
-- DELIMITER ;

DROP TRIGGER IF EXISTS `after_tbl_client_statutories_update`;
DELIMITER //
CREATE TRIGGER `after_tbl_client_statutories_update` AFTER UPDATE ON `tbl_client_statutories`
 FOR EACH ROW BEGIN
   SET @action = 1;


   IF (OLD.geography_id <> NEW.geography_id and NEW.submission_type = 1 )THEN

   INSERT INTO tbl_audit_log(action,
                             client_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
  SELECT @action, NEW.client_id, NEW.client_statutory_id, 'geography', parent_names, 'tbl_client_statutories'  FROM tbl_geographies WHERE geography_id=NEW.geography_id;
   END IF;




   IF (OLD.country_id <> NEW.country_id and NEW.submission_type = 1) THEN
   INSERT INTO tbl_audit_log(action,
                             client_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                NEW.client_id,
                NEW.client_statutory_id,
                'country_id',
                NEW.country_id,
                'tbl_client_statutories');
   END IF;


   IF (OLD.domain_id <> NEW.domain_id and NEW.submission_type = 1) THEN
   INSERT INTO tbl_audit_log(action,
                             client_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                NEW.client_id,
                NEW.client_statutory_id,
                'domain_id',
                NEW.domain_id,
                'tbl_client_statutories');
   END IF;


   IF (OLD.unit_id <> NEW.unit_id and NEW.submission_type = 1) THEN
   INSERT INTO tbl_audit_log(action,
                             client_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                NEW.client_id,
                NEW.client_statutory_id,
                'unit_id',
                NEW.unit_id,
                'tbl_client_statutories');
   END IF;

END
//
DELIMITER ;


--
-- Triggers `tbl_compliances`
--
DROP TRIGGER IF EXISTS `after_tbl_compliances_insert`;
DELIMITER //
CREATE TRIGGER `after_tbl_compliances_insert` AFTER INSERT ON `tbl_compliances`
 FOR EACH ROW BEGIN
   SET @action = 0;



   INSERT INTO tbl_audit_log(action,
                             client_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
  SELECT @action, 0, NEW.compliance_id, 'statutory_mapping', statutory_mapping, 'tbl_compliances'  FROM tbl_statutory_mappings WHERE statutory_mapping_id=NEW.statutory_mapping_id;




   INSERT INTO tbl_audit_log(action,
                             client_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                0,
                NEW.compliance_id,
                'domain_id',
                NEW.domain_id,
                'tbl_compliances');


   INSERT INTO tbl_audit_log(action,
                             client_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                0,
                NEW.compliance_id,
                'frequency_id',
                NEW.frequency_id,
                'tbl_compliances');


   INSERT INTO tbl_audit_log(action,
                             client_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                0,
                NEW.compliance_id,
                'repeats_type_id',
                NEW.repeats_type_id,
                'tbl_compliances');


   INSERT INTO tbl_audit_log(action,
                             client_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                0,
                NEW.compliance_id,
                'duration_type_id',
                NEW.duration_type_id,
                'tbl_compliances');


   INSERT INTO tbl_audit_log(action,
                             client_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                0,
                NEW.compliance_id,
                'statutory_provision',
                NEW.statutory_provision,
                'tbl_compliances');


   INSERT INTO tbl_audit_log(action,
                             client_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                0,
                NEW.compliance_id,
                'compliance_task',
                NEW.compliance_task,
                'tbl_compliances');


   INSERT INTO tbl_audit_log(action,
                             client_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                0,
                NEW.compliance_id,
                'compliance_description',
                NEW.compliance_description,
                'tbl_compliances');


   INSERT INTO tbl_audit_log(action,
                             client_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                0,
                NEW.compliance_id,
                'document_name',
                NEW.document_name,
                'tbl_compliances');


   INSERT INTO tbl_audit_log(action,
                             client_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                0,
                NEW.compliance_id,
                'format_file',
                NEW.format_file,
                'tbl_compliances');


   INSERT INTO tbl_audit_log(action,
                             client_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                0,
                NEW.compliance_id,
                'format_file_size',
                NEW.format_file_size,
                'tbl_compliances');


   INSERT INTO tbl_audit_log(action,
                             client_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                0,
                NEW.compliance_id,
                'penal_consequences',
                NEW.penal_consequences,
                'tbl_compliances');


   INSERT INTO tbl_audit_log(action,
                             client_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                0,
                NEW.compliance_id,
                'statutory_dates',
                NEW.statutory_dates,
                'tbl_compliances');


   INSERT INTO tbl_audit_log(action,
                             client_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                0,
                NEW.compliance_id,
                'repeats_every',
                NEW.repeats_every,
                'tbl_compliances');


   INSERT INTO tbl_audit_log(action,
                             client_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                0,
                NEW.compliance_id,
                'duration',
                NEW.duration,
                'tbl_compliances');


   INSERT INTO tbl_audit_log(action,
                             client_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                0,
                NEW.compliance_id,
                'is_active',
                NEW.is_active,
                'tbl_compliances');

END
//
DELIMITER ;

DROP TRIGGER IF EXISTS `after_tbl_compliances_update`;
DELIMITER //
CREATE TRIGGER `after_tbl_compliances_update` AFTER UPDATE ON `tbl_compliances`
 FOR EACH ROW BEGIN
   SET @action = 1;


   IF OLD.statutory_mapping_id <> NEW.statutory_mapping_id THEN

   INSERT INTO tbl_audit_log(action,
                             client_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
  SELECT @action, 0, NEW.compliance_id, 'statutory_mapping', statutory_mapping, 'tbl_compliances'  FROM tbl_statutory_mappings WHERE statutory_mapping_id=NEW.statutory_mapping_id;
   END IF;




   IF OLD.domain_id <> NEW.domain_id THEN
   INSERT INTO tbl_audit_log(action,
                             client_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                0,
                NEW.compliance_id,
                'domain_id',
                NEW.domain_id,
                'tbl_compliances');
   END IF;


   IF OLD.frequency_id <> NEW.frequency_id THEN
   INSERT INTO tbl_audit_log(action,
                             client_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                0,
                NEW.compliance_id,
                'frequency_id',
                NEW.frequency_id,
                'tbl_compliances');
   END IF;


   IF OLD.repeats_type_id <> NEW.repeats_type_id THEN
   INSERT INTO tbl_audit_log(action,
                             client_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                0,
                NEW.compliance_id,
                'repeats_type_id',
                NEW.repeats_type_id,
                'tbl_compliances');
   END IF;


   IF OLD.duration_type_id <> NEW.duration_type_id THEN
   INSERT INTO tbl_audit_log(action,
                             client_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                0,
                NEW.compliance_id,
                'duration_type_id',
                NEW.duration_type_id,
                'tbl_compliances');
   END IF;


   IF OLD.statutory_provision <> NEW.statutory_provision THEN
   INSERT INTO tbl_audit_log(action,
                             client_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                0,
                NEW.compliance_id,
                'statutory_provision',
                NEW.statutory_provision,
                'tbl_compliances');
   END IF;


   IF OLD.compliance_task <> NEW.compliance_task THEN
   INSERT INTO tbl_audit_log(action,
                             client_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                0,
                NEW.compliance_id,
                'compliance_task',
                NEW.compliance_task,
                'tbl_compliances');
   END IF;


   IF OLD.compliance_description <> NEW.compliance_description THEN
   INSERT INTO tbl_audit_log(action,
                             client_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                0,
                NEW.compliance_id,
                'compliance_description',
                NEW.compliance_description,
                'tbl_compliances');
   END IF;


   IF OLD.document_name <> NEW.document_name THEN
   INSERT INTO tbl_audit_log(action,
                             client_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                0,
                NEW.compliance_id,
                'document_name',
                NEW.document_name,
                'tbl_compliances');
   END IF;


   IF OLD.format_file <> NEW.format_file THEN
   INSERT INTO tbl_audit_log(action,
                             client_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                0,
                NEW.compliance_id,
                'format_file',
                NEW.format_file,
                'tbl_compliances');
   END IF;


   IF OLD.format_file_size <> NEW.format_file_size THEN
   INSERT INTO tbl_audit_log(action,
                             client_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                0,
                NEW.compliance_id,
                'format_file_size',
                NEW.format_file_size,
                'tbl_compliances');
   END IF;


   IF OLD.penal_consequences <> NEW.penal_consequences THEN
   INSERT INTO tbl_audit_log(action,
                             client_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                0,
                NEW.compliance_id,
                'penal_consequences',
                NEW.penal_consequences,
                'tbl_compliances');
   END IF;


   IF OLD.statutory_dates <> NEW.statutory_dates THEN
   INSERT INTO tbl_audit_log(action,
                             client_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                0,
                NEW.compliance_id,
                'statutory_dates',
                NEW.statutory_dates,
                'tbl_compliances');
   END IF;


   IF OLD.repeats_every <> NEW.repeats_every THEN
   INSERT INTO tbl_audit_log(action,
                             client_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                0,
                NEW.compliance_id,
                'repeats_every',
                NEW.repeats_every,
                'tbl_compliances');
   END IF;


   IF OLD.duration <> NEW.duration THEN
   INSERT INTO tbl_audit_log(action,
                             client_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                0,
                NEW.compliance_id,
                'duration',
                NEW.duration,
                'tbl_compliances');
   END IF;


   IF OLD.is_active <> NEW.is_active THEN
   INSERT INTO tbl_audit_log(action,
                             client_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                0,
                NEW.compliance_id,
                'is_active',
                NEW.is_active,
                'tbl_compliances');
   END IF;

END
//
DELIMITER ;


--
-- Triggers `tbl_divisions`
--
DROP TRIGGER IF EXISTS `after_tbl_divisions_insert`;
DELIMITER //
CREATE TRIGGER `after_tbl_divisions_insert` AFTER INSERT ON `tbl_divisions`
 FOR EACH ROW BEGIN
   SET @action = 0;


   INSERT INTO tbl_audit_log(action,
                             client_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                NEW.client_id,
                NEW.division_id,
                'division_name',
                NEW.division_name,
                'tbl_divisions');

   INSERT INTO tbl_audit_log(action,
                             client_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                NEW.client_id,
                NEW.division_id,
                'business_group_id',
                NEW.business_group_id,
                'tbl_divisions');


   INSERT INTO tbl_audit_log(action,
                             client_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                NEW.client_id,
                NEW.division_id,
                'legal_entity_id',
                NEW.legal_entity_id,
                'tbl_divisions');

END
//
DELIMITER ;
DROP TRIGGER IF EXISTS `after_tbl_divisions_update`;
DELIMITER //
CREATE TRIGGER `after_tbl_divisions_update` AFTER UPDATE ON `tbl_divisions`
 FOR EACH ROW BEGIN
   SET @action = 1;


   IF OLD.division_name <> NEW.division_name THEN
   INSERT INTO tbl_audit_log(action,
                             client_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                NEW.client_id,
                NEW.division_id,
                'division_name',
                NEW.division_name,
                'tbl_divisions');
   END IF;

END
//
DELIMITER ;


--
-- Triggers `tbl_geographies`
--
DROP TRIGGER IF EXISTS `after_tbl_geographies_update`;
DELIMITER //
CREATE TRIGGER `after_tbl_geographies_update` AFTER UPDATE ON `tbl_geographies`
 FOR EACH ROW BEGIN
   SET @action = 1;
   IF OLD.parent_names <> NEW.parent_names THEN
   INSERT INTO tbl_audit_log(action,
                             client_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
  SELECT @action, client_id, client_statutory_id, 'geography', NEW.parent_names, 'tbl_client_statutories'  FROM tbl_client_statutories WHERE geography_id=NEW.geography_id;
   END IF;
   IF OLD.parent_names <> NEW.parent_names THEN
   INSERT INTO tbl_audit_log(action,
                             client_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
  SELECT @action, client_id, unit_id, 'geography', NEW.parent_names, 'tbl_units'  FROM tbl_units WHERE geography_id=NEW.geography_id;
   END IF;
END
//
DELIMITER ;

--
-- Triggers `tbl_industries`
--
DROP TRIGGER IF EXISTS `after_tbl_industries_update`;
DELIMITER //
CREATE TRIGGER `after_tbl_industries_update` AFTER UPDATE ON `tbl_industries`
 FOR EACH ROW BEGIN
   SET @action = 1;
   IF OLD.industry_name <> NEW.industry_name THEN
   INSERT INTO tbl_audit_log(action,
                             client_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
  SELECT @action, client_id, unit_id, 'industry_name', NEW.industry_name, 'tbl_units'  FROM tbl_units WHERE industry_id=NEW.industry_id;
   END IF;
END
//
DELIMITER ;


--
-- Triggers `tbl_legal_entities`
--
DROP TRIGGER IF EXISTS `after_tbl_legal_entities_insert`;
DELIMITER //
CREATE TRIGGER `after_tbl_legal_entities_insert` AFTER INSERT ON `tbl_legal_entities`
 FOR EACH ROW BEGIN
   SET @action = 0;


   INSERT INTO tbl_audit_log(action,
                             client_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                NEW.client_id,
                NEW.legal_entity_id,
                'legal_entity_name',
                NEW.legal_entity_name,
                'tbl_legal_entities');

   INSERT INTO tbl_audit_log(action,
                             client_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                NEW.client_id,
                NEW.legal_entity_id,
                'business_group_id',
                NEW.business_group_id,
                'tbl_legal_entities');

END
//
DELIMITER ;
DROP TRIGGER IF EXISTS `after_tbl_legal_entities_update`;
DELIMITER //
CREATE TRIGGER `after_tbl_legal_entities_update` AFTER UPDATE ON `tbl_legal_entities`
 FOR EACH ROW BEGIN
   SET @action = 1;


   IF OLD.legal_entity_name <> NEW.legal_entity_name THEN
   INSERT INTO tbl_audit_log(action,
                             client_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                NEW.client_id,
                NEW.legal_entity_id,
                'legal_entity_name',
                NEW.legal_entity_name,
                'tbl_legal_entities');
   END IF;

END
//
DELIMITER ;

--
-- Triggers `tbl_statutory_mappings`
--
DROP TRIGGER IF EXISTS `after_tbl_statutory_mappings_update`;
DELIMITER //
CREATE TRIGGER `after_tbl_statutory_mappings_update` AFTER UPDATE ON `tbl_statutory_mappings`
 FOR EACH ROW BEGIN
   SET @action = 1;
   IF OLD.statutory_mapping <> NEW.statutory_mapping THEN
   INSERT INTO tbl_audit_log(action,
                             client_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
  SELECT @action, 0, compliance_id, 'statutory_mapping', NEW.statutory_mapping, 'tbl_compliances'  FROM tbl_compliances WHERE statutory_mapping_id=NEW.statutory_mapping_id;
   END IF;
END
//
DELIMITER ;


--
-- Triggers `tbl_statutory_notifications_log`
--
DROP TRIGGER IF EXISTS `after_tbl_statutory_notifications_log_insert`;
DELIMITER //
CREATE TRIGGER `after_tbl_statutory_notifications_log_insert` AFTER INSERT ON `tbl_statutory_notifications_log`
 FOR EACH ROW BEGIN
   SET @action = 0;


   INSERT INTO tbl_audit_log(action,
                             client_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                0,
                NEW.statutory_notification_id,
                'country_name',
                NEW.country_name,
                'tbl_statutory_notifications_log');


   INSERT INTO tbl_audit_log(action,
                             client_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                0,
                NEW.statutory_notification_id,
                'domain_name',
                NEW.domain_name,
                'tbl_statutory_notifications_log');


   INSERT INTO tbl_audit_log(action,
                             client_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                0,
                NEW.statutory_notification_id,
                'industry_name',
                NEW.industry_name,
                'tbl_statutory_notifications_log');


   INSERT INTO tbl_audit_log(action,
                             client_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                0,
                NEW.statutory_notification_id,
                'statutory_nature',
                NEW.statutory_nature,
                'tbl_statutory_notifications_log');


   INSERT INTO tbl_audit_log(action,
                             client_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                0,
                NEW.statutory_notification_id,
                'statutory_provision',
                NEW.statutory_provision,
                'tbl_statutory_notifications_log');


   INSERT INTO tbl_audit_log(action,
                             client_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                0,
                NEW.statutory_notification_id,
                'applicable_location',
                NEW.applicable_location,
                'tbl_statutory_notifications_log');


   INSERT INTO tbl_audit_log(action,
                             client_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                0,
                NEW.statutory_notification_id,
                'notification_text',
                NEW.notification_text,
                'tbl_statutory_notifications_log');

END
//
DELIMITER ;
DROP TRIGGER IF EXISTS `after_tbl_statutory_notifications_log_update`;
DELIMITER //
CREATE TRIGGER `after_tbl_statutory_notifications_log_update` AFTER UPDATE ON `tbl_statutory_notifications_log`
 FOR EACH ROW BEGIN
   SET @action = 1;


   IF OLD.country_name <> NEW.country_name THEN
   INSERT INTO tbl_audit_log(action,
                             client_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                0,
                NEW.statutory_notification_id,
                'country_name',
                NEW.country_name,
                'tbl_statutory_notifications_log');
   END IF;


   IF OLD.domain_name <> NEW.domain_name THEN
   INSERT INTO tbl_audit_log(action,
                             client_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                0,
                NEW.statutory_notification_id,
                'domain_name',
                NEW.domain_name,
                'tbl_statutory_notifications_log');
   END IF;


   IF OLD.industry_name <> NEW.industry_name THEN
   INSERT INTO tbl_audit_log(action,
                             client_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                0,
                NEW.statutory_notification_id,
                'industry_name',
                NEW.industry_name,
                'tbl_statutory_notifications_log');
   END IF;


   IF OLD.statutory_nature <> NEW.statutory_nature THEN
   INSERT INTO tbl_audit_log(action,
                             client_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                0,
                NEW.statutory_notification_id,
                'statutory_nature',
                NEW.statutory_nature,
                'tbl_statutory_notifications_log');
   END IF;


   IF OLD.statutory_provision <> NEW.statutory_provision THEN
   INSERT INTO tbl_audit_log(action,
                             client_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                0,
                NEW.statutory_notification_id,
                'statutory_provision',
                NEW.statutory_provision,
                'tbl_statutory_notifications_log');
   END IF;


   IF OLD.applicable_location <> NEW.applicable_location THEN
   INSERT INTO tbl_audit_log(action,
                             client_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                0,
                NEW.statutory_notification_id,
                'applicable_location',
                NEW.applicable_location,
                'tbl_statutory_notifications_log');
   END IF;


   IF OLD.notification_text <> NEW.notification_text THEN
   INSERT INTO tbl_audit_log(action,
                             client_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                0,
                NEW.statutory_notification_id,
                'notification_text',
                NEW.notification_text,
                'tbl_statutory_notifications_log');
   END IF;

END
//
DELIMITER ;


--
-- Triggers `tbl_statutory_notifications_units`
--
DROP TRIGGER IF EXISTS `after_tbl_statutory_notifications_units_insert`;
DELIMITER //
CREATE TRIGGER `after_tbl_statutory_notifications_units_insert` AFTER INSERT ON `tbl_statutory_notifications_units`
 FOR EACH ROW BEGIN
   SET @action = 0;


   INSERT INTO tbl_audit_log(action,
                             client_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                NEW.client_id,
                NEW.statutory_notification_unit_id,
                'statutory_notification_id',
                NEW.statutory_notification_id,
                'tbl_statutory_notifications_units');


   INSERT INTO tbl_audit_log(action,
                             client_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                NEW.client_id,
                NEW.statutory_notification_unit_id,
                'business_group_id',
                NEW.business_group_id,
                'tbl_statutory_notifications_units');


   INSERT INTO tbl_audit_log(action,
                             client_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                NEW.client_id,
                NEW.statutory_notification_unit_id,
                'legal_entity_id',
                NEW.legal_entity_id,
                'tbl_statutory_notifications_units');


   INSERT INTO tbl_audit_log(action,
                             client_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                NEW.client_id,
                NEW.statutory_notification_unit_id,
                'division_id',
                NEW.division_id,
                'tbl_statutory_notifications_units');


   INSERT INTO tbl_audit_log(action,
                             client_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                NEW.client_id,
                NEW.statutory_notification_unit_id,
                'unit_id',
                NEW.unit_id,
                'tbl_statutory_notifications_units');

END
//
DELIMITER ;
DROP TRIGGER IF EXISTS `after_tbl_statutory_notifications_units_update`;
DELIMITER //
CREATE TRIGGER `after_tbl_statutory_notifications_units_update` AFTER UPDATE ON `tbl_statutory_notifications_units`
 FOR EACH ROW BEGIN
   SET @action = 1;


   IF OLD.statutory_notification_id <> NEW.statutory_notification_id THEN
   INSERT INTO tbl_audit_log(action,
                             client_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                NEW.client_id,
                NEW.statutory_notification_unit_id,
                'statutory_notification_id',
                NEW.statutory_notification_id,
                'tbl_statutory_notifications_units');
   END IF;


   IF OLD.business_group_id <> NEW.business_group_id THEN
   INSERT INTO tbl_audit_log(action,
                             client_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                NEW.client_id,
                NEW.statutory_notification_unit_id,
                'business_group_id',
                NEW.business_group_id,
                'tbl_statutory_notifications_units');
   END IF;


   IF OLD.legal_entity_id <> NEW.legal_entity_id THEN
   INSERT INTO tbl_audit_log(action,
                             client_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                NEW.client_id,
                NEW.statutory_notification_unit_id,
                'legal_entity_id',
                NEW.legal_entity_id,
                'tbl_statutory_notifications_units');
   END IF;


   IF OLD.division_id <> NEW.division_id THEN
   INSERT INTO tbl_audit_log(action,
                             client_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                NEW.client_id,
                NEW.statutory_notification_unit_id,
                'division_id',
                NEW.division_id,
                'tbl_statutory_notifications_units');
   END IF;


   IF OLD.unit_id <> NEW.unit_id THEN
   INSERT INTO tbl_audit_log(action,
                             client_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                NEW.client_id,
                NEW.statutory_notification_unit_id,
                'unit_id',
                NEW.unit_id,
                'tbl_statutory_notifications_units');
   END IF;

END
//
DELIMITER ;


--
-- Triggers `tbl_units`
--
DROP TRIGGER IF EXISTS `after_tbl_units_insert`;
DELIMITER //
CREATE TRIGGER `after_tbl_units_insert` AFTER INSERT ON `tbl_units`
 FOR EACH ROW BEGIN
   SET @action = 0;



   INSERT INTO tbl_audit_log(action,
                             client_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
  SELECT @action, NEW.client_id, NEW.unit_id, 'industry_name', industry_name, 'tbl_units'  FROM tbl_industries WHERE industry_id=NEW.industry_id;





   INSERT INTO tbl_audit_log(action,
                             client_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
  SELECT @action, NEW.client_id, NEW.unit_id, 'geography', parent_names, 'tbl_units'  FROM tbl_geographies WHERE geography_id=NEW.geography_id;




   INSERT INTO tbl_audit_log(action,
                             client_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                NEW.client_id,
                NEW.unit_id,
                'business_group_id',
                NEW.business_group_id,
                'tbl_units');


   INSERT INTO tbl_audit_log(action,
                             client_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                NEW.client_id,
                NEW.unit_id,
                'legal_entity_id',
                NEW.legal_entity_id,
                'tbl_units');


   INSERT INTO tbl_audit_log(action,
                             client_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                NEW.client_id,
                NEW.unit_id,
                'division_id',
                NEW.division_id,
                'tbl_units');


   INSERT INTO tbl_audit_log(action,
                             client_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                NEW.client_id,
                NEW.unit_id,
                'country_id',
                NEW.country_id,
                'tbl_units');


   INSERT INTO tbl_audit_log(action,
                             client_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                NEW.client_id,
                NEW.unit_id,
                'unit_code',
                NEW.unit_code,
                'tbl_units');


   INSERT INTO tbl_audit_log(action,
                             client_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                NEW.client_id,
                NEW.unit_id,
                'unit_name',
                NEW.unit_name,
                'tbl_units');


   INSERT INTO tbl_audit_log(action,
                             client_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                NEW.client_id,
                NEW.unit_id,
                'address',
                NEW.address,
                'tbl_units');


   INSERT INTO tbl_audit_log(action,
                             client_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                NEW.client_id,
                NEW.unit_id,
                'postal_code',
                NEW.postal_code,
                'tbl_units');


   INSERT INTO tbl_audit_log(action,
                             client_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                NEW.client_id,
                NEW.unit_id,
                'domain_ids',
                NEW.domain_ids,
                'tbl_units');


   INSERT INTO tbl_audit_log(action,
                             client_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                NEW.client_id,
                NEW.unit_id,
                'is_active',
                NEW.is_active,
                'tbl_units');

END
//
DELIMITER ;

DROP TRIGGER IF EXISTS `after_tbl_units_update`;
DELIMITER //
CREATE TRIGGER `after_tbl_units_update` AFTER UPDATE ON `tbl_units`
 FOR EACH ROW BEGIN
   SET @action = 1;


   IF OLD.industry_id <> NEW.industry_id THEN

   INSERT INTO tbl_audit_log(action,
                             client_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
  SELECT @action, NEW.client_id, NEW.unit_id, 'industry_name', industry_name, 'tbl_units'  FROM tbl_industries WHERE industry_id=NEW.industry_id;
   END IF;




   IF OLD.geography_id <> NEW.geography_id THEN

   INSERT INTO tbl_audit_log(action,
                             client_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
  SELECT @action, NEW.client_id, NEW.unit_id, 'geography', parent_names, 'tbl_units'  FROM tbl_geographies WHERE geography_id=NEW.geography_id;
   END IF;




   IF OLD.business_group_id <> NEW.business_group_id THEN
   INSERT INTO tbl_audit_log(action,
                             client_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                NEW.client_id,
                NEW.unit_id,
                'business_group_id',
                NEW.business_group_id,
                'tbl_units');
   END IF;


   IF OLD.legal_entity_id <> NEW.legal_entity_id THEN
   INSERT INTO tbl_audit_log(action,
                             client_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                NEW.client_id,
                NEW.unit_id,
                'legal_entity_id',
                NEW.legal_entity_id,
                'tbl_units');
   END IF;


   IF OLD.division_id <> NEW.division_id THEN
   INSERT INTO tbl_audit_log(action,
                             client_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                NEW.client_id,
                NEW.unit_id,
                'division_id',
                NEW.division_id,
                'tbl_units');
   END IF;


   IF OLD.country_id <> NEW.country_id THEN
   INSERT INTO tbl_audit_log(action,
                             client_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                NEW.client_id,
                NEW.unit_id,
                'country_id',
                NEW.country_id,
                'tbl_units');
   END IF;


   IF OLD.unit_code <> NEW.unit_code THEN
   INSERT INTO tbl_audit_log(action,
                             client_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                NEW.client_id,
                NEW.unit_id,
                'unit_code',
                NEW.unit_code,
                'tbl_units');
   END IF;


   IF OLD.unit_name <> NEW.unit_name THEN
   INSERT INTO tbl_audit_log(action,
                             client_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                NEW.client_id,
                NEW.unit_id,
                'unit_name',
                NEW.unit_name,
                'tbl_units');
   END IF;


   IF OLD.address <> NEW.address THEN
   INSERT INTO tbl_audit_log(action,
                             client_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                NEW.client_id,
                NEW.unit_id,
                'address',
                NEW.address,
                'tbl_units');
   END IF;


   IF OLD.postal_code <> NEW.postal_code THEN
   INSERT INTO tbl_audit_log(action,
                             client_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                NEW.client_id,
                NEW.unit_id,
                'postal_code',
                NEW.postal_code,
                'tbl_units');
   END IF;


   IF OLD.domain_ids <> NEW.domain_ids THEN
   INSERT INTO tbl_audit_log(action,
                             client_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                NEW.client_id,
                NEW.unit_id,
                'domain_ids',
                NEW.domain_ids,
                'tbl_units');
   END IF;


   IF OLD.is_active <> NEW.is_active THEN
   INSERT INTO tbl_audit_log(action,
                             client_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                NEW.client_id,
                NEW.unit_id,
                'is_active',
                NEW.is_active,
                'tbl_units');
   END IF;

END
//
DELIMITER ;
