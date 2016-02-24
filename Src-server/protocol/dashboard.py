import json
from protocol.jsonvalidators import (parse_enum, parse_dictionary, parse_static_list)
from protocol.parse_structure import (
    parse_structure_VectorType_RecordType_core_Compliance,
    parse_structure_VectorType_RecordType_dashboard_CompliedMap,
    parse_structure_VariantType_dashboard_Request,
    parse_structure_VectorType_RecordType_dashboard_AssigneeWiseDetails,
    parse_structure_UnsignedIntegerType_32,
    parse_structure_VectorType_RecordType_dashboard_ChartDataMap,
    parse_structure_MapType_CustomTextType_50_VectorType_RecordType_dashboard_Level1Compliance,
    parse_structure_VectorType_RecordType_core_BusinessGroup,
    parse_structure_EnumType_core_FILTER_TYPE,
    parse_structure_CustomTextType_500,
    parse_structure_VectorType_RecordType_core_Country,
    parse_structure_VectorType_RecordType_dashboard_ApplicableDrillDown,
    parse_structure_CustomTextType_50,
    parse_structure_EnumType_core_COMPLIANCE_STATUS,
    parse_structure_CustomTextType_100,
    parse_structure_EnumType_core_APPLICABILITY_STATUS,
    parse_structure_VectorType_SignedIntegerType_8,
    parse_structure_VectorType_RecordType_core_Unit,
    parse_structure_VectorType_RecordType_dashboard_DataMap,
    parse_structure_VectorType_RecordType_core_Division,
    parse_structure_RecordType_dashboard_DelayedCompliance,
    parse_structure_VectorType_RecordType_dashboard_DomainWise,
    parse_structure_VectorType_RecordType_dashboard_RessignedCompliance,
    parse_structure_CustomTextType_250, parse_structure_Text,
    parse_structure_VectorType_RecordType_core_LegalEntity,
    parse_structure_VectorType_RecordType_core_Domain,
    parse_structure_VectorType_RecordType_dashboard_DrillDownData,
    parse_structure_VectorType_RecordType_dashboard_TrendData,
    parse_structure_CustomTextType_20,
    parse_structure_VectorType_RecordType_dashboard_AssigneeChartData,
    parse_structure_VectorType_RecordType_dashboard_UnitCompliance,
    parse_structure_VectorType_RecordType_dashboard_EscalationData,
    parse_structure_VectorType_RecordType_core_ClientBusinessGroup,
    parse_structure_VectorType_RecordType_core_ClientLegalEntity,
    parse_structure_VectorType_RecordType_core_ClientDivision,
    parse_structure_VectorType_RecordType_clienttransactions_ASSIGN_COMPLIANCE_UNITS,
    parse_structure_VectorType_RecordType_core_NumberOfCompliances,
    parse_structure_OptionalType_VectorType_SignedIntegerType_8,
    parse_structure_OptionalType_Text,
    parse_structure_MapType_SignedIntegerType_8_VectorType_RecordType_core_NumberOfCompliances,
    parse_structure_VectorType_UnsignedIntegerType_32,
    parse_structure_OptionalType_VectorType_UnsignedIntegerType_32,
    parse_structure_SignedIntegerType_8,
    parse_structure_VectorType_RecordType_dashboard_TrendCompliance,
    parse_structure_MapType_CustomTextType_100_VectorType_RecordType_dashboard_TrendCompliance,
    parse_structure_VectorType_RecordType_dashboard_TrendDrillDownData,
    parse_structure_OptionalType_UnsignedIntegerType_32,
    parse_structure_EnumType_core_NOT_COMPLIED_TYPE,
    parse_structure_MapType_SignedIntegerType_8_VectorType_RecordType_core_Compliance,
    parse_structure_VectorType_RecordType_dashboard_Notification,
    parse_structure_Bool,
    parse_structure_OptionalType_VectorType_RecordType_dashboard_RessignedCompliance,
    parse_structure_MapType_CustomTextType_50_VectorType_RecordType_dashboard_AssigneeWiseLevel1Compliance
)
from protocol.to_structure import (
    to_structure_VectorType_RecordType_core_Compliance,
    to_structure_VectorType_RecordType_dashboard_CompliedMap,
    to_structure_VariantType_dashboard_Request,
    to_structure_VectorType_RecordType_dashboard_AssigneeWiseDetails,
    to_structure_SignedIntegerType_8,
    to_structure_VectorType_RecordType_dashboard_ChartDataMap,
    to_structure_MapType_CustomTextType_50_VectorType_RecordType_dashboard_Level1Compliance,
    to_structure_VectorType_RecordType_core_BusinessGroup,
    to_structure_EnumType_core_FILTER_TYPE,
    to_structure_CustomTextType_500,
    to_structure_VectorType_RecordType_core_Country,
    to_structure_VectorType_RecordType_dashboard_ApplicableDrillDown,
    to_structure_CustomTextType_50,
    to_structure_EnumType_core_COMPLIANCE_STATUS,
    to_structure_CustomTextType_100,
    to_structure_EnumType_core_APPLICABILITY_STATUS,
    to_structure_VectorType_SignedIntegerType_8,
    to_structure_VectorType_RecordType_core_Unit,
    to_structure_VectorType_RecordType_dashboard_DataMap,
    to_structure_VectorType_RecordType_core_Division,
    to_structure_RecordType_dashboard_DelayedCompliance,
    to_structure_VectorType_RecordType_dashboard_DomainWise,
    to_structure_VectorType_RecordType_dashboard_RessignedCompliance,
    to_structure_CustomTextType_250, to_structure_Text,
    to_structure_VectorType_RecordType_core_LegalEntity,
    to_structure_VectorType_RecordType_core_Domain,
    to_structure_VectorType_RecordType_dashboard_DrillDownData,
    to_structure_VectorType_RecordType_dashboard_TrendData,
    to_structure_CustomTextType_20,
    to_structure_VectorType_RecordType_dashboard_AssigneeChartData,
    to_structure_VectorType_RecordType_dashboard_UnitCompliance,
    to_structure_VectorType_RecordType_dashboard_EscalationData,
    to_structure_VectorType_RecordType_core_ClientBusinessGroup,
    to_structure_VectorType_RecordType_core_ClientLegalEntity,
    to_structure_VectorType_RecordType_core_ClientDivision,
    to_structure_VectorType_RecordType_clienttransactions_ASSIGN_COMPLIANCE_UNITS,
    to_structure_VectorType_RecordType_core_NumberOfCompliances,
    to_structure_OptionalType_VectorType_SignedIntegerType_8,
    to_structure_OptionalType_Text,
    to_structure_MapType_SignedIntegerType_8_VectorType_RecordType_core_NumberOfCompliances,
    to_structure_VectorType_UnsignedIntegerType_32,
    to_structure_OptionalType_VectorType_UnsignedIntegerType_32,
    to_structure_UnsignedIntegerType_32,
    to_structure_VectorType_RecordType_dashboard_TrendCompliance,
    to_structure_MapType_CustomTextType_100_VectorType_RecordType_dashboard_TrendCompliance,
    to_structure_VectorType_RecordType_dashboard_TrendDrillDownData,
    to_structure_OptionalType_UnsignedIntegerType_32,
    to_structure_EnumType_core_NOT_COMPLIED_TYPE,
    to_structure_MapType_SignedIntegerType_8_VectorType_RecordType_core_Compliance,
    to_structure_VectorType_RecordType_dashboard_Notification,
    to_structure_Bool,
    to_structure_VectorType_RecordType_core_ClientUnit,
    to_structure_VectorType_RecordType_clientreport_User,
    to_structure_OptionalType_VectorType_RecordType_dashboard_RessignedCompliance,
    to_structure_MapType_CustomTextType_50_VectorType_RecordType_dashboard_AssigneeWiseLevel1Compliance
)

#
# Request
#

class Request(object):
    def to_structure(self):
        name = type(self).__name__
        inner = self.to_inner_structure()
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

