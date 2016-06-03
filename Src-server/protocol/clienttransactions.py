from protocol.jsonvalidators import (parse_dictionary, parse_static_list)
from protocol.parse_structure import (
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
    parse_structure_VectorType_CustomTextType_50,
    parse_structure_VectorType_RecordType_core_ClientDivision,
    parse_structure_VectorType_RecordType_core_StatutoryDate,
    parse_structure_VectorType_RecordType_clienttransactions_ASSINGED_COMPLIANCE,
    parse_structure_VectorType_RecordType_clienttransactions_APPORVALCOMPLIANCELIST,
    parse_structure_CustomTextType_250,
    parse_structure_EnumType_core_COMPLIANCE_APPROVAL_STATUS,
    parse_structure_VectorType_RecordType_core_ClientLegalEntity,
    parse_structure_VectorType_RecordType_core_Domain,
    parse_structure_EnumType_core_COMPLIANCE_FREQUENCY,
    parse_structure_CustomIntegerType_1_10,
    parse_structure_CustomTextType_20,
    parse_structure_VectorType_RecordType_clienttransactions_ComplianceApplicability,
    parse_structure_VectorType_RecordType_clienttransactions_UnitStatutoryCompliances,
    parse_structure_Bool,
    parse_structure_OptionalType_Bool,
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
    parse_structure_MapType_UnsignedIntegerType_32_UnsignedIntegerType_32
)
from protocol.to_structure import (
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
    to_structure_VectorType_SignedIntegerType_8,
    to_structure_VectorType_CustomTextType_50,
    to_structure_VectorType_RecordType_core_ClientDivision,
    to_structure_VectorType_RecordType_core_StatutoryDate,
    to_structure_VectorType_RecordType_clienttransactions_ASSINGED_COMPLIANCE,
    to_structure_VectorType_RecordType_clienttransactions_APPORVALCOMPLIANCELIST,
    to_structure_CustomTextType_250,
    to_structure_EnumType_core_COMPLIANCE_APPROVAL_STATUS,
    to_structure_VectorType_RecordType_core_ClientLegalEntity,
    to_structure_VectorType_RecordType_core_Domain,
    to_structure_EnumType_core_COMPLIANCE_FREQUENCY,
    to_structure_CustomIntegerType_1_10, to_structure_CustomTextType_20,
    to_structure_VectorType_RecordType_clienttransactions_ComplianceApplicability,
    to_structure_VectorType_RecordType_clienttransactions_UnitStatutoryCompliances,
    to_structure_Bool,
    to_structure_OptionalType_Bool,
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
    to_structure_MapType_UnsignedIntegerType_32_UnsignedIntegerType_32
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

#
# Statutory Settings Request
#
class GetStatutorySettings(Request):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return GetStatutorySettings()

    def to_inner_structure(self):
        return {
        }

class GetSettingsCompliances(Request):
    def __init__(self, unit_id, record_count):
        self.unit_id = unit_id
        self.record_count = record_count

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["unit_id", "record_count"])
        unit_id = data.get("unit_id")
        unit_id = parse_structure_UnsignedIntegerType_32(unit_id)
        record_count = data.get("record_count")
        record_count = parse_structure_UnsignedIntegerType_32(record_count)
        return GetSettingsCompliances(unit_id, record_count)

    def to_inner_structure(self):
        return {
            "unit_id": to_structure_UnsignedIntegerType_32(self.unit_id),
            "record_count": to_structure_UnsignedIntegerType_32(self.record_count),
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
        self, client_statutory_id, client_compliance_id,
        applicable_status, not_applicable_remarks,
        compliance_id, compliance_opted_status, compliance_remarks
    ):
        self.client_statutory_id = client_statutory_id
        self.client_compliance_id = client_compliance_id
        self.applicable_status = applicable_status
        self.not_applicable_remarks = not_applicable_remarks
        self.compliance_id = compliance_id
        self.compliance_opted_status = compliance_opted_status
        self.compliance_remarks = compliance_remarks

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "c_s_id", "c_c_id", "a_status", "n_a_remarks",
            "comp_id", "c_o_status", "c_remarks"
        ])
        client_statutory_id = data.get("c_s_id")
        client_statutory_id = parse_structure_UnsignedIntegerType_32(client_statutory_id)
        client_compliance_id = data.get("c_c_id")
        client_compliance_id = parse_structure_UnsignedIntegerType_32(client_compliance_id)
        applicable_status = data.get("a_status")
        applicable_status = parse_structure_Bool(applicable_status)
        not_applicable_remarks = data.get("n_a_remarks")
        not_applicable_remarks = parse_structure_OptionalType_CustomTextType_500(not_applicable_remarks)
        compliance_id = data.get("comp_id")
        compliance_id = parse_structure_UnsignedIntegerType_32(compliance_id)
        compliance_opted_status = data.get("c_o_status")
        compliance_opted_status = parse_structure_Bool(compliance_opted_status)
        compliance_remarks = data.get('c_remarks')
        compliance_remarks = parse_structure_OptionalType_CustomTextType_500(compliance_remarks)
        return UpdateStatutoryCompliance(
            client_statutory_id, client_compliance_id, applicable_status, not_applicable_remarks,
            compliance_id, compliance_opted_status, compliance_remarks
        )

    def to_structure(self):
        return {
            "c_s_id": to_structure_UnsignedIntegerType_32(self.client_statutory_id),
            "c_c_id": to_structure_UnsignedIntegerType_32(self.client_compliance_id),
            "a_status": to_structure_Bool(self.applicable_status),
            "n_a_remarks": to_structure_OptionalType_CustomTextType_500(self.not_applicable_remarks),
            "comp_id": to_structure_UnsignedIntegerType_32(self.compliance_id),
            "c_o_status": to_structure_Bool(self.compliance_opted_status),
            "c_remarks": to_structure_OptionalType_CustomTextType_500(self.compliance_remarks)
        }

