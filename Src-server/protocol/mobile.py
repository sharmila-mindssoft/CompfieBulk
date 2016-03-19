import json
from protocol.jsonvalidators import (parse_dictionary)
from protocol.parse_structure import (
    parse_structure_UnsignedIntegerType_32,
    parse_structure_OptionalType_VectorType_RecordType_core_FileList,
    parse_structure_OptionalType_CustomTextType_20,
    parse_structure_OptionalType_CustomTextType_500,
    parse_structure_Bool,
    parse_structure_CustomTextType_50
)
from protocol.to_structure import (
    to_structure_UnsignedIntegerType_32,
    to_structure_OptionalType_VectorType_RecordType_core_FileList,
    to_structure_OptionalType_CustomTextType_20,
    to_structure_OptionalType_CustomTextType_500,
    to_structure_Bool,
    to_structure_CustomTextType_50
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
    def __init__(
        self, group_id, unit_details_version, user_details_version,
        compliance_applicability_version, compliance_history_version,
        reassign_history_version
    ):
        self.group_id = group_id
		self.unit_details_version = unit_details_version
		self.user_details_version = user_details_version
		self.compliance_applicability_version = compliance_applicability_version
		self.compliance_history_version = compliance_history_version
		self.reassign_history_version = reassign_history_version

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(
            data, [
                "group_id", "unit_details_version", "user_details_version",
                "compliance_applicability_version", "compliance_history_version",
                "reassign_history_version"
            ]
        )
        group_id = data.get("group_id")
        group_id = parse_structure_UnsignedIntegerType_32(group_id)
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
        return GetVersions(
            group_id, unit_details_version, user_details_version,
            compliance_applicability_version, compliance_history_version,
            reassign_history_version
        )

    def to_inner_structure(self):
        return {
            "group_id": to_structure_UnsignedIntegerType_32(self.group_id),
            "unit_details_version": to_structure_UnsignedIntegerType_32(self.unit_details_version),
            "user_details_version": to_structure_UnsignedIntegerType_32(self.user_details_version),
            "compliance_applicability_version": to_structure_UnsignedIntegerType_32(self.compliance_applicability_version),
            "compliance_history_version": to_structure_UnsignedIntegerType_32(self.compliance_history_version),
            "reassign_history_version": to_structure_UnsignedIntegerType_32(self.reassign_history_version)
        }

class GetUsers(Request):
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
        return GetUsers(
            user_id, version
        )

    def to_inner_structure(self):
        return {
            "user_id": to_structure_UnsignedIntegerType_32(self.user_id),
            "version": to_structure_UnsignedIntegerType_32(self.version),
        }

class GetUnitDetails(Request):
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
        return GetUnitDetails(
            user_id, version
        )

    def to_inner_structure(self):
        return {
            "user_id": to_structure_UnsignedIntegerType_32(self.user_id),
            "version": to_structure_UnsignedIntegerType_32(self.version),
        }

class GetComplianceApplicabilityStatus(Request):
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
        return GetComplianceApplicabilityStatus(
            user_id, version
        )

    def to_inner_structure(self):
        return {
            "user_id": to_structure_UnsignedIntegerType_32(self.user_id),
            "version": to_structure_UnsignedIntegerType_32(self.version),
        }

class GetComplianceHistory(Request):
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
        return GetComplianceHistory(
            user_id, version
        )

    def to_inner_structure(self):
        return {
            "user_id": to_structure_UnsignedIntegerType_32(self.user_id),
            "version": to_structure_UnsignedIntegerType_32(self.version),
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
    classes = [GetUserGroups, SaveUserGroup, UpdateUserGroup, ChangeUserGroupStatus, GetUsers, SaveUser, UpdateUser, ChangeUserStatus]
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

class GetUsersSuccess(Response):
    def __init__(
        self, user_id, user_name
    ):
        self.user_id = user_id
        self.user_name = user_name

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(
            data, [
                "user_id", "user_name"
            ]
        )
        user_id = data.get("user_id")
        user_id = parse_structure_UnsignedIntegerType_32(user_id)
        user_name = data.get("user_name")
        user_name = parse_structure_CustomTextType_50(user_name)
        return GetUsersSuccess(
            user_id, user_name
        )

    def to_inner_structure(self):
        return {
            "user_id": to_structure_UnsignedIntegerType_32(self.user_id),
            "user_name": to_structure_CustomTextType_50(self.user_name)
        }

class GetUnitDetailsSuccess(Response):
    def __init__(
        self, unit_id, unit_name, country_id, country_name, domain_ids,
        domain_names, industry_id, industry_name, group_id, business_group_id,
        business_group_name, legal_entity_id, legal_entity_name, division_id,
        division_name
    ):
        self.unit_id = unit_id
        self.unit_name = unit_name
        self.country_id = country_id
        self.country_name = country_name
        self.domain_ids = domain_ids
        self.domain_names = domain_names
        self.industry_id = industry_id
        self.industry_name = industry_name
        self.group_id = group_id
        self.business_group_id = business_group_id
        self.business_group_name = business_group_name
        self.legal_entity_id = legal_entity_id
        self.legal_entity_name = legal_entity_name
        self.division_id = division_id
        self.division_name = division_name

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(
            data, [
                "unit_id", "unit_name", "country_id", "country_name", "domain_ids",
                "domain_names", "industry_id", "group_id", "business_group_id",
                "business_group_name", "legal_entity_id", "legal_entity_name",
                "division_id", "division_name"
            ]
        )
        unit_id = data.get("unit_id")
        unit_id = parse_structure_UnsignedIntegerType_32(unit_id)
        unit_name = data.get("unit_name")
        unit_name = parse_structure_CustomTextType_100(unit_name)
        country_id = data.get("country_id")
        country_id = parse_structure_UnsignedIntegerType_32(country_id)
        country_name = data.get("country_name")
        country_name = parse_structure_CustomTextType_100(country_name)
        domain_ids = data.get("domain_ids")
        domain_ids = parse_structure_VectorType_SignedIntegerType_8(domain_ids)
        domain_names = data.get("domain_names")
        domain_names = parse_structure_VectorType_CustomTextType_50(domain_names)
        industry_id = data.get("industry_id")
        industry_id = parse_structure_UnsignedIntegerType_32(industry_id)
        industry_name = data.get("industry_name")
        industry_name = parse_structure_CustomTextType_50(industry_name)
        group_id = data.get("group_id")
        group_id = parse_structure_UnsignedIntegerType_32(group_id)
        business_group_id = data.get("business_group_id")
        business_group_id = parse_structure_OptionalType_SignedIntegerType_8(business_group_id)
        business_group_name = data.get("business_group_name")
        business_group_name = parse_structure_CustomTextType_50(business_group_name)
        legal_entity_id = data.get("legal_entity_id")
        legal_entity_id = parse_structure_UnsignedIntegerType_32(legal_entity_id)
        legal_entity_name = data.get("legal_entity_name")
        legal_entity_name = parse_structure_CustomTextType_50(legal_entity_name)
        division_id = data.get("division_id")
        division_id = parse_structure_OptionalType_SignedIntegerType_8(division_id)
        division_name = data.get("division_name")
        division_name = parse_structure_CustomTextType_50(division_name)
        return GetUnitDetailsSuccess(
            unit_id, unit_name, country_id, country_name, domain_ids,
            domain_names, industry_id, industry_name, group_id, business_group_id,
            business_group_name, legal_entity_id, legal_entity_name, division_id,
            division_name
        )

    def to_structure(self):
        return {
            "unit_id" : to_structure_UnsignedIntegerType_32(self.unit_id),
            "unit_name" : to_structure_CustomTextType_100(self.unit_name),
            "country_id" : to_structure_UnsignedIntegerType_32(self.country_id),
            "country_name" : to_structure_CustomTextType_100(self.country_name),
            "domain_ids" : to_structure_VectorType_SignedIntegerType_8(self.domain_ids),
            "domain_names" : to_structure_VectorType_CustomTextType_50(self.domain_names),
            "industry_id" : to_structure_UnsignedIntegerType_32(self.industry_id),
            "industry_name" : to_structure_CustomTextType_50(self.industry_name),
            "group_id" : to_structure_UnsignedIntegerType_32(self.group_id),
            "business_group_id" : to_structure_OptionalType_SignedIntegerType_8(self.business_group_id),
            "business_group_name" : to_structure_CustomTextType_50(self.business_group_name),
            "legal_entity_id" : to_structure_UnsignedIntegerType_32(self.legal_entity_id),
            "legal_entity_name" : to_structure_CustomTextType_50(self.legal_entity_name),
            "division_id" : to_structure_OptionalType_SignedIntegerType_8(self.division_id),
            "division_name" : to_structure_CustomTextType_50(self.division_name)
        }

class ComplianceApplicability(object):
    def __init__(
        self, country_id, domain_id, unit_id, compliance_id, compliance_name,
        compliance_frequency, compliance_applicable, compliance_opted
    ):
        self.country_id = country_id
        self.domain_id = domain_id
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
        compliance_applicable = parse_structure_VectorType_SignedIntegerType_8(compliance_applicable)
        compliance_opted = data.get("compliance_opted")
        compliance_opted = parse_structure_VectorType_CustomTextType_50(compliance_opted)
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
            "compliance_applicable" : to_structure_VectorType_CustomTextType_50(self.compliance_applicable),
            "compliance_opted" : to_structure_CustomTextType_50(self.compliance_opted)
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
        return {
            "applicabilty_list": to_structure_VectorType_RecordType_mobile_ComplianceApplicability(self.applicabilty_list)
        }

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
        return {
            "compliance_history": to_structure_VectorType_RecordType_mobile_ComplianceHistory(self.compliance_history)
        }

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