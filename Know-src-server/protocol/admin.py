from protocol.jsonvalidators import (
    parse_dictionary, parse_static_list, parse_VariantType,
    to_VariantType, to_structure_dictionary_values
)
from protocol.parse_structure import (
    parse_structure_MapType_UnsignedInteger_32_VectorType_UnsignedInteger_32
)
from protocol.to_structure import (
    to_structure_MapType_UnsignedInteger_32_VectorType_UnsignedInteger_32
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


class GetUserGroups(Request):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return GetUserGroups()

    def to_inner_structure(self):
        return {
        }


class SaveUserGroup(Request):
    def __init__(self, user_group_name, form_category_id, form_ids):
        self.user_group_name = user_group_name
        self.form_category_id = form_category_id
        self.form_ids = form_ids

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["ug_name", "fc_id", "f_ids"])
        user_group_name = data.get("ug_name")
        form_category_id = data.get("fc_id")
        form_ids = data.get("f_ids")
        return SaveUserGroup(user_group_name, form_category_id, form_ids)

    def to_inner_structure(self):
        return {
            "ug_name": self.user_group_name,
            "fc_id": self.form_category_id,
            "f_ids": self.form_ids
        }


class UpdateUserGroup(Request):
    def __init__(
        self, user_group_id, user_group_name, form_category_id, form_ids
    ):
        self.user_group_id = user_group_id
        self.user_group_name = user_group_name
        self.form_category_id = form_category_id
        self.form_ids = form_ids

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["ug_id", "ug_name", "fc_id", "f_ids"])
        user_group_id = data.get("ug_id")
        user_group_name = data.get("ug_name")
        form_category_id = data.get("fc_id")
        form_ids = data.get("f_ids")
        return UpdateUserGroup(
            user_group_id, user_group_name, form_category_id, form_ids)

    def to_inner_structure(self):
        return {
            "ug_id": self.user_group_id,
            "ug_name": self.user_group_name,
            "fc_id": self.form_category_id,
            "f_ids": self.form_ids
        }


class ChangeUserGroupStatus(Request):
    def __init__(self, user_group_id, user_group_name, is_active):
        self.user_group_id = user_group_id
        self.user_group_name = user_group_name
        self.is_active = is_active

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["ug_id", "ug_name", "active"])
        user_group_id = data.get("ug_id")
        user_group_name = data.get("ug_name")
        is_active = data.get("active")
        return ChangeUserGroupStatus(user_group_id, user_group_name, is_active)

    def to_inner_structure(self):
        return {
            "ug_id": self.user_group_id,
            "ug_name": self.user_group_name,
            "active": self.is_active
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


class SendRegistraion(Request):
    def __init__(self, user_id, username, email_id):
        self.user_id = user_id
        self.email_id = email_id
        self.username = username

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["user_id", "username", "email_id"])
        user_id = data.get("user_id")
        username = data.get("username")
        email_id = data.get("email_id")
        return SendRegistraion(user_id, username, email_id)

    def to_inner_structure(self):
        return {
            "user_id": self.user_id,
            "username": self.username,
            "email_id": self.email_id
        }


class SaveUser(Request):
    def __init__(
        self, user_category_id, employee_name,
        employee_code, email_id, contact_no, mobile_no,
        user_group_id, address, designation,
        country_ids, domain_ids
    ):
        self.user_category_id = user_category_id
        self.employee_name = employee_name
        self.employee_code = employee_code
        self.email_id = email_id
        self.contact_no = contact_no
        self.mobile_no = mobile_no
        self.user_group_id = user_group_id
        self.address = address
        self.designation = designation
        self.country_ids = country_ids
        self.domain_ids = domain_ids

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "u_cat_id",  "employee_name", "employee_code",
            "email_id", "contact_no", "mobile_no",
            "ug_id", "address", "designation", "country_ids",
            "country_wise_domain"])
        user_category_id = data.get("u_cat_id")
        employee_name = data.get("employee_name")
        employee_code = data.get("employee_code")
        email_id = data.get("email_id")
        contact_no = data.get("contact_no")
        mobile_no = data.get("mobile_no")
        user_group_id = data.get("ug_id")
        address = data.get("address")
        designation = data.get("designation")
        country_ids = data.get("country_ids")
        domain_ids = data.get("country_wise_domain")
        return SaveUser(
            user_category_id, employee_name, employee_code, email_id,
            contact_no, mobile_no, user_group_id, address,
            designation, country_ids, domain_ids
        )

    def to_inner_structure(self):
        return {
            "u_cat_id": self.user_category_id,
            "employee_name": self.employee_name,
            "employee_code": self.employee_code,
            "email_id": self.email_id,
            "contact_no": self.contact_no,
            "mobile_no": self.mobile_no,
            "ug_id": self.user_group_id,
            "address": self.address,
            "designation": self.designation,
            "country_ids": self.country_ids,
            "country_wise_domain": self.domain_ids
        }


