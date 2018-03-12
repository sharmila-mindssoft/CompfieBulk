from ..buapiprotocol import buassignstatutoryprotocol as bu_as
from protocol import (core, domaintransactionprotocol)
import datetime
import mysql.connector
from server.dbase import Database
from server.constants import (
    KNOWLEDGE_DB_HOST, KNOWLEDGE_DB_PORT, KNOWLEDGE_DB_USERNAME,
    KNOWLEDGE_DB_PASSWORD, KNOWLEDGE_DATABASE_NAME,
    CSV_DELIMITER, BULKUPLOAD_INVALID_PATH
)
from server import logger

__all__ = [
    "get_client_list",
    "get_download_assing_statutory_list",
    "save_assign_statutory_csv",
    "save_assign_statutory_data",
    "get_pending_list",
    "get_assign_statutory_filters_for_approve",
    "get_assign_statutory_by_csv_id",
    "get_assign_statutory_by_filter",
    "update_approve_action_from_list",
    "fetch_rejected_assign_sm_data",
    "update_asm_download_count_by_csvid",
    "get_list_and_delete_rejected_asm",
    "fetch_assigned_statutory_bulk_report",
    "fetch_rejected_asm_download_csv_report",
    "get_asm_csv_file_name_by_id",
    "save_action_from_view"
    ]

########################################################
# Return the client info list
# :param db : database class object
# :type db  : Object
# :param session_user : user id who currently logged in
# :type session_user : String
# :returns : clients_data : list of client
# :returns : entitys_data: list of legal entities
# :returns : units_data: list of units
# rtypes: lsit of Object
########################################################
def get_client_list(db, session_user):
    _source_db_con = mysql.connector.connect(
        user=KNOWLEDGE_DB_USERNAME,
        password=KNOWLEDGE_DB_PASSWORD,
        host=KNOWLEDGE_DB_HOST,
        database=KNOWLEDGE_DATABASE_NAME,
        port=KNOWLEDGE_DB_PORT,
        autocommit=False,
    )
    _source_db = Database(_source_db_con)
    _source_db.begin()

    clients_data = []
    entitys_data = []
    units_data = []
    result = _source_db.call_proc_with_multiresult_set("sp_client_info", [session_user.user_id()], 4)
    clients = result[0]
    entitys = result[1]
    domains = result[2]
    units = result[3]

    for c in clients :

        clients_data.append(bu_as.Clients(
            c["client_id"], c["group_name"]
        ))

    for e in entitys :

        domains_data = []
        for d in domains :
            if e["legal_entity_id"] == d["legal_entity_id"]:
                domains_data.append(bu_as.Domains(
                d["domain_id"], d["domain_name"]))

        entitys_data.append(bu_as.LegalEntites(
            e["client_id"], e["legal_entity_id"], e["legal_entity_name"], domains_data)
        )


    for u in units :

        domain_ids = [int(x) for x in u["domain_ids"].split(',') if x != '']
        units_data.append(bu_as.Units(
            u["client_id"], u["legal_entity_id"], u["unit_id"], (u["unit_code"] + '-' +u["unit_name"]) , domain_ids
        ))

    return clients_data, entitys_data, units_data


########################################################
# Return the assign statutory compliance list
# :param db : database class object
# :type db  : Object
# :param session_user : user id who currently logged in
# :type session_user : String
# :returns : data_list : list of assign statutory compliance
# rtypes: lsit of Object
########################################################