class UpdateStatutorySettings(Request):
    def __init__(self, password, unit_name, unit_id, statutories):
        self.password = password
        self.unit_name = unit_name
        self.unit_id = unit_id
        self.statutories = statutories

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["password", "u_name", "u_id", "statutories"])
        password = data.get("password")
        password = parse_structure_CustomTextType_50(password)
        unit_name = data.get("u_name")
        unit_name = parse_structure_CustomTextType_250(unit_name)
        unit_id = data.get("u_id")
        unit_id = parse_structure_UnsignedIntegerType_32(unit_id)
        statutories = data.get("statutories")
        statutories = parse_structure_VectorType_RecordType_clienttransactions_UpdateStatutoryCompliance(statutories)
        return UpdateStatutorySettings(password, unit_name, unit_id, statutories)

    def to_inner_structure(self):
        return {
            "password": to_structure_VectorType_CustomTextType_50(self.password),
            "u_name": to_structure_CustomTextType_250(self.unit_name),
            "u_id": to_structure_SignedIntegerType_8(self.unit_id),
            "statutories": to_structure_VectorType_RecordType_clienttransactions_UpdateStatutoryCompliance(self.statutories)
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

class GetComplianceForUnits(Request):
    def __init__(self, unit_ids, domain_id, record_count):
        self.unit_ids = unit_ids
        self.domain_id = domain_id
        self.record_count = record_count

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["u_ids", "d_id"])
        unit_ids = data.get("u_ids")
        unit_ids = parse_structure_VectorType_UnsignedIntegerType_32(unit_ids)
        domain_id = data.get("d_id")
        domain_id = parse_structure_UnsignedIntegerType_32(domain_id)
        record_count = data.get("record_count")
        record_count = parse_structure_UnsignedIntegerType_32(record_count)
        return GetComplianceForUnits(unit_ids, domain_id, record_count)

    def to_inner_structure(self):
        return {
            "u_ids": to_structure_VectorType_UnsignedIntegerType_32(
                self.unit_ids
            ),
            "d_id": to_structure_UnsignedIntegerType_32(self.domain_id),
            "record_count": to_structure_UnsignedIntegerType_32(self.record_count)
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
        self, country_id, assignee, assignee_name,
        concurrence_person, concurrence_person_name,
        approval_person, approval_person_name,
        compliances, new_units
    ):
        self.country_id = country_id
        self.assignee = assignee
        self.assignee_name = assignee_name
        self.concurrence_person = concurrence_person
        self.concurrence_person_name = concurrence_person_name
        self.approval_person = approval_person
        self.approval_person_name = approval_person_name
        self.compliances = compliances
        self.new_units = new_units

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "c_id", "assignee", "a_name",
            "con_person", "con_person_name",
            "a_person", "a_person_name", "compliances",
            "n_units"
        ])
        country_id = data.get("c_id")
        country_id = parse_structure_UnsignedIntegerType_32(country_id)
        assignee = data.get("assignee")
        assignee = parse_structure_UnsignedIntegerType_32(assignee)
        assignee_name = data.get("a_name")
        assignee_name = parse_structure_CustomTextType_100(assignee_name)
        concurrence_person = data.get("con_person")
        concurrence_person = parse_structure_OptionalType_UnsignedIntegerType_32(concurrence_person)
        concurrence_person_name = data.get("con_person_name")
        concurrence_person_name = parse_structure_OptionalType_CustomTextType_100(concurrence_person_name)
        approval_person = data.get("a_person")
        approval_person = parse_structure_OptionalType_UnsignedIntegerType_32(approval_person)
        approval_person_name = data.get("a_person_name")
        approval_person_name = parse_structure_OptionalType_CustomTextType_100(approval_person_name)
        compliances = data.get("compliances")
        compliances = parse_structure_VectorType_RecordType_clienttransactions_ASSINGED_COMPLIANCE(compliances)
        new_units = data.get("n_units")
        new_units = parse_structure_OptionalType_VectorType_RecordType_clienttransactions_NewUnitSettings(new_units)
        return SaveAssignedCompliance(
            country_id, assignee, assignee_name,
            concurrence_person, concurrence_person_name,
            approval_person, approval_person_name,
            compliances, new_units
        )

    def to_inner_structure(self):
        return {
            "c_id": to_structure_SignedIntegerType_8(self.country_id),
            "assignee": to_structure_SignedIntegerType_8(self.assignee),
            "a_name": to_structure_CustomTextType_100(self.assignee_name),
            "con_person": to_structure_OptionalType_UnsignedIntegerType_32(self.concurrence_person),
            "con_person_name": to_structure_OptionalType_CustomTextType_100(self.concurrence_person_name),
            "a_person": to_structure_OptionalType_UnsignedIntegerType_32(self.approval_person),
            "a_person_name": to_structure_OptionalType_CustomTextType_100(self.approval_person_name),
            "compliances": to_structure_VectorType_RecordType_clienttransactions_ASSINGED_COMPLIANCE(self.compliances),
            "n_units": to_structure_OptionalType_VectorType_RecordType_clienttransactions_NewUnitSettings(self.new_units)
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
    def __init__(self, r_from, assignee, a_name, c_person, a_person, compliances, r_reason, new_units):
        self.reassigned_from = r_from
        self.assignee = assignee
        self.assignee_name = a_name
        self.concurrence_person = c_person
        self.approval_person = a_person
        self.compliances = compliances
        self.reassigned_reason = r_reason,
        self.new_units = new_units

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "r_from", "assignee", "a_name",
            "c_person", "a_person", "compliances", "r_reason",
            "n_units"
        ])
        reassigned_from = data.get("r_from")
        reassigned_from = parse_structure_UnsignedIntegerType_32(reassigned_from)
        assignee = data.get("assignee")
        assignee = parse_structure_UnsignedIntegerType_32(assignee)
        assignee_name = data.get("a_name")
        assignee_name = parse_structure_CustomTextType_250(assignee_name)
        concurrence_person = data.get("c_person")
        concurrence_person = parse_structure_OptionalType_SignedIntegerType_8(concurrence_person)
        approval_person = data.get("a_person")
        approval_person = parse_structure_UnsignedIntegerType_32(approval_person)
        compliances = data.get("compliances")
        compliances = parse_structure_VectorType_RecordType_clienttransactions_REASSIGNED_COMPLIANCE(compliances)
        reassigned_reason = data.get("r_reason")
        reassigned_reason = parse_structure_CustomTextType_500(reassigned_reason)
        new_units = data.get("n_units")
        new_units = parse_structure_OptionalType_VectorType_RecordType_clienttransactions_NewUnitSettings(new_units)
        return ReassignCompliance(
            reassigned_from, assignee, assignee_name, concurrence_person,
            approval_person, compliances, reassigned_reason, new_units
        )

    def to_inner_structure(self):
        return {
            "r_from": to_structure_SignedIntegerType_8(self.reassigned_from),
            "assignee": to_structure_SignedIntegerType_8(self.assignee),
            "a_name": to_structure_CustomTextType_250(self.assignee_name),
            "c_person": to_structure_OptionalType_SignedIntegerType_8(self.concurrence_person),
            "a_person": to_structure_SignedIntegerType_8(self.approval_person),
            "compliances": to_structure_VectorType_RecordType_clienttransactions_REASSIGNED_COMPLIANCE(self.compliances),
            "r_reason": to_structure_CustomTextType_500(self.reassigned_reason),
            "n_units": to_structure_OptionalType_VectorType_RecordType_clienttransactions_NewUnitSettings(self.new_units)
        }

