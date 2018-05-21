import os
import datetime
from server.clientdatabase.tables import *
from clientprotocol import (
    clientcore, clientreport, clientmasters
)
import json
# from server.constants import (CLIENT_LOGO_PATH)
from server.common import (
    datetime_to_string_time, string_to_datetime, datetime_to_string
)

CLIENT_DOCS_DOWNLOAD_URL = "/client/client_documents"
FORMAT_DOWNLOAD_URL = "/client/compliance_format"
ROOT_PATH = os.path.join(os.path.split(__file__)[0], "..", "..")
CLIENT_LOGO_PATH = "/clientlogo"

__all__ = [
    "get_domains_for_le",
    "get_units_for_le_domain",
    "get_acts_for_le_domain",
    "get_frequency_list",
    "get_compiance_status",
    "get_compliance_user_type",
    "get_compliance_user_list",
    "process_legal_entity_wise_report",
    "get_task_for_le_domain",
    "process_domain_wise_report",
    "process_unit_wise_report",
    "get_domains_for_sp_users",
    "get_units_for_sp_users",
    "get_acts_for_sp_users",
    "get_service_provider_user_list",
    "process_service_provider_wise_report",
    "get_le_users_list",
    "get_domains_for_le_users",
    "get_units_for_le_users",
    "get_acts_for_le_users",
    "process_user_wise_report",
    "get_divisions_for_unit_list",
    "get_categories_for_unit_list",
    "get_units_list",
    "get_domains_organization_for_le",
    "get_units_status",
    "process_unit_list_report",
    "process_statutory_notification_list_report",
    "process_audit_trail_report",
    "get_risk_compiance_status",
    "process_risk_report"
]


##########################################################################
# Objective: To get the domains list under selected legal entity
# Parameter: request object
# Result: list of domains under the leagl entity selection
##########################################################################
def get_domains_for_le(db, legal_entity_id):
    # print "le"
    # print legal_entity_id
    query = "select distinct(t1.domain_id), t1.legal_entity_id, t2.domain_name, t2.is_active " + \
            "from tbl_legal_entity_domains as t1 inner join tbl_domains as t2 " + \
            "on t2.domain_id = t1.domain_id where t1.legal_entity_id = %s " + \
            "order by t2.domain_name; "
    result = db.select_all(query, [legal_entity_id])
    # print "domains"
    # print result
    le_domains_list = []
    for row in result:
        le_domains_list.append(clientcore.Domain(
            row["domain_id"], row["domain_name"], row[
                "legal_entity_id"], bool(row["is_active"])
        )
        )
    return le_domains_list

##########################################################################
# Objective: To get the units under selected legal entity, domain and country
# Parameter: request object
# Result: list of units under the selected country, domain and legal entity
##########################################################################


def get_units_for_le_domain(db, country_id, legal_entity_id):
    query = "SELECT t1.unit_id, t1.unit_code, t1.unit_name, " + \
            "t2.domain_id, t1.country_id, t1.legal_entity_id " + \
            "FROM tbl_units as t1 inner join tbl_units_organizations" + \
            " as t2  on t2.unit_id = t1.unit_id " + \
            "where t1.legal_entity_id = %s and t1.country_id = %s " + \
            "group by t1.unit_id, t2.domain_id;"
    result = db.select_all(query, [legal_entity_id, country_id])
    # print "units"
    # print result
    le_units_list = []
    for row in result:
        le_units_list.append(clientreport.UnitLegalEntity(
            row["unit_id"], row["unit_code"], row[
                "unit_name"], row["domain_id"],
            row["country_id"], row["legal_entity_id"]
        )
        )
    return le_units_list

##########################################################################
# Objective: To get the acts under selected legal entity
# Parameter: request object
# Result: list of acts under the selected legal entity
##########################################################################


def get_acts_for_le_domain(db, legal_entity_id, country_id):
    query = "select t1.legal_entity_id, t1.domain_id, t1.unit_id, t2.compliance_id, " + \
            "t2.statutory_mapping, t2.frequency_id from " + \
            "tbl_client_compliances as t1 inner join tbl_compliances as t2 " + \
            "on t2.compliance_id = t1.compliance_id and t2.domain_id = t1.domain_id and " + \
            "t2.country_id = %s where t1.legal_entity_id = %s"
    result = db.select_all(query, [country_id, legal_entity_id])
    # print "acts"
    # print result
    # print len(result)
    le_act_list = []
    last = object()
    for row in result:
        stat_map = json.loads(row["statutory_mapping"])
        if stat_map[0].find(">>") >= 0:
            stat_map = stat_map[0].split(">>")[0]
        else:
            stat_map = str(stat_map)[3:-2]
        # print "mapped"
        # print stat_map
        if last != stat_map:
            last = stat_map
            le_act_list.append(clientreport.ActLegalEntity(
                row["legal_entity_id"], row["domain_id"], row["unit_id"],
                row["compliance_id"], statutory_mapping=stat_map
            )
            )
    # print len(le_act_list)
    return le_act_list

##########################################################################
# Objective: To get the compliance tasks under selected legal entity
# Parameter: request object
# Result: list of acts under the selected legal entity
##########################################################################


def get_task_for_le_domain(db, legal_entity_id):
    query = "select t1.legal_entity_id, t1.domain_id, t1.unit_id, t2.compliance_id, " + \
            "t2.statutory_mapping, t2.compliance_task, t2.frequency_id from " + \
            "tbl_client_compliances as t1 inner join tbl_compliances as t2 " + \
            "on t2.compliance_id = t1.compliance_id and t2.domain_id = t1.domain_id " + \
            "where t1.legal_entity_id = %s"
    result = db.select_all(query, [legal_entity_id])
    # print "task"
    # print result
    # print len(result)
    le_task_list = []
    last = object()
    for row in result:
        stat_map = json.loads(row["statutory_mapping"])
        if stat_map[0].find(">>") >= 0:
            stat_map = stat_map[0].split(">>")[0]
        else:
            stat_map = str(stat_map)[3:-2]
        if last != row["compliance_task"]:
            last = row["compliance_task"]
            le_task_list.append(clientreport.TaskLegalEntity(
                row["legal_entity_id"], row["domain_id"], row["unit_id"],
                row["compliance_id"], row[
                    "compliance_task"], row["frequency_id"],
                statutory_mapping=stat_map
            )
            )
    return le_task_list

##########################################################################
# Objective: To get the frequency from master
# Parameter: request object
# Result: list of frequencies
##########################################################################


def get_frequency_list(db):
    query = "select frequency_id, frequency as frequency_name from tbl_compliance_frequency"
    result = db.select_all(query, None)

    le_frequency_list = []
    for row in result:
        le_frequency_list.append(clientreport.ComplianceFrequency(
            row["frequency_id"], row["frequency_name"]
        )
        )
    return le_frequency_list

##########################################################################
# Objective: To get the compliance status
# Parameter: request object
# Result: list of compliance status
##########################################################################


def get_compiance_status(db):
    status = ("Complied", "Delayed Compliance", "Inprogress", "Not Complied")
    compliance_status = []
    i = 0
    for sts in status:
        c_task_status = clientreport.ComplianceTaskStatus(
            i, sts
        )
        compliance_status.append(c_task_status)
        i = i + 1
    return compliance_status

##########################################################################
# Objective: To get the compliance user type
# Parameter: request object
# Result: list of compliance user types
##########################################################################


def get_compliance_user_type(db):
    u_type = ("Assignee", "Concurrence", "Approval")
    user_types = []
    i = 0
    for u_t in u_type:
        c_user_type = clientreport.ComplianceUserType(
            i, u_t
        )
        user_types.append(c_user_type)
        i = i + 1
    return user_types

##########################################################################
# Objective: To get the compliance users under user types
# Parameter: request object
# Result: list of compliance users under user types
##########################################################################


def get_compliance_user_list(db, country_id, legal_entity_id):
    query = "select t1.legal_entity_id, t1.country_id, t1.domain_id, t1.unit_id, t1.compliance_id, " + \
            "t1.assignee, (select (case when employee_code is not null then concat(employee_code,'-',employee_name) " + \
            "else employee_name end) from tbl_users where user_id = t1.assignee) as assignee_name," + \
            "t1.concurrence_person, (select (case when employee_code is not null then " + \
            "concat(employee_code,'-',employee_name) else employee_name end) from tbl_users where " + \
            "user_id = t1.concurrence_person) as concurrer_name, t1.approval_person, " + \
            "(select (case when employee_code is not null then concat(employee_code,'-',employee_name) " + \
            "else employee_name end) from tbl_users where user_id = t1.approval_person) as approver_name " + \
            "from tbl_assign_compliances as t1 " + \
            "where t1.legal_entity_id = %s and t1.country_id = %s "

    result = db.select_all(query, [legal_entity_id, country_id])
    # print result
    le_user_type_users = []

    for row in result:
        le_user_type_users.append(clientreport.ComplianceUsers(
            row["legal_entity_id"], row["country_id"], row["domain_id"],
            row["unit_id"], row["compliance_id"], row[
                "assignee"], row["assignee_name"],
            row["concurrence_person"], row[
                "concurrer_name"], row["approval_person"],
            row["approver_name"]
        )
        )
    return le_user_type_users

##########################################################################
# Objective: To get the compliance list under filtered data
# Parameter: request object
# Result: list of compliance grouped by unit and act
##########################################################################


def process_legal_entity_wise_report(db, request):
    # u_type = ("Assignee", "Concurrence", "Approval")
    # status = ("Complied", "Delayed Compliance", "Inprogress", "Not Complied")
    where_clause = None
    count_clause = None
    condition_val = []
    select_qry = None
    from_clause = None
    u_type_val = 0
    country_id = request.country_id
    legal_entity_id = request.legal_entity_id
    domain_id = request.domain_id

    stat_map = request.statutory_mapping

    user_type = request.user_type
    if user_type == 'All':
        user_type = '%'
    if user_type == "Assignee":
        u_type_val = 1
    elif user_type == "Concurrence":
        u_type_val = 2
    elif user_type == "Approval":
        u_type_val = 3
    user_id = request.user_id
    if user_id == 0:
        user_id = None
    else:
        user_id = str(user_id)

    due_from = request.due_from_date
    due_to = request.due_to_date
    task_status = request.task_status
    unit_id = request.unit_id
    # if unit_id == 0:
    #     unit_id = None

    compliance_task = request.compliance_task
    if compliance_task is None:
        compliance_task = None

    frequency_id = request.frequency_id

    if due_from is not None and due_to is not None:
        due_from = string_to_datetime(due_from).date()
        due_to = string_to_datetime(due_to).date()

    query = "select t01.num, " + \
        "acl.compliance_activity_id,ch.compliance_history_id, ch.legal_entity_id,ch.unit_id, " + \
        "(select concat(unit_code,' - ',unit_name,' , ',address,' , ', postal_code) from tbl_units where unit_id = ch.unit_id) as unit_name,ch.compliance_id, " + \
        "concat(com.document_name,' - ',com.compliance_task) as compliance_name, " + \
        "(select frequency from tbl_compliance_frequency where frequency_id = com.frequency_id) as frequency_name, " + \
        "SUBSTRING_INDEX(substring(substring(com.statutory_mapping,3),1, char_length(com.statutory_mapping) -4), '>>', 1) as act_name, " + \
        "acl.activity_on, (select geography_name from tbl_units where unit_id = ch.unit_id) as geo_name, " + \
        "ch.due_date, ch.completion_date, ch.legal_entity_id, com.domain_id, ch.unit_id, com.country_id, " + \
        "(CASE WHEN (ch.due_date < ch.completion_date and ch.current_status = 3) THEN 'Delayed Compliance' " + \
        "WHEN (ch.due_date >= ch.completion_date and ch.approve_status <> 3 and ch.current_status = 3) THEN 'Complied' " + \
        "WHEN (ch.due_date >= ch.completion_date and ch.current_status < 3) THEN 'In Progress' " + \
        "WHEN (ch.due_date < ch.completion_date and ch.current_status < 3) THEN 'Not Complied' " + \
        "WHEN (ch.current_status = 3 and ch.approve_status = 3) THEN 'Not Complied' " + \
        "WHEN (ch.completion_date IS NULL and IFNULL(ch.current_status,0) = 0) THEN 'In Progress' " + \
        "ELSE 'In Progress' END) as task_status, com.compliance_task, " + \
        "(CASE WHEN ((acl.activity_by = ch.completed_by) or (acl.action is null and ch.current_status = 3)) " + \
        "THEN ch.documents ELSE '-' END) as documents, (case when acl.action is null and ch.current_status = 3 " + \
        "Then '-' when acl.action is null then 'Pending' else acl.action end) as activity_status, " + \
        "(CASE WHEN acl.activity_by = ch.approved_by THEN (select IFNULL(concat(employee_code,' - ',employee_name),'Administrator') from tbl_users where user_id = ac.approval_person) " + \
        "WHEN acl.activity_by = ch.concurred_by THEN (select concat(employee_code,' - ',employee_name) from tbl_users where user_id = ac.concurrence_person)  " + \
        "WHEN acl.activity_by = ch.completed_by THEN (select concat(employee_code,' - ',employee_name) from tbl_users where user_id = ac.assignee) ELSE  " + \
        "(select concat(employee_code,' - ',employee_name) from tbl_users where user_id = ac.assignee) END) as assignee_name, ch.start_date, " + \
        "(select logo from tbl_legal_entities where legal_entity_id = ch.legal_entity_id) as logo, " + \
        "(select logo_size from tbl_legal_entities where legal_entity_id = ch.legal_entity_id) as logo_size, " + \
        "(select count(compliance_history_id) from tbl_compliance_activity_log where " + \
        "compliance_history_id = ch.compliance_history_id) as history_count " + \
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
            "and IF(%s > 0, ac.unit_id = %s,1) " + \
            "and IF(%s IS NOT NULL,SUBSTRING_INDEX(substring(substring(com.statutory_mapping,3),1, char_length(com.statutory_mapping) -4), '>>', 1) = %s,1) " + \
            "and IF(%s IS NOT NULL, com.compliance_task like concat('%',%s,'%'),1) " + \
            "and IF(%s > 0, com.frequency_id = %s,1) " + \
            "and (CASE %s WHEN 1 THEN (ch.completed_by = acl.activity_by OR acl.activity_by IS NULL) " + \
            "WHEN 2 THEN ch.concurred_by = acl.activity_by WHEN 3 THEN ch.approved_by = acl.activity_by " + \
            "ELSE 1 END) " + \
            "and IF(%s IS NOT NULL, (ch.completed_by = %s OR ch.concurred_by = %s OR ch.approved_by = %s),1) " + \
            "and date(ch.due_date) >= %s and date(ch.due_date) <= %s " + \
            "and IF(%s <> 'All',(CASE WHEN (ch.due_date < ch.completion_date and ch.current_status = 3) THEN 'Delayed Compliance' " + \
            "WHEN (ch.due_date >= ch.completion_date and ch.approve_status <> 3 and ch.current_status = 3) THEN 'Complied' " + \
            "WHEN (ch.due_date >= ch.completion_date and ch.current_status < 3) THEN 'Inprogress' " + \
            "WHEN (ch.due_date < ch.completion_date and ch.current_status < 3) THEN 'Not Complied' " + \
            "WHEN (ch.current_status = 3 and ch.approve_status = 3) THEN 'Not Complied' " + \
            "WHEN (ch.completion_date IS NULL and IFNULL(ch.current_status,0) = 0) THEN 'Inprogress' " + \
            "ELSE 'In Progress' END) = %s,1) " + \
            "order by ch.compliance_history_id) t, " + \
            "(SELECT @rownum := 0) r) as cnt ) t01  " + \
        "on ch.compliance_history_id = t01.compliance_history_id " + \
        "order by t01.num,ch.compliance_history_id,acl.compliance_activity_id desc "

    # "where rc.assigned_on >= %s and rc.assigned_on <= %s " + \
    print query
    result = db.select_all(query, [
        country_id, legal_entity_id, domain_id, unit_id, unit_id, stat_map, stat_map, compliance_task,
        compliance_task, frequency_id, frequency_id, u_type_val, user_id, user_id, user_id,
        user_id, due_from, due_to, task_status, task_status
    ])

    print "length"
    print len(result)

    unit_count = []
    last = object()
    for r in result:
        if last != r["compliance_history_id"]:
            last = r["compliance_history_id"]
            unit_count.append(r["compliance_history_id"])
    print unit_count
    le_report = []
    for row in result:
        task_status = None
        activity_status = None
        # statutory_mapping = json.loads(row["statutory_mapping"])
        # if statutory_mapping[0].find(">>") >= 0:
        #     statutory_mapping = statutory_mapping[0].split(">>")[0]
        # else:
        #     statutory_mapping = str(statutory_mapping)[3:-2]
        statutory_mapping = row["act_name"]
        if row["geo_name"].find(">>") >= 0:
            val = row["geo_name"].split(">>")
            split_len = len(row["geo_name"].split(">>"))
            city = val[split_len - 1]
            unit_name = row["unit_name"].split(",")[0] + " , " + row["unit_name"].split(
                ",")[1] + " , " + city + "-" + row["unit_name"].split(",")[2]
        else:
            unit_name = row["unit_name"]

        document_name = row["documents"]
        logo = row["logo"]
        logo_size = row["logo_size"]
        if logo_size is not None:
            logo_size = int(logo_size)
        if logo:
            logo_url = "%s/%s" % (
                CLIENT_LOGO_PATH, logo
            )
        else:
            logo_url = None

        le_report.append(clientreport.LegalEntityWiseReport(
            row["compliance_history_id"], row["compliance_activity_id"],
            row["country_id"], row["legal_entity_id"], row["domain_id"], row["unit_id"],
            row["compliance_id"], unit_name, statutory_mapping, row["compliance_task"],
            row["frequency_name"], datetime_to_string(row["due_date"]), row["task_status"], row["assignee_name"],
            row["activity_status"], datetime_to_string(row["activity_on"]), document_name,
            datetime_to_string(row["completion_date"]), None, logo_url, datetime_to_string(row["start_date"]),
            row["history_count"]
        ))

    return le_report, int(len(unit_count))

