import datetime
import MySQLdb as mysql
import json
from types import *



__all__ = [
    "DatabaseHandler"
]

_databaseHandlerInstance = None

class DatabaseHandler(object) :
    def __init__(self) :
        self.mysqlHost = "localhost"
        self.mysqlUser = "root"
        self.mysqlPassword = "123456"
        self.mysqlDatabase = "mirror_knowledge"
        self.allStatutories = {}
        self.allGeographies = {}

    def dbConnect(self) :
        return mysql.connect(
            self.mysqlHost, self.mysqlUser, 
            self.mysqlPassword, self.mysqlDatabase
        )

    def dataInsertUpdate(self, query) :
        con = None
        cursor = None
        isComplete = True
        try:
            con = self.dbConnect()
            cursor = con.cursor()
            cursor.execute(query)
            con.commit()

        except mysql.Error, e:
            print ("Error:%s - %s" % (query, e))
            isComplete = False

        finally:
            if cursor is not None :
                cursor.close()
            if con is not None :
                con.close()

        return isComplete

    def dataSelect(self, query) :
        con = None
        cursor = None
        result = None
        try:
            con = self.dbConnect()
            cursor = con.cursor()
            cursor.execute(query)
            result = cursor.fetchall()

        except mysql.Error, e:
            print ("Error:%s - %s" % (query, e))

        finally:
            if cursor is not None :
                cursor.close()
            if con is not None :
                con.close()

        return result

    def validateSessionToken(self, sessionToken) :
        query = "SELECT user_id FROM tbl_user_sessions \
        WHERE session_id = '%s'" % sessionToken
        rows = self.dataSelect(query)
        row = rows[0]
        return row[0]

    def getNewId(self, field , tableName) :
        newId = 1
        query = "SELECT max(%s) from %s " % (field, tableName)

        rows = self.dataSelect(query)
        for row in rows :
            if row[0] is not None :
                newId = int(row[0]) + 1
        return newId

    def getDateTime(self) :
        return datetime.datetime.now()

    def saveActivity(self, userId, formId, action, notificationText=None, notificationLink=None):
        createdOn = self.getDateTime()
        activityId = self.getNewId("activity_log_id", "tbl_activity_log")
        query = "INSERT INTO tbl_activity_log(activity_log_id, user_id, form_id, \
            action, ticker_text, ticker_link, created_on) \
            VALUES (%s, %s, %s, '%s', '%s', '%s', '%s')" % (
                activityId, userId, formId, action, str(notificationText), str(notificationLink), createdOn
            )
        self.dataInsertUpdate(query)

    ### Domain ###

    def checkDuplicateDomain(self, domainName, domainId) :
        isDuplicate = False
        query = "SELECT count(*) FROM tbl_domains \
        WHERE LOWER(domain_name) = LOWER('%s') " % domainName
        if domainId is not None :
            query = query + " AND domain_id != %s" % domainId
        rows = self.dataSelect(query)
        row = rows[0]

        if row[0] > 0 :
            isDuplicate = True

        return isDuplicate
            
    def getDomains(self) :
        query = "SELECT domain_id, domain_name, is_active FROM tbl_domains "
        return self.dataSelect(query)

    def saveDomain(self, domainName, createdBy) :
        createdOn = self.getDateTime()
        domainId = self.getNewId("domain_id", "tbl_domains")
        isActive = 1

        query = "INSERT INTO tbl_domains(domain_id, domain_name, is_active, \
            created_by, created_on) VALUES (%s, '%s', %s, %s, '%s') " % (
            domainId, domainName, isActive, createdBy, createdOn
        )

        self.dataInsertUpdate(query)
        action = "Add Domain - \"%s\"" % domainName
        self.saveActivity(createdBy, 4, action)
        return True

    def getDomainByDomainId(self, domainId) :
        q = "SELECT domain_name FROM tbl_domains WHERE domain_id=%s" % domainId
        rows = self.dataSelect(q)
        domainName = rows[0][0]
        return domainName

    def updateDomain(self, domainId, domainName, updatedBy) :
        
        oldData = self.getDomainByDomainId(domainId)
        if oldData is not None :
            query = "UPDATE tbl_domains SET domain_name = '%s', \
            updated_by = %s WHERE domain_id = %s" % (
                domainName, updatedBy, domainId
            )
            self.dataInsertUpdate(query)
            action = "Edit Domain - \"%s\"" % domainName
            self.saveActivity(updatedBy, 4, action)
            return True
        else :
            return False

    def updateDomainStatus(self, domainId, isActive, updatedBy) :
        oldData = self.getDomainByDomainId(domainId)
        if oldData is not None :
            query = "UPDATE tbl_domains SET is_active = %s, \
            updated_by = %s WHERE domain_id = %s" % (
                isActive, updatedBy, domainId
            )
            self.dataInsertUpdate(query)
            if isActive == 0 :
                status = "deactivated"
            else:
                status = "activated"
            action = "Domain %s status  - %s" % (oldData, status)
            self.saveActivity(updatedBy, 4, action)
            return True
        else :
            return False

    ### Country ###

    def getCountries(self) :
        query = "SELECT country_id, country_name, is_active FROM tbl_countries "
        return self.dataSelect(query)

    def checkDuplicateCountry(self, countryName, countryId) :
        isDuplicate = False
        query = "SELECT count(*) FROM tbl_countries \
        WHERE LOWER(country_name) = LOWER('%s') " % countryName
        if countryId is not None :
            query = query + " AND country_id != %s" % countryId
        rows = self.dataSelect(query)
        row = rows[0]

        if row[0] > 0 :
            isDuplicate = True

        return isDuplicate

    def saveCountry(self, countryName, createdBy) :
        createdOn = self.getDateTime()
        countryId = self.getNewId("country_id", "tbl_countries")
        isActive = 1

        query = "INSERT INTO tbl_countries(country_id, country_name, \
            is_active, created_by, created_on) VALUES (%s, '%s', %s, %s, '%s') " % (
            countryId, countryName, isActive, createdBy, createdOn
        )
        self.dataInsertUpdate(query)
        action = "Add Country - \"%s\"" % countryName
        self.saveActivity(createdBy, 4, action)
        return True

    def getCountryByCountryId(self, countryId) :
        q = "SELECT country_name FROM tbl_countries WHERE country_id=%s" % countryId
        rows = self.dataSelect(q)
        countryName = rows[0][0]
        return countryName

    def updateCountry(self, countryId, countryName, updatedBy) :
        oldData = self.getCountryByCountryId(countryId)
        if oldData is not None :
            query = "UPDATE tbl_countries SET country_name = '%s', \
            updated_by = %s WHERE country_id = %s" % (
                countryName, updatedBy, countryId
            )
            self.dataInsertUpdate(query)
            action = "Edit Country - \"%s\"" % countryName
            self.saveActivity(updatedBy, 3, action)
            return True
        else :
            return False

    def updateCountryStatus(self, countryId, isActive, updatedBy) :
        oldData = self.getCountryByCountryId(countryId)
        if oldData is not None :
            query = "UPDATE tbl_countries SET is_active = %s, \
            updated_by = %s WHERE country_id = %s" % (
                isActive, updatedBy, countryId
            )
            if isActive == 0:
                status = "deactivated"
            else:
                status = "activated"
            self.dataInsertUpdate(query)
            action = "Country %s status  - %s" % (oldData, status)
            self.saveActivity(updatedBy, 3, action)
            return True
        else :
            return False

    ### Industry ###

    def getIndustries(self) :
        query = "SELECT industry_id, industry_name, is_active FROM tbl_industries "
        return self.dataSelect(query)

    def checkDuplicateIndustry(self, industryName, industryId) :
        isDuplicate = False
        query = "SELECT count(*) FROM tbl_industries \
            WHERE LOWER(industry_name) = LOWER('%s') " % industryName

        if industryId is not None :
            query = query + " AND industry_id != %s" % industryId
        rows = self.dataSelect(query)
        row = rows[0]

        if row[0] > 0 :
            isDuplicate = True

        return isDuplicate

    def saveIndustry(self, industryName, createdBy) :
        createdOn = self.getDateTime()
        industryId = self.getNewId("industry_id", "tbl_industries")
        isActive = 1

        query = "INSERT INTO tbl_industries(industry_id, industry_name, is_active, \
            created_by, created_on) VALUES (%s, '%s', %s, %s, '%s') " % (
            industryId, industryName, isActive, createdBy, createdOn
        )

        self.dataInsertUpdate(query)
        action = "Add Industry - \"%s\"" % industryName
        self.saveActivity(createdBy, 5, action)
        return True

    def getIndustryByIndustryId(self, industryId) :
        if type(industryId) == IntType :
            qry = "SELECT industry_name FROM tbl_industries WHERE industry_id=%s" % industryId
        else :
            if type(industryId) == ListType :
                ids = industryId
            else :
                ids = [int(x) for x in industryId[:-1].split(',')]
            if (len(ids) == 1) :
                qrywhere = "WHERE industry_id = %s" % ids[0]
            else :
                qrywhere = "WHERE industry_id in %s" % str(tuple(ids))

            qry = " SELECT (GROUP_CONCAT(industry_name SEPARATOR ', ')) as industry_name \
                FROM tbl_industries %s" % qrywhere

        rows = self.dataSelect(qry)
        industryName = str(rows[0][0])
        return industryName

    def updateIndustry(self, industryId, industryName, updatedBy) :
        oldData = self.getIndustryByIndustryId(industryId)
        if oldData is not None :
            query = "UPDATE tbl_industries SET industry_name = '%s', \
            updated_by = %s WHERE industry_id = %s" % (
                industryName, updatedBy, industryId
            )
            self.dataInsertUpdate(query)
            action = "Edit Industry - \"%s\"" % industryName
            self.saveActivity(updatedBy, 5, action)
            return True
        else :
            return False

    def updateIndustryStatus(self, industryId, isActive, updatedBy) :
        oldData = self.getIndustryByIndustryId(industryId)
        if oldData is not None :
            query = "UPDATE tbl_industries SET is_active = %s, updated_by = %s \
            WHERE industry_id = %s" % (
                isActive, updatedBy, industryId
            )
            if isActive == 0:
                status = "deactivated"
            else:
                status = "activated"
            self.dataInsertUpdate(query)
            action = "Industry %s status  - %s" % (oldData, status)
            self.saveActivity(updatedBy, 5, action)
            return True
        else :
            return False

    ### StatutoryNature ###

    def getStatutoryNatures(self) :
        query = "SELECT statutory_nature_id, statutory_nature_name, is_active \
            FROM tbl_statutory_natures "
        return self.dataSelect(query)

    def checkDuplicateStatutoryNature(self, statutoryNatureName, statutoryNatureId) :
        isDuplicate = False

        query = "SELECT count(*) FROM tbl_statutory_natures \
            WHERE LOWER(statutory_nature_name) = LOWER('%s') " % statutoryNatureName

        if statutoryNatureId is not None :
            query = query + " AND statutory_nature_id != %s" % statutoryNatureId
        rows = self.dataSelect(query)
        row = rows[0]

        if row[0] > 0 :
            isDuplicate = True

        return isDuplicate

    def saveStatutoryNature(self, statutoryNatureName, createdBy) :
        createdOn = self.getDateTime()
        statutoryNatureId = self.getNewId("statutory_nature_id", "tbl_statutory_natures")
        isActive = 1

        query = "INSERT INTO tbl_statutory_natures(statutory_nature_id, statutory_nature_name, \
            is_active, created_by, created_on)  VALUES (%s, '%s', %s, %s, '%s') " % (
                statutoryNatureId, statutoryNatureName, isActive, createdBy, createdOn
            )

        self.dataInsertUpdate(query)
        action = "Add Stautory Nature - \"%s\"" % statutoryNatureName
        self.saveActivity(createdBy, 8, action)
        return True

    def getStatutoryNatureById(self, statutoryNatureId) :
        q = "SELECT statutory_nature_name FROM tbl_statutory_natures \
            WHERE statutory_nature_id=%s" % statutoryNatureId
        rows = self.dataSelect(q)
        statutoryNatureName = rows[0][0]
        return statutoryNatureName

    def updateStatutoryNature(self, statutoryNatureId, statutoryNatureName, updatedBy) :
        oldData = self.getStatutoryNatureById(statutoryNatureId)
        if oldData is not None :
            query = "UPDATE tbl_statutory_natures SET statutory_nature_name = \'%s\', \
            updated_by = %s WHERE statutory_nature_id = %s" % (
                statutoryNatureName, updatedBy, statutoryNatureId
            )
            self.dataInsertUpdate(query)
            action = "Edit Stautory Nature - \"%s\"" % statutoryNatureName
            self.saveActivity(updatedBy, 8, action)
            return True
        else :
            return False

    def updateStatutoryNatureStatus(self, statutoryNatureId, isActive, updatedBy) :
        oldData = self.getStatutoryNatureById(statutoryNatureId)
        if oldData is not None :
            query = "UPDATE tbl_statutory_natures SET is_active = %s, \
                updated_by = %s WHERE statutory_nature_id = %s" % (
                    isActive, updatedBy, statutoryNatureId
                )
            if isActive == 0:
                status = "deactivated"
            else:
                status = "activated"
            self.dataInsertUpdate(query)
            action = "Statutory Nature %s status  - %s" % (oldData, status)
            self.saveActivity(updatedBy, 8, action)
            return True
        else :
            return False

    ### StatutoryLevels ###

    def getStatutoryLevels(self) :
        query = "SELECT level_id, level_position, level_name, country_id, domain_id \
            FROM tbl_statutory_levels ORDER BY level_position"
        return self.dataSelect(query)

    def getStatutoryLevelsByID(self, countryId, domainId) :
        query = "SELECT level_id, level_position, level_name \
            FROM tbl_statutory_levels WHERE country_id = %s and domain_id = %s ORDER BY level_position" % (
                countryId, domainId
            )
        return self.dataSelect(query)

    def saveStatutoryLevel(self, countryId, domainId, levelId, levelName, levelPosition, userId) :
        if levelId is None :
            levelId = self.getNewId("level_id", "tbl_statutory_levels")
            createdOn = self.getDateTime()

            query = "INSERT INTO tbl_statutory_levels (level_id, level_position, \
                level_name, country_id, domain_id, created_by, created_on) VALUES (%s, %s, '%s', %s, %s, %s, '%s')" % (
                    levelId, levelPosition, levelName, countryId, domainId, userId, createdOn
                )
            self.dataInsertUpdate(query)
            action = "Add Stautory Levels"
            self.saveActivity(userId, 9, action)
            return True
        else :
            query = "UPDATE tbl_statutory_levels SET level_position=%s, level_name='%s', \
            updated_by=%s WHERE level_id=%s" % (
                levelPosition, levelName, userId, levelId
            )
            self.dataInsertUpdate(query)
            action = "Edit Stautory Levels"
            self.saveActivity(userId, 9, action)
            return True

    ### Geography Levels ###

    def getGeographyLevels(self) :
        query = "SELECT level_id, level_position, level_name, country_id \
            FROM tbl_geography_levels ORDER BY level_position"
        return self.dataSelect(query)

    def getGeographyLevelsByCountry(self, countryId) :
        query = "SELECT level_id, level_position, level_name \
            FROM tbl_geography_levels WHERE country_id = %s ORDER BY level_position" % countryId
        return self.dataSelect(query)

    def saveGeographyLevel(self, countryId, levelId, levelName, levelPosition, userId) :
        if levelId is None :
            levelId = self.getNewId("level_id", "tbl_geography_levels")
            createdOn = self.getDateTime()

            query = "INSERT INTO tbl_geography_levels (level_id, level_position, \
                level_name, country_id, created_by, created_on) VALUES (%s, %s, '%s', %s, %s, '%s')" % (
                    levelId, levelPosition, levelName, countryId, userId, createdOn
                )
            self.dataInsertUpdate(query)
            action = "Add Geography Levels"
            self.saveActivity(userId,6, action)
            return True
        else :
            query = "UPDATE tbl_geography_levels SET level_position=%s, level_name='%s', \
            updated_by=%s WHERE level_id=%s" % (
                levelPosition, levelName, userId, levelId
            )
            self.dataInsertUpdate(query)
            action = "Edit Geography Levels"
            self.saveActivity(userId, 6, action)
            return True

    ### Geographies ###
    def getAllGeographies(self):
        rows = self.getGeographies()
        _tempDict = {}
        for row in rows :
            _tempDict[int(row[0])] = row[1]

        for row in rows :
            parentIds = [int(x) for x in row[3][:-1].split(',')]
            names = []
            names.append(row[6])
            for id in parentIds :
                if id > 0 :
                    names.append(_tempDict.get(id))
                names.append(row[1])
            mappings = '>>'.join(str(x) for x in names)
            self.allGeographies[int(row[0])] = [row[1], mappings, row[3]]

    def getGeographies(self) :
        query = "SELECT t1.geography_id, t1.geography_name, t1.level_id, \
            t1.parent_ids, t1.is_active, t2.country_id, t3.country_name FROM tbl_geographies t1 \
            INNER JOIN tbl_geography_levels t2 on t1.level_id = t2.level_id \
            INNER JOIN tbl_countries t3 on t2.country_id = t3.country_id"
        return self.dataSelect(query)

    def getDuplicateGeographies(self, parentIds, geographyId) :
        query = "SELECT geography_id, geography_name, level_id, is_active \
            FROM tbl_geographies WHERE parent_ids='%s' " % (parentIds)
        if geographyId is not None :
            query = query + " AND geography_id != %s" % geographyId
        return self.dataSelect(query)

    def saveGeographies(self, name, levelId, parentIds, userId) :
        geographyId = self.getNewId("geography_id", "tbl_geographies")
        createdOn = self.getDateTime()

        query = "INSERT INTO tbl_geographies (geography_id, geography_name, level_id, \
            parent_ids, created_by, created_on) VALUES (%s, '%s', %s, '%s', %s, '%s')" % (
                geographyId, name, levelId, parentIds, userId, createdOn
            )
        self.dataInsertUpdate(query)
        self.getAllGeographies()
        action = "Add Geography - %s" % name
        self.saveActivity(userId, 7, action)
        return True

    def updateGeographyMaster(self, geographyId, name, parentIds, updatedBy) :
        oldData = self.allGeographies.get(geographyId)
        oldParentIds = oldData[2]
        query = "UPDATE tbl_geographies set geography_name='%s', parent_ids='%s',\
            updated_by=%s WHERE geography_id=%s " % (
                name, parentIds, updatedBy, geographyId
            )
        self.dataInsertUpdate(query)
        action = "Edit Geography - %s" % name
        self.saveActivity(updatedBy, 7, action)
        if oldParentIds != parentIds :
            oldPId = str(oldParentIds) + str(geographyId)
            newPId = str(parentIds) + str(geographyId)
            qry = "SELECT geography_id, geography_name, parent_ids from tbl_geographies \
                WHERE parent_ids like '%s'" % str("%" + str(oldPId) + ",%")
            rows = self.dataSelect(qry)
            for row in rows :
                newParentId = str(row[2]).replace(oldPId, newPId)
                q = "UPDATE tbl_geographies set parent_ids='%s', updated_by=%s where geography_id=%s" % (
                    newParentId, updatedBy, row[0]
                )
                self.dataInsertUpdate(q)
            action = "Edit Geography Mappings Parent"
            self.saveActivity(updatedBy, 7, action)
        self.getAllGeographies()
        return True

    def changeGeographyStatus(self,geographyId, isActive, updatedBy) :
        query = "UPDATE tbl_geographies set is_active=%s, updated_by=%s WHERE geography_id=%s" % (
            isActive, updatedBy, geographyId
        )
        self.dataInsertUpdate(query)
        if isActive == 0:
            status = "deactivated"
        else:
            status = "activated"
        name = self.allGeographies.get(geographyId)[0]
        action = "Geography %s status  - %s" % (name, status)
        self.saveActivity(updatedBy, 7, action)
        return True

    ### Statutory ###
    def getAllStatutories(self):
        rows = self.getStatutories()
        _tempDict = {}
        for row in rows :
            _tempDict[int(row[0])] = row[1]

        for row in rows :
            parentIds = [int(x) for x in row[3][:-1].split(',')]
            names = []
            for id in parentIds :
                if id > 0 :
                    names.append(_tempDict.get(id))
                names.append(row[1])
            mappings = '>>'.join(str(x) for x in names)
            self.allStatutories[int(row[0])] = [row[1], mappings, row[3]]
                
    def getStatutories(self) :
        query = "SELECT t1.statutory_id, t1.statutory_name, t1.level_id, t1.parent_ids, \
            t2.country_id, t3.country_name, t2.domain_id, t4.domain_name \
            FROM tbl_statutories t1 \
            INNER JOIN tbl_statutory_levels t2 on t1.level_id = t2.level_id \
            INNER JOIN tbl_countries t3 on t2.country_id = t3.country_id \
            INNER JOIN tbl_domains t4 on t2.domain_id = t4.domain_id"
        return self.dataSelect(query)

    def getStatutoryWithMappings(self) :
        query = "SELECT t1.statutory_id, t1.statutory_name, t1.parent_ids FROM tbl_statutories t1"
        _rows = self.dataSelect(query)
        statutoryNames = {}
        statutoryMapping = {}

        for row in _rows :
            statutoryNames[int(row[0])] = row[1]

        for geo in _rows :
            parentIds = [int(x) for x in geo[2][:-1].split(',')]
            names = []
            for id in parentIds :
                if id > 0 :
                    names.append(statutoryNames.get(id))
                names.append(geo[1])

            statutoryMapping [int(geo[0])] = '>>'.join(str(x) for x in names)

        return statutoryMapping

    def getStatutoriesByIds(self, statutoryIds) :
        if type(statutoryIds) == IntType :
            qry = " WHERE t1.statutory_id = %s" %  statutoryIds
        else :
            ids = (int(x) for x in statutoryIds.split(','))
            qry = " WHERE t1.statutory_id in (%s)" % str(ids)

        query = "SELECT t1.statutory_id, t1.statutory_name, t1.level_id, t1.parent_ids, \
            t2.country_id, t3.country_name, t2.domain_id, t4.domain_name \
            FROM tbl_statutories t1 \
            INNER JOIN tbl_statutory_levels t2 on t1.level_id = t2.level_id \
            INNER JOIN tbl_countries t3 on t2.country_id = t3.country_id \
            INNER JOIN tbl_domains t4 on t2.domain_id = t4.domain_id %s" % qry
        return self.dataSelect(query)        

    def getDuplicateStatutories(self, parentIds, statutoryId) :
        query = "SELECT statutory_id, statutory_name, level_id \
            FROM tbl_statutories WHERE parent_ids='%s' " % (parentIds)
        if statutoryId is not None :
            query = query + " AND statutory_id != %s" % statutoryId
        return self.dataSelect(query)

    def saveStatutories(self, name, levelId, parentIds, userId) :
        statutoryId = self.getNewId("statutory_id", "tbl_statutories")
        createdOn = self.getDateTime()

        query = "INSERT INTO tbl_statutories (statutory_id, statutory_name, level_id, \
            parent_ids, created_by, created_on) VALUES (%s, '%s', %s, '%s', %s, '%s')" % (
                statutoryId, name, levelId, parentIds, userId, createdOn
            )
        if (self.dataInsertUpdate(query)) :
            self.getAllStatutories()
            action = "Add Statutory - %s" % name
            self.saveActivity(userId, 17, action)
            return True

    def updateStatutories(self, statutoryId, name, parentIds, updatedBy) :
        oldData = self.allStatutories.get(statutoryId)
        oldParentIds = oldData[2]
        query = "UPDATE tbl_statutories set statutory_name='%s', parent_ids='%s',\
            updated_by=%s WHERE statutory_id=%s " % (
                name, parentIds, updatedBy, statutoryId
            )
        self.dataInsertUpdate(query)
        action = "Edit Statutory - %s" % name
        self.saveActivity(updatedBy, 17, action)
        if oldParentIds != parentIds :
            oldPId = str(oldParentIds) + str(statutoryId)
            newPId = str(parentIds) + str(statutoryId)
            qry = "SELECT statutory_id, statutory_name, parent_ids from tbl_statutories \
                WHERE parent_ids like '%s'" % str("%" + str(oldPId) + ",%")
            rows = self.dataSelect(qry)
            for row in rows :
                newParentId = str(row[2]).replace(oldPId, newPId)
                q = "UPDATE tbl_statutories set parent_ids='%s', updated_by=%s where statutory_id=%s" % (
                    newParentId, updatedBy, row[0]
                )
                self.dataInsertUpdate(q)
            action = "Edit Statutory Mappings Parent"
            self.saveActivity(updatedBy, 17, action)
        self.getAllStatutories()
        return True


    def updateStatutoryMappingId(self, statutoryIds, mappingId, updatedBy) :
        # remove mapping id
        mapId = str("%" + str(mappingId) + ",%")
        q = "SELECT statutory_id, statutory_mapping_ids from tbl_statutories \
            WHERE statutory_mapping_ids like '%s'" % mapId
        rows = self.dataSelect(q)
        oldStatuIds = {}
        for row in rows :
            oldStatuIds[int(row[0])] = row[1][:-1]
        difference = list(set(oldStatuIds.keys()) - set(statutoryIds))

        for x in difference :
            oldMapId =  [int(j) for j in oldStatuIds.get(x).split(',')]
            oldMapId = oldMapId.remove(mappingId)

            newMapId = ""
            if oldMapId is not None : 
                newMapId = ','.join(str(k) for k in oldMapId) + ","

            qry1 = "UPDATE tbl_statutories set statutory_mapping_ids = '%s', updated_by = %s \
                WHERE statutory_id = %s" % (newMapId, updatedBy, x)
            if (self.dataInsertUpdate(qry1)) :
                print "Mapping Id %s removed from statutory table, Id=%s" % (mappingId, x)


        # statutoryIds = statutoryIds[:-1]
        # ids = [int(x) for x in statutoryIds.split(',')]
        ids = tuple(statutoryIds)
        if (len(ids) == 1) :
            qryWhere = " WHERE statutory_id = %s" % ids[0]
        else :
            qryWhere = " WHERE statutory_id in %s" % str(ids)

        qry = "SELECT statutory_id, statutory_mapping_ids from tbl_statutories %s" % qryWhere
        isUpdated = False
        rows = self.dataSelect(qry)
        for row in rows:
            statutoryId = int(row[0])

            if row[1] is None : 
                mapId = ""
            else :
                mapId = row[1]
            _statutoryMappingId = str(mappingId) + ","
            if (len(mapId) > 0):
                mappingIds = [int(x) for x in row[1][:-1].split(',')]
                if (mappingId not in mappingIds) :
                    mappingIds.append(mappingId)
                _statutoryMappingId = ','.join(str(x) for x in mappingIds) + ","
            query = "UPDATE tbl_statutories set statutory_mapping_ids = '%s', updated_by = %s \
                WHERE statutory_id = %s" % (
                _statutoryMappingId, updatedBy, statutoryId
            )
            isUpdated = self.dataInsertUpdate(query)
        return isUpdated


    ### Compliance ###
    def getCompliancesByIds(self, complianceIds) :
        if type(complianceIds) == IntType :
            qry = " WHERE t1.compliance_id = %s" %  complianceIds
        else :
            # ids = (int(x) for x in complianceIds.split(','))
            if (len(complianceIds) == 1):
                qry = " WHERE t1.compliance_id in (%s)" % complianceIds[0]
            else :
                qry = " WHERE t1.compliance_id in %s" % str(tuple(complianceIds))

        query = "SELECT t1.compliance_id, t1.statutory_provision, t1.compliance_task, \
            t1.compliance_description, t1.document_name, t1.format_file, t1.penal_consequences, \
            t1.compliance_frequency, t1.statutory_dates, t1.repeats_every, t1.repeats_type, \
            t1.duration, t1.duration_type, t1.is_active \
            FROM tbl_compliances t1 %s" % qry
        return self.dataSelect(query)

    def saveCompliance(self, mappingId, datas, createdBy) :
        complianceIds = []
        for data in datas :
            complianceId = self.getNewId("compliance_id", "tbl_compliances")
            createdOn = self.getDateTime()

            statutoryProvision = data.get("statutory_provision")
            complianceTask = data.get("compliance_task")
            complianceDescription = data.get("description")
            documentName = data.get("document")
            formatFile = data.get("format_file_name")
            penalConsequences = data.get("penal_consequences")
            complianceFrequency = data.get("compliance_frequency")
            statutoryDates =  json.dumps(data.get("statutory_dates"))
            repeatsEvery = data.get("repeats_every")
            repeatsType = data.get("repeats_type")
            duration = data.get("duration")
            durationType = data.get("duration_type")
            isActive = data.get("is_active")

            if complianceFrequency == "OneTime" :
                query = "INSERT INTO tbl_compliances (compliance_id, statutory_provision, \
                    compliance_task, compliance_description, document_name, format_file, \
                    penal_consequences, compliance_frequency, statutory_dates, statutory_mapping_id, \
                    is_active, created_by, created_on) VALUES (%s, '%s', '%s', '%s', '%s', '%s', '%s', '%s', \
                    '%s', %s, %s, %s, '%s')" % (complianceId, statutoryProvision, complianceTask, 
                    complianceDescription, documentName, formatFile, penalConsequences, complianceFrequency,
                    statutoryDates, mappingId, isActive, createdBy, createdOn)

            elif complianceFrequency == "OnOccurrence" :
                query = "INSERT INTO tbl_compliances (compliance_id, statutory_provision, \
                    compliance_task, compliance_description, document_name, format_file, \
                    penal_consequences, compliance_frequency, statutory_dates, duration, \
                    duration_type, statutory_mapping_id, \
                    is_active, created_by, created_on) VALUES (%s,'%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', %s, \
                    '%s', %s, %s, %s, '%s')" % (complianceId, statutoryProvision, complianceTask, 
                    complianceDescription, documentName, formatFile, penalConsequences, complianceFrequency,
                    statutoryDates, int(duration), durationType, mappingId, isActive, createdBy, createdOn)

            else :
                query = "INSERT INTO tbl_compliances (compliance_id, statutory_provision, \
                    compliance_task, compliance_description, document_name, format_file, \
                    penal_consequences, compliance_frequency, statutory_dates, repeats_every, \
                    repeats_type, statutory_mapping_id, \
                    is_active, created_by, created_on) VALUES (%s, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', \
                    %s, '%s', %s, %s, %s, '%s')"  % (complianceId, statutoryProvision, complianceTask, 
                    complianceDescription, documentName, formatFile, penalConsequences, complianceFrequency,
                    statutoryDates, int(repeatsEvery), repeatsType, mappingId, isActive, createdBy, createdOn)

            if (self.dataInsertUpdate(query)) :
                complianceIds.append(complianceId)

        return complianceIds

    def updateCompliance(self, mappingId, datas, updatedBy) :
        complianceIds = []
        for data in datas :
            complianceId = data.get("compliance_id")
            statutoryProvision = data.get("statutory_provision")
            complianceTask = data.get("compliance_task")
            complianceDescription = data.get("description")
            documentName = data.get("document")
            formatFile = data.get("format_file_name")
            penalConsequences = data.get("penal_consequences")
            complianceFrequency = data.get("compliance_frequency")
            statutoryDates =  json.dumps(data.get("statutory_dates"))
            repeatsEvery = data.get("repeats_every")
            repeatsType = data.get("repeats_type")
            duration = data.get("duration")
            durationType = data.get("duration_type")
            isActive = data.get("is_active")

            if complianceFrequency == "OneTime" :
                query = "UPDATE tbl_compliances set statutory_provision = '%s', \
                    compliance_task = '%s', compliance_description = '%s', document_name = '%s' , format_file = '%s', \
                    penal_consequences = '%s', compliance_frequency = '%s', statutory_dates = '%s', statutory_mapping_id = %s, \
                    is_active = %s, updated_by = %s WHERE compliance_id = %s "  % (
                        statutoryProvision, complianceTask, 
                        complianceDescription, documentName, formatFile, penalConsequences, complianceFrequency,
                        statutoryDates, mappingId, isActive, updatedBy, complianceId
                    )

            elif complianceFrequency == "OnOccurrence" :
                query = "UPDATE tbl_compliances set statutory_provision='%s', \
                    compliance_task='%s', compliance_description='%s', document_name='%s', format_file='%s', \
                    penal_consequences='%s', compliance_frequency='%s', statutory_dates='%s', duration=%s, \
                    duration_type='%s', statutory_mapping_id = %s, \
                    is_active = %s, updated_by = %s WHERE compliance_id = %s "% (
                        statutoryProvision, complianceTask, 
                        complianceDescription, documentName, formatFile, penalConsequences, complianceFrequency,
                        statutoryDates, int(duration), durationType, mappingId, isActive, updatedBy, complianceId
                    )

            else :
                query = "UPDATE tbl_compliances set statutory_provision ='%s', \
                    compliance_task ='%s', compliance_description='%s', document_name='%s', format_file='%s', \
                    penal_consequences='%s', compliance_frequency='%s', statutory_dates='%s', repeats_every=%s, \
                    repeats_type='%s', statutory_mapping_id=%s, \
                    is_active=%s, updated_by=%s WHERE compliance_id = %s "  % (
                        statutoryProvision, complianceTask, 
                        complianceDescription, documentName, formatFile, penalConsequences, complianceFrequency,
                        statutoryDates, int(repeatsEvery), repeatsType, mappingId, isActive, updatedBy, complianceId
                    )

            if (self.dataInsertUpdate(query)) :
                complianceIds.append(complianceId)

        return complianceIds

    def changeComplianceStatus(self, mappingId, isActive, updatedBy) :
        query = "UPDATE tbl_compliances set is_active=%s, \
            updated_by=%s WHERE statutory_mapping_id=%s" % (
                isActive, updatedBy, mappingId
            )
        return self.dataInsertUpdate(query)

    ### Stautory Mapping ###
    def getStautoryMappings(self) :
        query = "SELECT t1.statutory_mapping_id, t1.country_id, t2.country_name, t1.domain_id,  \
            t3.domain_name, t1.industry_ids, t1.statutory_nature_id, t4.statutory_nature_name, \
            t1.statutory_ids, t1.compliance_ids, t1.geography_ids, t1.approval_status, t1.is_active  \
            FROM tbl_statutory_mappings t1 \
            INNER JOIN tbl_countries t2 on t1.country_id = t2.country_id \
            INNER JOIN tbl_domains t3 on t1.domain_id = t3.domain_id \
            INNER JOIN tbl_statutory_natures t4 on t1.statutory_nature_id = t4.statutory_nature_id "
        return self.dataSelect(query)

    def getStatutoryMappingsById (self, mappingId) :
        query = "SELECT t1.country_id, t2.country_name, t1.domain_id,  \
            t3.domain_name, t1.industry_ids, t1.statutory_nature_id, t4.statutory_nature_name, \
            t1.statutory_ids, t1.compliance_ids, t1.geography_ids, t1.approval_status  \
            FROM tbl_statutory_mappings t1 \
            INNER JOIN tbl_countries t2 on t1.country_id = t2.country_id \
            INNER JOIN tbl_domains t3 on t1.domain_id = t3.domain_id \
            INNER JOIN tbl_statutory_natures t4 on t1.statutory_nature_id = t4.statutory_nature_id \
            WHERE t1.statutory_mapping_id=%s" % mappingId
        rows = self.dataSelect(query)
        return rows[0]


    def saveStatutoryMapping(self, data, createdBy) :
        countryId =data.get("country_id")
        domainId =data.get("domain_id")
        industryIds = ','.join(str(x) for x in data.get("industry_ids")) + ","
        natureId =data.get("statutory_nature_id")
        statutoryIds = ','.join(str(x) for x in data.get("statutory_ids")) + ","
        compliances = data.get("compliances")
        geographyIds = ','.join(str(x) for x in data.get("geography_ids")) + ","
        
        statutoryMappingId = self.getNewId("statutory_mapping_id", "tbl_statutory_mappings")
        createdOn = self.getDateTime()
        isActive = 1

        query = "INSERT INTO tbl_statutory_mappings (statutory_mapping_id, country_id, \
            domain_id, industry_ids, statutory_nature_id, statutory_ids, geography_ids,\
            is_active, created_by, created_on) \
            VALUES (%s, %s, %s, '%s', %s, '%s', '%s', %s, %s, '%s' )" % (
                statutoryMappingId, countryId, domainId, industryIds, natureId, statutoryIds,
                geographyIds, isActive, createdBy, createdOn
            )
        if (self.dataInsertUpdate(query)) :
            self.updateStatutoryMappingId(data.get("statutory_ids"), statutoryMappingId, createdBy)
            ids = self.saveCompliance(statutoryMappingId, compliances, createdBy)
            complianceIds = ','.join(str(x) for x in ids) + ","
            qry = "UPDATE tbl_statutory_mappings set compliance_ids='%s' \
                where statutory_mapping_id = %s" % (complianceIds, statutoryMappingId)
            self.dataInsertUpdate(qry)
            action = "Add Statutory Mappings"
            self.saveActivity(createdBy, 17, action)
            return True
        else :
            return False


    def updateStatutoryMapping(self, data, updatedBy) :
        statutoryMappingId = data.get("statutory_mapping_id")
        countryId =data.get("country_id")
        domainId =data.get("domain_id")
        industryIds = ','.join(str(x) for x in data.get("industry_ids")) + ","
        natureId =data.get("statutory_nature_id")
        statutoryIds = ','.join(str(x) for x in data.get("statutory_ids")) + ","
        compliances = data.get("compliances")
        geographyIds = ','.join(str(x) for x in data.get("geography_ids")) + ","

        self.saveStatutoryBackup(statutoryMappingId, updatedBy)
        query = "UPDATE tbl_statutory_mappings set country_id=%s, domain_id=%s, industry_ids='%s', \
            statutory_nature_id=%s, statutory_ids='%s', geography_ids='%s', updated_by=%s \
            WHERE statutory_mapping_id=%s" % (
                countryId, domainId, industryIds, natureId, statutoryIds, geographyIds,
                updatedBy, statutoryMappingId
            )
        if (self.dataInsertUpdate(query)) :
            self.updateStatutoryMappingId(data.get("statutory_ids"), statutoryMappingId, updatedBy)
            ids = self.updateCompliance(statutoryMappingId, compliances, updatedBy)
            complianceIds = ','.join(str(x) for x in ids) + ","
            qry = "UPDATE tbl_statutory_mappings set compliance_ids='%s' \
                where statutory_mapping_id = %s" % (complianceIds, statutoryMappingId)
            self.dataInsertUpdate(qry)
            action = "Edit Statutory Mappings"
            self.saveActivity(userId, 17, action)
            return True
        else :
            return False

    def changeStatutoryMappingStatus(self, data, updatedBy):
        statutoryMappingId = data.get("statutory_mapping_id")
        isActive = data.get("is_active")

        query = "UPDATE tbl_statutory_mappings set is_active=%s, updated_by=%s \
            WHERE statutory_mapping_id=%s" % (
            isActive, updatedBy, statutoryMappingId
        )
        if (self.dataInsertUpdate(query)) :
            self.changeComplianceStatus(statutoryMappingId, isActive, updatedBy)
            if isActive == 0:
                status = "deactivated"
            else:
                status = "activated"
            action = "Statutory Mapping status changed"
            self.saveActivity(updatedBy, 17, action)

    def changeApprovalStatus(self, data, updatedBy) :
        statutoryMappingId = data.get("statutory_mapping_id")
        approvalStatus = data.get("approval_status")
        rejectedReason = data.get("rejected_ reason")
        notificationText = data.get("notification_text")

        if approvalStatus == "Reject" :
            query = "UPDATE tbl_statutory_mappings set approval_status='%s', rejected_reason='%s', \
                updated_by=%s WHERE statutory_mapping_id = %s" % (
                    approvalStatus, rejectedReason, updatedBy, statutoryMappingId
                )
        elif approvalStatus == "Approve" :
            query = "UPDATE tbl_statutory_mappings set approval_status='%s', \
                updated_by=%s WHERE statutory_mapping_id = %s" % (
                    approvalStatus, rejectedReason, updatedBy, statutoryMappingId
                )
        else :
            query = "UPDATE tbl_statutory_mappings set approval_status='%s', \
                updated_by=%s WHERE statutory_mapping_id = %s" % (
                    approvalStatus, rejectedReason, updatedBy, statutoryMappingId
                )
            # if (self.dataInsertUpdate(query)) :

        return self.dataInsertUpdate(query)

    def saveStatutoryBackup(self, statutoryMappingId, createdBy):
        oldRecord = self.getStatutoryMappingsById(statutoryMappingId)
        backupId = self.getNewId("statutory_backup_id", "tbl_statutories_backup")
        createdOn = self.getDateTime()
        industryName = self.getIndustryByIndustryId(oldRecord[4])

        statutoryProvision = []
        for sid in oldRecord[7][:-1].split(',') :
            data = self.allStatutories.get(int(sid))
            statutoryProvision.append(data[1])
        mappings = ','.join(str(x) for x in statutoryProvision)
        geoMap = []
        for gid in oldRecord[8][:-1].split(',') :
            data = self.allGeographies.get(int(gid))
            geoMap.append(data[1])
        geoMappings = ','.join(str(x) for x in geoMap)
        query = "INSERT INTO tbl_statutories_backup(statutory_backup_id, country_name, domain_name, industry_name, \
            statutory_nature, statutory_provision, applicable_location, updated_by, updated_on) \
            VALUES(%s, '%s', '%s', '%s', '%s', '%s', '%s', %s, '%s') " % (
                backupId, oldRecord[1], oldRecord[3], industryName, oldRecord[6], mappings, geoMappings,
                createdBy, createdOn
            )
        if (self.dataInsertUpdate(query)) :
            qry = " INSERT INTO tbl_compliances_backup(statutory_backup_id, statutory_provision, \
                compliance_task, compliance_description, document_name, format_file, \
                penal_consequences, compliance_frequency, statutory_dates, repeats_every, \
                repeats_type, duration, duration_type)  \
                SELECT %s,t1.statutory_provision, t1.compliance_task, t1.compliance_description, \
                t1.document_name, t1.format_file, t1.penal_consequences, t1.compliance_frequency, \
                t1.statutory_dates, t1.repeats_every, t1.repeats_type, t1.duration, t1.duration_type \
                FROM tbl_compliances t1 WHERE statutory_mapping_id=%s" % (backupId, statutoryMappingId)
            self.dataInsertUpdate(qry)


    @staticmethod     
    def instance() :         
        global _databaseHandlerInstance
        if _databaseHandlerInstance is None :
            _databaseHandlerInstance = DatabaseHandler()
            _databaseHandlerInstance.getAllStatutories()
            _databaseHandlerInstance.getAllGeographies()
        return _databaseHandlerInstance