class GetComplianceApprovalList(Request):
    def __init__(self, start_count):
        self.start_count = start_count

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["start_count"])
        start_count = data.get("start_count")
        start_count = parse_structure_UnsignedIntegerType_32(start_count)
        return GetComplianceApprovalList(start_count)

    def to_inner_structure(self):
        return {
            "start_count": to_structure_UnsignedIntegerType_32(self.start_count)
        }

class ApproveCompliance(Request):
    def __init__(self, compliance_history_id, approval_status, remarks,
        next_due_date, validity_date):
        self.compliance_history_id = compliance_history_id
        self.approval_status = approval_status
        self.remarks = remarks
        self.next_due_date = next_due_date
        self.validity_date = validity_date

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(
            data, [
                "compliance_history_id", "approval_status",
                "remarks",  "next_due_date", "validity_date"
            ]
        )
        compliance_history_id = data.get("compliance_history_id")
        compliance_history_id = parse_structure_UnsignedIntegerType_32(compliance_history_id)
        approval_status = data.get("approval_status")
        approval_status = parse_structure_EnumType_core_COMPLIANCE_APPROVAL_STATUS(approval_status)
        remarks = data.get("remarks")
        remarks = parse_structure_OptionalType_CustomTextType_500(remarks)
        next_due_date = data.get("next_due_date")
        next_due_date = parse_structure_OptionalType_CustomTextType_20(next_due_date)
        validity_date = data.get("validity_date")
        validity_date = parse_structure_OptionalType_CustomTextType_20(validity_date)
        return ApproveCompliance(
            compliance_history_id, approval_status, remarks,
            next_due_date, validity_date
        )

    def to_inner_structure(self):
        return {
            "compliance_history_id": to_structure_UnsignedIntegerType_32(self.compliance_history_id),
            "approval_status": to_structure_EnumType_core_COMPLIANCE_APPROVAL_STATUS(self.approval_status),
            "remarks": to_structure_OptionalType_CustomTextType_500(self.remarks),
            "next_due_date": parse_structure_OptionalType_CustomTextType_20(self.next_due_date),
            "validity_date": parse_structure_OptionalType_CustomTextType_20(self.validity_date)
        }

class GetPastRecordsFormData(Request):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return GetPastRecordsFormData()

    def to_inner_structure(self):
        return {
        }

class GetStatutoriesByUnit(Request):
    def __init__(self, unit_id, domain_id, level_1_statutory_name,
        compliance_frequency, country_id, start_count):
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


def _init_Request_class_map():
    classes = [GetStatutorySettings, GetSettingsCompliances, UpdateStatutorySettings, GetAssignCompliancesFormData, GetComplianceForUnits, SaveAssignedCompliance, GetUserwiseCompliances, GetAssigneeCompliances, ReassignCompliance, GetComplianceApprovalList, ApproveCompliance, GetPastRecordsFormData, GetStatutoriesByUnit, SavePastRecords]
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

class UnitStatutoryCompliances(object):
    def __init__(self, unit_id, unit_name, address, country_name, domain_names, business_group_name, legal_entity_name, division_name, is_closed, is_new):
        self.unit_id = unit_id
        self.unit_name = unit_name
        self.address = address
        self.country_name = country_name
        self.domain_names = domain_names
        self.business_group_name = business_group_name
        self.legal_entity_name = legal_entity_name
        self.division_name = division_name
        self.is_closed = is_closed
        self.is_new = is_new

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["unit_id", "unit_name", "address", "country_name", "domain_names", "business_group_name", "legal_entity_name", "division_name", "is_closed", "is_new"])
        unit_id = data.get("unit_id")
        unit_id = parse_structure_UnsignedIntegerType_32(unit_id)
        unit_name = data.get("unit_name")
        unit_name = parse_structure_CustomTextType_50(unit_name)
        address = data.get("address")
        address = parse_structure_CustomTextType_250(address)
        country_name = data.get("country_name")
        country_name = parse_structure_CustomTextType_50(country_name)
        domain_names = data.get("domain_names")
        domain_names = parse_structure_VectorType_CustomTextType_50(domain_names)
        business_group_name = data.get("business_group_name")
        business_group_name = parse_structure_OptionalType_CustomTextType_100(business_group_name)
        legal_entity_name = data.get("legal_entity_name")
        legal_entity_name = parse_structure_CustomTextType_50(legal_entity_name)
        division_name = data.get("division_name")
        division_name = parse_structure_OptionalType_CustomTextType_100(division_name)
        is_closed = data.get("is_closed")
        is_closed = parse_structure_Bool(is_closed)
        is_new = data.get("is_new")
        is_new = parse_structure_Bool(is_new)
        return UnitStatutoryCompliances(unit_id, unit_name, address, country_name, domain_names, business_group_name, legal_entity_name, division_name, is_closed, is_new)

    def to_structure(self):
        return {
            "unit_id": to_structure_SignedIntegerType_8(self.unit_id),
            "unit_name": to_structure_CustomTextType_100(self.unit_name),
            "address": to_structure_CustomTextType_250(self.address),
            "country_name": to_structure_CustomTextType_50(self.country_name),
            "domain_names": to_structure_VectorType_CustomTextType_50(self.domain_names),
            "business_group_name": to_structure_OptionalType_CustomTextType_100(self.business_group_name),
            "legal_entity_name": to_structure_CustomTextType_50(self.legal_entity_name),
            "division_name": to_structure_OptionalType_CustomTextType_100(self.division_name),
            "is_closed": to_structure_Bool(self.is_closed),
            "is_new": to_structure_Bool(self.is_new)
        }

class GetStatutorySettingsSuccess(Response):
    def __init__(self, statutories):
        self.statutories = statutories

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["statutories"])
        statutories = data.get("statutories")
        statutories = parse_structure_VectorType_RecordType_clienttransactions_UnitStatutoryCompliances(statutories)
        return GetStatutorySettingsSuccess(statutories)

    def to_inner_structure(self):
        return {
            "statutories": to_structure_VectorType_RecordType_clienttransactions_UnitStatutoryCompliances(self.statutories)
        }

