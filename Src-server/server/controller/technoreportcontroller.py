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
	print "Validated session token : request frame : {}".format(request_frame)
	if type(request_frame) is technoreports.GetAssignedStatutoryReportFilters:
		return process_get_assigned_statutory_report_filters(db, user_id)
	elif type(request_frame) is technoreports.GetAssignedStatutoryReport:
		return process_get_assigned_statutory_report_data(db, request_frame, user_id)
	elif type(request_frame) is technoreports.GetClientDetailsReportFilters:
		return process_get_client_details_report_filters(db, request_frame, user_id) 
	elif type(request_frame) is technoreports.GetClientDetailsReportData:
		return process_get_client_details_report_data(db, request_frame, user_id) 
	elif type(request_frame) is technoreports.GetStatutoryNotificationsFilters:
		return process_get_statutory_notifications_filters(db, request_frame, user_id) 
	elif type(request_frame) is technoreports.GetStatutoryNotificationsReportData:
		return process_get_statutory_notifications_report_data(db, request_frame, user_id) 
 
def process_get_assigned_statutory_report_filters(db, user_id):
	countries = db.get_countries_for_user(user_id)
	domains = db.get_domains_for_user(user_id)
	group_companies = db.get_group_companies_for_user(user_id)
	business_groups = db.get_business_groups_for_user(user_id)
	legal_entities = db.get_legal_entities_for_user(user_id)
	divisions = db.get_divisions_for_user(user_id)
	units = db.get_units_for_user(user_id)
	level_1_statutories = db.get_country_wise_level_1_statutoy()
	return technoreports.GetAssignedStatutoryReportFiltersSuccess(
		countries, domains, group_companies,
		business_groups, legal_entities, divisions, units,
		level_1_statutories
	)

def process_get_assigned_statutory_report_data(db, request_frame, user_id):
	return db.get_assigned_statutories_report(request_frame, user_id)

def process_get_statutory_notifications_filters(db, request_frame, user_id):
	countries = db.get_countries_for_user(user_id)
	domains = db.get_domains_for_user(user_id)
	level_1_statutories = db.get_country_wise_level_1_statutoy()
	return technoreports.GetStatutoryNotificationsFiltersSuccess(countries = countries, domains = domains, 
	 level_1_statutories = level_1_statutories)

def process_get_statutory_notifications_report_data(db, request, user_id):
	countries = db.get_countries_for_user(user_id)
	domains = db.get_domains_for_user(user_id)
	level_1_statutories = db.get_country_wise_level_1_statutoy()
	print "level_!_statatatat: {} ".format(level_1_statutories)
	print "inside process_get_statutory_notifications_report_data: {}".format(request)
	result = db.get_statutory_notifications_report_data(request)
	return technoreports.GetStatutoryNotificationsReportDataSuccess(countries, domains, level_1_statutories, result)

def process_get_client_details_report_filters(db, request_frame, session_user):
	countries = db.get_countries_for_user(session_user)
	domains = db.get_domains_for_user(session_user)
	group_companies = db.get_group_companies_for_user(session_user)
	business_groups = db.get_business_groups_for_user(session_user)
	legal_entities = db.get_legal_entities_for_user(session_user)
	divisions = db.get_divisions_for_user(session_user)
	units = db.get_units_for_user(session_user)
	return technoreports.GetClientDetailsReportFiltersSuccess(countries = countries, domains = domains, 
		group_companies = group_companies, business_groups = business_groups, 
		legal_entities = legal_entities, divisions = divisions, units = units)

def process_get_client_details_report_data(db, request, session_user):
	units = db.get_client_details_report(request.country_id, request.group_id, request.business_group_id, 
            request.legal_entity_id, request.division_id, request.unit_id, request.domain_ids)
	return technoreports.GetClientDetailsReportDataSuccess(units = units)
