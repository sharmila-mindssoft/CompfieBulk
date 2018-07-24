import os
import pickle
import threading
import json
import traceback
from server import logger
from ..bucsvvalidation.statutorymappingvalidation import (
    ValidateStatutoryMappingCsvData,
    ValidateStatutoryMappingForApprove,
    StatutorySource
)
from ..bucsvvalidation.rejecteddownloadvalidation import (
    ValidateRejectedDownloadBulkData
)

from ..buapiprotocol import bustatutorymappingprotocol as bu_sm
from ..budatabase.bustatutorymappingdb import (
    get_uploaded_statutory_mapping_csv_list,
    fetch_statutory_bulk_report,
    save_mapping_csv, save_mapping_data,
    get_pending_mapping_list,
    get_filters_for_approve,
    get_statutory_mapping_by_filter,
    update_approve_action_from_list,
    get_statutory_mapping_by_csv_id,
    fetch_rejected_statutory_mapping_bulk_report,
    process_delete_rejected_sm_csv_id,
    update_download_count_by_csvid,
    fetch_rejected_sm_download_csv_report,
    get_sm_csv_file_name_by_id,
    save_action_from_view,
    get_pending_action,
    delete_action_after_approval, get_rejected_sm_file_count,
    get_domains_for_user_bu,
    get_countries_for_user_bu, get_knowledge_executive_bu,
    get_sm_document_count, get_update_approve_file_status,
    get_sm_csv_name
)

from ..bulkuploadcommon import (
    convert_base64_to_file, read_data_from_csv,
    generate_valid_file, remove_uploaded_file,
    remove_bulk_uploaded_files
)
from ..bulkexport import ConvertJsonToCSV
import datetime
from ..bulkconstants import (
    BULKUPLOAD_CSV_PATH, CSV_MAX_LINES, MAX_REJECTED_COUNT,
    BULKUPLOAD_INVALID_PATH
)

from protocol import generalprotocol, technoreports
import multiprocessing


__all__ = [
    "process_bu_statutory_mapping_request"
]

