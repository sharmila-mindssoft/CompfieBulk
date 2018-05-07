
from clientprotocol.jsonvalidators_client import (
    parse_dictionary, parse_static_list, to_structure_dictionary_values,
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

class GetLegalEntityWiseReportFilters(Request):
    def __init__(self, country_id, legal_entity_id):
        self.country_id = country_id
        self.legal_entity_id = legal_entity_id

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["country_id", "legal_entity_id"])
        country_id = data.get("country_id")
        legal_entity_id = data.get("legal_entity_id")
        return GetLegalEntityWiseReportFilters(country_id, legal_entity_id)

    def to_inner_structure(self):
        return {
            "country_id": self.country_id,
            "legal_entity_id": self.legal_entity_id,
        }

class GetLegalEntityWiseReport(Request):
    def __init__(
        self, country_id, legal_entity_id, domain_id, unit_id, statutory_mapping,
        compliance_task, frequency_id, user_type, user_id, due_from_date,
        due_to_date, task_status, csv, from_count, page_count
    ):
        self.country_id = country_id
        self.legal_entity_id = legal_entity_id
        self.domain_id = domain_id
        self.unit_id = unit_id
        self.statutory_mapping = statutory_mapping
        self.compliance_task = compliance_task
        self.frequency_id = frequency_id
        self.user_type = user_type
        self.user_id = user_id
        self.due_from_date = due_from_date
        self.due_to_date = due_to_date
        self.task_status = task_status
        self.csv = csv
        self.from_count = from_count
        self.page_count = page_count

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "country_id", "legal_entity_id", "domain_id", "unit_id", "statutory_mapping",
            "compliance_task", "frequency_id", "user_type", "user_id", "due_from_date",
            "due_to_date", "task_status", "csv", "from_count", "page_count"
        ])
        country_id = data.get("country_id")
        legal_entity_id = data.get("legal_entity_id")
        domain_id = data.get("domain_id")
        unit_id = data.get("unit_id")
        statutory_mapping = data.get("statutory_mapping")
        compliance_task = data.get("compliance_task")
        frequency_id = data.get("frequency_id")
        user_type = data.get("user_type")
        user_id = data.get("user_id")
        due_from_date = data.get("due_from_date")
        due_to_date = data.get("due_to_date")
        task_status = data.get("task_status")
        csv = data.get("csv")
        from_count = data.get("from_count")
        page_count = data.get("page_count")
        return GetLegalEntityWiseReport(
            country_id, legal_entity_id, domain_id, unit_id, statutory_mapping,
            compliance_task, frequency_id, user_type, user_id, due_from_date,
            due_to_date, task_status, csv, from_count, page_count
        )

    def to_inner_structure(self):
        return {
            "country_id": self.country_id,
            "legal_entity_id": self.legal_entity_id,
            "domain_id": self.domain_id,
            "unit_id": self.unit_id,
            "statutory_mapping": self.statutory_mapping,
            "compliance_task": self.compliance_task,
            "frequency_id": self.frequency_id,
            "user_type": self.user_type,
            "user_id": self.user_id,
            "due_from_date": self.due_from_date,
            "task_status": self.task_status,
            "csv": self.csv,
            "from_count": self.from_count,
            "page_count": self.page_count
        }

class GetDomainWiseReportFilters(Request):
    def __init__(self, country_id, legal_entity_id):
        self.country_id = country_id
        self.legal_entity_id = legal_entity_id

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["country_id", "legal_entity_id"])
        country_id = data.get("country_id")
        legal_entity_id = data.get("legal_entity_id")
        return GetDomainWiseReportFilters(country_id, legal_entity_id)

    def to_inner_structure(self):
        return {
            "country_id": self.country_id,
            "legal_entity_id": self.legal_entity_id,
        }

class GetDomainWiseReport(Request):
    def __init__(
        self, country_id, legal_entity_id, domain_id, unit_id, statutory_mapping,
        compliance_task, frequency_id, user_type, user_id, due_from_date,
        due_to_date, task_status, csv, from_count, page_count
    ):
        self.country_id = country_id
        self.legal_entity_id = legal_entity_id
        self.domain_id = domain_id
        self.unit_id = unit_id
        self.statutory_mapping = statutory_mapping
        self.compliance_task = compliance_task
        self.frequency_id = frequency_id
        self.user_type = user_type
        self.user_id = user_id
        self.due_from_date = due_from_date
        self.due_to_date = due_to_date
        self.task_status = task_status
        self.csv = csv
        self.from_count = from_count
        self.page_count = page_count

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "country_id", "legal_entity_id", "domain_id", "unit_id", "statutory_mapping",
            "compliance_task", "frequency_id", "user_type", "user_id", "due_from_date",
            "due_to_date", "task_status", "csv", "from_count", "page_count"
        ])
        country_id = data.get("country_id")
        legal_entity_id = data.get("legal_entity_id")
        domain_id = data.get("domain_id")
        unit_id = data.get("unit_id")
        statutory_mapping = data.get("statutory_mapping")
        compliance_task = data.get("compliance_task")
        frequency_id = data.get("frequency_id")
        user_type = data.get("user_type")
        user_id = data.get("user_id")
        due_from_date = data.get("due_from_date")
        due_to_date = data.get("due_to_date")
        task_status = data.get("task_status")
        csv = data.get("csv")
        from_count = data.get("from_count")
        page_count = data.get("page_count")
        return GetDomainWiseReport(
            country_id, legal_entity_id, domain_id, unit_id, statutory_mapping,
            compliance_task, frequency_id, user_type, user_id, due_from_date,
            due_to_date, task_status, csv, from_count, page_count
        )

    def to_inner_structure(self):
        return {
            "country_id": self.country_id,
            "legal_entity_id": self.legal_entity_id,
            "domain_id": self.domain_id,
            "unit_id": self.unit_id,
            "statutory_mapping": self.statutory_mapping,
            "compliance_task": self.compliance_task,
            "frequency_id": self.frequency_id,
            "user_type": self.user_type,
            "user_id": self.user_id,
            "due_from_date": self.due_from_date,
            "task_status": self.task_status,
            "csv": self.csv,
            "from_count": self.from_count,
            "page_count": self.page_count
        }

class GetUnitWiseReportFilters(Request):
    def __init__(self, country_id, legal_entity_id):
        self.country_id = country_id
        self.legal_entity_id = legal_entity_id

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["country_id", "legal_entity_id"])
        country_id = data.get("country_id")
        legal_entity_id = data.get("legal_entity_id")
        return GetUnitWiseReportFilters(country_id, legal_entity_id)

    def to_inner_structure(self):
        return {
            "country_id": self.country_id,
            "legal_entity_id": self.legal_entity_id,
        }

class GetUnitWiseReport(Request):
    def __init__(
        self, country_id, legal_entity_id, unit_id, d_id_optional, statutory_mapping,
        compliance_task, frequency_id, user_type, user_id, due_from_date,
        due_to_date, task_status, csv, from_count, page_count
    ):
        self.country_id = country_id
        self.legal_entity_id = legal_entity_id
        self.unit_id = unit_id
        self.d_id_optional = d_id_optional
        self.statutory_mapping = statutory_mapping
        self.compliance_task = compliance_task
        self.frequency_id = frequency_id
        self.user_type = user_type
        self.user_id = user_id
        self.due_from_date = due_from_date
        self.due_to_date = due_to_date
        self.task_status = task_status
        self.csv = csv
        self.from_count = from_count
        self.page_count = page_count

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "country_id", "legal_entity_id", "unit_id", "d_id_optional", "statutory_mapping",
            "compliance_task", "frequency_id", "user_type", "user_id", "due_from_date",
            "due_to_date", "task_status", "csv", "from_count", "page_count"
        ])
        country_id = data.get("country_id")
        legal_entity_id = data.get("legal_entity_id")
        unit_id = data.get("unit_id")
        d_id_optional = data.get("d_id_optional")
        statutory_mapping = data.get("statutory_mapping")
        compliance_task = data.get("compliance_task")
        frequency_id = data.get("frequency_id")
        user_type = data.get("user_type")
        user_id = data.get("user_id")
        due_from_date = data.get("due_from_date")
        due_to_date = data.get("due_to_date")
        task_status = data.get("task_status")
        csv = data.get("csv")
        from_count = data.get("from_count")
        page_count = data.get("page_count")
        return GetUnitWiseReport(
            country_id, legal_entity_id, unit_id, d_id_optional, statutory_mapping,
            compliance_task, frequency_id, user_type, user_id, due_from_date,
            due_to_date, task_status, csv, from_count, page_count
        )

    def to_inner_structure(self):
        return {
            "country_id": self.country_id,
            "legal_entity_id": self.legal_entity_id,
            "unit_id": self.unit_id,
            "d_id_optional": self.d_id_optional,
            "statutory_mapping": self.statutory_mapping,
            "compliance_task": self.compliance_task,
            "frequency_id": self.frequency_id,
            "user_type": self.user_type,
            "user_id": self.user_id,
            "due_from_date": self.due_from_date,
            "due_to_date": self.due_to_date,
            "task_status": self.task_status,
            "csv": self.csv,
            "from_count": self.from_count,
            "page_count": self.page_count
        }

class GetServiceProviderWiseReportFilters(Request):
    def __init__(self, country_id, legal_entity_id):
        self.country_id = country_id
        self.legal_entity_id = legal_entity_id

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["country_id", "legal_entity_id"])
        country_id = data.get("country_id")
        legal_entity_id = data.get("legal_entity_id")
        return GetServiceProviderWiseReportFilters(country_id, legal_entity_id)

    def to_inner_structure(self):
        return {
            "country_id": self.country_id,
            "legal_entity_id": self.legal_entity_id,
        }

class GetServiceProviderWiseReport(Request):
    def __init__(
        self, country_id, legal_entity_id, sp_id, domain_id, unit_id,
        statutory_mapping, compliance_task, user_id, due_from_date,
        due_to_date, task_status, csv, from_count, page_count
    ):
        self.country_id = country_id
        self.legal_entity_id = legal_entity_id
        self.sp_id = sp_id
        self.domain_id = domain_id
        self.unit_id = unit_id
        self.statutory_mapping = statutory_mapping
        self.compliance_task = compliance_task
        self.user_id = user_id
        self.due_from_date = due_from_date
        self.due_to_date = due_to_date
        self.task_status = task_status
        self.csv = csv
        self.from_count = from_count
        self.page_count = page_count

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "country_id", "legal_entity_id", "sp_id", "domain_id", "unit_id",
            "statutory_mapping", "compliance_task", "user_id", "due_from_date",
            "due_to_date", "task_status", "csv", "from_count", "page_count"
        ])
        country_id = data.get("country_id")
        legal_entity_id = data.get("legal_entity_id")
        sp_id = data.get("sp_id")
        domain_id = data.get("domain_id")
        unit_id = data.get("unit_id")
        statutory_mapping = data.get("statutory_mapping")
        compliance_task = data.get("compliance_task")
        user_id = data.get("user_id")
        due_from_date = data.get("due_from_date")
        due_to_date = data.get("due_to_date")
        task_status = data.get("task_status")
        csv = data.get("csv")
        from_count = data.get("from_count")
        page_count = data.get("page_count")
        return GetServiceProviderWiseReport(
            country_id, legal_entity_id, sp_id, domain_id, unit_id,
            statutory_mapping, compliance_task, user_id, due_from_date,
            due_to_date, task_status, csv, from_count, page_count
        )

    def to_inner_structure(self):
        return {
            "country_id": self.country_id,
            "legal_entity_id": self.legal_entity_id,
            "sp_id": self.sp_id,
            "domain_id": self.domain_id,
            "unit_id": self.unit_id,
            "statutory_mapping": self.statutory_mapping,
            "compliance_task": self.compliance_task,
            "user_id": self.user_id,
            "due_from_date": self.due_from_date,
            "due_to_date": self.due_to_date,
            "task_status": self.task_status,
            "csv": self.csv,
            "from_count": self.from_count,
            "page_count": self.page_count
        }

class GetUserWiseReportFilters(Request):
    def __init__(self, country_id, legal_entity_id):
        self.country_id = country_id
        self.legal_entity_id = legal_entity_id

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["country_id", "legal_entity_id"])
        country_id = data.get("country_id")
        legal_entity_id = data.get("legal_entity_id")
        return GetUserWiseReportFilters(country_id, legal_entity_id)

    def to_inner_structure(self):
        return {
            "country_id": self.country_id,
            "legal_entity_id": self.legal_entity_id,
        }

