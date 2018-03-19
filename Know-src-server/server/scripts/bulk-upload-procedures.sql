DROP FUNCTION IF EXISTS `current_ist_datetime`;

DELIMITER //

CREATE FUNCTION `current_ist_datetime`() RETURNS datetime
BEGIN
    DECLARE current_ist_date datetime;
    SET current_ist_date = convert_tz(utc_timestamp(),'+00:00','+05:30') ;

RETURN current_ist_date;
END //

DELIMITER ;

-- --------------------------------------------------------------------------------
-- Returns uploaded csv infor
-- --------------------------------------------------------------------------------

DROP PROCEDURE IF EXISTS `sp_statutory_mapping_csv_list`;

DELIMITER //

CREATE PROCEDURE `sp_statutory_mapping_csv_list`(
IN uploadedby INT
)
BEGIN
    select country_id, domain_id, csv_id, country_name,
    domain_name, csv_name, total_records, uploaded_on,
    total_documents, uploaded_documents
    from tbl_bulk_statutory_mapping_csv
    where upload_status = 0  and uploaded_by = uploadedby;
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
    UPDATE tbl_bulk_statutory_mapping set action = buaction,
    remarks = buremarks where csv_id = csvid and
    bulk_statutory_mapping_id = smid;
END //

DELIMITER ;


DROP PROCEDURE IF EXISTS `sp_pending_statutory_mapping_csv_list`;

DELIMITER //

CREATE PROCEDURE `sp_pending_statutory_mapping_csv_list`(
IN uploadedby varchar(50), cid INT, did INT
)
BEGIN
    select t1.csv_id, csv_name, uploaded_on, uploaded_by,
    total_records,
    (select count(action) from tbl_bulk_statutory_mapping where
     ifnull(action, 0) = 1 and csv_id = t1.csv_id) as approve_count,
    (select count(action) from tbl_bulk_statutory_mapping where
     ifnull(action, 0) = 2 and csv_id = t1.csv_id) as rej_count
    from tbl_bulk_statutory_mapping_csv as t1
    where upload_status =  1 and approve_status = 0 and ifnull(t1.is_fully_rejected, 0) = 0
    and country_id = cid and domain_id = did
    and uploaded_by like uploadedby;
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
DROP PROCEDURE IF EXISTS `sp_tbl_statutory_mappings_bulk_reportdata`;
DELIMITER //
CREATE PROCEDURE `sp_tbl_statutory_mappings_bulk_reportdata`(
  IN `user_ids` varchar(100),
  IN `country_ids` varchar(100),
  IN `domain_ids` varchar(100),
  IN `from_date` date,
  IN `to_date` date,
  IN `from_limit` int(11),
  IN `to_limit` int(11))
BEGIN
 SELECT
  tbl_bsm.csv_id,
  tbl_bsm_csv.country_name,
  tbl_bsm_csv.domain_name,
  tbl_bsm_csv.uploaded_by,
  tbl_bsm_csv.uploaded_on,
  LEFT(tbl_bsm_csv.csv_name, LENGTH(tbl_bsm_csv.csv_name) - LOCATE('_', REVERSE(tbl_bsm_csv.csv_name))) AS csv_name,
  tbl_bsm_csv.total_records,
  (SELECT COUNT(*) FROM tbl_bulk_statutory_mapping WHERE csv_id=tbl_bsm_csv.csv_id AND action=2) AS total_rejected_records,
  tbl_bsm_csv.approved_by,
  tbl_bsm_csv.rejected_by,
  tbl_bsm_csv.approved_on,
  tbl_bsm_csv.rejected_on,
  tbl_bsm_csv.is_fully_rejected,
  (SELECT COUNT(*) FROM tbl_bulk_statutory_mapping WHERE csv_id=tbl_bsm_csv.csv_id AND action=1) AS total_approve_records,
  tbl_bsm.action,
  tbl_bsm_csv.rejected_reason
FROM tbl_bulk_statutory_mapping AS tbl_bsm
INNER JOIN tbl_bulk_statutory_mapping_csv AS tbl_bsm_csv ON tbl_bsm_csv.csv_id=tbl_bsm.csv_id
WHERE
  FIND_IN_SET(tbl_bsm_csv.uploaded_by, user_ids)
  AND (DATE_FORMAT(date(tbl_bsm_csv.uploaded_on),"%Y-%m-%d") BETWEEN date(from_date) and date(to_date))
  AND FIND_IN_SET(tbl_bsm_csv.domain_id, domain_ids)
  AND FIND_IN_SET(tbl_bsm_csv.country_id, country_ids)
  GROUP BY tbl_bsm.csv_id
  ORDER BY tbl_bsm_csv.uploaded_on DESC
  LIMIT from_limit, to_limit;

SELECT count(DISTINCT tbl_bsm.csv_id) as total
FROM tbl_bulk_statutory_mapping AS tbl_bsm
INNER JOIN tbl_bulk_statutory_mapping_csv AS tbl_bsm_csv ON tbl_bsm_csv.csv_id=tbl_bsm.csv_id
 WHERE
  FIND_IN_SET(tbl_bsm_csv.uploaded_by, user_ids)
  AND (DATE_FORMAT(date(tbl_bsm_csv.uploaded_on),"%Y-%m-%d") BETWEEN date(from_date) and date(to_date))
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
    select distinct organization from tbl_bulk_statutory_mapping where csv_id = csvid;

    select distinct statutory_nature from tbl_bulk_statutory_mapping where csv_id = csvid;

    select distinct statutory from tbl_bulk_statutory_mapping where csv_id = csvid;

    select distinct compliance_frequency from tbl_bulk_statutory_mapping where csv_id = csvid;

    select distinct geography_location from tbl_bulk_statutory_mapping where csv_id = csvid;

    select distinct compliance_task from tbl_bulk_statutory_mapping where csv_id = csvid;

    select distinct compliance_description from tbl_bulk_statutory_mapping where csv_id = csvid;

    select distinct compliance_document from tbl_bulk_statutory_mapping where csv_id = csvid and compliance_document != '';

    select distinct task_id from tbl_bulk_statutory_mapping where csv_id = csvid;

    select distinct task_type from tbl_bulk_statutory_mapping where csv_id = csvid;
END //

DELIMITER ;

DROP PROCEDURE IF EXISTS `sp_download_assign_statutory_template`;

DELIMITER //

CREATE PROCEDURE `sp_download_assign_statutory_template`(
    IN clientgroup_name text, le_name text, domain_name text, unitname_ text
)
BEGIN
    select
    client_group, legal_entity, domain, organization, unit_code, unit_name,
    unit_location, perimary_legislation, secondary_legislation, statutory_provision, compliance_task_name,
    compliance_description
    from tbl_download_assign_statutory_template where
    client_group = clientgroup_name and legal_entity = le_name and find_in_set (domain, domain_name)
    and find_in_set (unit_name, unitname_)
    order by unit_name;
END //

DELIMITER ;

