import os
import json
from server.database.tables import *
from protocol import (core)
from server.constants import (
    KNOWLEDGE_FORMAT_DOWNLOAD_URL, KNOWLEDGE_FORMAT_PATH
)
from server.common import (
    convert_to_dict, get_date_time
)
from server.database.knowledgemaster import (
    STATUTORY_PARENTS, GEOGRAPHY_PARENTS,
    get_geographies, get_statutory_master,
    get_statutory_by_id, get_geography_by_id,
    get_industry_by_id
)

APPROVAL_STATUS = ["Pending", "Approved", "Rejected", "Approved & Notified"]
def get_compliance_by_id(db, compliance_id, is_active=None):
    q = ""
    if is_active is None :
        if type(compliance_id) == int :
            q = " WHERE t1.compliance_id = %s"
            value = [compliance_id]
        else :
            q = " WHERE t1.compliance_id in %s"
            value = [tuple(compliance_id)]
    else :
        is_active = int(is_active)

        if type(compliance_id) == int :
            q = " WHERE t1.is_active = %s AND t1.compliance_id = %s"
            value = [is_active, compliance_id]
        else :
            q = " WHERE t1.is_active = %s AND t1.compliance_id in %s"
            value = [is_active, tuple(compliance_id)]

    qry = "SELECT t1.compliance_id, t1.statutory_provision, \
        t1.compliance_task, t1.compliance_description, \
        t1.document_name, t1.format_file, t1.format_file_size, \
        t1.penal_consequences, t1.frequency_id, \
        t1.statutory_dates, t1.repeats_every, \
        t1.repeats_type_id, \
        t1.duration, t1.duration_type_id, t1.is_active, \
        (select frequency from tbl_compliance_frequency where frequency_id = t1.frequency_id), \
        (select duration_type from tbl_compliance_duration_type where duration_type_id = t1.duration_type_id) duration_type,\
        (select repeat_type from tbl_compliance_repeat_type where repeat_type_id = t1.repeats_type_id) repeat_type \
        FROM tbl_compliances t1 %s ORDER BY t1.frequency_id" % q
    rows = db.select_all(qry, value)
    print rows
    print '*' * 50
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
    if rows :
        result = convert_to_dict(rows, columns)
    return return_compliance(result)

def return_compliance(data):
    compliance_names = []
    compalinaces = []
    for d in data :
        statutory_dates = d["statutory_dates"]
        statutory_dates = json.loads(statutory_dates)
        date_list = []
        for date in statutory_dates :
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
        if document_name :
            name = "%s - %s" % (
                document_name, compliance_task
            )
        else :
            name = compliance_task
        format_file = d["format_file"]
        format_file_size = d["format_file_size"]
        if format_file_size is not None :
            format_file_size = int(format_file_size)
        file_list = []
        if format_file :
            file_download = "%s/%s" % (
                KNOWLEDGE_FORMAT_DOWNLOAD_URL, format_file
            )
            file_info = core.FileList(
                format_file_size, format_file, file_download
            )
            file_list.append(file_info)

        else :
            file_list = None
            file_download = None

        compliance_names.append(core.Compliance_Download(name, file_download))

        if d["frequency_id"] in (2, 3) :
            summary = "Repeats every %s - %s" % (d["repeats_every"], d["repeat_type"])
        elif d["frequency_id"] == 4 :
            summary = "To complete within %s - %s" % (d["duration"], d["duration_type"])
        else :
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
            d["frequency"], summary
        )
        compalinaces.append(compliance)
    return [compliance_names, compalinaces]

