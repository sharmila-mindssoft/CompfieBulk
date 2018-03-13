import traceback
from ..bucsvvalidation.statutorymappingvalidation import (
    ValidateStatutoryMappingCsvData,
    ValidateStatutoryMappingForApprove
)
from ..bucsvvalidation.rejectedstatutorymapping import ValidateRejectedSMBulkCsvData
from ..buapiprotocol import bustatutorymappingprotocol as bu_sm
from ..budatabase.bustatutorymappingdb import *
from ..bulkuploadcommon import (
    convert_base64_to_file,
    read_data_from_csv,
    generate_valid_file
)
from ..bulkexport import ConvertJsonToCSV
import datetime
from server.constants import BULKUPLOAD_CSV_PATH
from server.exceptionmessage import fetch_error, fetch_run_error
# from protocol import core, generalprotocol, technoreports
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

    if type(request_frame) is bu_sm.GetStatutoryMappingCsvUploadedList:
        result = get_statutory_mapping_csv_list(db, request_frame,
                                                session_user)

    if type(request_frame) is bu_sm.UploadStatutoryMappingCSV:
        result = upload_statutory_mapping_csv(db, request_frame, session_user)

    if type(request_frame) is bu_sm.GetBulkReportData:
        result = get_statutory_bulk_report_data(db, request_frame,
                                                session_user)

    if type(request_frame) is bu_sm.GetRejectedStatutoryMappingBulkUploadData:
        result = get_rejected_statutory_bulk_upload_data(db, request_frame,
                                                         session_user)

    if type(request_frame) is bu_sm.DeleteRejectedStatutoryMappingDataByCsvID:
        result = delete_rejected_statutory_data_by_csv_id(db,
                                                          request_frame,
                                                          session_user)

    if type(request_frame) is bu_sm.UpdateDownloadCountToRejectedStatutory:
        result = update_rejected_sm_download_count(
            db, request_frame, session_user
        )

    if type(request_frame) is bu_sm.GetApproveStatutoryMappingList:
        result = get_mapping_list_for_approve(db, request_frame, session_user)

    if type(request_frame) is bu_sm.UpdateApproveActionFromList:
        result = update_statutory_mapping_action(db, request_frame,
                                                 session_user)

    if type(request_frame) is bu_sm.GetApproveStatutoryMappingView:
        result = get_statutory_mapping_data_by_csvid(db, request_frame, session_user)

    if type(request_frame) is bu_sm.ExportSMBulkReportData:
        result = export_statutory_bulk_report(db, request_frame, session_user)

    if type(request_frame) is bu_sm.DownloadRejectedSMReportData:
        result = download_rejected_sm_report(db, request_frame, session_user)

    if type(request_frame) is bu_sm.SaveAction:
        result = save_action(db, request_frame, session_user)

    if type(request_frame) is bu_sm.GetApproveMappingFilter:
        result = get_filter_for_approve_page(db, request_frame, session_user)

    if type(request_frame) is bu_sm.GetApproveStatutoryMappingViewFilter:
        result = get_statutory_mapping_data_by_filter(db, request_frame, session_user)

    if type(request_frame) is bu_sm.SubmitStatutoryMapping:
        result = submit_statutory_mapping(db, request_frame, session_user)

    if type(request_frame) is bu_sm.ConfirmStatutoryMappingSubmit:
        result = confirm_submit_statutory_mapping(db, request_frame, session_user)

    return result

# transaction methods begin

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
        result: returns processed api response GetStatutoryMappingCsvUploadedListSuccess class Object
    rtype:
        result: Object
'''
########################################################

def get_statutory_mapping_csv_list(db, request_frame, session_user):

    upload_more, csv_data = get_uploaded_statutory_mapping_csv_list(db, session_user.user_id())
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
        result: return could be success class object or failure class objects also raise the exceptions
    rtype:
        result: Object
'''
########################################################

