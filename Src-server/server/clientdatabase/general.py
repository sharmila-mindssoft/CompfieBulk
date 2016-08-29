import os
import io
import datetime
import json
from dateutil import relativedelta
from server.clientdatabase.tables import *
from server.constants import (CLIENT_DOCS_BASE_PATH)
from protocol import (core, dashboard, clientreport)
from server.common import (
    encrypt, convert_to_dict, get_date_time, get_date_time_in_date,
    remove_uploaded_file, convert_to_key_dict
)
from server.exceptionmessage import client_process_error
from savetoknowledge import UpdateFileSpace

__all__ = [
    "get_client_user_forms",
    "get_countries_for_user",
    "get_domains_for_user",
    "get_business_groups_for_user",
    "get_legal_entities_for_user",
    "get_divisions_for_user",
    "get_group_name",
    "get_country_wise_domain_month_range",
    "get_units_for_user",
    "get_client_users",
    "get_user_domains",
    "get_user_countries",
    "verify_username",
    "verify_password",
    "get_countries",
    "get_domains",
    "is_primary_admin",
    "have_compliances",
    "is_seating_unit",
    "is_admin",
    "get_user_unit_ids",
    "is_two_levels_of_approval",
    "get_user_company_details",
    "get_client_level_1_statutoy",
    "get_service_providers",
    "get_client_compliances",
    "get_client_settings",
    "get_admin_info",
    "validate_compliance_due_date",
    "get_compliance_frequency",
    "get_users",
    "get_users_by_id",
    "get_users_by_unit_and_domain",
    "get_compliance_name_by_id",
    "is_space_available",
    "update_used_space",
    "save_compliance_activity",
    "save_compliance_notification",
    "get_email_id_for_users",
    "get_user_email_name",
    "calculate_due_date",
    "filter_out_due_dates",
    "convert_base64_to_file",
    "get_user_name_by_id",
    "get_form_ids_for_admin",
    "get_report_form_ids",
    "get_client_id_from_short_name",
    "validate_reset_token",
    "remove_session",
    "update_profile",
    "is_service_proivder_user",
    "convert_datetime_to_date"

]


def get_client_user_forms(db, form_ids, is_admin):
    columns = "tf.form_id, tf.form_type_id, tft.form_type, tf.form_name, "
    columns += "tf.form_url, tf.form_order, tf.parent_menu "

    tables = [tblForms, tblFormType]
    aliases = ["tf",  "tft"]
    joinConditions = ["tf.form_type_id = tft.form_type_id"]
    whereCondition, whereConditionVal = db.generate_tuple_condition(
        "form_id", [int(x) for x in form_ids.split(",")]
    )
    order = " order by tf.form_order "
    joinType = "left join"
    rows = db.get_data_from_multiple_tables(
        columns, tables, aliases, joinType,
        joinConditions, whereCondition + order, [whereConditionVal]
    )
    return rows


def get_admin_id(db):
    columns = "user_id"
    condition = " is_active = 1 and is_primary_admin = 1 "
    rows = db.get_data(tblUsers, columns, condition)
    return rows[0]["user_id"]


def get_countries_for_user(db, user_id):
    admin_id = get_admin_id(db)
    query = "SELECT distinct t1.country_id, t1.country_name, " + \
        " t1.is_active FROM tbl_countries t1 "
    if user_id != admin_id:
        query = query + " INNER JOIN tbl_user_countries t2 " + \
            " ON t1.country_id = t2.country_id WHERE t2.user_id = %s"
        rows = db.select_all(query, [user_id])
    else:
        rows = db.select_all(query)
    columns = ["country_id", "country_name", "is_active"]
    result = convert_to_dict(rows, columns)
    return return_countries(result)


def return_countries(data):
    results = []
    for d in data:
        results.append(core.Country(
            d["country_id"], d["country_name"], bool(d["is_active"])
        ))
    return results


def get_domains_for_user(db, user_id):
    admin_id = get_admin_id(db)
    query = "SELECT distinct t1.domain_id, t1.domain_name, " + \
        " t1.is_active FROM tbl_domains t1 "
    if user_id != admin_id:
        query = query + " INNER JOIN tbl_user_domains t2 ON " + \
            " t1.domain_id = t2.domain_id WHERE t2.user_id = %s"
        rows = db.select_all(query, [user_id])
    else:
        rows = db.select_all(query)
    columns = ["domain_id", "domain_name", "is_active"]
    result = convert_to_dict(rows, columns)
    return return_domains(result)


def return_domains(data):
    results = []
    for d in data:
        results.append(core.Domain(
            d["domain_id"], d["domain_name"], bool(d["is_active"])
        ))
    return results


def get_business_groups_for_user(db, business_group_ids):
    columns = "business_group_id, business_group_name"
    condition = "1 "
    condition_val = None
    if business_group_ids is not None:
        condition = " find_in_set (business_group_id, %s) "
        condition_val = [business_group_ids]
    order = " ORDER BY business_group_name "
    rows = db.get_data(
        tblBusinessGroups, columns, condition, condition_val, order
    )
    return return_business_groups(rows)


def return_business_groups(business_groups):
    results = []
    for business_group in business_groups:
        results.append(core.ClientBusinessGroup(
            business_group["business_group_id"],
            business_group["business_group_name"]
        ))
    return results


def get_legal_entities_for_user(db, legal_entity_ids):
    columns = "legal_entity_id, legal_entity_name, business_group_id"
    condition = "1 "
    condition_val = None
    if legal_entity_ids is not None:
        condition = " find_in_set(legal_entity_id, %s) "
        condition_val = [legal_entity_ids]
    order = "ORDER BY legal_entity_name "
    rows = db.get_data(
        tblLegalEntities, columns, condition, condition_val, order
    )
    return return_legal_entities(rows)


