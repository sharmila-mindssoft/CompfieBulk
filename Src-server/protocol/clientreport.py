import json
from protocol.jsonvalidators import (
    parse_enum, parse_dictionary, parse_static_list, parse_list
)
from protocol.parse_structure import (
    parse_structure_VectorType_RecordType_clientreport_UserWiseCompliance,
    parse_structure_VectorType_RecordType_core_Compliance,
    parse_structure_VectorType_RecordType_clientreport_LoginTrace,
    parse_structure_VectorType_RecordType_clientreport_ReassignHistory,
    parse_structure_VectorType_RecordType_clientreport_ReassignCompliance,
    parse_structure_VectorType_RecordType_clientreport_ReassignUnitCompliance,
    parse_structure_UnsignedIntegerType_32,
    parse_structure_MapType_SignedIntegerType_8_MapType_SignedIntegerType_8_VectorType_RecordType_core_Statutory,
    parse_structure_VectorType_RecordType_clientreport_DomainWiseCompliance,
    parse_structure_VectorType_RecordType_core_BusinessGroup,
    parse_structure_MapType_CustomTextType_50_VectorType_RecordType_clientreport_ActivityCompliance,
    parse_structure_VectorType_RecordType_core_ServiceProvider,
    parse_structure_CustomTextType_500,
    parse_structure_VectorType_RecordType_clientreport_UserName,
    parse_structure_VectorType_RecordType_clientreport_User,
    parse_structure_MapType_SignedIntegerType_8_VectorType_MapType_SignedIntegerType_8_VectorType_RecordType_core_Statutory,
    parse_structure_VectorType_RecordType_core_Country,
    parse_structure_VectorType_RecordType_clientreport_StatutoryReassignCompliance,
    parse_structure_VectorType_RecordType_clientreport_ComplianceUnit,
    parse_structure_VectorType_RecordType_clientreport_FormName,
    parse_structure_MapType_CustomTextType_50_VectorType_RecordType_clientreport_ApplicabilityCompliance,
    parse_structure_OptionalType_SignedIntegerType_8,
    parse_structure_CustomTextType_50,
    parse_structure_EnumType_core_COMPLIANCE_STATUS,
    parse_structure_CustomTextType_100,
    parse_structure_EnumType_core_USER_TYPE,
    parse_structure_VectorType_RecordType_clientreport_ActivityLog,
    parse_structure_VectorType_RecordType_core_Unit,
    parse_structure_VectorType_RecordType_clientreport_UnitWiseCompliance,
    parse_structure_VectorType_RecordType_clientreport_ComplianceForUnit,
    parse_structure_VectorType_CustomTextType_50,
    parse_structure_MapType_CustomTextType_50_VectorType_RecordType_clientreport_ComplianceUnit,
    parse_structure_VectorType_RecordType_core_Division,
    parse_structure_VectorType_RecordType_clientreport_UnitCompliance,
    parse_structure_OptionalType_CustomTextType_20,
    parse_structure_VectorType_RecordType_clientreport_ServiceProviderCompliance,
    parse_structure_VectorType_RecordType_clientreport_UnitName,
    parse_structure_EnumType_core_COMPLIANCE_ACTIVITY_STATUS,
    parse_structure_VectorType_VectorType_RecordType_core_StatutoryDate,
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
    parse_structure_OptionalType_VectorType_CustomTextType_50,
    parse_structure_VectorType_RecordType_core_ClientLevelOneStatutory,
    parse_structure_VectorType_RecordType_core_ComplianceFilter,
    parse_structure_OptionalType_EnumType_core_COMPLIANCE_STATUS,
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
    parse_structure_VectorType_Text
)
from protocol.to_structure import (
    to_structure_VectorType_RecordType_clientreport_UserWiseCompliance,
    to_structure_VectorType_RecordType_core_Compliance,
    to_structure_VectorType_RecordType_clientreport_LoginTrace,
    to_structure_VectorType_RecordType_clientreport_ReassignHistory,
    to_structure_VectorType_RecordType_clientreport_ReassignCompliance,
    to_structure_VectorType_RecordType_clientreport_ReassignUnitCompliance,
    to_structure_SignedIntegerType_8,
    to_structure_MapType_SignedIntegerType_8_MapType_SignedIntegerType_8_VectorType_RecordType_core_Statutory,
    to_structure_VectorType_RecordType_clientreport_DomainWiseCompliance,
    to_structure_VectorType_RecordType_core_BusinessGroup,
    to_structure_MapType_CustomTextType_50_VectorType_RecordType_clientreport_ActivityCompliance,
    to_structure_VectorType_RecordType_core_ServiceProvider,
    to_structure_CustomTextType_500,
    to_structure_VectorType_RecordType_clientreport_UserName,
    to_structure_VectorType_RecordType_clientreport_User,
    to_structure_MapType_SignedIntegerType_8_VectorType_MapType_SignedIntegerType_8_VectorType_RecordType_core_Statutory,
    to_structure_VectorType_RecordType_core_Country,
    to_structure_VectorType_RecordType_clientreport_StatutoryReassignCompliance,
    to_structure_VectorType_RecordType_clientreport_ComplianceUnit,
    to_structure_VectorType_RecordType_clientreport_FormName,
    to_structure_MapType_CustomTextType_50_VectorType_RecordType_clientreport_ApplicabilityCompliance,
    to_structure_OptionalType_SignedIntegerType_8,
    to_structure_CustomTextType_50,
    to_structure_EnumType_core_COMPLIANCE_STATUS,
    to_structure_CustomTextType_100, to_structure_EnumType_core_USER_TYPE,
    to_structure_VectorType_RecordType_clientreport_ActivityLog,
    to_structure_VectorType_RecordType_core_Unit,
    to_structure_VectorType_RecordType_clientreport_UnitWiseCompliance,
    to_structure_VectorType_RecordType_clientreport_ComplianceForUnit,
    to_structure_VectorType_CustomTextType_50,
    to_structure_MapType_CustomTextType_50_VectorType_RecordType_clientreport_ComplianceUnit,
    to_structure_VectorType_RecordType_core_Division,
    to_structure_VectorType_RecordType_clientreport_UnitCompliance,
    to_structure_OptionalType_CustomTextType_20,
    to_structure_VectorType_RecordType_clientreport_ServiceProviderCompliance,
    to_structure_VectorType_RecordType_clientreport_UnitName,
    to_structure_EnumType_core_COMPLIANCE_ACTIVITY_STATUS,
    to_structure_VectorType_VectorType_RecordType_core_StatutoryDate,
    to_structure_CustomTextType_250,
    to_structure_VectorType_RecordType_clientreport_ComplianceDetails,
    to_structure_VectorType_RecordType_core_LegalEntity,
    to_structure_VectorType_RecordType_core_Domain,
    to_structure_MapType_CustomTextType_50_VectorType_RecordType_clientreport_Level1Statutory,
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
    to_structure_OptionalType_VectorType_CustomTextType_50,
    to_structure_VectorType_RecordType_core_ClientLevelOneStatutory,
    to_structure_VectorType_RecordType_core_ComplianceFilter,
    to_structure_OptionalType_EnumType_core_COMPLIANCE_STATUS,
    to_structure_VectorType_RecordType_clientreport_RiskData,
    to_structure_VectorType_RecordType_clientreport_Level1Compliance,
    to_structure_RecordType_clientreport_STATUTORY_WISE_NOTIFICATIONS,
    to_structure_VectorType_RecordType_clientreport_STATUTORY_WISE_NOTIFICATIONS,
    to_structure_VectorType_RecordType_clientreports_LEVEL_1_STATUTORY_NOTIFICATIONS,
    to_structure_MapType_CustomTextType_50_VectorType_RecordType_clientreport_LEVEL_1_STATUTORY_NOTIFICATIONS,
    to_structure_VectorType_CustomTextType_100,
    to_structure_VectorType_RecordType_clientreport_ActivityData,
    to_structure_MapType_CustomTextType_50_MapType_CustomTextType_50_VectorType_RecordType_clientreport_ActivityData,
    to_structure_OptionalType_VectorType_SignedIntegerType_8,
    to_structure_VectorType_RecordType_client_report_GroupedUnits,
    to_structure_VectorType_RecordType_client_report_UnitDetails,
    to_structure_OptionalType_UnsignedIntegerType_32,
    to_structure_UnsignedIntegerType_32,
    to_structure_VectorType_SignedIntegerType_8,
    to_structure_VectorType_CustomTextType_500,
    to_structure_OptionalType_CustomTextType_500,
    to_structure_Text,
    to_structure_VectorType_Text
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
    def __init__(self, country_id, domain_id, statutory_id, unit_id, compliance_id, assignee_id, from_date, to_date, compliance_status):
        self.country_id = country_id
        self.domain_id = domain_id
        self.statutory_id = statutory_id
        self.unit_id = unit_id
        self.compliance_id = compliance_id
        self.assignee_id = assignee_id
        self.from_date = from_date
        self.to_date = to_date
        self.compliance_status = compliance_status

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["country_id", "domain_id", "statutory_id", "unit_id", "compliance_id", "assignee_id", "from_date", "to_date", "compliance_status"])
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
        compliance_status = parse_structure_OptionalType_EnumType_core_COMPLIANCE_STATUS(compliance_status)
        return GetComplianceDetailsReport(country_id, domain_id, statutory_id, unit_id, compliance_id, assignee_id, from_date, to_date, compliance_status)

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
            "compliance_status": to_structure_OptionalType_EnumType_core_COMPLIANCE_STATUS(self.compliance_status),
        }