class GetUserWiseReport(Request):
    def __init__(
        self, country_id, legal_entity_id, user_id, domain_id, unit_id,
        statutory_mapping, compliance_task, frequency_id, user_type, due_from_date,
        due_to_date, task_status, csv, from_count, page_count
    ):
        self.country_id = country_id
        self.legal_entity_id = legal_entity_id
        self.user_id = user_id
        self.domain_id = domain_id
        self.unit_id = unit_id
        self.statutory_mapping = statutory_mapping
        self.compliance_task = compliance_task
        self.frequency_id = frequency_id
        self.user_type = user_type
        self.due_from_date = due_from_date
        self.due_to_date = due_to_date
        self.task_status = task_status
        self.csv = csv
        self.from_count = from_count
        self.page_count = page_count

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "country_id", "legal_entity_id", "user_id", "domain_id", "unit_id",
            "statutory_mapping", "compliance_task", "frequency_id", "user_type",
            "due_from_date", "due_to_date", "task_status", "csv", "from_count",
            "page_count"
        ])
        country_id = data.get("country_id")
        legal_entity_id = data.get("legal_entity_id")
        user_id = data.get("user_id")
        domain_id = data.get("domain_id")
        unit_id = data.get("unit_id")
        statutory_mapping = data.get("statutory_mapping")
        compliance_task = data.get("compliance_task")
        frequency_id = data.get("frequency_id")
        user_type = data.get("user_type")
        due_from_date = data.get("due_from_date")
        due_to_date = data.get("due_to_date")
        task_status = data.get("task_status")
        csv = data.get("csv")
        from_count = data.get("from_count")
        page_count = data.get("page_count")
        return GetUserWiseReport(
            country_id, legal_entity_id, user_id, domain_id, unit_id,
            statutory_mapping, compliance_task, frequency_id, user_type,
            due_from_date, due_to_date, task_status, csv, from_count, page_count
        )

    def to_inner_structure(self):
        return {
            "country_id": self.country_id,
            "legal_entity_id": self.legal_entity_id,
            "user_id": self.user_id,
            "domain_id": self.domain_id,
            "unit_id": self.unit_id,
            "statutory_mapping": self.statutory_mapping,
            "compliance_task": self.compliance_task,
            "frequency_id": self.frequency_id,
            "user_type": self.user_type,
            "due_from_date": self.due_from_date,
            "due_to_date": self.due_to_date,
            "task_status": self.task_status,
            "csv": self.csv,
            "from_count": self.from_count,
            "page_count": self.page_count
        }

class GetUnitListReportFilters(Request):
    def __init__(self, country_id, business_group_id, legal_entity_id):
        self.country_id = country_id
        self.business_group_id = business_group_id
        self.legal_entity_id = legal_entity_id

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["country_id", "business_group_id", "legal_entity_id"])
        country_id = data.get("country_id")
        business_group_id = data.get("business_group_id")
        legal_entity_id = data.get("legal_entity_id")
        return GetUnitListReportFilters(country_id, business_group_id, legal_entity_id)

    def to_inner_structure(self):
        return {
            "country_id": self.country_id,
            "business_group_id": self.business_group_id,
            "legal_entity_id": self.legal_entity_id,
        }

class GetUnitListReport(Request):
    def __init__(
        self, country_id, business_group_id, legal_entity_id, division_id,
        category_id, unit_id, domain_id, organisation_id, unit_status,
        csv, from_count, page_count
    ):
        self.country_id = country_id
        self.business_group_id = business_group_id
        self.legal_entity_id = legal_entity_id
        self.division_id = division_id
        self.category_id = category_id
        self.unit_id = unit_id
        self.domain_id = domain_id
        self.organisation_id = organisation_id
        self.unit_status = unit_status
        self.csv = csv
        self.from_count = from_count
        self.page_count = page_count

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "country_id", "business_group_id", "legal_entity_id", "division_id",
            "category_id", "unit_id", "domain_id", "organisation_id", "unit_status",
            "csv", "from_count", "page_count"
        ])
        country_id = data.get("country_id")
        business_group_id = data.get("business_group_id")
        legal_entity_id = data.get("legal_entity_id")
        division_id = data.get("division_id")
        category_id = data.get("category_id")
        unit_id = data.get("unit_id")
        domain_id = data.get("domain_id")
        organisation_id = data.get("organisation_id")
        unit_status = data.get("unit_status")
        csv = data.get("csv")
        from_count = data.get("from_count")
        page_count = data.get("page_count")
        return GetUnitListReport(
            country_id, business_group_id, legal_entity_id, division_id, category_id,
            unit_id, domain_id, organisation_id, unit_status, csv, from_count, page_count
        )

    def to_inner_structure(self):
        return {
            "country_id": self.country_id,
            "business_group_id": self.business_group_id,
            "legal_entity_id": self.legal_entity_id,
            "division_id": self.division_id,
            "category_id": self.category_id,
            "unit_id": self.unit_id,
            "domain_id": self.domain_id,
            "organisation_id": self.organisation_id,
            "unit_status": self.unit_status,
            "csv": self.csv,
            "from_count": self.from_count,
            "page_count": self.page_count
        }

class GetStatutoryNotificationsListReportFilters(Request):
    def __init__(self, country_id, legal_entity_id):
        self.country_id = country_id
        self.legal_entity_id = legal_entity_id

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["country_id", "legal_entity_id"])
        country_id = data.get("country_id")
        legal_entity_id = data.get("legal_entity_id")
        return GetStatutoryNotificationsListReportFilters(country_id, legal_entity_id)

    def to_inner_structure(self):
        return {
            "country_id": self.country_id,
            "legal_entity_id": self.legal_entity_id,
        }

class GetStatutoryNotificationsListReportData(Request):
    def __init__(
        self, country_id, legal_entity_id, domain_id, statutory_mapping,
        due_from_date, due_to_date, csv, from_count, page_count
    ):
        self.country_id = country_id
        self.legal_entity_id = legal_entity_id
        self.domain_id = domain_id
        self.statutory_mapping = statutory_mapping
        self.due_from_date = due_from_date
        self.due_to_date = due_to_date
        self.csv = csv
        self.from_count = from_count
        self.page_count = page_count

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "country_id", "legal_entity_id", "domain_id", "statutory_mapping",
            "due_from_date", "due_to_date", "csv", "from_count", "page_count"
        ])
        country_id = data.get("country_id")
        legal_entity_id = data.get("legal_entity_id")
        domain_id = data.get("domain_id")
        statutory_mapping = data.get("statutory_mapping")
        due_from_date = data.get("due_from_date")
        due_to_date = data.get("due_to_date")
        csv = data.get("csv")
        from_count = data.get("from_count")
        page_count = data.get("page_count")
        return GetStatutoryNotificationsListReportData(
            country_id, legal_entity_id, domain_id, statutory_mapping,
            due_from_date, due_to_date, csv, from_count, page_count
        )

    def to_inner_structure(self):
        return {
            "country_id": self.country_id,
            "legal_entity_id": self.legal_entity_id,
            "domain_id": self.domain_id,
            "statutory_mapping": self.statutory_mapping,
            "due_from_date": self.due_from_date,
            "due_to_date": self.due_to_date,
            "csv": self.csv,
            "from_count": self.from_count,
            "page_count": self.page_count
        }

class GetAuditTrailReportData(Request):
    def __init__(
        self, legal_entity_id, user_id, form_id_optional, due_from_date, due_to_date,
        csv, from_count, page_count, check_count
    ):
        self.legal_entity_id = legal_entity_id
        self.user_id = user_id
        self.form_id_optional = form_id_optional
        self.due_from_date = due_from_date
        self.due_to_date = due_to_date
        self.csv = csv
        self.from_count = from_count
        self.page_count = page_count
        self.check_count = check_count

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "legal_entity_id", "user_id", "form_id_optional", "due_from_date", "due_to_date",
            "csv", "from_count", "page_count", "check_count"
        ])
        legal_entity_id = data.get("legal_entity_id")
        user_id = data.get("user_id")
        form_id_optional = data.get("form_id_optional")
        due_from_date = data.get("due_from_date")
        due_to_date = data.get("due_to_date")
        csv = data.get("csv")
        from_count = data.get("from_count")
        page_count = data.get("page_count")
        check_count = data.get("check_count")
        return GetAuditTrailReportData(
            legal_entity_id, user_id, form_id_optional, due_from_date, due_to_date,
            csv, from_count, page_count, check_count
        )

    def to_inner_structure(self):
        return {
            "legal_entity_id": self.legal_entity_id,
            "user_id": self.user_id,
            "form_id_optional": self.form_id_optional,
            "due_from_date": self.due_from_date,
            "due_to_date": self.due_to_date,
            "csv": self.csv,
            "from_count": self.from_count,
            "page_count": self.page_count,
            "check_count": self.check_count,
        }

class GetRiskReportFilters(Request):
    def __init__(self, country_id, business_group_id, legal_entity_id):
        self.country_id = country_id
        self.business_group_id = business_group_id
        self.legal_entity_id = legal_entity_id

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["country_id", "business_group_id", "legal_entity_id"])
        country_id = data.get("country_id")
        business_group_id = data.get("business_group_id")
        legal_entity_id = data.get("legal_entity_id")
        return GetRiskReportFilters(country_id, business_group_id, legal_entity_id)

    def to_inner_structure(self):
        return {
            "country_id": self.country_id,
            "business_group_id": self.business_group_id,
            "legal_entity_id": self.legal_entity_id,
        }

class GetRiskReportData(Request):
    def __init__(
        self, country_id, business_group_id, legal_entity_id, domain_id, division_id,
        category_id, unit_id, statutory_mapping, compliance_task, task_status,
        csv, from_count, page_count
    ):
        self.country_id = country_id
        self.business_group_id = business_group_id
        self.legal_entity_id = legal_entity_id
        self.domain_id = domain_id
        self.division_id = division_id
        self.category_id = category_id
        self.unit_id = unit_id
        self.statutory_mapping = statutory_mapping
        self.compliance_task = compliance_task
        self.task_status = task_status
        self.csv = csv
        self.from_count = from_count
        self.page_count = page_count

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "country_id", "business_group_id", "legal_entity_id", "domain_id", "division_id",
            "category_id", "unit_id", "statutory_mapping", "compliance_task", "task_status",
            "csv", "from_count", "page_count"
        ])
        country_id = data.get("country_id")
        business_group_id = data.get("business_group_id")
        legal_entity_id = data.get("legal_entity_id")
        domain_id = data.get("domain_id")
        division_id = data.get("division_id")
        category_id = data.get("category_id")
        unit_id = data.get("unit_id")
        statutory_mapping = data.get("statutory_mapping")
        compliance_task = data.get("compliance_task")
        task_status = data.get("task_status")
        csv = data.get("csv")
        from_count = data.get("from_count")
        page_count = data.get("page_count")
        return GetRiskReportData(
            country_id, business_group_id, legal_entity_id, domain_id, division_id, category_id,
            unit_id, statutory_mapping, compliance_task, task_status, csv, from_count, page_count
        )

    def to_inner_structure(self):
        return {
            "country_id": self.country_id,
            "business_group_id": self.business_group_id,
            "legal_entity_id": self.legal_entity_id,
            "domain_id": self.domain_id,
            "unit_id": self.unit_id,
            "statutory_mapping": self.statutory_mapping,
            "compliance_task": self.compliance_task,
            "frequency_id": self.frequency_id,
            "user_type": self.user_type,
            "user_id": self.user_id,
            "due_from_date": self.due_from_date,
            "task_status": self.task_status,
            "csv": self.csv,
            "from_count": self.from_count,
            "page_count": self.page_count
        }


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

class GetComplianceDetailsReportFiltersSuccess(Response):
    def __init__(self, countries, domains, level_1_statutories, units, Compliances, users):
        self.countries = countries
        self.domains = domains
        self.level_1_statutories = level_1_statutories
        self.units = units
        self.Compliances = Compliances
        self.users = users

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["countries", "domains", "level_1_statutories", "units", "compliances", "users"])
        countries = data.get("countries")
        countries = parse_structure_VectorType_RecordType_core_Country(countries)
        domains = data.get("domains")
        domains = parse_structure_VectorType_RecordType_core_Domain(domains)
        level_1_statutories = data.get("level_1_statutories")
        level_1_statutories = parse_structure_VectorType_CustomTextType_100(level_1_statutories)
        units = data.get("units")
        units = parse_structure_VectorType_RecordType_core_ClientUnit(units)
        Compliances = data.get("compliances")
        Compliances = parse_structure_VectorType_RecordType_core_ComplianceFilter(Compliances)
        users = data.get("users")
        users = parse_structure_VectorType_RecordType_clientreport_User(users)
        return GetComplianceDetailsReportFiltersSuccess(countries, domains, level_1_statutories, units, Compliances, users)

    def to_inner_structure(self):
        return {
            "countries": to_structure_VectorType_RecordType_core_Country(self.countries),
            "domains": to_structure_VectorType_RecordType_core_Domain(self.domains),
            "level_1_statutories": to_structure_VectorType_CustomTextType_100(self.level_1_statutories),
            "units": to_structure_VectorType_RecordType_core_ClientUnit(self.units),
            "compliances": to_structure_VectorType_RecordType_core_ComplianceFilter(self.Compliances),
            "users": to_structure_VectorType_RecordType_clientreport_User(self.users),
        }

