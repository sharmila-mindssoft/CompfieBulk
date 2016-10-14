from protocol.jsonvalidators import (
    parse_enum, parse_dictionary, to_structure_dictionary_values
)
from protocol.parse_structure import (
    parse_structure_VectorType_RecordType_core_Compliance,
    parse_structure_EnumType_core_DURATION_TYPE,
    parse_structure_UnsignedIntegerType_32, parse_structure_Bool,
    parse_structure_VectorType_RecordType_core_ComplianceShortDescription,
    parse_structure_EnumType_core_FILTER_TYPE,
    parse_structure_EnumType_core_REPEATS_TYPE,
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
    parse_structure_OptionalType_VectorType_RecordType_core_StatutoryDate,
    parse_structure_OptionalType_VectorType_RecordType_core_FileList,
    parse_structure_OptionalType_CustomIntegerType_1_100,
    parse_structure_OptionalType_CustomIntegerType_1_12,
    parse_structure_OptionalType_CustomIntegerType_1_31,
    parse_structure_Float,
    parse_structure_OptionalType_VectorType_RecordType_core_ComplianceApplicability,
    parse_structure_CustomTextType_500,
    parse_structure_OptionalType_CustomTextType_20,
    parse_structure_VectorType_CustomTextType_100,
    parse_structure_EnumType_core_NOT_COMPLIED_TYPE,
    parse_structure_VectorType_RecordType_core_Compliance_Download,
    parse_structure_CustomTextType_200,
    parse_structure_EnumType_core_COMPLIANCE_APPROVAL_STATUS,
    parse_structure_VectorType_UnsignedIntegerType_32,
    parse_structure_OptionalType_UnsignedIntegerType_32,
    parse_structure_SignedIntegerType_8,
    parse_structure_OptionalType_VectorType_CustomTextType_250,
    parse_structure_OptionalType_VectorType_UnsignedIntegerType_32,
    parse_structure_VectorType_CustomTextType_250,
    parse_structure_OptionalType_CustomTextType_250,
    parse_structure_OptionalType_VectorType_CustomTextType_500,
    parse_structure_VectorType_RecordType_core_LegalEntityDetails,
    parse_structure_VectorType_RecordType_core_EntityDomainDetails,
    parse_structure_MapType_CustomTextType_50_VectorType_UnsignedIntegerType_32,
    parse_structure_OptionalType_RecordType_core_ClientBusinessGroup,
    parse_structure_RecordType_core_FileList,
    parse_structure_OptionalType_RecordType_core_FileList,
    parse_structure_VectorType_RecordType_core_ClientConfiguration

)
from protocol.to_structure import (
    to_structure_VectorType_RecordType_core_Compliance,
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
    to_structure_EnumType_core_COMPLIANCE_APPROVAL_STATUS,
    to_structure_OptionalType_CustomTextType_20,
    to_structure_VectorType_CustomTextType_100,
    to_structure_EnumType_core_NOT_COMPLIED_TYPE,
    to_structure_OptionalType_Text,
    to_structure_VectorType_RecordType_core_Compliance_Download,
    to_structure_CustomTextType_200,
    to_structure_EnumType_core_COMPLIANCE_APPROVAL_STATUS,
    to_structure_VectorType_UnignedIntegerType_32,
    to_structure_OptionalType_UnsignedIntegerType_32,
    to_structure_OptionalType_CustomTextType_500,
    to_structure_CustomTextType_100,
    to_structure_OptionalType_VectorType_CustomTextType_250,
    to_structure_OptionalType_VectorType_UnsignedIntegerType_32,
    to_structure_VectorType_CustomTextType_250,
    to_structure_OptionalType_CustomTextType_250,
    to_structure_OptionalType_VectorType_CustomTextType_500,
    to_structure_VectorType_RecordType_core_LegalEntityDetails,
    to_structure_VectorType_RecordType_core_EntityDomainDetails,
    to_structure_MapType_CustomTextType_50_VectorType_UnsignedIntegerType_32,
    to_structure_OptionalType_RecordType_core_ClientBusinessGroup,
    to_structure_RecordType_core_FileList,
    to_structure_OptionalType_RecordType_core_FileList
)

#
# SESSION_TYPE
#

class SESSION_TYPE(object):
    # Web = "Web"
    # Android = "Android"
    # IOS = "IOS"
    # BlackBerry = "BlackBerry"

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
    # Inhouse = "Inhouse"
    # ServiceProvider = "ServiceProvider"

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
    # Pending = "Pending"
    # Approve = "Approved"
    # Reject = "Rejected"
    # ApproveAndNotify = "Approved & Notified"

    def __init__(self, value):
        self._value = value

    @staticmethod
    def values():
        return ["Pending", "Approved", "Rejected", "Approved & Notified"]

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
    # Concur = "Concur"
    # RejectConcurrence = "Reject Concurrence"
    # Approve = "Approve"
    # RejectApproval = "Reject Approval"

    def __init__(self, value):
        self._value = value

    @staticmethod
    def values():
        return ["Concur", "Reject Concurrence", "Approve", "Reject Approval"]

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
    # Submited = "Submited"
    # Pending = "Pending"

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
    # Submit = "Submit"
    # Save = "Save"

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
    # Notification = "Notification"
    # Reminder = "Reminder"
    # Escalation = "Escalation"

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
    # Group = "Group"
    # BusinessGroup = "BusinessGroup"
    # LegalEntity = "LegalEntity"
    # Division = "Division"
    # Unit = "Unit"
    # Consolidated = "Consolidated"

    def __init__(self, value):
        self._value = value

    @staticmethod
    def values():
        return ["Group", "BusinessGroup", "LegalEntity", "Division", "Unit", "Consolidated"]

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
    # OneTime = "One Time"
    # Periodical = "Periodical"
    # Review = "Review"
    # OnOccurrence = "On Occurrence"

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
    # Complied = "Complied"
    # DelayedCompliance = "Delayed Compliance"
    # Inprogress = "Inprogress"
    # NotComplied = "Not Complied"

    def __init__(self, value):
        self._value = value

    @staticmethod
    def values():
        return ["Complied", "Delayed Compliance", "Inprogress", "Not Complied"]

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
    # Applicable = "Applicable"
    # NotApplicable = "Not Applicable"
    # NotOpted = "Not Opted"

    def __init__(self, value):
        self._value = value

    @staticmethod
    def values():
        return ["Applicable", "Not Applicable", "Not Opted"]

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
    # IT = "IT"
    # Knowledge = "Knowledge"
    # Techno = "Techno"
    # Client = "Client"
    # ServiceProvider = "ServiceProvider"

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
    # Year = "Year(s)"
    # Month = "Month(s)"
    # Day = "Day(s)"

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
    # Day = "Day(s)"
    # Hour = "Hour(s)"

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
    # Submitted = "Submitted"
    # Approved = "Approved"
    # Rejected = "Rejected"
    # Concurred = "Concurred"

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

#
# NOT_COMPLIED_TYPE
#