class UpdateUser(Request):
    def __init__(
        self, user_id, user_category_id, employee_name,
        employee_code, email_id, contact_no, mobile_no,
        user_group_id, address, designation,
        country_ids, domain_ids
    ):
        self.user_id = user_id
        self.user_category_id = user_category_id
        self.employee_name = employee_name
        self.employee_code = employee_code
        self.email_id = email_id
        self.contact_no = contact_no
        self.mobile_no = mobile_no
        self.user_group_id = user_group_id
        self.address = address
        self.designation = designation
        self.country_ids = country_ids
        self.domain_ids = domain_ids

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "user_id", "u_cat_id",  "employee_name", "employee_code",
            "email_id", "contact_no", "mobile_no",
            "ug_id", "address", "designation", "country_ids",
            "country_wise_domain"])
        user_id = data.get("user_id")
        user_category_id = data.get("u_cat_id")
        employee_name = data.get("employee_name")
        employee_code = data.get("employee_code")
        email_id = data.get("email_id")
        contact_no = data.get("contact_no")
        mobile_no = data.get("mobile_no")
        user_group_id = data.get("ug_id")
        address = data.get("address")
        designation = data.get("designation")
        country_ids = data.get("country_ids")
        domain_ids = data.get("country_wise_domain")
        return UpdateUser(
            user_id, user_category_id, employee_name, employee_code, email_id,
            contact_no, mobile_no, user_group_id, address,
            designation, country_ids, domain_ids
        )

    def to_inner_structure(self):
        return {
            "user_id": self.user_id,
            "u_cat_id": self.user_category_id,
            "employee_name": self.employee_name,
            "employee_code": self.employee_code,
            "email_id": self.email_id,
            "contact_no": self.contact_no,
            "mobile_no": self.mobile_no,
            "ug_id": self.user_group_id,
            "address": self.address,
            "designation": self.designation,
            "country_ids": self.country_ids,
            "country_wise_domain": self.domain_ids
        }

class ChangeUserStatus(Request):
    def __init__(self, user_id, is_active):
        self.user_id = user_id
        self.is_active = is_active

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["user_id", "is_active"])
        user_id = data.get("user_id")
        is_active = data.get("is_active")
        return ChangeUserStatus(user_id, is_active)

    def to_inner_structure(self):
        return {
            "user_id": self.user_id,
            "is_active": self.is_active,
        }

class ChangeDisableStatus(Request):
    def __init__(self, user_id, is_active, remarks):
        self.user_id = user_id
        self.is_active = is_active
        self.remarks = remarks

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["user_id", "is_disable", "remarks"])
        user_id = data.get("user_id")
        is_active = data.get("is_disable")
        remarks = data.get("remarks")
        return ChangeDisableStatus(user_id, is_active, remarks)

    def to_inner_structure(self):
        return {
            "user_id": self.user_id,
            "is_disable": self.is_active,
            "remarks": self.remarks
        }

class GetValidityDateList(Request):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return GetValidityDateList()

    def to_inner_structure(self):
        return {
        }


class SaveValidityDateSettings(Request):
    def __init__(self, validity_date_settings):
        self.validity_date_settings = validity_date_settings

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["validity_date_settings"])
        validity_date_settings = data.get("validity_date_settings")
        return SaveValidityDateSettings(validity_date_settings)

    def to_inner_structure(self):
        return {
            "validity_date_settings": self.validity_date_settings
        }


class GetUserMappings(Request):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return GetUserMappings()

    def to_inner_structure(self):
        return {
        }


class SaveUserMappings(Request):
    def __init__(self, country_id, domain_id, parent_user_id, child_users, user_category_id, new_child_users, new_child_user_names):
        self.country_id = country_id
        self.domain_id = domain_id
        self.parent_user_id = parent_user_id
        self.child_users = child_users
        self.user_category_id = user_category_id
        self.new_child_users = new_child_users
        self.new_child_user_names = new_child_user_names

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(
            data, [
                "country_id", "domain_id", "parent_user_id", "child_users", "user_category_id", "new_child_users", "new_child_user_names"
            ])
        country_id = data.get("country_id")
        domain_id = data.get("domain_id")
        parent_user_id = data.get("parent_user_id")
        child_users = data.get("child_users")
        user_category_id = data.get("user_category_id")
        new_child_users = data.get("new_child_users")
        new_child_user_names = data.get("new_child_user_names")
        return SaveUserMappings(
            country_id, domain_id, parent_user_id, child_users, user_category_id, new_child_users, new_child_user_names
        )

    def to_inner_structure(self):
        return {
            "country_id": self.country_id,
            "domain_id": self.domain_id,
            "parent_user_id": self.parent_user_id,
            "child_users": self.child_users,
            "user_category_id": self.user_category_id,
            "new_child_users": self.new_child_users,
            "new_child_user_names": self.new_child_user_names
        }

class CheckUserMappings(Request):
    def __init__(self, country_id, domain_id, parent_user_id, child_user_id, user_category_id):
        self.country_id = country_id
        self.domain_id = domain_id
        self.parent_user_id = parent_user_id
        self.child_user_id = child_user_id
        self.user_category_id = user_category_id

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(
            data, [
                "country_id", "domain_id", "parent_user_id", "child_user_id", "user_category_id"
            ])
        country_id = data.get("country_id")
        domain_id = data.get("domain_id")
        parent_user_id = data.get("parent_user_id")
        child_user_id = data.get("child_user_id")
        user_category_id = data.get("user_category_id")
        return CheckUserMappings(
            country_id, domain_id, parent_user_id, child_user_id, user_category_id
        )

    def to_inner_structure(self):
        return {
            "country_id": self.country_id,
            "domain_id": self.domain_id,
            "parent_user_id": self.parent_user_id,
            "child_user_id": self.child_user_id,
            "user_category_id": self.user_category_id
        }


