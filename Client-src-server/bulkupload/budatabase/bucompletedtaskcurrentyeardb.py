from server.exceptionmessage import fetch_error
import traceback
from server import logger
from ..buapiprotocol import bucompletedtaskcurrentyearprotocol as bu_ct
import datetime

from server.constants import (
    KNOWLEDGE_DB_HOST, KNOWLEDGE_DB_PORT, KNOWLEDGE_DB_USERNAME,
    KNOWLEDGE_DB_PASSWORD, KNOWLEDGE_DATABASE_NAME
)
from bulkupload.client_bulkconstants import(CSV_DELIMITER, CSV_MAX_LINE_ITEM)

from server.common import (
   get_date_time, string_to_datetime, datetime_to_string,
   get_date_time_in_date
)

__all__ = [
    "get_legal_entity_domains",
    "save_completed_task_current_year_csv",
    "save_completed_task_data",
    "getPastRecordData",
    "getCompletedTaskCSVList",
    "get_client_id_by_le"
]

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

def save_completed_task_current_year_csv(
    db, completed_task, session_user
):

    columns = [
        "client_id", "legal_entity_id", "domain_id","unit_id_id", "client_group",
        "csv_name", "uploaded_by", "uploaded_on",
        "total_records", "total_documents", "uploaded_documents", "upload_status"
    ]
    # print "completed_task[7]>>", completed_task[7]
    # print "string_to_datetime(completed_task[7])>>", string_to_datetime(completed_task[7])
    values = [
        completed_task[0],completed_task[1],
        completed_task[2], completed_task[3],
        completed_task[4], completed_task[5],
        completed_task[6], string_to_datetime(completed_task[7]),
        completed_task[8], completed_task[9],
        completed_task[10], completed_task[11]
    ]

    completed_task_id = db.insert("tbl_bulk_past_data_csv", columns, values)

    return completed_task_id

def save_completed_task_data(db, csv_id, csv_data, client_id):
    try:
        columns = ["csv_past_id",  "Legal_Entity", "Domain",
        "Unit_Code", "Unit_Name", "perimary_legislation",
        "Secondary_Legislation", "compliance_task_name",
        "Compliance_Description", "Compliance_Frequency", "Statutory_Date",
        "Due_Date","Assignee","Completion_Date","document_name"
        ]

        values = []
        for idx, d in enumerate(csv_data):
            values.append((
                csv_id, d["Legal_Entity"],
                d["Domain"], d["Unit_Code"], d["Unit_Name"],
                d["Primary_Legislation"], d["Secondary_Legislation"],
                d["Compliance_Task"], d["Compliance_Description"],
                d["Compliance_Frequency"], d["Statutory_Date"],
                string_to_datetime(d["Due_Date"]), d["Assignee"],
                string_to_datetime(d["Completion_Date"]), d["Document_Name"]

            ))

        if values :
            db.bulk_insert("tbl_bulk_past_data", columns, values)
            return True
        else :
            return False
    except Exception, e:
        print "e>>", str(e)
        print "Exception>>", Exception
        raise ValueError("Transaction failed")

def getPastRecordData(db, csvID):

    query = " SELECT bulk_past_data_id, csv_past_id, legal_entity, "+\
        " domain, unit_code, unit_name, perimary_legislation, " + \
        " secondary_legislation, compliance_task_name, " + \
        " compliance_description, compliance_frequency, " + \
        " statutory_date, due_date, assignee, completion_date, " + \
        " document_name" +\
        "  FROM tbl_bulk_past_data where csv_past_id = %s; "

    param = [csvID]
    rows = db.select_all(query, param)
    # print "getPastRecordData>rows>>", rows

    return rows


def getComplianceID(db, compliance_task_name):

    query = "SELECT compliance_id FROM tbl_compliances where compliance_task = '%s' limit 1"

    param = [compliance_task_name]
    complianceID = db.select_all(query, param)

    return complianceID