##########################################################################
# Objective: To get the compliance list under filtered data
# Parameter: request object
# Result: list of compliance grouped by unit and act
##########################################################################


def process_domain_wise_report(db, request):
    where_clause = None
    count_clause = None
    condition_val = []
    select_qry = None
    from_clause = None
    u_type_val = 0
    country_id = request.country_id
    legal_entity_id = request.legal_entity_id
    domain_id = request.domain_id

    stat_map = request.statutory_mapping

    user_type = request.user_type
    if user_type == 'All':
        user_type = '%'
    if user_type == "Assignee":
        u_type_val = 1
    elif user_type == "Concurrence":
        u_type_val = 2
    elif user_type == "Approval":
        u_type_val = 3
    user_id = request.user_id
    if user_id == 0:
        user_id = None
    else:
        user_id = str(user_id)

    due_from = request.due_from_date
    due_to = request.due_to_date
    task_status = request.task_status
    unit_id = request.unit_id
    if unit_id == 0:
        unit_id = None

    compliance_task = request.compliance_task
    if compliance_task is None:
        compliance_task = None

    frequency_id = request.frequency_id

    if due_from is not None and due_to is not None:
        due_from = string_to_datetime(due_from).date()
        due_to = string_to_datetime(due_to).date()

    query = "select t01.num, " + \
        "acl.compliance_activity_id,ch.compliance_history_id, ch.legal_entity_id,ch.unit_id, " + \
        "(select concat(unit_code,' - ',unit_name,' , ',address,' , ', postal_code) from tbl_units where unit_id = ch.unit_id) as unit_name,ch.compliance_id, " + \
        "concat(com.document_name,' - ',com.compliance_task) as compliance_name, " + \
        "(select frequency from tbl_compliance_frequency where frequency_id = com.frequency_id) as frequency_name, " + \
        "SUBSTRING_INDEX(substring(substring(com.statutory_mapping,3),1, char_length(com.statutory_mapping) -4), '>>', 1) as act_name, " + \
        "acl.activity_on, (select geography_name from tbl_units where unit_id = ch.unit_id) as geo_name, " + \
        "ch.due_date,ch.completion_date, ch.legal_entity_id, com.domain_id, ch.unit_id, com.country_id, " + \
        "(CASE WHEN (ch.due_date < ch.completion_date and ch.current_status = 3) THEN 'Delayed Compliance' " + \
        "WHEN (ch.due_date >= ch.completion_date and ch.approve_status <> 3 and ch.current_status = 3) THEN 'Complied' " + \
        "WHEN (ch.due_date >= ch.completion_date and ch.current_status < 3) THEN 'In Progress' " + \
        "WHEN (ch.due_date < ch.completion_date and ch.current_status < 3) THEN 'Not Complied' " + \
        "WHEN (ch.current_status = 3 and ch.approve_status = 3) THEN 'Not Complied' " + \
        "WHEN (ch.completion_date IS NULL and IFNULL(ch.current_status,0) = 0) THEN 'In Progress' " + \
        "ELSE 'In Progress' END) as task_status, com.compliance_task, " + \
        "(CASE WHEN ((acl.activity_by = ch.completed_by) or (acl.action is null and ch.current_status = 3)) " + \
        "THEN ch.documents ELSE '-' END) as documents, (case when acl.action is null and ch.current_status = 3 " + \
        "Then '-' when acl.action is null then 'Pending' else acl.action end) as activity_status, " + \
        "(CASE WHEN acl.activity_by = ch.approved_by THEN (select IFNULL(concat(employee_code,' - ',employee_name),'Administrator') from tbl_users where user_id = ac.approval_person) " + \
        "WHEN acl.activity_by = ch.concurred_by THEN (select concat(employee_code,' - ',employee_name) from tbl_users where user_id = ac.concurrence_person)  " + \
        "WHEN acl.activity_by = ch.completed_by THEN (select concat(employee_code,' - ',employee_name) from tbl_users where user_id = ac.assignee) ELSE  " + \
        "(select concat(employee_code,' - ',employee_name) from tbl_users where user_id = ac.assignee) END) as assignee_name, ch.start_date, " + \
        "(select logo from tbl_legal_entities where legal_entity_id = ch.legal_entity_id) as logo, " + \
        "(select logo_size from tbl_legal_entities where legal_entity_id = ch.legal_entity_id) as logo_size, " + \
        "(select count(compliance_history_id) from tbl_compliance_activity_log where " + \
        "compliance_history_id = ch.compliance_history_id) as history_count " + \
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
            "and IF(%s IS NOT NULL, ac.unit_id = %s,1) " + \
            "and IF(%s IS NOT NULL,SUBSTRING_INDEX(substring(substring(com.statutory_mapping,3),1, char_length(com.statutory_mapping) -4), '>>', 1) = %s,1) " + \
            "and IF(%s IS NOT NULL, com.compliance_task like concat('%',%s,'%'),1) " + \
            "and IF(%s > 0, com.frequency_id = %s,1) " + \
            "and (CASE %s WHEN 1 THEN (ch.completed_by = acl.activity_by OR acl.activity_by IS NULL) " + \
            "WHEN 2 THEN ch.concurred_by = acl.activity_by WHEN 3 THEN ch.approved_by = acl.activity_by " + \
            "ELSE 1 END) " + \
            "and IF(%s IS NOT NULL, (ch.completed_by = %s OR ch.concurred_by = %s OR ch.approved_by = %s),1) " + \
            "and date(ch.due_date) >= %s and date(ch.due_date) <= %s " + \
            "and IF(%s <> 'All',(CASE WHEN (ch.due_date < ch.completion_date and ch.current_status = 3) THEN 'Delayed Compliance' " + \
            "WHEN (ch.due_date >= ch.completion_date and ch.approve_status <> 3 and ch.current_status = 3) THEN 'Complied' " + \
            "WHEN (ch.due_date >= ch.completion_date and ch.current_status < 3) THEN 'Inprogress' " + \
            "WHEN (ch.due_date < ch.completion_date and ch.current_status < 3) THEN 'Not Complied' " + \
            "WHEN (ch.current_status = 3 and ch.approve_status = 3) THEN 'Not Complied' " + \
            "WHEN (ch.completion_date IS NULL and IFNULL(ch.current_status,0) = 0) THEN 'Inprogress' " + \
            "ELSE 'In Progress' END) = %s,1) " + \
            "order by ch.compliance_history_id) t, " + \
            "(SELECT @rownum := 0) r) as cnt ) t01  " + \
        "on ch.compliance_history_id = t01.compliance_history_id " + \
        "order by t01.num,ch.compliance_history_id,acl.compliance_activity_id desc "

    # "where rc.assigned_on >= %s and rc.assigned_on <= %s " + \
    print query
    result = db.select_all(query, [
        country_id, legal_entity_id, domain_id, unit_id, unit_id, stat_map, stat_map, compliance_task,
        compliance_task, frequency_id, frequency_id, u_type_val, user_id, user_id, user_id,
        user_id, due_from, due_to, task_status, task_status
    ])

    print "length"
    print len(result)

    unit_count = []
    last = object()
    for r in result:
        if last != r["compliance_history_id"]:
            last = r["compliance_history_id"]
            unit_count.append(r["compliance_history_id"])
    print len(unit_count)
    le_report = []
    for row in result:
        task_status = None
        activity_status = None
        # statutory_mapping = json.loads(row["statutory_mapping"])
        # if statutory_mapping[0].find(">>") >= 0:
        #     statutory_mapping = statutory_mapping[0].split(">>")[0]
        # else:
        #     statutory_mapping = str(statutory_mapping)[3:-2]
        statutory_mapping = row["act_name"]

        if row["geo_name"].find(">>") >= 0:
            val = row["geo_name"].split(">>")
            split_len = len(row["geo_name"].split(">>"))
            city = val[split_len - 1]
            unit_name = row["unit_name"].split(",")[0] + " , " + row["unit_name"].split(
                ",")[1] + " , " + city + "-" + row["unit_name"].split(",")[2]
        else:
            unit_name = row["unit_name"]

        document_name = row["documents"]
        logo = row["logo"]
        logo_size = row["logo_size"]
        if logo_size is not None:
            logo_size = int(logo_size)
        if logo:
            logo_url = "%s/%s" % (
                CLIENT_LOGO_PATH, logo
            )
        else:
            logo_url = None

        le_report.append(clientreport.LegalEntityWiseReport(
            row["compliance_history_id"], row["compliance_activity_id"],
            row["country_id"], row["legal_entity_id"], row["domain_id"], row["unit_id"],
            row["compliance_id"], unit_name, statutory_mapping, row["compliance_task"],
            row["frequency_name"], datetime_to_string(row["due_date"]), row["task_status"], row["assignee_name"],
            row["activity_status"], datetime_to_string(row["activity_on"]), document_name,
            datetime_to_string(row["completion_date"]), None, logo_url, datetime_to_string(row["start_date"]),
            row["history_count"]
        ))

    return le_report, int(len(unit_count))


