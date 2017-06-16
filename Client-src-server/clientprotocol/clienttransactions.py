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
        return {}

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
            "le_id": self.legal_entity_id, "div_id": self.division_id, "cat_id": self.category_id
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
            "le_id": self.legal_entity_id, "d_id": self.domain_id, "u_id": self.unit_id,
            "lock": self.lock, "password": self.password
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
            "le_id": self.legal_entity_id, "u_ids": self.unit_id,
            "r_count": self.record_count, "d_id": self.domain_id, "f_id": self.frequency_id
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
            "c_c_id", "a_status", "n_a_remarks", "comp_id", "c_o_status", "c_remarks",
            "u_name", "u_id",
        ])
        return UpdateStatutoryCompliance(
            data.get("c_c_id"), data.get("a_status"), data.get("n_a_remarks"),
            data.get("comp_id"), data.get("c_o_status"), data.get('c_remarks'),
            data.get("u_name"), data.get("u_id"),
        )

    def to_structure(self):
        return {
            "c_c_id": self.client_compliance_id, "a_status": self.applicable_status,
            "n_a_remarks": self.not_applicable_remarks, "comp_id": self.compliance_id,
            "c_o_status": self.compliance_opted_status, "c_remarks": self.compliance_remarks,
            "u_name": self.unit_name, "u_id": self.unit_id,
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
            "password": self.password, "update_statutories": self.statutories,
            "le_id": self.legal_entity_id, "s_s": self.s_s,
            "d_id": self.domain_id, "u_ids": self.unit_ids
        }

class SaveStatutorySettings(Request):
    def __init__(
        self, statutories,
        legal_entity_id, s_s, domain_id, unit_ids
    ):
        self.statutories = statutories
        self.legal_entity_id = legal_entity_id
        self.s_s = s_s
        self.domain_id = domain_id
        self.unit_ids = unit_ids

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "update_statutories", "le_id", "s_s", "d_id", "u_ids"
        ])
        return SaveStatutorySettings(
            data.get("update_statutories"), data.get("le_id"),
            data.get("s_s"), data.get("d_id"), data.get("u_ids"),
        )

    def to_inner_structure(self):
        return {
            "update_statutories": self.statutories, "le_id": self.legal_entity_id,
            "s_s": self.s_s, "d_id": self.domain_id, "u_ids": self.unit_ids
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
    def __init__(self, legal_entity_id, domain_id, country_id):
        self.legal_entity_id = legal_entity_id
        self.domain_id = domain_id
        self.country_id = country_id

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["le_id", "d_id", "c_id"])
        return GetAssignComplianceUnits(
            data.get("le_id"), data.get("d_id"), data.get("c_id")
        )

    def to_inner_structure(self):
        return {
            "le_id": self.legal_entity_id, "d_id": self.domain_id, "c_id": self.country_id
        }


class GetUserToAssignCompliance(Request):
    def __init__(self, domain_id, unit_ids, legal_entity_id):
        self.domain_id = domain_id
        self.unit_ids = unit_ids
        self.legal_entity_id = legal_entity_id

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["d_id", "u_ids", "le_id"])
        return GetUserToAssignCompliance(
            data.get("d_id"), data.get("u_ids"), data.get("le_id"),
        )

    def to_inner_structure(self):
        return {
            "d_id": self.domain_id, "u_ids": self.unit_ids, "le_id": self.legal_entity_id
        }

class GetComplianceTotalToAssign(Request):
    def __init__(self, legal_entity_id, unit_ids, domain_id, frequency_ids):
        self.legal_entity_id = legal_entity_id
        self.unit_ids = unit_ids
        self.domain_id = domain_id
        self.frequency_ids = frequency_ids

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["le_id", "u_ids", "d_id", "f_ids"])

        return GetComplianceTotalToAssign(
            data.get("le_id"), data.get("u_ids"), data.get("d_id"), data.get("f_ids"),
        )

    def to_inner_structure(self):
        return {
            "le_id": self.legal_entity_id, "u_ids": self.unit_ids,
            "d_id": self.domain_id, "f_ids": self.frequency_ids
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
        return GetComplianceForUnits(
            data.get("le_id"), data.get("u_ids"), data.get("d_id"), data.get("r_count"), data.get("f_ids")
        )

    def to_inner_structure(self):
        return {
            "le_id": self.legal_entity_id, "u_ids": self.unit_ids, "d_id": self.domain_id,
            "r_count": self.record_count, "f_ids": self.frequency_ids
        }


class SaveAssignedCompliance(Request):
    def __init__(
        self, assignee, assignee_name,
        concurrence_person, concurrence_person_name,
        approval_person, approval_person_name,
        compliances, legal_entity_id, domain_id,
        unit_ids
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
        self.unit_ids = unit_ids

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "assignee", "assignee_name", "concurrence_person", "concurrer_name",
            "approval_person", "approver_name", "assign_compliances", "le_id", "d_id", "u_ids"
        ])
        return SaveAssignedCompliance(
            data.get("assignee"), data.get("assignee_name"), data.get("concurrence_person"),
            data.get("concurrer_name"), data.get("approval_person"), data.get("approver_name"),
            data.get("assign_compliances"), data.get("le_id"), data.get("d_id"), data.get("u_ids")
        )

    def to_inner_structure(self):
        return {
            "assignee": self.assignee, "assignee_name": self.assignee_name,
            "concurrence_person": self.concurrence_person, "concurrer_name": self.concurrence_person_name,
            "approval_person": self.approval_person, "approver_name": self.approval_person_name,
            "assign_compliances": self.compliances, "le_id": self.legal_entity_id,
            "d_id": self.domain_id, "u_ids": self.unit_ids
        }

