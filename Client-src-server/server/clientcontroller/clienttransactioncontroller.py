from clientprotocol import (clienttransactions, clientcore)
from server.constants import RECORD_DISPLAY_COUNT

from server.clientdatabase.clienttransaction import *

from server.clientdatabase.general import (
    verify_password, get_user_company_details,
    get_countries_for_user, get_domains_for_user,
    get_business_groups_for_user, get_legal_entities_for_user,
    get_divisions_for_user, get_client_settings, get_admin_id,
    get_compliance_frequency, get_users_by_unit_and_domain,
    get_compliance_name_by_id, validate_compliance_due_date
)


__all__ = [
    "process_client_transaction_requests",
    "process_client_master_filters_request"
]


########################################################
# To Redirect the requests to the corresponding
# functions
########################################################
def process_client_transaction_requests(request, db, session_user, session_category):
    request = request.request
    print type(request)

    if type(request) is clienttransactions.GetStatutorySettingsFilters:
        result = process_client_master_filters_request(db, request, session_user)

    elif type(request) is clienttransactions.GetStatutorySettings:
        result = process_get_statutory_settings(db, request, session_user)

    elif type(request) is clienttransactions.GetSettingsCompliances:
        result = process_get_statutory_compliance(db, session_user, request)

    elif type(request) is clienttransactions.UpdateStatutorySettings:
        result = process_update_statutory_settings(
            db, request, session_user
        )

    elif type(request) is clienttransactions.ChangeStatutorySettingsLock:
        result = process_update_statutory_settings_lock(
            db, request, session_user
        )

    elif type(request) is clienttransactions.GetAssignComplianceUnits :
        result = process_get_assign_compliance_unit(db, request, session_user, session_category)

    # elif type(request) is clienttransactions.GetAssignCompliancesFormData:
    #     result = process_get_assign_compliance_form_data(
    #         db, session_user
    #     )

    elif type(request) is clienttransactions.GetComplianceTotalToAssign:
        # return unassigned compliance total for the selected unit and domain
        result = process_get_compliance_total(db, request, session_user)


    # elif type(request) is clienttransactions.GetComplianceForUnits:
    #     result = process_get_compliance_for_units(
    #         db, request, session_user
    #     )
    # elif type(request) is clienttransactions.SaveAssignedCompliance:
    #     result = process_save_assigned_compliance(
    #         db, request, session_user
    #     )

    # elif type(request) is clienttransactions.GetUserwiseCompliances:
    #     result = process_get_user_wise_compliances(
    #         db, session_user
    #     )

    elif type(request) is clienttransactions.GetAssigneeCompliances:
        result = process_get_assignee_compliances(db, request, session_user)

    elif type(request) is clienttransactions.ReassignCompliance:
        result = process_reassign_compliance(
            db, request, session_user
        )
    elif type(request) is clienttransactions.GetPastRecordsFormData:
        result = process_get_past_records_form_data(
            db, request, session_user
        )
    elif type(request) is clienttransactions.GetStatutoriesByUnit:
        result = process_get_statutories_by_unit(
            db, request, session_user
        )

    elif type(request) is clienttransactions.SavePastRecords:
        result = process_save_past_records(
            db, request, session_user, client_id
        )

    elif type(request) is clienttransactions.GetComplianceApprovalList:
        result = process_get_compliance_approval_list(
            db, request, session_user, client_id
        )

    elif type(request) is clienttransactions.ApproveCompliance:
        result = process_approve_compliance(
            db, request, session_user
        )

    elif type(request) is clienttransactions.GetReviewSettingsFilters:
        result = process_review_settings_filters(
            db, request, session_user
        )

    elif type(request) is clienttransactions.GetReviewSettingsUnitFilters:
        result = process_review_settings_unit_filters(
            db, request, session_user
        )

    elif type(request) is clienttransactions.GetReviewSettingsComplianceFilters:
        result = process_review_settings_compliance_filters(
            db, request, session_user
        )

    return result

def process_get_statutory_settings(db, request, session_user):
    le_id = request.legal_entity_id
    div_id = request.division_id
    cat_id = request.category_id
    return get_statutory_settings(db, le_id, div_id, cat_id, session_user)


