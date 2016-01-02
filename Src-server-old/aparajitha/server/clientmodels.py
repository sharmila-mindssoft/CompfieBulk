from aparajitha.misc.dates import *

__all__ = [
    "Form",
    "Menu",
    "ServiceProvider",
    "UserPrivilege",
    "User",
    "BusinessGroup",
    "LegalEntity",
    "Division",
    "Unit"
]

class Form(object) :
    def __init__(self, form_id, form_name, form_url, form_order, form_type, 
        category, is_admin_form, parent_menu) :
        self.form_id = form_id
        self.form_name = form_name
        self.form_url = form_url
        self.form_order = form_order
        self.form_type = form_type
        self.category = category
        self.is_admin_form = is_admin_form
        self.parent_menu = parent_menu

    def to_Structure(self) :
        return {
            "form_id": self.form_id,
            "form_name": self.form_name,
            "form_url": self.form_url,
            "form_type": self.form_type,
            "form_order": self.form_order,
            "parent_menu": self.parent_menu
        }

    @classmethod
    def get_forms(self, type, db):
        forms = []
        rows = db.get_section_wise_forms(type)
        for row in rows:
            form_obj = Form(int(row[0]), row[1], row[2], int(row[3]), 
                row[4], row[5], row[6], row[7])
            forms.append(form_obj)
        return forms
            
class Menu(object):
    structured_form = {}
    def __init__(self, master_forms, transaction_forms, report_forms, setting_forms):
        self.master_forms = master_forms
        self.transaction_forms = transaction_forms
        self.report_forms = report_forms
        self.setting_forms = setting_forms

    def to_Structure(self):
        return {
            "masters": self.master_forms,
            "transactions": self.transaction_forms,
            "reports": self.report_forms,
            "settings": self.setting_forms
        }

    @classmethod
    def get_menu(self, formList) :
        masters = []
        transactions = []
        reports = []
        settings = []
        for form in formList:
            self.structured_form = form.to_Structure()
            if form.form_type == "master".lower():
                masters.append(self.structured_form)
            elif form.form_type == "transaction".lower():
                transactions.append(self.structured_form)
            elif form.form_type == "report".lower():
                reports.append(self.structured_form)    
            elif form.form_type == "setting".lower():
                settings.append(self.structured_form)
        menu = Menu(masters, transactions,reports, settings)
        return menu.to_Structure()

class ServiceProvider(object):
    def __init__(self, client_id, service_provider_id, service_provider_name, address, 
                contract_from, contract_to, contact_person, contact_no, is_active) :
        self.client_id = client_id
        self.service_provider_id =  service_provider_id
        self.service_provider_name =  service_provider_name
        self.address =  address
        self.contract_from =  contract_from
        self.contract_to =  contract_to
        self.contact_person =  contact_person
        self.contact_no =  contact_no
        self.is_active = is_active if is_active != None else 1

    @classmethod
    def initialize_with_request(self, request, service_provider_id, client_id):
    	service_provider_name = str(request["service_provider_name"])
    	address = str(request["address"])
    	contract_from =  str(request["contract_from"])
    	contract_to =  str(request["contract_to"])
    	contact_person =  str(request["contact_person"])
    	contact_no =  str(request["contact_no"])
    	contract_from = datetime_to_timestamp(string_to_datetime(contract_from))
    	contract_to = datetime_to_timestamp(string_to_datetime(contract_to))
    	return ServiceProvider(client_id, service_provider_id, service_provider_name, address, 
                contract_from, contract_to, contact_person, contact_no, None)

    def to_Structure(self):
        return {
	        "service_provider_id": self.service_provider_id,
	        "service_provider_name": self.service_provider_name, 
	        "address": self.address,
	        "contract_from": self.contract_from,
	        "contract_to": self.contract_to, 
	        "contact_person": self.contact_person,
	        "contact_no": self.contact_no,
	        "is_active": self.is_active
    	}

    @classmethod
    def get_list(self, db):
        servcie_provider_list = []
        rows = db.get_service_providers()
        for row in rows:
            service_provider_id = int(row[0])
            service_provider_name = row[1]
            address = row[2]
            contract_from = datetime_to_string(timestamp_to_datetime(row[3]))
            contract_to = datetime_to_string(timestamp_to_datetime(row[4]))
            contact_person = row[5]
            contact_no = row[6]
            is_active = row[7]
            service_provider = ServiceProvider(None, service_provider_id, service_provider_name, address, 
                contract_from, contract_to, contact_person, contact_no, is_active)
            servcie_provider_list.append(service_provider.to_Structure())
        return servcie_provider_list

