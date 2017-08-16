
from clientprotocol.jsonvalidators_client import (parse_dictionary, parse_static_list, to_structure_dictionary_values)

#
# Request
#

class Request(object):
    def to_structure(self):
        name = type(self).__name__
        inner = self.to_inner_structure()
        if type(inner) is dict:
            inner = to_structure_dictionary_values(inner)
        return [name, inner]

    def to_inner_structure(self):
        raise NotImplementedError

    @staticmethod
    def parse_structure(data):
        data = parse_static_list(data, 2)
        name, data = data
        if _Request_class_map.get(name) is None:
            msg = "invalid request: " + name
            raise ValueError(msg)
        return _Request_class_map[name].parse_inner_structure(data)

    @staticmethod
    def parse_inner_structure(data):
        raise NotImplementedError

class GetChartFilters(Request):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return GetChartFilters()

    def to_inner_structure(self):
        return {
        }

class CheckContractExpiration(Request):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return CheckContractExpiration()

    def to_inner_structure(self):
        return {
        }


class GetComplianceStatusChart(Request):
    def __init__(
        self,
        country_ids, domain_ids,
        filter_type, filter_ids,
        from_date, to_date,
        chart_year, legal_entity_ids
    ):
        self.country_ids = country_ids
        self.domain_ids = domain_ids
        self.filter_type = filter_type
        self.filter_ids = filter_ids
        self.from_date = from_date
        self.to_date = to_date
        self.chart_year = chart_year
        self.legal_entity_ids = legal_entity_ids

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "c_ids", "d_ids", "filter_type", "filter_ids", "from_date", "to_date",
            "chart_year", "le_ids"
        ])
        return GetComplianceStatusChart(
            data.get("c_ids"), data.get("d_ids"), data.get("filter_type"),
            data.get("filter_ids"), data.get("from_date"), data.get("to_date"),
            data.get("chart_year"), data.get("le_ids"),
        )

    def to_inner_structure(self):
        return {
            "c_ids": self.country_ids, "d_ids": self.domain_ids, "filter_type": self.filter_type,
            "filter_ids": self.filter_ids, "from_date": self.from_date, "to_date": self.to_date,
            "chart_year": self.chart_year, "le_ids": self.legal_entity_ids
        }

class GetEscalationsChart(Request):
    def __init__(self, country_ids, domain_ids, filter_type, filter_ids, legal_entity_ids):
        self.country_ids = country_ids
        self.domain_ids = domain_ids
        self.filter_type = filter_type
        self.filter_ids = filter_ids
        self.legal_entity_ids = legal_entity_ids

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["c_ids", "d_ids", "filter_type", "filter_ids", "le_ids"])
        return GetEscalationsChart(
            data.get("c_ids"), data.get("d_ids"), data.get("filter_type"), data.get("filter_ids"), data.get("le_ids"),
        )

    def to_inner_structure(self):
        return {
            "c_ids": self.country_ids,
            "d_ids": self.domain_ids,
            "filter_type": self.filter_type,
            "filter_ids": self.filter_ids,
            "le_ids": self.legal_entity_ids
        }

class GetNotCompliedChart(Request):
    def __init__(self, country_ids, domain_ids, filter_type, filter_ids, legal_entity_ids):
        self.country_ids = country_ids
        self.domain_ids = domain_ids
        self.filter_type = filter_type
        self.filter_ids = filter_ids
        self.legal_entity_ids = legal_entity_ids

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["c_ids", "d_ids", "filter_type", "filter_ids", "le_ids"])
        return GetNotCompliedChart(
            data.get("c_ids"), data.get("d_ids"), data.get("filter_type"), data.get("filter_ids"), data.get("le_ids"),
        )

    def to_inner_structure(self):
        return {
            "c_ids": self.country_ids, "d_ids": self.domain_ids,
            "filter_type": self.filter_type, "filter_ids": self.filter_ids, "le_ids": self.legal_entity_ids
        }


class GetTrendChart(Request):
    def __init__(self, country_ids, domain_ids, filter_type, filter_ids, legal_entity_ids):
        self.country_ids = country_ids
        self.domain_ids = domain_ids
        self.filter_type = filter_type
        self.filter_ids = filter_ids
        self.legal_entity_ids = legal_entity_ids

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["c_ids", "d_ids", "filter_type", "filter_ids", "le_ids"])
        return GetTrendChart(
            data.get("c_ids"), data.get("d_ids"), data.get("filter_type"), data.get("filter_ids"), data.get("le_ids"),
        )

    def to_inner_structure(self):
        return {
            "c_ids": self.country_ids, "d_ids": self.domain_ids, "filter_type": self.filter_type,
            "filter_ids": self.filter_ids, "le_ids": self.legal_entity_ids
        }

class GetComplianceApplicabilityStatusChart(Request):
    def __init__(self, country_ids, domain_ids, filter_type, filter_ids, legal_entity_ids):
        self.country_ids = country_ids
        self.domain_ids = domain_ids
        self.filter_type = filter_type
        self.filter_ids = filter_ids
        self.legal_entity_ids = legal_entity_ids

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["c_ids", "d_ids", "filter_type", "filter_ids", "le_ids"])
        return GetComplianceApplicabilityStatusChart(
            data.get("c_ids"), data.get("d_ids"), data.get("filter_type"), data.get("filter_ids"), data.get("le_ids"),
        )

    def to_inner_structure(self):
        return {
            "c_ids": self.country_ids, "d_ids": self.domain_ids, "filter_type": self.filter_type,
            "filter_ids": self.filter_id, "le_ids": self.legal_entity_ids
        }

class GetAssigneeWiseCompliancesChart(Request):
    def __init__(
        self, country_id, business_group_id, legal_entity_ids, division_id,
        unit_id, user_id, csv
    ):
        self.country_id = country_id
        self.business_group_id = business_group_id
        self.legal_entity_ids = legal_entity_ids
        self.division_id = division_id
        self.unit_id = unit_id
        self.user_id = user_id
        self.csv = csv

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "c_id", "bg_id", "le_ids", "div_id", "unit_id", "usr_id", "csv"
        ])
        return GetAssigneeWiseCompliancesChart(
            data.get("c_id"), data.get("bg_id"), data.get("le_ids"), data.get("div_id"),
            data.get("unit_id"), data.get("usr_id"), data.get("csv"),
        )

    def to_inner_structure(self):
        return {
            "c_id": self.country_id, "bg_id": self.business_group_id, "le_ids": self.legal_entity_ids,
            "div_id": self.division_id, "unit_id": self.unit_id, "usr_id": self.user_id, "csv": self.csv
        }

class GetAssigneewiseYearwiseCompliances(Request):
    def __init__(
        self, country_id, unit_id, user_id, legal_entity_ids,
        domain_ids
    ):
        self.country_id = country_id
        self.unit_id = unit_id
        self.user_id = user_id
        self.legal_entity_ids = legal_entity_ids
        self.domain_ids = domain_ids

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["c_id", "u_id", "usr_id", "le_ids", "d_ids"])
        return GetAssigneewiseYearwiseCompliances(
            data.get("c_id"), data.get("u_id"), data.get("usr_id"),
            data.get("le_ids"), data.get("d_ids"),
        )

    def to_inner_structure(self):
        return {
            "c_id": self.country_id, "u_id": self.unit_id, "usr_id": self.user_id,
            "le_ids": self.legal_entity_ids, "d_ids": self.domain_ids
        }

