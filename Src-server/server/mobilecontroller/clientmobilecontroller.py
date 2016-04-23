from protocol import mobile, login
from server.controller.generalcontroller import validate_user_session

__all__ = [
    "process_client_mobile_request"
]

def process_client_mobile_request(request, db):
    client_info = request.session_token.split("-")
    session_token = request.session_token
    request_frame = request.request
    client_id = int(client_info[0])
    session_user = db.validate_session_token(client_id, session_token)

    if session_user is None:
        return login.InvalidSessionToken()

    elif type(request_frame) is mobile.GetVersions :
        return process_get_version(db, request)

    elif type(request_frame) is mobile.GetUsers :
        return process_get_users(db, session_user)

    elif type(request_frame) is mobile.GetUnitDetails :
        return process_get_unit_details(db, session_user)
    elif type(request_frame) is mobile.GetComplianceApplicabilityStatus :
        return process_get_compliance_applicability(db, session_user)
    elif type(request_frame) is mobile.GetComplianceHistory :
        return process_get_compliance_history(db, session_user, request_frame)
    elif type(request_frame) is mobile.CheckDiskSpace :
        return process_check_disk_space(db)
    elif type(request_frame) is mobile.GetTrendChartData :
        return process_get_trend_chart(db, session_user)
    elif type(request_frame) is mobile.SaveRegistrationKey :
        return

def process_get_version(db, request):
    data = db.get_version()
    return mobile.GetVersionsSuccess(
        int(data["unit_details"]),
        int(data["user_details"]),
        int(data["compliance_applicability"]),
        int(data["compliance_history"]),
        int(data["reassign_history"])
    )

def process_get_users(db, session_user):
    users = db.get_users_for_mobile(session_user)
    return mobile.GetUsersSuccess(users)

def process_get_unit_details(db, session_user):
    countries = db.get_countries_for_user(session_user)
    domains = db.get_domains_for_user(session_user)
    business_groups = db.get_business_groups_for_mobile()
    legal_entity = db.get_legal_entities_for_mobile()
    division = db.get_divisions_for_mobile()
    units = db.get_units_for_assign_compliance(session_user)
    return mobile.GetUnitDetailsSuccess(
        countries, domains,
        business_groups, legal_entity,
        division, units
    )

def process_get_compliance_applicability(db, session_user):
    data = db.get_compliance_applicability_for_mobile(session_user)
    return mobile.GetComplianceApplicabilityStatusSuccess(data)

def process_get_trend_chart(db, session_user):
    data = db.get_trend_chart_for_mobile(session_user)
    return mobile.GetTrendChartDataSuccess(data)

def process_get_compliance_history(db, session_user, request):
    data = db.get_compliance_history_for_mobile(session_user, request)
    return mobile.GetComplianceHistorySuccess(data)

def process_check_disk_space(db):
    data = db.get_check_disk_space_for_mobile()
    return mobile.CheckDiskSpaceSuccess(
        int(data["total_disk_space"]),
        int(data["total_disk_space_used"])
    )

def process_save_registration_key(db, session_user, request):
    db.save_registration_key(session_user, request)
    return mobile.SaveRegistrationKeySuccess()
    # return mobile.InvalidRegistrationKey()
