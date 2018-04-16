
import os
import json

from server.database.tables import *
from server.database.forms import *
from protocol import (core, knowledgetransaction)
from server.constants import (
    KNOWLEDGE_FORMAT_DOWNLOAD_URL, KNOWLEDGE_FORMAT_PATH
)
from server.common import (
    convert_to_dict, get_date_time, datetime_to_string_time, make_summary
)
from server.database.general import(
    return_compliance_frequency, return_compliance_duration,
    return_compliance_repeat, return_approval_status
)
from server.database.knowledgemaster import (
    STATUTORY_PARENTS, GEOGRAPHY_PARENTS,
    get_geographies, get_statutory_master,
    get_statutory_by_id, get_geography_by_id,
    get_industry_by_id, return_geography_levels,
    return_statutory_levels
)
from server.exceptionmessage import process_error, fetch_error


APPROVAL_STATUS = ["Yet to submit", "Pending", "Approved", "Rejected", "Approved & Notified"]

__all__ = [
    "save_messages"
]

def get_compliance_by_id(db, compliance_id, is_active=None):
    q = ""
    if is_active is None:
        if type(compliance_id) == int:
            q = " WHERE t1.compliance_id = %s"
            value = [compliance_id]
        else:
            q = " WHERE t1.compliance_id in %s"
            value = [tuple(compliance_id)]
    else:
        is_active = int(is_active)

        if type(compliance_id) == int:
            q = " WHERE t1.is_active = %s AND t1.compliance_id = %s"
            value = [is_active, compliance_id]
        else:
            q = " WHERE t1.is_active = %s AND t1.compliance_id in %s"
            value = [is_active, tuple(compliance_id)]

    qry = "SELECT t1.compliance_id, t1.statutory_provision, " + \
        " t1.compliance_task, t1.compliance_description, " + \
        " t1.document_name, t1.format_file, t1.format_file_size, " + \
        " t1.penal_consequences, t1.frequency_id, " + \
        " t1.statutory_dates, t1.repeats_every, " + \
        " t1.repeats_type_id, " + \
        " t1.duration, t1.duration_type_id, t1.is_active, " + \
        " (select frequency from tbl_compliance_frequency " + \
        " where frequency_id = t1.frequency_id), " + \
        " (select duration_type from tbl_compliance_duration_type " + \
        " where duration_type_id = t1.duration_type_id) duration_type, " +\
        " (select repeat_type from tbl_compliance_repeat_type " + \
        " where repeat_type_id = t1.repeats_type_id) repeat_type " + \
        " FROM tbl_compliances t1 %s ORDER BY t1.frequency_id" % q
    rows = db.select_all(qry, value)
    columns = [
        "compliance_id", "statutory_provision",
        "compliance_task", "compliance_description",
        "document_name", "format_file",
        "format_file_size", "penal_consequences",
        "frequency_id", "statutory_dates", "repeats_every",
        "repeats_type_id", "duration", "duration_type_id",
        "is_active", "frequency",
        "duration_type", "repeat_type"
    ]
    result = []
    if rows:
        result = convert_to_dict(rows, columns)
    return return_compliance(result)


def return_compliance(data):
    compliance_names = []
    compalinaces = []
    for d in data:
        statutory_dates = d["statutory_dates"]
        if statutory_dates is not None :
            statutory_dates = json.loads(statutory_dates)
        date_list = []
        for date in statutory_dates:
            s_date = core.StatutoryDate(
                date["statutory_date"],
                date["statutory_month"],
                date["trigger_before_days"],
                date.get("repeat_by")
            )
            date_list.append(s_date)

        compliance_task = d["compliance_task"]
        document_name = d["document_name"]
        if document_name == "None":
            document_name = None
        if document_name:
            name = "%s - %s" % (
                document_name, compliance_task
            )
        else:
            name = compliance_task
        format_file = d["format_file"]
        format_file_size = d["format_file_size"]
        if format_file_size is not None:
            format_file_size = int(format_file_size)
        file_list = []
        if format_file:
            file_download = "%s/%s" % (
                KNOWLEDGE_FORMAT_DOWNLOAD_URL, format_file
            )
            file_info = core.FileList(
                format_file_size, format_file, file_download
            )
            file_list.append(file_info)

        else:
            file_list = None
            file_download = None

        compliance_names.append(core.Compliance_Download(name, file_download))

        if d["frequency_id"] in (2, 3):
            summary = "Repeats every %s - %s" % (
                d["repeats_every"], d["repeat_type"]
            )
        elif d["frequency_id"] == 4:
            summary = "To complete within %s - %s" % (
                d["duration"], d["duration_type"]
            )
        else:
            summary = None

        # compliance_names.append(name)
        compliance = core.Compliance(
            d["compliance_id"], d["statutory_provision"],
            compliance_task, d["compliance_description"],
            document_name, file_list,
            d["penal_consequences"], d["frequency_id"],
            date_list, d["repeats_type_id"],
            d["repeats_every"], d["duration_type_id"],
            d["duration"], bool(d["is_active"]),
            d["frequency"], summary, False
        )
        compalinaces.append(compliance)
    return [compliance_names, compalinaces]

def get_mapping_compliances(db, mapping_id):
    q = "select compliance_id from tbl_compliances where statutory_mapping_id = %s "
    rows = db.select_all(q, [mapping_id])
    compliance_ids = []
    for r in rows :
        compliance_ids.append(int(r[0]))
    return compliance_ids

def get_statutory_mappings(db, user_id, for_approve=False):
    q = "SELECT distinct t1.statutory_mapping_id, t1.country_id, " + \
        " (select country_name from tbl_countries " + \
        " where country_id = t1.country_id) " + \
        " country_name,  t1.domain_id, " + \
        " (select domain_name from tbl_domains " + \
        " where domain_id = t1.domain_id) domain_name, " + \
        " t1.industry_ids, t1.statutory_nature_id, " + \
        " (select statutory_nature_name from tbl_statutory_natures " + \
        " where statutory_nature_id = t1.statutory_nature_id) " + \
        " statutory_nature_name, t1.statutory_ids, t1.geography_ids, " + \
        " t1.approval_status, t1.is_active " + \
        " FROM tbl_statutory_mappings t1 " + \
        " INNER JOIN tbl_user_domains t5 " + \
        " ON t5.domain_id = t1.domain_id " + \
        " and t5.user_id = %s " + \
        " INNER JOIN tbl_user_countries t6 " + \
        " ON t6.country_id = t1.country_id " + \
        " and t6.user_id = %s "

    if for_approve is True:
        q = q + " WHERE t1.approval_status = 0 "

    q = q + " ORDER BY country_name, domain_name, statutory_nature_name"
    rows = db.select_all(q, [user_id, user_id])

    columns = [
        "statutory_mapping_id", "country_id",
        "country_name", "domain_id", "domain_name", "industry_ids",
        "statutory_nature_id", "statutory_nature_name",
        "statutory_ids", "geography_ids",
        "approval_status", "is_active"
    ]

    result = []
    if rows:
        result = convert_to_dict(rows, columns)
    return return_statutory_mappings(db, result)


