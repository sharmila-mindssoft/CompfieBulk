from clientprotocol.jsonvalidators_client import (parse_dictionary, parse_static_list, to_structure_dictionary_values)
from clientprotocol.parse_structure import (
    parse_structure_VectorType_RecordType_clienttransactions_STATUTORY_WISE_COMPLIANCES,
    parse_structure_VectorType_RecordType_clienttransactions_ASSIGN_COMPLIANCE_USER,
    parse_structure_VectorType_RecordType_core_ClientBusinessGroup,
    parse_structure_VectorType_RecordType_clienttransactions_REASSIGNED_COMPLIANCE,
    parse_structure_VectorType_RecordType_clienttransactions_USER_WISE_UNITS,
    parse_structure_CustomTextType_500,
    parse_structure_VectorType_RecordType_clienttransactions_PAST_RECORD_COMPLIANCE,
    parse_structure_VectorType_RecordType_core_Country,
    parse_structure_VectorType_RecordType_clienttransactions_ASSIGN_COMPLIANCE_UNITS,
    parse_structure_VectorType_RecordType_clienttransactions_APPROVALCOMPLIANCE,
    parse_structure_CustomTextType_50,
    parse_structure_VariantType_clienttransactions_Request,
    parse_structure_VectorType_SignedIntegerType_8,
    parse_structure_VectorType_RecordType_core_ClientDivision,
    parse_structure_VectorType_RecordType_core_StatutoryDate,
    parse_structure_VectorType_RecordType_clienttransactions_APPORVALCOMPLIANCELIST,
    parse_structure_CustomTextType_250,
    parse_structure_EnumType_core_COMPLIANCE_APPROVAL_STATUS,
    parse_structure_VectorType_RecordType_core_ClientLegalEntity,
    parse_structure_VectorType_RecordType_core_Domain,
    parse_structure_EnumType_core_COMPLIANCE_FREQUENCY,
    parse_structure_CustomTextType_20,
    parse_structure_VectorType_RecordType_clienttransactions_ComplianceApplicability,
    parse_structure_Bool,
    parse_structure_OptionalType_CustomTextType_500,
    parse_structure_VectorType_RecordType_clienttransactions_UpdateStatutoryCompliance,
    parse_structure_VectorType_RecordType_core_ComplianceFrequency,
    parse_structure_CustomTextType_100,
    parse_structure_OptionalType_CustomTextType_20,
    parse_structure_OptionalType_UnsignedIntegerType_32,
    parse_structure_OptionalType_VectorType_RecordType_core_StatutoryDate,
    parse_structure_OptionalType_VectorType_RecordType_core_FileList,
    parse_structure_VectorType_CustomTextType_100,
    parse_structure_MapType_CustomTextType_100_VectorType_RecordType_clienttransactions_STATUTORYWISECOMPLIANCE,
    parse_structure_MapType_SignedIntegerType_8_VectorType_RecordType_clienttransactions_USER_WISE_COMPLIANCE,
    parse_structure_OptionalType_SignedIntegerType_8,
    parse_structure_VectorType_RecordType_clienttransactions_UNIT_WISE_STATUTORIES_FOR_PAST_RECORDS,
    parse_structure_OptionalType_CustomTextType_100,
    parse_structure_OptionalType_EnumType_core_COMPLIANCE_FREQUENCY,
    parse_structure_UnsignedIntegerType_32,
    parse_structure_VectorType_RecordType_core_User,
    parse_structure_OptionalType_VectorType_CustomTextType_20,
    parse_structure_VectorType_RecordType_core_COMPLIANCE_APPROVAL_STATUS,
    parse_structure_OptionalType_VectorType_CustomTextType_500,
    parse_structure_VectorType_RecordType_clienttransactions_PastRecordUnits,
    parse_structure_MapType_CustomTextType_50_VectorType_CustomTextType_500,
    parse_structure_VectorType_UnsignedIntegerType_32,
    parse_structure_OptionalType_VectorType_UnsignedIntegerType_32,
    parse_structure_OptionalType_VectorType_RecordType_clienttransactions_NewUnitSettings,
    parse_structure_Text,
    parse_structure_MapType_CustomTextType_100_VectorType_RecordType_clienttransactions_UNIT_WISE_STATUTORIES,
    parse_structure_MapType_UnsignedIntegerType_32_UnsignedIntegerType_32,
    parse_structure_OptionalType_Smallvalue
)
from clientprotocol.to_structure import (
    to_structure_SignedIntegerType_8,
    to_structure_VectorType_RecordType_clienttransactions_STATUTORY_WISE_COMPLIANCES,
    to_structure_VectorType_RecordType_clienttransactions_ASSIGN_COMPLIANCE_USER,
    to_structure_VectorType_RecordType_core_ClientBusinessGroup,
    to_structure_VectorType_RecordType_clienttransactions_REASSIGNED_COMPLIANCE,
    to_structure_VectorType_RecordType_clienttransactions_USER_WISE_UNITS,
    to_structure_CustomTextType_500,
    to_structure_VectorType_RecordType_clienttransactions_PAST_RECORD_COMPLIANCE,
    to_structure_VectorType_RecordType_core_Country,
    to_structure_VectorType_RecordType_clienttransactions_APPROVALCOMPLIANCE,
    to_structure_CustomTextType_50,
    to_structure_VariantType_clienttransactions_Request,
    to_structure_VectorType_CustomTextType_50,
    to_structure_VectorType_RecordType_core_ClientDivision,
    to_structure_VectorType_RecordType_core_StatutoryDate,
    to_structure_VectorType_RecordType_clienttransactions_APPORVALCOMPLIANCELIST,
    to_structure_CustomTextType_250,
    to_structure_EnumType_core_COMPLIANCE_APPROVAL_STATUS,
    to_structure_VectorType_RecordType_core_ClientLegalEntity,
    to_structure_VectorType_RecordType_core_Domain,
    to_structure_EnumType_core_COMPLIANCE_FREQUENCY,
    to_structure_CustomTextType_20,
    to_structure_VectorType_RecordType_clienttransactions_ComplianceApplicability,
    to_structure_Bool,
    to_structure_OptionalType_CustomTextType_500,
    to_structure_VectorType_RecordType_clienttransactions_UpdateStatutoryCompliance,
    to_structure_UnsignedIntegerType_32,
    to_structure_CustomTextType_100,
    to_structure_OptionalType_CustomTextType_20,
    to_structure_VectorType_RecordType_client_transactions_IndustryWiseUnits,
    to_structure_OptionalType_UnsignedIntegerType_32,
    to_structure_OptionalType_CustomTextType_50,
    to_structure_VectorType_RecordType_core_ComplianceFrequency,
    to_structure_OptionalType_SignedIntegerType_8,
    to_structure_OptionalType_VectorType_RecordType_core_StatutoryDate,
    to_structure_VectorType_CustomTextType_100,
    to_structure_MapType_CustomTextType_100_VectorType_RecordType_clienttransactions_STATUTORYWISECOMPLIANCE,
    to_structure_MapType_SignedIntegerType_8_VectorType_RecordType_clienttransactions_USER_WISE_COMPLIANCE,
    to_structure_VectorType_RecordType_clienttransactions_UNIT_WISE_STATUTORIES_FOR_PAST_RECORDS,
    to_structure_OptionalType_CustomTextType_100,
    to_structure_OptionalType_EnumType_core_COMPLIANCE_FREQUENCY,
    to_structure_VectorType_RecordType_core_User,
    to_structure_OptionalType_VectorType_RecordType_core_FileList,
    to_structure_OptionalType_VectorType_CustomTextType_20,
    to_structure_VectorType_RecordType_core_COMPLIANCE_APPROVAL_STATUS,
    to_structure_OptionalType_VectorType_CustomTextType_500,
    to_structure_VectorType_RecordType_clienttransactions_PastRecordUnits,
    to_structure_VectorType_UnsignedIntegerType_32,
    to_structure_MapType_CustomTextType_50_VectorType_CustomTextType_500,
    to_structure_OptionalType_VectorType_UnsignedIntegerType_32,
    to_structure_OptionalType_VectorType_RecordType_clienttransactions_NewUnitSettings,
    to_structure_Text,
    to_structure_MapType_CustomTextType_100_VectorType_RecordType_clienttransactions_UNIT_WISE_STATUTORIES,
    to_structure_VectorType_RecordType_clienttransactions_ASSIGN_COMPLIANCE_UNITS,
    to_structure_MapType_UnsignedIntegerType_32_UnsignedIntegerType_32,
    to_structure_OptionalType_Smallvalue
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

#
# Statutory Settings Request
#
class GetStatutorySettingsFilters(Request):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return GetStatutorySettingsFilters()

    def to_inner_structure(self):
        return {
        }

class GetStatutorySettings(Request):
    def __init__(self, legal_entity_id, division_id, category_id):
        self.legal_entity_id = legal_entity_id
        self.division_id = division_id
        self.category_id = category_id

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["le_id", "div_id", "cat_id"])
        return GetStatutorySettings(
            data.get("le_id"), data.get("div_id"), data.get("cat_id")
        )

    def to_inner_structure(self):
        return {
            "le_id": self.legal_entity_id,
            "div_id": self.division_id,
            "cat_id": self.category_id
        }

class ChangeStatutorySettingsLock(Request):
    def __init__(self, legal_entity_id, domain_id, unit_id, lock, password):
        self.legal_entity_id = legal_entity_id
        self.domain_id = domain_id
        self.unit_id = unit_id
        self.lock = lock
        self.password = password

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["le_id", "d_id", "u_id", "lock", "password"])
        return ChangeStatutorySettingsLock(
            data.get("le_id"), data.get("d_id"), data.get("u_id"),
            data.get("lock"), data.get("password")
        )

    def to_inner_structure(self):
        return {
            "le_id": self.legal_entity_id,
            "d_id": self.domain_id,
            "u_id": self.unit_id,
            "lock": self.lock,
            "password": self.password
        }

class GetSettingsCompliances(Request):
    def __init__(self, legal_entity_id, unit_id, domain_id, frequency_id, record_count):
        self.legal_entity_id = legal_entity_id
        self.unit_id = unit_id
        self.record_count = record_count
        self.domain_id = domain_id
        self.frequency_id = frequency_id

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["le_id", "u_ids", "d_id", "r_count"])
        legal_entity_id = data.get("le_id")
        unit_id = data.get("u_ids")
        record_count = data.get("r_count")
        domain_id = data.get("d_id")
        frequency_id = data.get("f_id")
        return GetSettingsCompliances(
            legal_entity_id, unit_id, domain_id, frequency_id, record_count
        )

    def to_inner_structure(self):
        return {
            "le_id": self.legal_entity_id,
            "u_ids": self.unit_id,
            "r_count": self.record_count,
            "d_id": self.domain_id,
            "f_id": self.frequency_id
        }

class ApplicableCompliance(object):
    def __init__(self, compliance_id, compliance_opted_status, compliance_remarks):
        self.compliance_id = compliance_id
        self.compliance_opted_status = compliance_opted_status
        self.compliance_remarks = compliance_remarks

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["compliance_id", "compliance_opted_status", "compliance_remarks"])
        compliance_id = data.get("compliance_id")
        compliance_id = parse_structure_UnsignedIntegerType_32(compliance_id)
        compliance_opted_status = data.get("compliance_opted_status")
        compliance_opted_status = parse_structure_Bool(compliance_opted_status)
        compliance_remarks = data.get('compliance_remarks')
        compliance_remarks = parse_structure_OptionalType_CustomTextType_500(compliance_remarks)
        return ApplicableCompliance(compliance_id, compliance_opted_status, compliance_remarks)

    def to_structure(self):
        return {
            "compliance_id": to_structure_UnsignedIntegerType_32(self.compliance_id),
            "compliance_opted_status": to_structure_Bool(self.compliance_opted_status),
            "compliance_remarks": to_structure_OptionalType_CustomTextType_500(self.compliance_remarks)
        }