class GetRiskReportFilters(Request):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return GetRiskReportFilters()

    def to_inner_structure(self):
        return {
        }

class GetRiskReport(Request):
    def __init__(self, country_id, domain_id, business_group_id, legal_entity_id, division_id, unit_id, level_1_statutory_name, statutory_status):
        self.country_id = country_id
        self.domain_id = domain_id
        self.business_group_id = business_group_id
        self.legal_entity_id = legal_entity_id
        self.division_id = division_id
        self.unit_id = unit_id
        self.level_1_statutory_name = level_1_statutory_name
        self.statutory_status = statutory_status

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["country_id", "domain_id", "business_group_id", "legal_entity_id", "division_id", "unit_id", "level_1_statutory_name", "statutory_status"])
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
        level_1_statutory_name = data.get("level_1_statutory_name")
        level_1_statutory_name = parse_structure_OptionalType_CustomTextType_100(level_1_statutory_name)
        statutory_status = data.get("statutory_status")
        statutory_status = parse_structure_OptionalType_UnsignedIntegerType_32(statutory_status)
        return GetRiskReport(country_id, domain_id, business_group_id, legal_entity_id, division_id, unit_id, level_1_statutory_name, statutory_status)

    def to_inner_structure(self):
        return {
            "country_id": to_structure_SignedIntegerType_8(self.country_id),
            "domain_id": to_structure_SignedIntegerType_8(self.domain_id),
            "business_group_id": to_structure_OptionalType_SignedIntegerType_8(self.business_group_id),
            "legal_entity_id": to_structure_OptionalType_SignedIntegerType_8(self.legal_entity_id),
            "division_id": to_structure_OptionalType_SignedIntegerType_8(self.division_id),
            "unit_id": to_structure_OptionalType_SignedIntegerType_8(self.unit_id),
            "level_1_statutory_name": to_structure_OptionalType_CustomTextType_100(self.level_1_statutory_name),
            "statutory_status": to_structure_OptionalType_SignedIntegerType_8(self.statutory_status),
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
    def __init__(self, country_id, domain_id, statutory_id, unit_id, service_provider_id):
        self.country_id = country_id
        self.domain_id = domain_id
        self.statutory_id = statutory_id
        self.unit_id = unit_id
        self.service_provider_id = service_provider_id

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["country_id", "domain_id", "statutory_id", "unit_id", "service_provider_id"])
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
        return GetServiceProviderWiseCompliance(country_id, domain_id, statutory_id, unit_id, service_provider_id)

    def to_inner_structure(self):
        return {
            "country_id": to_structure_SignedIntegerType_8(self.country_id),
            "domain_id": to_structure_SignedIntegerType_8(self.domain_id),
            "statutory_id": to_structure_OptionalType_CustomTextType_100(self.statutory_id),
            "unit_id": to_structure_OptionalType_SignedIntegerType_8(self.unit_id),
            "service_provider_id": to_structure_OptionalType_SignedIntegerType_8(self.service_provider_id),
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
    def __init__(self, country_id, domain_id, business_group_id, legal_entity_id, division_id, unit_id, user_id):
        self.country_id = country_id
        self.domain_id = domain_id
        self.business_group_id = business_group_id
        self.legal_entity_id = legal_entity_id
        self.division_id = division_id
        self.unit_id = unit_id
        self.user_id = user_id

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["country_id", "domain_id", "business_group_id", "legal_entity_id", "division_id", "unit_id", "user_id"])
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
        return GetAssigneewisecomplianceReport(country_id, domain_id, business_group_id, legal_entity_id, division_id, unit_id, user_id)

    def to_inner_structure(self):
        return {
            "country_id": to_structure_SignedIntegerType_8(self.country_id),
            "domain_id": to_structure_SignedIntegerType_8(self.domain_id),
            "business_group_id": to_structure_OptionalType_SignedIntegerType_8(self.business_group_id),
            "legal_entity_id": to_structure_OptionalType_SignedIntegerType_8(self.legal_entity_id),
            "division_id": to_structure_OptionalType_SignedIntegerType_8(self.division_id),
            "unit_id": to_structure_OptionalType_SignedIntegerType_8(self.unit_id),
            "user_id": to_structure_OptionalType_SignedIntegerType_8(self.user_id),
        }


