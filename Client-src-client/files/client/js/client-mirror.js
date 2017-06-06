var CLIENT_BASE_URL = '/api/';
var my_ip = null;

var DEBUG = true;
// if (window.sessionStorage["my_ip"] == null){
//     get_ip();
// }
function log() {
    if (window.console) {
        console.log.apply(console, arguments);
    }
}

function toJSON(data) {
    return JSON.stringify(data, null, ' ');
}

function parseJSON(data) {
    if (data == undefined)
        return data;
    else
        return JSON.parse(data);
}

function initSession(userProfile, shortName) {
    // console.log(toJSON(userProfile))
    window.sessionStorage.userInfo = userProfile;
    window.localStorage.shortName = shortName;
}

function getShortName() {
    var pathArray = window.location.pathname.split('/');
    if (typeof pathArray[2] === 'undefined') {
        return null;
    } else {
        return pathArray[2];
    }
}
// function updateUser_Session(user) {
//     var info = parseJSON(window.sessionStorage["userInfo"])
//     delete window.sessionStorage["userInfo"];
//     info.userProfile = user;
//     window.sessionStorage["userInfo"] = toJSON(info);
// }
function clearSession() {
    // delete window.sessionStorage.userInfo;
    delete window.localStorage.shortName;
    delete window.sessionStorage.CLIENT_NOTIFICATION_COUNT;
    delete window.sessionStorage.CLIENT_REMINDER_COUNT;
    delete window.sessionStorage.CLIENT_ESCALATION_COUNT;
    delete window.sessionStorage.selectedEntity;
    delete window.sessionStorage.selectedEntityName;
}

function getUserInfo() {
    var info = window.sessionStorage.userInfo;
    user = parseJSON(info);
    return user;
}

function getSelectedLegalEntity() {
    var info = parseJSON(window.sessionStorage.selectedEntity);
    return info;
}

function getLEids() {
    le_ids = []
    le_data = getSelectedLegalEntity();
    $.each(le_data, function(i, v) {
        le_ids.push(v.le_id);
    });
    return le_ids;
}

function updateUserInfo(response) {
    var info = getUserInfo();
    info.contact_no = response.contact_no;
    info.address = response.address;
    window.sessionStorage.userInfo = toJSON(info);
}

function get_ip() {
    $.getJSON('http://jsonip.com?callback=?', function(data) {
        window.sessionStorage.my_ip = data.ip;
    });
}

function getEmployeeName() {
    var info = getUserInfo();
    if (info !== null)
        return info.employee_name;
    else
        return null;
}

function getUserCountry() {
    var info = getUserInfo();
    return info.country_info;

}

function getUserBusinessGroup() {
    var info = getUserInfo();
    return info.entity_info;
}

function getUserLegalEntity() {
    var info = getUserInfo();
    return info.entity_info;
}

function getUserCategoryID() {
    var info = getUserInfo();
    return info.usr_cat_id;
}

function getUserProfile() {
    var info = getUserInfo();
    var userDetails = {
        'user_id': info.user_id,
        'client_id': info.client_id,
        'user_group': info.user_group,
        'employee_name': info.employee_name,
        'employee_code': info.employee_code,
        'email_id': info.email_id,
        'contact_no': info.contact_no,
        'address': info.address,
        'designation': info.designation
    };
    return userDetails;
}

function getSessionToken() {
    var info = getUserInfo();
    return info.session_token;
}

function getUserMenu() {
    var info = getUserInfo();
    if (info != null) {
        return info.menu;
    } else {
        window.location.href = "/login";
    }
}

function getPageUrl() {
    ac_menu = getUserMenu();
    keys = Object.keys(ac_menu);
    page_urls = [];
    for (var k = 0; k < keys.length; k++) {
        key = keys[k];
        objs = ac_menu[key];
        for (var ob = 0; ob < objs.length; ob++) {
            data = objs[ob];
            page_urls.push(data.form_url);
        }
    }
    page_urls.push('/dashboard');
    page_urls.push('/reminders');
    page_urls.push('/notifications');
    page_urls.push('/escalations');
    page_urls.push('/change-password');
    page_urls.push('/settings');
    page_urls.push('/profile');
    page_urls.push('/home');
    return page_urls;
}

function getClientId() {
    var info = getUserInfo();
    return info.client_id;
}

function getClientShortName() {
    var name = window.localStorage.shortName;
    if (typeof name == 'undefined') {
        l_name = window.localStorage.recent_short_name;
        return l_name;
    }
    return name;
}