-- --------------------------------------------------------------------------------
-- to delete assign_statutory_template records
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_delete_assign_statutory_template`;

DELIMITER //


CREATE PROCEDURE `sp_delete_assign_statutory_template`(in
domain_name text, unitname_ text)
BEGIN
    delete from tbl_download_assign_statutory_template
    where
    find_in_set (domain, domain_name) and find_in_set (unit_name, unitname_);
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
frequency VARCHAR(50), statu VARCHAR(200), geo_location VARCHAR(500),
c_task VARCHAR(100), c_desc VARCHAR(500), c_doc VARCHAR(100),
f_count INT, f_range INT

)
BEGIN
    select distinct t1.csv_id, t1.country_name,
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

    from tbl_bulk_statutory_mapping_csv as t1
    inner join tbl_bulk_statutory_mapping as t2 on
    t1.csv_id  = t2.csv_id where t1.csv_id = csvid
    and organization like orga_name and geography_location like geo_location
    and statutory_nature like s_nature and statutory like statu
    and compliance_frequency like frequency and compliance_task like c_task
    and compliance_description like c_desc and compliance_document like c_doc
    limit  f_count, f_range;

    select count(distinct t2.bulk_statutory_mapping_id) as total

    from tbl_bulk_statutory_mapping_csv as t1
    inner join tbl_bulk_statutory_mapping as t2 on
    t1.csv_id  = t2.csv_id where t1.csv_id = csvid
    and organization like orga_name and geography_location like geo_location
    and statutory_nature like s_nature and statutory like statu
    and compliance_frequency like frequency and compliance_task like c_task
    and compliance_description like c_desc and compliance_document like c_doc;
END //

DELIMITER ;


DROP PROCEDURE IF EXISTS `sp_statutory_mapping_view_by_csvid`;

DELIMITER //

CREATE PROCEDURE `sp_statutory_mapping_view_by_csvid`(
IN csvid INT, f_count INT, f_range INT

)
BEGIN
    select t1.csv_id, t1.country_name,
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

    from tbl_bulk_statutory_mapping_csv as t1
    inner join tbl_bulk_statutory_mapping as t2 on
    t1.csv_id  = t2.csv_id where t1.csv_id = csvid
    limit  f_count, f_range;

END //

DELIMITER ;



DROP PROCEDURE IF EXISTS `sp_statutory_mapping_update_action`;

DELIMITER //

CREATE PROCEDURE `sp_statutory_mapping_update_action`(
IN csvid INT, action INT, remarks VARCHAR(500),
userid INT

)
BEGIN
    IF action = 2 then
        UPDATE tbl_bulk_statutory_mapping_csv SET
        rejected_reason = remarks, is_fully_rejected = 1,
        rejected_by = userid,
        rejected_on = current_ist_datetime(),
        total_rejected_records = (select count(0) from
        tbl_bulk_statutory_mapping as t WHERE t.csv_id = csvid)
        WHERE csv_id = csvid;
    else
        UPDATE tbl_bulk_statutory_mapping_csv SET
        approve_status = 1, approved_on = current_ist_datetime(),
        approved_by = userid, is_fully_rejected = 0
        WHERE csv_id = csvid;
    end if;

    IF action = 3 then
        UPDATE tbl_bulk_statutory_mapping set action = 3;

    end if;

END //

DELIMITER ;

-- --------------------------------------------------------------------------------
-- To get the client unit bulk uploaded file slist
-- --------------------------------------------------------------------------------

DROP PROCEDURE IF EXISTS `sp_client_units_csv_list`;

DELIMITER //

CREATE PROCEDURE `sp_client_units_csv_list`(
    IN _clientId INT(11), _groupName varchar(50))
BEGIN
    SELECT t1.csv_unit_id, t1.csv_name, t1.uploaded_by,
    DATE_FORMAT(t1.uploaded_on, '%d-%b-%Y %h:%i') as uploaded_on,
    t1.total_records as no_of_records,
    (SELECT count(*) from tbl_bulk_units where csv_unit_id =
    t1.csv_unit_id and action = 1) AS approved_count,
    (SELECT count(*) from tbl_bulk_units where csv_unit_id =
    t1.csv_unit_id and action = 2) AS rej_count,
    (SELECT count(*) from tbl_bulk_units where csv_unit_id =
    t1.csv_unit_id and action = 3) AS declined_count
 FROM
    tbl_bulk_units_csv as t1 WHERE t1.client_id = _clientId AND
    t1.client_group = _groupName ORDER BY t1.uploaded_on desc;
END //

DELIMITER ;

DROP PROCEDURE IF EXISTS `sp_statutory_mapping_by_csvid`;
DELIMITER //
CREATE PROCEDURE `sp_statutory_mapping_by_csvid`(
IN csvid INT
)
BEGIN
    select
    t2.bulk_statutory_mapping_id, t2.s_no,
    t2.organization as Organization, t2.geography_location as Applicable_Location,
    t2.statutory_nature as Statutory_Nature,
    t2.statutory as Statutory, t2.statutory_provision as Statutory_Provision,
    t2.compliance_task as Compliance_Task, t2.compliance_document as Compliance_Document,
    t2.compliance_description as Compliance_Description, t2.penal_consequences as Penal_Consequences,
    t2.reference_link as Reference_Link, t2.compliance_frequency as Compliance_Frequency,
    t2.statutory_month as Statutory_Month, t2.statutory_date as Statutory_Date, t2.trigger_before as Trigger_Days,
    t2.repeats_every as Repeats_Every, t2.repeats_type as Repeats_Type, t2.repeat_by as `Repeats_By (DOM/EOM)`, t2.duration as Duration,
    t2.duration_type as Duration_Type, t2.multiple_input as Multiple_Input_Section, t2.format_file as Format,
    t2.task_id as Task_ID, t2.task_type as Task_Type,
    t2.action, t2.remarks,
    t1.uploaded_by, t1.country_name, t1.domain_name, t1.csv_name

    from tbl_bulk_statutory_mapping as t2
    inner join tbl_bulk_statutory_mapping_csv as t1
    on t1.csv_id = t2.csv_id
    where t2.csv_id = csvid;

END //

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
    select t1.csv_assign_statutory_id, t1.csv_name, t1.uploaded_by,
    DATE_FORMAT(t1.uploaded_on, '%d-%b-%Y %h:%i') as uploaded_on, t1.total_records,
    (select count(action) from tbl_bulk_assign_statutory where
     action = 1 and csv_assign_statutory_id = t1.csv_assign_statutory_id) as approved_count,
    (select count(action) from tbl_bulk_assign_statutory where
     action = 2 and csv_assign_statutory_id = t1.csv_assign_statutory_id) as rejected_count
    from tbl_bulk_assign_statutory_csv as t1
    where t1.approve_status =  0 and t1.client_id = cl_id and t1.legal_entity_id = le_id;
END //

DELIMITER ;


DROP PROCEDURE IF EXISTS `sp_assgined_statutory_bulk_reportdata`;;
DELIMITER //
CREATE PROCEDURE `sp_assgined_statutory_bulk_reportdata`(
IN `client_group_id` int(11), IN `legal_entity_id` int(11),
IN `unit_id` varchar(100), IN `from_date` date, IN `to_date` date,
IN `from_limit` int, IN `to_limit` int,
IN `user_ids` varchar(100), IN `domain_ids` varchar(100))
BEGIN
IF (unit_id='') THEN
  SELECT  t1.domain, t1.uploaded_by, t1.uploaded_on,t1.csv_name, t1.total_records, t1.total_rejected_records,
  t1.approved_by,t1.rejected_by,t1.approved_on, t1.rejected_on,t1.is_fully_rejected,
  t1.approve_status, t1.rejected_reason
  FROM tbl_bulk_assign_statutory_csv AS t1
  INNER JOIN tbl_bulk_assign_statutory AS t2 ON t2.csv_assign_statutory_id=t1.csv_assign_statutory_id
  WHERE
  t1.client_id = client_group_id AND
  t1.legal_entity_id = legal_entity_id AND
   FIND_IN_SET(t1.uploaded_by, user_ids) AND
   FIND_IN_SET(t1.domain_ids, domain_ids) AND
  (DATE_FORMAT(date(t1.uploaded_on),"%Y-%m-%d") BETWEEN date(from_date) and date(to_date))
  ORDER BY t1.uploaded_on DESC
  LIMIT from_limit, to_limit;

  SELECT count(0) as total
  FROM tbl_bulk_assign_statutory_csv AS t1
  INNER JOIN tbl_bulk_assign_statutory AS t2 ON t2.csv_assign_statutory_id=t1.csv_assign_statutory_id
  WHERE
  t1.client_id = client_group_id AND
  t1.legal_entity_id = legal_entity_id AND
  FIND_IN_SET(t1.uploaded_by, user_ids) AND
  FIND_IN_SET(t1.domain_ids, domain_ids) AND
  (DATE_FORMAT(date(t1.uploaded_on),"%Y-%m-%d") BETWEEN date(from_date) and date(to_date))
  ORDER BY t1.uploaded_on DESC;
ELSE
  SELECT t1.domain, t2.unit_code, t1.uploaded_by, t1.uploaded_on,t1.csv_name, t1.total_records, t1.total_rejected_records,
  t1.approved_by,t1.rejected_by,t1.approved_on, t1.rejected_on,t1.is_fully_rejected,
  t1.approve_status, t1.rejected_reason
  FROM tbl_bulk_assign_statutory_csv AS t1
  INNER JOIN tbl_bulk_assign_statutory AS t2 ON t2.csv_assign_statutory_id=t1.csv_assign_statutory_id
  WHERE
   t2.unit_code=unit_id AND
   t1.client_id = client_group_id AND
   t1.legal_entity_id = legal_entity_id AND
   FIND_IN_SET(t1.uploaded_by, user_ids) AND
   FIND_IN_SET(t1.domain_ids, domain_ids) AND
  (DATE_FORMAT(date(t1.uploaded_on),"%Y-%m-%d") BETWEEN date(from_date) and date(to_date))
  ORDER BY t1.uploaded_on DESC
  LIMIT from_limit, to_limit;

  SELECT count(0) as total
  FROM tbl_bulk_assign_statutory_csv AS t1
  INNER JOIN tbl_bulk_assign_statutory AS t2 ON t2.csv_assign_statutory_id=t1.csv_assign_statutory_id
  WHERE
  t2.unit_code=unit_id AND
  t1.client_id = client_group_id AND
  t1.legal_entity_id = legal_entity_id AND
  FIND_IN_SET(t1.domain_ids, domain_ids) AND
  FIND_IN_SET(t1.uploaded_by, user_ids) AND
  (DATE_FORMAT(date(t1.uploaded_on),"%Y-%m-%d") BETWEEN date(from_date) and date(to_date))
  ORDER BY t1.uploaded_on DESC;
END IF;
END //
DELIMITER ;


-- --------------------------------------------------------------------------------
-- To delete the rejected statutory mapping record by csv id
-- --------------------------------------------------------------------------------

DROP PROCEDURE IF EXISTS `sp_delete_reject_sm_by_csvid`;
DELIMITER //
CREATE PROCEDURE `sp_delete_reject_sm_by_csvid`(IN `csvid` INT)
BEGIN
  Declare isfullyrejected INT default 0;
  SET isfullyrejected=(SELECT is_fully_rejected FROM tbl_bulk_statutory_mapping_csv WHERE csv_id=csvid);
 IF isfullyrejected=1 THEN
   DELETE FROM tbl_bulk_statutory_mapping WHERE csv_id=csvid;
 ELSE
   DELETE FROM tbl_bulk_statutory_mapping WHERE csv_id=csvid AND action=3;
 END IF;
END//
DELIMITER ;


DROP PROCEDURE IF EXISTS `sp_rejected_statutory_mapping_reportdata`;
DELIMITER //
CREATE PROCEDURE `sp_rejected_statutory_mapping_reportdata`(
    IN `country_id` int(11),
    IN `domain_id` int(11),
    IN `user_id` int(11))
 BEGIN
 SELECT DISTINCT sm.csv_id,
    sm_csv.country_name,
    sm_csv.domain_name,
    sm_csv.uploaded_by,
    sm_csv.uploaded_on,
    LEFT(sm_csv.csv_name, LENGTH(sm_csv.csv_name) - LOCATE('_', REVERSE(sm_csv.csv_name)))
    AS csv_name,
    sm_csv.total_records,
    sm_csv.total_rejected_records,
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
    (SELECT COUNT(*) FROM tbl_bulk_statutory_mapping WHERE csv_id = sm_csv.csv_id AND action=3)
     AS declined_count
FROM tbl_bulk_statutory_mapping AS sm
INNER JOIN tbl_bulk_statutory_mapping_csv AS sm_csv ON sm_csv.csv_id=sm.csv_id
WHERE
  sm_csv.country_id=country_id AND
  sm_csv.domain_id=domain_id AND
  sm_csv.uploaded_by=user_id AND
  (sm.action=3 OR sm_csv.is_fully_rejected=1)
  ORDER BY sm_csv.uploaded_on ASC;
END //
DELIMITER ;

DROP PROCEDURE IF EXISTS `sp_update_download_count_by_csvid`;

DELIMITER //
CREATE PROCEDURE `sp_update_download_count_by_csvid`(IN `csvid` int(11))
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
    IN `client_group_id` int(11),
    IN `from_date` date,
    IN `to_date` date,
    IN `from_limit` int(11),
    IN `to_limit` int(11),
    IN `user_ids` varchar(100))
BEGIN
  SELECT
    t1.uploaded_by,
    t1.uploaded_on,
    t1.csv_name,
    t1.total_records,
    t1.total_rejected_records,
    t1.approved_by,
    t1.rejected_by,
    t1.approved_on,
    t1.rejected_on,
    t1.is_fully_rejected,
    t1.approve_status,
    t1.rejected_reason
  FROM tbl_bulk_units_csv AS t1
  INNER JOIN tbl_bulk_units AS t2 ON t2.csv_unit_id=t1.csv_unit_id
  WHERE
    FIND_IN_SET(t1.uploaded_by, user_ids) AND
    t1.client_id = client_group_id AND
    (DATE_FORMAT(date(t1.uploaded_on),"%Y-%m-%d") BETWEEN date(from_date) and date(to_date))
  ORDER BY t1.uploaded_on DESC
  LIMIT from_limit, to_limit;

  SELECT count(0) as total
  FROM tbl_bulk_units_csv AS t1
  INNER JOIN tbl_bulk_units AS t2 ON t2.csv_unit_id=t1.csv_unit_id
  WHERE
    FIND_IN_SET(t1.uploaded_by, user_ids) AND
    t1.client_id = client_group_id AND
    (DATE_FORMAT(date(t1.uploaded_on),"%Y-%m-%d") BETWEEN date(from_date) and date(to_date))
  ORDER BY t1.uploaded_on DESC;
END //
DELIMITER ;

DROP PROCEDURE IF EXISTS `cu_delete_unit_by_csvid`;
DELIMITER //
CREATE PROCEDURE `cu_delete_unit_by_csvid`(IN `csvid` INT(11))
BEGIN
  DECLARE isfullyrejected INT DEFAULT 0;
  SET isfullyrejected=(SELECT is_fully_rejected FROM tbl_bulk_units_csv WHERE csv_unit_id=csvid);
 IF isfullyrejected=1 THEN
    DELETE FROM tbl_bulk_units WHERE csv_unit_id=csvid;
 ELSE
    DELETE FROM tbl_bulk_units WHERE csv_unit_id=csvid AND action=3;
 END IF;
END//
DELIMITER ;


DROP PROCEDURE IF EXISTS `cu_update_download_count`;
DELIMITER //
CREATE PROCEDURE `cu_update_download_count`(IN `csvid` int(11))
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
CREATE PROCEDURE `sp_rejected_client_unit_data`(IN `client_group_id` int(11), IN `user_id` int(11))
 BEGIN
  SELECT DISTINCT cu.csv_unit_id,
   cu_csv.uploaded_by,
   cu_csv.uploaded_on,
   cu_csv.csv_name,
   cu_csv.total_records,
   cu_csv.total_rejected_records,
   cu_csv.approved_by,
   cu_csv.rejected_by,
   cu_csv.approved_on,
   cu_csv.rejected_on,
   cu_csv.is_fully_rejected,
   cu_csv.approve_status,
   cu_csv.rejected_file_download_count,
   cu.remarks,
   cu.action,
  (SELECT COUNT(*) FROM tbl_bulk_units WHERE csv_unit_id = cu_csv.csv_unit_id AND action=3) AS declined_count
  FROM tbl_bulk_units AS cu
  INNER JOIN tbl_bulk_units_csv AS cu_csv ON cu_csv.csv_unit_id=cu.csv_unit_id
  WHERE
   cu_csv.client_group=client_group_id AND
   cu_csv.uploaded_by=user_id AND
   (cu.action=3 OR cu_csv.is_fully_rejected=1)
  ORDER BY cu_csv.uploaded_on ASC;
 END//
DELIMITER ;

DROP PROCEDURE IF EXISTS `sp_delete_reject_asm_by_csvid`;
DELIMITER //
CREATE PROCEDURE `sp_delete_reject_asm_by_csvid`(IN `csvid` INT)
BEGIN
  DECLARE isfullyrejected INT DEFAULT 0;
  SET isfullyrejected=(SELECT is_fully_rejected FROM tbl_bulk_assign_statutory_csv WHERE csv_assign_statutory_id=csvid);
 IF isfullyrejected=1 THEN
   DELETE FROM tbl_bulk_assign_statutory WHERE csv_assign_statutory_id=csvid;
 ELSE
   Delete FROM tbl_bulk_assign_statutory WHERE csv_assign_statutory_id=csvid AND action=3;
 END IF;
END //
DELIMITER ;


DROP PROCEDURE IF EXISTS `sp_rejected_assign_sm_reportdata`;
DELIMITER //
CREATE PROCEDURE `sp_rejected_assign_sm_reportdata`(IN `client_id` int(11), IN `le_id` int(11), IN `domain_ids` varchar(100), IN `unit_id` varchar(100), IN `user_id` int(11))
BEGIN
  IF(unit_id!='') THEN
   SELECT
    sm.csv_assign_statutory_id,
    sm_csv.uploaded_by,
    sm_csv.uploaded_on,
    sm_csv.csv_name,
    sm_csv.total_records,
    sm_csv.total_rejected_records,
    sm_csv.approved_by,
    sm_csv.rejected_by,
    sm_csv.approved_on,
    sm_csv.rejected_on,
    sm_csv.is_fully_rejected,
    sm_csv.approve_status,
    sm_csv.rejected_file_download_count,
    sm.remarks,
    sm.action,
    (SELECT COUNT(*) FROM tbl_bulk_assign_statutory WHERE csv_assign_statutory_id = sm_csv.csv_assign_statutory_id AND action=3) AS declined_count
   FROM tbl_bulk_assign_statutory AS sm
   INNER JOIN tbl_bulk_assign_statutory_csv AS sm_csv ON sm_csv.csv_assign_statutory_id=sm.csv_assign_statutory_id
   WHERE
    FIND_IN_SET(sm_csv.domain_ids, domain_ids) AND
    sm_csv.client_id=client_id AND
    sm_csv.legal_entity_id=le_id AND
    sm.unit_code=unit_id AND
    sm_csv.uploaded_by=user_id AND
    (sm.action=3 OR sm_csv.is_fully_rejected=1)
   Group by sm.csv_assign_statutory_id
   ORDER BY sm_csv.uploaded_on ASC;
 ELSE
   SELECT
    sm.csv_assign_statutory_id,
    sm_csv.uploaded_by,
    sm_csv.uploaded_on,
    sm_csv.csv_name,
    sm_csv.total_records,
    sm_csv.total_rejected_records,
    sm_csv.approved_by,
    sm_csv.rejected_by,
    sm_csv.approved_on,
    sm_csv.rejected_on,
    sm_csv.is_fully_rejected,
    sm_csv.approve_status,
    sm_csv.rejected_file_download_count,
    sm.remarks,
    sm.action,
    (SELECT COUNT(*) FROM tbl_bulk_assign_statutory WHERE csv_assign_statutory_id = sm_csv.csv_assign_statutory_id AND action=3) AS declined_count
   FROM tbl_bulk_assign_statutory AS sm
   INNER JOIN tbl_bulk_assign_statutory_csv AS sm_csv ON sm_csv.csv_assign_statutory_id=sm.csv_assign_statutory_id
   WHERE
    FIND_IN_SET(sm_csv.domain_ids, domain_ids) AND
    sm_csv.client_id=client_id AND
    sm_csv.legal_entity_id=le_id AND
    sm_csv.uploaded_by=user_id AND
    (sm.action=3 OR sm_csv.is_fully_rejected=1)
  Group by sm.csv_assign_statutory_id
  ORDER BY sm_csv.uploaded_on ASC;
 END IF;
END//
DELIMITER ;


DROP PROCEDURE IF EXISTS `sp_update_asm_download_count`;

DELIMITER //
CREATE PROCEDURE `sp_update_asm_download_count`(IN `csvid` int(11))
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
    IN `user_ids` varchar(100),
    IN `country_ids` varchar(100),
    IN `domain_ids` varchar(100),
    IN `from_date` date,
    IN `to_date` date)
BEGIN
   SELECT
     tbl_bsm_csv.country_name,
     tbl_bsm_csv.domain_name,
     tbl_bsm_csv.uploaded_by,
     tbl_bsm_csv.uploaded_on,
     tbl_bsm_csv.csv_name,
     tbl_bsm_csv.total_records,
     tbl_bsm_csv.total_rejected_records,
     tbl_bsm_csv.approved_by,
     tbl_bsm_csv.rejected_by,
     tbl_bsm_csv.approved_on,
     tbl_bsm_csv.rejected_on,
     tbl_bsm_csv.is_fully_rejected,
     tbl_bsm_csv.approve_status,
     tbl_bsm.action,
     tbl_bsm_csv.rejected_reason
   FROM tbl_bulk_statutory_mapping AS tbl_bsm
   INNER JOIN tbl_bulk_statutory_mapping_csv AS tbl_bsm_csv ON tbl_bsm_csv.csv_id=tbl_bsm.csv_id
   WHERE FIND_IN_SET(tbl_bsm_csv.uploaded_by, user_ids)
     AND (DATE_FORMAT(date(tbl_bsm_csv.uploaded_on),"%Y-%m-%d") BETWEEN date(from_date) and date(to_date))
     AND FIND_IN_SET(tbl_bsm_csv.domain_id, domain_ids)
     AND FIND_IN_SET(tbl_bsm_csv.country_id, country_ids)
   ORDER BY tbl_bsm_csv.uploaded_on DESC;


   SELECT count(0) as total
   FROM tbl_bulk_statutory_mapping AS tbl_bsm
   INNER JOIN tbl_bulk_statutory_mapping_csv AS tbl_bsm_csv ON tbl_bsm_csv.csv_id=tbl_bsm.csv_id
   WHERE
     FIND_IN_SET(tbl_bsm_csv.uploaded_by, user_ids)
     AND (DATE_FORMAT(date(tbl_bsm_csv.uploaded_on),"%Y-%m-%d") BETWEEN date(from_date) and date(to_date))
     AND FIND_IN_SET(tbl_bsm_csv.domain_id, domain_ids)
     AND FIND_IN_SET(tbl_bsm_csv.country_id, country_ids)
   ORDER BY tbl_bsm_csv.uploaded_on DESC;
END //
DELIMITER ;

DROP PROCEDURE IF EXISTS `sp_export_client_unit_bulk_reportdata`;
DELIMITER //

CREATE PROCEDURE `sp_export_client_unit_bulk_reportdata`(IN `client_group_id` int(11),
  IN `from_date` date, IN `to_date` date, IN `user_ids` varchar(100))
BEGIN
SELECT
t1.uploaded_by,
t1.uploaded_on,
t1.csv_name,
t1.total_records,
t1.total_rejected_records,
t1.approved_by,
t1.rejected_by,
t1.approved_on,
t1.rejected_on,
t1.is_fully_rejected,
t1.approve_status,
t1.rejected_reason
FROM tbl_bulk_units_csv AS t1
INNER JOIN tbl_bulk_units AS t2 ON t2.csv_unit_id=t1.csv_unit_id
WHERE
t1.client_group = client_group_id AND
FIND_IN_SET(t1.uploaded_by, user_ids) AND
(DATE_FORMAT(date(t1.uploaded_on),"%Y-%m-%d")
BETWEEN date(from_date) and date(to_date))
ORDER BY t1.uploaded_on DESC;

SELECT count(0) as total
FROM tbl_bulk_units_csv AS t1
INNER JOIN tbl_bulk_units AS t2 ON t2.csv_unit_id=t1.csv_unit_id
WHERE
t1.client_group = client_group_id AND
FIND_IN_SET(t1.uploaded_by, user_ids) AND
(DATE_FORMAT(date(t1.uploaded_on),"%Y-%m-%d")
BETWEEN date(from_date) and date(to_date))
ORDER BY t1.uploaded_on DESC;
END //
DELIMITER ;

DROP PROCEDURE IF EXISTS `sp_export_assigned_statutory_bulk_reportdata`;
DELIMITER //
CREATE PROCEDURE `sp_export_assigned_statutory_bulk_reportdata`(
  IN `client_group_id` int(11), IN `legal_entity_id` int(11),
  IN `unit_id` varchar(100), IN `from_date` date, IN `to_date` date,
  IN `user_ids` varchar(100), IN `domain_ids` varchar(100))
BEGIN
IF (unit_id='') THEN
  SELECT t1.domain, t1.uploaded_by, t1.uploaded_on,t1.csv_name, t1.total_records, t1.total_rejected_records,
  t1.approved_by,t1.rejected_by,t1.approved_on, t1.rejected_on,t1.is_fully_rejected,
  t1.approve_status,t1.rejected_reason
  FROM tbl_bulk_assign_statutory_csv AS t1
  INNER JOIN tbl_bulk_assign_statutory AS t2 ON t2.csv_assign_statutory_id=t1.csv_assign_statutory_id
  WHERE
  t1.client_id = client_group_id AND
  t1.legal_entity_id = legal_entity_id AND
   FIND_IN_SET(t1.uploaded_by, user_ids) AND
   FIND_IN_SET(t1.domain_ids, domain_ids) AND
  (DATE_FORMAT(date(t1.uploaded_on),"%Y-%m-%d") BETWEEN date(from_date) and date(to_date))
  ORDER BY t1.uploaded_on DESC;

  SELECT count(0) as total
  FROM tbl_bulk_assign_statutory_csv AS t1
  INNER JOIN tbl_bulk_assign_statutory AS t2 ON t2.csv_assign_statutory_id=t1.csv_assign_statutory_id
  WHERE
  t1.client_id = client_group_id AND
  t1.legal_entity_id = legal_entity_id AND
  FIND_IN_SET(t1.uploaded_by, user_ids) AND
  FIND_IN_SET(t1.domain_ids, domain_ids) AND
  (DATE_FORMAT(date(t1.uploaded_on),"%Y-%m-%d") BETWEEN date(from_date) and date(to_date))
  ORDER BY t1.uploaded_on DESC;
ELSE
  SELECT t1.domain, t2.unit_code, t1.uploaded_by, t1.uploaded_on,t1.csv_name, t1.total_records, t1.total_rejected_records,
  t1.approved_by,t1.rejected_by,t1.approved_on, t1.rejected_on,t1.is_fully_rejected,
  t1.approve_status, t1.rejected_reason
  FROM tbl_bulk_assign_statutory_csv AS t1
  INNER JOIN tbl_bulk_assign_statutory AS t2 ON t2.csv_assign_statutory_id=t1.csv_assign_statutory_id
  WHERE
   t2.unit_code=unit_id AND
   t1.client_id = client_group_id AND
  t1.legal_entity_id = legal_entity_id AND
   FIND_IN_SET(t1.uploaded_by, user_ids) AND
   FIND_IN_SET(t1.domain_ids, domain_ids) AND
  (DATE_FORMAT(date(t1.uploaded_on),"%Y-%m-%d") BETWEEN date(from_date) and date(to_date))
  ORDER BY t1.uploaded_on DESC;

  SELECT count(0) as total
  FROM tbl_bulk_assign_statutory_csv AS t1
  INNER JOIN tbl_bulk_assign_statutory AS t2 ON t2.csv_assign_statutory_id=t1.csv_assign_statutory_id
  WHERE
  t2.unit_code=unit_id AND
  t1.client_id = client_group_id AND
  t1.legal_entity_id = legal_entity_id AND
  FIND_IN_SET(t1.domain_ids, domain_ids) AND
  FIND_IN_SET(t1.uploaded_by, user_ids) AND
  (DATE_FORMAT(date(t1.uploaded_on),"%Y-%m-%d") BETWEEN date(from_date) and date(to_date))
  ORDER BY t1.uploaded_on DESC;
END IF;
END //
DELIMITER ;


DROP PROCEDURE IF EXISTS `sp_rejected_asm_csv_report`;
DELIMITER //
CREATE PROCEDURE `sp_rejected_asm_csv_report`(
    IN `client_id` int(11), IN `le_id` int(11), IN `domain_ids` varchar(100),
    IN `unit_id` varchar(100), IN `csv_id` int(11), IN `user_id` int(11))
 BEGIN
   IF(unit_id!='') THEN
    SELECT
     asm_csv.csv_assign_statutory_id,
     asm_csv.client_id,
     asm_csv.legal_entity_id,
     asm_csv.legal_entity,
     asm_csv.domain_ids,
     asm_csv.csv_name,
     asm_csv.uploaded_by,
     asm_csv.uploaded_on,
     asm_csv.total_records,
     asm_csv.approve_status,
     asm_csv.approved_on,
     asm_csv.approved_by,
     asm_csv.rejected_on,
     asm_csv.rejected_by,
     asm_csv.total_rejected_records,
     asm_csv.is_fully_rejected,
     asm_csv.rejected_file_name,
     asm_csv.rejected_file_download_count,
     asm.bulk_assign_statutory_id,
     asm.client_group,
     asm.organization,
     asm.unit_code,
     asm.unit_name,
     asm.unit_location,
     asm.perimary_legislation,
     asm.secondary_legislation,
     asm.statutory_provision,
     asm.compliance_task_name,
     asm.compliance_description,
     asm.statutory_applicable_status,
     asm.statytory_remarks,
     asm.compliance_applicable_status,
     asm.action,
     asm.remarks,
     asm_csv.rejected_reason
    FROM tbl_bulk_assign_statutory AS asm
    INNER JOIN tbl_bulk_assign_statutory_csv AS asm_csv
            ON asm_csv.csv_assign_statutory_id=asm.csv_assign_statutory_id
    WHERE FIND_IN_SET(asm_csv.domain_ids, domain_ids) AND
          asm_csv.client_id=client_id AND
          asm_csv.legal_entity_id=le_id AND
          asm.unit_code=unit_id AND
          asm_csv.uploaded_by=user_id AND
          asm.csv_assign_statutory_id=csv_id AND
          (asm.action=3 OR asm_csv.is_fully_rejected=1)
    Group by asm.csv_assign_statutory_id
    ORDER BY asm_csv.uploaded_on ASC;
   ELSE
    SELECT
     asm_csv.csv_assign_statutory_id,
     asm_csv.client_id,
     asm_csv.legal_entity_id,
     asm_csv.domain_ids,
     asm_csv.legal_entity,
     asm_csv.domain_ids,
     asm_csv.csv_name,
     asm_csv.uploaded_by,
     asm_csv.uploaded_on,
     asm_csv.total_records,
     asm_csv.approve_status,
     asm_csv.approved_on,
     asm_csv.approved_by,
     asm_csv.rejected_on,
     asm_csv.rejected_by,
     asm_csv.total_rejected_records,
     asm_csv.is_fully_rejected,
     asm_csv.rejected_file_name,
     asm_csv.rejected_file_download_count,
     asm.bulk_assign_statutory_id,
     asm.client_group,
     asm.organization,
     asm.unit_code,
     asm.unit_name,
     asm.unit_location,
     asm.perimary_legislation,
     asm.secondary_legislation,
     asm.statutory_provision,
     asm.compliance_task_name,
     asm.compliance_description,
     asm.statutory_applicable_status,
     asm.statytory_remarks,
     asm.compliance_applicable_status,
     asm.action,
     asm.remarks,
     asm_csv.rejected_reason
    FROM tbl_bulk_assign_statutory AS asm
    INNER JOIN tbl_bulk_assign_statutory_csv AS asm_csv ON asm_csv.csv_assign_statutory_id=asm.csv_assign_statutory_id
    WHERE
     FIND_IN_SET(asm_csv.domain_ids, domain_ids) AND
     asm_csv.client_id=client_id AND
     asm_csv.legal_entity_id=le_id AND
     asm_csv.uploaded_by=user_id AND
     asm.csv_assign_statutory_id=csv_id AND
     (asm.action=3 OR asm_csv.is_fully_rejected=1)
    Group by asm.csv_assign_statutory_id
    ORDER BY asm_csv.uploaded_on ASC;
   END IF;
END //
DELIMITER ;


DROP PROCEDURE IF EXISTS `sp_rejected_cu_csv_report`;
DELIMITER //
CREATE PROCEDURE `sp_rejected_cu_csv_report`(
    IN `cg_id` int(11),
    IN `csv_id` int(11),
    IN `user_id` int(11))
BEGIN
   SELECT
     u.bulk_unit_id,
     u.csv_unit_id,
     u.legal_entity,
     u.division,
     u.category,
     u.geography_level,
     u.unit_location,
     u.unit_code,
     u.unit_name,
     u.address,
     u.postalcode,
     u.domain,
     u.action,
     u.remarks,
     u_csv.client_id,
     u_csv.client_group,
     u_csv.csv_name,
     u_csv.uploaded_by,
     u_csv.uploaded_on,
     u_csv.total_records,
     u_csv.approve_status,
     u_csv.approved_on,
     u_csv.approved_by,
     u_csv.rejected_on,
     u_csv.rejected_by,
     u_csv.total_rejected_records,
     u_csv.is_fully_rejected,
     u_csv.rejected_file_name,
     u_csv.rejected_file_download_count,
     u_csv.rejected_reason
   FROM tbl_bulk_units AS u
   INNER JOIN tbl_bulk_units_csv AS u_csv ON u_csv.csv_unit_id=u.csv_unit_id
   WHERE
     u_csv.client_group=cg_id AND
     u_csv.uploaded_by=user_id AND
     u.csv_unit_id=csv_id AND
     (u.action=3 OR u_csv.is_fully_rejected=1)
   ORDER BY u_csv.uploaded_on ASC;
END //
DELIMITER ;


DROP PROCEDURE IF EXISTS `sp_rejected_sm_csv_report`;
DELIMITER //
CREATE PROCEDURE `sp_rejected_sm_csv_report`(
    IN `country_id` tinyint,
    IN `domain_id` tinyint,
    IN `user_id` tinyint,
    IN `csv_id` tinyint)
BEGIN
    SELECT
      sm.bulk_statutory_mapping_id,
      sm.csv_id,
      sm_csv.country_name,
      sm_csv.domain_name,
      sm_csv.uploaded_by,
      sm_csv.uploaded_on,
      sm_csv.csv_name,
      sm_csv.total_records,
      sm_csv.total_rejected_records,
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
      sm.organization,
      sm.geography_location,
      sm.statutory_nature,
      sm.statutory,
      sm.statutory_provision,
      sm.compliance_task,
      sm.compliance_document,
      sm.compliance_description,
      sm.penal_consequences,
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
      sm.format_file
    FROM tbl_bulk_statutory_mapping AS sm
    INNER JOIN tbl_bulk_statutory_mapping_csv AS sm_csv ON sm_csv.csv_id=sm.csv_id
    WHERE
      sm_csv.country_id=country_id AND
      sm_csv.domain_id=domain_id AND
      sm_csv.uploaded_by=user_id AND
      sm.csv_id=csv_id AND
      (sm.action=3 OR sm_csv.is_fully_rejected=1)
    ORDER BY sm_csv.uploaded_on ASC;
END //
DELIMITER ;

DROP PROCEDURE IF EXISTS `sp_get_cu_csv_file_name_by_id`;
DELIMITER //
CREATE PROCEDURE `sp_get_cu_csv_file_name_by_id`(IN `CSV_FILE_ID` int(11))
BEGIN
SELECT csv_name FROM tbl_bulk_units_csv WHERE csv_unit_id=CSV_FILE_ID;
END //
DELIMITER;

DROP PROCEDURE IF EXISTS `sp_get_sm_csv_file_name_by_id`;;
DELIMITER //
CREATE PROCEDURE `sp_get_sm_csv_file_name_by_id`(IN `CSV_FILE_ID` int(11))
BEGIN
SELECT csv_name FROM tbl_bulk_statutory_mapping_csv WHERE csv_id=CSV_FILE_ID;
END //
DELIMITER ;

DROP PROCEDURE IF EXISTS `sp_get_asm_csv_file_name_by_id`;;
DELIMITER //
CREATE PROCEDURE `sp_get_asm_csv_file_name_by_id`(IN `CSV_FILE_ID` int(11))
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
    select distinct domain from tbl_bulk_assign_statutory where csv_assign_statutory_id = csvid;

    select distinct CONCAT(unit_code,' - ',unit_name) AS unit_name from tbl_bulk_assign_statutory where csv_assign_statutory_id = csvid;

    select distinct perimary_legislation from tbl_bulk_assign_statutory where csv_assign_statutory_id = csvid;

    select distinct secondary_legislation from tbl_bulk_assign_statutory where csv_assign_statutory_id = csvid;

    select distinct statutory_provision from tbl_bulk_assign_statutory where csv_assign_statutory_id = csvid;

    select distinct compliance_task_name from tbl_bulk_assign_statutory where csv_assign_statutory_id = csvid;

    select distinct compliance_description from tbl_bulk_assign_statutory where csv_assign_statutory_id = csvid;
END //

DELIMITER ;

-- --------------------------------------------------------------------------------
-- To get the details of units under client id to check for duplication
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_groups_client_units_list`;