def return_legal_entities(legal_entities):
    results = []
    for legal_entity in legal_entities:
        b_group_id = None
        if legal_entity["business_group_id"] > 0:
            b_group_id = int(legal_entity["business_group_id"])
        results.append(core.ClientLegalEntity(
            legal_entity["legal_entity_id"],
            legal_entity["legal_entity_name"],
            b_group_id
        ))
    return results


def get_divisions_for_user(db, division_ids):
    columns = "division_id, division_name, legal_entity_id, business_group_id"
    condition = "1"
    condition_val = None
    if division_ids is not None:
        condition = " find_in_set(division_id, %s) "
        condition_val = [division_ids]
    order = " ORDER BY division_name"
    rows = db.get_data(
        tblDivisions, columns, condition, condition_val, order
    )
    return return_divisions(rows)


def return_divisions(divisions):
    results = []
    for division in divisions:
        division_obj = core.ClientDivision(
            division["division_id"], division["division_name"],
            division["legal_entity_id"], division["business_group_id"]
        )
        results.append(division_obj)
    return results


def get_group_name(db):
    query = "SELECT group_name from %s " % tblClientGroups
    row = db.select_one(query)
    if row:
        return row[0]
    return "group_name"


def get_country_wise_domain_month_range(db):
    q = " SELECT t1.country_id, " + \
        " (select country_name " + \
        " from tbl_countries " + \
        " where country_id = t1.country_id) country_name, " + \
        " t1.domain_id," + \
        " (select domain_name from tbl_domains " + \
        " where domain_id = t1.domain_id)domain_name, " + \
        " t1.period_from, t1.period_to " + \
        " from tbl_client_configurations t1 INNER JOIN " + \
        " tbl_countries TC ON TC.country_id = t1.country_id  " + \
        " INNER JOIN tbl_domains TD ON TD.domain_id = t1.domain_id"
    rows = db.select_all(q)
    columns = [
        "country_id", "country_name",
        "domain_id", "domain_name",
        "period_from", "period_to"
    ]
    result = convert_to_dict(rows, columns)

    country_wise = {}
    domain_info = []
    for r in result:
        country_name = r["country_name"].strip()
        domain_name = r["domain_name"]
        info = dashboard.DomainWiseYearConfiguration(
            country_name,
            domain_name,
            db.string_full_months.get(int(r["period_from"])),
            db.string_full_months.get(int(r["period_to"]))
        )
        domain_info = country_wise.get(country_name)
        if domain_info is None:
            domain_info = []

        domain_info.append(info)
        country_wise[country_name] = domain_info
    return country_wise


def get_units_for_user(db, unit_ids):
    columns = [
        "unit_id", "unit_code", "unit_name", "address", "division_id",
        "domain_ids", "country_id", "legal_entity_id", "business_group_id",
        "is_active", "is_closed"
    ]
    condition = "is_closed = 0"
    condition_val = None
    if unit_ids is not None:
        condition = " find_in_set(unit_id, %s) "
        condition_val = [unit_ids]
    order = "ORDER BY unit_name"
    rows = db.get_data(
        tblUnits, columns, condition, condition_val, order
    )
    return return_units(rows)


def return_units(units):
        results = []
        for unit in units:
            division_id = None
            b_group_id = None
            if unit["division_id"] > 0:
                division_id = unit["division_id"]
            if unit["business_group_id"] > 0:
                b_group_id = unit["business_group_id"]
            results.append(core.ClientUnit(
                unit["unit_id"], division_id, unit["legal_entity_id"],
                b_group_id, unit["unit_code"],
                unit["unit_name"], unit["address"], bool(unit["is_active"]),
                [int(x) for x in unit["domain_ids"].split(",")],
                unit["country_id"],
                bool(unit["is_closed"])
            ))
        return results


def get_client_users(db, unit_ids=None):
    columns = "user_id, employee_name, employee_code, is_active"
    condition = "1"
    conditon_val = None
    if unit_ids is not None:
        condition += " and seating_unit_id in (%s)"
        conditon_val = [unit_ids]
    rows = db.get_data(
        tblUsers, columns, condition, conditon_val
    )
    return return_client_users(rows)


def return_client_users(users):
    results = []
    for user in users:
        results.append(clientreport.User(
            user["user_id"], user["employee_code"], user["employee_name"]
        ))
    return results


def get_user_domains(db, user_id):
    q = "select domain_id from tbl_domains"
    param = None
    condition = ""
    if is_primary_admin(db, user_id) is not True:
        q = "select domain_id from tbl_user_domains"
        condition = " WHERE user_id = %s"
        param = [user_id]
    rows = db.select_all(q + condition, param)
    d_ids = []
    for r in rows:
        d_ids.append(int(r[0]))
    return d_ids


def is_service_provider_in_contract(db, service_provider_id):
    column = "count(1) as live"
    condition = "now() between contract_from " + \
        " and DATE_ADD(contract_to, INTERVAL 1 DAY) " + \
        " and service_provider_id = %s and is_active = 1"
    condition_val = [service_provider_id]
    rows = db.get_data(tblServiceProviders, column, condition, condition_val)
    if rows[0]["live"] > 0:
        return True
    else:
        return False


def is_in_contract(db):
    columns = "count(1) as live"
    condition = "now() between contract_from and " + \
        " DATE_ADD(contract_to, INTERVAL 1 DAY)"
    rows = db.get_data(
        tblClientGroups, columns, condition
    )
    if rows[0]["live"] <= 0:
        return False
    else:
        return True


def verify_username(db, username):
    columns = "count(*) as result, user_id"
    condition = "email_id=%s and is_active = 1"
    condition_val = [username]
    rows = db.get_data(
        tblUsers, columns, condition, condition_val
    )
    count = rows[0]["result"]
    if count == 1:
        return rows[0]["user_id"]
    else:
        return None


