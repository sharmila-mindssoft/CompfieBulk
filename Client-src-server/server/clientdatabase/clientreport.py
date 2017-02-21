import datetime
from server.clientdatabase.tables import *
from clientprotocol import (
    clientcore, clientreport, clientmasters
)
import json
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
__all__ = [
    "report_unitwise_compliance",
    "return_unitwise_report",
    "report_assigneewise_compliance",
    "return_assignee_report_data",
    "report_serviceproviderwise_compliance",
    "return_serviceprovider_report_data",
    "report_statutory_notifications_list",
    "report_compliance_details",
    "report_reassigned_history",
    "report_reassigned_history_total",
    "report_status_report_consolidated",
    "report_status_report_consolidated_total",
    "report_statutory_settings_unit_Wise",
    "report_statutory_settings_unit_Wise_total",
    "report_domain_score_card",
    "report_le_wise_score_card",
    "report_work_flow_score_card",
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
    "process_audit_trail_report"
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
                int(year_list[0]), int(r_c[1])+1, 1
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
    print rows

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
    query = "select t01.num,acl.compliance_activity_id,ch.compliance_history_id, ch.legal_entity_id,ch.unit_id, " + \
            "(select concat(unit_code,' - ',unit_name,' - ',address) from tbl_units where unit_id = ch.unit_id) as unit,ch.compliance_id, " + \
            "concat(com.document_name,' - ',com.compliance_task) as compliance_name, " + \
            "(select frequency from tbl_compliance_frequency where frequency_id = com.frequency_id) as frequency_name, " + \
            "SUBSTRING_INDEX(com.statutory_mapping,'>>',1) as act_name, acl.activity_on, ch.due_date,ch.completion_date, " + \
            "(CASE WHEN (ch.due_date < ch.approved_on and ch.approve_status = 3) THEN 'Delayed Compliance' " + \
            "WHEN (ch.due_date >= ch.approved_on and ch.approve_status = 3) THEN 'Complied' " + \
            "WHEN (ch.due_date >= ch.approved_on and ch.approve_status < 3) THEN 'In Progress' " + \
            "WHEN (ch.due_date < ch.approved_on and ch.approve_status < 3) THEN 'Not Complied' " + \
            "WHEN (ch.approved_on IS NULL and ch.approve_status IS NULL) THEN 'In Progress' " + \
            "ELSE 'In Progress' END) as task_status, " + \
            "(CASE WHEN acl.activity_by = ch.completed_by THEN ch.documents ELSE '-' END) as uploaded_document, " + \
            "(CASE WHEN acl.activity_by = ch.approved_by THEN (CASE ch.approve_status WHEN 1 THEN 'Rectify' WHEN 2 THEN 'Rejected' ElSE 'Approved' END) " + \
            "WHEN acl.activity_by = ch.concurred_by THEN (CASE ch.concurrence_status WHEN 1 THEN 'Concurred' ELSE 'Rejected' END) " + \
            "WHEN acl.activity_by = ch.completed_by THEN 'Submitted' ELSE 1 END) as activity_status, " + \
            "(CASE WHEN acl.activity_by = ch.approved_by THEN (select concat(employee_code,' - ',employee_name) from tbl_users where user_id = ac.approval_person) " + \
            "WHEN acl.activity_by = ch.concurred_by THEN (select concat(employee_code,' - ',employee_name) from tbl_users where user_id = ac.concurrence_person)  " + \
            "WHEN acl.activity_by = ch.completed_by THEN (select concat(employee_code,' - ',employee_name) from tbl_users where user_id = ac.assignee) ELSE 1 END) as user_name " + \
            "from tbl_compliance_history as ch " + \
            "inner join tbl_compliances as com on ch.compliance_id = com.compliance_id " + \
            "inner join tbl_compliance_activity_log as acl on ch.compliance_history_id = acl.compliance_history_id " + \
            "inner join tbl_assign_compliances as ac on acl.compliance_id = ac.compliance_id and acl.unit_id = ac.unit_id " + \
            "inner join (select compliance_id,unit_id,num from  " + \
               "(select compliance_id,unit_id,@rownum := @rownum + 1 AS num  " + \
               "from (select distinct t1.compliance_id,t1.unit_id from tbl_compliance_activity_log as t1 " + \
                 "inner join tbl_compliance_history as t2 on t1.compliance_history_id = t2.compliance_history_id " + \
                                "order by t1.unit_id,t1.compliance_id,t1.compliance_history_id asc,t1.compliance_activity_id desc) t, " + \
               "(SELECT @rownum := 0) r) as cnt " + \
               "where cnt.num between %s and %s order by cnt.unit_id, cnt.compliance_id) as t01  " + \
                        "on acl.compliance_id = t01.compliance_id and acl.unit_id = t01.unit_id " + \
            "where com.country_id = %s and ch.legal_entity_id = %s " + \
            "and com.domain_id = %s " + \
            "and IF(%s IS NOT NULL, acl.unit_id = %s,1) " + \
            "and IF(%s IS NOT NULL,SUBSTRING_INDEX(com.statutory_mapping,'>>',1) = %s,1) " + \
            "and IF(%s IS NOT NULL, ch.compliance_id = %s,1) " + \
            "and IF(%s > 0, com.frequency_id = %s,1) " + \
            "and (CASE %s WHEN 1 THEN ac.assignee = acl.activity_by " + \
            "WHEN 2 THEN ac.concurrence_person = acl.activity_by WHEN 3 THEN ac.approval_person = acl.activity_by " + \
            "ELSE 1 END) " + \
            "and IF(%s IS NOT NULL, acl.activity_by = %s,1) " + \
            "and acl.activity_on >= %s and acl.activity_on <= %s " + \
            "and IF(%s <> 'All',(CASE WHEN (ch.due_date < ch.approved_on and ch.approve_status = 3) THEN 'Delayed Compliance' " + \
            "WHEN (ch.due_date >= ch.approved_on and ch.approve_status = 3) THEN 'Complied' " + \
            "WHEN (ch.due_date >= ch.approved_on and ch.approve_status < 3) THEN 'In Progress' " + \
            "WHEN (ch.due_date < ch.approved_on and ch.approve_status < 3) THEN 'Not Complied' " + \
            "WHEN (ch.approved_on IS NULL and ch.approve_status IS NULL) THEN 'In Progress' " + \
            "ELSE 'In Progress' END) = %s,1) " + \
            "order by t01.num,acl.compliance_activity_id desc "

    # print query;

    rows = db.select_all(query, [
            f_count, t_count, country_id, legal_entity_id, domain_id, unit_id, unit_id, act, act, compliance_id,
            compliance_id, frequency_id, frequency_id, user_type_id, usr_id, usr_id, from_date, to_date, status_name, status_name
            ])
    print rows

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
        task_status = r["task_status"]
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
    query = "select count(Distinct com.compliance_id) as total_count from tbl_compliance_history as ch " + \
            "inner join tbl_compliances as com on ch.compliance_id = com.compliance_id " + \
            "inner join tbl_compliance_activity_log as acl on ch.compliance_history_id = acl.compliance_history_id " + \
            "inner join tbl_assign_compliances as ac on acl.compliance_id = ac.compliance_id and acl.unit_id = ac.unit_id " + \
            "where com.country_id = %s and ch.legal_entity_id = %s " + \
            "and com.domain_id = %s " + \
            "and IF(%s IS NOT NULL, acl.unit_id = %s,1) " + \
            "and IF(%s IS NOT NULL,SUBSTRING_INDEX(com.statutory_mapping,'>>',1) = %s,1) " + \
            "and IF(%s IS NOT NULL, ch.compliance_id = %s,1) " + \
            "and IF(%s > 0, com.frequency_id = %s,1) " + \
            "and (CASE %s WHEN 1 THEN ac.assignee = acl.activity_by " + \
            "WHEN 2 THEN ac.concurrence_person = acl.activity_by WHEN 3 THEN ac.approval_person = acl.activity_by " + \
            "ELSE 1 END) " + \
            "and IF(%s IS NOT NULL, acl.activity_by = %s,1) " + \
            "and acl.activity_on >= %s and acl.activity_on <= %s " + \
            "and IF(%s <> 'All',(CASE WHEN (ch.due_date < ch.approved_on and ch.approve_status = 3) THEN 'Delayed Compliance' " + \
            "WHEN (ch.due_date >= ch.approved_on and ch.approve_status = 3) THEN 'Complied' " + \
            "WHEN (ch.due_date >= ch.approved_on and ch.approve_status < 3) THEN 'In Progress' " + \
            "WHEN (ch.due_date < ch.approved_on and ch.approve_status < 3) THEN 'Not Complied' " + \
            "WHEN (ch.approved_on IS NULL and ch.approve_status IS NULL) THEN 'In Progress' " + \
            "ELSE 'In Progress' END) = %s,1)"

    rows = db.select_one(query, [
            country_id, legal_entity_id, domain_id, unit_id, unit_id, act, act, compliance_id,
            compliance_id, frequency_id, frequency_id, user_type_id, usr_id, usr_id, from_date, to_date, status_name, status_name
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
    print rows

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

    domain_wise_count = db.select_all(query, [country_id, bg_id, bg_id, legal_entity_id, div_id, div_id, cat_id, cat_id, domain_id, domain_id])
    print domain_wise_count

    def domain_wise_unit_count(country_id, bg_id, legal_entity_id, div_id, cat_id, domain_id) :
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

        rows = db.select_all(query_new, [ country_id, bg_id, bg_id, legal_entity_id, div_id, div_id, cat_id, cat_id, domain_id, domain_id ])
        print rows
        units = []
        for r in rows :
            unit_id = int(r["unit_id"])
            domain_name = r["domain_name"]
            unit = r["units"]
            not_opted_count = int(r["not_opted_count"])
            unassigned_count = int(r["unassigned_count"])
            complied_count = int(r["complied_count"])
            delayed_count = int(r["delayed_count"])
            inprogress_count = int(r["inprogress_count"])
            overdue_count = int(r["overdue_count"])
            unit_row = clientcore.GetDomainWiseUnitScoreCardSuccess(unit_id, domain_name, unit, not_opted_count, unassigned_count, complied_count, delayed_count, inprogress_count, overdue_count)
            units.append(unit_row)
        return units

    compliances = []
    for r in domain_wise_count :
        domain_id = int(r["domain_id"])
        domain_name = r["domain_name"]
        not_opted_count = int(r["not_opted_count"])
        unassigned_count = int(r["unassigned_count"])
        assigned_count = int(r["assigned_count"])
        units_count = domain_wise_unit_count(country_id, bg_id, legal_entity_id, div_id, cat_id, domain_id)
        compliance = clientcore.GetDomainScoreCardSuccess(domain_id, domain_name, not_opted_count, unassigned_count, assigned_count, units_count)
        compliances.append(compliance)
    return compliances
# Domain Score Card End


# Legal Entity Wise Score Card Start
def report_le_wise_score_card(
    db, country_id, legal_entity_id, domain_id, session_user
):
    query = "select sum(inprogress_count) as inprogress_count, (SUM(complied_count) +sum(delayed_count)) as completed_count, " + \
            "sum(overdue_count) as overdue_count " + \
            "from tbl_compliance_status_chart_unitwise " + \
            "where country_id = %s " + \
            "and legal_entity_id = %s " + \
            "and domain_id = %s "

    domain_wise_count = db.select_all(query, [country_id, legal_entity_id, domain_id])
    print domain_wise_count

    def inprogress_unit_wise_count(legal_entity_id, domain_id) :
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
        print rows
        inprogress_unit = []
        for r in rows :
            unit_id = int(r["unit_id"])
            unit = r["unitname"]
            to_complete = int(r["to_complete"])
            to_concur = int(r["to_concur"])
            to_approve = int(r["to_approve"])
            result = clientcore.GetInprogressUnitWiseCountSuccess(unit_id, unit, to_complete, to_concur, to_approve)
            inprogress_unit.append(result)
        return inprogress_unit

    def inprogress_user_wise_count(legal_entity_id, domain_id) :
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
        print rows
        inprogress_unit = []
        for r in rows :
            user_id = int(r["user_id"])
            user_name = r["user_name"]
            to_complete = int(r["to_complete"])
            to_concur = int(r["to_concur"])
            to_approve = int(r["to_approve"])
            result = clientcore.GetInprogressUserWiseCountSuccess(user_id, user_name, to_complete, to_concur, to_approve)
            inprogress_unit.append(result)
        return inprogress_unit

    def completed_unit_wise_count(legal_entity_id, domain_id) :
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
        print rows
        inprogress_unit = []
        for r in rows :
            unit_id = int(r["unit_id"])
            unit = r["unitname"]
            complied_count = int(r["complied_count"])
            delayed_count = int(r["delayed_count"])
            result = clientcore.GetCompletedUnitWiseCountSuccess(unit_id, unit, complied_count, delayed_count)
            inprogress_unit.append(result)
        return inprogress_unit

    def completed_user_wise_count(legal_entity_id, domain_id) :
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
        print rows
        inprogress_unit = []
        for r in rows :
            user_id = int(r["user_id"])
            user_name = r["user_name"]
            complied_count = int(r["complied_count"])
            delayed_count = int(r["delayed_count"])
            result = clientcore.GetCompletedUserWiseCountSuccess(user_id, user_name, complied_count, delayed_count)
            inprogress_unit.append(result)
        return inprogress_unit

    def overdue_unit_wise_count(legal_entity_id, domain_id) :
        query = "select ch.unit_id,concat(unt.unit_code,' - ',unt.unit_name) as unitname, " + \
                "sum(IF(com.frequency_id = 5,IF(ch.due_date < now() and IFNULL(ch.approve_status,0) <> 1,1,0), " + \
                "IF(date(ch.due_date) < curdate() and IFNULL(ch.approve_status,0) <> 1,1,0))) as overdue_count " + \
                "from tbl_compliance_history as ch " + \
                "inner join tbl_compliances as com on ch.compliance_id = com.compliance_id " + \
                "inner join tbl_units as unt on ch.unit_id = unt.unit_id " + \
                "where ch.legal_entity_id = %s and com.domain_id = %s " + \
                "group by ch.unit_id "
        rows = db.select_all(query, [legal_entity_id, domain_id])
        print rows
        inprogress_unit = []
        for r in rows :
            unit_id = int(r["unit_id"])
            unit = r["unitname"]
            overdue_count = int(r["overdue_count"])
            result = clientcore.GetOverdueUnitWiseCountSuccess(unit_id, unit, overdue_count)
            inprogress_unit.append(result)
        return inprogress_unit

    def overdue_user_wise_count(legal_entity_id, domain_id) :
        query = "select usr.user_id,concat(employee_code,' - ',employee_name) as user_name, " + \
                "sum(IF(com.frequency_id = 5,IF(ch.due_date < now() and IFNULL(ch.approve_status,0) <> 1,1,0), " + \
                "IF(date(ch.due_date) < curdate() and IFNULL(ch.approve_status,0) <> 1,1,0))) as overdue_count " + \
                "from tbl_compliance_history as ch " + \
                "inner join tbl_compliances as com on ch.compliance_id = com.compliance_id " + \
                "inner join tbl_users as usr on usr.user_id = ch.completed_by OR usr.user_id = ch.concurred_by OR usr.user_id = ch.approved_by " + \
                "where ch.legal_entity_id = %s and com.domain_id = %s " + \
                "group by usr.user_id"
        rows = db.select_all(query, [legal_entity_id, domain_id])
        print rows
        inprogress_unit = []
        for r in rows :
            unit_id = int(r["user_id"])
            unit = r["user_name"]
            overdue_count = int(r["overdue_count"])
            result = clientcore.GetOverdueUserWiseCountSuccess(unit_id, unit, overdue_count)
            inprogress_unit.append(result)
        return inprogress_unit

    compliances = []
    for r in domain_wise_count :
        inprogress_count = int(r["inprogress_count"])
        completed_count = int(r["completed_count"])
        overdue_count = int(r["overdue_count"])
        inprogress_unit_wise = inprogress_unit_wise_count(legal_entity_id, domain_id)
        inprogress_user_wise = inprogress_user_wise_count(legal_entity_id, domain_id)
        completed_unit_wise = completed_unit_wise_count(legal_entity_id, domain_id)
        completed_user_wise = completed_user_wise_count(legal_entity_id, domain_id)
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
    query = "select SUM(IF(ch.completed_on IS NOT NULL and ch.completed_by = acl.activity_by and ch.completed_by = %s,1,0)) as c_assignee, " + \
            "SUM(IF(ch.completed_on IS NOT NULL and ch.concurred_on IS NOT NULL and ch.concurred_by = acl.activity_by and ch.concurred_by = %s,1,0)) as c_concur, " + \
            "SUM(IF(ch.completed_on IS NOT NULL and ch.concurred_on IS NOT NULL and IFNULL(ch.approve_status,0) = 1 and ch.approved_by = acl.activity_by and ch.approved_by = %s,1,0)) as c_approver, " + \
            "SUM(IF(com.frequency_id = 5,(IF(ch.due_date >= now() and ch.completed_on IS NULL and ch.completed_by = acl.activity_by and ch.completed_by = %s,1,0)), " + \
            "(IF(date(ch.due_date) >= curdate() and ch.completed_on IS NULL and ch.completed_by = acl.activity_by and ch.completed_by = %s,1,0)))) as inp_assignee, " + \
            "SUM(IF(com.frequency_id = 5,(IF(ch.due_date >= now() and ch.completed_on IS NOT NULL and IFNULL(ch.concurrence_status,0) <> 1 and ch.concurred_by = acl.activity_by  and ch.concurred_by = %s,1,0)), " + \
            "(IF(date(ch.due_date) >= curdate() and ch.completed_on IS NOT NULL and IFNULL(ch.concurrence_status,0) <> 1 and ch.concurred_by = acl.activity_by  and ch.concurred_by = %s,1,0)))) as inp_concur, " + \
            "SUM(IF(com.frequency_id = 5,(IF(ch.due_date >= now() and ch.completed_on IS NOT NULL and ch.concurred_on IS NOT NULL and IFNULL(ch.approve_status,0) <> 1 and ch.approved_by = acl.activity_by and ch.approved_by = %s,1,0)), " + \
            "(IF(date(ch.due_date) >= curdate() and ch.completed_on IS NOT NULL and ch.concurred_on IS NOT NULL and IFNULL(ch.approve_status,0) <> 1 and ch.approved_by = acl.activity_by and ch.approved_by = %s,1,0)))) as inp_approver, " + \
            "SUM(IF(com.frequency_id = 5,(IF(ch.due_date < now() and ch.completed_on IS NULL and ch.completed_by = acl.activity_by and ch.completed_by = %s,1,0)), " + \
            "(IF(date(ch.due_date) < curdate() and ch.completed_on IS NULL and ch.completed_by = acl.activity_by and ch.completed_by = %s,1,0)))) as ov_assignee, " + \
            "SUM(IF(com.frequency_id = 5,(IF(ch.due_date < now() and ch.completed_on IS NOT NULL and IFNULL(ch.concurrence_status,0) <> 1 and ch.concurred_by = acl.activity_by and ch.concurred_by = %s,1,0)), " + \
            "(IF(date(ch.due_date) < curdate() and ch.completed_on IS NOT NULL and IFNULL(ch.concurrence_status,0) <> 1 and ch.concurred_by = acl.activity_by and ch.concurred_by = %s,1,0)))) as ov_concur, " + \
            "SUM(IF(com.frequency_id = 5,(IF(ch.due_date < now() and ch.completed_on IS NOT NULL and ch.concurred_on IS NOT NULL and IFNULL(ch.approve_status,0) <> 1 and ch.approved_by = acl.activity_by and ch.approved_by = %s,1,0)), " + \
            "(IF(date(ch.due_date) < curdate() and ch.completed_on IS NOT NULL and ch.concurred_on IS NOT NULL and IFNULL(ch.approve_status,0) <> 1 and ch.approved_by = acl.activity_by and ch.approved_by = %s,1,0)))) as ov_approver " + \
            "from tbl_compliance_history as ch inner join tbl_compliance_activity_log as acl on ch.compliance_history_id = acl.compliance_history_id " + \
            "inner join tbl_compliances as com on ch.compliance_id = com.compliance_id where com.country_id = %s and ch.legal_entity_id = %s and com.domain_id = %s "
    # print query

    domain_wise_count = db.select_all(query, [session_user, session_user, session_user, session_user, session_user, session_user, session_user, session_user, 
        session_user, session_user, session_user, session_user, session_user, session_user, session_user, country_id, legal_entity_id, domain_id])
    print domain_wise_count

    def completed_task_count(country_id, legal_entity_id, domain_id, session_user) :
        query = "select ch.unit_id,(select concat(unit_code,' - ',unit_name) from tbl_units where unit_id = ch.unit_id) as unitname, " + \
                "SUM(IF(ch.completed_on IS NOT NULL and ch.completed_by = acl.activity_by and ch.completed_by = %s,1,0)) as c_assignee, " + \
                "SUM(IF(ch.completed_on IS NOT NULL and ch.concurred_on IS NOT NULL and ch.concurred_by = acl.activity_by and ch.concurred_by = %s,1,0)) as c_concur, " + \
                "SUM(IF(ch.completed_on IS NOT NULL and ch.concurred_on IS NOT NULL and IFNULL(ch.approve_status,0) = 1 and ch.approved_by = acl.activity_by and ch.approved_by = %s,1,0)) as c_approver " + \
                "from tbl_compliance_history as ch inner join tbl_compliance_activity_log as acl on ch.compliance_history_id = acl.compliance_history_id " + \
                "inner join tbl_compliances as com on ch.compliance_id = com.compliance_id " + \
                "where com.country_id = %s and ch.legal_entity_id = %s and com.domain_id = %s group by ch.unit_id; "
        rows = db.select_all(query, [session_user, session_user, session_user, country_id, legal_entity_id, domain_id])
        print rows
        array = []
        for r in rows :
            unit_id = int(r["unit_id"])
            unit = r["unitname"]
            c_assignee = int(r["c_assignee"])
            c_concur = int(r["c_concur"])
            c_approver = int(r["c_approver"])
            result = clientcore.GetCompletedTaskCountSuccess(unit_id, unit, c_assignee, c_concur, c_approver)
            array.append(result)
        return array

    def inprogress_within_duedate_task_count(country_id, legal_entity_id, domain_id, session_user) :
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
        rows = db.select_all(query, [session_user, session_user, session_user, session_user, session_user, session_user, country_id, legal_entity_id, domain_id])
        print rows
        inprogress_unit = []
        for r in rows :
            unit_id = int(r["unit_id"])
            unit = r["unitname"]
            inp_assignee = int(r["inp_assignee"])
            inp_concur = int(r["inp_concur"])
            inp_approver = int(r["inp_approver"])
            result = clientcore.GetInprogressWithinDuedateTaskCountSuccess(unit_id, unit, inp_assignee, inp_concur, inp_approver)
            inprogress_unit.append(result)
        return inprogress_unit

    def over_due_task_count(country_id, legal_entity_id, domain_id, session_user) :
        query = "select ch.unit_id,(select concat(unit_code,' - ',unit_name) from tbl_units where unit_id = ch.unit_id) as unitname, " + \
                "SUM(IF(com.frequency_id = 5,(IF(ch.due_date < now() and ch.completed_on IS NULL and ch.completed_by = acl.activity_by and ch.completed_by = %s,1,0)), " + \
                "(IF(date(ch.due_date) < curdate() and ch.completed_on IS NULL and ch.completed_by = acl.activity_by and ch.completed_by = %s,1,0)))) as ov_assignee, " + \
                "SUM(IF(com.frequency_id = 5,(IF(ch.due_date < now() and ch.completed_on IS NOT NULL and IFNULL(ch.concurrence_status,0) <> 1 and ch.concurred_by = acl.activity_by and ch.concurred_by = %s,1,0)), " + \
                "(IF(date(ch.due_date) < curdate() and ch.completed_on IS NOT NULL and IFNULL(ch.concurrence_status,0) <> 1 and ch.concurred_by = acl.activity_by and ch.concurred_by = %s,1,0)))) as ov_concur, " + \
                "SUM(IF(com.frequency_id = 5,(IF(ch.due_date < now() and ch.completed_on IS NOT NULL and ch.concurred_on IS NOT NULL and IFNULL(ch.approve_status,0) <> 1 and ch.approved_by = acl.activity_by and ch.approved_by = %s,1,0)), " + \
                "(IF(date(ch.due_date) < curdate() and ch.completed_on IS NOT NULL and ch.concurred_on IS NOT NULL and IFNULL(ch.approve_status,0) <> 1 and ch.approved_by = acl.activity_by and ch.approved_by = %s,1,0)))) as ov_approver " + \
                "from tbl_compliance_history as ch inner join tbl_compliance_activity_log as acl on ch.compliance_history_id = acl.compliance_history_id " + \
                "inner join tbl_compliances as com on ch.compliance_id = com.compliance_id where com.country_id = %s and ch.legal_entity_id = %s and com.domain_id = %s group by ch.unit_id; "
        rows = db.select_all(query, [session_user, session_user, session_user, session_user, session_user, session_user, country_id, legal_entity_id, domain_id])
        print rows
        inprogress_unit = []
        for r in rows :
            unit_id = int(r["unit_id"])
            unit = r["unitname"]
            ov_assignee = int(r["ov_assignee"])
            ov_concur = int(r["ov_concur"])
            ov_approver = int(r["ov_approver"])
            result = clientcore.GetOverDueTaskCountSuccess(unit_id, unit, ov_assignee, ov_concur, ov_approver)
            inprogress_unit.append(result)
        return inprogress_unit

    compliances = []
    for r in domain_wise_count :
        c_assignee = int(r["c_assignee"])
        c_concur = int(r["c_concur"])
        c_approver = int(r["c_approver"])
        inp_assignee = int(r["inp_assignee"])
        inp_concur = int(r["inp_concur"])
        inp_approver = int(r["inp_approver"])
        ov_assignee = int(r["ov_assignee"])
        ov_concur = int(r["ov_concur"])
        ov_approver = int(r["ov_approver"])
        completed_task_count = completed_task_count(country_id, legal_entity_id, domain_id, session_user)
        inprogress_within_duedate_task_count = inprogress_within_duedate_task_count(country_id, legal_entity_id, domain_id, session_user)
        over_due_task_count = over_due_task_count(country_id, legal_entity_id, domain_id, session_user)
        compliance = clientcore.GetWorkFlowScoreCardSuccess(
            c_assignee, c_concur, c_approver, inp_assignee, inp_concur, inp_approver, ov_assignee, ov_concur, ov_approver, 
            completed_task_count, inprogress_within_duedate_task_count, over_due_task_count
        )
        compliances.append(compliance)
    return compliances
# Work Flow Score Card End

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


###############################################################################################
# Objective: To get the domains list under selected legal entity
# Parameter: request object
# Result: list of domains under the leagl entity selection
###############################################################################################
def get_domains_for_le(db, legal_entity_id):
    print "le"
    print legal_entity_id
    query = "select distinct(t1.domain_id), t1.legal_entity_id, t2.domain_name, t2.is_active " + \
            "from tbl_legal_entity_domains as t1 inner join tbl_domains as t2 " + \
            "on t2.domain_id = t1.domain_id where t1.legal_entity_id = %s " + \
            "order by t2.domain_name; "
    result = db.select_all(query, [legal_entity_id])
    print "domains"
    print result
    le_domains_list = []
    for row in result:
        le_domains_list.append(clientcore.Domain(
            row["domain_id"], row["domain_name"], row["legal_entity_id"], bool(row["is_active"])
            )
        )
    return le_domains_list

###############################################################################################
# Objective: To get the units under selected legal entity, domain and country
# Parameter: request object
# Result: list of units under the selected country, domain and legal entity
###############################################################################################
def get_units_for_le_domain(db, country_id, legal_entity_id):
    query = "SELECT t1.unit_id, t1.unit_code, t1.unit_name, t2.domain_id, t1.country_id, t1.legal_entity_id " + \
            "FROM tbl_units as t1 inner join tbl_units_organizations as t2 on t2.unit_id = t1.unit_id " + \
            "where t1.legal_entity_id = %s and t1.country_id = %s group by t1.unit_id;"
    result = db.select_all(query, [legal_entity_id, country_id])
    print "units"
    print result
    le_units_list = []
    for row in result:
        le_units_list.append(clientreport.UnitLegalEntity(
            row["unit_id"], row["unit_code"], row["unit_name"], row["domain_id"],
            row["country_id"], row["legal_entity_id"]
            )
        )
    return le_units_list

###############################################################################################
# Objective: To get the acts under selected legal entity
# Parameter: request object
# Result: list of acts under the selected legal entity
###############################################################################################
def get_acts_for_le_domain(db, legal_entity_id, country_id):
    query = "select t1.legal_entity_id, t1.domain_id, t1.unit_id, t2.compliance_id, " + \
            "t2.statutory_mapping, t2.compliance_task, t2.frequency_id from " + \
            "tbl_client_compliances as t1 inner join tbl_compliances as t2 " + \
            "on t2.compliance_id = t1.compliance_id and t2.domain_id = t1.domain_id and " + \
            "t2.country_id = %s where t1.legal_entity_id = %s"
    result = db.select_all(query, [country_id, legal_entity_id])
    print "acts"
    print result
    print len(result)
    le_act_list = []
    last = object()
    for row in result:
        stat_map = json.loads(row["statutory_mapping"])
        if stat_map[0].find(">>") >= 0:
            stat_map = stat_map[0].split(">>")[0]
        else:
            stat_map = str(stat_map)[3:-2]
        print "mapped"
        print stat_map
        if last != stat_map:
            last = stat_map
            le_act_list.append(clientreport.ActLegalEntity(
                row["legal_entity_id"], row["domain_id"], row["unit_id"],
                row["compliance_id"], statutory_mapping=stat_map
                )
            )
    print len(le_act_list)
    return le_act_list

###############################################################################################
# Objective: To get the compliance tasks under selected legal entity
# Parameter: request object
# Result: list of acts under the selected legal entity
###############################################################################################
def get_task_for_le_domain(db, legal_entity_id):
    query = "select t1.legal_entity_id, t1.domain_id, t1.unit_id, t2.compliance_id, " + \
            "t2.statutory_mapping, t2.compliance_task, t2.frequency_id from " + \
            "tbl_client_compliances as t1 inner join tbl_compliances as t2 " + \
            "on t2.compliance_id = t1.compliance_id and t2.domain_id = t1.domain_id " + \
            "where t1.legal_entity_id = %s"
    result = db.select_all(query, [legal_entity_id])
    print "task"
    print result
    print len(result)
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
                row["compliance_id"], row["compliance_task"], row["frequency_id"],
                statutory_mapping=stat_map
                )
            )
    return le_task_list

###############################################################################################
# Objective: To get the frequency from master
# Parameter: request object
# Result: list of frequencies
###############################################################################################
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

###############################################################################################
# Objective: To get the compliance status
# Parameter: request object
# Result: list of compliance status
###############################################################################################
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

###############################################################################################
# Objective: To get the compliance user type
# Parameter: request object
# Result: list of compliance user types
###############################################################################################
def get_compliance_user_type(db):
    u_type = ("Assignee", "Concurrence", "Approval")
    user_types = []
    i = 0
    for u_t in u_type:
        c_user_type = clientreport.ComplianceUserType(
            i , u_t
        )
        user_types.append(c_user_type)
        i = i + 1
    return user_types

###############################################################################################
# Objective: To get the compliance users under user types
# Parameter: request object
# Result: list of compliance users under user types
###############################################################################################
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
    print result
    le_user_type_users = []

    for row in result:
        le_user_type_users.append(clientreport.ComplianceUsers(
            row["legal_entity_id"], row["country_id"], row["domain_id"],
            row["unit_id"], row["compliance_id"], row["assignee"], row["assignee_name"],
            row["concurrence_person"], row["concurrer_name"], row["approval_person"],
            row["approver_name"]
            )
        )
    return le_user_type_users

###############################################################################################
# Objective: To get the compliance list under filtered data
# Parameter: request object
# Result: list of compliance grouped by unit and act
###############################################################################################
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
        "(select concat(unit_code,'-',unit_name,',',geography_name,',',address,',',postal_code)" + \
        "from tbl_units where unit_id = t1.unit_id) as unit_name, t3.statutory_mapping, " + \
        "t3.compliance_task, (select frequency from tbl_compliance_frequency where " + \
        "frequency_id = t3.frequency_id) as frequency_name, (select " + \
        "concat(employee_code,'-',employee_name) from tbl_users where user_id = t1.completed_by) " + \
        "as assignee_name, t1.completed_by, t2.activity_date, t3.format_file, t3.format_file_size "
    from_clause = "from tbl_compliance_history as t1 left join tbl_compliance_activity_log as t2 " + \
        "on t2.compliance_id = t1.compliance_id and t2.unit_id = t1.unit_id " + \
        "inner join tbl_compliances as t3 on t3.compliance_id = t1.compliance_id where "
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

    compliance_id = request.compliance_id
    if int(compliance_id) > 0:
        where_clause = where_clause + "and t1.compliance_id = %s "
        condition_val.append(compliance_id)

    unit_id = request.unit_id
    if int(unit_id) > 0:
        where_clause = where_clause + "and t1.unit_id = %s "
        condition_val.append(unit_id)

    where_clause = where_clause + "and t1.legal_entity_id = %s order by t1.due_date desc limit %s, %s;"
    condition_val.extend([legal_entity_id, int(request.from_count), int(request.page_count)])
    query = select_qry + from_clause + where_clause
    print "qry"
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
        print row["activity_date"]
        if row["activity_date"] is None:
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

        le_report.append(clientreport.LegalEntityWiseReport(
            row["country_id"], row["legal_entity_id"], row["domain_id"], row["unit_id"],
            row["compliance_id"], row["unit_name"], statutory_mapping, row["compliance_task"],
            row["frequency_name"], datetime_to_string(row["due_date"]), task_status, row["assignee_name"],
            activity_status, datetime_to_string(row["activity_date"]), name,
            datetime_to_string(row["completion_date"]), url
        ))
    return le_report

###############################################################################################
# Objective: To get the compliance list under filtered data
# Parameter: request object
# Result: list of compliance grouped by unit and act
###############################################################################################
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
        "(select concat(unit_code,'-',unit_name,',',geography_name,',',address,',',postal_code)" + \
        "from tbl_units where unit_id = t1.unit_id) as unit_name, t3.statutory_mapping, " + \
        "t3.compliance_task, (select frequency from tbl_compliance_frequency where " + \
        "frequency_id = t3.frequency_id) as frequency_name, (select " + \
        "concat(employee_code,'-',employee_name) from tbl_users where user_id = t1.completed_by) " + \
        "as assignee_name, t1.completed_by, t2.activity_date, t3.format_file, t3.format_file_size "
    from_clause = "from tbl_compliance_history as t1 left join tbl_compliance_activity_log as t2 " + \
        "on t2.compliance_id = t1.compliance_id and t2.unit_id = t1.unit_id " + \
        "inner join tbl_compliances as t3 on t3.compliance_id = t1.compliance_id where "
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

    compliance_id = request.compliance_id
    if int(compliance_id) > 0:
        where_clause = where_clause + "and t1.compliance_id = %s "
        condition_val.append(compliance_id)

    unit_id = request.unit_id
    if int(unit_id) > 0:
        where_clause = where_clause + "and t1.unit_id = %s "
        condition_val.append(unit_id)

    where_clause = where_clause + "and t1.legal_entity_id = %s order by t1.due_date desc limit %s, %s;"
    condition_val.extend([legal_entity_id, int(request.from_count), int(request.page_count)])
    query = select_qry + from_clause + where_clause
    print "qry"
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
        print row["activity_date"]
        if row["activity_date"] is None:
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

        le_report.append(clientreport.LegalEntityWiseReport(
            row["country_id"], row["legal_entity_id"], row["domain_id"], row["unit_id"],
            row["compliance_id"], row["unit_name"], statutory_mapping, row["compliance_task"],
            row["frequency_name"], datetime_to_string(row["due_date"]), task_status, row["assignee_name"],
            activity_status, datetime_to_string(row["activity_date"]), name,
            datetime_to_string(row["completion_date"]), url
        ))
    return le_report


###############################################################################################
# Objective: To get the compliance list under filtered data
# Parameter: request object
# Result: list of compliance grouped by domain and act
###############################################################################################
def process_unit_wise_report(db, request):
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
        "(select concat(unit_code,'-',unit_name,',',geography_name,',',address,',',postal_code)" + \
        "from tbl_units where unit_id = t1.unit_id) as unit_name, t3.statutory_mapping, " + \
        "t3.compliance_task, (select frequency from tbl_compliance_frequency where " + \
        "frequency_id = t3.frequency_id) as frequency_name, (select " + \
        "concat(employee_code,'-',employee_name) from tbl_users where user_id = t1.completed_by) " + \
        "as assignee_name, t1.completed_by, t2.activity_date, t3.format_file, t3.format_file_size, " + \
        "(select domain_name from tbl_domains where domain_id = t3.domain_id) as domain_name "
    from_clause = "from tbl_compliance_history as t1 left join tbl_compliance_activity_log as t2 " + \
        "on t2.compliance_id = t1.compliance_id and t2.unit_id = t1.unit_id " + \
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

    compliance_id = request.compliance_id
    if int(compliance_id) > 0:
        where_clause = where_clause + "and t1.compliance_id = %s "
        condition_val.append(compliance_id)

    where_clause = where_clause + "and t1.legal_entity_id = %s and t1.unit_id = %s order by t1.due_date desc limit %s, %s;"
    condition_val.extend([legal_entity_id, request.unit_id, int(request.from_count), int(request.page_count)])
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
        print row["activity_date"]
        if row["activity_date"] is None:
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

        unit_report.append(clientreport.UnitWiseReport(
            row["country_id"], row["legal_entity_id"], row["domain_id"], row["unit_id"],
            row["compliance_id"], row["unit_name"], statutory_mapping, row["compliance_task"],
            row["frequency_name"], datetime_to_string(row["due_date"]), task_status, row["assignee_name"],
            activity_status, datetime_to_string(row["activity_date"]), name,
            datetime_to_string(row["completion_date"]), url, row["domain_name"]
        ))
    return unit_report

###############################################################################################
# Objective: To get the domains list with user id under selected legal entity
# Parameter: request object
# Result: list of domains and its users under the leagl entity selection
###############################################################################################
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
            row["user_id"], row["domain_id"], row["domain_name"], row["sp_id_optional"]
            )
        )
    return user_domains_list