class GetLegalEntityWiseReportFiltersSuccess(Response):
    def __init__(
        self, domains, unit_legal_entity, act_legal_entity,
        compliance_frequency_list, compliance_user_type, compliance_task_status,
        compliance_users
    ):
        self.domains = domains
        self.unit_legal_entity = unit_legal_entity
        self.act_legal_entity = act_legal_entity
        self.compliance_frequency_list = compliance_frequency_list
        self.compliance_user_type = compliance_user_type
        self.compliance_task_status = compliance_task_status
        self.compliance_users = compliance_users

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "domains", "unit_legal_entity", "act_legal_entity",
            "compliance_frequency_list", "compliance_user_type", "compliance_task_status",
            "compliance_users"
        ])
        domains = data.get("domains")
        unit_legal_entity = data.get("unit_legal_entity")
        act_legal_entity = data.get("act_legal_entity")
        compliance_frequency_list = data.get("compliance_frequency_list")
        compliance_user_type = data.get("compliance_user_type")
        compliance_task_status = data.get("compliance_task_status")
        compliance_users = data.get("compliance_users")
        return GetLegalEntityWiseReportFiltersSuccess(
            domains, unit_legal_entity, act_legal_entity,
            compliance_frequency_list, compliance_user_type, compliance_task_status,
            compliance_users
        )

    def to_inner_structure(self):
        data = {
            "domains": self.domains,
            "unit_legal_entity": self.unit_legal_entity,
            "act_legal_entity": self.act_legal_entity,
            "compliance_frequency_list": self.compliance_frequency_list,
            "compliance_user_type": self.compliance_user_type,
            "compliance_task_status": self.compliance_task_status,
            "compliance_users": self.compliance_users
        }
        return data

class GetLegalEntityWiseReportSuccess(Response):
    def __init__(
        self, legal_entities_compliances, total_count
    ):
        self.legal_entities_compliances = legal_entities_compliances
        self.total_count = total_count

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["legal_entities_compliances", "total_count"])
        legal_entities_compliances = data.get("legal_entities_compliances")
        total_count = data.get("total_count")
        return GetLegalEntityWiseReportSuccess(
            legal_entities_compliances, total_count
        )

    def to_inner_structure(self):
        data = {
            "legal_entities_compliances": self.legal_entities_compliances,
            "total_count": self.total_count
        }
        return data

class GetDomainWiseReportFiltersSuccess(Response):
    def __init__(
        self, domains, unit_legal_entity, act_legal_entity,
        compliance_frequency_list, compliance_user_type, compliance_task_status,
        compliance_users
    ):
        self.domains = domains
        self.unit_legal_entity = unit_legal_entity
        self.act_legal_entity = act_legal_entity
        self.compliance_frequency_list = compliance_frequency_list
        self.compliance_user_type = compliance_user_type
        self.compliance_task_status = compliance_task_status
        self.compliance_users = compliance_users

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "domains", "unit_legal_entity", "act_legal_entity",
            "compliance_frequency_list", "compliance_user_type", "compliance_task_status",
            "compliance_users"
        ])
        domains = data.get("domains")
        unit_legal_entity = data.get("unit_legal_entity")
        act_legal_entity = data.get("act_legal_entity")
        compliance_frequency_list = data.get("compliance_frequency_list")
        compliance_user_type = data.get("compliance_user_type")
        compliance_task_status = data.get("compliance_task_status")
        compliance_users = data.get("compliance_users")
        return GetDomainWiseReportFiltersSuccess(
            domains, unit_legal_entity, act_legal_entity,
            compliance_frequency_list, compliance_user_type, compliance_task_status,
            compliance_users
        )

    def to_inner_structure(self):
        data = {
            "domains": self.domains,
            "unit_legal_entity": self.unit_legal_entity,
            "act_legal_entity": self.act_legal_entity,
            "compliance_frequency_list": self.compliance_frequency_list,
            "compliance_user_type": self.compliance_user_type,
            "compliance_task_status": self.compliance_task_status,
            "compliance_users": self.compliance_users
        }
        return data

class GetDomainWiseReportSuccess(Response):
    def __init__(
        self, legal_entities_compliances,  total_count
    ):
        self.legal_entities_compliances = legal_entities_compliances
        self.total_count = total_count

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["legal_entities_compliances", "total_count"])
        legal_entities_compliances = data.get("legal_entities_compliances")
        total_count = data.get("total_count")
        return GetDomainWiseReportSuccess(
            legal_entities_compliances, total_count
        )

    def to_inner_structure(self):
        data = {
            "legal_entities_compliances": self.legal_entities_compliances,
            "total_count": self.total_count
        }
        return data

class GetUnitWiseReportSuccess(Response):
    def __init__(
        self, unit_compliances, total_count
    ):
        self.unit_compliances = unit_compliances
        self.total_count = total_count

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["unit_compliances", "total_count"])
        unit_compliances = data.get("unit_compliances")
        total_count = data.get("total_count")
        return GetUnitWiseReportSuccess(
            unit_compliances, total_count
        )

    def to_inner_structure(self):
        data = {
            "unit_compliances": self.unit_compliances,
            "total_count": self.total_count
        }
        return data

class ComplianceDetailsUnitWise(object):
    def __init__(self, unit_id, unit_name, address, Compliances):
        self.unit_id = unit_id
        self.unit_name = unit_name
        self.address = address
        self.Compliances = Compliances

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["unit_id", "unit_name", "address", "compliances"])
        unit_id = data.get("unit_id")
        unit_id = parse_structure_UnsignedIntegerType_32(unit_id)
        unit_name = data.get("unit_name")
        unit_name = parse_structure_CustomTextType_100(unit_name)
        address = data.get("address")
        address = parse_structure_CustomTextType_250(address)
        Compliances = data.get("compliances")
        Compliances = parse_structure_VectorType_RecordType_clientreport_ComplianceDetails(Compliances)
        return ComplianceDetailsUnitWise(unit_id, unit_name, address, Compliances)

    def to_inner_structure(self):
        result = {
            "unit_id": to_structure_SignedIntegerType_8(self.unit_id),
            "unit_name": to_structure_CustomTextType_100(self.unit_name),
            "address": to_structure_CustomTextType_250(self.address),
            "compliances": to_structure_VectorType_RecordType_clientreport_ComplianceDetails(self.Compliances),
        }

        return result

class GetUnitWiseReportFiltersSuccess(Response):
    def __init__(
        self, domains, unit_legal_entity, act_legal_entity,
        compliance_frequency_list, compliance_user_type, compliance_task_status,
        compliance_users
    ):
        self.domains = domains
        self.unit_legal_entity = unit_legal_entity
        self.act_legal_entity = act_legal_entity
        self.compliance_frequency_list = compliance_frequency_list
        self.compliance_user_type = compliance_user_type
        self.compliance_task_status = compliance_task_status
        self.compliance_users = compliance_users

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "domains", "unit_legal_entity", "act_legal_entity",
            "compliance_frequency_list", "compliance_user_type", "compliance_task_status",
            "compliance_users"
        ])
        domains = data.get("domains")
        unit_legal_entity = data.get("unit_legal_entity")
        act_legal_entity = data.get("act_legal_entity")
        compliance_frequency_list = data.get("compliance_frequency_list")
        compliance_user_type = data.get("compliance_user_type")
        compliance_task_status = data.get("compliance_task_status")
        compliance_users = data.get("compliance_users")
        return GetUnitWiseReportFiltersSuccess(
            domains, unit_legal_entity, act_legal_entity,
            compliance_frequency_list, compliance_user_type, compliance_task_status,
            compliance_users
        )

    def to_inner_structure(self):
        data = {
            "domains": self.domains,
            "unit_legal_entity": self.unit_legal_entity,
            "act_legal_entity": self.act_legal_entity,
            "compliance_frequency_list": self.compliance_frequency_list,
            "compliance_user_type": self.compliance_user_type,
            "compliance_task_status": self.compliance_task_status,
            "compliance_users": self.compliance_users
        }
        return data

class GetComplianceDetailsReportSuccess(Response):
    def __init__(self, unit_wise_compliancess, total_count):
        self.unit_wise_compliancess = unit_wise_compliancess
        self.total_count = total_count

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["unit_wise_compliancess", "total_count"])
        unit_wise_compliances = data.get("unit_wise_compliances")
        unit_wise_compliances = parse_structure_VectorType_RecordType_clientreport_ComplianceDetailsUnitWise(unit_wise_compliances)
        total_count = data.get("total_count")
        total_count = parse_structure_UnsignedIntegerType_32(total_count)
        return GetComplianceDetailsReportSuccess(unit_wise_compliances, total_count)

    def to_inner_structure(self):
        return {
            "unit_wise_compliancess": to_structure_VectorType_RecordType_clientreport_ComplianceDetailsUnitWise(self.unit_wise_compliancess),
            "total_count": to_structure_UnsignedIntegerType_32(self.total_count)
        }


class GetServiceProviderReportFiltersSuccess(Response):
    def __init__(self, countries, domains, level_1_statutories, units, service_providers):
        self.countries = countries
        self.domains = domains
        self.level_1_statutories = level_1_statutories
        self.units = units
        self.service_providers = service_providers

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["countries", "domains", "level_1_statutories", "units", "service_providers"])
        countries = data.get("countries")
        countries = parse_structure_VectorType_RecordType_core_Country(countries)
        domains = data.get("domains")
        domains = parse_structure_VectorType_RecordType_core_Domain(domains)
        level_1_statutories = data.get("level_1_statutories")
        level_1_statutories = parse_structure_VectorType_CustomTextType_100(level_1_statutories)
        units = data.get("units")
        units = parse_structure_VectorType_RecordType_core_ClientUnit(units)
        service_providers = data.get("service_providers")
        service_providers = parse_structure_VectorType_RecordType_core_ServiceProvider(service_providers)
        return GetServiceProviderReportFiltersSuccess(countries, domains, level_1_statutories, units, service_providers)

    def to_inner_structure(self):
        return {
            "countries": to_structure_VectorType_RecordType_core_Country(self.countries),
            "domains": to_structure_VectorType_RecordType_core_Domain(self.domains),
            "level_1_statutories": to_structure_VectorType_CustomTextType_100(self.level_1_statutories),
            "units": to_structure_VectorType_RecordType_core_ClientUnit(self.units),
            "service_providers": to_structure_VectorType_RecordType_core_ServiceProvider(self.service_providers),
        }

class GetServiceProviderWiseComplianceSuccess(Response):
    def __init__(self, compliance_list, total_count):
        self.compliance_list = compliance_list
        self.total_count = total_count

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["compliance_list", "total_count"])
        compliance_list = data.get("compliance_list")
        compliance_list = parse_structure_VectorType_RecordType_clientreport_ServiceProviderCompliance(compliance_list)
        total_count = data.get("total_count")
        total_count = parse_structure_UnsignedIntegerType_32(total_count)
        return GetServiceProviderWiseComplianceSuccess(compliance_list, total_count)

    def to_inner_structure(self):
        return {
            "compliance_list": to_structure_VectorType_RecordType_clientreport_ServiceProviderCompliance(self.compliance_list),
            "total_count": to_structure_UnsignedIntegerType_32(self.total_count)
        }

class GetClientReportFiltersSuccess(Response):
    def __init__(self, countries, domains, business_groups, legal_entities, divisions, units, users):
        self.countries = countries
        self.domains = domains
        self.business_groups = business_groups
        self.legal_entities = legal_entities
        self.divisions = divisions
        self.units = units
        self.users = users

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["countries", "domains", "business_groups", "legal_entities", "divisions", "units", "users"])
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
        units = parse_structure_VectorType_RecordType_core_ClientUnit(units)
        users = data.get("users")
        users = parse_structure_VectorType_RecordType_clientreport_User(users)
        return GetClientReportFiltersSuccess(countries, domains, business_groups, legal_entities, divisions, units, users)

    def to_inner_structure(self):
        return {
            "countries": to_structure_VectorType_RecordType_core_Country(self.countries),
            "domains": to_structure_VectorType_RecordType_core_Domain(self.domains),
            "business_groups": to_structure_VectorType_RecordType_core_ClientBusinessGroup(self.business_groups),
            "legal_entities": to_structure_VectorType_RecordType_core_ClientLegalEntity(self.legal_entities),
            "divisions": to_structure_VectorType_RecordType_core_ClientDivision(self.divisions),
            "units": to_structure_VectorType_RecordType_core_ClientUnit(self.units),
            "users": to_structure_VectorType_RecordType_clientreport_User(self.users),
        }

