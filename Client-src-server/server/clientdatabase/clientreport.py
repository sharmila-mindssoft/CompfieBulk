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
    "report_unitwise_compliance",
    "return_unitwise_report",
    "report_assigneewise_compliance",
    "return_assignee_report_data",
    "report_serviceproviderwise_compliance",
    "return_serviceprovider_report_data",
    "report_statutory_notifications_list",
    "report_compliance_details",
    "get_delayed_compliances_with_count",
    "get_delayed_compliances_where_qry",
    "get_delayed_compliances_count",
    "get_delayed_compliances",
    "get_not_complied_where_qry",
    "get_not_complied_compliances_count",
    "get_not_complied_compliances",
    "get_not_complied_compliances_with_count",
    "get_not_opted_compliances_where_qry",
    "get_not_opted_compliances_count",
    "get_not_opted_compliances",
    "get_not_opted_compliances_with_count",
    "get_unassigned_compliances_where_qry",
    "get_unassigned_compliances_count",
    "get_unassigned_compliances",
    "get_unassigned_compliances_with_count",
    "get_login_trace",
    "return_compliance_activity_report",
    "get_compliance_task_applicability",
    "get_client_details_count",
    "get_client_details_report",
    "get_compliance_activity_report",
    "get_where_query_for_compliance_details_report",
    "get_compliance_details_total_count",
    "get_compliance_details",
    "get_client_details_condition",
    "get_service_provider_user_ids",
    "get_service_provider_user_unit_ids",
    "return_cmopliance_details_report",
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


def report_unitwise_compliance(
    db, country_id, domain_id, business_group_id,
    legal_entity_id, division_id, unit_id, assignee,
    session_user, from_count, page_count
):
    data, total = report_assigneewise_compliance(
        db, country_id, domain_id, business_group_id,
        legal_entity_id, division_id, unit_id, assignee,
        session_user, from_count, page_count
    )
    return data, total


# assigneewise compliance report
def report_assigneewise_compliance(
    db, country_id, domain_id, business_group_id,
    legal_entity_id, division_id, unit_id, assignee,
    session_user, from_count, page_count
):
    columns = [
        "country_id", "unit_id", "compliance_id", "statutory_dates",
        "trigger_before_days", "due_date", "validity_date",
        "compliance_task", "document_name", "description", "frequency_id",
        "assignee_name", "concurrence_name", "approval_name",
        "assignee", "concurrance", "approval",
        "business_group", "legal_entity", "division",
        "unit_code", "unit_name", "frequency",
        "duration_type", "repeat_type", "duration",
        "repeat_every"
    ]
    qry_where = ""
    qry_where_val = []
    admin_id = get_admin_id(db)

    if business_group_id is not None:
        qry_where += " AND u.business_group_id = %s "
        qry_where_val.append(business_group_id)

    if legal_entity_id is not None:
        qry_where += " AND u.legal_entity_id = %s "
        qry_where_val.append(legal_entity_id)

    if division_id is not None:
        qry_where += " AND u.division_id = %s "
        qry_where_val.append(division_id)

    if unit_id is not None:
        qry_where += " AND u.unit_id = %s"
        qry_where_val.append(unit_id)

    if assignee is not None:
        qry_where += " AND ac.assignee = %s"
        qry_where_val.append(assignee)

    if session_user != admin_id:
        qry_where += " AND u.unit_id in " + \
            " (select us.unit_id from tbl_user_units us where " + \
            " us.user_id = %s )"
        qry_where_val.append(session_user)

    q_count = " SELECT  " + \
        " count(ac.compliance_id) " + \
        " FROM tbl_assigned_compliances ac " + \
        " INNER JOIN tbl_units u on ac.unit_id = u.unit_id " + \
        " INNER JOIN tbl_compliances c " + \
        " on ac.compliance_id = c.compliance_id " + \
        " WHERE c.is_active = 1 " + \
        " and ac.country_id = %s and c.domain_id = %s "
    param = [country_id, domain_id]
    if qry_where is not None:
        q_count += qry_where
        param.extend(qry_where_val)

    row = db.select_one(q_count, param)

    if row:
        count = row[0]
    else:
        count = 0

    q = "SELECT " + \
        " ac.country_id, ac.unit_id, ac.compliance_id, " + \
        " ac.statutory_dates, " + \
        " ac. trigger_before_days, ac.due_date, ac.validity_date, " + \
        " c.compliance_task, c.document_name, " + \
        " c.compliance_description, c.frequency_id, " + \
        " IFNULL((select concat(a.employee_code, ' - ', a.employee_name) " + \
        " from tbl_users a " + \
        " where a.user_id = ac.assignee " + \
        " ), 'Administrator') assignee_name, " + \
        " (select concat(a.employee_code, ' - ', a.employee_name) " + \
        " from tbl_users a  " + \
        " where a.user_id = ac.concurrence_person )" + \
        " concurrence_name, " + \
        " IFNULL((select concat(a.employee_code, ' - ', a.employee_name) " + \
        " from tbl_users a  " + \
        " where a.user_id = ac.approval_person), " + \
        " 'Administrator') approval_name,  " + \
        " ac.assignee, ac.concurrence_person, ac.approval_person, " + \
        " (select b.business_group_name from tbl_business_groups b " + \
        " where b.business_group_id = u.business_group_id " + \
        " )business_group_name, " + \
        " (select l.legal_entity_name from tbl_legal_entities l " + \
        " where l.legal_entity_id = u.legal_entity_id " + \
        " )legal_entity_name, " + \
        " (select d.division_name from tbl_divisions d " + \
        " where d.division_id = u.division_id " + \
        " )business_group_name, " + \
        " u.unit_code, u.unit_name, " + \
        " (select f.frequency from tbl_compliance_frequency f " + \
        " where f.frequency_id = c.frequency_id) frequency, " + \
        " (select duration_type from tbl_compliance_duration_type " + \
        " where duration_type_id = c.duration_type_id) AS duration_type, " + \
        " (select repeat_type from tbl_compliance_repeat_type " + \
        " where repeat_type_id = c.repeats_type_id) AS repeat_type, " +  \
        " c.duration, c.repeats_every  " + \
        " FROM tbl_assigned_compliances ac " + \
        " INNER JOIN tbl_units u on ac.unit_id = u.unit_id " + \
        " INNER JOIN tbl_compliances c " + \
        " on ac.compliance_id = c.compliance_id " + \
        " WHERE c.is_active = 1 " + \
        " and ac.country_id = %s and c.domain_id = %s "
    order = " ORDER BY u.legal_entity_id, ac.assignee, u.unit_id " + \
        " limit %s, %s"

    param = [country_id, domain_id]
    if qry_where is not None:
        q += qry_where
        param.extend(qry_where_val)

    param.extend([from_count, page_count])
    rows = db.select_all("%s %s" % (q, order), param)

    data = convert_to_dict(rows, columns)
    return data, count


def return_unitwise_report(data):
    legal_wise = {}
    for d in data:
        statutory_dates = json.loads(d["statutory_dates"])
        date_list = []
        for date in statutory_dates:
            s_date = clientcore.StatutoryDate(
                date["statutory_date"],
                date["statutory_month"],
                date["trigger_before_days"],
                date.get("repeat_by")
            )
            date_list.append(s_date)

        compliance_frequency = clientcore.COMPLIANCE_FREQUENCY(
            d["frequency"]
        )

        due_date = None
        if(d["due_date"] is not None):
            due_date = datetime_to_string(d["due_date"])

        validity_date = None
        if(d["validity_date"] is not None):
            validity_date = datetime_to_string(d["validity_date"])

        if d["frequency_id"] in (2, 3):
            summary = "Repeats every %s - %s" % (
                d["repeat_every"], d["repeat_type"]
            )
        elif d["frequency_id"] == 4:
            summary = "To complete within %s - %s" % (
                d["duration"], d["duration_type"]
            )
        else:
            summary = None

        if d["document_name"] in ["None", None, ""]:
            name = d["compliance_task"]
        else:
            name = d["document_name"] + " - " + d["compliance_task"]
        uname = d["unit_code"] + " - " + d["unit_name"]
        compliance = clientreport.ComplianceUnit(
            name, uname,
            compliance_frequency, d["description"],
            date_list, due_date, validity_date,
            summary
        )

        group_by_legal = legal_wise.get(d["legal_entity"])
        if group_by_legal is None:
            unit_wise = {}
            unit_wise[uname] = [compliance]
            AC = clientreport.UnitCompliance(
                d["business_group"], d["legal_entity"],
                d["division"], unit_wise
            )
            AC.to_structure()
            legal_wise[d["legal_entity"]] = AC
        else:
            unit_wise_list = group_by_legal.unit_wise_compliances
            if unit_wise_list is None:
                unit_wise_list = {}
                unit_wise_list[uname] = [compliance]
            else:
                lst = unit_wise_list.get(uname)
                if lst is None:
                    lst = []
                lst.append(compliance)
                unit_wise_list[uname] = lst

            group_by_legal.unit_wise_compliances = unit_wise_list
            legal_wise[d["legal_entity"]] = group_by_legal
    return legal_wise.values()


def return_assignee_report_data(data):
    legal_wise = {}
    for d in data:
        statutory_dates = json.loads(d["statutory_dates"])
        date_list = []
        for date in statutory_dates:
            s_date = clientcore.StatutoryDate(
                date["statutory_date"],
                date["statutory_month"],
                date["trigger_before_days"],
                date.get("repeat_by")
            )
            date_list.append(s_date)

        compliance_frequency = clientcore.COMPLIANCE_FREQUENCY(
            d["frequency"]
        )

        due_date = None
        if(d["due_date"] is not None):
            due_date = datetime_to_string(d["due_date"])

        validity_date = None
        if(d["validity_date"] is not None):
            validity_date = datetime_to_string(d["validity_date"])

        if d["frequency_id"] in (2, 3):
            summary = "Repeats every %s - %s" % (
                d["repeat_every"], d["repeat_type"]
            )
        elif d["frequency_id"] == 4:
            summary = "To complete within %s - %s" % (
                d["duration"], d["duration_type"]
            )
        else:
            summary = None

        if d["document_name"] in ["None", None, ""]:
            name = d["compliance_task"]
        else:
            name = d["document_name"] + " - " + d["compliance_task"]
        compliance = clientreport.ComplianceUnit(
            name, d["unit_code"] + " - " + d["unit_name"],
            compliance_frequency, d["description"],
            date_list, due_date, validity_date,
            summary
        )
        user_wise_compliance = clientreport.UserWiseCompliance(
            d["assignee_name"], d["concurrence_name"],
            d["approval_name"], [compliance]
        )
        group_by_legal = legal_wise.get(d["legal_entity"])
        if group_by_legal is None:
            AC = clientreport.AssigneeCompliance(
                d["business_group"], d["legal_entity"],
                d["division"], [user_wise_compliance]
            )
            AC.to_structure()
            legal_wise[d["legal_entity"]] = AC
        else:
            user_wise_list = group_by_legal.user_wise_compliance
            if user_wise_list is None:
                user_wise_list = []
                user_wise_list.append(user_wise_compliance)
            else:
                is_added = False
                for u in user_wise_list:
                    if (
                        d["assignee_name"] == u.assignee and
                        d["concurrence_name"] == u.concurrence_person and
                        d["approval_name"] == u.approval_person
                    ):
                        lst = u.compliances
                        if lst is None:
                            lst = []
                        lst.append(compliance)
                        u.complaince = lst
                        is_added = True
                if is_added is False:
                    user_wise_list.append(user_wise_compliance)

            group_by_legal.user_wise_compliance = user_wise_list
            legal_wise[d["legal_entity"]] = group_by_legal
    return legal_wise.values()


