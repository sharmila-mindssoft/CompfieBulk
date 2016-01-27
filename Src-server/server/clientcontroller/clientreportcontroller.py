from protocol import (clientmasters, core, clientreport)
from server.controller.corecontroller import process_user_menus

__all__ = [
	"process_client_report_requests"
]

def process_client_report_requests(request, db) :
	session_token = request.session_token
	client_info = request.session_token.split("-")
	request = request.request
	client_id = int(client_info[0])
	session_user = db.validate_session_token(client_id, session_token)
	if session_user is None:
		return login.InvalidSessionToken()

	if type(request) is clientmasters.GetServiceProviders: 
		return get_service_providers(db, request, session_user, client_id)
	elif type(request) is clientreport.GetClientReportFilters:
		return get_client_report_filters(db, request, session_user, client_id)
	elif type(request) is clientreport.GetUnitwisecomplianceReport:
		return get_unitwise_compliance(db, request, session_user, client_id)


def get_client_report_filters(db, request, session_user, client_id):
	user_company_info = db.get_user_company_details( session_user, client_id)
	unit_ids = user_company_info[0]
	division_ids = user_company_info[1]
	legal_entity_ids = user_company_info[2]
	business_group_ids = user_company_info[3]
	country_list = db.get_countries_for_user(session_user, client_id)
	domain_list = db.get_domains_for_user(session_user, client_id)
	business_group_list = db.get_business_groups_for_user(business_group_ids, client_id)
	legal_entity_list = db.get_legal_entities_for_user(legal_entity_ids, client_id)
	division_list =  db.get_divisions_for_user(division_ids, client_id)
	unit_list = db.get_units_for_user(unit_ids, client_id)
	users_list = db.get_client_users(client_id);
	return clientreport.GetClientReportFiltersSuccess(
		countries = country_list, domains = domain_list, business_groups = business_group_list, legal_entities = legal_entity_list, divisions = division_list, units = unit_list, users = users_list)

def get_unitwise_compliance(db, request, session_user, client_id):
	country_id = request.country_id
	domain_id = request.domain_id
	business_group_id = request.business_group_id
	legal_entity_id = request.division_id
	division_id = request.division_id
	unit_id = request.unit_id
	user_id = request.user_id
	if business_group_id is None :
		business_group_id = '%'
	if legal_entity_id is None :
		legal_entity_id = '%'
	if division_id is None :
		division_id = '%'
	# if unit_id is None :
	# 	unit_id = '%'
	if user_id is None :
		user_id = '%'

	unit_wise_compliances_list = db.get_unitwise_compliance_report(
	    country_id, domain_id, business_group_id, 
	    legal_entity_id, division_id, unit_id, user_id, client_id,session_user
	)
	return clientreport.GetUnitwisecomplianceReportSuccess(unit_wise_compliances_list)


	

	