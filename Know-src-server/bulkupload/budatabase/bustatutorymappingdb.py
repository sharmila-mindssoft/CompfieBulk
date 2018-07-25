from server.exceptionmessage import fetch_error
import traceback
from server import logger
from ..buapiprotocol import bustatutorymappingprotocol as bu_sm
import datetime
import mysql.connector
from server.dbase import Database
from server.constants import (
    KNOWLEDGE_DB_HOST, KNOWLEDGE_DB_PORT, KNOWLEDGE_DB_USERNAME,
    KNOWLEDGE_DB_PASSWORD, KNOWLEDGE_DATABASE_NAME,
)
from ..bulkconstants import (
    MAX_REJECTED_COUNT, CSV_DELIMITER, BULK_UPLOAD_DB_HOST,
    BULK_UPLOAD_DB_PORT, BULK_UPLOAD_DB_USERNAME, BULK_UPLOAD_DB_PASSWORD,
    BULK_UPLOAD_DATABASE_NAME
)


__all__ = [
    "get_uploaded_statutory_mapping_csv_list",
    "fetch_statutory_bulk_report",
    "save_mapping_csv", "save_mapping_data",
    "get_pending_mapping_list",
    "get_filters_for_approve",
    "get_statutory_mapping_by_filter",
    "update_approve_action_from_list",
    "get_statutory_mapping_by_csv_id",
    "fetch_rejected_statutory_mapping_bulk_report",
    "process_delete_rejected_sm_csv_id",
    "update_download_count_by_csvid",
    "fetch_rejected_sm_download_csv_report",
    "get_sm_csv_file_name_by_id",
    "save_action_from_view",
    "get_pending_action",
    "delete_action_after_approval",
    "get_rejected_sm_file_count",
    "get_domains_for_user_bu",
    "get_countries_for_user_bu",
    "get_knowledge_executive_bu",
    "get_sm_document_count",
    "get_update_approve_file_status",
    "get_sm_csv_name",
]

# transaction method begin

#############################################################################
# To get domains configured under a user
# Parameter(s) : Object of database, user id
# Return Type : List of Object of Domain
#############################################################################


def get_domains_for_user_bu(user_id):
    _source_db_con = connect_knowledge_db()
    _source_db = Database(_source_db_con)
    _source_db.begin()
    result = _source_db.call_proc_with_multiresult_set(
        'sp_tbl_domains_for_user', (user_id,), 3
    )
    result.pop(0)
    return return_domains_bu(result)


############################################################################
# To convert the data fetched from database into List of object of Domain
# Parameter(s) : Data fetched from database
# Return Type : List of Object of Domain
############################################################################
def return_country_list_of_domain_bu(domain_id, countries):
    c_ids = []
    c_names = []
    for c in countries:
        if int(c["domain_id"]) == domain_id:
            c_ids.append(int(c["country_id"]))
            c_names.append(c["country_name"])

    return c_ids, c_names


def return_domains_bu(data):
    results = []
    for d in data[0]:
        d_id = d["domain_id"]
        c_ids, c_names = return_country_list_of_domain_bu(d_id, data[1])
        results.append(bu_sm.Domain(
            c_ids, c_names, d_id, d["domain_name"], bool(d["is_active"])
        ))
    return results


#############################################################################
# To get countries configured under a user
# Parameter(s) : Object of database, user id
# Return Type : List of Object of Countries
#############################################################################
def get_countries_for_user_bu(user_id):
    _source_db_con = connect_knowledge_db()
    _source_db = Database(_source_db_con)
    _source_db.begin()
    result = _source_db.call_proc_with_multiresult_set(
        "sp_countries_for_user", [user_id], 2
    )
    if len(result) > 1:
        result = result[1]
    return return_countries_bu(result)


###############################################################################
# To convert the data fetched from database into List of object of Country
# Parameter(s) : Data fetched from database
# Return Type : List of Object of Country
###############################################################################
def return_countries_bu(data):
    results = []
    for d in data:
        results.append(bu_sm.Country(
            d["country_id"], d["country_name"], bool(d["is_active"])
        ))
    return results


