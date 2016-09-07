import os
import datetime
import threading
from server import logger
from dateutil import relativedelta
from protocol import (core, clientuser, clienttransactions)
from server.clientdatabase.tables import *
from server.common import (
    datetime_to_string, string_to_datetime, new_uuid, get_date_time,
    string_to_datetime_with_time, convert_to_dict, get_date_time_in_date
)
from server.clientdatabase.general import (
    is_two_levels_of_approval, calculate_ageing, is_space_available,
    save_compliance_activity, save_compliance_notification, is_primary_admin,
    get_user_email_name, convert_base64_to_file, update_used_space,
    convert_datetime_to_date
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
    "start_on_occurrence_task"
]

email = EmailHandler()

CLIENT_DOCS_DOWNLOAD_URL = "/client/client_documents"

def get_inprogress_count(db, session_user):
    param = [session_user]
    other_compliance_condition = " WHERE (frequency_id != 4 OR " + \
        " (frequency_id = 4 and duration_type_id=1) )" + \
        " AND completed_by=%s  AND " + \
        " ac.is_active = 1 AND " + \
        " IFNULL(ch.due_date, 0) >= current_date() " + \
        " AND IFNULL(ch.completed_on, 0) = 0"
    on_occurrence_condition = " WHERE frequency_id = 4 " + \
        " and duration_type_id=2" + \
        " AND completed_by = %s AND " + \
        " ac.is_active = 1 AND " + \
        " IFNULL(ch.due_date, 0) >= now() " + \
        " AND IFNULL(ch.completed_on, 0) = 0"

    query = "SELECT count(*) FROM tbl_compliance_history ch INNER JOIN " + \
        " tbl_assigned_compliances ac " + \
        " ON (ch.compliance_id = ac.compliance_id " + \
        " and ac.unit_id = ch.unit_id) INNER JOIN " + \
        " tbl_compliances c ON (ch.compliance_id = c.compliance_id ) "

    other_compliance_rows = db.select_all(
        query + other_compliance_condition, param
    )
    on_occurrence_rows = db.select_all(query + on_occurrence_condition, param)
    other_compliance_count = other_compliance_rows[0][0]
    on_occurrence_count = on_occurrence_rows[0][0]
    return int(other_compliance_count) + int(on_occurrence_count)


def get_overdue_count(db, session_user):
    query = "SELECT count(*) FROM tbl_compliance_history ch INNER JOIN " + \
        " tbl_assigned_compliances ac " + \
        " ON (ch.compliance_id = ac.compliance_id " + \
        " and ac.unit_id = ch.unit_id) INNER JOIN " + \
        " tbl_compliances c ON (ch.compliance_id = c.compliance_id) WHERE "
    param = [session_user]
    other_compliance_condition = " completed_by = %s " + \
        " AND (frequency_id != 4 OR " + \
        " (frequency_id = 4 and duration_type_id=1)) AND " + \
        " ac.is_active = 1 AND " + \
        " IFNULL(ch.due_date, 0) < current_date() AND " + \
        " IFNULL(ch.completed_on, 0) = 0 "

    on_occurrence_condition = " completed_by = %s " + \
        " AND frequency_id = 4 AND duration_type_id=2 AND " + \
        " ac.is_active = 1 AND " + \
        " IFNULL(ch.due_date, 0) < now() AND " + \
        " IFNULL(ch.completed_on, 0) = 0 "
    other_compliance_count = db.select_one(
        query + other_compliance_condition, param
    )[0]
    on_occurrence_count = db.select_one(
        query + on_occurrence_condition, param
    )[0]
    return int(other_compliance_count) + int(on_occurrence_count)


