from ..bucsvvalidation.clientunitsvalidation import ValidateClientUnitsBulkCsvData
from ..buapiprotocol import buclientunitsprotocol as bu_cu
from ..budatabase.buclientunitsdb import *
from ..bulkuploadcommon import (
    convert_base64_to_file,
    read_data_from_csv
)

from server.constants import BULKUPLOAD_CSV_PATH
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

    elif type(request_frame) is bu_cu.GetClientUnitsUploadedCSVFiles:
        result = get_ClientUnits_Uploaded_CSVFiles(db, request_frame, session_user)

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
    csv_file_path = convert_base64_to_file(
            BULKUPLOAD_CSV_PATH, request_frame.csv_name,
            request_frame.csv_data
        )

    # read data from csv file
    header, client_units_bulk_data = read_data_from_csv(csv_file_path)

    # csv data validation
    cObj = ValidateClientUnitsBulkCsvData(
        db, client_units_bulk_data, session_user, request_frame.bu_client_id,
        request_frame.csv_name, header
    )
    res_data = cObj.perform_validation()
    print res_data
    if res_data["return_status"] is True :

        if res_data["doc_count"] == 0 :
            upload_sts = 1
        else :
            upload_sts = 0

        csv_args = [
            request_frame.bu_client_id, request_frame.bu_group_name,
            request_frame.csv_name, session_user.user_id(),
            res_data["total"]
        ]
        new_csv_id = save_client_units_mapping_csv(db, csv_args)
        if new_csv_id :
            if save_mapping_client_unit_data(db, new_csv_id, res_data["data"]) is True :
                result = bu_cu.UploadClientUnitBulkCSVSuccess(
                    res_data["total"], res_data["valid"], res_data["invalid"]
                )

        # csv data save to temp db
    else :
        result = bu_cu.UploadClientUnitBulkCSVFailed(
            res_data["invalid_file"], res_data["mandatory_error"],
            res_data["max_length_error"], res_data["duplicate_error"],
            res_data["invalid_char_error"], res_data["invalid_data_error"],
            res_data["inactive_error"], res_data["total"], res_data["invalid"]
        )
    return result

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
