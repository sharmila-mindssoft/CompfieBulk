from clientprotocol.jsonvalidators_client import (
    parse_enum, parse_dictionary, to_structure_dictionary_values
)

class SESSION_TYPE(object):
    # Web = "Web" # Android = "Android" # IOS = "IOS"

    def __init__(self, value):
        self._value = value

    @staticmethod
    def values():
        return ["Web", "Android", "IOS", "BlackBerry"]

    def value(self):
        return self._value

    @staticmethod
    def parse_structure(data):
        return parse_enum(data, SESSION_TYPE.values())

    def to_structure(self):
        return parse_enum(self._value, SESSION_TYPE.values())

class COMPLIANCE_APPROVAL_STATUS(object):
    # Concur = "Concur"     # RejectConcurrence = "Reject Concurrence"
    # Approve = "Approve"    # RejectApproval = "Reject Approval"
    # RectifyConcurrence = Rectify Concurrence # Rectify Approval = Rectify Approval

    def __init__(self, value):
        self._value = value

    @staticmethod
    def values():
        return ["Concur", "Reject Concurrence", "Approve", "Reject Approval", "Rectify Concurrence", "Rectify Approval"]

    def value(self):
        return self._value

    @staticmethod
    def parse_structure(data):
        return parse_enum(data, COMPLIANCE_APPROVAL_STATUS.values())

    def to_structure(self):
        return parse_enum(self._value, COMPLIANCE_APPROVAL_STATUS.values())

class FILTER_TYPE(object):
    # Group = "Group" # BusinessGroup = "BusinessGroup" # LegalEntity = "LegalEntity"
    # Division = "Division" # Unit = "Unit" # Consolidated = "Consolidated"

    def __init__(self, value):
        self._value = value

    @staticmethod
    def values():
        return [
            "Group", "BusinessGroup", "LegalEntity", "Division", "Category", "Unit", "Consolidated"
        ]

    def value(self):
        return self._value

    @staticmethod
    def parse_structure(data):
        return parse_enum(data, FILTER_TYPE.values())

    def to_structure(self):
        return parse_enum(self._value, FILTER_TYPE.values())

class COMPLIANCE_STATUS(object):
    # Complied = "Complied" # DelayedCompliance = "Delayed Compliance" # Inprogress = "Inprogress"
    # NotComplied = "Not Complied" # Rectify = "Rectify"

    def __init__(self, value):
        self._value = value

    @staticmethod
    def values():
        return ["Complied", "Delayed Compliance", "Inprogress", "Not Complied", "Rectify"]

    def value(self):
        return self._value

    @staticmethod
    def parse_structure(data):
        return parse_enum(data, COMPLIANCE_STATUS.values())

    def to_structure(self):
        return parse_enum(self._value, COMPLIANCE_STATUS.values())

class APPLICABILITY_STATUS(object):

    def __init__(self, value):
        self._value = value

    @staticmethod
    def values():
        return ["Not Complied", "Rejected", "Unassigned", "Not Opted"]

    def value(self):
        return self._value

    @staticmethod
    def parse_structure(data):
        return parse_enum(data, APPLICABILITY_STATUS.values())

    def to_structure(self):
        return parse_enum(self._value, APPLICABILITY_STATUS.values())

class COMPLIANCE_ACTIVITY_STATUS(object):
    # Submitted = "Submitted"  # Approved = "Approved"    # Rejected = "Rejected"    # Concurred = "Concurred"

    def __init__(self, value):
        self._value = value

    @staticmethod
    def values():
        return ["Submitted", "Approved", "Rejected", "Concurred"]

    def value(self):
        return self._value

    @staticmethod
    def parse_structure(data):
        return parse_enum(data, COMPLIANCE_ACTIVITY_STATUS.values())

    def to_structure(self):
        return parse_enum(self._value, COMPLIANCE_ACTIVITY_STATUS.values())

class NOT_COMPLIED_TYPE(object) :
    # below_30 = "Below 30"    # below_60 = "Below 60"    # below_90 = "Below 90" # above_90 = "Above 90"

    def __init__(self, value):
        self._value = value

    @staticmethod
    def values():
        return ["Below 30", "Below 60", "Below 90", "Above 90"]

    def value(self):
        return self._value

    @staticmethod
    def parse_structure(data):
        return parse_enum(data, NOT_COMPLIED_TYPE.values())

    def to_structure(self):
        return parse_enum(self._value, NOT_COMPLIED_TYPE.values())

class Form(object):
    def __init__(self, form_id, form_name, form_url, parent_menu, form_type):

        self.form_id = form_id
        self.form_name = form_name
        self.form_url = form_url
        self.parent_menu = parent_menu
        self.form_type = form_type

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "form_id", "form_name", "form_url", "parent_menu", "form_type"
        ])
        return Form(
            data.get("form_id"), data.get("form_name"), data.get("form_url"),
            data.get("parent_menu"), data.get("form_type")
        )

    def to_structure(self):
        data = {
            "form_id": self.form_id, "form_name": self.form_name,
            "form_url": self.form_url, "parent_menu": self.parent_menu, "form_type": self.form_type
        }
        return data

class Menu(object):
    def __init__(self, menus):
        self.menus = menus

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["menus"])
        menus = data.get("menus")
        return Menu(menus)

    def to_structure(self):
        return {"menus": self.menus}

class UserGroup(object):
    def __init__(
        self, user_group_id, user_category_id, user_group_name, is_active
    ):
        self.user_group_id = user_group_id
        self.user_category_id = user_category_id
        self.user_group_name = user_group_name
        self.is_active = is_active

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "user_group_id", "user_category_id", "user_group_name", "is_active"
        ])
        return UserGroup(
            data.get("user_group_id"), data.get("user_category_id"),
            data.get("user_group_name"), data.get("is_active")
        )

    def to_structure(self):
        data = {
            "user_group_id": self.user_group_id, "user_category_id": self.user_category_id,
            "user_group_name": self.user_group_name, "is_active": self.is_active,
        }
        return data

class Country(object):
    def __init__(self, country_id, country_name, is_active):
        self.country_id = country_id
        self.country_name = country_name
        self.is_active = is_active

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(
            data, ["c_id", "c_name", "is_active"])

        return Country(data.get("c_id"), data.get("c_name"), data.get("is_active"))

    def to_structure(self):
        return {
            "c_id": self.country_id, "c_name": self.country_name, "is_active": self.is_active
        }

class Domain(object):
    def __init__(
        self, domain_id, domain_name, legal_entity_id, is_active
    ):
        self.domain_id = domain_id
        self.domain_name = domain_name
        self.legal_entity_id = legal_entity_id
        self.is_active = is_active

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "d_id", "d_name", "le_id", "is_active"
        ])
        return Domain(
            data.get("d_id"), data.get("d_name"), data.get("le_id"), data.get("is_active")
        )

    def to_structure(self):
        data = {
            "d_id": self.domain_id, "d_name": self.domain_name,
            "le_id": self.legal_entity_id, "is_active": self.is_active,
        }
        return data

class DomainInfo(object):
    def __init__(
        self, domain_id, domain_name, is_active
    ):
        self.domain_id = domain_id
        self.domain_name = domain_name
        self.is_active = is_active

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "d_id", "d_name", "is_active"
        ])
        return DomainInfo(
            data.get("d_id"), data.get("d_name"), data.get("is_active")
        )

    def to_structure(self):
        data = {
            "d_id": self.domain_id, "d_name": self.domain_name, "is_active": self.is_active,
        }
        return data

class FileList(object):
    def __init__(self, file_size, file_name, file_content):
        self.file_size = file_size
        self.file_name = file_name
        self.file_content = file_content

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["file_size", "file_name", "file_content"])

        return FileList(data.get("file_size"), data.get("file_name"), data.get("file_content"))

    def to_structure(self):
        return {
            "file_size": self.file_size, "file_name": self.file_name, "file_content": self.file_content
        }

class ClientConfiguration(object):
    def __init__(self, country_id, domain_id, month_from, month_to):
        self.country_id = country_id
        self.domain_id = domain_id
        self.month_from = month_from
        self.month_to = month_to

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(
            data, ["country_id", "domain_id", "month_from", "month_to"]
        )
        return ClientConfiguration(
            data.get("country_id"), data.get("domain_id"), data.get("month_from"),
            data.get("month_to")
        )

    def to_structure(self):
        return {
            "country_id": self.country_id, "domain_id": self.domain_id,
            "month_from": self.month_from, "month_to": self.month_to,
        }

class ClientBusinessGroup(object):
    def __init__(self, business_group_id, business_group_name):
        self.business_group_id = business_group_id
        self.business_group_name = business_group_name

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(
            data, ["bg_id", "bg_name"])
        return ClientBusinessGroup(data.get("bg_id"), data.get("bg_name"))

    def to_structure(self):
        return {
            "bg_id": self.business_group_id, "bg_name": self.business_group_name,
        }

