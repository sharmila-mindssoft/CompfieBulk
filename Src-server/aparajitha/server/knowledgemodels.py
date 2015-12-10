from aparajitha.misc.client_mappings import client_db_mappings
from aparajitha.server.clientdatabase import ClientDatabase
from aparajitha.misc.dates import *

__all__ = [
    "Country",
    "Domain",
    "UserGroup",
    "AdminUser",
    "GroupCompany"
]

_client_db = None

def _get_database(client_id) :
    database_name = None
    if client_id is None :
        return None
    database_name = client_db_mappings[client_id]
    _client_db = ClientDatabase(database_name)
    return _client_db

class Country(object) :
    def __init__(self, country_id, country_name, is_active) :
        self.country_id = country_id
        self.country_name = country_name
        self.is_active = is_active

    def to_structure(self) :
        return {
            "country_id": self.country_id,
            "country_name": self.country_name,
            "is_active": self.is_active
        }

    @classmethod
    def get_list(self, db):
        country_list = []
        # try:
        rows = db.get_countries()
        for row in rows:
            country_id = int(row[0])
            country_name = row[1]
            is_active = row[2]
            country = Country(country_id, country_name, is_active)
            country_list.append(country.to_structure())
        # except:
        #     print "Error: While fetching Countries"
        return country_list

class Domain(object) :
    def __init__(self, domain_id, domain_name, is_active) :
        self.domain_id = domain_id
        self.domain_name = domain_name
        self.is_active = is_active

    def to_structure(self) :
        return {
            "domain_id": self.domain_id,
            "domain_name": self.domain_name,
            "is_active": self.is_active
        }

    @classmethod
    def get_list(self, db):
        domain_list = []
        # try:
        rows = db.get_domains()
        for row in rows:
            domain_id = int(row[0])
            domain_name = row[1]
            is_active = row[2]
            domain = Domain(domain_id, domain_name, is_active)
            domain_list.append(domain.to_structure())
        # except:
        #     print "Error: While fetching Countries"
        return domain_list

class UserGroup() :
    def __init__(self, user_group_id, user_group_name, form_type, form_ids, is_active) :
        self.user_group_id =  user_group_id 
        self.user_group_name = user_group_name
        self.form_type = form_type 
        self.form_ids = form_ids 
        self.is_active = is_active if is_active != None else 1

    @classmethod
    def initialize_with_request(self, request, user_group_id):
        user_group_name = str(request["user_group_name"])
        form_type = str(request["form_type"])
        form_ids =  request["form_ids"]
        user_group = UserGroup(user_group_id, user_group_name, form_type, form_ids, None)
        return user_group

    def to_detailed_structure(self) :
        return {
            "user_group_id": int(self.user_group_id),
            "user_group_name": str(self.user_group_name),
            "form_type": str(self.form_type),
            "form_ids": self.form_ids,
            "is_active": int(self.is_active)
        }

    def to_structure(self):
        return {
            "user_group_id": int(self.user_group_id),
            "user_group_name": str(self.user_group_name),
            "is_active": int(self.is_active)
        }

    @classmethod
    def get_detailed_list(self, db) :
        user_group_list = []
        rows = db.get_user_group_details_list()
        for row in rows:
            form_ids = [int(x) for x in row[3].split(",")]
            user_group = UserGroup(int(row[0]), row[1], row[2], form_ids, row[4])
            user_group_list.append(user_group.to_detailed_structure())
        return user_group_list

    @classmethod
    def get_list(self, db):
        user_group_list = []
        rows = db.get_user_group_list()
        for row in rows:
            user_group = UserGroup(int(row[0]), row[1], None, None, row[2])
            user_group_list.append(user_group.to_structure())
        return user_group_list