def return_statutory_mappings(db, data, is_report=None):
    if bool(STATUTORY_PARENTS) is False:
        get_statutory_master(db)
    if bool(GEOGRAPHY_PARENTS) is False:
        get_geographies(db)

    mapping_data_list = {}
    for d in data:
        mapping_id = int(d["statutory_mapping_id"])
        industry_names = ""
        compliance_ids = get_mapping_compliances(db, mapping_id)

        if len(compliance_ids) == 1:
            compliance_ids = compliance_ids[0]
        # compliance_id = int(d["compliance_id"])

        compliances_data = get_compliance_by_id(
            db, compliance_ids, is_report
        )
        compliance_names = compliances_data[0]
        compliances = compliances_data[1]
        geography_ids = [
            int(x) for x in d["geography_ids"].split(',') if x != ''
        ]
        geography_mapping_list = []
        for g_id in geography_ids:
            map_data = GEOGRAPHY_PARENTS.get(int(g_id))
            if map_data is not None:
                map_data = map_data[0]
                geography_mapping_list.append(map_data)
        statutory_ids = [
            int(x) for x in d["statutory_ids"][:-1].split(',')
        ]
        statutory_mapping_list = []
        for s_id in statutory_ids:
            s_map_data = STATUTORY_PARENTS.get(int(s_id))
            if s_map_data is not None:
                s_map_data = s_map_data[1]
            else :
                get_statutory_master(db)
                s_map_data = STATUTORY_PARENTS.get(int(s_id))
                if s_map_data is not None :
                    s_map_data = s_map_data[1]
                else :
                    s_map_data = ""
            statutory_mapping_list.append(
                s_map_data
            )
        industry_ids = [
            int(x) for x in d["industry_ids"][:-1].split(',')
        ]
        if len(industry_ids) == 1:
            industry_names = get_industry_by_id(db, industry_ids[0])
        else:
            industry_names = get_industry_by_id(db, industry_ids)

        approval = int(d["approval_status"])
        if approval in [0, 1, 2, 3]:
            approval_status_text = APPROVAL_STATUS[approval]
        else:
            approval_status_text = "Invalid"

        statutory = core.StatutoryMapping(
            d["country_id"], d["country_name"],
            d["domain_id"], d["domain_name"],
            industry_ids, industry_names,
            d["statutory_nature_id"], d["statutory_nature_name"],
            statutory_ids, statutory_mapping_list,
            compliances, compliance_names, geography_ids,
            geography_mapping_list, int(d["approval_status"]),
            bool(d["is_active"]), approval_status_text
        )
        mapping_data_list[mapping_id] = statutory
    return mapping_data_list


def check_duplicate_statutory_mapping(db, data, statutory_mapping_id=None):
    country_id = data.country_id
    domain_id = data.domain_id
    statutory_nature = data.statutory_nature_id
    industry_id = data.industry_ids
    statutory_id = data.statutory_ids
    industry_condition = db.generate_tuple_condition(
        "t3.industry_id", industry_id)
    statutory_condition = db.generate_tuple_condition(
        "t2.statutory_id", statutory_id)

    q = "SELECT distinct t1.statutory_mapping_id " + \
        " from tbl_statutory_mappings t1 " + \
        " inner join tbl_statutory_statutories t2 on " + \
        " t1.statutory_mapping_id = t2.statutory_mapping_id " + \
        " inner join tbl_statutory_industry t3 on " + \
        " t1.statutory_mapping_id = t3.statutory_mapping_id " +\
        " WHERE t1.country_id = %s AND t1.domain_id = %s AND " + \
        " t1.statutory_nature_id = %s AND %s AND %s "
    val = [
            country_id,
            domain_id,
            statutory_nature,
            statutory_condition,
            industry_condition,
        ]
    if statutory_mapping_id is not None:
        q = q + " AND t1.statutory_mapping_id != %s"
        val.append(statutory_mapping_id)
    row = db.select_one(q, val)
    result = None
    if row:
        result = row[0]
    return result


def check_duplicate_compliance_name(db, request_frame):
    compliances = request_frame.compliances
    country_id = request_frame.country_id
    domain_id = request_frame.domain_id
    mapping = request_frame.mappings
    compliance_names = []
    for m in mapping:
        statutory_mappings = m
        for c in compliances:
            compliance_name = c.compliance_task
            compliance_id = c.compliance_id
            statutory_provision = c.statutory_provision
            q = "SELECT count(t1.compliance_task) compliance_cnt" + \
                " FROM tbl_compliances t1 INNER JOIN " + \
                " tbl_statutory_mappings t2 on " + \
                " t1.statutory_mapping_id = t2.statutory_mapping_id " + \
                " WHERE t2.country_id = %s AND t2.domain_id = %s AND " + \
                " t1.compliance_task = %s " + \
                " AND t1.statutory_provision = %s " + \
                " AND t2.statutory_mapping LIKE %s"
            val = [
                country_id, domain_id, compliance_name,
                statutory_provision,
                str("[\"" + statutory_mappings + "\"]")
            ]
            if compliance_id is not None:
                q = q + " AND t1.compliance_id != %s"
                val.append(compliance_id)
                row = db.select_one(q, val)
            else:
                row = db.select_one(q, val)
            if row["compliance_cnt"] > 0:
                compliance_names.append(compliance_name)
    if len(compliance_names) > 0:
        return ", ".join(list(set(compliance_names)))
    else:
        return False

