
from clientprotocol.jsonvalidators_client import (
    parse_dictionary,
)

from clientreport import (Request, Response)

__all__ = [
    "GetReassignedHistoryReportFilters",
    "GetReassignedHistoryReport",
    "GetStatusReportConsolidatedFilters",
    "GetStatusReportConsolidated",
    "GetStatutorySettingsUnitWiseFilters",
    "GetStatutorySettingsUnitWise",
    "GetDomainScoreCardFilters",
    "GetDomainScoreCard",
    "GetLEWiseScoreCardFilters",
    "GetLEWiseScoreCard",
    "GetWorkFlowScoreCardFilters",
    "GetWorkFlowScoreCard",

    "GetReassignedHistoryReportFiltersSuccess",
    "GetReassignedHistoryReportSuccess",
    "GetStatusReportConsolidatedFiltersSuccess",
    "GetStatusReportConsolidatedSuccess",
    "GetStatutorySettingsUnitWiseFiltersSuccess",
    "GetStatutorySettingsUnitWiseSuccess",
    "GetDomainScoreCardFiltersSuccess",
    "GetDomainScoreCardSuccess",
    "GetLEWiseScoreCardFiltersSuccess",
    "GetLEWiseScoreCardSuccess",
    "GetWorkFlowScoreCardFiltersSuccess",
    "GetWorkFlowScoreCardSuccess"
]

# Reassigned History Report Start
class GetReassignedHistoryReportFilters(Request):
    def __init__(self, legal_entity_id):
        self.legal_entity_id = legal_entity_id

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["le_id"])
        legal_entity_id = data.get("le_id")
        return GetReassignedHistoryReportFilters(legal_entity_id)

    def to_inner_structure(self):
        return {
            "le_id": self.legal_entity_id
        }

class GetReassignedHistoryReport(Request):
    def __init__(
        self, c_id, legal_entity_id, d_id, unit_id, act, compliance_task,
        usr_id, from_date, to_date, csv, f_count, t_count, count_qry
    ):
        self.c_id = c_id
        self.legal_entity_id = legal_entity_id
        self.d_id = d_id
        self.unit_id = unit_id
        self.act = act
        self.compliance_task = compliance_task
        self.usr_id = usr_id
        self.from_date = from_date
        self.to_date = to_date
        self.csv = csv
        self.f_count = f_count
        self.t_count = t_count
        self.count_qry = count_qry

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "c_id", "le_id", "d_id", "unit_id", "act", "compliance_task",
            "usr_id", "from_date", "to_date", "csv", "f_count", "t_count", "count_qry"]
        )
        c_id = data.get("c_id")
        legal_entity_id = data.get("le_id")
        d_id = data.get("d_id")
        unit_id = data.get("unit_id")
        act = data.get("act")
        compliance_task = data.get("compliance_task")
        usr_id = data.get("usr_id")
        from_date = data.get("from_date")
        to_date = data.get("to_date")
        csv = data.get("csv")
        f_count = data.get("f_count")
        t_count = data.get("t_count")
        count_qry = data.get("count_qry")
        return GetReassignedHistoryReport(
            c_id, legal_entity_id, d_id, unit_id, act, compliance_task,
            usr_id, from_date, to_date, csv, f_count, t_count, count_qry)

    def to_inner_structure(self):
        return {
            "c_id": self.c_id,
            "le_id": self.legal_entity_id,
            "d_id": self.d_id,
            "unit_id": self.unit_id,
            "act": self.act,
            "compliance_task": self.compliance_task,
            "usr_id": self.usr_id,
            "from_date": self.from_date,
            "to_date": self.to_date,
            "csv": self.csv,
            "f_count": self.f_count,
            "t_count": self.t_count,
            "count_qry": self.count_qry
        }
# Reassigned History Report End

# Status Report Consolidated Report Start
class GetStatusReportConsolidatedFilters(Request):
    def __init__(self, legal_entity_id):
        self.legal_entity_id = legal_entity_id

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["le_id"])
        legal_entity_id = data.get("le_id")
        return GetStatusReportConsolidatedFilters(legal_entity_id)

    def to_inner_structure(self):
        return {
            "le_id": self.legal_entity_id
        }