##########################################################################
# Objective: To get the compliance list under filtered data
# Parameter: request object
# Result: list of compliance grouped by domain and act
##########################################################################
def process_unit_wise_report(db, request):
    where_clause = None
    count_clause = None
    condition_val = []
    select_qry = None
    from_clause = None
    u_type_val = 0
    country_id = request.country_id
    legal_entity_id = request.legal_entity_id
    domain_id = request.d_id_optional
    if domain_id == 0:
        domain_id = None

    stat_map = request.statutory_mapping

    user_type = request.user_type
    if user_type == 'All':
        user_type = '%'
    if user_type == "Assignee":
        u_type_val = 1
    elif user_type == "Concurrence":
        u_type_val = 2
    elif user_type == "Approval":
        u_type_val = 3
    user_id = request.user_id
    if user_id == 0:
        user_id = None
    else:
        user_id = str(user_id)

    due_from = request.due_from_date
    due_to = request.due_to_date
    task_status = request.task_status
    unit_id = request.unit_id
    if unit_id == 0:
        unit_id = None

    compliance_task = request.compliance_task
    if compliance_task is None:
        compliance_task = None

    frequency_id = request.frequency_id

    if due_from is not None and due_to is not None:
        due_from = string_to_datetime(due_from).date()
        due_to = string_to_datetime(due_to).date()

    query = "select t01.num, " + \
        "acl.compliance_activity_id,ch.compliance_history_id, ch.legal_entity_id,ch.unit_id, " + \
        "(select concat(unit_code,' - ',unit_name,' , ',address,' , ', postal_code) from tbl_units where unit_id = ch.unit_id) as unit_name,ch.compliance_id, " + \
        "concat(com.document_name,' - ',com.compliance_task) as compliance_name, " + \
        "(select frequency from tbl_compliance_frequency where frequency_id = com.frequency_id) as frequency_name, " + \
        "SUBSTRING_INDEX(substring(substring(com.statutory_mapping,3),1, char_length(com.statutory_mapping) -4), '>>', 1) as act_name, " + \
        "acl.activity_on, (select geography_name from tbl_units where unit_id = ch.unit_id) as geo_name, " + \
        "ch.due_date,ch.completion_date, ch.legal_entity_id, com.domain_id, ch.unit_id, com.country_id, " + \
        "(CASE WHEN (ch.due_date < ch.completion_date and ch.current_status = 3) THEN 'Delayed Compliance' " + \
        "WHEN (ch.due_date >= ch.completion_date and ch.approve_status <> 3 and ch.current_status = 3) THEN 'Complied' " + \
        "WHEN (ch.due_date >= ch.completion_date and ch.current_status < 3) THEN 'In Progress' " + \
        "WHEN (ch.due_date < ch.completion_date and ch.current_status < 3) THEN 'Not Complied' " + \
        "WHEN (ch.current_status = 3 and ch.approve_status = 3) THEN 'Not Complied' " + \
        "WHEN (ch.completion_date IS NULL and IFNULL(ch.current_status,0) = 0) THEN 'In Progress' " + \
        "ELSE 'In Progress' END) as task_status, com.compliance_task, " + \
        "(CASE WHEN ((acl.activity_by = ch.completed_by) or (acl.action is null and ch.current_status = 3)) " + \
        "THEN ch.documents ELSE '-' END) as documents, (case when acl.action is null and ch.current_status = 3 " + \
        "Then '-' when acl.action is null then 'Pending' else acl.action end) as activity_status, " + \
        "(CASE WHEN acl.activity_by = ch.approved_by THEN (select IFNULL(concat(employee_code,' - ',employee_name),'Administrator') from tbl_users where user_id = ac.approval_person) " + \
        "WHEN acl.activity_by = ch.concurred_by THEN (select concat(employee_code,' - ',employee_name) from tbl_users where user_id = ac.concurrence_person)  " + \
        "WHEN acl.activity_by = ch.completed_by THEN (select concat(employee_code,' - ',employee_name) from tbl_users where user_id = ac.assignee) ELSE  " + \
        "(select concat(employee_code,' - ',employee_name) from tbl_users where user_id = ac.assignee) END) as assignee_name, ch.start_date, " + \
        "(select logo from tbl_legal_entities where legal_entity_id = ch.legal_entity_id) as logo, " + \
        "(select logo_size from tbl_legal_entities where legal_entity_id = ch.legal_entity_id) as logo_size, " + \
        "(select domain_name from tbl_domains where domain_id = com.domain_id) as domain_name, " + \
        "(select count(compliance_history_id) from tbl_compliance_activity_log where " + \
        "compliance_history_id = ch.compliance_history_id) as history_count " + \
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
                    "where com.country_id = %s and ch.legal_entity_id = %s and ac.unit_id = %s " + \
            "and IF(%s IS NOT NULL, com.domain_id = %s,1) " + \
            "and IF(%s IS NOT NULL,SUBSTRING_INDEX(substring(substring(com.statutory_mapping,3),1, char_length(com.statutory_mapping) -4), '>>', 1) = %s,1) " + \
            "and IF(%s IS NOT NULL, com.compliance_task like concat('%',%s,'%'),1) " + \
            "and IF(%s > 0, com.frequency_id = %s,1) " + \
            "and (CASE %s WHEN 1 THEN (ch.completed_by = acl.activity_by OR acl.activity_by IS NULL) " + \
            "WHEN 2 THEN ch.concurred_by = acl.activity_by WHEN 3 THEN ch.approved_by = acl.activity_by " + \
            "ELSE 1 END) " + \
            "and IF(%s IS NOT NULL, (ch.completed_by = %s OR ch.concurred_by = %s OR ch.approved_by = %s),1) " + \
            "and date(ch.due_date) >= %s and date(ch.due_date) <= %s " + \
            "and IF(%s <> 'All',(CASE WHEN (ch.due_date < ch.completion_date and ch.current_status = 3) THEN 'Delayed Compliance' " + \
            "WHEN (ch.due_date >= ch.completion_date and ch.approve_status <> 3 and ch.current_status = 3) THEN 'Complied' " + \
            "WHEN (ch.due_date >= ch.completion_date and ch.current_status < 3) THEN 'Inprogress' " + \
            "WHEN (ch.due_date < ch.completion_date and ch.current_status < 3) THEN 'Not Complied' " + \
            "WHEN (ch.current_status = 3 and ch.approve_status = 3) THEN 'Not Complied' " + \
            "WHEN (ch.completion_date IS NULL and IFNULL(ch.current_status,0) = 0) THEN 'Inprogress' " + \
            "ELSE 'In Progress' END) = %s,1) " + \
            "order by ch.compliance_history_id) t, " + \
            "(SELECT @rownum := 0) r) as cnt ) t01  " + \
        "on ch.compliance_history_id = t01.compliance_history_id " + \
        "order by t01.num,ch.compliance_history_id,acl.compliance_activity_id desc "

    # "where rc.assigned_on >= %s and rc.assigned_on <= %s " + \
    print query
    result = db.select_all(query, [
        country_id, legal_entity_id, unit_id, domain_id, domain_id, stat_map, stat_map, compliance_task,
        compliance_task, frequency_id, frequency_id, u_type_val, user_id, user_id, user_id,
        user_id, due_from, due_to, task_status, task_status
    ])
    unit_count = []
    last = object()
    for r in result:
        if last != r["compliance_history_id"]:
            last = r["compliance_history_id"]
            unit_count.append(r["compliance_history_id"])

    unit_report = []
    for row in result:
        task_status = None
        statutory_mapping = row["act_name"]

        if row["geo_name"].find(">>") >= 0:
            val = row["geo_name"].split(">>")
            split_len = len(row["geo_name"].split(">>"))
            city = val[split_len - 1]
            unit_name = row["unit_name"].split(",")[0] + " , " + row["unit_name"].split(
                ",")[1] + " , " + city + "-" + row["unit_name"].split(",")[2]
        else:
            unit_name = row["unit_name"]

        document_name = row["documents"]
        url = None
        logo = row["logo"]
        logo_size = row["logo_size"]
        if logo_size is not None:
            logo_size = int(logo_size)
        if logo:
            logo_url = "%s/%s" % (
                CLIENT_LOGO_PATH, logo
            )
        else:
            logo_url = None

        unit_report.append(clientreport.UnitWiseReport(
            row["compliance_history_id"], row["compliance_activity_id"],
            row["country_id"], row["legal_entity_id"], row["domain_id"], row["unit_id"],
            row["compliance_id"], unit_name, statutory_mapping, row["compliance_task"],
            row["frequency_name"], datetime_to_string(row["due_date"]), row["task_status"], row["assignee_name"],
            row["activity_status"], datetime_to_string(row["activity_on"]), document_name,
            datetime_to_string(row["completion_date"]), url, row["domain_name"], logo_url,
            datetime_to_string(row["start_date"]), row["history_count"]
        ))
    return unit_report, int(len(unit_count))

##########################################################################
# Objective: To get the domains list with user id under selected legal entity
# Parameter: request object
# Result: list of domains and its users under the leagl entity selection
##########################################################################


def get_domains_for_sp_users(db, legal_entity_id):
    query = "select distinct(t2.user_id), t1.domain_id, (select domain_name from tbl_domains where " + \
            "domain_id = t2.domain_id) as domain_name, (select service_provider_id from tbl_users " +\
            "where user_id = t2.user_id) as sp_id_optional from tbl_legal_entity_domains as t1 " + \
            "inner join tbl_user_domains as t2 on t2.domain_id = t1.domain_id and " + \
            "t2.legal_entity_id = t1.legal_entity_id where t1.legal_entity_id = %s order by domain_name;"
    result = db.select_all(query, [legal_entity_id])
    user_domains_list = []
    for row in result:
        user_domains_list.append(clientreport.ServiceProviderDomains(
            row["user_id"], row["domain_id"], row[
                "domain_name"], row["sp_id_optional"]
        )
        )
    return user_domains_list

##########################################################################
# Objective: To get the units with the users under selected legal entity, country
# Parameter: request object
# Result: list of units with the users under the selected country, legal entity
##########################################################################


def get_units_for_sp_users(db, country_id, legal_entity_id):
    query = "select t2.user_id as user_id_optional,t1.unit_id, t3.domain_id, t1.unit_code, t1.unit_name, " + \
            "(select service_provider_id from tbl_users where user_id=t2.user_id) as sp_id_optional " + \
            "from tbl_units as t1 left join tbl_user_units as t2 on t2.unit_id=t1.unit_id " + \
            "inner join tbl_units_organizations as t3 on t3.unit_id = t1.unit_id " + \
            "where t1.legal_entity_id=%s and country_id=%s group by t1.unit_id, t2.user_id, t3.domain_id;"
    result = db.select_all(query, [legal_entity_id, country_id])
    users_units_list = []
    for row in result:
        users_units_list.append(clientreport.ServiceProviderUnits(
            row["user_id_optional"], row["unit_id"], row[
                "domain_id"], row["unit_code"],
            row["unit_name"], row["sp_id_optional"]
        )
        )
    return users_units_list

##########################################################################
# Objective: To get the acts with users under selected legal entity
# Parameter: request object
# Result: list of acts with the users under the selected legal entity
##########################################################################
def get_acts_for_sp_users(db, legal_entity_id, country_id):
    query = "select t1.legal_entity_id, t1.country_id, t1.domain_id, t1.unit_id, t2.compliance_id, " + \
            "t2.statutory_mapping, t1.assignee, (select service_provider_id from tbl_users where " + \
            "user_id = t1.assignee) as sp_ass_id_optional, t1.concurrence_person, (select " + \
            "service_provider_id from tbl_users where user_id = t1.concurrence_person) as " + \
            "sp_cc_id_optional, t1.approval_person, (select service_provider_id from tbl_users " + \
            "where user_id = t1.approval_person) as sp_app_id_optional " + \
            "from tbl_assign_compliances as t1 inner join tbl_compliances as t2 " + \
            "on t2.compliance_id = t1.compliance_id and t2.domain_id = t1.domain_id " + \
            "where t1.legal_entity_id = %s and t1.country_id = %s"
    result = db.select_all(query, [legal_entity_id, country_id])
    le_act_list = []
    for row in result:
        stat_map = json.loads(row["statutory_mapping"])
        if stat_map[0].find(">>") >= 0:
            stat_map = stat_map[0].split(">>")[0]
        else:
            stat_map = str(stat_map)[3:-2]
        le_act_list.append(clientreport.ServiceProviderActList(
            row["legal_entity_id"], row["country_id"], row[
                "domain_id"], row["unit_id"],
            row["compliance_id"], row["assignee"], row["sp_ass_id_optional"],
            row["concurrence_person"], row[
                "sp_cc_id_optional"], row["approval_person"],
            row["sp_app_id_optional"], statutory_mapping=stat_map
        )
        )
    return le_act_list

##########################################################################
# Objective: To get the lists of users under service provider
# Parameter: request object
# Result: list of users under service provider
##########################################################################


def get_service_provider_user_list(db, country_id, legal_entity_id):
    query = "select t1.domain_id, t1.unit_id, t1.compliance_id, t2.service_provider_id as sp_id, " + \
            "t2.user_id, IFNULL(concat(employee_code,' - ',employee_name),'Administrator') as username " + \
            "from tbl_assign_compliances as t1 inner join tbl_users as t2 " + \
            "on (t2.user_id=t1.assignee or t2.user_id=t1.concurrence_person or " + \
            "t2.user_id=t1.approval_person) where t1.legal_entity_id = %s and t1.country_id = %s "

    result = db.select_all(query, [legal_entity_id, country_id])
    sp_user_details = []
    for row in result:
        sp_id_optional = row["sp_id"]
        sp_user_details.append(clientreport.ServiceProvidersUsers(
            row["domain_id"], row["unit_id"], row["compliance_id"], sp_id_optional,
            row["user_id"], user_name=row["username"]
        ))
    return sp_user_details


##########################################################################
# Objective: To get the compliance list under filtered data
# Parameter: request object
# Result: list of compliance grouped by unit and act
##########################################################################
def process_service_provider_wise_report(db, request):
    where_clause = None
    condition_val = []
    select_qry = None
    from_clause = None
    country_id = request.country_id
    legal_entity_id = request.legal_entity_id
    sp_id = request.sp_id
    domain_id = request.domain_id
    stat_map = request.statutory_mapping
    due_from = request.due_from_date
    due_to = request.due_to_date
    task_status = request.task_status
    if task_status == "All":
        task_status = '%'

    user_id = request.user_id
    if user_id == 0:
        user_id = None
    else:
        user_id = str(user_id)

    select_qry = "select t1.compliance_history_id, t2.compliance_activity_id, t3.country_id, t1.legal_entity_id, t3.domain_id, t1.unit_id, t1.compliance_id, t1.due_date,  " + \
        "t1.completed_on, t1.completion_date, t1.current_status, t1.approve_status, t1.start_date, " + \
        "(select concat(unit_code,'-',unit_name,',',address,',',postal_code)" + \
        "from tbl_units where unit_id = t1.unit_id) as unit_name, t3.statutory_mapping, " + \
        "(select geography_name from tbl_units where unit_id = t1.unit_id) as geo_name, " + \
        "t3.compliance_task, (select frequency from tbl_compliance_frequency where " + \
        "frequency_id = t3.frequency_id) as frequency_name, " + \
        "(CASE WHEN (t1.due_date < t1.completion_date and t1.current_status = 3) THEN 'Delayed Compliance' " + \
        "WHEN (t1.due_date >= t1.completion_date and t1.approve_status <> 3 and t1.current_status = 3) THEN 'Complied' " + \
        "WHEN (t1.due_date >= t1.completion_date and t1.current_status < 3) THEN 'In Progress' " + \
        "WHEN (t1.due_date < t1.completion_date and t1.current_status < 3) THEN 'Not Complied' " + \
        "WHEN (t1.current_status = 3 and t1.approve_status = 3) THEN 'Not Complied' " + \
        "WHEN (t1.completion_date IS NULL and IFNULL(t1.current_status,0) = 0) THEN 'In Progress' " + \
        "ELSE 'In Progress' END) as task_status, " + \
        "(CASE WHEN ((t2.activity_by = t1.completed_by) or (t2.action is null and t1.current_status = 3)) " + \
        "THEN t1.documents ELSE '-' END) as documents, (case when t2.action is null and t1.current_status = 3 " + \
        "Then '-' when t2.action is null then 'Pending' else t2.action end) as activity_status, " + \
        "(CASE WHEN t2.activity_by = t1.approved_by THEN (select IFNULL(concat(employee_code,' - ',employee_name),'Administrator') from tbl_users where user_id = t1.approved_by) " + \
        "WHEN t2.activity_by = t1.concurred_by THEN (select concat(employee_code,' - ',employee_name) from tbl_users where user_id = t1.concurred_by)  " + \
        "WHEN t2.activity_by = t1.completed_by THEN (select concat(employee_code,' - ',employee_name) from tbl_users where user_id = t1.completed_by) ELSE  " + \
        "(select concat(employee_code,' - ',employee_name) from tbl_users where user_id = t1.completed_by) END) as assignee_name, " + \
        "t1.completed_by, t2.activity_on, t1.document_size, " + \
        "(select logo from tbl_legal_entities where legal_entity_id = t1.legal_entity_id) as logo, " + \
        "(select logo_size from tbl_legal_entities where legal_entity_id = t1.legal_entity_id) as logo_size, " + \
        "(select count(compliance_history_id) from tbl_compliance_activity_log where " + \
        "compliance_history_id = t1.compliance_history_id) as history_count "
    from_clause = "from tbl_users as t4 inner join tbl_compliance_history as t1 " + \
        "on t1.completed_by = t4.user_id and t4.is_service_provider = 1 " + \
        "inner join tbl_legal_entity_domains as t5 on t5.legal_entity_id = t1.legal_entity_id inner join " + \
        "tbl_compliances as t3 on t3.compliance_id = t1.compliance_id and t3.domain_id = t5.domain_id " + \
        "left join tbl_compliance_activity_log as t2 on t2.compliance_history_id = t1.compliance_history_id " + \
        "inner join tbl_assign_compliances as ac on ac.compliance_id = t1.compliance_id where "
    where_clause = "t3.country_id = %s and t3.domain_id = %s "
    condition_val.extend([country_id, domain_id])

    if request.statutory_mapping is not None:
        stat_map = '%' + stat_map + '%'
        where_clause = where_clause + "and t3.statutory_mapping like %s "
        condition_val.append(stat_map)

    # where_clause = where_clause + "and IF(%s IS NOT NULL, (t1.completed_by = %s),1) "
    # condition_val.extend([user_id, user_id, user_id, user_id])

    if task_status == "Complied":
        where_clause = where_clause + \
            "and t1.due_date >= t1.completion_date and t1.current_status = 3 and t1.approve_status <> 3 "
    elif task_status == "Delayed Compliance":
        where_clause = where_clause + \
            "and t1.due_date < t1.completion_date and t1.current_status = 3 "
    elif task_status == "Inprogress":
        where_clause = where_clause + "and ((t1.completion_date is NULL and IFNULL(t1.current_status,0) = 0) or " + \
            "(t1.due_date >= t1.completion_date and t1.current_status < 3)) "
    elif task_status == "Not Complied":
        where_clause = where_clause + "and ((t1.due_date < t1.completion_date and t1.current_status < 3) or " + \
            "(t1.current_status = 3 and t1.approve_status = 3))"

    if due_from is not None and due_to is not None:
        due_from = string_to_datetime(due_from).date()
        due_to = string_to_datetime(due_to).date()
        where_clause = where_clause + " and t1.due_date >= " + \
            " date(%s)  and t1.due_date < " + \
            " DATE_ADD(%s, INTERVAL 1 DAY) "
        condition_val.extend([due_from, due_to])
    elif due_from is not None and due_to is None:
        due_from = string_to_datetime(due_from).date()
        where_clause = where_clause + " and t1.due_date >= " + \
            " date(%s)  and t1.due_date < " + \
            " DATE_ADD(date(curdate()), INTERVAL 1 DAY) "
        condition_val.append(due_from)
    elif due_from is None and due_to is not None:
        due_to = string_to_datetime(due_to).date()
        where_clause = where_clause + " and t1.due_date < " + \
            " DATE_ADD(%s, INTERVAL 1 DAY) "
        condition_val.append(due_to)

    compliance_task = request.compliance_task
    if compliance_task is not None:
        where_clause = where_clause + "and t3.compliance_task like concat('%',%s, '%') "
        condition_val.append(compliance_task)

    unit_id = request.unit_id
    if int(unit_id) > 0:
        where_clause = where_clause + "and ac.unit_id = %s "
        condition_val.append(unit_id)

    if user_id is not None:
        where_clause = where_clause + "and t4.user_id = %s "
        condition_val.append(user_id)

    where_clause = where_clause + "and t4.service_provider_id = %s and " + \
        "t1.legal_entity_id = %s group by t2.compliance_activity_id " + \
        "order by t1.due_date,t1.compliance_history_id, t2.compliance_activity_id desc;"
    condition_val.extend([sp_id, legal_entity_id])

    query = select_qry + from_clause + where_clause
    result = db.select_all(query, condition_val)

    unit_count = []
    last = object()
    for r in result:
        if last != r["compliance_history_id"]:
            last = r["compliance_history_id"]
            unit_count.append(r["compliance_history_id"])

    sp_report = []
    for row in result:
        task_status = None
        activity_status = None
        statutory_mapping = json.loads(row["statutory_mapping"])
        if statutory_mapping[0].find(">>") >= 0:
            statutory_mapping = statutory_mapping[0].split(">>")[0]
        else:
            statutory_mapping = str(statutory_mapping)[3:-2]

        if row["geo_name"].find(">>") >= 0:
            val = row["geo_name"].split(">>")
            split_len = len(row["geo_name"].split(">>"))
            city = val[split_len - 1]
            unit_name = row["unit_name"].split(",")[0] + " , " + row["unit_name"].split(
                ",")[1] + " , " + city + "-" + row["unit_name"].split(",")[2]
        else:
            unit_name = row["unit_name"]

        document_name = row["documents"]
        compliance_task = row["compliance_task"]
        if document_name == "None":
            document_name = None
        if document_name:
            name = "%s - %s" % (
                document_name, compliance_task
            )
        else:
            name = compliance_task

        # format_file = row["format_file"]
        format_file_size = row["document_size"]
        if format_file_size is not None:
            format_file_size = int(format_file_size)
        if document_name:
            url = "%s" % (
                document_name
            )
        else:
            url = None

        logo = row["logo"]
        logo_size = row["logo_size"]
        if logo_size is not None:
            logo_size = int(logo_size)
        if logo:
            logo_url = "%s/%s" % (
                CLIENT_LOGO_PATH, logo
            )
        else:
            logo_url = None

        sp_report.append(clientreport.LegalEntityWiseReport(
            row["compliance_history_id"], row["compliance_activity_id"],
            row["country_id"], row["legal_entity_id"], row["domain_id"], row["unit_id"],
            row["compliance_id"], unit_name, statutory_mapping, row["compliance_task"],
            row["frequency_name"], datetime_to_string(row["due_date"]), row["task_status"], row["assignee_name"],
            row["activity_status"], datetime_to_string(row["activity_on"]), document_name,
            datetime_to_string(row["completion_date"]), url, logo_url, datetime_to_string(row["start_date"]),
            row["history_count"]
        ))
    return sp_report, int(len(unit_count))

