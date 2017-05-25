import os
import datetime
from server.clientdatabase.tables import *
from clientprotocol import (
    clientcore, clientreport, clientmasters
)
import json
# from server.constants import (CLIENT_LOGO_PATH)
from server.common import (
    datetime_to_string_time, string_to_datetime, datetime_to_string,
    convert_to_dict, get_date_time_in_date
)
from server.clientdatabase.common import (
    calculate_years, get_country_domain_timelines
)
from server.clientdatabase.general import (
    calculate_ageing, get_admin_id, get_user_unit_ids, is_admin, get_from_and_to_date_for_domain
)
CLIENT_DOCS_DOWNLOAD_URL = "/client/client_documents"
FORMAT_DOWNLOAD_URL = "/client/compliance_format"
ROOT_PATH = os.path.join(os.path.split(__file__)[0], "..", "..")
# CLIENT_LOGO_PATH = "/clientlogo"

__all__ = [
    "report_reassigned_history",
    "report_reassigned_history_total",
    "report_status_report_consolidated",
    "report_status_report_consolidated_total",
    "report_statutory_settings_unit_Wise",
    "report_statutory_settings_unit_Wise_total",
    "report_domain_score_card",
    "report_le_wise_score_card",
    "report_work_flow_score_card"
]

# Reassigned History Report Start


def report_reassigned_history(
    db, country_id, legal_entity_id, domain_id, unit_id,
    act, compliance_id, usr_id, from_date, to_date, session_user, f_count, t_count
):
    from_date = string_to_datetime(from_date).date()
    to_date = string_to_datetime(to_date).date()

    query = "select rc.reassign_history_id,com.domain_id,rc.unit_id,rc.compliance_id, " + \
            "com.compliance_task, SUBSTRING_INDEX(substring(substring(com.statutory_mapping,3),1, char_length(com.statutory_mapping) -4), '>>', 1) as act_name, " + \
            "concat((select concat(ifnull(employee_code,''),' - ',employee_name) from tbl_users where user_id = rc.old_assignee),' / ', " + \
            "(select concat(ifnull(employee_code,''),' - ',employee_name) from tbl_users where user_id = rc.old_concurrer),' / ', " + \
            "(select concat(ifnull(employee_code,''),' - ',employee_name) from tbl_users where user_id = rc.old_approver)) as old_user, " + \
            "concat((select concat(ifnull(employee_code,''),' - ',employee_name) from tbl_users where user_id = rc.assignee),' / ', " + \
            "(select concat(ifnull(employee_code,''),' - ',employee_name) from tbl_users where user_id = rc.concurrer),' / ', " + \
            "(select concat(ifnull(employee_code,''),' - ',employee_name) from tbl_users where user_id = rc.approver)) as new_user, " + \
            "rc.assigned_on,rc.remarks, " + \
            "(select max(due_date) from tbl_compliance_history where compliance_id = rc.compliance_id group by compliance_id) as due_date, " + \
            "(select concat(unit_code,' - ',unit_name,' - ',address) from tbl_units where unit_id = rc.unit_id) as unit " + \
            "from  tbl_reassigned_compliances_history as rc " + \
            "inner join tbl_compliances as com on rc.compliance_id = com.compliance_id " + \
            "inner join (select compliance_id,unit_id,num from  " + \
            "(select compliance_id,unit_id,@rownum := @rownum + 1 AS num  " + \
            "from (select distinct t1.compliance_id,unit_id from tbl_reassigned_compliances_history as t1 " + \
            "inner join tbl_compliances as t2 on t1.compliance_id = t2.compliance_id) t, " + \
            "(SELECT @rownum := 0) r) as cnt " + \
            "where  cnt.num between %s and %s) as t01 on rc.compliance_id = t01.compliance_id and rc.unit_id = t01.unit_id " + \
            "where  com.domain_id = %s and rc.unit_id = %s and  " + \
            "IF(%s IS NOT NULL,SUBSTRING_INDEX(substring(substring(com.statutory_mapping,3),1, char_length(com.statutory_mapping) -4), '>>', 1) = %s,1) " + \
            "and IF(%s IS NOT NULL, rc.compliance_id = %s,1) " + \
            "and (IF(%s IS NOT NULL,rc.old_assignee = 1, 1) " + \
            "or IF(%s IS NOT NULL,rc.old_concurrer = 1, 1) " + \
            "or IF(%s IS NOT NULL,rc.old_approver = 1, 1)  " + \
            "or IF(%s IS NOT NULL,rc.assignee = 1, 1) " + \
            "or IF(%s IS NOT NULL,rc.concurrer = 1, 1) " + \
            "or IF(%s IS NOT NULL,rc.approver = 1, 1)) " + \
            "and rc.assigned_on >= %s and rc.assigned_on <= %s " + \
            "order by t01.num asc,rc.reassign_history_id desc; "

            # "IF(%s IS NOT NULL,com.statutory_mapping like %s,1) " + \
            # "and IF(%s IS NOT NULL,SUBSTRING_INDEX(substring(substring(com.statutory_mapping,3),1, char_length(com.statutory_mapping) -4), '>>', 1) = %s,1)" + \

    rows = db.select_all(query, [
        f_count, t_count, domain_id, unit_id, act, act, compliance_id,
        compliance_id, usr_id, usr_id, usr_id, usr_id,
        usr_id, usr_id, from_date, to_date
    ])

    return return_reassinged_history_report(
        db, rows, country_id, legal_entity_id
    )


def return_reassinged_history_report(db, result, country_id, legal_entity_id):
    compliances = []
    for r in result:
        domain_id = r["domain_id"]
        unit_id = r["unit_id"]
        act_name = r["act_name"]
        compliance_id = r["compliance_id"]
        compliance_task = r["compliance_task"]
        old_user = r["old_user"]
        new_user = r["new_user"]
        assigned_on = datetime_to_string(r["assigned_on"])
        remarks = r["remarks"]
        due_date = datetime_to_string(r["due_date"])
        unit = r["unit"]

        compliance = clientcore.ReassignedHistoryReportSuccess(
            country_id, legal_entity_id, domain_id, unit_id, act_name, compliance_id, compliance_task,
            old_user, new_user, assigned_on, remarks, due_date, unit
        )
        compliances.append(compliance)
    return compliances


def report_reassigned_history_total(
    db, country_id, legal_entity_id, domain_id, unit_id,
    act, compliance_id, usr_id, from_date, to_date, session_user
):
    from_date = string_to_datetime(from_date).date()
    to_date = string_to_datetime(to_date).date()

    query = "select count(Distinct rc.compliance_id) as total_count from  tbl_reassigned_compliances_history as rc " + \
            "inner join tbl_compliances as com on rc.compliance_id = com.compliance_id " + \
            "inner join (select compliance_id,unit_id,num from  " + \
            "(select compliance_id,unit_id,@rownum := @rownum + 1 AS num  " + \
            "from (select distinct t1.compliance_id,unit_id from tbl_reassigned_compliances_history as t1 " + \
            "inner join tbl_compliances as t2 on t1.compliance_id = t2.compliance_id) t, " + \
            "(SELECT @rownum := 0) r) as cnt ) as t01 on rc.compliance_id = t01.compliance_id and rc.unit_id = t01.unit_id " + \
            "where com.domain_id = %s and rc.unit_id = %s and  " + \
            "IF(%s IS NOT NULL,SUBSTRING_INDEX(substring(substring(com.statutory_mapping,3),1, char_length(com.statutory_mapping) -4), '>>', 1) = %s,1) " + \
            "and IF(%s IS NOT NULL, rc.compliance_id = %s,1) " + \
            "and (IF(%s IS NOT NULL,rc.old_assignee = 1, 1) " + \
            "or IF(%s IS NOT NULL,rc.old_concurrer = 1, 1) " + \
            "or IF(%s IS NOT NULL,rc.old_approver = 1, 1)  " + \
            "or IF(%s IS NOT NULL,rc.assignee = 1, 1) " + \
            "or IF(%s IS NOT NULL,rc.concurrer = 1, 1) " + \
            "or IF(%s IS NOT NULL,rc.approver = 1, 1)) " + \
            "and rc.assigned_on >= %s and rc.assigned_on <= %s "

    rows = db.select_one(query, [
        domain_id, unit_id, act, act, compliance_id,
        compliance_id, usr_id, usr_id, usr_id, usr_id,
        usr_id, usr_id, from_date, to_date
    ])
    return int(rows["total_count"])
