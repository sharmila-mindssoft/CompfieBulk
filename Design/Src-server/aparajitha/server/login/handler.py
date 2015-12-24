import tornado.web
import hashlib
import json
from aparajitha.server.common import PossibleError, Form
from aparajitha.server.databasehandler import DatabaseHandler


__all__ = [
    "initializeLoginHandler"
]

def encrypt(value):
    m = hashlib.md5()
    m.update(value)
    return m.hexdigest()

class LoginModel(object) :
    def __init__(self, request) :
        self.request = request
        self.DH = DatabaseHandler.instance()
    
    def menuList(self, user_id):
        pass

    def userStructure(self, 
        user_id, session_token, email_id, user_group_name,
        menu, employee_name, employee_code, contact_no,
        address, designation
    ):
        return {
            "user_id": user_id,
            "session_token": session_token,
            "email_id": email_id,
            "user_group_name": user_group_name,
            "menu": menu,
            "employee_name": employee_name,
            "employee_code": employee_code,
            "contact_no": contact_no,
            "address": address,
            "designation": designation
        }

    def adminResponse(self) :
        #IT category 1
        user_id = 0
        session_type = 1 #web
        session_token = self.DH.add_session(user_id, session_type)
        print session_token
        menus = Form.getUserForms("1,2,3,4")
            
        return [
            "LoginSuccess",
            {
                "user_id": user_id,
                "session_token": session_token,
                "employee_name": "Administrator",
                "menu": menus
            }
        ]

    def userResponse(self, data):
        row = data[0]
        user_id = row[0]
        session_token = self.DH.add_session(user_id)



    def webLogin(self):
        _UserName = self.request["username"]
        _Password = self.request["password"]
        encryptedPassoword = encrypt(_Password)
        userDetails = self.DH.verifyLogin(_UserName, encryptedPassoword)
        print userDetails
        if userDetails != True :
            if (len(userDetails) == 0):
                return PossibleError("Login Failed")
            else :
                return self.userResponse(userDetails)
        else :
            return self.adminResponse()




class LoginAPIRequestHandler(tornado.web.RequestHandler) :
    def initialize(self, url, handler) :
        self.url = url
        self.handler = handler
        print "initializeLoginHandler"

    @tornado.web.asynchronous
    def post(self) :

        try:
            data = json.loads(self.request.body)
            data = data["data"]
            response = None
            if (data[0] == "Login") :
                response = LoginModel(data[1]).webLogin()
            else :
                response = PossibleError("Invalid Request")

        except Exception, e:
            print e
            self.send_error(400)
            return

        finally:
            self.set_header("Access-Control-Allow-Origin", "*")
            self.set_header("Access-Control-Allow-Headers", "Content-Type")
            self.set_header("Access-Control-Allow-Methods", "POST")
            self.write(json.dumps(response, indent=2))
            self.finish()

def initializeLoginHandler() :
    login_urls = [
        (r"/web-login", LoginAPIRequestHandler)
    ]
    return login_urls
