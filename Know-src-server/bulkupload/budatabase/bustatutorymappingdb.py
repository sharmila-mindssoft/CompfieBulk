from ..buapiprotocol import bustatutorymappingprotocol as bu_sm


__all__ = [
    "get_uploaded_statutory_mapping_csv_list",
    "save_mapping_csv",
    "save_mapping_data",
    "fetch_statutory_mapping_bulk_report"

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

def save_mapping_csv(db, args):
    newid = db.call_insert_proc("sp_statutory_mapping_csv_save", args)
    return newid

def save_mapping_data(db, csv_id, csv_data) :
    try:
        columns = [
            "csv_id", "s_no", "organization", "geography_location",
            "statutory_nature", "statutory", "statutory_provision",
            "compliance_task", "compliance_document", "compliance_description",
            "penal_consequences", "reference_link", "compliance_frequency",
            "statutory_month", "statutory_date", "trigger_before",
            "repeats_every", "repeats_type", "repeat_by", "duration", "duration_type",
            "multiple_type", "format_file", "task_id", "task_type"
        ]
        values = []
        for idx, d in enumerate(csv_data) :
            values.append((
                csv_id, idx + 1, d["Organization"]. d["Applicable_Location"],
                d["Statutory_Nature"], d["Statutory"], d["Statutory_Provision"],
                d["Compliance_Task"], d["Compliance_Document"],
                d["Compliance_Description"], d["Penal_Consequences"],
                d["Reference_Link"], d["Compliance_Frequency"], d["Statutory_Month"],
                d["Statutory_Date"], d["Trigger_Days"], d["Repeats_Every"], d["Repeats_Type"],
                d["Repeats_By"], d["Duration"], d["Duration_Type"], d["Multiple_Input_Section"],
                d["Format"], d["Task_ID"], d["Task_Type"],
            ))

        if values :
            db.bulk_insert("tbl_bulk_statutory_mapping", columns, values)
            return True
        else :
            return False
    except Exception, e:
        print str(e)
        raise ValueError("Transaction failed")

def convertArrayToString(array_ids):
    existing_id=[]
    id_list=""
    for d in array_ids :
     if d in existing_id:
       break
     id_list+=str(d)+","
     existing_id.append(d)
    id_list=id_list.rstrip(',');
    return id_list

def fetch_statutory_mapping_bulk_report(db, session_user, 
    user_id, country_ids, domain_ids, from_date, to_date, record_count, page_count):
    reportdatalist=[]
    expected_result=2

    domain_id_list=convertArrayToString(domain_ids)
    country_id_list=convertArrayToString(country_ids)

    args = [str(user_id), country_id_list, domain_id_list, from_date, to_date, record_count, page_count]
    data = db.call_proc_with_multiresult_set('sp_tbl_statutory_mappings_bulk_reportdata', args, expected_result)
    
    reportdata=data[0]
    total_record=data[1][0]["total"]

    for d in reportdata :
        reportdatalist.append(bu_sm.ReportData(
             str(d["country_name"]),
             str(d["domain_name"]),
             str(d["uploaded_by"]),
             str(d["uploaded_on"]),
             str(d["csv_name"]),
             int(d["total_records"]),
             int(d["total_rejected_records"]),
             str(d["approved_by"]),
             str(d["rejected_by"]),
             str(d["approved_on"]),
             str(d["rejected_on"]),
             int(d["is_fully_rejected"]),
             int(d["approve_status"])
        )) 

    
    return reportdatalist, total_record



