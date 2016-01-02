from protocol import login, core, knowledgemaster
from general import validate_user_session

__all__=[
	"process_knowledge_master_request",
]

def process_knowledge_master_request(request, db) :
	session_token = request.session_token
    request_frame = request.request
    user_id = validate_user_session(db, session_token)
    if user_id is None:
        return login.InvalidSessionToken()

    if type(request_frame) is knowledgemaster.GetGeographyLevels:
        pass

    if type(request_frame) is knowledgemaster.SaveGeographyLevel:
        pass

    if type(request_frame) is knowledgemaster.GetGeographies:
        pass

    if type(request_frame) is knowledgemaster.SaveGeography:
        pass

    if type(request_frame) is knowledgemaster.UpdateGeography:
        pass

    if type(request_frame) is knowledgemaster.ChangeGeographyStatus:
        pass

    if type(request_frame) is knowledgemaster.GetIndustries:
    	pass

    if type(request_frame) is knowledgemaster.SaveIndustry:
    	pass

    if type(request_frame) is knowledgemaster.UpdateIndustry:
    	pass

    if type(request_frame) is knowledgemaster.ChangeIndustryStatus:
    	pass

    if type(request_frame) is knowledgemaster.GetStatutoryNatures:
    	pass

    if type(request_frame) is knowledgemaster.SaveStatutoryNature:
    	pass

    if type(request_frame) is knowledgemaster.UpdateStatutoryNature:
    	pass

    if type(request_frame) is knowledgemaster.ChangeStatutoryNatureStatus :
    	pass

    if type(request_frame) is knowledgemaster.GetStatutoryLevels:
    	pass

    if type(request_frame) is knowledgemaster.SaveStatutoryLevel:
    	pass

	if type(request_frame) is knowledgemaster.SaveStatutory:
		pass 