##########################################################################
# Objective: To get the list of users under legal entity
# Parameter: request object
# Result: list of users
##########################################################################


def get_le_users_list(db):
    query = "select user_id, employee_code, employee_name, " + \
        "user_category_id from tbl_users where user_category_id <> 2;"
    result = db.select_all(query, None)
    units_users_list = []
    for row in result:
        if row["employee_code"] is None or row["employee_code"] == "":
            user_name = row["employee_name"]
        else:
            user_name = row["employee_code"] + ' - ' + row["employee_name"]
        units_users_list.append(clientreport.LegalEntityUsers(
            row["user_id"], user_name, row["user_category_id"]
        ))
    return units_users_list

##########################################################################
# Objective: To get the domains list with user id under selected legal entity
# Parameter: request object
# Result: list of domains and its users under the leagl entity selection
##########################################################################


def get_domains_for_le_users(db, legal_entity_id):
    query = "select distinct t1.user_id, t3.domain_id as d_id_optional, (select domain_name from tbl_domains where " + \
            "domain_id = t3.domain_id) as domain_name from tbl_users t1 left join tbl_user_legal_entities t2  " + \
            "on t1.user_id = t2.user_id left join tbl_legal_entity_domains t3 on t2.legal_entity_id = " + \
            "t3.legal_entity_id left join tbl_user_domains t4 on t1.user_id = t4.user_id and " + \
            "t3.legal_entity_id = t4.legal_entity_id and t3.domain_id = t4.domain_id where " + \
            "if(t1.user_id <> 1,t2.legal_entity_id = %s,1) and t3.domain_id is not null ; "
    result = db.select_all(query, [legal_entity_id])
    user_domains_list = []
    for row in result:
        user_domains_list.append(clientreport.UserDomains(
            row["user_id"], row["d_id_optional"], row["domain_name"]
        )
        )
    return user_domains_list

##########################################################################
# Objective: To get the units with the users under selected legal entity, country
# Parameter: request object
# Result: list of units with the users under the selected country, legal entity
##########################################################################


def get_units_for_le_users(db, country_id, legal_entity_id):
    query = "select t2.user_id as user_id_optional,t1.unit_id, t3.domain_id, t1.unit_code, t1.unit_name " + \
            "from tbl_units as t1 left join tbl_user_units as t2 on t2.unit_id=t1.unit_id " + \
            "inner join tbl_units_organizations as t3 on t3.unit_id = t1.unit_id " + \
            "where t1.legal_entity_id=%s and country_id=%s group by t1.unit_id, t2.user_id, t3.domain_id;"
    result = db.select_all(query, [legal_entity_id, country_id])
    users_units_list = []
    for row in result:
        users_units_list.append(clientreport.UserUnits(
            row["user_id_optional"], row["unit_id"], row[
                "domain_id"], row["unit_code"], row["unit_name"]
        )
        )
    return users_units_list

##########################################################################
# Objective: To get the acts with users under selected legal entity
# Parameter: request object
# Result: list of acts with the users under the selected legal entity
##########################################################################


def get_acts_for_le_users(db, legal_entity_id, country_id):
    query = "select t1.legal_entity_id, t1.country_id, t1.domain_id, t1.unit_id, t2.compliance_id, " + \
            "t2.statutory_mapping, t1.assignee, t1.concurrence_person, t1.approval_person " + \
            "from tbl_assign_compliances as t1 inner join tbl_compliances as t2 " + \
            "on t2.compliance_id = t1.compliance_id and t2.domain_id = t1.domain_id " + \
            "where t1.legal_entity_id = %s and t1.country_id = %s"
    result = db.select_all(query, [legal_entity_id, country_id])
    le_act_list = []
    for row in result:
        stat_map = json.loads(row["statutory_mapping"])
        if stat_map[0].find(">>") >= 0:
            stat_map = stat_map[0].split(">>")[0]
        else:
            stat_map = str(stat_map)[3:-2]
        print "mapped"
        print stat_map
        le_act_list.append(clientreport.UsersActList(
            row["legal_entity_id"], row["country_id"], row[
                "domain_id"], row["unit_id"],
            row["compliance_id"], row["assignee"], row["concurrence_person"],
            row["approval_person"], statutory_mapping=stat_map
        )
        )
    return le_act_list

##########################################################################
# Objective: To get the compliance list under filtered data
# Parameter: request object
# Result: list of compliance grouped by domain and act
##########################################################################


def process_user_wise_report(db, request):
    where_clause = None
    count_clause = None
    condition_val = []
    select_qry = None
    from_clause = None
    u_type_val = 0
    country_id = request.country_id
    legal_entity_id = request.legal_entity_id
    domain_id = request.domain_id
    if domain_id == 0:
        domain_id = None
    stat_map = request.statutory_mapping

    user_type = request.user_type
    if user_type == 'All':
        user_type = '%'
    if user_type == "Assignee":
        u_type_val = 1
    elif user_type == "Concurrence":
        u_type_val = 2
    elif user_type == "Approval":
        u_type_val = 3
    user_id = request.user_id
    if user_id == 0:
        user_id = None
    else:
        user_id = str(user_id)

    due_from = request.due_from_date
    due_to = request.due_to_date
    task_status = request.task_status
    unit_id = request.unit_id
    if unit_id == 0:
        unit_id = None

    compliance_task = request.compliance_task
    if compliance_task is None:
        compliance_task = None

    frequency_id = request.frequency_id

    if due_from is not None and due_to is not None:
        due_from = string_to_datetime(due_from).date()
        due_to = string_to_datetime(due_to).date()

    query = "select count(0) as user_cnt " + \
            "from tbl_assign_compliances as t1 " + \
            "where t1.legal_entity_id = %s and t1.country_id = %s and " + \
            "(CASE %s WHEN 1 THEN t1.assignee = %s WHEN 2 THEN t1.concurrence_person = %s " + \
            "WHEN 3 THEN t1.approval_person = %s ELSE 1 END) "

    result = db.select_one(query, [legal_entity_id, country_id, u_type_val, user_id, user_id, user_id])
    print "user result"
    print result

    if result["user_cnt"] > 0 :
        query = "select t01.num, " + \
            "acl.compliance_activity_id,ch.compliance_history_id, ch.legal_entity_id,ch.unit_id, " + \
            "(select concat(unit_code,' - ',unit_name,' , ',address,' , ', postal_code) from tbl_units where unit_id = ch.unit_id) as unit_name,ch.compliance_id, " + \
            "concat(com.document_name,' - ',com.compliance_task) as compliance_name, " + \
            "(select frequency from tbl_compliance_frequency where frequency_id = com.frequency_id) as frequency_name, " + \
            "SUBSTRING_INDEX(substring(substring(com.statutory_mapping,3),1, char_length(com.statutory_mapping) -4), '>>', 1) as act_name, " + \
            "acl.activity_on, (select geography_name from tbl_units where unit_id = ch.unit_id) as geo_name, " + \
            "ch.due_date,ch.completion_date, ch.legal_entity_id, com.domain_id, ch.unit_id, com.country_id, " + \
            "(CASE WHEN (ch.due_date < ch.completion_date and ch.current_status = 3) THEN 'Delayed Compliance' " + \
            "WHEN (ch.due_date >= ch.completion_date and ch.approve_status <> 3 and ch.current_status = 3) THEN 'Complied' " + \
            "WHEN (ch.due_date >= ch.completion_date and ch.current_status < 3) THEN 'In Progress' " + \
            "WHEN (ch.due_date < ch.completion_date and ch.current_status < 3) THEN 'Not Complied' " + \
            "WHEN (ch.current_status = 3 and ch.approve_status = 3) THEN 'Not Complied' " + \
            "WHEN (ch.completion_date IS NULL and IFNULL(ch.current_status,0) = 0) THEN 'In Progress' " + \
            "ELSE 'In Progress' END) as task_status, com.compliance_task, " + \
            "(CASE WHEN ((acl.activity_by = ch.completed_by) or (acl.action is null and ch.current_status = 3)) " + \
            "THEN ch.documents ELSE '-' END) as documents, (case when acl.action is null and ch.current_status = 3 " + \
            "Then '-' when acl.action is null then 'Pending' else acl.action end) as activity_status, " + \
            "(CASE WHEN acl.activity_by = ch.approved_by THEN (select IFNULL(concat(employee_code,' - ',employee_name),'Administrator') from tbl_users where user_id = ch.approved_by) " + \
            "WHEN acl.activity_by = ch.concurred_by THEN (select concat(employee_code,' - ',employee_name) from tbl_users where user_id = ch.concurred_by)  " + \
            "WHEN acl.activity_by = ch.completed_by THEN (select concat(employee_code,' - ',employee_name) from tbl_users where user_id = ch.completed_by) ELSE  " + \
            "(select concat(employee_code,' - ',employee_name) from tbl_users where user_id = ch.completed_by) END) as assignee_name, ch.start_date, " + \
            "(select logo from tbl_legal_entities where legal_entity_id = ch.legal_entity_id) as logo, " + \
            "(select logo_size from tbl_legal_entities where legal_entity_id = ch.legal_entity_id) as logo_size, " + \
            "(select domain_name from tbl_domains where domain_id = com.domain_id) as domain_name, " + \
            "(select count(compliance_history_id) from tbl_compliance_activity_log where " + \
            "compliance_history_id = ch.compliance_history_id) as history_count " + \
            "from tbl_users as t4 inner join tbl_compliance_history as ch on (ch.completed_by = t4.user_id or " + \
            "ch.approved_by = t4.user_id or ch.concurred_by = t4.user_id) " + \
            "inner join tbl_compliances as com on ch.compliance_id = com.compliance_id " + \
            "left join tbl_compliance_activity_log as acl on ch.compliance_history_id = acl.compliance_history_id " + \
            "inner join tbl_assign_compliances as ac on ch.compliance_id = ac.compliance_id and ch.unit_id = ac.unit_id " + \
            "inner join ( " + \
                "select compliance_history_id,num from  " + \
                "(select compliance_history_id,@rownum := @rownum + 1 AS num  " + \
                "from (select distinct ch.compliance_history_id  " + \
                    "from tbl_users as t4 inner join tbl_compliance_history as ch on (ch.completed_by = t4.user_id " + \
                    "or (ch.approved_by = t4.user_id and ch.approve_status is not null) or " + \
                    "(ch.concurred_by = t4.user_id and ch.concurrence_status is not null)) " + \
                    "inner join tbl_compliances as com on ch.compliance_id = com.compliance_id " + \
                    "left join tbl_compliance_activity_log as acl on ch.compliance_history_id = acl.compliance_history_id " + \
                    "inner join tbl_assign_compliances as ac on ch.compliance_id = ac.compliance_id and ch.unit_id = ac.unit_id " + \
                    "where t4.user_id = %s and com.country_id = %s and ch.legal_entity_id = %s " + \
                "and IF(%s IS NOT NULL, com.domain_id = %s,1) " + \
                "and IF(%s IS NOT NULL, ac.unit_id = %s,1) " + \
                "and IF(%s IS NOT NULL,SUBSTRING_INDEX(substring(substring(com.statutory_mapping,3),1, char_length(com.statutory_mapping) -4), '>>', 1) = %s,1) " + \
                "and IF(%s IS NOT NULL, com.compliance_task like concat('%',%s,'%'),1) " + \
                "and IF(%s > 0, com.frequency_id = %s,1) " + \
                "and (CASE %s WHEN 1 THEN (ch.completed_by = acl.activity_by OR acl.activity_by IS NULL) " + \
                "WHEN 2 THEN ch.concurred_by = acl.activity_by WHEN 3 THEN ch.approved_by = acl.activity_by " + \
                "ELSE 1 END) " + \
                "and date(ch.due_date) >= %s and date(ch.due_date) <= %s " + \
                "and IF(%s <> 'All',(CASE WHEN (ch.due_date < ch.completion_date and ch.current_status = 3) THEN 'Delayed Compliance' " + \
                "WHEN (ch.due_date >= ch.completion_date and ch.approve_status <> 3 and ch.current_status = 3) THEN 'Complied' " + \
                "WHEN (ch.due_date >= ch.completion_date and ch.current_status < 3) THEN 'Inprogress' " + \
                "WHEN (ch.due_date < ch.completion_date and ch.current_status < 3) THEN 'Not Complied' " + \
                "WHEN (ch.current_status = 3 and ch.approve_status = 3) THEN 'Not Complied' " + \
                "WHEN (ch.completion_date IS NULL and IFNULL(ch.current_status,0) = 0) THEN 'Inprogress' " + \
                "ELSE 'In Progress' END) = %s,1) " + \
                "order by ch.compliance_history_id) t, " + \
                "(SELECT @rownum := 0) r) as cnt ) t01  " + \
            "on ch.compliance_history_id = t01.compliance_history_id " + \
            "order by t01.num,ch.compliance_history_id,acl.compliance_activity_id desc "

        # "where rc.assigned_on >= %s and rc.assigned_on <= %s " + \
        print query
        result = db.select_all(query, [
            user_id, country_id, legal_entity_id, domain_id, domain_id, unit_id, unit_id, stat_map, stat_map, compliance_task,
            compliance_task, frequency_id, frequency_id, u_type_val, due_from, due_to, task_status, task_status
        ])

        unit_count = []
        last = object()
        for r in result:
            if last != r["compliance_history_id"]:
                last = r["compliance_history_id"]
                unit_count.append(r["compliance_history_id"])

        user_report = []
        for row in result:
            task_status = None
            statutory_mapping = row["act_name"]

            if row["geo_name"].find(">>") >= 0:
                val = row["geo_name"].split(">>")
                split_len = len(row["geo_name"].split(">>"))
                city = val[split_len - 1]
                unit_name = row["unit_name"].split(",")[0] + " , " + row["unit_name"].split(
                    ",")[1] + " , " + city + "-" + row["unit_name"].split(",")[2]
            else:
                unit_name = row["unit_name"]

            document_name = row["documents"]
            url = None

            logo = row["logo"]
            logo_size = row["logo_size"]
            if logo_size is not None:
                logo_size = int(logo_size)
            if logo:
                logo_url = "%s/%s" % (
                    CLIENT_LOGO_PATH, logo
                )
            else:
                logo_url = None

            user_report.append(clientreport.UnitWiseReport(
                row["compliance_history_id"], row["compliance_activity_id"],
                row["country_id"], row["legal_entity_id"], row["domain_id"], row["unit_id"],
                row["compliance_id"], unit_name, statutory_mapping, row["compliance_task"],
                row["frequency_name"], datetime_to_string(row["due_date"]), row["task_status"], row["assignee_name"],
                row["activity_status"], datetime_to_string(row["activity_on"]), document_name,
                datetime_to_string(row["completion_date"]), url, row["domain_name"], logo_url,
                datetime_to_string(row["start_date"]), row["history_count"]
            ))
        return user_report, int(len(unit_count))
    else:
        return [], 0

