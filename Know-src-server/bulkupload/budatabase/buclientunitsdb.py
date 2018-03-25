from server.exceptionmessage import fetch_error
import traceback
from server import logger
from ..buapiprotocol import buclientunitsprotocol as bu_cu
import datetime

__all__ = [
    "save_client_units_mapping_csv",
    "save_mapping_client_unit_data",
    "get_ClientUnits_Uploaded_CSVList",
    "fetch_rejected_client_unit_report",
    "update_unit_count",
    "get_list_and_delete_rejected_unit",
    "fetch_client_unit_bulk_report",
    "fetch_rejected_cu_download_csv_report",
    "get_cu_csv_file_name_by_id",
    "update_bulk_client_unit_approve_reject_list",
    "get_bulk_client_units_and_filtersets_by_csv_id",
    "get_bulk_client_unit_list_by_filter",
    "save_client_unit_action_from_view",
    "get_bulk_client_unit_null_action_count",
    "get_bulk_client_unit_file_count"
]

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


def save_client_units_mapping_csv(db, args) :

    newid = db.call_insert_proc("sp_client_units_bulk_csv_save", args)
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


def save_mapping_client_unit_data(db, csv_id, csv_data) :

    try :
        columns = [
            "csv_unit_id", "legal_entity", "division", "category",
            "geography_level", "unit_location", "unit_code",
            "unit_name", "address", "city", "state", "postalcode",
            "domain", "organization", "action"
        ]
        values = []

        for idx, d in enumerate(csv_data) :
            values.append((
                csv_id, d["Legal_Entity"], d["Division"],
                d["Category"], d["Geography_Level"], d["Unit_Location"],
                d["Unit_Code"], d["Unit_Name"], d["Unit_Address"], d["City"],
                d["State"], d["Postal_Code"], d["Domain"], d["Organization"],
                0
            ))

        if values :
            db.bulk_insert("tbl_bulk_units", columns, values)
            return True
        else :
            return False
    except Exception, e :
        print e
        raise ValueError("Transaction failed")

########################################################
'''
    returns result set from table
    :param
        db: database object
        args: list of procedure params
    :type
        db: Object
        args: List
    :returns
        result: return result set of csv uploaded list
    rtype:
        result: Datatable
'''
########################################################


def get_ClientUnits_Uploaded_CSVList(db, clientId, groupName) :

    csv_list = []
    result = db.call_proc("sp_client_units_csv_list", [clientId, groupName])
    print "uploaded data"
    print result
    for row in result:
        csv_list.append(bu_cu.ClientUnitCSVList(
            row["csv_unit_id"], row["csv_name"], row["uploaded_by"],
            row["uploaded_on"], row["no_of_records"], row["approved_count"],
            row["rej_count"], row["declined_count"]
        ))
    return csv_list

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


def fetch_rejected_client_unit_report(db, session_user, user_id,
                                      client_group_id):

    rejectdatalist = []
    uploaded_on = ''
    approved_on = ''
    rejected_on = ''

    args = [client_group_id, user_id]
    data = db.call_proc('sp_rejected_client_unit_data', args)
    for d in data:
        if(d["uploaded_on"] is not None):
            uploaded_on = datetime.datetime.strptime(
                str(d["uploaded_on"]),
                '%Y-%m-%d %H:%M:%S').strftime('%d-%b-%Y %H:%M')

        if(d["approved_on"] is not None):
            approved_on = datetime.datetime.strptime(
                str(d["approved_on"]),
                '%Y-%m-%d %H:%M:%S').strftime('%d-%b-%Y %H:%M')

        if(d["rejected_on"] is not None):
            rejected_on = datetime.datetime.strptime(
                str(d["rejected_on"]),
                '%Y-%m-%d %H:%M:%S').strftime('%d-%b-%Y %H:%M')

        if (d["rejected_file_download_count"] is None):
            download_count = 0
        else:
            download_count = d["rejected_file_download_count"]

        rejectdatalist.append(bu_cu.ClientUnitRejectData(
             int(d["csv_unit_id"]),
             int(d["uploaded_by"]),
             str(uploaded_on),
             str(d["csv_name"]),
             int(d["total_records"]),
             d["total_rejected_records"],
             d["approved_by"],
             d["rejected_by"],
             str(approved_on),
             str(rejected_on),
             d["is_fully_rejected"],
             int(d["total_approve_records"]),
             int(download_count),
             str(d["remarks"]),
             d["action"],
             d["declined_count"],
             d["rejected_file_name"]
        ))
    return rejectdatalist


