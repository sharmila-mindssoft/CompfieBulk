from protocol import login, knowledgetransaction
from generalcontroller import validate_user_session, validate_user_forms
from server import logger

from server.database.knowledgetransaction import (
    check_duplicate_compliance_name,
    check_duplicate_statutory_mapping,
    save_statutory_mapping,
    update_statutory_mapping,
    change_statutory_mapping_status,
    statutory_mapping_master,
    statutories_master,
    statutory_mapping_list,
    approve_statutory_mapping_list,
    get_compliance_details,
    save_approve_mapping,
    get_statutory_mapping_edit
)

from server.database.knowledgemaster import (
    get_industries, get_statutory_nature
)
from server.database.admin import (
    get_countries_for_user,
    get_domains_for_user, get_child_users
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

    elif type(request_frame) is knowledgetransaction.GetApproveStatutoryMappings:
        logger.logKnowledgeApi("GetApproveStatutoryMappings", "process begin")
        result = process_get_approve_statutory_mappings(db, request_frame, user_id)
        logger.logKnowledgeApi("GetApproveStatutoryMappings", "process end")

    elif type(request_frame) is knowledgetransaction.GetApproveStatutoryMappingsFilters:
        logger.logKnowledgeApi("GetApproveStatutoryMappingFilterSuccess", "process begin")
        result = process_get_approve_mapping_filters(db, user_id)
        logger.logKnowledgeApi("GetApproveStatutoryMappingFilterSuccess", "process end")

    elif type(
        request_frame
    ) is knowledgetransaction.GetComplianceInfo:
        logger.logKnowledgeApi("GetApproveStatutoryMappings", "process begin")
        result = process_get_compliance_info(db, request_frame, user_id)
        logger.logKnowledgeApi("GetApproveStatutoryMappings", "process end")

    elif type(request_frame) is knowledgetransaction.ApproveStatutoryMapping:
        logger.logKnowledgeApi("ApproveStatutoryMapping", "process begin")
        result = process_approve_statutory_mapping(db, request_frame, user_id)
        logger.logKnowledgeApi("ApproveStatutoryMapping", "process begin")

    elif type(request_frame) is knowledgetransaction.GetComplianceEdit:
        logger.logKnowledgeApi("ApproveStatutoryMapping", "process begin")
        result = process_get_compliance_Edit(db, request_frame, user_id)
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

def process_get_approve_mapping_filters(db, user_id):
    user_id = 4
    industry = get_industries(db)
    natures = get_statutory_nature(db)
    country = get_countries_for_user(db, user_id)
    domains = get_domains_for_user(db, user_id)
    users = get_child_users(db, user_id)
    return knowledgetransaction.GetApproveStatutoryMappingFilterSuccess(
        country, domains, natures, industry, users
    )

def process_get_approve_statutory_mappings(db, request_frame, user_id):
    statutory_mappings = approve_statutory_mapping_list(db, user_id, request_frame)
    return knowledgetransaction.GetApproveStatutoryMappingSuccess(
        statutory_mappings
    )


def process_get_compliance_info(db, request, user_id):
    comp_id = request.compliance_id
    comp_info = get_compliance_details(db, user_id, comp_id)
    return knowledgetransaction.GetComplianceInfoSuccess(
        comp_info[0], comp_info[1], comp_info[2], comp_info[3],
        comp_info[4], comp_info[5], comp_info[6], comp_info[7],
        comp_info[8], comp_info[9],
    )

def process_approve_statutory_mapping(db, request_frame, user_id):
    data = request_frame.statutory_mappings
    result = save_approve_mapping(db, user_id, data)
    if result:
        return knowledgetransaction.ApproveStatutoryMappingSuccess()

def process_get_compliance_Edit(db, request, user_id):
    comp_id = request.compliance_id
    m_id = request.mapping_id
    comp_info = get_statutory_mapping_edit(db, m_id, comp_id)
    return comp_info
