import os
import json
import datetime
import threading
from server import logger
from dateutil import relativedelta
from clientprotocol import (clientcore, clientuser, clienttransactions, clientmasters)
from server.clientdatabase.tables import *
from server.common import (
    datetime_to_string, string_to_datetime, new_uuid, get_date_time,
    string_to_datetime_with_time, convert_to_dict, get_date_time_in_date, encrypt,
    addMonth, datetime_to_string_time
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
    "verify_password",
    "get_calendar_view",
    "get_settings_form_data",
    "save_settings_form_data"
]

email = EmailHandler()

CLIENT_DOCS_DOWNLOAD_URL = "/client/client_documents"

#################################################################
# Compliance Task Details - Get inprogress count
#################################################################
def get_inprogress_count(db, session_user, unit_id, cal_view, cal_date):
    param = [session_user, unit_id, unit_id]
    other_compliance_condition = " WHERE (frequency_id != 5 OR " + \
        " (frequency_id = 5 and duration_type_id=1) )" + \
        " AND completed_by=%s  AND " + \
        " ac.is_active = 1 AND " + \
        " IFNULL(ch.due_date, 0) >= current_date() " + \
        " AND IFNULL(ch.completed_on, 0) = 0 AND ch.current_status = 0 " + \
        " AND IF(%s IS NOT NULL, ch.unit_id = %s,1) "
    on_occurrence_condition = " WHERE frequency_id = 5 " + \
        " and duration_type_id=2" + \
        " AND completed_by = %s AND " + \
        " ac.is_active = 1 AND " + \
        " IFNULL(ch.due_date, 0) >= now() " + \
        " AND IFNULL(ch.completed_on, 0) = 0 AND ch.current_status = 0 " + \
        " AND IF(%s IS NOT NULL, ch.unit_id = %s,1) "

    query = "SELECT count(*) as inprogress_count FROM tbl_compliance_history ch INNER JOIN " + \
        " tbl_assign_compliances ac " + \
        " ON (ch.compliance_id = ac.compliance_id " + \
        " and ac.unit_id = ch.unit_id) INNER JOIN " + \
        " tbl_compliances c ON (ch.compliance_id = c.compliance_id ) "

    if cal_view != None:
        if cal_view == "DUEDATE" :
            # or cal_view == "OVERDUE"
            final_other_query = query + other_compliance_condition + " AND date(ch.due_date) = date(%s)"
            final_onoccurrence_query = query + on_occurrence_condition + " AND date(ch.due_date) = date(%s)"
        elif cal_view == "INPROGRESS":
            final_other_query = query + other_compliance_condition + " AND date(ch.due_date) >= date(%s)"
            final_onoccurrence_query = query + on_occurrence_condition + " AND date(ch.due_date) >= date(%s)"
        else :
            final_other_query = query + other_compliance_condition + " AND date(ch.due_date) = date(%s)"
            final_onoccurrence_query = query + on_occurrence_condition + " AND date(ch.due_date) = date(%s)"

        param.extend([string_to_datetime(cal_date)])
    else:
        final_other_query = query + other_compliance_condition
        final_onoccurrence_query = query + on_occurrence_condition

    # other_compliance_rows = db.select_all(query + other_compliance_condition, param)
    # on_occurrence_rows = db.select_all(query + on_occurrence_condition, param)
    other_compliance_rows = db.select_all(final_other_query, param)
    on_occurrence_rows = db.select_all(final_onoccurrence_query, param)

    other_compliance_count = other_compliance_rows[0]["inprogress_count"]
    on_occurrence_count = on_occurrence_rows[0]["inprogress_count"]
    return int(other_compliance_count) + int(on_occurrence_count)

#################################################################
# Compliance Task Details - Get overdue count
#################################################################
def get_overdue_count(db, session_user, unit_id, cal_view, cal_date):
    query = "SELECT count(*) as occ FROM tbl_compliance_history ch INNER JOIN " + \
        " tbl_assign_compliances ac " + \
        " ON (ch.compliance_id = ac.compliance_id " + \
        " and ac.unit_id = ch.unit_id) INNER JOIN " + \
        " tbl_compliances c ON (ch.compliance_id = c.compliance_id) WHERE "
    param = [session_user, unit_id, unit_id]
    other_compliance_condition = " completed_by = %s " + \
        " AND (frequency_id != 5 OR " + \
        " (frequency_id = 5 and duration_type_id=1)) AND " + \
        " ac.is_active = 1 AND " + \
        " IFNULL(ch.due_date, 0) < current_date() AND " + \
        " IFNULL(ch.completed_on, 0) = 0 AND ch.current_status = 0 " + \
        " AND IF(%s IS NOT NULL, ch.unit_id = %s,1) "

    on_occurrence_condition = " completed_by = %s " + \
        " AND frequency_id = 5 AND duration_type_id=2 AND " + \
        " ac.is_active = 1 AND " + \
        " IFNULL(ch.due_date, 0) < now() AND " + \
        " IFNULL(ch.completed_on, 0) = 0 AND ch.current_status = 0 " + \
        " AND IF(%s IS NOT NULL, ch.unit_id = %s,1) "

    if cal_view != None:
        if cal_view == "OVERDUE":
            final_other_query = query + other_compliance_condition + " AND date(ch.due_date) <= date(%s)"
            final_onoccurrence_query = query + on_occurrence_condition + " AND date(ch.due_date) <= date(%s)"
        else:
            final_other_query = query + other_compliance_condition + " AND date(ch.due_date) = date(%s)"
            final_onoccurrence_query = query + on_occurrence_condition + " AND date(ch.due_date) = date(%s)"

        # print "cal_date>>>>>>", cal_date
        # print "string_to_datetime(cal_date)>>", string_to_datetime(cal_date)
        param.extend([string_to_datetime(cal_date)])
    else:
        final_other_query = query + other_compliance_condition
        final_onoccurrence_query = query + on_occurrence_condition

    # other_compliance_count = db.select_one(
    #     query + other_compliance_condition, param
    # )["occ"]
    # on_occurrence_count = db.select_one(
    #     query + on_occurrence_condition, param
    # )["occ"]

    other_compliance_count = db.select_one(final_other_query, param)["occ"]
    on_occurrence_count = db.select_one(final_onoccurrence_query, param)["occ"]

    return int(other_compliance_count) + int(on_occurrence_count)