class GetStatusReportConsolidated(Request):
    def __init__(
        self, c_id, legal_entity_id, d_id, unit_id, act, compliance_task, frequency_id, user_type_id, status_name,
        usr_id, from_date, to_date, csv, f_count, t_count, count_qry
    ):
        self.c_id = c_id
        self.legal_entity_id = legal_entity_id
        self.d_id = d_id
        self.unit_id = unit_id
        self.act = act
        self.compliance_task = compliance_task
        self.frequency_id = frequency_id
        self.user_type_id = user_type_id
        self.status_name = status_name
        self.usr_id = usr_id
        self.from_date = from_date
        self.to_date = to_date
        self.csv = csv
        self.f_count = f_count
        self.t_count = t_count
        self.count_qry = count_qry

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "c_id", "le_id", "d_id", "unit_id", "act", "compliance_task", "frequency_id", "user_type_id", "status_name",
            "usr_id", "from_date", "to_date", "csv", "f_count", "t_count", "count_qry"]
        )
        c_id = data.get("c_id")
        legal_entity_id = data.get("le_id")
        d_id = data.get("d_id")
        unit_id = data.get("unit_id")
        act = data.get("act")
        compliance_task = data.get("compliance_task")
        frequency_id = data.get("frequency_id")
        user_type_id = data.get("user_type_id")
        status_name = data.get("status_name")
        usr_id = data.get("usr_id")
        from_date = data.get("from_date")
        to_date = data.get("to_date")
        csv = data.get("csv")
        f_count = data.get("f_count")
        t_count = data.get("t_count")
        count_qry = data.get("count_qry")
        return GetStatusReportConsolidated(
            c_id, legal_entity_id, d_id, unit_id, act, compliance_task, frequency_id, user_type_id, status_name,
            usr_id, from_date, to_date, csv, f_count, t_count, count_qry)

    def to_inner_structure(self):
        return {
            "c_id": self.c_id,
            "le_id": self.legal_entity_id,
            "d_id": self.d_id,
            "unit_id": self.unit_id,
            "act": self.act,
            "compliance_id": self.compliance_id,
            "frequency_id": self.frequency_id,
            "user_type_id": self.user_type_id,
            "status_name": self.status_name,
            "usr_id": self.usr_id,
            "from_date": self.from_date,
            "to_date": self.to_date,
            "csv": self.csv,
            "f_count": self.f_count,
            "t_count": self.t_count,
            "count_qry": self.count_qry
        }
# Status Report Consolidated Report End

# Statutory Settings Unit Wise Start
class GetStatutorySettingsUnitWiseFilters(Request):
    def __init__(self, legal_entity_id):
        self.legal_entity_id = legal_entity_id

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["le_id"])
        legal_entity_id = data.get("le_id")
        return GetStatutorySettingsUnitWiseFilters(legal_entity_id)

    def to_inner_structure(self):
        return {
            "le_id": self.legal_entity_id
        }

class GetStatutorySettingsUnitWise(Request):
    def __init__(
        self, c_id, bg_id, legal_entity_id, d_id, unit_id, div_id, cat_id, act,
        compliance_task, frequency_id, status_name, csv, f_count, t_count, count_qry
    ):
        self.c_id = c_id
        self.bg_id = bg_id
        self.legal_entity_id = legal_entity_id
        self.d_id = d_id
        self.unit_id = unit_id
        self.div_id = div_id
        self.cat_id = cat_id
        self.act = act
        self.compliance_task = compliance_task
        self.frequency_id = frequency_id
        self.status_name = status_name
        self.csv = csv
        self.f_count = f_count
        self.t_count = t_count
        self.count_qry = count_qry

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "c_id", "bg_id", "le_id", "d_id", "unit_id", "div_id", "cat_id", "act", "compliance_task",
            "frequency_id", "status_name", "csv", "f_count", "t_count", "count_qry"]
        )
        c_id = data.get("c_id")
        bg_id = data.get("bg_id")
        legal_entity_id = data.get("le_id")
        d_id = data.get("d_id")
        unit_id = data.get("unit_id")
        div_id = data.get("div_id")
        cat_id = data.get("cat_id")
        act = data.get("act")
        compliance_task = data.get("compliance_task")
        frequency_id = data.get("frequency_id")
        status_name = data.get("status_name")
        csv = data.get("csv")
        f_count = data.get("f_count")
        t_count = data.get("t_count")
        count_qry = data.get("count_qry")
        return GetStatutorySettingsUnitWise(
            c_id, bg_id, legal_entity_id, d_id, unit_id, div_id, cat_id, act, compliance_task,
            frequency_id, status_name, csv, f_count, t_count, count_qry)

    def to_inner_structure(self):
        return {
            "c_id": self.c_id,
            "bg_id": self.bg_id,
            "le_id": self.legal_entity_id,
            "d_id": self.d_id,
            "unit_id": self.unit_id,
            "div_id": self.div_id,
            "cat_id": self.cat_id,
            "act": self.act,
            "compliance_task": self.compliance_task,
            "frequency_id": self.frequency_id,
            "status_name": self.status_name,
            "csv": self.csv,
            "f_count": self.f_count,
            "t_count": self.t_count,
            "count_qry":self.count_qry
        }
