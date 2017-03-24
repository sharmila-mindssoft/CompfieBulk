import os
import datetime
import threading
from server import logger
from dateutil import relativedelta
from clientprotocol import (clientcore, clientuser, clienttransactions)
from server.clientdatabase.tables import *
from server.common import (
    datetime_to_string, string_to_datetime, new_uuid, get_date_time,
    string_to_datetime_with_time, convert_to_dict, get_date_time_in_date, encrypt
)
from server.clientdatabase.general import (
    is_two_levels_of_approval, calculate_ageing, is_space_available,
    save_compliance_activity, save_compliance_notification, is_primary_admin,
    get_user_email_name, convert_base64_to_file, update_used_space,
    convert_datetime_to_date,
    update_task_status_in_chart
)
from server.exceptionmessage import client_process_error
from server.emailcontroller import EmailHandler
from server.constants import (
    FORMAT_DOWNLOAD_URL, CLIENT_DOCS_BASE_PATH
)
__all__ = [
    "get_inprogress_count",
    "get_overdue_count",
    "get_current_compliances_list",
    "get_upcoming_count",
    "get_upcoming_compliances_list",
    "update_compliances",
    "get_on_occurrence_compliance_count",
    "get_on_occurrence_compliances_for_user",
    "start_on_occurrence_task",
    "getLastTransaction_Onoccurrence",
    "verify_password"
]

email = EmailHandler()

CLIENT_DOCS_DOWNLOAD_URL = "/client/client_documents"

#################################################################
# Compliance Task Details - Get inprogress count
#################################################################
def get_inprogress_count(db, session_user):
    param = [session_user]
    other_compliance_condition = " WHERE (frequency_id != 5 OR " + \
        " (frequency_id = 5 and duration_type_id=1) )" + \
        " AND completed_by=%s  AND " + \
        " ac.is_active = 1 AND " + \
        " IFNULL(ch.due_date, 0) >= current_date() " + \
        " AND IFNULL(ch.completed_on, 0) = 0 AND ch.current_status = 0 "
    on_occurrence_condition = " WHERE frequency_id = 5 " + \
        " and duration_type_id=2" + \
        " AND completed_by = %s AND " + \
        " ac.is_active = 1 AND " + \
        " IFNULL(ch.due_date, 0) >= now() " + \
        " AND IFNULL(ch.completed_on, 0) = 0 AND ch.current_status = 0"

    query = "SELECT count(*) as inprogress_count FROM tbl_compliance_history ch INNER JOIN " + \
        " tbl_assign_compliances ac " + \
        " ON (ch.compliance_id = ac.compliance_id " + \
        " and ac.unit_id = ch.unit_id) INNER JOIN " + \
        " tbl_compliances c ON (ch.compliance_id = c.compliance_id ) "

    other_compliance_rows = db.select_all(
        query + other_compliance_condition, param
    )
    on_occurrence_rows = db.select_all(query + on_occurrence_condition, param)
    other_compliance_count = other_compliance_rows[0]["inprogress_count"]
    on_occurrence_count = on_occurrence_rows[0]["inprogress_count"]
    return int(other_compliance_count) + int(on_occurrence_count)

#################################################################
# Compliance Task Details - Get overdue count
#################################################################
def get_overdue_count(db, session_user):
    query = "SELECT count(*) as occ FROM tbl_compliance_history ch INNER JOIN " + \
        " tbl_assign_compliances ac " + \
        " ON (ch.compliance_id = ac.compliance_id " + \
        " and ac.unit_id = ch.unit_id) INNER JOIN " + \
        " tbl_compliances c ON (ch.compliance_id = c.compliance_id) WHERE "
    param = [session_user]
    other_compliance_condition = " completed_by = %s " + \
        " AND (frequency_id != 5 OR " + \
        " (frequency_id = 5 and duration_type_id=1)) AND " + \
        " ac.is_active = 1 AND " + \
        " IFNULL(ch.due_date, 0) < current_date() AND " + \
        " IFNULL(ch.completed_on, 0) = 0 AND ch.current_status = 0 "

    on_occurrence_condition = " completed_by = %s " + \
        " AND frequency_id = 5 AND duration_type_id=2 AND " + \
        " ac.is_active = 1 AND " + \
        " IFNULL(ch.due_date, 0) < now() AND " + \
        " IFNULL(ch.completed_on, 0) = 0 AND ch.current_status = 0 "
    other_compliance_count = db.select_one(
        query + other_compliance_condition, param
    )["occ"]
    on_occurrence_count = db.select_one(
        query + on_occurrence_condition, param
    )["occ"]
    return int(other_compliance_count) + int(on_occurrence_count)

