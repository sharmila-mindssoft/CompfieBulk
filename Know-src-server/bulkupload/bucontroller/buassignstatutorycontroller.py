from ..bucsvvalidation.assignstatutoryvalidation import ValidateAssignStatutoryCsvData
from ..bucsvvalidation.rejectedstatutorymapping import ValidateRejectedSMBulkCsvData
from server.jsontocsvconverter import ConvertJsonToCSV
from ..buapiprotocol import buassignstatutoryprotocol as bu_as
from ..buapiprotocol import bustatutorymappingprotocol as bu_sm
from ..budatabase.buassignstatutorydb import *
from ..bulkuploadcommon import (
    convert_base64_to_file,
    read_data_from_csv
)

from server.constants import BULKUPLOAD_CSV_PATH
import datetime
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
    if type(request_frame) is bu_as.GetClientInfo:
        result = get_client_info(db, request_frame, session_user)

    if type(request_frame) is bu_as.DownloadAssignStatutory:
        result = get_download_assing_statutory(db, request_frame, session_user)

    if type(request_frame) is bu_as.UploadAssignStatutoryCSV:
        result = upload_assign_statutory_csv(db, request_frame, session_user)

    if type(request_frame) is bu_as.GetAssignStatutoryForApprove:
        result = get_assign_statutory_pending_list(db, request_frame, session_user)

    if type(request_frame) is bu_as.UpdateASMClickCount:
        result = update_rejected_asm_download_count(db, request_frame, session_user)

    if type(request_frame) is bu_as.DeleteRejectedASMByCsvID:
        result = delete_rejected_asm_data(db, request_frame, session_user)

    if type(request_frame) is bu_as.GetRejectedAssignSMData:
        result = get_rejected_assign_sm_data(db, request_frame, session_user)

    if type(request_frame) is bu_as.GetAssignedStatutoryBulkReportData:
        result = get_assigned_statutory_bulk_report_data(db, request_frame, session_user)

    if type(request_frame) is bu_as.DownloadRejectedASMReport:
        result = download_rejected_asm_report(db, request_frame, session_user)

    return result

########################################################
'''
    returns client info list
    :param
        db: database object
        request_frame: api request GetClientInfo class object
        session_user: logged in user id
    :type
        db: Object
        request_frame: Object
        session_user: String
    :returns
        result: returns processed api response GetClientInfoSuccess class Object
    rtype:
        result: Object
'''
########################################################

