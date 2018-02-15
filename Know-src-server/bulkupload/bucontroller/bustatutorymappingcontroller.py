from ..bucsvvalidation.statutorymappingvalidation import ValidateStatutoryMappingCsvData
from ..buapiprotocol import bustatutorymappingprotocol as bu_sm
from ..budatabase.bustatutorymappingdb import *
from ..bulkuploadcommon import (
    convert_base64_to_file,
    read_data_from_csv
)
import datetime
from server.constants import BULKUPLOAD_CSV_PATH
# from server.jsontocsvconverter import ConvertJsonToCSV
# from server.constants import (
#     FILE_TYPES,
#     FILE_MAX_LIMIT, KNOWLEDGE_FORMAT_PATH,
#     CLIENT_DOCS_BASE_PATH,
#     BULKUPLOAD_CSV_PATH
# )


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
        result = get_statutory_mapping_csv_list(db, request_frame, session_user)

    if type(request_frame) is bu_sm.UploadStatutoryMappingCSV:
        result = upload_statutory_mapping_csv(db, request_frame, session_user)

    if type(request_frame) is bu_sm.GetStatutoryMappingBulkReportData:
        result = get_statutory_mapping_bulk_report_data(db, request_frame, session_user)
    
    # if type(request_frame) is bu_sm.ExportStatutoryMappingBulkReportData:
    #     result = process_statutory_bulk_report(db, request_frame, session_user)
        

    return result

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

        if res_data["doc_count"] == 0 :
            upload_sts = 1
        else :
            upload_sts = 0

        csv_args = [
            request_frame.uploadedby_name, request_frame.c_id,
            request_frame.d_id, request_frame.c_name,
            request_frame.d_name, csv_name,
            res_data["total"], res_data["doc_count"], upload_sts
        ]
        # new_csv_id = save_mapping_csv(db, csv_args)
        # if new_csv_id :
        #     if save_mapping_data(db, new_csv_id, res_data["data"]) is True :
        #         result = bu_sm.UploadStatutoryMappingCSVSuccess(
        #             res_data["total"], res_data["valid"], res_data["invalid"],
        #             res_data["doc_count"], res_data["doc_names"]
        #         )

        # csv data save to temp db
    else :
        result = bu_sm.UploadStatutoryMappingCSVFailed(
            res_data["invalid_file"], res_data["mandatory_error"],
            res_data["max_length_error"], res_data["duplicate_error"],
            res_data["invalid_char_error"], res_data["invalid_data_error"],
            res_data["inactive_error"], res_data["total"], res_data["invalid"]
        )

    return result

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

def get_statutory_mapping_bulk_report_data(db, request_frame, session_user):


    country_ids=request_frame.c_ids
    domain_ids=request_frame.d_ids   
    from_date=request_frame.from_date
    to_date=request_frame.to_date
    
    record_count=request_frame.r_count
    page_count=request_frame.p_count

    user_id=session_user.user_id()


    from_date = datetime.datetime.strptime(from_date, '%d-%b-%Y')
    to_date = datetime.datetime.strptime(to_date, '%d-%b-%Y')
    
    reportdata, total_record = fetch_statutory_mapping_bulk_report(db, session_user.user_id(), 
    user_id, country_ids, domain_ids, from_date, to_date, record_count, page_count)
    # reportdata=result[0]
    # total_record=result[1]
    
    result = bu_sm.GetStatutoryMappingBulkReportDataSuccess(reportdata,total_record)
    return result

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
