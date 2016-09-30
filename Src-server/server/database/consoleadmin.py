from protocol import consoleadmin
from forms import *

__all__ = [
    "get_db_server_list",
    "is_duplicate_db_server_name",
    "save_db_server",
    "get_client_server_list",
    "is_duplicate_client_server_name",
    "save_client_server"
]


def get_db_server_list(db):
    data = db.call_proc(
        "sp_databaseserver_list", None
    )
    return return_database_servers(data)


def return_database_servers(data):
    fn = consoleadmin.DBServer
    result = [
        fn(
            db_server_name=datum["db_server_name"], ip=datum["ip"],
            port=datum["port"], username=datum["server_username"],
            password=datum["server_password"], no_of_clients=datum["length"]
        ) for datum in data
    ]
    return result


def is_duplicate_db_server_name(db, db_server_name, ip):
    result = db.call_proc(
        "sp_databaseserver_is_duplicate", (db_server_name, ip))
    if result[0]["count"] > 0:
        return True
    else:
        return False


def save_db_server(db, request, session_user):
    db.call_insert_proc(
        "sp_databaseserver_save", (
            request.db_server_name, request.ip, request.port,
            request.username, request.password
        )
    )
    action = "New Database server %s added" % (request.db_server_name)
    db.save_activity(session_user,  frmConfigureDBServer, action)


def get_client_server_list(db):
    data = db.call_proc(
        "sp_machines_list", None
    )
    return return_client_servers(data)


def return_client_servers(data):
    fn = consoleadmin.ClientServer
    result = []
    for datum in data:
        no_of_clients = []
        if datum["client_ids"] is not None:
            no_of_clients = datum["client_ids"].split(",")
        result.append(
            fn(
                client_server_id=datum["machine_id"],
                client_server_name=datum["machine_name"], ip=datum["ip"],
                port=datum["port"], no_of_clients=len(no_of_clients)
            )
        )
    return result


def is_duplicate_client_server_name(db, client_server_name, client_server_id):
    result = db.call_proc(
        "sp_machines_is_duplicate", (client_server_name, client_server_id))
    if result[0]["count"] > 0:
        return True
    else:
        return False


def save_client_server(db, request, session_user):
    db.call_insert_proc(
        "sp_machines_save", (
            request.client_server_id, request.client_server_name,
            request.ip, request.port
        )
    )
    action = "New Machine %s added" % (request.client_server_name)
    if request.client_server_id is not None:
        action = "Machine %s updated" % (request.client_server_name)
    db.save_activity(session_user,  frmConfigureClientServer, action)
