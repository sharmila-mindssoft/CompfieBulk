import json
from protocol import (core, knowledgereport)
from server.common import (make_summary)
from server.constants import KNOWLEDGE_FORMAT_DOWNLOAD_URL


def get_geography_report(db):
    result = db.call_proc("sp_geographymaster_report_data", ())
    print "geography report"
    print result

    def return_report_data(result) :
        # mapping_dict = {}
        _list = []
        for item in result:
            geography_mapping = item["parent_names"]
            print "geo mapping"
            print geography_mapping
            is_active = bool(item["is_active"])
            country_id = item["country_id"]
            # _list = mapping_dict.get(country_id)

            _list.append(
                knowledgereport.GeographyMapping(
                    country_id, geography_mapping, is_active
                )
            )
            print _list
        return _list

    # print bool(GEOGRAPHY_PARENTS)

    # if bool(GEOGRAPHY_PARENTS) is False:
     # get_geographies(db)

    return return_report_data(result)


def get_statutory_mapping_report(
    db, country_id, domain_id, industry_id,
    statutory_nature_id, geography_id,
    level_1_statutory_id, frequency_id, user_id, from_count, to_count
):
    result = db.call_proc_with_multiresult_set(
        'sp_tbl_statutory_mappings_reportdata', [
            country_id, domain_id, industry_id, statutory_nature_id, geography_id,
            level_1_statutory_id, frequency_id, user_id, from_count, to_count
        ], 5
    )
    print [
            country_id, domain_id, industry_id, statutory_nature_id, geography_id,
            level_1_statutory_id, frequency_id, user_id, from_count, to_count
        ]
    rcount = result[1][0]["count"]
    records = result[2]
    industry = result[3]
    georecord = result[4]
    report_list = []
    for r in records:
        m_lst = json.loads(r["statutory_mapping"])
        statutory_provision = ", ".join(m_lst)
        # for m in m_lst :
        #     statutory_provision += ", ".join(m.split(">>")[1:])

        mapping = m_lst[0].split(">>")
        act_name = mapping[0].strip()

        statutory_provision += " >> " + r["statutory_provision"]
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
        i_names = []
        for i in industry :
            if i["statutory_mapping_id"] == r["statutory_mapping_id"] :
                i_names.append(i["organisation_name"])

        g_names = []
        for g in georecord :
            if g["statutory_mapping_id"] == r["statutory_mapping_id"]:
                g_names.append(g["parent_names"])

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
        summary, sum_dates = make_summary(date_list, r["frequency_id"], r)

        info = knowledgereport.StatutoryMappingReport(
            r["country_name"],
            r["domain_name"],
            i_names,
            r["statutory_nature_name"],
            g_names,
            r["is_approved"],
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
            url,
            summary
        )
        report_list.append(info)
    return report_list, rcount


# def return_knowledge_report(db, report_data, total_count=None):
#     if bool(GEOGRAPHY_PARENTS) is False:
#         get_geographies(db)

#     report_list = []
#     for r in records:
#         m_lst = json.loads(r["statutory_mapping"])
#         statutory_provision = ", ".join(m_lst)
#         # for m in m_lst :
#         #     statutory_provision += ", ".join(m.split(">>")[1:])

#         mapping = m_lst[0].split(">>")
#         act_name = mapping[0].strip()

#         statutory_provision = r["statutory_mapping"] + " " + r["statutory_provision"]
#         compliance_task = r["compliance_task"]
#         document_name = r["document_name"]
#         if document_name == "None":
#             document_name = None
#         if document_name:
#             name = "%s - %s" % (
#                 document_name, compliance_task
#             )
#         else:
#             name = compliance_task

#         format_file = r["format_file"]
#         format_file_size = r["format_file_size"]
#         if format_file_size is not None:
#             format_file_size = int(format_file_size)
#         if format_file:
#             url = "%s/%s" % (
#                 KNOWLEDGE_FORMAT_DOWNLOAD_URL, format_file
#             )
#         else:
#             url = None
#         # industry_ids = [
#         #     int(x) for x in r["industry_ids"][:-1].split(',')
#         # ]
#         # if len(industry_ids) == 1:
#         #     industry_names = get_industry_by_id(db, industry_ids[0])
#         # else:
#         #     industry_names = get_industry_by_id(db, industry_ids)

#         # geography_ids = [
#         #     int(x) for x in r["geography_ids"].split(',') if x != ''
#         # ]
#         # geography_mapping_list = []
#         # for g_id in geography_ids:
#         #     map_data = GEOGRAPHY_PARENTS.get(int(g_id))
#         #     if map_data is not None:
#         #         map_data = map_data[0]
#         #     geography_mapping_list.append(map_data)



#         statutory_dates = r["statutory_dates"]
#         statutory_dates = json.loads(statutory_dates)
#         date_list = []
#         for date in statutory_dates:
#             s_date = core.StatutoryDate(
#                 date["statutory_date"],
#                 date["statutory_month"],
#                 date["trigger_before_days"],
#                 date.get("repeat_by")
#             )
#             date_list.append(s_date)

#         info = knowledgereport.StatutoryMappingReport(
#             r["country_name"],
#             r["domain_name"],
#             industry_names,
#             r["statutory_nature_name"],
#             geography_mapping_list,
#             r["approval_status"],
#             bool(r["is_active"]),
#             act_name,
#             r["compliance_id"],
#             statutory_provision,
#             name,
#             r["compliance_description"],
#             r["penal_consequences"],
#             r["frequency_id"],
#             date_list,
#             r["repeats_type_id"],
#             r["repeats_every"],
#             r["duration_type_id"],
#             r["duration"],
#             url
#         )
#         report_list.append(info)
#     return report_list, total_count