class ClientLegalEntity(object):
    def __init__(self, legal_entity_id, legal_entity_name, business_group_id):
        self.legal_entity_id = legal_entity_id
        self.legal_entity_name = legal_entity_name
        self.business_group_id = business_group_id

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["le_id", "le_name", "bg_id"])
        return ClientLegalEntity(data.get("le_id"), data.get("le_name"), data.get("bg_id"))

    def to_structure(self):
        data = {
            "le_id": self.legal_entity_id, "le_name": self.legal_entity_name,
            "bg_id": self.business_group_id,
        }
        return to_structure_dictionary_values(data)

class Category(object):
    def __init__(
        self, category_id, category_name, division_id, legal_entity_id,
        business_group_id
    ):
        self.category_id = category_id
        self.category_name = category_name
        self.division_id = division_id
        self.legal_entity_id = legal_entity_id
        self.business_group_id = business_group_id

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["cat_id", "cat_name", "div_id", "le_id", "bg_id"])
        return Category(
            data.get("cat_id"), data.get("cat_name"), data.get("div_id"), data.get("le_id"), data.get("bg_id")
        )

    def to_structure(self):
        return {
            "cat_id": self.category_id, "cat_name": self.category_name,
            "div_id": self.division_id, "le_id": self.legal_entity_id,
            "bg_id": self.business_group_id,
        }

class ClientDivision(object):
    def __init__(
        self, division_id, division_name, legal_entity_id, business_group_id
    ):
        self.division_id = division_id
        self.division_name = division_name
        self.legal_entity_id = legal_entity_id
        self.business_group_id = business_group_id

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["div_id", "div_name", "le_id", "bg_id"])

        return ClientDivision(
            data.get("div_id"), data.get("div_name"), data.get("le_id"), data.get("bg_id")
        )

    def to_structure(self):
        return {
            "div_id": self.division_id, "div_name": self.division_name,
            "le_id": self.legal_entity_id, "bg_id": self.business_group_id,
        }

class ClientCategory(object):
    def __init__(
        self, category_id, category_name, legal_entity_id, business_group_id, division_id
    ):
        self.category_id = category_id
        self.category_name = category_name
        self.legal_entity_id = legal_entity_id
        self.business_group_id = business_group_id
        self.division_id = division_id

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["cat_id", "cat_name", "le_id", "bg_id", "div_id"])

        return ClientCategory(
            data.get("cat_id"), data.get("cat_name"), data.get("le_id"), data.get("bg_id"), data.get("div_id")
        )

    def to_structure(self):
        return {
            "cat_id": self.category_id, "cat_name": self.category_name,
            "le_id": self.legal_entity_id, "bg_id": self.business_group_id, "div_id": self.division_id,
        }

class ClientUnit(object):
    def __init__(
        self, unit_id, division_id, category_id, legal_entity_id, business_group_id,
        unit_code, unit_name, address, domain_ids, country_id,
        is_closed
    ):
        self.unit_id = unit_id
        self.division_id = division_id
        self.category_id = category_id
        self.legal_entity_id = legal_entity_id
        self.business_group_id = business_group_id
        self.unit_code = unit_code
        self.unit_name = unit_name
        self.address = address
        self.domain_ids = domain_ids
        self.country_id = country_id
        self.is_closed = is_closed

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(
            data, [
                "unit_id", "division_id", "category_id", "legal_entity_id",
                "business_group_id", "unit_code", "unit_name", "address",
                "d_ids", "country_id", "is_closed"
            ]
        )
        return ClientUnit(
            data.get("unit_id"), data.get("division_id"), data.get("category_id"),
            data.get("legal_entity_id"), data.get("business_group_id"), data.get("unit_code"),
            data.get("unit_name"), data.get("address"), data.get("d_ids"), data.get("country_id"),
            data.get("is_closed")
        )

    def to_structure(self):
        return {
            "unit_id": self.unit_id, "division_id": self.division_id,
            "category_id": self.category_id, "legal_entity_id": self.legal_entity_id,
            "business_group_id": self.business_group_id, "unit_code": self.unit_code,
            "unit_name": self.unit_name, "address": self.address,
            "d_ids": self.domain_ids, "country_id": self.country_id,
            "is_closed" : self.is_closed
        }

class ClientAct(object):
    def __init__(
        self, domain_id, act
    ):
        self.domain_id = domain_id
        self.act = act

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["d_id", "act"])
        return Domain(data.get("d_id"), data.get("act"))

    def to_structure(self):
        data = {"d_id": self.domain_id, "act": self.act}
        return data

class ServiceProviderDetails(object):
    def __init__(
        self, service_provider_id, service_provider_name, short_name, contract_from,
        contract_to, contact_person, contact_no, email_id, mobile_no, address,
        is_active, is_blocked, unblock_days, remarks
    ):
        self.service_provider_id = service_provider_id
        self.service_provider_name = service_provider_name
        self.short_name = short_name
        self.contract_from = contract_from
        self.contract_to = contract_to
        self.contact_person = contact_person
        self.contact_no = contact_no
        self.email_id = email_id
        self.mobile_no = mobile_no
        self.address = address
        self.is_active = is_active
        self.is_blocked = is_blocked
        self.unblock_days = unblock_days
        self.remarks = remarks

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "service_provider_id", "service_provider_name", "short_name", "contract_from",
            "contact_person", "contact_no", "mobile_no",
            "email_id", "address", "is_active", "is_blocked", "unblock_days", "remarks"
        ])

        return ServiceProviderDetails(
            data.get("service_provider_id"), data.get("service_provider_name"),
            data.get("short_name"), data.get("contract_from"), data.get("contract_to"),
            data.get("contact_person"), data.get("contact_no"), data.get("mobile_no"),
            data.get("email_id"), data.get("address"), data.get("is_active"),
            data.get("is_blocked"), data.get("unblock_days"), data.get("remarks")
        )

    def to_structure(self):
        return {
            "s_p_id": self.service_provider_id, "s_p_name": self.service_provider_name,
            "s_p_short": self.short_name, "cont_from": self.contract_from,
            "cont_to": self.contract_to, "cont_person": self.contact_person,
            "cont_no": self.contact_no, "mob_no": self.mobile_no,
            "e_id": self.email_id, "address": self.address,
            "is_active": self.is_active, "is_blocked": self.is_blocked,
            "unblock_days": self.unblock_days, "remarks": self.remarks
        }
# ActiveCompliance for Current Task Details
class ActiveCompliance(object):
    def __init__(
        self, compliance_history_id, compliance_name, compliance_frequency,
        domain_name, domain_id, unit_id, duration_type, validity_settings_days, assigned_on, start_date,
        due_date, compliance_status, validity_date,
        next_due_date, ageing, format_file_name, unit_name, address,
        compliance_description, remarks, compliance_id, file_names, download_url
    ):
        self.compliance_history_id = compliance_history_id
        self.compliance_name = compliance_name
        self.compliance_frequency = compliance_frequency
        self.domain_name = domain_name
        self.domain_id = domain_id
        self.unit_id = unit_id
        self.validity_settings_days = validity_settings_days
        self.duration_type = duration_type
        self.assigned_on = assigned_on
        self.start_date = start_date
        self.due_date = due_date
        self.compliance_status = compliance_status
        self.validity_date = validity_date
        self.next_due_date = next_due_date
        self.ageing = ageing
        self.format_file_name = format_file_name
        self.unit_name = unit_name
        self.address = address
        self.compliance_description = compliance_description
        self.remarks = remarks
        self.compliance_id = compliance_id
        self.file_names = file_names
        self.download_url = download_url

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(
            data, [
                "compliance_history_id", "compliance_name",
                "compliance_task_frequency", "domain_name", "domain_id", "unit_id", "duration_type", "validity_settings_days",
                "assigned_on", "start_date", "due_date",
                "compliance_status", "validity_date", "next_due_date", "ageing",
                "compliance_file_name", "unit_name", "address", "compliance_description",
                "remarks", "compliance_id", "file_names", "compliance_download_url"
            ]
        )
        return ActiveCompliance(
            data.get("compliance_history_id"), data.get("compliance_name"),
            data.get("compliance_task_frequency"), data.get("domain_name"), data.get("domain_id"),
            data.get("unit_id"), data.get("validity_settings_days"), data.get("duration_type"),
            data.get("assigned_on"), data.get("start_date"), data.get("due_date"),
            data.get("compliance_status"), data.get("validity_date"), data.get("next_due_date"),
            data.get("ageing"), data.get("compliance_file_name"), data.get("unit_name"),
            data.get("address"), data.get("compliance_description"), data.get("remarks"), data.get("compliance_id"),
            data.get("file_names"), data.get("compliance_download_url")
        )

    def to_structure(self):
        return {
            "compliance_history_id": self.compliance_history_id, "compliance_name": self.compliance_name,
            "compliance_task_frequency": self.compliance_frequency, "domain_name": self.domain_name,
            "domain_id": self.domain_id, "unit_id": self.unit_id, "duration_type": self.duration_type,
            "validity_settings_days": self.validity_settings_days, "assigned_on": self.assigned_on,
            "start_date": self.start_date, "due_date": self.due_date, "compliance_status": self.compliance_status,
            "validity_date": self.validity_date, "next_due_date": self.next_due_date,
            "ageing": self.ageing, "compliance_file_name": self.format_file_name,
            "unit_name" : self.unit_name, "address" : self.address, "compliance_description" : self.compliance_description,
            "remarks" : self.remarks, "compliance_id": self.compliance_id,
            "file_names": self.file_names, "compliance_download_url": self.download_url
        }

