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
        console.log(toJSON(userProfile))
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
        console.log(info)
        return info["client_id"];
    }

    function clientApiRequest(callerName, request, callback) {
        var sessionToken = getSessionToken();
        if (sessionToken == null)
            sessionToken = "b4c59894336c4ee3b598f5e4bd2b276b";
        var requestFrame = {
            "session_token": sessionToken,
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
                else{
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
        var sessionToken = getSessionToken();
        var client_id = getClientId()
        var request = [
            "ChangePassword",
            {
                "session_token" : client_id+"-"+sessionToken,
                "current_password": currentPassword,
                "new_password": newPassword
            }
        ];
        clientLoginApiRequest(callerName, request, callback);
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
        clientApiRequest(callerName, request, callback);
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
        clientApiRequest(callerName, request, callback);
    }

    function resetPassword(resetToken, newPassword, 
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

    function getAuditTrail(callback){
        callerName = "api/client_masters"
        var request = [
            "GetAuditTrails",
            {}
        ];
        clientApiRequest(callerName, request, callback);
    }

    function getComplianceDetailsReportFilters(callback){
        callerName = "api/client_reports"
        var request = [
            "GetComplianceDetailsReportFilters",
            {}
        ];
        clientApiRequest(callerName, request, callback);   
    }

    // 
    // Statutory settings
    // 
    function getStatutorySettings(callback) {
        callerName = "api/client_transaction";
        var request = [
            "GetStatutorySettings",
            {}
        ]
        clientApiRequest(callerName, request, callback);
    }

    function updateCompliances(complianceId, optedStatus, remarks) {
        return {
            "compliance_id": complianceId,
            "compliance_opted_status": optedStatus,
            "compliance_remarks": remarks
        }
    }

    function updateStatutory(clientStatutoryId, compliances, applicableStatus, applicableRemarks) {
        return {
            "client_statutory_id": clientStatutoryId,
            "compliances": compliances,
            "applicable_status": applicableStatus,
            "not_applicable_remarks": applicableRemarks
        };
    }

    function updateStatutorySettings(unitId, statutories, callback){
        var request = [
            "UpdateStatutorySettings", 
            {
                "unit_id": unitId,
                "statutories": statutories
            }
        ];
        var callerName = "api/client_transaction";
        clientApiRequest(callerName, request, callback);
    }

    // 
    // Assign compliance
    // 

    function getAssignComplianceFormData(callback){
        var request = [
            "GetAssignCompliancesFormData",
            {}
        ];
        var callerName = "api/client_transaction";
        clientApiRequest(callerName, request, callback);
    }

    function getAssignComplianceForUnits(unitIds, callback) {
        var request = [
            "GetComplianceForUnits",
            {
                "unit_ids": unitIds
            }
        ];
        var callerName = "api/client_transaction";
        clientApiRequest(callerName, request, callback);
    }

    function statutoryDates(date, month, triggerBefore) {
        var statutoryDate = {};
        statutoryDate["statutory_date"] = date;
        statutoryDate["statutory_month"] = month;
        statutoryDate["trigger_before_days"] = triggerBefore;
        return statutoryDate;
    }

    function assignCompliances(complianceId, statutoryDateList, dueDate, validityDate, unitIds, callback) {
        return {
            "compliance_id": complianceId,
            "statutory_dates": statutoryDateList,
            "due_date": dueDate,
            "validity_date": validityDate,
            "unit_ids": unitIds
        }
    }

    function saveAssignedComplianceFormData(countryId, assignee, concurrence, approval, compliances, callback) {
        var request = [
            "SaveAssignedCompliance",
            {
                "country_id": countryId,
                "assignee": assignee,
                "concurrence_person": concurrence,
                "approval_person": approval,
                "compliances": compliances
            }
        ];
        var callerName = "api/client_transaction";
        clientApiRequest(callerName, request, callback);   
    }

    // 
    // Past Records
    // 

    function getPastRecordsFormData(callback){
       var request = [
            "GetPastRecordsFormData",
            {}
       ];
       clientApiRequest("api/client_transaction", request, callback);
    }

    function getStatutoriesByUnit(unit_id, domain_id, level_1_statutory_id, 
                    frequency_id, callback){
        var request = [
            "GetStatutoriesByUnit",
            {
                "unit_id" : unit_id,
                "domain_id" : domain_id,
                "level_1_statutory_id": level_1_statutory_id,
                "compliance_frequency" : frequency_id
            }
        ]
        clientApiRequest("api/client_transaction", request, callback);  
    } 

    function getComplianceApprovalList(callback){
        var request = [
            "GetComplianceApprovalList",
            {}
        ];
        clientApiRequest("api/client_transaction", request, callback);
    }

    function getClientReportFilters(callback) {
        var request = [
            "GetClientReportFilters",
            {}
        ];
        callerName = "api/client_reports";
        clientApiRequest(callerName, request, callback);
    }
    
    function getUnitwisecomplianceReport(country_id, domain_id, business_group_id, legal_entity_id, 
        division_id, unit_id, user_id, callback) {
        var request = [
            "GetUnitwisecomplianceReport",
            {
                "country_id": country_id,
                "domain_id": domain_id,
                "business_group_id": business_group_id,
                "legal_entity_id": legal_entity_id,
                "division_id"  : division_id,
                "unit_id": unit_id,
                "user_id": user_id
            }
        ];
        callerName = "api/client_reports";
        clientApiRequest(callerName, request, callback);
    }
    
    function getAssigneewisecomplianceReport(country_id, domain_id, business_group_id, legal_entity_id, 
        division_id, unit_id, user_id, callback) {
        var request = [
            "GetAssigneewisecomplianceReport",
            {
                "country_id": country_id,
                "domain_id": domain_id,
                "business_group_id": business_group_id,
                "legal_entity_id": legal_entity_id,
                "division_id"  : division_id,
                "unit_id": unit_id,
                "user_id": user_id
            }
        ];
        callerName = "api/client_reports";
        clientApiRequest(callerName, request, callback);
    }


    function approveCompliance(compliance_history_id, compliance_approval_status, 
        remarks, next_due_date, callback){
        console.log()
        var request = [
            "ApproveCompliance",
            {
                "compliance_history_id": compliance_history_id,
                "approval_status": compliance_approval_status,
                "remarks": remarks,
                "next_due_date":next_due_date
            }
        ];
        callerName = "api/client_transaction";
        clientApiRequest(callerName, request, callback);
    }

    function getChartFilters(callback) {
        var request = [
            "GetChartFilters",
            {}
        ];
        var callerName = "api/client_dashboard";
        clientApiRequest(callerName, request, callback);         
    }

    function getComplianceStatusChartData(countryIds, domainIds, filterType, filterIds, fromDate, toDate,  callback) {
        var request = [
            "GetComplianceStatusChart",
            {
                "country_ids": countryIds,
                "domain_ids": domainIds,
                "filter_type": filterType,
                "filter_ids": filterIds,
                "from_date": fromDate,
                "to_date": toDate,

            }
        ];
        var callerName = "api/client_dashboard";
        clientApiRequest(callerName, request, callback); 
    }

/* Trend Chart */

    function getTrendChart(country_ids, domain_ids, filter_type, 
        filter_id, callback){
        var request = [
            "GetTrendChart",
            {
                "country_ids": country_ids,
                "domain_ids": domain_ids,
                "filter_type": filter_type,
                "filter_ids": filter_id
            }
        ];
        var callerName = "api/client_dashboard"
        clientApiRequest(callerName, request, callback)
    }
    function getTrendChartDrillDown(country_ids, domain_ids, filter_type, 
        filter_ids, year, callback){
        var request = [
            "GetTrendChartDrillDownData",
            {
                "country_ids": country_ids,
                "domain_ids": domain_ids,
                "filter_type": filter_type,
                "filter_ids": filter_ids,
                "year" : year
            }
        ];
        var callerName = "api/client_dashboard"
        clientApiRequest(callerName, request, callback)
    }

/* Settings */

    function getSettings(callback){
        var request = [
            "GetSettings",
            {}
        ];
        var callerName = "api/client_admin_settings"
        clientApiRequest(callerName, request, callback)
    }

    function updateSettings(is_two_levels_of_approval, assignee_reminder_days, 
        escalation_reminder_In_advance_days, escalation_reminder_days, callback){
        var request = [
            "UpdateSettings",
            {
               "is_two_levels_of_approval": is_two_levels_of_approval,
                "assignee_reminder_days": assignee_reminder_days,
                "escalation_reminder_In_advance_days": escalation_reminder_In_advance_days,
                "escalation_reminder_days": escalation_reminder_days 
            }  
        ];
        var callerName = "api/client_admin_settings"
        clientApiRequest(callerName, request, callback)
    }

    /* Notifications */
    
    function getNotifications(notification_type, callback){
        callerName = "api/general"
        var request = [
            "GetNotifications",
            {
                "notification_type" : notification_type
            }
        ];
        clientApiRequest(callerName, request, callback);
    }

    function updateNotificationStatus(notification_id, has_read, callback){
        callerName = "api/general"
        var request = [
            "UpdateNotificationStatus",
            {
                "notification_id" : notification_id,
                "has_read" : has_read
            }
        ];
        clientApiRequest(callerName, request, callback);
    }

/* Get Compliance List*/
    function  getComplianceDetail(callback){
        callerName = "api/client_user"
        var request = [
            "GetComplianceDetail",
            {
               
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
        getClientDetailsReport: getClientDetailsReport,
        getAuditTrail: getAuditTrail,

        getComplianceDetailsReportFilters: getComplianceDetailsReportFilters,

        getStatutorySettings: getStatutorySettings,
        updateCompliances: updateCompliances,
        updateStatutory: updateStatutory,
        updateStatutorySettings: updateStatutorySettings,

        getAssignComplianceFormData: getAssignComplianceFormData,
        getAssignComplianceForUnits: getAssignComplianceForUnits,
        statutoryDates: statutoryDates,
        assignCompliances: assignCompliances,
        saveAssignedComplianceFormData: saveAssignedComplianceFormData,

        getPastRecordsFormData: getPastRecordsFormData,
        getStatutoriesByUnit: getStatutoriesByUnit,

        getClientReportFilters: getClientReportFilters,
        getUnitwisecomplianceReport: getUnitwisecomplianceReport,
        getAssigneewisecomplianceReport: getAssigneewisecomplianceReport,

        getComplianceApprovalList: getComplianceApprovalList,
        approveCompliance: approveCompliance,

        getChartFilters: getChartFilters,
        getComplianceStatusChartData : getComplianceStatusChartData,
        getTrendChart: getTrendChart,
        getTrendChartDrillDown: getTrendChartDrillDown,

        getSettings: getSettings,
        updateSettings: updateSettings,
        getNotifications: getNotifications,
        updateNotificationStatus: updateNotificationStatus,

        getComplianceDetail: getComplianceDetail
    }
}
var client_mirror = initClientMirror();