########################################################
'''
    Process all statutory mapping request here
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
db = None
t = None


def process_bu_statutory_mapping_request(request, db, session_user):
    request_frame = request.request
    result = None
    db = db
    if type(request_frame) is bu_sm.GetDomains:
        result = process_get_domains_bu(session_user)

    if type(request_frame) is bu_sm.GetKExecutiveDetails:
        result = process_get_know_users_bu(session_user)

    if type(request_frame) is bu_sm.GetStatutoryMappingCsvUploadedList:
        result = get_statutory_mapping_csv_list(db, session_user)

    if type(request_frame) is bu_sm.UploadStatutoryMappingCSV:
        result = upload_statutory_mapping_csv(db, request_frame, session_user)

    if type(request_frame) is bu_sm.GetSMBulkReportData:
        result = get_sm_bulk_report_data(db, request_frame, session_user)

    if type(request_frame) is bu_sm.GetRejectedSMBulkUploadData:
        result = get_rejected_sm_bulk_data(db, request_frame, session_user)

    if type(request_frame) is bu_sm.DeleteRejectedSMCsvId:
        result = delete_rejected_sm_csv_id(db, request_frame, session_user)

    if type(request_frame) is bu_sm.UpdateDownloadCountToRejectedStatutory:
        result = update_rejected_sm_download_count(db, request_frame)

    if type(request_frame) is bu_sm.GetApproveStatutoryMappingList:
        result = get_mapping_list_for_approve(db, request_frame, session_user)

    if type(request_frame) is bu_sm.UpdateApproveActionFromList:
        result = update_statutory_mapping_action(db, request_frame,
                                                 session_user)

    if type(request_frame) is bu_sm.GetApproveStatutoryMappingView:
        result = get_statutory_mapping_data_by_csvid(db, request_frame)

    if type(request_frame) is bu_sm.ExportSMBulkReportData:
        result = export_statutory_bulk_report(db, request_frame, session_user)

    if type(request_frame) is bu_sm.DownloadRejectedSMReportData:
        result = download_rejected_sm_report(db, request_frame, session_user)

    if type(request_frame) is bu_sm.SaveAction:
        result = save_action(db, request_frame)

    if type(request_frame) is bu_sm.GetApproveMappingFilter:
        result = get_filter_for_approve_page(db, request_frame)

    if type(request_frame) is bu_sm.GetApproveStatutoryMappingViewFilter:
        result = get_statutory_mapping_data_by_filter(db, request_frame)

    if type(request_frame) is bu_sm.SubmitStatutoryMapping:
        result = submit_statutory_mapping(db, request_frame, session_user)

    if type(request_frame) is bu_sm.ConfirmStatutoryMappingSubmit:
        result = confirm_submit_statutory_mapping(
            db, request_frame, session_user
        )

    if type(request_frame) is bu_sm.SaveExecutiveMessageAfterDocUpload:
        result = save_executive_message_after_docupload(
            request_frame, session_user
        )
    if type(request_frame) is bu_sm.GetStatus:
        result = process_get_status(request_frame)

    if type(request_frame) is bu_sm.GetApproveMappingStatus:
        result = process_get_approve_mapping_status(request_frame)

    if type(request_frame) is bu_sm.DocumentQueueProcess:
        result = queue_process_statutory_document(
            db, request_frame, session_user
        )

    return result

# transaction methods begin

########################################################
# To get list of all domains
########################################################


def process_get_domains_bu(session_user):
    domains = get_domains_for_user_bu(0)
    countries = get_countries_for_user_bu(session_user.user_id())
    success = bu_sm.GetDomainsSuccess(domains, countries)
    return success


########################################################
# To get list of knowledge executive details
########################################################
def process_get_know_users_bu(session_user):

    res = get_knowledge_executive_bu(session_user.user_id())
    success = bu_sm.GetKExecutiveDetailsSuccess(res)
    return success


########################################################
'''
    returns statutory mapping uploaded csv list
   :param
        db: database object
        session_user: logged in user details
   :type
        db: Object
        session_user: Object

   :returns
        result: returns processed api response
        GetStatutoryMappingCsvUploadedListSuccess class Object
    rtype:
        result: Object