# Reassigned History Report End


# Status Report Consolidated Report Start
def report_status_report_consolidated(
    db, country_id, legal_entity_id, domain_id, unit_id,
    act, compliance_id, frequency_id, user_type_id, status_name, usr_id, from_date, to_date, session_user, f_count, t_count
):
    from_date = string_to_datetime(from_date).date()
    to_date = string_to_datetime(to_date).date()

    # print "--------------------------->", from_date, to_date

    query = "select t01.num, " + \
            "acl.compliance_activity_id,ch.compliance_history_id, ch.legal_entity_id,ch.unit_id, " + \
            "(select concat(unit_code,' - ',unit_name,' - ',address,' - ', postal_code) from tbl_units where unit_id = ch.unit_id) as unit,ch.compliance_id, " + \
            "concat(com.document_name,' - ',com.compliance_task) as compliance_name, " + \
            "(select frequency from tbl_compliance_frequency where frequency_id = com.frequency_id) as frequency_name, " + \
            "SUBSTRING_INDEX(substring(substring(com.statutory_mapping,3),1, char_length(com.statutory_mapping) -4), '>>', 1) as act_name, " + \
            "acl.activity_on, " + \
            "ch.due_date,ch.completion_date, " + \
            "(CASE WHEN (ch.due_date < ch.completion_date and ch.current_status = 3) THEN 'Delayed Compliance' " + \
            "WHEN (ch.due_date >= ch.completion_date and ch.approve_status <> 3 and ch.current_status = 3) THEN 'Complied' " + \
            "WHEN (ch.due_date >= ch.completion_date and ch.current_status < 3) THEN 'In Progress' " + \
            "WHEN (ch.due_date < ch.completion_date and ch.current_status < 3) THEN 'Not Complied' " + \
            "WHEN (ch.approve_status = 3 and ch.current_status = 3) THEN 'Not Complied' " + \
            "WHEN (ch.completion_date IS NULL and IFNULL(ch.current_status,0) = 0) THEN 'In Progress' " + \
            "ELSE 'In Progress' END) as compliance_task_status, " + \
            "(CASE WHEN acl.activity_by = ch.completed_by THEN ch.documents ELSE '-' END) as uploaded_document, " + \
            "IFNULL(acl.action,'Pending') as activity_status, " + \
            "(CASE WHEN acl.activity_by = ch.approved_by THEN (select IFNULL(concat(employee_code,' - ',employee_name),'Administrator') from tbl_users where user_id = ac.approval_person) " + \
            "WHEN acl.activity_by = ch.concurred_by THEN (select concat(employee_code,' - ',employee_name) from tbl_users where user_id = ac.concurrence_person)  " + \
            "WHEN acl.activity_by = ch.completed_by THEN (select concat(employee_code,' - ',employee_name) from tbl_users where user_id = ac.assignee) ELSE  " + \
            "(select concat(employee_code,' - ',employee_name) from tbl_users where user_id = ac.assignee) END) as user_name, ch.start_date " + \
            "from tbl_compliance_history as ch " + \
            "inner join tbl_compliances as com on ch.compliance_id = com.compliance_id " + \
            "left join tbl_compliance_activity_log as acl on ch.compliance_history_id = acl.compliance_history_id " + \
            "inner join tbl_assign_compliances as ac on ch.compliance_id = ac.compliance_id and ch.unit_id = ac.unit_id " + \
            "inner join ( " + \
                "select compliance_history_id,num from  " + \
                "(select compliance_history_id,@rownum := @rownum + 1 AS num  " + \
                "from (select distinct ch.compliance_history_id  " + \
                        "from tbl_compliance_history as ch " + \
                        "inner join tbl_compliances as com on ch.compliance_id = com.compliance_id " + \
                        "left join tbl_compliance_activity_log as acl on ch.compliance_history_id = acl.compliance_history_id " + \
                        "inner join tbl_assign_compliances as ac on ch.compliance_id = ac.compliance_id and ch.unit_id = ac.unit_id " + \
                        "where com.country_id = %s and ch.legal_entity_id = %s " + \
                "and com.domain_id = %s " + \
                "and IF(%s IS NOT NULL, acl.unit_id = %s,1) " + \
                "and IF(%s IS NOT NULL,SUBSTRING_INDEX(substring(substring(com.statutory_mapping,3),1, char_length(com.statutory_mapping) -4), '>>', 1) = %s,1) " + \
                "and IF(%s IS NOT NULL, ch.compliance_id = %s,1) " + \
                "and IF(%s > 0, com.frequency_id = %s,1) " + \
                "and (CASE %s WHEN 1 THEN (ch.completed_by = acl.activity_by OR acl.activity_by IS NULL) " + \
                "WHEN 2 THEN ch.concurred_by = acl.activity_by WHEN 3 THEN ch.approved_by = acl.activity_by " + \
                "ELSE 1 END) " + \
                "and IF(%s IS NOT NULL, ((ch.completion_date is not null and ch.completed_by = %s)  OR (ch.concurrence_status is not null and ch.concurred_by = %s) OR (ch.approve_status is not null and ch.approved_by = %s)),1) " + \
                "and date(ch.due_date) >= %s and date(ch.due_date) <= %s " + \
                "and IF(%s <> 'All',(CASE WHEN (ch.due_date < ch.completion_date and ch.current_status = 3) THEN 'Delayed Compliance' " + \
                "WHEN (ch.due_date >= ch.completion_date and ch.approve_status <> 3 and ch.current_status = 3) THEN 'Complied' " + \
                "WHEN (ch.due_date >= ch.completion_date and ch.current_status < 3) THEN 'In Progress' " + \
                "WHEN (ch.due_date < ch.completion_date and ch.current_status < 3) THEN 'Not Complied' " + \
                "WHEN (ch.approve_status = 3 and ch.current_status = 3) THEN 'Not Complied' " + \
                "WHEN (ch.completion_date IS NULL and IFNULL(ch.current_status,0) = 0) THEN 'In Progress' " + \
                "ELSE 'In Progress' END) = %s,1) " + \
                "order by ch.compliance_history_id) t, " + \
                "(SELECT @rownum := 0) r) as cnt " + \
                "where cnt.num between %s and %s ) t01  " + \
            "on ch.compliance_history_id = t01.compliance_history_id " + \
            "order by t01.num,ch.compliance_history_id,acl.compliance_activity_id desc "

            # "and IF(%s IS NOT NULL, (ch.completed_by = %s OR ch.concurred_by = %s OR ch.approved_by = %s),1) " + \

            # "where rc.assigned_on >= %s and rc.assigned_on <= %s " + \
    rows = db.select_all(query, [
        country_id, legal_entity_id, domain_id, unit_id, unit_id, act, act, compliance_id,
        compliance_id, frequency_id, frequency_id, user_type_id, usr_id, usr_id, usr_id,
        usr_id, from_date, to_date, status_name, status_name, f_count, t_count
    ])

    return return_status_report_consolidated(
        db, rows, country_id, legal_entity_id
    )


def return_status_report_consolidated(db, result, country_id, legal_entity_id):
    compliances = []
    for r in result:
        # compliance_activity_id, compliance_history_id, legal_entity_id, unit_id, unit, compliance_id, compliance_name, frequency_name, act_name, activity_on, due_date, completion_date, task_status, uploaded_document, activity_status, user_name
        compliance_activity_id = r["compliance_activity_id"]
        compliance_history_id = r["compliance_history_id"]
        legal_entity_id = r["legal_entity_id"]
        unit_id = r["unit_id"]
        unit = r["unit"]
        compliance_id = r["compliance_id"]
        compliance_name = r["compliance_name"]
        frequency_name = r["frequency_name"]
        act_name = r["act_name"]
        activity_on = datetime_to_string(r["activity_on"])
        due_date = datetime_to_string(r["due_date"])
        completion_date = datetime_to_string(r["completion_date"])
        task_status = r["compliance_task_status"]
        uploaded_document = r["uploaded_document"]
        activity_status = r["activity_status"]
        user_name = r["user_name"]
        start_date = datetime_to_string(r["start_date"])

        compliance = clientcore.GetStatusReportConsolidatedSuccess(
            compliance_activity_id, compliance_history_id, legal_entity_id, unit_id, unit, compliance_id, compliance_name, frequency_name,
            act_name, activity_on, due_date, completion_date, task_status, uploaded_document, activity_status, user_name, start_date
        )
        compliances.append(compliance)
    return compliances