def get_knowledge_executive_bu(manager_id):
    _source_db_con = connect_knowledge_db()
    _source_db = Database(_source_db_con)
    _source_db.begin()
    result = _source_db.call_proc("sp_know_executive_info", [manager_id])
    user_info = {}
    for r in result:
        userid = r.get("child_user_id")
        u = user_info.get(userid)
        emp_name = "%s - %s" % (r.get("employee_code"), r.get("employee_name"))
        if u is None:
            u = bu_sm.KExecutiveInfo(
                [r.get("country_id")], [r.get("domain_id")],
                emp_name, r.get("child_user_id")
            )
            user_info[userid] = u

        else:
            c_ids = user_info.get(userid).c_ids
            c_ids.append(r.get("country_id"))
            d_ids = user_info.get(userid).d_ids
            d_ids.append(r.get("domain_id"))

            user_info[userid].c_ids = c_ids
            user_info[userid].d_ids = d_ids

    return user_info.values()

########################################################
# Return the uploaded statutory mapping csv list
# param db: database class object
# type db : Object
# param session_user: user id who currently logged in
# type session_user: String
# returns: upload_mmore: flag which defines user upload rights
# returns: csv_data: list of uploaded csv_data
# rtypes: Boolean, lsit of Object
########################################################


def get_uploaded_statutory_mapping_csv_list(db, session_user):
    csv_data = []
    upload_more = True
    doc_names = {}
    data = db.call_proc_with_multiresult_set(
        "sp_statutory_mapping_csv_list", [session_user], 3
    )
    if len(data) == 3:
        if data[0][0]["max_count"] >= MAX_REJECTED_COUNT:
            upload_more = False
        else:
            upload_more = True

        for d in data[2]:
            csv_id = d.get("csv_id")
            docname = d.get("format_file")
            doc_list = doc_names.get(csv_id)
            if doc_list is None:
                doc_list = [docname]
            else:
                doc_list.append(docname)
            doc_names[csv_id] = doc_list

        for d in data[1]:
            # csv_name = d.get("csv_name").split('_')
            # csvname = "_".join(csv_name[:-1])
            upload_on = d.get("uploaded_on").strftime("%d-%b-%Y %H:%M")

            csv_data.append(bu_sm.CsvList(
                d.get("country_id"), d.get("country_name"), d.get("domain_id"),
                d.get("domain_name"),
                d.get("csv_id"), d.get("csv_name"), d.get("total_records"),
                d.get("total_documents"),
                d.get("uploaded_documents"), upload_on,
                doc_names.get(d.get("csv_id"))
            ))

    return upload_more, csv_data


########################################################
'''
    returns new primary key from table
   :param
        db: database object
        args: list of procedure params
   :type
        db: Object
        args: List
   :returns
        result: return new id
    rtype:
        result: Integer
'''
########################################################


def save_mapping_csv(args):
    db = connect_bulk_db()
    newid = db.call_insert_proc("sp_statutory_mapping_csv_save", args)
    db.commit()
    return newid


########################################################
'''
    returns true if the data save properply
   :param
        db: database object
        csv_id: parent table id
        csv_data: list of data to save
   :type
        db: Object
        csv_id: Integer
        csv_data: List
   :returns
        result: return boolean
    rtype:
        result: Boolean
'''
########################################################


