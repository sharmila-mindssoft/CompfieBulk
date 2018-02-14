import os
from functools import wraps
from buapiprotocol import ( 
    bustatutorymappingprotocol, buassignstatutoryprotocol, buclientunitsprotocol
    )
import bucontroller
# from server.main import api_request

ROOT_PATH = os.path.join(os.path.split(__file__)[0], "..", "..")

__all__ = [
    "BulkAPI"
]

#
# api_request
#
def api_request(request_data_type, need_session_id=False):
    def wrapper(f):
        @wraps(f)
        def wrapped(self):
            return self.handle_api_request(f, request_data_type, need_session_id)
        return wrapped
    return wrapper


class BulkAPI(object):
    def __init__(self):
        pass

    def bulk_upload_api_urls(self):
        return [
            ("/knowledge/api/bu/statutory_mapping", self.handle_statutory_mapping),
            ("/knowledge/api/assign_statutory", self.handle_assign_statutory),
            ("/knowledge/api/bu/client_units", self.handle_client_units),
        ]

    @api_request(bustatutorymappingprotocol.RequestFormat, need_session_id=True)
    def handle_statutory_mapping(self, request, db, session_user):
        return bucontroller.process_bu_statutory_mapping_request(request, db, session_user)

    @api_request(buassignstatutoryprotocol.RequestFormat, need_session_id=True)
    def handle_assign_statutory(self, request, db, session_user):
        return bucontroller.process_bu_assign_statutory_request(request, db, session_user)

    @api_request(buclientunitsprotocol.RequestFormat, need_session_id=True)
    def handle_client_units(self, request, db, session_user):
        return bucontroller.process_bu_client_units_request(request, db, session_user)
