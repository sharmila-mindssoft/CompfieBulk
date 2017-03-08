
from clientprotocol.jsonvalidators_client import (
    parse_enum, parse_dictionary, parse_static_list, to_structure_dictionary_values,
)
from clientprotocol.parse_structure import (
    parse_structure_VectorType_RecordType_clientreport_UserWiseCompliance,
    parse_structure_VectorType_RecordType_core_Compliance,
    parse_structure_VectorType_RecordType_clientreport_LoginTrace,
    parse_structure_VectorType_RecordType_clientreport_ReassignHistory,
    parse_structure_VectorType_RecordType_clientreport_ReassignCompliance,
    parse_structure_VectorType_RecordType_clientreport_ReassignUnitCompliance,
    parse_structure_UnsignedIntegerType_32,
    parse_structure_MapType_SignedIntegerType_8_MapType_SignedIntegerType_8_VectorType_RecordType_core_Statutory,
    parse_structure_VectorType_RecordType_core_BusinessGroup,
    parse_structure_MapType_CustomTextType_50_VectorType_RecordType_clientreport_ActivityCompliance,
    parse_structure_VectorType_RecordType_core_ServiceProvider,
    parse_structure_CustomTextType_500,
    parse_structure_OptionalType_CustomTextType_50,
    parse_structure_VectorType_RecordType_clientreport_UserName,
    parse_structure_VectorType_RecordType_clientreport_User,
    parse_structure_VectorType_RecordType_core_Country,
    parse_structure_VectorType_RecordType_clientreport_StatutoryReassignCompliance,
    parse_structure_VectorType_RecordType_clientreport_ComplianceUnit,
    parse_structure_VectorType_RecordType_clientreport_FormName,
    parse_structure_MapType_CustomTextType_500_VectorType_RecordType_clientreport_ApplicabilityCompliance,
    parse_structure_OptionalType_SignedIntegerType_8,
    parse_structure_CustomTextType_50,
    parse_structure_EnumType_core_COMPLIANCE_STATUS,
    parse_structure_CustomTextType_100,
    parse_structure_EnumType_core_USER_TYPE,
    parse_structure_VectorType_RecordType_clientreport_ActivityLog,
    parse_structure_VectorType_RecordType_core_Unit,
    parse_structure_VectorType_RecordType_clientreport_ComplianceForUnit,
    parse_structure_VectorType_CustomTextType_50,
    parse_structure_MapType_CustomTextType_50_VectorType_RecordType_clientreport_ComplianceUnit,
    parse_structure_VectorType_RecordType_core_Division,
    parse_structure_VectorType_RecordType_clientreport_UnitCompliance,
    parse_structure_OptionalType_CustomTextType_20,
    parse_structure_VectorType_RecordType_clientreport_ServiceProviderCompliance,
    parse_structure_VectorType_RecordType_clientreport_UnitName,
    parse_structure_EnumType_core_COMPLIANCE_ACTIVITY_STATUS,
    parse_structure_CustomTextType_250,
    parse_structure_VectorType_RecordType_clientreport_ComplianceDetails,
    parse_structure_VectorType_RecordType_core_LegalEntity,
    parse_structure_VectorType_RecordType_core_Domain,
    parse_structure_MapType_CustomTextType_50_VectorType_RecordType_clientreport_Level1Statutory,
    parse_structure_OptionalType_EnumType_core_APPLICABILITY_STATUS,
    parse_structure_EnumType_core_COMPLIANCE_FREQUENCY,
    parse_structure_OptionalType_CustomTextType_100,
    parse_structure_VectorType_RecordType_clientreport_ComplianceName,
    parse_structure_CustomTextType_20,
    parse_structure_VectorType_RecordType_clientreport_AssigneeCompliance,
    parse_structure_VariantType_clientreport_Request,
    parse_structure_VectorType_RecordType_clientreport_ComplianceList,
    parse_structure_VectorType_RecordType_clientreport_Activities,
    parse_structure_VectorType_RecordType_core_ClientBusinessGroup,
    parse_structure_VectorType_RecordType_core_ClientLegalEntity,
    parse_structure_VectorType_RecordType_core_ClientDivision,
    parse_structure_VectorType_RecordType_core_ClientUnit,
    parse_structure_VectorType_RecordType_core_StatutoryDate,
    parse_structure_VectorType_RecordType_clientreport_ComplianceDetailsUnitWise,
    parse_structure_VectorType_RecordType_core_ComplianceFilter,
    parse_structure_OptionalType_UnsignedIntegerType_32,
    parse_structure_VectorType_RecordType_clientreport_RiskData,
    parse_structure_RecordType_clientreport_STATUTORY_WISE_NOTIFICATIONS,
    parse_structure_VectorType_RecordType_clientreport_STATUTORY_WISE_NOTIFICATIONS,
    parse_structure_VectorType_CustomTextType_100,
    parse_structure_VectorType_RecordType_clientreport_ActivityData,
    parse_structure_OptionalType_VectorType_SignedIntegerType_8,
    parse_structure_VectorType_RecordType_core_UnitDetails,
    parse_structure_VectorType_RecordType_client_report_UnitDetails,
    parse_structure_VectorType_SignedIntegerType_8,
    parse_structure_VectorType_CustomTextType_500,
    parse_structure_OptionalType_CustomTextType_500,
    parse_structure_Text,
    parse_structure_VectorType_Text,
    parse_structure_OptionalType_Text,
    parse_structure_Bool,
    parse_structure_OptionalType_VectorType_CustomTextType_500,
    parse_structure_VectorType_RecordType_clientreport_GetComplianceTaskApplicabilityStatusReportData,
    parse_structure_OptionalType_CustomTextType_250,
    parse_structure_VectorType_RecordType_clientreport_Level1Compliance,
    parse_structure_MapType_CustomTextType_500_VectorType_RecordType_clientreport_LEVEL_1_STATUTORY_NOTIFICATIONS

)
from clientprotocol.to_structure import (
    to_structure_VectorType_RecordType_clientreport_UserWiseCompliance,
    to_structure_VectorType_RecordType_core_Compliance,
    to_structure_VectorType_RecordType_clientreport_LoginTrace,
    to_structure_VectorType_RecordType_clientreport_ReassignHistory,
    to_structure_VectorType_RecordType_clientreport_ReassignCompliance,
    to_structure_VectorType_RecordType_clientreport_ReassignUnitCompliance,
    to_structure_SignedIntegerType_8,
    to_structure_MapType_SignedIntegerType_8_MapType_SignedIntegerType_8_VectorType_RecordType_core_Statutory,
    to_structure_VectorType_RecordType_core_BusinessGroup,
    to_structure_MapType_CustomTextType_50_VectorType_RecordType_clientreport_ActivityCompliance,
    to_structure_VectorType_RecordType_core_ServiceProvider,
    to_structure_CustomTextType_500,
    to_structure_VectorType_RecordType_clientreport_UserName,
    to_structure_VectorType_RecordType_clientreport_User,
    to_structure_VectorType_RecordType_core_Country,
    to_structure_VectorType_RecordType_clientreport_StatutoryReassignCompliance,
    to_structure_VectorType_RecordType_clientreport_ComplianceUnit,
    to_structure_VectorType_RecordType_clientreport_FormName,
    to_structure_MapType_CustomTextType_500_VectorType_RecordType_clientreport_ApplicabilityCompliance,
    to_structure_OptionalType_SignedIntegerType_8,
    to_structure_CustomTextType_50,
    to_structure_OptionalType_CustomTextType_50,
    to_structure_EnumType_core_COMPLIANCE_STATUS,
    to_structure_CustomTextType_100, to_structure_EnumType_core_USER_TYPE,
    to_structure_VectorType_RecordType_clientreport_ActivityLog,
    to_structure_VectorType_RecordType_core_Unit,
    to_structure_VectorType_RecordType_clientreport_ComplianceForUnit,
    to_structure_VectorType_CustomTextType_50,
    to_structure_MapType_CustomTextType_50_VectorType_RecordType_clientreport_ComplianceUnit,
    to_structure_VectorType_RecordType_core_Division,
    to_structure_VectorType_RecordType_clientreport_UnitCompliance,
    to_structure_OptionalType_CustomTextType_20,
    to_structure_VectorType_RecordType_clientreport_ServiceProviderCompliance,
    to_structure_VectorType_RecordType_clientreport_UnitName,
    to_structure_EnumType_core_COMPLIANCE_ACTIVITY_STATUS,
    to_structure_CustomTextType_250,
    to_structure_VectorType_RecordType_clientreport_ComplianceDetails,
    to_structure_VectorType_RecordType_core_LegalEntity,
    to_structure_VectorType_RecordType_core_Domain,
    to_structure_MapType_CustomTextType_500_VectorType_RecordType_clientreport_Level1Statutory,
    to_structure_OptionalType_EnumType_core_APPLICABILITY_STATUS,
    to_structure_EnumType_core_COMPLIANCE_FREQUENCY,
    to_structure_OptionalType_CustomTextType_100,
    to_structure_VectorType_RecordType_clientreport_ComplianceName,
    to_structure_CustomTextType_20,
    to_structure_VectorType_RecordType_clientreport_AssigneeCompliance,
    to_structure_VariantType_clientreport_Request,
    to_structure_VectorType_RecordType_clientreport_ComplianceList,
    to_structure_VectorType_RecordType_clientreport_Activities,
    to_structure_VectorType_RecordType_core_ClientBusinessGroup,
    to_structure_VectorType_RecordType_core_ClientLegalEntity,
    to_structure_VectorType_RecordType_core_ClientDivision,
    to_structure_VectorType_RecordType_core_ClientUnit,
    to_structure_VectorType_RecordType_core_StatutoryDate,
    to_structure_VectorType_RecordType_clientreport_ComplianceDetailsUnitWise,
    to_structure_VectorType_RecordType_core_ComplianceFilter,
    to_structure_VectorType_RecordType_clientreport_RiskData,
    to_structure_VectorType_RecordType_clientreport_Level1Compliance,
    to_structure_RecordType_clientreport_STATUTORY_WISE_NOTIFICATIONS,
    to_structure_VectorType_RecordType_clientreport_STATUTORY_WISE_NOTIFICATIONS,
    to_structure_VectorType_RecordType_clientreports_LEVEL_1_STATUTORY_NOTIFICATIONS,
    to_structure_MapType_CustomTextType_500_VectorType_RecordType_clientreport_LEVEL_1_STATUTORY_NOTIFICATIONS,
    to_structure_VectorType_CustomTextType_100,
    to_structure_VectorType_RecordType_clientreport_ActivityData,
    to_structure_MapType_CustomTextType_500_MapType_CustomTextType_500_VectorType_RecordType_clientreport_ActivityData,
    to_structure_OptionalType_VectorType_SignedIntegerType_8,
    to_structure_VectorType_RecordType_client_report_GroupedUnits,
    to_structure_VectorType_RecordType_client_report_UnitDetails,
    to_structure_OptionalType_UnsignedIntegerType_32,
    to_structure_UnsignedIntegerType_32,
    to_structure_VectorType_SignedIntegerType_8,
    to_structure_VectorType_CustomTextType_500,
    to_structure_OptionalType_CustomTextType_500,
    to_structure_Text,
    to_structure_VectorType_Text,
    to_structure_OptionalType_Text,
    to_structure_Bool,
    to_structure_OptionalType_VectorType_CustomTextType_500,
    to_structure_MapType_CustomTextType_500_MapType_CustomTextType_500_VectorType_RecordType_clientreport_ActivityData,
    to_structure_VectorType_RecordType_clientreport_GetComplianceTaskApplicabilityStatusReportData,
    to_structure_OptionalType_CustomTextType_250,

)

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

class GetComplianceDetailsReportFilters(Request):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return GetComplianceDetailsReportFilters()

    def to_inner_structure(self):
        return {
        }

class GetComplianceDetailsReport(Request):
    def __init__(
        self, country_id, domain_id, statutory_id, unit_id, compliance_id, assignee_id, from_date,
        to_date, compliance_status, csv, from_count, page_count
    ):
        self.country_id = country_id
        self.domain_id = domain_id
        self.statutory_id = statutory_id
        self.unit_id = unit_id
        self.compliance_id = compliance_id
        self.assignee_id = assignee_id
        self.from_date = from_date
        self.to_date = to_date
        self.compliance_status = compliance_status
        self.csv = csv
        self.from_count = from_count
        self.page_count = page_count

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
                "country_id", "domain_id", "statutory_id", "unit_id", "compliance_id", "assignee_id",
                "from_date", "to_date", "compliance_status", "csv",
                "from_count", "page_count"
            ]
        )
        country_id = data.get("country_id")
        country_id = parse_structure_UnsignedIntegerType_32(country_id)
        domain_id = data.get("domain_id")
        domain_id = parse_structure_UnsignedIntegerType_32(domain_id)
        statutory_id = data.get("statutory_id")
        statutory_id = parse_structure_OptionalType_CustomTextType_100(statutory_id)
        unit_id = data.get("unit_id")
        unit_id = parse_structure_OptionalType_SignedIntegerType_8(unit_id)
        compliance_id = data.get("compliance_id")
        compliance_id = parse_structure_OptionalType_SignedIntegerType_8(compliance_id)
        assignee_id = data.get("assignee_id")
        assignee_id = parse_structure_OptionalType_SignedIntegerType_8(assignee_id)
        from_date = data.get("from_date")
        from_date = parse_structure_OptionalType_CustomTextType_20(from_date)
        to_date = data.get("to_date")
        to_date = parse_structure_OptionalType_CustomTextType_20(to_date)
        compliance_status = data.get("compliance_status")
        compliance_status = parse_structure_OptionalType_CustomTextType_50(compliance_status)
        csv = data.get("csv")
        csv = parse_structure_Bool(csv)
        from_count = data.get("from_count")
        from_count = parse_structure_UnsignedIntegerType_32(from_count)
        page_count = data.get("page_count")
        page_count = parse_structure_UnsignedIntegerType_32(page_count)
        return GetComplianceDetailsReport(
            country_id, domain_id, statutory_id, unit_id, compliance_id, assignee_id, from_date,
            to_date, compliance_status, csv, from_count, page_count
        )

    def to_inner_structure(self):
        return {
            "country_id": to_structure_SignedIntegerType_8(self.country_id),
            "domain_id": to_structure_SignedIntegerType_8(self.domain_id),
            "statutory_id": to_structure_OptionalType_CustomTextType_100(self.statutory_id),
            "unit_id": to_structure_OptionalType_SignedIntegerType_8(self.unit_id),
            "compliance_id": to_structure_OptionalType_SignedIntegerType_8(self.compliance_id),
            "assignee_id": to_structure_OptionalType_SignedIntegerType_8(self.assignee_id),
            "from_date": to_structure_OptionalType_CustomTextType_20(self.from_date),
            "to_date": to_structure_OptionalType_CustomTextType_20(self.to_date),
            "compliance_status": to_structure_OptionalType_CustomTextType_50(self.compliance_status),
            "csv": to_structure_Bool(self.csv),
            "from_count": to_structure_UnsignedIntegerType_32(self.from_count),
            "page_count": to_structure_UnsignedIntegerType_32(self.page_count)
        }

class GetServiceProviderReportFilters(Request):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return GetServiceProviderReportFilters()

    def to_inner_structure(self):
        return {
        }

class GetServiceProviderWiseCompliance(Request):
    def __init__(self, country_id, domain_id, statutory_id, unit_id, service_provider_id, from_count, page_count, csv):
        self.country_id = country_id
        self.domain_id = domain_id
        self.statutory_id = statutory_id
        self.unit_id = unit_id
        self.service_provider_id = service_provider_id
        self.from_count = from_count
        self.page_count = page_count
        self.csv = csv

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "country_id", "domain_id", "statutory_id", "unit_id", "service_provider_id", "from_count", "page_count", "csv"
        ])
        country_id = data.get("country_id")
        country_id = parse_structure_UnsignedIntegerType_32(country_id)
        domain_id = data.get("domain_id")
        domain_id = parse_structure_UnsignedIntegerType_32(domain_id)
        statutory_id = data.get("statutory_id")
        statutory_id = parse_structure_OptionalType_CustomTextType_100(statutory_id)
        unit_id = data.get("unit_id")
        unit_id = parse_structure_OptionalType_SignedIntegerType_8(unit_id)
        service_provider_id = data.get("service_provider_id")
        service_provider_id = parse_structure_OptionalType_SignedIntegerType_8(service_provider_id)
        from_count = data.get("from_count")
        from_count = parse_structure_UnsignedIntegerType_32(from_count)
        page_count = data.get("page_count")
        page_count = parse_structure_UnsignedIntegerType_32(page_count)
        csv = data.get("csv")
        csv = parse_structure_Bool(csv)
        return GetServiceProviderWiseCompliance(
            country_id, domain_id, statutory_id, unit_id,
            service_provider_id, from_count, page_count, csv
        )

    def to_inner_structure(self):
        return {
            "country_id": to_structure_SignedIntegerType_8(self.country_id),
            "domain_id": to_structure_SignedIntegerType_8(self.domain_id),
            "statutory_id": to_structure_OptionalType_CustomTextType_100(self.statutory_id),
            "unit_id": to_structure_OptionalType_SignedIntegerType_8(self.unit_id),
            "service_provider_id": to_structure_OptionalType_SignedIntegerType_8(self.service_provider_id),
            "from_count": to_structure_UnsignedIntegerType_32(self.from_count),
            "page_count": to_structure_UnsignedIntegerType_32(self.page_count),
            "csv": to_structure_Bool(self.csv)
        }

class GetClientReportFilters(Request):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return GetClientReportFilters()

    def to_inner_structure(self):
        return {
        }

class GetAssigneewisecomplianceReport(Request):
    def __init__(
        self, country_id, domain_id, business_group_id,
        legal_entity_id, division_id, unit_id, user_id,
        from_count, page_count
    ):
        self.country_id = country_id
        self.domain_id = domain_id
        self.business_group_id = business_group_id
        self.legal_entity_id = legal_entity_id
        self.division_id = division_id
        self.unit_id = unit_id
        self.user_id = user_id
        self.from_count = from_count
        self.page_count = page_count

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "country_id", "domain_id", "business_group_id",
            "legal_entity_id", "division_id", "unit_id", "user_id",
            "from_count", "page_count"
        ])
        country_id = data.get("country_id")
        country_id = parse_structure_UnsignedIntegerType_32(country_id)
        domain_id = data.get("domain_id")
        domain_id = parse_structure_UnsignedIntegerType_32(domain_id)
        business_group_id = data.get("business_group_id")
        business_group_id = parse_structure_OptionalType_SignedIntegerType_8(business_group_id)
        legal_entity_id = data.get("legal_entity_id")
        legal_entity_id = parse_structure_OptionalType_SignedIntegerType_8(legal_entity_id)
        division_id = data.get("division_id")
        division_id = parse_structure_OptionalType_SignedIntegerType_8(division_id)
        unit_id = data.get("unit_id")
        unit_id = parse_structure_OptionalType_SignedIntegerType_8(unit_id)
        user_id = data.get("user_id")
        user_id = parse_structure_OptionalType_SignedIntegerType_8(user_id)
        from_count = data.get("from_count")
        from_count = parse_structure_UnsignedIntegerType_32(from_count)
        page_count = data.get("page_count")
        page_count = parse_structure_UnsignedIntegerType_32(page_count)
        return GetAssigneewisecomplianceReport(
            country_id, domain_id, business_group_id, legal_entity_id,
            division_id, unit_id, user_id, from_count, page_count
        )

    def to_inner_structure(self):
        return {
            "country_id": to_structure_SignedIntegerType_8(self.country_id),
            "domain_id": to_structure_SignedIntegerType_8(self.domain_id),
            "business_group_id": to_structure_OptionalType_SignedIntegerType_8(self.business_group_id),
            "legal_entity_id": to_structure_OptionalType_SignedIntegerType_8(self.legal_entity_id),
            "division_id": to_structure_OptionalType_SignedIntegerType_8(self.division_id),
            "unit_id": to_structure_OptionalType_SignedIntegerType_8(self.unit_id),
            "user_id": to_structure_OptionalType_SignedIntegerType_8(self.user_id),
            "from_count": to_structure_UnsignedIntegerType_32(self.from_count),
            "page_count": to_structure_UnsignedIntegerType_32(self.page_count)
        }


class GetUnitwisecomplianceReport(Request):
    def __init__(
        self, country_id, domain_id, business_group_id,
        legal_entity_id, division_id, unit_id, user_id,
        from_count, page_count
    ):
        self.country_id = country_id
        self.domain_id = domain_id
        self.business_group_id = business_group_id
        self.legal_entity_id = legal_entity_id
        self.division_id = division_id
        self.unit_id = unit_id
        self.user_id = user_id
        self.from_count = from_count
        self.page_count = page_count

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "country_id", "domain_id", "business_group_id",
            "legal_entity_id", "division_id", "unit_id",
            "user_id", "from_count", "page_count"
        ])
        country_id = data.get("country_id")
        country_id = parse_structure_UnsignedIntegerType_32(country_id)
        domain_id = data.get("domain_id")
        domain_id = parse_structure_UnsignedIntegerType_32(domain_id)
        business_group_id = data.get("business_group_id")
        business_group_id = parse_structure_OptionalType_SignedIntegerType_8(business_group_id)
        legal_entity_id = data.get("legal_entity_id")
        legal_entity_id = parse_structure_OptionalType_SignedIntegerType_8(legal_entity_id)
        division_id = data.get("division_id")
        division_id = parse_structure_OptionalType_SignedIntegerType_8(division_id)
        unit_id = data.get("unit_id")
        unit_id = parse_structure_OptionalType_SignedIntegerType_8(unit_id)
        user_id = data.get("user_id")
        user_id = parse_structure_OptionalType_SignedIntegerType_8(user_id)
        from_count = data.get("from_count")
        from_count = parse_structure_UnsignedIntegerType_32(from_count)
        page_count = data.get("page_count")
        page_count = parse_structure_UnsignedIntegerType_32(page_count)
        return GetUnitwisecomplianceReport(
            country_id, domain_id, business_group_id, legal_entity_id,
            division_id, unit_id, user_id, from_count, page_count
        )

    def to_inner_structure(self):
        return {
            "country_id": to_structure_SignedIntegerType_8(self.country_id),
            "domain_id": to_structure_SignedIntegerType_8(self.domain_id),
            "business_group_id": to_structure_OptionalType_SignedIntegerType_8(self.business_group_id),
            "legal_entity_id": to_structure_OptionalType_SignedIntegerType_8(self.legal_entity_id),
            "division_id": to_structure_OptionalType_SignedIntegerType_8(self.division_id),
            "unit_id": to_structure_OptionalType_SignedIntegerType_8(self.unit_id),
            "user_id": to_structure_OptionalType_SignedIntegerType_8(self.user_id),
            "from_count": to_structure_UnsignedIntegerType_32(self.from_count),
            "page_count": to_structure_UnsignedIntegerType_32(self.page_count)
        }

class GetReassignComplianceTaskReportFilters(Request):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return GetReassignComplianceTaskReportFilters()

    def to_inner_structure(self):
        return {
        }