##########################################################################
# Objective: To get the divisions list under legal entity and business group
# Parameter: request object
# Result: list of divisions from master
##########################################################################


def get_divisions_for_unit_list(db, business_group_id, legal_entity_id):
    query = "select division_id, division_name from tbl_divisions " + \
        "where legal_entity_id = %s"
    result = db.select_all(query, [legal_entity_id])
    divisions_list = []
    for row in result:
        divisions_list.append(clientreport.Divisions(
            row["division_id"], row["division_name"]
        ))
    return divisions_list

##########################################################################
# Objective: To get the categories list under legal entity and business group
# Parameter: request object
# Result: list of categories from master
##########################################################################


def get_categories_for_unit_list(db, business_group_id, legal_entity_id):
    query = "select division_id, category_id, category_name from tbl_categories " + \
        "where legal_entity_id = %s"
    result = db.select_all(query, [legal_entity_id])
    category_list = []
    for row in result:
        category_list.append(clientreport.Category(
            row["division_id"], row["category_id"], row["category_name"]
        ))
    return category_list

##########################################################################
# Objective: To get the units list under legal entity and business group and country
# Parameter: request object
# Result: list of units from master
##########################################################################


def get_units_list(db, country_id, business_group_id, legal_entity_id):
    query = "select unit_id, unit_code, unit_name, division_id, category_id from " + \
        "tbl_units where legal_entity_id =%s and country_id = %s"
    result = db.select_all(
        query, [legal_entity_id, country_id])

    query = "select t1.unit_id, t2.domain_id, t2.organisation_id " + \
        "from tbl_units as t1 inner join tbl_units_organizations as t2 on " + \
        "t2.unit_id = t1.unit_id where t1.legal_entity_id = %s and " + \
        "t1.country_id = %s group by t1.unit_id, t2.domain_id, t2.organisation_id order by " + \
        "t1.unit_id;"
    result_1 = db.select_all(
        query, [legal_entity_id, country_id])

    unit_list = []
    for row in result:
        unit_id = row["unit_id"]
        unit_code = row["unit_code"]
        unit_name = row["unit_name"]
        division_id = row["division_id"]
        category_id = row["category_id"]
        d_ids = []
        i_ids = []
        for row_1 in result_1:
            if unit_id == row_1["unit_id"]:
                d_ids.append(int(row_1["domain_id"]))
                i_ids.append(int(row_1["organisation_id"]))
        unit_list.append(clientreport.UnitList(
            unit_id, unit_code, unit_name, division_id, category_id, d_ids, i_ids
        ))
    return unit_list

##########################################################################
# Objective: To get the domains and organization list under legal entity
# Parameter: request object
# Result: list of units from master
##########################################################################


def get_domains_organization_for_le(db, legal_entity_id):
    query = "select t1.domain_id, t2.domain_name, t1.organisation_id, t3.organisation_name " + \
        "from tbl_legal_entity_domains as t1 inner join tbl_domains as t2 on " + \
        "t2.domain_id = t1.domain_id inner join tbl_organisation as t3 on " + \
        "t3.organisation_id = t1.organisation_id where t1.legal_entity_id = %s"
    result = db.select_all(query, [legal_entity_id])
    domain_organisation = []
    for row in result:
        domain_organisation.append(clientreport.DomainsOrganisation(
            row["domain_id"], row["domain_name"], row["organisation_id"],
            row["organisation_name"]
        ))
    return domain_organisation

##########################################################################
# Objective: To get the status of the units
# Parameter: request object
# Result: list of status
##########################################################################


def get_units_status(db):
    status = ("Active", "Closed", "Inactive")
    units_status = []
    i = 0
    for sts in status:
        unit_status_name = clientreport.UnitStatus(
            i, sts
        )
        units_status.append(unit_status_name)
        i = i + 1
    return units_status


##########################################################################
# Objective: To get the unit details under filtered data
# Parameter: request object
# Result: list of units grouped by division
##########################################################################
def process_unit_list_report(db, request):
    where_clause = None
    condition_val = []
    select_qry = None
    country_id = request.country_id
    business_group_id = request.business_group_id
    legal_entity_id = request.legal_entity_id
    division_id = request.division_id
    category_id = request.category_id
    unit_id = request.unit_id
    domain_id = request.domain_id
    organisation_id = request.organisation_id

    unit_status = request.unit_status
    print unit_status
    select_qry = "select t1.unit_id, t1.unit_code, t1.unit_name, t1.address, t1.postal_code, " + \
        "t1.geography_name, t1.is_closed, t1.closed_on, t1.division_id, t1.category_id, (select  " + \
        "division_name from tbl_divisions where division_id = t1.division_id) as division_name, " + \
        "(select category_name from tbl_categories where category_id = t1.category_id) as " + \
        "category_name, (select logo from tbl_legal_entities where legal_entity_id = t1.legal_entity_id) as logo, " + \
        "(select logo_size from tbl_legal_entities where legal_entity_id = t1.legal_entity_id) as logo_size, " + \
        "DATEDIFF(now(),t1.closed_on) as closed_days from tbl_units as t1 where "
    where_clause = "t1.legal_entity_id = %s and t1.country_id = %s "
    condition_val.extend([legal_entity_id, country_id])
    print business_group_id
    if business_group_id is not None and int(business_group_id) > 0:
        where_clause = where_clause + "and t1.business_group_id = %s "
        condition_val.append(business_group_id)

    if int(unit_id) > 0:
        where_clause = where_clause + "and t1.unit_id = %s "
        condition_val.append(unit_id)

    if int(division_id) > 0:
        where_clause = where_clause + "and t1.division_id = %s "
        condition_val.append(division_id)

    if int(category_id) > 0:
        where_clause = where_clause + "and t1.category_id = %s "
        condition_val.append(category_id)

    if unit_status == "Active":
        where_clause = where_clause + "and t1.is_closed = %s "
        condition_val.append(0)
    elif unit_status == "Closed":
        where_clause = where_clause + "and t1.is_closed = %s and DATEDIFF(NOW(),t1.closed_on) > 30 "
        condition_val.append(1)
    elif unit_status == "Inactive":
        where_clause = where_clause + "and t1.is_closed = %s and DATEDIFF(NOW(),t1.closed_on) <= 30 "
        condition_val.append(1)

    where_clause = where_clause + "order by t1.closed_on desc limit %s, %s;"
    condition_val.extend([int(request.from_count), int(request.page_count)])
    query = select_qry + where_clause
    print "qry"
    print query
    result = db.select_all(query, condition_val)
    print result

    where_clause = None
    condition_val = []
    if request.from_count == 0:
        select_qry = "select t1.unit_id " + \
            "from tbl_units as t1 where "
        where_clause = "t1.legal_entity_id = %s and t1.country_id = %s "
        condition_val.extend([legal_entity_id, country_id])
        print business_group_id
        if business_group_id is not None and int(business_group_id) > 0:
            where_clause = where_clause + "and t1.business_group_id = %s "
            condition_val.append(business_group_id)

        if int(unit_id) > 0:
            where_clause = where_clause + "and t1.unit_id = %s "
            condition_val.append(unit_id)

        if int(division_id) > 0:
            where_clause = where_clause + "and t1.division_id = %s "
            condition_val.append(division_id)

        if int(category_id) > 0:
            where_clause = where_clause + "and t1.category_id = %s "
            condition_val.append(category_id)

        if unit_status == "Active":
            where_clause = where_clause + "and t1.is_closed = %s "
            condition_val.append(0)
        elif unit_status == "Closed":
            where_clause = where_clause + "and t1.is_closed = %s and DATEDIFF(NOW(),t1.closed_on) > 30 "
            condition_val.append(1)
        elif unit_status == "Inactive":
            where_clause = where_clause + "and t1.is_closed = %s and DATEDIFF(NOW(),t1.closed_on) <= 30 "
            condition_val.append(1)

        where_clause = where_clause + "order by t1.closed_on desc;"
        query = select_qry + where_clause
        print "qry"
        print query
        count = db.select_all(query, condition_val)

    # domains & organisations
    select_qry = None
    where_clause = None
    condition_val = []
    select_qry = "select t1.unit_id, t2.domain_id, t2.organisation_id, (select domain_name " + \
        "from tbl_domains where domain_id = t2.domain_id) as domain_name, (select " + \
        "organisation_name from tbl_organisation where organisation_id = t2.organisation_id) as " + \
        "organisation_name, DATEDIFF(now(),t1.closed_on) as closed_days from tbl_units as t1 inner join tbl_units_organizations as t2 on " + \
        "t2.unit_id = t1.unit_id inner join tbl_legal_entity_domains as t3 on t3.legal_entity_id = " + \
        "t1.legal_entity_id and t3.domain_id = t2.domain_id where "
    where_clause = "t1.legal_entity_id = %s and t1.country_id = %s "
    condition_val.extend([legal_entity_id, country_id])

    if business_group_id is not None and int(business_group_id) > 0:
        where_clause = where_clause + "and t1.business_group_id = %s "
        condition_val.append(business_group_id)

    if int(unit_id) > 0:
        where_clause = where_clause + "and t1.unit_id = %s "
        condition_val.append(unit_id)

    if int(division_id) > 0:
        where_clause = where_clause + "and t1.division_id = %s "
        condition_val.append(division_id)

    if int(category_id) > 0:
        where_clause = where_clause + "and t1.category_id = %s "
        condition_val.append(category_id)

    if int(domain_id) > 0:
        where_clause = where_clause + "and t2.domain_id = %s "
        condition_val.append(domain_id)

    if int(organisation_id) > 0:
        where_clause = where_clause + "and t2.organisation_id = %s "
        condition_val.append(organisation_id)

    if unit_status == "Active":
        where_clause = where_clause + "and t1.is_closed = %s "
        condition_val.append(0)
    elif unit_status == "Closed":
        where_clause = where_clause + "and t1.is_closed = %s and DATEDIFF(NOW(),t1.closed_on) > 30 "
        condition_val.append(1)
    elif unit_status == "Inactive":
        where_clause = where_clause + "and t1.is_closed = %s and DATEDIFF(NOW(),t1.closed_on) <= 30 "
        condition_val.append(1)

    where_clause = where_clause + " group by t1.unit_id, t2.domain_id, t2.organisation_id order by t1.unit_id asc;"
    query = select_qry + where_clause
    result_1 = db.select_all(query, condition_val)
    unit_report = []

    for row in result:
        unit_id = row["unit_id"]
        unit_code = row["unit_code"]
        unit_name = row["unit_name"]
        geography_name = row["geography_name"]
        address = row["address"]
        postal_code = row["postal_code"]
        division_name = row["division_name"]
        if division_name is None:
            division_name = "---"

        if row["is_closed"] == 0:
            unit_status = "Active"
            closed_date = None
        elif int(row["closed_days"]) <= 30:
            unit_status = "Inactive"
            closed_date = datetime_to_string(row["closed_on"])
        else:
            unit_status = "Closed"
            closed_date = datetime_to_string(row["closed_on"])
        d_i_names = []

        if geography_name.find(">>") >= 0:
            val = geography_name.split(">>")
            split_len = len(geography_name.split(">>"))
            city = val[split_len - 1]
            geography_name = city
        else:
            geography_name = None

        logo = row["logo"]
        logo_size = row["logo_size"]
        if logo_size is not None:
            logo_size = int(logo_size)
        if logo:
            logo_url = "%s/%s" % (
                CLIENT_LOGO_PATH, logo
            )
        else:
            logo_url = None

        d_i_names = getDomainOrgn(unit_id, result_1)

        unit_report.append(clientreport.UnitListReport(
            unit_id, unit_code, unit_name, geography_name, address, postal_code,
            d_i_names, unit_status, closed_date, division_name, logo_url
        ))
    if request.from_count == 0:
        return unit_report, len(count)
    else:
        return unit_report, 0