def report_serviceproviderwise_compliance(
    db, country_id, domain_id, statutory_id, unit_id,
    service_provider_id, session_user, from_count, page_count
):
    columns = [
        "country_id", "unit_id", "compliance_id", "statutory_dates",
        "trigger_before_days", "due_date", "validity_date",
        "compliance_task", "document_name", "description", "frequency_id",
        "assignee", "service_provider_id",
        "service_provider_name", "address", "contract_from",
        "contract_to", "contact_person", "contact_no",
        "unit_code", "unit_name", "frequency",
        "duration_type", "repeat_type", "duration",
        "repeat_every"
    ]
    qry_where = ""
    qry_where_val = []
    admin_id = get_admin_id(db)

    if unit_id is not None:
        qry_where += " AND u.unit_id = %s"
        qry_where_val.append(unit_id)

    if service_provider_id is not None:
        qry_where += " AND s.service_provider_id = %s"
        qry_where_val.append(service_provider_id)

    if session_user != admin_id:
        qry_where += " AND u.unit_id in " + \
            " (select us.unit_id from tbl_user_units us where " + \
            " us.user_id = %s )"
        qry_where_val.append(session_user)

    q_count = " SELECT  " + \
        " count(ac.compliance_id) " + \
        " FROM tbl_assigned_compliances ac " + \
        " INNER JOIN tbl_units u on ac.unit_id = u.unit_id " + \
        " INNER JOIN tbl_compliances c " + \
        " on ac.compliance_id = c.compliance_id " + \
        " INNER JOIN tbl_users ur on ur.user_id = ac.assignee " + \
        " and ur.is_service_provider = 1 " + \
        " INNER JOIN tbl_service_providers s " + \
        " on s.service_provider_id = ur.service_provider_id " + \
        " WHERE c.is_active = 1 " + \
        " and ac.country_id = %s and c.domain_id = %s " + \
        " AND SUBSTRING_INDEX(SUBSTRING_INDEX( " + \
        " c.statutory_mapping, '>>', 1),'>>',- 1) = %s "
    param = [country_id, domain_id, statutory_id]

    if qry_where is not None:
        q_count += qry_where
        param.extend(qry_where_val)

    row = db.select_one(q_count, param)
    if row:
        count = row[0]
    else:
        count = 0

    q = " SELECT " + \
        " ac.country_id, ac.unit_id, ac.compliance_id, " + \
        " ac.statutory_dates, ac.trigger_before_days, " + \
        " ac.due_date, ac.validity_date, " + \
        " c.compliance_task, c.document_name, c.compliance_description, " + \
        " c.frequency_id, ac.assignee, " + \
        " s.service_provider_id, s.service_provider_name, s.address, " + \
        " s.contract_from, s.contract_to, s.contact_person, s.contact_no, " + \
        " u.unit_code, u.unit_name, " + \
        " (select f.frequency from tbl_compliance_frequency f " + \
        " where f.frequency_id = c.frequency_id) frequency, " + \
        " (select duration_type from tbl_compliance_duration_type " + \
        " where duration_type_id = c.duration_type_id) AS duration_type, " + \
        " (select repeat_type from tbl_compliance_repeat_type " + \
        " where repeat_type_id = c.repeats_type_id) AS repeat_type, " + \
        " c.duration, c.repeats_every " + \
        " FROM tbl_assigned_compliances ac " + \
        " INNER JOIN tbl_units u on ac.unit_id = u.unit_id " + \
        " INNER JOIN tbl_compliances c " + \
        " on ac.compliance_id = c.compliance_id " + \
        " INNER JOIN tbl_users ur on ur.user_id = ac.assignee " + \
        " and ur.is_service_provider = 1 " + \
        " INNER JOIN tbl_service_providers s " + \
        " on s.service_provider_id = ur.service_provider_id " + \
        " WHERE c.is_active = 1 " + \
        " and ac.country_id = %s and c.domain_id = %s " + \
        " AND SUBSTRING_INDEX(SUBSTRING_INDEX( " + \
        " c.statutory_mapping, '>>', 1),'>>',- 1) = %s "
    order = " ORDER BY ac.assignee, u.unit_id " + \
            " limit %s, %s"

    param = [country_id, domain_id, statutory_id]
    if qry_where is not None:
        q += qry_where
        param.extend(qry_where_val)

    param.extend([from_count, page_count])
    rows = db.select_all(q + order, param)
    data = convert_to_dict(rows, columns)
    return data, count


def return_serviceprovider_report_data(data):
    serviceprovider_wise = {}
    for d in data:
        statutory_dates = json.loads(d["statutory_dates"])
        date_list = []
        for date in statutory_dates:
            s_date = clientcore.StatutoryDate(
                date["statutory_date"],
                date["statutory_month"],
                date["trigger_before_days"],
                date.get("repeat_by")
            )
            date_list.append(s_date)

        compliance_frequency = clientcore.COMPLIANCE_FREQUENCY(
            d["frequency"]
        )

        due_date = None
        if(d["due_date"] is not None):
            due_date = datetime_to_string(d["due_date"])

        validity_date = None
        if(d["validity_date"] is not None):
            validity_date = datetime_to_string(d["validity_date"])

        if d["frequency_id"] in (2, 3):
            summary = "Repeats every %s - %s" % (
                d["repeat_every"], d["repeat_type"]
            )
        elif d["frequency_id"] == 4:
            summary = "To complete within %s - %s" % (
                d["duration"], d["duration_type"]
            )
        else:
            summary = None

        if d["document_name"] in ["None", None, ""]:
            name = d["compliance_task"]
        else:
            name = d["document_name"] + " - " + d["compliance_task"]
        uname = d["unit_code"] + " - " + d["unit_name"]
        compliance = clientreport.ComplianceUnit(
            name, uname,
            compliance_frequency, d["description"],
            date_list, due_date, validity_date,
            summary
        )

        group_by_serviceprovider = serviceprovider_wise.get(
            d["service_provider_name"])
        if group_by_serviceprovider is None:
            unit_wise = {}
            unit_wise[uname] = [compliance]
            AC = clientreport.ServiceProviderCompliance(
                d["service_provider_name"], d["address"],
                datetime_to_string(d["contract_from"]),
                datetime_to_string(d["contract_to"]),
                d["contact_person"], d["contact_no"], unit_wise
            )
            AC.to_structure()
            serviceprovider_wise[d["service_provider_name"]] = AC
        else:
            unit_wise_list = group_by_serviceprovider.unit_wise_compliance
            if unit_wise_list is None:
                unit_wise_list = {}
                unit_wise_list[uname] = [compliance]
            else:
                lst = unit_wise_list.get(uname)
                if lst is None:
                    lst = []
                lst.append(compliance)
                unit_wise_list[uname] = lst

            group_by_serviceprovider.unit_wise_compliances = unit_wise_list
            serviceprovider_wise[
                d["service_provider_name"]
            ] = group_by_serviceprovider
    return serviceprovider_wise.values()


def report_statutory_notifications_list(db, request_data):
    country_name = request_data.country_name
    domain_name = request_data.domain_name
    business_group_id = request_data.business_group_id
    legal_entity_id = request_data.legal_entity_id
    division_id = request_data.division_id
    unit_id = request_data.unit_id
    level_1_statutory_name = request_data.level_1_statutory_name
    from_date = request_data.from_date
    to_date = request_data.to_date

    condition = ""
    condition_val = []
    if from_date is not None and to_date is not None:
        from_date = string_to_datetime(from_date).date()
        to_date = string_to_datetime(to_date).date()
        condition += " AND date(snl.updated_on)  >= %s AND " + \
            " date(snl.updated_on) <= %s "
        condition_val.extend([from_date, to_date])

    if business_group_id is not None:
        condition += " AND u.business_group_id = %s "
        condition_val.append(business_group_id)

    if legal_entity_id is not None:
        condition += " AND u.legal_entity_id = %s "
        condition_val.append(legal_entity_id)

    if division_id is not None:
        condition += " AND u.division_id = %s "
        condition_val.append(division_id)

    if unit_id is not None:
        condition += " AND u.unit_id = %s "
        condition_val.append(unit_id)

    if level_1_statutory_name is not None:
        condition += " AND snl.statutory_provision like %s "
        condition_val.append(str(level_1_statutory_name + '%'))

    query = "SELECT " + \
        " (select business_group_name from tbl_business_groups " + \
        " where business_group_id = u.business_group_id), " + \
        " (select legal_entity_name from tbl_legal_entities " + \
        " where legal_entity_id = u.legal_entity_id), " + \
        " (select division_name from tbl_divisions " + \
        " where division_id = u.division_id), " + \
        " u.unit_code, u.unit_name, u.address, snl.statutory_provision, " + \
        " snl.notification_text, snl.updated_on from " + \
        " tbl_statutory_notifications_log snl " + \
        " INNER JOIN " + \
        " tbl_statutory_notifications_units snu " + \
        " ON  " + \
        " snl.statutory_notification_id = snu.statutory_notification_id " + \
        " INNER JOIN " + \
        " tbl_units u ON snu.unit_id = u.unit_id " + \
        " INNER JOIN tbl_countries tc ON " + \
        " tc.country_id = snl.country_name " + \
        " INNER JOIN tbl_domains td ON " + \
        " td.domain_id = snl.domain_name " + \
        " where " + \
        " tc.country_name = %s " + \
        " and td.domain_name = %s "

    order = " ORDER BY snl.updated_on"
    param = [country_name, domain_name]
    if condition is not None:
        query += condition
        param.extend(condition_val)

    rows = db.select_all(query + order, param)
    columns = [
        "business_group", "legal_entity", "division", "unit_code", "unit_name",
        "address", "statutory_provision", "notification_text", "updated_on"
    ]
    data = convert_to_dict(rows, columns)
    legal_wise = {}
    for d in data:
        unit_name = "%s - %s" % (d["unit_code"], d["unit_name"])
        statutories = d["statutory_provision"].split(">>")
        level_1_statutory_name = statutories[0].strip()

        level_1_statutory_wise_notifications = {}
        notify = clientreport.LEVEL_1_STATUTORY_NOTIFICATIONS(
            d["statutory_provision"],
            unit_name,
            d["notification_text"],
            datetime_to_string(d["updated_on"])
        )
        level_1_statutory_wise_notifications[level_1_statutory_name] = [notify]
        legal_wise_data = legal_wise.get(d["legal_entity"])
        if legal_wise_data is None:
            legal_wise_data = clientreport.STATUTORY_WISE_NOTIFICATIONS(
                d["business_group"], d["legal_entity"], d["division"],
                level_1_statutory_wise_notifications
            )
        else:
            dict_level_1 = legal_wise_data.level_1_statutory_wise_notifications
            if dict_level_1 is None:
                dict_level_1 = {}
            lst = dict_level_1.get(level_1_statutory_name)
            if lst is None:
                lst = []
            else:
                lst.append(notify)
            dict_level_1[level_1_statutory_name] = lst
            legal_wise_data.level_1_statutory_wise_notifications = dict_level_1
        legal_wise[d["legal_entity"]] = legal_wise_data

    notification_lst = []
    for k in sorted(legal_wise):
        notification_lst.append(legal_wise.get(k))
    return notification_lst


def report_compliance_details(
    db, country_id, domain_id, statutory_id,
    unit_id, compliance_id, assignee,
    from_date, to_date, compliance_status,
    session_user, from_count, page_count
):

    qry_where, qry_where_val = get_where_query_for_compliance_details_report(
        db, country_id, domain_id, statutory_id,
        unit_id, compliance_id, assignee,
        from_date, to_date, compliance_status,
        session_user
    )

    total = get_compliance_details_total_count(
        db, country_id, domain_id, statutory_id, qry_where, qry_where_val
    )

    result = get_compliance_details(
        db, country_id, domain_id, statutory_id,
        qry_where, qry_where_val, from_count, page_count
    )

    return return_cmopliance_details_report(
        compliance_status, result, total
    )


def return_cmopliance_details_report(
    compliance_status, result, total
):
    unitWise = {}
    for r in result:
        uname = r["unit_code"] + ' - ' + r["unit_name"]
        if r["document_name"] in ["None", None]:
            compliance_name = r["compliance_task"]
        else:
            compliance_name = r["document_name"] + ' - ' + r["compliance_task"]

        if r["assigneename"] is None:
            assignee = 'Administrator'
        else:
            assignee = r["assigneename"]

        due_date = None
        if(r["due_date"] != None):
            due_date = datetime_to_string(r["due_date"])

        validity_date = None
        if(r["validity_date"] != None):
            validity_date = datetime_to_string(r["validity_date"])

        documents = [
            x for x in r["documents"].split(",")
        ] if r["documents"] != None else None
        doc_urls = []
        if documents is not None:
            for d in documents:
                if d != "":
                    t = "%s/%s/%s" % (
                        # CLIENT_DOCS_DOWNLOAD_URL, str(client_id), str(d)
                        CLIENT_DOCS_DOWNLOAD_URL, str(d)
                    )
                    doc_urls.append(t)

        completion_date = None
        if(r["completion_date"] != None):
            completion_date = datetime_to_string(r["completion_date"])

        remarks = calculate_ageing(
            r["due_date"], r["fname"], r["completion_date"]
        )[1]

        compliance = clientreport.ComplianceDetails(
            compliance_name, assignee, due_date,
            completion_date, validity_date,
            doc_urls, remarks
        )
        unit_compliance = unitWise.get(uname)
        if unit_compliance is None:
            unit_compliance = clientreport.ComplianceDetailsUnitWise(
                r["unit_id"], uname, r["address"],
                [compliance]
            )
        else:
            compliance_lst = unit_compliance.Compliances
            if compliance_lst is None:
                compliance_lst = []
            compliance_lst.append(compliance)
            unit_compliance.Compliances = compliance_lst
        unitWise[uname] = unit_compliance

    final_lst = []
    for k in sorted(unitWise):
        final_lst.append(unitWise.get(k))

    return final_lst, total


