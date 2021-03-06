DROP FUNCTION IF EXISTS `current_ist_datetime`;
DELIMITER //
CREATE FUNCTION `current_ist_datetime`() RETURNS DATETIME
BEGIN
    DECLARE current_ist_date DATETIME;
    SET current_ist_date = convert_tz(utc_timestamp(),'+00:00','+05:30') ;

RETURN current_ist_date;
END //
DELIMITER ;


DROP FUNCTION IF EXISTS `SPLIT_STR`;
CREATE FUNCTION `SPLIT_STR`(
  x VARCHAR(1000),
  delim VARCHAR(12),
  pos INT
) RETURNS VARCHAR(1000) CHARSET latin1
RETURN REPLACE(SUBSTRING(SUBSTRING_INDEX(x, delim, pos),
       LENGTH(SUBSTRING_INDEX(x, delim, pos -1)) + 1),
       delim, '');


-- --------------------------------------------------------------------------------
-- Returns uploaded csv infor
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_statutory_mapping_csv_list`;
DELIMITER //
CREATE PROCEDURE `sp_statutory_mapping_csv_list`(
IN uploadedby INT
)
BEGIN
    SELECT COUNT(0) AS max_count FROM tbl_bulk_statutory_mapping_csv
    WHERE (IFNULL(is_fully_rejected, 0) = 1  OR IFNULL(declined_count, 0) > 0)
    AND approve_status != 4  AND uploaded_by = uploadedby;

    SELECT country_id, domain_id, csv_id, country_name,
    domain_name, csv_name, total_records, uploaded_on,
    total_documents, uploaded_documents
    FROM tbl_bulk_statutory_mapping_csv
    WHERE IFNULL(upload_status, 0) = 0  AND uploaded_by = uploadedby
    ORDER BY uploaded_on DESC;

    SELECT t1.csv_id, format_file FROM tbl_bulk_statutory_mapping AS t1
    INNER JOIN tbl_bulk_statutory_mapping_csv AS t2
    ON t2.csv_id = t1.csv_id
    WHERE IFNULL(t2.upload_status, 0) = 0 AND format_file != ''
    AND t2.uploaded_by = uploadedby AND IFNULL(t1.format_upload_status, 0) = 0;
END //
DELIMITER ;


DROP PROCEDURE IF EXISTS `sp_statutory_mapping_csv_save`;
DELIMITER //
CREATE PROCEDURE `sp_statutory_mapping_csv_save`(
IN uploadedby VARCHAR(200), c_id INT, c_name VARCHAR(100), d_id INT,
    d_name VARCHAR(100), csv_name VARCHAR(500),no_of_records INT,
    no_of_docs INT, upload_sts INT
)
BEGIN
    INSERT INTO tbl_bulk_statutory_mapping_csv(country_id, domain_id,
        country_name, domain_name, csv_name, uploaded_by, uploaded_on,
        total_records, total_documents, upload_status)
    VALUES (c_id, d_id, c_name, d_name, csv_name, uploadedby,
        current_ist_datetime(), no_of_records, no_of_docs, upload_sts
    );
END //
DELIMITER ;


DROP PROCEDURE IF EXISTS `sp_approve_mapping_action_save`;
DELIMITER //
CREATE PROCEDURE `sp_approve_mapping_action_save`(
IN csvid INT, smid INT, buaction INT, buremarks VARCHAR(500)
)
BEGIN
    UPDATE tbl_bulk_statutory_mapping SET action = buaction,
    remarks = buremarks WHERE csv_id = csvid AND
    bulk_statutory_mapping_id = smid;
END //
DELIMITER ;


DROP PROCEDURE IF EXISTS `sp_pending_statutory_mapping_csv_list`;
DELIMITER //
CREATE PROCEDURE `sp_pending_statutory_mapping_csv_list`(
IN uploadedby VARCHAR(50), cid INT, did INT
)
BEGIN
    SELECT t1.csv_id, csv_name, uploaded_on, uploaded_by,
    total_records,
    (SELECT COUNT(action) FROM tbl_bulk_statutory_mapping WHERE
     IFNULL(action, 0) = 1 AND csv_id = t1.csv_id) AS approve_count,
    (SELECT COUNT(action) FROM tbl_bulk_statutory_mapping WHERE
    IFNULL(action, 0) = 2 AND csv_id = t1.csv_id) AS rej_count,
    IFNULL(declined_count, 0) AS declined_count
    FROM tbl_bulk_statutory_mapping_csv AS t1
    WHERE upload_status =  1 AND approve_status = 0 AND IFNULL(t1.is_fully_rejected, 0) = 0
    AND country_id = cid AND domain_id = did
    AND FIND_IN_SET(uploaded_by, uploadedby)
    ORDER BY uploaded_on DESC;
END //
DELIMITER ;


DROP PROCEDURE IF EXISTS `sp_statutory_mapping_rejected_list`;
DELIMITER //
CREATE PROCEDURE `sp_statutory_mapping_rejected_list`(
IN uploadedby INT
)
BEGIN
    SELECT
      country_id,
      domain_id,
      csv_id,
      country_name,
      domain_name,
      csv_name,
      total_records,
      rejected_on,
      rejected_by,
      total_rejected_records,
      is_fully_rejected,
      rejected_reason,
      rejected_file_name,
      rejected_file_download_count
    FROM tbl_bulk_statutory_mapping_csv
    WHERE uploaded_by = uploadedby
    AND approve_status = 1
    AND (is_fully_rejected = 1 OR total_rejected_records > 0);
END //
DELIMITER ;


-- --------------------------------
-- Statutory Mapping - Bulk Report
-- --------------------------------
DROP PROCEDURE IF EXISTS `sp_statutory_mappings_bulk_reportdata`;
DELIMITER //
CREATE PROCEDURE `sp_statutory_mappings_bulk_reportdata`(
  IN `user_ids` VARCHAR(100), IN `country_ids` VARCHAR(100),
  IN `domain_ids` VARCHAR(100), IN `from_date` DATE, IN `to_date` DATE,
  IN `from_limit` INT(11), IN `to_limit` INT(11))
BEGIN
 SELECT
  tbl_bsm_csv.csv_id,
  tbl_bsm_csv.country_name,
  tbl_bsm_csv.domain_name,
  tbl_bsm_csv.uploaded_by,
  tbl_bsm_csv.uploaded_on,
  LEFT(tbl_bsm_csv.csv_name, LENGTH(tbl_bsm_csv.csv_name) - LOCATE('_', REVERSE(tbl_bsm_csv.csv_name))) AS csv_name,
  tbl_bsm_csv.total_records,
  (IFNULL(tbl_bsm_csv.total_rejected_records, 0) + IFNULL(tbl_bsm_csv.declined_count, 0)) AS total_rejected_records,
  tbl_bsm_csv.approved_by,
  tbl_bsm_csv.rejected_by,
  tbl_bsm_csv.approved_on,
  tbl_bsm_csv.rejected_on,
  tbl_bsm_csv.is_fully_rejected,
  (tbl_bsm_csv.total_records - IFNULL(tbl_bsm_csv.total_rejected_records, 0) - IFNULL(tbl_bsm_csv.declined_count, 0)) AS total_approve_records,
  tbl_bsm_csv.rejected_reason,
  tbl_bsm_csv.declined_count
FROM tbl_bulk_statutory_mapping_csv AS tbl_bsm_csv
WHERE
  tbl_bsm_csv.approve_status>0 AND
  FIND_IN_SET(tbl_bsm_csv.uploaded_by, user_ids)
  AND (DATE_FORMAT(DATE(tbl_bsm_csv.uploaded_on),"%Y-%m-%d") BETWEEN DATE(from_date) AND DATE(to_date))
  AND FIND_IN_SET(tbl_bsm_csv.domain_id, domain_ids)
  AND FIND_IN_SET(tbl_bsm_csv.country_id, country_ids)
  ORDER BY tbl_bsm_csv.uploaded_on DESC
  LIMIT from_limit, to_limit;

SELECT COUNT(DISTINCT tbl_bsm_csv.csv_id) AS total
FROM tbl_bulk_statutory_mapping_csv AS tbl_bsm_csv
 WHERE
  tbl_bsm_csv.approve_status>0 AND
  FIND_IN_SET(tbl_bsm_csv.uploaded_by, user_ids)
  AND (DATE_FORMAT(DATE(tbl_bsm_csv.uploaded_on),"%Y-%m-%d") BETWEEN DATE(from_date) AND DATE(to_date))
  AND FIND_IN_SET(tbl_bsm_csv.domain_id, domain_ids)
  AND FIND_IN_SET(tbl_bsm_csv.country_id, country_ids)
  ORDER BY tbl_bsm_csv.uploaded_on DESC;
END //
DELIMITER ;


DROP PROCEDURE IF EXISTS `sp_statutory_mapping_filter_list`;
DELIMITER //
CREATE PROCEDURE `sp_statutory_mapping_filter_list`(
IN csvid INT
)
BEGIN
    SELECT distinct organization FROM tbl_bulk_statutory_mapping WHERE csv_id = csvid;

    SELECT distinct statutory_nature FROM tbl_bulk_statutory_mapping WHERE csv_id = csvid;

    SELECT distinct statutory FROM tbl_bulk_statutory_mapping WHERE csv_id = csvid;

    SELECT distinct compliance_frequency FROM tbl_bulk_statutory_mapping WHERE csv_id = csvid;

    SELECT distinct geography_location FROM tbl_bulk_statutory_mapping WHERE csv_id = csvid;

    SELECT distinct compliance_task FROM tbl_bulk_statutory_mapping WHERE csv_id = csvid;

    SELECT distinct compliance_description FROM tbl_bulk_statutory_mapping WHERE csv_id = csvid;

    SELECT distinct compliance_document FROM tbl_bulk_statutory_mapping WHERE csv_id = csvid AND compliance_document != '';

    SELECT distinct task_id FROM tbl_bulk_statutory_mapping WHERE csv_id = csvid;

    SELECT distinct task_type FROM tbl_bulk_statutory_mapping WHERE csv_id = csvid;
END //
DELIMITER ;


DROP PROCEDURE IF EXISTS `sp_download_assign_statutory_template`;
DELIMITER //
CREATE PROCEDURE `sp_download_assign_statutory_template`(
    IN clientgroup_name TEXT, country_name TEXT, le_name TEXT, domain_name TEXT, unitname_ TEXT
)
BEGIN
    SELECT
    client_group, country, legal_entity, domain, organization, unit_code, unit_name,
    unit_location, perimary_legislation, secondary_legislation, statutory_provision, compliance_task_name,
    compliance_description
    FROM tbl_download_assign_statutory_template WHERE
    client_group = clientgroup_name AND country = country_name AND legal_entity = le_name AND find_in_set (domain, domain_name)
    AND find_in_set (unit_name, unitname_)
    ORDER BY domain, unit_code;
END //
DELIMITER ;


-- --------------------------------------------------------------------------------
-- to delete assign_statutory_template records
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_delete_assign_statutory_template`;
DELIMITER //
CREATE PROCEDURE `sp_delete_assign_statutory_template`(IN
  legalentityname_ TEXT, domainname_ TEXT, unitname_ TEXT)
BEGIN
    DELETE FROM tbl_download_assign_statutory_template
    WHERE legal_entity = legalentityname_ AND
    find_in_set (domain, domainname_) AND find_in_set (unit_name, unitname_);
END //
DELIMITER ;