class UpdateStatutoryCompliance(object):
    def __init__(
        self, client_compliance_id,
        applicable_status, not_applicable_remarks,
        compliance_id, compliance_opted_status, compliance_remarks,
        unit_name, unit_id
    ):
        self.client_compliance_id = client_compliance_id
        self.applicable_status = applicable_status
        self.not_applicable_remarks = not_applicable_remarks
        self.compliance_id = compliance_id
        self.compliance_opted_status = compliance_opted_status
        self.compliance_remarks = compliance_remarks
        self.unit_name = unit_name
        self.unit_id = unit_id

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "c_c_id", "a_status", "n_a_remarks",
            "comp_id", "c_o_status", "c_remarks",
            "u_name", "u_id",
        ])
        client_compliance_id = data.get("c_c_id")
        applicable_status = data.get("a_status")
        not_applicable_remarks = data.get("n_a_remarks")
        compliance_id = data.get("comp_id")
        compliance_opted_status = data.get("c_o_status")
        compliance_remarks = data.get('c_remarks')
        unit_name = data.get("u_name")
        unit_id = data.get("u_id")
        return UpdateStatutoryCompliance(
            client_compliance_id, applicable_status, not_applicable_remarks,
            compliance_id, compliance_opted_status, compliance_remarks,
            unit_name, unit_id
        )

    def to_structure(self):
        return {
            "c_c_id": self.client_compliance_id,
            "a_status": self.applicable_status,
            "n_a_remarks": self.not_applicable_remarks,
            "comp_id": self.compliance_id,
            "c_o_status": self.compliance_opted_status,
            "c_remarks": self.compliance_remarks,
            "u_name": self.unit_name,
            "u_id": self.unit_id,
        }


class UpdateStatutorySettings(Request):
    def __init__(
        self, password, statutories,
        legal_entity_id, s_s, domain_id, unit_ids
    ):
        self.password = password
        self.statutories = statutories
        self.legal_entity_id = legal_entity_id
        self.s_s = s_s
        self.domain_id = domain_id
        self.unit_ids = unit_ids

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "password", "update_statutories", "le_id", "s_s", "d_id", "u_ids"
        ])
        password = data.get("password")
        statutories = data.get("update_statutories")
        legal_entity_id = data.get("le_id")
        s_s = data.get("s_s")
        domain_id = data.get("d_id")
        unit_ids = data.get("u_ids")
        return UpdateStatutorySettings(
            password, statutories, legal_entity_id, s_s,
            domain_id, unit_ids
        )

    def to_inner_structure(self):
        return {
            "password": self.password,
            "update_statutories": self.statutories,
            "le_id": self.legal_entity_id,
            "s_s": self.s_s,
            "d_id": self.domain_id,
            "u_ids": self.unit_ids
        }


#
# Assign Compliance Request
#

class GetAssignCompliancesFormData(Request):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return GetAssignCompliancesFormData()

    def to_inner_structure(self):
        return {}

class GetAssignComplianceUnits(Request):
    def __init__(self, legal_entity_id, domain_id):
        self.legal_entity_id = legal_entity_id
        self.domain_id = domain_id

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["le_id", "d_id"])
        return GetAssignComplianceUnits(
            data.get("le_id"),
            data.get("d_id")
        )

    def to_inner_structure(self):
        return {
            "le_id": self.legal_entity_id,
            "d_id": self.domain_id
        }


class GetUserToAssignCompliance(Request):
    def __init__(self, legal_entity_id, unit_ids, domain_id):
        self.unit_ids = unit_ids
        self.domain_id = domain_id
        self.legal_entity_id = legal_entity_id

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["u_ids", "d_id", "le_id"])
        unit_ids = data.get("u_ids")
        domain_id = data.get("d_id")
        legal_entity_id = data.get("le_id")
        return GetUserToAssignCompliance(legal_entity_id, unit_ids, domain_id)

    def to_inner_structure(self):
        return {
            "u_ids": self.unit_ids,
            "d_id": self.domain_id,
            "le_id": self.legal_entity_id
        }

class GetComplianceTotalToAssign(Request):
    def __init__(self, legal_entity_id, unit_ids, domain_id):
        self.legal_entity_id = legal_entity_id
        self.unit_ids = unit_ids
        self.domain_id = domain_id

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["le_id", "u_ids", "d_id"])
        legal_entity_id = data.get("le_id")
        unit_ids = data.get("u_ids")
        domain_id = data.get("d_id")
        return GetComplianceTotalToAssign(legal_entity_id, unit_ids, domain_id)

    def to_inner_structure(self):
        return {
            "le_id": self.legal_entity_id,
            "u_ids": self.unit_ids,
            "d_id": self.domain_id,
        }

class GetComplianceForUnits(Request):
    def __init__(self, legal_entity_id, unit_ids, domain_id, record_count, frequency_ids):
        self.legal_entity_id = legal_entity_id
        self.unit_ids = unit_ids
        self.domain_id = domain_id
        self.record_count = record_count
        self.frequency_ids = frequency_ids

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["le_id", "u_ids", "d_id", "f_ids"])
        legal_entity_id = data.get("le_id")
        unit_ids = data.get("u_ids")
        domain_id = data.get("d_id")
        record_count = data.get("r_count")
        frequency_ids = data.get("f_ids")
        return GetComplianceForUnits(legal_entity_id, unit_ids, domain_id, record_count, frequency_ids)

    def to_inner_structure(self):
        return {
            "le_id": self.legal_entity_id,
            "u_ids": self.unit_ids,
            "d_id": self.domain_id,
            "r_count": self.record_count,
            "f_ids": self.frequency_ids
        }

class NewUnitSettings(object):
    def __init__(self, user_id, unit_ids, domain_id, country_id):
        self.user_id = user_id
        self.unit_ids = unit_ids
        self.domain_id = domain_id
        self.country_id = country_id

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "user_id", "u_ids", "d_ids", "c_ids"
        ])
        user_id = data.get("user_id")
        user_id = parse_structure_UnsignedIntegerType_32(user_id)
        unit_ids = data.get("u_ids")
        unit_ids = parse_structure_OptionalType_VectorType_UnsignedIntegerType_32(unit_ids)
        domain_id = data.get("d_ids")
        domain_id = parse_structure_OptionalType_VectorType_UnsignedIntegerType_32(domain_id)
        country_id = data.get("c_ids")
        country_id = parse_structure_OptionalType_VectorType_UnsignedIntegerType_32(country_id)
        return NewUnitSettings(user_id, unit_ids, domain_id, country_id)

    def to_structure(self):
        return {
            "user_id": to_structure_UnsignedIntegerType_32(self.user_id),
            "u_ids": to_structure_OptionalType_VectorType_UnsignedIntegerType_32(self.unit_ids),
            "d_ids": to_structure_OptionalType_VectorType_UnsignedIntegerType_32(self.domain_id),
            "c_ids": to_structure_OptionalType_VectorType_UnsignedIntegerType_32(self.country_id)
        }

class SaveAssignedCompliance(Request):
    def __init__(
        self, assignee, assignee_name,
        concurrence_person, concurrence_person_name,
        approval_person, approval_person_name,
        compliances, legal_entity_id, domain_id,

    ):
        self.assignee = assignee
        self.assignee_name = assignee_name
        self.concurrence_person = concurrence_person
        self.concurrence_person_name = concurrence_person_name
        self.approval_person = approval_person
        self.approval_person_name = approval_person_name
        self.compliances = compliances
        self.legal_entity_id = legal_entity_id
        self.domain_id = domain_id

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "assignee", "assignee_name",
            "concurrence_person", "concurrer_name",
            "approval_person", "approver_name", "assign_compliances",
            "le_id", "d_id"
        ])
        assignee = data.get("assignee")
        assignee_name = data.get("assignee_name")
        concurrence_person = data.get("concurrence_person")
        concurrence_person_name = data.get("concurrer_name")
        approval_person = data.get("approval_person")
        approval_person_name = data.get("approver_name")
        compliances = data.get("assign_compliances")
        legal_entity_id = data.get("le_id")
        domain_id = data.get("d_id")
        return SaveAssignedCompliance(
            assignee, assignee_name,
            concurrence_person, concurrence_person_name,
            approval_person, approval_person_name,
            compliances, legal_entity_id, domain_id
        )

    def to_inner_structure(self):
        return {
            "assignee": self.assignee,
            "assignee_name": self.assignee_name,
            "concurrence_person": self.concurrence_person,
            "concurrer_name": self.concurrence_person_name,
            "approval_person": self.approval_person,
            "approver_name": self.approval_person_name,
            "assign_compliances": self.compliances,
            "le_id": self.legal_entity_id,
            "d_id": self.domain_id
        }

class GetUserwiseCompliances(Request):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return GetUserwiseCompliances()

    def to_inner_structure(self):
        return {
        }

class GetAssigneeCompliances(Request):
    def __init__(self, assignee, record_count):
        self.assignee = assignee
        self.record_count = record_count

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["assignee", "record_count"])
        assignee = data.get("assignee")
        assignee = parse_structure_UnsignedIntegerType_32(assignee)
        record_count = data.get("record_count")
        record_count = parse_structure_UnsignedIntegerType_32(record_count)
        return GetAssigneeCompliances(assignee, record_count)

    def to_inner_structure(self):
        return {
            "assignee": to_structure_UnsignedIntegerType_32(self.assignee),
            "record_count": to_structure_UnsignedIntegerType_32(self.record_count)
        }

class ReassignCompliance(Request):
    def __init__(self, legal_entity_id, r_from, assignee, assignee_name, concurrence_person, approval_person, reassigned_compliance, reason):
        self.legal_entity_id = legal_entity_id
        self.r_from = r_from
        self.assignee = assignee
        self.assignee_name = assignee_name
        self.concurrence_person = concurrence_person
        self.approval_person = approval_person
        self.reassigned_compliance = reassigned_compliance
        self.reason = reason

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "le_id", "r_from", "assignee", "assignee_name",
            "concurrence_person", "approval_person", "reassigned_compliance", "reason"
        ])

        return ReassignCompliance(
            data.get("le_id"),
            data.get("r_from"),
            data.get("assignee"),
            data.get("assignee_name"),
            data.get("concurrence_person"),
            data.get("approval_person"),
            data.get("reassigned_compliance"),
            data.get("reason")
        )

    def to_inner_structure(self):
        return {
            "le_id": self.legal_entity_id,
            "r_from": self.r_from,
            "assignee": self.assignee,
            "assignee_name": self.assignee_name,
            "concurrence_person": self.concurrence_person,
            "approval_person": self.approval_person,
            "reassigned_compliance": self.reassigned_compliance,
            "reason": self.reason
        }
#########################################################
# Get Compliance Approval List
#########################################################
class GetComplianceApprovalList(Request):
    def __init__(self, legal_entity_id, start_count):
        self.legal_entity_id = legal_entity_id
        self.start_count = start_count

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["le_id", "start_count"])
        legal_entity_id = data.get("le_id")
        start_count = data.get("start_count")
        return GetComplianceApprovalList(legal_entity_id, start_count)

    def to_inner_structure(self):
        return {
            "le_id": self.legal_entity_id,
            "start_count": self.start_count
        }
#########################################################
# Approval Compliance
#########################################################
class ApproveCompliance(Request):
    def __init__(
        self, legal_entity_id, compliance_history_id, approval_status, remarks,
        next_due_date, validity_date
    ):
        self.legal_entity_id = legal_entity_id
        self.compliance_history_id = compliance_history_id
        self.approval_status = approval_status
        self.remarks = remarks
        self.next_due_date = next_due_date
        self.validity_date = validity_date

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(
            data, [
                "le_id","compliance_history_id", "approval_status",
                "remarks",  "next_due_date", "validity_date"
            ]
        )
        legal_entity_id = data.get("le_id")
        compliance_history_id = data.get("compliance_history_id")
        # compliance_history_id = parse_structure_UnsignedIntegerType_32(compliance_history_id)
        approval_status = data.get("approval_status")
        # approval_status = parse_structure_EnumType_core_COMPLIANCE_APPROVAL_STATUS(approval_status)
        remarks = data.get("remarks")
        # remarks = parse_structure_OptionalType_CustomTextType_500(remarks)
        next_due_date = data.get("next_due_date")
        # next_due_date = parse_structure_OptionalType_CustomTextType_20(next_due_date)
        validity_date = data.get("validity_date")
        # validity_date = parse_structure_OptionalType_CustomTextType_20(validity_date)
        return ApproveCompliance(
            legal_entity_id, compliance_history_id, approval_status, remarks,
            next_due_date, validity_date
                            )

    def to_inner_structure(self):
        return {
            "le_id": self.legal_entity_id,
            "compliance_history_id": self.compliance_history_id,
            "approval_status": self.approval_status,
            "remarks": self.remarks,
            "next_due_date": self.next_due_date,
            "validity_date": self.validity_date
        }