class GetAssigneewiseReassignedComplianes(Request):
    def __init__(
        self, country_id, unit_id, user_id, domain_id,
        legal_entity_ids
    ):
        self.country_id = country_id
        self.unit_id = unit_id
        self.user_id = user_id
        self.domain_id = domain_id
        self.legal_entity_ids = legal_entity_ids

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["c_id", "u_id", "usr_id", "d_id", "le_ids"])
        country_id = data.get("c_id")
        unit_id = data.get("u_id")
        user_id = data.get("usr_id")
        domain_id = data.get("d_id")
        legal_entity_ids = data.get("le_ids")
        return GetAssigneewiseReassignedComplianes(
            country_id, unit_id, user_id, domain_id, legal_entity_ids
        )

    def to_inner_structure(self):
        return {
            "c_id": self.country_id,
            "u_id": self.unit_id,
            "usr_id": self.user_id,
            "d_id": self.domain_id,
            "le_ids": self.legal_entity_ids
        }

class GetAssigneeWiseComplianceDrillDown(Request):
    def __init__(
        self, country_id, assignee_id, domain_ids, year, unit_id, start_count,
        legal_entity_ids
    ):
        self.country_id = country_id
        self.assignee_id = assignee_id
        self.domain_ids = domain_ids
        self.year = year
        self.unit_id = unit_id
        self.start_count = start_count
        self.legal_entity_ids = legal_entity_ids

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "c_id", "assignee_id",
            "d_ids", "chart_year", "unit_id", "start_count", "le_ids"
        ])
        country_id = data.get("c_id")
        assignee_id = data.get("assignee_id")
        domain_ids = data.get("d_ids")
        year = data.get("chart_year")
        unit_id = data.get("unit_id")
        start_count = data.get("start_count")
        legal_entity_ids = data.get("le_ids")
        return GetAssigneeWiseComplianceDrillDown(
            country_id, assignee_id, domain_ids, year, unit_id, start_count,
            legal_entity_ids
        )

    def to_inner_structure(self):
        return {
            "c_id": self.country_id,
            "assignee_id": self.assignee_id,
            "d_ids": self.domain_ids,
            "chart_year": self.year,
            "unit_id": self.unit_id,
            "start_count" : self.start_count,
            "le_ids": self.legal_entity_ids
        }

class GetComplianceStatusDrillDownData(Request):
    def __init__(
        self, domain_ids, from_date, to_date, year,
        filter_type, filter_id, compliance_status,
        record_count, legal_entity_ids
    ):
        self.domain_ids = domain_ids
        self.from_date = from_date
        self.to_date = to_date
        self.year = year
        self.filter_type = filter_type
        self.filter_id = filter_id
        self.compliance_status = compliance_status
        self.record_count = record_count
        self.legal_entity_ids = legal_entity_ids

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "d_ids", "from_date", "to_date", "chart_year",  "filter_type",
            "filter_id", "compliance_status", "record_count",
            "le_ids"
        ])
        domain_ids = data.get("d_ids")
        from_date = data.get("from_date")
        to_date = data.get("to_date")
        year = data.get("chart_year")
        filter_type = data.get("filter_type")
        filter_id = data.get("filter_id")
        compliance_status = data.get("compliance_status")
        record_count = data.get("record_count")
        legal_entity_id = data.get("le_ids")
        return GetComplianceStatusDrillDownData(
            domain_ids, from_date, to_date,
            year, filter_type, filter_id,
            compliance_status, record_count,
            legal_entity_id
        )

    def to_inner_structure(self):
        return {
            "d_ids": self.domain_ids,
            "from_date": self.from_date,
            "to_date": self.to_date,
            "chart_year": self.year,
            "filter_type": self.filter_type,
            "filter_id": self.filter_id,
            "compliance_status": self.compliance_status,
            "record_count": self.record_count,
            "le_ids": self.legal_entity_ids
        }

class GetEscalationsDrillDownData(Request):
    def __init__(
        self, domain_ids, filter_type, filter_ids, year,
        record_count, legal_entity_ids
    ):
        self.domain_ids = domain_ids
        self.filter_type = filter_type
        self.filter_ids = filter_ids
        self.year = year
        self.record_count = record_count
        self.legal_entity_ids = legal_entity_ids

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "d_ids", "filter_type", "filter_ids", "chart_year",
            "record_count", "le_ids"
        ])
        domain_ids = data.get("d_ids")
        filter_type = data.get("filter_type")
        filter_ids = data.get("filter_ids")
        year = data.get("chart_year")
        record_count = data.get("record_count")
        legal_entity_ids = data.get("le_ids")
        return GetEscalationsDrillDownData(
            domain_ids, filter_type, filter_ids, year, record_count,
            legal_entity_ids
        )

    def to_inner_structure(self):
        return {
            "d_ids": self.domain_ids,
            "filter_type": self.filter_type,
            "filter_ids": self.filter_ids,
            "chart_year": self.year,
            "record_count": self.record_count,
            "le_ids": self.legal_entity_ids
        }

class GetComplianceApplicabilityStatusDrillDown(Request):
    def __init__(
        self, country_ids, domain_ids, filter_type, filter_ids,
        applicability_status, record_count,
        legal_entity_ids
    ):
        self.country_ids = country_ids
        self.domain_ids = domain_ids
        self.filter_type = filter_type
        self.filter_ids = filter_ids
        self.applicability_status = applicability_status
        self.record_count = record_count
        self.legal_entity_ids = legal_entity_ids

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "c_ids", "d_ids", "filter_type", "filter_ids",
            "applicability_status", "record_count", "le_ids"
        ])
        country_ids = data.get("c_ids")
        domain_ids = data.get("d_ids")
        filter_type = data.get("filter_type")
        filter_ids = data.get("filter_ids")
        applicability_status = data.get("applicability_status")
        record_count = data.get("record_count")
        legal_entity_ids = data.get("le_ids")
        return GetComplianceApplicabilityStatusDrillDown(
            country_ids, domain_ids, filter_type, filter_ids,
            applicability_status, record_count, legal_entity_ids
        )

    def to_inner_structure(self):
        return {
            "c_ids": self.country_ids,
            "d_ids": self.domain_ids,
            "filter_type": self.filter_type,
            "filter_ids": self.filter_ids,
            "applicability_status": self.applicability_status,
            "record_count": self.record_count,
            "le_ids": self.legal_entity_ids
        }

class GetNotCompliedDrillDown(Request):
    def __init__(
        self, domain_ids,  filter_type, filter_ids, not_complied_type,
        record_count, legal_entity_ids
    ):
        self.domain_ids = domain_ids
        self.filter_type = filter_type
        self.filter_ids = filter_ids
        self.not_complied_type = not_complied_type
        self.record_count = record_count
        self.legal_entity_ids = legal_entity_ids

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "d_ids", "filter_type", "filter_ids", "not_complied_type",
            "record_count", "le_ids"
        ])
        domain_ids = data.get("d_ids")
        filter_type = data.get("filter_type")
        filter_ids = data.get("filter_ids")
        not_complied_type = data.get("not_complied_type")
        record_count = data.get("record_count")
        legal_entity_ids = data.get("le_ids")
        return GetNotCompliedDrillDown(
            domain_ids, filter_type, filter_ids, not_complied_type,
            record_count, legal_entity_ids
        )

    def to_inner_structure(self):
        return {
            "d_ids": self.domain_ids,
            "filter_type": self.filter_type,
            "filter_ids": self.filter_ids,
            "not_complied_type": self.not_complied_type,
            "record_count": self.record_count,
            "le_ids": self.legal_entity_ids
        }

