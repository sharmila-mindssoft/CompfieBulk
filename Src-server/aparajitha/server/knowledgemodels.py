__all__ = [
    "Country",
    "Domain",
    "UserGroup"
]

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
