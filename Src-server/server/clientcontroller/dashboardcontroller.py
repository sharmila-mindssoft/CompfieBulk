from protocol import (dashboard, login, core)

__all__ = [
	"process_client_dashboard_requests"
]

def process_client_dashboard_requests(request, db) :
	session_token = request.session_token
	client_info = session_token.split("-")
	request = request.request
	client_id = int(client_info[0])
	session_user = db.validate_session_token(client_id, session_token)
	if session_user is None:
		return login.InvalidSessionToken()
	if type(request) is dashboard.GetChartFilters :
		return process_get_chart_filters(db, session_user, client_id)
	elif type(request) is dashboard.GetComplianceStatusChart :
		return process_compliance_status_chart(db, request, session_user, client_id)
	elif type(request) is dashboard.GetTrendChart :
		return process_trend_chart(db, request, session_user, client_id)
	

def process_get_chart_filters(db, session_user, client_id):
	countries = db.get_countries_for_user(session_user, client_id)
	domains = db.get_domains_for_user(session_user, client_id)
	business_group_ids = None
	business_groups = db.get_business_groups_for_user(business_group_ids, client_id)
	legal_entity_ids = None
	legal_entities = db.get_legal_entities_for_user(legal_entity_ids, client_id)
	division_ids = None
	divisions = db.get_divisions_for_user(division_ids, client_id)
	units = db.get_units_for_assign_compliance(session_user, client_id)
	return dashboard.GetChartFiltersSuccess(
		countries, domains, business_groups,
		legal_entities, divisions, units
	)

def process_compliance_status_chart(db, request, session_user, client_id):
	return db.get_compliance_status_chart(request, session_user, client_id)

def process_trend_chart(db, request, session_user, client_id):
	trend_chart_info = None
	if request.filter_type == "Group":
		trend_chart_info = db.get_trend_chart(request.country_ids, request.domain_ids,
			client_id)
	else:
		trend_chart_info = db.get_filtered_trend_data(request.country_ids, request.domain_ids,
			request.filter_type, request.filter_ids, client_id)
	years = trend_chart_info[0]
	data = trend_chart_info[1]
	return dashboard.GetTrendChartSuccess(years = years, data = data)