def get_download_assing_statutory_list(db, cl_id, le_id, d_ids, u_ids, cl_name, le_name, d_names, u_names, session_user):
    _source_db_con = mysql.connector.connect(
        user=KNOWLEDGE_DB_USERNAME,
        password=KNOWLEDGE_DB_PASSWORD,
        host=KNOWLEDGE_DB_HOST,
        database=KNOWLEDGE_DATABASE_NAME,
        port=KNOWLEDGE_DB_PORT,
        autocommit=False,
    )
    _source_db = Database(_source_db_con)
    _source_db.begin()

    u = ",".join(str(e) for e in u_ids)
    d = ",".join(str(e) for e in d_ids)

    domain_names = ",".join(str(e) for e in d_names)
    unit_names = ",".join(str(e) for e in u_names)

    # result = _source_db.call_proc_with_multiresult_set("sp_get_assign_statutory_compliance", [u, d], 3)

    # statu = result[0]
    # organisation = result[1]
    # assigned_new_compliance = result[2]

    # def organisation_list(map_id) :
    #     org_list = []
    #     for o in organisation :
    #         if o.get("statutory_mapping_id") == map_id :
    #             org_list.append(o["organisation_name"])
    #     return org_list

    # def status_list(map_id):
    #     level_1_id = None
    #     map_text = None
    #     level_1_s_name = None
    #     for s in statu :
    #         if s["statutory_mapping_id"] == map_id :
    #             if s["parent_ids"] == '' or s["parent_ids"] == 0 or s["parent_ids"] == '0,':
    #                 level_1_id = s["statutory_id"]
    #                 map_text = s["statutory_name"]
    #                 level_1_s_name = map_text
    #             else :
    #                 names = [x.strip() for x in s["parent_names"].split('>>') if x != '']
    #                 ids = [int(y) for y in s["parent_ids"].split(',') if y != '']
    #                 level_1_id = ids[0]
    #                 level_1_s_name = names[0]
    #                 if len(names) > 1 :
    #                     map_text = names[1]
    #                 else :
    #                     map_text = s["statutory_name"]
    #                     # map_text = ''
    #     return level_1_id, level_1_s_name, map_text

    # data_list = []
    # for r in assigned_new_compliance :
    #     map_id = r["statutory_mapping_id"]
    #     orgs = organisation_list(map_id)

    #     org = ",".join(str(e) for e in orgs)

    #     level_1, level_1_name, map_text = status_list(map_id)
    #     if map_text == level_1_name :
    #         map_text = ""
    #     if r["assigned_compid"] is None :
    #         # before save rest of the field will be null before save in assignstatutorycompliance
    #         data_tuple = (
    #             cl_name, le_name, "Finance Law",  org, "unit_code", `
    #             "unit_name", "unit_location" , level_1_name, map_text,
    #             r["statutory_provision"], r["compliance_task"], r["compliance_description"]
    #             )
    #         data_list.append(data_tuple)
    #     else :
    #         data_list.append()


    column = ["client_group", "legal_entity", "domain", "organization", "unit_code", "unit_name",
    "unit_location", "perimary_legislation", "secondary_legislation", "statutory_provision", "compliance_task_name",
    "compliance_description"]

    result = _source_db.call_proc("sp_get_assign_statutory_compliance", [u, d])

    ac_list = []
    for r in result :
        ac_tuple = (
            cl_name, le_name, r["domain_name"], r["organizations"], r["unit_code"],
            r["unit_name"], r["location"] , r["primary_legislation"], r["secondary_legislation"],
            r["statutory_provision"], r["compliance_task_name"], r["compliance_description"]
            )
        ac_list.append(ac_tuple)

    db.call_proc("sp_delete_assign_statutory_template", (domain_names, unit_names))

    db.bulk_insert("tbl_download_assign_statutory_template", column, ac_list)
    return ac_list



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

def save_assign_statutory_csv(db, args):
    newid = db.call_insert_proc("sp_assign_statutory_csv_save", args)
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

def save_assign_statutory_data(db, csv_id, csv_data) :
    try:
        columns = ["csv_assign_statutory_id", "client_group", "legal_entity", "domain", "organization", "unit_code", "unit_name",
            "unit_location", "perimary_legislation", "secondary_legislation", "statutory_provision", "compliance_task_name",
            "compliance_description", "statutory_applicable_status", "statytory_remarks", "compliance_applicable_status"
        ]

        values = []

        for idx, d in enumerate(csv_data) :
            values.append((
                csv_id, d["Client_Group"], d["Legal_Entity"],
                d["Domain"], d["Organisation"], d["Unit_Code"],
                d["Unit_Name_"], d["Unit_Location"],
                d["Primary_Legislation_"], d["Secondary_Legislaion"],
                d["Statutory_Provision_"], d["Compliance_Task_"], d["Compliance_Description_"],
                d["Statutory_Applicable_Status"], d["Statutory_remarks"], d["Compliance_Applicable_Status"]
            ))

        if values :
            db.bulk_insert("tbl_bulk_assign_statutory", columns, values)
            return True
        else :
            return False
    except Exception, e:
        print str(e)
        raise ValueError("Transaction failed")


