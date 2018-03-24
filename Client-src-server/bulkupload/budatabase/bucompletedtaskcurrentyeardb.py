from server.exceptionmessage import fetch_error
import traceback
from server import logger
from ..buapiprotocol import bucompletedtaskcurrentyearprotocol as bu_ct

import datetime

__all__ = [
    # "get_uploaded_statutory_mapping_csv_list"
    # "get_legal_entity_domains"
]

########################################################
# To get the compliances under the selected filters
# Completed Task - Current Year (Past Data)
########################################################


def get_statutory_wise_compliances(
    db, unit_id, domain_id, level_1_statutory_name, frequency_name,
    session_user, start_count, to_count
):
    condition = ""
    condition_val = []
    if frequency_name is not None:
        condition += "AND c.frequency_id = (SELECT frequency_id " + \
            " FROM tbl_compliance_frequency WHERE " + \
            " frequency = %s)"
        condition_val.append(frequency_name)
    else:
        condition += "AND c.frequency_id in (1,2,3)"

    if level_1_statutory_name is not None:
        condition += " AND statutory_mapping like %s"
        condition_val.append("%" + str(level_1_statutory_name + "%"))

    query = "SELECT ac.compliance_id, ac.statutory_dates, ac.due_date, " + \
        " assignee, employee_code, employee_name, " + \
        " SUBSTRING_INDEX(substring(substring(statutory_mapping,3),1, " + \
        " char_length(statutory_mapping) -4), '>>', 1) as statutory_mapping, " + \
        " document_name, compliance_task, compliance_description, " + \
        " c.repeats_type_id, rt.repeat_type, c.repeats_every, frequency, " + \
        " c.frequency_id FROM tbl_assign_compliances ac " + \
        " INNER JOIN tbl_users u ON (ac.assignee = u.user_id) " + \
        " INNER JOIN tbl_compliances c ON " + \
        " (ac.compliance_id = c.compliance_id) " + \
        " INNER JOIN tbl_compliance_frequency f " + \
        " ON (c.frequency_id = f.frequency_id) " + \
        " INNER JOIN tbl_compliance_repeat_type rt " + \
        " ON (c.repeats_type_id = rt.repeat_type_id) " + \
        " WHERE ac.is_active = 1 " + \
        " AND c.domain_id = %s AND ac.unit_id = %s "
    param = [
        domain_id, unit_id
    ]
    if condition != "":
        query += condition
        param.extend(condition_val)

    rows = db.select_all(query, param)

    level_1_statutory_wise_compliances = {}
    total_count = 0
    compliance_count = 0
    for compliance in rows:
        # statutories = compliance["statutory_mapping"].split(">>")

        # s_maps = json.loads(compliance["statutory_mapping"])
        # statutories = s_maps[0]
        s_maps = compliance["statutory_mapping"]
        statutories = s_maps

        if level_1_statutory_name is None or level_1_statutory_name == "" :
            level_1 = statutories
        else:
            level_1 = level_1_statutory_name

        if level_1 not in level_1_statutory_wise_compliances:
            level_1_statutory_wise_compliances[level_1] = []

        compliance_name = compliance["compliance_task"]
        if compliance["document_name"] not in (None, "None", ""):
            compliance_name = "%s - %s" % (
                compliance["document_name"], compliance_name
            )
        employee_code = compliance["employee_code"]
        if employee_code is None:
            employee_code = "Administrator"
        assingee_name = "%s - %s" % (
            employee_code, compliance["employee_name"]
        )
        due_dates = []
        summary = ""

        if compliance["repeats_type_id"] == 1:  # Days
            due_dates, summary = calculate_due_date(
                db,
                repeat_by=1,
                repeat_every=compliance["repeats_every"],
                due_date=compliance["due_date"],
                domain_id=domain_id
            )
        elif compliance["repeats_type_id"] == 2:  # Months
            due_dates, summary = calculate_due_date(
                db,
                statutory_dates=compliance["statutory_dates"],
                repeat_by=2,
                repeat_every=compliance["repeats_every"],
                due_date=compliance["due_date"],
                domain_id=domain_id
            )
        elif compliance["repeats_type_id"] == 3:  # years
            due_dates, summary = calculate_due_date(
                db,
                repeat_by=3,
                statutory_dates=compliance["statutory_dates"],
                repeat_every=compliance["repeats_every"],
                due_date=compliance["due_date"],
                domain_id=domain_id
            )

        final_due_dates = filter_out_due_dates(
            db, unit_id, compliance["compliance_id"], due_dates
        )
        total_count += len(final_due_dates)

        for due_date in final_due_dates:
            if (
                int(start_count) <= compliance_count and
                compliance_count < (int(start_count)+to_count)
            ):
                due_date_parts = due_date.replace("'", "").split("-")
                year = due_date_parts[0]
                month = due_date_parts[1]
                day = due_date_parts[2]
                due_date = datetime.date(int(year), int(month), int(day))

                statutories_strip = statutories[0].strip()

                level_1_statutory_wise_compliances[level_1].append(
                    clienttransactions.UNIT_WISE_STATUTORIES_FOR_PAST_RECORDS(
                        compliance["compliance_id"], compliance_name,
                        compliance["compliance_description"],
                        clientcore.COMPLIANCE_FREQUENCY(compliance["frequency"]),
                        summary, datetime_to_string(due_date),
                        assingee_name, compliance["assignee"]
                    )
                )
                compliance_count += 1
            elif compliance_count > (int(start_count)+to_count):
                break
            else:
                compliance_count += 1
                continue

    statutory_wise_compliances = []
    for (
        level_1_statutory_name, compliances
    ) in level_1_statutory_wise_compliances.iteritems():

        if len(compliances) > 0:
            statutory_wise_compliances.append(
                clienttransactions.STATUTORY_WISE_COMPLIANCES(
                    level_1_statutory_name, compliances
                )
            )
    return statutory_wise_compliances, total_count

