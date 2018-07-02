import traceback
import threading
import time
import json
import os
from server import logger
from ..bucsvvalidation.assignstatutoryvalidation import (
    ValidateAssignStatutoryCsvData, ValidateAssignStatutoryForApprove
)
from ..bucsvvalidation.rejecteddownloadvalidation import (
    ValidateRejectedDownloadBulkData
)
from ..buapiprotocol import buassignstatutoryprotocol as bu_as
from ..buapiprotocol import bustatutorymappingprotocol as bu_sm
from ..budatabase.buassignstatutorydb import *
from ..bulkuploadcommon import (
    convert_base64_to_file,
    read_data_from_csv,
    generate_valid_file,
    remove_uploaded_file,
    generate_random_string
)
from ..bulkexport import ConvertJsonToCSV

from bulkupload.bulkconstants import (
    BULKUPLOAD_CSV_PATH, MAX_REJECTED_COUNT, CSV_MAX_LINES,
    SYSTEM_REJECTED_BY, REJECTED_FILE_DOWNLOADCOUNT,
    BULKUPLOAD_INVALID_PATH
)

import datetime
from protocol import generalprotocol, technoreports
__all__ = [
    "process_bu_assign_statutory_request"
]
########################################################
'''
    Process all assign statutory request here
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
########################################################


def process_bu_assign_statutory_request(request, db, session_user):
    request_frame = request.request
    result = None
    if type(request_frame) is bu_as.GetClientInfo:
        result = get_client_info(db, session_user)

    if type(request_frame) is bu_as.DownloadAssignStatutory:
        result = get_download_assign_statutory(db, request_frame, session_user)

    if type(request_frame) is bu_as.UploadAssignStatutoryCSV:
        result = upload_assign_statutory_csv(db, request_frame, session_user)

    if type(request_frame) is bu_as.GetAssignStatutoryForApprove:
        result = get_assign_statutory_pending_list(
            db, request_frame, session_user
        )
    if type(request_frame) is bu_as.GetAssignStatutoryFilters:
        result = get_assign_statutory_filter_for_approve_page(
            db, request_frame
        )
    if type(request_frame) is bu_as.ViewAssignStatutoryData:
        result = get_assign_statutory_data_by_csvid(
            db, request_frame, session_user
        )
    if type(request_frame) is bu_as.ViewAssignStatutoryDataFromFilter:
        result = get_assign_statutory_data_by_filter(
            db, request_frame, session_user
        )
    if type(request_frame) is bu_as.AssignStatutoryApproveActionInList:
        result = update_assign_statutory_action_in_list(
            db, request_frame, session_user
        )
    if type(request_frame) is bu_as.UpdateASMClickCount:
        result = update_rejected_asm_download_count(
            db, request_frame, session_user
        )
    if type(request_frame) is bu_as.DeleteRejectedASMByCsvID:
        result = delete_rejected_asm_data(db, request_frame, session_user)

    if type(request_frame) is bu_as.GetRejectedAssignSMData:
        result = get_rejected_assign_sm_data(db, request_frame, session_user)

    if type(request_frame) is bu_as.GetAssignedStatutoryBulkReportData:
        result = get_assigned_statutory_bulk_report_data(
            db, request_frame, session_user
        )
    if type(request_frame) is bu_as.ExportASBulkReportData:
        result = export_assigned_statutory_bulk_report_data(
            db, request_frame, session_user
        )
    if type(request_frame) is bu_as.DownloadRejectedASMReport:
        result = download_rejected_asm_report(db, request_frame, session_user)

    if type(request_frame) is bu_as.SaveAction:
        result = save_action(db, request_frame, session_user)

    if type(request_frame) is bu_as.SubmitAssignStatutory:
        result = submit_assign_statutory(db, request_frame, session_user)

    if type(request_frame) is bu_as.ConfirmAssignStatutorySubmit:
        result = confirm_submit_assign_statutory(
            db, request_frame, session_user
        )
    if type(request_frame) is bu_as.AssignStatutoryValidate:
        result = validate_assign_statutory(db, request_frame)

    if type(request_frame) is bu_as.GetBulkUploadConstants:
        result = process_get_bulk_upload_constants(db, session_user)

    if type(request_frame) is bu_as.GetDomainExecutiveDetails:
        result = process_get_domain_users(db, session_user)

    if type(request_frame) is bu_as.GetAssignStatutoryStatus:
        result = process_get_status(db, request_frame)

    if type(request_frame) is bu_as.GetAssignStatutoryDownloadStatus:
        result = process_get_download_status(db, request_frame)

    if type(request_frame) is bu_as.GetAssignStatutorySubmitStatus:
        result = process_get_submit_status(db, request_frame)

    if type(request_frame) is bu_as.GetAssignStatutoryConfirmStatus:
        result = process_get_confirm_status(db, request_frame)

    if type(request_frame) is bu_as.GetAssignStatutoryListStatus:
        result = process_get_list_status(db, request_frame)

    return result

########################################################
'''
    returns client info list
    :param
        db: database object
        session_user: logged in user id
    :type
        db: Object
        session_user: String
    :returns
        result: returns processed api response GetClientInfoSucces class Object
    rtype:
        result: Object
