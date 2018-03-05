// var BASE_URL = "http://127.0.0.1:8082/";
var BASE_URL = '/knowledge/api/';
var login_url = '/knowledge/login';
var csrf_token = $('meta[name=csrf-token]').attr('content')
var my_ip = null;


var DEBUG = true;

function log() {
    if (window.console) {
        console.log.apply(console, arguments);
    }
}
// if (window.sessionStorage["my_ip"] == null){
//     get_ip();
// }
function toJSON(data) {
    return JSON.stringify(data, null, ' ');
}

function parseJSON(data) {
    return JSON.parse(data);
}

function initSession(userProfile) {
    window.sessionStorage.userInfo = toJSON(userProfile);
}

function getShortName() {
    var pathArray = window.location.pathname.split('/');
    if (typeof pathArray[2] === 'undefined') {
        return null;
    } else {
        return pathArray[2];
    }
}

function getBaseUrl() {
    return BASE_URL;
}
// function updateUser_Session(user) {
//     var info = parseJSON(window.sessionStorage["userInfo"])
//     delete window.sessionStorage["userInfo"];
//     info.userProfile = user;
//     window.sessionStorage["userInfo"] = toJSON(info);
// }
function clearSession() {
    delete window.sessionStorage.userInfo;
    delete window.sessionStorage.MESSAGES;
    delete window.sessionStorage.statutory_count;
    delete window.sessionStorage.messages_count;
}

function getUserInfo() {
    var info = window.sessionStorage.userInfo;
    if (typeof info === 'undefined') {
        user = null;
    } else {
        user = JSON.parse(info);
    }
    return user;
}

function updateUserInfo(response) {
    var info = getUserInfo();
    info.contact_no = response.contact_no;
    info.address = response.address;
    info.mobile_no = response.mobile_no;
    info.email_id = response.email_id;
    window.sessionStorage.userInfo = toJSON(info);
}
function getLegalEntityDict(leId, leName) {
  return {
    'le_id': leId,
    'le_name': leName
  };
}
function getDivisionDict(dv_id, dv_name, cg, div_cnt, unit_cnt) {
  return {
    'dv_id': dv_id,
    'dv_name': dv_name,
    'cg': cg,
    'div_cnt': div_cnt,
    'unit_cnt': unit_cnt
  };
}
function getDiviCatgDict(cId, bg_id, le_id, dv_id, dv_name, cg) {
  return {
    'cl_id': cId,
    'bg_id': bg_id,
    'le_id': le_id,
    'dv_id': dv_id,
    'dv_name': dv_name,
    'cg': cg
  };
}

function getUnitDict(uId, uName, uCode, uAdd, pCode, geoId, dIds, iIds, status) {
    return {
        'unit_id': uId,
        'unit_name': uName,
        'unit_code': uCode,
        'address': uAdd,
        'postal_code': pCode,
        'geography_id': geoId,
        'd_ids': dIds,
        'i_ids_list': iIds,
        'is_approved': status
    };
}
function mapUnitsToCountry(cId, units) {
  return {
    'c_id': cId,
    'units': units
  };
}
function saveClient(cId, bg_id, le_id, c_id, division_units, cw_units, division_dict, callback) {
  callerName = 'techno';
  var request = [
    'SaveClient',
    {
      'cl_id': cId,
      'bg_id': bg_id,
      'le_id': le_id,
      'c_id': c_id,
      'division_units': division_units,
      'units': cw_units,
      'division_category': division_dict
    }
  ];
  apiRequest(callerName, request, callback);
}
function saveDivisionCategory(division_dict, callback) {
  callerName = 'techno';
  var request = [
      'SaveDivisionCategory',
      {
       'division_category': division_dict
      }
  ];
  apiRequest(callerName, request, callback);
}
function updateClient(cId, bg, le, d, cwUnits, callback) {
  callerName = 'techno';
  var request = [
    'UpdateClient',
    {
      'c_id': cId,
      'bg': bg,
      'le': le,
      'd': d,
      'cw_units': cwUnits
    }
  ];
  apiRequest(callerName, request, callback);
}
function changeClientStatus(clientId, legalEntityId, divisionId, isActive, callback) {
  callerName = 'techno';
  var request = [
    'ChangeClientStatus',
    {
      'client_id': clientId,
      'legal_entity_id': legalEntityId,
      'division_id': divisionId,
      'is_active': isActive
    }
  ];
  apiRequest(callerName, request, callback);
}
function reactivateUnit(clientId, unitId, password, callback) {
  callerName = 'techno';
  var request = [
    'ReactivateUnit',
    {
      'client_id': clientId,
      'unit_id': unitId,
      'password': password
    }
  ];
  apiRequest(callerName, request, callback);
}
//Client Profile
function getClientProfile(callback) {
  callerName = 'techno';
  var request = [
    'GetClientProfile',
    {}
  ];
  apiRequest(callerName, request, callback);
}
// Client Details Report
function getClientDetailsReportFilters(callback) {
  callerName = 'techno_report';
  var request = [
    'GetClientDetailsReportFilters',
    {}
  ];
  apiRequest(callerName, request, callback);
}
function getClientDetailsReport(countryId, clientId, businessGroupId, legalEntityId, divisionId, unitId, domainIds, start_count, callback) {
  callerName = 'techno_report';
  var request = [
    'GetClientDetailsReportData',
    {
      'country_id': countryId,
      'group_id': clientId,
      'business_group_id': businessGroupId,
      'legal_entity_id': legalEntityId,
      'division_id': divisionId,
      'unit_id': unitId,
      'domain_ids': domainIds,
      'start_count': start_count
    }
  ];
  apiRequest(callerName, request, callback);
}
function exportClientDetailsReportData(countryId, clientId, legalEntityId, csv, u_m_none, callback){
  callerName = 'techno_report';
  var request = [
    'ExportClientDetailsReportData',
    {
      'country_id': countryId,
      'client_id': clientId,
      'legal_entity_id': legalEntityId,
      'csv': csv,
      'u_m_none': u_m_none
    }
  ];
  apiRequest(callerName, request, callback);
}
function getClientDetailsReportData(countryId, clientId, legalEntityId, u_m_none, callback){
  callerName = 'techno_report';
  var request = [
    'GetClientDetailsReportData',
    {
      'country_id': countryId,
      'client_id': clientId,
      'legal_entity_id': legalEntityId,
      'u_m_none': u_m_none
    }
  ];
  apiRequest(callerName, request, callback);
}
//Statutory Notifications List
function getStatutoryNotificationsFilters(callback) {
  callerName = 'techno_report';
  var request = [
    'GetStatutoryNotificationsFilters',
    {}
  ];
  apiRequest(callerName, request, callback);
}
function getStatutoryNotificationsReportData(countryId, domainId, level1Id, fromDate, toDate, from_count, page_count, callback) {
  callerName = 'techno_report';
  var request = [
    'GetStatutoryNotificationsReportData',
    {
      'country_id': countryId,
      'domain_id': domainId,
      'statutory_id_optional': level1Id,
      'from_date_optional': fromDate,
      'to_date_optional': toDate,
      'from_count': from_count,
      'page_count': page_count
    }
  ];
  apiRequest(callerName, request, callback);
}
function getAssignedStatutoryReportFilters(callback) {
  var request = [
    'GetAssignedStatutoryReportFilters',
    {}
  ];
  callerName = 'techno_report';
  apiRequest(callerName, request, callback);
}
function getAssignedStatutoryReport(cId, dId, clientId, bGroupId, lEntityId, statutoryval, uId, c_task, csv, from_count, page_count, callback) {
  var request = [
    'GetAssignedStatutoryReport',
    {
      'c_id': cId,
      'domain_id_optional': dId,
      'client_id': clientId,
      'bg_id': bGroupId,
      'le_id': lEntityId,
      'map_text': statutoryval,
      'unit_id': uId,
      'c_task': c_task,
      'csv': csv,
      'from_count': from_count,
      'page_count': page_count
    }
  ];
  callerName = 'techno_report';
  apiRequest(callerName, request, callback);
}

function getAuditTrail(
  fromDate, toDate, userId, formId, categoryId, client_id, legal_entity_id,
  unit_id, recordCount, pageCount, callback) {
    callerName = 'general';
    var request = [
        'GetAuditTrails', {
            'from_date': fromDate,
            'to_date': toDate,
            'user_id_search': userId,
            'form_id_search': formId,
            'category_id': categoryId,
            'client_id': client_id,
            'legal_entity_id': legal_entity_id,
            'unit_id': unit_id,
            'record_count': recordCount,
            'page_count': pageCount
        }
    ];
    apiRequest(callerName, request, callback);
}

function exportAuditTrail(
  fromDate, toDate, userId, formId, categoryId,
  client_id, legal_entity_id, unit_id,
  csv, callback) {
  callerName = 'general';
  var request = [
    'ExportAuditTrails',
    {
      'from_date': fromDate,
      'to_date': toDate,
      'user_id_search': userId,
      'form_id_search': formId,
      'category_id': categoryId,
      'client_id': client_id,
      'legal_entity_id': legal_entity_id,
      'unit_id': unit_id,
      'csv': csv
    }
  ];
  apiRequest(callerName, request, callback);
}

function getAuditTrailFilter(callback) {
  callerName = 'general';
  var request = [
    'GetAuditTrailsFilter',
    {}
  ];
  apiRequest(callerName, request, callback);
}