def save_mapping_data(csv_id, csv_data):
    try:
        columns = [
            "csv_id", "s_no", "organization", "geography_location",
            "statutory_nature", "statutory", "statutory_provision",
            "compliance_task", "compliance_document",
            "compliance_description",
            "penal_consequences", "reference_link", "compliance_frequency",
            "statutory_month", "statutory_date", "trigger_before",
            "repeats_every", "repeats_type", "repeat_by", "duration",
            "duration_type",
            "multiple_input", "format_file", "task_id", "task_type"
        ]
        values = []

        for idx, d in enumerate(csv_data):
            values.append((
                csv_id, idx + 1, d["Organization"], d["Applicable_Location"],
                d["Statutory_Nature"], d["Statutory"],
                d["Statutory_Provision"],
                d["Compliance_Task"], d["Compliance_Document"],
                d["Compliance_Description"], d["Penal_Consequences"],
                d["Reference_Link"], d["Compliance_Frequency"],
                d["Statutory_Month"],
                d["Statutory_Date"], d["Trigger_Days"],
                None if d["Repeats_Every"] == '' else d["Repeats_Every"],
                d["Repeats_Type"],
                None if d["Repeats_By (DOM/EOM)"] == '' else
                d["Repeats_By (DOM/EOM)"],
                None if d["Duration"] == '' else d["Duration"],
                d["Duration_Type"], d["Multiple_Input_Selection"],
                d["Format"], d["Task_ID"], d["Task_Type"],
            ))

        if values:
            db = connect_bulk_db()
            db.bulk_insert("tbl_bulk_statutory_mapping", columns, values)
            db.commit()
            return True
        else:
            return False
    except Exception, e:
        print str(e)
        raise ValueError("Transaction failed")


def remove_white_spaces(v):
    if v.find("|;|") > 0:
        v = "|;|".join(e.strip() for e in v.split("|;|"))
    return v

########################################################
'''
    returns statutory mapping csv list which waiting for approval
   :param
        db: database object
        session_user: logged in user details
   :type
        db: Object
        session_user: Object
   :returns
        result: list of pending csv data Object
    rtype:
        result: List
'''
########################################################


def get_pending_mapping_list(db, cid, did, uploaded_by, session_user):
    csv_data = []
    _source_db_con = connect_knowledge_db()
    _source_db = Database(_source_db_con)
    _source_db.begin()
    result = _source_db.call_proc(
        "sp_bu_get_mapped_knowledge_executives",
        [session_user.user_id(), cid, did]
    )
    _source_db_con.close()
    mapped_executives = ''
    if len(result) != 0:
        mapped_executives = ",".join(str(r["child_user_id"]) for r in result)

    if uploaded_by is None:
        uploaded_by = mapped_executives
    data = db.call_proc("sp_pending_statutory_mapping_csv_list", [
        uploaded_by, cid, did
    ])

    for d in data:
        # file_name = d["csv_name"].split('.')
        # remove_code = file_name[0].split('_')
        # csv_name = "%s.%s" % ('_'.join(remove_code[:-1]), file_name[1])
        upload_on = d["uploaded_on"].strftime("%d-%b-%Y %H:%M")
        csv_data.append(bu_sm.PendingCsvList(
            d["csv_id"], d["csv_name"], d["uploaded_by"],
            upload_on, d["total_records"], d["approve_count"],
            d["rej_count"],
            d["csv_name"], d["declined_count"], d["file_submit_status"]
        ))

    return csv_data

########################################################
'''
    returns select fileds in list for the given csv id
   :param
        db: database object
        csv_id: viewed csv id
   :type
        db: Object
        csv_id: INT
   :returns
        result: return filtered list in Api Object
    rtype:
        result: Object
'''
########################################################


