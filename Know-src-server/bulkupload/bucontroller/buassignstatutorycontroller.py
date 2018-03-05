from ..bucsvvalidation.assignstatutoryvalidation import ValidateAssignStatutoryCsvData
from server.jsontocsvconverter import ConvertJsonToCSV
from ..buapiprotocol import buassignstatutoryprotocol as bu_as
from ..budatabase.buassignstatutorydb import *
from ..bulkuploadcommon import (
    convert_base64_to_file,
    read_data_from_csv
)

from server.constants import BULKUPLOAD_CSV_PATH
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

    if type(request_frame) is bu_as.GetAssignStatutoryFilters:
        result = get_assign_statutory_filter_for_approve_page(db, request_frame, session_user)

    if type(request_frame) is bu_as.ViewAssignStatutoryData:
        result = get_assign_statutory_data_by_csvid(db, request_frame, session_user)

    if type(request_frame) is bu_as.ViewAssignStatutoryDataFromFilter:
        result = get_assign_statutory_data_by_filter(db, request_frame, session_user)

    if type(request_frame) is bu_as.AssignStatutoryApproveActionInList:
        result = update_assign_statutory_action_in_list(db, request_frame, session_user)

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


def get_assign_statutory_filter_for_approve_page(db, request_frame, session_user):
    csv_id = request_frame.csv_id
    response = get_assign_statutory_filters_for_approve(db, csv_id)
    return response

def get_assign_statutory_data_by_csvid(db, request_frame, session_user):
    response = get_assign_statutory_by_csv_id(db, request_frame, session_user)
    return response

def get_assign_statutory_data_by_filter(db, request_frame, session_user):
    response = get_assign_statutory_by_filter(db, request_frame, session_user)
    return response

def update_assign_statutory_action_in_list(db, request_frame, session_user):
    csv_id = request_frame.csv_id
    action = request_frame.bu_action
    remarks = request_frame.remarks
    client_id = request_frame.cl_id
    legal_entity_id = request_frame.le_id
    try :
        if action == 1 :
            cObj = ValidateAssignStatutoryForApprove(
                db, csv_id, client_id, legal_entity_id, session_user
            )
            is_declined = cObj.perform_validation_before_submit()
            if len(is_declined) > 0 :
                return bu_as.ValidationSuccess(is_declined)
            else :
                if (update_approve_action_from_list(db, csv_id, action, remarks, session_user)) :
                    cObj.frame_data_for_main_db_insert()
                    return bu_as.AssignStatutoryApproveActionInListSuccess()
        else :
            if (update_approve_action_from_list(db, csv_id, action, remarks, session_user)) :
                cObj.frame_data_for_main_db_insert()
                return bu_as.AssignStatutoryApproveActionInListSuccess()

    except Exception, e:
        raise e