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
    domain_name, csv_name, total_records,
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


DROP PROCEDURE IF EXISTS `sp_pending_statutory_mapping_csv_list`;

DELIMITER //

CREATE PROCEDURE `sp_pending_statutory_mapping_csv_list`(
IN uploadedby INT
)
BEGIN
    select t1.csv_id, csv_name, uploaded_on,
    total_records,
    (select count(action) from tbl_bulk_statutory_mapping where
     action is not null and csv_id = t1.csv_id) as action_count
    from tbl_bulk_statutory_mapping_csv as t1
    where upload_status =  1 and uploaded_by = uploadedby;
END //

DELIMITER ;



DROP PROCEDURE IF EXISTS `sp_statutory_mapping_rejected_list`;

DELIMITER //

CREATE PROCEDURE `sp_statutory_mapping_rejected_list`(
IN uploadedby INT
)
BEGIN
    select country_id, domain_id, csv_id, country_name,
    domain_name, csv_name, total_records,
    rejected_on, rejected_by, total_rejected_records, is_fully_rejected,
    rejected_reason, rejected_file_name, rejected_file_download_count
    from tbl_bulk_statutory_mapping_csv
    where uploaded_by = uploadedby and approve_status = 1  and (is_fully_rejected = 1 or total_rejected_records > 0);
END //

DELIMITER ;

-- --------------------------------
-- Statutory Mapping - Bulk Report
-- --------------------------------
DROP PROCEDURE IF EXISTS `sp_tbl_statutory_mappings_bulk_reportdata`;

DELIMITER //

CREATE PROCEDURE `sp_tbl_statutory_mappings_bulk_reportdata`(IN `user_id` varchar(100),
  IN `country_ids` varchar(100), IN `domain_ids` varchar(100),
    IN `from_date` date, IN `to_date` date,
    IN `from_limit` int(11), IN `to_limit` int(11))
BEGIN
 SELECT
t_sm_csv.country_name,
t_sm_csv.domain_name,
t_sm_csv.uploaded_by,
t_sm_csv.uploaded_on,
t_sm_csv.csv_name,
t_sm_csv.total_records,
t_sm_csv.total_rejected_records,
t_sm_csv.approved_by,
t_sm_csv.rejected_by,
t_sm_csv.approved_on,
t_sm_csv.rejected_on,
t_sm_csv.is_fully_rejected,
t_sm_csv.approve_status

 FROM tbl_bulk_statutory_mapping AS t_sm
 INNER JOIN tbl_bulk_statutory_mapping_csv AS t_sm_csv ON t_sm_csv.csv_id=t_sm.csv_id
 WHERE
  t_sm_csv.uploaded_by=user_id
  AND (DATE_FORMAT(date(t_sm_csv.uploaded_on),"%Y-%m-%d") BETWEEN date(from_date) and date(to_date))
  AND FIND_IN_SET(t_sm_csv.domain_id, domain_ids)
  AND FIND_IN_SET(t_sm_csv.country_id, country_ids)
  ORDER BY t_sm_csv.uploaded_on DESC
  LIMIT from_limit, to_limit;

 SELECT count(0) as total
 FROM tbl_bulk_statutory_mapping AS t_sm
 INNER JOIN tbl_bulk_statutory_mapping_csv AS t_sm_csv ON t_sm_csv.csv_id=t_sm.csv_id
 WHERE
  t_sm_csv.uploaded_by=user_id
  AND (DATE_FORMAT(date(t_sm_csv.uploaded_on),"%Y-%m-%d") BETWEEN date(from_date) and date(to_date))
  AND FIND_IN_SET(t_sm_csv.domain_id, domain_ids)
  AND FIND_IN_SET(t_sm_csv.country_id, country_ids)
  ORDER BY t_sm_csv.uploaded_on DESC;

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

    select distinct compliance_document from tbl_bulk_statutory_mapping where csv_id = csvid;
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
    select t1.csv_id, t1.country_name,
    t1.domain_name, t1.csv_name, t1.uploaded_by, t1.uploaded_on,
    t2.bulk_statutory_mapping_id, t2.s_no,
    t2.organization, t2.geography_location, t2.statutory_nature,
    t2.statutory, t2.statutory_provision, t2.compliance_task,
    t2.compliance_description, t2.penal_consequences,
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
END //

DELIMITER ;


DROP PROCEDURE IF EXISTS `sp_statutory_mapping_view_by_csvid`;