'''
########################################################


def get_client_info(db, session_user):

    clients_data, entitys_data, units_data, a_units_data = get_client_list(
        db, session_user
    )
    result = bu_as.GetClientInfoSuccess(
        clients_data, entitys_data, units_data, a_units_data
    )
    return result

########################################################
'''
    returns download assign statutory csv
    :param
        db: database object
        request_frame: api request DownloadAssignStatutory class object
        session_user: logged in user id
    :type
        db: Object
        request_frame: Object
        session_user: String
    :returns
        result: returns processed api response DownloadAssignStatutorySuccess
        class Object
    rtype:
        result: Object
'''
########################################################


def validate_download_data(db, request_frame, session_user, csv_name):

    def write_file():
        file_name = "%s_%s.%s" % (
            csv_name, "result", "txt"
        )
        file_path = "%s/%s" % (BULKUPLOAD_INVALID_PATH, file_name)
        with open(file_path, "wb") as fn:
            fn.write(return_data)
        return
    try:
        cl_id = request_frame.cl_id
        le_id = request_frame.le_id
        d_ids = request_frame.d_ids
        u_ids = request_frame.u_ids
        cl_name = request_frame.cl_name
        le_name = request_frame.le_name
        d_names = request_frame.d_names
        u_names = request_frame.u_names

        get_download_assing_statutory_list(
            db, cl_id, le_id, d_ids, u_ids,
            cl_name, le_name, d_names, u_names, session_user
        )

        converter = ConvertJsonToCSV(
            db, request_frame, session_user, "DownloadAssignStatutory"
        )

        return_data = bu_as.DownloadAssignStatutorySuccess(
            converter.FILE_DOWNLOAD_PATH
        ).to_structure()
        return_data = json.dumps(return_data)

    except AssertionError as error:
        e = "AssertionError"
        return_data = json.dumps(e)
        write_file()
        logger.logKnowledge(
            "error",
            "buassignstatutorycontroller.py - validate_download_data", e)
        raise(error)
    except Exception, e:
        return_data = json.dumps(str(e))
        write_file()
        logger.logKnowledge(
            "error",
            "buassignstatutorycontroller.py - validate_download_data", e)
        raise(e)
    write_file()
    return


def get_download_assign_statutory(db, request_frame, session_user):
    csv_name = generate_random_string()
    t = threading.Thread(
        target=validate_download_data,
        args=(db, request_frame, session_user, csv_name))
    t.start()
    return bu_as.Done(csv_name)


########################################################
'''
   save the file in csv folder after success full csv data validation
    :param
        db: database object
        request_frame: api request UploadAssignStatutoryCSV class object
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


