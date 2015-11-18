from tornado.httpclient import AsyncHTTPClient
import urllib
import tornado.web
import tornado.ioloop
import json



def handle_request(url, options) :
    
    def handle_response (api_response) :
        if api_response.error:
            print api_response.error
        else:
            data = api_response.body
            print data
            print 

    encoded_parameters = urllib.urlencode(options)
    # print options
    http_client = AsyncHTTPClient()
    http_client.fetch(
        url, 
        handle_response,
        method="POST", 
        body=json.dumps(options),
        request_timeout=3000                                                  
    )   

### get domain 
def getdomains():
    domain_url = "http://localhost:8080/ApiCall"
    domains_data = {
        "session_token" : "b4c59894336c4ee3b598f5e4bd2b276b",
        "request" : [
            "GetDomains",
            {}
        ]
    }

    print "GetDomains response"
    return handle_request( domain_url, domains_data)

def saveDomain():
    url = "http://localhost:8080/ApiCall"
    data = {
        "session_token" : "b4c59894336c4ee3b598f5e4bd2b276b",
        "request" : [
            "SaveDomain",
            {
                "domain_name": "New Labour Law"
            }
        ]
    }
    print "saveDomain response"
    return handle_request(url, data)

def updateDomain() :
    url = "http://localhost:8080/ApiCall"
    data = {
        "session_token" : "b4c59894336c4ee3b598f5e4bd2b276b",
        "request" : [
            "UpdateDomain",
            {
                "domain_id": 3,
                "domain_name": "Industry Law Update"
            }
        ]
    }
    print "updateDomain response"
    return handle_request(url, data)

def changeDomain() :
    url = "http://localhost:8080/ApiCall"
    data = {
        "session_token" : "b4c59894336c4ee3b598f5e4bd2b276b",
        "request" : [
            "ChangeDomainStatus",
            {
                "domain_id": 1,
                "is_active": 1
            }
        ]
    }
    print "changeDomain response"
    return handle_request(url, data)

### COUNTRY
def getcountries():
    url = "http://localhost:8080/ApiCall"
    data = {
        "session_token" : "b4c59894336c4ee3b598f5e4bd2b276b",
        "request" : [
            "GetCountries",
            {}
        ]
    }

    return handle_request(url, data)

def saveCountry():
    url = "http://localhost:8080/ApiCall"
    data = {
        "session_token" : "b4c59894336c4ee3b598f5e4bd2b276b",
        "request" : [
            "SaveCountry",
            {
                "country_name": "Spain"
            }
        ]
    }
    return handle_request(url, data)

def updateCountry() :
    url = "http://localhost:8080/ApiCall"
    data = {
        "session_token" : "b4c59894336c4ee3b598f5e4bd2b276b",
        "request" : [
            "UpdateCountry",
            {
                "country_id": 2,
                "country_name": "South Africa"
            }
        ]
    }
    return handle_request(url, data)

def changeCountry() :
    url = "http://localhost:8080/ApiCall"
    data = {
        "session_token" : "b4c59894336c4ee3b598f5e4bd2b276b",
        "request" : [
            "ChangeCountryStatus",
            {
                "country_id": 1,
                "is_active": 1
            }
        ]
    }
    return handle_request(url, data)

def getUserGroups():
    url = "http://localhost:8080/AdminAPI"
    data = {
        "session_token" : "b4c59894336c4ee3b598f5e4bd2b276b",
        "request" : [
            "GetUserGroups",
            {}
        ]
    }
    return handle_request(url, data)

def saveUserGroup():
    url = "http://localhost:8080/AdminAPI"
    data = {
        "session_token" : "b4c59894336c4ee3b598f5e4bd2b276b",
        "request" : [
            "SaveUserGroup",
            {
                "user_group_name": "Knowledge User",
                "form_type": "Knowledge",
                "form_ids": ['3','4']
            }
        ]
    }
    return handle_request(url, data)

def updateUserGroup():
    url = "http://localhost:8080/AdminAPI"
    data = {
        "session_token" : "b4c59894336c4ee3b598f5e4bd2b276b",
        "request" : [
            "UpdateUserGroup",
            { 
                "user_group_id" : 1,
                "user_group_name": "Techno Manager",
                "form_type": "Techno",
                "form_ids": ['11','29']
            }
        ]
    }
    return handle_request(url, data)

def changeUserGroupStatus(status):
    url = "http://localhost:8080/AdminAPI"
    data = {
        "session_token" : "b4c59894336c4ee3b598f5e4bd2b276b",
        "request" : [
            "ChangeUserGroupStatus",
            { 
                "user_group_id" : 1,
                "is_active": status
            }
        ]
    }
    return handle_request(url, data)

def saveUser():
    url = "http://localhost:8080/AdminAPI"
    data = {
        "session_token" : "b4c59894336c4ee3b598f5e4bd2b276b",
        "request" : [
            "SaveUser",
            {
                "email_id": "sumi@domain.com",
                "user_group_id": 1,
                "employee_name": "Sumitha",
                "employee_code": "EMP1054",
                "contact_no": "+919845605438",
                "address": "kk nagar, Madurai", 
                "designation": "developer",
                "domain_ids": ['1','4']
            }
        ]
    }
    return handle_request(url, data)

