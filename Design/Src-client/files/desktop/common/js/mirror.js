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

    function saveDomain(domainName, callback, failure_callback) {
        if (domainName == null)
            return null;
        var request = [
            "SaveDomain",
            { "domain_name" : domainName }
        ];
        apiRequest("SaveDomain", request, callback, failure_callback);
    }

    function updateDomain(domainId, domainName, callback, failure_callback) {
        if ((domainId == null) || (domainName == null))
            return null;
        var request = [
            "UpdateDomain",
            { "domain_id" : domainId, "domain_name" : domainName }
        ];
        apiRequest("UpdateDomain", request, callback, failure_callback);
    }

    function changeDomainStatus(domainId, isActive, callback, failure_callback) {
        if ((domainId == null) || (isActive == null))
            return null;
        var request = [
            "ChangeDomainStatus",
            {"domain_id" : domainId, "is_active" : isActive}
        ];
        apiRequest("ChangeDomainStatus", request, callback, failure_callback);
    }

    function getDomainList(callback, failure_callback) {
        var request = ["GetDomains", {}];
        apiRequest("GetDomains", request, callback, failure_callback);
    }

    //Country Master

    function saveCountry(countryName, callback, failure_callback) {
        if (countryName == null)
            return null;
        var request = [
            "SaveCountry",
            { "country_name" : countryName }
        ];
        apiRequest("SaveCountry", request, callback, failure_callback);
    }

    function updateCountry(countryId, countryName, callback, failure_callback) {
        if ((countryId == null) || (countryName == null))
            return null;
        var request = [
            "UpdateCountry",
            { "country_id" : countryId, "country_name" : countryName }
        ];
        apiRequest("UpdateCountry", request, callback, failure_callback);
    }

    function changeCountryStatus(countryId, isActive, callback, failure_callback) {
        if ((countryId == null) || (isActive == null))
            return null;
        var request = [
            "ChangeCountryStatus",
            {"country_id" : countryId, "is_active" : isActive}
        ];
        apiRequest("ChangeCountryStatus", request, callback, failure_callback);
    }

    function getCountryList(callback, failure_callback) {
        var request = ["GetCountries", {}];
        apiRequest("GetCountries", request, callback, failure_callback);
    }

    //Industry Master
    function saveIndustry(industryName, callback, failure_callback) {
        if (industryName == null)
            return null;
        var request = [
            "SaveIndustry",
            { "industry_name" : industryName }
        ];
        apiRequest("SaveIndustry", request, callback, failure_callback);
    }

    function updateIndustry(industryId, industryName, callback, failure_callback) {
        if ((industryId == null) || (industryName == null))
            return null;
        var request = [
            "UpdateIndustry",
            { "industry_id" : industryId, "industry_name" : industryName }
        ];
        apiRequest("UpdateIndustry", request, callback, failure_callback);
    }

    function changeIndustryStatus(industryId, isActive, callback, failure_callback) {
        if ((industryId == null) || (isActive == null))
            return null;
        var request = [
            "ChangeIndustryStatus",
            {"industry_id" : industryId, "is_active" : isActive}
        ];
        apiRequest("ChangeIndustryStatus", request, callback, failure_callback);
    }

    function getIndustryList(callback, failure_callback) {
        var request = ["GetIndustries", {}];
        apiRequest("GetIndustries", request, callback, failure_callback);
    }

    //Statutory Nature Master

    function saveStatutoryNature(statutoryNatureName, callback, failure_callback) {
        if (statutoryNatureName == null)
            return null;
        var request = [
            "SaveStatutoryNature",
            { "statutory_nature_name" : statutoryNatureName }
        ];
        apiRequest("SaveStatutoryNature", request, callback, failure_callback);
    }

    function updateStatutoryNature(statutoryNatureId, statutoryNatureName, 
        callback, failure_callback) {
        if ((statutoryNatureId == null) || (statutoryNatureName == null))
            return null;
        var request = [
            "UpdateStatutoryNature",
            { "statutory_nature_id" : statutoryNatureId, "statutory_nature_name" : statutoryNatureName }
        ];
        apiRequest("UpdateStatutoryNature", request, callback, failure_callback);
    }

    function changeStatutoryNatureStatus(statutoryNatureId, isActive, 
        callback, failure_callback) {
        if ((statutoryNatureId == null) || (isActive == null))
            return null;
        var request = [
            "ChangeStatutoryNatureStatus",
            {"statutory_nature_id" : statutoryNatureId, "is_active" : isActive}
        ];
        apiRequest("ChangeStatutoryNatureStatus", request, callback, failure_callback);
    }

    function getStatutoryNatureList(callback, failure_callback) {
        var request = ["GetStatutoryNatures", {}];
        apiRequest("GetStatutoryNatures", request, callback, failure_callback);
    }

    // Geography Levels 
    function getGeographyLevels(callback, failure_callback) {
        var request = ["GetGeographyLevels", {}];
        apiRequest("GetGeographyLevels", request, callback, failure_callback);   
    }

    function saveAndUpdateGeographyLevels(countryId, levels, 
        callback, failure_callback) {
        if ((countryId == null) || (levels == null))
            return null;
        var request = [
            "SaveGeographyLevel",
            { 
                "country_id" : countryId,
                "levels" : levels
            }
        ];
        apiRequest("SaveGeographyLevel", request, callback, failure_callback);
    }

    // Statutory Levels
    function getStatutoryLevels(callback, failure_callback) {
        var request = ["GetStatutoryLevels", {}];
        apiRequest("GetStatutoryLevels", request, callback, failure_callback);   
    }

    function saveAndUpdateStatutoryLevels(countryId, domainId, levels, 
        callback, failure_callback) {
        if ((countryId == null) || (domainId == null) || (levels == null))
            return null;
        var request = [
            "SaveStatutoryLevel",
            { 
                "country_id" : countryId,
                "domain_id" : domainId,
                "levels" : levels
            }
        ];
        apiRequest("SaveStatutoryLevel", request, callback, failure_callback);
    }

    //Geographies
    function getGeographies(callback, failure_callback) {
        var request = ["GetGeographies", {}];
        apiRequest("GetGeographies", request, callback, failure_callback);   
    }

    function saveGeography(levelId, name, parentIds, callback, failure_callback) {
        if ((levelId == null) || (name == null) || (parentIds == null))
            return null;
        var request = [
            "SaveGeography",
            { 
                "geography_level_id": levelId,
                "geography_name": name,
                "parent_ids": parentIds
            }
        ];
        apiRequest("SaveGeography", request, callback, failure_callback);
    }

    function updateGeography(geographyId, levelId, name, parentIds,
     callback, failure_callback) {
        if ((geographyId == null) || (levelId == null) || (name == null) || 
            (parentIds == null))
            return null;
        var request = [
            "UpdateGeography",
            { 
                "geography_id": geographyId,
                "geography_level_id": levelId,
                "geography_name": name,
                "parent_ids": parentIds
            }
        ];
        apiRequest("UpdateGeography", request, callback, failure_callback);
    }

    function changeGeographyStatus(geographyId, isActive, callback, failure_callback) {
        if ((geographyId == null) || (isActive == null))
            return null;
        var request = [
            "ChangeGeographyStatus",
            { 
                "geography_id": geographyId,
                "is_active": isActive
            }
        ];
        apiRequest("ChangeGeographyStatus", request, callback, failure_callback);
    }

    function getGeographyReport(callback, failure_callback) {
        var request = ["GeographyReport", {}];
        apiRequest("GeographyReport", request, callback, failure_callback);   
    }

    // statutory Mapping

    function saveStatutory(levelId, name, parentIds, callback, failure_callback) {
        var request = [
            "SaveStatutory",
            {
                "statutory_level_id": levelId,
                "statutory_name": name,
                "parent_ids": parentIds
            }
        ]
        apiRequest("SaveStatutory", request, callback, failure_callback);
    }

    function updateStatutory(statutoryId, levelId, name, parentIds, 
        callback, failure_callback) {
        var request = [
            "UpdateStatutory",
            {
                "statutory_id": statutoryId,
                "statutory_level_id": levelId,
                "statutory_name": name,
                "parent_ids": parentIds
            }
        ]
        apiRequest("UpdateStatutory", request, callback, failure_callback);
    }

    function saveStatutoryMapping(mappingData, callback, failure_callback ) {
        var request = [
            "SaveStatutoryMapping",
            mappingData
        ]
        apiRequest("SaveStatutoryMapping", request, callback, failure_callback);
    }

    function updateStatutoryMapping(mappingData, callback, failure_callback ) {
        var request = [
            "UpdateStatutoryMapping",
            mappingData
        ]
        apiRequest("UpdateStatutoryMapping", request, callback, failure_callback);
    }
    
    function getStatutoryMappings(callback, failure_callback) {
        var request = ["GetStatutoryMappings", {}];
        apiRequest("GetStatutoryMappings", request, callback, failure_callback);
    }

    // Admin User Group Master
    function isNull(value){
        if (value == null)
            return true
        else
            return false
    }


    function getAdminUserGroupList(callerName, 
        callback, failure_callback) {
        var request = [
            "GetUserGroups",
            {}
        ];
        apiRequest(callerName, request, callback, failure_callback);
    }

    function saveAdminUserGroup(callerName, userGroupDetail, 
        callback, failure_callback) {
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

    function updateAdminUserGroup(callerName, userGroupDetail, 
        callback, failure_callback) {
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

    function changeAdminUserGroupStatus(callerName, userGroupId, isActive, 
        callback, failure_callback) {
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


    function saveAdminUser(callerName, userDetail, 
        callback, failure_callback) {
       if (isNull(userDetail))
            return null;
        else if (userDetail.length != 9)
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
        var countryIds= userDetail[7].split(',') ;
        var domainIds= userDetail[8].split(',') ;
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
                "country_ids": countryIds,
                "domain_ids": domainIds
            }
        ];
        apiRequest(callerName, request, callback, failure_callback);
    }

    function updateAdminUser(callerName, userDetail, 
        callback, failure_callback) {
        if (isNull(userDetail))
            return null;
        else if (userDetail.length != 9)
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
        var countryIds= userDetail[7].split(',') ;
        var domainIds= userDetail[8].split(',') ;
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
                "country_ids": countryIds,
                "domain_ids": domainIds
            }
        ];
        apiRequest(callerName, request, callback, failure_callback);
    }

    function changeAdminUserStatus(callerName, userId, isActive,
     callback, failure_callback) {
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

    // Client Group Master

    function saveClientGroup(callerName, clientGroupDetails, 
        dateConfigurations, callback, failure_callback) {
        var request = [
            "SaveClientGroup",
            {
                "group_name": clientGroupDetails["group_name"],
                "country_ids": clientGroupDetails["country_ids"],
                "domain_ids":clientGroupDetails["domain_ids"],
                "logo" : clientGroupDetails["logo"],
                "contract_from": clientGroupDetails["contract_from"],
                "contract_to": clientGroupDetails["contract_to"],
                "incharge_persons": clientGroupDetails["incharge_persons"],
                "no_of_user_licence": clientGroupDetails["no_of_user_licence"],
                "file_space": clientGroupDetails["file_space"],
                "is_sms_subscribed": clientGroupDetails["is_sms_subscribed"],
                "email_id": clientGroupDetails["email_id"],
                "date_configurations":dateConfigurations
            }
        ];
       
        apiRequest(callerName, request, callback, failure_callback);
    }

    function updateClientGroup(callerName, clientGroupDetails, 
        dateConfigurations, callback, failure_callback) {
        var request = [
            "UpdateClientGroup",
            {
                "client_id": clientGroupDetails["client_id"],
                "group_name": clientGroupDetails["group_name"],
                "country_ids": clientGroupDetails["country_ids"],
                "domain_ids":clientGroupDetails["domain_ids"],
                "logo" : clientGroupDetails["logo"],
                "contract_from": clientGroupDetails["contract_from"],
                "contract_to": clientGroupDetails["contract_to"],
                "incharge_persons": clientGroupDetails["incharge_persons"],
                "no_of_user_licence": clientGroupDetails["no_of_user_licence"],
                "file_space": clientGroupDetails["file_space"],
                "is_sms_subscribed": clientGroupDetails["is_sms_subscribed"],
                "date_configurations":dateConfigurations
            }
        ];
        apiRequest(callerName, request, callback, failure_callback);
    }

    function changeClientGroupStatus(callerName, clientId, isActive, 
        callback, failure_callback) {
        var request = [
            "ChangeClientGroupStatus",
            {
                "client_id": clientId,
                "is_active": isActive
            }
        ];
        apiRequest(callerName, request, callback, failure_callback);
    }

    function getClientGroups(callerName, callback, failure_callback) {
        var request = [
            "GetClientGroups",
            {}
        ];
        apiRequest(callerName, request, callback, failure_callback);
    }

    // Change Password APIs

    function changePassword(callerName, currentPassword, newPassword,
     callback, failure_callback) {
        var request = [
            "ChangePassword",
            {
                "current_password": currentPassword,
                "new_password": newPassword
            }
        ];
        apiRequest(callerName, request, callback, failure_callback);
    }

    // Forgot Password APIs

    function forgotPassword(callerName, username, 
        callback, failure_callback) {
        var request = [
            "ForgotPassword",
            {
                "username": username
            }
        ];
        apiRequest(callerName, request, callback, failure_callback);
    }

    function validateResetToken(callerName, resetToken, 
        callback, failure_callback) {
        var request = [
            "ResetTokenValidation",
            {
                "reset_token": resetToken
            }
        ];
        apiRequest(callerName, request, callback, failure_callback);
    }

    function resetPassword(callerName, resetToken, newPassword, 
        callback, failure_callback) {
        var request = [
            "ResetPassword",
            {
                "reset_token": resetToken,
                "new_password": newPassword
            }
        ];
        apiRequest(callerName, request, callback, failure_callback);
    }

    // Client Unit APIs

    function getClients(callerName, callback, failure_callback) {
        var request = [
            "GetClients",
            {}
        ];
        apiRequest(callerName, request, callback, failure_callback);
    }

    function saveClient(callerName, clientId, businessGroup, legalEntity, 
        division, countryWiseUnits, callback, failure_callback) {
        var request = [
            "SaveClient",
            {
                "client_id": clientId,
                "business_group": businessGroup,
                "legal_entity": legalEntity,
                "division": division,
                "country_wise_units": countryWiseUnits
            }
        ];
        apiRequest(callerName, request, callback, failure_callback);
    }

    function changeClientStatus(callerName, clientId, divisionId, isActive, 
        callback, failure_callback) {
        var request = [
            "ChangeClientStatus",
            {
                "client_id": clientId,
                "division_id" : divisionId,
                "is_active": isActive
            }
        ];
        apiRequest(callerName, request, callback, failure_callback);
    }  

    function reactivateUnit(callerName, clientId, unitId, password, 
        callback, failure_callback) {
        var request = [
            "ReactivateUnit",
            {
                "client_id": clientId,
                "unit_id" : unitId,
                "password": password
            }
        ];
        apiRequest(callerName, request, callback, failure_callback);
    }  

    // Client User Group  
    function getClientUserGroups(callerName, callback, failure_callback) {
        var request = [
            "GetUserPrivileges",
            {}
        ];
        apiRequest(callerName, request, callback, failure_callback);
    }

    function saveClientUserGroup(callerName, userGroupDetail, 
        callback, failure_callback) {
        if (isNull(userGroupDetail))
            return null;   
        var request = [
            "SaveUserPrivilege",
            userGroupDetail
        ];
        apiRequest(callerName, request, callback, failure_callback);
    }

    function updateClientUserGroup(callerName, userGroupDetail, 
        callback, failure_callback) {
        if (isNull(userGroupDetail))
            return null;
        var request = [
            "UpdateUserPrivilege",
            userGroupDetail
        ];
        apiRequest(callerName, request, callback, failure_callback);
    }

    function changeClientUserGroupStatus(callerName, userGroupId, isActive, 
        callback, failure_callback) {
        if (isNull(userGroupId) || isNull(isActive) )
            return null;
        var request = [
            "ChangeUserPrivilegeStatus",
            {
                "user_group_id" : userGroupId,
                "is_active" : isActive
            }
        ];
        apiRequest(callerName, request, callback, failure_callback);
    }

     // Service Providers  
    function getServiceProviders(callerName, callback, failure_callback) {
        var request = [
            "GetServiceProviders",
            {}
        ];
        apiRequest(callerName, request, callback, failure_callback);
    }

    function saveServiceProvider(callerName, serviceProviderDetail,
     callback, failure_callback) {
        if (isNull(serviceProviderDetail))
            return null;
        var request = [
            "SaveServiceProvider",
            serviceProviderDetail
        ];
        apiRequest(callerName, request, callback, failure_callback);
    }

    function updateServiceProvider(callerName, serviceProviderDetail, 
        callback, failure_callback) {
        if (isNull(serviceProviderDetail))
            return null;    
        var request = [
            "UpdateServiceProvider",
            serviceProviderDetail
        ];
        apiRequest(callerName, request, callback, failure_callback);
    }

    function changeServiceProviderStatus(callerName, serviceProviderId, 
        isActive, callback, failure_callback) {
        if (isNull(serviceProviderId) || isNull(isActive) )
            return null;
        var request = [
            "ChangeServiceProviderStatus",
            {
                "service_provider_id" : serviceProviderId,
                "is_active" : isActive
            }
        ];
        apiRequest(callerName, request, callback, failure_callback);
    }

    // Client User
    function getClientUsers(callerName, callback, failure_callback) {
        var request = [
            "GetClientUsers",
            {}
        ];
        apiRequest(callerName, request, callback, failure_callback);
    }

    function saveClientUser(callerName, clientUserDetail,
     callback, failure_callback) {
        if (isNull(clientUserDetail))
            return null;
        var request = [
            "SaveClientUser",
            clientUserDetail
        ];
        apiRequest(callerName, request, callback, failure_callback);
    }

    function updateClientUser(callerName, clientUserDetail, 
        callback, failure_callback) {
        if (isNull(clientUserDetail))
            return null;
        var request = [
            "UpdateClientUser",
            clientUserDetail
        ];
        apiRequest(callerName, request, callback, failure_callback);
    }

    function changeClientUserStatus(callerName, userId, isActive, 
        callback, failure_callback) {
        if (isNull(userId) || isNull(isActive) )
            return null;
        var request = [
            "ChangeClientUserStatus",
            {
                "user_id" : userId,
                "is_active" : isActive
            }
        ];
        apiRequest(callerName, request, callback, failure_callback);
    }

    function changeAdminStatus(callerName, userId, isAdmin, 
        callback, failure_callback) {
        if (isNull(userId) || isNull(isAdmin) )
            return null;
        var request = [
            "ChangeAdminStatus",
            {
                "user_id" : userId,
                "is_admin" : isAdmin
            }
        ];
        apiRequest(callerName, request, callback, failure_callback);
    }

    // Unit Closure
    function getUnitClosureList(callerName, callback, failure_callback) {
        var request = [
            "GetUnitClosureList",
            {}
        ];
        apiRequest(callerName, request, callback, failure_callback);
    }

    function closeUnit(callerName, unitId, password, callback, 
        failure_callback){
        var request = [
            "CloseUnit",
            {
                "unit_id": unitId,
                "password": password
            }
        ];
        apiRequest(callerName, request, callback, failure_callback);
    }

    //Client Profile
    function getClientProfile(callerName, callback, failure_callback){
        var request = [
            "GetClientProfile",
            {}
        ];
        apiRequest(callerName, request, callback, failure_callback);
    }

    // Client Details Report
    function getClientDetailsReportFilters(callerName, callback, failure_callback){
        var request = [
            "GetClientDetailsReportFilters",
            {}
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
        getGeographyLevels: getGeographyLevels,
        saveAndUpdateGeographyLevels: saveAndUpdateGeographyLevels,
        getStatutoryLevels: getStatutoryLevels,
        saveAndUpdateStatutoryLevels: saveAndUpdateStatutoryLevels,
        getGeographies: getGeographies,
        saveGeography: saveGeography,
        updateGeography: updateGeography,
        changeGeographyStatus: changeGeographyStatus,
        getGeographyReport: getGeographyReport,
        saveStatutory: saveStatutory,
        updateStatutory: updateStatutory,
        saveStatutoryMapping: saveStatutoryMapping,
        updateStatutoryMapping: updateStatutoryMapping,
        getStatutoryMappings: getStatutoryMappings,


        saveAdminUserGroup: saveAdminUserGroup,
        updateAdminUserGroup: updateAdminUserGroup,
        changeAdminUserGroupStatus: changeAdminUserGroupStatus,
        getAdminUserGroupList: getAdminUserGroupList,

        saveAdminUser: saveAdminUser,
        updateAdminUser: updateAdminUser,
        changeAdminUserStatus: changeAdminUserStatus,
        getAdminUserList: getAdminUserList,

        saveClientGroup: saveClientGroup,
        updateClientGroup: updateClientGroup,
        getClientGroups: getClientGroups,
        changeClientGroupStatus: changeClientGroupStatus,

        changePassword: changePassword,
        forgotPassword: forgotPassword,
        validateResetToken: validateResetToken,
        resetPassword: resetPassword,

        getClients: getClients,
        saveClient: saveClient,
        changeClientStatus: changeClientStatus,
        reactivateUnit: reactivateUnit,

        saveClientUserGroup: saveClientUserGroup,
        updateClientUserGroup: updateClientUserGroup,
        changeClientUserGroupStatus: changeClientUserGroupStatus,
        getClientUserGroups: getClientUserGroups,

        saveServiceProvider: saveServiceProvider,
        updateServiceProvider: updateServiceProvider,
        changeServiceProviderStatus: changeServiceProviderStatus,
        getServiceProviders: getServiceProviders,

        getClientUsers: getClientUsers,
        saveClientUser: saveClientUser,
        updateClientUser: updateClientUser,
        changeClientUserStatus: changeClientUserStatus,
        changeAdminStatus: changeAdminStatus,

        getUnitClosureList: getUnitClosureList,
        closeUnit: closeUnit,

        getClientProfile: getClientProfile,
        getClientDetailsReportFilters: getClientDetailsReportFilters
    }

}
var mirror = initMirror();