-- --------------------------------------------------------------------------------
-- To save the client unit csv master table
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_client_units_bulk_csv_save`;
DELIMITER //
CREATE PROCEDURE `sp_client_units_bulk_csv_save`(
    IN _client_id INT(11), _group_name VARCHAR(50), _csv_name VARCHAR(100),
    _upl_by INT(11), _total_rec INT(11))
BEGIN
    INSERT INTO tbl_bulk_units_csv
    (client_id, client_group, csv_name, uploaded_by,
    uploaded_on, total_records)
    VALUES
    (_client_id, _group_name, _csv_name, _upl_by,
    current_ist_datetime(), _total_rec);
END //
DELIMITER ;


DROP PROCEDURE IF EXISTS `sp_statutory_mapping_view_by_filter`;
DELIMITER //
CREATE PROCEDURE `sp_statutory_mapping_view_by_filter`(
IN csvid INT, orga_name VARCHAR(50), s_nature VARCHAR(50),
frequency VARCHAR(70), statu VARCHAR(200), geo_location VARCHAR(500),
c_task VARCHAR(100), c_desc VARCHAR(500), c_doc VARCHAR(100),
f_count INT, f_range INT, tsk_id VARCHAR(50), tsk_type VARCHAR(100),
view_data INT
)
BEGIN
    SELECT distinct t1.csv_id, t1.country_name,
    t1.domain_name, t1.csv_name, t1.uploaded_by, t1.uploaded_on,
    t2.bulk_statutory_mapping_id, t2.s_no,
    t2.organization, t2.geography_location, t2.statutory_nature,
    t2.statutory, t2.statutory_provision, t2.compliance_task,
    t2.compliance_description, t2.penal_consequences,
    t2.compliance_document,
    t2.reference_link, t2.compliance_frequency,
    t2.statutory_month, t2.statutory_date, t2.trigger_before,
    t2.repeats_every, t2.repeats_type, t2.repeat_by, t2.duration,
    t2.duration_type, t2.multiple_input, t2.format_file,
    t2.task_id, t2.task_type, t2.action, t2.remarks

    FROM tbl_bulk_statutory_mapping_csv AS t1
    INNER JOIN tbl_bulk_statutory_mapping AS t2 ON
    t1.csv_id  = t2.csv_id WHERE t1.csv_id = csvid
    AND t2.organization LIKE orga_name AND t2.geography_location LIKE geo_location
    AND t2.statutory_nature LIKE s_nature AND t2.statutory LIKE statu
    AND t2.compliance_task LIKE c_task
    AND t2.compliance_description LIKE c_desc AND t2.compliance_document LIKE c_doc
    AND t2.task_id LIKE tsk_id AND t2.task_type LIKE tsk_type
    AND (CASE WHEN view_data =1 THEN IFNULL(t2.action, 0) > 0
      WHEN view_data =2 THEN IFNULL(t2.action, 0) = 0
          ELSE IFNULL(t2.action, 0) LIKE "%" END)
  AND (CASE WHEN frequency = '%' THEN t2.compliance_frequency LIKE "%"
          ELSE FIND_IN_SET(t2.compliance_frequency, frequency)
          END)
    LIMIT f_count, f_range;

    SELECT COUNT(distinct t2.bulk_statutory_mapping_id) AS total
    FROM tbl_bulk_statutory_mapping_csv AS t1
    INNER JOIN tbl_bulk_statutory_mapping AS t2 ON
    t1.csv_id  = t2.csv_id WHERE t1.csv_id = csvid
    AND t2.organization LIKE orga_name AND t2.geography_location LIKE geo_location
    AND t2.statutory_nature LIKE s_nature AND t2.statutory LIKE statu
    AND t2.compliance_task LIKE c_task
    AND t2.compliance_description LIKE c_desc AND t2.compliance_document LIKE c_doc
    AND t2.task_id LIKE tsk_id AND t2.task_type LIKE tsk_type
    AND (CASE WHEN view_data =1 THEN IFNULL(t2.action, 0) > 0
      WHEN view_data =2 THEN IFNULL(t2.action, 0) = 0
          ELSE IFNULL(t2.action, 0) LIKE "%"
          END)
  AND (CASE WHEN frequency = '%' THEN t2.compliance_frequency LIKE "%"
          ELSE FIND_IN_SET(t2.compliance_frequency, frequency)
          END);
END //
DELIMITER ;


DROP PROCEDURE IF EXISTS `sp_statutory_mapping_view_by_csvid`;
DELIMITER //
CREATE PROCEDURE `sp_statutory_mapping_view_by_csvid`(
IN csvid INT, f_count INT, f_range INT
)
BEGIN
    SELECT t1.csv_id, t1.country_name,
    t1.domain_name, t1.csv_name, t1.uploaded_by, t1.uploaded_on, t1.total_records,
    t2.bulk_statutory_mapping_id, t2.s_no,
    t2.organization, t2.geography_location, t2.statutory_nature,
    t2.statutory, t2.statutory_provision, t2.compliance_task,
    t2.compliance_description, t2.penal_consequences,
    t2.compliance_document,
    t2.reference_link, t2.compliance_frequency,
    t2.statutory_month, t2.statutory_date, t2.trigger_before,
    t2.repeats_every, t2.repeats_type, t2.repeat_by, t2.duration,
    t2.duration_type, t2.multiple_input, t2.format_file,
    t2.task_id, t2.task_type, t2.action, t2.remarks
    FROM tbl_bulk_statutory_mapping_csv AS t1
    INNER JOIN tbl_bulk_statutory_mapping AS t2 ON
    t1.csv_id  = t2.csv_id WHERE t1.csv_id = csvid
    LIMIT f_count, f_range;
END //
DELIMITER ;


DROP PROCEDURE IF EXISTS `sp_statutory_mapping_update_all_action`;
DELIMITER //
CREATE PROCEDURE `sp_statutory_mapping_update_all_action`(
IN csvid INT, action INT, remarks VARCHAR(500),
userid INT

)
BEGIN
    IF action = 2 THEN
        UPDATE tbl_bulk_statutory_mapping SET action = 2
        WHERE csv_id = csvid;

        UPDATE tbl_bulk_statutory_mapping_csv SET
        rejected_reason = remarks, is_fully_rejected = 1,
        rejected_by = userid,
        rejected_on = current_ist_datetime(),
        approve_status = 2,
        total_rejected_records = (SELECT COUNT(0) FROM
        tbl_bulk_statutory_mapping AS t WHERE IFNULL(action, 0) = 2
        AND t.csv_id = csvid)
        WHERE csv_id = csvid;

    ELSE
        UPDATE tbl_bulk_statutory_mapping SET
        action = 1, remarks = remarks
        WHERE csv_id = csvid;

        UPDATE tbl_bulk_statutory_mapping_csv SET
        approve_status = 1, approved_on = current_ist_datetime(),
        approved_by = userid, is_fully_rejected = 0,
        total_rejected_records = (SELECT COUNT(0)
          FROM tbl_bulk_statutory_mapping AS t
          WHERE IFNULL(action, 0) = 2 AND
          t.csv_id = csvid
        )
        WHERE csv_id = csvid;
    END IF;
END //
DELIMITER ;


-- --------------------------------------------------------------------------------
-- To get the client unit bulk uploaded file slist
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_client_units_csv_list`;
DELIMITER //
CREATE PROCEDURE `sp_client_units_csv_list`(
    IN _clientId INT(11), _groupName VARCHAR(50))
BEGIN
  SELECT t1.csv_unit_id, t1.csv_name, t1.uploaded_by,
    DATE_FORMAT(t1.uploaded_on, '%d-%b-%Y %H:%i') AS uploaded_on,
    t1.total_records AS no_of_records,
    (SELECT COUNT(*) FROM tbl_bulk_units WHERE csv_unit_id =
    t1.csv_unit_id AND action = 1) AS approved_count,
    (SELECT COUNT(*) FROM tbl_bulk_units WHERE csv_unit_id =
    t1.csv_unit_id AND action = 2) AS rej_count,
    (SELECT COUNT(*) FROM tbl_bulk_units WHERE csv_unit_id =
    t1.csv_unit_id AND action = 3) AS declined_count
  FROM
    tbl_bulk_units_csv AS t1 WHERE t1.client_id = _clientId AND
    (IFNULL(t1.is_fully_rejected, 0) = 0 AND IFNULL(t1.approve_status, 0) = 0)
    AND t1.client_group = _groupName ORDER BY t1.uploaded_on DESC;
END //
DELIMITER ;


DROP PROCEDURE IF EXISTS `sp_statutory_mapping_by_csvid`;
DELIMITER //
CREATE PROCEDURE `sp_statutory_mapping_by_csvid`(
IN csvid INT
)
BEGIN
    SELECT
    t2.bulk_statutory_mapping_id, t2.s_no,
    t2.organization AS Organization, t2.geography_location AS Applicable_Location,
    t2.statutory_nature AS Statutory_Nature,
    t2.statutory AS Statutory, t2.statutory_provision AS Statutory_Provision,
    t2.compliance_task AS Compliance_Task, t2.compliance_document AS Compliance_Document,
    t2.compliance_description AS Compliance_Description, t2.penal_consequences AS Penal_Consequences,
    t2.reference_link AS Reference_Link, t2.compliance_frequency AS Compliance_Frequency,
    t2.statutory_month AS Statutory_Month, t2.statutory_date AS Statutory_Date, t2.trigger_before AS Trigger_Days,
    t2.repeats_every AS Repeats_Every, t2.repeats_type AS Repeats_Type, t2.repeat_by AS `Repeats_By (DOM/EOM)`, t2.duration AS Duration,
    t2.duration_type AS Duration_Type, t2.multiple_input AS Multiple_Input_Section, t2.format_file AS Format,
    t2.task_id AS Task_ID, t2.task_type AS Task_Type,
    t2.action, t2.remarks, t2.format_file_size,
    t1.uploaded_by, t1.country_name, t1.domain_name, t1.csv_name,
    t1.approved_by, t1.approved_on
    FROM tbl_bulk_statutory_mapping AS t2
    INNER JOIN tbl_bulk_statutory_mapping_csv AS t1
    ON t1.csv_id = t2.csv_id
    WHERE (t2.action IS null or t2.action != 3) AND t2.csv_id = csvid;
END//
DELIMITER ;


DROP PROCEDURE IF EXISTS `sp_assign_statutory_csv_save`;
DELIMITER //
CREATE PROCEDURE `sp_assign_statutory_csv_save`(
IN uploadedby VARCHAR(200), cl_id INT, le_id INT, d_ids TEXT,
    le_name VARCHAR(100), d_names TEXT, csv_name VARCHAR(100),no_of_records INT
)
BEGIN
    INSERT INTO tbl_bulk_assign_statutory_csv(client_id, legal_entity_id,
        domain_ids, legal_entity, domain_names, csv_name, uploaded_by, uploaded_on,
        total_records)
    VALUES (cl_id, le_id, d_ids, le_name, d_names, csv_name, uploadedby,
        current_ist_datetime(), no_of_records
    );
END //
DELIMITER ;


DROP PROCEDURE IF EXISTS `sp_pending_assign_statutory_csv_list`;
DELIMITER //
CREATE PROCEDURE `sp_pending_assign_statutory_csv_list`(
IN cl_id INT, le_id INT
)
BEGIN
    SELECT t1.csv_assign_statutory_id, t1.csv_name, t1.uploaded_by,
    DATE_FORMAT(t1.uploaded_on, '%d-%b-%Y %H:%i') AS uploaded_on, t1.total_records,
    (SELECT COUNT(action) FROM tbl_bulk_assign_statutory WHERE
     action = 1 AND csv_assign_statutory_id = t1.csv_assign_statutory_id) AS approved_count,
    (SELECT COUNT(action) FROM tbl_bulk_assign_statutory WHERE
     action = 2 AND csv_assign_statutory_id = t1.csv_assign_statutory_id) AS rejected_count
    FROM tbl_bulk_assign_statutory_csv AS t1
    WHERE t1.approve_status =  0 AND t1.client_id = cl_id AND t1.legal_entity_id = le_id
    ORDER BY t1.uploaded_on DESC;