def report_status_report_consolidated_total(
    db, country_id, legal_entity_id, domain_id, unit_id,
    act, compliance_id, frequency_id, user_type_id, status_name, usr_id, from_date, to_date, session_user
):
    from_date = string_to_datetime(from_date).date()
    to_date = string_to_datetime(to_date).date()

    query = "select count(Distinct ch.compliance_history_id) as total_count from tbl_compliance_history as ch " + \
            "inner join tbl_compliances as com on ch.compliance_id = com.compliance_id " + \
            "left join tbl_compliance_activity_log as acl on ch.compliance_history_id = acl.compliance_history_id " + \
            "inner join tbl_assign_compliances as ac on ch.compliance_id = ac.compliance_id and ch.unit_id = ac.unit_id " + \
            "inner join ( " + \
                "select compliance_history_id,num from  " + \
                "(select compliance_history_id,@rownum := @rownum + 1 AS num  " + \
                "from (select distinct ch.compliance_history_id  " + \
                        "from tbl_compliance_history as ch " + \
                        "inner join tbl_compliances as com on ch.compliance_id = com.compliance_id " + \
                        "left join tbl_compliance_activity_log as acl on ch.compliance_history_id = acl.compliance_history_id " + \
                        "inner join tbl_assign_compliances as ac on ch.compliance_id = ac.compliance_id and ch.unit_id = ac.unit_id " + \
                        "where com.country_id = %s and ch.legal_entity_id = %s " + \
                "and com.domain_id = %s " + \
                "and IF(%s IS NOT NULL, acl.unit_id = %s,1) " + \
                "and IF(%s IS NOT NULL,SUBSTRING_INDEX(substring(substring(com.statutory_mapping,3),1, char_length(com.statutory_mapping) -4), '>>', 1) = %s,1) " + \
                "and IF(%s IS NOT NULL, ch.compliance_id = %s,1) " + \
                "and IF(%s > 0, com.frequency_id = %s,1) " + \
                "and (CASE %s WHEN 1 THEN (ch.completed_by = acl.activity_by OR acl.activity_by IS NULL) " + \
                "WHEN 2 THEN ch.concurred_by = acl.activity_by WHEN 3 THEN ch.approved_by = acl.activity_by " + \
                "ELSE 1 END) " + \
                "and IF(%s IS NOT NULL, (ch.completed_by = %s OR ch.concurred_by = %s OR ch.approved_by = %s),1) " + \
                "and date(ch.due_date) >= %s and date(ch.due_date) <= %s " + \
                "and IF(%s <> 'All',(CASE WHEN (ch.due_date < ch.completion_date and ch.current_status = 3) THEN 'Delayed Compliance' " + \
                "WHEN (ch.due_date >= ch.completion_date and ch.current_status = 3) THEN 'Complied' " + \
                "WHEN (ch.due_date >= ch.completion_date and ch.current_status < 3) THEN 'In Progress' " + \
                "WHEN (ch.due_date < ch.completion_date and ch.current_status < 3) THEN 'Not Complied' " + \
                "WHEN (ch.completion_date IS NULL and IFNULL(ch.current_status,0) = 0) THEN 'In Progress' " + \
                "ELSE 'In Progress' END) = %s,1) " + \
                "order by ch.compliance_history_id) t, " + \
                "(SELECT @rownum := 0) r) as cnt ) t01  " + \
            "on ch.compliance_history_id = t01.compliance_history_id "

    rows = db.select_one(query, [
        country_id, legal_entity_id, domain_id, unit_id, unit_id, act, act, compliance_id, compliance_id,
        frequency_id, frequency_id, user_type_id, usr_id, usr_id, usr_id, usr_id, from_date, to_date, status_name, status_name
    ])
    return int(rows["total_count"])
# Status Report Consolidated Report End


# Statutory Settings Unit Wise Start
def report_statutory_settings_unit_Wise(
    db, country_id, bg_id, legal_entity_id, domain_id, unit_id,
        div_id, cat_id, act, compliance_id, frequency_id, status_name, session_user, f_count, t_count
):
    f_date, t_date = get_from_and_to_date_for_domain(db, country_id, domain_id)

    query = "select num,cnt.compliance_id,cnt.unit_id,cnt.frequency,cnt.compliance_task,cnt.act_name,cnt.task_status, " + \
            "cnt.document_name, cnt.format_file as download_url, (select concat('Mr. ',employee_name) from tbl_users where user_id = aclh.activity_by) as user_name,  " + \
            "ifnull(aclh.due_date,cnt.due_date) as due_date ,cnt.unit_name " + \
            "from  " + \
            "(select @rownum := @rownum + 1 AS num ,t.* from  " + \
            "(select   " + \
            "cc.compliance_id,cc.unit_id, cf.frequency,  " + \
            "com.compliance_task,  " + \
            "SUBSTRING_INDEX(substring(substring(com.statutory_mapping,3),1, char_length(com.statutory_mapping) -4), '>>', 1) as act_name,  " + \
            "(CASE ifnull(cc.compliance_opted_status,0) WHEN 1 THEN   " + \
            "(CASE WHEN ac.compliance_id IS NULL and ac.unit_id IS NULL   " + \
            "THEN 'Un-Assigned' ELSE 'Assigned' END) ELSE 'Not Opted' END) as task_status,  " + \
            "com.document_name, com.format_file, " + \
            "ac.due_date, " + \
            "concat(unt.unit_code,' - ',unt.unit_name,' - ',unt.address) as unit_name  " + \
            "from tbl_client_compliances as cc  " + \
            "left join tbl_assign_compliances ac on cc.unit_id = ac.unit_id and cc.compliance_id = ac.compliance_id  " + \
            "inner join tbl_compliances as com on cc.compliance_id = com.compliance_id  " + \
            "inner join tbl_legal_entities as lg on cc.legal_entity_id = lg.legal_entity_id  " + \
            "inner join tbl_units as unt on cc.unit_id = unt.unit_id  " + \
            "inner join tbl_compliance_frequency as cf on com.frequency_id = cf.frequency_id  " + \
            "WHERE cc.compliance_opted_status is not null " + \
            "and com.country_id = %s   " + \
            "and IF(%s IS NOT NULL,lg.business_group_id = %s,1)  " + \
            "and cc.legal_entity_id = %s and cc.domain_id = %s  " + \
            "and IF(%s IS NOT NULL,unt.division_id = %s,1)  " + \
            "and IF(%s IS NOT NULL,unt.category_id = %s,1)  " + \
            "and IF(%s IS NOT NULL,unt.unit_id = %s,1)  " + \
            "and IF(%s IS NOT NULL,SUBSTRING_INDEX(substring(substring(com.statutory_mapping,3),1, char_length(com.statutory_mapping) -4), '>>', 1) = %s,1)  " + \
            "and IF(%s > 0,cf.frequency_id = %s,1)  " + \
            "and IF(%s IS NOT NULL,com.compliance_id = %s,1)  " + \
            "and IF(%s <> 'All', (CASE IFNULL(cc.compliance_opted_status,0) WHEN 1 THEN   " + \
            "(CASE WHEN ac.compliance_id IS NULL and ac.unit_id IS NULL THEN 'Un-Assigned'   " + \
            "ELSE 'Assigned' END) ELSE 'Not Opted' END) = %s,1) " + \
            "and cc.compliance_opted_status is not null ) as t, " + \
            "(SELECT @rownum := 0) r ) as cnt  " + \
            "left join (select ch.compliance_id,ch.unit_id,acl.activity_by,ch.due_date from tbl_compliance_history as ch   " + \
            "inner join tbl_compliance_activity_log as acl on ch.compliance_history_id = acl.compliance_history_id   " + \
            "and ch.completed_by = acl.activity_by and ch.due_date >= %s and ch.due_date <= %s) as aclh  " + \
            "on cnt.compliance_id = aclh.compliance_id and cnt.unit_id = aclh.unit_id  " + \
            "where cnt.num between %s and %s " + \
            "order by cnt.num,cnt.unit_id, cnt.compliance_id "

    rows = db.select_all(query, [
        country_id, bg_id, bg_id, legal_entity_id, domain_id, div_id,
        div_id, cat_id, cat_id, unit_id, unit_id, act, act, frequency_id, frequency_id,
        compliance_id, compliance_id, status_name, status_name, f_date, t_date, f_count, t_count
    ])

    return return_statutory_settings_unit_Wise(
        db, rows, country_id, legal_entity_id
    )