def get_current_compliances_list(
    db, current_start_count, to_count, session_user, client_id
):
    columns = [
        "compliance_history_id", "start_date", "due_date", "documents",
        "validity_date", "next_due_date",
        "document_name", "compliance_task", "description",
        "format_file", "unit", "domain_name", "frequency", "remarks",
        "compliance_id", "duration_type_id"
    ]
    query = " SELECT * FROM " + \
        " (SELECT compliance_history_id, start_date, " + \
        " ch.due_date as due_date, documents, " + \
        " ch.validity_date, ch.next_due_date, document_name, " + \
        " compliance_task, compliance_description, format_file, " + \
        " (SELECT " + \
        " concat(unit_code, '-', unit_name, ',', address) " + \
        " FROM  tbl_units tu " + \
        " WHERE tu.unit_id = ch.unit_id) as unit, " + \
        " (SELECT  domain_name FROM tbl_domains td WHERE " + \
        " td.domain_id = c.domain_id) as domain_name, " + \
        " (SELECT frequency FROM tbl_compliance_frequency " + \
        " WHERE frequency_id = c.frequency_id), ch.remarks, " + \
        " ch.compliance_id, " + \
        " duration_type_id FROM tbl_compliance_history ch " + \
        " INNER JOIN tbl_assigned_compliances ac " + \
        " ON (ac.unit_id = ch.unit_id " + \
        " AND ac.compliance_id = ch.compliance_id) " + \
        " INNER JOIN tbl_compliances c " + \
        " ON (ac.compliance_id = c.compliance_id) " + \
        " WHERE ch.completed_by = %s " + \
        " and ac.is_active = 1 and IFNULL(ch.completed_on, 0) = 0 " + \
        " and IFNULL(ch.due_date, 0) != 0 LIMIT %s, %s ) a " + \
        " ORDER BY due_date ASC "

    rows = db.select_all(query, [session_user, current_start_count, to_count])
    current_compliances_row = convert_to_dict(rows, columns)
    current_compliances_list = []
    for compliance in current_compliances_row:
        document_name = compliance["document_name"]
        compliance_task = compliance["compliance_task"]
        compliance_name = compliance_task
        if document_name not in (None, "None", ""):
            compliance_name = "%s - %s" % (
                document_name, compliance_task
            )
        unit_details = compliance["unit"].split(",")
        unit_name = unit_details[0]
        address = unit_details[1]
        no_of_days, ageing = calculate_ageing(
            due_date=compliance["due_date"],
            frequency_type=compliance["frequency"],
            duration_type=compliance["duration_type_id"]
        )
        compliance_status = core.COMPLIANCE_STATUS("Inprogress")
        if "Overdue" in ageing:
            compliance_status = core.COMPLIANCE_STATUS("Not Complied")
        format_files = None
        if(
            compliance["format_file"] is not None and
            compliance["format_file"].strip() != ''
        ):
            format_files = ["%s/%s" % (
                    FORMAT_DOWNLOAD_URL, x
                ) for x in compliance["format_file"].split(",")]
        remarks = compliance["remarks"]
        if remarks in ["None", None, ""]:
            remarks = None
        download_urls = []
        file_name = []
        if compliance["documents"] is not None and len(
                compliance["documents"]) > 0:
            for document in compliance["documents"].split(","):
                if document is not None and document.strip(',') != '':
                    dl_url = "%s/%s/%s" % (
                        CLIENT_DOCS_DOWNLOAD_URL, str(client_id), document
                    )
                    download_urls.append(dl_url)
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
            core.ActiveCompliance(
                compliance_history_id=compliance["compliance_history_id"],
                compliance_name=compliance_name,
                compliance_frequency=core.COMPLIANCE_FREQUENCY(
                    compliance["frequency"]
                ),
                domain_name=compliance["domain_name"],
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
                compliance_description=compliance["description"],
                remarks=remarks,
                compliance_id=compliance["compliance_id"],
                download_url=download_urls, file_names=file_name
            )
        )
    return current_compliances_list


