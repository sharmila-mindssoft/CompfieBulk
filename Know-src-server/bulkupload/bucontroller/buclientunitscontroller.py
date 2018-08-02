import os
import traceback
from server import logger
import pickle
import multiprocessing
import json

from ..bucsvvalidation.clientunitsvalidation import (
    ValidateClientUnitsBulkCsvData,
    ValidateClientUnitsBulkDataForApprove
)

from ..bucsvvalidation.rejecteddownloadvalidation import (
    ValidateRejectedDownloadBulkData)

from ..buapiprotocol import buclientunitsprotocol as bu_cu
from ..buapiprotocol import bustatutorymappingprotocol as bu_sm


from ..budatabase.buclientunitsdb import (
    save_client_units_mapping_csv,
    save_mapping_client_unit_data,
    get_clientunits_uploaded_csvList,
    fetch_rejected_client_unit_report,
    update_unit_count,
    get_list_and_delete_rejected_unit,
    fetch_client_unit_bulk_report,
    fetch_rejected_cu_download_csv_report,
    get_cu_csv_file_name_by_id,
    update_bulk_client_unit_approve_reject_list,
    get_bulk_client_units_and_filtersets_by_csv_id,
    get_bulk_client_unit_list_by_filter,
    save_client_unit_action_from_view,
    get_bulk_client_unit_null_action_count,
    get_bulk_client_unit_file_count,
    get_techno_users_list,
    get_cliens_for_client_unit_bulk_upload
)
from ..bulkuploadcommon import (
    convert_base64_to_file,
    read_data_from_csv,
    generate_valid_file,
    remove_uploaded_file
)
import datetime
from ..bulkexport import ConvertJsonToCSV
from bulkupload.bulkconstants import (
    BULKUPLOAD_CSV_PATH, CSV_MAX_LINES, BULKUPLOAD_INVALID_PATH
)
from protocol import generalprotocol, technoreports
__all__ = [
    "process_bu_client_units_request"
]
######################################################################
'''
    Process all client units bulk request here
   :param
        request: api Request class object
        db: database object
        session_user: logged in user id
   :type
        request: Object
        db: Object
        session_user: String
   :returns
        result: returns processed api response class Object
    rtype:
        result: Object
'''
######################################################################
db = None
t = None


def process_bu_client_units_request(request, db, session_user):
    result = None
    db = db
    request_frame = request.request

    if type(request_frame) is bu_cu.UploadClientUnitsBulkCSV:
        result = upload_client_units_bulk_csv(db, request_frame, session_user)

    if type(request_frame) is bu_cu.GetClientUnitsUploadedCSVFiles:
        result = get_clientunits_uploaded_csvFiles(
            db, request_frame, session_user
        )

    if type(request_frame) is bu_cu.GetClientUnitRejectedData:
        result = get_rejected_client_unit_data(db, request_frame, session_user)

    if type(request_frame) is bu_cu.UpdateUnitClickCount:
        result = update_unit_download_count(db, request_frame, session_user)

    if type(request_frame) is bu_cu.DeleteRejectedUnitDataByCsvID:
        result = delete_rejected_unit_data_by_csv_id(db, request_frame,
                                                     session_user)

    if type(request_frame) is bu_cu.GetClientUnitBulkReportData:
        result = get_client_unit_bulk_report_data(db, request_frame,
                                                  session_user)

    if type(request_frame) is bu_cu.DownloadRejectedClientUnitReport:
        result = download_rejected_cu_report(db, request_frame, session_user)

    if type(request_frame) is bu_cu.ExportCUBulkReportData:
        result = export_clientunit_bulk_report(db, request_frame, session_user)

    if type(request_frame) is bu_cu.PerformClientUnitApproveReject:
        result = perform_bulk_client_unit_approve_reject(
            db, request_frame, session_user
        )

    if type(request_frame) is bu_cu.ConfirmClientUnitDeclination:
        result = perform_bulk_client_unit_declination(
            db, request_frame, session_user
        )

    if type(request_frame) is bu_cu.GetBulkClientUnitApproveRejectList:
        result = get_client_unit_list_and_filters_for_view(
            db, request_frame, session_user
        )

    if type(request_frame) is bu_cu.GetBulkClientUnitListForFilterView:
        result = get_bulk_client_unit_list_by_filter_for_view(
            db, request_frame, session_user
        )

    if type(request_frame) is bu_cu.SaveBulkClientUnitListFromView:
        result = save_bulk_client_unit_list_action(
            db, request_frame, session_user
        )

    if type(request_frame) is bu_cu.SubmitBulkClientUnitListFromView:
        result = submit_bulk_client_unit_list_action(
            db, request_frame, session_user
        )

    if type(request_frame) is bu_cu.ConfirmSubmitClientUnitFromView:
        result = confirm_submit_bulk_client_unit_list_action(
            db, request_frame, session_user
        )

    if type(request_frame) is bu_cu.GetTechnoUserDetails:
        result = process_get_techno_users(db, request_frame, session_user)

    if type(request_frame) is bu_cu.GetClientGroupsList:
        result = get_client_groups_for_client_unit_bulk_upload(
            db, request_frame, session_user
        )

    if type(request_frame) is bu_cu.GetClientUnitUploadStatus:
        result = process_get_cu_upload_status(request_frame)

    if type(request_frame) is bu_cu.GetApproveClientUnitStatus:
        result = process_get_approve_client_unit_status(request_frame)

    return result

