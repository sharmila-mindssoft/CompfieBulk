from ..buapiprotocol import bustatutorymappingprotocol as bu_sm
from ..budatabase.bustatutorymappingdb import *
__all__ = [
    "process_bu_statutory_mapping_request"
]

def process_bu_statutory_mapping_request(request, db, session_user):
    request_frame = request.request

    if type(request_frame) is bu_sm.GetStatutoryMappingCsvUploadedList:
        result = get_statutory_mapping_csv_list(db, request_frame, session_user)

    return result


def get_statutory_mapping_csv_list(db, request_frame, session_user):

    upload_more, csv_data = get_uploaded_statutory_mapping_csv_list(db, session_user)
    result = bu_sm.GetStatutoryMappingCsvUploadedListSuccess(
        upload_more, csv_data
    )
    return result