DELIMITER //

CREATE PROCEDURE `sp_groups_client_units_list`(
  IN _ClientId INT(11))
BEGIN
  select t2.legal_entity, t2.unit_code, t2.domain, t2.organization
  from tbl_bulk_units_csv as t1 inner join tbl_bulk_units as t2
  on t2.csv_unit_id = t1.csv_unit_id
  where t1.client_id = _ClientId;
END //

DELIMITER ;


DROP PROCEDURE IF EXISTS `sp_assign_statutory_view_by_csvid`;

DELIMITER //

CREATE PROCEDURE `sp_assign_statutory_view_by_csvid`(
IN csvid INT, f_count INT, f_range INT

)
BEGIN
    select t1.csv_assign_statutory_id, t1.csv_name, t1.legal_entity,
    t1.client_id,  t1.uploaded_by,
    DATE_FORMAT(t1.uploaded_on, '%d-%b-%Y %h:%i') as uploaded_on,
    t2.bulk_assign_statutory_id,
    t2.unit_code, t2.unit_name, t2.unit_location,
    t2.domain, t2.organization, t2.perimary_legislation,
    t2.secondary_legislation, t2.statutory_provision,
    t2.compliance_task_name, t2.compliance_description,
    t2.statutory_applicable_status, t2.statytory_remarks, t2.compliance_applicable_status,
    t2.remarks, t2.action

    from tbl_bulk_assign_statutory_csv as t1
    inner join tbl_bulk_assign_statutory as t2 on
    t1.csv_assign_statutory_id  = t2.csv_assign_statutory_id where t1.csv_assign_statutory_id = csvid
    limit  f_count, f_range;