def verify_password(db, password, user_id):
    columns = "count(*) as result"
    encrypted_password = encrypt(password)
    condition = "1"
    rows = None
    condition = "password=%s and user_id=%s"
    condition_val = [encrypted_password, user_id]
    rows = db.get_data(
        tblUsers, columns, condition, condition_val
    )

    if(int(rows[0]["result"]) <= 0):
        return False
    else:
        return True


def get_countries(db):
    query = "SELECT distinct t1.country_id, t1.country_name, " + \
        " t1.is_active FROM tbl_countries t1 "
    rows = db.select_all(query)
    columns = ["country_id", "country_name", "is_active"]
    result = convert_to_dict(rows, columns)
    return return_countries(result)


def get_domains(db):
    query = "SELECT distinct t1.domain_id, t1.domain_name, " + \
        " t1.is_active FROM tbl_domains t1 "
    rows = db.select_all(query)
    columns = ["domain_id", "domain_name", "is_active"]
    result = convert_to_dict(rows, columns)
    return return_domains(result)


def is_primary_admin(db, user_id):
    column = "count(1) as result"
    condition = "user_id = %s and is_primary_admin = 1 and is_active = 1"
    condition_val = [user_id]
    rows = db.get_data(tblUsers, column, condition, condition_val)
    if rows[0]["result"] > 0 or user_id == 1:
        return True
    else:
        return False


def have_compliances(db, user_id):
        column = "count(compliance_id) as compliances"
        condition = "assignee = %s and is_active = 1"
        condition_val = [user_id]
        rows = db.get_data(
            tblAssignedCompliances, column, condition, condition_val
        )
        no_of_compliances = rows[0]["compliances"]
        if no_of_compliances > 0:
            return True
        else:
            return False


def is_seating_unit(db, unit_id):
    column = "count(*) as units"
    condition = "seating_unit_id =%s"
    condition_val = [unit_id]
    rows = db.get_data(tblUsers, column, condition, condition_val)
    user_count = rows[0]["units"]
    if user_count > 0:
        return True
    else:
        return False


def is_admin(db, user_id):
    if user_id == 0:
        return True
    else:
        columns = "count(user_id) as admin"
        condition = "(is_admin = 1 or is_primary_admin = 1) " + \
            " and user_id = %s"
        condition_val = [user_id]
        rows = db.get_data(tblUsers, columns, condition, condition_val)
        if rows[0]["admin"] > 0:
            return True
        else:
            return False


def get_user_unit_ids(db, user_id):
    q = "select distinct unit_id from tbl_units"
    param = None
    condition = ""
    if is_primary_admin(db, user_id) is not True:
        condition = " WHERE unit_id in (select unit_id " + \
            " from tbl_user_units " + \
            " where user_id = %s )"
        param = [user_id]

    rows = db.select_all(q + condition, param)
    u_ids = []
    for r in rows:
        u_ids.append(int(r[0]))
    return u_ids


def is_two_levels_of_approval(db):
    columns = "two_levels_of_approval"
    rows = db.get_data(tblClientGroups, columns, condition=None)
    return bool(rows[0]["two_levels_of_approval"])


def get_user_company_details(db, user_id):
    if is_primary_admin(db, user_id):
        condition = " 1 "
        condition_val = None
    else:
        condition = "  unit_id in ( " + \
            " SELECT unit_id FROM  tbl_user_units " + \
            " WHERE user_id = %s )"
        condition_val = [user_id]
    columns = [
        "unit_id", "division_id", "legal_entity_id", "business_group_id"
    ]
    rows = db.get_data(tblUnits, columns, condition, condition_val)

    unit_ids = []
    division_ids = []
    legal_entity_ids = []
    business_group_ids = []
    for row in rows:
        unit_ids.append(
            int(row["unit_id"])
        )
        if row["division_id"] is not None:
            if int(row["division_id"]) not in division_ids:
                division_ids.append(int(row["division_id"]))
        if int(row["legal_entity_id"]) not in legal_entity_ids:
            legal_entity_ids.append(int(row["legal_entity_id"]))
        if row["business_group_id"] is not None:
            if int(row["business_group_id"]) not in business_group_ids:
                business_group_ids.append(int(row["business_group_id"]))
    return (
        ",".join(str(x) for x in unit_ids),
        ",".join(str(x) for x in division_ids),
        ",".join(str(x) for x in legal_entity_ids),
        ",".join(str(x) for x in business_group_ids)
    )


def get_client_level_1_statutoy(db, user_id):
    query = "SELECT (case when (LEFT( " + \
            " statutory_mapping,INSTR(statutory_mapping,'>>')-1) = '') " + \
            " THEN " + \
            " statutory_mapping " + \
            " ELSE " + \
            " LEFT (statutory_mapping,INSTR(statutory_mapping,'>>')-1) " + \
            " END ) as statutory " + \
            " FROM tbl_compliances GROUP BY statutory"
    rows = db.select_all(query)
    columns = ["statutory"]
    result = convert_to_dict(rows, columns)
    return return_client_level_1_statutories(result)


def return_client_level_1_statutories(data):
    results = []
    for d in data:
        results.append(
            d["statutory"]
        )
    return results


def get_service_providers(db):
    columns = "service_provider_id, service_provider_name, is_active"
    condition = "1"
    rows = db.get_data(
        tblServiceProviders, columns, condition
    )
    return return_service_providers(rows)


def return_service_providers(service_providers):
    results = []
    for service_provider in service_providers:
        service_provider_obj = core.ServiceProvider(
            service_provider["service_provider_id"],
            service_provider["service_provider_name"],
            bool(service_provider["is_active"]))
        results.append(service_provider_obj)
    return results