#################################################################
# Compliance Task Details - Get Current Compliances
#################################################################
def get_current_compliances_list(
    db, unit_id, current_start_count, to_count, session_user
):
    columns = [
        "compliance_history_id", "start_date", "due_date", "documents",
        "validity_date", "next_due_date",
        "document_name", "compliance_task", "compliance_description",
        "format_file", "unit", "domain_name", "frequency", "remarks",
        "compliance_id", "duration_type_id"
    ] 
    query = " SELECT * FROM " + \
        " (SELECT compliance_history_id, start_date, " + \
        " ch.due_date as due_date, documents, " + \
        " ch.validity_date, ch.next_due_date, ch.unit_id, document_name, " + \
        " compliance_task, compliance_description, format_file, " + \
        " (SELECT " + \
        " concat(unit_code, '-', unit_name, ',', address) " + \
        " FROM  tbl_units tu " + \
        " WHERE tu.unit_id = ch.unit_id) as unit, " + \
        " (SELECT  domain_name FROM tbl_domains td WHERE " + \
        " td.domain_id = c.domain_id) as domain_name, " + \
        " (SELECT domain_id FROM tbl_domains td WHERE " + \
        " td.domain_id = c.domain_id) as domain_id, " + \
        " (SELECT frequency FROM tbl_compliance_frequency " + \
        " WHERE frequency_id = c.frequency_id) as frequency, ch.remarks, " + \
        " ch.compliance_id, ac.assigned_on, c.frequency_id, ch.concurrence_status, ch.approve_status, ch.current_status, " + \
        " (select IFNULL(days,0) from tbl_validity_date_settings where country_id = c.country_id " + \
        " and domain_id = c.domain_id) as validity_settings_days, " + \
        " c.duration_type_id FROM tbl_compliance_history ch " + \
        " INNER JOIN tbl_assign_compliances ac " + \
        " ON (ac.unit_id = ch.unit_id " + \
        " AND ac.compliance_id = ch.compliance_id) " + \
        " INNER JOIN tbl_compliances c " + \
        " ON (ac.compliance_id = c.compliance_id) " + \
        " WHERE ch.completed_by = %s AND ch.current_status = 0 " + \
        " and ac.is_active = 1 and IFNULL(ch.completed_on, 0) = 0 " + \
        " and IFNULL(ch.due_date, 0) != 0 and IF(%s IS NOT NULL, ch.unit_id = %s,1) LIMIT %s, %s ) a " + \
        " ORDER BY due_date ASC "

    rows = db.select_all(query, [session_user, unit_id, unit_id, current_start_count, to_count])

    current_compliances_list = []
    for compliance in rows:
        document_name = compliance["document_name"]
        compliance_task = compliance["compliance_task"]
        compliance_name = compliance_task
        if document_name not in (None, "None", ""):
            compliance_name = "%s - %s" % (
                document_name, compliance_task
            )
        # print "compliance_name157>>", compliance_name
        unit_details = compliance["unit"].split(",")
        unit_name = unit_details[0]
        address = unit_details[1]
        no_of_days, ageing = calculate_ageing(
            due_date=compliance["due_date"],
            frequency_type=compliance["frequency_id"],
            duration_type=compliance["duration_type_id"]
        )

        # print "compliance[concurrence_status], compliance[approve_status]", compliance["compliance_history_id"] , compliance["concurrence_status"], compliance["approve_status"]
        #
        if compliance["concurrence_status"] == "2" or compliance["approve_status"] == "2" :
            compliance_status = clientcore.COMPLIANCE_STATUS("Rectify")
        else:
            if compliance["current_status"]== 0:
                compliance_status = clientcore.COMPLIANCE_STATUS("Inprogress")
            if "Overdue" in ageing:
                compliance_status = clientcore.COMPLIANCE_STATUS("Not Complied")


        # print "compliance_status>>", compliance["compliance_history_id"], compliance_status
        format_files = None
        if(
            compliance["format_file"] is not None and
            compliance["format_file"].strip() != ''
        ):
            format_files = ["%s/%s" % (
                    FORMAT_DOWNLOAD_URL, x
                ) for x in compliance["format_file"].split(",")]
        remarks = compliance["remarks"]
        # if remarks in ["None", None, ""]:
        #     remarks = None
        download_urls = []
        file_name = []
        if compliance["documents"] is not None and len(
                compliance["documents"]) > 0:
            for document in compliance["documents"].split(","):
                if document is not None and document.strip(',') != '':
                    # dl_url = "%s/%s/%s" % (
                    #     CLIENT_DOCS_DOWNLOAD_URL, str(client_id), document
                    download_urls.append(document)
                    file_name_part = document.split("-")[0]
                    file_extn_parts = document.split(".")
                    file_extn_part = None
                    if len(file_extn_parts) > 1:
                        file_extn_part = file_extn_parts[
                            len(file_extn_parts)-1
                        ]
                    if file_extn_part is not None:
                        name = "%s.%s" % (
                            file_name_part, file_extn_part
                        )
                        file_name.append(name)
                    else:
                        file_name.append(file_name_part)
        current_compliances_list.append(
            clientcore.ActiveCompliance(
                compliance_history_id=compliance["compliance_history_id"],
                compliance_name=compliance_name,
                compliance_frequency=clientcore.COMPLIANCE_FREQUENCY(
                    compliance["frequency"]
                ),
                domain_name=compliance["domain_name"],
                domain_id=compliance["domain_id"],
                unit_id=compliance["unit_id"],
                duration_type=compliance["duration_type_id"],
                validity_settings_days=compliance["validity_settings_days"],
                assigned_on=datetime_to_string(compliance["assigned_on"]),
                start_date=datetime_to_string(compliance["start_date"]),
                due_date=datetime_to_string(compliance["due_date"]),
                compliance_status=compliance_status,
                validity_date=None if (
                    compliance["validity_date"] == None
                ) else datetime_to_string(compliance["validity_date"]),
                next_due_date=None if (
                    compliance["next_due_date"] == None
                ) else datetime_to_string(compliance["next_due_date"]),
                ageing=ageing,
                format_file_name=format_files,
                unit_name=unit_name, address=address,
                compliance_description=compliance["compliance_description"],
                remarks=remarks,
                compliance_id=compliance["compliance_id"],
                download_url=download_urls, file_names=file_name
            )
        )
    return current_compliances_list
