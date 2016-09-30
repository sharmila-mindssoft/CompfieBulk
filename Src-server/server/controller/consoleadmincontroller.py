###############################################################################
# This Controller will handle Console admin related requests
#
# In this module "db" is an object of "KnowledgeDatabase"
###############################################################################
import time
from server import logger
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
    print "inside process console admin"
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

    if(
        type(request_frame) is consoleadmin.GetDbServerList
    ):
        logger.logKnowledgeApi("GetDbServerList", "process begin")
        logger.logKnowledgeApi("------", str(time.time()))
        result = process_get_db_server_list(db)
        logger.logKnowledgeApi("GetDbServerList", "process end")
        logger.logKnowledgeApi("------", str(time.time()))

    elif(type(request_frame) is consoleadmin.SaveDBServer):
        logger.logKnowledgeApi("SaveDBServer", "process begin")
        logger.logKnowledgeApi("------", str(time.time()))
        result = process_save_db_server(db, request_frame, session_user)
        logger.logKnowledgeApi("SaveDBServer", "process end")
        logger.logKnowledgeApi("------", str(time.time()))
    return result


def process_get_db_server_list(db):
    db_servers = get_db_server_list(db)
    return consoleadmin.GetDbServerListSuccess(
        db_servers
    )


def process_save_db_server(db, request, session_user):
    if is_duplicate_db_server_name(db, request.db_server_name, request.ip):
        return consoleadmin.DBServerNameAlreadyExists()
    else:
        save_db_server(db, request, session_user)
        return consoleadmin.SaveDBServerSuccess()