def getDomainOrgn(unit_id, data):
    last = object()
    org_names = None
    d_i_names = []
    for row_1 in data:
        if unit_id == row_1["unit_id"]:
            if last != row_1["domain_name"] :
                if org_names is not None:
                    d_i_names.append(last + " - " + org_names + "\n")
                    org_names = None
                last = row_1["domain_name"]
                if org_names is None:
                    org_names = row_1["organisation_name"]
                else:
                    org_names = org_names + "," + row_1["organisation_name"]
            else:
                if org_names is None:
                    org_names = row_1["organisation_name"]
                else:
                    org_names = org_names + "," + row_1["organisation_name"]
    if org_names is not None:
        d_i_names.append(last + " - " + org_names + "\n")
        org_names = None
    return d_i_names
##########################################################################
# Objective: To get the Compliance details under filtered data
# Parameter: request object
# Result: list of compliances and acts
##########################################################################
def process_statutory_notification_list_report(db, request):
    where_clause = None
    condition_val = []
    select_qry = None
    country_id = request.country_id
    legal_entity_id = request.legal_entity_id
    domain_id = request.domain_id
    statutory_mapping = request.statutory_mapping
    due_from = request.due_from_date
    due_to = request.due_to_date

    select_qry = "select t1.compliance_id, t2.statutory_mapping, t2.compliance_description, " + \
        "t2.compliance_task, SUBSTRING_INDEX(t3.notification_text,'remarks',-1) as notification_text, t3.created_on from tbl_client_compliances as t1 " + \
        "inner join tbl_compliances as t2 on t2.compliance_id = t1.compliance_id inner join " + \
        "tbl_statutory_notifications as t3 on t3.compliance_id = t2.compliance_id where "
    where_clause = "t1.legal_entity_id = %s and t1.domain_id = %s and t2.country_id = %s "
    condition_val.extend([legal_entity_id, domain_id, country_id])

    if statutory_mapping is not None:
        statutory_mapping = '%' + statutory_mapping + '%'
        where_clause = where_clause + "and t2.statutory_mapping like %s "
        condition_val.append(statutory_mapping)

    if due_from is not None and due_to is not None:
        due_from = string_to_datetime(due_from).date()
        due_to = string_to_datetime(due_to).date()
        where_clause = where_clause + " and t3.created_on >= " + \
            " date(%s)  and t3.created_on < " + \
            " DATE_ADD(%s, INTERVAL 1 DAY)  "
        condition_val.extend([due_from, due_to])
    elif due_from is not None and due_to is None:
        due_from = string_to_datetime(due_from).date()
        where_clause = where_clause + " and t3.created_on >= " + \
            " date(%s)  and t3.created_on < " + \
            " DATE_ADD(date(curdate()), INTERVAL 1 DAY) "
        condition_val.append(due_from)
    elif due_from is None and due_to is not None:
        due_to = string_to_datetime(due_to).date()
        where_clause = where_clause + " and t3.created_on < " + \
            " DATE_ADD(%s, INTERVAL 1 DAY) "
        condition_val.append(due_to)

    where_clause = where_clause + \
        "group by t1.compliance_id order by t3.created_on desc limit %s, %s;"
    condition_val.extend([int(request.from_count), int(request.page_count)])
    query = select_qry + where_clause
    print "qry"
    print query
    result = db.select_all(query, condition_val)

    where_clause = None

    condition_val = []
    if request.from_count == 0:
        select_qry = "select t1.compliance_id, t2.statutory_mapping, t2.compliance_description, " + \
            "t2.compliance_task, t3.notification_text, t3.created_on from tbl_client_compliances as t1 " + \
            "inner join tbl_compliances as t2 on t2.compliance_id = t1.compliance_id inner join " + \
            "tbl_statutory_notifications as t3 on t3.compliance_id = t2.compliance_id where "
        where_clause = "t1.legal_entity_id = %s and t1.domain_id = %s and t2.country_id = %s "
        condition_val.extend([legal_entity_id, domain_id, country_id])

        if statutory_mapping is not None:
            statutory_mapping = '%' + statutory_mapping + '%'
            where_clause = where_clause + "and t2.statutory_mapping like %s "
            condition_val.append(statutory_mapping)

        if due_from is not None and due_to is not None:
            where_clause = where_clause + " and t3.created_on >= " + \
                " date(%s)  and t3.created_on < " + \
                " DATE_ADD(%s, INTERVAL 1 DAY) "
            condition_val.extend([due_from, due_to])
        elif due_from is not None and due_to is None:
            where_clause = where_clause + " and t3.created_on >= " + \
                " date(%s)  and t3.created_on < " + \
                " DATE_ADD(date(curdate()), INTERVAL 1 DAY) "
            condition_val.append(due_from)
        elif due_from is None and due_to is not None:
            where_clause = where_clause + " and t3.created_on < " + \
                " DATE_ADD(%s, INTERVAL 1 DAY) "
            condition_val.append(due_to)

        where_clause = where_clause + \
            "group by t1.compliance_id order by t3.created_on desc;"
        query = select_qry + where_clause
        count = db.select_all(query, condition_val)

    statutory_notification = []

    for row in result:
        stat_map = json.loads(row["statutory_mapping"])
        if stat_map[0].find(">>") >= 0:
            stat_map = stat_map[0].split(">>")[0]
        else:
            stat_map = str(stat_map)[3:-2]
        print "mapped"
        notf_txt = row["notification_text"]
        notification_text = None
        if notf_txt.find("-") :
            split_notf_txt = notf_txt.split("-")
            len_split_txt = len(split_notf_txt)
            notification_text = split_notf_txt[len_split_txt-1]
        else:
            notification_text = notf_txt
        statutory_notification.append(clientreport.StatutoryNotificationReport(
            row["compliance_id"], row["compliance_task"], row[
                "compliance_description"],
            datetime_to_string(row["created_on"]), notification_text,
            statutory_mapping=stat_map
        ))
    if request.from_count == 0:
        return statutory_notification, len(count)
    else:
        return statutory_notification, 0

##########################################################################
# Objective: To get the list of activities
# Parameter: request object
# Result: list of activities
##########################################################################


def process_audit_trail_report(db, request):
    where_clause = None
    condition_val = []
    select_qry = None
    legal_entity_id = request.legal_entity_id
    user_id = request.user_id
    form_id = request.form_id_optional
    due_from = request.due_from_date
    due_to = request.due_to_date
    print "pages"
    print request.from_count
    print request.page_count
    select_qry = "select t1.user_id, t1.form_id, t1.action, t1.created_on, (select  " + \
        "employee_name from tbl_users where user_id " + \
        "= t1.user_id) as user_name, (select employee_code from tbl_users " + \
        "where user_id = t1.user_id) as emp_code, " + \
        "(select logo from tbl_legal_entities where legal_entity_id = t1.legal_entity_id) " + \
        "as logo, (select logo_size from tbl_legal_entities where legal_entity_id = t1.legal_entity_id) as logo_size " + \
        "from tbl_activity_log as t1 where "
    where_clause = "t1.form_id <> 0 "
    # condition_val.append(legal_entity_id)

    if int(user_id) > 0:
        where_clause = where_clause + "and t1.user_id = %s "
        condition_val.append(user_id)
    if int(form_id) > 0:
        where_clause = where_clause + "and t1.form_id = %s "
        condition_val.append(form_id)
    if due_from is not None and due_to is not None:
        due_from = string_to_datetime(due_from).date()
        print due_from
        due_to = string_to_datetime(due_to).date()
        where_clause = where_clause + " and t1.created_on >= " + \
            " date(%s)  and t1.created_on < " + \
            " DATE_ADD(%s, INTERVAL 1 DAY) "
        condition_val.extend([due_from, due_to])
    elif due_from is not None and due_to is None:
        due_from = string_to_datetime(due_from).date()
        where_clause = where_clause + " and t1.created_on >= " + \
            " date(%s)  and t1.created_on < " + \
            " date(curdate()) "
        condition_val.append(due_from)
    elif due_from is None and due_to is not None:
        due_to = string_to_datetime(due_to).date()
        where_clause = where_clause + " and t1.created_on < " + \
            " DATE_ADD(%s, INTERVAL 1 DAY) "
        condition_val.append(due_to)

    where_clause = where_clause + "order by t1.created_on desc limit %s, %s;"
    condition_val.extend([int(request.from_count), int(request.page_count)])
    query = select_qry + where_clause
    print "qry", query
    result = db.select_all(query, condition_val)
    print result

    activity_list = []
    for row in result:
        logo = row["logo"]
        logo_size = row["logo_size"]
        if logo_size is not None:
            logo_size = int(logo_size)
        if logo:
            logo_url = "%s/%s" % (
                CLIENT_LOGO_PATH, logo
            )
        else:
            logo_url = None

        user_name = None
        if row["emp_code"] is not None:
            user_name = row["emp_code"] + " - "+row["user_name"]
        else:
            user_name = row["user_name"]

        activity_list.append(clientreport.AuditTrailActivities(
            row["user_id"], user_name, row["form_id"],
            row["action"], datetime_to_string_time(row["created_on"]), logo_url
        ))
    condition_val = []
    where_clause = None
    if request.from_count == 0:
        select_qry = "select count(*) as total_record " + \
            "from tbl_activity_log as t1 where "
        where_clause = "t1.form_id <> 0 and t1.legal_entity_id = %s "
        condition_val.append(legal_entity_id)

        if int(user_id) > 0:
            where_clause = where_clause + "and t1.user_id = %s "
            condition_val.append(user_id)
        if int(form_id) > 0:
            where_clause = where_clause + "and t1.form_id = %s "
            condition_val.append(form_id)
        if due_from is not None and due_to is not None:
            where_clause = where_clause + " and t1.created_on >= " + \
                " date(%s)  and t1.created_on < " + \
                " DATE_ADD(%s, INTERVAL 1 DAY) "
            condition_val.extend([due_from, due_to])
        elif due_from is not None and due_to is None:
            where_clause = where_clause + " and t1.created_on >= " + \
                " date(%s)  and t1.created_on < " + \
                " date(curdate()) "
            condition_val.append(due_from)
        elif due_from is None and due_to is not None:
            where_clause = where_clause + " and t1.created_on < " + \
                " DATE_ADD(%s, INTERVAL 1 DAY) "
            condition_val.append(due_to)

        query = select_qry + where_clause
        print "qry"
        print query
        result = db.select_one(query, condition_val)
        print result
        return activity_list, result["total_record"]
    else:
        return activity_list, 0


##########################################################################
# Objective: To get the compliance status for risk report
# Parameter: request object
# Result: list of compliance status
##########################################################################
def get_risk_compiance_status(db):
    status = ("Delayed Compliance", "Not Complied",
              "Not Opted", "Unassigned Compliance")
    compliance_status = []
    i = 0
    for sts in status:
        c_task_status = clientreport.ComplianceTaskStatus(
            i, sts
        )
        compliance_status.append(c_task_status)
        i = i + 1
    return compliance_status

##########################################################################
# Objective: To get the compliance list under filtered data
# Parameter: request object
# Result: list of compliance grouped by unit and act
##########################################################################