class GetReassignUserAccountFormdata(Request):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return GetReassignUserAccountFormdata()

    def to_inner_structure(self):
        return {
        }

class GetTechnoUserData(Request):
    def __init__(self, user_id):
        self.user_id = user_id

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["techno_id"])
        user_id = data.get("techno_id")
        return GetTechnoUserData(user_id)

    def to_inner_structure(self):
        return {
            "techno_id": self.user_id
        }

class GetDomainUserData(Request):
    def __init__(self, domain_user_id, group_id, entity_id, domain_id):
        self.domain_user_id = domain_user_id
        self.group_id = group_id
        self.entity_id = entity_id
        self.domain_id = domain_id

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["d_u_id", "gt_id", "le_id", "d_id"])
        user_id = data.get("d_u_id")
        group_id = data.get("gt_id")
        entity_id = data.get("le_id")
        domain_id = data.get("d_id")
        return GetDomainUserData(user_id, group_id, entity_id, domain_id)

    def to_inner_structure(self):
        return {
            "d_u_id": self.domain_user_id,
            "gt_id": self.group_id,
            "le_id": self.entity_id,
            "d_id": self.domain_id
        }


class SaveReassignTechnoManager(Request):
    def __init__(self, reassign_from, manager_info, remarks):
        self.reassign_from = reassign_from
        self.manager_info = manager_info
        self.remarks = remarks

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["reassign_from", "t_manager_info", "remarks"])
        return SaveReassignTechnoManager(
            data.get("reassign_from"),
            data.get("t_manager_info"), data.get("remarks")
        )

    def to_inner_structure(self):
        return {
            "reassign_from": self.reassign_from,
            "t_manager_info": self.manager_info,
            "remarks": self.remarks
        }

class ReassignTechnoManager(object):
    def __init__(
        self, reassign_to, client_id, entity_id,
        techno_executive, old_techno_executive
    ):
        self.reassign_to = reassign_to
        self.client_id = client_id
        self.entity_id = entity_id
        self.techno_executive = techno_executive
        self.old_techno_executive = old_techno_executive

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "reassign_to", "gt_id",
            "le_id", "t_e_id", "old_t_e_id"
        ])
        reassign_to = data.get("reassign_to")
        client_id = data.get("gt_id")
        entity_id = data.get("le_id")
        techno_executive = data.get("t_e_id")
        old_techno_executive = data.get("old_t_e_id")
        return ReassignTechnoManager(
            reassign_to,
            client_id, entity_id, techno_executive,
            old_techno_executive
        )

    def to_structure(self):
        return {
            "reassign_to": self.reassign_to,
            "gt_id": self.client_id,
            "le_id": self.entity_id,
            "t_e_id": self.techno_executive,
            "old_t_e_id": self.old_techno_executive
        }

class SaveReassignTechnoExecutive(Request):
    def __init__(self, reassign_from, reassign_to, manager_info, remarks):
        self.reassign_from = reassign_from
        self.reassign_to = reassign_to
        self.manager_info = manager_info
        self.remarks = remarks

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "reassign_from", "reassign_to", "t_executive_info",
            "remarks"
        ])
        return SaveReassignTechnoExecutive(
            data.get("reassign_from"), data.get("reassign_to"),
            data.get("t_executive_info"), data.get("remarks")
        )

    def to_inner_structure(self):
        return {
            "reassign_from": self.reassign_from,
            "reassign_to": self.reassign_to,
            "t_executive_info": self.manager_info,
            "remarks": self.remarks
        }

class ReassignTechnoExecutive(object):
    def __init__(
        self, client_id, entity_id
    ):
        self.client_id = client_id
        self.entity_id = entity_id

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "gt_id",
            "le_id",
        ])
        client_id = data.get("gt_id")
        entity_id = data.get("le_id")
        return ReassignTechnoExecutive(
            client_id, entity_id
        )

    def to_structure(self):
        return {
            "gt_id": self.client_id,
            "le_id": self.entity_id
        }

class SaveReassignDomainManager(Request):
    def __init__(
        self, reassign_from, reassign_to, group_id, entity_id,
        domain_id, manager_info, remarks
    ):
        self.reassign_from = reassign_from
        self.reassign_to = reassign_to
        self.group_id = group_id
        self.entity_id = entity_id
        self.domain_id = domain_id
        self.manager_info = manager_info
        self.remarks = remarks

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "reassign_from", "reassign_to", "gt_id", "le_id", "d_id",
            "d_manager_info", "remarks"
        ])
        return SaveReassignDomainManager(
            data.get("reassign_from"), data.get("reassign_to"),
            data.get("gt_id"),
            data.get("le_id"), data.get("d_id"),
            data.get("d_manager_info"),
            data.get("remarks")
        )

    def to_inner_structure(self):
        return {
            "reassign_from": self.reassign_from,
            "reassign_to": self.reassign_to,
            "gt_id": self.group_id,
            "le_id": self.entity_id,
            "d_id": self.domain_id,
            "d_manager_info": self.manager_info,
            "remarks": self.remarks
        }