class GetTrendChartDrillDownData(Request):
    def __init__(
        self, filter_type, filter_ids, country_ids, domain_ids, year,
        legal_entity_ids
    ):
        self.filter_type = filter_type
        self.filter_ids = filter_ids
        self.country_ids = country_ids
        self.domain_ids = domain_ids
        self.year = year
        self.legal_entity_ids = legal_entity_ids

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "filter_type", "filter_ids", "c_ids", "d_ids", "year",
            "le_ids"
        ])
        filter_type = data.get("filter_type")
        filter_ids = data.get("filter_ids")
        country_ids = data.get("c_ids")
        domain_ids = data.get("d_ids")
        year = data.get("year")
        legal_entity_ids = data.get("le_ids")
        return GetTrendChartDrillDownData(
            filter_type, filter_ids,
            country_ids, domain_ids, year,
            legal_entity_ids
        )

    def to_inner_structure(self):
        return {
            "filter_type": self.filter_type,
            "filter_ids": self.filter_ids,
            "c_ids": self.country_ids,
            "d_ids": self.domain_ids,
            "year": self.year,
            "le_ids": self.legal_entity_ids
        }

class GetNotificationsCount(Request):
    def __init__(self, legal_entity_ids):
        self.legal_entity_ids = legal_entity_ids

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["le_ids"])
        legal_entity_ids = data.get("le_ids")
        return GetNotificationsCount(legal_entity_ids)

    def to_inner_structure(self):
        return {
            "le_ids": self.legal_entity_ids
        }

class GetNotifications(Request):
    def __init__(self, legal_entity_ids, notification_type, start_count, end_count):
        self.legal_entity_ids = legal_entity_ids
        self.notification_type = notification_type
        self.start_count = start_count
        self.end_count = end_count

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["le_ids", "notification_type", "start_count", "end_count"])
        legal_entity_ids = data.get("le_ids")
        notification_type = data.get("notification_type")
        start_count = data.get("start_count")
        end_count = data.get("end_count")
        return GetNotifications(legal_entity_ids, notification_type, start_count, end_count)

    def to_inner_structure(self):
        return {
            "le_ids": self.legal_entity_ids,
            "notification_type": self.notification_type,
            "start_count": self.start_count,
            "end_count": self.end_count
        }

class UpdateNotificationStatus(Request):
    def __init__(self, legal_entity_ids, notification_id, has_read, extra_details):
        self.legal_entity_ids = legal_entity_ids
        self.notification_id = notification_id
        self.has_read = has_read
        self.extra_details = extra_details

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["le_ids", "notification_id", "has_read", "extra_details"])
        legal_entity_ids = data.get("le_ids")
        notification_id = data.get("notification_id")
        has_read = data.get("has_read")
        extra_details = data.get("extra_details")
        return UpdateNotificationStatus(legal_entity_ids, notification_id, has_read, extra_details)

    def to_inner_structure(self):
        return {
            "le_ids": self.legal_entity_ids,
            "notification_id": self.notification_id,
            "has_read": self.has_read,
            "extra_details": self.extra_details
        }

class GetStatutoryNotifications(Request):
    def __init__(self, legal_entity_ids, start_count, end_count):
        self.legal_entity_ids = legal_entity_ids
        self.start_count = start_count
        self.end_count = end_count

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["le_ids", "start_count", "end_count"])
        legal_entity_ids = data.get("le_ids")
        start_count = data.get("start_count")
        end_count = data.get("end_count")
        return GetStatutoryNotifications(legal_entity_ids, start_count, end_count)

    def to_inner_structure(self):
        return {
            "le_ids": self.legal_entity_ids,
            "start_count": self.start_count,
            "end_count": self.end_count
        }

class UpdateStatutoryNotificationsStatus(Request):
    def __init__(self, legal_entity_ids, notification_id, has_read):
        self.legal_entity_ids = legal_entity_ids
        self.notification_id = notification_id
        self.has_read = has_read

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["le_ids", "notification_id", "has_read"])
        legal_entity_ids = data.get("le_ids")
        notification_id = data.get("notification_id")
        has_read = data.get("has_read")
        return UpdateStatutoryNotificationsStatus(legal_entity_ids, notification_id, has_read)

    def to_inner_structure(self):
        return {
            "le_ids": self.legal_entity_ids,
            "notification_id": self.notification_id,
            "has_read": self.has_read
        }

def _init_Request_class_map():
    classes = [
        GetChartFilters, GetComplianceStatusChart, GetEscalationsChart,
        GetNotCompliedChart, GetTrendChart, GetComplianceApplicabilityStatusChart,
        GetAssigneeWiseCompliancesChart, GetAssigneeWiseComplianceDrillDown,
        GetComplianceStatusDrillDownData, GetEscalationsDrillDownData,
        GetComplianceApplicabilityStatusDrillDown, GetNotCompliedDrillDown,
        GetTrendChartDrillDownData, GetNotificationsCount, GetNotifications, UpdateNotificationStatus,
        CheckContractExpiration,
        GetAssigneewiseYearwiseCompliances, GetAssigneewiseReassignedComplianes,
        GetStatutoryNotifications, UpdateStatutoryNotificationsStatus
    ]
    class_map = {}
    for c in classes:
        class_map[c.__name__] = c
    return class_map

_Request_class_map = _init_Request_class_map()

#
# Response
#

class Response(object):
    def to_structure(self):
        name = type(self).__name__
        inner = self.to_inner_structure()
        if type(inner) is dict:
            inner = to_structure_dictionary_values(inner)
        return [name, inner]

    def to_inner_structure(self):
        raise NotImplementedError

    @staticmethod
    def parse_structure(data):
        data = parse_static_list(data, 2)
        name, data = data
        if _Response_class_map.get(name) is None:
            msg = "invalid request: " + name
            raise ValueError(msg)
        return _Response_class_map[name].parse_inner_structure(data)

    @staticmethod
    def parse_inner_structure(data):
        raise NotImplementedError

class GetChartFiltersSuccess(Response):
    def __init__(
        self, countries, domains, business_groups,
        legal_entities, divisions, units, domain_month,
        group_name, categories
    ):
        self.countries = countries
        self.domains = domains
        self.business_groups = business_groups
        self.legal_entities = legal_entities
        self.divisions = divisions
        self.units = units
        self.domain_month = domain_month
        self.group_name = group_name
        self.categories = categories

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "countries", "d_info", "bg_groups",
            "le_did_infos", "div_infos", "assign_units" "d_months", "g_name",
            "cat_info"
        ])
        countries = data.get("countries")
        domains = data.get("d_info")
        business_groups = data.get("bg_groups")
        legal_entities = data.get("le_did_infos")
        divisions = data.get("div_infos")
        units = data.get("assign_units")
        domain_month = data.get("d_months")
        group_name = data.get("g_name")
        cat_info = data.get("cat_info")
        return GetChartFiltersSuccess(
            countries, domains, business_groups, legal_entities,
            divisions, units, domain_month, group_name, cat_info
        )

    def to_inner_structure(self):
        return {
            "countries": self.countries,
            "d_info": self.domains,
            "bg_groups": self.business_groups,
            "le_did_infos": self.legal_entities,
            "div_infos": self.divisions,
            "assign_units": self.units,
            "d_months": self.domain_month,
            "g_name": self.group_name,
            "cat_info": self.categories
        }

class GetComplianceStatusChartSuccess(Response):
    def __init__(self, chart_data):
        self.chart_data = chart_data

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["chart_data"])
        chart_data = data.get("chart_data")
        return ChartDataMap(chart_data)

    def to_inner_structure(self):
        return {
            "chart_data": self.chart_data,
        }

class GetEscalationsChartSuccess(Response):
    def __init__(self, years, chart_data):
        self.years = years
        self.chart_data = chart_data

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["years", "es_chart_data"])
        years = data.get("years")
        chart_data = data.get("es_chart_data")
        return GetEscalationsChartSuccess(chart_data, years)

    def to_inner_structure(self):
        return {
            "years": self.years,
            "es_chart_data": self.chart_data,
        }