class GetReassignComplianceTaskDetails(Request):
    def __init__(self, country_id, domain_id, unit_id, statutory_id, compliance_id, user_id, from_date, to_date):
        self.country_id = country_id
        self.domain_id = domain_id
        self.unit_id = unit_id
        self.statutory_id = statutory_id
        self.compliance_id = compliance_id
        self.user_id = user_id
        self.from_date = from_date
        self.to_date = to_date

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["country_id", "domain_id", "unit_id", "statutory_id", "compliance_id", "user_id", "from_date", "to_date"])
        country_id = data.get("country_id")
        country_id = parse_structure_UnsignedIntegerType_32(country_id)
        domain_id = data.get("domain_id")
        domain_id = parse_structure_UnsignedIntegerType_32(domain_id)
        unit_id = data.get("unit_id")
        unit_id = parse_structure_OptionalType_SignedIntegerType_8(unit_id)
        statutory_id = data.get("statutory_id")
        statutory_id = parse_structure_OptionalType_SignedIntegerType_8(statutory_id)
        compliance_id = data.get("compliance_id")
        compliance_id = parse_structure_OptionalType_SignedIntegerType_8(compliance_id)
        user_id = data.get("user_id")
        user_id = parse_structure_OptionalType_SignedIntegerType_8(user_id)
        from_date = data.get("from_date")
        from_date = parse_structure_OptionalType_CustomTextType_20(from_date)
        to_date = data.get("to_date")
        to_date = parse_structure_OptionalType_CustomTextType_20(to_date)
        return GetReassignComplianceTaskDetails(country_id, domain_id, unit_id, statutory_id, compliance_id, user_id, from_date, to_date)

    def to_inner_structure(self):
        return {
            "country_id": to_structure_SignedIntegerType_8(self.country_id),
            "domain_id": to_structure_SignedIntegerType_8(self.domain_id),
            "unit_id": to_structure_OptionalType_SignedIntegerType_8(self.unit_id),
            "statutory_id": to_structure_OptionalType_SignedIntegerType_8(self.statutory_id),
            "compliance_id": to_structure_OptionalType_SignedIntegerType_8(self.compliance_id),
            "user_id": to_structure_OptionalType_SignedIntegerType_8(self.user_id),
            "from_date": to_structure_OptionalType_CustomTextType_20(self.from_date),
            "to_date": to_structure_OptionalType_CustomTextType_20(self.to_date),
        }

class GetClientDetailsReportFilters(Request):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return GetClientDetailsReportFilters()

    def to_inner_structure(self):
        return {
        }


class GetClientDetailsReportData(Request):
    def __init__(
        self, country_id, business_group_id, legal_entity_id, division_id,
        unit_id, domain_ids, csv, from_count, page_count
    ):
        self.country_id = country_id
        self.business_group_id = business_group_id
        self.legal_entity_id = legal_entity_id
        self.division_id = division_id
        self.unit_id = unit_id
        self.domain_ids = domain_ids
        self.csv = csv
        self.from_count = from_count
        self.page_count = page_count

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(
            data, [
                "country_id", "business_group_id", "legal_entity_id", "division_id",
                "unit_id", "domain_ids", "csv", "from_count", "page_count"
            ]
        )
        country_id = data.get("country_id")
        country_id = parse_structure_UnsignedIntegerType_32(country_id)
        business_group_id = data.get("business_group_id")
        business_group_id = parse_structure_OptionalType_SignedIntegerType_8(business_group_id)
        legal_entity_id = data.get("legal_entity_id")
        legal_entity_id = parse_structure_OptionalType_SignedIntegerType_8(legal_entity_id)
        division_id = data.get("division_id")
        division_id = parse_structure_OptionalType_SignedIntegerType_8(division_id)
        unit_id = data.get("unit_id")
        unit_id = parse_structure_OptionalType_SignedIntegerType_8(unit_id)
        domain_ids = data.get("domain_ids")
        domain_ids = parse_structure_OptionalType_VectorType_SignedIntegerType_8(domain_ids)
        csv = data.get("csv")
        csv = parse_structure_Bool(csv)
        from_count = data.get("from_count")
        from_count = parse_structure_UnsignedIntegerType_32(from_count)
        page_count = data.get("page_count")
        page_count = parse_structure_UnsignedIntegerType_32(page_count)
        return GetClientDetailsReportData(
            country_id, business_group_id, legal_entity_id, division_id,
            unit_id, domain_ids, csv, from_count, page_count
        )

    def to_inner_structure(self):
        return {
            "country_id": to_structure_SignedIntegerType_8(self.country_id),
            "business_group_id": to_structure_OptionalType_SignedIntegerType_8(self.business_group_id),
            "legal_entity_id": to_structure_OptionalType_SignedIntegerType_8(self.legal_entity_id),
            "division_id": to_structure_OptionalType_SignedIntegerType_8(self.division_id),
            "unit_id": to_structure_OptionalType_SignedIntegerType_8(self.unit_id),
            "domain_ids": to_structure_OptionalType_VectorType_SignedIntegerType_8(self.domain_ids),
            "csv": to_structure_Bool(self.csv),
            "from_count": to_structure_UnsignedIntegerType_32(self.from_count),
            "page_count": to_structure_UnsignedIntegerType_32(self.page_count)
        }

class GetTaskApplicabilityStatusFilters(Request):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return GetTaskApplicabilityStatusFilters()

    def to_inner_structure(self):
        return {
        }

class GetComplianceTaskApplicabilityStatusReport(Request):
    def __init__(
        self, country_id, domain_id, business_group_id, legal_entity_id, division_id, unit_id,
        statutory_name, applicable_status, csv, record_count
    ):
        self.country_id = country_id
        self.domain_id = domain_id
        self.business_group_id = business_group_id
        self.legal_entity_id = legal_entity_id
        self.division_id = division_id
        self.unit_id = unit_id
        self.statutory_name = statutory_name
        self.applicable_status = applicable_status
        self.csv = csv
        self.record_count = record_count

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
                "country_id", "domain_id", "business_group_id", "legal_entity_id", "division_id",
                "unit_id", "statutory_name", "applicable_status", "csv", "record_count"
            ]
        )
        country_id = data.get("country_id")
        country_id = parse_structure_UnsignedIntegerType_32(country_id)
        domain_id = data.get("domain_id")
        domain_id = parse_structure_UnsignedIntegerType_32(domain_id)
        business_group_id = data.get("business_group_id")
        business_group_id = parse_structure_OptionalType_SignedIntegerType_8(business_group_id)
        legal_entity_id = data.get("legal_entity_id")
        legal_entity_id = parse_structure_OptionalType_SignedIntegerType_8(legal_entity_id)
        division_id = data.get("division_id")
        division_id = parse_structure_OptionalType_SignedIntegerType_8(division_id)
        unit_id = data.get("unit_id")
        unit_id = parse_structure_OptionalType_SignedIntegerType_8(unit_id)
        statutory_name = data.get("statutory_name")
        statutory_name = parse_structure_OptionalType_CustomTextType_100(statutory_name)
        applicable_status = data.get("applicable_status")
        applicable_status = parse_structure_OptionalType_EnumType_core_APPLICABILITY_STATUS(applicable_status)
        csv = data.get("csv")
        csv = parse_structure_Bool(csv)
        record_count = data.get("record_count")
        record_count = parse_structure_UnsignedIntegerType_32(record_count)
        return GetComplianceTaskApplicabilityStatusReport(
            country_id, domain_id, business_group_id, legal_entity_id,
            division_id, unit_id,
            statutory_name, applicable_status, csv, record_count
        )

    def to_inner_structure(self):
        return {
            "country_id": to_structure_SignedIntegerType_8(self.country_id),
            "domain_id": to_structure_SignedIntegerType_8(self.domain_id),
            "business_group_id": to_structure_OptionalType_SignedIntegerType_8(self.business_group_id),
            "legal_entity_id": to_structure_OptionalType_SignedIntegerType_8(self.legal_entity_id),
            "division_id": to_structure_OptionalType_SignedIntegerType_8(self.division_id),
            "unit_id": to_structure_OptionalType_SignedIntegerType_8(self.unit_id),
            "statutory_name": to_structure_OptionalType_CustomTextType_100(self.statutory_name),
            "applicable_status": to_structure_OptionalType_EnumType_core_APPLICABILITY_STATUS(self.applicable_status),
            "csv": to_structure_Bool(self.csv),
            "record_count": to_structure_UnsignedIntegerType_32(self.record_count)
        }

class GetComplianceActivityReportFilters(Request):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return GetComplianceActivityReportFilters()

    def to_inner_structure(self):
        return {
        }

class GetComplianceActivityReport(Request):
    def __init__(
        self, user_type, user_id, domain_id, country_id, level_1_statutory_name, unit_id,
        compliance_id, from_date, to_date,  csv
    ):
        self.user_type = user_type
        self.user_id = user_id
        self.domain_id = domain_id
        self.country_id = country_id
        self.level_1_statutory_name = level_1_statutory_name
        self.unit_id = unit_id
        self.compliance_id = compliance_id
        self.from_date = from_date
        self.to_date = to_date
        self.csv = csv

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(
            data, [
                "user_type", "user_id", "domain_id", "country_id",
                "level_1_statutory_name", "unit_id", "compliance_id",
                "from_date", "to_date", "csv"
            ]
        )
        user_type = data.get("user_type")
        user_type = parse_structure_EnumType_core_USER_TYPE(user_type)
        user_id = data.get("user_id")
        user_id = parse_structure_OptionalType_SignedIntegerType_8(user_id)
        domain_id = data.get("domain_id")
        domain_id = parse_structure_UnsignedIntegerType_32(domain_id)
        country_id = data.get("country_id")
        country_id = parse_structure_UnsignedIntegerType_32(country_id)
        level_1_statutory_name = data.get("level_1_statutory_name")
        level_1_statutory_name = parse_structure_OptionalType_CustomTextType_100(level_1_statutory_name)
        unit_id = data.get("unit_id")
        unit_id = parse_structure_OptionalType_SignedIntegerType_8(unit_id)
        compliance_id = data.get("compliance_id")
        compliance_id = parse_structure_OptionalType_SignedIntegerType_8(compliance_id)
        from_date = data.get("from_date")
        from_date = parse_structure_OptionalType_CustomTextType_20(from_date)
        to_date = data.get("to_date")
        to_date = parse_structure_OptionalType_CustomTextType_20(to_date)
        csv = data.get("csv")
        csv = parse_structure_Bool(csv)
        return GetComplianceActivityReport(
            user_type, user_id, domain_id, country_id, level_1_statutory_name, unit_id, compliance_id,
            from_date, to_date, csv
        )

    def to_inner_structure(self):
        return {
            "user_type": to_structure_EnumType_core_USER_TYPE(self.user_type),
            "user_id": to_structure_OptionalType_SignedIntegerType_8(self.user_id),
            "domain_id": to_structure_SignedIntegerType_8(self.domain_id),
            "country_id": to_structure_SignedIntegerType_8(self.country_id),
            "level_1_statutory_name": to_structure_OptionalType_CustomTextType_100(self.level_1_statutory_name),
            "unit_id": to_structure_OptionalType_SignedIntegerType_8(self.unit_id),
            "compliance_id": to_structure_OptionalType_SignedIntegerType_8(self.compliance_id),
            "from_date": to_structure_OptionalType_CustomTextType_20(self.from_date),
            "to_date": to_structure_OptionalType_CustomTextType_20(self.to_date),
            "csv" : to_structure_Bool(self.csv)
        }

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
        self, c_id, legal_entity_id, d_id, unit_id, act, compliance_id,
        usr_id, from_date, to_date, csv, f_count, t_count
    ):
        self.c_id = c_id
        self.legal_entity_id = legal_entity_id
        self.d_id = d_id
        self.unit_id = unit_id
        self.act = act
        self.compliance_id = compliance_id
        self.usr_id = usr_id
        self.from_date = from_date
        self.to_date = to_date
        self.csv = csv
        self.f_count = f_count
        self.t_count = t_count

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "c_id", "le_id", "d_id", "unit_id", "act", "compliance_id",
            "usr_id", "from_date", "to_date", "csv", "f_count", "t_count"]
        )
        c_id = data.get("c_id")
        legal_entity_id = data.get("le_id")
        d_id = data.get("d_id")
        unit_id = data.get("unit_id")
        act = data.get("act")
        compliance_id = data.get("compliance_id")
        usr_id = data.get("usr_id")
        from_date = data.get("from_date")
        to_date = data.get("to_date")
        csv = data.get("csv")
        f_count = data.get("f_count")
        t_count = data.get("t_count")
        return GetReassignedHistoryReport(
            c_id, legal_entity_id, d_id, unit_id, act, compliance_id,
            usr_id, from_date, to_date, csv, f_count, t_count)

    def to_inner_structure(self):
        return {
            "c_id": self.c_id,
            "le_id": self.legal_entity_id,
            "d_id": self.d_id,
            "unit_id": self.unit_id,
            "act": self.act,
            "compliance_id": self.compliance_id,
            "usr_id": self.usr_id,
            "from_date": self.from_date,
            "to_date": self.to_date,
            "csv": self.csv,
            "f_count": self.f_count,
            "t_count": self.t_count
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
        self, c_id, legal_entity_id, d_id, unit_id, act, compliance_id, frequency_id, user_type_id, status_name,
        usr_id, from_date, to_date, csv, f_count, t_count
    ):
        self.c_id = c_id
        self.legal_entity_id = legal_entity_id
        self.d_id = d_id
        self.unit_id = unit_id
        self.act = act
        self.compliance_id = compliance_id
        self.frequency_id = frequency_id
        self.user_type_id = user_type_id
        self.status_name = status_name
        self.usr_id = usr_id
        self.from_date = from_date
        self.to_date = to_date
        self.csv = csv
        self.f_count = f_count
        self.t_count = t_count

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "c_id", "le_id", "d_id", "unit_id", "act", "compliance_id", "frequency_id", "user_type_id", "status_name",
            "usr_id", "from_date", "to_date", "csv", "f_count", "t_count"]
        )
        c_id = data.get("c_id")
        legal_entity_id = data.get("le_id")
        d_id = data.get("d_id")
        unit_id = data.get("unit_id")
        act = data.get("act")
        compliance_id = data.get("compliance_id")
        frequency_id = data.get("frequency_id")
        user_type_id = data.get("user_type_id")
        status_name = data.get("status_name")
        usr_id = data.get("usr_id")
        from_date = data.get("from_date")
        to_date = data.get("to_date")
        csv = data.get("csv")
        f_count = data.get("f_count")
        t_count = data.get("t_count")
        return GetStatusReportConsolidated(
            c_id, legal_entity_id, d_id, unit_id, act, compliance_id, frequency_id, user_type_id, status_name,
            usr_id, from_date, to_date, csv, f_count, t_count)

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
            "t_count": self.t_count
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
        compliance_id, frequency_id, status_name, csv, f_count, t_count
    ):
        self.c_id = c_id
        self.bg_id = bg_id
        self.legal_entity_id = legal_entity_id
        self.d_id = d_id
        self.unit_id = unit_id
        self.div_id = div_id
        self.cat_id = cat_id
        self.act = act
        self.compliance_id = compliance_id
        self.frequency_id = frequency_id
        self.status_name = status_name
        self.csv = csv
        self.f_count = f_count
        self.t_count = t_count

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "c_id", "bg_id", "le_id", "d_id", "unit_id", "div_id", "cat_id", "act", "compliance_id",
            "frequency_id", "status_name", "csv", "f_count", "t_count"]
        )
        c_id = data.get("c_id")
        bg_id = data.get("bg_id")
        legal_entity_id = data.get("le_id")
        d_id = data.get("d_id")
        unit_id = data.get("unit_id")
        div_id = data.get("div_id")
        cat_id = data.get("cat_id")
        act = data.get("act")
        compliance_id = data.get("compliance_id")
        frequency_id = data.get("frequency_id")
        status_name = data.get("status_name")
        csv = data.get("csv")
        f_count = data.get("f_count")
        t_count = data.get("t_count")
        return GetStatutorySettingsUnitWise(
            c_id, bg_id, legal_entity_id, d_id, unit_id, div_id, cat_id, act, compliance_id,
            frequency_id, status_name, csv, f_count, t_count)

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
            "compliance_id": self.compliance_id,
            "frequency_id": self.frequency_id,
            "status_name": self.status_name,
            "csv": self.csv,
            "f_count": self.f_count,
            "t_count": self.t_count
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

class GetStatutoryNotificationsListFilters(Request):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return GetStatutoryNotificationsListFilters()

    def to_inner_structure(self):
        return {
        }

class GetStatutoryNotificationsListReport(Request):
    def __init__(
        self, country_name, domain_name,  business_group_id, legal_entity_id, division_id,
        unit_id, level_1_statutory_name, from_date, to_date, csv
    ):
        self.country_name = country_name
        self.domain_name = domain_name
        self.business_group_id = business_group_id
        self.legal_entity_id = legal_entity_id
        self.division_id = division_id
        self.unit_id = unit_id
        self.level_1_statutory_name = level_1_statutory_name
        self.from_date = from_date
        self.to_date = to_date
        self.csv = csv

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "country_name", "domain_name", "business_group_id", "legal_entity_id",
            "division_id", "unit_id", "level_1_statutory_name",
            "from_date", "to_date", "csv"
        ])
        country_name = data.get("country_name")
        country_name = parse_structure_CustomTextType_50(country_name)
        domain_name = data.get("domain_name")
        domain_name = parse_structure_CustomTextType_50(domain_name)
        business_group_id = data.get("business_group_id")
        business_group_id = parse_structure_OptionalType_SignedIntegerType_8(business_group_id)
        legal_entity_id = data.get("legal_entity_id")
        legal_entity_id = parse_structure_OptionalType_SignedIntegerType_8(legal_entity_id)
        division_id = data.get("division_id")
        division_id = parse_structure_OptionalType_SignedIntegerType_8(division_id)
        unit_id = data.get("unit_id")
        unit_id = parse_structure_OptionalType_SignedIntegerType_8(unit_id)
        level_1_statutory_name = data.get("level_1_statutory_name")
        level_1_statutory_name = parse_structure_OptionalType_CustomTextType_100(level_1_statutory_name)
        from_date = data.get("from_date")
        from_date = parse_structure_OptionalType_CustomTextType_20(from_date)
        to_date = data.get("to_date")
        to_date = parse_structure_OptionalType_CustomTextType_20(to_date)
        csv = data.get("csv")
        csv = parse_structure_Bool(csv)
        return GetStatutoryNotificationsListReport(
            country_name, domain_name, business_group_id, legal_entity_id, division_id,
            unit_id, level_1_statutory_name, from_date, to_date, csv
        )

    def to_inner_structure(self):
        return {
            "country_name": to_structure_CustomTextType_50(self.country_name),
            "domain_name": to_structure_CustomTextType_50(self.domain_name),
            "business_group_id": to_structure_OptionalType_SignedIntegerType_8(self.business_group_id),
            "legal_entity_id": to_structure_OptionalType_SignedIntegerType_8(self.legal_entity_id),
            "division_id": to_structure_OptionalType_SignedIntegerType_8(self.division_id),
            "unit_id": to_structure_OptionalType_SignedIntegerType_8(self.unit_id),
            "level_1_statutory_name": to_structure_OptionalType_CustomTextType_100(self.level_1_statutory_name),
            "from_date": to_structure_OptionalType_CustomTextType_20(self.from_date),
            "to_date": to_structure_OptionalType_CustomTextType_20(self.to_date),
            "csv": to_structure_Bool(self.csv)
        }

class GetActivityLogFilters(Request):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return GetActivityLogFilters()

    def to_inner_structure(self):
        return {
        }

class GetActivityLogReport(Request):
    def __init__(self, from_date, to_date, form_name, action):
        self.from_date = from_date
        self.to_date = to_date
        self.form_name = form_name
        self.action = action

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["from_date", "to_date", "form_name", "action"])
        from_date = data.get("from_date")
        from_date = parse_structure_CustomTextType_20(from_date)
        to_date = data.get("to_date")
        to_date = parse_structure_CustomTextType_20(to_date)
        form_name = data.get("form_name")
        form_name = parse_structure_OptionalType_CustomTextType_20(form_name)
        action = data.get("action")
        action = parse_structure_OptionalType_CustomTextType_100(action)
        return GetActivityLogReport(from_date, to_date, form_name, action)

    def to_inner_structure(self):
        return {
            "from_date": to_structure_CustomTextType_20(self.from_date),
            "to_date": to_structure_CustomTextType_20(self.to_date),
            "form_name": to_structure_OptionalType_CustomTextType_20(self.form_name),
            "action": to_structure_OptionalType_CustomTextType_100(self.action),
        }

class GetLoginTrace(Request):
    def __init__(self, record_count, user_id, from_date, to_date):
        self.record_count = record_count
        self.user_id = user_id
        self.from_date = from_date
        self.to_date = to_date

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["record_count", "user_id", "from_date", "to_date"])
        record_count = data.get("record_count")
        record_count = parse_structure_UnsignedIntegerType_32(record_count)
        user_id = data.get("user_id")
        user_id = parse_structure_OptionalType_UnsignedIntegerType_32(user_id)
        from_date = data.get("from_date")
        from_date = parse_structure_OptionalType_CustomTextType_20(from_date)
        to_date = data.get("to_date")
        to_date = parse_structure_OptionalType_CustomTextType_20(to_date)
        return GetLoginTrace(record_count, user_id, from_date, to_date)

    def to_inner_structure(self):
        return {
            "record_count": to_structure_UnsignedIntegerType_32(self.record_count),
            "user_id": to_structure_OptionalType_UnsignedIntegerType_32(self.user_id),
            "from_date": to_structure_OptionalType_CustomTextType_20(self.from_date),
            "to_date": to_structure_OptionalType_CustomTextType_20(self.to_date)
        }

class GetLegalEntityWiseReportFilters(Request):
    def __init__(self, country_id, legal_entity_id):
        self.country_id = country_id
        self.legal_entity_id = legal_entity_id

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["country_id", "legal_entity_id"])
        country_id = data.get("country_id")
        legal_entity_id = data.get("legal_entity_id")
        return GetLegalEntityWiseReportFilters(country_id, legal_entity_id)

    def to_inner_structure(self):
        return {
            "country_id": self.country_id,
            "legal_entity_id": self.legal_entity_id,
        }

class GetLegalEntityWiseReport(Request):
    def __init__(
        self, country_id, legal_entity_id, domain_id, unit_id, statutory_mapping,
        compliance_id, frequency_id, user_type, user_id, due_from_date,
        due_to_date, task_status, csv, from_count, page_count
    ):
        self.country_id = country_id
        self.legal_entity_id = legal_entity_id
        self.domain_id = domain_id
        self.unit_id = unit_id
        self.statutory_mapping = statutory_mapping
        self.compliance_id = compliance_id
        self.frequency_id = frequency_id
        self.user_type = user_type
        self.user_id = user_id
        self.due_from_date = due_from_date
        self.due_to_date = due_to_date
        self.task_status = task_status
        self.csv = csv
        self.from_count = from_count
        self.page_count = page_count

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "country_id", "legal_entity_id", "domain_id", "unit_id", "statutory_mapping",
            "compliance_id", "frequency_id", "user_type", "user_id", "due_from_date",
            "due_to_date", "task_status", "csv", "from_count", "page_count"
        ])
        country_id = data.get("country_id")
        legal_entity_id = data.get("legal_entity_id")
        domain_id = data.get("domain_id")
        unit_id = data.get("unit_id")
        statutory_mapping = data.get("statutory_mapping")
        compliance_id = data.get("compliance_id")
        frequency_id = data.get("frequency_id")
        user_type = data.get("user_type")
        user_id = data.get("user_id")
        due_from_date = data.get("due_from_date")
        due_to_date = data.get("due_to_date")
        task_status = data.get("task_status")
        csv = data.get("csv")
        from_count = data.get("from_count")
        page_count = data.get("page_count")
        return GetLegalEntityWiseReport(
            country_id, legal_entity_id, domain_id, unit_id, statutory_mapping,
            compliance_id, frequency_id, user_type, user_id, due_from_date,
            due_to_date, task_status, csv, from_count, page_count
        )

    def to_inner_structure(self):
        return {
            "country_id": self.country_id,
            "legal_entity_id": self.legal_entity_id,
            "domain_id": self.domain_id,
            "unit_id": self.unit_id,
            "statutory_mapping": self.statutory_mapping,
            "compliance_id": self.compliance_id,
            "frequency_id": self.frequency_id,
            "user_type": self.user_type,
            "user_id": self.user_id,
            "due_from_date": self.due_from_date,
            "task_status": self.task_status,
            "csv": self.csv,
            "from_count": self.from_count,
            "page_count": self.page_count
        }

class GetDomainWiseReportFilters(Request):
    def __init__(self, country_id, legal_entity_id):
        self.country_id = country_id
        self.legal_entity_id = legal_entity_id

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["country_id", "legal_entity_id"])
        country_id = data.get("country_id")
        legal_entity_id = data.get("legal_entity_id")
        return GetDomainWiseReportFilters(country_id, legal_entity_id)

    def to_inner_structure(self):
        return {
            "country_id": self.country_id,
            "legal_entity_id": self.legal_entity_id,
        }