def get_client_compliances(db, user_id):
    query = " SELECT compliance_id, document_name ,compliance_task " + \
            " FROM tbl_compliances"
    rows = db.select_all(query)
    columns = ["compliance_id", "document_name", "compliance_name"]
    result = convert_to_dict(rows, columns)
    return return_client_compliances(result)


def return_client_compliances(data):
    results = []
    for d in data:
        compliance_name = d["compliance_name"]
        if d["document_name"] not in ["None", None, ""]:
            compliance_name = "%s - %s" % (d["document_name"], compliance_name)
        results.append(core.ComplianceFilter(
            d["compliance_id"], compliance_name
        ))
    return results


def set_new_due_date(statutory_dates, repeats_type_id, compliance_id):
    due_date = None
    due_date_list = []
    date_list = []
    now = datetime.datetime.now()
    current_year = now.year
    current_month = now.month
    for date in statutory_dates:
            s_date = core.StatutoryDate(
                date["statutory_date"],
                date["statutory_month"],
                date["trigger_before_days"],
                date.get("repeat_by")
            )
            date_list.append(s_date)

            s_month = date["statutory_month"]
            s_day = date["statutory_date"]
            current_date = n_date = datetime.date.today()

            if s_date.statutory_date is not None:
                try:
                    n_date = n_date.replace(day=int(s_day))
                except ValueError:
                    if n_date.month == 12:
                        days = 31
                    else:
                        days = (n_date.replace(
                                    month=n_date.month+1, day=1
                                ) - datetime.timedelta(
                                    days=1)
                                ).day
                    n_date = n_date.replace(day=days)

            if s_date.statutory_month is not None:
                if s_date.statutory_date is not None:
                    n_date = n_date.replace(day=s_day, month=int(s_month))
                else:
                    try:
                        n_date = n_date.replace(month=int(s_month))
                    except ValueError:
                        if n_date.month == 12:
                            days = 31
                        else:
                            days = (
                                n_date.replace(
                                    day=1, month=s_month+1
                                ) - datetime.timedelta(days=1)).day
                        n_date = n_date.replace(day=days, month=int(s_month))
            if current_date > n_date:
                if repeats_type_id == 2 and len(statutory_dates) == 1:
                    try:
                        n_date = n_date.replace(month=current_month+1)
                    except ValueError:
                        if n_date.month == 12:
                            days = 31
                        else:
                            days = (
                                n_date.replace(
                                    day=1, month=current_month+1,
                                    year=current_year+1
                                ) - datetime.timedelta(days=1)).day
                        try:
                            n_date = n_date.replace(
                                day=days, month=current_month+1
                            )
                        except ValueError:
                            logger.logClient(
                                "error", "set_new_due_date", n_date
                            )
                            logger.logClient("error", "set_new_due_date", days)
                            logger.logClient(
                                "error", "set_new_due_date", current_month+1
                            )

                else:
                    try:
                        n_date = n_date.replace(year=current_year+1)
                    except ValueError:
                        if n_date.month == 12:
                            days = 31
                        else:
                            days = (
                                n_date.replace(
                                    day=1, month=n_date.month+1,
                                    year=current_year+1
                                ) - datetime.timedelta(days=1)).day

                        n_date = n_date.replace(day=days, year=current_year+1)
            if s_day is None and s_month is None:
                due_date = ""
            else:
                due_date = n_date.strftime("%d-%b-%Y")
            due_date_list.append(due_date)
    return due_date, due_date_list, date_list


def convert_datetime_to_date(val):
    if type(val) == datetime.datetime:
        return val.date()
    else:
        return val


def create_datetime_summary_text(r, diff, only_hours=False):
    summary_text = ""
    if(only_hours):
        if abs(r.hours) > 0:
            hours = abs(r.hours)
            if abs(r.months) > 0:
                hours = (diff.days * 24) + hours
            elif abs(r.days) > 0:
                hours = (abs(r.days) * 24) + hours
            summary_text += " %s.%s hour(s) " % (hours, abs(r.minutes))
        elif r.minutes > 0:
            summary_text += " %s minute(s) " % r.minutes
    else:
        if abs(r.years) > 0:
            summary_text += " %s year(s) " % abs(r.years)
        if abs(r.months) > 0:
            summary_text += " %s month(s) " % abs(r.months)
        if abs(r.days) > 0:
            summary_text += " %s day(s) " % abs(r.days)
    return summary_text