class GetNotCompliedChartSuccess(Response):
    def __init__(self, T_0_to_30_days_count, T_31_to_60_days_count, T_61_to_90_days_count, Above_90_days_count):
        self.T_0_to_30_days_count = T_0_to_30_days_count
        self.T_31_to_60_days_count = T_31_to_60_days_count
        self.T_61_to_90_days_count = T_61_to_90_days_count
        self.Above_90_days_count = Above_90_days_count

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["T_0_to_30_days_count", "T_31_to_60_days_count", "T_61_to_90_days_count", "Above_90_days_count"])
        T_0_to_30_days_count = data.get("T_0_to_30_days_count")
        T_31_to_60_days_count = data.get("T_31_to_60_days_count")
        T_61_to_90_days_count = data.get("T_61_to_90_days_count")
        Above_90_days_count = data.get("Above_90_days_count")
        return GetNotCompliedChartSuccess(T_0_to_30_days_count, T_31_to_60_days_count, T_61_to_90_days_count, Above_90_days_count)

    def to_inner_structure(self):
        return {
            "T_0_to_30_days_count": self.T_0_to_30_days_count,
            "T_31_to_60_days_count": self.T_31_to_60_days_count,
            "T_61_to_90_days_count": self.T_61_to_90_days_count,
            "Above_90_days_count": self.Above_90_days_count,
        }

class GetTrendChartSuccess(Response):
    def __init__(self, years, data):
        self.years = years
        self.data = data

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["years", "trend_data"])
        years = data.get("years")
        data = data.get("trend_data")
        return GetTrendChartSuccess(years, data)

    def to_inner_structure(self):
        return {
            "years": self.years,
            "trend_data": self.data,
        }

class CheckContractExpirationSuccesss(Response):
    def __init__(
        self, no_of_days_left, notification_count, reminder_count,
        escalation_count, show_popup, notification_text
    ):
        self.no_of_days_left = no_of_days_left
        self.notification_count = notification_count
        self.reminder_count = reminder_count
        self.escalation_count = escalation_count
        self.show_popup = show_popup
        self.notification_text = notification_text

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(
            data, [
                "no_of_days_left", "notification_count", "reminder_count",
                "escalation_count", "show_popup", "notification_text"
            ]
        )
        no_of_days_left = data.get("no_of_days_left")
        # no_of_days_left = parse_structure_UnignedIntegerType_32(no_of_days_left)
        notification_count = data.get("notification_count")
        # notification_count = parse_structure_UnignedIntegerType_32(notification_count)
        reminder_count = data.get("reminder_count")
        # reminder_count = parse_structure_UnignedIntegerType_32(reminder_count)
        escalation_count = data.get("escalation_count")
        # escalation_count = parse_structure_UnignedIntegerType_32(escalation_count)
        show_popup = data.get("show_popup")
        show_popup = parse_structure_OptionalType_Bool(show_popup)
        notification_text = data.get("notification_text")
        notification_text = parse_structure_Text(notification_text)
        return CheckContractExpirationSuccesss(
            no_of_days_left, notification_count, reminder_count, escalation_count,
            show_popup, notification_text
        )

    # def to_inner_structure(self):
    #     return {
    #         "no_of_days_left": to_structure_UnsignedIntegerType_32(self.no_of_days_left),
    #         "notification_count": to_structure_UnsignedIntegerType_32(self.notification_count),
    #         "reminder_count": to_structure_UnsignedIntegerType_32(self.reminder_count),
    #         "escalation_count": to_structure_UnsignedIntegerType_32(self.escalation_count),
    #         "show_popup": to_structure_Bool(self.show_popup),
    #         "notification_text": to_structure_Text(self.notification_text)
    #     }

class GetComplianceApplicabilityStatusChartSuccess(Response):
    def __init__(self, unassign_count, not_opted_count, rejected_count, not_complied_count):
        self.unassign_count = unassign_count
        self.not_opted_count = not_opted_count
        self.rejected_count = rejected_count
        self.not_complied_count = not_complied_count

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["not_opted_count", "unassign_count", "rejected_count", "not_complied_count"])
        return GetComplianceApplicabilityStatusChartSuccess(
            data.get("unassign_count"), data.get("not_opted_count"),
            data.get("rejected_count"), data.get("not_complied_count")
        )

    def to_inner_structure(self):
        return {
            "not_opted_count": self.not_opted_count,
            "unassign_count": self.unassign_count,
            "rejected_count": self.rejected_count,
            "not_complied_count": self.not_complied_count
        }

class GetAssigneeWiseCompliancesChartSuccess(Response):
    def __init__(self, chart_data):
        self.chart_data = chart_data

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["assingee_data"])
        chart_data = data.get("assingee_data")
        return GetAssigneeWiseCompliancesChartSuccess(chart_data)

    def to_inner_structure(self):
        return {
            "assingee_data": self.chart_data,
        }

class GetAssigneewiseYearwiseCompliancesSuccess(Response):
    def __init__(self, chart_data):
        self.chart_data = chart_data

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["year_wise_data"])
        chart_data = data.get("year_wise_data")
        return GetAssigneewiseYearwiseCompliancesSuccess(chart_data)

    def to_inner_structure(self):
        return {
            "year_wise_data": self.chart_data,
        }

class GetAssigneewiseReassignedComplianesSuccess(Response):
    def __init__(self, chart_data):
        self.chart_data = chart_data

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["reassigned_compliances"])
        chart_data = data.get("reassigned_compliances")
        return GetAssigneewiseReassignedComplianesSuccess(chart_data)

    def to_inner_structure(self):
        return {
            "reassigned_compliances": self.chart_data,
        }


class AssigneeWiseCompliance(object):
    def __init__(self, complied, delayed, inprogress, not_complied):
        self.complied = complied
        self.delayed = delayed
        self.inprogress = inprogress
        self.not_complied = not_complied

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["complied_map", "delayed_map", "inprogress_map", "not_complied_map"])
        complied = data.get("complied_map")
        delayed = data.get("delayed_map")
        inprogress = data.get("inprogress_map")
        not_complied = data.get("not_complied_map")
        return AssigneeWiseCompliance(complied, delayed, inprogress, not_complied)

    def to_structure(self):
        return {
            "complied_map": self.complied,
            "delayed_map": self.delayed,
            "inprogress_map": self.inprogress,
            "not_complied_map": self.not_complied,
        }

class GetAssigneeWiseComplianceDrillDownSuccess(Response):
    def __init__(self, drill_down_data, total_count):
        self.drill_down_data = drill_down_data
        self.total_count = total_count

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["assignee_wise_drill_down"])
        drill_down_data = data.get("assignee_wise_drill_down")
        total_count = data.get("total_count")
        return GetAssigneeWiseComplianceDrillDownSuccess(drill_down_data, total_count)

    def to_inner_structure(self):
        return {
            "assignee_wise_drill_down": self.drill_down_data,
            "total_count": self.total_count
        }

class GetComplianceStatusDrillDownDataSuccess(Response):
    def __init__(self, drill_down_data):
        self.drill_down_data = drill_down_data

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["drill_down_data"])
        drill_down_data = data.get("drill_down_data")
        return GetComplianceStatusDrillDownDataSuccess(drill_down_data)

    def to_inner_structure(self):
        return {
            "drill_down_data": self.drill_down_data,
        }

class GetEscalationsDrillDownDataSuccess(Response):
    def __init__(self, delayed, not_complied):
        self.delayed = delayed
        self.not_complied = not_complied

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["delayed", "not_complied"])
        delayed = data.get("delayed")
        not_complied = data.get("not_complied")
        return GetEscalationsDrillDownDataSuccess(delayed, not_complied)

    def to_inner_structure(self):
        return {
            "delayed": self.delayed,
            "not_complied": self.not_complied
        }