class NOT_COMPLIED_TYPE(object) :
    # below_30 = "Below 30"
    # below_60 = "Below 60"
    # below_90 = "Below 90"
    # above_90 = "Above 90"

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
        form_name = data.get("form_name")
        form_url = data.get("form_url")
        parent_menu = data.get("parent_menu")
        form_type = data.get("form_type")
        return Form(form_id, form_name, form_url, parent_menu, form_type)

    def to_structure(self):
        data = {
            "form_id": self.form_id,
            "form_name": self.form_name,
            "form_url": self.form_url,
            "parent_menu": self.parent_menu,
            "form_type": self.form_type
        }
        return to_structure_dictionary_values(data)

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
        return Menu(menus)

    def to_structure(self):
        return {
            "menus": self.menus,
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
        user_group_name = data.get("user_group_name")
        is_active = data.get("is_active")
        return UserGroup(user_group_id, user_group_name, is_active)

    def to_structure(self):
        data = {
            "user_group_id": self.user_group_id,
            "user_group_name": self.user_group_name,
            "is_active": self.is_active,
        }
        return data


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
        data = parse_dictionary(
            data, ["country_id", "country_name", "is_active"])
        country_id = data.get("country_id")
        country_name = data.get("country_name")
        is_active = data.get("is_active")
        return Country(country_id, country_name, is_active)

    def to_structure(self):
        data = {
            "country_id": self.country_id,
            "country_name": self.country_name,
            "is_active": self.is_active,
        }
        return data

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
        domain_name = data.get("domain_name")
        is_active = data.get("is_active")
        return Domain(domain_id, domain_name, is_active)

    def to_structure(self):
        data = {
            "domain_id": self.domain_id,
            "domain_name": self.domain_name,
            "is_active": self.is_active,
        }
        return data

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
        data = parse_dictionary(data, ["l_id", "l_position", "l_name"])
        level_id = data.get("l_id")
        level_position = data.get("l_position")
        level_name = data.get("l_name")
        return Level(level_id, level_position, level_name)

    def to_structure(self):
        data = {
            "l_id": self.level_id,
            "l_position": self.level_position,
            "l_name": self.level_name,
        }
        return data

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
        level_position = data.get("level_position")
        level_name = data.get("level_name")
        return GeographyLevel(level_id, level_position, level_name)

    def to_structure(self):
        data = {
            "level_id": self.level_id,
            "level_position": self.level_position,
            "level_name": self.level_name,
        }
        return data

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
        geography_name = data.get("geography_name")
        level_id = data.get("level_id")
        parent_ids = data.get("parent_ids")
        parent_id = data.get("parent_id")
        is_active = data.get("is_active")
        return Geography(geography_id, geography_name, level_id, parent_ids, parent_id, is_active)

    def to_structure(self):
        data = {
            "geography_id": self.geography_id,
            "geography_name": self.geography_name,
            "level_id": self.level_id,
            "parent_ids": self.parent_ids,
            "parent_id": self.parent_id,
            "is_active": self.is_active,
        }
        return data

#
# Geography With Mapping
#

class GeographyWithMapping(object):
    def __init__(self, geography_id, geography_name, level_id, mapping, parent_ids, is_active):
        self.geography_id = geography_id
        self.geography_name = geography_name
        self.level_id = level_id
        self.mapping = mapping
        self.parent_ids = parent_ids
        self.is_active = is_active

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["geography_id", "geography_name", "level_id", "mapping", "parent_ids", "is_active"])
        geography_id = data.get("geography_id")
        geography_name = data.get("geography_name")
        level_id = data.get("level_id")
        mapping = data.get("mapping")
        parent_ids = data.get("parent_ids")
        is_active = data.get("is_active")
        return Geography(
            geography_id, geography_name, level_id,
            mapping, parent_id, is_active
        )

    def to_structure(self):
        data = {
            "geography_id": self.geography_id,
            "geography_name": self.geography_name,
            "level_id": self.level_id,
            "mapping": self.mapping,
            "parent_ids": self.parent_ids,
            "is_active": self.is_active,
        }
        return to_dictionary_values(data)

#
# Geography With Mapping & country for unit
#


class UnitGeographyMapping(object):
    def __init__(self, geography_id, geography_name, level_id, mapping, parent_ids, country_id, is_active):
        self.geography_id = geography_id
        self.geography_name = geography_name
        self.level_id = level_id
        self.mapping = mapping
        self.parent_ids = parent_ids
        self.country_id = country_id
        self.is_active = is_active

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["geography_id", "geography_name", "level_id", "mapping", "parent_ids", "country_id", "is_active"])
        geography_id = data.get("geography_id")
        geography_name = data.get("geography_name")
        level_id = data.get("level_id")
        mapping = data.get("mapping")
        parent_ids = data.get("parent_ids")
        country_id = data.get("country_id")
        is_active = data.get("is_active")
        return UnitGeographyMapping(geography_id, geography_name, level_id, mapping, parent_ids, country_id, is_active)

    def to_structure(self):
        data = {
            "geography_id": self.geography_id,
            "geography_name": self.geography_name,
            "level_id": self.level_id,
            "mapping": self.mapping,
            "parent_ids": self.parent_ids,
            "country_id": self.country_id,
            "is_active": self.is_active,
        }
        return to_dictionary_values(data)

#
# Geography level & country for unit
#

class UnitGeographyLevel(object):
    def __init__(self, level_id, level_position, level_name, country_id):
        self.level_id = level_id
        self.level_position = level_position
        self.level_name = level_name
        self.country_id = country_id

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["l_id", "l_position", "l_name", "c_id"])
        level_id = data.get("l_id")
        level_position = data.get("l_position")
        level_name = data.get("l_name")
        country_id = data.get("c_id")
        return UnitGeographyLevel(level_id, level_position, level_name, country_id)

    def to_structure(self):
        data = {
            "l_id": self.level_id,
            "l_position": self.level_position,
            "l_name": self.level_name,
            "c_id": self.country_id,
        }
        return data


#
# Industry
#
class Industry(object):
    def __init__(
        self, country_id, country_name, domain_id, domain_name, industry_id,
        industry_name, is_active
    ):
        self.country_id = country_id
        self.country_name = country_name
        self.domain_id = domain_id
        self.domain_name = domain_name
        self.industry_id = industry_id
        self.industry_name = industry_name
        self.is_active = is_active

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(
            data, [
                "country_id", "country_name", "domain_id", "domain_name",
                "industry_id", "industry_name", "is_active"
            ]
        )
        country_id = data.get("country_id")
        country_name = data.get("country_name")
        domain_id = data.get("domain_id")
        domain_name = data.get("domain_name")
        industry_id = data.get("industry_id")
        industry_name = data.get("industry_name")
        is_active = data.get("is_active")
        return Industry(
            country_id, country_name, domain_id, domain_name, industry_id,
            industry_name, is_active
        )

    def to_structure(self):
        data = {
            "country_id": self.country_id,
            "country_name": self.country_name,
            "domain_id": self.domain_id,
            "domain_name": self.domain_name,
            "industry_id": self.industry_id,
            "industry_name": self.industry_name,
            "is_active": self.is_active
        }
        return data


class Industries(object):
    def __init__(self, industry_id, industry_name, is_active):
        self.industry_id = industry_id
        self.industry_name = industry_name
        self.is_active = is_active

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(
            data, ["industry_id", "industry_name", "is_active"])
        industry_id = data.get("industry_id")
        industry_name = data.get("industry_name")
        is_active = data.get("is_active")

        return Industries(industry_id, industry_name, is_active)

    def to_structure(self):
        data = {
            "industry_id": self.industry_id,
            "industry_name": self.industry_name,
            "is_active": self.is_active,
        }
        return data


class UnitIndustries(object):
    def __init__(self, industry_id, industry_name, country_id, domain_id, client_id, unit_count, legal_entity_id, is_active):
        self.industry_id = industry_id
        self.industry_name = industry_name
        self.country_id = country_id
        self.domain_id = domain_id
        self.client_id = client_id
        self.unit_count = unit_count
        self.legal_entity_id = legal_entity_id
        self.is_active = is_active

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(
            data, ["industry_id", "industry_name", "country_id", "domain_id", "client_id", "unit_count", "legal_entity_id", "is_active"])
        industry_id = data.get("industry_id")
        industry_name = data.get("industry_name")
        country_id = data.get("country_id")
        domain_id = data.get("domain_id")
        client_id = data.get("client_id")
        unit_count = data.get("unit_count")
        legal_entity_id = data.get("legal_entity_id")
        is_active = data.get("is_active")

        return UnitIndustries(industry_id, industry_name, country_id, domain_id, client_id, unit_count, legal_entity_id, is_active)

    def to_structure(self):
        data = {
            "industry_id": self.industry_id,
            "industry_name": self.industry_name,
            "country_id": self.country_id,
            "domain_id": self.domain_id,
            "client_id": self.client_id,
            "unit_count": self.unit_count,
            "legal_entity_id": self.legal_entity_id,
            "is_active": self.is_active,
        }
        return data


#
# StatutoryNature
#