class GetComplianceStatusChart(Request):
    def __init__(
        self,
        country_ids, domain_ids,
        filter_type, filter_ids,
        from_date, to_date,
        chart_year
    ):
        self.country_ids = country_ids
        self.domain_ids = domain_ids
        self.filter_type = filter_type
        self.filter_ids = filter_ids
        self.from_date = from_date
        self.to_date = to_date
        self.chart_year = chart_year

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "country_ids", "domain_ids",
            "filter_type", "filter_ids",
            "from_date", "to_date",
            "chart_year"
        ])
        country_ids = data.get("country_ids")
        country_ids = parse_structure_VectorType_SignedIntegerType_8(country_ids)
        domain_ids = data.get("domain_ids")
        domain_ids = parse_structure_VectorType_SignedIntegerType_8(domain_ids)
        filter_type = data.get("filter_type")
        filter_type = parse_structure_EnumType_core_FILTER_TYPE(filter_type)
        filter_ids = data.get("filter_ids")
        filter_ids = parse_structure_OptionalType_VectorType_UnsignedIntegerType_32(filter_ids)
        from_date = data.get("from_date")
        from_date = parse_structure_OptionalType_Text(from_date)
        to_date = data.get("to_date")
        to_date = parse_structure_OptionalType_Text(to_date)
        chart_year = data.get("chart_year")
        chart_year = parse_structure_UnsignedIntegerType_32(chart_year)
        return GetComplianceStatusChart(
            country_ids, domain_ids,
            filter_type, filter_ids,
            from_date, to_date,
            chart_year
        )

    def to_inner_structure(self):
        return {
            "country_ids": to_structure_VectorType_SignedIntegerType_8(self.country_ids),
            "domain_ids": to_structure_VectorType_SignedIntegerType_8(self.domain_ids),
            "filter_type": to_structure_EnumType_core_FILTER_TYPE(self.filter_type),
            "filter_ids": to_structure_OptionalType_VectorType_UnsignedIntegerType_32(self.filter_ids),
            "from_date": to_structure_OptionalType_Text(self.from_date),
            "to_date": to_structure_OptionalType_Text(self.to_date),
            "chart_year": to_structure_UnsignedIntegerType_32(self.chart_year)
        }

class GetEscalationsChart(Request):
    def __init__(self, country_ids, domain_ids, filter_type, filter_id):
        self.country_ids = country_ids
        self.domain_ids = domain_ids
        self.filter_type = filter_type
        self.filter_id = filter_id

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["country_ids", "domain_ids", "filter_type", "filter_id"])
        country_ids = data.get("country_ids")
        country_ids = parse_structure_VectorType_SignedIntegerType_8(country_ids)
        domain_ids = data.get("domain_ids")
        domain_ids = parse_structure_VectorType_SignedIntegerType_8(domain_ids)
        filter_type = data.get("filter_type")
        filter_type = parse_structure_EnumType_core_FILTER_TYPE(filter_type)
        filter_id = data.get("filter_id")
        filter_id = parse_structure_UnsignedIntegerType_32(filter_id)
        return GetEscalationsChart(country_ids, domain_ids, filter_type, filter_id)

    def to_inner_structure(self):
        return {
            "country_ids": to_structure_VectorType_SignedIntegerType_8(self.country_ids),
            "domain_ids": to_structure_VectorType_SignedIntegerType_8(self.domain_ids),
            "filter_type": to_structure_EnumType_core_FILTER_TYPE(self.filter_type),
            "filter_id": to_structure_SignedIntegerType_8(self.filter_id),
        }

class GetNotCompliedChart(Request):
    def __init__(self, country_ids, domain_ids, filter_type, filter_id):
        self.country_ids = country_ids
        self.domain_ids = domain_ids
        self.filter_type = filter_type
        self.filter_id = filter_id

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["country_ids", "domain_ids", "filter_type", "filter_id"])
        country_ids = data.get("country_ids")
        country_ids = parse_structure_VectorType_SignedIntegerType_8(country_ids)
        domain_ids = data.get("domain_ids")
        domain_ids = parse_structure_VectorType_SignedIntegerType_8(domain_ids)
        filter_type = data.get("filter_type")
        filter_type = parse_structure_EnumType_core_FILTER_TYPE(filter_type)
        filter_id = data.get("filter_id")
        filter_id = parse_structure_UnsignedIntegerType_32(filter_id)
        return GetNotCompliedChart(country_ids, domain_ids, filter_type, filter_id)

    def to_inner_structure(self):
        return {
            "country_ids": to_structure_VectorType_SignedIntegerType_8(self.country_ids),
            "domain_ids": to_structure_VectorType_SignedIntegerType_8(self.domain_ids),
            "filter_type": to_structure_EnumType_core_FILTER_TYPE(self.filter_type),
            "filter_id": to_structure_SignedIntegerType_8(self.filter_id),
        }


class GetTrendChart(Request):
    def __init__(self, country_ids, domain_ids,filter_type, filter_ids):
        self.country_ids = country_ids
        self.domain_ids = domain_ids
        self.filter_type = filter_type
        self.filter_ids = filter_ids

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["country_ids", "domain_ids", "filter_type", "filter_ids"])
        country_ids = data.get("country_ids")
        country_ids = parse_structure_VectorType_UnsignedIntegerType_32(country_ids)
        domain_ids = data.get("domain_ids")
        domain_ids = parse_structure_VectorType_UnsignedIntegerType_32(domain_ids)
        filter_type = data.get("filter_type")
        filter_type = parse_structure_EnumType_core_FILTER_TYPE(filter_type)
        filter_ids = data.get("filter_ids")
        filter_ids = parse_structure_OptionalType_VectorType_UnsignedIntegerType_32(filter_ids)
        return GetTrendChart(country_ids, domain_ids, filter_type, filter_ids)

    def to_inner_structure(self):
        return {
            "country_ids": to_structure_VectorType_UnsignedIntegerType_32(self.country_ids),
            "domain_ids": to_structure_VectorType_UnsignedIntegerType_32(self.domain_ids),
            "filter_type": to_structure_EnumType_core_FILTER_TYPE(self.filter_type),
            "filter_ids": to_structure_OptionalType_VectorType_UnsignedIntegerType_32(self.filter_ids),
        }

class GetComplianceApplicabilityStatusChart(Request):
    def __init__(self, country_ids, domain_ids, filter_type, filter_id):
        self.country_ids = country_ids
        self.domain_ids = domain_ids
        self.filter_type = filter_type
        self.filter_id = filter_id

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["country_ids", "domain_ids", "filter_type", "filter_id"])
        country_ids = data.get("country_ids")
        country_ids = parse_structure_VectorType_SignedIntegerType_8(country_ids)
        domain_ids = data.get("domain_ids")
        domain_ids = parse_structure_VectorType_SignedIntegerType_8(domain_ids)
        filter_type = data.get("filter_type")
        filter_type = parse_structure_EnumType_core_FILTER_TYPE(filter_type)
        filter_id = data.get("filter_ids")
        filter_id = parse_structure_OptionalType_UnsignedIntegerType_32(filter_id)
        return GetComplianceApplicabilityStatusChart(country_ids, domain_ids, filter_type, filter_id)

    def to_inner_structure(self):
        return {
            "country_ids": to_structure_VectorType_SignedIntegerType_8(self.country_ids),
            "domain_ids": to_structure_VectorType_SignedIntegerType_8(self.domain_ids),
            "filter_type": to_structure_EnumType_core_FILTER_TYPE(self.filter_type),
            "filter_id": to_structure_OptionalType_UnsignedIntegerType_32(self.filter_id),
        }

class GetAssigneewiseComplianesFilters(Request):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return GetAssigneewiseComplianesFilters()

    def to_inner_structure(self):
        return {
        }

