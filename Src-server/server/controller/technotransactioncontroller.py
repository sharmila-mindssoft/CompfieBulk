from protocol import login, core, technotransactions
from generalcontroller import validate_user_session, validate_user_forms

__all__ =[
    "process_techno_transaction_request"
]

forms = [21]

def process_techno_transaction_request(request, db):
    session_token = request.session_token
    request_frame = request.request
    user_id = validate_user_session(db, session_token)
    if user_id is not None :
        is_valid = validate_user_forms(db, user_id, forms, request_frame)
        if is_valid is not True :
            return login.InvalidSessionToken()

    if user_id is None:
        return login.InvalidSessionToken()

    if type(request_frame) is technotransactions.GetAssignedStatutoriesList:
        return process_get_assigned_statutories(db, user_id)

    elif type(request_frame) is technotransactions.GetAssignedStatutoriesById:
        return process_get_assigned_statutories_by_id(db, request_frame)

    elif type(request_frame) is technotransactions.GetAssignedStatutoryWizardOneData:
        return process_get_assigned_statutory_wizard_one(db, request_frame, user_id)

    elif type(request_frame) is technotransactions.GetStatutoryWizardTwoData:
        return process_get_assigned_statutory_wizard_two(db, request_frame, user_id)

    elif type(request_frame) is technotransactions.SaveAssignedStatutory:
        return process_save_assigned_statutory(db, request_frame, user_id)

def process_get_assigned_statutories(db, user_id):
    return db.get_assigned_statutories_list(user_id)

def process_get_assigned_statutories_by_id(db, request_frame):
    client_statutory_id = request_frame.client_statutory_id
    return db.get_assigned_statutories_by_id(client_statutory_id)

def process_get_assigned_statutory_wizard_one(db, request_frame, user_id):
    country_id = request_frame.country_id
    domains = db.get_domains_for_user(user_id)
    industries = db.get_industries()
    geography_levels = db.get_geograhpy_levels_for_user(user_id)
    geographies = db.get_geographies(user_id, country_id)
    group_companies = db.get_groups_for_country(country_id, user_id)
    business_groups = db.get_business_groups_for_country(country_id, user_id)
    legal_entities = db.get_legal_entity_for_country(country_id, user_id)
    divisions = db.get_divisions_for_country(country_id, user_id)
    units = db.get_units_for_country(country_id, user_id)
    return technotransactions.GetAssignedStatutoryWizardOneDataSuccess(
        domains, industries, geography_levels,
        geographies, group_companies, business_groups,
        legal_entities, divisions, units
    )

def process_get_assigned_statutory_wizard_two(db, request_frame, user_id):
    geography_id = request_frame.geography_id
    industry_id = request_frame.industry_id
    domain_id = request_frame.domain_id
    country_id = request_frame.country_id
    unit_id = request_frame.unit_id
    print unit_id
    return db.get_assign_statutory_wizard_two(
        country_id, geography_id, industry_id,
        domain_id, unit_id, user_id
    )

def process_save_assigned_statutory(db, request_frame, user_id):
    return db.save_assigned_statutories(request_frame, user_id)