###############################################################################################
# Objective: To get the units with the users under selected legal entity, country
# Parameter: request object
# Result: list of units with the users under the selected country, legal entity
###############################################################################################
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
            row["user_id_optional"], row["unit_id"], row["domain_id"], row["unit_code"],
            row["unit_name"], row["sp_id_optional"]
            )
        )
    return users_units_list


###############################################################################################
# Objective: To get the acts with users under selected legal entity
# Parameter: request object
# Result: list of acts with the users under the selected legal entity
###############################################################################################
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
            row["legal_entity_id"], row["country_id"], row["domain_id"], row["unit_id"],
            row["compliance_id"], row["assignee"], row["sp_ass_id_optional"],
            row["concurrence_person"], row["sp_cc_id_optional"], row["approval_person"],
            row["sp_app_id_optional"], row["compliance_task"], statutory_mapping=stat_map
            )
        )
    print len(le_act_list)
    return le_act_list

###############################################################################################
# Objective: To get the lists of users under service provider
# Parameter: request object
# Result: list of users under service provider
##############################################################################################
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
            row["user_id"], row["username"]
        ))
    return sp_user_details


###############################################################################################
# Objective: To get the compliance list under filtered data
# Parameter: request object
# Result: list of compliance grouped by unit and act
###############################################################################################
def process_service_provider_wise_report(db , request):
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
        "(select concat(unit_code,'-',unit_name,',',geography_name,',',address,',',postal_code)" + \
        "from tbl_units where unit_id = t1.unit_id) as unit_name, t3.statutory_mapping, " + \
        "t3.compliance_task, (select frequency from tbl_compliance_frequency where " + \
        "frequency_id = t3.frequency_id) as frequency_name, (select " + \
        "concat(employee_code,'-',employee_name) from tbl_users where user_id = t1.completed_by) " + \
        "as assignee_name, t1.completed_by, t2.activity_date, t3.format_file, t3.format_file_size "
    from_clause = "from tbl_users as t4 inner join tbl_compliance_history as t1 " + \
        "on (t1.completed_by=t4.user_id or t1.concurred_by=t4.user_id or t1.approved_by=t4.user_id) " + \
        "left join tbl_compliance_activity_log as t2 " + \
        "on t2.compliance_id = t1.compliance_id and t2.unit_id = t1.unit_id " + \
        "inner join tbl_compliances as t3 on t3.compliance_id = t1.compliance_id where "
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
        "order by t1.due_date desc limit %s, %s;"
    condition_val.extend([sp_id, legal_entity_id, int(request.from_count), int(request.page_count)])
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
        print row["activity_date"]
        if row["activity_date"] is None:
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

        sp_report.append(clientreport.LegalEntityWiseReport(
            row["country_id"], row["legal_entity_id"], row["domain_id"], row["unit_id"],
            row["compliance_id"], row["unit_name"], statutory_mapping, row["compliance_task"],
            row["frequency_name"], datetime_to_string(row["due_date"]), task_status, row["assignee_name"],
            activity_status, datetime_to_string(row["activity_date"]), name,
            datetime_to_string(row["completion_date"]), url
        ))
    return sp_report