#################################################################
# Compliance Task Details - Get Current Compliances
#################################################################
def get_current_compliances_list(
    db, unit_id, current_start_count, to_count, session_user, cal_view, cal_date
):
    columns = [
        "compliance_history_id", "start_date", "due_date", "documents",
        "validity_date", "next_due_date",
        "document_name", "compliance_task", "compliance_description",
        "format_file", "unit", "domain_name", "frequency", "remarks",
        "compliance_id", "duration_type_id"
    ]

    compliance_history_ids = ""
    history_condition=""
    history_condition_val = []

    if cal_view != None:
        cal_date = string_to_datetime(cal_date).date()

    if cal_view != None:
        if cal_view == "OVERDUE":
            query1 = " SELECT " + \
                     " group_concat(ch.compliance_history_id) as compliance_history_ids, count(ch.compliance_history_id) as ov_count " + \
                     " from tbl_compliance_history as ch " + \
                     " inner join tbl_compliances as com on ch.compliance_id = com.compliance_id " + \
                     " inner join tbl_client_compliances as cc on ch.unit_id = cc.unit_id and cc.domain_id = com.domain_id " + \
                     " and cc.compliance_id = com.compliance_id " + \
                     " inner join tbl_user_units as un on un.unit_id = ch.unit_id and un.user_id = ch.completed_by " + \
                     " where un.user_id = %s " + \
                     " and IF((com.frequency_id = 5 AND com.duration_type_id = 2), ch.due_date < now(),date(ch.due_date) < curdate()) " + \
                     " and ifnull(ch.current_status,0) = 0 " + \
                     " and date(now()) = %s "
            rows_calendar = db.select_all(query1, [session_user, cal_date])

        elif cal_view == "INPROGRESS":
            query1 = " SELECT " + \
                         " group_concat(ch.compliance_history_id) as compliance_history_ids, count(ch.compliance_history_id) as ip_count " + \
                         " from tbl_compliance_history as ch " + \
                         " inner join tbl_compliances as com on ch.compliance_id = com.compliance_id " + \
                         " inner join tbl_client_compliances as cc on ch.unit_id = cc.unit_id and cc.domain_id = com.domain_id " + \
                         " and cc.compliance_id = com.compliance_id " + \
                         " inner join tbl_user_units as un on un.unit_id = ch.unit_id and un.user_id = ch.completed_by " + \
                         " where un.user_id = %s " + \
                         " and IF((com.frequency_id = 5 AND com.duration_type_id = 2),ch.due_date >= now(),date(ch.due_date) >= curdate()) " + \
                         " and ifnull(ch.current_status,0) = 0 " + \
                         " and date(now()) = %s "
            rows_calendar = db.select_all(query1, [session_user, cal_date])
            # print "query1>>>", query1
            # print "param>>>", session_user, cal_date

        elif cal_view == "DUEDATE":
            query1 = " SELECT ch.legal_entity_id, ch.unit_id, ch.completed_by, ch.due_date, " + \
                         " group_concat(compliance_history_id) as compliance_history_ids,count(compliance_history_id) du_count " + \
                         " from tbl_compliance_history as ch where current_status = 0 " + \
                         " and date(ch.due_Date) < DATE_ADD(date(now()), INTERVAL 6 MONTH) " + \
                         " and date(ch.due_date) = %s and ch.completed_by = %s "+ \
                         " group by ch.completed_by, date(ch.due_date)"
            rows_calendar = db.select_all(query1, [cal_date, session_user])

        for compliance in rows_calendar:
            compliance_history_ids = compliance["compliance_history_ids"]

        # history_condition = " WHERE find_in_set(a.compliance_history_id,%s)"
        history_condition = " WHERE find_in_set(a.compliance_history_id,%s) LIMIT %s, %s"
        history_condition_val = compliance_history_ids
    else:
        history_condition =""
        history_condition_val = ""

    # if current_start_count == 1:
    #     current_start_count = 0

    query = " SELECT * FROM " + \
        " (SELECT compliance_history_id, start_date, " + \
        " ch.due_date as due_date, documents, " + \
        " ch.validity_date, ch.next_due_date, ch.unit_id, document_name, " + \
        " compliance_task, compliance_description, format_file, " + \
        " substring(substring(c.statutory_mapping,3),1,char_length(c.statutory_mapping) -4) as statutory, " + \
        " (SELECT " + \
        " concat(unit_code, '-', unit_name, '|', address, ' ', postal_code) " + \
        " FROM  tbl_units tu " + \
        " WHERE tu.unit_id = ch.unit_id) as unit, " + \
        " (SELECT  domain_name FROM tbl_domains td WHERE " + \
        " td.domain_id = c.domain_id) as domain_name, " + \
        " (SELECT domain_id FROM tbl_domains td WHERE " + \
        " td.domain_id = c.domain_id) as domain_id, " + \
        " (SELECT frequency FROM tbl_compliance_frequency " + \
        " WHERE frequency_id = c.frequency_id) as frequency, ch.remarks, " + \
        " ch.compliance_id, ac.assigned_on, c.frequency_id, ch.concurrence_status, ch.approve_status, ch.current_status, " + \
        " IFNULL((select days from tbl_validity_date_settings where country_id = c.country_id " + \
        " and domain_id = c.domain_id),0) as validity_settings_days, " + \
        " c.duration_type_id FROM tbl_compliance_history ch " + \
        " INNER JOIN tbl_assign_compliances ac " + \
        " ON (ac.unit_id = ch.unit_id " + \
        " AND ac.compliance_id = ch.compliance_id) " + \
        " INNER JOIN tbl_compliances c " + \
        " ON (ac.compliance_id = c.compliance_id) " + \
        " WHERE ch.completed_by = %s AND ch.current_status = 0 " + \
        " and ac.is_active = 1 and IFNULL(ch.completed_on, 0) = 0 "
        # " and IFNULL(ch.due_date, 0) != 0 and IF(%s IS NOT NULL, ch.unit_id = %s,1) LIMIT %s, %s ) a "

    # print "param>>", session_user, unit_id, unit_id, current_start_count, to_count, history_condition_val
    if history_condition != "":
        query = query + " and IFNULL(ch.due_date, 0) != 0 and IF(%s IS NOT NULL, ch.unit_id = %s,1)) a "
        query = query + history_condition
        param = [session_user, unit_id, unit_id, history_condition_val, current_start_count, to_count]
    else:
        query = query  + " and IFNULL(ch.due_date, 0) != 0 and IF(%s IS NOT NULL, ch.unit_id = %s,1) LIMIT %s, %s ) a "
        param = [session_user, unit_id, unit_id, current_start_count, to_count]

        query += " ORDER BY due_date ASC "

    rows = db.select_all(query, param)

    current_compliances_list = []
    for compliance in rows:
        document_name = compliance["document_name"]
        compliance_task = compliance["compliance_task"]
        # compliance_task = compliance["compliance_history_id"]

        compliance_name = compliance_task
        if document_name not in (None, "None", ""):
            compliance_name = "%s - %s" % (
                document_name, compliance_task)

        unit_details = compliance["unit"].split("|")
        unit_name = unit_details[0]
        address = unit_details[1]

        no_of_days, ageing = calculate_ageing(
            due_date=compliance["due_date"],
            frequency_type=compliance["frequency_id"],
            duration_type=compliance["duration_type_id"]
        )
        if compliance["concurrence_status"] == "2":
            # compliance_status = clientcore.COMPLIANCE_STATUS("Concurred Rectify")
            compliance_status = clientcore.COMPLIANCE_STATUS("Rectify")
        elif compliance["approve_status"] == "2":
            # compliance_status = clientcore.COMPLIANCE_STATUS("Approver Rectified")
            compliance_status = clientcore.COMPLIANCE_STATUS("Rectify")
        else:
            if compliance["current_status"]== 0:
                compliance_status = clientcore.COMPLIANCE_STATUS("Inprogress")
            if "Overdue" in ageing:
                compliance_status = clientcore.COMPLIANCE_STATUS("Not Complied")

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
                # start_date=datetime_to_string(compliance["start_date"]),
                start_date=datetime_to_string_time(compliance["start_date"]),
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
                statu=compliance["statutory"],
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
    db, unit_id, upcoming_start_count, to_count, session_user, cal_view, cal_date
):
    compliance_history_ids = ""
    unit_ids =""
    history_condition=""
    history_condition_val = []

    if cal_view != None:
        cal_date = string_to_datetime(cal_date).date()
        cal_year, cal_month, cal_dat = str(cal_date).split("-")
        # print "AFTER SPLIT>>", cal_year, cal_month, cal_dat

        query1 = " select ac.legal_entity_id, ac.assignee, " + \
                 " year(DATE_SUB(ac.due_date, INTERVAL ac.trigger_before_days DAY)) as due_year, " + \
                 " month(DATE_SUB(ac.due_date, INTERVAL ac.trigger_before_days DAY)) as due_month, " + \
                 " day(DATE_SUB(ac.due_date, INTERVAL ac.trigger_before_days DAY)) as due_date,  " + \
                 " group_concat(distinct ac.compliance_id) as compliance_ids , " + \
                 " group_concat(distinct ac.unit_id) as unit_ids , " + \
                 " count(ac.compliance_id) as up_count1  " + \
                 " from tbl_assign_compliances as ac " + \
                 " inner join tbl_compliances as com on ac.compliance_id = com.compliance_id and com.frequency_id != 5 " + \
                 " where DATE_SUB(ac.due_date, INTERVAL ac.trigger_before_days DAY) > curdate()  " + \
                 " AND ac.due_Date < DATE_ADD(now(), INTERVAL 6 MONTH)  " + \
                 " AND year(DATE_SUB(ac.due_date, INTERVAL ac.trigger_before_days DAY))  = %s AND " + \
                 " month(DATE_SUB(ac.due_date, INTERVAL ac.trigger_before_days DAY)) = %s AND " + \
                 " day(DATE_SUB(ac.due_date, INTERVAL ac.trigger_before_days DAY)) = %s AND ac.assignee = %s " + \
                 " group by ac.assignee, DATE_SUB(ac.due_date, INTERVAL ac.trigger_before_days DAY) "

        rows_calendar = db.select_all(query1, [cal_year, cal_month, cal_dat, session_user])
        # print "query1>>", query1
        # print "cal_date>>", cal_date

        for compliance in rows_calendar:
            compliance_history_ids = compliance["compliance_ids"]
            unit_ids = compliance["unit_ids"]

        # print "compliance_history_ids>>", compliance_history_ids
        # print "unit_ids>>", unit_ids

        history_condition = " WHERE find_in_set(a.compliance_id,%s) and find_in_set(a.unit_id,%s) "
        history_condition_val = compliance_history_ids
        history_condition_val1 = unit_ids
    else:
        history_condition =""
        history_condition_val = ""
        history_condition_val1 = ""


    query = "SELECT * FROM (SELECT ac.due_date, document_name, " + \
            " compliance_task, compliance_description, format_file, " + \
            " unit_code, unit_name, address, " + \
            " (select domain_name " + \
            " FROM tbl_domains d " + \
            " where d.domain_id = c.domain_id) as domain_name, " + \
            " DATE_SUB(ac.due_date, INTERVAL ac.trigger_before_days DAY) " + \
            " as start_date, ac.assigned_on, ac.compliance_id, ac.unit_id " + \
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
            " ch.unit_id = ac.unit_id ) >0), 0,1) ) a "

    if history_condition != "":
        query = query + history_condition
        param = [session_user, unit_id, unit_id, history_condition_val, history_condition_val1, int(upcoming_start_count), to_count]
    else:
        param = [session_user, unit_id, unit_id, int(upcoming_start_count), to_count]

    query += " ORDER BY start_date ASC LIMIT %s, %s  "

    # upcoming_compliances_rows = db.select_all(
    #     query, [session_user, unit_id, unit_id, int(upcoming_start_count), to_count]
    # )

    upcoming_compliances_rows = db.select_all(query, param)

    upcoming_compliances_list = []

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


