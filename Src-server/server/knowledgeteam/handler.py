import json
import os
from tornado.web import StaticFileHandler
from collections import OrderedDict
from server.common import cors_handler

from server.constants import ROOT_PATH, HTTP_PORT

__all__ = [
    "KnowledgeteamHandler"
]

template_path = {
    "statutory-level": ("web/knowledge-team/statutory-level-master/StatutoryLevelMaster.html", None, {}),
    "statutory-master": ("web/knowledge-team/statutory-master/StatutoryMaster.html", None, {}),
    "statutory-mapping": ("web/knowledge-team/statutory-mapping/StatutoryMapping.html", None, {}),
}
def get_template_path(key) :
    return template_path.get(key)[0]

#
# StatutoryLevelHandler
#

class StatutoryLevelHandler(object) :
    def __init__ (self, io_loop, db, env, countryList) :
        self._io_loop = io_loop
        self._db = db
        self._env = env
        self._country = countryList

    
    def _get_country_level(self) :
        query = "SELECT distinct(country_code), status FROM StatutoryLevel";
        country = self._db.fetchAll(query);
        countries = []
        i = 1;
        for c in country :
            countries.append((i, c[0], c[1]))
            i += 1
        return countries

    def handle_get_statutory_list(self, request, response) :
        path = get_template_path("statutory-level")
        template = self._env.get_template(path)
        countries = self._get_country_level()
        output = template.render(mode="view", countryList=countries)
        response.send(output)

    def get_data(self, country_code) :
        query = "SELECT level_id, level, title, country_code, status " + \
                " FROM StatutoryLevel where LOWER(country_code) = LOWER('%s') ORDER BY level" % ( country_code )
        data = self._db.fetchAll(query)
        return data

    def handle_get_statutory_list_by_country(self, request, response) :
        country_code = request.parameter("country")
        data = self.get_data(country_code)
        response.send(json.dumps(data))

    def handle_add_statutory_list(self, request, response) :
        path = get_template_path("statutory-level")
        template = self._env.get_template(path)
        output = template.render(mode="add", country="")
        response.send(output)

    def handle_save_statutory_list(self, request, response) :
        level_list = json.loads(request.parameter("levels"))
        country_code = request.parameter("country")

        select_query = "SELECT level_id,level,title FROM StatutoryLevel where country_code='%s'" % (country_code)
        data = self._db.fetchAll(select_query)
        old_level = [];
        for d in data :
            old_level.append(d[2])

        for level in level_list :
            if level[2] > 0 :
                query = "UPDATE StatutoryLevel set title='%s' where level_id=%s" % (level[1], level[2])
            else :
                if level[1] not in old_level :
                    query = "INSERT INTO StatutoryLevel(level, title, country_code, status) VALUES (%s, '%s', '%s', 'A')" % (
                        level[0], level[1], country_code
                    )
            self._db.commit(query)

        response.set_content_type("application/json")
        response.send(json.dumps('data saved'));

    def handle_edit_statutory_list(self, request, response) :
        country_code = request.parameter("country")
        path = get_template_path("statutory-level")
        template = self._env.get_template(path)
        data = self.get_data(country_code)
        output = template.render(mode="edit", levels=data, country=country_code)
        response.send(output)

    def handle_status_statutory_list(self, request, response) :
        country_code = request.parameter("country")
        s_query = "SELECT distinct(status) from StatutoryLevel where LOWER(country_code) = LOWER('%s')" % (country_code)
        status = self._db.fetchOne(s_query)
        if (status[0] == 'A') :
            s = 'D'
        else :
            s = 'A'
        query = "UPDATE StatutoryLevel SET status='%s' where LOWER(country_code) = LOWER('%s') " % (s, country_code)
        self._db.commit(query)
        response.send(json.dumps(s))

    def configure(self, web_server) :
        urls = [
            ("/statutory-level", self.handle_get_statutory_list),
            ("/statutory-level/list", self.handle_get_statutory_list_by_country),
            ("/statutory-level/add", self.handle_add_statutory_list),
            ("/statutory-level/save", self.handle_save_statutory_list),
            ("/statutory-level/edit", self.handle_edit_statutory_list),
            ("/statutory-level/status", self.handle_status_statutory_list)
        ]
        for relative_url, handler in urls :
            web_server.url(
                relative_url, GET=handler, POST=handler, OPTIONS=cors_handler
            )
        

class StatutoryMasterHandler(object) :
    def __init__ (self, io_loop, db, env, countryList) :
        self._io_loop = io_loop
        self._db = db
        self._env = env
        self._country = countryList

    def _get_statutory(self) :
        query = " SELECT T2.id, T2.country_code, T1.level, T1.title, T2.title, T2.status FROM StatutoryMaster T2 " + \
         " inner join StatutoryLevel T1 on T1.level_id = T2.level_id order by T2.country_code,T1.level "
        data = self._db.fetchAll(query)
        master_list = []
        i = 1
        for d in data :
            master_list.append((i, d[0], d[1], d[3], d[4]))
            i += 1
        return master_list

    def _get_statutory_by_level(self, country, parentid) :
        query = "SELECT T2.country_code, T2.id, T1.level, T1.title, T2.title  FROM StatutoryMaster T2 " + \
        " inner join StatutoryLevel T1 on T1.level_id = T2.level_id where AND T2.status = 'A' " + \
        " LOWER(T2.country_code)=LOWER('%s') AND " + \
        " T2.parentid = '%s' "
        data = self._db.fetchAll(query)
        data_list = []
        i = 1
        for d in data :
            data_list.append((i, d[0], d[1], d[3], d[4]))
            i += 1
        return data_list

    def handle_get_statutory_master(self, request, response) :
        path = get_template_path("statutory-master")
        template = self._env.get_template(path)
        master_list = self._get_statutory()
        output = template.render(mode="view", masterList=master_list)
        response.send(output)

    def handle_add_statutory_master(self, request, response) :
        path = get_template_path("statutory-master")
        template = self._env.get_template(path)
        output = template.render(mode="add")
        response.send(output)

    def handle_get_statutory_master_by_country(self, request, response) :
        country_code = request.parameter("country")
        parentid = request.parameter("parentid")
        data = self._get_statutory_by_level(country_code, parentid)
        response.send(json.dumps(data))

    def configure (self, web_server) :
        urls = [
            ("/statutory-master", self.handle_get_statutory_master),
            ("/statutory-master/list", self.handle_get_statutory_master_by_country),
            ("/statutory-master/add", self.handle_add_statutory_master)
            # ("/statutory-master/save", self.handle_save_statutory_master),
            # ("/statutory-master/edit", self.handle_edit_statutory_master),
            # ("/statutory-master/status", self.handle_status_statutory_master)
        ]
        for relative_url, handler in urls :
            web_server.url(
                relative_url, GET=handler, POST=handler, OPTIONS=cors_handler
            )
        

class KnowledgeteamHandler(object) :
    def __init__ (self, io_loop, db, env, countryList) :
        self._io_loop = io_loop
        self._db = db
        self._env = env
        self._country = countryList

    def configure (self, web_server) :
        statutory_handler = StatutoryLevelHandler(
            self._io_loop, self._db, self._env, self._country
        )
        statutory_handler.configure(web_server)

        statutory_master_handler = StatutoryMasterHandler (
            self._io_loop, self._db, self._env, self._country   
        )
        statutory_master_handler.configure(web_server)

        STATIC_PATH = os.path.join(ROOT_PATH, "Src-client", "web", "knowledge-team", "script")
        web_server.low_level_url(
            "/Static/knowledge-team/(.*)", StaticFileHandler, dict(path=STATIC_PATH)
        )
    