###########################################################################
'''
   save the file in csv folder after success full csv data validation
   :param
        db: database object
        request_frame: api request UploadClientUnitsBulkCSV class object
        session_user: logged in user id
   :type
        db: Object
        request_frame: Object
        session_user: String
   :returns
        result: return could be success class object or failure class
            objects also raise the exceptions
    rtype:
        result: Object
'''
###########################################################################


def upload_client_units_bulk_csv(db, request_frame, session_user):
    try:
        starttime = datetime.datetime.now().strftime("%d-%b-%Y %H:%M:%S")
        logger.logKnowledge(
            "info", "upload_client_units_bulk_csv",
            "Begin - Upload Clicked. Start Time: %s" % (starttime))

        if get_bulk_client_unit_file_count(db, session_user.user_id()) is False:
            return bu_cu.ClientUnitUploadMaxReached()
        logger.logKnowledge(
            "info", "upload_client_units_bulk_csv",
            "Begin, Max Count Checked"
        )
        # save csv file
        csv_name = convert_base64_to_file(
            BULKUPLOAD_CSV_PATH, request_frame.csv_name,
            request_frame.csv_data
        )
        endtime = datetime.datetime.now().strftime("%d-%b-%Y %H:%M:%S")
        logger.logKnowledge(
            "info", "upload_client_units_bulk_csv",
            "Csv File Write Completed - %s" % (endtime))
        logger.logKnowledge(
            "info", "upload_client_units_bulk_csv",
            "Base 64 Converted csv_name - %s" % (csv_name))

        # read data from csv file
        header, client_units_bulk_data = read_data_from_csv(csv_name)
        logger.logKnowledge(
            "info", "upload_client_units_bulk_csv",
            "Read Data From Csv Done, header: %s " % (header))

        cu_header = pickle.dumps(header)
        cu_bulk_data = pickle.dumps(client_units_bulk_data)

        logger.logKnowledge("info", "upload_client_units_bulk_csv",
                            "Begin Multi processing")

        t = multiprocessing.Process(
            target=client_unit_validate_data,
            args=(
                request_frame, session_user.user_id(),
                csv_name, cu_header, cu_bulk_data
            )
        )
        t.start()
        print "Proces id=======================>", t.pid
        logger.logKnowledge(
            "info", "upload_client_units_bulk_csv",
            "Process Id %s for csvname %s: " % (t.pid, csv_name)
        )
        return bu_cu.Done(csv_name)
    except Exception, e:
        print e
        print str(traceback.format_exc())
        logger.logKnowledge(
            "error", "upload_client_units_bulk_csv",
            str(traceback.format_exc()))
        raise e


