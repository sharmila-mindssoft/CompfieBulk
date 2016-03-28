from protocol import mobile, login
from generalcontroller import validate_user_session

__all__ = [
    "process_client_mobile_request"
]

def process_client_mobile_request(request, db):
    session_token = request.session_token
    request_frame = request.request
    session_user = validate_user_session(db, session_token)
    if session_user is None:
        return login.InvalidSessionToken()

    elif type(request_frame) is mobile.GetVersions :
        return process_get_version(db, request)

    elif type(request_frame) is mobile.GetUsers :
        return process_get_users(db, session_user)

    elif type(request_frame) is mobile.GetUnitDatails :
        return process_get_unit_details(db, session_user)

    elif type(request_frame) is mobile.GetComplianceApplicabilityStatus :
        return process_get_compliance_applicability()

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
    pass
