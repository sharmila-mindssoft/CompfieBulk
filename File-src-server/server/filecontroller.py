import fileprotocol
from filehandler import *

__all__ = [
    "process_file_based_request"
]

def process_file_based_request(request):
    request = request.request

    if type(request) is fileprotocol.UploadComplianceTaskFile :
        result = upload_file(request)

    elif type(request) is fileprotocol.RemoveFile :
        result = remove_file(request)

    return result