class ReassignDomainManager(object):
    def __init__(
        self, unit_id, domain_executive, old_domain_executive
    ):
        self.unit_id = unit_id
        self.domain_executive = domain_executive
        self.old_domain_executive = old_domain_executive

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "u_id", "d_e_id", "old_d_e_id"
        ])
        unit_id = data.get("u_id")
        domain_executive = data.get("d_e_id")
        old_domain_executive = data.get("old_d_e_id")
        return ReassignDomainManager(
            unit_id, domain_executive,
            old_domain_executive
        )

    def to_structure(self):
        return {
            "u_id": self.unit_id,
            "d_e_id": self.domain_executive,
            "old_d_e_id": self.old_domain_executive
        }

class SaveReassignDomainExecutive(Request):
    def __init__(
        self, reassign_from, reassign_to, client_id, entity_id, domain_id,
        unit_ids, remarks
    ):
        self.reassign_from = reassign_from
        self.reassign_to = reassign_to
        self.client_id = client_id
        self.entity_id = entity_id
        self.domain_id = domain_id
        self.unit_ids = unit_ids
        self.remarks = remarks

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "reassign_from", "reassign_to", "client_id", "entity_id",
            "domain_id", "unit_ids", "remarks"
        ])
        return SaveReassignDomainExecutive(
            data.get("reassign_from"), data.get("reassign_to"),
            data.get("client_id"), data.get("entity_id"),
            data.get("domain_id"), data.get("unit_ids"),
            data.get("remarks")
        )

    def to_inner_structure(self):
        return {
            "reassign_from": self.reassign_from,
            "reassign_to": self.reassign_to,
            "client_id": self.client_id,
            "entity_id": self.entity_id,
            "domain_id": self.domain_id,
            "unit_ids": self.unit_ids,
            "remarks": self.remarks
        }

class UserReplacement(Request):
    def __init__(self, user_type, user_from, user_to, remarks):
        self.user_type = user_type
        self.user_from = user_from
        self.user_to = user_to
        self.remarks = remarks

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["user_type", "old_user_id", "new_user_id", "remarks"])
        return UserReplacement(
            data.get("user_type"),
            data.get("old_user_id"),
            data.get("new_user_id"),
            data.get("remarks")
        )

    def to_inner_structure(self):
        return {
            "user_type": self.user_type,
            "old_user_id": self.user_from,
            "new_user_id": self.user_to,
            "remarks": self.remarks
        }

class CheckUserReplacement(Request):
    def __init__(self, user_type, user_from):
        self.user_type = user_type
        self.user_from = user_from

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["user_type", "old_user_id"])
        return CheckUserReplacement(
            data.get("user_type"),
            data.get("old_user_id")
        )

    def to_inner_structure(self):
        return {
            "user_type": self.user_type,
            "old_user_id": self.user_from
        }

