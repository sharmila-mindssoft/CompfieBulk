from ..buapiprotocol import bustatutorymappingprotocol as bu_sm


__all__ = [
    "get_uploaded_statutory_mapping_csv_list",
    "get_statutory_mapping_bulk_report_data_list"
]
########################################################
# Return the uploaded statutory mapping csv list
# :param db : database class object
# :type db  : Object
# :param session_user : user id who currently logged in
# :type session_user : String
# :returns : upload_mmore : flag which defines user upload rights
# :returns : csv_data: list of uploaded csv_data
# rtypes: Boolean, lsit of Object
########################################################
def get_uploaded_statutory_mapping_csv_list(db, session_user):
    csv_data = []
    data = db.call_proc("sp_statutory_mapping_csv_list", [session_user])
    if len(data) > 5 :
        upload_more = False
    else :
        upload_more = True
    for d in data :
        csv_data.append(bu_sm.CsvList(
            d.country_id, d.country_name, d.domain_id, d.domain_name,
            d.csv_id, d.csv_name, d.total_records, d.total_documents,
            d.uploaded_documents
        ))

    return upload_more, csv_data

def get_statutory_mapping_bulk_report_data_list(db, session_user):
    # , country_id, domain_id, from_date, to_date, record_count, page_count
    print "Reports Before"
    data = db.call_proc("sp_tbl_statutory_mappings_bulk_reportsss", [session_user])

    print "Report Data"
    print data

    report_data=''
    total_record='5'
    # if len(data) > 5 :
    #     upload_more = False
    # else :
    #     upload_more = True
    # for d in data :
    #     csv_data.append(bu_sm.CsvList(
    #         d.country_id, d.country_name, d.domain_id, d.domain_name,
    #         d.csv_id, d.csv_name, d.total_records, d.total_documents,
    #         d.uploaded_documents
    #     ))

    return report_data, total_record