def get_upcoming_count(db, session_user):
    all_compliance_query = " SELECT ac.compliance_id, ac.unit_id " + \
        " FROM tbl_assigned_compliances ac " + \
        " INNER JOIN tbl_compliances c " + \
        " ON (ac.compliance_id = c.compliance_id) " + \
        " WHERE " + \
        " assignee = %s AND frequency_id != 4 " + \
        " AND ac.due_Date < DATE_ADD(now(), INTERVAL 6 MONTH) " + \
        " AND ac.is_active = 1;"
    all_compliace_rows = db.select_all(all_compliance_query, [session_user])
    all_compliance_count = len(all_compliace_rows)
    onetime_query = " SELECT ch.compliance_id, ch.unit_id " + \
        " FROM tbl_compliance_history ch " + \
        " INNER JOIN tbl_compliances c " + \
        " on (ch.compliance_id =  c.compliance_id) " + \
        " WHERE frequency_id = 1 and completed_by = %s ;"
    onetime_rows = db.select_all(onetime_query, [session_user])

    combined_rows = []
    for combination in onetime_rows:
        if combination in all_compliace_rows:
            combined_rows.append(combination)
        else:
            continue

    count = len(combined_rows)
    return all_compliance_count - count


def get_upcoming_compliances_list(
    db, upcoming_start_count, to_count, session_user, client_id
):
    query = "SELECT * FROM (SELECT ac.due_date, document_name, " + \
            " compliance_task, compliance_description, format_file, " + \
            " unit_code, unit_name, address, " + \
            " (select domain_name " + \
            " FROM tbl_domains d " + \
            " where d.domain_id = c.domain_id) as domain_name, " + \
            " DATE_SUB(ac.due_date, INTERVAL ac.trigger_before_days DAY) " + \
            " as start_date " + \
            " FROM tbl_assigned_compliances  ac " + \
            " INNER JOIN tbl_compliances c " + \
            " ON ac.compliance_id = c.compliance_id " + \
            " INNER JOIN tbl_units tu ON tu.unit_id = ac.unit_id " + \
            " WHERE assignee = %s AND frequency_id != 4 " + \
            " AND ac.due_Date < DATE_ADD(now(), INTERVAL 6 MONTH) " + \
            " AND ac.is_active = 1 AND IF ( (frequency_id = 1 AND ( " + \
            " select count(*) from tbl_compliance_history ch " + \
            " where ch.compliance_id = ac.compliance_id and " + \
            " ch.unit_id = ac.unit_id ) >0), 0,1) ) a " + \
            " ORDER BY start_date ASC LIMIT %s, %s  "
    upcoming_compliances_rows = db.select_all(
        query, [session_user, int(upcoming_start_count), to_count]
    )
    columns = [
        "due_date", "document_name", "compliance_task",
        "description", "format_file", "unit_code", "unit_name", "address",
        "domain_name", "start_date"
    ]
    upcoming_compliances_result = convert_to_dict(
        upcoming_compliances_rows, columns
    )
    upcoming_compliances_list = []
    for compliance in upcoming_compliances_result:
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
            core.UpcomingCompliance(
                compliance_name=compliance_name,
                domain_name=compliance["domain_name"],
                start_date=datetime_to_string(start_date),
                due_date=datetime_to_string(compliance["due_date"]),
                format_file_name=format_files,
                unit_name=unit_name,
                address=address,
                compliance_description=compliance["description"]
            ))
    return upcoming_compliances_list