def get_statutory_mappings(db, user_id, for_approve=False) :

    q = "SELECT distinct t1.statutory_mapping_id, t1.country_id, \
        (select country_name from tbl_countries where country_id = t1.country_id) country_name, \
        t1.domain_id, \
        (select domain_name from tbl_domains where domain_id = t1.domain_id) domain_name, \
        t1.industry_ids, t1.statutory_nature_id, \
        (select statutory_nature_name from tbl_statutory_natures where statutory_nature_id = t1.statutory_nature_id)\
        statutory_nature_name, \
        t1.statutory_ids, \
        t1.geography_ids, \
        t1.approval_status, t1.is_active,  \
        (select group_concat(distinct compliance_id) from tbl_compliances where statutory_mapping_id = t1.statutory_mapping_id) compliance_ids\
        FROM tbl_statutory_mappings t1 \
        INNER JOIN tbl_user_domains t5 \
        ON t5.domain_id = t1.domain_id \
        and t5.user_id = %s \
        INNER JOIN tbl_user_countries t6 \
        ON t6.country_id = t1.country_id \
        and t6.user_id = %s"

    if for_approve is True :
        q = q + " WHERE t1.approval_status in (0)"

    q = q + " ORDER BY country_name, domain_name, statutory_nature_name"
    rows = db.select_all(q, [user_id, user_id])
    # print q
    columns = [
        "statutory_mapping_id", "country_id",
        "country_name", "domain_id", "domain_name", "industry_ids",
        "statutory_nature_id", "statutory_nature_name",
        "statutory_ids", "geography_ids",
        "approval_status", "is_active", "compliance_ids"
    ]

    result = []
    if rows :
        result = convert_to_dict(rows, columns)
    return return_statutory_mappings(db, result)

def return_statutory_mappings(db, data, is_report=None):
    if bool(STATUTORY_PARENTS) is False :
        get_statutory_master(db)
    if bool(GEOGRAPHY_PARENTS) is False :
        get_geographies(db)

    mapping_data_list = {}
    for d in data :
        mapping_id = int(d["statutory_mapping_id"])
        industry_names = ""
        compliance_ids = [
            int(x) for x in d["compliance_ids"].split(',')
        ]
        if len(compliance_ids) == 1 :
            compliance_ids = compliance_ids[0]
        # compliance_id = int(d["compliance_id"])

        compliances_data = get_compliance_by_id(
            db, compliance_ids, is_report
        )
        compliance_names = compliances_data[0]
        compliances = compliances_data[1]
        geography_ids = [
            int(x) for x in d["geography_ids"][:-1].split(',')
        ]
        geography_mapping_list = []
        for g_id in geography_ids :
            map_data = GEOGRAPHY_PARENTS.get(int(g_id))
            if map_data is not None:
                map_data = map_data[0]
            geography_mapping_list.append(map_data)
        statutory_ids = [
            int(x) for x in d["statutory_ids"][:-1].split(',')
        ]
        statutory_mapping_list = []
        for s_id in statutory_ids :
            s_map_data = STATUTORY_PARENTS.get(int(s_id))
            # if s_map_data is not None :
            #     s_map_data = s_map_data[1]
            statutory_mapping_list.append(
                s_map_data[1]
            )
        industry_ids = [
            int(x) for x in d["industry_ids"][:-1].split(',')
        ]
        if len(industry_ids) == 1:
            industry_names = get_industry_by_id(db, industry_ids[0])
        else :
            industry_names = get_industry_by_id(db, industry_ids)

        approval = int(d["approval_status"])
        if approval in [0, 1, 2, 3] :
            approval_status_text = APPROVAL_STATUS[approval]
        else :
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

def check_duplicate_statutory_mapping(db, data, statutory_mapping_id=None) :
    country_id = data.country_id
    domain_id = data.domain_id
    statutory_nature = data.statutory_nature_id
    industry_id = data.industry_ids
    if len(industry_id) == 1  :
        industry_id = "(%s)" % (industry_id[0])
    else :
        industry_id = str(tuple(industry_id))
    statutory_id = data.statutory_ids
    if len(statutory_id) == 1 :
        statutory_id = "(%s)" % (statutory_id[0])
    else :
        statutory_id = str(tuple(statutory_id))

    q = "SELECT distinct t1.statutory_mapping_id from tbl_statutory_mappings t1 \
        inner join tbl_statutory_statutories t2 on \
        t1.statutory_mapping_id = t2.statutory_mapping_id \
        inner join tbl_statutory_industry t3 on \
        t1.statutory_mapping_id = t3.statutory_mapping_id \
        WHERE t1.country_id = %s AND t1.domain_id = %s AND \
        t1.statutory_nature_id = %s AND t2.statutory_id in %s AND \
        t3.industry_id in %s"
    val = [
            country_id,
            domain_id,
            statutory_nature,
            statutory_id,
            industry_id,
        ]
    if statutory_mapping_id is not None :
        q = q + " AND t1.statutory_mapping_id != %s"
        val.append(statutory_mapping_id)
        row = db.select_one(q, val)
    else :
        row = db.select_one(q, val)
    if row :
        return row[0]
    else :
        return None

