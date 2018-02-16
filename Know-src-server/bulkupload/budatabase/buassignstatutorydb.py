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
    "get_download_assing_statutory_list"
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
    result = _source_db.call_proc_with_multiresult_set("sp_client_info", [9], 4)

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


def get_download_assing_statutory_list(db, cl_id, le_id, d_ids, u_ids, session_user):
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

    result = _source_db.call_proc_with_multiresult_set("sp_get_assign_statutory_compliance", [u, d], 3)

    statu = result[0]
    organisation = result[1]
    assigned_new_compliance = result[2]

    def organisation_list(map_id) :
        org_list = []
        for o in organisation :
            if o.get("statutory_mapping_id") == map_id :
                org_list.append(o["organisation_name"])
        return org_list

    def status_list(map_id):
        level_1_id = None
        map_text = None
        level_1_s_name = None
        for s in statu :
            if s["statutory_mapping_id"] == map_id :
                if s["parent_ids"] == '' or s["parent_ids"] == 0 or s["parent_ids"] == '0,':
                    level_1_id = s["statutory_id"]
                    map_text = s["statutory_name"]
                    level_1_s_name = map_text
                else :
                    names = [x.strip() for x in s["parent_names"].split('>>') if x != '']
                    ids = [int(y) for y in s["parent_ids"].split(',') if y != '']
                    level_1_id = ids[0]
                    level_1_s_name = names[0]
                    if len(names) > 1 :
                        map_text = names[1]
                    else :
                        map_text = s["statutory_name"]
                        # map_text = ''
        return level_1_id, level_1_s_name, map_text

    data_list = []
    for r in assigned_new_compliance :
        map_id = r["statutory_mapping_id"]
        orgs = organisation_list(map_id)

        org = ",".join(str(e) for e in orgs)

        level_1, level_1_name, map_text = status_list(map_id)
        if map_text == level_1_name :
            map_text = ""
        if r["assigned_compid"] is None :
            # before save rest of the field will be null before save in assignstatutorycompliance
            data_tuple = (
                "Zerodha", "Zerodha Legal Entity", "Finance Law",  org, "unit_code", 
                "unit_name", "unit_location" , level_1_name, map_text,
                r["statutory_provision"], r["compliance_task"], r["compliance_description"]
                )
            data_list.append(data_tuple)
        else :
            data_list.append()
        

    column = ["client_group", "legal_entity", "domain", "organization", "unit_code", "unit_name",
    "unit_location", "perimary_legislation", "secondary_legislation", "statutory_provision", "compliance_task_name",
    "compliance_description"]

    
    db.bulk_insert("tbl_download_assign_statutory_template", column, data_list)

    
    return data_list    