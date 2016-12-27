from distribution.jsonvalidators import (
    parse_dictionary, parse_static_list
)
from distribution.parse_structure import (
    parse_structure_VectorType_RecordType_protocol_Company,
    parse_structure_Text, parse_structure_RecordType_protocol_IPAddress,
    parse_structure_UnsignedIntegerType_32
)
from distribution.to_structure import (
    to_structure_VectorType_RecordType_protocol_Company,
    to_structure_Text, to_structure_RecordType_protocol_IPAddress,
    to_structure_UnsignedIntegerType_32
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
        db_password, db_name, db_ip, company_server_ip
    ):
        self.company_id = company_id
        self.short_url = short_url
        self.db_username = db_username
        self.db_password = db_password
        self.db_name = db_name
        self.db_ip = db_ip
        self.company_server_ip = company_server_ip

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(
            data, [
                "company_id", "short_url", "db_username",
                "db_password", "db_name", "db_ip", "company_server_ip"
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
        return Company(
            company_id, short_url, db_username,
            db_password, db_name, db_ip, company_server_ip
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


def _init_Request_class_map():
    classes = [GetCompanyServerDetails]
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


def _init_Response_class_map():
    classes = [CompanyServerDetails]
    class_map = {}
    for c in classes:
        class_map[c.__name__] = c
    return class_map

_Response_class_map = _init_Response_class_map()