def get_where_query_for_compliance_details_report(
    db, country_id, domain_id, statutory_id,
    unit_id, compliance_id, assignee,
    from_date, to_date, compliance_status,
    session_user
):
    q_c = "SELECT t.period_from, t.period_to " + \
        " FROM tbl_client_configurations t " + \
        " where t.country_id = %s and t.domain_id = %s "
    r_c = db.select_one(q_c, [country_id, domain_id])
    f_date = t_date = None
    if r_c:
        year_list = calculate_years(int(r_c[0]), int(r_c[1]))[0]

        f_date = datetime.date(int(year_list[0]), int(r_c[0]), 1)
        if int(r_c[1]) == 12:
            t_date = datetime.date(int(year_list[0]), int(r_c[1]), 31)
        else:
            t_date = datetime.date(
                int(year_list[0]), int(r_c[1]) + 1, 1
            ) - datetime.timedelta(days=1)

    qry_where = ""
    qry_where_val = []
    admin_id = get_admin_id(db)
    if unit_id is not None:
        qry_where += " AND ch.unit_id = %s"
        qry_where_val.append(unit_id)

    if compliance_id is not None:
        qry_where += " AND ch.compliance_id = %s "
        qry_where_val.append(compliance_id)

    if assignee is not None:
        qry_where += " AND ch.completed_by = %s"
        qry_where_val.append(assignee)

    if session_user != admin_id:
        qry_where += " AND ch.unit_id in " + \
            " (select us.unit_id from tbl_user_units us where " + \
            " us.user_id = %s )"
        qry_where_val.append(session_user)
        qry_where += " and c.domain_id IN " + \
            " (SELECT ud.domain_id FROM tbl_user_domains ud " + \
            " where ud.user_id = %s)"
        qry_where_val.append(session_user)

    if(compliance_status == 'Complied'):
        c_status = " AND ch.due_date >= ch.completion_date " + \
            " AND IFNULL(ch.approve_status,0) = 1"
    elif(compliance_status == 'Delayed Compliance'):
        c_status = " AND ch.due_date < ch.completion_date " + \
            " AND IFNULL(ch.approve_status,0) = 1"
    elif(compliance_status == 'Inprogress'):
        c_status = " AND ((c.duration_type_id =2 " + \
            " AND ch.due_date >= now()) " + \
            " or (c.duration_type_id != 2 and ch.due_date >= CURDATE())) " + \
            " AND IFNULL(ch.approve_status,0) <> 1"
    elif(compliance_status == 'Not Complied'):
        c_status = " AND ((c.duration_type_id =2 AND ch.due_date < now()) " + \
            " or (c.duration_type_id != 2 and ch.due_date < CURDATE())) " + \
            " AND IFNULL(ch.approve_status,0) <> 1"
    else:
        c_status = ''

    qry_where += c_status

    if from_date is not None and to_date is not None:
        start_date = string_to_datetime(from_date)
        end_date = string_to_datetime(to_date)
        qry_where += " AND ch.due_date between " + \
            " DATE_SUB(%s, INTERVAL 1 DAY)  and " + \
            " DATE_ADD(%s, INTERVAL 1 DAY) "
        qry_where_val.extend([start_date, end_date])

    else:
        qry_where += " AND ch.due_date >= %s " + \
            " AND ch.due_date <= %s"
        qry_where_val.extend([f_date, t_date])
    return qry_where, qry_where_val


def get_compliance_details_total_count(
    db, country_id, domain_id, statutory_id, qry_where, qry_where_val
):
    qry_count = "SELECT " + \
        " count(distinct ch.compliance_history_id) " + \
        " from " + \
        " tbl_compliance_history ch " + \
        " inner join " + \
        " tbl_compliances c on ch.compliance_id = c.compliance_id " + \
        " inner join  " + \
        " tbl_units ut on ch.unit_id = ut.unit_id " + \
        " where ut.country_id = %s " + \
        " AND c.domain_id = %s " + \
        " AND c.statutory_mapping like %s "
    order = " ORDER BY ch.due_date desc "
    param = [country_id, domain_id, str(statutory_id + "%")]
    if qry_where is not None:
        qry_count += qry_where
        param.extend(qry_where_val)

    row = db.select_one(qry_count + order, param)
    if row:
        total = int(row[0])
    else:
        total = 0
    return total


def get_compliance_details(
    db, country_id, domain_id, statutory_id,
    qry_where, qry_where_val, from_count, to_count
):

    columns = [
        "compliance_history_id", "document_name",
        "compliance_description", "validity_date",
        "due_date", "completed_by", "status", "assigneename", "documents",
        "completion_date", "compliance_task", "frequency_id", "fname",
        "unit_id", "unit_code", "unit_name", "address"
    ]
    qry = "SELECT " + \
        " distinct ch.compliance_history_id, " + \
        " c.document_name, " + \
        " c.compliance_description, " + \
        " ch.validity_date, " + \
        " ch.due_date, " + \
        " ch.completed_by, " + \
        " ifnull(ch.approve_status, 0) status," + \
        " (SELECT  " + \
        " concat(u.employee_code, '-', u.employee_name) " + \
        " FROM " + \
        " tbl_users u " + \
        " WHERE " + \
        " u.user_id = ch.completed_by) AS assigneename, " + \
        " ch.documents, " + \
        " ch.completion_date, " + \
        " c.compliance_task, " + \
        " c.frequency_id, " + \
        " (select f.frequency from tbl_compliance_frequency f " + \
        " where f.frequency_id = c.frequency_id) fname, " + \
        " ch.unit_id, ut.unit_code, ut.unit_name, ut.address" + \
        " from " + \
        " tbl_compliance_history ch  " + \
        " inner join  " + \
        " tbl_compliances c on ch.compliance_id = c.compliance_id  " + \
        " inner join  " + \
        " tbl_units ut on ch.unit_id = ut.unit_id " + \
        " where ut.country_id = %s " + \
        " AND c.domain_id = %s " + \
        " AND c.statutory_mapping like %s "

    order = " ORDER BY ch.due_date desc limit %s, %s "

    param = [country_id, domain_id, str(statutory_id + "%")]
    if qry_where is not None:
        qry += qry_where
        param.extend(qry_where_val)

    param.extend([from_count, to_count])
    rows = db.select_all(qry + order, param)
    result = convert_to_dict(rows, columns)
    return result


def get_delayed_compliances_where_qry(
    db, business_group_id, legal_entity_id, division_id, unit_id,
    leval_1_statutory_name, session_user
):
    where_qry = ""
    where_qry_val = []
    admin_id = get_admin_id(db)
    if session_user != admin_id:
        where_qry += " AND u.unit_id in " + \
            " (select us.unit_id from tbl_user_units us where " + \
            " us.user_id = %s ) "
        where_qry_val.append(int(session_user))
        where_qry += " AND c.domain_id in " + \
            " (select us.domain_id from tbl_user_domains us where " + \
            " us.user_id = %s )"
        where_qry_val.append(int(session_user))

    if business_group_id is not None:
        where_qry += " AND u.business_group_id = %s "
        where_qry_val.append(business_group_id)

    if legal_entity_id is not None:
        where_qry += " AND u.legal_entity_id = %s "
        where_qry_val.append(legal_entity_id)

    if division_id is not None:
        where_qry += " AND u.division_id = %s "
        where_qry_val.append(division_id)

    if unit_id is not None:
        where_qry += " AND u.unit_id = %s "
        where_qry_val.append(unit_id)

    if leval_1_statutory_name is not None:
        where_qry += " AND c.statutory_mapping like %s "
        where_qry_val.append(leval_1_statutory_name + '%')
    return where_qry, where_qry_val


def get_delayed_compliances_count(
    db, country_id, domain_id, business_group_id,
    legal_entity_id, division_id, unit_id, leval_1_statutory_name,
    session_user
):
    where_qry, where_qry_val = get_delayed_compliances_where_qry(
        db, business_group_id, legal_entity_id, division_id, unit_id,
        leval_1_statutory_name, session_user
    )
    q_count = "SELECT count(distinct ch.compliance_history_id) " + \
        " FROM tbl_compliance_history ch " + \
        " INNER JOIN tbl_assigned_compliances ac " + \
        " ON ch.compliance_id = ac.compliance_id " + \
        " AND ch.unit_id = ac.unit_id " + \
        " INNER JOIN tbl_compliances c " + \
        " ON ch.compliance_id = c.compliance_id " + \
        " INNER JOIN tbl_units u ON  " + \
        " ch.unit_id = u.unit_id " + \
        " WHERE c.domain_id = %s " + \
        " AND ac.country_id = %s " + \
        " AND ch.due_date < ch.completion_date " + \
        " AND ch.approve_status = 1 "

    param = [domain_id, country_id]
    if where_qry != "":
        q_count += where_qry
        param.extend(where_qry_val)

    c_row = db.select_one(q_count, param)
    if c_row:
        total = int(c_row[0])
    else:
        total = 0
    return total


def get_delayed_compliances(
    db, domain_id, country_id, where_qry, where_qry_val, from_count, to_count
):
    query = "SELECT  c.compliance_id, c.compliance_task, c.document_name, " + \
        " ac.statutory_dates, c.compliance_description, " + \
        " c.penal_consequences, c.frequency_id," + \
        " (select frequency from tbl_compliance_frequency " + \
        " where frequency_id = c.frequency_id ), " + \
        " c.repeats_type_id, c.repeats_every, " + \
        " c.duration_type_id, c.duration, " + \
        " c.statutory_mapping, " + \
        " SUBSTRING_INDEX(SUBSTRING_INDEX( " + \
        " c.statutory_mapping, '>>', 1), '>>', - 1) level_1, " + \
        " c.statutory_provision, " + \
        " (select business_group_name from tbl_business_groups " + \
        " where business_group_id = u.business_group_id ), " + \
        " (select legal_entity_name from tbl_legal_entities " + \
        " where legal_entity_id = u.legal_entity_id), " + \
        " (select division_name from tbl_divisions " + \
        " where division_id = u.division_id), " + \
        " u.unit_code, u.unit_name, u.address, u.postal_code, u.unit_id " + \
        " FROM tbl_compliance_history ch " + \
        " INNER JOIN tbl_assigned_compliances ac " + \
        " ON ch.compliance_id = ac.compliance_id " + \
        " AND ch.unit_id = ac.unit_id " + \
        " INNER JOIN tbl_compliances c " + \
        " ON ch.compliance_id = c.compliance_id " + \
        " INNER JOIN tbl_units u ON  " + \
        " ch.unit_id = u.unit_id " + \
        " WHERE c.domain_id = %s " + \
        " AND ac.country_id = %s " + \
        " AND ch.due_date < ch.completion_date " + \
        " AND ch.approve_status = 1 "

    order = " ORDER BY SUBSTRING_INDEX(SUBSTRING_INDEX(" + \
        " c.statutory_mapping, '>>', 1), '>>', - 1), u.unit_id " + \
        " limit %s, %s "
    param = [domain_id, country_id]
    if where_qry != "":
        query += where_qry
        param.extend(where_qry_val)

    param.extend([from_count, to_count])
    rows = db.select_all(query + order, param)

    columns = [
        "compliance_id", "compliance_task", "document_name",
        "statutory_dates", "compliance_description", "penal_consequences",
        "frequency_id", "frequency",
        "repeats_type_id", "repeats_every", "duration_type_id", "duration",
        "statutory_mapping", "level_1", "statutory_provision",
        "business_group", "legal_entity",
        "division", "unit_code", "unit_name",
        "address", "postal_code", "unit_id"
    ]

    result = convert_to_dict(rows, columns)
    return result


def get_delayed_compliances_with_count(
    db, country_id, domain_id, business_group_id,
    legal_entity_id, division_id, unit_id, leval_1_statutory_name,
    session_user, from_count, to_count
):
    where_qry, where_qry_val = get_delayed_compliances_where_qry(
        db, business_group_id, legal_entity_id, division_id, unit_id,
        leval_1_statutory_name, session_user
    )
    total = get_delayed_compliances_count(
        db, country_id, domain_id, business_group_id,
        legal_entity_id, division_id, unit_id, leval_1_statutory_name,
        session_user
    )
    result = get_delayed_compliances(
        db, domain_id, country_id, where_qry,
        where_qry_val, from_count, to_count
    )
    return return_risk_report_data(db, result, total)


def get_not_complied_compliances(
    db, domain_id, country_id, where_qry, where_qry_val, from_count, to_count
):
    query = "SELECT distinct c.compliance_id, c.compliance_task, " + \
        " c.document_name, " + \
        " ac.statutory_dates, c.compliance_description, " + \
        " c.penal_consequences, c.frequency_id, " + \
        " (select frequency from tbl_compliance_frequency " + \
        " where frequency_id = c.frequency_id ), " + \
        " c.repeats_type_id, c.repeats_every, c.duration_type_id, " + \
        " c.duration,  c.statutory_mapping," + \
        " SUBSTRING_INDEX(SUBSTRING_INDEX( " + \
        " c.statutory_mapping, '>>', 1), '>>', - 1) level_1, " + \
        " c.statutory_provision, " + \
        " (select business_group_name from tbl_business_groups " + \
        " where business_group_id = u.business_group_id ), " + \
        " (select legal_entity_name from tbl_legal_entities " + \
        " where legal_entity_id = u.legal_entity_id), " + \
        " (select division_name from tbl_divisions " + \
        " where division_id = u.division_id), " + \
        " u.unit_code, u.unit_name, u.address, u.postal_code, u.unit_id, " + \
        " ch.compliance_history_id " + \
        " FROM tbl_compliance_history ch " + \
        " INNER JOIN tbl_assigned_compliances ac " + \
        " ON ch.compliance_id = ac.compliance_id " + \
        " AND ch.unit_id = ac.unit_id " + \
        " INNER JOIN tbl_compliances c " + \
        " ON ch.compliance_id = c.compliance_id " + \
        " INNER JOIN tbl_units u ON  " + \
        " ch.unit_id = u.unit_id " + \
        " WHERE c.domain_id = %s " + \
        " AND ac.country_id = %s" + \
        " AND ((IFNULL(c.duration_type_id, 0) = 2 AND ch.due_date < now())" + \
        " or (IFNULL(c.duration_type_id, 0) != 2 " + \
        " AND ch.due_date < CURDATE())) " + \
        " AND IFNULL(ch.approve_status, 0) != 1 "

    order = " ORDER BY SUBSTRING_INDEX(SUBSTRING_INDEX( " + \
        " c.statutory_mapping, '>>', 1), '>>', - 1), u.unit_id " + \
        " limit %s, %s "

    param = [domain_id, country_id]
    if where_qry != "":
        query += where_qry
        param.extend(where_qry_val)

    param.extend([from_count, to_count])
    rows = db.select_all(query + order, param)

    columns = [
        "compliance_id", "compliance_task", "document_name",
        "statutory_dates", "compliance_description", "penal_consequences",
        "frequency_id", "frequency",
        "repeats_type_id", "repeats_every", "duration_type_id", "duration",
        "statutory_mapping", "level_1", "statutory_provision",
        "business_group", "legal_entity",
        "division", "unit_code", "unit_name",
        "address", "postal_code", "unit_id",
        "compliance_history_id"
    ]

    result = convert_to_dict(rows, columns)
    return result