class GetSettingsCompliancesSuccess(Response):
    def __init__(self, statutories, total_count):
        self.statutories = statutories
        self.total_count = total_count

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["statutories", "total_count"])
        statutories = data.get("statutories")
        statutories = parse_structure_VectorType_RecordType_clienttransactions_ComplianceApplicability(statutories)
        total_count = data.get("total_count")
        total_count = parse_structure_UnsignedIntegerType_32(total_count)
        return GetSettingsCompliancesSuccess(statutories, total_count)

    def to_inner_structure(self):
        return {
            "statutories": to_structure_VectorType_RecordType_clienttransactions_ComplianceApplicability(self.statutories),
            "total_count": to_structure_UnsignedIntegerType_32(self.total_count)
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
        self, countries, domains, business_groups, legal_entities,
        divisions, units, users, two_level_approve, client_admin
    ):
        self.countries = countries
        self.domains = domains
        self.business_groups = business_groups
        self.legal_entities = legal_entities
        self.divisions = divisions
        self.units = units
        self.users = users
        self.two_level_approve = two_level_approve
        self.client_admin = client_admin

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "countries", "domains", "business_groups", "legal_entities",
            "divisions", "units", "users", "two_level_approve", "client_admin"
        ])
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
        users = data.get("users")
        users = parse_structure_VectorType_RecordType_clienttransactions_ASSIGN_COMPLIANCE_USER(users)
        two_level_approve = data.get("two_level_approve")
        two_level_approve = parse_structure_Bool(two_level_approve)
        client_admin = data.get("client_admin")
        client_admin = parse_structure_UnsignedIntegerType_32("client_admin")
        return GetAssignCompliancesFormDataSuccess(
            countries, domains, business_groups, legal_entities,
            divisions, units, users, two_level_approve,
            client_admin
        )

    def to_inner_structure(self):
        return {
            "countries": to_structure_VectorType_RecordType_core_Country(self.countries),
            "domains": to_structure_VectorType_RecordType_core_Domain(self.domains),
            "business_groups": to_structure_VectorType_RecordType_core_ClientBusinessGroup(self.business_groups),
            "legal_entities": to_structure_VectorType_RecordType_core_ClientLegalEntity(self.legal_entities),
            "divisions": to_structure_VectorType_RecordType_core_ClientDivision(self.divisions),
            "units": to_structure_VectorType_RecordType_clienttransactions_ASSIGN_COMPLIANCE_UNITS(self.units),
            "users": to_structure_VectorType_RecordType_clienttransactions_ASSIGN_COMPLIANCE_USER(self.users),
            "two_level_approve": to_structure_Bool(self.two_level_approve),
            "client_admin": to_structure_UnsignedIntegerType_32(self.client_admin)
        }

class GetComplianceForUnitsSuccess(Response):
    def __init__(self, level_one_name, statutories, total_count):
        self.level_one_name = level_one_name
        self.statutories = statutories
        self.total_count = total_count

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["level_one_name", "statutories", "total_count"])
        statutories = data.get("statutories")
        statutories = parse_structure_MapType_CustomTextType_100_VectorType_RecordType_clienttransactions_UNIT_WISE_STATUTORIES(statutories)
        level_one_name = data.get("level_one_name")
        level_one_name = parse_structure_VectorType_CustomTextType_100(level_one_name)
        total_count = data.get("total_count")
        total_count = parse_structure_UnsignedIntegerType_32(total_count)
        return GetComplianceForUnitsSuccess(level_one_name, statutories, total_count)

    def to_inner_structure(self):
        return {
            "level_one_name": to_structure_VectorType_CustomTextType_100(self.level_one_name),
            "statutories": to_structure_MapType_CustomTextType_100_VectorType_RecordType_clienttransactions_UNIT_WISE_STATUTORIES(self.statutories),
            "total_count": to_structure_UnsignedIntegerType_32(self.total_count)
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
        self, user_wise_compliances, users, units,
        two_level_approve, client_admin, domains
    ):
        self.user_wise_compliances = user_wise_compliances
        self.users = users
        self.units = units
        self.two_level_approve = two_level_approve
        self.client_admin = client_admin
        self.domains = domains

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(
            data, [
                "user_wise_compliances", "users", "units",
                "two_level_approve", "client_admin", "domains"
            ]
        )
        user_wise_compliances = data.get("user_wise_compliances")
        user_wise_compliances = parse_structure_MapType_UnsignedIntegerType_32_UnsignedIntegerType_32(
            user_wise_compliances
        )
        users = data.get("users")
        users = parse_structure_VectorType_RecordType_clienttransactions_ASSIGN_COMPLIANCE_USER(users)
        # users = parse_structure_MapType_SignedIntegerType_8_VectorType_RecordType_clienttransactions_ASSIGN_COMPLIANCE_USER(
        #     users
        # )
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

class GetComplianceApprovalListSuccess(Response):
    def __init__(self, approval_list, approval_status, total_count):
        self.approval_list = approval_list
        self.approval_status = approval_status
        self.total_count = total_count

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["approval_list", "approval_status", "total_count"])
        approval_list = data.get("approval_list")
        approval_list = parse_structure_VectorType_RecordType_clienttransactions_APPORVALCOMPLIANCELIST(approval_list)
        approval_status = data.get("approval_status")
        approval_status = parse_structure_VectorType_RecordType_core_COMPLIANCE_APPROVAL_STATUS(approval_status)
        total_count = data.get("total_count")
        total_count = parse_structure_UnsignedIntegerType_32(total_count)
        return GetComplianceApprovalListSuccess(approval_list, approval_status, total_count)

    def to_inner_structure(self):
        return {
            "approval_list": to_structure_VectorType_RecordType_clienttransactions_APPORVALCOMPLIANCELIST(self.approval_list),
            "approval_status": to_structure_VectorType_RecordType_core_COMPLIANCE_APPROVAL_STATUS(self.approval_status),
            "total_count": to_structure_UnsignedIntegerType_32(self.total_count)
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
    def __init__(self, industry_name, units):
        self.industry_name = industry_name
        self.units = units

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["industry_name", "units"])
        industry_name = data.get("industry_name")
        industry_name = parse_structure_CustomTextType_50(industry_name)
        units = data.get("units")
        units = parse_structure_VectorType_RecordType_clienttransactions_PastRecordUnits(units)

    def to_structure(self):
        return {
            "industry_name": to_structure_CustomTextType_50(self.industry_name),
            "units": to_structure_VectorType_RecordType_clienttransactions_PastRecordUnits(self.units)
        }