def updateUser():
    url = "http://localhost:8080/AdminAPI"
    data = {
        "session_token" : "b4c59894336c4ee3b598f5e4bd2b276b",
        "request" : [
            "UpdateUser",
            {
                "user_id": 1,
                "user_group_id": 1,
                "employee_name": "Sanju Madhavan",
                "employee_code": "EMP1012",
                "contact_no": "+917845635428",
                "address": "kk nagar, Madurai", 
                "designation": "developer",
                "domain_ids": ['1','4']
            }
        ]
    }
    return handle_request(url, data)

def changeUserStatus(status):
    url = "http://localhost:8080/AdminAPI"
    data = {
        "session_token" : "b4c59894336c4ee3b598f5e4bd2b276b",
        "request" : [
            "ChangeUserStatus",
            {
                "user_id": 1,
                "is_active" : status 
            }
        ]
    }
    return handle_request(url, data)

def getUsers():
    url = "http://localhost:8080/AdminAPI"
    data = {
        "session_token" : "b4c59894336c4ee3b598f5e4bd2b276b",
        "request" : [
            "GetUsers",
            {}
        ]
    }
    return handle_request(url, data)


### Industry
def getindustries():
    url = "http://localhost:8080/Industry"
    data = {
        "session_token" : "b4c59894336c4ee3b598f5e4bd2b276b",
        "request" : [
            "GetIndustries",
            {}
        ]
    }

    return handle_request(url, data)

def saveIndustry(industry):
    url = "http://localhost:8080/SaveIndustry"
    data = {
        "session_token" : "b4c59894336c4ee3b598f5e4bd2b276b",
        "request" : [
            "SaveIndustry",
            {
                "industry_name": industry
            }
        ]
    }
    return handle_request(url, data)

def updateIndustry(industry) :
    url = "http://localhost:8080/abcdefgh"
    data = {
        "session_token" : "b4c59894336c4ee3b598f5e4bd2b276b",
        "request" : [
            "UpdateIndustry",
            {
                "industry_id": 3,
                "industry_name": industry
            }
        ]
    }
    return handle_request(url, data)

def changeIndustry(status) :
    url = "http://localhost:8080/ChangeStatus"
    data = {
        "session_token" : "b4c59894336c4ee3b598f5e4bd2b276b",
        "request" : [
            "ChangeIndustryStatus",
            {
                "industry_id": 1,
                "is_active": status
            }
        ]
    }
    return handle_request(url, data)

### StatutoryNature

def getStatutoryNature():
    url = "http://localhost:8080/StatutoryNature"
    data = {
        "session_token" : "b4c59894336c4ee3b598f5e4bd2b276b",
        "request" : [
            "GetStatutoryNatures",
            {}
        ]
    }

    return handle_request(url, data)

def saveStatutoryNature(inputData):
    url = "http://localhost:8080/StatutoryNature"
    data = {
        "session_token" : "b4c59894336c4ee3b598f5e4bd2b276b",
        "request" : [
            "SaveStatutoryNature",
            {
                "statutory_nature_name": inputData
            }
        ]
    }
    return handle_request(url, data)

def updateStatutoryNature(inputData) :
    url = "http://localhost:8080/StatutoryNature"
    data = {
        "session_token" : "b4c59894336c4ee3b598f5e4bd2b276b",
        "request" : [
            "UpdateStatutoryNature",
            {
                "statutory_nature_id": 3,
                "statutory_nature_name": inputData
            }
        ]
    }
    return handle_request(url, data)

def changeStatutoryNatureStatus(status) :
    url = "http://localhost:8080/StatutoryNature"
    data = {
        "session_token" : "b4c59894336c4ee3b598f5e4bd2b276b",
        "request" : [
            "ChangeStatutoryNatureStatus",
            {
                "statutory_nature_id": 4,
                "is_active": status
            }
        ]
    }
    return handle_request(url, data)

if __name__ == "__main__" :
    print "listening on port 8090"
    ### Domain ###
    # saveDomain()
    # updateDomain()
    # changeDomain()
    # getdomains()
    
    ### Country ###
    # saveCountry()
    # updateCountry()
    # changeCountry()
    # getcountries()
    

    ### Industry ###
    # saveIndustry("Mines")
    # updateIndustry("New Plantation")
    # changeIndustry(1)
    # getindustries()

    ### StatutoryNature ###
    # saveStatutoryNature("test")
    # updateStatutoryNature("State")
    # changeStatutoryNatureStatus(0)
    # getStatutoryNature()

    ### AdminUserGroup ###
    # saveUserGroup()
    # updateUserGroup()
    # changeUserGroupStatus(1)
    # getUserGroups()

    ### AdminUser ###
    # saveUser()
    # updateUser()
    # changeUserStatus(1)
    getUsers()

    application = tornado.web.Application(
        [],
        gzip=True
    )
    application.listen(8090)
    tornado.ioloop.IOLoop.instance().start()

    