class StatutoryNature(object):
    def __init__(self, statutory_nature_id, statutory_nature_name, country_id, country_name, is_active):
        self.statutory_nature_id = statutory_nature_id
        self.statutory_nature_name = statutory_nature_name
        self.country_id = country_id
        self.country_name = country_name
        self.is_active = is_active

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(
            data, [
                "statutory_nature_id", "statutory_nature_name", "is_active"
                ]
            )
        statutory_nature_id = data.get("statutory_nature_id")
        statutory_nature_name = data.get("statutory_nature_name")
        country_id = data.get("country_id")
        country_name = data.get("country_name")
        is_active = data.get("is_active")

        return StatutoryNature(statutory_nature_id, statutory_nature_name, country_id, country_name, is_active)

    def to_structure(self):
        data = {
            "statutory_nature_id": self.statutory_nature_id,
            "statutory_nature_name": self.statutory_nature_name,
            "country_id": self.country_id,
            "country_name": self.country_name,
            "is_active": self.is_active,
        }
        return data

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
        level_position = data.get("level_position")
        level_name = data.get("level_name")
        return StatutoryLevel(level_id, level_position, level_name)

    def to_structure(self):
        return {
            "level_id": self.level_id,
            "level_position": self.level_position,
            "level_name": self.level_name,
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
        level_1_statutory_name = data.get("level_1_statutory_name")
        return Statutory(level_1_statutory_id, level_1_statutory_name)

    def to_structure(self):
        return {
            "level_1_statutory_id": self.level_1_statutory_id,
            "level_1_statutory_name": self.level_1_statutory_name
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
        statutory_name = data.get("statutory_name")
        level_id = data.get("level_id")
        parent_ids = data.get("parent_ids")
        parent_id = data.get("parent_id")
        parent_mappings = data.get("parent_mappings")
        return Statutory(statutory_id, statutory_name, level_id, parent_ids, parent_id, parent_mappings)

    def to_structure(self):
        return {
            "statutory_id": self.statutory_id,
            "statutory_name": self.statutory_name,
            "level_id": self.level_id,
            "parent_ids": self.parent_ids,
            "parent_id": self.parent_id,
            "parent_mappings": self.parent_mappings,
        }

#
# FileList
#

class FileList(object):
    def __init__(self, file_size, file_name, file_content):
        self.file_size = file_size
        self.file_name = file_name
        self.file_content = file_content

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["file_size", "file_name", "file_content"])
        file_size = data.get("file_size")
        file_name = data.get("file_name")
        file_content = data.get("file_content")
        return FileList(file_size, file_name, file_content)

    def to_structure(self):
        return {
            "file_size": self.file_size,
            "file_name": self.file_name,
            "file_content": self.file_content
        }

#
# Compliance
#

class Compliance_Download(object):
    def __init__(self, compliance_name, url):
        self.compliance_name = compliance_name
        self.url = url

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["compliance_name", 'url'])
        compliance_name = data.get("compliance_name")
        url = data.get("url")
        return Compliance_Download(compliance_name, url)

    def to_structure(self):
        return {
            "compliance_name": self.compliance_name,
            "url": self.url
        }

class Compliance(object):
    def __init__(
        self, compliance_id, statutory_provision,
        compliance_task, description, document_name,
        format_file_list, penal_consequences,
        frequency_id, statutory_dates, repeats_type_id,
        repeats_every, duration_type_id,
        duration, is_active,
        frequency, summary
    ):
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
        self.frequency = frequency
        self.summary = summary

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "comp_id", "s_provision",
            "c_task", "description",
            "doc_name", "f_f_list",
            "p_consequences", "f_id",
            "statu_dates", "r_type_id",
            "r_every", "d_type_id",
            "duration", "is_active",
            "frequency", "summary"
        ])
        compliance_id = data.get("comp_id")
        statutory_provision = data.get("s_provision")
        compliance_task = data.get("c_task")
        description = data.get("description")
        document_name = data.get("doc_name")
        format_file_list = data.get("f_f_list")
        penal_consequences = data.get("p_consequences")
        frequency_id = data.get("f_id")
        statutory_dates = data.get("statu_dates")
        repeats_type_id = data.get("r_type_id")
        repeats_every = data.get("r_every")
        duration_type_id = data.get("d_type_id")
        duration = data.get("duration")
        is_active = data.get("is_active")
        frequency = data.get("frequency")
        summary = data.get("summary")
        return Compliance(
            compliance_id, statutory_provision,
            compliance_task, description,
            document_name, format_file_list,
            penal_consequences, frequency_id,
            statutory_dates, repeats_type_id,
            repeats_every, duration_type_id,
            duration, is_active,
            frequency, summary
        )

    def to_structure(self):
        return {
            "comp_id": self.compliance_id,
            "s_provision": self.statutory_provision,
            "c_task": self.compliance_task,
            "description": self.description,
            "doc_name": self.document_name,
            "f_f_list": self.format_file_list,
            "p_consequences": self.penal_consequences,
            "f_id": self.frequency_id,
            "statu_dates": self.statutory_dates,
            "r_type_id": self.repeats_type_id,
            "r_every": self.repeats_every,
            "d_type_id": self.duration_type_id,
            "duration": self.duration,
            "is_active": self.is_active,
            "frequency": self.frequency,
            "summary": self.summary
        }

#
# StatutoryMapping
#

class StatutoryMapping(object):
    def __init__(
        self, country_id, country_name, domain_id,
        domain_name, industry_ids, industry_names,
        statutory_nature_id, statutory_nature_name,
        statutory_ids, statutory_mappings, compliances,
        compliance_names, geography_ids, geography_mappings,
        approval_status, is_active, approval_status_text
    ):
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
        self.approval_status_text = approval_status_text

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "country_id", "country_name", "domain_id",
            "domain_name", "industry_ids", "industry_names",
            "statutory_nature_id", "statutory_nature_name",
            "statutory_ids", "statutory_mappings",
            "compliances", "compliance_names", "geography_ids",
            "geography_mappings", "approval_status", "is_active",
            "approval_status_text"
        ])
        country_id = data.get("country_id")
        country_name = data.get("country_name")
        domain_id = data.get("domain_id")
        domain_name = data.get("domain_name")
        industry_ids = data.get("industry_ids")
        industry_names = data.get("industry_names")
        statutory_nature_id = data.get("statutory_nature_id")
        statutory_nature_name = data.get("statutory_nature_name")
        statutory_ids = data.get("statutory_ids")
        statutory_mappings = data.get("statutory_mappings")
        compliances = data.get("compliances")
        compliance_names = data.get("compliance_names")
        geography_ids = data.get("geography_ids")
        geography_mappings = data.get("geography_mappings")
        approval_status = data.get("approval_status")
        is_active = data.get("is_active")
        is_active = parse_structure_Bool(is_active)
        approval_status_text = data.get("approval_status_text")
        return StatutoryMapping(
            country_id, country_name, domain_id, domain_name,
            industry_ids, industry_names, statutory_nature_id,
            statutory_nature_name, statutory_ids, statutory_mappings,
            compliances, compliance_names, geography_ids,
            geography_mappings, approval_status, is_active, approval_status_text
        )

    def to_structure(self):
        return {
            "country_id": self.country_id,
            "country_name": self.country_name,
            "domain_id": self.domain_id,
            "domain_name": self.domain_name,
            "industry_ids": self.industry_ids,
            "industry_names": self.industry_names,
            "statutory_nature_id": self.statutory_nature_id,
            "statutory_nature_name": self.statutory_nature_name,
            "statutory_ids": self.statutory_ids,
            "statutory_mappings": self.statutory_mappings,
            "compliances": self.compliances,
            "compliance_names": self.compliance_names,
            "geography_ids": self.geography_ids,
            "geography_mappings": self.geography_mappings,
            "approval_status": self.approval_status,
            "is_active": self.is_active,
            "approval_status_text": self.approval_status_text
        }

#
# GroupCompanyForUnitCreation
#

