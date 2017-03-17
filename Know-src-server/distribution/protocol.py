from distribution.jsonvalidators import (
    parse_dictionary, parse_static_list
)
from distribution.parse_structure import (
    parse_structure_VectorType_RecordType_protocol_Company,
    parse_structure_Text, parse_structure_RecordType_protocol_IPAddress,
    parse_structure_UnsignedIntegerType_32, parse_structure_Bool,
    parse_structure_VectorType_RecordType_protocol_FileServer,
    parse_structure_VectorType_RecordType_protocol_Server,
    parse_structure_MapType_CustomeText_VectorType_RecordType_protocol_IPInfo
)
from distribution.to_structure import (
    to_structure_VectorType_RecordType_protocol_Company,
    to_structure_Text, to_structure_RecordType_protocol_IPAddress,
    to_structure_UnsignedIntegerType_32, to_structure_Bool,
    to_structure_VectorType_RecordType_protocol_FileServer,
    to_structure_VectorType_RecordType_protocol_Server,
    to_structure_MapType_CustomeText_VectorType_RecordType_protocol_IPInfo
)

#
# IPAddress
#

class IPAddress(object):
    def __init__(self, ip_address, port):
        self.ip_address = ip_address
        self.port = port

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["ip_address", "port"])
        ip_address = data.get("ip_address")
        ip_address = parse_structure_Text(ip_address)
        port = data.get("port")
        port = parse_structure_UnsignedIntegerType_32(port)
        return IPAddress(ip_address, port)

    def to_structure(self):
        return {
            "ip_address": to_structure_Text(self.ip_address),
            "port": to_structure_UnsignedIntegerType_32(self.port),
        }

#
# Company
#

class Company(object):
    def __init__(
        self,
        company_id, short_url, db_username,
        db_password, db_name, db_ip, company_server_ip,
        is_group
    ):
        self.company_id = company_id
        self.short_url = short_url
        self.db_username = db_username
        self.db_password = db_password
        self.db_name = db_name
        self.db_ip = db_ip
        self.company_server_ip = company_server_ip
        self.is_group = is_group

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(
            data, [
                "company_id", "short_url", "db_username",
                "db_password", "db_name", "db_ip", "company_server_ip",
                "is_group"
            ]
        )
        company_id = data.get("company_id")
        company_id = parse_structure_UnsignedIntegerType_32(company_id)
        short_url = data.get("short_url")
        short_url = parse_structure_Text(short_url)
        db_username = data.get("db_username")
        db_username = parse_structure_Text(db_username)
        db_password = data.get("db_password")
        db_password = parse_structure_Text(db_password)
        db_name = data.get("db_name")
        db_name = parse_structure_Text(db_name)
        db_ip = data.get("db_ip")
        db_ip = parse_structure_RecordType_protocol_IPAddress(db_ip)
        company_server_ip = data.get("company_server_ip")
        company_server_ip = parse_structure_RecordType_protocol_IPAddress(
            company_server_ip
        )
        is_group = data.get("is_group")
        is_group = parse_structure_Bool(is_group)
        return Company(
            company_id, short_url, db_username,
            db_password, db_name, db_ip, company_server_ip,
            is_group
        )

    def to_structure(self):
        return {
            "company_id": to_structure_UnsignedIntegerType_32(self.company_id),
            "short_url": to_structure_Text(self.short_url),
            "db_username": to_structure_Text(self.db_username),
            "db_password": to_structure_Text(self.db_password),
            "db_name": to_structure_Text(self.db_name),
            "db_ip": to_structure_RecordType_protocol_IPAddress(self.db_ip),
            "company_server_ip": to_structure_RecordType_protocol_IPAddress(
                self.company_server_ip
            ),
            "is_group": to_structure_Bool(self.is_group)
        }


