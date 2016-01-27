import json
from protocol.jsonvalidators import (parse_enum, parse_dictionary, parse_static_list)
from protocol.parse_structure import (
    parse_structure_VectorType_RecordType_core_Compliance,
    parse_structure_MapType_SignedIntegerType_8_VectorType_RecordType_core_Form,
    parse_structure_EnumType_core_DURATION_TYPE,
    parse_structure_UnsignedIntegerType_32, parse_structure_Bool,
    parse_structure_VectorType_RecordType_core_ComplianceShortDescription,
    parse_structure_EnumType_core_FILTER_TYPE,
    parse_structure_EnumType_core_REPEATS_TYPE,
    parse_structure_CustomTextType_500,
    parse_structure_VectorType_SignedIntegerType_8,
    parse_structure_VectorType_RecordType_core_UnitDetails,
    parse_structure_VectorType_Text, parse_structure_CustomTextType_50,
    parse_structure_EnumType_core_COMPLIANCE_STATUS,
    parse_structure_CustomTextType_100,
    parse_structure_EnumType_core_APPROVAL_STATUS,
    parse_structure_OptionalType_Bool,
    parse_structure_VectorType_CustomTextType_50,
    parse_structure_VectorType_RecordType_core_StatutoryDate,
    parse_structure_OptionalType_SignedIntegerType_8,
    parse_structure_OptionalType_UnsignedIntegerType_32,
    parse_structure_CustomTextType_250,
    parse_structure_VectorType_RecordType_core_ComplianceApplicability,
    parse_structure_Text,
    parse_structure_EnumType_core_COMPLIANCE_FREQUENCY,
    parse_structure_CustomIntegerType_1_10,
    parse_structure_CustomIntegerType_1_12,
    parse_structure_CustomTextType_20,
    parse_structure_CustomIntegerType_1_31,
    parse_structure_OptionalType_CustomTextType_50,
    parse_structure_OptionalType_CustomTextType_500,
    parse_structure_MapType_CustomTextType_50_VectorType_RecordType_core_Form,
    parse_structure_UnsignedIntegerType_32,
    parse_structure_OptionalType_VectorType_CustomTextType_50,
    parse_structure_OptionalType_VectorType_RecordType_core_StatutoryDate,
    parse_structure_OptionalType_VectorType_RecordType_core_FileList,
    parse_structure_OptionalType_CustomIntegerType_1_100,
    parse_structure_OptionalType_CustomIntegerType_1_12,
    parse_structure_OptionalType_CustomIntegerType_1_31,
    parse_structure_Float,
    parse_structure_OptionalType_UnsignedIntegerType_32,
    parse_structure_OptionalType_VectorType_RecordType_core_ComplianceApplicability
)
from protocol.to_structure import (
    to_structure_VectorType_RecordType_core_Compliance,
    to_structure_MapType_SignedIntegerType_8_VectorType_RecordType_core_Form,
    to_structure_EnumType_core_DURATION_TYPE,
    to_structure_SignedIntegerType_8, to_structure_Bool,
    to_structure_VectorType_RecordType_core_ComplianceShortDescription,
    to_structure_EnumType_core_FILTER_TYPE,
    to_structure_EnumType_core_REPEATS_TYPE,
    to_structure_CustomTextType_500,
    to_structure_VectorType_SignedIntegerType_8,
    to_structure_VectorType_RecordType_core_UnitDetails,
    to_structure_VectorType_Text, to_structure_CustomTextType_50,
    to_structure_EnumType_core_COMPLIANCE_STATUS,
    to_structure_CustomTextType_100,
    to_structure_EnumType_core_APPROVAL_STATUS,
    to_structure_OptionalType_Bool,
    to_structure_VectorType_CustomTextType_50,
    to_structure_VectorType_RecordType_core_StatutoryDate,
    to_structure_OptionalType_SignedIntegerType_8,
    to_structure_OptionalType_UnsignedIntegerType_32,
    to_structure_CustomTextType_250,
    to_structure_VectorType_RecordType_core_ComplianceApplicability,
    to_structure_Text, to_structure_EnumType_core_COMPLIANCE_FREQUENCY,
    to_structure_CustomIntegerType_1_10,
    to_structure_CustomIntegerType_1_12, to_structure_CustomTextType_20,
    to_structure_CustomIntegerType_1_31,
    to_structure_OptionalType_CustomTextType_50,
    to_structure_OptionalType_CustomTextType_500,
    to_structure_MapType_CustomTextType_50_VectorType_RecordType_core_Form,
    to_structure_UnsignedIntegerType_32,
    to_structure_OptionalType_VectorType_CustomTextType_50,
    to_structure_OptionalType_VectorType_RecordType_core_StatutoryDate,
    to_structure_OptionalType_VectorType_RecordType_core_FileList,
    to_structure_OptionalType_CustomIntegerType_1_100,
    to_structure_OptionalType_CustomIntegerType_1_12,
    to_structure_OptionalType_CustomIntegerType_1_31,
    to_structure_Float,
    to_structure_OptionalType_UnsignedIntegerType_32,
    to_structure_VectorType_RecordType_core_ClientBusinessGroup,
    to_structure_VectorType_RecordType_core_ClientLegalEntity,
    to_structure_VectorType_RecordType_core_ClientDivision,
    to_structure_VectorType_RecordType_core_ClientUnit,
    to_structure_VectorType_RecordType_core_ClientConfiguration,
    to_structure_VectorType_UnsignedIntegerType_32,
    to_structure_OptionalType_VectorType_RecordType_core_ComplianceApplicability,
    to_structure_EnumType_core_COMPLIANCE_APPROVAL_STATUS
)

#
# SESSION_TYPE
#

class SESSION_TYPE(object):
    Web = "Web"
    Android = "Android"
    IOS = "IOS"
    BlackBerry = "BlackBerry"

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

#
# USER_TYPE
#

class USER_TYPE(object):
    Inhouse = "Inhouse"
    ServiceProvider = "ServiceProvider"

    def __init__(self, value):
        self._value = value

    @staticmethod
    def values():
        return ["Inhouse", "ServiceProvider"]

    def value(self):
        return self._value

    @staticmethod
    def parse_structure(data):
        return parse_enum(data, USER_TYPE.values())

    def to_structure(self):
        return parse_enum(self._value, USER_TYPE.values())
#
# APPROVAL_STATUS
#

class APPROVAL_STATUS(object):
    Pending = "Pending"
    Approve = "Approve"
    Reject = "Reject"
    ApproveAndNotify = "Approve & Notify"

    def __init__(self, value):
        self._value = value

    @staticmethod
    def values():
        return ["Pending", "Approve", "Reject", "Approve & Notify"]

    def value(self):
        return self._value

    @staticmethod
    def parse_structure(data):
        return parse_enum(data, APPROVAL_STATUS.values())

    def to_structure(self):
        return parse_enum(self._value, APPROVAL_STATUS.values())

#
# COMPLIANCE_APPROVAL_STATUS
#

class COMPLIANCE_APPROVAL_STATUS(object):
    Concur = "Concur"
    RejectConcurrence = "RejectConcurrence"
    Approve = "Approve"
    RejectApproval = "RejectApproval"

    def __init__(self, value):
        self._value = value

    @staticmethod
    def values():
        return ["Concur", "RejectConcurrence", "Approve", "RejectApproval"]

    def value(self):
        return self._value

    @staticmethod
    def parse_structure(data):
        return parse_enum(data, COMPLIANCE_APPROVAL_STATUS.values())

    def to_structure(self):
        return parse_enum(self._value, COMPLIANCE_APPROVAL_STATUS.values())

#
# ASSIGN_STATUTORY_SUBMISSION_STATUS
#

class ASSIGN_STATUTORY_SUBMISSION_STATUS(object):
    Submited = "Submited"
    Pending = "Pending"

    def __init__(self, value):
        self._value = value

    @staticmethod
    def values():
        return ["Submited", "Pending"]

    def value(self):
        return self._value

    @staticmethod
    def parse_structure(data):
        return parse_enum(data, ASSIGN_STATUTORY_SUBMISSION_STATUS.values())

    def to_structure(self):
        return parse_enum(self._value, ASSIGN_STATUTORY_SUBMISSION_STATUS.values())

#
# ASSIGN_STATUTORY_SUBMISSION_TYPE
#

class ASSIGN_STATUTORY_SUBMISSION_TYPE(object):
    Submit = "Submit"
    Save = "Save"

    def __init__(self, value):
        self._value = value

    @staticmethod
    def values():
        return ["Submit", "Save"]

    def value(self):
        return self._value

    @staticmethod
    def parse_structure(data):
        return parse_enum(data, ASSIGN_STATUTORY_SUBMISSION_TYPE.values())

    def to_structure(self):
        return parse_enum(self._value, ASSIGN_STATUTORY_SUBMISSION_TYPE.values())

#
# NOTIFICATION_TYPE
#

class NOTIFICATION_TYPE(object):
    Notification = "Notification"
    Reminder = "Reminder"
    Escalation = "Escalation"

    def __init__(self, value):
        self._value = value

    @staticmethod
    def values():
        return ["Notification", "Reminder", "Escalation"]

    def value(self):
        return self._value

    @staticmethod
    def parse_structure(data):
        return parse_enum(data, NOTIFICATION_TYPE.values())

    def to_structure(self):
        return parse_enum(self._value, NOTIFICATION_TYPE.values())

#
# FILTER_TYPE
#

class FILTER_TYPE(object):
    Group = "Group"
    BusinessGroup = "BusinessGroup"
    LegalEntity = "LegalEntity"
    Division = "Division"
    Unit = "Unit"

    def __init__(self, value):
        self._value = value

    @staticmethod
    def values():
        return ["Group", "BusinessGroup", "LegalEntity", "Division", "Unit"]

    def value(self):
        return self._value

    @staticmethod
    def parse_structure(data):
        return parse_enum(data, FILTER_TYPE.values())

    def to_structure(self):
        return parse_enum(self._value, FILTER_TYPE.values())

#
# COMPLIANCE_FREQUENCY
#

class COMPLIANCE_FREQUENCY(object):
    OneTime = "One Time"
    Periodical = "Periodical"
    Review = "Review"
    OnOccurrence = "On Occurrence"

    def __init__(self, value):
        self._value = value

    @staticmethod
    def values():
        return ["One Time", "Periodical", "Review", "On Occurrence"]

    def value(self):
        return self._value

    @staticmethod
    def parse_structure(data):
        return parse_enum(data, COMPLIANCE_FREQUENCY.values())

    def to_structure(self):
        return parse_enum(self._value, COMPLIANCE_FREQUENCY.values())

#
# COMPLIANCE_STATUS
#

class COMPLIANCE_STATUS(object):
    Complied = "Complied"
    DelayedCompliance = "DelayedCompliance"
    Inprogress = "Inprogress"
    NotComplied = "NotComplied"

    def __init__(self, value):
        self._value = value

    @staticmethod
    def values():
        return ["Complied", "DelayedCompliance", "Inprogress", "NotComplied"]

    def value(self):
        return self._value

    @staticmethod
    def parse_structure(data):
        return parse_enum(data, COMPLIANCE_STATUS.values())

    def to_structure(self):
        return parse_enum(self._value, COMPLIANCE_STATUS.values())

#
# APPLICABILITY_STATUS
#

class APPLICABILITY_STATUS(object):
    Applicable = "Applicable"
    NotApplicable = "NotApplicable"
    NotOpted = "NotOpted"

    def __init__(self, value):
        self._value = value

    @staticmethod
    def values():
        return ["Applicable", "NotApplicable", "NotOpted"]

    def value(self):
        return self._value

    @staticmethod
    def parse_structure(data):
        return parse_enum(data, APPLICABILITY_STATUS.values())

    def to_structure(self):
        return parse_enum(self._value, APPLICABILITY_STATUS.values())

#
# FORM_TYPE
#