def update_unit_count(db, session_user, csv_id):
    updated_unit_count = []
    args = [csv_id]
    data = db.call_proc('cu_update_download_count', args)
    for d in data:
        updated_unit_count.append(bu_cu.UpdateUnitDownloadCount(
             int(d["csv_unit_id"]), int(d["rejected_file_download_count"])
        ))
    return updated_unit_count


def get_list_and_delete_rejected_unit(db, session_user, user_id,
                                      csv_id, bu_client_id):

    args = [csv_id]
    db.call_proc('sp_delete_reject_cu_by_csvid', args)
    rejectdatalist = fetch_rejected_client_unit_report(db, session_user,
                                                       user_id, bu_client_id)
    return rejectdatalist

def fetch_client_unit_bulk_report(db, session_user, user_id,
                                  clientGroupId, from_date, to_date,
                                  record_count, page_count, child_ids,
                                  user_category_id):

    clientdatalist = []
    expected_result = 2

    if(len(child_ids) > 0):
        if(user_category_id == 5):
            user_ids = convertArrayToString(child_ids)
        elif(user_category_id == 6 and user_category_id != 5):
            user_ids = convertArrayToString(child_ids)
        else:
            user_ids = user_id
    args = [clientGroupId, from_date, to_date, record_count, page_count,
            str(user_ids)]
    data = db.call_proc_with_multiresult_set('sp_client_unit_bulk_reportdata',
                                             args, expected_result)

    clientdata = data[0]
    total_record = data[1][0]["total"]
    approved_on = ""
    rejected_on = ""
    uploaded_on = ""
    if(clientdata):
        for d in clientdata:

            if(d["uploaded_on"] is not None):
                uploaded_on = d["uploaded_on"].strptime(
                          str(d["uploaded_on"]),
                          '%Y-%m-%d %H:%M:%S').strftime('%d-%b-%Y %H:%M')

            if(d["approved_on"] is not None):
                approved_on = d["approved_on"].strptime(
                              str(d["approved_on"]),
                              '%Y-%m-%d %H:%M:%S').strftime('%d-%b-%Y %H:%M')

            if(d["rejected_on"] is not None):
                rejected_on = d["rejected_on"].strptime(
                              str(d["rejected_on"]),
                              '%Y-%m-%d %H:%M:%S').strftime('%d-%b-%Y %H:%M')

            clientdatalist.append(bu_cu.StatutoryReportData(
                 int(d["uploaded_by"]),
                 str(uploaded_on),
                 str(d["csv_name"]),
                 int(d["total_records"]),
                 d["total_rejected_records"],
                 d["approved_by"],
                 d["rejected_by"],
                 str(approved_on),
                 str(rejected_on),
                 d["is_fully_rejected"],
                 d["total_approve_records"],
                 d["rejected_reason"]
            ))
    else:
            clientdatalist = []
            total_record = 0
    return clientdatalist, total_record

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

def fetch_rejected_cu_download_csv_report(db, session_user,
    user_id, cg_id, csv_id):

    rejectdatalist=[]
    args = [cg_id, csv_id, user_id]
    data = db.call_proc('sp_rejected_cu_csv_report', args)
    approved_on='0000-00-00'
    uploaded_on=''
    rejected_on=''

    if(data):
        for d in data:
            if(d["uploaded_on"] is not None):
                uploaded_on = d["uploaded_on"].strptime(str(d["uploaded_on"]),
                                                        '%Y-%m-%d %H:%M:%S'
                                                        ).strftime(
                                                        '%d-%b-%Y %H:%M')
            if(d["approved_on"] is not None):
                approved_on = d["approved_on"].strptime(str(d["approved_on"]),
                                                        '%Y-%m-%d %H:%M:%S'
                                                        ).strftime(
                                                        '%d-%b-%Y %H:%M')
            if(d["rejected_on"] is not None):
                rejected_on = d["rejected_on"].strptime(str(d["rejected_on"]),
                                                        '%Y-%m-%d %H:%M:%S'
                                                        ).strftime(
                                                        '%d-%b-%Y %H:%M')
            download_count = 0
            if (d["rejected_file_download_count"] is not None):
                download_count = d["rejected_file_download_count"]

            rejectdatalist.append({
                 str(d["csv_unit_id"]),
                 str(d["uploaded_by"]),
                 str(uploaded_on),
                 str(d["csv_name"]),
                 str(d["total_records"]),
                 str(d["total_rejected_records"]),
                 str(d["approved_by"]),
                 str(d["rejected_by"]),
                 str(approved_on),
                 str(rejected_on),
                 str(d["is_fully_rejected"]),
                 str(d["approve_status"]),
                 str(download_count),
                 str(d["remarks"]),
                 str(d["action"]),
                 str(d["rejected_reason"])
            })
    else:
        rejectdatalist = []

    return rejectdatalist


