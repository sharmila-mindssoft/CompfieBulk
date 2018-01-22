
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