class FORM_TYPE(object):
    IT = "IT"
    Knowledge = "Knowledge"
    Techno = "Techno"
    Client = "Client"
    ServiceProvider = "ServiceProvider"

    def __init__(self, value):
        self._value = value

    @staticmethod
    def values():
        return ["IT", "Knowledge", "Techno", "Client", "ServiceProvider"]

    def value(self):
        return self._value

    @staticmethod
    def parse_structure(data):
        return parse_enum(data, FORM_TYPE.values())

    def to_structure(self):
        return parse_enum(self._value, FORM_TYPE.values())

#
# REPEATS_TYPE
#

class REPEATS_TYPE(object):
    Year = "Year(s)"
    Month = "Month(s)"
    Day = "Day(s)"

    def __init__(self, value):
        self._value = value

    @staticmethod
    def values():
        return ["Year(s)", "Month(s)", "Day(s)"]

    def value(self):
        return self._value

    @staticmethod
    def parse_structure(data):
        return parse_enum(data, REPEATS_TYPE.values())

    def to_structure(self):
        return parse_enum(self._value, REPEATS_TYPE.values())

#
# DURATION_TYPE
#

class DURATION_TYPE(object):
    Day = "Day(s)"
    Hour = "Hour(s)"

    def __init__(self, value):
        self._value = value

    @staticmethod
    def values():
        return ["Day(s)", "Hour(s)"]

    def value(self):
        return self._value

    @staticmethod
    def parse_structure(data):
        return parse_enum(data, DURATION_TYPE.values())

    def to_structure(self):
        return parse_enum(self._value, DURATION_TYPE.values())

#
# COMPLIANCE_ACTIVITY_STATUS
#

class COMPLIANCE_ACTIVITY_STATUS(object):
    Submited = "Submited"
    Approved = "Approved"
    Rejected = "Rejected"

    def __init__(self, value):
        self._value = value

    @staticmethod
    def values():
        return ["Submited", "Approved", "Rejected"]

    def value(self):
        return self._value

    @staticmethod
    def parse_structure(data):
        return parse_enum(data, COMPLIANCE_ACTIVITY_STATUS.values())

    def to_structure(self):
        return parse_enum(self._value, COMPLIANCE_ACTIVITY_STATUS.values())

#
#  Form
#

class Form(object):
    def __init__(self, form_id, form_name, form_url, parent_menu, form_type):

        self.form_id = form_id
        self.form_name = form_name
        self.form_url = form_url
        self.parent_menu = parent_menu
        self.form_type = form_type

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["form_id", "form_name", "form_url", "parent_menu", "form_type"])
        form_id = data.get("form_id")
        form_id = parse_structure_UnsignedIntegerType_32(form_id)
        form_name = data.get("form_name")
        form_name = parse_structure_CustomTextType_50(form_name)
        form_url = data.get("form_url")
        form_url = parse_structure_CustomTextType_250(form_url)
        parent_menu = data.get("parent_menu")
        parent_menu = parse_structure_OptionalType_CustomTextType_50(parent_menu)
        form_type = data.get("form_type")
        form_type = parse_structure_CustomTextType_50(form_type)
        return Form(form_id, form_name, form_url, parent_menu, form_type)

    def to_structure(self):
        return {
            "form_id": to_structure_SignedIntegerType_8(self.form_id),
            "form_name": to_structure_CustomTextType_50(self.form_name),
            "form_url": to_structure_CustomTextType_250(self.form_url),
            "parent_menu": to_structure_OptionalType_CustomTextType_50(self.parent_menu),
            "form_type": to_structure_CustomTextType_50(self.form_type)
        }

#
# Menu
#

class Menu(object):
    def __init__(self, menus):
        self.menus = menus

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["menus"])
        menus = data.get("menus")
        menus = parse_structure_MapType_CustomTextType_50_VectorType_RecordType_core_Form(menus)
        return Menu(menus)

    def to_structure(self):
        return {
            "menus": to_structure_MapType_CustomTextType_50_VectorType_RecordType_core_Form(self.menus),
        }

#
# UserGroup
#

class UserGroup(object):
    def __init__(self, user_group_id, user_group_name, is_active):
        self.user_group_id = user_group_id
        self.user_group_name = user_group_name
        self.is_active = is_active

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["user_group_id", "user_group_name", "is_active"])
        user_group_id = data.get("user_group_id")
        user_group_id = parse_structure_UnsignedIntegerType_32(user_group_id)
        user_group_name = data.get("user_group_name")
        user_group_name = parse_structure_CustomTextType_50(user_group_name)
        is_active = data.get("is_active")
        is_active = parse_structure_Bool(is_active)
        return UserGroup(user_group_id, user_group_name, is_active)

    def to_structure(self):
        return {
            "user_group_id": to_structure_SignedIntegerType_8(self.user_group_id),
            "user_group_name": to_structure_CustomTextType_50(self.user_group_name),
            "is_active": to_structure_Bool(self.is_active),
        }

#
# Country
#

class Country(object):
    def __init__(self, country_id, country_name, is_active):
        self.country_id = country_id
        self.country_name = country_name
        self.is_active = is_active

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["country_id", "country_name", "is_active"])
        country_id = data.get("country_id")
        country_id = parse_structure_UnsignedIntegerType_32(country_id)
        country_name = data.get("country_name")
        country_name = parse_structure_CustomTextType_50(country_name)
        is_active = data.get("is_active")
        is_active = parse_structure_Bool(is_active)
        return Country(country_id, country_name, is_active)

    def to_structure(self):
        return {
            "country_id": to_structure_SignedIntegerType_8(self.country_id),
            "country_name": to_structure_CustomTextType_50(self.country_name),
            "is_active": to_structure_Bool(self.is_active),
        }

#
# Domain
#

class Domain(object):
    def __init__(self, domain_id, domain_name, is_active):
        self.domain_id = domain_id
        self.domain_name = domain_name
        self.is_active = is_active

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["domain_id", "domain_name", "is_active"])
        domain_id = data.get("domain_id")
        domain_id = parse_structure_UnsignedIntegerType_32(domain_id)
        domain_name = data.get("domain_name")
        domain_name = parse_structure_CustomTextType_50(domain_name)
        is_active = data.get("is_active")
        is_active = parse_structure_Bool(is_active)
        return Domain(domain_id, domain_name, is_active)

    def to_structure(self):
        return {
            "domain_id": to_structure_SignedIntegerType_8(self.domain_id),
            "domain_name": to_structure_CustomTextType_50(self.domain_name),
            "is_active": to_structure_Bool(self.is_active),
        }

#
# Level
#

class Level(object):
    def __init__(self, level_id, level_position, level_name):
        self.level_id = level_id
        self.level_position = level_position
        self.level_name = level_name

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["level_id", "level_position", "level_name"])
        level_id = data.get("level_id")
        level_id = parse_structure_OptionalType_SignedIntegerType_8(level_id)
        level_position = data.get("level_position")
        level_position = parse_structure_CustomIntegerType_1_10(level_position)
        level_name = data.get("level_name")
        level_name = parse_structure_CustomTextType_50(level_name)
        return Level(level_id, level_position, level_name)

    def to_structure(self):
        return {
            "level_id": to_structure_OptionalType_SignedIntegerType_8(self.level_id),
            "level_position": to_structure_CustomIntegerType_1_10(self.level_position),
            "level_name": to_structure_CustomTextType_50(self.level_name),
        }

#
# GeographyLevel
#

class GeographyLevel(object):
    def __init__(self, level_id, level_position, level_name):
        self.level_id = level_id
        self.level_position = level_position
        self.level_name = level_name

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["level_id", "level_position", "level_name"])
        level_id = data.get("level_id")
        level_id = parse_structure_UnsignedIntegerType_32(level_id)
        level_position = data.get("level_position")
        level_position = parse_structure_CustomIntegerType_1_10(level_position)
        level_name = data.get("level_name")
        level_name = parse_structure_CustomTextType_50(level_name)
        return GeographyLevel(level_id, level_position, level_name)

    def to_structure(self):
        return {
            "level_id": to_structure_SignedIntegerType_8(self.level_id),
            "level_position": to_structure_CustomIntegerType_1_10(self.level_position),
            "level_name": to_structure_CustomTextType_50(self.level_name),
        }

#
# Geography
#

class Geography(object):
    def __init__(self, geography_id, geography_name, level_id, parent_ids, parent_id, is_active):
        self.geography_id = geography_id
        self.geography_name = geography_name
        self.level_id = level_id
        self.parent_ids = parent_ids
        self.parent_id = parent_id
        self.is_active = is_active

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["geography_id", "geography_name", "level_id", "parent_ids", "parent_id", "is_active"])
        geography_id = data.get("geography_id")
        geography_id = parse_structure_UnsignedIntegerType_32(geography_id)
        geography_name = data.get("geography_name")
        geography_name = parse_structure_CustomTextType_50(geography_name)
        level_id = data.get("level_id")
        level_id = parse_structure_UnsignedIntegerType_32(level_id)
        parent_ids = data.get("parent_ids")
        parent_ids = parse_structure_VectorType_SignedIntegerType_8(parent_ids)
        parent_id = data.get("parent_id")
        parent_id = parse_structure_UnsignedIntegerType_32(parent_id)
        is_active = data.get("is_active")
        is_active = parse_structure_Bool(is_active)
        return Geography(geography_id, geography_name, level_id, parent_ids, parent_id, is_active)

    def to_structure(self):
        return {
            "geography_id": to_structure_SignedIntegerType_8(self.geography_id),
            "geography_name": to_structure_CustomTextType_50(self.geography_name),
            "level_id": to_structure_SignedIntegerType_8(self.level_id),
            "parent_ids": to_structure_VectorType_SignedIntegerType_8(self.parent_ids),
            "parent_id": to_structure_SignedIntegerType_8(self.parent_id),
            "is_active": to_structure_Bool(self.is_active),
        }

#
# Geography With Mapping
#

class GeographyWithMapping(object):
    def __init__(self, geography_id, geography_name, level_id, mapping, parent_id, is_active):
        self.geography_id = geography_id
        self.geography_name = geography_name
        self.level_id = level_id
        self.mapping = mapping
        self.parent_id = parent_id
        self.is_active = is_active

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["geography_id", "geography_name", "level_id", "mapping", "parent_id", "is_active"])
        geography_id = data.get("geography_id")
        geography_id = parse_structure_UnsignedIntegerType_32(geography_id)
        geography_name = data.get("geography_name")
        geography_name = parse_structure_CustomTextType_50(geography_name)
        level_id = data.get("level_id")
        level_id = parse_structure_UnsignedIntegerType_32(level_id)
        mapping = data.get("mapping")
        mapping = parse_structure_CustomTextType_250(mapping)
        parent_id = data.get("parent_id")
        parent_id = parse_structure_UnsignedIntegerType_32(parent_id)
        is_active = data.get("is_active")
        is_active = parse_structure_Bool(is_active)
        return Geography(geography_id, geography_name, level_id, mapping, parent_id, is_active)

    def to_structure(self):
        return {
            "geography_id": to_structure_SignedIntegerType_8(self.geography_id),
            "geography_name": to_structure_CustomTextType_50(self.geography_name),
            "level_id": to_structure_SignedIntegerType_8(self.level_id),
            "mapping": to_structure_CustomTextType_250(self.mapping),
            "parent_id": to_structure_SignedIntegerType_8(self.parent_id),
            "is_active": to_structure_Bool(self.is_active),
        }

#
# Industry
#

class Industry(object):
    def __init__(self, industry_id, industry_name, is_active):
        self.industry_id = industry_id
        self.industry_name = industry_name
        self.is_active = is_active

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["industry_id", "industry_name", "is_active"])
        industry_id = data.get("industry_id")
        industry_id = parse_structure_UnsignedIntegerType_32(industry_id)
        industry_name = data.get("industry_name")
        industry_name = parse_structure_CustomTextType_50(industry_name)
        is_active = data.get("is_active")
        is_active = parse_structure_Bool(is_active)
        return Industry(industry_id, industry_name, is_active)

    def to_structure(self):
        return {
            "industry_id": to_structure_SignedIntegerType_8(self.industry_id),
            "industry_name": to_structure_CustomTextType_50(self.industry_name),
            "is_active": to_structure_Bool(self.is_active),
        }