class GetDomainWiseReport(Request):
    def __init__(
        self, country_id, legal_entity_id, domain_id, unit_id, statutory_mapping,
        compliance_id, frequency_id, user_type, user_id, due_from_date,
        due_to_date, task_status, csv, from_count, page_count
    ):
        self.country_id = country_id
        self.legal_entity_id = legal_entity_id
        self.domain_id = domain_id
        self.unit_id = unit_id
        self.statutory_mapping = statutory_mapping
        self.compliance_id = compliance_id
        self.frequency_id = frequency_id
        self.user_type = user_type
        self.user_id = user_id
        self.due_from_date = due_from_date
        self.due_to_date = due_to_date
        self.task_status = task_status
        self.csv = csv
        self.from_count = from_count
        self.page_count = page_count

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "country_id", "legal_entity_id", "domain_id", "unit_id", "statutory_mapping",
            "compliance_id", "frequency_id", "user_type", "user_id", "due_from_date",
            "due_to_date", "task_status", "csv", "from_count", "page_count"
        ])
        country_id = data.get("country_id")
        legal_entity_id = data.get("legal_entity_id")
        domain_id = data.get("domain_id")
        unit_id = data.get("unit_id")
        statutory_mapping = data.get("statutory_mapping")
        compliance_id = data.get("compliance_id")
        frequency_id = data.get("frequency_id")
        user_type = data.get("user_type")
        user_id = data.get("user_id")
        due_from_date = data.get("due_from_date")
        due_to_date = data.get("due_to_date")
        task_status = data.get("task_status")
        csv = data.get("csv")
        from_count = data.get("from_count")
        page_count = data.get("page_count")
        return GetDomainWiseReport(
            country_id, legal_entity_id, domain_id, unit_id, statutory_mapping,
            compliance_id, frequency_id, user_type, user_id, due_from_date,
            due_to_date, task_status, csv, from_count, page_count
        )

    def to_inner_structure(self):
        return {
            "country_id": self.country_id,
            "legal_entity_id": self.legal_entity_id,
            "domain_id": self.domain_id,
            "unit_id": self.unit_id,
            "statutory_mapping": self.statutory_mapping,
            "compliance_id": self.compliance_id,
            "frequency_id": self.frequency_id,
            "user_type": self.user_type,
            "user_id": self.user_id,
            "due_from_date": self.due_from_date,
            "task_status": self.task_status,
            "csv": self.csv,
            "from_count": self.from_count,
            "page_count": self.page_count
        }

class GetUnitWiseReportFilters(Request):
    def __init__(self, country_id, legal_entity_id):
        self.country_id = country_id
        self.legal_entity_id = legal_entity_id

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["country_id", "legal_entity_id"])
        country_id = data.get("country_id")
        legal_entity_id = data.get("legal_entity_id")
        return GetUnitWiseReportFilters(country_id, legal_entity_id)

    def to_inner_structure(self):
        return {
            "country_id": self.country_id,
            "legal_entity_id": self.legal_entity_id,
        }

class GetUnitWiseReport(Request):
    def __init__(
        self, country_id, legal_entity_id, unit_id, d_id_optional, statutory_mapping,
        compliance_id, frequency_id, user_type, user_id, due_from_date,
        due_to_date, task_status, csv, from_count, page_count
    ):
        self.country_id = country_id
        self.legal_entity_id = legal_entity_id
        self.unit_id = unit_id
        self.d_id_optional = d_id_optional
        self.statutory_mapping = statutory_mapping
        self.compliance_id = compliance_id
        self.frequency_id = frequency_id
        self.user_type = user_type
        self.user_id = user_id
        self.due_from_date = due_from_date
        self.due_to_date = due_to_date
        self.task_status = task_status
        self.csv = csv
        self.from_count = from_count
        self.page_count = page_count

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "country_id", "legal_entity_id", "unit_id", "d_id_optional", "statutory_mapping",
            "compliance_id", "frequency_id", "user_type", "user_id", "due_from_date",
            "due_to_date", "task_status", "csv", "from_count", "page_count"
        ])
        country_id = data.get("country_id")
        legal_entity_id = data.get("legal_entity_id")
        unit_id = data.get("unit_id")
        d_id_optional = data.get("d_id_optional")
        statutory_mapping = data.get("statutory_mapping")
        compliance_id = data.get("compliance_id")
        frequency_id = data.get("frequency_id")
        user_type = data.get("user_type")
        user_id = data.get("user_id")
        due_from_date = data.get("due_from_date")
        due_to_date = data.get("due_to_date")
        task_status = data.get("task_status")
        csv = data.get("csv")
        from_count = data.get("from_count")
        page_count = data.get("page_count")
        return GetUnitWiseReport(
            country_id, legal_entity_id, unit_id, d_id_optional, statutory_mapping,
            compliance_id, frequency_id, user_type, user_id, due_from_date,
            due_to_date, task_status, csv, from_count, page_count
        )

    def to_inner_structure(self):
        return {
            "country_id": self.country_id,
            "legal_entity_id": self.legal_entity_id,
            "unit_id": self.unit_id,
            "d_id_optional": self.d_id_optional,
            "statutory_mapping": self.statutory_mapping,
            "compliance_id": self.compliance_id,
            "frequency_id": self.frequency_id,
            "user_type": self.user_type,
            "user_id": self.user_id,
            "due_from_date": self.due_from_date,
            "due_to_date": self.due_to_date,
            "task_status": self.task_status,
            "csv": self.csv,
            "from_count": self.from_count,
            "page_count": self.page_count
        }

class GetServiceProviderWiseReportFilters(Request):
    def __init__(self, country_id, legal_entity_id):
        self.country_id = country_id
        self.legal_entity_id = legal_entity_id

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["country_id", "legal_entity_id"])
        country_id = data.get("country_id")
        legal_entity_id = data.get("legal_entity_id")
        return GetServiceProviderWiseReportFilters(country_id, legal_entity_id)

    def to_inner_structure(self):
        return {
            "country_id": self.country_id,
            "legal_entity_id": self.legal_entity_id,
        }

class GetServiceProviderWiseReport(Request):
    def __init__(
        self, country_id, legal_entity_id, sp_id, domain_id, unit_id,
        statutory_mapping, compliance_id, user_id, due_from_date,
        due_to_date, task_status, csv, from_count, page_count
    ):
        self.country_id = country_id
        self.legal_entity_id = legal_entity_id
        self.sp_id = sp_id
        self.domain_id = domain_id
        self.unit_id = unit_id
        self.statutory_mapping = statutory_mapping
        self.compliance_id = compliance_id
        self.user_id = user_id
        self.due_from_date = due_from_date
        self.due_to_date = due_to_date
        self.task_status = task_status
        self.csv = csv
        self.from_count = from_count
        self.page_count = page_count

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "country_id", "legal_entity_id", "sp_id", "domain_id", "unit_id",
            "statutory_mapping", "compliance_id", "user_id", "due_from_date",
            "due_to_date", "task_status", "csv", "from_count", "page_count"
        ])
        country_id = data.get("country_id")
        legal_entity_id = data.get("legal_entity_id")
        sp_id = data.get("sp_id")
        domain_id = data.get("domain_id")
        unit_id = data.get("unit_id")
        statutory_mapping = data.get("statutory_mapping")
        compliance_id = data.get("compliance_id")
        user_id = data.get("user_id")
        due_from_date = data.get("due_from_date")
        due_to_date = data.get("due_to_date")
        task_status = data.get("task_status")
        csv = data.get("csv")
        from_count = data.get("from_count")
        page_count = data.get("page_count")
        return GetServiceProviderWiseReport(
            country_id, legal_entity_id, sp_id, domain_id, unit_id,
            statutory_mapping, compliance_id, user_id, due_from_date,
            due_to_date, task_status, csv, from_count, page_count
        )

    def to_inner_structure(self):
        return {
            "country_id": self.country_id,
            "legal_entity_id": self.legal_entity_id,
            "sp_id": self.sp_id,
            "domain_id": self.domain_id,
            "unit_id": self.unit_id,
            "statutory_mapping": self.statutory_mapping,
            "compliance_id": self.compliance_id,
            "user_id": self.user_id,
            "due_from_date": self.due_from_date,
            "due_to_date": self.due_to_date,
            "task_status": self.task_status,
            "csv": self.csv,
            "from_count": self.from_count,
            "page_count": self.page_count
        }

class GetUserWiseReportFilters(Request):
    def __init__(self, country_id, legal_entity_id):
        self.country_id = country_id
        self.legal_entity_id = legal_entity_id

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["country_id", "legal_entity_id"])
        country_id = data.get("country_id")
        legal_entity_id = data.get("legal_entity_id")
        return GetUserWiseReportFilters(country_id, legal_entity_id)

    def to_inner_structure(self):
        return {
            "country_id": self.country_id,
            "legal_entity_id": self.legal_entity_id,
        }

class GetUserWiseReport(Request):
    def __init__(
        self, country_id, legal_entity_id, user_id, domain_id, unit_id,
        statutory_mapping, compliance_id, frequency_id, user_type, due_from_date,
        due_to_date, task_status, csv, from_count, page_count
    ):
        self.country_id = country_id
        self.legal_entity_id = legal_entity_id
        self.user_id = user_id
        self.domain_id = domain_id
        self.unit_id = unit_id
        self.statutory_mapping = statutory_mapping
        self.compliance_id = compliance_id
        self.frequency_id = frequency_id
        self.user_type = user_type
        self.due_from_date = due_from_date
        self.due_to_date = due_to_date
        self.task_status = task_status
        self.csv = csv
        self.from_count = from_count
        self.page_count = page_count

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "country_id", "legal_entity_id", "user_id", "domain_id", "unit_id",
            "statutory_mapping", "compliance_id", "frequency_id", "user_type",
            "due_from_date", "due_to_date", "task_status", "csv", "from_count",
            "page_count"
        ])
        country_id = data.get("country_id")
        legal_entity_id = data.get("legal_entity_id")
        user_id = data.get("user_id")
        domain_id = data.get("domain_id")
        unit_id = data.get("unit_id")
        statutory_mapping = data.get("statutory_mapping")
        compliance_id = data.get("compliance_id")
        frequency_id = data.get("frequency_id")
        user_type = data.get("user_type")
        due_from_date = data.get("due_from_date")
        due_to_date = data.get("due_to_date")
        task_status = data.get("task_status")
        csv = data.get("csv")
        from_count = data.get("from_count")
        page_count = data.get("page_count")
        return GetUserWiseReport(
            country_id, legal_entity_id, user_id, domain_id, unit_id,
            statutory_mapping, compliance_id, frequency_id, user_type,
            due_from_date, due_to_date, task_status, csv, from_count, page_count
        )

    def to_inner_structure(self):
        return {
            "country_id": self.country_id,
            "legal_entity_id": self.legal_entity_id,
            "user_id": self.user_id,
            "domain_id": self.domain_id,
            "unit_id": self.unit_id,
            "statutory_mapping": self.statutory_mapping,
            "compliance_id": self.compliance_id,
            "frequency_id": self.frequency_id,
            "user_type": self.user_type,
            "due_from_date": self.due_from_date,
            "due_to_date": self.due_to_date,
            "task_status": self.task_status,
            "csv": self.csv,
            "from_count": self.from_count,
            "page_count": self.page_count
        }

class GetUnitListReportFilters(Request):
    def __init__(self, country_id, business_group_id, legal_entity_id):
        self.country_id = country_id
        self.business_group_id = business_group_id
        self.legal_entity_id = legal_entity_id

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["country_id", "business_group_id", "legal_entity_id"])
        country_id = data.get("country_id")
        business_group_id = data.get("business_group_id")
        legal_entity_id = data.get("legal_entity_id")
        return GetUnitListReportFilters(country_id, business_group_id, legal_entity_id)

    def to_inner_structure(self):
        return {
            "country_id": self.country_id,
            "business_group_id": self.business_group_id,
            "legal_entity_id": self.legal_entity_id,
        }

class GetUnitListReport(Request):
    def __init__(
        self, country_id, business_group_id, legal_entity_id, division_id,
        category_id, unit_id, domain_id, organisation_id, unit_status,
        csv, from_count, page_count
    ):
        self.country_id = country_id
        self.business_group_id = business_group_id
        self.legal_entity_id = legal_entity_id
        self.division_id = division_id
        self.category_id = category_id
        self.unit_id = unit_id
        self.domain_id = domain_id
        self.organisation_id = organisation_id
        self.unit_status = unit_status
        self.csv = csv
        self.from_count = from_count
        self.page_count = page_count

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "country_id", "business_group_id", "legal_entity_id", "division_id",
            "category_id", "unit_id", "domain_id", "organisation_id", "unit_status",
            "csv", "from_count", "page_count"
        ])
        country_id = data.get("country_id")
        business_group_id = data.get("business_group_id")
        legal_entity_id = data.get("legal_entity_id")
        division_id = data.get("division_id")
        category_id = data.get("category_id")
        unit_id = data.get("unit_id")
        domain_id = data.get("domain_id")
        organisation_id = data.get("organisation_id")
        unit_status = data.get("unit_status")
        csv = data.get("csv")
        from_count = data.get("from_count")
        page_count = data.get("page_count")
        return GetUnitListReport(
            country_id, business_group_id, legal_entity_id, division_id, category_id,
            unit_id, domain_id, organisation_id, unit_status, csv, from_count, page_count
        )

    def to_inner_structure(self):
        return {
            "country_id": self.country_id,
            "business_group_id": self.business_group_id,
            "legal_entity_id": self.legal_entity_id,
            "division_id": self.division_id,
            "category_id": self.category_id,
            "unit_id": self.unit_id,
            "domain_id": self.domain_id,
            "organisation_id": self.organisation_id,
            "unit_status": self.unit_status,
            "csv": self.csv,
            "from_count": self.from_count,
            "page_count": self.page_count
        }

class GetStatutoryNotificationsListReportFilters(Request):
    def __init__(self, country_id, legal_entity_id):
        self.country_id = country_id
        self.legal_entity_id = legal_entity_id

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["country_id", "legal_entity_id"])
        country_id = data.get("country_id")
        legal_entity_id = data.get("legal_entity_id")
        return GetStatutoryNotificationsListReportFilters(country_id, legal_entity_id)

    def to_inner_structure(self):
        return {
            "country_id": self.country_id,
            "legal_entity_id": self.legal_entity_id,
        }

class GetStatutoryNotificationsListReportData(Request):
    def __init__(
        self, country_id, legal_entity_id, domain_id, statutory_mapping,
        due_from_date, due_to_date, csv, from_count, page_count
    ):
        self.country_id = country_id
        self.legal_entity_id = legal_entity_id
        self.domain_id = domain_id
        self.statutory_mapping = statutory_mapping
        self.due_from_date = due_from_date
        self.due_to_date = due_to_date
        self.csv = csv
        self.from_count = from_count
        self.page_count = page_count

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "country_id", "legal_entity_id", "domain_id", "statutory_mapping",
            "due_from_date", "due_to_date", "csv", "from_count", "page_count"
        ])
        country_id = data.get("country_id")
        legal_entity_id = data.get("legal_entity_id")
        domain_id = data.get("domain_id")
        statutory_mapping = data.get("statutory_mapping")
        due_from_date = data.get("due_from_date")
        due_to_date = data.get("due_to_date")
        csv = data.get("csv")
        from_count = data.get("from_count")
        page_count = data.get("page_count")
        return GetStatutoryNotificationsListReportData(
            country_id, legal_entity_id, domain_id, statutory_mapping,
            due_from_date, due_to_date, csv, from_count, page_count
        )

    def to_inner_structure(self):
        return {
            "country_id": self.country_id,
            "legal_entity_id": self.legal_entity_id,
            "domain_id": self.domain_id,
            "statutory_mapping": self.statutory_mapping,
            "due_from_date": self.due_from_date,
            "due_to_date": self.due_to_date,
            "csv": self.csv,
            "from_count": self.from_count,
            "page_count": self.page_count
        }

class GetAuditTrailReportData(Request):
    def __init__(
        self, legal_entity_id, user_id, form_id_optional, due_from_date, due_to_date,
        csv, from_count, page_count
    ):
        self.legal_entity_id = legal_entity_id
        self.user_id = user_id
        self.form_id_optional = form_id_optional
        self.due_from_date = due_from_date
        self.due_to_date = due_to_date
        self.csv = csv
        self.from_count = from_count
        self.page_count = page_count

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "legal_entity_id", "user_id", "form_id_optional", "due_from_date", "due_to_date",
            "csv", "from_count", "page_count"
        ])
        legal_entity_id = data.get("legal_entity_id")
        user_id = data.get("user_id")
        form_id_optional = data.get("form_id_optional")
        due_from_date = data.get("due_from_date")
        due_to_date = data.get("due_to_date")
        csv = data.get("csv")
        from_count = data.get("from_count")
        page_count = data.get("page_count")
        return GetAuditTrailReportData(
            legal_entity_id, user_id, form_id_optional, due_from_date, due_to_date,
            csv, from_count, page_count
        )

    def to_inner_structure(self):
        return {
            "legal_entity_id": self.legal_entity_id,
            "user_id": self.user_id,
            "form_id_optional": self.form_id_optional,
            "due_from_date": self.due_from_date,
            "due_to_date": self.due_to_date,
            "csv": self.csv,
            "from_count": self.from_count,
            "page_count": self.page_count
        }

class GetRiskReportFilters(Request):
    def __init__(self, country_id, business_group_id, legal_entity_id):
        self.country_id = country_id
        self.business_group_id = business_group_id
        self.legal_entity_id = legal_entity_id

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["country_id", "business_group_id", "legal_entity_id"])
        country_id = data.get("country_id")
        business_group_id = data.get("business_group_id")
        legal_entity_id = data.get("legal_entity_id")
        return GetRiskReportFilters(country_id, business_group_id, legal_entity_id)

    def to_inner_structure(self):
        return {
            "country_id": self.country_id,
            "business_group_id": self.business_group_id,
            "legal_entity_id": self.legal_entity_id,
        }

class GetRiskReportData(Request):
    def __init__(
        self, country_id, business_group_id, legal_entity_id, domain_id, division_id,
        category_id, unit_id, statutory_mapping, compliance_id, task_status,
        csv, from_count, page_count
    ):
        self.country_id = country_id
        self.business_group_id = business_group_id
        self.legal_entity_id = legal_entity_id
        self.domain_id = domain_id
        self.division_id = division_id
        self.category_id = category_id
        self.unit_id = unit_id
        self.statutory_mapping = statutory_mapping
        self.compliance_id = compliance_id
        self.task_status = task_status
        self.csv = csv
        self.from_count = from_count
        self.page_count = page_count

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "country_id", "business_group_id", "legal_entity_id", "domain_id", "division_id",
            "category_id", "unit_id", "statutory_mapping", "compliance_id", "task_status",
            "csv", "from_count", "page_count"
        ])
        country_id = data.get("country_id")
        business_group_id = data.get("business_group_id")
        legal_entity_id = data.get("legal_entity_id")
        domain_id = data.get("domain_id")
        division_id = data.get("division_id")
        category_id = data.get("category_id")
        unit_id = data.get("unit_id")
        statutory_mapping = data.get("statutory_mapping")
        compliance_id = data.get("compliance_id")
        task_status = data.get("task_status")
        csv = data.get("csv")
        from_count = data.get("from_count")
        page_count = data.get("page_count")
        return GetRiskReportData(
            country_id, business_group_id, legal_entity_id, domain_id, division_id, category_id,
            unit_id, statutory_mapping, compliance_id, task_status, csv, from_count, page_count
        )

    def to_inner_structure(self):
        return {
            "country_id": self.country_id,
            "business_group_id": self.business_group_id,
            "legal_entity_id": self.legal_entity_id,
            "domain_id": self.domain_id,
            "division_id": self.division_id,
            "category_id": self.category_id,
            "unit_id": self.unit_id,
            "statutory_mapping": self.statutory_mapping,
            "compliance_id": self.compliance_id,
            "task_status": self.task_status,
            "csv": self.csv,
            "from_count": self.from_count,
            "page_count": self.page_count
        }

def _init_Request_class_map():
    classes = [
        GetComplianceDetailsReportFilters, GetComplianceDetailsReport,
        GetRiskReportFilters, GetRiskReportData, GetServiceProviderReportFilters,
        GetServiceProviderWiseCompliance, GetClientReportFilters,
        GetAssigneewisecomplianceReport, GetUnitwisecomplianceReport,
        GetReassignComplianceTaskReportFilters, GetReassignComplianceTaskDetails,
        GetTaskApplicabilityStatusFilters, GetComplianceTaskApplicabilityStatusReport,
        GetComplianceActivityReportFilters, GetComplianceActivityReport,
        GetReassignedHistoryReportFilters, GetReassignedHistoryReport,
        GetStatusReportConsolidatedFilters, GetStatusReportConsolidated,
        GetStatutorySettingsUnitWiseFilters, GetStatutorySettingsUnitWise,
        GetDomainScoreCardFilters, GetDomainScoreCard,
        GetLEWiseScoreCardFilters, GetLEWiseScoreCard,
        GetWorkFlowScoreCardFilters, GetWorkFlowScoreCard,
        GetStatutoryNotificationsListFilters, GetStatutoryNotificationsListReport,
        GetClientDetailsReportFilters, GetClientDetailsReportData, GetActivityLogFilters,
        GetActivityLogReport, GetLoginTrace, GetLegalEntityWiseReportFilters,
        GetLegalEntityWiseReport, GetDomainWiseReportFilters, GetDomainWiseReport,
        GetUnitWiseReportFilters, GetUnitWiseReport, GetServiceProviderWiseReportFilters,
        GetServiceProviderWiseReport, GetUserWiseReportFilters, GetUserWiseReport,
        GetUnitListReportFilters, GetUnitListReport, GetStatutoryNotificationsListReportFilters,
        GetStatutoryNotificationsListReportData, GetAuditTrailReportData
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

class GetComplianceDetailsReportFiltersSuccess(Response):
    def __init__(self, countries, domains, level_1_statutories, units, Compliances, users):
        self.countries = countries
        self.domains = domains
        self.level_1_statutories = level_1_statutories
        self.units = units
        self.Compliances = Compliances
        self.users = users

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["countries", "domains", "level_1_statutories", "units", "compliances", "users"])
        countries = data.get("countries")
        countries = parse_structure_VectorType_RecordType_core_Country(countries)
        domains = data.get("domains")
        domains = parse_structure_VectorType_RecordType_core_Domain(domains)
        level_1_statutories = data.get("level_1_statutories")
        level_1_statutories = parse_structure_VectorType_CustomTextType_100(level_1_statutories)
        units = data.get("units")
        units = parse_structure_VectorType_RecordType_core_ClientUnit(units)
        Compliances = data.get("compliances")
        Compliances = parse_structure_VectorType_RecordType_core_ComplianceFilter(Compliances)
        users = data.get("users")
        users = parse_structure_VectorType_RecordType_clientreport_User(users)
        return GetComplianceDetailsReportFiltersSuccess(countries, domains, level_1_statutories, units, Compliances, users)

    def to_inner_structure(self):
        return {
            "countries": to_structure_VectorType_RecordType_core_Country(self.countries),
            "domains": to_structure_VectorType_RecordType_core_Domain(self.domains),
            "level_1_statutories": to_structure_VectorType_CustomTextType_100(self.level_1_statutories),
            "units": to_structure_VectorType_RecordType_core_ClientUnit(self.units),
            "compliances": to_structure_VectorType_RecordType_core_ComplianceFilter(self.Compliances),
            "users": to_structure_VectorType_RecordType_clientreport_User(self.users),
        }