def calculate_ageing(
    due_date, frequency_type=None, completion_date=None, duration_type=None
):
    current_time_stamp = get_date_time_in_date()
    compliance_status = "-"
    # due_date = self.localize(due_date)
    if frequency_type == "On Occurrence":
        if completion_date is not None:  # Completed compliances
            r = relativedelta.relativedelta(
                convert_datetime_to_date(due_date),
                convert_datetime_to_date(completion_date)
            )
            diff = abs(due_date-completion_date)
            if r.days < 0 and r.hours < 0 and r.minutes < 0:
                compliance_status = "On Time"
            else:
                summary_text = "Delayed by "
                if duration_type in ["2", 2]:
                    compliance_status = (
                            summary_text + create_datetime_summary_text(
                                r, diff, only_hours=True
                            )
                        )
                else:
                    compliance_status = (
                        summary_text + create_datetime_summary_text(
                            r, diff, only_hours=False
                        )
                    )
                return r.days, compliance_status
        else:
            r = relativedelta.relativedelta(
                convert_datetime_to_date(due_date),
                convert_datetime_to_date(current_time_stamp)
            )
            diff = abs(due_date-current_time_stamp)
            summary_text = ""
            if duration_type in ["2", 2]:
                compliance_status = (
                        summary_text + create_datetime_summary_text(
                            r, diff, only_hours=True
                        )
                    )
            else:
                compliance_status = (
                        summary_text + create_datetime_summary_text(
                            r, diff, only_hours=False
                        )
                    )
            if r.days >= 0 and r.hours >= 0 and r.minutes >= 0:
                compliance_status += " left"
            else:
                compliance_status = " Overdue by " + compliance_status
            return r.days, compliance_status
    else:
        if completion_date is not None:  # Completed compliances
            compliance_status = "On Time"
            due_date = convert_datetime_to_date(due_date)
            completion_date = convert_datetime_to_date(completion_date)
            if due_date not in [None, "None", 0]:
                r = relativedelta.relativedelta(
                    due_date, completion_date
                )
                diff = abs(due_date-completion_date)
                compliance_status = (
                    "Delayed by " + create_datetime_summary_text(
                        r, diff, only_hours=False)
                )
                return r.days, compliance_status
        else:
            if due_date not in [None, "None", 0]:
                due_date = convert_datetime_to_date(due_date)
                current_time_stamp = convert_datetime_to_date(
                    current_time_stamp)
                r = relativedelta.relativedelta(due_date, current_time_stamp)
                diff = abs(due_date-current_time_stamp)
                compliance_status = create_datetime_summary_text(
                    r, diff, only_hours=False
                )
                if r.days < 0:
                    compliance_status = "Overdue by " + compliance_status
                else:
                    compliance_status = compliance_status + " left"
                return r.days, compliance_status
    return 0, compliance_status


def get_client_settings(db):
    query = "SELECT two_levels_of_approval " + \
        " FROM tbl_client_groups"
    row = db.select_one(query)
    if row:
        return bool(int(row[0]))


def get_admin_info(db):
    query = "SELECT email_id from tbl_users"
    row = db.select_one(query)
    return int(row[0])


def validate_compliance_due_date(db, request):
    c_ids = []
    for c in request.compliances:
        c_ids.append(c.compliance_id)
        q = "SELECT compliance_id, compliance_task, " + \
            " statutory_dates, repeats_type_id from tbl_compliances " + \
            " where compliance_id = %s"
        param = [int(c.compliance_id)]
        row = db.select_one(q, param)
        if row:
            comp_id = row[0]
            task = row[1]
            s_dates = json.loads(row[2])
            repeats_type_id = row[3]
            due_date, due_date_list, date_list = set_new_due_date(
                s_dates, repeats_type_id, comp_id
            )
            if c.due_date not in [None, ""] and due_date not in [None, ""]:
                t_due_date = datetime.datetime.strptime(c.due_date, "%d-%b-%Y")
                n_due_date = datetime.datetime.strptime(due_date, "%d-%b-%Y")
                if c.validity_date is None :
                    if (n_due_date < t_due_date):
                        # Due date should be lessthen statutory date
                        return False, task
                else :
                    v_due_date = datetime.datetime.strptime(c.validity_date, "%d-%b-%Y")
                    if (t_due_date > v_due_date):
                        return False, task
    return True, None


def get_compliance_frequency(db, condition="1"):
    columns = "frequency_id, frequency"
    rows = db.get_data(
        tblComplianceFrequency, columns, condition
    )
    compliance_frequency = []
    for row in rows:
        compliance_frequency.append(
            core.ComplianceFrequency(
                row["frequency_id"],
                core.COMPLIANCE_FREQUENCY(row["frequency"])
                )
            )
    return compliance_frequency


def get_user_ids_by_unit_and_domain(
    db, unit_id, domain_id
):
    unit_user_rows = db.get_data(
        tblUserUnits, "user_id",
        "unit_id = %s", [unit_id]
    )
    unit_users = [
        int(unit_user["user_id"]) for unit_user in unit_user_rows
    ]

    domain_user_rows = db.get_data(
        tblUserDomains, "user_id",
        "domain_id = %s", [domain_id]
    )
    domain_users = [
        int(domain_user["user_id"]) for domain_user in domain_user_rows
    ]

    users = list(set(unit_users).intersection(domain_users))
    if len(users) > 0:
        user_ids = ",".join(str(x) for x in users)
    else:
        user_ids = None
    return user_ids


def get_users_by_unit_and_domain(
    db, unit_id, domain_id
):
    user_ids = get_user_ids_by_unit_and_domain(
        db, unit_id, domain_id
    )
    if user_ids is not None:
        columns = "user_id, employee_name, employee_code, is_active"
        condition = " is_active = 1 and user_id in (%s)"
        condtion_val = [user_ids]
        rows = db.get_data(
            tblUsers, columns, condition, condtion_val
        )
    return return_users(rows)


def get_all_users(db):
    columns = [
        "user_id", "employee_code", "employee_name",
        "contact_no", "email_id"
    ]
    q = "select user_id, IFNULL(employee_code, '-'), employee_name, " + \
        " IFNULL(contact_no, '--'), email_id from tbl_users"
    data = db.select_all(q)
    rows = convert_to_key_dict(data, columns)
    return rows


def get_users(db):
    columns = "user_id, employee_name, employee_code, is_active"
    condition = "1"
    rows = db.get_data(
        tblUsers, columns, condition
    )
    return return_users(rows)


def get_users_by_id(db, user_ids):
    columns = "user_id, employee_name, employee_code, is_active"
    condition = " user_id in (%s)"
    condition_val = [user_ids]
    rows = db.get_data(
        tblUsers, columns, condition, condition_val
    )
    return return_users(rows)


def return_users(users):
    results = []
    for user in users:
        if user["employee_code"] is not None:
            employee_name = "%s - %s" % (
                user["employee_code"], user["employee_name"]
            )
        else:
            employee_name = "Administrator"
        results.append(core.User(
            user["user_id"], employee_name, bool(user["is_active"])
        ))
    return results


