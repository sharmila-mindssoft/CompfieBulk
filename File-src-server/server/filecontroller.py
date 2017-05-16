import fileprotocol
from filehandler import *

__all__ = [
    "process_file_based_request",
]

def process_file_based_request(request):
    session = request.session_token
    request = request.request

    client_id = session.split('-')[0]
    print client_id
    if type(request) is fileprotocol.UploadComplianceTaskFile :
        result = upload_file(request, client_id)

    elif type(request) is fileprotocol.RemoveFile :
        result = remove_file(request, client_id)

    elif type(request) is fileprotocol.DownloadFile :
        result = download_file(request, client_id)

    elif type(request) is fileprotocol.FormulateDownload :
        result = process_contract_download(request, client_id)

    return result