def process_get_statutory_compliance(db, session_user, request):
    from_count = request.record_count
    to_count = RECORD_DISPLAY_COUNT
    unit_id = request.unit_id
    data, total_count = return_compliance_for_statutory_settings(
        db, unit_id, from_count, to_count
    )
    return clienttransactions.GetSettingsCompliancesSuccess(
        data, total_count
    )


def process_update_statutory_settings(db, request, session_user):
    return update_statutory_settings(db, request, session_user)

def process_update_statutory_settings_lock(db, request, session_user):
    unit_id = request.unit_id
    domain_id = request.domain_id
    lock = request.lock
    if (update_new_statutory_settings_lock(db, unit_id, domain_id, lock, session_user)) :
        return clienttransactions.ChangeStatutorySettingsLockSuccess()

def process_get_assign_compliance_unit(db, request, session_user, session_category):
    d_id = request.domain_id
    units = get_units_to_assig(db, d_id, session_user, session_category)
    comp_freq = get_review_settings_frequency(db)
    return clienttransactions.GetAssignComplianceUnitsSuccess(units, comp_freq)


# def process_get_assign_compliance_form_data(db, session_user):
#     countries = get_countries_for_user(db, session_user)
#     domains = get_domains_for_user(db, session_user)
#     row = get_user_company_details(db, session_user)
#     business_group_ids = row[3]
#     business_groups = get_business_groups_for_user(
#         db, business_group_ids
#     )
#     legal_entity_ids = row[2]
#     legal_entities = get_legal_entities_for_user(
#         db, legal_entity_ids
#     )
#     division_ids = row[1]
#     divisions = get_divisions_for_user(db, division_ids)
#     units = get_units_to_assig(db, session_user)
#     users = get_users_for_seating_units(db, session_user)
#     two_level_approve = get_client_settings(db)
#     client_admin = get_admin_id(db)
#     return clienttransactions.GetAssignCompliancesFormDataSuccess(
#         countries, domains, business_groups, legal_entities,
#         divisions, units, users,
#         two_level_approve, client_admin
#     )

def process_get_compliance_total(db, request, session_user):
    u_ids = request.unit_ids
    d_id = request.domain_id
    total = total_compliance_for_units(db, u_ids, d_id)
    return clienttransactions.GetComplianceTotalToAssignSuccess(total)

def process_get_compliance_for_units(db, request, session_user):
    unit_ids = request.unit_ids
    domain_id = request.domain_id
    from_count = request.record_count
    to_count = RECORD_DISPLAY_COUNT
    level_1_name, statutories, total = get_assign_compliance_statutories_for_units(
        db, unit_ids, domain_id, session_user, from_count, to_count
    )
    return clienttransactions.GetComplianceForUnitsSuccess(
        level_1_name, statutories, total
    )


def process_save_assigned_compliance(db, request, session_user):
    status, task = validate_compliance_due_date(db, request)
    if (status is False):
        return clienttransactions.InvalidDueDate(task)
    else:
        return save_assigned_compliance(db, request, session_user)


########################################################
# To get data to populate the completed task -
# current year form wizards
########################################################
def process_get_past_records_form_data(db, request, session_user):
    countries = get_countries_for_user(db, session_user)
    row = get_user_company_details(db, session_user)
    business_groups = get_business_groups_for_user(db, row[3])
    legal_entities = get_legal_entities_for_user(db, row[2])
    divisions = get_divisions_for_user(db, row[1])
    units = get_units_for_user_grouped_by_industry(db, row[0])
    domains = get_domains_for_user(db, session_user)
    level1_statutories = get_level_1_statutories_for_user_with_domain(
        db, session_user
    )
    compliance_frequency = get_compliance_frequency(
        db, "frequency_id in (2,3)"
    )
    return clienttransactions.GetPastRecordsFormDataSuccess(
        countries=countries,
        business_groups=business_groups,
        legal_entities=legal_entities,
        divisions=divisions,
        units=units,
        domains=domains,
        level_1_statutories=level1_statutories,
        compliance_frequency=compliance_frequency
    )