class UserPrivilege() :
    def __init__(self, client_id, user_group_id, user_group_name, form_type, form_ids, is_active) :
        self.client_id = client_id
        self.user_group_id =  user_group_id 
        self.user_group_name = user_group_name
        self.form_type = form_type 
        self.form_ids = form_ids 
        self.is_active = is_active if is_active != None else 1

    @classmethod
    def initialize_with_request(self, request, user_group_id, client_id):
        user_group_name = str(request["user_group_name"])
        form_type = str(request["form_type"])
        form_ids =  request["form_ids"]
        user_privilege = UserPrivilege(client_id, user_group_id, user_group_name, 
            form_type, form_ids, None)
        return user_privilege

    def to_detailed_structure(self) :
        return {
            "user_group_id": self.user_group_id,
            "user_group_name": self.user_group_name,
            "form_type": self.form_type,
            "form_ids": self.form_ids,
            "is_active": self.is_active
        }

    def to_Structure(self):
        return {
            "user_group_id": self.user_group_id,
            "user_group_name": self.user_group_name,
            "is_active": self.is_active
        }

    @classmethod
    def get_detailed_list(self, client_id, db) :
        user_group_list = []
        rows = db.get_user_group_details()
        for row in rows:
            user_group = UserPrivilege(client_id, int(row[0]), row[1], row[2], 
                [int(x) for x in row[3].split(",")], row[4])
            user_group_list.append(user_group.to_detailed_structure())
        return user_group_list

    @classmethod
    def get_list(self, client_id, db):
        user_group_list = []
        rows = db.get_user_groups()
        for row in rows:
            user_group = UserPrivilege(client_id, int(row[0]), row[1], None, None, int(row[2]))
            user_group_list.append(user_group.to_Structure())
        return user_group_list

