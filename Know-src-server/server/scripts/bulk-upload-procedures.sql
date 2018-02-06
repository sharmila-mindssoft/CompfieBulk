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
IN uploadedby INT, c_id INT, c_name: VARCHAR, d_id: INT,
    d_name: VARCHAR, csv_name VARCHAR,no_of_records INT,
    no_of_docs INT, uploaded_docs INT
)
BEGIN
    INSERT INTO tbl_bulk_statutory_mapping_csv(country_id, domain_id,
        country_name, domain_name, csv_name, uploaded_by, uploaded_on,
        total_records, total_documents, uploaded_documents)
    VALUES (c_id, d_id, c_name, d_name, csv_name, uploadedby,
        current_ist_datetime(), no_of_records, no_of_docs,
        uploaded_docs
    );
END //

DELIMITER ;


CREATE PROCEDURE `sp_statutory_mapping_csv_data_save`(
IN uploadedby INT, csv_id INT, s_no INT, org VARCHAR, geo_location VARCHAR,
    s_nature VARCHAR, statu VARCHAR, s_provision VARCHAR,
    c_task VARCHAR, c_doc VARCHAR, c_desc VARCHAR, p_cons VARCHAR,
    refer VARCHAR, frequency VARCHAR, s_month VARCHAR, s_date VARCHAR,
    trigger VARCHAR, r_every VARCHAR, r_type VARCHAR, r_by VARCHAR,
    dur VARCHAR, dur_type VARCHAR, multiple VARCHAR, format VARCHAR
)
BEGIN
    INSERT INTO tbl_bulk_statutory_mapping(csv_id, s_no, organzation,
        geography_location, statutory_nature, statutory, statutory_provision,
        compliance_task, compliance_document, compliance_description,
        penal_consequences, reference_link, compliance_frequency,
        statutory_month, statutory_date, trigger_before, repeats_every,
        repeats_type, repeat_by, duration, duration_type,
        multiple_input, format_file
    )
    VALUES (csv_id, s_no, org, geo_location, s_nature, statu, s_provision,
            c_task, c_doc, c_desc, p_cons, refer, frequency, s_month,
            s_date, trigger, r_every, r_type, r_by, dur, dur_type,
            multiple, format
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