#############################################################
# Get Upcoming Compliances List - Count
#############################################################
def get_upcoming_count(db, unit_id, session_user):
    all_compliance_query = " SELECT ac.compliance_id, ac.unit_id " + \
        " FROM tbl_assign_compliances ac " + \
        " INNER JOIN tbl_compliances c " + \
        " ON (ac.compliance_id = c.compliance_id) " + \
        " WHERE " + \
        " assignee = %s AND frequency_id != 4 " + \
        " AND ac.due_Date < DATE_ADD(now(), INTERVAL 6 MONTH) " + \
        " AND ac.is_active = 1 "+ \
        " AND IF(%s IS NOT NULL, ac.unit_id = %s,1) "
    all_compliace_rows = db.select_all(all_compliance_query, [session_user, unit_id, unit_id])
    all_compliance_count = len(all_compliace_rows)
    onetime_query = " SELECT ch.compliance_id, ch.unit_id " + \
        " FROM tbl_compliance_history ch " + \
        " INNER JOIN tbl_compliances c " + \
        " on (ch.compliance_id =  c.compliance_id) " + \
        " WHERE frequency_id = 1 and completed_by = %s  " + \
        " AND IF(%s IS NOT NULL, ch.unit_id = %s,1) "
    onetime_rows = db.select_all(onetime_query, [session_user, unit_id, unit_id])

    combined_rows = []
    for combination in onetime_rows:
        if combination in all_compliace_rows:
            combined_rows.append(combination)
        else:
            continue

    count = len(combined_rows)
    return all_compliance_count - count