class GetUnitwisecomplianceReport(Request):
    def __init__(self, country_id, domain_id, business_group_id, legal_entity_id, division_id, unit_id, user_id):
        self.country_id = country_id
        self.domain_id = domain_id
        self.business_group_id = business_group_id
        self.legal_entity_id = legal_entity_id
        self.division_id = division_id
        self.unit_id = unit_id
        self.user_id = user_id

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["country_id", "domain_id", "business_group_id", "legal_entity_id", "division_id", "unit_id", "user_id"])
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
        return GetUnitwisecomplianceReport(country_id, domain_id, business_group_id, legal_entity_id, division_id, unit_id, user_id)

    def to_inner_structure(self):
        return {
            "country_id": to_structure_SignedIntegerType_8(self.country_id),
            "domain_id": to_structure_SignedIntegerType_8(self.domain_id),
            "business_group_id": to_structure_OptionalType_SignedIntegerType_8(self.business_group_id),
            "legal_entity_id": to_structure_OptionalType_SignedIntegerType_8(self.legal_entity_id),
            "division_id": to_structure_OptionalType_SignedIntegerType_8(self.division_id),
            "unit_id": to_structure_OptionalType_SignedIntegerType_8(self.unit_id),
            "user_id": to_structure_OptionalType_SignedIntegerType_8(self.user_id),
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
    def __init__(self, country_id, business_group_id, legal_entity_id, division_id, unit_id, domain_ids):
        self.country_id = country_id
        self.business_group_id = business_group_id
        self.legal_entity_id = legal_entity_id
        self.division_id = division_id
        self.unit_id = unit_id
        self.domain_ids = domain_ids

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["country_id", "business_group_id", "legal_entity_id", "division_id", "unit_id", "domain_ids"])
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
        return GetClientDetailsReportData(country_id, business_group_id, legal_entity_id, division_id, unit_id, domain_ids)

    def to_inner_structure(self):
        return {
            "country_id": to_structure_SignedIntegerType_8(self.country_id),
            "business_group_id": to_structure_OptionalType_SignedIntegerType_8(self.business_group_id),
            "legal_entity_id": to_structure_OptionalType_SignedIntegerType_8(self.legal_entity_id),
            "division_id": to_structure_OptionalType_SignedIntegerType_8(self.division_id),
            "unit_id": to_structure_OptionalType_SignedIntegerType_8(self.unit_id),
            "domain_ids": to_structure_OptionalType_VectorType_SignedIntegerType_8(self.domain_ids),
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
    def __init__(self, country_id, domain_id, business_group_id, legal_entity_id, division_id, unit_id, statutory_name, applicable_status):
        self.country_id = country_id
        self.domain_id = domain_id
        self.business_group_id = business_group_id
        self.legal_entity_id = legal_entity_id
        self.division_id = division_id
        self.unit_id = unit_id
        self.statutory_name = statutory_name
        self.applicable_status = applicable_status

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["country_id", "domain_id", "business_group_id", "legal_entity_id", "division_id", "unit_id", "statutory_name", "applicable_status"])
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
        statutory_name = parse_structure_OptionalType_SignedIntegerType_8(statutory_name)
        applicable_status = data.get("applicable_status")
        applicable_status = parse_structure_OptionalType_EnumType_core_APPLICABILITY_STATUS(applicable_status)
        return GetComplianceTaskApplicabilityStatusReport(country_id, domain_id, business_group_id, legal_entity_id, division_id, unit_id, statutory_name, applicable_status)

    def to_inner_structure(self):
        return {
            "country_id": to_structure_SignedIntegerType_8(self.country_id),
            "domain_id": to_structure_SignedIntegerType_8(self.domain_id),
            "business_group_id": to_structure_OptionalType_SignedIntegerType_8(self.business_group_id),
            "legal_entity_id": to_structure_OptionalType_SignedIntegerType_8(self.legal_entity_id),
            "division_id": to_structure_OptionalType_SignedIntegerType_8(self.division_id),
            "unit_id": to_structure_OptionalType_SignedIntegerType_8(self.unit_id),
            "statutory_name": to_structure_OptionalType_SignedIntegerType_8(self.statutory_name),
            "applicable_status": to_structure_OptionalType_EnumType_core_APPLICABILITY_STATUS(self.applicable_status),
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
    def __init__(self, user_type, user_id, domain_id, country_id, level_1_statutory_name, unit_id,
        compliance_id, from_date, to_date):
        self.user_type = user_type
        self.user_id = user_id
        self.domain_id = domain_id
        self.country_id = country_id
        self.level_1_statutory_name = level_1_statutory_name
        self.unit_id = unit_id
        self.compliance_id = compliance_id
        self.from_date = from_date
        self.to_date = to_date

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(
            data, [
                "user_type", "user_id", "domain_id", "country_id",
                "level_1_statutory_name", "unit_id", "compliance_id", "from_date", "to_date"
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
        return GetComplianceActivityReport(
            user_type, user_id, domain_id, country_id, level_1_statutory_name, unit_id, compliance_id,
            from_date, to_date
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
        }

class GetReassignedHistoryReportFilters(Request):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return GetReassignedHistoryReportFilters()

    def to_inner_structure(self):
        return {
        }

class GetReassignedHistoryReport(Request):
    def __init__(self, country_id, domain_id, unit_id, level_1_statutory_id, compliance_id, user_id, from_date, to_date):
        self.country_id = country_id
        self.domain_id = domain_id
        self.unit_id = unit_id
        self.level_1_statutory_id = level_1_statutory_id
        self.compliance_id = compliance_id
        self.user_id = user_id
        self.from_date = from_date
        self.to_date = to_date

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["country_id", "domain_id", "unit_id", "level_1_statutory_id", "compliance_id", "user_id", "from_date", "to_date"])
        country_id = data.get("country_id")
        country_id = parse_structure_UnsignedIntegerType_32(country_id)
        domain_id = data.get("domain_id")
        domain_id = parse_structure_UnsignedIntegerType_32(domain_id)
        unit_id = data.get("unit_id")
        unit_id = parse_structure_OptionalType_SignedIntegerType_8(unit_id)
        level_1_statutory_id = data.get("level_1_statutory_id")
        level_1_statutory_id = parse_structure_OptionalType_CustomTextType_100(level_1_statutory_id)
        compliance_id = data.get("compliance_id")
        compliance_id = parse_structure_OptionalType_SignedIntegerType_8(compliance_id)
        user_id = data.get("user_id")
        user_id = parse_structure_OptionalType_SignedIntegerType_8(user_id)
        from_date = data.get("from_date")
        from_date = parse_structure_OptionalType_CustomTextType_20(from_date)
        to_date = data.get("to_date")
        to_date = parse_structure_OptionalType_CustomTextType_20(to_date)
        return GetReassignedHistoryReport(country_id, domain_id, unit_id, level_1_statutory_id, compliance_id, user_id, from_date, to_date)

    def to_inner_structure(self):
        return {
            "country_id": to_structure_SignedIntegerType_8(self.country_id),
            "domain_id": to_structure_SignedIntegerType_8(self.domain_id),
            "unit_id": to_structure_OptionalType_SignedIntegerType_8(self.unit_id),
            "level_1_statutory_id": to_structure_OptionalType_CustomTextType_100(self.level_1_statutory_id),
            "compliance_id": to_structure_OptionalType_SignedIntegerType_8(self.compliance_id),
            "user_id": to_structure_OptionalType_SignedIntegerType_8(self.user_id),
            "from_date": to_structure_OptionalType_CustomTextType_20(self.from_date),
            "to_date": to_structure_OptionalType_CustomTextType_20(self.to_date),
        }

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
    def __init__(self, country_name, domain_name,  business_group_id, legal_entity_id, division_id,
     unit_id, level_1_statutory_name, from_date, to_date):
        self.country_name = country_name
        self.domain_name = domain_name
        self.business_group_id = business_group_id
        self.legal_entity_id = legal_entity_id
        self.division_id = division_id
        self.unit_id = unit_id
        self.level_1_statutory_name = level_1_statutory_name
        self.from_date = from_date
        self.to_date = to_date

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["country_name", "domain_name", "business_group_id", "legal_entity_id",
            "division_id", "unit_id", "level_1_statutory_name", "from_date", "to_date"])
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

        return GetStatutoryNotificationsListReport(country_name, domain_name, business_group_id, legal_entity_id, division_id, unit_id, level_1_statutory_name, from_date, to_date)

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
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return GetLoginTrace()

    def to_inner_structure(self):
        return {
        }

class ExportToCSV(Request):
    def __init__(self, json_data):
        self.json_data = json_data

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["data"])
        json_data = data.get("data")
        json_data = parse_dictionary(json_data)
        return ExportToCSV(json_data)

    def to_inner_structure(self):
        return {
            "data": to_list(self.json_data)
        }