def get_filters_for_approve(db, csv_id):
    data = db.call_proc_with_multiresult_set(
        "sp_statutory_mapping_filter_list", [csv_id], 10
    )
    org_names = []
    s_natures = []
    statutories = []
    frequencies = []
    geo_locations = []
    c_tasks = []
    c_descs = []
    c_docs = []
    task_ids = []
    task_types = []
    if len(data) > 0:
        if len(data[0]) > 0:
            for d in data[0]:
                organization = remove_white_spaces(d["organization"])
                org_names.extend(organization.strip().split('|;|'))
                org_names = list(set(org_names))

        if len(data[1]) > 0:
            for d in data[1]:
                s_natures.append(d["statutory_nature"])

        if len(data[2]) > 0:
            for d in data[2]:
                statutory = remove_white_spaces(d["statutory"])
                statutories.extend(statutory.strip().split('|;|'))
                statutories = list(set(statutories))

        compliance_frequency = get_all_compliance_frequency()
        if len(compliance_frequency) > 0:
            for d in compliance_frequency:
                frequencies.append(d["frequency"])

        if len(data[4]) > 0:
            for d in data[4]:
                geography_loc = remove_white_spaces(d["geography_location"])
                geo_locations.extend(
                    geography_loc.strip().split('|;|')
                )
                geo_locations = list(set(geo_locations))

        if len(data[5]) > 0:
            for d in data[5]:
                c_tasks.append(d["compliance_task"])

        if len(data[6]) > 0:
            for d in data[6]:
                c_descs.append(d["compliance_description"])

        if len(data[7]) > 0:
            for d in data[7]:
                c_docs.append(d["compliance_document"])

        if len(data[8]) > 0:
            for d in data[8]:
                task_ids.append(d["task_id"])

        if len(data[9]) > 0:
            for d in data[9]:
                task_types.append(d["task_type"])

    return bu_sm.GetApproveMappingFilterSuccess(
        org_names, s_natures, statutories, frequencies, geo_locations,
        c_tasks, c_descs, c_docs,
        task_ids, task_types
    )


def get_statutory_mapping_by_filter(db, request_frame):
    csv_id = request_frame.csv_id
    organization = request_frame.orga_name
    s_nature = request_frame.s_nature
    frequency = request_frame.f_types
    statutory = request_frame.statutory
    geo_location = request_frame.geo_location
    c_task = request_frame.c_task_name
    c_desc = request_frame.c_desc
    c_doc = request_frame.c_doc
    f_count = request_frame.f_count
    f_range = request_frame.r_range
    task_id = request_frame.tsk_id
    task_type = request_frame.tsk_type
    view_data = request_frame.filter_view_data

    if organization is None or organization == "":
        organization = '%'
    else:
        organization = '%' + organization + '%'

    if s_nature is None or s_nature == "":
        s_nature = '%'

    if frequency is None or frequency == "" or len(frequency) == 0:
        frequency = '%'
    else:
        frequency = ",".join(frequency)

    if statutory is None or statutory == "":
        statutory = '%'
    else:
        statutory = statutory + '%'

    if geo_location is None or geo_location == "":
        geo_location = '%'
    else:
        geo_location = geo_location + '%'

    if task_id is None or task_id == "":
        task_id = '%'
    else:
        task_id = task_id + '%'
    if task_type is None or task_type == "":
        task_type = '%'
    else:
        task_type = task_type + '%'

    if c_task is None or c_task == "":
        c_task = '%'

    if c_desc is None or c_desc == "":
        c_desc = '%'

    if c_doc is None or c_doc == "":
        c_doc = '%'

    data = db.call_proc_with_multiresult_set(
        "sp_statutory_mapping_view_by_filter",
        [
            csv_id, organization, s_nature, frequency,
            statutory, geo_location, c_task, c_desc, c_doc,
            f_count, f_range, task_id, task_type, view_data
        ], 2
    )
    country_name = None
    domain_name = None
    csv_name = None
    upload_by = None
    upload_on = None
    total = 0
    mapping_data = []
    if len(data) > 0:
        if len(data[1]) > 0:
            total = data[1][0]["total"]
        if len(data[0]) > 0:
            compliance = data[0]
            for idx, d in enumerate(compliance):
                if idx == 0:
                    country_name = d["country_name"]
                    domain_name = d["domain_name"]
                    csv_name = d["csv_name"]
                    upload_on = d["uploaded_on"].strftime("%d-%b-%Y %H:%M")
                    upload_by = d["uploaded_by"]

                mapping_data.append(bu_sm.MappingData(
                    d["bulk_statutory_mapping_id"],
                    d["organization"], d["geography_location"],
                    d["statutory_nature"], d["statutory"],
                    d["statutory_provision"], d["compliance_task"],
                    d["compliance_document"], d["compliance_description"],
                    d["penal_consequences"], d["reference_link"],
                    d["compliance_frequency"], d["statutory_month"],
                    d["statutory_date"], d["trigger_before"],
                    d["repeats_every"],
                    d["repeats_type"], d["repeat_by"], d["duration"],
                    d["duration_type"],
                    d["multiple_input"], d["format_file"],
                    d["action"], d["remarks"],
                    d["task_id"], d["task_type"],
                ))

    return bu_sm.GetApproveStatutoryMappingViewSuccess(
        country_name, domain_name, csv_name, upload_by,
        upload_on, csv_id, mapping_data, total
    )