'''
########################################################


def get_statutory_mapping_csv_list(db, session_user):

    upload_more, csv_data = get_uploaded_statutory_mapping_csv_list(
        db, session_user.user_id()
    )
    result = bu_sm.GetStatutoryMappingCsvUploadedListSuccess(
        upload_more, csv_data
    )
    return result


def validate_data(
    request_frame, session_user, csv_name, s_header, s_smap_data
):
    def write_file():
        file_string = csv_name.split(".")
        file_name = "%s_%s.%s" % (
            file_string[0], "upload", "txt"
        )
        file_path = "%s/%s" % (BULKUPLOAD_INVALID_PATH, file_name)
        with open(file_path, "wb") as fn:
            fn.write(return_data)
            os.chmod(file_path, 0777)
        return
    try:
        header = pickle.loads(s_header)
        statutory_mapping_data = pickle.loads(s_smap_data)
        c_obj = ValidateStatutoryMappingCsvData(
            db, statutory_mapping_data, session_user,
            request_frame.c_id, request_frame.d_id,
            request_frame.csv_name, header
        )
        res_data = c_obj.perform_validation()
        return_data = None
        if res_data == "InvalidCSV":
            return_data = "InvalidCSV"

        elif res_data is None:
            raise RuntimeError("Invalid Csv File")

        elif res_data["return_status"] is True:
            generate_valid_file(csv_name)
            if res_data["doc_count"] == 0:
                upload_sts = 1
            else:
                upload_sts = 0

            csv_args = [
                session_user,
                request_frame.c_id, request_frame.c_name,
                request_frame.d_id,
                request_frame.d_name, csv_name,
                res_data["total"], res_data["doc_count"], upload_sts
            ]
            new_csv_id = save_mapping_csv(csv_args)

            # result = None

            if new_csv_id:
                if save_mapping_data(new_csv_id, res_data["data"]) is True:
                    if res_data["doc_count"] == 0:
                        c_obj.save_executive_message(
                            csv_name, request_frame.c_name,
                            request_frame.d_name, session_user
                        )
                        c_obj.source_commit()
                    return_data = bu_sm.UploadStatutoryMappingCSVValidSuccess(
                        new_csv_id, res_data["csv_name"],
                        res_data["total"], res_data["valid"],
                        res_data["invalid"],
                        res_data["doc_count"], res_data["doc_names"],
                        csv_name
                    ).to_structure()
                    return_data = json.dumps(return_data)
            # csv data save to temp db
        else:
            return_data = bu_sm.UploadStatutoryMappingCSVInvalidSuccess(
                res_data["invalid_file"], res_data["mandatory_error"],
                res_data["max_length_error"], res_data["duplicate_error"],
                res_data["invalid_char_error"], res_data["invalid_data_error"],
                res_data["inactive_error"], res_data["total"],
                res_data["invalid"],
                res_data["total"] - res_data["invalid"],
                res_data["invalid_frequency_error"]
            ).to_structure()
            return_data = json.dumps(return_data)
    except AssertionError as error:
        e = "AssertionError"
        return_data = json.dumps(e)
        write_file()
        logger.logKnowledge(
            "error",
            "bustatutorymappingcontroller.py - validate_data", e)
        raise error
    except Exception, e:
        return_data = json.dumps(str(e))
        write_file()
        logger.logKnowledge(
            "error",
            "bustatutorymappingcontroller.py - validate_data()", e)
        raise e
    write_file()
    print "os pid ---->>>", os.getpid()
    return


########################################################
'''
   save the file in csv folder after success full csv data validation
   :param
        db: database object
        request_frame: api request UploadStatutoryMappingCSV class object
        session_user: logged in user details
   :type
        db: Object
        request_frame: Object
        session_user: Object

   :returns
        result: return could be success class object or failure
         class objects also raise the exceptions
    rtype:
        result: Object
'''
########################################################


def upload_statutory_mapping_csv(db, request_frame, session_user):
    try:
        if request_frame.csv_size > 0:
            pass

        if get_rejected_sm_file_count(db, session_user) >= MAX_REJECTED_COUNT:
            return bu_sm.RejectionMaxCountReached()

        # save csv file
        csv_name = convert_base64_to_file(
            BULKUPLOAD_CSV_PATH, request_frame.csv_name, request_frame.csv_data
        )
        # read data from csv file
        header, statutory_mapping_data = read_data_from_csv(csv_name)

        if len(statutory_mapping_data) == 0:
            return bu_sm.CsvFileCannotBeBlank()

        if len(statutory_mapping_data) > CSV_MAX_LINES:
            file_path = "%s/csv/%s" % (BULKUPLOAD_CSV_PATH, csv_name)
            remove_uploaded_file(file_path)
            return bu_sm.CsvFileExeededMaxLines(CSV_MAX_LINES)

        s_header = pickle.dumps(header)
        s_smap_data = pickle.dumps(statutory_mapping_data)
        t = multiprocessing.Process(
            target=validate_data,
            args=(
                request_frame, session_user.user_id(),
                csv_name, s_header, s_smap_data
            )
        )
        t.start()
        print "Proces id========================================>", t.pid
        return bu_sm.Done(csv_name)
    except Exception, e:
        print e
        print str(traceback.format_exc())
        logger.logKnowledge(
            "error", "upload_statutory_mapping_csv",
            str(traceback.format_exc()))
        raise e


########################################################
# To Save Executives notification message to manager once
# documents are uploaded
########################################################


def save_executive_message_after_docupload(request_frame, session_user):
    try:
        c_obj = StatutorySource()
        c_obj.save_executive_message(
            request_frame.csv_name, request_frame.c_name,
            request_frame.d_name, session_user.user_id()
        )
        c_obj.source_commit()
        result = bu_sm.SendExecutiveMessageSuccess()
        return result

    except Exception, e:
        print e
        print str(traceback.format_exc())
        logger.logKnowledge(
            "error", "save_executive_message_after_docupload",
            str(traceback.format_exc()))
        raise e

########################################################
'''
    returns statutory mapping list for approve
   :param
        db: database object
        request_frame: api request GetApproveStatutoryMappingList class object
        session_user: logged in user details
   :type
        db: Object
        request_frame: Object
        session_user: Object
   :returns
        result: returns processed api response
        GetApproveStatutoryMappingListSuccess class Object
    rtype:
        result: Object
