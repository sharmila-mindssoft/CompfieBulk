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
    domain in (domain_name) and unit_name in (unitname_);
END //

DELIMITER ;