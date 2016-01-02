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
        if (typeof(info) === "undefined")
            return null;
        user = parseJSON(info)
        return user
    }

    function getUserProfile() {
        var info = getUserInfo();
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

    function apiRequest(callerName, request, callback) {
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
                matchString = 'success';
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
            BASE_URL + "api/login",
            toJSON(request),
            function (data) {
                var data = parseJSON(data);
                var status = data[0];
                var response = data[1];
                matchString = 'success';
                if (status.toLowerCase().indexOf(matchString) != -1){
                    callback(null, response);
                }
                callback(status, null) 
            }
        )
    }
    function verifyLoggedIn() {
        sessionToken = getSessionToken()
        if (sessionToken == null)
            return false
        else 
            return true
    }
    //Domain Master

    function saveDomain(domainName, callback) {
        var request = [
            "SaveDomain",
            { "domain_name" : domainName }
        ];
        apiRequest("SaveDomain", request, callback);
    }

    function updateDomain(domainId, domainName, callback) {
        var request = [
            "UpdateDomain",
            { "domain_id" : domainId, "domain_name" : domainName }
        ];
        apiRequest("UpdateDomain", request, callback);
    }

    function changeDomainStatus(domainId, isActive, callback) {
        var request = [
            "ChangeDomainStatus",
            {"domain_id" : domainId, "is_active" : isActive}
        ];
        apiRequest("ChangeDomainStatus", request, callback);
    }

    function getDomainList(callback) {
        var request = ["GetDomains", {}];
        apiRequest("GetDomains", request, callback);
    }

    //Country Master

    function saveCountry(countryName, callback) {
        var request = [
            "SaveCountry",
            { "country_name" : countryName }
        ];
        apiRequest("SaveCountry", request, callback);
    }

    function updateCountry(countryId, countryName, callback) {
        var request = [
            "UpdateCountry",
            { "country_id" : countryId, "country_name" : countryName }
        ];
        apiRequest("UpdateCountry", request, callback);
    }

    function changeCountryStatus(countryId, isActive, callback) {
        var request = [
            "ChangeCountryStatus",
            {"country_id" : countryId, "is_active" : isActive}
        ];
        apiRequest("ChangeCountryStatus", request, callback);
    }

    function getCountryList(callback) {
        var request = ["GetCountries", {}];
        apiRequest("GetCountries", request, callback);
    }

    //Industry Master
    function saveIndustry(industryName, callback) {
        var request = [
            "SaveIndustry",
            { "industry_name" : industryName }
        ];
        apiRequest("SaveIndustry", request, callback);
    }

    function updateIndustry(industryId, industryName, callback) {
        var request = [
            "UpdateIndustry",
            { "industry_id" : industryId, "industry_name" : industryName }
        ];
        apiRequest("UpdateIndustry", request, callback);
    }

    function changeIndustryStatus(industryId, isActive, callback) {
        var request = [
            "ChangeIndustryStatus",
            {"industry_id" : industryId, "is_active" : isActive}
        ];
        apiRequest("ChangeIndustryStatus", request, callback);
    }

    function getIndustryList(callback) {
        var request = ["GetIndustries", {}];
        apiRequest("GetIndustries", request, callback);
    }

    //Statutory Nature Master

    function saveStatutoryNature(statutoryNatureName, callback) {
        var request = [
            "SaveStatutoryNature",
            { "statutory_nature_name" : statutoryNatureName }
        ];
        apiRequest("SaveStatutoryNature", request, callback);
    }

    function updateStatutoryNature(statutoryNatureId, statutoryNatureName, 
        callback) {
        var request = [
            "UpdateStatutoryNature",
            { "statutory_nature_id" : statutoryNatureId, "statutory_nature_name" : statutoryNatureName }
        ];
        apiRequest("UpdateStatutoryNature", request, callback);
    }

    function changeStatutoryNatureStatus(statutoryNatureId, isActive, 
        callback) {
        var request = [
            "ChangeStatutoryNatureStatus",
            {"statutory_nature_id" : statutoryNatureId, "is_active" : isActive}
        ];
        apiRequest("ChangeStatutoryNatureStatus", request, callback);
    }

    function getStatutoryNatureList(callback) {
        var request = ["GetStatutoryNatures", {}];
        apiRequest("GetStatutoryNatures", request, callback);
    }

    // Geography Levels 
    function getGeographyLevels(callback) {
        var request = ["GetGeographyLevels", {}];
        apiRequest("GetGeographyLevels", request, callback);   
    }

    function levelDetails(levelId, levelPosition, levelName) {
        var level = {};
        level["level_id"] = levelId;
        level["level_position"] = levelPosition;
        level["level_name"] = levelName;
        return level;
    }

    function saveAndUpdateGeographyLevels(countryId, levels, 
        callback) {
        var request = [
            "SaveGeographyLevel",
            { 
                "country_id" : countryId,
                "levels" : levels
            }
        ];
        apiRequest("SaveGeographyLevel", request, callback);
    }

    // Statutory Levels
    function getStatutoryLevels(callback) {
        var request = ["GetStatutoryLevels", {}];
        apiRequest("GetStatutoryLevels", request, callback);   
    }

    function saveAndUpdateStatutoryLevels(countryId, domainId, levels, 
        callback) {
        var request = [
            "SaveStatutoryLevel",
            { 
                "country_id" : countryId,
                "domain_id" : domainId,
                "levels" : levels
            }
        ];
        apiRequest("SaveStatutoryLevel", request, callback);
    }

    //Geographies
    function getGeographies(callback) {
        var request = ["GetGeographies", {}];
        apiRequest("GetGeographies", request, callback);   
    }

    function saveGeography(levelId, name, parentIds, callback) {
        var request = [
            "SaveGeography",
            { 
                "geography_level_id": levelId,
                "geography_name": name,
                "parent_ids": parentIds
            }
        ];
        apiRequest("SaveGeography", request, callback);
    }

    function updateGeography(geographyId, levelId, name, parentIds,
     callback) {
        var request = [
            "UpdateGeography",
            { 
                "geography_id": geographyId,
                "geography_level_id": levelId,
                "geography_name": name,
                "parent_ids": parentIds
            }
        ];
        apiRequest("UpdateGeography", request, callback);
    }

    function changeGeographyStatus(geographyId, isActive, callback) {
        var request = [
            "ChangeGeographyStatus",
            { 
                "geography_id": geographyId,
                "is_active": isActive
            }
        ];
        apiRequest("ChangeGeographyStatus", request, callback);
    }

    function getGeographyReport(callback) {
        var request = ["GeographyReport", {}];
        apiRequest("GeographyReport", request, callback);   
    }

    // statutory Mapping

    function saveStatutory(levelId, name, parentIds, callback) {
        var request = [
            "SaveStatutory",
            {
                "statutory_level_id": levelId,
                "statutory_name": name,
                "parent_ids": parentIds
            }
        ]
        apiRequest("SaveStatutory", request, callback);
    }

    function updateStatutory(statutoryId, levelId, name, parentIds, callback) {
        var request = [
            "UpdateStatutory",
            {
                "statutory_id": statutoryId,
                "statutory_level_id": levelId,
                "statutory_name": name,
                "parent_ids": parentIds
            }
        ]
        apiRequest("UpdateStatutory", request, callback);
    }

    function statutoryDates(date, month, triggerBefore) {
        var statutoryDate = {};
        statutoryDate["statutory_date"] = date;
        statutoryDate["statutory_month"] = month;
        statutoryDate["trigger_before_days"] = triggerBefore;
        return statutoryDate;
    }

    function complianceDetails (
        statutoryProvision, complianceTask, 
        description, documentName, fileFormat, penalConsequence, 
        complianceFrequency, statutoryDates, repeatsTypeId, repeatsEvery,
        durationTypeId, duration, isActive, complianceId
    ) {
        var compliance = {};
        compliance["statutory_provision"] = statutoryProvision;
        compliance["compliance_task"] = complianceTask;
        compliance["description"] = description;
        compliance["document_name"] = documentName;
        compliance["format_file_name"] = fileFormat;
        compliance["penal_consequences"] = penalConsequence;
        compliance["frequency_id"] = complianceFrequency;
        compliance["statutory_dates"] = statutoryDates;
        compliance["repeats_type_id"] = repeatsTypeId;
        compliance["repeats_every"] = repeatsEvery;
        compliance["duration_type_id"] = durationTypeId;
        compliance["duration"] = duration;
        compliance["is_active"] = isActive;
        if (complianceId !== null) {
            compliance["compliance_id"] = complianceId;
        }

        return compliance;
    }

    function statutoryMapping(
        countryId, domainId, industryIds, statutoryNatureId, 
        statutoryIds, compliances, geographyIds, mappingId
    ) {
        var mappingData = {};
        mappingData["country_id"] = countryId;
        mappingData["domain_id"] = domainId;
        mappingData["industry_ids"] = industryIds;
        mappingData["statutory_nature_id"] = statutoryNatureId;
        mappingData["statutory_ids"] = statutoryIds;
        mappingData["compliances"] = compliances;
        mappingData["geography_ids"] = geographyIds;
        if (mappingId !== null) {
            mappingData["statutory_mapping_id"] = mappingId
        }

        return mappingData;
    }

    function saveStatutoryMapping(mappingData, callback ) {
        var request = [
            "SaveStatutoryMapping",
            mappingData
        ];
        apiRequest("SaveStatutoryMapping", request, callback);
    }

    function updateStatutoryMapping(mappingData, callback ) {
        var request = [
            "UpdateStatutoryMapping",
            mappingData
        ]
        apiRequest("UpdateStatutoryMapping", request, callback);
    }
    
    function getStatutoryMappings(callback) {
        var request = ["GetStatutoryMappings", {}];
        apiRequest("GetStatutoryMappings", request, callback);
    }

    function changeStatutoryMappingStatus(mappingId, isActive, callback) {
        var request = [
            "ChangeStatutoryMappingStatus",
            {
                "statutory_mapping_id":mappingId,
                "is_active" : isActive
            }
        ]
        apiRequest("ChangeStatutoryMappingStatus", request, callback);
    }

    function approveStatutoryList(statutoryMappingId, statutoryProvision, approvalStatus, reason, notificationText) {
        var dict = {}
        dict["statutory_mapping_id"] = statutoryMappingId;
        dict["statutory_provision"] = statutoryProvision;
        dict["approval_status"] = approvalStatus;
        dict["rejected_reason"] = reason;
        dict["notification_text"] = notificationText;
        return dict;
    }

    function approveStatutoryMapping(approvalList, callback) {
        var request = [
            "ApproveStatutoryMapping",
            {
                "statutory_mappings": approvalList
            }
        ]
        apiRequest("ApproveStatutoryMapping", request, callback);
    }

    function getStatutoryMappingsReportFilter(callback) {
        var request = ["GetStatutoryMappingReportFilters", {}];
        apiRequest("GetStatutoryMappingReportFilters", request, callback);
    }

    function filterData(countryId, domainId, industryId, statutoryNatureId, geographyId, level1StatutoryId) {
        var filter = {};
        filter["country_id"] = countryId;
        filter["domain_id"] = domainId;
        filter["industry_id"] = industryId;
        filter["statutory_nature_id"] = statutoryNatureId;
        filter["geography_id"] = geographyId;
        filter["level_1_statutory_id"] = level1StatutoryId;
        return filter;
    }

    function getStatutoryMappingsReportData(filterDatas, callback) {
        var request = ["GetStatutoryMappingReportData", filterDatas];
        apiRequest("getStatutoryMappingReportData", request, callback);
    }

    // Admin User Group Master

    function getAdminUserGroupList(callback) {
        callerName = "AdminAPI"
        var request = [
            "GetUserGroups",
            {}
        ];
        apiRequest(callerName, request, callback);
    }

    function getSaveAdminUserGroupDict(userGroupName, formCategoryId, formIds){
        userGroup = {};
        userGroup["user_group_name"] = userGroupName;
        userGroup["form_category_id"] = formCategoryId;
        userGroup["form_ids"] = formIds;
        return userGroup;
    }

    function saveAdminUserGroup(userGroupDetail, callback) {
        callerName = "AdminAPI"
        var request = [
            "SaveUserGroup",
            userGroupDetail
        ];
        apiRequest(callerName, request, callback);
    }

    function getUpdateAdminUserGroupDict(userGroupId, userGroupName, formCategoryId, formIds){
        userGroup = {};
        userGroup["user_group_id"] = userGroupId;
        userGroup["user_group_name"] = userGroupName;
        userGroup["form_category_id"] = formCategoryId;
        userGroup["form_ids"] = formIds;
        return userGroup;
    }

    function updateAdminUserGroup(userGroupDetail, callback) {
        callerName = "AdminAPI"
        var request = [
            "UpdateUserGroup",
            userGroupDetail
        ];
        apiRequest(callerName, request, callback);
    }

    function changeAdminUserGroupStatus(userGroupId, isActive, callback) {
        callerName = "AdminAPI"
        var request = [
            "ChangeUserGroupStatus",
            {
                "user_group_id" : userGroupId,
                "is_active" : isActive
            }
        ];
        apiRequest(callerName, request, callback);
    }


    // Admin User Master

    function getAdminUserList(callback) {
        callerName = "AdminAPI"
        var request = [
            "GetUsers",
            {}
        ];
        apiRequest(callerName, request, callback);
    }

    function getSaveAdminUserDict(userDetail){
        var emailId = userDetail[0];
        var userGroupId = userDetail[1];
        var employeeName = userDetail[2];
        var employeeCode = userDetail[3];
        var contactNo = userDetail[4];
        var address = userDetail[5];
        var designation = userDetail[6];
        var countryIds= userDetail[7].split(',') ;
        var domainIds= userDetail[8].split(',') ;
        return {
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
    }
    
    function saveAdminUser(userDetail, callback) {
        callerName = "AdminAPI"
        var request = [
            "SaveUser",
            userDetail
        ];
        apiRequest(callerName, request, callback);
    }

    function getUpdateAdminUserDict(userDetail){
        var userId = userDetail[0];
        var userGroupId = userDetail[1];
        var employeeName = userDetail[2];
        var employeeCode = userDetail[3];
        var contactNo = userDetail[4];
        var address = userDetail[5];
        var designation = userDetail[6];
        var countryIds= userDetail[7].split(',') ;
        var domainIds= userDetail[8].split(',') ;
        return {
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
    }

    function updateAdminUser(userDetail, callback) {
        callerName = "AdminAPI"        
        var request = [
            "UpdateUser",
            userDetail
        ];
        apiRequest(callerName, request, callback);
    }

    function changeAdminUserStatus(userId, isActive,
     callback) {
        callerName = "AdminAPI"
        var request = [
            "ChangeUserStatus",
            {
                "user_id": userId,
                "is_active" : isActive 
            }
        ];
        apiRequest(callerName, request, callback);
    }

    // Client Group Master

    function saveClientGroup(callerName, clientGroupDetails, 
        dateConfigurations, callback) {
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
       
        apiRequest(callerName, request, callback);
    }

    function updateClientGroup(callerName, clientGroupDetails, 
        dateConfigurations, callback) {
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
        apiRequest(callerName, request, callback);
    }

    function changeClientGroupStatus(callerName, clientId, isActive, 
        callback) {
        var request = [
            "ChangeClientGroupStatus",
            {
                "client_id": clientId,
                "is_active": isActive
            }
        ];
        apiRequest(callerName, request, callback);
    }

    function getClientGroups(callerName, callback) {
        var request = [
            "GetClientGroups",
            {}
        ];
        apiRequest(callerName, request, callback);
    }

    // Change Password APIs

    function changePassword(callerName, currentPassword, newPassword,
     callback) {
        var request = [
            "ChangePassword",
            {
                "current_password": currentPassword,
                "new_password": newPassword
            }
        ];
        apiRequest(callerName, request, callback);
    }

    // Forgot Password APIs

    function forgotPassword(callerName, username, 
        callback) {
        var request = [
            "ForgotPassword",
            {
                "username": username
            }
        ];
        apiRequest(callerName, request, callback);
    }

    function validateResetToken(callerName, resetToken, 
        callback) {
        var request = [
            "ResetTokenValidation",
            {
                "reset_token": resetToken
            }
        ];
        apiRequest(callerName, request, callback);
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
        apiRequest(callerName, request, callback);
    }

    // Client Unit APIs

    function getClients(callerName, callback) {
        var request = [
            "GetClients",
            {}
        ];
        apiRequest(callerName, request, callback);
    }

    function saveClient(callerName, clientId, businessGroup, legalEntity, 
        division, countryWiseUnits, callback) {

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
        apiRequest(callerName, request, callback);
    }


    function updateClient(callerName, clientId, businessGroup, legalEntity, 
        division, countryWiseUnits, callback) {
        var request = [
            "UpdateClient",
            {
                "client_id": clientId,
                "business_group": businessGroup,
                "legal_entity": legalEntity,
                "division": division,
                "country_wise_units": countryWiseUnits
            }
        ];
        apiRequest(callerName, request, callback);
    }

    function changeClientStatus(callerName, clientId, legalEntityId, divisionId, isActive, 
        callback) {
        var request = [
            "ChangeClientStatus",
            {
                "client_id": clientId,
                "legal_entity_id" : legalEntityId,
                "division_id" : divisionId,
                "is_active": isActive
            }
        ];
        apiRequest(callerName, request, callback);
    }  

    function reactivateUnit(callerName, clientId, unitId, password, 
        callback) {
        var request = [
            "ReactivateUnit",
            {
                "client_id": clientId,
                "unit_id" : unitId,
                "password": password
            }
        ];
        apiRequest(callerName, request, callback);
    }  

    // Client User Group  
    function getClientUserGroups(callerName, callback) {
        var request = [
            "GetUserPrivileges",
            {}
        ];
        apiRequest(callerName, request, callback);
    }

    function getSaveClientUserGroupDict(userGroupDetail){
        return {
            "user_group_name": userGroupDetail[0],
            "form_ids": userGroupDetail[1]
        }
    }

    function saveClientUserGroup(userGroupDetail, callback) {
        callerName = "ClientAdminAPI"
        var request = [
            "SaveUserPrivilege",
            userGroupDetail
        ];
        apiRequest(callerName, request, callback);
    }

    function getUpdateClientUserGroupDict(userGroupDetail){
        return {
            "user_group_id": userGroupDetail[0],
            "user_group_name": userGroupDetail[1],
            "form_ids": userGroupDetail[2]
        }
    }

    function updateClientUserGroup(userGroupDetail, callback) {
        callerName = "ClientAdminAPI"
        var request = [
            "UpdateUserPrivilege",
            userGroupDetail
        ];
        apiRequest(callerName, request, callback);
    }

    function changeClientUserGroupStatus(userGroupId, isActive, 
        callback) {
        callerName = "ClientAdminAPI"
        var request = [
            "ChangeUserPrivilegeStatus",
            {
                "user_group_id" : userGroupId,
                "is_active" : isActive
            }
        ];
        apiRequest(callerName, request, callback);
    }

     // Service Providers  
    function getServiceProviders(callback) {
        callerName = "ClientAdminAPI"
        var request = [
            "GetServiceProviders",
            {}
        ];
        apiRequest(callerName, request, callback);
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
        callerName = "ClientAdminAPI"
        var request = [
            "SaveServiceProvider",
            serviceProviderDetail
        ];
        apiRequest(callerName, request, callback);
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
        callerName = "ClientAdminAPI"
        var request = [
            "UpdateServiceProvider",
            serviceProviderDetail
        ];
        apiRequest(callerName, request, callback);
    }

    function changeServiceProviderStatus(serviceProviderId, 
        isActive, callback) {
        callerName = "ClientAdminAPI"
        var request = [
            "ChangeServiceProviderStatus",
            {
                "service_provider_id" : serviceProviderId,
                "is_active" : isActive
            }
        ];
        apiRequest(callerName, request, callback);
    }

    // Client User
    function getClientUsers(callback) {
        callerName = "ClientAdminAPI"
        var request = [
            "GetClientUsers",
            {}
        ];
        apiRequest(callerName, request, callback);
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
        callerName = "ClientAdminAPI"
        var request = [
            "SaveClientUser",
            clientUserDetail
        ];
        apiRequest(callerName, request, callback);
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
        callerName = "ClientAdminAPI"
        var request = [
            "UpdateClientUser",
            clientUserDetail
        ];
        apiRequest(callerName, request, callback);
    }

    function changeClientUserStatus(userId, isActive, callback) {
        callerName = "ClientAdminAPI"
        var request = [
            "ChangeClientUserStatus",
            {
                "user_id" : userId,
                "is_active" : isActive
            }
        ];
        apiRequest(callerName, request, callback);
    }

    function changeAdminStatus(userId, isAdmin, callback) {
        callerName = "ClientAdminAPI"
        var request = [
            "ChangeAdminStatus",
            {
                "user_id" : userId,
                "is_admin" : isAdmin
            }
        ];
        apiRequest(callerName, request, callback);
    }

    // Unit Closure
    function getUnitClosureList(callerName, callback) {
        var request = [
            "GetUnitClosureList",
            {}
        ];
        apiRequest(callerName, request, callback);
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
        apiRequest(callerName, request, callback);
    }

    //Client Profile
    function getClientProfile(callerName, callback){
        var request = [
            "GetClientProfile",
            {}
        ];
        apiRequest(callerName, request, callback);
    }

    // Client Details Report
    function getClientDetailsReportFilters(callerName, callback){
        var request = [
            "GetClientDetailsReportFilters",
            {}
        ];
        apiRequest(callerName, request, callback);
    }

    function getClientDetailsReport(callerName, reportFilters, 
        callback){
        var request = [
            "GetClientDetailsReport",
            reportFilters
        ];
        apiRequest(callerName, request, callback);
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

        levelDetails: levelDetails,
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

        statutoryDates: statutoryDates,
        complianceDetails: complianceDetails,
        statutoryMapping: statutoryMapping,

        saveStatutoryMapping: saveStatutoryMapping,
        updateStatutoryMapping: updateStatutoryMapping,
        getStatutoryMappings: getStatutoryMappings,
        changeStatutoryMappingStatus: changeStatutoryMappingStatus,
        approveStatutoryList: approveStatutoryList,
        approveStatutoryMapping: approveStatutoryMapping,
        getStatutoryMappingsReportFilter: getStatutoryMappingsReportFilter,
        filterData: filterData,
        getStatutoryMappingsReportData: getStatutoryMappingsReportData,

        getSaveAdminUserGroupDict: getSaveAdminUserGroupDict,
        saveAdminUserGroup: saveAdminUserGroup,
        getUpdateAdminUserGroupDict: getUpdateAdminUserGroupDict,
        updateAdminUserGroup: updateAdminUserGroup,
        changeAdminUserGroupStatus: changeAdminUserGroupStatus,
        getAdminUserGroupList: getAdminUserGroupList,

        getSaveAdminUserDict : getSaveAdminUserDict,
        saveAdminUser: saveAdminUser,
        getUpdateAdminUserDict : getUpdateAdminUserDict,
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
        updateClient : updateClient,
        changeClientStatus: changeClientStatus,
        reactivateUnit: reactivateUnit,

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
var mirror = initMirror();