def check_duplicate_compliance_name(db, request_frame):
    compliances = request_frame.compliances
    country_id = request_frame.country_id
    domain_id = request_frame.domain_id
    mapping = request_frame.mappings
    compliance_names = []
    for m in mapping :
        statutory_mappings = m
        for c in compliances :
            compliance_name = c.compliance_task
            compliance_id = c.compliance_id
            statutory_provision = c.statutory_provision
            q = "SELECT count(t1.compliance_task) FROM tbl_compliances t1 INNER JOIN \
                tbl_statutory_mappings t2 on t1.statutory_mapping_id = t2.statutory_mapping_id \
                WHERE t2.country_id = %s AND t2.domain_id = %s AND \
                t1.compliance_task = %s \
                AND t1.statutory_provision = %s \
                AND t2.statutory_mapping LIKE %s"
            val = [
                country_id, domain_id, compliance_name,
                statutory_provision,
                str("%" + statutory_mappings + "%")
            ]
            if compliance_id is not None :
                q = q + " AND t1.compliance_id != %s"
                val.append(compliance_id)
                row = db.select_one(q, val)
            else :
                row = db.select_one(q, val)
            if row[0] > 0 :
                compliance_names.append(compliance_name)
    if len(compliance_names) > 0 :
        return list(set(compliance_names))
    else :
        raise process_error("E017")

def save_statutory_mapping(db, data, created_by) :
    country_id = data.country_id
    domain_id = data.domain_id
    industry_ids = ','.join(str(x) for x in data.industry_ids) + ","
    nature_id = data.statutory_nature_id
    statutory_ids = ','.join(str(x) for x in data.statutory_ids) + ","
    compliances = data.compliances
    geography_ids = ','.join(str(x) for x in data.geography_ids) + ","
    statutory_mapping = '-'.join(data.mappings)

    # statutory_mapping_id = self.get_new_id(
    #     "statutory_mapping_id", "tbl_statutory_mappings"
    # )
    created_on = get_date_time()
    is_active = 1

    mapping_column = [
        "country_id", "domain_id",
        "industry_ids", "statutory_nature_id", "statutory_ids",
        "geography_ids", "is_active", "statutory_mapping", "created_by", "created_on"
    ]
    mapping_value = [
        int(country_id), int(domain_id),
        industry_ids, int(nature_id), statutory_ids,
        geography_ids, int(is_active),
        statutory_mapping, int(created_by), str(created_on)
    ]
    statutory_mapping_id = db.insert(tblStatutoryMappings, mapping_column, mapping_value)
    if statutory_mapping_id is False :
        raise process_error("E018")
    else :

        # if (self.save_data(statutory_table, field, data_save)) :
        # self.update_statutory_mapping_id(
        #     data.statutory_ids,
        #     statutory_mapping_id, created_by
        # )
        ids, names = save_compliance(
            db,
            statutory_mapping_id, domain_id,
            compliances, created_by
        )
        compliance_ids = ','.join(str(x) for x in ids) + ","
        # qry = "UPDATE tbl_statutory_mappings set compliance_ids='%s' \
        #     where statutory_mapping_id = %s"
        # db.execute(qry, [compliance_ids, statutory_mapping_id])
        db.update(
            tblStatutoryMappings, ["compliance_ids"],
            [compliance_ids, statutory_mapping_id],
            "statutory_mapping_id = %s",
        )
        save_statutory_industry(
            db, statutory_mapping_id, data.industry_ids, True
        )
        save_statutory_geography_id(
            db, statutory_mapping_id, data.geography_ids, True
        )
        save_statutory_statutories_id(
            db, statutory_mapping_id, data.statutory_ids, True
        )
        notification_log_text = "New statutory mapping has been created %s" % (statutory_mapping)
        link = "/knowledge/approve-statutory-mapping"
        save_notifications(
            db, notification_log_text, link,
            domain_id, country_id, created_by,
            user_id=None
        )
        action = "New statutory mappings added"
        db.save_activity(created_by, 10, action)
        return True