########################################################
'''
    returns assign statutory csv list which waiting for approval
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

def get_pending_list(db, cl_id, le_id, session_user):
    csv_data = []
    data = db.call_proc("sp_pending_assign_statutory_csv_list", [cl_id, le_id])

    for d in data :
        file_name = d["csv_name"].split('.')
        remove_code = file_name[0].split('_')
        csv_name = "%s.%s" % ('_'.join(remove_code[:-1]), file_name[1])
        csv_data.append(bu_as.PendingCsvListAssignStatutory(
            d["csv_assign_statutory_id"], csv_name, d["uploaded_by"],
            d["uploaded_on"], d["total_records"], d["approved_count"],
            d["rejected_count"], d["csv_name"]
        ))

    return csv_data

def get_assign_statutory_filters_for_approve(db, csv_id):
    data = db.call_proc_with_multiresult_set("sp_assign_statutory_filter_list", [csv_id], 7)
    d_names = []
    u_names = []
    p_legis = []
    s_legis = []
    s_provs = []
    c_tasks = []
    c_descs = []

    if len(data) > 0 :
        if len(data[0]) > 0:
            for d in data[0]:
                d_names.append(d["domain"])

        if len(data[1]) > 0:
            for d in data[1]:
                u_names.append(d["unit_name"])

        if len(data[2]) > 0:
            for d in data[2]:
                p_legis.append(d["perimary_legislation"])

        if len(data[3]) > 0:
            for d in data[3]:
                s_legis.append(d["secondary_legislation"])

        if len(data[4]) > 0:
            for d in data[4]:
                s_provs.append(d["statutory_provision"])

        if len(data[5]) > 0:
            for d in data[5]:
                c_tasks.append(d["compliance_task_name"])

        if len(data[6]) > 0:
            for d in data[6]:
                c_descs.append(d["compliance_description"])


    return bu_as.GetAssignStatutoryFiltersSuccess(
        d_names, u_names, p_legis, s_legis, s_provs,
        c_tasks, c_descs
    )

def get_assign_statutory_by_csv_id(db, request_frame, session_user):
    csv_id = request_frame.csv_id
    f_count = request_frame.f_count
    r_range = request_frame.r_range
    data = db.call_proc("sp_assign_statutory_view_by_csvid", [
        csv_id, f_count, r_range
    ])
    client_name = None
    legal_entity_name = None
    csv_name = None
    upload_by = None
    upload_on = None
    as_data = []
    if len(data) > 0 :
        for idx, d in enumerate(data) :
            if idx == 0 :
                client_name = "Client Name"
                legal_entity_name = d["legal_entity"]
                csv_name = d["csv_name"]
                upload_on = d["uploaded_on"]
                upload_by = d["uploaded_by"]
            as_data.append(bu_as.AssignStatutoryData(
                d["bulk_assign_statutory_id"],
                d["unit_location"], d["unit_code"],
                d["unit_name"], d["domain"],
                d["organization"], d["perimary_legislation"],
                d["secondary_legislation"], d["statutory_provision"],
                d["compliance_task_name"], d["compliance_description"],
                d["statutory_applicable_status"], d["statytory_remarks"],
                d["compliance_applicable_status"], d["action"], d["remarks"]
            ))
    return bu_as.ViewAssignStatutoryDataSuccess(
        csv_id, csv_name, client_name, legal_entity_name, upload_by,
        upload_on,  as_data
    )


def get_assign_statutory_by_filter(db, request_frame, session_user):
    csv_id = request_frame.csv_id
    domain_name = request_frame.filter_d_name
    unit_name = request_frame.filter_u_name
    p_legis = request_frame.filter_p_leg
    s_legis = request_frame.s_leg
    s_prov = request_frame.s_prov
    c_task = request_frame.c_task
    c_desc = request_frame.c_desc
    f_count = request_frame.f_count
    r_range = request_frame.r_range
    view_data = request_frame.filter_view_data
    s_status = request_frame.s_status
    c_status = request_frame.c_status


    data = db.call_proc(
        "sp_assign_statutory_view_by_filter",
        [
            csv_id, domain_name, unit_name, p_legis,
            s_legis, s_prov, c_task, c_desc, f_count, r_range,
            view_data, s_status, c_status
        ]
    )
    client_name = None
    legal_entity_name = None
    csv_name = None
    upload_by = None
    upload_on = None
    as_data = []

    if len(data) > 0 :
        for idx, d in enumerate(data) :
            if idx == 0 :
                client_name = "Client Name"
                legal_entity_name = d["legal_entity"]
                csv_name = d["csv_name"]
                upload_on = d["uploaded_on"]
                upload_by = d["uploaded_by"]
            as_data.append(bu_as.AssignStatutoryData(
                d["bulk_assign_statutory_id"],
                d["unit_location"], d["unit_code"],
                d["unit_name"], d["domain"],
                d["organization"], d["perimary_legislation"],
                d["secondary_legislation"], d["statutory_provision"],
                d["compliance_task_name"], d["compliance_description"],
                d["statutory_applicable_status"], d["statytory_remarks"],
                d["compliance_applicable_status"], d["action"], d["remarks"]
            ))
    return bu_as.ViewAssignStatutoryDataSuccess(
        csv_id, csv_name, client_name, legal_entity_name, upload_by,
        upload_on,  as_data, len(data)
    )


def update_approve_action_from_list(db, csv_id, action, remarks, session_user):
    try :
        args = [csv_id, action, remarks, session_user.user_id()]
        data = db.call_proc("sp_assign_statutory_update_action", args)
        print data
        return True

    except Exception, e:
        logger.logKnowledge("error", "update action from list", str(traceback.format_exc()))
        logger.logKnowledge("error", "update action from list", str(e))
        raise fetch_error()

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

def fetch_rejected_assign_sm_data(db, session_user,
    user_id, client_id, le_id, domain_ids, unit_id):

    rejectdatalist=[]
    domain_id_list=convertArrayToString(domain_ids)

    args = [client_id, le_id, domain_id_list, unit_id, user_id]
    data = db.call_proc('sp_rejected_assign_sm_reportdata', args)

    for d in data:
        uploaded_on = datetime.datetime.strptime(str(d["uploaded_on"]),
            '%Y-%m-%d %H:%M:%S').strftime('%d-%b-%Y %H:%M');

        approved_on = datetime.datetime.strptime(str(d["approved_on"]),
            '%Y-%m-%d %H:%M:%S').strftime('%d-%b-%Y %H:%M');

        rejected_on = datetime.datetime.strptime(str(d["rejected_on"]),
            '%Y-%m-%d %H:%M:%S').strftime('%d-%b-%Y %H:%M');

        if (d["rejected_file_download_count"] is None):
            download_count=0
        else:
            download_count=d["rejected_file_download_count"]

        rejectdatalist.append(bu_as.AssignStatutoryMappingRejectData(
             int(d["csv_assign_statutory_id"]),
             int(d["uploaded_by"]),
             str(uploaded_on),
             str(d["csv_name"]),
             int(d["total_records"]),
             int(d["total_rejected_records"]),
             int(d["approved_by"]),
             int(d["rejected_by"]),
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

def update_asm_download_count_by_csvid(db, session_user, csv_id):
    asm_updated_count=[];
    args = [csv_id]
    data = db.call_proc('sp_update_asm_download_count', args)
    for d in data:
        asm_updated_count.append(bu_as.ASMRejectUpdateDownloadCount(
             int(d["csv_assign_statutory_id"]), int(d["rejected_file_download_count"])
        ))
    return asm_updated_count

def get_list_and_delete_rejected_asm(db, session_user, user_id,
        client_id, le_id, domain_ids, unit_code, csv_id):

    args = [csv_id]
    data = db.call_proc('sp_delete_reject_asm_by_csvid', args)

    rejectdatalist=fetch_rejected_assign_sm_data(db, session_user,
    user_id, client_id, le_id, domain_ids, unit_code)

    return rejectdatalist

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
    clientGroupId, legalEntityId, unitId, domainIds, from_date, to_date,
    record_count, page_count, child_ids, user_category_id):
    reportdatalist=[]
    expected_result=2
    domain_ids=''

    if(domainIds is not None):
        domain_ids=convertArrayToString(domainIds)

    if(len(child_ids)>0):
        if(user_category_id==7):
            user_ids=convertArrayToString(child_ids)
        elif(user_category_id==8 and user_category_id!=7):
            user_ids=convertArrayToString(child_ids)
        else:
            user_ids=user_id

    args = [clientGroupId, legalEntityId, unitId, from_date, to_date, record_count, page_count, str(user_ids), domain_ids]
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

        reportdatalist.append(bu_as.StatutoryReportData(
             int(d["uploaded_by"]),
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

def fetch_rejected_asm_download_csv_report(db, session_user, user_id,
    client_id, le_id, domain_ids, asm_unit_code, csv_id):

    rejectdatalist=[]
    domainIds=''
    if(domain_ids is not None):
        domainIds=convertArrayToString(domain_ids)

    args = [client_id, le_id, domainIds, asm_unit_code, csv_id, user_id]
    data = db.call_proc('sp_rejected_asm_csv_report', args)
    approved_on='0000-00-00'
    uploaded_on=''
    rejected_on=''

    for d in data:
        if(d["uploaded_on"] is not None):
            uploaded_on = datetime.datetime.strptime(str(d["uploaded_on"]),
            '%Y-%m-%d %H:%M:%S').strftime('%d-%b-%Y %H:%M');

        if(d["approved_on"] is not None):
            approved_on = datetime.datetime.strptime(str(d["approved_on"]),
        '%Y-%m-%d %H:%M:%S').strftime('%d-%b-%Y %H:%M');

        if(d["rejected_on"] is not None):
            rejected_on = datetime.datetime.strptime(str(d["rejected_on"]),
            '%Y-%m-%d %H:%M:%S').strftime('%d-%b-%Y %H:%M');

        if (d["rejected_file_download_count"] is None):
            download_count=0
        else:
            download_count=d["rejected_file_download_count"]

        rejectdatalist.append({
             int(d["csv_assign_statutory_id"]),
             int(d["uploaded_by"]),
             str(uploaded_on),
             str(d["csv_name"]),
             str(d["total_records"]),
             str(d["total_rejected_records"]),
             int(d["approved_by"]),
             int(d["rejected_by"]),
             str(approved_on),
             str(d["rejected_on"]),
             str(d["is_fully_rejected"]),
             str(d["approve_status"]),
             str(download_count),
             str(d["remarks"]),
             str(d["action"]),
             str(d["rejected_reason"])
        })
    return data

def get_asm_csv_file_name_by_id(db, session_user, user_id, csv_id):
    args = [csv_id]
    data = db.call_proc('sp_get_asm_csv_file_name_by_id', args)
    print data[0]["csv_name"]
    return data[0]["csv_name"]

def save_action_from_view(db, csv_id, as_id, action, remarks, session_user):
    try :
        args = [csv_id, as_id, action, remarks]
        data = db.call_proc("sp_approve_assign_statutory_action_save", args)
        return True

    except Exception, e:
        logger.logKnowledge("error", "update action from view", str(traceback.format_exc()))
        logger.logKnowledge("error", "update action from view", str(e))
        raise fetch_error()