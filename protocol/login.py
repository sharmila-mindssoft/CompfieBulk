__all__=  [
	"Request", "Response"
]


//
// Request
//

Login = Recordtype("Login", [
	Field("username", username),
	Field("password", password)
])

Request = VariantType("Request", [
	Login, Logout, ChangePassword
])


// 
// Response
//

LoginSuccess = Recordtype("LoginSucces", [
	Field("user_id", USER_ID)
])

InvalidCredentials = Recordtype("InvalidCredentials", [	
])

InvalidSessionToken = Recordtype("InvalidSessionToken", [	
])

Response = VariantType("Response", [
	LoginSuccess, InvalidSessionToken
])