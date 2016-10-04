from server.exceptionmessage import process_error
from protocol import consoleadmin
from forms import *
from tables import *

__all__ = [
    "get_db_server_list",
    "is_duplicate_db_server_name",
    "save_db_server",
    "get_client_server_list",
    "is_duplicate_client_server_name",
    "save_client_server",
    "get_client_database_form_data",
    "save_allocated_db_env",
    "get_file_storage_form_data",
    "save_file_storage",
    "get_auto_deletion_form_data",
    "save_auto_deletion_details"
]


###############################################################################
# To get list of database servers
# parameter : Object of database
# return type : Returns List of object of DBServer
###############################################################################
def get_db_server_list(db):
    #
    #  To get list of all database servers
    #  Parameters : None
    #  Return : Returns all database servers
    #
    data = db.call_proc(
        "sp_databaseserver_list", None
    )
    return return_database_servers(data)


###############################################################################
# To convert data fetched from database into a list of Object of DBServer
# parameter : Data fetched from database (Tuple of tuples)
# return type : Returns List of object of DBServer
###############################################################################
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


###############################################################################
# To check whether the db server name already exists or not
# parameter : Object of database, db server name, ip
# return type : Returns True if db server name already exists otherwise returns
#               False
###############################################################################
def is_duplicate_db_server_name(db, db_server_name, ip):
    #
    #  To check whether db server name already exists or not
    #  Parameters : Db server name, ip
    #  Return : returns count of db servers exists with the save name
    #
    result = db.call_proc(
        "sp_databaseserver_is_duplicate", (db_server_name, ip))
    if result[0]["count"] > 0:
        return True
    else:
        return False


###############################################################################
# To save db server
# parameter : Object of database, Save DB server request, session user
# return type : Returns True if db server name already exists otherwise returns
#               False
###############################################################################
def save_db_server(db, request, session_user):
    #
    #  To save database server
    #  Parameters : Db server name, ip, port, username, password
    #  Return : returns last inserted row id
    #
    db_server_id = db.call_insert_proc(
        "sp_databaseserver_save", (
            request.db_server_name, request.ip, request.port,
            request.username, request.password
        )
    )
    if db_server_id:
        action = "New Database server %s added" % (request.db_server_name)
        db.save_activity(session_user,  frmConfigureDBServer, action)
    else:
        raise process_error("E074")


###############################################################################
# To Get list of client servers
# parameter : Object of database
# return type : Returns list of object of ClientServer
###############################################################################
def get_client_server_list(db):
    #
    #  To get list of client servers
    #  Parameters : None
    #  Return : Returns all client servers
    #
    data = db.call_proc(
        "sp_machines_list", None
    )
    return return_client_servers(data)


###############################################################################
# To convert data fetched from database into list of Object of Client Server
# parameter : Data fetched from database (Tuple of tuples)
# return type : Returns list of object of ClientServer
###############################################################################
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


###############################################################################
# To check whether the client server name already exists or not
# parameter : Object of database, client server name, client server id
# return type : Returns True if a duplicate cilent server name already exists
#               Otherwise returns False
###############################################################################
def is_duplicate_client_server_name(db, client_server_name, client_server_id):
    #
    #  To check whether the client server name already exists or not
    #  Parameters : Client server name, client server id
    #  Return : Returns count of client server with the same name
    #
    result = db.call_proc(
        "sp_machines_is_duplicate", (client_server_name, client_server_id))
    if result[0]["count"] > 0:
        return True
    else:
        return False


###############################################################################
# To Save Client server
# parameter : Object of database, Save Client server request, session user
# return type : Raises process error if saving client server fails otherwise
#                returns None
###############################################################################
def save_client_server(db, request, session_user):
    #
    #  To save client server
    #  Parameters : Client server id, Client server name, ip, port
    #  Return : returns last inserted id
    #
    machine_id = db.call_insert_proc(
        "sp_machines_save", (
            request.client_server_id, request.client_server_name,
            request.ip, request.port
        )
    )
    if machine_id:
        action = "New Machine %s added" % (request.client_server_name)
        if request.client_server_id is not None:
            action = "Machine %s updated" % (request.client_server_name)
        db.save_activity(session_user,  frmConfigureClientServer, action)
    else:
        raise process_error("E075")