####################################################
# Get Completed Task Current Year (Past Data) 
####################################################
class GetPastRecordsFormData(Request):
    def __init__(self, legal_entity_id):
        self.legal_entity_id = legal_entity_id

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data,["le_id"])
        legal_entity_id = data.get("le_id")
        return GetPastRecordsFormData(legal_entity_id)

    def to_inner_structure(self):
        return {
            "le_id": self.legal_entity_id
        }

class GetStatutoriesByUnit(Request):
    def __init__(
        self, unit_id, domain_id, level_1_statutory_name,
        compliance_frequency, country_id, start_count
    ):
        self.unit_id = unit_id
        self.domain_id = domain_id
        self.level_1_statutory_name = level_1_statutory_name
        self.compliance_frequency = compliance_frequency
        self.country_id = country_id
        self.start_count = start_count

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["unit_id", "domain_id",
            "level_1_statutory_name", "compliance_frequency",
            "country_id", "start_count"])
        unit_id = data.get("unit_id")
        unit_id = parse_structure_UnsignedIntegerType_32(unit_id)
        domain_id = data.get("domain_id")
        domain_id = parse_structure_UnsignedIntegerType_32(domain_id)
        level_1_statutory_name = data.get("level_1_statutory_name")
        level_1_statutory_name = parse_structure_OptionalType_CustomTextType_100(level_1_statutory_name)
        compliance_frequency = data.get("compliance_frequency")
        compliance_frequency = parse_structure_OptionalType_EnumType_core_COMPLIANCE_FREQUENCY(compliance_frequency)
        country_id = data.get("country_id")
        country_id = parse_structure_UnsignedIntegerType_32(country_id)
        start_count = data.get("start_count")
        start_count = parse_structure_UnsignedIntegerType_32(start_count)
        return GetStatutoriesByUnit(
            unit_id, domain_id, level_1_statutory_name,
            compliance_frequency, country_id, start_count
        )

    def to_inner_structure(self):
        return {
            "unit_id": to_structure_SignedIntegerType_8(self.unit_id),
            "domain_id": to_structure_SignedIntegerType_8(self.domain_id),
            "level_1_statutory_name": to_structure_OptionalType_CustomTextType_100(self.level_1_statutory_name),
            "compliance_frequency": to_structure_OptionalType_EnumType_core_COMPLIANCE_FREQUENCY(self.compliance_frequency),
            "country_id": to_structure_UnsignedIntegerType_32(self.country_id),
            "start_count": to_structure_UnsignedIntegerType_32(self.start_count)
        }


class SavePastRecords(Request):
    def __init__(self, compliances):
        self.compliances = compliances

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["compliances"])
        compliances = data.get("compliances")
        compliances = parse_structure_VectorType_RecordType_clienttransactions_PAST_RECORD_COMPLIANCE(compliances)
        return SavePastRecords(compliances)

    def to_inner_structure(self):
        return {
            "compliances": to_structure_VectorType_RecordType_clienttransactions_PAST_RECORD_COMPLIANCE(self.compliances),
        }


class GetReviewSettingsFilters(Request):
    def __init__(self, legal_entity_id):
        self.legal_entity_id = legal_entity_id

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["le_id"])
        legal_entity_id = data.get("le_id")
        return GetReviewSettingsFilters(legal_entity_id)

    def to_inner_structure(self):
        return {
            "le_id": self.legal_entity_id
        }


class GetReviewSettingsUnitFilters(Request):
    def __init__(self, legal_entity_id, domain_id):
        self.legal_entity_id = legal_entity_id
        self.domain_id = domain_id

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["le_id", "d_id"])
        legal_entity_id = data.get("le_id")
        domain_id = data.get("d_id")
        return GetReviewSettingsUnitFilters(legal_entity_id, domain_id)

    def to_inner_structure(self):
        return {
            "le_id": self.legal_entity_id,
            "d_id": self.domain_id
        }


class GetReviewSettingsComplianceFilters(Request):
    def __init__(self, legal_entity_id, domain_id, unit_ids, f_id, sno):
        self.legal_entity_id = legal_entity_id
        self.domain_id = domain_id
        self.unit_ids = unit_ids
        self.f_id = f_id
        self.sno = sno

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["le_id", "d_id", "unit_ids", "f_id", "sno"])
        legal_entity_id = data.get("le_id")
        domain_id = data.get("d_id")
        unit_ids = data.get("unit_ids")
        f_id = data.get("f_id")
        sno = data.get("sno")
        return GetReviewSettingsComplianceFilters(legal_entity_id, domain_id, unit_ids, f_id, sno)

    def to_inner_structure(self):
        return {
            "le_id": self.legal_entity_id,
            "d_id": self.domain_id,
            "unit_ids": self.unit_ids,
            "f_id": self.f_id,
            "sno": self.sno
        }


class SaveReviewSettingsCompliance(Request):
    def __init__(self, rs_compliances):
        self.rs_compliances = rs_compliances

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["compliances"])
        rs_compliances = data.get("compliances")
        return SaveReviewSettingsCompliance(rs_compliances)

    def to_inner_structure(self):
        return {
            "compliances": self.rs_compliances
        }


class SaveReviewSettingsComplianceDict(Request):
    def __init__(
        self, legal_entity_id, domain_id, f_id, unit_ids, compliance_id, repeat_by,
        repeat_type_id, due_date, trigger_before_days, statu_dates, old_repeat_by,
        old_repeat_type_id, old_due_date, old_statu_dates
    ):
        self.legal_entity_id = legal_entity_id
        self.domain_id = domain_id
        self.f_id = f_id
        self.unit_ids = unit_ids
        self.compliance_id = compliance_id
        self.repeat_by = repeat_by
        self.repeat_type_id = repeat_type_id
        self.due_date = due_date
        self.statu_dates = statu_dates
        self.trigger_before_days = trigger_before_days
        self.old_repeat_by = old_repeat_by
        self.old_repeat_type_id = old_repeat_type_id
        self.old_due_date = old_due_date
        self.old_statu_dates = old_statu_dates

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "le_id", "d_id",  "f_id", "unit_ids", "comp_id", "r_every",
            "repeat_type_id", "due_date", "trigger_before_days", "statu_dates",
            "old_repeat_by", "old_repeat_type_id", "old_due_date", "old_statu_dates"
            ])
        legal_entity_id = data.get("le_id")
        domain_id = data.get("d_id")
        f_id = data.get("f_id")
        unit_ids = data.get("unit_ids")
        comp_id = data.get("comp_id")
        r_every = data.get("r_every")
        repeat_type_id = data.get("repeat_type_id")
        due_date = data.get("due_date")
        trigger_before_days = data.get("trigger_before_days")
        statu_dates = data.get("statu_dates")
        old_repeat_by = data.get("old_repeat_by")
        old_repeat_type_id = data.get("old_repeat_type_id")
        old_due_date = data.get("old_due_date")
        old_statu_dates = data.get("old_statu_dates")

        return SaveReviewSettingsComplianceDict(
            legal_entity_id, domain_id, unit_ids, f_id, comp_id,
            r_every, repeat_type_id, due_date, trigger_before_days, statu_dates,
            old_repeat_by, old_repeat_type_id, old_due_date, old_statu_dates
            )

    def to_inner_structure(self):
        return {
            "le_id": self.legal_entity_id,
            "d_id": self.domain_id,
            "f_id": self.f_id,
            "unit_ids": self.unit_ids,
            "comp_id": self.comp_id,
            "r_every": self.r_every,
            "repeat_type_id": self.repeat_type_id,
            "due_date": self.due_date,
            "trigger_before_days": self.trigger_before_days,
            "statu_dates": self.statu_dates,
            "old_repeat_by": self.old_repeat_by,
            "old_repeat_type_id": self.old_repeat_type_id,
            "old_due_date": self.old_due_date,
            "old_statu_dates": self.old_statu_dates,
        }

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

class GetReassignComplianceFilters(Request):
    def __init__(self, legal_entity_id):
        self.legal_entity_id = legal_entity_id

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["le_id"])
        legal_entity_id = data.get("le_id")
        return GetReassignComplianceFilters(legal_entity_id)

    def to_inner_structure(self):
        return {
            "le_id": self.legal_entity_id
        }

class GetReAssignComplianceUnits(Request):
    def __init__(self, legal_entity_id, d_id, usr_id, user_type_id, unit_id):
        self.legal_entity_id = legal_entity_id
        self.d_id = d_id
        self.usr_id = usr_id
        self.user_type_id = user_type_id
        self.unit_id = unit_id

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["le_id", "d_id", "usr_id", "user_type_id", "unit_id"])
        return GetReAssignComplianceUnits(
            data.get("le_id"),
            data.get("d_id"),
            data.get("usr_id"),
            data.get("user_type_id"),
            data.get("unit_id")
        )

    def to_inner_structure(self):
        return {
            "le_id": self.legal_entity_id,
            "d_id": self.d_id,
            "usr_id": self.usr_id,
            "user_type_id": self.user_type_id,
            "unit_id": self.unit_id
        }


class GetReAssignComplianceForUnits(Request):
    def __init__(self, legal_entity_id, d_id, usr_id, user_type_id, u_ids, r_count):
        self.legal_entity_id = legal_entity_id
        self.d_id = d_id
        self.usr_id = usr_id
        self.user_type_id = user_type_id
        self.u_ids = u_ids
        self.r_count = r_count

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["le_id", "d_id", "usr_id", "user_type_id", "u_ids", "r_count"])
        return GetReAssignComplianceForUnits(
            data.get("le_id"),
            data.get("d_id"),
            data.get("usr_id"),
            data.get("user_type_id"),
            data.get("u_ids"),
            data.get("r_count")
        )

    def to_inner_structure(self):
        return {
            "le_id": self.legal_entity_id,
            "d_id": self.d_id,
            "usr_id": self.usr_id,
            "user_type_id": self.user_type_id,
            "u_ids": self.u_ids,
            "r_count": self.r_count
        }


class GetReAssignComplianceForUnits(Request):
    def __init__(self, legal_entity_id, d_id, usr_id, user_type_id, u_ids, r_count):
        self.legal_entity_id = legal_entity_id
        self.d_id = d_id
        self.usr_id = usr_id
        self.user_type_id = user_type_id
        self.u_ids = u_ids
        self.r_count = r_count

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["le_id", "d_id", "usr_id", "user_type_id", "u_ids", "r_count"])
        return GetReAssignComplianceForUnits(
            data.get("le_id"),
            data.get("d_id"),
            data.get("usr_id"),
            data.get("user_type_id"),
            data.get("u_ids"),
            data.get("r_count")
        )

    def to_inner_structure(self):
        return {
            "le_id": self.legal_entity_id,
            "d_id": self.d_id,
            "usr_id": self.usr_id,
            "user_type_id": self.user_type_id,
            "u_ids": self.u_ids,
            "r_count": self.r_count
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


class GetUserWidgetData(Request):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [])
        return GetUserWidgetData()

    def to_inner_structure(self):
        return {}

class WidgetInfo(object):
    def __init__(self, widget_id, width, height, pin_status):
        self.widget_id = widget_id
        self.width = width
        self.height = height
        self.pin_status = pin_status

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["w_id", "width", "height", "pin_status"])
        return WidgetInfo(
            data.get("w_id"), data.get("width"),
            data.get("height"), data.get("pin_status")
        )

    def to_structure(self):
        return {
            "w_id": self.widget_id,
            "width": self.width,
            "height": self.height,
            "pin_status": self.pin_status
        }

class WidgetList(object):
    def __init__(self, widget_id, widget_name, active_status):
        self.widget_id = widget_id
        self.widget_name = widget_name
        self.active_status = active_status

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["w_id", "w_name", "active_status"])
        return WidgetList(
            data.get("w_id"), data.get("w_name"),
            data.get("active_status")
        )

    def to_structure(self):
        return {
            "w_id": self.widget_id,
            "w_name": self.widget_name,
            "active_status": self.active_status
        }


class SaveWidgetData(Request):
    def __init__(self, widget_data):
        self.widget_data = widget_data

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["widget_info"])
        return SaveWidgetData(data.get("widget_info"))

    def to_inner_structure(self):
        return {
            "widget_info": self.widget_data
        }