class GetUserwiseCompliances(Request):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return GetUserwiseCompliances()

    def to_inner_structure(self):
        return {}


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
            data.get("le_id"), data.get("r_from"), data.get("assignee"), data.get("assignee_name"),
            data.get("concurrence_person"), data.get("approval_person"), data.get("reassigned_compliance"),
            data.get("reason")
        )

    def to_inner_structure(self):
        return {
            "le_id": self.legal_entity_id, "r_from": self.r_from, "assignee": self.assignee,
            "assignee_name": self.assignee_name, "concurrence_person": self.concurrence_person,
            "approval_person": self.approval_person, "reassigned_compliance": self.reassigned_compliance, "reason": self.reason
        }
#########################################################
# Get Compliance Approval List
#########################################################
class GetComplianceApprovalList(Request):
    def __init__(self, legal_entity_id, unit_id, start_count):
        self.legal_entity_id = legal_entity_id
        self.unit_id = unit_id
        self.start_count = start_count

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["le_id", "unit_id", "start_count"])
        return GetComplianceApprovalList(data.get("le_id"), data.get("unit_id"), data.get("start_count"))

    def to_inner_structure(self):
        return {"le_id": self.legal_entity_id, "unit_id": self.unit_id, "start_count": self.start_count}
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
        data = parse_dictionary(data, [
            "le_id", "compliance_history_id", "approval_status",
            "remarks",  "next_due_date", "validity_date"
        ])
        return ApproveCompliance(
            data.get("le_id"), data.get("compliance_history_id"), data.get("approval_status"),
            data.get("remarks"), data.get("next_due_date"), data.get("validity_date"),
        )

    def to_inner_structure(self):
        return {
            "le_id": self.legal_entity_id, "compliance_history_id": self.compliance_history_id,
            "approval_status": self.approval_status, "remarks": self.remarks,
            "next_due_date": self.next_due_date, "validity_date": self.validity_date
        }

####################################################
# Get Completed Task Current Year (Past Data)
####################################################
class GetPastRecordsFormData(Request):
    def __init__(self, legal_entity_id):
        self.legal_entity_id = legal_entity_id

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["le_id"])
        return GetPastRecordsFormData(data.get("le_id"))

    def to_inner_structure(self):
        return {"le_id": self.legal_entity_id}
####################################################
# Get Completed Task Current Year (Past Data)
####################################################
class GetStatutoriesByUnit(Request):
    def __init__(
        self, legal_entity_id, unit_id, domain_id, level_1_statutory_name,
        compliance_frequency, start_count
    ):
        self.legal_entity_id = legal_entity_id
        self.unit_id = unit_id
        self.domain_id = domain_id
        self.level_1_statutory_name = level_1_statutory_name
        self.compliance_frequency = compliance_frequency
        self.start_count = start_count

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "le_id", "unit_id", "domain_id",
            "level_1_statutory_name", "compliance_task_frequency",
            "start_count"
        ])
        return GetStatutoriesByUnit(
            data.get("le_id"), data.get("unit_id"), data.get("domain_id"),
            data.get("level_1_statutory_name"), data.get("compliance_task_frequency"), data.get("start_count"),
        )

    def to_inner_structure(self):
        return {
            "le_id": self.legal_entity_id, "unit_id": self.unit_id, "domain_id": self.domain_id,
            "level_1_statutory_name": self.level_1_statutory_name, "compliance_task_frequency": self.compliance_frequency,
            "start_count": self.start_count
        }


class SavePastRecords(Request):
    def __init__(self, legal_entity_id, compliances):
        self.legal_entity_id = legal_entity_id
        self.compliances = compliances

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["le_id", "pr_compliances_1"])
        return SavePastRecords(data.get("le_id"), data.get("pr_compliances_1"))

    def to_inner_structure(self):
        return {
            "le_id": self.legal_entity_id, "pr_compliances_1": self.compliances
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
        return {"le_id": self.legal_entity_id}


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
        return {"le_id": self.legal_entity_id, "d_id": self.domain_id}


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
        return GetReviewSettingsComplianceFilters(
            data.get("le_id"), data.get("d_id"), data.get("unit_ids"), data.get("f_id"), data.get("sno"),
        )

    def to_inner_structure(self):
        return {
            "le_id": self.legal_entity_id, "d_id": self.domain_id, "unit_ids": self.unit_ids,
            "f_id": self.f_id, "sno": self.sno
        }


class SaveReviewSettingsCompliance(Request):
    def __init__(self, legal_entity_id, rs_compliances):
        self.legal_entity_id = legal_entity_id
        self.rs_compliances = rs_compliances

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["le_id", "rs_compliances"])
        return SaveReviewSettingsCompliance(data.get("le_id"), data.get("rs_compliances"))

    def to_inner_structure(self):
        return {
            "le_id": self.legal_entity_id, "rs_compliances": self.rs_compliances
        }


class SaveReviewSettingsComplianceDict(object):
    def __init__(
        self, compliance_id, legal_entity_id, domain_id, f_id, unit_ids, repeat_by,
        repeat_type_id, due_date, trigger_before_days, statu_dates, old_repeat_by,
        old_repeat_type_id, old_due_date, old_statu_dates
    ):
        self.compliance_id = compliance_id
        self.legal_entity_id = legal_entity_id
        self.domain_id = domain_id
        self.f_id = f_id
        self.unit_ids = unit_ids
        self.repeat_by = repeat_by
        self.repeat_type_id = repeat_type_id
        self.due_date = due_date
        self.trigger_before_days = trigger_before_days
        self.statu_dates = statu_dates
        self.old_repeat_by = old_repeat_by
        self.old_repeat_type_id = old_repeat_type_id
        self.old_due_date = old_due_date
        self.old_statu_dates = old_statu_dates

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "comp_id", "le_id", "d_id",  "f_id", "unit_ids", "repeat_by",
            "repeat_type_id", "due_date", "trigger_before_days", "statu_dates",
            "old_repeat_by", "old_repeat_type_id", "old_due_date", "old_statu_dates"
            ])

        return SaveReviewSettingsComplianceDict(
            data.get("comp_id"), data.get("le_id"), data.get("d_id"), data.get("f_id"),
            data.get("unit_ids"), data.get("repeat_by"), data.get("repeat_type_id"), data.get("due_date"),
            data.get("trigger_before_days"), data.get("statu_dates"), data.get("old_repeat_by"), data.get("old_repeat_type_id"),
            data.get("old_due_date"), data.get("old_statu_dates"),
        )

    def to_structure(self):
        return {
            "comp_id": self.comp_id, "le_id": self.legal_entity_id,
            "d_id": self.domain_id, "f_id": self.f_id, "unit_ids": self.unit_ids,
            "repeat_by": self.repeat_by, "repeat_type_id": self.repeat_type_id,
            "due_date": self.due_date, "trigger_before_days": self.trigger_before_days,
            "statu_dates": self.statu_dates, "old_repeat_by": self.old_repeat_by,
            "old_repeat_type_id": self.old_repeat_type_id, "old_due_date": self.old_due_date,
            "old_statu_dates": self.old_statu_dates,
        }


