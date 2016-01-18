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

    function getShortName(){
        var pathArray = window.location.pathname.split( '/' );
        if(typeof pathArray[2] === 'undefined'){
            return null;
        }else{
            return pathArray[2]   
        }
        
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
        if (typeof info === "undefined") {
            user = null;
        }
        else {
            user = parseJSON(info);
        }
        return user;
    }

    function updateUserInfo(response){
        var info = getUserInfo();
        info["contact_no"] = response["contact_no"]
        info["address"] = response["address"]
        window.localStorage["userInfo"] = toJSON(info)
    }

    function getUserProfile() {
        var info = getUserInfo();
        var userDetails = {
            "user_id": info["user_id"],
            "client_id": info["client_id"],
            "user_group": info["user_group_name"],
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
        if (info !== null)
            return info["session_token"];
        else 
            return null;
    }

    function getUserMenu(){
        var info = getUserInfo();
        return info["menu"]["menus"];
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
                log("API STATUS :"+status)
                if (status.toLowerCase().indexOf(matchString) != -1){
                    if(status == "UpdateUserProfileSuccess"){
                        updateUserInfo(response);
                    }
                    callback(null, response);
                }
                else {
                    callback(status, null) 
                }
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

    function LoginApiRequest(callerName, request, callback) {
        jQuery.post(
            BASE_URL + callerName,
            toJSON(request),
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
    function login(username, password, short_name, callback) {
        var request = [
            "Login", {
                "login_type": "Web",
                "username": username,
                "password": password,
                "short_name": short_name
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
    function logout() {
        sessionToken = getSessionToken()
        var request = [
            "Logout", {
                "session_token": sessionToken
            }
        ]
        jQuery.post(
            BASE_URL + "api/login",
            toJSON(request),
            function (data) {
                var data = parseJSON(data);
                var status = data[0];
                var response = data[1];
                clearSession()
                matchString = 'success';
                if (status.toLowerCase().indexOf(matchString) != -1){
                    callback(null, response)
                }
                else {
                    callback(status, null); 
                }
            }
        )
    }
    //Domain Master

    function saveDomain(domainName, callback) {
        var request = [
            "SaveDomain",
            { "domain_name" : domainName }
        ];
        apiRequest("api/general", request, callback);
    }

    function updateDomain(domainId, domainName, callback) {
        var request = [
            "UpdateDomain",
            { "domain_id" : domainId, "domain_name" : domainName }
        ];
        apiRequest("api/general", request, callback);
    }

    function changeDomainStatus(domainId, isActive, callback) {
        var request = [
            "ChangeDomainStatus",
            {"domain_id" : domainId, "is_active" : isActive}
        ];
        apiRequest("api/general", request, callback);
    }

    function getDomainList(callback) {
        var request = ["GetDomains", {}];
        apiRequest("api/general", request, callback);
    }

    //Country Master

    function saveCountry(countryName, callback) {
        var request = [
            "SaveCountry",
            { "country_name" : countryName }
        ];
        apiRequest("api/general", request, callback);
    }

    function updateCountry(countryId, countryName, callback) {
        var request = [
            "UpdateCountry",
            { "country_id" : countryId, "country_name" : countryName }
        ];
        apiRequest("api/general", request, callback);
    }

    function changeCountryStatus(countryId, isActive, callback) {
        var request = [
            "ChangeCountryStatus",
            {"country_id" : countryId, "is_active" : isActive}
        ];
        apiRequest("api/general", request, callback);
    }

    function getCountryList(callback) {
        var request = ["GetCountries", {}];
        apiRequest("api/general", request, callback);
    }

    //Industry Master
    function saveIndustry(industryName, callback) {
        var request = [
            "SaveIndustry",
            { "industry_name" : industryName }
        ];
        apiRequest("api/knowledge_master", request, callback);
    }

    function updateIndustry(industryId, industryName, callback) {
        var request = [
            "UpdateIndustry",
            { "industry_id" : industryId, "industry_name" : industryName }
        ];
        apiRequest("api/knowledge_master", request, callback);
    }

    function changeIndustryStatus(industryId, isActive, callback) {
        var request = [
            "ChangeIndustryStatus",
            {"industry_id" : industryId, "is_active" : isActive}
        ];
        apiRequest("api/knowledge_master", request, callback);
    }

    function getIndustryList(callback) {
        var request = ["GetIndustries", {}];
        apiRequest("api/knowledge_master", request, callback);
    }

    //Statutory Nature Master

    function saveStatutoryNature(statutoryNatureName, callback) {
        var request = [
            "SaveStatutoryNature",
            { "statutory_nature_name" : statutoryNatureName }
        ];
        apiRequest("api/knowledge_master", request, callback);
    }

    function updateStatutoryNature(statutoryNatureId, statutoryNatureName, 
        callback) {
        var request = [
            "UpdateStatutoryNature",
            { "statutory_nature_id" : statutoryNatureId, "statutory_nature_name" : statutoryNatureName }
        ];
        apiRequest("api/knowledge_master", request, callback);
    }

    function changeStatutoryNatureStatus(statutoryNatureId, isActive, 
        callback) {
        var request = [
            "ChangeStatutoryNatureStatus",
            {"statutory_nature_id" : statutoryNatureId, "is_active" : isActive}
        ];
        apiRequest("api/knowledge_master", request, callback);
    }

    function getStatutoryNatureList(callback) {
        var request = ["GetStatutoryNatures", {}];
        apiRequest("api/knowledge_master", request, callback);
    }

    // Geography Levels 
    function getGeographyLevels(callback) {
        var request = ["GetGeographyLevels", {}];
        apiRequest("api/knowledge_master", request, callback);   
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
        apiRequest("api/knowledge_master", request, callback);
    }

    // Statutory Levels
    function getStatutoryLevels(callback) {
        var request = ["GetStatutoryLevels", {}];
        apiRequest("api/knowledge_master", request, callback);   
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
        apiRequest("api/knowledge_master", request, callback);
    }

    //Geographies
    function getGeographies(callback) {
        var request = ["GetGeographies", {}];
        apiRequest("api/knowledge_master", request, callback);   
    }

    function saveGeography(levelId, name, parentIds, countryId, callback) {
        var request = [
            "SaveGeography",
            { 
                "geography_level_id": levelId,
                "geography_name": name,
                "parent_ids": parentIds,
                "country_id": countryId
            }
        ];
        apiRequest("api/knowledge_master", request, callback);
    }

    function updateGeography(
        geographyId, levelId, name, parentIds, countryId, callback
    ) {
        var request = [
            "UpdateGeography",
            { 
                "geography_id": geographyId,
                "geography_level_id": levelId,
                "geography_name": name,
                "parent_ids": parentIds,
                "country_id": countryId
            }
        ];
        apiRequest("api/knowledge_master", request, callback);
    }

    function changeGeographyStatus(geographyId, isActive, callback) {
        var request = [
            "ChangeGeographyStatus",
            { 
                "geography_id": geographyId,
                "is_active": isActive
            }
        ];
        apiRequest("api/knowledge_master", request, callback);
    }

    function getGeographyReport(callback) {
        var request = ["GetGeographyReport", {}];
        apiRequest("api/knowledge_report", request, callback);   
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
        apiRequest("api/knowledge_master", request, callback);
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
        apiRequest("api/knowledge_master", request, callback);
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
        compliance["format_file_list"] = fileFormat;
        compliance["penal_consequences"] = penalConsequence;
        compliance["frequency_id"] = complianceFrequency;
        compliance["statutory_dates"] = statutoryDates;
        compliance["repeats_type_id"] = repeatsTypeId;
        compliance["repeats_every"] = repeatsEvery;
        compliance["duration_type_id"] = durationTypeId;
        compliance["duration"] = duration;
        compliance["is_active"] = isActive;
        if ((complianceId !== null) && (complianceId !== '')) {
            compliance["compliance_id"] = complianceId;
        }
        else {
            compliance["compliance_id"] = null
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
        apiRequest("api/knowledge_transaction", request, callback);
    }

    function UpdateStatutoryMappingData(
        industryIds, statutoryNatureId, 
        statutoryIds, compliances, geographyIds, mappingId
    ) {
        var mappingData = {};
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


    function updateStatutoryMapping(mappingData, callback ) {
        var request = [
            "UpdateStatutoryMapping",
            mappingData
        ]
        apiRequest("api/knowledge_transaction", request, callback);
    }
    
    function getStatutoryMappings(callback) {
        var request = ["GetStatutoryMappings", {}];
        apiRequest("api/knowledge_transaction", request, callback);
    }

    function changeStatutoryMappingStatus(mappingId, isActive, callback) {
        var request = [
            "ChangeStatutoryMappingStatus",
            {
                "statutory_mapping_id":mappingId,
                "is_active" : isActive
            }
        ]
        apiRequest("api/knowledge_transaction", request, callback);
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
        apiRequest("api/knowledge_transaction", request, callback);
    }

    function getStatutoryMappingsReportFilter(callback) {
        var request = ["GetStatutoryMappingReportFilters", {}];
        apiRequest("api/knowledge_report", request, callback);
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
        apiRequest("api/knowledge_report", request, callback);
    }

    // Admin User Group Master
    function getAdminUserGroupList(callback) {
        callerName = "api/admin"
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
        callerName = "api/admin"
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
        callerName = "api/admin"
        var request = [
            "UpdateUserGroup",
            userGroupDetail
        ];
        apiRequest(callerName, request, callback);
    }

    function changeAdminUserGroupStatus(userGroupId, isActive, callback) {
        callerName = "api/admin"
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
        callerName = "api/admin"
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
    
    function saveAdminUser(userDetail, callback) {
        callerName = "api/admin"
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

    function updateAdminUser(userDetail, callback) {
        callerName = "api/admin"        
        var request = [
            "UpdateUser",
            userDetail
        ];
        apiRequest(callerName, request, callback);
    }

    function changeAdminUserStatus(userId, isActive,
     callback) {
        callerName = "api/admin"
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

    function getDateConfigurations(countryId, domainId, periodFrom, 
        periodTo){
        return {
            "country_id": countryId,
            "domain_id": domainId,
            "period_from": periodFrom,
            "period_to": periodTo
        }
    }
    
    function getSaveClientGroupDict(groupName, countryIds, domainIds, logo,
        contractFrom, contractTo, inchargePersons, noOfUserLicence, fileSpace,
        isSmsSubscribed, emailId, dateConfigurations, shortName){
        return {
            "group_name": groupName,
            "country_ids": countryIds,
            "domain_ids": domainIds,
            "logo" : logo,
            "contract_from": contractFrom,
            "contract_to": contractTo,
            "incharge_persons": inchargePersons,
            "no_of_user_licence": noOfUserLicence,
            "file_space": fileSpace,
            "is_sms_subscribed": isSmsSubscribed,
            "email_id": emailId,
            "date_configurations":dateConfigurations,
            "short_name": shortName
        }
    }

    function saveClientGroup(clientGroupDetails, 
        callback) {
        callerName = "api/techno"
        var request = [
            "SaveClientGroup",
            clientGroupDetails
        ];
       
        apiRequest(callerName, request, callback);
    }

    function getUpdateClientGroupDict(clientId, groupName, countryIds, domainIds, logo,
        contractFrom, contractTo, inchargePersons, noOfUserLicence, fileSpace,
        isSmsSubscribed, dateConfigurations){
        return {
            "client_id": clientId,
            "group_name": groupName,
            "country_ids": countryIds,
            "domain_ids": domainIds,
            "logo" : logo,
            "contract_from": contractFrom,
            "contract_to": contractTo,
            "incharge_persons": inchargePersons,
            "no_of_user_licence": noOfUserLicence,
            "file_space": fileSpace,
            "is_sms_subscribed": isSmsSubscribed,
            "date_configurations":dateConfigurations
        }
    } 

    function updateClientGroup(clientGroupDetails, callback) {
        callerName = "api/techno"
        var request = [
            "UpdateClientGroup",
            clientGroupDetails
        ];
        apiRequest(callerName, request, callback);
    }

    function changeClientGroupStatus( clientId, isActive, 
        callback) {
        callerName = "api/techno"
        var request = [
            "ChangeClientGroupStatus",
            {
                "client_id": clientId,
                "is_active": isActive
            }
        ];
        apiRequest(callerName, request, callback);
    }

    function getClientGroups(callback) {
        callerName = "api/techno"
        var request = [
            "GetClientGroups",
            {}
        ];
        apiRequest(callerName, request, callback);
    }

    // Change Password APIs

    function changePassword(currentPassword, newPassword,
     callback) {
        callerName = "api/login"
        var request = [
            "ChangePassword",
            {
                "session_token": getSessionToken(),
                "current_password": currentPassword,
                "new_password": newPassword
            }
        ];
        LoginApiRequest(callerName, request, callback);
    }

    // Forgot Password APIs

    function forgotPassword(username, callback) {
        callerName = "api/login"
        var request = [
            "ForgotPassword",
            {
                "username": username,
                "short_name": getShortName()
            }
        ];
        LoginApiRequest(callerName, request, callback);
    }

    function validateResetToken(resetToken, 
        callback) {
        callerName = "api/login"
        var request = [
            "ResetTokenValidation",
            {
                "reset_token": resetToken,
                "short_name": getShortName()
            }
        ];
        LoginApiRequest(callerName, request, callback);
    }

    function resetPassword( resetToken, newPassword, 
        callback) {
        callerName = "api/login"
        var request = [
            "ResetPassword",
            {
                "reset_token": resetToken,
                "new_password": newPassword,
                "short_name": getShortName()
            }
        ];
        LoginApiRequest(callerName, request, callback);
    }

    // Client Unit APIs

    function getClients(callback) {
        callerName = "api/techno"
        var request = [
            "GetClients",
            {}
        ];
        apiRequest(callerName, request, callback);
    }

    function getBusinessGroupDict(businessGroupId, busienssGroupName){
        return {
            "business_group_id" : businessGroupId,
            "business_group_name" : busienssGroupName
        }
    }

    function getLegalEntityDict(legalEntityId, legalEntityName){
        return {
            "legal_entity_id" : legalEntityId,
            "legal_entity_name" : legalEntityName
        }
    }

    function getDivisionDict(divisionId, divisionName){
        return {
            "division_id" : divisionId,
            "division_name" : divisionName
        }
    }

    function getUnitDict(unitId, unitName, unitCode, unitAddress,
        postalCode, geographyId, unitLocation, industryId, industryName,
        domainIds){
        return {
            "unit_id" : unitId,
            "unit_name" : unitName,
            "unit_code" : unitCode,
            "unit_address" : unitAddress,
            "postal_code" : postalCode,
            "geography_id" : geographyId,
            "unit_location" : unitLocation,
            "industry_id" : industryId,
            "industry_name" : industryName,
            "domain_ids" : domainIds
        }
    }

    function mapUnitsToCountry(countryId, units){
        return {
            "country_id" : countryId,
            "units" : units
        }
    }

    function saveClient(clientId, businessGroup, legalEntity, 
        division, countryWiseUnits, callback) {
        callerName = "api/techno"
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


    function updateClient(clientId, businessGroup, legalEntity, 
        division, countryWiseUnits, callback) {
        callerName = "api/techno"
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

    function changeClientStatus(clientId, legalEntityId, divisionId, isActive, 
        callback) {
        callerName = "api/techno"
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

    function reactivateUnit(clientId, unitId, password, 
        callback) {
        callerName = "api/techno"
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

    //Client Profile
    function getClientProfile(callback){
        callerName = "api/techno"
        var request = [
            "GetClientProfile",
            {}
        ];
        apiRequest(callerName, request, callback);
    }

    // Client Details Report
    function getClientDetailsReportFilters(callback){
        callerName = "api/techno_report"
        var request = [
            "GetClientDetailsReportFilters",
            {}
        ];
        apiRequest(callerName, request, callback);
    }

    function getClientDetailsReport(countryId, clientId, businessGroupId, legalEntityId, divisionId, 
        unitId, domainIds, callback){
        callerName = "api/techno_report"
        var request = [
            "GetClientDetailsReportData",
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
        apiRequest(callerName, request, callback);
    }

    // Assign statutories
    function getAssignStatutoryWizardOne(countryId, callback) {
        var request = [
            "GetAssignedStatutoryWizardOneData",
            {
                "country_id": countryId
            }
        ];
        callerName = "api/techno_transaction"
        apiRequest(callerName, request, callback)
    }

    function getAssignStatutoryWizardTwo(countryId, domainId, industryId, geographyId, unitId, callback) {
        var request = [
            "GetStatutoryWizardTwoData",
            {
                "country_id": countryId,
                "domain_id": domainId,
                "industry_id": industryId,
                "geography_id": geographyId,
                "unit_id": unitId
            }
        ]
        callerName = "api/techno_transaction"
        apiRequest(callerName, request, callback)
    }

    function getAssignedStatutoriesList(callback) {
        var request = [
            "GetAssignedStatutoriesList", {}
        ];
        callerName = "api/techno_transaction";
        apiRequest(callerName, request, callback);
    }

    function assignedStatutories(level1ID, compliances, applicableStatus, remarks) {
        var statutories = {
            "level_1_statutory_id": level1ID,
            "compliances": compliances,
            "applicable_status": applicableStatus,
            "not_applicable_remarks": remarks
        };
        return statutories;
    }

    function saveOrSubmitAssignStatutory(
        countryId, clientId, geographyId, unitIds, 
        domainId, submissionType, clientStatutoryId, 
        assignStatutories, callback
    ){
        var request = [
            "SaveAssignedStatutory",
            {
                "country_id": countryId,
                "client_id": clientId,
                "geography_id": geographyId,
                "unit_ids": unitIds,
                "domain_id": domainId,
                "submission_type": submissionType,
                "client_statutory_id": clientStatutoryId,
                "assigned_statutories": assignStatutories
            }
        ];
        callerName = "api/techno_transaction";
        apiRequest(callerName, request, callback);
    }
    
    function getAssignedStatutoryById(clientStatutoryId, callback) {
        var request = [
            "GetAssignedStatutoriesById",
            {
                "client_statutory_id": clientStatutoryId
            }
        ];
        callerName = "api/techno_transaction"
        apiRequest(callerName, request, callback);
    }
    
    function getAssignedStatutoryReportFilters(callback) {
        var request = [
            "GetAssignedStatutoryReportFilters",
            {}
        ];
        callerName = "api/techno_report";
        apiRequest(callerName, request, callback);
    }
    
    function getAssignedStatutoryReport(countryId, domainId, 
        clientId, businessGroupId, legalEntityId, divisionId, 
        unitId, level1StatutoryId, applicableStatus, callback
    ){
        var request = [
            "GetAssignedStatutoryReport",
            {
                "country_id": countryId,
                "domain_id": domainId,
                "group_id": clientId,
                "business_group_id": businessGroupId,
                "legal_entity_id": legalEntityId,
                "division_id": divisionId,
                "unit_id": unitId,
                "level_1_statutory_id" : level1StatutoryId,
                "applicability_status" : applicableStatus
            }
        ];
        console.log(request)
        callerName = "api/techno_report";
        apiRequest(callerName, request, callback);
    }

    function getAuditTrail(callback){
        callerName = "api/general"
        var request = [
            "GetAuditTrails",
            {}
        ];
        apiRequest(callerName, request, callback);
    }

    function updateUserProfile(contact_no, address, callback){
        callerName = "api/general"
        var request = [
            "UpdateUserProfile",
            {
                "contact_no" : contact_no,
                "address" : address
            }
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
        logout: logout,

        getUserInfo: getUserInfo,
        updateUserInfo: updateUserInfo,
        getUserProfile: getUserProfile,
        getSessionToken: getSessionToken,
        getUserMenu: getUserMenu,
        apiRequest: apiRequest,
        LoginApiRequest : LoginApiRequest,

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
        UpdateStatutoryMappingData: UpdateStatutoryMappingData,

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

        getDateConfigurations: getDateConfigurations,
        getSaveClientGroupDict: getSaveClientGroupDict,
        saveClientGroup: saveClientGroup,
        getUpdateClientGroupDict: getUpdateClientGroupDict,
        updateClientGroup: updateClientGroup,
        getClientGroups: getClientGroups,
        changeClientGroupStatus: changeClientGroupStatus,

        changePassword: changePassword,
        forgotPassword: forgotPassword,
        validateResetToken: validateResetToken,
        resetPassword: resetPassword,

        getClients: getClients,
        getBusinessGroupDict :getBusinessGroupDict , 
        getLegalEntityDict :getLegalEntityDict , 
        getDivisionDict :getDivisionDict , 
        getUnitDict :getUnitDict , 
        mapUnitsToCountry : mapUnitsToCountry,
        saveClient: saveClient,
        updateClient : updateClient,
        changeClientStatus: changeClientStatus,
        reactivateUnit: reactivateUnit,

        getClientProfile: getClientProfile,
        getClientDetailsReportFilters: getClientDetailsReportFilters,
        getClientDetailsReport: getClientDetailsReport,

        getAssignStatutoryWizardOne: getAssignStatutoryWizardOne,
        getAssignStatutoryWizardTwo: getAssignStatutoryWizardTwo,
        getAssignedStatutoriesList: getAssignedStatutoriesList,
        assignedStatutories: assignedStatutories,
        saveOrSubmitAssignStatutory: saveOrSubmitAssignStatutory,
        getAssignedStatutoryById: getAssignedStatutoryById,
        getAssignedStatutoryReportFilters: getAssignedStatutoryReportFilters,
        getAssignedStatutoryReport: getAssignedStatutoryReport,

        getAuditTrail: getAuditTrail,
        updateUserProfile: updateUserProfile
    }

}
var mirror = initMirror();