class UpcomingCompliance(object):
    def __init__(
        self, compliance_name, domain_name, start_date, due_date,
        format_file_name, unit_name, address, assigned_on, compliance_description
    ):
        self.compliance_name = compliance_name
        self.domain_name = domain_name
        self.start_date = start_date
        self.assigned_on = assigned_on
        self.due_date = due_date
        self.format_file_name = format_file_name
        self.unit_name = unit_name
        self.address = address
        self.assigned_on = assigned_on
        self.compliance_description = compliance_description

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "compliance_name", "domain_name", "start_date", "assigned_on"
            "due_date", "upcoming_format_file_name", "unit_name", "address",
            "assigned_on", "compliance_description"
        ])
        return UpcomingCompliance(
            data.get("compliance_name"), data.get("domain_name"),
            data.get("start_date"), data.get("assigned_on"), data.get("due_date"),
            data.get("upcoming_format_file_name"), data.get("unit_name"),
            data.get("address"), data.get("assigned_on"), data.get("compliance_description")
        )

    def to_structure(self):
        return {
            "compliance_name": self.compliance_name, "domain_name": self.domain_name,
            "start_date": self.start_date, "assigned_on": self.assigned_on, "due_date": self.due_date,
            "upcoming_format_file_name": self.format_file_name, "unit_name": self.unit_name,
            "address" : self.address, "assigned_on": self.assigned_on,
            "compliance_description" : self.compliance_description
        }

class NumberOfCompliances(object):
    def __init__(
        self, domain_id, country_id, year, complied_count,
        delayed_compliance_count,
        inprogress_compliance_count, not_complied_count
    ):
        self.domain_id = domain_id
        self.country_id = country_id
        self.year = year
        self.complied_count = complied_count
        self.delayed_compliance_count = delayed_compliance_count
        self.inprogress_compliance_count = inprogress_compliance_count
        self.not_complied_count = not_complied_count

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "d_id", "c_id", "year", "complied_count",
            "delayed_compliance_count",
            "inprogress_compliance_count", "not_complied_count"
        ])
        return NumberOfCompliances(
            data.get("d_id"), data.get("c_id"), data.get("year"),
            data.get("complied_count"), data.get("delayed_compliance_count"),
            data.get("inprogress_compliance_count"), data.get("not_complied_count")
        )

    def to_structure(self):
        return {
            "d_id": self.domain_id, "c_id": self.country_id, "year": self.year,
            "complied_count": self.complied_count, "delayed_compliance_count": self.delayed_compliance_count,
            "inprogress_compliance_count": self.inprogress_compliance_count, "not_complied_count": self.not_complied_count,
        }

class User(object):
    def __init__(self, user_id, user_category_id, employee_name, is_active):
        self.user_id = user_id
        self.user_category_id = user_category_id
        self.employee_name = employee_name
        self.is_active = is_active

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["user_id", "user_category_id", "employee_name", "is_active"])
        return User(
            data.get("user_id"), data.get("user_category_id"), data.get("employee_name"), data.get("is_active")
        )

    def to_structure(self):
        return {
            "user_id": self.user_id, "user_category_id": self.user_category_id,
            "employee_name": self.employee_name, "is_active": self.is_active
        }

class StatutoryDate(object):
    def __init__(self, statutory_date, statutory_month, trigger_before_days, repeat_by):
        self.statutory_date = statutory_date
        self.statutory_month = statutory_month
        self.trigger_before_days = trigger_before_days
        self.repeat_by = repeat_by

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["statutory_date", "statutory_month", "trigger_before_days", "repeat_by"])
        return StatutoryDate(
            data.get("statutory_date"), data.get("statutory_month"),
            data.get("trigger_before_days"), data.get("repeat_by")
        )

    def to_structure(self):
        return {
            "statutory_date": self.statutory_date, "statutory_month": self.statutory_month,
            "trigger_before_days": self.trigger_before_days, "repeat_by": self.repeat_by
        }

class FormCategory(object):
    def __init__(self, form_category_id, form_category):
        self.form_category_id = form_category_id
        self.form_category = form_category

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["form_category_id", "form_category"])
        return FormCategory(data.get("form_category_id"), data.get("form_category"))

    def to_structure(self):
        return {
            "form_category_id": self.form_category_id, "form_category": self.form_category,
        }

class UserCategory(object):
    def __init__(self, user_category_id, user_category_name):
        self.user_category_id = user_category_id
        self.user_category_name = user_category_name

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["user_category_id", "user_category_name"])
        return UserCategory(data.get("user_category_id"), data.get("user_category_name"))

    def to_structure(self):
        return {
            "user_category_id": self.user_category_id, "user_category_name": self.user_category_name,
        }
# ComplianceFrequency
class ComplianceFrequency(object):
    def __init__(self, frequency_id, frequency):
        self.frequency_id = frequency_id
        self.frequency = frequency

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["frequency_id", "frequency"])
        return ComplianceFrequency(data.get("frequency_id"), data.get("frequency"))

    def to_structure(self):
        return {"frequency_id": self.frequency_id, "frequency": self.frequency}


class ComplianceFilter(object):
    def __init__(self, domain_id, compliance_id, compliance_task):
        self.domain_id = domain_id
        self.compliance_id = compliance_id
        self.compliance_task = compliance_task

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["d_id", "c_task", "compliance_id"])
        return ComplianceFilter(data.get("d_id"), data.get("compliance_id"), data.get("c_task"))

    def to_structure(self):
        return {
            "d_id": self.domain_id, "compliance_id": self.compliance_id, "c_task": self.compliance_task,
        }


class ClientUserGroup(object):
    def __init__(self, user_group_id, user_group_name, user_category_id, user_category_name, category_form_ids, is_active):
        self.user_group_id = user_group_id
        self.user_group_name = user_group_name
        self.user_category_id = user_category_id
        self.user_category_name = user_category_name
        self.category_form_ids = category_form_ids
        self.is_active = is_active

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["user_group_id", "user_group_name", "user_category_id", "user_category_name", "category_form_ids", "is_active"])
        return ClientUserGroup(
            data.get("user_group_id"), data.get("user_group_name"), data.get("user_category_id"),
            data.get("user_category_name"), data.get("category_form_ids"), data.get("is_active")
        )

    def to_structure(self):
        return {
            "u_g_id": self.user_group_id, "u_g_name": self.user_group_name, "u_c_id": self.user_category_id,
            "u_c_name": self.user_category_name, "f_ids": self.category_form_ids, "is_active": self.is_active,
        }

class ClientUsercategory(object):
    def __init__(self, user_category_id, user_category_name):
        self.user_category_id = user_category_id
        self.user_category_name = user_category_name

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["user_category_id", "user_category_name"])
        return ClientUserGroup(data.get("user_category_id"), data.get("user_category_name"))

    def to_structure(self):
        return {
            "u_c_id": self.user_category_id, "u_c_name": self.user_category_name,
        }

class UnitClosureLegalEntity(object):
    def __init__(self, legal_entity_id, legal_entity_name):
        self.legal_entity_id = legal_entity_id
        self.legal_entity_name = legal_entity_name

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["legal_entity_id", "legal_entity_name"])
        return UnitClosureLegalEntity(data.get("legal_entity_id"), data.get("legal_entity_name"))

    def to_structure(self):
        return {
            "legal_entity_id": self.legal_entity_id, "legal_entity_name": self.legal_entity_name,
        }

