from protocol.jsonvalidators import (parse_dictionary, parse_static_list)
from protocol.parse_structure import (
    parse_structure_UnsignedIntegerType_32,
    parse_structure_OptionalType_VectorType_RecordType_core_FileList,
    parse_structure_OptionalType_CustomTextType_20,
    parse_structure_OptionalType_CustomTextType_500,
    parse_structure_Bool,
    parse_structure_CustomTextType_50,
    parse_structure_CustomTextType_20,
    parse_structure_CustomTextType_100,
    parse_structure_VectorType_SignedIntegerType_8,
    parse_structure_VectorType_CustomTextType_50,
    parse_structure_OptionalType_SignedIntegerType_8,
    parse_structure_CustomTextType_500,
    parse_structure_VectorType_RecordType_core_ClientConfiguration,
    parse_structure_RecordType_core_Menu,
    parse_structure_VectorType_RecordType_mobile_GetUsersList,
    parse_structure_VectorType_RecordType_core_Country,
    parse_structure_VectorType_RecordType_core_Domain,
    parse_structure_VectorType_RecordType_core_Industry,
    parse_structure_VectorType_RecordType_core_ClientBusinessGroup,
    parse_structure_VectorType_RecordType_core_ClientLegalEntity,
    parse_structure_VectorType_RecordType_core_ClientDivision,
    parse_structure_VectorType_RecordType_technotransactions_UNIT,
    parse_structure_VectorType_RecordType_mobile_ComplianceApplicability,
    parse_structure_VectorType_RecordType_mobile_UnitWiseCount,
    parse_structure_VectorType_RecordType_mobile_DomainWiseCount,
    parse_structure_VariantType_mobile_Request,
    parse_structure_VectorType_RecordType_clienttransactions_ASSIGN_COMPLIANCE_UNITS,
    parse_structure_VectorType_RecordType_mobile_ComplianceHistory
)
from protocol.to_structure import (
    to_structure_UnsignedIntegerType_32,
    to_structure_OptionalType_VectorType_RecordType_core_FileList,
    to_structure_OptionalType_CustomTextType_20,
    to_structure_OptionalType_CustomTextType_500,
    to_structure_Bool,
    to_structure_CustomTextType_50,
    to_structure_CustomTextType_20,
    to_structure_CustomTextType_100,
    to_structure_VectorType_SignedIntegerType_8,
    to_structure_VectorType_CustomTextType_50,
    to_structure_OptionalType_SignedIntegerType_8,
    to_structure_CustomTextType_500,
    to_structure_VectorType_RecordType_core_ClientConfiguration,
    to_structure_RecordType_core_Menu,
    to_structure_VectorType_RecordType_mobile_GetUsersList,
    to_structure_VectorType_RecordType_core_Country,
    to_structure_VectorType_RecordType_core_Domain,
    to_structure_VectorType_RecordType_core_Industry,
    to_structure_VectorType_RecordType_core_ClientBusinessGroup,
    to_structure_VectorType_RecordType_core_ClientLegalEntity,
    to_structure_VectorType_RecordType_core_ClientDivision,
    to_structure_VectorType_RecordType_technotransactions_UNIT,
    to_structure_VectorType_RecordType_mobile_ComplianceApplicability,
    to_structure_VectorType_RecordType_mobile_UnitWiseCount,
    to_structure_VectorType_RecordType_mobile_DomainWiseCount,
    to_structure_VariantType_mobile_Request
    to_structure_VectorType_RecordType_clienttransactions_ASSIGN_COMPLIANCE_UNITS,
    to_structure_VectorType_RecordType_mobile_ComplianceHistory
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

class GetVersions(Request):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return GetVersions()

    def to_inner_structure(self):
        return {
        }


class GetUsers(Request):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return GetUsers()

    def to_inner_structure(self):
        return {
        }


class GetUnitDetails(Request):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return GetUnitDetails()

    def to_inner_structure(self):
        return {
        }


class GetComplianceApplicabilityStatus(Request):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return GetComplianceApplicabilityStatus()

    def to_inner_structure(self):
        return {
        }

class GetComplianceHistory(Request):
    def __init__(self, compliance_history_id):
        self.compliance_history_id = compliance_history_id

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(
            data, [
                "compliance_history_id"
            ]
        )
        compliance_history_id = data.get("compliance_history_id")
        compliance_history_id = parse_structure_UnsignedIntegerType_32(compliance_history_id)
        return GetComplianceHistory(
            compliance_history_id
        )

    def to_inner_structure(self):
        return {
            "compliance_history_id": to_structure_UnsignedIntegerType_32(self.compliance_history_id)
        }

class GetReassignedComplianceHistory(Request):
    def __init__(
        self, user_id, version
    ):
        self.user_id = user_id
        self.version = version

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(
            data, [
                "user_id", "version",
            ]
        )
        user_id = data.get("user_id")
        user_id = parse_structure_UnsignedIntegerType_32(user_id)
        version = data.get("version")
        version = parse_structure_UnsignedIntegerType_32(version)
        return GetReassignedComplianceHistory(
            user_id, version
        )

    def to_inner_structure(self):
        return {
            "user_id": to_structure_UnsignedIntegerType_32(self.user_id),
            "version": to_structure_UnsignedIntegerType_32(self.version),
        }

class GetPastFourYearEscalations(Request):
    def __init__(
        self, user_id, version
    ):
        self.user_id = user_id
        self.version = version

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(
            data, [
                "user_id", "version",
            ]
        )
        user_id = data.get("user_id")
        user_id = parse_structure_UnsignedIntegerType_32(user_id)
        version = data.get("version")
        version = parse_structure_UnsignedIntegerType_32(version)
        return GetPastFourYearEscalations(
            user_id, version
        )

    def to_inner_structure(self):
        return {
            "user_id": to_structure_UnsignedIntegerType_32(self.user_id),
            "version": to_structure_UnsignedIntegerType_32(self.version),
        }

class CheckDiskSpace(Request):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return CheckDiskSpace()

    def to_inner_structure(self):
        return {
        }

class SaveCompliance(Request):
    def __init__(
        self, compliance_history_id, user_id, documents
    ):
        self.compliance_history_id = compliance_history_id
        self.user_id = user_id
        self.documents = documents

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(
            data, [
                "compliance_history_id", "user_id", "documents"
            ]
        )
        compliance_history_id = data.get("compliance_history_id")
        compliance_history_id = parse_structure_UnsignedIntegerType_32(compliance_history_id)
        user_id = data.get("user_id")
        user_id = parse_structure_UnsignedIntegerType_32(user_id)
        documents = data.get("documents")
        documents = parse_structure_OptionalType_VectorType_RecordType_core_FileList(documents)
        completion_date = data.get("completion_date")
        completion_date = parse_structure_CustomTextType_20(completion_date)
        validity_date = data.get("validity_date")
        validity_date = parse_structure_OptionalType_CustomTextType_20(validity_date)
        next_due_date = data.get("next_due_date")
        next_due_date = parse_structure_OptionalType_CustomTextType_20(next_due_date)
        remarks = data.get("remarks")
        remarks = parse_structure_OptionalType_CustomTextType_500(remarks)
        return SaveCompliance(
            compliance_history_id, user_id, documents, completion_date, validity_date,
            next_due_date, remarks
        )

    def to_inner_structure(self):
        return {
            "compliance_history_id": to_structure_UnsignedIntegerType_32(self.compliance_history_id),
            "user_id": to_structure_UnsignedIntegerType_32(self.user_id),
            "documents": to_structure_OptionalType_VectorType_RecordType_core_FileList(self.documents),
            "completion_date": to_structure_CustomTextType_20(self.completion_date),
            "validity_date": to_structure_OptionalType_CustomTextType_20(self.validity_date),
            "next_due_date": to_structure_OptionalType_CustomTextType_20(self.next_due_date),
            "remarks": to_structure_OptionalType_CustomTextType_500(self.remarks),
        }

class ApproveCompliance(object):
    def __init__(
        self, compliance_history_id, approval_status, concurrence_status, approved_on, concurred_on, remarks
    ):
        self.compliance_history_id = compliance_history_id
        self.approval_status = approval_status
        self.concurrence_status = concurrence_status
        self.approved_on = approved_on
        self.concurred_on = concurred_on
        self.remarks = remarks

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(
            data, [
                "compliance_history_id", "approval_status", "concurrence_status",
                "approved_on", "concurred_on", "remarks"
            ]
        )
        compliance_history_id = data.get("compliance_history_id")
        compliance_history_id = parse_structure_UnsignedIntegerType_32(compliance_history_id)
        approval_status = data.get("approval_status")
        approval_status = parse_structure_Bool(approval_status)
        concurrence_status = data.get("concurrence_status")
        concurrence_status = parse_structure_Bool(concurrence_status)
        approved_on = data.get("approved_on")
        approved_on = parse_structure_CustomTextType_20(approved_on)
        concurred_on = data.get("concurred_on")
        concurred_on = parse_structure_OptionalType_CustomTextType_20(concurred_on)
        remarks = data.get("remarks")
        remarks = parse_structure_OptionalType_CustomTextType_500(remarks)
        return ApproveCompliance(
            compliance_history_id, approval_status, concurrence_status, approved_on, concurred_on, remarks
        )

    def to_inner_structure(self):
        return {
            "compliance_history_id": to_structure_UnsignedIntegerType_32(self.compliance_history_id),
            "approval_status": to_structure_Bool(self.approval_status),
            "concurrence_status": to_structure_Bool(self.concurrence_status),
            "approved_on": to_structure_CustomTextType_20(self.approved_on),
            "concurred_on": to_structure_OptionalType_CustomTextType_20(self.concurred_on),
            "remarks": to_structure_OptionalType_CustomTextType_500(self.remarks)
        }

class ApproveComplianceList(object):
    def __init__(
        self, compliances
    ):
        self.compliances = compliances

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(
            data, [
                "compliances"
            ]
        )
        compliances = data.get("compliances")
        compliances = parse_structure_VectorType_RecordType_mobile_ApproveCompliance(compliances)
        return ApproveCompliance(
            compliances
        )

    def to_inner_structure(self):
        return {
            "compliances": to_structure_VectorType_RecordType_mobile_ApproveCompliance(self.compliances)
        }

class GetTrendChartData(Request):
    def __init__(
        self, user_id
    ):
        self.user_id = user_id

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(
            data, [
                "user_id"
            ]
        )
        user_id = data.get("user_id")
        user_id = parse_structure_UnsignedIntegerType_32(user_id)
        return GetTrendChartData(
            user_id
        )

    def to_inner_structure(self):
        return {
            "user_id": to_structure_UnsignedIntegerType_32(self.user_id)
        }

def _init_Request_class_map():
    classes = [
        GetVersions,
        GetUsers,
        GetUnitDetails,
        GetComplianceApplicabilityStatus,
        GetTrendChartData
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

class UserLoginResponseSuccess(Response):
    def __init__(
        self, user_id, name, session_token
    ):
        self.user_id = user_id
        self.name = name
        self.session_token = session_token

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["user_id", "name", "session_token"])
        user_id = data.get("user_id")
        user_id = parse_structure_UnsignedIntegerType_32(user_id)
        name = data.get("name")
        name = parse_structure_CustomTextType_50(name)
        session_token = data.get("session_token")
        session_token = parse_structure_CustomTextType_50(session_token)
        return UserLoginResponseSuccess(user_id, name, session_token)

    def to_inner_structure(self):
        return {
            "user_id": to_structure_UnsignedIntegerType_32(self.user_id),
            "name": to_structure_CustomTextType_100(self.name),
            "session_token": to_structure_CustomTextType_50(self.session_token)
        }

class ClientUserLoginResponseSuccess(Response):
    def __init__(
        self, user_id, name, session_token,
        group_id, group_name, configuration,
        menu
    ):
        self.user_id = user_id
        self.name = name
        self.session_token = session_token
        self.group_id = group_id
        self.group_name = group_name
        self.configuration = configuration
        self.menu = menu

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "user_id", "name", "session_token",
            "group_id", "group_name",
            "configuration", "menu"
        ])
        user_id = data.get("user_id")
        user_id = parse_structure_UnsignedIntegerType_32(user_id)
        name = data.get("name")
        name = parse_structure_CustomTextType_50(name)
        session_token = data.get("session_token")
        session_token = parse_structure_CustomTextType_50(session_token)
        group_id = data.get("group_id")
        group_id = parse_structure_UnsignedIntegerType_32(group_id)
        group_name = data.get("group_name")
        group_name = parse_structure_CustomTextType_100(group_name)
        configuration = data.get("configuration")
        configuration = parse_structure_VectorType_RecordType_core_ClientConfiguration(configuration)
        menu = data.get("menu")
        menu = parse_structure_RecordType_core_Menu(menu)
        return ClientUserLoginResponseSuccess(user_id, name, session_token, group_id, group_name, configuration, menu)

    def to_inner_structure(self):
        return {
            "user_id": to_structure_UnsignedIntegerType_32(self.user_id),
            "name": to_structure_CustomTextType_100(self.name),
            "session_token": to_structure_CustomTextType_50(self.session_token),
            "group_id": to_structure_UnsignedIntegerType_32(self.group_id),
            "group_name": to_structure_CustomTextType_100(self.group_name),
            "configuration": to_structure_VectorType_RecordType_core_ClientConfiguration(self.configuration),
            "menu": to_structure_RecordType_core_Menu(self.menu)
        }