def get_country_domain_name(db, country_id, domain_id):
    rows = db.call_proc_with_multiresult_set("sp_get_country_domain_name", [country_id, domain_id], 2)
    c_name = rows[0][0].get("country_name")
    d_name = rows[1][0].get("domain_name")
    return c_name, d_name

def save_statutory_mapping(db, data, created_by):
    # Yet to submit : 0, Pending: 1, Approved: 2, Approve and Notify: 3, Reject: 4
    # tr_type 1: save, 2: submit
    country_id = data.country_id
    domain_id = data.domain_id
    c_name, d_name = get_country_domain_name(db, country_id, domain_id)
    nature_id = data.statutory_nature_id
    compliances = data.compliances
    statutory_mapping = json.dumps(data.mappings)
    created_on = get_date_time()
    is_active = 1
    if data.tr_type == 0 :
        is_approve = 0
    else:
        is_approve = 1
    mapping_value = [
        int(country_id), int(domain_id),
        int(nature_id), int(is_active), is_approve,
        int(created_by), str(created_on), statutory_mapping
    ]
    q = "INSERT INTO tbl_statutory_mappings (country_id, domain_id, " + \
        " statutory_nature_id, is_active, is_approved, created_by, created_on, statutory_mapping) values " + \
        " (%s, %s, %s, %s, %s, %s, %s, %s)"
    statutory_mapping_id = db.execute_insert(
        q, mapping_value
    )
    if statutory_mapping_id is False:
        raise process_error("E018")
    else:

        ids, names = save_compliance(
            db,
            statutory_mapping_id, domain_id, country_id, is_approve,
            compliances, created_by
        )

        save_statutory_industry(
            db, statutory_mapping_id, data.industry_ids, created_by, True
        )
        save_statutory_geography_id(
            db, statutory_mapping_id, data.geography_ids, created_by, True
        )
        save_statutory_statutories_id(
            db, statutory_mapping_id, data.statutory_ids, created_by, True
        )

        text = "New statutory mapping has been created %s - %s - %s for the following compliances %s" % (
                c_name, d_name, str(",".join(data.mappings)), names
            )

        link = "/knowledge/approve-statutory-mapping"
        save_messages(db, 3, "Statutory Mapping", text, link, created_by)

        action = "New statutory mappings added"
        db.save_activity(created_by, frmStatutoryMapping, action)
        return True


def save_compliance(
    db, mapping_id, domain_id, country_id, is_approve, datas, created_by
):
    compliance_ids = []
    compliance_names = []
    file_path = KNOWLEDGE_FORMAT_PATH
    for data in datas:

        created_on = get_date_time()

        provision = data.statutory_provision
        compliance_task = data.compliance_task
        compliance_description = data.description
        document_name = data.document_name
        file_list = data.format_file_list
        file_name = ""
        file_size = 0
        if file_list == []:
            file_list = None

        if file_list is not None:
            file_list = file_list[0]
            file_name = file_list.file_name
            file_size = file_list.file_size

        if data.is_file_removed and file_name:
            # remove uploaded file
            remove_uploaded_file(file_path + "/" + file_name)
            file_name = ""
            file_size = 0

        penal_consequences = data.penal_consequences
        compliance_frequency = data.frequency_id
        statutory_dates = []
        for s_d in data.statutory_dates:
            statutory_dates.append(s_d.to_structure())
        statutory_dates = json.dumps(statutory_dates)
        repeats_every = data.repeats_every
        repeats_type = data.repeats_type_id
        duration = data.duration
        duration_type = data.duration_type_id
        is_active = int(data.is_active)
        reference = data.reference

        table_name = "tbl_compliances"
        columns = [
            "statutory_provision",
            "compliance_task", "compliance_description",
            "document_name", "format_file", "format_file_size",
            "penal_consequences", "reference_link", "frequency_id",
            "statutory_dates", "statutory_mapping_id",
            "is_active", "created_by", "created_on",
            "domain_id", "country_id", "is_approved"

        ]
        values = [
            provision, compliance_task,
            compliance_description, document_name,
            file_name, file_size, penal_consequences, reference,
            compliance_frequency, statutory_dates,
            mapping_id, is_active, created_by, created_on,
            domain_id, country_id, is_approve
        ]
        if compliance_frequency == 1:
            # values.extend([0, 0, 0, 0])
            pass

        elif compliance_frequency == 5:
            if duration is not None and duration_type is not None:
                columns.extend(["duration", "duration_type_id"])
                values.extend([duration, duration_type])
        else:
            if repeats_every is not None and repeats_type is not None :
                columns.extend(["repeats_every", "repeats_type_id"])
                values.extend([repeats_every, repeats_type])

        compliance_id = db.insert(table_name, columns, values)
        if compliance_id is False:
            raise process_error("E019")

        compliance_ids.append(compliance_id)
        if document_name == "None":
            document_name = None
        if document_name:
            compliance_names.append(
                document_name + "-" + compliance_task
            )
        else:
            compliance_names.append(compliance_task)

    return compliance_ids, compliance_names


def save_statutory_industry(
    db, mapping_id, industry_ids, updated_by, is_new
):
    columns = ["statutory_mapping_id", "organisation_id", "assigned_by"]

    if is_new is False:
        db.delete(
            tblStatutoryIndustry, "statutory_mapping_id = %s", [mapping_id]
        )

    for i_id in industry_ids:
        values = [mapping_id, i_id, updated_by]
        db.insert(tblStatutoryIndustry, columns, values)


def save_statutory_geography_id(
    db, mapping_id, geography_ids, updated_by, is_new
):
    columns = ["statutory_mapping_id", "geography_id", "assigned_by"]

    if is_new is False:
        db.delete(
            tblStatutoryGeographies, "statutory_mapping_id = %s", [mapping_id]
        )

    for g_id in geography_ids:
        values = [mapping_id, g_id, updated_by]
        db.insert(tblStatutoryGeographies, columns, values)


def save_statutory_statutories_id(
    db, mapping_id, statutory_ids, updated_by, is_new
):
    columns = ["statutory_mapping_id", "statutory_id", "assigned_by"]

    if is_new is False:
        db.delete(
            tblStatutoryStatutories, "statutory_mapping_id = %s", [mapping_id]
        )

    for s_id in statutory_ids:
        values = [mapping_id, s_id, updated_by]
        db.insert(tblStatutoryStatutories, columns, values)