END //

DELIMITER ;


DROP PROCEDURE IF EXISTS `sp_assign_statutory_view_by_filter`;

DELIMITER //

CREATE PROCEDURE `sp_assign_statutory_view_by_filter`(
    IN csvid INT, domain_name text, unit_code text,
    p_legis text, s_legis VARCHAR(200), s_prov VARCHAR(500),
    c_task VARCHAR(100), c_desc VARCHAR(500), f_count INT, f_range INT,
    view_data INT, s_status INT, c_status INT
)
BEGIN
    
    select t1.csv_assign_statutory_id, t1.csv_name, t1.legal_entity,
    t1.client_id,  t1.uploaded_by,
    DATE_FORMAT(t1.uploaded_on, '%d-%b-%Y %h:%i') as uploaded_on,
    (select distinct client_group from tbl_bulk_assign_statutory where csv_assign_statutory_id = t1.csv_assign_statutory_id) as client_group,
    (select count(0) from tbl_bulk_assign_statutory where csv_assign_statutory_id = t1.csv_assign_statutory_id) as total_count
    from tbl_bulk_assign_statutory_csv as t1
    where t1.csv_assign_statutory_id = csvid;

    select t2.bulk_assign_statutory_id,
    t2.unit_code, t2.unit_name, t2.unit_location,
    t2.domain, t2.organization, t2.perimary_legislation,
    t2.secondary_legislation, t2.statutory_provision,
    t2.compliance_task_name, t2.compliance_description,
    t2.statutory_applicable_status, t2.statytory_remarks, t2.compliance_applicable_status,
    t2.remarks, t2.action
    from tbl_bulk_assign_statutory_csv as t1
    inner join tbl_bulk_assign_statutory as t2 on
    t1.csv_assign_statutory_id  = t2.csv_assign_statutory_id where t1.csv_assign_statutory_id = csvid

    and IF(domain_name IS NOT NULL, FIND_IN_SET(t2.domain, domain_name), 1)
    and IF(unit_code IS NOT NULL, FIND_IN_SET(t2.unit_code, unit_code), 1)
    and IF(p_legis IS NOT NULL, FIND_IN_SET(t2.perimary_legislation, p_legis), 1)
    and IF(s_legis IS NOT NULL, t2.secondary_legislation = s_legis, 1)
    and IF(s_prov IS NOT NULL, t2.statutory_provision = s_prov, 1)
    and IF(c_task IS NOT NULL, t2.compliance_task_name = c_task, 1)
    and IF(c_desc IS NOT NULL, t2.compliance_description = c_desc, 1)
    and IF(view_data IS NOT NULL, t2.action = view_data, 1)
    and IF(s_status IS NOT NULL, t2.statutory_applicable_status = s_status, 1)
    and IF(c_status IS NOT NULL, t2.compliance_applicable_status = c_status, 1)
    limit  f_count, f_range;