def upload_statutory_mapping_csv(db, request_frame, session_user):
    if request_frame.csv_size > 0 :
        pass
    # save csv file
    csv_name = convert_base64_to_file(
            BULKUPLOAD_CSV_PATH, request_frame.csv_name,
            request_frame.csv_data
        )
    # read data from csv file
    header, statutory_mapping_data = read_data_from_csv(csv_name)

    # csv data validation
    cObj = ValidateStatutoryMappingCsvData(
        db, statutory_mapping_data, session_user, request_frame.c_id, request_frame.d_id,
        request_frame.csv_name, header
    )
    res_data = cObj.perform_validation()

    if res_data["return_status"] is True :
        generate_valid_file(csv_name)
        if res_data["doc_count"] == 0 :
            upload_sts = 1
        else :
            upload_sts = 0

        csv_args = [
            session_user.user_id(),
            request_frame.c_id, request_frame.c_name,
            request_frame.d_id,
            request_frame.d_name, csv_name,
            res_data["total"], res_data["doc_count"], upload_sts
        ]
        new_csv_id = save_mapping_csv(db, csv_args)

        if new_csv_id :
            if save_mapping_data(db, new_csv_id, res_data["data"]) is True :
                cObj.save_executive_message(csv_name, request_frame.c_name, request_frame.d_name, session_user.user_id())
                result = bu_sm.UploadStatutoryMappingCSVValidSuccess(
                    res_data["total"], res_data["valid"], res_data["invalid"],
                    res_data["doc_count"], res_data["doc_names"]
                )

        # csv data save to temp db
    else :
        result = bu_sm.UploadStatutoryMappingCSVInvalidSuccess(
            res_data["invalid_file"], res_data["mandatory_error"],
            res_data["max_length_error"], res_data["duplicate_error"],
            res_data["invalid_char_error"], res_data["invalid_data_error"],
            res_data["inactive_error"], res_data["total"], res_data["invalid"],
            res_data["total"] - res_data["invalid"]
        )

    return result

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
        result: returns processed api response GetApproveStatutoryMappingListSuccess class Object
    rtype:
        result: Object
'''
########################################################
def get_mapping_list_for_approve(db, request_frame, session_user):

    pending_data = get_pending_mapping_list(db, request_frame.c_id, request_frame.d_id, request_frame.uploaded_by)
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
        result: returns processed api response GetApproveMappingFilterSuccess class Object
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
    try :
        cObj = ValidateStatutoryMappingForApprove(
            db, csv_id, country_id, domain_id, session_user
        )
        if action == 1 :
            print "Object init"
            is_declined = cObj.perform_validation_before_submit()
            print "After validation"
            print is_declined
            if len(is_declined) > 0 :
                return bu_sm.ValidationSuccess(is_declined)
            else :
                if (update_approve_action_from_list(db, csv_id, action, remarks, session_user)) :
                    print "after temp db update"
                    cObj.frame_data_for_main_db_insert()
                    cObj.save_manager_message(action, cObj._csv_name, cObj._country_name, cObj._domain_name, session_user.user_id())
                    cObj.source_commit()
                    return bu_sm.UpdateApproveActionFromListSuccess()
        else :
            if (update_approve_action_from_list(db, csv_id, action, remarks, session_user)) :
                cObj.save_manager_message(action, cObj._csv_name, cObj._country_name, cObj._domain_name, session_user.user_id())
                cObj.source_commit()
                return bu_sm.UpdateApproveActionFromListSuccess()

    except Exception, e:
        raise e


def submit_statutory_mapping(db, request_frame, session_user):
    try :
        csv_id = request_frame.csv_id
        country_id = request_frame.c_id
        domain_id = request_frame.d_id
        # csv data validation
        if get_pending_action(db, csv_id):
            raise fetch_run_error("Some records action pending, Complete action before submmit")

        cObj = ValidateStatutoryMappingForApprove(
            db, csv_id, country_id, domain_id, session_user
        )
        is_declined = cObj.perform_validation_before_submit()
        if len(is_declined) > 0 :
            return bu_sm.ValidationSuccess(is_declined)
        else :

            cObj.save_manager_message(
                1, cObj._csv_name, cObj._country_name, cObj._domain_name,
                session_user.user_id()
            )
            cObj.frame_data_for_main_db_insert()
            cObj.source_commit()
            update_approve_action_from_list(db, csv_id, 1, None, session_user)
            return bu_sm.SubmitStatutoryMappingSuccess()
    except Exception, e:
        print e
        print str(traceback.format_exc())
        raise fetch_error()

def confirm_submit_statutory_mapping(db, request_frame, session_user):
    csv_id = request_frame.csv_id
    country_id = request_frame.c_id
    domain_id = request_frame.d_id
    # csv data validation
    cObj = ValidateStatutoryMappingForApprove(
        db, csv_id, country_id, domain_id, session_user
    )
    is_declined = cObj.perform_validation_before_submit()
    if len(is_declined) > 0 :
        cObj.frame_data_for_main_db_insert()
        cObj.make_rejection(is_declined)
        cObj.save_manager_message(1, cObj._csv_name, cObj._country_name, cObj._domain_name, session_user.user_id())
        return bu_sm.SubmitStatutoryMappingSuccess()

def save_action(db, request_frame, session_user):
    try :
        save_action_from_view(
            db, request_frame.csv_id, request_frame.sm_id,
            request_frame.bu_action, request_frame.remarks,
            session_user
        )
        return bu_sm.SaveActionSuccess()

    except Exception, e :
        raise e

# transaction methods end







######## REport methods
def get_statutory_bulk_report_data(db, request_frame, session_user):

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
    reportdata, total_record = fetch_statutory_bulk_report(db, session_user,
    user_id, country_ids, domain_ids, from_date, to_date, record_count,
    page_count, child_ids, user_category_id)    # reportdata=result[0]
    # total_record=result[1]
    result = bu_sm.GetBulkReportDataSuccess(reportdata,total_record)
    return result

def get_rejected_statutory_bulk_upload_data(db, request_frame, session_user):
    country_id=request_frame.c_id
    domain_id=request_frame.d_id
    user_id=session_user.user_id()

    rejecteddata = fetch_rejected_statutory_mapping_bulk_report(db, session_user, user_id,
        country_id, domain_id)
    result = bu_sm.GetRejectedStatutoryMappingBulkUploadDataSuccess(rejecteddata)
    return result

def delete_rejected_statutory_data_by_csv_id(db, request_frame, session_user):

    country_id=request_frame.c_id
    domain_id=request_frame.d_id
    csv_id=request_frame.csv_id

    user_id=session_user.user_id()

    rejected_data = get_list_and_delete_rejected_statutory_mapping_by_csv_id(db, session_user, user_id,
        country_id, domain_id, csv_id)
    result = bu_sm.GetRejectedStatutoryMappingBulkUploadDataSuccess(rejected_data)
    return result
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
        result: returns processed api response GetApproveStatutoryMappingListSuccess class Object
    rtype:
        result: Object
'''
########################################################
def delete_rejected_sm_data(db, request_frame, session_user):


    client_id=request_frame.client_id
    le_id=request_frame.le_id
    domain_ids=request_frame.domain_ids
    unit_code=request_frame.asm_unit_code
    csv_id=request_frame.csv_id
    user_id=session_user.user_id()

    rejected_data = get_list_and_delete_rejected_asm(db, session_user, user_id,
        client_id, le_id, domain_ids, unit_code, csv_id)
    result = bu_sm.GetRejectedASMDataSuccess(rejected_data)
    return result

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
        result: returns processed api response GetApproveStatutoryMappingListSuccess class Object
    rtype:
        result: Object
