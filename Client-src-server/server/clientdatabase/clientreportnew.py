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
    calculate_ageing, get_admin_id, get_user_unit_ids, is_admin
)
CLIENT_DOCS_DOWNLOAD_URL = "/client/client_documents"
FORMAT_DOWNLOAD_URL = "/client/compliance_format"
ROOT_PATH = os.path.join(os.path.split(__file__)[0], "..", "..")
CLIENT_LOGO_PATH = "/clientlogo"

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
    from_date = string_to_datetime(from_date)
    to_date = string_to_datetime(to_date)
    query = "select t01.num, rc.reassign_history_id, com.domain_id, rc.unit_id,rc.compliance_id, " + \
        "com.compliance_task, SUBSTRING_INDEX(com.statutory_mapping,'>>',1) as act_name, " + \
        "concat((select concat(employee_code,' - ',employee_name) from tbl_users where user_id = rc.old_assignee),' / ', " + \
        "(select concat(employee_code,' - ',employee_name) from tbl_users where user_id = rc.old_concurrer),' / ', " + \
        "(select concat(employee_code,' - ',employee_name) from tbl_users where user_id = rc.old_approver)) as old_user, " + \
        "concat((select concat(employee_code,' - ',employee_name) from tbl_users where user_id = rc.assignee),' / ', " + \
        "(select concat(employee_code,' - ',employee_name) from tbl_users where user_id = rc.concurrer),' / ', " + \
        "(select concat(employee_code,' - ',employee_name) from tbl_users where user_id = rc.approver)) as new_user, " + \
        "rc.assigned_on,rc.remarks,ch.due_date, " + \
        "(select concat(unit_code,' - ',unit_name,' - ',address) from tbl_units where unit_id = rc.unit_id) as unit " + \
            "from  tbl_reassigned_compliances_history as rc " + \
            "inner join tbl_compliances as com on rc.compliance_id = com.compliance_id " + \
            "inner join (select compliance_id,unit_id,num from  " + \
        "(select compliance_id,unit_id,@rownum := @rownum + 1 AS num  " + \
        "from (select distinct t1.compliance_id,unit_id from tbl_reassigned_compliances_history as t1 " + \
        "inner join tbl_compliances as t2 on t1.compliance_id = t2.compliance_id) t, " + \
        "(SELECT @rownum := 0) r) as cnt " + \
        "where  cnt.num between %s and %s) as t01 on rc.compliance_id = t01.compliance_id and rc.unit_id = t01.unit_id " + \
            "left join tbl_compliance_history as ch on rc.compliance_id = ch.compliance_id " + \
            "where  com.domain_id = %s and rc.unit_id = %s and  " + \
        "IF(%s IS NOT NULL,com.statutory_mapping like %s,1) " + \
        "and IF(%s IS NOT NULL, rc.compliance_id = %s,1) " + \
        "and (IF(%s IS NOT NULL,rc.old_assignee = 1, 1) " + \
        "or IF(%s IS NOT NULL,rc.old_concurrer = 1, 1) " + \
        "or IF(%s IS NOT NULL,rc.old_approver = 1, 1)  " + \
        "or IF(%s IS NOT NULL,rc.assignee = 1, 1) " + \
        "or IF(%s IS NOT NULL,rc.concurrer = 1, 1) " + \
        "or IF(%s IS NOT NULL,rc.approver = 1, 1)) " + \
        "and rc.assigned_on >= %s and rc.assigned_on <= %s " + \
            "order by t01.num asc,rc.reassign_history_id desc"

    rows = db.select_all(query, [
        f_count, t_count, domain_id, unit_id, act, act, compliance_id,
        compliance_id, usr_id, usr_id, usr_id, usr_id,
        usr_id, usr_id, from_date, to_date
    ])
    # print rows

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
    from_date = string_to_datetime(from_date)
    to_date = string_to_datetime(to_date)

    query = "select count(Distinct rc.compliance_id) as total_count from  tbl_reassigned_compliances_history as rc " + \
            "inner join tbl_compliances as com on rc.compliance_id = com.compliance_id " + \
            "left join tbl_compliance_history as ch on rc.compliance_id = ch.compliance_id " + \
            "where  com.domain_id = %s and rc.unit_id = %s and  " + \
        "IF(%s IS NOT NULL,com.statutory_mapping like %s,1) " + \
        "and IF(%s IS NOT NULL, rc.compliance_id = %s,1) " + \
        "and (IF(%s IS NOT NULL,rc.old_assignee = 1, 1) " + \
        "or IF(%s IS NOT NULL,rc.old_concurrer = 1, 1) " + \
        "or IF(%s IS NOT NULL,rc.old_approver = 1, 1) " + \
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
    from_date = string_to_datetime(from_date)
    to_date = string_to_datetime(to_date)
    query = "select acl.compliance_activity_id,ch.compliance_history_id, ch.legal_entity_id,ch.unit_id, " + \
            "(select concat(unit_code,' - ',unit_name,' - ',address) from tbl_units where unit_id = ch.unit_id) as unit,ch.compliance_id, " + \
            "concat(com.document_name,' - ',com.compliance_task) as compliance_name, " + \
            "(select frequency from tbl_compliance_frequency where frequency_id = com.frequency_id) as frequency_name, " + \
            "SUBSTRING_INDEX(com.statutory_mapping,'>>',1) as act_name,  acl.activity_on, ch.due_date,ch.completion_date, " + \
            "(CASE WHEN (ch.due_date < ch.approved_on and ch.approve_status = 3) THEN 'Delayed Compliance' " + \
            "WHEN (ch.due_date >= ch.approved_on and ch.approve_status = 3) THEN 'Complied' " + \
            "WHEN (ch.due_date >= ch.approved_on and ch.approve_status < 3) THEN 'In Progress' " + \
            "WHEN (ch.due_date < ch.approved_on and ch.approve_status < 3) THEN 'Not Complied' " + \
            "WHEN (ch.approved_on IS NULL and ch.approve_status IS NULL) THEN 'In Progress' " + \
            "ELSE 'In Progress' END) as compliance_task_status, " + \
            "(CASE WHEN %s = ch.completed_by THEN ch.documents ELSE '-' END) as uploaded_document, " + \
            "ifnull(acl.action, 'Pending')  as activity_status, " + \
            "ifnull((select employee_name from tbl_users where user_id = acl.activity_by), (select employee_name from tbl_users where user_id = ch.completed_by)) as user_name " + \
            "from tbl_compliance_history as ch " + \
            "inner join tbl_compliances as com on ch.compliance_id = com.compliance_id " + \
            "left join tbl_compliance_activity_log as acl on ch.compliance_history_id = acl.compliance_history_id " + \
            "inner join tbl_assign_compliances as ac on ch.compliance_id = ac.compliance_id and ch.unit_id = ac.unit_id " + \
            "inner join (select compliance_id,unit_id,num from  " + \
            "(select compliance_id,unit_id,@rownum := @rownum + 1 AS num  " + \
            "from (select distinct t1.compliance_id,t1.unit_id from tbl_compliance_history as t1 " + \
            "left join tbl_compliance_activity_log as t2 on t1.compliance_history_id = t2.compliance_history_id " + \
            "order by t1.unit_id,t1.compliance_id, t1.compliance_history_id asc,t2.compliance_activity_id desc) t, " + \
            "(SELECT @rownum := 0) r) as cnt " + \
            "where cnt.num between %s and %s order by cnt.unit_id, cnt.compliance_id) as t01  " + \
            "on ch.compliance_id = t01.compliance_id and ch.unit_id = t01.unit_id " + \
            "where com.country_id = %s and ch.legal_entity_id = %s " + \
            "and com.domain_id = %s " + \
            "and IF(%s IS NOT NULL, ch.unit_id = %s,1) " + \
            "and IF(%s IS NOT NULL,SUBSTRING_INDEX(com.statutory_mapping,'>>',1) = %s,1) " + \
            "and IF(%s IS NOT NULL, ch.compliance_id = %s,1) " + \
            "and IF(%s > 0, com.frequency_id = %s,1) " + \
            "and (CASE %s WHEN 1 THEN ac.assignee = %s " + \
            "WHEN 2 THEN ac.concurrence_person = %s WHEN 3 THEN ac.approval_person = %s " + \
            "ELSE 1 END) " + \
            "and ch.due_date >= %s and ch.due_date <= %s " + \
            "and IF(%s <> 'All',(CASE WHEN (ch.due_date < ch.approved_on and ch.approve_status = 3) THEN 'Delayed Compliance' " + \
            "WHEN (ch.due_date >= ch.approved_on and ch.approve_status = 3) THEN 'Complied' " + \
            "WHEN (ch.due_date >= ch.approved_on and ch.approve_status < 3) THEN 'In Progress' " + \
            "WHEN (ch.due_date < ch.approved_on and ch.approve_status < 3) THEN 'Not Complied' " + \
            "WHEN (ch.approved_on IS NULL and ch.approve_status IS NULL) THEN 'In Progress' " + \
            "ELSE 'In Progress' END) = %s,1) " + \
            "order by t01.num, acl.compliance_history_id asc, acl.compliance_activity_id desc"

    # print query;

    rows = db.select_all(query, [
        usr_id, f_count, t_count,
        country_id, legal_entity_id, domain_id, unit_id, unit_id, act, act, compliance_id, compliance_id,
        frequency_id, frequency_id, user_type_id, usr_id, usr_id, usr_id, from_date, to_date, status_name, status_name
    ])
    # print rows

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
        act_name = r["act_name"].replace('["', '')
        activity_on = datetime_to_string(r["activity_on"])
        due_date = datetime_to_string(r["due_date"])
        completion_date = datetime_to_string(r["completion_date"])
        task_status = r["compliance_task_status"]
        uploaded_document = r["uploaded_document"]
        activity_status = r["activity_status"]
        user_name = r["user_name"]

        compliance = clientcore.GetStatusReportConsolidatedSuccess(
            compliance_activity_id, compliance_history_id, legal_entity_id, unit_id, unit, compliance_id, compliance_name, frequency_name,
            act_name, activity_on, due_date, completion_date, task_status, uploaded_document, activity_status, user_name
        )
        compliances.append(compliance)
    return compliances


