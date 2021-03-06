import traceback
from ..bucsvvalidation.statutorymappingvalidation import (
    ValidateStatutoryMappingCsvData,
    ValidateStatutoryMappingForApprove
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
    get_countries_for_user_bu, get_knowledge_executive_bu
)

from ..bulkuploadcommon import (
    convert_base64_to_file, read_data_from_csv,
    generate_valid_file, remove_uploaded_file
)
from ..bulkexport import ConvertJsonToCSV
import datetime
from ..bulkconstants import (
    BULKUPLOAD_CSV_PATH, CSV_MAX_LINES, MAX_REJECTED_COUNT
)
# from server.exceptionmessage import fetch_run_error

from protocol import generalprotocol, technoreports

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


def process_bu_statutory_mapping_request(request, db, session_user):
    request_frame = request.request

    if type(request_frame) is bu_sm.GetDomains:
        result = process_get_domains_bu(db, session_user)

    if type(request_frame) is bu_sm.GetKExecutiveDetails:
        result = process_get_know_users_bu(db, session_user)

    if type(request_frame) is bu_sm.GetStatutoryMappingCsvUploadedList:
        result = get_statutory_mapping_csv_list(db, request_frame,
                                                session_user)

    if type(request_frame) is bu_sm.UploadStatutoryMappingCSV:
        result = upload_statutory_mapping_csv(db, request_frame, session_user)

    if type(request_frame) is bu_sm.GetSMBulkReportData:
        result = get_sm_bulk_report_data(db, request_frame, session_user)

    if type(request_frame) is bu_sm.GetRejectedSMBulkUploadData:
        result = get_rejected_sm_bulk_data(db, request_frame, session_user)

    if type(request_frame) is bu_sm.DeleteRejectedSMCsvId:
        result = delete_rejected_sm_csv_id(db, request_frame, session_user)

    if type(request_frame) is bu_sm.UpdateDownloadCountToRejectedStatutory:
        result = update_rejected_sm_download_count(db, request_frame,
                                                   session_user)

    if type(request_frame) is bu_sm.GetApproveStatutoryMappingList:
        result = get_mapping_list_for_approve(db, request_frame, session_user)

    if type(request_frame) is bu_sm.UpdateApproveActionFromList:
        result = update_statutory_mapping_action(db, request_frame,
                                                 session_user)

    if type(request_frame) is bu_sm.GetApproveStatutoryMappingView:
        result = get_statutory_mapping_data_by_csvid(
            db, request_frame, session_user
        )

    if type(request_frame) is bu_sm.ExportSMBulkReportData:
        result = export_statutory_bulk_report(db, request_frame, session_user)

    if type(request_frame) is bu_sm.DownloadRejectedSMReportData:
        result = download_rejected_sm_report(db, request_frame, session_user)

    if type(request_frame) is bu_sm.SaveAction:
        result = save_action(db, request_frame, session_user)

    if type(request_frame) is bu_sm.GetApproveMappingFilter:
        result = get_filter_for_approve_page(db, request_frame, session_user)

    if type(request_frame) is bu_sm.GetApproveStatutoryMappingViewFilter:
        result = get_statutory_mapping_data_by_filter(
            db, request_frame, session_user
        )

    if type(request_frame) is bu_sm.SubmitStatutoryMapping:
        result = submit_statutory_mapping(db, request_frame, session_user)

    if type(request_frame) is bu_sm.ConfirmStatutoryMappingSubmit:
        result = confirm_submit_statutory_mapping(
            db, request_frame, session_user
        )

    return result

# transaction methods begin

########################################################
# To get list of all domains
########################################################


def process_get_domains_bu(db, session_user):
    domains = get_domains_for_user_bu(db, 0)
    countries = get_countries_for_user_bu(db, session_user.user_id())
    success = bu_sm.GetDomainsSuccess(domains, countries)
    return success


########################################################
# To get list of knowledge executive details
########################################################
def process_get_know_users_bu(db, session_user):

    res = get_knowledge_executive_bu(db, session_user.user_id())
    success = bu_sm.GetKExecutiveDetailsSuccess(res)
    return success


########################################################
'''
    returns statutory mapping uploaded csv list
   :param
        db: database object
    request_frame: api request GetStatutoryMappingCsvUploadedList class object
        session_user: logged in user details
   :type
        db: Object
        request_frame: Object
        session_user: Object

   :returns
        result: returns processed api response
        GetStatutoryMappingCsvUploadedListSuccess class Object
    rtype:
        result: Object
'''
########################################################