class GetAssigneewisecomplianceReportSuccess(Response):
    def __init__(self, compliance_list, total_count):
        self.compliance_list = compliance_list
        self.total_count = total_count

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["compliance_list", "total_count"])
        compliance_list = data.get("compliance_list")
        compliance_list = parse_structure_VectorType_RecordType_clientreport_AssigneeCompliance(compliance_list)
        total_count = data.get("total_count")
        total_count = parse_structure_UnsignedIntegerType_32(total_count)
        return GetAssigneewisecomplianceReportSuccess(compliance_list, total_count)

    def to_inner_structure(self):
        return {
            "compliance_list": to_structure_VectorType_RecordType_clientreport_AssigneeCompliance(self.compliance_list),
            "total_count": to_structure_UnsignedIntegerType_32(self.total_count)
        }

class GetUnitwisecomplianceReportSuccess(Response):
    def __init__(self, compliance_list, total_count):
        self.compliance_list = compliance_list
        self.total_count = total_count

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["compliance_list", "total_count"])
        compliance_list = data.get("compliance_list")
        compliance_list = parse_structure_VectorType_RecordType_clientreport_UnitCompliance(compliance_list)
        total_count = data.get("total_count")
        total_count = parse_structure_UnsignedIntegerType_32(total_count)
        return GetUnitwisecomplianceReportSuccess(compliance_list)

    def to_inner_structure(self):
        return {
            "compliance_list": to_structure_VectorType_RecordType_clientreport_UnitCompliance(self.compliance_list),
            "total_count": to_structure_UnsignedIntegerType_32(self.total_count)
        }

class GetReassignComplianceTaskReportFiltersSuccess(Response):
    def __init__(self, countries, doamins, level_1_statutories, units, compliances, users):
        self.countries = countries
        self.doamins = doamins
        self.level_1_statutories = level_1_statutories
        self.units = units
        self.compliances = compliances
        self.users = users

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["countries", "doamins", "level_1_statutories", "units", "compliances", "users"])
        countries = data.get("countries")
        countries = parse_structure_VectorType_RecordType_core_Country(countries)
        doamins = data.get("doamins")
        doamins = parse_structure_VectorType_RecordType_core_Domain(doamins)
        level_1_statutories = data.get("level_1_statutories")
        level_1_statutories = parse_structure_MapType_SignedIntegerType_8_MapType_SignedIntegerType_8_VectorType_RecordType_core_Statutory(level_1_statutories)
        units = data.get("units")
        units = parse_structure_VectorType_RecordType_clientreport_UnitName(units)
        compliances = data.get("compliances")
        compliances = parse_structure_VectorType_RecordType_clientreport_ComplianceName(compliances)
        users = data.get("users")
        users = parse_structure_VectorType_RecordType_clientreport_UserName(users)
        return GetReassignComplianceTaskReportFiltersSuccess(countries, doamins, level_1_statutories, units, compliances, users)

    def to_inner_structure(self):
        return {
            "countries": to_structure_VectorType_RecordType_core_Country(self.countries),
            "doamins": to_structure_VectorType_RecordType_core_Domain(self.doamins),
            "level_1_statutories": to_structure_MapType_SignedIntegerType_8_MapType_SignedIntegerType_8_VectorType_RecordType_core_Statutory(self.level_1_statutories),
            "units": to_structure_VectorType_RecordType_clientreport_UnitName(self.units),
            "compliances": to_structure_VectorType_RecordType_clientreport_ComplianceName(self.compliances),
            "users": to_structure_VectorType_RecordType_clientreport_UserName(self.users),
        }

class GetReassignComplianceTaskDetailsSuccess(Response):
    def __init__(self, compliance_list):
        self.compliance_list = compliance_list

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["compliance_list"])
        compliance_list = data.get("compliance_list")
        compliance_list = parse_structure_VectorType_RecordType_clientreport_ReassignCompliance(compliance_list)
        return GetReassignComplianceTaskDetailsSuccess(compliance_list)

    def to_inner_structure(self):
        return {
            "compliance_list": to_structure_VectorType_RecordType_clientreport_ReassignCompliance(self.compliance_list),
        }

class GetTaskApplicabilityStatusFiltersSuccess(Response):
    def __init__(
        self, countries, domains, business_groups, legal_entities,
        divisions, units, level_1_statutories, applicable_status
    ):
        self.countries = countries
        self.domains = domains
        self.business_groups = business_groups
        self.legal_entities = legal_entities
        self.divisions = divisions
        self.units = units
        self.level_1_statutories = level_1_statutories
        self.applicable_status = applicable_status

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["countries", "domains", "business_groups", "legal_entities", "divisions", "units", "level_1_statutories"])
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
        units = parse_structure_VectorType_RecordType_core_ClientUnit(units)
        level_1_statutories = data.get("level_1_statutories")
        level_1_statutories = parse_structure_VectorType_CustomTextType_100(level_1_statutories)
        applicable_status = data.get("applicable_status")
        applicable_status = parse_structure_VectorType_CustomTextType_100(applicable_status)
        return GetTaskApplicabilityStatusFiltersSuccess(countries, domains, business_groups, legal_entities, divisions, units, level_1_statutories, applicable_status)

    def to_inner_structure(self):
        return {
            "countries": to_structure_VectorType_RecordType_core_Country(self.countries),
            "domains": to_structure_VectorType_RecordType_core_Domain(self.domains),
            "business_groups": to_structure_VectorType_RecordType_core_ClientBusinessGroup(self.business_groups),
            "legal_entities": to_structure_VectorType_RecordType_core_ClientLegalEntity(self.legal_entities),
            "divisions": to_structure_VectorType_RecordType_core_ClientDivision(self.divisions),
            "units": to_structure_VectorType_RecordType_core_ClientUnit(self.units),
            "level_1_statutories": to_structure_VectorType_CustomTextType_100(self.level_1_statutories),
            "applicable_status": to_structure_VectorType_CustomTextType_100(self.applicable_status),
        }

class GetComplianceTaskApplicabilityStatusReportData(object):
    def __init__(
        self, business_group_name, legal_entity_name, division_name, actwise_units
    ):
        self.business_group_name = business_group_name
        self.legal_entity_name = legal_entity_name
        self.division_name = division_name
        self.actwise_units = actwise_units

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(
            data, [
                "business_group_name", "legal_entity_name", "division_name",
                "actwise_units"
            ]
        )
        business_group_name = data.get("business_group_name")
        business_group_name = parse_structure_OptionalType_CustomTextType_50(business_group_name)
        legal_entity_name = data.get("legal_entity_name")
        legal_entity_name = parse_structure_CustomTextType_50(legal_entity_name)
        division_name = data.get("division_name")
        division_name = parse_structure_OptionalType_CustomTextType_50(division_name)
        division_name = data.get("division_name")
        division_name = parse_structure_OptionalType_CustomTextType_50(division_name)
        actwise_units = data.get("actwise_units")
        actwise_units = parse_structure_MapType_CustomTextType_500_VectorType_RecordType_clientreport_ApplicabilityCompliance(actwise_units)
        return GetComplianceTaskApplicabilityStatusReportData(
            business_group_name, legal_entity_name, division_name, actwise_units
        )

    def to_structure(self):
        return {
            "business_group_name": to_structure_OptionalType_CustomTextType_50(self.business_group_name),
            "legal_entity_name": to_structure_CustomTextType_50(self.legal_entity_name),
            "division_name": to_structure_OptionalType_CustomTextType_50(self.division_name),
            "actwise_units": to_structure_MapType_CustomTextType_500_VectorType_RecordType_clientreport_ApplicabilityCompliance(self.actwise_units),
        }

class GetComplianceTaskApplicabilityStatusReportSuccess(Response):
    def __init__(self, total_record, applicable_status):
        self.total_record = total_record
        self.applicable_status = applicable_status

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["total_record", "applicable_status"])
        total_record = data.get("total_record")
        total_record = parse_structure_UnsignedIntegerType_32(total_record)
        applicable_status = data.get("applicable_status")
        applicable_status = parse_structure_VectorType_RecordType_clientreport_GetComplianceTaskApplicabilityStatusReportData(applicable_status)
        return GetComplianceTaskApplicabilityStatusReportSuccess(total_record, applicable_status)

    def to_inner_structure(self):
        return {
            "total_record": to_structure_UnsignedIntegerType_32(self.total_record),
            "applicable_status": to_structure_VectorType_RecordType_clientreport_GetComplianceTaskApplicabilityStatusReportData(self.applicable_status),
        }

class GetComplianceActivityReportFiltersSuccess(Response):
    def __init__(self, users, countries, domains, level_1_statutories, units, compliances):
        self.users = users
        self.domains = domains
        self.level_1_statutories = level_1_statutories
        self.units = units
        self.compliances = compliances
        self.countries = countries

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["users", "countries", "domains", "level_1_statutories", "units", "compliances"])
        users = data.get("users")
        countries = data.get("countries")
        domains = data.get("domains")
        level_1_statutories = data.get("level_1_statutories")
        units = data.get("units")
        compliances = data.get("compliances")
        return GetComplianceActivityReportFiltersSuccess(
            users, countries, domains, level_1_statutories,
            units, compliances
        )

    def to_inner_structure(self):
        return {
            "users": self.users,
            "countries": self.countries,
            "domains": self.domains,
            "level_1_statutories": self.level_1_statutories,
            "units": self.units,
            "compliances": self.compliances
        }

class GetComplianceActivityReportSuccess(Response):
    def __init__(self, activities):
        self.activities = activities

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["activities"])
        activities = data.get("activities")
        activities = parse_structure_VectorType_RecordType_clientreport_Activities(activities)
        return GetComplianceActivityReportSuccess(activities)

    def to_inner_structure(self):
        return {
            "activities": to_structure_VectorType_RecordType_clientreport_Activities(self.activities),
        }

#
# Statutory Notificaiton List
#

class GetStatutoryNotificationsListFiltersSuccess(Response):
    def __init__(self, countries, domains, business_groups, legal_entities, divisions, units, level_1_statutories, users):
        self.countries = countries
        self.domains = domains
        self.business_groups = business_groups
        self.legal_entities = legal_entities
        self.divisions = divisions
        self.units = units
        self.level_1_statutories = level_1_statutories

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["countries", "domains", "business_groups", "legal_entities", "divisions", "units", "level_1_statutories"])
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
        units = parse_structure_VectorType_RecordType_core_ClientUnit(units)
        level_1_statutories = data.get("level_1_statutories")
        level_1_statutories = parse_structure_VectorType_CustomTextType_500(level_1_statutories)
        return GetStatutoryNotificationsListFiltersSuccess(countries, domains, business_groups, legal_entities, divisions, units, level_1_statutories)

    def to_inner_structure(self):
        return {
            "countries": to_structure_VectorType_RecordType_core_Country(self.countries),
            "domains": to_structure_VectorType_RecordType_core_Domain(self.domains),
            "business_groups": to_structure_VectorType_RecordType_core_ClientBusinessGroup(self.business_groups),
            "legal_entities": to_structure_VectorType_RecordType_core_ClientLegalEntity(self.legal_entities),
            "divisions": to_structure_VectorType_RecordType_core_ClientDivision(self.divisions),
            "units": to_structure_VectorType_RecordType_core_ClientUnit(self.units),
            "level_1_statutories": to_structure_VectorType_CustomTextType_500(self.level_1_statutories),
        }

class GetStatutoryNotificationsListReportSuccess(Response):
    def __init__(self, statutory_wise_notifications):
        self.statutory_wise_notifications = statutory_wise_notifications

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["statutory_wise_notifications"])
        statutory_wise_notifications = data.get("statutory_wise_notifications")
        statutory_wise_notifications = parse_structure_VectorType_RecordType_clientreport_STATUTORY_WISE_NOTIFICATIONS(statutory_wise_notifications)
        return GetStatutoryNotificationsListReportSuccess(statutory_wise_notifications)

    def to_inner_structure(self):
        return {
            "statutory_wise_notifications": to_structure_VectorType_RecordType_clientreport_STATUTORY_WISE_NOTIFICATIONS(self.statutory_wise_notifications),
        }