'''
########################################################


def get_mapping_list_for_approve(db, request_frame, session_user):

    pending_data = get_pending_mapping_list(
        db, request_frame.c_id, request_frame.d_id,
        request_frame.uploaded_by, session_user
    )
    result = bu_sm.GetApproveStatutoryMappingListSuccess(
        pending_data
    )
    return result


########################################################
'''
    returns filters for approve statutory mapping view
   :param
        db: database object
        request_frame: api request GetApproveMappingFilter class object
        session_user: logged in user details
   :type
        db: Object
        request_frame: Object
        session_user: Object
   :returns
        result: returns processed api response
        GetApproveMappingFilterSuccess class Object
    rtype:
        result: Object
'''
########################################################


def get_filter_for_approve_page(db, request_frame):
    csv_id = request_frame.csv_id
    response = get_filters_for_approve(db, csv_id)
    return response


def get_statutory_mapping_data_by_filter(db, request_frame):
    response = get_statutory_mapping_by_filter(db, request_frame)
    return response


def get_statutory_mapping_data_by_csvid(db, request_frame):
    response = get_statutory_mapping_by_csv_id(db, request_frame)
    return response


def update_statutory_mapping_action(db, request_frame, session_user):
    try:
        csv_id = request_frame.csv_id
        country_id = request_frame.c_id
        domain_id = request_frame.d_id

        c_obj = ValidateStatutoryMappingForApprove(
            db, csv_id, country_id, domain_id, session_user
        )
        t = multiprocessing.Process(
            target=statutory_validate_data,
            args=(db, request_frame, c_obj, session_user))
        t.start()
        print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!", t.pid
        return bu_sm.Done(c_obj._csv_name)
    except Exception, e:
        print e
        print str(traceback.format_exc())
        raise e


def queue_process_statutory_document(db, request_frame, session_user):
    csv_id = request_frame.csv_id
    action = request_frame.bu_action
    country_id = request_frame.c_id
    domain_id = request_frame.d_id
    rejected_reason = ""
    if action == 1:
        c_obj = ValidateStatutoryMappingForApprove(
            db, csv_id, country_id, domain_id, session_user
        )

        if c_obj._doc_count > 0:
            get_update_approve_file_status(csv_id, 3)
            if c_obj.format_download_process_initiate(csv_id):
                rejected_reason = "success"
            else:
                rejected_reason = "error"
        return bu_sm.DocumentQueueProcessSuccess(rejected_reason)


def statutory_validate_data(db, request_frame, c_obj, session_user):
    def write_file(return_data):
        csv_name = c_obj._csv_name
        file_string = csv_name.split(".")
        file_name = "%s_%s.%s" % (
            file_string[0], "approve", "txt"
        )
        file_path = "%s/%s" % (BULKUPLOAD_INVALID_PATH, file_name)
        with open(file_path, "wb") as fn:
            os.chmod(file_path, 0777)
            fn.write(return_data)

    try:
        return_data = None
        csv_name = c_obj._csv_name
        csv_id = request_frame.csv_id
        action = request_frame.bu_action
        remarks = request_frame.remarks
        if action == 1:
            is_declined = c_obj.perform_validation_before_submit()
            if len(is_declined.keys()) > 0:
                return_data = bu_sm.ValidationSuccess(
                    len(is_declined.keys())).to_structure()
            else:

                if (update_approve_action_from_list(csv_id, action, remarks, session_user, "all")):
                    if c_obj._doc_count > 0:
                        get_update_approve_file_status(csv_id, 3)
                        print "Download process init"
                        c_obj.format_download_process_initiate(csv_id)
                    else:
                        get_update_approve_file_status(csv_id, 1)

                    c_obj.frame_data_for_main_db_insert()
                    c_obj.save_manager_message(
                        action, c_obj._csv_name, c_obj._country_name,
                        c_obj._domain_name, session_user.user_id(),
                        None, 0
                    )
                    c_obj.source_commit()
                    delete_action_after_approval(csv_id)
                    remove_bulk_uploaded_files(csv_name)
                    return_data = bu_sm.UpdateApproveActionFromListSuccess().to_structure()
        else:
            if (update_approve_action_from_list(csv_id, action, remarks, session_user, "all")):
                get_update_approve_file_status(csv_id, 1)
                c_obj.save_manager_message(
                    action, c_obj._csv_name, c_obj._country_name,
                    c_obj._domain_name, session_user.user_id(), remarks, 0
                )
                c_obj.source_commit()
                return_data = bu_sm.UpdateApproveActionFromListSuccess().to_structure()
        return_data = json.dumps(return_data)

    except AssertionError as error:
        e = "AssertionError"
        return_data = json.dumps(e)
        write_file(return_data)
        logger.logKnowledge(
            "error",
            "bustatutorymappingcontroller.py - statutory_validate_data", e)
        raise error
    except Exception, e:
        return_data = json.dumps(str(e))
        write_file(return_data)
        logger.logKnowledge(
            "error",
            "bustatutorymappingcontroller.py - statutory_validate_data()", e)
        raise e
    write_file(return_data)
    return


def submit_statutory_mapping(db, request_frame, session_user):
    try:
        csv_id = request_frame.csv_id
        country_id = request_frame.c_id
        domain_id = request_frame.d_id
        # csv data validation
        if get_pending_action(db, csv_id):
            return bu_sm.Failure()

        c_obj = ValidateStatutoryMappingForApprove(
            db, csv_id, country_id, domain_id, session_user
        )
        t = multiprocessing.Process(
            target=submit_statutory_validate,
            args=(db, request_frame, c_obj, session_user))
        t.start()
        print "!!!!!!!!!!!!!!!!SUBMIT Statu mapping !!!!!!!!!!!!!!!!!", t.pid
        return bu_sm.Done(c_obj._csv_name)
    except Exception, e:
        print e
        print str(traceback.format_exc())
        raise e


def submit_statutory_validate(db, request_frame, c_obj, session_user):
    def write_file(return_data):
        return_data = json.dumps(return_data)
        file_string = csv_name.split(".")
        file_name = "%s_%s.%s" % (
            file_string[0], "approve", "txt"
        )
        file_path = "%s/%s" % (BULKUPLOAD_INVALID_PATH, file_name)
        with open(file_path, "wb") as fn:
            os.chmod(file_path, 0777)
            fn.write(return_data)

    try:
        is_declined = c_obj.perform_validation_before_submit()
        return_data = None

        csv_id = request_frame.csv_id
        csv_name = c_obj._csv_name

        if len(is_declined.keys()) > 0:
            return_data = bu_sm.ValidationSuccess(
                len(is_declined.keys())
            ).to_structure()
        else:
            update_approve_action_from_list(
                csv_id, 1, None, session_user, "single"
            )
            if c_obj._doc_count > 0:
                get_update_approve_file_status(csv_id, 3)
                c_obj.format_download_process_initiate(csv_id)
            else:
                get_update_approve_file_status(csv_id, 1)
            c_obj.save_manager_message(
                1, c_obj._csv_name, c_obj._country_name, c_obj._domain_name,
                session_user.user_id(), None, 0
            )
            c_obj.frame_data_for_main_db_insert()
            c_obj.source_commit()
            delete_action_after_approval(csv_id)
            remove_bulk_uploaded_files(csv_name)
            return_data = bu_sm.SubmitStatutoryMappingSuccess().to_structure()

    except AssertionError as error:
        e = "AssertionError"
        return_data = json.dumps(e)
        write_file(return_data)
        logger.logKnowledge(
            "error",
            "bustatutorymappingcontroller.py - submit_statutory_validate", e)
        raise error
    except Exception, e:
        return_data = json.dumps(str(e))
        write_file(return_data)
        logger.logKnowledge(
            "error",
            "bustatutorymappingcontroller.py - submit_statutory_validate()", e)
        raise e
    write_file(return_data)
    return


def confirm_submit_statutory_mapping(db, request_frame, session_user):
    try:
        csv_id = request_frame.csv_id
        country_id = request_frame.c_id
        domain_id = request_frame.d_id
        # csv data validation

        c_obj = ValidateStatutoryMappingForApprove(
            db, csv_id, country_id, domain_id, session_user
        )
        t = multiprocessing.Process(
            target=confirm_statutory_validate,
            args=(db, request_frame, c_obj, session_user))
        t.start()
        print "!!!!!!!!!!!!!!!Confirm Statu mapping !!!!!!!!!!!!!!!!!!", t.pid
        return bu_sm.Done(c_obj._csv_name)
    except Exception, e:
        raise e


def confirm_statutory_validate(db, request_frame, c_obj, session_user):
    def write_file(return_data):
        csv_name = c_obj._csv_name
        file_string = csv_name.split(".")
        file_name = "%s_%s.%s" % (
            file_string[0], "approve", "txt"
        )
        file_path = "%s/%s" % (BULKUPLOAD_INVALID_PATH, file_name)
        with open(file_path, "wb") as fn:
            os.chmod(file_path, 0777)
            fn.write(return_data)
        return

    try:
        is_declined = c_obj.perform_validation_before_submit()
        csv_id = request_frame.csv_id
        user_id = session_user.user_id()
        csv_name = c_obj._csv_name
        return_data = None

        if len(is_declined.keys()) > 0:
            rej_done = c_obj.make_rejection(is_declined, user_id)
            c_obj.save_manager_message(
                1, c_obj._csv_name, c_obj._country_name, c_obj._domain_name,
                user_id, None, len(is_declined.keys())
            )
            c_obj.frame_data_for_main_db_insert()
            c_obj.source_commit()
            delete_action_after_approval(csv_id)
            if c_obj._doc_count > 0 and rej_done:
                get_update_approve_file_status(csv_id, 3)
                c_obj.format_download_process_initiate(csv_id)
            else:
                get_update_approve_file_status(csv_id, 1)

            c_obj.source_bulkdb_commit()
            remove_bulk_uploaded_files(csv_name)
            return_data = bu_sm.SubmitStatutoryMappingSuccess().to_structure()

        return_data = json.dumps(return_data)

    except AssertionError as error:
        e = "AssertionError"
        return_data = json.dumps(e)
        write_file(return_data)
        logger.logKnowledge(
            "error",
            "bustatutorymappingcontroller.py - statutory_validate_data", e)
        raise error
    except Exception, e:
        return_data = json.dumps(str(e))
        write_file(return_data)
        logger.logKnowledge(
            "error",
            "bustatutorymappingcontroller.py - statutory_validate_data()", e)
        raise e
    write_file(return_data)
    return


def save_action(db, request_frame):
    try:
        save_action_from_view(
            db, request_frame.csv_id, request_frame.sm_id,
            request_frame.bu_action, request_frame.remarks
        )
        return bu_sm.SaveActionSuccess()

    except Exception, e:
        raise e

# transaction methods end


########################################################
'''
    returns statutory mapping bulk report data
   :param
        db: database object
        request_frame: api request GetSMBulkReportData class object
        session_user: logged in user details
   :type
        db: Object
        request_frame: Object
        session_user: Object
   :returns
        result: returns processed api response
        GetSMBulkReportDataSuccess class Object
    rtype:
        result: Object
