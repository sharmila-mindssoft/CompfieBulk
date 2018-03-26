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
    print "Inside controller>>>"

    if type(request_frame) is bu_ct.UploadCompletedTaskCurrentYearCSV:
        result = upload_completed_task_current_year_csv(db, request_frame, session_user)

    return result

########################################################

def upload_completed_task_current_year_csv(db, request_frame, session_user):

    print "inside bucompletedtaskcurrentyearcontroller>>>>upload_completed_task_current_year_csv "
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
        db, completed_task_data, session_user, request_frame.csv_name, header)
    res_data = cObj.perform_validation()

    if res_data["return_status"] is True :

        # d_ids = ",".join(str(e) for e in request_frame.d_ids)
        # d_names = ",".join(str(e) for e in request_frame.d_names)
        # session_user.user_id(),
        # print "request_frame>>>", request_frame
        # request_frame.le_id,

        # csv_args = [
        #     cObj._legal_entity_names, cObj._Domains,
        #     cObj._Unit_Codes, cObj._Unit_Names, cObj._Primary_Legislations,
        #     cObj._Secondary_Legislations, cObj._Compliance_Tasks,
        #     cObj._Compliance_Descriptions, cObj._Compliance_Frequencys,
        #     cObj._Statutory_Dates, cObj._Due_Dates, cObj._Assignees,
        #     cObj._Completion_Dates, cObj._Document_Names, csv_name,
        #     res_data["total"]
        # ]
        #  "csv_past_id", "client_id", "legal_entity_id", "domain_id",
        # "unit_id_id", "client_group", "csv_name",
        # "uploaded_by", "uploaded_on",
        # "total_records", "total_documents", "uploaded_documents", "upload_status"

        csv_args = [
            "1","1","1","1","1", csv_name, "1","", res_data["total"],"0","0"
        ]
        new_csv_id = save_completed_task_current_year_csv(db, csv_args, session_user)
        if new_csv_id :
            if save_completed_task_data(db, new_csv_id, res_data["data"]) is True :
                result = bu_ct.UploadCompletedTaskCurrentYearCSVSuccess(
                    res_data["total"], res_data["valid"], res_data["invalid"]
                )

        # csv data save to temp db
    else:
        print "res_data[invalid_file]>>", res_data["invalid_file"]
        print "res_data[mandatory_error]", res_data["mandatory_error"]
        print "res_data[max_length_error]", res_data["max_length_error"]
        print "res_data[duplicate_error]", res_data["duplicate_error"]
        print "res_data[invalid_char_error]", res_data["invalid_char_error"]
        print "res_data[invalid_data_error]", res_data["invalid_data_error"]
        print "res_data[inactive_error]", res_data["inactive_error"]
        # print "res_data[total]", res_data[total]
        # print"res_data[invalid]", res_data[invalid]
        #  res_data["total"]
        # res_data["invalid"]

        result = bu_ct.UploadCompletedTaskCurrentYearCSVFailed(
            res_data["invalid_file"], res_data["mandatory_error"],
            res_data["max_length_error"], res_data["duplicate_error"],
            res_data["invalid_char_error"], res_data["invalid_data_error"],
            res_data["inactive_error"]
        )
        print "result>>>", result

    return result