###############################################################################################
# Objective: To get the list of users under legal entity
# Parameter: request object
# Result: list of users
###############################################################################################
def get_le_users_list(db):
    query = "select user_id, concat(employee_code,' - ',employee_name) as username, " + \
        "user_category_id from tbl_users where user_category_id <> 2;"
    result = db.select_all(query, None)
    units_users_list = []
    for row in result:
        units_users_list.append(clientreport.LegalEntityUsers(
            row["user_id"], row["username"], row["user_category_id"]
        ))
    return units_users_list

###############################################################################################
# Objective: To get the domains list with user id under selected legal entity
# Parameter: request object
# Result: list of domains and its users under the leagl entity selection
###############################################################################################
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

###############################################################################################
# Objective: To get the units with the users under selected legal entity, country
# Parameter: request object
# Result: list of units with the users under the selected country, legal entity
###############################################################################################
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
            row["user_id_optional"], row["unit_id"], row["domain_id"], row["unit_code"], row["unit_name"]
            )
        )
    return users_units_list

###############################################################################################
# Objective: To get the acts with users under selected legal entity
# Parameter: request object
# Result: list of acts with the users under the selected legal entity
###############################################################################################
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
            row["legal_entity_id"], row["country_id"], row["domain_id"], row["unit_id"],
            row["compliance_id"], row["assignee"], row["concurrence_person"],
            row["approval_person"], row["compliance_task"], statutory_mapping=stat_map
            )
        )
    print len(le_act_list)
    return le_act_list

