
import MySQLdb as mysql
import datetime
import pytz
import os
import json
import traceback

from server.constants import (
    KNOWLEDGE_DB_HOST, KNOWLEDGE_DB_PORT, KNOWLEDGE_DB_USERNAME,
    KNOWLEDGE_DB_PASSWORD, KNOWLEDGE_DATABASE_NAME,
    ROOT_PATH
)
client_base_path = os.path.join(ROOT_PATH, "clientdocuments")

def convert_to_dict(data_list, columns) :
    assert type(data_list) in (list, tuple)
    if len(data_list) > 0:
        if type(data_list[0]) is tuple :
            result_list = []
            if len(data_list[0]) == len(columns) :
                for data in data_list:
                    result = {}
                    for i, d in enumerate(data):
                        result[columns[i]] = d
                    result_list.append(result)
            return result_list
        else :
            result = {}
            if len(data_list) == len(columns) :
                for i, d in enumerate(data_list):
                    result[columns[i]] = d
            return result
    else:
        return []


def db_connection(host, user, password, db, port):
    connection = mysql.connect(
        host, user, password, db, port
    )
    connection.autocommit(False)
    return connection

def knowledge_db_connect():
    con = db_connection(
        KNOWLEDGE_DB_HOST, KNOWLEDGE_DB_USERNAME,
        KNOWLEDGE_DB_PASSWORD, KNOWLEDGE_DATABASE_NAME,
        KNOWLEDGE_DB_PORT
    )
    return con

def get_client_db_list():
    print "begin fetching client info"
    con = knowledge_db_connect()
    cursor = con.cursor()
    query = "SELECT T1.client_id, T1.database_ip, T1.database_port, \
        T1.database_username, T1.database_password, T1.database_name \
        FROM tbl_client_database T1"
    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()
    con.close()
    if rows :
        columns = [
            "client_id", "database_ip", "database_port", "database_username",
            "database_password", "database_name"
        ]
        result = convert_to_dict(rows, columns)
        return result
    else :
        return None


def create_client_db_connection(data):
    if data is None :
        return None

    print "begin client db connection"
    client_connection = {}
    for d in data :
        try :
            db_conn = db_connection(
                d["database_ip"], d["database_username"],
                d["database_password"], d["database_name"],
                d["database_port"]
            )
            client_connection[d["client_id"]] = db_conn
        except Exception, e :
            print "unable to connect database %s", d
            print e
            continue

    return client_connection

def get_client_database():
    client_list = get_client_db_list()
    client_db = create_client_db_connection(client_list)
    return client_db

def get_records_more_then_7year(db):
    q = "select compliance_history_id, unit_id, documents, document_size from \
    tbl_compliance_history where DATE(completion_date) < '%s'"
    pass

def delete_compliance_more_then_7year(db, cleint_id):
    pass

def run_delete_process():
    client_info = get_client_database()
    if client_info is not None :
        for client_id, db in client_info.iteritems() :
            try :
                db.commit()
            except Exception, e :
                print e
                db.rollback()
                print(traceback.format_exc())