class GroupCompanyForUnitCreation(object):
    def __init__(self, client_id, group_name, country_ids, domain_ids, next_unit_code):
        self.client_id = client_id
        self.group_name = group_name
        self.country_ids = country_ids
        self.domain_ids = domain_ids
        self.next_unit_code = next_unit_code

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "client_id", "group_name",
            "country_ids", "domain_ids", "next_unit_code"
        ])
        client_id = data.get("client_id")
        group_name = data.get("group_name")
        domain_ids = data.get("domain_ids")
        country_ids = data.get("country_ids")
        next_unit_code = data.get("next_unit_code")
        return GroupCompanyForUnitCreation(
            client_id, group_name, country_ids, domain_ids, next_unit_code
        )

    def to_structure(self):
        data = {
            "client_id": self.client_id,
            "group_name": self.group_name,
            "country_ids": self.country_ids,
            "domain_ids": self.domain_ids,
            "next_unit_code": self.next_unit_code
        }
        return data

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
        data = parse_dictionary(data, [
            "client_id", "group_name", "is_active",
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
        data = {
            "client_id": to_structure_UnsignedIntegerType_32(self.client_id),
            "group_name": to_structure_CustomTextType_50(self.group_name),
            "is_active": to_structure_Bool(self.is_active),
            "country_ids": to_structure_VectorType_UnsignedIntegerType_32(self.country_ids),
            "domain_ids": to_structure_VectorType_UnsignedIntegerType_32(self.domain_ids),
        }
        return data

#
# GroupCompanyDetail
#

class GroupCompanyDetail(object):
    def __init__(
        self, client_id, client_name, domain_ids, country_ids,
        incharge_persons, file_name, logo, contract_from, contract_to, no_of_user_licence,
        total_disk_space, is_sms_subscribed, username, is_active, short_name,
        date_configurations
    ):
        self.client_id = client_id
        self.client_name = client_name
        self.domain_ids = domain_ids
        self.country_ids = country_ids
        self.incharge_persons = incharge_persons
        self.file_name = file_name
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
        data = parse_dictionary(data, [
            "client_id", "client_name", "domain_ids",
            "country_ids", "incharge_persons", "file_name", "logo", "contract_from", "contract_to",
            "no_of_user_licence", "total_disk_space", "is_sms_subscribed", "username",
            "is_active", "short_name"
        ])
        client_id = data.get("client_id")
        client_id = parse_structure_UnsignedIntegerType_32(client_id)
        client_name = data.get("client_name")
        client_name = parse_structure_CustomTextType_50(client_name)
        domain_ids = data.get("domain_ids")
        country_ids = data.get("country_ids")
        country_ids = parse_structure_OptionalType_VectorType_UnsignedIntegerType_32(country_ids)
        incharge_persons = data.get("incharge_persons")
        incharge_persons = parse_structure_VectorType_SignedIntegerType_8(incharge_persons)
        file_name = data.get("file_name")
        file_name = parse_structure_CustomTextType_250(file_name)
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
        return GroupCompanyDetail(
            client_id, client_name, domain_ids,
            country_ids, incharge_persons, file_name, logo, contract_from, contract_to,
            no_of_user_licence, total_disk_space, is_sms_subscribed,
            username, is_active, short_name, date_configurations
        )

    def to_structure(self):
        return {
            "client_id": to_structure_UnsignedIntegerType_32(self.client_id),
            "client_name": to_structure_CustomTextType_50(self.client_name),
            "domain_ids": to_structure_OptionalType_VectorType_UnsignedIntegerType_32(self.domain_ids),
            "country_ids": to_structure_OptionalType_VectorType_UnsignedIntegerType_32(self.country_ids),
            "incharge_persons": to_structure_VectorType_UnsignedIntegerType_32(self.incharge_persons),
            "file_name": to_structure_CustomTextType_250(self.file_name),
            "logo": to_structure_CustomTextType_250(self.logo),
            "contract_from": to_structure_CustomTextType_20(self.contract_from),
            "contract_to": to_structure_CustomTextType_20(self.contract_to),
            "no_of_user_licence": to_structure_UnsignedIntegerType_32(self.no_of_user_licence),
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
        data = parse_dictionary(
            data, [
                "country_id", "domain_id", "period_from", "period_to"
            ]
        )
        country_id = data.get("country_id")
        country_id = parse_structure_UnsignedIntegerType_32(country_id)
        domain_id = data.get("domain_id")
        domain_id = parse_structure_UnsignedIntegerType_32(domain_id)
        period_from = data.get("period_from")
        period_from = parse_structure_UnsignedIntegerType_32(period_from)
        period_to = data.get("period_to")
        period_to = parse_structure_UnsignedIntegerType_32(period_to)
        return ClientConfiguration(
            country_id, domain_id, period_from, period_to
        )

    def to_structure(self):
        return {
            "country_id": to_structure_UnsignedIntegerType_32(self.country_id),
            "domain_id": to_structure_UnsignedIntegerType_32(self.domain_id),
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
        business_group_name = data.get("business_group_name")
        client_id = data.get("client_id")
        return BusinessGroup(business_group_id, business_group_name, client_id)

    def to_structure(self):
        data = {
            "business_group_id": self.business_group_id,
            "business_group_name": self.business_group_name,
            "client_id": self.client_id,
        }
        return data

class ClientBusinessGroup(object):
    def __init__(self, business_group_id, business_group_name):
        self.business_group_id = business_group_id
        self.business_group_name = business_group_name

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(
            data, ["business_group_id", "business_group_name"])
        business_group_id = data.get("business_group_id")
        business_group_name = data.get("business_group_name")
        return ClientBusinessGroup(business_group_id, business_group_name)

    def to_structure(self):
        return {
            "business_group_id": self.business_group_id,
            "business_group_name": self.business_group_name,
        }


class ClientLegalEntity(object):
    def __init__(self, legal_entity_id, legal_entity_name, business_group_id):
        self.legal_entity_id = legal_entity_id
        self.legal_entity_name = legal_entity_name
        self.business_group_id = business_group_id

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(
            data, [
                "legal_entity_id", "legal_entity_name", "business_group_id"])
        legal_entity_id = data.get("legal_entity_id")
        legal_entity_name = data.get("legal_entity_name")
        business_group_id = data.get("business_group_id")
        return ClientLegalEntity(
            legal_entity_id, legal_entity_name, business_group_id)

    def to_structure(self):
        return {
            "legal_entity_id": self.legal_entity_id,
            "legal_entity_name": self.legal_entity_name,
            "business_group_id": self.business_group_id
        }

#
# Division
#

class Division(object):
    def __init__(
        self, division_id, division_name, legal_entity_id,
        business_group_id, client_id
    ):
        self.division_id = division_id
        self.division_name = division_name
        self.legal_entity_id = legal_entity_id
        self.business_group_id = business_group_id
        self.client_id = client_id

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(
            data, [
                "division_id", "division_name", "legal_entity_id",
                "business_group_id", "client_id"])
        division_id = data.get("division_id")
        division_name = data.get("division_name")
        legal_entity_id = data.get("legal_entity_id")
        business_group_id = data.get("business_group_id")
        client_id = data.get("client_id")
        return Division(division_id, division_name, legal_entity_id, business_group_id, client_id)

    def to_structure(self):
        data = {
            "division_id": self.division_id,
            "division_name": self.division_name,
            "legal_entity_id": self.legal_entity_id,
            "business_group_id": self.business_group_id,
            "client_id": self.client_id,
        }
        return data



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
        data = parse_dictionary(
            data, [
                "division_id", "division_name",
                "legal_entity_id", "business_group_id"]
        )
        division_id = data.get("division_id")
        division_name = data.get("division_name")
        legal_entity_id = data.get("legal_entity_id")
        business_group_id = data.get("business_group_id")
        return Division(
            division_id, division_name, legal_entity_id, business_group_id
        )

    def to_structure(self):
        return {
            "division_id": self.division_id,
            "division_name": self.division_name,
            "legal_entity_id": self.legal_entity_id,
            "business_group_id": self.business_group_id,
        }


#
# Unit
#
class Unit(object):
    def __init__(
        self, unit_id, client_id, business_group_id, legal_entity_id, country_id,
        division_id, category_name, geography_id, unit_code, unit_name, unit_address,
        postal_code, domain_ids, i_ids, is_active, approve_status
    ):
        self.unit_id = unit_id
        self.client_id = client_id
        self.business_group_id = business_group_id
        self.legal_entity_id = legal_entity_id
        self.country_id = country_id
        self.division_id = division_id
        self.category_name = category_name
        self.geography_id = geography_id
        self.unit_code = unit_code
        self.unit_name = unit_name
        self.unit_address = unit_address
        self.postal_code = postal_code
        self.domain_ids = domain_ids
        self.i_ids = i_ids
        self.is_active = is_active
        self.approve_status = approve_status

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
                "unit_id", "client_id", "business_group_id", "legal_entity_id", "country_id", "division_id", "category_name",
                "geography_id", "unit_code", "unit_name", "unit_address",
                "postal_code", "domain_ids", "i_ids", "is_active", "approve_status"])
        unit_id = data.get("unit_id")
        client_id = data.get("client_id")
        business_group_id = data.get("business_group_id")
        legal_entity_id = data.get("legal_entity_id")
        country_id = data.get("country_id")
        division_id = data.get("division_id")
        category_name = data.get("category_name")
        geography_id = data.get("geography_id")
        unit_code = data.get("unit_code")
        unit_name = data.get("unit_name")
        unit_address = data.get("unit_address")
        postal_code = data.get("postal_code")
        domain_ids = data.get("domain_ids")
        i_ids = data.get("i_ids")
        is_active = data.get("is_active")
        approve_status = data.get("approve_status")
        return Unit(
            unit_id, client_id, business_group_id, legal_entity_id, country_id, division_id, category_name,
            geography_id, unit_code, unit_name, unit_address, postal_code, domain_ids, i_ids, is_active, approve_status
        )

    def to_structure(self):
        data = {
            "unit_id": self.unit_id,
            "client_id": self.client_id,
            "business_group_id": self.business_group_id,
            "legal_entity_id": self.legal_entity_id,
            "country_id": self.country_id,
            "division_id": self.division_id,
            "category_name": self.category_name,
            "geography_id": self.geography_id,
            "unit_code": self.unit_code,
            "unit_name": self.unit_name,
            "unit_address": self.unit_address,
            "postal_code": self.postal_code,
            "domain_ids": self.domain_ids,
            "i_ids": self.i_ids,
            "is_active": self.is_active,
            "approve_status": self.approve_status,
        }
        return data

class ClientUnit(object):
    def __init__(
        self, unit_id, division_id, legal_entity_id, business_group_id,
        unit_code, unit_name, unit_address, is_active, domain_ids, country_id,
        is_closed
    ):
        self.unit_id = unit_id
        self.division_id = division_id
        self.legal_entity_id = legal_entity_id
        self.business_group_id = business_group_id
        self.unit_code = unit_code
        self.unit_name = unit_name
        self.unit_address = unit_address
        self.is_active = is_active
        self.domain_ids = domain_ids
        self.country_id = country_id
        self.is_closed = is_closed

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(
            data, [
                "unit_id", "division_id", "legal_entity_id",
                "business_group_id", "unit_code", "unit_name", "unit_address",
                "is_active", "domain_ids", "country_id", "is_closed"
            ]
        )
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
        domain_ids = data.get("domain_ids")
        domain_ids = parse_structure_VectorType_UnsignedIntegerType_32(domain_ids)
        country_id = data.get("country_id")
        country_id = parse_structure_VectorType_UnsignedIntegerType_32(country_id)
        is_closed = data.get("is_closed")
        is_closed = parse_structure_Bool(is_closed)
        return Unit(
            unit_id, division_id, legal_entity_id, business_group_id,
            unit_code, unit_name, unit_address, is_active, domain_ids,
            country_id, is_closed
        )

    def to_structure(self):
        return {
            "unit_id": to_structure_OptionalType_SignedIntegerType_8(self.unit_id),
            "division_id": to_structure_OptionalType_SignedIntegerType_8(self.division_id),
            "legal_entity_id": to_structure_UnsignedIntegerType_32(self.legal_entity_id),
            "business_group_id": to_structure_OptionalType_SignedIntegerType_8(self.business_group_id),
            "unit_code": to_structure_CustomTextType_20(self.unit_code),
            "unit_name": to_structure_CustomTextType_100(self.unit_name),
            "unit_address": to_structure_CustomTextType_250(self.unit_address),
            "is_active": to_structure_Bool(self.is_active),
            "domain_ids": to_structure_VectorType_UnsignedIntegerType_32(self.domain_ids),
            "country_id": to_structure_UnsignedIntegerType_32(self.country_id),
            "is_closed" : to_structure_Bool(self.is_closed)
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
            "legal_entity_id": to_structure_UnsignedIntegerType_32(self.legal_entity_id),
            "business_group_id": to_structure_OptionalType_SignedIntegerType_8(self.business_group_id),
            "client_id": to_structure_UnsignedIntegerType_32(self.client_id),
            "country_id": to_structure_UnsignedIntegerType_32(self.country_id),
            "geography_id": to_structure_UnsignedIntegerType_32(self.geography_id),
            "unit_code": to_structure_CustomTextType_20(self.unit_code),
            "unit_name": to_structure_CustomTextType_250(self.unit_name),
            "industry_id": to_structure_UnsignedIntegerType_32(self.industry_id),
            "unit_address": to_structure_CustomTextType_250(self.unit_address),
            "postal_code": to_structure_UnsignedIntegerType_32(self.postal_code),
            "domain_ids": to_structure_VectorType_TexttorType_SignedIntegerType_8(self.domain_ids),
            "is_active": to_structure_Bool(self.is_active),
        }


#
#   Units - legal Entity details
#

class UnitLegalEntity(object):
    def __init__(
        self, legal_entity_id, legal_entity_name, business_group_id, client_id
        ):
        self.legal_entity_id = legal_entity_id
        self.legal_entity_name = legal_entity_name
        self.business_group_id = business_group_id
        self.client_id = client_id

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(
            data, [
            "legal_entity_id", "legal_entity_name", "business_group_id", "client_id"
            ]
        )
        legal_entity_id = data.get("legal_entity_id")
        legal_entity_name = data.get("legal_entity_name")
        business_group_id = data.get("business_group_id")
        client_id = data.get("client_id")
        return UnitLegalEntity(legal_entity_id, legal_entity_name, business_group_id, client_id)

    def to_structure(self):
        data = {
            "legal_entity_id": self.legal_entity_id,
            "legal_entity_name": self.legal_entity_name,
            "business_group_id": self.business_group_id,
            "client_id": self.client_id,
        }
        print "UnitLegalEntity"
        print data
        return to_dictionary_values(data)


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
            "service_provider_name": to_structure_CustomTextType_250(self.service_provider_name),
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
        address = parse_structure_OptionalType_CustomTextType_250(address)
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
            "service_provider_name": to_structure_CustomTextType_250(self.service_provider_name),
            "address": to_structure_OptionalType_CustomTextType_250(self.address),
            "contract_from": to_structure_CustomTextType_20(self.contract_from),
            "contract_to": to_structure_CustomTextType_20(self.contract_to),
            "contact_person": to_structure_CustomTextType_250(self.contact_person),
            "contact_no": to_structure_CustomTextType_20(self.contact_no),
            "is_active": to_structure_OptionalType_Bool(self.is_active),
        }

#
# ClientUser
#

class ClientUser(object):
    def __init__(
        self, user_id, email_id, user_group_id, employee_name,
        employee_code, contact_no, seating_unit_id, user_level, country_ids,
        domain_ids, unit_ids, is_admin, is_service_provider,
        service_provider_id, is_active, is_primary_admin
    ):
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
        self.is_primary_admin = is_primary_admin

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
        seating_unit_id = parse_structure_OptionalType_UnsignedIntegerType_32(seating_unit_id)
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
        is_primary_admin = data.get("is_primary_admin")
        is_primary_admin = parse_structure_Bool(is_primary_admin)
        return ClientUser(
            user_id, email_id, user_group_id, employee_name,
            employee_code, contact_no, seating_unit_id,
            user_level, country_ids, domain_ids, unit_ids, is_admin,
            is_service_provider, service_provider_id, is_active,
            is_primary_admin
        )

    def to_structure(self):
        return {
            "user_id": to_structure_UnsignedIntegerType_32(self.user_id),
            "email_id": to_structure_CustomTextType_100(self.email_id),
            "user_group_id": to_structure_OptionalType_UnsignedIntegerType_32(self.user_group_id),
            "employee_name": to_structure_CustomTextType_50(self.employee_name),
            "employee_code": to_structure_OptionalType_CustomTextType_50(self.employee_code),
            "contact_no": to_structure_OptionalType_CustomTextType_20(self.contact_no),
            "seating_unit_id": to_structure_OptionalType_UnsignedIntegerType_32(self.seating_unit_id),
            "user_level": to_structure_CustomIntegerType_1_10(self.user_level),
            "country_ids": to_structure_VectorType_SignedIntegerType_8(self.country_ids),
            "domain_ids": to_structure_VectorType_SignedIntegerType_8(self.domain_ids),
            "unit_ids": to_structure_VectorType_UnsignedIntegerType_32(self.unit_ids),
            "is_admin": to_structure_Bool(self.is_admin),
            "is_service_provider": to_structure_Bool(self.is_service_provider),
            "service_provider_id": to_structure_OptionalType_UnsignedIntegerType_32(self.service_provider_id),
            "is_active": to_structure_Bool(self.is_active),
            "is_primary_admin": to_structure_Bool(self.is_primary_admin),
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
        level_1_statutory_name = parse_structure_CustomTextType_100(level_1_statutory_name)
        compliances = data.get("compliances")
        compliances = parse_structure_OptionalType_VectorType_RecordType_core_ComplianceApplicability(compliances)
        applicable_status = data.get("applicable_status")
        applicable_status = parse_structure_Bool(applicable_status)
        opted_status = data.get("opted_status")
        opted_status = parse_structure_OptionalType_Bool(opted_status)
        not_applicable_remarks = data.get("not_applicable_remarks")
        not_applicable_remarks = parse_structure_OptionalType_CustomTextType_500(not_applicable_remarks)
        return AssignedStatutory(level_1_statutory_id, level_1_statutory_name, compliances, applicable_status, opted_status, not_applicable_remarks)

    def to_structure(self):
        return {
            "level_1_statutory_id": to_structure_UnsignedIntegerType_32(self.level_1_statutory_id),
            "level_1_statutory_name": to_structure_CustomTextType_100(self.level_1_statutory_name),
            "compliances": to_structure_OptionalType_VectorType_RecordType_core_ComplianceApplicability(self.compliances),
            "applicable_status": to_structure_Bool(self.applicable_status),
            "opted_status": to_structure_OptionalType_Bool(self.opted_status),
            "not_applicable_remarks": to_structure_OptionalType_CustomTextType_500(self.not_applicable_remarks),
        }

#
# ActiveCompliance
#

class ActiveCompliance(object):
    def __init__(
        self, compliance_history_id, compliance_name, compliance_frequency,
        domain_name, start_date, due_date, compliance_status, validity_date,
        next_due_date, ageing, format_file_name, unit_name, address,
        compliance_description, remarks, compliance_id, file_names, download_url
    ):
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
                "compliance_frequency", "domain_name", "start_date", "due_date",
                "compliance_status", "validity_date", "next_due_date", "ageing",
                "format_file_name", "unit_name", "address", "compliance_description",
                "remarks", "compliance_id", "file_names", "download_url"
            ]
        )
        compliance_history_id = data.get("compliance_history_id")
        compliance_history_id = parse_structure_UnsignedIntegerType_32(compliance_history_id)
        compliance_name = data.get("compliance_name")
        compliance_name = parse_structure_CustomTextType_250(compliance_name)
        compliance_frequency = data.get("compliance_frequency")
        compliance_frequency = parse_structure_EnumType_core_COMPLIANCE_FREQUENCY(compliance_frequency)
        domain_name = data.get("domain_name")
        domain_name = parse_structure_CustomTextType_50(domain_name)
        start_date = data.get("start_date")
        start_date = parse_structure_CustomTextType_20(start_date)
        due_date = data.get("due_date")
        due_date = parse_structure_CustomTextType_20(due_date)
        compliance_status = data.get("compliance_status")
        compliance_status = parse_structure_EnumType_core_COMPLIANCE_STATUS(compliance_status)
        validity_date = data.get("validity_date")
        validity_date = parse_structure_OptionalType_CustomTextType_20(validity_date)
        next_due_date = data.get("next_due_date")
        next_due_date = parse_structure_OptionalType_CustomTextType_20(next_due_date)
        ageing = data.get("ageing")
        ageing = parse_structure_CustomTextType_20(ageing)
        format_file_name = data.get("format_file_name")
        format_file_name = parse_structure_OptionalType_VectorType_CustomTextType_250(format_file_name)
        unit_name = data.get("unit_name")
        unit_name = parse_structure_CustomTextType_200(unit_name)
        address = data.get("address")
        address = parse_structure_CustomTextType_500(address)
        compliance_description = data.get("compliance_description")
        compliance_description = parse_structure_CustomTextType_500(compliance_description)
        remarks = data.get("remarks")
        remarks = parse_structure_OptionalType_CustomTextType_500(compliance_description)
        compliance_id = data.get("compliance_id")
        compliance_id = parse_structure_UnsignedIntegerType_32(compliance_id)
        file_names = data.get("file_names")
        file_names = parse_structure_OptionalType_VectorType_CustomTextType_500(file_names)
        download_url = data.get("download_url")
        download_url = parse_structure_OptionalType_VectorType_CustomTextType_500(download_url)
        return ActiveCompliance(
            compliance_history_id, compliance_name,
            compliance_frequency, domain_name, start_date, due_date,
            compliance_status, validity_date, next_due_date, ageing,
            format_file_name, unit_name, address, compliance_description,
            remarks, compliance_id, file_names, download_url
        )

    def to_structure(self):
        return {
            "compliance_history_id": to_structure_UnsignedIntegerType_32(self.compliance_history_id),
            "compliance_name": to_structure_CustomTextType_250(self.compliance_name),
            "compliance_frequency": to_structure_EnumType_core_COMPLIANCE_FREQUENCY(self.compliance_frequency),
            "domain_name": to_structure_CustomTextType_50(self.domain_name),
            "start_date": to_structure_CustomTextType_20(self.start_date),
            "due_date": to_structure_OptionalType_CustomTextType_20(self.due_date),
            "compliance_status": to_structure_EnumType_core_COMPLIANCE_STATUS(self.compliance_status),
            "validity_date": to_structure_OptionalType_CustomTextType_20(self.validity_date),
            "next_due_date": to_structure_OptionalType_CustomTextType_20(self.next_due_date),
            "ageing": to_structure_CustomTextType_100(self.ageing),
            "format_file_name": to_structure_OptionalType_VectorType_CustomTextType_250(self.format_file_name),
            "unit_name" : to_structure_CustomTextType_200(self.unit_name),
            "address" : to_structure_CustomTextType_500(self.address),
            "compliance_description" : to_structure_CustomTextType_500(self.compliance_description),
            "remarks" : to_structure_OptionalType_CustomTextType_500(self.remarks),
            "compliance_id": to_structure_UnsignedIntegerType_32(self.compliance_id),
            "file_names": to_structure_OptionalType_VectorType_CustomTextType_500(self.file_names),
            "download_url": to_structure_OptionalType_VectorType_CustomTextType_500(self.download_url)
        }