class GetAssigneeWiseCompliancesChart(Request):
    def __init__(
        self, country_id, business_group_id, legal_entity_id, division_id, 
        unit_id, user_id
    ):
        self.country_id = country_id
        self.business_group_id = business_group_id
        self.legal_entity_id = legal_entity_id
        self.division_id = division_id
        self.unit_id = unit_id
        self.user_id = user_id

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(
            data, [
                "country_id", "business_group_id", "legal_entity_id", "division_id", 
                "unit_id", "user_id"
            ]
        )
        country_id = data.get("country_id")
        country_id = parse_structure_UnsignedIntegerType_32(country_id)
        business_group_id = data.get("business_group_id")
        business_group_id = parse_structure_OptionalType_UnsignedIntegerType_32(business_group_id)
        legal_entity_id = data.get("legal_entity_id")
        legal_entity_id = parse_structure_OptionalType_UnsignedIntegerType_32(legal_entity_id)
        division_id = data.get("division_id")
        division_id = parse_structure_OptionalType_UnsignedIntegerType_32(division_id)
        unit_id = data.get("unit_id")
        unit_id = parse_structure_OptionalType_UnsignedIntegerType_32(unit_id)
        user_id = data.get("user_id")
        user_id = parse_structure_OptionalType_UnsignedIntegerType_32(user_id)
        return GetAssigneeWiseCompliancesChart(
            country_id, business_group_id, legal_entity_id, division_id, 
            unit_id, user_id
        )

    def to_inner_structure(self):
        return {
            "country_id": to_structure_SignedIntegerType_8(self.country_id),
            "business_group_id": to_structure_OptionalType_UnsignedIntegerType_32(self.business_group_id),
            "legal_entity_id": to_structure_OptionalType_UnsignedIntegerType_32(self.legal_entity_id),
            "division_id": to_structure_OptionalType_UnsignedIntegerType_32(self.division_id),
            "unit_id": to_structure_OptionalType_UnsignedIntegerType_32(self.unit_id),
            "user_id": to_structure_OptionalType_UnsignedIntegerType_32(self.user_id)
        }

class GetAssigneeWiseComplianceDrillDown(Request):
    def __init__(self, assignee_id, domain_id):
        self.assignee_id = assignee_id
        self.domain_id = domain_id

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["assignee_id", "domain_id"])
        assignee_id = data.get("assignee_id")
        assignee_id = parse_structure_UnsignedIntegerType_32(assignee_id)
        domain_id = data.get("domain_id")
        domain_id = parse_structure_UnsignedIntegerType_32(domain_id)
        return GetAssigneeWiseComplianceDrillDown(assignee_id, domain_id)

    def to_inner_structure(self):
        return {
            "assignee_id": to_structure_SignedIntegerType_8(self.assignee_id),
            "domain_id": to_structure_SignedIntegerType_8(self.domain_id),
        }

class GetComplianceStatusDrillDownData(Request):
    def __init__(self, domain_ids, from_date, to_date, year, filter_type, filter_id, compliance_status):
        self.domain_ids = domain_ids
        self.from_date = from_date
        self.to_date = to_date
        self.year = year
        self.filter_type = filter_type
        self.filter_id = filter_id
        self.compliance_status = compliance_status

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["domain_ids", "from_date", "to_date", "year",  "filter_type", "filter_id", "compliance_status"])
        domain_ids = data.get("domain_ids")
        domain_ids = parse_structure_VectorType_SignedIntegerType_8(domain_ids)
        from_date = data.get("from_date")
        from_date = parse_structure_OptionalType_Text(from_date)
        to_date = data.get("to_date")
        to_date = parse_structure_OptionalType_Text(to_date)
        year = data.get("year")
        year = parse_structure_UnsignedIntegerType_32(year)
        filter_type = data.get("filter_type")
        filter_type = parse_structure_EnumType_core_FILTER_TYPE(filter_type)
        filter_id = data.get("filter_id")
        filter_id = parse_structure_UnsignedIntegerType_32(filter_id)
        compliance_status = data.get("compliance_status")
        compliance_status = parse_structure_EnumType_core_COMPLIANCE_STATUS(compliance_status)
        return GetComplianceStatusDrillDownData(
            domain_ids, from_date, to_date,
            year, filter_type, filter_id,
            compliance_status
        )

    def to_inner_structure(self):
        return {
            "domain_ids": to_structure_VectorType_SignedIntegerType_8(self.domain_ids),
            "from_date": to_structure_OptionalType_Text(self.from_date),
            "to_date": to_structure_OptionalType_Text(self.to_date),
            "year": parse_structure_UnsignedIntegerType_32(self.year),
            "filter_type": to_structure_EnumType_core_FILTER_TYPE(self.filter_type),
            "filter_id": to_structure_SignedIntegerType_8(self.filter_id),
            "compliance_status": to_structure_EnumType_core_COMPLIANCE_STATUS(self.compliance_status),
        }

class GetEscalationsDrillDownData(Request):
    def __init__(self, domain_ids, filter_type, filter_ids, year):
        self.domain_ids = domain_ids
        self.filter_type = filter_type
        self.filter_ids = filter_ids
        self.year = year

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["domain_ids", "filter_type", "filter_ids", "year"])
        domain_ids = data.get("domain_ids")
        domain_ids = parse_structure_VectorType_SignedIntegerType_8(domain_ids)
        filter_type = data.get("filter_type")
        filter_type = parse_structure_EnumType_core_FILTER_TYPE(filter_type)
        filter_ids = data.get("filter_ids")
        filter_ids = parse_structure_VectorType_SignedIntegerType_8(filter_ids)
        year = data.get("year")
        year = parse_structure_UnsignedIntegerType_32(year)
        return GetEscalationsDrillDownData(domain_ids, filter_type, filter_ids, year)

    def to_inner_structure(self):
        return {
            "domain_ids": to_structure_VectorType_SignedIntegerType_8(self.domain_ids),
            "filter_type": to_structure_EnumType_core_FILTER_TYPE(self.filter_type),
            "filter_ids": to_structure_VectorType_SignedIntegerType_8(self.filter_ids),
            "year": to_structure_SignedIntegerType_8(self.year),
        }

class GetComplianceApplicabilityStatusDrillDown(Request):
    def __init__(self, country_ids, domain_ids, filter_type, filter_id, applicability_status):
        self.country_ids = country_ids
        self.domain_ids = domain_ids
        self.filter_type = filter_type
        self.filter_id = filter_id
        self.applicability_status = applicability_status

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["country_ids", "domain_ids", "filter_type", "filter_id", "applicability_status"])
        country_ids = data.get("country_ids")
        country_ids = parse_structure_VectorType_SignedIntegerType_8(country_ids)
        domain_ids = data.get("domain_ids")
        domain_ids = parse_structure_VectorType_SignedIntegerType_8(domain_ids)
        filter_type = data.get("filter_type")
        filter_type = parse_structure_EnumType_core_FILTER_TYPE(filter_type)
        filter_id = data.get("filter_id")
        filter_id = parse_structure_OptionalType_UnsignedIntegerType_32(filter_id)
        applicability_status = data.get("applicability_status")
        applicability_status = parse_structure_EnumType_core_APPLICABILITY_STATUS(applicability_status)
        return GetComplianceApplicabilityStatusDrillDown(country_ids, domain_ids, filter_type, filter_id, applicability_status)

    def to_inner_structure(self):
        return {
            "country_ids": to_structure_VectorType_SignedIntegerType_8(self.country_ids),
            "domain_ids": to_structure_VectorType_SignedIntegerType_8(self.domain_ids),
            "filter_type": to_structure_EnumType_core_FILTER_TYPE(self.filter_type),
            "filter_id": to_structure_OptionalType_UnsignedIntegerType_32(self.filter_id),
            "applicability_status": to_structure_EnumType_core_APPLICABILITY_STATUS(self.applicability_status),
        }

class GetNotCompliedDrillDown(Request):
    def __init__(self, domain_ids,  filter_type, filter_ids, not_complied_type, year):
        self.domain_ids = domain_ids
        self.filter_type = filter_type
        self.filter_ids = filter_ids
        self.not_complied_type = not_complied_type
        self.year = year

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["domain_ids", "filter_type", "filter_ids", "not_complied_type", "year"])
        domain_ids = data.get("domain_ids")
        domain_ids = parse_structure_VectorType_SignedIntegerType_8(domain_ids)
        filter_type = data.get("filter_type")
        filter_type = parse_structure_EnumType_core_FILTER_TYPE(filter_type)
        filter_ids = data.get("filter_ids")
        filter_ids = parse_structure_VectorType_SignedIntegerType_8(filter_ids)
        not_complied_type = data.get("not_complied_type")
        not_complied_type = parse_structure_EnumType_core_NOT_COMPLIED_TYPE(not_complied_type)
        year = data.get("year")
        year = parse_structure_UnsignedIntegerType_32(year)
        return GetNotCompliedDrillDown(domain_ids, filter_type, filter_ids, not_complied_type, year)

    def to_inner_structure(self):
        return {
            "domain_ids": to_structure_VectorType_SignedIntegerType_8(self.domain_ids),
            "filter_type": to_structure_EnumType_core_FILTER_TYPE(self.filter_type),
            "filter_ids": to_structure_VectorType_SignedIntegerType_8(self.filter_ids),
            "not_complied_type": to_structure_EnumType_core_NOT_COMPLIED_TYPE(self.not_complied_type),
            "year": to_structure_UnsignedIntegerType_32(self.year)
        }

