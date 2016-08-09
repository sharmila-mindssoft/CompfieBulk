import json
from protocol import (core, knowledgereport)
from server.common import (convert_to_dict)
from server.constants import KNOWLEDGE_FORMAT_DOWNLOAD_URL
from server.database.knowledgemaster import (
    GEOGRAPHY_PARENTS,
    get_geographies,
    get_industry_by_id
)


def get_geography_report(db):
    q = "SELECT t1.geography_id, t1.geography_name, " + \
        " t1.parent_names, t1.is_active, " + \
        " (select distinct country_id FROM tbl_geography_levels " + \
        " where level_id = t1.level_id) country_id, " + \
        " (select level_position FROM tbl_geography_levels " + \
        " where level_id = t1.level_id) position " + \
        " FROM tbl_geographies t1 " + \
        " ORDER BY position, parent_names, geography_name"
    rows = db.select_all(q)
    columns = [
        "geography_id", "geography_name", "parent_names",
        "is_active", "country_id", "position"
    ]
    result = convert_to_dict(rows, columns)

    def return_report_data(result):
        mapping_dict = {}
        for item in result:
            mappings = item["parent_names"]
            is_active = bool(item["is_active"])
            country_id = item["country_id"]
            _list = mapping_dict.get(country_id)
            if _list is None:
                _list = []

            _list.append(
                knowledgereport.GeographyMapping(
                    mappings, is_active
                )
            )
            mapping_dict[country_id] = _list

        return mapping_dict

    if bool(GEOGRAPHY_PARENTS) is False:
        get_geographies(db)

    return return_report_data(result)


def get_statutory_mapping_report(
    db, country_id, domain_id, industry_id,
    statutory_nature_id, geography_id,
    level_1_statutory_id, frequency_id, user_id, from_count, to_count
):
    qry_where = ""
    qry_val = []
    if industry_id is not None:
        qry_where += "AND t3.industry_id = %s "
        qry_val.append(industry_id)
    if geography_id is not None:
        qry_where += "AND t4.geography_id = %s "
        qry_val.append(geography_id)
    if statutory_nature_id is not None:
        qry_where += "AND t1.statutory_nature_id = %s "
        qry_val.append(statutory_nature_id)
    if level_1_statutory_id is not None:
        qry_where += " AND t1.statutory_mapping LIKE ( " + \
            " select group_concat(statutory_name, %s)" + \
            " from tbl_statutories where statutory_id = %s)"
        qry_val.append(str("%"))
        qry_val.append(level_1_statutory_id)
    if frequency_id is not None:
        qry_where += "AND t2.frequency_id = %s " % (frequency_id)
        qry_val.append(frequency_id)

    q_count = "SELECT  count(distinct t2.compliance_id) " + \
        " FROM tbl_statutory_mappings t1 " + \
        " INNER JOIN tbl_compliances t2 " + \
        " ON t2.statutory_mapping_id = t1.statutory_mapping_id " + \
        " INNER JOIN tbl_statutory_industry t3 " + \
        " ON t3.statutory_mapping_id = t1.statutory_mapping_id " + \
        " INNER JOIN tbl_statutory_geographies t4 " + \
        " ON t4.statutory_mapping_id = t1.statutory_mapping_id " + \
        " INNER JOIN tbl_user_domains t5 " + \
        " ON t5.domain_id = t1.domain_id " + \
        " and t5.user_id = %s " + \
        " INNER JOIN tbl_user_countries t6 " + \
        " ON t6.country_id = t1.country_id " + \
        " and t6.user_id = %s " + \
        " WHERE t1.approval_status in (1, 3) AND t2.is_active = 1 AND " + \
        " t1.country_id = %s " + \
        " and t1.domain_id = %s "
    order = " ORDER BY SUBSTRING_INDEX(SUBSTRING_INDEX( " + \
            " t1.statutory_mapping, '>>', 1), '>>', -1), " + \
            " t2.frequency_id "
    param_lst = [
        user_id, user_id,
        country_id, domain_id
    ]
    if qry_where is not "":
        q_count += qry_where
        param_lst.extend(qry_val)

    row = db.select_one(q_count + order, param_lst)

    if row:
        r_count = row[0]
    else:
        r_count = 0

    q = "SELECT distinct t1.statutory_mapping_id, t1.country_id," + \
        " (select country_name from tbl_countries " + \
        " where country_id = t1.country_id) " + \
        " country_name,  t1.domain_id, " + \
        " (select domain_name from tbl_domains " + \
        " where domain_id = t1.domain_id) domain_name, " + \
        " t1.industry_ids, t1.statutory_nature_id, " + \
        " (select statutory_nature_name from tbl_statutory_natures " + \
        " where statutory_nature_id = t1.statutory_nature_id) " + \
        " statutory_nature_name,  t1.statutory_ids, t1.geography_ids, " + \
        " t1.approval_status, t1.is_active, t1.statutory_mapping," + \
        " t2.compliance_id, t2.statutory_provision, " + \
        " t2.compliance_task, t2.compliance_description, " + \
        " t2.document_name, t2.format_file, t2.format_file_size, " + \
        " t2.penal_consequences, t2.frequency_id, " + \
        " t2.statutory_dates, t2.repeats_every, " + \
        " t2.repeats_type_id, t2.duration, t2.duration_type_id " + \
        " FROM tbl_statutory_mappings t1 " + \
        " INNER JOIN tbl_compliances t2 " + \
        " ON t2.statutory_mapping_id = t1.statutory_mapping_id " + \
        " INNER JOIN tbl_statutory_industry t3 " + \
        " ON t3.statutory_mapping_id = t1.statutory_mapping_id " + \
        " INNER JOIN tbl_statutory_geographies t4 " + \
        " ON t4.statutory_mapping_id = t1.statutory_mapping_id " + \
        " INNER JOIN tbl_user_domains t5 " + \
        " ON t5.domain_id = t1.domain_id " + \
        " and t5.user_id = %s " + \
        " INNER JOIN tbl_user_countries t6 " + \
        " ON t6.country_id = t1.country_id " + \
        " and t6.user_id = %s " + \
        " WHERE t1.approval_status in (1, 3) AND t2.is_active = 1 AND " + \
        " t1.country_id = %s " + \
        " and t1.domain_id = %s "

    order = " ORDER BY SUBSTRING_INDEX( " + \
        " SUBSTRING_INDEX(t1.statutory_mapping, '>>', 1), '>>', -1), " + \
        " t2.frequency_id " + \
        " limit %s, %s"
    param_lst = [
        user_id, user_id,
        country_id, domain_id
    ]

    if qry_where is not None:
        q += qry_where
        param_lst.extend(qry_val)

    param_lst.extend([from_count, to_count])
    rows = db.select_all(q + order, param_lst)
    columns = [
        "statutory_mapping_id", "country_id",
        "country_name", "domain_id", "domain_name", "industry_ids",
        "statutory_nature_id", "statutory_nature_name",
        "statutory_ids", "geography_ids",
        "approval_status", "is_active", "statutory_mapping",
        "compliance_id", "statutory_provision",
        "compliance_task", "compliance_description",
        "document_name", "format_file",
        "format_file_size", "penal_consequences",
        "frequency_id", "statutory_dates", "repeats_every",
        "repeats_type_id", "duration", "duration_type_id"
    ]
    report_data = []
    if rows:
        report_data = convert_to_dict(rows, columns)

    return return_knowledge_report(
        db, report_data, r_count
    )


