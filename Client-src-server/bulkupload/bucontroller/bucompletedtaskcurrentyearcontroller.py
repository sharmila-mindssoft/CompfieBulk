import os
import threading
import json
from ..buapiprotocol.pastdatadownloadbulk import PastDataJsonToCSV
from server.common import (
    get_date_time_in_date,
    datetime_to_string_time)
from bulkupload.client_bulkconstants import (
    BULKUPLOAD_CSV_PATH, CSV_MAX_LINE_ITEM,
    BULKUPLOAD_INVALID_PATH, csv_headers)
from ..client_bulkuploadcommon import (
    convert_base64_to_file, save_file_in_client_docs,
    read_data_from_csv, remove_uploaded_file)
from ..bucsvvalidation.completedtaskcurrentyearvalidation import (
    ValidateCompletedTaskCurrentYearCsvData,
    ValidateCompletedTaskForSubmit)
from..buapiprotocol import bucompletedtaskcurrentyearprotocol as bu_ct
from..budatabase.bucompletedtaskcurrentyeardb import (
    get_units_for_user, get_completed_task_csv_list_from_db,
    get_client_id_by_le,
    save_completed_task_current_year_csv, save_completed_task_data,
    get_past_record_data,
    get_files_as_zip, update_document_count,
    get_current_doc_data_submit_status
)


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


def process_bu_completed_task_current_year_request(
        request, db, session_user):
    request_frame = request.request
    result = None
    if type(request_frame) is bu_ct.GetCompletedTaskCsvUploadedList:
        result = get_completed_task_csv_list(db, request_frame, session_user)

    if type(request_frame) is bu_ct.UploadCompletedTaskCurrentYearCSV:
        result = upload_completed_task_current_year_csv(
            db, request_frame, session_user
        )

    if type(request_frame) is bu_ct.SaveBulkRecords:
        result = process_save_bulk_records(
            db, request_frame, session_user, request.session_token
        )

    if type(request_frame) is bu_ct.GetDownloadData:
        result = process_get_bulk_download_data(
            db, request_frame, session_user
        )

    if type(request_frame) is bu_ct.GetUnits:
        result = process_get_units(
            db, request_frame, session_user
        )

    if type(request_frame) is bu_ct.DownloadUploadedData:
        result = process_download_uploaded_data(
            request_frame
        )

    if type(request_frame) is bu_ct.UpdateDocumentCount:
        result = process_update_document_count(
            db, request_frame
        )

    if type(request_frame) is bu_ct.GetStatus:
        result = process_get_status(db, request_frame)

    if type(request_frame) is bu_ct.ProcessQueuedTasks:
        result = process_queued_tasks(
            db, request_frame, session_user, request.session_token
        )

    return result


def process_get_units(
    db, request, session_user
):
    le_id = request.legal_entity_id
    domain_id = request.domain_id
    user_units = get_units_for_user(le_id, domain_id, session_user)

    return bu_ct.GetUnitsSuccess(user_units=user_units)


def get_completed_task_csv_list(db, request_frame, session_user):
    csv_data = get_completed_task_csv_list_from_db(
        db, session_user, request_frame.legal_entity_list
    )
    result = bu_ct.GetCompletedTaskCsvUploadedListSuccess(csv_data)
    return result


def validate_data(db, request_frame, c_obj, session_user, csv_name):
    res_data = c_obj.perform_validation(request_frame.legal_entity_id)
    res_data = c_obj.res_data
    return_data = None
    if res_data is False:
        return_data = bu_ct.InvalidCsvFile().to_structure()
    # elif c_obj.check_if_already_saved_compliance(
    #         request_frame.legal_entity_id) is False:
    #     return_data = bu_ct.DataAlreadyExists().to_structure()
    elif res_data["return_status"] is True:
        current_date_time = get_date_time_in_date()
        str_current_date_time = datetime_to_string_time(current_date_time)
        unit_id = res_data["unit_id"]
        domain_id = res_data["domain_id"]
        client_id, client_group_name = get_client_id_by_le(
            request_frame.legal_entity_id)
        csv_args = [
            client_id, request_frame.legal_entity_id, domain_id,
            unit_id, client_group_name, csv_name, session_user,
            str_current_date_time, res_data["total"],
            res_data["doc_count"], "0", "0"
        ]
        new_csv_id = save_completed_task_current_year_csv(
            db, csv_args
        )
        if new_csv_id:
            if save_completed_task_data(
                db, new_csv_id, res_data["data"]
            ):
                save_file_in_client_docs(csv_name, request_frame.csv_data)
        return_data = bu_ct.UploadCompletedTaskCurrentYearCSVSuccess(
            res_data["total"], res_data["valid"],
            res_data["invalid"],
            new_csv_id, csv_name, res_data["doc_count"],
            res_data["doc_names"], unit_id, domain_id
        ).to_structure()
    else:
        return_data = bu_ct.UploadCompletedTaskCurrentYearCSVFailed(
            res_data["invalid_file"], res_data["mandatory_error"],
            res_data["max_length_error"], res_data["duplicate_error"],
            res_data["invalid_char_error"], res_data["invalid_data_error"],
            res_data["inactive_error"], res_data["total"], res_data["invalid"],
            res_data["invalid_file_format"], res_data["invalid_date"]
        ).to_structure()
    return_data = json.dumps(return_data)

    file_string = csv_name.split(".")
    file_name = "%s_%s.%s" % (
        file_string[0], "result", "txt"
    )
    file_path = "%s/%s" % (BULKUPLOAD_INVALID_PATH, file_name)
    with open(file_path, "wb") as fn:
        fn.write(return_data)
    return


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
    if csv_headers != header:
        return bu_ct.InvalidCsvFile()
    if len(completed_task_data) > CSV_MAX_LINE_ITEM:
        file_path = "%s/csv/%s" % (BULKUPLOAD_CSV_PATH, csv_name)
        remove_uploaded_file(file_path)
        return bu_ct.CsvFileExeededMaxLines(CSV_MAX_LINE_ITEM)
    # csv data validation
    c_obj = ValidateCompletedTaskCurrentYearCsvData(
        db, completed_task_data, session_user,
        request_frame.csv_name, header)
    t = threading.Thread(
        target=validate_data,
        args=(db, request_frame, c_obj, session_user, csv_name))
    t.start()
    return bu_ct.Done(csv_name)