'''
########################################################


def update_rejected_sm_download_count(db, request_frame, session_user):

    csv_id=request_frame.csv_id

    user_id=session_user.user_id()

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

########################################################
# To retrieve all the audit trails of the given User
########################################################
# def process_statutory_bulk_report(db, request, session_user):
#     if request.csv:
#         converter = ConvertJsonToCSV(
#             db, request, session_user, "StatutoryMappingBulkReport"
#         )
#         if converter.FILE_DOWNLOAD_PATH is None:
#             return technoreports.ExportToCSVEmpty()
#         else:
#             return generalprotocol.ExportToCSVSuccess(
#                 link=converter.FILE_DOWNLOAD_PATH
#             )

def get_mapping_list_for_approve(db, request_frame, session_user):

    pending_data = get_pending_mapping_list(db, request_frame.c_id, request_frame.d_id, request_frame.uploaded_by)
    result = bu_sm.GetApproveStatutoryMappingListSuccess(
        pending_data
    )
    return result


########################################################
'''
   save the file in csv folder after success full csv data validation
    :param
        db: database object
        request_frame: api request RejectedStatutoryMappingCSV class object
        session_user: logged in user details
    :type
        db: Object
        request_frame: Object
        session_user: Object
    :returns
        result: return could be success class object or failure class objects
        also raise the exceptions
    rtype:
        result: Object
'''
########################################################


def download_rejected_sm_report(db, request_frame, session_user):
    csv_id = request_frame.csv_id
    country_id = request_frame.c_id
    domain_id = request_frame.d_id
    download_format = request_frame.download_format
    user_id = session_user.user_id()

    download_link = []
    csv_header=[
            "csv_name",
            "uploaded_by",
            "uploaded_on",
            "total_records",
            "total_rejected_records",
            "approved_by",
            "rejected_by",
            "approved_on",
            "rejected_on",
            "is_fully_rejected",
            "approve_status"
        ]

    csv_name = get_sm_csv_file_name_by_id(db, session_user, user_id, csv_id)
    source_data = fetch_rejected_sm_download_csv_report(
        db, session_user, user_id,
        country_id, domain_id, csv_id)

    cObj = ValidateRejectedSMBulkCsvData(
        db, source_data, session_user, download_format, csv_name, csv_header
    )
    result = cObj.perform_validation()

    return bu_sm.DownloadActionSuccess(
        result["xlsx_link"],
        result["csv_link"],
        result["ods_link"],
        result["txt_link"])