###############################################################################################
# Objective: To get the compliance list under filtered data
# Parameter: request object
# Result: list of compliance grouped by domain and act
###############################################################################################
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
        "(select concat(unit_code,'-',unit_name,',',geography_name,',',address,',',postal_code)" + \
        "from tbl_units where unit_id = t1.unit_id) as unit_name, t3.statutory_mapping, " + \
        "t3.compliance_task, (select frequency from tbl_compliance_frequency where " + \
        "frequency_id = t3.frequency_id) as frequency_name, (select " + \
        "concat(employee_code,'-',employee_name) from tbl_users where user_id = t1.completed_by) " + \
        "as assignee_name, t1.completed_by, t2.activity_date, t3.format_file, t3.format_file_size, " + \
        "(select domain_name from tbl_domains where domain_id = t3.domain_id) as domain_name "
    from_clause = "from tbl_compliance_history as t1 left join tbl_compliance_activity_log as t2 " + \
        "on t2.compliance_id = t1.compliance_id and t2.unit_id = t1.unit_id " + \
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

    compliance_id = request.compliance_id
    if int(compliance_id) > 0:
        where_clause = where_clause + "and t1.compliance_id = %s "
        condition_val.append(compliance_id)

    unit_id = request.unit_id
    if int(unit_id) > 0:
        where_clause = where_clause + "and t1.unit_id = %s "
        condition_val.append(unit_id)

    where_clause = where_clause + "and t1.legal_entity_id = %s order by t1.due_date desc limit %s, %s;"
    condition_val.extend([legal_entity_id, int(request.from_count), int(request.page_count)])
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
        print row["activity_date"]
        if row["activity_date"] is None:
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

        user_report.append(clientreport.UnitWiseReport(
            row["country_id"], row["legal_entity_id"], row["domain_id"], row["unit_id"],
            row["compliance_id"], row["unit_name"], statutory_mapping, row["compliance_task"],
            row["frequency_name"], datetime_to_string(row["due_date"]), task_status, row["assignee_name"],
            activity_status, datetime_to_string(row["activity_date"]), name,
            datetime_to_string(row["completion_date"]), url, row["domain_name"]
        ))
    return user_report

