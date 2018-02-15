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


CREATE PROCEDURE `sp_statutory_mapping_csv_data_save`(
IN csv_id INT, s_no INT, org LONGTEXT, geo_location LONGTEXT,
    s_nature VARCHAR(50), statu LONGTEXT, s_provision VARCHAR(500),
    c_task VARCHAR(100), c_doc(100) VARCHAR, c_desc LONGTEXT, p_cons LONGTEXT,
    refer LONGTEXT, frequency LONGTEXT, s_month LONGTEXT, s_date LONGTEXT,
    trigger LONGTEXT, r_every INT, r_type LONGTEXT, r_by INT,
    dur INT, dur_type LONGTEXT, multiple VARCHAR(5), format LONGTEXT,
    taskid INT, tasktype VARCHAR(100)
)
BEGIN
    INSERT INTO tbl_bulk_statutory_mapping(csv_id, s_no, organzation,
        geography_location, statutory_nature, statutory, statutory_provision,
        compliance_task, compliance_document, compliance_description,
        penal_consequences, reference_link, compliance_frequency,
        statutory_month, statutory_date, trigger_before, repeats_every,
        repeats_type, repeat_by, duration, duration_type,
        multiple_input, format_file, task_id, task_type
    )
    VALUES (csv_id, s_no, org, geo_location, s_nature, statu, s_provision,
            c_task, c_doc, c_desc, p_cons, refer, frequency, s_month,
            s_date, trigger, r_every, r_type, r_by, dur, dur_type,
            multiple, format, taskid, tasktype
    );
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


----------------------------------
-- Statutory Mapping - Bulk Report
----------------------------------
DROP PROCEDURE IF EXISTS `sp_tbl_statutory_mappings_bulk_reportdata`;;
CREATE PROCEDURE `sp_tbl_statutory_mappings_bulk_reportdata`(IN `user_id` varchar(100), IN `country_ids` varchar(100), IN `domain_ids` varchar(100), IN `from_date` date, IN `to_date` date, IN `from_limit` int(11), IN `to_limit` int(11))
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

END;;