def save_compliance(db, mapping_id, domain_id, datas, created_by) :
    compliance_ids = []
    compliance_names = []
    is_format = False
    for data in datas :
        # compliance_id = self.get_new_id(
        #     "compliance_id", "tbl_compliances"
        # )
        created_on = get_date_time()

        provision = data.statutory_provision
        compliance_task = data.compliance_task
        compliance_description = data.description
        document_name = data.document_name
        file_list = data.format_file_list
        file_name = ""
        file_size = 0
        file_content = ""

        if file_list is not None :
            file_list = file_list[0]
            file_name = file_list.file_name
            # exten = file_list.file_name.split('.')[1]
            # auto_code = self.new_uuid()
            # file_name = "%s-%s.%s" % (name, auto_code, exten)
            file_size = file_list.file_size
            file_content = file_list.file_content
            is_format = True

        penal_consequences = data.penal_consequences
        compliance_frequency = data.frequency_id
        statutory_dates = []
        for s_d in data.statutory_dates :
            statutory_dates.append(s_d.to_structure())
        statutory_dates = json.dumps(statutory_dates)
        repeats_every = data.repeats_every
        repeats_type = data.repeats_type_id
        duration = data.duration
        duration_type = data.duration_type_id
        is_active = int(data.is_active)

        table_name = "tbl_compliances"
        columns = [
            "statutory_provision",
            "compliance_task", "compliance_description",
            "document_name", "format_file", "format_file_size",
            "penal_consequences", "frequency_id",
            "statutory_dates", "statutory_mapping_id",
            "is_active", "created_by", "created_on", "domain_id"
        ]
        values = [
            provision, compliance_task,
            compliance_description, document_name,
            file_name, file_size, penal_consequences,
            compliance_frequency, statutory_dates,
            mapping_id, is_active, created_by, created_on, domain_id
        ]
        if compliance_frequency == 1 :
            pass

        elif compliance_frequency == 4 :
            if duration is None :
                duration = ""
            if duration_type is None:
                duration_type = ""
            columns.extend(["duration", "duration_type_id"])
            values.extend([duration, duration_type])
        else :
            if repeats_every is None :
                repeats_every = ""
            if repeats_type is None :
                repeats_type = ""
            columns.extend(["repeats_every", "repeats_type_id"])
            values.extend([repeats_every, repeats_type])
        compliance_id = db.insert(table_name, columns, values)
        if compliance_id is False :
            raise process_error("E019")

        # if is_format :
        #     self.convert_base64_to_file(file_name, file_content)
        #     is_format = False
        compliance_ids.append(compliance_id)
        if document_name == "None":
            document_name = None
        if document_name :
            compliance_names.append(
                document_name + "-" + compliance_task
            )
        else :
            compliance_names.append(compliance_task)

    return compliance_ids, compliance_names

def save_statutory_industry(db, mapping_id, industry_ids, is_new) :
    columns = ["statutory_mapping_id", "industry_id"]

    if is_new is False :
        db.delete(tblStatutoryIndustry, "statutory_mapping_id = %s", [mapping_id])

    for i_id in industry_ids :
        values = [mapping_id, i_id]
        db.insert(tblStatutoryIndustry, columns, values)

def save_statutory_geography_id(db, mapping_id, geography_ids, is_new) :
    columns = ["statutory_mapping_id", "geography_id"]

    if is_new is False :
        db.delete(tblStatutoryGeographies, "statutory_mapping_id = %s", [mapping_id])

    for g_id in geography_ids :
        values = [mapping_id, g_id]
        db.insert(tblStatutoryGeographies, columns, values)

def save_statutory_statutories_id(
    db, mapping_id, statutory_ids, is_new
) :
    columns = ["statutory_mapping_id", "statutory_id"]

    if is_new is False :
        db.delete(tblStatutoryStatutories, "statutory_mapping_id = %s", [mapping_id])

    for s_id in statutory_ids :
        values = [mapping_id, s_id]
        db.insert(tblStatutoryStatutories, columns, values)