class GetVersionsSuccess(Response):
    def __init__(
        self, unit_details_version, user_details_version,
        compliance_applicability_version, compliance_history_version,
        reassign_history_version
    ):
        self.unit_details_version = unit_details_version
        self.user_details_version = user_details_version
        self.compliance_applicability_version = compliance_applicability_version
        self.compliance_history_version = compliance_history_version
        self.reassign_history_version = reassign_history_version

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(
            data, [
                "unit_details_version", "user_details_version",
                "compliance_applicability_version", "compliance_history_version",
                "reassign_history_version"
            ]
        )
        unit_details_version = data.get("unit_details_version")
        unit_details_version = parse_structure_UnsignedIntegerType_32(unit_details_version)
        user_details_version = data.get("user_details_version")
        user_details_version = parse_structure_UnsignedIntegerType_32(user_details_version)
        compliance_applicability_version = data.get("compliance_applicability_version")
        compliance_applicability_version = parse_structure_UnsignedIntegerType_32(compliance_applicability_version)
        compliance_history_version = data.get("compliance_history_version")
        compliance_history_version = parse_structure_UnsignedIntegerType_32(compliance_history_version)
        reassign_history_version = data.get("reassign_history_version")
        reassign_history_version = parse_structure_UnsignedIntegerType_32(reassign_history_version)
        return GetVersionsSuccess(
            unit_details_version, user_details_version,
            compliance_applicability_version, compliance_history_version,
            reassign_history_version
        )

    def to_inner_structure(self):
        return {
            "unit_details_version": to_structure_UnsignedIntegerType_32(self.unit_details_version),
            "user_details_version": to_structure_UnsignedIntegerType_32(self.user_details_version),
            "compliance_applicability_version": to_structure_UnsignedIntegerType_32(self.compliance_applicability_version),
            "compliance_history_version": to_structure_UnsignedIntegerType_32(self.compliance_history_version),
            "reassign_history_version": to_structure_UnsignedIntegerType_32(self.reassign_history_version)
        }