def save_notifications(
    db, message_heading, notification_text, link,
    domain_id, country_id, current_user, user_id, user_cat_id
):
    # internal notification

    notification_id = db.insert(
        "tbl_messages", ["user_category_id", "message_heading", "message_text", "link"],
        [user_cat_id, message_heading, notification_text, link]
    )
    if notification_id is False:
        return
    save_notifications_status(
        db, notification_id, domain_id, country_id, current_user, user_id
    )


def save_notifications_status(
    db, notification_id, domain_id=None, country_id=None,
    current_user=None,
    user_id=None
):
    user_ids = []
    q = "INSERT INTO tbl_messages " + \
        " (message_id, user_id, read_status) VALUES " + \
        " (%s, %s, 0) "

    query = "SELECT t1.user_id FROM tbl_users t1 INNER JOIN " + \
        "tbl_user_group_forms t2 ON t1.user_group_id = t2.user_group_id " + \
        "INNER JOIN tbl_user_domains as t3 ON t1.user_id = t3.user_id " + \
        "INNER JOIN tbl_user_countries as t4 ON t1.user_id = t4.user_id " + \
        "WHERE t1.is_active = 1 AND t1.is_disable = 0 AND t2.form_id = %s " + \
        " AND t3.domain_id = %s AND t4.country_id = %s"

    # query = "SELECT distinct user_id from tbl_users WHERE " + \
    #     " user_group_id in " + \
    #     "(select user_group_id from tbl_user_groups " + \
    #     " where form_ids like %s) AND " + \
    #     " user_id in (select user_id from " + \
    #     " tbl_user_domains where domain_id = %s )" + \
    #     " AND user_id in (select distinct user_id from " + \
    #     " tbl_user_countries where country_id = %s)"
    rows = db.select_all(query, [
        str('%11,%'),
        domain_id,
        country_id
    ])
    if rows:
        for r in rows:
            notify_user_id = r[0]
            if current_user == notify_user_id:
                continue
            user_ids.append(notify_user_id)
            db.execute(q, [notification_id, notify_user_id])
    if user_id is not None and user_id != current_user:
        if user_ids:
            if user_id not in user_ids:
                db.execute(q, [notification_id, user_id])
        else:
            db.execute(q, [notification_id, user_id])


#
# update statutory-mapping
#
def get_statutory_mapping_by_id(db, mapping_id):
    q = "SELECT t1.country_id, t2.country_name, " + \
        " t1.domain_id, t3.domain_name,  " + \
        " t1.statutory_nature_id, t4.statutory_nature_name, " + \
        " t1.is_approved, t1.statutory_mapping " + \
        " FROM tbl_statutory_mappings t1 " + \
        " INNER JOIN tbl_countries t2 " + \
        " on t1.country_id = t2.country_id " + \
        " INNER JOIN tbl_domains t3 " + \
        " on t1.domain_id = t3.domain_id " + \
        " INNER JOIN tbl_statutory_natures t4 " + \
        " on t1.statutory_nature_id = t4.statutory_nature_id " + \
        " WHERE t1.statutory_mapping_id=%s"
    rows = db.select_one(q, [mapping_id])
    # columns = [
    #     "country_id", "country_name", "domain_id",
    #     "domain_name", "industry_ids", "statutory_nature_id",
    #     "statutory_nature_name", "statutory_ids",
    #     "compliance_ids", "geography_ids",
    #     "approval_status", "statutory_mapping"
    # ]
    # result = {}
    # if rows:
    #     result = convert_to_dict(rows, columns)
    return rows


def update_statutory_mapping(db, data, updated_by):
    statutory_mapping_id = data.mapping_id
    is_exists = get_statutory_mapping_by_id(db, statutory_mapping_id)
    if bool(is_exists) is False:
        raise process_error("E020")
    domain_id = data.domain_id
    country_id = int(is_exists["country_id"])
    c_name, d_name = get_country_domain_name(db, country_id, domain_id)

    # industry_ids = ','.join(str(x) for x in data.industry_ids) + ","
    nature_id = data.statutory_nature_id
    # statutory_ids = ','.join(str(x) for x in data.statutory_ids) + ","
    compliances = data.compliances
    # geography_ids = ','.join(str(x) for x in data.geography_ids) + ","
    statutory_mapping = json.dumps(data.mappings)
    print type(statutory_mapping)
    if data.tr_type == 0:
        is_approve = 0
    else:
        is_approve = 1

    # save_statutory_backup(db, statutory_mapping_id, updated_by)
    table_name = "tbl_statutory_mappings"
    columns = (
        "country_id", "domain_id", "statutory_nature_id",
        "updated_by", "updated_on",
        "statutory_mapping", "is_approved"
    )
    values = (
        country_id, domain_id, nature_id,
        int(updated_by), get_date_time(), statutory_mapping, is_approve, statutory_mapping_id
    )
    where_condition = " statutory_mapping_id= %s "

    db.update(table_name, columns, values, where_condition)
    # self.update_statutory_mapping_id(
    #     data.statutory_ids, statutory_mapping_id, updated_by
    # )
    ids, names = update_compliance(
        db, statutory_mapping_id, country_id, domain_id, compliances, updated_by,
        is_approve
    )
    save_statutory_industry(
        db, statutory_mapping_id, data.industry_ids, updated_by, False
    )
    save_statutory_geography_id(
        db, statutory_mapping_id, data.geography_ids, updated_by, False
    )
    save_statutory_statutories_id(
        db, statutory_mapping_id, data.statutory_ids, updated_by, False
    )

    text = " %s - %s - %s statutory mappings has been edited for following compliances %s" % (c_name, d_name, str(", ".join(data.mappings)), str(", ".join(names)))
    db.save_activity(updated_by, frmStatutoryMapping, text)

    link = "/knowledge/approve-statutory-mapping"
    save_messages(db, 3, "Statutory Mapping", text, link, updated_by)
    return True