class ChangeThemes(Request):
    def __init__(self, theme):
        self.theme = theme

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["theme"])
        theme = data.get("theme")
        return ChangeThemes(theme)

    def to_inner_structure(self):
        return {
            "theme": self.theme
        }


def _init_Request_class_map():

    classes = [
        GetStatutorySettingsFilters, ChangeStatutorySettingsLock,
        GetStatutorySettings, GetSettingsCompliances, UpdateStatutorySettings,
        GetAssignCompliancesFormData, GetComplianceForUnits, SaveAssignedCompliance,
        GetUserwiseCompliances, GetAssigneeCompliances, ReassignCompliance,
        GetComplianceApprovalList, ApproveCompliance, GetPastRecordsFormData,
        GetStatutoriesByUnit, SavePastRecords, GetReviewSettingsFilters,
        GetReviewSettingsUnitFilters, GetReviewSettingsComplianceFilters,
        SaveReviewSettingsCompliance, SaveReviewSettingsComplianceDict,
        GetAssignComplianceUnits, GetComplianceTotalToAssign,

        GetReAssignComplianceUnits, GetReAssignComplianceForUnits,
        GetAssigneewiseComplianesFilters,
        GetUserToAssignCompliance, GetChartFilters,
        GetReassignComplianceFilters, GetUserWidgetData, SaveWidgetData,
        ChangeThemes
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

class UnitStatutoryCompliances(object):
    def __init__(
        self, unit_id, unit_name, address, domain_name,
        is_new, is_locked, allow_unlock,
        updated_by, updated_on, r_count,
        domain_id
    ):
        self.unit_id = unit_id
        self.unit_name = unit_name
        self.address = address
        self.domain_name = domain_name
        self.is_new = is_new
        self.is_locked = is_locked
        self.allow_unlock = allow_unlock
        self.updated_by = updated_by
        self.updated_on = updated_on
        self.r_count = r_count
        self.domain_id = domain_id

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "u_id", "u_name", "address", "c_name", "d_name",
            "is_new", "is_locked", "allow_unlock",
            "usr_by", "usr_on", "r_count", "d_id"
        ])
        unit_id = data.get("u_id")
        unit_name = data.get("u_name")
        address = data.get("address")
        domain_name = data.get("d_name")
        is_new = data.get("is_new")
        is_locked = data.get("is_locked")
        allow_unlock = data.get("allow_unlock")
        updated_by = data.get("usr_by")
        updated_on = data.get("usr_on")
        r_count = data.get("r_count")
        domain_id = data.get("d_id")
        return UnitStatutoryCompliances(
            unit_id, unit_name, address, domain_name,
            is_new, is_locked, allow_unlock,
            updated_by, updated_on, r_count, domain_id
        )

    def to_structure(self):
        return {
            "u_id": self.unit_id,
            "u_name": self.unit_name,
            "address": self.address,
            "d_name": self.domain_name,
            "is_new": self.is_new,
            "is_locked": self.is_locked,
            "allow_unlock": self.allow_unlock,
            "usr_by": self.updated_by,
            "usr_on": self.updated_on,
            "r_count": self.r_count,
            "d_id": self.domain_id
        }

class GetStatutorySettingsFiltersSuccess(Response):
    def __init__(self, le_info, div_info, cat_info):
        self.le_info = le_info
        self.div_info = div_info
        self.cat_info = cat_info

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["le_did_infos", "div_infos", "cat_info"])

        return GetStatutorySettingsFiltersSuccess(
            data.get("le_did_infos"), data.get("div_infos"), data.get("cat_info")
        )

    def to_inner_structure(self):
        return {
            "le_did_infos": self.le_info,
            "div_infos": self.div_info,
            "cat_info": self.cat_info
        }

class GetStatutorySettingsSuccess(Response):
    def __init__(self, statutories):
        self.statutories = statutories

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["statutories"])
        statutories = data.get("statutories")
        return GetStatutorySettingsSuccess(statutories)

    def to_inner_structure(self):
        return {
            "statutories": self.statutories
        }

class GetSettingsCompliancesSuccess(Response):
    def __init__(self, statutories, total_record):
        self.statutories = statutories
        self.total_record = total_record

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["applicable_statu", "r_count"])
        statutories = data.get("applicable_statu")
        total_record = data.get("r_count")
        return GetSettingsCompliancesSuccess(statutories, total_record)

    def to_inner_structure(self):
        return {
            "applicable_statu": self.statutories,
            "r_count": self.total_record
        }

class UpdateStatutorySettingsSuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return UpdateStatutorySettingsSuccess()

    def to_inner_structure(self):
        return {
        }


class ComplianceUpdateFailed(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return ComplianceUpdateFailed()

    def to_inner_structure(self):
        return {
        }


class InvalidPassword(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return InvalidPassword()

    def to_inner_structure(self):
        return {
        }

class GetAssignCompliancesFormDataSuccess(Response):
    def __init__(
        self, legal_entities,
        divisions, categories, domains
    ):
        self.domains = domains
        self.legal_entities = legal_entities
        self.divisions = divisions
        self.categories = categories

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "le_did_infos", "div_infos", "cat_info", "domains"
        ])
        domains = data.get("domains")
        legal_entities = data.get("le_did_infos")
        divisions = data.get("div_infos")
        categories = data.get("cat_info")
        return GetAssignCompliancesFormDataSuccess(
            legal_entities, divisions, categories, domains
        )

    def to_inner_structure(self):
        return {
            "le_did_infos": self.legal_entities,
            "div_infos": self.divisions,
            "cat_info": self.categories,
            "domains": self.domains
        }

class GetAssignComplianceUnitsSuccess(Response):
    def __init__(self, units, comp_frequency):
        self.units = units
        self.comp_frequency = comp_frequency

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["assign_units", "comp_frequency"])
        return GetAssignComplianceUnitsSuccess(
            data.get("units"), data.get("comp_frequency"),
        )

    def to_inner_structure(self):
        return {
            "assign_units": self.units,
            "comp_frequency": self.comp_frequency,
        }


class GetUserToAssignComplianceSuccess(Request):
    def __init__(self, assign_users, two_level_approve):
        self.assign_users = assign_users
        self.two_level_approve = two_level_approve

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["assign_users", "t_l_approve"])
        return GetUserToAssignComplianceSuccess(
            data.get("assign_users"),
            data.get("t_l_approve")
        )

    def to_inner_structure(self):
        return {
            "assign_users": self.assign_users,
            "t_l_approve": self.two_level_approve
        }


class GetComplianceTotalToAssignSuccess(Request):
    def __init__(self, record_count):
        self.record_count = record_count

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["r_count"])
        return GetComplianceTotalToAssignSuccess(
            data.get("r_count"),
        )

    def to_inner_structure(self):
        return {
            "r_count": self.record_count,
        }

class GetComplianceForUnitsSuccess(Response):
    def __init__(self, level_one_name, statutories):
        self.level_one_name = level_one_name
        self.statutories = statutories

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["level_one_name", "assign_statutory"])
        statutories = data.get("assign_statutory")
        level_one_name = data.get("level_one_name")
        return GetComplianceForUnitsSuccess(level_one_name, statutories)

    def to_inner_structure(self):
        return {
            "level_one_name": self.level_one_name,
            "assign_statutory": self.statutories,
        }

class SaveAssignedComplianceSuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return SaveAssignedComplianceSuccess()

    def to_inner_structure(self):
        return {
        }

class InvalidDueDate(Response):
    def __init__(self, compliance_task):
        self.compliance_task = compliance_task

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["compliance_task"])
        compliance_task = data.get("compliance_task")
        compliance_task = parse_structure_CustomTextType_100(compliance_task)
        return InvalidDueDate(compliance_task)

    def to_inner_structure(self):
        return {
            "compliance_task": to_structure_CustomTextType_100(self.compliance_task)
        }

class AssigneeNotBelongToUnit(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return AssigneeNotBelongToUnit()

    def to_inner_structure(self):
        return {
        }

class ConcurrenceNotBelongToUnit(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return ConcurrenceNotBelongToUnit()

    def to_inner_structure(self):
        return {
        }

class ApprovalPersonNotBelongToUnit(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return ApprovalPersonNotBelongToUnit()

    def to_inner_structure(self):
        return {
        }

class GetUserwiseCompliancesSuccess(Response):
    def __init__(
        self, user_wise_compliances, users,
        two_level_approve
    ):
        self.user_wise_compliances = user_wise_compliances
        self.users = users
        self.two_level_approve = two_level_approve

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(
            data, [
                "user_wise_compliances", "users",
                "two_level_approve",
            ]
        )
        user_wise_compliances = data.get("user_wise_compliances")
        user_wise_compliances = parse_structure_MapType_UnsignedIntegerType_32_UnsignedIntegerType_32(
            user_wise_compliances
        )
        users = data.get("users")
        users = parse_structure_VectorType_RecordType_clienttransactions_ASSIGN_COMPLIANCE_USER(users)
        units = data.get("units")
        units = parse_structure_VectorType_RecordType_clienttransactions_ASSIGN_COMPLIANCE_UNITS(units)
        two_level_approve = data.get("two_level_approve")
        two_level_approve = parse_structure_Bool(two_level_approve)
        client_admin = data.get("client_admin")
        client_admin = parse_structure_UnsignedIntegerType_32("client_admin")
        domains = data.get("domains")
        domains = parse_structure_VectorType_RecordType_core_Domain(domains)
        return GetUserwiseCompliancesSuccess(
            user_wise_compliances, users, units,
            two_level_approve, client_admin,
            domains
        )

    def to_inner_structure(self):
        result = {
            "user_wise_compliances": to_structure_MapType_UnsignedIntegerType_32_UnsignedIntegerType_32(self.user_wise_compliances),
            "users": to_structure_VectorType_RecordType_clienttransactions_ASSIGN_COMPLIANCE_USER(self.users),
            "units": to_structure_VectorType_RecordType_clienttransactions_ASSIGN_COMPLIANCE_UNITS(self.units),
            "two_level_approve": to_structure_Bool(self.two_level_approve),
            "client_admin": to_structure_UnsignedIntegerType_32(self.client_admin),
            "domains": to_structure_VectorType_RecordType_core_Domain(self.domains)
        }
        return result

class GetAssigneeCompliancesSuccess(Response):
    def __init__(self, user_wise_compliance):
        self.user_wise_compliance = user_wise_compliance

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["user_wise_compliance"])
        user_wise_complaince = data.get("user_wise_complaince")
        user_wise_complaince = parse_structure_MapType_SignedIntegerType_8_VectorType_RecordType_clienttransactions_USER_WISE_COMPLIANCE(user_wise_complaince)
        return GetAssigneeCompliancesSuccess(user_wise_complaince)

    def to_inner_structure(self):
        return {
            "user_wise_compliance": to_structure_MapType_SignedIntegerType_8_VectorType_RecordType_clienttransactions_USER_WISE_COMPLIANCE(self.user_wise_compliance)
        }


class ReassignComplianceSuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return ReassignComplianceSuccess()

    def to_inner_structure(self):
        return {
        }
#########################################################
# Get Approval list Response
########################################################
class GetComplianceApprovalListSuccess(Response):
    def __init__(self, approval_list, approval_status, total_count):
        self.approval_list = approval_list
        self.approval_status = approval_status
        self.total_count = total_count

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["approval_list", 
                                       "approval_status", "total_count"])
        approval_list = data.get("approval_list")
        # approval_list = parse_structure_VectorType_RecordType_clienttransactions_APPORVALCOMPLIANCELIST(approval_list)
        approval_status = data.get("approval_status")
        # approval_status = parse_structure_VectorType_RecordType_core_COMPLIANCE_APPROVAL_STATUS(approval_status)
        total_count = data.get("total_count")
        # total_count = parse_structure_UnsignedIntegerType_32(total_count)
        return GetComplianceApprovalListSuccess(approval_list, approval_status, total_count)

    def to_inner_structure(self):
        return {
            "approval_list": self.approval_list,
            "approval_status": self.approval_status,
            "total_count": self.total_count
        }

class ApproveComplianceSuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return ApproveComplianceSuccess()

    def to_inner_structure(self):
        return {
        }

class IndustryWiseUnits(object):
    def __init__(self, units):
        # self.industry_name = industry_name
        self.units = units

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["units"])
        # industry_name = data.get("industry_name")
        # industry_name = parse_structure_CustomTextType_50(industry_name)
        units = data.get("pr_units")
        # units = parse_structure_VectorType_RecordType_clienttransactions_PastRecordUnits(units)

    def to_structure(self):
        return {
            # "industry_name": to_structure_CustomTextType_50(self.industry_name),
            "units": self.units
        }