def save_notifications(
    db, notification_text, link,
    domain_id, country_id, current_user, user_id
):
    # internal notification

    notification_id = db.insert(tblNotifications, ["notification_text", "link"], [notification_text, link])
    if notification_id is False :
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
    q = "INSERT INTO tbl_notifications_status \
            (notification_id, user_id, read_status) VALUES \
            (%s, %s, 0)"

    query = "SELECT distinct user_id from tbl_users WHERE \
        user_group_id in \
        (select user_group_id from tbl_user_groups \
        where form_ids like '%s') AND \
        user_id in (select user_id from \
            tbl_user_domains where domain_id = %s \
        )  \
        AND user_id in (select distinct user_id from \
            tbl_user_countries where country_id = %s)"
    rows = db.select_all(query, [
        str('%11,%'),
        domain_id,
        country_id
    ])
    if rows :
        for r in rows :
            notify_user_id = r[0]
            if current_user == notify_user_id :
                continue
            user_ids.append(notify_user_id)
            db.execute(q, [notification_id, notify_user_id])
    if user_id is not None and user_id != current_user:
        if user_ids:
            if user_id not in user_ids:
                db.execute(q, [notification_id, user_id])
        else :
            db.execute(q, [notification_id, user_id])

#
# update statutory-mapping
#
def get_statutory_mapping_by_id(db, mapping_id) :
    q = "SELECT t1.country_id, t2.country_name, \
        t1.domain_id, t3.domain_name, t1.industry_ids, \
        t1.statutory_nature_id, t4.statutory_nature_name, \
        t1.statutory_ids, t1.compliance_ids, \
        t1.geography_ids, t1.approval_status, t1.statutory_mapping  \
        FROM tbl_statutory_mappings t1 \
        INNER JOIN tbl_countries t2 \
        on t1.country_id = t2.country_id \
        INNER JOIN tbl_domains t3 \
        on t1.domain_id = t3.domain_id \
        INNER JOIN tbl_statutory_natures t4 \
        on t1.statutory_nature_id = t4.statutory_nature_id \
        WHERE t1.statutory_mapping_id=%s"
    rows = db.select_one(q, [mapping_id])
    columns = [
        "country_id", "country_name", "domain_id",
        "domain_name", "industry_ids", "statutory_nature_id",
        "statutory_nature_name", "statutory_ids",
        "compliance_ids", "geography_ids",
        "approval_status", "statutory_mapping"
    ]
    result = {}
    if rows :
        result = convert_to_dict(rows, columns)
    return result


def update_statutory_mapping(db, data, updated_by) :
    statutory_mapping_id = data.statutory_mapping_id
    is_exists = get_statutory_mapping_by_id(db, statutory_mapping_id)
    if bool(is_exists) is False :
        raise process_error("E020")
    domain_id = data.domain_id
    country_id = int(is_exists["country_id"])
    industry_ids = ','.join(str(x) for x in data.industry_ids) + ","
    nature_id = data.statutory_nature_id
    statutory_ids = ','.join(str(x) for x in data.statutory_ids) + ","
    compliances = data.compliances
    geography_ids = ','.join(str(x) for x in data.geography_ids) + ","
    statutory_mapping = '-'.join(data.mappings)

    save_statutory_backup(db, statutory_mapping_id, updated_by)
    table_name = "tbl_statutory_mappings"
    columns = (
        "industry_ids", "statutory_nature_id", "statutory_ids",
        "geography_ids", "approval_status", "rejected_reason",
        "statutory_mapping",
        "updated_by"
    )
    values = (
        industry_ids, nature_id, statutory_ids, geography_ids,
        0, '', statutory_mapping, int(updated_by)
    )
    where_condition = " statutory_mapping_id= %s " % (statutory_mapping_id)

    db.update(table_name, columns, values, where_condition)
    # self.update_statutory_mapping_id(data.statutory_ids, statutory_mapping_id, updated_by)
    ids, names = update_compliance(db, statutory_mapping_id, domain_id, compliances, updated_by)
    compliance_ids = ','.join(str(x) for x in ids) + ","
    db.update(table_name, ["compliance_ids"], [compliance_ids], where_condition)
    save_statutory_industry(
        db, statutory_mapping_id, data.industry_ids, False
    )
    save_statutory_geography_id(
        db, statutory_mapping_id, data.geography_ids, False
    )
    save_statutory_statutories_id(
        db, statutory_mapping_id, data.statutory_ids, False
    )
    action = "Edit Statutory Mappings"
    db.save_activity(updated_by, 10, action)
    notification_log_text = "Stautory mapping has been updated %s" % (statutory_mapping)
    link = "/knowledge/approve-statutory-mapping"
    save_notifications(
        db, notification_log_text, link,
        domain_id, country_id, updated_by,
        user_id=None
    )
    return True

