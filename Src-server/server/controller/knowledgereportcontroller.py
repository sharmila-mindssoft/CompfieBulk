from protocol import login, core, knowledgereport
from generalcontroller import validate_user_session

__all__ = [
    "process_knowledge_report_request"
]

def process_knowledge_report_request(request, db) :
    session_token = request.session_token
    request_frame = request.request
    user_id = validate_user_session(db, session_token)
    if user_id is None:
        return login.InvalidSessionToken()

    if type(request_frame) is knowledgereport.GetStatutoryMappingReportFilters :
        return process_get_statutory_mapping_filters(db, request_frame, user_id)

    elif type(request_frame) is knowledgereport.GetStatutoryMappingReportData :
        return process_get_statutory_mapping_report_data(db, request_frame, user_id)

    elif type(request_frame) is knowledgereport.GetGeographyReport:
        return process_get_geography_report(db, request_frame, user_id)

def process_get_statutory_mapping_filters(db, request_frame, user_id):
    pass

def process_get_statutory_mapping_report_data(db, request_frame, user_id):
    pass

def process_get_geography_report(db, request_frame, user_id):
    pass