def get_not_complied_where_qry(
    db, business_group_id, legal_entity_id, division_id, unit_id,
    leval_1_statutory_name
):
    where_qry = ""
    where_qry_val = []
    if business_group_id is not None:
        where_qry += " AND u.business_group_id = %s "
        where_qry_val.append(business_group_id)

    if legal_entity_id is not None:
        where_qry += " AND u.legal_entity_id = %s "
        where_qry_val.append(legal_entity_id)

    if division_id is not None:
        where_qry += " AND u.division_id = %s "
        where_qry_val.append(division_id)

    if unit_id is not None:
        where_qry += " AND u.unit_id = %s "
        where_qry_val.append(unit_id)

    if leval_1_statutory_name is not None:
        where_qry += " AND c.statutory_mapping like %s "
        where_qry_val.append(leval_1_statutory_name + '%')
    return where_qry, where_qry_val


def get_not_complied_compliances_count(
    db, country_id, domain_id, where_qry, where_qry_val
):
    q_count = "SELECT count(c.compliance_id) " + \
        " FROM tbl_compliance_history ch " + \
        " INNER JOIN tbl_compliances c " + \
        " ON ch.compliance_id = c.compliance_id " + \
        " INNER JOIN tbl_units u ON  " + \
        " ch.unit_id = u.unit_id " + \
        " WHERE c.domain_id = %s " + \
        " AND u.country_id = %s " + \
        " AND ((IFNULL(c.duration_type_id, 0) = 2 " + \
        " AND ch.due_date < now()) " + \
        " or (IFNULL(c.duration_type_id, 0) != 2 " + \
        " AND ch.due_date < CURDATE()))  " + \
        " AND IFNULL(ch.approve_status, 0) != 1 "

    param = [domain_id, country_id]
    if where_qry != "":
        q_count += where_qry
        param += where_qry_val

    c_row = db.select_one(q_count, param)
    if c_row:
        total = int(c_row[0])
    else:
        total = 0
    return total


def get_not_complied_compliances_with_count(
    db, country_id, domain_id, business_group_id,
    legal_entity_id, division_id, unit_id, leval_1_statutory_name,
    session_user, from_count, to_count
):
    where_qry, where_qry_val = get_not_complied_where_qry(
        db, business_group_id, legal_entity_id, division_id, unit_id,
        leval_1_statutory_name
    )
    total = get_not_complied_compliances_count(
        db, country_id, domain_id, where_qry, where_qry_val
    )
    result = get_not_complied_compliances(
        db, domain_id, country_id, where_qry,
        where_qry_val, from_count, to_count
    )
    return return_risk_report_data(db, result, total)


def get_not_opted_compliances(
    db, domain_id, country_id, where_qry, where_qry_val, from_count, to_count
):
    query = "SELECT c.compliance_id, c.compliance_task, c.document_name," + \
        " c.statutory_dates, c.compliance_description, " + \
        " c.penal_consequences, c.frequency_id, " + \
        " (select frequency from tbl_compliance_frequency " + \
        " where frequency_id = c.frequency_id ), " + \
        " c.repeats_type_id, c.repeats_every, c.duration_type_id, " + \
        " c.duration, c.statutory_mapping, " + \
        " SUBSTRING_INDEX(SUBSTRING_INDEX( " + \
        " c.statutory_mapping, '>>', 1), '>>', - 1) level_1, " + \
        " c.statutory_provision, " + \
        " (select business_group_name from tbl_business_groups " + \
        " where business_group_id = u.business_group_id ), " + \
        " (select legal_entity_name from tbl_legal_entities " + \
        " where legal_entity_id = u.legal_entity_id), " + \
        " (select division_name from tbl_divisions " + \
        " where division_id = u.division_id), " + \
        " u.unit_code, u.unit_name, u.address, u.postal_code, u.unit_id " + \
        " FROM tbl_compliances c " + \
        " INNER JOIN tbl_client_compliances cc " + \
        " ON c.compliance_id = cc.compliance_id " + \
        " INNER JOIN tbl_client_statutories cs  " + \
        " ON cs.client_statutory_id = cc.client_statutory_id " + \
        " INNER JOIN tbl_units u ON  " + \
        " cs.unit_id = u.unit_id " + \
        " WHERE  cc.compliance_opted = 0 " + \
        " AND c.domain_id = %s " + \
        " AND cs.country_id = %s "
    order = " ORDER BY SUBSTRING_INDEX(SUBSTRING_INDEX( " + \
        " c.statutory_mapping, '>>', 1), '>>', - 1), u.unit_id " + \
        " limit %s, %s "
    param = [domain_id, country_id]
    if where_qry != "":
        query += where_qry
        param.extend(where_qry_val)

    param.extend([from_count, to_count])
    rows = db.select_all(query + order, param)

    columns = [
        "compliance_id", "compliance_task", "document_name",
        "statutory_dates", "compliance_description", "penal_consequences",
        "frequency_id", "frequency",
        "repeats_type_id", "repeats_every", "duration_type_id", "duration",
        "statutory_mapping", "level_1", "statutory_provision",
        "business_group", "legal_entity",
        "division", "unit_code", "unit_name",
        "address", "postal_code", "unit_id"
    ]

    result = convert_to_dict(rows, columns)
    return result


def get_not_opted_compliances_where_qry(
    db, business_group_id, legal_entity_id, division_id, unit_id,
    leval_1_statutory_name, session_user
):
    where_qry = ""
    where_qry_val = []
    admin_id = get_admin_id(db)

    if session_user != admin_id:
        where_qry += " AND u.unit_id in " + \
            " (select us.unit_id from tbl_user_units us where " + \
            " us.user_id = %s)"
        where_qry_val.append(session_user)
        where_qry += " AND c.domain_id in " + \
            " (select us.domain_id from tbl_user_domains us where " + \
            " us.user_id = %s)"
        where_qry_val.append(session_user)

    if business_group_id is not None:
        where_qry += " AND u.business_group_id = %s "
        where_qry_val.append(business_group_id)

    if legal_entity_id is not None:
        where_qry += " AND u.legal_entity_id = %s "
        where_qry_val.append(legal_entity_id)

    if division_id is not None:
        where_qry += " AND u.division_id = %s "
        where_qry_val.append(division_id)

    if unit_id is not None:
        where_qry += " AND u.unit_id = %s "
        where_qry_val.append(unit_id)

    if leval_1_statutory_name is not None:
        where_qry += " AND c.statutory_mapping like %s "
        where_qry_val.append(leval_1_statutory_name + '%')

    return where_qry, where_qry_val


def get_not_opted_compliances_count(
    db, country_id, domain_id, where_qry, where_qry_val
):
    q_count = "SELECT count(c.compliance_id) " + \
        " FROM tbl_compliances c " + \
        " INNER JOIN tbl_client_compliances cc " + \
        " ON c.compliance_id = cc.compliance_id " + \
        " INNER JOIN tbl_client_statutories cs  " + \
        " ON cs.client_statutory_id = cc.client_statutory_id " + \
        " INNER JOIN tbl_units u ON  " + \
        " cs.unit_id = u.unit_id " + \
        " WHERE  cc.compliance_opted = 0 " + \
        " AND c.domain_id = %s " + \
        " AND cs.country_id = %s "

    param = [domain_id, country_id]
    if where_qry != "":
        q_count += where_qry
        param.extend(where_qry_val)

    c_row = db.select_one(q_count, param)
    if c_row:
        total = int(c_row[0])
    else:
        total = 0
    return total


def get_not_opted_compliances_with_count(
    db, country_id, domain_id, business_group_id,
    legal_entity_id, division_id, unit_id, leval_1_statutory_name,
    session_user, from_count, to_count
):
    where_qry, where_qry_val = get_not_opted_compliances_where_qry(
        db, business_group_id, legal_entity_id, division_id, unit_id,
        leval_1_statutory_name,  session_user
    )
    total = get_not_opted_compliances_count(
        db, country_id, domain_id, where_qry, where_qry_val
    )
    result = get_not_opted_compliances(
        db, domain_id, country_id, where_qry,
        where_qry_val, from_count, to_count
    )
    return return_risk_report_data(db, result, total)


def get_unassigned_compliances(
    db, domain_id, country_id, where_qry, where_qry_val, from_count, to_count
):
    query = "SELECT c.compliance_id, c.compliance_task, c.document_name, " + \
        " c.statutory_dates, c.compliance_description, " + \
        " c.penal_consequences, c.frequency_id, " + \
        " (select frequency from tbl_compliance_frequency " + \
        " where frequency_id = c.frequency_id ), " + \
        " c.repeats_type_id, c.repeats_every, c.duration_type_id, " + \
        " c.duration, c.statutory_mapping," + \
        " SUBSTRING_INDEX(SUBSTRING_INDEX(" + \
        " c.statutory_mapping, '>>', 1), '>>', - 1) level_1, " + \
        " c.statutory_provision, " + \
        " (select business_group_name from tbl_business_groups " + \
        " where business_group_id = u.business_group_id ), " + \
        " (select legal_entity_name from tbl_legal_entities " + \
        " where legal_entity_id = u.legal_entity_id), " + \
        " (select division_name from tbl_divisions " + \
        " where division_id = u.division_id), " + \
        " u.unit_code, u.unit_name, u.address, u.postal_code, u.unit_id " + \
        " FROM tbl_compliances c " + \
        " INNER JOIN tbl_client_compliances cc " + \
        " ON c.compliance_id = cc.compliance_id " + \
        " and ifnull(cc.compliance_opted, 0) = 1 " + \
        " INNEr JOIN tbl_client_statutories cs  " + \
        " ON cs.client_statutory_id = cc.client_statutory_id " + \
        " INNER JOIN tbl_units u ON  " + \
        " cs.unit_id = u.unit_id " + \
        " LEFT JOIN tbl_assigned_compliances ac " + \
        " ON ac.compliance_id = cc.compliance_id and " + \
        " ac.unit_id = cs.unit_id " + \
        " WHERE  ac.compliance_id is Null " + \
        " AND c.domain_id = %s " + \
        " AND cs.country_id = %s "

    order = " ORDER BY SUBSTRING_INDEX(SUBSTRING_INDEX(" + \
        " c.statutory_mapping, '>>', 1), '>>', - 1), u.unit_id " + \
        " limit %s, %s "
    param = [domain_id, country_id]
    if where_qry != "":
        query += where_qry
        param.extend(where_qry_val)

    param.extend([from_count, to_count])
    rows = db.select_all(query + order, param)

    columns = [
        "compliance_id", "compliance_task", "document_name",
        "statutory_dates", "compliance_description", "penal_consequences",
        "frequency_id", "frequency",
        "repeats_type_id", "repeats_every", "duration_type_id", "duration",
        "statutory_mapping", "level_1", "statutory_provision",
        "business_group", "legal_entity",
        "division", "unit_code", "unit_name",
        "address", "postal_code", "unit_id"
    ]

    result = convert_to_dict(rows, columns)
    return result


def get_unassigned_compliances_where_qry(
    db, business_group_id, legal_entity_id, division_id, unit_id,
    leval_1_statutory_name, session_user
):
    where_qry = ""
    where_qry_val = []
    admin_id = get_admin_id(db)

    if session_user != admin_id:
        where_qry += " AND u.unit_id in " + \
            " (select us.unit_id from tbl_user_units us where " + \
            " us.user_id = %s)"
        where_qry_val.append(session_user)
        where_qry += " AND c.domain_id in " + \
            " (select us.domain_id from tbl_user_domains us where " + \
            " us.user_id = %s )"
        where_qry_val.append(session_user)

    if business_group_id is not None:
        where_qry += " AND u.business_group_id = %s "
        where_qry_val.append(business_group_id)

    if legal_entity_id is not None:
        where_qry += " AND u.legal_entity_id = %s "
        where_qry_val.append(legal_entity_id)

    if division_id is not None:
        where_qry += " AND u.division_id = %s "
        where_qry_val.append(division_id)

    if unit_id is not None:
        where_qry += " AND u.unit_id = %s "
        where_qry_val.append(unit_id)

    if leval_1_statutory_name is not None:
        where_qry += " AND c.statutory_mapping like %s "
        where_qry_val.append(leval_1_statutory_name + '%')

    return where_qry, where_qry_val


