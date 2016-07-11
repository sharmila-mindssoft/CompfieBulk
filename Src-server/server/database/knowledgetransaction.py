
from server.database.tables import *
from protocol import (general, core)

from server.common import (
    convert_to_dict, datetime_to_string
)

__all__ = [
    "get_statutory_mappings"
]

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
        q = q + " WHERE t1.approval_status in (0, 2)"

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
    return return_statutory_mappings(result)

def return_statutory_mappings(data, is_report=None):
    if bool(self.statutory_parent_mapping) is False :
        self.get_statutory_master()
    if bool(self.geography_parent_mapping) is False :
        self.get_geographies()
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

        compliances_data = self.get_compliance_by_id(
            compliance_ids, is_report
        )
        compliance_names = compliances_data[0]
        compliances = compliances_data[1]
        geography_ids = [
            int(x) for x in d["geography_ids"][:-1].split(',')
        ]
        geography_mapping_list = []
        for g_id in geography_ids :
            map_data = self.geography_parent_mapping.get(int(g_id))
            if map_data is not None:
                map_data = map_data[0]
            geography_mapping_list.append(map_data)
        statutory_ids = [
            int(x) for x in d["statutory_ids"][:-1].split(',')
        ]
        statutory_mapping_list = []
        for s_id in statutory_ids :
            s_map_data = self.statutory_parent_mapping.get(int(s_id))
            if s_map_data is not None :
                s_map_data = s_map_data[1]
            statutory_mapping_list.append(
                s_map_data
            )
        industry_ids = [
            int(x) for x in d["industry_ids"][:-1].split(',')
        ]
        if len(industry_ids) == 1:
            industry_names = self.get_industry_by_id(industry_ids[0])
        else :
            industry_names = self.get_industry_by_id(industry_ids)

        approval = int(d["approval_status"])
        if approval == 0 :
            approval_status_text = "Pending"
        elif approval == 1 :
            approval_status_text = "Approved"
        elif approval == 2 :
            approval_status_text = "Rejected"
        else :
            approval_status_text = "Approved & Notified"

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