class GetLegalEntityWiseReportFiltersSuccess(Response):
    def __init__(
        self, domains, unit_legal_entity, act_legal_entity, compliance_task_list,
        compliance_frequency_list, compliance_user_type, compliance_task_status,
        compliance_users
    ):
        self.domains = domains
        self.unit_legal_entity = unit_legal_entity
        self.act_legal_entity = act_legal_entity
        self.compliance_task_list = compliance_task_list
        self.compliance_frequency_list = compliance_frequency_list
        self.compliance_user_type = compliance_user_type
        self.compliance_task_status = compliance_task_status
        self.compliance_users = compliance_users

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "domains", "unit_legal_entity", "act_legal_entity", "compliance_task_list",
            "compliance_frequency_list", "compliance_user_type", "compliance_task_status",
            "compliance_users"
        ])
        domains = data.get("domains")
        unit_legal_entity = data.get("unit_legal_entity")
        act_legal_entity = data.get("act_legal_entity")
        compliance_task_list = data.get("compliance_task_list")
        compliance_frequency_list = data.get("compliance_frequency_list")
        compliance_user_type = data.get("compliance_user_type")
        compliance_task_status = data.get("compliance_task_status")
        compliance_users = data.get("compliance_users")
        return GetLegalEntityWiseReportFiltersSuccess(
            domains, unit_legal_entity, act_legal_entity, compliance_task_list,
            compliance_frequency_list, compliance_user_type, compliance_task_status,
            compliance_users
        )

    def to_inner_structure(self):
        data = {
            "domains": self.domains,
            "unit_legal_entity": self.unit_legal_entity,
            "act_legal_entity": self.act_legal_entity,
            "compliance_task_list": self.compliance_task_list,
            "compliance_frequency_list": self.compliance_frequency_list,
            "compliance_user_type": self.compliance_user_type,
            "compliance_task_status": self.compliance_task_status,
            "compliance_users": self.compliance_users
        }
        return data

class GetLegalEntityWiseReportSuccess(Response):
    def __init__(
        self, legal_entities_compliances, total_count
    ):
        self.legal_entities_compliances = legal_entities_compliances
        self.total_count = total_count

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["legal_entities_compliances", "total_count"])
        legal_entities_compliances = data.get("legal_entities_compliances")
        total_count = data.get("total_count")
        return GetLegalEntityWiseReportSuccess(
            legal_entities_compliances, total_count
        )

    def to_inner_structure(self):
        data = {
            "legal_entities_compliances": self.legal_entities_compliances,
            "total_count": self.total_count
        }
        return data

class GetDomainWiseReportFiltersSuccess(Response):
    def __init__(
        self, domains, unit_legal_entity, act_legal_entity, compliance_task_list,
        compliance_frequency_list, compliance_user_type, compliance_task_status,
        compliance_users
    ):
        self.domains = domains
        self.unit_legal_entity = unit_legal_entity
        self.act_legal_entity = act_legal_entity
        self.compliance_task_list = compliance_task_list
        self.compliance_frequency_list = compliance_frequency_list
        self.compliance_user_type = compliance_user_type
        self.compliance_task_status = compliance_task_status
        self.compliance_users = compliance_users

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "domains", "unit_legal_entity", "act_legal_entity", "compliance_task_list",
            "compliance_frequency_list", "compliance_user_type", "compliance_task_status",
            "compliance_users"
        ])
        domains = data.get("domains")
        unit_legal_entity = data.get("unit_legal_entity")
        act_legal_entity = data.get("act_legal_entity")
        compliance_task_list = data.get("compliance_task_list")
        compliance_frequency_list = data.get("compliance_frequency_list")
        compliance_user_type = data.get("compliance_user_type")
        compliance_task_status = data.get("compliance_task_status")
        compliance_users = data.get("compliance_users")
        return GetDomainWiseReportFiltersSuccess(
            domains, unit_legal_entity, act_legal_entity, compliance_task_list,
            compliance_frequency_list, compliance_user_type, compliance_task_status,
            compliance_users
        )

    def to_inner_structure(self):
        data = {
            "domains": self.domains,
            "unit_legal_entity": self.unit_legal_entity,
            "act_legal_entity": self.act_legal_entity,
            "compliance_task_list": self.compliance_task_list,
            "compliance_frequency_list": self.compliance_frequency_list,
            "compliance_user_type": self.compliance_user_type,
            "compliance_task_status": self.compliance_task_status,
            "compliance_users": self.compliance_users
        }
        return data

class GetDomainWiseReportSuccess(Response):
    def __init__(
        self, legal_entities_compliances, total_count
    ):
        self.legal_entities_compliances = legal_entities_compliances
        self.total_count = total_count

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["legal_entities_compliances", "total_count"])
        legal_entities_compliances = data.get("legal_entities_compliances")
        total_count = data.get("total_count")
        return GetDomainWiseReportSuccess(
            legal_entities_compliances, total_count
        )

    def to_inner_structure(self):
        data = {
            "legal_entities_compliances": self.legal_entities_compliances,
            "total_count": self.total_count
        }
        return data

class GetUnitWiseReportSuccess(Response):
    def __init__(
        self, unit_compliances, total_count
    ):
        self.unit_compliances = unit_compliances
        self.total_count = total_count

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["unit_compliances", "total_count"])
        unit_compliances = data.get("unit_compliances")
        total_count = data.get("total_count")
        return GetUnitWiseReportSuccess(
            unit_compliances, total_count
        )

    def to_inner_structure(self):
        data = {
            "unit_compliances": self.unit_compliances,
            "total_count": self.total_count
        }
        return data

class ComplianceDetailsUnitWise(object):
    def __init__(self, unit_id, unit_name, address, Compliances):
        self.unit_id = unit_id
        self.unit_name = unit_name
        self.address = address
        self.Compliances = Compliances

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["unit_id", "unit_name", "address", "compliances"])
        unit_id = data.get("unit_id")
        unit_id = parse_structure_UnsignedIntegerType_32(unit_id)
        unit_name = data.get("unit_name")
        unit_name = parse_structure_CustomTextType_100(unit_name)
        address = data.get("address")
        address = parse_structure_CustomTextType_250(address)
        Compliances = data.get("compliances")
        Compliances = parse_structure_VectorType_RecordType_clientreport_ComplianceDetails(Compliances)
        return ComplianceDetailsUnitWise(unit_id, unit_name, address, Compliances)

    def to_inner_structure(self):
        result = {
            "unit_id": to_structure_SignedIntegerType_8(self.unit_id),
            "unit_name": to_structure_CustomTextType_100(self.unit_name),
            "address": to_structure_CustomTextType_250(self.address),
            "compliances": to_structure_VectorType_RecordType_clientreport_ComplianceDetails(self.Compliances),
        }

        return result

class GetUnitWiseReportFiltersSuccess(Response):
    def __init__(
        self, domains, unit_legal_entity, act_legal_entity, compliance_task_list,
        compliance_frequency_list, compliance_user_type, compliance_task_status,
        compliance_users
    ):
        self.domains = domains
        self.unit_legal_entity = unit_legal_entity
        self.act_legal_entity = act_legal_entity
        self.compliance_task_list = compliance_task_list
        self.compliance_frequency_list = compliance_frequency_list
        self.compliance_user_type = compliance_user_type
        self.compliance_task_status = compliance_task_status
        self.compliance_users = compliance_users

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "domains", "unit_legal_entity", "act_legal_entity", "compliance_task_list",
            "compliance_frequency_list", "compliance_user_type", "compliance_task_status",
            "compliance_users"
        ])
        domains = data.get("domains")
        unit_legal_entity = data.get("unit_legal_entity")
        act_legal_entity = data.get("act_legal_entity")
        compliance_task_list = data.get("compliance_task_list")
        compliance_frequency_list = data.get("compliance_frequency_list")
        compliance_user_type = data.get("compliance_user_type")
        compliance_task_status = data.get("compliance_task_status")
        compliance_users = data.get("compliance_users")
        return GetUnitWiseReportFiltersSuccess(
            domains, unit_legal_entity, act_legal_entity, compliance_task_list,
            compliance_frequency_list, compliance_user_type, compliance_task_status,
            compliance_users
        )

    def to_inner_structure(self):
        data = {
            "domains": self.domains,
            "unit_legal_entity": self.unit_legal_entity,
            "act_legal_entity": self.act_legal_entity,
            "compliance_task_list": self.compliance_task_list,
            "compliance_frequency_list": self.compliance_frequency_list,
            "compliance_user_type": self.compliance_user_type,
            "compliance_task_status": self.compliance_task_status,
            "compliance_users": self.compliance_users
        }
        return data

class GetComplianceDetailsReportSuccess(Response):
    def __init__(self, unit_wise_compliancess, total_count):
        self.unit_wise_compliancess = unit_wise_compliancess
        self.total_count = total_count

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["unit_wise_compliancess", "total_count"])
        unit_wise_compliances = data.get("unit_wise_compliances")
        unit_wise_compliances = parse_structure_VectorType_RecordType_clientreport_ComplianceDetailsUnitWise(unit_wise_compliances)
        total_count = data.get("total_count")
        total_count = parse_structure_UnsignedIntegerType_32(total_count)
        return GetComplianceDetailsReportSuccess(unit_wise_compliances, total_count)

    def to_inner_structure(self):
        return {
            "unit_wise_compliancess": to_structure_VectorType_RecordType_clientreport_ComplianceDetailsUnitWise(self.unit_wise_compliancess),
            "total_count": to_structure_UnsignedIntegerType_32(self.total_count)
        }


class GetServiceProviderReportFiltersSuccess(Response):
    def __init__(self, countries, domains, level_1_statutories, units, service_providers):
        self.countries = countries
        self.domains = domains
        self.level_1_statutories = level_1_statutories
        self.units = units
        self.service_providers = service_providers

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["countries", "domains", "level_1_statutories", "units", "service_providers"])
        countries = data.get("countries")
        countries = parse_structure_VectorType_RecordType_core_Country(countries)
        domains = data.get("domains")
        domains = parse_structure_VectorType_RecordType_core_Domain(domains)
        level_1_statutories = data.get("level_1_statutories")
        level_1_statutories = parse_structure_VectorType_CustomTextType_100(level_1_statutories)
        units = data.get("units")
        units = parse_structure_VectorType_RecordType_core_ClientUnit(units)
        service_providers = data.get("service_providers")
        service_providers = parse_structure_VectorType_RecordType_core_ServiceProvider(service_providers)
        return GetServiceProviderReportFiltersSuccess(countries, domains, level_1_statutories, units, service_providers)

    def to_inner_structure(self):
        return {
            "countries": to_structure_VectorType_RecordType_core_Country(self.countries),
            "domains": to_structure_VectorType_RecordType_core_Domain(self.domains),
            "level_1_statutories": to_structure_VectorType_CustomTextType_100(self.level_1_statutories),
            "units": to_structure_VectorType_RecordType_core_ClientUnit(self.units),
            "service_providers": to_structure_VectorType_RecordType_core_ServiceProvider(self.service_providers),
        }

class GetServiceProviderWiseComplianceSuccess(Response):
    def __init__(self, compliance_list, total_count):
        self.compliance_list = compliance_list
        self.total_count = total_count

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["compliance_list", "total_count"])
        compliance_list = data.get("compliance_list")
        compliance_list = parse_structure_VectorType_RecordType_clientreport_ServiceProviderCompliance(compliance_list)
        total_count = data.get("total_count")
        total_count = parse_structure_UnsignedIntegerType_32(total_count)
        return GetServiceProviderWiseComplianceSuccess(compliance_list, total_count)

    def to_inner_structure(self):
        return {
            "compliance_list": to_structure_VectorType_RecordType_clientreport_ServiceProviderCompliance(self.compliance_list),
            "total_count": to_structure_UnsignedIntegerType_32(self.total_count)
        }

class GetClientReportFiltersSuccess(Response):
    def __init__(self, countries, domains, business_groups, legal_entities, divisions, units, users):
        self.countries = countries
        self.domains = domains
        self.business_groups = business_groups
        self.legal_entities = legal_entities
        self.divisions = divisions
        self.units = units
        self.users = users

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["countries", "domains", "business_groups", "legal_entities", "divisions", "units", "users"])
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
        units = parse_structure_VectorType_RecordType_core_ClientUnit(units)
        users = data.get("users")
        users = parse_structure_VectorType_RecordType_clientreport_User(users)
        return GetClientReportFiltersSuccess(countries, domains, business_groups, legal_entities, divisions, units, users)

    def to_inner_structure(self):
        return {
            "countries": to_structure_VectorType_RecordType_core_Country(self.countries),
            "domains": to_structure_VectorType_RecordType_core_Domain(self.domains),
            "business_groups": to_structure_VectorType_RecordType_core_ClientBusinessGroup(self.business_groups),
            "legal_entities": to_structure_VectorType_RecordType_core_ClientLegalEntity(self.legal_entities),
            "divisions": to_structure_VectorType_RecordType_core_ClientDivision(self.divisions),
            "units": to_structure_VectorType_RecordType_core_ClientUnit(self.units),
            "users": to_structure_VectorType_RecordType_clientreport_User(self.users),
        }

class GetAssigneewisecomplianceReportSuccess(Response):
    def __init__(self, compliance_list, total_count):
        self.compliance_list = compliance_list
        self.total_count = total_count

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["compliance_list", "total_count"])
        compliance_list = data.get("compliance_list")
        compliance_list = parse_structure_VectorType_RecordType_clientreport_AssigneeCompliance(compliance_list)
        total_count = data.get("total_count")
        total_count = parse_structure_UnsignedIntegerType_32(total_count)
        return GetAssigneewisecomplianceReportSuccess(compliance_list, total_count)

    def to_inner_structure(self):
        return {
            "compliance_list": to_structure_VectorType_RecordType_clientreport_AssigneeCompliance(self.compliance_list),
            "total_count": to_structure_UnsignedIntegerType_32(self.total_count)
        }

class GetUnitwisecomplianceReportSuccess(Response):
    def __init__(self, compliance_list, total_count):
        self.compliance_list = compliance_list
        self.total_count = total_count

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["compliance_list", "total_count"])
        compliance_list = data.get("compliance_list")
        compliance_list = parse_structure_VectorType_RecordType_clientreport_UnitCompliance(compliance_list)
        total_count = data.get("total_count")
        total_count = parse_structure_UnsignedIntegerType_32(total_count)
        return GetUnitwisecomplianceReportSuccess(compliance_list)

    def to_inner_structure(self):
        return {
            "compliance_list": to_structure_VectorType_RecordType_clientreport_UnitCompliance(self.compliance_list),
            "total_count": to_structure_UnsignedIntegerType_32(self.total_count)
        }

class GetReassignComplianceTaskReportFiltersSuccess(Response):
    def __init__(self, countries, doamins, level_1_statutories, units, compliances, users):
        self.countries = countries
        self.doamins = doamins
        self.level_1_statutories = level_1_statutories
        self.units = units
        self.compliances = compliances
        self.users = users

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["countries", "doamins", "level_1_statutories", "units", "compliances", "users"])
        countries = data.get("countries")
        countries = parse_structure_VectorType_RecordType_core_Country(countries)
        doamins = data.get("doamins")
        doamins = parse_structure_VectorType_RecordType_core_Domain(doamins)
        level_1_statutories = data.get("level_1_statutories")
        level_1_statutories = parse_structure_MapType_SignedIntegerType_8_MapType_SignedIntegerType_8_VectorType_RecordType_core_Statutory(level_1_statutories)
        units = data.get("units")
        units = parse_structure_VectorType_RecordType_clientreport_UnitName(units)
        compliances = data.get("compliances")
        compliances = parse_structure_VectorType_RecordType_clientreport_ComplianceName(compliances)
        users = data.get("users")
        users = parse_structure_VectorType_RecordType_clientreport_UserName(users)
        return GetReassignComplianceTaskReportFiltersSuccess(countries, doamins, level_1_statutories, units, compliances, users)

    def to_inner_structure(self):
        return {
            "countries": to_structure_VectorType_RecordType_core_Country(self.countries),
            "doamins": to_structure_VectorType_RecordType_core_Domain(self.doamins),
            "level_1_statutories": to_structure_MapType_SignedIntegerType_8_MapType_SignedIntegerType_8_VectorType_RecordType_core_Statutory(self.level_1_statutories),
            "units": to_structure_VectorType_RecordType_clientreport_UnitName(self.units),
            "compliances": to_structure_VectorType_RecordType_clientreport_ComplianceName(self.compliances),
            "users": to_structure_VectorType_RecordType_clientreport_UserName(self.users),
        }

class GetReassignComplianceTaskDetailsSuccess(Response):
    def __init__(self, compliance_list):
        self.compliance_list = compliance_list

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["compliance_list"])
        compliance_list = data.get("compliance_list")
        compliance_list = parse_structure_VectorType_RecordType_clientreport_ReassignCompliance(compliance_list)
        return GetReassignComplianceTaskDetailsSuccess(compliance_list)

    def to_inner_structure(self):
        return {
            "compliance_list": to_structure_VectorType_RecordType_clientreport_ReassignCompliance(self.compliance_list),
        }

class GetTaskApplicabilityStatusFiltersSuccess(Response):
    def __init__(
        self, countries, domains, business_groups, legal_entities,
        divisions, units, level_1_statutories, applicable_status
    ):
        self.countries = countries
        self.domains = domains
        self.business_groups = business_groups
        self.legal_entities = legal_entities
        self.divisions = divisions
        self.units = units
        self.level_1_statutories = level_1_statutories
        self.applicable_status = applicable_status

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["countries", "domains", "business_groups", "legal_entities", "divisions", "units", "level_1_statutories"])
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
        units = parse_structure_VectorType_RecordType_core_ClientUnit(units)
        level_1_statutories = data.get("level_1_statutories")
        level_1_statutories = parse_structure_VectorType_CustomTextType_100(level_1_statutories)
        applicable_status = data.get("applicable_status")
        applicable_status = parse_structure_VectorType_CustomTextType_100(applicable_status)
        return GetTaskApplicabilityStatusFiltersSuccess(countries, domains, business_groups, legal_entities, divisions, units, level_1_statutories, applicable_status)

    def to_inner_structure(self):
        return {
            "countries": to_structure_VectorType_RecordType_core_Country(self.countries),
            "domains": to_structure_VectorType_RecordType_core_Domain(self.domains),
            "business_groups": to_structure_VectorType_RecordType_core_ClientBusinessGroup(self.business_groups),
            "legal_entities": to_structure_VectorType_RecordType_core_ClientLegalEntity(self.legal_entities),
            "divisions": to_structure_VectorType_RecordType_core_ClientDivision(self.divisions),
            "units": to_structure_VectorType_RecordType_core_ClientUnit(self.units),
            "level_1_statutories": to_structure_VectorType_CustomTextType_100(self.level_1_statutories),
            "applicable_status": to_structure_VectorType_CustomTextType_100(self.applicable_status),
        }

class GetComplianceTaskApplicabilityStatusReportData(object):
    def __init__(
        self, business_group_name, legal_entity_name, division_name, actwise_units
    ):
        self.business_group_name = business_group_name
        self.legal_entity_name = legal_entity_name
        self.division_name = division_name
        self.actwise_units = actwise_units

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(
            data, [
                "business_group_name", "legal_entity_name", "division_name",
                "actwise_units"
            ]
        )
        business_group_name = data.get("business_group_name")
        business_group_name = parse_structure_OptionalType_CustomTextType_50(business_group_name)
        legal_entity_name = data.get("legal_entity_name")
        legal_entity_name = parse_structure_CustomTextType_50(legal_entity_name)
        division_name = data.get("division_name")
        division_name = parse_structure_OptionalType_CustomTextType_50(division_name)
        division_name = data.get("division_name")
        division_name = parse_structure_OptionalType_CustomTextType_50(division_name)
        actwise_units = data.get("actwise_units")
        actwise_units = parse_structure_MapType_CustomTextType_500_VectorType_RecordType_clientreport_ApplicabilityCompliance(actwise_units)
        return GetComplianceTaskApplicabilityStatusReportData(
            business_group_name, legal_entity_name, division_name, actwise_units
        )

    def to_structure(self):
        return {
            "business_group_name": to_structure_OptionalType_CustomTextType_50(self.business_group_name),
            "legal_entity_name": to_structure_CustomTextType_50(self.legal_entity_name),
            "division_name": to_structure_OptionalType_CustomTextType_50(self.division_name),
            "actwise_units": to_structure_MapType_CustomTextType_500_VectorType_RecordType_clientreport_ApplicabilityCompliance(self.actwise_units),
        }

class GetComplianceTaskApplicabilityStatusReportSuccess(Response):
    def __init__(self, total_record, applicable_status):
        self.total_record = total_record
        self.applicable_status = applicable_status

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["total_record", "applicable_status"])
        total_record = data.get("total_record")
        total_record = parse_structure_UnsignedIntegerType_32(total_record)
        applicable_status = data.get("applicable_status")
        applicable_status = parse_structure_VectorType_RecordType_clientreport_GetComplianceTaskApplicabilityStatusReportData(applicable_status)
        return GetComplianceTaskApplicabilityStatusReportSuccess(total_record, applicable_status)

    def to_inner_structure(self):
        return {
            "total_record": to_structure_UnsignedIntegerType_32(self.total_record),
            "applicable_status": to_structure_VectorType_RecordType_clientreport_GetComplianceTaskApplicabilityStatusReportData(self.applicable_status),
        }

class GetComplianceActivityReportFiltersSuccess(Response):
    def __init__(self, users, countries, domains, level_1_statutories, units, compliances):
        self.users = users
        self.domains = domains
        self.level_1_statutories = level_1_statutories
        self.units = units
        self.compliances = compliances
        self.countries = countries

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["users", "countries", "domains", "level_1_statutories", "units", "compliances"])
        users = data.get("users")
        countries = data.get("countries")
        domains = data.get("domains")
        level_1_statutories = data.get("level_1_statutories")
        units = data.get("units")
        compliances = data.get("compliances")
        return GetComplianceActivityReportFiltersSuccess(
            users, countries, domains, level_1_statutories,
            units, compliances
        )

    def to_inner_structure(self):
        return {
            "users": self.users,
            "countries": self.countries,
            "domains": self.domains,
            "level_1_statutories": self.level_1_statutories,
            "units": self.units,
            "compliances": self.compliances
        }

class GetComplianceActivityReportSuccess(Response):
    def __init__(self, activities):
        self.activities = activities

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["activities"])
        activities = data.get("activities")
        activities = parse_structure_VectorType_RecordType_clientreport_Activities(activities)
        return GetComplianceActivityReportSuccess(activities)

    def to_inner_structure(self):
        return {
            "activities": to_structure_VectorType_RecordType_clientreport_Activities(self.activities),
        }

# Reassigned History Report Start

class GetReassignedHistoryReportFiltersSuccess(Response):
    def __init__(self, domains, units, acts, compliances, legal_entity_users):
        self.domains = domains
        self.units = units
        self.acts = acts
        self.compliances = compliances
        self.legal_entity_users = legal_entity_users

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["domains", "units", "acts", "compliances", "legal_entity_users"])
        domains = data.get("domains")
        units = data.get("units")
        acts = data.get("acts")
        compliances = data.get("compliances")
        legal_entity_users = data.get("legal_entity_users")
        return GetReassignedHistoryReportFiltersSuccess(domains, units, acts, compliances, legal_entity_users)

    def to_inner_structure(self):
        return {
            "domains": self.domains,
            "units": self.units,
            "acts": self.acts,
            "compliances": self.compliances,
            "legal_entity_users": self.legal_entity_users,
        }

class GetReassignedHistoryReportSuccess(Response):
    def __init__(self, reassigned_history_list, total_count):
        self.reassigned_history_list = reassigned_history_list
        self.total_count = total_count

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["reassigned_history_list", "total_count"])
        reassigned_history_list = data.get("reassigned_history_list"),
        total_count = data.get("total_count")
        return GetReassignedHistoryReportSuccess(reassigned_history_list, total_count)

    def to_inner_structure(self):
        return {
            "reassigned_history_list": self.reassigned_history_list,
            "total_count": self.total_count
        }
# Reassigned History Report End