def _init_Request_class_map():
    classes = [GetComplianceDetailsReportFilters, GetComplianceDetailsReport,
    GetRiskReportFilters, GetRiskReport, GetServiceProviderReportFilters,
    GetServiceProviderWiseCompliance, GetClientReportFilters,
    GetAssigneewisecomplianceReport, GetUnitwisecomplianceReport,
    GetReassignComplianceTaskReportFilters, GetReassignComplianceTaskDetails,
    GetTaskApplicabilityStatusFilters, GetComplianceTaskApplicabilityStatusReport,
    GetComplianceActivityReportFilters, GetComplianceActivityReport,
    GetReassignedHistoryReportFilters, GetReassignedHistoryReport,
    GetStatutoryNotificationsListFilters, GetStatutoryNotificationsListReport,
    GetClientDetailsReportFilters, GetClientDetailsReportData, GetActivityLogFilters,
    GetActivityLogReport, GetLoginTrace, ExportToCSV]
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

class ComplianceDetailsUnitWise(object):
    def __init__(self, unit_id, unit_name, address, Compliances):
        self.unit_id = unit_id
        self.unit_name = unit_name
        self.address = address
        self.Compliances = Compliances

    @staticmethod
    def parse_structure(data):
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

    def to_structure(self):
        result = {
            "unit_id": to_structure_SignedIntegerType_8(self.unit_id),
            "unit_name": to_structure_CustomTextType_100(self.unit_name),
            "address": to_structure_CustomTextType_250(self.address),
            "compliances": to_structure_VectorType_RecordType_clientreport_ComplianceDetails(self.Compliances),
        }

        return result

class GetComplianceDetailsReportSuccess(Response):
    def __init__(self, unit_wise_compliancess):
        self.unit_wise_compliancess = unit_wise_compliancess

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["unit_wise_compliancess"])
        unit_wise_compliances = data.get("unit_wise_compliances")
        unit_wise_compliances = parse_structure_VectorType_RecordType_clientreport_ComplianceDetailsUnitWise(unit_wise_compliancess)
        return GetComplianceDetailsReportSuccess(unit_wise_compliancess)

    def to_inner_structure(self):

        return {
            "unit_wise_compliancess": to_structure_VectorType_RecordType_clientreport_ComplianceDetailsUnitWise(self.unit_wise_compliancess)
        }

class GetRiskReportFiltersSuccess(Response):
    def __init__(self, countries, domains, business_groups, legal_entities, divisions, units, level1_statutories):
        self.countries = countries
        self.domains = domains
        self.business_groups = business_groups
        self.legal_entities = legal_entities
        self.divisions = divisions
        self.units = units
        self.level1_statutories = level1_statutories

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["countries", "domains", "business_groups", "legal_entities", "divisions", "units", "level1_statutories"])
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
        level1_statutories = data.get("level1_statutories")
        level1_statutories = parse_structure_VectorType_CustomTextType_100(level1_statutories)
        return GetRiskReportFiltersSuccess(countries, domains, business_groups, legal_entities, divisions, units, level1_statutories)

    def to_inner_structure(self):
        return {
            "countries": to_structure_VectorType_RecordType_core_Country(self.countries),
            "domains": to_structure_VectorType_RecordType_core_Domain(self.domains),
            "business_groups": to_structure_VectorType_RecordType_core_ClientBusinessGroup(self.business_groups),
            "legal_entities": to_structure_VectorType_RecordType_core_ClientLegalEntity(self.legal_entities),
            "divisions": to_structure_VectorType_RecordType_core_ClientDivision(self.divisions),
            "units": to_structure_VectorType_RecordType_core_ClientUnit(self.units),
            "level1_statutories": to_structure_VectorType_CustomTextType_100(self.level1_statutories),
        }