'''
########################################################


def get_sm_bulk_report_data(db, request_frame, session_user):
    country_ids = request_frame.c_ids
    domain_ids = request_frame.d_ids
    from_date = request_frame.from_date
    to_date = request_frame.to_date
    record_count = request_frame.r_count
    page_count = request_frame.p_count
    child_ids = request_frame.child_ids

    user_id = session_user.user_id()

    from_date = datetime.datetime.strptime(from_date, '%d-%b-%Y')
    to_date = datetime.datetime.strptime(to_date, '%d-%b-%Y')
    reportdata, total_record = fetch_statutory_bulk_report(
        db, user_id, country_ids, domain_ids, from_date, to_date,
        record_count, page_count, child_ids
    )
    result = bu_sm.GetSMBulkReportDataSuccess(reportdata, total_record)
    return result


########################################################
'''
    returns only rejected statutory mapping bulk report data
   :param
        db: database object
        request_frame: api request GetRejectedSMBulkUploadData class object
        session_user: logged in user details
   :type
        db: Object
        request_frame: Object
        session_user: Object
   :returns
        result: returns processed api response
        RejectedSMBulkDataSuccess class Object
    rtype:
        result: Object
'''
########################################################


def get_rejected_sm_bulk_data(db, request_frame, session_user):
    country_id = request_frame.c_id
    domain_id = request_frame.d_id
    user_id = session_user.user_id()

    rejecteddata = fetch_rejected_statutory_mapping_bulk_report(
        db, user_id, country_id, domain_id
    )
    result = bu_sm.RejectedSMBulkDataSuccess(rejecteddata)
    return result


########################################################
'''
    Delete Rejected Statutory Mapping for requested CSV Id
    returns Rejected Statutory Mapping
   :param
        db: database object
        request_frame: api request DeleteRejectedSMCsvId class object
        session_user: logged in user details
   :type
        db: Object
        request_frame: Object
        session_user: Object
   :returns
        result: returns processed api response
        RejectedSMBulkDataSuccess class Object
    rtype:
        result: Object