def update_only_compliance(db, data, updated_by):
    statutory_mapping_id = data.mapping_id
    is_exists = get_statutory_mapping_by_id(db, statutory_mapping_id)
    if bool(is_exists) is False:
        raise process_error("E020")
    domain_id = data.domain_id
    country_id = int(is_exists["country_id"])
    c_name, d_name = get_country_domain_name(db, country_id, domain_id)

    compliances = data.compliances
    statutory_mapping = json.dumps(data.mappings)
    if data.tr_type == 0:
        is_approve = 0
    else:
        is_approve = 1

    ids, names = update_compliance(
        db, statutory_mapping_id, country_id, domain_id, compliances, updated_by,
        is_approve
    )
    names = json.dumps(names)
    text = " %s - %s - %s statutory mappings has been edited for following compliances %s" % (c_name, d_name, str(statutory_mapping), names)
    db.save_activity(updated_by, frmStatutoryMapping, text)

    link = "/knowledge/approve-statutory-mapping"
    save_messages(db, 3, "Statutory Mapping", text, link, updated_by)

    return True


def get_saved_format_file(db, compliance_id):
    query = "SELECT format_file, format_file_size " + \
        " FROM tbl_compliances WHERE compliance_id = %s "
    rows = db.select_one(query, [compliance_id])
    result = convert_to_dict(rows, ["format_file", "format_file_size"])
    if result:
        return (result["format_file"], result["format_file_size"])
    else:
        return None


def remove_uploaded_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)


def update_compliance(db, mapping_id, country_id, domain_id, datas, updated_by, is_approve):
    compliance_ids = []
    compliance_names = []
    file_path = KNOWLEDGE_FORMAT_PATH
    for data in datas:
        compliance_id = data.compliance_id

        if (compliance_id is None):
            ids, names = save_compliance(
                db, mapping_id, domain_id, country_id, is_approve, [data], updated_by
            )
            compliance_ids.extend(ids)
            continue
        else:
            pass
            # saved_file = get_saved_format_file(db, compliance_id)
        provision = data.statutory_provision
        compliance_task = data.compliance_task
        description = data.description
        document_name = data.document_name

        file_list = data.format_file_list
        file_name = ""
        file_size = 0
        if file_list == []:
            file_list = None

        if file_list is not None:
            file_list = file_list[0]
            file_name = file_list.file_name
            file_size = file_list.file_size

        if data.is_file_removed and file_name :
            # remove uploaded file
            remove_uploaded_file(file_path + "/" + file_name)
            file_name = ""
            file_size = 0

        penal_consequences = data.penal_consequences
        compliance_frequency = data.frequency_id
        statutory_dates = []
        for s_d in data.statutory_dates:
            statutory_dates.append(s_d.to_structure())

        statutory_dates = json.dumps(statutory_dates)
        repeats_every = data.repeats_every
        repeats_type = data.repeats_type_id
        duration = data.duration
        duration_type = data.duration_type_id
        is_active = int(data.is_active)
        reference = data.reference
        table_name = "tbl_compliances"
        columns = [
            "statutory_provision", "compliance_task",
            "compliance_description", "document_name",
            "format_file", "format_file_size", "penal_consequences",
            "reference_link", "frequency_id", "statutory_dates",
            "statutory_mapping_id", "is_active",
            "updated_by", "domain_id", "country_id", "is_approved",
            "duration", "duration_type_id", "repeats_every", "repeats_type_id"
        ]
        values = [
            provision, compliance_task, description,
            document_name, file_name, file_size,
            penal_consequences, reference, compliance_frequency,
            statutory_dates, mapping_id, is_active,
            updated_by, domain_id, country_id, is_approve
        ]
        if compliance_frequency == 1:
            values.extend([0, 0, 0, 0])

        elif compliance_frequency == 5:
            values.extend([duration, duration_type, 0, 0])

        else:
            values.extend([0, 0, repeats_every, repeats_type])

        where_condition = "compliance_id = %s"
        values.append(compliance_id)
        if (db.update(table_name, columns, values, where_condition)):
            compliance_ids.append(compliance_id)
            cname = compliance_task
            if document_name is not None :
                cname = document_name + " - " + compliance_task
            compliance_names.append(cname)
        else:
            raise process_error("E021")
    return compliance_ids, compliance_names


def save_statutory_backup(db, statutory_mapping_id, created_by):
    old_record = get_statutory_mapping_by_id(db, statutory_mapping_id)
    # backup_id = self.get_new_id(
    #     "statutory_backup_id", "tbl_statutories_backup"
    # )
    created_on = get_date_time()
    industry_ids = [
        int(x) for x in old_record["industry_ids"][:-1].split(',')
    ]

    if len(industry_ids) == 1:
        industry_name = get_industry_by_id(db, industry_ids[0])
    else:
        industry_name = get_industry_by_id(db, industry_ids)

    provision = []
    # for sid in old_record["statutory_ids"][:-1].split(','):
    #     data = self.statutory_parent_mapping.get(int(sid))
    #     provision.append(data[1])
    for sid in old_record["statutory_ids"][:-1].split(','):
        data = get_statutory_by_id(db, sid)
        provision.append(data["parent_names"])
    mappings = ','.join(provision)

    geo_map = []
    for gid in [int(x) for x in old_record["geography_ids"].split(',') if x != '']:
        data = get_geography_by_id(db, gid)
        if type(data) is dict :
            data = data["parent_names"]
            geo_map.append(data)
    geo_mappings = ','.join(geo_map)

    tbl_statutory_backup = "tbl_statutories_backup"
    columns = [
        "statutory_mapping_id",
        "country_name", "domain_name", "industry_name",
        "statutory_nature", "statutory_provision",
        "applicable_location", "created_by",
        "created_on"
    ]
    values = [
        statutory_mapping_id,
        old_record["country_name"], old_record["domain_name"],
        industry_name, old_record["statutory_nature_name"],
        mappings,
        geo_mappings, int(created_by), created_on
    ]
    backup_id = db.insert(tbl_statutory_backup, columns, values)
    if backup_id is False:
        raise process_error("E022")

    qry = " INSERT INTO tbl_compliances_backup " + \
        " (statutory_backup_id, statutory_provision, " +\
        " compliance_task, compliance_description, " + \
        " document_name, format_file, " + \
        " penal_consequences, frequency_id, " + \
        " statutory_dates, repeats_every, " + \
        " repeats_type_id, duration, duration_type_id)  " + \
        " SELECT " + \
        " %s,t1.statutory_provision, t1.compliance_task, " + \
        " t1.compliance_description, t1.document_name, " + \
        " t1.format_file, t1.penal_consequences, " + \
        " t1.frequency_id, t1.statutory_dates, " + \
        " t1.repeats_every, t1.repeats_type_id, " + \
        " t1.duration, t1.duration_type_id " + \
        " FROM tbl_compliances t1 " + \
        " WHERE statutory_mapping_id=%s"
    db.execute(qry, [backup_id, statutory_mapping_id])


