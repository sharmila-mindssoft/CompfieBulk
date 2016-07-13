from server.common import (
    datetime_to_string, string_to_datetime, new_uuid, get_date_time,
    string_to_datetime_with_time
    )
from server.clientdatabase.general import (
    is_two_levels_of_approval
    )

all__ = [
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

def get_inprogress_count(db, session_user):
    other_compliance_condition = "completed_by='{}' AND \
    ac.is_active = 1 AND \
    IFNULL(ch.due_date, 0) >= current_date() \
    AND IFNULL(ch.completed_on, 0) = 0".format(
        session_user
    )
    on_occurrence_condition = "completed_by='{}' AND \
    ac.is_active = 1 AND \
    IFNULL(ch.due_date, 0) >= now() \
    AND IFNULL(ch.completed_on, 0) = 0".format(
        session_user
    )
    query = "SELECT count(*) FROM %s ch INNER JOIN \
    %s ac ON (ch.compliance_id = ac.compliance_id and ac.unit_id = ch.unit_id) INNER JOIN\
    %s c ON (ch.compliance_id = c.compliance_id ) " % (
        tblComplianceHistory , tblAssignedCompliances, tblCompliances
    )

    other_compliance_rows = db.select_all(
        "%s WHERE frequency_id != 4 AND %s" % (query, other_compliance_condition)
    )
    other_compliance_count = other_compliance_rows[0][0]

    query += " WHERE frequency_id = 4 AND %s" % (on_occurrence_condition)
    on_occurrence_rows = db.select_all(query)
    on_occurrence_count = on_occurrence_rows[0][0]

    return int(other_compliance_count) + int(on_occurrence_count)

def get_overdue_count(db, session_user):
    query = "SELECT count(*) FROM %s ch INNER JOIN \
    %s ac ON (ch.compliance_id = ac.compliance_id and ac.unit_id = ch.unit_id) INNER JOIN\
    %s c ON (ch.compliance_id = c.compliance_id) WHERE " % (
        tblComplianceHistory, tblAssignedCompliances, tblCompliances
    )
    condition = "completed_by ='%d'" % (session_user)
    other_compliance_condition = " %s AND frequency_id != 4 AND \
    ac.is_active = 1 AND \
    IFNULL(ch.due_date, 0) < current_date() AND \
    IFNULL(ch.completed_on, 0) = 0 " % (
        condition
    )

    on_occurrence_condition = " %s AND frequency_id = 4 AND \
    ac.is_active = 1 AND \
    IFNULL(ch.due_date, 0) < now() AND \
    IFNULL(ch.completed_on, 0) = 0 " % (
        condition
    )
    other_compliance_count = db.select_all("%s %s" % (
        query, other_compliance_condition)
    )[0][0]
    on_occurrence_count = db.select_all("%s %s" % (
        query, on_occurrence_condition)
    )[0][0]
    return int(other_compliance_count) + int(on_occurrence_count)

def get_current_compliances_list(db, current_start_count, to_count, session_user, client_id):
    columns = [
        "compliance_history_id", "start_date", "due_date", "validity_date",
        "next_due_date", "document_name", "compliance_task", "description",
        "format_file", "unit", "domain_name", "frequency", "remarks",
        "compliance_id", "duration_type_id"
    ]
    query = '''
        SELECT * FROM
        (SELECT
        compliance_history_id,
        start_date,
        ch.due_date as due_date,
        ch.validity_date,
        ch.next_due_date,
        document_name,
        compliance_task,
        compliance_description,
        format_file,
        (SELECT
                concat(unit_code, '-', unit_name, ',', address)
            FROM
                tbl_units tu
            WHERE
                tu.unit_id = ch.unit_id) as unit,
        (SELECT
                domain_name
            FROM
                tbl_domains td
            WHERE
                td.domain_id = c.domain_id) as domain_name,
        (SELECT
                frequency
            FROM
                tbl_compliance_frequency
            WHERE
                frequency_id = c.frequency_id),
        ch.remarks,
        ch.compliance_id,
        duration_type_id
    FROM
        tbl_compliance_history ch
            INNER JOIN
        tbl_assigned_compliances ac ON (ac.unit_id = ch.unit_id
            AND ac.compliance_id = ch.compliance_id)
            INNER JOIN
        tbl_compliances c ON (ac.compliance_id = c.compliance_id)
    WHERE
        ch.completed_by = '%d'
            and ac.is_active = 1
            and IFNULL(ch.completed_on, 0) = 0
            and IFNULL(ch.due_date, 0) != 0
    LIMIT %s, %s ) a
    ORDER BY due_date ASC
    ''' % (
        session_user, current_start_count, to_count
    )
    rows = db.select_all(query)
    current_compliances_row = db.convert_to_dict(rows, columns)
    current_compliances_list = []
    for compliance in current_compliances_row:
        document_name = compliance["document_name"]
        compliance_task = compliance["compliance_task"]
        compliance_name = compliance_task
        if document_name not in (None, "None", "") :
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
        if compliance["format_file"] is not None and compliance["format_file"].strip() != '':
            format_files = [ "%s/%s" % (
                    FORMAT_DOWNLOAD_URL, x
                ) for x in compliance["format_file"].split(",")]
        remarks = compliance["remarks"]
        if remarks in ["None", None, ""]:
            remarks = None
        current_compliances_list.append(
            core.ActiveCompliance(
                compliance_history_id=compliance["compliance_history_id"],
                compliance_name=compliance_name,
                compliance_frequency=core.COMPLIANCE_FREQUENCY(compliance["frequency"]),
                domain_name=compliance["domain_name"],
                start_date=datetime_to_string(compliance["start_date"]),
                due_date=datetime_to_string(compliance["due_date"]),
                compliance_status=compliance_status,
                validity_date=None if compliance["validity_date"] == None else datetime_to_string(compliance["validity_date"]),
                next_due_date=None if compliance["next_due_date"] == None else datetime_to_string(compliance["next_due_date"]),
                ageing=ageing,
                format_file_name=format_files,
                unit_name=unit_name, address=address,
                compliance_description=compliance["description"],
                remarks=remarks,
                compliance_id=compliance["compliance_id"]
            )
        )
    return current_compliances_list

def get_upcoming_count(db, session_user):
    all_compliance_query = '''
        SELECT ac.compliance_id, ac.unit_id FROM tbl_assigned_compliances ac
        INNER JOIN tbl_compliances c ON (ac.compliance_id = c.compliance_id)
        WHERE
        assignee = '%d' AND frequency_id != 4
        AND ac.due_Date < DATE_ADD(now(), INTERVAL 6 MONTH)
        AND ac.is_active = 1;
    ''' % (
        session_user
    )
    all_compliace_rows = db.select_all(all_compliance_query)
    all_compliance_count = len(all_compliace_rows)
    onetime_query = '''
        SELECT ch.compliance_id, ch.unit_id FROM tbl_compliance_history ch
        INNER JOIN tbl_compliances c on (ch.compliance_id =  c.compliance_id)
        WHERE frequency_id = 1 and completed_by = '%d' ;
    ''' % (
        session_user
    )
    onetime_rows = db.select_all(onetime_query)

    combined_rows = []
    for combination in onetime_rows:
        if combination in all_compliace_rows:
            combined_rows.append(combination)
        else:
            continue

    count = len(combined_rows)
    return all_compliance_count - count

def get_upcoming_compliances_list(db, upcoming_start_count, to_count, session_user, client_id):
    query = "SELECT * FROM (SELECT ac.due_date, document_name, compliance_task, \
            compliance_description, format_file, \
            (select concat(unit_code,'-' ,unit_name, ',',address) from %s tu  where\
            tu.unit_id = ac.unit_id), \
            (select domain_name \
            FROM %s d where d.domain_id = c.domain_id) as domain_name, \
            DATE_SUB(ac.due_date, INTERVAL ac.trigger_before_days DAY) \
            as start_date\
            FROM %s  ac \
            INNER JOIN %s c ON (ac.compliance_id = c.compliance_id) WHERE \
            assignee = '%d' AND frequency_id != 4 \
            AND ac.due_Date < DATE_ADD(now(), INTERVAL 6 MONTH) \
            AND ac.is_active = 1 AND IF ( (frequency_id = 1 AND ( \
            select count(*) from tbl_compliance_history ch \
            where ch.compliance_id = ac.compliance_id and \
            ch.unit_id = ac.unit_id ) >0), 0,1) \
            ) a ORDER BY start_date ASC LIMIT %d, %d "  % (
                tblUnits, tblDomains, tblAssignedCompliances,
                tblCompliances, session_user, int(upcoming_start_count),
                to_count
            )
    upcoming_compliances_rows = db.select_all(query)

    columns = ["due_date", "document_name", "compliance_task",
    "description","format_file", "unit", "domain_name",  "start_date"]
    upcoming_compliances_result = db.convert_to_dict(
        upcoming_compliances_rows, columns
    )
    upcoming_compliances_list = []
    for compliance in upcoming_compliances_result:
        document_name = compliance["document_name"]
        compliance_task = compliance["compliance_task"]
        compliance_name = compliance_task
        if document_name not in (None, "None", "") :
            compliance_name = "%s - %s" % (document_name, compliance_task)

        unit_details = compliance["unit"].split(",")
        unit_name = unit_details[0]
        address = unit_details[1]

        start_date = compliance["start_date"]
        format_files = None
        if compliance["format_file"] is not None and compliance["format_file"].strip() != '':
            format_files = [ "%s/%s" % (
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

# def calculate_next_start_date(self, due_date, statutory_dates, repeats_every):
#     statutory_dates = json.loads(statutory_dates)
#     next_start_date = None
#     if len(statutory_dates) > 1:
#         month_of_due_date = due_date.month
#         for statutory_date in statutory_dates:
#             if month_of_due_date >= statutory_date["statutory_month"]:
#                 next_start_date = due_date - timedelta(
#                     days = statutory_date["trigger_before_days"])
#                 break
#             else:
#                 continue
#     else:
#         trigger_before = 0
#         if len(statutory_dates) > 0:
#             trigger_before = int(statutory_dates[0]["trigger_before_days"])
#         next_start_date = due_date - timedelta(days=trigger_before)
#     return next_start_date

def update_compliances(
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
        r = relativedelta.relativedelta(validity_date, next_due_date)
        if abs(r.months) > 3 or abs(r.years) > 0:
            return False

    # Hanling upload
    document_names = []
    file_size = 0
    if documents is not None:
        if len(documents) > 0:
            for doc in documents:
                file_size += doc.file_size

            if is_space_available(db, file_size):
                is_uploading_file = True
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
                    convert_base64_to_file(file_name, doc.file_content, client_id)
                db.update_used_space(file_size)
            else:
                return clienttransactions.NotEnoughSpaceAvailable()

    assignee_id, concurrence_id, approver_id, compliance_name, document_name, due_date = get_compliance_history_details(db, 
        compliance_history_id
    )
    current_time_stamp = get_date_time()
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
    history_condition = "compliance_history_id = '%d' \
        and completed_by ='%d'" % (
            compliance_history_id, session_user
        )

    columns = "unit_id, compliance_id"
    condition = "compliance_history_id = '%d'" % compliance_history_id
    rows = db.get_data(
        tblComplianceHistory, columns, condition
    )
    unit_id = rows[0][0]
    compliance_id = rows[0][1]
    ageing, remarks = calculate_ageing(
        due_date, frequency_type=None, completion_date=completion_date, duration_type=None
    )
    if assignee_id == approver_id:
        history_columns.append("approve_status")
        history_columns.append("approved_on")
        history_values.append(1)
        history_values.append(current_time_stamp)
        query = "SELECT frequency_id FROM %s tc WHERE tc.compliance_id = '%s' " % (
            tblCompliances, compliance_id
        )
        rows = db.select_one(query)
        columns = ["frequency_id"]
        rows = db.convert_to_dict(rows, columns)
        frequency_id = int(rows["frequency_id"])
        as_columns = []
        as_values = []
        print next_due_date
        if next_due_date is not None:
            as_columns.append("due_date")
            as_values.append(next_due_date)
        if validity_date is not None:
            as_columns.append("validity_date")
            as_values.append(validity_date)
        if frequency_id in (1, "1"):
            as_columns.append("is_active")
            as_values.append(0)

        as_condition = " unit_id = '%d' and compliance_id = '%d'" % (
            unit_id, compliance_id
        )
        if len(as_columns) > 0 and len(as_values) > 0 and len(as_columns) == len(as_values):
            db.update(
                tblAssignedCompliances, as_columns, as_values, as_condition,
                client_id
            )

        save_compliance_activity(db, 
            unit_id, compliance_id, "Approved", "Complied",
            remarks
        )
    else:
        save_compliance_activity(db, 
            unit_id, compliance_id, "Submitted", "Inprogress",
            remarks
        )

    db.update(
        tblComplianceHistory, history_columns, history_values,
        history_condition
    )

    if assignee_id != approver_id:
        if document_name is not None and document_name != '' and document_name != 'None':
            compliance_name = "%s - %s" % (document_name, compliance_name)

        assignee_email, assignee_name = get_user_email_name(db, str(assignee_id))
        approver_email, approver_name = get_user_email_name(db, str(approver_id))
        action = "approve"
        notification_text = "%s has completed the compliance %s. Review and approve" % (
            assignee_name, compliance_name
        )
        concurrence_email, concurrence_name = (None, None)
        if is_two_levels_of_approval(db) and concurrence_id not in [None, "None", 0, "", "null", "Null"]:
            concurrence_email, concurrence_name = get_user_email_name(db, str(concurrence_id))
            action = "Concur"
            notification_text = "%s has completed the compliance %s. Review and concur" % (
                assignee_name, compliance_name
            )

        save_compliance_notification(
            db, compliance_history_id, notification_text, "Compliance Completed", action
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
    query = "SELECT count(*) \
            FROM %s ac \
            INNER JOIN %s c ON (ac.compliance_id = c.compliance_id)\
            INNER JOIN %s u ON (ac.unit_id = u.unit_id) \
            WHERE u.is_closed = 0 \
            AND ac.unit_id in (%s)\
            AND c.domain_id in (%s) \
            AND c.frequency_id = 4 \
            AND ac.assignee = '%d' " % (
                tblAssignedCompliances,
                tblCompliances, tblUnits, user_unit_ids,
                user_domain_ids, session_user
            )
    rows = db.select_all(query)
    return rows[0][0]

def get_on_occurrence_compliances_for_user(
    db, session_user, user_domain_ids, user_unit_ids, start_count,
    to_count
):
    columns = "ac.compliance_id, c.statutory_provision,\
            compliance_task, compliance_description, \
            duration_type, duration, document_name, u.unit_id"
    concat_columns = "concat(unit_code, '-', unit_name)"
    query = "SELECT %s, %s \
            FROM %s ac \
            INNER JOIN %s c ON (ac.compliance_id = c.compliance_id)\
            INNER JOIN %s cd ON (c.duration_type_id = cd.duration_type_id) \
            INNER JOIN %s u ON (ac.unit_id = u.unit_id) \
            WHERE u.is_closed = 0 \
            AND ac.unit_id in (%s)\
            AND c.domain_id in (%s) \
            AND c.frequency_id = 4 \
            AND ac.assignee = '%d' \
            ORDER BY u.unit_id, document_name, compliance_task \
            LIMIT %d, %d" % (
                columns, concat_columns, tblAssignedCompliances,
                tblCompliances, tblComplianceDurationType,
                tblUnits, user_unit_ids, user_domain_ids,
                session_user, int(start_count), to_count
            )
    rows = db.select_all(query)
    columns_list = columns.replace(" ", "").split(",")
    columns_list += ["unit_name"]
    result = db.convert_to_dict(rows, columns_list)
    compliances = []
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
                row["ac.compliance_id"], row["c.statutory_provision"],
                compliance_name, row["compliance_description"],
                duration, row["u.unit_id"]
            )
        )
    return unit_wise_compliances

def start_on_occurrence_task(
    db, compliance_id, start_date, unit_id, duration, session_user, client_id
):
    columns = [
        "compliance_history_id", "unit_id", "compliance_id",
        "start_date", "due_date", "completed_by"
    ]
    compliance_history_id = db.get_new_id(
        "compliance_history_id", tblComplianceHistory, client_id
    )
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
        compliance_history_id, unit_id, compliance_id, start_date, due_date,
        session_user
    ]

    approval_columns = "approval_person, concurrence_person"
    approval_condition = " compliance_id = '%d' and unit_id = '%d' " % (
        compliance_id, unit_id
    )
    rows = db.get_data(
        tblAssignedCompliances, approval_columns, approval_condition
    )
    concurred_by = rows[0][1]
    approved_by = rows[0][0]
    if is_two_levels_of_approval(db):
        columns.append("concurred_by")
        values.append(concurred_by)
    columns.append("approved_by")
    values.append(approved_by)

    db.insert(
        tblComplianceHistory, columns, values
    )

    assignee_id, concurrence_id, approver_id, compliance_name, document_name, due_date = get_compliance_history_details(db, 
        compliance_history_id
    )
    user_ids = "{},{},{}".format(assignee_id, concurrence_id, approver_id)
    assignee_email, assignee_name = get_user_email_name(db, str(assignee_id))
    approver_email, approver_name = get_user_email_name(db, str(approver_id))
    if concurrence_id not in [None, "None", 0, "", "null", "Null"] and is_two_levels_of_approval(db):
        concurrence_email, concurrence_name = get_user_email_name(db, str(concurrence_id))
    if document_name not in (None, "None", "") :
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
        print "Error sending email :{}".format(e)
    return True

def is_space_available(db, upload_size):
        columns = "total_disk_space - total_disk_space_used"
        rows = db.get_data(tblClientGroups, columns, "1")
        remaining_space = rows[0][0]
        if upload_size < remaining_space:
            return True
        else:
            return False

def calculate_ageing(due_date, frequency_type=None, completion_date=None, duration_type=None):
    current_time_stamp = get_date_time()
    compliance_status = "-"
    # due_date = self.localize(due_date)
    if frequency_type == "On Occurrence":
        r = relativedelta.relativedelta(due_date, current_time_stamp)
        if completion_date is not None:
            r = relativedelta.relativedelta(due_date, completion_date)
            if r.days < 0 and r.hours < 0 and r.minutes < 0:
                compliance_status = "On Time"
            else:
                if r.days == 0:
                    if duration_type in ["2", 2]:
                        compliance_status = "Delayed by %d.%d hour(s) " % (
                            abs(r.hours), abs(r.minutes)
                        )
                    else:
                        compliance_status = "Delayed by 1 day "
                else:
                    if duration_type in ["2", 2]:
                        compliance_status = "Delayed by %d.%d hour(s)" % (
                           ( abs(r.days) * 4 + abs(r.hours)), abs(r.minutes)
                        )
                    else:
                        compliance_status = "Delayed by %d day(s)" % (
                            abs(r.days)
                        )
                return r.days, compliance_status
        else:
            if r.days >= 0 and r.hours >= 0 and r.minutes >= 0:
                if r.days == 0:
                    if duration_type in ["2", 2]:
                        compliance_status = " %d.%d hour(s) left" % (
                            abs(r.hours), abs(r.minutes)
                        )
                    else:
                        compliance_status = "1 Day left"
                else:
                    if duration_type in ["2", 2]:
                        compliance_status = "%d.%d hour(s) left" % (
                           ( abs(r.days) * 24 + abs(r.hours)), abs(r.minutes)
                        )
                    else:
                        compliance_status = " %d day(s) left" % (
                            abs(r.days)
                        )
            else:
                if r.days == 0:
                    if duration_type in ["2", 2]:
                        compliance_status = "Overdue by %d.%d hour(s) " % (
                            abs(r.hours), abs(r.minutes)
                        )
                    else:
                        compliance_status = "Overdue by 1 day "
                else:
                    if duration_type in ["2", 2]:
                        compliance_status = "Overdue by %d.%d hours" % (
                           (abs(r.days) * 24 + abs(r.hours)), abs(r.minutes)
                        )
                    else:
                        compliance_status = "Overdue by %d day(s)" %(
                            abs(r.days)
                        )
            return r.days, compliance_status
    else:
        if completion_date is not None:
            compliance_status = "On Time"
            if due_date not in [None, "None", 0]:
                if type(due_date) == datetime.datetime:
                    due_date = due_date.date()
                if type(completion_date) == datetime.datetime:
                    completion_date = completion_date.date()
                r = relativedelta.relativedelta(due_date, completion_date)
                if r.days < 0:
                    compliance_status = "Delayed by %d day(s)" % abs(r.days)
                return r.days, compliance_status
        else:
            if due_date not in [None, "None", 0]:
                r = relativedelta.relativedelta(due_date.date(), current_time_stamp.date())
                compliance_status = " %d days left" % abs(r.days+1)
                if r.days < 0:
                    compliance_status = "Overdue by %d day(s)" % abs(r.days)
                    return r.days, compliance_status
    return 0, compliance_status

def convert_base64_to_file(file_name, file_content, client_id):
    client_directory = "%s/%d" % (CLIENT_DOCS_BASE_PATH, client_id)
    file_path = "%s/%s" % (client_directory, file_name)
    if not os.path.exists(client_directory):
        os.makedirs(client_directory)
    remove_uploaded_file(file_path)
    if file_content is not None :
        new_file = open(file_path, "wb")
        new_file.write(file_content.decode('base64'))
        new_file.close()

def remove_uploaded_file(file_path):
    if os.path.exists(file_path) :
        os.remove(file_path)

def get_compliance_history_details(db, compliance_history_id):
    columns = "completed_by, ifnull(concurred_by, 0), approved_by, ( \
        select compliance_task from %s c \
        where c.compliance_id = ch.compliance_id ), \
        (select document_name from %s c \
        where c.compliance_id = ch.compliance_id ), due_date" % (
            tblCompliances, tblCompliances)
    condition = "compliance_history_id = '%d'" % compliance_history_id
    rows = db.get_data(tblComplianceHistory + " ch", columns, condition)
    if rows:
        return rows[0]

def is_onOccurrence_with_hours(db, compliance_history_id):
    columns = "compliance_id"
    condition = "compliance_history_id = '%d'" % compliance_history_id
    rows = db.get_data(tblComplianceHistory, columns, condition)
    compliance_id = rows[0][0]

    comp_columns = "frequency_id, duration_type_id"
    comp_condition = "compliance_id = '%d'" % compliance_id
    comp_rows = db.get_data(tblCompliances, comp_columns, comp_condition)
    frequency_id = comp_rows[0][0]
    duration_type_id = comp_rows[0][1]
    if frequency_id == 4 and duration_type_id == 2:
        return True
    else:
        return False

def save_compliance_activity(
    db, unit_id, compliance_id, activity_status, compliance_status,
    remarks
):
    compliance_activity_id = db.get_new_id(
        "compliance_activity_id", tblComplianceActivityLog,
    )
    date = get_date_time()
    columns = [
        "compliance_activity_id", "unit_id", "compliance_id",
        "activity_date", "activity_status", "compliance_status",
        "updated_on"
    ]
    values = [
        compliance_activity_id, unit_id, compliance_id, date, activity_status,
        compliance_status,  date
    ]
    if remarks:
        columns.append("remarks")
        values.append(remarks)
    db.insert(
       tblComplianceActivityLog, columns, values
    )

def get_user_email_name(db, user_ids):
    user_id_list = [int(x) for x in user_ids.split(",")]
    admin_email = None
    index = None
    if 0 in user_id_list:
        index = user_id_list.index(0)
        column = "username"
        admin_rows = db.get_data(tblAdmin, column, "1")
        user_id_list.remove(0)
        admin_email = admin_rows[0][0]
    column = "email_id, employee_name"
    condition = "user_id in (%s)" % ",".join(str(x) for x in user_ids)
    rows = db.get_data(
        tblUsers, column, condition
    )
    email_ids = ""
    employee_name = ""
    for index, row in enumerate(rows):
        if index == 0:
            if row[1] is not None:
                employee_name += "%s" % row[1]
            email_ids += "%s" % row[0]
        else:
            if row[1] is not None:
                employee_name += ", %s" % row[1]
            email_ids += ", %s" % row[0]
    if admin_email is not None:
        employee_name += "Administrator"
        email_ids += admin_email

    return email_ids, employee_name

def save_compliance_notification(
    db, compliance_history_id, notification_text, category, action
):
    notification_id = db.get_new_id(
        "notification_id", tblNotificationsLog
    )
    current_time_stamp = get_date_time()

    # Get history details from compliance history id
    history_columns = "unit_id, compliance_id, completed_by, concurred_by, \
    approved_by"
    history_condition = "compliance_history_id = '%d'" % compliance_history_id
    history_rows = db.get_data(
        tblComplianceHistory, history_columns, history_condition
    )
    history_columns_list = [
        "unit_id", "compliance_id", "completed_by",
        "concurred_by", "approved_by"
    ]
    history = db.convert_to_dict(history_rows[0], history_columns_list)
    unit_id = history["unit_id"]
    compliance_id = history["compliance_id"]

    # Getting Unit details from unit_id
    unit_columns = "country_id, business_group_id, legal_entity_id, division_id"
    unit_condition = "unit_id = '%d'" % int(unit_id)
    unit_rows = db.get_data(tblUnits, unit_columns, unit_condition)
    unit_columns_list = [
        "country_id", "business_group_id", "legal_entity_id", "division_id"
    ]
    unit = db.convert_to_dict(unit_rows[0], unit_columns_list)

    # Getting compliance_details from compliance_id
    compliance_columns = "domain_id"
    compliance_condition = "compliance_id = '%d'" % compliance_id
    compliance_rows = db.get_data(
        tblCompliances, compliance_columns, compliance_condition
    )
    domain_id = compliance_rows[0][0]

    # Saving notification
    columns = [
        "notification_id", "country_id", "domain_id", "business_group_id",
        "legal_entity_id", "division_id", "unit_id", "compliance_id",
        "assignee", "concurrence_person", "approval_person", "notification_type_id",
        "notification_text", "extra_details", "created_on"
    ]
    extra_details = "%d-%s" % (compliance_history_id, category)
    values = [
        notification_id, unit["country_id"], domain_id, unit["business_group_id"],
        unit["legal_entity_id"], unit["division_id"], unit_id, compliance_id,
        history["completed_by"], history["concurred_by"], history["approved_by"],
        1, notification_text, extra_details, current_time_stamp
    ]
    db.insert(tblNotificationsLog, columns, values)

    # Saving in user log
    columns = [
        "notification_id", "read_status", "updated_on", "user_id"
    ]
    values = [
        notification_id, 0, current_time_stamp
    ]
    if action.lower() == "concur":
        values.append(int(history["concurred_by"]))
    elif action.lower() == "approve":
        values.append(int(history["approved_by"]))
    elif action.lower() == "concurred":
        values.append(int(history["completed_by"]))
    elif action.lower() == "approvedtoassignee":
        values.append(int(history["completed_by"]))
    elif action.lower() == "approvedtoconcur":
        values.append(int(history["concurred_by"]))
    elif action.lower() == "concurrejected":
        values.append(int(history["completed_by"]))
    elif action.lower() == "approverejectedtoassignee":
        values.append(int(history["completed_by"]))
    elif action.lower() == "approverejectedtoconcur":
        values.append(int(history["concurred_by"]))
    elif action.lower() == "started":
        values.append(int(history["completed_by"]))
    return db.insert(tblNotificationUserLog, columns, values)