END //
DELIMITER ;


DROP PROCEDURE IF EXISTS `sp_assgined_statutory_bulk_reportdata`;
DELIMITER //
CREATE PROCEDURE `sp_assgined_statutory_bulk_reportdata`(
  IN `client_group_id` INT(11),
  IN `legal_entity_id` INT(11),
  IN `unit_id` VARCHAR(100),
  IN `from_date` DATE,
  IN `to_date` DATE,
  IN `from_limit` INT,
  IN `to_limit` INT,
  IN `user_ids` VARCHAR(100),
  IN `domain_id` VARCHAR(50))
BEGIN
DROP TEMPORARY TABLE IF EXISTS my_temp_table;
  Call split_comma (domain_id);

  SELECT t1.csv_assign_statutory_id, t1.domain_names,
    t1.uploaded_by,
    t1.uploaded_on,
    LEFT(t1.csv_name, LENGTH(t1.csv_name) - LOCATE('_', REVERSE(t1.csv_name)))
    AS csv_name,
    t1.total_records,
    (IFNULL(t1.total_rejected_records, 0) + IFNULL(t1.declined_count, 0))
    AS total_rejected_records,
    t1.approved_by,
    t1.rejected_by,
    t1.approved_on,
    t1.rejected_on,
    t1.is_fully_rejected,
    (t1.total_records - IFNULL(t1.total_rejected_records, 0) - IFNULL(t1.declined_count, 0))
    AS total_approve_records,
    t1.approve_status,
    t1.rejected_reason,
    t1.declined_count
  FROM tbl_bulk_assign_statutory_csv AS t1
  INNER JOIN my_temp_table t3 ON t1.domain_ids = t3.comma_stuff
  WHERE
  t1.approve_status>0 AND
  t1.client_id = client_group_id AND
  t1.legal_entity_id = legal_entity_id AND
  FIND_IN_SET(t1.uploaded_by, user_ids) AND
  (DATE_FORMAT(DATE(t1.uploaded_on),"%Y-%m-%d") BETWEEN DATE(from_date) AND DATE(to_date))
  ORDER BY t1.uploaded_on DESC
  LIMIT from_limit, to_limit;

  SELECT COUNT(t1.csv_assign_statutory_id) AS total
  FROM tbl_bulk_assign_statutory_csv AS t1
  INNER JOIN my_temp_table t3 ON t1.domain_ids = t3.comma_stuff
  WHERE
  t1.approve_status>0 AND
  t1.client_id = client_group_id AND
  t1.legal_entity_id = legal_entity_id AND
  FIND_IN_SET(t1.uploaded_by, user_ids) AND
  (DATE_FORMAT(DATE(t1.uploaded_on),"%Y-%m-%d") BETWEEN DATE(from_date) AND DATE(to_date))
  ORDER BY t1.uploaded_on DESC;

  DELETE FROM my_temp_table;

END //
DELIMITER ;