def get_saved_format_file(db, compliance_id):
    query = "SELECT format_file, format_file_size \
        FROM tbl_compliances WHERE compliance_id = %s "
    rows = db.select_one(query, [compliance_id])
    result = convert_to_dict(rows, ["format_file", "format_file_size"])
    if result :
        return (result["format_file"], result["format_file_size"])
    else :
        return None

def remove_uploaded_file(file_path):
    if os.path.exists(file_path) :
        os.remove(file_path)

def update_compliance(db, mapping_id, domain_id, datas, updated_by) :
    is_format = False
    compliance_ids = []
    compliance_names = []
    file_path = KNOWLEDGE_FORMAT_PATH
    for data in datas :
        compliance_id = data.compliance_id

        if (compliance_id is None) :
            ids, names = save_compliance(db, mapping_id, domain_id, [data], updated_by)
            compliance_ids.extend(ids)
            continue
        else :
            saved_file = get_saved_format_file(db, compliance_id)
        provision = data.statutory_provision
        compliance_task = data.compliance_task
        description = data.description
        document_name = data.document_name
        file_list = data.format_file_list
        file_name = ""
        file_size = 0
        file_content = ""
        saved_file_name = saved_file[0]

        if len(saved_file_name) == 0 :
            saved_file_name = None
        if file_list is None :
            if saved_file_name is not None :
                remove_uploaded_file(file_path + "/" + saved_file_name)
        else :
            if saved_file_name is None :
                file_list = file_list[0]
                file_name = file_list.file_name
                file_size = file_list.file_size
                file_content = file_list.file_content
                is_format = True
            else :
                file_list = file_list[0]
                file_name = file_list.file_name
                if len(file_name) == 0 :
                    file_name = None

                file_size = file_list.file_size
                file_content = file_list.file_content

        penal_consequences = data.penal_consequences
        compliance_frequency = data.frequency_id
        statutory_dates = []
        for s_d in data.statutory_dates :
            statutory_dates.append(s_d.to_structure())

        statutory_dates = json.dumps(statutory_dates)
        repeats_every = data.repeats_every
        repeats_type = data.repeats_type_id
        duration = data.duration
        duration_type = data.duration_type_id
        is_active = int(data.is_active)

        table_name = "tbl_compliances"
        columns = [
            "statutory_provision", "compliance_task",
            "compliance_description", "document_name",
            "format_file", "format_file_size", "penal_consequences",
            "frequency_id", "statutory_dates",
            "statutory_mapping_id", "is_active",
            "updated_by", "domain_id"
        ]
        values = [
            provision, compliance_task, description,
            document_name, file_name, file_size,
            penal_consequences, compliance_frequency,
            statutory_dates, mapping_id, is_active,
            updated_by, domain_id
        ]
        if compliance_frequency == 1 :
            pass

        elif compliance_frequency == 4 :
            columns.extend(["duration", "duration_type_id", "repeats_every", "repeats_type_id"])
            values.extend([duration, duration_type, 0, 0])

        else :
            columns.extend(["repeats_every", "repeats_type_id", "duration", "duration_type_id"])
            values.extend([repeats_every, repeats_type, 0, 0])

        where_condition = "compliance_id = %s" % (compliance_id)
        if (db.update(table_name, columns, values, where_condition)) :
            if is_format :
                convert_base64_to_file(file_name, file_content)
                is_format = False
            compliance_ids.append(compliance_id)
        else :
            raise process_error("E021")

    return compliance_ids, compliance_names