def get_compliance_name_by_id(db, compliance_id):
    column = "document_name, compliance_task"
    condition = "compliance_id = %s"
    condition_val = [compliance_id]
    rows = db.get_data(
        tblCompliances, column, condition, condition_val
    )
    compliance_name = ""
    if rows[0]["document_name"] is not None:
        if str(rows[0]["document_name"]) == "None":
            compliance_name = rows[0]["compliance_task"]
        else:
            compliance_name += rows[0][
                    "document_name"
                ]+" - "+rows[0]["compliance_task"]
    else:
        compliance_name = rows[0]["compliance_task"]
    return compliance_name


def is_space_available(db, upload_size):
    columns = "(total_disk_space - total_disk_space_used) as space"
    rows = db.get_data(tblClientGroups, columns, "1")
    remaining_space = rows[0]["space"]
    if upload_size < remaining_space:
        return True
    else:
        return False


def update_used_space(db, file_size):
    columns = ["total_disk_space_used"]
    condition = "1"
    db.increment(
        tblClientGroups, columns, condition, value=file_size
    )

    total_used_space = 0
    rows = db.get_data(
        tblClientGroups, "total_disk_space_used, client_id", "1"
    )
    client_id = rows[0]["client_id"]
    if rows[0]["total_disk_space_used"] is not None:
        total_used_space = int(rows[0]["total_disk_space_used"])

    UpdateFileSpace(total_used_space, client_id)


def save_compliance_activity(
    db, unit_id, compliance_id, activity_status, compliance_status,
    remarks
):
    date = get_date_time()
    columns = [
        "unit_id", "compliance_id",
        "activity_date", "activity_status", "compliance_status",
        "updated_on"
    ]
    values = [
        unit_id, compliance_id, date, activity_status,
        compliance_status,  date
    ]
    if remarks:
        columns.append("remarks")
        values.append(remarks)
    result = db.insert(
       tblComplianceActivityLog, columns, values
    )
    if result is False:
        raise client_process_error("E018")


def save_compliance_notification(
    db, compliance_history_id, notification_text, category, action
):
    current_time_stamp = get_date_time_in_date()

    # Get history details from compliance history id
    history_columns = [
        "unit_id", "compliance_id", "completed_by",
        "concurred_by", "approved_by"
    ]
    history_condition = "compliance_history_id = %s"
    history_condition_val = [compliance_history_id]
    history_rows = db.get_data(
        tblComplianceHistory, history_columns,
        history_condition, history_condition_val
    )
    history = history_rows[0]
    unit_id = history["unit_id"]
    compliance_id = history["compliance_id"]

    # Getting Unit details from unit_id
    unit_columns = [
        "country_id", "business_group_id", "legal_entity_id", "division_id"
    ]
    unit_condition = "unit_id = %s"
    unit_condition_val = [int(unit_id)]
    unit_rows = db.get_data(
        tblUnits, unit_columns, unit_condition, unit_condition_val
    )
    # unit_columns_list = [
    #     "country_id", "business_group_id", "legal_entity_id", "division_id"
    # ]
    unit = unit_rows[0]  # convert_to_dict(unit_rows[0], unit_columns_list)

    # Getting compliance_details from compliance_id
    compliance_columns = "domain_id"
    compliance_condition = "compliance_id = %s "
    compliance_condition_val = [compliance_id]
    compliance_rows = db.get_data(
        tblCompliances, compliance_columns,
        compliance_condition, compliance_condition_val
    )
    domain_id = compliance_rows[0]["domain_id"]

    # Saving notification
    columns = [
        "country_id", "domain_id", "business_group_id",
        "legal_entity_id", "division_id", "unit_id", "compliance_id",
        "assignee", "concurrence_person", "approval_person",
        "notification_type_id", "notification_text", "extra_details",
        "created_on"
    ]
    extra_details = "%s-%s" % (compliance_history_id, category)
    values = [
        unit["country_id"], domain_id, unit["business_group_id"],
        unit["legal_entity_id"], unit["division_id"], unit_id, compliance_id,
        history["completed_by"], history["concurred_by"],
        history["approved_by"], 1, notification_text, extra_details,
        current_time_stamp
    ]
    notification_id = db.insert(tblNotificationsLog, columns, values)
    if notification_id is False:
        raise client_process_error("E019")

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
    r1 = db.insert(tblNotificationUserLog, columns, values)
    if r1 is False:
        raise client_process_error("E019")
    return r1


def get_user_countries(db, user_id):
    q = "select country_id from tbl_countries"
    param = None
    condition = ""
    if is_primary_admin(db, user_id) is not True:
        q = "select country_id from tbl_user_countries"
        condition = " WHERE user_id = %s"
        param = [user_id]
    rows = db.select_all(q + condition, param)
    c_ids = []
    for r in rows:
        c_ids.append(int(r[0]))
    return c_ids


def get_email_id_for_users(db, user_id):
    q = "SELECT employee_name, email_id from tbl_users where user_id = %s" % (
        user_id
    )
    row = db.select_one(q)
    if row:
        return row[0], row[1]
    else:
        return None


def get_user_email_name(db, user_ids):
    index = None
    column = "email_id, employee_name"
    condition = "user_id in (%s)"
    condition_val = [",".join(str(x) for x in user_ids)]
    rows = db.get_data(
        tblUsers, column, condition, condition_val
    )
    email_ids = ""
    employee_name = ""
    for index, row in enumerate(rows):
        if index == 0:
            if row["employee_name"] is not None:
                employee_name += "%s" % row["employee_name"]
            email_ids += "%s" % row["email_id"]
        else:
            if row["employee_name"] is not None:
                employee_name += ", %s" % row["employee_name"]
            email_ids += ", %s" % row["email_id"]
    # if admin_email is not None:
    #     employee_name += "Administrator"
    #     email_ids += admin_email

    return email_ids, employee_name