def get_cu_csv_file_name_by_id(db, session_user, user_id, csv_id):
    args = [csv_id]
    data = db.call_proc('sp_get_cu_csv_file_name_by_id', args)
    return data[0]["csv_name"]

########################################################
'''
    returns true if the data updates properply
    :param
        db: database object
        csv_id: parent table id
        action: approve or reject action
        remarks: remarks reason if required
        user_id: logged user
    :type
        db: Object
        csv_id: Integer
        action: Integer
        remarks: String
        user_id: Integer
    :returns
        result: return boolean
    rtype:
        result: Boolean
'''
########################################################


def update_bulk_client_unit_approve_reject_list(db, csv_unit_id, action, remarks, declined_count, session_user) :

    try :
        args = [csv_unit_id, action, remarks, session_user.user_id(), declined_count]
        data = db.call_proc("sp_bulk_client_unit_update_action", args)
        print "here"
        print data
        return True

    except Exception, e :
        logger.logKnowledge("error", "update action from list", str(traceback.format_exc()))
        logger.logKnowledge("error", "update action from list", str(e))
        raise fetch_error()

########################################################
'''
    returns sets of dataset
    :param
        db: database object
        csv_id: parent table id
        user_id: logged user
    :type
        db: Object
        csv_id: Integer
        user_id: Integer
    :returns
        result: return sets of dataset
    rtype:
        result: Object
'''
########################################################


def get_bulk_client_units_and_filtersets_by_csv_id(db, request, session_user) :

    csv_id = request.csv_id
    f_count = request.f_count
    f_range = request.r_range
    unit_list = db.call_proc("sp_bulk_client_unit_view_by_csvid", [
        csv_id, f_count, f_range
    ])

    group_name = None
    csv_name = None
    upload_by = session_user.user_full_name()
    upload_on = None
    client_unit_data = []
    if len(unit_list) > 0 :
        for idx, d in enumerate(unit_list) :
            if idx == 0 :
                group_name = d["client_group"]
                csv_name = d["csv_name"]
                upload_on = d["uploaded_on"].strftime("%d-%b-%Y %H:%M")
                upload_by = d["uploaded_by"]

            client_unit_data.append(bu_cu.BulkClientUnitList(
                int(d["bulk_unit_id"]), d["legal_entity"], d["division"],
                d["category"], d["geography_level"], d["unit_location"],
                d["unit_code"], d["unit_name"], d["address"], d["city"],
                d["state"], str(d["postalcode"]), d["domain"], d["organization"],
                d["action"], d["remarks"]
            ))

    # fetch data for filter
    filter_data = db.call_proc_with_multiresult_set("sp_bulk_client_unit_filter_data", [csv_id], 7)
    print "filtered data"
    print filter_data
    le_names = []
    div_names = []
    cg_names = []
    u_locations = []
    u_codes = []
    domain_names = []
    orga_names = []

    if len(filter_data) > 0 :
        if len(filter_data[0]) > 0 :
            for d in filter_data[0]:
                le_names.append(d["legal_entity"])

        if len(filter_data[1]) > 0 :
            for d in filter_data[1] :
                div_names.append(d["division"])

        if len(filter_data[2]) > 0 :
            for d in filter_data[2] :
                cg_names.append(d["category"])

        if len(filter_data[3]) > 0 :
            for d in filter_data[3] :
                u_locations.append(d["unit_location"])

        if len(filter_data[4]) > 0 :
            for d in filter_data[4] :
                u_codes.append(d["unit_code"])

        last = object()
        if len(filter_data[5]) > 0 :
            for d in filter_data[5] :
                if d["domain"].find('|;|') > 0 :
                    dom = d["domain"].split('|;|')
                    for domain in dom:
                        if last != domain:
                            last = domain
                            domain_names.append(domain)
                else:
                    if last != d["domain"] :
                        last = d["domain"]
                        domain_names.append(d["domain"])

        last = object()
        if len(filter_data[6]) > 0 :
            for d in filter_data[6] :
                if d["organization"].find('|;|') > 0 :
                    org = d["organization"].split('|;|')
                    for d_o in org :
                        o = d_o.split(">>")
                        if last != o[1].strip():
                            last = o[1].strip()
                            orga_names.append(o[1].strip())
                else:
                    if d["organization"].find(">>") > 0 :
                        o = d["organization"].split(">>")
                        if last != o[1].strip() :
                            last = o[1].strip()
                            orga_names.append(o[1].strip())
                    else:
                        if last != d["organization"].strip() :
                            last = d["organization"].strip()
                            orga_names.append(d["organization"].strip())

    return bu_cu.GetBulkClientUnitViewAndFilterDataSuccess(
        group_name, csv_name, upload_by, upload_on, csv_id,
        le_names, div_names, cg_names, u_locations, u_codes,
        domain_names, orga_names, client_unit_data
    )