def report_status_report_consolidated_total(
    db, country_id, legal_entity_id, domain_id, unit_id,
    act, compliance_id, frequency_id, user_type_id, status_name, usr_id, from_date, to_date, session_user
):
    from_date = string_to_datetime(from_date)
    to_date = string_to_datetime(to_date)
    query = "select count(Distinct ch.compliance_history_id) as total_count " + \
            "from tbl_compliance_history as ch " + \
            "inner join tbl_compliances as com on ch.compliance_id = com.compliance_id " + \
            "left join tbl_compliance_activity_log as acl on ch.compliance_history_id = acl.compliance_history_id " + \
            "inner join tbl_assign_compliances as ac on ch.compliance_id = ac.compliance_id and ch.unit_id = ac.unit_id " + \
            "where com.country_id = %s and ch.legal_entity_id = %s " + \
            "and com.domain_id = %s " + \
            "and IF(%s IS NOT NULL, ch.unit_id = %s,1) " + \
            "and IF(%s IS NOT NULL,SUBSTRING_INDEX(com.statutory_mapping,'>>',1) = %s,1) " + \
            "and IF(%s IS NOT NULL, ch.compliance_id = %s,1) " + \
            "and IF(%s > 0, com.frequency_id = %s,1) " + \
            "and (CASE %s WHEN 1 THEN ac.assignee = %s " + \
            "WHEN 2 THEN ac.concurrence_person = %s WHEN 3 THEN ac.approval_person = %s " + \
            "ELSE 1 END) " + \
            "and ch.due_date >= %s and ch.due_date <= %s " + \
            "and IF(%s <> 'All',(CASE WHEN (ch.due_date < ch.approved_on and ch.approve_status = 3) THEN 'Delayed Compliance' " + \
            "WHEN (ch.due_date >= ch.approved_on and ch.approve_status = 3) THEN 'Complied' " + \
            "WHEN (ch.due_date >= ch.approved_on and ch.approve_status < 3) THEN 'In Progress' " + \
            "WHEN (ch.due_date < ch.approved_on and ch.approve_status < 3) THEN 'Not Complied' " + \
            "WHEN (ch.approved_on IS NULL and ch.approve_status IS NULL) THEN 'In Progress' " + \
            "ELSE 'In Progress' END) = %s,1) "

    rows = db.select_one(query, [
        country_id, legal_entity_id, domain_id, unit_id, unit_id, act, act, compliance_id, compliance_id,
        frequency_id, frequency_id, user_type_id, usr_id, usr_id, usr_id, from_date, to_date, status_name, status_name
    ])
    return int(rows["total_count"])