def calculate_from_and_to_date_for_domain(db, country_id, domain_id):
    columns = "contract_from, contract_to"
    rows = db.get_data(tblClientGroups, columns, "1")
    if rows:
        contract_from = rows[0]["contract_from"]
    else:
        contract_from = None
    # contract_to = rows[0][1]

    columns = "period_from, period_to"
    condition = "country_id = %s and domain_id = %s"
    condition_val = [country_id, domain_id]
    rows = db.get_data(
        tblClientConfigurations, columns, condition, condition_val
    )
    period_from = rows[0]["period_from"]

    to_date = contract_from
    current_year = to_date.year
    previous_year = current_year-1
    from_date = datetime.date(previous_year, period_from, 1)
    r = relativedelta.relativedelta(
        convert_datetime_to_date(to_date),
        convert_datetime_to_date(from_date)
    )
    no_of_years = r.years
    no_of_months = r.months
    if no_of_years is not 0 or no_of_months >= 12:
        from_date = datetime.date(current_year, period_from, 1)
    return from_date, to_date


def calculate_due_date(
    db, country_id, domain_id, statutory_dates=None, repeat_by=None,
    repeat_every=None, due_date=None
):
    def is_future_date(test_date):
        result = False
        current_date = datetime.date.today()
        if type(test_date) == datetime.datetime:
            test_date = test_date.date()
        if ((current_date - test_date).days < 0):
            result = True
        return result
    from_date, to_date = calculate_from_and_to_date_for_domain(
        db, country_id, domain_id
    )
    due_dates = []
    summary = ""
    # For Monthly Recurring compliances
    if statutory_dates and len(json.loads(statutory_dates)) > 1:
        summary += "Every %s month(s) (" % (repeat_every)
        for statutory_date in json.loads(statutory_dates):
            date = statutory_date["statutory_date"]
            month = statutory_date["statutory_month"]
            summary += "%s %s " % (db.string_months[month], date)
            current_date = datetime.datetime.today().date()
            due_date_guess = datetime.date(current_date.year, month, date)
            real_due_date = None
            if is_future_date(due_date_guess):
                real_due_date = datetime.date(
                    current_date.year - 1, month, date
                )
            else:
                real_due_date = due_date_guess
            if from_date <= real_due_date <= to_date:
                due_dates.append(
                    real_due_date
                )
            else:
                continue
        summary += ")"
    elif repeat_by:
        date_details = ""
        if statutory_dates not in ["None", None, ""]:
            statutory_date_json = json.loads(statutory_dates)
            if len(statutory_date_json) > 0:
                date_details += "(%s)" % (
                    statutory_date_json[0]["statutory_date"]
                )
        # For Compliances Recurring in days
        if repeat_by == 1:  # Days
            summary = "Every %s day(s)" % (repeat_every)
            previous_year_due_date = datetime.date(
                due_date.year - 1, due_date.month, due_date.day
            )
            if from_date <= previous_year_due_date <= to_date:
                due_dates.append(previous_year_due_date)
            iter_due_date = previous_year_due_date
            while not is_future_date(iter_due_date):
                iter_due_date = iter_due_date + datetime.timedelta(
                    days=repeat_every
                )
                if from_date <= iter_due_date <= to_date:
                    due_dates.append(iter_due_date)
        elif repeat_by == 2:   # Months
            summary = "Every %s month(s) %s " % (repeat_every, date_details)
            iter_due_date = due_date
            while iter_due_date > from_date:
                iter_due_date = iter_due_date + relativedelta.relativedelta(
                    months=-repeat_every
                )
                if from_date <= iter_due_date <= to_date:
                    due_dates.append(iter_due_date)
        elif repeat_by == 3:   # Years
            summary = "Every %s year(s) %s" % (repeat_every, date_details)
            year = from_date.year
            while year <= to_date.year:
                due_date = datetime.date(
                    year, due_date.month, due_date.day
                )
                if from_date <= due_date <= to_date:
                    due_dates.append(due_date)
                year += 1
    if len(due_dates) >= 2:
        if due_dates[0] > due_dates[1]:
            due_dates.reverse()
    return due_dates, summary


def filter_out_due_dates(db, unit_id, compliance_id, due_dates_list):
    # Checking same due date already exists
    if due_dates_list is not None and len(due_dates_list) > 0:
        formated_date_list = []
        for x in due_dates_list:
            x = str(x)
            x.replace(" ", "")
            formated_date_list.append("%s" % (x))
            # if len(formated_date_list) == 1:
            #     formated_date_list.append(formated_date_list[0])
        (
            due_date_condition, due_date_condition_val
        ) = db.generate_tuple_condition(
            "DATE(due_date)", due_dates_list
        )
        query = " SELECT is_ok FROM " + \
            " (SELECT (CASE WHEN (unit_id = %s " + \
            " AND " + due_date_condition + \
            " AND compliance_id = %s) THEN DATE(due_date) " + \
            " ELSE 'NotExists' END ) as " + \
            " is_ok FROM tbl_compliance_history ) a WHERE is_ok != 'NotExists'"
        rows = db.select_all(
            query, [unit_id, due_date_condition_val, compliance_id]
        )
        if len(rows) > 0:
            for row in rows:
                formated_date_list.remove("%s" % (row[0]))
        result_due_date = []
        for current_due_date_index, due_date in enumerate(formated_date_list):
            next_due_date = None

            if len(due_dates_list) < current_due_date_index + 1:
                continue
            else:
                if current_due_date_index == len(formated_date_list)-1:
                    next_due_date = due_dates_list[current_due_date_index]
                else:
                    next_due_date = due_dates_list[current_due_date_index+1]

                columns = "count(*) as compliance"
                condition = "unit_id = %s AND due_date <= %s " + \
                    " AND compliance_id = %s AND " + \
                    " approve_status = 1 and validity_date >= %s "

                condition_val = [
                    unit_id, due_date, compliance_id, next_due_date
                ]
                rows = db.get_data(
                    tblComplianceHistory, columns, condition, condition_val
                )
                if rows[0]["compliance"] > 0:
                    continue
                else:
                    result_due_date.append(due_date)
        return result_due_date
    else:
        return []