-- ----------------------------------------------------------------------------
-- To delete the rejected statutory mapping record by csv id
-- ----------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_delete_reject_sm_by_csvid`;
DELIMITER //
CREATE PROCEDURE `sp_delete_reject_sm_by_csvid`(IN `csvid` INT)
BEGIN
Declare isfullyrejected INT DEFAULT 0;
SET isfullyrejected=(SELECT is_fully_rejected FROM tbl_bulk_statutory_mapping_csv WHERE csv_id=csvid);

 if isfullyrejected=1 THEN
  UPDATE tbl_bulk_statutory_mapping_csv SET approve_status = 4 WHERE csv_id=csvid;
  Delete FROM tbl_bulk_statutory_mapping WHERE csv_id=csvid;
 ELSE
  UPDATE tbl_bulk_statutory_mapping_csv SET approve_status = 4 WHERE csv_id=csvid;
  Delete FROM tbl_bulk_statutory_mapping WHERE csv_id=csvid AND action=3;
 END IF;
END//
DELIMITER ;


DROP PROCEDURE IF EXISTS `sp_rejected_statutory_mapping_reportdata`;
DELIMITER //
CREATE PROCEDURE `sp_rejected_statutory_mapping_reportdata`(IN `country_id` INT(11),
  IN `domain_id` INT(11), IN `user_id` INT(11))
BEGIN
 SELECT sm.csv_id,
sm_csv.country_name,
sm_csv.domain_name,
sm_csv.uploaded_by,
sm_csv.uploaded_on,
LEFT(sm_csv.csv_name, LENGTH(sm_csv.csv_name) - LOCATE('_', REVERSE(sm_csv.csv_name))) AS csv_name,
sm_csv.total_records,
(IFNULL(sm_csv.total_rejected_records, 0) + IFNULL(sm_csv.declined_count, 0)) AS total_rejected_records,
sm_csv.approved_by,
sm_csv.rejected_by,
sm_csv.approved_on,
IFNULL(sm_csv.rejected_on, sm_csv.approved_on) AS rejected_on,
sm_csv.is_fully_rejected,
sm_csv.approve_status,
sm_csv.rejected_file_download_count,
sm.remarks,
sm.action,
sm_csv.rejected_reason,
(sm_csv.total_records - IFNULL(sm_csv.total_rejected_records, 0) - IFNULL(sm_csv.declined_count, 0)) AS total_approve_records,
sm_csv.declined_count
FROM tbl_bulk_statutory_mapping AS sm
INNER JOIN tbl_bulk_statutory_mapping_csv AS sm_csv ON sm_csv.csv_id=sm.csv_id
 WHERE
  sm_csv.country_id=country_id AND
  sm_csv.domain_id=domain_id AND
  sm_csv.uploaded_by=user_id AND
  (sm.action=3 OR sm_csv.is_fully_rejected=1) -- Declined Action
  GROUP BY sm.csv_id,
  sm_csv.country_name,
  sm_csv.domain_name,
  sm_csv.uploaded_by,
  sm_csv.uploaded_on,
  sm_csv.csv_name,
  sm_csv.total_records,
  sm_csv.approved_by,
  sm_csv.rejected_by,
  sm_csv.approved_on,
  sm_csv.rejected_on,
  sm_csv.is_fully_rejected,
  sm_csv.approve_status,
  sm_csv.rejected_file_download_count,
  sm.remarks,
  sm.action,
  sm_csv.rejected_reason,
  sm_csv.total_records,sm_csv.total_rejected_records,sm_csv.declined_count,
  sm_csv.declined_count
  ORDER BY IFNULL(sm_csv.approved_on, sm_csv.rejected_on) DESC;
END//
DELIMITER ;


DROP PROCEDURE IF EXISTS `sp_update_download_count_by_csvid`;
DELIMITER //
CREATE PROCEDURE `sp_update_download_count_by_csvid`(IN `csvid` INT(11))
BEGIN
DECLARE checknull INT DEFAULT 0;

SET checknull=(SELECT rejected_file_download_count FROM tbl_bulk_statutory_mapping_csv  WHERE csv_id=csvid);

IF(checknull IS NULL) THEN
   UPDATE tbl_bulk_statutory_mapping_csv SET rejected_file_download_count=1 WHERE csv_id=csvid;
ELSE
  UPDATE tbl_bulk_statutory_mapping_csv
  SET rejected_file_download_count=rejected_file_download_count+1
  WHERE csv_id=csvid;
END IF;

SELECT csv_id, rejected_file_download_count
FROM tbl_bulk_statutory_mapping_csv
WHERE csv_id=csvid;
END //
DELIMITER ;


DROP PROCEDURE IF EXISTS `sp_client_unit_bulk_reportdata`;
DELIMITER //
CREATE PROCEDURE `sp_client_unit_bulk_reportdata`(
  IN `client_group_id` INT(11),
  IN `from_date` DATE,
  IN `to_date` DATE,
  IN `from_limit` INT(11),
  IN `to_limit` INT(11),
  IN `user_ids` VARCHAR(100))
BEGIN
  SELECT
  DISTINCT t1.csv_unit_id,
  t1.uploaded_by,
  t1.uploaded_on,
  LEFT(t1.csv_name, LENGTH(t1.csv_name) - LOCATE('_', REVERSE(t1.csv_name))) AS csv_name,
  t1.total_records,
  (IFNULL(t1.total_rejected_records, 0) + IFNULL(t1.declined_count, 0)) AS total_rejected_records,
  t1.approved_by,
  t1.rejected_by,
  t1.approved_on,
  t1.rejected_on,
  t1.is_fully_rejected,
  t1.approve_status,
  t1.rejected_reason,
  (t1.total_records - IFNULL(t1.total_rejected_records, 0) - IFNULL(t1.declined_count, 0))
  AS total_approve_records,
  t1.declined_count
  FROM tbl_bulk_units_csv AS t1
  WHERE
    t1.approve_status>0 AND
    FIND_IN_SET(t1.uploaded_by, user_ids) AND
    t1.client_id = client_group_id AND
    (DATE_FORMAT(DATE(t1.uploaded_on),"%Y-%m-%d")
  BETWEEN DATE(from_date) AND DATE(to_date))
  ORDER BY t1.uploaded_on DESC
  LIMIT from_limit, to_limit;

  SELECT COUNT(DISTINCT t1.csv_unit_id) AS total
  FROM tbl_bulk_units_csv AS t1
  WHERE
  t1.approve_status>0 AND
  FIND_IN_SET(t1.uploaded_by, user_ids) AND
  t1.client_id = client_group_id AND
  (DATE_FORMAT(DATE(t1.uploaded_on),"%Y-%m-%d")
  BETWEEN DATE(from_date) AND DATE(to_date))
  ORDER BY t1.uploaded_on DESC;
END //
DELIMITER ;


DROP PROCEDURE IF EXISTS `sp_delete_reject_cu_by_csvid`;
DELIMITER //
CREATE PROCEDURE `sp_delete_reject_cu_by_csvid`(IN `csvid` INT(11))
BEGIN
Declare isfullyrejected INT DEFAULT 0;
SET isfullyrejected=(SELECT is_fully_rejected FROM tbl_bulk_units_csv WHERE csv_unit_id=csvid);
 IF isfullyrejected=1 THEN
  UPDATE tbl_bulk_units_csv SET approve_status = 4 WHERE csv_unit_id=csvid;
  Delete FROM tbl_bulk_units WHERE csv_unit_id=csvid;
 ELSE
  UPDATE tbl_bulk_units_csv SET approve_status = 4 WHERE csv_unit_id=csvid;
  Delete FROM tbl_bulk_units WHERE csv_unit_id=csvid AND action=3;
 END IF;
END //
DELIMITER ;



DROP PROCEDURE IF EXISTS `cu_update_download_count`;
DELIMITER //
CREATE PROCEDURE `cu_update_download_count`(IN `csvid` INT(11))
BEGIN
DECLARE checknull INT DEFAULT 0;

SET checknull=(SELECT rejected_file_download_count FROM tbl_bulk_units_csv  WHERE csv_unit_id=csvid);

IF(checknull IS NULL) THEN
   UPDATE tbl_bulk_units_csv SET rejected_file_download_count=1 WHERE csv_unit_id=csvid;
ELSE
  UPDATE tbl_bulk_units_csv
  SET rejected_file_download_count=rejected_file_download_count+1
  WHERE csv_unit_id=csvid;
END IF;

SELECT csv_unit_id, rejected_file_download_count
FROM tbl_bulk_units_csv
WHERE csv_unit_id=csvid;
END//
DELIMITER ;


DROP PROCEDURE IF EXISTS `sp_rejected_client_unit_data`;
DELIMITER //
CREATE PROCEDURE `sp_rejected_client_unit_data`(IN `client_group_id` INT(11), IN `user_id` INT(11))
BEGIN
SELECT DISTINCT cu.csv_unit_id,
cu_csv.uploaded_by,
cu_csv.uploaded_on,
LEFT(cu_csv.csv_name, LENGTH(cu_csv.csv_name) - LOCATE('_', REVERSE(cu_csv.csv_name))) AS csv_name,
cu_csv.total_records,
(IFNULL(cu_csv.total_rejected_records, 0) + IFNULL(cu_csv.declined_count, 0)) AS total_rejected_records,
cu_csv.approved_by,
cu_csv.rejected_by,
cu_csv.approved_on,
cu_csv.rejected_on,
cu_csv.is_fully_rejected,
(cu_csv.total_records - IFNULL(cu_csv.total_rejected_records, 0) - IFNULL(cu_csv.declined_count, 0)) AS total_approve_records,
cu_csv.rejected_file_download_count,
cu_csv.declined_count,
cu.remarks,
cu.action,
cu_csv.rejected_reason,
cu_csv.rejected_file_name
FROM tbl_bulk_units AS cu
INNER JOIN tbl_bulk_units_csv AS cu_csv ON cu_csv.csv_unit_id=cu.csv_unit_id
 WHERE
  cu_csv.client_id=client_group_id AND
  cu_csv.uploaded_by=user_id AND
  (cu.action=3 OR cu_csv.is_fully_rejected=1) -- Declined Action
  ORDER BY cu_csv.rejected_on DESC;
END//
DELIMITER ;


DROP PROCEDURE IF EXISTS `sp_delete_reject_asm_by_csvid`;
DELIMITER //
CREATE PROCEDURE `sp_delete_reject_asm_by_csvid`(IN `csvid` INT)
BEGIN
DECLARE isfullyrejected INT DEFAULT 0;
SET isfullyrejected=(SELECT is_fully_rejected FROM tbl_bulk_assign_statutory_csv WHERE csv_assign_statutory_id=csvid);
 IF isfullyrejected=1 THEN
  UPDATE tbl_bulk_assign_statutory_csv SET approve_status = 4 WHERE csv_assign_statutory_id=csvid;
  Delete FROM tbl_bulk_assign_statutory WHERE csv_assign_statutory_id=csvid;
 ELSE
  UPDATE tbl_bulk_assign_statutory_csv SET approve_status = 4 WHERE csv_assign_statutory_id=csvid;
  Delete FROM tbl_bulk_assign_statutory WHERE csv_assign_statutory_id=csvid AND action=3;
 END IF;
END //
DELIMITER ;


DROP PROCEDURE IF EXISTS `sp_rejected_assign_sm_reportdata`;
DELIMITER //
CREATE PROCEDURE `sp_rejected_assign_sm_reportdata`(
  IN `client_id` INT(11), IN `le_id` INT(11), IN `domain_id` INT(11),
  IN `unit_id` VARCHAR(100), IN `user_id` INT(11))
BEGIN
  SELECT sm.csv_assign_statutory_id,
  sm_csv.uploaded_by,
  sm_csv.uploaded_on,
  LEFT(sm_csv.csv_name, LENGTH(sm_csv.csv_name) - LOCATE('_', REVERSE(sm_csv.csv_name))) AS csv_name,
  sm_csv.total_records,
  (IFNULL(sm_csv.total_rejected_records, 0) + IFNULL(sm_csv.declined_count, 0)) AS total_rejected_records,
  sm_csv.approved_by,
  sm_csv.rejected_by,
  sm_csv.approved_on,
  sm_csv.rejected_on,
  sm_csv.is_fully_rejected,
  sm_csv.approve_status,
  sm_csv.rejected_file_download_count,
  sm.remarks,
  sm.action,
  sm_csv.declined_count,
  sm_csv.rejected_reason,
  (sm_csv.total_records - IFNULL(sm_csv.total_rejected_records, 0) - IFNULL(sm_csv.declined_count, 0)) AS total_approve_records
  FROM tbl_bulk_assign_statutory AS sm
  INNER JOIN tbl_bulk_assign_statutory_csv AS sm_csv ON sm_csv.csv_assign_statutory_id = sm.csv_assign_statutory_id
   WHERE
    sm_csv.client_id=client_id AND
    sm_csv.legal_entity_id=le_id AND
    sm_csv.uploaded_by=user_id AND
    (sm.action=3 OR sm_csv.is_fully_rejected=1) AND
    IF(domain_id > 0, FIND_IN_SET(domain_id, sm_csv.domain_ids), 1)
    AND
    IF(unit_id != '', sm.unit_code=unit_id, 1)
    Group by sm.csv_assign_statutory_id,
    sm_csv.uploaded_by,
    sm_csv.uploaded_on,
    sm_csv.csv_name,
    sm_csv.total_records,
    sm_csv.approved_by,
    sm_csv.rejected_by,
    sm_csv.approved_on,
    sm_csv.rejected_on,
    sm_csv.is_fully_rejected,
    sm_csv.approve_status,
    sm_csv.rejected_file_download_count,
    sm.remarks,
    sm.action,
    sm_csv.declined_count,
    sm_csv.rejected_reason,
    sm_csv.total_records, sm_csv.total_rejected_records,sm_csv.declined_count
    ORDER BY sm_csv.rejected_on, sm_csv.approved_on DESC;
END//
DELIMITER ;


DROP PROCEDURE IF EXISTS `sp_update_asm_download_count`;
DELIMITER //
CREATE PROCEDURE `sp_update_asm_download_count`(IN `csvid` INT(11))
BEGIN
  DECLARE checknull INT DEFAULT 0;

  SET checknull=(SELECT rejected_file_download_count FROM tbl_bulk_assign_statutory_csv  WHERE csv_assign_statutory_id=csvid);

  IF(checknull IS NULL) THEN
     UPDATE tbl_bulk_assign_statutory_csv SET rejected_file_download_count=1 WHERE csv_assign_statutory_id=csvid;
  ELSE
    UPDATE tbl_bulk_assign_statutory_csv
    SET rejected_file_download_count=rejected_file_download_count+1
    WHERE csv_assign_statutory_id=csvid;
  END IF;

  SELECT csv_assign_statutory_id, rejected_file_download_count
  FROM tbl_bulk_assign_statutory_csv
  WHERE csv_assign_statutory_id=csvid;
END //
DELIMITER ;


DROP PROCEDURE IF EXISTS `sp_export_statutory_mappings_bulk_reportdata`;
DELIMITER //
CREATE PROCEDURE `sp_export_statutory_mappings_bulk_reportdata`(
    IN `user_ids` VARCHAR(100),
    IN `country_ids` VARCHAR(100),
    IN `domain_ids` VARCHAR(100),
    IN `FROM_date` DATE,
    IN `to_date` DATE)
BEGIN
 SELECT
  tbl_bsm_csv.csv_id,
  tbl_bsm_csv.country_name,
  tbl_bsm_csv.domain_name,
  tbl_bsm_csv.uploaded_by,
  tbl_bsm_csv.uploaded_on,
  LEFT(tbl_bsm_csv.csv_name, LENGTH(tbl_bsm_csv.csv_name) - LOCATE('_', REVERSE(tbl_bsm_csv.csv_name))) AS csv_name,
  tbl_bsm_csv.total_records,
  (IFNULL(tbl_bsm_csv.total_rejected_records, 0) + IFNULL(tbl_bsm_csv.declined_count, 0)) AS total_rejected_records,
  tbl_bsm_csv.approved_by,
  tbl_bsm_csv.rejected_by,
  tbl_bsm_csv.approved_on,
  tbl_bsm_csv.rejected_on,
  tbl_bsm_csv.is_fully_rejected,
  (tbl_bsm_csv.total_records - IFNULL(tbl_bsm_csv.total_rejected_records, 0) - IFNULL(tbl_bsm_csv.declined_count, 0)) AS total_approve_records,
  tbl_bsm_csv.rejected_reason,
  tbl_bsm_csv.declined_count
FROM tbl_bulk_statutory_mapping_csv AS tbl_bsm_csv
WHERE
  tbl_bsm_csv.approve_status>0 AND
  FIND_IN_SET(tbl_bsm_csv.uploaded_by, user_ids)
  AND (DATE_FORMAT(DATE(tbl_bsm_csv.uploaded_on),"%Y-%m-%d") BETWEEN DATE(from_date) AND DATE(to_date))
  AND FIND_IN_SET(tbl_bsm_csv.domain_id, domain_ids)
  AND FIND_IN_SET(tbl_bsm_csv.country_id, country_ids)
  ORDER BY tbl_bsm_csv.uploaded_on DESC;

SELECT COUNT(DISTINCT tbl_bsm_csv.csv_id) AS total
FROM tbl_bulk_statutory_mapping_csv AS tbl_bsm_csv
 WHERE
  tbl_bsm_csv.approve_status>0 AND
  FIND_IN_SET(tbl_bsm_csv.uploaded_by, user_ids)
  AND (DATE_FORMAT(DATE(tbl_bsm_csv.uploaded_on),"%Y-%m-%d") BETWEEN DATE(from_date) AND DATE(to_date))
  AND FIND_IN_SET(tbl_bsm_csv.domain_id, domain_ids)
  AND FIND_IN_SET(tbl_bsm_csv.country_id, country_ids)
  ORDER BY tbl_bsm_csv.uploaded_on DESC;
END //
DELIMITER ;


DROP PROCEDURE IF EXISTS `sp_export_client_unit_bulk_reportdata`;
DELIMITER //
CREATE PROCEDURE `sp_export_client_unit_bulk_reportdata`(IN `client_group_id` INT(11),
  IN `FROM_date` DATE, IN `to_date` DATE, IN `user_ids` VARCHAR(100))
BEGIN
SELECT
  t1.csv_unit_id,
  t1.uploaded_by,
  t1.uploaded_on,
  LEFT(t1.csv_name, LENGTH(t1.csv_name) - LOCATE('_', REVERSE(t1.csv_name))) AS csv_name,
  t1.total_records,
  IFNULL(t1.total_rejected_records, 0) AS total_rejected_records,
  t1.approved_by,
  t1.rejected_by,
  t1.approved_on,
  t1.rejected_on,
  t1.is_fully_rejected,
  t1.approve_status,
  t1.rejected_reason,
  (t1.total_records - IFNULL(t1.total_rejected_records, 0) - IFNULL(t1.declined_count, 0)) AS total_approve_records,
  t1.declined_count
FROM tbl_bulk_units_csv AS t1
WHERE
  t1.approve_status>0 AND
  FIND_IN_SET(t1.uploaded_by, user_ids) AND
  t1.client_id = client_group_id AND
  (DATE_FORMAT(DATE(t1.uploaded_on),"%Y-%m-%d")
BETWEEN DATE(from_date) AND DATE(to_date))
ORDER BY t1.uploaded_on DESC;

SELECT COUNT(DISTINCT t1.csv_unit_id) AS total
FROM tbl_bulk_units_csv AS t1
WHERE
  t1.approve_status>0 AND
  FIND_IN_SET(t1.uploaded_by, user_ids) AND
  t1.client_id = client_group_id AND
  (DATE_FORMAT(DATE(t1.uploaded_on),"%Y-%m-%d")
BETWEEN DATE(from_date) AND DATE(to_date))
ORDER BY t1.uploaded_on DESC;

END //
DELIMITER ;


DELIMITER ;
DROP PROCEDURE IF EXISTS `sp_export_assigned_statutory_bulk_reportdata`;
DELIMITER //
CREATE PROCEDURE `sp_export_assigned_statutory_bulk_reportdata`(
  IN `client_group_id` INT(11),
  IN `legal_entity_id` INT(11),
  IN `unit_id` VARCHAR(100),
  IN `from_date` DATE,
  IN `to_date` DATE,
  IN `user_ids` VARCHAR(100),
  IN `domain_id` VARCHAR(50))
BEGIN

DROP TEMPORARY TABLE IF EXISTS my_temp_table;
  Call split_comma (domain_id);

  SELECT t1.csv_assign_statutory_id, t1.domain_names,
    t1.uploaded_by,
    t1.uploaded_on,
    LEFT(t1.csv_name, LENGTH(t1.csv_name) - LOCATE('_', REVERSE(t1.csv_name))) AS csv_name,
    t1.total_records,
    (IFNULL(t1.total_rejected_records, 0) + IFNULL(t1.declined_count, 0)) AS total_rejected_records,
    t1.approved_by,
    t1.rejected_by,
    t1.approved_on,
    t1.rejected_on,
    t1.is_fully_rejected,
    (t1.total_records - IFNULL(t1.total_rejected_records, 0) - IFNULL(t1.declined_count, 0)) AS total_approve_records,
    t1.approve_status,
    t1.rejected_reason,
    t1.declined_count
  FROM tbl_bulk_assign_statutory_csv AS t1
  INNER JOIN my_temp_table t3 ON t1.domain_ids = t3.comma_stuff
  WHERE
  t1.approve_status>0 AND
  t1.client_id = client_group_id AND
  t1.legal_entity_id = legal_entity_id AND
  FIND_IN_SET(t1.uploaded_by, user_ids) AND
  (DATE_FORMAT(DATE(t1.uploaded_on),"%Y-%m-%d") BETWEEN DATE(from_date) AND DATE(to_date))
  ORDER BY t1.uploaded_on DESC;

  SELECT COUNT(t1.csv_assign_statutory_id) AS total
  FROM tbl_bulk_assign_statutory_csv AS t1
  INNER JOIN my_temp_table t3 ON t1.domain_ids = t3.comma_stuff
  WHERE
  t1.approve_status>0 AND
  t1.client_id = client_group_id AND
  t1.legal_entity_id = legal_entity_id AND
  FIND_IN_SET(t1.uploaded_by, user_ids) AND
  (DATE_FORMAT(DATE(t1.uploaded_on),"%Y-%m-%d") BETWEEN DATE(from_date) AND DATE(to_date))
  ORDER BY t1.uploaded_on DESC;

  DELETE FROM my_temp_table;
END //
DELIMITER ;


DROP PROCEDURE IF EXISTS `sp_rejected_asm_csv_report`;
DELIMITER //
CREATE PROCEDURE `sp_rejected_asm_csv_report`(
  IN `client_id` INT(11),
  IN `le_id` INT(11),
  IN `d_id` INT(11),
  IN `unit_id` VARCHAR(100),
  IN `csv_id` INT(11),
  IN `user_id` INT(11))
BEGIN

IF(unit_id!='') THEN

  SELECT
   asm.client_group,
   asm.legal_entity,
   asm.domain,
   asm.organization,
   asm.unit_code,
   asm.unit_name,
   asm.unit_location,
   asm.perimary_legislation,
   asm.secondary_legislation,
   asm.statutory_provision,
   asm.compliance_task_name,
   asm.compliance_description,
   (CASE WHEN asm.statutory_applicable_status = 1 THEN 'Applicable'
         WHEN asm.statutory_applicable_status = 2 THEN 'Not Applicable'
         WHEN asm.statutory_applicable_status = 3 THEN 'Do Not Show'
    END) AS statutory_applicable_status,
   asm.statytory_remarks,
   (CASE WHEN asm.compliance_applicable_status = 1 THEN 'Applicable'
         WHEN asm.compliance_applicable_status = 2 THEN 'Not Applicable'
         WHEN asm.compliance_applicable_status = 3 THEN 'Do Not Show'
    END) AS compliance_applicable_status,
   asm.remarks,
   (CASE WHEN asm_csv.is_fully_rejected = 1 THEN asm_csv.rejected_reason ELSE '' END) AS rejected_reason,
   asm_csv.is_fully_rejected
  FROM tbl_bulk_assign_statutory AS asm
  INNER JOIN tbl_bulk_assign_statutory_csv AS asm_csv ON asm_csv.csv_assign_statutory_id=asm.csv_assign_statutory_id
   WHERE
    FIND_IN_SET(d_id, asm_csv.domain_ids) AND
    asm_csv.client_id=client_id AND
    asm_csv.legal_entity_id=le_id AND
    asm.unit_code=unit_id AND
    asm_csv.uploaded_by=user_id AND
    asm.csv_assign_statutory_id=csv_id AND
    (asm.action=3 OR asm_csv.is_fully_rejected=1)
    ORDER BY asm_csv.rejected_on, asm_csv.approved_on DESC;
ELSE
  SELECT
   asm.client_group,
   asm.legal_entity,
   asm.domain,
   asm.organization,
   asm.unit_code,
   asm.unit_name,
   asm.unit_location,
   asm.perimary_legislation,
   asm.secondary_legislation,
   asm.statutory_provision,
   asm.compliance_task_name,
   asm.compliance_description,
   (CASE WHEN asm.statutory_applicable_status = 1 THEN 'Applicable'
         WHEN asm.statutory_applicable_status = 2 THEN 'Not Applicable'
         WHEN asm.statutory_applicable_status = 3 THEN 'Do Not Show'
    END) AS statutory_applicable_status,
   asm.statytory_remarks,
   (CASE WHEN asm.compliance_applicable_status = 1 THEN 'Applicable'
         WHEN asm.compliance_applicable_status = 2 THEN 'Not Applicable'
         WHEN asm.compliance_applicable_status = 3 THEN 'Do Not Show'
    END) AS compliance_applicable_status,
   asm_csv.rejected_reason,
   asm.remarks,
   (CASE WHEN asm_csv.is_fully_rejected = 1 THEN asm_csv.rejected_reason ELSE '' END) AS rejected_reason,
   asm_csv.is_fully_rejected
  FROM tbl_bulk_assign_statutory AS asm
  INNER JOIN tbl_bulk_assign_statutory_csv AS asm_csv ON asm_csv.csv_assign_statutory_id=asm.csv_assign_statutory_id
   WHERE
    FIND_IN_SET(d_id, asm_csv.domain_ids) AND
    asm_csv.client_id=client_id AND
    asm_csv.legal_entity_id=le_id AND
    asm_csv.uploaded_by=user_id AND
    asm.csv_assign_statutory_id=csv_id AND
    (asm.action=3 OR asm_csv.is_fully_rejected=1)
    ORDER BY asm_csv.rejected_on, asm_csv.approved_on DESC;
  END IF;
END //
DELIMITER ;


DROP PROCEDURE IF EXISTS `sp_rejected_cu_csv_report`;
DELIMITER //
CREATE PROCEDURE `sp_rejected_cu_csv_report`(IN `cg_id` INT(11), IN `csv_id` INT(11), IN `user_id` INT(11))
BEGIN
 SELECT
  u.legal_entity,
  u.division,
  u.category,
  u.geography_level,
  u.unit_location,
  u.unit_code,
  u.unit_name,
  u.address,
  u.city,
  u.state,
  u.postalcode,
  u.domain,
  u.organization,
  u_csv.rejected_reason,
  u.remarks,
  (CASE WHEN u_csv.is_fully_rejected = 1 THEN u_csv.rejected_reason ELSE '' END) AS rejected_reason,
  u_csv.is_fully_rejected
FROM tbl_bulk_units AS u
INNER JOIN tbl_bulk_units_csv AS u_csv ON u_csv.csv_unit_id=u.csv_unit_id
 WHERE
  u_csv.client_id=cg_id AND
  u_csv.uploaded_by=user_id AND
  u.csv_unit_id=csv_id AND
  (u.action=3 OR u_csv.is_fully_rejected=1)
  ORDER BY u_csv.uploaded_on DESC;
END //
DELIMITER ;


DROP PROCEDURE IF EXISTS `sp_rejected_sm_csv_report`;
DELIMITER //
CREATE PROCEDURE `sp_rejected_sm_csv_report`(
  IN `country_id` INT(11),
  IN `domain_id` INT(11),
  IN `user_id` INT(11),
  IN `csv_id` INT(11))
BEGIN

SELECT
  sm.organization,
  sm.geography_location,
  sm.statutory_nature,
  sm.statutory,
  sm.statutory_provision,
  sm.compliance_task,
  sm.compliance_document,
  sm.task_id,
  sm.compliance_description,
  sm.penal_consequences,
  sm.task_Type,
  sm.reference_link,
  sm.compliance_frequency,
  sm.statutory_month,
  sm.statutory_date,
  sm.trigger_before,
  sm.repeats_every,
  sm.repeats_type,
  sm.repeat_by,
  sm.duration,
  sm.duration_type,
  sm.multiple_input,
  sm.format_file,
  sm.remarks,
  (CASE WHEN sm_csv.is_fully_rejected = 1 THEN sm_csv.rejected_reason ELSE '' END) AS rejected_reason,
  sm_csv.is_fully_rejected
FROM tbl_bulk_statutory_mapping AS sm
INNER JOIN tbl_bulk_statutory_mapping_csv AS sm_csv ON sm_csv.csv_id=sm.csv_id
WHERE
  sm_csv.country_id=country_id AND
  sm_csv.domain_id=domain_id AND
  sm_csv.uploaded_by=user_id AND
  sm.csv_id=csv_id AND
  (sm.action=3 OR sm_csv.is_fully_rejected=1)
  ORDER BY sm_csv.rejected_on, sm_csv.approved_on DESC;
END //
DELIMITER ;


DROP PROCEDURE IF EXISTS `sp_get_cu_csv_file_name_by_id`;
DELIMITER //
CREATE PROCEDURE `sp_get_cu_csv_file_name_by_id`(IN `CSV_FILE_ID` INT(11))
BEGIN
  SELECT csv_name FROM tbl_bulk_units_csv WHERE csv_unit_id=CSV_FILE_ID;
END //
DELIMITER ;


DROP PROCEDURE IF EXISTS `sp_get_sm_csv_file_name_by_id`;
DELIMITER //
CREATE PROCEDURE `sp_get_sm_csv_file_name_by_id`(IN `CSV_FILE_ID` INT(11))
BEGIN
  SELECT csv_name FROM tbl_bulk_statutory_mapping_csv WHERE csv_id=CSV_FILE_ID;
END //
DELIMITER ;


DROP PROCEDURE IF EXISTS `sp_get_asm_csv_file_name_by_id`;
DELIMITER //
CREATE PROCEDURE `sp_get_asm_csv_file_name_by_id`(IN `CSV_FILE_ID` INT(11))
BEGIN
SELECT csv_name FROM tbl_bulk_assign_statutory_csv WHERE csv_assign_statutory_id=CSV_FILE_ID;
END //
DELIMITER ;


DROP PROCEDURE IF EXISTS `sp_assign_statutory_filter_list`;
DELIMITER //
CREATE PROCEDURE `sp_assign_statutory_filter_list`(
IN csvid INT
)
BEGIN
    SELECT distinct domain FROM tbl_bulk_assign_statutory WHERE csv_assign_statutory_id = csvid;

    SELECT distinct CONCAT(unit_code,' - ',unit_name) AS unit_name FROM tbl_bulk_assign_statutory WHERE csv_assign_statutory_id = csvid;

    SELECT distinct perimary_legislation FROM tbl_bulk_assign_statutory WHERE csv_assign_statutory_id = csvid;

    SELECT distinct secondary_legislation FROM tbl_bulk_assign_statutory WHERE csv_assign_statutory_id = csvid;

    SELECT distinct statutory_provision FROM tbl_bulk_assign_statutory WHERE csv_assign_statutory_id = csvid;

    SELECT distinct compliance_task_name FROM tbl_bulk_assign_statutory WHERE csv_assign_statutory_id = csvid;

    SELECT distinct compliance_description FROM tbl_bulk_assign_statutory WHERE csv_assign_statutory_id = csvid;
END //
DELIMITER ;


-- --------------------------------------------------------------------------------
-- To get the details of units under client id to check for duplication
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_groups_client_units_list`;
DELIMITER //
CREATE PROCEDURE `sp_groups_client_units_list`(
  IN _ClientId INT)
