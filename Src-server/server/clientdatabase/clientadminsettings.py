
from server.common import (
    datetime_to_string
    )

all__ = [
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
    columns = "tcu.user_id, tcu.email_id, tcu.employee_name, tcu.employee_code," + \
        " tcu.contact_no, tcu.is_admin, tu.unit_code, tu.unit_name, tu.address," + \
        " tcu.is_active, tsp.service_provider_name"
    tables = [tblUsers, tblUnits, tblServiceProviders]
    aliases = ["tcu", "tu", "tsp"]
    join_type = "left join"
    join_conditions = [
        "tcu.seating_unit_id = tu.unit_id",
        "tcu.service_provider_id=tsp.service_provider_id"
    ]
    where_condition = "1"
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

    admin_columns = "username"
    admin_condition = "1"
    result = db.get_data(
        tblAdmin, admin_columns, admin_condition
    )
    admin_email = result[0][0]
    is_admin_is_a_user = False

    licence_holder_rows = get_licence_holder_details(db, client_id)
    licence_holders = []
    for row in licence_holder_rows:
        employee_name = None
        unit_name = None
        if(row[3] == None):
            employee_name = row[2]
        else:
            employee_name = "%s - %s" % (row[3], row[2])

        if row[7] == None:
            unit_name = row[10]
        else:
            unit_name = "%s - %s" % (row[6], row[7])
        user_id = row[0]
        email_id = row[1]
        if email_id == admin_email:
            is_admin_is_a_user = True
            employee_name = "Administrator: %s" % employee_name
        contact_no = row[4]
        is_admin = row[5]
        address = row[8]
        is_active = row[9]
        licence_holders.append(
            clientadminsettings.LICENCE_HOLDER(
                user_id, employee_name, email_id, contact_no,
                unit_name, address
            ))
    remaining_licence = (no_of_user_licence) - len(licence_holder_rows)
    if not is_admin_is_a_user:
        licence_holders.append(
            clientadminsettings.LICENCE_HOLDER(
                0, "Administrator", admin_email, None,
                None, None
            ))
        remaining_licence -= 1

    used_space = round((total_disk_space_used/1000000000), 2)
    total_space = total_disk_space/1000000000

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
    is_two_levels_of_approval = 1 if is_two_levels_of_approval == True else 0
    values = [
        is_two_levels_of_approval, assignee_reminder_days,
        escalation_reminder_In_advance_days, escalation_reminder_days
    ]
    condition = "1"
    db.update(tblClientGroups, columns, values, condition, client_id)

    action = "Settings Updated"
    db.save_activity(0, 25, action)