class GetUsersList(object):
    def __init__(
        self, user_id, user_name
    ):
        self.user_id = user_id
        self.user_name = user_name

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(
            data, [
                "user_id", "user_name"
            ]
        )
        user_id = data.get("user_id")
        user_id = parse_structure_UnsignedIntegerType_32(user_id)
        user_name = data.get("user_name")
        user_name = parse_structure_CustomTextType_50(user_name)
        return GetUsersList(
            user_id, user_name
        )

    def to_structure(self):
        return {
            "user_id": to_structure_UnsignedIntegerType_32(self.user_id),
            "user_name": to_structure_CustomTextType_50(self.user_name)
        }

class GetUsersSuccess(Response):
    def __init__(self, user_list):
        self.user_list = user_list

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["user_list"])
        user_list = data.get("user_list")
        user_list = parse_structure_VectorType_RecordType_mobile_GetUsersList(user_list)
        return GetUsersSuccess(user_list)

    def to_inner_structure(self):
        return to_structure_VectorType_RecordType_mobile_GetUsersList(self.user_list)

class GetUnitDetailsSuccess(Response):
    def __init__(self, countries, domains, business_groups, legal_entities, divisions, units):
        self.countries = countries
        self.domains = domains
        self.business_groups = business_groups
        self.legal_entities = legal_entities
        self.divisions = divisions
        self.units = units

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["countries", "domains", "industries", "business_groups", "legal_entities", "divisions", "units"])
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
        return GetUnitDetailsSuccess(
            countries, domains, business_groups,
            legal_entities, divisions, units
        )

    def to_inner_structure(self):
        return {
            "countries": to_structure_VectorType_RecordType_core_Country(self.countries),
            "domains": to_structure_VectorType_RecordType_core_Domain(self.domains),
            "business_groups": to_structure_VectorType_RecordType_core_ClientBusinessGroup(self.business_groups),
            "legal_entities": to_structure_VectorType_RecordType_core_ClientLegalEntity(self.legal_entities),
            "divisions": to_structure_VectorType_RecordType_core_ClientDivision(self.divisions),
            "units": to_structure_VectorType_RecordType_clienttransactions_ASSIGN_COMPLIANCE_UNITS(self.units),
        }

