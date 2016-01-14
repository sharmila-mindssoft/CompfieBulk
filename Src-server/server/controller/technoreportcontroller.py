from protocol import login, core, technoreports
from generalcontroller import validate_user_session

__all__ =[ 
    "process_techno_report_request"
]

def process_techno_report_request(request, db):
    session_token = request.session_token
    request_frame = request.request
    user_id = validate_user_session(db, session_token)
    if user_id is None:
        return login.InvalidSessionToken()

    if type(request_frame) is technoreports.GetAssignedStatutoryReportFilters:
        return process_get_assigned_statutory_report_filters(db, user_id)

    elif type(request_frame) is technoreports.GetAssignedStatutoryReport:
        return process_get_assigned_statutory_report_data(db, request_frame, user_id)

    
def process_get_assigned_statutory_report_filters(db, user_id):
	countries = db.get_countries_for_user(user_id)
	domains = db.get_domains_for_user(user_id)
	group_companies = db.get_group_companies_for_user(user_id)
	business_groups = db.get_business_groups_for_user(user_id)
	legal_entities = db.get_legal_entities_for_user(user_id)
	divisions = db.get_divisions_for_user(user_id)
	units = db.get_units_for_user(user_id)
	return technoreports.GetClientDetailsReportFiltersSuccess(
		countries, domains, group_companies,
		business_groups, legal_entities, divisions, units
	)

def process_get_assigned_statutory_report_data(db, request_frame, user_id):
	return db.get_assigned_statutories_report(request_frame, user_id)