def get_client_info(db, request_frame, session_user):

    clients_data, entitys_data, units_data = get_client_list(db, session_user)
    result = bu_as.GetClientInfoSuccess(
        clients_data, entitys_data, units_data
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
        result: returns processed api response DownloadAssignStatutorySuccess class Object
    rtype:
        result: Object
'''
########################################################
def get_download_assing_statutory(db, request_frame, session_user):

    cl_id = request_frame.cl_id
    le_id = request_frame.le_id
    d_ids = request_frame.d_ids
    u_ids = request_frame.u_ids
    cl_name = request_frame.cl_name
    le_name = request_frame.le_name
    d_names = request_frame.d_names
    u_names = request_frame.u_names

    res = get_download_assing_statutory_list(db, cl_id, le_id, d_ids, u_ids, cl_name, le_name, d_names, u_names, session_user)

    if len(res) > 0:
        converter = ConvertJsonToCSV(
                db, request_frame, session_user, "DownloadAssignStatutory"
            )
        result = bu_as.DownloadAssignStatutorySuccess(
            converter.FILE_DOWNLOAD_PATH
        )
        return result


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
        result: return could be success class object or failure class objects also raise the exceptions
    rtype:
        result: Object
'''
########################################################

def upload_assign_statutory_csv(db, request_frame, session_user):

    if request_frame.csv_size > 0 :
        pass
    # save csv file
    csv_name = convert_base64_to_file(
            BULKUPLOAD_CSV_PATH, request_frame.csv_name,
            request_frame.csv_data
        )
    # read data from csv file
    header, assign_statutory_data = read_data_from_csv(csv_name)

    # csv data validation
    cObj = ValidateAssignStatutoryCsvData(
        db, assign_statutory_data, session_user, request_frame.csv_name, header, 1
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
        new_csv_id = save_assign_statutory_csv(db, csv_args)
        if new_csv_id :
            if save_assign_statutory_data(db, new_csv_id, res_data["data"]) is True :
                result = bu_as.UploadAssignStatutoryCSVSuccess(
                    res_data["total"], res_data["valid"], res_data["invalid"]
                )

        # csv data save to temp db
    else :
        result = bu_as.UploadAssignStatutoryCSVFailed(
            res_data["invalid_file"], res_data["mandatory_error"],
            res_data["max_length_error"], res_data["duplicate_error"],
            res_data["invalid_char_error"], res_data["invalid_data_error"],
            res_data["inactive_error"], res_data["total"], res_data["invalid"]
        )

    return result

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
        result: returns processed api response GetAssignStatutoryForApproveSuccess class Object
    rtype:
        result: Object
'''
########################################################

def get_assign_statutory_pending_list(db, request_frame, session_user):

    pending_csv_list_as = get_pending_list(db, request_frame.cl_id, request_frame.le_id, session_user)
    result = bu_as.GetAssignStatutoryForApproveSuccess(
        pending_csv_list_as
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
def update_rejected_asm_download_count(db, request_frame, session_user):

    csv_id=request_frame.csv_id

    user_id=session_user.user_id()

    asm_updated_count = update_asm_download_count_by_csvid(db, session_user, csv_id)
    result = bu_as.RejecteASMUpdatedDownloadCountSuccess(asm_updated_count)
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
def delete_rejected_asm_data(db, request_frame, session_user):


    client_id=request_frame.client_id
    le_id=request_frame.le_id
    domain_ids=request_frame.domain_ids
    unit_code=request_frame.asm_unit_code
    csv_id=request_frame.csv_id



    user_id=session_user.user_id()

    rejected_data = get_list_and_delete_rejected_asm(db, session_user, user_id,
        client_id, le_id, domain_ids, unit_code, csv_id)
    result = bu_as.GetRejectedASMDataSuccess(rejected_data)
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
def get_rejected_assign_sm_data(db, request_frame, session_user):

    client_id=request_frame.client_id
    le_id=request_frame.le_id
    domain_ids=request_frame.domain_ids
    unit_code=request_frame.asm_unit_code

    user_id=session_user.user_id()

    asm_rejected_data = fetch_rejected_assign_sm_data(db, session_user, user_id,
        client_id, le_id, domain_ids, unit_code)
    result = bu_as.GetRejectedASMBulkUploadDataSuccess(asm_rejected_data)
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
def get_assigned_statutory_bulk_report_data(db, request_frame, session_user):

    clientGroupId=request_frame.bu_client_id
    legalEntityId=request_frame.bu_legal_entity_id
    unitId=request_frame.bu_unit_id
    domainIds=request_frame.domain_ids

    from_date=request_frame.from_date
    to_date=request_frame.to_date
    record_count=request_frame.r_count
    page_count=request_frame.p_count
    child_ids=request_frame.child_ids
    user_category_id=request_frame.user_category_id


    user_id=session_user.user_id()


    from_date = datetime.datetime.strptime(from_date, '%d-%b-%Y')
    to_date = datetime.datetime.strptime(to_date, '%d-%b-%Y')
    asm_reportdata, total_record = fetch_assigned_statutory_bulk_report(db, session_user,
    session_user.user_id(), clientGroupId, legalEntityId, unitId, domainIds, from_date, to_date,
    record_count, page_count, child_ids, user_category_id)
    result = bu_as.GetAssignedStatutoryReportDataSuccess(asm_reportdata,total_record)
    return result

def download_rejected_asm_report(db, request_frame, session_user):
    client_id = request_frame.client_id
    le_id = request_frame.le_id
    domain_ids = request_frame.domain_ids
    asm_unit_code = request_frame.asm_unit_code
    csv_id = request_frame.csv_id
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

    csv_name = "RejectedData.xlsx"

    source_data = fetch_rejected_asm_download_csv_report(
        db, session_user, user_id, client_id, le_id, domain_ids, asm_unit_code, csv_id)

    cObj = ValidateRejectedSMBulkCsvData(
        db, source_data, session_user, download_format, csv_name, csv_header
    )
    result = cObj.perform_validation()

    return bu_sm.DownloadActionSuccess(result["xlsx_link"], result["csv_link"],
        result["ods_link"], result["txt_link"])