function updateUserProfile(contact_no, address, mobile_no, email_id, callback) {
  callerName = 'general';
  var request = [
    'UpdateUserProfile',
    {
      'contact_no': contact_no,
      'address': address,
      'mobile_no': mobile_no,
      'email_id': email_id
    }
  ];
  apiRequest(callerName, request, callback);
}
/* Notifications */
function getNotifications(notification_type, callback) {
  callerName = 'general';
  var request = [
    'GetNotifications',
    { 'notification_type': notification_type }
  ];
  apiRequest(callerName, request, callback);
}
function updateNotificationStatus(notification_id, has_read, callback) {
  callerName = 'general';
  var request = [
    'UpdateNotificationStatus',
    {
      'notification_id': notification_id,
      'has_read': has_read
    }
  ];
  apiRequest(callerName, request, callback);
}
function createNewAdmin(user_id, client_id, old_admin_id, employee_name, callback) {
  callerName = 'techno';
  var request = [
    'CreateNewAdmin',
    {
      'new_admin_id': user_id,
      'client_id': client_id,
      'old_admin_id': old_admin_id,
      'username': employee_name
    }
  ];
  apiRequest(callerName, request, callback);
}
function getValidityDateList(callback){
  callerName = 'admin';
  var request = [
    'GetValidityDateList',
    {}
  ];
  apiRequest(callerName, request, callback);
}
function get_validity_day_setting(
  validity_days_id, country_id, domain_id, validity_days
){
    if(!validity_days_id){
      validity_days_id = null;
    }
    return {
      "validity_days_id": validity_days_id,
      "country_id": country_id,
      "domain_id": domain_id,
      "validity_days": validity_days
    }
}

function saveValidityDateSettings(
  validity_date_settings, callback
){
  callerName = "admin";
  var request = [
    'SaveValidityDateSettings',
    {
      "validity_date_settings": validity_date_settings
    }
  ];
  apiRequest(callerName, request, callback);
}

function progress(percent, $element) {
  var progressBarWidth = percent * $element.width() / 100;
  $('.upload-progress-count').html("Uploading " + percent + "% ");
  //$element.find('div').animate({ width: progressBarWidth }, 500).html(percent + "% ");
}

function getUserProfile() {
    var info = getUserInfo();
    var userDetails = {
        'user_id': info.user_id,
        'client_id': info.client_id,
        'user_group': info.user_group_name,
        'employee_name': info.employee_name,
        'employee_code': info.employee_code,
        'email_id': info.email_id,
        'contact_no': info.contact_no,
        'mobile_no': info.mobile_no,
        'address': info.address,
        'designation': info.designation,
        'user_name': info.username
    };
    return userDetails;
}

function getSessionToken() {
    var info = getUserInfo();
    if (info !== null)
        return info.session_token;
    else
        return null;
}

function getDatabaseServerList(callback){
  callerName = 'console_admin';
  var request = [
    'GetDatabaseServerList',
    {
    }
  ];
  apiRequest(callerName, request, callback);
}

function saveDBServer(
  db_server_id, db_server_name, ip, port, username, password, callback
){
  callerName = "console_admin"
  var request = [
    "SaveDBServer",
    {
      "db_server_id": db_server_id,
      "db_server_name": db_server_name,
      "ip": ip,
      "port": port,
      "username": username,
      "password": password
    }
  ];
  apiRequest(callerName, request, callback)
}
function getClientServerList(callback){
  callerName = 'console_admin';
  var request = [
    'GetClientServerList',
    {
    }
  ];
  apiRequest(callerName, request, callback);
}
function saveClientServer(
  client_server_id, client_server_name, ip, port, callback
){
  callerName = "console_admin";
  var request = [
    "SaveClientServer",
    {
      "client_server_id": client_server_id,
      "client_server_name": client_server_name,
      "ip": ip,
      "port": port
    }
  ];
  apiRequest(callerName, request, callback);
}
function getFileServerList(callback){
  callerName = 'console_admin';
  var request = [
    'GetFileServerList',
    {
    }
  ];
  apiRequest(callerName, request, callback);
}
function fileServerEntry(
  file_server_id, file_server_name, ip, port, callback
){
  callerName = "console_admin";
  var request = [
    "SaveFileServer",
    {
      "file_server_id": file_server_id,
      "file_server_name": file_server_name,
      "ip": ip,
      "port": port
    }
  ];
  apiRequest(callerName, request, callback);
}
function getAllocatedDBEnv(callback){
    callerName = "console_admin";
    var request = [
      "GetAllocatedDBEnv",
      {}
    ];
    apiRequest(callerName, request, callback);
}
function saveDBEnv(
  client_db_id, client_id, le_id, machine_id, db_server_id, le_db_server_id, file_server_id,
  cl_ids, le_ids, f_le_ids, le_le_ids, old_grp_app_id, old_grp_db_s_id, old_le_db_s_id, old_le_f_s_id,
  new_cl_ids, new_grp_le_ids, new_le_le_ids, new_le_f_s_ids, callback
){
    callerName = "console_admin";
    var request = [
        "SaveAllocatedDBEnv",
        {
          "client_database_id": client_db_id,
          "client_id": client_id,
          "legal_entity_id": le_id,
          "machine_id": machine_id,
          "db_server_id": db_server_id,
          "le_db_server_id": le_db_server_id,
          "file_server_id": file_server_id,
          "console_cl_ids": cl_ids,
          "console_le_ids": le_ids,
          "console_f_le_ids": f_le_ids,
          "console_le_le_ids": le_le_ids,
          "old_grp_app_id": old_grp_app_id,
          "old_grp_db_s_id": old_grp_db_s_id,
          "old_le_db_s_id": old_le_db_s_id,
          "old_le_f_s_id": old_le_f_s_id,
          "new_cl_ids": new_cl_ids,
          "new_grp_le_ids": new_grp_le_ids,
          "new_le_le_ids": new_le_le_ids,
          "new_le_f_s_ids": new_le_f_s_ids
        }
    ];
    apiRequest(callerName, request, callback);
}
function getFileStorage(callback){
    callerName = "console_admin";
    var request = [
      "GetFileStorage",
      {}
    ];
    apiRequest(callerName, request, callback);
}
function saveFileStorage(client_id, le_id, machine_id, callback){
    callerName = "console_admin";
    var request = [
        "SaveFileStorage",
        {
          "client_id": client_id,
          "legal_entity_id": le_id,
          "machine_id": machine_id
        }
    ];
    apiRequest(callerName, request, callback);
}
function getAutoDeletionList(callback){
    callerName = "console_admin";
    var request = [
      "GetAutoDeletionList",
      {}
    ];
    apiRequest(callerName, request, callback);
}

function saveAutoDeletion(auto_deletion_details, callback){
    callerName = "console_admin";
    var request = [
      "SaveAutoDeletion",
      {
        "auto_deletion_details": auto_deletion_details
      }
    ];
    apiRequest(callerName, request, callback);
}


function getUnassignedUnitsList(callback){
  callerName = "techno";
  var request = [
    "GetUnassignedUnits",
    {}
  ];
  apiRequest(callerName, request, callback);
}
function getAssignedUnitsList(domain_id, client_id, legal_entity_id, callback){
  callerName = "techno";
  var request = [
    "GetAssignedUnits",
    {
      "domain_id": domain_id,
      "client_id": client_id,
      "legal_entity_id": legal_entity_id
    }
  ];
  apiRequest(callerName, request, callback);
}
function getAssignedUnitDetails(legal_entity_id, domain_manager_id, client_id, domain_id, callback){
  callerName = "techno";
  var request = [
    "GetAssignedUnitDetails",
    {
      "legal_entity_id": legal_entity_id,
      "user_id": domain_manager_id,
      "client_id": client_id,
      "domain_id": domain_id
    }
  ];
  apiRequest(callerName, request, callback);
}
function getAssignUnitFormData(domain_id, client_id, legal_entity_id, callback){
  callerName = "techno";
  var request = [
    "GetAssignUnitFormData",
    {
      "domain_id": domain_id,
      "client_id": client_id,
      "legal_entity_id": legal_entity_id
    }
  ];
  apiRequest(callerName, request, callback);
}
function saveAssignedUnits(client_id, user_id, active_units, callback){
    callerName = "techno";
    var request = [
      "SaveAsssignedUnits",
      {
        "user_id": user_id,
        "active_units": active_units,
        "client_id": client_id
      }
    ];
    apiRequest(callerName, request, callback);
}

function getUserMenu() {
    var info = getUserInfo();
    if (info != null) {
        return info.menu.menus;
    } else {
        frm = window.location.href;
    }
}

function getPageUrl() {
    page_urls = [];
    ac_menu = getUserMenu();
    if (ac_menu == undefined) {
        return page_urls;
    }
    keys = Object.keys(ac_menu);
    for (var k = 0; k < keys.length; k++) {
        key = keys[k];
        objs = ac_menu[key];
        for (var ob = 0; ob < objs.length; ob++) {
            data = objs[ob];
            page_urls.push(data.form_url);
        }
    }
    page_urls.push('/knowledge/home');
    page_urls.push('/knowledge/profile');
    page_urls.push('/knowledge/change-password');
    return page_urls;
}

function getEmployeeName() {
    var info = getUserInfo();
    if (info !== null)
        return info.employee_name;
    else
        return null;
}

function getAssignedStatutoriesById(u_id, d_id, rcount, callback){
  callerName = 'domain_transaction';
  var request = [
      "GetAssignedStatutoriesById",
      {
        "u_id": u_id,
        "d_id": d_id,
        "rcount": rcount
      }
    ];
  apiRequest(callerName, request, callback);
}

//user mapping report

function getUsermappingDetailsReport(countryId, clientId, legalEntityId, u_m_none, csv, from_count, page_count, callback) {
  callerName = 'techno_report';
  var request = [
    'GetUserMappingDetailsReportData',
    {
      'country_id': countryId,
      'client_id': clientId,
      'legal_entity_id': legalEntityId,
      'u_m_none': u_m_none,
      'csv': csv,
      'from_count': from_count,
      'page_count': page_count
    }
  ];
  apiRequest(callerName, request, callback);
}