class GetPastRecordsFormDataSuccess(Response):
    def __init__(
        self, countries, business_groups, legal_entities, divisions, units,
        domains, level_1_statutories, compliance_frequency
    ):
        self.countries = countries
        self.business_groups = business_groups
        self.legal_entities = legal_entities
        self.divisions = divisions
        self.units = units
        self.domains = domains
        self.level_1_statutories = level_1_statutories
        self.compliance_frequency = compliance_frequency

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(
            data, [
                "countries", "business_groups", "legal_entites",
                "divisions", "units", "domains", "level_1_statutories", "compliance_frequency"
                ]
            )
        countries = data.get("countries")
        countries = parse_structure_VectorType_RecordType_core_Country(countries)
        business_groups = data.get("business_groups")
        business_groups = parse_structure_VectorType_RecordType_core_ClientBusinessGroup(business_groups)
        legal_entities = data.get("legal_entities")
        legal_entities = parse_structure_VectorType_RecordType_core_ClientLegalEntity(legal_entities)
        divisions = data.get("divisions")
        divisions = parse_structure_VectorType_RecordType_core_ClientDivision(divisions)
        units = data.get("units")
        units = parse_structure_VectorType_RecordType_client_transactions_IndustryWiseUnits(units)
        domains = data.get("domains")
        domains = parse_structure_VectorType_RecordType_core_Domain(domains)
        level_1_statutories = data.get("level_1_statutories")
        level_1_statutories = parse_structure_MapType_CustomTextType_50_VectorType_CustomTextType_500(level_1_statutories)
        compliance_frequency = data.get("compliance_frequency")
        compliance_frequency = parse_structure_VectorType_RecordType_core_ComplianceFrequency(compliance_frequency)
        return GetPastRecordsFormDataSuccess(
            countries, business_groups, legal_entities, divisions,
            units, domains, level_1_statutories, compliance_frequency
        )

    def to_inner_structure(self):
        return {
            "countries": to_structure_VectorType_RecordType_core_Country(self.countries),
            "business_groups": to_structure_VectorType_RecordType_core_ClientBusinessGroup(self.business_groups),
            "legal_entities": to_structure_VectorType_RecordType_core_ClientLegalEntity(self.legal_entities),
            "divisions": to_structure_VectorType_RecordType_core_ClientDivision(self.divisions),
            "industry_wise_units": to_structure_VectorType_RecordType_client_transactions_IndustryWiseUnits(self.units),
            "domains": to_structure_VectorType_RecordType_core_Domain(self.domains),
            "level_1_statutories": to_structure_MapType_CustomTextType_50_VectorType_CustomTextType_500(self.level_1_statutories),
            "compliance_frequency" : to_structure_VectorType_RecordType_core_ComplianceFrequency(self.compliance_frequency)
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

def _init_Response_class_map():
    classes = [
        GetStatutorySettingsSuccess, GetSettingsCompliancesSuccess, UpdateStatutorySettingsSuccess,
        InvalidPassword, GetAssignCompliancesFormDataSuccess, GetComplianceForUnitsSuccess,
        SaveAssignedComplianceSuccess, InvalidDueDate, AssigneeNotBelongToUnit, ConcurrenceNotBelongToUnit,
        ApprovalPersonNotBelongToUnit, GetUserwiseCompliancesSuccess, ReassignComplianceSuccess,
        GetComplianceApprovalListSuccess, ApproveComplianceSuccess, GetPastRecordsFormDataSuccess,
        GetStatutoriesByUnitSuccess, SavePastRecordsSuccess, SavePastRecordsFailed,
        GetAssigneeCompliancesSuccess
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
# ASSINGED_COMPLIANCE
#

class ASSINGED_COMPLIANCE(object):
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
            "d_date", "v_date", "trig_before", "u_ids"
        ])
        compliance_id = data.get("comp_id")
        compliance_id = parse_structure_UnsignedIntegerType_32(compliance_id)
        compliance_name = data.get("comp_name")
        compliance_name = parse_structure_CustomTextType_250(compliance_name)
        statutory_dates = data.get("statu_dates")
        statutory_dates = parse_structure_OptionalType_VectorType_RecordType_core_StatutoryDate(statutory_dates)
        due_date = data.get("d_date")
        due_date = parse_structure_OptionalType_CustomTextType_20(due_date)
        validity_date = data.get("v_date")
        validity_date = parse_structure_OptionalType_CustomTextType_20(validity_date)
        trigger_before = data.get("trig_before")
        trigger_before = parse_structure_OptionalType_SignedIntegerType_8(trigger_before)
        unit_ids = data.get("u_ids")
        unit_ids = parse_structure_VectorType_SignedIntegerType_8(unit_ids)
        return ASSINGED_COMPLIANCE(compliance_id, compliance_name, statutory_dates, due_date, validity_date, trigger_before, unit_ids)

    def to_structure(self):
        return {
            "comp_id": to_structure_SignedIntegerType_8(self.compliance_id),
            "comp_name": to_structure_CustomTextType_250(self.compliance_name),
            "statu_dates": to_structure_OptionalType_VectorType_RecordType_core_StatutoryDate(self.statutory_dates),
            "d_date": to_structure_OptionalType_CustomTextType_20(self.due_date),
            "v_date": to_structure_OptionalType_CustomTextType_20(self.validity_date),
            "trig_before": to_structure_OptionalType_SignedIntegerType_8(self.trigger_before),
            "u_ids": to_structure_VectorType_UnsignedIntegerType_32(self.unit_ids),
        }

#
# REASSIGNED_COMPLIANCE
#

