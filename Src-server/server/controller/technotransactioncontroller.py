import time
from protocol import login, technotransactions, technomasters
from generalcontroller import (
    validate_user_session, validate_user_forms
)
from server import logger
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


def process_techno_transaction_request(request, db):
    session_token = request.session_token
    request_frame = request.request
    user_id = validate_user_session(db, session_token)
    if user_id is not None:
        is_valid = validate_user_forms(db, user_id, forms, request_frame)
        if is_valid is not True:
            return login.InvalidSessionToken()

    if user_id is None:
        return login.InvalidSessionToken()

    if type(request_frame) is technotransactions.GetAssignedStatutories:
        logger.logKnowledgeApi("GetAssignedStatutoriesList", "process begin")
        logger.logKnowledgeApi("------", str(time.time()))
        result = process_get_assigned_statutories(db)
        logger.logKnowledgeApi("GetAssignedStatutoriesList", "process end")
        logger.logKnowledgeApi("------", str(time.time()))

    elif type(request_frame) is technotransactions.GetAssignedStatutoriesById:
        logger.logKnowledgeApi("GetAssignedStatutoriesById", "process begin")
        logger.logKnowledgeApi("------", str(time.time()))
        result = process_get_assigned_statutories_by_id(db, request_frame, user_id)
        logger.logKnowledgeApi("GetAssignedStatutoriesById", "process end")
        logger.logKnowledgeApi("------", str(time.time()))

    elif type(
        request_frame
    ) is technotransactions.GetAssignedStatutoryWizardOneData:
        logger.logKnowledgeApi(
            "GetAssignedStatutoryWizardOneData", "process begin"
        )
        logger.logKnowledgeApi("------", str(time.time()))
        result = process_get_assigned_statutory_wizard_one(
            db, user_id
        )
        logger.logKnowledgeApi(
            "GetAssignedStatutoryWizardOneData", "process end"
        )
        logger.logKnowledgeApi("------", str(time.time()))

    elif(
        type(
            request_frame
        ) is technotransactions.GetAssignedStatutoryWizardTwoData
    ):
        logger.logKnowledgeApi(
            "GetAssignedStatutoryWizardTwoData", "process begin")
        logger.logKnowledgeApi("------", str(time.time()))
        result = process_get_assigned_statutory_wizard_two(
            db, request_frame, user_id
        )
        logger.logKnowledgeApi(
            "GetAssignedStatutoryWizardTwoData", "process end")
        logger.logKnowledgeApi("------", str(time.time()))

    elif type(request_frame) is technotransactions.SaveAssignedStatutory:
        logger.logKnowledgeApi("SaveAssignedStatutory", "process begin")
        logger.logKnowledgeApi("------", str(time.time()))
        result = process_save_assigned_statutory(db, request_frame, user_id)
        logger.logKnowledgeApi("SaveAssignedStatutory", "process end")
        logger.logKnowledgeApi("------", str(time.time()))

    elif type(request_frame) is technotransactions.GetCountriesForGroup:
        logger.logKnowledgeApi("GetCountriesForGroup", "process begin")
        logger.logKnowledgeApi("------", str(time.time()))
        result = process_get_countries_for_groups(db, user_id)
        logger.logKnowledgeApi("GetCountriesForGroup", "process end")
        logger.logKnowledgeApi("------", str(time.time()))

    elif type(request_frame) is technotransactions.GetGroupAdminGroupUnitList:
        logger.logKnowledgeApi("GetGroupAdminGroupUnitList", "process begin")
        logger.logKnowledgeApi("------", str(time.time()))
        result = process_get_groupadmingroup_unit_list(db, user_id)
        logger.logKnowledgeApi("GetGroupAdminGroupUnitList", "process end")
        logger.logKnowledgeApi("------", str(time.time()))

    elif type(request_frame) is technotransactions.ResendGroupAdminRegnMail:
        logger.logKnowledgeApi("SendRegistraion", "process begin")
        result = resend_user_registration_mail(db, request_frame, user_id)
        logger.logKnowledgeApi("SendRegistraion", "process end")

    elif type(request_frame) is technotransactions.SendGroupAdminRegnMail:
        logger.logKnowledgeApi("SendGroupAdminRegnMail", "process begin")
        logger.logKnowledgeApi("------", str(time.time()))
        result = process_Send_GroupAdminRegn_Mail(db, request_frame, user_id)
        logger.logKnowledgeApi("SendGroupAdminRegnMail", "process end")
        logger.logKnowledgeApi("------", str(time.time()))

    elif type(request_frame) is technotransactions.GetLegalEntityClosureReportData:
        logger.logKnowledgeApi("GetLegalEntityClosureReportData", "process begin")
        logger.logKnowledgeApi("------", str(time.time()))
        result = process_get_LegalEntityClosureReportData(db, user_id)
        logger.logKnowledgeApi("GetLegalEntityClosureReportData", "process end")
        logger.logKnowledgeApi("------", str(time.time()))

    elif type(request_frame) is technotransactions.SaveLegalEntityClosureData:
        logger.logKnowledgeApi("SaveLegalEntityClosureData", "process begin")
        logger.logKnowledgeApi("------", str(time.time()))
        result = process_Save_LegalEntityClosureData(db, request_frame, user_id)
        logger.logKnowledgeApi("SaveLegalEntityClosureData", "process end")
        logger.logKnowledgeApi("------", str(time.time()))


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


