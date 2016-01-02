import json
from protocol.jsonvalidators import (parse_enum, parse_dictionary, parse_static_list)
from protocol.parse_structure import (
    parse_structure_CustomIntegerType_1_7,
    parse_structure_VectorType_RecordType_clientadminsettings_LICENCE_HOLDER,
    parse_structure_CustomTextType_250,
    parse_structure_VectorType_RecordType_clientadminsettings_PROFILE_DETAIL,
    parse_structure_SignedIntegerType_8,
    parse_structure_CustomTextType_100, parse_structure_Bool,
    parse_structure_CustomTextType_20, parse_structure_CustomTextType_50,
    parse_structure_VariantType_clientadminsettings_Request
)
from protocol.to_structure import (
    to_structure_CustomIntegerType_1_7,
    to_structure_VectorType_RecordType_clientadminsettings_LICENCE_HOLDER,
    to_structure_CustomTextType_250,
    to_structure_VectorType_RecordType_clientadminsettings_PROFILE_DETAIL,
    to_structure_SignedIntegerType_8, to_structure_CustomTextType_100,
    to_structure_Bool, to_structure_CustomTextType_20,
    to_structure_CustomTextType_50,
    to_structure_VariantType_clientadminsettings_Request
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

class GetSettings(Request):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return GetSettings()

    def to_inner_structure(self):
        return {
        }

class UpdateSettings(Request):
    def __init__(self, is_two_levels_of_approval, assignee_reminder_days, escalation_reminder_In_advance_days, escalation_reminder_days):
        self.is_two_levels_of_approval = is_two_levels_of_approval
        self.assignee_reminder_days = assignee_reminder_days
        self.escalation_reminder_In_advance_days = escalation_reminder_In_advance_days
        self.escalation_reminder_days = escalation_reminder_days

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["is_two_levels_of_approval", "assignee_reminder_days", "escalation_reminder_In_advance_days", "escalation_reminder_days"])
        is_two_levels_of_approval = data.get("is_two_levels_of_approval")
        is_two_levels_of_approval = parse_structure_Bool(is_two_levels_of_approval)
        assignee_reminder_days = data.get("assignee_reminder_days")
        assignee_reminder_days = parse_structure_CustomIntegerType_1_7(assignee_reminder_days)
        escalation_reminder_In_advance_days = data.get("escalation_reminder_In_advance_days")
        escalation_reminder_In_advance_days = parse_structure_CustomIntegerType_1_7(escalation_reminder_In_advance_days)
        escalation_reminder_days = data.get("escalation_reminder_days")
        escalation_reminder_days = parse_structure_CustomIntegerType_1_7(escalation_reminder_days)
        return UpdateSettings(is_two_levels_of_approval, assignee_reminder_days, escalation_reminder_In_advance_days, escalation_reminder_days)

    def to_inner_structure(self):
        return {
            "is_two_levels_of_approval": to_structure_Bool(self.is_two_levels_of_approval),
            "assignee_reminder_days": to_structure_CustomIntegerType_1_7(self.assignee_reminder_days),
            "escalation_reminder_In_advance_days": to_structure_CustomIntegerType_1_7(self.escalation_reminder_In_advance_days),
            "escalation_reminder_days": to_structure_CustomIntegerType_1_7(self.escalation_reminder_days),
        }


def _init_Request_class_map():
    classes = [GetSettings, UpdateSettings]
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

class GetSettingsSuccess(Response):
    def __init__(self, is_two_levels_of_approval, assignee_reminder_days, escalation_reminder_In_advance_days, escalation_reminder_days, profile_detail):
        self.is_two_levels_of_approval = is_two_levels_of_approval
        self.assignee_reminder_days = assignee_reminder_days
        self.escalation_reminder_In_advance_days = escalation_reminder_In_advance_days
        self.escalation_reminder_days = escalation_reminder_days
        self.profile_detail = profile_detail

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["is_two_levels_of_approval", "assignee_reminder_days", "escalation_reminder_In_advance_days", "escalation_reminder_days", "profile_detail"])
        is_two_levels_of_approval = data.get("is_two_levels_of_approval")
        is_two_levels_of_approval = parse_structure_Bool(is_two_levels_of_approval)
        assignee_reminder_days = data.get("assignee_reminder_days")
        assignee_reminder_days = parse_structure_SignedIntegerType_8(assignee_reminder_days)
        escalation_reminder_In_advance_days = data.get("escalation_reminder_In_advance_days")
        escalation_reminder_In_advance_days = parse_structure_SignedIntegerType_8(escalation_reminder_In_advance_days)
        escalation_reminder_days = data.get("escalation_reminder_days")
        escalation_reminder_days = parse_structure_SignedIntegerType_8(escalation_reminder_days)
        profile_detail = data.get("profile_detail")
        profile_detail = parse_structure_VectorType_RecordType_clientadminsettings_PROFILE_DETAIL(profile_detail)
        return GetSettingsSuccess(is_two_levels_of_approval, assignee_reminder_days, escalation_reminder_In_advance_days, escalation_reminder_days, profile_detail)

    def to_inner_structure(self):
        return {
            "is_two_levels_of_approval": to_structure_Bool(self.is_two_levels_of_approval),
            "assignee_reminder_days": to_structure_SignedIntegerType_8(self.assignee_reminder_days),
            "escalation_reminder_In_advance_days": to_structure_SignedIntegerType_8(self.escalation_reminder_In_advance_days),
            "escalation_reminder_days": to_structure_SignedIntegerType_8(self.escalation_reminder_days),
            "profile_detail": to_structure_VectorType_RecordType_clientadminsettings_PROFILE_DETAIL(self.profile_detail),
        }

class UpdateSettingsSuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return UpdateSettingsSuccess()

    def to_inner_structure(self):
        return {
        }


def _init_Response_class_map():
    classes = [GetSettingsSuccess, UpdateSettingsSuccess]
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
        request = parse_structure_VariantType_clientadminsettings_Request(request)
        return RequestFormat(session_token, request)

    def to_structure(self):
        return {
            "session_token": to_structure_CustomTextType_50(self.session_token),
            "request": to_structure_VariantType_clientadminsettings_Request(self.request),
        }

#
# PROFILE_DETAIL
#

class PROFILE_DETAIL(object):
    def __init__(self, contract_from, contract_to, no_of_user_licence, remaining_licence, licence_holders):
        self.contract_from = contract_from
        self.contract_to = contract_to
        self.no_of_user_licence = no_of_user_licence
        self.remaining_licence = remaining_licence
        self.licence_holders = licence_holders

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["contract_from", "contract_to", "no_of_user_licence", "remaining_licence", "licence_holders"])
        contract_from = data.get("contract_from")
        contract_from = parse_structure_CustomTextType_20(contract_from)
        contract_to = data.get("contract_to")
        contract_to = parse_structure_CustomTextType_20(contract_to)
        no_of_user_licence = data.get("no_of_user_licence")
        no_of_user_licence = parse_structure_SignedIntegerType_8(no_of_user_licence)
        remaining_licence = data.get("remaining_licence")
        remaining_licence = parse_structure_SignedIntegerType_8(remaining_licence)
        licence_holders = data.get("licence_holders")
        licence_holders = parse_structure_VectorType_RecordType_clientadminsettings_LICENCE_HOLDER(licence_holders)
        return PROFILE_DETAIL(contract_from, contract_to, no_of_user_licence, remaining_licence, licence_holders)

    def to_structure(self):
        return {
            "contract_from": to_structure_CustomTextType_20(self.contract_from),
            "contract_to": to_structure_CustomTextType_20(self.contract_to),
            "no_of_user_licence": to_structure_SignedIntegerType_8(self.no_of_user_licence),
            "remaining_licence": to_structure_SignedIntegerType_8(self.remaining_licence),
            "licence_holders": to_structure_VectorType_RecordType_clientadminsettings_LICENCE_HOLDER(self.licence_holders),
        }

#
# LICENCE_HOLDER
#

class LICENCE_HOLDER(object):
    def __init__(self, user_id, user_name, email_id, contact_no, seating_unit_name, address, total_disk_space, used_disk_space):
        self.user_id = user_id
        self.user_name = user_name
        self.email_id = email_id
        self.contact_no = contact_no
        self.seating_unit_name = seating_unit_name
        self.address = address
        self.total_disk_space = total_disk_space
        self.used_disk_space = used_disk_space

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["user_id", "user_name", "email_id", "contact_no", "seating_unit_name", "address", "total_disk_space", "used_disk_space"])
        user_id = data.get("user_id")
        user_id = parse_structure_SignedIntegerType_8(user_id)
        user_name = data.get("user_name")
        user_name = parse_structure_CustomTextType_100(user_name)
        email_id = data.get("email_id")
        email_id = parse_structure_CustomTextType_100(email_id)
        contact_no = data.get("contact_no")
        contact_no = parse_structure_CustomTextType_20(contact_no)
        seating_unit_name = data.get("seating_unit_name")
        seating_unit_name = parse_structure_CustomTextType_100(seating_unit_name)
        address = data.get("address")
        address = parse_structure_CustomTextType_250(address)
        total_disk_space = data.get("total_disk_space")
        total_disk_space = parse_structure_SignedIntegerType_8(total_disk_space)
        used_disk_space = data.get("used_disk_space")
        used_disk_space = parse_structure_SignedIntegerType_8(used_disk_space)
        return LICENCE_HOLDER(user_id, user_name, email_id, contact_no, seating_unit_name, address, total_disk_space, used_disk_space)

    def to_structure(self):
        return {
            "user_id": to_structure_SignedIntegerType_8(self.user_id),
            "user_name": to_structure_CustomTextType_100(self.user_name),
            "email_id": to_structure_CustomTextType_100(self.email_id),
            "contact_no": to_structure_CustomTextType_20(self.contact_no),
            "seating_unit_name": to_structure_CustomTextType_100(self.seating_unit_name),
            "address": to_structure_CustomTextType_250(self.address),
            "total_disk_space": to_structure_SignedIntegerType_8(self.total_disk_space),
            "used_disk_space": to_structure_SignedIntegerType_8(self.used_disk_space),
        }

