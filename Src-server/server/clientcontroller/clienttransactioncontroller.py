from protocol import (clienttransactions, clientmasters, login, core)
from server import logger
import threading
__all__ = [
    "process_client_transaction_requests"
]

########################################################
# To Redirect the requests to the corresponding
# functions
########################################################
def process_client_transaction_requests(request, db) :
    client_info = request.session_token.split("-")
    session_token = request.session_token
    request = request.request
    client_id = int(client_info[0])
    session_user = db.validate_session_token(client_id, session_token)
    if session_user is None:
        return login.InvalidSessionToken()

    if type(request) is clienttransactions.GetStatutorySettings :
        logger.logClientApi("GetStatutorySettings", "process begin")
        result = process_get_statutory_settings(db, session_user, client_id)
        logger.logClientApi("GetStatutorySettings", "process end")

    elif type(request) is clienttransactions.GetSettingsCompliances :
        logger.logClientApi("GetSettingsCompliances", "process begin")
        result = process_get_statutory_compliance(db, session_user, request)
        logger.logClientApi("GetSettingsCompliances", "process end")

    elif type(request) is clienttransactions.UpdateStatutorySettings :
        logger.logClientApi("UpdateStatutorySettings", "process begin")
        result = process_update_statutory_settings(
            db, request, session_user, client_id
        )
        logger.logClientApi("UpdateStatutorySettings", "process end")

    elif type(request) is clienttransactions.GetAssignCompliancesFormData:
        logger.logClientApi("GetAssignCompliancesFormData", "process begin")
        result = process_get_assign_compliance_form_data(
            db, session_user, client_id
        )
        logger.logClientApi("GetAssignCompliancesFormData", "process end")

    elif type(request) is clienttransactions.GetComplianceForUnits:
        logger.logClientApi("GetComplianceForUnits", "process begin")
        result = process_get_compliance_for_units(
            db, request, session_user, client_id
        )
        logger.logClientApi("GetComplianceForUnits", "process end")

    elif type(request) is clienttransactions.SaveAssignedCompliance :
        logger.logClientApi("SaveAssignedCompliance", "process begin")
        result = process_save_assigned_compliance(
            db, request, session_user, client_id
        )
        logger.logClientApi("SaveAssignedCompliance", "process end")

    elif type(request) is clienttransactions.GetUserwiseCompliances :
        logger.logClientApi("GetUserwiseCompliances", "process begin")
        result = process_get_user_wise_compliances(
            db, session_user, client_id
        )
        logger.logClientApi("GetUserwiseCompliances", "process end")

    elif type(request) is clienttransactions.GetAssigneeCompliances :
        logger.logClientApi("GetAssigneeCompliances", "process begin")
        result = process_get_assignee_compliances(db, request, session_user)
        logger.logClientApi("GetAssigneeCompliances", "process end")

    elif type(request) is clienttransactions.ReassignCompliance :
        result = process_reassign_compliance(
            db, request, session_user
        )
    elif type(request) is clienttransactions.GetPastRecordsFormData :
        logger.logClientApi("GetPastRecordsFormData", "process begin")
        result = process_get_past_records_form_data(
            db, request, session_user, client_id
        )
        logger.logClientApi("GetPastRecordsFormData", "process end")

    elif type(request) is clienttransactions.GetStatutoriesByUnit :
        logger.logClientApi("GetStatutoriesByUnit", "process begin")
        result = process_get_statutories_by_unit(
            db, request, session_user, client_id
        )
        logger.logClientApi("GetStatutoriesByUnit", "process end")

    elif type(request) is clienttransactions.SavePastRecords :
        logger.logClientApi("SavePastRecords", "process begin")
        result = process_save_past_records(
            db, request, session_user, client_id
        )
        logger.logClientApi("SavePastRecords", "process end")

    elif type(request) is clienttransactions.GetComplianceApprovalList :
        logger.logClientApi("GetComplianceApprovalList", "process begin")
        result = process_get_compliance_approval_list(
            db, request, session_user, client_id
        )
        logger.logClientApi("GetComplianceApprovalList", "process end")

    elif type(request) is clienttransactions.ApproveCompliance:
        logger.logClientApi("ApproveCompliance", "process begin")
        result = process_approve_compliance(
            db, request, session_user, client_id
        )
        logger.logClientApi("ApproveCompliance", "process end")

    return result


def process_get_statutory_settings(db, session_user, client_id):
    return db.get_statutory_settings(session_user, client_id)

def process_get_statutory_compliance(db, session_user, request):
    from_count = request.record_count
    to_count = 500
    unit_id = request.unit_id

    data, total_count = db.return_compliance_for_statutory_settings(unit_id, from_count, to_count)
    return clienttransactions.GetSettingsCompliancesSuccess(
        data, total_count
    )

def process_update_statutory_settings(db, request, session_user, client_id):
    password = request.password
    if db.verify_password(password, session_user) :
        return db.update_statutory_settings(request, session_user, client_id)
    else :
        return clientmasters.InvalidPassword()

def process_get_assign_compliance_form_data(db, session_user, client_id):
    countries = db.get_countries_for_user(session_user)
    domains = db.get_domains_for_user(session_user)
    row = db.get_user_company_details(session_user)
    business_group_ids = row[3]
    business_groups = db.get_business_groups_for_user(
        business_group_ids
    )
    legal_entity_ids = row[2]
    legal_entities = db.get_legal_entities_for_user(
        legal_entity_ids
    )
    division_ids = row[1]
    divisions = db.get_divisions_for_user(division_ids)
    units = db.get_units_for_assign_compliance(session_user)
    users = db.get_users_for_seating_units(session_user, client_id)
    two_level_approve = db.get_client_settings()
    client_admin = db.get_admin_info()
    return clienttransactions.GetAssignCompliancesFormDataSuccess(
        countries, domains, business_groups, legal_entities,
        divisions, units, users,
        two_level_approve, client_admin
    )