###############################################################################
# To Get data required for allocating database environment
# parameter : Object of database
# return type : Returns tuple of Lists. List contains client databases,
#               Client groups, Legal entities, Client Servers, DB Servers
###############################################################################
def get_client_database_form_data(db):
    #
    #  To get data required for allocating database environment
    #  Parameters : None
    #  Return : returns list of Client db environments, Client groups,
    #   Legal entities, Client servers and Database servers
    #
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


###############################################################################
# Convert data fetched from database into List of object of ClientDatabase
# parameter : Data fetched from database (Tuple of tuples)
# return type : Returns List of object of ClientDatabase
###############################################################################
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


###############################################################################
# Convert data fetched from database into List of object of ClientGroup
# parameter : Data fetched from database (Tuple of tuples)
# return type : Returns List of object of ClientGroup
###############################################################################
def return_client_groups(data):
    fn = consoleadmin.ClientGroup
    client_groups = [
        fn(
            client_id=datum["client_id"],
            group_name=datum["group_name"]
        ) for datum in data
    ]
    return client_groups


###############################################################################
# Convert data fetched from database into List of object of LegalEntity
# parameter : Data fetched from database (Tuple of tuples)
# return type : Returns List of object of LegalEntity
###############################################################################
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


###############################################################################
# Convert data fetched from database into List of object of Machines
# parameter : Data fetched from database (Tuple of tuples)
# return type : Returns List of object of ClientServerNameAndID
###############################################################################
def return_machines(data):
    fn = consoleadmin.ClientServerNameAndID
    client_server_name_and_id = [
        fn(
            machine_id=datum["machine_id"],
            machine_name=datum["machine_name"]
        ) for datum in data
    ]
    return client_server_name_and_id


###############################################################################
# Convert data fetched from database into List of object of DBServerNameAndID
# parameter : Data fetched from database (Tuple of tuples)
# return type : Returns List of object of DBServerNameAndID
###############################################################################
def return_db_servers(data):
    fn = consoleadmin.DBServerNameAndID
    db_servers_name_and_id = [
        fn(
            db_server_name=datum["db_server_name"], ip=datum["ip"]
        ) for datum in data
    ]
    return db_servers_name_and_id


###############################################################################
# To Save allocated databse environment
# parameter : Object of database, Save Allocated database environment request
# return type : Raises process error if save fails otherwise returns None
###############################################################################
def save_allocated_db_env(db, request):
    client_id = request.client_id
    legal_entity_id = request.legal_entity_id
    db_server_ip = request.database_server_ip
    machine_id = request.machine_id
    #
    #  To save allocated database environment
    #  Parameters : client id, legal entity id, database ip, client server id
    #  Return : List of allocated database environment details
    #
    result = db.call_insert_proc(
        "sp_clientdatabase_save",
        (client_id, legal_entity_id, db_server_ip, machine_id)
    )
    if result:
        #
        #  To get legal entity name by it's id to save activity
        #  Parameters : legal entity id
        #  Return : Returns legal entity name
        #
        data = db.call_proc("sp_legal_entity_id_by_name", (legal_entity_id,))
        action = "Allocated database environment for %s " % (
            data[0]["legal_entity_name"])
        db.save_activity(session_user, frmAllocateDatabaseEnvironment, action)
    else:
        raise process_error("E076")


###############################################################################
# To Get data required for Configuring file storage
# parameter : Object of database
# return type : Tuple of Lists. List contains File Storage details list,
#  Client Group list, Legal entities list and Client servers list
###############################################################################
def get_file_storage_form_data(db):
    #
    #  To get list of form data for configuring file storage
    #  Parameters : None
    #  Return : Returns file storage details, Client group details,
    #   Legal entity details, Client server details
    #
    data = db.call_proc_with_multiresult_set(
        "sp_clientfilestorage_list", None, 4)
    file_storages = data[0]
    groups = data[1]
    les = data[2]
    machines = data[3]
    file_storages_list = return_file_storages(file_storages)
    groups_list = return_client_groups(groups)
    les_list = return_legal_entites(les)
    machines_list = return_machines(machines)
    return (
        file_storages_list, groups_list, les_list,
        machines_list
    )


###############################################################################
# To convert data fetched from database into List of object of FileStorage
# parameter : Data fetched from database (Tuple of tuples)
# return type : Returns List of object of FileStorage
###############################################################################
def return_file_storages(data):
    fn = consoleadmin.FileStorage
    file_storages = [
        fn(
            client_id=datum["client_id"],
            legal_entity_id=datum["legal_entity_id"],
            machine_id=datum["machine_id"]
        ) for datum in data
    ]
    return file_storages


