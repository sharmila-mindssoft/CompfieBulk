var CLIENT_BASE_URL = "http://localhost:8090/";
function initClientMirror() {
    var DEBUG = true;

    function log() {
        if (window.console) {
            console.log.apply(console, arguments);
        }
    }

    function toJSON(data) {
        return JSON.stringify(data, null, " ");
    }

    function parseJSON(data) {
        return JSON.parse(data);
    }

    function initSession(userProfile){
        window.localStorage["userInfo"] = toJSON(userProfile);
    }

    // function updateUser_Session(user) {
    //     var info = parseJSON(window.localStorage["userInfo"])
    //     delete window.localStorage["userInfo"];

    //     info.userProfile = user;
    //     window.localStorage["userInfo"] = toJSON(info);
    // }

    function clearSession() {
        delete window.localStorage["userInfo"];
    }

    function getUserInfo() {
        var info = window.localStorage["userInfo"];
        user = parseJSON(info)
        return user
    }

    function getUserProfile() {
        var info = getUserInfo();
        var userDetails = {
            "user_id": info["user_id"],
            "client_id": info["client_id"],
            "user_group": info["user_group"],
            "employee_name": info["employee_name"],
            "employee_code": info["employee_code"],
            "email_id": info["email_id"],
            "contact_no": info["contact_no"],
            "address": info["address"],
            "designation": info["designation"]
        }
        return userDetails;
    }

    function getSessionToken() {
        var info = getUserInfo();
        return info["session_token"];
    }

    function getUserMenu(){
        var info = getUserInfo();
        return info["menu"]["menus"];
    }

    function getClientId(){
        var info = getUserInfo();
        return info["client_id"];
    }

    function clientApiRequest(callerName, request, callback) {
        var sessionToken = getSessionToken();
        var client_id = getClientId();
        if (sessionToken == null)
            sessionToken = "b4c59894336c4ee3b598f5e4bd2b276b";
        var requestFrame = {
            "session_token": client_id+"-"+sessionToken,
            "request": request
        };
        jQuery.post(
            CLIENT_BASE_URL + callerName,
            toJSON(requestFrame),
            function (data) {
                var data = parseJSON(data);
                var status = data[0];
                var response = data[1];
                matchString = 'success';
                log("API STATUS :"+status)
                if (status.toLowerCase().indexOf(matchString) != -1){
                    callback(null, response);
                }
                callback(status, null) 
            }
        )
        .fail(
            function (jqXHR, textStatus, errorThrown) {
                // alert("jqXHR:"+jqXHR.status);
                // alert("textStatus:"+textStatus);
                // alert("errorThrown:"+errorThrown);
                // callback(error, null);
            }
        );
    }

    // Login function 
    function login(username, password, callback) {
        var request = [
            "Login", {
                "login_type": "Web",
                "username": username,
                "password": password
            }
        ]
        jQuery.post(
            CLIENT_BASE_URL + "api/login",
            toJSON(request),
            function (data) {
                var data = parseJSON(data);
                var status = data[0];
                var response = data[1];
                matchString = 'success';
                if (status.toLowerCase().indexOf(matchString) != -1){
                    console.log("status success");
                    callback(null, response);
                }
                else {
                    callback(status, null); 
                }
            }
        )
    }
    function verifyLoggedIn() {
        sessionToken = getSessionToken()
        if (sessionToken == null)
            return false
        else 
            return false
    }
    function logout(callback) {
        sessionToken = getSessionToken()
        var request = [
            "Logout", {
                "session_token": sessionToken
            }
        ]
        jQuery.post(
            CLIENT_BASE_URL + "api/login",
            toJSON(request),
            function (data) {
                var data = parseJSON(data);
                var status = data[0];
                var response = data[1];
                matchString = 'success';
                if (status.toLowerCase().indexOf(matchString) != -1){
                    callback(null, response);
                }
                else {
                    callback(status, null); 
                }
            }
        )
    }

    // Change Password APIs

    function changePassword(currentPassword, newPassword,
     callback) {
        callerName = "api/login"
        var request = [
            "ChangePassword",
            {
                "current_password": currentPassword,
                "new_password": newPassword
            }
        ];
        clientApiRequest(callerName, request, callback);
    }

    // Forgot Password APIs

    function forgotPassword(username, 
        callback) {
        callerName = "api/login"
        var request = [
            "ForgotPassword",
            {
                "username": username
            }
        ];
        clientApiRequest(callerName, request, callback);
    }

    function validateResetToken(callerName, resetToken, 
        callback) {
        var request = [
            "ResetTokenValidation",
            {
                "reset_token": resetToken
            }
        ];
        clientApiRequest(callerName, request, callback);
    }

    function resetPassword(callerName, resetToken, newPassword, 
        callback) {
        var request = [
            "ResetPassword",
            {
                "reset_token": resetToken,
                "new_password": newPassword
            }
        ];
        clientApiRequest(callerName, request, callback);
    }

    // Client User Group  
    function getClientUserGroups(callback) {
        callerName = "api/client_masters"
        var request = [
            "GetUserPrivileges",
            {}
        ];
        clientApiRequest(callerName, request, callback);
    }

    function getSaveClientUserGroupDict(userGroupName, formIds){
        return {
            "user_group_name": userGroupName,
            "form_ids": formIds
        }
    }

    function saveClientUserGroup(userGroupDetail, callback) {
        callerName = "api/client_masters"  
        var request = [
            "SaveUserPrivileges",
            userGroupDetail
        ];
        clientApiRequest(callerName, request, callback);
    }

    function getUpdateClientUserGroupDict(userGroupId, userGroupName, formIds){
        return {
            "user_group_id": userGroupId,
            "user_group_name": userGroupName,
            "form_ids": formIds
        }
    }

    function updateClientUserGroup(userGroupDetail, callback) {
        callerName = "api/client_masters"
        var request = [
            "UpdateUserPrivileges",
            userGroupDetail
        ];
        clientApiRequest(callerName, request, callback);
    }

    function changeClientUserGroupStatus(userGroupId, isActive, 
        callback) {
        callerName = "api/client_masters"
        var request = [
            "ChangeUserPrivilegeStatus",
            {
                "user_group_id" : userGroupId,
                "is_active" : isActive
            }
        ];
        clientApiRequest(callerName, request, callback);
    }

     // Service Providers  
    function getServiceProviders(callback) {
        callerName = "api/client_masters"
        var request = [
            "GetServiceProviders",
            {}
        ];
        clientApiRequest(callerName, request, callback);
    }

    function getSaveServiceProviderDict(serviceProviderDetail){
        return {
            "service_provider_name": serviceProviderDetail[0],
            "address" : serviceProviderDetail[1],
            "contract_from" : serviceProviderDetail[2],
            "contract_to" : serviceProviderDetail[3],
            "contact_person" : serviceProviderDetail[4],
            "contact_no" : serviceProviderDetail[5]
        }
    }

    function saveServiceProvider(serviceProviderDetail, callback) {
        callerName = "api/client_masters"
        var request = [
            "SaveServiceProvider",
            serviceProviderDetail
        ];
        clientApiRequest(callerName, request, callback);
    }

    function getUpdateServiceProviderDict(serviceProviderDetail){
        return {
            "service_provider_id" : serviceProviderDetail[0],
            "service_provider_name": serviceProviderDetail[1],
            "address" : serviceProviderDetail[2],
            "contract_from" : serviceProviderDetail[3],
            "contract_to" : serviceProviderDetail[4],
            "contact_person" : serviceProviderDetail[5],
            "contact_no" : serviceProviderDetail[6]
        }
    }

    function updateServiceProvider(serviceProviderDetail, 
        callback) {
        callerName = "api/client_masters"  
        var request = [
            "UpdateServiceProvider",
            serviceProviderDetail
        ];
        clientApiRequest(callerName, request, callback);
    }

    function changeServiceProviderStatus(serviceProviderId, 
        isActive, callback) {
        callerName = "api/client_masters"
        var request = [
            "ChangeServiceProviderStatus",
            {
                "service_provider_id" : serviceProviderId,
                "is_active" : isActive
            }
        ];
        clientApiRequest(callerName, request, callback);
    }

    // Client User
    function getClientUsers(callback) {
        callerName = "api/client_masters"
        var request = [
            "GetClientUsers",
            {}
        ];
        clientApiRequest(callerName, request, callback);
    }

    function getSaveClientUserDict(clientUserDetail){
        return {
            "email_id" : clientUserDetail[0],
            "user_group_id" : clientUserDetail[1],
            "employee_name" : clientUserDetail[2],
            "employee_code" : clientUserDetail[3],
            "contact_no" : clientUserDetail[4],
            "seating_unit_id" : clientUserDetail[5],
            "user_level" : clientUserDetail[6],
            "country_ids" : clientUserDetail[7],
            "domain_ids" : clientUserDetail[8],
            "unit_ids" : clientUserDetail[9],
            "is_admin" : clientUserDetail[10],
            "is_service_provider" : clientUserDetail[11],
            "service_provider_id" : clientUserDetail[12]
        }
    }

    function saveClientUser(clientUserDetail, callback) {
        callerName = "api/client_masters"
        var request = [
            "SaveClientUser",
            clientUserDetail
        ];
        clientApiRequest(callerName, request, callback);
    }

    function getUpdateClientUserDict(clientUserDetail){
        return {
            "user_id": clientUserDetail[0],
            "user_group_id" : clientUserDetail[1],
            "employee_name" : clientUserDetail[2],
            "employee_code" : clientUserDetail[3],
            "contact_no" : clientUserDetail[4],
            "seating_unit_id" : clientUserDetail[5],
            "user_level" : clientUserDetail[6],
            "country_ids" : clientUserDetail[7],
            "domain_ids" : clientUserDetail[8],
            "unit_ids" : clientUserDetail[9],
            "is_admin" : clientUserDetail[10],
            "is_service_provider" : clientUserDetail[11],
            "service_provider_id" : clientUserDetail[12]
        }
    }

    function updateClientUser(clientUserDetail, callback) {
        callerName = "api/client_masters"
        var request = [
            "UpdateClientUser",
            clientUserDetail
        ];
        clientApiRequest(callerName, request, callback);
    }

    function changeClientUserStatus(userId, isActive, callback) {
        callerName = "api/client_masters"
        var request = [
            "ChangeClientUserStatus",
            {
                "user_id" : userId,
                "is_active" : isActive
            }
        ];
        clientApiRequest(callerName, request, callback);
    }

    function changeAdminStatus(userId, isAdmin, callback) {
        callerName = "api/client_masters"
        var request = [
            "ChangeAdminStatus",
            {
                "user_id" : userId,
                "is_admin" : isAdmin
            }
        ];
        clientApiRequest(callerName, request, callback);
    }

    // Unit Closure
    function getUnitClosureList(callback) {
        callerName = "api/client_masters"
        var request = [
            "GetUnits",
            {}
        ];
        clientApiRequest(callerName, request, callback);
    }

    function closeUnit(unitId, password, callback, 
        failure_callback){
        callerName = "api/client_masters"
        var request = [
            "CloseUnit",
            {
                "unit_id": unitId,
                "password": password
            }
        ];
        clientApiRequest(callerName, request, callback);
    }

    //Client Profile
    function getClientProfile(callback){
        callerName = "api/techno"
        var request = [
            "GetClientProfile",
            {}
        ];
        clientApiRequest(callerName, request, callback);
    }

    // Client Details Report
    function getClientDetailsReportFilters(callback){
        callerName = "api/techno"
        var request = [
            "GetClientDetailsReportFilters",
            {}
        ];
        clientApiRequest(callerName, request, callback);
    }

    function getClientDetailsReport(countryId, clientId, businessGroupId, legalEntityId, divisionId, 
        unitId, domainIds, callback){
        callerName = "api/techno"
        var request = [
            "GetClientDetailsReport",
            {
                "country_id": countryId,
                "group_id" : clientId,
                "business_group_id": businessGroupId,
                "legal_entity_id" : legalEntityId,
                "division_id" : divisionId,
                "unit_id": unitId,
                "domain_ids" : domainIds
            }
        ];
        clientApiRequest(callerName, request, callback);
    }

    return {
        log: log,
        toJSON: toJSON, 
        parseJSON: parseJSON,

        initSession: initSession,
        // updateUser_Session: updateUser_Session,
        clearSession: clearSession,
        verifyLoggedIn: verifyLoggedIn,
        login: login,
        logout: logout,

        getUserInfo: getUserInfo,
        getUserProfile: getUserProfile,
        getSessionToken: getSessionToken,
        getUserMenu: getUserMenu,
        clientApiRequest: clientApiRequest,
        getClientId: getClientId,

        changePassword: changePassword,
        forgotPassword: forgotPassword,
        validateResetToken: validateResetToken,
        resetPassword: resetPassword,

        getSaveClientUserGroupDict: getSaveClientUserGroupDict,
        saveClientUserGroup: saveClientUserGroup,
        getUpdateClientUserGroupDict: getUpdateClientUserGroupDict, 
        updateClientUserGroup: updateClientUserGroup,
        changeClientUserGroupStatus: changeClientUserGroupStatus,
        getClientUserGroups: getClientUserGroups,

        getSaveServiceProviderDict: getSaveServiceProviderDict,
        saveServiceProvider: saveServiceProvider,
        getUpdateServiceProviderDict: getUpdateServiceProviderDict,
        updateServiceProvider: updateServiceProvider,
        changeServiceProviderStatus: changeServiceProviderStatus,
        getServiceProviders: getServiceProviders,

        getClientUsers: getClientUsers,
        getSaveClientUserDict: getSaveClientUserDict,
        saveClientUser: saveClientUser,
        getUpdateClientUserDict:getUpdateClientUserDict,
        updateClientUser: updateClientUser,
        changeClientUserStatus: changeClientUserStatus,
        changeAdminStatus: changeAdminStatus,

        getUnitClosureList: getUnitClosureList,
        closeUnit: closeUnit,

        getClientProfile: getClientProfile,
        getClientDetailsReportFilters: getClientDetailsReportFilters,
        getClientDetailsReport: getClientDetailsReport
    }

}
var client_mirror = initClientMirror();