def get_unassigned_compliances_count(
    db, country_id, domain_id, where_qry, where_qry_val
):
    q_count = "SELECT count(c.compliance_id) " + \
        " FROM tbl_compliances c " + \
        " INNER JOIN tbl_client_compliances cc " + \
        " ON c.compliance_id = cc.compliance_id " + \
        " and ifnull(cc.compliance_opted,0) = 1 " + \
        " INNER JOIN tbl_client_statutories cs  " + \
        " ON cs.client_statutory_id = cc.client_statutory_id " + \
        " INNER JOIN tbl_units u ON  " + \
        " cs.unit_id = u.unit_id " + \
        " Left JOIN tbl_assigned_compliances ac " + \
        " ON ac.compliance_id = cc.compliance_id and " + \
        " ac.unit_id = cs.unit_id " + \
        " WHERE  ac.compliance_id is Null " + \
        " AND c.domain_id = %s " + \
        " AND cs.country_id = %s "

    param = [domain_id, country_id]
    if where_qry != "":
        q_count += where_qry
        param.extend(where_qry_val)

    c_row = db.select_one(q_count, param)
    if c_row:
        total = int(c_row[0])
    else:
        total = 0
    return total


def get_unassigned_compliances_with_count(
    db, country_id, domain_id, business_group_id,
    legal_entity_id, division_id, unit_id, leval_1_statutory_name,
    session_user, from_count, to_count
):
    where_qry, where_qry_val = get_unassigned_compliances_where_qry(
        db, business_group_id, legal_entity_id, division_id, unit_id,
        leval_1_statutory_name, session_user
    )
    total = get_unassigned_compliances_count(
        db, country_id, domain_id, where_qry, where_qry_val
    )
    result = get_unassigned_compliances(
        db, domain_id, country_id, where_qry,
        where_qry_val, from_count, to_count
    )
    return return_risk_report_data(db, result, total)


def return_risk_report_data(db, data, total):
    report_data_list = {}
    for d in data:
        unit_id = int(d["unit_id"])
        business_group_name = d["business_group"]
        legal_entity = d["legal_entity"]
        division_name = d["division"]
        level_1 = d["level_1"]
        compliance_name = d["compliance_task"]
        if d["document_name"] not in (None, "None", ""):
            compliance_name = "%s - %s" % (
                d["document_name"], d["compliance_task"]
            )
        statutory_mapping = "%s >> %s" % (
            d["statutory_mapping"], d["statutory_provision"]
        )
        repeats = ""
        trigger = "Trigger:"
        if d["frequency_id"] != 1 and d["frequency_id"] != 4:
            if d["repeats_type_id"] == 1:
                repeats = "Every %s Day/s " % (d["repeats_every"])
            elif d["repeats_type_id"] == 2:
                repeats = "Every %s Month/s " % (d["repeats_every"])
            elif d["repeats_type_id"] == 3:
                repeats = "Every %s Year/s " % (d["repeats_every"])
            if d["statutory_dates"] is not None:
                statutory_dates = json.loads(d["statutory_dates"])
                for index, statutory_date in enumerate(statutory_dates):
                    if index == 0:
                        if(
                            statutory_date["statutory_date"] is not None and
                            statutory_date["statutory_month"] is not None
                        ):
                            repeats += "%s %s, " % (
                                statutory_date["statutory_date"],
                                statutory_date["statutory_month"]
                            )
                        if(statutory_date["trigger_before_days"] is not None):
                            trigger += "%s Days" % (
                                statutory_date["trigger_before_days"]
                            )
                    else:
                        if statutory_date["trigger_before_days"] is not None:
                            trigger += " and %s Days" % (
                                statutory_date["trigger_before_days"]
                            )
            repeats += trigger
        elif d["frequency_id"] == 1:
            statutory_dates = json.loads(d["statutory_dates"])
            for index, statutory_date in enumerate(statutory_dates):
                statutory_date = statutory_dates[0]
                if(
                    statutory_date["statutory_date"] is not None and
                    statutory_date["statutory_month"] is not None
                ):
                    repeats = "%s %s " % (
                        statutory_date["statutory_date"],
                        db.string_months[statutory_date["statutory_month"]]
                    )
                if statutory_date["trigger_before_days"] is not None:
                    trigger += "%s Days " % (
                        statutory_date["trigger_before_days"]
                    )
                repeats += trigger
        elif d["frequency_id"] == 4:
            if d["duration_type_id"] == 1:
                if d["duration"] is not None:
                    repeats = "Complete within %s Day/s " % (d["duration"])
            elif d["duration_type_id"] == 2:  # Hours
                if d["duration"] is not None:
                    repeats = "Complete within %s Hour/s" % (d["duration"])
        compliance = clientreport.Level1Compliance(
            statutory_mapping, compliance_name,
            d["compliance_description"], d["penal_consequences"],
            d["frequency"], repeats
        )
        unit_name = "%s - %s" % (
            d["unit_code"], d["unit_name"]
        )
        address = d["address"] + " - " + str(d["postal_code"])
        unit_wise_comp = clientreport.Level1Statutory(
            unit_id, unit_name, address, [compliance]
        )
        level_1_statutory_wise_units = {}
        level_1_statutory_wise_units[level_1] = [unit_wise_comp]
        report_data = clientreport.RiskData(
            business_group_name, legal_entity, division_name,
            level_1_statutory_wise_units
        )
        legal_wise = report_data_list.get(legal_entity)
        if legal_wise is None:
            legal_wise = report_data
        else:
            level_1_units = legal_wise.level_1_statutory_wise_units.get(
                level_1
            )
            if level_1_units is None:
                level_1_units = []
                level_1_units.append(unit_wise_comp)
            else:
                is_new_unit = True
                for u in level_1_units:
                    if u.unit_id == unit_id:
                        is_new_unit = False
                        c_list = u.compliances
                        if c_list is None:
                            c_list = []
                        c_list.append(compliance)
                        u.compliances = c_list
                if is_new_unit:
                    level_1_units.append(unit_wise_comp)
            legal_wise.level_1_statutory_wise_units[level_1] = level_1_units
        report_data_list[legal_entity] = legal_wise

    final_lst = []
    for k in sorted(report_data_list):
        final_lst.append(report_data_list.get(k))
    return total, final_lst


def get_login_trace(
    db, session_user, from_count, to_count, user_id,
    from_date, to_date
):
    from_date = string_to_datetime(from_date).date()
    to_date = string_to_datetime(to_date).date()
    condition = ""

    query = "SELECT al.created_on, al.action " + \
        " FROM tbl_activity_log al " + \
        " INNER JOIN " + \
        " tbl_users u ON " + \
        " al.user_id  = u.user_id " + \
        " WHERE " + \
        " al.form_id = 0 and al.action not like %s "
    order = " ORDER BY al.created_on desc " + \
            " limit %s, %s"

    param = [str("%" + 'password' + "%")]

    if user_id is not None:
        condition = " AND al.user_id = %s "
        param.append(user_id)

    if from_date is not None and to_date is not None:
        condition += " AND  date(al.created_on) >= %s " + \
            " AND date(al.created_on) <= %s "
        param.extend([from_date, to_date])

    if condition is not None:
        query += condition

    param.extend([from_count, to_count])
    rows = db.select_all(query + order, param)
    columns = ["created_on", "action"]
    result = convert_to_dict(rows, columns)
    return return_logintrace(result)


def return_logintrace(data):
    results = []
    for d in data:
        created_on = datetime_to_string_time(d["created_on"])
        results.append(clientreport.LoginTrace(created_on, d["action"]))
    return results


def get_compliance_activity_report(
    db, country_id, domain_id, user_type, user_id, unit_id, compliance_id,
    level_1_statutory_name, from_date, to_date, session_user
):
    conditions = ""
    condition_val = []
    # assignee_condition
    if user_id is not None:
        conditions += " AND ac.completed_by = %s"
        condition_val.append(user_id)

    # user_type_condition
    if user_type == "Inhouse":
        conditions += " AND us.is_service_provider = 0"
    else:
        conditions += " AND us.is_service_provider = 1"

    # unit_condition
    if unit_id is not None:
        conditions += " AND cal.unit_id = %s "
        condition_val.append(unit_id)

    # session_user_condition
    if not is_admin(db, session_user):
        conditions += " AND u.unit_id in ( " + \
            " SELECT unit_id FROM tbl_user_units WHERE user_id = %s ) "
        condition_val.append(session_user)

    # level_1_statutory_condition
    if level_1_statutory_name is not None:
        conditions += " AND c.statutory_mapping like %s"
        condition_val.append(str('%' + level_1_statutory_name + '%'))

    # compliance_name_condition
    if compliance_id is not None:
        conditions += " AND compliance_task = (SELECT compliance_task " + \
            " FROM tbl_compliances WHERE " + \
            " compliance_id = %s )"
        condition_val.append(compliance_id)

    # timeline_condition
    # [[1, [[1, [{'start_date': datetime.datetime(2016, 5, 1, 5, 30),
    # 'end_date': datetime.datetime(2016, 12, 31, 5, 30),
    # 'year': 2016}]]]]]
    timeline = get_country_domain_timelines(
        db, [country_id], [domain_id],
        [get_date_time_in_date().year]
    )
    year_start_date = timeline[0][1][0][1][0]["start_date"]
    year_end_date = timeline[0][1][0][1][0]["end_date"]
    if from_date is not None and to_date is not None:
        conditions += " AND cal.updated_on between %s and " + \
            " DATE_ADD(%s, INTERVAL 1 DAY)"
        condition_val.extend(
            [
                string_to_datetime(from_date).date(),
                string_to_datetime(to_date).date()
            ]
        )

    elif from_date is not None and to_date is None:
        conditions += " AND cal.updated_on between %s and " + \
            " DATE_ADD(%s, INTERVAL 1 DAY)"
        condition_val.extend([string_to_datetime(
            from_date).date(), year_end_date]
        )

    elif from_date is None and to_date is not None:
        conditions += " AND cal.updated_on between %s and " + \
            " DATE_ADD(%s, INTERVAL 1 DAY)"
        condition_val.extend(
            [
                year_start_date, string_to_datetime(to_date).date()
            ]
        )

    else:
        conditions += " AND cal.updated_on between %s and " + \
            " DATE_ADD(%s, INTERVAL 1 DAY)"
        condition_val.extend([year_start_date, year_end_date])

    query = "SELECT activity_date, activity_status, " + \
        " compliance_status, cal.remarks, " + \
        " concat(unit_code, '-', unit_name), " + \
        " address, document_name, compliance_task, " + \
        " compliance_description, " + \
        " statutory_mapping, ac.completed_by, employee_code, " + \
        " employee_name FROM tbl_compliance_activity_log cal " + \
        " INNER JOIN tbl_compliances c " + \
        " ON (c.compliance_id = cal.compliance_id) " + \
        " INNER JOIN tbl_units u ON (u.unit_id = cal.unit_id) " + \
        " INNER JOIN tbl_compliance_history ac " + \
        " ON ((cal.compliance_id = ac.compliance_id) " + \
        " and (cal.unit_id = ac.unit_id)) " + \
        " INNER JOIN tbl_users us ON (us.user_id = ac.completed_by) " + \
        " WHERE u.country_id = %s " + \
        " AND c.domain_id = %s "
    order = " group by compliance_activity_id " + \
        " ORDER BY cal.updated_on DESC"

    # print query
    param = [country_id, domain_id]
    if conditions != "":
        query += conditions
        param.extend(condition_val)
    result = db.select_all(query + order, param)
    columns = [
        "activity_date", "activity_status", "compliance_status", "remarks",
        "unit_name", "address", "document_name",
        "compliance_name", "description",
        "statutory_mapping", "assignee_id",
        "employee_code", "employee_name"
    ]
    rows = convert_to_dict(result, columns)
    return rows


def return_compliance_activity_report(
    db, country_id, domain_id, user_type, user_id,
    unit_id, compliance_id,
    level_1_statutory_name, from_date, to_date, session_user
):
    rows = get_compliance_activity_report(
        db, country_id, domain_id, user_type, user_id,
        unit_id, compliance_id,
        level_1_statutory_name, from_date, to_date,
        session_user
    )
    unit_wise_activities = {}
    unit_address_mapping = {}
    for row in rows:
        unit_name = row["unit_name"]
        if unit_name not in unit_address_mapping:
            unit_address_mapping[unit_name] = row["address"]
        if unit_name not in unit_wise_activities:
            unit_wise_activities[row["unit_name"]] = {}

        statutories = row["statutory_mapping"].split(">>")
        level_1_statutory = statutories[0]
        if level_1_statutory not in unit_wise_activities[unit_name]:
            unit_wise_activities[unit_name][level_1_statutory] = {}

        compliance_name = row["compliance_name"]
        if row["document_name"] not in [None, "None", ""]:
            compliance_name = "%s - %s" % (
                row["document_name"], compliance_name
            )

        if(
            compliance_name not in
            unit_wise_activities[unit_name][level_1_statutory]
        ):
            unit_wise_activities[
                unit_name
            ][level_1_statutory][compliance_name] = []

        employee_name = row["employee_name"]
        if row["employee_code"] not in ["None", None, ""]:
            employee_name = "%s - %s" % (row["employee_code"], employee_name)
        if row["activity_status"] == "Submited":
            row["activity_status"] = "Submitted"
        unit_wise_activities[
            unit_name
        ][level_1_statutory][compliance_name].append(
            clientreport.ActivityData(
                activity_date=datetime_to_string(row["activity_date"]),
                activity_status=clientcore.COMPLIANCE_ACTIVITY_STATUS(
                    row["activity_status"]
                ),
                compliance_status=clientcore.COMPLIANCE_STATUS(
                    row["compliance_status"]
                ),
                remarks=row["remarks"],
                assignee_name=employee_name
            )
        )

    activities = []
    for unit in unit_wise_activities:
        activities.append(
            clientreport.Activities(
                unit_name=unit,
                address=unit_address_mapping[unit],
                statutory_wise_compliances=unit_wise_activities[unit]
            )
        )
    return activities