class GetRiskReportSuccess(Response):
    def __init__(self, delayed_compliance, not_complied, not_opted, unassigned_compliance):
        self.delayed_compliance = delayed_compliance
        self.not_complied = not_complied
        self.not_opted = not_opted
        self.unassigned_compliance = unassigned_compliance

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["delayed_compliance", "not_complied", "not_opted", "unassigned_compliance"])
        delayed_compliance = data.get("delayed_compliance")
        delayed_compliance = parse_structure_VectorType_RecordType_clientreport_RiskData(delayed_compliance)
        not_complied = data.get("not_complied")
        not_complied = parse_structure_VectorType_RecordType_clientreport_RiskData(not_complied)
        not_opted = data.get("not_opted")
        not_opted = parse_structure_VectorType_RecordType_clientreport_RiskData(not_opted)
        unassigned_compliance = data.get("unassigned_compliance")
        unassigned_compliance = parse_structure_VectorType_RecordType_clientreport_RiskData(unassigned_compliance)
        return GetRiskReportSuccess(delayed_compliance, not_complied, not_opted, unassigned_compliance)

    def to_inner_structure(self):
        return {
            "delayed_compliance": to_structure_VectorType_RecordType_clientreport_RiskData(self.delayed_compliance),
            "not_complied": to_structure_VectorType_RecordType_clientreport_RiskData(self.not_complied),
            "not_opted": to_structure_VectorType_RecordType_clientreport_RiskData(self.not_opted),
            "unassigned_compliance" : to_structure_VectorType_RecordType_clientreport_RiskData(self.unassigned_compliance)
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
    def __init__(self, compliance_list):
        self.compliance_list = compliance_list

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["compliance_list"])
        compliance_list = data.get("compliance_list")
        compliance_list = parse_structure_VectorType_RecordType_clientreport_ServiceProviderCompliance(compliance_list)
        return GetServiceProviderWiseComplianceSuccess(compliance_list)

    def to_inner_structure(self):
        return {
            "compliance_list": to_structure_VectorType_RecordType_clientreport_ServiceProviderCompliance(self.compliance_list),
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
    def __init__(self, compliance_list):
        self.compliance_list = compliance_list

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["compliance_list"])
        compliance_list = data.get("compliance_list")
        compliance_list = parse_structure_VectorType_RecordType_clientreport_AssigneeCompliance(compliance_list)
        return GetAssigneewisecomplianceReportSuccess(compliance_list)

    def to_inner_structure(self):
        return {
            "compliance_list": to_structure_VectorType_RecordType_clientreport_AssigneeCompliance(self.compliance_list),
        }

class GetUnitwisecomplianceReportSuccess(Response):
    def __init__(self, compliance_list):
        self.compliance_list = compliance_list

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["compliance_list"])
        compliance_list = data.get("compliance_list")
        compliance_list = parse_structure_VectorType_RecordType_clientreport_UnitCompliance(compliance_list)
        return GetUnitwisecomplianceReportSuccess(compliance_list)

    def to_inner_structure(self):
        return {
            "compliance_list": to_structure_VectorType_RecordType_clientreport_UnitCompliance(self.compliance_list),
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

class GetComplianceTaskApplicabilityStatusReportSuccess(Response):
    def __init__(self, applicable, not_applicable, not_opted):
        self.applicable = applicable
        self.not_applicable = not_applicable
        self.not_opted = not_opted

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["applicable", "not_applicable", "not_opted"])
        applicable = data.get("applicable")
        applicable = parse_structure_MapType_CustomTextType_50_VectorType_RecordType_clientreport_ApplicabilityCompliance(applicable)
        not_applicable = data.get("not_applicable")
        not_applicable = parse_structure_MapType_CustomTextType_50_VectorType_RecordType_clientreport_ApplicabilityCompliance(not_applicable)
        not_opted = data.get("not_opted")
        not_opted = parse_structure_MapType_CustomTextType_50_VectorType_RecordType_clientreport_ApplicabilityCompliance(not_opted)
        return GetComplianceTaskApplicabilityStatusReportSuccess(applicable, not_applicable, not_opted)

    def to_inner_structure(self):
        return {
            "applicable": to_structure_MapType_CustomTextType_50_VectorType_RecordType_clientreport_ApplicabilityCompliance(self.applicable),
            "not_applicable": to_structure_MapType_CustomTextType_50_VectorType_RecordType_clientreport_ApplicabilityCompliance(self.not_applicable),
            "not_opted": to_structure_MapType_CustomTextType_50_VectorType_RecordType_clientreport_ApplicabilityCompliance(self.not_opted),
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
        users = parse_structure_VectorType_RecordType_clientreport_User(users)
        countries = data.get("countries")
        countries = parse_structure_VectorType_RecordType_core_Domain(countries)
        domains = data.get("domains")
        domains = parse_structure_VectorType_RecordType_core_Domain(domains)
        level_1_statutories = data.get("level_1_statutories")
        level_1_statutories = parse_structure_VectorType_CustomTextType_100(level_1_statutories)
        units = data.get("units")
        units = parse_structure_VectorType_RecordType_core_ClientUnit(units)
        compliances = data.get("compliances")
        compliances = parse_structure_VectorType_RecordType_core_ComplianceFilter(compliances)
        return GetComplianceActivityReportFiltersSuccess(
            users, countries, domains, level_1_statutories,
            units, compliances
        )

    def to_inner_structure(self):
        return {
            "users": to_structure_VectorType_RecordType_clientreport_User(self.users),
            "countries": to_structure_VectorType_RecordType_core_Country(self.countries),
            "domains": to_structure_VectorType_RecordType_core_Domain(self.domains),
            "level_1_statutories": to_structure_VectorType_CustomTextType_100(self.level_1_statutories),
            "units": to_structure_VectorType_RecordType_core_ClientUnit(self.units),
            "compliances": to_structure_VectorType_RecordType_core_ComplianceFilter(self.compliances)
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

class GetReassignedHistoryReportFiltersSuccess(Response):
    def __init__(self, countries, domains, units, level_1_statutories, compliances, users):
        self.countries = countries
        self.domains = domains
        self.units = units
        self.level_1_statutories = level_1_statutories
        self.compliances = compliances
        self.users = users

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["countries", "domains", "units", "level_1_statutories", "compliances", "users"])
        countries = data.get("countries")
        countries = parse_structure_VectorType_RecordType_core_Country(countries)
        domains = data.get("domains")
        domains = parse_structure_VectorType_RecordType_core_Domain(domains)
        units = data.get("units")
        units = parse_structure_VectorType_RecordType_core_ClientUnit(units)
        level_1_statutories = data.get("level_1_statutories")
        level_1_statutories = parse_structure_VectorType_CustomTextType_100(level_1_statutories)
        compliances = data.get("compliances")
        compliances = parse_structure_VectorType_RecordType_core_ComplianceFilter(compliances)
        users = data.get("users")
        users = parse_structure_VectorType_RecordType_clientreport_User(users)

        return GetReassignedHistoryReportFiltersSuccess(countries, domains, units, level_1_statutories, compliances, users)

    def to_inner_structure(self):
        return {
            "countries": to_structure_VectorType_RecordType_core_Country(self.countries),
            "domains": to_structure_VectorType_RecordType_core_Domain(self.domains),
            "units": to_structure_VectorType_RecordType_core_ClientUnit(self.units),
            "level_1_statutories": to_structure_VectorType_CustomTextType_100(self.level_1_statutories),
            "compliances": to_structure_VectorType_RecordType_core_ComplianceFilter(self.compliances),
            "users": to_structure_VectorType_RecordType_clientreport_User(self.users),
        }

class GetReassignedHistoryReportSuccess(Response):
    def __init__(self, statutory_wise_compliances):
        self.statutory_wise_compliances = statutory_wise_compliances

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["statutory_wise_compliances"])
        statutory_wise_compliances = data.get("statutory_wise_compliances")
        statutory_wise_compliances = parse_structure_VectorType_RecordType_clientreport_StatutoryReassignCompliance(statutory_wise_compliances)
        return GetReassignedHistoryReportSuccess(statutory_wise_compliances)

    def to_inner_structure(self):
        return {
            "statutory_wise_compliances": to_structure_VectorType_RecordType_clientreport_StatutoryReassignCompliance(self.statutory_wise_compliances),
        }


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
        return GetStatutoryNotificationsListFiltersSuccess(statutory_wise_notifications)

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
    def __init__(self, units):
        self.units = units

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["units"])
        units = data.get("units")
        units = parse_structure_VectorType_RecordType_core_UnitDetails(units)
        return GetClientDetailsReportDataSuccess(units)

    def to_inner_structure(self):
        return {
            "units": to_structure_VectorType_RecordType_client_report_GroupedUnits(self.units)
        }

