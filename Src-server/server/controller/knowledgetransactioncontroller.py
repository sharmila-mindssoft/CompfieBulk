from protocol import login, knowledgetransaction
from generalcontroller import validate_user_session, validate_user_forms
from server import logger

from server.database.knowledgetransaction import (
    get_statutory_mappings,
    check_duplicate_compliance_name,
    check_duplicate_statutory_mapping,
    save_statutory_mapping,
    update_statutory_mapping,
    change_statutory_mapping_status,
    change_approval_status,
    statutory_mapping_master,
    statutories_master,
    statutory_mapping_list
)
__all__ = [
    "process_knowledge_transaction_request"
]

forms = [10, 11]


def process_knowledge_transaction_request(request, db):
    session_token = request.session_token
    request_frame = request.request
    user_id = validate_user_session(db, session_token)
    if user_id is not None:
        is_valid = validate_user_forms(db, user_id, forms, request_frame)
        if is_valid is not True:
            return login.InvalidSessionToken()

    if user_id is None:
        return login.InvalidSessionToken()

    if type(request_frame) is knowledgetransaction.GetStatutoryMappingsMaster:
        logger.logKnowledgeApi("GetStatutoryMappingsMaster", "process begin")
        result = process_get_statutory_mapping_master(db, user_id)
        logger.logKnowledgeApi("GetStatutoryMappingsMaster", "process end")

    if type(request_frame) is knowledgetransaction.GetStatutoryMaster:
        logger.logKnowledgeApi("GetStatutoryMaster", "process begin")
        result = process_get_statutory_master(db, user_id)
        logger.logKnowledgeApi("GetStatutoryMaster", "process end")

    elif type(request_frame) is knowledgetransaction.GetStatutoryMappings:
        logger.logKnowledgeApi("GetStatutoryMappings", "process begin")
        result = process_get_statutory_mappings(db, user_id, request_frame)
        logger.logKnowledgeApi("GetStatutoryMappings", "process end")

    elif type(
        request_frame
    ) is knowledgetransaction.CheckDuplicateStatutoryMapping:
        logger.logKnowledgeApi(
            "CheckDuplicateStatutoryMapping", "process begin"
        )
        result = process_check_statutory_mapping(db, request_frame)
        logger.logKnowledgeApi("CheckDuplicateStatutoryMapping", "process end")

    elif type(request_frame) is knowledgetransaction.SaveStatutoryMapping:
        logger.logKnowledgeApi("SaveStatutoryMapping", "process begin")
        result = process_save_statutory_mapping(db, request_frame, user_id)
        logger.logKnowledgeApi("SaveStatutoryMapping", "process end")

    elif type(request_frame) is knowledgetransaction.UpdateStatutoryMapping:
        logger.logKnowledgeApi("UpdateStatutoryMapping", "process begin")
        result = process_update_statutory_mapping(db, request_frame, user_id)
        logger.logKnowledgeApi("UpdateStatutoryMapping", "process end")

    elif type(
        request_frame
    ) is knowledgetransaction.ChangeStatutoryMappingStatus:
        logger.logKnowledgeApi("ChangeStatutoryMappingStatus", "process begin")
        result = process_change_statutory_mapping_status(
            db, request_frame, user_id
        )
        logger.logKnowledgeApi("ChangeStatutoryMappingStatus", "process end")

    elif type(
        request_frame
    ) is knowledgetransaction.GetApproveStatutoryMappings:
        logger.logKnowledgeApi("GetApproveStatutoryMappings", "process begin")
        result = process_get_approve_statutory_mappings(db, user_id)
        logger.logKnowledgeApi("GetApproveStatutoryMappings", "process end")

    elif type(request_frame) is knowledgetransaction.ApproveStatutoryMapping:
        logger.logKnowledgeApi("ApproveStatutoryMapping", "process begin")
        result = process_approve_statutory_mapping(db, request_frame, user_id)
        logger.logKnowledgeApi("ApproveStatutoryMapping", "process begin")

    return result


def process_get_statutory_master(db, user_id):
    return statutories_master(db, user_id)

def process_get_statutory_mapping_master(db, user_id):
    return statutory_mapping_master(db, user_id)


def process_get_statutory_mappings(db, user_id, request):
    a_status = request.approval_status_id
    rcount = request.rcount
    statutory_mappings, total = statutory_mapping_list(db, user_id, a_status, rcount)
    return knowledgetransaction.GetStatutoryMappingsSuccess(
        statutory_mappings, total
    )


def process_check_statutory_mapping(db, request_frame):
    is_duplicate = check_duplicate_statutory_mapping(db, request_frame)
    if is_duplicate is None:
        is_duplicate = False
    else:
        is_duplicate = True
    return knowledgetransaction.CheckDuplicateStatutoryMappingSuccess(
        is_duplicate
    )


def process_save_statutory_mapping(db, request_frame, user_id):
    is_duplicate = check_duplicate_compliance_name(db, request_frame)
    if is_duplicate is False:
        if (save_statutory_mapping(db, request_frame, user_id)):
            return knowledgetransaction.SaveStatutoryMappingSuccess()
    else:
        return knowledgetransaction.ComplianceNameAlreadyExists(is_duplicate)


def process_update_statutory_mapping(db, request_frame, user_id):
    is_duplicate = check_duplicate_compliance_name(db, request_frame)
    if is_duplicate is False:
        if (update_statutory_mapping(db, request_frame, user_id)):
            return knowledgetransaction.UpdateStatutoryMappingSuccess()
        else:
            return knowledgetransaction.InvalidStatutoryMappingId()
    else:
        return knowledgetransaction.ComplianceNameAlreadyExists(is_duplicate)


def process_change_statutory_mapping_status(db, request_frame, user_id):
    if (change_statutory_mapping_status(db, request_frame, user_id)):
        return knowledgetransaction.ChangeStatutoryMappingStatusSuccess()
    else:
        return knowledgetransaction.InvalidStatutoryMappingId()


def process_get_approve_statutory_mappings(db, user_id):
    statutory_mappings = get_statutory_mappings(db, user_id, for_approve=True)
    return knowledgetransaction.GetStatutoryMappingsSuccess(
        statutory_mappings
    )


def process_approve_statutory_mapping(db, request_frame, user_id):
    is_approved = False
    message = value = None
    for data in request_frame.statutory_mappings:
        result = change_approval_status(db, data, user_id)
        if result is True:
            is_approved = True
        else:
            message, value = result
            is_approved = False
            break

    if is_approved:
        return knowledgetransaction.ApproveStatutoryMappingSuccess()
    else:
        return knowledgetransaction.TransactionFailed(message, value)
