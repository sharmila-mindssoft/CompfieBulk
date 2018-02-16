# from ..bucsvvalidation.assignstatutoryvalidation import *
from server.jsontocsvconverter import ConvertJsonToCSV
from ..buapiprotocol import buassignstatutoryprotocol as bu_as
from ..budatabase.buassignstatutorydb import *
from ..bulkuploadcommon import (
    convert_base64_to_file,
    read_data_from_csv
)

from server.constants import BULKUPLOAD_CSV_PATH
__all__ = [
    "process_bu_assign_statutory_request"
]
########################################################
'''
    Process all assign statutory request here
    :param
        request: api Request class object
        db: database object
        session_user: logged in user id
    :type
        request: Object
        db: Object
        session_user: String
    :returns
        result: returns processed api response class Object
    rtype:
        result: Object
'''
########################################################
def process_bu_assign_statutory_request(request, db, session_user):
    request_frame = request.request
    
    if type(request_frame) is bu_as.GetClientInfo:
        result = get_client_info(db, request_frame, session_user)

    if type(request_frame) is bu_as.DownloadAssignStatutory:
        result = get_download_assing_statutory(db, request_frame, session_user)

    return result

########################################################
'''
    returns statutory mapping uploaded csv list
    :param
        db: database object
        request_frame: api request GetStatutoryMappingCsvUploadedList class object
        session_user: logged in user id
    :type
        db: Object
        request_frame: Object
        session_user: String
    :returns
        result: returns processed api response GetStatutoryMappingCsvUploadedListSuccess class Object
    rtype:
        result: Object
'''
########################################################

def get_client_info(db, request_frame, session_user):

    clients_data, entitys_data, units_data = get_client_list(db, session_user)
    result = bu_as.GetClientInfoSuccess(
        clients_data, entitys_data, units_data
    )
    return result

def get_download_assing_statutory(db, request_frame, session_user):

    cl_id = request_frame.cl_id
    le_id = request_frame.le_id
    d_ids = request_frame.d_ids
    u_ids = request_frame.u_ids

    res = get_download_assing_statutory_list(db, cl_id, le_id, d_ids, u_ids, session_user)

    if len(res) > 0:
        converter = ConvertJsonToCSV(
                db, request_frame, session_user, "DownloadAssignStatutory"
            )

        print '$$$$$$$$$$$$$$$$$$$$$$$$$$$'
        print converter.FILE_DOWNLOAD_PATH
        return bu_as.DownloadAssignStatutorySuccess(
            download_file=converter.FILE_DOWNLOAD_PATH
        )

    