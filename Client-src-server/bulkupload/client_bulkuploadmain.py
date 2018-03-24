import os
from functools import wraps
from buapiprotocol import (
    bucompletedtaskcurrentyearprotocol
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
        print("bulk_upload_api_urls")
        return [
            ("/api/bu/completed_task", api.handle_completed_task),
        ]

    @api_request(bucompletedtaskcurrentyearprotocol.RequestFormat, need_session_id=True)
    def handle_completed_task(self, request, db, session_user):
        return bucontroller.process_bu_completed_task_current_year_request(request, db, session_user)