class GetActivityLogFiltersSuccess(Response):
    def __init__(self, users, forms):
        self.users = users
        self.forms = forms

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["users", "forms"])
        users = data.get("users")
        users = parse_structure_VectorType_RecordType_clientreport_UserName(users)
        forms = data.get("forms")
        forms = parse_structure_VectorType_RecordType_clientreport_FormName(forms)
        return GetActivityLogFiltersSuccess(users, forms)

    def to_inner_structure(self):
        return {
            "users": to_structure_VectorType_RecordType_clientreport_UserName(self.users),
            "forms": to_structure_VectorType_RecordType_clientreport_FormName(self.forms),
        }

class GetActivityLogReportSuccess(Response):
    def __init__(self, activity_log):
        self.activity_log = activity_log

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["activity_log"])
        activity_log = data.get("activity_log")
        activity_log = parse_structure_VectorType_RecordType_clientreport_ActivityLog(activity_log)
        return GetActivityLogReportSuccess(activity_log)

    def to_inner_structure(self):
        return {
            "activity_log": to_structure_VectorType_RecordType_clientreport_ActivityLog(self.activity_log),
        }

class GetLoginTraceSuccess(Response):
    def __init__(self, users, login_trace):
        self.users = users
        self.login_trace = login_trace

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["users", "login_trace"])
        users = data.get("users")
        users = parse_structure_VectorType_RecordType_clientreport_User(users)
        login_trace = data.get("login_trace")
        login_trace = parse_structure_VectorType_RecordType_clientreport_LoginTrace(login_trace)
        return GetLoginTraceSuccess(users, login_trace)

    def to_inner_structure(self):
        return {
            "users": to_structure_VectorType_RecordType_clientreport_User(self.users),
            "login_trace": to_structure_VectorType_RecordType_clientreport_LoginTrace(self.login_trace),
        }

class GetClientDetailsReportDataSuccess(Response):
    def __init__(self, units, total_count):
        self.units = units
        self.total_count = total_count

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["units", "total_count"])
        units = data.get("units")
        units = parse_structure_VectorType_RecordType_core_UnitDetails(units)
        total_count = data.get("total_count")
        total_count = parse_structure_UnsignedIntegerType_32(total_count)
        return GetClientDetailsReportDataSuccess(units, total_count)

    def to_inner_structure(self):
        return {
            "units": to_structure_VectorType_RecordType_client_report_GroupedUnits(self.units),
            "total_count": to_structure_UnsignedIntegerType_32(self.total_count)
        }

class GetClientDetailsReportFiltersSuccess(Response):
    def __init__(
        self, countries, domains, business_groups,
        legal_entities, divisions, units
    ):
        self.countries = countries
        self.domains = domains
        self.business_groups = business_groups
        self.legal_entities = legal_entities
        self.divisions = divisions
        self.units = units

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "countries", "domains",
            "business_groups", "legal_entities", "divisions", "units",
            ]
        )
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
        units = parse_structure_VectorType_RecordType_core_ClientUnit(units)
        return GetClientDetailsReportFiltersSuccess(
            countries, domains,
            business_groups, legal_entities, divisions, units
        )

    def to_inner_structure(self):
        return {
            "countries": to_structure_VectorType_RecordType_core_Country(self.countries),
            "domains": to_structure_VectorType_RecordType_core_Domain(self.domains),
            "business_groups": to_structure_VectorType_RecordType_core_ClientBusinessGroup(self.business_groups),
            "legal_entities": to_structure_VectorType_RecordType_core_ClientLegalEntity(self.legal_entities),
            "divisions": to_structure_VectorType_RecordType_core_ClientDivision(self.divisions),
            "units": to_structure_VectorType_RecordType_core_ClientUnit(self.units)
        }

class GetServiceProviderWiseReportFiltersSuccess(Response):
    def __init__(
        self, sp_domains_list, sp_unit_list, sp_act_task_list, sp_list,
        compliance_task_status, sp_users_list
    ):
        self.sp_domains_list = sp_domains_list
        self.sp_unit_list = sp_unit_list
        self.sp_act_task_list = sp_act_task_list
        self.sp_list = sp_list
        self.compliance_task_status = compliance_task_status
        self.sp_users_list = sp_users_list

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "sp_domains_list", "sp_unit_list", "sp_act_task_list", "sp_list",
            "compliance_task_status", "sp_users_list"
        ])
        sp_domains_list = data.get("sp_domains_list")
        sp_unit_list = data.get("sp_unit_list")
        sp_act_task_list = data.get("sp_act_task_list")
        sp_list = data.get("sp_list")
        compliance_task_status = data.get("compliance_task_status")
        sp_users_list = data.get("sp_users_list")
        return GetServiceProviderWiseReportFiltersSuccess(
            sp_domains_list, sp_unit_list, sp_act_task_list, sp_list,
            compliance_task_status, sp_users_list
        )

    def to_inner_structure(self):
        data = {
            "sp_domains_list": self.sp_domains_list,
            "sp_unit_list": self.sp_unit_list,
            "sp_act_task_list": self.sp_act_task_list,
            "sp_list": self.sp_list,
            "compliance_task_status": self.compliance_task_status,
            "sp_users_list": self.sp_users_list
        }
        return data

class GetServiceProviderWiseReportSuccess(Response):
    def __init__(self, sp_compliances, total_count):
        self.sp_compliances = sp_compliances
        self.total_count = total_count

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["sp_compliances", "total_count"])
        sp_compliances = data.get("sp_compliances")
        total_count = data.get("total_count")
        return GetServiceProviderWiseReportSuccess(sp_compliances, total_count)

    def to_inner_structure(self):
        return {
            "sp_compliances" : self.sp_compliances,
            "total_count": self.total_count
        }

class GetUserWiseReportFiltersSuccess(Response):
    def __init__(
        self, le_users_list, user_domains_list, users_units_list, user_act_task_list,
        compliance_frequency_list, compliance_user_type, compliance_task_status
    ):
        self.le_users_list = le_users_list
        self.user_domains_list = user_domains_list
        self.users_units_list = users_units_list
        self.user_act_task_list = user_act_task_list
        self.compliance_frequency_list = compliance_frequency_list
        self.compliance_user_type = compliance_user_type
        self.compliance_task_status = compliance_task_status

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "le_users_list", "user_domains_list", "users_units_list", "user_act_task_list",
            "compliance_frequency_list", "compliance_user_type", "compliance_task_status"
        ])
        le_users_list = data.get("le_users_list")
        user_domains_list = data.get("user_domains_list")
        users_units_list = data.get("users_units_list")
        user_act_task_list = data.get("user_act_task_list")
        compliance_frequency_list = data.get("compliance_frequency_list")
        compliance_user_type = data.get("compliance_user_type")
        compliance_task_status = data.get("compliance_task_status")
        return GetUserWiseReportFiltersSuccess(
            le_users_list, user_domains_list, users_units_list, user_act_task_list,
            compliance_frequency_list, compliance_user_type, compliance_task_status
        )

    def to_inner_structure(self):
        data = {
            "le_users_list": self.le_users_list,
            "user_domains_list": self.user_domains_list,
            "users_units_list": self.users_units_list,
            "user_act_task_list": self.user_act_task_list,
            "compliance_frequency_list": self.compliance_frequency_list,
            "compliance_user_type": self.compliance_user_type,
            "compliance_task_status": self.compliance_task_status
        }
        return data

class GetUserWiseReportSuccess(Response):
    def __init__(self, user_compliances, total_count):
        self.user_compliances = user_compliances
        self.total_count = total_count

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["user_compliances", "total_count"])
        user_compliances = data.get("user_compliances")
        total_count = data.get("total_count")
        return GetUserWiseReportSuccess(user_compliances, total_count)

    def to_inner_structure(self):
        return {
            "user_compliances" : self.user_compliances,
            "total_count": self.total_count
        }

class GetUnitListReportFiltersSuccess(Response):
    def __init__(
        self, divisions, categories, units_list, domains_organisations_list,
        unit_status_list
    ):
        self.divisions = divisions
        self.categories = categories
        self.units_list = units_list
        self.domains_organisations_list = domains_organisations_list
        self.unit_status_list = unit_status_list

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "divisions", "categories", "units_list", "domains_organisations_list",
            "unit_status_list"
        ])
        divisions = data.get("divisions")
        categories = data.get("categories")
        units_list = data.get("units_list")
        domains_organisations_list = data.get("domains_organisations_list")
        unit_status_list = data.get("unit_status_list")
        return (
            divisions, categories, units_list, domains_organisations_list, unit_status_list
        )

    def to_inner_structure(self):
        return {
            "divisions": self.divisions,
            "categories": self.categories,
            "units_list": self.units_list,
            "domains_organisations_list": self.domains_organisations_list,
            "unit_status_list": self.unit_status_list
        }

class GetunitListReportSuccess(Response):
    def __init__(self, unit_list_report, total_count):
        self.unit_list_report = unit_list_report
        self.total_count = total_count

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["unit_list_report", "total_count"])
        unit_list_report = data.get("unit_list_report")
        total_count = data.get("total_count")
        return GetunitListReportSuccess(unit_list_report, total_count)

    def to_inner_structure(self):
        return {
            "unit_list_report" : self.unit_list_report,
            "total_count": self.total_count
        }

class GetStatutoryNotificationsListReportFilterSuccess(Response):
    def __init__(self, domains, act_legal_entity):
        self.domains = domains
        self.act_legal_entity = act_legal_entity

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["domains", "act_legal_entity"])
        domains = data.get("domains")
        act_legal_entity = data.get("act_legal_entity")
        return GetStatutoryNotificationsListReportFilterSuccess(
            domains, act_legal_entity
        )

    def to_inner_structure(self):
        return {
            "domains": self.domains,
            "act_legal_entity": self.act_legal_entity
        }

class GetStatutoryNotificationReportDataSuccess(Response):
    def __init__(self, stat_notf_list_report, total_count):
        self.stat_notf_list_report = stat_notf_list_report
        self.total_count = total_count

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["stat_notf_list_report", "total_count"])
        stat_notf_list_report = data.get("stat_notf_list_report")
        total_count = data.get("total_count")
        return GetStatutoryNotificationReportDataSuccess(stat_notf_list_report, total_count)

    def to_inner_structure(self):
        return {
            "stat_notf_list_report" : self.stat_notf_list_report,
            "total_count": self.total_count
        }

class GetAuditTrailReportDataSuccess(Response):
    def __init__(self, audit_activities, total_count):
        self.audit_activities = audit_activities
        self.total_count = total_count

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["audit_activities", "total_count"])
        audit_activities = data.get("audit_activities")
        total_count = data.get("total_count")
        return GetAuditTrailReportDataSuccess(audit_activities, total_count)

    def to_inner_structure(self):
        return {
            "audit_activities" : self.audit_activities,
            "total_count": self.total_count
        }

class GetRiskReportFiltersSuccess(Response):
    def __init__(
        self, domains, divisions, categories, units_list, act_legal_entity,
        compliance_task_status
    ):
        self.domains = domains
        self.divisions = divisions
        self.categories = categories
        self.units_list = units_list
        self.act_legal_entity = act_legal_entity
        self.compliance_task_status = compliance_task_status

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, [
            "domains", "divisions", "categories", "units_list", "act_legal_entity",
            "compliance_task_status"
        ])
        domains = data.get("domains")
        divisions = data.get("divisions")
        categories = data.getr("categories")
        units_list = data.get("units_list")
        act_legal_entity = data.get("act_legal_entity")
        compliance_task_status = data.get("compliance_task_status")
        return GetRiskReportFiltersSuccess(
           domains, divisions, categories, units_list, act_legal_entity,
           compliance_task_status
        )

    def to_inner_structure(self):
        return {
            "domains": self.domains,
            "divisions": self.divisions,
            "categories": self.categories,
            "units_list": self.units_list,
            "act_legal_entity": self.act_legal_entity,
            "compliance_task_status": self.compliance_task_status
        }

class GetRiskReportSuccess(Response):
    def __init__(self, risk_report, total_count):
        self.risk_report = risk_report
        self.total_count = total_count

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["risk_report", "total_count"])
        risk_report = data.get("risk_report")
        total_count = data.get("total_count")
        return GetRiskReportSuccess(risk_report, total_count)

    def to_inner_structure(self):
        return {
            "risk_report" : self.risk_report,
            "total_count": self.total_count
        }

class ExportToCSVSuccess(Response):
    def __init__(self, link):
        self.link = link

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data, ["link"])
        link = data.get("link")
        return ExportToCSVSuccess(link)

    def to_inner_structure(self):
        return {
            "link" : self.link
        }

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
            "session_token": self.session_token,
            "request": Request.to_structure(self.request),
        }

#
# Units for Legal Entity
#

