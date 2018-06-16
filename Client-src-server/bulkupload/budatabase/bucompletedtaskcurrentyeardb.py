import mysql
import requests
from ..buapiprotocol import bucompletedtaskcurrentyearprotocol as bu_ct
import datetime
from server.dbase import Database
from server.constants import (
    KNOWLEDGE_DB_HOST, KNOWLEDGE_DB_PORT, KNOWLEDGE_DB_USERNAME,
    KNOWLEDGE_DB_PASSWORD, KNOWLEDGE_DATABASE_NAME,
)
from server.common import (
    string_to_datetime, string_to_datetime_with_time
)
from clientprotocol import clientcore
from bulkupload.client_bulkconstants import (TEMP_FILE_SERVER)


__all__ = [
    "get_legal_entity_domains",
    "save_completed_task_current_year_csv",
    "save_completed_task_data",
    "get_past_record_data",
    "get_completed_task_csv_list",
    "get_client_id_by_le",
    "get_units_for_user",
    "get_files_as_zip",
    "update_document_count"
]


def get_legal_entity_domains(
    db, le_id
):
    query = "SELECT T02. domain_name, T01.le_domain_id, " + \
            "T01.legal_entity_id, " + \
            "T01.domain_id, T02.domain_id " + \
            " FROM tbl_legal_entity_domains AS T01 " + \
            "INNER JOIN tbl_domains AS T02 " + \
            " ON T01.domain_id = T02.domain_id " + \
            "WHERE is_active ='0' AND T01.legal_entity_id = %s " + \
            "Group by T01.domain_id;"

    param = [le_id]
    rows = db.select_all(query, param)
    results = []
    for domains in rows:
        domain_obj = bu_ct.Domains(
            domains["legal_entity_id"], domains["le_domain_id"],
            domains["domain_name"])
        results.append(domain_obj)

    return results


def save_completed_task_current_year_csv(
    db, completed_task
):

    columns = [
        "client_id", "legal_entity_id", "domain_id", "unit_id_id",
        "client_group", "csv_name", "uploaded_by", "uploaded_on",
        "total_records", "total_documents", "uploaded_documents",
        "upload_status"
    ]
    values = [
        completed_task[0], completed_task[1],
        completed_task[2], completed_task[3],
        completed_task[4], completed_task[5],
        completed_task[6], string_to_datetime_with_time(completed_task[7]),
        completed_task[8], completed_task[9],
        completed_task[10], completed_task[11]
    ]

    completed_task_id = db.insert("tbl_bulk_past_data_csv", columns, values)

    return completed_task_id