class AdminUser(object) :
    def __init__(self, user_id, email_id, user_group_id, form_type,employee_name, 
                employee_code, contact_no, address, designation, country_ids,
                domain_ids, client_id,is_active) :
        self.user_id =  int(user_id)
        self.email_id =  str(email_id)
        self.user_group_id =  int(user_group_id) if user_group_id != None else None
        self.form_type = str(form_type) if form_type != None else None
        self.employee_name =  str(employee_name)
        self.employee_code =  str(employee_code)
        self.contact_no =  str(contact_no)
        self.address =  str(address)
        self.designation =  str(designation)
        self.country_ids =  country_ids
        self.domain_ids =  domain_ids
        self.client_id = client_id 
        self.is_active = int(is_active) if is_active != None else 1

    @classmethod
    def initialize_with_request(self, request, user_id):
        email_id = None
        try:
            email_id = request["email_id"]
        except:
            email_id = None
        user_group_id = request["user_group_id"]
        employee_name = request["employee_name"]
        employee_code = request["employee_code"]
        contact_no = request["contact_no"]
        address =  request["address"]
        designation =  request["designation"]
        country_ids = request["country_ids"]
        domain_ids = request["domain_ids"]
        user = AdminUser(user_id, email_id, user_group_id, None,employee_name, employee_code, contact_no, 
                    address, designation, country_ids, domain_ids, None,None)
        return user

    def to_detailed_structure(self) :
        return {
            "user_id": self.user_id,
            "email_id": self.email_id,
            "user_group_id": self.user_group_id,
            "employee_name": self.employee_name,
            "employee_code": self.employee_code,
            "contact_no": self.contact_no,
            "address": self.address, 
            "designation": self.designation,
            "country_ids": self.country_ids,
            "domain_ids": self.domain_ids,
            "client_id": self.client_id,
            "is_active": self.is_active
        }

    def to_structure(self):
        employee_name = None
        if self.employee_code == None:
            employee_name = self.employee_name
        else:
            employee_name = "%s-%s" % (self.employee_code, self.employee_name)
        return {
            "user_id": self.user_id,
            "employee_name": employee_name,
        }

    @classmethod
    def get_detailed_list(self, db):
        userList = []
        rows = db.get_user_details_list()    
        for row in rows:
            country_ids = [int(x) for x in row[8].split(",")] if row[8] != None else None
            domain_ids = [int(x) for x in row[9].split(",")] if row[9] != None else None
            user = AdminUser(row[0],row[1], row[2], None,row[3], row[4],
                 row[5], row[6], row[7], country_ids, domain_ids, 
                 row[10], row[11])
            userList.append(user.to_detailed_structure())
        return userList

    @classmethod
    def get_list(self, db):
        userList = []
        rows = db.get_user_list()
        for row in rows:
            user = AdminUser(int(row[0]),None,None, None,row[1], row[2],
                 None, None, None, None, None, None, None)
            userList.append(user.to_structure())
        return userList    