def validate_data(db, request_frame, c_obj, session_user, csv_name):
    def write_file():
        file_string = csv_name.split(".")
        file_name = "%s_%s.%s" % (
            file_string[0], "result", "txt"
        )
        file_path = "%s/%s" % (BULKUPLOAD_INVALID_PATH, file_name)
        with open(file_path, "wb") as fn:
            fn.write(return_data)
        return
    try:
        res_data = c_obj.perform_validation()
        assigned_units = verify_user_units(
            db, session_user, ",".join(map(str, c_obj._unit_ids))
        )
        return_data = None
        if res_data == "InvalidCSV":
            return_data = "InvalidCSV"
        elif assigned_units < len(c_obj._unit_ids):
            return_data = "UnitsNotAssignedToUser"
        elif res_data["return_status"] is True:
            invalid_units = c_obj.check_uploaded_count_in_csv()
            if len(invalid_units) > 0:
                return_data = bu_as.UploadedRecordsCountNotMatch(
                    invalid_units
                ).to_structure()
                return_data = json.dumps(return_data)
            else:
                generate_valid_file(csv_name)
                d_ids = ",".join(map(str, c_obj._domain_ids))
                d_names = ",".join(c_obj._domain_names)
                csv_args = [
                    session_user.user_id(),
                    c_obj._client_id, c_obj._legal_entity_id,
                    d_ids, c_obj._legal_entity, d_names,
                    csv_name, c_obj._country,
                    res_data["total"]
                ]
                new_csv_id = save_assign_statutory_csv(db, csv_args)
                if new_csv_id:
                    if (
                        save_assign_statutory_data(
                            db, new_csv_id, res_data["data"]
                        ) is True
                    ):
                        u_ids = ",".join(map(str, c_obj._unit_ids))
                        c_obj.save_manager_message(
                            csv_name, c_obj._client_group,
                            c_obj._legal_entity, session_user.user_id(),
                            u_ids
                        )
                        c_obj.source_commit()
                        return_data = bu_as.UploadAssignStatutoryCSVSuccess(
                            res_data["total"], res_data["valid"],
                            res_data["invalid"]
                        ).to_structure()
                        return_data = json.dumps(return_data)

        # csv data save to temp db
        else:
            return_data = bu_as.UploadAssignStatutoryCSVFailed(
                res_data["invalid_file"], res_data["mandatory_error"],
                res_data["max_length_error"], res_data["duplicate_error"],
                res_data["invalid_char_error"], res_data["invalid_data_error"],
                res_data["inactive_error"], res_data["total"],
                res_data["invalid"]
            ).to_structure()
            return_data = json.dumps(return_data)

    except AssertionError as error:
        e = "AssertionError"
        return_data = json.dumps(e)
        write_file()
        logger.logKnowledge(
            "error",
            "buassignstatutorycontroller.py - validate_data", e)
        raise(error)

    except Exception, e:
        return_data = json.dumps(str(e))
        write_file()
        logger.logKnowledge(
            "error",
            "buassignstatutorycontroller.py - validate_data", e)
        raise(e)
    write_file()
    return


def upload_assign_statutory_csv(db, request_frame, session_user):
    try:
        if request_frame.csv_size > 0:
            pass

        if get_rejected_file_count(db, session_user) > MAX_REJECTED_COUNT:
            return bu_as.RejectionMaxCountReached()

        # save csv file
        csv_name = convert_base64_to_file(
            BULKUPLOAD_CSV_PATH, request_frame.csv_name,
            request_frame.csv_data
        )
        # read data from csv file
        header, assign_statutory_data = read_data_from_csv(csv_name)

        if len(assign_statutory_data) == 0:
            return bu_as.CsvFileBlank()

        if len(assign_statutory_data) > CSV_MAX_LINES:
            file_path = "%s/csv/%s" % (BULKUPLOAD_CSV_PATH, csv_name)
            remove_uploaded_file(file_path)
            return bu_as.CsvFileExeededMaxLines(CSV_MAX_LINES)

        # csv data validation
        c_obj = ValidateAssignStatutoryCsvData(
            db, assign_statutory_data, session_user, request_frame.csv_name,
            header
        )

        t = threading.Thread(
            target=validate_data,
            args=(db, request_frame, c_obj, session_user, csv_name))
        t.start()
        return bu_as.Done(csv_name)

    except Exception, e:
        print e
        raise e