def handle_file_upload(
    db, documents, uploaded_documents, client_id, old_documents
):
    document_names = []
    file_size = 0
    if documents is not None:
        if len(documents) > 0:
            for doc in documents:
                file_size += doc.file_size

            if is_space_available(db, file_size):
                for doc in documents:
                    file_name_parts = doc.file_name.split('.')
                    name = None
                    exten = None
                    for index, file_name_part in enumerate(file_name_parts):
                        if index == len(file_name_parts) - 1:
                            exten = file_name_part
                        else:
                            if name is None:
                                name = file_name_part
                            else:
                                name += file_name_part
                    auto_code = new_uuid()
                    file_name = "%s-%s.%s" % (name, auto_code, exten)
                    document_names.append(file_name)
                    convert_base64_to_file(
                        file_name, doc.file_content, client_id
                    )
                update_used_space(db, file_size)
            else:
                return clienttransactions.NotEnoughSpaceAvailable()

    if old_documents is not None and len(old_documents) > 0:
        for document in old_documents.split(","):
            if document is not None and document.strip(',') != '':
                name = document.split("-")[0]
                document_parts = document.split(".")
                ext = document_parts[len(document_parts)-1]
                name = "%s.%s" % (name, ext)
                if name not in uploaded_documents:
                    path = "%s/%s/%s" % (
                       CLIENT_DOCS_BASE_PATH, client_id, document
                    )
                    remove_uploaded_file(path)
                else:
                    document_names.append(document)
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


def update_compliances(
    db, compliance_history_id, documents, uploaded_compliances,
    completion_date, validity_date, next_due_date, assignee_remarks,
    client_id, session_user
):
    current_time_stamp = get_date_time_in_date()
    query = " SELECT unit_id, tch.compliance_id,  completed_by, " + \
        " ifnull(concurred_by, 0) as concurred, approved_by, " + \
        " compliance_task, document_name, " + \
        " due_date, frequency_id, duration_type_id, documents " + \
        " FROM tbl_compliance_history tch " + \
        " INNER JOIN tbl_compliances tc " + \
        " ON (tc.compliance_id=tch.compliance_id) " + \
        " WHERE compliance_history_id=%s "
    param = [compliance_history_id]
    rows = db.select_all(query, param)
    columns = [
        "unit_id", "compliance_id", "completed_by", "concurred_by",
        "approved_by", "compliance_name", "document_name", "due_date",
        "frequency_id", "duration_type_id", "documents"
    ]
    result = convert_to_dict(rows, columns)
    row = result[0]

    if not is_diff_greater_than_90_days(validity_date, next_due_date):
        return False
    document_names = handle_file_upload(
        db, documents, uploaded_compliances, client_id, row["documents"])
    if type(document_names) is not list:
        return document_names
    if row["frequency_id"] == 4 and row["duration_type_id"] == 2:
        completion_date = string_to_datetime(completion_date)
    else:
        completion_date = string_to_datetime(completion_date).date()
    ageing, remarks = calculate_ageing(
        row["due_date"], frequency_type=None, completion_date=completion_date,
        duration_type=row["duration_type_id"]
    )
    history_columns = [
        "completion_date", "documents", "remarks", "completed_on"
    ]
    history_values = [
        completion_date, ",".join(document_names),
        assignee_remarks, current_time_stamp
    ]
    if validity_date not in ["", None, "None"]:
        history_columns.append("validity_date")
        history_values.append(validity_date)
    if next_due_date not in ["", None, "None"]:
        history_columns.append("next_due_date")
        history_values.append(next_due_date)

    history_condition = "compliance_history_id = %s " + \
        " and completed_by = %s "
    history_condition_val = [compliance_history_id, session_user]
    if(
        row["completed_by"] == row["approved_by"] or
        is_primary_admin(db, row["completed_by"])
    ):
        history_columns.extend(["approve_status", "approved_on"])
        history_values.extend([1, current_time_stamp])
        if row["concurred_by"] not in [None, 0, ""]:
            history_columns.extend(["concurrence_status", "concurred_on"])
            history_values.extend([1, current_time_stamp])
        as_columns = []
        as_values = []
        if next_due_date is not None:
            as_columns.append("due_date")
            as_values.append(next_due_date)
        if validity_date is not None:
            as_columns.append("validity_date")
            as_values.append(validity_date)
        if frequency_id in (1, "1"):
            as_columns.append("is_active")
            as_values.append(0)

        as_condition = " unit_id = %s and compliance_id = %s "
        as_values.extend([unit_id, compliance_id])
        db.update(
            tblAssignedCompliances, as_columns, as_values, as_condition
        )
        save_compliance_activity(
            db, row["unit_id"], row["compliance_id"],
            "Approved", "Complied", assignee_remarks
        )
    else:
        save_compliance_activity(
            db, row["unit_id"], row["compliance_id"],
            "Submitted", "Inprogress", assignee_remarks
        )

    history_values.extend(history_condition_val)
    update_status = db.update(
        tblComplianceHistory, history_columns, history_values,
        history_condition
    )
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