class REASSIGNED_COMPLIANCE(object):
    def __init__(
        self, u_id, c_id,
        c_name,
        c_history_id, d_date
    ):
        self.unit_id = u_id
        self.compliance_id = c_id
        self.compliance_name = c_name
        self.compliance_history_id = c_history_id
        self.due_date = d_date

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["u_id", "c_id", "c_name",  "c_history_id", "d_date"])
        unit_id = data.get("u_id")
        unit_id = parse_structure_UnsignedIntegerType_32(unit_id)
        compliance_id = data.get("c_id")
        compliance_id = parse_structure_UnsignedIntegerType_32(compliance_id)
        compliance_name = data.get("c_name")
        compliance_name = parse_structure_CustomTextType_500(compliance_name)
        compliance_history_id = data.get("c_history_id")
        compliance_history_id = parse_structure_OptionalType_UnsignedIntegerType_32(compliance_history_id)
        due_date = data.get("d_date")
        due_date = parse_structure_OptionalType_CustomTextType_20(due_date)
        return REASSIGNED_COMPLIANCE(
            unit_id, compliance_id, compliance_name, compliance_history_id, due_date
        )

    def to_structure(self):
        return {
            "u_id": to_structure_SignedIntegerType_8(self.unit_id),
            "c_id": to_structure_SignedIntegerType_8(self.compliance_id),
            "c_name": to_structure_CustomTextType_500(self.compliance_name),
            "c_history_id": to_structure_OptionalType_UnsignedIntegerType_32(self.compliance_history_id),
            "d_date": to_structure_OptionalType_CustomTextType_20(self.due_date),
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
            "compliance_id", "compliance_name", "description",
            "frequency", "statutory_date", "due_date",
            "applicable_units", "summary"
        ])
        compliance_id = data.get("compliance_id")
        compliance_id = parse_structure_UnsignedIntegerType_32(compliance_id)
        compliance_name = data.get("compliance_name")
        compliance_name = parse_structure_CustomTextType_250(compliance_name)
        description = data.get("description")
        description = parse_structure_Text(description)
        frequency = data.get("frequency")
        frequency = parse_structure_EnumType_core_COMPLIANCE_FREQUENCY(frequency)
        statutory_date = data.get("statutory_date")
        statutory_date = parse_structure_VectorType_RecordType_core_StatutoryDate(statutory_date)
        due_date = data.get("due_date")
        due_date = parse_structure_OptionalType_VectorType_CustomTextType_20(due_date)
        applicable_units = data.get("applicable_units")
        applicable_units = parse_structure_VectorType_UnsignedIntegerType_32(applicable_units)
        summary = data.get("summary")
        summary = parse_structure_OptionalType_CustomTextType_100(summary)
        return UNIT_WISE_STATUTORIES(
            compliance_id, compliance_name, description,
            frequency, statutory_date, due_date, applicable_units,
            summary
        )

    def to_structure(self):
        return {
            "compliance_id": to_structure_SignedIntegerType_8(self.compliance_id),
            "compliance_name": to_structure_CustomTextType_250(self.compliance_name),
            "description": to_structure_Text(self.description),
            "frequency": to_structure_EnumType_core_COMPLIANCE_FREQUENCY(self.frequency),
            "statutory_date": to_structure_VectorType_RecordType_core_StatutoryDate(self.statutory_date),
            "due_date": to_structure_OptionalType_VectorType_CustomTextType_20(self.due_date),
            "applicable_units": to_structure_VectorType_UnsignedIntegerType_32(self.applicable_units),
            "summary": to_structure_OptionalType_CustomTextType_100(self.summary)
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
            "legal_entity_id", "business_group_id", "country_id",
            "domain_ids"
        ])
        unit_id = data.get("unit_id")
        unit_id = parse_structure_UnsignedIntegerType_32(unit_id)
        unit_name = data.get("unit_name")
        unit_name = parse_structure_CustomTextType_100(unit_name)
        address = data.get("address")
        address = parse_structure_CustomTextType_250(address)
        division_id = data.get("division_id")
        division_id = parse_structure_UnsignedIntegerType_32(division_id)
        legal_entity_id = data.get("legal_entity_id")
        legal_entity_id = parse_structure_UnsignedIntegerType_32(legal_entity_id)
        business_group_id = data.get("business_group_id")
        business_group_id = parse_structure_UnsignedIntegerType_32(business_group_id)
        country_id = data.get("country_id")
        country_id = parse_structure_UnsignedIntegerType_32(country_id)
        domain_ids = data.get("domain_ids")
        domain_ids = parse_structure_VectorType_UnsignedIntegerType_32(domain_ids)
        return ASSIGN_COMPLIANCE_UNITS(
            unit_id, unit_name, address, division_id,
            legal_entity_id, business_group_id, country_id, domain_ids
        )

    def to_structure(self):
        return {
            "unit_id": to_structure_OptionalType_UnsignedIntegerType_32(self.unit_id),
            "unit_name": to_structure_CustomTextType_100(self.unit_name),
            "address": to_structure_CustomTextType_250(self.address),
            "division_id": to_structure_OptionalType_SignedIntegerType_8(self.division_id),
            "legal_entity_id": to_structure_SignedIntegerType_8(self.legal_entity_id),
            "business_group_id": to_structure_OptionalType_SignedIntegerType_8(self.business_group_id),
            "country_id": to_structure_UnsignedIntegerType_32(self.country_id),
            "domain_ids": to_structure_VectorType_UnsignedIntegerType_32(self.domain_ids)
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
        unit_id = parse_structure_UnsignedIntegerType_32(unit_id)
        unit_name = data.get("unit_name")
        unit_name = parse_structure_CustomTextType_100(unit_name)
        address = data.get("address")
        address = parse_structure_CustomTextType_250(address)
        division_id = data.get("division_id")
        division_id = parse_structure_OptionalType_UnsignedIntegerType_32(division_id)
        legal_entity_id = data.get("legal_entity_id")
        legal_entity_id = parse_structure_UnsignedIntegerType_32(legal_entity_id)
        business_group_id = data.get("business_group_id")
        business_group_id = parse_structure_OptionalType_UnsignedIntegerType_32(business_group_id)
        country_id = data.get("country_id")
        country_id = parse_structure_UnsignedIntegerType_32(country_id)
        domain_ids = data.get("domain_ids")
        domain_ids = parse_structure_VectorType_UnsignedIntegerType_32(domain_ids)
        return PastRecordUnits(
            unit_id, unit_name, address, division_id,
            legal_entity_id, business_group_id, country_id, domain_ids
        )

    def to_structure(self):
        return {
            "unit_id": to_structure_UnsignedIntegerType_32(self.unit_id),
            "unit_name": to_structure_CustomTextType_100(self.unit_name),
            "address": to_structure_CustomTextType_250(self.address),
            "division_id": to_structure_OptionalType_UnsignedIntegerType_32(self.division_id),
            "legal_entity_id": to_structure_UnsignedIntegerType_32(self.legal_entity_id),
            "business_group_id": to_structure_OptionalType_UnsignedIntegerType_32(self.business_group_id),
            "country_id": to_structure_UnsignedIntegerType_32(self.country_id),
            "domain_ids": to_structure_VectorType_UnsignedIntegerType_32(self.domain_ids)
        }


#
# ASSIGN_COMPLIANCE_USER
#

class ASSIGN_COMPLIANCE_USER(object):
    def __init__(
        self, user_id, user_name, user_level, seating_unit_id,
        unit_ids, domain_ids,
        is_assignee, is_approver,
        is_concurrence
    ):
        self.user_id = user_id
        self.user_name = user_name
        self.user_level = user_level
        self.seating_unit_id = seating_unit_id
        self.unit_ids = unit_ids
        self.domain_ids = domain_ids
        self.is_assignee = is_assignee
        self.is_approver = is_approver
        self.is_concurrence = is_concurrence

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "user_id", "user_name", "user_level",
            "seating_unit_id", "unit_ids", "domain_ids",
            "is_assignee", "is_approver", "is_concurrence"
        ])
        user_id = data.get("user_id")
        user_id = parse_structure_UnsignedIntegerType_32(user_id)
        user_name = data.get("user_name")
        user_name = parse_structure_CustomTextType_50(user_name)
        user_level = data.get("user_level")
        user_level = parse_structure_CustomIntegerType_1_10(user_level)
        seating_unit_id = data.get("seating_unit_id")
        seating_unit_id = parse_structure_UnsignedIntegerType_32(seating_unit_id)
        unit_ids = data.get("unit_ids")
        unit_ids = parse_structure_VectorType_SignedIntegerType_8(unit_ids)
        domain_ids = data.get("domain_ids")
        domain_ids = parse_structure_VectorType_SignedIntegerType_8(domain_ids)
        is_assignee = data.get("is_assignee")
        is_assignee = parse_structure_Bool(is_assignee)
        is_approver = data.get("is_approver")
        is_approver = parse_structure_Bool(is_approver)
        is_concurrence = data.get("is_concurrence")
        is_concurrence = parse_structure_Bool(is_concurrence)
        return ASSIGN_COMPLIANCE_USER(
            user_id, user_name, user_level, seating_unit_id,
            unit_ids, domain_ids,
            is_assignee, is_concurrence, is_approver
        )

    def to_structure(self):
        return {
            "user_id": to_structure_SignedIntegerType_8(self.user_id),
            "user_name": to_structure_CustomTextType_50(self.user_name),
            "user_level": to_structure_CustomIntegerType_1_10(self.user_level),
            "seating_unit_id": to_structure_OptionalType_UnsignedIntegerType_32(self.seating_unit_id),
            "unit_ids": to_structure_VectorType_UnsignedIntegerType_32(self.unit_ids),
            "domain_ids": to_structure_VectorType_SignedIntegerType_8(self.domain_ids),
            "is_assignee": to_structure_Bool(self.is_assignee),
            "is_concurrence": to_structure_Bool(self.is_concurrence),
            "is_approver": to_structure_Bool(self.is_approver)
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

#
# APPROVALCOMPLIANCE
#

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
                "compliance_frequency", "documents", "upload_date", "completion_date",
                "next_due_date", "concurrenced_by", "remarks", "action",
                "statutory_dates", "validity_date", "unit_name"
            ]
        )
        compliance_history_id = data.get("compliance_history_id")
        compliance_history_id = parse_structure_UnsignedIntegerType_32(compliance_history_id)
        compliance_name = data.get("compliance_name")
        compliance_name = parse_structure_CustomTextType_250(compliance_name)
        description = data.get("description")
        description = parse_structure_Text(description)
        domain_name = data.get("domain_name")
        domain_name = parse_structure_CustomTextType_500(domain_name)
        file_names = data.get("file_names")
        file_names = parse_structure_OptionalType_VectorType_CustomTextType_500(file_names)
        start_date = data.get("start_date")
        start_date = parse_structure_CustomTextType_20(start_date)
        due_date = data.get("due_date")
        due_date = parse_structure_CustomTextType_20(due_date)
        delayed_by = data.get("delayed_by")
        delayed_by = parse_structure_OptionalType_UnsignedIntegerType_32(delayed_by)
        compliance_frequency = data.get("compliance_frequency")
        compliance_frequency = parse_structure_EnumType_core_COMPLIANCE_FREQUENCY(compliance_frequency)
        documents = data.get("documents")
        documents = parse_structure_OptionalType_VectorType_CustomTextType_500(documents)
        upload_date = data.get("upload_date")
        upload_date = parse_structure_OptionalType_CustomTextType_20(upload_date)
        completion_date = data.get("completion_date")
        completion_date = parse_structure_CustomTextType_20(completion_date)
        next_due_date = data.get("next_due_date")
        next_due_date = parse_structure_OptionalType_CustomTextType_20(next_due_date)
        concurrenced_by = data.get("concurrenced_by")
        concurrenced_by = parse_structure_OptionalType_CustomTextType_500(concurrenced_by)
        remarks = data.get("remarks")
        remarks = parse_structure_OptionalType_CustomTextType_500(remarks)
        action = data.get("action")
        action = parse_structure_CustomTextType_20(remarks)
        statutory_dates = data.get("statutory_dates")
        statutory_dates = parse_structure_VectorType_RecordType_core_StatutoryDate(statutory_dates)
        validity_date = data.get("validity_date")
        validity_date = parse_structure_OptionalType_CustomTextType_20(validity_date)
        unit_name = data.get("unit_name")
        unit_name = parse_structure_CustomTextType_250(unit_name)
        return APPROVALCOMPLIANCE(
            compliance_history_id, compliance_name, description,
            domain_name, start_date, due_date, delayed_by, compliance_frequency,
            documents, file_names, upload_date, completion_date, next_due_date, concurrenced_by,
            remarks, action, statutory_dates, validity_date, unit_name
        )

    def to_structure(self):
        return {
            "compliance_history_id": to_structure_SignedIntegerType_8(self.compliance_history_id),
            "compliance_name": to_structure_CustomTextType_250(self.compliance_name),
            "description": to_structure_Text(self.description),
            "domain_name": to_structure_CustomTextType_50(self.domain_name),
            "start_date": to_structure_CustomTextType_20(self.start_date),
            "due_date": to_structure_OptionalType_CustomTextType_20(self.due_date),
            "delayed_by": to_structure_OptionalType_UnsignedIntegerType_32(self.delayed_by),
            "compliance_frequency": to_structure_EnumType_core_COMPLIANCE_FREQUENCY(self.compliance_frequency),
            "documents": to_structure_OptionalType_VectorType_CustomTextType_500(self.documents),
            "file_names": to_structure_OptionalType_VectorType_CustomTextType_500(self.file_names),
            "upload_date": to_structure_OptionalType_CustomTextType_20(self.upload_date),
            "completion_date": to_structure_CustomTextType_20(self.completion_date),
            "next_due_date": to_structure_OptionalType_CustomTextType_20(self.next_due_date),
            "concurrenced_by": to_structure_OptionalType_CustomTextType_50(self.concurrenced_by),
            "remarks": to_structure_OptionalType_CustomTextType_500(self.remarks),
            "action": to_structure_CustomTextType_20(self.action),
            "statutory_dates" : to_structure_VectorType_RecordType_core_StatutoryDate(self.statutory_dates),
            "validity_date": to_structure_OptionalType_CustomTextType_20(self.validity_date),
            "unit_name": to_structure_CustomTextType_250(self.unit_name)
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
        data = parse_dictionary(data, ["assignee_id", "assignee_name", "compliances"])
        assignee_id = data.get("assignee_id")
        assignee_id = parse_structure_UnsignedIntegerType_32(assignee_id)
        assignee_name = data.get("assignee_name")
        assignee_name = parse_structure_CustomTextType_50(assignee_name)
        compliances = data.get("compliances")
        compliances = parse_structure_VectorType_RecordType_clienttransactions_APPROVALCOMPLIANCE(compliances)
        return APPORVALCOMPLIANCELIST(assignee_id, assignee_name, compliances)

    def to_structure(self):
        return {
            "assignee_id": to_structure_SignedIntegerType_8(self.assignee_id),
            "assignee_name": to_structure_CustomTextType_50(self.assignee_name),
            "compliances": to_structure_VectorType_RecordType_clienttransactions_APPROVALCOMPLIANCE(self.compliances),
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


class ComplianceApplicability(object):
    def __init__(
        self,
        level_1_statutory_name, applicable_status, opted_status, not_applicable_remarks,
        client_statutory_id,
        client_compliance_id,
        compliance_id,
        compliance_name, description, statutory_provision,
        compliance_applicable_status, compliance_opted_status,
        compliance_remarks, is_new, domain_name
    ):
        self.level_1_statutory_name = level_1_statutory_name
        self.applicable_status = applicable_status
        self.opted_status = opted_status
        self.not_applicable_remarks = not_applicable_remarks
        self.client_statutory_id = client_statutory_id
        self.client_compliance_id = client_compliance_id
        self.compliance_id = compliance_id
        self.compliance_name = compliance_name
        self.description = description
        self.statutory_provision = statutory_provision
        self.compliance_applicable_status = compliance_applicable_status
        self.compliance_opted_status = compliance_opted_status
        self.compliance_remarks = compliance_remarks
        self.is_new = is_new
        self.domain_name = domain_name

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "level_1_statutory_name", "applicable_status", "opted_status", "not_applicable_remarks",
            "client_statutory_id", "client_compliance_id",
            "compliance_id",
            "compliance_name", "description",
            "statutory_provision",
            "compliance_applicable_status",
            "compliance_opted_status", "compliance_remarks",
            "is_new", "domain_name"
        ])
        level_1_statutory_name = data.get("level_1_statutory_name")
        level_1_statutory_name = parse_structure_CustomTextType_500(level_1_statutory_name)
        applicable_status = data.get("applicable_status")
        applicable_status = parse_structure_Bool(applicable_status)
        opted_status = data.get("opted_status")
        opted_status = parse_structure_Bool(opted_status)
        not_applicable_remarks = data.get("not_applicable_remarks")
        not_applicable_remarks = parse_structure_OptionalType_CustomTextType_500(not_applicable_remarks)
        client_statutory_id = data.get("client_statutory_id")
        client_statutory_id = parse_structure_UnsignedIntegerType_32(client_statutory_id)
        client_compliance_id = data.get("client_compliance_id")
        client_compliance_id = parse_structure_UnsignedIntegerType_32(client_compliance_id)
        compliance_id = data.get("compliance_id")
        compliance_id = parse_structure_UnsignedIntegerType_32(compliance_id)
        compliance_name = data.get("compliance_name")
        compliance_name = parse_structure_CustomTextType_250(compliance_name)
        description = data.get("description")
        description = parse_structure_Text(description)
        statutory_provision = data.get("statutory_provision")
        statutory_provision = parse_structure_Text(statutory_provision)
        compliance_applicable_status = data.get("compliance_applicable_status")
        compliance_applicable_status = parse_structure_Bool(compliance_applicable_status)
        compliance_opted_status = data.get("compliance_opted_status")
        compliance_opted_status = parse_structure_OptionalType_Bool(compliance_opted_status)
        compliance_remarks = data.get("compliance_remarks")
        compliance_remarks = parse_structure_OptionalType_CustomTextType_500(compliance_remarks)
        is_new = data.get("is_new")
        is_new = parse_structure_Bool(is_new)
        domain_name = data.get("domain_name")
        domain_name = parse_structure_CustomTextType_50(domain_name)
        return ComplianceApplicability(
            level_1_statutory_name, applicable_status, opted_status, not_applicable_remarks,
            client_statutory_id, client_compliance_id,
            compliance_id, compliance_name,
            description, statutory_provision,
            compliance_applicable_status, compliance_opted_status,
            compliance_remarks, is_new,
            domain_name
        )

    def to_structure(self):
        return {
            "level_1_statutory_name": to_structure_CustomTextType_500(self.level_1_statutory_name),
            "applicable_status": to_structure_Bool(self.applicable_status),
            "opted_status": to_structure_Bool(self.opted_status),
            "not_applicable_remarks": to_structure_OptionalType_CustomTextType_500(self.not_applicable_remarks),
            "client_statutory_id": to_structure_UnsignedIntegerType_32(self.client_statutory_id),
            "client_compliance_id": to_structure_UnsignedIntegerType_32(self.client_compliance_id),
            "compliance_id": to_structure_SignedIntegerType_8(self.compliance_id),
            "compliance_name": to_structure_CustomTextType_250(self.compliance_name),
            "description": to_structure_Text(self.description),
            "statutory_provision": parse_structure_Text(self.statutory_provision),
            "compliance_applicable_status": to_structure_Bool(self.compliance_applicable_status),
            "compliance_opted_status": to_structure_OptionalType_Bool(self.compliance_opted_status),
            "compliance_remarks": to_structure_OptionalType_CustomTextType_500(self.compliance_remarks),
            "is_new": to_structure_Bool(self.is_new),
            "domain_name": to_structure_CustomTextType_50(self.domain_name)
        }