def getCompletedTaskCSVList(db, session_user, legal_entity_list):

    doc_names = {}

    # query = " Select legal_entity_id, csv_past_id, csv_name, uploaded_on, uploaded_by, total_records, total_documents, " + \
    #         " uploaded_documents, (total_documents - uploaded_documents) AS remaining_documents " + \
    #         " From tbl_bulk_past_data_csv where (total_documents - uploaded_documents) >= 1 " + \
    #         " and uploaded_by = %s and legal_entity_id like '%' "
    print "legal_entity_list>>", legal_entity_list
    legal_entity_list = ",".join([str(x) for x in legal_entity_list])
    print "legal_entity_list>>", legal_entity_list

    query = " SELECT DISTINCT T01.legal_entity_id, T02.legal_entity, " + \
            " T01.csv_past_id, T01.csv_name, T01.uploaded_on, T01.uploaded_by, " + \
            " total_records, total_documents, T01.uploaded_documents, " + \
            " (T01.total_documents - T01.uploaded_documents) AS remaining_documents, " + \
            " T01.domain_id, T01.unit_id_id as unit_id, NOW() as start_date" + \
            " From tbl_bulk_past_data_csv  AS T01 " + \
            " INNER JOIN tbl_bulk_past_data AS T02 " + \
            " ON T01.csv_past_id = T02.csv_past_id " + \
            " where (T01.total_documents - T01.uploaded_documents) >= 1 " + \
            " and uploaded_by = %s AND FIND_IN_SET(T01.legal_entity_id, %s)"
    param = [session_user, legal_entity_list]

    rows = db.select_all(query, param)
    print "getCompletedTaskCSVList>rows>>", rows

    param1 = [session_user]
    docQuery = "select t1.csv_past_id, document_name from tbl_bulk_past_data as t1 " + \
               " INNER JOIN tbl_bulk_past_data_csv as t2 " + \
               " ON t2.csv_past_id = t1.csv_past_id " + \
               " where ifnull(t2.upload_status, 0) = 0 and document_name != '' " + \
               " and t2.uploaded_by = %s "
    docRows = db.select_all(docQuery, param1)
    print "docRows-> ", docRows

    for d in docRows:
        csv_id = d.get("csv_past_id")
        docname = d.get("document_name")
        doc_list = doc_names.get(csv_id)
        if doc_list is None:
            doc_list = [docname]
        else:
            doc_list.append(docname)
        doc_names[csv_id] = doc_list

    print "doc Names-> ", doc_names
    csv_list = []
    for row in rows:
        uploaded_on = row["uploaded_on"].strftime("%d-%b-%Y %H:%M")
        curr_date = datetime.datetime.now().strftime('%d-%b-%Y')
        csv_list.append(
            bu_ct.CsvList(
                row["csv_past_id"], row["csv_name"],
                uploaded_on, row["uploaded_by"], row["total_records"],
                row["total_documents"], row["uploaded_documents"],
                row["remaining_documents"],
                doc_names.get(d.get("csv_past_id")), row["legal_entity"],
                row["domain_id"], row["unit_id"], curr_date
            )
        )

    # print "getCompletedTaskCSVList>csv_list>>", csv_list
    return csv_list


def connectKnowledgeDB():
    try:
        _source_db_con = mysql.connector.connect(
            user=KNOWLEDGE_DB_USERNAME,
            password=KNOWLEDGE_DB_PASSWORD,
            host=KNOWLEDGE_DB_HOST,
            database=KNOWLEDGE_DATABASE_NAME,
            port=KNOWLEDGE_DB_PORT,
            autocommit=False,
        )
        return _source_db_con
    except Exception, e:
        print "Connection Exception Caught"
        print e

def get_client_id_by_le(db, legal_entity_id): 
    # _source_db = connectKnowledgeDB()
    # query = "SELECT client_id fro tbl_legal_entities where " + \
    #         "legal_enitity id=%s" 
    # rows = _source_db.select_all(query, (legal_entity_id,))
    # client_id = rows[1]
    client_id = 1
    return client_id