# Statutory Settings Unit Wise End

# Domain Score Card Start
class GetDomainScoreCardFilters(Request):
    def __init__(self, legal_entity_id):
        self.legal_entity_id = legal_entity_id

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["le_id"])
        legal_entity_id = data.get("le_id")
        return GetDomainScoreCardFilters(legal_entity_id)

    def to_inner_structure(self):
        return {
            "le_id": self.legal_entity_id
        }

class GetDomainScoreCard(Request):
    def __init__(
        self, c_id, bg_id, legal_entity_id, d_id, div_id, cat_id, csv
    ):
        self.c_id = c_id
        self.bg_id = bg_id
        self.legal_entity_id = legal_entity_id
        self.d_id = d_id
        self.div_id = div_id
        self.cat_id = cat_id
        self.csv = csv

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "c_id", "bg_id", "le_id", "d_id", "div_id", "cat_id", "csv"]
        )
        c_id = data.get("c_id")
        bg_id = data.get("bg_id")
        legal_entity_id = data.get("le_id")
        d_id = data.get("d_id")
        div_id = data.get("div_id")
        cat_id = data.get("cat_id")
        csv = data.get("csv")
        return GetDomainScoreCard(
            c_id, bg_id, legal_entity_id, d_id, div_id, cat_id, csv)

    def to_inner_structure(self):
        return {
            "c_id": self.c_id,
            "bg_id": self.bg_id,
            "le_id": self.legal_entity_id,
            "d_id": self.d_id,
            "div_id": self.div_id,
            "cat_id": self.cat_id,
            "csv": self.csv
        }
# Domain Score Card End


# Legal Entity Wise Score Card Start
class GetLEWiseScoreCardFilters(Request):
    def __init__(self, legal_entity_id):
        self.legal_entity_id = legal_entity_id

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["le_id"])
        legal_entity_id = data.get("le_id")
        return GetLEWiseScoreCardFilters(legal_entity_id)

    def to_inner_structure(self):
        return {
            "le_id": self.legal_entity_id
        }

class GetLEWiseScoreCard(Request):
    def __init__(
        self, c_id, legal_entity_id, d_id, csv
    ):
        self.c_id = c_id
        self.legal_entity_id = legal_entity_id
        self.d_id = d_id
        self.csv = csv

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "c_id", "le_id", "d_id", "csv"]
        )
        c_id = data.get("c_id")
        legal_entity_id = data.get("le_id")
        d_id = data.get("d_id")
        csv = data.get("csv")
        return GetLEWiseScoreCard(
            c_id, legal_entity_id, d_id, csv)

    def to_inner_structure(self):
        return {
            "c_id": self.c_id,
            "le_id": self.legal_entity_id,
            "d_id": self.d_id,
            "csv": self.csv
        }
# Legal Entity Wise Score Card End


# Work Flow Score Card Start
class GetWorkFlowScoreCardFilters(Request):
    def __init__(self, legal_entity_id):
        self.legal_entity_id = legal_entity_id

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["le_id"])
        legal_entity_id = data.get("le_id")
        return GetWorkFlowScoreCardFilters(legal_entity_id)

    def to_inner_structure(self):
        return {
            "le_id": self.legal_entity_id
        }

class GetWorkFlowScoreCard(Request):
    def __init__(
        self, c_id, legal_entity_id, d_id, csv
    ):
        self.c_id = c_id
        self.legal_entity_id = legal_entity_id
        self.d_id = d_id
        self.csv = csv

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "c_id", "le_id", "d_id", "csv"]
        )
        c_id = data.get("c_id")
        legal_entity_id = data.get("le_id")
        d_id = data.get("d_id")
        csv = data.get("csv")
        return GetWorkFlowScoreCard(
            c_id, legal_entity_id, d_id, csv)

    def to_inner_structure(self):
        return {
            "c_id": self.c_id,
            "le_id": self.legal_entity_id,
            "d_id": self.d_id,
            "csv": self.csv
        }