class GetComplianceApplicabilityStatusDrillDownSuccess(Response):
    def __init__(self, drill_down_data):
        self.drill_down_data = drill_down_data

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["r_drill_down_data"])
        drill_down_data = data.get("r_drill_down_data")
        return GetComplianceApplicabilityStatusDrillDownSuccess(drill_down_data)

    def to_inner_structure(self):
        return {
            "r_drill_down_data": self.drill_down_data,
        }

class GetNotCompliedDrillDownSuccess(Response):
    def __init__(self, drill_down_data):
        self.drill_down_data = drill_down_data

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["n_drill_down_data"])
        drill_down_data = data.get("n_drill_down_data")
        return GetNotCompliedDrillDownSuccess(drill_down_data)

    def to_inner_structure(self):
        return {
            "n_drill_down_data": self.drill_down_data,
        }

class GetTrendChartDrillDownDataSuccess(Response):
    def __init__(self, drill_down_data):
        self.drill_down_data = drill_down_data

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["t_drill_down_data"])
        drill_down_data = data.get("t_drill_down_data")
        return GetTrendChartDrillDownDataSuccess(drill_down_data)

    def to_inner_structure(self):
        return {
            "t_drill_down_data": self.drill_down_data,
        }

class GetNotificationsCountSuccess(Response):
    def __init__(self, notification_count):
        self.notification_count = notification_count

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["notification_count"])
        statutory = data.get("notification_count")
        return GetNotificationsCountSuccess(notification_count)

    def to_inner_structure(self):
        return {
            "notification_count": self.notification_count
        }

class GetRemindersSuccess(Response):
    def __init__(self, reminders, reminder_count, reminder_expire_count):
        self.reminders = reminders
        self.reminder_count = reminder_count
        self.reminder_expire_count = reminder_expire_count

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["reminders", "reminder_count", "reminder_expire_count"])
        reminders = data.get("reminders")
        reminder_count = data.get("reminder_count")
        reminder_expire_count = data.get("reminder_expire_count")
        return GetRemindersSuccess(reminders, reminder_count, reminder_expire_count)

    def to_inner_structure(self):
        return {
            "reminders": self.reminders,
            "reminder_count": self.reminder_count,
            "reminder_expire_count": self.reminder_expire_count
        }

class GetEscalationsSuccess(Response):
    def __init__(self, escalations, escalation_count):
        self.escalations = escalations
        self.escalation_count = escalation_count

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["escalations", "escalation_count"])
        escalations = data.get("escalations")
        escalation_count = data.get("escalation_count")
        return GetEscalationsSuccess(escalations)

    def to_inner_structure(self):
        return {
            "escalations": self.escalations,
            "escalation_count": self.escalation_count
        }

class GetMessagesSuccess(Response):
    def __init__(self, messages, messages_count):
        self.messages = messages
        self.messages_count = messages_count

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["messages", "messages_count"])
        messages = data.get("messages")
        messages_count = data.get("messages_count")
        return GetMessagesSuccess(messages, messages_count)

    def to_inner_structure(self):
        return {
            "messages": self.messages,
            "messages_count": self.messages_count
        }

class UpdateNotificationStatusSuccess(Response):
    def __init__(self, notification_details):
        self.notification_details = notification_details

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["notification_details"])
        notification_details = data.get("notification_details")
        return UpdateNotificationStatusSuccess(notification_details)

    def to_inner_structure(self):
        return {
            "notification_details": self.notification_details
        }

class GetStatutorySuccess(Response):
    def __init__(self, statutory, statutory_count):
        self.statutory = statutory
        self.statutory_count = statutory_count

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["statutory", "statutory_count"])
        statutory = data.get("statutory")
        statutory_count = data.get("statutory_count")
        return GetStatutorySuccess(statutory, statutory_count)

    def to_inner_structure(self):
        return {
            "statutory": self.statutory,
            "statutory_count": self.statutory_count
        }

class StatutoryUpdateNotificationStatusSuccess(Response):
    def __init__(self, statutory_notification_details):
        self.statutory_notification_details = statutory_notification_details

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["statutory_notification_details"])
        statutory_notification_details = data.get("statutory_notification_details")
        return StatutoryUpdateNotificationStatusSuccess(statutory_notification_details)

    def to_inner_structure(self):
        return {
            "statutory_notification_details": self.statutory_notification_details
        }


def _init_Response_class_map():
    classes = [
        GetChartFiltersSuccess, GetComplianceStatusChartSuccess,
        GetEscalationsChartSuccess, GetNotCompliedChartSuccess,
        GetTrendChartSuccess,
        GetComplianceApplicabilityStatusChartSuccess,
        GetAssigneeWiseCompliancesChartSuccess,
        GetAssigneeWiseComplianceDrillDownSuccess,
        GetComplianceStatusDrillDownDataSuccess,
        GetEscalationsDrillDownDataSuccess,
        GetComplianceApplicabilityStatusDrillDownSuccess,
        GetNotCompliedDrillDownSuccess,
        GetTrendChartDrillDownDataSuccess,
        GetNotificationsCountSuccess,
        GetRemindersSuccess,
        GetEscalationsSuccess,
        GetMessagesSuccess,
        GetStatutorySuccess,
        UpdateNotificationStatusSuccess,
        StatutoryUpdateNotificationStatusSuccess,
        CheckContractExpirationSuccesss,
        GetAssigneewiseYearwiseCompliancesSuccess
    ]
    class_map = {}
    for c in classes:
        class_map[c.__name__] = c
    return class_map

_Response_class_map = _init_Response_class_map()

#
# RequestFormat
#

class RequestFormat(object):
    def __init__(self, session_token, request):
        self.session_token = session_token
        self.request = request

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["session_token", "request"])
        session_token = data.get("session_token")
        request = data.get("request")
        request = Request.parse_structure(request)
        return RequestFormat(session_token, request)

    def to_structure(self):
        return {
            "session_token": self.session_token,
            "request": Request.to_structure(self.request)
        }

#
# ApplicableDrillDown
#

class ApplicableDrillDown(object):
    def __init__(self, level1_statutory_name, compliances):
        self.level1_statutory_name = level1_statutory_name
        self.compliances = compliances

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["level1_statutory_name", "ap_compliances"])
        level1_statutory_name = data.get("level1_statutory_name")
        compliances = data.get("ap_compliances")
        return ApplicableDrillDown(level1_statutory_name, compliances)

    def to_structure(self):
        return {
            "level1_statutory_name": self.level1_statutory_name,
            "ap_compliances": self.compliances,
        }

#
# DataMap
#

class DataMap(object):
    def __init__(self, filter_name, no_of_compliances):
        self.filter_name = filter_name
        self.no_of_compliances = no_of_compliances

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["filter_name", "no_of_compliances"])
        filter_name = data.get("filter_name")
        filter_name = parse_structure_CustomTextType_100(filter_name)
        no_of_compliances = data.get("no_of_compliances")
        no_of_compliances = parse_structure_VectorType_RecordType_core_NumberOfCompliances(no_of_compliances)
        return DataMap(filter_name, no_of_compliances)

    def to_structure(self):
        return {
            "filter_name": parse_structure_SignedIntegerType_8(self.filter_name),
            "no_of_compliances": to_structure_VectorType_RecordType_core_NumberOfCompliances(self.no_of_compliances),
        }

#
# ChartDataMap
#

class ChartDataMap(object):
    def __init__(self, filter_type_id, data):
        self.filter_type_id = filter_type_id
        self.data = data

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["filter_type_id", "c_data"])
        filter_type_id = data.get("filter_type_id")
        data = data.get("c_data")
        return ChartDataMap(filter_type_id, data)

    def to_structure(self):
        return {
            "filter_type_id": self.filter_type_id,
            "c_data": self.data,
        }

#
# EscalationData
#