#
# UpcomingCompliance
#

class UpcomingCompliance(object):
    def __init__(
        self, compliance_name, domain_name, start_date, due_date,
        format_file_name, unit_name, address, compliance_description
    ):
        self.compliance_name = compliance_name
        self.domain_name = domain_name
        self.start_date = start_date
        self.due_date = due_date
        self.format_file_name = format_file_name
        self.unit_name = unit_name
        self.address = address
        self.compliance_description = compliance_description

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "compliance_name", "domain_name", "start_date",
            "due_date", "format_file_name", "unit_name", "address",
            "compliance_description"
        ])
        compliance_name = data.get("compliance_name")
        compliance_name = parse_structure_CustomTextType_250(compliance_name)
        domain_name = data.get("domain_name")
        domain_name = parse_structure_CustomTextType_50(domain_name)
        start_date = data.get("start_date")
        start_date = parse_structure_CustomTextType_20(start_date)
        due_date = data.get("due_date")
        due_date = parse_structure_CustomTextType_20(due_date)
        format_file_name = data.get("format_file_name")
        format_file_name = parse_structure_OptionalType_VectorType_CustomTextType_250(format_file_name)
        unit_name = data.get("unit_name")
        unit_name = parse_structure_CustomTextType_100(unit_name)
        address = data.get("address")
        address = parse_structure_CustomTextType_500(address)
        compliance_description = data.get("compliance_description")
        compliance_description = parse_structure_CustomTextType_500(compliance_description)
        return UpcomingCompliance(
            compliance_name, domain_name, start_date, due_date,
            format_file_name, unit_name, address, compliance_description
        )

    def to_structure(self):
        return {
            "compliance_name": to_structure_CustomTextType_250(self.compliance_name),
            "domain_name": to_structure_CustomTextType_50(self.domain_name),
            "start_date": to_structure_CustomTextType_20(self.start_date),
            "due_date": to_structure_CustomTextType_20(self.due_date),
            "format_file_name": to_structure_OptionalType_VectorType_CustomTextType_250(self.format_file_name),
            "unit_name": to_structure_CustomTextType_100(self.unit_name),
            "address" : to_structure_CustomTextType_500(self.address),
            "compliance_description" : to_structure_CustomTextType_500(self.compliance_description)
        }

