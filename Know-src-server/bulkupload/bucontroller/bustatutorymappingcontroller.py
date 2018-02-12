from ..bucsvvalidation.statutorymappingvalidation import ValidateStatutoryMappingCsvData
from ..buapiprotocol import bustatutorymappingprotocol as bu_sm
from ..budatabase.bustatutorymappingdb import *
from ..bulkuploadcommon import (
    convert_base64_to_file,
    read_data_from_csv
)

from server.constants import BULKUPLOAD_CSV_PATH
__all__ = [
    "process_bu_statutory_mapping_request"
]
########################################################
'''
    Process all statutory mapping request here
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
def process_bu_statutory_mapping_request(request, db, session_user):
    request_frame = request.request

    if type(request_frame) is bu_sm.GetStatutoryMappingCsvUploadedList:
        result = get_statutory_mapping_csv_list(db, request_frame, session_user)

    if type(request_frame) is bu_sm.UploadStatutoryMappingCSV:
        result = upload_statutory_mapping_csv(db, request_frame, session_user)

    elif type(request_frame) is bu_sm.GetStatutoryMappingBulkReportData:
        result = get_statutory_mapping_bulk_report_data(db, session_user)

    return result

########################################################
'''
    returns statutory mapping uploaded csv list
    :param
        db: database object
        request_frame: api request GetStatutoryMappingCsvUploadedList class object
        session_user: logged in user id
    :type
        db: Object
        request_frame: Object
        session_user: String
    :returns
        result: returns processed api response GetStatutoryMappingCsvUploadedListSuccess class Object
    rtype:
        result: Object
'''
########################################################

def get_statutory_mapping_csv_list(db, request_frame, session_user):

    upload_more, csv_data = get_uploaded_statutory_mapping_csv_list(db, session_user)
    result = bu_sm.GetStatutoryMappingCsvUploadedListSuccess(
        upload_more, csv_data
    )
    return result

########################################################
'''
    returns statutory mapping uploaded csv list
    :param
        db: database object
        request_frame: api request GetStatutoryMappingCsvUploadedList class object
        session_user: logged in user id
    :type
        db: Object
        request_frame: Object
        session_user: String
    :returns
        result: returns processed api response GetStatutoryMappingCsvUploadedListSuccess class Object
    rtype:
        result: Object
'''
########################################################

def get_statutory_mapping_bulk_report_data(db, session_user):

    # country_id = request_frame.country_id
    # domain_id = request_frame.domain_id
    # from_date = request_frame.from_date
    # to_date = request_frame.to_date
    # record_count = request_frame.record_count
    # page_count = request_frame.page_count

    # report_data= get_statutory_mapping_bulk_report_data_list(db, session_user, 
    #     country_id, domain_id, from_date, to_date, record_count, page_count)

    report_data= get_statutory_mapping_bulk_report_data_list(db, session_user)


    # result = bu_sm.GetStatutoryMappingBulkReportDataSuccess(
    #     country_id, domain_id, report_data, total_record
    # )
    result='resullll'
    return result


########################################################
'''
   save the file in csv folder after success full csv data validation
    :param
        db: database object
        request_frame: api request UploadStatutoryMappingCSV class object
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
########################################################

def upload_statutory_mapping_csv(db, request_frame, session_user):
    if request_frame.csv_size > 0 :
        pass
    # save csv file
    csv_file_path = convert_base64_to_file(
            BULKUPLOAD_CSV_PATH, request_frame.csv_name,
            request_frame.csv_data
        )
    # read data from csv file
    header, statutory_mapping_data = read_data_from_csv(csv_file_path)

    # csv data validation
    cObj = ValidateStatutoryMappingCsvData(
        db, statutory_mapping_data, request_frame.c_id, request_frame.d_id,
        request_frame.csv_name, header
    )
    res_data = cObj.perform_validation()

    # csv data save to temp db



    return result