def get_statutory_mapping_by_csv_id(db, request_frame):
    csv_id = request_frame.csv_id
    f_count = request_frame.f_count
    f_range = request_frame.r_range
    data = db.call_proc("sp_statutory_mapping_view_by_csvid", [
        csv_id, f_count, f_range
    ])
    country_name = None
    domain_name = None
    csv_name = None
    upload_by = None
    upload_on = None
    total = None
    mapping_data = []
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep',
              'Oct', 'Nov', 'Dec']
    if len(data) > 0:
        for idx, d in enumerate(data):
            statu_months = ''
            if idx == 0:
                country_name = d["country_name"]
                domain_name = d["domain_name"]
                csv_name = d["csv_name"]
                upload_on = d["uploaded_on"].strftime("%d-%b-%Y %H:%M")
                upload_by = d["uploaded_by"]
                total = d["total_records"]

            statutory_date = d["statutory_date"].replace(CSV_DELIMITER, ", ")
            trigger_before = d["trigger_before"].replace(CSV_DELIMITER, ", ")
            statu_month = d["statutory_month"].replace(CSV_DELIMITER, ",")

            if statu_month != '' and len(statu_month) >= 1:
                smonth_list = statu_month.split(",")
                smonth_list = ','.join(
                    str(x).rstrip().lstrip() for x in smonth_list
                )
                smonth_list = smonth_list.split(",")
                statu_months = []
                mon = None
                for smon in smonth_list:
                    i = 0
                    for index, mon in enumerate(months):
                        i = i + 1
                        smon = smon.lstrip()
                        smon = smon.rstrip()
                        if i == int(smon):
                            statu_months.append(str(mon))
                statu_months = ', '.join(str(x) for x in statu_months)
            else:
                statu_months = ''

            mapping_data.append(bu_sm.MappingData(
                d["bulk_statutory_mapping_id"],
                d["organization"], d["geography_location"],
                d["statutory_nature"], d["statutory"],
                d["statutory_provision"], d["compliance_task"],
                d["compliance_document"], d["compliance_description"],
                d["penal_consequences"], d["reference_link"],
                d["compliance_frequency"], statu_months,
                statutory_date, trigger_before, d["repeats_every"],
                d["repeats_type"], d["repeat_by"], d["duration"],
                d["duration_type"], d["multiple_input"], d["format_file"],
                d["action"], d["remarks"], d["task_id"], d["task_type"],
            ))
    return bu_sm.GetApproveStatutoryMappingViewSuccess(
        country_name, domain_name, csv_name, upload_by,
        upload_on, csv_id, mapping_data, total
    )


def update_approve_action_from_list(
    csv_id, action, remarks, session_user, action_type
):
    try:
        if action_type == "all":
            args = [csv_id, action, remarks, session_user]
            db = connect_bulk_db()
            db.call_proc("sp_statutory_mapping_update_all_action", args)
            db.commit()
            return True
        else:
            args = [csv_id, session_user]
            db = connect_bulk_db()
            db.call_proc("sp_statutory_update_action", args)
            db.commit()
            return True

    except Exception, e:
        logger.logKnowledge(
            "error", "update action from list", str(traceback.format_exc())
        )
        logger.logKnowledge("error", "update action from list", str(e))
        raise fetch_error()


def delete_action_after_approval(csv_id):
    try:
        args = [csv_id]
        db = connect_bulk_db()
        db.call_proc("sp_statutory_mapping_delete", args)
        db.commit()
        return True

    except Exception, e:
        logger.logKnowledge(
            "error", "update action from list", str(traceback.format_exc())
        )
        logger.logKnowledge("error", "update action from list", str(e))
        raise fetch_error()


