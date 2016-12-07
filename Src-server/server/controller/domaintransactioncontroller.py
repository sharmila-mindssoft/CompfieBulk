import time
from protocol import login, technotransactions
from generalcontroller import (validate_user_session)
from server import logger
# from server.database.login import verify_password

_all__ = ["process_domain_transaction_request"]

def process_domain_transaction_request(request, db):
    session_token = request.session_token
    request_frame = request.request
    user_id = validate_user_session(db, session_token)
    # if user_id is not None:
    #     is_valid = validate_user_forms(db, user_id, forms, request_frame)
    #     if is_valid is not True:
    #         return login.InvalidSessionToken()

    if user_id is None:
        return login.InvalidSessionToken()

    if type(request_frame) is technotransactions.GetAssignedStatutories:
        logger.logKnowledgeApi("GetAssignedStatutoriesList", "process begin")
        logger.logKnowledgeApi("------", str(time.time()))
        result = process_get_approve_statutory_list(db, user_id)
        logger.logKnowledgeApi("GetAssignedStatutoriesList", "process end")
        logger.logKnowledgeApi("------", str(time.time()))

    return result

def process_get_approve_statutory_list(db, user_id):
    pass
