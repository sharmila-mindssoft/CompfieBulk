// var CLIENT_BASE_URL = "http://localhost:8080/";
var CLIENT_BASE_URL = "/api/";

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

    function initSession(userProfile, shortName) {
        // console.log(toJSON(userProfile))
        window.localStorage["userInfo"] = toJSON(userProfile);
        window.localStorage["shortName"] = shortName;
    }

    function getShortName() {
        var pathArray = window.location.pathname.split('/');
        if (typeof pathArray[2] === 'undefined') {
            return null;
        } else {
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
        delete window.localStorage["shortName"];
    }

    function getUserInfo() {
        var info = window.localStorage["userInfo"];
        user = parseJSON(info)
        return user;
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

    function getUserMenu() {
        var info = getUserInfo();
        return info["menu"]["menus"];
    }

    function getClientId() {
        var info = getUserInfo();
        // console.log(info)
        return info["client_id"];
    }

    function getClientShortName(){
        var name = window.localStorage["shortName"];
        return name;
    }

    function redirect_login(){
        login_url = "/login/" + getClientShortName();
        // console.log(login_url)
        clearSession();
        window.location.href = login_url;
    }

    function clientApiRequest(callerName, request, callback) {
        var sessionToken = getSessionToken();
        if (sessionToken == null)
            sessionToken = "b4c59894336c4ee3b598f5e4bd2b276b";
        var requestFrame = {
            "session_token": sessionToken,
            "request": request
        };
        var body = [
            sessionToken, requestFrame
        ]
        jQuery.post(
            CLIENT_BASE_URL + callerName,
            toJSON(body),
            function(data) {
                var data = parseJSON(data);
                var status = data[0];
                var response = data[1];
                matchString = 'success';
                log("API STATUS :" + status)

                if (status.toLowerCase().indexOf(matchString) != -1) {
                    callback(null, response);
                }
                else if (status == "InvalidSessionToken") {
                    // console.log(status)
                    redirect_login()
                }
                else {
                    callback(status, null)
                }

            }
        )
            .fail(
                function(jqXHR, textStatus, errorThrown) {
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
            short_name, [
                "Login", {
                    "login_type": "Web",
                    "username": username,
                    "password": password,
                    "short_name": short_name
                }
            ]
        ]
        jQuery.post(
            CLIENT_BASE_URL + "login",
            toJSON(request),
            function(data) {
                var data = parseJSON(data);
                var status = data[0];
                var response = data[1];
                matchString = 'success';
                if (status.toLowerCase().indexOf(matchString) != -1) {
                    console.log("status success");
                    initSession(response, short_name)
                    callback(null, response);

                }
                else {
                    callback(status, null);
                }
            }
        )
    }

    function verifyLoggedIn() {
        sessionToken = getSessionToken();
        if (sessionToken == null)
            return false;
        else
            return true;
    }

    function logout() {
        sessionToken = getSessionToken()
        var request =  [
            sessionToken,
            [
                "Logout", {
                    "session_token": sessionToken
                }
            ]
        ];

        jQuery.post(
            CLIENT_BASE_URL + "login",
            toJSON(request),
            function(data) {
                var data = parseJSON(data);
                var status = data[0];
                var response = data[1];
                matchString = 'success';
                // if (status.toLowerCase().indexOf(matchString) != -1) {
                //     callback(null, response);
                // } else {
                //     callback(status, null);
                // }
                redirect_login()
            }
        )
    }

    // Change Password APIs

    function changePassword(
        currentPassword, newPassword,
        callback
    ) {
        callerName = "login"
        var sessionToken = getSessionToken();
        var client_id = getClientId()
        var request = [
            "ChangePassword", {
                "session_token": client_id + "-" + sessionToken,
                "current_password": currentPassword,
                "new_password": newPassword
            }
        ];
        clientLoginApiRequest(callerName, request, callback);
    }

    // Forgot Password APIs

    function forgotPassword(username, callback) {
        callerName = "login"
        var short_name = getShortName();
        var request = [
            short_name, [
                "ForgotPassword", {
                    "username": username,
                    "short_name" : short_name
                }
            ]
        ]
        jQuery.post(
            CLIENT_BASE_URL + callerName,
            toJSON(request),
            function(data) {
                var data = parseJSON(data);
                var status = data[0];
                var response = data[1];
                matchString = 'success';
                if (status.toLowerCase().indexOf(matchString) != -1) {
                    console.log("status success");
                    initSession(response, short_name)
                    callback(null, response);

                }
                else {
                    callback(status, null);
                }
            }
        )
    }

    function validateResetToken(resetToken,
        callback) {
        callerName = "login"
        var request = [
            "ResetTokenValidation", {
                "reset_token": resetToken,
                "short_name": getShortName()
            }
        ];
        clientApiRequest(callerName, request, callback);
    }

    function resetPassword(resetToken, newPassword,
        callback) {
        callerName = "login"
        var request = [
            "ResetPassword", {
                "reset_token": resetToken,
                "new_password": newPassword,
                "short_name": getShortName()
            }
        ];
        clientApiRequest(callerName, request, callback);
    }

    // Client User Group
    function getClientUserGroups(callback) {
        callerName = "client_masters"
        var request = [
            "GetUserPrivileges", {}
        ];
        clientApiRequest(callerName, request, callback);
    }

    function getSaveClientUserGroupDict(userGroupName, formIds) {
        return {
            "user_group_name": userGroupName,
            "form_ids": formIds
        }
    }

    function saveClientUserGroup(userGroupDetail, callback) {
        callerName = "client_masters"
        var request = [
            "SaveUserPrivileges",
            userGroupDetail
        ];
        clientApiRequest(callerName, request, callback);
    }

    function getUpdateClientUserGroupDict(userGroupId, userGroupName, formIds) {
        return {
            "user_group_id": userGroupId,
            "user_group_name": userGroupName,
            "form_ids": formIds
        }
    }

    function updateClientUserGroup(userGroupDetail, callback) {
        callerName = "client_masters"
        var request = [
            "UpdateUserPrivileges",
            userGroupDetail
        ];
        clientApiRequest(callerName, request, callback);
    }

    function changeClientUserGroupStatus(userGroupId, isActive,
        callback) {
        callerName = "client_masters"
        var request = [
            "ChangeUserPrivilegeStatus", {
                "user_group_id": userGroupId,
                "is_active": isActive
            }
        ];
        clientApiRequest(callerName, request, callback);
    }

    // Service Providers

    function getServiceProviders(callback) {
        callerName = "client_masters"
        var request = [
            "GetServiceProviders", {}
        ];
        clientApiRequest(callerName, request, callback);
    }

    function getSaveServiceProviderDict(serviceProviderDetail) {
        return {
            "service_provider_name": serviceProviderDetail[0],
            "address": serviceProviderDetail[1],
            "contract_from": serviceProviderDetail[2],
            "contract_to": serviceProviderDetail[3],
            "contact_person": serviceProviderDetail[4],
            "contact_no": serviceProviderDetail[5]
        }
    }

    function saveServiceProvider(serviceProviderDetail, callback) {
        callerName = "client_masters"
        var request = [
            "SaveServiceProvider",
            serviceProviderDetail
        ];
        clientApiRequest(callerName, request, callback);
    }

    function getUpdateServiceProviderDict(serviceProviderDetail) {
        return {
            "service_provider_id": serviceProviderDetail[0],
            "service_provider_name": serviceProviderDetail[1],
            "address": serviceProviderDetail[2],
            "contract_from": serviceProviderDetail[3],
            "contract_to": serviceProviderDetail[4],
            "contact_person": serviceProviderDetail[5],
            "contact_no": serviceProviderDetail[6]
        }
    }

    function updateServiceProvider(serviceProviderDetail,
        callback) {
        callerName = "client_masters"
        var request = [
            "UpdateServiceProvider",
            serviceProviderDetail
        ];
        clientApiRequest(callerName, request, callback);
    }

    function changeServiceProviderStatus(serviceProviderId,
        isActive, callback) {
        callerName = "client_masters"
        var request = [
            "ChangeServiceProviderStatus", {
                "service_provider_id": serviceProviderId,
                "is_active": isActive
            }
        ];
        clientApiRequest(callerName, request, callback);
    }

    // Client User
    function getClientUsers(callback) {
        callerName = "client_masters"
        var request = [
            "GetClientUsers", {}
        ];
        clientApiRequest(callerName, request, callback);
    }

    function getSaveClientUserDict(clientUserDetail) {
        return {
            "email_id": clientUserDetail[0],
            "user_group_id": clientUserDetail[1],
            "employee_name": clientUserDetail[2],
            "employee_code": clientUserDetail[3],
            "contact_no": clientUserDetail[4],
            "seating_unit_id": clientUserDetail[5],
            "user_level": clientUserDetail[6],
            "country_ids": clientUserDetail[7],
            "domain_ids": clientUserDetail[8],
            "unit_ids": clientUserDetail[9],
            "is_admin": clientUserDetail[10],
            "is_service_provider": clientUserDetail[11],
            "service_provider_id": clientUserDetail[12]
        }
    }

    function saveClientUser(clientUserDetail, callback) {
        callerName = "client_masters"
        var request = [
            "SaveClientUser",
            clientUserDetail
        ];
        clientApiRequest(callerName, request, callback);
    }

    function getUpdateClientUserDict(clientUserDetail) {
        return {
            "user_id": clientUserDetail[0],
            "user_group_id": clientUserDetail[1],
            "employee_name": clientUserDetail[2],
            "employee_code": clientUserDetail[3],
            "contact_no": clientUserDetail[4],
            "seating_unit_id": clientUserDetail[5],
            "user_level": clientUserDetail[6],
            "country_ids": clientUserDetail[7],
            "domain_ids": clientUserDetail[8],
            "unit_ids": clientUserDetail[9],
            "is_admin": clientUserDetail[10],
            "is_service_provider": clientUserDetail[11],
            "service_provider_id": clientUserDetail[12]
        }
    }

    function updateClientUser(clientUserDetail, callback) {
        callerName = "client_masters"
        var request = [
            "UpdateClientUser",
            clientUserDetail
        ];
        clientApiRequest(callerName, request, callback);
    }

    function changeClientUserStatus(userId, isActive, callback) {
        callerName = "client_masters"
        var request = [
            "ChangeClientUserStatus", {
                "user_id": userId,
                "is_active": isActive
            }
        ];
        clientApiRequest(callerName, request, callback);
    }

    function changeAdminStatus(userId, isAdmin, callback) {
        callerName = "client_masters"
        var request = [
            "ChangeAdminStatus", {
                "user_id": userId,
                "is_admin": isAdmin
            }
        ];
        clientApiRequest(callerName, request, callback);
    }

    // Unit Closure
    function getUnitClosureList(callback) {
        callerName = "client_masters"
        var request = [
            "GetUnits", {}
        ];
        clientApiRequest(callerName, request, callback);
    }

    function closeUnit(unitId, password, callback,
        failure_callback) {
        callerName = "client_masters"
        var request = [
            "CloseUnit", {
                "unit_id": unitId,
                "password": password
            }
        ];
        clientApiRequest(callerName, request, callback);
    }

    //Client Profile
    function getClientProfile(callback) {
        callerName = "techno"
        var request = [
            "GetClientProfile", {}
        ];
        clientApiRequest(callerName, request, callback);
    }

    // Client Details Report
    function getClientDetailsReportFilters(callback) {
        callerName = "techno"
        var request = [
            "GetClientDetailsReportFilters", {}
        ];
        clientApiRequest(callerName, request, callback);
    }

    function getClientDetailsReport(countryId, clientId, businessGroupId, legalEntityId, divisionId,
        unitId, domainIds, callback) {
        callerName = "techno"
        var request = [
            "GetClientDetailsReport", {
                "country_id": countryId,
                "group_id": clientId,
                "business_group_id": businessGroupId,
                "legal_entity_id": legalEntityId,
                "division_id": divisionId,
                "unit_id": unitId,
                "domain_ids": domainIds
            }
        ];
        clientApiRequest(callerName, request, callback);
    }

    function getAuditTrail(callback) {
        callerName = "client_masters"
        var request = [
            "GetAuditTrails", {}
        ];
        clientApiRequest(callerName, request, callback);
    }

    //
    // Statutory settings
    //
    function getStatutorySettings(callback) {
        callerName = "client_transaction";
        var request = [
            "GetStatutorySettings", {}
        ]
        clientApiRequest(callerName, request, callback);
    }


    function updateStatutory(clientStatutoryId, applicableStatus, applicableRemarks, complianceId, optedStatus, remarks) {
        return {
            "client_statutory_id": clientStatutoryId,
            "applicable_status": applicableStatus,
            "not_applicable_remarks": applicableRemarks,
            "compliance_id": complianceId,
            "compliance_opted_status": optedStatus,
            "compliance_remarks": remarks
        };
    }

    function updateStatutorySettings(unitName, unitId, statutories, callback) {
        var request = [
            "UpdateStatutorySettings", {
                "unit_name": unitName,
                "unit_id": unitId,
                "statutories": statutories
            }
        ];
        var callerName = "client_transaction";
        clientApiRequest(callerName, request, callback);
    }

    //
    // Assign compliance
    //

    function getAssignComplianceFormData(callback) {
        var request = [
            "GetAssignCompliancesFormData", {}
        ];
        var callerName = "client_transaction";
        clientApiRequest(callerName, request, callback);
    }

    function getAssignComplianceForUnits(unitIds, callback) {
        var request = [
            "GetComplianceForUnits", {
                "unit_ids": unitIds
            }
        ];
        var callerName = "client_transaction";
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
            "SaveAssignedCompliance", {
                "country_id": countryId,
                "assignee": assignee,
                "concurrence_person": concurrence,
                "approval_person": approval,
                "compliances": compliances
            }
        ];
        var callerName = "client_transaction";
        clientApiRequest(callerName, request, callback);
    }


    /* Past Records */


    function getPastRecordsFormData(callback) {
        var request = [
            "GetPastRecordsFormData", {}
        ];
        clientApiRequest("client_transaction", request, callback);
    }

    function getStatutoriesByUnit(unit_id, domain_id, level_1_statutory_name,
        compliance_frequency, callback) {
        var request = [
            "GetStatutoriesByUnit", {
                "unit_id": unit_id,
                "domain_id": domain_id,
                "level_1_statutory_name": level_1_statutory_name,
                "compliance_frequency": compliance_frequency
            }
        ]
        clientApiRequest("client_transaction", request, callback);
    }

    function getPastRecordsComplianceDict(
        unit_id, compliance_id, due_date, completion_date, documents, validity_date, completed_by
    ){
        return {
            "unit_id" : unit_id,
            "compliance_id" : compliance_id,
            "due_date" : due_date,
            "completion_date" : completion_date,
            "documents": documents,
            "validity_date": validity_date,
            "completed_by" : completed_by
        };
    }

    function savePastRecords(
        compliances_list, callback
    ){
        var request = [
            "SavePastRecords",
            {
                "compliances" : compliances_list
            }
        ];
        clientApiRequest("client_transaction", request, callback);
    }

/* Multiple File Upload */

    function uploadFileFormat(size, name, content) {
        result = {
            "file_size": parseInt(size),
            "file_name": name,
            "file_content": content
        }
        return result
    }

    function convert_to_base64(file, name, size, callback) {
        var reader = new FileReader();
        reader.onload = function(readerEvt) {
            var binaryString = readerEvt.target.result;
            file_content = btoa(binaryString);
            callback(file_content, name, size)
        };
        reader.readAsBinaryString(file);
    }

    function uploadFile(fileListener, callback) {
        var evt = fileListener
        max_limit =  1024 * 1024 * 50
        // file max limit 50MB
        var files = evt.target.files;
        var results = [];
        for(var i = 0; i < files.length; i++){
            var file = files[i];
            file_name = file.name
            file_size = file.size
            if (file_size > max_limit) {
                callback("File max limit exceeded");
            }
            file_content = null;
            if (file) {
                convert_to_base64(file, file_name, file_size, function(file_content, name, size) {
                    if (file_content == null) {
                        callback("File content is empty")
                    }
                    result = uploadFileFormat(
                            size, name, file_content
                    );
                    results.push(result);
                    if (results.length == files.length){
                        callback(results)
                    }
                });
            }
        }

    }

    /* Compliance Approal */

    function getComplianceApprovalList(callback) {
        var request = [
            "GetComplianceApprovalList", {}
        ];
        clientApiRequest("client_transaction", request, callback);
    }

    function getClientReportFilters(callback) {
        var request = [
            "GetClientReportFilters", {}
        ];
        callerName = "client_reports";
        clientApiRequest(callerName, request, callback);
    }

    function getUnitwisecomplianceReport(
        country_id, domain_id, business_group_id, legal_entity_id,
        division_id, unit_id, user_id, callback
    ) {
        var request = [
            "GetUnitwisecomplianceReport", {
                "country_id": country_id,
                "domain_id": domain_id,
                "business_group_id": business_group_id,
                "legal_entity_id": legal_entity_id,
                "division_id": division_id,
                "unit_id": unit_id,
                "user_id": user_id
            }
        ];
        callerName = "client_reports";
        clientApiRequest(callerName, request, callback);
    }

    function getAssigneewisecomplianceReport(
        country_id, domain_id, business_group_id, legal_entity_id,
        division_id, unit_id, user_id, callback
    ) {
        var request = [
            "GetAssigneewisecomplianceReport", {
                "country_id": country_id,
                "domain_id": domain_id,
                "business_group_id": business_group_id,
                "legal_entity_id": legal_entity_id,
                "division_id": division_id,
                "unit_id": unit_id,
                "user_id": user_id
            }
        ];
        callerName = "client_reports";
        clientApiRequest(callerName, request, callback);
    }

    function approveCompliance(
        compliance_history_id, compliance_approval_status,
        remarks, next_due_date, validity_date, callback
    ) {
        var request = [
            "ApproveCompliance", {
                "compliance_history_id": compliance_history_id,
                "approval_status": compliance_approval_status,
                "remarks": remarks,
                "next_due_date": next_due_date,
                "validity_date" : validity_date
            }
        ];
        console.log(request)
        callerName = "client_transaction";
        clientApiRequest(callerName, request, callback);
    }

    function getChartFilters(callback) {
        var request = [
            "GetChartFilters", {}
        ];
        var callerName = "client_dashboard";
        clientApiRequest(callerName, request, callback);
    }

    // function getComplianceStatusChartData(countryIds, domainIds, filterType, filterIds, fromDate, toDate, callback) {
    //     var request = [
    //         "GetComplianceStatusChart", {
    //             "country_ids": countryIds,
    //             "domain_ids": domainIds,
    //             "filter_type": filterType,
    //             "filter_ids": filterIds,
    //             "from_date": fromDate,
    //             "to_date": toDate,

    //         }

    function getComplianceStatusChartData(requestData, callback) {
        var request = [
            "GetComplianceStatusChart",
            requestData
        ];
        var callerName = "client_dashboard";
        clientApiRequest(callerName, request, callback);
    }

    function getComplianceStatusDrillDown(requestData, callback) {
        var request = [
            "GetComplianceStatusDrillDownData",
            requestData
        ];
        var callerName = "client_dashboard";
        clientApiRequest(callerName, request, callback);
    }

    function getEscalationChartData(requestData, callback) {
        var request = [
            "GetEscalationsChart",
            requestData
        ];
        var callerName = "client_dashboard";
        clientApiRequest(callerName, request, callback);
    }

    function getServiceProviderReportFilters(callback) {
        var request = [
            "GetServiceProviderReportFilters", {}
        ];
        callerName = "client_reports";
        clientApiRequest(callerName, request, callback);
    }

    function getServiceProviderWiseCompliance(country_id, domain_id, statutory_id, unit_id, service_provider_id, callback) {
        var request = [
            "GetServiceProviderWiseCompliance", {
                "country_id": country_id,
                "domain_id": domain_id,
                "statutory_id": statutory_id,
                "unit_id": unit_id,
                "service_provider_id": service_provider_id
            }
        ];
        callerName = "client_reports";
        clientApiRequest(callerName, request, callback);
    }

    function getComplianceDetailsReportFilters(callback) {
        var request = [
            "GetComplianceDetailsReportFilters", {}
        ];
        callerName = "client_reports";
        clientApiRequest(callerName, request, callback);
    }


    function getComplianceDetailsReport(country_id, domain_id, statutory_id, unit_id, compliance_id, assignee_id, from_date, to_date, compliance_status, callback) {
        var request = [
            "GetComplianceDetailsReport", {
                "country_id": country_id,
                "domain_id": domain_id,
                "statutory_id": statutory_id,
                "unit_id": unit_id,
                "compliance_id": compliance_id,
                "assignee_id": assignee_id,
                "from_date": from_date,
                "to_date": to_date,
                "compliance_status": compliance_status
            }
        ];
        callerName = "client_reports";
        clientApiRequest(callerName, request, callback);
    }

    /* Trend Chart */

    function getTrendChart(country_ids, domain_ids, filter_type,
        filter_id, callback) {
        var request = [
            "GetTrendChart", {
                "country_ids": country_ids,
                "domain_ids": domain_ids,
                "filter_type": filter_type,
                "filter_ids": filter_id
            }
        ];
        var callerName = "client_dashboard"
        clientApiRequest(callerName, request, callback)
    }

    function getTrendChartDrillDown(country_ids, domain_ids, filter_type,
        filter_ids, year, callback) {
        var request = [
            "GetTrendChartDrillDownData", {
                "country_ids": country_ids,
                "domain_ids": domain_ids,
                "filter_type": filter_type,
                "filter_ids": filter_ids,
                "year": year
            }
        ];
        var callerName = "client_dashboard"
        clientApiRequest(callerName, request, callback)
    }

    /* Settings */

    function getSettings(callback) {
        var request = [
            "GetSettings", {}
        ];
        var callerName = "client_admin_settings"
        clientApiRequest(callerName, request, callback)
    }

    function updateSettings(is_two_levels_of_approval, assignee_reminder_days,
        escalation_reminder_In_advance_days, escalation_reminder_days, callback) {
        var request = [
            "UpdateSettings", {
                "is_two_levels_of_approval": is_two_levels_of_approval,
                "assignee_reminder_days": assignee_reminder_days,
                "escalation_reminder_In_advance_days": escalation_reminder_In_advance_days,
                "escalation_reminder_days": escalation_reminder_days
            }
        ];
        var callerName = "client_admin_settings"
        clientApiRequest(callerName, request, callback)
    }

    /* Notifications */
    function getNotifications(notification_type, callback) {
        callerName = "client_dashboard"
        var request = [
            "GetNotifications", {
                "notification_type": notification_type
            }
        ];
        clientApiRequest(callerName, request, callback);
    }

    function updateNotificationStatus(notification_id, has_read, callback) {
        callerName = "client_dashboard"
        var request = [
            "UpdateNotificationStatus", {
                "notification_id": notification_id,
                "has_read": has_read
            }
        ];
        clientApiRequest(callerName, request, callback);
    }

    /* Get Compliance List*/
    function getComplianceDetail(callback) {
        callerName = "client_user"
        var request = [
            "GetComplianceDetail", {

            }
        ];
        clientApiRequest(callerName, request, callback);
    }

    /* Risk Report */
    function getRiskReportFilters(callback) {
        var request = [
            "GetRiskReportFilters", {}
        ];
        callerName = "client_reports";
        clientApiRequest(callerName, request, callback);
    }

    function getRiskReport(
        country_id, domain_id, business_group_id, legal_entity_id, division_id, unit_id,
        level_1_statutory_name, statutory_status, callback
    ) {
        var request = [
            "GetRiskReport", {
                "country_id": country_id,
                "domain_id": domain_id,
                "business_group_id": business_group_id,
                "legal_entity_id": legal_entity_id,
                "division_id": division_id,
                "unit_id": unit_id,
                "level_1_statutory_name": level_1_statutory_name,
                "statutory_status": statutory_status
            }
        ];
        callerName = "client_reports";
        clientApiRequest(callerName, request, callback);
    }

    function updateComplianceDetail(compliance_history_id, documents, completion_date,
        validity_date, next_due_date, remarks, callback) {
        callerName = "client_user"
        console.log(validity_date);
        var request = [
            "UpdateComplianceDetail", {
                "compliance_history_id": compliance_history_id,
                "documents": documents,
                "completion_date": completion_date,
                "validity_date": validity_date,
                "next_due_date": next_due_date,
                "remarks": remarks
            }
        ];
        console.log(request);
        clientApiRequest(callerName, request, callback);
    }

    /*Statutory Notifications List*/
    function getStatutoryNotificationsListFilters(callback){
        callerName = "client_reports"
        var request = [
            "GetStatutoryNotificationsListFilters",
            {}
        ];
        clientApiRequest(callerName, request, callback);
    }

    function getStatutoryNotificationsListReport(countryName, domainName, businessGroupId,
        legalEntityId, divisionId, unitId, level1Id, fromdate, todate, callback){
        callerName = "client_reports"
        var request = [
            "GetStatutoryNotificationsListReport",
            {
                "country_name": countryName,
                "domain_name": domainName,
                "business_group_id": businessGroupId,
                "legal_entity_id": legalEntityId,
                "division_id": divisionId,
                "unit_id": unitId,
                "level_1_statutory_name": level1Id,
                "from_date": fromdate,
                "to_date": todate
            }
        ];
    }

    /* Reassigned History Report */
    function getReassignedHistoryReportFilters(callback) {
        var request = [
            "GetReassignedHistoryReportFilters", {}
        ];
        callerName = "client_reports";
        clientApiRequest(callerName, request, callback);
    }

    function getReassignedHistoryReport(country_id, domain_id, unit_id, level_1_statutory_id,
        compliance_id, user_id, from_date, to_date, callback) {
        var request = [
            "GetReassignedHistoryReport", {

                "country_id": country_id,
                "domain_id": domain_id,
                "unit_id": unit_id,
                "level_1_statutory_id": level_1_statutory_id,
                "compliance_id": compliance_id,
                "user_id": user_id,
                "from_date" : from_date,
                "to_date" : to_date
            }
        ];
        callerName = "client_reports";
        clientApiRequest(callerName, request, callback);
    }

    function getLoginTrace(callback){
        var request = [
            "GetLoginTrace",{}
        ];
        callerName = "client_reports";
        clientApiRequest(callerName, request, callback);
    }

    function getComplianceActivityReportFilters(callback){
        var request = [
            "GetComplianceActivityReportFilters",{}
        ];
        callerName = "client_reports";
        clientApiRequest(callerName, request, callback);
    }


    function getComplianceActivityReportData(
            user_type, user_id, country_id, domain_id, level_1_statutory_name, unit_id,
            compliance_id, from_date, to_date, callback
        ){
        var request = [
            "GetComplianceActivityReport",
            {
                "user_type": user_type,
                "user_id": user_id,
                "country_id" : country_id,
                "domain_id": domain_id,
                "level_1_statutory_name": level_1_statutory_name,
                "unit_id": unit_id,
                "compliance_id": compliance_id,
                "from_date" : from_date,
                "to_date" : to_date
            }
        ];
        callerName = "client_reports";
        clientApiRequest(callerName, request, callback);

    }
    // Client Details Report
    function getClientDetailsReportFilters(callback){
        var request = [
            "GetClientDetailsReportFilters",
            {}
        ];
        callerName = "client_reports"
        clientApiRequest(callerName, request, callback);
    }

    function getClientDetailsReportData(countryId, businessGroupId, legalEntityId, divisionId,
        unitId, domainIds, callback){
        callerName = "client_reports"
        var request = [
            "GetClientDetailsReportData",
            {
                "country_id": countryId,
                "business_group_id": businessGroupId,
                "legal_entity_id" : legalEntityId,
                "division_id" : divisionId,
                "unit_id": unitId,
                "domain_ids" : domainIds
            }
        ];
        clientApiRequest(callerName, request, callback);
    }

    function getAssigneewiseComplianesFilters(
        callback
    ){
        var request = [
            "GetAssigneewiseComplianesFilters",
            {}
        ];
        callerName = "client_dashboard";
        clientApiRequest(callerName, request, callback);

    }

    function getAssigneewiseComplianes(
        country_id, business_group_id, legal_entity_id, division_id,
        unit_id, user_id, callback
    ){
        var request = [
            "GetAssigneeWiseCompliancesChart",
            {
                "country_id": country_id,
                "business_group_id": business_group_id,
                "legal_entity_id": legal_entity_id,
                "division_id": division_id,
                "unit_id": unit_id
            }
        ];
        callerName = "client_dashboard";
        clientApiRequest(callerName, request, callback);

    }
    function getAssigneewiseCompliancesDrilldown(
        assignee_id, domain_id
    ){
        var request = [
            "GetAssigneeWiseComplianceDrillDown",
            {
                "assignee_id": assignee_id,
                "domain_id": domain_id
            }
        ];
        callerName = "client_dashboard";
        clientApiRequest(callerName, request, callback);
    }


    function getTaskApplicabilityReportFilters(callback) {
        var request = [
            "GetTaskApplicabilityStatusFilters", {}
        ];
        callerName = "client_reports";
        clientApiRequest(callerName, request, callback);
    }

    function getTaskApplicabilityReportData(
        country_id, domain_id, business_group_id,
        legal_entity_id, division_id, unit_id,
        statutory_name, applicable_status, callback
    ) {
        var request = [
            "GetComplianceTaskApplicabilityStatusReport", {
                "country_id" : country_id,
                "domain_id" : domain_id,
                "business_group_id": business_group_id,
                "legal_entity_id": legal_entity_id,
                "division_id": division_id,
                "unit_id": unit_id,
                "statutory_name": statutory_name,
                "applicable_status": applicable_status
            }
        ];
        callerName = "client_reports";
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
        getClientShortName: getClientShortName,

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
        getUpdateClientUserDict: getUpdateClientUserDict,
        updateClientUser: updateClientUser,
        changeClientUserStatus: changeClientUserStatus,
        changeAdminStatus: changeAdminStatus,

        getUnitClosureList: getUnitClosureList,
        closeUnit: closeUnit,

        getClientProfile: getClientProfile,
        getClientDetailsReportFilters: getClientDetailsReportFilters,
        getClientDetailsReport: getClientDetailsReport,
        getAuditTrail: getAuditTrail,

        getStatutorySettings: getStatutorySettings,
        updateStatutory: updateStatutory,
        updateStatutorySettings: updateStatutorySettings,

        getAssignComplianceFormData: getAssignComplianceFormData,
        getAssignComplianceForUnits: getAssignComplianceForUnits,
        statutoryDates: statutoryDates,
        assignCompliances: assignCompliances,
        saveAssignedComplianceFormData: saveAssignedComplianceFormData,

        getPastRecordsFormData: getPastRecordsFormData,
        getStatutoriesByUnit: getStatutoriesByUnit,
        getPastRecordsComplianceDict : getPastRecordsComplianceDict,
        savePastRecords : savePastRecords,

        getClientReportFilters: getClientReportFilters,
        getUnitwisecomplianceReport: getUnitwisecomplianceReport,
        getAssigneewisecomplianceReport: getAssigneewisecomplianceReport,

        getServiceProviderReportFilters: getServiceProviderReportFilters,
        getServiceProviderWiseCompliance: getServiceProviderWiseCompliance,

        getComplianceDetailsReportFilters: getComplianceDetailsReportFilters,
        getComplianceDetailsReport: getComplianceDetailsReport,

        getComplianceApprovalList: getComplianceApprovalList,
        approveCompliance: approveCompliance,

        getChartFilters: getChartFilters,
        getComplianceStatusChartData: getComplianceStatusChartData,
        getComplianceStatusDrillDown: getComplianceStatusDrillDown,
        getEscalationChartData: getEscalationChartData,
        getTrendChart: getTrendChart,
        getTrendChartDrillDown: getTrendChartDrillDown,

        getSettings: getSettings,
        updateSettings: updateSettings,
        getNotifications: getNotifications,
        updateNotificationStatus: updateNotificationStatus,

        getComplianceDetail: getComplianceDetail,

        getRiskReportFilters: getRiskReportFilters,
        getRiskReport: getRiskReport,

        getReassignedHistoryReportFilters: getReassignedHistoryReportFilters,
        getReassignedHistoryReport: getReassignedHistoryReport,

        updateComplianceDetail: updateComplianceDetail,

        getLoginTrace: getLoginTrace,

        uploadFile: uploadFile,
        uploadFileFormat: uploadFileFormat,

        getComplianceActivityReportFilters: getComplianceActivityReportFilters,
        getComplianceActivityReportData: getComplianceActivityReportData,

        getClientDetailsReportFilters: getClientDetailsReportFilters,
        getClientDetailsReportData: getClientDetailsReportData,

        getAssigneewiseComplianesFilters: getAssigneewiseComplianesFilters,
        getAssigneewiseComplianes: getAssigneewiseComplianes,
        getAssigneewiseCompliancesDrilldown: getAssigneewiseCompliancesDrilldown,

        getTaskApplicabilityReportFilters: getTaskApplicabilityReportFilters,
        getTaskApplicabilityReportData: getTaskApplicabilityReportData
    }
}
var client_mirror = initClientMirror();