def get_compliance_task_applicability(db, request, session_user):
    business_group = request.business_group_id
    legal_entity = request.legal_entity_id
    division_id = request.division_id
    unit = request.unit_id
    from_count = request.record_count
    to_count = 100
    statutory_name = request.statutory_name
    status = request.applicable_status

    def statutory_repeat_text(db, statutory_dates, repeat, repeat_type):
        trigger_days = ""
        repeats_text = ""
        for index, dat in enumerate(statutory_dates):
            if dat["statutory_month"] is not None:
                day = dat["statutory_date"]
                if day == 1:
                    day = "1st"
                elif day == 2:
                    day = "2nd"
                else:
                    day = "%sth" % (day)
                month = db.string_months[dat["statutory_month"]]
                days = dat["trigger_before_days"]
                if index == 0:
                    repeats_text += " %s %s" % (day, month)
                    trigger_days += " %s days" % (days)
                else:
                    repeats_text += " %s %s" % (day, month)
                    trigger_days += " and %s days" % (days)

        if repeats_text == "":
            repeats_text = "Every %s %s" % (repeat, repeat_type)
        else:
            repeats_text = "Every %s" % (repeats_text)

        if trigger_days is not "":
            trigger_days = "triggers (%s)" % (trigger_days)
        result = "%s %s" % (repeats_text, trigger_days)
        return result

    def statutory_duration_text(duration, duration_type):
        result = "To complete within %s %s" % (duration, duration_type)
        return result

    where_qry = ""
    where_qry_val = []
    admin_id = get_admin_id(db)

    if status.lower() == "applicable":
        where_qry += " AND T1.compliance_applicable = 1"
    elif status.lower() == "not applicable":
        where_qry += " AND T1.compliance_applicable = 0"
    else:
        where_qry += " AND T1.compliance_opted = 0"

    if business_group is not None:
        where_qry = " AND T4.business_group_id = %s"
        where_qry_val.append(business_group)

    if legal_entity is not None:
        where_qry += " AND T4.legal_entity_id = %s"
        where_qry_val.append(legal_entity)

    if division_id is not None:
        where_qry += " AND T4.division_id = %s"
        where_qry_val.append(division_id)

    if unit is not None:
        where_qry += " AND T3.unit_id = %s"
        where_qry_val.append(unit)

    if statutory_name is not None:
        where_qry += " AND T2.statutory_mapping like %s"
        where_qry_val.append(str(statutory_name + '%'))

    if session_user != admin_id:
        where_qry += " AND T4.unit_id in " + \
            " (select us.unit_id from tbl_user_units us where " + \
            " us.user_id = %s)"
        where_qry_val.append(session_user)

    act_wise = {}

    q_count = "SELECT count( T2.compliance_id) " + \
        " FROM tbl_client_compliances T1 " + \
        " INNER JOIN tbl_compliances T2 " + \
        " ON T1.compliance_id = T2.compliance_id " + \
        " INNER JOIN tbl_client_statutories T3 " + \
        " ON T1.client_statutory_id = T3.client_statutory_id " + \
        " INNER JOIN tbl_units T4 " + \
        " ON T3.unit_id = T4.unit_id " + \
        " WHERE T3.country_id = %s " + \
        " AND T3.domain_id = %s "

    param = [request.country_id, request.domain_id]
    if where_qry != "":
        q_count += where_qry
        param.extend(where_qry_val)

    row = db.select_one(q_count, param)
    if row:
        total = int(row[0])
    else:
        total = 0

    query = "SELECT distinct T2.compliance_id, T2.statutory_provision, " + \
        " T2.statutory_mapping, " + \
        " T2.compliance_task, T2.document_name, T2.format_file, " + \
        " T2.penal_consequences, T2.compliance_description, " + \
        " T2.statutory_dates, (select frequency " + \
        " from tbl_compliance_frequency where " + \
        " frequency_id = T2.frequency_id) as frequency, " + \
        " (select business_group_name from tbl_business_groups " + \
        " where business_group_id = T4.business_group_id)business_group, " + \
        " (select legal_entity_name from tbl_legal_entities " + \
        " where legal_entity_id = T4.legal_entity_id)legal_entity, " + \
        " (select division_name from tbl_divisions " + \
        " where division_id = T4.division_id )division_name, " + \
        " T4.unit_id, T4.unit_code, T4.unit_name, T4.address, " + \
        " T4.postal_code, T1.statutory_applicable, " + \
        "  T1.statutory_opted, T1.compliance_opted, " + \
        " (select repeat_type from tbl_compliance_repeat_type where " + \
        " repeat_type_id = T2.repeats_type_id) repeat_type, " + \
        " (select duration_type from tbl_compliance_duration_type where " + \
        " duration_type_id = T2.duration_type_id) duration_type , " + \
        " T2.repeats_every, T2.duration " + \
        " FROM tbl_client_compliances T1 " + \
        " INNER JOIN tbl_compliances T2 " + \
        " ON T1.compliance_id = T2.compliance_id " + \
        " INNER JOIN tbl_client_statutories T3 " + \
        " ON T1.client_statutory_id = T3.client_statutory_id " + \
        " INNER JOIN tbl_units T4 " + \
        " ON T3.unit_id = T4.unit_id " + \
        " WHERE T3.country_id = %s " + \
        " AND T3.domain_id = %s "
    order = " limit %s, %s"

    param = [request.country_id, request.domain_id]
    if where_qry != "":
        query += where_qry
        param.extend(where_qry_val)

    param.extend([from_count, to_count])
    rows = db.select_all(query + order, param)
    columns = [
        "compliance_id", "statutory_provision", "statutory_mapping",
        "compliance_task", "document_name", "format_file",
        "penal_consequences", "compliance_description",
        "statutory_dates", "frequency",
        "business_group", "legal_entity", "division_name",
        "unit_id", "unit_code", "unit_name", "address",
        "postal_code", "statutory_applicable",
        "statutory_opted", "compliance_opted",
        "repeat_type", "duration_type", "repeats_every",
        "duration"
    ]
    result = convert_to_dict(rows, columns)
    legal_entity_wise = {}
    for r in result:
        business_group_name = r["business_group"]
        legal_entity_name = r["legal_entity"]
        division_name = r["division_name"]
        unit_id = r["unit_id"]
        name = "%s - %s" % (r["unit_code"], r["unit_name"])
        mapping = r["statutory_mapping"].split(">>")
        address = "%s - %s" % (r["address"], r["postal_code"])
        level_1_statutory = mapping[0]
        level_1_statutory = level_1_statutory.strip()

        document_name = r["document_name"]
        if document_name not in (None, "None", ""):
            compliance_name = "%s - %s" % (document_name, r["compliance_task"])
        else:
            compliance_name = r["compliance_task"]

        statutory_dates = json.loads(r["statutory_dates"])
        repeat_text = ""
        repeats_every = r["repeats_every"]
        repeat_type = r["repeat_type"]
        if repeats_every:
            repeat_text = statutory_repeat_text(
                db, statutory_dates, repeats_every, repeat_type
            )

        duration = r["duration"]
        duration_type = r["duration_type"]
        if duration:
            repeat_text = statutory_duration_text(duration, duration_type)

        compliance_name_list = [compliance_name]
        format_file = r["format_file"]
        if format_file:
            compliance_name_list.append("%s/%s" % (
                FORMAT_DOWNLOAD_URL, format_file)
            )
        compliance = clientreport.ComplianceList(
            r["statutory_provision"] + r["statutory_mapping"],
            compliance_name_list,
            r["compliance_description"],
            r["penal_consequences"],
            clientcore.COMPLIANCE_FREQUENCY(r["frequency"]),
            repeat_text
        )
        unit_data = clientreport.ApplicabilityCompliance(
            unit_id, name, address, [compliance]
        )

        legal_wise = legal_entity_wise.get(legal_entity_name)
        if legal_wise is None:
            act_wise = {}
            act_wise[level_1_statutory] = [unit_data]
            legal_wise = clientreport.GetComplianceTaskApplicabilityStatusReportData(
                business_group_name, legal_entity_name, division_name,
                act_wise
            )
            # legal_entity_wise[legal_entity_name] = legal_wise
        else:
            act_wise = legal_wise.actwise_units
            unit_wise = act_wise.get(level_1_statutory)

            if unit_wise is None:
                unit_wise = []
                unit_wise.append(unit_data)
            else:
                is_new_unit = True
                for u in unit_wise:
                    if u.unit_id == unit_id:
                        is_new_unit = False
                        c_list = u.compliances
                        if c_list is None:
                            c_list = []
                        c_list.append(compliance)
                        u.compliances = c_list

                if is_new_unit:
                    unit_wise.append(unit_data)

            act_wise[level_1_statutory] = unit_wise
            legal_wise.actwise_units = act_wise
        legal_entity_wise[legal_entity_name] = legal_wise

    lst = []
    for k in sorted(legal_entity_wise):
        lst.append(legal_entity_wise.get(k))
    return clientreport.GetComplianceTaskApplicabilityStatusReportSuccess(
        total, lst
    )


def get_client_details_report(
    db, country_id,  business_group_id, legal_entity_id, division_id,
    unit_id, domain_ids, session_user, from_count, page_count
):
    condition, condition_val = get_client_details_condition(
        db, country_id,  business_group_id, legal_entity_id, division_id,
        unit_id, domain_ids, session_user
    )
    columns = "unit_id, unit_code, unit_name, geography, " + \
        " address, domain_ids, postal_code, " + \
        " business_group_name, legal_entity_name, division_name"

    query = "SELECT unit_id, unit_code, unit_name, geography, " + \
            " address, domain_ids, postal_code, business_group_name, " + \
            " legal_entity_name, division_name " + \
            " FROM tbl_units u " +\
            " LEFT JOIN tbl_business_groups b " + \
            " ON (b.business_group_id = u.business_group_id) " + \
            " INNER JOIN tbl_legal_entities l " + \
            " ON (l.legal_entity_id = u.legal_entity_id) " + \
            " LEFT JOIN tbl_divisions d " + \
            " ON (d.division_id = u.division_id) " + \
            " WHERE "

    order = " ORDER BY u.business_group_id, u.legal_entity_id," + \
            " u.division_id, u.unit_id ASC LIMIT %s, %s"
    param = []
    if condition is not None:
        query += condition
        param.extend(condition_val)
    param.extend([from_count, page_count])

    rows = db.select_all(query + order, param)

    columns_list = columns.replace(" ", "").split(",")
    unit_rows = convert_to_dict(rows, columns_list)
    # units = []
    grouped_units = {}
    for unit in unit_rows:
        business_group_name = unit["business_group_name"]
        legal_entity_name = unit["legal_entity_name"]
        division_name = unit["division_name"]
        if business_group_name in ["None", None, ""]:
            business_group_name = "null"
        if division_name in ["None", None, ""]:
            division_name = "null"
        if business_group_name not in grouped_units:
            grouped_units[business_group_name] = {}
        if legal_entity_name not in grouped_units[business_group_name]:
            grouped_units[business_group_name][legal_entity_name] = {}
        if division_name not in grouped_units[
            business_group_name
        ][legal_entity_name]:
            grouped_units[
                business_group_name
            ][legal_entity_name][division_name] = []

        grouped_units[
            business_group_name
        ][legal_entity_name][division_name].append(
            clientreport.UnitDetails(
                unit["unit_id"], unit["geography"], unit["unit_code"],
                unit["unit_name"], unit["address"], unit["postal_code"],
                [int(x) for x in unit["domain_ids"].split(",")]
            )
        )
    GroupedUnits = []
    for business_group in grouped_units:
        for legal_entity_name in grouped_units[business_group]:
            for division in grouped_units[business_group][legal_entity_name]:
                if business_group == "null":
                    business_group_name = None
                else:
                    business_group_name = business_group
                if division == "null":
                    division_name = None
                else:
                    division_name = division
                GroupedUnits.append(
                    clientreport.GroupedUnits(
                        division_name, legal_entity_name, business_group_name,
                        grouped_units[
                            business_group
                        ][legal_entity_name][division]
                    )
                )
    return GroupedUnits


def get_client_details_condition(
    db, country_id,  business_group_id, legal_entity_id, division_id,
    unit_id, domain_ids, session_user
):
    user_unit_ids = get_user_unit_ids(db, session_user)
    condition = "u.country_id = %s "
    condition_val = [country_id]
    if business_group_id is not None:
        condition += " AND u.business_group_id = %s "
        condition_val.append(business_group_id)

    if legal_entity_id is not None:
        condition += " AND u.legal_entity_id = %s "
        condition_val.append(legal_entity_id)

    if division_id is not None:
        condition += " AND u.division_id = %s "
        condition_val.append(division_id)

    if unit_id is not None:
        condition += " AND unit_id = %s "
        condition_val.append(unit_id)

    else:
        unit_condition, unit_condition_val = db.generate_tuple_condition(
            "unit_id", user_unit_ids
        )
        condition += " AND %s " % unit_condition
        condition_val.append(unit_condition_val)

    if domain_ids is not None:
        dm_con = ""
        for i, domain_id in enumerate(domain_ids):
            if i == 0:
                dm_con += " FIND_IN_SET(%s, domain_ids)" % (domain_id)
            elif i > 0:
                dm_con += " OR FIND_IN_SET(%s, domain_ids) " % (domain_id)
        condition += " AND (%s)" % dm_con
    return condition, condition_val