#############################################################
# Get Upcoming Compliances List
#############################################################
def get_upcoming_compliances_list(
    db, unit_id, upcoming_start_count, to_count, session_user
):
    query = "SELECT * FROM (SELECT ac.due_date, document_name, " + \
            " compliance_task, compliance_description, format_file, " + \
            " unit_code, unit_name, address, " + \
            " (select domain_name " + \
            " FROM tbl_domains d " + \
            " where d.domain_id = c.domain_id) as domain_name, " + \
            " DATE_SUB(ac.due_date, INTERVAL ac.trigger_before_days DAY) " + \
            " as start_date, ac.assigned_on " + \
            " FROM tbl_assign_compliances  ac " + \
            " INNER JOIN tbl_compliances c " + \
            " ON ac.compliance_id = c.compliance_id " + \
            " INNER JOIN tbl_units tu ON tu.unit_id = ac.unit_id " + \
            " WHERE assignee = %s AND frequency_id != 5 " + \
            " AND ac.due_Date < DATE_ADD(now(), INTERVAL 6 MONTH) " + \
            " AND ac.is_active = 1 " + \
            " AND IF(%s IS NOT NULL, tu.unit_id = %s,1) " + \
            " AND IF ( (frequency_id = 1 AND ( " + \
            " select count(*) from tbl_compliance_history ch " + \
            " where ch.compliance_id = ac.compliance_id and " + \
            " ch.unit_id = ac.unit_id ) >0), 0,1) ) a " + \
            " ORDER BY start_date ASC LIMIT %s, %s  "

    # print query, [session_user, int(upcoming_start_count), to_count]
    upcoming_compliances_rows = db.select_all(
        query, [session_user, unit_id, unit_id, int(upcoming_start_count), to_count]
    )
    columns = [
        "due_date", "document_name", "compliance_task",
        "description", "format_file", "unit_code", "unit_name", "address",
        "domain_name", "start_date", "assigned_on"
    ]
    # upcoming_compliances_result = convert_to_dict(
    #     upcoming_compliances_rows, columns
    # )
    upcoming_compliances_list = []
    # print "upcoming_compliances_rows >>>", upcoming_compliances_rows
    for compliance in upcoming_compliances_rows:
        document_name = compliance["document_name"]
        compliance_task = compliance["compliance_task"]
        compliance_name = compliance_task
        if document_name not in (None, "None", ""):
            compliance_name = "%s - %s" % (document_name, compliance_task)
        unit_name = "%s-%s" % (
            compliance["unit_code"], compliance["unit_name"]
        )
        address = compliance["address"]
        start_date = compliance["start_date"]
        format_files = None
        if(
            compliance["format_file"] is not None and
            compliance["format_file"].strip() != ''
        ):
            format_files = ["%s/%s" % (
                    FORMAT_DOWNLOAD_URL, x
                ) for x in compliance["format_file"].split(",")]
        upcoming_compliances_list.append(
            clientcore.UpcomingCompliance(
                compliance_name=compliance_name,
                domain_name=compliance["domain_name"],
                start_date=datetime_to_string(start_date),
                due_date=datetime_to_string(compliance["due_date"]),
                format_file_name=format_files,
                unit_name=unit_name,
                address=address,
                assigned_on=datetime_to_string(compliance["assigned_on"]),
                compliance_description=compliance["compliance_description"]
            ))
    return upcoming_compliances_list


def handle_file_upload(
    db, documents, uploaded_documents, old_documents
):
    document_names = []
    file_size = 0
    if documents is not None:
        if len(documents) > 0:
            for doc in documents:
                file_size += doc.file_size

            if is_space_available(db, file_size):
                for doc in documents:
                    # # file_name_parts = doc.file_name.split('.')
                    # name = None
                    # exten = None
                    # for index, file_name_part in enumerate(file_name_parts):
                    #     if index == len(file_name_parts) - 1:
                    #         exten = file_name_part
                    #     else:
                    #         if name is None:
                    #             name = file_name_part
                    #         else:
                    #             name += file_name_part
                    # auto_code = new_uuid()
                    # file_name = "%s-%s.%s" % (name, auto_code, exten)
                    file_name = doc.file_name
                    document_names.append(file_name)
                    # convert_base64_to_file(
                    #     file_name, doc.file_content, client_id
                    # )
                update_used_space(db, file_size)
            else:
                return clienttransactions.NotEnoughSpaceAvailable()

    # TO DO: Show Old uploaded documents
    # if old_documents is not None and len(old_documents) > 0:
    #     for document in old_documents.split(","):
    #         if document is not None and document.strip(',') != '':
    #             name = document.split("-")[0]
    #             document_parts = document.split(".")
    #             ext = document_parts[len(document_parts)-1]
    #             name = "%s.%s" % (name, ext)
    #             # if name not in uploaded_documents:
    #             #     # path = "%s/%s/%s" % (
    #             #     #    CLIENT_DOCS_BASE_PATH, client_id, document
    #             #     # )
    #             #     # remove_uploaded_file(path)
    #             # else:
    #             #     document_names.append(document)
    #             document_names.append(document)
    return document_names


def is_diff_greater_than_90_days(validity_date, next_due_date):
    if validity_date not in [None, "None", ""]:
        validity_date = string_to_datetime(validity_date)
    else:
        validity_date = None
    if next_due_date not in [None, "None", ""]:
        next_due_date = string_to_datetime(next_due_date)
    else:
        next_due_date = None

    if None not in [validity_date, next_due_date]:
        r = relativedelta.relativedelta(
            convert_datetime_to_date(validity_date),
            convert_datetime_to_date(next_due_date)
        )
        if abs(r.months) > 3 or abs(r.years) > 0:
            #  Difference should not be more than 90 days
            return False
        else:
            return True
    else:
        return True