########################################################
'''
    returns assign statutory pending list
    :param
        db: database object
        request_frame: api request GetAssignStatutoryForApprove class object
        session_user: logged in user id
    :type
        db: Object
        request_frame: Object
        session_user: String
    :returns
        result: returns processed api response
        GetAssignStatutoryForApproveSuccess class Object
    rtype:
        result: Object
'''
########################################################


def get_assign_statutory_pending_list(db, request_frame, session_user):
    pending_csv_list_as = get_pending_list(
        db, request_frame.cl_id, request_frame.le_id, session_user
    )
    result = bu_as.GetAssignStatutoryForApproveSuccess(
        pending_csv_list_as
    )
    return result


###################################################################
# get master details for filter process in approve assign statutory
###################################################################

def get_assign_statutory_filter_for_approve_page(db, request_frame):
    csv_id = request_frame.csv_id
    response = get_assign_statutory_filters_for_approve(db, csv_id)
    return response


################################
# get filtered result by csv_id
################################
def get_assign_statutory_data_by_csvid(db, request_frame, session_user):
    response = get_assign_statutory_by_csv_id(db, request_frame, session_user)
    return response


#####################################
# get filtered result by filter page
#####################################
def get_assign_statutory_data_by_filter(db, request_frame, session_user):
    response = get_assign_statutory_by_filter(db, request_frame, session_user)
    return response


#################################################################
# To update records in table by approve all / reject all function
#################################################################
def list_statutory_thread_process(
    db, request_frame, c_obj, session_user, csv_name
):
    def write_file():
        file_name = "%s_%s.%s" % (
            csv_name, "result", "txt"
        )
        file_path = "%s/%s" % (BULKUPLOAD_INVALID_PATH, file_name)
        with open(file_path, "wb") as fn:
            fn.write(return_data)
        return
    try:
        csv_id = request_frame.csv_id
        action = request_frame.bu_action
        remarks = request_frame.remarks
        return_data = None
        is_declined = c_obj.perform_validation_before_submit()
        if action == 1:
            if len(is_declined.keys()) > 0:
                c_obj.update_child(csv_id)
                return_data = bu_as.ValidationSuccess(
                    len(is_declined.keys())
                ).to_structure()
                return_data = json.dumps(return_data)
            else:
                if(update_approve_action_from_list(
                    db, csv_id, action, remarks, session_user, "all"
                )
                ):
                    c_obj.frame_data_for_main_db_insert(session_user.user_id())
                    u_ids = ",".join(map(str, c_obj._unit_ids))
                    c_obj.save_executive_message(
                        action, c_obj._csv_name, c_obj._client_group,
                        c_obj._legal_entity, session_user.user_id(),
                        u_ids, None, 0
                    )
                    c_obj.source_commit()
                    delete_action_after_approval(db, csv_id)
                    return_data = bu_as.AssignStatutoryApproveActionInListSuccess().to_structure()
                    return_data = json.dumps(return_data)
        else:
            if(update_approve_action_from_list(
                db, csv_id, action, remarks, session_user, "all"
            )):
                u_ids = ",".join(map(str, c_obj._unit_ids))
                c_obj.save_executive_message(
                    action, c_obj._csv_name, c_obj._client_group,
                    c_obj._legal_entity, session_user.user_id(),
                    u_ids, remarks, 0
                )
                c_obj.source_commit()
                return_data =  bu_as.AssignStatutoryApproveActionInListSuccess().to_structure()
                return_data = json.dumps(return_data)
    except AssertionError as error:
        e = "AssertionError"
        return_data = json.dumps(e)
        write_file()
        logger.logKnowledge(
            "error",
            "buassignstatutorycontroller.py - list_statutory_thread_process", e)
        raise(error)
    except Exception, e:
        return_data = json.dumps(str(e))
        write_file()
        logger.logKnowledge(
            "error",
            "buassignstatutorycontroller.py - list_statutory_thread_process", e)
        raise(e)
    write_file()
    return


def update_assign_statutory_action_in_list(db, request_frame, session_user):
    csv_id = request_frame.csv_id
    client_id = request_frame.cl_id
    legal_entity_id = request_frame.le_id
    csv_name = generate_random_string()
    try:
        c_obj = ValidateAssignStatutoryForApprove(
            db, csv_id, client_id, legal_entity_id, session_user
        )

        t = threading.Thread(
            target=list_statutory_thread_process,
            args=(db, request_frame, c_obj, session_user, csv_name))
        t.start()
        return bu_as.Done(csv_name)

    except Exception, e:
        raise e


