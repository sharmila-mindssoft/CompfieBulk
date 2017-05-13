from protocol import technotransactions, technomasters

from server.database.admin import (
    get_domains_for_user
)
from server.database.login import verify_password
from server.database.technomaster import (
    get_clients_by_user, get_business_groups_for_user,
    get_legal_entities_for_user, get_divisions_for_user,
    get_units_for_user, is_invalid_id
)
from server.database.technotransaction import *


__all__ = [
    "process_techno_transaction_request"
]

forms = [21]


def process_techno_transaction_request(request, db, user_id):

    request_frame = request.request

    if type(request_frame) is technotransactions.GetCountriesForGroup:
        result = process_get_countries_for_groups(db, user_id)

    elif type(request_frame) is technotransactions.GetGroupAdminGroupUnitList:
        result = process_get_groupadmingroup_unit_list(db, user_id)

    elif type(request_frame) is technotransactions.ResendGroupAdminRegnMail:
        result = resend_user_registration_mail(db, request_frame, user_id)

    elif type(request_frame) is technotransactions.SendGroupAdminRegnMail:
        result = process_Send_GroupAdminRegn_Mail(db, request_frame, user_id)

    elif type(request_frame) is technotransactions.GetLegalEntityClosureReportData:
        result = process_get_LegalEntityClosureReportData(db, user_id)

    elif type(request_frame) is technotransactions.SaveLegalEntityClosureData:
        result = process_Save_LegalEntityClosureData(db, request_frame, user_id)

    return result


def process_get_assigned_statutory_wizard_one(db, user_id):
    group_companies = get_clients_by_user(db, user_id)
    business_groups = get_business_groups_for_user(db, user_id)
    legal_entities = get_legal_entities_for_user(db, user_id)
    divisions = get_divisions_for_user(db, user_id)
    categories = get_categories_for_user(db, user_id)
    domains = get_domains_for_user(db, user_id)
    units = get_units_for_user(db, user_id)
    return technotransactions.GetAssignedStatutoryWizardOneDataSuccess(
        group_companies, business_groups, legal_entities, divisions,
        categories, domains, units
    )


def process_get_assigned_statutory_wizard_two(db, request, session_user):
    level_1_statutories, statutories = get_assigned_statutory_wizard_two_data(
        db, request.client_id, request.business_group_id,
        request.legal_entity_id, request.division_id, request.category_id,
        request.domain_id_optional, request.unit_ids
    )
    return technotransactions.GetAssignedStatutoryWizardTwoDataSuccess(
        level_1_statutories_list=level_1_statutories,
        statutories_for_assigning=statutories
    )


def process_save_assigned_statutory(db, request, session_user):
    client_statutory_id = request.client_statutory_id
    client_id = request.client_id
    compliances_list = request.compliances_applicablity_status
    unit_ids = request.unit_ids
    units = request.unit_id_name
    level_1_statutory_compliance = request.level_1_statutory_wise_compliances
    submission_type = request.submission_type
    if client_statutory_id is None:
        save_assigned_statutory(
            db, client_statutory_id, client_id, compliances_list, unit_ids, units,
            level_1_statutory_compliance, submission_type, session_user
        )
    else:
        update_assigned_statutory(
            db, client_statutory_id, client_id, compliances_list, unit_ids, units,
            level_1_statutory_compliance, submission_type, session_user
        )
    return technotransactions.SaveAssignedStatutorySuccess()


def process_get_assigned_statutories_by_id(db, request, session_user):
    client_statutory_id = request.client_statutory_id
    level_1_statutories, assigned_statutories = get_assigned_statutories_by_id(db, client_statutory_id)
    return technotransactions.GetAssignedStatutoriesByIdSuccess(
        level_1_statutories_list=level_1_statutories,
        statutories_for_assigning=assigned_statutories
    )

######################################################################################
# Process to get group admin registered email units and groups list
# Parameter(s) : Object of the database, user id
# Return Type : Return lists of group admin registered email units and groups list
######################################################################################
def process_get_groupadmingroup_unit_list(db, session_user):
    groupadmin_groupsList = get_groupadmin_registration_grouplist(db, session_user)
    groupadmin_unitsList = get_groupadmin_registration_unitlist(db, session_user)
    return technotransactions.getGroupAdminGroupsUnitsSuccess(
        groupadmin_groupList=groupadmin_groupsList,
        groupadmin_unitList=groupadmin_unitsList
    )

######################################################################################
# Process to resend group admin registered email list
# Parameter(s) : Object of the database, user id, request set
# Return Type : Return the value of the email process
######################################################################################
def resend_user_registration_mail(db, request, session_user):
    res = resave_registration_token(db, request.user_id, request.email_id, request.grp_mode, session_user)
    if res:
        return technotransactions.ResendRegistraionSuccess()
    else:
        print "send email failed"

######################################################################################
# Process to send group admin registered email list
# Parameter(s) : Object of the database, user id, request set
# Return Type : Return the process message
######################################################################################
def process_Send_GroupAdminRegn_Mail(db, request_frame, session_user):
    result = send_groupadmin_registration_mail(db, request_frame, session_user)
    if result is True:
        return technotransactions.SaveGroupAdminRegnSuccess()


#
# To get the legal entity list under the techno manager for closure prrocess
#
######################################################################################
# To get legal entity closure form data
# Parameter(s) : Object of the database, user id
# Return Type : Return list of legal entity list with its status
######################################################################################
def process_get_LegalEntityClosureReportData(db, session_user):
    result = get_LegalEntityClosureReportData(db, session_user)
    return technotransactions.LegalEntityClosureReportDataSuccess(
        legalentity_closure=result
    )

######################################################################################
# To save Legal entity closure data
# Parameter(s) : Object of the database, user id, request set
# Return Type : Return value of the save process
######################################################################################
def process_Save_LegalEntityClosureData(db, request_frame, session_user):
    session_user = int(session_user)
    legal_entity_id = request_frame.legal_entity_id
    action_mode = request_frame.grp_mode
    password = request_frame.password
    remarks = request_frame.closed_remarks

    if not is_invalid_id(db, "legal_entity_id", legal_entity_id):
        return technomasters.InvalidLegalEntityId()
    else:
        if verify_password(db, password, session_user):
            result = save_legalentity_closure_data(db, session_user, password, legal_entity_id, remarks, action_mode)
            if result is True:
                return technotransactions.SaveLegalEntityClosureSuccess()
            else:
                return technotransactions.SaveLegalEntityClosureFailure()
        else:
            return technomasters.InvalidPassword()
