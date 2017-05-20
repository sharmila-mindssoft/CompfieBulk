import json
from clientprotocol import (clienttransactions, clientcore)
from server.constants import RECORD_DISPLAY_COUNT

from server.clientdatabase.clienttransaction import *

from server.clientdatabase.general import (
    get_user_company_details,
    get_countries_for_user, get_domains_for_user,
    get_business_groups_for_user, get_legal_entities_for_user,
    get_divisions_for_user,
    get_compliance_frequency, get_users_by_unit_and_domain,
    get_compliance_name_by_id, validate_compliance_due_date,
    get_country_wise_domain_month_range, get_group_name, get_domains_info,
    get_assignees,
    get_units_for_user, get_user_based_units,
    save_user_widget_settings, get_user_widget_settings,
    get_themes_for_user, save_themes_for_user, update_themes_for_user,
    get_categories_for_user, get_reassign_client_users
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

    # if type(request) is clienttransactions.GetStatutorySettingsFilters:
    #     result = process_client_master_filters_request(db, request, session_user)

    if type(request) is clienttransactions.GetStatutorySettings:
        result = process_get_statutory_settings(db, request, session_user)

    elif type(request) is clienttransactions.GetSettingsCompliances:
        result = process_get_statutory_compliance(db, session_user, request)

    elif type(request) is clienttransactions.UpdateStatutorySettings:
        result = process_update_statutory_settings(
            db, request, session_user
        )
    elif type(request) is clienttransactions.SaveStatutorySettings:
        result = process_update_statutory_settings(
            db, request, session_user
        )
    elif type(request) is clienttransactions.ChangeStatutorySettingsLock:
        result = process_update_statutory_settings_lock(
            db, request, session_user
        )

    elif type(request) is clienttransactions.GetAssignComplianceUnits :
        result = process_get_assign_compliance_unit(db, request, session_user, session_category)

    elif type(request) is clienttransactions.GetComplianceTotalToAssign:
        # return unassigned compliance total for the selected unit and domain
        result = process_get_compliance_total(db, request, session_user)

    elif type(request) is clienttransactions.GetComplianceForUnits:
        result = process_get_compliance_for_units(
            db, request, session_user
        )
    elif type(request) is clienttransactions.SaveAssignedCompliance:
        result = process_save_assigned_compliance(
            db, request, session_user
        )

    elif type(request) is clienttransactions.ReassignCompliance:
        result = process_reassign_compliance(
            db, request, session_user
        )
    elif type(request) is clienttransactions.GetStatutoriesByUnit:
        result = process_get_statutories_by_unit(
            db, request, session_user
        )

    elif type(request) is clienttransactions.GetPastRecordsFormData:
        result = process_get_past_records_form_data(
            db, request, session_user, session_category
        )

    elif type(request) is clienttransactions.SavePastRecords:
        result = process_save_past_records(
            db, request, session_user
        )

    elif type(request) is clienttransactions.GetComplianceApprovalList:
        result = process_get_compliance_approval_list(
            db, request, session_user
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

    elif type(request) is clienttransactions.SaveReviewSettingsCompliance:
        result = process_save_review_settings_compliance(
            db, request, session_user
        )

    elif type(request) is clienttransactions.GetReassignComplianceFilters:
        result = process_reassign_compliance_filters(
            db, request, session_user, session_category
        )
    elif type(request) is clienttransactions.GetReAssignComplianceUnits :
        result = process_get_reassign_compliance_unit(db, request, session_user, session_category)  # GetReAssignComplianceUnits

    elif type(request) is clienttransactions.GetReAssignComplianceForUnits:
        result = process_get_reassign_compliance_for_units(
            db, request, session_user
        )

    elif type(request) is clienttransactions.GetReAssignComplianceUnits :
        result = process_get_reassign_compliance_unit(db, request, session_user, session_category)

    elif type(request) is clienttransactions.GetReAssignComplianceForUnits:
        result = process_get_reassign_compliance_for_units(
            db, request, session_user
        )
    elif type(request) is clienttransactions.HaveCompliances:
        result = process_have_compliances(
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
    domain_d = request.domain_id
    f_id = request.frequency_id
    data, total = return_compliance_for_statutory_settings(
        db, unit_id, domain_d, f_id, from_count, to_count
    )
    return clienttransactions.GetSettingsCompliancesSuccess(
        data, total
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
    c_id = request.country_id
    le_id = request.legal_entity_id

    validity_days = get_validity_days(db, c_id, d_id)
    units = get_units_to_assig(db, d_id, session_user, session_category)
    comp_freq = get_all_frequency(db, d_id)
    two_level = get_approve_level(db, le_id)

    return clienttransactions.GetAssignComplianceUnitsSuccess(units, comp_freq, validity_days, two_level)


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
    f_ids = request.frequency_ids
    total = total_compliance_for_units(db, u_ids, d_id, f_ids)
    return clienttransactions.GetComplianceTotalToAssignSuccess(total)


def process_get_compliance_for_units(db, request, session_user):
    unit_ids = request.unit_ids
    domain_id = request.domain_id
    from_count = request.record_count
    f_ids = request.frequency_ids
    to_count = RECORD_DISPLAY_COUNT
    level_1_name, statutories = get_assign_compliance_statutories_for_units(
        db, unit_ids, domain_id, f_ids, session_user, from_count, to_count
    )
    return clienttransactions.GetComplianceForUnitsSuccess(
        level_1_name, statutories
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
def process_get_past_records_form_data(db, request, session_user, session_category):
    countries = get_countries_for_user(db, session_user)
    row = get_user_company_details(db, session_user)
    business_groups = get_business_groups_for_user(db, row[3])
    legal_entities = get_legal_entities_for_user(db, row[2])
    divisions = get_divisions_for_user(db, row[1])
    category = get_categories_for_user(db, row[4])
    units = get_user_based_units(db, session_user, session_category)
    domains = get_domains_for_user(db, session_user, session_category)
    level1_statutories = get_level_1_statutories_for_user_with_domain(
        db, session_user
    )
    compliance_frequency = get_compliance_frequency(
        db, "frequency_id in (1,2,3)"
    )

    return clienttransactions.GetPastRecordsFormDataSuccess(
        countries=countries,
        business_groups=business_groups,
        legal_entities=legal_entities,
        divisions=divisions,
        category=category,
        units=units,
        domains=domains,
        level_1_statutories=level1_statutories,
        compliance_frequency=compliance_frequency
    )


########################################################
# To get the compliances under the selected filters
# Completed Task - Current Year (Past Data)
########################################################
def process_get_statutories_by_unit(
        db, request, session_user
):
    to_count = RECORD_DISPLAY_COUNT
    unit_id = request.unit_id
    domain_id = request.domain_id
    level_1_statutory_name = request.level_1_statutory_name
    compliance_frequency = request.compliance_frequency
    # country_id = request.country_id
    start_count = request.start_count
    # country_id
    statutory_wise_compliances, total_count = get_statutory_wise_compliances(
        db, unit_id, domain_id, level_1_statutory_name,
        compliance_frequency, session_user, start_count,
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
        db, request, session_user
):
    compliance_list = request.compliances
    legal_entity_id = request.legal_entity_id
    # print "legal_entity_id>>>", legal_entity_id
    error = ""
    for compliance in compliance_list:
        if validate_before_save(
            db, compliance.unit_id, compliance.compliance_id,
            compliance.due_date,
            compliance.completion_date, compliance.documents,
            compliance.completed_by
        ):
            continue
        else:
            compliance_name = get_compliance_name_by_id(
                db, compliance.compliance_id
            )
            # print "validate_before_save>>>>327"
            error = "Cannot Submit compliance task %s, " + \
                " Because a compliance has already submited " + \
                " for the entered due date %s, or previous compliance " + \
                " has validity greater than the " + \
                " entered due date "
            error = error % (compliance_name, compliance.due_date)
            return clienttransactions.SavePastRecordsFailed(error=error)
    # print "compliance.documents>>>>", compliance.documents
    for compliance in compliance_list:
        if save_past_record(
            db, compliance.unit_id, compliance.compliance_id,
            compliance.due_date, compliance.completion_date,
            compliance.documents,
            compliance.completed_by, legal_entity_id
        ):
            continue
        else:
            compliance_name = get_compliance_name_by_id(
                db, compliance.compliance_id
            )
            # print "save_past_record>>>>347"
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
def process_get_compliance_approval_list(db, request, session_user):
    to_count = RECORD_DISPLAY_COUNT
    compliance_approval_list, count = get_compliance_approval_list(
        db, request.start_count, to_count, session_user
    )
    total_count = get_compliance_approval_count(db, session_user)
    approval_status = [
        clientcore.COMPLIANCE_APPROVAL_STATUS("Concur"),
        clientcore.COMPLIANCE_APPROVAL_STATUS("Reject Concurrence"),
        clientcore.COMPLIANCE_APPROVAL_STATUS("Approve"),
        clientcore.COMPLIANCE_APPROVAL_STATUS("Reject Approval"),
        clientcore.COMPLIANCE_APPROVAL_STATUS("Rectify Concurrence"),
        clientcore.COMPLIANCE_APPROVAL_STATUS("Rectify Approval")
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
    legal_entity_id = request.legal_entity_id

    status = status[0]

    if status == "Concur":
        concurrence_status = 1
        current_status = 2
        concur_compliance(
            db, concurrence_status, compliance_history_id, remarks,
            next_due_date, validity_date, session_user, current_status
        )
    # Concurrence Rectify Option
    elif status == "Rectify Concurrence":
        concurrence_status = 2
        current_status = 0
        reject_compliance_concurrence(db, compliance_history_id, remarks, next_due_date,
                                      session_user, concurrence_status, current_status)

     # Concurrence Reject Option
    elif status == "Reject Concurrence":
        concurrence_status = 3
        current_status = 2
        concur_compliance(
            db, concurrence_status, compliance_history_id, remarks,
            next_due_date, validity_date, session_user, current_status)

    elif status == "Approve":
        approve_status = 1
        current_status = 3
        approve_compliance(
            db, approve_status, compliance_history_id, remarks,
            next_due_date, validity_date, session_user, current_status)

    elif status == "Rectify Approval":
        approve_status = 2
        current_status = 0
        reject_compliance_approval(db, compliance_history_id, remarks, next_due_date,
                                   session_user, approve_status, current_status)

    elif status == "Reject Approval":
        approve_status = 3
        current_status = 3
        approve_compliance(
            db, approve_status, compliance_history_id, remarks,
            next_due_date, validity_date, session_user, current_status)

    return clienttransactions.ApproveComplianceSuccess()


def process_reassign_compliance(db, request, session_user):
    return reassign_compliance(db, request, session_user)


########################################################
# To get the freqency and list of domains for based on
# legal entity
########################################################
def process_review_settings_filters(db, request, session_user):
    frequency_type = get_review_settings_frequency(db)
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


#####################################################################
# To save the  review settings compliance list
#####################################################################
def process_save_review_settings_compliance(db, request, session_user):
    compliances = request.rs_compliances
    save_review_settings_compliance(db, compliances, session_user)
    return clienttransactions.SaveReviewSettingsComplianceSuccess()


##################################################################
# Master filters
##################################################################

def process_client_master_filters_request(pre_request, db, session_user, session_category):
    request = pre_request.request

    if type(request) is clienttransactions.GetStatutorySettingsFilters:
        result = process_get_statu_settings_filters(db, session_user, session_category)

    elif type(request) is clienttransactions.GetAssignCompliancesFormData:
        result = process_get_assign_compliance_filters(db, session_user, session_category)

    elif type(request) is clienttransactions.GetUserToAssignCompliance:
        result = process_get_user_to_assign(db, request)

    elif type(request) is clienttransactions.GetChartFilters:
        result = process_get_chart_filters(db, request, session_user, session_category)

    elif type(request) is clienttransactions.GetAssigneewiseComplianesFilters:
        result = process_assigneewise_compliances_filters(db, session_user, session_category)

    elif type(request) is clienttransactions.GetUserWidgetData:
        result = process_get_widget_data(db, session_user, session_category)

    elif type(request) is clienttransactions.SaveWidgetData:
        result = process_save_widget_data(db, request, session_user)

    elif type(request) is clienttransactions.ChangeThemes:
        result = process_change_theme(db, request, session_user)

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
    users = get_clien_users_by_unit_and_domain(db, le_id, unit_ids, domain_id)
    two_level = get_approve_level(db, le_id)
    return clienttransactions.GetUserToAssignComplianceSuccess(users, two_level)

def process_get_chart_filters(db, request, session_user, session_category):
    le_ids = request.legal_entity_ids
    countries = get_user_based_countries(db, session_user, session_category, le_ids)
    business_groups = get_business_groups_for_user(db, None)

    units = get_units_for_assign_compliance(db, session_user, le_ids=le_ids)
    domain_info = get_country_wise_domain_month_range(db)
    group_name = get_group_name(db)

    le_info = get_user_based_legal_entity(db, session_user, session_category, le_ids)
    div_info = get_user_based_division(db, session_user, session_category, le_ids)
    cat_info = get_user_based_category(db, session_user, session_category, le_ids)
    domains = get_domains_info(db, session_user, session_category, le_ids)

    return clienttransactions.GetChartFiltersSuccess(
        countries, domains, business_groups,
        le_info, div_info, units,
        domain_info, group_name, cat_info
    )

def process_assigneewise_compliances_filters(
    db, session_user, session_category
):
    print session_user, session_category
    countries = get_user_based_countries(db, session_user, session_category)

    domain_list = get_domains_info(db, session_user, session_category)
    business_group_list = get_business_groups_for_user(db, None)
    legal_entity_list = get_user_based_legal_entity(db, session_user, session_category)
    division_list = get_user_based_division(db, session_user, session_category)
    unit_list = get_user_based_units(db, session_user, session_category)
    users_list = get_assignees(db, None)
    category_list = get_user_based_category(db, session_user, session_category, le_ids=None)
    return clienttransactions.GetAssigneewiseComplianesFiltersSuccess(
        countries=countries, business_groups=business_group_list,
        legal_entities=legal_entity_list, divisions=division_list,
        units=unit_list, users=users_list, domains=domain_list,
        categories=category_list
    )

def process_reassign_compliance_filters(db, request, session_user, session_category):
    domain_list = get_domains_for_user(db, session_user, session_category)
    unit_list = get_units_for_user(db, session_user)
    users_list = get_reassign_client_users(db)

    return clienttransactions.GetReassignComplianceFiltersSuccess(
        domains=domain_list,
        units=unit_list,
        legal_entity_users=users_list
    )

def process_get_widget_data(db, session_user, session_category):
    forms, data = get_user_widget_settings(db, session_user, session_category)
    result = []
    frm_result = []
    w_ids = []
    for d in data :
        w_ids.append(d["w_id"])
        result.append(clienttransactions.WidgetInfo(
            d["w_id"], d["width"], d["height"], d["pin_status"]
        ))

    for f in forms :
        active = False
        if f["form_id"] in w_ids :
            active = True
        frm_result.append(clienttransactions.WidgetList(
            f["form_id"], f["form_name"], active
        ))

    return clienttransactions.GetUserWidgetDataSuccess(result, frm_result)


def process_save_widget_data(db, request, session_user):
    widget_data = request.widget_data
    w_data = []
    for d in widget_data :
        w_data.append(d.to_structure())
    w_data = json.dumps(w_data)
    save_user_widget_settings(db, session_user, w_data)
    return clienttransactions.SaveWidgetDataSuccess()

def process_get_reassign_compliance_unit(db, request, session_user, session_category):
    d_id = request.d_id
    user_id = request.usr_id
    user_type = request.user_type_id
    u_id = request.unit_id

    units = get_units_to_reassig(db, d_id, user_id, user_type, u_id, session_user, session_category)

    return clienttransactions.GetReAssignComplianceUnitsSuccess(units)

def process_get_reassign_compliance_for_units(db, request, session_user):
    domain_id = request.d_id
    unit_ids = request.u_ids
    user_id = request.usr_id
    user_type = request.user_type_id
    from_count = request.r_count
    to_count = RECORD_DISPLAY_COUNT

    # level_1_name, statutories = get_assign_compliance_statutories_for_units(
    #     db, unit_ids, domain_id, f_ids, session_user, from_count, to_count
    # )
    reassign_compliances = get_reassign_compliance_for_units(
        db, domain_id, unit_ids, user_id, user_type, session_user, from_count, to_count
    )

    return clienttransactions.GetReAssignComplianceForUnitsSuccess(
        reassign_compliances
    )

#######################################################
# To Check User have Compliances
#######################################################
def process_have_compliances(db, request, session_user):
    user_id = request.user_id
    compliance_available = have_compliances(db, user_id)

    print "compliance_available>>", compliance_available
    if compliance_available:
        print "HaveComplianceFailed()"
        return clienttransactions.HaveComplianceFailed()
    else:
        print "HaveComplianceSuccess()"
        return clienttransactions.HaveComplianceSuccess()


########################################################
# To change new theme and update theme
########################################################
def process_change_theme(db, request, session_user):
    theme_name = request.theme
    theme_id = get_themes_for_user(db, session_user)

    if not theme_id:
        theme_value = save_themes_for_user(db, session_user, theme_name)
    else:
        theme_value = update_themes_for_user(db, session_user, theme_id, theme_name)

    return clienttransactions.ChangeThemeSuccess(theme_value)