##################################################
# Update Compliances
##################################################
def update_compliances(
    db, compliance_history_id, documents, uploaded_compliances,
    completion_date, validity_date, next_due_date, assignee_remarks,
    session_user
):
    current_time_stamp = get_date_time_in_date()
    query = " SELECT legal_entity_id, unit_id, tch.compliance_id,  completed_by, " + \
        " ifnull(concurred_by, 0) as concurred, approved_by, " + \
        " compliance_task, document_name, " + \
        " due_date, frequency_id, duration_type_id, documents " + \
        " FROM tbl_compliance_history tch " + \
        " INNER JOIN tbl_compliances tc " + \
        " ON (tc.compliance_id=tch.compliance_id) " + \
        " WHERE compliance_history_id=%s "
    param = [compliance_history_id]
    row = db.select_one(query, param)
    columns = [
        "unit_id", "compliance_id", "completed_by", "concurred_by",
        "approved_by", "compliance_name", "document_name", "due_date",
        "frequency_id", "duration_type_id", "documents"
    ]
    # result = convert_to_dict(rows, columns)
    # row = result[0]
    compliance_task = row["compliance_task"]

    if not is_diff_greater_than_90_days(validity_date, next_due_date):
        return False
    # document_names = handle_file_upload(
    #     db, documents, uploaded_compliances, row["documents"])
    document_names = handle_file_upload(
        db, documents, documents, row["documents"])

    if type(document_names) is not list:
        return document_names
    #On Occurrence hourly compliances    
    if row["frequency_id"] == 5 and str(row["duration_type_id"]) == "2":
        completion_date = string_to_datetime_with_time(completion_date)
    else:
        completion_date = string_to_datetime(completion_date).date()
    ageing, remarks = calculate_ageing(
        row["due_date"], frequency_type=None, completion_date=completion_date,
        duration_type=row["duration_type_id"]
    )
    history_columns = [
        "completion_date", "documents", "remarks", "completed_on", "current_status"
    ]

    is_two_levels = is_two_levels_of_approval(db)

    if is_two_levels:
        current_status = "1"
    else:
        current_status = "2"

    history_values = [
        completion_date, ",".join(document_names),
        assignee_remarks, current_time_stamp, current_status
    ]
    if validity_date not in ["", None, "None"]:
        history_columns.append("validity_date")
        validity_date = string_to_datetime(validity_date).date()
        history_values.append(validity_date)
    if next_due_date not in ["", None, "None"]:
        history_columns.append("next_due_date")
        next_due_date = string_to_datetime(next_due_date).date()
        history_values.append(next_due_date)

    history_condition = "compliance_history_id = %s " + \
        " and completed_by = %s "
    history_condition_val = [compliance_history_id, session_user]
    # if(
    #     # row["completed_by"] == row["approved_by"] or
    #     # is_primary_admin(db, row["completed_by"])
    #     # row["completed_by"] == row["approved_by"]
    # ):
        # history_columns.extend(["approve_status", "approved_on"])
        # history_values.extend([1, current_time_stamp])
        # if row["concurred_by"] not in [None, 0, ""]:
        #     history_columns.extend(["concurrence_status", "concurred_on"])
        #     history_values.extend([1, current_time_stamp])
    as_columns = []
    as_values = []
    if next_due_date is not None:
        as_columns.append("due_date")
        as_values.append(next_due_date)
    if validity_date is not None:
        as_columns.append("validity_date")
        as_values.append(validity_date)
    # if frequency_id in (1, "1"):
    #     as_columns.append("is_active")
    #     as_values.append(0)

    # as_condition = " unit_id = %s and compliance_id = %s "
    # as_values.extend([unit_id, compliance_id])
    # db.update(
    #     tblAssignedCompliances, as_columns, as_values, as_condition
    # )
    save_compliance_activity(
        db, row["unit_id"], row["compliance_id"], compliance_history_id,
        session_user, current_time_stamp, "Submitted", assignee_remarks
    )
    # else:
    #     save_compliance_activity(
    #         db, row["unit_id"], row["compliance_id"], compliance_history_id,
    #         session_user, current_time_stamp, "Submitted", assignee_remarks
    #     )

    history_values.extend(history_condition_val)

    update_status = db.update(
        tblComplianceHistory, history_columns, history_values,
        history_condition
    )

    # Audit Log Entry
    action = "Upload Compliances \"%s\"" % (compliance_task)
    db.save_activity(session_user, 35, action, row["legal_entity_id"], row["unit_id"])

    if(update_status is False):
        return clienttransactions.ComplianceUpdateFailed()
    if row["completed_by"] == row["approved_by"]:
        notify_users(
            db, row["document_name"], row["compliance_task"],
            row["completed_by"],  row["approved_by"]
        )
    return True