class EscalationData(object):
    def __init__(self, year, delayed_compliance_count, not_complied_count):
        self.year = year
        self.delayed_compliance_count = delayed_compliance_count
        self.not_complied_count = not_complied_count

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["chart_year", "delayed_compliance_count", "not_complied_count"])
        year = data.get("chart_year")
        delayed_compliance_count = data.get("delayed_compliance_count")
        not_complied_count = data.get("not_complied_count")
        return EscalationData(year, delayed_compliance_count, not_complied_count)

    def to_structure(self):
        return {
            "chart_year": self.year,
            "delayed_compliance_count": self.delayed_compliance_count,
            "not_complied_count": self.not_complied_count,
        }

#
# CompliedMap
#

class TrendCompliedMap(object):
    def __init__(self, filter_id, year, total_compliances, complied_compliances_count):
        self.filter_id = filter_id
        self.year = year
        self.total_compliances = total_compliances
        self.complied_compliances_count = complied_compliances_count

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["filter_id", "chart_year", "total_compliances", "complied_compliances_count"])
        filter_id = data.get("filter_id")
        year = data.get("chart_year")
        total_compliances = data.get("total_compliances")
        complied_compliances_count = data.get("complied_compliances_count")
        return TrendCompliedMap(filter_id, year, total_compliances, complied_compliances_count)

    def to_structure(self):
        return {
            "filter_id": self.filter_id,
            "chart_year": self.year,
            "total_compliances": self.total_compliances,
            "complied_compliances_count": self.complied_compliances_count,
        }


#
# RessignedCompliance
#

class RessignedCompliance(object):
    def __init__(self, compliance_name, reassigned_from, start_date, due_date, reassigned_date, completed_date):
        self.compliance_name = compliance_name
        self.reassigned_from = reassigned_from
        self.start_date = start_date
        self.due_date = due_date
        self.reassigned_date = reassigned_date
        self.completed_date = completed_date

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["compliance_name", "reassigned_from", "start_date", "due_date", "reassigned_date", "completed_date"])
        compliance_name = data.get("compliance_name")
        reassigned_from = data.get("reassigned_from")
        start_date = data.get("start_date")
        due_date = data.get("due_date")
        reassigned_date = data.get("reassigned_date")
        completed_date = data.get("completed_date")
        return RessignedCompliance(compliance_name, reassigned_from, start_date, due_date, reassigned_date, completed_date)

    def to_structure(self):
        return {
            "compliance_name": self.compliance_name,
            "reassigned_from": self.reassigned_from,
            "start_date": self.start_date,
            "due_date": self.due_date,
            "reassigned_date": self.reassigned_date,
            "completed_date": self.completed_date,
        }

#
# DelayedCompliance
#

class DelayedCompliance(object):
    def __init__(self, assigned_count, reassigned_count, reassigned_compliances):
        self.assigned_count = assigned_count
        self.reassigned_count = reassigned_count
        self.reassigned_compliances = reassigned_compliances

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "assigned_count", "reassigned_count", "reassigned_compliances"
        ])
        assigned_count = data.get("assigned_count")
        reassigned_count = data.get("reassigned_count")
        reassigned_compliances = data.get("reassigned_compliances")
        return DelayedCompliance(assigned_count, reassigned_count, reassigned_compliances)

    def to_structure(self):
        return {
            "assigned_count": self.assigned_count,
            "reassigned_count": self.reassigned_count,
            "reassigned_compliances": self.reassigned_compliances,
        }

#
# DomainWise
#

class DomainWise(object):
    def __init__(
        self, domain_id, domain_name, total_compliances, complied_count,
        assigned_count, reassigned_count, inprogress_compliance_count,
        not_complied_count, rejected_count
    ):
        self.domain_id = domain_id
        self.domain_name = domain_name
        self.total_compliances = total_compliances
        self.complied_count = complied_count
        self.assigned_count = assigned_count
        self.reassigned_count = reassigned_count
        self.inprogress_compliance_count = inprogress_compliance_count
        self.not_complied_count = not_complied_count
        self.rejected_count = rejected_count

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "domain_id", "domain_name",
            "total_compliances", "complied_count", "assigned_count",
            "reassigned_count", "inprogress_compliance_count", "not_complied_count",
            "rejected_count"
        ])
        domain_id = data.get("domain_id")
        domain_name = data.get("domain_name")
        total_compliances = data.get("total_compliances")
        complied_count = data.get("complied_count")
        assigned_count = data.get("assigned_count")
        reassigned_count = data.get("reassigned_count")
        inprogress_compliance_count = data.get("inprogress_compliance_count")
        not_complied_count = data.get("not_complied_count")
        rejected_count = data.get("rejected_count")
        return DomainWise(
            domain_id, domain_name, total_compliances,
            complied_count, assigned_count, reassigned_count,
            inprogress_compliance_count, not_complied_count,
            rejected_count
        )

    def to_structure(self):
        return {
            "domain_id": self.domain_id,
            "domain_name": self.domain_name,
            "total_compliances": self.total_compliances,
            "complied_count": self.complied_count,
            "assigned_count": self.assigned_count,
            "reassigned_count": self.reassigned_count,
            "inprogress_compliance_count": self.inprogress_compliance_count,
            "not_complied_count": self.not_complied_count,
            "rejected_count": self.rejected_count
        }

#
#   Year Wise
#

class YearWise(object):
    def __init__(self, year, total_compliances, complied_count, delayed_compliance, inprogress_compliance_count, not_complied_count):
        self.year = year
        self.total_compliances = total_compliances
        self.complied_count = complied_count
        self.delayed_compliance = delayed_compliance
        self.inprogress_compliance_count = inprogress_compliance_count
        self.not_complied_count = not_complied_count

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
                "year", "total_compliances", "complied_count", "delayed_compliance_count",
                "inprogress_compliance_count", "not_complied_count"
            ]
        )
        year = data.get("year")
        total_compliances = data.get("total_compliances")
        complied_count = data.get("complied_count")
        delayed_compliance = data.get("delayed_compliance_count")
        inprogress_compliance_count = data.get("inprogress_compliance_count")
        not_complied_count = data.get("not_complied_count")
        return YearWise(
            year, total_compliances, complied_count, delayed_compliance,
            inprogress_compliance_count, not_complied_count
        )

    def to_structure(self):
        return {
            "year": self.year,
            "total_compliances": self.total_compliances,
            "complied_count": self.complied_count,
            "delayed_compliance_count": self.delayed_compliance,
            "inprogress_compliance_count": self.inprogress_compliance_count,
            "not_complied_count": self.not_complied_count,
        }

#
# AssigneeWiseDetails
#

class AssigneeWiseDetails(object):
    def __init__(self, user_id, assignee_name, domain_wise_details):
        self.user_id = user_id
        self.assignee_name = assignee_name
        self.domain_wise_details = domain_wise_details

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(
            data, [
                "user_id", "assignee_name", "domain_wise_details"
            ]
        )
        user_id = data.get("user_id")
        assignee_name = data.get("assignee_name")
        domain_wise_details = data.get("domain_wise_details")
        return AssigneeWiseDetails(
            user_id, assignee_name, domain_wise_details
        )

    def to_structure(self):
        return {
            "user_id": self.user_id,
            "assignee_name": self.assignee_name,
            "domain_wise_details": self.domain_wise_details
        }

#
# AssigneeChartData
#

class AssigneeChartData(object):
    def __init__(self, unit_name, unit_id, assignee_wise_details, address):
        self.unit_name = unit_name
        self.unit_id = unit_id
        self.assignee_wise_details = assignee_wise_details
        self.address = address

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["unit_name", "unit_id", "assignee_wise_details", "address"])
        unit_name = data.get("unit_name")
        unit_id = data.get("unit_id")
        assignee_wise_details = data.get("assignee_wise_details")
        address = data.get("address")
        return AssigneeChartData(unit_name, unit_id, assignee_wise_details, address)

    def to_structure(self):
        return {
            "unit_name": self.unit_name,
            "unit_id": self.unit_id,
            "address": self.address,
            "assignee_wise_details": self.assignee_wise_details,
        }