class UnitClosure_Units(object):
    def __init__(
        self, unit_id, unit_code, unit_name, address, postal_code,
        legal_entity_id, legal_entity_name, business_group_name, division_name,
        category_name, is_active, closed_on, validity_days
    ):
        self.unit_id = unit_id
        self.unit_code = unit_code
        self.unit_name = unit_name
        self.address = address
        self.postal_code = postal_code
        self.legal_entity_id = legal_entity_id
        self.legal_entity_name = legal_entity_name
        self.business_group_name = business_group_name
        self.division_name = division_name
        self.category_name = category_name
        self.is_active = is_active
        self.closed_on = closed_on
        self.validity_days = validity_days

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "unit_id", "unit_code", "unit_name", "address", "postal_code",
            "legal_entity_id", "legal_entity_name", "business_group_name",
            "division_name", "category_name", "is_active", "closed_on",
            "validity_days"
        ])
        return UnitClosure_Units(
            data.get("unit_id"), data.get("unit_code"), data.get("unit_name"),
            data.get("address"), data.get("postal_code"), data.get("legal_entity_id"),
            data.get("legal_entity_name"), data.get("business_group_name"), data.get("division_name"),
            data.get("category_name"), data.get("is_active"), data.get("closed_on"), data.get("validity_days")
        )

    def to_structure(self):
        return {
            "unit_id": self.unit_id, "unit_code": self.unit_code, "unit_name": self.unit_name,
            "address": self.address, "postal_code": self.postal_code, "legal_entity_id": self.legal_entity_id,
            "legal_entity_name": self.legal_entity_name, "business_group_name": self.business_group_name,
            "division_name": self.division_name, "category_name": self.category_name, "is_active": self.is_active,
            "closed_on": self.closed_on, "validity_days": self.validity_days,
        }


class LegalEntityInfo(object):
    def __init__(self, legal_entity_id, legal_entity_name, country_id, business_group_id, business_group_name, country_name):
        self.legal_entity_id = legal_entity_id
        self.legal_entity_name = legal_entity_name
        self.country_id = country_id
        self.business_group_id = business_group_id
        self.business_group_name = business_group_name
        self.country_name = country_name

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["le_id", "le_name", "country_id", "bg_id", "bg_name", "country_name"])
        return LegalEntityInfo(
            data.get("le_id"), data.get("le_name"), data.get("country_id"),
            data.get("bg_id"), data.get("bg_name"), data.get("country_name")
        )

    def to_structure(self):
        return {
            "le_id": self.legal_entity_id, "le_name": self.legal_entity_name, "c_id": self.country_id,
            "bg_id": self.business_group_id, "bg_name": self.business_group_name, "c_name" : self.country_name
        }

class ReviewSettingsUnits(object):
    def __init__(
        self, unit_id, unit_code, unit_name, address, geography_name, division_name
    ):
        self.unit_id = unit_id
        self.unit_code = unit_code
        self.unit_name = unit_name
        self.address = address
        self.geography_name = geography_name
        self.division_name = division_name

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "u_id", "u_code", "u_name", "address", "g_name", "div_name"
            ])
        return ReviewSettingsUnits(
            data.get("u_id"), data.get("u_code"), data.get("u_name"), data.get("address"),
            data.get("g_name"), data.get("div_name")
        )

    def to_structure(self):
        return {
            "u_id": self.unit_id, "u_code": self.unit_code, "u_name": self.unit_name,
            "address": self.address, "g_name": self.geography_name, "div_name": self.division_name
        }

class ReviewSettingsCompliance(object):
    def __init__(
        self, compliance_id, compliance_task, compliance_description, statutory_provision,
        repeats_every, repeats_type_id, statutory_dates, due_date,
        unit_ids, level_1_statutory_name
    ):
        self.compliance_id = compliance_id
        self.compliance_task = compliance_task
        self.compliance_description = compliance_description
        self.statutory_provision = statutory_provision
        self.repeats_every = repeats_every
        self.repeats_type_id = repeats_type_id
        self.statutory_dates = statutory_dates
        self.due_date = due_date
        self.unit_ids = unit_ids
        self.level_1_statutory_name = level_1_statutory_name

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(
            data, [
                "comp_id", "comp_name", "descp", "s_prov", "r_every", "repeats_type_id",
                "s_dates", "due_date_list", "u_ids", "level_1_s_name"
            ]
        )
        return ReviewSettingsCompliance(
            data.get("comp_id"), data.get("comp_name"), data.get("descp"), data.get("s_prov"), data.get("r_every"),
            data.get("repeats_type_id"), data.get("s_dates"), data.get("due_date_list"),
            data.get("u_ids"), data.get("level_1_s_name")
        )

    def to_structure(self):
        return {
            "comp_id": self.compliance_id, "comp_name": self.compliance_task, "descp": self.compliance_description,
            "s_prov": self.statutory_provision, "r_every": self.repeats_every, "repeats_type_id": self.repeats_type_id,
            "s_dates": self.statutory_dates, "due_date_list": self.due_date, "u_ids": self.unit_ids,
            "level_1_s_name": self.level_1_statutory_name
        }

class LegalEntityUser(object):
    def __init__(self, user_id, employee_code, employee_name, is_active, legal_entity_id, user_category_id):
        self.user_id = user_id
        self.employee_code = employee_code
        self.employee_name = employee_name
        self.is_active = is_active
        self.legal_entity_id = legal_entity_id
        self.user_category_id = user_category_id

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["user_id", "employee_code", "employee_name", "is_active", "le_id", "user_category_id"])
        return User(
            data.get("user_id"), data.get("employee_code"), data.get("employee_name"),
            data.get("is_active"), data.get("le_id"), data.get("user_category_id")
        )

    def to_structure(self):
        return {
            "user_id": self.user_id, "employee_code": self.employee_code,
            "employee_name": self.employee_name, "is_active": self.is_active, "le_id": self.legal_entity_id,
            "user_category_id": self.user_category_id
        }
# User Management Form
class UserDomains(object):
    def __init__(self, legal_entity_id, domain_id):
        self.legal_entity_id = legal_entity_id
        self.domain_id = domain_id

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["le_id", "d_id"])
        return UserDomains(data.get("le_id"), data.get("d_id"))

    def to_structure(self):
        return {"le_id": self.legal_entity_id, "d_id": self.domain_id}

# User Management Form
class UserUnits(object):
    def __init__(self, legal_entity_id, unit_id):
        self.legal_entity_id = legal_entity_id
        self.unit_id = unit_id

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["le_id", "u_id"])
        return UserUnits(data.get("le_id"), data.get("u_id"))

    def to_structure(self):
        return {"le_id": self.legal_entity_id, "u_id": self.unit_id}

# User Management Form
class UserEntities(object):
    def __init__(self, legal_entity_id):
        self.legal_entity_id = legal_entity_id

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["le_id"])
        return UserEntities(data.get("le_id"))

    def to_structure(self):
        return {"le_id": self.legal_entity_id}

# User Management Add - Category Prerequisite
class ClientUsercategory_UserManagement(object):
    def __init__(self, user_category_id, user_category_name):
        self.user_category_id = user_category_id
        self.user_category_name = user_category_name

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["user_category_id", "user_category_name"])
        return ClientUsercategory_UserManagement(
            data.get("user_category_id"), data.get("user_category_name")
        )

    def to_structure(self):
        return {
            "u_c_id": self.user_category_id, "u_c_name": self.user_category_name,
        }

# User Management Add - User Group Prerequisite
class ClientUserGroup_UserManagement(object):
    def __init__(self, user_group_id, user_group_name, user_category_id):
        self.user_group_id = user_group_id
        self.user_group_name = user_group_name
        self.user_category_id = user_category_id

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["user_group_id", "user_group_name", "user_category_id"])
        return ClientUserGroup_UserManagement(
            data.get("user_group_id"), data.get("user_group_name"), data.get("user_category_id")
        )

    def to_structure(self):
        return {
            "u_g_id": self.user_group_id, "u_g_name": self.user_group_name, "u_c_id": self.user_category_id
        }
# User Management Add - Business Group
class ClientUserBusinessGroup_UserManagement(object):
    def __init__(self, business_group_id, business_group_name):
        self.business_group_id = business_group_id
        self.business_group_name = business_group_name

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["business_group_id", "business_group_name"])
        return ClientUserBusinessGroup_UserManagement(
            data.get("business_group_id"), data.get("business_group_name")
        )

    def to_structure(self):
        return {
            "bg_id": self.business_group_id, "bg_name": self.business_group_name
        }
# User Management Add - Legal Entity
class ClientUserLegalEntity_UserManagement(object):
    def __init__(self, legal_entity_id, business_group_id, legal_entity_name, le_admin):
        self.legal_entity_id = legal_entity_id
        self.business_group_id = business_group_id
        self.legal_entity_name = legal_entity_name
        self.le_admin = le_admin

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["legal_entity_id", "business_group_id", "legal_entity_name", "le_admin"])
        return ClientUserLegalEntity_UserManagement(
            data.get("legal_entity_id"), data.get("business_group_id"),
            data.get("legal_entity_name"), data.get("le_admin")
        )

    def to_structure(self):
        return {
            "le_id": self.legal_entity_id, "bg_id": self.business_group_id,
            "le_name": self.legal_entity_name, "le_admin": self.le_admin
        }