class UnitLegalEntity(object):
    def __init__(self, unit_id, unit_code, unit_name, domain_id, country_id, legal_entity_id):
        self.unit_id = unit_id
        self.unit_code = unit_code
        self.unit_name = unit_name
        self.domain_id = domain_id
        self.country_id = country_id
        self.legal_entity_id = legal_entity_id

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "unit_id", "unit_code", "unit_name", "domain_id", "country_id", "legal_entity_id"
            ]
        )
        unit_id = data.get("unit_id")
        unit_code = data.get("unit_code")
        unit_name = data.get("unit_name")
        domain_id = data.get("domain_id")
        country_id = data.get("country_id")
        legal_entity_id = data.get("legal_entity_id")
        return UnitLegalEntity(unit_id, unit_code, unit_name, domain_id, country_id, legal_entity_id)

    def to_structure(self):
        return {
            "unit_id": self.unit_id,
            "unit_code": self.unit_code,
            "unit_name": self.unit_name,
            "domain_id": self.domain_id,
            "country_id": self.country_id,
            "legal_entity_id": self.legal_entity_id
        }

#
# Acts for Legal Entity
#

class ActLegalEntity(object):
    def __init__(
        self, legal_entity_id, domain_id, unit_id, compliance_id,
        statutory_mapping
    ):
        self.legal_entity_id = legal_entity_id
        self.domain_id = domain_id
        self.unit_id = unit_id
        self.compliance_id = compliance_id
        self.statutory_mapping = statutory_mapping

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "legal_entity_id", "domain_id", "unit_id", "compliance_id",
            "statutory_mapping",
            ]
        )
        legal_entity_id = data.get("legal_entity_id")
        domain_id = data.get("domain_id")
        unit_id = data.get("unit_id")
        compliance_id = data.get("compliance_id")
        statutory_mapping = data.get("statutory_mapping")

        return ActLegalEntity(
            legal_entity_id, domain_id, unit_id, compliance_id,
            statutory_mapping
        )

    def to_structure(self):
        return {
            "legal_entity_id": self.legal_entity_id,
            "domain_id": self.domain_id,
            "unit_id": self.unit_id,
            "compliance_id": self.compliance_id,
            "statutory_mapping": self.statutory_mapping,
        }

#
# Compliance Task for Legal Entity
#

class TaskLegalEntity(object):
    def __init__(
        self, legal_entity_id, domain_id, unit_id, compliance_id,
        compliance_task, frequency_id, statutory_mapping
    ):
        self.legal_entity_id = legal_entity_id
        self.domain_id = domain_id
        self.unit_id = unit_id
        self.compliance_id = compliance_id
        self.compliance_task = compliance_task
        self.frequency_id = frequency_id
        self.statutory_mapping = statutory_mapping

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "legal_entity_id", "domain_id", "unit_id", "compliance_id",
            "compliance_task", "frequency_id", "statutory_mapping",
            ]
        )
        legal_entity_id = data.get("legal_entity_id")
        domain_id = data.get("domain_id")
        unit_id = data.get("unit_id")
        compliance_id = data.get("compliance_id")
        compliance_task = data.get("compliance_task")
        frequency_id = data.get("frequency_id")
        statutory_mapping = data.get("statutory_mapping")

        return TaskLegalEntity(
            legal_entity_id, domain_id, unit_id, compliance_id,
            compliance_task, frequency_id, statutory_mapping
        )

    def to_structure(self):
        return {
            "legal_entity_id": self.legal_entity_id,
            "domain_id": self.domain_id,
            "unit_id": self.unit_id,
            "compliance_id": self.compliance_id,
            "compliance_task": self.compliance_task,
            "frequency_id": self.frequency_id,
            "statutory_mapping": self.statutory_mapping,
        }

#
# Compliance Frequency
#

class ComplianceFrequency(object):
    def __init__(
        self, frequency_id, frequency_name
    ):
        self.frequency_id = frequency_id
        self.frequency_name = frequency_name

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "frequency_id", "frequency_name"
            ]
        )
        frequency_id = data.get("frequency_id")
        frequency_name = data.get("frequency_name")
        return ComplianceFrequency(
            frequency_id, frequency_name
        )

    def to_structure(self):
        data = {
            "frequency_id": self.frequency_id,
            "frequency_name": self.frequency_name
        }
        return data

#
# Compliance user type
#

class ComplianceUserType(object):
    def __init__(self, user_type_id, user_type):
        self.user_type_id = user_type_id
        self.user_type = user_type

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["user_type_id", "user_type"])
        user_type_id = data.get("user_type_id")
        user_type = data.get("user_type")
        return ComplianceUserType(user_type_id, user_type)

    def to_structure(self):
        data = {
            "user_type_id": self.user_type_id,
            "user_type": self.user_type
        }
        return data

#
# Compliance Task Status
#

class ComplianceTaskStatus(object):
    def __init__(self, task_status_id, task_status):
        self.task_status_id = task_status_id
        self.task_status = task_status

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["task_status_id", "task_status"])
        task_status_id = data.get("task_status_id")
        task_status = data.get("task_status")
        return ComplianceTaskStatus(task_status_id, task_status)

    def to_structure(self):
        return {
            "task_status_id": self.task_status_id,
            "task_status": self.task_status
        }

#
# Compliance user type - users
#

class ComplianceUsers(object):
    def __init__(
        self, legal_entity_id, country_id, domain_id, unit_id, compliance_id,
        assignee, assignee_name, concurrence_person, concurrer_name,
        approval_person, approver_name
    ):
        self.legal_entity_id = legal_entity_id
        self.country_id = country_id
        self.domain_id = domain_id
        self.unit_id = unit_id
        self.compliance_id = compliance_id
        self.assignee = assignee
        self.assignee_name = assignee_name
        self.concurrence_person = concurrence_person
        self.concurrer_name = concurrer_name
        self.approval_person = approval_person
        self.approver_name = approver_name

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "legal_entity_id", "country_id", "domain_id", "unit_id", "compliance_id",
            "assignee", "assignee_name", "concurrence_person", "concurrer_name",
            "approval_person", "approver_name"
        ])
        legal_entity_id = data.get("legal_entity_id")
        country_id = data.get("country_id")
        domain_id = data.get("domain_id")
        unit_id = data.get("unit_id")
        compliance_id = data.get("compliance_id")
        assignee = data.get("assignee")
        assignee_name = data.get("assignee_name")
        concurrence_person = data.get("concurrence_person")
        concurrer_name = data.get("concurrer_name")
        approval_person = data.get("approval_person")
        approver_name = data.get("approver_name")
        return ComplianceUsers(
            legal_entity_id, country_id, domain_id, unit_id, compliance_id, assignee,
            assignee_name, concurrence_person, concurrer_name, approval_person,
            approver_name
        )

    def to_structure(self):
        data = {
            "legal_entity_id": self.legal_entity_id,
            "country_id": self.country_id,
            "domain_id": self.domain_id,
            "unit_id": self.unit_id,
            "compliance_id": self.compliance_id,
            "assignee": self.assignee,
            "assignee_name": self.assignee_name,
            "concurrence_person": self.concurrence_person,
            "concurrer_name": self.concurrer_name,
            "approval_person": self.approval_person,
            "approver_name": self.approver_name
        }
        return data

#
# Legal Entity Wise Report
#

class LegalEntityWiseReport(object):
    def __init__(
        self, compliance_history_id, compliance_activity_id, country_id, legal_entity_id,
        domain_id, unit_id, compliance_id, unit_name, statutory_mapping, compliance_task,
        frequency_name, due_date, task_status, assignee_name, activity_status, activity_date,
        document_name, completion_date, url, logo_url, start_date, history_count
    ):
        self.compliance_history_id = compliance_history_id
        self.compliance_activity_id = compliance_activity_id
        self.country_id = country_id
        self.legal_entity_id = legal_entity_id
        self.domain_id = domain_id
        self.unit_id = unit_id
        self.compliance_id = compliance_id
        self.unit_name = unit_name
        self.statutory_mapping = statutory_mapping
        self.compliance_task = compliance_task
        self.frequency_name = frequency_name
        self.due_date = due_date
        self.task_status = task_status
        self.assignee_name = assignee_name
        self.activity_status = activity_status
        self.activity_date = activity_date
        self.document_name = document_name
        self.completion_date = completion_date
        self.url = url
        self.logo_url = logo_url
        self.start_date = start_date
        self.history_count = history_count

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "compliance_history_id", "compliance_activity_id", "country_id", "legal_entity_id",
            "domain_id", "unit_id", "compliance_id", "unit_name", "statutory_mapping", "compliance_task",
            "frequency_name", "due_date", "task_status", "assignee_name", "activity_status", "activity_date",
            "document_name", "completion_date", "url", "logo_url", "start_date", "history_count"
        ])
        compliance_history_id = data.get("compliance_history_id")
        compliance_activity_id = data.get("compliance_activity_id")
        country_id = data.get("country_id")
        legal_entity_id = data.get("legal_entity_id")
        domain_id = data.get("domain_id")
        unit_id = data.get("unit_id")
        compliance_id = data.get("compliance_id")
        unit_name = data.get("unit_name")
        statutory_mapping = data.get("statutory_mapping")
        compliance_task = data.get("compliance_task")
        frequency_name = data.get("frequency_name")
        due_date = data.get("due_date")
        task_status = data.get("task_status")
        assignee_name = data.get("assignee_name")
        activity_status = data.get("activity_status")
        activity_date = data.get("activity_date")
        document_name = data.get("document_name")
        completion_date = data.get("completion_date")
        url = data.get("url")
        logo_url = data.get("logo_url")
        start_date = data.get("start_date")
        history_count = data.get("history_count")
        return LegalEntityWiseReport(
            compliance_history_id, compliance_activity_id, country_id, legal_entity_id, domain_id, unit_id, compliance_id,
            unit_name, statutory_mapping, compliance_task, frequency_name,
            due_date, task_status, assignee_name, activity_status, activity_date,
            document_name, completion_date, url, logo_url, start_date, history_count
        )

    def to_structure(self):
        data = {
            "compliance_history_id": self.compliance_history_id,
            "compliance_activity_id": self.compliance_activity_id,
            "country_id": self.country_id,
            "legal_entity_id": self.legal_entity_id,
            "domain_id": self.domain_id,
            "unit_id": self.unit_id,
            "compliance_id": self.compliance_id,
            "unit_name": self.unit_name,
            "statutory_mapping": self.statutory_mapping,
            "compliance_task": self.compliance_task,
            "frequency_name": self.frequency_name,
            "due_date": self.due_date,
            "task_status": self.task_status,
            "assignee_name": self.assignee_name,
            "activity_status": self.activity_status,
            "activity_date": self.activity_date,
            "document_name": self.document_name,
            "completion_date": self.completion_date,
            "url": self.url,
            "logo_url": self.logo_url,
            "start_date": self.start_date,
            "history_count": self.history_count
        }
        return data

#
# Legal Entity Wise Report
#

