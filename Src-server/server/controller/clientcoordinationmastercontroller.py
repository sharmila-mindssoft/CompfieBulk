###############################################################################
# This Controller will handle Client Coordination Manager related requests
#
# In this module "db" is an object of "KnowledgeDatabase"
###############################################################################
import time
from server import logger
from protocol import login, clientcoordinationmaster
from server.database.clientcoordinationmaster import *
from generalcontroller import validate_user_session, validate_user_forms

__all__ = [
    "process_client_coordination_master_request"
]

forms = [28]


###############################################################################
# process_client_coordination_master_request will process
# below mentioned request.
# parameter : request type is object of request class from clientcoordination
#   master protocol, db is database connection object.
# return :
#   return type is object of response class from
#   clientcoordination master protocol.
###############################################################################
def process_client_coordination_master_request(request, db):
    session_token = request.session_token
    request_frame = request.request
    session_user = validate_user_session(db, session_token)
    if session_user is not None:
        is_valid = validate_user_forms(db, session_user, forms, request_frame)
        if is_valid is not True:
            return login.InvalidSessionToken()

    if session_user is None:
        return login.InvalidSessionToken()

    if(
        type(
            request_frame
        ) is clientcoordinationmaster.GetClientUnitApprovalList
    ):
        logger.logKnowledgeApi("GetClientUnitApprovalList", "process begin")
        logger.logKnowledgeApi("------", str(time.time()))
        result = process_get_client_unit_approval_list(db)
        logger.logKnowledgeApi("GetClientUnitApprovalList", "process end")
        logger.logKnowledgeApi("------", str(time.time()))

    elif type(request_frame) is clientcoordinationmaster.GetEntityApprovalList:
        logger.logKnowledgeApi("GetEntityApprovalList", "process begin")
        logger.logKnowledgeApi("------", str(time.time()))
        result = process_get_entity_unit_approval_list(
            db, request_frame, session_user
        )
        logger.logKnowledgeApi("GetEntityApprovalList", "process end")
        logger.logKnowledgeApi("------", str(time.time()))

    elif type(request_frame) is clientcoordinationmaster.ApproveUnit:
        logger.logKnowledgeApi("ApproveUnit", "process begin")
        logger.logKnowledgeApi("------", str(time.time()))
        result = process_approve_unit(
            db, request_frame, session_user
        )
        logger.logKnowledgeApi("ApproveUnit", "process end")
        logger.logKnowledgeApi("------", str(time.time()))

    return result


###############################################################################
# To process the GetClientUnitApprovalList Request
# parameter : None
# return : GetClientUnitApprovalListSuccess Response
###############################################################################
def process_get_client_unit_approval_list(db):
    unit_approval_list = get_unit_approval_list(db)
    return clientcoordinationmaster.GetClientUnitApprovalListSuccess(
        unit_approval_list)


###############################################################################
# To process the GetEntityApprovalList Request
# parameter : Object of database, request, and user id
# return : GetEntityApprovalListSuccess Response
###############################################################################
def process_get_entity_unit_approval_list(db, request, session_user):
    units_list = get_entity_units_list(db, request.legal_entity_id)
    return clientcoordinationmaster.GetEntityApprovalListSuccess(
        units_list
    )


###############################################################################
# To process the ApproveUnit Request
# parameter : Object of database, request, and user id
# return : ApproveUnitSuccess Response
###############################################################################
def process_approve_unit(db, request, session_user):
    approve_unit(db, request, session_user)
    return clientcoordinationmaster.ApproveUnitSuccess()
