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
    query = "SELECT t1.unit_id, t1.unit_code, t1.unit_name, t2.domain_id, t1.country_id, t1.legal_entity_id " + \
            "FROM tbl_units as t1 inner join tbl_units_organizations as t2 on t2.unit_id = t1.unit_id " + \
            "where t1.legal_entity_id = %s and t1.country_id = %s group by t1.unit_id;"
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
            "t2.statutory_mapping, t2.compliance_task, t2.frequency_id from " + \
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
            "t1.assignee, (select concat(employee_code,'-',employee_name) from tbl_users where " + \
            "user_id = t1.assignee) as assignee_name, t1.concurrence_person, " + \
            "(select concat(employee_code,'-',employee_name) from tbl_users where " + \
            "user_id = t1.concurrence_person) as concurrer_name, t1.approval_person, " + \
            "(select concat(employee_code,'-',employee_name) from tbl_users where " + \
            "user_id = t1.approval_person) as approver_name from tbl_assign_compliances as t1 " + \
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
    country_id = request.country_id
    legal_entity_id = request.legal_entity_id
    domain_id = request.domain_id

    stat_map = request.statutory_mapping

    user_type = request.user_type
    if user_type == 'All':
        user_type = '%'
    user_id = request.user_id

    due_from = request.due_from_date
    due_to = request.due_to_date
    task_status = request.task_status
    if task_status == "All":
        task_status = '%'

    select_qry = "select t1.compliance_history_id, t2.compliance_activity_id, t3.country_id, " + \
        "t1.legal_entity_id, t3.domain_id, t1.unit_id, t1.compliance_id, t1.due_date,  " + \
        "t1.documents, t1.completed_on, t1.completion_date, t1.approve_status, " + \
        "(select concat(unit_code,'-',unit_name,',',address,',',postal_code)" + \
        "from tbl_units where unit_id = t1.unit_id) as unit_name, t3.statutory_mapping, " + \
        "(select geography_name from tbl_units where unit_id = t1.unit_id) as geo_name, " + \
        "t3.compliance_task, (select frequency from tbl_compliance_frequency where " + \
        "frequency_id = t3.frequency_id) as frequency_name, (select " + \
        "concat(employee_code,'-',employee_name) from tbl_users where user_id = t1.completed_by) " + \
        "as assignee_name, t1.completed_by, t2.activity_on, t1.documents, t1.document_size, " + \
        "(select logo from tbl_legal_entities where legal_entity_id = t1.legal_entity_id) as logo, " + \
        "(select logo_size from tbl_legal_entities where legal_entity_id = t1.legal_entity_id) as logo_size "
    from_clause = "from tbl_compliance_history as t1 left join tbl_compliance_activity_log as t2 " + \
        "on t2.compliance_history_id = t1.compliance_history_id " + \
        "inner join tbl_compliances as t3 on t3.compliance_id = t1.compliance_id where "
    where_clause = "t3.country_id = %s and t3.domain_id = %s "
    condition_val.extend([country_id, domain_id])
    if request.statutory_mapping is not None:
        stat_map = '%' + stat_map + '%'
        where_clause = where_clause + "and t3.statutory_mapping like %s "
        condition_val.append(stat_map)

    frequency_id = request.frequency_id
    if int(request.frequency_id) > 0:
        where_clause = where_clause + "and t3.frequency_id = %s "
        condition_val.append(frequency_id)

    if user_type == "Assignee":
        if user_id == 0:
            where_clause = where_clause + \
                "and coalesce(t1.completed_by,'') like %s "
            condition_val.append('%')
        else:
            where_clause = where_clause + "and t1.completed_by = %s "
            condition_val.append(user_id)
    elif user_type == "Concurrence":
        if user_id == 0:
            where_clause = where_clause + \
                "and coalesce(t1.concurred_by,'') like %s "
            condition_val.append('%')
        else:
            where_clause = where_clause + "and t1.concurred_by = %s "
            condition_val.append(user_id)
    elif user_type == "Approval":
        if user_id == 0:
            where_clause = where_clause + \
                "and coalesce(t1.approved_by,'') like %s "
            condition_val.append('%')
        else:
            where_clause = where_clause + "and t1.approved_by = %s "
            condition_val.append(user_id)
    print task_status
    if task_status == "Complied":
        where_clause = where_clause + \
            "and t1.due_date > t1.completion_date and t1.approve_status = 1 "
    elif task_status == "Delayed Compliance":
        where_clause = where_clause + \
            "and t1.due_date < t1.completion_date and t1.approve_status = 1 "
    elif task_status == "Inprogress":
        where_clause = where_clause + "and t1.due_date > curdate() and t1.approve_status = 0 "
    elif task_status == "Not Complied":
        where_clause = where_clause + "and t1.due_date < curdate() and t1.approve_status = 0 "

    if due_from is not None and due_to is not None:
        due_from = string_to_datetime(due_from).date()
        due_to = string_to_datetime(due_to).date()
        where_clause = where_clause + " and t1.due_date >= " + \
            " date(%s)  and t1.due_date <= " + \
            " date(%s) "
        condition_val.extend([due_from, due_to])
    elif due_from is not None and due_to is None:
        due_from = string_to_datetime(due_from).date()
        where_clause = where_clause + " and t1.due_date >= " + \
            " date(%s)  and t1.due_date <= " + \
            " date(curdate()) "
        condition_val.append(due_from)
    elif due_from is None and due_to is not None:
        due_to = string_to_datetime(due_to).date()
        where_clause = where_clause + " and t1.due_date < " + \
            " DATE_ADD(%s, INTERVAL 1 DAY) "
        condition_val.append(due_to)

    compliance_id = request.compliance_id
    if int(compliance_id) > 0:
        where_clause = where_clause + "and t1.compliance_id = %s "
        condition_val.append(compliance_id)

    unit_id = request.unit_id
    if int(unit_id) > 0:
        where_clause = where_clause + "and t1.unit_id = %s "
        condition_val.append(unit_id)

    where_clause = where_clause + "and t1.legal_entity_id = %s order by t1.due_date, t2.compliance_activity_id desc limit %s, %s;"
    condition_val.extend([legal_entity_id, int(request.from_count), int(request.page_count)])
    query = select_qry + from_clause + where_clause
    print "qry"
    print condition_val
    print query
    result = db.select_all(query, condition_val)
    where_clause = None
    condition_val = []
    select_qry = "select t3.country_id, t1.legal_entity_id, t3.domain_id, t1.unit_id, t1.compliance_id, t1.due_date,  " + \
        "t1.documents, t1.completed_on, t1.completion_date, t1.approve_status, " + \
        "(select concat(unit_code,'-',unit_name,',',address,',',postal_code)" + \
        "from tbl_units where unit_id = t1.unit_id) as unit_name, t3.statutory_mapping, " + \
        "(select geography_name from tbl_units where unit_id = t1.unit_id) as geo_name, " + \
        "t3.compliance_task, (select frequency from tbl_compliance_frequency where " + \
        "frequency_id = t3.frequency_id) as frequency_name, (select " + \
        "concat(employee_code,'-',employee_name) from tbl_users where user_id = t1.completed_by) " + \
        "as assignee_name, t1.completed_by, t2.activity_on, t1.documents, t1.document_size, " + \
        "(select logo from tbl_legal_entities where legal_entity_id = t1.legal_entity_id) as logo, " + \
        "(select logo_size from tbl_legal_entities where legal_entity_id = t1.legal_entity_id) as logo_size "
    where_clause = "t3.country_id = %s and t3.domain_id = %s "
    condition_val.extend([country_id, domain_id])
    if request.statutory_mapping is not None:
        stat_map = '%'+stat_map+'%'
        where_clause = where_clause + "and t3.statutory_mapping like %s "
        condition_val.append(stat_map)

    frequency_id = request.frequency_id
    if int(request.frequency_id) > 0:
        where_clause = where_clause + "and t3.frequency_id = %s "
        condition_val.append(frequency_id)

    if user_type == "Assignee":
        if user_id == 0:
            where_clause = where_clause + "and coalesce(t1.completed_by,'') like %s "
            condition_val.append('%')
        else:
            where_clause = where_clause + "and t1.completed_by = %s "
            condition_val.append(user_id)
    elif user_type == "Concurrence":
        if user_id == 0:
            where_clause = where_clause + "and coalesce(t1.concurred_by,'') like %s "
            condition_val.append('%')
        else:
            where_clause = where_clause + "and t1.concurred_by = %s "
            condition_val.append(user_id)
    elif user_type == "Approval":
        if user_id == 0:
            where_clause = where_clause + "and coalesce(t1.approved_by,'') like %s "
            condition_val.append('%')
        else:
            where_clause = where_clause + "and t1.approved_by = %s "
            condition_val.append(user_id)

    if task_status == "Complied":
        where_clause = where_clause + "and t1.due_date > t1.completion_date and t1.approve_status = 1 "
    elif task_status == "Delayed Compliance":
        where_clause = where_clause + "and t1.due_date < t1.completion_date and t1.approve_status = 1 "
    elif task_status == "Inprogress":
        where_clause = where_clause + "and t1.due_date > curdate() and t1.approve_status = 0 "
    elif task_status == "Not Complied":
        where_clause = where_clause + "and t1.due_date < curdate() and t1.approve_status = 0 "

    if due_from is not None and due_to is not None:
        where_clause = where_clause + " and t1.due_date >= " + \
            " date(%s)  and t1.due_date <= " + \
            " date(%s) "
        condition_val.extend([due_from, due_to])
    elif due_from is not None and due_to is None:
        where_clause = where_clause + " and t1.due_date >= " + \
            " date(%s)  and t1.due_date <= " + \
            " date(curdate()) "
        condition_val.append(due_from)
    elif due_from is None and due_to is not None:
        where_clause = where_clause + " and t1.due_date < " + \
            " DATE_ADD(%s, INTERVAL 1 DAY) "
        condition_val.append(due_to)

    compliance_id = request.compliance_id
    if int(compliance_id) > 0:
        where_clause = where_clause + "and t1.compliance_id = %s "
        condition_val.append(compliance_id)

    unit_id = request.unit_id
    if int(unit_id) > 0:
        where_clause = where_clause + "and t1.unit_id = %s "
        condition_val.append(unit_id)

    where_clause = where_clause + "and t1.legal_entity_id = %s "
    condition_val.extend([legal_entity_id])
    query = select_qry + from_clause + where_clause
    count = db.select_all(query, condition_val)
    le_report = []
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

        # Find task status
        if (row["approve_status"] == 1):
            if (str(row["due_date"]) > str(row["completion_date"])):
                task_status = "Complied"
            else:
                task_status = "Delayed Compliance"
        else:
            if (str(row["due_date"]) > str(datetime.datetime.now())):
                task_status = "In Progress"
            else:
                task_status = "Not Complied"

        # Find Activity Status
        # print row["activity_date"]
        if row["activity_on"] is None:
            print row["approve_status"]
            if row["approve_status"] == "0" or row["approve_status"] is None:
                activity_status = "Pending"
            elif row["approve_status"] == "1":
                activity_status = "Approved"
            elif row["approve_status"] == "2":
                activity_status = "Rejected"
        else:
            activity_status = "Submitted"

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
        format_file = document_name
        # format_file_size = row["format_file_size"]
        format_file_size = row["document_size"]
        if format_file_size is not None:
            format_file_size = int(format_file_size)
        if format_file:
            url = "%s/%s" % (
                FORMAT_DOWNLOAD_URL, format_file
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

        le_report.append(clientreport.LegalEntityWiseReport(
            row["compliance_history_id"], row["compliance_activity_id"],
            row["country_id"], row["legal_entity_id"], row["domain_id"], row["unit_id"],
            row["compliance_id"], unit_name, statutory_mapping, row["compliance_task"],
            row["frequency_name"], datetime_to_string(row["due_date"]), task_status, row["assignee_name"],
            activity_status, datetime_to_string(row["activity_on"]), name,
            datetime_to_string(row["completion_date"]), url, logo_url
        ))
    return le_report, len(count)

##########################################################################
# Objective: To get the compliance list under filtered data
# Parameter: request object
# Result: list of compliance grouped by unit and act
##########################################################################


def process_domain_wise_report(db, request):
    # u_type = ("Assignee", "Concurrence", "Approval")
    # status = ("Complied", "Delayed Compliance", "Inprogress", "Not Complied")
    where_clause = None
    count_clause = None
    condition_val = []
    select_qry = None
    from_clause = None
    country_id = request.country_id
    legal_entity_id = request.legal_entity_id
    domain_id = request.domain_id

    stat_map = request.statutory_mapping

    user_type = request.user_type
    if user_type == 'All':
        user_type = '%'
    user_id = request.user_id

    due_from = request.due_from_date
    due_to = request.due_to_date
    task_status = request.task_status
    if task_status == "All":
        task_status = '%'

    select_qry = "select t1.compliance_history_id, t2.compliance_activity_id, t3.country_id, t1.legal_entity_id, t3.domain_id, t1.unit_id, t1.compliance_id, t1.due_date,  " + \
        "t1.documents, t1.completed_on, t1.completion_date, t1.approve_status, " + \
        "(select concat(unit_code,'-',unit_name,',',address,',',postal_code)" + \
        "from tbl_units where unit_id = t1.unit_id) as unit_name, t3.statutory_mapping, " + \
        "(select geography_name from tbl_units where unit_id = t1.unit_id) as geo_name, " + \
        "t3.compliance_task, (select frequency from tbl_compliance_frequency where " + \
        "frequency_id = t3.frequency_id) as frequency_name, (select " + \
        "concat(employee_code,'-',employee_name) from tbl_users where user_id = t1.completed_by) " + \
        "as assignee_name, t1.completed_by, t2.activity_on, t1.document_size, " + \
        "(select logo from tbl_legal_entities where legal_entity_id = t1.legal_entity_id) as logo, " + \
        "(select logo_size from tbl_legal_entities where legal_entity_id = t1.legal_entity_id) as logo_size "
    from_clause = "from tbl_compliance_history as t1 left join tbl_compliance_activity_log as t2 " + \
        "on t2.compliance_history_id = t1.compliance_history_id " + \
        "inner join tbl_compliances as t3 on t3.compliance_id = t1.compliance_id where "
    where_clause = "t3.country_id = %s and t3.domain_id = %s "
    condition_val.extend([country_id, domain_id])
    if request.statutory_mapping is not None:
        stat_map = '%' + stat_map + '%'
        where_clause = where_clause + "and t3.statutory_mapping like %s "
        condition_val.append(stat_map)

    frequency_id = request.frequency_id
    if int(request.frequency_id) > 0:
        where_clause = where_clause + "and t3.frequency_id = %s "
        condition_val.append(frequency_id)

    if user_type == "Assignee":
        if user_id == 0:
            where_clause = where_clause + \
                "and coalesce(t1.completed_by,'') like %s "
            condition_val.append('%')
        else:
            where_clause = where_clause + "and t1.completed_by = %s "
            condition_val.append(user_id)
    elif user_type == "Concurrence":
        if user_id == 0:
            where_clause = where_clause + \
                "and coalesce(t1.concurred_by,'') like %s "
            condition_val.append('%')
        else:
            where_clause = where_clause + "and t1.concurred_by = %s "
            condition_val.append(user_id)
    elif user_type == "Approval":
        if user_id == 0:
            where_clause = where_clause + \
                "and coalesce(t1.approved_by,'') like %s "
            condition_val.append('%')
        else:
            where_clause = where_clause + "and t1.approved_by = %s "
            condition_val.append(user_id)
    print task_status
    if task_status == "Complied":
        where_clause = where_clause + \
            "and t1.due_date > t1.completion_date and t1.approve_status = 1 "
    elif task_status == "Delayed Compliance":
        where_clause = where_clause + \
            "and t1.due_date < t1.completion_date and t1.approve_status = 1 "
    elif task_status == "Inprogress":
        where_clause = where_clause + "and t1.due_date > curdate() and t1.approve_status = 0 "
    elif task_status == "Not Complied":
        where_clause = where_clause + "and t1.due_date < curdate() and t1.approve_status = 0 "

    if due_from is not None and due_to is not None:
        due_from = string_to_datetime(due_from).date()
        due_to = string_to_datetime(due_to).date()
        where_clause = where_clause + " and t1.due_date >= " + \
            " date(%s)  and t1.due_date <= " + \
            " date(%s) "
        condition_val.extend([due_from, due_to])
    elif due_from is not None and due_to is None:
        due_from = string_to_datetime(due_from).date()
        where_clause = where_clause + " and t1.due_date >= " + \
            " date(%s)  and t1.due_date <= " + \
            " date(curdate()) "
        condition_val.append(due_from)
    elif due_from is None and due_to is not None:
        due_to = string_to_datetime(due_to).date()
        where_clause = where_clause + " and t1.due_date < " + \
            " DATE_ADD(%s, INTERVAL 1 DAY) "
        condition_val.append(due_to)

    compliance_id = request.compliance_id
    if int(compliance_id) > 0:
        where_clause = where_clause + "and t1.compliance_id = %s "
        condition_val.append(compliance_id)

    unit_id = request.unit_id
    if int(unit_id) > 0:
        where_clause = where_clause + "and t1.unit_id = %s "
        condition_val.append(unit_id)

    where_clause = where_clause + "and t1.legal_entity_id = %s order by t1.due_date desc, t2.compliance_activity_id limit %s, %s;"
    condition_val.extend([legal_entity_id, int(request.from_count), int(request.page_count)])
    query = select_qry + from_clause + where_clause
    print "qry"
    print condition_val
    print query
    result = db.select_all(query, condition_val)
    where_clause = None
    condition_val = []
    select_qry = "select t1.compliance_history_id, t2.compliance_activity_id, t3.country_id, t1.legal_entity_id, t3.domain_id, t1.unit_id, t1.compliance_id, t1.due_date,  " + \
        "t1.documents, t1.completed_on, t1.completion_date, t1.approve_status, " + \
        "(select concat(unit_code,'-',unit_name,',',address,',',postal_code)" + \
        "from tbl_units where unit_id = t1.unit_id) as unit_name, t3.statutory_mapping, " + \
        "(select geography_name from tbl_units where unit_id = t1.unit_id) as geo_name, " + \
        "t3.compliance_task, (select frequency from tbl_compliance_frequency where " + \
        "frequency_id = t3.frequency_id) as frequency_name, (select " + \
        "concat(employee_code,'-',employee_name) from tbl_users where user_id = t1.completed_by) " + \
        "as assignee_name, t1.completed_by, t2.activity_on, t1.document_size, " + \
        "(select logo from tbl_legal_entities where legal_entity_id = t1.legal_entity_id) as logo, " + \
        "(select logo_size from tbl_legal_entities where legal_entity_id = t1.legal_entity_id) as logo_size "
    where_clause = "t3.country_id = %s and t3.domain_id = %s "
    condition_val.extend([country_id, domain_id])
    if request.statutory_mapping is not None:
        stat_map = '%'+stat_map+'%'
        where_clause = where_clause + "and t3.statutory_mapping like %s "
        condition_val.append(stat_map)

    frequency_id = request.frequency_id
    if int(request.frequency_id) > 0:
        where_clause = where_clause + "and t3.frequency_id = %s "
        condition_val.append(frequency_id)

    if user_type == "Assignee":
        if user_id == 0:
            where_clause = where_clause + "and coalesce(t1.completed_by,'') like %s "
            condition_val.append('%')
        else:
            where_clause = where_clause + "and t1.completed_by = %s "
            condition_val.append(user_id)
    elif user_type == "Concurrence":
        if user_id == 0:
            where_clause = where_clause + "and coalesce(t1.concurred_by,'') like %s "
            condition_val.append('%')
        else:
            where_clause = where_clause + "and t1.concurred_by = %s "
            condition_val.append(user_id)
    elif user_type == "Approval":
        if user_id == 0:
            where_clause = where_clause + "and coalesce(t1.approved_by,'') like %s "
            condition_val.append('%')
        else:
            where_clause = where_clause + "and t1.approved_by = %s "
            condition_val.append(user_id)

    if task_status == "Complied":
        where_clause = where_clause + "and t1.due_date > t1.completion_date and t1.approve_status = 1 "
    elif task_status == "Delayed Compliance":
        where_clause = where_clause + "and t1.due_date < t1.completion_date and t1.approve_status = 1 "
    elif task_status == "Inprogress":
        where_clause = where_clause + "and t1.due_date > curdate() and t1.approve_status = 0 "
    elif task_status == "Not Complied":
        where_clause = where_clause + "and t1.due_date < curdate() and t1.approve_status = 0 "

    if due_from is not None and due_to is not None:
        where_clause = where_clause + " and t1.due_date >= " + \
            " date(%s)  and t1.due_date <= " + \
            " date(%s) "
        condition_val.extend([due_from, due_to])
    elif due_from is not None and due_to is None:
        where_clause = where_clause + " and t1.due_date >= " + \
            " date(%s)  and t1.due_date <= " + \
            " date(curdate()) "
        condition_val.append(due_from)
    elif due_from is None and due_to is not None:
        where_clause = where_clause + " and t1.due_date < " + \
            " DATE_ADD(%s, INTERVAL 1 DAY) "
        condition_val.append(due_to)

    compliance_id = request.compliance_id
    if int(compliance_id) > 0:
        where_clause = where_clause + "and t1.compliance_id = %s "
        condition_val.append(compliance_id)

    unit_id = request.unit_id
    if int(unit_id) > 0:
        where_clause = where_clause + "and t1.unit_id = %s "
        condition_val.append(unit_id)

    where_clause = where_clause + "and t1.legal_entity_id = %s"
    condition_val.extend([legal_entity_id])
    query = select_qry + from_clause + where_clause
    count = db.select_all(query, condition_val)
    le_report = []
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


        # Find task status
        if (row["approve_status"] == 1):
            if (str(row["due_date"]) > str(row["completion_date"])):
                task_status = "Complied"
            else:
                task_status = "Delayed Compliance"
        else:
            if (str(row["due_date"]) > str(datetime.datetime.now())):
                task_status = "In Progress"
            else:
                task_status = "Not Complied"

        # Find Activity Status
        # print row["activity_date"]
        if row["activity_on"] is None:
            print row["approve_status"]
            if row["approve_status"] == "0" or row["approve_status"] is None:
                activity_status = "Pending"
            elif row["approve_status"] == "1":
                activity_status = "Approved"
            elif row["approve_status"] == "2":
                activity_status = "Rejected"
        else:
            activity_status = "Submitted"

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
            url = "%s/%s" % (
                FORMAT_DOWNLOAD_URL, document_name
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

        le_report.append(clientreport.LegalEntityWiseReport(
            row["compliance_history_id"], row["compliance_activity_id"],
            row["country_id"], row["legal_entity_id"], row["domain_id"], row["unit_id"],
            row["compliance_id"], unit_name, statutory_mapping, row["compliance_task"],
            row["frequency_name"], datetime_to_string(row["due_date"]), task_status, row["assignee_name"],
            activity_status, datetime_to_string(row["activity_on"]), name,
            datetime_to_string(row["completion_date"]), url, logo_url
        ))
    return le_report, len(count)


##########################################################################
# Objective: To get the compliance list under filtered data
# Parameter: request object
# Result: list of compliance grouped by domain and act
##########################################################################
def process_unit_wise_report(db, request):
    where_clause = None
    condition_val = []
    select_qry = None
    from_clause = None
    country_id = request.country_id
    legal_entity_id = request.legal_entity_id
    domain_id = request.d_id_optional

    stat_map = request.statutory_mapping

    user_type = request.user_type
    if user_type == 'All':
        user_type = '%'
    user_id = request.user_id

    due_from = request.due_from_date
    due_to = request.due_to_date
    task_status = request.task_status
    if task_status == "All":
        task_status = '%'

    select_qry = "select t1.compliance_history_id, t2.compliance_activity_id, t3.country_id, t1.legal_entity_id, t3.domain_id, t1.unit_id, t1.compliance_id, t1.due_date,  " + \
        "t1.documents, t1.completed_on, t1.completion_date, t1.approve_status, " + \
        "(select concat(unit_code,'-',unit_name,',',address,',',postal_code)" + \
        "from tbl_units where unit_id = t1.unit_id) as unit_name, t3.statutory_mapping, " + \
        "(select geography_name from tbl_units where unit_id = t1.unit_id) as geo_name, " + \
        "t3.compliance_task, (select frequency from tbl_compliance_frequency where " + \
        "frequency_id = t3.frequency_id) as frequency_name, (select " + \
        "concat(employee_code,'-',employee_name) from tbl_users where user_id = t1.completed_by) " + \
        "as assignee_name, t1.completed_by, t2.activity_on, t1.document_size, " + \
        "(select domain_name from tbl_domains where domain_id = t3.domain_id) as domain_name, " + \
        "(select logo from tbl_legal_entities where legal_entity_id = t1.legal_entity_id) as logo, " + \
        "(select logo_size from tbl_legal_entities where legal_entity_id = t1.legal_entity_id) as logo_size "
    from_clause = "from tbl_compliance_history as t1 left join tbl_compliance_activity_log as t2 " + \
        "on t2.compliance_history_id = t1.compliance_history_id " + \
        "inner join tbl_compliances as t3 on t3.compliance_id = t1.compliance_id where "
    where_clause = "t3.country_id = %s "
    condition_val.append(country_id)

    if int(domain_id) > 0:
        where_clause = where_clause + "and t3.domain_id = %s "
        condition_val.append(domain_id)

    if request.statutory_mapping is not None:
        stat_map = '%' + stat_map + '%'
        where_clause = where_clause + "and t3.statutory_mapping like %s "
        condition_val.append(stat_map)

    frequency_id = request.frequency_id
    if int(request.frequency_id) > 0:
        where_clause = where_clause + "and t3.frequency_id = %s "
        condition_val.append(frequency_id)

    if user_type == "Assignee":
        if user_id == 0:
            where_clause = where_clause + \
                "and coalesce(t1.completed_by,'') like %s "
            condition_val.append('%')
        else:
            where_clause = where_clause + "and t1.completed_by = %s "
            condition_val.append(user_id)
    elif user_type == "Concurrence":
        if user_id == 0:
            where_clause = where_clause + \
                "and coalesce(t1.concurred_by,'') like %s "
            condition_val.append('%')
        else:
            where_clause = where_clause + "and t1.concurred_by = %s "
            condition_val.append(user_id)
    elif user_type == "Approval":
        if user_id == 0:
            where_clause = where_clause + \
                "and coalesce(t1.approved_by,'') like %s "
            condition_val.append('%')
        else:
            where_clause = where_clause + "and t1.approved_by = %s "
            condition_val.append(user_id)

    if task_status == "Complied":
        where_clause = where_clause + \
            "and t1.due_date > t1.completion_date and t1.approve_status = 1 "
    elif task_status == "Delayed Compliance":
        where_clause = where_clause + \
            "and t1.due_date < t1.completion_date and t1.approve_status = 1 "
    elif task_status == "Inprogress":
        where_clause = where_clause + "and t1.due_date > curdate() and t1.approve_status = 0 "
    elif task_status == "Not Complied":
        where_clause = where_clause + "and t1.due_date < curdate() and t1.approve_status = 0 "

    if due_from is not None and due_to is not None:
        due_from = string_to_datetime(due_from).date()
        due_to = string_to_datetime(due_to).date()
        where_clause = where_clause + " and t1.due_date >= " + \
            " date(%s)  and t1.due_date <= " + \
            " date(%s) "
        condition_val.extend([due_from, due_to])
    elif due_from is not None and due_to is None:
        due_from = string_to_datetime(due_from).date()
        where_clause = where_clause + " and t1.due_date >= " + \
            " date(%s)  and t1.due_date <= " + \
            " date(curdate()) "
        condition_val.append(due_from)
    elif due_from is None and due_to is not None:
        due_to = string_to_datetime(due_to).date()
        where_clause = where_clause + " and t1.due_date < " + \
            " DATE_ADD(%s, INTERVAL 1 DAY) "
        condition_val.append(due_to)

    compliance_id = request.compliance_id
    if int(compliance_id) > 0:
        where_clause = where_clause + "and t1.compliance_id = %s "
        condition_val.append(compliance_id)

    where_clause = where_clause + "and t1.legal_entity_id = %s and t1.unit_id = %s order by t1.due_date, t2.compliance_activity_id desc limit %s, %s;"
    condition_val.extend([legal_entity_id, request.unit_id, int(request.from_count), int(request.page_count)])
    query = select_qry + from_clause + where_clause
    print "qry"
    print query
    result = db.select_all(query, condition_val)

    where_clause = None
    condition_val = []
    select_qry = "select t1.compliance_history_id, t2.compliance_activity_id, t3.country_id, t1.legal_entity_id, t3.domain_id, t1.unit_id, t1.compliance_id, t1.due_date,  " + \
        "t1.documents, t1.completed_on, t1.completion_date, t1.approve_status, " + \
        "(select concat(unit_code,'-',unit_name,',',address,',',postal_code)" + \
        "from tbl_units where unit_id = t1.unit_id) as unit_name, t3.statutory_mapping, " + \
        "(select geography_name from tbl_units where unit_id = t1.unit_id) as geo_name, " + \
        "t3.compliance_task, (select frequency from tbl_compliance_frequency where " + \
        "frequency_id = t3.frequency_id) as frequency_name, (select " + \
        "concat(employee_code,'-',employee_name) from tbl_users where user_id = t1.completed_by) " + \
        "as assignee_name, t1.completed_by, t2.activity_on, t1.document_size, " + \
        "(select domain_name from tbl_domains where domain_id = t3.domain_id) as domain_name, " + \
        "(select logo from tbl_legal_entities where legal_entity_id = t1.legal_entity_id) as logo, " + \
        "(select logo_size from tbl_legal_entities where legal_entity_id = t1.legal_entity_id) as logo_size "
    where_clause = "t3.country_id = %s "
    condition_val.append(country_id)

    if int(domain_id) > 0:
        where_clause = where_clause + "and t3.domain_id = %s "
        condition_val.append(domain_id)

    if request.statutory_mapping is not None:
        stat_map = '%'+stat_map+'%'
        where_clause = where_clause + "and t3.statutory_mapping like %s "
        condition_val.append(stat_map)

    frequency_id = request.frequency_id
    if int(request.frequency_id) > 0:
        where_clause = where_clause + "and t3.frequency_id = %s "
        condition_val.append(frequency_id)

    if user_type == "Assignee":
        if user_id == 0:
            where_clause = where_clause + "and coalesce(t1.completed_by,'') like %s "
            condition_val.append('%')
        else:
            where_clause = where_clause + "and t1.completed_by = %s "
            condition_val.append(user_id)
    elif user_type == "Concurrence":
        if user_id == 0:
            where_clause = where_clause + "and coalesce(t1.concurred_by,'') like %s "
            condition_val.append('%')
        else:
            where_clause = where_clause + "and t1.concurred_by = %s "
            condition_val.append(user_id)
    elif user_type == "Approval":
        if user_id == 0:
            where_clause = where_clause + "and coalesce(t1.approved_by,'') like %s "
            condition_val.append('%')
        else:
            where_clause = where_clause + "and t1.approved_by = %s "
            condition_val.append(user_id)

    if task_status == "Complied":
        where_clause = where_clause + "and t1.due_date > t1.completion_date and t1.approve_status = 1 "
    elif task_status == "Delayed Compliance":
        where_clause = where_clause + "and t1.due_date < t1.completion_date and t1.approve_status = 1 "
    elif task_status == "Inprogress":
        where_clause = where_clause + "and t1.due_date > curdate() and t1.approve_status = 0 "
    elif task_status == "Not Complied":
        where_clause = where_clause + "and t1.due_date < curdate() and t1.approve_status = 0 "

    if due_from is not None and due_to is not None:
        where_clause = where_clause + " and t1.due_date >= " + \
            " date(%s)  and t1.due_date <= " + \
            " date(%s) "
        condition_val.extend([due_from, due_to])
    elif due_from is not None and due_to is None:
        where_clause = where_clause + " and t1.due_date >= " + \
            " date(%s)  and t1.due_date <= " + \
            " date(curdate()) "
        condition_val.append(due_from)
    elif due_from is None and due_to is not None:
        where_clause = where_clause + " and t1.due_date < " + \
            " DATE_ADD(%s, INTERVAL 1 DAY) "
        condition_val.append(due_to)

    compliance_id = request.compliance_id
    if int(compliance_id) > 0:
        where_clause = where_clause + "and t1.compliance_id = %s "
        condition_val.append(compliance_id)

    where_clause = where_clause + "and t1.legal_entity_id = %s and t1.unit_id = %s"
    condition_val.extend([legal_entity_id, request.unit_id])
    query = select_qry + from_clause + where_clause
    count = db.select_all(query, condition_val)

    unit_report = []
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

        # Find task status
        if (row["approve_status"] == 1):
            if (str(row["due_date"]) > str(row["completion_date"])):
                task_status = "Complied"
            else:
                task_status = "Delayed Compliance"
        else:
            if (str(row["due_date"]) > str(datetime.datetime.now())):
                task_status = "In Progress"
            else:
                task_status = "Not Complied"

        # Find Activity Status
        print row["activity_on"]
        if row["activity_on"] is None:
            print row["approve_status"]
            if row["approve_status"] == "0" or row["approve_status"] is None:
                activity_status = "Pending"
            elif row["approve_status"] == "1":
                activity_status = "Approved"
            elif row["approve_status"] == "2":
                activity_status = "Rejected"
        else:
            activity_status = "Submitted"

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
            url = "%s/%s" % (
                FORMAT_DOWNLOAD_URL, document_name
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

        unit_report.append(clientreport.UnitWiseReport(
            row["compliance_history_id"], row["compliance_activity_id"],
            row["country_id"], row["legal_entity_id"], row["domain_id"], row["unit_id"],
            row["compliance_id"], unit_name, statutory_mapping, row["compliance_task"],
            row["frequency_name"], datetime_to_string(row["due_date"]), task_status, row["assignee_name"],
            activity_status, datetime_to_string(row["activity_on"]), name,
            datetime_to_string(row["completion_date"]), url, row[
                "domain_name"], logo_url
        ))
    return unit_report, len(count)

##########################################################################
# Objective: To get the domains list with user id under selected legal entity
# Parameter: request object
# Result: list of domains and its users under the leagl entity selection
##########################################################################


def get_domains_for_sp_users(db, legal_entity_id):
    print "le"
    print legal_entity_id
    query = "select distinct(t2.user_id), t1.domain_id, (select domain_name from tbl_domains where " + \
            "domain_id = t2.domain_id) as domain_name, (select service_provider_id from tbl_users " +\
            "where user_id = t2.user_id) as sp_id_optional from tbl_legal_entity_domains as t1 " + \
            "inner join tbl_user_domains as t2 on t2.domain_id = t1.domain_id and " + \
            "t2.legal_entity_id = t1.legal_entity_id where t1.legal_entity_id = %s order by domain_name;"
    result = db.select_all(query, [legal_entity_id])
    print "domains"
    print result
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
    print "units"
    print result
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
            "where user_id = t1.approval_person) as sp_app_id_optional,t2.compliance_task " + \
            "from tbl_assign_compliances as t1 inner join tbl_compliances as t2 " + \
            "on t2.compliance_id = t1.compliance_id and t2.domain_id = t1.domain_id " + \
            "where t1.legal_entity_id = %s and t1.country_id = %s"
    result = db.select_all(query, [legal_entity_id, country_id])
    print "acts"
    print result
    print len(result)
    le_act_list = []
    for row in result:
        stat_map = json.loads(row["statutory_mapping"])
        if stat_map[0].find(">>") >= 0:
            stat_map = stat_map[0].split(">>")[0]
        else:
            stat_map = str(stat_map)[3:-2]
        print "mapped"
        print stat_map
        le_act_list.append(clientreport.ServiceProviderActList(
            row["legal_entity_id"], row["country_id"], row[
                "domain_id"], row["unit_id"],
            row["compliance_id"], row["assignee"], row["sp_ass_id_optional"],
            row["concurrence_person"], row[
                "sp_cc_id_optional"], row["approval_person"],
            row["sp_app_id_optional"], row[
                "compliance_task"], statutory_mapping=stat_map
        )
        )
    print len(le_act_list)
    return le_act_list

##########################################################################
# Objective: To get the lists of users under service provider
# Parameter: request object
# Result: list of users under service provider
##########################################################################


def get_service_provider_user_list(db, country_id, legal_entity_id):
    query = "select t1.domain_id, t1.unit_id, t1.compliance_id, t2.service_provider_id as sp_id, " + \
            "t2.user_id, concat(t2.employee_code,' - ',t2.employee_name) as username " + \
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

    select_qry = "select t1.compliance_history_id, t2.compliance_activity_id, t3.country_id, t1.legal_entity_id, t3.domain_id, t1.unit_id, t1.compliance_id, t1.due_date,  " + \
        "t1.documents, t1.completed_on, t1.completion_date, t1.approve_status, " + \
        "(select concat(unit_code,'-',unit_name,',',address,',',postal_code)" + \
        "from tbl_units where unit_id = t1.unit_id) as unit_name, t3.statutory_mapping, " + \
        "(select geography_name from tbl_units where unit_id = t1.unit_id) as geo_name, " + \
        "t3.compliance_task, (select frequency from tbl_compliance_frequency where " + \
        "frequency_id = t3.frequency_id) as frequency_name, (select " + \
        "concat(employee_code,'-',employee_name) from tbl_users where user_id = t1.completed_by) " + \
        "as assignee_name, t1.completed_by, t2.activity_on, t1.document_size, " + \
        "(select logo from tbl_legal_entities where legal_entity_id = t1.legal_entity_id) as logo, " + \
        "(select logo_size from tbl_legal_entities where legal_entity_id = t1.legal_entity_id) as logo_size "
    from_clause = "from tbl_users as t4 inner join tbl_compliance_history as t1 " + \
        "on (t1.completed_by=t4.user_id or t1.concurred_by=t4.user_id or t1.approved_by=t4.user_id) " + \
        "left join tbl_compliance_activity_log as t2 " + \
        "on t2.compliance_history_id = t1.compliance_history_id " + \
        "inner join tbl_compliances as t3 on t3.compliance_id = t1.compliance_id where "
    where_clause = "t3.country_id = %s and t3.domain_id = %s "
    condition_val.extend([country_id, domain_id])
    if request.statutory_mapping is not None:
        stat_map = '%' + stat_map + '%'
        where_clause = where_clause + "and t3.statutory_mapping like %s "
        condition_val.append(stat_map)

    if task_status == "Complied":
        where_clause = where_clause + \
            "and t1.due_date > t1.completion_date and t1.approve_status = 1 "
    elif task_status == "Delayed Compliance":
        where_clause = where_clause + \
            "and t1.due_date < t1.completion_date and t1.approve_status = 1 "
    elif task_status == "Inprogress":
        where_clause = where_clause + "and t1.due_date > curdate() and t1.approve_status = 0 "
    elif task_status == "Not Complied":
        where_clause = where_clause + "and t1.due_date < curdate() and t1.approve_status = 0 "

    if due_from is not None and due_to is not None:
        due_from = string_to_datetime(due_from).date()
        due_to = string_to_datetime(due_to).date()
        where_clause = where_clause + " and t1.due_date >= " + \
            " date(%s)  and t1.due_date <= " + \
            " date(%s) "
        condition_val.extend([due_from, due_to])
    elif due_from is not None and due_to is None:
        due_from = string_to_datetime(due_from).date()
        where_clause = where_clause + " and t1.due_date >= " + \
            " date(%s)  and t1.due_date <= " + \
            " date(curdate()) "
        condition_val.append(due_from)
    elif due_from is None and due_to is not None:
        due_to = string_to_datetime(due_to).date()
        where_clause = where_clause + " and t1.due_date < " + \
            " DATE_ADD(%s, INTERVAL 1 DAY) "
        condition_val.append(due_to)

    compliance_id = request.compliance_id
    if int(compliance_id) > 0:
        where_clause = where_clause + "and t1.compliance_id = %s "
        condition_val.append(compliance_id)

    unit_id = request.unit_id
    if int(unit_id) > 0:
        where_clause = where_clause + "and t1.unit_id = %s "
        condition_val.append(unit_id)

    user_id = request.user_id
    if int(user_id) > 0:
        where_clause = where_clause + "and t4.user_id = %s "
        condition_val.append(user_id)

    where_clause = where_clause + "and t4.service_provider_id = %s and t1.legal_entity_id = %s " + \
        "order by t1.due_date, t2.compliance_activity_id desc limit %s, %s;"
    condition_val.extend([sp_id, legal_entity_id, int(request.from_count), int(request.page_count)])
    query = select_qry + from_clause + where_clause
    print "qry"
    print query
    result = db.select_all(query, condition_val)

    where_clause = None
    condition_val = []
    select_qry = "select t3.country_id, t1.legal_entity_id, t3.domain_id, t1.unit_id, t1.compliance_id, t1.due_date,  " + \
        "t1.documents, t1.completed_on, t1.completion_date, t1.approve_status, " + \
        "(select concat(unit_code,'-',unit_name,',',address,',',postal_code)" + \
        "from tbl_units where unit_id = t1.unit_id) as unit_name, t3.statutory_mapping, " + \
        "(select geography_name from tbl_units where unit_id = t1.unit_id) as geo_name, " + \
        "t3.compliance_task, (select frequency from tbl_compliance_frequency where " + \
        "frequency_id = t3.frequency_id) as frequency_name, (select " + \
        "concat(employee_code,'-',employee_name) from tbl_users where user_id = t1.completed_by) " + \
        "as assignee_name, t1.completed_by, t2.activity_on, t1.document_size, " + \
        "(select logo from tbl_legal_entities where legal_entity_id = t1.legal_entity_id) as logo, " + \
        "(select logo_size from tbl_legal_entities where legal_entity_id = t1.legal_entity_id) as logo_size "
    where_clause = "t3.country_id = %s and t3.domain_id = %s "
    condition_val.extend([country_id, domain_id])
    if request.statutory_mapping is not None:
        stat_map = '%'+stat_map+'%'
        where_clause = where_clause + "and t3.statutory_mapping like %s "
        condition_val.append(stat_map)

    if task_status == "Complied":
        where_clause = where_clause + "and t1.due_date > t1.completion_date and t1.approve_status = 1 "
    elif task_status == "Delayed Compliance":
        where_clause = where_clause + "and t1.due_date < t1.completion_date and t1.approve_status = 1 "
    elif task_status == "Inprogress":
        where_clause = where_clause + "and t1.due_date > curdate() and t1.approve_status = 0 "
    elif task_status == "Not Complied":
        where_clause = where_clause + "and t1.due_date < curdate() and t1.approve_status = 0 "

    if due_from is not None and due_to is not None:
        where_clause = where_clause + " and t1.due_date >= " + \
            " date(%s)  and t1.due_date <= " + \
            " date(%s) "
        condition_val.extend([due_from, due_to])
    elif due_from is not None and due_to is None:
        where_clause = where_clause + " and t1.due_date >= " + \
            " date(%s)  and t1.due_date <= " + \
            " date(curdate()) "
        condition_val.append(due_from)
    elif due_from is None and due_to is not None:
        where_clause = where_clause + " and t1.due_date < " + \
            " DATE_ADD(%s, INTERVAL 1 DAY) "
        condition_val.append(due_to)

    compliance_id = request.compliance_id
    if int(compliance_id) > 0:
        where_clause = where_clause + "and t1.compliance_id = %s "
        condition_val.append(compliance_id)

    unit_id = request.unit_id
    if int(unit_id) > 0:
        where_clause = where_clause + "and t1.unit_id = %s "
        condition_val.append(unit_id)

    user_id = request.user_id
    if int(user_id) > 0:
        where_clause = where_clause + "and t4.user_id = %s "
        condition_val.append(user_id)

    where_clause = where_clause + "and t4.service_provider_id = %s and t1.legal_entity_id = %s " + \
        "order by t1.due_date, t2.compliance_activity_id desc;"
    condition_val.extend([sp_id, legal_entity_id])
    query = select_qry + from_clause + where_clause
    count = db.select_all(query, condition_val)

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

        # Find task status
        if (row["approve_status"] == 1):
            if (str(row["due_date"]) > str(row["completion_date"])):
                task_status = "Complied"
            else:
                task_status = "Delayed Compliance"
        else:
            if (str(row["due_date"]) > str(datetime.datetime.now())):
                task_status = "In Progress"
            else:
                task_status = "Not Complied"

        # Find Activity Status
        print row["activity_on"]
        if row["activity_on"] is None:
            print row["approve_status"]
            if row["approve_status"] == "0" or row["approve_status"] is None:
                activity_status = "Pending"
            elif row["approve_status"] == "1":
                activity_status = "Approved"
            elif row["approve_status"] == "2":
                activity_status = "Rejected"
        else:
            activity_status = "Submitted"

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
            url = "%s/%s" % (
                FORMAT_DOWNLOAD_URL, document_name
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
            row["frequency_name"], datetime_to_string(row["due_date"]), task_status, row["assignee_name"],
            activity_status, datetime_to_string(row["activity_on"]), name,
            datetime_to_string(row["completion_date"]), url, logo_url
        ))
    return sp_report, len(count)

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
    print "le"
    print legal_entity_id
    query = "select distinct(t2.user_id), t1.domain_id, (select domain_name from tbl_domains where " + \
            "domain_id = t2.domain_id) as domain_name from tbl_legal_entity_domains as t1 " + \
            "inner join tbl_user_domains as t2 on t2.domain_id = t1.domain_id and " + \
            "t2.legal_entity_id = t1.legal_entity_id where t1.legal_entity_id = %s order by domain_name;"
    result = db.select_all(query, [legal_entity_id])
    print "domains"
    print result
    user_domains_list = []
    for row in result:
        user_domains_list.append(clientreport.UserDomains(
            row["user_id"], row["domain_id"], row["domain_name"]
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
    print "units"
    print result
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
            "t2.statutory_mapping, t1.assignee, t1.concurrence_person, t1.approval_person, " + \
            "t2.compliance_task from tbl_assign_compliances as t1 inner join tbl_compliances as t2 " + \
            "on t2.compliance_id = t1.compliance_id and t2.domain_id = t1.domain_id " + \
            "where t1.legal_entity_id = %s and t1.country_id = %s"
    result = db.select_all(query, [legal_entity_id, country_id])
    print "acts"
    print result
    print len(result)
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
            row["approval_person"], row[
                "compliance_task"], statutory_mapping=stat_map
        )
        )
    print len(le_act_list)
    return le_act_list

##########################################################################
# Objective: To get the compliance list under filtered data
# Parameter: request object
# Result: list of compliance grouped by domain and act
##########################################################################


def process_user_wise_report(db, request):
    where_clause = None
    condition_val = []
    select_qry = None
    from_clause = None
    country_id = request.country_id
    legal_entity_id = request.legal_entity_id
    domain_id = request.domain_id

    stat_map = request.statutory_mapping

    user_type = request.user_type
    user_id = request.user_id

    due_from = request.due_from_date
    due_to = request.due_to_date
    task_status = request.task_status
    if task_status == "All":
        task_status = '%'

    select_qry = "select t1.compliance_history_id, t2.compliance_activity_id, t3.country_id, t1.legal_entity_id, t3.domain_id, t1.unit_id, t1.compliance_id, t1.due_date,  " + \
        "t1.documents, t1.completed_on, t1.completion_date, t1.approve_status, " + \
        "(select concat(unit_code,'-',unit_name,',',address,',',postal_code)" + \
        "from tbl_units where unit_id = t1.unit_id) as unit_name, t3.statutory_mapping, " + \
        "(select geography_name from tbl_units where unit_id = t1.unit_id) as geo_name, " + \
        "t3.compliance_task, (select frequency from tbl_compliance_frequency where " + \
        "frequency_id = t3.frequency_id) as frequency_name, (select " + \
        "concat(employee_code,'-',employee_name) from tbl_users where user_id = t1.completed_by) " + \
        "as assignee_name, t1.completed_by, t2.activity_on, t1.document_size, " + \
        "(select domain_name from tbl_domains where domain_id = t3.domain_id) as domain_name, " + \
        "(select logo from tbl_legal_entities where legal_entity_id = t1.legal_entity_id) as logo, " + \
        "(select logo_size from tbl_legal_entities where legal_entity_id = t1.legal_entity_id) as logo_size "
    from_clause = "from tbl_compliance_history as t1 left join tbl_compliance_activity_log as t2 " + \
        "on t2.compliance_history_id = t1.compliance_history_id " + \
        "inner join tbl_compliances as t3 on t3.compliance_id = t1.compliance_id where "
    where_clause = "t3.country_id = %s "
    condition_val.append(country_id)

    if int(domain_id) > 0:
        where_clause = where_clause + "and t3.domain_id = %s "
        condition_val.append(domain_id)

    if request.statutory_mapping is not None:
        stat_map = '%' + stat_map + '%'
        where_clause = where_clause + "and t3.statutory_mapping like %s "
        condition_val.append(stat_map)

    frequency_id = request.frequency_id
    if int(request.frequency_id) > 0:
        where_clause = where_clause + "and t3.frequency_id = %s "
        condition_val.append(frequency_id)
    print "u t"
    print user_type
    if user_type == "Assignee":
        where_clause = where_clause + "and t1.completed_by = %s "
        condition_val.append(user_id)
    elif user_type == "Concurrence":
        where_clause = where_clause + "and t1.concurred_by = %s "
        condition_val.append(user_id)
    elif user_type == "Approval":
        where_clause = where_clause + "and t1.approved_by = %s "
        condition_val.append(user_id)
    elif user_type == "All":
        where_clause = where_clause + \
            "and %s in (t1.completed_by, t1.concurred_by, t1.approved_by) "
        condition_val.append(user_id)

    if task_status == "Complied":
        where_clause = where_clause + \
            "and t1.due_date > t1.completion_date and t1.approve_status = 1 "
    elif task_status == "Delayed Compliance":
        where_clause = where_clause + \
            "and t1.due_date < t1.completion_date and t1.approve_status = 1 "
    elif task_status == "Inprogress":
        where_clause = where_clause + "and t1.due_date > curdate() and t1.approve_status = 0 "
    elif task_status == "Not Complied":
        where_clause = where_clause + "and t1.due_date < curdate() and t1.approve_status = 0 "

    if due_from is not None and due_to is not None:
        due_from = string_to_datetime(due_from).date()
        due_to = string_to_datetime(due_to).date()
        where_clause = where_clause + " and t1.due_date >= " + \
            " date(%s)  and t1.due_date <= " + \
            " date(%s) "
        condition_val.extend([due_from, due_to])
    elif due_from is not None and due_to is None:
        due_from = string_to_datetime(due_from).date()
        where_clause = where_clause + " and t1.due_date >= " + \
            " date(%s)  and t1.due_date <= " + \
            " date(curdate()) "
        condition_val.append(due_from)
    elif due_from is None and due_to is not None:
        due_to = string_to_datetime(due_to).date()
        where_clause = where_clause + " and t1.due_date < " + \
            " DATE_ADD(%s, INTERVAL 1 DAY) "
        condition_val.append(due_to)

    compliance_id = request.compliance_id
    if int(compliance_id) > 0:
        where_clause = where_clause + "and t1.compliance_id = %s "
        condition_val.append(compliance_id)

    unit_id = request.unit_id
    if int(unit_id) > 0:
        where_clause = where_clause + "and t1.unit_id = %s "
        condition_val.append(unit_id)
    where_clause = where_clause + "and t1.legal_entity_id = %s order by t1.due_date desc, t2.compliance_activity_id limit %s, %s;"
    condition_val.extend([legal_entity_id, int(request.from_count), int(request.page_count)])
    query = select_qry + from_clause + where_clause
    print "qry"
    print query
    result = db.select_all(query, condition_val)

    where_clause = None
    condition_val = []
    select_qry = "select t1.compliance_history_id, t2.compliance_activity_id, t3.country_id, t1.legal_entity_id, t3.domain_id, t1.unit_id, t1.compliance_id, t1.due_date,  " + \
        "t1.documents, t1.completed_on, t1.completion_date, t1.approve_status, " + \
        "(select concat(unit_code,'-',unit_name,',',address,',',postal_code)" + \
        "from tbl_units where unit_id = t1.unit_id) as unit_name, t3.statutory_mapping, " + \
        "(select geography_name from tbl_units where unit_id = t1.unit_id) as geo_name, " + \
        "t3.compliance_task, (select frequency from tbl_compliance_frequency where " + \
        "frequency_id = t3.frequency_id) as frequency_name, (select " + \
        "concat(employee_code,'-',employee_name) from tbl_users where user_id = t1.completed_by) " + \
        "as assignee_name, t1.completed_by, t2.activity_on, t1.document_size, " + \
        "(select domain_name from tbl_domains where domain_id = t3.domain_id) as domain_name, " + \
        "(select logo from tbl_legal_entities where legal_entity_id = t1.legal_entity_id) as logo, " + \
        "(select logo_size from tbl_legal_entities where legal_entity_id = t1.legal_entity_id) as logo_size "
    from_clause = "from tbl_compliance_history as t1 left join tbl_compliance_activity_log as t2 " + \
        "on t2.compliance_history_id = t1.compliance_history_id " + \
        "inner join tbl_compliances as t3 on t3.compliance_id = t1.compliance_id where "
    where_clause = "t3.country_id = %s "
    condition_val.append(country_id)

    if int(domain_id) > 0:
        where_clause = where_clause + "and t3.domain_id = %s "
        condition_val.append(domain_id)

    if request.statutory_mapping is not None:
        stat_map = '%'+stat_map+'%'
        where_clause = where_clause + "and t3.statutory_mapping like %s "
        condition_val.append(stat_map)

    frequency_id = request.frequency_id
    if int(request.frequency_id) > 0:
        where_clause = where_clause + "and t3.frequency_id = %s "
        condition_val.append(frequency_id)
    print "u t"
    print user_type
    if user_type == "Assignee":
        where_clause = where_clause + "and t1.completed_by = %s "
        condition_val.append(user_id)
    elif user_type == "Concurrence":
        where_clause = where_clause + "and t1.concurred_by = %s "
        condition_val.append(user_id)
    elif user_type == "Approval":
        where_clause = where_clause + "and t1.approved_by = %s "
        condition_val.append(user_id)
    elif user_type == "All":
        where_clause = where_clause + "and %s in (t1.completed_by, t1.concurred_by, t1.approved_by) "
        condition_val.append(user_id)

    if task_status == "Complied":
        where_clause = where_clause + "and t1.due_date > t1.completion_date and t1.approve_status = 1 "
    elif task_status == "Delayed Compliance":
        where_clause = where_clause + "and t1.due_date < t1.completion_date and t1.approve_status = 1 "
    elif task_status == "Inprogress":
        where_clause = where_clause + "and t1.due_date > curdate() and t1.approve_status = 0 "
    elif task_status == "Not Complied":
        where_clause = where_clause + "and t1.due_date < curdate() and t1.approve_status = 0 "

    if due_from is not None and due_to is not None:
        where_clause = where_clause + " and t1.due_date >= " + \
            " date(%s)  and t1.due_date <= " + \
            " date(%s) "
        condition_val.extend([due_from, due_to])
    elif due_from is not None and due_to is None:
        where_clause = where_clause + " and t1.due_date >= " + \
            " date(%s)  and t1.due_date <= " + \
            " date(curdate()) "
        condition_val.append(due_from)
    elif due_from is None and due_to is not None:
        where_clause = where_clause + " and t1.due_date < " + \
            " DATE_ADD(%s, INTERVAL 1 DAY) "
        condition_val.append(due_to)

    compliance_id = request.compliance_id
    if int(compliance_id) > 0:
        where_clause = where_clause + "and t1.compliance_id = %s "
        condition_val.append(compliance_id)

    unit_id = request.unit_id
    if int(unit_id) > 0:
        where_clause = where_clause + "and t1.unit_id = %s "
        condition_val.append(unit_id)

    where_clause = where_clause + "and t1.legal_entity_id = %s"
    condition_val.extend([legal_entity_id])
    query = select_qry + from_clause + where_clause
    print "qry"
    print query
    count = db.select_all(query, condition_val)

    user_report = []
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

        # Find task status
        if (row["approve_status"] == 1):
            if (str(row["due_date"]) > str(row["completion_date"])):
                task_status = "Complied"
            else:
                task_status = "Delayed Compliance"
        else:
            if (str(row["due_date"]) > str(datetime.datetime.now())):
                task_status = "In Progress"
            else:
                task_status = "Not Complied"

        # Find Activity Status
        print row["activity_on"]
        if row["activity_on"] is None:
            print row["approve_status"]
            if row["approve_status"] == "0" or row["approve_status"] is None:
                activity_status = "Pending"
            elif row["approve_status"] == "1":
                activity_status = "Approved"
            elif row["approve_status"] == "2":
                activity_status = "Rejected"
        else:
            activity_status = "Submitted"

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
            url = "%s/%s" % (
                FORMAT_DOWNLOAD_URL, document_name
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

        user_report.append(clientreport.UnitWiseReport(
            row["compliance_history_id"], row["compliance_activity_id"],
            row["country_id"], row["legal_entity_id"], row["domain_id"], row["unit_id"],
            row["compliance_id"], unit_name, statutory_mapping, row["compliance_task"],
            row["frequency_name"], datetime_to_string(row["due_date"]), task_status, row["assignee_name"],
            activity_status, datetime_to_string(row["activity_on"]), name,
            datetime_to_string(row["completion_date"]), url, row[
                "domain_name"], logo_url
        ))
    return user_report, len(count)

##########################################################################
# Objective: To get the divisions list under legal entity and business group
# Parameter: request object
# Result: list of divisions from master
##########################################################################


def get_divisions_for_unit_list(db, business_group_id, legal_entity_id):
    query = "select division_id, division_name from tbl_divisions " + \
        "where legal_entity_id = %s and business_group_id = %s"
    result = db.select_all(query, [legal_entity_id, business_group_id])
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
        "where legal_entity_id = %s and business_group_id = %s"
    result = db.select_all(query, [legal_entity_id, business_group_id])
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
        "tbl_units where business_group_id = %s and legal_entity_id =%s and country_id = %s"
    result = db.select_all(
        query, [business_group_id, legal_entity_id, country_id])

    query = "select t1.unit_id, t2.domain_id, t2.organisation_id " + \
        "from tbl_units as t1 inner join tbl_units_organizations as t2 on " + \
        "t2.unit_id = t1.unit_id where t1.business_group_id = %s and t1.legal_entity_id = %s and " + \
        "t1.country_id = %s group by t1.unit_id, t2.domain_id, t2.organisation_id order by " + \
        "t1.unit_id;"
    result_1 = db.select_all(
        query, [business_group_id, legal_entity_id, country_id])

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
    status = ("Active", "Closed")
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

    select_qry = "select t1.unit_id, t1.unit_code, t1.unit_name, t1.address, t1.postal_code, " + \
        "t1.geography_name, t1.is_closed, t1.closed_on, t1.division_id, t1.category_id, (select  " + \
        "division_name from tbl_divisions where division_id = t1.division_id) as division_name, " + \
        "(select category_name from tbl_categories where category_id = t1.category_id) as " + \
        "category_name, (select logo from tbl_legal_entities where legal_entity_id = t1.legal_entity_id) as logo, " + \
        "(select logo_size from tbl_legal_entities where legal_entity_id = t1.legal_entity_id) as logo_size " + \
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
        where_clause = where_clause + "and t1.is_closed = %s "
        condition_val.append(1)

    where_clause = where_clause + "order by t1.closed_on desc limit %s, %s;"
    condition_val.extend([int(request.from_count), int(request.page_count)])
    query = select_qry + where_clause
    print "qry"
    print query
    result = db.select_all(query, condition_val)

    where_clause = None
    condition_val = []
    select_qry = "select t1.unit_id, t1.unit_code, t1.unit_name, t1.address, t1.postal_code, " + \
        "t1.geography_name, t1.is_closed, t1.closed_on, t1.division_id, t1.category_id, (select  " + \
        "division_name from tbl_divisions where division_id = t1.division_id) as division_name, " + \
        "(select category_name from tbl_categories where category_id = t1.category_id) as " + \
        "category_name, (select logo from tbl_legal_entities where legal_entity_id = t1.legal_entity_id) as logo, " + \
        "(select logo_size from tbl_legal_entities where legal_entity_id = t1.legal_entity_id) as logo_size " + \
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
        where_clause = where_clause + "and t1.is_closed = %s "
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
        "organisation_name from tbl_units as t1 inner join tbl_units_organizations as t2 on " + \
        "t2.unit_id = t1.unit_id where "
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
        where_clause = where_clause + "and t1.is_closed = %s "
        condition_val.append(1)

    where_clause = where_clause + "order by t1.closed_on desc limit %s, %s;"
    condition_val.extend([int(request.from_count), int(request.page_count)])
    query = select_qry + where_clause
    print "qry"
    print query
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
        print row["is_closed"]
        if row["is_closed"] == 0:
            unit_status = "Active"
        else:
            unit_status = "Closed"
        d_i_names = []
        if row["closed_on"] is None:
            closed_date = datetime_to_string(row["closed_on"])
        else:
            closed_date = None

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

        last = object()
        for row_1 in result_1:
            if unit_id == row_1["unit_id"]:
                if last != (row_1["domain_name"] + " - " + row_1["organisation_name"]):
                    last = row_1["domain_name"] + \
                        " - " + row_1["organisation_name"]
                    d_i_names.append(
                        row_1["domain_name"] + " - " + row_1["organisation_name"])
        unit_report.append(clientreport.UnitListReport(
            unit_id, unit_code, unit_name, geography_name, address, postal_code,
            d_i_names, unit_status, closed_date, division_name, logo_url
        ))
    return unit_report, len(count)


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
        due_from = string_to_datetime(due_from).date()
        due_to = string_to_datetime(due_to).date()
        where_clause = where_clause + " and t3.created_on >= " + \
            " date(%s)  and t3.created_on <= " + \
            " date(%s) "
        condition_val.extend([due_from, due_to])
    elif due_from is not None and due_to is None:
        due_from = string_to_datetime(due_from).date()
        where_clause = where_clause + " and t3.created_on >= " + \
            " date(%s)  and t3.created_on <= " + \
            " date(curdate()) "
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
            " date(%s)  and t3.created_on <= " + \
            " date(%s) "
        condition_val.extend([due_from, due_to])
    elif due_from is not None and due_to is None:
        where_clause = where_clause + " and t3.created_on >= " + \
            " date(%s)  and t3.created_on <= " + \
            " date(curdate()) "
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
        statutory_notification.append(clientreport.StatutoryNotificationReport(
            row["compliance_id"], row["compliance_task"], row[
                "compliance_description"],
            datetime_to_string(row["created_on"]), row["notification_text"],
            statutory_mapping=stat_map
        ))
    return statutory_notification, len(count)

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

    select_qry = "select t1.user_id, t1.form_id, t1.action, t1.created_on, (select  " + \
        "employee_name from tbl_users where user_id " + \
        "= t1.user_id) as user_name, (select employee_code from tbl_users " + \
        "where user_id = t1.user_id) as emp_code, " + \
        "(select logo from tbl_legal_entities where legal_entity_id = t1.legal_entity_id) " + \
        "as logo, (select logo_size from tbl_legal_entities where legal_entity_id = t1.legal_entity_id) as logo_size " + \
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
        due_from = string_to_datetime(due_from).date()
        due_to = string_to_datetime(due_to).date()
        where_clause = where_clause + " and t1.created_on >= " + \
            " date(%s)  and t1.created_on <= " + \
            " date(%s) "
        condition_val.extend([due_from, due_to])
    elif due_from is not None and due_to is None:
        due_from = string_to_datetime(due_from).date()
        where_clause = where_clause + " and t1.created_on >= " + \
            " date(%s)  and t1.created_on <= " + \
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
    print "qry"
    print query
    result = db.select_all(query, condition_val)
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
            " date(%s)  and t1.created_on <= " + \
            " date(%s) "
        condition_val.extend([due_from, due_to])
    elif due_from is not None and due_to is None:
        where_clause = where_clause + " and t1.created_on >= " + \
            " date(%s)  and t1.created_on <= " + \
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
    compliance_id = request.compliance_id
    task_status = request.task_status
    print(task_status == "All" or task_status == "Unassigned Compliance")
    condition_val = []
    total_record = 0
    print "other"
    if task_status == "All":
        print task_status
        # All or unassigned compliance
        union_qry = "select t2.statutory_mapping, (select concat(unit_code,'-',unit_name,',', " + \
            "address,',',postal_code) from tbl_units where unit_id = t1.unit_id) as unit_name, t2.compliance_task, " + \
            "(select frequency from tbl_compliance_frequency where frequency_id = t2.frequency_id) as frequency_name, " + \
            "t2.penal_consequences, t2.format_file, t2.format_file_size, " + \
            "(select geography_name from tbl_units where unit_id = t1.unit_id) as geo_name, " + \
            "(select logo from tbl_legal_entities where legal_entity_id = t1.legal_entity_id) as logo, " + \
            "(select logo_size from tbl_legal_entities where legal_entity_id = t1.legal_entity_id) as logo_size "
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

        compliance_id = request.compliance_id
        if int(compliance_id) > 0:
            union_where_clause = union_where_clause + "and t1.compliance_id = %s "
            condition_val.append(compliance_id)

        unit_id = request.unit_id
        if int(unit_id) > 0:
            union_where_clause = union_where_clause + "and t1.unit_id = %s "
            condition_val.append(unit_id)

        union_where_clause = union_where_clause + "and t1.legal_entity_id = %s and t1.compliance_id not in " + \
            "(select compliance_id from tbl_assign_compliances) order by t2.compliance_task asc limit %s, %s"
        condition_val.extend([legal_entity_id, request.from_count, request.page_count])

        query = union_qry + union_from_clause + union_where_clause
        print "qry1"
        print query
        result_1 = db.select_all(query, condition_val)
        condition_val = []
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

        compliance_id = request.compliance_id
        if int(compliance_id) > 0:
            union_where_clause = union_where_clause + "and t1.compliance_id = %s "
            condition_val.append(compliance_id)

        unit_id = request.unit_id
        if int(unit_id) > 0:
            union_where_clause = union_where_clause + "and t1.unit_id = %s "
            condition_val.append(unit_id)

        union_where_clause = union_where_clause + "and t1.legal_entity_id = %s and t1.compliance_id not in " + \
            "(select compliance_id from tbl_assign_compliances) order by t2.compliance_task asc"
        condition_val.extend([legal_entity_id])
        query = union_qry + union_from_clause + union_where_clause
        count = db.select_all(query, condition_val)
        total_record = len(count)
        print result_1
        risk_report = []
        j = 1
        for row in result_1:
            if (j <= int(request.page_count)):
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
                    url = "%s/%s" % (
                        FORMAT_DOWNLOAD_URL, format_file
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
                    None, None, None, None, None, comp_remarks=None
                ))
                j = j + 1
        print len(risk_report)
        condition_val = []
        j = 1
        # other compliance
        select_qry = "select t3.statutory_mapping, (select concat(unit_code,'-',unit_name,',', " + \
            "address,',',postal_code) from tbl_units where unit_id = t1.unit_id) as unit_name, t3.compliance_task, " + \
            "(select frequency from tbl_compliance_frequency where frequency_id = t3.frequency_id) as frequency_name, " + \
            "(select geography_name from tbl_units where unit_id = t1.unit_id) as geo_name, " + \
            "(select employee_name from tbl_users where user_id = t6.assigned_by) as " + \
            "admin_incharge, (select employee_name from tbl_users where user_id = " + \
            "t1.completed_by) as assignee_name, t3.penal_consequences, t1.documents, t1.document_size, " + \
            "(select logo from tbl_legal_entities where legal_entity_id = t1.legal_entity_id) as logo, " + \
            "(select logo_size from tbl_legal_entities where legal_entity_id = t1.legal_entity_id) as logo_size, " + \
            "t1.completion_date, t1.due_date, t1.approve_status, t5.compliance_opted_status, t1.start_date, " + \
            "t1.due_date, (select concat(employee_code,'-',employee_name) from tbl_users where user_id = " + \
            "t1.concurred_by) as concurrer_name, (select concat(employee_code,'-',employee_name) from tbl_users " + \
            "where user_id = t1.approved_by) as approver_name, t1.remarks, t1.documents, t1.completed_on as " + \
            "assigned_on, t1.concurred_on, t1.approved_on "

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
            where_clause = where_clause + \
                "and t1.due_date < t1.completion_date and t1.approve_status = 1 "
        elif task_status == "Not Complied":
            where_clause = where_clause + "and t1.due_date < curdate() and t1.approve_status <> 0  " + \
                "and t1.approve_status <> 1 "

        compliance_id = request.compliance_id
        if int(compliance_id) > 0:
            where_clause = where_clause + "and t1.compliance_id = %s "
            condition_val.append(compliance_id)

        unit_id = request.unit_id
        if int(unit_id) > 0:
            where_clause = where_clause + "and t1.unit_id = %s "
            condition_val.append(unit_id)

        where_clause = where_clause + \
            "and t1.legal_entity_id = %s group by t1.compliance_history_id order by t3.compliance_task asc limit %s, %s;"
        condition_val.extend([legal_entity_id, request.from_count, request.page_count])

        query = select_qry + from_clause + where_clause
        print "qry"
        print query

        result = db.select_all(query, condition_val)

        # total_record
        condition_val = []
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
            where_clause = where_clause + \
                "and t1.due_date < t1.completion_date and t1.approve_status = 1 "
        elif task_status == "Not Complied":
            where_clause = where_clause + "and t1.due_date < curdate() and t1.approve_status <> 0  " + \
                "and t1.approve_status <> 1 "

        compliance_id = request.compliance_id
        if int(compliance_id) > 0:
            where_clause = where_clause + "and t1.compliance_id = %s "
            condition_val.append(compliance_id)

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
        print result
        j = 1
        for row in result:
            if (j <= int(request.page_count)):
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

                # Find task status
                if row["compliance_opted_status"] == 0:
                    task_status = "Not Opted"
                elif (str(row["due_date"]) < str(datetime.datetime.now())) and row["approve_status"] != 0:
                    task_status = "Not Complied"
                elif (str(row["due_date"]) < str(row["completion_date"])) and row["approve_status"] != 1 and row["approve_status"] != 0:
                    task_status = "Delayed Compliance"
                elif row["compliance_opted_status"] == 0 and row["approve_status"] == 3:
                    task_status = "Not Opted - Rejected"

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
                    url = "%s/%s" % (
                        FORMAT_DOWNLOAD_URL, format_file
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
                    row["penal_consequences"], row["admin_incharge"], row[
                        "assignee_name"], task_status,
                    name, url, logo_url, datetime_to_string_time(
                        row["start_date"]),
                    datetime_to_string_time(row["due_date"]), row[
                        "concurrer_name"], row["approver_name"],
                    datetime_to_string_time(row["assigned_on"]), datetime_to_string_time(
                        row["concurred_on"]),
                    datetime_to_string_time(row["approved_on"]), comp_remarks=row["remarks"]
                ))
                j = j + 1
        print len(risk_report)
    elif task_status == "Unassigned Compliance":
        j = 1
        print task_status
        # All or unassigned compliance
        union_qry = "select t2.statutory_mapping, (select concat(unit_code,'-',unit_name,',', " + \
            "address,',',postal_code) from tbl_units where unit_id = t1.unit_id) as unit_name, t2.compliance_task, " + \
            "(select frequency from tbl_compliance_frequency where frequency_id = t2.frequency_id) as frequency_name, " + \
            "(select geography_name from tbl_units where unit_id = t1.unit_id) as geo_name, " + \
            "t2.penal_consequences, t2.format_file, t2.format_file_size, " + \
            "(select logo from tbl_legal_entities where legal_entity_id = t1.legal_entity_id) as logo, " + \
            "(select logo_size from tbl_legal_entities where legal_entity_id = t1.legal_entity_id) as logo_size "
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

        compliance_id = request.compliance_id
        if int(compliance_id) > 0:
            union_where_clause = union_where_clause + "and t1.compliance_id = %s "
            condition_val.append(compliance_id)

        unit_id = request.unit_id
        if int(unit_id) > 0:
            union_where_clause = union_where_clause + "and t1.unit_id = %s "
            condition_val.append(unit_id)

        union_where_clause = union_where_clause + "and t1.legal_entity_id = %s and t1.compliance_id not in " + \
            "(select compliance_id from tbl_assign_compliances) order by t2.compliance_task asc;"
        condition_val.extend([legal_entity_id])

        query = union_qry + union_from_clause + union_where_clause
        print "qry1"
        print query
        result_1 = db.select_all(query, condition_val)

        # total
        condition_val = []
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

        compliance_id = request.compliance_id
        if int(compliance_id) > 0:
            union_where_clause = union_where_clause + "and t1.compliance_id = %s "
            condition_val.append(compliance_id)

        unit_id = request.unit_id
        if int(unit_id) > 0:
            union_where_clause = union_where_clause + "and t1.unit_id = %s "
            condition_val.append(unit_id)

        union_where_clause = union_where_clause + "and t1.legal_entity_id = %s and t1.compliance_id not in " + \
            "(select compliance_id from tbl_assign_compliances) order by t2.compliance_task asc"
        condition_val.extend([legal_entity_id])
        query = union_qry + union_from_clause + union_where_clause
        count = db.select_all(query, condition_val)
        total_record = len(count)

        risk_report = []

        for row in result_1:
            if (j <= int(request.page_count)):
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
                    url = "%s/%s" % (
                        FORMAT_DOWNLOAD_URL, format_file
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
                    None, None, None, None, None, comp_remarks=None
                ))
                j = j + 1
        print len(risk_report)
        condition_val = []
        j = 1
        print len(risk_report)
    elif (task_status != "All" or task_status != "Unassigned Compliance"):
        print "a"
        condition_val = []
        # other compliance
        select_qry = "select t3.statutory_mapping, (select concat(unit_code,'-',unit_name,',', " + \
            "address,',',postal_code) from tbl_units where unit_id = t1.unit_id) as unit_name, t3.compliance_task, " + \
            "(select frequency from tbl_compliance_frequency where frequency_id = t3.frequency_id) as frequency_name, " + \
            "(select geography_name from tbl_units where unit_id = t1.unit_id) as geo_name, " + \
            "(select employee_name from tbl_users where user_id = t6.assigned_by) as " + \
            "admin_incharge, (select employee_name from tbl_users where user_id = " + \
            "t1.completed_by) as assignee_name, t3.penal_consequences, t1.documents, t1.document_size, " + \
            "(select logo from tbl_legal_entities where legal_entity_id = t1.legal_entity_id) as logo, " + \
            "(select logo_size from tbl_legal_entities where legal_entity_id = t1.legal_entity_id) as logo_size, " + \
            "t1.completion_date, t1.due_date, t1.approve_status, t5.compliance_opted_status, t1.start_date, " + \
            "t1.due_date, (select concat(employee_code,'-',employee_name) from tbl_users where user_id = " + \
            "t1.concurred_by) as concurrer_name, (select concat(employee_code,'-',employee_name) from tbl_users " + \
            "where user_id = t1.approved_by) as approver_name, t1.remarks, t1.documents, t1.completed_on as " + \
            "assigned_on, t1.concurred_on, t1.approved_on "

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
            where_clause = where_clause + \
                "and t1.due_date < t1.completion_date and t1.approve_status = 1 "
        elif task_status == "Not Complied":
            where_clause = where_clause + "and t1.due_date < curdate() and t1.approve_status <> 0  " + \
                "and t1.approve_status <> 1 "

        compliance_id = request.compliance_id
        if int(compliance_id) > 0:
            where_clause = where_clause + "and t1.compliance_id = %s "
            condition_val.append(compliance_id)

        unit_id = request.unit_id
        if int(unit_id) > 0:
            where_clause = where_clause + "and t1.unit_id = %s "
            condition_val.append(unit_id)

        where_clause = where_clause + \
            "and t1.legal_entity_id = %s group by t1.compliance_history_id order by t3.compliance_task asc;"
        condition_val.extend([legal_entity_id])

        query = select_qry + from_clause + where_clause
        print "qry"
        print query

        result = db.select_all(query, condition_val)

        # total_record
        condition_val = []
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
            where_clause = where_clause + \
                "and t1.due_date < t1.completion_date and t1.approve_status = 1 "
        elif task_status == "Not Complied":
            where_clause = where_clause + "and t1.due_date < curdate() and t1.approve_status <> 0  " + \
                "and t1.approve_status <> 1 "

        compliance_id = request.compliance_id
        if int(compliance_id) > 0:
            where_clause = where_clause + "and t1.compliance_id = %s "
            condition_val.append(compliance_id)

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

        risk_report = []

        for row in result:
            if (j <= int(request.page_count)):
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

                # Find task status
                if row["compliance_opted_status"] == 0:
                    task_status = "Not Opted"
                elif (str(row["due_date"]) < str(datetime.datetime.now())) and row["approve_status"] != 0:
                    task_status = "Not Complied"
                elif (str(row["due_date"]) < str(row["completion_date"])) and row["approve_status"] != 1 and row["approve_status"] != 0:
                    task_status = "Delayed Compliance"
                elif row["compliance_opted_status"] == 0 and row["approve_status"] == 3:
                    task_status = "Not Opted - Rejected"

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
                    url = "%s/%s" % (
                        FORMAT_DOWNLOAD_URL, document_name
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
                    row["penal_consequences"], row["admin_incharge"], row[
                        "assignee_name"], task_status,
                    name, url, logo_url, datetime_to_string_time(
                        row["start_date"]),
                    datetime_to_string_time(row["due_date"]), row[
                        "concurrer_name"], row["approver_name"],
                    datetime_to_string_time(row["assigned_on"]), datetime_to_string_time(
                        row["concurred_on"]),
                    datetime_to_string_time(row["approved_on"]), comp_remarks=row["remarks"]
                ))
                j = j + 1
    print len(risk_report)
    return risk_report, total_record