#
# StatutoryNature
#

class StatutoryNature(object):
    def __init__(self, statutory_nature_id, statutory_nature_name, is_active):
        self.statutory_nature_id = statutory_nature_id
        self.statutory_nature_name = statutory_nature_name
        self.is_active = is_active

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["statutory_nature_id", "statutory_nature_name", "is_active"])
        statutory_nature_id = data.get("statutory_nature_id")
        statutory_nature_id = parse_structure_UnsignedIntegerType_32(statutory_nature_id)
        statutory_nature_name = data.get("statutory_nature_name")
        statutory_nature_name = parse_structure_CustomTextType_50(statutory_nature_name)
        is_active = data.get("is_active")
        is_active = parse_structure_Bool(is_active)
        return StatutoryNature(statutory_nature_id, statutory_nature_name, is_active)

    def to_structure(self):
        return {
            "statutory_nature_id": to_structure_SignedIntegerType_8(self.statutory_nature_id),
            "statutory_nature_name": to_structure_CustomTextType_50(self.statutory_nature_name),
            "is_active": to_structure_Bool(self.is_active),
        }

#
# StatutoryLevel
#

class StatutoryLevel(object):
    def __init__(self, level_id, level_position, level_name):
        self.level_id = level_id
        self.level_position = level_position
        self.level_name = level_name

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["level_id", "level_position", "level_name"])
        level_id = data.get("level_id")
        level_id = parse_structure_UnsignedIntegerType_32(level_id)
        level_position = data.get("level_position")
        level_position = parse_structure_CustomIntegerType_1_10(level_position)
        level_name = data.get("level_name")
        level_name = parse_structure_CustomTextType_50(level_name)
        return StatutoryLevel(level_id, level_position, level_name)

    def to_structure(self):
        return {
            "level_id": to_structure_SignedIntegerType_8(self.level_id),
            "level_position": to_structure_CustomIntegerType_1_10(self.level_position),
            "level_name": to_structure_CustomTextType_50(self.level_name),
        }

#
# Statutory
#

class Level1Statutory(object):
    def __init__(self, level_1_statutory_id, level_1_statutory_name):
        self.level_1_statutory_id = level_1_statutory_id
        self.level_1_statutory_name = level_1_statutory_name

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["level_1_statutory_id", "level_1_statutory_name"])
        level_1_statutory_id = data.get("level_1_statutory_id")
        level_1_statutory_id = parse_structure_UnsignedIntegerType_32(level_1_statutory_id)
        level_1_statutory_name = data.get("level_1_statutory_name")
        level_1_statutory_name = parse_structure_CustomTextType_50(level_1_statutory_name)
        return Statutory(level_1_statutory_id, level_1_statutory_name)

    def to_structure(self):
        return {
            "level_1_statutory_id": to_structure_UnsignedIntegerType_32(self.level_1_statutory_id),
            "level_1_statutory_name": to_structure_CustomTextType_50(self.level_1_statutory_name)
        }


#
# Statutory
#

class Statutory(object):
    def __init__(self, statutory_id, statutory_name, level_id, parent_ids, parent_id, parent_mappings):
        self.statutory_id = statutory_id
        self.statutory_name = statutory_name
        self.level_id = level_id
        self.parent_ids = parent_ids
        self.parent_id = parent_id
        self.parent_mappings = parent_mappings

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["statutory_id", "statutory_name", "level_id", "parent_ids", "parent_id", "parent_mappings"])
        statutory_id = data.get("statutory_id")
        statutory_id = parse_structure_UnsignedIntegerType_32(statutory_id)
        statutory_name = data.get("statutory_name")
        statutory_name = parse_structure_CustomTextType_50(statutory_name)
        level_id = data.get("level_id")
        level_id = parse_structure_UnsignedIntegerType_32(level_id)
        parent_ids = data.get("parent_ids")
        parent_ids = parse_structure_VectorType_SignedIntegerType_8(parent_ids)
        parent_id = data.get("parent_id")
        parent_id = parse_structure_UnsignedIntegerType_32(parent_id)
        parent_mappings = data.get("parent_mappings")
        parent_mappings = parse_structure_Text(parent_mappings)
        return Statutory(statutory_id, statutory_name, level_id, parent_ids, parent_id, parent_mappings)

    def to_structure(self):
        return {
            "statutory_id": to_structure_SignedIntegerType_8(self.statutory_id),
            "statutory_name": to_structure_CustomTextType_50(self.statutory_name),
            "level_id": to_structure_SignedIntegerType_8(self.level_id),
            "parent_ids": to_structure_VectorType_SignedIntegerType_8(self.parent_ids),
            "parent_id": to_structure_SignedIntegerType_8(self.parent_id),
            "parent_mappings": to_structure_Text(self.parent_mappings),
        }

#
# FileList
#

class FileList(object):
    def __init__(self, file_size, file_type, file_content):
        self.file_size = file_size
        self.file_type = file_type
        self.file_content = file_content

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["file_size", "file_type", "file_content"])
        file_size = data.get("file_size")
        file_size = parse_structure_OptionalType_UnsignedIntegerType_32(file_size)
        file_type = data.get("file_type")
        file_type = parse_structure_CustomTextType_20(file_type)
        file_content = data.get("file_content")
        file_content = parse_structure_Text(file_content)
        return FileList(file_size, file_type, file_content)

    def to_structure(self):
        return {
            "file_size":to_structure_OptionalType_UnsignedIntegerType_32(self.file_size),
            "file_type": to_structure_CustomTextType_20(self.file_type),
            "file_content": to_structure_Text(self.file_content)
        }

#
# Compliance
#

class Compliance(object):
    def __init__(self, compliance_id, statutory_provision, compliance_task, description, document_name, format_file_list, penal_consequences, frequency_id, statutory_dates, repeats_type_id, repeats_every, duration_type_id, duration, is_active):
        self.compliance_id = compliance_id
        self.statutory_provision = statutory_provision
        self.compliance_task = compliance_task
        self.description = description
        self.document_name = document_name
        self.format_file_list = format_file_list
        self.penal_consequences = penal_consequences
        self.frequency_id = frequency_id
        self.statutory_dates = statutory_dates
        self.repeats_type_id = repeats_type_id
        self.repeats_every = repeats_every
        self.duration_type_id = duration_type_id
        self.duration = duration
        self.is_active = is_active

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["compliance_id", "statutory_provision", "compliance_task", "description", "document_name", "format_file_list", "penal_consequences", "frequency_id", "statutory_dates", "repeats_type_id", "repeats_every", "duration_type_id", "duration", "is_active"])
        compliance_id = data.get("compliance_id")
        compliance_id = parse_structure_OptionalType_SignedIntegerType_8(compliance_id)
        statutory_provision = data.get("statutory_provision")
        statutory_provision = parse_structure_CustomTextType_500(statutory_provision)
        compliance_task = data.get("compliance_task")
        compliance_task = parse_structure_CustomTextType_50(compliance_task)
        description = data.get("description")
        description = parse_structure_CustomTextType_500(description)
        document_name = data.get("document_name")
        document_name = parse_structure_OptionalType_CustomTextType_50(document_name)
        format_file_list = data.get("format_file_list")
        format_file_list = parse_structure_OptionalType_VectorType_RecordType_core_FileList(format_file_list)
        penal_consequences = data.get("penal_consequences")
        penal_consequences = parse_structure_OptionalType_CustomTextType_500(penal_consequences)
        frequency_id = data.get("frequency_id")
        frequency_id = parse_structure_OptionalType_SignedIntegerType_8(frequency_id)
        statutory_dates = data.get("statutory_dates")
        statutory_dates = parse_structure_OptionalType_VectorType_RecordType_core_StatutoryDate(statutory_dates)
        repeats_type_id = data.get("repeats_type_id")
        repeats_type_id = parse_structure_OptionalType_UnsignedIntegerType_32(repeats_type_id)
        repeats_every = data.get("repeats_every")
        repeats_every = parse_structure_OptionalType_UnsignedIntegerType_32(repeats_every)
        duration_type_id = data.get("duration_type_id")
        duration_type_id = parse_structure_OptionalType_UnsignedIntegerType_32(duration_type_id)
        duration = data.get("duration")
        duration = parse_structure_OptionalType_UnsignedIntegerType_32(duration)
        is_active = data.get("is_active")
        is_active = parse_structure_Bool(is_active)
        return Compliance(compliance_id, statutory_provision, compliance_task, description, document_name, format_file_list, penal_consequences, frequency_id, statutory_dates, repeats_type_id, repeats_every, duration_type_id, duration, is_active)

    def to_structure(self):
        return {
            "compliance_id": to_structure_OptionalType_SignedIntegerType_8(self.compliance_id),
            "statutory_provision": to_structure_CustomTextType_500(self.statutory_provision),
            "compliance_task": to_structure_CustomTextType_50(self.compliance_task),
            "description": to_structure_CustomTextType_500(self.description),
            "document_name": to_structure_OptionalType_CustomTextType_50(self.document_name),
            "format_file_list": to_structure_OptionalType_VectorType_RecordType_core_FileList(self.format_file_list),
            "penal_consequences": to_structure_OptionalType_CustomTextType_500(self.penal_consequences),
            "frequency_id": to_structure_OptionalType_SignedIntegerType_8(self.frequency_id),
            "statutory_dates": to_structure_OptionalType_VectorType_RecordType_core_StatutoryDate(self.statutory_dates),
            "repeats_type_id": to_structure_OptionalType_UnsignedIntegerType_32(self.repeats_type_id),
            "repeats_every": to_structure_OptionalType_UnsignedIntegerType_32(self.repeats_every),
            "duration_type_id": to_structure_OptionalType_UnsignedIntegerType_32(self.duration_type_id),
            "duration": to_structure_OptionalType_UnsignedIntegerType_32(self.duration),
            "is_active": to_structure_Bool(self.is_active),
        }

#
# StatutoryMapping
#