class ComplianceApplicability(object):
    def __init__(
        self, country_id, domain_id, unit_id, compliance_id, compliance_name,
        compliance_frequency, compliance_applicable, compliance_opted
    ):
        self.country_id = country_id
        self.domain_id = domain_id
        self.unit_id = unit_id
        self.compliance_id = compliance_id
        self.compliance_name = compliance_name
        self.compliance_frequency = compliance_frequency
        self.compliance_applicable = compliance_applicable
        self.compliance_opted = compliance_opted

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(
            data, [
                "country_id", "domain_id", "unit_id", "compliance_id",
                "compliance_name", "compliance_frequency",
                "compliance_applicable", "compliance_opted"
            ]
        )
        country_id = data.get("country_id")
        country_id = parse_structure_UnsignedIntegerType_32(country_id)
        domain_id = data.get("domain_id")
        domain_id = parse_structure_UnsignedIntegerType_32(domain_id)
        unit_id = data.get("unit_id")
        unit_id = parse_structure_UnsignedIntegerType_32(unit_id)
        compliance_id = data.get("compliance_id")
        compliance_id = parse_structure_UnsignedIntegerType_32(compliance_id)
        compliance_name = data.get("compliance_name")
        compliance_name = parse_structure_CustomTextType_500(compliance_name)
        compliance_frequency = data.get("compliance_frequency")
        compliance_frequency = parse_structure_CustomTextType_100(compliance_frequency)
        compliance_applicable = data.get("compliance_applicable")
        compliance_applicable = parse_structure_Bool(compliance_applicable)
        compliance_opted = data.get("compliance_opted")
        compliance_opted = parse_structure_Bool(compliance_opted)
        return ComplianceApplicability(
            country_id, domain_id, unit_id, compliance_id, compliance_name,
            compliance_frequency, compliance_applicable, compliance_opted
        )

    def to_structure(self):
        return {
            "country_id" : to_structure_UnsignedIntegerType_32(self.country_id),
            "domain_id" : to_structure_UnsignedIntegerType_32(self.domain_id),
            "unit_id" : to_structure_UnsignedIntegerType_32(self.unit_id),
            "compliance_id" : to_structure_UnsignedIntegerType_32(self.compliance_id),
            "compliance_name" : to_structure_CustomTextType_500(self.compliance_name),
            "compliance_frequency" : to_structure_CustomTextType_100(self.compliance_frequency),
            "compliance_applicable" : to_structure_Bool(self.compliance_applicable),
            "compliance_opted" : to_structure_Bool(self.compliance_opted)
        }