class GetTrendChartDrillDownData(Request):
    def __init__(self, filter_type, filter_ids, country_ids, domain_ids, year):
        self.filter_type = filter_type
        self.filter_ids = filter_ids
        self.country_ids = country_ids
        self.domain_ids = domain_ids
        self.year = year

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["filter_type", "filter_ids", "country_ids", "domain_ids", "year"])
        filter_type = data.get("filter_type")
        filter_type = parse_structure_EnumType_core_FILTER_TYPE(filter_type)
        filter_ids = data.get("filter_ids")
        filter_ids = parse_structure_OptionalType_VectorType_UnsignedIntegerType_32(filter_ids)
        country_ids = data.get("country_ids")
        country_ids = parse_structure_VectorType_SignedIntegerType_8(country_ids)
        domain_ids = data.get("domain_ids")
        domain_ids = parse_structure_VectorType_SignedIntegerType_8(domain_ids)
        year = data.get("year")
        year = parse_structure_UnsignedIntegerType_32(year)
        return GetTrendChartDrillDownData(filter_type, filter_ids,
            country_ids, domain_ids, year)

    def to_inner_structure(self):
        return {
            "filter_type": to_structure_EnumType_core_FILTER_TYPE(self.filter_type),
            "filter_ids": to_structure_OptionalType_VectorType_UnsignedIntegerType_32(self.filter_ids),
            "country_ids": to_structure_VectorType_SignedIntegerType_8(self.country_ids),
            "domain_ids": to_structure_VectorType_SignedIntegerType_8(self.domain_ids),
            "year": to_structure_UnsignedIntegerType_32(self.year)
        }

class GetNotifications(Request):
    def __init__(self, notification_type):
        self.notification_type = notification_type

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["notification_type"])
        notification_type = data.get("notification_type")
        notification_type = parse_structure_CustomTextType_20(notification_type)
        return GetNotifications(notification_type)

    def to_inner_structure(self):
        return {
            "notification_type": to_structure_CustomTextType_20(self.notification_type),
        }

class UpdateNotificationStatus(Request):
    def __init__(self, notification_id, has_read):
        self.notification_id = notification_id
        self.has_read = has_read

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["notification_id", "has_read"])
        notification_id = data.get("notification_id")
        notification_id = parse_structure_UnsignedIntegerType_32(notification_id)
        has_read = data.get("has_read")
        has_read = parse_structure_Bool(has_read)
        return UpdateNotificationStatus(notification_id, has_read)

    def to_inner_structure(self):
        return {
            "notification_id": to_structure_SignedIntegerType_8(self.notification_id),
            "has_read": to_structure_Bool(self.has_read),
        }


def _init_Request_class_map():
    classes = [GetChartFilters, GetComplianceStatusChart, GetEscalationsChart,
    GetNotCompliedChart, GetTrendChart, GetComplianceApplicabilityStatusChart,
    GetAssigneeWiseCompliancesChart, GetAssigneeWiseComplianceDrillDown,
    GetComplianceStatusDrillDownData, GetEscalationsDrillDownData,
    GetComplianceApplicabilityStatusDrillDown, GetNotCompliedDrillDown,
    GetTrendChartDrillDownData, GetNotifications, UpdateNotificationStatus,
    GetAssigneewiseComplianesFilters]
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
    def __init__(self, countries, domains, business_groups, legal_entities, divisions, units):
        self.countries = countries
        self.domains = domains
        self.business_groups = business_groups
        self.legal_entities = legal_entities
        self.divisions = divisions
        self.units = units

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["countries", "domains", "business_groups", "legal_entities", "divisions", "units"])
        countries = data.get("countries")
        countries = parse_structure_VectorType_RecordType_core_Country(countries)
        domains = data.get("domains")
        domains = parse_structure_VectorType_RecordType_core_Domain(domains)
        business_groups = data.get("business_groups")
        business_groups = parse_structure_VectorType_RecordType_core_ClientBusinessGroup(business_groups)
        legal_entities = data.get("legal_entities")
        legal_entities = parse_structure_VectorType_RecordType_core_ClientLegalEntity(legal_entities)
        divisions = data.get("divisions")
        divisions = parse_structure_VectorType_RecordType_core_ClientDivision(divisions)
        units = data.get("units")
        units = parse_structure_VectorType_RecordType_clienttransactions_ASSIGN_COMPLIANCE_UNITS(units)
        return GetChartFiltersSuccess(countries, domains, business_groups, legal_entities, divisions, units)

    def to_inner_structure(self):
        return {
            "countries": to_structure_VectorType_RecordType_core_Country(self.countries),
            "domains": to_structure_VectorType_RecordType_core_Domain(self.domains),
            "business_groups": to_structure_VectorType_RecordType_core_ClientBusinessGroup(self.business_groups),
            "legal_entities": to_structure_VectorType_RecordType_core_ClientLegalEntity(self.legal_entities),
            "divisions": to_structure_VectorType_RecordType_core_ClientDivision(self.divisions),
            "units": to_structure_VectorType_RecordType_clienttransactions_ASSIGN_COMPLIANCE_UNITS(self.units),
        }

class GetComplianceStatusChartSuccess(Response):
    def __init__(self, chart_data):
        self.chart_data = chart_data

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["chart_data"])
        chart_data = data.get("chart_data")
        chart_data = parse_structure_VectorType_RecordType_dashboard_ChartDataMap(chart_data)
        return ChartDataMap(chart_data)

    def to_inner_structure(self):
        return {
            "chart_data": to_structure_VectorType_RecordType_dashboard_ChartDataMap(self.chart_data),
        }

class GetEscalationsChartSuccess(Response):
    def __init__(self, chart_data):
        self.chart_data = chart_data

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["chart_data"])
        chart_data = data.get("chart_data")
        chart_data = parse_structure_VectorType_RecordType_dashboard_ChartDataMap(chart_data)
        return GetEscalationsChartSuccess(chart_data)

    def to_inner_structure(self):
        return {
            "chart_data": to_structure_VectorType_RecordType_dashboard_ChartDataMap(self.chart_data),
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
        T_0_to_30_days_count = parse_structure_UnsignedIntegerType_32(T_0_to_30_days_count)
        T_31_to_60_days_count = data.get("T_31_to_60_days_count")
        T_31_to_60_days_count = parse_structure_UnsignedIntegerType_32(T_31_to_60_days_count)
        T_61_to_90_days_count = data.get("T_61_to_90_days_count")
        T_61_to_90_days_count = parse_structure_UnsignedIntegerType_32(T_61_to_90_days_count)
        Above_90_days_count = data.get("Above_90_days_count")
        Above_90_days_count = parse_structure_UnsignedIntegerType_32(Above_90_days_count)
        return GetNotCompliedChartSuccess(T_0_to_30_days_count, T_31_to_60_days_count, T_61_to_90_days_count, Above_90_days_count)

    def to_inner_structure(self):
        return {
            "T_0_to_30_days_count": to_structure_SignedIntegerType_8(self.T_0_to_30_days_count),
            "T_31_to_60_days_count": to_structure_SignedIntegerType_8(self.T_31_to_60_days_count),
            "T_61_to_90_days_count": to_structure_SignedIntegerType_8(self.T_61_to_90_days_count),
            "Above_90_days_count": to_structure_SignedIntegerType_8(self.Above_90_days_count),
        }

class GetTrendChartSuccess(Response):
    def __init__(self, years, data):
        self.years = years
        self.data = data

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["years", "data"])
        years = data.get("years")
        years = parse_structure_VectorType_UnignedIntegerType_32(years)
        data = data.get("data")
        data = parse_structure_VectorType_RecordType_dashboard_TrendData(data)
        return GetTrendChartSuccess(years, data)

    def to_inner_structure(self):
        return {
            "years": to_structure_VectorType_UnsignedIntegerType_32(self.years),
            "data": to_structure_VectorType_RecordType_dashboard_TrendData(self.data),
        }