class ExportToCSVSuccess(Response):
    def __init__(self, link):
        self.link = link

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["link"])
        link = data.get("link")
        link = parse_structure_CustomTextType_500(link)
        return ExportToCSVSuccess(link)

    def to_inner_structure(self):
        return {
            "link" : to_structure_CustomTextType_500(self.link)
        }

class GetClientDetailsReportFiltersSuccess(Response):
    def __init__(self, countries, domains, business_groups,
        legal_entities, divisions, units):
        self.countries = countries
        self.domains = domains
        self.business_groups = business_groups
        self.legal_entities = legal_entities
        self.divisions = divisions
        self.units = units

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["countries", "domains",
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
        return GetClientDetailsReportFiltersSuccess(countries, domains,
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


def _init_Response_class_map():
    classes = [GetComplianceDetailsReportFiltersSuccess,
    GetComplianceDetailsReportSuccess, GetRiskReportFiltersSuccess,
    GetRiskReportSuccess, GetServiceProviderReportFiltersSuccess,
    GetServiceProviderWiseComplianceSuccess, GetClientReportFiltersSuccess,
    GetAssigneewisecomplianceReportSuccess, GetUnitwisecomplianceReportSuccess,
    GetReassignComplianceTaskReportFiltersSuccess,
    GetReassignComplianceTaskDetailsSuccess,
    GetTaskApplicabilityStatusFiltersSuccess,
    GetComplianceTaskApplicabilityStatusReportSuccess,
    GetComplianceActivityReportFiltersSuccess, GetComplianceActivityReportSuccess,
    GetReassignedHistoryReportFiltersSuccess, GetReassignedHistoryReportSuccess,
    GetStatutoryNotificationsListFiltersSuccess,
    GetStatutoryNotificationsListReportSuccess,
    GetClientDetailsReportDataSuccess, GetActivityLogFiltersSuccess,
    GetActivityLogReportSuccess, GetLoginTraceSuccess, ExportToCSVSuccess,
    GetClientDetailsReportFiltersSuccess]
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
        employee_code = parse_structure_CustomTextType_50(employee_code)
        employee_name = data.get("employee_name")
        employee_name = parse_structure_CustomTextType_50(employee_name)
        return User(employee_id, employee_code, employee_name)

    def to_structure(self):
        return {
            "employee_id": to_structure_SignedIntegerType_8(self.employee_id),
            "employee_code": to_structure_CustomTextType_50(self.employee_code),
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
        documents = parse_structure_OptionalType_VectorType_CustomTextType_50(documents)
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
            "documents": to_structure_OptionalType_VectorType_CustomTextType_50(self.documents),
            "remarks": to_structure_CustomTextType_500(self.remarks),
        }

#
# Level1Statutory
#

class Level1Compliance(object):

    def __init__(self, statutory_mapping, compliance_name, description,
        penal_consequences, compliance_frequency, repeats):
        self.statutory_mapping = statutory_mapping
        self.compliance_name = compliance_name
        self.description = description
        self.penal_consequences = penal_consequences
        self.compliance_frequency = compliance_frequency
        self.repeats = repeats

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["statutory_mapping", "compliance_name",
            "description", "penal_consequences", "compliance_frequency", "repeats"])
        statutory_mapping = data.get("statutory_mapping")
        statutory_mapping = parse_structure_Text(statutory_mapping)
        compliance_name = data.get("compliance_name")
        compliance_name = parse_structure_CustomTextType_500(compliance_name)
        description = data.get("description")
        description = parse_structure_CustomTextType_250(description)
        penal_consequences = data.get("penal_consequences")
        penal_consequences = parse_structure_CustomTextType_250(penal_consequences)
        compliance_frequency = data.get("compliance_frequency")
        compliance_frequency = parse_structure_CustomTextType_50(compliance_frequency)
        repeats = data.get("repeats")
        repeats = parse_structure_CustomTextType_50(repeats)
        return Level1Compliance(statutory_mapping, compliance_name, description,
        penal_consequences, compliance_frequency, repeats)

    def to_structure(self):
        return {
            "statutory_mapping": to_structure_Text(self.statutory_mapping),
            "compliance_name": to_structure_CustomTextType_500(self.compliance_name),
            "description": to_structure_CustomTextType_250(self.description),
            "penal_consequences": to_structure_CustomTextType_250(self.penal_consequences),
            "compliance_frequency": to_structure_CustomTextType_50(self.compliance_frequency),
            "repeats"  : to_structure_CustomTextType_50(self.repeats)
        }

class Level1Statutory(object):
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
        compliances = parse_structure_VectorType_RecordType_clientreport_Level1Compliance(compliances)
        return Level1Statutory(unit_name, address, compliances)

    def to_structure(self):
        return {
            "unit_name": to_structure_CustomTextType_100(self.unit_name),
            "address": to_structure_CustomTextType_250(self.address),
            "compliances": to_structure_VectorType_RecordType_clientreport_Level1Compliance(self.compliances)
        }

class RiskData(object):
    def __init__(self, business_group_name, legal_entity_name, division_name,
        level_1_statutory_wise_units):
        self.business_group_name = business_group_name
        self.legal_entity_name = legal_entity_name
        self.division_name = division_name
        self.level_1_statutory_wise_units = level_1_statutory_wise_units

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [ "business_group_name", "legal_entity_name",
            "division_name", "level_1_statutory_wise_units"])
        business_group_name = data.get("business_group_name")
        business_group_name = parse_structure_CustomTextType_100(business_group_name)
        legal_entity_name = data.get("legal_entity_name")
        legal_entity_name = parse_structure_CustomTextType_100(legal_entity_name)
        division_name = data.get("division_name")
        division_name = parse_structure_CustomTextType_100(division_name)
        level_1_statutory_wise_units = data.get("level_1_statutory_wise_units")
        level_1_statutory_wise_units = parse_structure_MapType_CustomTextType_50_VectorType_RecordType_clientreport_Level1Statutory(level_1_statutory_wise_units)
        return RiskData(business_group_name, legal_entity_name, division_name,
        level_1_statutory_wise_units)

    def to_structure(self):
        return {
            "business_group_name": to_structure_CustomTextType_100(self.business_group_name),
            "legal_entity_name": to_structure_CustomTextType_100(self.legal_entity_name),
            "division_name": to_structure_CustomTextType_100(self.division_name),
            "level_1_statutory_wise_units": to_structure_MapType_CustomTextType_50_VectorType_RecordType_clientreport_Level1Statutory(self.level_1_statutory_wise_units),
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
        address = parse_structure_CustomTextType_250(address)
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
            "address": to_structure_CustomTextType_250(self.address),
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
            "statutory_wise_compliances": to_structure_MapType_CustomTextType_50_MapType_CustomTextType_50_VectorType_RecordType_clientreport_ActivityData(self.statutory_wise_compliances)
        }

