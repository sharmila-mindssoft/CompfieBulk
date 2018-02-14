from ..buapiprotocol import bustatutorymappingprotocol as bu_sm

__all__ = [
    "get_uploaded_statutory_mapping_csv_list",
    "save_mapping_csv", "save_mapping_data",
    "get_pending_mapping_list"
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
            d.get("country_id"), d.get("country_name"), d.get("domain_id"), d.get("domain_name"),
            d.get("csv_id"), d.get("csv_name"), d.get("total_records"), d.get("total_documents"),
            d.get("uploaded_documents")
        ))

    return upload_more, csv_data


########################################################
'''
    returns new primary key from table
    :param
        db: database object
        args: list of procedure params
    :type
        db: Object
        args: List
    :returns
        result: return new id
    rtype:
        result: Integer
'''
########################################################

def save_mapping_csv(db, args):
    newid = db.call_insert_proc("sp_statutory_mapping_csv_save", args)
    return newid


########################################################
'''
    returns true if the data save properply
    :param
        db: database object
        csv_id: parent table id
        csv_data: list of data to save
    :type
        db: Object
        csv_id: Integer
        csv_data: List
    :returns
        result: return boolean
    rtype:
        result: Boolean
'''
########################################################

def save_mapping_data(db, csv_id, csv_data) :
    try:
        columns = [
            "csv_id", "s_no", "organization", "geography_location",
            "statutory_nature", "statutory", "statutory_provision",
            "compliance_task", "compliance_document", "compliance_description",
            "penal_consequences", "reference_link", "compliance_frequency",
            "statutory_month", "statutory_date", "trigger_before",
            "repeats_every", "repeats_type", "repeat_by", "duration", "duration_type",
            "multiple_input", "format_file", "task_id", "task_type"
        ]
        values = []

        for idx, d in enumerate(csv_data) :
            print d
            values.append((
                csv_id, idx + 1, d["Organization"], d["Applicable_Location"],
                d["Statutory_Nature"], d["Statutory"], d["Statutory_Provision"],
                d["Compliance_Task"], d["Compliance_Document"],
                d["Compliance_Description"], d["Penal_Consequences"],
                d["Reference_Link"], d["Compliance_Frequency"], d["Statutory_Month"],
                d["Statutory_Date"], d["Trigger_Days"], d["Repeats_Every"], d["Repeats_Type"],
                d["Repeats_By (DOM/EOM)"], d["Duration"], d["Duration_Type"], d["Multiple_Input_Section"],
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

########################################################
'''
    returns statutory mapping csv list which waiting for approval
    :param
        db: database object
        session_user: logged in user details
    :type
        db: Object
        session_user: Object
    :returns
        result: list of pending csv data Object
    rtype:
        result: List
'''
########################################################

def get_pending_mapping_list(db, session_user):
    csv_data = []
    data = db.call_proc("sp_pending_statutory_mapping_csv_list", [session_user.user_id()])

    for d in data :
        file_name = d["csv_name"].split('.')
        remove_code = file_name[0].split('_')
        csv_name = "%s.%s" % ('_'.join(remove_code[:-1]), file_name[1])
        csv_data.append(bu_sm.PendingCsvList(
            d["csv_id"], csv_name, session_user.user_full_name(),
            d["uploaded_on"], d["total_records"], d["action_count"],
            d["csv_name"]
        ))

    return csv_data


def get_filters_for_approve(db, csv_id):
    data = db.call_proc_with_multiresult_set("sp_statutory_mapping_filter_list", [csv_id], 8)
    org_names = []
    s_natures = []
    statutories = []
    frequencies = []
    geo_locations = []
    c_tasks = []
    c_descs = []
    c_docs = []
    if len(data) > 0 :