# Work Flow Score Card End


# Reassigned History Report Start

class GetReassignedHistoryReportFiltersSuccess(Response):
    def __init__(self, domains, units, acts, legal_entity_users): # compliances, 
        self.domains = domains
        self.units = units
        self.acts = acts
        # self.compliances = compliances
        self.legal_entity_users = legal_entity_users

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["domains", "units", "acts",  "legal_entity_users"]) # "compliances",
        domains = data.get("domains")
        units = data.get("units")
        acts = data.get("acts")
        # compliances = data.get("compliances")
        legal_entity_users = data.get("legal_entity_users")
        return GetReassignedHistoryReportFiltersSuccess(domains, units, acts, legal_entity_users) # compliances, 

    def to_inner_structure(self):
        return {
            "domains": self.domains,
            "units": self.units,
            "acts": self.acts,
            # "compliances": self.compliances,
            "legal_entity_users": self.legal_entity_users,
        }

class GetReassignedHistoryReportSuccess(Response):
    def __init__(self, reassigned_history_list, total_count, logo_url):
        self.reassigned_history_list = reassigned_history_list
        self.total_count = total_count
        self.logo_url = logo_url

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["reassigned_history_list", "total_count", "logo_url"])
        reassigned_history_list = data.get("reassigned_history_list"),
        total_count = data.get("total_count"),
        logo_url = data.get("logo_url")
        return GetReassignedHistoryReportSuccess(reassigned_history_list, total_count, logo_url)

    def to_inner_structure(self):
        return {
            "reassigned_history_list": self.reassigned_history_list,
            "total_count": self.total_count,
            "logo_url": self.logo_url
        }
# Reassigned History Report End

# Status Report Consolidated Report Start
class GetStatusReportConsolidatedFiltersSuccess(Response):
    def __init__(self, domains, units, acts, compliance_frequency, legal_entity_users): # compliances, 
        self.domains = domains
        self.units = units
        self.acts = acts
        # self.compliances = compliances
        self.compliance_frequency = compliance_frequency
        self.legal_entity_users = legal_entity_users

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["domains", "units", "acts", "compliance_frequency", "legal_entity_users"]) # "compliances", 
        domains = data.get("domains")
        units = data.get("units")
        acts = data.get("acts")
        # compliances = data.get("compliances")
        compliance_frequency = data.get("compliance_frequency")
        legal_entity_users = data.get("legal_entity_users")
        return GetStatusReportConsolidatedFiltersSuccess(domains, units, acts, compliance_frequency, legal_entity_users) # compliances, 

    def to_inner_structure(self):
        return {
            "domains": self.domains,
            "units": self.units,
            "acts": self.acts,
            # "compliances": self.compliances,
            "compliance_frequency": self.compliance_frequency,
            "legal_entity_users": self.legal_entity_users
        }

class GetStatusReportConsolidatedSuccess(Response):
    def __init__(self, status_report_consolidated_list, total_count, logo_url):
        self.status_report_consolidated_list = status_report_consolidated_list
        self.total_count = total_count
        self.logo_url = logo_url

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["status_report_consolidated_list", "total_count", "logo_url"])
        status_report_consolidated_list = data.get("status_report_consolidated_list"),
        total_count = data.get("total_count")
        logo_url = data.get("logo_url")
        return GetStatusReportConsolidatedSuccess(status_report_consolidated_list, total_count, logo_url)
        
    def to_inner_structure(self):
        return {
            "status_report_consolidated_list": self.status_report_consolidated_list,
            "total_count": self.total_count,
            "logo_url": self.logo_url
        }
# Status Report Consolidated Report End


# Statutory Settings Unit Wise Start
class GetStatutorySettingsUnitWiseFiltersSuccess(Response):
    def __init__(self, domains, units, acts, compliance_frequency, divisions, categories): # compliances
        self.domains = domains
        self.units = units
        self.acts = acts
        # self.compliances = compliances
        self.compliance_frequency = compliance_frequency
        self.divisions = divisions
        self.categories = categories

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["domains", "units", "acts", "compliance_frequency", "div_infos", "cat_infos"]) # "compliances", 
        domains = data.get("domains")
        units = data.get("units")
        acts = data.get("acts")
        # compliances = data.get("compliances")
        compliance_frequency = data.get("compliance_frequency")
        divisions = data.get("div_infos")
        categories = data.get("cat_infos")
        return GetStatutorySettingsUnitWiseFiltersSuccess(domains, units, acts, compliance_frequency, divisions, categories) # compliances, 

    def to_inner_structure(self):
        return {
            "domains": self.domains,
            "units": self.units,
            "acts": self.acts,
            # "compliances": self.compliances,
            "compliance_frequency": self.compliance_frequency,
            "div_infos": self.divisions,
            "cat_infos": self.categories
        }