def update_compliances1(
    db, compliance_history_id, documents, completion_date,
    validity_date, next_due_date, remarks, client_id, session_user
):
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
    # Hanling upload
    document_names = handle_file_upload(db, documents, client_id)
    if type(document_names) is not list:
        return document_names
    history = get_compliance_history_details(db, compliance_history_id)
    assignee_id = history["completed_by"]
    concurrence_id = history["concurred"]
    approver_id = history["approved_by"]
    compliance_name = history["compliance_name"]
    document_name = history["doc_name"]
    due_date = history["due_date"]
    current_time_stamp = get_date_time_in_date()
    history_columns = [
        "completion_date", "documents", "remarks", "completed_on"
    ]
    if is_onOccurrence_with_hours(db, compliance_history_id):
        completion_date = string_to_datetime(completion_date)
    else:
        completion_date = string_to_datetime(completion_date).date()
    history_values = [
        completion_date,
        ",".join(document_names),
        remarks,
        current_time_stamp
    ]
    if validity_date not in ["", None, "None"]:
        history_columns.append("validity_date")
        history_values.append(validity_date)
    if next_due_date not in ["", None, "None"]:
        history_columns.append("next_due_date")
        history_values.append(next_due_date)
    history_condition = "compliance_history_id = %s " + \
        " and completed_by = %s "
    history_condition_val = [compliance_history_id, session_user]
    columns = "unit_id, compliance_id"
    condition = "compliance_history_id = %s "
    rows = db.get_data(
        tblComplianceHistory, columns, condition, [compliance_history_id]
    )
    unit_id = rows[0]["unit_id"]
    compliance_id = rows[0]["compliance_id"]
    ageing, remarks = calculate_ageing(
        due_date, frequency_type=None,
        completion_date=completion_date,
        duration_type=None
    )
    if(
        assignee_id == approver_id or
        is_primary_admin(db, assignee_id)
    ):
        history_columns.extend(
            [
                "approve_status", "approved_on"
            ]
        )
        history_values.extend([1, current_time_stamp])
        if concurrence_id not in [None, 0, ""]:
            history_columns.extend(
                ["concurrence_status", "concurred_on"]
            )
            history_values.extend([1, current_time_stamp])

        query = "SELECT frequency_id " + \
            " FROM tbl_compliances tc WHERE tc.compliance_id = %s "

        rows = db.select_one(query, [compliance_id])
        columns = ["frequency_id"]
        rows = convert_to_dict(rows, columns)
        frequency_id = int(rows["frequency_id"]) if(
            rows["frequency_id"] is not None) else None
        as_columns = []
        as_values = []
        if next_due_date is not None:
            as_columns.append("due_date")
            as_values.append(next_due_date)
        if validity_date is not None:
            as_columns.append("validity_date")
            as_values.append(validity_date)
        if frequency_id in (1, "1"):
            as_columns.append("is_active")
            as_values.append(0)

        as_condition = " unit_id = %s and compliance_id = %s "
        as_values.extend([unit_id, compliance_id])
        if(
            len(as_columns) > 0 and len(as_values) > 0 and
            len(as_columns) == len(as_values)
        ):
            db.update(
                tblAssignedCompliances, as_columns, as_values, as_condition
            )
        save_compliance_activity(
            db, unit_id, compliance_id, "Approved", "Complied", remarks
        )
    else:
        save_compliance_activity(
            db, unit_id, compliance_id, "Submitted", "Inprogress", remarks
        )

    history_values.extend(history_condition_val)
    update_status = db.update(
        tblComplianceHistory, history_columns, history_values,
        history_condition
    )
    if(update_status is False):
        return clienttransactions.ComplianceUpdateFailed()

    if assignee_id != approver_id:
        if(
            document_name is not None and
            document_name != '' and
            document_name != 'None'
        ):
            compliance_name = "%s - %s" % (document_name, compliance_name)

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
    return True