# User Management Add - Division
class ClientUserDivision_UserManagement(object):
    def __init__(self, division_id, division_name, legal_entity_id, business_group_id):
        self.division_id = division_id
        self.division_name = division_name
        self.legal_entity_id = legal_entity_id
        self.business_group_id = business_group_id

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "division_id", "division_name", "legal_entity_id", "business_group_id"
        ])
        return ClientUserDivision_UserManagement(
            data.get("division_id"), data.get("division_name"), data.get("legal_entity_id"),
            data.get("business_group_id")
        )

    def to_structure(self):
        return {
            "d_id": self.division_id, "d_name": self.division_name, "le_id": self.legal_entity_id, "bg_id": self.business_group_id
        }
# User Management Add - Category
class ClientGroupCategory_UserManagement(object):
    def __init__(self, category_id, category_name, legal_entity_id, business_group_id, division_id):
        self.category_id = category_id
        self.category_name = category_name
        self.legal_entity_id = legal_entity_id
        self.business_group_id = business_group_id
        self.division_id = division_id

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "category_id", "category_name", "legal_entity_id",
            "business_group_id", "division_id"
        ])
        return ClientGroupCategory_UserManagement(
            data.get("category_id"), data.get("category_name"), data.get("legal_entity_id"),
            data.get("business_group_id"), data.get("division_id")
        )

    def to_structure(self):
        return {
            "cat_id": self.category_id, "cat_name": self.category_name, "le_id": self.legal_entity_id,
            "bg_id": self.business_group_id, "d_id": self.division_id
        }
# User Management Add - Domains
class ClientLegalDomains_UserManagement(object):
    def __init__(self, legal_entity_id, domain_id, domain_name):
        self.legal_entity_id = legal_entity_id
        self.domain_id = domain_id
        self.domain_name = domain_name

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "category_id", "category_name", "legal_entity_id",
            "business_group_id", "division_id"
        ])
        return ClientLegalDomains_UserManagement(
            data.get("legal_entity_id"), data.get("domain_id"), data.get("domain_name")
        )

    def to_structure(self):
        return {
            "le_id": self.legal_entity_id, "u_dm_id": self.domain_id, "u_dm_name": self.domain_name
        }
# User Management Add - Units
class ClientLegalUnits_UserManagement(object):
    def __init__(
        self, unit_id, business_group_id, legal_entity_id, division_id,
        category_id, unit_code, unit_name, address, postal_code, domains
    ):
        self.unit_id = unit_id
        self.business_group_id = business_group_id
        self.legal_entity_id = legal_entity_id
        self.division_id = division_id
        self.category_id = category_id
        self.unit_code = unit_code
        self.unit_name = unit_name
        self.address = address
        self.postal_code = postal_code
        self.domains = domains

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "unit_id", "business_group_id", "legal_entity_id",
            "division_id", "category_id", "unit_code", "unit_name", "address", "postal_code", "d_ids"
        ])
        return ClientLegalUnits_UserManagement(
            data.get("unit_id"), data.get("business_group_id"), data.get("legal_entity_id"),
            data.get("division_id"), data.get("category_id"), data.get("unit_code"),
            data.get("unit_name"), data.get("address"), data.get("postal_code"), data.get("d_ids")
        )

    def to_structure(self):
        return {
            "u_unt_id": self.unit_id, "bg_id": self.business_group_id, "le_id": self.legal_entity_id,
            "d_id": self.division_id, "cat_id": self.category_id, "u_unt_code": self.unit_code,
            "u_unt_name": self.unit_name, "u_unt_address": self.address, "u_unt_postal": self.postal_code, "d_ids": self.domains
        }
# User Management Add - Legal Entities
class ClientLegalEntity_UserManagement(object):
    def __init__(self, legal_entity_id):
        self.legal_entity_id = legal_entity_id

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["legal_entity_id"])
        return ClientLegalEntity_UserManagement(data.get("legal_entity_id"))

    def to_structure(self):
        return {"le_id": self.legal_entity_id}

# User Management Add - Service Providers
class ClientServiceProviders_UserManagement(object):
    def __init__(self, service_provider_id, service_provider_name, short_name):
        self.service_provider_id = service_provider_id
        self.service_provider_name = service_provider_name
        self.short_name = short_name

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["service_provider_id", "service_provider_name", "short_name"])
        return ClientServiceProviders_UserManagement(
            data.get("service_provider_id"), data.get("service_provider_name"), data.get("short_name")
        )

    def to_structure(self):
        return {
            "u_sp_id": self.service_provider_id, "u_sp_name": self.service_provider_name, "u_sp_short": self.short_name
        }
# User Management List - Get Legal Entity details
class ClientLegalEntities_UserManagementList(object):
    def __init__(
        self, country_name, business_group_name, legal_entity_id, legal_entity_name,
        contract_from, contract_to, total_licence, used_licence
    ):
        self.country_name = country_name
        self.business_group_name = business_group_name
        self.legal_entity_id = legal_entity_id
        self.legal_entity_name = legal_entity_name
        self.contract_from = contract_from
        self.contract_to = contract_to
        self.total_licence = total_licence
        self.used_licence = used_licence

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "country_name", "business_group_name", "legal_entity_id", "legal_entity_name",
            "contract_from", "contract_to", "total_licence", "used_licence"
        ])
        return ClientLegalEntities_UserManagementList(
            data.get("country_name"), data.get("business_group_name"), data.get("legal_entity_id"),
            data.get("legal_entity_name"), data.get("contract_from"), data.get("contract_to"),
            data.get("total_licence"), data.get("used_licence")
        )

    def to_structure(self):
        return {
            "c_name": self.country_name, "b_g_name": self.business_group_name, "le_id": self.legal_entity_id,
            "le_name": self.legal_entity_name, "cont_from": self.contract_from, "cont_to": self.contract_to,
            "total_licences": self.total_licence, "used_licences": self.used_licence
        }
# User Management List - Get Users
class ClientUsers_UserManagementList(object):
    def __init__(
        self, user_id, user_category_id, employee_code, employee_name,
        username, email_id, mobile_no, legal_entity_id, is_active,
        is_disable, unblock_days, seating_unit, legal_entity_ids
    ):
        self.user_id = user_id
        self.user_category_id = user_category_id
        self.employee_code = employee_code
        self.employee_name = employee_name
        self.username = username
        self.email_id = email_id
        self.mobile_no = mobile_no
        self.legal_entity_id = legal_entity_id
        self.is_active = is_active
        self.is_disable = is_disable
        self.unblock_days = unblock_days
        self.seating_unit = seating_unit
        self.legal_entity_ids = legal_entity_ids

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "user_id", "user_category_id", "employee_code"
            "employee_name", "username", "email_id", "mobile_no", "legal_entity_id",
            "is_active", "is_disable", "unblock_days", "seating_unit", "le_ids"
        ])
        return ClientUsers_UserManagementList(
            data.get("user_id"), data.get("user_category_id"), data.get("employee_code"),
            data.get("employee_name"), data.get("username"), data.get("email_id"),
            data.get("mobile_no"), data.get("legal_entity_id"), data.get("is_active"),
            data.get("is_disable"), data.get("unblock_days"), data.get("seating_unit"), data.get("le_ids")
        )

    def to_structure(self):
        return {
            "user_id": self.user_id, "u_cat_id": self.user_category_id, "emp_code": self.employee_code,
            "emp_name": self.employee_name, "user_name": self.username, "email_id": self.email_id,
            "mob_no": self.mobile_no, "le_id": self.legal_entity_id, "is_active": self.is_active,
            "is_disable": self.is_disable, "unblock_days": self.unblock_days, "seating_unit": self.seating_unit, "le_ids": self.legal_entity_ids
        }