def notify_users(
    db, document_name, compliance_task, assignee_id,  approver_id
):
    compliance_name = compliance_task
    if(
        document_name is not None and
        document_name != '' and document_name != 'None'
    ):
        compliance_name = "%s - %s" % (document_name, compliance_task)

    assignee_email, assignee_name = get_user_email_name(
        db, str(assignee_id)
    )
    approver_email, approver_name = get_user_email_name(
        db, str(approver_id)
    )
    action = "approve"
    notification_text = "%s has completed the " + \
        " compliance %s. Review and approve"
    notification_text = notification_text % (
            assignee_name, compliance_name
        )
    concurrence_email, concurrence_name = (None, None)
    if(
        is_two_levels_of_approval(db) and
        concurrence_id not in [None, "None", 0, "", "null", "Null"]
    ):
        concurrence_email, concurrence_name = get_user_email_name(
            db, str(concurrence_id)
        )
        action = "Concur"
        notification_text = "%s has completed the " + \
            " compliance %s. Review and concur"
        notification_text = notification_text % (
                assignee_name, compliance_name
            )
    save_compliance_notification(
        db, compliance_history_id, notification_text,
        "Compliance Completed", action
    )
    notify_task_completed_thread = threading.Thread(
        target=email.notify_task_completed, args=[
            assignee_email, assignee_name, concurrence_email,
            concurrence_name, approver_email, approver_name, action,
            is_two_levels_of_approval(db), compliance_name
        ]
    )
    notify_task_completed_thread.start()

#####################################################
# Get Onoccurrence Compliance Count
#####################################################
def get_on_occurrence_compliance_count(
    db, session_user, user_domain_ids, user_unit_ids
):
    query = "SELECT count(*) as total_count" + \
            " FROM tbl_assign_compliances ac " + \
            " INNER JOIN tbl_compliances c " + \
            " ON (ac.compliance_id = c.compliance_id) " + \
            " INNER JOIN tbl_units u ON (ac.unit_id = u.unit_id) " + \
            " WHERE u.is_closed = 0 " + \
            " AND find_in_set(ac.unit_id, %s) " + \
            " AND find_in_set(c.domain_id, %s) " + \
            " AND c.frequency_id = 5 " + \
            " AND ac.assignee = %s "
    rows = db.select_one(query, [
        ",".join(str(x) for x in user_unit_ids),
        ",".join(str(x) for x in user_domain_ids), session_user
    ])
    return rows["total_count"]

##########################################################
# Get Onoccurrence Compliances
##########################################################
def get_on_occurrence_compliances_for_user(
    db, session_user, user_domain_ids, user_unit_ids, start_count,
    to_count
):
    columns = [
        "compliance_id", "statutory_provision",
        "compliance_task", "compliance_description",
        "duration_type", "duration", "document_name", "unit_id", "unit_name"
    ]
    # concat_columns = "concat(unit_code, '-', unit_name)"

    query = "SELECT ac.compliance_id, c.statutory_provision, " + \
            " compliance_task, compliance_description, " + \
            " duration_type, duration, document_name, u.unit_id, " + \
            " concat(u.unit_code, '-', u.unit_name) AS unit_name " + \
            " FROM tbl_assign_compliances ac " + \
            " INNER JOIN tbl_compliances c " + \
            " ON (ac.compliance_id = c.compliance_id) " + \
            " INNER JOIN tbl_compliance_duration_type cd " + \
            " ON (c.duration_type_id = cd.duration_type_id) " + \
            " INNER JOIN tbl_units u ON (ac.unit_id = u.unit_id) " + \
            " WHERE u.is_closed = 0 " + \
            " AND find_in_set(ac.unit_id, %s) " + \
            " AND find_in_set(c.domain_id,%s) " + \
            " AND c.frequency_id = 5 " + \
            " AND ac.assignee = %s " + \
            " ORDER BY u.unit_id, document_name, compliance_task " + \
            " LIMIT %s, %s "

    rows = db.select_all(query, [
        ",".join(str(x) for x in user_unit_ids),
        ",".join(str(x) for x in user_domain_ids),
        session_user, int(start_count), int(to_count)
    ])
    unit_wise_compliances = {}
    for row in rows:
        duration = "%s %s" % (row["duration"], row["duration_type"])
        compliance_name = row["compliance_task"]
        if row["document_name"] not in ["None", "", None]:
            compliance_name = "%s - %s" % (
                row["document_name"], compliance_name
            )
        unit_name = row["unit_name"]
        if unit_name not in unit_wise_compliances:
            unit_wise_compliances[unit_name] = []
        unit_wise_compliances[unit_name].append(
            clientuser.ComplianceOnOccurrence(
                row["compliance_id"], row["statutory_provision"],
                compliance_name, row["compliance_description"],
                duration, row["unit_id"]
            )
        )
    return unit_wise_compliances