#############################################################
# To update rejected asm download count by csvid in db table.
#############################################################

def update_rejected_asm_download_count(db, request_frame, session_user):

    csv_id = request_frame.csv_id
    asm_updated_count = update_asm_download_count_by_csvid(db,
                                                           session_user,
                                                           csv_id)
    result = bu_as.RejecteASMUpdatedDownloadCountSuccess(asm_updated_count)
    return result


###################################
# To delete rejected asm by csvid.
###################################

def delete_rejected_asm_data(db, request_frame, session_user):
    client_id = request_frame.client_id
    le_id = request_frame.le_id
    d_id = request_frame.d_id
    unit_code = request_frame.asm_unit_code
    csv_id = request_frame.csv_id
    user_id = session_user.user_id()
    rejected_data = get_list_and_delete_rejected_asm(db, session_user, user_id,
                                                     client_id, le_id,
                                                     d_id, unit_code,
                                                     csv_id)
    result = bu_as.GetRejectedASMDataSuccess(rejected_data)
    return result


##################################
# To get all rejected asm by user
##################################

def get_rejected_assign_sm_data(db, request_frame, session_user):

    client_id = request_frame.client_id
    le_id = request_frame.le_id
    d_id = request_frame.d_id
    unit_code = request_frame.asm_unit_code
    user_id = session_user.user_id()

    asm_rejected_data = fetch_rejected_assign_sm_data(
        db, user_id, client_id, le_id, d_id, unit_code)
    result = bu_as.GetRejectedASMBulkUploadDataSuccess(asm_rejected_data)
    return result


###################################################
# To get all asm report data by user
###################################################

def get_assigned_statutory_bulk_report_data(db, request_frame, session_user):

    clientGroupId = request_frame.bu_client_id
    legalEntityId = request_frame.bu_legal_entity_id
    unitId = request_frame.bu_unit_id
    domainIds = request_frame.domain_ids
    from_date = request_frame.from_date
    to_date = request_frame.to_date
    record_count = request_frame.r_count
    page_count = request_frame.p_count
    child_ids = request_frame.child_ids
    user_category_id = request_frame.user_category_id

    from_date = datetime.datetime.strptime(from_date, '%d-%b-%Y')
    to_date = datetime.datetime.strptime(to_date, '%d-%b-%Y')
    asm_reportdata, total_record = fetch_assigned_statutory_bulk_report(
        db, session_user, session_user.user_id(), clientGroupId, legalEntityId,
        unitId, domainIds, from_date, to_date, record_count, page_count,
        child_ids, user_category_id)

    result = bu_as.GetAssignedStatutoryReportDataSuccess(asm_reportdata,
                                                         total_record)
    return result


########################################################
# To Export the Assign statu Report Data
########################################################

def export_assigned_statutory_bulk_report_data(db, request, session_user):
    if request.csv:
        converter = ConvertJsonToCSV(
            db, request, session_user, "ExportASBulkReport"
        )
        if converter.FILE_DOWNLOAD_PATH is None:
            return technoreports.ExportToCSVEmpty()
        else:
            return generalprotocol.ExportToCSVSuccess(
                link=converter.FILE_DOWNLOAD_PATH
            )


###################################################
# To download rejected asm data
###################################################