def handle_file_upload(db, documents, uploaded_documents, old_documents):
    document_names = []
    file_size = 0
    if documents is not None:
        if len(documents) > 0:
            for doc in documents:
                file_size += doc.file_size

            if is_space_available(db, file_size):
                for doc in documents:
                    file_name = doc.file_name
                    document_names.append(file_name)

                update_used_space(db, file_size)
            else:
                return clienttransactions.NotEnoughSpaceAvailable()

    # Show Old uploaded documents
    if old_documents is not None and len(old_documents) > 0:
        for document in old_documents.split(","):
            if document is not None and document.strip(',') != '':
                name = document.split("-")[0]
                document_parts = document.split(".")
                ext = document_parts[len(document_parts)-1]
                name = "%s.%s" % (name, ext)
                # if name not in uploaded_documents:
                #     # path = "%s/%s/%s" % (
                #     #    CLIENT_DOCS_BASE_PATH, client_id, document
                #     # )
                #     # remove_uploaded_file(path)
                # else:
                #     document_names.append(document)
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

    compliance_task = row["compliance_task"]

    # document_names = handle_file_upload(
    #     db, documents, documents, row["documents"])
    # To show old file names
    document_names = handle_file_upload(
        db, documents, uploaded_compliances, row["documents"])

    file_size = 0
    if documents != None:
        for doc in documents:
            file_size += doc.file_size

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
        "completion_date", "documents", "remarks", "completed_on", "current_status", "document_size"
    ]

    is_two_levels = is_two_levels_of_approval(db)

    if is_two_levels:
        current_status = "1"
    else:
        current_status = "2"

    history_values = [
        completion_date, ",".join(document_names),
        assignee_remarks, current_time_stamp, current_status, file_size
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
        # history_columns.extend(["approve_status", "approved_on"])+
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
        "Compliance Completed", action, 4
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
    db, session_user, user_domain_ids, user_unit_ids, unit_id
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
            " AND ac.assignee = %s " + \
            " AND IF(%s IS NOT NULL, ac.unit_id = %s,1) "
    rows = db.select_one(query, [
        ",".join(str(x) for x in user_unit_ids),
        ",".join(str(x) for x in user_domain_ids), session_user, unit_id, unit_id
    ])
    return rows["total_count"]

##########################################################
# Get Onoccurrence Compliances
##########################################################
def get_on_occurrence_compliances_for_user(
    db, session_user, user_domain_ids, user_unit_ids, unit_id, start_count,
    to_count
):
    columns = [
        "compliance_id", "statutory_provision",
        "compliance_task", "compliance_description",
        "duration_type", "duration", "document_name", "unit_id", "unit_name"
    ]
    # concat_columns = "concat(unit_code, '-', unit_name)"

    query = "SELECT ac.compliance_id, " + \
            " concat(substring(substring(c.statutory_mapping,3),1,char_length(c.statutory_mapping) -4), " + \
            " '>>' , c.statutory_provision) AS statutory_provision, " + \
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
            " AND IF(%s IS NOT NULL, ac.unit_id = %s,1) " + \
            " ORDER BY u.unit_id, document_name, compliance_task " + \
            " LIMIT %s, %s "

    rows = db.select_all(query, [
        ",".join(str(x) for x in user_unit_ids),
        ",".join(str(x) for x in user_domain_ids),
        session_user, unit_id, unit_id, int(start_count), int(to_count)
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
    current_time_stamp = get_date_time_in_date()
    columns = [
        "legal_entity_id", "unit_id", "compliance_id",
        "start_date", "due_date", "completed_by", "occurrence_remarks"
    ]
    start_date = string_to_datetime_with_time(start_date)
    duration = duration.split(" ")
    duration_value = duration[0]
    duration_type = duration[1]
    print duration_type, duration_value
    due_date = None
    if duration_type == "Day(s)":
        due_date = start_date + datetime.timedelta(days=int(duration_value))
    elif duration_type == "Hour(s)":
        due_date = start_date + datetime.timedelta(hours=int(duration_value))
    elif duration_type == "Month(s)" :
        # due_date = start_date + datetime.timedelta(months=int(duration_value))
        due_date = addMonth(int(duration_value), start_date)
    print due_date
    values = [
        legal_entity_id, unit_id, compliance_id, start_date, due_date,
        session_user, remarks
    ]

    q = "select t2.compliance_id, t3.country_id, t1.domain_id, t1.compliance_task,  " + \
        "t1.document_name, t2.approval_person, " + \
        "t2.concurrence_person, t1.statutory_mapping, t3.unit_code, t3.unit_name, t3.geography_name, " + \
        "  t4.legal_entity_name " + \
        " from tbl_assign_compliances as t2 " + \
        " inner join tbl_compliances as t1 on t2.compliance_id = t1.compliance_id " + \
        " inner join tbl_units as t3 on t2.unit_id = t3.unit_id " + \
        " inner join tbl_legal_entities as t4 on t3.legal_entity_id = t4.legal_entity_id " + \
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
    # "Primary/Secondary Legislation & Task Name" has been
    # triggered for "LE Name& Unit Code & Unit Location" has been triggered by "Assignee Name"
    maps = json.loads(row["statutory_mapping"])[0]

    if document_name not in (None, "None", "") :
        compliance_name = document_name + " - " + compliance_name

    compliance_name = "%s - %s" % (maps, compliance_name)
    uname = "%s - %s - %s" % (row["unit_code"], row["unit_name"], row["geography_name"])

    # user_ids = "{},{},{}".format(assignee_id, concurrence_id, approver_id)
    assignee_email, assignee_name = get_user_email_name(db, str(session_user))
    approver_email, approver_name = get_user_email_name(db, str(approver_id))

    notification_text = "%s has been triggered for %s has been triggered by %s " % (
        compliance_name, uname, assignee_name
    )
    print notification_text
    db.save_activity(session_user, 11, notification_text, legal_entity_id, unit_id)

    if (
        concurrence_id not in [None, "None", 0, "", "null", "Null"] and
        is_two_levels_of_approval(db)
    ):
        concurrence_email, concurrence_name = get_user_email_name(
            db, str(concurrence_id))

    save_compliance_notification(
        db, compliance_history_id, notification_text, "Compliance Started",
        "Started", 4)
    try:
        email.notify_task(
            assignee_email, assignee_name,
            concurrence_email, concurrence_name,
            approver_email, approver_name, notification_text,
            due_date, "Start"
        )
        if current_time_stamp > due_date and current_time_stamp.date() > due_date.date() :
            email.notify_task(
                assignee_email, assignee_name,
                concurrence_email, concurrence_name,
                approver_email, approver_name, compliance_name,
                due_date, "After Due Date"
            )

    except Exception, e:
        logger.logclient("error", "clientdatabase.py-start-on-occurance", e)
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
        " (SELECT concat(unit_code,' - ',unit_name) FROM tbl_units where unit_id = %s limit 1) as unit, " + \
        " com.compliance_description,ch.start_date, " + \
        " (SELECT concat(employee_code,' - ',employee_name) FROM tbl_users where user_id = ch.completed_by) as assignee,ch.completion_date, " + \
        " (SELECT concat(employee_code,' - ',employee_name) FROM tbl_users where user_id = ch.concurred_by) as concurr,ch.concurred_on, " + \
        " (SELECT concat(ifnull(employee_code, ''),' - ',employee_name) FROM tbl_users where user_id = ch.approved_by) as approver,ch.approved_on, " + \
        " (CASE WHEN (IF(com.frequency_id = 5,ch.due_date >= ch.completion_date,date(ch.due_date) >= date(ch.completion_date)) " + \
        " and (ifnull(ch.approve_status,0) = 1 AND ifnull(ch.current_status,0) = 3)) THEN 'Complied' " + \
        " WHEN (IF(com.frequency_id = 5,ch.due_date < ch.completion_date,date(ch.due_date) < date(ch.completion_date)) " +\
        " and (ifnull(ch.approve_status,0) = 1 AND ifnull(ch.current_status,0) = 3)) THEN 'Delayed Compliance' " + \
        " WHEN (IF(com.frequency_id = 5,ch.due_date < now(), date(ch.due_date) < curdate()) and ch.current_status < 3) THEN 'Over due' " + \
        " WHEN (IF(com.frequency_id = 5,ch.due_date > now(), date(ch.due_date) > curdate()) and ch.current_status < 3) THEN 'In progress' " + \
        " WHEN (ifnull(ch.approve_status, 0) = 3) THEN 'Not Complied'" + \
        " ELSE 'Pending' END) as compliance_status " + \
        " FROM tbl_compliance_history as ch " + \
        " LEFT JOIN tbl_compliances as com on ch.compliance_id = com.compliance_id " + \
        " WHERE ch.compliance_id = %s and ch.unit_id = %s " + \
        " ORDER BY ch.compliance_history_id desc limit 5"

    row = db.select_all(q, [unit_id, compliance_id, unit_id])

    # print q % (unit_id, compliance_id, unit_id)
    print row
    return row

######################################################################
# Calendar View
######################################################################
def get_calendar_view(db, request, user_id):

    unit_id = request.unit_id
    cal_date = request.cal_date

    if cal_date is None:
        year = getCurrentYear("NOW", "")
        month = getCurrentMonth("NOW", "")
    else:
        year = getCurrentYear("", cal_date)
        month = getCurrentMonth("", cal_date)

    q = "select ch.legal_entity_id, ch.unit_id, ch.completed_by, day(ch.due_date) as du_date, " + \
        " month(ch.due_date) as du_month, year(ch.due_date) as du_year,  " + \
        " count(compliance_history_id) du_count " + \
        " from tbl_compliance_history as ch " + \
        " where current_status = 0  " + \
        " and ch.due_date < DATE_ADD(now(), INTERVAL 6 MONTH)  " + \
        " and date(ch.due_date) >= date(now()) AND MONTH(ch.due_date) = %s  " + \
        " AND ch.completed_by = %s AND IF(%s IS NOT NULL, ch.unit_id = %s,1) " + \
        " group by ch.completed_by, day(due_date), month(ch.due_date), year(ch.due_date)  " + \
        " order by year(ch.due_date), month(ch.due_date), day(due_date)"
    rows = db.select_all(q, [month, user_id, unit_id, unit_id])

    q1 = " select ac.legal_entity_id, ac.unit_id, ac.assignee, " + \
         " day(DATE_SUB(ac.due_date, INTERVAL ac.trigger_before_days DAY)) as up_date,  " + \
         " month(DATE_SUB(ac.due_date, INTERVAL ac.trigger_before_days DAY)) as up_month,  " + \
         " year(DATE_SUB(ac.due_date, INTERVAL ac.trigger_before_days DAY)) as up_year,  " + \
         " count(ac.compliance_id) as up_count  " + \
         " from tbl_assign_compliances as ac  " + \
         " inner join tbl_compliances as com on ac.compliance_id = com.compliance_id and com.frequency_id != 5  " + \
         " where DATE_SUB(ac.due_date, INTERVAL ac.trigger_before_days DAY) > curdate()  " + \
         " AND ac.due_Date < DATE_ADD(now(), INTERVAL 6 MONTH)  " + \
         " AND IF(%s IS NOT NULL, ac.unit_id = %s,1) AND month(DATE_SUB(ac.due_date, INTERVAL ac.trigger_before_days DAY)) = %s  " + \
         " AND ac.assignee = %s " + \
         " group by ac.unit_id, ac.assignee, DATE_SUB(ac.due_date, INTERVAL ac.trigger_before_days DAY)"

    rows1 = db.select_all(q1, [unit_id, unit_id, month, user_id])

    return frame_calendar_view(db, unit_id, cal_date, rows, rows1, user_id)

def getCurrentYear(mode, next_date):
    if mode == "NOW":
        now = datetime.datetime.now()
    else:
        now = string_to_datetime(next_date)
    return now.year

def getCurrentMonth(mode, next_date):
    if mode == "NOW":
        now = datetime.datetime.now()
    else:
        now = string_to_datetime(next_date)
    return now.month

def totalDays(cal_date):
    if cal_date is None:
        thismonth = getFirstDate("NOW","")
        nextmonth = thismonth.replace(month=getCurrentMonth("NOW", "")+1)
    else:
        thismonth = getFirstDate("", cal_date)
        nextmonth = thismonth.replace(month=getCurrentMonth("", cal_date)+1)

    return (nextmonth - thismonth).days

def getFirstDate(mode, next_date):
    if mode == "NOW":
        now = datetime.date.today().replace(day=1)
    else:
        now = string_to_datetime(next_date).replace(day=1).date()
    return now

def currentDay():
    return datetime.datetime.now().day

def getDayName(date):
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    dayNumber = date.weekday()
    return days[dayNumber]

def get_current_inprogess_overdue(db, unit_id, user_id):
    q = " select " + \
        " sum(IF((com.frequency_id = 5 AND com.duration_type_id = 2), IF(ch.due_date >= now() and ifnull(ch.current_status,0) = 0 ,1,0), " + \
        " IF(date(ch.due_date) >= curdate() and ifnull(ch.current_status,0) = 0 ,1,0))) as inprogress_count, " + \
        " sum(IF((com.frequency_id = 5 AND com.duration_type_id = 2), IF(ch.due_date < now() and ifnull(ch.current_status,0) = 0 ,1,0), " + \
        " IF(date(ch.due_date) < curdate() and ifnull(ch.current_status,0) = 0 ,1,0))) as overdue_count " + \
        " from tbl_compliance_history as ch " + \
        " inner join tbl_compliances as com on ch.compliance_id = com.compliance_id  " + \
        " inner join tbl_client_compliances as cc on ch.unit_id = cc.unit_id and cc.domain_id = com.domain_id " + \
        " and cc.compliance_id = com.compliance_id " + \
        " inner join tbl_user_units as un on un.unit_id = ch.unit_id and un.user_id = ch.completed_by " + \
        " where un.user_id = %s and IF(%s IS NOT NULL, ch.unit_id = %s,1)"
    rows = db.select_one(q, [user_id, unit_id, unit_id])

    overdue = inprogress = 0
    if rows :
        overdue = int(rows["overdue_count"]) if rows["overdue_count"] is not None else 0
        inprogress = int(rows["inprogress_count"]) if rows["inprogress_count"] is not None else 0
    return overdue, inprogress

def frame_calendar_view(db, unit_id, cal_date, due_data, up_data, user_id):
    chart_title = "Calendar View"
    xaxis_name = "Total Compliances"
    xaxis = []
    yaxis_name = "Total Compliances"
    yaxis = []
    chartData = []
    cdata = []

    for i in range(totalDays(cal_date)) :
        overdue = 0
        inprogress = 0

        if cal_date is None:
            if i+1 == currentDay() :
                overdue, inprogress = get_current_inprogess_overdue(db, unit_id, user_id)

        xaxis.append(str(i+1))
        cdata.append({
            "date": i+1,
            "overdue": overdue,
            "upcoming": 0,
            "inprogress": inprogress,
            "duedate": 0
        })
    for d in due_data :
        idx = xaxis.index(str(d["du_date"]))
        c = cdata[idx]

        duedate = d["du_count"]
        duedate = 0 if duedate is None else int(duedate)
        # upcoming = d["upcoming_count"]
        # upcoming = 0 if upcoming is None else int(upcoming)

        # c["overdue"] += overdue
        # c["upcoming"] += upcoming
        # c["inprogress"] += inprogress
        c["duedate"] += duedate

        cdata[idx] = c

    for d in up_data :
        idx = xaxis.index(str(d["up_date"]))
        c = cdata[idx]

        # duedate = d["du_count"]
        # duedate = 0 if duedate is None else int(duedate)
        upcoming = d["up_count"]
        upcoming = 0 if upcoming is None else int(upcoming)

        # c["overdue"] += overdue
        c["upcoming"] += upcoming
        # c["inprogress"] += inprogress
        # c["duedate"] += duedate

        cdata[idx] = c

    CurrentMonth = ""
    StartDay =""

    if cal_date is None:
        CurrentMonth = str(getFirstDate("NOW",""))
        StartDay = getDayName(getFirstDate("NOW",""))
    else:
        CurrentMonth = str(getFirstDate("", cal_date))
        StartDay = getDayName(getFirstDate("", cal_date))

    chartData.append({
        "CurrentMonth": CurrentMonth,
        "StartDay": StartDay,
        "data": cdata
    })
    return clientuser.ChartSuccess(chart_title, xaxis_name, xaxis, yaxis_name, yaxis, chartData)


###############################################################################################
# Objective: To get reminder settings details
# Parameter: request object and the client id, legal entity id
# Result: return list of legal entity details, domains and organization
###############################################################################################
def get_settings_form_data(db, request):
    le_id = request.legal_entity_id
    query = "select t1.legal_entity_id, t1.legal_entity_name, (select business_group_name " + \
        "from tbl_business_groups where business_group_id = t1.business_group_id) as business_group_name, " + \
        "t1.contract_from, t1.contract_to, (select country_name from tbl_countries where country_id = " + \
        "t1.country_id) as country_name, (select two_levels_of_approval from tbl_reminder_settings where " + \
        "legal_entity_id = t1.legal_entity_id) as two_level_approve, (select assignee_reminder from " + \
        "tbl_reminder_settings where legal_entity_id = t1.legal_entity_id) as assignee_reminder, (select " + \
        "escalation_reminder_in_advance from tbl_reminder_settings where legal_entity_id = t1.legal_entity_id) " + \
        "as advance_escalation_reminder, (select escalation_reminder from tbl_reminder_settings where " + \
        "legal_entity_id = t1.legal_entity_id) as escalation_reminder, (select reassign_service_provider from " + \
        "tbl_reminder_settings where legal_entity_id = t1.legal_entity_id) as reassign_sp, t1.file_space_limit, " + \
        "t1.used_file_space, t1.total_licence, t1.used_licence from tbl_legal_entities as t1 where t1.legal_entity_id = %s"
    result = db.select_all(query, [le_id])
    settings_info = []
    for row in result:
        settings_info.append(clientuser.SettingsInfo(
            row["legal_entity_name"], row["business_group_name"], row["country_name"],
            datetime_to_string(row["contract_from"]), datetime_to_string(row["contract_to"]),
            bool(row["two_level_approve"]), row["assignee_reminder"], row["advance_escalation_reminder"],
            row["escalation_reminder"], row["reassign_sp"], str(row["file_space_limit"]),
            str(row["used_file_space"]), str(row["total_licence"]), str(row["used_licence"])
        ))

    # legal entity domains
    # query = "select t1.activation_date, t1.count as org_count, (select domain_name from tbl_domains where " + \
    #     "domain_id = t1.domain_id) as domain_name, (select organisation_name from tbl_organisation " + \
    #     "where organisation_id = t1.organisation_id) as organisation_name from tbl_legal_entity_domains as t1 " + \
    #     "where t1.legal_entity_id = %s"
    # result = db.select_all(query, [le_id])
    # le_domains_info = []
    # for row in result:
    #     if (row["domain_name"] is not None or row["organisation_name"] is not None):
    #         le_domains_info.append(clientmasters.LegalEntityDomains(
    #             row["domain_name"], row["organisation_name"], row["org_count"],
    #             activity_date=datetime_to_string(row["activation_date"])
    #         ))

    # legal entity users
    # (select username " + \
    #     "from tbl_user_login_details where user_id = t1.user_id) as user_name ," + \
    query = "select IFNULL(concat(t2.employee_code,'-',t2.employee_name),t2.employee_name) as employee_name, " + \
        "(select user_category_name from tbl_user_category where user_category_id = " + \
        "t2.user_category_id) as category_name, t2.user_level, (select concat(unit_code,'-',unit_name) " + \
        "as unit_name from tbl_units where unit_id = t2.seating_unit_id) as unit_code_name, (select concat(address,',', " + \
        "postal_code) from tbl_units where unit_id = t2.seating_unit_id) as address from " + \
        "tbl_user_legal_entities as t1 inner join tbl_users as t2 on t2.user_id = t1.user_id " + \
        "where t1.legal_entity_id = %s"
    result = db.select_all(query, [le_id])
    le_users_info = []
    for row in result:
        if row["user_level"] is not None:
            user_level_name = "Level "+str(row["user_level"])
        else:
            user_level_name = None
        le_users_info.append(clientmasters.LegalEntityUsers(
            row["employee_name"], None, user_level_name,
            row["category_name"], row["unit_code_name"], row["address"]
        ))
    return settings_info, le_users_info

###############################################################################################
# Objective: To save reminder settings details
# Parameter: request object and the client id, legal entity id
# Result: return success/failure of the transaction
###############################################################################################
def save_settings_form_data(db, request, session_user):
    le_id = request.legal_entity_id
    legal_entity_name = request.legal_entity_name
    two_level_approve = int(request.two_level_approve)
    assignee_reminder = request.assignee_reminder
    escalation_reminder_in_advance = request.advance_escalation_reminder
    escalation_reminder = request.escalation_reminder
    reassign_sp = request.reassign_sp
    current_time_stamp = get_date_time()

    columns = [
        "two_levels_of_approval", "assignee_reminder", "escalation_reminder_in_advance",
        "escalation_reminder", "reassign_service_provider", "updated_on", "updated_by"
    ]
    values = [
        two_level_approve, assignee_reminder, escalation_reminder_in_advance, escalation_reminder,
        reassign_sp, current_time_stamp, session_user
    ]
    condition = "legal_entity_id= %s "

    values.append(le_id)
    result1 = db.update(tblReminderSettings, columns, values, condition)
    if result1 is False:
        raise client_process_error("E015")

    action = "Updated reminder settings for \"%s - %s\"" % (
        le_id, legal_entity_name
    )
    db.save_activity(session_user, 4, action)

    return True