#
# update stautory mapping status
#
def change_compliance_status(db, mapping_id, is_active, updated_by):
    tbl_name = "tbl_compliances"
    columns = ["is_active", "updated_by", "is_approved"]
    values = [is_active, int(updated_by), 1]
    where = "statutory_mapping_id=%s"
    values.append(mapping_id)
    db.update(tbl_name, columns, values, where)


def change_statutory_mapping_status(db, data, updated_by):
    statutory_mapping_id = int(data.statutory_mapping_id)
    map_info = db.call_proc("sp_tbl_statutory_mappings_country_domain", [statutory_mapping_id])
    c_name = map_info[0].get("country_name")
    d_name = map_info[0].get("domain_name")
    mapping = map_info[0].get("statutory_mapping")

    # mapping = ", ".join(mapping)
    is_active = int(data.is_active)
    columns = ["is_active", "updated_by", "is_approved"]
    values = [is_active, int(updated_by), 1]
    where = "statutory_mapping_id=%s"
    values.append(statutory_mapping_id)
    db.update(tblStatutoryMappings, columns, values, where)
    change_compliance_status(db, statutory_mapping_id, is_active, updated_by)
    if is_active == 0:
        status = "deactivated"
    else:
        status = "activated"
    text = "%s - %s - %s statutory mapping has been %s" % (
            c_name, d_name, str(mapping), status
        )

    action = "Statutory Mapping has been %s" % status
    link = "/knowledge/approve-statutory-mapping"
    save_messages(db, 3, "Statutory Mapping", action, link, updated_by)

    db.save_activity(updated_by, 10, text)
    return True


def get_statutory_assigned_to_client(db, mapping_id):
    query = " SELECT distinct t1.unit_id, t1.client_id, " + \
            " (select business_group_id from tbl_units " + \
            " where unit_id = t1.unit_id) business_group_id, " + \
            " (select legal_entity_id from tbl_units " + \
            " where unit_id = t1.unit_id) legal_entity_id, " + \
            " (select division_id from tbl_units " + \
            " where unit_id = t1.unit_id) division_id " + \
            " from tbl_client_statutories t1 " + \
            " INNER JOIN tbl_client_compliances t2 " + \
            " ON t1.client_statutory_id = t2.client_statutory_id " + \
            " AND t2.compliance_id in " + \
            " (select c.compliance_id from " + \
            " tbl_compliances c where c.statutory_mapping_id = %s) "
    rows = db.select_all(query, [mapping_id])
    if rows:
        columns = [
            "unit_id", "client_id", "business_group_id",
            "legal_entity_id", "division_id"
        ]
        result = convert_to_dict(rows, columns)
        return result
    else:
        return None

# /////////////////////////////////
#  Knowledge transaction:
#    Statutory mapping
#       Save mapping
#       List mappings compliance wise
#       update data complianceid wise or mapping wise
#       Track and show which data updated in mapping while approve

def return_domains(data):
    result = []
    for d in data :
        result.append(
            knowledgetransaction.DomainInfo(
                d["domain_id"], d["country_id"],
                d["domain_name"], bool(d["is_active"])
            )
        )
    return result

def return_country(data):
    result = []
    for d in data:
        result.append(
            knowledgetransaction.CountryInfo(
                d["country_id"], d["country_name"], bool(d["is_active"])
            )
        )
    return result

def return_organisation(data):
    result = []
    for d in data :
        result.append(
            knowledgetransaction.OrganisationInfo(
                d["organisation_id"],
                d["country_id"], d["domain_id"],
                d["organisation_name"],
                bool(d["is_active"])
            )
        )
    return result

def return_statutory_nature(data):
    results = []
    for d in data:
        nature_id = d["statutory_nature_id"]
        nature_name = d["statutory_nature_name"]
        country_id = d["country_id"]
        is_active = bool(d["is_active"])
        results.append(
            knowledgetransaction.StatutoryNatureInfo(
                nature_id, nature_name, country_id,
                is_active
            )
        )
    return results

def return_stautory(data):
    result = []
    for d in data :
        p_ids = [int(x) for x in d["parent_ids"].split(',') if x != '']
        p_id = p_ids[-1:]
        if len(p_id) > 0:
            p_id = p_id[0]
        else :
            p_id = 0
            p_ids = None
        p_names = [y.strip() for y in d["parent_names"].split('>>') if y != '']
        if len(p_names) == 0:
            p_names = None

        result.append(
            knowledgetransaction.StatutoryInfo(
                d["statutory_id"], d["statutory_name"],
                d["level_id"], p_ids, p_id, p_names,
                d["country_id"], d["domain_id"],
                d["level_position"]
            )
        )
    return result

def return_geography(data):
    result = []
    for d in data :
        p_ids = [int(x) for x in d["parent_ids"].split(',') if x != '']
        p_id = p_ids[-1:]
        if len(p_id) > 0:
            p_id = p_id[0]
        p_names = [y.strip() for y in d["parent_names"].split('>>') if y != '']
        result.append(
            knowledgetransaction.GeographyInfo(
                d["geography_id"], d["geography_name"],
                d["level_id"], p_ids, p_id, p_names,
                bool(d["is_active"]), d["country_id"],
                d["level_position"]
            )
        )
    return result

def statutories_master(db, user_id):
    result = db.call_proc(
        'sp_tbl_statutory_masterdata', [user_id],
    )
    statutories = return_stautory(result)
    return knowledgetransaction.GetStatutoryMasterSuccess(statutories)

def statutory_mapping_master(db, user_id):
    result = db.call_proc_with_multiresult_set(
        'sp_tbl_statutory_mapping_masterdata', [user_id], 10
    )
    countries = return_country(result[0])
    domains = return_domains(result[1])
    organisation = return_organisation(result[2])
    statutory_nature = return_statutory_nature(result[3])
    geography = return_geography(result[4])
    geography_level = return_geography_levels(result[5])
    statutory_level = return_statutory_levels(result[6])
    frequency = return_compliance_frequency(result[7])
    repeats = return_compliance_repeat(result[8])
    duration = return_compliance_duration(result[9])
    approval_status = return_approval_status(APPROVAL_STATUS)

    return knowledgetransaction.GetStatutoryMappingsMasterSuccess(
        countries, domains, organisation, statutory_nature,
        statutory_level, geography_level,
        geography, frequency,
        repeats,
        approval_status, duration
    )