END //

DELIMITER ;

DROP PROCEDURE IF EXISTS `sp_assign_statutory_by_csvid`;
DELIMITER //
CREATE PROCEDURE `sp_assign_statutory_by_csvid`(
IN csvid INT
)
BEGIN
    select
    t2.csv_assign_statutory_id,
    t2.bulk_assign_statutory_id,
    t2.domain as Domain, t2.organization as Organization,
    t2.unit_code as Unit_Code, t2.unit_name as Unit_Name, t2.unit_location as Unit_Location,
    t2.perimary_legislation as Primary_Legislation, t2.secondary_legislation as Secondary_Legislaion,
    t2.statutory_provision as Statutory_Provision,
    t2.compliance_task_name as Compliance_Task, t2.compliance_description as Compliance_Description,
    t2.statutory_applicable_status as Statutory_Applicable_Status, t2.statytory_remarks as Statutory_remarks,
    t2.compliance_applicable_status as Compliance_Applicable_Status,
    t2.remarks, t2.action, t1.uploaded_by

    from tbl_bulk_assign_statutory as t2
    inner join tbl_bulk_assign_statutory_csv as t1
    on t1.csv_assign_statutory_id = t2.csv_assign_statutory_id
    where t2.csv_assign_statutory_id = csvid;

END //