def get_client_details_count(
    db, country_id,  business_group_id, legal_entity_id, division_id,
    unit_id, domain_ids, session_user
):

    condition, condition_val = get_client_details_condition(
        db, country_id,  business_group_id, legal_entity_id, division_id,
        unit_id, domain_ids, session_user
    )
    query = "SELECT count(*) " + \
            " FROM %s u " + \
            " WHERE "
    query = query % (tblUnits)
    query += condition
    rows = db.select_all(query, condition_val)
    count = 0
    if rows:
        count = rows[0][0]
    return count


def get_service_provider_user_ids(db, service_provider_id):
    columns = "user_id"
    condition = " service_provider_id = %s and is_service_provider = 1"
    rows = db.get_data(tblUsers, columns, condition, [service_provider_id])
    user_ids = [
        int(row["user_id"]) for row in rows
    ]
    return ",".join(str(x) for x in user_ids)


def get_service_provider_user_unit_ids(db, user_ids):
    columns = "unit_id"
    condition = " user_id in (%s)"
    rows = db.get_data(tblUserUnits, columns, condition, [user_ids])
    unit_ids = [
        int(row["unit_id"]) for row in rows
    ]
    return ",".join(str(x) for x in unit_ids)


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

    select_qry = "select t3.country_id, t1.legal_entity_id, t3.domain_id, t1.unit_id, t1.compliance_id, t1.due_date,  " + \
        "t1.documents, t1.completed_on, t1.completion_date, t1.approve_status, " + \
        "(select concat(unit_code,'-',unit_name,',',address,',',postal_code)" + \
        "from tbl_units where unit_id = t1.unit_id) as unit_name, t3.statutory_mapping, " + \
        "(select geography_name from tbl_units where unit_id = t1.unit_id) as geo_name, " + \
        "t3.compliance_task, (select frequency from tbl_compliance_frequency where " + \
        "frequency_id = t3.frequency_id) as frequency_name, (select " + \
        "concat(employee_code,'-',employee_name) from tbl_users where user_id = t1.completed_by) " + \
        "as assignee_name, t1.completed_by, t2.activity_on, t3.format_file, t3.format_file_size, " + \
        "(select logo from tbl_legal_entities where legal_entity_id = t1.legal_entity_id) as logo, " + \
        "(select logo_size from tbl_legal_entities where legal_entity_id = t1.legal_entity_id) as logo_size "
    from_clause = "from tbl_compliance_history as t1 left join tbl_compliance_activity_log as t2 " + \
        "on t2.compliance_id = t1.compliance_id and t2.unit_id = t1.unit_id " + \
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
        where_clause = where_clause + " and t1.due_date between " + \
            " DATE_SUB(%s, INTERVAL 1 DAY)  and " + \
            " DATE_ADD(%s, INTERVAL 1 DAY) "
        condition_val.extend([due_from, due_to])
    elif due_from is not None and due_to is None:
        due_from = string_to_datetime(due_from).date()
        where_clause = where_clause + " and t1.due_date between " + \
            " DATE_SUB(%s, INTERVAL 1 DAY)  and " + \
            " DATE_ADD(curdate(), INTERVAL 1 DAY) "
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

    where_clause = where_clause + \
        "and t1.legal_entity_id = %s group by t1.compliance_history_id order by t1.due_date desc limit %s, %s;"
    condition_val.extend([legal_entity_id, int(
        request.from_count), int(request.page_count)])
    query = select_qry + from_clause + where_clause
    print "qry"
    print condition_val
    print query
    result = db.select_all(query, condition_val)
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
            if row["approve_status"] == "0":
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

        format_file = row["format_file"]
        format_file_size = row["format_file_size"]
        if format_file_size is not None:
            format_file_size = int(format_file_size)
        if format_file:
            url = "%s/%s" % (
                CLIENT_DOCS_DOWNLOAD_URL, format_file
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
            row["country_id"], row["legal_entity_id"], row[
                "domain_id"], row["unit_id"],
            row["compliance_id"], unit_name, statutory_mapping, row[
                "compliance_task"],
            row["frequency_name"], datetime_to_string(
                row["due_date"]), task_status, row["assignee_name"],
            activity_status, datetime_to_string(row["activity_on"]), name,
            datetime_to_string(row["completion_date"]), url, logo_url
        ))
    return le_report

##########################################################################
# Objective: To get the compliance list under filtered data
# Parameter: request object
# Result: list of compliance grouped by unit and act
##########################################################################