########################################################
# To get the compliances under the selected filters
########################################################
def process_get_statutories_by_unit(
        db, request, session_user
):
    to_count = RECORD_DISPLAY_COUNT
    unit_id = request.unit_id
    domain_id = request.domain_id
    level_1_statutory_name = request.level_1_statutory_name
    compliance_frequency = request.compliance_frequency
    country_id = request.country_id
    start_count = request.start_count
    statutory_wise_compliances, total_count = get_statutory_wise_compliances(
        db, unit_id, domain_id, level_1_statutory_name,
        compliance_frequency, country_id, session_user, start_count,
        to_count
    )
    users = get_users_by_unit_and_domain(db, unit_id, domain_id)
    return clienttransactions.GetStatutoriesByUnitSuccess(
        statutory_wise_compliances=statutory_wise_compliances,
        users=users, total_count=total_count
    )


########################################################
# To validate and save a past record entry
########################################################
def process_save_past_records(
        db, request, session_user, client_id
):
    compliance_list = request.compliances
    error = ""
    for compliance in compliance_list:
        if validate_before_save(
            db, compliance.unit_id, compliance.compliance_id,
            compliance.due_date,
            compliance.completion_date, compliance.documents,
            compliance.validity_date,
            compliance.completed_by
        ):
            continue
        else:
            compliance_name = get_compliance_name_by_id(
                db, compliance.compliance_id
            )
            error = "Cannot Submit compliance task %s, " + \
                " Because a compliance has already submited " + \
                " for the entered due date %s, or previous compliance " + \
                " has validity greater than the " + \
                " entered due date "
            error = error % (compliance_name, compliance.due_date)
            return clienttransactions.SavePastRecordsFailed(error=error)
    for compliance in compliance_list:
        if save_past_record(
            db, compliance.unit_id, compliance.compliance_id,
            compliance.due_date, compliance.completion_date,
            compliance.documents, compliance.validity_date,
            compliance.completed_by, client_id
        ):
            continue
        else:
            compliance_name = get_compliance_name_by_id(
                db, compliance.compliance_id
            )
            error = "Cannot Submit compliance task %s, " + \
                " Because a compliance has already submited " + \
                " for the entered due date %s, or previous " + \
                " compliance has validity greater than the " + \
                " entered due date"
            error = error % (compliance_name, compliance.due_date)
            return clienttransactions.SavePastRecordsFailed(error=error)
    return clienttransactions.SavePastRecordsSuccess()


########################################################
# To get the list of compliances to be approved by the
# given user
########################################################
def process_get_compliance_approval_list(db, request, session_user, client_id):
    to_count = RECORD_DISPLAY_COUNT
    compliance_approval_list, count = get_compliance_approval_list(
        db, request.start_count, to_count, session_user, client_id
    )
    total_count = get_compliance_approval_count(db, session_user)
    approval_status = [
        clientcore.COMPLIANCE_APPROVAL_STATUS("Concur"),
        clientcore.COMPLIANCE_APPROVAL_STATUS("Reject Concurrence"),
        clientcore.COMPLIANCE_APPROVAL_STATUS("Approve"),
        clientcore.COMPLIANCE_APPROVAL_STATUS("Reject Approval")
    ]
    return clienttransactions.GetComplianceApprovalListSuccess(
        approval_list=compliance_approval_list,
        approval_status=approval_status,
        total_count=total_count
    )


########################################################
# To handle approve, concur, or reject request of a
# compliance
########################################################
def process_approve_compliance(db, request, session_user):
    compliance_history_id = request.compliance_history_id
    status = request.approval_status
    remarks = request.remarks
    next_due_date = request.next_due_date
    validity_date = request.validity_date
    if status == "Approve":
        approve_compliance(
            db, compliance_history_id, remarks,
            next_due_date, validity_date
        )
    elif status == "Reject Approval":
        reject_compliance_approval(
            db, compliance_history_id, remarks,  next_due_date
        )
    elif status == "Concur":
        concur_compliance(
            db, compliance_history_id, remarks,
            next_due_date, validity_date
        )
    elif status == "Reject Concurrence":
        reject_compliance_concurrence(
            db, compliance_history_id, remarks, next_due_date
        )
    return clienttransactions.ApproveComplianceSuccess()