# Status Report Consolidated Report Start
class GetStatusReportConsolidatedFiltersSuccess(Response):
    def __init__(self, domains, units, acts, compliances, compliance_frequency, legal_entity_users):
        self.domains = domains
        self.units = units
        self.acts = acts
        self.compliances = compliances
        self.compliance_frequency = compliance_frequency
        self.legal_entity_users = legal_entity_users

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["domains", "units", "acts", "compliances", "compliance_frequency", "legal_entity_users"])
        domains = data.get("domains")
        units = data.get("units")
        acts = data.get("acts")
        compliances = data.get("compliances")
        compliance_frequency = data.get("compliance_frequency")
        legal_entity_users = data.get("legal_entity_users")
        return GetStatusReportConsolidatedFiltersSuccess(domains, units, acts, compliances, compliance_frequency, legal_entity_users)

    def to_inner_structure(self):
        return {
            "domains": self.domains,
            "units": self.units,
            "acts": self.acts,
            "compliances": self.compliances,
            "compliance_frequency": self.compliance_frequency,
            "legal_entity_users": self.legal_entity_users
        }

class GetStatusReportConsolidatedSuccess(Response):
    def __init__(self, status_report_consolidated_list, total_count):
        self.status_report_consolidated_list = status_report_consolidated_list
        self.total_count = total_count

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["status_report_consolidated_list", "total_count"])
        status_report_consolidated_list = data.get("status_report_consolidated_list"),
        total_count = data.get("total_count")
        return GetStatusReportConsolidatedSuccess(status_report_consolidated_list, total_count)

    def to_inner_structure(self):
        return {
            "status_report_consolidated_list": self.status_report_consolidated_list,
            "total_count": self.total_count
        }
# Status Report Consolidated Report End


# Statutory Settings Unit Wise Start
class GetStatutorySettingsUnitWiseFiltersSuccess(Response):
    def __init__(self, domains, units, acts, compliances, compliance_frequency, divisions, categories):
        self.domains = domains
        self.units = units
        self.acts = acts
        self.compliances = compliances
        self.compliance_frequency = compliance_frequency
        self.divisions = divisions
        self.categories = categories

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["domains", "units", "acts", "compliances", "compliance_frequency", "div_infos", "cat_infos"])
        domains = data.get("domains")
        units = data.get("units")
        acts = data.get("acts")
        compliances = data.get("compliances")
        compliance_frequency = data.get("compliance_frequency")
        divisions = data.get("div_infos")
        categories = data.get("cat_infos")
        return GetStatutorySettingsUnitWiseFiltersSuccess(domains, units, acts, compliances, compliance_frequency, divisions, categories)

    def to_inner_structure(self):
        return {
            "domains": self.domains,
            "units": self.units,
            "acts": self.acts,
            "compliances": self.compliances,
            "compliance_frequency": self.compliance_frequency,
            "div_infos": self.divisions,
            "cat_infos": self.categories
        }

class GetStatutorySettingsUnitWiseSuccess(Response):
    def __init__(self, statutory_settings_unit_Wise_list, total_count):
        self.statutory_settings_unit_Wise_list = statutory_settings_unit_Wise_list
        self.total_count = total_count

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["statutory_settings_unit_Wise_list", "total_count"])
        statutory_settings_unit_Wise_list = data.get("statutory_settings_unit_Wise_list"),
        total_count = data.get("total_count")
        return GetStatutorySettingsUnitWiseSuccess(statutory_settings_unit_Wise_list, total_count)

    def to_inner_structure(self):
        return {
            "statutory_settings_unit_Wise_list": self.statutory_settings_unit_Wise_list,
            "total_count": self.total_count
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
    def __init__(self, domain_score_card_list):
        self.domain_score_card_list = domain_score_card_list

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["domain_score_card_list"])
        domain_score_card_list = data.get("domain_score_card_list")
        return GetDomainScoreCardSuccess(domain_score_card_list)

    def to_inner_structure(self):
        return {
            "domain_score_card_list": self.domain_score_card_list
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
    def __init__(self, le_wise_score_card_list):
        self.le_wise_score_card_list = le_wise_score_card_list

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["le_wise_score_card_list"])
        le_wise_score_card_list = data.get("le_wise_score_card_list")
        return GetDomainScoreCardSuccess(le_wise_score_card_list)

    def to_inner_structure(self):
        return {
            "le_wise_score_card_list": self.le_wise_score_card_list
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
    def __init__(self, work_flow_score_card_list):
        self.work_flow_score_card_list = work_flow_score_card_list

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["work_flow_score_card_list"])
        work_flow_score_card_list = data.get("work_flow_score_card_list")
        return GetWorkFlowScoreCardSuccess(work_flow_score_card_list)

    def to_inner_structure(self):
        return {
            "work_flow_score_card_list": self.work_flow_score_card_list
        }
# Work Flow Score Card End

#
# Statutory Notificaiton List
#

class GetStatutoryNotificationsListFiltersSuccess(Response):
    def __init__(self, countries, domains, business_groups, legal_entities, divisions, units, level_1_statutories, users):
        self.countries = countries
        self.domains = domains
        self.business_groups = business_groups
        self.legal_entities = legal_entities
        self.divisions = divisions
        self.units = units
        self.level_1_statutories = level_1_statutories

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["countries", "domains", "business_groups", "legal_entities", "divisions", "units", "level_1_statutories"])
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
        units = parse_structure_VectorType_RecordType_core_ClientUnit(units)
        level_1_statutories = data.get("level_1_statutories")
        level_1_statutories = parse_structure_VectorType_CustomTextType_500(level_1_statutories)
        return GetStatutoryNotificationsListFiltersSuccess(countries, domains, business_groups, legal_entities, divisions, units, level_1_statutories)

    def to_inner_structure(self):
        return {
            "countries": to_structure_VectorType_RecordType_core_Country(self.countries),
            "domains": to_structure_VectorType_RecordType_core_Domain(self.domains),
            "business_groups": to_structure_VectorType_RecordType_core_ClientBusinessGroup(self.business_groups),
            "legal_entities": to_structure_VectorType_RecordType_core_ClientLegalEntity(self.legal_entities),
            "divisions": to_structure_VectorType_RecordType_core_ClientDivision(self.divisions),
            "units": to_structure_VectorType_RecordType_core_ClientUnit(self.units),
            "level_1_statutories": to_structure_VectorType_CustomTextType_500(self.level_1_statutories),
        }

class GetStatutoryNotificationsListReportSuccess(Response):
    def __init__(self, statutory_wise_notifications):
        self.statutory_wise_notifications = statutory_wise_notifications

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["statutory_wise_notifications"])
        statutory_wise_notifications = data.get("statutory_wise_notifications")
        statutory_wise_notifications = parse_structure_VectorType_RecordType_clientreport_STATUTORY_WISE_NOTIFICATIONS(statutory_wise_notifications)
        return GetStatutoryNotificationsListReportSuccess(statutory_wise_notifications)

    def to_inner_structure(self):
        return {
            "statutory_wise_notifications": to_structure_VectorType_RecordType_clientreport_STATUTORY_WISE_NOTIFICATIONS(self.statutory_wise_notifications),
        }

class GetActivityLogFiltersSuccess(Response):
    def __init__(self, users, forms):
        self.users = users
        self.forms = forms

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["users", "forms"])
        users = data.get("users")
        users = parse_structure_VectorType_RecordType_clientreport_UserName(users)
        forms = data.get("forms")
        forms = parse_structure_VectorType_RecordType_clientreport_FormName(forms)
        return GetActivityLogFiltersSuccess(users, forms)

    def to_inner_structure(self):
        return {
            "users": to_structure_VectorType_RecordType_clientreport_UserName(self.users),
            "forms": to_structure_VectorType_RecordType_clientreport_FormName(self.forms),
        }

class GetActivityLogReportSuccess(Response):
    def __init__(self, activity_log):
        self.activity_log = activity_log

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["activity_log"])
        activity_log = data.get("activity_log")
        activity_log = parse_structure_VectorType_RecordType_clientreport_ActivityLog(activity_log)
        return GetActivityLogReportSuccess(activity_log)

    def to_inner_structure(self):
        return {
            "activity_log": to_structure_VectorType_RecordType_clientreport_ActivityLog(self.activity_log),
        }

class GetLoginTraceSuccess(Response):
    def __init__(self, users, login_trace):
        self.users = users
        self.login_trace = login_trace

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["users", "login_trace"])
        users = data.get("users")
        users = parse_structure_VectorType_RecordType_clientreport_User(users)
        login_trace = data.get("login_trace")
        login_trace = parse_structure_VectorType_RecordType_clientreport_LoginTrace(login_trace)
        return GetLoginTraceSuccess(users, login_trace)

    def to_inner_structure(self):
        return {
            "users": to_structure_VectorType_RecordType_clientreport_User(self.users),
            "login_trace": to_structure_VectorType_RecordType_clientreport_LoginTrace(self.login_trace),
        }

class GetClientDetailsReportDataSuccess(Response):
    def __init__(self, units, total_count):
        self.units = units
        self.total_count = total_count

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["units", "total_count"])
        units = data.get("units")
        units = parse_structure_VectorType_RecordType_core_UnitDetails(units)
        total_count = data.get("total_count")
        total_count = parse_structure_UnsignedIntegerType_32(total_count)
        return GetClientDetailsReportDataSuccess(units, total_count)

    def to_inner_structure(self):
        return {
            "units": to_structure_VectorType_RecordType_client_report_GroupedUnits(self.units),
            "total_count": to_structure_UnsignedIntegerType_32(self.total_count)
        }

class GetClientDetailsReportFiltersSuccess(Response):
    def __init__(
        self, countries, domains, business_groups,
        legal_entities, divisions, units
    ):
        self.countries = countries
        self.domains = domains
        self.business_groups = business_groups
        self.legal_entities = legal_entities
        self.divisions = divisions
        self.units = units

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "countries", "domains",
            "business_groups", "legal_entities", "divisions", "units",
            ]
        )
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
        units = parse_structure_VectorType_RecordType_core_ClientUnit(units)
        return GetClientDetailsReportFiltersSuccess(
            countries, domains,
            business_groups, legal_entities, divisions, units
        )

    def to_inner_structure(self):
        return {
            "countries": to_structure_VectorType_RecordType_core_Country(self.countries),
            "domains": to_structure_VectorType_RecordType_core_Domain(self.domains),
            "business_groups": to_structure_VectorType_RecordType_core_ClientBusinessGroup(self.business_groups),
            "legal_entities": to_structure_VectorType_RecordType_core_ClientLegalEntity(self.legal_entities),
            "divisions": to_structure_VectorType_RecordType_core_ClientDivision(self.divisions),
            "units": to_structure_VectorType_RecordType_core_ClientUnit(self.units)
        }

class GetServiceProviderWiseReportFiltersSuccess(Response):
    def __init__(
        self, sp_domains_list, sp_unit_list, sp_act_task_list, sp_list,
        compliance_task_status, sp_users_list
    ):
        self.sp_domains_list = sp_domains_list
        self.sp_unit_list = sp_unit_list
        self.sp_act_task_list = sp_act_task_list
        self.sp_list = sp_list
        self.compliance_task_status = compliance_task_status
        self.sp_users_list = sp_users_list

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "sp_domains_list", "sp_unit_list", "sp_act_task_list", "sp_list",
            "compliance_task_status", "sp_users_list"
        ])
        sp_domains_list = data.get("sp_domains_list")
        sp_unit_list = data.get("sp_unit_list")
        sp_act_task_list = data.get("sp_act_task_list")
        sp_list = data.get("sp_list")
        compliance_task_status = data.get("compliance_task_status")
        sp_users_list = data.get("sp_users_list")
        return GetServiceProviderWiseReportFiltersSuccess(
            sp_domains_list, sp_unit_list, sp_act_task_list, sp_list,
            compliance_task_status, sp_users_list
        )

    def to_inner_structure(self):
        data = {
            "sp_domains_list": self.sp_domains_list,
            "sp_unit_list": self.sp_unit_list,
            "sp_act_task_list": self.sp_act_task_list,
            "sp_list": self.sp_list,
            "compliance_task_status": self.compliance_task_status,
            "sp_users_list": self.sp_users_list
        }
        return data

class GetServiceProviderWiseReportSuccess(Response):
    def __init__(self, sp_compliances, total_count):
        self.sp_compliances = sp_compliances
        self.total_count = total_count

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["sp_compliances", "total_count"])
        sp_compliances = data.get("sp_compliances")
        total_count = data.get("total_count")
        return GetServiceProviderWiseReportSuccess(sp_compliances, total_count)

    def to_inner_structure(self):
        return {
            "sp_compliances" : self.sp_compliances,
            "total_count": self.total_count
        }

class GetUserWiseReportFiltersSuccess(Response):
    def __init__(
        self, le_users_list, user_domains_list, users_units_list, user_act_task_list,
        compliance_frequency_list, compliance_user_type, compliance_task_status
    ):
        self.le_users_list = le_users_list
        self.user_domains_list = user_domains_list
        self.users_units_list = users_units_list
        self.user_act_task_list = user_act_task_list
        self.compliance_frequency_list = compliance_frequency_list
        self.compliance_user_type = compliance_user_type
        self.compliance_task_status = compliance_task_status

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "le_users_list", "user_domains_list", "users_units_list", "user_act_task_list",
            "compliance_frequency_list", "compliance_user_type", "compliance_task_status"
        ])
        le_users_list = data.get("le_users_list")
        user_domains_list = data.get("user_domains_list")
        users_units_list = data.get("users_units_list")
        user_act_task_list = data.get("user_act_task_list")
        compliance_frequency_list = data.get("compliance_frequency_list")
        compliance_user_type = data.get("compliance_user_type")
        compliance_task_status = data.get("compliance_task_status")
        return GetUserWiseReportFiltersSuccess(
            le_users_list, user_domains_list, users_units_list, user_act_task_list,
            compliance_frequency_list, compliance_user_type, compliance_task_status
        )

    def to_inner_structure(self):
        data = {
            "le_users_list": self.le_users_list,
            "user_domains_list": self.user_domains_list,
            "users_units_list": self.users_units_list,
            "user_act_task_list": self.user_act_task_list,
            "compliance_frequency_list": self.compliance_frequency_list,
            "compliance_user_type": self.compliance_user_type,
            "compliance_task_status": self.compliance_task_status
        }
        return data

class GetUserWiseReportSuccess(Response):
    def __init__(self, user_compliances, total_count):
        self.user_compliances = user_compliances
        self.total_count = total_count

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["user_compliances", "total_count"])
        user_compliances = data.get("user_compliances")
        total_count = data.get("total_count")
        return GetUserWiseReportSuccess(user_compliances, total_count)

    def to_inner_structure(self):
        return {
            "user_compliances" : self.user_compliances,
            "total_count": self.total_count
        }

class GetUnitListReportFiltersSuccess(Response):
    def __init__(
        self, divisions, categories, units_list, domains_organisations_list,
        unit_status_list
    ):
        self.divisions = divisions
        self.categories = categories
        self.units_list = units_list
        self.domains_organisations_list = domains_organisations_list
        self.unit_status_list = unit_status_list

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "divisions", "categories", "units_list", "domains_organisations_list",
            "unit_status_list"
        ])
        divisions = data.get("divisions")
        categories = data.get("categories")
        units_list = data.get("units_list")
        domains_organisations_list = data.get("domains_organisations_list")
        unit_status_list = data.get("unit_status_list")
        return (
            divisions, categories, units_list, domains_organisations_list, unit_status_list
        )

    def to_inner_structure(self):
        return {
            "divisions": self.divisions,
            "categories": self.categories,
            "units_list": self.units_list,
            "domains_organisations_list": self.domains_organisations_list,
            "unit_status_list": self.unit_status_list
        }

class GetunitListReportSuccess(Response):
    def __init__(self, unit_list_report):
        self.unit_list_report = unit_list_report

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["unit_list_report"])
        unit_list_report = data.get("unit_list_report")
        return GetunitListReportSuccess(unit_list_report)

    def to_inner_structure(self):
        return {
            "unit_list_report" : self.unit_list_report
        }

class GetStatutoryNotificationsListReportFilterSuccess(Response):
    def __init__(self, domains, act_legal_entity):
        self.domains = domains
        self.act_legal_entity = act_legal_entity

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["domains", "act_legal_entity"])
        domains = data.get("domains")
        act_legal_entity = data.get("act_legal_entity")
        return GetStatutoryNotificationsListReportFilterSuccess(
            domains, act_legal_entity
        )

    def to_inner_structure(self):
        return {
            "domains": self.domains,
            "act_legal_entity": self.act_legal_entity
        }

class GetStatutoryNotificationReportDataSuccess(Response):
    def __init__(self, stat_notf_list_report):
        self.stat_notf_list_report = stat_notf_list_report

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["stat_notf_list_report"])
        stat_notf_list_report = data.get("stat_notf_list_report")
        return GetStatutoryNotificationReportDataSuccess(stat_notf_list_report)

    def to_inner_structure(self):
        return {
            "stat_notf_list_report" : self.stat_notf_list_report
        }

class GetAuditTrailReportDataSuccess(Response):
    def __init__(self, audit_activities, total_count):
        self.audit_activities = audit_activities
        self.total_count = total_count

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["audit_activities", "total_count"])
        audit_activities = data.get("audit_activities")
        total_count = data.get("total_count")
        return GetAuditTrailReportDataSuccess(audit_activities, total_count)

    def to_inner_structure(self):
        return {
            "audit_activities" : self.audit_activities,
            "total_count": self.total_count
        }

class GetRiskReportFiltersSuccess(Response):
    def __init__(
        self, domains, divisions, categories, units_list, act_legal_entity,
        compliance_task_list, compliance_task_status
    ):
        self.domains = domains
        self.divisions = divisions
        self.categories = categories
        self.units_list = units_list
        self.act_legal_entity = act_legal_entity
        self.compliance_task_list = compliance_task_list
        self.compliance_task_status = compliance_task_status

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "domains", "divisions", "categories", "units_list", "act_legal_entity",
            "compliance_task_list", "compliance_task_status"
        ])
        domains = data.get("domains")
        divisions = data.get("divisions")
        categories = data.getr("categories")
        units_list = data.get("units_list")
        act_legal_entity = data.get("act_legal_entity")
        compliance_task_list = data.get("compliance_task_list")
        compliance_task_status = data.get("compliance_task_status")
        return GetRiskReportFiltersSuccess(
           domains, divisions, categories, units_list, act_legal_entity,
           compliance_task_list, compliance_task_status
        )

    def to_inner_structure(self):
        return {
            "domains": self.domains,
            "divisions": self.divisions,
            "categories": self.categories,
            "units_list": self.units_list,
            "act_legal_entity": self.act_legal_entity,
            "compliance_task_list": self.compliance_task_list,
            "compliance_task_status": self.compliance_task_status
        }

class GetRiskReportSuccess(Response):
    def __init__(self, risk_report):
        self.risk_report = risk_report

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["risk_report"])
        risk_report = data.get("risk_report")
        return GetRiskReportSuccess(risk_report)

    def to_inner_structure(self):
        return {
            "risk_report" : self.risk_report
        }

class ExportToCSVSuccess(Response):
    def __init__(self, link):
        self.link = link

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["link"])
        link = data.get("link")
        return ExportToCSVSuccess(link)

    def to_inner_structure(self):
        return {
            "link" : self.link
        }

def _init_Response_class_map():
    classes = [
        GetComplianceDetailsReportFiltersSuccess,
        GetComplianceDetailsReportSuccess, GetRiskReportFiltersSuccess,
        GetServiceProviderReportFiltersSuccess,
        GetServiceProviderWiseComplianceSuccess, GetClientReportFiltersSuccess,
        GetAssigneewisecomplianceReportSuccess, GetUnitwisecomplianceReportSuccess,
        GetReassignComplianceTaskReportFiltersSuccess,
        GetReassignComplianceTaskDetailsSuccess,
        GetTaskApplicabilityStatusFiltersSuccess,
        GetComplianceTaskApplicabilityStatusReportSuccess,
        GetComplianceActivityReportFiltersSuccess, GetComplianceActivityReportSuccess,
        GetReassignedHistoryReportFiltersSuccess, GetReassignedHistoryReportSuccess,
        GetStatusReportConsolidatedFiltersSuccess, GetStatusReportConsolidatedSuccess,
        GetStatutorySettingsUnitWiseFiltersSuccess, GetStatutorySettingsUnitWiseSuccess,
        GetDomainScoreCardFiltersSuccess, GetDomainScoreCardSuccess,
        GetLEWiseScoreCardFiltersSuccess, GetLEWiseScoreCardSuccess,
        GetWorkFlowScoreCardFiltersSuccess, GetWorkFlowScoreCardSuccess,
        GetStatutoryNotificationsListFiltersSuccess,
        GetStatutoryNotificationsListReportSuccess,
        GetClientDetailsReportDataSuccess, GetActivityLogFiltersSuccess,
        GetActivityLogReportSuccess, GetLoginTraceSuccess,
        GetClientDetailsReportFiltersSuccess, ExportToCSVSuccess,
        GetLegalEntityWiseReportFiltersSuccess,
        GetLegalEntityWiseReportSuccess,
        GetDomainWiseReportFiltersSuccess,
        GetDomainWiseReportSuccess,
        GetUnitWiseReportFiltersSuccess,
        GetUnitWiseReportSuccess,
        GetServiceProviderWiseReportFiltersSuccess,
        GetServiceProviderWiseReportSuccess,
        GetUserWiseReportFiltersSuccess,
        GetUserWiseReportSuccess,
        GetUnitListReportFiltersSuccess,
        GetunitListReportSuccess,
        GetStatutoryNotificationsListReportFilterSuccess,
        GetStatutoryNotificationReportDataSuccess,
        GetAuditTrailReportDataSuccess,
        GetRiskReportSuccess
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
        session_token = parse_structure_CustomTextType_50(session_token)
        request = data.get("request")
        request = parse_structure_VariantType_clientreport_Request(request)
        return RequestFormat(session_token, request)

    def to_structure(self):
        return {
            "session_token": to_structure_CustomTextType_50(self.session_token),
            "request": to_structure_VariantType_clientreport_Request(self.request),
        }

#
# ComplianceName
#

class ComplianceName(object):
    def __init__(self, compliance_id, compliance_name):
        self.compliance_id = compliance_id
        self.compliance_name = compliance_name

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["compliance_id", "compliance_name"])
        compliance_id = data.get("compliance_id")
        compliance_id = parse_structure_UnsignedIntegerType_32(compliance_id)
        compliance_name = data.get("compliance_name")
        compliance_name = parse_structure_CustomTextType_500(compliance_name)
        return ComplianceName(compliance_id, compliance_name)

    def to_structure(self):
        return {
            "compliance_id": to_structure_SignedIntegerType_8(self.compliance_id),
            "compliance_name": to_structure_CustomTextType_500(self.compliance_name),
        }

#
# User
#

class User(object):
    def __init__(self, employee_id, employee_code, employee_name):
        self.employee_id = employee_id
        self.employee_code = employee_code
        self.employee_name = employee_name

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["employee_id", "employee_code", "employee_name"])
        employee_id = data.get("employee_id")
        employee_id = parse_structure_UnsignedIntegerType_32(employee_id)
        employee_code = data.get("employee_code")
        employee_code = parse_structure_OptionalType_CustomTextType_50(employee_code)
        employee_name = data.get("employee_name")
        employee_name = parse_structure_CustomTextType_50(employee_name)
        return User(employee_id, employee_code, employee_name)

    def to_structure(self):
        return {
            "employee_id": to_structure_SignedIntegerType_8(self.employee_id),
            "employee_code": to_structure_OptionalType_CustomTextType_50(self.employee_code),
            "employee_name": to_structure_CustomTextType_50(self.employee_name),
        }

#
# ComplianceDetails
#

