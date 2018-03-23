import traceback
from ..bucsvvalidation.completedtaskcurrentyearvalidation import (
    ValidateCompletedTaskCurrentYearCsvData
)

from..buapiprotocol import bucompletedtaskcurrentyearprotocol as bu_ct
from..budatabase.bucompletedtaskcurrentyeardb import *
from ..client_bulkuploadcommon import (
    convert_base64_to_file,
    read_data_from_csv,
    generate_valid_file
)
from ..client_bulkexport import ConvertJsonToCSV
import datetime
from server.constants import BULKUPLOAD_CSV_PATH
from server.exceptionmessage import fetch_error

__all__ = [
    "process_bu_completed_task_current_year_request"
]
########################################################
'''
    Process all completed task current year request here
    :param
        request: api Request class object
        db: database object
        session_user: logged in user details
    :type
        request: Object
        db: Object
        session_user: Object
    :returns
        result: returns processed api response class Object
    rtype:
        result: Object
'''
########################################################
def process_bu_completed_task_current_year_request(request, db, session_user):
    request_frame = request.request

    if type(request_frame) is bu_ct.UploadCompletedTaskCurrentYearCSV:
        result = upload_completed_task_current_year_csv(db, request_frame, session_user)

########################################################

def upload_completed_task_current_year_csv(db, request_frame, session_user):

    if request_frame.csv_size > 0 :
        pass
    # save csv file
    csv_name = convert_base64_to_file(
            BULKUPLOAD_CSV_PATH, request_frame.csv_name,
            request_frame.csv_data
        )
    # read data from csv file
    header, completed_task_data = read_data_from_csv(csv_name)

    # csv data validation
    cObj = ValidateCompletedTaskCurrentYearCsvData(
        db, completed_task_data, session_user, request_frame.csv_name, header, 1
    )
    res_data = cObj.perform_validation()

    if res_data["return_status"] is True :

        d_ids = ",".join(str(e) for e in request_frame.d_ids)
        d_names = ",".join(str(e) for e in request_frame.d_names)

        csv_args = [
            session_user.user_id(),
            request_frame.cl_id, request_frame.le_id,
            d_ids, request_frame.le_name, d_names,
            csv_name,
            res_data["total"]
        ]
        new_csv_id = save_completed_task_current_year_csv(db, csv_args)
        if new_csv_id :
            if save_completed_task_data(db, new_csv_id, res_data["data"]) is True :
                result = bu_ct.UploadCompletedTaskCurrentYearCSVSuccess(
                    res_data["total"], res_data["valid"], res_data["invalid"]
                )

        # csv data save to temp db
    else :
        result = bu_ct.UploadCompletedTaskCurrentYearCSVFailed(
            res_data["invalid_file"], res_data["mandatory_error"],
            res_data["max_length_error"], res_data["duplicate_error"],
            res_data["invalid_char_error"], res_data["invalid_data_error"],
            res_data["inactive_error"], res_data["total"], res_data["invalid"]
        )

    return result