function getGroupAdminGroupList(callback)
{
  console.log("mirror")
  callerName = 'techno_transaction';
  var request = [
    'GetGroupAdminGroupUnitList',
    {}
  ];
  apiRequest(callerName, request, callback);
}

function resendGroupAdminRegnmail(clientInfo, callback) {
  var request = ['ResendGroupAdminRegnMail', clientInfo];
  apiRequest("techno_transaction", request, callback);
}

function sendGroupAdminRegnmail(clientInfo, callback) {
  var request = ['SendGroupAdminRegnMail', clientInfo];
  apiRequest("techno_transaction", request, callback);
}

function getGroupAdminReportData(callback){
  console.log("mirror")
  callerName = 'techno_report';
  var request = [
    'GetGroupAdminReportData',
    {}
  ];
  apiRequest(callerName, request, callback);
}

function exportGroupAdminReportData(cl_id, c_id, csv, callback){
  console.log("mirror")
  callerName = 'techno_report';
  var request = [
    'ExportGroupAdminReportData',
    {
      "client_id": cl_id,
      "country_id": c_id,
      "csv": csv
    }
  ];
  apiRequest(callerName, request, callback);
}

function getAssignedUserClientGroups(callback)
{
  console.log("mirror")
  callerName = 'techno_report';
  var request = [
    'GetAssignedUserClientGroups',
    {}
  ];
  apiRequest(callerName, request, callback);
}

function getReassignUserReportData(cg_id, u_id, g_id, callback)
{
  callerName = 'techno_report';
  var request = [
    'GetReassignUserReportData',
    {
      "user_category_id": cg_id,
      "user_id": u_id,
      "group_id_none": g_id
    }
  ];
  apiRequest(callerName, request, callback);
}
function exportReassignUserReportData(cg_id, u_id, g_id, u_m_none, csv, callback)
{
  callerName = 'techno_report';
  var request = [
    'ExportReassignUserReportData',
    {
      "user_category_id": cg_id,
      "user_id": u_id,
      "group_id_none": g_id,
      "u_m_none": u_m_none,
      "csv": csv
    }
  ];
  apiRequest(callerName, request, callback);
}
function getReassignUserDomainReportData(cg_id, u_id, g_id, bg_id, le_id, d_id, callback){
  callerName = 'techno_report';
  var request = [
    'GetReassignUserDomainReportData',
    {
      "user_category_id": cg_id,
      "user_id": u_id,
      "group_id_none": g_id,
      "bg_id": bg_id,
      "le_id": le_id,
      "d_id": d_id
    }
  ];
  apiRequest(callerName, request, callback);
}

function getLegalEntityClosureData(callback){
  callerName = 'techno_transaction';
  var request = [
    'GetLegalEntityClosureReportData',
    {}
  ];
  apiRequest(callerName, request, callback);
}

function saveLegalEntityClosureData(password, remarks, le_id, action_mode, callback)
{
  callerName = 'techno_transaction';
  var request = [
    'SaveLegalEntityClosureData',
    {
      "password": password,
      "closed_remarks": remarks,
      "legal_entity_id": le_id,
      "grp_mode": action_mode
    }
  ];
  apiRequest(callerName, request, callback);
}
//Verify Password
function verifyPassword(password, callback) {
  var request = [
    'VerifyPassword',
    {
      'password': password
    }
  ];
  apiRequest('general', request, callback);
}

// Client Agreement Master Report
function getClientAgreementReportFilters(callback) {
  callerName = 'techno_report';
  var request = [
      'GetClientAgreementReportFilters',
      {}
    ];
    apiRequest(callerName, request, callback);
}

function getClientAgreementReport(countryId, clientId, businessGroupId, legalEntityId, domainId, contractFrom, contractTo, csv, from_count, page_count, countryName, callback) {
  callerName = 'techno_report';
  var request = [
    'GetClientAgreementReportData',
    {
      'country_id': countryId,
      'client_id': clientId,
      'business_group_id': businessGroupId,
      'legal_entity_id': legalEntityId,
      'domain_id_optional': domainId,
      'contract_from_optional': contractFrom,
      'contract_to_optional': contractTo,
      'csv': csv,
      'from_count': from_count,
      'page_count': page_count,
      'country_name': countryName        }
  ];
  apiRequest(callerName, request, callback);
}

function getDomainwiseAgreementReport(countryId, clientId, businessGroupId, legalEntityId, domainId, contractFrom, contractTo, csv, from_count, page_count, countryName, domainName, callback) {
  callerName = 'techno_report';
  var request = [
    'GetDomainwiseAgreementReportData',
    {
      'country_id': countryId,
      'client_id': clientId,
      'business_group_id': businessGroupId,
      'legal_entity_id': legalEntityId,
      'domain_id': domainId,
      'contract_from_optional': contractFrom,
      'contract_to_optional': contractTo,
      'csv': csv,
      'from_count': from_count,
      'page_count': page_count,
      'country_name': countryName,
      'domain_name': domainName
    }
  ];
  apiRequest(callerName, request, callback);
}

function getOrganizationWiseUnitCount(legalEntityId, domainId, callback) {
  callerName = 'techno_report';
  var request = [
    'GetOrganizationWiseUnitCount',
    {
      'legal_entity_id': legalEntityId,
      'domain_id': domainId
    }
  ];
  apiRequest(callerName, request, callback);
}

/* Messages */
function getMessages(from_count, page_count, callback) {
  callerName = 'general';
  var request = [
    'GetMessages',
    {
      'from_count': from_count,
      'page_count': page_count
    }
  ];
  apiRequest(callerName, request, callback);
}

function updateMessageStatus(message_id, has_read, callback) {
  callerName = 'general';
  var request = [
    'UpdateMessageStatus',
    {
      'message_id': message_id,
      'has_read': has_read
    }
  ];
  apiRequest(callerName, request, callback);
}

/* Messages */
function getStatutoryNotifications(from_count, page_count, callback) {
  callerName = 'general';
  var request = [
    'GetStatutoryNotifications',
    {
      'from_count': from_count,
      'page_count': page_count
    }
  ];
  apiRequest(callerName, request, callback);
}

function updateStatutoryNotificationStatus(notification_id, user_id, has_read, callback) {
  callerName = 'general';
  var request = [
    'UpdateStatutoryNotificationStatus',
    {
      'notification_id': notification_id,
      'user_id': user_id,
      'has_read': has_read
    }
  ];
  apiRequest(callerName, request, callback);
}

function getAssignedStatutoriesList(callback) {
  var request = [
    'GetAssignedStatutoriesList',
    {}
  ];
  apiRequest('techno_report', request, callback);
}

function getComplianceStatutoriesList(unitId, domainId, callback){
  var request = [
    'GetComplianceStatutoriesList',
    {
      'unit_id': unitId,
      'd_id': domainId
    }
  ];
  apiRequest("techno_report", request, callback);
}


function getUserId() {
    var info = getUserInfo();
    if (info !== null)
        return info.user_id;
    else
        return null;
}

function local_session_timeout() {
    var myVar = setInterval(function() { myTimer() }, 1000);
    var t = 0;

    function myTimer() {
        t += 1;
        console.log(t);
        if (t == 2) {
            clearInterval(myVar);
        }
    }
}

function get_ip() {
    $.getJSON('http://jsonip.com?callback=?', function(data) {
        window.sessionStorage.my_ip = data.ip;
    });
}

function getCookie(name) {
    var r = document.cookie.match('\\b' + name + '=([^;]*)\\b');
    return r ? r[1] : undefined;
}
function makekey()
{
    var text = "";
    var possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";

    for( var i=0; i < 5; i++ )
        text += possible.charAt(Math.floor(Math.random() * possible.length));
    return text;
}

function apiRequest(callerName, request, callback) {
    login_url = '/knowledge/login';
    var sessionToken = getSessionToken();
    var requestFrame = {
        'session_token': sessionToken,
        'request': request
    };
    actula_data = toJSON(requestFrame);
    if (callerName )
    $.ajax({
        url: BASE_URL + callerName,
        headers: { 'X-CSRFToken': csrf_token, 'Caller-Name': window.location.pathname},
        type: 'POST',
        contentType: 'application/json',
        data: makekey() + btoa(actula_data),
        success: function(data) {
            data = atob(data.substring(5));
            data = parseJSON(data);
            var status = data[0];
            var response = data[1];


            matchString = 'success';
            if (status.toLowerCase().indexOf(matchString) != -1) {
                if (status == 'UpdateUserProfileSuccess') {
                    updateUserInfo(response);
                }
                callback(null, response);
            } else if (status == 'InvalidSessionToken') {
                window.sessionStorage.login_url = login_url;
                clearSession();
                confirm_ok_alert(message[status], login_url);

            } else {
                if (Object.keys(response).length == 0)
                    callback(status, null);
                else
                    callback(status, response);
            }
        },
        error: function(jqXHR, textStatus, errorThrown) {
            rdata = parseJSON(jqXHR.responseText);
            rdata = atob(rdata.substring(5));
            callback(rdata, errorThrown); // alert("jqXHR:"+jqXHR.status);
        }
    });
}