#
# Level1Compliance
#

class Level1Compliance(object):
    def __init__(
        self, compliance_name, description, assignee_name, assigned_date,
        due_date, completion_date, status, ageing
    ):
        self.compliance_name = compliance_name
        self.description = description
        self.assignee_name = assignee_name
        self.assigned_date = assigned_date
        self.due_date = due_date
        self.completion_date = completion_date
        self.status = status
        self.ageing = ageing

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "comp_name", "descp",
            "assignee_name", "assigned_date", "due_date", "completion_date",
            "status", "ageing"
        ])
        compliance_name = data.get("comp_name")
        description = data.get("descp")
        assignee_name = data.get("assignee_name")
        assigned_date = data.get("assigned_date")
        due_date = data.get("due_date")
        completion_date = data.get("completion_date")
        status = data.get("status")
        ageing = data.get("ageing")
        return Level1Compliance(
            compliance_name, description, assignee_name, assigned_date,
            due_date, completion_date,
            status, ageing
        )

    def to_structure(self):
        return {
            "comp_name": self.compliance_name,
            "descp": self.description,
            "assignee_name": self.assignee_name,
            "assigned_date": self.assigned_date,
            "due_date": self.due_date,
            "completion_date": self.completion_date,
            "status": self.status,
            "ageing": self.ageing
        }

#
# AssigneeWiseLevel1Compliance
#

class AssigneeWiseLevel1Compliance(object):
    def __init__(
        self, compliance_name, description, assignee_name, assigned_date,
        due_date, completion_date
    ):
        self.compliance_name = compliance_name
        self.description = description
        self.assignee_name = assignee_name
        self.assigned_date = assigned_date
        self.due_date = due_date
        self.completion_date = completion_date

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "compliance_name", "description",
            "assignee_name", "assigned_date", "due_date", "completion_date",
        ])
        compliance_name = data.get("compliance_name")
        description = data.get("description")
        assignee_name = data.get("assignee_name")
        assigned_date = data.get("assigned_date")
        due_date = data.get("due_date")
        completion_date = data.get("completion_date")
        return AssigneeWiseLevel1Compliance(
            compliance_name, description, assignee_name, assigned_date,
            due_date, completion_date
        )

    def to_structure(self):
        return {
            "compliance_name": self.compliance_name,
            "description": self.description,
            "assignee_name": self.assignee_name,
            "assigned_date": self.assigned_date,
            "due_date": self.due_date,
            "completion_date": self.completion_date
        }

#
# UnitCompliance
#

class UnitCompliance(object):
    def __init__(self, unit_name, address, compliances):
        self.unit_name = unit_name
        self.address = address
        self.compliances = compliances

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["unit_name", "address", "compliances"])
        unit_name = data.get("unit_name")
        unit_name = parse_structure_CustomTextType_100(unit_name)
        address = data.get("address")
        address = parse_structure_CustomTextType_250(address)
        compliances = data.get("compliances")
        compliances = parse_structure_MapType_CustomTextType_500_VectorType_RecordType_dashboard_AssigneeWiseLevel1Compliance(compliances)
        return UnitCompliance(unit_name, address, compliances)

    def to_structure(self):
        return {
            "unit_name": to_structure_CustomTextType_100(self.unit_name),
            "address": to_structure_CustomTextType_250(self.address),
            "compliances": to_structure_MapType_CustomTextType_500_VectorType_RecordType_dashboard_AssigneeWiseLevel1Compliance(self.compliances),
        }

class TrendCompliance(object):
    def __init__(self, compliance_name, description, assignee_name):
        self.compliance_name = compliance_name
        self.description = description
        self.assignee_name = assignee_name

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["comp_name", "descp", "assingee_name"])
        compliance_name = data.get("comp_name")
        description = data.get("descp")
        assignee_name = data.get("assingee_name")
        return TrendCompliance(compliance_name, description, assignee_name)

    def to_structure(self):
        return {
            "comp_name": self.compliance_name,
            "descp": self.description,
            "assignee_name": self.assignee_name,
        }

#
# DrillDownData
#

class DrillDownData(object):
    def __init__(
        self, business_group, legal_entity, division, category,
        unit_name, address, industry_name, compliances
    ):
        self.business_group = business_group
        self.legal_entity = legal_entity
        self.division = division
        self.category = category
        self.unit_name = unit_name
        self.address = address
        self.industry_name = industry_name
        self.compliances = compliances

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "bg_name", "le_name", "div_name", "cat_name",
            "u_name", "address", "indus_name", "drill_compliances"
        ])
        return DrillDownData(
            data.get("bg_name"), data.get("le_name"), data.get("div_name"), data.get("cat_name"),
            data.get("u_name"), data.get("address"), data.get("indus_name"), data.get("drill_compliances"),
        )

    def to_structure(self):
        return {
            "bg_name": self.business_group, "le_name": self.legal_entity, "div_name": self.division, "cat_name": self.category,
            "u_name": self.unit_name, "address": self.address, "indus_name": self.industry_name,
            "drill_compliances": self.compliances,
        }

class NotificationsCountSuccess(object):
    def __init__(self, statutory, reminder, escalation, messages, reminder_expire):
        self.statutory = statutory
        self.reminder = reminder
        self.escalation = escalation
        self.messages = messages
        self.reminder_expire_count = reminder_expire

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["statutory_count", "reminder_count", "escalation_count", "messages_count", "reminder_expire_count"])
        return NotificationsCountSuccess(
            data.get("statutory_count"), data.get("reminder_count"), data.get("escalation_count"), 
            data.get("messages_count"), data.get("reminder_expire_count")
        )

    def to_structure(self):
        return {
            "statutory_count": self.statutory, "reminder_count": self.reminder,
            "escalation_count": self.escalation, "messages_count": self.messages, "reminder_expire_count": self.reminder_expire_count
        }

class RemindersSuccess(object):
    def __init__(self, legal_entity_id, notification_id, notification_text, extra_details, created_on):
        self.legal_entity_id = legal_entity_id
        self.notification_id = notification_id
        self.notification_text = notification_text
        self.extra_details = extra_details
        self.created_on = created_on

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["le_id", "notification_id", "notification_text", "extra_details" "created_on"])
        return RemindersSuccess(
            data.get("le_id"), data.get("notification_id"), data.get("notification_text"),
            data.get("extra_details"), data.get("created_on"),
        )

    def to_structure(self):
        return {
            "le_id" : self.legal_entity_id, "notification_id" : self.notification_id,
            "notification_text" : self.notification_text, "extra_details" : self.extra_details, "created_on" : self.created_on,
        }

class EscalationsSuccess(object):
    def __init__(self, legal_entity_id, notification_id, notification_text, extra_details, created_on):
        self.legal_entity_id = legal_entity_id
        self.notification_id = notification_id
        self.notification_text = notification_text
        self.extra_details = extra_details
        self.created_on = created_on

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["le_id", "notification_id", "notification_text", "extra_details", "created_on"])
        return EscalationsSuccess(
            data.get("le_id"), data.get("notification_id"), data.get("notification_text"),
            data.get("extra_details"), data.get("created_on"),
        )

    def to_structure(self):
        return {
            "le_id" : self.legal_entity_id, "notification_id" : self.notification_id,
            "notification_text" : self.notification_text, "extra_details" : self.extra_details, "created_on" : self.created_on,
        }