class FileServer(object):
    def __init__(self, file_server_ip, legal_entity_id):
        self.file_server_ip = file_server_ip
        self.legal_entity_id = legal_entity_id

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["file_server_ip", "legal_entity_id"])
        file_server_ip = data.get("file_server_ip")
        file_server_ip = parse_structure_RecordType_protocol_IPAddress(file_server_ip)
        legal_entity_id = data.get("legal_entity_id")
        legal_entity_id = parse_structure_UnsignedIntegerType_32(legal_entity_id)
        return FileServer(file_server_ip, legal_entity_id)

    def to_structure(self):
        return {
            "file_server_ip": to_structure_RecordType_protocol_IPAddress(self.file_server_ip),
            "legal_entity_id": to_structure_UnsignedIntegerType_32(self.legal_entity_id)
        }


class Server(object):
    def __init__(self, company_id, short_url, company_server_ip, file_server_info, is_group) :
        self. company_id = company_id
        self.short_url = short_url
        self.company_server_ip = company_server_ip
        self.file_server_info = file_server_info
        self.is_group = is_group

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(
            data, [
                "company_id", "short_url", "company_server_ip", "is_group",
                "file_server_info"
            ]
        )
        company_id = data.get("company_id")
        company_id = parse_structure_UnsignedIntegerType_32(company_id)
        short_url = data.get("short_url")
        short_url = parse_structure_Text(short_url)
        company_server_ip = data.get("company_server_ip")
        company_server_ip = parse_structure_RecordType_protocol_IPAddress(
            company_server_ip
        )
        file_server_info = data.get("file_server_info")
        file_server_info = parse_structure_VectorType_RecordType_protocol_FileServer(file_server_info)
        is_group = data.get("is_group")
        is_group = parse_structure_Bool(is_group)
        return Server(
            company_id, short_url, company_server_ip, file_server_info, is_group
        )

    def to_structure(self):
        return {
            "company_id": to_structure_UnsignedIntegerType_32(self.company_id),
            "short_url": to_structure_Text(self.short_url),
            "company_server_ip": to_structure_RecordType_protocol_IPAddress(self.company_server_ip),
            "is_group": to_structure_Bool(self.is_group),
            "file_server_info": to_structure_VectorType_RecordType_protocol_FileServer(self.file_server_info)
        }

class IPInfo(object):
    def __init__(self, form_name, ip):
        self.form_name = form_name
        self.ip = ip

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["form_name", "ip"])
        form_name = parse_structure_Text(data.get("form_name"))
        # ip = parse_structure_Text(data.get("ip"))
        ip = data.get("ip")
        return IPInfo(form_name, ip)

    def to_structure(self):
        return {
            "form_name": to_structure_Text(self.form_name),
            "ip": self.ip
        }

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

class GetCompanyServerDetails(Request):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return GetCompanyServerDetails()

    def to_inner_structure(self):
        return {
        }

class GetIPDetails(Request):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return GetIPDetails()

    def to_inner_structure(self):
        return {
        }


def _init_Request_class_map():
    classes = [GetCompanyServerDetails, GetIPDetails]
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

class CompanyServerDetails(Response):
    def __init__(self, companies):
        self.companies = companies

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["companies"])
        companies = data.get("companies")
        companies = parse_structure_VectorType_RecordType_protocol_Company(
            companies
        )
        return CompanyServerDetails(companies)

    def to_inner_structure(self):
        return {
            "companies": to_structure_VectorType_RecordType_protocol_Company(
                self.companies
            ),
        }

class ServerDetails(Response):
    def __init__(self, servers, infos):
        self.servers = servers
        self.infos = infos

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["servers", "infos"])
        servers = data.get("servers")
        servers = parse_structure_VectorType_RecordType_protocol_Server(
            servers
        )
        infos = data.get("infos")
        infos = parse_structure_MapType_CustomeText_VectorType_RecordType_protocol_IPInfo(infos)
        return ServerDetails(servers)

    def to_inner_structure(self):
        return {
            "servers": to_structure_VectorType_RecordType_protocol_Server(
                self.servers
            ),
            "infos": to_structure_MapType_CustomeText_VectorType_RecordType_protocol_IPInfo(self.infos)

        }

def _init_Response_class_map():
    classes = [CompanyServerDetails, ServerDetails]
    class_map = {}
    for c in classes:
        class_map[c.__name__] = c
    return class_map

_Response_class_map = _init_Response_class_map()