class UnitWiseReport(object):
    def __init__(
        self, compliance_history_id, compliance_activity_id, country_id, legal_entity_id, domain_id,
        unit_id, compliance_id, unit_name, statutory_mapping, compliance_task, frequency_name,
        due_date, task_status, assignee_name, activity_status, activity_date,
        document_name, completion_date, url, domain_name, logo_url, start_date, history_count
    ):
        self.compliance_history_id = compliance_history_id
        self.compliance_activity_id = compliance_activity_id
        self.country_id = country_id
        self.legal_entity_id = legal_entity_id
        self.domain_id = domain_id
        self.unit_id = unit_id
        self.compliance_id = compliance_id
        self.unit_name = unit_name
        self.statutory_mapping = statutory_mapping
        self.compliance_task = compliance_task
        self.frequency_name = frequency_name
        self.due_date = due_date
        self.task_status = task_status
        self.assignee_name = assignee_name
        self.activity_status = activity_status
        self.activity_date = activity_date
        self.document_name = document_name
        self.completion_date = completion_date
        self.url = url
        self.domain_name = domain_name
        self.logo_url = logo_url
        self.start_date = start_date
        self.history_count = history_count

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "compliance_history_id", "compliance_activity_id", "country_id", "legal_entity_id",
            "domain_id", "unit_id", "compliance_id", "unit_name", "statutory_mapping", "compliance_task",
            "frequency_name", "due_date", "task_status", "assignee_name", "activity_status", "activity_date",
            "document_name", "completion_date", "url", "domain_name", "logo_url", "start_date", "history_count"
        ])
        compliance_history_id = data.get("compliance_history_id")
        compliance_activity_id = data.get("compliance_activity_id")
        country_id = data.get("country_id")
        legal_entity_id = data.get("legal_entity_id")
        domain_id = data.get("domain_id")
        unit_id = data.get("unit_id")
        compliance_id = data.get("compliance_id")
        unit_name = data.get("unit_name")
        statutory_mapping = data.get("statutory_mapping")
        compliance_task = data.get("compliance_task")
        frequency_name = data.get("frequency_name")
        due_date = data.get("due_date")
        task_status = data.get("task_status")
        assignee_name = data.get("assignee_name")
        activity_status = data.get("activity_status")
        activity_date = data.get("activity_date")
        document_name = data.get("document_name")
        completion_date = data.get("completion_date")
        url = data.get("url")
        domain_name = data.get("domain_name")
        logo_url = data.get("logo_url")
        start_date = data.get("start_date")
        history_count = data.get("history_count")
        return UnitWiseReport(
            compliance_history_id, compliance_activity_id, country_id, legal_entity_id,
            domain_id, unit_id, compliance_id, unit_name, statutory_mapping, compliance_task,
            frequency_name, due_date, task_status, assignee_name, activity_status, activity_date,
            document_name, completion_date, url, domain_name, logo_url, start_date, history_count
        )

    def to_structure(self):
        data = {
            "compliance_history_id": self.compliance_history_id,
            "compliance_activity_id": self.compliance_activity_id,
            "country_id": self.country_id,
            "legal_entity_id": self.legal_entity_id,
            "domain_id": self.domain_id,
            "unit_id": self.unit_id,
            "compliance_id": self.compliance_id,
            "unit_name": self.unit_name,
            "statutory_mapping": self.statutory_mapping,
            "compliance_task": self.compliance_task,
            "frequency_name": self.frequency_name,
            "due_date": self.due_date,
            "task_status": self.task_status,
            "assignee_name": self.assignee_name,
            "activity_status": self.activity_status,
            "activity_date": self.activity_date,
            "document_name": self.document_name,
            "completion_date": self.completion_date,
            "url": self.url,
            "domain_name": self.domain_name,
            "logo_url": self.logo_url,
            "start_date": self.start_date,
            "history_count": self.history_count
        }
        return data

#
# Service Provider Domains
#

class ServiceProviderDomains(object):
    def __init__(self, user_id, domain_id, domain_name, sp_id_optional):
        self.user_id = user_id
        self.domain_id = domain_id
        self.domain_name = domain_name
        self.sp_id_optional = sp_id_optional

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "user_id", "domain_id", "domain_name", "sp_id_optional"
        ])
        user_id = data.get("user_id")
        domain_id = data.get("domain_id")
        domain_name = data.get("domain_name")
        sp_id_optional = data.get("sp_id_optional")
        return ServiceProviderDomains(user_id, domain_id, domain_name, sp_id_optional)

    def to_structure(self):
        return {
            "user_id": self.user_id,
            "domain_id": self.domain_id,
            "domain_name": self.domain_name,
            "sp_id_optional": self.sp_id_optional
        }

#
# Service Provider Units
#

class ServiceProviderUnits(object):
    def __init__(self, user_id_optional, unit_id, domain_id, unit_code, unit_name, sp_id_optional):
        self.user_id_optional = user_id_optional
        self.unit_id = unit_id
        self.domain_id = domain_id
        self.unit_code = unit_code
        self.unit_name = unit_name
        self.sp_id_optional = sp_id_optional

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "user_id_optional", "unit_id", "domain_id", "unit_code", "unit_name", "sp_id_optional"
        ])
        user_id_optional = data.get("user_id_optional")
        unit_id = data.get("unit_id")
        domain_id = data.get("domain_id")
        unit_code = data.get("unit_code")
        unit_name = data.get("unit_name")
        sp_id_optional = data.get("sp_id_optional")
        return ServiceProviderUnits(user_id_optional, unit_id, domain_id, unit_code, unit_name, sp_id_optional)

    def to_structure(self):
        return {
            "user_id_optional": self.user_id_optional,
            "unit_id": self.unit_id,
            "domain_id": self.domain_id,
            "unit_code": self.unit_code,
            "unit_name": self.unit_name,
            "sp_id_optional": self.sp_id_optional
        }

#
# Legal Entity - Users Acts
#

class ServiceProviderActList(object):
    def __init__(
        self, legal_entity_id, country_id, domain_id, unit_id, compliance_id,
        assignee, sp_ass_id_optional, concurrence_person, sp_cc_id_optional,
        approval_person, sp_app_id_optional, statutory_mapping
    ):
        self.legal_entity_id = legal_entity_id
        self.country_id = country_id
        self.domain_id = domain_id
        self.unit_id = unit_id
        self.compliance_id = compliance_id
        self.assignee = assignee
        self.sp_ass_id_optional = sp_ass_id_optional
        self.concurrence_person = concurrence_person
        self.sp_cc_id_optional = sp_cc_id_optional
        self.approval_person = approval_person
        self.sp_app_id_optional = sp_app_id_optional
        self.statutory_mapping = statutory_mapping

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "legal_entity_id", "country_id", "domain_id", "unit_id", "compliance_id",
            "assignee", "sp_ass_id_optional", "concurrence_person", "sp_cc_id_optional",
            "approval_person", "sp_app_id_optional", "statutory_mapping"
        ])
        legal_entity_id = data.get("legal_entity_id")
        country_id = data.get("country_id")
        domain_id = data.get("domain_id")
        unit_id = data.get("unit_id")
        compliance_id = data.get("compliance_id")
        assignee = data.get("assignee")
        sp_ass_id_optional = data.get("sp_ass_id_optional")
        concurrence_person = data.get("concurrence_person")
        sp_cc_id_optional = data.get("sp_cc_id_optional")
        approval_person = data.get("approval_person")
        sp_app_id_optional = data.get("sp_app_id_optional")
        statutory_mapping = data.get("statutory_mapping")
        return ServiceProviderActList(
            legal_entity_id, country_id, domain_id, unit_id, compliance_id,
            assignee, sp_ass_id_optional, concurrence_person, sp_cc_id_optional,
            approval_person, sp_app_id_optional, statutory_mapping
        )

    def to_structure(self):
        return {
            "legal_entity_id": self.legal_entity_id,
            "country_id": self.country_id,
            "domain_id": self.domain_id,
            "unit_id": self.unit_id,
            "compliance_id": self.compliance_id,
            "assignee": self.assignee,
            "sp_ass_id_optional": self.sp_ass_id_optional,
            "concurrence_person": self.concurrence_person,
            "sp_cc_id_optional": self.sp_cc_id_optional,
            "approval_person": self.approval_person,
            "sp_app_id_optional": self.sp_app_id_optional,
            "statutory_mapping": self.statutory_mapping
        }

#
# Service Providers - Users List
#

class ServiceProvidersUsers(object):
    def __init__(self, domain_id, unit_id, compliance_id, sp_id_optional, user_id, user_name):
        self.domain_id = domain_id
        self.unit_id = unit_id
        self.compliance_id = compliance_id
        self.sp_id_optional = sp_id_optional
        self.user_id = user_id
        self.user_name = user_name

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "domain_id", "unit_id", "compliance_id", "sp_id_optional", "user_id", "user_name"
        ])
        domain_id = data.get("domain_id")
        unit_id = data.get("unit_id")
        compliance_id = data.get("compliance_id")
        sp_id_optional = data.get("sp_id_optional")
        user_id = data.get("user_id")
        user_name = data.get("user_name")
        return ServiceProvidersUsers(domain_id, unit_id, compliance_id, sp_id_optional, user_id, user_name)

    def to_structure(self):
        data = {
            "domain_id": self.domain_id,
            "unit_id": self.unit_id,
            "compliance_id": self.compliance_id,
            "sp_id_optional": self.sp_id_optional,
            "user_id": self.user_id,
            "user_name": self.user_name
        }
        return to_structure_dictionary_values(data)

#
# Users list
#

class LegalEntityUsers(object):
    def __init__(self, user_id, username, user_category_id):
        self.user_id = user_id
        self.username = username
        self.user_category_id = user_category_id

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["user_id", "username", "user_category_id"])
        user_id = data.get("user_id")
        username = data.get("username")
        user_category_id = data.get("user_category_id")
        return UserName(user_id, username, user_category_id)

    def to_structure(self):
        return {
            "user_id": self.user_id,
            "username": self.username,
            "user_category_id": self.user_category_id
        }

#
# Legal Entity - Users Domains
#

class UserDomains(object):
    def __init__(self, user_id, domain_id, domain_name):
        self.user_id = user_id
        self.domain_id = domain_id
        self.domain_name = domain_name

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "user_id", "domain_id", "domain_name"
        ])
        user_id = data.get("user_id")
        domain_id = data.get("domain_id")
        domain_name = data.get("domain_name")
        return UserDomains(user_id, domain_id, domain_name)

    def to_structure(self):
        data = {
            "user_id": self.user_id,
            "domain_id": self.domain_id,
            "domain_name": self.domain_name
        }
        return to_structure_dictionary_values(data)


#
# Legal Entity - Users Units
#

class UserUnits(object):
    def __init__(self, user_id_optional, unit_id, domain_id, unit_code, unit_name):
        self.user_id_optional = user_id_optional
        self.unit_id = unit_id
        self.domain_id = domain_id
        self.unit_code = unit_code
        self.unit_name = unit_name

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "user_id_optional", "unit_id", "domain_id", "unit_code", "unit_name"
        ])
        user_id_optional = data.get("user_id_optional")
        unit_id = data.get("unit_id")
        domain_id = data.get("domain_id")
        unit_code = data.get("unit_code")
        unit_name = data.get("unit_name")
        return UserUnits(user_id_optional, unit_id, domain_id, unit_code, unit_name)

    def to_structure(self):
        return {
            "user_id_optional": self.user_id_optional,
            "unit_id": self.unit_id,
            "domain_id": self.domain_id,
            "unit_code": self.unit_code,
            "unit_name": self.unit_name
        }

#
# Legal Entity - Users Acts
#

class UsersActList(object):
    def __init__(
        self, legal_entity_id, country_id, domain_id, unit_id, compliance_id,
        assignee, concurrence_person, approval_person,
        statutory_mapping
    ):
        self.legal_entity_id = legal_entity_id
        self.country_id = country_id
        self.domain_id = domain_id
        self.unit_id = unit_id
        self.compliance_id = compliance_id
        self.assignee = assignee
        self.concurrence_person = concurrence_person
        self.approval_person = approval_person
        self.statutory_mapping = statutory_mapping

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "legal_entity_id", "country_id", "domain_id", "unit_id", "compliance_id",
            "assignee", "concurrence_person", "approval_person", "statutory_mapping"
        ])
        legal_entity_id = data.get("legal_entity_id")
        country_id = data.get("country_id")
        domain_id = data.get("domain_id")
        unit_id = data.get("unit_id")
        compliance_id = data.get("compliance_id")
        assignee = data.get("assignee")
        concurrence_person = data.get("concurrence_person")
        approval_person = data.get("approval_person")
        statutory_mapping = data.get("statutory_mapping")
        return UsersActList(
            legal_entity_id, country_id, domain_id, unit_id, compliance_id,
            assignee, concurrence_person, approval_person, statutory_mapping
        )

    def to_structure(self):
        return {
            "legal_entity_id": self.legal_entity_id,
            "country_id": self.country_id,
            "domain_id": self.domain_id,
            "unit_id": self.unit_id,
            "compliance_id": self.compliance_id,
            "assignee": self.assignee,
            "concurrence_person": self.concurrence_person,
            "approval_person": self.approval_person,
            "statutory_mapping": self.statutory_mapping
        }

#
# Unit List - Divisions
#

class Divisions(object):
    def __init__(self, division_id, division_name):
        self.division_id = division_id
        self.division_name = division_name

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["division_id", "division_name"])
        division_id = data.get("division_id")
        division_name = data.get("division_name")
        return Divisions(division_id, division_name)

    def to_structure(self):
        return {
            "division_id": self.division_id,
            "division_name": self.division_name,
        }

#
# Unit List - Categories
#

class Category(object):
    def __init__(self, division_id, category_id, category_name):
        self.division_id = division_id
        self.category_id = category_id
        self.category_name = category_name

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["division_id", "category_id", "category_name"])
        division_id = data.get("division_id")
        category_id = data.get("category_id")
        category_name = data.get("category_name")
        return Category(division_id, category_id, category_name)

    def to_structure(self):
        return {
            "division_id": self.division_id,
            "category_id": self.category_id,
            "category_name": self.category_name
        }

#
# Unit List - Units
#