class GetComplianceApplicabilityStatusSuccess(Response):
    def __init__(
        self, applicabilty_list
    ):
        self.applicabilty_list = applicabilty_list

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(
            data, [
                "applicabilty_list"
            ]
        )
        applicabilty_list = data.get("applicabilty_list")
        applicabilty_list = parse_structure_VectorType_RecordType_mobile_ComplianceApplicability(applicabilty_list)
        return GetComplianceApplicabilityStatusSuccess(
            applicabilty_list
        )

    def to_inner_structure(self):
        return to_structure_VectorType_RecordType_mobile_ComplianceApplicability(self.applicabilty_list)


class ComplianceHistory(object):
    def __init__(
        self, compliance_history_id, unit_id, compliance_id, start_date,
        due_date, completion_date, documents, validity_date, next_due_date,
        remarks, completed_by, completed_on, concurrence_status, concurred_by,
        concurred_on, approval_status, approved_by, approved_on
    ):
        self.compliance_history_id = compliance_history_id
        self.unit_id = unit_id
        self.compliance_id = compliance_id
        self.start_date = start_date
        self.due_date = due_date
        self.completion_date = completion_date
        self.documents = documents
        self.validity_date = validity_date
        self.next_due_date = next_due_date
        self.remarks = remarks
        self.completed_by = completed_by
        self.completed_on = completed_on
        self.concurrence_status = concurrence_status
        self.concurred_by = concurred_by
        self.concurred_on = concurred_on
        self.approval_status = approval_status
        self.approved_by = approved_by
        self.approved_on = approved_on

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(
            data, [
                "compliance_history_id", "unit_id", "compliance_id", "start_date",
                "due_date", "completion_date", "documents", "validity_date",
                "next_due_date", "remarks", "completed_by", "completed_on",
                "concurrence_status", "concurred_by", "concurred_on",
                "approval_status", "approved_by", "approved_on"
            ]
        )
        compliance_history_id = data.get("compliance_history_id")
        compliance_history_id = parse_structure_UnsignedIntegerType_32(compliance_history_id)
        unit_id = data.get("unit_id")
        unit_id = parse_structure_UnsignedIntegerType_32(unit_id)
        compliance_id = data.get("compliance_id")
        compliance_id = parse_structure_UnsignedIntegerType_32(compliance_id)
        start_date = data.get("start_date")
        start_date = parse_structure_CustomTextType_20(start_date)
        due_date = data.get("due_date")
        due_date = parse_structure_CustomTextType_20(due_date)
        completion_date = data.get("completion_date")
        completion_date = parse_structure_CustomTextType_20(completion_date)
        documents = data.get("documents")
        documents = parse_structure_OptionalType_VectorType_RecordType_core_FileList(documents)
        validity_date = data.get("validity_date")
        validity_date = parse_structure_CustomTextType_20(validity_date)
        next_due_date = data.get("next_due_date")
        next_due_date = parse_structure_CustomTextType_20(next_due_date)
        remarks = data.get("remarks")
        remarks = parse_structure_CustomTextType_100(remarks)
        completed_by = data.get("completed_by")
        completed_by = parse_structure_UnsignedIntegerType_32(completed_by)
        completed_on = data.get("completed_on")
        completed_on = parse_structure_CustomTextType_20(completed_on)
        concurrence_status = data.get("concurrence_status")
        concurrence_status = parse_structure_Bool(concurrence_status)
        concurred_by = data.get("concurred_by")
        concurred_by = parse_structure_UnsignedIntegerType_32(concurred_by)
        concurred_on = data.get("concurred_on")
        concurred_on = parse_structure_CustomTextType_20(concurred_on)
        approval_status = data.get("approval_status")
        approval_status = parse_structure_Bool(approval_status)
        approved_by = data.get("approved_by")
        approved_by = parse_structure_UnsignedIntegerType_32(approved_by)
        approved_on = data.get("approved_on")
        approved_on = parse_structure_CustomTextType_20(approved_on)
        return ComplianceHistory(
            compliance_history_id, unit_id, compliance_id, start_date,
            due_date, completion_date, documents, validity_date, next_due_date,
            remarks, completed_by, completed_on, concurrence_status, concurred_by,
            concurred_on, approval_status, approved_by, approved_on
        )

    def to_structure(self):
        return {
            "compliance_history_id" : to_structure_UnsignedIntegerType_32(self.compliance_history_id),
            "unit_id" : to_structure_UnsignedIntegerType_32(self.unit_id),
            "compliance_id" : to_structure_UnsignedIntegerType_32(self.compliance_id),
            "start_date" : to_structure_CustomTextType_20(self.start_date),
            "due_date" : to_structure_CustomTextType_20(self.due_date),
            "completion_date" : to_structure_CustomTextType_20(self.completion_date),
            "documents" : to_structure_OptionalType_VectorType_RecordType_core_FileList(self.documents),
            "validity_date" : to_structure_CustomTextType_20(self.validity_date),
            "next_due_date" : to_structure_CustomTextType_20(self.next_due_date),
            "remarks" : to_structure_CustomTextType_100(self.remarks),
            "completed_by" : to_structure_UnsignedIntegerType_32(self.completed_by),
            "completed_on" : to_structure_CustomTextType_20(self.completed_on),
            "concurrence_status" : to_structure_Bool(self.concurrence_status),
            "concurred_by" : to_structure_UnsignedIntegerType_32(self.concurred_by),
            "concurred_on" : to_structure_CustomTextType_20(self.concurred_on),
            "approval_status" : to_structure_Bool(self.approval_status),
            "approved_by" : to_structure_UnsignedIntegerType_32(self.approved_by),
            "approved_on" : to_structure_CustomTextType_20(self.approved_on)
        }

