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
		return process_get_assign_compliance_form_data(db, session_user, client_id)

	elif type(request) is clienttransactions.GetComplianceForUnits:
		return process_get_compliance_for_units(db, request, session_user, client_id)

	elif type(request) is clienttransactions.SaveAssignedCompliance :
		return process_save_assigned_compliance(db, request, session_user, client_id)

	elif type(request) is clienttransactions.GetUserwiseCompliances :
		pass

	elif type(request) is clienttransactions.ReassignCompliance :
		pass

def process_get_statutory_settings(db, session_user, client_id):
	return db.get_statutory_settings(session_user, client_id)

def process_update_statutory_settings(db, request, session_user, client_id):
	return db.update_statutory_settings(request, session_user, client_id)

def process_get_assign_compliance_form_data(db, session_user, client_id):
	countries = db.get_countries_for_user(session_user, client_id)
	business_group_ids = None
	business_groups = db.get_business_groups_for_user(business_group_ids, client_id)
	legal_entity_ids = None
	legal_entities = db.get_legal_entities_for_user(legal_entity_ids, client_id)
	division_ids = None
	divisions = db.get_divisions_for_user(division_ids, client_id)
	units = db.get_units_for_assign_compliance(session_user, client_id)
	users = db.get_users_for_seating_units(session_user, client_id)
	return clienttransactions.GetAssignCompliancesFormDataSuccess(
		countries, business_groups, legal_entities,
		divisions, units, users
	)

def process_get_compliance_for_units(db, request, session_user, client_id):
	unit_ids = request.unit_ids
	statutories = db.get_assign_compliance_statutories_for_units(unit_ids, session_user, client_id)
	return clienttransactions.GetComplianceForUnitsSuccess(statutories)

def process_save_assigned_compliance(db, request, session_user, client_id):
	return 	db.save_assigned_compliance(request, session_user, client_id)