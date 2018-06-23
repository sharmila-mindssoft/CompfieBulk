__all__ = ["UserInfo"]

class UserInfo(object):
    def __init__(self, db, session_user):
        self._db = db
        self._session_user_id = session_user
        self._user_details = {}
        self._user_category_id = None
        self._user_countries = []
        self._user_domains = {}
        self._user_clients = []
        self._user_legal_entities = {}
        self._user_units = {}
        self._user_child_info = []
        self._user_parent_info = []
        self.set_user_info()

    def set_user_info(self):
        data = self._db.call_proc_with_multiresult_set("sp_user_details", [self._session_user_id], 8)
        print "DaTa-> ", data
        if len(data) > 0:
            if len(data[0]) > 0:
                self._user_details = data[0][0]
                self._user_clients = self._user_details.get("user_category_id")

            if len(data[1]) > 0:
                for d in data[1]:
                    self._user_countries.append(d.get("country_id"))

            if len(data[2]) > 0:
                # key is country name value is list of domain id
                for d in data[2]:
                    d_list = self._user_domains.get(d["country_id"])
                    if d_list is None :
                        d_list = []

                    d_list.append(d["domain_id"])
                    self._user_domains[d["country_id"]] = d_list

            if len(data[3]) > 0:
                self._user_child_info = data[3]

            if len(data[4]) > 0:
                self._user_parent_info = data[4]

            if len(data[5]) > 0:
                for d in data[5]:
                    print "d-clientid->> ", d["client_id"]
                    print "_user_clients-> ", self._user_clients
                    # self._user_clients.append(d["client_id"])
                    self._user_clients = d["client_id"]

            if len(data[6]) > 0:
                # key is client id and vlue is list of legal entity id
                for d in data[6]:
                    le_list = self._user_legal_entities.get(d["client_id"])
                    if le_list is None :
                        le_list = []
                    le_list.append(d["legal_entity_id"])
                    self._user_legal_entities[d["client_id"]] = le_list

            if len(data[7]) > 0:
                # key is le id and vlue is list of unit id
                for d in data[7]:
                    u_list = self._user_units.get(d["legal_entity_id"])
                    if u_list is None :
                        u_list = []
                    u_list.append(d["unit_id"])
                    self._user_units[d["legal_entity_id"]] = u_list

    def user_full_name(self):
        return "%s - %s" % (
            self._user_details.get("emploayee_code"),
            self._user_details.get("employee_name")
        )

    def user_id(self):
        return self._session_user_id

    def country_ids(self):
        return self._user_countries

    def user_domains(self):
        return self._user_domains

    def user_units(self):
        return self._user_units

    def client_ids(self):
        return self._user_clients

    def user_le_info(self):
        return self._user_legal_entities

    def manager_info(self):
        return self._user_parent_info

    def executive_info(self):
        return self._user_child_info