def download_rejected_asm_report(db, request_frame, session_user):
    client_id = request_frame.client_id
    le_id = request_frame.le_id
    d_id = request_frame.d_id
    asm_unit_code = request_frame.asm_unit_code
    csv_id = request_frame.csv_id
    download_format = request_frame.download_format
    user_id = session_user.user_id()

    if asm_unit_code == '':
        asm_unit_code = 0
    sheet_name = "Rejected Assign Statutory"

    csv_header_key = ["client_group", "legal_entity", "country", "domain",
                      "organization", "unit_code", "unit_name",
                      "unit_location", "perimary_legislation",
                      "secondary_legislation", "statutory_provision",
                      "compliance_task_name", "compliance_description",
                      "statutory_applicable_status", "statytory_remarks",
                      "compliance_applicable_status", "remarks",
                      "rejected_reason", "is_fully_rejected"
                      ]

    csv_column_name = ["Client_Group", "Legal_Entity", "Country",
                       "Domain", "Organisation",
                       "Unit_Code", "Unit_Name",
                       "Unit_Location",
                       "Primary_Legislation", "Secondary_Legislaion",
                       "Statutory_Provision", "Compliance_Task_Name",
                       "Compliance_Description",
                       "Statutory_Applicable_Status*", "Statutory_remarks",
                       "Compliance_Applicable_Status*", "Error_Description"]
    csv_name = get_asm_csv_file_name_by_id(db, session_user, user_id, csv_id)
    source_data = fetch_rejected_asm_download_csv_report(
        db, session_user, user_id, client_id, le_id, d_id, asm_unit_code,
        csv_id)
    cObj = ValidateRejectedDownloadBulkData(
        db, source_data, session_user, download_format, csv_name,
        csv_header_key, csv_column_name, sheet_name)
    result = cObj.perform_validation()
    return bu_sm.DownloadActionSuccess(result["xlsx_link"],
                                       result["csv_link"],
                                       result["ods_link"],
                                       result["txt_link"])


####################################################
# save record in table by user using individual row
#####################################################
def save_action(db, request_frame, session_user):
    try:
        save_action_from_view(
            db, request_frame.csv_id, request_frame.as_ids,
            request_frame.bu_action, request_frame.remarks,
            session_user
        )
        return bu_as.SaveActionSuccess()

    except Exception, e:
        raise e


#########################################################
# submit record by user after select all individual rpw
#########################################################

def submit_statutory_thread_process(
    db, request_frame, c_obj, session_user, csv_name
):
    def write_file():
        file_name = "%s_%s.%s" % (
            csv_name, "result", "txt"
        )
        file_path = "%s/%s" % (BULKUPLOAD_INVALID_PATH, file_name)
        with open(file_path, "wb") as fn:
            fn.write(return_data)
        return
    try:
        csv_id = request_frame.csv_id
        return_data = None
        is_declined = c_obj.perform_validation_before_submit()
        if len(is_declined.keys()) > 0:
            return_data = bu_as.ValidationSuccess(
                len(is_declined.keys())
                ).to_structure()
            return_data = json.dumps(return_data)
        else:
            update_approve_action_from_list(
                db, csv_id, 1, None, session_user, "single"
            )
            u_ids = ",".join(map(str, c_obj._unit_ids))
            c_obj.save_executive_message(
                1, c_obj._csv_name, c_obj._client_group,
                c_obj._legal_entity, session_user.user_id(),
                u_ids, None, 0
            )
            c_obj.frame_data_for_main_db_insert(session_user.user_id())
            c_obj.source_commit()
            delete_action_after_approval(db, csv_id)

            return_data = bu_as.SubmitAssignStatutorySuccess().to_structure()
            return_data = json.dumps(return_data)
    except AssertionError as error:
        e = "AssertionError"
        return_data = json.dumps(e)
        write_file()
        logger.logKnowledge(
            "error",
            "buassignstatutorycontroller.py - submit_statutory_thread_process", e)
        raise(error)
    except Exception, e:
        return_data = json.dumps(str(e))
        write_file()
        logger.logKnowledge(
            "error",
            "buassignstatutorycontroller.py - submit_statutory_thread_process", e)
        raise(e)
    write_file()
    return


def submit_assign_statutory(db, request_frame, session_user):
    try:
        csv_id = request_frame.csv_id
        client_id = request_frame.cl_id
        legal_entity_id = request_frame.le_id
        # csv data validation

        csv_name = generate_random_string()

        approved_count, un_saved_count = get_validation_info(db, csv_id)
        if un_saved_count > 0:
            return bu_as.CompleteActionBeforeSubmit()

        c_obj = ValidateAssignStatutoryForApprove(
            db, csv_id, client_id, legal_entity_id, session_user
        )

        t = threading.Thread(
            target=submit_statutory_thread_process,
            args=(db, request_frame, c_obj, session_user, csv_name))
        t.start()
        return bu_as.Done(csv_name)

    except Exception, e:
        print e
        print str(traceback.format_exc())
        raise e


