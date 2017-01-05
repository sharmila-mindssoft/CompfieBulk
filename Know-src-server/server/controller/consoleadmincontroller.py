###############################################################################
# This Controller will handle Console admin related requests
#
# In this module "db" is an object of "KnowledgeDatabase"
###############################################################################
from protocol import login, consoleadmin
from server.database.consoleadmin import *
from generalcontroller import validate_user_session, validate_user_forms


__all__ = [
    "process_console_admin_request"
]

forms = [38, 39, 40, 41, 42]


###############################################################################
# process_client_coordination_master_request will process
# below mentioned request.
# parameter : request type is object of request class from clientcoordination
#   master protocol, db is database connection object.
# return :
#   return type is object of response class from
#   clientcoordination master protocol.
###############################################################################
def process_console_admin_request(request, db):
    session_token = request.session_token
    request_frame = request.request
    session_user = validate_user_session(db, session_token)
    if session_user is not None:
        admin_user_type = 1
        is_valid = validate_user_forms(
            db, session_user, forms, request_frame, admin_user_type)
        if is_valid is not True:
            return login.InvalidSessionToken()

    if session_user is None:
        return login.InvalidSessionToken()

    if(type(request_frame) is consoleadmin.GetDatabaseServerList):
        result = process_get_db_server_list(db)

    elif(type(request_frame) is consoleadmin.SaveDBServer):
        result = process_save_db_server(db, request_frame, session_user)

    elif(
        type(request_frame) is consoleadmin.GetClientServerList
    ):
        result = process_get_client_server_list(db)

    elif(type(request_frame) is consoleadmin.SaveClientServer):
        result = process_save_client_server(db, request_frame, session_user)

    elif(
        type(request_frame) is consoleadmin.GetFileServerList
    ):
        result = process_get_file_server_list(db)

    elif(
        type(request_frame) is consoleadmin.SaveFileServer
    ):
        result = process_file_server_entry(db, request_frame, session_user)

    elif(type(request_frame) is consoleadmin.GetAllocatedDBEnv):
        result = process_get_allocated_db_env(db)

    elif(type(request_frame) is consoleadmin.SaveAllocatedDBEnv):
        result = process_save_allocated_db_env(db, request_frame, session_user)

    elif(type(request_frame) is consoleadmin.GetFileStorage):
        result = process_get_file_storage(db)

    elif(type(request_frame) is consoleadmin.SaveFileStorage):
        result = process_save_file_storage(db, request_frame, session_user)

    elif(type(request_frame) is consoleadmin.GetAutoDeletionList):
        result = process_get_auto_deletion_list(
            db, request_frame, session_user)

    elif(type(request_frame) is consoleadmin.SaveAutoDeletion):
        result = process_save_auto_deletion(
            db, request_frame, session_user)

    return result


###############################################################################
# To get Database servers List
# parameter : Object of database
# return type : Returns Success response
###############################################################################
def process_get_db_server_list(db):
    db_servers = get_db_server_list(db)
    return consoleadmin.GetDbServerListSuccess(
        db_servers
    )


###############################################################################
# To save a database server
# parameter : Object of database, SaveDBServer Request, session user
# return type : Raises process error if save fails otherwise returns success
#               response
###############################################################################
def process_save_db_server(db, request, session_user):
    if is_duplicate_db_server_name(db, request.db_server_name, request.db_server_id):
        return consoleadmin.DBServerNameAlreadyExists()
    else:
        save_db_server(db, request, session_user)
        return consoleadmin.SaveDBServerSuccess()


###############################################################################
# To get client servers list
# parameter : Object of database
# return type : Returns success response
###############################################################################
def process_get_client_server_list(db):
    client_servers = get_client_server_list(db)
    return consoleadmin.GetClientServerListSuccess(
        client_servers
    )


###############################################################################
# To save client servers
# parameter : Object of database, Save Client server request
# return type : Raises process error if save fails otherwise returns success
#               response
###############################################################################
def process_save_client_server(db, request, session_user):
    if is_duplicate_client_server_name(
            db, request.client_server_name, request.client_server_id):
        return consoleadmin.ClientServerNameAlreadyExists()
    else:
        save_client_server(db, request, session_user)
        return consoleadmin.SaveClientServerSuccess()


###############################################################################
# To get list of all allocated database environments
# parameter : Object of database
# return type : Returns success response
###############################################################################
def process_get_allocated_db_env(db):
    (
        client_dbs_list, machines_list, db_servers_list, file_server_list
    ) = get_client_database_form_data(db)
    return consoleadmin.GetAllocatedDBEnvSuccess(
        client_dbs=client_dbs_list,
        client_server_name_and_id=machines_list,
        db_server_name_and_id=db_servers_list,
        file_server_list=file_server_list
    )


###############################################################################
# To save allocated database environment
# parameter : Object of database, Save Request, session user
# return type : Returns success response
###############################################################################
def process_save_allocated_db_env(db, request, session_user):
    save_allocated_db_env(db, request, session_user)
    return consoleadmin.SaveAllocatedDBEnvSuccess()


###############################################################################
# To get all file storage details
# parameter : Object of database
# return type : Returns success response
###############################################################################
def process_get_file_storage(db):
    (
        client_dbs_list, groups_list, les_list,
        machines_list
    ) = get_file_storage_form_data(db)
    return consoleadmin.GetFileStorageSuccess(
        file_storages=client_dbs_list, client_groups=groups_list,
        client_legal_entities=les_list,
        client_server_name_and_id=machines_list,
    )


###############################################################################
# To save file storage details
# parameter : Object of database, Save Request, session user
# return type : Returns success response
###############################################################################
def process_save_file_storage(db, request, session_user):
    save_file_storage(db, request, session_user)
    return consoleadmin.SaveFileStorageSuccess()


###############################################################################
# To get auto deletion details
# parameter : Object of database, Save Request, session user
# return type : Returns success response
###############################################################################
def process_get_auto_deletion_list(db, request, session_user):
    (
        groups_list, les_list, units_list
    ) = get_auto_deletion_form_data(db)
    return consoleadmin.GetAutoDeletionListSuccess(
        client_groups=groups_list, auto_deletion_entities=les_list,
        auto_deletion_units=units_list
    )


###############################################################################
# To save auto deletion details
# parameter : Object of database, Save Request, session user
# return type : Returns success response
###############################################################################
def process_save_auto_deletion(db, request, session_user):
    save_auto_deletion_details(db, request, session_user)
    return consoleadmin.SaveAutoDeletionSuccess()


###############################################################################
# To GET configure file server details
# parameter : Object of database, Get Request, session user
# return type : Returns file server records
###############################################################################
def process_get_file_server_list(db):
    file_server_list = get_file_server_list(db)
    return consoleadmin.GetFileServerListSuccess(file_server_list)


###############################################################################
# To save configure file server details
# parameter : Object of database, Save Request, session user
# return type : Returns success response
###############################################################################
def process_file_server_entry(db, request, session_user):
    if is_duplicate_file_server_name(
            db, request.file_server_name, request.file_server_id):
        return consoleadmin.FileServerNameAlreadyExists()
    else:
        file_server_entry_process(db, request, session_user)
        return consoleadmin.SaveFileServerSuccess()
