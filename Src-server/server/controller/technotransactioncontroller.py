from protocol import login, core, technotransactions
from generalcontroller import validate_user_session

__all__ =[ 
    "process_techno_transaction_request"
]

def process_techno_transaction_request(request, db):
    session_token = request.session_token
    request_frame = request.request
    user_id = validate_user_session(db, session_token)
    if user_id is None:
        return login.InvalidSessionToken()

    if type(request_frame) is technotransactions.GetAssignedStatutoriesList:
        return process_get_assigned_statutories(db, user_id)

    elif type(request_frame) is technotransactions.GetAssignedStatutoriesById:
        return process_get_assigned_statutories_by_id(db, request_frame, user_id)

    elif type(request_frame) is technotransactions.GetAssignedStatutoryWizardOneData:
        return process_get_assigned_statutory_wizard_one(db, user_id)

    elif type(request_frame) is technotransactions.GetStatutoryWizardTwoData:
        return process_get_assigned_statutory_wizard_two(db, request_frame, user_id)

    elif type(request_frame) is technotransactions.SaveAssignedStatutory:
        pass

def process_get_assigned_statutories(db, user_id):
    pass

def process_get_assigned_statutories_by_id(db, request_frame, user_id):
    pass

def process_get_assigned_statutory_wizard_one(db, user_id):
    countries = db.get_countries_for_user(user_id)
    domains = db.get_domains_for_user(user_id)
    industries = db.get_industries()
    geography_levels = db.get_geograhpy_levels_for_user(user_id)
    geographies = db.get_geographies_for_user(user_id)
    group_companies = db.get_group_companies_for_user(user_id)
    business_groups = db.get_business_groups_for_user(user_id)
    legal_entities = db.get_legal_entities_for_user(user_id)
    divisions = db.get_divisions_for_user(user_id)
    units = db.get_units_with_domains(user_id)
    return technotransactions.GetAssignedStatutoryWizardOneDataSuccess(
        countries, domains, industries, geography_levels,
        geographies, group_companies, business_groups,
        legal_entities, divisions, units
    )

def process_get_assigned_statutory_wizard_two(db, request_frame, user_id):
    pass