function LoginApiRequest(callerName, request, callback) {
    $.ajax({
        url: BASE_URL + callerName,
        // headers: {'X-Xsrftoken' : getCookie('_xsrf')},
        headers: { 'X-CSRFToken': csrf_token, 'Caller-Name': window.location.pathname },
        type: 'POST',
        contentType: 'application/json',
        data: makekey() + btoa(toJSON(request)),
        success: function(data) {
            data = atob(data.substring(5));
            data = parseJSON(data);
            var status = data[0];
            var response = data[1];
            matchString = 'success';
            log('API STATUS :' + status);
            if (status.toLowerCase().indexOf(matchString) != -1) {
                callback(null, response);
            } else if (status == 'InvalidSessionToken') {
                window.sessionStorage.login_url = login_url;
                clearSession();
                confirm_ok_alert(message[status], login_url);
            }
            else {
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
// Login function
function verifyLoggedIn() {
    sessionToken = getSessionToken();
    if (sessionToken == null) {
        return false;
    } else
        return true;
}

function logout(callback) {
    sessionToken = getSessionToken();
    var request = [
        'Logout',
        { 'session_token': sessionToken }
    ];
    $.ajax({
        url: BASE_URL + 'login',
        headers: { 'X-CSRFToken': csrf_token, 'Caller-Name': window.location.pathname },
        // headers: {'X-Xsrftoken' : getCookie('_xsrf')},
        type: 'POST',
        contentType: 'application/json',
        data: makekey() + btoa(toJSON(request)),
        success: function(data) {
            data = atob(data.substring(5));
            data = parseJSON(data);
            var status = data[0];
            var response = data[1];
            console.log(status);
            console.log(response);
            matchString = 'success';
            clearSession();
            login_url = '/knowledge/login';
            window.sessionStorage.login_url = login_url;
            window.location.href = login_url;
        },
        error: function(jqXHR, textStatus, errorThrown) {
            rdata = parseJSON(jqXHR.responseText);
            rdata = atob(rdata.substring(5));
            callback(rdata.responseText);
        }
    });
}
//Domain Master
function saveDomain(dName, cIds, callback) {
    var request = [
        'SaveDomain', {
            'd_name': dName,
            'c_ids': cIds
        }
    ];
    apiRequest('general', request, callback);
}

function getAllocateServerReportData(callback){
  callerName = 'console_admin';
  var request = [
      "GetAllocateServerReportData",
      {}
    ];
  apiRequest(callerName, request, callback);
}

function updateDomain(dId, dName, cIds, callback) {
    var request = [
        'UpdateDomain', {
            'd_id': dId,
            'd_name': dName,
            'c_ids': cIds
        }
    ];
    apiRequest('general', request, callback);
}

function changeDomainStatus(dId, isActive, callback) {
    var request = [
        'ChangeDomainStatus', {
            'd_id': dId,
            'is_active': isActive
        }
    ];
    apiRequest('general', request, callback);
}

function getDomainList(callback) {
    var request = [
        'GetDomains',
        {}
    ];
    apiRequest('general', request, callback);
}

function getDomainReport(callback) {
    var request = [
        'GetDomainsReport',
        {}
    ];
    apiRequest('knowledge_report', request, callback);
}
//Country Master
function saveCountry(cName, callback) {
    var request = [
        'SaveCountry',
        { 'c_name': cName }
    ];
    apiRequest('general', request, callback);
}

function updateCountry(cId, cName, callback) {
    var request = [
        'UpdateCountry', {
            'c_id': cId,
            'c_name': cName
        }
    ];
    apiRequest('general', request, callback);
}

function changeCountryStatus(cId, isActive, callback) {
    var request = [
        'ChangeCountryStatus', {
            'c_id': cId,
            'is_active': isActive
        }
    ];
    apiRequest('general', request, callback);
}

function getCountryList(callback) {
    var request = [
        'GetCountries',
        {}
    ];
    apiRequest('general', request, callback);
}

function getCountryListForUser(callback) {
    var request = [
        'GetCountriesForUser',
        {}
    ];
    apiRequest('general', request, callback);
}

function getCountryReport(callback) {
    var request = [
        'GetCountriesReport',
        {}
    ];
    apiRequest('knowledge_report', request, callback);
}
//Industry Master
function getSaveIndustryDict(industryDetail) {
    var cIds = industryDetail[0];
    var dIds = industryDetail[1];
    var i_name = industryDetail[2];
    return {
        'c_id': cIds,
        'd_id': dIds,
        'i_name': i_name
    };
}

function saveIndustry(industryDetail, callback) {
    var request = [
        'SaveIndustry',
        industryDetail
    ];
    apiRequest('knowledge_master', request, callback);
}

function getUpdateIndustryDict(industryDetail) {
    var cIds = industryDetail[0];
    var dIds = industryDetail[1];
    var iIds = industryDetail[2];
    var iName = industryDetail[3];

    return {
        'c_id': cIds,
        'd_id': dIds,
        'i_id': iIds,
        'i_name': iName
    };
}

function updateIndustry(industryDetail, callback) {
    var request = [
        'UpdateIndustry',
        industryDetail
    ];
    apiRequest('knowledge_master', request, callback);
}

function changeIndustryStatus(iId, isActive, callback) {
    var request = [
        'ChangeIndustryStatus', {
            'i_id': iId,
            'is_active': isActive
        }
    ];
    apiRequest('knowledge_master', request, callback);
}

function getIndustryList(callback) {
    var request = [
        'GetIndustries',
        {}
    ];
    apiRequest('knowledge_master', request, callback);
}
//Statutory Nature Master
function getSaveStatutoryNatureDict(statutoryNatureDetail) {
    var cIds = statutoryNatureDetail[1];
    var s_n_name = statutoryNatureDetail[0];
    return {
        's_n_name': s_n_name,
        'c_id': cIds
    };
}

function saveStatutoryNature(statutoryNatureDetail, callback) {
    var request = [
        'SaveStatutoryNature',
        statutoryNatureDetail
    ];
    apiRequest('knowledge_master', request, callback);
}

function getUpdateStatutoryNatureDict(statutoryNatureDetail) {
    var snIds = statutoryNatureDetail[0];
    var snName = statutoryNatureDetail[1];
    var cIds = statutoryNatureDetail[2];
    return {
        's_n_id': snIds,
        's_n_name': snName,
        'c_id': cIds
    };
}

function updateStatutoryNature(statutoryNatureDetail, callback) {
    var request = [
        'UpdateStatutoryNature',
        statutoryNatureDetail
    ];
    apiRequest('knowledge_master', request, callback);
}

function changeStatutoryNatureStatus(sNId, isActive, callback) {
    var request = [
        'ChangeStatutoryNatureStatus', {
            's_n_id': sNId,
            'is_active': isActive
        }
    ];
    apiRequest('knowledge_master', request, callback);
}

function getStatutoryNatureList(callback) {
    var request = [
        'GetStatutoryNatures',
        {}
    ];
    apiRequest('knowledge_master', request, callback);
}
// Geography Levels
function getGeographyLevels(callback) {
    var request = [
        'GetGeographyLevels',
        {}
    ];
    apiRequest('knowledge_master', request, callback);
}

function levelDetails(lId, lPosition, lName, is_remove) {
    var level = {};
    level.l_id = lId;
    level.l_position = lPosition;
    level.l_name = lName;
    level.is_remove = is_remove;
    return level;
}

function saveAndUpdateGeographyLevels(cId, levels, insertValText, callback) {
    var request = [
        'SaveGeographyLevel', {
            'c_id': cId,
            'levels': levels,
            'insertValText': insertValText
        }
    ];
    apiRequest('knowledge_master', request, callback);
}
// Statutory Levels
function getStatutoryLevels(callback) {
    var request = [
        'GetStatutoryLevels',
        {}
    ];
    apiRequest('knowledge_master', request, callback);
}

function saveAndUpdateStatutoryLevels(cId, dId, levels, callback) {
    var request = [
        'SaveStatutoryLevel', {
            'c_id': cId,
            'd_id': dId,
            'levels': levels
        }
    ];
    apiRequest('knowledge_master', request, callback);
}
//Geographies
function getGeographies(callback) {
    var request = [
        'GetGeographies',
        {}
    ];
    apiRequest('knowledge_master', request, callback);
}

function saveGeography(lId, name, pIds, pNames, cId, callback) {
    var request = [
        'SaveGeography', {
            'g_l_id': lId,
            'g_name': name,
            'p_ids': pIds,
            'p_names': pNames,
            'c_id': cId
        }
    ];
    apiRequest('knowledge_master', request, callback);
}

function updateGeography(gId, lId, name, pIds, pNames, cId, callback) {
    var request = [
        'UpdateGeography', {
            'g_id': gId,
            'g_l_id': lId,
            'g_name': name,
            'p_ids': pIds,
            'p_names': pNames,
            'c_id': cId
        }
    ];
    apiRequest('knowledge_master', request, callback);
}

function changeGeographyStatus(gId, isActive, callback) {
    var request = [
        'ChangeGeographyStatus', {
            'g_id': gId,
            'is_active': isActive
        }
    ];
    apiRequest('knowledge_master', request, callback);
}

function getGeographyReport(callback) {
    var request = [
        'GetGeographyReport',
        {}
    ];
    apiRequest('knowledge_report', request, callback);
}
// statutory Mapping
function saveStatutory(dId, cId, lId, name, pIds, pNames, callback) {
    var request = [
        'SaveStatutory', {
            'c_id': cId,
            'd_id': dId,
            's_l_id': lId,
            's_name': name,
            's_pids': pIds,
            's_pnames': pNames
        }
    ];
    apiRequest('knowledge_master', request, callback);
}

function updateStatutory(dId, cId, sId, name, pIds, pNames, callback) {
    var request = [
        'UpdateStatutory', {
            'c_id': cId,
            'd_id': dId,
            's_id': sId,
            's_name': name,
            "s_pids": pIds,
            "s_pnames": pNames
        }
    ];
    apiRequest('knowledge_master', request, callback);
}

function statutoryDates(date, month, triggerBefore, repeatBy) {
    var statutoryDate = {};
    statutoryDate.statutory_date = date;
    statutoryDate.statutory_month = month;
    statutoryDate.trigger_before_days = triggerBefore;
    statutoryDate.repeat_by = repeatBy;
    return statutoryDate;
}

function uploadFileFormat(size, name, content) {
    return {
        'file_size': parseInt(size),
        'file_name': name,
        'file_content': content
    };
}

function convert_to_base64(file, callback) {
    var reader = new FileReader();
    reader.onload = function(readerEvt) {
        var binaryString = readerEvt.target.result;
        file_content = btoa(binaryString);
        callback(file_content);
    };
    reader.readAsBinaryString(file);
}

function uploadFile(fileListener, le_cnt, callback) {
    var evt = fileListener;
    max_limit = 1024 * 1024 * 50;
    // file max limit 50MB
    var files = evt.target.files;
    var file = files[0];
    file_name = file.name;
    file_size = file.size;
    var file_extension = file_name.substring(file_name.lastIndexOf('.') + 1);
    if (file_name.indexOf('.') !== -1) {
      console.log("file_extension--"+file_extension);
        if (file_size > max_limit) {
            callback('File max limit exceeded');
        } else if ($.inArray(file_extension, ['gif', 'png', 'jpg', 'jpeg', 'bmp']) == -1) {
            callback('Invalid file format');
        } else {
            file_content = null;
            if (files && file) {
                convert_to_base64(file, function(file_content) {
                    if (file_content == null) {
                        callback('File content is empty');
                    }
                    result = uploadFileFormat(file_size, file_name, file_content);
                    callback(result, le_cnt);
                });
            }
        }
    } else {
        callback('Invalid file format');
    } // file_extension = file_name.substr(
    //     file_name.lastIndexOf('.') + 1
    // );
}

function complianceDetails(sProvision, cTask, description, docName, fFormat, pConsequence, cFrequency, statuDates, rTypeId, rEvery, dTypeId, duration, isActive, cId) {
    var compliance = {};
    compliance.s_provision = sProvision;
    compliance.c_task = cTask;
    compliance.description = description;
    compliance.doc_name = docName;
    compliance.f_f_list = fFormat;
    compliance.p_consequences = pConsequence;
    compliance.f_id = cFrequency;
    compliance.statu_dates = statuDates;
    compliance.r_type_id = rTypeId;
    compliance.r_every = rEvery;
    compliance.d_type_id = dTypeId;
    compliance.duration = duration;
    compliance.is_active = isActive;
    compliance.frequency = null;
    compliance.summary = null;
    if (cId !== null && cId !== '') {
        compliance.c_id = cId;
    } else {
        compliance.c_id = null;
    }
    return compliance;
}

function checkDuplicateStatutoryMapping(cId, dId, iIds, sNId, sIds, callback) {
    var request = [
        'CheckDuplicateStatutoryMapping', {
            'c_id': cId,
            'd_id': dId,
            'i_ids': iIds,
            's_n_id': sNId,
            's_ids': sIds
        }
    ];
    apiRequest('knowledge_transaction', request, callback);
}

function statutoryMapping(cId, dId, iIds, sNId, sIds, compliances, gIds, mappings, mId) {
    var mappingData = {};
    mappingData.c_id = cId;
    mappingData.d_id = dId;
    mappingData.i_ids = iIds;
    mappingData.s_n_id = sNId;
    mappingData.s_ids = sIds;
    mappingData.compliances = compliances;
    mappingData.g_ids = gIds;
    mappingData.mappings = mappings;
    if (mId !== null) {
        mappingData.s_m_id = mId;
    }
    return mappingData;
}

function saveStatutoryMapping(mappingData, callback) {
    var request = [
        'SaveStatutoryMapping',
        mappingData
    ];
    apiRequest('knowledge_transaction', request, callback);
}

function updateStatutoryMapping(mappingData, callback) {
    var request = [
        'UpdateStatutoryMapping',
        mappingData
    ];
    apiRequest('knowledge_transaction', request, callback);
}

function updateComplianceOnly(mappingData, callback) {
    var request = [
        'UpdateCompliance',
        mappingData
    ];
    apiRequest('knowledge_transaction', request, callback);
}


function getStatutoryMaster(callback) {
    var request = [
        'GetStatutoryMaster',
        {}
    ];
    apiRequest('knowledge_transaction', request, callback);
}

function getStatutoryMappingsMaster(callback) {
    var request = [
        'GetStatutoryMappingsMaster',
        {}
    ];
    apiRequest('knowledge_transaction', request, callback);
}

function getStatutoryMappings(approval_status, active_status, rcount, page_limit, callback) {
    var request = [
        'GetStatutoryMappings', {
            "approval_status_id": parseInt(approval_status),
            "active_status_id" : parseInt(active_status),
            "rcount": parseInt(rcount),
            "page_limit": parseInt(page_limit)
        }
    ];
    apiRequest('knowledge_transaction', request, callback);
}

function getStatutoryMappingsEdit(m_id, comp_id, callback) {
    var request = [
        'GetComplianceEdit', {
            "m_id": parseInt(m_id),
            "comp_id": comp_id
        }
    ];
    apiRequest('knowledge_transaction', request, callback);
}

function changeStatutoryMappingStatus(mId, isActive, callback) {
    var request = [
        'ChangeStatutoryMappingStatus', {
            's_m_id': mId,
            'is_active': isActive
        }
    ];
    apiRequest('knowledge_transaction', request, callback);
}

function getApproveStatutoryMapingsFilters(callback) {
    var request = [
        'GetApproveStatutoryMappingsFilters',
        {}
    ];
    apiRequest('knowledge_transaction', request, callback);
}

function getApproveStatutoryMapings(cid, did, iid, nid, uid, rcount, callback) {
    var request = [
        'GetApproveStatutoryMappings', {
            "a_c_id": cid,
            "a_d_id": did,
            "a_i_id": iid,
            "a_s_n_id": nid,
            "a_u_id": uid,
            "r_count": rcount
        }
    ];
    apiRequest('knowledge_transaction', request, callback);
}

function getComplianceInfo(comp_id, callback) {
    var request = [
        'GetComplianceInfo', {
            "comp_id": comp_id
        }
    ];
    apiRequest('knowledge_transaction', request, callback);
}

function approveStatutoryList(cname, dname, sname, mapText, ctask, asid, remarks, mid, compid, is_common, updatedby) {
    return {
        "c_name": cname,
        "d_name": dname,
        "s_n_name": sname,
        "map_text": mapText,
        "c_task": ctask,
        "a_s_id": asid,
        "remarks": remarks,
        "m_id": mid,
        "comp_id": compid,
        "is_common": is_common,
        "u_by": updatedby,
    }

}

function approveStatutoryMapping(approvalList, callback) {
    var request = [
        'ApproveStatutoryMapping',
        { 's_mappings': approvalList }
    ];
    apiRequest('knowledge_transaction', request, callback);
}

function getStatutoryMappingsReportFilter(callback) {
    var request = [
        'GetStatutoryMappingReportFilters',
        {}
    ];
    apiRequest('knowledge_report', request, callback);
}

function filterData(cId, dId, iId, sNId, gId, level1SId, fId, rCount, page_count) {
    var filter = {};
    filter.c_id = cId;
    filter.d_id = dId;
    filter.a_i_id = iId;
    filter.a_s_n_id = sNId;
    filter.a_g_id = gId;
    filter.statutory_id_optional = level1SId;
    filter.frequency_id = fId;
    filter.r_count = rCount;
    filter.page_count = page_count;
    return filter;
}

function getStatutoryMappingsReportData(filterDatas, callback) {
    var request = [
        'GetStatutoryMappingReportData',
        filterDatas
    ];
    apiRequest('knowledge_report', request, callback);
}
// compliance task list
function getComplianceTaskFilter(callback) {
    var request = [
        'GetComplianceTaskFilter',
        {}
    ];
    apiRequest('techno_report', request, callback);
}

// function getComplianceTaskReport(filterDatas, callback) {
//     var request = [
//         'GetComplianceTaskReport',
//         filterDatas
//     ];
//     apiRequest('techno_report', request, callback);
// }
// Admin User Group Master
function getAdminUserGroupList(callback) {
    callerName = 'admin';
    var request = [
        'GetUserGroups',
        {}
    ];
    apiRequest(callerName, request, callback);
}

function getSaveAdminUserGroupDict(ugName, fcId, fIds) {
    userGroup = {};
    userGroup.ug_name = ugName;
    userGroup.fc_id = fcId;
    userGroup.f_ids = fIds;
    return userGroup;
}

function saveAdminUserGroup(userGroupDetail, callback) {
    callerName = 'admin';
    var request = [
        'SaveUserGroup',
        userGroupDetail
    ];
    apiRequest(callerName, request, callback);
}

function getUpdateAdminUserGroupDict(ugId, ugName, fcId, fIds) {
    userGroup = {};
    userGroup.ug_id = ugId;
    userGroup.ug_name = ugName;
    userGroup.fc_id = fcId;
    userGroup.f_ids = fIds;
    return userGroup;
}

function updateAdminUserGroup(userGroupDetail, callback) {
    callerName = 'admin';
    var request = [
        'UpdateUserGroup',
        userGroupDetail
    ];
    apiRequest(callerName, request, callback);
}

function changeAdminUserGroupStatus(ugId, ugName, active, callback) {
    callerName = 'admin';
    var request = [
        'ChangeUserGroupStatus', {
            'ug_id': ugId,
            'ug_name': ugName,
            'active': active
        }
    ];
    apiRequest(callerName, request, callback);
}
// Admin User Master
function getAdminUserList(callback) {
    callerName = 'admin';
    var request = [
        'GetUsers',
        {}
    ];
    apiRequest(callerName, request, callback);
}

function getSaveAdminUserDict(userDetail) {
    var catId = userDetail[0];
    var email = userDetail[1];
    var ugId = userDetail[2];
    var empN = userDetail[3];
    var empC = userDetail[4];
    var cNo = userDetail[5];
    var mNo = userDetail[6];
    var add = userDetail[7];
    if (userDetail[7] == '') {
        add = null;
    }
    var desig = userDetail[8];
    if (userDetail[8] == '') {
        desig = null;
    }
    var cIds = userDetail[9];
    var dIds = userDetail[10];
    return {
        'u_cat_id': catId,
        'employee_name': empN,
        'employee_code': empC,
        'email_id': email,
        'contact_no': cNo,
        'mobile_no': mNo,
        'ug_id': ugId,
        'address': add,
        'designation': desig,
        'country_ids': cIds,
        'country_wise_domain': dIds
    };
}

function sendRegistration(userInfo, callback) {
    var request = ['SendRegistraion', userInfo];
    apiRequest("admin", request, callback);
}

function saveAdminUser(userDetail, callback) {
    callerName = 'admin';
    var request = [
        'SaveUser',
        userDetail
    ];
    apiRequest(callerName, request, callback);
}

function getUpdateAdminUserDict(userDetail) {
    var uId = userDetail[0];
    var ugId = userDetail[1];
    var empN = userDetail[2];
    var empC = userDetail[3];
    var cn = userDetail[4];
    var add = userDetail[5];
    if (userDetail[5] == '') {
        add = null;
    }
    var desig = userDetail[6];
    if (userDetail[6] == '') {
        desig = null;
    }
    var cIds = userDetail[7];
    var dIds = userDetail[8];
    return {
        'user_id': uId,
        'ug_id': ugId,
        'employee_name': empN,
        'employee_code': empC,
        'contact_no': cn,
        'address': add,
        'designation': desig,
        'country_ids': cIds,
        'country_wise_domain': dIds
    };
}

function updateAdminUser(userDetail, callback) {
    callerName = 'admin';
    var request = [
        'UpdateUser',
        userDetail
    ];
    apiRequest(callerName, request, callback);
}

function changeAdminUserStatus(uId, active, callback) {
    callerName = 'admin';
    var request = [
        'ChangeUserStatus', {
            'user_id': uId,
            'is_active': active
        }
    ];
    apiRequest(callerName, request, callback);
}

function changeAdminDisaleStatus(uId, active, remarks, callback) {
    callerName = 'admin';
    var request = [
        'ChangeDisableStatus', {
            'user_id': uId,
            'is_disable': active,
            'remarks': remarks
        }
    ];
    apiRequest(callerName, request, callback);
}
// Client Group Master
function getDateConfigurations(cId, dId, pFrom, pTo) {
    return {
        'country_id': cId,
        'domain_id': dId,
        'month_from': pFrom,
        'month_to': pTo
    };
}

function getDomainRow(
    d_id, a_date, org
) {
    return {
        "d_id": d_id,
        "activation_date": a_date,
        "org": org,
        "is_delete": 0
    }
}

function getLegalEntityRow(
    c_id, b_g_id, b_g_name, l_e_name,
    logo, n_o_l, f_s, c_f, c_t, d
) {
    return {
        "country_id": c_id,
        "business_group": getBusinessGroupDict(b_g_id, b_g_name),
        "legal_entity_name": l_e_name,
        "logo": logo,
        "no_of_licence": n_o_l,
        "file_space": f_s,
        "contract_from": c_f,
        "contract_to": c_t,
        "domain_details": d
    };
}

function getLegalEntityUpdateRow(
    c_id, b_g_id, b_g_name, l_e_id, l_e_name,
    logo, new_logo, n_o_l, f_s, c_f, c_t, d
) {
    console.log("inside getLegalEntityUpdateRow:" + b_g_id)
    return {
        "country_id": c_id,
        "business_group": getBusinessGroupDict(b_g_id, b_g_name),
        "legal_entity_id": l_e_id,
        "legal_entity_name": l_e_name,
        "old_logo": logo,
        "new_logo": new_logo,
        "no_of_licence": n_o_l,
        "file_space": f_s,
        "contract_from": c_f,
        "contract_to": c_t,
        "domain_details": d
    };
}

function saveClientGroup(g_name, u_name, short_name, no_of_view_licence, les, d_cs, callback) {
    callerName = 'techno';
    var request = [
        'SaveClientGroup', {
            "group_name": g_name,
            "email_id": u_name,
            "short_name": short_name,
            "no_of_view_licence": no_of_view_licence,
            "legal_entity_details": les,
            "date_configurations": d_cs
        }
    ];
    apiRequest(callerName, request, callback);
}

function updateClientGroup(g_id, g_name, u_name, short_name, no_of_view_licence, remarks,
    les, d_cs, callback) {
    callerName = 'techno';
    var request = [
        'UpdateClientGroup', {
            "client_id": g_id,
            "group_name": g_name,
            "email_id": u_name,
            "short_name": short_name,
            "no_of_view_licence": no_of_view_licence,
            "legal_entities": les,
            "date_configurations": d_cs,
            "remarks": remarks
        }
    ];
    apiRequest(callerName, request, callback);
}

function changeClientGroupStatus(clientId, isActive, callback) {
    callerName = 'techno';
    var request = [
        'ChangeClientGroupStatus', {
            'client_id': clientId,
            'is_active': isActive
        }
    ];
    apiRequest(callerName, request, callback);
}

function getClientGroups(callback) {
    callerName = 'techno';
    var request = [
        'GetClientGroups',
        {}
    ];
    apiRequest(callerName, request, callback);
}

function getClientGroupFormData(callback) {
    callerName = 'techno';
    var request = [
        'GetClientGroupFormData',
        {}
    ];
    apiRequest(callerName, request, callback);
}

function getEditClientGroupFormData(client_id, callback) {
    callerName = 'techno';
    var request = [
        'GetEditClientGroupFormData', {
            'group_id': client_id
        }
    ];
    apiRequest(callerName, request, callback);
}

// Assign Legal Entity
function getAssignLegalEntityList(callback) {
    callerName = 'techno';
    var request = [
        'GetAssignLegalEntityList',
        {}
    ];
    apiRequest(callerName, request, callback);
}


function getEditAssignLegalEntity(client_id, callback) {
    callerName = 'techno';
    var request = [
        'GetEditAssignLegalEntity', {
            'group_id': client_id
        }
    ];
    apiRequest(callerName, request, callback);
}

function saveAssignLegalEntity(client_id, legal_entity_ids, user_ids, callback) {
    callerName = 'techno';
    var request = [
        'SaveAssignLegalEntity', {
            'client_id': client_id,
            'legal_entity_ids': legal_entity_ids,
            'user_ids': user_ids
        }
    ];
    apiRequest(callerName, request, callback);
}

function viewAssignLegalEntity(client_id, callback) {
    callerName = 'techno';
    var request = [
        'ViewAssignLegalEntity', {
            'client_id': client_id
        }
    ];
    apiRequest(callerName, request, callback);
}

// Change Password APIs
function changePassword(currentPassword, newPassword, callback) {
    callerName = 'login';
    var request = [
        'ChangePassword', {
            'session_token': getSessionToken(),
            'current_password': currentPassword,
            'new_password': newPassword
        }
    ];
    LoginApiRequest(callerName, request, callback);
}
// Forgot Password APIs
function forgotPassword(username, callback) {
    callerName = 'login';
    var request = [
        'ForgotPassword', {
            'username': username,
            'short_name': null
        }
    ];
    LoginApiRequest(callerName, request, callback);
}

function validateResetToken(resetToken, callback) {
    callerName = 'login';
    var request = [
        'ResetTokenValidation', {
            'reset_token': resetToken,
            'short_name': getShortName()
        }
    ];
    LoginApiRequest(callerName, request, callback);
}

function resetPassword(resetToken, newPassword, callback) {
    callerName = 'login';
    var request = [
        'ResetPassword', {
            'reset_token': resetToken,
            'new_password': newPassword,
            'short_name': getShortName()
        }
    ];
    LoginApiRequest(callerName, request, callback);
}
// Client Unit APIs
function getClients(type, callback) {
    callerName = 'techno';
    var request = [
        'GetClients',
        {}
    ];
    apiRequest(callerName, request, callback);
}

function getClientsEdit(client_id, business_group_id, legal_entity_id, country_id, from_count, unitsPerPage, callback) {
    callerName = 'techno';
    var request = [
        'GetClientsEdit', {
            'client_id': client_id,
            'bg_id': business_group_id,
            'le_id': legal_entity_id,
            'c_id': country_id,
            'from_count': from_count,
            'page_count': unitsPerPage
        }
    ];
    apiRequest(callerName, request, callback);
}

function getNextUnitCode(client_id, callback) {
    callerName = 'techno';
    var request = [
        'GetNextUnitCode',
        { 'client_id': client_id }
    ];
    apiRequest(callerName, request, callback);
}

function getBusinessGroupDict(bgId, bgName) {
    console.log("bgName:" + bgName);
    if ((bgName == null || bgName == '') && (bgId == null || bgId == '')) {
        return null;
    } else {
        return {
            'business_group_id': bgId,
            'business_group_name': bgName
        };
    }
}


function uploadFormatFile(formdata, callback) {
    $.ajax({

        xhr: function() {
            var xhr = new window.XMLHttpRequest();
            xhr.upload.addEventListener("progress", function(evt) {
                if (evt.lengthComputable) {
                    var percentComplete = evt.loaded / evt.total;
                    percentComplete = parseInt(percentComplete * 100);
                    progress(percentComplete, $('#progressBar'));

                    if (percentComplete === 100) {
                        $('.upload-progress-count').hide();
                    }

                }
            }, false);
            return xhr;
        },

        url: '/knowledge/api/files',
        headers: { 'X-CSRFToken': csrf_token, 'Caller-Name': window.location.pathname },
        type: 'POST',
        crossDomain: true,
        data: formdata,
        processData: false,
        contentType: false,
        success: function(data, textStatus, jqXHR) {
            // var data = parseJSON(data);
            data = atob(data.substring(5));
            data = parseJSON(data);

            var status = data[0];
            var response = data[1];
            matchString = 'success';
            if (status.toLowerCase().indexOf(matchString) != -1) {
                callback(null, response);
            }
            else if (status == 'InvalidSessionToken') {
                window.sessionStorage.login_url = login_url;
                clearSession();
                confirm_ok_alert(message[status], login_url);
            }
            else
                callback(status, response);
        },
        error: function(jqXHR, textStatus, errorThrown) {
            rdata = parseJSON(jqXHR.responseText);
            rdata = atob(rdata);
            callback(rdata, errorThrown); // alert("jqXHR:"+jqXHR.status);
        }
    });
}

function getClientUnitApprovalList(callback) {
    callerName = 'client_coordination_master';
    var request = [
        'GetClientUnitApprovalList',
        {}
    ];
    apiRequest(callerName, request, callback);
}

function getEntityApprovalList(legal_entity_id, callback) {
    callerName = 'client_coordination_master';
    var request = [
        'GetEntityApprovalList', {
            "legal_entity_id": legal_entity_id
        }
    ];
    apiRequest(callerName, request, callback);
}

function approveUnit(unit_approval_details, callback) {
    callerName = 'client_coordination_master';
    var request = [
        'ApproveUnit', {
            "unit_approval_details": unit_approval_details
        }
    ];
    apiRequest(callerName, request, callback);
}

function getClientGroupApprovalList(callback) {
    callerName = 'client_coordination_master';
    var request = [
        'GetClientGroupApprovalList',
        {}
    ];
    apiRequest(callerName, request, callback);
}

function getLegalEntity(entity_id, callback) {
    callerName = 'client_coordination_master';
    var request = [
        'GetLegalEntityInfo', {
            "le_id": entity_id
        }
    ];
    apiRequest(callerName, request, callback);
}

function approveClientGroupList(client_id, entity_id, entity_name, approval_status, reason) {
    return {
        "ct_id": client_id,
        "le_id": entity_id,
        "le_name": entity_name,
        "approval_status": approval_status,
        "reason": reason,
    }

}

function approveClientGroup(group_approval_details, callback) {
    callerName = 'client_coordination_master';
    var request = [
        'ApproveClientGroup', {
            "client_group_approval_details": group_approval_details
        }
    ];
    apiRequest(callerName, request, callback);
}


function saveDBServer(
    db_server_id, db_server_name, ip, port, username, password, callback
) {
    callerName = "console_admin"
    var request = [
        "SaveDBServer", {
            "db_server_id": db_server_id,
            "db_server_name": db_server_name,
            "ip": ip,
            "port": port,
            "username": username,
            "password": password
        }
    ];
    apiRequest(callerName, request, callback)
}

function getClientServerList(callback) {
    callerName = 'console_admin';
    var request = [
        'GetClientServerList', {}
    ];
    apiRequest(callerName, request, callback);
}

function saveClientServer(
    client_server_id, client_server_name, ip, port, callback
) {
    callerName = "console_admin";
    var request = [
        "SaveClientServer", {
            "client_server_id": client_server_id,
            "client_server_name": client_server_name,
            "ip": ip,
            "port": port
        }
    ];
    apiRequest(callerName, request, callback);
}

function getFileServerList(callback) {
    callerName = 'console_admin';
    var request = [
        'GetFileServerList', {}
    ];
    apiRequest(callerName, request, callback);
}

function fileServerEntry(
    file_server_id, file_server_name, ip, port, callback
) {
    callerName = "console_admin";
    var request = [
        "SaveFileServer", {
            "file_server_id": file_server_id,
            "file_server_name": file_server_name,
            "ip": ip,
            "port": port
        }
    ];
    apiRequest(callerName, request, callback);
}

function getAllocatedDBEnv(callback) {
    callerName = "console_admin";
    var request = [
        "GetAllocatedDBEnv",
        {}
    ];
    apiRequest(callerName, request, callback);
}

function getDeletionDetails(client_id, entity_id, unit_id, deletion_period) {
    return {
        "client_id": client_id,
        "legal_entity_id": entity_id,
        "unit_id": unit_id,
        "deletion_period": deletion_period,
    }
}


function getUserMappings(callback) {
    callerName = "admin";
    var request = [
        "GetUserMappings",
        {}
    ];
    apiRequest(callerName, request, callback);
}



function checkUserMappings(country_id, domain_id, parent_user_id, child_user_id, user_category_id, callback) {
    callerName = "admin";
    var request = [
        "CheckUserMappings", {
            "country_id": country_id,
            "domain_id": domain_id,
            "parent_user_id": parent_user_id,
            "child_user_id": child_user_id,
            "user_category_id": user_category_id
        }
    ];
    apiRequest(callerName, request, callback);
}

function saveUserMappings(country_id, domain_id, parent_user_id, child_users, user_category_id, new_child_users,
    new_child_user_names, callback) {
    callerName = "admin";
    var request = [
        "SaveUserMappings", {
            "country_id": country_id,
            "domain_id": domain_id,
            "parent_user_id": parent_user_id,
            "child_users": child_users,
            "user_category_id": user_category_id,
            "new_child_users": new_child_users,
            "new_child_user_names": new_child_user_names
        }
    ];
    apiRequest(callerName, request, callback);
}

function getReassignUserAccountFormdata(callback) {
    callerName = "admin";
    var request = [
        "GetReassignUserAccountFormdata",
        {}
    ];
    apiRequest(callerName, request, callback);
}

function getTechnoUSerInfo(techno_user_id, callback) {
    callerName = "admin";
    var request = [
        "GetTechnoUserData", {
            "techno_id": techno_user_id
        }
    ];
    apiRequest(callerName, request, callback);
}

function getDomainUserInfo(domain_user_id, group_id, entity_id, domain_id, callback) {
    callerName = "admin";
    var request = [
        "GetDomainUserData", {
            "d_u_id": domain_user_id,
            "gt_id": group_id,
            "le_id": entity_id,
            "d_id": domain_id
        }
    ];
    apiRequest(callerName, request, callback);
}

function technoManagerInfo(reassign_to, client_id, entity_id, techno_executive, old_techno_executive) {
    var userInfo = {};
    userInfo.reassign_to = reassign_to;
    userInfo.gt_id = client_id;
    userInfo.le_id = entity_id;
    userInfo.t_e_id = techno_executive;
    userInfo.old_t_e_id = old_techno_executive;
    return userInfo;
}

function ReassignTechnoManager(user_from, data, remarks, callback) {
    callerName = "admin";
    var request = [
        "SaveReassignTechnoManager", {
            "reassign_from": user_from,
            "t_manager_info": data,
            "remarks": remarks
        }
    ];
    apiRequest(callerName, request, callback);
}

function technoExecutiveInfo(client_id, entity_id) {
    var userInfo = {};
    userInfo.gt_id = client_id;
    userInfo.le_id = entity_id;
    return userInfo;
}

function ReassignTechnoExecutive(user_from, user_to, data, remarks, callback) {
    callerName = "admin";
    var request = [
        "SaveReassignTechnoExecutive", {
            "reassign_from": user_from,
            "reassign_to": user_to,
            "t_executive_info": data,
            "remarks": remarks
        }
    ];
    apiRequest(callerName, request, callback);
}

function domainManagerInfo(unit_id, domain_executive, old_domain_executive) {
    var userInfo = {};
    userInfo.u_id = unit_id;
    userInfo.d_e_id = domain_executive;
    userInfo.old_d_e_id = old_domain_executive;
    return userInfo;
}

function ReassignDomainManager(
    user_from, user_to, client_id, entity_id, domain_id, data,
    remarks, callback
) {
    callerName = "admin";
    var request = [
        "SaveReassignDomainManager", {
            "reassign_from": user_from,
            "reassign_to": user_to,
            "gt_id": client_id,
            "le_id": entity_id,
            "d_id": domain_id,
            "d_manager_info": data,
            "remarks": remarks
        }
    ];
    apiRequest(callerName, request, callback);
}

function ReassignDomainExecutive(
    user_from, user_to, client_id, entity_id, domain_id, unit_ids,
    remarks, callback
) {
    callerName = "admin";
    var request = [
        "SaveReassignDomainExecutive", {
            "reassign_from": user_from,
            "reassign_to": user_to,
            "client_id": client_id,
            "entity_id": entity_id,
            "domain_id": domain_id,
            "unit_ids": unit_ids,
            "remarks": remarks
        }
    ];
    apiRequest(callerName, request, callback);
}

function SaveUserReplacement(user_type, user_from, user_to, remarks, callback) {
    callerName = "admin";
    var request = [
        "UserReplacement", {
            "user_type": user_type,
            "old_user_id": user_from,
            "new_user_id": user_to,
            "remarks": remarks
        }
    ];
    apiRequest(callerName, request, callback);
}

function getAssignStatutoryWizardOneData(callback) {
    callerName = 'domain_transaction';
    var request = [
        "GetAssignedStatutoryWizardOneData",
        {}
    ];
    apiRequest(callerName, request, callback);
}

function getAssignStatutoryWizardOneDataUnits(clientid, bgid, leid, divid, catid, domainid, callback) {
    callerName = 'domain_transaction';
    var request = [
        "GetAssignedStatutoryWizardOneUnits", {
            "ct_id": clientid,
            "bg_id": bgid,
            "le_id": leid,
            "dv_id": divid,
            "cat_id": catid,
            "d_id": domainid
        }
    ];
    apiRequest(callerName, request, callback);
}

function getAssignStatutoryWizardTwoData(
    domain_id, unit_ids, rcount, callback
) {
    callerName = 'domain_transaction';
    var request = [
        "GetAssignedStatutoryWizardTwoData", {
            "d_id": domain_id,
            "unit_ids": unit_ids,
            "rcount": rcount
        }
    ];
    apiRequest(callerName, request, callback);
}

function getAssignStatutoryWizardTwoCount(
    domain_id, unit_ids, callback
) {
    callerName = 'domain_transaction';
    var request = [
        "GetAssignedStatutoryWizardTwoCount", {
            "d_id": domain_id,
            "unit_ids": unit_ids            }
    ];
    apiRequest(callerName, request, callback);
}

function getAssignedStatutoriesForApprove(callback){
  callerName = 'domain_transaction';
  var request = [
      "GetAssignedStatutoriesForApprove",
      {}
    ];
  apiRequest(callerName, request, callback);
}
function getAssignedStatutoriesComplianceToApprove(domain_id, unit_id, client_statutory_id, rcount, callback){
  callerName = 'domain_transaction';
  var request = [
      "GetAssignedStatutoriesToApprove",
      {
        "d_id": domain_id,
        "u_id": unit_id,
        "client_statutory_id": client_statutory_id,
        "rcount": rcount
      }
    ];
  apiRequest(callerName, request, callback);
}

function saveComplianceStatus(client_id, legal_entity_id, unit_id,
    domain_id, compliance_id, compliance_status,
    level_1_id, status, remarks, client_statutory_id,
    unit_name, domain_name
) {
    return {

        "u_id": unit_id,
        "d_id": domain_id,
        "comp_id": compliance_id,
        "comp_status": compliance_status,
        "level_1_s_id": level_1_id,
        "a_status": status,
        "remarks": remarks,
        "client_statutory_id": client_statutory_id,
        "u_name": unit_name,
        "d_name": domain_name
    }
}

function saveAssignedStatutory(
    compliances_applicablity_status, submission_type, client_id,
    legal_entity_id, domain_id, domain_name, unit_ids,
    legal_entity_name, b_grp_name,  callback
) {
    callerName = 'domain_transaction';
    var request = [
        "SaveAssignedStatutory", {
            "compliances_applicablity_status": compliances_applicablity_status,
            "submission_status": submission_type,
            "ct_id": client_id,
            "le_id": legal_entity_id,
            "d_id": domain_id,
            "d_name": domain_name,
            "unit_ids": unit_ids,
            "legal_entity_name": legal_entity_name,
            "b_grp_name": b_grp_name
        }
    ];
    apiRequest(callerName, request, callback);
}

function approveAssignedStatutory(
    unitId, domainId, cSID, complience_ids, submissionStatus, remark,
    unitName, domainName, groupName, legalentityName, businessgroupName, callback
) {
    callerName = 'domain_transaction';
    var request = [
        "ApproveAssignedStatutory", {
            'u_id': unitId,
            'd_id': domainId,
            'client_statutory_id': cSID,
            'comp_ids': complience_ids,
            'submission_status': submissionStatus,
            'remarks': remark,
            'u_name': unitName,
            'd_name': domainName,
            'group_name': groupName,
            'legal_entity_name': legalentityName,
            'business_group_name': businessgroupName,


        }
    ];
    apiRequest(callerName, request, callback);
}

function getAssignedStatutories(from_count, page_count, callback) {
    callerName = 'domain_transaction';
    var request = [
        "GetAssignedStatutories",
        {
          'from_count': from_count,
          'page_count': page_count
        }
    ];
    apiRequest(callerName, request, callback);
}

function getAssignedStatutoriesById(u_id, d_id, rcount, callback) {
    callerName = 'domain_transaction';
    var request = [
        "GetAssignedStatutoriesById", {
            "u_id": u_id,
            "d_id": d_id,
            "rcount": rcount
        }
    ];
    apiRequest(callerName, request, callback);
}

//user mapping report
function getUserMappingReportFilters(callback) {
    callerName = 'techno_report';
    var request = [
        'GetUserMappingReportFilters',
        {}
    ];
    apiRequest(callerName, request, callback);
}

//user mapping report
function getUserMappingStatutoryFilters(callback) {
    callerName = 'techno_report';
    var request = [
        'GetUserMappingStatutoryFilters',
        {}
    ];
    apiRequest(callerName, request, callback);
}

function getIPSettingsList(callback) {
    callerName = "console_admin";
    var request = [
        "GetIPSettingsList",
        {}
    ];
    apiRequest(callerName, request, callback);
}

function getGroupIPDetails(clientId, callback) {
    callerName = "console_admin";
    var request = [
        "GetGroupIPDetails", {
            "client_id": clientId
        }
    ];
    apiRequest(callerName, request, callback);
}

function getIPSettingsDetails(form_id, ip, client_id) {
    return {
        "form_id": form_id,
        "ip": ip,
        "client_id": client_id,
    }
}

function saveIPSettings(ip_details, callback) {
    callerName = "console_admin";
    var request = [
        "SaveIPSettings", {
            "group_ips_list": ip_details
        }
    ];
    apiRequest(callerName, request, callback);
}

function deleteIPSettings(clientId, callback) {
    callerName = "console_admin";
    var request = [
        "DeleteIPSettings", {
            "client_id": clientId
        }
    ];
    apiRequest(callerName, request, callback);
}

function getIPSettingsReportFilter(callback) {
    callerName = "console_admin";
    var request = [
        "GetIPSettingsReportFilter",
        {}
    ];
    apiRequest(callerName, request, callback);
}

function getIPSettingsReport(clientId, IP, FCount, TCount, csv, callback) {
    callerName = "console_admin";
    var request = [
        "GetIPSettingsReport", {
            "client_id": clientId,
            "ip_optional": IP,
            "from_count": FCount,
            "page_count": TCount,
            "csv": csv
        }
    ];
    apiRequest(callerName, request, callback);
}

function getAllocateServerReportData(callback) {
    callerName = 'console_admin';
    var request = [
        "GetAllocateServerReportData",
        {}
    ];
    console.log(request)
    apiRequest(callerName, request, callback);
}

function exportAllocateServerReportData(cl_id, le_id, csv, callback){
    callerName = 'console_admin';
    var request = [
        "ExportAllocateServerReportData", {
          "client_id": cl_id,
          "legal_entity_id": le_id,
          "csv": csv
        }
    ];
    console.log(request)
    apiRequest(callerName, request, callback);
}

function checkUserReplacement(user_type, user_from, callback) {
    callerName = "admin";
    var request = [
        "CheckUserReplacement", {
            "user_type": user_type,
            "old_user_id": user_from
        }
    ];
    apiRequest(callerName, request, callback);
}

function checkAssignedDomainUnits(u_id, d_ids, callback) {
    callerName = 'techno';
    var request = [
        "CheckAssignedDomainUnits", {
          "unit_id": u_id,
          "d_id": d_ids
        }
    ];
    apiRequest(callerName, request, callback);
}

function getClientAuditTrailFilter(callback) {
  callerName = 'general';
  var request = [
    'GetClientAuditTrailsFilter',
    {}
  ];
  apiRequest(callerName, request, callback);
}

function getClientAuditTrail(
  fromDate, toDate, userId, formId, client_id, legal_entity_id,
  recordCount, pageCount, callback) {
    callerName = 'general';
    var request = [
        'GetClientAuditTrails', {
            'from_date': fromDate,
            'to_date': toDate,
            'user_id_search': userId,
            'form_id_search': formId,
            'client_id': client_id,
            'legal_entity_id': legal_entity_id,
            'record_count': recordCount,
            'page_count': pageCount
        }
    ];
    apiRequest(callerName, request, callback);
}

function getClientLoginTraceFilter(callback) {
  callerName = 'general';
  var request = [
    'GetClientLoginTraceFilter',
    {}
  ];
  apiRequest(callerName, request, callback);
}

function getClientLoginTrace(
  fromDate, toDate, userId, client_id,
  recordCount, pageCount, callback) {
    callerName = 'general';
    var request = [
        'GetClientLoginTrace', {
            'from_date': fromDate,
            'to_date': toDate,
            'user_id_search': userId,
            'client_id': client_id,
            'record_count': recordCount,
            'page_count': pageCount
        }
    ];
    apiRequest(callerName, request, callback);
}

function getExportClientAuditTrail(
  fromDate, toDate, userId, formId, client_id, legal_entity_id,
  csv, callback) {
    callerName = 'general';
    var request = [
        'ExportClientAuditTrails', {
            'from_date': fromDate,
            'to_date': toDate,
            'user_id_search': userId,
            'form_id_search': formId,
            'client_id': client_id,
            'legal_entity_id': legal_entity_id,
            'csv': csv
        }
    ];
    apiRequest(callerName, request, callback);
}

function getExportClientLoginTrace(
  fromDate, toDate, userId, client_id, csv, callback) {
    callerName = 'general';
    var request = [
        'ExportClientLoginTrace', {
            'from_date': fromDate,
            'to_date': toDate,
            'user_id_search': userId,
            'client_id': client_id,
            'csv': csv
        }
    ];
    apiRequest(callerName, request, callback);
}

/* client bulk upload - api function starts */

function getClientGroupsList(callback) {
  callerName = 'techno';
  var request = [
      'GetClientGroupsList',
      {}
  ];
  apiRequest(callerName, request, callback);
}

function uploadCSVFile(fileListener, callback) {
    var evt = fileListener;
    max_limit = 1024 * 1024 * 50;
    // file max limit 50MB
    var files = evt.target.files;
    var file = files[0];
    file_name = file.name;
    file_size = file.size;
    if (file_size > max_limit) {
        callback('File max limit exceeded');
    } else {
        file_content = null;
        if (files && file) {
            convert_to_base64(file, function(file_content) {
                if (file_content == null) {
                    callback('File content is empty');
                }
                result = uploadFileFormat(file_size, file_name, file_content);
                callback(result);
            });
        }
    }
}

/* client bulk upload - api function ends */



function getKnowledgeUserInfo(callback) {
  callerName = 'general';
  var request = [
      'GetKExecutiveDetails',
      {}
  ];
  apiRequest(callerName, request, callback);
}