class UnitList(object):
    def __init__(self, unit_id, unit_code, unit_name, division_id, category_id, d_ids, i_ids):
        self.unit_id = unit_id
        self.unit_code = unit_code
        self.unit_name = unit_name
        self.division_id = division_id
        self.category_id = category_id
        self.d_ids = d_ids
        self.i_ids = i_ids

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "unit_id", "unit_code", "unit_name", "division_id", "category_id", "d_ids", "i_ids"
        ])
        unit_id = data.get("unit_id")
        unit_code = data.get("unit_code")
        unit_name = data.get("unit_name")
        division_id = data.get("division_id")
        category_id = data.get("category_id")
        d_ids = data.get("d_ids")
        i_ids = data.get("i_ids")
        return UnitList(unit_id, unit_code, unit_name, division_id, category_id, d_ids, i_ids)

    def to_structure(self):
        return {
            "unit_id": self.unit_id,
            "unit_code": self.unit_code,
            "unit_name": self.unit_name,
            "division_id": self.division_id,
            "category_id": self.category_id,
            "d_ids": self.d_ids,
            "i_ids": self.i_ids
        }

#
# Unit List - Domains and Organisation
#

class DomainsOrganisation(object):
    def __init__(self, domain_id, domain_name, organisation_id, organisation_name):
        self.domain_id = domain_id
        self.domain_name = domain_name
        self.organisation_id = organisation_id
        self.organisation_name = organisation_name

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "domain_id", "domain_name", "organisation_id", "organisation_name"
        ])
        domain_id = data.get("domain_id")
        domain_name = data.get("domain_name")
        organisation_id = data.get("organisation_id")
        organisation_name = data.get("organisation_name")
        return DomainsOrganisation(
            domain_id, domain_name, organisation_id, organisation_name
        )

    def to_structure(self):
        return {
            "domain_id": self.domain_id,
            "domain_name": self.domain_name,
            "organisation_id": self.organisation_id,
            "organisation_name": self.organisation_name
        }

#
# Unit Status
#

class UnitStatus(object):
    def __init__(self, unit_status_id, unit_status):
        self.unit_status_id = unit_status_id
        self.unit_status = unit_status

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["unit_status_id", "unit_status"])
        unit_status_id = data.get("unit_status_id")
        unit_status = data.get("unit_status")
        return UnitStatus(unit_status_id, unit_status)

    def to_structure(self):
        return {
            "unit_status_id": self.unit_status_id,
            "unit_status": self.unit_status,
        }

class UnitListReport(object):
    def __init__(
        self, unit_id, unit_code, unit_name, geography_name, address, postal_code,
        d_i_names, unit_status, closed_on, division_name, logo_url
    ):
        self.unit_id = unit_id
        self.unit_code = unit_code
        self.unit_name = unit_name
        self.geography_name = geography_name
        self.address = address
        self.postal_code = postal_code
        self.d_i_names = d_i_names
        self.unit_status = unit_status
        self.closed_on = closed_on
        self.division_name = division_name
        self.logo_url = logo_url

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "unit_id", "unit_code", "unit_name", "geography_name", "address", "postal_code",
            "d_i_names", "unit_status", "closed_on", "division_name", "logo_url"
        ])
        unit_id = data.get("unit_id")
        unit_code = data.get("unit_code")
        unit_name = data.get("unit_name")
        geography_name = data.get("geography_name")
        address = data.get("address")
        postal_code = data.get("postal_code")
        d_i_names = data.get("d_i_names")
        unit_status = data.get("unit_status")
        closed_on = data.get("closed_on")
        division_name = data.get("division_name")
        logo_url = data.get("logo_url")
        return UnitListReport(
            unit_id, unit_code, unit_name, geography_name, address, postal_code,
            d_i_names, unit_status, closed_on, division_name, logo_url
        )

    def to_structure(self):
        return {
            "unit_id": self.unit_id,
            "unit_code": self.unit_code,
            "unit_name": self.unit_name,
            "geography_name": self.geography_name,
            "address": self.address,
            "postal_code": self.postal_code,
            "d_i_names": self.d_i_names,
            "unit_status": self.unit_status,
            "closed_on": self.closed_on,
            "division_name": self.division_name,
            "logo_url": self.logo_url
        }

#
# Statutory Notification List
#

class StatutoryNotificationReport(object):
    def __init__(
        self, compliance_id, compliance_task, compliance_description,
        created_on, notification_text, statutory_mapping
    ):
        self.compliance_id = compliance_id
        self.compliance_task = compliance_task
        self.compliance_description = compliance_description
        self.created_on = created_on
        self.notification_text = notification_text
        self.statutory_mapping = statutory_mapping

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "compliance_id", "compliance_task", "compliance_description",
            "created_on", "notification_text", "statutory_mapping"
        ])
        compliance_id = data.get("compliance_id")
        compliance_task = data.get("compliance_task")
        compliance_description = data.get("compliance_description")
        created_on = data.get("created_on")
        notification_text = data.get("notification_text")
        statutory_mapping = data.get("statutory_mapping")

        return StatutoryNotificationReport(
            compliance_id, compliance_task, compliance_description,
            created_on, notification_text, statutory_mapping
        )

    def to_structure(self):
        return {
            "compliance_id": self.compliance_id,
            "compliance_task": self.compliance_task,
            "compliance_description": self.compliance_description,
            "created_on": self.created_on,
            "notification_text": self.notification_text,
            "statutory_mapping": self.statutory_mapping
        }

#
# Audit Trail Forms
#

class AuditTrailActivities(object):
    def __init__(self, user_id, user_name, form_id, action, created_on, logo_url):
        self.user_id = user_id
        self.user_name = user_name
        self.form_id = form_id
        self.action = action
        self.created_on = created_on
        self.logo_url = logo_url

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "user_id", "user_name", "form_id", "action," "created_on", "logo_url"
        ])
        user_id = data.get("user_id")
        user_name = data.get("user_name")
        form_id = data.get("form_id")
        action = data.get("action")
        created_on = data.get("created_on")
        logo_url = data.get("logo_url")
        return AuditTrailActivities(user_id, user_name, form_id, action, created_on, logo_url)

    def to_structure(self):
        return {
            "user_id": self.user_id,
            "user_name": self.user_name,
            "form_id": self.form_id,
            "action": self.action,
            "created_on": self.created_on,
            "logo_url": self.logo_url
        }

#
# UserName
#

class UserName(object):
    def __init__(self, user_id, user_name):
        self.user_id = user_id
        self.user_name = user_name

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, ["user_id", "user_name"])
        user_id = data.get("user_id")
        user_name = data.get("user_name")
        return UserName(user_id, user_name)

    def to_structure(self):
        return {
            "user_id": self.user_id,
            "user_name": self.user_name,
        }

#
# UserName
#

class RiskReport(object):
    def __init__(
        self, statutory_mapping, unit_name, compliance_task, frequency_name, penal_consequences,
        admin_incharge, assignee_name, task_status, document_name, url, logo_url, start_date, due_date,
        concurrer_name, approver_name, assigned_on, concurred_on, approved_on, comp_remarks, unit_id
    ):
        self.statutory_mapping = statutory_mapping
        self.unit_name = unit_name
        self.compliance_task = compliance_task
        self.frequency_name = frequency_name
        self.penal_consequences = penal_consequences
        self.admin_incharge = admin_incharge
        self.assignee_name = assignee_name
        self.task_status = task_status
        self.document_name = document_name
        self.url = url
        self.logo_url = logo_url
        self.start_date = start_date
        self.due_date = due_date
        self.concurrer_name = concurrer_name
        self.approver_name = approver_name
        self.assigned_on = assigned_on
        self.concurred_on = concurred_on
        self.approved_on = approved_on
        self.comp_remarks = comp_remarks
        self.unit_id = unit_id

    @staticmethod
    def parse_structure(data):
        data = parse_dictionary(data, [
            "statutory_mapping", "unit_name", "compliance_task", "frequency_name", "penal_consequences",
            "admin_incharge", "assignee_name", "task_status", "document_name", "url", "logo_url", "start_date",
            "due_date", "concurrer_name", "approver_name", "assigned_on", "concurred_on", "approved_on",
            "comp_remarks", "unit_id"
        ])
        statutory_mapping = data.get("statutory_mapping")
        unit_name = data.get("unit_name")
        compliance_task = data.get("compliance_task")
        frequency_name = data.get("frequency_name")
        penal_consequences = data.get("penal_consequences")
        admin_incharge = data.get("admin_incharge")
        assignee_name = data.get("assignee_name")
        task_status = data.get("task_status")
        document_name = data.get("document_name")
        url = data.get("url")
        logo_url = data.get("logo_url")
        start_date = data.get("start_date")
        due_date = data.get("due_date")
        concurrer_name = data.get("concurrer_name")
        approver_name = data.get("approver_name")
        assigned_on = data.get("assigned_on")
        concurred_on = data.get("concurred_on")
        approved_on = data.get("approved_on")
        comp_remarks = data.get("comp_remarks")
        unit_id = data.get("unit_id")
        return RiskReport(
            statutory_mapping, unit_name, compliance_task, frequency_name, penal_consequences,
            admin_incharge, assignee_name, task_status, document_name, url, logo_url, start_date,
            due_date, concurrer_name, approver_name, assigned_on, concurred_on, approved_on,
            comp_remarks, unit_id
        )

    def to_structure(self):
        return {
            "statutory_mapping": self.statutory_mapping, "unit_name": self.unit_name,
            "compliance_task": self.compliance_task, "frequency_name": self.frequency_name,
            "penal_consequences": self.penal_consequences, "admin_incharge": self.admin_incharge,
            "assignee_name": self.assignee_name, "task_status": self.task_status, "document_name": self.document_name,
            "url": self.url, "logo_url": self.logo_url,
            "start_date": self.start_date, "due_date": self.due_date,
            "concurrer_name": self.concurrer_name, "approver_name": self.approver_name,
            "assigned_on": self.assigned_on, "concurred_on": self.concurred_on,
            "approved_on": self.approved_on, "comp_remarks": self.comp_remarks,
            "unit_id": self.unit_id
        }

from clientreportnew import *

def _init_Request_class_map():
    classes = [
        GetRiskReportFilters, GetRiskReportData, GetLegalEntityWiseReportFilters,
        GetLegalEntityWiseReport, GetDomainWiseReportFilters, GetDomainWiseReport,
        GetUnitWiseReportFilters, GetUnitWiseReport, GetServiceProviderWiseReportFilters,
        GetServiceProviderWiseReport, GetUserWiseReportFilters, GetUserWiseReport,
        GetUnitListReportFilters, GetUnitListReport, GetStatutoryNotificationsListReportFilters,
        GetStatutoryNotificationsListReportData, GetAuditTrailReportData,

        GetReassignedHistoryReportFilters, GetReassignedHistoryReport,
        GetStatusReportConsolidatedFilters, GetStatusReportConsolidated,
        GetStatutorySettingsUnitWiseFilters, GetStatutorySettingsUnitWise,
        GetDomainScoreCardFilters, GetDomainScoreCard,
        GetLEWiseScoreCardFilters, GetLEWiseScoreCard,
        GetWorkFlowScoreCardFilters, GetWorkFlowScoreCard,

    ]
    class_map = {}
    for c in classes:
        class_map[c.__name__] = c
    return class_map

_Request_class_map = _init_Request_class_map()

def _init_Response_class_map():
    classes = [
        GetRiskReportFiltersSuccess, ExportToCSVSuccess, GetLegalEntityWiseReportFiltersSuccess,
        GetLegalEntityWiseReportSuccess, GetDomainWiseReportFiltersSuccess, GetDomainWiseReportSuccess,
        GetUnitWiseReportFiltersSuccess, GetUnitWiseReportSuccess, GetServiceProviderWiseReportFiltersSuccess,
        GetServiceProviderWiseReportSuccess, GetUserWiseReportFiltersSuccess, GetUserWiseReportSuccess,
        GetUnitListReportFiltersSuccess, GetunitListReportSuccess,
        GetStatutoryNotificationsListReportFilterSuccess, GetStatutoryNotificationReportDataSuccess,
        GetAuditTrailReportDataSuccess, GetRiskReportSuccess,

        GetReassignedHistoryReportFiltersSuccess, GetReassignedHistoryReportSuccess,
        GetStatusReportConsolidatedFiltersSuccess, GetStatusReportConsolidatedSuccess,
        GetStatutorySettingsUnitWiseFiltersSuccess, GetStatutorySettingsUnitWiseSuccess,
        GetDomainScoreCardFiltersSuccess, GetDomainScoreCardSuccess,
        GetLEWiseScoreCardFiltersSuccess, GetLEWiseScoreCardSuccess,
        GetWorkFlowScoreCardFiltersSuccess, GetWorkFlowScoreCardSuccess
    ]
    class_map = {}
    for c in classes:
        class_map[c.__name__] = c
    return class_map

_Response_class_map = _init_Response_class_map()