def client_unit_validate_data(
    request_frame, session_user, csv_name, cu_header, cu_bulk_data
):
    def write_file():
        file_string = csv_name.split(".")
        file_name = "%s_%s.%s" % (
            file_string[0], "upload", "txt"
        )
        file_path = "%s/%s" % (BULKUPLOAD_INVALID_PATH, file_name)
        try:
            with open(file_path, "wb") as fn:
                fn.write(return_data)
                os.chmod(file_path, 0777)
        except IOError, e:
            logger.logKnowledge(
                "error", "client_unit_validate_data - write_file",
                "IO Error While writing return_data file %s" % (e))
            raise RuntimeError(e)
        return
    try:
        # csv data validation
        logger.logKnowledge("info", "client_unit_validate_data",
                            "Process begin")
        header = pickle.loads(cu_header)
        client_units_bulk_data = pickle.loads(cu_bulk_data)
        return_data = None
        print "db -> ", db
        clientUnitObj = ValidateClientUnitsBulkCsvData(
            db, client_units_bulk_data, session_user,
            request_frame.bu_client_id,
            csv_name, header
        )
        logger.logKnowledge("info", "client_unit_validate_data",
                            "clientUnitObj Generated")
        validationResult = clientUnitObj.perform_validation()

        logger.logKnowledge("info", "client_unit_validate_data",
                            "Perform validation Done ")
        print "err--------------------------------------------"
        print validationResult
        if (
            "No such file or directory" not in validationResult and
            validationResult != "Empty CSV File Uploaded" and
            validationResult != "CSV File lines reached max limit" and
            validationResult != "Csv Column Mismatched" and
            "ordinal not in range(128)" not in validationResult and
            (validationResult["return_status"] is not None and
                validationResult["return_status"] is True)
        ):
            logger.logKnowledge("info", "client_unit_validate_data",
                                "Came into if before generate valid file ")
            generate_valid_file(csv_name)
            csv_args = [
                request_frame.bu_client_id, request_frame.bu_group_name,
                csv_name, session_user, validationResult["total"]
            ]
            new_csv_id = save_client_units_mapping_csv(db, csv_args)
            logger.logKnowledge("info", "client_unit_validate_data",
                                "csv id generated -> %s " % (new_csv_id))
            if new_csv_id:
                if save_mapping_client_unit_data(
                        db, new_csv_id, validationResult["data"]
                ) is True:
                    logger.logKnowledge("info", "client_unit_validate_data",
                                        "save mapping client unit if True ")
                    clientUnitObj.save_executive_message(
                        csv_name, request_frame.bu_group_name,
                        session_user
                    )
                    logger.logKnowledge("info", "client_unit_validate_data",
                                        "save_executive_message saved ")
                    clientUnitObj.source_commit()
                    result = bu_cu.UploadClientUnitBulkCSVSuccess(
                        validationResult["total"], validationResult["valid"],
                        validationResult["invalid"]
                    ).to_structure()
                    return_data = json.dumps(result)
                    logger.logKnowledge(
                        "info", "client_unit_validate_data",
                        "return data in first If-> %s" % (return_data))
        elif (
            "No such file or directory" not in validationResult and
            "ordinal not in range(128)" not in validationResult and
            validationResult != "Empty CSV File Uploaded" and
            validationResult != "CSV File lines reached max limit" and
            validationResult != "Csv Column Mismatched" and
            (validationResult["return_status"] is not None and
                validationResult["return_status"] is False)
        ):
            result = bu_cu.UploadClientUnitBulkCSVFailed(
                validationResult["invalid_file"],
                validationResult["mandatory_error"],
                validationResult["max_length_error"],
                validationResult["duplicate_error"],
                validationResult["invalid_char_error"],
                validationResult["invalid_data_error"],
                validationResult["inactive_error"],
                validationResult["max_unit_count_error"],
                validationResult["total"], validationResult["invalid"]
            ).to_structure()
            return_data = json.dumps(result)
            logger.logKnowledge(
                        "info", "client_unit_validate_data",
                        "return data in first elIf-> %s" % (return_data))
        elif (
            "No such file or directory" not in validationResult and
            "ordinal not in range(128)" not in validationResult and
            validationResult != "CSV File lines reached max limit" and
            validationResult != "Csv Column Mismatched" and
            validationResult == "Empty CSV File Uploaded"
        ):
            result = bu_cu.EmptyCSVUploaded().to_structure()
            return_data = json.dumps(result)
            logger.logKnowledge(
                        "info", "client_unit_validate_data",
                        "return data in second elIf-> %s" % (return_data))
        elif (
            "No such file or directory" not in validationResult and
            "ordinal not in range(128)" not in validationResult and
            validationResult != "Csv Column Mismatched" and
            validationResult == "CSV File lines reached max limit"
        ):
            csv_path = os.path.join(BULKUPLOAD_CSV_PATH, "csv")
            file_path = os.path.join(csv_path, csv_name)
            remove_uploaded_file(file_path)
            result = bu_cu.CSVFileLinesMaxREached(
                                            csv_max_lines=CSV_MAX_LINES
                            ).to_structure()
            return_data = json.dumps(result)
            logger.logKnowledge(
                        "info", "client_unit_validate_data",
                        "return data in third elIf-> %s" % (return_data))
        elif (
            "No such file or directory" not in validationResult and
            "ordinal not in range(128)" not in validationResult and
            validationResult == "Csv Column Mismatched"
        ):
            result = bu_cu.CSVColumnMisMatched().to_structure()
            return_data = json.dumps(result)
            logger.logKnowledge(
                        "info", "client_unit_validate_data",
                        "return data in fourth elIf-> %s" % (return_data))
        elif (
            "No such file or directory" in validationResult or
            "ordinal not in range(128)" in validationResult
        ):
            result = bu_cu.InvalidCSVUploaded().to_structure()
            return_data = json.dumps(result)
            logger.logKnowledge(
                        "info", "client_unit_validate_data",
                        "return data in fifth elIf-> %s" % (return_data))
    except AssertionError as error:
        e = "AssertionError"
        return_data = json.dumps(e)
        write_file()
        logger.logKnowledge(
            "error",
            "buclientunitscontroller.py - client_unit_validate_data", e)
        raise error
    except Exception, e:
        return_data = json.dumps(str(e))
        write_file()
        logger.logKnowledge(
            "error",
            "buclientunitscontroller.py - client_unit_validate_data", e)
        raise e
    write_file()
    print "os pid ---->>>", os.getpid()
    return


def upload_client_units_bulk_csv_old_copy(db, request_frame, session_user):

    if get_bulk_client_unit_file_count(db, session_user.user_id()):
        # save csv file
        csv_name = convert_base64_to_file(
            BULKUPLOAD_CSV_PATH, request_frame.csv_name,
            request_frame.csv_data
        )
        # read data from csv file
        header, client_units_bulk_data = read_data_from_csv(csv_name)
        # csv data validation
        clientUnitObj = ValidateClientUnitsBulkCsvData(
            db, client_units_bulk_data, session_user,
            request_frame.bu_client_id,
            csv_name, header
        )
        validationResult = clientUnitObj.perform_validation()
        print "err--------------------------------------------"
        if (
            "No such file or directory" not in validationResult and
            validationResult != "Empty CSV File Uploaded" and
            validationResult != "CSV File lines reached max limit" and
            validationResult != "Csv Column Mismatched" and
            "ordinal not in range(128)" not in validationResult and
            (validationResult["return_status"] is not None and
                validationResult["return_status"] is True)
        ):
            generate_valid_file(csv_name)
            csv_args = [
                request_frame.bu_client_id, request_frame.bu_group_name,
                csv_name, session_user.user_id(), validationResult["total"]
            ]
            new_csv_id = save_client_units_mapping_csv(db, csv_args)
            if new_csv_id:
                if save_mapping_client_unit_data(
                        db, new_csv_id, validationResult["data"]
                ) is True:
                    clientUnitObj.save_executive_message(
                        csv_name, request_frame.bu_group_name,
                        session_user.user_id()
                    )
                    clientUnitObj.source_commit()
                    result = bu_cu.UploadClientUnitBulkCSVSuccess(
                        validationResult["total"], validationResult["valid"],
                        validationResult["invalid"]
                    )
                    return result
        elif (
            "No such file or directory" not in validationResult and
            "ordinal not in range(128)" not in validationResult and
            validationResult != "Empty CSV File Uploaded" and
            validationResult != "CSV File lines reached max limit" and
            validationResult != "Csv Column Mismatched" and
            (validationResult["return_status"] is not None and
                validationResult["return_status"] is False)
        ):
            result = bu_cu.UploadClientUnitBulkCSVFailed(
                validationResult["invalid_file"],
                validationResult["mandatory_error"],
                validationResult["max_length_error"],
                validationResult["duplicate_error"],
                validationResult["invalid_char_error"],
                validationResult["invalid_data_error"],
                validationResult["inactive_error"],
                validationResult["max_unit_count_error"],
                validationResult["total"], validationResult["invalid"]
            )
            return result
        elif (
            "No such file or directory" not in validationResult and
            "ordinal not in range(128)" not in validationResult and
            validationResult != "CSV File lines reached max limit" and
            validationResult != "Csv Column Mismatched" and
            validationResult == "Empty CSV File Uploaded"
        ):
            return bu_cu.EmptyCSVUploaded()
        elif (
            "No such file or directory" not in validationResult and
            "ordinal not in range(128)" not in validationResult and
            validationResult != "Csv Column Mismatched" and
            validationResult == "CSV File lines reached max limit"
        ):
            csv_path = os.path.join(BULKUPLOAD_CSV_PATH, "csv")
            file_path = os.path.join(csv_path, csv_name)
            remove_uploaded_file(file_path)
            return bu_cu.CSVFileLinesMaxREached(csv_max_lines=CSV_MAX_LINES)
        elif (
            "No such file or directory" not in validationResult and
            "ordinal not in range(128)" not in validationResult and
            validationResult == "Csv Column Mismatched"
        ):
            return bu_cu.CSVColumnMisMatched()
        elif (
            "No such file or directory" in validationResult or
            "ordinal not in range(128)" in validationResult
        ):
            return bu_cu.InvalidCSVUploaded()
    else:
        return bu_cu.ClientUnitUploadMaxReached()

