// var CLIENT_BASE_URL = "http://localhost:8080/";
var CLIENT_BASE_URL = "/api/";
var my_ip = null;

function initClientMirror() {
    var DEBUG = true;

    // if (window.localStorage["my_ip"] == null){
    //     get_ip();
    // }

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

    function get_ip(){
        $.getJSON("http://jsonip.com?callback=?", function (data) {
            window.localStorage["my_ip"] = data.ip;
        });
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
        if (info != null){
            return info["menu"]["menus"];
        }else{
            login_url = "/login/"+window.localStorage["recent_short_name"]
            window.location.href = login_url;
        }
    }

    function getClientId() {
        var info = getUserInfo();
        // console.log(info)
        return info["client_id"];
    }

    function getClientShortName(){
        var name = window.localStorage["shortName"];
        if (typeof(name) == "undefined"){
            return null;
        }
        return name;
    }

    function redirect_login(){
        var short_name = getClientShortName();
        login_url = "/login/" + short_name;
        console.log(login_url);
        window.localStorage["recent_short_name"] = short_name;
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
                log("API STATUS :" + status);
                console.log(response)
                console.log(status.toLowerCase().indexOf(matchString))
                callback(null, response)

                if (status.toLowerCase().indexOf(matchString) != -1) {
                    callback(error=null, response);
                }
                else if (status == "InvalidSessionToken") {
                    // console.log(status)
                    redirect_login()
                }
                else {
                    if (status == "SavePastRecordsFailed"){
                        callback(data, null);
                    }else{
                        callback(status, null);
                    }

                }

            }
        )
            .fail(
                function(jqXHR, textStatus, errorThrown) {
                    // alert("jqXHR:"+jqXHR.status);
                    // alert("textStatus:"+textStatus);
                    // alert("errorThrown:"+errorThrown);
                    if (errorThrown == "Not Found"){
                        alert("Server connection not found");
                        redirect_login();
                    }
                    else
                        callback(jqXHR["responseText"], errorThrown)
                }
        );
    }

    // Login function
    function login(username, password, short_name, callback) {
        if (window.localStorage["my_ip"] == null)
            get_ip();
        var request = [
            short_name, [
                "Login", {
                    "login_type": "Web",
                    "username": username,
                    "password": password,
                    "short_name": short_name,
                    "ip": window.localStorage["my_ip"]
                }
            ]
        ]
        jQuery.post(
            CLIENT_BASE_URL + "login",
            toJSON(request),
            function(data) {
                console.log("data:"+data);
                var data = parseJSON(data);
                var status = data[0];
                var response = data[1];
                matchString = 'success';
                if (status.toLowerCase().indexOf(matchString) != -1) {
                    console.log("status success");
                    console.log(data);
                    initSession(response, short_name)
                    callback(null, response);
                }
                else {
                    callback(status, null);
                }
            }
        ).fail(function(jqXHR, textStatus, errorThrown){
            if(jqXHR.status == 404) {
                callback("Client Database not exists")
            }
        });
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

    function changePassword(currentPassword, newPassword,callback) {
        callerName = "login"
        var sessionToken = getSessionToken();
        var client_id = getClientId()
        var request =  [
            sessionToken,
            [
                "ChangePassword", {
                    "session_token": client_id + "-" + sessionToken,
                    "current_password": currentPassword,
                    "new_password": newPassword
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
                if (status.toLowerCase().indexOf(matchString) != -1) {
                    callback(null, response);

                }
                else {
                    callback(status, null);
                }
            }
        )

    }

    // Forgot Password APIs

    function forgotPassword(username, callback) {
        callerName = "login"
        var short_name = getShortName();
        window.localStorage["recent_short_name"] = short_name
        login_url = "/login/"+short_name
        var request = [
            short_name, [
                "ForgotPassword", {
                    "username": username,
                    "short_name" : short_name
                }
            ]
        ];
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
                    // initSession(response, short_name)
                    callback(null, response);

                }
                else {
                    callback(status, null);
                }
            }
        )
    }

    function validateResetToken(resetToken, short_name,
        callback) {
        window.localStorage["recent_short_name"] = short_name
        login_url = "/login/"+short_name
        callerName = "login"
        var request = [
            short_name, [
                "ResetTokenValidation", {
                    "reset_token": resetToken,
                    "short_name": short_name
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
                    // initSession(response, short_name)
                    callback(null, response);

                }
                else {
                    callback(status, null);
                }
            }
        )

    }

    function resetPassword(resetToken, newPassword, short_name,
        callback) {
        window.localStorage["recent_short_name"] = short_name
        login_url = "/login/"+short_name
        callerName = "login"
        var request = [
            short_name, [
                "ResetPassword", {
                    "reset_token": resetToken,
                    "new_password": newPassword,
                    "short_name": short_name
                }
            ]
        ];
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
                    // initSession(response, short_name)
                    callback(null, response);

                }
                else {
                    callback(status, null);
                }
            }
        )
    }

    // Client User Group
    function getClientUserGroups(callback) {
        callerName = "client_masters"
        var request = [
            "GetUserPrivileges", {}
        ];
        clientApiRequest(callerName, request, callback);
    }

    function getSaveClientUserGroupDict(ugName, fIds) {
        return {
            "ug_name": ugName,
            "f_ids": fIds
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

    function getUpdateClientUserGroupDict(ugId, ugName, fIds) {
        return {
            "ug_id": ugId,
            "ug_name": ugName,
            "f_ids": fIds
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

    function changeClientUserGroupStatus(ugId, active,
        callback) {
        callerName = "client_masters"
        var request = [
            "ChangeUserPrivilegeStatus", {
                "ug_id": ugId,
                "active": active
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
        add = serviceProviderDetail[1]
        if (add  == ""){
            add = null;
        }
        console.log(add)
        result = {
            "s_name": serviceProviderDetail[0],
            "add": add,
            "c_from": serviceProviderDetail[2],
            "c_to": serviceProviderDetail[3],
            "c_person": serviceProviderDetail[4],
            "c_no": serviceProviderDetail[5]
        }
        console.log(result)
        return result
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
        add = serviceProviderDetail[2]
        if (add  == ""){
            add = null;
        }
        return {
            "s_id": serviceProviderDetail[0],
            "s_name": serviceProviderDetail[1],
            "add": add,
            "c_from": serviceProviderDetail[3],
            "c_to": serviceProviderDetail[4],
            "c_person": serviceProviderDetail[5],
            "c_no": serviceProviderDetail[6]
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

    function changeServiceProviderStatus(sId,
        active, callback) {
        callerName = "client_masters"
        var request = [
            "ChangeServiceProviderStatus", {
                "s_id": sId,
                "active": active
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
            "email": clientUserDetail[0],
            "ug_id": clientUserDetail[1],
            "emp_n": clientUserDetail[2],
            "emp_c": clientUserDetail[3],
            "cn": clientUserDetail[4],
            "s_u_id": clientUserDetail[5],
            "ul": clientUserDetail[6],
            "c_ids": clientUserDetail[7],
            "d_ids": clientUserDetail[8],
            "u_ids": clientUserDetail[9],
            "admin": clientUserDetail[10],
            "sp": clientUserDetail[11],
            "sp_id": clientUserDetail[12]
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
        console.log("clientUserDetail[0]"+clientUserDetail[0]);
        result =  {
            "u_id": clientUserDetail[0],
            "ug_id": clientUserDetail[1],
            "emp_n": clientUserDetail[2],
            "emp_c": clientUserDetail[3],
            "cn": clientUserDetail[4],
            "s_u_id": clientUserDetail[5],
            "ul": clientUserDetail[6],
            "c_ids": clientUserDetail[7],
            "d_ids": clientUserDetail[8],
            "u_ids": clientUserDetail[9],
            "admin": clientUserDetail[10],
            "sp": clientUserDetail[11],
            "sp_id": clientUserDetail[12]
        }
        return result
    }

    function updateClientUser(clientUserDetail, callback) {
        callerName = "client_masters"
        var request = [
            "UpdateClientUser",
            clientUserDetail
        ];
        clientApiRequest(callerName, request, callback);
    }

    function changeClientUserStatus(uId, active, callback) {
        callerName = "client_masters"
        var request = [
            "ChangeClientUserStatus", {
                "u_id": uId,
                "active": active
            }
        ];
        clientApiRequest(callerName, request, callback);
    }

    function changeAdminStatus(uId, admin, callback) {
        callerName = "client_masters"
        var request = [
            "ChangeAdminStatus", {
                "u_id": uId,
                "admin": admin
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

    function closeUnit(uId, pwd, callback,
        failure_callback) {
        callerName = "client_masters"
        var request = [
            "CloseUnit", {
                "u_id": uId,
                "pwd": pwd
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
        unitId, domainIds, csv, callback) {
        callerName = "techno"
        var request = [
            "GetClientDetailsReport", {
                "country_id": countryId,
                "group_id": clientId,
                "business_group_id": businessGroupId,
                "legal_entity_id": legalEntityId,
                "division_id": divisionId,
                "unit_id": unitId,
                "domain_ids": domainIds,
                "csv": csv
            }
        ];
        clientApiRequest(callerName, request, callback);
    }


    function getAuditTrail(fromDate, toDate, userId, formId, recordCount, callback) {
        callerName = "client_masters"
        var request = [
            "GetAuditTrails", {
                "from_date": fromDate,
                "to_date": toDate,
                "user_id": userId,
                "form_id": formId,
                "record_count": recordCount
            }
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

    function getStatutorySettingsCompliance(unitId, recordCount, callback) {
        callerName = "client_transaction";
        var request = [
            "GetSettingsCompliances", {
                "unit_id": unitId,
                "record_count": recordCount
            }
        ]
        clientApiRequest(callerName, request, callback);
    }


    function updateStatutory(clientSId, clientCId, aStatus, aRemarks, compId, oStatus, remarks) {
        return {
            "c_s_id": clientSId,
            "c_c_id": clientCId,
            "a_status": aStatus,
            "n_a_remarks": aRemarks,
            "comp_id": compId,
            "c_o_status": oStatus,
            "c_remarks": remarks
        };
    }

    function updateStatutorySettings(password, uName, uId, statutories, callback) {
        var request = [
            "UpdateStatutorySettings", {
                "password": password,
                "u_name": uName,
                "u_id": uId,
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

    function getAssignComplianceForUnits(unitIds, domainId, recordCount, callback) {
        var request = [
            "GetComplianceForUnits", {
                "u_ids": unitIds,
                "d_id": domainId,
                "record_count": recordCount
            }
        ];
        var callerName = "client_transaction";
        clientApiRequest(callerName, request, callback);
    }

    function statutoryDates(date, month, triggerBefore, repeatBy) {
        var statutoryDate = {};
        statutoryDate["statutory_date"] = date;
        statutoryDate["statutory_month"] = month;
        statutoryDate["trigger_before_days"] = triggerBefore;
        statutoryDate["repeat_by"] = repeatBy;
        return statutoryDate;
    }

    function assignCompliances(compId, compName, sDateList, dDate, vDate, trigBefore, uIds) {
        return {
            "comp_id": compId,
            "comp_name": compName,
            "statu_dates": sDateList,
            "d_date": dDate,
            "v_date": vDate,
            "trig_before": trigBefore,
            "u_ids": uIds
        }
    }

    function newUnitSettings(userId, uIds, dId, cId) {
        return {
            "user_id": userId,
            "u_ids": uIds,
            "d_id": dId,
            "c_id": cId
        }
    }

    function saveAssignedComplianceFormData(
        cId, assignee, aName,
        concurrence, conName,
        approval, appName,
        compliances, newUnits, callback
    ) {
        var request = [
            "SaveAssignedCompliance", {
                "c_id": cId,
                "assignee": assignee,
                "a_name": aName,
                "con_person": concurrence,
                "con_person_name": conName,
                "a_person": approval,
                "a_person_name": appName,
                "compliances": compliances,
                "n_units" : newUnits
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
        compliance_frequency, country_id, callback) {
        var request = [
            "GetStatutoriesByUnit", {
                "unit_id": unit_id,
                "domain_id": domain_id,
                "level_1_statutory_name": level_1_statutory_name,
                "compliance_frequency": compliance_frequency,
                "country_id": country_id
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
            console.log("file.size : "+file.size);
            console.log("max_limit : "+max_limit);
            if (file_size > max_limit) {
                callback("File max limit exceeded");
                return;
            }
            else{
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

    }

    /* Compliance Approal */

    function getComplianceApprovalList(start_count, callback) {
        var request = [
            "GetComplianceApprovalList",
            {
                "start_count": start_count
            }
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
        division_id, unit_id, user_id, record_count, callback
    ) {
        var request = [
            "GetUnitwisecomplianceReport", {
                "country_id": country_id,
                "domain_id": domain_id,
                "business_group_id": business_group_id,
                "legal_entity_id": legal_entity_id,
                "division_id": division_id,
                "unit_id": unit_id,
                "user_id": user_id,
                "record_count": record_count
            }
        ];
        callerName = "client_reports";
        clientApiRequest(callerName, request, callback);
    }

    function getAssigneewisecomplianceReport(
        country_id, domain_id, business_group_id, legal_entity_id,
        division_id, unit_id, user_id, record_count, callback
    ) {
        var request = [
            "GetAssigneewisecomplianceReport", {
                "country_id": country_id,
                "domain_id": domain_id,
                "business_group_id": business_group_id,
                "legal_entity_id": legal_entity_id,
                "division_id": division_id,
                "unit_id": unit_id,
                "user_id": user_id,
                "record_count": record_count
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

    function getEscalationDrillDown(requestData, callback) {
        var request = [
            "GetEscalationsDrillDownData",
            requestData
        ];
        var callerName =  "client_dashboard";
        clientApiRequest(callerName, request, callback);
    }

    function getServiceProviderReportFilters(callback) {
        var request = [
            "GetServiceProviderReportFilters", {}
        ];
        callerName = "client_reports";
        clientApiRequest(callerName, request, callback);
    }

    function getServiceProviderWiseCompliance(
        country_id, domain_id, statutory_id, unit_id, service_provider_id, csv, callback) {
        var request = [
            "GetServiceProviderWiseCompliance", {
                "country_id": country_id,
                "domain_id": domain_id,
                "statutory_id": statutory_id,
                "unit_id": unit_id,
                "service_provider_id": service_provider_id,
                "csv": csv
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


    function getComplianceDetailsReport(
        country_id, domain_id, statutory_id, unit_id, compliance_id, assignee_id, from_date, to_date,
        compliance_status, csv, record_count, callback
    ) {
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
                "compliance_status": compliance_status,
                "csv" : csv,
                "record_count": record_count
            }
        ];
        callerName = "client_reports";
        clientApiRequest(callerName, request, callback);
    }

    /* Trend Chart */

    function getTrendChart(requestData, callback) {
        var request = [
            "GetTrendChart",
            requestData
        ];
        var callerName = "client_dashboard"
        clientApiRequest(callerName, request, callback)
    }

    function getTrendChartDrillDown(requestData, callback) {
        var request = [
            "GetTrendChartDrillDownData",
            requestData
        ];
        var callerName = "client_dashboard"
        clientApiRequest(callerName, request, callback)
    }

    function getNotCompliedData(requestData, callback) {
        var request = [
            "GetNotCompliedChart",
            requestData
        ];
        var callerName = "client_dashboard";
        clientApiRequest(callerName, request, callback);
    }

    function getNotCompliedDrillDown(requestData, callback) {
        var request = [
            "GetNotCompliedDrillDown",
            requestData
        ];
        var callerName = "client_dashboard";
        clientApiRequest(callerName, request, callback);
    }

    function getComplianceApplicabilityChart(requestData, callback) {
        var request = [
            "GetComplianceApplicabilityStatusChart",
            requestData
        ];
        var callerName = "client_dashboard";
        clientApiRequest(callerName, request, callback);
    }

    function getComplianceApplicabilityDrillDown(requestData, callback) {
        var request = [
            "GetComplianceApplicabilityStatusDrillDown",
            requestData
        ];
        var callerName = "client_dashboard";
        clientApiRequest(callerName, request, callback);
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
    function getCurrentComplianceDetail(current_start_count, callback) {
        callerName = "client_user"
        var request = [
            "GetCurrentComplianceDetail", {
                "current_start_count": current_start_count,
            }
        ];
        clientApiRequest(callerName, request, callback);
    }

    function getUpcomingComplianceDetail(upcoming_start_count, callback) {
        callerName = "client_user"
        var request = [
            "GetUpcomingComplianceDetail", {
                "upcoming_start_count": upcoming_start_count
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
        level_1_statutory_name, statutory_status, csv, callback
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
                "statutory_status": statutory_status,
                "csv" : csv
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
        legalEntityId, divisionId, unitId, level1Id, fromdate, todate, csv, callback){
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
                "to_date": todate,
                "csv": csv
            }
        ];
        clientApiRequest(callerName, request, callback);
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
        compliance_id, user_id, from_date, to_date, csv, record_count, callback) {
        var request = [
            "GetReassignedHistoryReport", {

                "country_id": country_id,
                "domain_id": domain_id,
                "unit_id": unit_id,
                "level_1_statutory_id": level_1_statutory_id,
                "compliance_id": compliance_id,
                "user_id": user_id,
                "from_date" : from_date,
                "to_date" : to_date,
                "csv": csv,
                "record_count" : record_count
            }
        ];
        callerName = "client_reports";
        clientApiRequest(callerName, request, callback);
    }

    function getLoginTrace(record_count, callback){
        var request = [
            "GetLoginTrace",{
                "record_count" : record_count
            }
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
            compliance_id, from_date, to_date, csv, callback
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
                "to_date" : to_date,
                "csv" : csv
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
        unitId, domainIds, csv, callback){
        callerName = "client_reports"
        var request = [
            "GetClientDetailsReportData",
            {
                "country_id": countryId,
                "business_group_id": businessGroupId,
                "legal_entity_id" : legalEntityId,
                "division_id" : divisionId,
                "unit_id": unitId,
                "domain_ids" : domainIds,
                "csv": csv
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
                "unit_id": unit_id,
                "user_id" : user_id
            }
        ];
        console.log(request);
        callerName = "client_dashboard";
        clientApiRequest(callerName, request, callback);

    }
    function getAssigneewiseCompliancesDrilldown(
        assignee_id, domain_id, year, callback
    ){
        var request = [
            "GetAssigneeWiseComplianceDrillDown",
            {
                "assignee_id": assignee_id,
                "domain_id": domain_id,
                "year" : year
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
        statutory_name, applicable_status, csv, callback
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
                "applicable_status": applicable_status,
                "record_count":0,
                "csv": csv,
            }
        ];
        callerName = "client_reports";
        clientApiRequest(callerName, request, callback);
    }

    function getOnOccurrenceCompliances(callback){
        var request = [
            "GetOnOccurrenceCompliances", {}
        ];
        callerName = "client_user";
        clientApiRequest(callerName, request, callback);
    }

    function startOnOccurrenceCompliance(
        compliance_id, start_date, unit_id, duration, callback
    ){
        var request = [
            "StartOnOccurrenceCompliance",
            {
                "compliance_id": compliance_id,
                "start_date": start_date,
                "unit_id": unit_id,
                "duration": duration
            }
        ];
        callerName = "client_user";
        clientApiRequest(callerName, request, callback);
    }
    function exportToCSV(jsonResponse, callback){
        var request = [
            "ExportToCSV",
            {
                "data":jsonResponse
            }
        ];
        callerName = "client_reports";
        clientApiRequest(callerName, request, callback);
    }

    function getUserwiseCompliances(callback){
        var request = [
            "GetUserwiseCompliances", {}
        ];
        callerName = "client_transaction";
        clientApiRequest(callerName, request, callback);
    }

    function checkContractExpiration(callback){
        var request = [
            "CheckContractExpiration", {}
        ];
        callerName = "client_dashboard";
        clientApiRequest(callerName, request, callback);
    }

    function getAssigneeWiseCompliances(assignee, record_count, callback) {
        var request = [
            "GetAssigneeCompliances", {
                "assignee": assignee,
                "record_count": record_count
            }
        ];
        callerName = "client_transaction";
        clientApiRequest(callerName, request, callback);
    }

    function reassignComplianceDet(uID, cID, cNAME, cHistoryId, dDate) {
        return {
            "u_id": uID,
            "c_id": cID,
            "c_name": cNAME,
            "c_history_id": cHistoryId,
            "d_date": dDate
        }
    }

    function saveReassignCompliance(
        rFrom, rTo, aName, cPerson, aPerson,
        cList, reason, callback
    ) {
        request = [
            "ReassignCompliance",
            {
                "r_from": rFrom,
                "assignee": rTo,
                "a_name": aName,
                "c_person": cPerson,
                "a_person": aPerson,
                "compliances": cList,
                "r_reason": reason
            }
        ];
        callerName = "client_transaction";
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
        redirect_login : redirect_login,

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
        getStatutorySettingsCompliance: getStatutorySettingsCompliance,
        updateStatutory: updateStatutory,
        updateStatutorySettings: updateStatutorySettings,

        getAssignComplianceFormData: getAssignComplianceFormData,
        getAssignComplianceForUnits: getAssignComplianceForUnits,
        statutoryDates: statutoryDates,
        assignCompliances: assignCompliances,
        newUnitSettings: newUnitSettings,
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
        getEscalationDrillDown: getEscalationDrillDown,

        getTrendChart: getTrendChart,
        getTrendChartDrillDown: getTrendChartDrillDown,
        getNotCompliedData: getNotCompliedData,
        getNotCompliedDrillDown: getNotCompliedDrillDown,
        getComplianceApplicabilityChart: getComplianceApplicabilityChart,
        getComplianceApplicabilityDrillDown: getComplianceApplicabilityDrillDown,

        getSettings: getSettings,
        updateSettings: updateSettings,
        getNotifications: getNotifications,
        updateNotificationStatus: updateNotificationStatus,

        getCurrentComplianceDetail: getCurrentComplianceDetail,
        getUpcomingComplianceDetail: getUpcomingComplianceDetail,

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

        getStatutoryNotificationsListFilters: getStatutoryNotificationsListFilters,
        getStatutoryNotificationsListReport: getStatutoryNotificationsListReport,

        getAssigneewiseComplianesFilters: getAssigneewiseComplianesFilters,
        getAssigneewiseComplianes: getAssigneewiseComplianes,
        getAssigneewiseCompliancesDrilldown: getAssigneewiseCompliancesDrilldown,

        getTaskApplicabilityReportFilters: getTaskApplicabilityReportFilters,
        getTaskApplicabilityReportData: getTaskApplicabilityReportData,

        getOnOccurrenceCompliances: getOnOccurrenceCompliances,
        startOnOccurrenceCompliance: startOnOccurrenceCompliance,
        getUserwiseCompliances: getUserwiseCompliances,
        exportToCSV: exportToCSV,
        get_ip: get_ip,
        checkContractExpiration: checkContractExpiration,
        saveReassignCompliance : saveReassignCompliance,
        reassignComplianceDet : reassignComplianceDet,
        getAssigneeWiseCompliances: getAssigneeWiseCompliances,
    }
}
var client_mirror = initClientMirror();