def save_statutory_backup(db, statutory_mapping_id, created_by):
    old_record = get_statutory_mapping_by_id(db, statutory_mapping_id)
    # backup_id = self.get_new_id("statutory_backup_id", "tbl_statutories_backup")
    created_on = get_date_time()
    industry_ids = [
        int(x) for x in old_record["industry_ids"][:-1].split(',')
    ]

    if len(industry_ids) == 1:
        industry_name = get_industry_by_id(db, industry_ids[0])
    else :
        industry_name = get_industry_by_id(db, industry_ids)

    provision = []
    # for sid in old_record["statutory_ids"][:-1].split(',') :
    #     data = self.statutory_parent_mapping.get(int(sid))
    #     provision.append(data[1])
    for sid in old_record["statutory_ids"][:-1].split(',') :
        data = get_statutory_by_id(db, sid)
        provision.append(data["parent_names"])
    mappings = ','.join(provision)

    geo_map = []
    for gid in old_record["geography_ids"][:-1].split(',') :
        data = get_geography_by_id(db, gid)
        if data is not None :
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
    if backup_id is False :
        raise process_error("E022")

    qry = " INSERT INTO tbl_compliances_backup \
        (statutory_backup_id, statutory_provision, \
        compliance_task, compliance_description, \
        document_name, format_file, \
        penal_consequences, frequency_id, \
        statutory_dates, repeats_every, \
        repeats_type_id, duration, duration_type_id)  \
        SELECT \
        %s,t1.statutory_provision, t1.compliance_task, \
        t1.compliance_description, t1.document_name, \
        t1.format_file, t1.penal_consequences, \
        t1.frequency_id, t1.statutory_dates, \
        t1.repeats_every, t1.repeats_type_id, \
        t1.duration, t1.duration_type_id \
        FROM tbl_compliances t1 \
        WHERE statutory_mapping_id=%s"
    db.execute(qry, [backup_id, statutory_mapping_id])

#
# update stautory mapping status
#
def change_compliance_status(db, mapping_id, is_active, updated_by) :
    tbl_name = "tbl_compliances"
    columns = ["is_active", "updated_by"]
    values = [is_active, int(updated_by)]
    where = "statutory_mapping_id=%s" % (mapping_id)
    db.update(tbl_name, columns, values, where)

def change_statutory_mapping_status(db, data, updated_by):
    statutory_mapping_id = int(data.statutory_mapping_id)
    is_active = int(data.is_active)
    columns = ["is_active", "updated_by"]
    values = [is_active, int(updated_by)]
    where = "statutory_mapping_id=%s" % (statutory_mapping_id)
    db.update(tblStatutoryMappings, columns, values, where)
    change_compliance_status(db, statutory_mapping_id, is_active, updated_by)
    if is_active == 0:
        status = "deactivated"
    else:
        status = "activated"
    action = "Statutory Mapping has been %s" % status
    db.save_activity(updated_by, 10, action)
    return True

def change_approval_status(db, data, updated_by) :
    statutory_mapping_id = int(data.statutory_mapping_id)
    provision = data.statutory_provision
    approval_status = int(data.approval_status)
    rejected_reason = data.rejected_reason
    notification_text = data.notification_text
    tbl_name = "tbl_statutory_mappings"
    columns = [
        "approval_status"
    ]
    values = [
        approval_status
    ]
    where = "statutory_mapping_id=%s" % (statutory_mapping_id)

    q = "SELECT statutory_mapping, created_by, updated_by, domain_id, \
        country_id, IFNULL(approval_status,0) from tbl_statutory_mappings \
        where statutory_mapping_id = %s"

    rows = db.select_one(q, [statutory_mapping_id])
    users = convert_to_dict(rows, [
        "statutory_mapping", "created_by", "updated_by",
        "domain_id", "country_id", "approval_status"
    ])
    if int(users["approval_status"]) > 0 :
        msg = """ Statutory mapping "%s" already approved or rejected. """ % (users["statutory_mapping"])
        return msg,  None
    if approval_status == 2 :
        # Rejected
        columns.extend(["rejected_reason"])
        values.extend([rejected_reason])
        notification_log_text = "Statutory Mapping: %s \
            has been Rejected and reason is %s" % (provision, rejected_reason)
    else :
        notification_log_text = "Statutory Mapping: %s \
            has been Approved" % (provision)

    db.update(tbl_name, columns, values, where)
    if approval_status == 3 :
        save_statutory_notifications(
            db, statutory_mapping_id, notification_text
        )
        notification_log_text = "Statutory Mapping: %s \
            has been Approved & Notified" % (provision)

    link = "/knowledge/statutory-mapping"
    if users["updated_by"] is None :
        user_id = int(users["created_by"])
    else :
        user_id = int(users["updated_by"])
    save_notifications(
        db, notification_log_text, link,
        users["domain_id"], users["country_id"], updated_by,
        user_id
    )
    db.save_activity(updated_by, 11, notification_log_text)
    return True

