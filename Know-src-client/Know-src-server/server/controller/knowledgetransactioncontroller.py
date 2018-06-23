from protocol import knowledgetransaction

from server.database.knowledgetransaction import (
    check_duplicate_compliance_name,
    check_duplicate_statutory_mapping,
    save_statutory_mapping,
    update_statutory_mapping,
    update_only_compliance,
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
from server.constants import RECORD_DISPLAY_COUNT

__all__ = [
    "process_knowledge_transaction_request"
]


def process_knowledge_transaction_request(request, db, user_id):
    request_frame = request.request

    if type(request_frame) is knowledgetransaction.GetStatutoryMappingsMaster:
        result = process_get_statutory_mapping_master(db, user_id)

    if type(request_frame) is knowledgetransaction.GetStatutoryMaster:
        result = process_get_statutory_master(db, user_id)

    elif type(request_frame) is knowledgetransaction.GetStatutoryMappings:
        result = process_get_statutory_mappings(db, user_id, request_frame)

    elif type(
        request_frame
    ) is knowledgetransaction.CheckDuplicateStatutoryMapping:
        result = process_check_statutory_mapping(db, request_frame)

    elif type(request_frame) is knowledgetransaction.SaveStatutoryMapping:
        result = process_save_statutory_mapping(db, request_frame, user_id)

    elif type(request_frame) is knowledgetransaction.UpdateStatutoryMapping:
        result = process_update_statutory_mapping(db, request_frame, user_id)

    elif type(request_frame) is knowledgetransaction.UpdateCompliance:
        result = process_update_compliance(db, request_frame, user_id)

    elif type(
        request_frame
    ) is knowledgetransaction.ChangeStatutoryMappingStatus:
        result = process_change_statutory_mapping_status(
            db, request_frame, user_id
        )

    elif type(request_frame) is knowledgetransaction.GetApproveStatutoryMappings:
        result = process_get_approve_statutory_mappings(db, request_frame, user_id)

    elif type(request_frame) is knowledgetransaction.GetApproveStatutoryMappingsFilters:
        result = process_get_approve_mapping_filters(db, user_id)

    elif type(
        request_frame
    ) is knowledgetransaction.GetComplianceInfo:
        result = process_get_compliance_info(db, request_frame, user_id)

    elif type(request_frame) is knowledgetransaction.ApproveStatutoryMapping:
        result = process_approve_statutory_mapping(db, request_frame, user_id)

    elif type(request_frame) is knowledgetransaction.GetComplianceEdit:
        result = process_get_compliance_Edit(db, request_frame, user_id)

    return result

##############################################################################
# To return the statutory master list under user id
##############################################################################
def process_get_statutory_master(db, user_id):
    return statutories_master(db, user_id)

def process_get_statutory_mapping_master(db, user_id):
    return statutory_mapping_master(db, user_id)


def process_get_statutory_mappings(db, user_id, request):
    a_status = request.approval_status_id
    ac_status = request.active_status_id
    rcount = request.rcount
    page_limit = request.page_limit
    statutory_mappings, total = statutory_mapping_list(db, user_id, a_status, ac_status, rcount, page_limit)
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


def process_update_compliance(db, request_frame, user_id):
    is_duplicate = check_duplicate_compliance_name(db, request_frame)
    if is_duplicate is False:
        if (update_only_compliance(db, request_frame, user_id)):
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

    industry = get_industries(db)
    natures = get_statutory_nature(db)
    country = get_countries_for_user(db, user_id)
    domains = get_domains_for_user(db, user_id)
    users = get_child_users(db, user_id)
    return knowledgetransaction.GetApproveStatutoryMappingFilterSuccess(
        country, domains, natures, industry, users
    )

def process_get_approve_statutory_mappings(db, request_frame, user_id):
    from_count = request_frame.r_count
    to_count = from_count + RECORD_DISPLAY_COUNT
    if from_count != 0:
        from_count = from_count + 1
    statutory_mappings, total_count = approve_statutory_mapping_list(db, user_id, request_frame, from_count, to_count)
    print "total_count", total_count
    return knowledgetransaction.GetApproveStatutoryMappingSuccess(
        statutory_mappings, total_count
    )


def process_get_compliance_info(db, request, user_id):
    comp_id = request.compliance_id
    comp_info = get_compliance_details(db, user_id, comp_id)
    return knowledgetransaction.GetComplianceInfoSuccess(
        comp_info[0], comp_info[1], comp_info[2], comp_info[3],
        comp_info[4], comp_info[5], comp_info[6], comp_info[7],
        comp_info[8], comp_info[9], comp_info[10]
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