class ComplianceDetails(object):
    def __init__(self, compliance_name, assignee, due_date, completion_date, validity_date, documents, remarks):
        self.compliance_name = compliance_name
        self.assignee = assignee
        self.due_date = due_date
        self.completion_date = completion_date
        self.validity_date = validity_date
        self.documents = documents
        self.remarks = remarks

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["compliance_name", "assignee", "due_date", "completion_date", "validity_date", "documents", "remarks"])
        compliance_name = data.get("compliance_name")
        compliance_name = parse_structure_CustomTextType_500(compliance_name)
        assignee = data.get("assignee")
        assignee = parse_structure_CustomTextType_100(assignee)
        due_date = data.get("due_date")
        due_date = parse_structure_CustomTextType_20(due_date)
        completion_date = data.get("completion_date")
        completion_date = parse_structure_OptionalType_CustomTextType_20(completion_date)
        validity_date = data.get("validity_date")
        validity_date = parse_structure_OptionalType_CustomTextType_20(validity_date)
        documents = data.get("documents")
        documents = parse_structure_OptionalType_VectorType_CustomTextType_500(documents)
        remarks = data.get("remarks")
        remarks = parse_structure_CustomTextType_500(remarks)
        return ComplianceDetails(compliance_name, assignee, due_date, completion_date, validity_date, documents, remarks)

    def to_structure(self):
        return {
            "compliance_name": to_structure_CustomTextType_500(self.compliance_name),
            "assignee": to_structure_CustomTextType_100(self.assignee),
            "due_date": to_structure_CustomTextType_20(self.due_date),
            "completion_date": to_structure_OptionalType_CustomTextType_20(self.completion_date),
            "validity_date": to_structure_OptionalType_CustomTextType_20(self.validity_date),
            "documents": to_structure_OptionalType_VectorType_CustomTextType_500(self.documents),
            "remarks": to_structure_CustomTextType_500(self.remarks),
        }

#
# Level1Statutory
#

class Level1Compliance(object):

    def __init__(
        self, statutory_mapping, compliance_name, description,
        penal_consequences, compliance_frequency, repeats
    ):
        self.statutory_mapping = statutory_mapping
        self.compliance_name = compliance_name
        self.description = description
        self.penal_consequences = penal_consequences
        self.compliance_frequency = compliance_frequency
        self.repeats = repeats

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "statutory_mapping", "compliance_name",
            "description", "penal_consequences", "compliance_frequency",
            "repeats"
        ])
        statutory_mapping = data.get("statutory_mapping")
        statutory_mapping = parse_structure_Text(statutory_mapping)
        compliance_name = data.get("compliance_name")
        compliance_name = parse_structure_Text(compliance_name)
        description = data.get("description")
        description = parse_structure_Text(description)
        penal_consequences = data.get("penal_consequences")
        penal_consequences = parse_structure_OptionalType_CustomTextType_500(penal_consequences)
        compliance_frequency = data.get("compliance_frequency")
        compliance_frequency = parse_structure_CustomTextType_50(compliance_frequency)
        repeats = data.get("repeats")
        repeats = parse_structure_CustomTextType_500(repeats)
        return Level1Compliance(
            statutory_mapping, compliance_name, description,
            penal_consequences, compliance_frequency, repeats
        )

    def to_structure(self):
        return {
            "statutory_mapping": to_structure_Text(self.statutory_mapping),
            "compliance_name": to_structure_CustomTextType_500(self.compliance_name),
            "description": to_structure_Text(self.description),
            "penal_consequences": to_structure_OptionalType_CustomTextType_500(self.penal_consequences),
            "compliance_frequency": to_structure_CustomTextType_50(self.compliance_frequency),
            "repeats"  : to_structure_CustomTextType_500(self.repeats)
        }

class Level1Statutory(object):
    def __init__(self, unit_id, unit_name, address, compliances):
        self.unit_id = unit_id
        self.unit_name = unit_name
        self.address = address
        self.compliances = compliances

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["unit_id", "unit_name", "address", "compliances"])
        unit_id = data.get("unit_id")
        unit_id = parse_structure_UnsignedIntegerType_32(unit_id)
        unit_name = data.get("unit_name")
        unit_name = parse_structure_CustomTextType_100(unit_name)
        address = data.get("address")
        address = parse_structure_CustomTextType_250(address)
        compliances = data.get("compliances")
        compliances = parse_structure_VectorType_RecordType_clientreport_Level1Compliance(compliances)
        return Level1Statutory(unit_id, unit_name, address, compliances)

    def to_structure(self):
        return {
            "unit_id": to_structure_UnsignedIntegerType_32(self.unit_id),
            "unit_name": to_structure_CustomTextType_100(self.unit_name),
            "address": to_structure_CustomTextType_250(self.address),
            "compliances": to_structure_VectorType_RecordType_clientreport_Level1Compliance(self.compliances)
        }

class RiskData(object):
    def __init__(
        self, business_group_name, legal_entity_name, division_name,
        level_1_statutory_wise_units
    ):
        self.business_group_name = business_group_name
        self.legal_entity_name = legal_entity_name
        self.division_name = division_name
        self.level_1_statutory_wise_units = level_1_statutory_wise_units

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "business_group_name", "legal_entity_name",
            "division_name", "level_1_statutory_wise_units"
        ])
        business_group_name = data.get("business_group_name")
        business_group_name = parse_structure_OptionalType_CustomTextType_100(business_group_name)
        legal_entity_name = data.get("legal_entity_name")
        legal_entity_name = parse_structure_CustomTextType_100(legal_entity_name)
        division_name = data.get("division_name")
        division_name = parse_structure_OptionalType_CustomTextType_100(division_name)
        level_1_statutory_wise_units = data.get("level_1_statutory_wise_units")
        level_1_statutory_wise_units = parse_structure_MapType_CustomTextType_50_VectorType_RecordType_clientreport_Level1Statutory(level_1_statutory_wise_units)
        return RiskData(
            business_group_name, legal_entity_name, division_name,
            level_1_statutory_wise_units
        )

    def to_structure(self):
        return {
            "business_group_name": to_structure_OptionalType_CustomTextType_100(self.business_group_name),
            "legal_entity_name": to_structure_CustomTextType_100(self.legal_entity_name),
            "division_name": to_structure_OptionalType_CustomTextType_100(self.division_name),
            "level_1_statutory_wise_units": to_structure_MapType_CustomTextType_500_VectorType_RecordType_clientreport_Level1Statutory(self.level_1_statutory_wise_units),
        }

#
# ServiceProviderCompliance
#

class ServiceProviderCompliance(object):
    def __init__(self, service_provider_name, address, contract_from, contract_to, contact_person, contact_no, unit_wise_compliance):
        self.service_provider_name = service_provider_name
        self.address = address
        self.contract_from = contract_from
        self.contract_to = contract_to
        self.contact_person = contact_person
        self.contact_no = contact_no
        self.unit_wise_compliance = unit_wise_compliance

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["service_provider_name", "address", "contract_from", "contract_to", "contact_person", "contact_no", "unit_wise_compliance"])
        service_provider_name = data.get("service_provider_name")
        service_provider_name = parse_structure_CustomTextType_50(service_provider_name)
        address = data.get("address")
        address = to_structure_OptionalType_CustomTextType_250(address)
        contract_from = data.get("contract_from")
        contract_from = parse_structure_CustomTextType_20(contract_from)
        contract_to = data.get("contract_to")
        contract_to = parse_structure_CustomTextType_20(contract_to)
        contact_person = data.get("contact_person")
        contact_person = parse_structure_CustomTextType_50(contact_person)
        contact_no = data.get("contact_no")
        contact_no = parse_structure_CustomTextType_20(contact_no)
        unit_wise_compliance = data.get("unit_wise_compliance")
        unit_wise_compliance = parse_structure_MapType_CustomTextType_50_VectorType_RecordType_clientreport_ComplianceUnit(unit_wise_compliance)
        return ServiceProviderCompliance(service_provider_name, address, contract_from, contract_to, contact_person, contact_no, unit_wise_compliance)

    def to_structure(self):
        return {
            "service_provider_name": to_structure_CustomTextType_50(self.service_provider_name),
            "address": to_structure_OptionalType_CustomTextType_250(self.address),
            "contract_from": to_structure_CustomTextType_20(self.contract_from),
            "contract_to": to_structure_CustomTextType_20(self.contract_to),
            "contact_person": to_structure_CustomTextType_50(self.contact_person),
            "contact_no": to_structure_CustomTextType_20(self.contact_no),
            "unit_wise_compliance": to_structure_MapType_CustomTextType_50_VectorType_RecordType_clientreport_ComplianceUnit(self.unit_wise_compliance),
        }

#
# Activities
#

class Activities(object):
    def __init__(self, unit_name, address, statutory_wise_compliances):
        self.unit_name = unit_name
        self.address = address
        self.statutory_wise_compliances = statutory_wise_compliances

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["unit_name", "address", "statutory_wise_compliances"])
        unit_name = data.get("unit_name")
        unit_name = parse_structure_CustomTextType_100(unit_name)
        address = data.get("address")
        address = parse_structure_CustomTextType_250(address)
        statutory_wise_compliances = data.get("statutory_wise_compliances")
        statutory_wise_compliances = parse_structure_MapType_CustomTextType_50_VectorType_RecordType_clientreport_ActivityCompliance(statutory_wise_compliances)
        return Activities(unit_name, address, statutory_wise_compliances)

    def to_structure(self):
        return {
            "unit_name": to_structure_CustomTextType_100(self.unit_name),
            "address": to_structure_CustomTextType_250(self.address),
            "statutory_wise_compliances": to_structure_MapType_CustomTextType_500_MapType_CustomTextType_500_VectorType_RecordType_clientreport_ActivityData(self.statutory_wise_compliances)
        }

#
# ActivityData
#

class ActivityData(object):
    def __init__(
        self, activity_date, activity_status, compliance_status, remarks,
        assignee_name
    ):
        self.activity_date = activity_date
        self.activity_status = activity_status
        self.compliance_status = compliance_status
        self.remarks = remarks
        self.assignee_name = assignee_name

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(
            data, [
                "activity_date", "activity_status", "compliance_status",
                "remarks", "assignee_name"
            ]
        )
        activity_date = data.get("activity_date")
        activity_date = parse_structure_CustomTextType_20(activity_date)
        activity_status = data.get("activity_status")
        activity_status = parse_structure_EnumType_core_COMPLIANCE_ACTIVITY_STATUS(activity_status)
        compliance_status = data.get("compliance_status")
        compliance_status = parse_structure_EnumType_core_COMPLIANCE_STATUS(compliance_status)
        remarks = data.get("remarks")
        remarks = parse_structure_OptionalType_CustomTextType_500(remarks)
        assignee_name = data.get("assignee_name")
        assignee_name = parse_structure_OptionalType_CustomTextType_500(assignee_name)
        return ActivityCompliance(
            activity_date, activity_status, compliance_status, remarks,
            assignee_name
        )

    def to_structure(self):
        return {
            "activity_date": to_structure_CustomTextType_20(self.activity_date),
            "activity_status": to_structure_EnumType_core_COMPLIANCE_ACTIVITY_STATUS(self.activity_status),
            "compliance_status": to_structure_EnumType_core_COMPLIANCE_STATUS(self.compliance_status),
            "remarks": to_structure_OptionalType_CustomTextType_500(self.remarks),
            "assignee_name": to_structure_OptionalType_CustomTextType_500(self.assignee_name)
        }

#
# ActivityCompliance
#

class ActivityCompliance(object):
    def __init__(self, compliance_name, activity_data):
        self.compliance_name = compliance_name
        self.activity_data = activity_data

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["compliance_name", "activity_data"])
        compliance_name = data.get("compliance_name")
        compliance_name = parse_structure_CustomTextType_500(compliance_name)
        activity_data = data.get("activity_data")
        activity_data = parse_structure_VectorType_RecordType_clientreport_ActivityData(activity_data)
        return ActivityCompliance(compliance_name, activity_data)

    def to_structure(self):
        return {
            "compliance_name": to_structure_CustomTextType_500(self.compliance_name),
            "activity_data": to_structure_VectorType_RecordType_clientreport_ActivityData(self.activity_data)
        }

#
# ActivityLog
#

class ActivityLog(object):
    def __init__(self, user_name, date_and_time, form_name, action):
        self.user_name = user_name
        self.date_and_time = date_and_time
        self.form_name = form_name
        self.action = action

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["user_name", "date_and_time", "form_name", "action"])
        user_name = data.get("user_name")
        user_name = parse_structure_CustomTextType_100(user_name)
        date_and_time = data.get("date_and_time")
        date_and_time = parse_structure_CustomTextType_20(date_and_time)
        form_name = data.get("form_name")
        form_name = parse_structure_CustomTextType_50(form_name)
        action = data.get("action")
        action = parse_structure_CustomTextType_500(action)
        return ActivityLog(user_name, date_and_time, form_name, action)

    def to_structure(self):
        return {
            "user_name": to_structure_CustomTextType_100(self.user_name),
            "date_and_time": to_structure_CustomTextType_20(self.date_and_time),
            "form_name": to_structure_CustomTextType_50(self.form_name),
            "action": to_structure_CustomTextType_500(self.action),
        }

#
# ApplicabilityCompliance
#

class ApplicabilityCompliance(object):
    def __init__(self, unit_id, unit_name, address, compliances):
        self.unit_id = unit_id
        self.unit_name = unit_name
        self.address = address
        self.compliances = compliances

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["unit_id", "unit_name", "address", "compliances"])
        unit_id = data.get("unit_id")
        unit_id = parse_structure_UnsignedIntegerType_32(unit_id)
        unit_name = data.get("unit_name")
        unit_name = parse_structure_CustomTextType_100(unit_name)
        address = data.get("address")
        address = parse_structure_CustomTextType_250(address)
        compliances = data.get("compliances")
        compliances = parse_structure_VectorType_RecordType_clientreport_ComplianceList(compliances)
        return ApplicabilityCompliance(unit_id, unit_name, address, compliances)

    def to_structure(self):
        return {
            "unit_id": to_structure_UnsignedIntegerType_32(self.unit_id),
            "unit_name": to_structure_CustomTextType_100(self.unit_name),
            "address": to_structure_CustomTextType_250(self.address),
            "compliances": to_structure_VectorType_RecordType_clientreport_ComplianceList(self.compliances),
        }

#
# AssigneeCompliance
#

class AssigneeCompliance(object):
    def __init__(self, business_group_name, legal_entity_name, division_name, user_wise_compliance):
        self.business_group_name = business_group_name
        self.legal_entity_name = legal_entity_name
        self.division_name = division_name
        self.user_wise_compliance = user_wise_compliance

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["business_group_name", "legal_entity_name", "division_name", "user_wise_compliance"])
        business_group_name = data.get("business_group_name")
        business_group_name = parse_structure_OptionalType_CustomTextType_100(business_group_name)
        legal_entity_name = data.get("legal_entity_name")
        legal_entity_name = parse_structure_CustomTextType_100(legal_entity_name)
        division_name = data.get("division_name")
        division_name = parse_structure_OptionalType_CustomTextType_100(division_name)

        user_wise_compliance = data.get("user_wise_compliance")
        user_wise_compliance = parse_structure_VectorType_RecordType_clientreport_UserWiseCompliance(user_wise_compliance)
        return AssigneeCompliance(business_group_name, legal_entity_name, division_name, user_wise_compliance)

    def to_structure(self):
        return {
            "business_group_name": to_structure_OptionalType_CustomTextType_100(self.business_group_name),
            "legal_entity_name": to_structure_CustomTextType_100(self.legal_entity_name),
            "division_name": to_structure_OptionalType_CustomTextType_100(self.division_name),
            "user_wise_compliance": to_structure_VectorType_RecordType_clientreport_UserWiseCompliance(self.user_wise_compliance),
        }

#
# ComplianceForUnit
#

class ComplianceForUnit(object):
    def __init__(self, compliance_name, description, statutory_dates, due_date, validity_date):
        self.compliance_name = compliance_name
        self.description = description
        self.statutory_dates = statutory_dates
        self.due_date = due_date
        self.validity_date = validity_date

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["compliance_name", "description", "statutory_dates", "due_date", "validity_date"])
        compliance_name = data.get("compliance_name")
        compliance_name = parse_structure_CustomTextType_500(compliance_name)
        description = data.get("description")
        description = parse_structure_Text(description)
        statutory_dates = data.get("statutory_dates")
        statutory_dates = parse_structure_VectorType_RecordType_core_StatutoryDate(statutory_dates)
        due_date = data.get("due_date")
        due_date = parse_structure_CustomTextType_20(due_date)
        validity_date = data.get("validity_date")
        validity_date = parse_structure_CustomTextType_20(validity_date)
        return ComplianceForUnit(compliance_name, description, statutory_dates, due_date, validity_date)

    def to_structure(self):
        return {
            "compliance_name": to_structure_CustomTextType_500(self.compliance_name),
            "description": to_structure_Text(self.description),
            "statutory_dates": parse_structure_VectorType_RecordType_core_StatutoryDate(self.statutory_dates),
            "due_date": to_structure_CustomTextType_20(self.due_date),
            "validity_date": to_structure_CustomTextType_20(self.validity_date),
        }

#
# ComplianceList
#

class ComplianceList(object):
    def __init__(self, statutory_provision, compliance_name, description, penal_consequences, compliance_frequency, repeats):
        self.statutory_provision = statutory_provision
        self.compliance_name = compliance_name
        self.description = description
        self.penal_consequences = penal_consequences
        self.compliance_frequency = compliance_frequency
        self.repeats = repeats

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["statutory_provision", "compliance_name", "description", "penal_consequences", "compliance_frequency", "repeats"])
        statutory_provision = data.get("statutory_provision")
        statutory_provision = parse_structure_Text(statutory_provision)
        compliance_name = data.get("compliance_name")
        compliance_name = parse_structure_VectorType_Text(compliance_name)
        description = data.get("description")
        description = parse_structure_Text(description)
        penal_consequences = data.get("penal_consequences")
        penal_consequences = parse_structure_OptionalType_CustomTextType_500(penal_consequences)
        compliance_frequency = data.get("compliance_frequency")
        compliance_frequency = parse_structure_EnumType_core_COMPLIANCE_FREQUENCY(compliance_frequency)
        repeats = data.get("repeats")
        repeats = parse_structure_CustomTextType_500(repeats)
        return ComplianceList(statutory_provision, compliance_name, description, penal_consequences, compliance_frequency, repeats)

    def to_structure(self):
        return {
            "statutory_provision": to_structure_Text(self.statutory_provision),
            "compliance_name": to_structure_VectorType_Text(self.compliance_name),
            "description": to_structure_Text(self.description),
            "penal_consequences": to_structure_OptionalType_CustomTextType_500(self.penal_consequences),
            "compliance_frequency": to_structure_EnumType_core_COMPLIANCE_FREQUENCY(self.compliance_frequency),
            "repeats": to_structure_CustomTextType_500(self.repeats),
        }

#
# ComplianceUnit
#

class ComplianceUnit(object):
    def __init__(self, compliance_name, unit_address, compliance_frequency, description, statutory_dates, due_date, validity_date, summary):
        self.compliance_name = compliance_name
        self.unit_address = unit_address
        self.compliance_frequency = compliance_frequency
        self.description = description
        self.statutory_dates = statutory_dates
        self.due_date = due_date
        self.validity_date = validity_date
        self.summary = summary

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["compliance_name", "unit_address", "compliance_frequency", "description", "statutory_dates", "due_date", "validity_date", "summary"])
        compliance_name = data.get("compliance_name")
        compliance_name = parse_structure_CustomTextType_500(compliance_name)
        unit_address = data.get("unit_address")
        unit_address = parse_structure_CustomTextType_500(unit_address)
        compliance_frequency = data.get("compliance_frequency")
        compliance_frequency = parse_structure_EnumType_core_COMPLIANCE_FREQUENCY(compliance_frequency)
        description = data.get("description")
        description = parse_structure_Text(description)
        statutory_dates = data.get("statutory_dates")
        statutory_dates = parse_structure_VectorType_RecordType_core_StatutoryDate(statutory_dates)
        due_date = data.get("due_date")
        due_date = parse_structure_OptionalType_CustomTextType_20(due_date)
        validity_date = data.get("validity_date")
        validity_date = parse_structure_OptionalType_CustomTextType_20(validity_date)
        summary = data.get("summary")
        summary = parse_structure_OptionalType_CustomTextType_50(summary)
        return ComplianceUnit(compliance_name, unit_address, compliance_frequency, description, statutory_dates, due_date, validity_date, summary)

    def to_structure(self):
        return {
            "compliance_name": to_structure_CustomTextType_500(self.compliance_name),
            "unit_address": to_structure_CustomTextType_500(self.unit_address),
            "compliance_frequency": to_structure_EnumType_core_COMPLIANCE_FREQUENCY(self.compliance_frequency),
            "description": to_structure_Text(self.description),
            "statutory_dates": to_structure_VectorType_RecordType_core_StatutoryDate(self.statutory_dates),
            "due_date": to_structure_OptionalType_CustomTextType_20(self.due_date),
            "validity_date": to_structure_OptionalType_CustomTextType_20(self.validity_date),
            "summary": to_structure_OptionalType_CustomTextType_50(self.summary),
        }

#
# DomainWiseCompliance
#

class DomainWiseCompliance(object):
    def __init__(self, domain_name, statutory_wise_compliances):
        self.domain_name = domain_name
        self.statutory_wise_compliances = statutory_wise_compliances

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["domain_name", "statutory_wise_compliances"])
        domain_name = data.get("domain_name")
        domain_name = parse_structure_CustomTextType_50(domain_name)
        statutory_wise_compliances = data.get("statutory_wise_compliances")
        statutory_wise_compliances = parse_structure_MapType_CustomTextType_50_VectorType_RecordType_clientreport_ActivityCompliance(statutory_wise_compliances)
        return DomainWiseCompliance(domain_name, statutory_wise_compliances)

    def to_structure(self):
        return {
            "domain_name": to_structure_CustomTextType_50(self.domain_name),
            "statutory_wise_compliances": to_structure_MapType_CustomTextType_50_VectorType_RecordType_clientreport_ActivityCompliance(self.statutory_wise_compliances),
        }

#
# FormName
#

class FormName(object):
    def __init__(self, form_id, form_name):
        self.form_id = form_id
        self.form_name = form_name

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["form_id", "form_name"])
        form_id = data.get("form_id")
        form_id = parse_structure_UnsignedIntegerType_32(form_id)
        form_name = data.get("form_name")
        form_name = parse_structure_CustomTextType_50(form_name)
        return FormName(form_id, form_name)

    def to_structure(self):
        return {
            "form_id": to_structure_SignedIntegerType_8(self.form_id),
            "form_name": to_structure_CustomTextType_50(self.form_name),
        }

#
# LoginTrace
#

class LoginTrace(object):
    def __init__(self,  created_on, action):
        self.created_on = created_on
        self.action = action

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["created_on", "action"])
        created_on = data.get("created_on")
        created_on = parse_structure_CustomTextType_50(created_on)
        action = data.get("action")
        action = to_structure_CustomTextType_500(action)
        return LoginTrace(created_on,  action)

    def to_structure(self):
        return {
            "created_on": to_structure_CustomTextType_20(self.created_on),
            "action": to_structure_CustomTextType_500(self.action),
        }

#
# ReassignUnitCompliance
#
class ReassignUnitCompliance(object):
    def __init__(self, unit_id, unit_name, address, reassign_compliances):
        self.unit_id = unit_id
        self.unit_name = unit_name
        self.address = address
        self.reassign_compliances = reassign_compliances

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["unit_id", "unit_name",  "address", "reassign_compliances"])
        unit_id = data.get("unit_id")
        unit_id = parse_structure_UnsignedIntegerType_32(unit_id)
        unit_name = data.get("unit_name")
        unit_name = parse_structure_CustomTextType_100(unit_name)
        address = data.get("address")
        address = parse_structure_CustomTextType_100(address)
        reassign_compliances = data.get("reassign_compliances")
        reassign_compliances = parse_structure_VectorType_RecordType_clientreport_ReassignCompliance(reassign_compliances)
        return ReassignCompliance(unit_id, unit_name, address, reassign_compliances)

    def to_structure(self):
        return {
            "unit_id": to_structure_UnsignedIntegerType_32(self.unit_id),
            "unit_name": to_structure_CustomTextType_100(self.unit_name),
            "address": to_structure_CustomTextType_100(self.address),
            "reassign_compliances": to_structure_VectorType_RecordType_clientreport_ReassignCompliance(self.reassign_compliances)
        }


