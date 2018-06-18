import os
from functools import wraps
from bucontroller.bucompletedtaskcurrentyearcontroller import (
    process_bu_completed_task_current_year_request
)
from buapiprotocol import (
    bucompletedtaskcurrentyearprotocol
)


ROOT_PATH = os.path.join(os.path.split(__file__)[0], "..", "..")

__all__ = [
    "BulkAPI"
]

#
# api_request
#


def bulk_upload_api_request(
    request_data_type, is_group=True, need_category=False
):
    def wrapper(f):
        @wraps(f)
        def wrapped(self):
            return self.handle_bulk_upload_api_request(
                f, request_data_type, is_group, need_category
            )
        return wrapped
    return wrapper


class BulkAPI(object):
    def __init__(self):
        pass

    def bulk_upload_api_urls(self):
        print("bulk_upload_api_urls")
        return [
            ("/api/bu/completed_task", self.handle_completed_task),
        ]

    @bulk_upload_api_request(
        bucompletedtaskcurrentyearprotocol.RequestFormat,
        is_group=False, need_category=True)
    def handle_completed_task(
        self, request, db, session_user, session_category):
        return process_bu_completed_task_current_year_request(
            request, db, session_user)