BEGIN
  SELECT t2.legal_entity, t2.unit_code, t2.domain, t2.organization
  FROM tbl_bulk_units_csv AS t1 INNER JOIN tbl_bulk_units AS t2
  ON t2.csv_unit_id = t1.csv_unit_id
  WHERE t1.client_id = _ClientId;
END //
DELIMITER ;


DROP PROCEDURE IF EXISTS `sp_assign_statutory_view_by_csvid`;
DELIMITER //
CREATE PROCEDURE `sp_assign_statutory_view_by_csvid`(
IN csvid INT, f_count INT, f_range INT
)
BEGIN
    SELECT t1.csv_assign_statutory_id, t1.csv_name, t1.legal_entity,
    t1.client_id,  t1.uploaded_by,
    DATE_FORMAT(t1.uploaded_on, '%d-%b-%Y %h:%i') AS uploaded_on,
    t2.bulk_assign_statutory_id,
    t2.unit_code, t2.unit_name, t2.unit_location,
    t2.domain, t2.organization, t2.perimary_legislation,
    t2.secondary_legislation, t2.statutory_provision,
    t2.compliance_task_name, t2.compliance_description,
    t2.statutory_applicable_status, t2.statytory_remarks, t2.compliance_applicable_status,
    t2.remarks, t2.action
    FROM tbl_bulk_assign_statutory_csv AS t1
    INNER JOIN tbl_bulk_assign_statutory AS t2 ON
    t1.csv_assign_statutory_id  = t2.csv_assign_statutory_id WHERE t1.csv_assign_statutory_id = csvid
    LIMIT f_count, f_range;