def process_get_compliance_for_units(db, request, session_user, client_id):
    unit_ids = request.unit_ids
    domain_id = request.domain_id
    from_count = request.record_count
    to_count = 250
    level_1_name, statutories, total = db.get_assign_compliance_statutories_for_units(
        unit_ids, domain_id, session_user, from_count, to_count
    )
    return clienttransactions.GetComplianceForUnitsSuccess(
        level_1_name, statutories, total
    )

def process_save_assigned_compliance(db, request, session_user, client_id):
    if (db.validate_compliance_due_date(request) is False) :
        return clienttransactions.InvalidDueDate()
    else :
        return db.save_assigned_compliance(request, session_user, client_id)

########################################################
# To get data to populate the completed task -
# current year form wizards
########################################################
def process_get_past_records_form_data(db, request, session_user, client_id):
    countries = db.get_countries_for_user(session_user, client_id)
    row = db.get_user_company_details(session_user, client_id)
    business_groups = db.get_business_groups_for_user(row[3])
    legal_entities = db.get_legal_entities_for_user(row[2])
    divisions = db.get_divisions_for_user(row[1])
    units = db.get_units_for_user_grouped_by_industry(row[0])
    domains = db.get_domains_for_user(session_user, client_id)
    level1_statutories = db.get_level_1_statutories_for_user_with_domain(session_user, client_id)
    compliance_frequency = db.get_compliance_frequency(client_id, "frequency_id in (2,3)")
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
        db, request, session_user, client_id
):
    unit_id = request.unit_id
    domain_id = request.domain_id
    level_1_statutory_name = request.level_1_statutory_name
    compliance_frequency = request.compliance_frequency
    country_id = request.country_id
    statutory_wise_compliances = db.get_statutory_wise_compliances(
        unit_id,
        domain_id, level_1_statutory_name,
        compliance_frequency, country_id,
        session_user
    )
    users = db.get_users_by_unit_and_domain(unit_id, domain_id)
    return clienttransactions.GetStatutoriesByUnitSuccess(
        statutory_wise_compliances=statutory_wise_compliances,
        users=users
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
        if db.validate_before_save(
            compliance.unit_id, compliance.compliance_id, compliance.due_date,
            compliance.completion_date, compliance.documents, compliance.validity_date,
            compliance.completed_by, client_id
        ):
            continue
        else:
            compliance_name = db.get_compliance_name_by_id(compliance.compliance_id)
            error ="Cannot Submit compliance task {}, Because a compliance has already submited \
                for the entered due date {}, or previous compliance has validity greater than the \
                entered due date".format(compliance_name, compliance.due_date)
            return clienttransactions.SavePastRecordsFailed(error=error)
    for compliance in compliance_list:
        if db.save_past_record(
                compliance.unit_id, compliance.compliance_id, compliance.due_date,
                compliance.completion_date, compliance.documents, compliance.validity_date,
                compliance.completed_by, client_id
            ):
            continue
        else:
            compliance_name = db.get_compliance_name_by_id(compliance.compliance_id)
            error = "Cannot Submit compliance task {}, Because a compliance has already submited \
                for the entered due date {}, or previous compliance has validity greater than the \
                entered due date".format(compliance_name, compliance.due_date)
            return clienttransactions.SavePastRecordsFailed(error=error)
    return clienttransactions.SavePastRecordsSuccess()

########################################################
# To get the list of compliances to be approved by the
# given user
########################################################
def process_get_compliance_approval_list(db, request, session_user, client_id):
    to_count = 500
    compliance_approval_list = db.get_compliance_approval_list(
        request.start_count, to_count, session_user, client_id
    )
    total_count = db.get_compliance_approval_count(session_user)
    approval_status = [
        core.COMPLIANCE_APPROVAL_STATUS("Concur"),
        core.COMPLIANCE_APPROVAL_STATUS("Reject Concurrence"),
        core.COMPLIANCE_APPROVAL_STATUS("Approve"),
        core.COMPLIANCE_APPROVAL_STATUS("Reject Approval")
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
def process_approve_compliance(db, request, session_user, client_id):
    compliance_history_id = request.compliance_history_id
    status = request.approval_status
    remarks = request.remarks
    next_due_date = request.next_due_date
    validity_date = request.validity_date
    if status == "Approve":
        db.approve_compliance(
            compliance_history_id, remarks, next_due_date, validity_date, client_id
        )
    elif status == "Reject Approval":
        db.reject_compliance_approval(
            compliance_history_id, remarks,  next_due_date, client_id
        )
    elif status == "Concur":
        db.concur_compliance(
            compliance_history_id, remarks, next_due_date, validity_date, client_id
        )
    elif status == "Reject Concurrence":
        db.reject_compliance_concurrence(
            compliance_history_id, remarks, next_due_date, client_id
        )
    return clienttransactions.ApproveComplianceSuccess()

def process_get_user_wise_compliances(db, session_user, client_id):
    users = db.get_users_for_seating_units(
        session_user, client_id
    )
    units = db.get_units_for_assign_compliance(session_user)

    two_level_approve = db.get_client_settings()
    client_admin = db.get_admin_info()

    compliance_count = db.get_assigneewise_complaince_count(session_user)

    result = clienttransactions.GetUserwiseCompliancesSuccess(
        compliance_count, users, units,
        two_level_approve,
        client_admin
    )

    return result

def process_get_assignee_compliances(db, request, session_user):
    assignee = request.assignee
    from_count = request.record_count
    to_count = 500
    result = db.get_compliance_for_assignee(session_user, assignee, from_count, to_count)
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
    return db.reassign_compliance(request, session_user)
