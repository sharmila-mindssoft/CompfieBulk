from ..buapiprotocol import buassignstatutoryprotocol as bu_as
from protocol import (core, domaintransactionprotocol)


import mysql.connector
from server.dbase import Database
from server.constants import (
    KNOWLEDGE_DB_HOST, KNOWLEDGE_DB_PORT, KNOWLEDGE_DB_USERNAME,
    KNOWLEDGE_DB_PASSWORD, KNOWLEDGE_DATABASE_NAME,
    CSV_DELIMITER, BULKUPLOAD_INVALID_PATH
)

__all__ = [
    "get_client_list",
    "get_download_assing_statutory_list",
    "save_assign_statutory_csv",
    "save_assign_statutory_data",
    "get_pending_list"
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
            print d
            values.append((
                csv_id, d["Client_Group"], d["Legal_Entity"],
                d["Domain"], d["Organisation"], d["Unit_Code"],
                d["Unit_Name"], d["Location"],
                d["Primary_Legislation"], d["Secondary_Legislaion"],
                d["Statutory_Provision"], d["Compliance_Task_Name"], d["Compliance_Description"],
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
            d["csv_assign_statutory_id"], csv_name, session_user.user_full_name(),
            d["uploaded_on"], d["total_records"], d["action_count"],
            d["csv_name"]
        ))

    return csv_data