from protocol import consoleadmin
from forms import *

__all__ = [
    "get_db_server_list",
    "is_duplicate_db_server_name",
    "save_db_server"
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