def get_statutory_mapping_csv_list(db, request_frame, session_user):

    upload_more, csv_data = get_uploaded_statutory_mapping_csv_list(
        db, session_user.user_id()
    )
    result = bu_sm.GetStatutoryMappingCsvUploadedListSuccess(
        upload_more, csv_data
    )
    return result

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
        print "CSV NAME--->>> ", csv_name
        # read data from csv file
        header, statutory_mapping_data = read_data_from_csv(csv_name)

        if len(statutory_mapping_data) == 0:
            return bu_sm.CsvFileCannotBeBlank()

        if len(statutory_mapping_data) > CSV_MAX_LINES:
            file_path = "%s/csv/%s" % (BULKUPLOAD_CSV_PATH, csv_name)
            remove_uploaded_file(file_path)
            return bu_sm.CsvFileExeededMaxLines(CSV_MAX_LINES)

        # csv data validation
        cObj = ValidateStatutoryMappingCsvData(
            db, statutory_mapping_data, session_user,
            request_frame.c_id, request_frame.d_id,
            request_frame.csv_name, header
        )
        print "cObj", cObj
        res_data = cObj.perform_validation()
        print "Res Data ->", res_data

        if res_data == "InvalidCSV":
            print "in res data"
            return bu_sm.InvalidCsvFile()

        if res_data is None:
            raise RuntimeError("Invalid Csv File")

        if res_data["return_status"] is True:
            generate_valid_file(csv_name)
            if res_data["doc_count"] == 0:
                upload_sts = 1
            else:
                upload_sts = 0

            csv_args = [
                session_user.user_id(),
                request_frame.c_id, request_frame.c_name,
                request_frame.d_id,
                request_frame.d_name, csv_name,
                res_data["total"], res_data["doc_count"], upload_sts
            ]
            new_csv_id = save_mapping_csv(db, csv_args)

            if new_csv_id:
                if save_mapping_data(db, new_csv_id, res_data["data"]) is True:
                    cObj.save_executive_message(
                        csv_name, request_frame.c_name,
                        request_frame.d_name, session_user.user_id()
                    )
                    cObj.source_commit()
                    result = bu_sm.UploadStatutoryMappingCSVValidSuccess(
                        new_csv_id, res_data["csv_name"],
                        res_data["total"], res_data["valid"],
                        res_data["invalid"],
                        res_data["doc_count"], res_data["doc_names"],
                        csv_name
                    )

            # csv data save to temp db
        else:
            result = bu_sm.UploadStatutoryMappingCSVInvalidSuccess(
                res_data["invalid_file"], res_data["mandatory_error"],
                res_data["max_length_error"], res_data["duplicate_error"],
                res_data["invalid_char_error"], res_data["invalid_data_error"],
                res_data["inactive_error"], res_data["total"],
                res_data["invalid"],
                res_data["total"] - res_data["invalid"],
                res_data["invalid_frequency_error"]
            )

        return result
    except Exception, e:
        print e
        print str(traceback.format_exc())
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


def get_filter_for_approve_page(db, request_frame, session_user):
    csv_id = request_frame.csv_id
    response = get_filters_for_approve(db, csv_id)
    return response


def get_statutory_mapping_data_by_filter(db, request_frame, session_user):
    response = get_statutory_mapping_by_filter(db, request_frame, session_user)
    return response


def get_statutory_mapping_data_by_csvid(db, request_frame, session_user):
    response = get_statutory_mapping_by_csv_id(db, request_frame, session_user)
    return response


def update_statutory_mapping_action(db, request_frame, session_user):
    csv_id = request_frame.csv_id
    action = request_frame.bu_action
    remarks = request_frame.remarks
    country_id = request_frame.c_id
    domain_id = request_frame.d_id
    try:
        cObj = ValidateStatutoryMappingForApprove(
            db, csv_id, country_id, domain_id, session_user
        )
        print "cObj-> ", cObj
        print "action -> ", action
        if action == 1:
            is_declined = cObj.perform_validation_before_submit()
            print "is Declined --->> ", is_declined
            if len(is_declined.keys()) > 0:
                # update_approve_action_from_list(
                #     db, csv_id, action, remarks, session_user, "all"
                # )
                return bu_sm.ValidationSuccess(len(is_declined.keys()))
            else:
                if (update_approve_action_from_list(
                        db, csv_id, action, remarks, session_user, "all"
                )):
                    if cObj._doc_count > 0:
                        cObj.format_download_process_initiate(csv_id)
                    cObj.frame_data_for_main_db_insert()
                    cObj.save_manager_message(
                        action, cObj._csv_name, cObj._country_name,
                        cObj._domain_name, session_user.user_id(),
                        None, 0
                    )
                    cObj.source_commit()
                    delete_action_after_approval(db, csv_id)
                    return bu_sm.UpdateApproveActionFromListSuccess()
        else:
            if (update_approve_action_from_list(
                db, csv_id, action, remarks, session_user, "all"
            )):
                cObj.save_manager_message(
                    action, cObj._csv_name, cObj._country_name,
                    cObj._domain_name, session_user.user_id(), remarks, 0
                )
                cObj.source_commit()
                # print "DB Comitted >>"
                # cObj.source_bulkdb_commit()
                # if cObj._doc_count > 0:
                #     print "inside if"
                #     cObj.format_download_process_initiate(csv_id)
                return bu_sm.UpdateApproveActionFromListSuccess()

    except Exception, e:
        raise e