#
# ReassignHistory
#

class ReassignHistory(object):
    def __init__(self, reassigned_from, reassigned_to, reassigned_date, reassign_reason):
        self.reassigned_from = reassigned_from
        self.reassigned_to = reassigned_to
        self.reassigned_date = reassigned_date
        self.reassign_reason = reassign_reason

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["reassigned_from", "reassigned_to", "reassigned_date", "reassign_reason"])
        reassigned_from = data.get("reassigned_from")
        reassigned_from = parse_structure_CustomTextType_100(reassigned_from)
        reassigned_to = data.get("reassigned_to")
        reassigned_to = parse_structure_CustomTextType_100(reassigned_to)
        reassigned_date = data.get("reassigned_date")
        reassigned_date = parse_structure_CustomTextType_20(reassigned_date)
        reassign_reason = data.get("reassign_reason")
        reassign_reason = parse_structure_CustomTextType_500(reassign_reason)
        return ReassignHistory(reassigned_from, reassigned_to, reassigned_date, reassign_reason)

    def to_structure(self):
        return {
            "reassigned_from": to_structure_CustomTextType_100(self.reassigned_from),
            "reassigned_to": to_structure_CustomTextType_100(self.reassigned_to),
            "reassigned_date": to_structure_CustomTextType_20(self.reassigned_date),
            "reassign_reason": to_structure_CustomTextType_500(self.reassign_reason),
        }


#
# ReassignCompliance
#

class ReassignCompliance(object):
    def __init__(self, compliance_name, due_date, reassign_history):
        self.compliance_name = compliance_name
        self.due_date = due_date
        self.reassign_history = reassign_history

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["compliance_name", "due_date", "assignee", "reassign_history"])

        compliance_name = data.get("compliance_name")
        compliance_name = parse_structure_CustomTextType_500(compliance_name)
        due_date = data.get("due_date")
        due_date = parse_structure_OptionalType_CustomTextType_50(due_date)
        reassign_history = data.get("reassign_history")
        reassign_history = parse_structure_VectorType_RecordType_clientreport_ReassignHistory(reassign_history)
        return ReassignCompliance(compliance_name, due_date, reassign_history)

    def to_structure(self):
        return {
            "compliance_name": to_structure_CustomTextType_500(self.compliance_name),
            "due_date": to_structure_OptionalType_CustomTextType_50(self.due_date),
            "reassign_history": to_structure_VectorType_RecordType_clientreport_ReassignHistory(self.reassign_history),
        }


#
# StatutoryReassignCompliance
#

class StatutoryReassignCompliance(object):
    def __init__(self, level_1_statutory_name, compliance):
        self.level_1_statutory_name = level_1_statutory_name
        self.compliance = compliance

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["level_1_statutory_name", "compliance"])
        level_1_statutory_name = data.get("level_1_statutory_name")
        level_1_statutory_name = parse_structure_CustomTextType_500(level_1_statutory_name)
        compliance = data.get("compliance")
        compliance = parse_structure_VectorType_RecordType_clientreport_ReassignUnitCompliance(compliance)
        return StatutoryReassignCompliance(level_1_statutory_name, compliance)

    def to_structure(self):
        return {
            "level_1_statutory_name": to_structure_CustomTextType_500(self.level_1_statutory_name),
            "compliance": to_structure_VectorType_RecordType_clientreport_ReassignUnitCompliance(self.compliance),
        }

#
# UnitCompliance
#

class UnitCompliance(object):
    def __init__(self, business_group_name, legal_entity_name, division_name, unit_wise_compliances):
        self.business_group_name = business_group_name
        self.legal_entity_name = legal_entity_name
        self.division_name = division_name
        self.unit_wise_compliances = unit_wise_compliances

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["business_group_name", "legal_entity_name", "division_name", "unit_wise_compliances"])
        business_group_name = data.get("business_group_name")
        business_group_name = parse_structure_OptionalType_CustomTextType_100(business_group_name)
        legal_entity_name = data.get("legal_entity_name")
        legal_entity_name = parse_structure_CustomTextType_50(legal_entity_name)
        division_name = data.get("division_name")
        division_name = parse_structure_OptionalType_CustomTextType_100(division_name)
        unit_wise_compliances = data.get("unit_wise_compliances")
        unit_wise_compliances = parse_structure_MapType_CustomTextType_50_VectorType_RecordType_clientreport_ComplianceUnit(unit_wise_compliances)
        return UnitCompliance(business_group_name, legal_entity_name, division_name, unit_wise_compliances)

    def to_structure(self):
        return {
            "business_group_name": to_structure_OptionalType_CustomTextType_100(self.business_group_name),
            "legal_entity_name": to_structure_CustomTextType_50(self.legal_entity_name),
            "division_name": to_structure_OptionalType_CustomTextType_100(self.division_name),
            "unit_wise_compliances": to_structure_MapType_CustomTextType_50_VectorType_RecordType_clientreport_ComplianceUnit(self.unit_wise_compliances),
        }

#
# UnitWiseCompliance
#

class UnitWiseCompliance(object):
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
        compliances = parse_structure_VectorType_RecordType_clientreport_ComplianceForUnit(compliances)
        return UnitWiseCompliance(unit_name, address, compliances)

    def to_structure(self):
        return {
            "unit_name": to_structure_CustomTextType_100(self.unit_name),
            "address": to_structure_CustomTextType_250(self.address),
            "compliances": to_structure_VectorType_RecordType_clientreport_ComplianceForUnit(self.compliances),
        }

#
# UnitName
#

class UnitName(object):
    def __init__(self, unit_name, address):
        self.unit_name = unit_name
        self.address = address

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["unit_name", "address"])
        unit_name = data.get("unit_name")
        unit_name = parse_structure_CustomTextType_100(unit_name)
        address = data.get("address")
        address = parse_structure_CustomTextType_250(address)
        return UnitName(unit_name, address)

    def to_structure(self):
        return {
            "unit_name": to_structure_CustomTextType_100(self.unit_name),
            "address": to_structure_CustomTextType_250(self.address),
        }

#
# Units for Legal Entity
#

class UnitLegalEntity(object):
    def __init__(self, unit_id, unit_code, unit_name, domain_id, country_id, legal_entity_id):
        self.unit_id = unit_id
        self.unit_code = unit_code
        self.unit_name = unit_name
        self.domain_id = domain_id
        self.country_id = country_id
        self.legal_entity_id = legal_entity_id

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "unit_id", "unit_code", "unit_name", "domain_id", "country_id", "legal_entity_id"
            ]
        )
        unit_id = data.get("unit_id")
        unit_code = data.get("unit_code")
        unit_name = data.get("unit_name")
        domain_id = data.get("domain_id")
        country_id = data.get("country_id")
        legal_entity_id = data.get("legal_entity_id")
        return UnitLegalEntity(unit_id, unit_code, unit_name, domain_id, country_id, legal_entity_id)

    def to_structure(self):
        return {
            "unit_id": self.unit_id,
            "unit_code": self.unit_code,
            "unit_name": self.unit_name,
            "domain_id": self.domain_id,
            "country_id": self.country_id,
            "legal_entity_id": self.legal_entity_id
        }

#
# Acts for Legal Entity
#

class ActLegalEntity(object):
    def __init__(
        self, legal_entity_id, domain_id, unit_id, compliance_id,
        statutory_mapping
    ):
        self.legal_entity_id = legal_entity_id
        self.domain_id = domain_id
        self.unit_id = unit_id
        self.compliance_id = compliance_id
        self.statutory_mapping = statutory_mapping

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "legal_entity_id", "domain_id", "unit_id", "compliance_id",
            "statutory_mapping",
            ]
        )
        legal_entity_id = data.get("legal_entity_id")
        domain_id = data.get("domain_id")
        unit_id = data.get("unit_id")
        compliance_id = data.get("compliance_id")
        statutory_mapping = data.get("statutory_mapping")

        return ActLegalEntity(
            legal_entity_id, domain_id, unit_id, compliance_id,
            statutory_mapping
        )

    def to_structure(self):
        return {
            "legal_entity_id": self.legal_entity_id,
            "domain_id": self.domain_id,
            "unit_id": self.unit_id,
            "compliance_id": self.compliance_id,
            "statutory_mapping": self.statutory_mapping,
        }

#
# Compliance Task for Legal Entity
#

class TaskLegalEntity(object):
    def __init__(
        self, legal_entity_id, domain_id, unit_id, compliance_id,
        compliance_task, frequency_id, statutory_mapping
    ):
        self.legal_entity_id = legal_entity_id
        self.domain_id = domain_id
        self.unit_id = unit_id
        self.compliance_id = compliance_id
        self.compliance_task = compliance_task
        self.frequency_id = frequency_id
        self.statutory_mapping = statutory_mapping

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "legal_entity_id", "domain_id", "unit_id", "compliance_id",
            "compliance_task", "frequency_id", "statutory_mapping",
            ]
        )
        legal_entity_id = data.get("legal_entity_id")
        domain_id = data.get("domain_id")
        unit_id = data.get("unit_id")
        compliance_id = data.get("compliance_id")
        compliance_task = data.get("compliance_task")
        frequency_id = data.get("frequency_id")
        statutory_mapping = data.get("statutory_mapping")

        return TaskLegalEntity(
            legal_entity_id, domain_id, unit_id, compliance_id,
            compliance_task, frequency_id, statutory_mapping
        )

    def to_structure(self):
        return {
            "legal_entity_id": self.legal_entity_id,
            "domain_id": self.domain_id,
            "unit_id": self.unit_id,
            "compliance_id": self.compliance_id,
            "compliance_task": self.compliance_task,
            "frequency_id": self.frequency_id,
            "statutory_mapping": self.statutory_mapping,
        }

#
# Compliance Frequency
#

class ComplianceFrequency(object):
    def __init__(
        self, frequency_id, frequency_name
    ):
        self.frequency_id = frequency_id
        self.frequency_name = frequency_name

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "frequency_id", "frequency_name"
            ]
        )
        frequency_id = data.get("frequency_id")
        frequency_name = data.get("frequency_name")
        return ComplianceFrequency(
            frequency_id, frequency_name
        )

    def to_structure(self):
        data = {
            "frequency_id": self.frequency_id,
            "frequency_name": self.frequency_name
        }
        return data

#
# Compliance user type
#

class ComplianceUserType(object):
    def __init__(self, user_type_id, user_type):
        self.user_type_id = user_type_id
        self.user_type = user_type

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["user_type_id", "user_type"])
        user_type_id = data.get("user_type_id")
        user_type = data.get("user_type")
        return ComplianceUserType(user_type_id, user_type)

    def to_structure(self):
        data = {
            "user_type_id": self.user_type_id,
            "user_type": self.user_type
        }
        return data

#
# Compliance Task Status
#

class ComplianceTaskStatus(object):
    def __init__(self, task_status_id, task_status):
        self.task_status_id = task_status_id
        self.task_status = task_status

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["task_status_id", "task_status"])
        task_status_id = data.get("task_status_id")
        task_status = data.get("task_status")
        return ComplianceTaskStatus(task_status_id, task_status)

    def to_structure(self):
        return {
            "task_status_id": self.task_status_id,
            "task_status": self.task_status
        }

#
# Compliance user type - users
#

class ComplianceUsers(object):
    def __init__(
        self, legal_entity_id, country_id, domain_id, unit_id, compliance_id,
        assignee, assignee_name, concurrence_person, concurrer_name,
        approval_person, approver_name
    ):
        self.legal_entity_id = legal_entity_id
        self.country_id = country_id
        self.domain_id = domain_id
        self.unit_id = unit_id
        self.compliance_id = compliance_id
        self.assignee = assignee
        self.assignee_name = assignee_name
        self.concurrence_person = concurrence_person
        self.concurrer_name = concurrer_name
        self.approval_person = approval_person
        self.approver_name = approver_name

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "legal_entity_id", "country_id", "domain_id", "unit_id", "compliance_id",
            "assignee", "assignee_name", "concurrence_person", "concurrer_name",
            "approval_person", "approver_name"
        ])
        legal_entity_id = data.get("legal_entity_id")
        country_id = data.get("country_id")
        domain_id = data.get("domain_id")
        unit_id = data.get("unit_id")
        compliance_id = data.get("compliance_id")
        assignee = data.get("assignee")
        assignee_name = data.get("assignee_name")
        concurrence_person = data.get("concurrence_person")
        concurrer_name = data.get("concurrer_name")
        approval_person = data.get("approval_person")
        approver_name = data.get("approver_name")
        return ComplianceUsers(
            legal_entity_id, country_id, domain_id, unit_id, compliance_id, assignee,
            assignee_name, concurrence_person, concurrer_name, approval_person,
            approver_name
        )

    def to_structure(self):
        data = {
            "legal_entity_id": self.legal_entity_id,
            "country_id": self.country_id,
            "domain_id": self.domain_id,
            "unit_id": self.unit_id,
            "compliance_id": self.compliance_id,
            "assignee": self.assignee,
            "assignee_name": self.assignee_name,
            "concurrence_person": self.concurrence_person,
            "concurrer_name": self.concurrer_name,
            "approval_person": self.approval_person,
            "approver_name": self.approver_name
        }
        return data

#
# Legal Entity Wise Report
#

class LegalEntityWiseReport(object):
    def __init__(
        self, compliance_history_id, compliance_activity_id, country_id, legal_entity_id,
        domain_id, unit_id, compliance_id, unit_name, statutory_mapping, compliance_task,
        frequency_name, due_date, task_status, assignee_name, activity_status, activity_date,
        document_name, completion_date, url, logo_url
    ):
        self.compliance_history_id = compliance_history_id
        self.compliance_activity_id = compliance_activity_id
        self.country_id = country_id
        self.legal_entity_id = legal_entity_id
        self.domain_id = domain_id
        self.unit_id = unit_id
        self.compliance_id = compliance_id
        self.unit_name = unit_name
        self.statutory_mapping = statutory_mapping
        self.compliance_task = compliance_task
        self.frequency_name = frequency_name
        self.due_date = due_date
        self.task_status = task_status
        self.assignee_name = assignee_name
        self.activity_status = activity_status
        self.activity_date = activity_date
        self.document_name = document_name
        self.completion_date = completion_date
        self.url = url
        self.logo_url = logo_url

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "compliance_history_id", "compliance_activity_id", "country_id", "legal_entity_id",
            "domain_id", "unit_id", "compliance_id", "unit_name", "statutory_mapping", "compliance_task",
            "frequency_name", "due_date", "task_status", "assignee_name", "activity_status", "activity_date",
            "document_name", "completion_date", "url", "logo_url"
        ])
        compliance_history_id = data.get("compliance_history_id")
        compliance_activity_id = data.get("compliance_activity_id")
        country_id = data.get("country_id")
        legal_entity_id = data.get("legal_entity_id")
        domain_id = data.get("domain_id")
        unit_id = data.get("unit_id")
        compliance_id = data.get("compliance_id")
        unit_name = data.get("unit_name")
        statutory_mapping = data.get("statutory_mapping")
        compliance_task = data.get("compliance_task")
        frequency_name = data.get("frequency_name")
        due_date = data.get("due_date")
        task_status = data.get("task_status")
        assignee_name = data.get("assignee_name")
        activity_status = data.get("activity_status")
        activity_date = data.get("activity_date")
        document_name = data.get("document_name")
        completion_date = data.get("completion_date")
        url = data.get("url")
        logo_url = data.get("logo_url")
        return LegalEntityWiseReport(
            compliance_history_id, compliance_activity_id, country_id, legal_entity_id, domain_id, unit_id, compliance_id,
            unit_name, statutory_mapping, compliance_task, frequency_name,
            due_date, task_status, assignee_name, activity_status, activity_date,
            document_name, completion_date, url, logo_url
        )

    def to_structure(self):
        data = {
            "compliance_history_id": self.compliance_history_id,
            "compliance_activity_id": self.compliance_activity_id,
            "country_id": self.country_id,
            "legal_entity_id": self.legal_entity_id,
            "domain_id": self.domain_id,
            "unit_id": self.unit_id,
            "compliance_id": self.compliance_id,
            "unit_name": self.unit_name,
            "statutory_mapping": self.statutory_mapping,
            "compliance_task": self.compliance_task,
            "frequency_name": self.frequency_name,
            "due_date": self.due_date,
            "task_status": self.task_status,
            "assignee_name": self.assignee_name,
            "activity_status": self.activity_status,
            "activity_date": self.activity_date,
            "document_name": self.document_name,
            "completion_date": self.completion_date,
            "url": self.url,
            "logo_url": self.logo_url
        }
        return data

#
# Legal Entity Wise Report
#

class UnitWiseReport(object):
    def __init__(
        self, compliance_history_id, compliance_activity_id, country_id, legal_entity_id, domain_id,
        unit_id, compliance_id, unit_name, statutory_mapping, compliance_task, frequency_name,
        due_date, task_status, assignee_name, activity_status, activity_date,
        document_name, completion_date, url, domain_name, logo_url
    ):
        self.compliance_history_id = compliance_history_id
        self.compliance_activity_id = compliance_activity_id
        self.country_id = country_id
        self.legal_entity_id = legal_entity_id
        self.domain_id = domain_id
        self.unit_id = unit_id
        self.compliance_id = compliance_id
        self.unit_name = unit_name
        self.statutory_mapping = statutory_mapping
        self.compliance_task = compliance_task
        self.frequency_name = frequency_name
        self.due_date = due_date
        self.task_status = task_status
        self.assignee_name = assignee_name
        self.activity_status = activity_status
        self.activity_date = activity_date
        self.document_name = document_name
        self.completion_date = completion_date
        self.url = url
        self.domain_name = domain_name
        self.logo_url = logo_url

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "compliance_history_id", "compliance_activity_id", "country_id", "legal_entity_id",
            "domain_id", "unit_id", "compliance_id", "unit_name", "statutory_mapping", "compliance_task",
            "frequency_name", "due_date", "task_status", "assignee_name", "activity_status", "activity_date",
            "document_name", "completion_date", "url", "domain_name", "logo_url"
        ])
        compliance_history_id = data.get("compliance_history_id")
        compliance_activity_id = data.get("compliance_activity_id")
        country_id = data.get("country_id")
        legal_entity_id = data.get("legal_entity_id")
        domain_id = data.get("domain_id")
        unit_id = data.get("unit_id")
        compliance_id = data.get("compliance_id")
        unit_name = data.get("unit_name")
        statutory_mapping = data.get("statutory_mapping")
        compliance_task = data.get("compliance_task")
        frequency_name = data.get("frequency_name")
        due_date = data.get("due_date")
        task_status = data.get("task_status")
        assignee_name = data.get("assignee_name")
        activity_status = data.get("activity_status")
        activity_date = data.get("activity_date")
        document_name = data.get("document_name")
        completion_date = data.get("completion_date")
        url = data.get("url")
        domain_name = data.get("domain_name")
        logo_url = data.get("logo_url")
        return UnitWiseReport(
            compliance_history_id, compliance_activity_id, country_id, legal_entity_id,
            domain_id, unit_id, compliance_id, unit_name, statutory_mapping, compliance_task,
            frequency_name, due_date, task_status, assignee_name, activity_status, activity_date,
            document_name, completion_date, url, domain_name, logo_url
        )

    def to_structure(self):
        data = {
            "compliance_history_id": self.compliance_history_id,
            "compliance_activity_id": self.compliance_activity_id,
            "country_id": self.country_id,
            "legal_entity_id": self.legal_entity_id,
            "domain_id": self.domain_id,
            "unit_id": self.unit_id,
            "compliance_id": self.compliance_id,
            "unit_name": self.unit_name,
            "statutory_mapping": self.statutory_mapping,
            "compliance_task": self.compliance_task,
            "frequency_name": self.frequency_name,
            "due_date": self.due_date,
            "task_status": self.task_status,
            "assignee_name": self.assignee_name,
            "activity_status": self.activity_status,
            "activity_date": self.activity_date,
            "document_name": self.document_name,
            "completion_date": self.completion_date,
            "url": self.url,
            "domain_name": self.domain_name,
            "logo_url": self.logo_url
        }
        return data

#
# Service Provider Domains
#

class ServiceProviderDomains(object):
    def __init__(self, user_id, domain_id, domain_name, sp_id_optional):
        self.user_id = user_id
        self.domain_id = domain_id
        self.domain_name = domain_name
        self.sp_id_optional = sp_id_optional

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "user_id", "domain_id", "domain_name", "sp_id_optional"
        ])
        user_id = data.get("user_id")
        domain_id = data.get("domain_id")
        domain_name = data.get("domain_name")
        sp_id_optional = data.get("sp_id_optional")
        return ServiceProviderDomains(user_id, domain_id, domain_name, sp_id_optional)

    def to_structure(self):
        return {
            "user_id": self.user_id,
            "domain_id": self.domain_id,
            "domain_name": self.domain_name,
            "sp_id_optional": self.sp_id_optional
        }

#
# Service Provider Units
#

class ServiceProviderUnits(object):
    def __init__(self, user_id_optional, unit_id, domain_id, unit_code, unit_name, sp_id_optional):
        self.user_id_optional = user_id_optional
        self.unit_id = unit_id
        self.domain_id = domain_id
        self.unit_code = unit_code
        self.unit_name = unit_name
        self.sp_id_optional = sp_id_optional

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "user_id_optional", "unit_id", "domain_id", "unit_code", "unit_name", "sp_id_optional"
        ])
        user_id_optional = data.get("user_id_optional")
        unit_id = data.get("unit_id")
        domain_id = data.get("domain_id")
        unit_code = data.get("unit_code")
        unit_name = data.get("unit_name")
        sp_id_optional = data.get("sp_id_optional")
        return ServiceProviderUnits(user_id_optional, unit_id, domain_id, unit_code, unit_name, sp_id_optional)

    def to_structure(self):
        return {
            "user_id_optional": self.user_id_optional,
            "unit_id": self.unit_id,
            "domain_id": self.domain_id,
            "unit_code": self.unit_code,
            "unit_name": self.unit_name,
            "sp_id_optional": self.sp_id_optional
        }

#
# Legal Entity - Users Acts
#

class ServiceProviderActList(object):
    def __init__(
        self, legal_entity_id, country_id, domain_id, unit_id, compliance_id,
        assignee, sp_ass_id_optional, concurrence_person, sp_cc_id_optional,
        approval_person, sp_app_id_optional, compliance_task, statutory_mapping
    ):
        self.legal_entity_id = legal_entity_id
        self.country_id = country_id
        self.domain_id = domain_id
        self.unit_id = unit_id
        self.compliance_id = compliance_id
        self.assignee = assignee
        self.sp_ass_id_optional = sp_ass_id_optional
        self.concurrence_person = concurrence_person
        self.sp_cc_id_optional = sp_cc_id_optional
        self.approval_person = approval_person
        self.sp_app_id_optional = sp_app_id_optional
        self.compliance_task = compliance_task
        self.statutory_mapping = statutory_mapping

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "legal_entity_id", "country_id", "domain_id", "unit_id", "compliance_id",
            "assignee", "sp_ass_id_optional", "concurrence_person", "sp_cc_id_optional",
            "approval_person", "sp_app_id_optional", "compliance_task", "statutory_mapping"
        ])
        legal_entity_id = data.get("legal_entity_id")
        country_id = data.get("country_id")
        domain_id = data.get("domain_id")
        unit_id = data.get("unit_id")
        compliance_id = data.get("compliance_id")
        assignee = data.get("assignee")
        sp_ass_id_optional = data.get("sp_ass_id_optional")
        concurrence_person = data.get("concurrence_person")
        sp_cc_id_optional = data.get("sp_cc_id_optional")
        approval_person = data.get("approval_person")
        sp_app_id_optional = data.get("sp_app_id_optional")
        compliance_task = data.get("compliance_task")
        statutory_mapping = data.get("statutory_mapping")
        return ServiceProviderActList(
            legal_entity_id, country_id, domain_id, unit_id, compliance_id,
            assignee, sp_ass_id_optional, concurrence_person, sp_cc_id_optional,
            approval_person, sp_app_id_optional, compliance_task, statutory_mapping
        )

    def to_structure(self):
        return {
            "legal_entity_id": self.legal_entity_id,
            "country_id": self.country_id,
            "domain_id": self.domain_id,
            "unit_id": self.unit_id,
            "compliance_id": self.compliance_id,
            "assignee": self.assignee,
            "sp_ass_id_optional": self.sp_ass_id_optional,
            "concurrence_person": self.concurrence_person,
            "sp_cc_id_optional": self.sp_cc_id_optional,
            "approval_person": self.approval_person,
            "sp_app_id_optional": self.sp_app_id_optional,
            "compliance_task": self.compliance_task,
            "statutory_mapping": self.statutory_mapping
        }