def get_statutory_assigned_to_client(db, mapping_id):
    query = "SELECT distinct t1.unit_id, t1.client_id, \
        (select business_group_id from tbl_units \
            where unit_id = t1.unit_id) business_group_id, \
        (select legal_entity_id from tbl_units \
            where unit_id = t1.unit_id) legal_entity_id,\
        (select division_id from tbl_units \
            where unit_id = t1.unit_id) division_id \
        from tbl_client_statutories t1 \
        INNER JOIN tbl_client_compliances t2 \
        ON t1.client_statutory_id = t2.client_statutory_id \
        AND t2.compliance_id in \
            (select c.compliance_id from \
            tbl_compliances c where c.statutory_mapping_id = %s) "
    rows = db.select_all(query, [mapping_id])

    if rows :
        columns = [
            "unit_id", "client_id", "business_group_id",
            "legal_entity_id", "division_id"
        ]
        result = convert_to_dict(rows, columns)
        return result
    else :
        return None


def save_statutory_notifications(db, mapping_id, notification_text):
    # client notification
    client_info = get_statutory_assigned_to_client(db, mapping_id)
    old_record = get_statutory_mapping_by_id(
        db, mapping_id
    )
    industry_ids = [
        (x) for x in old_record["industry_ids"][:-1].split(',')
    ]
    industry_ids = ','.join(industry_ids)
    mappings = old_record["statutory_mapping"]
    geo_map = []
    for gid in old_record["geography_ids"][:-1].split(',') :
        data = get_geography_by_id(db, int(gid))
        if data is not None :
            names = data["parent_names"]
            geo_map.append(names)
    geo_mappings = ','.join(str(x) for x in geo_map)

    # notification_id = self.get_new_id(
    #     "statutory_notification_id",
    #     "tbl_statutory_notifications_log"
    # )
    columns = [
        "statutory_mapping_id",
        "country_name", "domain_name", "industry_name",
        "statutory_nature", "statutory_provision",
        "applicable_location", "notification_text"
    ]
    values = [
        int(mapping_id),
        old_record["country_id"], old_record["domain_id"],
        industry_ids, old_record["statutory_nature_id"],
        mappings, geo_mappings, notification_text
    ]
    notification_id = db.insert(tblStatutoryNotificationsLog, columns, values)
    if notification_id is False :
        raise process_error("E023")
    save_statutory_notification_units(db, notification_id, mapping_id, client_info)

def save_statutory_notification_units(db, statutory_notification_id, mapping_id, client_info):

    if client_info is not None:
        for r in client_info :
            column = [
                "statutory_notification_id", "client_id",
                "legal_entity_id", "unit_id"
            ]
            # notification_unit_id = self.get_new_id(
            #     "statutory_notification_unit_id",
            #     "tbl_statutory_notifications_units"
            # )
            business_group = r["business_group_id"]
            division_id = r["division_id"]
            values = [
                statutory_notification_id,
                int(r["client_id"]), int(r["legal_entity_id"]),
                int(r["unit_id"])
            ]
            if business_group is not None :
                column.append("business_group_id")
                values.append(business_group)

            if division_id is not None :
                column.append("division_id")
                values.append(division_id)

            n_id = db.insert(tblStatutoryNotificationsUnits, column, values)
            if n_id is False :
                raise process_error("E023")
