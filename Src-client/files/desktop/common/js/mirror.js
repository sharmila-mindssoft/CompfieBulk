
var BASE_URL = "http://localhost:8080/";
function initMirror() {
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
        var info = {
            "userProfile": userProfile
        };
        windows.localStorage["userInfo"] = toJSON(info);
    }

    function updateUser_Session(user) {
        var info = parseJSON(window.localStorage["userInfo"])
        delete window.localStorage["userInfo"];

        info.userProfile = user;
        window.localStorage["userInfo"] = toJSON(info);
    }

    function clearSession() {
        delete window.localStorage["userInfo"];
    }

    function getUserInfo() {
        var info = window.localStorage["userInfo"];
        if (typeof(info) === "undefined")
            return null;
        user = parseJSON(info)
        return user["userProfile"];
    }

    function getUserProfile() {
        var info = getUserProfile();
        if (info === null)
            return null
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
        if (info === null)
            return null;
        return info["session_token"];
    }

    function getUserMenu(){
        var info = getUserInfo();
        if (info === null)
            return null;
        return info["menu"];
    }

    function apiRequest(callerName, request, callback, failure_callback) {
        var sessionToken = getSessionToken();
        if (sessionToken == null)
            sessionToken = "b4c59894336c4ee3b598f5e4bd2b276b";
        var requestFrame = {
            "session_token": sessionToken,
            "request": request
        };
        jQuery.post(
            BASE_URL + callerName,
            toJSON(requestFrame),
            function (data) {
                var data = parseJSON(data);
                var status = data[0];
                var response = data[1];

                if (DEBUG) {
                    log("API Status: " + status);
                }
                if (callback) {
                    callback(status, response);
                }
            }
        )
        .fail(
            function (data) {
                log(data);
                if (failure_callback) 
                    failure_callback(data);
            }
        );
    }

    // Login function 

    //Domain Master

    function saveDomain(callerName, domainName, callback, failure_callback) {
        if (domainName == null)
            return null;
        var request = [
            "SaveDomain",
            { "domain_name" : domainName }
        ];
        apiRequest(callerName, request, callback, failure_callback);
    }

    function updateDomain(callerName, domainId, domainName, callback, failure_callback) {
        if ((domainId == null) || (domainName == null))
            return null;
        var request = [
            "UpdateDomain",
            { "domain_id" : domainId, "domain_name" : domainName }
        ];
        apiRequest(callerName, request, callback, failure_callback);
    }

    function changeDomainStatus(callerName, domainId, isActive, callback, failure_callback) {
        if ((domainId == null) || (isActive == null))
            return null;
        var request = [
            "ChangeDomainStatus",
            {"domain_id" : domainId, "is_active" : isActive}
        ];
        apiRequest(callerName, request, callback, failure_callback);
    }

    function getDomainList(callerName, callback, failure_callback) {
        var request = ["GetDomains", {}];
        apiRequest(callerName, request, callback, failure_callback);
    }

    //Country Master

    function saveCountry(callerName, countryName, callback, failure_callback) {
        if (countryName == null)
            return null;
        var request = [
            "SaveCountry",
            { "country_name" : countryName }
        ];
        apiRequest(callerName, request, callback, failure_callback);
    }

    function updateCountry(callerName, countryId, countryName, callback, failure_callback) {
        if ((countryId == null) || (countryName == null))
            return null;
        var request = [
            "UpdateCountry",
            { "country_id" : countryId, "country_name" : countryName }
        ];
        apiRequest(callerName, request, callback, failure_callback);
    }

    function changeCountryStatus(callerName, countryId, isActive, callback, failure_callback) {
        if ((countryId == null) || (isActive == null))
            return null;
        var request = [
            "ChangeCountryStatus",
            {"country_id" : countryId, "is_active" : isActive}
        ];
        apiRequest(callerName, request, callback, failure_callback);
    }

    function getCountryList(callerName, callback, failure_callback) {
        var request = ["GetCountries", {}];
        apiRequest(callerName, request, callback, failure_callback);
    }

    //Industry Master

    function saveIndustry(callerName, industryName, callback, failure_callback) {
        if (industryName == null)
            return null;
        var request = [
            "SaveIndustry",
            { "industry_name" : industryName }
        ];
        apiRequest(callerName, request, callback, failure_callback);
    }

    function updateIndustry(callerName, industryId, industryName, callback, failure_callback) {
        if ((industryId == null) || (industryName == null))
            return null;
        var request = [
            "UpdateIndustry",
            { "industry_id" : industryId, "industry_name" : industryName }
        ];
        apiRequest(callerName, request, callback, failure_callback);
    }

    function changeIndustryStatus(callerName, industryId, isActive, callback, failure_callback) {
        if ((industryId == null) || (isActive == null))
            return null;
        var request = [
            "ChangeIndustryStatus",
            {"industry_id" : industryId, "is_active" : isActive}
        ];
        apiRequest(callerName, request, callback, failure_callback);
    }

    function getIndustryList(callerName, callback, failure_callback) {
        var request = ["GetIndustries", {}];
        apiRequest(callerName, request, callback, failure_callback);
    }

    //Statutory Nature Master

    function saveStatutoryNature(callerName, statutoryNatureName, callback, failure_callback) {
        if (statutoryNatureName == null)
            return null;
        var request = [
            "SaveStatutoryNature",
            { "statutory_nature_name" : statutoryNatureName }
        ];
        apiRequest(callerName, request, callback, failure_callback);
    }

    function updateStatutoryNature(callerName, statutoryNatureId, statutoryNatureName, callback, failure_callback) {
        if ((statutoryNatureId == null) || (statutoryNatureName == null))
            return null;
        var request = [
            "UpdateStatutoryNature",
            { "statutory_nature_id" : statutoryNatureId, "statutory_nature_name" : statutoryNatureName }
        ];
        apiRequest(callerName, request, callback, failure_callback);
    }

    function changeStatutoryNatureStatus(callerName, statutoryNatureId, isActive, callback, failure_callback) {
        if ((statutoryNatureId == null) || (isActive == null))
            return null;
        var request = [
            "ChangeStatutoryNatureStatus",
            {"statutory_nature_id" : statutoryNatureId, "is_active" : isActive}
        ];
        apiRequest(callerName, request, callback, failure_callback);
    }

    function getStatutoryNatureList(callerName, callback, failure_callback) {
        var request = ["GetIStatutoryNatures", {}];
        apiRequest(callerName, request, callback, failure_callback);
    }

    // Admin User Group Master
    function isNull(value){
        if (value == null)
            return true
        else
            return false
    }


    function getAdminUserGroupList(callerName, callback, failure_callback) {
        var request = [
            "GetUserGroups",
            {}
        ];
        apiRequest(callerName, request, callback, failure_callback);
    }

    function saveAdminUserGroup(callerName, userGroupDetail, callback, failure_callback) {
        if (isNull(userGroupDetail))
            return null;
        else if (userGroupDetail.length != 3)
            return null;
        $.each(userGroupDetail, function( index, value ) {
            if (isNull(value))
                return null
        });
        var userGroupName= userGroupDetail[0] ;
        var fromType= userGroupDetail[1] ;
        var formIds= userGroupDetail[2].split(',') ;
        var request = [
            "SaveUserGroup",
            {
                "user_group_name": userGroupName,
                "form_type": fromType,
                "form_ids": formIds
            }
        ];
        apiRequest(callerName, request, callback, failure_callback);
    }

    function updateAdminUserGroup(callerName, userGroupDetail, statutoryNatureName, callback, failure_callback) {
        if (isNull(userGroupDetail))
            return null;
        else if (userGroupDetail.length != 4)
            return null;
        $.each(userGroupDetail, function( index, value ) {
            if (isNull(value))
                return null
        });
        var userGroupId= userGroupDetail[0] ;
        var userGroupName= userGroupDetail[1] ;
        var fromType= userGroupDetail[2] ;
        var formIds= userGroupDetail[3].split(',') ;
        var request = [
            "UpdateUserGroup",
            {
                "user_group_id" : userGroupId,
                "user_group_name": userGroupName,
                "form_type": fromType,
                "form_ids": formIds
            }
        ];
        apiRequest(callerName, request, callback, failure_callback);
    }

    function changeAdminUserGroupStatus(callerName, userGroupId, isActive, callback, failure_callback) {
        if (isNull(userGroupId) || isNull(isActive) )
            return null;
        var request = [
            "ChangeUserGroupStatus",
            {
                "user_group_id" : userGroupId,
                "is_active" : isActive
            }
        ];
        apiRequest(callerName, request, callback, failure_callback);
    }


    // Admin User Master

    function getAdminUserList(callerName, callback, failure_callback) {
        var request = [
            "GetUsers",
            {}
        ];
        apiRequest(callerName, request, callback, failure_callback);
    }


    function saveAdminUser(callerName, userDetail, callback, failure_callback) {
       if (isNull(userDetail))
            return null;
        else if (userDetail.length != 8)
            return null;
        $.each(userDetail, function( index, value ) {
            if (isNull(value))
                return null
        });
        var emailId = userDetail[0];
        var userGroupId = userDetail[1];
        var employeeName = userDetail[2];
        var employeeCode = userDetail[3];
        var contactNo = userDetail[4];
        var address = userDetail[5];
        var designation = userDetail[6];
        var domainIds= userDetail[7].split(',') ;
        var request = [
            "SaveUser",
            {
                "email_id": emailId,
                "user_group_id": userGroupId,
                "employee_name": employeeName,
                "employee_code": employeeCode,
                "contact_no": contactNo,
                "address": address, 
                "designation": designation,
                "domain_ids": domainIds
            }
        ];
        apiRequest(callerName, request, callback, failure_callback);
    }

    function updateAdminUser(callerName, userDetail, callback, failure_callback) {
        if (isNull(userDetail))
            return null;
        else if (userDetail.length != 8)
            return null;
        $.each(userDetail, function( index, value ) {
            if (isNull(value))
                return null
        });
        var userId = userDetail[0];
        var userGroupId = userDetail[1];
        var employeeName = userDetail[2];
        var employeeCode = userDetail[3];
        var contactNo = userDetail[4];
        var address = userDetail[5];
        var designation = userDetail[6];
        var domainIds= userDetail[7].split(',') ;
        var request = [
            "UpdateUser",
            {
                "user_id": userId,
                "user_group_id": userGroupId,
                "employee_name": employeeName,
                "employee_code": employeeCode,
                "contact_no": contactNo,
                "address": address, 
                "designation": designation,
                "domain_ids": domainIds
            }
        ];
        apiRequest(callerName, request, callback, failure_callback);
    }

    function changeAdminUserStatus(callerName, userId, isActive, callback, failure_callback) {
        if (isNull(userId) || isNull(isActive) )
            return null;
        var request = [
            "ChangeUserStatus",
            {
                "user_id": userId,
                "is_active" : isActive 
            }
        ];
        apiRequest(callerName, request, callback, failure_callback);
    }

    return {
        log: log,
        toJSON: toJSON,
        parseJSON: parseJSON,

        initSession: initSession,
        updateUser_Session: updateUser_Session,
        clearSession: clearSession,

        getUserInfo: getUserInfo,
        getUserProfile: getUserProfile,
        getSessionToken: getSessionToken,
        getUserMenu: getUserMenu,
        apiRequest: apiRequest,

        saveDomain: saveDomain,
        updateDomain: updateDomain,
        changeDomainStatus: changeDomainStatus,
        getDomainList: getDomainList,
        saveCountry: saveCountry,
        updateCountry: updateCountry,
        changeCountryStatus: changeCountryStatus,
        getCountryList: getCountryList,
        saveIndustry: saveIndustry,
        updateIndustry: updateIndustry,
        changeIndustryStatus: changeIndustryStatus,
        getIndustryList: getIndustryList,
        saveStatutoryNature: saveStatutoryNature,
        updateStatutoryNature: updateStatutoryNature,
        changeStatutoryNatureStatus: changeStatutoryNatureStatus,
        getStatutoryNatureList: getStatutoryNatureList,

        saveAdminUserGroup: saveAdminUserGroup,
        updateAdminUserGroup: updateAdminUserGroup,
        changeAdminUserGroupStatus: changeAdminUserGroupStatus,
        getAdminUserGroupList: getAdminUserGroupList,

        saveAdminUser: saveAdminUser,
        updateAdminUser: updateAdminUser,
        changeAdminUserStatus: changeAdminUserStatus,
        getAdminUserList: getAdminUserList

    }

}
var mirror = initMirror();