############################################################
# submit record bu user with system declined information
#############################################################
def confirm_statutory_thread_process(
    db, request_frame, c_obj, session_user, csv_name
):
    def write_file():
        file_name = "%s_%s.%s" % (
            csv_name, "result", "txt"
        )
        file_path = "%s/%s" % (BULKUPLOAD_INVALID_PATH, file_name)
        with open(file_path, "wb") as fn:
            fn.write(return_data)
        return
    try:
        csv_id = request_frame.csv_id
        return_data = None
        is_declined = c_obj.perform_validation_before_submit()
        if len(is_declined.keys()) > 0:
            c_obj.make_rejection(is_declined, session_user.user_id())
            u_ids = ",".join(map(str, c_obj._unit_ids))
            c_obj.save_executive_message(
                1, c_obj._csv_name, c_obj._client_group,
                c_obj._legal_entity, session_user.user_id(),
                u_ids, None, len(is_declined.keys())
            )
            c_obj.frame_data_for_main_db_insert(session_user.user_id())
            c_obj.source_commit()
            delete_action_after_approval(db, csv_id)
            return_data = bu_as.SubmitAssignStatutorySuccess().to_structure()
            return_data = json.dumps(return_data)

    except AssertionError as error:
        e = "AssertionError"
        return_data = json.dumps(e)
        write_file()
        logger.logKnowledge(
            "error",
            "buassignstatutorycontroller.py - confirm_statutory_thread_process", e)
        raise(error)
    except Exception, e:
        return_data = json.dumps(str(e))
        write_file()
        logger.logKnowledge(
            "error",
            "buassignstatutorycontroller.py - confirm_statutory_thread_process", e)
        raise(e)
    write_file()
    return


def confirm_submit_assign_statutory(db, request_frame, session_user):
    csv_id = request_frame.csv_id
    client_id = request_frame.cl_id
    legal_entity_id = request_frame.le_id

    csv_name = generate_random_string()
    # csv data validation
    c_obj = ValidateAssignStatutoryForApprove(
        db, csv_id, client_id, legal_entity_id, session_user
    )
    t = threading.Thread(
        target=confirm_statutory_thread_process,
        args=(db, request_frame, c_obj, session_user, csv_name))
    t.start()
    return bu_as.Done(csv_name)


#####################################################
# validate pending record count while submit process
#####################################################
def validate_assign_statutory(db, request_frame):
    csv_id = request_frame.csv_id
    approved_count, un_saved_count = get_validation_info(db, csv_id)

    result = bu_as.AssignStatutoryValidateSuccess(
        approved_count, un_saved_count
    )
    return result


########################################################
# To get list of user_category_id and constants
########################################################
def process_get_bulk_upload_constants(db, session_user):

    user_category_list = get_form_categories(db, session_user)
    success = bu_as.GetBulkUploadConstantSuccess(
        user_category_list, SYSTEM_REJECTED_BY, REJECTED_FILE_DOWNLOADCOUNT)
    return success


########################################################
# To get list of domain executive details
########################################################
def process_get_domain_users(db, session_user):
    res = get_domain_executive(db, session_user)
    success = bu_as.GetDomainExecutiveDetailsSuccess(res)

    return success


def process_get_status(db, request):
    csv_name = request.csv_name
    file_string = csv_name.split(".")
    file_name = "%s_%s.%s" % (
        file_string[0], "result", "txt"
    )
    file_path = "%s/%s" % (BULKUPLOAD_INVALID_PATH, file_name)
    if os.path.exists(file_path) is False:
        return bu_as.Alive()
    else:
        return_data = ""
        with open(file_path, "r") as fn:
            return_data += fn.read()
        if return_data == "InvalidCSV":
            return bu_as.InvalidCsvFile()
        elif return_data == "UnitsNotAssignedToUser":
            return bu_as.UnitsNotAssignedToUser()
        else:
            result = json.loads(return_data)
            if str(result[0]) == "UploadAssignStatutoryCSVSuccess":
                return bu_as.UploadAssignStatutoryCSVSuccess.parse_inner_structure(
                    result[1])
            elif str(result[0]) == "UploadAssignStatutoryCSVFailed":
                return bu_as.UploadAssignStatutoryCSVFailed.parse_inner_structure(
                    result[1])
            elif str(result[0]) == "UploadedRecordsCountNotMatch":
                return bu_as.UploadedRecordsCountNotMatch.parse_inner_structure(
                    result[1])
            else:
                logger.logKnowledge(
                    "error",
                    "buassignstatutorycontroller.py-process_get_status",
                    result)
                raise Exception(str(result))