def process_save_bulk_records(db, request_frame, session_user, session_token):
    csv_id = request_frame.new_csv_id
    country_id = request_frame.country_id
    legal_id = request_frame.legal_entity_id
    domain_id = request_frame.domain_id
    unit_id = request_frame.unit_id
    data_result = get_past_record_data(db, csv_id)
    c_obj = ValidateCompletedTaskForSubmit(
        db, csv_id, data_result, session_user)
    if c_obj.check_for_duplicate_records(legal_id) is False:
        return bu_ct.DataAlreadyExists()
    if c_obj.doc_count > 0:
        c_obj.document_download_process_initiate(
            csv_id, country_id, legal_id, domain_id, unit_id, session_token
        )

    if c_obj.frame_data_for_main_db_insert(
        db, data_result, request_frame.legal_entity_id, csv_id
    ) is True:
        result = bu_ct.SaveBulkRecordSuccess()
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
    converter = PastDataJsonToCSV(request_frame, "DownloadPastData")

    if(
        converter.FILE_DOWNLOAD_PATH is None or
        converter.data_available_status is False
    ):
            return bu_ct.ExportToCSVEmpty()
    else:
        result = bu_ct.DownloadBulkPastDataSuccess(
            converter.FILE_DOWNLOAD_PATH
        )
    return result


def process_download_uploaded_data(
        request_frame
):
    csv_id = request_frame.csv_id
    file_download_path = get_files_as_zip(
        csv_id
    )
    return bu_ct.DownloadUploadedDataSuccess(
        file_download_path
    )


def process_update_document_count(
    db, request_frame
):
    csv_id = request_frame.csv_id
    count = request_frame.count
    update_document_count(db, csv_id, count)
    return bu_ct.UpdateDocumentCountSuccess()


def process_get_status(db, request):
    csv_name = request.csv_name
    file_string = csv_name.split(".")
    file_name = "%s_%s.%s" % (
        file_string[0], "result", "txt"
    )
    file_path = "%s/%s" % (BULKUPLOAD_INVALID_PATH, file_name)
    if os.path.exists(file_path) is False:
        return bu_ct.Alive()
    else:
        return_data = ""
        with open(file_path, "r") as fn:
            return_data += fn.read()
        result = json.loads(return_data)
        remove_uploaded_file(file_path)
        if str(result[0]) == "InvalidCsvFile":
            return bu_ct.InvalidCsvFile()
        elif str(result[0]) == "DataAlreadyExists":
            return bu_ct.DataAlreadyExists()
        elif str(result[0]) == "UploadCompletedTaskCurrentYearCSVSuccess":
            return bu_ct.UploadCompletedTaskCurrentYearCSVSuccess.parse_inner_structure(
                result[1])
        elif str(result[0]) == "UploadCompletedTaskCurrentYearCSVFailed":
            return bu_ct.UploadCompletedTaskCurrentYearCSVFailed.parse_inner_structure(
                result[1])
        else:
            return bu_ct.InvalidCsvFile()


def process_queued_tasks(db, request_frame, session_user, session_token):
    # file_submit_status = request_frame.file_submit_status
    # data_submit_status = request_frame.data_submit_status
    csv_id = request_frame.new_csv_id
    country_id = request_frame.country_id
    legal_id = request_frame.legal_entity_id
    domain_id = request_frame.domain_id
    unit_id = request_frame.unit_id
    result = None

    file_cur_stats, data_cur_stats, \
        file_download_stats = \
        get_current_doc_data_submit_status(db, csv_id)

    dataResult = get_past_record_data(db, csv_id)
    cObj = ValidateCompletedTaskForSubmit(
        db, csv_id, dataResult, session_user)

    if (file_cur_stats == 1 and data_cur_stats == 1):
        return bu_ct.ProcessCompleted()

    if(file_cur_stats in [0, 2] and file_download_stats != "completed"):
        cObj.document_download_process_initiate(
            csv_id, country_id, legal_id, domain_id, unit_id, session_token
        )
        print "document Download process initiated "
        result = bu_ct.ProcessDocumentSubmitQueued()

    if(data_cur_stats in [0, 2]):
        print "data submit process initiated "
        if cObj.check_for_duplicate_records(legal_id) is False:
            return bu_ct.DataAlreadyExists()
        if cObj.frame_data_for_main_db_insert(
            db, dataResult, request_frame.legal_entity_id, session_user
        ) is True:
            result = bu_ct.ProcessQueuedTasksSuccess()
    else:
        result = bu_ct.ProcessQueuedTasksSuccess()
    return result
