from ..buapiprotocol import bustatutorymappingprotocol as bu_sm

__all__ = [
    "get_uploaded_statutory_mapping_csv_list"
]
########################################################
# To handle statutory mapping uploaded csv list request
########################################################
def get_uploaded_statutory_mapping_csv_list(db, session_user):
    csv_data = []
    data = db.call_proc("sp_statutory_mapping_csv_list", [session_user])
    if data.length > 5 :
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