def process_get_assigned_statutories(db):
    assigned_statutories = get_assigned_statutories_list(db)
    return technotransactions.GetAssignedStatutoriesSuccess(
        assigned_statutories
    )


def process_get_assigned_statutories_by_id(db, request, session_user):
    client_statutory_id = request.client_statutory_id
    level_1_statutories, assigned_statutories = get_assigned_statutories_by_id(db, client_statutory_id)
    return technotransactions.GetAssignedStatutoriesByIdSuccess(
        level_1_statutories_list=level_1_statutories,
        statutories_for_assigning=assigned_statutories
    )


def process_get_groupadmingroup_unit_list(db, session_user):
    print "inside controller"
    groupadmin_groupsList = get_groupadmin_registration_grouplist(db, session_user)
    groupadmin_unitsList = get_groupadmin_registration_unitlist(db, session_user)
    print "controller"
    print groupadmin_unitsList
    return technotransactions.getGroupAdminGroupsUnitsSuccess(
        groupadmin_groupList=groupadmin_groupsList,
        groupadmin_unitList=groupadmin_unitsList
    )


def resend_user_registration_mail(db, request, session_user):
    res = resave_registraion_token(db, request.user_id, request.email_id)
    if res:
        return technotransactions.ResendRegistraionSuccess()
    else:
        print "send email failed"


def process_Send_GroupAdminRegn_Mail(db, request_frame, session_user):
    print "inside group admin controller"
    result = send_groupadmin_registration_mail(db, request_frame, session_user)
    if result is True:
        return technotransactions.SaveGroupAdminRegnSuccess()


#
# To get the legal entity list under the techno manager for closure prrocess
#
def process_get_LegalEntityClosureReportData(db, session_user):
    result = get_LegalEntityClosureReportData(db, session_user)
    return technotransactions.LegalEntityClosureReportDataSuccess(
        legalentity_closure=result
    )


def process_Save_LegalEntityClosureData(db, request_frame, session_user):
    session_user = int(session_user)
    legal_entity_id = request_frame.legal_entity_id
    action_mode = request_frame.grp_mode
    password = request_frame.password
    remarks = request_frame.closed_remarks

    if not is_invalid_id(db, "legal_entity_id", legal_entity_id):
        print "invalid le"
        return technomasters.InvalidLegalEntityId()
    else:
        if verify_password(db, password, session_user):
            print "valid pwd"
            result = save_legalentity_closure_data(db, session_user, password, legal_entity_id, remarks, action_mode)
            print result
            if result is True:
                return technotransactions.SaveLegalEntityClosureSuccess()
        else:
            return technomasters.InvalidPassword()