function redirect_login() {
    var short_name = getClientShortName();
    login_url = '/login';
    window.localStorage.recent_short_name = short_name;
    clearSession();
    window.location.href = login_url;
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

function makekey() {
    var text = "";
    var possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
    for (var i = 0; i < 5; i++)
        text += possible.charAt(Math.floor(Math.random() * possible.length));
    return text;
}

function clientApiRequest(callerName, request, callback) {
    var sessionToken = getSessionToken();
    var requestFrame = {
        'session_token': sessionToken,
        'request': request
    };
    var body = [
        sessionToken,
        requestFrame
    ];
    actula_data = toJSON(body);
    $.ajax({
        url: CLIENT_BASE_URL + callerName,
        headers: { 'X-Xsrftoken': getCookie('_xsrf'), 'Caller-Name': window.location.pathname },
        type: 'POST',
        contentType: 'application/json',
        data: makekey() + btoa(actula_data),
        success: function(data) {
            // console.log(data);
            data = atob(data.substring(5));
            data = parseJSON(data);
            var status = data[0];
            var response = data[1];
            matchString = 'success';
            log('API STATUS :' + status);
            ///callback(null, response)
            if (status.toLowerCase().indexOf(matchString) != -1) {
                callback(null, response);
            } else if (status == 'InvalidSessionToken') {
                confirm_ok_alert(message[status], "/login");
            } else {
                if (status == 'SavePastRecordsFailed') {
                    callback(data, null);
                } else {
                    callback(status, response);
                }
            }
        },
        error: function(jqXHR, textStatus, errorThrown) {
            rdata = parseJSON(jqXHR.responseText);
            rdata = atob(rdata.substring(5));
            callback(rdata, errorThrown);
        }
    });
}

function LoginApiRequest(callerName, request, callback) {
    actula_data = toJSON(request);
    $.ajax({
        url: CLIENT_BASE_URL + callerName,

        type: 'POST',
        contentType: 'application/json',
        data: makekey() + btoa(actula_data),
        success: function(data) {
            // var data = parseJSON(data);
            data = atob(data.substring(5));
            data = parseJSON(data);
            var status = data[0];
            var response = data[1];
            matchString = 'success';
            log('API STATUS :' + status);
            if (status.toLowerCase().indexOf(matchString) != -1) {
                callback(null, response);
            } else {
                callback(status, null);
            }
        },
        error: function(jqXHR, textStatus, errorThrown) {
            rdata = parseJSON(jqXHR.responseText);
            rdata = atob(rdata.substring(5));
            callback(rdata, null);
        }
    });
}

function updateUserProfile(contact_no, address, callback) {
    var request = [
        sessionToken = getSessionToken(), [
            'UpdateUserProfile', {
                'contact_no': contact_no,
                'address': address,
                'session_token': sessionToken
            }
        ]
    ];
    LoginApiRequest('login', request, function(status, response) {
        if (status == null) {
            updateUserInfo(response);
            callback(null, response);
        } else {
            callback(status, null);
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
    sessionToken = getSessionToken();
    var request = [
        sessionToken, [
            'Logout',
            { 'session_token': sessionToken }
        ]
    ];
    LoginApiRequest('login', request, function(status, response) {
        redirect_login();
    });
}
// Change Password APIs
function changePassword(currentPassword, newPassword, callback) {
    callerName = 'login';
    var sessionToken = getSessionToken();
    var client_id = getClientId();
    var request = [
        sessionToken, [
            'ChangePassword', {
                'session_token': client_id + '-' + sessionToken,
                'current_password': currentPassword,
                'new_password': newPassword
            }
        ]
    ];
    LoginApiRequest('login', request, callback);
}
// Forgot Password APIs
function forgotPassword(username, callback) {
    callerName = 'login';
    var short_name = getShortName();
    window.localStorage.recent_short_name = short_name;
    login_url = '/login/' + short_name;
    var request = [
        short_name, [
            'ForgotPassword', {
                'username': username,
                'short_name': short_name
            }
        ]
    ];
    LoginApiRequest('login', request, callback);
}

function validateResetToken(resetToken, short_name, callback) {
    window.localStorage.recent_short_name = short_name;
    login_url = '/login/' + short_name;
    callerName = 'login';
    var request = [
        short_name, [
            'ResetTokenValidation', {
                'reset_token': resetToken,
                'short_name': short_name
            }
        ]
    ];
    LoginApiRequest('login', request, callback);
}

function resetPassword(resetToken, newPassword, short_name, callback) {
    window.localStorage.recent_short_name = short_name;
    login_url = '/login/' + short_name;
    callerName = 'login';
    var request = [
        short_name, [
            'ResetPassword', {
                'reset_token': resetToken,
                'new_password': newPassword,
                'short_name': short_name
            }
        ]
    ];
    LoginApiRequest('login', request, callback);
}

//Verify Password
function verifyPassword(password, callback) {
    var request = [
        'VerifyPassword', {
            'password': password
        }
    ];
    apiRequest('general', request, callback);
}

/* Compliance Approval */
function getComplianceApprovalList(le_id, unit_id, start_count, callback) {
    var request = [
        'GetComplianceApprovalList', {
            'le_id': le_id,
            'unit_id': unit_id,
            'start_count': start_count
        }
    ];
    clientApiRequest('client_transaction', request, callback);
}

/* Have Compliances */
function haveCompliances(le_id, user_id, callback) {
    var request = [
        'HaveCompliances', {
            'le_id': le_id,
            'user_id': user_id
        }
    ];
    clientApiRequest('client_transaction', request, callback);
}

function approveCompliance(le_id, compliance_history_id, compliance_approval_status, remarks, next_due_date, validity_date, callback) {
    var request = [
        'ApproveCompliance', {
            'le_id': le_id,
            'compliance_history_id': compliance_history_id,
            'approval_status': compliance_approval_status,
            'remarks': remarks,
            'next_due_date': next_due_date,
            'validity_date': validity_date
        }
    ];
    callerName = 'client_transaction';
    clientApiRequest(callerName, request, callback);
}

function getChartFilters(le_ids, callback) {
    var request = [
        'GetChartFilters', {
            'le_ids': le_ids
        }
    ];
    var callerName = 'client_master_filters';
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
        'GetComplianceStatusChart',
        requestData
    ];
    var callerName = 'client_dashboard';
    clientApiRequest(callerName, request, callback);
}

function getComplianceStatusDrillDown(requestData, callback) {
    var request = [
        'GetComplianceStatusDrillDownData',
        requestData
    ];
    var callerName = 'client_dashboard';
    clientApiRequest(callerName, request, callback);
}

function getEscalationChartData(requestData, callback) {
    var request = [
        'GetEscalationsChart',
        requestData
    ];
    var callerName = 'client_dashboard';
    clientApiRequest(callerName, request, callback);
}

function getEscalationDrillDown(requestData, callback) {
    var request = [
        'GetEscalationsDrillDownData',
        requestData
    ];
    var callerName = 'client_dashboard';
    clientApiRequest(callerName, request, callback);
}

/* Trend Chart */
function getTrendChart(requestData, callback) {
    var request = [
        'GetTrendChart',
        requestData
    ];
    var callerName = 'client_dashboard';
    clientApiRequest(callerName, request, callback);
}

function getTrendChartDrillDown(requestData, callback) {
    var request = [
        'GetTrendChartDrillDownData',
        requestData
    ];
    var callerName = 'client_dashboard';
    clientApiRequest(callerName, request, callback);
}

function getNotCompliedData(requestData, callback) {
    var request = [
        'GetNotCompliedChart',
        requestData
    ];
    var callerName = 'client_dashboard';
    clientApiRequest(callerName, request, callback);
}

function getNotCompliedDrillDown(requestData, callback) {
    var request = [
        'GetNotCompliedDrillDown',
        requestData
    ];
    var callerName = 'client_dashboard';
    clientApiRequest(callerName, request, callback);
}

function getComplianceApplicabilityChart(requestData, callback) {
    var request = [
        'GetComplianceApplicabilityStatusChart',
        requestData
    ];
    var callerName = 'client_dashboard';
    clientApiRequest(callerName, request, callback);
}

function getComplianceApplicabilityDrillDown(requestData, callback) {
    var request = [
        'GetComplianceApplicabilityStatusDrillDown',
        requestData
    ];
    var callerName = 'client_dashboard';
    clientApiRequest(callerName, request, callback);
}

/* Notifications */
function getNotificationsCount(le_ids, callback) {
    callerName = 'client_dashboard';
    var request = [
        'GetNotificationsCount', {
            'le_ids': le_ids
        }
    ];
    clientApiRequest(callerName, request, callback);
}

function getNotifications(le_ids, notification_type, start_count, end_count, callback) {
    callerName = 'client_dashboard';
    var request = [
        'GetNotifications', {
            'le_ids': le_ids,
            'notification_type': notification_type,
            'start_count': start_count,
            'end_count': end_count
        }
    ];
    clientApiRequest(callerName, request, callback);
}

function updateNotificationStatus(le_ids, notification_id, has_read, extra_details, callback) {
    callerName = 'client_dashboard';
    var request = [
        'UpdateNotificationStatus', {
            'le_ids': le_ids,
            'notification_id': notification_id,
            'has_read': has_read,
            "extra_details": extra_details
        }
    ];
    clientApiRequest(callerName, request, callback);
}

/* Statutory Notifications */
function getStatutoryNotifications(le_ids, start_count, end_count, callback) {
    callerName = 'client_dashboard';
    var request = [
        'GetStatutoryNotifications', {
            'le_ids': le_ids,
            'start_count': start_count,
            'end_count': end_count
        }
    ];
    clientApiRequest(callerName, request, callback);
}

function updateStatutoryNotificationsStatus(le_ids, notification_id, has_read, callback) {
    callerName = 'client_dashboard';
    var request = [
        'UpdateStatutoryNotificationsStatus', {
            'le_ids': le_ids,
            'notification_id': notification_id,
            'has_read': has_read
        }
    ];
    clientApiRequest(callerName, request, callback);
}

/* Get Compliance List*/
function getCurrentComplianceDetail(le_id, unit_id, current_start_count, cal_view, cal_date, callback) {
    callerName = 'client_user';
    var request = [
        'GetCurrentComplianceDetail', {
            'le_id': le_id,
            'unit_id': unit_id,
            'current_start_count': current_start_count,
            'cal_view': cal_view,
            'cal_date': cal_date
        }
    ];
    clientApiRequest(callerName, request, callback);
}

function getUpcomingComplianceDetail(le_id, unit_id, upcoming_start_count, cal_view, cal_date, callback) {
    callerName = 'client_user';
    var request = [
        'GetUpcomingComplianceDetail', {
            'le_id': le_id,
            'unit_id': unit_id,
            'upcoming_start_count': upcoming_start_count,
            'cal_view': cal_view,
            'cal_date': cal_date
        }
    ];
    clientApiRequest(callerName, request, callback);
}

function progress(percent, $element) {
    var progressBarWidth = percent * $element.width() / 100;
    $('.upload-progress-count').html("Uploading " + percent + "% ")
}

function updateComplianceDetail(
    le_id, compliance_history_id, documents, uploaded_documents,
    completion_date, validity_date, next_due_date, remarks, callback
) {
    if (documents != null) {
        // for(var i =  0; i<documents.length; i++){
        //     documents[i]["file_content"] = null;
        // }
        $.each(documents, function(k, val) {
            val["file_content"] = null;
        });
    }
    var request = [
        'UpdateComplianceDetail', {
            'le_id': le_id,
            'compliance_history_id': compliance_history_id,
            'documents': documents,
            'uploaded_documents': uploaded_documents,
            'completion_date': completion_date,
            'validity_date': validity_date,
            'next_due_date': next_due_date,
            'remarks': remarks
        }
    ];
    var sessionToken = getSessionToken();
    var requestFrame = {
        'session_token': sessionToken,
        'request': request
    };
    var body = [
        sessionToken,
        requestFrame
    ];
    $.ajax({

        xhr: function() {
            var xhr = new window.XMLHttpRequest();
            xhr.upload.addEventListener("progress", function(evt) {
                if (evt.lengthComputable) {
                    var percentComplete = evt.loaded / evt.total;
                    percentComplete = parseInt(percentComplete * 100);
                    progress(percentComplete, $('#progressBar'));
                    console.log(percentComplete)
                    if (percentComplete === 100) {
                        //console.log(percentComplete)
                        $('.upload-progress-count').hide();
                    }

                }
            }, false);
            return xhr;
        },

        url: CLIENT_BASE_URL + 'client_user',
        headers: { 'X-Xsrftoken': getCookie('_xsrf'), 'Caller-Name': window.location.pathname },
        type: 'POST',
        contentType: 'application/json',
        data: makekey() + btoa(toJSON(body)),
        success: function(data) {
            data = atob(data.substring(5));
            data = parseJSON(data);
            var status = data[0];
            var response = data[1];
            matchString = 'success';
            log('API STATUS :' + status);
            ///callback(null, response)
            if (status.toLowerCase().indexOf(matchString) != -1) {
                callback(null, response);
            } else if (status == 'InvalidSessionToken') {
                confirm_ok_alert(message[status], "/login");

            } else {
                if (status == 'SavePastRecordsFailed') {
                    callback(data, null);
                } else {
                    callback(status, response);
                }
            }
        },
        error: function(jqXHR, textStatus, errorThrown) {
            rdata = parseJSON(jqXHR.responseText);
            rdata = atob(rdata.substring(5));
            callback(rdata, errorThrown);
        }
    });
}

// Reassigned History Report Start
function getReassignedHistoryReportFilters(le_id, callback) {
    var request = [
        'GetReassignedHistoryReportFilters', {
            'le_id': le_id
        }
    ];
    callerName = 'client_reports';
    clientApiRequest(callerName, request, callback);
}

function getReassignedHistoryReport(c_id, le_id, d_id, u_id, act, compliance_task, usr_id, from_date, to_date, f_count, t_count, csv, count_qry, callback) {
    var request = [
        'GetReassignedHistoryReport', {
            'c_id': c_id,
            'le_id': le_id,
            'd_id': d_id,
            'unit_id': u_id,
            'act': act,
            'compliance_task': compliance_task,
            'usr_id': usr_id,
            'from_date': from_date,
            'to_date': to_date,
            'csv': csv,
            'f_count': f_count,
            't_count': t_count,
            'count_qry': count_qry
        }
    ];
    callerName = 'client_reports';
    clientApiRequest(callerName, request, callback);
}
// Reassigned History Report End

// Status Report Consolidated Report Start
function getStatusReportConsolidatedFilters(le_id, callback) {
    var request = [
        'GetStatusReportConsolidatedFilters', {
            'le_id': le_id
        }
    ];
    callerName = 'client_reports';
    clientApiRequest(callerName, request, callback);
}


function getStatusReportConsolidated(c_id, le_id, d_id, u_id, act, compliance_task, usr_id, comp_fre_id, user_type_id, comp_task_status_id, from_date, to_date, f_count, t_count, csv, count_qry, callback) {
    var request = [
        'GetStatusReportConsolidated', {
            'c_id': c_id,
            'le_id': le_id,
            'd_id': d_id,
            'unit_id': u_id,
            'act': act,
            'compliance_task': compliance_task,
            'frequency_id': comp_fre_id,
            'user_type_id': user_type_id,
            'status_name': comp_task_status_id,
            'usr_id': usr_id,
            'from_date': from_date,
            'to_date': to_date,
            'csv': csv,
            'f_count': f_count,
            't_count': t_count,
            'count_qry': count_qry
        }
    ];
    callerName = 'client_reports';
    clientApiRequest(callerName, request, callback);
}
// Status Report Consolidated Report End


// Statutory Settings Unit Wise Start
function getStatutorySettingsUnitWiseFilters(le_id, callback) {
    var request = [
        'GetStatutorySettingsUnitWiseFilters', {
            'le_id': le_id
        }
    ];
    callerName = 'client_reports';
    clientApiRequest(callerName, request, callback);
}

function getStatutorySettingsUnitWise(c_id, bg_id, le_id, d_id, u_id, div_id, cat_id, act, compliance_task, comp_fre_id, comp_task_status_id, f_count, t_count, csv, count_qry, callback) {
    var request = [
        'GetStatutorySettingsUnitWise', {
            'c_id': c_id,
            'bg_id': bg_id,
            'le_id': le_id,
            'd_id': d_id,
            'unit_id': u_id,
            'div_id': div_id,
            'cat_id': cat_id,
            'act': act,
            'compliance_task': compliance_task,
            'frequency_id': comp_fre_id,
            'status_name': comp_task_status_id,
            'csv': csv,
            'f_count': f_count,
            't_count': t_count,
            'count_qry': count_qry
        }
    ];
    callerName = 'client_reports';
    clientApiRequest(callerName, request, callback);
}
// Statutory Settings Unit Wise End

// Domain Score Card Start
function getDomainScoreCardFilters(le_id, callback) {
    var request = [
        'GetDomainScoreCardFilters', {
            'le_id': le_id
        }
    ];
    callerName = 'client_reports';
    clientApiRequest(callerName, request, callback);
}

function getDomainScoreCard(c_id, bg_id, le_id, d_id, div_id, cat_id, csv, callback) {
    var request = [
        'GetDomainScoreCard', {
            'c_id': c_id,
            'bg_id': bg_id,
            'le_id': le_id,
            'd_id': d_id,
            'div_id': div_id,
            'cat_id': cat_id,
            'csv': csv
        }
    ];
    callerName = 'client_reports';
    clientApiRequest(callerName, request, callback);
}
// Domain Score Card End

// Legal Entity Wise Score Card Start
function getLEWiseScoreCardFilters(le_id, callback) {
    var request = [
        'GetLEWiseScoreCardFilters', {
            'le_id': le_id
        }
    ];
    callerName = 'client_reports';
    clientApiRequest(callerName, request, callback);
}

function getLEWiseScoreCard(c_id, le_id, d_id, csv, callback) {
    var request = [
        'GetLEWiseScoreCard', {
            'c_id': c_id,
            'le_id': le_id,
            'd_id': d_id,
            'csv': csv
        }
    ];
    callerName = 'client_reports';
    clientApiRequest(callerName, request, callback);
}
// Legal Entity Wise Score Card End

// Work Flow Score Card Start
function getWorkFlowScoreCardFilters(le_id, callback) {
    var request = [
        'GetWorkFlowScoreCardFilters', {
            'le_id': le_id
        }
    ];
    callerName = 'client_reports';
    clientApiRequest(callerName, request, callback);
}

function getWorkFlowScoreCard(c_id, le_id, d_id, csv, callback) {
    var request = [
        'GetWorkFlowScoreCard', {
            'c_id': c_id,
            'le_id': le_id,
            'd_id': d_id,
            'csv': csv
        }
    ];
    callerName = 'client_reports';
    clientApiRequest(callerName, request, callback);
}
// Work Flow Score Card End

function getComplianceActivityReportFilters(callback) {
    var request = [
        'GetComplianceActivityReportFilters',
        {}
    ];
    callerName = 'client_reports';
    clientApiRequest(callerName, request, callback);
}

function getComplianceActivityReportData(user_type, user_id, country_id, domain_id, level_1_statutory_name, unit_id, compliance_id, from_date, to_date, csv, callback) {
    var request = [
        'GetComplianceActivityReport', {
            'user_type': user_type,
            'user_id': user_id,
            'country_id': country_id,
            'domain_id': domain_id,
            'level_1_statutory_name': level_1_statutory_name,
            'unit_id': unit_id,
            'compliance_id': compliance_id,
            'from_date': from_date,
            'to_date': to_date,
            'csv': csv
        }
    ];
    callerName = 'client_reports';
    clientApiRequest(callerName, request, callback);
}

function getClientDetailsReportData(countryId, businessGroupId, legalEntityId, divisionId, unitId, domainIds, csv, from_count, page_count, callback) {
    callerName = 'client_reports';
    var request = [
        'GetClientDetailsReportData', {
            'country_id': countryId,
            'business_group_id': businessGroupId,
            'legal_entity_id': legalEntityId,
            'division_id': divisionId,
            'unit_id': unitId,
            'domain_ids': domainIds,
            'csv': csv,
            'from_count': from_count,
            'page_count': page_count
        }
    ];
    clientApiRequest(callerName, request, callback);
}

function getAssigneewiseComplianesFilters(callback) {
    var request = [
        'GetAssigneewiseComplianesFilters',
        {}
    ];
    callerName = 'client_master_filters';
    clientApiRequest(callerName, request, callback);
}

function getAssigneewiseComplianes(country_id, business_group_id, legal_entity_id, division_id, unit_id, user_id, csv, callback) {
    var request = [
        'GetAssigneeWiseCompliancesChart', {
            'c_id': country_id,
            'bg_id': business_group_id,
            'le_ids': legal_entity_id,
            'div_id': division_id,
            'unit_id': unit_id,
            'usr_id': user_id,
            'csv': csv
        }
    ];
    callerName = 'client_dashboard';
    clientApiRequest(callerName, request, callback);
}

function getAssigneewiseYearwiseComplianes(country_id, unit_id, user_id, legalEntityIds, d_ids, callback) {
    var request = [
        'GetAssigneewiseYearwiseCompliances', {
            'c_id': country_id,
            'u_id': unit_id,
            'usr_id': user_id,
            'le_ids': legalEntityIds,
            'd_ids': d_ids,

        }
    ];
    callerName = 'client_dashboard';
    clientApiRequest(callerName, request, callback);
}

function getAssigneewiseReassignedComplianes(country_id, unit_id, user_id, domain_id, legalEntityIds, callback) {
    var request = [
        'GetAssigneewiseReassignedComplianes', {
            'c_id': country_id,
            'u_id': unit_id,
            'usr_id': user_id,
            'd_id': domain_id,
            "le_ids": legalEntityIds,
        }
    ];
    callerName = 'client_dashboard';
    clientApiRequest(callerName, request, callback);
}

function getAssigneewiseCompliancesDrilldown(country_id, assignee_id, domain_ids, year, unit_id, start_count, legalEntityIds, callback) {
    var request = [
        'GetAssigneeWiseComplianceDrillDown', {
            'c_id': country_id,
            'assignee_id': assignee_id,
            'd_ids': domain_ids,
            'chart_year': year,
            'unit_id': unit_id,
            'start_count': start_count,
            'le_ids': legalEntityIds
        }
    ];
    callerName = 'client_dashboard';
    clientApiRequest(callerName, request, callback);
}

function getTaskApplicabilityReportFilters(callback) {
    var request = [
        'GetTaskApplicabilityStatusFilters',
        {}
    ];
    callerName = 'client_reports';
    clientApiRequest(callerName, request, callback);
}

function getTaskApplicabilityReportData(country_id, domain_id, business_group_id, legal_entity_id, division_id, unit_id, statutory_name, applicable_status, csv, record_count, callback) {
    var request = [
        'GetComplianceTaskApplicabilityStatusReport', {
            'country_id': country_id,
            'domain_id': domain_id,
            'business_group_id': business_group_id,
            'legal_entity_id': legal_entity_id,
            'division_id': division_id,
            'unit_id': unit_id,
            'statutory_name': statutory_name,
            'applicable_status': applicable_status,
            'csv': csv,
            'record_count': record_count
        }
    ];
    callerName = 'client_reports';
    clientApiRequest(callerName, request, callback);
}

function getOnOccurrenceCompliances(le_id, unit_id, start_count, callback) {
    var request = [
        'GetOnOccurrenceCompliances', {
            'le_id': le_id,
            'unit_id': unit_id,
            'start_count': start_count
        }
    ];
    callerName = 'client_user';
    clientApiRequest(callerName, request, callback);
}

function startOnOccurrenceCompliance(le_id, compliance_id, start_date, unit_id, duration, remarks, password, callback) {
    var request = [
        'StartOnOccurrenceCompliance', {
            'le_id': le_id,
            'compliance_id': compliance_id,
            'start_date': start_date,
            'unit_id': unit_id,
            'duration': duration,
            'remarks': remarks,
            'password': password
        }
    ];
    callerName = 'client_user';
    clientApiRequest(callerName, request, callback);
}

function complianceFilters(le_id, callback) {
    var request = [
        'ComplianceFilters', {
            'le_id': le_id
        }
    ];
    callerName = 'client_user';
    clientApiRequest(callerName, request, callback);
}

function onOccurrenceLastTransaction(le_id, compliance_id, unit_id, callback) {
    var request = [
        'OnOccurrenceLastTransaction', {
            'le_id': le_id,
            'compliance_id': compliance_id,
            'unit_id': unit_id
        }
    ];
    callerName = 'client_user';
    clientApiRequest(callerName, request, callback);
}

function exportToCSV(jsonResponse, callback) {
    var request = [
        'ExportToCSV',
        { 'data': jsonResponse }
    ];
    callerName = 'client_reports';
    clientApiRequest(callerName, request, callback);
}

function getUserwiseCompliances(callback) {
    var request = [
        'GetUserwiseCompliances',
        {}
    ];
    callerName = 'client_transaction';
    clientApiRequest(callerName, request, callback);
}

function checkContractExpiration(callback) {
    var request = [
        'CheckContractExpiration',
        {}
    ];
    callerName = 'client_dashboard';
    clientApiRequest(callerName, request, callback);
}
// Client User Group
function getClientUserGroups(callback) {
    callerName = 'client_masters';
    var request = [
        'GetUserPrivileges',
        {}
    ];
    clientApiRequest(callerName, request, callback);
}

function saveClientUserGroup(u_g_name, f_cat_id, f_ids, callback) {
    callerName = 'client_masters';
    var request = [
        'SaveUserPrivileges', {
            'u_g_name': u_g_name,
            'u_c_id': f_cat_id,
            'f_ids': f_ids
        }
    ];
    clientApiRequest(callerName, request, callback);
}

function updateClientUserGroup(u_g_id, u_g_name, f_cat_id, f_ids, callback) {
    callerName = 'client_masters';
    var request = [
        'UpdateUserPrivileges', {
            'u_g_id': u_g_id,
            'u_g_name': u_g_name,
            'u_c_id': f_cat_id,
            'f_ids': f_ids
        }
    ];
    clientApiRequest(callerName, request, callback);
}

function changeClientUserGroupStatus(ugId, active, password, callback) {
    callerName = 'client_masters';
    var request = [
        'ChangeUserPrivilegeStatus', {
            'u_g_id': ugId,
            'is_active': active,
            "password": password
        }
    ];
    clientApiRequest(callerName, request, callback);
}
// Service Providers
function getServiceProviders(callback) {
    callerName = 'client_masters';
    var request = [
        'GetServiceProviders',
        {}
    ];
    clientApiRequest(callerName, request, callback);
}

function getSaveServiceProviderDict(serviceProviderDetail) {
    add = serviceProviderDetail[1];
    if (add == '') {
        add = null;
    }
    result = {
        's_name': serviceProviderDetail[0],
        'add': add,
        'c_from': serviceProviderDetail[2],
        'c_to': serviceProviderDetail[3],
        'c_person': serviceProviderDetail[4],
        'c_no': serviceProviderDetail[5]
    };
    return result;
}

function saveServiceProvider(s_p_name, s_p_short, cont_from, cont_to, cont_person, cont_no, mob_no, e_id, address, callback) {
    callerName = 'client_masters';
    var request = [
        'SaveServiceProvider', {
            "s_p_name": s_p_name,
            "s_p_short": s_p_short,
            "cont_from": cont_from,
            "cont_to": cont_to,
            "cont_person": cont_person,
            "cont_no": cont_no,
            "mob_no": mob_no,
            "e_id": e_id,
            "address": address
        }
    ];
    clientApiRequest(callerName, request, callback);
}

function getUpdateServiceProviderDict(serviceProviderDetail) {
    add = serviceProviderDetail[2];
    if (add == '') {
        add = null;
    } else {
        add = serviceProviderDetail[9]
    }
    return {
        's_p_id': serviceProviderDetail[0],
        's_p_name': serviceProviderDetail[1],
        's_p_short': serviceProviderDetail[2],
        'address': add,
        'cont_from': serviceProviderDetail[3],
        'cont_to': serviceProviderDetail[4],
        'cont_person': serviceProviderDetail[5],
        'cont_no': serviceProviderDetail[6],
        'mob_no': serviceProviderDetail[7],
        'e_id': serviceProviderDetail[8]
    };
}

function updateServiceProvider(serviceProviderDetail, callback) {
    callerName = 'client_masters';
    var request = [
        'UpdateServiceProvider',
        serviceProviderDetail
    ];
    clientApiRequest(callerName, request, callback);
}

function changeServiceProviderStatus(sId, active, password, callback) {
    callerName = 'client_masters';
    var request = [
        'ChangeServiceProviderStatus', {
            'sp_id': sId,
            'active_status': active,
            "password": password
        }
    ];
    clientApiRequest(callerName, request, callback);
}

function blockServiceProvider(sId, block, remarks, password, callback) {
    callerName = 'client_masters';
    var request = [
        'BlockServiceProvider', {
            'sp_id': sId,
            'is_blocked': block,
            'remarks': remarks,
            "password": password
        }
    ];
    clientApiRequest(callerName, request, callback);
}

function blockUser(user_id, block, remarks, password, callback) {
    callerName = 'client_masters';
    var request = [
        'BlockUser', {
            'user_id': user_id,
            'is_blocked': block,
            'remarks': remarks,
            "password": password
        }
    ];
    clientApiRequest(callerName, request, callback);
}

function resendRegistrationEmail(user_id, callback) {
    callerName = 'client_masters';
    var request = [
        'ResendRegistrationEmail', {
            'user_id': user_id
        }
    ];
    clientApiRequest(callerName, request, callback);
}



// Client User
function getClientUsers(callback) {
    callerName = 'client_masters';
    var request = [
        'GetClientUsers',
        {}
    ];
    clientApiRequest(callerName, request, callback);
}

function saveClientUser(clientUserDetail, callback) {
    callerName = 'client_masters';
    var request = [
        'SaveClientUser',
        clientUserDetail
    ];
    clientApiRequest(callerName, request, callback);
}

function updateClientUser(clientUserDetail, callback) {
    callerName = 'client_masters';
    var request = [
        'UpdateClientUser',
        clientUserDetail
    ];
    clientApiRequest(callerName, request, callback);
}

function employeeCodeExists(mode, uId, emp_code, callback) {
    callerName = 'client_masters';
    var request = [
        'EmployeeCodeExists', {
            'mode': mode,
            'user_id_optional': uId,
            'employee_code': emp_code
        }
    ];
    clientApiRequest(callerName, request, callback);
}

function changeClientUserStatus(uId, active_status, employeeName, password, callback) {
    callerName = 'client_masters';
    var request = [
        'ChangeClientUserStatus', {
            'u_id': uId,
            'active_status': active_status,
            'emp_name': employeeName,
            'password': password
        }
    ];
    clientApiRequest(callerName, request, callback);
}

//Client Profile
function getClientProfile(callback) {
    callerName = 'techno';
    var request = [
        'GetClientProfile',
        {}
    ];
    clientApiRequest(callerName, request, callback);
}

function getClientDetailsReport(countryId, clientId, businessGroupId, legalEntityId, divisionId, unitId, domainIds, csv, callback) {
    callerName = 'techno';
    var request = [
        'GetClientDetailsReport', {
            'country_id': countryId,
            'group_id': clientId,
            'business_group_id': businessGroupId,
            'legal_entity_id': legalEntityId,
            'division_id': divisionId,
            'unit_id': unitId,
            'domain_ids': domainIds,
            'csv': csv
        }
    ];
    clientApiRequest(callerName, request, callback);
}
//
// Statutory settings
//
function getStatutorySettings(legalEntityId, divisionId, categoryId, callback) {
    callerName = 'client_transaction';
    var request = [
        'GetStatutorySettings', {
            'le_id': legalEntityId,
            'div_id': divisionId,
            'cat_id': categoryId
        }
    ];
    clientApiRequest(callerName, request, callback);
}

function getStatutorySettingsCompliance(legalEntityId, unitIds, recordCount, domainId, callback) {
    callerName = 'client_transaction';
    var request = [
        'GetSettingsCompliances', {
            'le_id': legalEntityId,
            'u_ids': unitIds,
            'r_count': recordCount,
            'd_id': domainId
        }
    ];
    clientApiRequest(callerName, request, callback);
}

function updateStatutory(clientCId, aStatus, naRemarks, compId, oStatus, remarks, uName, uId) {
    return {
        'c_c_id': clientCId,
        'a_status': aStatus,
        'n_a_remarks': naRemarks,
        'comp_id': compId,
        'c_o_status': oStatus,
        'c_remarks': remarks,
        'u_name': uName,
        'u_id': uId
    };
}

function updateStatutorySettings(password, statutories, legalEntityId, submissionStatus, dId, uIds, callback) {
    var request = [
        'UpdateStatutorySettings', {
            'password': password,
            'update_statutories': statutories,
            'le_id': legalEntityId,
            's_s': submissionStatus,
            'd_id': dId,
            'u_ids': uIds
        }
    ];
    var callerName = 'client_transaction';
    clientApiRequest(callerName, request, callback);
}

function saveStatutorySettings(statutories, legalEntityId, submissionStatus, dId, uIds, callback) {
    var request = [
        'SaveStatutorySettings', {
            'update_statutories': statutories,
            'le_id': legalEntityId,
            's_s': submissionStatus,
            'd_id': dId,
            'u_ids': uIds
        }
    ];
    var callerName = 'client_transaction';
    clientApiRequest(callerName, request, callback);
}

//
// Assign compliance
//
function getAssignComplianceFormData(callback) {
    var request = [
        'GetAssignCompliancesFormData',
        {}
    ];
    var callerName = 'client_master_filters';
    clientApiRequest(callerName, request, callback);
}

function getAssignComplianceUnits(legalEntityId, domainId, countryId, callback) {
    var request = [
        'GetAssignComplianceUnits', {
            'le_id': legalEntityId,
            'd_id': domainId,
            'c_id': countryId,
        }
    ];
    var callerName = 'client_transaction';
    clientApiRequest(callerName, request, callback);
}

function getAssignComplianceForUnits(legalEntityId, unitIds, domainId, recordCount, frequency_ids, callback) {
    var request = [
        'GetComplianceForUnits', {
            'le_id': legalEntityId,
            'u_ids': unitIds,
            'd_id': domainId,
            'r_count': recordCount,
            "f_ids": frequency_ids
        }
    ];
    var callerName = 'client_transaction';
    clientApiRequest(callerName, request, callback);
}

function getComplianceTotalToAssign(legalEntityId, unitIds, domainId, frequency_ids, callback) {
    var request = [
        'GetComplianceTotalToAssign', {
            'le_id': legalEntityId,
            'u_ids': unitIds,
            'd_id': domainId,
            'f_ids': frequency_ids
        }
    ];
    var callerName = 'client_transaction';
    clientApiRequest(callerName, request, callback);
}

function getUserToAssignCompliance(domainId, unitIds, legalEntityId, callback) {
    var request = [
        'GetUserToAssignCompliance', {
            'd_id': domainId,
            'u_ids': unitIds,
            'le_id': legalEntityId
        }
    ];
    var callerName = 'client_master_filters';
    clientApiRequest(callerName, request, callback);
}


function statutoryDates(date, month, triggerBefore, repeatBy) {
    var statutoryDate = {};
    statutoryDate.statutory_date = date;
    statutoryDate.statutory_month = month;
    statutoryDate.trigger_before_days = triggerBefore;
    statutoryDate.repeat_by = repeatBy;
    return statutoryDate;
}

function assignCompliances(compId, compName, sDateList, dDate, vDate, trigBefore, uIds, rBy, rEvery, frequency) {
    return {
        'comp_id': compId,
        'comp_name': compName,
        'statu_dates': sDateList,
        'd_date': dDate,
        'v_date': vDate,
        'trigger_before_days': trigBefore,
        'u_ids': uIds,
        'repeat_by': rBy,
        'r_every': rEvery,
        'frequency': frequency
    };
}

function newUnitSettings(userId, uIds, dIds, cIds) {
    return {
        'user_id': userId,
        'u_ids': uIds,
        'd_ids': dIds,
        'c_ids': cIds
    };
}

function saveAssignedComplianceFormData(assignee, aName, concurrence, conName, approval, appName, compliances, legalEntityId, domainId, unitIds, callback) {
    var request = [
        'SaveAssignedCompliance', {
            'assignee': assignee,
            'assignee_name': aName,
            'concurrence_person': concurrence,
            'concurrer_name': conName,
            'approval_person': approval,
            'approver_name': appName,
            'assign_compliances': compliances,
            'le_id': legalEntityId,
            'd_id': domainId,
            'u_ids': unitIds
        }
    ];
    var callerName = 'client_transaction';
    clientApiRequest(callerName, request, callback);
}

/* Past Records */
function getPastRecordsFormData(le_id, callback) {
    var request = [
        'GetPastRecordsFormData', {
            'le_id': le_id
        }
    ];
    clientApiRequest('client_transaction', request, callback);
}

function getStatutoriesByUnit(legalEntityId, unit_id, domain_id, level_1_statutory_name, compliance_frequency, start_count, callback) {
    var request = [
        'GetStatutoriesByUnit', {
            'le_id': legalEntityId,
            'unit_id': unit_id,
            'domain_id': domain_id,
            'level_1_statutory_name': level_1_statutory_name,
            'compliance_task_frequency': compliance_frequency,
            'start_count': start_count
        }
    ];
    clientApiRequest('client_transaction', request, callback);
}

function getPastRecordsComplianceDict(unit_id, compliance_id, due_date, completion_date, documents, completed_by) {
    return {
        'unit_id': unit_id,
        'compliance_id': compliance_id,
        'due_date': due_date,
        'completion_date': completion_date,
        'documents': documents,
        'validity_date': null,
        'pr_completed_by': completed_by
    };
}

function savePastRecords(legalEntityId, compliances_list, callback) {
    var request = [
        'SavePastRecords', {
            'le_id': legalEntityId,
            'pr_compliances_1': compliances_list
        }
    ];
    clientApiRequest('client_transaction', request, callback);
}
/* Multiple File Upload */
function uploadFileFormat(size, name, content) {
    result = {
        'file_size': parseInt(size),
        'file_name': name,
        'file_content': content
    };
    return result;
}

function convert_to_base64(file, name, size, callback) {
    var reader = new FileReader();
    reader.onload = function(readerEvt) {
        var binaryString = readerEvt.target.result;
        file_content = btoa(binaryString);
        callback(file_content, name, size);
    };
    reader.readAsBinaryString(file);
}

function uploadFile(fileListener, callback) {
    var evt = fileListener;
    max_limit = 1024 * 1024 * 50;
    // file max limit 50MB
    var files = evt.target.files;
    var results = [];
    for (var i = 0; i < files.length; i++) {
        var file = files[i];
        file_name = file.name;
        file_size = file.size;
        var file_extension = file_name.substring(file_name.lastIndexOf('.') + 1);
        if (file_size > max_limit) {
            displayMessage(message.file_maxlimit_exceed);
            return;
        } else if (file_extension == 'exe') {
            displayMessage(message.invalid_file_format);
            return;
        } else if (file_extension == 'htm') {
            displayMessage(message.invalid_file_format);
            return;
        } else if (file_extension == 'xhtml') {
            displayMessage(message.invalid_file_format);
            return;
        } else if (file_extension == 'html') {
            displayMessage(message.invalid_file_format);
            return;
        } else {
            file_content = null;
            if (file) {
                convert_to_base64(file, file_name, file_size, function(file_content, name, size) {
                    if (file_content == null) {
                        callback(message.file_content_empty);
                    }
                    var fN = name.substring(0, name.indexOf('.'));
                    var fE = name.substring(name.lastIndexOf('.') + 1);
                    var uniqueId = Math.floor(Math.random() * 90000) + 10000;
                    var f_Name = fN + '-' + uniqueId + '.' + fE;

                    result = uploadFileFormat(size, f_Name, file_content);
                    results.push(result);
                    if (results.length == files.length) {
                        callback(results);
                    }
                });
            }
        }
    }
}

function getAssigneeWiseCompliances(assignee, record_count, callback) {
    var request = [
        'GetAssigneeCompliances', {
            'assignee': assignee,
            'record_count': record_count
        }
    ];
    callerName = 'client_transaction';
    clientApiRequest(callerName, request, callback);
}

function reassignComplianceDet(uID, cID, cNAME, cHistoryId, dDate, oAssignee, oConcurrence, oApprover) {
    return {
        'u_id': uID,
        'comp_id': cID,
        'compliance_name': cNAME,
        'c_h_id': cHistoryId,
        'd_date': dDate,
        'o_assignee': oAssignee,
        'o_concurrence_person': oConcurrence,
        'o_approval_person': oApprover
    };
}

function saveReassignCompliance(legalEntityId, rFrom, rTo, aName, cPerson, aPerson, cList, reason, callback) {
    request = [
        'ReassignCompliance', {
            'le_id': legalEntityId,
            'r_from': rFrom,
            'assignee': rTo,
            'assignee_name': aName,
            'concurrence_person': cPerson,
            'approval_person': aPerson,
            'reassigned_compliance': cList,
            'reason': reason
        }
    ];
    callerName = 'client_transaction';
    clientApiRequest(callerName, request, callback);
}

function getContractExpireAndNotificationCount() {
    var clientNotificationCount = window.sessionStorage.CLIENT_NOTIFICATION_COUNT;
    var clientReminderCount = window.sessionStorage.CLIENT_REMINDER_COUNT;
    var clientEscalationCount = window.sessionStorage.CLIENT_ESCALATION_COUNT;
    if (typeof clientNotificationCount != 'undefined' && clientNotificationCount != null) {
        $('#notification_count').text(clientNotificationCount);
    } else {
        $('#notification_count').text('0');
    }
    if (typeof clientReminderCount != 'undefined' && clientReminderCount != null) {
        $('#reminder_count').text(clientReminderCount);
    } else {
        $('#reminder_count').text('0');
    }
    if (typeof clientEscalationCount != 'undefined' && clientEscalationCount != null) {
        $('#escalation_count').text(clientEscalationCount);
    } else {
        $('#escalation_count').text('0');
    }
}

function getUnitClosureData(callback) {
    var request = [
        'GetUnitClosureData',
        {}
    ];
    callerName = 'client_masters';
    clientApiRequest(callerName, request, callback);
}

function getUnitClosureUnitList(le_id, callback) {
    var request = [
        'GetUnitClosureUnitData', {
            "legal_entity_id": le_id
        }
    ];
    callerName = 'client_masters';
    clientApiRequest(callerName, request, callback);
}

function saveUnitClosureData(legal_entity_id, password, remarks, unit_id, action_mode, callback) {
    callerName = 'client_masters';
    var request = [
        'SaveUnitClosureData', {
            "password": password,
            "closed_remarks": remarks,
            "unit_id": unit_id,
            "grp_mode": action_mode,
            "legal_entity_id": legal_entity_id
        }
    ];
    clientApiRequest(callerName, request, callback);
}

function uploadFormatFile(formdata, callback) {
    $.ajax({
        url: '/api/files/' + getSessionToken(),
        type: 'POST',
        crossDomain: true,
        data: formdata,
        processData: false,
        contentType: false,
        success: function(data, textStatus, jqXHR) {
            // var data = parseJSON(data);
            var status = data[0];
            var response = data[1];
            if (Object.keys(response).length == 0)
                callback(status, null);
            else
                callback(status, response);
        },
        error: function(jqXHR, textStatus, errorThrown) {}
    });
}

/* Legal entity wise report - updated*/
function getLegalEntityWiseReportFilters(country_id, le_id, callback) {
    console.log(country_id + ' - ' + le_id);
    var request = [
        'GetLegalEntityWiseReportFilters', {
            'country_id': country_id,
            'legal_entity_id': le_id
        }
    ];
    callerName = 'client_reports';
    clientApiRequest(callerName, request, callback);
}

function getLegalEntityWiseReport(
    country_id, legal_entity_id, domain_id, unit_id, statutory_mapping,
    compliance_id, frequency_id, user_type, user_id, from_date, to_date,
    task_status, csv, from_count, page_count, callback
) {
    var request = [
        'GetLegalEntityWiseReport', {
            'country_id': country_id,
            'legal_entity_id': legal_entity_id,
            'domain_id': domain_id,
            'unit_id': unit_id,
            'statutory_mapping': statutory_mapping,
            'compliance_id': compliance_id,
            'frequency_id': frequency_id,
            'user_type': user_type,
            'user_id': user_id,
            'due_from_date': from_date,
            'due_to_date': to_date,
            'task_status': task_status,
            'csv': csv,
            'from_count': from_count,
            'page_count': page_count
        }
    ];
    callerName = 'client_reports';
    clientApiRequest(callerName, request, callback);
}

function getReviewSettingsFilters(le_id, callback) {
    var request = [
        'GetReviewSettingsFilters', {
            "le_id": le_id
        }
    ];
    callerName = 'client_transaction';
    clientApiRequest(callerName, request, callback);
}

/* Domain Wise report - updated*/
function getDomainWiseReportFilters(country_id, le_id, callback) {
    var request = [
        'GetDomainWiseReportFilters', {
            'country_id': country_id,
            'legal_entity_id': le_id
        }
    ];
    callerName = 'client_reports';
    clientApiRequest(callerName, request, callback);
}

function getDomainWiseReport(
    country_id, legal_entity_id, domain_id, unit_id, statutory_mapping,
    compliance_id, frequency_id, user_type, user_id, from_date, to_date,
    task_status, csv, from_count, page_count, callback
) {
    var request = [
        'GetDomainWiseReport', {
            'country_id': country_id,
            'legal_entity_id': legal_entity_id,
            'domain_id': domain_id,
            'unit_id': unit_id,
            'statutory_mapping': statutory_mapping,
            'compliance_id': compliance_id,
            'frequency_id': frequency_id,
            'user_type': user_type,
            'user_id': user_id,
            'due_from_date': from_date,
            'due_to_date': to_date,
            'task_status': task_status,
            'csv': csv,
            'from_count': from_count,
            'page_count': page_count
        }
    ];
    callerName = 'client_reports';
    clientApiRequest(callerName, request, callback);
}

/* Domain Wise report - updated*/
function getUnitWiseReportFilters(country_id, le_id, callback) {
    var request = [
        'GetUnitWiseReportFilters', {
            'country_id': country_id,
            'legal_entity_id': le_id
        }
    ];
    callerName = 'client_reports';
    clientApiRequest(callerName, request, callback);
}

function getUnitWiseReport(
    country_id, legal_entity_id, unit_id, domain_id, statutory_mapping,
    compliance_id, frequency_id, user_type, user_id, from_date, to_date,
    task_status, csv, from_count, page_count, callback
) {
    var request = [
        'GetUnitWiseReport', {
            'country_id': country_id,
            'legal_entity_id': legal_entity_id,
            'unit_id': unit_id,
            'd_id_optional': domain_id,
            'statutory_mapping': statutory_mapping,
            'compliance_id': compliance_id,
            'frequency_id': frequency_id,
            'user_type': user_type,
            'user_id': user_id,
            'due_from_date': from_date,
            'due_to_date': to_date,
            'task_status': task_status,
            'csv': csv,
            'from_count': from_count,
            'page_count': page_count
        }
    ];
    callerName = 'client_reports';
    clientApiRequest(callerName, request, callback);
}
/* Service Provider Wise report - updated*/
function getServiceProviderWiseReportFilters(country_id, le_id, callback) {
    var request = [
        'GetServiceProviderWiseReportFilters', {
            'country_id': country_id,
            'legal_entity_id': le_id
        }
    ];
    callerName = 'client_reports';
    clientApiRequest(callerName, request, callback);
}

function getServiceProviderWiseReport(
    country_id, legal_entity_id, sp_id, domain_id, unit_id, statutory_mapping,
    compliance_id, user_id, from_date, to_date,
    task_status, csv, from_count, page_count, callback
) {
    var request = [
        'GetServiceProviderWiseReport', {
            'country_id': country_id,
            'legal_entity_id': legal_entity_id,
            'sp_id': sp_id,
            'domain_id': domain_id,
            'unit_id': unit_id,
            'statutory_mapping': statutory_mapping,
            'compliance_id': compliance_id,
            'user_id': user_id,
            'due_from_date': from_date,
            'due_to_date': to_date,
            'task_status': task_status,
            'csv': csv,
            'from_count': from_count,
            'page_count': page_count
        }
    ];
    callerName = 'client_reports';
    clientApiRequest(callerName, request, callback);
}

/* User Wise report - updated*/
function getUserWiseReportFilters(country_id, le_id, callback) {
    var request = [
        'GetUserWiseReportFilters', {
            'country_id': country_id,
            'legal_entity_id': le_id
        }
    ];
    callerName = 'client_reports';
    clientApiRequest(callerName, request, callback);
}

function getUserWiseReport(
    country_id, legal_entity_id, user_id, domain_id, unit_id, statutory_mapping,
    compliance_id, frequency_id, user_type, from_date, to_date,
    task_status, csv, from_count, page_count, callback
) {
    var request = [
        'GetUserWiseReport', {
            'country_id': country_id,
            'legal_entity_id': legal_entity_id,
            'user_id': user_id,
            'domain_id': domain_id,
            'unit_id': unit_id,
            'statutory_mapping': statutory_mapping,
            'compliance_id': compliance_id,
            'frequency_id': frequency_id,
            'user_type': user_type,
            'due_from_date': from_date,
            'due_to_date': to_date,
            'task_status': task_status,
            'csv': csv,
            'from_count': from_count,
            'page_count': page_count
        }
    ];
    callerName = 'client_reports';
    clientApiRequest(callerName, request, callback);
}

function getReviewSettingsUnitFilters(le_id, d_id, callback) {
    var request = [
        'GetReviewSettingsUnitFilters', {
            "le_id": le_id,
            "d_id": d_id
        }
    ];
    callerName = 'client_transaction';
    clientApiRequest(callerName, request, callback);
}

function getReviewSettingsComplianceFilters(le_id, d_id, units, f_type, sno, callback) {
    var request = [
        'GetReviewSettingsComplianceFilters', {
            "le_id": le_id,
            "d_id": d_id,
            "unit_ids": units,
            "f_id": f_type,
            "sno": sno,
        }
    ];
    callerName = 'client_transaction';
    clientApiRequest(callerName, request, callback);
}

function saveReviewSettingsComplianceDict(
    compliance_id, le_id, d_id, f_type, units, repeat_by, repeat_type_id, due_date, trigger_before_days,
    statu_dates, old_repeat_by, old_repeat_type_id, old_due_date, old_statu_dates
) {
    return {
        'comp_id': compliance_id,
        'le_id': le_id,
        'd_id': d_id,
        'f_id': f_type,
        'unit_ids': units,
        'repeat_by': repeat_by,
        'repeat_type_id': repeat_type_id,
        'due_date': due_date,
        'trigger_before_days': trigger_before_days,
        'statu_dates': statu_dates,
        'old_repeat_by': old_repeat_by,
        'old_repeat_type_id': old_repeat_type_id,
        'old_due_date': old_due_date,
        'old_statu_dates': old_statu_dates,
    };
}

function saveReviewSettingsCompliance(le_id, compliances_list, callback) {
    var request = [
        'SaveReviewSettingsCompliance', {
            'le_id': le_id,
            'rs_compliances': compliances_list
        }
    ];
    clientApiRequest('client_transaction', request, callback);
}

function getStatutorySettingsFilters(callback) {
    var request = [
        'GetStatutorySettingsFilters',
        {}
    ];
    callerName = 'client_master_filters';
    clientApiRequest(callerName, request, callback);
}

/* Unit List report - updated*/
function getUnitListReportFilters(country_id, business_group_id, le_id, callback) {
    var request = [
        'GetUnitListReportFilters', {
            'country_id': country_id,
            'business_group_id': business_group_id,
            'legal_entity_id': le_id
        }
    ];
    callerName = 'client_reports';
    clientApiRequest(callerName, request, callback);
}

function getUnitListReport(
    country_id, business_group_id, legal_entity_id, division_id, category_id,
    unit_id, domain_id, organisation_id, unit_status, csv, from_count, page_count, callback
) {
    var request = [
        'GetUnitListReport', {
            'country_id': country_id,
            'business_group_id': business_group_id,
            'legal_entity_id': legal_entity_id,
            'division_id': division_id,
            'category_id': category_id,
            'unit_id': unit_id,
            'domain_id': domain_id,
            'organisation_id': organisation_id,
            'unit_status': unit_status,
            'csv': csv,
            'from_count': from_count,
            'page_count': page_count
        }
    ];
    callerName = 'client_reports';
    clientApiRequest(callerName, request, callback);
}

/* Statutory Notifications List report - updated*/
function getStatutoryNotificationsListReportFilters(country_id, le_id, callback) {
    var request = [
        'GetStatutoryNotificationsListReportFilters', {
            'country_id': country_id,
            'legal_entity_id': le_id
        }
    ];
    callerName = 'client_reports';
    clientApiRequest(callerName, request, callback);
}

function getStatutoryNotificationsListReportData(
    country_id, legal_entity_id, domain_id, statutory_mapping, from_date,
    to_date, csv, from_count, page_count, callback
) {
    var request = [
        'GetStatutoryNotificationsListReportData', {
            'country_id': country_id,
            'legal_entity_id': legal_entity_id,
            'domain_id': domain_id,
            'statutory_mapping': statutory_mapping,
            'due_from_date': from_date,
            'due_to_date': to_date,
            'csv': csv,
            'from_count': from_count,
            'page_count': page_count
        }
    ];
    callerName = 'client_reports';
    clientApiRequest(callerName, request, callback);
}

/* Service Provider Details report - updated*/
function getServiceProviderDetailsReportFilters(callback) {
    var request = [
        'GetServiceProviderDetailsReportFilters', {}
    ];
    callerName = 'client_masters';
    clientApiRequest(callerName, request, callback);
}

function getServiceProviderDetailsReport(
    sp_id, user_id, s_p_status, from_count, page_count, callback
) {
    var request = [
        'GetServiceProviderDetailsReport', {
            'sp_id': sp_id,
            'user_id': user_id,
            's_p_status': s_p_status,
            'from_count': from_count,
            'page_count': page_count
        }
    ];
    callerName = 'client_masters';
    clientApiRequest(callerName, request, callback);
}

/* Audit Trail - updated*/
function getAuditTrailReportFilters(le_id, callback) {
    var request = [
        'GetAuditTrailReportFilters', {
            'legal_entity_id': le_id
        }
    ];
    callerName = 'client_masters';
    clientApiRequest(callerName, request, callback);
}

function getAuditTrailReportData(
    le_id, user_id, form_id, from_date, to_date, csv, from_count, page_count, check_count, callback
) {
    var request = [
        'GetAuditTrailReportData', {
            'legal_entity_id': le_id,
            'user_id': user_id,
            'form_id_optional': form_id,
            'due_from_date': from_date,
            'due_to_date': to_date,
            'csv': csv,
            'from_count': from_count,
            'page_count': page_count,
            'check_count': check_count
        }
    ];
    callerName = 'client_reports';
    clientApiRequest(callerName, request, callback);
}

/* Login Trace - updated*/
function getLoginTraceReportFilters(callback) {
    var request = [
        'GetLogintraceReportFilters', {}
    ];
    callerName = 'client_masters';
    clientApiRequest(callerName, request, callback);
}

function getLoginTraceReportData(user_id, from_date, to_date, csv, from_count, page_count, callback) {
    var request = [
        'GetLoginTraceReportData', {
            'user_id': user_id,
            'due_from_date': from_date,
            'due_to_date': to_date,
            'csv': csv,
            'from_count': from_count,
            'page_count': page_count
        }
    ];
    callerName = 'client_masters';
    clientApiRequest(callerName, request, callback);
}

/* View Profile */
function getUserProfile(callback) {
    var request = [
        'GetUserProfile', {}
    ];
    callerName = 'client_masters';
    clientApiRequest(callerName, request, callback);
}

function updateUserProfile(user_id, emailId, c_no, m_no, address, employee_code, employee_name, callback) {
    var request = [
        'UpdateUserProfile', {
            'user_id': user_id,
            'email_id': emailId,
            'con_no': c_no,
            'mob_no': m_no,
            'address': address,
            'emp_code': employee_code,
            'emp_name': employee_name
        }
    ];
    callerName = 'client_masters';
    clientApiRequest(callerName, request, callback);
}

// Reassign Compliance Filter Start
function getReassignComplianceFilters(le_id, callback) {
    var request = [
        'GetReassignComplianceFilters', {
            'le_id': le_id
        }
    ];
    callerName = 'client_transaction';
    clientApiRequest(callerName, request, callback);
}


// User Management Prerequisite
function getUserManagement_Prerequisite(callback) {
    callerName = 'client_masters';
    var request = [
        'UserManagementPrerequisite',
        {}
    ];
    clientApiRequest(callerName, request, callback);
}

// User Management List
function getUserManagement_List(callback) {
    callerName = 'client_masters';
    var request = [
        'UserManagementList',
        {}
    ];
    clientApiRequest(callerName, request, callback);
}

// User Management Edit View
function userManagementEditView(user_id, callback) {
    callerName = 'client_masters';
    var request = [
        'UserManagementEditView', {
            'user_id': user_id
        }
    ];
    clientApiRequest(callerName, request, callback);
}

function getReAssignComplianceUnits(legalEntityId, domainId, userId, userType, unitId, callback) {
    var request = [
        'GetReAssignComplianceUnits', {
            'le_id': legalEntityId,
            'd_id': domainId,
            'usr_id': userId,
            'user_type_id': userType,
            'unit_id': unitId
        }
    ];
    callerName = 'client_transaction';
    clientApiRequest(callerName, request, callback);
}

function getReAssignComplianceForUnits(legalEntityId, domainId, userId, userType, unitIds, recordCount, callback) {
    var request = [
        'GetReAssignComplianceForUnits', {
            'le_id': legalEntityId,
            'd_id': domainId,
            'usr_id': userId,
            'user_type_id': userType,
            'u_ids': unitIds,
            'r_count': recordCount
        }
    ];
    var callerName = 'client_transaction';
    clientApiRequest(callerName, request, callback);
}

// function saveReviewSettingsComplianceDict(
//     compliance_id, le_id, d_id, f_type, units, repeat_by, repeat_type_id, due_date, trigger_before_days,
//     statu_dates, old_repeat_by, old_repeat_type_id, old_due_date, old_statu_dates
// ) {
//     return {
//         'comp_id': compliance_id,
//         'le_id': le_id,
//         'd_id': d_id,
//         'f_id': f_type,
//         'unit_ids': units,
//         'repeat_by': repeat_by,
//         'repeat_type_id': repeat_type_id,
//         'due_date': due_date,
//         'trigger_before_days': trigger_before_days,
//         'statu_dates': statu_dates,
//         'old_repeat_by': old_repeat_by,
//         'old_repeat_type_id': old_repeat_type_id,
//         'old_due_date': old_due_date,
//         'old_statu_dates': old_statu_dates,
//     };
// }
// Widget api call begin
function getUserWidgetData(callback) {
    var request = [
        "GetUserWidgetData", {}
    ];
    callerName = "client_master_filters";
    clientApiRequest(callerName, request, callback);
}

function saveUserWidgetDataDict(w_id, width, height, pinstatus) {
    return {
        "w_id": w_id,
        "width": width,
        "height": height,
        "pin_status": pinstatus
    }
}

function saveUserWidgetData(widget_info, callback) {
    var request = [
        "SaveWidgetData", {
            "widget_info": widget_info
        }
    ];
    callerName = "client_master_filters";
    clientApiRequest(callerName, request, callback);
}

function getWidgetComplianceChart(le_ids, callback) {
    var request = [
        "GetComplianceChart", {
            "le_ids": le_ids
        }
    ];
    callerName = "widgets";
    clientApiRequest(callerName, request, callback);
}

function getWidgetEscalationChart(le_ids, callback) {
    var request = [
        "GetEscalationChart", {
            "le_ids": le_ids
        }
    ];
    callerName = "widgets";
    clientApiRequest(callerName, request, callback);
}

function getWidgetNotCompliedChart(le_ids, callback) {
    var request = [
        "GetNotCompliedChart", {
            "le_ids": le_ids
        }
    ];
    callerName = "widgets";
    clientApiRequest(callerName, request, callback);
}


function getWidgetRiskChart(le_ids, callback) {
    var request = [
        "GetRiskChart", {
            "le_ids": le_ids
        }
    ];
    callerName = "widgets";
    clientApiRequest(callerName, request, callback);
}

function getWidgetTrendChart(le_ids, callback) {
    var request = [
        "GetTrendChart", {
            "le_ids": le_ids
        }
    ];
    callerName = "widgets";
    clientApiRequest(callerName, request, callback);
}

function getWidgetCalender(le_ids, callback) {
    var request = [
        "GetCalendarView", {
            "le_ids": le_ids
        }
    ];
    callerName = "widgets";
    clientApiRequest(callerName, request, callback);
}

function getCalenderView(le_id, unit_id, cal_date, callback) {
    var request = [
        "GetCalendarView", {
            "le_id": le_id,
            "unit_id": unit_id,
            "cal_date": cal_date
        }
    ];
    callerName = 'client_user';
    clientApiRequest(callerName, request, callback);
}

function getWidgetUserScoreCard(le_ids, callback) {
    var request = [
        "GetUserScoreCard", {
            "le_ids": le_ids
        }
    ];
    callerName = "widgets";
    clientApiRequest(callerName, request, callback);
}

function getWidgetDomainScoreCard(le_ids, callback) {
    var le_idsarray;
    if (le_ids.length == 0) {
        le_idsarray = getLEids();
    } else {
        le_idsarray = le_ids;
    }
    var request = [
        "GetDomainScoreCard", {
            "le_ids": le_idsarray
        }
    ];
    callerName = "widgets";
    clientApiRequest(callerName, request, callback);
}
// Widget api call end

/* Risk report - updated*/
function getRiskReportFilters(country_id, business_group_id, le_id, callback) {
    var request = [
        'GetRiskReportFilters', {
            'country_id': country_id,
            'business_group_id': business_group_id,
            'legal_entity_id': le_id
        }
    ];
    callerName = 'client_reports';
    clientApiRequest(callerName, request, callback);
}

function getRiskReportData(
    country_id, business_group_id, legal_entity_id, domain_id, division_id,
    category_id, unit_id, statutory_mapping, compliance_id,
    task_status, csv, from_count, page_count, callback
) {
    var request = [
        'GetRiskReportData', {
            'country_id': country_id,
            'business_group_id': business_group_id,
            'legal_entity_id': legal_entity_id,
            'domain_id': domain_id,
            'division_id': division_id,
            'category_id': category_id,
            'unit_id': unit_id,
            'statutory_mapping': statutory_mapping,
            'compliance_id': compliance_id,
            'task_status': task_status,
            'csv': csv,
            'from_count': from_count,
            'page_count': page_count
        }
    ];
    callerName = 'client_reports';
    clientApiRequest(callerName, request, callback);
}

function changeStatutorySettingsLock(
    le_id, d_id, u_id, lock, password, callback
) {
    var request = [
        'ChangeStatutorySettingsLock', {
            'le_id': le_id,
            'd_id': d_id,
            'u_id': u_id,
            'lock': lock,
            'password': password
        }
    ];
    callerName = 'client_transaction';
    clientApiRequest(callerName, request, callback);
}

function changeThemes(theme, callback) {
    var request = [
        "ChangeThemes", {
            "theme": theme
        }
    ];
    callerName = "client_master_filters";
    clientApiRequest(callerName, request, callback);
}

function getSettingsFormDetails(le_id, callback) {
    var request = [
        'GetSettingsFormDetails', {
            'legal_entity_id': le_id
        }
    ];
    callerName = 'client_user';
    clientApiRequest(callerName, request, callback);
}

function saveSettingsFormDetails(le_id, le_name, app_opt, ass_rem, esc_rem_adv, esc_rem, reassign_sp, callback) {
    var request = [
        'SaveSettingsFormDetails', {
            'legal_entity_id': le_id,
            'legal_entity_name': le_name,
            'two_level_approve': app_opt,
            'assignee_reminder': ass_rem,
            'advance_escalation_reminder': esc_rem_adv,
            'escalation_reminder': esc_rem,
            'reassign_sp': reassign_sp
        }
    ];
    callerName = 'client_user';
    clientApiRequest(callerName, request, callback);
}

function DownloadApiRequest(request) {
    var sessionToken = getSessionToken();
    var requestFrame = {
        'session_token': sessionToken,
        'request': request
    };
    var body = [
        sessionToken,
        requestFrame
    ];
    actula_data = toJSON(body);
    var saveData = (function() {
        var a = document.createElement("a");
        document.body.appendChild(a);
        a.style = "display: none";
        return function(data, fileName) {
            url = 'data:application/octet-stream;base64,' + data;
            a.href = url;
            a.download = fileName;
            a.click();
            window.URL.revokeObjectURL(url);

        };
    }());

    $.ajax({
        xhr: function() {
            var xhr = new window.XMLHttpRequest();

            xhr.onreadystatechange = function() {
                if (this.readyState == 4 && this.status == 200) {
                    var data = this.response;
                    // data = atob(data);
                    var fileName = this.getResponseHeader('filename');
                    saveData(data, fileName);
                }
            }
            return xhr;
        },
        url: '/api/files',
        headers: { 'X-Xsrftoken': getCookie('_xsrf'), 'Caller-Name': window.location.pathname },
        type: 'POST',
        crossDomain: true,
        data: makekey() + btoa(actula_data),
        processData: false,
        contentType: false,

    });
}

function downloadTaskFile(le_id, c_id, d_id, u_id, start_date, file_name) {
    // console.log(le_id + "--" + c_id + "--" + d_id + "--" + u_id + "--" + start_date + "--" + file_name);
    var request = [
        "DownloadFile", {
            "le_id": le_id,
            "c_id": c_id,
            "d_id": d_id,
            "u_id": u_id,
            "start_date": start_date,
            "file_name": file_name,
        }
    ];
    DownloadApiRequest(request);
}


function uploadComplianceTaskFile(le_id, c_id, d_id, u_id, start_date, file_info, callback) {
    var request = [
        'UploadComplianceTaskFile', {
            "le_id": le_id,
            "c_id": c_id,
            "d_id": d_id,
            "u_id": u_id,
            "start_date": start_date,
            "file_info": file_info
        }
    ];
    callerName = 'files';
    clientApiRequest(callerName, request, callback);
}


function removeUploadedTaskFile(le_id, c_id, d_id, u_id, start_date, file_info) {
    var request = [
        'RemoveFile', {
            "le_id": le_id,
            "c_id": c_id,
            "d_id": d_id,
            "u_id": u_id,
            "start_date": start_date,
            "file_info": file_info
        }
    ];
    callerName = 'files';
    clientApiRequest(callerName, request, callback);
}


function ConvertToCSV(objArray) {
    var array = typeof objArray != 'object' ? JSON.parse(objArray) : objArray;
    // var lblarray = typeof lblsArray != 'object' ? JSON.parse(lblsArray) : lblsArray;

    var str = '';

    function makecsv(objContent) {
        for (var i = 0; i < objContent.length; i++) {
            var line = '';
            for (var index in objContent[i]) {
                if (line != '') line += ','

                line += objContent[i][index];
            }
            str += line + '\r\n';
        }
        return str;
    }
    // str += makecsv(lblarray);
    str += makecsv(array);

    console.log(str);
    return str;
}

function exportJsontoCsv(data, fileName) {

    var jsonObject = JSON.stringify(data);

    csv_data = ConvertToCSV(jsonObject);
    csv_data = btoa(csv_data);
    var a = document.createElement("a");
    document.body.appendChild(a);
    a.style = "display: none";
    url = 'data:application/octet-stream;base64,' + csv_data;
    a["href"] = url;
    a.download = fileName + ".csv";
    a.click();
    window.URL.revokeObjectURL(url);
}

function getCurrentDateTime(callback) {

    callerName = "now";
    $.ajax({
        url: CLIENT_BASE_URL + callerName,
        type: 'GET',
        success: function(data) {
            callback(data)
        },
        error: function(jqXHR, textStatus, errorThrown) {

        }
    });
}