END //
DELIMITER ;


DROP PROCEDURE IF EXISTS `sp_assign_statutory_view_by_filter`;
DELIMITER //
CREATE PROCEDURE `sp_assign_statutory_view_by_filter`(
    IN csvid INT, domain_name TEXT, unit_name TEXT,
    p_legis TEXT, s_legis VARCHAR(200), s_prov VARCHAR(500),
    c_task VARCHAR(100), c_desc VARCHAR(500), f_count INT, f_range INT,
    view_data INT, s_status INT, c_status INT
)
BEGIN

    SELECT t1.csv_assign_statutory_id, t1.csv_name, t1.legal_entity,
    t1.client_id,  t1.uploaded_by,
    DATE_FORMAT(t1.uploaded_on, '%d-%b-%Y %h:%i') AS uploaded_on,
    (SELECT distinct client_group FROM tbl_bulk_assign_statutory
      WHERE csv_assign_statutory_id = t1.csv_assign_statutory_id) AS client_group
    FROM tbl_bulk_assign_statutory_csv AS t1
    WHERE t1.csv_assign_statutory_id = csvid;

    SELECT COUNT(t1.csv_assign_statutory_id) AS total_count
    FROM tbl_bulk_assign_statutory_csv AS t1
    INNER JOIN tbl_bulk_assign_statutory AS t2 ON
    t1.csv_assign_statutory_id  = t2.csv_assign_statutory_id WHERE t1.csv_assign_statutory_id = csvid
    AND IF(domain_name IS NOT NULL, FIND_IN_SET(t2.domain, domain_name), 1)
    AND IF(unit_name IS NOT NULL, FIND_IN_SET(t2.unit_code, unit_name), 1)
    AND IF(p_legis IS NOT NULL, FIND_IN_SET(REPLACE(t2.perimary_legislation, ',', '|'), p_legis), 1)
    AND IF(s_legis IS NOT NULL, t2.secondary_legislation = s_legis, 1)
    AND IF(s_prov IS NOT NULL, t2.statutory_provision = s_prov, 1)
    AND IF(c_task IS NOT NULL, t2.compliance_task_name = c_task, 1)
    AND IF(c_desc IS NOT NULL, t2.compliance_description = c_desc, 1)
    AND IF(view_data IS NULL, 1,
      IF(view_data = 0, t2.action IS NULL, t2.action IS NOT NULL)
    )
    AND IF(s_status IS NOT NULL, t2.statutory_applicable_status = s_status, 1)
    AND IF(c_status IS NOT NULL, t2.compliance_applicable_status = c_status, 1);

    SELECT t2.bulk_assign_statutory_id,
    t2.unit_code, t2.unit_name, t2.unit_location,
    t2.domain, t2.organization, t2.perimary_legislation,
    t2.secondary_legislation, t2.statutory_provision,
    t2.compliance_task_name, t2.compliance_description,
    t2.statutory_applicable_status, t2.statytory_remarks, t2.compliance_applicable_status,
    t2.remarks, t2.action
    FROM tbl_bulk_assign_statutory_csv AS t1
    INNER JOIN tbl_bulk_assign_statutory AS t2 ON
    t1.csv_assign_statutory_id  = t2.csv_assign_statutory_id WHERE t1.csv_assign_statutory_id = csvid
    AND IF(domain_name IS NOT NULL, FIND_IN_SET(t2.domain, domain_name), 1)
    AND IF(unit_name IS NOT NULL, FIND_IN_SET(t2.unit_code, unit_name), 1)
    AND IF(p_legis IS NOT NULL, FIND_IN_SET(REPLACE(t2.perimary_legislation, ',', '|'), p_legis), 1)
    AND IF(s_legis IS NOT NULL, t2.secondary_legislation = s_legis, 1)
    AND IF(s_prov IS NOT NULL, t2.statutory_provision = s_prov, 1)
    AND IF(c_task IS NOT NULL, t2.compliance_task_name = c_task, 1)
    AND IF(c_desc IS NOT NULL, t2.compliance_description = c_desc, 1)
    AND IF(view_data IS NULL, 1,
      IF(view_data = 0, t2.action IS NULL, t2.action IS NOT NULL)
    )
    AND IF(s_status IS NOT NULL, t2.statutory_applicable_status = s_status, 1)
    AND IF(c_status IS NOT NULL, t2.compliance_applicable_status = c_status, 1)
    LIMIT f_count, f_range;
END //


DELIMITER ;
DROP PROCEDURE IF EXISTS `sp_assign_statutory_by_csvid`;
DELIMITER //
CREATE PROCEDURE `sp_assign_statutory_by_csvid`(
IN csvid INT
)
BEGIN
    SELECT
    t2.csv_assign_statutory_id,
    t2.bulk_assign_statutory_id,
    t2.legal_entity AS Legal_Entity, t2.client_group AS Client_Group,
    t1.csv_name AS Csv_Name, t2.domain AS Domain, t2.organization AS Organization,
    t2.unit_code AS Unit_Code, t2.unit_name AS Unit_Name, t2.unit_location AS Unit_Location,
    t2.perimary_legislation AS Primary_Legislation, t2.secondary_legislation AS Secondary_Legislation,
    t2.statutory_provision AS Statutory_Provision,
    t2.compliance_task_name AS Compliance_Task, t2.compliance_description AS Compliance_Description,
    t2.statutory_applicable_status AS Statutory_Applicable_Status, t2.statytory_remarks AS Statutory_remarks,
    t2.compliance_applicable_status AS Compliance_Applicable_Status,
    t2.remarks, t2.action, t1.uploaded_by, t1.uploaded_on
    FROM tbl_bulk_assign_statutory AS t2
    INNER join tbl_bulk_assign_statutory_csv AS t1
    ON t1.csv_assign_statutory_id = t2.csv_assign_statutory_id
    WHERE (t2.action IS null or t2.action != 3) AND t2.csv_assign_statutory_id = csvid;
END //
DELIMITER ;


DROP PROCEDURE IF EXISTS `sp_assign_statutory_update_all_action`;
DELIMITER //
CREATE PROCEDURE `sp_assign_statutory_update_all_action`(
IN csvid INT, action INT, _remarks VARCHAR(500),
userid INT)
BEGIN
    IF action = 2 THEN
        UPDATE tbl_bulk_assign_statutory SET
        action = 2, remarks = _remarks
        WHERE csv_assign_statutory_id = csvid;

        UPDATE tbl_bulk_assign_statutory_csv SET
        approve_status = 2,
        rejected_reason = _remarks, is_fully_rejected = 1,
        rejected_by = userid,
        rejected_on = current_ist_datetime(),
        total_rejected_records = (SELECT COUNT(0) FROM
        tbl_bulk_assign_statutory AS t WHERE t.csv_assign_statutory_id = csvid)
        WHERE csv_assign_statutory_id = csvid;
    ELSE
        UPDATE tbl_bulk_assign_statutory SET
        action = 1, remarks = _remarks
        WHERE csv_assign_statutory_id = csvid;

        UPDATE tbl_bulk_assign_statutory_csv SET
        approve_status = 1, approved_on = current_ist_datetime(),
        approved_by = userid, is_fully_rejected = 0
        WHERE csv_assign_statutory_id = csvid;
    END IF;
END//
DELIMITER ;


-- --------------------------------------------------------------------------------
-- To get domain organization count created in temp db
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_get_domain_organization_count`;
DELIMITER //
CREATE PROCEDURE `sp_get_domain_organization_count`(
  IN _ClientID INT(11))
BEGIN
  SELECT t2.legal_entity, t2.domain, t2.organization,
  COUNT(t2.bulk_unit_id) AS saved_units
  FROM tbl_bulk_units_csv AS t1 INNER JOIN tbl_bulk_units AS t2
  ON t2.csv_unit_id = t1.csv_unit_id
  WHERE t1.client_id = _ClientId
  GROUP BY t2.legal_entity, t2.domain, t2.organization;
END//
DELIMITER ;


-- --------------------------------------------------------------------------------
-- To get the CSV uploaded bulk client units under the file id
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_bulk_client_unit_by_csvid`;
DELIMITER //
CREATE PROCEDURE `sp_bulk_client_unit_by_csvid`(
    IN _csv_id INT)
BEGIN
    SELECT t1.client_id, t1.client_group, t2.bulk_unit_id,
    t2.legal_entity AS Legal_Entity, t2.division AS Division,
    t2.category AS Category, t2.geography_level AS Geography_Level,
    t2.unit_location AS Unit_Location, t2.unit_code AS Unit_Code,
    t2.unit_name AS Unit_Name, t2.address AS Unit_Address,
    t2.city AS City, t2.state AS State, t2.postalcode AS Postal_Code,
    t2.domain AS Domain, t2.organization AS Organization,
    t1.uploaded_by, t1.csv_name, t2.action, t2.remarks
    FROM tbl_bulk_units_csv AS t1 INNER JOIN tbl_bulk_units AS t2
    ON t2.csv_unit_id = t1.csv_unit_id
    WHERE t1.csv_unit_id = _csv_id;