class User(object):
    def __init__(self, client_id ,user_id, email_id, user_group_id, employee_name, employee_code, 
        contact_no, seating_unit_id, user_level, country_ids, domain_ids, unit_ids, 
        is_admin, is_service_provider, service_provider_id, is_active ) :
        self.client_id = client_id if client_id != None else 0
        self.user_id =  user_id 
        self.email_id =  email_id
        self.user_group_id =  user_group_id
        self.employee_name =  employee_name
        self.employee_code =  employee_code
        self.contact_no =  contact_no
        self.seating_unit_id =  seating_unit_id
        self.user_level =  user_level
        self.country_ids =  country_ids
        self.domain_ids =  domain_ids
        self.unit_ids =  unit_ids
        self.is_admin =  is_active if is_active != None else 0
        self.is_active =  is_active if is_active != None else 1
        self.is_service_provider =  is_service_provider
        self.service_provider_id =  service_provider_id

    @classmethod
    def initialize_with_request(self, request, user_id, client_id):
        email_id = ""
        try:
            email_id = str(request["email_id"])
        except:
            print "Updating User"
        user_group_id = int(request["user_group_id"])
        employee_name = str(request["employee_name"])
        employee_code = str(request["employee_code"])
        contact_no = str(request["contact_no"])
        seating_unit_id =  int(request["seating_unit_id"])
        user_level =  int(request["user_level"])
        country_ids = request["country_ids"]
        domain_ids = request["domain_ids"]
        unit_ids = request["unit_ids"]
        is_service_provider = int(request["is_service_provider"])
        service_provider_id = request["service_provider_id"]
        user = User(client_id ,user_id, email_id, user_group_id, employee_name, 
            employee_code, contact_no, seating_unit_id, user_level, country_ids, 
            domain_ids, unit_ids, None, is_service_provider, 
            service_provider_id, None)
        return user

    def to_detailed_structure(self) :
        employee_name = "%s - %s" % (self.employee_code,self.employee_name)
        return {
            "user_id": self.user_id,
            "email_id": self.email_id,
            "user_group_id": self.user_group_id,
            "employee_name": employee_name,
            "contact_no": self.contact_no,
            "seating_unit_id": self.seating_unit_id, 
            "user_level": self.user_level,
            "country_ids": self.country_ids,
            "domain_ids": self.domain_ids,
            "unit_ids": self.unit_ids,
            "is_admin": self.is_admin,
            "is_active": self.is_active,
            "is_service_provider": self.is_service_provider,
            "service_provider_id": self.service_provider_id
        }

    def to_Structure(self):
        employee_name = None
        if self.employee_code == None:
            employee_name = self.employee_name
        else:
            employee_name = "%s-%s" % (self.employee_code, self.employee_name)
        return {
            "user_id": self.user_id,
            "employee_name": employee_name,
            "user_level": self.user_level
        }

    @classmethod
    def get_detailed_list(self, client_id, db):
        user_list = []
        rows = db.get_client_user_details_list()
        for row in rows:
            user_id = int(row[0])
            email_id = row[1]
            user_group_id = int(row[2]) if row[2] != None else None
            employee_name = row[3]
            employee_code = row[4]
            contact_no =  row[5]
            seating_unit_id = int(row[6]) if row[6] != None else None
            user_level = int(row[7]) if row[7] != None else None
            country_ids = [int(x) for x in row[8].split(",")]
            domain_ids = [int(x) for x in row[9].split(",")]
            unit_ids = [int(x) for x in row[10].split(",")] if row[10] != None else None
            is_admin = int(row[11])
            is_service_provider = int(row[12])
            is_active = int(row[13])
            user = User(client_id,user_id, email_id, user_group_id, employee_name, employee_code,
                         contact_no, seating_unit_id, user_level, country_ids, domain_ids, unit_ids, 
                         is_admin, is_service_provider,None, is_active) 
            user_list.append(user.to_detailed_structure())
        return user_list

    @classmethod
    def get_list(self, client_id, db):
        user_list = []
        rows = db.get_client_user_list()
        for row in rows:
            user_id = int(row[0])
            employee_name = row[1]
            employee_code = row[2]
            is_active = int(row[3])
            user = User(client_id, user_id, None, employee_name, employee_code,
                 None, None, None, None, None, None, None, is_active)
            user_list.append(user.to_Structure())
        return user_list


class BusinessGroup(object):
    def __init__(self, business_group_id, business_group_name, client_id):
        self.client_id = client_id
        self.business_group_id = business_group_id 
        self.business_group_name = business_group_name

    def to_Structure(self) :
        return {
            "business_group_id": self.business_group_id,
            "business_group_name": self.business_group_name,
            "client_id": self.client_id
        }

    @classmethod
    def get_list(self, client_id, db):
        business_group_list = []
        rows = db.get_business_groups()
        for row in rows:
            business_group_id = int(row[0])
            business_group_name = row[1]
            business_group = BusinessGroup(business_group_id, business_group_name, client_id)
            business_group_list.append(business_group.to_Structure())

        return business_group_list

class LegalEntity(object):

    def __init__(self, legal_entity_id, legal_entity_name, business_group_id, client_id):
        self.client_id = client_id
        self.legal_entity_id = legal_entity_id 
        self.legal_entity_name = legal_entity_name
        self.business_group_id = business_group_id

    def to_Structure(self) :
        return {
            "legal_entity_id": self.legal_entity_id,
            "legal_entity_name": self.legal_entity_name,
            "business_group_id": self.business_group_id,
            "client_id": self.client_id
        }

    @classmethod
    def get_list(self, client_id, db):
        legal_entities_list = []
        rows = db.get_legal_entities()
        for row in rows:
            legal_entity_id = int(row[0])
            legal_entity_name = row[1]
            business_group_id = int(row[2])
            legal_entity = LegalEntity(legal_entity_id, legal_entity_name, business_group_id, client_id)
            legal_entities_list.append(legal_entity.to_Structure())
        return legal_entities_list

