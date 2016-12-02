// var BASE_URL = "http://127.0.0.1:8082/";
var BASE_URL = '/knowledge/api/';
var login_url = '/knowledge/login';
var csrf_token = $('meta[name=csrf-token]').attr('content')
var my_ip = null;
function initMirror() {
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
    data = JSON.stringify(data);
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
  function getUserId() {
    var info = getUserInfo();
    if (info !== null)
      return info.user_id;
    else
      return null;
  }
  function local_session_timeout(){
    var myVar = setInterval(function(){ myTimer() }, 1000);
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
    $.getJSON('http://jsonip.com?callback=?', function (data) {
      window.sessionStorage.my_ip = data.ip;
    });
  }
  function getCookie(name) {
    var r = document.cookie.match('\\b' + name + '=([^;]*)\\b');
    return r ? r[1] : undefined;
  }
  function apiRequest(callerName, request, callback) {
    var sessionToken = getSessionToken();
    var requestFrame = {
      'session_token': sessionToken,
      'request': request
    };
    $.ajax({
      url: BASE_URL + callerName,
      headers: { 'X-CSRFToken': csrf_token },
      type: 'POST',
      contentType: 'application/json',
      data: toJSON(requestFrame),
      success: function (data) {
        // var data = parseJSON(data);
        var status = data[0];
        var response = data[1];
        matchString = 'success';
        if (status.toLowerCase().indexOf(matchString) != -1) {
          if (status == 'UpdateUserProfileSuccess') {
            updateUserInfo(response);
          }
          callback(null, response);
        } else if (status == 'InvalidSessionToken') {
          login_url = '/knowledge/login';
          window.sessionStorage.login_url = login_url;
          clearSession();
          window.location.href = login_url;
        } else {
          if (Object.keys(response).length == 0)
            callback(status, null);
          else
            callback(status, response);
        }
      },
      error: function (jqXHR, textStatus, errorThrown) {
        // alert(jqXHR["responseText"]);
        callback(jqXHR.responseText, errorThrown);  // alert("jqXHR:"+jqXHR.status);
                                                    // alert("textStatus:"+textStatus);
                                                    // alert("errorThrown:"+errorThrown);
                                                    // callback(error, null);
      }
    });
  }
  function LoginApiRequest(callerName, request, callback) {
    $.ajax({
      url: BASE_URL + callerName,
      // headers: {'X-Xsrftoken' : getCookie('_xsrf')},
      headers: { 'X-CSRFToken': csrf_token },
      type: 'POST',
      contentType: 'application/json',
      data: toJSON(request),
      success: function (data) {
        // var data = parseJSON(data);
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
      error: function (jqXHR, textStatus, errorThrown) {
        callback(jqXHR.responseText, null);
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
      headers: { 'X-CSRFToken': csrf_token },
      // headers: {'X-Xsrftoken' : getCookie('_xsrf')},
      type: 'POST',
      contentType: 'application/json',
      data: toJSON(request),
      success: function (data) {
        // var data = parseJSON(data);
        var status = data[0];
        var response = data[1];
        matchString = 'success';
        clearSession();
        login_url = '/knowledge/login';
        window.sessionStorage.login_url = login_url;
        window.location.href = login_url;
      },
      error: function (jqXHR, textStatus, errorThrown) {
        callback(jqXHR.responseText);
      }
    });
  }
  //Domain Master
  function saveDomain(dName, cIds, callback) {
    var request = [
      'SaveDomain',
      {
        'd_name': dName,
        'c_ids': cIds
      }
    ];
    apiRequest('general', request, callback);
  }
  function updateDomain(dId, dName, cIds, callback) {
    var request = [
      'UpdateDomain',
      {
        'd_id': dId,
        'd_name': dName,
        'c_ids': cIds
      }
    ];
    apiRequest('general', request, callback);
  }
  function changeDomainStatus(dId, isActive, callback) {
    var request = [
      'ChangeDomainStatus',
      {
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
      'UpdateCountry',
      {
        'c_id': cId,
        'c_name': cName
      }
    ];
    apiRequest('general', request, callback);
  }
  function changeCountryStatus(cId, isActive, callback) {
    var request = [
      'ChangeCountryStatus',
      {
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
      'ChangeIndustryStatus',
      {
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
      'ChangeStatutoryNatureStatus',
      {
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
  function saveAndUpdateGeographyLevels(cId, levels, callback) {
    var request = [
      'SaveGeographyLevel',
      {
        'c_id': cId,
        'levels': levels
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
      'SaveStatutoryLevel',
      {
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
      'SaveGeography',
      {
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
      'UpdateGeography',
      {
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
      'ChangeGeographyStatus',
      {
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
  function saveStatutory(dId, lId, name, pIds, pNames, callback) {
    var request = [
      'SaveStatutory',
      {
        'd_id': dId,
        's_l_id': lId,
        's_name': name,
        's_pids': pIds,
        's_pnames': pNames
      }
    ];
    apiRequest('knowledge_master', request, callback);
  }
  function updateStatutory(sId, lId, name, pIds, pNames, callback) {
    var request = [
      'UpdateStatutory',
      {
        's_id': sId,
        's_l_id': lId,
        's_name': name,
        'p_ids': pIds,
        'p_names': pNames
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
    reader.onload = function (readerEvt) {
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
      if (file_size > max_limit) {
        callback('File max limit exceeded');
      } else if (file_extension == 'exe' || file_extension == 'xhtml' || file_extension == 'htm' || file_extension == 'html') {
        callback('Invalid file format');
      } else {
        file_content = null;
        if (files && file) {
          convert_to_base64(file, function (file_content) {
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
    }  // file_extension = file_name.substr(
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
      'CheckDuplicateStatutoryMapping',
      {
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
  function getStatutoryMappings(approval_status, rcount, callback) {
    var request = [
      'GetStatutoryMappings',
      {
        "approval_status_id": parseInt(approval_status),
        "rcount": parseInt(rcount)
      }
    ];
    apiRequest('knowledge_transaction', request, callback);
  }
  function changeStatutoryMappingStatus(mId, isActive, callback) {
    var request = [
      'ChangeStatutoryMappingStatus',
      {
        's_m_id': mId,
        'is_active': isActive
      }
    ];
    apiRequest('knowledge_transaction', request, callback);
  }
  function getApproveStatutoryMapings(callback) {
    var request = [
      'GetApproveStatutoryMappings',
      {}
    ];
    apiRequest('knowledge_transaction', request, callback);
  }

  function getComplianceInfo(comp_id, callback) {
    var request = [
      'GetComplianceInfo',
      {
        "comp_id" : comp_id
      }
    ];
    apiRequest('knowledge_transaction', request, callback);
  }

  function approveStatutoryList(sMId, sProvision, aStatus, reason, nText) {
    var dict = {};
    if (reason == '') {
      reason = null;
    }
    if (nText == '') {
      nText = null;
    }
    dict.s_m_id = sMId;
    dict.s_provision = sProvision;
    dict.a_status = aStatus;
    dict.r_reason = reason;
    dict.n_text = nText;
    return dict;
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
  function filterData(cId, dId, iId, sNId, gId, level1SId, fId, rCount) {
    var filter = {};
    filter.c_id = cId;
    filter.d_id = dId;
    filter.i_id = iId;
    filter.s_n_id = sNId;
    filter.g_id = gId;
    filter.level_1_s_id = level1SId;
    filter.f_id = fId;
    filter.r_count = rCount;
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
  function getComplianceTaskReport(filterDatas, callback) {
    var request = [
      'GetComplianceTaskReport',
      filterDatas
    ];
    apiRequest('techno_report', request, callback);
  }
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
      'ChangeUserGroupStatus',
      {
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
      'ChangeUserStatus',
      {
        'user_id': uId,
        'is_active': active
      }
    ];
    apiRequest(callerName, request, callback);
  }
  function changeAdminDisaleStatus(uId, active, remarks, callback) {
    callerName = 'admin';
    var request = [
      'ChangeDisableStatus',
      {
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
  ){
      return {
        "d_id": d_id,
        "activation_date": a_date,
        "org": org
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
      'SaveClientGroup',
      {
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

  function updateClientGroup(g_id, g_name, u_name, short_name, no_of_view_licence,
    les, d_cs, callback) {
    callerName = 'techno';
    var request = [
      'UpdateClientGroup',
      {
        "client_id": g_id,
        "group_name": g_name,
        "email_id": u_name,
        "short_name": short_name,
        "no_of_view_licence": no_of_view_licence,
        "legal_entities": les,
        "date_configurations": d_cs
      }
    ];
    apiRequest(callerName, request, callback);
  }
  function changeClientGroupStatus(clientId, isActive, callback) {
    callerName = 'techno';
    var request = [
      'ChangeClientGroupStatus',
      {
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

  function getEditClientGroupFormData(client_id, callback){
    callerName = 'techno';
    var request = [
      'GetEditClientGroupFormData',
      {
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


  function getEditAssignLegalEntity(client_id, callback){
    callerName = 'techno';
    var request = [
      'GetEditAssignLegalEntity',
      {
        'group_id': client_id
      }
    ];
    apiRequest(callerName, request, callback);
  }

  function saveAssignLegalEntity(client_id, legal_entity_ids, user_ids, callback){
    callerName = 'techno';
    var request = [
      'SaveAssignLegalEntity',
      {
        'client_id': client_id,
        'legal_entity_ids': legal_entity_ids,
        'user_ids': user_ids
      }
    ];
    apiRequest(callerName, request, callback);
  }

  function viewAssignLegalEntity(client_id, callback){
    callerName = 'techno';
    var request = [
      'ViewAssignLegalEntity',
      {
        'client_id': client_id
      }
    ];
    apiRequest(callerName, request, callback);
  }

  // Change Password APIs
  function changePassword(currentPassword, newPassword, callback) {
    callerName = 'login';
    var request = [
      'ChangePassword',
      {
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
      'ForgotPassword',
      {
        'username': username,
        'short_name': null
      }
    ];
    LoginApiRequest(callerName, request, callback);
  }
  function validateResetToken(resetToken, callback) {
    callerName = 'login';
    var request = [
      'ResetTokenValidation',
      {
        'reset_token': resetToken,
        'short_name': getShortName()
      }
    ];
    LoginApiRequest(callerName, request, callback);
  }
  function resetPassword(resetToken, newPassword, callback) {
    callerName = 'login';
    var request = [
      'ResetPassword',
      {
        'reset_token': resetToken,
        'new_password': newPassword,
        'short_name': getShortName()
      }
    ];
    LoginApiRequest(callerName, request, callback);
  }
  // Client Unit APIs
  function getClients(callback) {
    callerName = 'techno';
    var request = [
      'GetClients',
      {}
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
    console.log("bgName:"+bgName);
    if ((bgName == null || bgName == '') && (bgId == null || bgId == '')) {
      return null;
    } else {
      return {
        'business_group_id': bgId,
        'business_group_name': bgName
      };
    }
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
  /*function getUnitDict(uId, uName, uCode, uAdd, pCode, geoId, uLoc, iId, iName, dIds) {
    return {
      'u_id': uId,
      'u_name': uName,
      'u_code': uCode,
      'u_add': uAdd,
      'p_code': pCode,
      'geo_id': geoId,
      'u_loc': uLoc,
      'i_id': iId,
      'i_name': iName,
      'd_ids': dIds
    };
  }old*/
  function getUnitDict(uId, uName, uCode, uAdd, pCode, geoId, dIds, iIds) {
    return {
      'u_id': uId,
      'u_name': uName,
      'u_code': uCode,
      'u_add': uAdd,
      'p_code': pCode,
      'geo_id': geoId,
      'd_ids': dIds,
      'i_ids': iIds
    };
  }
  function mapUnitsToCountry(cId, units) {
    return {
      'c_id': cId,
      'units': units
    };
  }
  function saveClient(cId, bg_id, le_id, c_id, div_dict, cw_units, callback) {
    callerName = 'techno';
    var request = [
      'SaveClient',
      {
        'cl_id': cId,
        'bg_id': bg_id,
        'le_id': le_id,
        'c_id': c_id,
        'div_dict': div_dict,
        'units': cw_units
      }
    ];
    console.log("req:"+request)
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
  //Statutory Notifications List
  function getStatutoryNotificationsFilters(callback) {
    callerName = 'techno_report';
    var request = [
      'GetStatutoryNotificationsFilters',
      {}
    ];
    apiRequest(callerName, request, callback);
  }
  function getStatutoryNotificationsReportData(countryId, domainId, level1Id, fromDate, toDate, callback) {
    callerName = 'techno_report';
    var request = [
      'GetStatutoryNotificationsReportData',
      {
        'country_id': countryId,
        'domain_id': domainId,
        'level_1_statutory_id': level1Id,
        'from_date': fromDate,
        'to_date': toDate
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
  function getAssignedStatutoryReport(cId, dId, clientId, bGroupId, lEntityId, statId, uId, complId, callback) {
    var request = [
      'GetAssignedStatutoryReport',
      {
        'c_id': cId,
        'domain_id_optional': dId,
        'client_id': clientId,
        'bg_id': bGroupId,
        'le_id': lEntityId,
        'statutory_id': statId,
        'unit_id': uId,
        'comp_id': complId
      }
    ];
    callerName = 'techno_report';
    apiRequest(callerName, request, callback);
  }
  function getAuditTrail(fromDate, toDate, userId, formId, countryId, categoryId, recordCount, pageCount, callback) {
    callerName = 'general';
    var request = [
      'GetAuditTrails',
      {
        'from_date': fromDate,
        'to_date': toDate,
        'user_id': userId,
        'form_id_search': formId,
        'country_id': countryId,
        'category_id': categoryId,
        'record_count': recordCount,
        'page_count': pageCount
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
    $('.upload-progress-count').html("Uploading " + percent + "% ")
    //$element.find('div').animate({ width: progressBarWidth }, 500).html(percent + "% ");
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
      headers: { 'X-CSRFToken': csrf_token },
      type: 'POST',
      crossDomain: true,
      data: formdata,
      processData: false,
      contentType: false,
      success: function (data, textStatus, jqXHR) {
        // var data = parseJSON(data);
        var status = data[0];
        var response = data[1];
        if (Object.keys(response).length == 0)
          callback(status, null);
        else
          callback(status, response);
      },
      error: function (jqXHR, textStatus, errorThrown) {
      }
    });
  }
  function getClientUnitApprovalList(callback){
    callerName = 'client_coordination_master';
    var request = [
      'GetClientUnitApprovalList',
      {}
    ];
    apiRequest(callerName, request, callback);
  }
  function getEntityApprovalList(legal_entity_id, callback){
    callerName = 'client_coordination_master';
    var request = [
      'GetEntityApprovalList',
      {
        "legal_entity_id": legal_entity_id
      }
    ];
    apiRequest(callerName, request, callback);
  }
  function approveUnit(unit_approval_details, callback){
    callerName = 'client_coordination_master';
    var request = [
      'ApproveUnit',
      {
        "unit_approval_details": unit_approval_details
      }
    ];
    apiRequest(callerName, request, callback);
  }
  function getClientGroupApprovalList(callback){
    callerName = 'client_coordination_master';
    var request = [
      'GetClientGroupApprovalList',
      {}
    ];
    apiRequest(callerName, request, callback);
  }
  function approveClientGroup(group_approval_details, callback){
    callerName = 'client_coordination_master';
    var request = [
      'ApproveClientGroup',
      {
        "client_group_approval_details": group_approval_details
      }
    ];
    apiRequest(callerName, request, callback);
  }
  function getDbServerList(callback){
    callerName = 'console_admin';
    var request = [
      'GetDbServerList',
      {
      }
    ];
    apiRequest(callerName, request, callback);
  }
  function saveDBServer(
    db_server_name, ip, port, username, password, callback
  ){
    callerName = "console_admin"
    var request = [
      "SaveDBServer",
      {
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
  function getAllocatedDBEnv(callback){
      callerName = "console_admin";
      var request = [
        "GetAllocatedDBEnv",
        {}
      ];
      apiRequest(callerName, request, callback);
  }
  function saveDBEnv(client_id, le_id, db_server_ip, machine_id, callback){
      callerName = "console_admin";
      var request = [
          "SaveAllocatedDBEnv",
          {
            "client_id": client_id,
            "legal_entity_id": le_id,
            "database_server_ip": db_server_ip,
            "machine_id": machine_id
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
  function getUserMappings(callback){
    callerName = "admin";
      var request = [
        "GetUserMappings",
        {}
      ];
      apiRequest(callerName, request, callback);
  }
  function saveUserMappings(country_id, domain_id, parent_user_id, child_users, callback){
    callerName = "admin";
    var request = [
      "SaveUserMappings",
      {
        "country_id": country_id,
        "domain_id": domain_id,
        "parent_user_id": parent_user_id,
        "child_users": child_users
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
  function getAssignedUnitsList(domain_id, client_id, callback){
    callerName = "techno";
    var request = [
      "GetAssignedUnits",
      {
        "domain_id": domain_id,
        "client_id": client_id
      }
    ];
    apiRequest(callerName, request, callback);
  }
  function getAssignedUnitDetails(legal_entity_id, domain_manager_id, callback){
    callerName = "techno";
    var request = [
      "GetAssignedUnitDetails",
      {
        "legal_entity_id": legal_entity_id,
        "user_id": domain_manager_id
      }
    ];
    apiRequest(callerName, request, callback);
  }
  function getAssignUnitFormData(domain_id, client_id, callback){
    callerName = "techno";
    var request = [
      "GetAssignUnitFormData",
      {
        "domain_id": domain_id,
        "client_id": client_id
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
  function getReassignUserAccountFormdata(callback){
    callerName = "admin";
    var request = [
        "GetReassignUserAccountFormdata",
        {}
      ];
      apiRequest(callerName, request, callback);
  }
  function saveReassignUserAccount(
    user_type, old_user_id, new_user_id, assigned_ids, remarks, callback
  ){
      callerName = "admin";
      var request = [
        "SaveReassignUserAccount",
        {
          "user_type": user_type,
          "old_user_id": old_user_id,
          "new_user_id": new_user_id,
          "assigned_ids": assigned_ids,
          "remarks": remarks
        }
      ];
      apiRequest(callerName, request, callback);
  }
  function getAssignStatutoryWizardOneData(callback){
    callerName = 'techno_transaction';
    var request = [
      "GetAssignedStatutoryWizardOneData",
      {}
    ];
    apiRequest(callerName, request, callback);
  }

  function getAssignStatutoryWizardTwoData(
    client_id, business_group_id, legal_entity_id, division_id, category_id,
    domain_id, unit_ids, callback
  ){
      callerName = 'techno_transaction';
      var request = [
        "GetAssignedStatutoryWizardTwoData",
        {
          "client_id": client_id,
          "business_group_id": business_group_id,
          "legal_entity_id": legal_entity_id,
          "division_id": division_id,
          "category_id": category_id,
          "domain_id_optional": domain_id,
          "unit_ids": unit_ids
        }
      ];
      apiRequest(callerName, request, callback);
  }

  function saveAssignedStatutory(
    client_statutory_id, units, client_id, unit_ids, compliances_list,
    level_1_statutory_wise_compliances, callback
  ){
    callerName = 'techno_transaction';
    var request = [
        "SaveAssignedStatutory",
        {
          "client_statutory_id": client_statutory_id,
          "unit_id_name": units,
          "client_id": client_id,
          "unit_ids": unit_ids,
          "compliances_applicablity_status": compliances_list,
          "level_1_statutory_wise_compliances": level_1_statutory_wise_compliances,
          "submission_type": "save"
        }
      ];
      apiRequest(callerName, request, callback);
  }

  function submitAssignedStatutory(
    client_statutory_id, units, client_id, unit_ids, compliances_list, level_1_statutory_wise_compliances, callback
  ){
    callerName = 'techno_transaction';
    var request = [
        "SaveAssignedStatutory",
        {
          "client_statutory_id": client_statutory_id,
          "unit_id_name": units,
          "client_id": client_id,
          "unit_ids": unit_ids,
          "compliances_applicablity_status": compliances_list,
          "level_1_statutory_wise_compliances": level_1_statutory_wise_compliances,
          "submission_type": "submit"
        }
      ];
      apiRequest(callerName, request, callback);
  }

  function getAssignedStatutories(callback){
    callerName = 'techno_transaction';
    var request = [
        "GetAssignedStatutories",
        {}
      ];
    apiRequest(callerName, request, callback);
  }

  function getAssignedStatutoriesById(client_statutory_id, callback){
    callerName = 'techno_transaction';
    var request = [
        "GetAssignedStatutoriesById",
        {
          "client_statutory_id": client_statutory_id
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

  function getUsermappingDetailsReport(countryId, clientId, legalEntityId, u_m_none, callback) {
    callerName = 'techno_report';
    var request = [
      'GetUserMappingDetailsReportData',
      {
        'country_id': countryId,
        'client_id': clientId,
        'legal_entity_id': legalEntityId,
        'u_m_none': u_m_none,
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
    //apiRequest(callerName, request, callback);
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

  function getClientAgreementReport(countryId, clientId, businessGroupId, legalEntityId, domainId, contractFrom, contractTo, csv, from_count, page_count, callback) {
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
        'page_count': page_count
      }
    ];
    apiRequest(callerName, request, callback);
  }

  function getDomainwiseAgreementReport(countryId, clientId, businessGroupId, legalEntityId, domainId, contractFrom, contractTo, csv, from_count, page_count, callback) {
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
        'page_count': page_count
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

  return {
    log: log,
    toJSON: toJSON,
    parseJSON: parseJSON,
    getBaseUrl: getBaseUrl,
    initSession: initSession,
    clearSession: clearSession,
    verifyLoggedIn: verifyLoggedIn,
    logout: logout,
    getEmployeeName: getEmployeeName,
    getUserId: getUserId,
    getUserInfo: getUserInfo,
    updateUserInfo: updateUserInfo,
    getUserProfile: getUserProfile,
    getSessionToken: getSessionToken,
    getUserMenu: getUserMenu,
    getPageUrl: getPageUrl,
    apiRequest: apiRequest,
    LoginApiRequest: LoginApiRequest,
    saveDomain: saveDomain,
    updateDomain: updateDomain,
    changeDomainStatus: changeDomainStatus,
    getDomainList: getDomainList,
    getDomainReport: getDomainReport,
    saveCountry: saveCountry,
    updateCountry: updateCountry,
    changeCountryStatus: changeCountryStatus,
    getCountryList: getCountryList,
    getCountryListForUser: getCountryListForUser,
    getCountryReport: getCountryReport,
    getSaveIndustryDict: getSaveIndustryDict,
    saveIndustry: saveIndustry,
    getUpdateIndustryDict:getUpdateIndustryDict,
    updateIndustry: updateIndustry,
    changeIndustryStatus: changeIndustryStatus,
    getIndustryList: getIndustryList,
    getSaveStatutoryNatureDict: getSaveStatutoryNatureDict,
    saveStatutoryNature: saveStatutoryNature,
    getUpdateStatutoryNatureDict: getUpdateStatutoryNatureDict,
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
    uploadFile: uploadFile,
    uploadFileFormat: uploadFileFormat,
    complianceDetails: complianceDetails,
    statutoryMapping: statutoryMapping,
    checkDuplicateStatutoryMapping: checkDuplicateStatutoryMapping,
    saveStatutoryMapping: saveStatutoryMapping,
    updateStatutoryMapping: updateStatutoryMapping,
    getStatutoryMaster: getStatutoryMaster,
    getStatutoryMappingsMaster: getStatutoryMappingsMaster,
    getStatutoryMappings: getStatutoryMappings,
    changeStatutoryMappingStatus: changeStatutoryMappingStatus,
    approveStatutoryList: approveStatutoryList,
    approveStatutoryMapping: approveStatutoryMapping,
    getStatutoryMappingsReportFilter: getStatutoryMappingsReportFilter,
    filterData: filterData,
    getStatutoryMappingsReportData: getStatutoryMappingsReportData,
    getApproveStatutoryMapings: getApproveStatutoryMapings,
    getComplianceInfo: getComplianceInfo,
    getSaveAdminUserGroupDict: getSaveAdminUserGroupDict,
    saveAdminUserGroup: saveAdminUserGroup,
    getUpdateAdminUserGroupDict: getUpdateAdminUserGroupDict,
    updateAdminUserGroup: updateAdminUserGroup,
    changeAdminUserGroupStatus: changeAdminUserGroupStatus,
    getAdminUserGroupList: getAdminUserGroupList,
    getSaveAdminUserDict: getSaveAdminUserDict,
    saveAdminUser: saveAdminUser,
    sendRegistration: sendRegistration,
    getUpdateAdminUserDict: getUpdateAdminUserDict,
    updateAdminUser: updateAdminUser,
    changeAdminUserStatus: changeAdminUserStatus,
    getAdminUserList: getAdminUserList,
    getDateConfigurations: getDateConfigurations,
    saveClientGroup: saveClientGroup,
    updateClientGroup: updateClientGroup,
    getClientGroups: getClientGroups,
    changeClientGroupStatus: changeClientGroupStatus,
    getAssignLegalEntityList: getAssignLegalEntityList,
    getEditAssignLegalEntity: getEditAssignLegalEntity,
    saveAssignLegalEntity: saveAssignLegalEntity,
    viewAssignLegalEntity: viewAssignLegalEntity,
    changePassword: changePassword,
    forgotPassword: forgotPassword,
    validateResetToken: validateResetToken,
    resetPassword: resetPassword,
    getClients: getClients,
    getBusinessGroupDict: getBusinessGroupDict,
    getLegalEntityDict: getLegalEntityDict,
    getDivisionDict: getDivisionDict,
    getUnitDict: getUnitDict,
    mapUnitsToCountry: mapUnitsToCountry,
    saveClient: saveClient,
    updateClient: updateClient,
    changeClientStatus: changeClientStatus,
    reactivateUnit: reactivateUnit,
    getClientProfile: getClientProfile,
    getClientDetailsReportFilters: getClientDetailsReportFilters,
    getClientDetailsReport: getClientDetailsReport,
    getAssignedStatutoryReportFilters: getAssignedStatutoryReportFilters,
    getAssignedStatutoryReport: getAssignedStatutoryReport,
    getStatutoryNotificationsFilters: getStatutoryNotificationsFilters,
    getStatutoryNotificationsReportData: getStatutoryNotificationsReportData,
    getComplianceTaskFilter: getComplianceTaskFilter,
    getComplianceTaskReport: getComplianceTaskReport,
    get_ip: get_ip,
    getAuditTrail: getAuditTrail,
    getAuditTrailFilter: getAuditTrailFilter,
    updateUserProfile: updateUserProfile,
    getNotifications: getNotifications,
    updateNotificationStatus: updateNotificationStatus,
    createNewAdmin: createNewAdmin,
    getNextUnitCode: getNextUnitCode,
    uploadFormatFile: uploadFormatFile,
    getValidityDateList: getValidityDateList,
    get_validity_day_setting: get_validity_day_setting,
    saveValidityDateSettings: saveValidityDateSettings,
    getClientGroupFormData: getClientGroupFormData,
    getLegalEntityRow: getLegalEntityRow,
    getDomainRow: getDomainRow,
    getEditClientGroupFormData: getEditClientGroupFormData,
    getLegalEntityUpdateRow: getLegalEntityUpdateRow,
    getClientUnitApprovalList: getClientUnitApprovalList,
    getEntityApprovalList: getEntityApprovalList,
    approveUnit: approveUnit,
    getClientGroupApprovalList: getClientGroupApprovalList,
    approveClientGroup: approveClientGroup,
    getDbServerList: getDbServerList,
    saveDBServer: saveDBServer,
    getClientServerList: getClientServerList,
    saveClientServer: saveClientServer,
    getAllocatedDBEnv: getAllocatedDBEnv,
    saveDBEnv: saveDBEnv,
    getFileStorage: getFileStorage,
    saveFileStorage: saveFileStorage,
    getAutoDeletionList: getAutoDeletionList,
    saveAutoDeletion: saveAutoDeletion,
    getUserMappings: getUserMappings,
    saveUserMappings: saveUserMappings,
    getUnassignedUnitsList: getUnassignedUnitsList,
    getAssignedUnitsList: getAssignedUnitsList,
    getAssignedUnitDetails: getAssignedUnitDetails,
    getAssignUnitFormData: getAssignUnitFormData,
    saveAssignedUnits: saveAssignedUnits,
    getReassignUserAccountFormdata: getReassignUserAccountFormdata,
    saveReassignUserAccount: saveReassignUserAccount,
    getAssignStatutoryWizardOneData: getAssignStatutoryWizardOneData,
    getAssignStatutoryWizardTwoData: getAssignStatutoryWizardTwoData,
    saveAssignedStatutory: saveAssignedStatutory,
    submitAssignedStatutory: submitAssignedStatutory,
    getAssignedStatutories: getAssignedStatutories,
    getAssignedStatutoriesById: getAssignedStatutoriesById,
    changeAdminDisaleStatus: changeAdminDisaleStatus,
    getUserMappingReportFilters: getUserMappingReportFilters,
    getUsermappingDetailsReport: getUsermappingDetailsReport,
    getGroupAdminGroupList: getGroupAdminGroupList,
    sendGroupAdminRegnmail: sendGroupAdminRegnmail,
    resendGroupAdminRegnmail: resendGroupAdminRegnmail,
    getGroupAdminReportData: getGroupAdminReportData,
    getAssignedUserClientGroups: getAssignedUserClientGroups,
    getReassignUserReportData: getReassignUserReportData,
    getLegalEntityClosureData: getLegalEntityClosureData,
    saveLegalEntityClosureData: saveLegalEntityClosureData,
    verifyPassword: verifyPassword,
    getClientAgreementReportFilters: getClientAgreementReportFilters,
    getClientAgreementReport: getClientAgreementReport,
    getDomainwiseAgreementReport: getDomainwiseAgreementReport,
    getOrganizationWiseUnitCount: getOrganizationWiseUnitCount

  };
}
var mirror = initMirror();
