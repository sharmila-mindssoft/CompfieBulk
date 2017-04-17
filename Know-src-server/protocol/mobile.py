from protocol.jsonvalidators import (
    parse_dictionary, parse_static_list, to_structure_dictionary_values, parse_VariantType,
    to_VariantType
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

class GetApproveStatutoryMappings(Request):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return GetApproveStatutoryMappings()

    def to_inner_structure(self):
        return {}

class GetComplianceInfo(Request):
    def __init__(self, compliance_id):
        self.compliance_id = compliance_id

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["comp_id"])
        comp_id = data.get("comp_id")
        return GetComplianceInfo(comp_id)

    def to_inner_structure(self):
        return {
            "comp_id": self.compliance_id
        }

class ApproveStatutoryMapping(Request):
    def __init__(self, statutory_mappings):
        self.statutory_mappings = statutory_mappings

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["s_mappings"])
        statutory_mappings = data.get("s_mappings")
        return ApproveStatutoryMapping(statutory_mappings)

    def to_inner_structure(self):
        return {
            "s_mappings": self.statutory_mappings,
        }

def _init_Request_class_map():
    classes = [
        GetApproveStatutoryMappings,
        GetComplianceInfo,
        ApproveStatutoryMapping

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


class UserLoginResponseSuccess(Response):
    def __init__(
        self, user_id, name, session_token
    ):
        self.user_id = user_id
        self.name = name
        self.session_token = session_token

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["user_id", "employee_name", "session_token"])
        user_id = data.get("user_id")
        name = data.get("employee_name")
        session_token = data.get("session_token")
        return UserLoginResponseSuccess(user_id, name, session_token)

    def to_inner_structure(self):
        return {
            "user_id": self.user_id,
            "employee_name": self.name,
            "session_token": self.session_token
        }

class GetApproveStatutoryMappingSuccess(Response):
    def __init__(self, approve_mappings):
        self.approve_mappings = approve_mappings

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["map_list"])
        approve_mappings = data.get("map_list")
        return GetApproveStatutoryMappingSuccess(approve_mappings)

    def to_inner_structure(self):
        return {
            "map_list": self.approve_mappings
        }

class ApproveStatutoryMappingSuccess(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return ApproveStatutoryMappingSuccess()

    def to_inner_structure(self):
        return {
        }


def _init_Response_class_map():
    classes = [
        UserLoginResponseSuccess,
        GetApproveStatutoryMappingSuccess,
        ApproveStatutoryMappingSuccess

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
            request, "mobile", "Request"
        )
        return RequestFormat(session_token, request)

    def to_structure(self):
        return {
            "session_token": self.session_token,
            "request": to_VariantType(
                self.request, "mobile", "Response"
            )
        }

class MappingApproveInfo(object):
    def __init__(
        self, mapping_id, country_name, domain_name,
        nature_name, organisations, mapping_text,
        compliance_list
    ):
        self.mapping_id = mapping_id
        self.country_name = country_name
        self.domain_name = domain_name
        self.nature_name = nature_name
        self.organisations = organisations
        self.mapping_text = mapping_text
        self.compliance_list = compliance_list

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "m_id", "c_name", "d_name",
            "s_n_name", "org_names",
            "map_text", "comp_list"
        ])
        mapping_id = data.get("m_id")
        country_name = data.get("c_name")
        domain_name = data.get("d_name")
        nature_name = data.get("s_n_name")
        organisations = data.get("org_namees")
        mapping_text = data.get("map_text")
        compliance_list = data.get("comp_lists")
        return MappingApproveInfo(
            mapping_id, country_name, domain_name,
            nature_name, organisations, mapping_text,
            compliance_list
        )

    def to_structure(self):
        return {
            "m_id": self.mapping_id,
            "c_name": self.country_name,
            "d_name": self.domain_name,
            "s_n_name": self.nature_name,
            "org_names": self.organisations,
            "map_text": self.mapping_text,
            "comp_lists": self.compliance_list
        }


class MappingComplianceInfo(object):
    def __init__(
        self, compliance_id,
        compliance_task, is_active, created_by, created_on, updated_by,
        updated_on, statutory_provision,
        description,
        penal_consequences,
        frequency, summary, reference, locations
    ):
        self.compliance_id = compliance_id
        self.compliance_task = compliance_task
        self.statutory_provision = statutory_provision
        self.description = description
        self.penal_consequences = penal_consequences
        self.frequency = frequency
        self.summary = summary
        self.reference = reference
        self.locations = locations

        self.is_active = is_active
        self.created_by = created_by
        self.created_on = created_on
        self.updated_by = updated_by
        self.updated_on = updated_on

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "comp_id", "c_task", "is_active",
            "c_by", "c_on", "u_by", "u_on",
            "s_pro", "descrip",
            "p_cons",
            "freq", "summary",
            "refer", "locat"
        ])
        compliance_id = data.get("comp_id")
        compliance_task = data.get("c_task")
        is_active = data.get("is_active")
        created_by = data.get("c_by")
        created_on = data.get("c_on")
        updated_by = data.get("u_by")
        updated_on = data.get("u_on")
        statutory_provision = data.get("s_pro")
        description = data.get("descrip")
        penal_consequences = data.get("p_cons")
        frequency = data.get("freq")
        summary = data.get("summary")
        reference = data.get("refer")
        locations = data.get("locat")

        return MappingComplianceInfo(
            compliance_id,
            compliance_task, is_active, created_by, created_on, updated_by,
            updated_on, statutory_provision,
            description,
            penal_consequences,
            frequency, summary, reference, locations
        )

    def to_structure(self):
        return {
            "comp_id": self.compliance_id,
            "c_task": self.compliance_task,
            "is_active": self.is_active,
            "c_by": self.created_by,
            "c_on": self.created_on,
            "u_by": self.updated_by,
            "u_on": self.updated_on,
            "s_pro": self.statutory_provision,
            "descrip": self.description,
            "p_cons": self.penal_consequences,
            "freq" : self.frequency,
            "summary": self.summary,
            "refer": self.reference,
            "locat": self.locations
        }