###################################################
# Start Onoccurrence Compliances
###################################################
def start_on_occurrence_task(
    db, legal_entity_id, compliance_id, start_date, unit_id, duration, remarks, session_user
):
    columns = [
        "legal_entity_id", "unit_id", "compliance_id",
        "start_date", "due_date", "completed_by", "occurrence_remarks"
    ]
    start_date = string_to_datetime_with_time(start_date)
    duration = duration.split(" ")
    duration_value = duration[0]
    duration_type = duration[1]
    due_date = None
    if duration_type == "Day(s)":
        due_date = start_date + datetime.timedelta(days=int(duration_value))
    elif duration_type == "Hour(s)":
        due_date = start_date + datetime.timedelta(hours=int(duration_value))
    values = [
        legal_entity_id, unit_id, compliance_id, start_date, due_date,
        session_user, remarks
    ]

    q = "select t2.compliance_id, t3.country_id, t1.domain_id, t1.compliance_task, t1.document_name, t2.approval_person, " + \
        "t2.concurrence_person from tbl_assign_compliances as t2 " + \
        " inner join tbl_compliances as t1 on t2.compliance_id = t1.compliance_id " + \
        " inner join tbl_units as t3 on t2.unit_id = t3.unit_id " + \
        " where t2.compliance_id = %s and t2.unit_id = %s "

    row = db.select_one(q, [compliance_id, unit_id])
    approver_id = row.get("approval_person")
    concurrence_id = row.get("concurrence_person")
    compliance_name = row.get("compliance_task")
    document_name = row.get("document_name")
    country_id = row.get("country_id")
    domain_id = row.get("domain_id")

    if is_two_levels_of_approval(db):
        columns.append("concurred_by")
        values.append(concurrence_id)
    columns.append("approved_by")
    values.append(approver_id)

    compliance_history_id = db.insert(
        tblComplianceHistory, columns, values
    )
    if compliance_history_id is False:
        raise client_process_error("E017")

    users = [session_user, approver_id]
    if concurrence_id is not None :
        users.append(concurrence_id)

    if due_date is not None:
        update_task_status_in_chart(db, country_id, domain_id, unit_id, due_date, users)

    # Audit Log Entry
    action = "Compliances started \"%s\"" % (compliance_name)
    db.save_activity(session_user, 35, action, legal_entity_id, unit_id)

    # user_ids = "{},{},{}".format(assignee_id, concurrence_id, approver_id)
    assignee_email, assignee_name = get_user_email_name(db, str(session_user))
    approver_email, approver_name = get_user_email_name(db, str(approver_id))
    if (
        concurrence_id not in [None, "None", 0, "", "null", "Null"] and
        is_two_levels_of_approval(db)
    ):
        concurrence_email, concurrence_name = get_user_email_name(
            db, str(concurrence_id)
        )
    if document_name not in (None, "None", ""):
        compliance_name = "%s - %s" % (document_name, compliance_name)
    notification_text = "Compliance task %s has started" % compliance_name
    save_compliance_notification(
        db, compliance_history_id, notification_text, "Compliance Started",
        "Started"
    )
    try:
        notify_on_occur_thread = threading.Thread(
            target=email.notify_task, args=[
                assignee_email, assignee_name,
                concurrence_email, concurrence_name,
                approver_email, approver_name, compliance_name,
                due_date, "Start"
            ]
        )
        notify_on_occur_thread.start()
    except Exception, e:
        logger.logClient("error", "clientdatabase.py-start-on-occurance", e)
        print "Error sending email: %s" % (e)
    return True