def get_on_occurrence_compliance_count(
    db, session_user, user_domain_ids, user_unit_ids
):
    query = "SELECT count(*) " + \
            " FROM tbl_assigned_compliances ac " + \
            " INNER JOIN tbl_compliances c " + \
            " ON (ac.compliance_id = c.compliance_id) " + \
            " INNER JOIN tbl_units u ON (ac.unit_id = u.unit_id) " + \
            " WHERE u.is_closed = 0 " + \
            " AND find_in_set(ac.unit_id, %s) " + \
            " AND find_in_set(c.domain_id, %s) " + \
            " AND c.frequency_id = 4 " + \
            " AND ac.assignee = %s "
    rows = db.select_one(query, [
        ",".join(str(x) for x in user_unit_ids),
        ",".join(str(x) for x in user_domain_ids), session_user
    ])
    return rows[0]


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
            " concat(u.unit_code, '-', u.unit_name) " + \
            " FROM tbl_assigned_compliances ac " + \
            " INNER JOIN tbl_compliances c " + \
            " ON (ac.compliance_id = c.compliance_id) " + \
            " INNER JOIN tbl_compliance_duration_type cd " + \
            " ON (c.duration_type_id = cd.duration_type_id) " + \
            " INNER JOIN tbl_units u ON (ac.unit_id = u.unit_id) " + \
            " WHERE u.is_closed = 0 " + \
            " AND find_in_set(ac.unit_id, %s) " + \
            " AND find_in_set(c.domain_id,%s) " + \
            " AND c.frequency_id = 4 " + \
            " AND ac.assignee = %s " + \
            " ORDER BY u.unit_id, document_name, compliance_task " + \
            " LIMIT %s, %s "

    rows = db.select_all(query, [
        ",".join(str(x) for x in user_unit_ids),
        ",".join(str(x) for x in user_domain_ids),
        session_user, int(start_count), int(to_count)
    ])
    result = convert_to_dict(rows, columns)
    # compliances = []
    unit_wise_compliances = {}
    for row in result:
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


def start_on_occurrence_task(
    db, compliance_id, start_date, unit_id, duration, session_user, client_id
):
    columns = [
        "unit_id", "compliance_id",
        "start_date", "due_date", "completed_by"
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
        unit_id, compliance_id, start_date, due_date,
        session_user
    ]

    approval_columns = ["approval_person", "concurrence_person"]
    approval_condition = " compliance_id = %s and unit_id = %s "
    rows = db.get_data(
        tblAssignedCompliances, approval_columns,
        approval_condition, [compliance_id, unit_id]
    )
    approved_by = rows[0]["approval_person"]
    concurred_by = rows[0]["concurrence_person"]
    if is_two_levels_of_approval(db):
        columns.append("concurred_by")
        values.append(concurred_by)
    columns.append("approved_by")
    values.append(approved_by)

    compliance_history_id = db.insert(
        tblComplianceHistory, columns, values
    )
    if compliance_history_id is False:
        raise client_process_error("E017")

    history = get_compliance_history_details(db, compliance_history_id)
    assignee_id = history["completed_by"]
    concurrence_id = history["concurred"]
    approver_id = history["approved_by"]
    if approver_id is None:
        approver_id = assignee_id
    compliance_name = history["compliance_name"]
    document_name = history["doc_name"]
    due_date = history["due_date"]

    # user_ids = "{},{},{}".format(assignee_id, concurrence_id, approver_id)
    assignee_email, assignee_name = get_user_email_name(db, str(assignee_id))
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