####################################################
# Get Completed Task Current Year (Past Data) 
####################################################
class GetPastRecordsFormDataSuccess(Response):
    def __init__(
        self, business_groups, legal_entities, divisions, category, units,
        domains, level_1_statutories, compliance_frequency
    ):
        self.business_groups = business_groups
        self.legal_entities = legal_entities
        self.divisions = divisions
        self.category = category
        self.units = units
        self.domains = domains
        self.level_1_statutories = level_1_statutories
        self.compliance_frequency = compliance_frequency

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(
            data, [
                    "business_groups", "pr_legal_entities",
                    "client_divisions", "client_categories", "in_units", "domains", "level_1_statutories", "compliance_frequency"
                ]
            )
        # countries = data.get("countries")
        # countries = parse_structure_VectorType_RecordType_core_Country(countries)
        business_groups = data.get("business_groups")
        # business_groups = parse_structure_VectorType_RecordType_core_ClientBusinessGroup(business_groups)
        legal_entities = data.get("pr_legal_entities")
        # legal_entities = parse_structure_VectorType_RecordType_core_ClientLegalEntity(legal_entities)
        divisions = data.get("client_divisions")
        # divisions = parse_structure_VectorType_RecordType_core_ClientDivision(divisions)
        category = data.get("client_categories")
        units = data.get("in_units")
        # units = parse_structure_VectorType_RecordType_client_transactions_IndustryWiseUnits(units) TO DO
        domains = data.get("domains")
        # domains = parse_structure_VectorType_RecordType_core_Domain(domains)
        level_1_statutories = data.get("level_1_statutories")
        # level_1_statutories = parse_structure_MapType_CustomTextType_50_VectorType_CustomTextType_500(level_1_statutories) clarify
        compliance_frequency = data.get("compliance_frequency")
        # compliance_frequency = parse_structure_VectorType_RecordType_core_ComplianceFrequency(compliance_frequency)
        return GetPastRecordsFormDataSuccess(
            business_groups, legal_entities, divisions, category,
            units, domains, level_1_statutories, compliance_frequency
        )

    def to_inner_structure(self):
        return {            
            "business_groups": self.business_groups,
            "pr_legal_entities": self.legal_entities,
            "client_divisions": self.divisions,
            "client_categories": self.category,
            "in_units": self.units,
            "domains": self.domains,
            "level_1_statutories": self.level_1_statutories,
            "compliance_frequency" : self.compliance_frequency
        }

class GetStatutoriesByUnitSuccess(Response):
    def __init__(self, statutory_wise_compliances, users, total_count):
        self.statutory_wise_compliances = statutory_wise_compliances
        self.users = users
        self.total_count = total_count

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["statutory_wise_compliances", "users", "total_count"])
        statutory_wise_compliances = data.get("statutory_wise_compliances")
        statutory_wise_compliances = parse_structure_VectorType_RecordType_clienttransactions_STATUTORY_WISE_COMPLIANCES(statutory_wise_compliances)
        users = data.get("users")
        users = parse_structure_VectorType_RecordType_core_User(users)
        total_count = data.get("total_count")
        total_count = parse_structure_UnsignedIntegerType_32(total_count)
        return GetStatutoriesByUnitSuccess(statutory_wise_compliances, users, total_count)

    def to_inner_structure(self):
        return {
            "statutory_wise_compliances" : to_structure_VectorType_RecordType_clienttransactions_STATUTORY_WISE_COMPLIANCES(self.statutory_wise_compliances),
            "users" : to_structure_VectorType_RecordType_core_User(self.users),
            "total_count": to_structure_UnsignedIntegerType_32(self.total_count)
        }

class NotEnoughSpaceAvailable(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return NotEnoughSpaceAvailable()

    def to_inner_structure(self):
        return {
        }

class SavePastRecordsSuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return SavePastRecordsSuccess()

    def to_inner_structure(self):
        return {
        }

class SavePastRecordsFailed(Response):
    def __init__(self, error):
        self.error = error

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["error"])
        error = data.get("error")
        error = parse_structure_Text(error)
        return SavePastRecordsFailed(error)

    def to_inner_structure(self):
        return {
            "error" : to_structure_Text(self.error)
        }


class ChangeStatutorySettingsLockSuccess(Request):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [])
        return ChangeStatutorySettingsLockSuccess()

    def to_inner_structure(self):
        return {
        }

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


class GetAssigneewiseComplianesFiltersSuccess(Response):
    def __init__(
        self, countries, business_groups, legal_entities, divisions,
        units, users, domains, categories
    ):
        self.countries = countries
        self.business_groups = business_groups
        self.legal_entities = legal_entities
        self.divisions = divisions
        self.units = units
        self.users = users
        self.domains = domains
        self.categories = categories

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "countries", "business_groups", "legal_entities", "client_divisions",
            "units", "users", "d_info", "client_categories"
        ])
        countries = data.get("countries")
        business_groups = data.get("business_groups")
        legal_entities = data.get("legal_entities")
        divisions = data.get("client_divisions")
        categories = data.get("client_categories")
        units = data.get("units")
        users = data.get("users")
        domains = data.get("d_info")

        return GetAssigneewiseComplianesFiltersSuccess(
            countries, business_groups, legal_entities, divisions, units, users, domains, categories
        )

    def to_inner_structure(self):
        return {
            "countries": self.countries,
            "business_groups": self.business_groups,
            "legal_entities": self.legal_entities,
            "client_divisions": self.divisions,
            "client_categories": self.categories,
            "units": self.units,
            "users": self.users,
            "d_info": self.domains
        }


class GetReassignComplianceFiltersSuccess(Response):
    def __init__(self, domains, units, legal_entity_users):
        self.domains = domains
        self.units = units
        self.legal_entity_users = legal_entity_users

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["domains", "units", "legal_entity_users"])
        domains = data.get("domains")
        units = data.get("units")
        legal_entity_users = data.get("legal_entity_users")
        return GetReassignComplianceFiltersSuccess(domains, units, legal_entity_users)

    def to_inner_structure(self):
        return {
            "domains": self.domains,
            "units": self.units,
            "legal_entity_users": self.legal_entity_users
        }

class GetReAssignComplianceUnitsSuccess(Response):
    def __init__(self, units):
        self.units = units

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["reassign_units"])
        return GetReAssignComplianceUnitsSuccess(
            data.get("units"),
        )

    def to_inner_structure(self):
        return {
            "reassign_units": self.units,
        }

class GetReAssignComplianceForUnitsSuccess(Response):
    def __init__(self, reassign_compliances):
        self.reassign_compliances = reassign_compliances

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["reassign_compliances"])
        return GetReAssignComplianceForUnitsSuccess(
            data.get("reassign_compliances"),
        )

    def to_inner_structure(self):
        return {
            "reassign_compliances": self.reassign_compliances,
        }

class GetUserWidgetDataSuccess(Response):
    def __init__(self, widget_order_info, widget_list):
        self.widget_order_info = widget_order_info
        self.widget_list = widget_list

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["widget_info", "widget_list"])
        return GetUserWidgetDataSuccess(
            data.get("widget_info"), data.get("widget_list")
        )

    def to_inner_structure(self):
        return {
            "widget_info": self.widget_order_info,
            "widget_list": self.widget_list
        }

class SaveWidgetDataSuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [])
        return SaveWidgetDataSuccess()

    def to_inner_structure(self):
        return {}

def _init_Response_class_map():
    classes = [
        GetStatutorySettingsSuccess, GetSettingsCompliancesSuccess, UpdateStatutorySettingsSuccess,
        InvalidPassword, GetAssignCompliancesFormDataSuccess, GetComplianceForUnitsSuccess,
        SaveAssignedComplianceSuccess, InvalidDueDate, AssigneeNotBelongToUnit, ConcurrenceNotBelongToUnit,
        ApprovalPersonNotBelongToUnit, GetUserwiseCompliancesSuccess, ReassignComplianceSuccess,
        GetComplianceApprovalListSuccess, ApproveComplianceSuccess, GetPastRecordsFormDataSuccess,
        GetStatutoriesByUnitSuccess, SavePastRecordsSuccess, SavePastRecordsFailed,
        GetAssigneeCompliancesSuccess, ComplianceUpdateFailed,
        GetStatutorySettingsFiltersSuccess, ChangeStatutorySettingsLockSuccess,
        GetAssignComplianceUnitsSuccess,
        GetComplianceTotalToAssignSuccess, GetUserToAssignComplianceSuccess,
        GetChartFiltersSuccess, GetReassignComplianceFiltersSuccess, GetReAssignComplianceUnitsSuccess,
        GetReAssignComplianceUnitsSuccess, GetAssigneewiseComplianesFilters,
        GetUserWidgetDataSuccess, SaveWidgetDataSuccess
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
        request = parse_structure_VariantType_clienttransactions_Request(request)
        return RequestFormat(session_token, request)

    def to_structure(self):
        return {
            "session_token": to_structure_CustomTextType_50(self.session_token),
            "request": to_structure_VariantType_clienttransactions_Request(self.request),
        }

#
# ASSIGNED_COMPLIANCE
#

class ASSIGNED_COMPLIANCE(object):
    def __init__(
        self, compliance_id, compliance_name, statutory_dates,
        due_date, validity_date, trigger_before, unit_ids
    ):
        self.compliance_id = compliance_id
        self.compliance_name = compliance_name
        self.statutory_dates = statutory_dates
        self.due_date = due_date
        self.validity_date = validity_date
        self.trigger_before = trigger_before
        self.unit_ids = unit_ids

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "comp_id", "comp_name", "statu_dates",
            "d_date", "v_date", "trigger_before_days", "u_ids"
        ])
        compliance_id = data.get("comp_id")
        compliance_name = data.get("comp_name")
        statutory_dates = data.get("statu_dates")
        due_date = data.get("d_date")
        validity_date = data.get("v_date")
        trigger_before = data.get("trigger_before_days")
        unit_ids = data.get("u_ids")
        return ASSIGNED_COMPLIANCE(
            compliance_id, compliance_name, statutory_dates,
            due_date, validity_date, trigger_before, unit_ids
        )

    def to_structure(self):
        return {
            "comp_id": self.compliance_id,
            "comp_name": self.compliance_name,
            "statu_dates": self.statutory_dates,
            "d_date": self.due_date,
            "v_date": self.validity_date,
            "trigger_before_days": self.trigger_before,
            "u_ids": self.unit_ids,
        }

#
# REASSIGNED_COMPLIANCE
#

class REASSIGNED_COMPLIANCE(object):
    def __init__(
        self, u_id, comp_id,
        compliance_name,
        c_h_id, d_date, o_assignee, o_concurrence_person,
        o_approval_person
    ):
        self.u_id = u_id
        self.comp_id = comp_id
        self.compliance_name = compliance_name
        self.c_h_id = c_h_id
        self.d_date = d_date
        self.o_assignee = o_assignee
        self.o_concurrence_person = o_concurrence_person
        self.o_approval_person = o_approval_person

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["u_id", "comp_id", "compliance_name",  "c_h_id", "d_date", "o_assignee", "o_concurrence_person", "o_approval_person"])
        u_id = data.get("u_id")
        comp_id = data.get("comp_id")
        compliance_name = data.get("compliance_name")
        c_h_id = data.get("c_h_id")
        d_date = data.get("d_date")
        o_assignee = data.get("o_assignee")
        o_concurrence_person = data.get("o_concurrence_person")
        o_approval_person = data.get("o_approval_person")

        return REASSIGNED_COMPLIANCE(
            u_id, comp_id, compliance_name, c_h_id, d_date, o_assignee, o_concurrence_person, o_approval_person
        )

    def to_structure(self):
        return {
            "u_id": self.u_id,
            "comp_id": self.comp_id,
            "compliance_name": self.compliance_name,
            "c_h_id": self.c_h_id,
            "d_date": self.d_date,
            "o_assignee": self.o_assignee,
            "o_concurrence_person": self.o_concurrence_person,
            "o_approval_person": self.o_approval_person,
        }