# User Management Edit - Get Users for Edit View
class ClientUsers_UserManagement_EditView_Users(object):
    def __init__(
        self, user_id, user_category_id, seating_unit_id, service_provider_id, user_level,
        user_group_id, email_id, employee_code, employee_name,
        contact_no, mobile_no, address, is_service_provider,
        is_active, is_disable
    ):
        self.user_id = user_id
        self.user_category_id = user_category_id
        self.seating_unit_id = seating_unit_id
        self.service_provider_id = service_provider_id
        self.user_level = user_level
        self.user_group_id = user_group_id
        self.email_id = email_id
        self.employee_code = employee_code
        self.employee_name = employee_name
        self.contact_no = contact_no
        self.mobile_no = mobile_no
        self.address = address
        self.is_service_provider = is_service_provider
        self.is_active = is_active
        self.is_disable = is_disable

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "user_id", "user_category_id", "seating_unit_id", "is_service_provider", "user_level",
            "user_group_id", "email_id", "employee_code",
            "employee_name", "contact_no", "mobile_no", "address",
            "is_service_provider", "is_active", "is_disable"])

        return ClientUsers_UserManagement_EditView_Users(
            data.get("user_id"), data.get("user_category_id"), data.get("seating_unit_id"),
            data.get("is_service_provider"), data.get("user_level"), data.get("user_group_id"),
            data.get("email_id"), data.get("employee_code"), data.get("employee_name"),
            data.get("contact_no"), data.get("mobile_no"), data.get("address"),
            data.get("is_service_provider"), data.get("is_active"), data.get("is_disable")
        )

    def to_structure(self):
        return {
            "user_id": self.user_id, "u_cat_id": self.user_category_id,
            "seating_unit_id": self.seating_unit_id, "sp_id": self.service_provider_id,
            "user_level": self.user_level, "u_g_id": self.user_group_id,
            "email_id": self.email_id, "emp_code": self.employee_code, "emp_name": self.employee_name,
            "cont_no": self.contact_no, "mob_no": self.mobile_no, "address": self.address,
            "is_sp": self.is_service_provider, "is_active": self.is_active, "is_disable": self.is_disable
        }

# User Management Edit - Get Legal Entities for Edit View
class ClientUsers_UserManagement_EditView_LegalEntities(object):
    def __init__(self, user_id, legal_entity_id, business_group_id):
        self.user_id = user_id
        self.legal_entity_id = legal_entity_id
        self.business_group_id = business_group_id

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["user_id", "le_id", "bg_id"])
        return ClientUsers_UserManagement_EditView_LegalEntities(
            data.get("user_id"), data.get("le_id"), data.get("bg_id")
        )

    def to_structure(self):
        return {
            "user_id": self.user_id, "le_id": self.legal_entity_id, "bg_id": self.business_group_id
        }
# User Management Edit - Get Domains for Edit View
class ClientUsers_UserManagement_EditView_Domains(object):
    def __init__(self, user_id, legal_entity_id, domain_id):
        self.user_id = user_id
        self.legal_entity_id = legal_entity_id
        self.domain_id = domain_id

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["user_id", "le_id", "u_dm_id"])
        return ClientUsers_UserManagement_EditView_Domains(
            data.get("user_id"), data.get("le_id"), data.get("u_dm_id")
        )

    def to_structure(self):
        return {
            "user_id": self.user_id, "le_id": self.legal_entity_id, "u_dm_id": self.domain_id
        }
# User Management Edit - Get Units for Edit View
class ClientUsers_UserManagement_EditView_Units(object):
    def __init__(self, user_id, legal_entity_id, unit_id, business_group_id, division_id, category_id):
        self.user_id = user_id
        self.legal_entity_id = legal_entity_id
        self.unit_id = unit_id
        self.business_group_id = business_group_id
        self.division_id = division_id
        self.category_id = category_id

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["user_id", "le_id", "u_unt_id", "bg_id", "div_id", "cat_id"])
        return ClientUsers_UserManagement_EditView_Units(
            data.get("user_id"), data.get("le_id"), data.get("u_unt_id"),
            data.get("bg_id"), data.get("div_id"), data.get("cat_id")
        )

    def to_structure(self):
        return {
            "user_id": self.user_id, "le_id": self.legal_entity_id, "u_unt_id": self.unit_id,
            "bg_id": self.business_group_id, "div_id": self.division_id, "cat_id": self.category_id
        }

class ReassignedHistoryReportSuccess(object):
    def __init__(
        self, country_id, legal_entity_id, domain_id, unit_id, act_name, compliance_id, compliance_task,
            old_user, new_user, assigned_on, remarks, due_date, unit
    ):
        self.country_id = country_id
        self.legal_entity_id = legal_entity_id
        self.domain_id = domain_id
        self.unit_id = unit_id
        self.act_name = act_name
        self.compliance_id = compliance_id
        self.compliance_task = compliance_task
        self.old_user = old_user
        self.new_user = new_user
        self.assigned_on = assigned_on
        self.remarks = remarks
        self.due_date = due_date
        self.unit = unit

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "country_id", "legal_entity_id", "domain_id", "unit_id", "act_name",
            "compliance_id", "compliance_task", "old_user", "new_user",
            "assigned_on", "remarks", "due_date", "unit"
        ])
        return ReassignedHistoryReportSuccess(
            data("country_id"), data("legal_entity_id"), data("domain_id"),
            data("unit_id"), data("act_name"), data("compliance_id"), data("compliance_task"),
            data("old_user"), data("new_user"), data("assigned_on"), data("remarks"),
            data("due_date"), data("unit")
        )

    def to_structure(self):
        return {
            "country_id": self.country_id, "legal_entity_id": self.legal_entity_id,
            "domain_id": self.domain_id, "unit_id": self.unit_id, "act_name": self.act_name,
            "compliance_id": self.compliance_id, "compliance_task": self.compliance_task,
            "old_user": self.old_user, "new_user": self.new_user, "assigned_on": self.assigned_on,
            "remarks": self.remarks, "due_date": self.due_date, "unit": self.unit
        }

class GetStatusReportConsolidatedSuccess(object):
    def __init__(
        self, compliance_activity_id, compliance_history_id, legal_entity_id, unit_id, unit, compliance_id, compliance_name, frequency_name,
        act_name, activity_on, due_date, completion_date, task_status, uploaded_document, activity_status, user_name, start_date
    ):

        self.compliance_activity_id = compliance_activity_id
        self.compliance_history_id = compliance_history_id
        self.legal_entity_id = legal_entity_id
        self.unit_id = unit_id
        self.unit = unit
        self.compliance_id = compliance_id
        self.compliance_name = compliance_name
        self.frequency_name = frequency_name
        self.act_name = act_name
        self.activity_on = activity_on
        self.due_date = due_date
        self.completion_date = completion_date
        self.task_status = task_status
        self.uploaded_document = uploaded_document
        self.activity_status = activity_status
        self.user_name = user_name
        self.start_date = start_date

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "compliance_activity_id", "compliance_history_id", "legal_entity_id", "unit_id", "unit", "compliance_id", "compliance_name",
            "frequency_name", "act_name", "activity_on", "due_date", "completion_date", "task_status", "uploaded_document", "activity_status", "user_name", "start_date"])
        return GetStatusReportConsolidatedSuccess(
            data("compliance_activity_id"), data("compliance_history_id"), data("legal_entity_id"),
            data("unit_id"), data("unit"), data("compliance_id"), data("compliance_name"),
            data("frequency_name"), data("act_name"), data("activity_on"), data("due_date"),
            data("completion_date"), data("task_status"), data("uploaded_document"),
            data("activity_status"), data("user_name"), data("start_date")
        )

    def to_structure(self):
        return {
            "compliance_activity_id": self.compliance_activity_id, "compliance_history_id": self.compliance_history_id,
            "legal_entity_id": self.legal_entity_id, "unit_id": self.unit_id, "unit": self.unit,
            "compliance_id": self.compliance_id, "compliance_name": self.compliance_name,
            "frequency_name": self.frequency_name, "act_name": self.act_name,
            "activity_on": self.activity_on, "due_date": self.due_date,
            "completion_date": self.completion_date, "task_status": self.task_status,
            "uploaded_document": self.uploaded_document, "activity_status": self.activity_status,
            "user_name": self.user_name, "start_date": self.start_date
        }

class GetStatutorySettingsUnitWiseSuccess(object):
    def __init__(self, compliance_id, frequency, compliance_task, act_name, task_status, document_name, user_name, due_date, unit, unit_id):
        self.compliance_id = compliance_id
        self.frequency = frequency
        self.compliance_task = compliance_task
        self.act_name = act_name
        self.task_status = task_status
        self.document_name = document_name
        self.user_name = user_name
        self.due_date = due_date
        self.unit = unit
        self.unit_id = unit_id

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "compliance_id", "frequency", "compliance_task", "act_name", "task_status",
            "document_name", "user_name", "due_date", "unit", "unit_id"
        ])
        return GetStatutorySettingsUnitWiseSuccess(
            data.get("compliance_id"), data.get("frequency"), data.get("compliance_task"),
            data.get("act_name"), data.get("task_status"), data.get("document_name"),
            data.get("user_name"), data.get("due_date"), data.get("unit"), data.get("unit_id")
        )

    def to_structure(self):
        return {
            "compliance_id": self.compliance_id, "frequency": self.frequency,
            "compliance_task": self.compliance_task, "act_name": self.act_name,
            "task_status": self.task_status, "document_name": self.document_name,
            "user_name": self.user_name, "due_date": self.due_date,
            "unit": self.unit, "unit_id": self.unit_id
        }