def save_completed_task_data(db, csv_id, csv_data):
    try:
        columns = [
            "csv_past_id", "Legal_Entity", "Domain",
            "Unit_Code", "Unit_Name", "perimary_legislation",
            "Secondary_Legislation", "compliance_task_name",
            "Compliance_Description", "Compliance_Frequency", "Statutory_Date",
            "Due_Date", "Assignee", "Completion_Date", "document_name"
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

        if values:
            db.bulk_insert("tbl_bulk_past_data", columns, values)
            return True
        else:
            return False
    except Exception:
        raise ValueError("Transaction failed")


def get_past_record_data(db, csv_id):
    query = " SELECT bulk_past_data_id, csv_past_id, " + \
        " legal_entity, " + \
        " domain, unit_code, unit_name, perimary_legislation, " + \
        " secondary_legislation, compliance_task_name, " + \
        " compliance_description, compliance_frequency, " + \
        " statutory_date, due_date, assignee, completion_date, " + \
        " document_name" + \
        " FROM tbl_bulk_past_data where csv_past_id = %s; "
    param = [csv_id]
    rows = db.select_all(query, param)
    return rows


def get_compliance_id(db, compliance_task_name):
    query = "SELECT compliance_id FROM tbl_compliances " + \
        "where compliance_task = '%s' limit 1"

    param = [compliance_task_name]
    compliance_id = db.select_all(query, param)

    return compliance_id


def get_completed_task_csv_list(db, session_user, legal_entity_list):

    doc_names = {}
    legal_entity_list = ",".join([str(x) for x in legal_entity_list])

    query = " SELECT DISTINCT T01.legal_entity_id, " + \
            " T02.legal_entity, " + \
            " T01.csv_past_id, T01.csv_name, T01.uploaded_on, " + \
            " T01.uploaded_by, " + \
            " total_records, total_documents, T01.uploaded_documents, " + \
            " (T01.total_documents - T01.uploaded_documents) " + \
            " AS remaining_documents, " + \
            " T01.domain_id, T01.unit_id_id as unit_id, " + \
            " NOW() as start_date" + \
            " From tbl_bulk_past_data_csv  AS T01 " + \
            " INNER JOIN tbl_bulk_past_data AS T02 " + \
            " ON T01.csv_past_id = T02.csv_past_id " + \
            " where (T01.total_documents - T01.uploaded_documents) >= 1 " + \
            " and uploaded_by = %s AND FIND_IN_SET " + \
            " (T01.legal_entity_id, %s)  order by T01.uploaded_on DESC"
    param = [session_user, legal_entity_list]

    rows = db.select_all(query, param)

    param1 = [session_user]
    doc_query = "select t1.csv_past_id, document_name " + \
                   " from tbl_bulk_past_data as t1 " + \
                   " INNER JOIN tbl_bulk_past_data_csv as t2 " + \
                   " ON t2.csv_past_id = t1.csv_past_id " + \
                   " where ifnull(t2.upload_status, 0) = 0 " + \
                   " and document_name != '' " + \
                   " and t2.uploaded_by = %s "
    doc_rows = db.select_all(doc_query, param1)
    if doc_rows is not None:
        for d in doc_rows:
            csv_id = d.get("csv_past_id")
            docname = d.get("document_name")
            doc_list = doc_names.get(csv_id)
            if doc_list is None:
                doc_list = [docname]
            else:
                doc_list.append(docname)
            doc_names[csv_id] = doc_list

    csv_list = []
    if rows is not None:
        for row in rows:
            uploaded_on = row["uploaded_on"].strftime("%d-%b-%Y %H:%M")
            curr_date = datetime.datetime.now().strftime("%d-%b-%Y")
            csv_list.append(
                bu_ct.CsvList(
                    row["csv_past_id"], row["csv_name"],
                    uploaded_on, row["uploaded_by"], row["total_records"],
                    row["total_documents"], row["uploaded_documents"],
                    row["remaining_documents"],
                    doc_names.get(row["csv_past_id"]), row["legal_entity"],
                    row["domain_id"], row["unit_id"], curr_date
                )
            )
    return csv_list


def connect_le_db(le_id):
    try:
        _knowledge_db_con = mysql.connector.connect(
            user=KNOWLEDGE_DB_USERNAME,
            password=KNOWLEDGE_DB_PASSWORD,
            host=KNOWLEDGE_DB_HOST,
            database=KNOWLEDGE_DATABASE_NAME,
            port=KNOWLEDGE_DB_PORT,
            autocommit=False
        )
        _knowledge_db = Database(_knowledge_db_con)
        _knowledge_db.begin()
        _source_db_con = None
        query = "select t1.client_database_id, t1.database_name, " + \
            "t1.database_username, t1.database_password, " + \
            "t3.database_ip, database_port " + \
            " from tbl_client_database_info as t1 " + \
            " inner join tbl_client_database as t2 on " + \
            " t2.client_database_id = t1.client_database_id " + \
            " inner join tbl_database_server as t3 on " + \
            " t3.database_server_id = t2.database_server_id " + \
            " where t1.db_owner_id = %s and t1.is_group = 0;"
        param = [le_id]

        result = _knowledge_db.select_all(query, param)
        if len(result) > 0:
            for row in result:
                dhost = row["database_ip"]
                uname = row["database_username"]
                pwd = row["database_password"]
                port = row["database_port"]
                db_name = row["database_name"]

                _source_db_con = mysql.connector.connect(
                    user=uname,
                    password=pwd,
                    host=dhost,
                    database=db_name,
                    port=port,
                    autocommit=False,
                )
        _source_db = Database(_source_db_con)
        _source_db.begin()
        return _source_db
    except Exception, e:
        print "Connection Exception Caught"
        print e


def get_client_id_by_le(legal_entity_id):
    db = connect_le_db(legal_entity_id)
    query = "SELECT client_id, group_name from tbl_client_groups "
    rows = db.select_all(query)
    client_id = rows[0]["client_id"]
    client_name = rows[0]["group_name"]
    return client_id, client_name


def get_user_category(db, user_id):
    q = "select user_category_id from tbl_users where user_id = %s"
    row = db.select_one(q, [user_id])
    if row:
        return row["user_category_id"]
    else:
        return None


def get_units_for_user(le_id, domain_id, user_id):
    db = connect_le_db(le_id)
    user_category_id = get_user_category(db, user_id)
    if user_category_id > 3:
        query = "SELECT t2.unit_id, t2.legal_entity_id, " + \
                " t2.division_id, " + \
                "t2.category_id, t2.unit_code, t2.unit_name, " + \
                " t2.is_closed, " + \
                "t2.address, " + \
                " GROUP_CONCAT(t3.domain_id) as domain_ids, " + \
                " t2.country_id, t2.business_group_id " + \
                "FROM tbl_user_units AS t1 " + \
                "INNER JOIN tbl_units AS t2 " + \
                " ON t2.unit_id = t1.unit_id  " + \
                "INNER JOIN tbl_units_organizations AS t3 " + \
                " ON t3.unit_id = t2.unit_id " + \
                "WHERE t1.user_id = %s and t2.legal_entity_id = %s " + \
                " and %s in (t3.domain_id) AND t2.is_closed = 0 " + \
                " group by t2.unit_id ORDER BY t2.unit_name"
        rows = db.select_all(query, [user_id, le_id, domain_id])
    else:
        query = "SELECT t2.unit_id, t2.legal_entity_id, " + \
                " t2.division_id, " + \
                "t2.category_id, t2.unit_code, t2.unit_name," + \
                " t2.is_closed, " + \
                "t2.address, GROUP_CONCAT(t3.domain_id) " + \
                " as domain_ids, t2.country_id, " + \
                " t2.business_group_id " + \
                "FROM tbl_user_units AS t1 " + \
                "INNER JOIN tbl_units AS t2 ON " + \
                " t2.unit_id = t1.unit_id  " + \
                "INNER JOIN tbl_units_organizations AS t3 ON " + \
                " t3.unit_id = t2.unit_id " + \
                "WHERE t2.is_closed = 0 and t2.legal_entity_id = %s " + \
                " and %s in (t3.domain_id) group by t2.unit_id " + \
                " ORDER BY t2.unit_name"
        rows = db.select_all(query, [le_id, domain_id])
    return return_units(rows)


def return_units(units):
        results = []
        for unit in units:
            division_id = None
            category_id = None
            b_group_id = None
            if unit["division_id"] > 0:
                division_id = unit["division_id"]
            if unit["category_id"] > 0:
                category_id = unit["category_id"]
            if unit["business_group_id"] > 0:
                b_group_id = unit["business_group_id"]
            results.append(clientcore.ClientUnit(
                unit["unit_id"], division_id, category_id,
                unit["legal_entity_id"],
                b_group_id, unit["unit_code"],
                unit["unit_name"], unit["address"],
                [int(x) for x in unit["domain_ids"].split(",")],
                unit["country_id"],
                bool(unit["is_closed"])
            ))
        return results


def get_files_as_zip(csv_id):
    caller_name = (
        "%sdownloadzip?csv_id=%s"
    ) % (
        TEMP_FILE_SERVER, csv_id
    )
    response = requests.post(caller_name)
    download_link = response.text
    return download_link


def update_document_count(db, csv_id, count):
    q = " update tbl_bulk_past_data_csv set " + \
        " uploaded_documents = uploaded_documents + %s " + \
        " where csv_past_id = %s"
    param = [count, csv_id]
    rows = db.execute(q, param)
    return rows