#
# ActivityData
#

class ActivityData(object):
    def __init__(self, activity_date, activity_status, compliance_status, remarks):
        self.activity_date = activity_date
        self.activity_status = activity_status
        self.compliance_status = compliance_status
        self.remarks = remarks

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["activity_date", "activity_status", "compliance_status", "remarks"])
        activity_date = data.get("activity_date")
        activity_date = parse_structure_CustomTextType_20(activity_date)
        activity_status = data.get("activity_status")
        activity_status = parse_structure_EnumType_core_COMPLIANCE_ACTIVITY_STATUS(activity_status)
        compliance_status = data.get("compliance_status")
        compliance_status = parse_structure_EnumType_core_COMPLIANCE_STATUS(compliance_status)
        remarks = data.get("remarks")
        remarks = parse_structure_OptionalType_CustomTextType_500(remarks)
        return ActivityCompliance(activity_date, activity_status, compliance_status, remarks)

    def to_structure(self):
        return {
            "activity_date": to_structure_CustomTextType_20(self.activity_date),
            "activity_status": to_structure_EnumType_core_COMPLIANCE_ACTIVITY_STATUS(self.activity_status),
            "compliance_status": to_structure_EnumType_core_COMPLIANCE_STATUS(self.compliance_status),
            "remarks": to_structure_OptionalType_CustomTextType_500(self.remarks),
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
        business_group_name = parse_structure_CustomTextType_100(business_group_name)
        legal_entity_name = data.get("legal_entity_name")
        legal_entity_name = parse_structure_CustomTextType_100(legal_entity_name)
        division_name = data.get("division_name")
        division_name = parse_structure_CustomTextType_100(division_name)

        user_wise_compliance = data.get("user_wise_compliance")
        user_wise_compliance = parse_structure_VectorType_RecordType_clientreport_UserWiseCompliance(user_wise_compliance)
        return AssigneeCompliance(business_group_name, legal_entity_name, division_name, user_wise_compliance)

    def to_structure(self):
        return {
            "business_group_name": to_structure_CustomTextType_100(self.business_group_name),
            "legal_entity_name": to_structure_CustomTextType_100(self.legal_entity_name),
            "division_name": to_structure_CustomTextType_100(self.division_name),
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
        description = parse_structure_CustomTextType_500(description)
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
            "description": to_structure_CustomTextType_500(self.description),
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
        description = parse_structure_CustomTextType_500(description)
        penal_consequences = data.get("penal_consequences")
        penal_consequences = parse_structure_CustomTextType_500(penal_consequences)
        compliance_frequency = data.get("compliance_frequency")
        compliance_frequency = parse_structure_EnumType_core_COMPLIANCE_FREQUENCY(compliance_frequency)
        repeats = data.get("repeats")
        repeats = parse_structure_CustomTextType_500(repeats)
        return ComplianceList(statutory_provision, compliance_name, description, penal_consequences, compliance_frequency, repeats)

    def to_structure(self):
        return {
            "statutory_provision": to_structure_Text(self.statutory_provision),
            "compliance_name": to_structure_VectorType_Text(self.compliance_name),
            "description": to_structure_CustomTextType_500(self.description),
            "penal_consequences": to_structure_CustomTextType_500(self.penal_consequences),
            "compliance_frequency": to_structure_EnumType_core_COMPLIANCE_FREQUENCY(self.compliance_frequency),
            "repeats": to_structure_CustomTextType_500(self.repeats),
        }

#
# ComplianceUnit
#

class ComplianceUnit(object):
    def __init__(self, compliance_name, unit_address, compliance_frequency, description, statutory_dates, due_date, validity_date):
        self.compliance_name = compliance_name
        self.unit_address = unit_address
        self.compliance_frequency = compliance_frequency
        self.description = description
        self.statutory_dates = statutory_dates
        self.due_date = due_date
        self.validity_date = validity_date

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["compliance_name", "unit_address", "compliance_frequency", "description", "statutory_dates", "due_date", "validity_date"])
        compliance_name = data.get("compliance_name")
        compliance_name = parse_structure_CustomTextType_500(compliance_name)
        unit_address = data.get("unit_address")
        unit_address = parse_structure_CustomTextType_500(unit_address)
        compliance_frequency = data.get("compliance_frequency")
        compliance_frequency = parse_structure_EnumType_core_COMPLIANCE_FREQUENCY(compliance_frequency)
        description = data.get("description")
        description = parse_structure_CustomTextType_500(description)
        statutory_dates = data.get("statutory_dates")
        statutory_dates = parse_structure_VectorType_RecordType_core_StatutoryDate(statutory_dates)
        due_date = data.get("due_date")
        due_date = parse_structure_CustomTextType_20(due_date)
        validity_date = data.get("validity_date")
        validity_date = parse_structure_OptionalType_CustomTextType_20(validity_date)
        return ComplianceUnit(compliance_name, unit_address, compliance_frequency, description, statutory_dates, due_date, validity_date)

    def to_structure(self):
        return {
            "compliance_name": to_structure_CustomTextType_500(self.compliance_name),
            "unit_address": to_structure_CustomTextType_500(self.unit_address),
            "compliance_frequency": to_structure_EnumType_core_COMPLIANCE_FREQUENCY(self.compliance_frequency),
            "description": to_structure_CustomTextType_500(self.description),
            "statutory_dates": to_structure_VectorType_RecordType_core_StatutoryDate(self.statutory_dates),
            "due_date": to_structure_CustomTextType_20(self.due_date),
            "validity_date": to_structure_OptionalType_CustomTextType_20(self.validity_date),
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
    def __init__(self, unit_name, address, reassign_compliances):
        self.unit_name = unit_name
        self.address = address
        self.reassign_compliances = reassign_compliances

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["unit_name",  "address", "reassign_compliances"])
        unit_name = data.get("unit_name")
        unit_name = parse_structure_CustomTextType_100(unit_name)
        address = data.get("address")
        address = parse_structure_CustomTextType_100(address)
        reassign_compliances = data.get("reassign_compliances")
        reassign_compliances = parse_structure_VectorType_RecordType_clientreport_ReassignCompliance(reassign_compliances)
        return ReassignCompliance(unit_name, address, reassign_compliances)

    def to_structure(self):
        return {
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
        due_date = parse_structure_CustomTextType_20(due_date)
        reassign_history = data.get("reassign_history")
        reassign_history = parse_structure_VectorType_RecordType_clientreport_ReassignHistory(reassign_history)
        return ReassignCompliance(compliance_name, due_date, reassign_history)

    def to_structure(self):
        return {
            "compliance_name": to_structure_CustomTextType_500(self.compliance_name),
            "due_date": to_structure_CustomTextType_20(self.due_date),
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
        business_group_name = parse_structure_CustomTextType_50(business_group_name)
        legal_entity_name = data.get("legal_entity_name")
        legal_entity_name = parse_structure_CustomTextType_50(legal_entity_name)
        division_name = data.get("division_name")
        division_name = parse_structure_CustomTextType_50(division_name)
        unit_wise_compliances = data.get("unit_wise_compliances")
        unit_wise_compliances = parse_structure_MapType_CustomTextType_50_VectorType_RecordType_clientreport_ComplianceUnit(unit_wise_compliances)
        return UnitCompliance(business_group_name, legal_entity_name, division_name, unit_wise_compliances)

    def to_structure(self):
        return {
            "business_group_name": to_structure_CustomTextType_50(self.business_group_name),
            "legal_entity_name": to_structure_CustomTextType_50(self.legal_entity_name),
            "division_name": to_structure_CustomTextType_50(self.division_name),
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
        user_id = parse_structure_UnsignedIntegerType_32(user_id)
        user_name = data.get("user_name")
        user_name = parse_structure_CustomTextType_100(user_name)
        return UserName(user_id, user_name)

    def to_structure(self):
        return {
            "user_id": to_structure_SignedIntegerType_8(self.user_id),
            "user_name": to_structure_CustomTextType_100(self.user_name),
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
        business_group_name = parse_structure_CustomTextType_50(business_group_name)
        legal_entity_name = data.get("legal_entity_name")
        legal_entity_name = parse_structure_CustomTextType_50(legal_entity_name)
        division_name = data.get("division_name")
        division_name = parse_structure_CustomTextType_50(division_name)
        level_1_statutory_wise_notifications = data.get("level_1_statutory_wise_notifications")
        level_1_statutory_wise_notifications = parse_structure_VectorType_RecordType_clientreport_LEVEL_1_STATUTORY_NOTIFICATIONS(level_1_statutory_wise_notifications)
        return STATUTORY_WISE_NOTIFICATIONS(business_group_name, legal_entity_name, division_name, level_1_statutory_wise_notifications)

    def to_structure(self):
        return {
            "business_group_name": to_structure_CustomTextType_50(self.business_group_name),
            "legal_entity_name": to_structure_CustomTextType_50(self.legal_entity_name),
            "division_name": to_structure_CustomTextType_50(self.division_name),
            "level_1_statutory_wise_notifications": to_structure_MapType_CustomTextType_50_VectorType_RecordType_clientreport_LEVEL_1_STATUTORY_NOTIFICATIONS(self.level_1_statutory_wise_notifications),
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
        notification_text = parse_structure_CustomTextType_500(notification_text)
        date_and_time = data.get("date_and_time")
        date_and_time = parse_structure_CustomTextType_20(date_and_time)
        return LEVEL_1_STATUTORY_NOTIFICATIONS(statutory_provision, notification_text, date_and_time)

    def to_structure(self):
        return {
            "statutory_provision": to_structure_Text(self.statutory_provision),
            "unit_name": to_structure_CustomTextType_250(self.unit_name),
            "notification_text": to_structure_CustomTextType_500(self.notification_text),
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
        approval_person = parse_structure_CustomTextType_100(approval_person)
        compliances = data.get("compliances")
        compliances = parse_structure_VectorType_RecordType_clientreport_ComplianceUnit(compliances)
        return UserWiseCompliance(assignee, concurrence_person, approval_person, compliances)

    def to_structure(self):
        return {
            "assignee": to_structure_CustomTextType_100(self.assignee),
            "concurrence_person": to_structure_OptionalType_CustomTextType_100(self.concurrence_person),
            "approval_person": to_structure_CustomTextType_100(self.approval_person),
            "compliances": to_structure_VectorType_RecordType_clientreport_ComplianceUnit(self.compliances),
        }

class GroupedUnits(object):
    def __init__(self, division_id, legal_entity_id, business_group_id, units):
        self.division_id = division_id
        self.legal_entity_id = legal_entity_id
        self.business_group_id = business_group_id
        self.units = units

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["division_id", "legal_entity_id", "business_group_id", "units"])
        division_id = data.get("division_id")
        division_id = parse_structure_OptionalType_UnsignedIntegerType_32(division_id)
        legal_entity_id = data.get("legal_entity_id")
        legal_entity_id = parse_structure_UnsignedIntegerType_32(legal_entity_id)
        business_group_id = data.get("business_group_id")
        business_group_id = parse_structure_OptionalType_UnsignedIntegerType_32(business_group_id)
        units = data.get("units")
        units = parse_structure_VectorType_RecordType_client_report_UnitDetails(units)
        return GroupedUnits(division_id, legal_entity_id, business_group_id, units)

    def to_structure(self):
        return {
            "division_id": to_structure_OptionalType_UnsignedIntegerType_32(self.division_id),
            "legal_entity_id": to_structure_UnsignedIntegerType_32(self.legal_entity_id),
            "business_group_id": to_structure_OptionalType_UnsignedIntegerType_32(self.business_group_id),
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