##############################################################################
'''
   Get the bulk client unit CSV files uploaded list
   :param
        db: database object
        request_frame: api request GetClientUnitsUploadedCSVFiles class object
        session_user: logged in user id
   :type
        db: Object
        request_frame: Object
        session_user: String
   :returns
        result: return could be success class object or failure class objects
            also raise the exceptions
    rtype:
        result: Object
'''
###############################################################################


def get_clientunits_uploaded_csvFiles(db, request_frame, session_user):

    clientId = request_frame.bu_client_id
    groupName = request_frame.bu_group_name
    csvFilesList = get_clientunits_uploaded_csvList(db, clientId, groupName)
    return bu_cu.ClientUnitsUploadedCSVFilesListSuccess(
        bu_cu_csv_files_list=csvFilesList
    )


####################################################################
# Retrieved Rejected Client Unit
####################################################################

def get_rejected_client_unit_data(db, request_frame, session_user):
    client_group_id = request_frame.bu_client_id
    user_id = session_user.user_id()
    rejected_unit_data = fetch_rejected_client_unit_report(db, session_user,
                                                           user_id,
                                                           client_group_id)
    result = bu_cu.GetRejectedClientUnitDataSuccess(rejected_unit_data)
    return result


####################################################################
# Update Client Unit Download Count
####################################################################

def update_unit_download_count(db, request_frame, session_user):

    csv_id = request_frame.csv_id
    updated_unit_count = update_unit_count(db, session_user, csv_id)
    result = bu_cu.UpdateUnitDownloadCountSuccess(updated_unit_count)
    return result


def delete_rejected_unit_data_by_csv_id(db, request_frame, session_user):

    bu_client_id = request_frame.bu_client_id
    csv_id = request_frame.csv_id
    user_id = session_user.user_id()

    rejected_unit_data = get_list_and_delete_rejected_unit(
        db, session_user, user_id, csv_id, bu_client_id)

    result = bu_cu.GetRejectedClientUnitDataSuccess(rejected_unit_data)
    return result


def get_client_unit_bulk_report_data(db, request_frame, session_user):
    clientGroupId = request_frame.bu_client_id
    from_date = request_frame.from_date
    to_date = request_frame.to_date
    record_count = request_frame.r_count
    page_count = request_frame.p_count
    child_ids = request_frame.child_ids
    user_category_id = request_frame.user_category_id

    date_time = datetime.datetime
    request_format = '%Y-%m-%d %H:%M:%S'
    from_date = date_time.strptime(from_date, '%d-%b-%Y').strftime(
        request_format)

    to_date = date_time.strptime(to_date, '%d-%b-%Y').strftime(request_format)

    clientdata, total_record = fetch_client_unit_bulk_report(
        db, session_user, session_user.user_id(), clientGroupId, from_date,
        to_date, record_count, page_count, child_ids, user_category_id)

    result = bu_cu.GetClientUnitReportDataSuccess(clientdata, total_record)
    return result

########################################################
# To Export the Client Unit Report Data
########################################################


def export_clientunit_bulk_report(db, request, session_user):
    if request.csv:
        converter = ConvertJsonToCSV(
            db, request, session_user, "ExportCUBulkReport"
        )
        if converter.FILE_DOWNLOAD_PATH is None:
            return technoreports.ExportToCSVEmpty()
        else:
            return generalprotocol.ExportToCSVSuccess(
                link=converter.FILE_DOWNLOAD_PATH
            )

###############################################################################
'''   returns system declination count from the csv file data
   :param
        db: database object
        request_frame: api request PerformClientUnitApproveReject class object
        session_user: logged in user details
   :type
        db: Object
        request_frame: Object
        session_user: Object
   :returns
        result: returns processed api response
            PerformClientUnitApproveRejectSuccess class Object
    rtype:
        result: Object
'''
###############################################################################