class GetComplianceApplicabilityStatusChartSuccess(Response):
    def __init__(self, applicable_count, not_applicable_count, not_opted_count):
        self.applicable_count = applicable_count
        self.not_applicable_count = not_applicable_count
        self.not_opted_count = not_opted_count

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["applicable_count", "not_applicable_count", "not_opted_count"])
        applicable_count = data.get("applicable_count")
        applicable_count = parse_structure_UnsignedIntegerType_32(applicable_count)
        not_applicable_count = data.get("not_applicable_count")
        not_applicable_count = parse_structure_UnsignedIntegerType_32(not_applicable_count)
        not_opted_count = data.get("not_opted_count")
        not_opted_count = parse_structure_UnsignedIntegerType_32(not_opted_count)
        return GetComplianceApplicabilityStatusChartSuccess(applicable_count, not_applicable_count, not_opted_count)

    def to_inner_structure(self):
        return {
            "applicable_count": to_structure_SignedIntegerType_8(self.applicable_count),
            "not_applicable_count": to_structure_SignedIntegerType_8(self.not_applicable_count),
            "not_opted_count": to_structure_SignedIntegerType_8(self.not_opted_count),
        }


class GetAssigneewiseComplianesFiltersSuccess(Response):
    def __init__(self, countries, business_groups, legal_entities, divisions, units, users):
        self.countries = countries
        self.business_groups = business_groups
        self.legal_entities = legal_entities
        self.divisions = divisions
        self.units = units
        self.users = users

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "countries", "business_groups", "legal_entities", "divisions", "units", "users"
        ])
        countries = data.get("countries")
        countries = parse_structure_VectorType_RecordType_core_Country(countries)
        business_groups = data.get("business_groups")
        business_groups = parse_structure_VectorType_RecordType_core_ClientBusinessGroup(business_groups)
        legal_entities = data.get("legal_entities")
        legal_entities = parse_structure_VectorType_RecordType_core_ClientLegalEntity(legal_entities)
        divisions = data.get("divisions")
        divisions = parse_structure_VectorType_RecordType_core_ClientDivision(divisions)
        units = data.get("units")
        units = parse_structure_VectorType_RecordType_core_ClientUnit(units)
        users = data.get("users")
        users = parse_structure_VectorType_RecordType_clientreport_User(users)
        return GetAssigneewiseComplianesFiltersSuccess(countries, business_groups, legal_entities, divisions, units, users)

    def to_inner_structure(self):
        return {
            "countries": to_structure_VectorType_RecordType_core_Country(self.countries),
            "business_groups": to_structure_VectorType_RecordType_core_ClientBusinessGroup(self.business_groups),
            "legal_entities": to_structure_VectorType_RecordType_core_ClientLegalEntity(self.legal_entities),
            "divisions": to_structure_VectorType_RecordType_core_ClientDivision(self.divisions),
            "units": to_structure_VectorType_RecordType_core_ClientUnit(self.units),
            "users": to_structure_VectorType_RecordType_clientreport_User(self.users)
        }


class GetAssigneeWiseCompliancesChartSuccess(Response):
    def __init__(self, chart_data):
        self.chart_data = chart_data

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["chart_data"])
        chart_data = data.get("chart_data")
        chart_data = parse_structure_VectorType_RecordType_dashboard_AssigneeChartData(chart_data)
        return GetAssigneeWiseCompliancesChartSuccess(chart_data)

    def to_inner_structure(self):
        return {
            "chart_data": to_structure_VectorType_RecordType_dashboard_AssigneeChartData(self.chart_data),
        }

class GetAssigneeWiseComplianceDrillDownSuccess(Response):
    def __init__(self, complied, delayed, inprogress, not_complied):
        self.complied = complied
        self.delayed = delayed
        self.inprogress = inprogress
        self.not_complied = not_complied

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["complied", "delayed", "inprogress", "not_complied"])
        complied = data.get("complied")
        complied = parse_structure_VectorType_RecordType_dashboard_UnitCompliance(complied)
        delayed = data.get("delayed")
        delayed = parse_structure_VectorType_RecordType_dashboard_UnitCompliance(delayed)
        inprogress = data.get("inprogress")
        inprogress = parse_structure_VectorType_RecordType_dashboard_UnitCompliance(inprogress)
        not_complied = data.get("not_complied")
        not_complied = parse_structure_VectorType_RecordType_dashboard_UnitCompliance(not_complied)
        return GetAssigneeWiseComplianceDrillDownSuccess(complied, delayed, inprogress, not_complied)

    def to_inner_structure(self):
        return {
            "complied": to_structure_VectorType_RecordType_dashboard_UnitCompliance(self.complied),
            "delayed": to_structure_VectorType_RecordType_dashboard_UnitCompliance(self.delayed),
            "inprogress": to_structure_VectorType_RecordType_dashboard_UnitCompliance(self.inprogress),
            "not_complied": to_structure_VectorType_RecordType_dashboard_UnitCompliance(self.not_complied),
        }

class GetComplianceStatusDrillDownDataSuccess(Response):
    def __init__(self, drill_down_data):
        self.drill_down_data = drill_down_data

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["drill_down_data"])
        drill_down_data = data.get("drill_down_data")
        drill_down_data = parse_structure_VectorType_RecordType_dashboard_DrillDownData(drill_down_data)
        return GetComplianceStatusDrillDownDataSuccess(drill_down_data)

    def to_inner_structure(self):
        return {
            "drill_down_data": to_structure_VectorType_RecordType_dashboard_DrillDownData(self.drill_down_data),
        }

class GetEscalationsDrillDownDataSuccess(Response):
    def __init__(self, delayed, not_complied):
        self.delayed = delayed
        self.not_complied = not_complied

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["delayed", "not_complied"])
        delayed = data.get("delayed")
        delayed = parse_structure_VectorType_RecordType_dashboard_DrillDownData(delayed)
        not_complied = data.get("not_complied")
        not_complied = parse_structure_VectorType_RecordType_dashboard_DrillDownData(not_complied)
        return GetEscalationsDrillDownDataSuccess(delayed, not_complied)

    def to_inner_structure(self):
        return {
            "delayed": to_structure_VectorType_RecordType_dashboard_DrillDownData(self.delayed),
            "not_complied": to_structure_VectorType_RecordType_dashboard_DrillDownData(self.not_complied),
        }

class GetComplianceApplicabilityStatusDrillDownSuccess(Response):
    def __init__(self, drill_down_data):
        self.drill_down_data = drill_down_data

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["drill_down_data"])
        drill_down_data = data.get("drill_down_data")
        drill_down_data = parse_structure_VectorType_RecordType_dashboard_ApplicableDrillDown(drill_down_data)
        return GetComplianceApplicabilityStatusDrillDownSuccess(drill_down_data)

    def to_inner_structure(self):
        return {
            "drill_down_data": to_structure_VectorType_RecordType_dashboard_ApplicableDrillDown(self.drill_down_data),
        }

class GetNotCompliedDrillDownSuccess(Response):
    def __init__(self, drill_down_data):
        self.drill_down_data = drill_down_data

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["drill_down_data"])
        drill_down_data = data.get("drill_down_data")
        drill_down_data = parse_structure_VectorType_RecordType_dashboard_DrillDownData(drill_down_data)
        return GetNotCompliedDrillDownSuccess(filter_name, drill_down_data)

    def to_inner_structure(self):
        return {
            "drill_down_data": to_structure_VectorType_RecordType_dashboard_DrillDownData(self.drill_down_data),
        }

class GetTrendChartDrillDownDataSuccess(Response):
    def __init__(self, drill_down_data):
        self.drill_down_data = drill_down_data

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["drill_down_data"])
        drill_down_data = data.get("drill_down_data")
        drill_down_data = parse_structure_VectorType_RecordType_dashboard_TrendDrillDownData(drill_down_data)
        return GetTrendChartDrillDownDataSuccess(drill_down_data)

    def to_inner_structure(self):
        return {
            "drill_down_data": to_structure_VectorType_RecordType_dashboard_TrendDrillDownData(self.drill_down_data),
        }

class GetNotificationsSuccess(Response):
    def __init__(self, notifications):
        self.notifications = notifications

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["notifications"])
        notifications = data.get("notifications")
        notifications = parse_structure_VectorType_RecordType_dashboard_Notification(notifications)
        return GetNotificationsSuccess(notifications)

    def to_inner_structure(self):
        return {
            "notifications": to_structure_VectorType_RecordType_dashboard_Notification(self.notifications),
        }

class UpdateNotificationStatusSuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return UpdateNotificationStatusSuccess()

    def to_inner_structure(self):
        return {
        }


def _init_Response_class_map():
    classes = [GetChartFiltersSuccess, GetComplianceStatusChartSuccess,
    GetEscalationsChartSuccess, GetNotCompliedChartSuccess, GetTrendChartSuccess,
    GetComplianceApplicabilityStatusChartSuccess,
    GetAssigneeWiseCompliancesChartSuccess,
    GetAssigneeWiseComplianceDrillDownSuccess,
    GetComplianceStatusDrillDownDataSuccess, GetEscalationsDrillDownDataSuccess,
    GetComplianceApplicabilityStatusDrillDownSuccess, GetNotCompliedDrillDownSuccess,
    GetTrendChartDrillDownDataSuccess, GetNotificationsSuccess,
    UpdateNotificationStatusSuccess, GetAssigneewiseComplianesFiltersSuccess]
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
        session_token = parse_structure_CustomTextType_50(session_token)
        request = data.get("request")
        request = parse_structure_VariantType_dashboard_Request(request)
        return RequestFormat(session_token, request)

    def to_structure(self):
        return {
            "session_token": to_structure_CustomTextType_50(self.session_token),
            "request": to_structure_VariantType_dashboard_Request(self.request),
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
        data = parse_dictionary(data, ["level1_statutory_name", "compliances"])
        level1_statutory_name = data.get("level1_statutory_name")
        level1_statutory_name = parse_structure_CustomTextType_50(level1_statutory_name)
        compliances = data.get("compliances")
        compliances = parse_structure_MapType_SignedIntegerType_8_VectorType_RecordType_core_Compliance(compliances)
        return ApplicableDrillDown(level1_statutory_name, compliances)

    def to_structure(self):
        return {
            "level1_statutory_name": to_structure_CustomTextType_50(self.level1_statutory_name),
            "compliances": to_structure_MapType_SignedIntegerType_8_VectorType_RecordType_core_Compliance(self.compliances),
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
        data = parse_dictionary(data, ["filter_type_id", "data"])
        filter_type_id = data.get("filter_type_id")
        filter_type_id = parse_structure_UnsignedIntegerType_32(filter_type_id)
        data = data.get("data")
        data = parse_structure_VectorType_RecordType_core_NumberOfCompliances(data)
        return ChartDataMap(filter_type_id, data)

    def to_structure(self):
        return {
            "filter_type_id": to_structure_SignedIntegerType_8(self.filter_type_id),
            "data": to_structure_VectorType_RecordType_core_NumberOfCompliances(self.data),
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
        data = parse_dictionary(data, ["year", "delayed_compliance_count", "not_complied_count"])
        year = data.get("year")
        year = parse_structure_CustomTextType_20(year)
        delayed_compliance_count = data.get("delayed_compliance_count")
        delayed_compliance_count = parse_structure_UnsignedIntegerType_32(delayed_compliance_count)
        not_complied_count = data.get("not_complied_count")
        not_complied_count = parse_structure_UnsignedIntegerType_32(not_complied_count)
        return EscalationData(year, delayed_compliance_count, not_complied_count)

    def to_structure(self):
        return {
            "year": to_structure_CustomTextType_20(self.year),
            "delayed_compliance_count": to_structure_SignedIntegerType_8(self.delayed_compliance_count),
            "not_complied_count": to_structure_SignedIntegerType_8(self.not_complied_count),
        }

#
# CompliedMap
#

class CompliedMap(object):
    def __init__(self, year, total_compliances, complied_compliances_count):
        self.year = year
        self.total_compliances = total_compliances
        self.complied_compliances_count = complied_compliances_count

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["year", "total_compliances", "complied_compliances_count"])
        year = data.get("year")
        year = parse_structure_UnsignedIntegerType_32(year)
        total_compliances = data.get("total_compliances")
        total_compliances = parse_structure_UnsignedIntegerType_32(total_compliances)
        complied_compliances_count = data.get("complied_compliances_count")
        complied_compliances_count = parse_structure_UnsignedIntegerType_32(complied_compliances_count)
        return CompliedMap(year, total_compliances, complied_compliances_count)

    def to_structure(self):
        return {
            "year": to_structure_UnsignedIntegerType_32(self.year),
            "total_compliances": to_structure_UnsignedIntegerType_32(self.total_compliances),
            "complied_compliances_count": to_structure_SignedIntegerType_8(self.complied_compliances_count),
        }

#
# TrendData
#

class TrendData(object):
    def __init__(self, filter_id, complied_compliance):
        self.filter_id = filter_id
        self.complied_compliance = complied_compliance

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["filter_id", "complied_compliance"])
        filter_id = data.get("filter_id")
        filter_id = parse_structure_UnsignedIntegerType_32(filter_id)
        complied_compliance = data.get("complied_compliance")
        complied_compliance = parse_structure_VectorType_RecordType_dashboard_CompliedMap(complied_compliance)
        return TrendData(filter_id, complied_compliance)

    def to_structure(self):
        return {
            "filter_id": to_structure_UnsignedIntegerType_32(self.filter_id),
            "complied_compliance": to_structure_VectorType_RecordType_dashboard_CompliedMap(self.complied_compliance),
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
        compliance_name = parse_structure_CustomTextType_50(compliance_name)
        reassigned_from = data.get("reassigned_from")
        reassigned_from = parse_structure_CustomTextType_50(reassigned_from)
        start_date = data.get("start_date")
        start_date = parse_structure_CustomTextType_20(start_date)
        due_date = data.get("due_date")
        due_date = parse_structure_CustomTextType_20(due_date)
        reassigned_date = data.get("reassigned_date")
        reassigned_date = parse_structure_CustomTextType_20(reassigned_date)
        completed_date = data.get("completed_date")
        completed_date = parse_structure_CustomTextType_20(completed_date)
        return RessignedCompliance(compliance_name, reassigned_from, start_date, due_date, reassigned_date, completed_date)

    def to_structure(self):
        return {
            "compliance_name": to_structure_CustomTextType_50(self.compliance_name),
            "reassigned_from": to_structure_CustomTextType_50(self.reassigned_from),
            "start_date": to_structure_CustomTextType_20(self.start_date),
            "due_date": to_structure_CustomTextType_20(self.due_date),
            "reassigned_date": to_structure_CustomTextType_20(self.reassigned_date),
            "completed_date": to_structure_CustomTextType_20(self.completed_date),
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
        data = parse_dictionary(data,
        ["assigned_count", "reassigned_count", "reassigned_compliances"])
        assigned_count = data.get("assigned_count")
        assigned_count = parse_structure_UnsignedIntegerType_32(assigned_count)
        reassigned_count = data.get("reassigned_count")
        reassigned_count = parse_structure_UnsignedIntegerType_32(reassigned_count)
        reassigned_compliances = data.get("reassigned_compliances")
        reassigned_compliances = parse_structure_OptionalType_VectorType_RecordType_dashboard_RessignedCompliance(reassigned_compliances)
        return DelayedCompliance(assigned_count, reassigned_count, reassigned_compliances)

    def to_structure(self):
        return {
            "assigned_count": to_structure_SignedIntegerType_8(self.assigned_count),
            "reassigned_count": to_structure_SignedIntegerType_8(self.reassigned_count),
            "reassigned_compliances": to_structure_OptionalType_VectorType_RecordType_dashboard_RessignedCompliance(self.reassigned_compliances),
        }

#
# DomainWise
#

class DomainWise(object):
    def __init__(self, domain_id, domain_name, total_compliances, complied_count, delayed_compliance, inprogress_compliance_count, not_complied_count):
        self.domain_id = domain_id
        self.domain_name = domain_name
        self.total_compliances = total_compliances
        self.complied_count = complied_count
        self.delayed_compliance = delayed_compliance
        self.inprogress_compliance_count = inprogress_compliance_count
        self.not_complied_count = not_complied_count

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["domain_id", "domain_name", "total_compliances", "complied_count", "delayed_compliance", "inprogress_compliance_count", "not_complied_count"])
        domain_id = data.get("domain_id")
        domain_id = parse_structure_UnsignedIntegerType_32(domain_id)
        domain_name = data.get("domain_name")
        domain_name = parse_structure_CustomTextType_50(domain_name)
        total_compliances = data.get("total_compliances")
        total_compliances = parse_structure_UnsignedIntegerType_32(total_compliances)
        complied_count = data.get("complied_count")
        complied_count = parse_structure_UnsignedIntegerType_32(complied_count)
        delayed_compliance = data.get("delayed_compliance")
        delayed_compliance = parse_structure_RecordType_dashboard_DelayedCompliance(delayed_compliance)
        inprogress_compliance_count = data.get("inprogress_compliance_count")
        inprogress_compliance_count = parse_structure_UnsignedIntegerType_32(inprogress_compliance_count)
        not_complied_count = data.get("not_complied_count")
        not_complied_count = parse_structure_UnsignedIntegerType_32(not_complied_count)
        return DomainWise(domain_id, domain_name, total_compliances, complied_count, delayed_compliance, inprogress_compliance_count, not_complied_count)

    def to_structure(self):
        return {
            "domain_id": to_structure_SignedIntegerType_8(self.domain_id),
            "domain_name": to_structure_CustomTextType_50(self.domain_name),
            "total_compliances": to_structure_SignedIntegerType_8(self.total_compliances),
            "complied_count": to_structure_SignedIntegerType_8(self.complied_count),
            "delayed_compliance": to_structure_RecordType_dashboard_DelayedCompliance(self.delayed_compliance),
            "inprogress_compliance_count": to_structure_SignedIntegerType_8(self.inprogress_compliance_count),
            "not_complied_count": to_structure_SignedIntegerType_8(self.not_complied_count),
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
        data = parse_dictionary(data, ["user_id", "assignee_name", "domain_wise_details"])
        user_id = data.get("user_id")
        user_id = parse_structure_UnsignedIntegerType_32(user_id)
        assignee_name = data.get("assignee_name")
        assignee_name = parse_structure_CustomTextType_100(assignee_name)
        domain_wise_details = data.get("domain_wise_details")
        domain_wise_details = parse_structure_VectorType_RecordType_dashboard_DomainWise(domain_wise_details)
        return AssigneeWiseDetails(user_id, assignee_name, domain_wise_details)

    def to_structure(self):
        return {
            "user_id": to_structure_SignedIntegerType_8(self.user_id),
            "assignee_name": to_structure_CustomTextType_100(self.assignee_name),
            "domain_wise_details": to_structure_VectorType_RecordType_dashboard_DomainWise(self.domain_wise_details),
        }

#
# AssigneeChartData
#

class AssigneeChartData(object):
    def __init__(self, unit_name, assignee_wise_details, address):
        self.unit_name = unit_name
        self.assignee_wise_details = assignee_wise_details
        self.address = address

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["unit_name", "assignee_wise_details", "address"])
        unit_name = data.get("unit_name")
        unit_name = parse_structure_CustomTextType_50(unit_name)
        assignee_wise_details = data.get("assignee_wise_details")
        assignee_wise_details = parse_structure_VectorType_RecordType_dashboard_AssigneeWiseDetails(assignee_wise_details)
        address = data.get("address")
        address = parse_structure_CustomTextType_500(address)
        return AssigneeChartData(unit_name, assignee_wise_details, address)

    def to_structure(self):
        return {
            "unit_name": to_structure_CustomTextType_50(self.unit_name),
            "address": to_structure_CustomTextType_500(self.address),
            "assignee_wise_details": to_structure_VectorType_RecordType_dashboard_AssigneeWiseDetails(self.assignee_wise_details),
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
            "compliance_name", "description",
            "assignee_name", "assigned_date", "due_date", "completion_date",
            "status", "ageing"
        ])
        compliance_name = data.get("compliance_name")
        compliance_name = parse_structure_CustomTextType_100(compliance_name)
        description = data.get("description")
        description = parse_structure_CustomTextType_500(description)
        assignee_name = data.get("assignee_name")
        assignee_name = parse_structure_CustomTextType_100(assignee_name)
        assigned_date = data.get("assigned_date")
        assigned_date = parse_structure_CustomTextType_20(assigned_date)
        due_date = data.get("due_date")
        due_date = parse_structure_CustomTextType_20(due_date)
        completion_date = data.get("completion_date")
        completion_date = parse_structure_CustomTextType_20(completion_date)
        status = data.get("status")
        status = parse_structure_EnumType_core_COMPLIANCE_STATUS(status)
        ageing = data.get("ageing")
        ageing = parse_structure_UnsignedIntegerType_32(ageing)
        return Level1Compliance(
            compliance_name, description, assignee_name, assigned_date,
            due_date, completion_date,
            status, ageing
        )

    def to_structure(self):
        return {
            "compliance_name": to_structure_CustomTextType_100(self.compliance_name),
            "description": to_structure_CustomTextType_500(self.description),
            "assignee_name": to_structure_CustomTextType_100(self.assignee_name),
            "assigned_date": to_structure_CustomTextType_20(self.assigned_date),
            "due_date": to_structure_CustomTextType_20(self.due_date),
            "completion_date": to_structure_CustomTextType_20(self.completion_date),
            "status": to_structure_EnumType_core_COMPLIANCE_STATUS(self.status),
            "ageing": to_structure_UnsignedIntegerType_32(self.ageing)
        }

#
# Level1Compliance
#

class AssigneeWiseLevel1Compliance(object):
    def __init__(self, compliance_name, description, assignee_name, assigned_date,
        due_date, completion_date):
        self.compliance_name = compliance_name
        self.description = description
        self.assignee_name = assignee_name
        self.assigned_date = assigned_date
        self.due_date = due_date
        self.completion_date = completion_date

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["compliance_name", "description",
            "assignee_name", "assigned_date", "due_date", "completion_date",
        ])
        compliance_name = data.get("compliance_name")
        compliance_name = parse_structure_CustomTextType_100(compliance_name)
        description = data.get("description")
        description = parse_structure_CustomTextType_500(description)
        assignee_name = data.get("assignee_name")
        assignee_name = parse_structure_CustomTextType_100(assignee_name)
        assigned_date = data.get("assigned_date")
        assigned_date = parse_structure_CustomTextType_20(assigned_date)
        due_date = data.get("due_date")
        due_date = parse_structure_CustomTextType_20(due_date)
        completion_date = data.get("completion_date")
        completion_date = parse_structure_CustomTextType_20(completion_date)
        return AssigneeWiseLevel1Compliance(compliance_name, description, assignee_name, assigned_date,
        due_date, completion_date)

    def to_structure(self):
        return {
            "compliance_name": to_structure_CustomTextType_100(self.compliance_name),
            "description": to_structure_CustomTextType_500(self.description),
            "assignee_name": to_structure_CustomTextType_100(self.assignee_name),
            "assigned_date": to_structure_CustomTextType_20(self.assigned_date),
            "due_date": to_structure_CustomTextType_20(self.due_date),
            "completion_date": to_structure_CustomTextType_20(self.completion_date)
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
        compliances = parse_structure_MapType_CustomTextType_50_VectorType_RecordType_dashboard_AssigneeWiseLevel1Compliance(compliances)
        return UnitCompliance(unit_name, address, compliances)

    def to_structure(self):
        return {
            "unit_name": to_structure_CustomTextType_100(self.unit_name),
            "address": to_structure_CustomTextType_250(self.address),
            "compliances": to_structure_MapType_CustomTextType_50_VectorType_RecordType_dashboard_AssigneeWiseLevel1Compliance(self.compliances),
        }

class TrendCompliance(object):
    def __init__(self, compliance_name, description, assignee_name):
        self.compliance_name = compliance_name
        self.description = description
        self.assignee_name = assignee_name

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["compliance_name", "description", "assignee_name"])
        compliance_name = data.get("compliance_name")
        compliance_name = parse_structure_CustomTextType_100(compliance_name)
        description = data.get("description")
        description = parse_structure_CustomTextType_500(description)
        assignee_name = data.get("assignee_name")
        assignee_name = parse_structure_CustomTextType_100(assignee_name)
        return TrendCompliance(compliance_name, description, assignee_name)

    def to_structure(self):
        return {
            "compliance_name": to_structure_CustomTextType_100(self.compliance_name),
            "description": to_structure_CustomTextType_500(self.description),
            "assignee_name": to_structure_CustomTextType_100(self.assignee_name),
        }