def statutory_mapping_list(db, user_id, approve_status, active_status, rcount, page_limit):

    def return_compliance(mapping_id, comp_info):
        compliances = []
        for c in comp_info:
            if c["statutory_mapping_id"] != mapping_id :
                continue

            dname = c["document_name"]
            cname = c["compliance_task"]
            if dname :
                cname = "%s - %s" % (dname, c["compliance_task"])

            compliances.append(
                core.MappedCompliance(
                    c["compliance_id"], cname, bool(c["c_is_active"]),
                    c["c_is_approved"],
                    core.getMappingApprovalStatus(c["c_is_approved"]),
                    c["remarks"]
                )
            )
        return compliances

    def return_organisation(mapping_id, org_info):
        orgs = [
            org["organisation_name"] for org in org_info
            if org["statutory_mapping_id"] == mapping_id
        ]
        return orgs

    def return_location(mapping_id, location_info):
        locations = [
            l["geography_name"] for l in location_info
            if l["statutory_mapping_id"] == mapping_id
        ]
        return locations

    def return_statutory(mapping_id, statutory_info):
        statutory = []

        for s in statutory_info :
            if s["statutory_mapping_id"] == mapping_id :
                if s["parent_names"] != '' and s["parent_names"] is not None:
                    statutory.append("%s >> %s" % (s["parent_names"], s["statutory_name"]))
                else :
                    statutory.append(s["statutory_name"])

        return statutory

    if active_status == 3 :
        active_status = "%"

    fromcount = rcount
    tocount = page_limit
    result = db.call_proc_with_multiresult_set(
        'sp_tbl_statutory_mapping_list',
        [user_id, approve_status, active_status, fromcount, tocount], 5
    )
    print [user_id, approve_status, fromcount, tocount]
    if len(result) == 0 :
        raise fetch_error()
    mapping = result[0]
    # compliance = result[1]
    organisation = result[1]
    statutory = result[2]
    location = result[3]
    total_record = result[4][0].get("total")
    print total_record
    data = []
    m_ids = []

    for m in mapping:
        map_id = m["statutory_mapping_id"]
        if map_id in m_ids :
            continue

        m_ids.append(map_id)
        mapped_compliance = return_compliance(map_id, mapping)
        if len(mapped_compliance) == 0 :
            continue

        data.append(core.StatutoryMapping(
            m["country_name"], m["domain_name"],
            return_organisation(map_id, organisation),
            m["nature"],
            return_statutory(map_id, statutory),
            mapped_compliance,
            return_location(map_id, location),
            m["is_approved"],
            bool(m["is_active"]),
            core.getMappingApprovalStatus(m["is_approved"]),
            map_id
        ))

    return data, total_record

def approve_statutory_mapping_list(db, user_id, request, from_count, to_count):
    i_id = request.industry_id
    s_n_id = request.nature_id
    c_id = request.country_id
    d_id = request.domain_id
    u_id = request.user_id
    args = [user_id, i_id, s_n_id, c_id, d_id, u_id, from_count, to_count]
    result = db.call_proc_with_multiresult_set("sp_tbl_statutory_mapping_approve_list_filter", args, 3)

    mappings = result[0]
    orgs = result[1]
    total_count = result[2][0].get("mapping_count")
    data = []

    def get_orgs(map_id):
        orgname = []
        for o in orgs :
            if o["statutory_mapping_id"] == map_id :
                orgname.append(o["organisation_name"])
        return orgname

    for m in mappings :
        map_id = m["statutory_mapping_id"]
        if (m["document_name"] is None or m["document_name"] == ''):
            c_name = m["compliance_task"]
        else :
            c_name = m["document_name"] + " - " + m["compliance_task"]
        orgname = get_orgs(map_id)
        c_on = datetime_to_string_time(m["created_on"])

        u_on = None
        if m["updated_by"] is not None :
            u_on = datetime_to_string_time(m["updated_on"])

        map_text = json.loads(m["statutory_mapping"])
        map_text = ", ".join(map_text)

        data.append(knowledgetransaction.MappingApproveInfo(
            map_id, m["compliance_id"],
            m["country_id"], m["domain_id"],
            c_name, bool(m["is_active"]), m["created_by"],
            c_on, m["updated_by"], u_on,
            m["statutory_nature_name"], sorted(orgname), map_text
        ))

    return data, total_count


def get_compliance_details(db, user_id, compliance_id):
    result = db.call_proc_with_multiresult_set("sp_tbl_statutory_mapping_compliance", [compliance_id], 2)
    c_info = result[0][0]
    geo_info = result[1]
    geo_names = []
    for g in geo_info:
        geo_names.append(g["parent_names"])

    if c_info["document_name"] is None or c_info["document_name"] == '':
        c_name = c_info["compliance_task"]
    else :
        c_name = c_info["document_name"] + " - " + c_info["compliance_task"]

    date_list = []

    statutory_dates = c_info["statutory_dates"]

    if statutory_dates is not None and statutory_dates != "":
        statutory_dates = json.loads(statutory_dates)

        for date in statutory_dates:
            s_date = core.StatutoryDate(
                date["statutory_date"],
                date["statutory_month"],
                date["trigger_before_days"],
                date.get("repeat_by")
            )
            date_list.append(s_date)
    summary, dates = make_summary(date_list, c_info["frequency_id"], c_info)
    if summary != "" and dates is not None and dates != "" :
        summary += ' on (%s)' % (dates)

    format_file = c_info["format_file"]
    if format_file:
        url = "%s/%s" % (
            KNOWLEDGE_FORMAT_DOWNLOAD_URL, format_file
        )
    else:
        url = None

    return (
        c_info["compliance_id"], c_info["statutory_provision"],
        c_name, c_info["compliance_description"],
        c_info["penal_consequences"], bool(c_info["is_active"]),
        c_info["freq_name"], summary, c_info["reference_link"],
        ", ".join(geo_names), url
    )