class GetChartFilters(Request):
    def __init__(self, legal_entity_ids):
        self.legal_entity_ids = legal_entity_ids

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["le_ids"])
        return GetChartFilters(data.get("le_ids"))

    def to_inner_structure(self):
        return {"le_ids": self.legal_entity_ids}

class GetReassignComplianceFilters(Request):
    def __init__(self, legal_entity_id):
        self.legal_entity_id = legal_entity_id

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["le_id"])
        return GetReassignComplianceFilters(data.get("le_id"))

    def to_inner_structure(self):
        return {"le_id": self.legal_entity_id}

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
            data.get("le_id"), data.get("d_id"), data.get("usr_id"), data.get("user_type_id"), data.get("unit_id")
        )

    def to_inner_structure(self):
        return {
            "le_id": self.legal_entity_id, "d_id": self.d_id, "usr_id": self.usr_id,
            "user_type_id": self.user_type_id, "unit_id": self.unit_id
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
            data.get("le_id"), data.get("d_id"), data.get("usr_id"),
            data.get("user_type_id"), data.get("u_ids"), data.get("r_count")
        )

    def to_inner_structure(self):
        return {
            "le_id": self.legal_entity_id, "d_id": self.d_id, "usr_id": self.usr_id,
            "user_type_id": self.user_type_id, "u_ids": self.u_ids, "r_count": self.r_count
        }

class HaveCompliances(Request):
    def __init__(self, legal_entity_id, user_id):
        self.legal_entity_id = legal_entity_id
        self.user_id = user_id

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["le_id", "user_id"])
        return HaveCompliances(data.get("le_id"), data.get("user_id"))

    def to_inner_structure(self):
        return {"le_id": self.legal_entity_id, "user_id": self.user_id}

class GetAssigneewiseComplianesFilters(Request):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return GetAssigneewiseComplianesFilters()

    def to_inner_structure(self):
        return {}


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
            data.get("w_id"), data.get("width"), data.get("height"), data.get("pin_status")
        )

    def to_structure(self):
        return {
            "w_id": self.widget_id, "width": self.width, "height": self.height, "pin_status": self.pin_status
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
            data.get("w_id"), data.get("w_name"), data.get("active_status")
        )

    def to_structure(self):
        return {
            "w_id": self.widget_id, "w_name": self.widget_name, "active_status": self.active_status
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
        return {"theme": self.theme}


def _init_Request_class_map():

    classes = [
        GetStatutorySettingsFilters, ChangeStatutorySettingsLock, GetStatutorySettings, GetSettingsCompliances, UpdateStatutorySettings,
        GetAssignCompliancesFormData, GetComplianceForUnits, SaveAssignedCompliance, GetUserwiseCompliances, ReassignCompliance,
        GetComplianceApprovalList, ApproveCompliance, GetPastRecordsFormData,
        GetStatutoriesByUnit, SavePastRecords, GetReviewSettingsFilters,
        GetReviewSettingsUnitFilters, GetReviewSettingsComplianceFilters, SaveReviewSettingsCompliance,
        GetAssignComplianceUnits, GetComplianceTotalToAssign, GetReAssignComplianceUnits, GetReAssignComplianceForUnits,
        GetAssigneewiseComplianesFilters, GetUserToAssignCompliance, GetChartFilters,
        GetReassignComplianceFilters, GetUserWidgetData, SaveWidgetData, ChangeThemes, HaveCompliances, SaveStatutorySettings

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
        domain_id, location
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
        self.location = location

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "u_id", "u_name", "address", "c_name", "d_name",
            "is_new", "is_locked", "allow_unlock",
            "usr_by", "usr_on", "r_count", "d_id", "location"
        ])

        return UnitStatutoryCompliances(
            data.get("u_id"), data.get("u_name"), data.get("address"),
            data.get("d_name"), data.get("is_new"), data.get("is_locked"),
            data.get("allow_unlock"), data.get("usr_by"), data.get("usr_on"),
            data.get("r_count"), data.get("d_id"), data.get("location"),
        )

    def to_structure(self):
        return {
            "u_id": self.unit_id, "u_name": self.unit_name, "address": self.address,
            "d_name": self.domain_name, "is_new": self.is_new, "is_locked": self.is_locked,
            "allow_unlock": self.allow_unlock, "usr_by": self.updated_by, "usr_on": self.updated_on,
            "r_count": self.r_count, "d_id": self.domain_id, "location": self.location
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
            "le_did_infos": self.le_info, "div_infos": self.div_info, "cat_info": self.cat_info
        }

class GetStatutorySettingsSuccess(Response):
    def __init__(self, statutories):
        self.statutories = statutories

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["statutories"])
        return GetStatutorySettingsSuccess(data.get("statutories"))

    def to_inner_structure(self):
        return {"statutories": self.statutories}

class GetSettingsCompliancesSuccess(Response):
    def __init__(self, statutories, total_record):
        self.statutories = statutories
        self.total_record = total_record

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["applicable_statu", "r_count"])
        return GetSettingsCompliancesSuccess(data.get("applicable_statu"), data.get("r_count"))

    def to_inner_structure(self):
        return {"applicable_statu": self.statutories, "r_count": self.total_record}

class UpdateStatutorySettingsSuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return UpdateStatutorySettingsSuccess()

    def to_inner_structure(self):
        return {}


class ComplianceUpdateFailed(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return ComplianceUpdateFailed()

    def to_inner_structure(self):
        return {}


class InvalidPassword(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return InvalidPassword()

    def to_inner_structure(self):
        return {}

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

        return GetAssignCompliancesFormDataSuccess(
            data.get("domains"), data.get("le_did_infos"), data.get("div_infos"), data.get("cat_info"),
        )

    def to_inner_structure(self):
        return {
            "le_did_infos": self.legal_entities, "div_infos": self.divisions,
            "cat_info": self.categories, "domains": self.domains
        }

class GetAssignComplianceUnitsSuccess(Response):
    def __init__(self, units, unit_comp_frequency, validity_days, two_level_approve):
        self.units = units
        self.unit_comp_frequency = unit_comp_frequency
        self.validity_days = validity_days
        self.two_level_approve = two_level_approve

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["assign_units", "unit_comp_frequency", "validity_days", "t_l_approve"])
        return GetAssignComplianceUnitsSuccess(
            data.get("units"), data.get("unit_comp_frequency"), data.get("validity_days"), data.get("t_l_approve")
        )

    def to_inner_structure(self):
        return {
            "assign_units": self.units, "unit_comp_frequency": self.unit_comp_frequency, "validity_days": self.validity_days,
            "t_l_approve": self.two_level_approve
        }

class GetUserToAssignComplianceSuccess(Request):
    def __init__(self, assign_users, two_level_approve):
        self.assign_users = assign_users
        self.two_level_approve = two_level_approve

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["assign_users", "t_l_approve"])
        return GetUserToAssignComplianceSuccess(
            data.get("assign_users"), data.get("t_l_approve")
        )

    def to_inner_structure(self):
        return {
            "assign_users": self.assign_users, "t_l_approve": self.two_level_approve
        }


class GetComplianceTotalToAssignSuccess(Request):
    def __init__(self, record_count):
        self.record_count = record_count

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["r_count"])
        return GetComplianceTotalToAssignSuccess(data.get("r_count"))

    def to_inner_structure(self):
        return {"r_count": self.record_count}

class GetComplianceForUnitsSuccess(Response):
    def __init__(self, level_one_name, statutories):
        self.level_one_name = level_one_name
        self.statutories = statutories

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["level_one_name", "assign_statutory"])
        return GetComplianceForUnitsSuccess(data.get("assign_statutory"), data.get("level_one_name"))

    def to_inner_structure(self):
        return {
            "level_one_name": self.level_one_name, "assign_statutory": self.statutories,
        }

class SaveAssignedComplianceSuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return SaveAssignedComplianceSuccess()

    def to_inner_structure(self):
        return {}

class InvalidDueDate(Response):
    def __init__(self, compliance_task):
        self.compliance_task = compliance_task

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["compliance_task"])
        return InvalidDueDate(data.get("compliance_task"))

    def to_inner_structure(self):
        return {"compliance_task": self.compliance_task}

