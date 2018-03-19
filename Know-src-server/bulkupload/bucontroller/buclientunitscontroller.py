from ..bucsvvalidation.clientunitsvalidation import (
    ValidateClientUnitsBulkCsvData,
    ValidateClientUnitsBulkDataForApprove
)

from ..bucsvvalidation.rejectedstatutorymapping import ValidateRejectedSMBulkCsvData

from ..buapiprotocol import buclientunitsprotocol as bu_cu
from ..buapiprotocol import bustatutorymappingprotocol as bu_sm


from ..budatabase.buclientunitsdb import *
from ..bulkuploadcommon import (
    convert_base64_to_file,
    read_data_from_csv,
    generate_valid_file
)
import datetime
from ..bulkexport import ConvertJsonToCSV
from server.constants import BULKUPLOAD_CSV_PATH
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
def process_bu_client_units_request(request, db, session_user):
    request_frame = request.request

    if type(request_frame) is bu_cu.UploadClientUnitsBulkCSV:
        result = upload_client_units_bulk_csv(db, request_frame, session_user)

    if type(request_frame) is bu_cu.GetClientUnitsUploadedCSVFiles:
        result = get_ClientUnits_Uploaded_CSVFiles(db, request_frame, session_user)

    if type(request_frame) is bu_cu.GetClientUnitRejectedData:
        result = get_rejected_client_unit_data(db, request_frame, session_user)

    if type(request_frame) is bu_cu.UpdateUnitClickCount:
        result = update_unit_download_count(db, request_frame, session_user)

    if type(request_frame) is bu_cu.DeleteRejectedUnitDataByCsvID:
        result = delete_rejected_unit_data_by_csv_id(db, request_frame, session_user)

    if type(request_frame) is bu_cu.GetClientUnitBulkReportData:
        result = get_client_unit_bulk_report_data(db, request_frame, session_user)

    if type(request_frame) is bu_cu.DownloadRejectedClientUnitReport:
        result = download_rejected_cu_report(db, request_frame, session_user)

    if type(request_frame) is bu_cu.ExportCUBulkReportData:
        result = export_clientunit_bulk_report(db, request_frame, session_user)

    if type(request_frame) is bu_cu.DownloadRejectedClientUnitReport:
        result = download_rejected_cu_report(db, request_frame, session_user)

    if type(request_frame) is bu_cu.PerformClientUnitApproveReject:
        result = perform_bulk_client_unit_approve_reject(db, request_frame, session_user)

    if type(request_frame) is bu_cu.ConfirmClientUnitDeclination:
        result = perform_bulk_client_unit_declination(db, request_frame, session_user)

    if type(request_frame) is bu_cu.GetBulkClientUnitApproveRejectList:
        result = get_client_unit_list_and_filters_for_view(db, request_frame, session_user)

    if type(request_frame) is bu_cu.GetBulkClientUnitListForFilterView:
        result = get_bulk_client_unit_list_by_filter_for_view(db, request_frame, session_user)

    if type(request_frame) is bu_cu.SaveBulkClientUnitListFromView:
        result = save_bulk_client_unit_list_action(db, request_frame, session_user)

    if type(request_frame) is bu_cu.SubmitBulkClientUnitListFromView:
        result = submit_bulk_client_unit_list_action(db, request_frame, session_user)

    if type(request_frame) is bu_cu.ConfirmSubmitClientUnitFromView:
        result = confirm_submit_bulk_client_unit_list_action(db, request_frame, session_user)

    return result

#########################################################################################################
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
        result: return could be success class object or failure class objects also raise the exceptions
    rtype:
        result: Object