def save_action_from_view(db, csv_id, sm_id, action, remarks):
    try:
        args = [csv_id, sm_id, action, remarks]
        db.call_proc("sp_approve_mapping_action_save", args)
        return True

    except Exception, e:
        logger.logKnowledge(
            "error", "update action from view", str(traceback.format_exc())
        )
        logger.logKnowledge("error", "update action from view", str(e))
        raise fetch_error()


def get_pending_action(db, csv_id):
    data = db.call_proc("sp_statutory_action_pending_count", [csv_id])
    if data[0].get("pending_count") > 0:
        return True
    else:
        return False


def get_update_approve_file_status(csv_id, file_status):
    db = connect_bulk_db()
    db.call_proc("sp_update_approve_file_status", [csv_id, file_status])
    db.commit()
    return True
#  transaction method end


#########################################
# Retrieved Statutory Mapping Report Data
#########################################

def fetch_statutory_bulk_report(
        db, user_id, country_ids, domain_ids, from_date, to_date,
        record_count, page_count, dependent_users):
    report_data = []
    expected_result = 2
    domain_id_list = ",".join(map(str, domain_ids))
    country_id_list = ",".join(map(str, country_ids))

    if len(dependent_users) >= 1:
        user_ids = ",".join(map(str, dependent_users))
    else:
        user_ids = user_id

    args = [user_ids, country_id_list, domain_id_list, from_date, to_date,
            record_count, page_count]
    data = db.call_proc_with_multiresult_set(
        'sp_statutory_mappings_bulk_reportdata', args, expected_result)

    if data:
        response_report_data = data[0]
        total_record = data[1][0]["total"]
        for d in response_report_data:
            uploaded_on = None
            approved_on = None
            rejected_on = None

            if d["uploaded_on"] is not None:
                uploaded_on = d["uploaded_on"].strftime("%d-%b-%Y %H:%M")

            if d["approved_on"] is not None:
                approved_on = d["approved_on"].strftime("%d-%b-%Y %H:%M")

            if d["rejected_on"] is not None:
                rejected_on = d["rejected_on"].strftime("%d-%b-%Y %H:%M")

            report_data.append(bu_sm.ReportData(
                d["country_name"], d["domain_name"],
                d["uploaded_by"], uploaded_on, d["csv_name"],
                d["total_records"], d["total_rejected_records"],
                d["approved_by"], d["rejected_by"], approved_on,
                rejected_on, d["is_fully_rejected"],
                d["total_approve_records"], str(d["rejected_reason"]),
                d["declined_count"]))
    else:
        report_data = []
        total_record = 0
    return report_data, total_record


###########################################################
#    Retreived only rejected statutory mapping report data
###########################################################

def fetch_rejected_statutory_mapping_bulk_report(
    db, user_id, country_id, domain_id
):

    rejected_list = []
    args = [country_id, domain_id, user_id]
    data = db.call_proc('sp_rejected_statutory_mapping_reportdata', args)

    response_format = '%Y-%m-%d %H:%M:%S'
    # requestFormat = '%Y-%m-%d %H:%M:%S'
    request_format = '%d-%b-%Y %H:%M'
    date_time = datetime.datetime
    for d in data:
        approved_on = ''
        uploaded_on = ''
        rejected_on = ''
        if d["uploaded_on"] is not None:
            uploaded_on = date_time.strptime(str(
                d["uploaded_on"]), response_format).strftime(request_format)

        if d["approved_on"] is not None:
            approved_on = date_time.strptime(str(
                d["approved_on"]), response_format).strftime(request_format)

        if d["rejected_on"] is not None:
            rejected_on = approved_on = date_time.strptime(str(
                d["rejected_on"]), response_format).strftime(request_format)

        if d["rejected_file_download_count"] is None:
            download_count = 0
        else:
            download_count = d["rejected_file_download_count"]

        rejected_list.append(bu_sm.StatutoryMappingRejectData(
            int(d["csv_id"]), int(d["uploaded_by"]), str(uploaded_on),
            str(d["csv_name"]), int(d["total_records"]),
            d["total_rejected_records"], d["approved_by"],
            d["rejected_by"], str(approved_on), str(rejected_on),
            d["is_fully_rejected"], int(d["approve_status"]),
            int(download_count), str(d["remarks"]), d["action"],
            d["declined_count"], d["rejected_reason"]
        ))
    return rejected_list