def perform_bulk_client_unit_approve_reject(db, request_frame, session_user):

    csv_id = request_frame.csv_id
    # bu_client_id = request_frame.bu_client_id
    # bu_remarks = request_frame.bu_remarks
    # actionType = request_frame.bu_action

    try:

        t = multiprocessing.Process(
            target=client_unit_approve_reject_process,
            args=(request_frame, session_user.user_id()))
        t.start()
        print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!", t.pid
        return bu_cu.Done(str(csv_id))
    except Exception, e:
        print e
        print str(traceback.format_exc())
        raise e


def client_unit_approve_reject_process(request_frame, session_user):
    def write_file(return_data):
        csv_id = request_frame.csv_id
        file_name = "%s_%s.%s" % (
            csv_id, "approve_cu", "txt"
        )
        file_path = "%s/%s" % (BULKUPLOAD_INVALID_PATH, file_name)
        with open(file_path, "wb") as fn:
            os.chmod(file_path, 0777)
            fn.write(return_data)

    try:
        return_data = None
        csv_id = request_frame.csv_id
        bu_client_id = request_frame.bu_client_id
        bu_remarks = request_frame.bu_remarks
        actionType = request_frame.bu_action
        print "sessionusr client_unit_approve_reject_process-> ", session_user
        clientUnitObj = ValidateClientUnitsBulkDataForApprove(
            db, csv_id, bu_client_id, session_user
        )
        if actionType == 1:
            system_declined_count, system_declined_error, \
                manual_rejection_count = \
                clientUnitObj.check_for_system_declination_errors()
            if len(system_declined_count) == 0 and manual_rejection_count > 0:
                return_data = bu_cu.ReturnDeclinedCount(
                    len(system_declined_count), int(manual_rejection_count)
                ).to_structure()
            elif (
                    len(system_declined_count) > 0 and
                    manual_rejection_count == 0
            ):
                return_data = bu_cu.ReturnDeclinedCount(
                    len(system_declined_count), int(manual_rejection_count)
                ).to_structure()
            elif len(system_declined_count) > 0 and manual_rejection_count > 0:
                return_data = bu_cu.ReturnDeclinedCount(
                    len(system_declined_count), int(manual_rejection_count)
                ).to_structure()
            else:
                if (
                    update_bulk_client_unit_approve_reject_list(
                        db, csv_id, actionType, bu_remarks, 0, session_user
                    )
                ):
                    clientUnitObj.process_data_to_main_db_insert(
                        system_declined_count
                    )
                    clientUnitObj.save_manager_message(
                        actionType, clientUnitObj._csv_name,
                        clientUnitObj._group_name,
                        session_user, clientUnitObj._uploaded_by,
                        None, 0
                    )
                    clientUnitObj.source_commit()
                    return_data = bu_cu.UpdateApproveRejectActionFromListSuccess().to_structure()
        else:
            if (
                update_bulk_client_unit_approve_reject_list(
                    db, csv_id, actionType, bu_remarks, 0, session_user
                )
            ):
                clientUnitObj.store_initial_values()
                clientUnitObj.save_manager_message(
                    actionType, clientUnitObj._csv_name,
                    clientUnitObj._group_name,
                    session_user, clientUnitObj._uploaded_by,
                    bu_remarks, 0
                )
                clientUnitObj.source_commit()
                return_data = bu_cu.UpdateApproveRejectActionFromListSuccess().to_structure()
        return_data = json.dumps(return_data)
    except AssertionError as error:
        e = "AssertionError"
        return_data = json.dumps(e)
        write_file(return_data)
        logger.logKnowledge(
            "error",
            "buclientunitscontroller.py - client_unit_approve_reject_process",
            e
        )
        raise error
    except Exception, e:
        return_data = json.dumps(str(e))
        write_file(return_data)
        logger.logKnowledge(
            "error",
            "buclientunitscontroller.py - client_unit_approve_reject_process",
            e
        )
        raise e
    write_file(return_data)
    return


########################################################
'''
   save the file in csv folder after success full csv data validation
   :param
        db: database object
        request_frame: api request RejectedStatutoryMappingCSV class object
    result: return could be success class object or failure class objects
        also raise the exceptions
    rtype:
        result: Object
'''
##############################################################################


def download_rejected_cu_report(db, request_frame, session_user):
    csv_id = request_frame.csv_id
    cg_id = request_frame.cg_id
    download_format = request_frame.download_format
    user_id = session_user.user_id()
    sheet_name = "Rejected Client Unit"

    csv_header_key = ["country", "legal_entity", "division", "category",
                      "geography_level", "unit_location", "unit_code",
                      "unit_name", "address",
                      "city", "state",
                      "postalcode", "domain", "organization",
                      "remarks", "rejected_reason", "is_fully_rejected"]

    csv_column_name = ["Country", "Legal_Entity*", "Division*",
                       "Category*", "Geography_Level*",
                       "Unit_Location*", "Unit_Code*",
                       "Unit_Name*  ",
                       "Unit_Address*", "City*",
                       "State*", "Postal_Code*",
                       "Domain*", "Organization*",
                       "Error_Description"]

    csv_name = get_cu_csv_file_name_by_id(db, session_user, user_id, csv_id)

    source_data = fetch_rejected_cu_download_csv_report(
        db, session_user, user_id,
        cg_id, csv_id)

    cObj = ValidateRejectedDownloadBulkData(
        db, source_data, session_user, download_format, csv_name,
        csv_header_key, csv_column_name, sheet_name)
    result = cObj.perform_validation()

    return bu_sm.DownloadActionSuccess(result["xlsx_link"], result["csv_link"],
                                       result["ods_link"], result["txt_link"]
                                       )