def convert_base64_to_file(file_name, file_content, client_id):
    client_directory = "%s/%s" % (CLIENT_DOCS_BASE_PATH, client_id)
    file_path = "%s/%s" % (client_directory, file_name)
    if not os.path.exists(client_directory):
        os.makedirs(client_directory)
    remove_uploaded_file(file_path)
    if file_content is not None:
        with io.FileIO(file_path, "wb") as fn:
            fn.write(file_content.decode('base64'))


def get_user_name_by_id(db, user_id):
    employee_name = None
    if user_id is not None and user_id != 0:
        columns = "employee_code, employee_name"
        condition = "user_id = %s "
        condition_val = [user_id]
        rows = db.get_data(
            tblUsers, columns, condition, condition_val
        )
        if len(rows) > 0:
            employee_name = "%s - %s" % (
                rows[0]["employee_code"], rows[0]["employee_name"]
            )
    else:
        employee_name = "Administrator"
    return employee_name


def get_form_ids_for_admin(db):
    columns = ["form_id"]
    condition = " is_admin = 1 OR form_type_id in (4,5) " + \
        " OR form_id in (1, 9,11,10,12)"
    rows = db.get_data(
        tblForms, columns, condition
    )
    form_ids = [
        row["form_id"] for row in rows
    ]
    return ",".join(str(x) for x in form_ids)


def get_report_form_ids(db):
    columns = ["form_id"]
    condition = " form_type_id = 3"
    rows = db.get_data(
        tblForms, columns, condition
    )
    form_ids = [
        row["form_id"] for row in rows
    ]
    return ",".join(str(x) for x in form_ids)


def get_client_id_from_short_name(db, short_name):
    columns = "client_id"
    condition = "url_short_name = %s"
    condition_val = [short_name]
    rows = db.get_data(
        "tbl_client_groups", columns, condition, condition_val
    )
    return rows[0]["client_id"]


def validate_reset_token(db, reset_token):
    column = "count(*) as result, user_id"
    condition = " verification_code=%s"
    condition_val = [reset_token]
    rows = db.get_data(
        tblEmailVerification, column, condition, condition_val
    )
    count = rows[0]["result"]
    user_id = rows[0]["user_id"]
    if count == 1:
        column = "count(*) as usercount"
        condition = "user_id = %s and is_active = 1"
        condition_val = [user_id]
        rows = db.get_data(tblUsers, column, condition, condition_val)
        if rows[0]["usercount"] > 0 or user_id == 0:
            return user_id
        else:
            return None
    else:
        return None


def update_password(db, password, user_id):
    columns = ["password"]
    values = [encrypt(password)]
    condition = "1"
    result = False
    condition = " user_id=%s"
    values.append(user_id)
    result = db.update(
        tblUsers, columns, values, condition
    )
    columns = "employee_code, employee_name"
    condition = "user_id = %s"
    condition_val = [user_id]
    rows = db.get_data(tblUsers, columns, condition, condition_val)
    employee_name = rows[0]["employee_name"]
    if rows[0]["employee_code"] is not None:
        employee_name = "%s - %s" % (
            rows[0]["employee_code"], rows[0]["employee_name"]
        )
    else:
        employee_name = rows[0]["employee_name"]

    action = "\"%s\" has updated his/her password" % (employee_name)
    db.save_activity(user_id, 0, action)

    if result:
        return True
    else:
        return False


def delete_used_token(db, reset_token):
    condition = " verification_code=%s"
    condition_val = [reset_token]
    if db.delete(tblEmailVerification, condition, condition_val):
        return True
    else:
        return False


def remove_session(db, session_token):
    condition = "session_token = %s"
    condition_val = [session_token]
    if db.delete(tblUserSessions, condition, condition_val):
        return True
    else:
        return False


def update_profile(db, contact_no, address, session_user):
    columns = ["contact_no", "address"]
    values = [contact_no, address, session_user]
    condition = "user_id= %s"
    db.update(tblUsers, columns, values, condition)


def is_service_proivder_user(db, user_id):
    column = "count(1) as result"
    condition = "user_id = %s and is_service_provider = 1"
    condition_val = [user_id]
    rows = db.get_data(tblUsers, column, condition, condition_val)
    if rows[0]["result"] > 0:
        return True
    else:
        return False


def get_trail_id(db, type=None):
    if type is None:
        query = "select IFNULL(MAX(audit_trail_id), 0) as audit_trail_id " + \
            " from tbl_audit_log;"
    else:
        query = "select IFNULL(MAX(domain_trail_id), 0) as audit_trail_id " + \
            " from tbl_audit_log;"
    row = db.select_one(query)
    trail_id = row[0]
    return trail_id


def update_traild_id(db, audit_trail_id, get_type=None):
    if get_type is None:
        query = "UPDATE tbl_audit_log SET audit_trail_id=%s;" % (
            audit_trail_id
        )
    else:
        query = "UPDATE tbl_audit_log SET domain_trail_id=%s;" % (
            audit_trail_id
        )
    db.execute(query)


def reset_domain_trail_id(db):
    q = "update tbl_audit_log set domain_trail_id=0"
    db.execute(q)