#
# PAST_RECORD_COMPLIANCE
#

class PAST_RECORD_COMPLIANCE(object):
    def __init__(
            self, unit_id, compliance_id, due_date, completion_date, documents,
            validity_date, completed_by
        ):
        self.unit_id = unit_id
        self.compliance_id = compliance_id
        self.due_date = due_date
        self.completion_date = completion_date
        self.validity_date = validity_date
        self.documents = documents
        self.completed_by = completed_by

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(
            data, [
                    "unit_id", "compliance_id", "due_date", "completion_date",
                    "documents", "validity_date", "completed_by"
                ]
        )
        unit_id = data.get("unit_id")
        unit_id = parse_structure_UnsignedIntegerType_32(unit_id)
        compliance_id = data.get("compliance_id")
        compliance_id = parse_structure_UnsignedIntegerType_32(compliance_id)
        due_date = data.get("due_date")
        due_date = parse_structure_CustomTextType_20(due_date)
        completion_date = data.get("completion_date")
        completion_date = parse_structure_CustomTextType_20(completion_date)
        validity_date = data.get("validity_date")
        validity_date = parse_structure_CustomTextType_20(validity_date)
        documents = data.get("documents")
        documents = parse_structure_OptionalType_VectorType_RecordType_core_FileList(documents)
        completed_by = data.get("completed_by")
        completed_by = parse_structure_UnsignedIntegerType_32(completed_by)
        return PAST_RECORD_COMPLIANCE(
            unit_id, compliance_id, due_date, completion_date, documents,
            validity_date, completed_by
        )

    def to_structure(self):
        return {
            "unit_id": to_structure_SignedIntegerType_8(self.unit_id),
            "compliance_id": to_structure_SignedIntegerType_8(self.compliance_id),
            "due_date": to_structure_CustomTextType_20(self.due_date),
            "completion_date": to_structure_CustomTextType_20(self.completion_date),
            "validity_date": to_structure_CustomTextType_20(self.validity_date),
            "documents": to_structure_OptionalType_VectorType_RecordType_core_FileList(self.documents),
            "completed_by": to_structure_SignedIntegerType_8(self.completed_by)
        }

#
# UNIT_WISE_STATUTORIES
#

class UNIT_WISE_STATUTORIES(object):
    def __init__(
        self, compliance_id, compliance_name, description,
        frequency, statutory_date, due_date, applicable_units,
        summary
    ):
        self.compliance_id = compliance_id
        self.compliance_name = compliance_name
        self.description = description
        self.frequency = frequency
        self.statutory_date = statutory_date
        self.due_date = due_date
        self.applicable_units = applicable_units
        self.summary = summary

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "comp_id", "comp_name", "descp"
            "freq", "statu_dates", "due_date_list",
            "applicable_units", "summary",
        ])
        compliance_id = data.get("comp_id")
        compliance_name = data.get("comp_name")
        description = data.get("descp")
        frequency = data.get("freq")
        statutory_date = data.get("statu_dates")
        due_date = data.get("due_date_list")
        applicable_units = data.get("applicable_units")
        summary = data.get("summary")
        return UNIT_WISE_STATUTORIES(
            compliance_id, compliance_name, description,
            frequency, statutory_date, due_date, applicable_units,
            summary,
        )

    def to_structure(self):
        return {
            "comp_id": self.compliance_id,
            "comp_name": self.compliance_name,
            "descp": self.description,
            "freq": self.frequency,
            "statu_dates": self.statutory_date,
            "due_date_list": self.due_date,
            "applicable_units": self.applicable_units,
            "summary": self.summary
        }

#
# UNIT_WISE_STATUTORIES_FOR_PAST_RECORS
#

class UNIT_WISE_STATUTORIES_FOR_PAST_RECORDS(object):
    def __init__(
        self, compliance_id, compliance_name, description, frequency, statutory_date,
        due_date, assignee_name, assignee_id
    ):
        self.compliance_id = compliance_id
        self.compliance_name = compliance_name
        self.description = description
        self.frequency = frequency
        self.statutory_date = statutory_date
        self.due_date = due_date
        self.assignee_name = assignee_name
        self.assignee_id = assignee_id

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["compliance_id", "compliance_name", "description", "frequency",
            "statutory_date", "due_date", "assignee_name", "assignee_id"])
        compliance_id = data.get("compliance_id")
        compliance_id = parse_structure_UnsignedIntegerType_32(compliance_id)
        compliance_name = data.get("compliance_name")
        compliance_name = parse_structure_CustomTextType_250(compliance_name)
        description = data.get("description")
        description = parse_structure_Text(description)
        frequency = data.get("frequency")
        frequency = parse_structure_EnumType_core_COMPLIANCE_FREQUENCY(frequency)
        statutory_date = data.get("statutory_date")
        statutory_date = parse_structure_Text(statutory_date)
        due_date = data.get("due_date")
        due_date = parse_structure_OptionalType_CustomTextType_20(due_date)
        assignee_name = data.get("assignee_name")
        assignee_name = parse_structure_CustomTextType_50(assignee_name)
        assignee_id = data.get("assignee_id")
        assignee_id = parse_structure_UnsignedIntegerType_32(assignee_id)
        return UNIT_WISE_STATUTORIES_FOR_PAST_RECORDS(compliance_id, compliance_name, description, frequency,
            statutory_date, due_date, assignee_name, assignee_id)

    def to_structure(self):
        return {
            "compliance_id": to_structure_UnsignedIntegerType_32(self.compliance_id),
            "compliance_name": to_structure_CustomTextType_250(self.compliance_name),
            "description": to_structure_Text(self.description),
            "frequency": to_structure_EnumType_core_COMPLIANCE_FREQUENCY(self.frequency),
            "statutory_date": to_structure_Text(self.statutory_date),
            "due_date": to_structure_OptionalType_CustomTextType_20(self.due_date),
            "assignee_name" : to_structure_CustomTextType_50(self.assignee_name),
            "assignee_id": to_structure_UnsignedIntegerType_32(self.assignee_id)
        }

#
# ASSIGN_COMPLIANCE_UNITS
#

class ASSIGN_COMPLIANCE_UNITS(object):
    def __init__(
        self, unit_id, unit_name, address, postal_code
    ):
        self.unit_id = unit_id
        self.unit_name = unit_name
        self.address = address
        self.postal_code = postal_code

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "u_id", "u_name", "address", "postal_code"
        ])
        unit_id = data.get("u_id")
        unit_name = data.get("u_name")
        address = data.get("address")
        postal_code = data.get("postal_code")
        return ASSIGN_COMPLIANCE_UNITS(
            unit_id, unit_name, address, postal_code
        )

    def to_structure(self):
        return {
            "u_id": self.unit_id,
            "u_name": self.unit_name,
            "address": self.address,
            "postal_code": self.postal_code
        }

#
# ASSIGN_COMPLIANCE_UNITS
#

class PastRecordUnits(object):
    def __init__(
        self, unit_id, unit_name, address, division_id,
        legal_entity_id, business_group_id, country_id, domain_ids
    ):
        self.unit_id = unit_id
        self.unit_name = unit_name
        self.address = address
        self.division_id = division_id
        self.legal_entity_id = legal_entity_id
        self.business_group_id = business_group_id
        self.country_id = country_id
        self.domain_ids = domain_ids

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "unit_id", "unit_name", "address", "division_id",
            "legal_entity_id", "business_group_id", "country_id", "domain_ids"
        ])
        unit_id = data.get("unit_id")
        # unit_id = parse_structure_UnsignedIntegerType_32(unit_id)
        unit_name = data.get("unit_name")
        # unit_name = parse_structure_CustomTextType_100(unit_name)
        address = data.get("address")
        # address = parse_structure_CustomTextType_250(address)
        division_id = data.get("division_id")
        # division_id = parse_structure_OptionalType_UnsignedIntegerType_32(division_id)
        legal_entity_id = data.get("legal_entity_id")
        # legal_entity_id = parse_structure_UnsignedIntegerType_32(legal_entity_id)
        business_group_id = data.get("business_group_id")
        # business_group_id = parse_structure_OptionalType_UnsignedIntegerType_32(business_group_id)
        country_id = data.get("country_id")
        # country_id = parse_structure_UnsignedIntegerType_32(country_id)
        domain_ids = data.get("domain_ids")
        # domain_ids = parse_structure_VectorType_UnsignedIntegerType_32(domain_ids)
        return PastRecordUnits(
            unit_id, unit_name, address, division_id,
            legal_entity_id, business_group_id, country_id, domain_ids
        )

    def to_structure(self):
        return {
            "unit_id": self.unit_id,
            "unit_name": self.unit_name,
            "address": self.address,
            "division_id": self.division_id,
            "legal_entity_id": self.legal_entity_id,
            "business_group_id": self.business_group_id,
            "country_id": self.country_id,
            "domain_ids": self.domain_ids
        }


#
# ASSIGN_COMPLIANCE_USER
#

class ASSIGN_COMPLIANCE_USER(object):
    def __init__(
        self, user_id, service_provider_id, user_name, user_level, seating_unit_id,
        unit_ids, domain_ids,
        is_assignee, is_approver,
        is_concurrence,
        seating_unit_name
    ):
        self.user_id = user_id
        self.service_provider_id = service_provider_id
        self.user_name = user_name
        self.user_level = user_level
        self.seating_unit_id = seating_unit_id
        self.unit_ids = unit_ids
        self.domain_ids = domain_ids
        self.is_assignee = is_assignee
        self.is_approver = is_approver
        self.is_concurrence = is_concurrence
        self.seating_unit_name = seating_unit_name

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "usr_id", "sp_id", "emp_name", "user_level",
            "s_u_id", "u_ids", "d_ids",
            "is_assignee", "is_approver", "is_concurrence", "s_u_name"
        ])
        user_id = data.get("usr_id")
        service_provider_id = data.get("sp_id")
        user_name = data.get("emp_name")
        user_level = data.get("user_level")
        seating_unit_id = data.get("s_u_id")
        unit_ids = data.get("u_ids")
        domain_ids = data.get("d_ids")
        is_assignee = data.get("is_assignee")
        is_approver = data.get("is_approver")
        is_concurrence = data.get("is_concurrence")
        seating_unit_name = data.get("s_u_name")
        return ASSIGN_COMPLIANCE_USER(
            user_id, service_provider_id, user_name, user_level, seating_unit_id,
            unit_ids, domain_ids,
            is_assignee, is_concurrence, is_approver, seating_unit_name
        )

    def to_structure(self):
        return {
            "usr_id": self.user_id,
            "s_p_id": self.service_provider_id,
            "emp_name": self.user_name,
            "user_level": self.user_level,
            "s_u_id": self.seating_unit_id,
            "u_ids": self.unit_ids,
            "d_ids": self.domain_ids,
            "is_assignee": self.is_assignee,
            "is_concurrence": self.is_concurrence,
            "is_approver": self.is_approver,
            "s_u_name": self.seating_unit_name
        }

#
# STATUTORYWISECOMPLIANCE
#