class StatutoryMapping(object):
    def __init__(self, country_id, country_name, domain_id, domain_name, industry_ids, industry_names, statutory_nature_id, statutory_nature_name, statutory_ids, statutory_mappings, compliances, compliance_names, geography_ids, geography_mappings, approval_status, is_active):
        self.country_id = country_id
        self.country_name = country_name
        self.domain_id = domain_id
        self.domain_name = domain_name
        self.industry_ids = industry_ids
        self.industry_names = industry_names
        self.statutory_nature_id = statutory_nature_id
        self.statutory_nature_name = statutory_nature_name
        self.statutory_ids = statutory_ids
        self.statutory_mappings = statutory_mappings
        self.compliances = compliances
        self.compliance_names = compliance_names
        self.geography_ids = geography_ids
        self.geography_mappings = geography_mappings
        self.approval_status = approval_status
        self.is_active = is_active

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["country_id", "country_name", "domain_id", "domain_name", "industry_ids", "industry_names", "statutory_nature_id", "statutory_nature_name", "statutory_ids", "statutory_mappings", "compliances", "compliance_names", "geography_ids", "geography_mappings", "approval_status", "is_active"])
        country_id = data.get("country_id")
        country_id = parse_structure_UnsignedIntegerType_32(country_id)
        country_name = data.get("country_name")
        country_name = parse_structure_CustomTextType_50(country_name)
        domain_id = data.get("domain_id")
        domain_id = parse_structure_UnsignedIntegerType_32(domain_id)
        domain_name = data.get("domain_name")
        domain_name = parse_structure_CustomTextType_50(domain_name)
        industry_ids = data.get("industry_ids")
        industry_ids = parse_structure_VectorType_SignedIntegerType_8(industry_ids)
        industry_names = data.get("industry_names")
        industry_names = parse_structure_Text(industry_names)
        statutory_nature_id = data.get("statutory_nature_id")
        statutory_nature_id = parse_structure_UnsignedIntegerType_32(statutory_nature_id)
        statutory_nature_name = data.get("statutory_nature_name")
        statutory_nature_name = parse_structure_CustomTextType_50(statutory_nature_name)
        statutory_ids = data.get("statutory_ids")
        statutory_ids = parse_structure_VectorType_SignedIntegerType_8(statutory_ids)
        statutory_mappings = data.get("statutory_mappings")
        statutory_mappings = parse_structure_VectorType_Text(statutory_mappings)
        compliances = data.get("compliances")
        compliances = parse_structure_VectorType_RecordType_core_Compliance(compliances)
        compliance_names = data.get("compliance_names")
        compliance_names = parse_structure_VectorType_Text(compliance_names)
        geography_ids = data.get("geography_ids")
        geography_ids = parse_structure_VectorType_SignedIntegerType_8(geography_ids)
        geography_mappings = data.get("geography_mappings")
        geography_mappings = parse_structure_VectorType_Text(geography_mappings)
        approval_status = data.get("approval_status")
        approval_status = parse_structure_SignedIntegerType_8(approval_status)
        is_active = data.get("is_active")
        is_active = parse_structure_Bool(is_active)
        return StatutoryMapping(country_id, country_name, domain_id, domain_name, industry_ids, industry_names, statutory_nature_id, statutory_nature_name, statutory_ids, statutory_mappings, compliances, compliance_names, geography_ids, geography_mappings, approval_status, is_active)

    def to_structure(self):
        return {
            "country_id": to_structure_SignedIntegerType_8(self.country_id),
            "country_name": to_structure_CustomTextType_50(self.country_name),
            "domain_id": to_structure_SignedIntegerType_8(self.domain_id),
            "domain_name": to_structure_CustomTextType_50(self.domain_name),
            "industry_ids": to_structure_VectorType_SignedIntegerType_8(self.industry_ids),
            "industry_names": to_structure_Text(self.industry_names),
            "statutory_nature_id": to_structure_SignedIntegerType_8(self.statutory_nature_id),
            "statutory_nature_name": to_structure_CustomTextType_50(self.statutory_nature_name),
            "statutory_ids": to_structure_VectorType_SignedIntegerType_8(self.statutory_ids),
            "statutory_mappings": to_structure_VectorType_Text(self.statutory_mappings),
            "compliances": to_structure_VectorType_RecordType_core_Compliance(self.compliances),
            "compliance_names": to_structure_VectorType_Text(self.compliance_names),
            "geography_ids": to_structure_VectorType_SignedIntegerType_8(self.geography_ids),
            "geography_mappings": to_structure_VectorType_Text(self.geography_mappings),
            "approval_status": to_structure_SignedIntegerType_8(self.approval_status),
            "is_active": to_structure_Bool(self.is_active),
        }

#
# GroupCompany
#

class GroupCompany(object):
    def __init__(self, client_id, group_name, is_active, country_ids, domain_ids):
        self.client_id = client_id
        self.group_name = group_name
        self.is_active = is_active
        self.country_ids = country_ids
        self.domain_ids = domain_ids

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["client_id", "group_name", "is_active", 
            "country_ids", "domain_ids"])
        client_id = data.get("client_id")
        client_id = parse_structure_UnsignedIntegerType_32(client_id)
        group_name = data.get("group_name")
        group_name = parse_structure_CustomTextType_50(group_name)
        is_active = data.get("is_active")
        is_active = parse_structure_Bool(is_active)
        domain_ids = data.get("domain_ids")
        domain_ids = parse_structure_VectorType_UnsignedIntegerType_32(domain_ids)
        country_ids = data.get("country_ids")
        country_ids = parse_structure_VectorType_UnsignedIntegerType_32(country_ids)

        return GroupCompany(client_id, group_name, is_active, country_ids, domain_ids)

    def to_structure(self):
        return {
            "client_id": to_structure_SignedIntegerType_8(self.client_id),
            "group_name": to_structure_CustomTextType_50(self.group_name),
            "is_active": to_structure_Bool(self.is_active),
            "country_ids": to_structure_VectorType_UnsignedIntegerType_32(self.country_ids),
            "domain_ids": to_structure_VectorType_UnsignedIntegerType_32(self.domain_ids),
        }

#
# GroupCompanyDetail
#

class GroupCompanyDetail(object):
    def __init__(self, client_id, client_name, domain_ids, country_ids, 
        incharge_persons, logo, contract_from, contract_to, no_of_user_licence, 
        total_disk_space, is_sms_subscribed, username, is_active, short_name,
        date_configurations):
        self.client_id = client_id
        self.client_name = client_name
        self.domain_ids = domain_ids
        self.country_ids = country_ids
        self.incharge_persons = incharge_persons
        self.logo = logo
        self.contract_from = contract_from
        self.contract_to = contract_to
        self.no_of_user_licence = no_of_user_licence
        self.total_disk_space = total_disk_space
        self.is_sms_subscribed = is_sms_subscribed
        self.username = username
        self.is_active = is_active
        self.short_name = short_name
        self.date_configurations = date_configurations

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["client_id", "client_name", "domain_ids", "country_ids", "incharge_persons", "logo", "contract_from", "contract_to", "no_of_user_licence", "total_disk_space", "is_sms_subscribed", "username", "is_active", "short_name"])
        client_id = data.get("client_id")
        client_id = parse_structure_UnsignedIntegerType_32(client_id)
        client_name = data.get("client_name")
        client_name = parse_structure_CustomTextType_50(client_name)
        domain_ids = data.get("domain_ids")
        domain_ids = parse_structure_VectorType_SignedIntegerType_8(domain_ids)
        country_ids = data.get("country_ids")
        country_ids = parse_structure_VectorType_SignedIntegerType_8(country_ids)
        incharge_persons = data.get("incharge_persons")
        incharge_persons = parse_structure_VectorType_SignedIntegerType_8(incharge_persons)
        logo = data.get("logo")
        logo = parse_structure_CustomTextType_250(logo)
        contract_from = data.get("contract_from")
        contract_from = parse_structure_CustomTextType_20(contract_from)
        contract_to = data.get("contract_to")
        contract_to = parse_structure_CustomTextType_20(contract_to)
        no_of_user_licence = data.get("no_of_user_licence")
        no_of_user_licence = parse_structure_UnsignedIntegerType_32(no_of_user_licence)
        total_disk_space = data.get("total_disk_space")
        total_disk_space = parse_structure_Float(total_disk_space)
        is_sms_subscribed = data.get("is_sms_subscribed")
        is_sms_subscribed = parse_structure_Bool(is_sms_subscribed)
        username = data.get("username")
        username = parse_structure_CustomTextType_100(username)
        is_active = data.get("is_active")
        is_active = parse_structure_Bool(is_active)
        short_name = data.get("short_name")
        short_name = parse_structure_CustomTextType_100(short_name)
        date_configurations = data.get("date_configurations")
        date_configurations = parse_structure_VectorType_RecordType_core_ClientConfiguration(date_configurations)
        return GroupCompanyDetail(client_id, client_name, domain_ids, 
            country_ids, incharge_persons, logo, contract_from, contract_to, 
            no_of_user_licence, total_disk_space, is_sms_subscribed, 
            username, is_active, short_name, date_configurations)

    def to_structure(self):
        return {
            "client_id": to_structure_SignedIntegerType_8(self.client_id),
            "client_name": to_structure_CustomTextType_50(self.client_name),
            "domain_ids": to_structure_VectorType_SignedIntegerType_8(self.domain_ids),
            "country_ids": to_structure_VectorType_SignedIntegerType_8(self.country_ids),
            "incharge_persons": to_structure_VectorType_SignedIntegerType_8(self.incharge_persons),
            "logo": to_structure_CustomTextType_250(self.logo),
            "contract_from": to_structure_CustomTextType_20(self.contract_from),
            "contract_to": to_structure_CustomTextType_20(self.contract_to),
            "no_of_user_licence": to_structure_SignedIntegerType_8(self.no_of_user_licence),
            "total_disk_space": to_structure_Float(self.total_disk_space),
            "is_sms_subscribed": to_structure_Bool(self.is_sms_subscribed),
            "username": to_structure_CustomTextType_100(self.username),
            "is_active": to_structure_Bool(self.is_active),
            "short_name": to_structure_CustomTextType_100(self.short_name),
            "date_configurations": to_structure_VectorType_RecordType_core_ClientConfiguration(self.date_configurations),
        }

#
# ClientConfiguration
#

class ClientConfiguration(object):
    def __init__(self, country_id, domain_id, period_from, period_to):
        self.country_id = country_id
        self.domain_id = domain_id
        self.period_from = period_from
        self.period_to = period_to

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["country_id", "domain_id", "period_from", "period_to"])
        country_id = data.get("country_id")
        country_id = parse_structure_UnsignedIntegerType_32(country_id)
        domain_id = data.get("domain_id")
        domain_id = parse_structure_UnsignedIntegerType_32(domain_id)
        period_from = data.get("period_from")
        period_from = parse_structure_UnsignedIntegerType_32(period_from)
        period_to = data.get("period_to")
        period_to = parse_structure_UnsignedIntegerType_32(period_to)
        return ClientConfiguration(country_id, domain_id, period_from, period_to)

    def to_structure(self):
        return {
            "country_id": to_structure_SignedIntegerType_8(self.country_id),
            "domain_id": to_structure_SignedIntegerType_8(self.domain_id),
            "period_from": to_structure_SignedIntegerType_8(self.period_from),
            "period_to": to_structure_SignedIntegerType_8(self.period_to),
        }

#
# BusinessGroup
#

class BusinessGroup(object):
    def __init__(self, business_group_id, business_group_name, client_id):
        self.business_group_id = business_group_id
        self.business_group_name = business_group_name
        self.client_id = client_id

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["business_group_id", "business_group_name", "client_id"])
        business_group_id = data.get("business_group_id")
        business_group_id = parse_structure_OptionalType_SignedIntegerType_8(business_group_id)
        business_group_name = data.get("business_group_name")
        business_group_name = parse_structure_CustomTextType_50(business_group_name)
        client_id = data.get("client_id")
        client_id = parse_structure_UnsignedIntegerType_32(client_id)
        return BusinessGroup(business_group_id, business_group_name, client_id)

    def to_structure(self):
        return {
            "business_group_id": to_structure_OptionalType_SignedIntegerType_8(self.business_group_id),
            "business_group_name": to_structure_CustomTextType_50(self.business_group_name),
            "client_id": to_structure_SignedIntegerType_8(self.client_id),
        }

class ClientBusinessGroup(object):
    def __init__(self, business_group_id, business_group_name):
        self.business_group_id = business_group_id
        self.business_group_name = business_group_name

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["business_group_id", "business_group_name"])
        business_group_id = data.get("business_group_id")
        business_group_id = parse_structure_OptionalType_SignedIntegerType_8(business_group_id)
        business_group_name = data.get("business_group_name")
        business_group_name = parse_structure_CustomTextType_50(business_group_name)
        return BusinessGroup(business_group_id, business_group_name)

    def to_structure(self):
        return {
            "business_group_id": to_structure_OptionalType_SignedIntegerType_8(self.business_group_id),
            "business_group_name": to_structure_CustomTextType_50(self.business_group_name),
        }

#
# LegalEntity
#

class LegalEntity(object):
    def __init__(self, legal_entity_id, legal_entity_name, business_group_id, client_id):
        self.legal_entity_id = legal_entity_id
        self.legal_entity_name = legal_entity_name
        self.business_group_id = business_group_id
        self.client_id = client_id

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["legal_entity_id", "legal_entity_name", "business_group_id", "client_id"])
        legal_entity_id = data.get("legal_entity_id")
        legal_entity_id = parse_structure_OptionalType_SignedIntegerType_8(legal_entity_id)
        legal_entity_name = data.get("legal_entity_name")
        legal_entity_name = parse_structure_CustomTextType_50(legal_entity_name)
        business_group_id = data.get("business_group_id")
        business_group_id = parse_structure_OptionalType_SignedIntegerType_8(business_group_id)
        client_id = data.get("client_id")
        client_id = parse_structure_UnsignedIntegerType_32(client_id)
        return LegalEntity(legal_entity_id, legal_entity_name, business_group_id, client_id)

    def to_structure(self):
        return {
            "legal_entity_id": to_structure_OptionalType_SignedIntegerType_8(self.legal_entity_id),
            "legal_entity_name": to_structure_CustomTextType_50(self.legal_entity_name),
            "business_group_id": to_structure_OptionalType_SignedIntegerType_8(self.business_group_id),
            "client_id": to_structure_SignedIntegerType_8(self.client_id),
        }

