from protocol import (clienttransactions, core)

__all__ = [
	"process_client_transaction_requests"
]

def process_client_transaction_requests(request, db) :
	client_info = request.session_token.split("-")
	request = request.request
	client_id = int(client_info[0])
	session_token = client_info[1]
	session_user = db.validate_session_token(client_id, session_token)
	if session_user is None:
		return login.InvalidSessionToken()

	if type(request) is clienttransactions.GetStatutorySettings :
		return process_get_statutory_settings(db, session_user, client_id)

	elif type(request) is clienttransactions.UpdateStatutorySettings :
		return process_update_statutory_settings(db, request, session_user, client_id)

	elif type(request) is clienttransactions.GetAssignCompliancesFormData:
		pass

	elif type(request) is clienttransactions.SaveAssignedCompliance :
		pass

	elif type(request) is clienttransactions.GetUserwiseCompliances :
		pass

	elif type(request) is clienttransactions.ReassignCompliance :
		pass

	elif type(request) is clienttransactions.GetPastRecordsFormData :
		return process_get_past_records_form_data(db, request, session_user, client_id)

def process_get_statutory_settings(db, session_user, client_id):
	return db.get_statutory_settings(session_user, client_id)

def process_update_statutory_settings(db, request, session_user, client_id):
	return db.update_statutory_settings(request, session_user, client_id)

def process_get_past_records_form_data(db, request, session_user, client_id):
	countries = db.get_countries_for_user(session_user, client_id)
	row = db.get_user_company_details(session_user, client_id)
	business_groups = db.get_business_groups_for_user(row[3], client_id)
	legal_entities = db.get_legal_entities_for_user(row[2], client_id)
	divisions = db.get_divisions_for_user(row[1], client_id)
	units = db.get_units_for_user_grouped_by_industry(row[0], client_id)
	domains = db.get_domains_for_user(session_user, client_id)
	level1_statutories = db.get_level_1_statutory(client_id)
	compliance_frequency = db.get_compliance_frequency(client_id)
	return clienttransactions.GetPastRecordsFormDataSuccess(countries = countries, 
		business_groups = business_groups, legal_entities = legal_entities, divisions = divisions,
		units = units, domains = domains, level_1_statutories = level1_statutories,
		compliance_frequency = compliance_frequency)
	 