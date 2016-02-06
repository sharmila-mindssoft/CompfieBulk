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
	elif type(request) is clientreport.GetAssigneewisecomplianceReport:
		return get_assigneewise_compliance(db, request, session_user, client_id)
	elif type(request) is clientreport.GetServiceProviderReportFilters:
		return get_serviceprovider_report_filters(db, request, session_user, client_id) 
	elif type(request) is clientreport.GetServiceProviderWiseCompliance:
		return get_serviceproviderwise_compliance(db, request, session_user, client_id)
	elif type(request) is clientreport.GetComplianceDetailsReportFilters:
		return get_compliancedetails_report_filters(db, request, session_user, client_id) 
	elif type(request) is clientreport.GetComplianceDetailsReport:
		return get_compliancedetails_report(db, request, session_user, client_id)
	elif type(request) is clientreport.GetStatutoryNotificationsListFilters:
		return get_statutory_notifications_list_filters(db, request, session_user, client_id) 
	elif type(request) is clientreport.GetStatutoryNotificationsListReport:
		return get_statutory_notifications_list_report(db, request, session_user, client_id)
	elif type(request) is clientreport.GetRiskReportFilters:
		return get_risk_report_filters(db, request, session_user, client_id) 
	elif type(request) is clientreport.GetRiskReport:
		return get_risk_report(db, request, session_user, client_id)


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
	if user_id is None :
		user_id = '%'

	unit_wise_compliances_list = db.get_unitwise_compliance_report(
	    country_id, domain_id, business_group_id, 
	    legal_entity_id, division_id, unit_id, user_id, client_id,session_user
	)
	return clientreport.GetUnitwisecomplianceReportSuccess(unit_wise_compliances_list)


def get_assigneewise_compliance(db, request, session_user, client_id):
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
	if user_id is None :
		user_id = '%'

	assignee_wise_compliances_list = db.get_assigneewise_compliance_report(
	    country_id, domain_id, business_group_id, 
	    legal_entity_id, division_id, unit_id, user_id, client_id,session_user
	)
	return clientreport.GetAssigneewisecomplianceReportSuccess(assignee_wise_compliances_list)


def get_serviceprovider_report_filters(db, request, session_user, client_id):
	user_company_info = db.get_user_company_details( session_user, client_id)
	unit_ids = user_company_info[0]
	country_list = db.get_countries_for_user(session_user, client_id)
	domain_list = db.get_domains_for_user(session_user, client_id)
	unit_list = db.get_units_for_user(unit_ids, client_id)
	level_1_statutories_list = db.get_client_level_1_statutoy(session_user, client_id)
	service_providers_list = db.get_service_providers(client_id)

	return clientreport.GetServiceProviderReportFiltersSuccess(
		countries = country_list, domains = domain_list, level_1_statutories = level_1_statutories_list, units = unit_list, service_providers = service_providers_list)

def get_serviceproviderwise_compliance(db, request, session_user, client_id):
	country_id = request.country_id
	domain_id = request.domain_id
	statutory_id = request.statutory_id
	unit_id = request.unit_id
	service_provider_id = request.service_provider_id
	
	if service_provider_id is None :
		service_provider_id = '%'

	serviceprovider_wise_compliances_list = db.get_serviceproviderwise_compliance_report(
	    country_id, domain_id, statutory_id, unit_id, service_provider_id, client_id,session_user
	)
	return clientreport.GetServiceProviderWiseComplianceSuccess(serviceprovider_wise_compliances_list)

def get_compliancedetails_report_filters(db, request, session_user, client_id):
	user_company_info = db.get_user_company_details( session_user, client_id)
	unit_ids = user_company_info[0]
	country_list = db.get_countries_for_user(session_user, client_id)
	domain_list = db.get_domains_for_user(session_user, client_id)
	unit_list = db.get_units_for_user(unit_ids, client_id)
	level_1_statutories_list = db.get_client_level_1_statutoy(session_user, client_id)
	compliances_list = db.get_client_compliances(session_user, client_id);
	users_list = db.get_client_users(client_id);

	return clientreport.GetComplianceDetailsReportFiltersSuccess(
		countries = country_list, domains = domain_list, level_1_statutories = level_1_statutories_list, units = unit_list, Compliances = compliances_list, users = users_list)

def get_statutory_notifications_list_filters(db, request, session_user, client_id):
	user_company_info = db.get_user_company_details( session_user, client_id)
	unit_ids = user_company_info[0]
	country_list = db.get_countries_for_user(session_user, client_id)
	domain_list = db.get_domains_for_user(session_user, client_id)
	business_group_list = db.get_business_groups_for_user(session_user, client_id)
	legal_entity_list = db.get_legal_entities_for_user(session_user, client_id)
	division_list = db.get_divisions_for_user(session_user, client_id)
	unit_list = db.get_units_for_user(unit_ids, client_id)
	level_1_statutories_list = db.get_client_level_1_statutoy(session_user, client_id)
	users_list = db.get_client_users(client_id);

	return clientreport.GetStatutoryNotificationsListFiltersSuccess	(countries = country_list, domains = domain_list, 
		business_groups = business_group_list, legal_entities = legal_entity_list, divisions = division_list, units = unit_list,
		level_1_statutories = level_1_statutories_list, users = users_list)

def get_statutory_notifications_list_report(db, request, session_user, client_id):
	result = db.get_statutory_notifications_list_report(request, client_id)
	return clientreport.GetStatutoryNotificationsListReportSuccess(result)



def get_compliancedetails_report(db, request, session_user, client_id):
	country_id = request.country_id
	domain_id = request.domain_id
	statutory_id = request.statutory_id
	unit_id = request.unit_id
	compliance_id = request.compliance_id
	assignee_id = request.assignee_id
	from_date = request.from_date
	to_date = request.to_date
	
	
	if compliance_id is None :
		compliance_id = '%'
	if assignee_id is None :
		assignee_id = '%'
	if request.compliance_status is None :
		compliance_status = '%'
	else :
		compliance_status = core.COMPLIANCE_STATUS(request.compliance_status)


	compliance_details_list = db.get_compliance_details_report(
	    country_id, domain_id, statutory_id, unit_id, compliance_id, assignee_id, from_date, to_date, compliance_status, client_id,session_user
	)
	return clientreport.GetComplianceDetailsReportSuccess(compliance_details_list)

def get_risk_report_filters(db, request, session_user, client_id):
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
	level_1_statutories_list = db.get_client_level_1_statutoy(session_user, client_id)
	return clientreport.GetRiskReportFiltersSuccess(
		countries = country_list, domains = domain_list, business_groups = business_group_list, legal_entities = legal_entity_list, divisions = division_list, units = unit_list, level1_statutories = level_1_statutories_list)

def get_risk_report(db, request, session_user, client_id):
	country_id = request.country_id
	domain_id = request.domain_id
	business_group_id = request.business_group_id
	legal_entity_id = request.division_id
	division_id = request.division_id
	unit_id = request.unit_id
	statutory_id = request.statutory_id
	statutory_status = request.statutory_status

	if business_group_id is None :
		business_group_id = '%'
	if legal_entity_id is None :
		legal_entity_id = '%'
	if division_id is None :
		division_id = '%'
	if statutory_id is None :
		statutory_id = '%'
	if statutory_status is None :
		statutory_status = '%'

	risk_report_list = db.get_risk_report(
	    country_id, domain_id, business_group_id, 
	    legal_entity_id, division_id, unit_id, statutory_id, statutory_status, client_id,session_user
	)
	return clientreport.GetRiskReportSuccess(risk_report_list,risk_report_list,risk_report_list)


	

	