#
# Service Providers - Users List
#

class ServiceProvidersUsers(object):
    def __init__(self, domain_id, unit_id, compliance_id, sp_id_optional, user_id, user_name):
        self.domain_id = domain_id
        self.unit_id = unit_id
        self.compliance_id = compliance_id
        self.sp_id_optional = sp_id_optional
        self.user_id = user_id
        self.user_name = user_name

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "domain_id", "unit_id", "compliance_id", "sp_id_optional", "user_id", "user_name"
        ])
        domain_id = data.get("domain_id")
        unit_id = data.get("unit_id")
        compliance_id = data.get("compliance_id")
        sp_id_optional = data.get("sp_id_optional")
        user_id = data.get("user_id")
        user_name = data.get("user_name")
        return ServiceProvidersUsers(domain_id, unit_id, compliance_id, sp_id_optional, user_id, user_name)

    def to_structure(self):
        data = {
            "domain_id": self.domain_id,
            "unit_id": self.unit_id,
            "compliance_id": self.compliance_id,
            "sp_id_optional": self.sp_id_optional,
            "user_id": self.user_id,
            "user_name": self.user_name
        }
        return to_structure_dictionary_values(data)

#
# Users list
#

class LegalEntityUsers(object):
    def __init__(self, user_id, username, user_category_id):
        self.user_id = user_id
        self.username = username
        self.user_category_id = user_category_id

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["user_id", "username", "user_category_id"])
        user_id = data.get("user_id")
        username = data.get("username")
        user_category_id = data.get("user_category_id")
        return UserName(user_id, username, user_category_id)

    def to_structure(self):
        return {
            "user_id": self.user_id,
            "username": self.username,
            "user_category_id": self.user_category_id
        }

#
# Legal Entity - Users Domains
#

class UserDomains(object):
    def __init__(self, user_id, domain_id, domain_name):
        self.user_id = user_id
        self.domain_id = domain_id
        self.domain_name = domain_name

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "user_id", "domain_id", "domain_name"
        ])
        user_id = data.get("user_id")
        domain_id = data.get("domain_id")
        domain_name = data.get("domain_name")
        return UserDomains(user_id, domain_id, domain_name)

    def to_structure(self):
        data = {
            "user_id": self.user_id,
            "domain_id": self.domain_id,
            "domain_name": self.domain_name
        }
        return to_structure_dictionary_values(data)


#
# Legal Entity - Users Units
#

class UserUnits(object):
    def __init__(self, user_id_optional, unit_id, domain_id, unit_code, unit_name):
        self.user_id_optional = user_id_optional
        self.unit_id = unit_id
        self.domain_id = domain_id
        self.unit_code = unit_code
        self.unit_name = unit_name

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "user_id_optional", "unit_id", "domain_id", "unit_code", "unit_name"
        ])
        user_id_optional = data.get("user_id_optional")
        unit_id = data.get("unit_id")
        domain_id = data.get("domain_id")
        unit_code = data.get("unit_code")
        unit_name = data.get("unit_name")
        return UserUnits(user_id_optional, unit_id, domain_id, unit_code, unit_name)

    def to_structure(self):
        return {
            "user_id_optional": self.user_id_optional,
            "unit_id": self.unit_id,
            "domain_id": self.domain_id,
            "unit_code": self.unit_code,
            "unit_name": self.unit_name
        }

#
# Legal Entity - Users Acts
#

class UsersActList(object):
    def __init__(
        self, legal_entity_id, country_id, domain_id, unit_id, compliance_id,
        assignee, concurrence_person, approval_person, compliance_task,
        statutory_mapping
    ):
        self.legal_entity_id = legal_entity_id
        self.country_id = country_id
        self.domain_id = domain_id
        self.unit_id = unit_id
        self.compliance_id = compliance_id
        self.assignee = assignee
        self.concurrence_person = concurrence_person
        self.approval_person = approval_person
        self.compliance_task = compliance_task
        self.statutory_mapping = statutory_mapping

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "legal_entity_id", "country_id", "domain_id", "unit_id", "compliance_id",
            "assignee", "concurrence_person", "approval_person", "compliance_task",
            "statutory_mapping"
        ])
        legal_entity_id = data.get("legal_entity_id")
        country_id = data.get("country_id")
        domain_id = data.get("domain_id")
        unit_id = data.get("unit_id")
        compliance_id = data.get("compliance_id")
        assignee = data.get("assignee")
        concurrence_person = data.get("concurrence_person")
        approval_person = data.get("approval_person")
        compliance_task = data.get("compliance_task")
        statutory_mapping = data.get("statutory_mapping")
        return UsersActList(
            legal_entity_id, country_id, domain_id, unit_id, compliance_id,
            assignee, concurrence_person, approval_person, compliance_task,
            statutory_mapping
        )

    def to_structure(self):
        return {
            "legal_entity_id": self.legal_entity_id,
            "country_id": self.country_id,
            "domain_id": self.domain_id,
            "unit_id": self.unit_id,
            "compliance_id": self.compliance_id,
            "assignee": self.assignee,
            "concurrence_person": self.concurrence_person,
            "approval_person": self.approval_person,
            "compliance_task": self.compliance_task,
            "statutory_mapping": self.statutory_mapping
        }

#
# Unit List - Divisions
#

class Divisions(object):
    def __init__(self, division_id, division_name):
        self.division_id = division_id
        self.division_name = division_name

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["division_id", "division_name"])
        division_id = data.get("division_id")
        division_name = data.get("division_name")
        return Divisions(division_id, division_name)

    def to_structure(self):
        return {
            "division_id": self.division_id,
            "division_name": self.division_name,
        }

#
# Unit List - Categories
#

class Category(object):
    def __init__(self, division_id, category_id, category_name):
        self.division_id = division_id
        self.category_id = category_id
        self.category_name = category_name

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["division_id", "category_id", "category_name"])
        division_id = data.get("division_id")
        category_id = data.get("category_id")
        category_name = data.get("category_name")
        return Category(division_id, category_id, category_name)

    def to_structure(self):
        return {
            "division_id": self.division_id,
            "category_id": self.category_id,
            "category_name": self.category_name
        }

#
# Unit List - Units
#

class UnitList(object):
    def __init__(self, unit_id, unit_code, unit_name, division_id, category_id, d_ids, i_ids):
        self.unit_id = unit_id
        self.unit_code = unit_code
        self.unit_name = unit_name
        self.division_id = division_id
        self.category_id = category_id
        self.d_ids = d_ids
        self.i_ids = i_ids

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "unit_id", "unit_code", "unit_name", "division_id", "category_id", "d_ids", "i_ids"
        ])
        unit_id = data.get("unit_id")
        unit_code = data.get("unit_code")
        unit_name = data.get("unit_name")
        division_id = data.get("division_id")
        category_id = data.get("category_id")
        d_ids = data.get("d_ids")
        i_ids = data.get("i_ids")
        return UnitList(unit_id, unit_code, unit_name, division_id, category_id, d_ids, i_ids)

    def to_structure(self):
        return {
            "unit_id": self.unit_id,
            "unit_code": self.unit_code,
            "unit_name": self.unit_name,
            "division_id": self.division_id,
            "category_id": self.category_id,
            "d_ids": self.d_ids,
            "i_ids": self.i_ids
        }

#
# Unit List - Domains and Organisation
#

class DomainsOrganisation(object):
    def __init__(self, domain_id, domain_name, organisation_id, organisation_name):
        self.domain_id = domain_id
        self.domain_name = domain_name
        self.organisation_id = organisation_id
        self.organisation_name = organisation_name

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "domain_id", "domain_name", "organisation_id", "organisation_name"
        ])
        domain_id = data.get("domain_id")
        domain_name = data.get("domain_name")
        organisation_id = data.get("organisation_id")
        organisation_name = data.get("organisation_name")
        return DomainsOrganisation(
            domain_id, domain_name, organisation_id, organisation_name
        )

    def to_structure(self):
        return {
            "domain_id": self.domain_id,
            "domain_name": self.domain_name,
            "organisation_id": self.organisation_id,
            "organisation_name": self.organisation_name
        }

#
# Unit Status
#

class UnitStatus(object):
    def __init__(self, unit_status_id, unit_status):
        self.unit_status_id = unit_status_id
        self.unit_status = unit_status

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["unit_status_id", "unit_status"])
        unit_status_id = data.get("unit_status_id")
        unit_status = data.get("unit_status")
        return UnitStatus(unit_status_id, unit_status)

    def to_structure(self):
        return {
            "unit_status_id": self.unit_status_id,
            "unit_status": self.unit_status,
        }

class UnitListReport(object):
    def __init__(
        self, unit_id, unit_code, unit_name, geography_name, address, postal_code,
        d_i_names, unit_status, closed_on, division_name, logo_url
    ):
        self.unit_id = unit_id
        self.unit_code = unit_code
        self.unit_name = unit_name
        self.geography_name = geography_name
        self.address = address
        self.postal_code = postal_code
        self.d_i_names = d_i_names
        self.unit_status = unit_status
        self.closed_on = closed_on
        self.division_name = division_name
        self.logo_url = logo_url

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "unit_id", "unit_code", "unit_name", "geography_name", "address", "postal_code",
            "d_i_names", "unit_status", "closed_on", "division_name", "logo_url"
        ])
        unit_id = data.get("unit_id")
        unit_code = data.get("unit_code")
        unit_name = data.get("unit_name")
        geography_name = data.get("geography_name")
        address = data.get("address")
        postal_code = data.get("postal_code")
        d_i_names = data.get("d_i_names")
        unit_status = data.get("unit_status")
        closed_on = data.get("closed_on")
        division_name = data.get("division_name")
        logo_url = data.get("logo_url")
        return UnitListReport(
            unit_id, unit_code, unit_name, geography_name, address, postal_code,
            d_i_names, unit_status, closed_on, division_name, logo_url
        )

    def to_structure(self):
        return {
            "unit_id": self.unit_id,
            "unit_code": self.unit_code,
            "unit_name": self.unit_name,
            "geography_name": self.geography_name,
            "address": self.address,
            "postal_code": self.postal_code,
            "d_i_names": self.d_i_names,
            "unit_status": self.unit_status,
            "closed_on": self.closed_on,
            "division_name": self.division_name,
            "logo_url": self.logo_url
        }

#
# Statutory Notification List
#

class StatutoryNotificationReport(object):
    def __init__(
        self, compliance_id, compliance_task, compliance_description,
        created_on, notification_text, statutory_mapping
    ):
        self.compliance_id = compliance_id
        self.compliance_task = compliance_task
        self.compliance_description = compliance_description
        self.created_on = created_on
        self.notification_text = notification_text
        self.statutory_mapping = statutory_mapping

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "compliance_id", "compliance_task", "compliance_description",
            "created_on", "notification_text", "statutory_mapping"
        ])
        compliance_id = data.get("compliance_id")
        compliance_task = data.get("compliance_task")
        compliance_description = data.get("compliance_description")
        created_on = data.get("created_on")
        notification_text = data.get("notification_text")
        statutory_mapping = data.get("statutory_mapping")

        return StatutoryNotificationReport(
            compliance_id, compliance_task, compliance_description,
            created_on, notification_text, statutory_mapping
        )

    def to_structure(self):
        return {
            "compliance_id": self.compliance_id,
            "compliance_task": self.compliance_task,
            "compliance_description": self.compliance_description,
            "created_on": self.created_on,
            "notification_text": self.notification_text,
            "statutory_mapping": self.statutory_mapping
        }

#
# Audit Trail Forms
#

class AuditTrailActivities(object):
    def __init__(self, user_id, user_name, form_id, action, created_on, logo_url):
        self.user_id = user_id
        self.user_name = user_name
        self.form_id = form_id
        self.action = action
        self.created_on = created_on
        self.logo_url = logo_url

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "user_id", "user_name", "form_id", "action," "created_on", "logo_url"
        ])
        user_id = data.get("user_id")
        user_name = data.get("user_name")
        form_id = data.get("form_id")
        action = data.get("action")
        created_on = data.get("created_on")
        logo_url = data.get("logo_url")
        return AuditTrailActivities(user_id, user_name, form_id, action, created_on, logo_url)

    def to_structure(self):
        return {
            "user_id": self.user_id,
            "user_name": self.user_name,
            "form_id": self.form_id,
            "action": self.action,
            "created_on": self.created_on,
            "logo_url": self.logo_url
        }

#
# UserName
#

class UserName(object):
    def __init__(self, user_id, user_name):
        self.user_id = user_id
        self.user_name = user_name

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["user_id", "user_name"])
        user_id = data.get("user_id")
        user_name = data.get("user_name")
        return UserName(user_id, user_name)

    def to_structure(self):
        return {
            "user_id": self.user_id,
            "user_name": self.user_name,
        }

#
# UserName
#

class RiskReport(object):
    def __init__(
        self, statutory_mapping, unit_name, compliance_task, frequency_name, penal_consequences,
        admin_incharge, assignee_name, task_status, document_name, url, logo_url, start_date, due_date,
        concurrer_name, approver_name, assigned_on, concurred_on, approved_on, comp_remarks
    ):
        self.statutory_mapping = statutory_mapping
        self.unit_name = unit_name
        self.compliance_task = compliance_task
        self.frequency_name = frequency_name
        self.penal_consequences = penal_consequences
        self.admin_incharge = admin_incharge
        self.assignee_name = assignee_name
        self.task_status = task_status
        self.document_name = document_name
        self.url = url
        self.logo_url = logo_url
        self.start_date = start_date
        self.due_date = due_date
        self.concurrer_name = concurrer_name
        self.approver_name = approver_name
        self.assigned_on = assigned_on
        self.concurred_on = concurred_on
        self.approved_on = approved_on
        self.comp_remarks = comp_remarks

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "statutory_mapping", "unit_name", "compliance_task", "frequency_name", "penal_consequences",
            "admin_incharge", "assignee_name", "task_status", "document_name", "url", "logo_url", "start_date",
            "due_date", "concurrer_name", "approver_name", "assigned_on", "concurred_on", "approved_on",
            "comp_remarks"
        ])
        statutory_mapping = data.get("statutory_mapping")
        unit_name = data.get("unit_name")
        compliance_task = data.get("compliance_task")
        frequency_name = data.get("frequency_name")
        penal_consequences = data.get("penal_consequences")
        admin_incharge = data.get("admin_incharge")
        assignee_name = data.get("assignee_name")
        task_status = data.get("task_status")
        document_name = data.get("document_name")
        url = data.get("url")
        logo_url = data.get("logo_url")
        start_date = data.get("start_date")
        due_date = data.get("due_date")
        concurrer_name = data.get("concurrer_name")
        approver_name = data.get("approver_name")
        assigned_on = data.get("assigned_on")
        concurred_on = data.get("concurred_on")
        approved_on = data.get("approved_on")
        comp_remarks = data.get("comp_remarks")
        return RiskReport(
            statutory_mapping, unit_name, compliance_task, frequency_name, penal_consequences,
            admin_incharge, assignee_name, task_status, document_name, url, logo_url, start_date,
            due_date, concurrer_name, approver_name, assigned_on, concurred_on, approved_on,
            comp_remarks
        )

    def to_structure(self):
        return {
            "statutory_mapping": self.statutory_mapping,
            "unit_name": self.unit_name,
            "compliance_task": self.compliance_task,
            "frequency_name": self.frequency_name,
            "penal_consequences": self.penal_consequences,
            "admin_incharge": self.admin_incharge,
            "assignee_name": self.assignee_name,
            "task_status": self.task_status,
            "document_name": self.document_name,
            "url": self.url,
            "logo_url": self.logo_url,
            "start_date": self.start_date,
            "due_date": self.due_date,
            "concurrer_name": self.concurrer_name,
            "approver_name": self.approver_name,
            "assigned_on": self.assigned_on,
            "concurred_on": self.concurred_on,
            "approved_on": self.approved_on,
            "comp_remarks": self.comp_remarks
        }


#
# STATUTORY_WISE_NOTIFICATIONS
#

class STATUTORY_WISE_NOTIFICATIONS(object):
    def __init__(self, business_group_name, legal_entity_name, division_name,  level_1_statutory_wise_notifications):
        self.business_group_name = business_group_name
        self.legal_entity_name = legal_entity_name
        self.division_name = division_name
        self.level_1_statutory_wise_notifications = level_1_statutory_wise_notifications

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["business_group_name", "legal_entity_name", "division_name", "level_1_statutory_wise_notifications"])
        business_group_name = data.get("business_group_name")
        business_group_name = parse_structure_OptionalType_CustomTextType_100(business_group_name)
        legal_entity_name = data.get("legal_entity_name")
        legal_entity_name = parse_structure_OptionalType_CustomTextType_100(legal_entity_name)
        division_name = data.get("division_name")
        division_name = parse_structure_OptionalType_CustomTextType_100(division_name)
        level_1_statutory_wise_notifications = data.get("level_1_statutory_wise_notifications")
        level_1_statutory_wise_notifications = parse_structure_MapType_CustomTextType_500_VectorType_RecordType_clientreport_LEVEL_1_STATUTORY_NOTIFICATIONS(level_1_statutory_wise_notifications)
        return STATUTORY_WISE_NOTIFICATIONS(business_group_name, legal_entity_name, division_name, level_1_statutory_wise_notifications)

    def to_structure(self):
        return {
            "business_group_name": to_structure_OptionalType_CustomTextType_100(self.business_group_name),
            "legal_entity_name": to_structure_OptionalType_CustomTextType_100(self.legal_entity_name),
            "division_name": to_structure_OptionalType_CustomTextType_100(self.division_name),
            "level_1_statutory_wise_notifications": to_structure_MapType_CustomTextType_500_VectorType_RecordType_clientreport_LEVEL_1_STATUTORY_NOTIFICATIONS(self.level_1_statutory_wise_notifications),
        }

#
# LEVEL_1_STATUTORY_NOTIFICATIONS
#

class LEVEL_1_STATUTORY_NOTIFICATIONS(object):
    def __init__(self, statutory_provision, unit_name, notification_text, date_and_time):
        self.statutory_provision = statutory_provision
        self.notification_text = notification_text
        self.unit_name = unit_name
        self.date_and_time = date_and_time

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["statutory_provision", "notification_text", "date_and_time"])
        statutory_provision = data.get("statutory_provision")
        statutory_provision = parse_structure_Text(statutory_provision)
        unit_name = data.get("unit_name")
        unit_name = parse_structure_CustomTextType_250(unit_name)
        notification_text = data.get("notification_text")
        notification_text = parse_structure_OptionalType_Text(notification_text)
        date_and_time = data.get("date_and_time")
        date_and_time = parse_structure_CustomTextType_20(date_and_time)
        return LEVEL_1_STATUTORY_NOTIFICATIONS(statutory_provision, notification_text, date_and_time)

    def to_structure(self):
        return {
            "statutory_provision": to_structure_Text(self.statutory_provision),
            "unit_name": to_structure_CustomTextType_250(self.unit_name),
            "notification_text": to_structure_OptionalType_Text(self.notification_text),
            "date_and_time": to_structure_CustomTextType_20(self.date_and_time)
        }

#
# UserWiseCompliance
#

class UserWiseCompliance(object):
    def __init__(self, assignee, concurrence_person, approval_person, compliances):
        self.assignee = assignee
        self.concurrence_person = concurrence_person
        self.approval_person = approval_person
        self.compliances = compliances

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["assignee", "concurrence_person", "approval_person", "compliances"])
        assignee = data.get("assignee")
        assignee = parse_structure_CustomTextType_100(assignee)
        concurrence_person = data.get("concurrence_person")
        concurrence_person = parse_structure_OptionalType_CustomTextType_100(concurrence_person)
        approval_person = data.get("approval_person")
        approval_person = parse_structure_OptionalType_CustomTextType_100(approval_person)
        compliances = data.get("compliances")
        compliances = parse_structure_VectorType_RecordType_clientreport_ComplianceUnit(compliances)
        return UserWiseCompliance(assignee, concurrence_person, approval_person, compliances)

    def to_structure(self):
        return {
            "assignee": to_structure_CustomTextType_100(self.assignee),
            "concurrence_person": to_structure_OptionalType_CustomTextType_100(self.concurrence_person),
            "approval_person": to_structure_OptionalType_CustomTextType_100(self.approval_person),
            "compliances": to_structure_VectorType_RecordType_clientreport_ComplianceUnit(self.compliances),
        }

class GroupedUnits(object):
    def __init__(self, division_name, legal_entity_name, business_group_name, units):
        self.division_name = division_name
        self.legal_entity_name = legal_entity_name
        self.business_group_name = business_group_name
        self.units = units

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["division_name", "legal_entity_name", "business_group_name", "units"])
        division_name = data.get("division_name")
        division_name = parse_structure_OptionalType_CustomTextType_250(division_name)
        legal_entity_name = data.get("legal_entity_name")
        legal_entity_name = parse_structure_CustomTextType_250(legal_entity_name)
        business_group_name = data.get("business_group_name")
        business_group_name = parse_structure_OptionalType_CustomTextType_250(business_group_name)
        units = data.get("units")
        units = parse_structure_VectorType_RecordType_client_report_UnitDetails(units)
        return GroupedUnits(division_name, legal_entity_name, business_group_name, units)

    def to_structure(self):
        return {
            "division_name": to_structure_OptionalType_CustomTextType_250(self.division_name),
            "legal_entity_name": to_structure_CustomTextType_250(self.legal_entity_name),
            "business_group_name": to_structure_OptionalType_CustomTextType_250(self.business_group_name),
            "units" : to_structure_VectorType_RecordType_client_report_UnitDetails(self.units)
        }


class UnitDetails(object):
    def __init__(self, unit_id, geography_name, unit_code, unit_name, unit_address, postal_code, domain_ids):
        self.unit_id = unit_id
        self.geography_name = geography_name
        self.unit_code = unit_code
        self.unit_name = unit_name
        self.unit_address = unit_address
        self.postal_code = postal_code
        self.domain_ids = domain_ids

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["unit_id", "geography_name", "unit_code", "unit_name", "unit_address", "postal_code", "domain_ids"])
        unit_id = data.get("unit_id")
        unit_id = parse_structure_UnsignedIntegerType_32(unit_id)
        geography_name = data.get("geography_name")
        geography_name = parse_structure_CustomTextType_250(geography_name)
        unit_code = data.get("unit_code")
        unit_code = parse_structure_CustomTextType_20(unit_code)
        unit_name = data.get("unit_name")
        unit_name = parse_structure_CustomTextType_50(unit_name)
        unit_address = data.get("unit_address")
        unit_address = parse_structure_CustomTextType_250(unit_address)
        postal_code = data.get("postal_code")
        postal_code = parse_structure_UnsignedIntegerType_32(postal_code)
        domain_ids = data.get("domain_ids")
        domain_ids = parse_structure_VectorType_SignedIntegerType_8(domain_ids)
        return UnitDetails(unit_id, geography_name, unit_code, unit_name, unit_address, postal_code, domain_ids)

    def to_structure(self):
        return {
            "unit_id": to_structure_UnsignedIntegerType_32(self.unit_id),
            "geography_name": to_structure_CustomTextType_250(self.geography_name),
            "unit_code": to_structure_CustomTextType_20(self.unit_code),
            "unit_name": to_structure_CustomTextType_50(self.unit_name),
            "unit_address": to_structure_CustomTextType_250(self.unit_address),
            "postal_code": to_structure_UnsignedIntegerType_32(self.postal_code),
            "domain_ids": to_structure_VectorType_SignedIntegerType_8(self.domain_ids)
        }