DELIMITER //

CREATE PROCEDURE `sp_statutory_mapping_view_by_csvid`(
IN csvid INT, f_count INT, f_range INT

)
BEGIN
    select t1.csv_id, t1.country_name,
    t1.domain_name, t1.csv_name, t1.uploaded_by, t1.uploaded_on,
    t2.bulk_statutory_mapping_id, t2.s_no,
    t2.organization, t2.geography_location, t2.statutory_nature,
    t2.statutory, t2.statutory_provision, t2.compliance_task,
    t2.compliance_description, t2.penal_consequences,
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
        UPDATE tbl_bulk_statutory_mapping set action = 3

    end if;

END //

DELIMITER ;

-- --------------------------------------------------------------------------------
-- To get the client unit bulk uploaded file slist
-- --------------------------------------------------------------------------------
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
    t1.csv_unit_id and action = 2) AS rej_count
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
    t1.uploaded_by

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

DROP PROCEDURE IF EXISTS `sp_assgined_statutory_bulk_reportdata`;

DELIMITER //
CREATE PROCEDURE `sp_assgined_statutory_bulk_reportdata`(
    IN `client_group_id` int(11),
    IN `legal_entity_id` int(11),
    IN `unit_id` varchar(100),
    IN `from_date` date,
    IN `to_date` date,
    IN `from_limit` int,
    IN `to_limit` int,
    IN `user_ids` varchar(100)
    )
BEGIN
IF (unit_id='') THEN
  SELECT  t1.uploaded_by, t1.uploaded_on,t1.csv_name, t1.total_records, t1.total_rejected_records,
  t1.approved_by,t1.rejected_by,t1.approved_on, t1.rejected_on,t1.is_fully_rejected,t1.approve_status
  FROM tbl_bulk_assign_statutory_csv AS t1
  INNER JOIN tbl_bulk_assign_statutory AS t2 ON t2.csv_assign_statutory_id=t1.csv_assign_statutory_id
  WHERE
   FIND_IN_SET(t1.uploaded_by, user_ids) AND
  (DATE_FORMAT(date(t1.uploaded_on),"%Y-%m-%d") BETWEEN date(from_date) and date(to_date))
  ORDER BY t1.uploaded_on DESC
  LIMIT from_limit, to_limit;

  SELECT count(0) as total
  FROM tbl_bulk_assign_statutory_csv AS t1
  INNER JOIN tbl_bulk_assign_statutory AS t2 ON t2.csv_assign_statutory_id=t1.csv_assign_statutory_id
  WHERE FIND_IN_SET(t1.uploaded_by, user_ids)
  AND (DATE_FORMAT(date(t1.uploaded_on),"%Y-%m-%d") BETWEEN date(from_date) and date(to_date))
  ORDER BY t1.uploaded_on DESC;
ELSE
  SELECT  t2.unit_code, t1.uploaded_by, t1.uploaded_on,t1.csv_name, t1.total_records, t1.total_rejected_records,
  t1.approved_by,t1.rejected_by,t1.approved_on, t1.rejected_on,t1.is_fully_rejected,t1.approve_status
  FROM tbl_bulk_assign_statutory_csv AS t1
  INNER JOIN tbl_bulk_assign_statutory AS t2 ON t2.csv_assign_statutory_id=t1.csv_assign_statutory_id
  WHERE
   t2.unit_code=unit_id AND
   FIND_IN_SET(t1.uploaded_by, user_ids) AND
  (DATE_FORMAT(date(t1.uploaded_on),"%Y-%m-%d") BETWEEN date(from_date) and date(to_date))
  ORDER BY t1.uploaded_on DESC
  LIMIT from_limit, to_limit;

  SELECT count(0) as total
  FROM tbl_bulk_assign_statutory_csv AS t1
  INNER JOIN tbl_bulk_assign_statutory AS t2 ON t2.csv_assign_statutory_id=t1.csv_assign_statutory_id
  WHERE
  t2.unit_code=unit_id AND
  FIND_IN_SET(t1.uploaded_by, user_ids)
  AND (DATE_FORMAT(date(t1.uploaded_on),"%Y-%m-%d") BETWEEN date(from_date) and date(to_date))
  ORDER BY t1.uploaded_on DESC;
END IF;

END //
DELIMITER ;


-- --------------------------------------------------------------------------------
-- To delete the rejected statutory mapping record by csv id
-- --------------------------------------------------------------------------------

