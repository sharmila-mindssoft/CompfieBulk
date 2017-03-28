from clientprotocol import clientmobile
from server.clientdatabase.mobile import *

__all__ = [
    "process_client_mobile_request"
]


def process_client_mobile_request(request, db):
    request_frame = request.request
