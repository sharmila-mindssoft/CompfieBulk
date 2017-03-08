import fileprotocol
from filehandler import *

__all__ = [
    "process_file_request"
]

def process_file_based_request(request):
    request = request.request
    if type(request) is fileprotocol.UploadComplianceTaskFile :
        result = process_save_file(request)

    return result

def process_save_file(request):
    pass