class GetStatutorySettingsUnitWiseSuccess(Response):
    def __init__(self, statutory_settings_unit_Wise_list, total_count, logo_url):
        self.statutory_settings_unit_Wise_list = statutory_settings_unit_Wise_list
        self.total_count = total_count
        self.logo_url = logo_url

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["statutory_settings_unit_Wise_list", "total_count", "logo_url"])
        statutory_settings_unit_Wise_list = data.get("statutory_settings_unit_Wise_list"),
        total_count = data.get("total_count")
        logo_url = data.get("logo_url")
        return GetStatutorySettingsUnitWiseSuccess(statutory_settings_unit_Wise_list, total_count, logo_url)

    def to_inner_structure(self):
        return {
            "statutory_settings_unit_Wise_list": self.statutory_settings_unit_Wise_list,
            "total_count": self.total_count,
            "logo_url": self.logo_url
        }
# Statutory Settings Unit Wise End


# Domain Score Card Start
class GetDomainScoreCardFiltersSuccess(Response):
    def __init__(self, domains, divisions, categories):
        self.domains = domains
        self.divisions = divisions
        self.categories = categories

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["domains", "div_infos", "cat_infos"])
        domains = data.get("domains")
        divisions = data.get("div_infos")
        categories = data.get("cat_infos")
        return GetDomainScoreCardFiltersSuccess(domains, divisions, categories)

    def to_inner_structure(self):
        return {
            "domains": self.domains,
            "div_infos": self.divisions,
            "cat_infos": self.categories
        }

class GetDomainScoreCardSuccess(Response):
    def __init__(self, domain_score_card_list, logo_url):
        self.domain_score_card_list = domain_score_card_list
        self.logo_url = logo_url

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["domain_score_card_list", "logo_url"])
        domain_score_card_list = data.get("domain_score_card_list")
        logo_url = data.get("logo_url")
        return GetDomainScoreCardSuccess(domain_score_card_list, logo_url)

    def to_inner_structure(self):
        return {
            "domain_score_card_list": self.domain_score_card_list,
            "logo_url": self.logo_url
        }
# Domain Score Card End


# Legal Entity Wise Score Card Start
class GetLEWiseScoreCardFiltersSuccess(Response):
    def __init__(self, domains):
        self.domains = domains

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["domains"])
        domains = data.get("domains")
        return GetLEWiseScoreCardFiltersSuccess(domains)

    def to_inner_structure(self):
        return {
            "domains": self.domains
        }

class GetLEWiseScoreCardSuccess(Response):
    def __init__(self, le_wise_score_card_list, logo_url):
        self.le_wise_score_card_list = le_wise_score_card_list
        self.logo_url = logo_url

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["le_wise_score_card_list", "logo_url"])
        le_wise_score_card_list = data.get("le_wise_score_card_list")
        logo_url = data.get("logo_url")
        return GetLEWiseScoreCardSuccess(le_wise_score_card_list, logo_url)

    def to_inner_structure(self):
        return {
            "le_wise_score_card_list": self.le_wise_score_card_list,
            "logo_url": self.logo_url
        }
# Legal Entity Wise Score Card End


# Work Flow Score Card Start
class GetWorkFlowScoreCardFiltersSuccess(Response):
    def __init__(self, domains):
        self.domains = domains

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["domains"])
        domains = data.get("domains")
        return GetWorkFlowScoreCardFiltersSuccess(domains)

    def to_inner_structure(self):
        return {
            "domains": self.domains
        }

class GetWorkFlowScoreCardSuccess(Response):
    def __init__(self, work_flow_score_card_list, logo_url):
        self.work_flow_score_card_list = work_flow_score_card_list
        self.logo_url = logo_url

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["work_flow_score_card_list", "logo_url"])
        work_flow_score_card_list = data.get("work_flow_score_card_list")
        logo_url = data.get("logo_url")
        return GetWorkFlowScoreCardSuccess(work_flow_score_card_list, logo_url)

    def to_inner_structure(self):
        return {
            "work_flow_score_card_list": self.work_flow_score_card_list,
            "logo_url": self.logo_url
        }
# Work Flow Score Card End