def _init_Request_class_map():
    classes = [
        GetUserGroups, SaveUserGroup, UpdateUserGroup,
        ChangeUserGroupStatus, GetUsers, SaveUser, UpdateUser,
        ChangeUserStatus, GetValidityDateList, SaveValidityDateSettings,
        GetUserMappings, SaveUserMappings, GetReassignUserAccountFormdata,
        SaveReassignTechnoManager, SaveReassignTechnoExecutive,
        SaveReassignDomainManager, SaveReassignDomainExecutive,
        SendRegistraion, ChangeDisableStatus,
        GetTechnoUserData, GetDomainUserData,
        UserReplacement, CheckUserMappings, CheckUserReplacement
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


class UserGroup(object):
    def __init__(
        self, user_group_id, user_group_name, user_category_id,
        form_ids, is_active, no_of_users
    ):
        self.user_group_id = user_group_id
        self.user_group_name = user_group_name
        self.user_category_id = user_category_id
        self.form_ids = form_ids
        self.is_active = is_active
        self.no_of_users = no_of_users

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(
            data, [
                "user_group_id", "user_group_name",
                "user_category_id", "form_ids", "is_active", "no_of_users"
            ])
        user_group_id = data.get("user_group_id")
        user_group_name = data.get("user_group_name")
        user_category_id = data.get("user_category_id")
        form_ids = data.get("form_ids")
        is_active = data.get("is_active")
        no_of_users = data.get("no_of_users")
        return UserGroup(
            user_group_id, user_group_name, user_category_id,
            form_ids, is_active, no_of_users)

    def to_structure(self):
        return {
            "user_group_id": self.user_group_id,
            "user_group_name": self.user_group_name,
            "user_category_id": self.user_category_id,
            "form_ids": self.form_ids,
            "is_active": self.is_active,
            "no_of_users": self.no_of_users
        }


class GetUserGroupsSuccess(Response):
    def __init__(self, form_categories, forms, user_groups):
        self.form_categories = form_categories
        self.forms = forms
        self.user_groups = user_groups

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(
            data, ["form_categories", "forms", "user_group_details"])
        form_categories = data.get("form_categories")
        forms = data.get("forms")
        user_groups = data.get("user_group_details")
        return GetUserGroupsSuccess(form_categories, forms, user_groups)

    def to_inner_structure(self):
        return {
            "form_categories": self.form_categories,
            "forms": self.forms,
            "user_group_details": self.user_groups
        }


class SaveUserGroupSuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return SaveUserGroupSuccess()

    def to_inner_structure(self):
        return {
        }


class GroupNameAlreadyExists(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return GroupNameAlreadyExists()

    def to_inner_structure(self):
        return {
        }


class UpdateUserGroupSuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return UpdateUserGroupSuccess()

    def to_inner_structure(self):
        return {
        }


class InvalidUserGroupId(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return InvalidUserGroupId()

    def to_inner_structure(self):
        return {
        }


class ChangeUserGroupStatusSuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return ChangeUserGroupStatusSuccess()

    def to_inner_structure(self):
        return {
        }


class GetUsersSuccess(Response):
    def __init__(self, user_groups, domains, countries, user_categories, users):
        self.user_groups = user_groups
        self.domains = domains
        self.countries = countries
        self.user_categories = user_categories
        self.users = users

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(
            data, ["user_groups", "domains", "countries", "user-categories", "user_details"])
        user_groups = data.get("user_groups")
        domains = data.get("domains")
        countries = data.get("countries")
        user_categories = data.get("user_categories")
        users = data.get("user_details")
        return GetUsersSuccess(user_groups, domains, countries, user_categories, users)

    def to_inner_structure(self):
        return {
            "user_groups": self.user_groups,
            "domains": self.domains,
            "countries": self.countries,
            "user_categories": self.user_categories,
            "user_details": self.users
        }

class SendRegistraionSuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return SendRegistraionSuccess()

    def to_inner_structure(self):
        return {
        }


class SaveUserSuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return SaveUserSuccess()

    def to_inner_structure(self):
        return {
        }


class EmailIDAlreadyExists(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return EmailIDAlreadyExists()

    def to_inner_structure(self):
        return {
        }


class ContactNumberAlreadyExists(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return ContactNumberAlreadyExists()

    def to_inner_structure(self):
        return {
        }


class EmployeeCodeAlreadyExists(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return EmployeeCodeAlreadyExists()

    def to_inner_structure(self):
        return {
        }


class InvalidUserId(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return InvalidUserId()

    def to_inner_structure(self):
        return {
        }


class CannotDeactivateUserExists(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return CannotDeactivateUserExists()

    def to_inner_structure(self):
        return {
        }

class CannotDisableUserTransactionExists(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return CannotDisableUserTransactionExists()

    def to_inner_structure(self):
        return {
        }


class UpdateUserSuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return UpdateUserSuccess()

    def to_inner_structure(self):
        return {
        }


class ChangeUserStatusSuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return ChangeUserStatusSuccess()

    def to_inner_structure(self):
        return {
        }


class SaveValidityDateSettingsSuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return SaveValidityDateSettingsSuccess()

    def to_inner_structure(self):
        return {
        }

class SaveValidityDateSettingsFailure(Response):
    def __init__(self, domain_id, country_id):
        self.domain_id = domain_id
        self.country_id = country_id

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["domain_id", "country_id"])
        domain_id = data.get("domain_id")
        country_id = data.get("country_id")
        return SaveValidityDateSettingsFailure(domain_id, country_id)

    def to_inner_structure(self):
        return {
            "domain_id": self.domain_id,
            "country_id": self.country_id
        }


class GetValidityDateListSuccess(Response):
    def __init__(
        self, countries, domains, validity_dates, country_domain_mappings
    ):
        self.countries = countries
        self.domains = domains
        self.validity_dates = validity_dates
        self.country_domain_mappings = country_domain_mappings

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(
            data, [
                "countries", "domains", "validity_date_settings",
                "country_domain_mappings"
            ])
        countries = data.get("countries")
        domains = data.get("domains")
        validity_dates = data.get("validity_date_settings")
        country_domain_mappings = data.get("country_domain_mappings")
        country_domain_mappings = parse_structure_MapType_UnsignedInteger_32_VectorType_UnsignedInteger_32(country_domain_mappings)
        return GetValidityDateListSuccess(
            countries, domains, validity_dates, country_domain_mappings
        )

    def to_inner_structure(self):
        return {
            "countries": self.countries,
            "domains": self.domains,
            "validity_date_settings": self.validity_dates,
            "country_domain_mappings": to_structure_MapType_UnsignedInteger_32_VectorType_UnsignedInteger_32(
                self.country_domain_mappings)
        }


class UserMapping(object):
    def __init__(
        self, user_mapping_id, parent_user_id, child_user_id, country_id, domain_id
    ):
        self.user_mapping_id = user_mapping_id
        self.parent_user_id = parent_user_id
        self.child_user_id = child_user_id
        self.country_id = country_id
        self.domain_id = domain_id

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(
            data, [
                "user_mapping_id", "parent_user_id", "child_user_id", "country_id", "domain_id"
            ])
        user_mapping_id = data.get("user_mapping_id")
        parent_user_id = data.get("parent_user_id")
        child_user_id = data.get("child_user_id")
        country_id = data.get("country_id")
        domain_id = data.get("domain_id")
        return UserMapping(
            user_mapping_id, parent_user_id, child_user_id, country_id, domain_id
        )

    def to_structure(self):
        return {
            "user_mapping_id": self.user_mapping_id,
            "parent_user_id": self.parent_user_id,
            "child_user_id": self.child_user_id,
            "country_id": self.country_id,
            "domain_id": self.domain_id
        }


class User(object):
    def __init__(
        self, user_id, employee_name, is_active, country_ids, domain_ids
    ):
        self.user_id = user_id
        self.employee_name = employee_name
        self.is_active = is_active
        self.country_ids = country_ids
        self.domain_ids = domain_ids

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(
            data, [
                "user_id", "employee_name", "is_active",
                "country_ids", "domain_ids"
            ]
        )
        user_id = data.get("user_id")
        employee_name = data.get("employee_name")
        is_active = data.get("is_active")
        country_ids = data.get("country_ids")
        domain_ids = data.get("domain_ids")
        return User(user_id, employee_name, is_active, country_ids, domain_ids)

    def to_structure(self):
        return {
            "user_id": self.user_id,
            "employee_name": self.employee_name,
            "is_active": self.is_active,
            "country_ids": self.country_ids,
            "domain_ids": self.domain_ids
        }

class MappedUser(object):
    def __init__(
        self, user_id, employee_name, is_active, country_ids, domain_ids, mapped_country_domains
    ):
        self.user_id = user_id
        self.employee_name = employee_name
        self.is_active = is_active
        self.country_ids = country_ids
        self.domain_ids = domain_ids
        self.mapped_country_domains = mapped_country_domains

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(
            data, [
                "user_id", "employee_name", "is_active",
                "country_ids", "domain_ids", "mapped_country_domains"
            ]
        )
        user_id = data.get("user_id")
        employee_name = data.get("employee_name")
        is_active = data.get("is_active")
        country_ids = data.get("country_ids")
        domain_ids = data.get("domain_ids")
        mapped_country_domains = data.get("mapped_country_domains")
        return MappedUser(user_id, employee_name, is_active, country_ids, domain_ids, mapped_country_domains)

    def to_structure(self):
        return {
            "user_id": self.user_id,
            "employee_name": self.employee_name,
            "is_active": self.is_active,
            "country_ids": self.country_ids,
            "domain_ids": self.domain_ids,
            "mapped_country_domains": self.mapped_country_domains
        }

class GetUserMappingsSuccess(Response):
    def __init__(
        self, countries, domains, knowledge_managers, knowledge_users,
        techno_managers, techno_users, domain_managers, domain_users,
        user_mappings
    ):
        self.countries = countries
        self.domains = domains
        self.knowledge_managers = knowledge_managers
        self.knowledge_users = knowledge_users
        self.techno_managers = techno_managers
        self.techno_users = techno_users
        self.domain_managers = domain_managers
        self.domain_users = domain_users
        self.user_mappings = user_mappings

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(
            data, [
                "countries", "domains", "knowledge_managers",
                "knowledge_users", "techno_managers", "techno_users",
                "domain_managers", "domain_users", "user_mappings"
            ])
        countries = data.get("countries")
        domains = data.get("domains")
        knowledge_managers = data.get("knowledge_managers")
        knowledge_users = data.get("knowledge_users")
        techno_managers = data.get("techno_managers")
        techno_users = data.get("techno_users")
        domain_managers = data.get("domain_managers")
        domain_users = data.get("domain_users")
        user_mappings = data.get("user_mappings")
        return GetUserMappingsSuccess(
            countries, domains, knowledge_managers, knowledge_users,
            techno_managers, techno_users, domain_managers, domain_users,
            user_mappings
        )

    def to_inner_structure(self):
        return {
            "countries": self.countries,
            "domains": self.domains,
            "knowledge_managers": self.knowledge_managers,
            "knowledge_users": self.knowledge_users,
            "techno_managers": self.techno_managers,
            "techno_users": self.techno_users,
            "domain_managers": self.domain_managers,
            "domain_users": self.domain_users,
            "user_mappings": self.user_mappings
        }


class SaveUserMappingsSuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return SaveUserMappingsSuccess()

    def to_inner_structure(self):
        return {
        }

class CheckUserMappingsSuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return CheckUserMappingsSuccess()

    def to_inner_structure(self):
        return {
        }


class LegalEntity(object):
    def __init__(
        self, legal_entity_id, legal_entity_name, business_group_id,
        client_id, country_id, domain_ids
    ):
        self.legal_entity_id = legal_entity_id
        self.legal_entity_name = legal_entity_name
        self.business_group_id = business_group_id
        self.client_id = client_id
        self.country_id = country_id
        self.domain_ids = domain_ids

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(
            data, [
                "legal_entity_id", "legal_entity_name", "business_group_id",
                "client_id", "country_id", "domain_ids"
            ]
        )
        legal_entity_id = data.get("legal_entity_id")
        legal_entity_name = data.get("legal_entity_name")
        business_group_id = data.get("business_group_id")
        client_id = data.get("client_id")
        country_id = data.get("country_id")
        domain_ids = data.get("domain_ids")
        return LegalEntity(
            legal_entity_id, legal_entity_name, business_group_id, client_id,
            country_id, domain_ids
        )

    def to_structure(self):
        return {
            "legal_entity_id": self.legal_entity_id,
            "legal_entity_name": self.legal_entity_name,
            "business_group_id": self.business_group_id,
            "client_id": self.client_id,
            "country_id": self.country_id,
            "domain_ids": self.domain_ids
        }


class AssignedLegalEntities(object):
    def __init__(
        self, user_id, legal_entity_id
    ):
        self.user_id = user_id
        self.legal_entity_id = legal_entity_id

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "user_id", "legal_entity_id"
        ])
        user_id = data.get("user_id")
        legal_entity_id = data.get("legal_entity_id")
        return AssignedLegalEntities(user_id, legal_entity_id)

    def to_structure(self):
        return {
            "user_id": self.user_id,
            "legal_entity_id": self.legal_entity_id
        }


class AssignedUnits(object):
    def __init__(
        self, user_id, unit_id, domain_id
    ):
        self.user_id = user_id
        self.unit_id = unit_id
        self.domain_id = domain_id

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "user_id", "unit_id", "domain_id"
        ])
        user_id = data.get("user_id")
        unit_id = data.get("unit_id")
        domain_id = data.get("domain_id")
        return AssignedUnits(user_id, unit_id, domain_id)

    def to_structure(self):
        return {
            "user_id": self.user_id,
            "unit_id": self.unit_id,
            "domain_id": self.domain_id
        }


class AssignedClient(object):
    def __init__(
        self, user_id, client_id
    ):
        self.user_id = user_id
        self.client_id = client_id

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "user_id", "client_id"
        ])
        user_id = data.get("user_id")
        client_id = data.get("client_id")
        return AssignedUnits(user_id, client_id)

    def to_structure(self):
        return {
            "user_id": self.user_id,
            "client_id": self.client_id
        }

class CountryWiseDomain(object):
    def __init__(
        self, country_id, domain_id
    ):
        self.country_id = country_id
        self.domain_id = domain_id

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "c_id", "d_id"
        ])
        country_id = data.get("c_id")
        domain_id = data.get("d_id")
        return CountryWiseDomain(country_id, domain_id)

    def to_structure(self):
        return {
            "c_id": self.country_id,
            "d_id": self.domain_id
        }