##############################################################################
'''   returns boolean value for the updation
   :param
        db: database object
        request_frame: api request ConfirmClientUnitDeclination class object
        session_user: logged in user details
   :type
        db: Object
        request_frame: Object
        session_user: Object
   :returns
        result: returns processed api response ConfirmClientUnitDeclination
        class Object
    rtype:
        result: Boolean
'''
##############################################################################


def perform_bulk_client_unit_declination(db, request_frame, session_user):

    csv_id = request_frame.csv_id
    bu_client_id = request_frame.bu_client_id
    try:

        t = multiprocessing.Process(
            target=client_unit_declination_process,
            args=(request_frame, session_user.user_id()))
        t.start()
        print "!!!!!!!!! perform_bulk_client_unit_declination!!!!!!!!", t.pid
        return bu_cu.Done(str(csv_id))
    except Exception, e:
        print e
        print str(traceback.format_exc())
        raise e


def client_unit_declination_process(request_frame, session_user):
    def write_file(return_data):
        csv_id = request_frame.csv_id
        file_name = "%s_%s.%s" % (
            csv_id, "approve_cu", "txt"
        )
        file_path = "%s/%s" % (BULKUPLOAD_INVALID_PATH, file_name)
        with open(file_path, "wb") as fn:
            os.chmod(file_path, 0777)
            fn.write(return_data)

    try:
        return_data = None
        csv_id = request_frame.csv_id
        bu_client_id = request_frame.bu_client_id

        clientUnitObj = ValidateClientUnitsBulkDataForApprove(
            db, csv_id, bu_client_id, session_user
        )

        system_declined_count, system_declined_error, \
            manual_rejection_count = \
            clientUnitObj.check_for_system_declination_errors()
        if len(system_declined_count) > 0:
            if (
                update_bulk_client_unit_approve_reject_list(
                    db, csv_id, 1, None, len(system_declined_count),
                    session_user
                )
            ):
                clientUnitObj.process_data_to_main_db_insert(
                    system_declined_count
                )
                clientUnitObj.make_rejection(
                    csv_id, 1, system_declined_count, system_declined_error
                )
                clientUnitObj.save_manager_message(
                    1, clientUnitObj._csv_name, clientUnitObj._group_name,
                    session_user, clientUnitObj._uploaded_by,
                    None, len(system_declined_count)
                )
                clientUnitObj.source_commit()
                return_data = bu_cu.SubmitClientUnitDeclinationSuccess().to_structure()
        else:
            if (
                update_bulk_client_unit_approve_reject_list(
                    db, csv_id, 1, None, len(system_declined_count),
                    session_user
                )
            ):
                print "in if update_bulk_client_unit_approve_reject_list "
                clientUnitObj.process_data_to_main_db_insert([])
                clientUnitObj.save_manager_message(
                    1, clientUnitObj._csv_name, clientUnitObj._group_name,
                    session_user, clientUnitObj._uploaded_by,
                    None, len(system_declined_count)
                )
                clientUnitObj.source_commit()
                return_data = bu_cu.SubmitClientUnitDeclinationSuccess().to_structure()

        return_data = json.dumps(return_data)
    except AssertionError as error:
        e = "AssertionError"
        return_data = json.dumps(e)
        write_file(return_data)
        logger.logKnowledge(
            "error",
            "buclientunitscontroller.py - client_unit_declination_process",
            e
        )
        raise error
    except Exception, e:
        return_data = json.dumps(str(e))
        write_file(return_data)
        logger.logKnowledge(
            "error",
            "buclientunitscontroller.py - client_unit_declination_process",
            e
        )
        raise e
    write_file(return_data)
    return

############################################################################
'''   returns set of dataset
   :param
        db: database object
        request_frame: api request GetBulkClientUnitApproveRejectList class
            object
        session_user: logged in user details
   :type
        db: Object
        request_frame: Object
        session_user: Object
   :returns
        result: returns processed api response
            GetBulkClientUnitApproveRejectList class Object
    rtype:
        result: set of datasets
'''
############################################################################


def get_client_unit_list_and_filters_for_view(
    db, request_frame, session_user
):

    resultSet = get_bulk_client_units_and_filtersets_by_csv_id(
        db, request_frame, session_user
    )
    return resultSet

##########################################################################
'''   returns a dataset
   :param
        db: database object
        request_frame: api request GetBulkClientUnitApproveRejectList
            class object
        session_user: logged in user details
   :type
        db: Object
        request_frame: Object
        session_user: Object
   :returns
        result: returns processed api response
            GetBulkClientUnitApproveRejectList class Object
    rtype:
        result: set of datasets
'''
###########################################################################


def get_bulk_client_unit_list_by_filter_for_view(
    db, request_frame, session_user
):

    response = get_bulk_client_unit_list_by_filter(
        db, request_frame, session_user
    )
    return response

###########################################################################
'''   returns boolean value for the updation
   :param
        db: database object
        request_frame: api request SubmitBulkClientUnitListFromView
            class object
        session_user: logged in user details
   :type
        db: Object
        request_frame: Object
        session_user: Object
   :returns
        result: returns processed api response
            SubmitBulkClientUnitListFromView class Object
    rtype:
        result: Boolean
'''
###########################################################################


def submit_bulk_client_unit_list_action(db, request_frame, session_user):
    csv_id = request_frame.csv_id
    # bu_client_id = request_frame.bu_client_id
    try:
        if (get_bulk_client_unit_null_action_count(
            db, request_frame, session_user
        )) is False:
            return bu_cu.SubmitClientUnitActionFromListFailure()

        else:
            t = multiprocessing.Process(
                target=client_unit_submit_list_process,
                args=(request_frame, session_user.user_id()))
            t.start()
            print "!!!!!!!submit_bulk_client_unit_list_action!!!!!!!!", t.pid
            return bu_cu.Done(str(csv_id))
    except Exception, e:
        print e
        print str(traceback.format_exc())
        raise e