class GetDomainScoreCardSuccess(object):
    def __init__(self, domain_id, domain_name, not_opted_count, unassigned_count, assigned_count, units_count):
        self.domain_id = domain_id
        self.domain_name = domain_name
        self.not_opted_count = not_opted_count
        self.unassigned_count = unassigned_count
        self.assigned_count = assigned_count
        self.units_count = units_count

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["domain_id", "domain_name", "not_opted_count", "unassigned_count", "assigned_count", "units_wise_count"])
        return GetDomainScoreCardSuccess(
            data.get("domain_id"), data.get("domain_name"), data.get("not_opted_count"),
            data.get("unassigned_count"), data.get("assigned_count"), data.get("units_wise_count")
        )

    def to_structure(self):
        return {
            "domain_id" : self.domain_id, "domain_name" : self.domain_name,
            "not_opted_count" : self.not_opted_count, "unassigned_count" : self.unassigned_count,
            "assigned_count" : self.assigned_count, "units_wise_count" : self.units_count
        }

class GetDomainWiseUnitScoreCardSuccess(object):
    def __init__(self, unit_id, domain_name, units, not_opted_count, unassigned_count, complied_count, delayed_count, inprogress_count, overdue_count):
        self.unit_id = unit_id
        self.domain_name = domain_name
        self.units = units
        self.not_opted_count = not_opted_count
        self.unassigned_count = unassigned_count
        self.complied_count = complied_count
        self.delayed_count = delayed_count
        self.inprogress_count = inprogress_count
        self.overdue_count = overdue_count

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["unit_id", "domain_name", "unit", "not_opted_count", "unassigned_count", "complied_count", "delayed_count", "inprogress_count", "overdue_count"])
        return GetDomainWiseUnitScoreCardSuccess(
            data.get("unit_id"), data.get("domain_name"), data.get("unit"),
            data.get("not_opted_count"), data.get("unassigned_count"), data.get("complied_count"),
            data.get("delayed_count"), data.get("inprogress_count"), data.get("overdue_count")
        )

    def to_structure(self):
        return {
            "unit_id": self.unit_id, "domain_name": self.domain_name, "unit": self.units, "not_opted_count": self.not_opted_count,
            "unassigned_count": self.unassigned_count, "complied_count": self.complied_count,
            "delayed_count": self.delayed_count, "inprogress_count": self.inprogress_count,
            "overdue_count": self.overdue_count
        }

class GetLEWiseScoreCardSuccess(object):
    def __init__(
        self, inprogress_count, completed_count, overdue_count, inprogress_unit_wise, inprogress_user_wise,
        completed_unit_wise, completed_user_wise, overdue_unit_wise, overdue_user_wise
    ):
        self.inprogress_count = inprogress_count
        self.completed_count = completed_count
        self.overdue_count = overdue_count
        self.inprogress_unit_wise = inprogress_unit_wise
        self.inprogress_user_wise = inprogress_user_wise
        self.completed_unit_wise = completed_unit_wise
        self.completed_user_wise = completed_user_wise
        self.overdue_unit_wise = overdue_unit_wise
        self.overdue_user_wise = overdue_user_wise

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "inprogress_count", "completed_count", "overdue_count", "inprogress_unit_wise",
            "inprogress_unit_wise", "completed_unit_wise", "completed_user_wise", "overdue_unit_wise", "overdue_user_wise"])
        return GetLEWiseScoreCardSuccess(
            data.get("inprogress_count"), data.get("completed_count"), data.get("overdue_count"),
            data.get("inprogress_unit_wise"), data.get("inprogress_user_wise"), data.get("completed_unit_wise"),
            data.get("completed_user_wise"), data.get("overdue_unit_wise"), data.get("overdue_user_wise")
        )

    def to_structure(self):
        return {
            "inprogress_count": self.inprogress_count, "completed_count": self.completed_count,
            "overdue_count": self.overdue_count, "inprogress_unit_wise": self.inprogress_unit_wise,
            "inprogress_user_wise": self.inprogress_user_wise, "completed_unit_wise": self.completed_unit_wise,
            "completed_user_wise": self.completed_user_wise, "overdue_unit_wise": self.overdue_unit_wise,
            "overdue_user_wise": self.overdue_user_wise
        }

class GetInprogressUnitWiseCountSuccess(object):
    def __init__(self, unit_id, unit, to_complete, to_concur, to_approve):
        self.unit_id = unit_id
        self.unit = unit
        self.to_complete = to_complete
        self.to_concur = to_concur
        self.to_approve = to_approve

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["unit_id", "unit", "to_complete", "to_concur", "to_approve"])
        return GetInprogressUnitWiseCountSuccess(
                data.get("unit_id"), data.get("unit"), data.get("to_complete"),
                data.get("to_concur"), data.get("to_approve")
        )

    def to_structure(self):
        return {
            "unit_id": self.unit_id, "unit": self.unit, "to_complete": self.to_complete,
            "to_concur": self.to_concur, "to_approve": self.to_approve
        }

class GetInprogressUserWiseCountSuccess(object):
    def __init__(self, user_id, user_name, to_complete, to_concur, to_approve):
        self.user_id = user_id
        self.user_name = user_name
        self.to_complete = to_complete
        self.to_concur = to_concur
        self.to_approve = to_approve

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["user_id", "user_name", "to_complete", "to_concur", "to_approve"])
        return GetInprogressUserWiseCountSuccess(
            data.get("user_id"), data.get("user_name"), data.get("to_complete"),
            data.get("to_concur"), data.get("to_approve")
        )

    def to_structure(self):
        return {
            "user_id": self.user_id, "user_name": self.user_name, "to_complete": self.to_complete,
            "to_concur": self.to_concur, "to_approve": self.to_approve
        }

class GetCompletedUnitWiseCountSuccess(object):
    def __init__(self, unit_id, unit, complied_count, delayed_count):
        self.unit_id = unit_id
        self.unit = unit
        self.complied_count = complied_count
        self.delayed_count = delayed_count

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["unit_id", "unit", "complied_count", "delayed_count"])
        return GetCompletedUnitWiseCountSuccess(
            data.get("unit_id"), data.get("unit"), data.get("complied_count"), data.get("delayed_count")
        )

    def to_structure(self):
        return {
            "unit_id": self.unit_id, "unit": self.unit, "complied_count": self.complied_count, "delayed_count": self.delayed_count
        }

class GetCompletedUserWiseCountSuccess(object):
    def __init__(self, user_id, user_name, complied_count, delayed_count):
        self.user_id = user_id
        self.user_name = user_name
        self.complied_count = complied_count
        self.delayed_count = delayed_count

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["user_id", "user_name", "complied_count", "delayed_count"])
        return GetCompletedUserWiseCountSuccess(
            data.get("user_id"), data.get("user_name"), data.get("complied_count"),
            data.get("delayed_count")
        )

    def to_structure(self):
        return {
            "user_id": self.user_id, "user_name": self.user_name,
            "complied_count": self.complied_count, "delayed_count": self.delayed_count
        }

class GetOverdueUnitWiseCountSuccess(object):
    def __init__(self, unit_id, unit, to_complete, to_concur, to_approve):
        self.unit_id = unit_id
        self.unit = unit
        self.to_complete = to_complete
        self.to_concur = to_concur
        self.to_approve = to_approve

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["unit_id", "unit", "to_complete", "to_concur", "to_approve"])
        return GetOverdueUnitWiseCountSuccess(
            data.get("unit_id"), data.get("unit"), data.get("to_complete"),
            data.get("to_concur"), data.get("to_approve")
        )

    def to_structure(self):
        return {
            "unit_id": self.unit_id, "unit": self.unit, "to_complete": self.to_complete,
            "to_concur": self.to_concur, "to_approve": self.to_approve
        }

class GetOverdueUserWiseCountSuccess(object):
    def __init__(self, user_id, user_name, to_complete, to_concur, to_approve):
        self.user_id = user_id
        self.user_name = user_name
        self.to_complete = to_complete
        self.to_concur = to_concur
        self.to_approve = to_approve

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["user_id", "user_name", "to_complete", "to_concur", "to_approve"])

        return GetOverdueUserWiseCountSuccess(
            data.get("user_id"), data.get("user_name"), data.get("to_complete"),
            data.get("to_concur"), data.get("to_approve")
        )

    def to_structure(self):
        return {
            "user_id": self.user_id, "user_name": self.user_name, "to_complete": self.to_complete,
            "to_concur": self.to_concur, "to_approve": self.to_approve
        }

