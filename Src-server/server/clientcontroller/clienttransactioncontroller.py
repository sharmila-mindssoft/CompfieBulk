from protocol import (clienttransactions, clientmasters, login, core)

__all__ = [
    "process_client_transaction_requests"
]

def process_client_transaction_requests(request, db) :
    client_info = request.session_token.split("-")
    session_token = request.session_token
    request = request.request
    client_id = int(client_info[0])
    session_user = db.validate_session_token(client_id, session_token)
    if session_user is None:
        return login.InvalidSessionToken()

    if type(request) is clienttransactions.GetStatutorySettings :
        return process_get_statutory_settings(db, session_user, client_id)

    elif type(request) is clienttransactions.UpdateStatutorySettings :
        return process_update_statutory_settings(
            db, request, session_user, client_id
        )
    elif type(request) is clienttransactions.GetAssignCompliancesFormData:
        return process_get_assign_compliance_form_data(
            db, session_user, client_id
        )
    elif type(request) is clienttransactions.GetComplianceForUnits:
        return process_get_compliance_for_units(
            db, request, session_user, client_id
        )
    elif type(request) is clienttransactions.SaveAssignedCompliance :
        return process_save_assigned_compliance(
            db, request, session_user, client_id
        )
    elif type(request) is clienttransactions.GetUserwiseCompliances :
        return process_get_user_wise_compliances(
            db, session_user, client_id
        )
    elif type(request) is clienttransactions.ReassignCompliance :
        return process_reassign_compliance(
            db, request, session_user
        )
    elif type(request) is clienttransactions.GetPastRecordsFormData :
        return process_get_past_records_form_data(
            db, request, session_user, client_id
        )
    elif type(request) is clienttransactions.GetStatutoriesByUnit :
        return process_get_statutories_by_unit(
            db, request, session_user, client_id
        )
    elif type(request) is clienttransactions.SavePastRecords :
        return process_save_past_records(
            db, request, session_user, client_id
        )
    elif type(request) is clienttransactions.GetComplianceApprovalList :
        return process_get_compliance_approval_list(
            db, request, session_user, client_id
        )
    elif type(request) is clienttransactions.ApproveCompliance:
        return process_approve_compliance(
            db, request, session_user, client_id
        )

def process_get_statutory_settings(db, session_user, client_id):
    return db.get_statutory_settings(session_user, client_id)

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
    units = db.get_units_for_assign_compliance(session_user, client_id)
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
    statutories = db.get_assign_compliance_statutories_for_units(
        unit_ids, session_user, client_id
    )
    return clienttransactions.GetComplianceForUnitsSuccess(statutories)

def process_save_assigned_compliance(db, request, session_user, client_id):
    return db.save_assigned_compliance(
        request, session_user, client_id
    )

def process_get_past_records_form_data(db, request, session_user, client_id):
    countries = db.get_countries_for_user(session_user, client_id)
    row = db.get_user_company_details(session_user, client_id)
    business_groups = db.get_business_groups_for_user(row[3])
    legal_entities = db.get_legal_entities_for_user(row[2])
    divisions = db.get_divisions_for_user(row[1])
    units = db.get_units_for_user_grouped_by_industry(row[0])
    domains = db.get_domains_for_user(session_user, client_id)
    level1_statutories = db.get_level_1_statutories_for_user_with_domain(session_user, client_id)
    compliance_frequency = db.get_compliance_frequency(client_id)
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

def process_get_statutories_by_unit(
        db, request, session_user, client_id
    ):
    unit_id = request.unit_id
    domain_id = request.domain_id
    level_1_statutory_name = request.level_1_statutory_name
    compliance_frequency = request.compliance_frequency
    country_id = 1
    statutory_wise_compliances = db.get_statutory_wise_compliances(
        unit_id,
        domain_id, level_1_statutory_name,
        compliance_frequency, country_id
    )
    users = db.get_users_by_unit_and_domain(unit_id, domain_id)
    return clienttransactions.GetStatutoriesByUnitSuccess(
        statutory_wise_compliances = statutory_wise_compliances,
        users = users
    )

def process_save_past_records(
        db, request, session_user, client_id
    ):
    compliance_list = request.compliances
    for compliance in compliance_list:
        db.save_past_record(
            compliance.unit_id, compliance.compliance_id, compliance.due_date,
            compliance.completion_date, compliance.documents, compliance.validity_date,
            compliance.completed_by, client_id
        )
    return clienttransactions.SavePastRecordsSuccess()

def process_get_compliance_approval_list(db, request, session_user, client_id):
    compliance_approval_list = db.get_compliance_approval_list(
        session_user, client_id
    )
    approval_status = [
        core.COMPLIANCE_APPROVAL_STATUS("Concur"),
        core.COMPLIANCE_APPROVAL_STATUS("Reject Concurrence"),
        core.COMPLIANCE_APPROVAL_STATUS("Approve"),
        core.COMPLIANCE_APPROVAL_STATUS("Reject Approval")
    ]
    return clienttransactions.GetComplianceApprovalListSuccess(
        approval_list=compliance_approval_list,
        approval_status=approval_status
    )


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
    units = db.get_units_for_assign_compliance(session_user, client_id)
    result = db.get_user_wise_compliance(session_user, client_id)
    assignee_wise_compliance = result[0]
    assignee_compliance_count = result[1]
    final_dict = {}

    for key, value in assignee_wise_compliance.iteritems():
        unit_list = []
        for k, v in value.iteritems():
            unit_list.append(v)
        no_of_compliance = assignee_compliance_count[key]
        user_data = clienttransactions.USER_WISE_COMPLIANCE(
            no_of_compliance,
            unit_list
        )
        final_dict[key] = [user_data]

    two_level_approve = db.get_client_settings()
    client_admin = db.get_admin_info()

    result = clienttransactions.GetUserwiseCompliancesSuccess(
        final_dict, users, units,
        two_level_approve,
        client_admin
    )

    return result

def process_reassign_compliance(db, request, session_user):
    return db.reassign_compliance(request, session_user)
