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



DROP PROCEDURE IF EXISTS `sp_client_info`;

DELIMITER //

CREATE PROCEDURE `sp_client_info`(
    IN uid INT(11)
)
BEGIN
    -- group details
    select distinct t1.client_id, t1.group_name, t1.is_active
     from tbl_client_groups as t1
     inner join tbl_user_units as t2
     on t1.client_id = t2.client_id where t2.user_id = uid;

    -- legal entity details
    select distinct t1.client_id, t1.legal_entity_id, t1.legal_entity_name
     from tbl_legal_entities as t1
     inner join tbl_user_units as t2
     on t1.legal_entity_id = t2.legal_entity_id where t2.user_id = uid;

    -- domains
    select distinct t1.domain_name, t3.domain_id, t3.legal_entity_id
     from tbl_domains as t1
     inner join tbl_user_units as t3 on t1.domain_id = t3.domain_id
     where t3.user_id = uid;


END //

DELIMITER ;