def client_unit_submit_list_process(request_frame, session_user):
    def write_file(return_data):
        csv_id = request_frame.csv_id
        file_name = "%s_%s.%s" % (
            csv_id, "approve_cu", "txt"
        )
        file_path = "%s/%s" % (BULKUPLOAD_INVALID_PATH, file_name)
        with open(file_path, "wb") as fn:
            os.chmod(file_path, 0777)
            fn.write(return_data)

    try:
        return_data = None
        csv_id = request_frame.csv_id
        bu_client_id = request_frame.bu_client_id
        clientUnitObj = ValidateClientUnitsBulkDataForApprove(
            db, csv_id, bu_client_id, session_user
        )
        system_declined_count, system_declined_error, \
            manual_rejection_count = \
            clientUnitObj.check_for_system_declination_errors()
        if (
                len(system_declined_count) > 0 and
                manual_rejection_count == 0
        ):
            return_data = bu_cu.ReturnDeclinedCount(
                len(system_declined_count), int(manual_rejection_count)
            ).to_structure()
        elif len(system_declined_count) > 0 and manual_rejection_count > 0:
            return_data = bu_cu.ReturnDeclinedCount(
                len(system_declined_count), int(manual_rejection_count)
            ).to_structure()
        else:
            clientUnitObj.process_data_to_main_db_insert(
                system_declined_count
            )
            clientUnitObj.save_manager_message(
                1, clientUnitObj._csv_name, clientUnitObj._group_name,
                session_user, clientUnitObj._uploaded_by,
                None, 0
            )
            clientUnitObj.source_commit()
            update_bulk_client_unit_approve_reject_list(
                db, csv_id, 4, None, 0, session_user
            )
            return_data = bu_cu.SubmitClientUnitActionFromListSuccess(
                ).to_structure()
        return_data = json.dumps(return_data)
    except AssertionError as error:
        e = "AssertionError"
        return_data = json.dumps(e)
        write_file(return_data)
        logger.logKnowledge(
            "error",
            "buclientunitscontroller.py - client_unit_submit_list_process",
            e
        )
        raise error
    except Exception, e:
        return_data = json.dumps(str(e))
        write_file(return_data)
        logger.logKnowledge(
            "error",
            "buclientunitscontroller.py - client_unit_submit_list_process",
            e
        )
        raise e
    write_file(return_data)
    return


###########################################################################
'''   returns boolean value for the updation
   :param
        db: database object
        request_frame: api request SubmitBulkClientUnitListFromView class
            object
        session_user: logged in user details
   :type
        db: Object
        request_frame: Object
        session_user: Object
   :returns
        result: returns processed api response
            SubmitBulkClientUnitListFromView class Object
    rtype:
        result: Boolean
'''
###########################################################################


def confirm_submit_bulk_client_unit_list_action(
    db, request_frame, session_user
):

    csv_id = request_frame.csv_id
    bu_client_id = request_frame.bu_client_id
    try:
        t = multiprocessing.Process(
                target=client_unit_confirm_submit_process,
                args=(request_frame, session_user.user_id()))
        t.start()
        print "!!!!!!!confirm_submit_bulk_client_unit_list_action!!!!!", t.pid
        return bu_cu.Done(str(csv_id))
    except Exception, e:
        print e
        print str(traceback.format_exc())
        raise e


def client_unit_confirm_submit_process(request_frame, session_user):
    def write_file(return_data):
        csv_id = request_frame.csv_id
        file_name = "%s_%s.%s" % (
            csv_id, "approve_cu", "txt"
        )
        file_path = "%s/%s" % (BULKUPLOAD_INVALID_PATH, file_name)
        with open(file_path, "wb") as fn:
            os.chmod(file_path, 0777)
            fn.write(return_data)

    try:
        return_data = None
        csv_id = request_frame.csv_id
        bu_client_id = request_frame.bu_client_id
        clientUnitObj = ValidateClientUnitsBulkDataForApprove(
            db, csv_id, bu_client_id, session_user
        )

        system_declined_count, system_declined_error, \
            manual_rejection_count = \
            clientUnitObj.check_for_system_declination_errors()
        if len(system_declined_count) > 0:
            print "Entering If"
            clientUnitObj.process_data_to_main_db_insert(system_declined_count)
            print "Main DB Inserted"
            clientUnitObj.make_rejection(
                csv_id, 4, system_declined_count, system_declined_error
            )
            print "rejection made"
            clientUnitObj.save_manager_message(
                1, clientUnitObj._csv_name, clientUnitObj._group_name,
                session_user, clientUnitObj._uploaded_by,
                None, len(system_declined_count)
            )
            print "Manaher message saved"
            update_bulk_client_unit_approve_reject_list(
                db, csv_id, 4, None, len(system_declined_count), session_user
            )
            print "Update Done"
            clientUnitObj.source_commit()
            return_data = bu_cu.SubmitClientUnitActionFromListSuccess(
                ).to_structure()
        return_data = json.dumps(return_data)
    except AssertionError as error:
        e = "AssertionError"
        return_data = json.dumps(e)
        write_file(return_data)
        logger.logKnowledge(
            "error",
            "buclientunitscontroller.py - client_unit_confirm_submit_process",
            e
        )
        raise error
    except Exception, e:
        return_data = json.dumps(str(e))
        write_file(return_data)
        logger.logKnowledge(
            "error",
            "buclientunitscontroller.py - client_unit_confirm_submit_process",
            e
        )
        raise e
    write_file(return_data)
    return