def process_risk_report(db, request):
    # u_type = ("Assignee", "Concurrence", "Approval")
    # status = ("Complied", "Delayed Compliance", "Inprogress", "Not Complied")
    where_clause = None
    condition_val = []
    select_qry = None
    union_qry = None
    from_clause = None
    union_from_clause = None
    union_where_clause = None
    union_condition_val = []
    country_id = request.country_id
    business_group_id = request.business_group_id
    legal_entity_id = request.legal_entity_id
    domain_id = request.domain_id
    division_id = request.division_id
    category_id = request.category_id
    unit_id = request.unit_id
    stat_map = request.statutory_mapping
    compliance_task = request.compliance_task
    task_status = request.task_status
    condition_val = []
    total_record = 0
    u_type_val = 0
    user_type = request.task_status
    if task_status == 'All':
        user_type = '%'
    if task_status == "Not Opted":
        u_type_val = 1
    elif task_status == "Delayed Compliance":
        u_type_val = 2
    elif task_status == "Not Complied":
        u_type_val = 3
    if task_status == "All":
        print "jcj"
        # All or unassigned compliance
        union_qry = "(select t2.statutory_mapping, (select concat(unit_code,'-',unit_name,',', " + \
            "address,',',postal_code) from tbl_units where unit_id = t1.unit_id) as unit_name, t2.compliance_task, " + \
            "(select frequency from tbl_compliance_frequency where frequency_id = t2.frequency_id) as frequency_name, " + \
            "(select geography_name from tbl_units where unit_id = t1.unit_id) as geo_name, null as admin_incharge, " + \
            "null as assignee_name, t2.penal_consequences, null as documents, null as document_size, " + \
            "(select logo from tbl_legal_entities where legal_entity_id = t1.legal_entity_id) as logo, " + \
            "(select logo_size from tbl_legal_entities where legal_entity_id = t1.legal_entity_id) as logo_size, " + \
            "null as completion_date, null as due_date, null as current_status, t1.compliance_opted_status, " + \
            "null as start_date, null as due_date, null as concurrer_name, null as approver_name, null as remarks, " + \
            "null as documents, null as assigned_on, null as concurred_on, null as approved_on, null as approve_status, " + \
            "'Unassigned Compliance' as compliance_task_status, t1.unit_id, t2.frequency_id, t2.duration_type_id "
        union_from_clause = "from tbl_client_compliances as t1 inner join tbl_compliances as t2 " + \
            "on t2.compliance_id = t1.compliance_id inner join tbl_units as t3 on t3.unit_id = t1.unit_id where "
        union_where_clause = "t2.country_id = %s and t2.domain_id = %s "
        condition_val.extend([country_id, domain_id])

        if int(division_id) > 0:
            union_where_clause = union_where_clause + "and t3.division_id = %s "
            condition_val.append(division_id)

        if int(category_id) > 0:
            union_where_clause = union_where_clause + "and t3.category_id = %s "
            condition_val.append(category_id)

        if request.statutory_mapping is not None:
            stat_map = '%' + stat_map + '%'
            union_where_clause = union_where_clause + "and t2.statutory_mapping like %s "
            condition_val.append(stat_map)

        compliance_task = request.compliance_task
        print compliance_task
        if compliance_task is not None:
            union_where_clause = union_where_clause + "and coalesce(t2.compliance_task,'') like concat('%',%s,'%') "
            condition_val.append(compliance_task)

        unit_id = request.unit_id
        if int(unit_id) > 0:
            union_where_clause = union_where_clause + "and t1.unit_id = %s "
            condition_val.append(unit_id)

        union_where_clause = union_where_clause + "and t1.legal_entity_id = %s and t1.compliance_opted_status = 1 and t1.compliance_id not in " + \
            "(select compliance_id from tbl_assign_compliances) order by t2.compliance_task asc)"
        condition_val.extend([legal_entity_id])

        # other compliance
        select_qry = "(select t3.statutory_mapping, (select concat(unit_code,'-',unit_name,',', " + \
            "address,',',postal_code) from tbl_units where unit_id = t1.unit_id) as unit_name, t3.compliance_task, " + \
            "(select frequency from tbl_compliance_frequency where frequency_id = t3.frequency_id) as frequency_name, " + \
            "(select geography_name from tbl_units where unit_id = t1.unit_id) as geo_name, " + \
            "(select employee_name from tbl_users where user_id = t6.assigned_by) as admin_incharge, " + \
            "(CASE WHEN t2.activity_by = t1.approved_by THEN (select IFNULL(concat(employee_code,' - ',employee_name),'Administrator') from tbl_users where user_id = t6.approval_person) " + \
            "WHEN t2.activity_by = t1.concurred_by THEN (select concat(employee_code,' - ',employee_name) from tbl_users where user_id = t6.concurrence_person)  " + \
            "WHEN t2.activity_by = t1.completed_by THEN (select concat(employee_code,' - ',employee_name) from tbl_users where user_id = t6.assignee) ELSE  " + \
            "(select concat(employee_code,' - ',employee_name) from tbl_users where user_id = t6.assignee) END) as assignee_name, " + \
            "t3.penal_consequences, t1.documents, t1.document_size, " + \
            "(select logo from tbl_legal_entities where legal_entity_id = t1.legal_entity_id) as logo, " + \
            "(select logo_size from tbl_legal_entities where legal_entity_id = t1.legal_entity_id) as logo_size, " + \
            "t1.completion_date, t1.due_date, t1.current_status, t5.compliance_opted_status, t1.start_date, " + \
            "t1.due_date, (select concat(employee_code,'-',employee_name) from tbl_users where user_id = " + \
            "t1.concurred_by) as concurrer_name, (select (case when employee_code is not null then " + \
            "concat(employee_code,'-',employee_name) else employee_name end) from tbl_users " + \
            "where user_id = t1.approved_by) as approver_name, t1.remarks, t1.documents, t1.completed_on as " + \
            "assigned_on, t1.concurred_on, t1.approved_on, t1.approve_status, " + \
            "(CASE WHEN (t1.due_date < t1.completion_date and ifnull(t1.current_status,0) = 3 and ifnull(t1.approve_status,0) < 3) THEN 'Delayed Compliance' " + \
            "WHEN (t1.due_date < t1.completion_date and ifnull(t1.current_status,0) < 3) then 'Not Complied' " + \
            "when (ifnull(t1.current_status,0) =3 and ifnull(t1.approve_status,0) = 3) THEN 'Not Complied' " + \
            "WHEN t5.compliance_opted_status = 0 THEN 'Not Opted' END) as compliance_task_status, t1.unit_id, " + \
            "t3.frequency_id, t3.duration_type_id "
        from_clause = "from tbl_compliance_history as t1 inner join tbl_compliances as t3 on " + \
            "t3.compliance_id = t1.compliance_id inner join tbl_client_compliances as t5 " + \
            "on t5.compliance_id = t1.compliance_id left join tbl_compliance_activity_log as t2 " + \
            "on t2.compliance_history_id = t1.compliance_history_id inner join tbl_assign_compliances as t6 on t6.compliance_id = " + \
            "t1.compliance_id and t6.unit_id = t1.unit_id inner join tbl_units as t4 on t4.unit_id = t1.unit_id where "
        where_clause = "t3.country_id = %s and t3.domain_id = %s "
        condition_val.extend([country_id, domain_id])

        where_clause = where_clause + "and (CASE %s WHEN 1 THEN (t5.compliance_opted_status = 0) " + \
            "WHEN 2 THEN t1.due_date < t1.completion_date and ifnull(t1.current_status,0) = 3 and ifnull(t1.approve_status,0) < 3 " + \
            "WHEN 3 THEN (t1.due_date < t1.completion_date and ifnull(t1.current_status,0) < 3) or (ifnull(t1.current_status,0) = 3 and ifnull(t1.approve_status,0) = 3) " + \
            "else ((t5.compliance_opted_status = 0) or (t1.due_date < t1.completion_date and ifnull(t1.current_status,0) = 3 and ifnull(t1.approve_status,0) < 3) " + \
            "or (t1.due_date < t1.completion_date and ifnull(t1.current_status,0) < 3) or (ifnull(t1.current_status,0) = 3 and ifnull(t1.approve_status,0) = 3)" + \
            ") end)"
        condition_val.append(u_type_val)

        if int(division_id) > 0:
            where_clause = where_clause + "and t4.division_id = %s "
            condition_val.append(division_id)

        if int(category_id) > 0:
            where_clause = where_clause + "and t4.category_id = %s "
            condition_val.append(category_id)

        if request.statutory_mapping is not None:
            stat_map = '%' + stat_map + '%'
            where_clause = where_clause + "and t3.statutory_mapping like %s "
            condition_val.append(stat_map)

        compliance_task = request.compliance_task
        if compliance_task is not None:
            where_clause = where_clause + "and t3.compliance_task like concat('%',%s, '%') "
            condition_val.append(compliance_task)

        unit_id = request.unit_id
        if int(unit_id) > 0:
            where_clause = where_clause + "and t1.unit_id = %s "
            condition_val.append(unit_id)

        where_clause = where_clause + \
            "and t1.legal_entity_id = %s group by t1.compliance_history_id order by t3.compliance_task asc)"
        condition_val.extend([legal_entity_id])

        query = union_qry + union_from_clause + union_where_clause + " union " + select_qry + from_clause + where_clause + "limit %s, %s;"
        condition_val.extend([int(request.from_count), int(request.page_count)])
        result = db.select_all(query, condition_val)
        print "aaa"
        print query
        where_clause = None
        condition_val = []
        select_qry = None
        union_qry = None
        from_clause = None
        union_from_clause = None
        union_where_clause = None
        if request.from_count == 0:
            union_qry = "(select t2.statutory_mapping, (select concat(unit_code,'-',unit_name,',', " + \
                "address,',',postal_code) from tbl_units where unit_id = t1.unit_id) as unit_name, t2.compliance_task, " + \
                "(select frequency from tbl_compliance_frequency where frequency_id = t2.frequency_id) as frequency_name, " + \
                "(select geography_name from tbl_units where unit_id = t1.unit_id) as geo_name, null as admin_incharge, " + \
                "null as assignee_name, t2.penal_consequences, null as documents, null as document_size, " + \
                "(select logo from tbl_legal_entities where legal_entity_id = t1.legal_entity_id) as logo, " + \
                "(select logo_size from tbl_legal_entities where legal_entity_id = t1.legal_entity_id) as logo_size, " + \
                "null as completion_date, null as due_date, null as current_status, t1.compliance_opted_status, " + \
                "null as start_date, null as due_date, null as concurrer_name, null as approver_name, null as remarks, " + \
                "null as documents, null as assigned_on, null as concurred_on, null as approved_on, null as approve_status, " + \
                "'Unassigned Compliance' as compliance_task_status, t1.unit_id, t2.frequency_id, t2.duration_type_id "
            union_from_clause = "from tbl_client_compliances as t1 inner join tbl_compliances as t2 " + \
                "on t2.compliance_id = t1.compliance_id inner join tbl_units as t3 on t3.unit_id = t1.unit_id where "
            union_where_clause = "t2.country_id = %s and t2.domain_id = %s "
            condition_val.extend([country_id, domain_id])

            if int(division_id) > 0:
                union_where_clause = union_where_clause + "and t3.division_id = %s "
                condition_val.append(division_id)

            if int(category_id) > 0:
                union_where_clause = union_where_clause + "and t3.category_id = %s "
                condition_val.append(category_id)

            if request.statutory_mapping is not None:
                stat_map = '%' + stat_map + '%'
                union_where_clause = union_where_clause + "and t2.statutory_mapping like %s "
                condition_val.append(stat_map)

            compliance_task = request.compliance_task
            if compliance_task is not None:
                union_where_clause = union_where_clause + "and t2.compliance_task like concat('%',%s, '%') "
                condition_val.append(compliance_task)

            unit_id = request.unit_id
            if int(unit_id) > 0:
                union_where_clause = union_where_clause + "and t1.unit_id = %s "
                condition_val.append(unit_id)

            union_where_clause = union_where_clause + "and t1.legal_entity_id = %s and t1.compliance_opted_status = 1 and t1.compliance_id not in " + \
                "(select compliance_id from tbl_assign_compliances) order by t2.compliance_task asc)"
            condition_val.extend([legal_entity_id])

            # other compliance
            select_qry = "(select t3.statutory_mapping, (select concat(unit_code,'-',unit_name,',', " + \
                "address,',',postal_code) from tbl_units where unit_id = t1.unit_id) as unit_name, t3.compliance_task, " + \
                "(select frequency from tbl_compliance_frequency where frequency_id = t3.frequency_id) as frequency_name, " + \
                "(select geography_name from tbl_units where unit_id = t1.unit_id) as geo_name, " + \
                "(select employee_name from tbl_users where user_id = t6.assigned_by) as admin_incharge, " + \
                "(CASE WHEN t2.activity_by = t1.approved_by THEN (select IFNULL(concat(employee_code,' - ',employee_name),'Administrator') from tbl_users where user_id = t6.approval_person) " + \
                "WHEN t2.activity_by = t1.concurred_by THEN (select concat(employee_code,' - ',employee_name) from tbl_users where user_id = t6.concurrence_person)  " + \
                "WHEN t2.activity_by = t1.completed_by THEN (select concat(employee_code,' - ',employee_name) from tbl_users where user_id = t6.assignee) ELSE  " + \
                "(select concat(employee_code,' - ',employee_name) from tbl_users where user_id = t6.assignee) END) as assignee_name, " + \
                "t3.penal_consequences, t1.documents, t1.document_size, " + \
                "(select logo from tbl_legal_entities where legal_entity_id = t1.legal_entity_id) as logo, " + \
                "(select logo_size from tbl_legal_entities where legal_entity_id = t1.legal_entity_id) as logo_size, " + \
                "t1.completion_date, t1.due_date, t1.current_status, t5.compliance_opted_status, t1.start_date, " + \
                "t1.due_date, (select concat(employee_code,'-',employee_name) from tbl_users where user_id = " + \
                "t1.concurred_by) as concurrer_name, (select (case when employee_code is not null then " + \
                "concat(employee_code,'-',employee_name) else employee_name end) from tbl_users " + \
                "where user_id = t1.approved_by) as approver_name, t1.remarks, t1.documents, t1.completed_on as " + \
                "assigned_on, t1.concurred_on, t1.approved_on, t1.approve_status, " + \
                "(CASE WHEN (t1.due_date < t1.completion_date and ifnull(t1.current_status,0) = 3 and ifnull(t1.approve_status,0) < 3) THEN 'Delayed Compliance' " + \
                "WHEN (t1.due_date < t1.completion_date and ifnull(t1.current_status,0) < 3) then 'Not Complied' " + \
                "when (ifnull(t1.current_status,0) =3 and ifnull(t1.approve_status,0) = 3) THEN 'Not Complied' " + \
                "WHEN t5.compliance_opted_status = 0 THEN 'Not Opted' END) as compliance_task_status, t1.unit_id, " +\
                "t3.frequency_id, t3.duration_type_id "

            from_clause = "from tbl_compliance_history as t1 left join tbl_compliance_activity_log as t2 " + \
                "on t2.compliance_history_id = t1.compliance_history_id inner join " + \
                "tbl_compliances as t3 on t3.compliance_id = t1.compliance_id inner join tbl_client_compliances as t5 " + \
                "on t5.compliance_id = t1.compliance_id inner join tbl_assign_compliances as t6 on t6.compliance_id = " + \
                "t1.compliance_id inner join tbl_units as t4 on t4.unit_id = t1.unit_id where "
            where_clause = "t3.country_id = %s and t3.domain_id = %s "
            condition_val.extend([country_id, domain_id])

            where_clause = where_clause + "and (CASE %s WHEN 1 THEN (t5.compliance_opted_status = 0) " + \
                "WHEN 2 THEN t1.due_date < t1.completion_date and ifnull(t1.current_status,0) = 3 and ifnull(t1.approve_status,0) < 3 " + \
                "WHEN 3 THEN (t1.due_date < t1.completion_date and ifnull(t1.current_status,0) < 3) or (ifnull(t1.current_status,0) = 3 and ifnull(t1.approve_status,0) = 3) " + \
                "else ((t5.compliance_opted_status = 0) or (t1.due_date < t1.completion_date and ifnull(t1.current_status,0) = 3 and ifnull(t1.approve_status,0) < 3) " + \
                "or (t1.due_date < t1.completion_date and ifnull(t1.current_status,0) < 3) or (ifnull(t1.current_status,0) = 3 and ifnull(t1.approve_status,0) = 3)" + \
                ") end)"
            condition_val.append(u_type_val)
            if int(division_id) > 0:
                where_clause = where_clause + "and t4.division_id = %s "
                condition_val.append(division_id)

            if int(category_id) > 0:
                where_clause = where_clause + "and t4.category_id = %s "
                condition_val.append(category_id)

            if request.statutory_mapping is not None:
                stat_map = '%' + stat_map + '%'
                where_clause = where_clause + "and t3.statutory_mapping like %s "
                condition_val.append(stat_map)

            compliance_task = request.compliance_task
            if compliance_task is not None:
                where_clause = where_clause + "and t3.compliance_task like concat('%',%s, '%') "
                condition_val.append(compliance_task)

            unit_id = request.unit_id
            if int(unit_id) > 0:
                where_clause = where_clause + "and t1.unit_id = %s "
                condition_val.append(unit_id)

            where_clause = where_clause + \
                "and t1.legal_entity_id = %s group by t1.compliance_history_id order by t3.compliance_task asc)"
            condition_val.extend([legal_entity_id])
            query = union_qry + union_from_clause + union_where_clause + " union " + select_qry + from_clause + where_clause
            count = db.select_all(query, condition_val)
            total_record = len(count)
        else:
            total_record = 0
        risk_report = []
        for row in result:
            task_status = None
            statutory_mapping = json.loads(row["statutory_mapping"])
            if statutory_mapping[0].find(">>") >= 0:
                statutory_mapping = statutory_mapping[0].split(">>")[0]
            else:
                statutory_mapping = str(statutory_mapping)[3:-2]

            if row["geo_name"].find(">>") >= 0:
                val = row["geo_name"].split(">>")
                split_len = len(row["geo_name"].split(">>"))
                city = val[split_len - 1]
                unit_name = row["unit_name"].split(",")[0] + " , " + row["unit_name"].split(
                    ",")[1] + " , " + city + "-" + row["unit_name"].split(",")[2]
            else:
                unit_name = row["unit_name"]


            if row["compliance_task_status"] is None:
                print row["compliance_opted_status"], row["due_date"], row["completion_date"], row["current_status"], row["approve_status"]

            document_name = row["documents"]
            compliance_task = row["compliance_task"]
            if document_name == "None":
                document_name = None
            if document_name:
                name = "%s - %s" % (
                    document_name, compliance_task
                )
            else:
                name = compliance_task

            format_file = row["documents"]
            format_file_size = row["document_size"]
            if format_file_size is not None:
                format_file_size = int(format_file_size)
            if format_file:
                url = "%s" % (
                    format_file
                )
            else:
                url = None

            logo = row["logo"]
            logo_size = row["logo_size"]
            if logo_size is not None:
                logo_size = int(logo_size)
            if logo:
                logo_url = "%s/%s" % (
                    CLIENT_LOGO_PATH, logo
                )
            else:
                logo_url = None
            print row["frequency_id"], row["duration_type_id"]
            start_date = datetime_to_string(row["start_date"])
            due_date = datetime_to_string(row["due_date"])
            if row["frequency_id"] == 5 and row["duration_type_id"] == 2:
                start_date = datetime_to_string_time(row["start_date"])
                due_date = datetime_to_string_time(row["due_date"])

            risk_report.append(clientreport.RiskReport(
                statutory_mapping, unit_name, row[
                    "compliance_task"], row["frequency_name"],
                row["penal_consequences"], row["admin_incharge"], row[
                    "assignee_name"], row["compliance_task_status"],
                document_name, url, logo_url, start_date, due_date,
                row["concurrer_name"], row["approver_name"],
                datetime_to_string_time(row["assigned_on"]), datetime_to_string_time(
                    row["concurred_on"]),
                datetime_to_string_time(row["approved_on"]), comp_remarks=row["remarks"],
                unit_id=row["unit_id"]
            ))

    elif task_status == "Unassigned Compliance":
        # All or unassigned compliance
        union_qry = "select t2.statutory_mapping, (select concat(unit_code,'-',unit_name,',', " + \
            "address,',',postal_code) from tbl_units where unit_id = t1.unit_id) as unit_name, t2.compliance_task, " + \
            "(select frequency from tbl_compliance_frequency where frequency_id = t2.frequency_id) as frequency_name, " + \
            "(select geography_name from tbl_units where unit_id = t1.unit_id) as geo_name, " + \
            "t2.penal_consequences, t2.format_file, t2.format_file_size, t1.unit_id, " + \
            "(select logo from tbl_legal_entities where legal_entity_id = t1.legal_entity_id) as logo, " + \
            "(select logo_size from tbl_legal_entities where legal_entity_id = t1.legal_entity_id) as logo_size, " + \
            "t2.frequency_id, t2.duration_type_id "
        union_from_clause = "from tbl_client_compliances as t1 inner join tbl_compliances as t2 " + \
            "on t2.compliance_id = t1.compliance_id inner join tbl_units as t3 on t3.unit_id = t1.unit_id where "
        union_where_clause = "t2.country_id = %s and t2.domain_id = %s "
        condition_val.extend([country_id, domain_id])

        if int(division_id) > 0:
            union_where_clause = union_where_clause + "and t3.division_id = %s "
            condition_val.append(division_id)

        if int(category_id) > 0:
            union_where_clause = union_where_clause + "and t3.category_id = %s "
            condition_val.append(category_id)

        if request.statutory_mapping is not None:
            stat_map = '%' + stat_map + '%'
            union_where_clause = union_where_clause + "and t2.statutory_mapping like %s "
            condition_val.append(stat_map)

        compliance_task = request.compliance_task
        if compliance_task is not None:
            union_where_clause = union_where_clause + "and t2.compliance_task like concat('%',%s, '%') "
            condition_val.append(compliance_task)

        unit_id = request.unit_id
        if int(unit_id) > 0:
            union_where_clause = union_where_clause + "and t1.unit_id = %s "
            condition_val.append(unit_id)

        union_where_clause = union_where_clause + "and t1.compliance_opted_status =1 and t1.legal_entity_id = %s and t1.compliance_id not in " + \
            "(select compliance_id from tbl_assign_compliances) order by t2.compliance_task asc limit %s, %s;"
        condition_val.extend([legal_entity_id, request.from_count, request.page_count])

        query = union_qry + union_from_clause + union_where_clause
        result_1 = db.select_all(query, condition_val)

        # total
        condition_val = []
        if request.from_count == 0:
            union_where_clause = "t2.country_id = %s and t2.domain_id = %s "
            condition_val.extend([country_id, domain_id])

            if int(division_id) > 0:
                union_where_clause = union_where_clause + "and t3.division_id = %s "
                condition_val.append(division_id)

            if int(category_id) > 0:
                union_where_clause = union_where_clause + "and t3.category_id = %s "
                condition_val.append(category_id)

            if request.statutory_mapping is not None:
                stat_map = '%' + stat_map + '%'
                union_where_clause = union_where_clause + "and t2.statutory_mapping like %s "
                condition_val.append(stat_map)

            compliance_task = request.compliance_task
            if compliance_task is not None:
                union_where_clause = union_where_clause + "and t2.compliance_task like concat('%',%s, '%') "
                condition_val.append(compliance_task)

            unit_id = request.unit_id
            if int(unit_id) > 0:
                union_where_clause = union_where_clause + "and t1.unit_id = %s "
                condition_val.append(unit_id)

            union_where_clause = union_where_clause + "and t1.compliance_opted_status = 1 and t1.legal_entity_id = %s and t1.compliance_id not in " + \
                "(select compliance_id from tbl_assign_compliances) order by t2.compliance_task asc"
            condition_val.extend([legal_entity_id])
            query = union_qry + union_from_clause + union_where_clause
            count = db.select_all(query, condition_val)
            total_record = len(count)
        else:
            total_record = 0

        risk_report = []

        for row in result_1:
            task_status = "Unassigned Compliance"
            statutory_mapping = json.loads(row["statutory_mapping"])
            if statutory_mapping[0].find(">>") >= 0:
                statutory_mapping = statutory_mapping[0].split(">>")[0]
            else:
                statutory_mapping = str(statutory_mapping)[3:-2]

            if row["geo_name"].find(">>") >= 0:
                val = row["geo_name"].split(">>")
                split_len = len(row["geo_name"].split(">>"))
                city = val[split_len - 1]
                unit_name = row["unit_name"].split(",")[0] + " , " + row["unit_name"].split(
                    ",")[1] + " , " + city + "-" + row["unit_name"].split(",")[2]
            else:
                unit_name = row["unit_name"]

            document_name = None

            format_file = row["format_file"]
            format_file_size = row["format_file_size"]
            if format_file_size is not None:
                format_file_size = int(format_file_size)
            if format_file:
                url = "%s" % (
                    format_file
                )
            else:
                url = None

            logo = row["logo"]
            logo_size = row["logo_size"]
            if logo_size is not None:
                logo_size = int(logo_size)
            if logo:
                logo_url = "%s/%s" % (
                    CLIENT_LOGO_PATH, logo
                )
            else:
                logo_url = None

            risk_report.append(clientreport.RiskReport(
                statutory_mapping, unit_name, row[
                    "compliance_task"], row["frequency_name"],
                row["penal_consequences"], None, None, task_status, None, None, logo_url, None, None,
                None, None, None, None, None, comp_remarks=None, unit_id=row["unit_id"]
            ))
        condition_val = []
    elif (task_status != "All" or task_status != "Unassigned Compliance"):
        condition_val = []
        # other compliance
        select_qry = "select t3.statutory_mapping, (select concat(unit_code,'-',unit_name,',', " + \
            "address,',',postal_code) from tbl_units where unit_id = t1.unit_id) as unit_name, t3.compliance_task, " + \
            "(select frequency from tbl_compliance_frequency where frequency_id = t3.frequency_id) as frequency_name, " + \
            "(select geography_name from tbl_units where unit_id = t1.unit_id) as geo_name, " + \
            "(select employee_name from tbl_users where user_id = t6.assigned_by) as admin_incharge, " + \
            "(CASE WHEN t2.activity_by = t1.approved_by THEN (select IFNULL(concat(employee_code,' - ',employee_name),'Administrator') from tbl_users where user_id = t6.approval_person) " + \
            "WHEN t2.activity_by = t1.concurred_by THEN (select concat(employee_code,' - ',employee_name) from tbl_users where user_id = t6.concurrence_person)  " + \
            "WHEN t2.activity_by = t1.completed_by THEN (select concat(employee_code,' - ',employee_name) from tbl_users where user_id = t6.assignee) ELSE  " + \
            "(select concat(employee_code,' - ',employee_name) from tbl_users where user_id = t6.assignee) END) as assignee_name, " + \
            "t3.penal_consequences, t1.documents, t1.document_size, " + \
            "(select logo from tbl_legal_entities where legal_entity_id = t1.legal_entity_id) as logo, " + \
            "(select logo_size from tbl_legal_entities where legal_entity_id = t1.legal_entity_id) as logo_size, " + \
            "t1.completion_date, t1.due_date, t1.current_status, t5.compliance_opted_status, t1.start_date, " + \
            "t1.due_date, (select concat(employee_code,'-',employee_name) from tbl_users where user_id = " + \
            "t1.concurred_by) as concurrer_name, (select (case when employee_code is not null then " + \
            "concat(employee_code,'-',employee_name) else employee_name end) from tbl_users " + \
            "where user_id = t1.approved_by) as approver_name, t1.remarks, t1.documents, t1.completed_on as " + \
            "assigned_on, t1.concurred_on, t1.approved_on, t1.approve_status, " + \
            "(CASE WHEN (t1.due_date < t1.completion_date and ifnull(t1.current_status,0) = 3 and ifnull(t1.approve_status,0) < 3) THEN 'Delayed Compliance' " + \
            "WHEN (t1.due_date < t1.completion_date and ifnull(t1.current_status,0) < 3) then 'Not Complied' " + \
            "when (ifnull(t1.current_status,0) =3 and ifnull(t1.approve_status,0) = 3) THEN 'Not Complied' " + \
            "WHEN t5.compliance_opted_status = 0 THEN 'Not Opted' END) as compliance_task_status, t1.unit_id, " + \
            "t3.frequency_id, t3.duration_type_id "
        from_clause = "from tbl_compliance_history as t1 left join tbl_compliance_activity_log as t2 " + \
            "on t2.compliance_history_id = t1.compliance_history_id inner join " + \
            "tbl_compliances as t3 on t3.compliance_id = t1.compliance_id inner join tbl_client_compliances as t5 " + \
            "on t5.compliance_id = t1.compliance_id inner join tbl_assign_compliances as t6 on t6.compliance_id = " + \
            "t1.compliance_id inner join tbl_units as t4 on t4.unit_id = t1.unit_id where "
        where_clause = "t3.country_id = %s and t3.domain_id = %s "
        condition_val.extend([country_id, domain_id])

        if int(division_id) > 0:
            where_clause = where_clause + "and t4.division_id = %s "
            condition_val.append(division_id)

        if int(category_id) > 0:
            where_clause = where_clause + "and t4.category_id = %s "
            condition_val.append(category_id)

        if request.statutory_mapping is not None:
            stat_map = '%' + stat_map + '%'
            where_clause = where_clause + "and t3.statutory_mapping like %s "
            condition_val.append(stat_map)

        if task_status == "Not Opted":
            where_clause = where_clause + "and t5.compliance_opted_status = 0 "
        elif task_status == "Delayed Compliance":
            where_clause = where_clause + "and t1.due_date < t1.completion_date and ifnull(t1.current_status,0) = 3 and ifnull(t1.approve_status,0) < 3 "
        elif task_status == "Not Complied":
            where_clause = where_clause + "and ((t1.due_date < t1.completion_date and ifnull(t1.current_status,0) < 3) or (ifnull(t1.current_status,0) = 3 and ifnull(t1.approve_status,0) = 3)) "

        compliance_task = request.compliance_task
        if compliance_task is not None:
            where_clause = where_clause + "and t3.compliance_task like concat('%',%s, '%') "
            condition_val.append(compliance_task)

        unit_id = request.unit_id
        if int(unit_id) > 0:
            where_clause = where_clause + "and t1.unit_id = %s "
            condition_val.append(unit_id)

        where_clause = where_clause + \
            "and t1.legal_entity_id = %s group by t1.compliance_history_id order by t3.compliance_task asc limit %s, %s;"
        condition_val.extend([legal_entity_id, request.from_count, request.page_count])

        query = select_qry + from_clause + where_clause
        result = db.select_all(query, condition_val)
        # total_record
        condition_val = []
        if request.from_count == 0:
            where_clause = "t3.country_id = %s and t3.domain_id = %s "
            condition_val.extend([country_id, domain_id])

            if int(division_id) > 0:
                where_clause = where_clause + "and t4.division_id = %s "
                condition_val.append(division_id)

            if int(category_id) > 0:
                where_clause = where_clause + "and t4.category_id = %s "
                condition_val.append(category_id)

            if request.statutory_mapping is not None:
                stat_map = '%' + stat_map + '%'
                where_clause = where_clause + "and t3.statutory_mapping like %s "
                condition_val.append(stat_map)

            if task_status == "Not Opted":
                where_clause = where_clause + "and t5.compliance_opted_status = 0 "
            elif task_status == "Delayed Compliance":
                where_clause = where_clause + "and t1.due_date < t1.completion_date and ifnull(t1.current_status,0) = 3 and ifnull(t1.approve_status,0) < 3 "
            elif task_status == "Not Complied":
                where_clause = where_clause + "and ((t1.due_date < t1.completion_date and ifnull(t1.current_status,0) < 3) or (ifnull(t1.current_status,0) = 3 and ifnull(t1.approve_status,0) = 3)) "

            compliance_task = request.compliance_task
            if compliance_task is not None:
                where_clause = where_clause + "and t3.compliance_task like concat('%',%s, '%') "
                condition_val.append(compliance_task)

            unit_id = request.unit_id
            if int(unit_id) > 0:
                where_clause = where_clause + "and t1.unit_id = %s "
                condition_val.append(unit_id)

            where_clause = where_clause + \
                "and t1.legal_entity_id = %s group by t1.compliance_history_id order by t3.compliance_task asc;"
            condition_val.extend([legal_entity_id])

            query = select_qry + from_clause + where_clause
            count = db.select_all(query, condition_val)

            total_record = total_record + len(count)
        else:
            total_record = 0

        risk_report = []

        for row in result:
            task_status = None
            statutory_mapping = json.loads(row["statutory_mapping"])
            if statutory_mapping[0].find(">>") >= 0:
                statutory_mapping = statutory_mapping[0].split(">>")[0]
            else:
                statutory_mapping = str(statutory_mapping)[3:-2]

            if row["geo_name"].find(">>") >= 0:
                val = row["geo_name"].split(">>")
                split_len = len(row["geo_name"].split(">>"))
                city = val[split_len - 1]
                unit_name = row["unit_name"].split(",")[0] + " , " + row["unit_name"].split(
                    ",")[1] + " , " + city + "-" + row["unit_name"].split(",")[2]
            else:
                unit_name = row["unit_name"]

            if task_status is None:
                print row["compliance_opted_status"], row["due_date"], row["completion_date"], row["current_status"], row["approve_status"]

            document_name = row["documents"]
            compliance_task = row["compliance_task"]
            if document_name == "None":
                document_name = None
            if document_name:
                name = "%s - %s" % (
                    document_name, compliance_task
                )
            else:
                name = compliance_task

            format_file_size = row["document_size"]
            if format_file_size is not None:
                format_file_size = int(format_file_size)
            if document_name:
                url = "%s" % (
                    document_name
                )
            else:
                url = None

            logo = row["logo"]
            logo_size = row["logo_size"]
            if logo_size is not None:
                logo_size = int(logo_size)
            if logo:
                logo_url = "%s/%s" % (
                    CLIENT_LOGO_PATH, logo
                )
            else:
                logo_url = None

            print row["frequency_id"], row["duration_type_id"]
            start_date = datetime_to_string(row["start_date"])
            due_date = datetime_to_string(row["due_date"])
            if row["frequency_id"] == 5 and row["duration_type_id"] == 2:
                start_date = datetime_to_string_time(row["start_date"])
                due_date = datetime_to_string_time(row["due_date"])

            risk_report.append(clientreport.RiskReport(
                statutory_mapping, unit_name, row[
                    "compliance_task"], row["frequency_name"],
                row["penal_consequences"], row["admin_incharge"], row[
                    "assignee_name"], row["compliance_task_status"],
                document_name, url, logo_url, start_date, due_date,
                row["concurrer_name"], row["approver_name"],
                datetime_to_string_time(row["assigned_on"]), datetime_to_string_time(
                    row["concurred_on"]),
                datetime_to_string_time(row["approved_on"]), comp_remarks=row["remarks"],
                unit_id=row["unit_id"]
            )) # frequency_id = 5, duration type = 2
    return risk_report, total_record