class STATUTORYWISECOMPLIANCE(object):
    def __init__(
        self, compliance_history_id, compliance_id,
        compliance_name, description, compliance_frequency,
        statutory_date, due_date, validity_date, summary,
        domain_id, trigger_before_days
    ):
        self.compliance_history_id = compliance_history_id
        self.compliance_id = compliance_id
        self.compliance_name = compliance_name
        self.description = description
        self.compliance_frequency = compliance_frequency
        self.statutory_date = statutory_date
        self.due_date = due_date
        self.validity_date = validity_date
        self.summary = summary
        self.domain_id = domain_id
        self.trigger_before_days = trigger_before_days

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(
            data,
            [
                "compliance_history_id", "compliance_id",
                "compliance_name", "description",
                "compliance_frequency", "statutory_date",
                "due_date", "validity_date", "summary",
                "domain_id", "trigger_before_days"
            ]
        )
        compliance_history_id = data.get("compliance_history_id")
        compliance_history_id = parse_structure_OptionalType_UnsignedIntegerType_32(compliance_history_id)
        compliance_id = data.get("compliance_id")
        compliance_id = parse_structure_UnsignedIntegerType_32(compliance_id)
        compliance_name = data.get("compliance_name")
        compliance_name = parse_structure_CustomTextType_250(compliance_name)
        description = data.get("description")
        description = parse_structure_Text(description)
        compliance_frequency = data.get("compliance_frequency")
        compliance_frequency = parse_structure_EnumType_core_COMPLIANCE_FREQUENCY(compliance_frequency)
        statutory_date = data.get("statutory_date")
        statutory_date = parse_structure_VectorType_RecordType_core_StatutoryDate(statutory_date)
        due_date = data.get("due_date")
        due_date = parse_structure_CustomTextType_20(due_date)
        validity_date = data.get("validity_date")
        validity_date = parse_structure_OptionalType_CustomTextType_20(validity_date)
        summary = data.get("summary")
        summary = parse_structure_OptionalType_CustomTextType_500(summary)
        domain_id = data.get("domain_id")
        domain_id = parse_structure_UnsignedIntegerType_32(domain_id)
        trigger_before_days = data.get("trigger_before_days")
        trigger_before_days = parse_structure_OptionalType_UnsignedIntegerType_32(trigger_before_days)
        return STATUTORYWISECOMPLIANCE(
            compliance_history_id, compliance_id, compliance_name,
            description, compliance_frequency,
            statutory_date, due_date, validity_date,
            summary, domain_id, trigger_before_days
        )

    def to_structure(self):
        return {
            "compliance_history_id": to_structure_OptionalType_UnsignedIntegerType_32(self.compliance_history_id),
            "compliance_id": to_structure_SignedIntegerType_8(self.compliance_id),
            "compliance_name": to_structure_CustomTextType_250(self.compliance_name),
            "description": to_structure_Text(self.description),
            "compliance_frequency": to_structure_EnumType_core_COMPLIANCE_FREQUENCY(self.compliance_frequency),
            "statutory_date": to_structure_VectorType_RecordType_core_StatutoryDate(self.statutory_date),
            "due_date": to_structure_CustomTextType_20(self.due_date),
            "validity_date": to_structure_OptionalType_CustomTextType_20(self.validity_date),
            "summary": to_structure_OptionalType_CustomTextType_500(self.summary),
            "domain_id": to_structure_UnsignedIntegerType_32(self.domain_id),
            "trigger_before_days": to_structure_OptionalType_UnsignedIntegerType_32(self.trigger_before_days)
        }

#
# USER_WISE_UNITS
#

class USER_WISE_UNITS(object):
    def __init__(self, unit_id, unit_name, address, statutories):
        self.unit_id = unit_id
        self.unit_name = unit_name
        self.address = address
        self.statutories = statutories

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["unit_id", "unit_name", "address", "statutories"])
        unit_id = data.get("unit_id")
        unit_id = parse_structure_UnsignedIntegerType_32(unit_id)
        unit_name = data.get("unit_name")
        unit_name = parse_structure_CustomTextType_100(unit_name)
        address = data.get("address")
        address = parse_structure_CustomTextType_250(address)
        statutories = data.get("statutories")
        statutories = parse_structure_MapType_CustomTextType_100_VectorType_RecordType_clienttransactions_STATUTORYWISECOMPLIANCE(statutories)
        return USER_WISE_UNITS(unit_id, unit_name, address, statutories)

    def to_structure(self):
        return {
            "unit_id": to_structure_SignedIntegerType_8(self.unit_id),
            "unit_name": to_structure_CustomTextType_100(self.unit_name),
            "address": to_structure_CustomTextType_250(self.address),
            "statutories": to_structure_MapType_CustomTextType_100_VectorType_RecordType_clienttransactions_STATUTORYWISECOMPLIANCE(self.statutories),
        }

#
# USER_WISE_COMPLIANCE
#

class USER_WISE_COMPLIANCE(object):
    def __init__(self, no_of_compliances, units):
        self.no_of_compliances = no_of_compliances
        self.units = units

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["no_of_compliances", "units"])
        no_of_compliances = data.get("no_of_compliances")
        no_of_compliances = parse_structure_UnsignedIntegerType_32(no_of_compliances)
        units = data.get("units")
        units = parse_structure_VectorType_RecordType_clienttransactions_USER_WISE_UNITS(units)
        return USER_WISE_COMPLIANCE(no_of_compliances, units)

    def to_structure(self):
        return {
            "no_of_compliances": to_structure_SignedIntegerType_8(self.no_of_compliances),
            "units": to_structure_VectorType_RecordType_clienttransactions_USER_WISE_UNITS(self.units),
        }

################################################################
# APPROVALCOMPLIANCE - Used In Get Approval Compliances list
###############################################################
class APPROVALCOMPLIANCE(object):
    def __init__(
        self, compliance_history_id, compliance_name, description,
        domain_name, start_date, due_date, delayed_by, compliance_frequency,
        documents, file_names, upload_date, completion_date, next_due_date, concurrenced_by,
        remarks, action, statutory_dates, validity_date, unit_name
    ):
        self.compliance_history_id = compliance_history_id
        self.compliance_name = compliance_name
        self.description = description
        self.domain_name = domain_name
        self.start_date = start_date
        self.due_date = due_date
        self.delayed_by = delayed_by
        self.compliance_frequency = compliance_frequency
        self.documents = documents
        self.file_names = file_names
        self.upload_date = upload_date
        self.completion_date = completion_date
        self.next_due_date = next_due_date
        self.concurrenced_by = concurrenced_by
        self.remarks = remarks
        self.action = action
        self.statutory_dates = statutory_dates
        self.validity_date = validity_date
        self.unit_name = unit_name

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(
            data, [
                "compliance_history_id", "compliance_name",
                "description", "domain_name", "file_names", "start_date", "due_date", "delayed_by",
                "compliance_task_frequency", "uploaded_documents", "upload_date", "completion_date",
                "next_due_date", "concurrenced_by", "remarks", "action",
                "statutory_dates", "validity_date", "unit_name"
            ]
        )
        compliance_history_id = data.get("compliance_history_id")
        # compliance_history_id = parse_structure_UnsignedIntegerType_32(compliance_history_id)
        compliance_name = data.get("compliance_name")
        # compliance_name = parse_structure_CustomTextType_250(compliance_name)
        description = data.get("description")
        # description = parse_structure_Text(description)
        domain_name = data.get("domain_name")
        # domain_name = parse_structure_CustomTextType_500(domain_name)
        file_names = data.get("file_names")
        # file_names = parse_structure_OptionalType_VectorType_CustomTextType_500(file_names)
        start_date = data.get("start_date")
        # start_date = parse_structure_CustomTextType_20(start_date)
        due_date = data.get("due_date")
        # due_date = parse_structure_CustomTextType_20(due_date)
        delayed_by = data.get("delayed_by")
        # delayed_by = parse_structure_OptionalType_UnsignedIntegerType_32(delayed_by)
        compliance_frequency = data.get("compliance_task_frequency")
        # compliance_frequency = parse_structure_EnumType_core_COMPLIANCE_FREQUENCY(compliance_frequency)
        documents = data.get("uploaded_documents")        
        # documents = data.get("documents")
        # documents = parse_structure_OptionalType_VectorType_CustomTextType_500(documents)
        upload_date = data.get("upload_date")
        # upload_date = parse_structure_OptionalType_CustomTextType_20(upload_date)
        completion_date = data.get("completion_date")
        # completion_date = parse_structure_CustomTextType_20(completion_date)
        next_due_date = data.get("next_due_date")
        # next_due_date = parse_structure_OptionalType_CustomTextType_20(next_due_date)
        concurrenced_by = data.get("concurrenced_by")
        # concurrenced_by = parse_structure_OptionalType_CustomTextType_500(concurrenced_by)
        remarks = data.get("remarks")
        # remarks = parse_structure_OptionalType_CustomTextType_500(remarks)
        action = data.get("action")
        # action = parse_structure_CustomTextType_20(remarks)
        statutory_dates = data.get("statutory_dates")
        # statutory_dates = parse_structure_VectorType_RecordType_core_StatutoryDate(statutory_dates)
        validity_date = data.get("validity_date")
        # validity_date = parse_structure_OptionalType_CustomTextType_20(validity_date)
        unit_name = data.get("unit_name")
        # unit_name = parse_structure_CustomTextType_250(unit_name)
        return APPROVALCOMPLIANCE(
            compliance_history_id, compliance_name, description,
            domain_name, start_date, due_date, delayed_by, compliance_frequency,
            documents, file_names, upload_date, completion_date, next_due_date, concurrenced_by,
            remarks, action, statutory_dates, validity_date, unit_name
        )

    def to_structure(self):
        return {
            "compliance_history_id": self.compliance_history_id,
            "compliance_name": self.compliance_name,
            "description": self.description,
            "domain_name": self.domain_name,
            "start_date": self.start_date,
            "due_date": self.due_date,
            "delayed_by": self.delayed_by,
            "compliance_task_frequency": self.compliance_frequency,
            "uploaded_documents": self.documents,
            "file_names": self.file_names,
            "upload_date": self.upload_date,
            "completion_date": self.completion_date,
            "next_due_date": self.next_due_date,
            "concurrenced_by": self.concurrenced_by,
            "remarks": self.remarks,
            "action": self.action,
            "statutory_dates" : self.statutory_dates,
            "validity_date": self.validity_date,
            "unit_name": self.unit_name
        }

#
# APPORVALCOMPLIANCELIST
#

class APPORVALCOMPLIANCELIST(object):
    def __init__(self, assignee_id, assignee_name, compliances):
        self.assignee_id = assignee_id
        self.assignee_name = assignee_name
        self.compliances = compliances

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["assignee_id", "assignee_name", "approval_compliances"])
        assignee_id = data.get("assignee_id")
        # assignee_id = parse_structure_UnsignedIntegerType_32(assignee_id)
        assignee_name = data.get("assignee_name")
        # assignee_name = parse_structure_CustomTextType_50(assignee_name)
        compliances = data.get("approval_compliances")
        # compliances = parse_structure_VectorType_RecordType_clienttransactions_APPROVALCOMPLIANCE(compliances)
        return APPORVALCOMPLIANCELIST(assignee_id, assignee_name, compliances)

    def to_structure(self):
        return {
            "assignee_id": self.assignee_id,
            "assignee_name": self.assignee_name,
            "approval_compliances": self.compliances,
        }

#
# STATUTORY_WISE_COMPLIANCES
#

class STATUTORY_WISE_COMPLIANCES(object):
    def __init__(self, level_1_statutory_name, compliences):
        self.level_1_statutory_name = level_1_statutory_name
        self.compliences = compliences

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["level_1_statutory_name", "compliences"])
        level_1_statutory_name = data.get("level_1_statutory_name")
        level_1_statutory_name = parse_structure_CustomTextType_500(level_1_statutory_name)
        compliences = data.get("compliences")
        compliences = parse_structure_VectorType_RecordType_clienttransactions_UNIT_WISE_STATUTORIES_FOR_PAST_RECORDS(compliences)
        return STATUTORY_WISE_COMPLIANCES(
            level_1_statutory_name, compliences
        )

    def to_structure(self):
        return {
            "level_1_statutory_name": to_structure_CustomTextType_500(self.level_1_statutory_name),
            "compliences": to_structure_VectorType_RecordType_clienttransactions_UNIT_WISE_STATUTORIES_FOR_PAST_RECORDS(self.compliences),
        }

#
# Statutory Settings AssignedStatutory
#

class AssignedStatutory(object):
    def __init__(self, client_statutory_id, level_1_statutory_name, compliances, applicable_status, opted_status, not_applicable_remarks):
        self.client_statutory_id = client_statutory_id
        self.level_1_statutory_name = level_1_statutory_name
        self.compliances = compliances
        self.applicable_status = applicable_status
        self.opted_status = opted_status
        self.not_applicable_remarks = not_applicable_remarks

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["client_statutory_id", "level_1_statutory_name", "compliances", "applicable_status", "opted_status", "not_applicable_remarks"])
        client_statutory_id = data.get("client_statutory_id")
        client_statutory_id = parse_structure_UnsignedIntegerType_32(client_statutory_id)
        level_1_statutory_name = data.get("level_1_statutory_name")
        level_1_statutory_name = parse_structure_CustomTextType_500(level_1_statutory_name)
        compliances = data.get("compliances")
        compliances = parse_structure_VectorType_RecordType_clienttransactions_ComplianceApplicability(compliances)
        applicable_status = data.get("applicable_status")
        applicable_status = parse_structure_Bool(applicable_status)
        opted_status = data.get("opted_status")
        opted_status = parse_structure_Bool(opted_status)
        not_applicable_remarks = data.get("not_applicable_remarks")
        not_applicable_remarks = parse_structure_OptionalType_CustomTextType_500(not_applicable_remarks)
        return AssignedStatutory(client_statutory_id, level_1_statutory_name, compliances, applicable_status, opted_status, not_applicable_remarks)

    def to_structure(self):
        return {
            "client_statutory_id": to_structure_UnsignedIntegerType_32(self.client_statutory_id),
            "level_1_statutory_name": to_structure_CustomTextType_500(self.level_1_statutory_name),
            "compliances": to_structure_VectorType_RecordType_clienttransactions_ComplianceApplicability(self.compliances),
            "applicable_status": to_structure_Bool(self.applicable_status),
            "opted_status": to_structure_Bool(self.opted_status),
            "not_applicable_remarks": to_structure_OptionalType_CustomTextType_500(self.not_applicable_remarks),
        }