def save_approve_mapping(db, user_id, data):

    map_id = "None"
    try :
        for d in data :
            remarks = d.remarks
            if d.is_common :
                if map_id != d.mapping_id :
                    map_id = d.mapping_id
                    q = "update tbl_statutory_mappings set is_approved = %s, " + \
                        "remarks = %s where statutory_mapping_id = %s"
                    db.execute(q, [d.approval_status_id, remarks, d.mapping_id])

            q1 = "update tbl_compliances set is_approved = %s, " + \
                "approved_by = %s, approved_on = %s, remarks = %s where compliance_id = %s "

            if d.approval_status_id == 2 :
                text = "%s - %s - %s - %s has been approved"
                q1 = "update tbl_compliances set is_approved = %s, " + \
                    "approved_by = %s, approved_on = %s where compliance_id = %s "
                db.execute(q1, [d.approval_status_id, user_id, get_date_time(), d.compliance_id])

            elif d.approval_status_id == 3:
                text = "%s - %s - %s - %s has been approved & Notified With remarks " + d.remarks
                db.execute(q1, [d.approval_status_id, user_id, get_date_time(), remarks, d.compliance_id])
            else :
                text = "%s - %s - %s - %s has been rejected wih reason " + d.remarks
                db.execute(q1, [d.approval_status_id, user_id, get_date_time(), remarks, d.compliance_id])

            text = text % (
                d.country_name, d.domain_name, d.mapping_text, d.compliance_task
            )
            # updated notification

            save_messages(db, 4, "Statutory Mapping", text, d.compliance_id, user_id)

            if d.approval_status_id == 3 :
                save_approve_notify(db, text, user_id, d.compliance_id)

            db.save_activity(user_id, frmApproveStatutoryMapping, text)
        return True
    except Exception, e :
        print e
        raise fetch_error()

def save_messages(db, user_cat_id, message_head, message_text, link, created_by):

    msg_user_id = []
    if user_cat_id == 3 :
        # get reporting manager id to send executive actions
        q = "select t1.user_id from tbl_user_login_details as t1 " + \
            " inner join tbl_user_mapping as t2 on t2.parent_user_id = t1.user_id " + \
            " where t1.is_active = 1 and t2.child_user_id = %s"
    else :
        # get executive id
        q = "select t1.user_id from tbl_user_login_details as t1 " + \
            " inner join tbl_user_mapping as t2 on t2.child_user_id = t1.user_id " + \
            " where t1.is_active = 1 and t2.parent_user_id = %s "

    row = db.select_all(q, [created_by])

    for r in row :
        msg_user_id.append(r["user_id"])

    if msg_user_id is not None :
        db.save_toast_messages(user_cat_id, message_head, message_text, link, msg_user_id, created_by)

    q1 = "select user_id from tbl_user_login_details where is_active = 1 and user_category_id = 1"
    row1 = db.select_all(q1)
    c_admin = []
    for r in row1 :
        c_admin.append(r["user_id"])

    if len(c_admin) > 0 :
        db.save_toast_messages(1, message_head, message_text, link, c_admin, created_by)


def save_approve_notify(db, text, user_id, compliance_id):
    users = db.call_proc_with_multiresult_set("sp_tbl_users_to_notify", [compliance_id], 2)
    q = "insert into tbl_statutory_notifications (notification_text, compliance_id, created_by, created_on) " + \
        "values (%s, %s, %s, %s)"

    new_id = db.execute_insert(q, [text, compliance_id, user_id, get_date_time()])
    q1 = "insert into tbl_statutory_notifications_users (notification_id, user_id) " +  \
        "values (%s, %s)"
    for u in users:
        for u1 in u :
            db.execute(q1, [new_id, u1["user_id"]])

def get_statutory_mapping_edit(db, map_id, comp_id):
    if comp_id is None :
        comp_id = '%'
    print "comp_id>>>>>", map_id, comp_id
    result = db.call_proc_with_multiresult_set("sp_tbl_statutory_mapping_by_id", [map_id, comp_id, 0, 1000], 5)
    print "result>>>", result
    if len(result) == 0 :
        raise process_error("E087")

    comp_info = result[0]
    org_info = result[1]
    geo_info = result[2]
    statu_info = result[3]
    is_assigned = result[4][0]["is_assigned"]
    allow_edit = True
    if is_assigned > 0 :
        allow_edit = False
    org_list = []
    for org in org_info :
        org_list.append(org["organisation_id"])
    statu_list = []
    for statu in statu_info :
        statu_list.append(statu["statutory_id"])
    geo_list = []
    for geo in geo_info :
        geo_list.append(geo["geography_id"])

    compliance_list = []
    country_id = None
    domain_id = None
    nature_id = None
    mapping_id = None
    for c in comp_info :
        mapping_id = c["statutory_mapping_id"]
        country_id = c["country_id"]
        domain_id = c["domain_id"]
        nature_id = c["statutory_nature_id"]
        date_list = []
        statutory_dates = c["statutory_dates"]
        if statutory_dates is not None :
            statutory_dates = json.loads(statutory_dates)
            date_list = []
            for date in statutory_dates:
                s_date = core.StatutoryDate(
                    date["statutory_date"],
                    date["statutory_month"],
                    date["trigger_before_days"],
                    date.get("repeat_by")
                )
                date_list.append(s_date)
        else :
            date_list = None
        summary, dates = make_summary(date_list, c["frequency_id"], c)
        # if summary != "" and dates is not None or dates != "" :
        #     summary += ' on (%s)' % (dates)
        f_list = []
        if int(c["format_file_size"]) > 0 :
            f_list.append(core.FileList(
                int(c["format_file_size"]), c["format_file"], None
            ))
        is_file_removed = False
        compliance_list.append(knowledgetransaction.ComplianceList(
            c["compliance_id"], c["statutory_provision"],
            c["compliance_task"], c["document_name"],
            c["compliance_description"], c["penal_consequences"],
            bool(c["is_active"]),
            c["frequency_id"], date_list, c["repeats_type_id"],
            c["repeats_every"], c["duration_type_id"],
            c["duration"], c["format_file"], f_list,
            summary, c["reference_link"],  c["freq_name"], is_file_removed
        ))

    data = knowledgetransaction.GetComplianceEditSuccess(
        mapping_id, country_id, domain_id, nature_id,
        org_list, statu_list, compliance_list,
        geo_list, allow_edit
    )

    return data