class GetWorkFlowScoreCardSuccess(object):
    def __init__(
        self, c_assignee, c_concur, c_approver, inp_assignee, inp_concur, inp_approver,
        ov_assignee, ov_concur, ov_approver, completed_task_count, inprogress_within_duedate_task_count, over_due_task_count
    ):
        self.c_assignee = c_assignee
        self.c_concur = c_concur
        self.c_approver = c_approver
        self.inp_assignee = inp_assignee
        self.inp_concur = inp_concur
        self.inp_approver = inp_approver
        self.ov_assignee = ov_assignee
        self.ov_concur = ov_concur
        self.ov_approver = ov_approver
        self.completed_task_count = completed_task_count
        self.inprogress_within_duedate_task_count = inprogress_within_duedate_task_count
        self.over_due_task_count = over_due_task_count

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "c_assignee", "c_concur", "c_approver", "inp_assignee", "inp_concur", "inp_approver",
            "ov_assignee", "ov_concur", "ov_approver", "completed_task_count", "inprogress_within_duedate_task_count", "over_due_task_count"
        ])
        return GetWorkFlowScoreCardSuccess(
            data.get("c_assignee"), data.get("c_concur"), data.get("c_approver"),
            data.get("inp_assignee"), data.get("inp_concur"), data.get("inp_approver"),
            data.get("ov_assignee"), data.get("ov_concur"), data.get("ov_approver"),
            data.get("completed_task_count"), data.get("inprogress_within_duedate_task_count"),
            data.get("over_due_task_count")
        )

    def to_structure(self):
        return {
            "c_assignee": self.c_assignee, "c_concur": self.c_concur,
            "c_approver": self.c_approver, "inp_assignee": self.inp_assignee,
            "inp_concur": self.inp_concur, "inp_approver": self.inp_approver,
            "ov_assignee": self.ov_assignee, "ov_concur": self.ov_concur,
            "ov_approver": self.ov_approver, "completed_task_count": self.completed_task_count,
            "inprogress_within_duedate_task_count": self.inprogress_within_duedate_task_count,
            "over_due_task_count": self.over_due_task_count
        }

class GetCompletedTaskCountSuccess(object):
    def __init__(self, unit_id, unit, c_assignee, c_concur, c_approver):
        self.unit_id = unit_id
        self.unit = unit
        self.c_assignee = c_assignee
        self.c_concur = c_concur
        self.c_approver = c_approver

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["unit_id", "unit", "c_assignee", "c_concur", "c_approver"])
        return GetCompletedTaskCountSuccess(
            data.get("unit_id"), data.get("unit"), data.get("c_assignee"),
            data.get("c_concur"), data.get("c_approver")
        )

    def to_structure(self):
        return {
            "unit_id": self.unit_id, "unit": self.unit, "c_assignee": self.c_assignee,
            "c_concur": self.c_concur, "c_approver": self.c_approver
        }

class GetInprogressWithinDuedateTaskCountSuccess(object):
    def __init__(self, unit_id, unit, inp_assignee, inp_concur, inp_approver):
        self.unit_id = unit_id
        self.unit = unit
        self.inp_assignee = inp_assignee
        self.inp_concur = inp_concur
        self.inp_approver = inp_approver

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["unit_id", "unit", "inp_assignee", "inp_concur", "inp_approver"])
        return GetInprogressWithinDuedateTaskCountSuccess(
            data.get("unit_id"), data.get("unit"), data.get("inp_assignee"),
            data.get("inp_concur"), data.get("inp_approver")
        )

    def to_structure(self):
        return {
            "unit_id": self.unit_id, "unit": self.unit,
            "inp_assignee": self.inp_assignee, "inp_concur": self.inp_concur,
            "inp_approver": self.inp_approver
        }

class GetOverDueTaskCountSuccess(object):
    def __init__(self, user_id, unit, ov_assignee, ov_concur, ov_approver):
        self.user_id = user_id
        self.unit = unit
        self.ov_assignee = ov_assignee
        self.ov_concur = ov_concur
        self.ov_approver = ov_approver

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["user_id", "unit", "ov_assignee", "ov_concur", "ov_approver"])

        return GetOverDueTaskCountSuccess(
            data.get("user_id"), data.get("unit"), data.get("ov_assignee"),
            data.get("ov_concur"), data.get("ov_approver")
        )

    def to_structure(self):
        return {
            "user_id": self.user_id, "unit": self.unit, "ov_assignee": self.ov_assignee,
            "ov_concur": self.ov_concur, "ov_approver": self.ov_approver
        }

# User Management List Success
class GetUserManagement_List_Success(object):
    def __init__(
        self, c_name, b_g_name, le_name, cont_from, cont_to, total_licences,
        used_licences, le_id, completed_task_count
    ):
        self.c_name = c_name
        self.b_g_name = b_g_name
        self.le_name = le_name
        self.cont_from = cont_from
        self.cont_to = cont_to
        self.total_licences = total_licences
        self.used_licences = used_licences
        self.le_id = le_id
        self.completed_task_count = completed_task_count

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "c_name", "b_g_name", "le_name", "cont_from", "cont_to", "total_licences",
            "used_licences", "le_id", "completed_task_count"
        ])
        return GetUserManagement_List_Success(
            data.get("c_name"), data.get("b_g_name"), data.get("le_name"),
            data.get("cont_from"), data.get("cont_to"), data.get("total_licences"),
            data.get("used_licences"), data.get("le_id"), data.get("completed_task_count")
        )

    def to_structure(self):
        return {
            "c_name": self.c_name, "b_g_name": self.b_g_name, "le_name": self.le_name,
            "cont_from": self.cont_from, "cont_to": self.cont_to,
            "total_licences": self.total_licences, "used_licences": self.used_licences,
            "le_id": self.le_id, "users_list": self.users_list,
        }
# OnOccurrence Last Transaction
class GetOnoccurrencce_Last_Transaction(object):
    def __init__(
        self, compliance_history_id, compliance_id, compliance_task, on_statutory, on_unit,
        compliance_description, start_date, assignee_name, completion_date, concurrer_name,
        concurred_on, approver_name, approved_on, on_compliance_status
    ):
        self.compliance_history_id = compliance_history_id
        self.compliance_id = compliance_id
        self.compliance_task = compliance_task
        self.on_statutory = on_statutory
        self.on_unit = on_unit
        self.compliance_description = compliance_description
        self.start_date = start_date
        self.assignee_name = assignee_name
        self.completion_date = completion_date
        self.concurrer_name = concurrer_name
        self.concurred_on = concurred_on
        self.approver_name = approver_name
        self.approved_on = approved_on
        self.on_compliance_status = on_compliance_status

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "compliance_history_id", "compliance_id", "compliance_task", "on_statutory", "on_unit", "compliance_description",
            "start_date", "assignee_name", "completion_date", "concurrer_name", "concurred_on", "approver_name", "approved_on", "on_compliance_status"
        ])
        return GetOnoccurrencce_Last_Transaction(
            data.get("compliance_history_id"), data.get("compliance_id"), data.get("compliance_task"),
            data.get("on_statutory"), data.get("on_unit"), data.get("compliance_description"),
            data.get("start_date"), data.get("assignee_name"), data.get("completion_date"),
            data.get("concurrer_name"), data.get("concurred_on"), data.get("approver_name"),
            data.get("approved_on"), data.get("on_compliance_status")
        )

    def to_structure(self):
        return {
            "compliance_history_id": self.compliance_history_id, "compliance_id": self.compliance_id,
            "compliance_task": self.compliance_task, "on_statutory": self.on_statutory,
            "on_unit": self.on_unit, "compliance_description": self.compliance_description,
            "start_date": self.start_date, "assignee_name": self.assignee_name,
            "completion_date": self.completion_date, "concurrer_name": self.concurrer_name,
            "concurred_on": self.concurred_on, "approver_name": self.approver_name,
            "approved_on": self.approved_on, "on_compliance_status": self.on_compliance_status,
        }

#
# COMPLIANCE_FREQUENCY
#
class COMPLIANCE_FREQUENCY(object):
    def __init__(self, value):
        self._value = value

    @staticmethod
    def values():
        return ["One Time", "Periodical", "Review", "Flexi Review", "On Occurrence"]

    def value(self):
        return self._value

    @staticmethod
    def parse_structure(data):
        return parse_enum(data, COMPLIANCE_FREQUENCY.values())

    def to_structure(self):
        return parse_enum(self._value, COMPLIANCE_FREQUENCY.values())

#
# UNIR'S COMPLIANCE_FREQUENCY
#
class UnitComplianceFrequency(object):
    def __init__(self, frequency_id, frequency, u_ids):
        self.frequency_id = frequency_id
        self.frequency = frequency
        self.u_ids = u_ids

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["frequency_id", "frequency", "unit_id"])
        return UnitComplianceFrequency(data.get("frequency_id"), data.get("frequency"), data.get("u_ids"))

    def to_structure(self):
        return {"frequency_id": self.frequency_id, "frequency": self.frequency, "u_ids": self.u_ids}