###############################################################################################
# Objective: To get the divisions list under legal entity and business group
# Parameter: request object
# Result: list of divisions from master
###############################################################################################
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

###############################################################################################
# Objective: To get the categories list under legal entity and business group
# Parameter: request object
# Result: list of categories from master
###############################################################################################
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

###############################################################################################
# Objective: To get the units list under legal entity and business group and country
# Parameter: request object
# Result: list of units from master
###############################################################################################
def get_units_list(db, country_id, business_group_id, legal_entity_id):
    query = "select unit_id, unit_code, unit_name, division_id, category_id from " + \
        "tbl_units where business_group_id = %s and legal_entity_id =%s and country_id = %s"
    result = db.select_all(query, [business_group_id, legal_entity_id, country_id])

    query = "select t1.unit_id, t2.domain_id, t2.organisation_id " + \
        "from tbl_units as t1 inner join tbl_units_organizations as t2 on " + \
        "t2.unit_id = t1.unit_id where t1.business_group_id = %s and t1.legal_entity_id = %s and " + \
        "t1.country_id = %s group by t1.unit_id, t2.domain_id, t2.organisation_id order by " + \
        "t1.unit_id;"
    result_1 = db.select_all(query, [business_group_id, legal_entity_id, country_id])

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

###############################################################################################
# Objective: To get the domains and organization list under legal entity
# Parameter: request object
# Result: list of units from master
###############################################################################################
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