DELIMITER ;

DROP PROCEDURE IF EXISTS `sp_assign_statutory_update_action`;

DELIMITER //

CREATE PROCEDURE `sp_assign_statutory_update_action`(
IN csvid INT, action INT, remarks VARCHAR(500),
userid INT

)
BEGIN
    IF action = 2 then
        UPDATE tbl_bulk_assign_statutory_csv SET
        approve_status = 2,
        rejected_reason = remarks, is_fully_rejected = 1,
        rejected_by = userid,
        rejected_on = current_ist_datetime(),
        total_rejected_records = (select count(0) from
        tbl_bulk_assign_statutory as t WHERE t.csv_assign_statutory_id = csvid)
        WHERE csv_assign_statutory_id = csvid;
    else
        UPDATE tbl_bulk_assign_statutory_csv SET
        approve_status = 1, approved_on = current_ist_datetime(),
        approved_by = userid, is_fully_rejected = 0
        WHERE csv_assign_statutory_id = csvid;
    end if;

    IF action = 3 then
        UPDATE tbl_bulk_assign_statutory set action = 3;

    end if;
END //

DELIMITER ;

-- --------------------------------------------------------------------------------
-- To get domain organization count created in temp db
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_get_domain_organization_count`;

DELIMITER //

CREATE PROCEDURE `sp_get_domain_organization_count`(
  IN _ClientID int(11))
BEGIN
  select t2.legal_entity, t2.domain, t2.organization,
  count(t2.bulk_unit_id) as saved_units
  from tbl_bulk_units_csv as t1 inner join tbl_bulk_units as t2
  on t2.csv_unit_id = t1.csv_unit_id
  where t1.client_id = _ClientId
  group by t2.legal_entity, t2.organization;
END //

DELIMITER ;


-- --------------------------------------------------------------------------------
-- To get the CSV uploaded bulk client units under the file id
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_bulk_client_unit_by_csvid`;