def process_domain_wise_report(db, request):
    # u_type = ("Assignee", "Concurrence", "Approval")
    # status = ("Complied", "Delayed Compliance", "Inprogress", "Not Complied")
    where_clause = None
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

    select_qry = "select t3.country_id, t1.legal_entity_id, t3.domain_id, t1.unit_id, t1.compliance_id, t1.due_date,  " + \
        "t1.documents, t1.completed_on, t1.completion_date, t1.approve_status, " + \
        "(select concat(unit_code,'-',unit_name,',',address,',',postal_code)" + \
        "from tbl_units where unit_id = t1.unit_id) as unit_name, t3.statutory_mapping, " + \
        "(select geography_name from tbl_units where unit_id = t1.unit_id) as geo_name, " + \
        "t3.compliance_task, (select frequency from tbl_compliance_frequency where " + \
        "frequency_id = t3.frequency_id) as frequency_name, (select " + \
        "concat(employee_code,'-',employee_name) from tbl_users where user_id = t1.completed_by) " + \
        "as assignee_name, t1.completed_by, t2.activity_on, t3.format_file, t3.format_file_size, " + \
        "(select logo from tbl_legal_entities where legal_entity_id = t1.legal_entity_id) as logo, " + \
        "(select logo_size from tbl_legal_entities where legal_entity_id = t1.legal_entity_id) as logo_size "
    from_clause = "from tbl_compliance_history as t1 left join tbl_compliance_activity_log as t2 " + \
        "on t2.compliance_id = t1.compliance_id and t2.unit_id = t1.unit_id " + \
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
        where_clause = where_clause + " and t1.due_date between " + \
            " DATE_SUB(%s, INTERVAL 1 DAY)  and " + \
            " DATE_ADD(%s, INTERVAL 1 DAY) "
        condition_val.extend([due_from, due_to])
    elif due_from is not None and due_to is None:
        due_from = string_to_datetime(due_from).date()
        where_clause = where_clause + " and t1.due_date between " + \
            " DATE_SUB(%s, INTERVAL 1 DAY)  and " + \
            " DATE_ADD(curdate(), INTERVAL 1 DAY) "
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

    where_clause = where_clause + \
        "and t1.legal_entity_id = %s group by t1.compliance_history_id order by t1.due_date desc limit %s, %s;"
    condition_val.extend([legal_entity_id, int(
        request.from_count), int(request.page_count)])
    query = select_qry + from_clause + where_clause
    # print "qry"
    # print query
    result = db.select_all(query, condition_val)
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
        print row["activity_on"]
        if row["activity_on"] is None:
            print row["approve_status"]
            if row["approve_status"] == "0":
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

        format_file = row["format_file"]
        format_file_size = row["format_file_size"]
        if format_file_size is not None:
            format_file_size = int(format_file_size)
        if format_file:
            url = "%s/%s" % (
                CLIENT_DOCS_DOWNLOAD_URL, format_file
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
            row["country_id"], row["legal_entity_id"], row[
                "domain_id"], row["unit_id"],
            row["compliance_id"], unit_name, statutory_mapping, row[
                "compliance_task"],
            row["frequency_name"], datetime_to_string(
                row["due_date"]), task_status, row["assignee_name"],
            activity_status, datetime_to_string(row["activity_on"]), name,
            datetime_to_string(row["completion_date"]), url, logo_url
        ))
    return le_report


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

    select_qry = "select t3.country_id, t1.legal_entity_id, t3.domain_id, t1.unit_id, t1.compliance_id, t1.due_date,  " + \
        "t1.documents, t1.completed_on, t1.completion_date, t1.approve_status, " + \
        "(select concat(unit_code,'-',unit_name,',',address,',',postal_code)" + \
        "from tbl_units where unit_id = t1.unit_id) as unit_name, t3.statutory_mapping, " + \
        "(select geography_name from tbl_units where unit_id = t1.unit_id) as geo_name, " + \
        "t3.compliance_task, (select frequency from tbl_compliance_frequency where " + \
        "frequency_id = t3.frequency_id) as frequency_name, (select " + \
        "concat(employee_code,'-',employee_name) from tbl_users where user_id = t1.completed_by) " + \
        "as assignee_name, t1.completed_by, t2.activity_on, t3.format_file, t3.format_file_size, " + \
        "(select domain_name from tbl_domains where domain_id = t3.domain_id) as domain_name, " + \
        "(select logo from tbl_legal_entities where legal_entity_id = t1.legal_entity_id) as logo, " + \
        "(select logo_size from tbl_legal_entities where legal_entity_id = t1.legal_entity_id) as logo_size "
    from_clause = "from tbl_compliance_history as t1 left join tbl_compliance_activity_log as t2 " + \
        "on t2.compliance_id = t1.compliance_id and t2.unit_id = t1.unit_id " + \
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
        print due_from
        due_to = string_to_datetime(due_to).date()
        print due_to
        where_clause = where_clause + " and t1.due_date between " + \
            " DATE_SUB(%s, INTERVAL 1 DAY)  and " + \
            " DATE_ADD(%s, INTERVAL 1 DAY) "
        condition_val.extend([due_from, due_to])
    elif due_from is not None and due_to is None:
        due_from = string_to_datetime(due_from).date()
        where_clause = where_clause + " and t1.due_date between " + \
            " DATE_SUB(%s, INTERVAL 1 DAY)  and " + \
            " DATE_ADD(curdate(), INTERVAL 1 DAY) "
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

    where_clause = where_clause + \
        "and t1.legal_entity_id = %s and t1.unit_id = %s  group by t1.compliance_history_id order by t1.due_date desc limit %s, %s;"
    condition_val.extend([legal_entity_id, request.unit_id, int(
        request.from_count), int(request.page_count)])
    query = select_qry + from_clause + where_clause
    print "qry"
    print query
    result = db.select_all(query, condition_val)
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
            if row["approve_status"] == "0":
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

        format_file = row["format_file"]
        format_file_size = row["format_file_size"]
        if format_file_size is not None:
            format_file_size = int(format_file_size)
        if format_file:
            url = "%s/%s" % (
                CLIENT_DOCS_DOWNLOAD_URL, format_file
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
            row["country_id"], row["legal_entity_id"], row[
                "domain_id"], row["unit_id"],
            row["compliance_id"], unit_name, statutory_mapping, row[
                "compliance_task"],
            row["frequency_name"], datetime_to_string(
                row["due_date"]), task_status, row["assignee_name"],
            activity_status, datetime_to_string(row["activity_on"]), name,
            datetime_to_string(row["completion_date"]), url, row[
                "domain_name"], logo_url
        ))
    return unit_report

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
            row["domain_id"], row["unit_id"], row[
                "compliance_id"], sp_id_optional,
            row["user_id"], row["username"]
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

    select_qry = "select t3.country_id, t1.legal_entity_id, t3.domain_id, t1.unit_id, t1.compliance_id, t1.due_date,  " + \
        "t1.documents, t1.completed_on, t1.completion_date, t1.approve_status, " + \
        "(select concat(unit_code,'-',unit_name,',',address,',',postal_code)" + \
        "from tbl_units where unit_id = t1.unit_id) as unit_name, t3.statutory_mapping, " + \
        "(select geography_name from tbl_units where unit_id = t1.unit_id) as geo_name, " + \
        "t3.compliance_task, (select frequency from tbl_compliance_frequency where " + \
        "frequency_id = t3.frequency_id) as frequency_name, (select " + \
        "concat(employee_code,'-',employee_name) from tbl_users where user_id = t1.completed_by) " + \
        "as assignee_name, t1.completed_by, t2.activity_on, t3.format_file, t3.format_file_size, " + \
        "(select logo from tbl_legal_entities where legal_entity_id = t1.legal_entity_id) as logo, " + \
        "(select logo_size from tbl_legal_entities where legal_entity_id = t1.legal_entity_id) as logo_size "
    from_clause = "from tbl_users as t4 inner join tbl_compliance_history as t1 " + \
        "on (t1.completed_by=t4.user_id or t1.concurred_by=t4.user_id or t1.approved_by=t4.user_id) " + \
        "left join tbl_compliance_activity_log as t2 " + \
        "on t2.compliance_id = t1.compliance_id and t2.unit_id = t1.unit_id " + \
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
        where_clause = where_clause + " and t1.due_date between " + \
            " DATE_SUB(%s, INTERVAL 1 DAY)  and " + \
            " DATE_ADD(%s, INTERVAL 1 DAY) "
        condition_val.extend([due_from, due_to])
    elif due_from is not None and due_to is None:
        due_from = string_to_datetime(due_from).date()
        where_clause = where_clause + " and t1.due_date between " + \
            " DATE_SUB(%s, INTERVAL 1 DAY)  and " + \
            " DATE_ADD(curdate(), INTERVAL 1 DAY) "
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
        " group by t1.compliance_history_id order by t1.due_date desc limit %s, %s;"
    condition_val.extend([sp_id, legal_entity_id, int(
        request.from_count), int(request.page_count)])
    query = select_qry + from_clause + where_clause
    print "qry"
    print query
    result = db.select_all(query, condition_val)
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
            if row["approve_status"] == "0":
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

        format_file = row["format_file"]
        format_file_size = row["format_file_size"]
        if format_file_size is not None:
            format_file_size = int(format_file_size)
        if format_file:
            url = "%s/%s" % (
                CLIENT_DOCS_DOWNLOAD_URL, format_file
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
            row["country_id"], row["legal_entity_id"], row[
                "domain_id"], row["unit_id"],
            row["compliance_id"], unit_name, statutory_mapping, row[
                "compliance_task"],
            row["frequency_name"], datetime_to_string(
                row["due_date"]), task_status, row["assignee_name"],
            activity_status, datetime_to_string(row["activity_on"]), name,
            datetime_to_string(row["completion_date"]), url, logo_url
        ))
    return sp_report

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

    select_qry = "select t3.country_id, t1.legal_entity_id, t3.domain_id, t1.unit_id, t1.compliance_id, t1.due_date,  " + \
        "t1.documents, t1.completed_on, t1.completion_date, t1.approve_status, " + \
        "(select concat(unit_code,'-',unit_name,',',address,',',postal_code)" + \
        "from tbl_units where unit_id = t1.unit_id) as unit_name, t3.statutory_mapping, " + \
        "(select geography_name from tbl_units where unit_id = t1.unit_id) as geo_name, " + \
        "t3.compliance_task, (select frequency from tbl_compliance_frequency where " + \
        "frequency_id = t3.frequency_id) as frequency_name, (select " + \
        "concat(employee_code,'-',employee_name) from tbl_users where user_id = t1.completed_by) " + \
        "as assignee_name, t1.completed_by, t2.activity_on, t3.format_file, t3.format_file_size, " + \
        "(select domain_name from tbl_domains where domain_id = t3.domain_id) as domain_name, " + \
        "(select logo from tbl_legal_entities where legal_entity_id = t1.legal_entity_id) as logo, " + \
        "(select logo_size from tbl_legal_entities where legal_entity_id = t1.legal_entity_id) as logo_size "
    from_clause = "from tbl_compliance_history as t1 left join tbl_compliance_activity_log as t2 " + \
        "on t2.compliance_id = t1.compliance_id and t2.unit_id = t1.unit_id " + \
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
        where_clause = where_clause + " and t1.due_date between " + \
            " DATE_SUB(%s, INTERVAL 1 DAY)  and " + \
            " DATE_ADD(%s, INTERVAL 1 DAY) "
        condition_val.extend([due_from, due_to])
    elif due_from is not None and due_to is None:
        due_from = string_to_datetime(due_from).date()
        where_clause = where_clause + " and t1.due_date between " + \
            " DATE_SUB(%s, INTERVAL 1 DAY)  and " + \
            " DATE_ADD(curdate(), INTERVAL 1 DAY) "
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

    where_clause = where_clause + \
        "and t1.legal_entity_id = %s group by t1.compliance_history_id order by t1.due_date desc limit %s, %s;"
    condition_val.extend([legal_entity_id, int(
        request.from_count), int(request.page_count)])
    query = select_qry + from_clause + where_clause
    print "qry"
    print query
    result = db.select_all(query, condition_val)
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
            if row["approve_status"] == "0":
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

        format_file = row["format_file"]
        format_file_size = row["format_file_size"]
        if format_file_size is not None:
            format_file_size = int(format_file_size)
        if format_file:
            url = "%s/%s" % (
                CLIENT_DOCS_DOWNLOAD_URL, format_file
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
            row["country_id"], row["legal_entity_id"], row[
                "domain_id"], row["unit_id"],
            row["compliance_id"], unit_name, statutory_mapping, row[
                "compliance_task"],
            row["frequency_name"], datetime_to_string(
                row["due_date"]), task_status, row["assignee_name"],
            activity_status, datetime_to_string(row["activity_on"]), name,
            datetime_to_string(row["completion_date"]), url, row[
                "domain_name"], logo_url
        ))
    return user_report

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

    if int(business_group_id) > 0:
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

    if int(business_group_id) > 0:
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
        if row["is_closed"] == "0":
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
    return unit_report


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
        where_clause = where_clause + " and t3.created_on between " + \
            " DATE_SUB(%s, INTERVAL 1 DAY)  and " + \
            " DATE_ADD(%s, INTERVAL 1 DAY) "
        condition_val.extend([due_from, due_to])
    elif due_from is not None and due_to is None:
        due_from = string_to_datetime(due_from).date()
        where_clause = where_clause + " and t3.created_on between " + \
            " DATE_SUB(%s, INTERVAL 1 DAY)  and " + \
            " DATE_ADD(curdate(), INTERVAL 1 DAY) "
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
    return statutory_notification

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
        "concat(employee_code,' - ',employee_name) from tbl_users where user_id " + \
        "= t1.user_id) as user_name, (select logo from tbl_legal_entities where legal_entity_id = t1.legal_entity_id) " + \
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
        where_clause = where_clause + " and t1.created_on between " + \
            " DATE_SUB(%s, INTERVAL 1 DAY)  and " + \
            " DATE_ADD(%s, INTERVAL 1 DAY) "
        condition_val.extend([due_from, due_to])
    elif due_from is not None and due_to is None:
        due_from = string_to_datetime(due_from).date()
        where_clause = where_clause + " and t1.created_on between " + \
            " DATE_SUB(%s, INTERVAL 1 DAY)  and " + \
            " DATE_ADD(curdate(), INTERVAL 1 DAY) "
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

        activity_list.append(clientreport.AuditTrailActivities(
            row["user_id"], row["user_name"], row["form_id"],
            row["action"], datetime_to_string_time(row["created_on"]), logo_url
        ))
    return activity_list


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
            "(select compliance_id from tbl_assign_compliances) order by t2.compliance_task asc limit %s, %s;"
        condition_val.extend([legal_entity_id, int(
            request.from_count), int(request.page_count)])

        query = union_qry + union_from_clause + union_where_clause
        print "qry1"
        print query
        result_1 = db.select_all(query, condition_val)
        print result_1
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
                url = "%s/%s" % (
                    CLIENT_DOCS_DOWNLOAD_URL, format_file
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
                row["penal_consequences"], None, None, task_status, document_name, url, logo_url, None, None,
                None, None, None, None, None, comp_remarks=None
            ))
        print len(risk_report)
        condition_val = []
        # other compliance
        select_qry = "select t3.statutory_mapping, (select concat(unit_code,'-',unit_name,',', " + \
            "address,',',postal_code) from tbl_units where unit_id = t1.unit_id) as unit_name, t3.compliance_task, " + \
            "(select frequency from tbl_compliance_frequency where frequency_id = t3.frequency_id) as frequency_name, " + \
            "(select geography_name from tbl_units where unit_id = t1.unit_id) as geo_name, " + \
            "(select concat(employee_code,'-',employee_name) from tbl_users where user_id = t6.assigned_by) as " + \
            "admin_incharge, (select concat(employee_code,'-',employee_name) from tbl_users where user_id = " + \
            "t1.completed_by) as assignee_name, t3.penal_consequences, t3.format_file, t3.format_file_size, " + \
            "(select logo from tbl_legal_entities where legal_entity_id = t1.legal_entity_id) as logo, " + \
            "(select logo_size from tbl_legal_entities where legal_entity_id = t1.legal_entity_id) as logo_size, " + \
            "t1.completion_date, t1.due_date, t1.approve_status, t5.compliance_opted_status, t1.start_date, " + \
            "t1.due_date, (select concat(employee_code,'-',employee_name) from tbl_users where user_id = " + \
            "t1.concurred_by) as concurrer_name, (select concat(employee_code,'-',employee_name) from tbl_users " + \
            "where user_id = t1.approved_by) as approver_name, t1.remarks, t1.documents, t1.completed_on as " + \
            "assigned_on, t1.concurred_on, t1.approved_on "

        from_clause = "from tbl_compliance_history as t1 left join tbl_compliance_activity_log as t2 " + \
            "on t2.compliance_id = t1.compliance_id and t2.unit_id = t1.unit_id inner join " + \
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
                "and t1.approve_status <> 1"

        compliance_id = request.compliance_id
        if int(compliance_id) > 0:
            where_clause = where_clause + "and t1.compliance_id = %s "
            condition_val.append(compliance_id)

        unit_id = request.unit_id
        if int(unit_id) > 0:
            where_clause = where_clause + "and t1.unit_id = %s "
            condition_val.append(unit_id)

        where_clause = where_clause + \
            "and t1.legal_entity_id = %s group by t1.approve_status and t1.compliance_history_id order by t3.compliance_task asc limit %s, %s;"
        condition_val.extend([legal_entity_id, int(
            request.from_count), int(request.page_count)])

        query = select_qry + from_clause + where_clause
        print "qry"
        print query

        result = db.select_all(query, condition_val)
        print result
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

            format_file = row["format_file"]
            format_file_size = row["format_file_size"]
            if format_file_size is not None:
                format_file_size = int(format_file_size)
            if format_file:
                url = "%s/%s" % (
                    CLIENT_DOCS_DOWNLOAD_URL, format_file
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
        print len(risk_report)
    elif task_status == "Unassigned Compliance":
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
            "(select compliance_id from tbl_assign_compliances) order by t2.compliance_task asc limit %s, %s;"
        condition_val.extend([legal_entity_id, int(
            request.from_count), int(request.page_count)])

        query = union_qry + union_from_clause + union_where_clause
        print "qry1"
        print query
        result_1 = db.select_all(query, condition_val)

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
                url = "%s/%s" % (
                    CLIENT_DOCS_DOWNLOAD_URL, format_file
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
                row["penal_consequences"], None, None, task_status, document_name, url, logo_url, None, None,
                None, None, None, None, None, comp_remarks=None
            ))
        print len(risk_report)
        condition_val = []
        print len(risk_report)
    elif (task_status != "All" or task_status != "Unassigned Compliance"):
        print "a"
        condition_val = []
        # other compliance
        select_qry = "select t3.statutory_mapping, (select concat(unit_code,'-',unit_name,',', " + \
            "address,',',postal_code) from tbl_units where unit_id = t1.unit_id) as unit_name, t3.compliance_task, " + \
            "(select frequency from tbl_compliance_frequency where frequency_id = t3.frequency_id) as frequency_name, " + \
            "(select geography_name from tbl_units where unit_id = t1.unit_id) as geo_name, " + \
            "(select concat(employee_code,'-',employee_name) from tbl_users where user_id = t6.assigned_by) as " + \
            "admin_incharge, (select concat(employee_code,'-',employee_name) from tbl_users where user_id = " + \
            "t1.completed_by) as assignee_name, t3.penal_consequences, t3.format_file, t3.format_file_size, " + \
            "(select logo from tbl_legal_entities where legal_entity_id = t1.legal_entity_id) as logo, " + \
            "(select logo_size from tbl_legal_entities where legal_entity_id = t1.legal_entity_id) as logo_size, " + \
            "t1.completion_date, t1.due_date, t1.approve_status, t5.compliance_opted_status, t1.start_date, " + \
            "t1.due_date, (select concat(employee_code,'-',employee_name) from tbl_users where user_id = " + \
            "t1.concurred_by) as concurrer_name, (select concat(employee_code,'-',employee_name) from tbl_users " + \
            "where user_id = t1.approved_by) as approver_name, t1.remarks, t1.documents, t1.completed_on as " + \
            "assigned_on, t1.concurred_on, t1.approved_on "

        from_clause = "from tbl_compliance_history as t1 left join tbl_compliance_activity_log as t2 " + \
            "on t2.compliance_id = t1.compliance_id and t2.unit_id = t1.unit_id inner join " + \
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
                "and t1.approve_status <> 1"

        compliance_id = request.compliance_id
        if int(compliance_id) > 0:
            where_clause = where_clause + "and t1.compliance_id = %s "
            condition_val.append(compliance_id)

        unit_id = request.unit_id
        if int(unit_id) > 0:
            where_clause = where_clause + "and t1.unit_id = %s "
            condition_val.append(unit_id)

        where_clause = where_clause + \
            "and t1.legal_entity_id = %s group by t1.approve_status and t1.compliance_history_id order by t3.compliance_task asc limit %s, %s;"
        condition_val.extend([legal_entity_id, int(
            request.from_count), int(request.page_count)])

        query = select_qry + from_clause + where_clause
        print "qry"
        print query

        result = db.select_all(query, condition_val)
        print result
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

            format_file = row["format_file"]
            format_file_size = row["format_file_size"]
            if format_file_size is not None:
                format_file_size = int(format_file_size)
            if format_file:
                url = "%s/%s" % (
                    CLIENT_DOCS_DOWNLOAD_URL, format_file
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
    print len(risk_report)
    return risk_report