class GetComplianceHistorySuccess(Response):
    def __init__(
        self, compliance_history
    ):
        self.compliance_history = compliance_history

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(
            data, [
                "compliance_history"
            ]
        )
        compliance_history = data.get("compliance_history")
        compliance_history = parse_structure_VectorType_RecordType_mobile_ComplianceHistory(compliance_history)
        return GetComplianceHistorySuccess(
            compliance_history
        )

    def to_inner_structure(self):
        return to_structure_VectorType_RecordType_mobile_ComplianceHistory(self.compliance_history)

class ReassignHistory(object):
    def __init__(
        self, compliance_history_id, unit_id, assignee,
        reassigned_from, reassigned_date, remarks
    ):
        self.compliance_history_id = compliance_history_id
        self.unit_id = unit_id
        self.assignee = assignee
        self.reassigned_from = reassigned_from
        self.reassigned_date = reassigned_date
        self.remarks = remarks

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(
            data, [
                "compliance_history_id", "unit_id", "assignee",
                "reassigned_from", "reassigned_date", "remarks"
            ]
        )
        compliance_history_id = data.get("compliance_history_id")
        compliance_history_id = parse_structure_UnsignedIntegerType_32(compliance_history_id)
        unit_id = data.get("unit_id")
        unit_id = parse_structure_UnsignedIntegerType_32(unit_id)
        compliance_id = data.get("compliance_id")
        compliance_id = parse_structure_UnsignedIntegerType_32(compliance_id)
        start_date = data.get("start_date")
        start_date = parse_structure_CustomTextType_20(start_date)
        due_date = data.get("due_date")
        due_date = parse_structure_CustomTextType_20(due_date)
        completion_date = data.get("completion_date")
        completion_date = parse_structure_CustomTextType_20(completion_date)
        documents = data.get("documents")
        documents = parse_structure_OptionalType_VectorType_RecordType_core_FileList(documents)
        validity_date = data.get("validity_date")
        validity_date = parse_structure_CustomTextType_20(validity_date)
        next_due_date = data.get("next_due_date")
        next_due_date = parse_structure_CustomTextType_20(next_due_date)
        remarks = data.get("remarks")
        remarks = parse_structure_CustomTextType_100(remarks)
        completed_by = data.get("completed_by")
        completed_by = parse_structure_UnsignedIntegerType_32(completed_by)
        completed_on = data.get("completed_on")
        completed_on = parse_structure_CustomTextType_20(completed_on)
        concurrence_status = data.get("concurrence_status")
        concurrence_status = parse_structure_Bool(concurrence_status)
        concurred_by = data.get("concurred_by")
        concurred_by = parse_structure_UnsignedIntegerType_32(concurred_by)
        concurred_on = data.get("concurred_on")
        concurred_on = parse_structure_CustomTextType_20(concurred_on)
        approval_status = data.get("approval_status")
        approval_status = parse_structure_Bool(approval_status)
        approved_by = data.get("approved_by")
        approved_by = parse_structure_UnsignedIntegerType_32(approved_by)
        approved_on = data.get("approved_on")
        approved_on = parse_structure_CustomTextType_20(approved_on)
        return ReassignHistory(
            compliance_history_id, unit_id, compliance_id, start_date,
            due_date, completion_date, documents, validity_date, next_due_date,
            remarks, completed_by, completed_on, concurrence_status, concurred_by,
            concurred_on, approval_status, approved_by, approved_on
        )

    def to_structure(self):
        return {
            "compliance_history_id" : to_structure_UnsignedIntegerType_32(self.compliance_history_id),
            "unit_id" : to_structure_UnsignedIntegerType_32(self.unit_id),
            "compliance_id" : to_structure_UnsignedIntegerType_32(self.compliance_id),
            "start_date" : to_structure_CustomTextType_20(self.start_date),
            "due_date" : to_structure_CustomTextType_20(self.due_date),
            "completion_date" : to_structure_CustomTextType_20(self.completion_date),
            "documents" : to_structure_OptionalType_VectorType_RecordType_core_FileList(self.documents),
            "validity_date" : to_structure_CustomTextType_20(self.validity_date),
            "next_due_date" : to_structure_CustomTextType_20(self.next_due_date),
            "remarks" : to_structure_CustomTextType_100(self.remarks),
            "completed_by" : to_structure_UnsignedIntegerType_32(self.completed_by),
            "completed_on" : to_structure_CustomTextType_20(self.completed_on),
            "concurrence_status" : to_structure_Bool(self.concurrence_status),
            "concurred_by" : to_structure_UnsignedIntegerType_32(self.concurred_by),
            "concurred_on" : to_structure_CustomTextType_20(self.concurred_on),
            "approval_status" : to_structure_Bool(self.approval_status),
            "approved_by" : to_structure_UnsignedIntegerType_32(self.approved_by),
            "approved_on" : to_structure_CustomTextType_20(self.approved_on)
        }