###############################################################################################
# Objective: To get the status of the units
# Parameter: request object
# Result: list of status
###############################################################################################
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


###############################################################################################
# Objective: To get the unit details under filtered data
# Parameter: request object
# Result: list of units grouped by division
###############################################################################################
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
        "category_name from tbl_units as t1 where "
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
        last = object()
        for row_1 in result_1:
            if unit_id == row_1["unit_id"]:
                if last != (row_1["domain_name"]+" - "+row_1["organisation_name"]):
                    last = row_1["domain_name"]+" - "+row_1["organisation_name"]
                    d_i_names.append(row_1["domain_name"]+" - "+row_1["organisation_name"])
        unit_report.append(clientreport.UnitListReport(
            unit_id, unit_code, unit_name, geography_name, address, postal_code,
            d_i_names, unit_status, closed_date, division_name
        ))
    return unit_report


###############################################################################################
# Objective: To get the Compliance details under filtered data
# Parameter: request object
# Result: list of compliances and acts
###############################################################################################
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
        statutory_mapping = '%'+statutory_mapping+'%'
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

    where_clause = where_clause + "group by t1.compliance_id order by t3.created_on desc limit %s, %s;"
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
            row["compliance_id"], row["compliance_task"], row["compliance_description"],
            datetime_to_string(row["created_on"]), row["notification_text"],
            statutory_mapping=stat_map
        ))
    return statutory_notification

###############################################################################################
# Objective: To get the list of activities
# Parameter: request object
# Result: list of activities
###############################################################################################
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
        "= t1.user_id) as user_name from tbl_activity_log as t1 where "
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
        activity_list.append(clientreport.AuditTrailActivities(
            row["user_id"], row["user_name"], row["form_id"],
            row["action"], datetime_to_string_time(row["created_on"])
        ))
    return activity_list