'''
##########################################################################################################

def upload_client_units_bulk_csv(db, request_frame, session_user):
    if request_frame.csv_size > 0 :
        pass
    # save csv file
    csv_name = convert_base64_to_file(
            BULKUPLOAD_CSV_PATH, request_frame.csv_name,
            request_frame.csv_data
        )

    # read data from csv file
    header, client_units_bulk_data = read_data_from_csv(csv_name)
    # csv data validation
    cObj = ValidateClientUnitsBulkCsvData(
        db, client_units_bulk_data, session_user, request_frame.bu_client_id,
        request_frame.csv_name, header
    )
    res_data = cObj.perform_validation()
    print "err"
    print res_data
    if res_data != "Empty CSV File Uploaded" and res_data["return_status"] is True :
        generate_valid_file(csv_name)
        if res_data["doc_count"] == 0 :
            upload_sts = 1
        else :
            upload_sts = 0

        csv_args = [
            request_frame.bu_client_id, request_frame.bu_group_name,
            csv_name, session_user.user_id(),
            res_data["total"]
        ]
        new_csv_id = save_client_units_mapping_csv(db, csv_args)
        if new_csv_id :
            if save_mapping_client_unit_data(db, new_csv_id, res_data["data"]) is True :
                cObj.save_executive_message(csv_name, request_frame.bu_group_name, session_user.user_id())
                result = bu_cu.UploadClientUnitBulkCSVSuccess(
                    res_data["total"], res_data["valid"], res_data["invalid"]
                )
                return result
    elif res_data != "Empty CSV File Uploaded" and res_data["return_status"] is False :
        result = bu_cu.UploadClientUnitBulkCSVFailed(
            res_data["invalid_file"], res_data["mandatory_error"],
            res_data["max_length_error"], res_data["duplicate_error"],
            res_data["invalid_char_error"], res_data["invalid_data_error"],
            res_data["inactive_error"], res_data["max_unit_count_error"],
            res_data["total"], res_data["invalid"]
        )
        return result
    elif res_data == "Empty CSV File Uploaded" :
        return bu_cu.EmptyCSVUploaded()

#########################################################################################################
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
        result: return could be success class object or failure class objects also raise the exceptions
    rtype:
        result: Object
'''
##########################################################################################################

def get_ClientUnits_Uploaded_CSVFiles(db, request_frame, session_user):
    clientId = request_frame.bu_client_id
    groupName = request_frame.bu_group_name
    csvFilesList = get_ClientUnits_Uploaded_CSVList(db, clientId, groupName)
    return bu_cu.ClientUnitsUploadedCSVFilesListSuccess(
        bu_cu_csvFilesList=csvFilesList
    )

########################################################


def get_rejected_client_unit_data(db, request_frame, session_user):
    client_group_id = request_frame.bu_client_id
    user_id = session_user.user_id()
    print "client_group_id, user_id >>>"
    print client_group_id, user_id
    rejected_unit_data = fetch_rejected_client_unit_report(db, session_user,
                                                           user_id,
                                                           client_group_id)
    result = bu_cu.GetRejectedClientUnitDataSuccess(rejected_unit_data)
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
def update_unit_download_count(db, request_frame, session_user):

    csv_id=request_frame.csv_id
    user_id=session_user.user_id()

    updated_unit_count = update_unit_count(db, session_user, csv_id)
    result = bu_cu.UpdateUnitDownloadCountSuccess(updated_unit_count)
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
def delete_rejected_unit_data_by_csv_id(db, request_frame, session_user):


    bu_client_id=request_frame.bu_client_id
    csv_id=request_frame.csv_id

    user_id=session_user.user_id()

    rejected_unit_data = get_list_and_delete_rejected_unit(db, session_user, user_id,
        csv_id, bu_client_id)
    result = bu_cu.GetRejectedClientUnitDataSuccess(rejected_unit_data)
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


def get_client_unit_bulk_report_data(db, request_frame, session_user):
    clientGroupId = request_frame.bu_client_id
    from_date = request_frame.from_date
    to_date = request_frame.to_date
    record_count = request_frame.r_count
    page_count = request_frame.p_count
    child_ids = request_frame.child_ids
    user_category_id = request_frame.user_category_id

    user_id = session_user.user_id()


    from_date = datetime.datetime.strptime(from_date, '%d-%b-%Y').strftime('%Y-%m-%d %H:%M:%S')
    to_date = datetime.datetime.strptime(to_date, '%d-%b-%Y').strftime('%Y-%m-%d %H:%M:%S')

    clientdata, total_record = fetch_client_unit_bulk_report(db, session_user,
    session_user.user_id(), clientGroupId, from_date, to_date,
    record_count, page_count, child_ids, user_category_id)
    # reportdata=result[0]
    # total_record=result[1]

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