class ClientLegalEntity(object):
    def __init__(self, legal_entity_id, legal_entity_name, business_group_id):
        self.legal_entity_id = legal_entity_id
        self.legal_entity_name = legal_entity_name
        self.business_group_id = business_group_id

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["legal_entity_id", "legal_entity_name", "business_group_id"])
        legal_entity_id = data.get("legal_entity_id")
        legal_entity_id = parse_structure_OptionalType_SignedIntegerType_8(legal_entity_id)
        legal_entity_name = data.get("legal_entity_name")
        legal_entity_name = parse_structure_CustomTextType_50(legal_entity_name)
        business_group_id = data.get("business_group_id")
        business_group_id = parse_structure_OptionalType_SignedIntegerType_8(business_group_id)
        return ClientLegalEntity(legal_entity_id, legal_entity_name, business_group_id)

    def to_structure(self):
        return {
            "legal_entity_id": to_structure_OptionalType_SignedIntegerType_8(self.legal_entity_id),
            "legal_entity_name": to_structure_CustomTextType_50(self.legal_entity_name),
            "business_group_id": to_structure_OptionalType_SignedIntegerType_8(self.business_group_id),
        }

#
# Division
#

class Division(object):
    def __init__(self, division_id, division_name, legal_entity_id, business_group_id, client_id):
        self.division_id = division_id
        self.division_name = division_name
        self.legal_entity_id = legal_entity_id
        self.business_group_id = business_group_id
        self.client_id = client_id

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["division_id", "division_name", "legal_entity_id", "business_group_id", "client_id"])
        division_id = data.get("division_id")
        division_id = parse_structure_OptionalType_SignedIntegerType_8(division_id)
        division_name = data.get("division_name")
        division_name = parse_structure_CustomTextType_50(division_name)
        legal_entity_id = data.get("legal_entity_id")
        legal_entity_id = parse_structure_UnsignedIntegerType_32(legal_entity_id)
        business_group_id = data.get("business_group_id")
        business_group_id = parse_structure_UnsignedIntegerType_32(business_group_id)
        client_id = data.get("client_id")
        client_id = parse_structure_UnsignedIntegerType_32(client_id)
        return Division(division_id, division_name, legal_entity_id, business_group_id, client_id)

    def to_structure(self):
        return {
            "division_id": to_structure_OptionalType_SignedIntegerType_8(self.division_id),
            "division_name": to_structure_CustomTextType_50(self.division_name),
            "legal_entity_id": to_structure_SignedIntegerType_8(self.legal_entity_id),
            "business_group_id": to_structure_SignedIntegerType_8(self.business_group_id),
            "client_id": to_structure_SignedIntegerType_8(self.client_id),
        }

class ClientDivision(object):
    def __init__(self, division_id, division_name, legal_entity_id, business_group_id):
        self.division_id = division_id
        self.division_name = division_name
        self.legal_entity_id = legal_entity_id
        self.business_group_id = business_group_id

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["division_id", "division_name", "legal_entity_id", "business_group_id"])
        division_id = data.get("division_id")
        division_id = parse_structure_OptionalType_SignedIntegerType_8(division_id)
        division_name = data.get("division_name")
        division_name = parse_structure_CustomTextType_50(division_name)
        legal_entity_id = data.get("legal_entity_id")
        legal_entity_id = parse_structure_UnsignedIntegerType_32(legal_entity_id)
        business_group_id = data.get("business_group_id")
        business_group_id = parse_structure_UnsignedIntegerType_32(business_group_id)
        return Division(division_id, division_name, legal_entity_id, business_group_id)

    def to_structure(self):
        return {
            "division_id": to_structure_OptionalType_SignedIntegerType_8(self.division_id),
            "division_name": to_structure_CustomTextType_50(self.division_name),
            "legal_entity_id": to_structure_SignedIntegerType_8(self.legal_entity_id),
            "business_group_id": to_structure_SignedIntegerType_8(self.business_group_id),
        }

#
# Unit
#

class Unit(object):
    def __init__(self, unit_id, division_id, legal_entity_id, business_group_id, client_id, unit_code, unit_name, unit_address, is_active):
        self.unit_id = unit_id
        self.division_id = division_id
        self.legal_entity_id = legal_entity_id
        self.business_group_id = business_group_id
        self.client_id = client_id
        self.unit_code = unit_code
        self.unit_name = unit_name
        self.unit_address = unit_address
        self.is_active = is_active

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["unit_id", "division_id", "legal_entity_id", "business_group_id", "client_id", "unit_code", "unit_name", "unit_address", "is_active"])
        unit_id = data.get("unit_id")
        unit_id = parse_structure_OptionalType_SignedIntegerType_8(unit_id)
        division_id = data.get("division_id")
        division_id = parse_structure_OptionalType_SignedIntegerType_8(division_id)
        legal_entity_id = data.get("legal_entity_id")
        legal_entity_id = parse_structure_UnsignedIntegerType_32(legal_entity_id)
        business_group_id = data.get("business_group_id")
        business_group_id = parse_structure_OptionalType_SignedIntegerType_8(business_group_id)
        client_id = data.get("client_id")
        client_id = parse_structure_UnsignedIntegerType_32(client_id)
        unit_code = data.get("unit_code")
        unit_code = parse_structure_CustomTextType_20(unit_code)
        unit_name = data.get("unit_name")
        unit_name = parse_structure_CustomTextType_50(unit_name)
        unit_address = data.get("unit_address")
        unit_address = parse_structure_CustomTextType_250(unit_address)
        is_active = data.get("is_active")
        is_active = parse_structure_Bool(is_active)
        return Unit(unit_id, division_id, legal_entity_id, business_group_id, client_id, unit_code, unit_name, unit_address, is_active)

    def to_structure(self):
        return {
            "unit_id": to_structure_OptionalType_SignedIntegerType_8(self.unit_id),
            "division_id": to_structure_OptionalType_SignedIntegerType_8(self.division_id),
            "legal_entity_id": to_structure_SignedIntegerType_8(self.legal_entity_id),
            "business_group_id": to_structure_OptionalType_SignedIntegerType_8(self.business_group_id),
            "client_id": to_structure_SignedIntegerType_8(self.client_id),
            "unit_code": to_structure_CustomTextType_20(self.unit_code),
            "unit_name": to_structure_CustomTextType_50(self.unit_name),
            "unit_address": to_structure_CustomTextType_250(self.unit_address),
            "is_active": to_structure_Bool(self.is_active)
        }

class ClientUnit(object):
    def __init__(self, unit_id, division_id, legal_entity_id, business_group_id, unit_code, unit_name, unit_address, is_active):
        self.unit_id = unit_id
        self.division_id = division_id
        self.legal_entity_id = legal_entity_id
        self.business_group_id = business_group_id
        self.unit_code = unit_code
        self.unit_name = unit_name
        self.unit_address = unit_address
        self.is_active = is_active

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["unit_id", "division_id", "legal_entity_id", "business_group_id", "unit_code", "unit_name", "unit_address", "is_active"])
        unit_id = data.get("unit_id")
        unit_id = parse_structure_OptionalType_SignedIntegerType_8(unit_id)
        division_id = data.get("division_id")
        division_id = parse_structure_OptionalType_SignedIntegerType_8(division_id)
        legal_entity_id = data.get("legal_entity_id")
        legal_entity_id = parse_structure_UnsignedIntegerType_32(legal_entity_id)
        business_group_id = data.get("business_group_id")
        business_group_id = parse_structure_OptionalType_SignedIntegerType_8(business_group_id)
        unit_code = data.get("unit_code")
        unit_code = parse_structure_CustomTextType_20(unit_code)
        unit_name = data.get("unit_name")
        unit_name = parse_structure_CustomTextType_50(unit_name)
        unit_address = data.get("unit_address")
        unit_address = parse_structure_CustomTextType_250(unit_address)
        is_active = data.get("is_active")
        is_active = parse_structure_Bool(is_active)
        return Unit(unit_id, division_id, legal_entity_id, business_group_id, unit_code, unit_name, unit_address, is_active)

    def to_structure(self):
        return {
            "unit_id": to_structure_OptionalType_SignedIntegerType_8(self.unit_id),
            "division_id": to_structure_OptionalType_SignedIntegerType_8(self.division_id),
            "legal_entity_id": to_structure_SignedIntegerType_8(self.legal_entity_id),
            "business_group_id": to_structure_OptionalType_SignedIntegerType_8(self.business_group_id),
            "unit_code": to_structure_CustomTextType_20(self.unit_code),
            "unit_name": to_structure_CustomTextType_50(self.unit_name),
            "unit_address": to_structure_CustomTextType_250(self.unit_address),
            "is_active": to_structure_Bool(self.is_active)
        }

#
# UnitDetails
#

class UnitDetails(object):
    def __init__(self, unit_id, division_id, legal_entity_id, business_group_id, client_id, country_id, geography_id, unit_code, unit_name, industry_id, unit_address, postal_code, domain_ids, is_active):
        self.unit_id = unit_id
        self.division_id = division_id
        self.legal_entity_id = legal_entity_id
        self.business_group_id = business_group_id
        self.client_id = client_id
        self.country_id = country_id
        self.geography_id = geography_id
        self.unit_code = unit_code
        self.unit_name = unit_name
        self.industry_id = industry_id
        self.unit_address = unit_address
        self.postal_code = postal_code
        self.domain_ids = domain_ids
        self.is_active = is_active

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["unit_id", "division_id", "legal_entity_id", "business_group_id", "client_id", "country_id", "geography_id", "unit_code", "unit_name", "industry_id", "unit_address", "postal_code", "domain_ids", "is_active"])
        unit_id = data.get("unit_id")
        unit_id = parse_structure_OptionalType_SignedIntegerType_8(unit_id)
        division_id = data.get("division_id")
        division_id = parse_structure_OptionalType_SignedIntegerType_8(division_id)
        legal_entity_id = data.get("legal_entity_id")
        legal_entity_id = parse_structure_UnsignedIntegerType_32(legal_entity_id)
        business_group_id = data.get("business_group_id")
        business_group_id = parse_structure_OptionalType_SignedIntegerType_8(business_group_id)
        client_id = data.get("client_id")
        client_id = parse_structure_UnsignedIntegerType_32(client_id)
        country_id = data.get("country_id")
        country_id = parse_structure_UnsignedIntegerType_32(country_id)
        geography_id = data.get("geography_id")
        geography_id = parse_structure_UnsignedIntegerType_32(geography_id)
        unit_code = data.get("unit_code")
        unit_code = parse_structure_CustomTextType_20(unit_code)
        unit_name = data.get("unit_name")
        unit_name = parse_structure_CustomTextType_50(unit_name)
        industry_id = data.get("industry_id")
        industry_id = parse_structure_UnsignedIntegerType_32(industry_id)
        unit_address = data.get("unit_address")
        unit_address = parse_structure_CustomTextType_250(unit_address)
        postal_code = data.get("postal_code")
        postal_code = parse_structure_UnsignedIntegerType_32(postal_code)
        domain_ids = data.get("domain_ids")
        domain_ids = parse_structure_VectorType_SignedIntegerType_8(domain_ids)
        is_active = data.get("is_active")
        is_active = parse_structure_Bool(is_active)
        return UnitDetails(unit_id, division_id, legal_entity_id, business_group_id, client_id, country_id, geography_id, unit_code, unit_name, industry_id, unit_address, postal_code, domain_ids, is_active)

    def to_structure(self):
        return {
            "unit_id": to_structure_OptionalType_SignedIntegerType_8(self.unit_id),
            "division_id": to_structure_OptionalType_SignedIntegerType_8(self.division_id),
            "legal_entity_id": to_structure_SignedIntegerType_8(self.legal_entity_id),
            "business_group_id": to_structure_OptionalType_SignedIntegerType_8(self.business_group_id),
            "client_id": to_structure_SignedIntegerType_8(self.client_id),
            "country_id": to_structure_SignedIntegerType_8(self.country_id),
            "geography_id": to_structure_SignedIntegerType_8(self.geography_id),
            "unit_code": to_structure_CustomTextType_20(self.unit_code),
            "unit_name": to_structure_CustomTextType_50(self.unit_name),
            "industry_id": to_structure_SignedIntegerType_8(self.industry_id),
            "unit_address": to_structure_CustomTextType_250(self.unit_address),
            "postal_code": to_structure_SignedIntegerType_8(self.postal_code),
            "domain_ids": to_structure_VectorType_SignedIntegerType_8(self.domain_ids),
            "is_active": to_structure_Bool(self.is_active),
        }