'''
########################################################


def delete_rejected_sm_csv_id(db, request_frame, session_user):

    country_id = request_frame.c_id
    domain_id = request_frame.d_id
    csv_id = request_frame.csv_id
    user_id = session_user.user_id()
    document_count = get_sm_document_count(db, csv_id)
    csv_name = get_sm_csv_name(db, csv_id)
    c_obj = ValidateStatutoryMappingForApprove(db, csv_id, country_id,
                                               domain_id, session_user)
    if document_count > 0:
        c_obj.temp_server_folder_remove_call(csv_id)

    rejected_data = process_delete_rejected_sm_csv_id(
        db, user_id, country_id, domain_id, csv_id
    )
    remove_bulk_uploaded_files(csv_name)
    result = bu_sm.RejectedSMBulkDataSuccess(rejected_data)
    return result


# Update User Download Count for Rejected Statutory Mapping
def update_rejected_sm_download_count(db, request_frame):
    csv_id = request_frame.csv_id
    updated_count = update_download_count_by_csvid(db, csv_id)
    result = bu_sm.SMRejecteUpdatedDownloadCountSuccess(updated_count)
    return result


########################################################
# To Export the Statutory Bulk Report Data
########################################################
def export_statutory_bulk_report(db, request, session_user):
    if request.csv:
        converter = ConvertJsonToCSV(
            db, request, session_user, "ExportSMBulkReport"
        )
        if converter.FILE_DOWNLOAD_PATH is None:
            return technoreports.ExportToCSVEmpty()
        else:
            return generalprotocol.ExportToCSVSuccess(
                link=converter.FILE_DOWNLOAD_PATH
            )


#############################################################
# Dowload Rejected Statutory Mapping Data For Request CSV id
#############################################################

def download_rejected_sm_report(db, request_frame, session_user):
    csv_id = request_frame.csv_id
    country_id = request_frame.c_id
    domain_id = request_frame.d_id
    download_format = request_frame.download_format
    user_id = session_user.user_id()

    sheet_name = "Rejected Statutory Mapping"

    csv_header_key = ["organization", "geography_location", "statutory_nature",
                      "statutory", "statutory_provision", "compliance_task",
                      "compliance_document", "task_id",
                      "compliance_description", "penal_consequences",
                      "task_Type", "reference_link", "compliance_frequency",
                      "statutory_month", "statutory_date", "trigger_before",
                      "repeats_every", "repeats_type", "repeat_by",
                      "duration", "duration_type", "multiple_input",
                      "format_file", "remarks", "rejected_reason",
                      "is_fully_rejected"]

    csv_column_name = ["Organization*", "Applicable_Location*",
                       "Statutory_Nature*", "Statutory*",
                       "Statutory_Provision*", "Compliance_Task*",
                       "Compliance_Document",
                       "Task_ID*", "Compliance_Description*",
                       "Penal_Consequences", "Task_Type*",
                       "Reference_Link", "Compliance_Frequency*",
                       "Statutory_Month", "Statutory_Date",
                       "Trigger_Days", "Repeats_Every",
                       "Repeats_Type", "Repeats_By (DOM/EOM)",
                       "Duration", "Duration_Type",
                       "Multiple_Input_Selection", "Format",
                       "Error_Description"]

    csv_name = get_sm_csv_file_name_by_id(db, csv_id)
    source_data = fetch_rejected_sm_download_csv_report(
        db, user_id, country_id, domain_id, csv_id
    )
    c_obj = ValidateRejectedDownloadBulkData(
        db, source_data, session_user, download_format, csv_name,
        csv_header_key, csv_column_name, sheet_name)
    result = c_obj.perform_validation()
    return bu_sm.DownloadActionSuccess(
        result["xlsx_link"],
        result["csv_link"],
        result["ods_link"],
        result["txt_link"])


def process_get_status(request):
    csv_name = request.csv_name
    file_string = csv_name.split(".")
    file_name = "%s_%s.%s" % (
        file_string[0], "upload", "txt"
    )
    file_path = "%s/%s" % (BULKUPLOAD_INVALID_PATH, file_name)
    if os.path.exists(file_path) is False:
        return bu_sm.Alive()
    else:
        return_data = ""
        with open(file_path, "r") as fn:
            return_data += fn.read()
        remove_uploaded_file(file_path)
        if return_data == "InvalidCSV":
            return bu_sm.InvalidCsvFile()
        else:
            result = json.loads(return_data)
            if str(result[0]) == "UploadStatutoryMappingCSVValidSuccess":
                return bu_sm.UploadStatutoryMappingCSVValidSuccess.parse_inner_structure(result[1])
            elif str(result[0]) == "UploadStatutoryMappingCSVInvalidSuccess":
                return bu_sm.UploadStatutoryMappingCSVInvalidSuccess.parse_inner_structure(result[1])
            else:
                logger.logKnowledge(
                    "error",
                    "bustatutorymappingcontroller.py-process_get_status",
                    result
                )
                raise Exception(str(result))


def process_get_approve_mapping_status(request):
    csv_name = request.csv_name
    file_string = csv_name.split(".")
    file_name = "%s_%s.%s" % (
        file_string[0], "approve", "txt"
    )
    file_path = "%s/%s" % (BULKUPLOAD_INVALID_PATH, file_name)
    if os.path.exists(file_path) is False:
        return bu_sm.Alive()
    else:
        return_data = ""
        with open(file_path, "r") as fn:
            return_data += fn.read()
        remove_uploaded_file(file_path)
        result = json.loads(return_data)
        if str(result[0]) == "UpdateApproveActionFromListSuccess":
            return bu_sm.UpdateApproveActionFromListSuccess.parse_inner_structure(result[1])
        elif str(result[0]) == "ValidationSuccess":
            return bu_sm.ValidationSuccess.parse_inner_structure(
                result[1])
        elif str(result[0]) == "SubmitStatutoryMappingSuccess":
            return bu_sm.SubmitStatutoryMappingSuccess.parse_inner_structure(
                result[1])
        else:
            log_param = "bustatutorymappingcontroller.py-" + \
                "process_get_approve_mapping_status"
            logger.logKnowledge("error", log_param, result)
            raise Exception(str(result))