##########################################################################################################
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
        result: returns processed api response PerformClientUnitApproveRejectSuccess class Object
    rtype:
        result: Object
'''
##########################################################################################################

def perform_bulk_client_unit_approve_reject(db, request_frame, session_user):
    csv_id = request_frame.csv_id
    bu_client_id = request_frame.bu_client_id
    bu_remarks = request_frame.bu_remarks
    password = request_frame.password
    actionType = request_frame.bu_action

    try:
        cuObj = ValidateClientUnitsBulkDataForApprove(
                db, csv_id, bu_client_id, session_user
            )
        if actionType == 1:
            system_declined_count = cuObj.check_for_system_declination_errors()
            if (update_bulk_client_unit_approve_reject_list(db, csv_id, actionType, bu_remarks, session_user)) :
                cuObj.process_data_to_main_db_insert()
                cuObj.make_rejection(system_declined_count)
                cuObj.save_manager_message(actionType, cuObj._csv_name, cuObj._group_name, session_user.user_id())
                cuObj.source_commit()
                return bu_cu.UpdateApproveRejectActionFromListSuccess(declined_count=len(system_declined_count))
        else :
            if (update_bulk_client_unit_approve_reject_list(db, csv_id, actionType, bu_remarks, session_user)) :
                print "after main db update"
                cuObj.save_manager_message(actionType, cuObj._csv_name, cuObj._group_name, session_user.user_id())
                cuObj.source_commit()
                return bu_cu.UpdateApproveRejectActionFromListSuccess(declined_count=0)

    except Exception, e:
        raise e


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
###########################################################################################################

def download_rejected_cu_report(db, request_frame, session_user):
    csv_id = request_frame.csv_id
    cg_id = request_frame.cg_id
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

    #csv_name = "RejectedData.xlsx"
    csv_name = get_cu_csv_file_name_by_id(db, session_user, user_id, csv_id)

    source_data = fetch_rejected_cu_download_csv_report(
        db, session_user, user_id,
        cg_id, csv_id)

    cObj = ValidateRejectedSMBulkCsvData(
        db, source_data, session_user, download_format, csv_name, csv_header
    )
    result = cObj.perform_validation()

    return bu_sm.DownloadActionSuccess(result["xlsx_link"], result["csv_link"],
        result["ods_link"], result["txt_link"])

##########################################################################################################
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
        result: returns processed api response ConfirmClientUnitDeclination class Object
    rtype:
        result: Boolean
'''
##########################################################################################################

def perform_bulk_client_unit_declination(db, request_frame, session_user):
    csv_id = request_frame.csv_id
    bu_client_id = request_frame.bu_client_id
    try:
        print "inside declined confirm"
        cuObj = ValidateClientUnitsBulkDataForApprove(
            db, csv_id, bu_client_id, session_user
        )

        system_declined_count = cuObj.check_for_system_declination_errors()
        print system_declined_count
        if len(system_declined_count) > 0:
            print "before main db insert"
            cuObj.process_data_to_main_db_insert()
            print "after insert"
            cuObj.make_rejection(system_declined_count)
            print "after rejection"
            cuObj.save_manager_message(1, cuObj._csv_name, cuObj._group_name, session_user.user_id())
            print "save tech msg"
            cuObj.source_commit()
            return bu_cu.SubmitClientUnitDeclinationSuccess()

    except Exception, e:
        raise e

##########################################################################################################
'''   returns set of dataset
    :param
        db: database object
        request_frame: api request GetBulkClientUnitApproveRejectList class object
        session_user: logged in user details
    :type
        db: Object
        request_frame: Object
        session_user: Object
    :returns
        result: returns processed api response GetBulkClientUnitApproveRejectList class Object
    rtype:
        result: set of datasets
'''
##########################################################################################################