class CountryWiseDomainParent(object):
    def __init__(
        self, country_id, domain_id, p_user_ids
    ):
        self.country_id = country_id
        self.domain_id = domain_id
        self.p_user_ids = p_user_ids

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "c_id", "d_id", "p_user_ids"
        ])
        country_id = data.get("c_id")
        domain_id = data.get("d_id")
        p_user_ids = data.get("p_user_ids")
        return CountryWiseDomain(country_id, domain_id, p_user_ids)

    def to_structure(self):
        return {
            "c_id": self.country_id,
            "d_id": self.domain_id,
            "p_user_ids": self.p_user_ids,
        }

class GetReassignUserAccountFormdataSuccess(Request):
    def __init__(
        self, techno_managers, techno_users, domain_managers,
        domain_users, groups, business_groups,
        legal_entities, domains, user_categories
    ):
        self.techno_managers = techno_managers
        self.techno_users = techno_users
        self.domain_managers = domain_managers
        self.domain_users = domain_users
        self.groups = groups
        self.business_groups = business_groups
        self.legal_entities = legal_entities
        self.domains = domains
        self.user_categories = user_categories

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "t_m_reassign", "t_e_reassign", "d_m_reassign",
            "d_e_reassign", "re_assign_groups", "business_groups",
            "admin_legal_entity", "domains", "user_categories"
        ])
        techno_managers = data.get("t_m_reassign")
        techno_users = data.get("t_e_reassign")
        domain_managers = data.get("d_m_reassign")
        domain_users = data.get("d_e_reassign")
        groups = data.get("re_assign_groups")
        business_groups = data.get("business_groups")
        legal_entities = data.get("admin_legal_entity")
        domains = data.get("domains")
        user_categories = data.get("user_categories")
        return GetReassignUserAccountFormdataSuccess(
            techno_managers, techno_users, domain_managers,
            domain_users, groups, business_groups,
            legal_entities, domains, user_categories
        )

    def to_inner_structure(self):
        return {
            "t_m_reassign": self.techno_managers,
            "t_e_reassign": self.techno_users,
            "d_m_reassign": self.domain_managers,
            "d_e_reassign": self.domain_users,
            "re_assign_groups": self.groups,
            "business_groups": self.business_groups,
            "admin_legal_entity": self.legal_entities,
            "domains": self.domains,
            "user_categories": self.user_categories
        }


class SaveReassignUserAccountSuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return SaveReassignUserAccountSuccess()

    def to_inner_structure(self):
        return {
        }

class GetTechnoUserDataSuccess(Response):
    def __init__(self, group_list):
        self.group_list = group_list

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["t_user_info"])
        group_list = data.get("t_user_info")
        return GetTechnoUserDataSuccess(group_list)

    def to_inner_structure(self):
        return {
            "t_user_info": self.group_list
        }

class GetDomainUserDataSuccess(Response):
    def __init__(self, group_list):
        self.group_list = group_list

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["d_user_info"])
        group_list = data.get("d_user_info")
        return GetDomainUserDataSuccess(group_list)

    def to_inner_structure(self):
        return {
            "d_user_info": self.group_list
        }

class UserReplacementSuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return UserReplacementSuccess()

    def to_inner_structure(self):
        return {}

class CannotRemoveUserTransactionExists(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return CannotRemoveUserTransactionExists()

    def to_inner_structure(self):
        return {
        }

class CheckUserReplacementSuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return CheckUserReplacementSuccess()

    def to_inner_structure(self):
        return {}

class NoTransactionExists(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return NoTransactionExists()

    def to_inner_structure(self):
        return {
        }

def _init_Response_class_map():
    classes = [
        GetUserGroupsSuccess, SaveUserGroupSuccess,
        GroupNameAlreadyExists, UpdateUserGroupSuccess, InvalidUserGroupId,
        ChangeUserGroupStatusSuccess, GetUsersSuccess, SaveUserSuccess,
        EmailIDAlreadyExists, ContactNumberAlreadyExists,
        EmployeeCodeAlreadyExists, InvalidUserId, UpdateUserSuccess,
        ChangeUserStatusSuccess, CannotDeactivateUserExists,
        GetValidityDateListSuccess, SaveValidityDateSettingsSuccess,
        GetUserMappingsSuccess, GetUserMappingsSuccess,
        SaveUserMappingsSuccess, SaveReassignUserAccountSuccess,
        SendRegistraionSuccess,
        GetTechnoUserDataSuccess, GetDomainUserDataSuccess,
        SaveValidityDateSettingsFailure, UserReplacementSuccess, 
        CannotDisableUserTransactionExists, CannotRemoveUserTransactionExists,
        CheckUserMappingsSuccess, CheckUserReplacementSuccess, NoTransactionExists

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
        request = parse_VariantType(
            request, "admin", "Request"
        )
        return RequestFormat(session_token, request)

    def to_structure(self):
        return {
            "session_token": self.session_token,
            "request": to_VariantType(
                self.request, "admin", "Response"
            )
        }


class UserInfo(object):
    def __init__(
        self, user_id, employee_name, country_domains,
        user_category_id, group_ids, entity_ids,
    ):
        self.user_id = user_id
        self.employee_name = employee_name
        self.country_domains = country_domains
        self.user_category_id = user_category_id
        self.group_ids = group_ids
        self.entity_ids = entity_ids

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(
            data, [
                "user_id", "employee_name",
                "country_domains_parent",
                "user_category_id",
                "grp_ids", "le_ids"
            ]
        )
        user_id = data.get("user_id")
        employee_name = data.get("employee_name")
        country_domains = data.get("country_domains_parent")
        user_category_id = data.get("user_category_id")
        group_ids = data.get("grp_ids")
        entity_ids = data.get("le_ids")
        return UserInfo(
            user_id, employee_name, country_domains,
            user_category_id, group_ids, entity_ids
        )

    def to_structure(self):
        return {
            "user_id": self.user_id,
            "employee_name": self.employee_name,
            "country_domains_parent": self.country_domains,
            "user_category_id": self.user_category_id,
            "grp_ids": self.group_ids,
            "le_ids": self.entity_ids
        }

class TechnoEntity(object):
    def __init__(
        self, client_id, client_name, c_id, c_name, d_ids, d_names, le_id, le_name,
        bg_name, executive_id
    ):
        self.client_id = client_id
        self.client_name = client_name
        self.c_id = c_id
        self.c_name = c_name
        self.d_ids = d_ids
        self.d_names = d_names
        self.le_id = le_id
        self.le_name = le_name
        self.bg_name = bg_name
        self.executive_id = executive_id

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "ct_id", "ct_name", "c_id", "c_name", "d_ids", "d_names", "le_id", "le_name",
            "bg_name", "executive_id"
        ])
        client_id = data.get("ct_id")
        client_name = data.get("ct_name")
        country_ids = data.get("c_id")
        country_names = data.get("c_name")
        domain_ids = data.get("d_ids")
        domain_names = data.get("d_names")
        entity_id = data.get("le_id")
        entity_name = data.get("le_name")
        bg_name = data.get("bg_name")
        executive_id = data.get("executive_id")
        return TechnoEntity(
            client_id, client_name, country_ids, country_names, domain_ids,
            domain_names, entity_id, entity_name, bg_name, executive_id
        )

    def to_structure(self):
        return {
            "ct_id": self.client_id,
            "ct_name": self.client_name,
            "c_id": self.c_id,
            "c_name": self.c_name,
            "d_ids": self.d_ids,
            "d_names": self.d_names,
            "le_id": self.le_id,
            "le_name": self.le_name,
            "bg_name": self.bg_name,
            "executive_id": self.executive_id
        }


class DomainUnit(object):
    def __init__(
        self, unit_id, unit_code, unit_name, address,
        location, le_id, le_name, executive_id
    ):
        self.unit_id = unit_id
        self.unit_code = unit_code
        self.unit_name = unit_name
        self.address = address
        self.location = location
        self.le_id = le_id
        self.le_name = le_name
        self.executive_id = executive_id

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "u_id", "u_code", "u_name", "address",
            "location", "le_id", "le_name", "executive_id"
        ])
        return DomainUnit(
            data.get("u_id"), data.get("u_code"), data.get("u_name"), data.get("address"),
            data.get("location"), data.get("le_id"), data.get("le_name"),
            data.get("executive_id")
        )

    def to_structure(self):
        return {
            "u_id" : self.unit_id,
            "u_code" : self.unit_code,
            "u_name" : self.unit_name,
            "address" : self.address,
            "location": self.location,
            "le_id" : self.le_id,
            "le_name" : self.le_name,
            "executive_id": self.executive_id
        }