DELIMITER //

CREATE PROCEDURE `sp_bulk_client_unit_by_csvid`(
    IN _csv_id INT(11))
BEGIN
    select t1.client_id, t1.client_group, t2.bulk_unit_id,
    t2.legal_entity as Legal_Entity, t2.division as Division,
    t2.category as Category, t2.geography_level as Geography_Level,
    t2.unit_location as Unit_Location, t2.unit_code as Unit_Code,
    t2.unit_name as Unit_Name, t2.address as Unit_Address,
    t2.city as City, t2.state as State, t2.postalcode as Postal_Code,
    t2.domain as Domain, t2.organization as Organization,
    t1.uploaded_by, t1.csv_name
    from tbl_bulk_units_csv as t1 inner join tbl_bulk_units as t2
    on t2.csv_unit_id = t1.csv_unit_id
    where t1.csv_unit_id = _csv_id;

END //

DELIMITER ;

DROP PROCEDURE IF EXISTS `sp_approve_assign_statutory_action_save`;

DELIMITER //

CREATE PROCEDURE `sp_approve_assign_statutory_action_save`(
IN csvid INT, asid INT, buaction INT, buremarks VARCHAR(500)
)
BEGIN
    UPDATE tbl_bulk_assign_statutory set action = buaction,
    remarks = buremarks where csv_assign_statutory_id = csvid and
    bulk_assign_statutory_id = asid;