def process_get_download_status(db, request):
    csv_name = request.csv_name
    file_name = "%s_%s.%s" % (
        csv_name, "result", "txt"
    )
    file_path = "%s/%s" % (BULKUPLOAD_INVALID_PATH, file_name)
    if os.path.exists(file_path) is False:
        return bu_as.Alive()
    else:
        return_data = ""
        with open(file_path, "r") as fn:
            return_data += fn.read()

        result = json.loads(return_data)
        if str(result[0]) == "DownloadAssignStatutorySuccess":
            return bu_as.DownloadAssignStatutorySuccess.parse_inner_structure(
                result[1])
        else:
            logger.logKnowledge(
                "error",
                "buassignstatutorycontroller.py-process_get_download_status",
                result)
            raise Exception(str(result))


def process_get_submit_status(db, request):
    csv_name = request.csv_name
    file_name = "%s_%s.%s" % (
        csv_name, "result", "txt"
    )
    file_path = "%s/%s" % (BULKUPLOAD_INVALID_PATH, file_name)
    if os.path.exists(file_path) is False:
        return bu_as.Alive()
    else:
        return_data = ""
        with open(file_path, "r") as fn:
            return_data += fn.read()

        result = json.loads(return_data)
        if str(result[0]) == "ValidationSuccess":
            return bu_as.ValidationSuccess.parse_inner_structure(
                result[1])
        elif str(result[0]) == "SubmitAssignStatutorySuccess":
            return bu_as.SubmitAssignStatutorySuccess.parse_inner_structure(
                result[1])
        else:
            logger.logKnowledge(
                "error",
                "buassignstatutorycontroller.py-process_get_submit_status",
                result)
            raise Exception(str(result))


def process_get_confirm_status(db, request):
    csv_name = request.csv_name
    file_name = "%s_%s.%s" % (
        csv_name, "result", "txt"
    )
    file_path = "%s/%s" % (BULKUPLOAD_INVALID_PATH, file_name)
    if os.path.exists(file_path) is False:
        return bu_as.Alive()
    else:
        return_data = ""
        with open(file_path, "r") as fn:
            return_data += fn.read()

        result = json.loads(return_data)
        if str(result[0]) == "SubmitAssignStatutorySuccess":
            return bu_as.SubmitAssignStatutorySuccess.parse_inner_structure(
                result[1])
        else:
            logger.logKnowledge(
                "error",
                "buassignstatutorycontroller.py-process_get_confirm_status",
                result)
            raise Exception(str(result))


def process_get_list_status(db, request):
    csv_name = request.csv_name
    file_name = "%s_%s.%s" % (
        csv_name, "result", "txt"
    )
    file_path = "%s/%s" % (BULKUPLOAD_INVALID_PATH, file_name)
    if os.path.exists(file_path) is False:
        return bu_as.Alive()
    else:
        return_data = ""
        with open(file_path, "r") as fn:
            return_data += fn.read()

        result = json.loads(return_data)
        if str(result[0]) == "ValidationSuccess":
            return bu_as.ValidationSuccess.parse_inner_structure(
                result[1])
        elif str(result[0]) == "AssignStatutoryApproveActionInListSuccess":
            return bu_as.AssignStatutoryApproveActionInListSuccess.parse_inner_structure(
                result[1])
        else:
            logger.logKnowledge(
                "error",
                "buassignstatutorycontroller.py-process_get_list_status",
                result)
            raise Exception(str(result))
