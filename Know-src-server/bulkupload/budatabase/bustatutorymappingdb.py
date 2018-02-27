from ..buapiprotocol import bustatutorymappingprotocol as bu_sm
import datetime


__all__ = [
    "get_uploaded_statutory_mapping_csv_list",
    "save_mapping_csv",
    "save_mapping_data",
    "fetch_bulk_report",
    "fetch_assigned_statutory_bulk_report",
    "save_mapping_csv", "save_mapping_data",
    "get_pending_mapping_list",
    "get_filters_for_approve",
    "get_statutory_mapping_by_filter",
    "fetch_rejected_statutory_mapping_bulk_report",
    "get_list_and_delete_rejected_statutory_mapping_by_csv_id",
    "update_download_count_by_csvid"
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

            values.append((
                csv_id, idx + 1, d["Organization"], d["Applicable_Location"],
                d["Statutory_Nature"], d["Statutory"], d["Statutory_Provision"],
                d["Compliance_Task"], d["Compliance_Document"],
                d["Compliance_Description"], d["Penal_Consequences"],
                d["Reference_Link"], d["Compliance_Frequency"], d["Statutory_Month"],
                d["Statutory_Date"], d["Trigger_Days"],
                None if d["Repeats_Every"] == '' else d["Repeats_Every"],
                d["Repeats_Type"],
                None if d["Repeats_By (DOM/EOM)"] == '' else d["Repeats_By (DOM/EOM)"],
                None if d["Duration"] == '' else d["Duration"],
                d["Duration_Type"], d["Multiple_Input_Section"],
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
    returns statutory mapping bulk report list
    :param
        db: database object
        session_user: logged in user details
    :type
        db: Object
        session_user: Object
    :returns
        result: list of bulk data records by mulitple country, 
        domain, KnowledgeExecutives selections based.
    rtype:
        result: List
'''
########################################################

def fetch_bulk_report(db, session_user, 
    user_id, country_ids, domain_ids, from_date, to_date, 
    record_count, page_count, child_ids, user_category_id):
    reportdatalist=[]
    expected_result=2

    domain_id_list=convertArrayToString(domain_ids)
    country_id_list=convertArrayToString(country_ids)  

    if(user_category_id==3):
        user_ids=convertArrayToString(child_ids)
    elif(user_category_id==5 and user_category_id!=3):
        user_ids=convertArrayToString(child_ids)
    else:
        user_ids=user_id

    args = [user_ids, country_id_list, domain_id_list, from_date, to_date, record_count, page_count]
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

def convertArrayToString(array_ids):
    existing_id=[]
    id_list=""
    if(len(array_ids)>1):
        for d in array_ids :
         if d in existing_id:
           break
         id_list+=str(d)+","
         existing_id.append(d)
        id_list=id_list.rstrip(',');
    else : 
        id_list=array_ids[0]
    return id_list




########################################################
'''
    returns statutory mapping bulk report list
    :param
        db: database object
        session_user: logged in user details
    :type
        db: Object
        session_user: Object
    :returns
        result: list of bulk data records by mulitple country, 
        domain, KnowledgeExecutives selections based.
    rtype:
        result: List
'''
########################################################

def fetch_assigned_statutory_bulk_report(db, session_user, user_id, 
    clientGroupId, legalEntityId, unitId, from_date, to_date, 
    record_count, page_count, child_ids, user_category_id):
    reportdatalist=[]
    expected_result=2

    if(len(child_ids)>0):
        if(user_category_id==7):
            user_ids=convertArrayToString(child_ids)
        elif(user_category_id==8 and user_category_id!=7):
            user_ids=convertArrayToString(child_ids)
        else:
            user_ids=user_id

    args = [clientGroupId, legalEntityId, unitId, from_date, to_date, record_count, page_count, str(user_ids)]
    data = db.call_proc_with_multiresult_set('sp_assgined_statutory_bulk_reportdata', args, expected_result)


    reportdata=data[0]
    total_record=data[1][0]["total"] 

    for d in reportdata :

        uploaded_on = datetime.datetime.strptime(str(d["uploaded_on"]), 
            '%Y-%m-%d %H:%M:%S').strftime('%d-%b-%Y %H:%M');

        approved_on = datetime.datetime.strptime(str(d["approved_on"]), 
            '%Y-%m-%d %H:%M:%S').strftime('%d-%b-%Y %H:%M');

        rejected_on = datetime.datetime.strptime(str(d["rejected_on"]), 
            '%Y-%m-%d %H:%M:%S').strftime('%d-%b-%Y %H:%M');

        reportdatalist.append(bu_sm.StatutoryReportData(
             str(d["uploaded_by"]),
             str(uploaded_on),
             str(d["csv_name"]),
             int(d["total_records"]),
             int(d["total_rejected_records"]),
             str(d["approved_by"]),
             str(d["rejected_by"]),
             str(approved_on),
             str(rejected_on),
             int(d["is_fully_rejected"]),
             int(d["approve_status"])
        )) 

    return reportdatalist, total_record

########################################################
'''
    returns statutory mapping bulk report list
    :param
        db: database object
        session_user: logged in user details
    :type
        db: Object
        session_user: Object
    :returns
        result: list of bulk data records by mulitple country, 
        domain, KnowledgeExecutives selections based.
    rtype:
        result: List
'''
########################################################

def fetch_client_unit_bulk_report(db, session_user, user_id, 
    clientGroupId, from_date, to_date, 
    record_count, page_count, child_ids, user_category_id):
    
    clientdatalist=[]
    expected_result=2

    if(len(child_ids)>0):
        if(user_category_id==7):
            user_ids=convertArrayToString(child_ids)
        elif(user_category_id==8 and user_category_id!=7):
            user_ids=convertArrayToString(child_ids)
        else:
            user_ids=user_id

    args = [clientGroupId, from_date, to_date, record_count, page_count, str(user_ids)]
    data = db.call_proc_with_multiresult_set('sp_client_unit_bulk_reportdata', args, expected_result)


    clientdata=data[0]
    total_record=data[1][0]["total"] 

    for d in clientdata :

        uploaded_on = datetime.datetime.strptime(str(d["uploaded_on"]), 
            '%Y-%m-%d %H:%M:%S').strftime('%d-%b-%Y %H:%M');

        approved_on = datetime.datetime.strptime(str(d["approved_on"]), 
            '%Y-%m-%d %H:%M:%S').strftime('%d-%b-%Y %H:%M');

        rejected_on = datetime.datetime.strptime(str(d["rejected_on"]), 
            '%Y-%m-%d %H:%M:%S').strftime('%d-%b-%Y %H:%M');

        clientdatalist.append(bu_sm.StatutoryReportData(
             str(d["uploaded_by"]),
             str(uploaded_on),
             str(d["csv_name"]),
             int(d["total_records"]),
             int(d["total_rejected_records"]),
             str(d["approved_by"]),
             str(d["rejected_by"]),
             str(approved_on),
             str(rejected_on),
             int(d["is_fully_rejected"]),
             int(d["approve_status"])
        )) 

    return clientdatalist, total_record

########################################################
'''
    returns statutory mapping bulk report list
    :param
        db: database object
        session_user: logged in user details
    :type
        db: Object
        session_user: Object
    :returns
        result: list of bulk data records by mulitple country, 
        domain, KnowledgeExecutives selections based.
    rtype:
        result: List
'''
########################################################

def fetch_rejected_statutory_mapping_bulk_report(db, session_user, 
    user_id, country_id, domain_id):

    rejectdatalist=[]
    args = [country_id, domain_id, user_id]
    data = db.call_proc('sp_rejected_statutory_mapping_reportdata', args)


    for d in data:
        uploaded_on = datetime.datetime.strptime(str(d["uploaded_on"]), 
            '%Y-%m-%d').strftime('%d-%b-%Y %H:%M');

        approved_on = datetime.datetime.strptime(str(d["approved_on"]), 
            '%Y-%m-%d %H:%M:%S').strftime('%d-%b-%Y %H:%M');

        rejected_on = datetime.datetime.strptime(str(d["rejected_on"]), 
            '%Y-%m-%d %H:%M:%S').strftime('%d-%b-%Y %H:%M');

        if (d["rejected_file_download_count"] is None):
            download_count=0
        else:
            download_count=d["rejected_file_download_count"]

        rejectdatalist.append(bu_sm.StatutorMappingRejectData(
             int(d["csv_id"]),
             str(d["uploaded_by"]),
             str(uploaded_on),
             str(d["csv_name"]),
             int(d["total_records"]),
             int(d["total_rejected_records"]),
             str(d["approved_by"]),
             str(d["rejected_by"]),
             str(approved_on),
             str(rejected_on),
             int(d["is_fully_rejected"]),
             int(d["approve_status"]),
             int(download_count),
             str(d["remarks"]),
             d["action"],
             int(d["declined_count"])
             
        )) 
    return rejectdatalist

def get_list_and_delete_rejected_statutory_mapping_by_csv_id(db, session_user, 
    user_id, country_id, domain_id, csv_id):

    args = [csv_id]
    data = db.call_proc('sp_delete_reject_sm_by_csvid', args)

    rejectdatalist=fetch_rejected_statutory_mapping_bulk_report(db, session_user, 
    user_id, country_id, domain_id)

    return rejectdatalist

def update_download_count_by_csvid(db, session_user, csv_id):
    updated_count=[];
    args = [csv_id]
    data = db.call_proc('sp_update_download_count_by_csvid', args)
    for d in data:
        updated_count.append(bu_sm.SMRejectUpdateDownloadCount(
             int(d["csv_id"]), int(d["rejected_file_download_count"])
        )) 
    return updated_count

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

########################################################
'''
    returns select fileds in list for the given csv id
    :param
        db: database object
        csv_id: viewed csv id
    :type
        db: Object
        csv_id: INT
    :returns
        result: return filtered list in Api Object
    rtype:
        result: Object
'''
########################################################

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
        if len(data[0]) > 0:
            for d in data[0]:
                org_names.append(d["oraganization"])

        if len(data[1]) > 0:
            for d in data[1]:
                s_natures.append(d["statutory_nature"])

        if len(data[2]) > 0:
            for d in data[2]:
                statutories.append(d["statutory"].strip().split('|;|'))
                statutories = list(set(statutories))

        if len(data[3]) > 0:
            for d in data[3]:
                frequencies.append(d["compliance_frequency"])

        if len(data[4]) > 0:
            for d in data[4]:
                geo_locations.extend(d["geography_location"].strip().split('|;|'))
                geo_locations = list(set(geo_locations))

        if len(data[5]) > 0:
            for d in data[5]:
                c_tasks.append(d["compliance_tasl"])

        if len(data[6]) > 0:
            for d in data[6]:
                c_descs.append(d["compliance_description"])

        if len(data[7]) > 0:
            for d in data[7]:
                c_docs.append(d["compliance_document"])

    return bu_sm.GetApproveMappingFilterSuccess(
        org_names, s_natures, statutories, frequencies, geo_locations,
        c_tasks, c_descs, c_docs
    )


def get_statutory_mapping_by_filter(db, request_frame, session_user):
    csv_id = request_frame.csv_id
    organization = request_frame.orga_name
    s_nature = request_frame.s_nature
    frequency = request_frame.frequency
    statutory = request_frame.statutory
    geo_location = request_frame.geo_location
    c_task = request_frame.c_task_name
    c_desc = request_frame.c_desc
    c_doc = request_frame.c_doc
    f_count = request_frame.f_count
    f_range = request_frame.f_range
    if organization is None or organization == "":
        organization = '%'

    if s_nature is None or s_nature == "":
        s_nature = '%'

    if frequency is None or frequency == "":
        frequency = '%'

    if statutory is None or statutory == "":
        statutory = '%'

    if geo_location is None or geo_location == "":
        geo_location = '%'

    if c_task is None or c_task == "":
        c_task = '%'

    if c_desc is None or c_desc == "":
        c_desc = '%'

    if c_doc is None or c_doc == "":
        c_doc = '%'

    data = db.call_proc(
        "sp_statutory_mapping_view_by_filter",
        [
            csv_id, organization, s_nature, frequency,
            statutory, geo_location, c_task, c_desc, c_doc,
            f_count, f_range
        ]
    )
    country_name = None
    domain_name = None
    csv_name = None
    upload_by = session_user.user_full_name()
    upload_on = None
    mapping_data = []
    if len(data) > 0 :
        for idx, d in enumerate(data) :
            if idx == 0 :
                country_name = d["country_name"]
                domain_name = d["domain_name"]
                csv_name = d["csv_name"]
                upload_on = d["uploaded_on"]

            mapping_data.append(bu_sm.MappingData(
                d["bulk_statutory_mapping_id"],
                d["oraganization"], d["geography_location"],
                d["statutory_nature"], d["statutory"],
                d["statutory_provision"], d["compliance_task"],
                d["compliance_document"], d["compliance_description"],
                d["penal_consequences"], d["reference_link"],
                d["compliance_frequency"], d["statutory_month"],
                d["statutory_date"], d["trigger_before"], d["repeats_every"],
                d["repeats_type"], d["repeat_by"], d["duration"], d["duration_type"],
                d["multiple_input"], d["format_file"],  d["task_id"], d["task_type"],
                d["action"], d["remarks"]
            ))

    return bu_sm.GetApproveStatutoryMappingViewSuccess(
        country_name, domain_name, csv_name, upload_by,
        upload_on, csv_id, mapping_data
    )

def get_statutory_mapping_by_csv_id(db, request_frame, session_user):
    csv_id = request_frame.csv_id
    f_count = request_frame.f_count
    f_range = request_frame.f_range
    data = db.call_proc("sp_statutory_mapping_view_by_csvid", [
        csv_id, f_count, f_range
    ])
    country_name = None
    domain_name = None
    csv_name = None
    upload_by = session_user.user_full_name()
    upload_on = None
    mapping_data = []
    if len(data) > 0 :
        for idx, d in enumerate(data) :
            if idx == 0 :
                country_name = d["country_name"]
                domain_name = d["domain_name"]
                csv_name = d["csv_name"]
                upload_on = d["uploaded_on"]

            mapping_data.append(bu_sm.MappingData(
                d["bulk_statutory_mapping_id"],
                d["oraganization"], d["geography_location"],
                d["statutory_nature"], d["statutory"],
                d["statutory_provision"], d["compliance_task"],
                d["compliance_document"], d["compliance_description"],
                d["penal_consequences"], d["reference_link"],
                d["compliance_frequency"], d["statutory_month"],
                d["statutory_date"], d["trigger_before"], d["repeats_every"],
                d["repeats_type"], d["repeat_by"], d["duration"], d["duration_type"],
                d["multiple_input"], d["format_file"],  d["task_id"], d["task_type"],
                d["action"], d["remarks"]
            ))
    return bu_sm.GetApproveStatutoryMappingViewSuccess(
        country_name, domain_name, csv_name, upload_by,
        upload_on, csv_id, mapping_data
    )

def update_approve_action_from_list(db, csv_id, action, remarks, session_user):
    args = [csv_id, action, remarks, session_user.user_id()]
    if (db.call_proc("sp_statutory_mapping_update_action", args)) :
        return True
    else :
        return False