class Division(object):
    def __init__(self, division_id, division_name,legal_entity_id, business_group_id, client_id):
        self.client_id = client_id
        self.division_id = division_id 
        self.division_name = division_name
        self.legal_entity_id = legal_entity_id
        self.business_group_id = business_group_id

    def to_Structure(self) :
        return {
            "division_id": self.division_id,
            "division_name": self.division_name,
            "legal_entity_id": self.legal_entity_id,
            "business_group_id": self.business_group_id,
            "client_id": self.client_id
        }

    @classmethod
    def get_list(self, client_id, db):
        divisions_list = []
        rows = db.get_divisions()     
        for row in rows:
            division_id = int(row[0])
            division_name = row[1]
            legal_entity_id = int(row[2])
            business_group_id = int(row[2])
            division = Division(division_id, division_name, legal_entity_id, 
                        business_group_id, client_id)
            divisions_list.append(division.to_Structure())

        return divisions_list

class Unit(object):

    def __init__(self, unit_id, division_id, legal_entity_id, business_group_id, client_id, 
                country_id, geography_id, unit_code, unit_name, industry_id, address, 
                postal_code, domain_ids, is_active, industry_name, geography):
        self.client_id = client_id
        self.unit_id = int(unit_id)
        self.division_id = division_id
        self.legal_entity_id = legal_entity_id
        self.business_group_id = business_group_id
        self.country_id = country_id
        self.geography_id = geography_id
        self.unit_code = unit_code
        self.unit_name = unit_name
        self.industry_id = industry_id
        self.address = address
        self.postal_code = postal_code
        self.domain_ids = domain_ids
        self.is_active = is_active if is_active != None else 1
        self.industry_name = industry_name
        self.geography = geography

    def to_detailed_structure(self) :
        return {
            "unit_id": self.unit_id,
            "division_id": self.division_id,
            "legal_entity_id": self.legal_entity_id,
            "business_group_id": self.business_group_id,
            "client_id"  : self.client_id,
            "country_id": self.country_id,
            "geography_id": self.geography_id,
            "unit_code": self.unit_code,
            "unit_name": self.unit_name,
            "industry_id": self.industry_id,
            "unit_address": self.address,
            "postal_code": self.postal_code,
            "domain_ids": self.domain_ids,
            "is_active": self.is_active
        }

    def to_Structure(self):
        unit_name = "%s - %s" % (self.unit_code, self.unit_name)
        return{
            "unit_id": self.unit_id,
            "division_id": self.division_id,
            "legal_entity_id": self.legal_entity_id,
            "business_group_id": self.business_group_id,
            "client_id": self.client_id,
            "country_id": self.country_id,
            "domain_ids": self.domain_ids,
            "unit_name": unit_name,
            "unit_address": self.address
        }

    @classmethod
    def get_list(self, client_id , db):
        unit_list = []
        rows = db.get_units()
        for row in rows:
            unit_id = row[0]
            division_id = int(row[1])
            legal_entity_id = int(row[2])
            business_group_id = int(row[3])
            unit_code = row[4]
            unit_name = row[5]
            country_id = int(row[6])
            address = row[7]
            domain_ids = [int(x) for x in row[8].split(",")]
            unit = Unit(unit_id, division_id, legal_entity_id, business_group_id, 
                        client_id, country_id, None, unit_code, unit_name,
                        None, address, None, domain_ids, None, None, None)
            unit_list.append(unit.to_Structure())
        return unit_list

    @classmethod
    def get_unit_list_for_closure(self, client_id, db):
        unit_list = []
        rows = db.get_units_closure_list()
        for row in rows:
            unit_structure = {}
            unit_structure["business_group_name"] = str(row[0])
            unit_structure["legal_entity_name"] = str(row[1])
            unit_structure["division_name"] = str(row[2])
            unit_structure["unit_id"] = int(row[3])
            unit_structure["unit_name"] = "%s - %s" % (str(row[4]), str(row[5]))
            unit_structure["address"] = str(row[6])
            unit_structure["is_active"] = int(row[7])
            unit_list.append(unit_structure)
        return unit_list