def process_get_user_wise_compliances(db, session_user):
    users = get_users_for_seating_units(
        db, session_user
    )
    units = get_units_for_assign_compliance(db, session_user)
    two_level_approve = get_client_settings(db)
    client_admin = get_admin_id(db)
    domains = get_domains_for_user(db, session_user)
    compliance_count = get_assigneewise_compliance_count(db, session_user)

    result = clienttransactions.GetUserwiseCompliancesSuccess(
        compliance_count, users, units,
        two_level_approve,
        client_admin, domains
    )

    return result


def process_get_assignee_compliances(db, request, session_user):
    assignee = request.assignee
    from_count = request.record_count
    to_count = RECORD_DISPLAY_COUNT
    result = get_compliance_for_assignee(
        db, session_user, assignee, from_count, to_count
    )
    assignee_wise_compliance = result[0]
    assignee_compliance_count = result[1]
    final_dict = {}

    for key, value in assignee_wise_compliance.iteritems():
        unit_list = []
        for k in sorted(value):
            unit_list.append(value.get(k))
        no_of_compliance = assignee_compliance_count[key]
        user_data = clienttransactions.USER_WISE_COMPLIANCE(
            no_of_compliance,
            unit_list
        )
        final_dict[key] = [user_data]

    return clienttransactions.GetAssigneeCompliancesSuccess(final_dict)


def process_reassign_compliance(db, request, session_user):
    return reassign_compliance(db, request, session_user)


########################################################
# To get the freqency and list of domains for based on
# legal entity
########################################################
def process_review_settings_filters(db, request, session_user):
    frequency_type = get_review_settings_frequency(db, session_user)
    domains = get_domains_for_legalentity(db, request, session_user)
    return clienttransactions.GetReviewSettingsFiltersSuccess(
        compliance_frequency=frequency_type,
        domain_list=domains
    )


########################################################
# To get the unit list for based on legal entity, domain
########################################################
def process_review_settings_unit_filters(db, request, session_user):
    units = get_review_settings_units(db, request, session_user)
    return clienttransactions.GetReviewSettingsUnitFiltersSuccess(
        rs_unit_list=units
    )


#####################################################################
# To get the compliance list for based on legal entity, domain, units
#####################################################################
def process_review_settings_compliance_filters(db, request, session_user):
    timeline = get_review_settings_timeline(db, request, session_user)
    compliances = get_review_settings_compliance(db, request, session_user)
    return clienttransactions.GetReviewSettingsComplianceFiltersSuccess(
        rs_compliance_list=compliances,
        timeline=timeline
    )

##################################################################
# Master filters
##################################################################

def process_client_master_filters_request(request, db, session_user, session_category):
    request = request.request

    if type(request) is clienttransactions.GetStatutorySettingsFilters:
        result = process_get_statu_settings_filters(db, session_user, session_category)

    elif type(request) is clienttransactions.GetAssignCompliancesFormData :
        result = process_get_assign_compliance_filters(db, session_user, session_category)

    elif type(request) is clienttransactions.GetUserToAssignCompliance :
        result = process_get_user_to_assign(db, request)

    return result


def process_get_statu_settings_filters(db, session_user, session_category):
    le_info = get_user_based_legal_entity(db, session_user, session_category)
    div_info = get_user_based_division(db, session_user, session_category)
    cat_info = get_user_based_category(db, session_user, session_category)

    return clienttransactions.GetStatutorySettingsFiltersSuccess(
        le_info, div_info, cat_info
    )

def process_get_assign_compliance_filters(db, session_user, session_category):
    le_info = get_user_based_legal_entity(db, session_user, session_category)
    div_info = get_user_based_division(db, session_user, session_category)
    cat_info = get_user_based_category(db, session_user, session_category)
    domains = get_domains_for_user(db, session_user, session_category)
    return clienttransactions.GetAssignCompliancesFormDataSuccess(
        le_info, div_info, cat_info, domains
    )

def process_get_user_to_assign(db, request):
    unit_ids = request.unit_ids
    domain_id = request.domain_id
    le_id = request.legal_entity_id