class GroupCompany(object):
    def __init__(self, client_id, group_name, incharge_persons, country_ids ,domain_ids, logo, 
        contract_from, contract_to, no_of_user_licence, file_space, is_sms_subscribed,
        date_configurations, username, is_active):
        self.client_id = client_id
        self.group_name = group_name
        self.incharge_persons = incharge_persons
        self.country_ids = country_ids
        self.domain_ids = domain_ids
        self.logo = logo
        self.contract_from = contract_from
        self.contract_to = contract_to
        self.no_of_user_licence = no_of_user_licence
        self.file_space = file_space
        self.is_sms_subscribed = is_sms_subscribed
        self.date_configurations = date_configurations
        self.username = username
        self.is_active = is_active

    def to_detailed_structure(self) :
        return {
            "client_id": self.client_id,
            "client_name": self.group_name,
            "incharge_persons": self.incharge_persons,
            "country_ids": self.country_ids,
            "domain_ids": self.domain_ids,
            "logo" : self.logo,
            "contract_from": self.contract_from,
            "contract_to": self.contract_to,
            "no_of_user_licence": self.no_of_user_licence,
            "file_space": self.file_space,
            "is_sms_subscribed": self.is_sms_subscribed,
            "date_configurations": self.date_configurations,
            "username": self.username,
            "is_active": self.is_active
        }

    def to_structure(self):
        return {
            "client_id": self.client_id,
            "group_name": self.group_name,
            "country_ids": self.country_ids,
            "domain_ids": self.domain_ids,
            "is_active": self.is_active
        }

    @classmethod
    def get_detailed_list(self, db):
        clientList = []
        client_group_rows = db.get_client_groups()

        for row in client_group_rows:
            client_id = int(row[0])
            group_name = row[1]
            incharge_persons = [int(x) for x in row[2].split(",")]
            is_active = row[3]
            client_db = _get_database(client_id)
            username = client_db.get_client_admin_username()

            settings = client_db.get_client_settings()
            country_ids = [int(x) for x in settings[0]["country_ids"].split(",")]
            domain_ids = [int(x) for x in settings[0]["domain_ids"].split(",")]
            contract_from = datetime_to_string(
                timestamp_to_datetime(settings[0]["contract_from"]))
            contract_to = datetime_to_string(
                timestamp_to_datetime(settings[0]["contract_to"]))
            no_of_user_licence = int(settings[0]["no_of_user_licence"])
            is_sms_subscribed = settings[0]["is_sms_subscribed"]
            file_space = str(settings[0]["total_disk_space"])
            logo = settings[0]["logo_url"]

            date_configurations = ClientConfiguration.get_list(client_db)
            groupCompany = GroupCompany(int(client_id), 
                group_name, incharge_persons, country_ids,
                domain_ids, logo, contract_from, contract_to, 
                no_of_user_licence, file_space, is_sms_subscribed, 
                date_configurations, username, is_active)
            clientList.append(groupCompany.to_detailed_structure())
        return clientList

    @classmethod
    def get_list(self, client_ids):
        clientList = []
        clientDetails = {}
        column = "client_id, group_name, is_active"
        condition = "client_id in (%s)" % client_ids
        clientRows = DatabaseHandler.instance().getData(self.clientTblName, column, condition)

        for row in clientRows:
            clientDetails[str(row[0])] = [row[1], row[2]]

        for index, client_id in enumerate(client_ids.split(",")):
            clientDBName = self.getClienDatabaseName(client_id)
            columns = "country_ids, domain_ids"
            settingsRows = ClientDatabaseHandler.instance(clientDBName).getData(self.clientSettingsTblName,
                columns, "1")

            clientDetail = clientDetails[client_id]
            group_name = clientDetail[0]
            country_ids = settingsRows[0][0]
            domain_ids = settingsRows[0][1]
            is_active = clientDetail[1]
                
            groupCompany = GroupCompany(int(client_id), group_name, None, country_ids ,domain_ids, None, 
                                        None, None, None, None, None,None, None, is_active)
            clientList.append(groupCompany.to_structure())
        return clientList

class ClientConfiguration(object):

    def __init__(self, country_id, domain_id, period_from, period_to):
        self.country_id = country_id
        self.domain_id = domain_id
        self.period_from = period_from
        self.period_to = period_to

    def to_structure(self):
        return {
            "country_id": self.country_id,
            "domain_id": self.domain_id,
            "period_from": self.period_from,
            "period_to": self.period_to
        }

    @classmethod
    def get_list(self, client_db):
        configuration_rows = client_db.get_date_configurations()
        date_configurations = []
        for configuraion in configuration_rows:
            country_id = int(configuraion[0])
            domain_id = int(configuraion[1])
            period_from = int(configuraion[2])
            period_to = int(configuraion[3])
            client_configuration = ClientConfiguration(country_id, domain_id,
                period_from, period_to)
            date_configurations.append(client_configuration.to_structure())

        return date_configurations
