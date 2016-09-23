// var BASE_URL = "http://127.0.0.1:8082/";
var BASE_URL = '/knowledge/api/';
var login_url = '/knowledge/login';
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
      user = parseJSON(info);
    }
    return user;
  }
  function updateUserInfo(response) {
    var info = getUserInfo();
    info.contact_no = response.contact_no;
    info.address = response.address;
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
      'address': info.address,
      'designation': info.designation
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
      frm = window.location.href;  // if (frm.indexOf("knowledge") > -1)
                                   //     window.location.href = "/knowledge/login";
                                   // else
                                   //     window.location.href = "/login/" + window.localStorage["recent_short_name"];
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
      // headers: {'X-Xsrftoken': getCookie('_xsrf')},
      type: 'POST',
      contentType: 'application/json',
      data: toJSON(requestFrame),
      success: function (data) {
        var data = parseJSON(data);
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
      type: 'POST',
      contentType: 'application/json',
      data: toJSON(request),
      success: function (data) {
        var data = parseJSON(data);
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
      // headers: {'X-Xsrftoken' : getCookie('_xsrf')},
      type: 'POST',
      contentType: 'application/json',
      data: toJSON(request),
      success: function (data) {
        var data = parseJSON(data);
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
  function saveDomain(dName, callback) {
    var request = [
      'SaveDomain',
      { 'd_name': dName }
    ];
    apiRequest('general', request, callback);
  }
  function updateDomain(dId, dName, callback) {
    var request = [
      'UpdateDomain',
      {
        'd_id': dId,
        'd_name': dName
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
  function getCountriesForGroup(callback) {
    var request = [
      'GetCountriesForGroup',
      {}
    ];
    apiRequest('techno_transaction', request, callback);
  }
  //Industry Master
  function getSaveIndustryDict(industryDetail) {
    var cIds = industryDetail[0];
    var dIds = industryDetail[1];
    var i_name = industryDetail[2];
    return {
      'c_ids': cIds,
      'd_ids': dIds,
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
      'c_ids': cIds,
      'd_ids': dIds,
      'i_ids': iIds,
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
      'c_ids': cIds
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
      's_n_ids': snIds,
      's_n_name': snName,
      'c_ids': cIds
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
        'p_ids': pIds,
        'p_names': pNames
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
  function uploadFile(fileListener, callback) {
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
            callback(result);
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
  function getStatutoryMappingsMaster(callback) {
    var request = [
      'GetStatutoryMappingsMaster',
      {}
    ];
    apiRequest('knowledge_transaction', request, callback);
  }
  function getStatutoryMappings(callback) {
    var request = [
      'GetStatutoryMappings',
      {}
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
  function changeAdminUserGroupStatus(ugId, active, callback) {
    callerName = 'admin';
    var request = [
      'ChangeUserGroupStatus',
      {
        'ug_id': ugId,
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
    var email = userDetail[0];
    var ugId = userDetail[1];
    var empN = userDetail[2];
    var empC = userDetail[3];
    var cNo = userDetail[4];
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
      'email': email,
      'ug_id': ugId,
      'emp_n': empN,
      'emp_c': empC,
      'c_n': cNo,
      'add': add,
      'desig': desig,
      'c_ids': cIds,
      'd_ids': dIds
    };
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
      'u_id': uId,
      'ug_id': ugId,
      'emp_n': empN,
      'emp_c': empC,
      'c_n': cn,
      'add': add,
      'desig': desig,
      'c_ids': cIds,
      'd_ids': dIds
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
        'u_id': uId,
        'active': active
      }
    ];
    apiRequest(callerName, request, callback);
  }
  // Client Group Master
  function getDateConfigurations(cId, dId, pFrom, pTo) {
      return {
        'c_id': cId,
        'd_id': dId,
        'p_from': pFrom,
        'p_to': pTo
      };
  }

  function getDomainRow(
    d_id, org
  ){
      return {
        "d_id": d_id,
        "org": org
      }
  }

  function getLegalEntityRow(
    c_id, b_g_id, b_g_name, l_e_name,
    inc_p, logo, n_o_l, f_s, sms, c_f, c_t, d
  ) {
    return {
        "c_id": c_id,
        "b_g": {
            "b_g_id": b_g_id,
            "b_g_name": b_g_name
        },
        "l_e_name": l_e_name,
        "inc_p": inc_p,
        "logo": logo,
        "n_o_l": n_o_l,
        "f_s": f_s,
        "sms": sms,
        "c_f": c_f,
        "c_t": c_t,
        "d": d
    };
  }
  function saveClientGroup(
    g_name, u_name, les, d_cs, callback) {
    callerName = 'techno';
    var request = [
      'SaveClientGroup',
      {
        "g_name": g_name,
        "u_name": u_name,
        "les": les,
        "d_cs": d_cs
      }
    ];
    apiRequest(callerName, request, callback);
  }
  function getUpdateClientGroupDict(cId, gName, cIds, dIds, logo, cFrom, cTo, incharge, licence, fSpace, sms, config) {
    return {
      'c_id': cId,
      'g_name': gName,
      'c_ids': cIds,
      'd_ids': dIds,
      'logo': logo,
      'c_from': cFrom,
      'c_to': cTo,
      'incharge': incharge,
      'licence': licence,
      'f_space': fSpace,
      'sms': sms,
      'config': config
    };
  }
  function updateClientGroup(clientGroupDetails, callback) {
    callerName = 'techno';
    var request = [
      'UpdateClientGroup',
      clientGroupDetails
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
  function getEditClientGroupFormData(callback) {
    callerName = 'techno';
    var request = [
      'GetEditClientGroupFormData',
      {}
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
    if (bgName == null || bgName == '') {
      return null;
    } else {
      return {
        'bg_id': bgId,
        'bg_name': bgName
      };
    }
  }
  function getLegalEntityDict(leId, leName) {
    return {
      'le_id': leId,
      'le_name': leName
    };
  }
  function getDivisionDict(dId, dName) {
    if (dName == null || dName == '') {
      return null;
    } else {
      return {
        'd_id': dId,
        'd_name': dName
      };
    }
  }
  function getUnitDict(uId, uName, uCode, uAdd, pCode, geoId, uLoc, iId, iName, dIds) {
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
  }
  function mapUnitsToCountry(cId, units) {
    return {
      'c_id': cId,
      'units': units
    };
  }
  function saveClient(cId, bg, le, d, cw_units, callback) {
    callerName = 'techno';
    var request = [
      'SaveClient',
      {
        'c_id': cId,
        'bg': bg,
        'le': le,
        'd': d,
        'cw_units': cw_units
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
  // Assign statutories
  function getAssignStatutoryWizardOne(countryId, callback) {
    var request = [
      'GetAssignedStatutoryWizardOneData',
      { 'country_id': countryId }
    ];
    callerName = 'techno_transaction';
    apiRequest(callerName, request, callback);
  }
  function getAssignStatutoryWizardTwo(countryId, domainId, industryId, geographyId, unitId, callback) {
    var request = [
      'GetStatutoryWizardTwoData',
      {
        'country_id': countryId,
        'domain_id': domainId,
        'industry_id': industryId,
        'geography_id': geographyId,
        'unit_id': unitId
      }
    ];
    callerName = 'techno_transaction';
    apiRequest(callerName, request, callback);
  }
  function getAssignedStatutoriesList(callback) {
    var request = [
      'GetAssignedStatutoriesList',
      {}
    ];
    callerName = 'techno_transaction';
    apiRequest(callerName, request, callback);
  }
  function assignedStatutories(l1ID, compliances, aStatus, remarks) {
    var statutories = {
      'level_1_s_id': l1ID,
      'compliances': compliances,
      'a_status': aStatus,
      'n_a_remarks': remarks
    };
    return statutories;
  }
  function saveOrSubmitAssignStatutory(cId, clientId, geoId, uIds, dId, subType, cSId, asStatutories, callback) {
    var request = [
      'SaveAssignedStatutory',
      {
        'c_id': cId,
        'client_id': clientId,
        'g_id': geoId,
        'u_ids': uIds,
        'd_id': dId,
        'sub_type': subType,
        'c_s_id': cSId,
        'a_statutories': asStatutories
      }
    ];
    callerName = 'techno_transaction';
    apiRequest(callerName, request, callback);
  }
  function getAssignedStatutoryById(clientStatutoryId, callback) {
    var request = [
      'GetAssignedStatutoriesById',
      { 'client_statutory_id': clientStatutoryId }
    ];
    callerName = 'techno_transaction';
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
  function getAssignedStatutoryReport(cId, dId, clientId, bGroupId, lEntityId, divId, uId, level1SId, aStatus, callback) {
    var request = [
      'GetAssignedStatutoryReport',
      {
        'c_id': cId,
        'd_id': dId,
        'g_id': clientId,
        'b_group_id': bGroupId,
        'l_entity_id': lEntityId,
        'div_id': divId,
        'u_id': uId,
        'level_1_s_id': level1SId,
        'a_status': aStatus
      }
    ];
    callerName = 'techno_report';
    apiRequest(callerName, request, callback);
  }
  function getAuditTrail(fromDate, toDate, userId, formId, recordCount, pageCount, callback) {
    callerName = 'general';
    var request = [
      'GetAuditTrails',
      {
        'from_date': fromDate,
        'to_date': toDate,
        'user_id': userId,
        'form_id': formId,
        'record_count': recordCount,
        'page_count': pageCount
      }
    ];
    apiRequest(callerName, request, callback);
  }
  function updateUserProfile(contact_no, address, callback) {
    callerName = 'general';
    var request = [
      'UpdateUserProfile',
      {
        'contact_no': contact_no,
        'address': address
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
      type: 'POST',
      crossDomain: true,
      data: formdata,
      processData: false,
      contentType: false,
      success: function (data, textStatus, jqXHR) {
        var data = parseJSON(data);
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

  return {
    log: log,
    toJSON: toJSON,
    parseJSON: parseJSON,
    getBaseUrl: getBaseUrl,
    initSession: initSession,
    // updateUser_Session: updateUser_Session,
    clearSession: clearSession,
    verifyLoggedIn: verifyLoggedIn,
    // login: login,
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
    getCountriesForGroup: getCountriesForGroup,
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
    getStatutoryMappingsMaster: getStatutoryMappingsMaster,
    getStatutoryMappings: getStatutoryMappings,
    changeStatutoryMappingStatus: changeStatutoryMappingStatus,
    approveStatutoryList: approveStatutoryList,
    approveStatutoryMapping: approveStatutoryMapping,
    getStatutoryMappingsReportFilter: getStatutoryMappingsReportFilter,
    filterData: filterData,
    getStatutoryMappingsReportData: getStatutoryMappingsReportData,
    getApproveStatutoryMapings: getApproveStatutoryMapings,
    getSaveAdminUserGroupDict: getSaveAdminUserGroupDict,
    saveAdminUserGroup: saveAdminUserGroup,
    getUpdateAdminUserGroupDict: getUpdateAdminUserGroupDict,
    updateAdminUserGroup: updateAdminUserGroup,
    changeAdminUserGroupStatus: changeAdminUserGroupStatus,
    getAdminUserGroupList: getAdminUserGroupList,
    getSaveAdminUserDict: getSaveAdminUserDict,
    saveAdminUser: saveAdminUser,
    getUpdateAdminUserDict: getUpdateAdminUserDict,
    updateAdminUser: updateAdminUser,
    changeAdminUserStatus: changeAdminUserStatus,
    getAdminUserList: getAdminUserList,
    getDateConfigurations: getDateConfigurations,
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
    getAssignStatutoryWizardOne: getAssignStatutoryWizardOne,
    getAssignStatutoryWizardTwo: getAssignStatutoryWizardTwo,
    getAssignedStatutoriesList: getAssignedStatutoriesList,
    assignedStatutories: assignedStatutories,
    saveOrSubmitAssignStatutory: saveOrSubmitAssignStatutory,
    getAssignedStatutoryById: getAssignedStatutoryById,
    getAssignedStatutoryReportFilters: getAssignedStatutoryReportFilters,
    getAssignedStatutoryReport: getAssignedStatutoryReport,
    getStatutoryNotificationsFilters: getStatutoryNotificationsFilters,
    getStatutoryNotificationsReportData: getStatutoryNotificationsReportData,
    getComplianceTaskFilter: getComplianceTaskFilter,
    getComplianceTaskReport: getComplianceTaskReport,
    get_ip: get_ip,
    getAuditTrail: getAuditTrail,
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
    getClientUnitApprovalList: getClientUnitApprovalList

  };
}
var mirror = initMirror();