def return_statutory_settings_unit_Wise(db, result, country_id, legal_entity_id):
    compliances = []
    for r in result:
        print r["num"]
        compliance_id = r["compliance_id"]
        frequency = r["frequency"]
        compliance_task = r["compliance_task"]
        act_name = r["act_name"]
        task_status = r["task_status"]
        document_name = r["document_name"]
        download_url = r["download_url"]
        user_name = r["user_name"]
        due_date = datetime_to_string(r["due_date"])
        unit = r["unit_name"]
        unit_id = r["unit_id"]

        compliance = clientcore.GetStatutorySettingsUnitWiseSuccess(
            compliance_id, frequency, compliance_task, act_name, task_status, document_name, download_url, user_name, due_date, unit, unit_id
        )
        compliances.append(compliance)
    return compliances


def report_statutory_settings_unit_Wise_total(
    db, country_id, bg_id, legal_entity_id, domain_id, unit_id, div_id, cat_id,
        act, compliance_id, frequency_id, status_name, session_user
):
    f_date, t_date = get_from_and_to_date_for_domain(db, country_id, domain_id) 

    query = "select count(distinct num) as total_count from  " + \
            "(select @rownum := @rownum + 1 AS num ,t.* from  " + \
            "(select   " + \
            "cc.compliance_id,cc.unit_id, cf.frequency,  " + \
            "com.compliance_task,  " + \
            "SUBSTRING_INDEX(substring(substring(com.statutory_mapping,3),1, char_length(com.statutory_mapping) -4), '>>', 1) as act_name,  " + \
            "(CASE ifnull(cc.compliance_opted_status,0) WHEN 1 THEN   " + \
            "(CASE WHEN ac.compliance_id IS NULL and ac.unit_id IS NULL   " + \
            "THEN 'Un-Assigned' ELSE 'Assigned' END) ELSE 'Not Opted' END) as task_status,  " + \
            "com.document_name, com.format_file, " + \
            "ac.due_date, " + \
            "concat(unt.unit_code,' - ',unt.unit_name,' - ',unt.address) as unit_name  " + \
            "from tbl_client_compliances as cc  " + \
            "left join tbl_assign_compliances ac on cc.unit_id = ac.unit_id and cc.compliance_id = ac.compliance_id  " + \
            "inner join tbl_compliances as com on cc.compliance_id = com.compliance_id  " + \
            "inner join tbl_legal_entities as lg on cc.legal_entity_id = lg.legal_entity_id  " + \
            "inner join tbl_units as unt on cc.unit_id = unt.unit_id  " + \
            "inner join tbl_compliance_frequency as cf on com.frequency_id = cf.frequency_id  " + \
            "WHERE cc.compliance_opted_status is not null " + \
            "and com.country_id = %s   " + \
            "and IF(%s IS NOT NULL,lg.business_group_id = %s,1)  " + \
            "and cc.legal_entity_id = %s and cc.domain_id = %s  " + \
            "and IF(%s IS NOT NULL,unt.division_id = %s,1)  " + \
            "and IF(%s IS NOT NULL,unt.category_id = %s,1)  " + \
            "and IF(%s IS NOT NULL,unt.unit_id = %s,1)  " + \
            "and IF(%s IS NOT NULL,SUBSTRING_INDEX(substring(substring(com.statutory_mapping,3),1, char_length(com.statutory_mapping) -4), '>>', 1) = %s,1)  " + \
            "and IF(%s > 0,cf.frequency_id = %s,1)  " + \
            "and IF(%s IS NOT NULL,com.compliance_id = %s,1)  " + \
            "and IF(%s <> 'All', (CASE IFNULL(cc.compliance_opted_status,0) WHEN 1 THEN   " + \
            "(CASE WHEN ac.compliance_id IS NULL and ac.unit_id IS NULL THEN 'Un-Assigned'   " + \
            "ELSE 'Assigned' END) ELSE 'Not Opted' END) = %s,1) " + \
            "and cc.compliance_opted_status is not null ) as t, " + \
            "(SELECT @rownum := 0) r ) as cnt  " + \
            "left join (select ch.compliance_id,ch.unit_id,acl.activity_by,ch.due_date from tbl_compliance_history as ch   " + \
            "inner join tbl_compliance_activity_log as acl on ch.compliance_history_id = acl.compliance_history_id   " + \
            "and ch.completed_by = acl.activity_by and ch.due_date >= %s and ch.due_date <= %s) as aclh  " + \
            "on cnt.compliance_id = aclh.compliance_id and cnt.unit_id = aclh.unit_id  " + \
            "order by cnt.num,cnt.unit_id, cnt.compliance_id "
            
    rows = db.select_one(query, [
        country_id, bg_id, bg_id, legal_entity_id, domain_id, div_id,
        div_id, cat_id, cat_id, unit_id, unit_id, act, act, frequency_id, frequency_id,
        compliance_id, compliance_id, status_name, status_name, f_date, t_date
    ])
    return int(rows["total_count"])
# Statutory Settings Unit Wise End

# Domain Score Card Start


