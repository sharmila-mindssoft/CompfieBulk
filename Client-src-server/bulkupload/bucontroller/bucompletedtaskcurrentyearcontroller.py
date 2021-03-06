from ..bucsvvalidation.completedtaskcurrentyearvalidation import (
    ValidateCompletedTaskCurrentYearCsvData,
    ValidateCompletedTaskForSubmit, SourceDB
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
from bulkupload.client_bulkconstants import BULKUPLOAD_CSV_PATH
from server.exceptionmessage import fetch_error

from server.common import (
    get_date_time_in_date, datetime_to_string_time, get_current_date, datetime_to_string
)

from ..buapiprotocol.pastdatadownloadbulk import PastDataJsonToCSV


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
    if type(request_frame) is bu_ct.GetCompletedTaskCsvUploadedList:
        result = get_completed_task_csv_list(db, request_frame, session_user)

    if type(request_frame) is bu_ct.UploadCompletedTaskCurrentYearCSV:
        result = upload_completed_task_current_year_csv(db, request_frame, session_user)

    if type(request_frame) is bu_ct.saveBulkRecords:
        result = process_saveBulkRecords(
            db, request_frame, session_user, request.session_token
        )

    if type(request_frame) is bu_ct.GetDownloadData:
        result = process_get_bulk_download_data(
            db, request_frame, session_user
        )

    return result

########################################################


def get_completed_task_csv_list(db, request_frame, session_user):

    csv_data = getCompletedTaskCSVList(
        db, session_user, request_frame.legal_entity_list
    )
    # print "csv_data>>", csv_data
    result = bu_ct.GetCompletedTaskCsvUploadedListSuccess(csv_data)
    return result

########################################################

def upload_completed_task_current_year_csv(db, request_frame, session_user):

    if request_frame.csv_size > 0:
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
    # print "request_frame.legal_entity_id>>", request_frame.legal_entity_id
    res_data = cObj.perform_validation(request_frame.legal_entity_id)

    if res_data is False:
        return bu_ct.InvalidCsvFile()
    elif res_data["return_status"] is True:
        current_date_time = get_date_time_in_date()
        str_current_date_time = datetime_to_string(current_date_time)
        unit_id = res_data["unit_id"]
        domain_id = res_data["domain_id"]
        client_id, client_group_name = get_client_id_by_le(
            db, request_frame.legal_entity_id
        )
        csv_args = [
            client_id, request_frame.legal_entity_id, domain_id,
            unit_id, client_group_name, csv_name, session_user,
            str_current_date_time, res_data["total"],
            res_data["doc_count"], "0", "0"
        ]

        new_csv_id = save_completed_task_current_year_csv(
            db, csv_args, session_user
        )
        if new_csv_id:
            if save_completed_task_data(
                    db, new_csv_id, res_data["data"], client_id
                    ) is True:
                    result = bu_ct.UploadCompletedTaskCurrentYearCSVSuccess(
                        res_data["total"], res_data["valid"],
                        res_data["invalid"],
                        new_csv_id, csv_name, res_data["doc_count"],
                        res_data["doc_names"], unit_id, domain_id
                    )
        # csv data save to temp db
    else:
        result = bu_ct.UploadCompletedTaskCurrentYearCSVFailed(
            res_data["invalid_file"], res_data["mandatory_error"],
            res_data["max_length_error"], res_data["duplicate_error"],
            res_data["invalid_char_error"], res_data["invalid_data_error"],
            res_data["inactive_error"], res_data["total"], res_data["invalid"],
            res_data["invalid_file_format"], res_data["invalid_date"]
        )

    return result


def process_saveBulkRecords(db, request_frame, session_user, session_token):
    print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!", session_token
    csv_id = request_frame.new_csv_id
    country_id = request_frame.country_id
    legal_id = request_frame.legal_entity_id
    domain_id = request_frame.domain_id
    unit_id = request_frame.unit_id
    dataResult = getPastRecordData(db, csv_id)
    cObj = ValidateCompletedTaskForSubmit(
        db, csv_id, dataResult, session_user)

    if cObj._doc_count > 0:
        cObj.document_download_process_initiate(
            csv_id, country_id, legal_id, domain_id, unit_id, session_token
        )

    if cObj.frame_data_for_main_db_insert(
        db, dataResult, request_frame.legal_entity_id, session_user
    ) is True:
        result = bu_ct.saveBulkRecordSuccess()
    else:
        result = []

    return result


########################################################
# To get the compliances under the selected filters
# Completed Task - Current Year BULK (Past Data)
########################################################


def process_get_bulk_download_data(
        db, request_frame, session_user
):
    # print "Process get Bulk download"
    # print "request_frame>> ", request_frame
    # print "leid->>>> ", request_frame.legal_entity_id
    converter = PastDataJsonToCSV(
                db, request_frame, session_user, "DownloadPastData"
            )
    if converter.FILE_DOWNLOAD_PATH is None:
            return bu_ct.ExportToCSVEmpty()
    else:
        result = bu_ct.DownloadBulkPastDataSuccess(
                 converter.FILE_DOWNLOAD_PATH)
    return result