class MessagesSuccess(object):
    def __init__(self, legal_entity_id, notification_id, notification_text, extra_details, created_on):
        self.legal_entity_id = legal_entity_id
        self.notification_id = notification_id
        self.notification_text = notification_text
        self.extra_details = extra_details
        self.created_on = created_on

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["le_id", "notification_id", "notification_text", "extra_details", "created_on"])
        return MessagesSuccess(
            data.get("le_id"), data.get("notification_id"), data.get("notification_text"),
            data.get("extra_details"), data.get("created_on"),
        )

    def to_structure(self):
        return {
            "le_id" : self.legal_entity_id, "notification_id" : self.notification_id,
            "notification_text" : self.notification_text, "extra_details" : self.extra_details, "created_on" : self.created_on,
        }

class StatutorySuccess(object):
    def __init__(self, notification_id, compliance_id, notification_text, user_name, created_on):
        self.notification_id = notification_id
        self.compliance_id = compliance_id
        self.notification_text = notification_text
        self.user_name = user_name
        self.created_on = created_on

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["le_id", "notification_id", "compliance_id", "notification_text", "user_name", "created_on"])
        return StatutorySuccess(
            data.get("notification_id"), data.get("compliance_id"),  data.get("notification_text"),
            data.get("user_name"),  data.get("created_on")
        )

    def to_structure(self):
        return {
            "notification_id" : self.notification_id, "compliance_id" : self.compliance_id,
            "notification_text" : self.notification_text, "user_name" : self.user_name,
            "created_on" : self.created_on,
        }

class NotificationDetailsSuccess(object):
    def __init__(self, notification_id, act_name, unit, compliance_name, due_date, delayed_by, assignee_name, concurrer_name, approver_name):
        self.notification_id = notification_id
        self.act_name = act_name
        self.unit = unit
        self.compliance_name = compliance_name
        self.due_date = due_date
        self.delayed_by = delayed_by
        self.assignee_name = assignee_name
        self.concurrer_name = concurrer_name
        self.approver_name = approver_name

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["notification_id", "act_name", "unit", "compliance_name", "due_date", "delayed_by", "assignee_name", "concurrer_name", "approver_name"])
        return NotificationDetailsSuccess(
            data.get("notification_id"), data.get("act_name"), data.get("unit"), data.get("compliance_name"),
            data.get("due_date"), data.get("delayed_by"), data.get("assignee_name"), data.get("concurrer_name"), data.get("approver_name"),
        )

    def to_structure(self):
        return {
            "notification_id" : self.notification_id, "act_name" : self.act_name, "unit" : self.unit,
            "compliance_name" : self.compliance_name, "due_date" : self.due_date, "delayed_by" : self.delayed_by,
            "assignee_name" : self.assignee_name, "concurrer_name" : self.concurrer_name, "approver_name" : self.approver_name
        }

class StatutoryNotificationDetailsSuccess(object):
    def __init__(self, compliance_id, statutory_provision, compliance_task, compliance_description, penal_consequences, freq_name, summary, reference_link):
        self.compliance_id = compliance_id
        self.statutory_provision = statutory_provision
        self.compliance_task = compliance_task
        self.compliance_description = compliance_description
        self.penal_consequences = penal_consequences
        self.freq_name = freq_name
        self.summary = summary
        self.reference_link = reference_link

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["compliance_id", "statutory_provision", "compliance_task", "compliance_description", "penal_consequences", "freq_name", "summary", "reference_link"])
        return StatutoryNotificationDetailsSuccess(
            data.get("compliance_id"), data.get("statutory_provision"), data.get("compliance_task"),
            data.get("compliance_description"), data.get("penal_consequences"), data.get("freq_name"),
            data.get("summary"), data.get("reference_link"),
        )

    def to_structure(self):
        return {
            "compliance_id" : self.compliance_id, "statutory_provision" : self.statutory_provision,
            "compliance_task" : self.compliance_task, "compliance_description" : self.compliance_description,
            "penal_consequences" : self.penal_consequences, "freq_name" : self.freq_name,
            "summary" : self.summary, "reference_link" : self.reference_link
        }

#
# Trend DrillDownData
#

class TrendDrillDownData(object):
    def __init__(
        self, business_group, legal_entity, division, category, unit_name,
        address, compliances
    ):
        self.business_group = business_group
        self.legal_entity = legal_entity
        self.division = division
        self.category = category
        self.unit_name = unit_name
        self.address = address
        self.compliances = compliances

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "bg_name", "le_name", "div_name", "cat_name", "u_name", "address", "t_compliances"
        ])
        return TrendDrillDownData(
            data.get("bg_name"), data.get("le_name"), data.get("div_name"), data.get("cat_name"),
            data.get("u_name"), data.get("address"), data.get("t_compliances"),
        )

    def to_structure(self):
        return {
            "bg_name": self.business_group, "le_name": self.legal_entity,
            "div_name": self.division, "cat_name": self.category,
            "u_name": self.unit_name, "address": self.address, "t_compliances": self.compliances,
        }


class DomainWiseYearConfiguration(object):
    def __init__(self, country_name, domain_name, period_from, period_to):
        self.country_name = country_name
        self.domain_name = domain_name
        self.period_from = period_from
        self.period_to = period_to

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["c_name", "d_name", "m_name_from", "m_name_to"])
        return DomainWiseYearConfiguration(
            data.get("c_name"), data.get("d_name"), data.get("m_name_from"), data.get("m_name_to"),
        )

    def to_structure(self):
        return {
            "c_name": self.country_name, "d_name": self.domain_name,
            "m_name_from": self.period_from, "m_name_to": self.period_to
        }

class Compliance(object):
    def __init__(
        self, compliance_id, statutory_provision,
        compliance_task, description, document_name,
        format_file_list, penal_consequences,
        frequency, statutory_dates,
        is_active, download_url, summary
    ):
        self.compliance_id = compliance_id
        self.statutory_provision = statutory_provision
        self.compliance_task = compliance_task
        self.description = description
        self.document_name = document_name
        self.format_file_list = format_file_list
        self.penal_consequences = penal_consequences
        self.frequency = frequency
        self.statutory_dates = statutory_dates
        self.is_active = is_active
        self.download_url = download_url
        self.summary = summary

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "comp_id", "s_prov", "comp_name", "descp", "doc_name", "format_file_list",
            "p_cons", "frequency", "statu_dates", "is_active", "download_url_list", "summary"
        ])
        return Compliance(
            data.get("comp_id"), data.get("s_prov"), data.get("comp_name"), data.get("descp"),
            data.get("doc_name"), data.get("format_file_list"), data.get("p_cons"), data.get("frequency"),
            data.get("statu_dates"), data.get("is_active"), data.get("download_url_list"), data.get("summary"),
        )

    def to_structure(self):
        return {
            "comp_id": self.compliance_id, "s_prov": self.statutory_provision,
            "comp_name": self.compliance_task, "descp": self.description,
            "doc_name": self.document_name, "format_file_list": self.format_file_list,
            "p_cons": self.penal_consequences, "frequency": self.frequency,
            "statu_dates": self.statutory_dates, "is_active": self.is_active,
            "download_url_list": self.download_url, "summary": self.summary,
        }


class ClientLegalEntityInfo(object):
    def __init__(
        self, legal_entity_id, legal_entity_name, business_group_id, domain_ids
    ):
        self.legal_entity_id = legal_entity_id
        self.legal_entity_name = legal_entity_name
        self.business_group_id = business_group_id
        self.domain_ids = domain_ids

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["le_id", "le_name", "bg_id"])
        return ClientLegalEntityInfo(
            data.get("le_id"), data.get("le_name"), data.get("bg_id"), data.get("d_ids"),
        )

    def to_structure(self):
        data = {
            "le_id": self.legal_entity_id, "le_name": self.legal_entity_name,
            "bg_id": self.business_group_id, "d_ids": self.domain_ids
        }
        return to_structure_dictionary_values(data)
