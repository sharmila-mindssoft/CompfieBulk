from protocol import login, core, knowledgetransaction
from generalcontroller import validate_user_session

__all__ = [
	"process_knowledge_transaction_request"
]

def process_knowledge_transaction_request(request, db) :
	session_token = request.session_token
    request_frame = request.request
    user_id = validate_user_session(db, session_token)
    if user_id is None:
        return login.InvalidSessionToken()

    if type(request_frame) is knowledgetransaction.GetStatutoryMappings :
		return process_get_statutory_mappings(db, user_id)

	elif type(request_frame) is knowledgetransaction.SaveStatutoryMapping :
		return process_save_statutory_mapping(db, request_frame, user_id)

	elif type(request_frame) is knowledgetransaction.UpdateStatutoryMapping :
		return process_update_statutory_mapping(db, request_frame, user_id)

	elif type(request_frame) is knowledgetransaction.ChangeStatutoryMappingStatus :
		return process_change_statutory_mapping_status(db, request_frame, user_id)

	elif type(request_frame) is knowledgetransaction.ApproveStatutoryMapping :
		return process_approve_statutory_mapping(db, request_frame, user_id)

def process_get_statutory_mappings(db, user_id):
	countries = db.get_countries_for_user(user_id)
	domains = db.get_domains_for_user(user_id)
	industries = db.get_industries()
	statutory_natures = db.get_statutory_nature()
	statutory_levels = db.get_statutory_levels()
	geography_levels = db.get_get_geography_levels()
	geographies = db.get_geographies()
	compliance_frequency = db.get_compliance_frequency()
	compliance_repeat_type = db.get_compliance_repeat()
	compliance_duration_type = db.get_compliance_duration()
	compliance_approval_status = db.get_approval_status()
	statutory_mappings = db.get_statutory_mappings(user_id)
	return knowledgetransaction.GetStatutoryMappingsSuccess(
		countries, domains, industries, statutory_natures, 
		statutory_levels, geography_levels, geographies,
		compliance_frequency, compliance_repeat_type,
		compliance_duration_type, compliance_approval_status,
		statutory_mappings
	)

def process_save_statutory_mapping(db, request_frame, user_id):
	if (db.save_statutory_mapping(request_frame, user_id)):
		return knowledgetransaction.SaveStatutoryMappingSuccess()

def process_update_statutory_mapping(db, request_frame, user_id):
	if (db.update_statutory_mapping(request_frame, user_id)):
		return knowledgetransaction.UpdateStatutoryMappingSuccess()
	else :
		return knowledgetransaction.InvalidStatutoryMappingId()

def process_change_statutory_mapping_status(db, request_frame, user_id):	
	if (db.change_statutory_mapping_status(request_frame, user_id)) :
		return knowledgetransaction.ChangeStatutoryMappingStatusSuccess()
	else :	
		return knowledgetransaction.InvalidStatutoryMappingId()
	
def process_approve_statutory_mapping(db, request_frame, user_id):
	is_approved = False
	for data in request_frame :
		if (db.change_approval_status(data, user_id)):
			is_approved = True
		else :
			is_approved = False
			break

	if is_approved :
		return knowledgetransaction.ApproveStatutoryMappingSuccess()
	else :	
		return knowledgetransaction.InvalidStatutoryMappingId()
	