#
# ServiceProvider
#

class ServiceProvider(object):
    def __init__(self, service_provider_id, service_provider_name, is_active):
        self.service_provider_id = service_provider_id
        self.service_provider_name = service_provider_name
        self.is_active = is_active

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["service_provider_id", "service_provider_name","is_active"])
        service_provider_id = data.get("service_provider_id")
        service_provider_id = parse_structure_OptionalType_SignedIntegerType_8(service_provider_id)
        service_provider_name = data.get("service_provider_name")
        service_provider_name = parse_structure_CustomTextType_50(service_provider_name)
        is_active = data.get("is_active")
        is_active = parse_structure_OptionalType_Bool(is_active)
        return ServiceProvider(service_provider_id, service_provider_name, is_active)

    def to_structure(self):
        return {
            "service_provider_id": to_structure_OptionalType_SignedIntegerType_8(self.service_provider_id),
            "service_provider_name": to_structure_CustomTextType_50(self.service_provider_name),
            "is_active": to_structure_OptionalType_Bool(self.is_active),
        }

class ServiceProviderDetails(object):
    def __init__(self, service_provider_id, service_provider_name, address, contract_from, contract_to, contact_person, contact_no, is_active):
        self.service_provider_id = service_provider_id
        self.service_provider_name = service_provider_name
        self.address = address
        self.contract_from = contract_from
        self.contract_to = contract_to
        self.contact_person = contact_person
        self.contact_no = contact_no
        self.is_active = is_active

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["service_provider_id", "service_provider_name", "address", "contract_from", "contract_to", "contact_person", "contact_no", "is_active"])
        service_provider_id = data.get("service_provider_id")
        service_provider_id = parse_structure_OptionalType_SignedIntegerType_8(service_provider_id)
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
        is_active = data.get("is_active")
        is_active = parse_structure_OptionalType_Bool(is_active)
        return ServiceProviderDetails(service_provider_id, service_provider_name, address, contract_from, contract_to, contact_person, contact_no, is_active)

    def to_structure(self):
        return {
            "service_provider_id": to_structure_OptionalType_SignedIntegerType_8(self.service_provider_id),
            "service_provider_name": to_structure_CustomTextType_50(self.service_provider_name),
            "address": to_structure_CustomTextType_250(self.address),
            "contract_from": to_structure_CustomTextType_20(self.contract_from),
            "contract_to": to_structure_CustomTextType_20(self.contract_to),
            "contact_person": to_structure_CustomTextType_50(self.contact_person),
            "contact_no": to_structure_CustomTextType_20(self.contact_no),
            "is_active": to_structure_OptionalType_Bool(self.is_active),
        }

#
# ClientUser
#

class ClientUser(object):
    def __init__(self, user_id, email_id, user_group_id, employee_name, employee_code, contact_no, seating_unit_id, user_level, country_ids, domain_ids, unit_ids, is_admin, is_service_provider, service_provider_id, is_active):
        self.user_id = user_id
        self.email_id = email_id
        self.user_group_id = user_group_id
        self.employee_name = employee_name
        self.employee_code = employee_code
        self.contact_no = contact_no
        self.seating_unit_id = seating_unit_id
        self.user_level = user_level
        self.country_ids = country_ids
        self.domain_ids = domain_ids
        self.unit_ids = unit_ids
        self.is_admin = is_admin
        self.is_service_provider = is_service_provider
        self.service_provider_id = service_provider_id
        self.is_active = is_active

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["user_id", "email_id", "user_group_id", "employee_name", "employee_code", "contact_no", "seating_unit_id", "user_level", "country_ids", "domain_ids", "unit_ids", "is_admin", "is_service_provider", "service_provider_id", "is_active"])
        user_id = data.get("user_id")
        user_id = parse_structure_UnsignedIntegerType_32(user_id)
        email_id = data.get("email_id")
        email_id = parse_structure_CustomTextType_100(email_id)
        user_group_id = data.get("user_group_id")
        user_group_id = parse_structure_UnsignedIntegerType_32(user_group_id)
        employee_name = data.get("employee_name")
        employee_name = parse_structure_CustomTextType_50(employee_name)
        employee_code = data.get("employee_code")
        employee_code = parse_structure_CustomTextType_50(employee_code)
        contact_no = data.get("contact_no")
        contact_no = parse_structure_CustomTextType_20(contact_no)
        seating_unit_id = data.get("seating_unit_id")
        seating_unit_id = parse_structure_UnsignedIntegerType_32(seating_unit_id)
        user_level = data.get("user_level")
        user_level = parse_structure_CustomIntegerType_1_10(user_level)
        country_ids = data.get("country_ids")
        country_ids = parse_structure_VectorType_SignedIntegerType_8(country_ids)
        domain_ids = data.get("domain_ids")
        domain_ids = parse_structure_VectorType_SignedIntegerType_8(domain_ids)
        unit_ids = data.get("unit_ids")
        unit_ids = parse_structure_VectorType_SignedIntegerType_8(unit_ids)
        is_admin = data.get("is_admin")
        is_admin = parse_structure_Bool(is_admin)
        is_service_provider = data.get("is_service_provider")
        is_service_provider = parse_structure_Bool(is_service_provider)
        service_provider_id = data.get("service_provider_id")
        service_provider_id = parse_structure_OptionalType_UnsignedIntegerType_32(service_provider_id)
        is_active = data.get("is_active")
        is_active = parse_structure_Bool(is_active)
        return ClientUser(user_id, email_id, user_group_id, employee_name, employee_code, contact_no, seating_unit_id, seating_unit_name, user_level, country_ids, domain_ids, unit_ids, is_admin, is_service_provider, service_provider_id, is_active)

    def to_structure(self):
        print "inside core client users inner structure"
        return {
            "user_id": to_structure_SignedIntegerType_8(self.user_id),
            "email_id": to_structure_CustomTextType_100(self.email_id),
            "user_group_id": to_structure_SignedIntegerType_8(self.user_group_id),
            "employee_name": to_structure_CustomTextType_50(self.employee_name),
            "employee_code": to_structure_CustomTextType_50(self.employee_code),
            "contact_no": to_structure_CustomTextType_20(self.contact_no),
            "seating_unit_id": to_structure_SignedIntegerType_8(self.seating_unit_id),
            "user_level": to_structure_CustomIntegerType_1_10(self.user_level),
            "country_ids": to_structure_VectorType_SignedIntegerType_8(self.country_ids),
            "domain_ids": to_structure_VectorType_SignedIntegerType_8(self.domain_ids),
            "unit_ids": to_structure_VectorType_SignedIntegerType_8(self.unit_ids),
            "is_admin": to_structure_Bool(self.is_admin),
            "is_service_provider": to_structure_Bool(self.is_service_provider),
            "service_provider_id": to_structure_OptionalType_UnsignedIntegerType_32(self.service_provider_id),
            "is_active": to_structure_Bool(self.is_active),
        }

#
# AssignedStatutory
#

class AssignedStatutory(object):
    def __init__(self, level_1_statutory_id, level_1_statutory_name, compliances, applicable_status, opted_status, not_applicable_remarks):
        self.level_1_statutory_id = level_1_statutory_id
        self.level_1_statutory_name = level_1_statutory_name
        self.compliances = compliances
        self.applicable_status = applicable_status
        self.opted_status = opted_status
        self.not_applicable_remarks = not_applicable_remarks

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["level_1_statutory_id", "level_1_statutory_name", "compliances", "applicable_status", "opted_status", "not_applicable_remarks"])
        level_1_statutory_id = data.get("level_1_statutory_id")
        level_1_statutory_id = parse_structure_UnsignedIntegerType_32(level_1_statutory_id)
        level_1_statutory_name = data.get("level_1_statutory_name")
        level_1_statutory_name = parse_structure_CustomTextType_50(level_1_statutory_name)
        compliances = data.get("compliances")
        compliances = parse_structure_OptionalType_VectorType_RecordType_core_ComplianceApplicability(compliances)
        applicable_status = data.get("applicable_status")
        applicable_status = parse_structure_Bool(applicable_status)
        opted_status = data.get(opted_status)
        opted_status = parse_structure_OptionalType_Bool(opted_status)
        not_applicable_remarks = data.get("not_applicable_remarks")
        not_applicable_remarks = parse_structure_OptionalType_CustomTextType_500(not_applicable_remarks)
        return AssignedStatutory(level_1_statutory_id, level_1_statutory_name, compliances, applicable_status, opted_status, not_applicable_remarks)

    def to_structure(self):
        return {
            "level_1_statutory_id": to_structure_SignedIntegerType_8(self.level_1_statutory_id),
            "level_1_statutory_name": to_structure_CustomTextType_50(self.level_1_statutory_name),
            "compliances": to_structure_OptionalType_VectorType_RecordType_core_ComplianceApplicability(self.compliances),
            "applicable_status": to_structure_Bool(self.applicable_status),
            "opted_status": to_structure_OptionalType_Bool(self.opted_status),
            "not_applicable_remarks": to_structure_OptionalType_CustomTextType_500(self.not_applicable_remarks),
        }

#
# ActiveCompliance
#

class ActiveCompliance(object):
    def __init__(self, compliance_history_id, compliance_name, compliance_frequency, domain_name, start_date, due_date, compliance_status, validity_date, next_due_date, ageing, format_file_name):
        self.compliance_history_id = compliance_history_id
        self.compliance_name = compliance_name
        self.compliance_frequency = compliance_frequency
        self.domain_name = domain_name
        self.start_date = start_date
        self.due_date = due_date
        self.compliance_status = compliance_status
        self.validity_date = validity_date
        self.next_due_date = next_due_date
        self.ageing = ageing
        self.format_file_name = format_file_name

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["compliance_history_id", "compliance_name", "compliance_frequency", "domain_name", "start_date", "due_date", "compliance_status", "validity_date", "next_due_date", "ageing", "format_file_name"])
        compliance_history_id = data.get("compliance_history_id")
        compliance_history_id = parse_structure_UnsignedIntegerType_32(compliance_history_id)
        compliance_name = data.get("compliance_name")
        compliance_name = parse_structure_CustomTextType_50(compliance_name)
        compliance_frequency = data.get("compliance_frequency")
        compliance_frequency = parse_structure_EnumType_core_COMPLIANCE_FREQUENCY(compliance_frequency)
        domain_name = data.get("domain_name")
        domain_name = parse_structure_CustomTextType_50(domain_name)
        start_date = data.get("start_date")
        start_date = parse_structure_CustomTextType_20(start_date)
        due_date = data.get("due_date")
        due_date = parse_structure_CustomTextType_20(due_date)
        compliance_status = data.get("compliance_status")
        compliance_status = parse_structure_Bool(compliance_status)
        validity_date = data.get("validity_date")
        validity_date = parse_structure_CustomTextType_20(validity_date)
        next_due_date = data.get("next_due_date")
        next_due_date = parse_structure_CustomTextType_20(next_due_date)
        ageing = data.get("ageing")
        ageing = parse_structure_UnsignedIntegerType_32(ageing)
        format_file_name = data.get("format_file_name")
        format_file_name = parse_structure_VectorType_CustomTextType_50(format_file_name)
        return ActiveCompliance(compliance_history_id, compliance_name, compliance_frequency, domain_name, start_date, due_date, compliance_status, validity_date, next_due_date, ageing, format_file_name)

    def to_structure(self):
        return {
            "compliance_history_id": to_structure_SignedIntegerType_8(self.compliance_history_id),
            "compliance_name": to_structure_CustomTextType_50(self.compliance_name),
            "compliance_frequency": to_structure_EnumType_core_COMPLIANCE_FREQUENCY(self.compliance_frequency),
            "domain_name": to_structure_CustomTextType_50(self.domain_name),
            "start_date": to_structure_CustomTextType_20(self.start_date),
            "due_date": to_structure_CustomTextType_20(self.due_date),
            "compliance_status": to_structure_Bool(self.compliance_status),
            "validity_date": to_structure_CustomTextType_20(self.validity_date),
            "next_due_date": to_structure_CustomTextType_20(self.next_due_date),
            "ageing": to_structure_SignedIntegerType_8(self.ageing),
            "format_file_name": to_structure_VectorType_CustomTextType_50(self.format_file_name),
        }