#
# DrillDownData
#

class DrillDownData(object):
    def __init__(self, business_group, legal_entity, division, unit_name, address, industry_name, compliances):
        self.business_group = business_group
        self.legal_entity = legal_entity
        self.division = division
        self.unit_name = unit_name
        self.address = address
        self.industry_name = industry_name
        self.compliances = compliances

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["business_group", "legal_entity", "division", "unit_name", "address", "industry_name", "compliances"])
        business_group = data.get("business_group")
        business_group = parse_structure_CustomTextType_50(business_group)
        legal_entity = data.get("legal_entity")
        legal_entity = parse_structure_CustomTextType_50(legal_entity)
        division = data.get("division")
        division = parse_structure_CustomTextType_50(division)
        unit_name = data.get("unit_name")
        unit_name = parse_structure_CustomTextType_100(unit_name)
        address = data.get("address")
        address = parse_structure_CustomTextType_500(address)
        industry_name =  data.geT("industry_name")
        industry_name = parse_structure_CustomTextType_50(industry_name)
        compliances = data.get("compliances")
        compliances = parse_structure_MapType_CustomTextType_50_VectorType_RecordType_dashboard_Level1Compliance(compliances)
        return DrillDownData(business_group, legal_entity, division, unit_name, address, industry_name, compliances)

    def to_structure(self):
        return {
            "business_group": to_structure_CustomTextType_50(self.business_group),
            "legal_entity": to_structure_CustomTextType_50(self.legal_entity),
            "division": to_structure_CustomTextType_50(self.division),
            "unit_name": to_structure_CustomTextType_100(self.unit_name),
            "address": to_structure_CustomTextType_500(self.address),
            "industry_name": to_structure_CustomTextType_50(self.industry_name),
            "compliances": to_structure_MapType_CustomTextType_50_VectorType_RecordType_dashboard_Level1Compliance(self.compliances),
        }

