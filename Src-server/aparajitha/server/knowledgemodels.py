__all__ = [
    "Country",
    "Domain"
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