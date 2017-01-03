###############################################################################
# This Controller will handle Client Coordination Manager related requests
#
# In this module "db" is an object of "KnowledgeDatabase"
###############################################################################
import time
from server import logger
from protocol import login, clientcoordinationmaster
from server.database.clientcoordinationmaster import *
from server.database.technomaster import get_user_countries
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
        result = process_get_client_unit_approval_list(db, session_user)
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
    elif(
        type(request_frame) is clientcoordinationmaster.GetClientGroupApprovalList
    ):
        result = process_client_group_approval_list(
            db, request_frame, session_user
        )

    elif(
        type(request_frame) is clientcoordinationmaster.ApproveClientGroup
    ):
        result = process_approve_client_group(
            db, request_frame, session_user
        )

    elif type(request_frame) is clientcoordinationmaster.GetLegalEntityInfo :
        result = process_get_legal_entity_info(db, request_frame, session_user)

    return result


###############################################################################
# To process the GetClientUnitApprovalList Request
# parameter : None
# return : GetClientUnitApprovalListSuccess Response
###############################################################################
def process_get_client_unit_approval_list(db, session_user):
    unit_approval_list = get_unit_approval_list(db, session_user)
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


def process_client_group_approval_list(db, request, session_user):
    countries = get_user_countries(db, session_user)
    client_groups = get_client_groups_approval_list(db, session_user)
    return clientcoordinationmaster.GetClientGroupApprovalListSuccess(
        countries=countries, group_approval_list=client_groups
    )


def process_approve_client_group(db, request, session_user):
    approve_client_group(db, request, session_user)
    return clientcoordinationmaster.ApproveClientGroupSuccess()

def process_get_legal_entity_info(db, request, session_user):
    entity_id = request.entity_id
    data = get_legal_entity_info(db, entity_id)
    return data