# Status Report Consolidated Report End


# Statutory Settings Unit Wise Start
def report_statutory_settings_unit_Wise(
    db, country_id, bg_id, legal_entity_id, domain_id, unit_id,
        div_id, cat_id, act, compliance_id, frequency_id, status_name, session_user, f_count, t_count
):
    query = "select t01.num,cc.compliance_id, cf.frequency, " + \
            "com.compliance_task,SUBSTRING_INDEX(com.statutory_mapping,'>>',1) as act_name, " + \
            "(CASE cc.compliance_opted_status WHEN 1 THEN  " + \
            "(CASE WHEN ac.compliance_id IS NULL and ac.unit_id IS NULL THEN 'Un-Assigned' ELSE 'Assigned' END) ELSE 'Not Opted' END) as task_status, " + \
            "com.document_name,(select concat('Mr. ',employee_name) from tbl_users where user_id = aclh.activity_by) as user_name,aclh.due_date, " + \
            "concat(unt.unit_code,' - ',unt.unit_name,' - ',unt.address) as unit, unt.unit_id " + \
            "from tbl_client_compliances as cc " + \
            "inner join tbl_compliances as com on cc.compliance_id = com.compliance_id " + \
            "inner join tbl_legal_entities as lg on cc.legal_entity_id = lg.legal_entity_id " + \
            "inner join tbl_units as unt on cc.unit_id = unt.unit_id " + \
            "inner join tbl_compliance_frequency as cf on com.frequency_id = cf.frequency_id " + \
            "left join tbl_assign_compliances ac on cc.unit_id = ac.unit_id and cc.compliance_id = ac.compliance_id " + \
            "left join (select ch.compliance_id,ch.unit_id,acl.activity_by,ch.due_date from tbl_compliance_history as ch  " + \
            "inner join tbl_compliance_activity_log as acl on ch.compliance_history_id = acl.compliance_history_id and ch.completed_by = acl.activity_by) as aclh " + \
            "on cc.compliance_id = aclh.compliance_id and cc.unit_id = aclh.unit_id " + \
            "inner join (select compliance_id,unit_id,num from  " + \
        "(select compliance_id,unit_id,@rownum := @rownum + 1 AS num  " + \
        "from (select distinct t1.compliance_id,t1.unit_id from tbl_client_compliances as t1 " + \
        "order by t1.unit_id,t1.compliance_id) t, " + \
        "(SELECT @rownum := 0) r) as cnt " + \
        "where cnt.num between %s and %s order by cnt.unit_id, cnt.compliance_id) as t01 " + \
        "on cc.compliance_id = t01.compliance_id and cc.unit_id = t01.unit_id " + \
            "WHERE com.country_id = %s  " + \
            "and IF(%s IS NOT NULL,lg.business_group_id = %s,1) " + \
            "and cc.legal_entity_id = %s and cc.domain_id = %s " + \
            "and IF(%s IS NOT NULL,unt.division_id = %s,1) " + \
            "and IF(%s IS NOT NULL,unt.category_id = %s,1) " + \
            "and IF(%s IS NOT NULL,unt.unit_id = %s,1) " + \
            "and IF(%s IS NOT NULL,SUBSTRING_INDEX(com.statutory_mapping,'>>',1) = %s,1) " + \
            "and IF(%s > 0,cf.frequency_id = %s,1) " + \
            "and IF(%s IS NOT NULL,com.compliance_id = %s,1) " + \
            "and IF(%s <> 'All', (CASE cc.compliance_opted_status WHEN 1 THEN  " + \
            "(CASE WHEN ac.compliance_id IS NULL and ac.unit_id IS NULL THEN 'Un-Assigned' ELSE 'Assigned' END) ELSE 'Not Opted' END) = %s,1) "

    # print query;

    rows = db.select_all(query, [
        f_count, t_count, country_id, bg_id, bg_id, legal_entity_id, domain_id, div_id,
        div_id, cat_id, cat_id, unit_id, unit_id, act, act, frequency_id, frequency_id,
        compliance_id, compliance_id, status_name, status_name
    ])
    # print rows

    return return_statutory_settings_unit_Wise(
        db, rows, country_id, legal_entity_id
    )


def return_statutory_settings_unit_Wise(db, result, country_id, legal_entity_id):
    compliances = []
    for r in result:
        compliance_id = r["compliance_id"]
        frequency = r["frequency"]
        compliance_task = r["compliance_task"]
        act_name = r["act_name"]
        task_status = r["task_status"]
        document_name = r["document_name"]
        user_name = r["user_name"]
        due_date = datetime_to_string(r["due_date"])
        unit = r["unit"]
        unit_id = r["unit_id"]
        compliance = clientcore.GetStatutorySettingsUnitWiseSuccess(
            compliance_id, frequency, compliance_task, act_name, task_status, document_name, user_name, due_date, unit, unit_id
        )
        compliances.append(compliance)
    return compliances


def report_statutory_settings_unit_Wise_total(
    db, country_id, bg_id, legal_entity_id, domain_id, unit_id, div_id, cat_id,
        act, compliance_id, frequency_id, status_name, session_user
):
    query = "select count(distinct cc.compliance_id) as total_count from tbl_client_compliances as cc " + \
            "inner join tbl_compliances as com on cc.compliance_id = com.compliance_id " + \
            "inner join tbl_legal_entities as lg on cc.legal_entity_id = lg.legal_entity_id " + \
            "inner join tbl_units as unt on cc.unit_id = unt.unit_id " + \
            "inner join tbl_compliance_frequency as cf on com.frequency_id = cf.frequency_id " + \
            "left join tbl_assign_compliances ac on cc.unit_id = ac.unit_id and cc.compliance_id = ac.compliance_id " + \
            "left join (select ch.compliance_id,ch.unit_id,acl.activity_by,ch.due_date from tbl_compliance_history as ch  " + \
            "inner join tbl_compliance_activity_log as acl on ch.compliance_history_id = acl.compliance_history_id and ch.completed_by = acl.activity_by) as aclh " + \
            "on cc.compliance_id = aclh.compliance_id and cc.unit_id = aclh.unit_id " + \
            "WHERE com.country_id = %s  " + \
            "and IF(%s IS NOT NULL,lg.business_group_id = %s,1) " + \
            "and cc.legal_entity_id = %s and cc.domain_id = %s " + \
            "and IF(%s IS NOT NULL,unt.division_id = %s,1) " + \
            "and IF(%s IS NOT NULL,unt.category_id = %s,1) " + \
            "and IF(%s IS NOT NULL,unt.unit_id = %s,1) " + \
            "and IF(%s IS NOT NULL,SUBSTRING_INDEX(com.statutory_mapping,'>>',1) = %s,1) " + \
            "and IF(%s > 0,cf.frequency_id = %s,1) " + \
            "and IF(%s IS NOT NULL,com.compliance_id = %s,1) " + \
            "and IF(%s <> 'All', (CASE cc.compliance_opted_status WHEN 1 THEN  " + \
            "(CASE WHEN ac.compliance_id IS NULL and ac.unit_id IS NULL THEN 'Un-Assigned' ELSE 'Assigned' END) ELSE 'Not Opted' END) = %s,1)"

    rows = db.select_one(query, [
        country_id, bg_id, bg_id, legal_entity_id, domain_id, div_id,
        div_id, cat_id, cat_id, unit_id, unit_id, act, act, frequency_id, frequency_id,
        compliance_id, compliance_id, status_name, status_name
    ])
    return int(rows["total_count"])
