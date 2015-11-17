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
    domain_url = "http://192.168.1.3:8080/GetDomains"
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
    url = "http://localhost:8080/SaveDomain"
    data = {
        "session_token" : "b4c59894336c4ee3b598f5e4bd2b276b",
        "request" : [
            "SaveDomain",
            {
                "domain_name": "Labour Law"
            }
        ]
    }
    print "saveDomain response"
    return handle_request(url, data)

def updateDomain() :
    url = "http://localhost:8080/UpdateDomain"
    data = {
        "session_token" : "b4c59894336c4ee3b598f5e4bd2b276b",
        "request" : [
            "UpdateDomain",
            {
                "domain_id": 3,
                "domain_name": "Industry Law"
            }
        ]
    }
    print "updateDomain response"
    return handle_request(url, data)

def changeDomain() :
    url = "http://localhost:8080/ChangeDomainStatus"
    data = {
        "session_token" : "b4c59894336c4ee3b598f5e4bd2b276b",
        "request" : [
            "ChangeDomainStatus",
            {
                "domain_id": 1,
                "is_active": 0
            }
        ]
    }
    print "changeDomain response"
    return handle_request(url, data)

### COUNTRY
def getcountries():
    url = "http://localhost:8080/GetCountries"
    data = {
        "session_token" : "b4c59894336c4ee3b598f5e4bd2b276b",
        "request" : [
            "GetCountries",
            {}
        ]
    }

    return handle_request(url, data)

def saveCountry():
    url = "http://localhost:8080/SaveCountry"
    data = {
        "session_token" : "b4c59894336c4ee3b598f5e4bd2b276b",
        "request" : [
            "SaveCountry",
            {
                "country_name": "USA"
            }
        ]
    }
    return handle_request(url, data)

def updateCountry() :
    url = "http://localhost:8080/UpdateCountry"
    data = {
        "session_token" : "b4c59894336c4ee3b598f5e4bd2b276b",
        "request" : [
            "UpdateCountry",
            {
                "country_id": 2,
                "country_name": "Sri Lanka"
            }
        ]
    }
    return handle_request(url, data)

def changeCountry() :
    url = "http://localhost:8080/ChangeCountryStatus"
    data = {
        "session_token" : "b4c59894336c4ee3b598f5e4bd2b276b",
        "request" : [
            "ChangeCountryStatus",
            {
                "country_id": 1,
                "is_active": 0
            }
        ]
    }
    return handle_request(url, data)

def sendUserGroupRequests():
    url = "http://localhost:8080/UserGroups"

    ## To Get User Groups list and Form data 
    # data = {
    #     "session_token" : "b4c59894336c4ee3b598f5e4bd2b276b",
    #     "request" : [
    #         "GetUserGroups",
    #         {}
    #     ]
    # }

    ## To Save User Group
    # data = {
    #     "session_token" : "b4c59894336c4ee3b598f5e4bd2b276b",
    #     "request" : [
    #         "SaveUserGroup",
    #         {
    #             "user_group_name": "Techno User",
    #             "form_type": "Techno",
    #             "form_ids": ['1','2']
    #         }
    #     ]
    # }

    ## To Update User Group
    # data = {
    #     "session_token" : "b4c59894336c4ee3b598f5e4bd2b276b",
    #     "request" : [
    #         "UpdateUserGroup",
    #         { 
    #             "user_group_id" : 5,
    #             "user_group_name": "Techno Manager",
    #             "form_type": "Techno",
    #             "form_ids": ['11','29']
    #         }
    #     ]
    # }

    ## To Change Status
    data = {
        "session_token" : "b4c59894336c4ee3b598f5e4bd2b276b",
        "request" : [
            "ChangeUserGroupStatus",
            { 
                "user_group_id" : 1,
                "is_active": 1,
            }
        ]
    }
    return handle_request(url, data)

def sendUserRequests():
    url = "http://localhost:8080/AdminUsers"
    ## To Save User 
    # data = {
    #     "session_token" : "b4c59894336c4ee3b598f5e4bd2b276b",
    #     "request" : [
    #         "SaveUser",
    #         {
    #             "email_id": "sanju@domain.com",
    #             "user_group_id": 1,
    #             "employee_name": "Sharmila Madhavan",
    #             "employee_code": "EMP1002",
    #             "contact_no": "+917845605418",
    #             "address": "kk nagar, Madurai", 
    #             "designation": "developer",
    #             "domain_ids": ['1','4']
    #         }
    #     ]
    # }
    ## To Update User 
    data = {
        "session_token" : "b4c59894336c4ee3b598f5e4bd2b276b",
        "request" : [
            "UpdateUser",
            {
                "user_id": 1,
                "email_id": "sanjana@domain.com",
                "user_group_id": 1,
                "employee_name": "Sharmila Madhavan",
                "employee_code": "EMP1003",
                "contact_no": "+917845605428",
                "address": "kk nagar, Madurai", 
                "designation": "developer",
                "domain_ids": ['1','4']
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
    # sendUserGroupRequests()
    sendUserRequests()

    ### Country ###
    # saveCountry()
    # updateCountry()
    # changeCountry()
    # getcountries()

    application = tornado.web.Application(
        [],
        gzip=True
    )
    application.listen(8090)
    tornado.ioloop.IOLoop.instance().start()

    