################################################################
# retreiving rejected statutory mapping data for download action
################################################################

def fetch_rejected_sm_download_csv_report(
        db, user_id, country_id, domain_id, csv_id
):
    args = [country_id, domain_id, user_id, csv_id]
    data = db.call_proc('sp_rejected_sm_csv_report', args)
    return data


########################################################################
# Deleting rejected statutory mapping for request csv id
# Change Approve Status is 4 when deleting csv record
# And retrieving rejected statutory mapping data for data refresh action
#########################################################################

def process_delete_rejected_sm_csv_id(
    db, user_id, country_id, domain_id, csv_id
):
    args = [csv_id]
    db.call_proc('sp_delete_reject_sm_by_csvid', args)
    rejected_list = fetch_rejected_statutory_mapping_bulk_report(
        db, user_id, country_id, domain_id
    )
    return rejected_list


###########################################
# Update download count for request csv id
###########################################

def update_download_count_by_csvid(db, csv_id):
    updated_count = []
    args = [csv_id]
    data = db.call_proc('sp_update_download_count_by_csvid', args)
    for d in data:
        updated_count.append(bu_sm.SMRejectUpdateDownloadCount(
            int(d["csv_id"]), int(d["rejected_file_download_count"])
        ))
    return updated_count

################################################################
# Retrived CSV file name for request csv id - Download file name
################################################################


def get_sm_csv_file_name_by_id(db, csv_id):
    args = [csv_id]
    data = db.call_proc('sp_get_sm_csv_file_name_by_id', args)
    return data[0]["csv_name"]


################################################################
# To Get the Rejected File Count to prevent from uploading
################################################################


def get_rejected_sm_file_count(db, session_user):
    result = db.call_proc(
        "sp_sm_rejected_file_count", [session_user.user_id()]
    )
    rej_count = result[0]["rejected"]
    return rej_count


def get_sm_document_count(db, csv_id):
    result = db.call_proc(
        "sp_get_document_count", [csv_id]
    )
    document_count = result[0]["document_count"]
    return document_count


def get_sm_csv_name(db, csv_id):
    result = db.call_proc(
        "sp_get_sm_csv_name", [csv_id]
    )
    csv_name = result[0]["csv_name"]
    return csv_name


def get_all_compliance_frequency():
    _source_db_con = connect_knowledge_db()
    _source_db = Database(_source_db_con)
    _source_db.begin()
    result = _source_db.call_proc('sp_bu_compliance_frequency')
    return result


def connect_knowledge_db():
    try:
        _source_db_con = mysql.connector.connect(
            user=KNOWLEDGE_DB_USERNAME,
            password=KNOWLEDGE_DB_PASSWORD,
            host=KNOWLEDGE_DB_HOST,
            database=KNOWLEDGE_DATABASE_NAME,
            port=KNOWLEDGE_DB_PORT,
            autocommit=False,
        )
        return _source_db_con
    except Exception, e:
        print "Connection Exception Caught"
        print e


def connect_bulk_db():
    _bulk_db = None
    try:
        _bulk_db_con = mysql.connector.connect(
            user=BULK_UPLOAD_DB_USERNAME,
            password=BULK_UPLOAD_DB_PASSWORD,
            host=BULK_UPLOAD_DB_HOST,
            database=BULK_UPLOAD_DATABASE_NAME,
            port=BULK_UPLOAD_DB_PORT,
            autocommit=False
        )
        _bulk_db = Database(_bulk_db_con)
        _bulk_db.begin()
    except Exception, e:
        print "Connection Exception Caught"
        print e
    return _bulk_db