END //

DELIMITER ;

-- --------------------------------------------------------------------------------
-- To update approve status/ reject status during approve all or reject all
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_bulk_client_unit_update_action`;

DELIMITER //

CREATE PROCEDURE `sp_bulk_client_unit_update_action`(
    IN _csv_unit_id INT(11), _action TINYINT, _remarks TEXT, _user_id INT(11))
BEGIN
    IF _action = 2 then
        UPDATE tbl_bulk_units SET
        action = 2, remarks = _remarks
        WHERE csv_unit_id = _csv_unit_id;

        UPDATE tbl_bulk_units_csv SET
        is_fully_rejected = 1,
        rejected_by = _user_id,
        rejected_on = current_ist_datetime(),
        total_rejected_records = (select count(0) from
        tbl_bulk_units as t1 WHERE t1.csv_unit_id = _csv_unit_id)
        WHERE csv_unit_id = _csv_unit_id;
    else
        UPDATE tbl_bulk_units SET
        action = 1, remarks = _remarks
        WHERE csv_unit_id = _csv_unit_id;

        UPDATE tbl_bulk_units_csv SET
        approve_status = 1, approved_on = current_ist_datetime(),
        approved_by = _user_id, is_fully_rejected = 0
        WHERE csv_unit_id = _csv_unit_id;
    end if;
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
    select t1.client_id, t1.client_group, t2.bulk_unit_id,
    t2.legal_entity, t2.division, t2.category,
    t2.geography_level, t2.unit_location, t2.unit_code,
    t2.unit_name, t2.address, t2.city, t2.state,
    t2.postalcode, t2.domain, t2.organization,
    t1.uploaded_by, t1.csv_name, t1.csv_unit_id, t1.uploaded_on,
    t2.action, t2.remarks
    from tbl_bulk_units_csv as t1 inner join tbl_bulk_units as t2
    on t2.csv_unit_id = t1.csv_unit_id
    where t1.csv_unit_id = _csv_unit_id
    limit  f_count, f_range;
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
    select distinct legal_entity from tbl_bulk_units where csv_unit_id = _csv_unit_id;

    select distinct division from tbl_bulk_units where csv_unit_id = _csv_unit_id;

    select distinct category from tbl_bulk_units where csv_unit_id = _csv_unit_id;

    select distinct unit_location from tbl_bulk_units where csv_unit_id = _csv_unit_id;

    select unit_code from tbl_bulk_units where csv_unit_id = _csv_unit_id;

    select distinct domain from tbl_bulk_units where csv_unit_id = _csv_unit_id;

    select distinct organization from tbl_bulk_units where csv_unit_id = _csv_unit_id;
END //

DELIMITER ;

-- --------------------------------------------------------------------------------
-- To fetch records as per the filter
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_bulk_client_unit_view_by_filter`;

DELIMITER //

CREATE PROCEDURE `sp_bulk_client_unit_view_by_filter`(
    IN _csv_unit_id INT, _le_name VARCHAR(50),
    _div_name VARCHAR(50), _cg_name VARCHAR(50),
    _u_location VARCHAR(200), _u_code VARCHAR(50),
    _domain VARCHAR(200), _orgn VARCHAR(500),
    _f_count INT, _f_limit INT
)
BEGIN
    select t1.client_id, t1.client_group, t2.bulk_unit_id,
    t2.legal_entity, t2.division, t2.category,
    t2.geography_level, t2.unit_location, t2.unit_code,
    t2.unit_name, t2.address, t2.city, t2.state,
    t2.postalcode, t2.domain, t2.organization,
    t1.uploaded_by, t1.csv_name, t1.csv_unit_id, t1.uploaded_on,
    t2.action, t2.remarks
    from tbl_bulk_units_csv as t1 inner join tbl_bulk_units as t2
    on t2.csv_unit_id = t1.csv_unit_id where t1.csv_unit_id = _csv_unit_id
    and legal_entity like legal_entity and division like _div_name and
    category like _cg_name and unit_location like _u_location and
    unit_code like _u_code and domain like _domain and
    organization like _orgn
    limit  _f_count, _f_limit;
END //

DELIMITER ;

-- --------------------------------------------------------------------------------
-- To save approve / reject of each unit in view
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_bulk_client_unit_id_save`;

DELIMITER //

CREATE PROCEDURE `sp_bulk_client_unit_id_save`(
    IN _csv_unit_id INT, _bu_unit_id INT, _action INT,
    _remarks VARCHAR(200)
)
BEGIN
    UPDATE tbl_bulk_units set action = _action,
    remarks = _remarks where csv_unit_id = _csv_unit_id and
    bulk_unit_id = _bu_unit_id;
END //

DELIMITER ;

-- --------------------------------------------------------------------------------
-- To get the count of units which has action as 0 or null
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_bulk_client_unit_action_count`;

DELIMITER //

CREATE PROCEDURE `sp_bulk_client_unit_action_count`(
    IN _csv_unit_id INT)
BEGIN
    select count(*) as null_action_count from tbl_bulk_units
    where csv_unit_id = _csv_unit_id and (action = 0 or action is null);
END //

DELIMITER ;


DROP PROCEDURE IF EXISTS `sp_statutory_action_pending_count`;
DELIMITER //
CREATE PROCEDURE `sp_statutory_action_pending_count`(
IN csvid INT
)
BEGIN
    select count(bulk_statutory_mapping_id) as pending_count
    from tbl_bulk_statutory_mapping as t2
    where t2.csv_id = csvid and ifnull(action, 0) = 0;

END //

DELIMITER ;

DROP PROCEDURE IF EXISTS `sp_check_duplicate_compliance_for_unit`;

DELIMITER //

CREATE PROCEDURE `sp_check_duplicate_compliance_for_unit`(
IN domain_ VARCHAR(50), unitcode_ VARCHAR(50), provision_ VARCHAR(500),
taskname_ VARCHAR(150), description_ VARCHAR(500)
)
BEGIN
  select
    compliance_task_name 
    from tbl_bulk_assign_statutory where
    domain = domain_ and unit_code = unitcode_ and statutory_provision = provision_
    and compliance_task_name = taskname_ and compliance_description = description_;
END //

DELIMITER ;


DROP PROCEDURE IF EXISTS `sp_check_upload_compliance_count_for_unit`;

DELIMITER //

CREATE PROCEDURE `sp_check_upload_compliance_count_for_unit`(
IN domain_ VARCHAR(50), unitcode_ VARCHAR(50)
)
BEGIN
  select count(1) as count from tbl_download_assign_statutory_template where
    domain = domain_ and unit_code = unitcode_;
END //

DELIMITER ;