#
# NumberOfCompliances
#

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
            "domain_id", "country_id", "year", "complied_count",
            "delayed_compliance_count",
            "inprogress_compliance_count", "not_complied_count"
        ])
        domain_id = data.get("domain_id")
        domain_id = parse_structure_UnsignedIntegerType_32(domain_id)
        country_id = data.get("country_id")
        country_id = parse_structure_UnsignedIntegerType_32(country_id)
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
        return NumberOfCompliances(
            domain_id, country_id, year, complied_count,
            delayed_compliance_count,
            inprogress_compliance_count, not_complied_count
        )

    def to_structure(self):
        return {
            "domain_id": to_structure_UnsignedIntegerType_32(self.domain_id),
            "country_id": to_structure_UnsignedIntegerType_32(self.country_id),
            "year": to_structure_CustomTextType_20(self.year),
            "complied_count": to_structure_UnsignedIntegerType_32(self.complied_count),
            "delayed_compliance_count": to_structure_UnsignedIntegerType_32(self.delayed_compliance_count),
            "inprogress_compliance_count": to_structure_UnsignedIntegerType_32(self.inprogress_compliance_count),
            "not_complied_count": to_structure_UnsignedIntegerType_32(self.not_complied_count),
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
            "country_id": to_structure_UnsignedIntegerType_32(self.country_id),
            "domain_id": to_structure_UnsignedIntegerType_32(self.domain_id),
            "from_date": to_structure_CustomTextType_20(self.from_date),
            "to_date": to_structure_CustomTextType_20(self.to_date),
            "filter_type": to_structure_EnumType_core_FILTER_TYPE(self.filter_type),
            "filter_id": to_structure_UnsignedIntegerType_32(self.filter_id),
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
            "unit_name": to_structure_UnsignedIntegerType_32(self.unit_name),
            "address": to_structure_UnsignedIntegerType_32(self.address),
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
            "unit_name": to_structure_UnsignedIntegerType_32(self.unit_name),
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
            "user_group_id": to_structure_UnsignedIntegerType_32(self.user_group_id),
            "user_group_name": to_structure_CustomTextType_50(self.user_group_name),
            "form_category_id": to_structure_UnsignedIntegerType_32(self.form_category_id),
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
        employee_name = parse_structure_CustomTextType_250(employee_name)
        is_active = data.get("is_active")
        is_active = parse_structure_Bool(is_active)
        return User(user_id, employee_name, is_active)

    def to_structure(self):
        return {
            "user_id": to_structure_UnsignedIntegerType_32(self.user_id),
            "employee_name": to_structure_CustomTextType_250(self.employee_name),
            "is_active": to_structure_Bool(self.is_active),
        }

#
# Client Incharge Persons
#

class ClientInchargePersons(object):
    def __init__(
        self, user_id, employee_name, is_active, countries, domains
    ):
        self.user_id = user_id
        self.employee_name = employee_name
        self.is_active = is_active
        self.countries = countries
        self.domains = domains

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(
            data, [
                "user_id", "employee_name",
                "is_active", "countries", "domains"
            ]
        )
        user_id = data.get("user_id")
        user_id = parse_structure_UnsignedIntegerType_32(user_id)
        employee_name = data.get("employee_name")
        employee_name = parse_structure_CustomTextType_50(employee_name)
        is_active = data.get("is_active")
        is_active = parse_structure_Bool(is_active)
        countries = data.get("countries")
        countries = parse_structure_VectorType_UnsignedIntegerType_32(countries)
        domains = data.get("domains")
        domains = parse_structure_VectorType_UnsignedIntegerType_32(domains)
        return User(user_id, employee_name, is_active, countries, domains)

    def to_structure(self):
        return {
            "user_id": to_structure_UnsignedIntegerType_32(self.user_id),
            "employee_name": to_structure_CustomTextType_50(self.employee_name),
            "is_active": to_structure_Bool(self.is_active),
            "countries": to_structure_VectorType_UnsignedIntegerType_32(self.countries),
            "domains": to_structure_VectorType_UnsignedIntegerType_32(self.domains)
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
        address = parse_structure_OptionalType_CustomTextType_250(address)
        designation = data.get("designation")
        designation = parse_structure_OptionalType_CustomTextType_50(designation)
        country_ids = data.get("country_ids")
        country_ids = parse_structure_VectorType_SignedIntegerType_8(country_ids)
        domain_ids = data.get("domain_ids")
        domain_ids = parse_structure_VectorType_SignedIntegerType_8(domain_ids)
        is_active = data.get("is_active")
        is_active = parse_structure_Bool(is_active)
        return UserDetails(user_id, email_id, user_group_id, employee_name, employee_code, contact_no, address, designation, country_ids, domain_ids, is_active)

    def to_structure(self):
        return {
            "user_id": to_structure_UnsignedIntegerType_32(self.user_id),
            "email_id": to_structure_CustomTextType_100(self.email_id),
            "user_group_id": to_structure_UnsignedIntegerType_32(self.user_group_id),
            "employee_name": to_structure_CustomTextType_50(self.employee_name),
            "employee_code": to_structure_CustomTextType_50(self.employee_code),
            "contact_no": to_structure_CustomTextType_20(self.contact_no),
            "address": to_structure_OptionalType_CustomTextType_250(self.address),
            "designation": to_structure_OptionalType_CustomTextType_50(self.designation),
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
            "country_id": to_structure_UnsignedIntegerType_32(self.country_id),
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
        compliance_name = to_structure_CustomTextType_250(compliance_name)
        description = data.get("description")
        description = parse_structure_Text(description)
        statutory_provision = data.get("statutory_provision")
        statutory_provision = parse_structure_Text(statutory_provision)
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
            "compliance_id": to_structure_UnsignedIntegerType_32(self.compliance_id),
            "compliance_name": to_structure_CustomTextType_250(self.compliance_name),
            "description": to_structure_Text(self.description),
            "statutory_provision": to_structure_Text(self.statutory_provision),
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
        compliance_name = parse_structure_CustomTextType_250(compliance_name)
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
            "compliance_name": to_structure_CustomTextType_250(self.compliance_name),
            "description": to_structure_CustomTextType_500(self.description),
            "assignee_name": to_structure_CustomTextType_50(self.assignee_name),
            "compliance_status": to_structure_EnumType_core_COMPLIANCE_STATUS(self.compliance_status),
            "ageing": to_structure_UnsignedIntegerType_32(self.ageing),
        }

#
# StatutoryDate
#

class StatutoryDate(object):
    def __init__(self, statutory_date, statutory_month, trigger_before_days, repeat_by):
        self.statutory_date = statutory_date
        self.statutory_month = statutory_month
        self.trigger_before_days = trigger_before_days
        self.repeat_by = repeat_by

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["statutory_date", "statutory_month", "trigger_before_days", "repeat_by"])
        statutory_date = data.get("statutory_date")
        statutory_date = parse_structure_OptionalType_CustomIntegerType_1_31(statutory_date)
        statutory_month = data.get("statutory_month")
        statutory_month = parse_structure_OptionalType_CustomIntegerType_1_12(statutory_month)
        trigger_before_days = data.get("trigger_before_days")
        trigger_before_days = parse_structure_OptionalType_CustomIntegerType_1_100(trigger_before_days)
        repeat_by = data.get("repeat_by")
        repeat_by = parse_structure_OptionalType_CustomTextType_20(repeat_by)
        return StatutoryDate(statutory_date, statutory_month, trigger_before_days, repeat_by)

    def to_structure(self):
        return {
            "statutory_date": to_structure_OptionalType_CustomIntegerType_1_31(self.statutory_date),
            "statutory_month": to_structure_OptionalType_CustomIntegerType_1_12(self.statutory_month),
            "trigger_before_days": to_structure_OptionalType_CustomIntegerType_1_100(self.trigger_before_days),
            "repeat_by": to_structure_OptionalType_CustomTextType_20(self.repeat_by)
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
            "form_category_id": to_structure_UnsignedIntegerType_32(self.form_category_id),
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
            "form_type_id": to_structure_UnsignedIntegerType_32(self.form_type_id),
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
# StatutoryApprovalAtatus
#
class StatutoryApprovalStatus(object):
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
        return StatutoryApprovalStatus(approval_status_id, approval_status)

    def to_structure(self):
        return {
            "approval_status_id": to_structure_SignedIntegerType_8(self.approval_status_id),
            "approval_status": to_structure_EnumType_core_APPROVAL_STATUS(self.approval_status),
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
        data = parse_dictionary(
            data, ["approval_status_id", "approval_status"]
        )
        approval_status_id = data.get("approval_status_id")
        approval_status_id = parse_structure_UnsignedIntegerType_32(
            approval_status_id)
        approval_status = data.get("approval_status")
        approval_status = parse_structure_EnumType_core_COMPLIANCE_APPROVAL_STATUS(
            approval_status)
        return ComplianceApprovalStatus(approval_status_id, approval_status)

    def to_structure(self):
        return {
            "approval_status_id": to_structure_SignedIntegerType_8(
                self.approval_status_id),
            "approval_status": to_structure_EnumType_core_COMPLIANCE_APPROVAL_STATUS(
                self.approval_status),
        }


#
# Client Level One Statutory
#
class ClientLevelOneStatutory(object):
    def __init__(self, statutory):
        self.statutory = statutory

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["statutory"])
        statutory = data.get("statutory")
        statutory = parse_structure_CustomTextType_50(statutory)
        return ClientLevelOneStatutory(statutory)

    def to_structure(self):
        return {
            "statutory": to_structure_CustomTextType_50(self.statutory)
        }


#
# Client Compliance Filter
#
class ComplianceFilter(object):
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

        return ComplianceFilter(compliance_id, compliance_name)

    def to_structure(self):
        return {
            "compliance_id": to_structure_UnsignedIntegerType_32(
                self.compliance_id),
            "compliance_name": to_structure_CustomTextType_500(
                self.compliance_name),
        }


#
# Validity Dates
#
class ValidityDates(object):
    def __init__(self, validity_days_id, country_id, domain_id, validity_days):
        self.validity_days_id = validity_days_id
        self.country_id = country_id
        self.domain_id = domain_id
        self.validity_days = validity_days

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(
            data, [
                "validity_days_id", "country_id", "domain_id", "validity_days"
            ]
        )
        validity_days_id = data.get("validity_days_id")
        country_id = data.get("country_id")
        domain_id = data.get("domain_id")
        validity_days = data.get("validity_days")
        return ValidityDates(
            validity_days_id, country_id, domain_id, validity_days
        )

    def to_structure(self):
        return {
            "validity_days_id": self.validity_days_id,
            "country_id": self.country_id,
            "domain_id": self.domain_id,
            "validity_days": self.validity_days
        }


#
# Client Group
#
class ClientGroup(object):
    def __init__(
        self, group_id, group_name, country_names,
        no_of_legal_entities, is_active, is_approved, remarks
    ):
        self.group_id = group_id
        self.group_name = group_name
        self.country_names = country_names
        self.no_of_legal_entities = no_of_legal_entities
        self.is_active = is_active
        self.is_approved = is_approved
        self.remarks = remarks

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(
            data, [
                "group_id", "group_name", "country_names",
                "no_of_legal_entities", "is_active", "is_approved",
                "remarks"
            ]
        )
        group_id = data.get("group_id")
        group_name = data.get("group_name")
        country_names = data.get("country_names")
        no_of_legal_entities = data.get("no_of_legal_entities")
        is_active = data.get("is_active")
        is_approved = data.get("is_approved")
        remarks = data.get("remarks")
        return ClientGroup(
            group_id, group_name, country_names, no_of_legal_entities,
            is_active, is_approved, remarks
        )

    def to_structure(self):
        return {
            "group_id": self.group_id,
            "group_name": self.group_name,
            "country_names": self.country_names,
            "no_of_legal_entities": self.no_of_legal_entities,
            "is_active": self.is_active,
            "is_approved": self.is_approved,
            "remarks": self.remarks
        }


#
# Legal Entity Details
#
class LegalEntityDetails(object):
    def __init__(
        self, country_id, business_group, legal_entity_name,
        logo, no_of_licence, file_space, contract_from,
        contract_to, domain_details
    ):
        self.country_id = country_id
        self.business_group = business_group
        self.legal_entity_name = legal_entity_name
        self.logo = logo
        self.no_of_licence = no_of_licence
        self.file_space = file_space
        self.contract_from = contract_from
        self.contract_to = contract_to
        self.domain_details = domain_details

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(
            data, [
                "country_id", "business_group", "legal_entity_name", "logo",
                "no_of_licence", "file_space", "contract_from",
                "contract_to", "domain_details"
            ]
        )
        country_id = data.get("country_id")
        business_group = data.get("business_group")
        legal_entity_name = data.get("legal_entity_name")
        logo = data.get("logo")
        no_of_licence = data.get("no_of_licence")
        file_space = data.get("file_space")
        contract_from = data.get("contract_from")
        contract_to = data.get("contract_to")
        domain_details = data.get("domain_details")
        return LegalEntityDetails(
            country_id, business_group, legal_entity_name,
            logo, no_of_licence, file_space, contract_from,
            contract_to, domain_details
        )

    def to_structure(self):
        return {
            "country_id": self.country_id,
            "business_group": self.business_group,
            "legal_entity_name": self.legal_entity_name,
            "logo": self.logo,
            "no_of_licence": self.no_of_licence,
            "file_space": self.file_space,
            "contract_from": self.contract_from,
            "contract_to": self.contract_to,
            "domain_details": self.domain_details
        }


class LegalEntity(object):
    def __init__(
        self, country_id, business_group, legal_entity_id,
        legal_entity_name, old_logo, new_logo,
        no_of_licence, file_space, contract_from,
        contract_to, domain_details
    ):
        self.country_id = country_id
        self.business_group = business_group
        self.legal_entity_id = legal_entity_id
        self.legal_entity_name = legal_entity_name
        self.old_logo = old_logo
        self.new_logo = new_logo
        self.no_of_licence = no_of_licence
        self.file_space = file_space
        self.contract_from = contract_from
        self.contract_to = contract_to
        self.domain_details = domain_details

    @staticmethod
    def parse_structure(data):
        print
        print
        print "inside legal entity parse structure:  =======================>"
        print
        print
        data = parse_dictionary(
            data, [
                "country_id", "business_group", "legal_entity_id",
                "legal_entity_name", "old_logo", "new_logo", "no_of_licence",
                "file_space", "contract_from", "contract_to", "domain_details"
            ]
        )
        country_id = data.get("country_id")
        business_group = data.get("business_group")
        legal_entity_id = data.get("legal_entity_id")
        legal_entity_name = data.get("legal_entity_name")
        logo = data.get("old_logo")
        new_logo = data.get("new_logo")
        no_of_licence = data.get("no_of_licence")
        file_space = data.get("file_space")
        contract_from = data.get("contract_from")
        contract_to = data.get("contract_to")
        domain_details = data.get("domain_details")
        return LegalEntity(
            country_id, business_group, legal_entity_id, legal_entity_name,
            logo, new_logo, no_of_licence, file_space,
            contract_from, contract_to, domain_details
        )

    def to_structure(self):
        return {
            "country_id": self.country_id,
            "business_group": self.business_group,
            "legal_entity_id": self.legal_entity_id,
            "legal_entity_name": self.legal_entity_name,
            "old_logo": self.old_logo,
            "new_logo": self.new_logo,
            "no_of_licence": self.no_of_licence,
            "file_space": self.file_space,
            "contract_from": self.contract_from,
            "contract_to": self.contract_to,
            "domain_details": self.domain_details
        }

#
# Entity Domain Details
#
class EntityDomainDetails(object):
    def __init__(
        self, domain_id, organization, activation_date
    ):
        self.domain_id = domain_id
        self.organization = organization
        self.activation_date = activation_date

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["d_id", "org", "activation_date"])
        domain_id = data.get("d_id")
        organization = data.get("org")
        organization = parse_structure_MapType_CustomTextType_50_VectorType_UnsignedIntegerType_32(organization)
        activation_date = data.get("activation_date")
        return EntityDomainDetails(
            domain_id, organization, activation_date
        )

    def to_structure(self):
        return {
            "d_id": self.domain_id,
            "org": to_structure_MapType_CustomTextType_50_VectorType_UnsignedIntegerType_32(
                    self.organization
                ),
            "activation_date": self.activation_date
        }

class AssignLegalEntity(object):
    def __init__(
        self, client_id, group_id, country_name,
        group_name,no_of_legal_entities
    ):
        self.client_id = client_id
        self.group_id = group_id
        self.country_name = country_name
        self.group_name = group_name
        self.no_of_legal_entities = no_of_legal_entities


    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(
            data, [
                "client_id", "group_id", "country_name", "group_name"
                "no_of_legal_entities"
            ]
        )
        client_id = data.get("client_id")
        group_id = data.get("group_id")
        country_name = data.get("country_name")
        group_name = data.get("group_name")
        no_of_legal_entities = data.get("no_of_legal_entities")
        
        return AssignLegalEntity(
            client_id, group_id, country_name, group_name, no_of_legal_entities
        )

    def to_structure(self):
        return {
            "client_id": self.client_id,
            "group_id": self.group_id,
            "country_name": self.country_name,
            "group_name": self.group_name,
            "no_of_legal_entities": self.no_of_legal_entities
        }