###############################################################################
# To Save File storage configuration
# parameter : Object of database, Save file storage request
# return type : Returns List of object of FileStorage
###############################################################################
def save_file_storage(db, request):
    client_id = request.client_id
    legal_entity_id = request.legal_entity_id
    machine_id = request.machine_id
    #
    #  To save file storage configuration
    #  Parameters : Client id, Legal entity id, Clietn server id
    #  Return : Returns last inserted id
    #
    result = db.call_update_proc(
        "sp_clientfilestorage_save",
        (client_id, legal_entity_id, machine_id)
    )
    if result:
        #
        #  To get legal entity name by it's id to save activity
        #  Parameters : legal entity id
        #  Return : Returns legal entity name
        #
        data = db.call_proc("sp_legal_entity_id_by_name", (legal_entity_id,))
        action = "Configured file storage for %s " % (
            data[0]["legal_entity_name"])
        db.save_activity(session_user, frmConfigureFileStorage, action)
    else:
        raise process_error("E077")


###############################################################################
# To get data required for Auto deletion form
# parameter : Object of database
# return type : Returns Tuple of lists. List contains Client Groups list,
#  Legal entities list, Units List
###############################################################################
def get_auto_deletion_form_data(db):
    #
    #  To get data required for auto deletion form
    #  Parameters : None
    #  Return : Returns Client group details, Legal entity details and
    #   Unit details
    #
    data = db.call_proc_with_multiresult_set(
        "sp_unit_autodeletion_list", None, 4)
    groups = data[0]
    les = data[1]
    units = data[2]
    groups_list = return_client_groups(groups)
    les_list = return_auto_deletion_legal_entites(les)
    units_list = return_units(units)
    return (
        groups_list, les_list, units_list
    )


###############################################################################
# To convert data fetched from database into List of object of
# EntitiesWithAutoDeletion
# parameter : Data fetched from database (Tuple of tuples)
# return type : Returns List of object of EntitiesWithAutoDeletion
###############################################################################
def return_auto_deletion_legal_entites(data):
    fn = consoleadmin.EntitiesWithAutoDeletion
    result = [
        fn(
            legal_entity_id=datum["legal_entity_id"],
            legal_entity_name=datum["legal_entity_name"],
            client_id=datum["client_id"],
            unit_count=datum["unit_count"],
            deletion_period=datum["deletion_period"]
        ) for datum in data
    ]
    return result


###############################################################################
# To convert data fetched from database into List of object of Unit
# parameter : Data fetched from database (Tuple of tuples)
# return type : Returns List of object of Unit
###############################################################################
def return_units(data):
    fn = consoleadmin.Unit
    result = [
        fn(
            unit_id=datum["unit_id"], client_id=datum["client_id"],
            legal_entity_id=datum["legal_entity_id"],
            unit_code=datum["unit_code"],
            unit_name=datum["unit_name"], deletion_year=datum["deletion_year"]
        ) for datum in data
    ]
    return result


###############################################################################
# To save auto deletion details
# parameter : Object of databse, Save Auto deletion request, session user
# return type : Returns True on success full save. Otherwise raises
#   process error
###############################################################################
def save_auto_deletion_details(db, request, session_user):
    auto_deletion_details = request.auto_deletion_details
    unit_ids = []
    insert_columns = [
        "client_id", "legal_entity_id", "unit_id", "deletion_year"
    ]
    insert_values = []
    legal_entity_id = None
    for detail in auto_deletion_details:
        unit_ids.append(detail.unit_id)
        legal_entity_id = detail.legal_entity_id
        insert_values.append(
            (
                detail.client_id, detail.legal_entity_id,
                detail.unit_id, detail.deletion_year
            )
        )
    #
    #  To delete all auto deletion details under the legal entity
    #  Parameters : Legal entity id
    #  Return : True on successfull deletion otherwise returns False
    #
    db.call_update_proc("sp_unitautodeletion_delete", (legal_entity_id,))
    result = db.bulk_insert(
        tblUnitAutoDeletion, insert_columns, insert_values
    )
    if result:
        #
        #  To get legal entity name by it's id to save activity
        #  Parameters : legal entity id
        #  Return : Returns legal entity name
        #
        data = db.call_proc("sp_legal_entity_id_by_name", (legal_entity_id,))
        action = "Configured auto deletion for %s " % (
            data[0]["legal_entity_name"])
        db.save_activity(session_user, frmAutoDeletion, action)
    else:
        raise process_error("E078")