# Statutory Settings Unit Wise End

# Domain Score Card Start


def report_domain_score_card(
    db, country_id, bg_id, legal_entity_id, domain_id, div_id, cat_id, session_user
):
    query = "select cc.domain_id,(select domain_name from tbl_domains where domain_id = cc.domain_id) as domain_name, " + \
            "IFNULL(sum(IF(IFNULL(cc.compliance_opted_status,0) = 0,1,0)), 0) as not_opted_count, " + \
            "count(IFNULL(ac.compliance_id,0)) as unassigned_count, " + \
            "IFNULL(csu.assigned_count,0) as assigned_count " + \
            "from tbl_client_compliances as cc " + \
            "inner join tbl_units as unt on cc.unit_id = unt.unit_id " + \
            "left join (select domain_id,sum(complied_count + delayed_count + inprogress_count + overdue_count) as assigned_count,unit_id " + \
            "from tbl_compliance_status_chart_unitwise group by domain_id,unit_id) as csu on cc.domain_id = csu.domain_id and cc.unit_id = csu.unit_id " + \
            "left join tbl_assign_compliances as ac on cc.compliance_id = ac.compliance_id and cc.unit_id = ac.unit_id and cc.domain_id = ac.domain_id " + \
            "where unt.country_id = %s " + \
            "and IF(%s IS NOT NULL,unt.business_group_id = %s,1) " + \
            "and cc.legal_entity_id = %s " + \
            "and IF(%s IS NOT NULL,unt.division_id = %s,1) " + \
            "and IF(%s IS NOT NULL,unt.category_id = %s,1) " + \
            "and IF(%s IS NOT NULL,cc.domain_id = %s,1) " + \
            "group by cc.domain_id,csu.unit_id,csu.domain_id "

    domain_wise_count = db.select_all(
        query, [country_id, bg_id, bg_id, legal_entity_id, div_id, div_id, cat_id, cat_id, domain_id, domain_id])
    # print domain_wise_count

    def domain_wise_unit_count(country_id, bg_id, legal_entity_id, div_id, cat_id, domain_id):
        query_new = "select cc.unit_id,(select domain_name from tbl_domains where domain_id = cc.domain_id) as domain_name, " + \
            "concat(unt.unit_code,' - ',unt.unit_name) as units, " + \
            "IFNULL(sum(IF(IFNULL(cc.compliance_opted_status,0) = 0,1,0)), 0) as not_opted_count, " + \
            "IFNULL(count(IFNULL(ac.compliance_id,0)), 0) as unassigned_count, " + \
            "IFNULL(csu.complied_count, 0) as complied_count, IFNULL(csu.delayed_count, 0) as delayed_count,  " + \
            "IFNULL(csu.inprogress_count, 0) as inprogress_count, IFNULL(csu.overdue_count, 0) as overdue_count " + \
            "from tbl_client_compliances as cc " + \
            "inner join tbl_units as unt on cc.unit_id = unt.unit_id " + \
            "left join (select unit_id,domain_id,sum(complied_count) as complied_count,sum(delayed_count) as delayed_count, " + \
            "sum(inprogress_count) as inprogress_count,sum(overdue_count) as overdue_count  " + \
            "from tbl_compliance_status_chart_unitwise group by unit_id,domain_id) as csu on cc.unit_id = csu.unit_id and cc.domain_id = csu.domain_id " + \
            "left join tbl_assign_compliances as ac on cc.compliance_id = ac.compliance_id and cc.unit_id = ac.unit_id and cc.domain_id = ac.domain_id " + \
            "where unt.country_id = %s " + \
            "and IF(%s IS NOT NULL,unt.business_group_id = %s,1) " + \
            "and cc.legal_entity_id = %s " + \
            "and IF(%s IS NOT NULL,unt.division_id = %s,1) " + \
            "and IF(%s IS NOT NULL,unt.category_id = %s,1) " + \
            "and IF(%s IS NOT NULL,cc.domain_id = %s,1) " + \
            "group by cc.domain_id,cc.unit_id "

        rows = db.select_all(query_new, [
                             country_id, bg_id, bg_id, legal_entity_id, div_id, div_id, cat_id, cat_id, domain_id, domain_id])
        # print rows
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
    db, country_id, legal_entity_id, domain_id, session_user
):
    query = "select ifnull(sum(inprogress_count),0) as inprogress_count, ifnull((SUM(complied_count) +sum(delayed_count)),0) as completed_count, " + \
            "ifnull(sum(overdue_count),0) as overdue_count " + \
            "from tbl_compliance_status_chart_unitwise " + \
            "where country_id = %s " + \
            "and legal_entity_id = %s " + \
            "and domain_id = %s "

    domain_wise_count = db.select_all(
        query, [country_id, legal_entity_id, domain_id])
    # print domain_wise_count

    def inprogress_unit_wise_count(legal_entity_id, domain_id):
        query = "select ch.unit_id,concat(unt.unit_code,' - ',unt.unit_name) as unitname, " + \
                "sum(IF(com.frequency_id = 5,IF(ch.due_date >= now() and ch.completed_on IS NULL ,1,0), " + \
                "IF(date(ch.due_date) >= curdate() and ch.completed_on IS NULL ,1,0))) as to_complete, " + \
                "sum(IF(com.frequency_id = 5,IF(ch.due_date >= now() and ch.completed_on IS NOT NULL and IFNULL(ch.concurrence_status,0) <> 1 ,1,0), " + \
                "IF(date(ch.due_date) >= curdate() and ch.completed_on IS NOT NULL and IFNULL(ch.concurrence_status,0) <> 1,1,0))) as to_concur, " + \
                "sum(IF(com.frequency_id = 5,IF(ch.due_date >= now() and ch.completed_on IS NOT NULL and ch.concurrence_status IS NOT NULL and IFNULL(ch.approve_status,0) <> 1,1,0), " + \
                "IF(date(ch.due_date) >= curdate() and ch.completed_on IS NOT NULL and ch.concurrence_status IS NOT NULL and IFNULL(ch.approve_status,0) <> 1,1,0))) as to_approve " + \
                "from tbl_compliance_history as ch " + \
                "inner join tbl_compliances as com on ch.compliance_id = com.compliance_id " + \
                "inner join tbl_units as unt on ch.unit_id = unt.unit_id " + \
                "where ch.legal_entity_id = %s and com.domain_id = %s " + \
                "group by ch.unit_id"
        rows = db.select_all(query, [legal_entity_id, domain_id])
        # print rows
        inprogress_unit = []
        for r in rows:
            unit_id = int(r["unit_id"])
            unit = r["unitname"]
            to_complete = int(r["to_complete"])
            to_concur = int(r["to_concur"])
            to_approve = int(r["to_approve"])
            result = clientcore.GetInprogressUnitWiseCountSuccess(
                unit_id, unit, to_complete, to_concur, to_approve)
            inprogress_unit.append(result)
        return inprogress_unit

    def inprogress_user_wise_count(legal_entity_id, domain_id):
        query = "SELECT t01.user_id,t01.user_name,t01.to_complete,t01.to_concur,t01.to_approve FROM ( " + \
                "select usr.user_id,concat(employee_code,' - ',employee_name) as user_name, " + \
                "sum(IF(com.frequency_id = 5,IF(ch.due_date >= now() and ch.completed_on IS NULL ,1,0) and ch.completed_by = usr.user_id, " + \
                "IF(date(ch.due_date) >= curdate() and ch.completed_on IS NULL and ch.completed_by = usr.user_id ,1,0))) as to_complete, " + \
                "sum(IF(com.frequency_id = 5,IF(ch.due_date >= now() and ch.completed_on IS NOT NULL and IFNULL(ch.concurrence_status,0) <> 1 and ch.concurred_by = usr.user_id ,1,0), " + \
                "IF(date(ch.due_date) >= curdate() and ch.completed_on IS NOT NULL and IFNULL(ch.concurrence_status,0) <> 1 and ch.concurred_by = usr.user_id,1,0))) as to_concur, " + \
                "sum(IF(com.frequency_id = 5,IF(ch.due_date >= now() and ch.completed_on IS NOT NULL and ch.concurrence_status IS NOT NULL and IFNULL(ch.approve_status,0) <> 1 and ch.approved_by = usr.user_id,1,0), " + \
                "IF(date(ch.due_date) >= curdate() and ch.completed_on IS NOT NULL and ch.concurrence_status IS NOT NULL and IFNULL(ch.approve_status,0) <> 1 and ch.approved_by = usr.user_id,1,0))) as to_approve " + \
                "from tbl_compliance_history as ch " + \
                "inner join tbl_compliances as com on ch.compliance_id = com.compliance_id " + \
                "inner join tbl_users as usr on usr.user_id = ch.completed_by OR usr.user_id = ch.concurred_by OR usr.user_id = ch.approved_by " + \
                "where ch.legal_entity_id = %s and com.domain_id = %s " + \
                "group by usr.user_id) as t01 "
        rows = db.select_all(query, [legal_entity_id, domain_id])
        # print rows
        inprogress_unit = []
        for r in rows:
            user_id = int(r["user_id"])
            user_name = r["user_name"]
            to_complete = int(r["to_complete"])
            to_concur = int(r["to_concur"])
            to_approve = int(r["to_approve"])
            result = clientcore.GetInprogressUserWiseCountSuccess(
                user_id, user_name, to_complete, to_concur, to_approve)
            inprogress_unit.append(result)
        return inprogress_unit

    def completed_unit_wise_count(legal_entity_id, domain_id):
        query = "select ch.unit_id,concat(unt.unit_code,' - ',unt.unit_name) as unitname, " + \
                "sum(IF(com.frequency_id = 5,IF(ch.due_date >= ch.completion_date and ifnull(ch.approve_status,0) = 1,1,0), " + \
                "IF(date(ch.due_date) >= date(ch.completion_date) and ifnull(ch.approve_status,0) = 1,1,0))) as complied_count, " + \
                "sum(IF(com.frequency_id = 5,IF(ch.due_date < ch.completion_date and ifnull(ch.approve_status,0) = 1,1,0), " + \
                "IF(date(ch.due_date) < date(ch.completion_date) and ifnull(ch.approve_status,0) = 1,1,0))) as delayed_count " + \
                "from tbl_compliance_history as ch " + \
                "inner join tbl_compliances as com on ch.compliance_id = com.compliance_id " + \
                "inner join tbl_units as unt on ch.unit_id = unt.unit_id " + \
                "where ch.legal_entity_id = %s and com.domain_id = %s " + \
                "group by ch.unit_id "
        rows = db.select_all(query, [legal_entity_id, domain_id])
        # print rows
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
        query = "select usr.user_id,concat(employee_code,' - ',employee_name) as user_name, " + \
                "sum(IF(com.frequency_id = 5,IF(ch.due_date >= ch.completion_date and ifnull(ch.approve_status,0) = 1 ,1,0), " + \
                "IF(date(ch.due_date) >= date(ch.completion_date) and ifnull(ch.approve_status,0) = 1,1,0))) as complied_count, " + \
                "sum(IF(com.frequency_id = 5,IF(ch.due_date < ch.completion_date and ifnull(ch.approve_status,0) = 1,1,0), " + \
                "IF(date(ch.due_date) < date(ch.completion_date) and ifnull(ch.approve_status,0) = 1,1,0))) as delayed_count " + \
                "from tbl_compliance_history as ch " + \
                "inner join tbl_compliances as com on ch.compliance_id = com.compliance_id " + \
                "inner join tbl_users as usr on usr.user_id = ch.completed_by OR usr.user_id = ch.concurred_by OR usr.user_id = ch.approved_by " + \
                "where ch.legal_entity_id = %s and com.domain_id = %s " + \
                "group by usr.user_id "
        rows = db.select_all(query, [legal_entity_id, domain_id])
        # print rows
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
                "sum(IF(com.frequency_id = 5,IF(ch.due_date < now() and IFNULL(ch.approve_status,0) <> 1,1,0), " + \
                "IF(date(ch.due_date) < curdate() and IFNULL(ch.approve_status,0) <> 1,1,0))) as overdue_count " + \
                "from tbl_compliance_history as ch " + \
                "inner join tbl_compliances as com on ch.compliance_id = com.compliance_id " + \
                "inner join tbl_units as unt on ch.unit_id = unt.unit_id " + \
                "where ch.legal_entity_id = %s and com.domain_id = %s " + \
                "group by ch.unit_id "
        rows = db.select_all(query, [legal_entity_id, domain_id])
        # print rows
        inprogress_unit = []
        for r in rows:
            unit_id = int(r["unit_id"])
            unit = r["unitname"]
            overdue_count = int(r["overdue_count"])
            result = clientcore.GetOverdueUnitWiseCountSuccess(
                unit_id, unit, overdue_count)
            inprogress_unit.append(result)
        return inprogress_unit

    def overdue_user_wise_count(legal_entity_id, domain_id):
        query = "select usr.user_id,concat(employee_code,' - ',employee_name) as user_name, " + \
                "sum(IF(com.frequency_id = 5,IF(ch.due_date < now() and IFNULL(ch.approve_status,0) <> 1,1,0), " + \
                "IF(date(ch.due_date) < curdate() and IFNULL(ch.approve_status,0) <> 1,1,0))) as overdue_count " + \
                "from tbl_compliance_history as ch " + \
                "inner join tbl_compliances as com on ch.compliance_id = com.compliance_id " + \
                "inner join tbl_users as usr on usr.user_id = ch.completed_by OR usr.user_id = ch.concurred_by OR usr.user_id = ch.approved_by " + \
                "where ch.legal_entity_id = %s and com.domain_id = %s " + \
                "group by usr.user_id"
        rows = db.select_all(query, [legal_entity_id, domain_id])
        # print rows
        inprogress_unit = []
        for r in rows:
            unit_id = int(r["user_id"])
            unit = r["user_name"]
            overdue_count = int(r["overdue_count"])
            result = clientcore.GetOverdueUserWiseCountSuccess(
                unit_id, unit, overdue_count)
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
    db, country_id, legal_entity_id, domain_id, session_user
):
    # query = "select SUM(IF(ch.completed_on IS NOT NULL and ch.completed_by = acl.activity_by and ch.completed_by = %s,1,0)) as c_assignee, " + \
    #         "SUM(IF(ch.completed_on IS NOT NULL and ch.concurred_on IS NOT NULL and ch.concurred_by = acl.activity_by and ch.concurred_by = %s,1,0)) as c_concur, " + \
    #         "SUM(IF(ch.completed_on IS NOT NULL and ch.concurred_on IS NOT NULL and IFNULL(ch.approve_status,0) = 1 and ch.approved_by = acl.activity_by and ch.approved_by = %s,1,0)) as c_approver, " + \
    #         "SUM(IF(com.frequency_id = 5,(IF(ch.due_date >= now() and ch.completed_on IS NULL and ch.completed_by = acl.activity_by and ch.completed_by = %s,1,0)), " + \
    #         "(IF(date(ch.due_date) >= curdate() and ch.completed_on IS NULL and ch.completed_by = acl.activity_by and ch.completed_by = %s,1,0)))) as inp_assignee, " + \
    #         "SUM(IF(com.frequency_id = 5,(IF(ch.due_date >= now() and ch.completed_on IS NOT NULL and IFNULL(ch.concurrence_status,0) <> 1 and ch.concurred_by = acl.activity_by  and ch.concurred_by = %s,1,0)), " + \
    #         "(IF(date(ch.due_date) >= curdate() and ch.completed_on IS NOT NULL and IFNULL(ch.concurrence_status,0) <> 1 and ch.concurred_by = acl.activity_by  and ch.concurred_by = %s,1,0)))) as inp_concur, " + \
    #         "SUM(IF(com.frequency_id = 5,(IF(ch.due_date >= now() and ch.completed_on IS NOT NULL and ch.concurred_on IS NOT NULL and IFNULL(ch.approve_status,0) <> 1 and ch.approved_by = acl.activity_by and ch.approved_by = %s,1,0)), " + \
    #         "(IF(date(ch.due_date) >= curdate() and ch.completed_on IS NOT NULL and ch.concurred_on IS NOT NULL and IFNULL(ch.approve_status,0) <> 1 and ch.approved_by = acl.activity_by and ch.approved_by = %s,1,0)))) as inp_approver, " + \
    #         "SUM(IF(com.frequency_id = 5,(IF(ch.due_date < now() and ch.completed_on IS NULL and ch.completed_by = acl.activity_by and ch.completed_by = %s,1,0)), " + \
    #         "(IF(date(ch.due_date) < curdate() and ch.completed_on IS NULL and ch.completed_by = acl.activity_by and ch.completed_by = %s,1,0)))) as ov_assignee, " + \
    #         "SUM(IF(com.frequency_id = 5,(IF(ch.due_date < now() and ch.completed_on IS NOT NULL and IFNULL(ch.concurrence_status,0) <> 1 and ch.concurred_by = acl.activity_by and ch.concurred_by = %s,1,0)), " + \
    #         "(IF(date(ch.due_date) < curdate() and ch.completed_on IS NOT NULL and IFNULL(ch.concurrence_status,0) <> 1 and ch.concurred_by = acl.activity_by and ch.concurred_by = %s,1,0)))) as ov_concur, " + \
    #         "SUM(IF(com.frequency_id = 5,(IF(ch.due_date < now() and ch.completed_on IS NOT NULL and ch.concurred_on IS NOT NULL and IFNULL(ch.approve_status,0) <> 1 and ch.approved_by = acl.activity_by and ch.approved_by = %s,1,0)), " + \
    #         "(IF(date(ch.due_date) < curdate() and ch.completed_on IS NOT NULL and ch.concurred_on IS NOT NULL and IFNULL(ch.approve_status,0) <> 1 and ch.approved_by = acl.activity_by and ch.approved_by = %s,1,0)))) as ov_approver " + \
    #         "from tbl_compliance_history as ch inner join tbl_compliance_activity_log as acl on ch.compliance_history_id = acl.compliance_history_id " + \
    #         "inner join tbl_compliances as com on ch.compliance_id = com.compliance_id where com.country_id = %s and ch.legal_entity_id = %s and com.domain_id = %s "

    query = "select ifnull(SUM(IF(ch.completed_on IS NOT NULL and ch.completed_by = acl.activity_by and ch.completed_by = %s,1,0)),0) as c_assignee, " + \
            "ifnull(SUM(IF(ch.completed_on IS NOT NULL and ch.concurred_on IS NOT NULL and ch.concurred_by = acl.activity_by and ch.concurred_by = %s,1,0)),0) as c_concur, " + \
            "ifnull(SUM(IF(ch.completed_on IS NOT NULL and ch.concurred_on IS NOT NULL and IFNULL(ch.approve_status,0) = 1 and ch.approved_by = acl.activity_by and ch.approved_by = %s,1,0)),0) as c_approver, " + \
            "ifnull(SUM(IF(com.frequency_id = 5,(IF(ch.due_date >= now() and ch.completed_on IS NULL and ch.completed_by = acl.activity_by and ch.completed_by = %s,1,0)), " + \
            "(IF(date(ch.due_date) >= curdate() and ch.completed_on IS NULL and ch.completed_by = acl.activity_by and ch.completed_by = %s,1,0)))),0) as inp_assignee, " + \
            "ifnull(SUM(IF(com.frequency_id = 5,(IF(ch.due_date >= now() and ch.completed_on IS NOT NULL and IFNULL(ch.concurrence_status,0) <> 1 and ch.concurred_by = acl.activity_by  and ch.concurred_by = %s,1,0)), " + \
            "(IF(date(ch.due_date) >= curdate() and ch.completed_on IS NOT NULL and IFNULL(ch.concurrence_status,0) <> 1 and ch.concurred_by = acl.activity_by  and ch.concurred_by = %s,1,0)))),0) as inp_concur, " + \
            "ifnull(SUM(IF(com.frequency_id = 5,(IF(ch.due_date >= now() and ch.completed_on IS NOT NULL and ch.concurred_on IS NOT NULL and IFNULL(ch.approve_status,0) <> 1 and ch.approved_by = acl.activity_by and ch.approved_by = %s,1,0)), " + \
            "(IF(date(ch.due_date) >= curdate() and ch.completed_on IS NOT NULL and ch.concurred_on IS NOT NULL and IFNULL(ch.approve_status,0) <> 1 and ch.approved_by = acl.activity_by and ch.approved_by = %s,1,0)))),0) as inp_approver, " + \
            "ifnull(SUM(IF(com.frequency_id = 5,(IF(ch.due_date < now() and ch.completed_on IS NULL and ch.completed_by = acl.activity_by and ch.completed_by = %s,1,0)), " + \
            "(IF(date(ch.due_date) < curdate() and ch.completed_on IS NULL and ch.completed_by = acl.activity_by and ch.completed_by = %s,1,0)))),0) as ov_assignee, " + \
            "ifnull(SUM(IF(com.frequency_id = 5,(IF(ch.due_date < now() and ch.completed_on IS NOT NULL and IFNULL(ch.concurrence_status,0) <> 1 and ch.concurred_by = acl.activity_by and ch.concurred_by = %s,1,0)), " + \
            "(IF(date(ch.due_date) < curdate() and ch.completed_on IS NOT NULL and IFNULL(ch.concurrence_status,0) <> 1 and ch.concurred_by = acl.activity_by and ch.concurred_by = %s,1,0)))),0) as ov_concur, " + \
            "ifnull(SUM(IF(com.frequency_id = 5,(IF(ch.due_date < now() and ch.completed_on IS NOT NULL and ch.concurred_on IS NOT NULL and IFNULL(ch.approve_status,0) <> 1 and ch.approved_by = acl.activity_by and ch.approved_by = %s,1,0)), " + \
            "(IF(date(ch.due_date) < curdate() and ch.completed_on IS NOT NULL and ch.concurred_on IS NOT NULL and IFNULL(ch.approve_status,0) <> 1 and ch.approved_by = acl.activity_by and ch.approved_by = %s,1,0)))),0) as ov_approver " + \
            "from tbl_compliance_history as ch inner join tbl_compliance_activity_log as acl on ch.compliance_history_id = acl.compliance_history_id " + \
            "inner join tbl_compliances as com on ch.compliance_id = com.compliance_id where com.country_id = %s and ch.legal_entity_id = %s and com.domain_id = %s "
    # print query

    domain_wise_count = db.select_all(query, [session_user, session_user, session_user, session_user, session_user, session_user, session_user, session_user,
                                              session_user, session_user, session_user, session_user, session_user, session_user, session_user, country_id, legal_entity_id, domain_id])
    # print domain_wise_count

    def completed_task_count(country_id, legal_entity_id, domain_id, session_user):
        query = "select ch.unit_id,(select concat(unit_code,' - ',unit_name) from tbl_units where unit_id = ch.unit_id) as unitname, " + \
                "SUM(IF(ch.completed_on IS NOT NULL and ch.completed_by = acl.activity_by and ch.completed_by = %s,1,0)) as c_assignee, " + \
                "SUM(IF(ch.completed_on IS NOT NULL and ch.concurred_on IS NOT NULL and ch.concurred_by = acl.activity_by and ch.concurred_by = %s,1,0)) as c_concur, " + \
                "SUM(IF(ch.completed_on IS NOT NULL and ch.concurred_on IS NOT NULL and IFNULL(ch.approve_status,0) = 1 and ch.approved_by = acl.activity_by and ch.approved_by = %s,1,0)) as c_approver " + \
                "from tbl_compliance_history as ch inner join tbl_compliance_activity_log as acl on ch.compliance_history_id = acl.compliance_history_id " + \
                "inner join tbl_compliances as com on ch.compliance_id = com.compliance_id " + \
                "where com.country_id = %s and ch.legal_entity_id = %s and com.domain_id = %s group by ch.unit_id; "
        rows = db.select_all(query, [
                             session_user, session_user, session_user, country_id, legal_entity_id, domain_id])
        array = []
        for r in rows:
            unit_id = int(r["unit_id"])
            unit = r["unitname"]
            c_assignee = int(r["c_assignee"])
            c_concur = int(r["c_concur"])
            c_approver = int(r["c_approver"])
            result = clientcore.GetCompletedTaskCountSuccess(
                unit_id, unit, c_assignee, c_concur, c_approver)
            array.append(result)
        return array

    def inprogress_within_duedate_task_count(country_id, legal_entity_id, domain_id, session_user):
        query = "select ch.unit_id,(select concat(unit_code,' - ',unit_name) from tbl_units where unit_id = ch.unit_id) as unitname, " + \
                "SUM(IF(com.frequency_id = 5,(IF(ch.due_date >= now() and ch.completed_on IS NULL and ch.completed_by = acl.activity_by and ch.completed_by = %s,1,0)), " + \
                "(IF(date(ch.due_date) >= curdate() and ch.completed_on IS NULL and ch.completed_by = acl.activity_by and ch.completed_by = %s,1,0)))) as inp_assignee, " + \
                "SUM(IF(com.frequency_id = 5,(IF(ch.due_date >= now() and ch.completed_on IS NOT NULL and IFNULL(ch.concurrence_status,0) <> 1 and ch.concurred_by = acl.activity_by  and ch.concurred_by = %s,1,0)), " + \
                "(IF(date(ch.due_date) >= curdate() and ch.completed_on IS NOT NULL and IFNULL(ch.concurrence_status,0) <> 1 and ch.concurred_by = acl.activity_by  and ch.concurred_by = %s,1,0)))) as inp_concur, " + \
                "SUM(IF(com.frequency_id = 5,(IF(ch.due_date >= now() and ch.completed_on IS NOT NULL and ch.concurred_on IS NOT NULL and IFNULL(ch.approve_status,0) <> 1 and ch.approved_by = acl.activity_by and ch.approved_by = %s,1,0)), " + \
                "(IF(date(ch.due_date) >= curdate() and ch.completed_on IS NOT NULL and ch.concurred_on IS NOT NULL and IFNULL(ch.approve_status,0) <> 1 and ch.approved_by = acl.activity_by and ch.approved_by = %s,1,0)))) as inp_approver " + \
                "from tbl_compliance_history as ch inner join tbl_compliance_activity_log as acl on ch.compliance_history_id = acl.compliance_history_id " + \
                "inner join tbl_compliances as com on ch.compliance_id = com.compliance_id " + \
                "where com.country_id = %s and ch.legal_entity_id = %s and com.domain_id = %s group by ch.unit_id; "
        rows = db.select_all(query, [session_user, session_user, session_user, session_user,
                                     session_user, session_user, country_id, legal_entity_id, domain_id])
        # print rows
        inprogress_unit = []
        for r in rows:
            unit_id = int(r["unit_id"])
            unit = r["unitname"]
            inp_assignee = int(r["inp_assignee"])
            inp_concur = int(r["inp_concur"])
            inp_approver = int(r["inp_approver"])
            result = clientcore.GetInprogressWithinDuedateTaskCountSuccess(
                unit_id, unit, inp_assignee, inp_concur, inp_approver)
            inprogress_unit.append(result)
        return inprogress_unit

    def over_due_task_count(country_id, legal_entity_id, domain_id, session_user):
        query = "select ch.unit_id,(select concat(unit_code,' - ',unit_name) from tbl_units where unit_id = ch.unit_id) as unitname, " + \
                "SUM(IF(com.frequency_id = 5,(IF(ch.due_date < now() and ch.completed_on IS NULL and ch.completed_by = acl.activity_by and ch.completed_by = %s,1,0)), " + \
                "(IF(date(ch.due_date) < curdate() and ch.completed_on IS NULL and ch.completed_by = acl.activity_by and ch.completed_by = %s,1,0)))) as ov_assignee, " + \
                "SUM(IF(com.frequency_id = 5,(IF(ch.due_date < now() and ch.completed_on IS NOT NULL and IFNULL(ch.concurrence_status,0) <> 1 and ch.concurred_by = acl.activity_by and ch.concurred_by = %s,1,0)), " + \
                "(IF(date(ch.due_date) < curdate() and ch.completed_on IS NOT NULL and IFNULL(ch.concurrence_status,0) <> 1 and ch.concurred_by = acl.activity_by and ch.concurred_by = %s,1,0)))) as ov_concur, " + \
                "SUM(IF(com.frequency_id = 5,(IF(ch.due_date < now() and ch.completed_on IS NOT NULL and ch.concurred_on IS NOT NULL and IFNULL(ch.approve_status,0) <> 1 and ch.approved_by = acl.activity_by and ch.approved_by = %s,1,0)), " + \
                "(IF(date(ch.due_date) < curdate() and ch.completed_on IS NOT NULL and ch.concurred_on IS NOT NULL and IFNULL(ch.approve_status,0) <> 1 and ch.approved_by = acl.activity_by and ch.approved_by = %s,1,0)))) as ov_approver " + \
                "from tbl_compliance_history as ch inner join tbl_compliance_activity_log as acl on ch.compliance_history_id = acl.compliance_history_id " + \
                "inner join tbl_compliances as com on ch.compliance_id = com.compliance_id where com.country_id = %s and ch.legal_entity_id = %s and com.domain_id = %s group by ch.unit_id; "
        rows = db.select_all(query, [session_user, session_user, session_user, session_user,
                                     session_user, session_user, country_id, legal_entity_id, domain_id])
        # print rows
        inprogress_unit = []
        for r in rows:
            unit_id = int(r["unit_id"])
            unit = r["unitname"]
            ov_assignee = int(r["ov_assignee"])
            ov_concur = int(r["ov_concur"])
            ov_approver = int(r["ov_approver"])
            result = clientcore.GetOverDueTaskCountSuccess(
                unit_id, unit, ov_assignee, ov_concur, ov_approver)
            inprogress_unit.append(result)
        return inprogress_unit

    compliances = []
    for r in domain_wise_count:
        c_assignee = int(r["c_assignee"])
        c_concur = int(r["c_concur"])
        c_approver = int(r["c_approver"])
        inp_assignee = int(r["inp_assignee"])
        inp_concur = int(r["inp_concur"])
        inp_approver = int(r["inp_approver"])
        ov_assignee = int(r["ov_assignee"])
        ov_concur = int(r["ov_concur"])
        ov_approver = int(r["ov_approver"])
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