#
# UpcomingCompliance
#

class UpcomingCompliance(object):
    def __init__(self, compliance_history_id, compliance_name, compliance_frequency, domain_name, start_date, due_date, format_file_name):
        self.compliance_history_id = compliance_history_id
        self.compliance_name = compliance_name
        self.compliance_frequency = compliance_frequency
        self.domain_name = domain_name
        self.start_date = start_date
        self.due_date = due_date
        self.format_file_name = format_file_name

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["compliance_history_id", "compliance_name", "compliance_frequency", "domain_name", "start_date", "due_date", "format_file_name"])
        compliance_history_id = data.get("compliance_history_id")
        compliance_history_id = parse_structure_UnsignedIntegerType_32(compliance_history_id)
        compliance_name = data.get("compliance_name")
        compliance_name = parse_structure_CustomTextType_50(compliance_name)
        compliance_frequency = data.get("compliance_frequency")
        compliance_frequency = parse_structure_EnumType_core_COMPLIANCE_FREQUENCY(compliance_frequency)
        domain_name = data.get("domain_name")
        domain_name = parse_structure_CustomTextType_50(domain_name)
        start_date = data.get("start_date")
        start_date = parse_structure_CustomTextType_20(start_date)
        due_date = data.get("due_date")
        due_date = parse_structure_CustomTextType_20(due_date)
        format_file_name = data.get("format_file_name")
        format_file_name = parse_structure_VectorType_CustomTextType_50(format_file_name)
        return UpcomingCompliance(compliance_history_id, compliance_name, compliance_frequency, domain_name, start_date, due_date, format_file_name)

    def to_structure(self):
        return {
            "compliance_history_id": to_structure_SignedIntegerType_8(self.compliance_history_id),
            "compliance_name": to_structure_CustomTextType_50(self.compliance_name),
            "compliance_frequency": to_structure_EnumType_core_COMPLIANCE_FREQUENCY(self.compliance_frequency),
            "domain_name": to_structure_CustomTextType_50(self.domain_name),
            "start_date": to_structure_CustomTextType_20(self.start_date),
            "due_date": to_structure_CustomTextType_20(self.due_date),
            "format_file_name": to_structure_VectorType_CustomTextType_50(self.format_file_name),
        }

#
# NumberOfCompliances
#

class NumberOfCompliances(object):
    def __init__(self, year, complied_count, delayed_compliance_count, inprogress_compliance_count, not_complied_count):
        self.year = year
        self.complied_count = complied_count
        self.delayed_compliance_count = delayed_compliance_count
        self.inprogress_compliance_count = inprogress_compliance_count
        self.not_complied_count = not_complied_count

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["year", "complied_count", "delayed_compliance_count", "inprogress_compliance_count", "not_complied_count"])
        year = data.get("year")
        year = parse_structure_CustomTextType_20(year)
        complied_count = data.get("complied_count")
        complied_count = parse_structure_UnsignedIntegerType_32(complied_count)
        delayed_compliance_count = data.get("delayed_compliance_count")
        delayed_compliance_count = parse_structure_UnsignedIntegerType_32(delayed_compliance_count)
        inprogress_compliance_count = data.get("inprogress_compliance_count")
        inprogress_compliance_count = parse_structure_UnsignedIntegerType_32(inprogress_compliance_count)
        not_complied_count = data.get("not_complied_count")
        not_complied_count = parse_structure_UnsignedIntegerType_32(not_complied_count)
        return NumberOfCompliances(year, complied_count, delayed_compliance_count, inprogress_compliance_count, not_complied_count)

    def to_structure(self):
        return {
            "year": to_structure_CustomTextType_20(self.year),
            "complied_count": to_structure_SignedIntegerType_8(self.complied_count),
            "delayed_compliance_count": to_structure_SignedIntegerType_8(self.delayed_compliance_count),
            "inprogress_compliance_count": to_structure_SignedIntegerType_8(self.inprogress_compliance_count),
            "not_complied_count": to_structure_SignedIntegerType_8(self.not_complied_count),
        }

#
# ChartFilters
#

class ChartFilters(object):
    def __init__(self, country_id, domain_id, from_date, to_date, filter_type, filter_id):
        self.country_id = country_id
        self.domain_id = domain_id
        self.from_date = from_date
        self.to_date = to_date
        self.filter_type = filter_type
        self.filter_id = filter_id

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["country_id", "domain_id", "from_date", "to_date", "filter_type", "filter_id"])
        country_id = data.get("country_id")
        country_id = parse_structure_UnsignedIntegerType_32(country_id)
        domain_id = data.get("domain_id")
        domain_id = parse_structure_UnsignedIntegerType_32(domain_id)
        from_date = data.get("from_date")
        from_date = parse_structure_CustomTextType_20(from_date)
        to_date = data.get("to_date")
        to_date = parse_structure_CustomTextType_20(to_date)
        filter_type = data.get("filter_type")
        filter_type = parse_structure_EnumType_core_FILTER_TYPE(filter_type)
        filter_id = data.get("filter_id")
        filter_id = parse_structure_UnsignedIntegerType_32(filter_id)
        return ChartFilters(country_id, domain_id, from_date, to_date, filter_type, filter_id)

    def to_structure(self):
        return {
            "country_id": to_structure_SignedIntegerType_8(self.country_id),
            "domain_id": to_structure_SignedIntegerType_8(self.domain_id),
            "from_date": to_structure_CustomTextType_20(self.from_date),
            "to_date": to_structure_CustomTextType_20(self.to_date),
            "filter_type": to_structure_EnumType_core_FILTER_TYPE(self.filter_type),
            "filter_id": to_structure_SignedIntegerType_8(self.filter_id),
        }

#
# ComplianceStatusDrillDown
#

class ComplianceStatusDrillDown(object):
    def __init__(self, unit_name, address, compliances):
        self.unit_name = unit_name
        self.address = address
        self.compliances = compliances

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["unit_name", "address", "compliances"])
        unit_name = data.get("unit_name")
        unit_name = parse_structure_UnsignedIntegerType_32(unit_name)
        address = data.get("address")
        address = parse_structure_UnsignedIntegerType_32(address)
        compliances = data.get("compliances")
        compliances = parse_structure_VectorType_RecordType_core_ComplianceShortDescription(compliances)
        return ComplianceStatusDrillDown(unit_name, address, compliances)

    def to_structure(self):
        return {
            "unit_name": to_structure_SignedIntegerType_8(self.unit_name),
            "address": to_structure_SignedIntegerType_8(self.address),
            "compliances": to_structure_VectorType_RecordType_core_ComplianceShortDescription(self.compliances),
        }

#
# EscalationsDrillDown
#

class EscalationsDrillDown(object):
    def __init__(self, unit_name, address, compliances):
        self.unit_name = unit_name
        self.address = address
        self.compliances = compliances

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["unit_name", "address", "compliances"])
        unit_name = data.get("unit_name")
        unit_name = parse_structure_UnsignedIntegerType_32(unit_name)
        address = data.get("address")
        address = parse_structure_UnsignedIntegerType_32(address)
        compliances = data.get("compliances")
        compliances = parse_structure_VectorType_RecordType_core_ComplianceShortDescription(compliances)
        return EscalationsDrillDown(unit_name, address, compliances)

    def to_structure(self):
        return {
            "unit_name": to_structure_SignedIntegerType_8(self.unit_name),
            "address": to_structure_SignedIntegerType_8(self.address),
            "compliances": to_structure_VectorType_RecordType_core_ComplianceShortDescription(self.compliances),
        }

#
# UserGroupDetails
#

class UserGroupDetails(object):
    def __init__(self, user_group_id, user_group_name, form_category_id, form_ids, is_active):
        self.user_group_id = user_group_id
        self.user_group_name = user_group_name
        self.form_category_id = form_category_id
        self.form_ids = form_ids
        self.is_active = is_active

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["user_group_id", "user_group_name", "form_category_id", "form_ids", "is_active"])
        user_group_id = data.get("user_group_id")
        user_group_id = parse_structure_UnsignedIntegerType_32(user_group_id)
        user_group_name = data.get("user_group_name")
        user_group_name = parse_structure_CustomTextType_50(user_group_name)
        form_category_id = data.get("form_category_id")
        form_category_id = parse_structure_UnsignedIntegerType_32(form_category_id)
        form_ids = data.get("form_ids")
        form_ids = parse_structure_VectorType_SignedIntegerType_8(form_ids)
        is_active = data.get("is_active")
        is_active = parse_structure_Bool(is_active)
        return UserGroupDetails(user_group_id, user_group_name, form_category_id, form_ids, is_active)

    def to_structure(self):
        return {
            "user_group_id": to_structure_SignedIntegerType_8(self.user_group_id),
            "user_group_name": to_structure_CustomTextType_50(self.user_group_name),
            "form_category_id": to_structure_SignedIntegerType_8(self.form_category_id),
            "form_ids": to_structure_VectorType_SignedIntegerType_8(self.form_ids),
            "is_active": to_structure_Bool(self.is_active),
        }

#
# User
#

class User(object):
    def __init__(self, user_id, employee_name, is_active):
        self.user_id = user_id
        self.employee_name = employee_name
        self.is_active = is_active

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["user_id", "employee_name", "is_active"])
        user_id = data.get("user_id")
        user_id = parse_structure_UnsignedIntegerType_32(user_id)
        employee_name = data.get("employee_name")
        employee_name = parse_structure_CustomTextType_50(employee_name)
        is_active = data.get("is_active")
        is_active = parse_structure_Bool(is_active)
        return User(user_id, employee_name, is_active)

    def to_structure(self):
        return {
            "user_id": to_structure_SignedIntegerType_8(self.user_id),
            "employee_name": to_structure_CustomTextType_50(self.employee_name),
            "is_active": to_structure_Bool(self.is_active),
        }

#
# UserDetails
#