def get_client_unit_list_and_filters_for_view(db, request_frame, session_user):
    resultSet = get_bulk_client_units_and_filtersets_by_csv_id(db, request_frame, session_user)
    return resultSet

##########################################################################################################
'''   returns a dataset
    :param
        db: database object
        request_frame: api request GetBulkClientUnitApproveRejectList class object
        session_user: logged in user details
    :type
        db: Object
        request_frame: Object
        session_user: Object
    :returns
        result: returns processed api response GetBulkClientUnitApproveRejectList class Object
    rtype:
        result: set of datasets
'''
##########################################################################################################

def get_bulk_client_unit_list_by_filter_for_view(db, request_frame, session_user):
    response = get_bulk_client_unit_list_by_filter(db, request_frame, session_user)
    return response

##########################################################################################################
'''   returns boolean value for the updation
    :param
        db: database object
        request_frame: api request SubmitBulkClientUnitListFromView class object
        session_user: logged in user details
    :type
        db: Object
        request_frame: Object
        session_user: Object
    :returns
        result: returns processed api response SubmitBulkClientUnitListFromView class Object
    rtype:
        result: Boolean
'''
##########################################################################################################

def submit_bulk_client_unit_list_action(db, request_frame, session_user):
    csv_id = request_frame.csv_id
    bu_client_id = request_frame.bu_client_id
    actionType = request_frame.bu_action
    try:
        if get_bulk_client_unit_null_action_count(db, request_frame, session_user):
            cuObj = ValidateClientUnitsBulkDataForApprove(
                db, csv_id, bu_client_id, session_user
            )
            system_declined_count = cuObj.check_for_system_declination_errors()
            if len(system_declined_count) > 0:
                return bu_cu.ReturnDeclinedCount(system_declined_count)
            else:
                cuObj.save_manager_message(actionType, cuObj._csv_name, cuObj._group_name, session_user.user_id())
                cuObj.process_data_to_main_db_insert()
                cuObj.source_commit()
                return bu_cu.SubmitClientUnitActionFromListSuccess()
        else:
            return bu_cu.SubmitClientUnitActionFromListFailure()
    except Exception, e:
        raise e


##########################################################################################################
'''   returns boolean value for the updation
    :param
        db: database object
        request_frame: api request SubmitBulkClientUnitListFromView class object
        session_user: logged in user details
    :type
        db: Object
        request_frame: Object
        session_user: Object
    :returns
        result: returns processed api response SubmitBulkClientUnitListFromView class Object
    rtype:
        result: Boolean
'''
##########################################################################################################

def confirm_submit_bulk_client_unit_list_action(db, request_frame, session_user):
    csv_id = request_frame.csv_id
    bu_client_id = request_frame.bu_client_id
    actionType = request_frame.bu_action
    try:
        cuObj = ValidateClientUnitsBulkDataForApprove(
            db, csv_id, bu_client_id, session_user
        )

        system_declined_count = cuObj.check_for_system_declination_errors()
        if len(system_declined_count) > 0:
            return bu_cu.ReturnDeclinedCount(system_declined_count)
        else:
            cuObj.save_manager_message(actionType, cuObj._csv_name, cuObj._group_name, session_user.user_id())
            cuObj.process_data_to_main_db_insert()
            cuObj.source_commit()
            return bu_cu.SubmitClientUnitActionFromListSuccess()
    except Exception, e:
        raise e

##########################################################################################################
'''   returns boolean value for the updation
    :param
        db: database object
        request_frame: api request SaveBulkClientUnitListFromView class object
        session_user: logged in user details
    :type
        db: Object
        request_frame: Object
        session_user: Object
    :returns
        result: returns processed api response SaveBulkClientUnitListFromView class Object
    rtype:
        result: Boolean
'''
##########################################################################################################
def save_bulk_client_unit_list_action(db, request_frame, session_user):
    try :
        save_client_unit_action_from_view(
            db, request_frame.csv_id, request_frame.bulk_unit_id,
            request_frame.bu_action, request_frame.bu_remarks,
            session_user
        )
        return bu_cu.SaveClientUnitActionSuccess()

    except Exception, e :
        raise e
