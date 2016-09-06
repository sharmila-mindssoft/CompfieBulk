from server.clientdatabase.tables import *

from protocol import (
  clientadminsettings
)

from server.common import (
    datetime_to_string
    )

__all__ = [
    "get_settings",
    "get_profile",
    "updateSettings"
]


#
#   Client Admin Settings
#
def get_settings(db, client_id):
    columns = "two_levels_of_approval, assignee_reminder, " + \
        "escalation_reminder_in_advance, escalation_reminder," + \
        "contract_from, contract_to, no_of_user_licence, " + \
        "total_disk_space, total_disk_space_used"
    condition = "1"
    rows = db.get_data(
        tblClientGroups, columns, condition
    )
    if len(rows) > 0:
        row = rows[0]
        return row
    else:
        return None


def get_licence_holder_details(db, client_id):
    columns = [
        "tcu.user_id", "tcu.email_id", "tcu.employee_name",
        "ifnull(tcu.employee_code, 0) as employee_code",
        "tcu.contact_no", "tcu.is_admin", "tu.unit_code",
        "tu.unit_name", "tu.address",
        "tcu.is_active", "tsp.service_provider_name", "tcu.is_primary_admin",
        "ifnull(tcu.is_service_provider, 0) as is_service_provider"
    ]
    tables = [tblUsers, tblUnits, tblServiceProviders]
    aliases = ["tcu", "tu", "tsp"]
    join_type = "left join"
    join_conditions = [
        "tcu.seating_unit_id = tu.unit_id",
        "tcu.service_provider_id = tsp.service_provider_id"
    ]
    where_condition = "1 order by tcu.user_id"
    return db.get_data_from_multiple_tables(
        columns, tables, aliases,
        join_type, join_conditions,
        where_condition
    )


def get_profile(
    db, contract_from, contract_to, no_of_user_licence,
    total_disk_space, total_disk_space_used, client_id
):
    contract_from = datetime_to_string(contract_from)
    contract_to = datetime_to_string(contract_to)

    licence_holder_rows = get_licence_holder_details(db, client_id)
    licence_holders = []
    for row in licence_holder_rows:
        employee_name = None
        unit_name = None
        if row["is_service_provider"] == 0:
            if(row["employee_code"] == "0"):
                employee_name = row["employee_name"]
            else:
                employee_name = "%s - %s" % (
                    row["employee_code"], row["employee_name"]
                )
        else:
            employee_name = "%s - %s" % (
                row["service_provider_name"], row["employee_name"]
            )

        if row["unit_name"] == None:
            unit_name = " - "
        else:
            unit_name = "%s - %s" % (row["unit_code"], row["unit_name"])
        user_id = row["user_id"]
        email_id = row["email_id"]
        contact_no = row["contact_no"]
        address = row["address"]
        is_admin = False if (row["is_admin"] == 0) else True
        is_active = False if (row["is_active"] == 0) else True
        is_primary_admin = False if (row["is_primary_admin"] == 0) else True
        licence_holders.append(
            clientadminsettings.LICENCE_HOLDER(
                user_id, employee_name, email_id, contact_no,
                unit_name, address, is_admin, is_active, is_primary_admin
            ))
    remaining_licence = (no_of_user_licence) - len(licence_holder_rows)

    used_space = round((total_disk_space_used/(1024 * 1024 * 1024)), 2)
    total_space = round(total_disk_space/(1024 * 1024 * 1024), 2)

    profile_detail = clientadminsettings.PROFILE_DETAIL(
        contract_from,
        contract_to,
        no_of_user_licence,
        remaining_licence,
        licence_holders,
        total_space,
        used_space
    )
    return profile_detail


def updateSettings(
    db, is_two_levels_of_approval, assignee_reminder_days,
    escalation_reminder_In_advance_days, escalation_reminder_days, client_id
):
    columns = [
        "two_levels_of_approval", "assignee_reminder",
        "escalation_reminder_in_advance", "escalation_reminder"
    ]
    is_two_levels_of_approval = 1 if is_two_levels_of_approval is True else 0
    values = [
        is_two_levels_of_approval, assignee_reminder_days,
        escalation_reminder_In_advance_days, escalation_reminder_days
    ]
    condition = "1"
    db.update(tblClientGroups, columns, values, condition)

    action = "Settings Updated"
    db.save_activity(0, 25, action)
