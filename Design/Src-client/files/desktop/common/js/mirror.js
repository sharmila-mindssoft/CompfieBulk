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
        // var sessionToken = getSessionToken();
        // if (sessionToken == null)
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

    function levelDetails(levelId, levelPosition, levelName) {
        var level = {};
        level["level_id"] = levelId;
        level["level_position"] = levelPosition;
        level["level_name"] = levelName;
        return level;
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

    function updateStatutory(statutoryId, levelId, name, parentIds, callback, failure_callback) {
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

    function saveStatutoryMapping(mappingData, callback, failure_callback ) {
        var request = [
            "SaveStatutoryMapping",
            mappingData
        ];
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

    function changeStatutoryMappingStatus(mappingId, isActive, callback, failure_callback) {
        var request = [
            "ChangeStatutoryMappingStatus",
            {
                "statutory_mapping_id":mappingId,
                "is_active" : isActive
            }
        ]
        apiRequest("ChangeStatutoryMappingStatus", request, callback, failure_callback);
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

    function approveStatutoryMapping(approvalList, callback, failure_callback) {
        var request = [
            "ApproveStatutoryMapping",
            {
                "statutory_mappings": approvalList
            }
        ]
        apiRequest("ApproveStatutoryMapping", request, callback, failure_callback);
    }

    function getStatutoryMappingsReportFilter(callback, failure_callback) {
        var request = ["GetStatutoryMappingReportFilters", {}];
        apiRequest("GetStatutoryMappingReportFilters", request, callback, failure_callback);
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

    function getStatutoryMappingsReportData(filterDatas, callback, failure_callback) {
        var request = ["GetStatutoryMappingReportData", filterDatas];
        apiRequest("getStatutoryMappingReportData", request, callback, failure_callback);
    }

    // Admin User Group Master
    function isNull(value){
        if (value == null)
            return true
        else
            return false
    }


    function getAdminUserGroupList(callback, failure_callback) {
        callerName = "AdminAPI"
        var request = [
            "GetUserGroups",
            {}
        ];
        apiRequest(callerName, request, callback, failure_callback);
    }

    function getSaveAdminUserGroupDict(userGroupName, formCategoryId, formIds){
        userGroup = {};
        userGroup["user_group_name"] = userGroupName;
        userGroup["form_category_id"] = formCategoryId;
        userGroup["form_ids"] = formIds;
        return userGroup;
    }

    function saveAdminUserGroup(userGroupDetail, callback, failure_callback) {
        callerName = "AdminAPI"
        if (isNull(userGroupDetail))
            return null;
        var request = [
            "SaveUserGroup",
            userGroupDetail
        ];
        apiRequest(callerName, request, callback, failure_callback);
    }

    function getUpdateAdminUserGroupDict(userGroupId, userGroupName, formCategoryId, formIds){
        userGroup = {};
        userGroup["user_group_id"] = userGroupId;
        userGroup["user_group_name"] = userGroupName;
        userGroup["form_category_id"] = formCategoryId;
        userGroup["form_ids"] = formIds;
        return userGroup;
    }

    function updateAdminUserGroup(userGroupDetail, callback, failure_callback) {
        callerName = "AdminAPI"
        if (isNull(userGroupDetail))
            return null;
        var request = [
            "UpdateUserGroup",
            userGroupDetail
        ];
        apiRequest(callerName, request, callback, failure_callback);
    }

    function changeAdminUserGroupStatus(userGroupId, isActive, callback, failure_callback) {
        callerName = "AdminAPI"
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

    function getAdminUserList(callback, failure_callback) {
        callerName = "AdminAPI"
        var request = [
            "GetUsers",
            {}
        ];
        apiRequest(callerName, request, callback, failure_callback);
    }

    function getSaveAdminUserDict(userDetail){
        var emailId = userDetail[0];
        var userGroupId = userDetail[1];
        var employeeName = userDetail[2];
        var employeeCode = userDetail[3];
        var contactNo = userDetail[4];
        var address = userDetail[5];
        var designation = userDetail[6];
        var countryIds= userDetail[7] ;
        var domainIds= userDetail[8];
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
    
    function saveAdminUser(userDetail, callback, failure_callback) {
        callerName = "AdminAPI"
        if (isNull(userDetail))
            return null;
        var request = [
            "SaveUser",
            userDetail
        ];
        apiRequest(callerName, request, callback, failure_callback);
    }

    function getUpdateAdminUserDict(userDetail){
        var userId = userDetail[0];
        var userGroupId = userDetail[1];
        var employeeName = userDetail[2];
        var employeeCode = userDetail[3];
        var contactNo = userDetail[4];
        var address = userDetail[5];
        var designation = userDetail[6];
        var countryIds= userDetail[7] ;
        var domainIds= userDetail[8] ;
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

    function updateAdminUser(userDetail, callback, failure_callback) {
        callerName = "AdminAPI"
        if (isNull(userDetail))
            return null;
        
        var request = [
            "UpdateUser",
            userDetail
        ];
        apiRequest(callerName, request, callback, failure_callback);
    }

    function changeAdminUserStatus(userId, isActive,
     callback, failure_callback) {
        callerName = "AdminAPI"
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

    function forgotPassword(username, 
        callback, failure_callback) {
        callerName = "api/login"
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

    function getUnit(){
        unit = {}
        unit["a"] = a
        return unit
    }

    function saveClient(clientId, businessGroup, legalEntity, 
        division, countryWiseUnits, callback, failure_callback) {
        callerName = "TechnoAPI"
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


    function updateClient(callerName, clientId, businessGroup, legalEntity, 
        division, countryWiseUnits, callback, failure_callback) {
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
        apiRequest(callerName, request, callback, failure_callback);
    }

    function changeClientStatus(callerName, clientId, legalEntityId, divisionId, isActive, 
        callback, failure_callback) {
        var request = [
            "ChangeClientStatus",
            {
                "client_id": clientId,
                "legal_entity_id" : legalEntityId,
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
    function getClientUserGroups(callback, failure_callback) {
        callerName = "ClientAdminAPI"
        var request = [
            "GetUserPrivileges",
            {}
        ];
        apiRequest(callerName, request, callback, failure_callback);
    }

    function getSaveClientUserGroupDict(userGroupName, formIds){
        return {
            "user_group_name": userGroupName,
            "form_ids": formIds
        }
    }

    function saveClientUserGroup(userGroupDetail, callback, failure_callback) {
        callerName = "ClientAdminAPI"  
        var request = [
            "SaveUserPrivilege",
            userGroupDetail
        ];
        apiRequest(callerName, request, callback, failure_callback);
    }

    function getUpdateClientUserGroupDict(userGroupId, userGroupName, formIds){
        return {
            "user_group_id": userGroupId,
            "user_group_name": userGroupName,
            "form_ids": formIds
        }
    }

    function updateClientUserGroup(userGroupDetail, callback, failure_callback) {
        callerName = "ClientAdminAPI"
        var request = [
            "UpdateUserPrivilege",
            userGroupDetail
        ];
        apiRequest(callerName, request, callback, failure_callback);
    }

    function changeClientUserGroupStatus(userGroupId, isActive, 
        callback, failure_callback) {
        callerName = "ClientAdminAPI"
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
    function getServiceProviders(callback, failure_callback) {
        callerName = "ClientAdminAPI"
        var request = [
            "GetServiceProviders",
            {}
        ];
        apiRequest(callerName, request, callback, failure_callback);
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

    function saveServiceProvider(serviceProviderDetail, callback, failure_callback) {
        callerName = "ClientAdminAPI"
        if (isNull(serviceProviderDetail))
            return null;
        var request = [
            "SaveServiceProvider",
            serviceProviderDetail
        ];
        apiRequest(callerName, request, callback, failure_callback);
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
        callback, failure_callback) {
        callerName = "ClientAdminAPI"
        if (isNull(serviceProviderDetail))
            return null;    
        var request = [
            "UpdateServiceProvider",
            serviceProviderDetail
        ];
        apiRequest(callerName, request, callback, failure_callback);
    }

    function changeServiceProviderStatus(serviceProviderId, 
        isActive, callback, failure_callback) {
        callerName = "ClientAdminAPI"
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
    function getClientUsers(callback, failure_callback) {
        callerName = "ClientAdminAPI"
        var request = [
            "GetClientUsers",
            {}
        ];
        apiRequest(callerName, request, callback, failure_callback);
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

    function saveClientUser(clientUserDetail, callback, failure_callback) {
        callerName = "ClientAdminAPI"
        var request = [
            "SaveClientUser",
            clientUserDetail
        ];
        apiRequest(callerName, request, callback, failure_callback);
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

    function updateClientUser(clientUserDetail, callback, failure_callback) {
        callerName = "ClientAdminAPI"
        var request = [
            "UpdateClientUser",
            clientUserDetail
        ];
        apiRequest(callerName, request, callback, failure_callback);
    }

    function changeClientUserStatus(userId, isActive, callback, failure_callback) {
        callerName = "ClientAdminAPI"
        var request = [
            "ChangeClientUserStatus",
            {
                "user_id" : userId,
                "is_active" : isActive
            }
        ];
        apiRequest(callerName, request, callback, failure_callback);
    }

    function changeAdminStatus(userId, isAdmin, callback, failure_callback) {
        callerName = "ClientAdminAPI"
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

    function getClientDetailsReport(callerName, reportFilters, 
        callback, failure_callback){
        var request = [
            "GetClientDetailsReport",
            reportFilters
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