def report_domain_score_card(
    db, country_id, bg_id, legal_entity_id, domain_id, div_id, cat_id, session_user
):
    query = "select cc.domain_id,(select domain_name from tbl_domains where domain_id = cc.domain_id) as domain_name, " + \
            "sum(IF(cc.compliance_opted_status = 0,1,0)) as not_opted_count, " + \
            "SUM(IF(ifnull(cc.compliance_opted_status,0) = 1 and IFNULL(ac.compliance_id,0) = 0,1,0)) as unassigned_count, " + \
            "(IFNULL(csu.complied_count, 0) + IFNULL(csu.delayed_count, 0) + " + \
            "IFNULL(csu.inprogress_count, 0) + IFNULL(csu.overdue_count, 0)) as assigned_count " + \
            "from tbl_client_compliances as cc " + \
            "inner join tbl_units as unt on cc.unit_id = unt.unit_id " + \
            "left join tbl_assign_compliances as ac on cc.compliance_id = ac.compliance_id and cc.unit_id = ac.unit_id and cc.domain_id = ac.domain_id " + \
            "left join (select sum(inprogress_count) as inprogress_count,sum(overdue_count) as overdue_count, " + \
            "sum(delayed_count) as delayed_count,sum(complied_count) as complied_count,domain_id,legal_entity_id, unit_id, " + \
            "date(concat_ws('-',chart_year,month_from,1)) as from_date,last_day(date(concat_ws('-',chart_year,month_to,1))) as to_date " + \
            "From tbl_compliance_status_chart_unitwise " + \
            "where utc_date() >= date(concat_ws('-',chart_year,month_from,1)) " + \
            "and utc_date() <= (if(month_from > 1,last_day(date(concat_ws('-',(chart_year+1),month_to,1))), " + \
            "last_day(date(concat_ws('-',chart_year,month_to,1))))) " + \
            "group by domain_id " + \
            ") as csu on cc.legal_entity_id = csu.legal_entity_id and cc.domain_id = csu.domain_id and cc.unit_id = csu.unit_id " + \
            "where unt.country_id = %s " + \
            "and IF(%s IS NOT NULL,unt.business_group_id = %s,1) " + \
            "and cc.legal_entity_id = %s " + \
            "and IF(%s IS NOT NULL,unt.division_id = %s,1) " + \
            "and IF(%s IS NOT NULL,unt.category_id = %s,1) " + \
            "and IF(%s IS NOT NULL,cc.domain_id = %s,1) " + \
            "group by cc.domain_id "

    domain_wise_count = db.select_all(query, [country_id, bg_id, bg_id, legal_entity_id, div_id, div_id, cat_id, cat_id, domain_id, domain_id])
    # "sum(IF(ifnull(cc.compliance_opted_status,0) = 0,1,0)) as not_opted_count, " + \

    def domain_wise_unit_count(country_id, bg_id, legal_entity_id, div_id, cat_id, domain_id):
        query_new = "select cc.unit_id,(select domain_name from tbl_domains where domain_id = cc.domain_id) as domain_name, " + \
                    "concat(unt.unit_code,' - ',unt.unit_name) as units, " + \
                    "sum(IF(cc.compliance_opted_status = 0,1,0)) as not_opted_count, " + \
                    "SUM(IF((ifnull(cc.compliance_opted_status,0) = 1 and ac.compliance_id IS NULL),1,0)) as unassigned_count, " + \
                    "IFNULL(csu.complied_count, 0) as complied_count, IFNULL(csu.delayed_count, 0) as delayed_count,  " + \
                    "IFNULL(csu.inprogress_count, 0) as inprogress_count, IFNULL(csu.overdue_count, 0) as overdue_count " + \
                    "from tbl_client_compliances as cc " + \
                    "inner join tbl_units as unt on cc.unit_id = unt.unit_id " + \
                    "left join (select sum(inprogress_count) as inprogress_count,sum(overdue_count) as overdue_count, " + \
                    "sum(delayed_count) as delayed_count,sum(complied_count) as complied_count,domain_id,legal_entity_id,unit_id, " + \
                    "date(concat_ws('-',chart_year,month_from,1)) as from_date,last_day(date(concat_ws('-',chart_year,month_to,1))) as to_date " + \
                    "From tbl_compliance_status_chart_unitwise " + \
                    "where utc_date() >= date(concat_ws('-',chart_year,month_from,1)) " + \
                    "and utc_date() <= (if(month_from > 1,last_day(date(concat_ws('-',(chart_year+1),month_to,1))), " + \
                    "last_day(date(concat_ws('-',chart_year,month_to,1))))) " + \
                    "group by domain_id,unit_id) as csu on cc.legal_entity_id = csu.legal_entity_id and cc.domain_id = csu.domain_id and cc.unit_id = csu.unit_id " + \
                    "left join tbl_assign_compliances as ac on cc.compliance_id = ac.compliance_id and cc.unit_id = ac.unit_id and cc.domain_id = ac.domain_id " + \
                    "where unt.country_id = %s " + \
                    "and IF(%s IS NOT NULL,unt.business_group_id = %s,1) " + \
                    "and cc.legal_entity_id = %s " + \
                    "and IF(%s IS NOT NULL,unt.division_id = %s,1) " + \
                    "and IF(%s IS NOT NULL,unt.category_id = %s,1) " + \
                    "and IF(%s IS NOT NULL,cc.domain_id = %s,1) " + \
                    "group by cc.domain_id,cc.unit_id"

        rows = db.select_all(query_new, [country_id, bg_id, bg_id, legal_entity_id, div_id, div_id, cat_id, cat_id, domain_id, domain_id])
        units = []
        for r in rows:
            unit_id = int(r["unit_id"])
            domain_name = r["domain_name"]
            unit = r["units"]
            not_opted_count = int(r["not_opted_count"])
            unassigned_count = int(r["unassigned_count"])
            complied_count = int(r["complied_count"])
            delayed_count = int(r["delayed_count"])
            inprogress_count = int(r["inprogress_count"])
            overdue_count = int(r["overdue_count"])
            unit_row = clientcore.GetDomainWiseUnitScoreCardSuccess(
                unit_id, domain_name, unit, not_opted_count, unassigned_count, complied_count, delayed_count, inprogress_count, overdue_count)
            units.append(unit_row)
        return units
    compliances = []
    for r in domain_wise_count:
        domain_id = int(r["domain_id"])
        domain_name = r["domain_name"]
        not_opted_count = int(r["not_opted_count"])
        unassigned_count = int(r["unassigned_count"])
        assigned_count = int(r["assigned_count"])
        units_count = domain_wise_unit_count(
            country_id, bg_id, legal_entity_id, div_id, cat_id, domain_id)
        compliance = clientcore.GetDomainScoreCardSuccess(
            domain_id, domain_name, not_opted_count, unassigned_count, assigned_count, units_count)
        compliances.append(compliance)
    return compliances
# Domain Score Card End