def return_knowledge_report(db, report_data, total_count=None):
    if bool(GEOGRAPHY_PARENTS) is False:
        get_geographies(db)

    report_list = []
    for r in report_data:
        mapping = r["statutory_mapping"].split(">>")
        act_name = mapping[0].strip()
        statutory_provision = " >>".join(mapping[1:])
        statutory_provision += " " + r["statutory_provision"]
        compliance_task = r["compliance_task"]
        document_name = r["document_name"]
        if document_name == "None":
            document_name = None
        if document_name:
            name = "%s - %s" % (
                document_name, compliance_task
            )
        else:
            name = compliance_task

        format_file = r["format_file"]
        format_file_size = r["format_file_size"]
        if format_file_size is not None:
            format_file_size = int(format_file_size)
        if format_file:
            url = "%s/%s" % (
                KNOWLEDGE_FORMAT_DOWNLOAD_URL, format_file
            )
        else:
            url = None
        industry_ids = [
            int(x) for x in r["industry_ids"][:-1].split(',')
        ]
        if len(industry_ids) == 1:
            industry_names = get_industry_by_id(db, industry_ids[0])
        else:
            industry_names = get_industry_by_id(db, industry_ids)

        geography_ids = [
            int(x) for x in r["geography_ids"][:-1].split(',')
        ]
        geography_mapping_list = []
        for g_id in geography_ids:
            map_data = GEOGRAPHY_PARENTS.get(int(g_id))
            if map_data is not None:
                map_data = map_data[0]
            geography_mapping_list.append(map_data)

        statutory_dates = r["statutory_dates"]
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

        info = knowledgereport.StatutoryMappingReport(
            r["country_name"],
            r["domain_name"],
            industry_names,
            r["statutory_nature_name"],
            geography_mapping_list,
            r["approval_status"],
            bool(r["is_active"]),
            act_name,
            r["compliance_id"],
            statutory_provision,
            name,
            r["compliance_description"],
            r["penal_consequences"],
            r["frequency_id"],
            date_list,
            r["repeats_type_id"],
            r["repeats_every"],
            r["duration_type_id"],
            r["duration"],
            url
        )
        report_list.append(info)
    return report_list, total_count