###########################################################################
'''   returns boolean value for the updation
   :param
        db: database object
        request_frame: api request SaveBulkClientUnitListFromView
            class object
        session_user: logged in user details
   :type
        db: Object
        request_frame: Object
        session_user: Object
   :returns
        result: returns processed api response
            SaveBulkClientUnitListFromView class Object
    rtype:
        result: Boolean
'''
###########################################################################


def save_bulk_client_unit_list_action(db, request_frame, session_user):

    try:
        save_client_unit_action_from_view(
            db, request_frame.csv_id, request_frame.bulk_unit_id,
            request_frame.bu_action, request_frame.bu_remarks,
            session_user
        )
        return bu_cu.SaveClientUnitActionSuccess()

    except Exception, e:
        raise e


##################################################################
'''   returns list of techno managers / executives details
   :param
        db: database object
        request_frame: api request GetClientGroupsList
            class object
        session_user: logged in user details
   :type
        db: Object
        request_frame: Object
        session_user: Object
   :returns
        result: returns processed api response
            GetClientGroupsList class Object
    rtype:
        result: Dataset
'''
###################################################################


def process_get_techno_users(db, request, session_user):
    userType = request.user_type
    res = get_techno_users_list(db, userType, session_user.user_id())
    result_set = bu_cu.GetTechnoDetailsSuccess(res)
    return result_set


##################################################################
'''   returns list of of all clients with details for client unit
    bulk upload
   :param
        db: database object
        request_frame: api request GetClientGroupsList
            class object
        session_user: logged in user details
   :type
        db: Object
        request_frame: Object
        session_user: Object
   :returns
        result: returns processed api response
            GetClientGroupsList class Object
    rtype:
        result: Dataset
'''
###################################################################


def get_client_groups_for_client_unit_bulk_upload(db, request, session_user):
    groups = get_cliens_for_client_unit_bulk_upload(db, session_user.user_id())
    return bu_cu.GetClientGroupsListSuccess(
        client_group_list=groups
    )


def process_get_cu_upload_status(request):
    csv_name = request.csv_name
    file_string = csv_name.split(".")
    file_name = "%s_%s.%s" % (
        file_string[0], "upload", "txt"
    )
    file_path = "%s/%s" % (BULKUPLOAD_INVALID_PATH, file_name)
    if os.path.exists(file_path) is False:
        return bu_cu.Alive()
    else:
        return_data = ""
        try:
            with open(file_path, "r") as fn:
                return_data += fn.read()
        except IOError, e:
            logger.logKnowledge(
                "error", "buclientunitscontroller - process_get_cu_upload_status",
                "IO Error While Reading return_data file %s" % (e))
            raise RuntimeError(e)
        remove_uploaded_file(file_path)
        if return_data == "InvalidCSV":
            return bu_sm.InvalidCsvFile()
        else:
            result = json.loads(return_data)
            if str(result[0]) == "UploadClientUnitBulkCSVSuccess":
                return bu_cu.UploadClientUnitBulkCSVSuccess.parse_inner_structure(result[1])
            elif str(result[0]) == "UploadClientUnitBulkCSVFailed":
                return bu_cu.UploadClientUnitBulkCSVFailed.parse_inner_structure(result[1])
            elif str(result[0]) == "EmptyCSVUploaded":
                return bu_cu.EmptyCSVUploaded.parse_inner_structure(result[1])
            elif str(result[0]) == "CSVFileLinesMaxREached":
                return bu_cu.CSVFileLinesMaxREached.parse_inner_structure(result[1])
            elif str(result[0]) == "CSVColumnMisMatched":
                return bu_cu.CSVColumnMisMatched.parse_inner_structure(result[1])
            elif str(result[0]) == "InvalidCSVUploaded":
                return bu_cu.InvalidCSVUploaded.parse_inner_structure(result[1])
            else:
                logger.logKnowledge(
                    "error",
                    "buclientunitscontroller.py-process_get_cu_upload_status",
                    result
                )
                raise Exception(str(result))


def process_get_approve_client_unit_status(request):
    csv_name = request.csv_name
    file_name = "%s_%s.%s" % (
        csv_name, "approve_cu", "txt"
    )
    file_path = "%s/%s" % (BULKUPLOAD_INVALID_PATH, file_name)
    if os.path.exists(file_path) is False:
        return bu_cu.Alive()
    else:
        return_data = ""
        with open(file_path, "r") as fn:
            return_data += fn.read()
        remove_uploaded_file(file_path)
        result = json.loads(return_data)
        if str(result[0]) == "ReturnDeclinedCount":
            return bu_cu.ReturnDeclinedCount.parse_inner_structure(result[1])

        elif str(result[0]) == "UpdateApproveRejectActionFromListSuccess":
            return bu_cu.UpdateApproveRejectActionFromListSuccess.parse_inner_structure(
                result[1])

        elif str(result[0]) == "SubmitClientUnitDeclinationSuccess":
            return bu_cu.SubmitClientUnitDeclinationSuccess.parse_inner_structure(
                result[1])

        elif str(result[0]) == "SubmitClientUnitActionFromListSuccess":
            return bu_cu.SubmitClientUnitActionFromListSuccess.parse_inner_structure(
                result[1])

        elif str(result[0]) == "SubmitClientUnitActionFromListSuccess":
            return bu_cu.SubmitClientUnitActionFromListSuccess.parse_inner_structure(
                result[1])
        else:
            log_param = "buclientunitscontroller.py-" + \
                "process_get_approve_client_unit_status"
            logger.logKnowledge("error", log_param, result)
            raise Exception(str(result))