DROP PROCEDURE IF EXISTS `sp_delete_reject_sm_by_csvid`;

DELIMITER //
CREATE PROCEDURE `sp_delete_reject_sm_by_csvid`(IN `csvid` int)
BEGIN
Declare isfullyrejected int default 0;
SET isfullyrejected=(select is_fully_rejected from tbl_bulk_statutory_mapping_csv where csv_id=csvid);

 if isfullyrejected=1 then
  Delete FROM tbl_bulk_statutory_mapping WHERE csv_id=csvid;
 else
  Delete FROM tbl_bulk_statutory_mapping WHERE csv_id=csvid AND action=3;
 end if;
END//
DELIMITER ;


DROP PROCEDURE IF EXISTS `sp_rejected_statutory_mapping_reportdata`;

DELIMITER //
CREATE PROCEDURE `sp_rejected_statutory_mapping_reportdata`(IN `country_id` int(11), IN `domain_id` int(11), IN `user_id` int(11))
BEGIN
 SELECT DISTINCT sm.csv_id,
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
(SELECT COUNT(*) FROM tbl_bulk_statutory_mapping WHERE csv_id = sm_csv.csv_id AND action=3) AS declined_count

FROM tbl_bulk_statutory_mapping AS sm
INNER JOIN tbl_bulk_statutory_mapping_csv AS sm_csv ON sm_csv.csv_id=sm.csv_id
 WHERE
  sm_csv.country_id=country_id AND
  sm_csv.domain_id=domain_id AND
  sm_csv.uploaded_by=user_id AND
  (sm.action=3 OR sm_csv.is_fully_rejected=1) -- Declined Action
  ORDER BY sm_csv.uploaded_on ASC;
END//
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

CREATE PROCEDURE `sp_client_unit_bulk_reportdata`(IN `client_group_id` int(11), IN `from_date` date, IN `to_date` date, IN `from_limit` int(11), IN `to_limit` int(11), IN `user_ids` varchar(100))
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
t1.approve_status
FROM tbl_bulk_units_csv AS t1
INNER JOIN tbl_bulk_units AS t2 ON t2.csv_unit_id=t1.csv_unit_id
WHERE
FIND_IN_SET(t1.uploaded_by, user_ids) AND
(DATE_FORMAT(date(t1.uploaded_on),"%Y-%m-%d")
BETWEEN date(from_date) and date(to_date))
ORDER BY t1.uploaded_on DESC
LIMIT from_limit, to_limit;

SELECT count(0) as total
FROM tbl_bulk_units_csv AS t1
INNER JOIN tbl_bulk_units AS t2 ON t2.csv_unit_id=t1.csv_unit_id
WHERE
FIND_IN_SET(t1.uploaded_by, user_ids) AND
(DATE_FORMAT(date(t1.uploaded_on),"%Y-%m-%d")
BETWEEN date(from_date) and date(to_date))
ORDER BY t1.uploaded_on DESC;

END//
DELIMITER ;

DROP PROCEDURE IF EXISTS `cu_delete_unit_by_csvid`;

DELIMITER //

CREATE PROCEDURE `cu_delete_unit_by_csvid`(IN `csvid` int(11))
BEGIN
Declare isfullyrejected int default 0;
SET isfullyrejected=(select is_fully_rejected from tbl_bulk_units_csv where csv_unit_id=csvid);

 if isfullyrejected=1 then
  Delete FROM tbl_bulk_units WHERE csv_unit_id=csvid;
 else
  Delete FROM tbl_bulk_units WHERE csv_unit_id=csvid AND action=3;
 end if;
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

  (cu.action=3 OR cu_csv.is_fully_rejected=1) -- Declined Action
  ORDER BY cu_csv.uploaded_on ASC;
END//
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
IN csvid INT, domain_name VARCHAR(50), unit_name VARCHAR(50),
p_legis VARCHAR(200), s_legis VARCHAR(200), s_prov VARCHAR(500),
c_task VARCHAR(100), c_desc VARCHAR(500), f_count INT, f_range INT

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

    and t2.domain like domain_name and t2.unit_name like unit_name
    and t2.perimary_legislation like p_legis and t2.secondary_legislation like s_legis
    and t2.statutory_provision like s_prov and t2.compliance_task_name like c_task
    and t2.compliance_description like c_desc
    limit  f_count, f_range;
END //

DELIMITER ;