class AssigneeNotBelongToUnit(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return AssigneeNotBelongToUnit()

    def to_inner_structure(self):
        return {}

class ConcurrenceNotBelongToUnit(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return ConcurrenceNotBelongToUnit()

    def to_inner_structure(self):
        return {}

class ApprovalPersonNotBelongToUnit(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return ApprovalPersonNotBelongToUnit()

    def to_inner_structure(self):
        return {}

class ReassignComplianceSuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return ReassignComplianceSuccess()

    def to_inner_structure(self):
        return {}
#########################################################
# Get Approval list Response
########################################################
class GetComplianceApprovalListSuccess(Response):
    def __init__(self, approval_list, approval_status, current_date, total_count):
        self.approval_list = approval_list
        self.approval_status = approval_status
        self.current_date = current_date
        self.total_count = total_count

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["approval_list", "approval_status", "current_date", "total_count"])
        return GetComplianceApprovalListSuccess(
            data.get("approval_list"), data.get("approval_status"), data.get("current_date"), data.get("total_count")
        )

    def to_inner_structure(self):
        return {
            "approval_list": self.approval_list, "approval_status": self.approval_status,
            "current_date" : self.current_date, "total_count": self.total_count
        }

class ApproveComplianceSuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return ApproveComplianceSuccess()

    def to_inner_structure(self):
        return {}

####################################################
# Get Completed Task Current Year (Past Data)
####################################################
class GetPastRecordsFormDataSuccess(Response):
    def __init__(
        self, countries, business_groups, legal_entities, divisions, category, units,
        domains, level_1_statutories, compliance_frequency
    ):
        self.countries = countries
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
        data = parse_dictionary(data, [
            "countries", "business_groups", "pr_legal_entities",
            "client_divisions", "pr_categories", "in_units", "domains", "level_1_statutories", "compliance_frequency"
        ])

        return GetPastRecordsFormDataSuccess(
            data.get("countries"), data.get("business_groups"), data.get("pr_legal_entities"),
            data.get("client_divisions"), data.get("pr_categories"), data.get("in_units"),
            data.get("domains"), data.get("level_1_statutories"), data.get("compliance_frequency"),
        )

    def to_inner_structure(self):
        return {
            "countries": self.countries, "business_groups": self.business_groups,
            "pr_legal_entities": self.legal_entities, "client_divisions": self.divisions,
            "pr_categories": self.category, "in_units": self.units, "domains": self.domains,
            "level_1_statutories": self.level_1_statutories, "compliance_frequency" : self.compliance_frequency
        }

class GetStatutoriesByUnitSuccess(Response):
    def __init__(self, statutory_wise_compliances, users, total_count):
        self.statutory_wise_compliances = statutory_wise_compliances
        self.users = users
        self.total_count = total_count

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["statutory_wise_compliances", "pr_users", "total_count"])
        return GetStatutoriesByUnitSuccess(
            data.get("statutory_wise_compliances"), data.get("pr_users"), data.get("total_count"),
        )

    def to_inner_structure(self):
        return {
            "statutory_wise_compliances" : self.statutory_wise_compliances,
            "pr_users" : self.users, "total_count": self.total_count
        }

class NotEnoughSpaceAvailable(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return NotEnoughSpaceAvailable()

    def to_inner_structure(self):
        return {}

class SavePastRecordsSuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return SavePastRecordsSuccess()

    def to_inner_structure(self):
        return {}

class SavePastRecordsFailed(Response):
    def __init__(self, error):
        self.error = error

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["error"])
        return SavePastRecordsFailed(data.get("error"))

    def to_inner_structure(self):
        return {"error" : self.error}


class ChangeStatutorySettingsLockSuccess(Request):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [])
        return ChangeStatutorySettingsLockSuccess()

    def to_inner_structure(self):
        return {}

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
            "le_did_infos", "div_infos", "chart_units" "d_months", "g_name",
            "cat_info"
        ])
        countries = data.get("countries")
        domains = data.get("d_info")
        business_groups = data.get("bg_groups")
        legal_entities = data.get("le_did_infos")
        divisions = data.get("div_infos")
        units = data.get("chart_units")
        domain_month = data.get("d_months")
        group_name = data.get("g_name")
        cat_info = data.get("cat_info")
        return GetChartFiltersSuccess(
            countries, domains, business_groups, legal_entities,
            divisions, units, domain_month, group_name, cat_info
        )

    def to_inner_structure(self):
        return {
            "countries": self.countries, "d_info": self.domains, "bg_groups": self.business_groups,
            "le_did_infos": self.legal_entities, "div_infos": self.divisions,
            "chart_units": self.units, "d_months": self.domain_month,
            "g_name": self.group_name, "cat_info": self.categories
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

        return GetAssigneewiseComplianesFiltersSuccess(
            data.get("countries"), data.get("business_groups"), data.get("legal_entities"),
            data.get("client_divisions"), data.get("client_categories"), data.get("units"),
            data.get("users"), data.get("d_info")
        )

    def to_inner_structure(self):
        return {
            "countries": self.countries, "business_groups": self.business_groups,
            "legal_entities": self.legal_entities, "client_divisions": self.divisions,
            "client_categories": self.categories, "units": self.units, "users": self.users, "d_info": self.domains
        }

class HaveComplianceSuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return HaveComplianceSuccess()

    def to_inner_structure(self):
        return {}

class HaveComplianceFailed(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return HaveComplianceFailed()

    def to_inner_structure(self):
        return {}


class GetReassignComplianceFiltersSuccess(Response):
    def __init__(self, domains, units, legal_entity_users):
        self.domains = domains
        self.units = units
        self.legal_entity_users = legal_entity_users

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["domains", "units", "legal_entity_users"])
        return GetReassignComplianceFiltersSuccess(
            data.get("domains"), data.get("units"), data.get("legal_entity_users"),
        )

    def to_inner_structure(self):
        return {
            "domains": self.domains, "units": self.units, "legal_entity_users": self.legal_entity_users
        }

class GetReAssignComplianceUnitsSuccess(Response):
    def __init__(self, units):
        self.units = units

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["reassign_units"])
        return GetReAssignComplianceUnitsSuccess(data.get("units"))

    def to_inner_structure(self):
        return {"reassign_units": self.units}

class GetReAssignComplianceForUnitsSuccess(Response):
    def __init__(self, reassign_compliances):
        self.reassign_compliances = reassign_compliances

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["reassign_compliances"])
        return GetReAssignComplianceForUnitsSuccess(data.get("reassign_compliances"))

    def to_inner_structure(self):
        return {"reassign_compliances": self.reassign_compliances}


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
            "widget_info": self.widget_order_info, "widget_list": self.widget_list
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


class SaveReviewSettingsComplianceSuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return SaveReviewSettingsComplianceSuccess()

    def to_inner_structure(self):
        return {}

def _init_Response_class_map():
    classes = [
        GetStatutorySettingsSuccess, GetSettingsCompliancesSuccess, UpdateStatutorySettingsSuccess,
        InvalidPassword, GetAssignCompliancesFormDataSuccess, GetComplianceForUnitsSuccess,
        SaveAssignedComplianceSuccess, InvalidDueDate, AssigneeNotBelongToUnit, ConcurrenceNotBelongToUnit,
        ApprovalPersonNotBelongToUnit, ReassignComplianceSuccess,
        GetComplianceApprovalListSuccess, ApproveComplianceSuccess, GetPastRecordsFormDataSuccess,
        GetStatutoriesByUnitSuccess, SavePastRecordsSuccess, SavePastRecordsFailed,
        ComplianceUpdateFailed,
        GetStatutorySettingsFiltersSuccess, ChangeStatutorySettingsLockSuccess,
        GetAssignComplianceUnitsSuccess,
        GetComplianceTotalToAssignSuccess, GetUserToAssignComplianceSuccess,
        GetChartFiltersSuccess, GetReassignComplianceFiltersSuccess, GetReAssignComplianceUnitsSuccess,
        GetReAssignComplianceUnitsSuccess, GetAssigneewiseComplianesFilters,
        GetUserWidgetDataSuccess, SaveWidgetDataSuccess, SaveReviewSettingsComplianceSuccess, HaveComplianceSuccess,
        HaveComplianceFailed
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
            "session_token": self.session_token, "request": Request.to_structure(self.request)
        }

#
# ASSIGNED_COMPLIANCE
#