class UserDetails(object):
    def __init__(self, user_id, email_id, user_group_id, employee_name, employee_code, contact_no, address, designation, country_ids, domain_ids, is_active):
        self.user_id = user_id
        self.email_id = email_id
        self.user_group_id = user_group_id
        self.employee_name = employee_name
        self.employee_code = employee_code
        self.contact_no = contact_no
        self.address = address
        self.designation = designation
        self.country_ids = country_ids
        self.domain_ids = domain_ids
        self.is_active = is_active

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["user_id", "email_id", "user_group_id", "employee_name", "employee_code", "contact_no", "address", "designation", "country_ids", "domain_ids", "is_active"])
        user_id = data.get("user_id")
        user_id = parse_structure_UnsignedIntegerType_32(user_id)
        email_id = data.get("email_id")
        email_id = parse_structure_CustomTextType_100(email_id)
        user_group_id = data.get("user_group_id")
        user_group_id = parse_structure_UnsignedIntegerType_32(user_group_id)
        employee_name = data.get("employee_name")
        employee_name = parse_structure_CustomTextType_50(employee_name)
        employee_code = data.get("employee_code")
        employee_code = parse_structure_CustomTextType_50(employee_code)
        contact_no = data.get("contact_no")
        contact_no = parse_structure_CustomTextType_20(contact_no)
        address = data.get("address")
        address = parse_structure_CustomTextType_250(address)
        designation = data.get("designation")
        designation = parse_structure_CustomTextType_50(designation)
        country_ids = data.get("country_ids")
        country_ids = parse_structure_VectorType_SignedIntegerType_8(country_ids)
        domain_ids = data.get("domain_ids")
        domain_ids = parse_structure_VectorType_SignedIntegerType_8(domain_ids)
        is_active = data.get("is_active")
        is_active = parse_structure_Bool(is_active)
        return UserDetails(user_id, email_id, user_group_id, employee_name, employee_code, contact_no, address, designation, country_ids, domain_ids, is_active)

    def to_structure(self):
        return {
            "user_id": to_structure_SignedIntegerType_8(self.user_id),
            "email_id": to_structure_CustomTextType_100(self.email_id),
            "user_group_id": to_structure_SignedIntegerType_8(self.user_group_id),
            "employee_name": to_structure_CustomTextType_50(self.employee_name),
            "employee_code": to_structure_CustomTextType_50(self.employee_code),
            "contact_no": to_structure_CustomTextType_20(self.contact_no),
            "address": to_structure_CustomTextType_250(self.address),
            "designation": to_structure_CustomTextType_50(self.designation),
            "country_ids": to_structure_VectorType_SignedIntegerType_8(self.country_ids),
            "domain_ids": to_structure_VectorType_SignedIntegerType_8(self.domain_ids),
            "is_active": to_structure_Bool(self.is_active),
        }

#
# CountryWiseUnits
#

class CountryWiseUnits(object):
    def __init__(self, country_id, units):
        self.country_id = country_id
        self.units = units

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["country_id", "units"])
        country_id = data.get("country_id")
        country_id = parse_structure_UnsignedIntegerType_32(country_id)
        units = data.get("units")
        units = parse_structure_VectorType_RecordType_core_UnitDetails(units)
        return CountryWiseUnits(country_id, units)

    def to_structure(self):
        return {
            "country_id": to_structure_SignedIntegerType_8(self.country_id),
            "units": to_structure_VectorType_RecordType_core_UnitDetails(self.units),
        }

#
# ComplianceApplicability
#

class ComplianceApplicability(object):
    def __init__(self, compliance_id, compliance_name, description, statutory_provision, statutory_nature, compliance_applicable_status, compliance_opted_status, compliance_remarks):
        self.compliance_id = compliance_id
        self.compliance_name = compliance_name
        self.description = description
        self.statutory_provision = statutory_provision
        self.statutory_nature = statutory_nature
        self.compliance_applicable_status = compliance_applicable_status
        self.compliance_opted_status = compliance_opted_status
        self.compliance_remarks = compliance_remarks

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["compliance_id", "compliance_name", "description", "statutory_provision", "statutory_nature", "compliance_applicable_status", "compliance_opted_status", "compliance_remarks"])
        compliance_id = data.get("compliance_id")
        compliance_id = parse_structure_UnsignedIntegerType_32(compliance_id)
        compliance_name = data.get("compliance_name")
        compliance_name = parse_structure_CustomTextType_50(compliance_name)
        description = data.get("description")
        description = parse_structure_CustomTextType_500(description)
        statutory_provision = data.get("statutory_provision")
        statutory_provision = parse_structure_CustomTextType_500(statutory_provision)
        statutory_nature = data.get("statutory_nature")
        statutory_nature = parse_structure_CustomTextType_50(statutory_nature)
        compliance_applicable_status = data.get("compliance_applicable_status")
        compliance_applicable_status = parse_structure_Bool(compliance_applicable_status)
        compliance_opted_status = data.get("compliance_opted_status")
        compliance_opted_status = parse_structure_OptionalType_Bool(compliance_opted_status)
        compliance_remarks = data.get("compliance_remarks")
        compliance_remarks = parse_structure_OptionalType_CustomTextType_500(compliance_remarks)
        return ComplianceApplicability(compliance_id, compliance_name, description, statutory_provision, statutory_nature, compliance_applicable_status, compliance_opted_status, compliance_remarks)

    def to_structure(self):
        return {
            "compliance_id": to_structure_SignedIntegerType_8(self.compliance_id),
            "compliance_name": to_structure_CustomTextType_50(self.compliance_name),
            "description": to_structure_CustomTextType_500(self.description),
            "statutory_provision": to_structure_CustomTextType_500(self.statutory_provision),
            "statutory_nature": to_structure_CustomTextType_50(self.statutory_nature),
            "compliance_applicable_status": to_structure_Bool(self.compliance_applicable_status),
            "compliance_opted_status": to_structure_OptionalType_Bool(self.compliance_opted_status),
            "compliance_remarks": to_structure_OptionalType_CustomTextType_500(self.compliance_remarks),
        }

#
# ComplianceShortDescription
#

class ComplianceShortDescription(object):
    def __init__(self, compliance_name, description, assignee_name, compliance_status, ageing):
        self.compliance_name = compliance_name
        self.description = description
        self.assignee_name = assignee_name
        self.compliance_status = compliance_status
        self.ageing = ageing

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["compliance_name", "description", "assignee_name", "compliance_status", "ageing"])
        compliance_name = data.get("compliance_name")
        compliance_name = parse_structure_CustomTextType_50(compliance_name)
        description = data.get("description")
        description = parse_structure_CustomTextType_500(description)
        assignee_name = data.get("assignee_name")
        assignee_name = parse_structure_CustomTextType_50(assignee_name)
        compliance_status = data.get("compliance_status")
        compliance_status = parse_structure_EnumType_core_COMPLIANCE_STATUS(compliance_status)
        ageing = data.get("ageing")
        ageing = parse_structure_UnsignedIntegerType_32(ageing)
        return ComplianceShortDescription(compliance_name, description, assignee_name, compliance_status, ageing)

    def to_structure(self):
        return {
            "compliance_name": to_structure_CustomTextType_50(self.compliance_name),
            "description": to_structure_CustomTextType_500(self.description),
            "assignee_name": to_structure_CustomTextType_50(self.assignee_name),
            "compliance_status": to_structure_EnumType_core_COMPLIANCE_STATUS(self.compliance_status),
            "ageing": to_structure_SignedIntegerType_8(self.ageing),
        }

#
# StatutoryDate
#

class StatutoryDate(object):
    def __init__(self, statutory_date, statutory_month, trigger_before_days):
        self.statutory_date = statutory_date
        self.statutory_month = statutory_month
        self.trigger_before_days = trigger_before_days

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["statutory_date", "statutory_month", "trigger_before_days"])
        statutory_date = data.get("statutory_date")
        statutory_date = parse_structure_OptionalType_CustomIntegerType_1_31(statutory_date)
        statutory_month = data.get("statutory_month")
        statutory_month = parse_structure_OptionalType_CustomIntegerType_1_12(statutory_month)
        trigger_before_days = data.get("trigger_before_days")
        trigger_before_days = parse_structure_OptionalType_CustomIntegerType_1_100(trigger_before_days)
        return StatutoryDate(statutory_date, statutory_month, trigger_before_days)

    def to_structure(self):
        return {
            "statutory_date": to_structure_OptionalType_CustomIntegerType_1_31(self.statutory_date),
            "statutory_month": to_structure_OptionalType_CustomIntegerType_1_12(self.statutory_month),
            "trigger_before_days": to_structure_OptionalType_CustomIntegerType_1_100(self.trigger_before_days),
        }

#
# FormCategory
#

class FormCategory(object):
    def __init__(self, form_category_id, form_category):
        self.form_category_id = form_category_id
        self.form_category = form_category

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["form_category_id", "form_category"])
        form_category_id = data.get("form_category_id")
        form_category_id = parse_structure_UnsignedIntegerType_32(form_category_id)
        form_category = data.get("form_category")
        form_category = parse_structure_CustomTextType_50(form_category)
        return FormCategory(form_category_id, form_category)

    def to_structure(self):
        return {
            "form_category_id": to_structure_SignedIntegerType_8(self.form_category_id),
            "form_category": to_structure_CustomTextType_50(self.form_category),
        }

#
# FormType
#

class FormType(object):
    def __init__(self, form_type_id, form_type):
        self.form_type_id = form_type_id
        self.form_type = form_type

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["form_type_id", "form_type"])
        form_type_id = data.get("form_type_id")
        form_type_id = parse_structure_UnsignedIntegerType_32(form_type_id)
        form_type = data.get("form_type")
        form_type = parse_structure_CustomTextType_50(form_type)
        return FormType(form_type_id, form_type)

    def to_structure(self):
        return {
            "form_type_id": to_structure_SignedIntegerType_8(self.form_type_id),
            "form_type": to_structure_CustomTextType_50(self.form_type),
        }

#
# ComplianceFrequency
#

class ComplianceFrequency(object):
    def __init__(self, frequency_id, frequency):
        self.frequency_id = frequency_id
        self.frequency = frequency

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["frequency_id", "frequency"])
        frequency_id = data.get("frequency_id")
        frequency_id = parse_structure_UnsignedIntegerType_32(frequency_id)
        frequency = data.get("frequency")
        frequency = parse_structure_EnumType_core_COMPLIANCE_FREQUENCY(frequency)
        return ComplianceFrequency(frequency_id, frequency)

    def to_structure(self):
        return {
            "frequency_id": to_structure_SignedIntegerType_8(self.frequency_id),
            "frequency": to_structure_EnumType_core_COMPLIANCE_FREQUENCY(self.frequency),
        }

#
# ComplianceRepeatType
#

class ComplianceRepeatType(object):
    def __init__(self, repeat_type_id, repeat_type):
        self.repeat_type_id = repeat_type_id
        self.repeat_type = repeat_type

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["repeat_type_id", "repeat_type"])
        repeat_type_id = data.get("repeat_type_id")
        repeat_type_id = parse_structure_UnsignedIntegerType_32(repeat_type_id)
        repeat_type = data.get("repeat_type")
        repeat_type = parse_structure_EnumType_core_REPEATS_TYPE(repeat_type)
        return ComplianceRepeatType(repeat_type_id, repeat_type)

    def to_structure(self):
        return {
            "repeat_type_id": to_structure_SignedIntegerType_8(self.repeat_type_id),
            "repeat_type": to_structure_EnumType_core_REPEATS_TYPE(self.repeat_type),
        }

#
# ComplianceDurationType
#

class ComplianceDurationType(object):
    def __init__(self, duration_type_id, duration_type):
        self.duration_type_id = duration_type_id
        self.duration_type = duration_type

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["duration_type_id", "duration_type"])
        duration_type_id = data.get("duration_type_id")
        duration_type_id = parse_structure_UnsignedIntegerType_32(duration_type_id)
        duration_type = data.get("duration_type")
        duration_type = parse_structure_EnumType_core_DURATION_TYPE(duration_type)
        return ComplianceDurationType(duration_type_id, duration_type)

    def to_structure(self):
        return {
            "duration_type_id": to_structure_SignedIntegerType_8(self.duration_type_id),
            "duration_type": to_structure_EnumType_core_DURATION_TYPE(self.duration_type),
        }

#
# ComplianceApprovalStatus
#

class ComplianceApprovalStatus(object):
    def __init__(self, approval_status_id, approval_status):
        self.approval_status_id = approval_status_id
        self.approval_status = approval_status

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["approval_status_id", "approval_status"])
        approval_status_id = data.get("approval_status_id")
        approval_status_id = parse_structure_UnsignedIntegerType_32(approval_status_id)
        approval_status = data.get("approval_status")
        approval_status = parse_structure_EnumType_core_APPROVAL_STATUS(approval_status)
        return ComplianceApprovalStatus(approval_status_id, approval_status)

    def to_structure(self):
        return {
            "approval_status_id": to_structure_SignedIntegerType_8(self.approval_status_id),
            "approval_status": to_structure_EnumType_core_APPROVAL_STATUS(self.approval_status),
        }