# Legal Entity Wise Score Card Start
def report_le_wise_score_card(
    db, country_id, legal_entity_id, domain_id, session_user, session_category
):
    query = "select ifnull(sum(if((com.frequency_id = 5 and com.duration_type_id = 2), if(ch.due_date >= now() and ch.current_status < 3,1,0), " + \
            "if(date(ch.due_date) >= date(now()) and ch.current_status < 3,1,0))),0) as inprogress_count, " + \
            "ifnull(sum(if(ch.current_status = 3,1,0)),0) as completed_count, " + \
            "ifnull(sum(if((com.frequency_id = 5 and com.duration_type_id = 2),if(ch.due_date < now() and ch.current_status < 3,1,0), " + \
            "if(date(ch.due_date) < date(now()) and ch.current_status < 3,1,0))),0) as overdue_count " + \
            "from tbl_compliance_history as ch " + \
            "inner join tbl_units as unt on ch.unit_id = unt.unit_id " + \
            "inner join tbl_compliances as com on ch.compliance_id = com.compliance_id " + \
            "left join (Select uu.unit_id,ud.domain_id from tbl_user_units as uu " + \
            "inner join tbl_user_domains as ud on uu.user_id = ud.user_id " + \
            "where uu.user_id = %s and ud.domain_id = %s) as uud on ch.unit_id = uud.unit_id and com.domain_id = uud.domain_id " + \
            "where ch.legal_entity_id = %s and com.domain_id = %s " + \
            "and IF(%s > 3,ch.unit_id = uud.unit_id and com.domain_id = uud.domain_id,1) "

    domain_wise_count = db.select_all(query, [session_user, domain_id, legal_entity_id, domain_id, session_category])

    def inprogress_unit_wise_count(legal_entity_id, domain_id):
        query = "select ch.unit_id,concat(unt.unit_code,' - ',unt.unit_name) as unitname, " + \
                "sum(if((com.frequency_id = 5 and com.duration_type_id = 2),if(ch.due_date >= now() and ch.current_status = 0,1,0), " + \
                "if(date(ch.due_date) >= date(now()) and ch.current_status = 0,1,0))) as to_complete, " + \
                "sum(if((com.frequency_id = 5 and com.duration_type_id = 2),if(ch.due_date >= now() and ch.current_status = 1,1,0), " + \
                "if(date(ch.due_date) >= date(now()) and ch.current_status = 1,1,0))) as to_concur, " + \
                "sum(if((com.frequency_id = 5 and com.duration_type_id = 2),if(ch.due_date >= now() and ch.current_status = 2,1,0), " + \
                "if(date(ch.due_date) >= date(now()) and ch.current_status = 2,1,0))) as to_approver " + \
                "from tbl_compliance_history as ch " + \
                "inner join tbl_units as unt on ch.unit_id = unt.unit_id " + \
                "inner join tbl_compliances as com on ch.compliance_id = com.compliance_id " + \
                "left join (Select uu.unit_id,ud.domain_id from tbl_user_units as uu " + \
                "inner join tbl_user_domains as ud on uu.user_id = ud.user_id " + \
                "where uu.user_id = %s and ud.domain_id = %s) as uud on ch.unit_id = uud.unit_id and com.domain_id = uud.domain_id " + \
                "where ch.legal_entity_id = %s and com.domain_id = %s " + \
                "and IF(%s > 3,ch.unit_id = uud.unit_id and com.domain_id = uud.domain_id,1) " + \
                "group by ch.unit_id"

        rows = db.select_all(query, [session_user, domain_id, legal_entity_id, domain_id, session_category])

        inprogress_unit = []
        for r in rows:
            unit_id = int(r["unit_id"])
            unit = r["unitname"]
            to_complete = int(r["to_complete"])
            to_concur = int(r["to_concur"])
            to_approve = int(r["to_approver"])
            result = clientcore.GetInprogressUnitWiseCountSuccess(
                unit_id, unit, to_complete, to_concur, to_approve)
            inprogress_unit.append(result)
        return inprogress_unit

    def inprogress_user_wise_count(legal_entity_id, domain_id):

        query = "select usr.user_id,ifnull(concat(usr.employee_code,' - ',usr.employee_name),'Administrator') as user_name, " + \
                "sum(if((com.frequency_id = 5 and com.duration_type_id = 2),if(ch.due_date >= now() and usr.user_id = ch.completed_by and ch.current_status = 0,1,0), " + \
                "if(date(ch.due_date) >= date(now()) and usr.user_id = ch.completed_by and ch.current_status = 0,1,0))) as to_complete, " + \
                "sum(if((com.frequency_id = 5 and com.duration_type_id = 2),if(ch.due_date >= now() and usr.user_id = ch.concurred_by and ch.current_status = 1,1,0), " + \
                "if(date(ch.due_date) >= date(now()) and usr.user_id = ch.concurred_by and ch.current_status = 1,1,0))) as to_concur, " + \
                "sum(if((com.frequency_id = 5 and com.duration_type_id = 2),if(ch.due_date >= now() and usr.user_id = ch.approved_by and ch.current_status = 2,1,0), " + \
                "if(date(ch.due_date) >= date(now()) and usr.user_id = ch.approved_by and ch.current_status = 2,1,0))) as to_approver " + \
                "from tbl_compliance_history as ch " + \
                "inner join tbl_users as usr on (usr.user_id = ch.completed_by OR usr.user_id = ch.concurred_by OR usr.user_id = ch.approved_by) " + \
                "inner join tbl_compliances as com on ch.compliance_id = com.compliance_id " + \
                "left join (Select uu.unit_id,ud.domain_id from tbl_user_units as uu " + \
                "inner join tbl_user_domains as ud on uu.user_id = ud.user_id " + \
                "where uu.user_id = %s and ud.domain_id = %s) as uud on ch.unit_id = uud.unit_id and com.domain_id = uud.domain_id " + \
                "where ch.legal_entity_id = %s and com.domain_id = %s " + \
                "and IF(%s > 3,ch.unit_id = uud.unit_id and com.domain_id = uud.domain_id,1) group by usr.user_id"

        rows = db.select_all(query, [session_user, domain_id, legal_entity_id, domain_id, session_category])

        inprogress_unit = []
        for r in rows:
            user_id = int(r["user_id"])
            user_name = r["user_name"]
            to_complete = int(r["to_complete"])
            to_concur = int(r["to_concur"])
            to_approve = int(r["to_approver"])
            result = clientcore.GetInprogressUserWiseCountSuccess(
                user_id, user_name, to_complete, to_concur, to_approve)
            inprogress_unit.append(result)
        return inprogress_unit

    def completed_unit_wise_count(legal_entity_id, domain_id):
        query = "select ch.unit_id, concat(unt.unit_code,' - ',unt.unit_name) as unitname, " + \
                "sum(if((com.frequency_id = 5 and com.duration_type_id = 2),if(ch.due_date >= now() and ch.current_status = 3,1,0), " + \
                "if(date(ch.due_date) >= date(now()) and ch.current_status = 3,1,0))) as complied_count, " + \
                "sum(if((com.frequency_id = 5 and com.duration_type_id = 2),if(ch.due_date < now() and ch.current_status = 3,1,0), " + \
                "if(date(ch.due_date) < date(now()) and ch.current_status = 3,1,0))) as delayed_count " + \
                "from tbl_compliance_history as ch " + \
                "inner join tbl_units as unt on ch.unit_id = unt.unit_id " + \
                "inner join tbl_compliances as com on ch.compliance_id = com.compliance_id " + \
                "left join (Select uu.unit_id,ud.domain_id from tbl_user_units as uu " + \
                "inner join tbl_user_domains as ud on uu.user_id = ud.user_id " + \
                "where uu.user_id = %s and ud.domain_id = %s) as uud on ch.unit_id = uud.unit_id and com.domain_id = uud.domain_id " + \
                "where ch.legal_entity_id = %s and com.domain_id = %s " + \
                "and IF(%s > 3,ch.unit_id = uud.unit_id and com.domain_id = uud.domain_id,1) group by ch.unit_id; "
        rows = db.select_all(query, [session_user, domain_id, legal_entity_id, domain_id, session_category])

        inprogress_unit = []
        for r in rows:
            unit_id = int(r["unit_id"])
            unit = r["unitname"]
            complied_count = int(r["complied_count"])
            delayed_count = int(r["delayed_count"])
            result = clientcore.GetCompletedUnitWiseCountSuccess(
                unit_id, unit, complied_count, delayed_count)
            inprogress_unit.append(result)
        return inprogress_unit

    def completed_user_wise_count(legal_entity_id, domain_id):
        query = "select usr.user_id,ifnull(concat(usr.employee_code,' - ',usr.employee_name),'Administrator') as user_name, " + \
                "sum(if((com.frequency_id = 5 and com.duration_type_id = 2),if(ch.due_date >= now() and usr.user_id = ch.completed_by and ch.current_status = 3,1,0), " + \
                "if(date(ch.due_date) >= date(now()) and usr.user_id = ch.completed_by and ch.current_status = 3,1,0))) as complied_count, " + \
                "sum(if((com.frequency_id = 5 and com.duration_type_id = 2),if(ch.due_date < now() and usr.user_id = ch.completed_by and ch.current_status = 3,1,0), " + \
                "if(date(ch.due_date) < date(now()) and usr.user_id = ch.completed_by and ch.current_status = 3,1,0))) as delayed_count " + \
                "from tbl_compliance_history as ch " + \
                "inner join tbl_users as usr on usr.user_id = ch.completed_by  " + \
                "inner join tbl_compliances as com on ch.compliance_id = com.compliance_id " + \
                "left join (Select uu.unit_id,ud.domain_id from tbl_user_units as uu " + \
                "inner join tbl_user_domains as ud on uu.user_id = ud.user_id " + \
                "where uu.user_id = %s and ud.domain_id = %s) as uud on ch.unit_id = uud.unit_id and com.domain_id = uud.domain_id " + \
                "where ch.legal_entity_id = %s and com.domain_id = %s " + \
                "and IF(%s > 3,ch.unit_id = uud.unit_id and com.domain_id = uud.domain_id,1) group by usr.user_id"
        rows = db.select_all(query, [session_user, domain_id, legal_entity_id, domain_id, session_category])

        inprogress_unit = []
        for r in rows:
            user_id = int(r["user_id"])
            user_name = r["user_name"]
            complied_count = int(r["complied_count"])
            delayed_count = int(r["delayed_count"])
            result = clientcore.GetCompletedUserWiseCountSuccess(
                user_id, user_name, complied_count, delayed_count)
            inprogress_unit.append(result)
        return inprogress_unit

    def overdue_unit_wise_count(legal_entity_id, domain_id):
        query = "select ch.unit_id,concat(unt.unit_code,' - ',unt.unit_name) as unitname, " + \
                "sum(if((com.frequency_id = 5 and com.duration_type_id = 2),if(ch.due_date < now() and ch.current_status = 0,1,0), " + \
                "if(date(ch.due_date) < date(now()) and ch.current_status = 0,1,0))) as to_complete, " + \
                "sum(if((com.frequency_id = 5 and com.duration_type_id = 2),if(ch.due_date < now() and ch.current_status = 1,1,0), " + \
                "if(date(ch.due_date) < date(now()) and ch.current_status = 1,1,0))) as to_concur, " + \
                "sum(if((com.frequency_id = 5 and com.duration_type_id = 2),if(ch.due_date < now() and ch.current_status = 2,1,0), " + \
                "if(date(ch.due_date) < date(now()) and ch.current_status = 2,1,0))) as to_approver " + \
                "from tbl_compliance_history as ch " + \
                "inner join tbl_units as unt on ch.unit_id = unt.unit_id " + \
                "inner join tbl_compliances as com on ch.compliance_id = com.compliance_id " + \
                "left join (Select uu.unit_id,ud.domain_id from tbl_user_units as uu " + \
                "inner join tbl_user_domains as ud on uu.user_id = ud.user_id " + \
                "where uu.user_id = %s and ud.domain_id = %s) as uud on ch.unit_id = uud.unit_id and com.domain_id = uud.domain_id " + \
                "where ch.legal_entity_id = %s and com.domain_id = %s " + \
                "and IF(%s > 3,ch.unit_id = uud.unit_id and com.domain_id = uud.domain_id,1) group by ch.unit_id"

        rows = db.select_all(query, [session_user, domain_id, legal_entity_id, domain_id, session_category])

        inprogress_unit = []
        for r in rows:
            unit_id = int(r["unit_id"])
            unit = r["unitname"]
            to_complete = int(r["to_complete"])
            to_concur = int(r["to_concur"])
            to_approve = int(r["to_approver"])
            result = clientcore.GetOverdueUnitWiseCountSuccess(
                unit_id, unit, to_complete, to_concur, to_approve)
            inprogress_unit.append(result)
        return inprogress_unit

    def overdue_user_wise_count(legal_entity_id, domain_id):
        query = "select usr.user_id,ifnull(concat(usr.employee_code,' - ',usr.employee_name),'Administrator') as user_name, " + \
                "sum(if((com.frequency_id = 5 and com.duration_type_id = 2),if(ch.due_date < now() and usr.user_id = ch.completed_by and ch.current_status = 0,1,0), " + \
                "if(date(ch.due_date) < date(now()) and usr.user_id = ch.completed_by and ch.current_status = 0,1,0))) as to_complete, " + \
                "sum(if((com.frequency_id = 5 and com.duration_type_id = 2),if(ch.due_date < now() and usr.user_id = ch.concurred_by and ch.current_status = 1,1,0), " + \
                "if(date(ch.due_date) < date(now()) and usr.user_id = ch.concurred_by and ch.current_status = 1,1,0))) as to_concur, " + \
                "sum(if((com.frequency_id = 5 and com.duration_type_id = 2),if(ch.due_date < now() and usr.user_id = ch.approved_by and ch.current_status = 2,1,0), " + \
                "if(date(ch.due_date) < date(now()) and usr.user_id = ch.approved_by and ch.current_status = 2,1,0))) as to_approver " + \
                "from tbl_compliance_history as ch " + \
                "inner join tbl_users as usr on (usr.user_id = ch.completed_by OR usr.user_id = ch.concurred_by OR usr.user_id = ch.approved_by) " + \
                "inner join tbl_compliances as com on ch.compliance_id = com.compliance_id " + \
                "left join (Select uu.unit_id,ud.domain_id from tbl_user_units as uu " + \
                "inner join tbl_user_domains as ud on uu.user_id = ud.user_id " + \
                "where uu.user_id = %s and ud.domain_id = %s) as uud on ch.unit_id = uud.unit_id and com.domain_id = uud.domain_id " + \
                "where ch.legal_entity_id = %s and com.domain_id = %s " + \
                "and IF(%s > 3,ch.unit_id = uud.unit_id and com.domain_id = uud.domain_id,1) group by usr.user_id; "

        rows = db.select_all(query, [session_user, domain_id, legal_entity_id, domain_id, session_category])

        inprogress_unit = []
        for r in rows:
            unit_id = int(r["user_id"])
            unit = r["user_name"]
            to_complete = int(r["to_complete"])
            to_concur = int(r["to_concur"])
            to_approve = int(r["to_approver"])
            result = clientcore.GetOverdueUserWiseCountSuccess(
                unit_id, unit, to_complete, to_concur, to_approve)
            inprogress_unit.append(result)
        return inprogress_unit

    compliances = []
    for r in domain_wise_count:
        inprogress_count = int(r["inprogress_count"])
        completed_count = int(r["completed_count"])
        overdue_count = int(r["overdue_count"])
        inprogress_unit_wise = inprogress_unit_wise_count(
            legal_entity_id, domain_id)
        inprogress_user_wise = inprogress_user_wise_count(
            legal_entity_id, domain_id)
        completed_unit_wise = completed_unit_wise_count(
            legal_entity_id, domain_id)
        completed_user_wise = completed_user_wise_count(
            legal_entity_id, domain_id)
        overdue_unit_wise = overdue_unit_wise_count(legal_entity_id, domain_id)
        overdue_user_wise = overdue_user_wise_count(legal_entity_id, domain_id)
        compliance = clientcore.GetLEWiseScoreCardSuccess(
            inprogress_count, completed_count, overdue_count, inprogress_unit_wise, inprogress_user_wise,
            completed_unit_wise, completed_user_wise, overdue_unit_wise, overdue_user_wise
        )
        compliances.append(compliance)
    return compliances