END //
DELIMITER ;


DROP PROCEDURE IF EXISTS `sp_approve_assign_statutory_action_save`;
DELIMITER //
CREATE PROCEDURE `sp_approve_assign_statutory_action_save`(
IN csvid INT, asid INT, buaction INT, buremarks VARCHAR(500)
)
BEGIN
    UPDATE tbl_bulk_assign_statutory SET action = buaction,
    remarks = buremarks WHERE csv_assign_statutory_id = csvid AND
    bulk_assign_statutory_id = asid;
END //
DELIMITER ;


-- --------------------------------------------------------------------------------
-- To update approve status/ reject status during approve all OR reject all
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_bulk_client_unit_update_action`;
DELIMITER //
CREATE PROCEDURE `sp_bulk_client_unit_update_action`(
    IN _csv_unit_id INT, _action TINYINT, _remarks TEXT, _user_id INT,
  _declinedCount INT)
BEGIN
    IF _action = 2 THEN
        UPDATE tbl_bulk_units SET
        action = 2, remarks = _remarks
        WHERE csv_unit_id = _csv_unit_id;

        UPDATE tbl_bulk_units_csv SET
        is_fully_rejected = 1,
        approve_status = 2,
        rejected_by = _user_id,
        rejected_on = current_ist_datetime(),
        rejected_reason = _remarks,
        total_rejected_records = (SELECT COUNT(0) FROM
        tbl_bulk_units AS t1 WHERE t1.csv_unit_id = _csv_unit_id)
        WHERE csv_unit_id = _csv_unit_id;
    ELSEIF _action = 1 THEN
    IF _declinedCount = 0 THEN
      DELETE FROM tbl_bulk_units
      WHERE csv_unit_id = _csv_unit_id
      AND (action = 1 OR action = 0);
    ELSE
      UPDATE tbl_bulk_units SET
      action = 1 WHERE csv_unit_id = _csv_unit_id;
    END IF;

      UPDATE tbl_bulk_units_csv SET
        approve_status = 1, approved_on = current_ist_datetime(),
        approved_by = _user_id, is_fully_rejected = 0,
        declined_count = _declinedCount,
        total_rejected_records = (SELECT COUNT(0) FROM
        tbl_bulk_units AS t1 WHERE t1.csv_unit_id = _csv_unit_id
      AND action = 2)
      WHERE csv_unit_id = _csv_unit_id;
  ELSEIF _action = 4 THEN
        UPDATE tbl_bulk_units_csv SET
        approve_status = 1, approved_on = current_ist_datetime(),
        approved_by = _user_id, is_fully_rejected = 0,
    declined_count = _declinedCount,
    total_rejected_records = (SELECT COUNT(0) FROM
    tbl_bulk_units AS t1 WHERE t1.csv_unit_id = _csv_unit_id
    AND action = 2)
        WHERE csv_unit_id = _csv_unit_id;

    IF _declinedCount = 0 THEN
      DELETE FROM tbl_bulk_units
      WHERE csv_unit_id = _csv_unit_id;
    END IF;
  END IF;
END //
DELIMITER ;


-- --------------------------------------------------------------------------------
-- To get the uploaded client units bulk data of a csv file for view
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_bulk_client_unit_view_by_csvid`;
DELIMITER //
CREATE PROCEDURE `sp_bulk_client_unit_view_by_csvid`(
    IN _csv_unit_id INT, f_count INT, f_range INT)
BEGIN
    SELECT t1.client_id, t1.client_group, t2.bulk_unit_id,
    t2.legal_entity, t2.division, t2.category,
    t2.geography_level, t2.unit_location, t2.unit_code,
    t2.unit_name, t2.address, t2.city, t2.state,
    t2.postalcode, t2.domain, t2.organization,
    t1.uploaded_by, t1.csv_name, t1.csv_unit_id, t1.uploaded_on,
    t2.action, t2.remarks, t1.total_records
    FROM tbl_bulk_units_csv AS t1 INNER JOIN tbl_bulk_units AS t2
    ON t2.csv_unit_id = t1.csv_unit_id
    WHERE t1.csv_unit_id = _csv_unit_id
    LIMIT f_count, f_range;
END //
DELIMITER ;


-- --------------------------------------------------------------------------------
-- To get sets of data for approve client unit - bulk - filter action
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_bulk_client_unit_filter_data`;
DELIMITER //
CREATE PROCEDURE `sp_bulk_client_unit_filter_data`(
    IN _csv_unit_id INT)
BEGIN
    SELECT DISTINCT legal_entity FROM tbl_bulk_units WHERE csv_unit_id = _csv_unit_id;

    SELECT DISTINCT division FROM tbl_bulk_units WHERE csv_unit_id = _csv_unit_id;

    SELECT DISTINCT category FROM tbl_bulk_units WHERE csv_unit_id = _csv_unit_id;

    SELECT DISTINCT unit_location FROM tbl_bulk_units WHERE csv_unit_id = _csv_unit_id;

    SELECT unit_code FROM tbl_bulk_units WHERE csv_unit_id = _csv_unit_id;

    SELECT DISTINCT domain FROM tbl_bulk_units WHERE csv_unit_id = _csv_unit_id;

    SELECT DISTINCT organization FROM tbl_bulk_units WHERE csv_unit_id = _csv_unit_id;
END //
DELIMITER ;


-- --------------------------------------------------------------------------------
-- To fetch records AS per the filter
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_bulk_client_unit_view_by_filter`;
DELIMITER //
CREATE PROCEDURE `sp_bulk_client_unit_view_by_filter`(
    IN _csv_unit_id INT, _le_name VARCHAR(50),
    _div_name VARCHAR(50), _cg_name VARCHAR(50),
    _u_location VARCHAR(200), _u_code VARCHAR(50),
    _domain VARCHAR(200), _orgn VARCHAR(500), _action INT,
    _f_count INT, _f_LIMIT INT
)
BEGIN
    SELECT t1.client_id, t1.client_group, t2.bulk_unit_id,
    t2.legal_entity, t2.division, t2.category,
    t2.geography_level, t2.unit_location, t2.unit_code,
    t2.unit_name, t2.address, t2.city, t2.state,
    t2.postalcode, t2.domain, t2.organization,
    t1.uploaded_by, t1.csv_name, t1.csv_unit_id, t1.uploaded_on,
    t2.action, t2.remarks
    FROM tbl_bulk_units_csv AS t1 INNER JOIN tbl_bulk_units AS t2
    ON t2.csv_unit_id = t1.csv_unit_id WHERE t1.csv_unit_id = _csv_unit_id
    AND legal_entity LIKE legal_entity AND division LIKE _div_name AND
    category LIKE _cg_name AND unit_location LIKE _u_location AND
    unit_code LIKE _u_code AND domain LIKE concat('%',_domain,'%') AND
    organization LIKE concat('%',_orgn,'%') AND
    CASE WHEN _action = 1 THEN
      action = 0
    WHEN _action = 2 THEN
      action != 0
    ELSE
      action >= 0
    END
    LIMIT _f_count, _f_limit;

  SELECT COUNT(distinct t2.bulk_unit_id) AS total_records
    FROM tbl_bulk_units_csv AS t1 INNER JOIN tbl_bulk_units AS t2
    ON t2.csv_unit_id = t1.csv_unit_id WHERE t1.csv_unit_id = _csv_unit_id
    AND legal_entity LIKE legal_entity AND division LIKE _div_name AND
    category LIKE _cg_name AND unit_location LIKE _u_location AND
    unit_code LIKE _u_code AND domain LIKE concat('%',_domain,'%') AND
    organization LIKE concat('%',_orgn,'%') AND
    CASE WHEN _action = 1 THEN
      action = 0
    WHEN _action = 2 THEN
      action != 0
    ELSE
      action >= 0
    END;
END //
DELIMITER ;


-- --------------------------------------------------------------------------------
-- To save approve / reject of each unit in view
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_bulk_client_unit_id_save`;
DELIMITER //
CREATE PROCEDURE `sp_bulk_client_unit_id_save`(
    IN _csv_unit_id INT, _bu_unit_id INT, _action INT,
    _remarks VARCHAR(500)
)
BEGIN
    UPDATE tbl_bulk_units SET action = _action,
    remarks = _remarks WHERE csv_unit_id = _csv_unit_id AND
    bulk_unit_id = _bu_unit_id;
END //
DELIMITER ;


-- --------------------------------------------------------------------------------
-- To get the count of units which has action AS 0 OR null
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_bulk_client_unit_action_count`;
DELIMITER //
CREATE PROCEDURE `sp_bulk_client_unit_action_count`(
    IN _csv_unit_id INT)
BEGIN
    SELECT COUNT(*) AS null_action_count FROM tbl_bulk_units
    WHERE csv_unit_id = _csv_unit_id AND (action = 0 OR action IS null);
END //
DELIMITER ;


DROP PROCEDURE IF EXISTS `sp_statutory_action_pending_count`;
DELIMITER //
CREATE PROCEDURE `sp_statutory_action_pending_count`(
IN csvid INT
)
BEGIN
    SELECT COUNT(bulk_statutory_mapping_id) AS pending_count
    FROM tbl_bulk_statutory_mapping AS t2
    WHERE t2.csv_id = csvid AND IFNULL(action, 0) = 0;
END //
DELIMITER ;


-- --------------------------------------------------------------------------------
-- To update format file AND upload statis
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_sm_format_file_status_update`;
DELIMITER //
CREATE PROCEDURE `sp_sm_format_file_status_update`(
    IN old_file_name VARCHAR(150), IN csvid INT,
    IN filename VARCHAR(150),
    IN file_size FLOAT
)
BEGIN
    UPDATE tbl_bulk_statutory_mapping SET format_upload_status = 1,
           format_file_size = file_size , format_file = filename
      WHERE csv_id = csvid AND format_file=old_file_name;

    UPDATE tbl_bulk_statutory_mapping_csv
      SET uploaded_documents = uploaded_documents + 1
      WHERE csv_id = csvid AND uploaded_documents < total_documents;

    UPDATE tbl_bulk_statutory_mapping_csv SET upload_status = 1 WHERE
      uploaded_documents = total_documents AND csv_id = csvid;
END //
DELIMITER ;


DROP PROCEDURE IF EXISTS `sp_check_duplicate_compliance_for_unit`;
DELIMITER //
CREATE PROCEDURE `sp_check_duplicate_compliance_for_unit`(
IN domain_ VARCHAR(50), unitcode_ VARCHAR(50), provision_ VARCHAR(500),
taskname_ VARCHAR(150), description_ VARCHAR(500),
p_legislation VARCHAR(500), s_legislation VARCHAR(500),
legal_entity_ VARCHAR(500)
)
BEGIN
  SELECT
    compliance_task_name
    FROM tbl_bulk_assign_statutory WHERE
    domain = domain_ AND unit_code = unitcode_ AND statutory_provision = provision_
    AND compliance_task_name = taskname_ AND compliance_description = description_
    AND legal_entity = legal_entity_ AND perimary_legislation = p_legislation
    AND secondary_legislation = s_legislation;
END //
DELIMITER ;


DROP PROCEDURE IF EXISTS `sp_check_upload_compliance_count_for_unit`;
DELIMITER //
CREATE PROCEDURE `sp_check_upload_compliance_count_for_unit`(
IN groupname_ VARCHAR(50), country_ VARCHAR(50), legalentityname_ VARCHAR(50), domain_ VARCHAR(50), unitcode_ VARCHAR(50)
)
BEGIN
  SELECT COUNT(1) AS count FROM tbl_download_assign_statutory_template WHERE
  client_group = groupname_ AND country = country_ AND legal_entity = legalentityname_
  AND domain = domain_ AND unit_code = unitcode_;
END //
DELIMITER ;


-- --------------------------------------------------------------------------------
-- To update file download status
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_sm_file_download_status_update`;
DELIMITER //
CREATE PROCEDURE `sp_sm_file_download_status_update`(
    IN csvid INT, download_status VARCHAR(50)
)
BEGIN
    UPDATE  tbl_bulk_statutory_mapping_csv SET file_download_status =  download_status
    WHERE csv_id = csvid;