class DomainWiseCount(object):
    def __init__(
        self, domain_id, year, total_compliances, complied_compliances_count
    ):
        self.domain_id = domain_id
        self.year = year
        self.total_compliances = total_compliances
        self.complied_compliances_count = complied_compliances_count

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(
            data, [
                "domain_id", "year", "total_compliances",
                "complied_compliances_count"
            ]
        )
        domain_id = data.get("domain_id")
        domain_id = parse_structure_UnsignedIntegerType_32(domain_id)
        year = data.get("year")
        year = parse_structure_UnsignedIntegerType_32(year)
        total_compliances = data.get("total_compliances")
        total_compliances = parse_structure_UnsignedIntegerType_32(total_compliances)
        complied_compliances_count = data.get("complied_compliances")
        complied_compliances_count = parse_structure_UnsignedIntegerType_32(complied_compliances_count)
        return DomainWiseCount(
            domain_id, year, total_compliances, complied_compliances_count
        )

    def to_structure(self):
        return {
            "domain_id" : to_structure_UnsignedIntegerType_32(self.domain_id),
            "year" : to_structure_UnsignedIntegerType_32(self.year),
            "total_compliances" : to_structure_UnsignedIntegerType_32(self.total_compliances),
            "complied_compliances_count" : to_structure_UnsignedIntegerType_32(self.complied_compliances_count)
        }

