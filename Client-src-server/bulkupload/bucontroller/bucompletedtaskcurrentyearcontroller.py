import traceback
from ..bucsvvalidation.completedtaskcurrentyearvalidation import (
    ValidateStatutoryMappingCsvData,
    ValidateStatutoryMappingForApprove
)
# from ..bucsvvalidation.rejectedstatutorymapping import ValidateRejectedSMBulkCsvData
from..buapiprotocol import bucompletedtaskcurrentyearprotocol as bu_ct
from ..budatabase.bucompletedtaskcurrentyeardb import *
from ..client_bulkuploadcommon import (
    convert_base64_to_file,
    read_data_from_csv,
    generate_valid_file
)
# from ..client_bulkexport import ConvertJsonToCSV
import datetime
from server.constants import BULKUPLOAD_CSV_PATH
from server.exceptionmessage import fetch_error
# from protocol import generalprotocol, technoreports
__all__ = [
    "process_bu_completed_task_current_year_request"
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
def process_bu_completed_task_current_year_request(request, db, session_user):
    request_frame = request.request

    if type(request_frame) is bu_sm.GetCompletedTask_Domains:
        result = get_completed_task_legal_domains(db, request_frame,
                                                session_user)

    elif type(request) is bu_sm.GetDownloadData:
        result = process_get_download_data(
            db, request, session_user
        )
    return result

########################################################
def get_completed_task_legal_domains(db, request_frame, session_user):

    domains = get_legal_entity_domains(db, request_frame.le_id)
    result = bu_ct.GetStatutoryMappingCsvUploadedListSuccess(domains)
    return result


########################################################
# To get the compliances under the selected filters
# Completed Task - Current Year (Past Data)
########################################################
def process_get_download_data(
        db, request, session_user
):
    # to_count = RECORD_DISPLAY_COUNT
    unit_id = request.unit_id
    domain_id = request.domain_id
    compliance_frequency = request.compliance_frequency
    # country_id = request.country_id
    start_count = request.start_count
    # country_id
    statutory_wise_compliances, total_count = get_statutory_wise_compliances(
        db, unit_id, domain_id, level_1_statutory_name,
        compliance_frequency, session_user, start_count,
        to_count
    )
    users = get_users_by_unit_and_domain(db, unit_id, domain_id)
    return clienttransactions.GetStatutoriesByUnitSuccess(
        statutory_wise_compliances=statutory_wise_compliances,
        users=users, total_count=total_count
    )