#
# Notification
#

class Notification(object):
    def __init__(
        self, notification_id, read_status, notification_text, extra_details,
        updated_on, level_1_statutory, unit_name, unit_address, assignee,
        concurrence_person, approval_person, compliance_name,
        compliance_description, due_date, delayed_days, penal_consequences
    ):
        self.notification_id = notification_id
        self.read_status = read_status
        self.notification_text = notification_text
        self.extra_details = extra_details
        self.updated_on = updated_on
        self.level_1_statutory = level_1_statutory
        self.unit_name = unit_name
        self.unit_address = unit_address
        self.assignee = assignee
        self.concurrence_person = concurrence_person
        self.approval_person = approval_person
        self.compliance_name = compliance_name
        self.compliance_description = compliance_description
        self.due_date = due_date
        self.delayed_days = delayed_days
        self.penal_consequences = penal_consequences

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "notification_id", "read_status", "notification_text",
            "extra_details", "updated_on", "level_1_statutory", "unit_name",
            "unit_address", "assignee", "concurrence_person", "approval_person",
            "compliance_name", "compliance_description", "due_date", "delayed_days",
            "penal_consequences"
        ])
        notification_id = data.get("notification_id")
        notification_id = parse_structure_UnsignedIntegerType_32(notification_id)
        read_status = data.get("read_status")
        read_status = parse_structure_Bool(read_status)
        notification_text = data.get("notification_text")
        notification_text = parse_structure_CustomTextType_500(notification_text)
        extra_details = data.get("extra_details")
        extra_details = parse_structure_CustomTextType_500(extra_details)
        updated_on = data.get("updated_on")
        updated_on = parse_structure_CustomTextType_20(updated_on)
        level_1_statutory = data.get("level_1_statutory")
        level_1_statutory = parse_structure_CustomTextType_50(level_1_statutory)
        unit_name = data.get("unit_name")
        unit_name = parse_structure_CustomTextType_50(unit_name)
        unit_address = data.get("unit_address")
        unit_address = parse_structure_CustomTextType_50(unit_address)
        assignee = data.get("assignee")
        assignee = parse_structure_CustomTextType_100(assignee)
        concurrence_person = data.get("concurrence_person")
        concurrence_person = parse_structure_CustomTextType_100(concurrence_person)
        approval_person = data.get("approval_person")
        approval_person = parse_structure_CustomTextType_100(approval_person)
        compliance_name = data.get("compliance_name")
        compliance_name = parse_structure_CustomTextType_100(compliance_name)
        compliance_description = data.get("compliance_description")
        compliance_description = parse_structure_CustomTextType_500(compliance_description)
        due_date = data.get("due_date")
        due_date = parse_structure_CustomTextType_20(due_date)
        delayed_days = data.get("delayed_days")
        delayed_days = parse_structure_CustomTextType_20(delayed_days)
        penal_consequences = data.get("penal_consequences")
        penal_consequences = parse_structure_CustomTextType_500(penal_consequences)
        return Notification(
            notification_id, read_status, notification_text, extra_details,
            updated_on, level_1_statutory, unit_name, unit_address, assignee,
            concurrence_person, approval_person, compliance_name,
            compliance_description, due_date, delayed_days, penal_consequences
        )

    def to_structure(self):
        return {
            "notification_id" : to_structure_UnsignedIntegerType_32(self.notification_id),
            "read_status" : to_structure_Bool(self.read_status),
            "notification_text" : to_structure_CustomTextType_500(self.notification_text),
            "extra_details" : to_structure_CustomTextType_500(self.extra_details),
            "updated_on" : to_structure_CustomTextType_20(self.updated_on),
            "level_1_statutory" : to_structure_CustomTextType_50(self.level_1_statutory),
            "unit_name" : to_structure_CustomTextType_50(self.unit_name),
            "unit_address" : to_structure_CustomTextType_50(self.unit_address),
            "assignee" : to_structure_CustomTextType_100(self.assignee),
            "concurrence_person" : to_structure_CustomTextType_100(self.concurrence_person),
            "approval_person" : to_structure_CustomTextType_100(self.approval_person),
            "compliance_name" : to_structure_CustomTextType_100(self.compliance_name),
            "compliance_description" : to_structure_CustomTextType_500(self.compliance_description),
            "due_date" : to_structure_CustomTextType_20(self.due_date),
            "delayed_days" : to_structure_CustomTextType_20(self.delayed_days),
            "penal_consequences" : to_structure_CustomTextType_500(self.penal_consequences)
        }

#
# Trend DrillDownData
#

class TrendDrillDownData(object):
    def __init__(self, business_group_id, legal_entity_id, division_id, unit_name, address, compliances):
        self.business_group_id = business_group_id
        self.legal_entity_id = legal_entity_id
        self.division_id = division_id
        self.unit_name = unit_name
        self.address = address
        self.compliances = compliances

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["business_group_id", "legal_entity_id", "division_id", "unit_name", "address", "compliances"])
        business_group_id = data.get("business_group_id")
        business_group_id = parse_structure_UnsignedIntegerType_32(business_group_id)
        legal_entity_id = data.get("legal_entity_id")
        legal_entity_id = parse_structure_UnsignedIntegerType_32(legal_entity_id)
        division_id = data.get("division_id")
        division_id = parse_structure_UnsignedIntegerType_32(division_id)
        unit_name = data.get("unit_name")
        unit_name = parse_structure_CustomTextType_100(unit_name)
        address = data.get("address")
        address = parse_structure_CustomTextType_500(address)
        compliances = data.get("compliances")
        compliances = parse_structure_MapType_CustomTextType_100_VectorType_RecordType_dashboard_TrendCompliance(compliances)
        return TrendDrillDownData(business_group_id, legal_entity_id, division_id, unit_name, address, compliances)

    def to_structure(self):
        return {
            "business_group_id": to_structure_UnsignedIntegerType_32(self.business_group_id),
            "legal_entity_id": to_structure_UnsignedIntegerType_32(self.legal_entity_id),
            "division_id": to_structure_UnsignedIntegerType_32(self.division_id),
            "unit_name": to_structure_CustomTextType_100(self.unit_name),
            "address": to_structure_CustomTextType_500(self.address),
            "compliances": to_structure_MapType_CustomTextType_100_VectorType_RecordType_dashboard_TrendCompliance(self.compliances),
        }

