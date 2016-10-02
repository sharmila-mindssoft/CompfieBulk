from protocol import consoleadmin
from forms import *

__all__ = [
    "get_db_server_list",
    "is_duplicate_db_server_name",
    "save_db_server",
    "get_client_server_list",
    "is_duplicate_client_server_name",
    "save_client_server",
    "get_client_database_form_data",
    "save_allocated_db_env"
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


def get_client_database_form_data(db):
    data = db.call_proc_with_multiresult_set(
        "sp_clientdatabase_list", None, 5)
    client_dbs = data[0]
    groups = data[1]
    les = data[2]
    machines = data[3]
    db_servers = data[4]
    client_dbs_list = return_client_dbs(client_dbs)
    groups_list = return_client_groups(groups)
    les_list = return_legal_entites(les)
    machines_list = return_machines(machines)
    db_servers_list = return_db_servers(db_servers)
    return (
        client_dbs_list, groups_list, les_list,
        machines_list, db_servers_list
    )


def return_client_dbs(data):
    fn = consoleadmin.ClientDatabase
    client_dbs = [
        fn(
            client_id=datum["client_id"],
            legal_entity_id=datum["legal_entity_id"],
            machine_id=datum["machine_id"],
            database_server_ip=datum["database_ip"]
        ) for datum in data
    ]
    return client_dbs


def return_client_groups(data):
    fn = consoleadmin.ClientGroup
    client_groups = [
        fn(
            client_id=datum["client_id"],
            group_name=datum["group_name"]
        ) for datum in data
    ]
    return client_groups


def return_legal_entites(data):
    fn = consoleadmin.LegalEntity
    legal_entites = [
        fn(
            legal_entity_id=datum["legal_entity_id"],
            legal_entity_name=datum["legal_entity_name"],
            client_id=datum["client_id"]
        ) for datum in data
    ]
    return legal_entites


def return_machines(data):
    fn = consoleadmin.ClientServerNameAndID
    client_server_name_and_id = [
        fn(
            machine_id=datum["machine_id"],
            machine_name=datum["machine_name"]
        ) for datum in data
    ]
    return client_server_name_and_id


def return_db_servers(data):
    fn = consoleadmin.DBServerNameAndID
    db_servers_name_and_id = [
        fn(
            db_server_name=datum["db_server_name"], ip=datum["ip"]
        ) for datum in data
    ]
    return db_servers_name_and_id


def save_allocated_db_env(db, request):
    client_id = request.client_id
    legal_entity_id = request.legal_entity_id
    db_server_ip = request.database_server_ip
    machine_id = request.machine_id
    db.call_insert_proc(
        "sp_clientdatabase_save",
        (client_id, legal_entity_id, db_server_ip, machine_id)
    )