def remove_uploaded_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
##################################################
# Verify password - Pop Confirmation
##################################################
def verify_password(db, user_id, password):
    ec_password = encrypt(password)
    q = "SELECT username from tbl_user_login_details where user_id = %s and password = %s"
    #print q
    data_list = db.select_one(q, [user_id, ec_password])
    if data_list is None:
        return True
    else:
        return False

def get_compliance_history_details(
    db, compliance_history_id
):
    compliance_column = "(select compliance_task from %s c " + \
        " where c.compliance_id = ch.compliance_id ) " + \
        " as compliance_name "
    compliance_column = compliance_column % tblCompliances
    document_name_column = "(select document_name from %s c " + \
        " where c.compliance_id = ch.compliance_id ) " + \
        " as doc_name"
    document_name_column = document_name_column % tblCompliances
    columns = [
        "completed_by", "ifnull(concurred_by, 0) as concurred", "approved_by",
        compliance_column, document_name_column, "due_date"
    ]
    condition = "compliance_history_id = %s "
    condition_val = [compliance_history_id]
    rows = db.get_data(
        tblComplianceHistory + " ch", columns, condition,
        condition_val
    )
    if rows:
        return rows[0]


def is_onOccurrence_with_hours(db, compliance_history_id):
    columns = "compliance_id"
    condition = "compliance_history_id = %s"
    condition_val = [compliance_history_id]
    rows = db.get_data(
        tblComplianceHistory, columns, condition, condition_val
    )
    compliance_id = rows[0]["compliance_id"]

    comp_columns = "frequency_id, duration_type_id"
    comp_condition = "compliance_id = %s"
    comp_condition_val = [compliance_id]
    comp_rows = db.get_data(
        tblCompliances, comp_columns, comp_condition, comp_condition_val
    )
    frequency_id = comp_rows[0]["frequency_id"]
    duration_type_id = comp_rows[0]["duration_type_id"]
    if frequency_id == 4 and duration_type_id == 2:
        return True
    else:
        return False

#####################################################
# Onoccurrence Compliances - Get Last 5 Transactions
#####################################################
def getLastTransaction_Onoccurrence(db, compliance_id, unit_id):
    q = " SELECT ch.compliance_history_id,ch.compliance_id,com.compliance_task, " + \
        " substring(substring(com.statutory_mapping,3),1,char_length(com.statutory_mapping) -4) as statutory, " + \
        " (SELECT concat(unit_code,' - ',unit_name) FROM tbl_units where unit_id = ch.unit_id) as unit, " + \
        " com.compliance_description,ch.start_date, " + \
        " (SELECT concat(employee_code,' - ',employee_name) FROM tbl_users where user_id = ch.completed_by) as assignee,ch.completion_date, " + \
        " (SELECT concat(employee_code,' - ',employee_name) FROM tbl_users where user_id = ch.concurred_by) as concurr,ch.concurred_on, " + \
        " (SELECT concat(employee_code,' - ',employee_name) FROM tbl_users where user_id = ch.approved_by) as approver,ch.approved_on, " + \
        " (CASE WHEN (IF(com.frequency_id = 5,ch.due_date >= ch.completion_date,date(ch.due_date) >= date(ch.completion_date)) " + \
        " and (ifnull(ch.approve_status,0) = 1 OR ifnull(ch.approve_status,0) = 3)) THEN 'Complied' " + \
        " WHEN (IF(com.frequency_id = 5,ch.due_date < ch.completion_date,date(ch.due_date) < date(ch.completion_date)) " +\
        " and (ifnull(ch.approve_status,0) = 1 OR ifnull(ch.approve_status,0) = 3)) THEN 'Delayed Compliance' " + \
        " WHEN (IF(com.frequency_id = 5,ch.due_date < ch.completion_date, date(ch.due_date) < date(ch.completion_date))) THEN 'Over due' " + \
        " WHEN (IF(com.frequency_id = 5,ch.due_date >= ch.completion_date, date(ch.due_date) >= date(ch.completion_date))) THEN 'In Progress' " + \
        " WHEN (IF(com.frequency_id = 5,ch.start_date < now(), date(ch.start_date) < curdate())) THEN 'In progress' " + \
        " ELSE 'Pending' END) as compliance_status " + \
        " FROM tbl_compliance_history as ch " + \
        " LEFT JOIN tbl_compliances as com on ch.compliance_id = com.compliance_id " + \
        " WHERE ch.compliance_id = %s and ch.unit_id = %s " + \
        " ORDER BY ch.compliance_history_id desc limit 5" ;

    row = db.select_all(q, [compliance_id, unit_id])
    return row