END //
DELIMITER ;


DROP PROCEDURE IF EXISTS `sp_as_validation_info`;
DELIMITER //
CREATE PROCEDURE `sp_as_validation_info`(
    IN csv_id INT(11)
)
BEGIN
    SELECT COUNT(1) AS rejected FROM tbl_bulk_assign_statutory
    WHERE action = 2 AND csv_assign_statutory_id = csv_id;

    SELECT COUNT(1) AS un_saved FROM tbl_bulk_assign_statutory
    WHERE action IS null AND csv_assign_statutory_id = csv_id;
END //
DELIMITER ;


-- --------------------------------------------------------------------------------
-- To update file download status
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_sm_get_file_download_status`;
DELIMITER //
CREATE PROCEDURE `sp_sm_get_file_download_status`(
    IN csvid INT
)
BEGIN
    SELECT file_download_status FROM tbl_bulk_statutory_mapping_csv
    WHERE csv_id = csvid;
END //
DELIMITER ;


DROP PROCEDURE IF EXISTS `sp_as_rejected_file_count`;
DELIMITER //
CREATE PROCEDURE `sp_as_rejected_file_count`(
    IN user_ INT(11)
)
BEGIN
  SELECT COUNT(1) AS rejected FROM tbl_bulk_assign_statutory_csv
  WHERE (IFNULL(declined_count, 0) > 0 or IFNULL(is_fully_rejected, 0) = 1)
  AND approve_status < 4 AND uploaded_by = user_;
END //
DELIMITER ;


DROP PROCEDURE IF EXISTS `sp_assign_statutory_delete`;
DELIMITER //
CREATE PROCEDURE `sp_assign_statutory_delete`(
IN csvid INT
)
BEGIN
    DELETE FROM tbl_bulk_assign_statutory
    WHERE (action = 1 or action = 2) AND csv_assign_statutory_id = csvid;
END //
DELIMITER ;


-- --------------------------------------------------------------------------------
-- To get the file count of client unit csv uploaded under a client
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_bulk_client_unit_file_count`;
DELIMITER //
CREATE PROCEDURE `sp_bulk_client_unit_file_count`(
  IN _user_id INT(11))
BEGIN
  SELECT COUNT(csv_unit_id) AS file_count FROM tbl_bulk_units_csv
  WHERE uploaded_by = _user_id AND approve_status < 4 AND
  (IFNULL(declined_count, 0) > 0 OR IFNULL(is_fully_rejected, 0) = 1);
END //
DELIMITER ;


-- --------------------------------------------------------------------------------
-- To get total document count
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_sm_get_total_file_count`;
DELIMITER //
CREATE PROCEDURE `sp_sm_get_total_file_count`(
    IN csvid INT
)
BEGIN
    SELECT total_documents FROM tbl_bulk_statutory_mapping_csv
    WHERE csv_id = csvid;
END //
DELIMITER ;


DROP PROCEDURE IF EXISTS `sp_check_duplicate_statu_mapping`;
DELIMITER //
CREATE PROCEDURE `sp_check_duplicate_statu_mapping`(
    IN countryid INT(11), IN domainid INT(11), IN statutory VARCHAR(500),
    IN statutory_provision VARCHAR(500), IN compliance_task VARCHAR(100)
)
BEGIN
 SELECT
    t1.compliance_task
    FROM tbl_bulk_statutory_mapping AS t1
    INNER JOIN tbl_bulk_statutory_mapping_csv AS t2 ON t1.csv_id = t2.csv_id
    WHERE
      t2.country_id = countryid AND
      t2.domain_id = domainid AND
      t1.statutory = statutory AND
      t1.statutory_provision = statutory_provision AND
      t1.compliance_task = compliance_task;
END //
DELIMITER ;


DROP PROCEDURE IF EXISTS `sp_check_duplicate_task_id`;
DELIMITER //
CREATE PROCEDURE `sp_check_duplicate_task_id`(
    IN countryid INT(11), IN domainid INT(11), IN taskid VARCHAR(100)
)
BEGIN
SELECT
    t1.compliance_task
    FROM tbl_bulk_statutory_mapping AS t1
    INNER JOIN tbl_bulk_statutory_mapping_csv AS t2 ON t1.csv_id = t2.csv_id
    WHERE
      t2.country_id = countryid AND
      t2.domain_id = domainid AND
      t1.task_id = taskid;
END //
DELIMITER ;


DROP PROCEDURE IF EXISTS `sp_check_invalid_compliance_in_csv`;
DELIMITER //
CREATE PROCEDURE `sp_check_invalid_compliance_in_csv`(
IN client_group_ VARCHAR(50), legal_entity_ VARCHAR(100), domain_ TEXT,
organization_ TEXT, unit_code_ VARCHAR(50), unit_name_ VARCHAR(50),
unit_location_ TEXT , primary_legislation_ VARCHAR(100),
secondary_legislation_ TEXT, statutory_provision_ VARCHAR(500),
compliance_task_ VARCHAR(100), compliance_description_ TEXT
)
BEGIN
  SELECT as_id
  FROM tbl_download_assign_statutory_template WHERE
  client_group = client_group_ AND legal_entity = legal_entity_ AND
  domain = domain_ AND organization = organization_ AND
  unit_code = unit_code_ AND unit_name = unit_name_ AND
  unit_location = unit_location_ AND
  perimary_legislation = primary_legislation_ AND
  secondary_legislation = secondary_legislation_ AND
  statutory_provision = statutory_provision_ AND
  compliance_task_name = compliance_task_ AND
  compliance_description = compliance_description_;
END //
DELIMITER ;


DROP PROCEDURE IF EXISTS `sp_assign_statutory_update_action`;
DELIMITER //
CREATE PROCEDURE `sp_assign_statutory_update_action`(
IN csvid INT, userid INT
)
BEGIN
  UPDATE tbl_bulk_assign_statutory_csv SET
  approve_status = 1, approved_on = current_ist_datetime(),
  approved_by = userid, is_fully_rejected = 0,
  total_rejected_records = (SELECT COUNT(0) FROM
  tbl_bulk_assign_statutory AS t WHERE
  t.action = 2 AND t.csv_assign_statutory_id = csvid)
  WHERE csv_assign_statutory_id = csvid;
END//
DELIMITER ;


DROP PROCEDURE IF EXISTS `sp_statutory_update_action`;
DELIMITER //
CREATE PROCEDURE `sp_statutory_update_action`(
IN csvid INT, userid INT
)
BEGIN
  UPDATE tbl_bulk_statutory_mapping_csv SET
  approve_status = 1, approved_on = current_ist_datetime(),
  approved_by = userid, is_fully_rejected = 0,
  total_rejected_records = (SELECT COUNT(0) FROM
  tbl_bulk_statutory_mapping AS t WHERE t.csv_id = csvid
  AND t.action = 2)
  WHERE csv_id = csvid;
END //
DELIMITER ;


DROP PROCEDURE IF EXISTS `sp_statutory_mapping_delete`;
DELIMITER //
CREATE PROCEDURE `sp_statutory_mapping_delete`(
IN csvid INT
)
BEGIN
    DELETE FROM tbl_bulk_statutory_mapping
    WHERE IFNULL(action, 0) != 3  AND csv_id = csvid;
END //
DELIMITER ;


DROP PROCEDURE IF EXISTS `sp_sm_rejected_file_count`;
DELIMITER //
CREATE PROCEDURE `sp_sm_rejected_file_count`(
    IN user_ INT(11)
)
BEGIN
  SELECT COUNT(1) AS rejected FROM tbl_bulk_statutory_mapping_csv
  WHERE (IFNULL(declined_count, 0) > 0 or IFNULL(is_fully_rejected, 0) = 1)
  AND approve_status < 4 AND uploaded_by = user_;
END //
DELIMITER ;


DROP PROCEDURE IF EXISTS `sp_ct_format_file_status_update`;
DELIMITER //
CREATE PROCEDURE `sp_ct_format_file_status_update`(
    IN old_file_name VARCHAR(150), IN csvid INT,
    IN filename VARCHAR(150),
    IN file_size FLOAT
)
BEGIN

    update tbl_bulk_past_data set document_upload_status = 1,
           document_file_size = file_size , document_name = filename
      where csv_past_id = csvid and document_name=old_file_name;

    update tbl_bulk_past_data_csv
      set uploaded_documents = uploaded_documents + 1
      where csv_past_id = csvid and uploaded_documents < total_documents;

    UPDATE tbl_bulk_past_data_csv SET upload_status = 1 WHERE
      uploaded_documents = total_documents AND csv_past_id = csvid;
END //
DELIMITER ;


DROP PROCEDURE IF EXISTS `sp_check_client_compliance_rejected_status`;
DELIMITER //

CREATE PROCEDURE `sp_check_client_compliance_rejected_status`(
IN legal_entity_ VARCHAR(50), domain_ VARCHAR(50), unitcode_ VARCHAR(50),
csvid INT
)
BEGIN
  SELECT
    unit_code
    FROM tbl_bulk_assign_statutory WHERE
    legal_entity = legal_entity_ AND domain = domain_ AND unit_code = unitcode_
    AND csv_assign_statutory_id = csvid AND action = 2;
END //
DELIMITER ;


DROP PROCEDURE IF EXISTS `split_comma`;
DELIMITER //
CREATE PROCEDURE `split_comma`(IN fullstr VARCHAR(5000))
BEGIN
      DECLARE a INT Default 0 ;
      DECLARE str VARCHAR(2550);
      DROP TEMPORARY TABLE IF EXISTS my_temp_table;
    CREATE TEMPORARY TABLE my_temp_table (comma_stuff VARCHAR(5000));
      simple_loop: LOOP
         SET a=a+1;
         SET str=SPLIT_STR(fullstr,",",a);
         IF str='' THEN
            LEAVE simple_loop;
         END IF;

         insert into my_temp_table values (str);
   END LOOP simple_loop;
END //
DELIMITER ;


DROP PROCEDURE IF EXISTS `sp_pastdata_doc_download_status_update`;

DELIMITER //

CREATE PROCEDURE `sp_pastdata_doc_download_status_update`(
    IN csvid INT, download_status VARCHAR(50)
)
BEGIN

    update  tbl_bulk_past_data_csv set file_download_status =  download_status
      where csv_id = csvid;
END //

DELIMITER ;


DROP PROCEDURE IF EXISTS `sp_pastdata_get_file_download_status`;
DROP PROCEDURE IF EXISTS `sp_sm_get_declined_docs`;


ALTER TABLE `compfie_bulkupload`.`tbl_bulk_past_data`
ADD COLUMN `document_upload_status` TINYINT NULL AFTER `document_name`,
ADD COLUMN `document_file_size` FLOAT DEFAULT '0' AFTER `document_upload_status`;



ALTER TABLE `compfie_bulkupload`.`tbl_bulk_past_data_csv`
ADD COLUMN `file_download_status` VARCHAR(50) NULL AFTER `upload_status`;