class ComplianceUnitApplicability(object):
    def __init__(
        self,
        unit_id, client_compliance_id,
        compliance_applicable_status, compliance_opted_status,
        compliance_remarks, is_new, is_saved
    ):
        self.unit_id = unit_id
        self.client_compliance_id = client_compliance_id
        self.compliance_applicable_status = compliance_applicable_status
        self.compliance_opted_status = compliance_opted_status
        self.compliance_remarks = compliance_remarks
        self.is_new = is_new
        self.is_saved = is_saved

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "u_id", "c_comp_id",
            "comp_app_status", "comp_opt_status", "comp_remarks", "is_new",
            "is_saved"
        ])
        unit_id = data.get("u_id")
        client_compliance_id = data.get("c_comp_id")
        compliance_applicable_status = data.get("comp_app_status")
        compliance_opted_status = data.get("comp_opt_status")
        compliance_remarks = data.get("comp_remarks")
        is_new = data.get("is_new")
        is_saved = data.get("is_saved")
        return ComplianceUnitApplicability(
            unit_id, client_compliance_id,
            compliance_applicable_status, compliance_opted_status,
            compliance_remarks, is_new,
            is_saved
        )

    def to_structure(self):
        return {
            "unit_id": self.unit_id,
            "c_comp_id": self.client_compliance_id,
            "comp_app_status": self.compliance_applicable_status,
            "comp_opt_status": self.compliance_opted_status,
            "comp_remarks": self.compliance_remarks,
            "is_new": self.is_new,
            "is_saved": self.is_saved
        }


class ComplianceApplicability(object):
    def __init__(
        self,
        level_1_statutory_name, applicable_status, opted_status, not_applicable_remarks,
        compliance_id, compliance_name, description, statutory_provision,
        unit_wise_status
    ):
        self.level_1_statutory_name = level_1_statutory_name
        self.applicable_status = applicable_status
        self.opted_status = opted_status
        self.not_applicable_remarks = not_applicable_remarks
        self.compliance_id = compliance_id
        self.compliance_name = compliance_name
        self.description = description
        self.statutory_provision = statutory_provision
        self.unit_wise_status = unit_wise_status

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "lone_statu_name", "app_status", "opt_status", "not_app_remarks",
            "comp_id", "comp_name", "descp", "s_prov",
            "unit_wise_status"
        ])
        level_1_statutory_name = data.get("lone_statu_name")
        applicable_status = data.get("app_status")
        opted_status = data.get("opt_status")
        not_applicable_remarks = data.get("not_app_remarks")
        compliance_id = data.get("comp_id")
        compliance_name = data.get("comp_name")
        description = data.get("descp")
        statutory_provision = data.get("s_prov")
        unit_wise_status = data.get("unit_wise_status")
        return ComplianceApplicability(
            level_1_statutory_name, applicable_status, opted_status,
            not_applicable_remarks,
            compliance_id, compliance_name,
            description, statutory_provision,
            unit_wise_status
        )

    def to_structure(self):
        return {
            "lone_statu_name": self.level_1_statutory_name,
            "app_status": self.applicable_status,
            "opt_status": self.opted_status,
            "not_app_remarks": self.not_applicable_remarks,
            "comp_id": self.compliance_id,
            "comp_name": self.compliance_name,
            "descp": self.description,
            "s_prov": self.statutory_provision,
            "unit_wise_status": self.unit_wise_status
        }


class GetReviewSettingsFiltersSuccess(Response):
    def __init__(self, compliance_frequency, domain_list):
        self.compliance_frequency = compliance_frequency
        self.domain_list = domain_list

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["compliance_frequency", "domain_list"])
        compliance_frequency = data.get("compliance_frequency")
        domain_list = data.get("domain_list")
        return GetReviewSettingsFiltersSuccess(compliance_frequency, domain_list)

    def to_inner_structure(self):
        return {
            "compliance_frequency": self.compliance_frequency,
            "domain_list": self.domain_list,
        }


class GetReviewSettingsUnitFiltersSuccess(Response):
    def __init__(self, rs_unit_list):
        self.rs_unit_list = rs_unit_list

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["rs_unit_list"])
        rs_unit_list = data.get("rs_unit_list")
        return GetReviewSettingsUnitFiltersSuccess(rs_unit_list)

    def to_inner_structure(self):
        return {
            "rs_unit_list": self.rs_unit_list
        }


class GetReviewSettingsComplianceFiltersSuccess(Response):
    def __init__(self, timeline, rs_compliance_list):
        self.timeline = timeline
        self.rs_compliance_list = rs_compliance_list

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["timeline", "rs_compliance_list"])
        timeline = data.get("timeline")
        rs_compliance_list = data.get("rs_compliance_list")
        return GetReviewSettingsComplianceFiltersSuccess(timeline, rs_compliance_list)

    def to_inner_structure(self):
        return {
            "timeline": self.timeline,
            "rs_compliance_list": self.rs_compliance_list
        }


class Users(object):
    def __init__(
        self, user_id, employee_name, employee_code, user_category_id, seating_unit_id,
        seating_unit_name, is_assignee, is_approver,
        user_level, service_provider_id, service_provider_name, sp_short_name
    ):
        self.user_id = user_id
        self.employee_name = employee_name
        self.employee_code = employee_code
        self.user_category_id = user_category_id
        self.seating_unit_id = seating_unit_id
        self.seating_unit_name = seating_unit_name
        self.is_assignee = is_assignee
        self.is_approver = is_approver
        self.user_level = user_level
        self.service_provider_id = service_provider_id
        self.service_provider_name = service_provider_name
        self.sp_short_name = sp_short_name

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "usr_id", "emp_name", "emp_code", "usr_cat_id", "s_u_id", "s_u_name",
            "is_assignee", "is_approver", "u_l", "sp_id", "sp_name",
            "sp_short_name"
        ])
        return Users(
            data.get("usr_id"), data.get("emp_name"), data.get("emp_code"),
            data.get("usr_cat_id"), data.get("s_u_id"), data.get("s_u_name"),
            data.get("is_assignee"), data.get("is_approver"), data.get("u_l"),
            data.get("sp_id"), data.get("sp_name"), data.get("sp_short_name")
        )

    def to_structure(self):
        return {
            "usr_id": self.user_id,
            "emp_name": self.employee_name,
            "emp_code": self.employee_code,
            "usr_cat_id": self.user_category_id,
            "s_u_id": self.seating_unit_id,
            "s_u_name": self.seating_unit_name,
            "is_assignee": self.is_assignee,
            "is_approver": self.is_approver,
            "u_l": self.user_level,
            "sp_id": self.service_provider_id,
            "sp_name": self.service_provider_name,
            "sp_short_name": self.sp_short_name
        }

#
# REASSIGN_COMPLIANCE_UNITS
#

class REASSIGN_COMPLIANCE_UNITS(object):
    def __init__(
        self, unit_id, unit_name, address, postal_code, user_type_id, no_of_compliances
    ):
        self.unit_id = unit_id
        self.unit_name = unit_name
        self.address = address
        self.postal_code = postal_code
        self.user_type_id = user_type_id
        self.no_of_compliances = no_of_compliances

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "u_id", "u_name", "address", "postal_code", "user_type_id", "no_of_compliances"
        ])
        unit_id = data.get("u_id")
        unit_name = data.get("u_name")
        address = data.get("address")
        postal_code = data.get("postal_code")
        user_type_id = data.get("user_type_id")
        no_of_compliances = data.get("no_of_compliances")

        return ASSIGN_COMPLIANCE_UNITS(
            unit_id, unit_name, address, postal_code, user_type_id, no_of_compliances
        )

    def to_structure(self):
        return {
            "u_id": self.unit_id,
            "u_name": self.unit_name,
            "address": self.address,
            "postal_code": self.postal_code,
            "user_type_id": self.user_type_id,
            "no_of_compliances": self.no_of_compliances
        }

#
# REASSIGN_COMPLIANCES
#

class REASSIGN_COMPLIANCES(object):
    def __init__(
        self, u_id, u_name, act_name, task_type, compliance_name, comp_id, f_id, frequency, compliance_description,
        summary, trigger_before_days,assignee, assignee_name, concurrence_person, concurrer_name, approval_person, approver_name,
        c_h_id, d_date, v_date
    ):
        self.u_id = u_id
        self.u_name = u_name
        self.act_name = act_name
        self.task_type = task_type
        self.compliance_name = compliance_name
        self.comp_id = comp_id
        self.f_id = f_id
        self.frequency = frequency
        self.compliance_description = compliance_description
        self.summary = summary
        self.trigger_before_days = trigger_before_days
        self.assignee = assignee
        self.assignee_name = assignee_name
        self.concurrence_person = concurrence_person
        self.concurrer_name = concurrer_name
        self.approval_person = approval_person
        self.approver_name = approver_name
        self.c_h_id = c_h_id
        self.d_date = d_date
        self.v_date = v_date

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "u_id", "u_name", "act_name", "task_type", "compliance_name", "comp_id", "f_id", "frequency", "compliance_description",
            "summary", "trigger_before_days","assignee", "assignee_name", "concurrence_person", "concurrer_name", "approval_person", "approver_name",
            "c_h_id", "d_date", "v_date"
        ])
        u_id = data.get("u_id")
        u_name = data.get("u_name")
        act_name = data.get("act_name")
        task_type = data.get("task_type")
        compliance_name = data.get("compliance_name")
        comp_id = data.get("comp_id")
        f_id = data.get("f_id")
        frequency = data.get("frequency")
        compliance_description = data.get("compliance_description")
        summary = data.get("summary")
        trigger_before_days = data.get("trigger_before_days")
        assignee = data.get("assignee")
        assignee_name = data.get("assignee_name")
        concurrence_person = data.get("concurrence_person")
        concurrer_name = data.get("concurrer_name")
        approval_person = data.get("approval_person")
        approver_name = data.get("approver_name")
        c_h_id = data.get("c_h_id")
        d_date = data.get("d_date")
        v_date = data.get("v_date")


        return ASSIGN_COMPLIANCE_UNITS(
            unit_id, unit_name, address, task_type, compliance_name, comp_id, f_id, frequency, compliance_description,
            summary, trigger_before_days,assignee, assignee_name, concurrence_person, concurrer_name, approval_person, approver_name,
            c_h_id, d_date, v_date
        )

    def to_structure(self):
        return {
            "u_id": self.u_id,
            "u_name": self.u_name,
            "act_name": self.act_name,
            "task_type": self.task_type,
            "compliance_name": self.compliance_name,
            "comp_id": self.comp_id,
            "f_id": self.f_id,
            "frequency": self.frequency,
            "compliance_description": self.compliance_description,
            "summary": self.summary,
            "trigger_before_days": self.trigger_before_days,
            "assignee": self.assignee,
            "assignee_name": self.assignee_name,
            "concurrence_person": self.concurrence_person,
            "concurrer_name": self.concurrer_name,
            "approval_person": self.approval_person,
            "approver_name": self.approver_name,
            "c_h_id": self.c_h_id,
            "d_date": self.d_date,
            "v_date": self.v_date
        }

class ChangeThemeSuccess(Response):
    def __init__(self, theme_value):
        self.theme_value = theme_value

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["theme"])
        theme_value = data.get("theme")
        return ChangeThemeSuccess(theme_value)

    def to_inner_structure(self):
        return {
            "theme": self.theme_value
        }