class ASSIGNED_COMPLIANCE(object):
    def __init__(
        self, compliance_id, compliance_name, statutory_dates,
        due_date, validity_date, trigger_before, unit_ids, repeat_by, r_every, frequency_
    ):
        self.compliance_id = compliance_id
        self.compliance_name = compliance_name
        self.statutory_dates = statutory_dates
        self.due_date = due_date
        self.validity_date = validity_date
        self.trigger_before = trigger_before
        self.unit_ids = unit_ids
        self.repeat_by = repeat_by
        self.r_every = r_every
        self.frequency = frequency_

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "comp_id", "comp_name", "statu_dates",
            "d_date", "v_date", "trigger_before_days", "u_ids", "repeat_by", "r_every", "frequency"
        ])

        return ASSIGNED_COMPLIANCE(
            data.get("comp_id"), data.get("comp_name"), data.get("statu_dates"),
            data.get("d_date"), data.get("v_date"), data.get("trigger_before_days"),
            data.get("u_ids"), data.get("repeat_by"), data.get("r_every"), data.get("frequency")
        )

    def to_structure(self):
        return {
            "comp_id": self.compliance_id, "comp_name": self.compliance_name,
            "statu_dates": self.statutory_dates, "d_date": self.due_date,
            "v_date": self.validity_date, "trigger_before_days": self.trigger_before,
            "u_ids": self.unit_ids, "repeat_by": self.repeat_by, "r_every": self.r_every,
            "frequency": self.frequency_
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

        return REASSIGNED_COMPLIANCE(
            data.get("u_id"), data.get("comp_id"), data.get("compliance_name"), data.get("c_h_id"),
            data.get("d_date"), data.get("o_assignee"), data.get("o_concurrence_person"), data.get("o_approval_person"),
        )

    def to_structure(self):
        return {
            "u_id": self.u_id, "comp_id": self.comp_id, "compliance_name": self.compliance_name,
            "c_h_id": self.c_h_id, "d_date": self.d_date, "o_assignee": self.o_assignee,
            "o_concurrence_person": self.o_concurrence_person, "o_approval_person": self.o_approval_person,
        }

#
# PAST_RECORD_COMPLIANCE
#

class PAST_RECORD_COMPLIANCE(object):
    def __init__(
        self, unit_id, compliance_id, due_date, completion_date, documents,
        completed_by
    ):
        self.unit_id = unit_id
        self.compliance_id = compliance_id
        self.due_date = due_date
        self.completion_date = completion_date
        self.documents = documents
        self.completed_by = completed_by

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(
            data, [
                    "unit_id", "compliance_id", "due_date", "completion_date",
                    "documents", "pr_completed_by"
                ]
        )
        return PAST_RECORD_COMPLIANCE(
            data.get("unit_id"), data.get("compliance_id"), data.get("due_date"),
            data.get("completion_date"), data.get("documents"), data.get("pr_completed_by"),
        )

    def to_structure(self):
        return {
            "unit_id": self.unit_id, "compliance_id": self.compliance_id,
            "due_date": self.due_date, "completion_date": self.completion_date,
            "documents": self.documents, "pr_completed_by": self.completed_by
        }

#
# UNIT_WISE_STATUTORIES
#

class UNIT_WISE_STATUTORIES(object):
    def __init__(
        self, compliance_id, compliance_name, description,
        frequency, statutory_date, due_date, applicable_units,
        summary, r_every, repeat_by
    ):
        self.compliance_id = compliance_id
        self.compliance_name = compliance_name
        self.description = description
        self.frequency = frequency
        self.statutory_date = statutory_date
        self.due_date = due_date
        self.applicable_units = applicable_units
        self.summary = summary
        self.r_every = r_every
        self.repeat_by = repeat_by

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "comp_id", "comp_name", "descp" "freq", "statu_dates", "due_date_list",
            "applicable_units", "summary", "r_every", "repeat_by"
        ])

        return UNIT_WISE_STATUTORIES(
            data.get("comp_id"), data.get("comp_name"), data.get("descp"),
            data.get("freq"), data.get("statu_dates"), data.get("due_date_list"),
            data.get("applicable_units"), data.get("summary"), data.get("r_every"), data.get("repeat_by")
        )

    def to_structure(self):
        return {
            "comp_id": self.compliance_id, "comp_name": self.compliance_name,
            "descp": self.description, "freq": self.frequency, "statu_dates": self.statutory_date,
            "due_date_list": self.due_date, "applicable_units": self.applicable_units,
            "summary": self.summary, "r_every": self.r_every, "repeat_by": self.repeat_by
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
        data = parse_dictionary(data, [
            "compliance_id", "compliance_name", "description", "compliance_task_frequency",
            "pr_statutory_date", "due_date", "assignee_name", "assignee_id"
        ])
        return UNIT_WISE_STATUTORIES_FOR_PAST_RECORDS(
            data.get("compliance_id"), data.get("compliance_name"), data.get("description"),
            data.get("compliance_task_frequency"), data.get("pr_statutory_date"), data.get("due_date"),
            data.get("assignee_name"), data.get("assignee_id")
        )

    def to_structure(self):
        return {
            "compliance_id": self.compliance_id, "compliance_name": self.compliance_name,
            "description": self.description, "compliance_task_frequency": self.frequency,
            "pr_statutory_date": self.statutory_date, "due_date": self.due_date,
            "assignee_name" : self.assignee_name, "assignee_id": self.assignee_id
        }

#
# ASSIGN_COMPLIANCE_UNITS
#

class ASSIGN_COMPLIANCE_UNITS(object):
    def __init__(
        self, unit_id, unit_name, address, postal_code, category_id, division_id
    ):
        self.unit_id = unit_id
        self.unit_name = unit_name
        self.address = address
        self.postal_code = postal_code
        self.category_id = category_id
        self.division_id = division_id

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "u_id", "u_name", "address", "postal_code", "category_id", "division_id"
        ])
        return ASSIGN_COMPLIANCE_UNITS(
            data.get("u_id"), data.get("u_name"), data.get("address"), data.get("postal_code"), data.get("category_id"), data.get("division_id")
        )

    def to_structure(self):
        return {
            "u_id": self.unit_id, "u_name": self.unit_name, "address": self.address, "postal_code": self.postal_code, "category_id": self.category_id, "division_id": self.division_id
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
        return PastRecordUnits(
            data.get("unit_id"), data.get("unit_name"), data.get("address"), data.get("division_id"),
            data.get("legal_entity_id"), data.get("business_group_id"), data.get("country_id"), data.get("domain_ids"),
        )

    def to_structure(self):
        return {
            "unit_id": self.unit_id, "unit_name": self.unit_name, "address": self.address,
            "division_id": self.division_id, "legal_entity_id": self.legal_entity_id,
            "business_group_id": self.business_group_id, "country_id": self.country_id,
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
        return ASSIGN_COMPLIANCE_USER(
            data.get("usr_id"), data.get("sp_id"), data.get("emp_name"), data.get("user_level"),
            data.get("s_u_id"), data.get("u_ids"), data.get("d_ids"), data.get("is_assignee"),
            data.get("is_approver"), data.get("is_concurrence"), data.get("s_u_name")
        )

    def to_structure(self):
        return {
            "usr_id": self.user_id, "s_p_id": self.service_provider_id,
            "emp_name": self.user_name, "user_level": self.user_level,
            "s_u_id": self.seating_unit_id, "u_ids": self.unit_ids, "d_ids": self.domain_ids,
            "is_assignee": self.is_assignee, "is_concurrence": self.is_concurrence,
            "is_approver": self.is_approver, "s_u_name": self.seating_unit_name
        }


################################################################
# APPROVALCOMPLIANCE - Used In Get Approval Compliances list
###############################################################
class APPROVALCOMPLIANCE(object):
    def __init__(
        self, compliance_history_id, compliance_name, description,
        domain_name, domain_id, start_date, due_date, delayed_by, compliance_frequency,
        documents, file_names, upload_date, completion_date, next_due_date, concurrenced_by,
        concurrence_status, approve_status, current_status,
        remarks, action, statutory_dates, validity_date, validity_settings_days, unit_id,
        unit_name, unit_address, assignee_id, assignee_name
    ):
        self.compliance_history_id = compliance_history_id
        self.compliance_name = compliance_name
        self.description = description
        self.domain_name = domain_name
        self.domain_id = domain_id
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
        self.concurrence_status = concurrence_status
        self.approve_status = approve_status
        self.current_status = current_status
        self.remarks = remarks
        self.action = action
        self.statutory_dates = statutory_dates
        self.validity_date = validity_date
        self.validity_settings_days = validity_settings_days
        self.unit_id = unit_id
        self.unit_name = unit_name
        self.unit_address = unit_address
        self.assignee_id = assignee_id
        self.assignee_name = assignee_name

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(
            data, [
                "compliance_history_id", "compliance_name",
                "description", "domain_name", "domain_id", "file_names", "start_date", "due_date", "delayed_by",
                "compliance_task_frequency", "uploaded_documents", "upload_date", "completion_date",
                "next_due_date", "concurrenced_by", "concurrence_status", "approve_status", "current_status",
                "remarks", "action",
                "statutory_dates", "validity_date", "validity_settings_days", "unit_id", "unit_name",
                "unit_address", "assignee_id", "assignee_name"
            ]
        )

        return APPROVALCOMPLIANCE(
            data.get("compliance_history_id"), data.get("compliance_name"), data.get("description"),
            data.get("domain_name"), data.get("domain_id"), data.get("file_names"), data.get("start_date"),
            data.get("due_date"), data.get("delayed_by"), data.get("compliance_task_frequency"), data.get("uploaded_documents"),
            data.get("upload_date"), data.get("completion_date"), data.get("next_due_date"), data.get("concurrenced_by"),
            data.get("concurrence_status"), data.get("approve_status"), data.get("current_status"),
            data.get("remarks"), data.get("action"), data.get("statutory_dates"), data.get("validity_date"),
            data.get("validity_settings_days"), data.get("unit_id"), data.get("unit_name"), data.get("unit_address"),
            data.get("assignee_id"), data.get("assignee_name"),
        )

    def to_structure(self):
        return {
            "compliance_history_id": self.compliance_history_id, "compliance_name": self.compliance_name,
            "description": self.description, "domain_name": self.domain_name, "domain_id": self.domain_id,
            "start_date": self.start_date, "due_date": self.due_date, "delayed_by": self.delayed_by,
            "compliance_task_frequency": self.compliance_frequency, "uploaded_documents": self.documents,
            "file_names": self.file_names, "upload_date": self.upload_date,
            "completion_date": self.completion_date, "next_due_date": self.next_due_date,
            "concurrenced_by": self.concurrenced_by, "concurrence_status": self.concurrence_status,
            "approve_status": self.approve_status, "current_status": self.current_status,
            "remarks": self.remarks, "action": self.action,
            "statutory_dates" : self.statutory_dates, "validity_date": self.validity_date,
            "validity_settings_days": self.validity_settings_days, "unit_id": self.unit_id,
            "unit_name": self.unit_name, "unit_address": self.unit_address, "assignee_id": self.assignee_id,
            "assignee_name": self.assignee_name
        }
#
# STATUTORY_WISE_COMPLIANCES
#

class STATUTORY_WISE_COMPLIANCES(object):
    def __init__(self, level_1_statutory_name, compliances):
        self.level_1_statutory_name = level_1_statutory_name
        self.compliances = compliances

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["level_1_statutory_name", "pr_compliances"])
        return STATUTORY_WISE_COMPLIANCES(
            data.get("level_1_statutory_name"), data.get("pr_compliances")
        )

    def to_structure(self):
        return {
            "level_1_statutory_name": self.level_1_statutory_name, "pr_compliances": self.compliances,
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
        return ComplianceUnitApplicability(
            data.get("u_id"), data.get("c_comp_id"), data.get("comp_app_status"),
            data.get("comp_opt_status"), data.get("comp_remarks"), data.get("is_new"), data.get("is_saved")
        )

    def to_structure(self):
        return {
            "unit_id": self.unit_id, "c_comp_id": self.client_compliance_id,
            "comp_app_status": self.compliance_applicable_status, "comp_opt_status": self.compliance_opted_status,
            "comp_remarks": self.compliance_remarks, "is_new": self.is_new, "is_saved": self.is_saved
        }


class ComplianceApplicability(object):
    def __init__(
        self,
        level_1_statutory_name, applicable_status, opted_status, not_applicable_remarks,
        compliance_id, compliance_name, description, statutory_provision,
        unit_wise_status, frequency_name
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
        self.frequency_name = frequency_name

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "lone_statu_name", "app_status", "opt_status", "not_app_remarks",
            "comp_id", "comp_name", "descp", "s_prov",
            "unit_wise_status", "frequency_name"
        ])
        return ComplianceApplicability(
            data.get("lone_statu_name"), data.get("app_status"), data.get("opt_status"),
            data.get("not_app_remarks"), data.get("comp_id"), data.get("comp_name"), data.get("descp"),
            data.get("s_prov"), data.get("unit_wise_status"), data.get("frequency_name"),
        )

    def to_structure(self):
        return {
            "lone_statu_name": self.level_1_statutory_name, "app_status": self.applicable_status,
            "opt_status": self.opted_status, "not_app_remarks": self.not_applicable_remarks,
            "comp_id": self.compliance_id, "comp_name": self.compliance_name,
            "descp": self.description, "s_prov": self.statutory_provision,
            "unit_wise_status": self.unit_wise_status, "frequency_name": self.frequency_name
        }


class GetReviewSettingsFiltersSuccess(Response):
    def __init__(self, compliance_frequency, domain_list):
        self.compliance_frequency = compliance_frequency
        self.domain_list = domain_list

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["compliance_frequency", "domain_list"])
        return GetReviewSettingsFiltersSuccess(
            data.get("compliance_frequency"), data.get("domain_list")
        )

    def to_inner_structure(self):
        return {
            "compliance_frequency": self.compliance_frequency, "domain_list": self.domain_list,
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
        return {"rs_unit_list": self.rs_unit_list}


class GetReviewSettingsComplianceFiltersSuccess(Response):
    def __init__(self, timeline, rs_compliance_list):
        self.timeline = timeline
        self.rs_compliance_list = rs_compliance_list

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["timeline", "rs_compliance_list"])
        return GetReviewSettingsComplianceFiltersSuccess(
            data.get("timeline"), data.get("rs_compliance_list")
        )

    def to_inner_structure(self):
        return {
            "timeline": self.timeline, "rs_compliance_list": self.rs_compliance_list
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
            "usr_id": self.user_id, "emp_name": self.employee_name, "emp_code": self.employee_code,
            "usr_cat_id": self.user_category_id, "s_u_id": self.seating_unit_id, "s_u_name": self.seating_unit_name,
            "is_assignee": self.is_assignee, "is_approver": self.is_approver,
            "u_l": self.user_level, "sp_id": self.service_provider_id, "sp_name": self.service_provider_name,
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

        return ASSIGN_COMPLIANCE_UNITS(
            data.get("u_id"), data.get("u_name"), data.get("address"), data.get("postal_code"),
            data.get("user_type_id"), data.get("no_of_compliances"),
        )

    def to_structure(self):
        return {
            "u_id": self.unit_id, "u_name": self.unit_name, "address": self.address,
            "postal_code": self.postal_code, "user_type_id": self.user_type_id,
            "no_of_compliances": self.no_of_compliances
        }

#
# REASSIGN_COMPLIANCES
#

class REASSIGN_COMPLIANCES(object):
    def __init__(
        self, u_id, u_name, act_name, task_type, compliance_name, comp_id, f_id, frequency, compliance_description,
        summary, trigger_before_days, assignee, assignee_name, concurrence_person, concurrer_name, approval_person, approver_name,
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
            "summary", "trigger_before_days", "assignee", "assignee_name", "concurrence_person", "concurrer_name", "approval_person", "approver_name",
            "c_h_id", "d_date", "v_date"
        ])

        return ASSIGN_COMPLIANCE_UNITS(
            data.get("u_id"), data.get("u_name"), data.get("act_name"), data.get("task_type"),
            data.get("compliance_name"), data.get("comp_id"), data.get("f_id"), data.get("frequency"),
            data.get("compliance_description"), data.get("summary"), data.get("trigger_before_days"),
            data.get("assignee"), data.get("assignee_name"), data.get("concurrence_person"), data.get("concurrer_name"),
            data.get("approval_person"), data.get("approver_name"), data.get("c_h_id"), data.get("d_date"), data.get("v_date"),
        )

    def to_structure(self):
        return {
            "u_id": self.u_id, "u_name": self.u_name, "act_name": self.act_name,
            "task_type": self.task_type, "compliance_name": self.compliance_name,
            "comp_id": self.comp_id, "f_id": self.f_id, "frequency": self.frequency,
            "compliance_description": self.compliance_description, "summary": self.summary,
            "trigger_before_days": self.trigger_before_days, "assignee": self.assignee,
            "assignee_name": self.assignee_name, "concurrence_person": self.concurrence_person,
            "concurrer_name": self.concurrer_name, "approval_person": self.approval_person,
            "approver_name": self.approver_name, "c_h_id": self.c_h_id, "d_date": self.d_date, "v_date": self.v_date
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
        return {"theme": self.theme_value}


#
# CHART_UNITS
#

class CHART_UNITS(object):
    def __init__(
        self, unit_id, unit_name, address, postal_code, country_id, domain_ids, legal_entity_id
    ):
        self.unit_id = unit_id
        self.unit_name = unit_name
        self.address = address
        self.postal_code = postal_code
        self.country_id = country_id
        self.domain_ids = domain_ids
        self.legal_entity_id = legal_entity_id

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "u_id", "u_name", "address", "postal_code", "country_id", "d_ids", "le_id"
        ])
        return CHART_UNITS(
            data.get("u_id"), data.get("u_name"), data.get("address"), data.get("postal_code"),
            data.get("country_id"), data.get("d_ids"), data.get("le_id")
        )

    def to_structure(self):
        return {
            "u_id": self.unit_id, "u_name": self.unit_name, "address": self.address,
            "postal_code": self.postal_code, "country_id": self.country_id,
            "d_ids": self.domain_ids, "le_id": self.legal_entity_id
        }