########################################################
'''
    returns a dataset
    :param
        db: database object
        csv_id: parent table id
        user_id: logged user
    :type
        db: Object
        csv_id: Integer
        user_id: Integer
    :returns
        result: return a dataset
    rtype:
        result: Object
'''
########################################################


def get_bulk_client_unit_list_by_filter(db, request_frame, session_user) :

    csv_id = request_frame.csv_id
    legal_entity = request_frame.bu_le_name
    division = request_frame.bu_division_name
    category = request_frame.bu_category_name
    unit_location = request_frame.bu_unit_location
    unit_code = request_frame.bu_unit_code
    domain = request_frame.bu_domain
    orga_name = request_frame.bu_orgn
    f_count = request_frame.f_count
    f_range = request_frame.r_range

    if legal_entity is None or legal_entity == "" :
        legal_entity = '%'

    if division is None or division == "" :
        division = '%'

    if category is None or category == "" :
        category = '%'

    if unit_location is None or unit_location == "" :
        unit_location = '%'

    if unit_code is None or unit_code == "" :
        unit_code = '%'

    if domain is None or domain == "" :
        domain = '%'

    if orga_name is None or orga_name == "" :
        orga_name = '%'

    unit_list = db.call_proc(
        "sp_bulk_client_unit_view_by_filter",
        [
            csv_id, legal_entity, division, category, unit_location,
            unit_code, domain, orga_name, f_count, f_range
        ]
    )
    group_name = None
    csv_name = None
    upload_by = session_user.user_full_name()
    upload_on = None
    client_unit_data = []
    if len(unit_list) > 0 :
        for idx, d in enumerate(unit_list) :
            if idx == 0 :
                group_name = d["client_group"]
                csv_name = d["csv_name"]
                upload_on = d["uploaded_on"].strftime("%d-%b-%Y %H:%M")
                upload_by = d["uploaded_by"]

            client_unit_data.append(bu_cu.BulkClientUnitList(
                d["bulk_unit_id"], d["legal_entity"], d["division"],
                d["category"], d["geography_level"], d["unit_location"],
                d["unit_code"], d["unit_name"], d["address"], d["city"],
                d["state"], str(d["postalcode"]), d["domain"], d["organization"],
                d["action"], d["remarks"]
            ))

    return bu_cu.GetBulkClientUnitFilterDataSuccess(
        group_name, csv_name, upload_by, upload_on, csv_id,
        client_unit_data
    )

########################################################
'''
    returns true if the data updates properply
    :param
        db: database object
        csv_id: parent table id
        bulk_unit_id: sub table primary id
        action: approve or reject action
        remarks: remarks reason if required
        user_id: logged user
    :type
        db: Object
        csv_id: Integer
        action: Integer
        remarks: String
        user_id: Integer
    :returns
        result: return boolean
    rtype:
        result: Boolean
'''
########################################################


def save_client_unit_action_from_view(db, csv_id, bulk_unit_id, action, remarks, session_user) :

    try :
        args = [csv_id, bulk_unit_id, action, remarks]
        data = db.call_proc("sp_bulk_client_unit_id_save", args)
        print data
        return True

    except Exception, e :
        logger.logKnowledge(
            "error",
            "update action from view",
            str(traceback.format_exc())
        )
        logger.logKnowledge("error", "update action from view", str(e))
        raise fetch_error()

########################################################
'''
    returns boolean value
    :param
        db: database object
        csv_id: parent table id
        user_id: logged user
    :type
        db: Object
        csv_id: Integer
        user_id: Integer
    :returns
        result: return a boolean value
    rtype:
        result: boolean value
'''
########################################################


def get_bulk_client_unit_null_action_count(db, request_frame, session_user) :

    csv_id = request_frame.csv_id
    args = [csv_id]
    data = db.call_proc("sp_bulk_client_unit_action_count", args)
    if len(data) > 0 :
        if int(data[0].get("null_action_count")) > 0 :
            return False
        else:
            return True

########################################################
'''
    returns boolean value
    :param
        db: database object
        csv_id: parent table id
        user_id: logged user
    :type
        db: Object
        csv_id: Integer
        user_id: Integer
    :returns
        result: return a boolean value
    rtype:
        result: boolean value
'''
########################################################


def get_bulk_client_unit_file_count(db, request_frame) :

    client_id = request_frame.bu_client_id
    args = [client_id]
    data = db.call_proc("sp_bulk_client_unit_file_count", args)
    if len(data) > 0 :
        if int(data[0].get("file_count")) < 5 :
            return True
        else:
            return False