class UnitWiseCount(object):
    def __init__(
        self, unit_id, domain_wise_count
    ):
        self.unit_id = unit_id
        self.domain_wise_count = domain_wise_count

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(
            data, [
                "unit_id", "domain_wise_count"
            ]
        )
        unit_id = data.get("unit_id")
        unit_id = parse_structure_UnsignedIntegerType_32(unit_id)
        domain_wise_count = data.get("domain_wise_count")
        domain_wise_count = parse_structure_VectorType_RecordType_mobile_DomainWiseCount(domain_wise_count)
        return UnitWiseCount(
            unit_id, domain_wise_count
        )

    def to_structure(self):
        return {
            "unit_id": to_structure_UnsignedIntegerType_32(self.unit_id),
            "domain_wise_count": to_structure_VectorType_RecordType_mobile_DomainWiseCount(self.domain_wise_count)
        }

class GetTrendChartDataSuccess(Response):
    def __init__(
        self, unit_wise_count
    ):
        self.unit_wise_count = unit_wise_count

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(
            data, [
                "unit_wise_count"
            ]
        )
        unit_wise_count = data.get("unit_wise_count")
        unit_wise_count = parse_structure_VectorType_RecordType_mobile_UnitWiseCount(unit_wise_count)
        return GetComplianceHistorySuccess(
            unit_wise_count
        )

    def to_inner_structure(self):
        return {
            "unit_wise_count": to_structure_VectorType_RecordType_mobile_UnitWiseCount(self.unit_wise_count)
        }

def _init_Response_class_map():
    classes = [
        UserLoginResponseSuccess,
        ClientUserLoginResponseSuccess,
        GetVersionsSuccess,
        GetUsersSuccess,
        GetUnitDetailsSuccess,
        GetTrendChartDataSuccess

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
        request = parse_structure_VariantType_mobile_Request(request)
        return RequestFormat(session_token, request)

    def to_structure(self):
        return {
            "session_token": to_structure_CustomTextType_50(self.session_token),
            "request": to_structure_VariantType_mobile_Request(self.request),
        }
