from server.exceptionmessage import fetch_error
import traceback
from server import logger
from ..buapiprotocol import bucompletedtaskcurrentyearprotocol as bu_ct

import datetime

__all__ = [
    # "get_uploaded_statutory_mapping_csv_list"
    "get_legal_entity_domains",
    "save_completed_task_current_year_csv",
    "save_completed_task_data"
]
# transaction method begin
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
def get_legal_entity_domains(
    db, user_id, session_user, le_id
):
    query = "SELECT T02. domain_name, T01.le_domain_id, T01.legal_entity_id, " + \
            "T01.domain_id, T02.domain_id FROM tbl_legal_entity_domains AS T01 " + \
            "INNER JOIN tbl_domains AS T02 ON T01.domain_id = T02.domain_id " + \
            "WHERE is_active ='0' AND T01.legal_entity_id = %s " + \
            "Group by T01.domain_id;"

    param = [le_id]
    rows = db.select_all(query, param)
    results = []
    for domains in rows:
        domainObj =bu_ct.Domains(
            domains["legal_entity_id"], domains["le_domain_id"],
            domains["domain_name"] )
        results.append(domainObj)

    return results

# def save_completed_task_csv(db, args):
#     newid = db.call_insert_proc("sp_assign_statutory_csv_save", args)
#     return newid

def save_completed_task_current_year_csv(db, completed_task, session_user):
    columns = [
        "csv_past_id", "client_id", "legal_entity_id", "domain_id",
        "unit_id_id", "client_group", "csv_name",
        "uploaded_by", "uploaded_on",
        "total_records", "total_documents", "uploaded_documents", "upload_status"
    ]
    values = [
        completed_task.csv_past_id, completed_task.client_id, completed_task.legal_entity_id,
        completed_task.domain_id, completed_task.unit_id_id,
        completed_task.client_group, completed_task.csv_name,
        completed_task.uploaded_by, completed_task.uploaded_on,
        completed_task.total_records, completed_task.total_documents,
        completed_task.uploaded_documents, completed_task.upload_status
    ]

    completed_task_id = db.insert("tbl_bulk_past_data_csv", columns, values)

    return completed_task_id

def save_completed_task_data(db, csv_id, csv_data) :
    try:
        columns = ["csv_past_id", "client_group", "legal_entity", "domain",
        "unit_code", "unit_name", "perimary_legislation",
        "secondary_legislation", "statutory_provision", "compliance_task_name",
        "compliance_description", "compliance_frequency", "statutory_date",
        "due_date","assignee","completion_date","document_name"
        ]

        values = []
        for idx, d in enumerate(csv_data) :
            values.append((
                csv_id, d["Client_Group"], d["legal_entity"],
                d["domain"], d["unit_code"], d["unit_name"],
                d["Primary_Legislation_"], d["Secondary_Legislaion"],
                d["compliance_task_name"], d["Compliance_Description_"],
                d["compliance_frequency"], d["statutory_date"],
                d["due_date"], d["assignee"],
                d["completion_date"], d["document_name"]
            ))

        if values :
            db.bulk_insert("tbl_bulk_past_data", columns, values)
            return True
        else :
            return False
    except Exception, e:
        print str(e)
        raise ValueError("Transaction failed")

def get_uploaded_statutory_mapping_csv_list(db, session_user):
    csv_data = []
    data = db.call_proc("sp_statutory_mapping_csv_list", [session_user])
    if len(data) > 5 :
        upload_more = False
    else :
        upload_more = True
    for d in data :
        upload_on = d["uploaded_on"].strftime("%d-%b-%Y %H:%M")

        csv_data.append(bu_sm.CsvList(
            d.get("country_id"), d.get("country_name"), d.get("domain_id"), d.get("domain_name"),
            d.get("csv_id"), d.get("csv_name"), d.get("total_records"), d.get("total_documents"),
            d.get("uploaded_documents"), upload_on
        ))

    return upload_more, csv_data
########################################################
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