# Legal Entity Wise Score Card End


# Work Flow Score Card Start
def report_work_flow_score_card(
    db, country_id, legal_entity_id, domain_id, session_user, session_category
):
    query = "select ifnull(sum(if((com.frequency_id = 5 and com.duration_type_id = 2),if(ch.due_date >= now() and usr.user_id = ch.completed_by and ch.current_status = 0,1,0), " + \
            "if(date(ch.due_date) >= date(now()) and usr.user_id = ch.completed_by and ch.current_status = 0,1,0))),0) as inprogress_assignee, " + \
            "ifnull(sum(if((com.frequency_id = 5 and com.duration_type_id = 2),if(ch.due_date >= now() and usr.user_id = ch.concurred_by and ch.current_status = 1,1,0), " + \
            "if(date(ch.due_date) >= date(now()) and usr.user_id = ch.concurred_by and ch.current_status = 1,1,0))),0) as inprogress_concur, " + \
            "ifnull(sum(if((com.frequency_id = 5 and com.duration_type_id = 2),if(ch.due_date >= now() and usr.user_id = ch.approved_by and ch.current_status = 2,1,0), " + \
            "if(date(ch.due_date) >= date(now()) and usr.user_id = ch.approved_by and ch.current_status = 2,1,0))),0) as inprogress_approver, " + \
            "ifnull(sum(if(usr.user_id = ch.completed_by and ch.current_status = 1,1,0)),0) as completed_assignee, " + \
            "ifnull(sum(if(usr.user_id = ch.concurred_by and ch.current_status = 2,1,0)),0) as completed_concur, " + \
            "ifnull(sum(if(usr.user_id = ch.approved_by and ch.current_status = 3,1,0)),0) as completed_approver, " + \
            "ifnull(sum(if((com.frequency_id = 5 and com.duration_type_id = 2),if(ch.due_date < now() and usr.user_id = ch.completed_by and ch.current_status = 0,1,0), " + \
            "if(date(ch.due_date) < date(now()) and usr.user_id = ch.completed_by and ch.current_status = 0,1,0))),0) as overdue_assignee, " + \
            "ifnull(sum(if((com.frequency_id = 5 and com.duration_type_id = 2),if(ch.due_date < now() and usr.user_id = ch.concurred_by and ch.current_status = 1,1,0), " + \
            "if(date(ch.due_date) < date(now()) and usr.user_id = ch.concurred_by and ch.current_status = 1,1,0))),0) as overdue_concur, " + \
            "ifnull(sum(if((com.frequency_id = 5 and com.duration_type_id = 2),if(ch.due_date < now() and usr.user_id = ch.approved_by and ch.current_status = 2,1,0), " + \
            "if(date(ch.due_date) < date(now()) and usr.user_id = ch.approved_by and ch.current_status = 2,1,0))),0) as overdue_approver " + \
            "from tbl_compliance_history as ch " + \
            "inner join tbl_units as unt on ch.unit_id = unt.unit_id " + \
            "inner join tbl_users as usr on (usr.user_id = ch.completed_by OR usr.user_id = ch.concurred_by OR usr.user_id = ch.approved_by) " + \
            "inner join tbl_compliances as com on ch.compliance_id = com.compliance_id " + \
            "left join (Select uu.unit_id,ud.domain_id from tbl_user_units as uu " + \
            "inner join tbl_user_domains as ud on uu.user_id = ud.user_id " + \
            "where uu.user_id = %s and ud.domain_id = %s) as uud on ch.unit_id = uud.unit_id and com.domain_id = uud.domain_id " + \
            "where ch.legal_entity_id = %s and com.domain_id = %s " + \
            "and IF(%s > 3,ch.unit_id = uud.unit_id and com.domain_id = uud.domain_id,1)"

    domain_wise_count = db.select_all(query, [session_user, domain_id, legal_entity_id, domain_id, session_category])

    def completed_task_count(country_id, legal_entity_id, domain_id, session_user):
        query = "select ch.unit_id,concat(unit_code,' - ',unit_name) as unit_name, " + \
                "sum(if(usr.user_id = ch.completed_by and ch.current_status = 1,1,0)) as you_submitted, " + \
                "sum(if(usr.user_id = ch.concurred_by and ch.current_status = 2,1,0)) as you_concurred, " + \
                "sum(if(usr.user_id = ch.approved_by and ch.current_status = 3,1,0)) as you_approved " + \
                "from tbl_compliance_history as ch " + \
                "inner join tbl_units as unt on ch.unit_id = unt.unit_id " + \
                "inner join tbl_users as usr on (usr.user_id = ch.completed_by OR usr.user_id = ch.concurred_by OR usr.user_id = ch.approved_by) " + \
                "inner join tbl_compliances as com on ch.compliance_id = com.compliance_id " + \
                "left join (Select uu.unit_id,ud.domain_id from tbl_user_units as uu " + \
                "inner join tbl_user_domains as ud on uu.user_id = ud.user_id " + \
                "where uu.user_id = %s and ud.domain_id = %s) as uud on ch.unit_id = uud.unit_id and com.domain_id = uud.domain_id " + \
                "where ch.legal_entity_id = %s and com.domain_id = %s " + \
                "and IF(%s > 3,ch.unit_id = uud.unit_id and com.domain_id = uud.domain_id,1) group by ch.unit_id; "

        rows = db.select_all(query, [session_user, domain_id, legal_entity_id, domain_id, session_category])
        array = []
        for r in rows:
            unit_id = int(r["unit_id"])
            unit = r["unit_name"]
            c_assignee = int(r["you_submitted"])
            c_concur = int(r["you_concurred"])
            c_approver = int(r["you_approved"])
            result = clientcore.GetCompletedTaskCountSuccess(
                unit_id, unit, c_assignee, c_concur, c_approver)
            array.append(result)
        return array

    def inprogress_within_duedate_task_count(country_id, legal_entity_id, domain_id, session_user):
        query = "select ch.unit_id,concat(unit_code,' - ',unit_name) as unit_name, " + \
                "sum(if((com.frequency_id = 5 and com.duration_type_id = 2),if(ch.due_date >= now() and usr.user_id = ch.completed_by and ch.current_status = 0,1,0), " + \
                "if(date(ch.due_date) >= date(now()) and usr.user_id = ch.completed_by and ch.current_status = 0,1,0))) as yet_submit, " + \
                "sum(if((com.frequency_id = 5 and com.duration_type_id = 2),if(ch.due_date >= now() and usr.user_id = ch.concurred_by and ch.current_status = 1,1,0), " + \
                "if(date(ch.due_date) >= date(now()) and usr.user_id = ch.concurred_by and ch.current_status = 1,1,0))) as yet_concur, " + \
                "sum(if((com.frequency_id = 5 and com.duration_type_id = 2),if(ch.due_date >= now() and usr.user_id = ch.approved_by and ch.current_status = 2,1,0), " + \
                "if(date(ch.due_date) >= date(now()) and usr.user_id = ch.approved_by and ch.current_status = 2,1,0))) as yet_approve " + \
                "from tbl_compliance_history as ch " + \
                "inner join tbl_units as unt on ch.unit_id = unt.unit_id " + \
                "inner join tbl_users as usr on (usr.user_id = ch.completed_by OR usr.user_id = ch.concurred_by OR usr.user_id = ch.approved_by) " + \
                "inner join tbl_compliances as com on ch.compliance_id = com.compliance_id " + \
                "left join (Select uu.unit_id,ud.domain_id from tbl_user_units as uu " + \
                "inner join tbl_user_domains as ud on uu.user_id = ud.user_id " + \
                "where uu.user_id = %s and ud.domain_id = %s) as uud on ch.unit_id = uud.unit_id and com.domain_id = uud.domain_id " + \
                "where ch.legal_entity_id = %s and com.domain_id = %s " + \
                "and IF(%s > 3,ch.unit_id = uud.unit_id and com.domain_id = uud.domain_id,1) group by ch.unit_id "

        rows = db.select_all(query, [session_user, domain_id, legal_entity_id, domain_id, session_category])

        inprogress_unit = []
        for r in rows:
            unit_id = int(r["unit_id"])
            unit = r["unit_name"]
            inp_assignee = int(r["yet_submit"])
            inp_concur = int(r["yet_concur"])
            inp_approver = int(r["yet_approve"])
            result = clientcore.GetInprogressWithinDuedateTaskCountSuccess(
                unit_id, unit, inp_assignee, inp_concur, inp_approver)
            inprogress_unit.append(result)
        return inprogress_unit

    def over_due_task_count(country_id, legal_entity_id, domain_id, session_user):
        query = "select ch.unit_id,concat(unit_code,' - ',unit_name) as unit_name, " + \
                "sum(if((com.frequency_id = 5 and com.duration_type_id = 2),if(ch.due_date < now() and usr.user_id = ch.completed_by and ch.current_status = 0,1,0), " + \
                "if(date(ch.due_date) < date(now()) and usr.user_id = ch.completed_by and ch.current_status = 0,1,0))) as yet_submit, " + \
                "sum(if((com.frequency_id = 5 and com.duration_type_id = 2),if(ch.due_date < now() and usr.user_id = ch.concurred_by and ch.current_status = 1,1,0), " + \
                "if(date(ch.due_date) < date(now()) and usr.user_id = ch.concurred_by and ch.current_status = 1,1,0))) as yet_concur, " + \
                "sum(if((com.frequency_id = 5 and com.duration_type_id = 2),if(ch.due_date < now() and usr.user_id = ch.approved_by and ch.current_status = 2,1,0), " + \
                "if(date(ch.due_date) < date(now()) and usr.user_id = ch.approved_by and ch.current_status = 2,1,0))) as yet_approve " + \
                "from tbl_compliance_history as ch " + \
                "inner join tbl_units as unt on ch.unit_id = unt.unit_id " + \
                "inner join tbl_users as usr on (usr.user_id = ch.completed_by OR usr.user_id = ch.concurred_by OR usr.user_id = ch.approved_by) " + \
                "inner join tbl_compliances as com on ch.compliance_id = com.compliance_id " + \
                "left join (Select uu.unit_id,ud.domain_id from tbl_user_units as uu " + \
                "inner join tbl_user_domains as ud on uu.user_id = ud.user_id " + \
                "where uu.user_id = %s and ud.domain_id = %s) as uud on ch.unit_id = uud.unit_id and com.domain_id = uud.domain_id " + \
                "where ch.legal_entity_id = %s and com.domain_id = %s " + \
                "and IF(%s > 3,ch.unit_id = uud.unit_id and com.domain_id = uud.domain_id,1) group by ch.unit_id "
        rows = db.select_all(query, [session_user, domain_id, legal_entity_id, domain_id, session_category])

        inprogress_unit = []
        for r in rows:
            unit_id = int(r["unit_id"])
            unit = r["unit_name"]
            ov_assignee = int(r["yet_submit"])
            ov_concur = int(r["yet_concur"])
            ov_approver = int(r["yet_approve"])
            result = clientcore.GetOverDueTaskCountSuccess(unit_id, unit, ov_assignee, ov_concur, ov_approver)
            inprogress_unit.append(result)
        return inprogress_unit

    compliances = []
    for r in domain_wise_count:
        c_assignee = int(r["completed_assignee"])
        c_concur = int(r["completed_concur"])
        c_approver = int(r["completed_approver"])
        inp_assignee = int(r["inprogress_assignee"])
        inp_concur = int(r["inprogress_concur"])
        inp_approver = int(r["inprogress_approver"])
        ov_assignee = int(r["overdue_assignee"])
        ov_concur = int(r["overdue_concur"])
        ov_approver = int(r["overdue_approver"])
        completed_task_count = completed_task_count(
            country_id, legal_entity_id, domain_id, session_user)
        inprogress_within_duedate_task_count = inprogress_within_duedate_task_count(
            country_id, legal_entity_id, domain_id, session_user)
        over_due_task_count = over_due_task_count(
            country_id, legal_entity_id, domain_id, session_user)
        compliance = clientcore.GetWorkFlowScoreCardSuccess(
            c_assignee, c_concur, c_approver, inp_assignee, inp_concur, inp_approver, ov_assignee, ov_concur, ov_approver,
            completed_task_count, inprogress_within_duedate_task_count, over_due_task_count
        )
        compliances.append(compliance)
    return compliances
# Work Flow Score Card End