def submit_statutory_mapping(db, request_frame, session_user):
    try:
        csv_id = request_frame.csv_id
        country_id = request_frame.c_id
        domain_id = request_frame.d_id
        # csv data validation
        if get_pending_action(db, csv_id):
            raise RuntimeError(
                "All compliance should be selected before submit"
            )

        cObj = ValidateStatutoryMappingForApprove(
            db, csv_id, country_id, domain_id, session_user
        )
        is_declined = cObj.perform_validation_before_submit()
        if len(is_declined.keys()) > 0:
            return bu_sm.ValidationSuccess(len(is_declined.keys()))
        else:
            update_approve_action_from_list(
                db, csv_id, 1, None, session_user, "single"
            )
            if cObj._doc_count > 0:
                cObj.format_download_process_initiate(csv_id)
            cObj.save_manager_message(
                1, cObj._csv_name, cObj._country_name, cObj._domain_name,
                session_user.user_id(), None, 0
            )
            cObj.frame_data_for_main_db_insert()
            cObj.source_commit()

            delete_action_after_approval(db, csv_id)

            return bu_sm.SubmitStatutoryMappingSuccess()
    except Exception, e:
        print e
        print str(traceback.format_exc())
        raise e


def confirm_submit_statutory_mapping(db, request_frame, session_user):
    try:
        print "Confirm Submit "
        print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
        csv_id = request_frame.csv_id
        country_id = request_frame.c_id
        domain_id = request_frame.d_id
        user_id = session_user.user_id()
        # csv data validation
        cObj = ValidateStatutoryMappingForApprove(
            db, csv_id, country_id, domain_id, session_user
        )
        print "cObj- > > ", cObj
        is_declined = cObj.perform_validation_before_submit()
        print "is declined -> ", is_declined
        if len(is_declined.keys()) > 0:
            rej_done = cObj.make_rejection(is_declined, user_id)
            print "Rej Done->> ", rej_done
            cObj.save_manager_message(
                1, cObj._csv_name, cObj._country_name, cObj._domain_name,
                session_user.user_id(), None, len(is_declined.keys())
            )
            cObj.frame_data_for_main_db_insert()
            cObj.source_commit()
            delete_action_after_approval(db, csv_id)
            if cObj._doc_count > 0 and rej_done:
                cObj.format_download_process_initiate(csv_id)

            cObj.source_bulkdb_commit()
            return bu_sm.SubmitStatutoryMappingSuccess()
    except Exception, e:
        raise e


def save_action(db, request_frame, session_user):
    try:
        save_action_from_view(
            db, request_frame.csv_id, request_frame.sm_id,
            request_frame.bu_action, request_frame.remarks,
            session_user
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
    user_category_id = request_frame.user_category_id

    user_id = session_user.user_id()

    from_date = datetime.datetime.strptime(from_date, '%d-%b-%Y')
    to_date = datetime.datetime.strptime(to_date, '%d-%b-%Y')
    reportdata, total_record = fetch_statutory_bulk_report(
        db, session_user, user_id, country_ids, domain_ids, from_date,
        to_date, record_count, page_count, child_ids, user_category_id
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
        db, session_user, user_id, country_id, domain_id
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
    rejected_data = process_delete_rejected_sm_csv_id(
        db, session_user, user_id, country_id, domain_id, csv_id
    )
    result = bu_sm.RejectedSMBulkDataSuccess(rejected_data)
    return result


# Update User Download Count for Rejected Statutory Mapping
def update_rejected_sm_download_count(db, request_frame, session_user):
    csv_id = request_frame.csv_id
    updated_count = update_download_count_by_csvid(db, session_user, csv_id)
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
                       "Multiple_Input_Section", "Format",
                       "Error_Description"]

    csv_name = get_sm_csv_file_name_by_id(db, session_user, user_id, csv_id)
    source_data = fetch_rejected_sm_download_csv_report(
        db, session_user, user_id, country_id, domain_id, csv_id
    )
    cObj = ValidateRejectedDownloadBulkData(
        db, source_data, session_user, download_format, csv_name,
        csv_header_key, csv_column_name, sheet_name)
    result = cObj.perform_validation()
    return bu_sm.DownloadActionSuccess(
        result["xlsx_link"],
        result["csv_link"],
        result["ods_link"],
        result["txt_link"])
