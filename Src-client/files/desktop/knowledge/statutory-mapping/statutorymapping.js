var statutoryMappingsList;
var geographyLevelsList;
var geographiesList;
var countriesList;
var domainsList;
var industriesList;
var statutoryNaturesList;
var statutoryLevelsList;
var statutoriesList;
var complianceFrequencyList;
var complianceDurationTypeList;
var complianceRepeatTypeList;
var complianceApprovalStatusList;
var sm_countryid = '';
var sm_domainid = '';
var sm_statutorynatureid = '';
var sm_industryids = [];
var sm_countryval = '';
var sm_domainval = '';
var sm_industryvals = [];
var sm_statutorynatureval = '';
var sm_statutoryids = [];
var disp_statutories = [];
var statutory_dates = [];
var sm_geographyids = [];
var compliances = [];
var uploadFile = null;
var isAllComplianceActive;
var finalList;
var pageSize = 50;
var startCount;
var endCount;
var editLevel = '';
var file_lst = [];
var f_Name = '';
var f_Size = '';
var f_Content = null;
var form_data = new FormData();
var complianceid = 0;
var isUpload = false;

function displayLoader() {
  $('.loading-indicator-spin').show();
}
function hideLoader() {
  $('.loading-indicator-spin').hide();
}
function resetvalues() {
  $('.sdate').val('');
}
function load_selectdomain_master() {
  //load country details
  var clsval = '.countrylist';
  var clsval1 = 'countrylist';
  var str = '';
  $('#country').empty();
  for (var country in countriesList) {
    var countryid = countriesList[country].country_id;
    var dispcountryname = countriesList[country].country_name;
    if (countriesList[country].is_active == true) {
      str += '<li id="' + countryid + '" class="' + clsval1 + '" onclick="activate(this,' + '\'' + clsval + '\')" ><span class="filter1_name">' + dispcountryname + '</span></li>';
    }
  }
  $('#country').append(str);
  //load domain details
  var clsval = '.domainlist';
  var clsval1 = 'domainlist';
  var str = '';
  $('#domain').empty();
  for (var domain in domainsList) {
    var domainid = domainsList[domain].domain_id;
    var dispdomainname = domainsList[domain].domain_name;
    if (domainsList[domain].is_active == true) {
      str += '<li id="' + domainid + '" class="' + clsval1 + '" onclick="activate(this,' + '\'' + clsval + '\')" ><span class="filter2_name">' + dispdomainname + '</span></li>';
    }
  }
  $('#domain').append(str);
  //load industry details
  var clsval = '.industrylist';
  var clsval1 = 'industrylist';
  var str = '';
  $('#industry').empty();
  for (var industry in industriesList) {
    var industryid = industriesList[industry].industry_id;
    var dispindustryname = industriesList[industry].industry_name;
    if (industriesList[industry].is_active == true) {
      str += '<li id="' + industryid + '" class="' + clsval1 + '" onclick="multiactivate(this,' + '\'' + clsval + '\')" ><span class="filter3_name">' + dispindustryname + '</span></li>';
    }
  }
  $('#industry').append(str);
  //load statutorynature details
  var clsval = '.statutorynaturelist';
  var clsval1 = 'statutorynaturelist';
  var str = '';
  $('#statutorynature').empty();
  for (var statutorynature in statutoryNaturesList) {
    var statutorynatureid = statutoryNaturesList[statutorynature].statutory_nature_id;
    var dispstatutoryname = statutoryNaturesList[statutorynature].statutory_nature_name;
    if (statutoryNaturesList[statutorynature].is_active == true) {
      str += '<li id="' + statutorynatureid + '" class="' + clsval1 + '" onclick="activate(this,' + '\'' + clsval + '\')" ><span class="filter4_name">' + dispstatutoryname + '</span></li>';
    }
  }
  $('#statutorynature').append(str);
  //load compliance frequency selectbox
  $('#compliance_frequency').empty();
  $('#compliance_frequency').append('<option value=""> Select </option>');
  for (var compliancefrequency in complianceFrequencyList) {
    var option = $('<option></option>');
    option.val(complianceFrequencyList[compliancefrequency].frequency_id);
    option.text(complianceFrequencyList[compliancefrequency].frequency);
    $('#compliance_frequency').append(option);
  }
  //load compliance duration type selectbox
  $('#duration_type').empty();
  $('#duration_type').append('<option value=""> Select </option>');
  for (var compliancedurationtype in complianceDurationTypeList) {
    var option = $('<option></option>');
    option.val(complianceDurationTypeList[compliancedurationtype].duration_type_id);
    option.text(complianceDurationTypeList[compliancedurationtype].duration_type);
    $('#duration_type').append(option);
  }
  //load compliance repeat type selectbox
  $('#repeats_type').empty();
  $('#repeats_type').append('<option value=""> Select </option>');
  for (var compliancerepeattype in complianceRepeatTypeList) {
    var option = $('<option></option>');
    option.val(complianceRepeatTypeList[compliancerepeattype].repeat_type_id);
    option.text(complianceRepeatTypeList[compliancerepeattype].repeat_type);
    $('#repeats_type').append(option);
  }
}
$('.btn-statutorymapping-add').click(function () {
  isUpload = false;
  reset_compliance();
  $('#statutorymapping-view').hide();
  $('#statutorymapping-add').show();
  $('#edit_sm_id').val('');
  displayMessage('');
  sm_countryid = '';
  sm_domainid = '';
  sm_statutorynatureid = '';
  sm_countryval = '';
  sm_domainval = '';
  sm_statutorynatureval = '';
  sm_statutoryids = [];
  sm_industryids = [];
  sm_industryvals = [];
  compliances = [];
  load_selectdomain_master();
  $('.tbody-statutory-list').find('tr').remove();
  $('.tbody-compliance-list').find('tr').remove();
  $('.tbody-statutory-level').find('div').remove();
  $('.tbody-geography-level').find('div').remove();
});
//activate/deactivate statutory mapping
function changeStatus(statutorymappingId, isActive) {
  var msgstatus = message.deactive_message;
  if (isActive) {
    msgstatus = message.active_message;
  }
  $('.warning-confirm').dialog({
    title: message.title_status_change,
    buttons: {
      Ok: function () {
        $(this).dialog('close');
        function onSuccess(data) {
          $('.listfilter').val('');
          getStatutoryMappings();
        }
        function onFailure(error) {
          if (error == 'TransactionExists') {
            custom_alert(message.trasaction_exists);
          } else {
            custom_alert(error);
          }
        }
        mirror.changeStatutoryMappingStatus(statutorymappingId, isActive, function (error, response) {
          if (error == null) {
            onSuccess(response);
          } else {
            onFailure(error);
          }
        });
      },
      Cancel: function () {
        $(this).dialog('close');
      }
    },
    open: function () {
      $('.warning-message').html(msgstatus);
    }
  });
}
//load statutory mapping list in view page
function loadCountwiseStatutoryMapping(keysList, statutoryMappingsList) {
  $('#activate-step-finish').prop('disabled', false);
  $('#activate-step-finish').text('Submit');
  $('#activate-step-finish').addClass('btn-right');
  $('#activate-step-finish').removeClass('btn-right-submiting');
  var j = startCount + 1;
  $('.tbody-statutorymapping-list').find('tr').remove();
  if (endCount > Object.keys(finalList).length)
    endCount = Object.keys(finalList).length;
  if (Object.keys(finalList).length > 0)
    $('.view-count-message').text('Showing ' + (startCount + 1) + ' to ' + endCount + ' of ' + Object.keys(finalList).length);
  $.each(keysList, function (key, value) {
    //for(var k=0; k<keysList.length; k++){
    var entity = keysList[key];
    var statutorymappingId = entity;
    var industryName = statutoryMappingsList[entity].industry_names;
    var statutoryNatureName = statutoryMappingsList[entity].statutory_nature_name;
    var statutoryMappings = '';
    for (var i = 0; i < statutoryMappingsList[entity].statutory_mappings.length; i++) {
      statutoryMappings = statutoryMappings + statutoryMappingsList[entity].statutory_mappings[i] + ' <br>';
    }
    var complianceNames = '';
    for (var i = 0; i < statutoryMappingsList[entity].compliance_names.length; i++) {
      complianceNames = complianceNames + statutoryMappingsList[entity].compliance_names[i].compliance_name + ' <br>';
    }
    statutoryMappings = statutoryMappings.replace(/>>/gi, ' <img src=\'/knowledge/images/right_arrow.png\'/> ');
    var countryName = statutoryMappingsList[entity].country_name;
    var domainName = statutoryMappingsList[entity].domain_name;
    var isActive = statutoryMappingsList[entity].is_active;
    var approvalStatus = statutoryMappingsList[entity].approval_status_text;
    var passStatus = null;
    var classValue = null;
    var tableRow = $('#templates .table-statutorymapping .table-row');
    var clone = tableRow.clone();
    $('.sno', clone).text(j);
    $('.country', clone).text(countryName);
    $('.domain', clone).text(domainName);
    $('.industry', clone).text(industryName);
    $('.statutorynature', clone).text(statutoryNatureName);
    $('.statutory', clone).html(statutoryMappings);
    $('.compliancetask', clone).html(complianceNames);
    if (isActive == true) {
      $('.edit-icon').attr('title', 'Edit');
      $('.edit-icon', clone).on('click', function () {
        displayEdit(statutorymappingId);
      });
      passStatus = false;
      classValue = 'active-icon';
    } else {
      $('.edit-icon').attr('title', 'Only active status mapping have edit option');
      passStatus = true;
      classValue = 'inactive-icon';
    }
    $('.status', clone).addClass(classValue);
    $('.active-icon').attr('title', 'Deactivate');
    $('.inactive-icon').attr('title', 'Activate');
    $('.status', clone).on('click', function () {
      changeStatus(parseInt(statutorymappingId), passStatus);
    });
    $('.approvalstatus', clone).text(approvalStatus);
    $('.tbody-statutorymapping-list').append(clone);
    j = j + 1;
  });
}
//get statutory mapping list for selected page
function get_sub_array(object, start, end) {
  if (!end) {
    end = -1;
  }
  return object.slice(start, end);
}
//get list when click pagination button
$('.pagination').click(function (event) {
  var text = $(event.target).attr('id');
  var pageId = text.substring(text.lastIndexOf('w') + 1);
  var type = '.page';
  $(type).each(function (index, el) {
    $(el).removeClass('active');
  });
  $('#pageview' + pageId).addClass('active');
  startCount = pageSize * (pageId - 1);
  endCount = pageSize * pageId;
  var keys_list = Object.keys(finalList);
  var sub_keys_list = get_sub_array(keys_list, startCount, endCount);
  loadCountwiseStatutoryMapping(sub_keys_list, finalList);
});
//create pagination according to statutory mapping list
function loadStatutoryMappingList(statutoryMappingsList) {
  var listSize = Math.ceil(Object.keys(statutoryMappingsList).length / pageSize);
  startCount = 0;
  endCount = pageSize;
  if (Object.keys(statutoryMappingsList).length > 0) {
    var str = '<li id="pview1">\xAB</li>';
    $('.pagination').empty();
    var j;
    for (j = 1; j <= listSize; j++) {
      if (j == 1) {
        str += '<li class="page active" id="pageview' + j + '">' + j + '</li>';
      } else {
        str += '<li class="page" id="pageview' + j + '">' + j + '</li>';
      }
    }
    str += '<li id="pview' + (j - 1) + '">\xBB</li>';
    $('.pagination').append(str);
  } else {
    $('.pagination').empty();
    $('.view-count-message').text('');
  }
  finalList = statutoryMappingsList;
  var keys_list = Object.keys(finalList);
  var sub_keys_list = get_sub_array(keys_list, startCount, endCount);
  loadCountwiseStatutoryMapping(sub_keys_list, finalList);
}
//get statutory mapping master date from api
function getStatutoryMappingsMastersList() {
  mirror.getStatutoryMappingsMaster(function (error, data) {
    if (error == null) {
      industriesList = data.industries;
      statutoryLevelsList = data.statutory_levels;
      statutoriesList = data.statutories;
      countriesList = data.countries;
      domainsList = data.domains;
      geographyLevelsList = data.geography_levels;
      statutoryNaturesList = data.statutory_natures;
      geographiesList = data.geographies;
      complianceFrequencyList = data.compliance_frequency;
      complianceDurationTypeList = data.compliance_duration_type;
      complianceRepeatTypeList = data.compliance_repeat_type;
      complianceApprovalStatusList = data.compliance_approval_status;
    } else {
      console.log(error);
    }
  });
}
//get statitroy mapping lists from api
function getStatutoryMappings() {
  displayLoader();
  mirror.getStatutoryMappings(function (error, data) {
    if (error == null) {
      statutoryMappingsList = data.statutory_mappings;
      loadStatutoryMappingList(statutoryMappingsList);
      hideLoader();
    } else {
      console.log(error);
      custom_alert(error);
      hideLoader();
    }
  });
}
//load statutory levels
function loadStatutoryLevels(countryval, domainval) {
  $('.tbody-statutory-level').find('div').remove();
  if (countryval in statutoryLevelsList && domainval in statutoryLevelsList[countryval]) {
    var statutoryLevelList = statutoryLevelsList[countryval][domainval];
    var levelposition;
    for (var j in statutoryLevelList) {
      levelposition = statutoryLevelList[j].l_position;
      var tableRow = $('#statutory-level-templates');
      var clone = tableRow.clone();
      $('.statutory_title', clone).html('<div class="scrollable">' + statutoryLevelList[j].l_name + '</div>');
      $('.statutory_levelvalue', clone).html('<input type="text" class="filter-text-box" id="statutoryfilter' + levelposition + '" onkeyup="filter_statutory(' + levelposition + ')"> <ul id="statutorylist' + levelposition + '"></ul><div class="bottomfield"><input type="text" maxlength="100" class="input-box addleft" placeholder="" style="width:90%" id="datavalue' + levelposition + '" onkeypress="saverecord(' + levelposition + ',event)"/><span> <a class="addleftbutton popup-link" id="update' + levelposition + '"><img src="/knowledge/images/icon-plus.png" formtarget="_self" onclick="saverecord(' + levelposition + ',\'clickimage\')" /></a></span></div><input type="hidden" id="statutorylevelid' + levelposition + '" value="' + statutoryLevelList[j].l_id + '"/><input type="hidden" id="level' + levelposition + '" value="' + levelposition + '" />');
      $('.tbody-statutory-level').append(clone);
    }
    var setlevelstage = 1;
    $('#datavalue' + setlevelstage).val('');
    $('#statutorylist' + setlevelstage).empty();
    var firstlevelid = $('#statutorylevelid' + setlevelstage).val();
    var str = '';
    var idval = '';
    var clsval = '.slist' + setlevelstage;
    var clsval1 = 'slist' + setlevelstage;
    if (countryval in statutoriesList && domainval in statutoriesList[countryval]) {
      var statutoryList = statutoriesList[countryval][domainval];
      for (var i in statutoryList) {
        var setstatutoryid = statutoryList[i].statutory_id;
        if (statutoryList[i].level_id == firstlevelid) {
          str += '<span class="eslist-filter' + setlevelstage + '" style="float:left;margin-right:5px;margin-left:5px;margin-top:3px;cursor:pointer;" onclick="editstaturoty(' + setstatutoryid + ',\'' + statutoryList[i].statutory_name.replace(/"/gi, '##') + '\',' + setlevelstage + ')"><img src="/knowledge/images/icon-edit.png" style="width:11px;height:11px"/> </span> <li id="' + setstatutoryid + '" class="' + clsval1 + '" onclick="activate_statutorylist(this,' + setstatutoryid + ',\'' + clsval + '\',' + countryval + ',' + domainval + ',' + setlevelstage + ')" >' + statutoryList[i].statutory_name + '</li> ';
        }
      }
    }
    $('#statutorylist' + setlevelstage).append(str);
    $('.addleft').on('input', function (e) {
      this.value = isCommon($(this));
    });
  }
}
//filter process
$('.listfilter').keyup(function () {
  var filter1 = $('#filter1').val().toLowerCase();
  var filter2 = $('#filter2').val().toLowerCase();
  var filter3 = $('#filter3').val().toLowerCase();
  var filter4 = $('#filter4').val().toLowerCase();
  var filter5 = $('#filter5').val().toLowerCase();
  var filter6 = $('#filter6').val().toLowerCase();
  var filteredList = {};
  if ((filter1 == '' || filter1.length >= 3) && (filter2 == '' || filter2.length >= 3) && (filter3 == '' || filter3.length >= 3) && (filter4 == '' || filter4.length >= 3) && (filter5 == '' || filter5.length >= 3) && (filter6 == '' || filter6.length >= 3)) {
    for (var entity in statutoryMappingsList) {
      var filter1val = statutoryMappingsList[entity].country_name;
      var filter2val = statutoryMappingsList[entity].domain_name;
      var filter3val = statutoryMappingsList[entity].industry_names;
      var filter4val = statutoryMappingsList[entity].statutory_nature_name;
      var filter5val = '';
      for (var i = 0; i < statutoryMappingsList[entity].statutory_mappings.length; i++) {
        filter5val = filter5val + statutoryMappingsList[entity].statutory_mappings[i] + ' <br>';
      }
      var filter6val = '';
      for (var i = 0; i < statutoryMappingsList[entity].compliance_names.length; i++) {
        filter6val = filter6val + statutoryMappingsList[entity].compliance_names[i].compliance_name + ' <br>';
      }
      if (~filter1val.toLowerCase().indexOf(filter1) && ~filter2val.toLowerCase().indexOf(filter2) && ~filter3val.toLowerCase().indexOf(filter3) && ~filter4val.toLowerCase().indexOf(filter4) && ~filter5val.toLowerCase().indexOf(filter5) && ~filter6val.toLowerCase().indexOf(filter6)) {
        filteredList[entity] = statutoryMappingsList[entity];
      }
    }
    loadStatutoryMappingList(filteredList);
  }
});
//check & uncheck list data for single selection
function activate(element, type) {
  var dispname = $(element).text();
  var id = parseInt($(element).attr('id'));
  $(type).each(function (index, el) {
    $(el).removeClass('active');
  });
  $(element).addClass('active');
  var checkbox_status = $(element).attr('class');
  if (checkbox_status == 'countrylist active') {
    sm_countryid = id;
    sm_countryval = dispname;
  }
  if (checkbox_status == 'domainlist active') {
    sm_domainid = id;
    sm_domainval = dispname;
  }
  if (checkbox_status == 'statutorynaturelist active') {
    sm_statutorynatureid = id;
    sm_statutorynatureval = dispname;
  }
  if (sm_countryid != '' && sm_domainid != '' && type != '.statutorynaturelist') {
    loadStatutoryLevels(sm_countryid, sm_domainid);
    sm_statutoryids = [];
    load_statories();
    $('ul.setup-panel li:eq(0)').addClass('active');
    $('ul.setup-panel li:eq(1)').addClass('disabled');
    $('ul.setup-panel li:eq(2)').addClass('disabled');
    $('ul.setup-panel li:eq(3)').addClass('disabled');
  }
  if (sm_countryid != '' && type != '.statutorynaturelist') {
    loadGeographyLevels(sm_countryid);
  }
  make_breadcrumbs();
}
//check & uncheck list data for multi selection
function multiactivate(element, type) {
  var dispname = $(element).text();
  var id = parseInt($(element).attr('id'));
  var chkstatus = $(element).attr('class');
  if (chkstatus == 'industrylist active') {
    $(element).removeClass('active');
    var removeid = sm_industryids.indexOf(id);
    sm_industryids.splice(removeid, 1);
    var removename = sm_industryvals.indexOf(dispname);
    sm_industryvals.splice(removename, 1);
  } else {
    $(element).addClass('active');
    sm_industryids.push(id);
    sm_industryvals.push(dispname);
  }
  make_breadcrumbs();
}
function make_breadcrumbs() {
  var arrowimage = ' <img src=\'/knowledge/images/right_arrow.png\'/> ';
  $('.breadcrumbs_1').html(sm_countryval + arrowimage + sm_domainval + arrowimage + sm_industryvals + arrowimage + sm_statutorynatureval);
}
//check & uncheck list data
function activate_statutorylist(element, id, type, country, domain, level) {
  $(type).each(function (index, el) {
    $(el).removeClass('active');
  });
  $(element).addClass('active');
  load(id, level, country, domain);
}
//load statutory sub level data dynamically
function load(id, level, country, domain) {
  var levelstages = parseInt(level) + 1;
  for (var k = levelstages; k <= 10; k++) {
    var setlevelstage = k;
    if ($('#statutoryid').val() == '') {
      $('#datavalue' + setlevelstage).val('');
    }
    $('#statutorylist' + setlevelstage).empty();
    var str = '';
    var idval = '';
    var clsval = '.slist' + setlevelstage;
    var clsval1 = 'slist' + setlevelstage;
    var levelid = $('#statutorylevelid' + setlevelstage).val();
    var statutoryList = statutoriesList[country][domain];
    for (var i in statutoryList) {
      var setstatutoryid = statutoryList[i].statutory_id;
      if (id == statutoryList[i].parent_id && statutoryList[i].level_id == levelid) {
        str += '<span class="eslist-filter' + setlevelstage + '" style="float:left;margin-right:5px;margin-left:5px;margin-top:3px;cursor:pointer;" onclick="editstaturoty(' + setstatutoryid + ',\'' + statutoryList[i].statutory_name.replace(/"/gi, '##') + '\',' + setlevelstage + ')"><img src="/knowledge/images/icon-edit.png" style="width:11px;height:11px"/></span> <li id="' + setstatutoryid + '" class="' + clsval1 + '" onclick="activate_statutorylist(this,' + setstatutoryid + ',\'' + clsval + '\',' + country + ',' + domain + ',' + setlevelstage + ')" >' + statutoryList[i].statutory_name + '</li> ';
      }
    }
    $('#statutorylist' + setlevelstage).append(str);
  }
}
//remove uploaded file
function remove_temp_file(edit_id) {
  form_data.delete('file' + edit_id);
  uploadFile = null;
  $('#uploaded_fileview').hide();
  $('#uploaded_filename').html('');
  $('#upload_file').val('');
}
//convert file to object on upload file
file_type = [
  'exe',
  'xhtml',
  'htm',
  'html',
  'php',
  'py',
  'pyc',
  'sql',
  'xml',
  'css',
  'java',
  'apk',
  'javac',
  'asp'
];
$('#upload_file').on('change', function (e) {
  var tFN = this.files[0].name;
  var fN = tFN.substring(0, tFN.indexOf('.'));
  var fE = tFN.substring(tFN.lastIndexOf('.') + 1);
  var uniqueId = Math.floor(Math.random() * 90000) + 10000;
  f_Name = fN + '-' + uniqueId + '.' + fE;
  f_Size = this.files[0].size;
  var max_limit = 1024 * 1024 * 50;
  if (tFN.indexOf('.') !== -1) {
    if (f_Size > max_limit) {
      displayMessage(message.file_maxlimit_exceed);
      $('#uploaded_fileview').hide();
      $('#uploaded_filename').html('');
      $('#upload_file').val('');
    } else if (file_type.indexOf(fE) > -1) {
      displayMessage(message.invalid_file_format);
      $('#uploaded_fileview').hide();
      $('#uploaded_filename').html('');
      $('#upload_file').val('');
    } else {
      file_lst = e.target.files;
      displayMessage('');
      $('#uploaded_fileview').show();
      $('#uploaded_filename').html(tFN + '   <img src=\'/knowledge/images/close-icon-black.png\' onclick=\'remove_temp_file()\' />');
    }
  } else {
    displayMessage(message.invalid_file_format);
    $('#uploaded_fileview').hide();
    $('#uploaded_filename').html('');
    $('#upload_file').val('');
  }  /*mirror.uploadFile(e, function result_data(data) {
    if (data == "File max limit exceeded") {
      displayMessage(message.file_maxlimit_exceed)
      $("#uploaded_fileview").hide();
      $("#uploaded_filename").html('');
      $("#upload_file").val('');
    }else if(data == "File content is empty"){
      displayMessage(message.file_content_empty)
      $("#uploaded_fileview").hide();
      $("#uploaded_filename").html('');
      $("#upload_file").val('');
    }else if(data == "Invalid file format"){
      displayMessage(message.invalid_file_format)
      $("#uploaded_fileview").hide();
      $("#uploaded_filename").html('');
      $("#upload_file").val('');
    }else{
      uploadFile = data;
      displayMessage("");
      $("#uploaded_fileview").show();
      $("#uploaded_filename").html( data["file_name"] + "   <img src=\'/images/close-icon-black.png\' onclick='remove_temp_file()' />")
    }
  });*/
});
//validate and insert records in statutory table
function saverecord(j, e) {
  var data = e.keyCode;
  if (data == 13 || data == undefined) {
    var checkLength = statutoryValidate($('#datavalue' + j).val().trim());
    if (checkLength) {
      displayMessage('');
      var levelstage = $('#level' + j).val();
      var statutorylevel_id = $('#statutorylevelid' + j).val();
      var datavalue = $('#datavalue' + j).val().trim();
      var map_statutory_id = [];
      var map_statutory_names = [];
      var last_statutory_id = 0;
      var last_level = 0;
      for (k = 1; k < j; k++) {
        $('.slist' + k + '.active').each(function (index, el) {
          map_statutory_id.push(parseInt(el.id));
          map_statutory_names.push(el.innerHTML);
          last_statutory_id = el.id;
          last_level = k;
        });
      }
      if (map_statutory_id == 0 && levelstage > 1) {
        displayMessage(message.levelselection_required);
      } else if (datavalue == '') {
        var msg = 'Level-' + levelstage;
        displayMessage(msg + message.shouldnot_empty);
      } else {
        if ($('#statutoryid').val() != '' && editLevel == levelstage) {
          function onSuccessUpdate(data) {
            $('#statutoryid').val('');
            $('.addleft').val('');
            editLevel = '';
            displayMessage(message.record_updated);
            reload(last_statutory_id, last_level, sm_countryid, sm_domainid);
          }
          function onFailureUpdate(error) {
            if (error == 'StatutoryNameAlreadyExists') {
              displayMessage(message.statutoryname_exists);
            } else {
              displayMessage(error);
            }
          }
          if (map_statutory_id.length == 0) {
            map_statutory_id.push(0);
            map_statutory_names.push(datavalue);
          }
          mirror.updateStatutory(parseInt($('#statutoryid').val()), parseInt(statutorylevel_id), datavalue, map_statutory_id, map_statutory_names, function (error, response) {
            if (error == null) {
              onSuccessUpdate(response);
            } else {
              onFailureUpdate(error);
            }
          });
        } else {
          function onSuccess(data) {
            $('#statutoryid').val('');
            $('.addleft').val('');
            editLevel = '';
            displayMessage(message.record_added);
            reload(last_statutory_id, last_level, sm_countryid, sm_domainid);
          }
          function onFailure(error) {
            if (error == 'StatutoryNameAlreadyExists') {
              displayMessage(message.statutoryname_exists);
            } else {
              displayMessage(error);
            }
          }
          if (map_statutory_id.length == 0) {
            map_statutory_id.push(0);
            map_statutory_names.push(datavalue);
          }
          mirror.saveStatutory(sm_domainid, parseInt(statutorylevel_id), datavalue, map_statutory_id, map_statutory_names, function (error, response) {
            if (error == null) {
              onSuccess(response);
            } else {
              onFailure(error);
            }
          });
        }
      }
    }
  }
}
// reload statutory master after save/update
function reload(last_statutory_id, last_level, country, domain) {
  function success(status, data) {
    statutoriesList = data.statutories;
    load(last_statutory_id, last_level, country, domain);
  }
  function failure(data) {
    custom_alert(data);
  }
  mirror.getStatutoryMappingsMaster(success, failure);
}
function filter_statutory(position) {
  var slist_filter = document.getElementsByClassName('slist' + position);
  var eslist_filter = document.getElementsByClassName('eslist-filter' + position);
  var filter = $('#statutoryfilter' + position).val().toLowerCase();
  for (var i = 0; i < slist_filter.length; i++) {
    name = slist_filter[i].innerHTML.trim();
    if (~name.toLowerCase().indexOf(filter)) {
      slist_filter[i].style.display = 'list-item';
      eslist_filter[i].style.display = 'list-item';
    } else {
      slist_filter[i].style.display = 'none';
      eslist_filter[i].style.display = 'none';
    }
  }
}
function editstaturoty(statu_id, statu_name, position) {
  $('#statutoryid').val(statu_id);
  editLevel = position;
  for (var z = 1; z <= 10; z++) {
    $('#datavalue' + z).val('');
  }
  $('#datavalue' + position).val(statu_name.replace(/##/gi, '"'));
}
//load selected statutories in second wizard
function load_statories() {
  disp_statutories = [];
  $('.tbody-statutory-list').find('tr').remove();
  for (var i = 0; i < sm_statutoryids.length; i++) {
    var dispstatutory = '';
    var statutoryList = statutoriesList[sm_countryid][sm_domainid];
    for (var statutory in statutoryList) {
      if (statutoryList[statutory].statutory_id == sm_statutoryids[i]) {
        dispstatutory = statutoryList[statutory].parent_mappings;
        disp_statutories.push(dispstatutory);
      }
    }
    var tableRow = $('#statutory-templates .table-statutory .table-row');
    var clone = tableRow.clone();
    $('.sno', clone).text(i + 1);
    $('.statutory', clone).html(dispstatutory.replace(/>>/gi, ' <img src=\'/knowledge/images/right_arrow.png\'/> '));
    $('.remove', clone).html('<img src=\'/knowledge/images/icon-delete.png\' onclick="temp_removestatutories(\'' + sm_statutoryids[i] + '\')"/>');
    $('.tbody-statutory-list').append(clone);
  }
  make_breadcrumbs2();
  // Reset all level of statutory list after added in temp statutory list
  for (var i = 2; i <= 10; i++) {
    $('#statutorylist' + i).empty();
  }
  $('.slist1').each(function (index, el) {
    $(el).removeClass('active');
  });
}
//add statutories in second wizard
$('#temp_addstatutories').click(function () {
  var last_statutory_id = 0;
  for (k = 1; k <= 10; k++) {
    $('.slist' + k + '.active').each(function (index, el) {
      last_statutory_id = parseInt(el.id);
    });
  }
  if (last_statutory_id == 0) {
    displayMessage(message.nostatutory_selected);
  } else if ($.inArray(last_statutory_id, sm_statutoryids) >= 0) {
    displayMessage(message.statutory_already_added);
  } else {
    if (sm_statutoryids.length > 0) {
      var parentSelection = $('.slist1.active').text();
      if (disp_statutories.length > 0) {
        var parentAct = disp_statutories[0].split('>>');
        if (parentSelection != parentAct[0]) {
          displayMessage(message.invalid_levelone + parentAct[0] + message.selectin_firstlevel);
          return false;
        } else {
          sm_statutoryids.push(parseInt(last_statutory_id));
        }
      }
    } else {
      sm_statutoryids.push(parseInt(last_statutory_id));
    }
  }
  load_statories();
});
//remove statutories from list
function temp_removestatutories(remove_id) {
  remove = sm_statutoryids.indexOf(parseInt(remove_id));
  sm_statutoryids.splice(remove, 1);
  load_statories();
}
function reset_compliance() {
  $('#statutory_provision').val('');
  $('#compliance_task').val('');
  $('#compliance_description').val('');
  $('#compliance_frequency').val('');
  $('#compliance_document').val('');
  $('#upload_file').val('');
  $('#penal_consequences').val('');
  $('#Recurring').hide();
  $('#Occasional').hide();
  $('#One_Time').hide();
  $('#repeats_every').val('');
  $('#repeats_type').val('');
  $('#duration').val('');
  $('#statutory_date').val('');
  $('#statutory_month').val('');
  $('#triggerbefore').val('');
  $('#complianceid').val('');
  uploadFile = null;
  $('#uploaded_fileview').hide();
  $('#uploaded_filename').html('');
  $('.multipleinput').prop('checked', false);
  $('.multipleselectnone').show();
  $('.multipleselect').hide();
  $('#multipleview').hide();
  $('#dayofmonth').prop('checked', true);
  $('.repeatby-view').show();
  $('#counter').html('');
  $('#counter1').html('');
  $('#counter2').html('');
  $('#duration_type').val('');
  $('#summary').html('');
  $('.summary_repeat').html('');
  for (i = 1; i <= 12; i++) {
    $('#multiple_statutory_date' + i).show();
  }
  resetvalues();
}
//load compliances in third wizard
function load_compliance() {
  isAllComplianceActive = false;
  $('.tbody-compliance-list').find('tr').remove();
  complianceid = 0;
  for (var entity in compliances) {
    var display_repeats = 'Nil';
    var edit_compliance_id = compliances[entity].c_id;
    var passStatus = '';
    var isActive = compliances[entity].is_active;
    var display_image = '';
    var complianceFrequency = null;
    var repeatsval = null;
    if (compliances[entity].r_every != null && compliances[entity].r_type_id != null && compliances[entity].r_every != 0 && compliances[entity].r_type_id != 0) {
      for (var rtype in complianceRepeatTypeList) {
        if (complianceRepeatTypeList[rtype].repeat_type_id == compliances[entity].r_type_id) {
          repeatsval = complianceRepeatTypeList[rtype].repeat_type;
        }
      }
      display_repeats = compliances[entity].r_every + ' ' + repeatsval;
    }
    for (var compliancefrequency in complianceFrequencyList) {
      if (complianceFrequencyList[compliancefrequency].frequency_id == compliances[entity].f_id) {
        complianceFrequency = complianceFrequencyList[compliancefrequency].frequency;
      }
    }
    var cDescription = compliances[entity].description;
    var partDescription = cDescription;
    if (cDescription != null && cDescription.length > 50) {
      partDescription = cDescription.substring(0, 49) + '...';
    }
    var tableRow = $('#compliance-templates .table-compliance .table-row');
    var clone = tableRow.clone();
    $('.sno', clone).text(complianceid + 1);
    $('.statutory-provision', clone).text(compliances[entity].s_provision);
    $('.task', clone).text(compliances[entity].c_task);
    $('.description', clone).html('<abbr class="page-load" title="' + cDescription + '">' + partDescription + '</abbr>');
    $('.frequency', clone).text(complianceFrequency);
    $('.repeats', clone).text(display_repeats);
    $('.edit', clone).html('<img src=\'/knowledge/images/icon-edit.png\' onclick="temp_editcompliance(\'' + complianceid + '\')"/>');
    if (edit_compliance_id != null) {
      if (isActive == true) {
        display_image = 'icon-active.png';
        passStatus = false;
        isAllComplianceActive = true;
      } else {
        display_image = 'icon-inactive.png';
        passStatus = true;
      }
      $('.status', clone).html('<img src=\'/knowledge/images/' + display_image + '\' onclick="temp_change_status_compliance(\'' + complianceid + '\',' + passStatus + ')"/>');
    } else {
      isAllComplianceActive = true;
      $('.status', clone).html('<img src=\'/knowledge/images/icon-delete.png\' onclick="temp_removecompliance(\'' + complianceid + '\')"/>');
    }
    $('.tbody-compliance-list').append(clone);
    complianceid = complianceid + 1;
  }
  make_breadcrumbs3();
}
//add compliances in third wizard
$('#temp_addcompliance').click(function () {
  var checkLength = complianceValidate();
  if (checkLength) {
    var comp_id = $('#complianceid').val();
    if ($('#upload_file').val() != '') {
      var fCId = '';
      if (comp_id == '') {
        fCId = complianceid;
      } else {
        fCId = comp_id;
      }
      uploadFile = mirror.uploadFileFormat(f_Size, f_Name, f_Content);
      var file_data = file_lst[0];
      form_data.append('file' + fCId, file_data, f_Name);
      form_data.append('session_token', mirror.getSessionToken());
      isUpload = true;
    }
    /*for (var i = 0; i < file_lst.length; i++) {
      var file_data = file_lst[i];
      console.log(file_data);
      form_data.append("file" + i, file_data, f_Name);
    }*/
    var statutory_provision = $('#statutory_provision').val().trim();
    var compliance_task = $('#compliance_task').val().trim();
    var description = $('#compliance_description').val().trim();
    var compliance_document = null;
    if ($('#compliance_document').val().trim().length > 0)
      compliance_document = $('#compliance_document').val().trim();
    var file_format = null;
    if (uploadFile != null) {
      file_format = [];
      file_format.push(uploadFile);
    }
    var penal_consequences = $('#penal_consequences').val().trim();
    var compliance_frequency = $('#compliance_frequency').val().trim();
    var repeats_type = null;
    var repeats_every = null;
    var duration = null;
    var duration_type = null;
    var statutory_date = null;
    var statutory_day = null;
    var statutory_month = null;
    var trigger_before_days = null;
    var is_active = true;
    statutory_dates = [];
    if (statutory_provision.length == 0) {
      displayMessage(message.statutoryprovision_required);
    } else if (compliance_task.length == 0) {
      displayMessage(message.compliancetask_required);
    } else if (description.length == 0) {
      displayMessage(message.compliancedescription_required);
    } else if (compliance_frequency.length == 0) {
      displayMessage(message.compliancefrequency_required);
    } else if ((compliance_frequency == '2' || compliance_frequency == '3') && $('#repeats_type').val() == '') {
      displayMessage(message.repeatstype_required);
    } else if ((compliance_frequency == '2' || compliance_frequency == '3') && $('#repeats_every').val().trim() == '') {
      displayMessage(message.repeatsevery_required);
    } else if (compliance_frequency == '4' && $('#duration').val().trim() == '') {
      displayMessage(message.duration_required);
    } else if (compliance_frequency == '4' && $('#duration').val().trim() == 0) {
      displayMessage(message.invalid_duration);
    } else if (compliance_frequency == '4' && $('#duration_type').val() == '') {
      displayMessage(message.durationtype_required);
    } else {
      displayMessage('');
      var repeatBy = $('input[name="repeatby"]:checked').val();
      if (compliance_frequency == '1') {
        if ($('#statutory_date').val() != '')
          statutory_day = parseInt($('#statutory_date').val());
        if ($('#statutory_month').val() != '')
          statutory_month = parseInt($('#statutory_month').val());
        if ($('#triggerbefore').val().trim().length > 0) {
          trigger_before_days = parseInt($('#triggerbefore').val());
          if (trigger_before_days > 100) {
            displayMessage(message.triggerbefore_exceed);
            return false;
          }
          if (trigger_before_days == 0) {
            displayMessage(message.triggerbefore_iszero);
            return false;
          }
        }
        if ($('#statutory_date').val() != '' || $('#statutory_month').val() != '' || $('#triggerbefore').val().trim().length > 0) {
          statutory_date = mirror.statutoryDates(statutory_day, statutory_month, trigger_before_days, repeatBy);
          statutory_dates.push(statutory_date);
        }
      } else if (compliance_frequency == '2' || compliance_frequency == '3') {
        repeats_type = parseInt($('#repeats_type').val());
        repeats_every = parseInt($('#repeats_every').val());
        repeats_every_length = $('#repeats_every').val().trim().length;
        var max_triggerbefore = 0;
        if (repeats_type == 1) {
          max_triggerbefore = repeats_every;
        } else if (repeats_type == 2) {
          max_triggerbefore = repeats_every * 30;
        } else {
          max_triggerbefore = repeats_every * 365;
        }
        if (repeats_every == 0) {
          displayMessage(message.invalid_repeatsevery);
          return false;
        } else if (repeats_type == 1 && repeats_every_length > 3) {
          displayMessage(message.days_maximum);
          return false;
        } else if (repeats_type == 2 && repeats_every_length > 2) {
          displayMessage(message.months_maximum);
          return false;
        } else if (repeats_type == 3 && repeats_every_length > 1) {
          displayMessage(message.years_maximum);
          return false;
        } else {
          if (repeats_type == 2 && $('.multipleinput').prop('checked') == true) {
            var s_months = [];
            var rep_every = parseInt($('#repeats_every').val());
            var maxCount = 0;
            if (rep_every == 1) {
              maxCount = 12;
            } else if (rep_every == 2) {
              maxCount = 6;
            } else if (rep_every == 3) {
              maxCount = 4;
            } else if (rep_every == 4) {
              maxCount = 3;
            } else if (rep_every == 12) {
              maxCount = 1;
            } else {
              maxCount = 2;
            }
            for (var i = 1; i <= maxCount; i++) {
              statutory_day = null;
              statutory_month = null;
              trigger_before_days = null;
              if ($('#multiple_statutory_date' + i).val() == '' || $('#multiple_statutory_month' + i).val() == '' || $('#multiple_triggerbefore' + i).val().trim().length == 0) {
                displayMessage(message.statutorydate_triggerdte_mandatory_multipleinputs);
                return false;
              } else {
                statutory_day = parseInt($('#multiple_statutory_date' + i).val());
                statutory_month = parseInt($('#multiple_statutory_month' + i).val());
                trigger_before_days = parseInt($('#multiple_triggerbefore' + i).val());
                if (trigger_before_days > 100) {
                  displayMessage(message.triggerbefore_exceed);
                  return false;
                }
                if (trigger_before_days == 0) {
                  displayMessage(message.triggerbefore_iszero);
                  return false;
                }
                if (trigger_before_days > max_triggerbefore) {
                  displayMessage(message.triggerdays_exceeding_repeatsevery);
                  return false;
                }
                if ($.inArray(statutory_month, s_months) >= 0) {
                  displayMessage(message.invalid_statutory_month);
                  return false;
                }
                statutory_date = mirror.statutoryDates(statutory_day, statutory_month, trigger_before_days, repeatBy);
                statutory_dates.push(statutory_date);
                s_months.push(statutory_month);
              }
            }
          } else {
            if ($('#single_statutory_date').val() != '' || $('#single_statutory_month').val() != '' || $('#single_triggerbefore').val().trim().length > 0) {
              if ($('#single_statutory_date').val() != '')
                statutory_day = parseInt($('#single_statutory_date').val());
              if ($('#single_statutory_month').val() != '')
                statutory_month = parseInt($('#single_statutory_month').val());
              if ($('#single_triggerbefore').val().trim().length > 0)
                trigger_before_days = parseInt($('#single_triggerbefore').val());
              if (trigger_before_days > 100) {
                displayMessage(message.triggerbefore_exceed);
                return false;
              }
              if (trigger_before_days == 0) {
                displayMessage(message.triggerbefore_iszero);
                return false;
              }
              if (trigger_before_days > max_triggerbefore) {
                displayMessage(message.triggerdays_exceeding_repeatsevery);
                return false;
              }
              statutory_date = mirror.statutoryDates(statutory_day, statutory_month, trigger_before_days, repeatBy);
              statutory_dates.push(statutory_date);
            }
          }
        }
      } else {
        duration = parseInt($('#duration').val());
        duration_type = parseInt($('#duration_type').val());
      }
      var check_duplicate_status = true;
      var ccount = 0;
      $.each(compliances, function (index, value) {
        if (value.s_provision == statutory_provision && value.c_task == compliance_task && (comp_id == '' || comp_id != ccount)) {
          if (value.s_provision == statutory_provision) {
            displayMessage(message.statutoryprovision_duplicate);
          }
          if (value.c_task == compliance_task) {
            displayMessage(message.compliancetask_duplicate);
          }
          check_duplicate_status = false;
        }
        ccount = ccount + 1;
      });
      if (check_duplicate_status) {
        if (comp_id == '') {
          compliance = mirror.complianceDetails(statutory_provision, compliance_task, description, compliance_document, file_format, penal_consequences, parseInt(compliance_frequency), statutory_dates, repeats_type, repeats_every, duration_type, duration, is_active, comp_id);
          compliances.push(compliance);
        } else {
          compliances[comp_id].s_provision = statutory_provision;
          compliances[comp_id].c_task = compliance_task;
          compliances[comp_id].description = description;
          compliances[comp_id].doc_name = compliance_document;
          compliances[comp_id].f_f_list = file_format;
          compliances[comp_id].p_consequences = penal_consequences;
          compliances[comp_id].f_id = parseInt(compliance_frequency);
          compliances[comp_id].statu_dates = statutory_dates;
          compliances[comp_id].r_type_id = repeats_type;
          compliances[comp_id].r_every = repeats_every;
          compliances[comp_id].d_type_id = duration_type;
          compliances[comp_id].duration = duration;
          compliances[comp_id].is_active = true;
          compliances[comp_id].download_file_list = null;
        }
        reset_compliance();
        load_compliance();
        $('#statutory_provision').focus();
      }
    }
  }
});
//edit compliances in third wizard
function temp_editcompliance(edit_id) {
  $('#dayofmonth').prop('checked', true);
  $('#single_statutory_date').val('');
  $('#statutory_provision').val(compliances[edit_id].s_provision);
  $('#compliance_task').val(compliances[edit_id].c_task);
  $('#compliance_description').val(compliances[edit_id].description);
  $('#compliance_frequency').val(compliances[edit_id].f_id);
  $('#compliance_document').val(compliances[edit_id].doc_name);
  $('#penal_consequences').val(compliances[edit_id].p_consequences);
  $('#duration_type').val(compliances[edit_id].d_type_id);
  $('#duration').val(compliances[edit_id].duration);
  $('#repeats_type').val(compliances[edit_id].r_type_id);
  $('#repeats_every').val(compliances[edit_id].r_every);
  if (compliances[edit_id].f_f_list != null) {
    uploadFile = compliances[edit_id].f_f_list;
    if (uploadFile != null && uploadFile.length > 0) {
      uploadFile = uploadFile[0];
    }
    var fullname = compliances[edit_id].f_f_list[0].file_name;
    var concatfilename = '';
    if (fullname.indexOf('-') != -1) {
      var fname = fullname.substr(0, fullname.lastIndexOf('-'));
      var fextension = fullname.substr(fullname.indexOf('.') + 1);
      concatfilename = fname + '.' + fextension;
    } else {
      concatfilename = fullname;
    }
    $('#uploaded_fileview').show();
    $('#uploaded_filename').html(concatfilename + '   <img src=\'/knowledge/images/close-icon-black.png\' onclick=\'remove_temp_file(' + edit_id + ')\' />');
  } else {
    $('#uploaded_fileview').hide();
    $('#uploaded_filename').html('');
  }
  var compliance_frequency = compliances[edit_id].f_id;
  statutory_dates = compliances[edit_id].statu_dates;
  if (compliance_frequency == '1') {
    if (statutory_dates.length > 0) {
      $('#statutory_date').val(statutory_dates[0].statutory_date);
      $('#statutory_month').val(statutory_dates[0].statutory_month);
      $('#triggerbefore').val(statutory_dates[0].trigger_before_days);
    }
    $('#Recurring').hide();
    $('#Occasional').hide();
    $('#One_Time').show();
  } else if (compliance_frequency == '2' || compliance_frequency == '3') {
    $('#Recurring').show();
    $('#Occasional').hide();
    $('#One_Time').hide();
    if (compliance_frequency == '2') {
      $('.frequency_type').html('Periodical');
    } else {
      $('.frequency_type').html('Review');
    }
    if (statutory_dates.length > 1) {
      $('.multipleinput').prop('checked', true);
      $('#multipleview').show();
      $('.multipleselectnone').hide();
      $('.multipleselect').show();
      load_stautorydates();
      for (var i = 1; i <= statutory_dates.length; i++) {
        $('#multiple_statutory_date' + i).val(statutory_dates[i - 1].statutory_date);
        $('#multiple_statutory_month' + i).val(statutory_dates[i - 1].statutory_month);
        $('#multiple_triggerbefore' + i).val(statutory_dates[i - 1].trigger_before_days);
      }
      for (var i = statutory_dates + 1; i <= 12; i++) {
        $('#multiple_statutory_date' + i).val('');
        $('#multiple_statutory_month' + i).val('');
        $('#multiple_triggerbefore' + i).val('');
      }
      if (statutory_dates[0].repeat_by == 'enddayofmonth') {
        $('#enddayofmonth').prop('checked', true);
        for (i = 1; i <= 12; i++) {
          $('#multiple_statutory_date' + i).hide();
        }
        $('#single_statutory_date').hide();
      } else {
        $('#dayofmonth').prop('checked', true);
        for (i = 1; i <= 12; i++) {
          $('#multiple_statutory_date' + i).show();
        }
        $('#single_statutory_date').show();
      }
      load_data();
    } else {
      $('.multipleinput').prop('checked', false);
      $('.multipleselectnone').show();
      $('.multipleselect').hide();
      if (statutory_dates.length > 0) {
        $('#single_statutory_date').val(statutory_dates[0].statutory_date);
        $('#single_statutory_month').val(statutory_dates[0].statutory_month);
        $('#single_triggerbefore').val(statutory_dates[0].trigger_before_days);
        if (statutory_dates[0].repeat_by == 'enddayofmonth') {
          $('#enddayofmonth').prop('checked', true);
          $('#single_statutory_date').hide();
        } else {
          $('#dayofmonth').prop('checked', true);
          $('#single_statutory_date').show();
        }
      }
      load_data();
      if ($('input[name="repeatby"]:checked').val() == 'enddayofmonth') {
        $('#single_statutory_date').hide();
        $('#sdate').hide();
      } else {
        $('#single_statutory_date').show();
      }
      if ($('#repeats_type').val() == 1) {
        $('#single_statutory_date').hide();
      }
      if ($('#repeats_type').val() == 3) {
        $('#sdate').show();
      }
    }
  } else {
    $('#Recurring').hide();
    $('#Occasional').show();
    $('#One_Time').hide();
  }
  $('#complianceid').val(edit_id);
  load_summary();
}
//remove compliance in third wizard
function temp_removecompliance(remove_id) {
  compliances.splice(parseInt(remove_id), 1);
  load_compliance();
}
//activate/deactivate compliance in third wizard
function temp_change_status_compliance(edit_id, passStatus) {
  compliances[edit_id].is_active = passStatus;
  load_compliance();
}
//create breadcrumb & display
function make_breadcrumbs2() {
  var arrowimage = ' <img src=\'/knowledge/images/right_arrow.png\'/> ';
  var statutories_name = '';
  for (var i = 0; i < disp_statutories.length; i++) {
    statutories_name = statutories_name + disp_statutories[i].replace(/>>/gi, ' <img src=\'/knowledge/images/right_arrow.png\'/> ') + ',';
  }
  statutories_name = statutories_name.replace(/,\s*$/, '');
  $('.breadcrumbs_2').html(statutories_name);
}
function make_breadcrumbs3() {
  var compliance_name = '';
  for (var entity in compliances) {
    var doc_name = compliances[entity].doc_name;
    var statu_provision = compliances[entity].s_provision;
    var breadcrumbs_text = '';
    if (doc_name != null) {
      breadcrumbs_text = doc_name + ' - ' + statu_provision;
    } else {
      breadcrumbs_text = statu_provision;
    }
    compliance_name = compliance_name + breadcrumbs_text + ',';
  }
  compliance_name = compliance_name.replace(/,\s*$/, '');
  $('.breadcrumbs_3').html(compliance_name);
}
//load geography level date in last wizard
function loadGeographyLevels(sm_countryid) {
  $('.tbody-geography-level').find('div').remove();
  if (sm_countryid in geographyLevelsList) {
    var geographyLevelList = geographyLevelsList[sm_countryid];
    var levelposition;
    for (var j in geographyLevelList) {
      levelposition = geographyLevelList[j].l_position;
      var tableRow = $('#geography-level-templates');
      var clone = tableRow.clone();
      $('.title', clone).text(geographyLevelList[j].l_name);
      $('.levelvalue', clone).html('<input type="text" class="filter-text-box" id="filter_geography' + levelposition + '" onkeyup="filter_geography(' + levelposition + ')"> <ul id="ulist' + levelposition + '"></ul><input type="hidden" id="glmid' + levelposition + '" value="' + geographyLevelList[j].l_id + '"/><input type="hidden" id="level' + levelposition + '" value="' + levelposition + '" />');
      $('.tbody-geography-level').append(clone);
    }
    var setlevelstage = 1;
    $('#datavalue' + setlevelstage).val('');
    $('#ulist' + setlevelstage).empty();
    var firstlevelid = $('#glmid' + setlevelstage).val();
    var idval = '';
    var clsval = '.list' + setlevelstage;
    var clsval1 = 'list' + setlevelstage;
    var str = '';
    var geographyList = geographiesList[sm_countryid];
    for (var i in geographyList) {
      if (geographyList[i].level_id == firstlevelid && geographyList[i].is_active == true) {
        str = '<li id="select' + setlevelstage + '" class="' + clsval1 + '" onclick="activate_geography_all(this,' + sm_countryid + ',' + setlevelstage + ')" > Select All</li>';
      }
    }
    for (var i in geographyList) {
      var setgeographyid = geographyList[i].geography_id;
      var setparentid = geographyList[i].parent_id;
      var combineid = setgeographyid + '-' + setparentid;
      if (geographyList[i].level_id == firstlevelid && geographyList[i].is_active == true) {
        str += '<li id="' + combineid + '" value="' + setparentid + '" class="' + clsval1 + '" onclick="activate_geography(this,' + sm_countryid + ',' + setlevelstage + ',\'' + combineid + '\')" >' + geographyList[i].geography_name + '</li>';
      }
    }
    $('#ulist' + setlevelstage).append(str);
  }
}
//check & uncheck list data
function activate_geography(element, country, level, combineid) {
  var chkstatus = $(element).attr('class');
  var displaytext = $(element).text();
  if (chkstatus == 'list' + level + ' active') {
    $(element).removeClass('active');
    load_geography(level, country, combineid, 'remove', displaytext);
  } else {
    $(element).addClass('active');
    load_geography(level, country, combineid, 'add', displaytext);
  }
}
//select all geography level data
function activate_geography_all(element, country, level) {
  var chkstatus = $(element).attr('class');
  if (chkstatus == 'list' + level + ' active') {
    $('.list' + level + '.active').each(function (index, el) {
      $(el).removeClass('active');
    });
  } else {
    $('.list' + level).each(function (index, el) {
      $(el).addClass('active');
    });
  }
  load_geography_all(level, country);
}
//load geographymapping sub level data dynamically
function load_geography(level, country, combineids, status, displaytext) {
  var geographyids = [];
  displayMessage('');
  var split_id = combineids.split('-');
  var previous_primary_id = split_id[1];
  geographyids.push([
    parseInt(split_id[0]),
    displaytext
  ]);
  var levelstages = parseInt(level) + 1;
  for (var k = levelstages; k <= 10; k++) {
    var setlevelstage = k;
    $('#select' + setlevelstage).remove();
    if ($('#geographyid').val() == '') {
      $('#datavalue' + setlevelstage).val('');
    }
    var splittext = '';
    var idval = '';
    var clsval = '.list' + setlevelstage;
    var clsval1 = 'list' + setlevelstage;
    var str = '';
    var sel_all = '<li id="select' + setlevelstage + '" class="' + clsval1 + '" onclick="activate_geography_all(this,' + sm_countryid + ',' + setlevelstage + ')" > Select All</li>';
    var levelid = $('#glmid' + setlevelstage).val();
    var geographyList = geographiesList[country];
    $('#ulist' + setlevelstage).children('li').each(function () {
      if ($(this).val() == previous_primary_id) {
        $(this).remove();
        $('.split' + previous_primary_id + setlevelstage).remove();
      }
    });
    for (var j = 0; j < geographyids.length; j++) {
      splittext = '';
      for (var i in geographyList) {
        var setgeographyid = geographyList[i].geography_id;
        var setparentid = geographyList[i].parent_id;
        var combineid = setgeographyid + '-' + setparentid;
        if (geographyList[i].parent_id == geographyids[j][0] && geographyList[i].level_id == levelid && geographyList[i].is_active == true) {
          if (status == 'add') {
            if (splittext != '') {
              str += '<li id="' + combineid + '" value="' + setparentid + '" class="' + clsval1 + '" onclick="activate_geography(this,' + country + ',' + setlevelstage + ',\'' + combineid + '\')" > ' + geographyList[i].geography_name + '</li>';
            } else {
              splittext = '<h3 class="split' + setparentid + setlevelstage + '" style="background-color:gray;padding:2px;font-size:13px;color:white;">' + geographyids[j][1] + '</h3>';
              str += splittext + '<li id="' + combineid + '" value="' + setparentid + '" class="' + clsval1 + '" onclick="activate_geography(this,' + country + ',' + setlevelstage + ',\'' + combineid + '\')" >' + geographyList[i].geography_name + '</li>';
            }
          } else {
            if ($('#' + combineid).attr('class') == 'list' + setlevelstage + ' active') {
              displayMessage(message.removechild_first);
              $('#' + combineids).addClass('active');
            } else {
              $('#' + combineid).remove();
              $('.split' + setparentid + setlevelstage).remove();
            }
          }
        }
      }
    }
    $('#ulist' + setlevelstage).append(str);
    if ($('#ulist' + setlevelstage + ' li').length > 0) {
      $('#ulist' + setlevelstage).prepend(sel_all);
    }
  }
}
//load geographymapping sub level data dynamically
function load_geography_all(level, country) {
  var geographyids = [];
  $('.list' + level + '.active').each(function (index, el) {
    var split_id = el.id.split('-');
    geographyids.push([
      parseInt(split_id[0]),
      el.innerHTML
    ]);
  });
  var levelstages = parseInt(level) + 1;
  for (var k = levelstages; k <= 10; k++) {
    var setlevelstage = k;
    if ($('#geographyid').val() == '') {
      $('#datavalue' + setlevelstage).val('');
    }
    $('#ulist' + setlevelstage).empty();
    var splittext = '';
    var idval = '';
    var clsval = '.list' + setlevelstage;
    var clsval1 = 'list' + setlevelstage;
    var str = '';
    var sel_all = '<li id="selectall' + setlevelstage + '" class="' + clsval1 + '" onclick="activate_geography_all(this,' + sm_countryid + ',' + setlevelstage + ')" > Select All</li>';
    var levelid = $('#glmid' + setlevelstage).val();
    var geographyList = geographiesList[country];
    //working order is even for multiple selection
    for (var j = 0; j < geographyids.length; j++) {
      splittext = '';
      for (var i in geographyList) {
        var setgeographyid = geographyList[i].geography_id;
        var setparentid = geographyList[i].parent_id;
        var combineid = setgeographyid + '-' + setparentid;
        if (geographyList[i].parent_id == geographyids[j][0] && geographyList[i].level_id == levelid && geographyList[i].is_active == true) {
          str += sel_all;
          if (splittext != '') {
            str += '<li id="' + combineid + '" class="' + clsval1 + '" onclick="activate_geography(this,' + country + ',' + setlevelstage + ',\'' + combineid + '\')" > ' + geographyList[i].geography_name + '</li>';
          } else {
            splittext = '<h3 style="background-color:gray;padding:2px;font-size:13px;color:white;">' + geographyids[j][1] + '</h3>';
            str += splittext + '<li id="' + combineid + '" class="' + clsval1 + '" onclick="activate_geography(this,' + country + ',' + setlevelstage + ',\'' + combineid + '\')" >' + geographyList[i].geography_name + '</li>';
          }
          sel_all = '';
        }
      }
    }
    $('#ulist' + setlevelstage).append(str);
  }
}
//save selected applicable location in variable
function getGeographyResult() {
  sm_geographyids = [];
  for (k = 1; k <= 10; k++) {
    $('.list' + k + '.active').each(function (index, el) {
      var split_id = el.id.split('-');
      if ($.isNumeric(split_id[0])) {
        var g_id = parseInt(split_id[0]);
        var p_id = parseInt(split_id[1]);
        sm_geographyids.push(g_id);
        if ($.inArray(p_id, sm_geographyids) >= 0) {
          var remove_geography = sm_geographyids.indexOf(p_id);
          sm_geographyids.splice(remove_geography, 1);
        }
      }
    });
  }
}
//filter location
function filter_geography(position) {
  var glist_filter = document.getElementsByClassName('list' + position);
  var filter = $('#filter_geography' + position).val().toLowerCase();
  for (var i = 0; i < glist_filter.length; i++) {
    name = glist_filter[i].innerHTML.trim();
    if (~name.toLowerCase().indexOf(filter)) {
      glist_filter[i].style.display = 'list-item';
    } else {
      glist_filter[i].style.display = 'none';
    }
  }
}


//save/update statutory mapping
function savestatutorymapping() {
  displayLoader();
  function onSuccess(data) {
    getStatutoryMappings();
    $('.listfilter').val('');
    $('#statutorymapping-add').hide();
    $('ul.setup-panel li:eq(0)').addClass('active');
    $('ul.setup-panel li:eq(1)').addClass('disabled');
    $('ul.setup-panel li:eq(2)').addClass('disabled');
    $('ul.setup-panel li:eq(3)').addClass('disabled');
    $('ul.setup-panel li a[href="#step-1"]').trigger('click');
    uploadFile = null;
    $('#uploaded_fileview').hide();
    $('#uploaded_filename').html('');
    $('#statutorymapping-view').show();
    hideLoader();
  }
  function onFailure(error, response) {
    if (error == 'ComplianceNameAlreadyExists') {
      var duplicateComplianceList = response.compliance_name;
      displayMessage(message.compliancename_exists + duplicateComplianceList);
    } else {
      displayMessage(error);
    }
    $('#activate-step-finish').prop('disabled', false);
    $('#activate-step-finish').text('Submit');
    $('#activate-step-finish').addClass('btn-right');
    $('#activate-step-finish').removeClass('btn-right-submiting');
    hideLoader();
  }
  var sm_id = null;
  if ($('#edit_sm_id').val().length > 0) {
    sm_id = parseInt($('#edit_sm_id').val());
  }

  /*for (var [key, value] of form_data.entries()) {
    isUpload = true;
    //console.log(key, value);
  }*/
  statutorymappingData = mirror.statutoryMapping(sm_countryid, sm_domainid, sm_industryids, sm_statutorynatureid, sm_statutoryids, compliances, sm_geographyids, disp_statutories, sm_id);
  
  if (sm_id == null) {
    
    mirror.saveStatutoryMapping(statutorymappingData, function (error, response) {
      if (error == null) {
        if(isUpload){
          $('.upload-progress-count').html("");
          $('.upload-progress-count').show();
          mirror.uploadFormatFile(form_data, function result_data(status, data) {
            if(status == 'FileUploadSuccess'){
              form_data = new FormData();
              $('.upload-progress-count').hide();
              onSuccess(response);
            }else{
              displayMessage(status);
              hideLoader();
              $('.upload-progress-count').hide();
              $('.upload-progress-count').html("");
              $('#activate-step-finish').prop('disabled', false);
              $('#activate-step-finish').text('Submit');
              $('#activate-step-finish').addClass('btn-right');
              $('#activate-step-finish').removeClass('btn-right-submiting');
            }
          });
        }else{
          onSuccess(response);
        }
      } else {
        onFailure(error, response);
      }
    });
  } else {

    mirror.updateStatutoryMapping(statutorymappingData, function (error, response) {
      if (error == null) {
        if(isUpload){
          $('.upload-progress-count').html("");
          $('.upload-progress-count').show();
          mirror.uploadFormatFile(form_data, function result_data(status, data) {

            if(status == 'FileUploadSuccess'){
              form_data = new FormData();
              $('.upload-progress-count').hide();
              onSuccess(response);
            }else{
              displayMessage(status);
              hideLoader();
              $('.upload-progress-count').hide();
              $('.upload-progress-count').html("");
              $('#activate-step-finish').prop('disabled', false);
              $('#activate-step-finish').text('Submit');
              $('#activate-step-finish').addClass('btn-right');
              $('#activate-step-finish').removeClass('btn-right-submiting');
                        }
          });
        }else{
          onSuccess(response);
        }
      } else {
        onFailure(error, response);
      }
    });
  }
}
//first wizard validation
function validate_firsttab() {
  if (sm_countryid == '') {
    displayMessage(message.country_required);
  } else if (sm_domainid == '') {
    displayMessage(message.domain_required);
  } else if (sm_industryids.length == 0) {
    displayMessage(message.industry_required);
  } else if (sm_statutorynatureid == '') {
    displayMessage(message.statutorynature_required);
  } else {
    displayMessage('');
    return true;
  }
}
//second wizard validation
function validate_secondtab() {
  if (sm_statutoryids.length == 0) {
    displayMessage(message.statutory_selection_required);
  } else {
    displayMessage('');
    return true;
  }
}
//third wizard validation
function validate_thirdtab() {
  if (compliances.length == 0) {
    displayMessage(message.compliance_selection_required);
  } else if (isAllComplianceActive == false) {
    displayMessage(message.active_compliance_required);
  } else {
    displayMessage('');
    return true;
  }
}
//fourth wizard validation
function validate_fourthtab() {
  if (sm_geographyids.length == 0) {
    displayMessage(message.location_selection_required);
  } else {
    displayMessage('');
    return true;
  }
}
function load_edit_selectdomain_master(sm_countryid, sm_domainid, sm_industryids, sm_statutorynatureid) {
  //load country details
  var clsval = '.countrylist';
  var clsval1 = 'countrylist';
  var str = '';
  $('#country').empty();
  for (var country in countriesList) {
    var countryid = countriesList[country].country_id;
    var dispcountryname = countriesList[country].country_name;
    if (countriesList[country].is_active == true) {
      if (sm_countryid == countryid) {
        str += '<li id="' + countryid + '" class="' + clsval1 + ' active"><span class="filter1_name">' + dispcountryname + '</span></li>';
      } else {
        str += '<li id="' + countryid + '" class="' + clsval1 + '"><span class="filter1_name">' + dispcountryname + '</span></li>';
      }
    }
  }
  $('#country').append(str);
  //load domain details
  var clsval = '.domainlist';
  var clsval1 = 'domainlist';
  var str = '';
  $('#domain').empty();
  for (var domain in domainsList) {
    var domainid = domainsList[domain].domain_id;
    var dispdomainname = domainsList[domain].domain_name;
    if (domainsList[domain].is_active == true) {
      if (sm_domainid == domainid) {
        str += '<li id="' + domainid + '" class="' + clsval1 + ' active" ><span class="filter2_name">' + dispdomainname + '</span></li>';
      } else {
        str += '<li id="' + domainid + '" class="' + clsval1 + '" ><span class="filter2_name">' + dispdomainname + '</span></li>';
      }
    }
  }
  $('#domain').append(str);
  //load industry details
  var clsval = '.industrylist';
  var clsval1 = 'industrylist';
  var str = '';
  $('#industry').empty();
  for (var industry in industriesList) {
    var industryid = industriesList[industry].industry_id;
    var dispindustryname = industriesList[industry].industry_name;
    if (industriesList[industry].is_active == true) {
      if ($.inArray(industryid, sm_industryids) >= 0) {
        str += '<li id="' + industryid + '" class="' + clsval1 + ' active" onclick="multiactivate(this,' + '\'' + clsval + '\')" ><span class="filter3_name">' + dispindustryname + '</span></li>';
      } else {
        str += '<li id="' + industryid + '" class="' + clsval1 + '" onclick="multiactivate(this,' + '\'' + clsval + '\')" ><span class="filter3_name">' + dispindustryname + '</span></li>';
      }
    }
  }
  $('#industry').append(str);
  //load statutorynature details
  var clsval = '.statutorynaturelist';
  var clsval1 = 'statutorynaturelist';
  var str = '';
  $('#statutorynature').empty();
  for (var statutorynature in statutoryNaturesList) {
    var statutorynatureid = statutoryNaturesList[statutorynature].statutory_nature_id;
    var dispstatutoryname = statutoryNaturesList[statutorynature].statutory_nature_name;
    if (statutoryNaturesList[statutorynature].is_active == true) {
      if (statutorynatureid == sm_statutorynatureid) {
        str += '<li id="' + statutorynatureid + '" class="' + clsval1 + ' active" onclick="activate(this,' + '\'' + clsval + '\')" ><span class="filter4_name">' + dispstatutoryname + '</span></li>';
      } else {
        str += '<li id="' + statutorynatureid + '" class="' + clsval1 + '" onclick="activate(this,' + '\'' + clsval + '\')" ><span class="filter4_name">' + dispstatutoryname + '</span></li>';
      }
    }
  }
  $('#statutorynature').append(str);
  if (sm_countryid != '' && sm_domainid != '') {
    loadStatutoryLevels(sm_countryid, sm_domainid);
  }
  if (sm_countryid != '') {
    loadGeographyLevels(sm_countryid);
  }
  make_breadcrumbs();
  //load compliance frequency selectbox
  $('#compliance_frequency').empty();
  $('#compliance_frequency').append('<option value=""> Select </option>');
  for (var compliancefrequency in complianceFrequencyList) {
    var option = $('<option></option>');
    option.val(complianceFrequencyList[compliancefrequency].frequency_id);
    option.text(complianceFrequencyList[compliancefrequency].frequency);
    $('#compliance_frequency').append(option);
  }
  //load compliance duration type selectbox
  $('#duration_type').empty();
  $('#duration_type').append('<option value=""> Select </option>');
  for (var compliancedurationtype in complianceDurationTypeList) {
    var option = $('<option></option>');
    option.val(complianceDurationTypeList[compliancedurationtype].duration_type_id);
    option.text(complianceDurationTypeList[compliancedurationtype].duration_type);
    $('#duration_type').append(option);
  }
  //load compliance repeat type selectbox
  $('#repeats_type').empty();
  $('#repeats_type').append('<option value=""> Select </option>');
  for (var compliancerepeattype in complianceRepeatTypeList) {
    var option = $('<option></option>');
    option.val(complianceRepeatTypeList[compliancerepeattype].repeat_type_id);
    option.text(complianceRepeatTypeList[compliancerepeattype].repeat_type);
    $('#repeats_type').append(option);
  }
}
//edit geographymapping data dynamically
function edit_geography(country, geographyids_edit) {
  var geographyids = geographyids_edit;
  var temp_parent = [];
  for (var i = 0; i < geographyids.length; i++) {
    var geographyList = geographiesList[country];
    for (glist in geographyList) {
      if (geographyids[i] == geographyList[glist].geography_id) {
        var parentids = geographyList[glist].parent_ids;
        var level = geographyList[glist].level_position;
      }
    }
    for (var j = 0; j < parentids.length; j++) {
      var geo_id = parentids[j];
      ;
      var parent_id = 0;
      if (j != 0) {
        parent_id = parentids[j - 1];
      }
      for (glist in geographyList) {
        if (geo_id == geographyList[glist].geography_id) {
          var level_id = geographyList[glist].level_id;
          var displaytext = geographyList[glist].geography_name;
        }
      }
      var combineid = geo_id + '-' + parent_id;
      var displaytext = displaytext;
      var geographyLevelList = geographyLevelsList[country];
      for (glevel in geographyLevelList) {
        if (level_id == geographyLevelList[glevel].l_id) {
          var levelposition = geographyLevelList[glevel].l_position;
        }
      }
      $('#' + combineid).addClass('active');
      if ($.inArray(geo_id, temp_parent) == -1) {
        temp_parent.push(geo_id);
        load_geography(levelposition, country, combineid, 'add', displaytext);
      }
    }
    var finalcombineid = geographyids[i] + '-' + geo_id;
    $('#' + finalcombineid).addClass('active');
  }
}
//edit statutory mapping
function displayEdit(sm_Id) {
  isUpload = false;
  displayMessage('');
  $('#statutorymapping-view').hide();
  $('#statutorymapping-add').show();
  $('#edit_sm_id').val(sm_Id);
  sm_countryid = statutoryMappingsList[sm_Id].country_id;
  sm_countryval = statutoryMappingsList[sm_Id].country_name;
  sm_domainid = statutoryMappingsList[sm_Id].domain_id;
  sm_domainval = statutoryMappingsList[sm_Id].domain_name;
  sm_industryids = statutoryMappingsList[sm_Id].industry_ids;
  sm_industryvals = statutoryMappingsList[sm_Id].industry_names.split(',');
  sm_statutorynatureid = statutoryMappingsList[sm_Id].statutory_nature_id;
  sm_statutorynatureval = statutoryMappingsList[sm_Id].statutory_nature_name;
  sm_statutoryids = statutoryMappingsList[sm_Id].statutory_ids;
  compliances = statutoryMappingsList[sm_Id].compliances;
  sm_geographyids = statutoryMappingsList[sm_Id].geography_ids;
  load_edit_selectdomain_master(sm_countryid, sm_domainid, sm_industryids, sm_statutorynatureid);
  load_statories();
  reset_compliance();
  load_compliance();
  edit_geography(sm_countryid, sm_geographyids);
}
//load statutories date according to repeats every selection
function load_stautorydates() {
  var rep_every = parseInt($('#repeats_every').val());
  var modResult = 12 % rep_every;
  if (modResult == 0 && rep_every < 12) {
    if (rep_every == 1) {
      $('.input-row1').show();
      $('.input-row2').show();
      $('.input-row3').show();
      $('.input-row4').show();
      $('.input-row5').show();
      $('.input-row6').show();
      $('.input-row7').show();
      $('.input-row8').show();
      $('.input-row9').show();
      $('.input-row10').show();
      $('.input-row11').show();
      $('.input-row12').show();
    } else if (rep_every == 2) {
      $('.input-row1').show();
      $('.input-row2').show();
      $('.input-row3').show();
      $('.input-row4').show();
      $('.input-row5').show();
      $('.input-row6').show();
      for (i = 7; i <= 12; i++) {
        $('.input-row' + i).hide();
        $('#multiple_statutory_date' + i).val('');
        $('#multiple_statutory_month' + i).val('');
        $('#multiple_triggerbefore' + i).val('');
      }
    } else if (rep_every == 3) {
      $('.input-row1').show();
      $('.input-row2').show();
      $('.input-row3').show();
      $('.input-row4').show();
      for (i = 5; i <= 12; i++) {
        $('.input-row' + i).hide();
        $('#multiple_statutory_date' + i).val('');
        $('#multiple_statutory_month' + i).val('');
        $('#multiple_triggerbefore' + i).val('');
      }
    } else if (rep_every == 4) {
      $('.input-row1').show();
      $('.input-row2').show();
      $('.input-row3').show();
      for (i = 4; i <= 12; i++) {
        $('.input-row' + i).hide();
        $('#multiple_statutory_date' + i).val('');
        $('#multiple_statutory_month' + i).val('');
        $('#multiple_triggerbefore' + i).val('');
      }
    } else if (rep_every == 12) {
      $('.input-row1').show();
      for (i = 2; i <= 12; i++) {
        $('.input-row' + i).hide();
        $('#multiple_statutory_date' + i).val('');
        $('#multiple_statutory_month' + i).val('');
        $('#multiple_triggerbefore' + i).val('');
      }
    } else {
      $('.input-row1').show();
      $('.input-row2').show();
      for (i = 3; i <= 12; i++) {
        $('.input-row' + i).hide();
        $('#multiple_statutory_date' + i).val('');
        $('#multiple_statutory_month' + i).val('');
        $('#multiple_triggerbefore' + i).val('');
      }
    }
  } else {
    $('#single_statutory_date').show();
    $('#single_statutory_month').hide();
    $('.multipleselect').hide();
    $('.multipleselectnone').show();
    $('#sdate').show();
    $('.repeatby-view').show();
    $('#multipleview').hide();
    $('.multipleinput').prop('checked', false);
  }
  if ($('input[name="repeatby"]:checked').val() == 'enddayofmonth') {
    for (i = 1; i <= 12; i++) {
      $('#multiple_statutory_date' + i).hide();
    }
    $('#single_statutory_date').hide();
    $('#sdate').hide();
  }
}
function load_summary() {
  var durationVal = $('#duration').val();
  var durationType = $('#duration_type option:selected').text().trim();
  var summaryVal = '';
  if (durationVal != '' && durationType != 'Select') {
    summaryVal = durationVal + ' ' + durationType;
  }
  $('#summary').html('To Complete within ' + summaryVal);
  var repeatVal = $('#repeats_every').val();
  var repeatType = $('#repeats_type option:selected').text().trim();
  var summaryVal1 = '';
  if (repeatVal != '' && repeatType != 'Select') {
    summaryVal1 = repeatVal + ' ' + repeatType;
  }
  $('.summary_repeat').html('Every ' + summaryVal1);
}
//display summary
$(function () {
  $('#compliance_description').keyup(function (e) {
    var maxLength = 500;
    var textlength = this.value.length;
    if (textlength >= maxLength) {
      $('#counter').html('You cannot write more then ' + maxLength + ' characters!');
      this.value = this.value.substring(0, maxLength);
      e.preventDefault();
    } else {
      $('#counter').html(maxLength - textlength + ' characters left.');
    }
  });
  $('#statutory_provision').keyup(function (e) {
    var maxLength = 500;
    var textlength = this.value.length;
    if (textlength >= maxLength) {
      $('#counter1').html('You cannot write more then ' + maxLength + ' characters!');
      this.value = this.value.substring(0, maxLength);
      e.preventDefault();
    } else {
      $('#counter1').html(maxLength - textlength + ' characters left.');
    }
  });
  $('#penal_consequences').keyup(function (e) {
    var maxLength = 500;
    var textlength = this.value.length;
    if (textlength >= maxLength) {
      $('#counter2').html('You cannot write more then ' + maxLength + ' characters!');
      this.value = this.value.substring(0, maxLength);
      e.preventDefault();
    } else {
      $('#counter2').html(maxLength - textlength + ' characters left.');
    }
  });
  $('#duration').keyup(function () {
    load_summary();
  });
  $('#duration_type').change(function () {
    load_summary();
  });
  $('#repeats_every').change(function () {
    load_summary();
  });
  $('#repeats_type').change(function () {
    load_summary();
  });
});
//start -filter process in select domain tab
$('#filter_country').keyup(function () {
  var filter = $('#filter_country').val().toLowerCase();
  var lis = document.getElementsByClassName('countrylist');
  for (var i = 0; i < lis.length; i++) {
    var name = lis[i].getElementsByClassName('filter1_name')[0].innerHTML;
    if (~name.toLowerCase().indexOf(filter))
      lis[i].style.display = 'list-item';
    else
      lis[i].style.display = 'none';
  }
});
$('#filter_domain').keyup(function () {
  var filter = $('#filter_domain').val().toLowerCase();
  var lis = document.getElementsByClassName('domainlist');
  for (var i = 0; i < lis.length; i++) {
    var name = lis[i].getElementsByClassName('filter2_name')[0].innerHTML;
    if (~name.toLowerCase().indexOf(filter))
      lis[i].style.display = 'list-item';
    else
      lis[i].style.display = 'none';
  }
});
$('#filter_industry').keyup(function () {
  var filter = $('#filter_industry').val().toLowerCase();
  var lis = document.getElementsByClassName('industrylist');
  for (var i = 0; i < lis.length; i++) {
    var name = lis[i].getElementsByClassName('filter3_name')[0].innerHTML;
    if (~name.toLowerCase().indexOf(filter))
      lis[i].style.display = 'list-item';
    else
      lis[i].style.display = 'none';
  }
});
$('#filter_statutorynature').keyup(function () {
  var filter = $('#filter_statutorynature').val().toLowerCase();
  var lis = document.getElementsByClassName('statutorynaturelist');
  for (var i = 0; i < lis.length; i++) {
    var name = lis[i].getElementsByClassName('filter4_name')[0].innerHTML;
    if (~name.toLowerCase().indexOf(filter))
      lis[i].style.display = 'list-item';
    else
      lis[i].style.display = 'none';
  }
});
//create wizard
var navListItems = $('ul.setup-panel li a'), allWells = $('.setup-content');
allWells.hide();
navListItems.click(function (e) {
  e.preventDefault();
  var $target = $($(this).attr('href')), $item = $(this).closest('li');
  if (!$item.hasClass('disabled')) {
    navListItems.closest('li').removeClass('active');
    $item.addClass('active');
    allWells.hide();
    $target.show();
  }
});
$('ul.setup-panel li.active a').trigger('click');
$('#activate-step-2').on('click', function (e) {
  if (validate_firsttab()) {
    $('ul.setup-panel li:eq(1)').removeClass('disabled');
    $('ul.setup-panel li a[href="#step-2"]').trigger('click');
  }
});
$('#activate-step-3').on('click', function (e) {
  if (validate_secondtab()) {
    $('ul.setup-panel li:eq(2)').removeClass('disabled');
    $('ul.setup-panel li a[href="#step-3"]').trigger('click');
    $('#statutory_provision').focus();
  }
});
$('#activate-step-4').on('click', function (e) {
  if (validate_thirdtab()) {
    $('ul.setup-panel li:eq(3)').removeClass('disabled');
    $('ul.setup-panel li a[href="#step-4"]').trigger('click');
  }
});
$('#backward-step-1').on('click', function (e) {
  $('ul.setup-panel li:eq(1)').removeClass('disabled');
  $('ul.setup-panel li a[href="#step-1"]').trigger('click');
});
$('#backward-step-2').on('click', function (e) {
  $('ul.setup-panel li:eq(2)').removeClass('disabled');
  $('ul.setup-panel li a[href="#step-2"]').trigger('click');
});
$('#backward-step-3').on('click', function (e) {
  $('ul.setup-panel li:eq(3)').removeClass('disabled');
  $('ul.setup-panel li a[href="#step-3"]').trigger('click');
  $('#statutory_provision').focus();
});
$('#activate-step-finish').on('click', function (e) {
  getGeographyResult();
  if (validate_fourthtab()) {
    $('#activate-step-finish').prop('disabled', true);
    $('#activate-step-finish').removeClass('btn-right');
    $('#activate-step-finish').addClass('btn-right-submiting');
    $('#activate-step-finish').text('Submitting...');
    savestatutorymapping();
  }
});
$('#single_statutory_month').change(function () {
  var selectedMonth = $('#single_statutory_month').val();
  var maxDate = load_date(selectedMonth);
  $('#single_statutory_date').empty();
  var defaultoption = $('<option></option>');
  defaultoption.val('');
  defaultoption.text('');
  $('#single_statutory_date').append(defaultoption);
  for (var i = 1; i <= maxDate; i++) {
    var option = $('<option></option>');
    option.val(i);
    option.text(i);
    $('#single_statutory_date').append(option);
  }
  if ($('input[name="repeatby"]:checked').val() == 'enddayofmonth') {
    var selectedMonth = $('#single_statutory_month').val();
    var monthDate = load_date(selectedMonth);
    $('#single_statutory_date').val(monthDate);
  }
});
$('#statutory_month').change(function () {
  var selectedMonth = $('#statutory_month').val();
  var maxDate = load_date(selectedMonth);
  $('#statutory_date').empty();
  var defaultoption = $('<option></option>');
  defaultoption.val('');
  defaultoption.text('');
  $('#statutory_date').append(defaultoption);
  for (var i = 1; i <= maxDate; i++) {
    var option = $('<option></option>');
    option.val(i);
    option.text(i);
    $('#statutory_date').append(option);
  }
  if ($('input[name="repeatby"]:checked').val() == 'enddayofmonth') {
    var selectedMonth = $('#statutory_month').val();
    var monthDate = load_date(selectedMonth);
    $('#statutory_date').val(monthDate);
  }
});
$('.multipleinput').change(function () {
  load_data();
  resetvalues();
});
$('#repeats_type').change(function () {
  load_data();
  resetvalues();
});
$('#repeats_every').change(function () {
  load_data();  //resetvalues();
});
$('.repeatlabelday').click(function () {
  //resetvalues()
  for (i = 1; i <= 12; i++) {
    $('#multiple_statutory_date' + i).show();
    $('#multiple_statutory_date' + i).val('');  //load date based on month
                                                /*$("#multiple_statutory_date"+i).empty();
    var defaultoption = $("<option></option>");
    defaultoption.val("");
    defaultoption.text("");
    $("#multiple_statutory_date"+i).append(defaultoption);

    var mMonth = $('#multiple_statutory_month'+i).val();
    var maxDate = 31;
    if(mMonth != '' || mMonth != undefined){
      maxDate = load_date(mMonth);
    }
    for (var j=1; j<=maxDate; j++) {
        var option = $("<option></option>");
        option.val(j);
        option.text(j)
        $("#multiple_statutory_date"+i).append(option);
    }*/
  }
  $('#single_statutory_date').val('');
  $('#statutory_date').val('');
  $('#single_statutory_date').show();
  $('#sdate').show();  //$('#statutory_date').show();
});
$('.repeatlabelendday').click(function () {
  //resetvalues();
  if ($('#single_statutory_month').val() != '') {
    var maxDate = load_date($('#single_statutory_month').val());
    $('#single_statutory_date').val(maxDate);
  } else {
    $('#single_statutory_date').val('31');
  }
  $('#statutory_date').val('31');
  for (i = 1; i <= 12; i++) {
    var mMonth = $('#multiple_statutory_month' + i).val();
    if (mMonth != '' || mMonth != undefined) {
      var maxDate = load_date(mMonth);
      $('#multiple_statutory_date' + i).val(maxDate);
    } else {
      $('#multiple_statutory_date' + i).val('31');
    }
    $('#multiple_statutory_date' + i).hide();
  }
  $('#single_statutory_date').hide();
  if ($('#repeats_type').val() == '2') {
    $('#sdate').hide();
  }  //$('#statutory_date').hide();
});
function load_date(selectedMonth) {
  var result;
  if (selectedMonth == 1 || selectedMonth == 3 || selectedMonth == 5 || selectedMonth == 7 || selectedMonth == 8 || selectedMonth == 10 || selectedMonth == 12) {
    result = 31;
  } else if (selectedMonth == 2) {
    result = 29;
  } else {
    result = 30;
  }
  return result;
}
function load_data() {
  if ($('#repeats_type').val() == '2' && $('.multipleinput').prop('checked') == true) {
    $('.multipleselectnone').hide();
    $('.multipleselect').show();
    $('#multipleview').show();
    $('#sdate').show();
    $('.repeatby-view').show();
    load_stautorydates();
  } else if ($('#repeats_type').val() == '1') {
    $('#single_statutory_date').hide();
    $('#single_statutory_month').hide();
    $('.multipleselect').hide();
    $('.multipleselectnone').show();
    $('#sdate').hide();
    $('#multipleview').hide();
    $('.repeatby-view').hide();
  } else if ($('#repeats_type').val() == '3') {
    $('#single_statutory_date').show();
    $('#single_statutory_month').show();
    $('.multipleselect').hide();
    $('.multipleselectnone').show();
    $('#sdate').show();
    $('.repeatby-view').show();
    $('#multipleview').hide();
    if ($('input[name="repeatby"]:checked').val() == 'enddayofmonth') {
      $('#single_statutory_date').hide();
    }
  } else if ($('#repeats_type').val() == '2' && $('.multipleinput').prop('checked') == false && $('#repeats_every').val() != '') {
    var rep_every = parseInt($('#repeats_every').val());
    var modResult = 12 % rep_every;
    if (modResult == 0 && rep_every < 12) {
      $('#single_statutory_date').show();
      $('#single_statutory_month').hide();
      $('.multipleselect').hide();
      $('.multipleselectnone').show();
      $('#sdate').show();
      $('.repeatby-view').show();
      $('#multipleview').show();
    } else {
      $('#single_statutory_date').show();
      $('#single_statutory_month').hide();
      $('.multipleselect').hide();
      $('.multipleselectnone').show();
      $('#sdate').show();
      $('.repeatby-view').show();
      $('#multipleview').hide();
      $('.multipleinput').prop('checked', false);
    }
    if ($('input[name="repeatby"]:checked').val() == 'enddayofmonth') {
      $('#single_statutory_date').hide();
      $('#single_statutory_month').hide();
      $('#sdate').hide();
    }
  }
  if ($('#repeats_type').val() == '2') {
    $('.repeatby-view').show();
  }
}
$('.dayhour').change(function () {
  if ($(this).val() == '1') {
    $('#days').show();
    $('#hours').hide();
    $('#trigger_every').show();
  } else if ($(this).val() == '2') {
    $('#days').hide();
    $('#hours').show();
    $('#trigger_every').show();
  }
});
$('.tasktype').on('keyup change', function () {
  if ($(this).val() == '2' || $(this).val() == '3') {
    $('#Recurring').show();
    $('#Occasional').hide();
    $('#One_Time').hide();
    if ($(this).val() == '2') {
      $('.frequency_type').html('Periodical');
    } else {
      $('.frequency_type').html('Review');
    }
  } else if ($(this).val() == '4') {
    $('#Recurring').hide();
    $('#Occasional').show();
    $('#One_Time').hide();
  } else if ($(this).val() == '1') {
    $('#Recurring').hide();
    $('#Occasional').hide();
    $('#One_Time').show();
  } else {
    $('#Recurring').hide();
    $('#Occasional').hide();
    $('#One_Time').hide();
  }
});
$('#statutory_date').empty();
var defaultoption = $('<option></option>');
defaultoption.val('');
defaultoption.text('');
$('#statutory_date').append(defaultoption);
for (var i = 1; i <= 31; i++) {
  var option = $('<option></option>');
  option.val(i);
  option.text(i);
  $('#statutory_date').append(option);
}
$('#statutory_month').empty();
var defaultoption1 = $('<option></option>');
defaultoption1.val('');
defaultoption1.text('Select');
$('#statutory_month').append(defaultoption1);
for (var i = 1; i <= 12; i++) {
  var option = $('<option></option>');
  var sMonth = getMonth_IntegettoString(i);
  option.val(i);
  option.text(sMonth);
  $('#statutory_month').append(option);
}
$('#single_statutory_date').empty();
var defaultoption = $('<option></option>');
defaultoption.val('');
defaultoption.text('');
$('#single_statutory_date').append(defaultoption);
for (var i = 1; i <= 31; i++) {
  var option = $('<option></option>');
  option.val(i);
  option.text(i);
  $('#single_statutory_date').append(option);
}
$('#single_statutory_month').empty();
var defaultoption1 = $('<option></option>');
defaultoption1.val('');
defaultoption1.text('Select');
$('#single_statutory_month').append(defaultoption1);
for (var i = 1; i <= 12; i++) {
  var option = $('<option></option>');
  var sMonth = getMonth_IntegettoString(i);
  option.val(i);
  option.text(sMonth);
  $('#single_statutory_month').append(option);
}
for (var j = 1; j <= 12; j++) {
  $('#multiple_statutory_date' + j).empty();
  var defaultoption = $('<option></option>');
  defaultoption.val('');
  defaultoption.text('');
  $('#multiple_statutory_date' + j).append(defaultoption);
  for (var i = 1; i <= 31; i++) {
    var option = $('<option></option>');
    option.val(i);
    option.text(i);
    $('#multiple_statutory_date' + j).append(option);
  }
  $('#multiple_statutory_month' + j).empty();
  var defaultoption1 = $('<option></option>');
  defaultoption1.val('');
  defaultoption1.text('Select');
  $('#multiple_statutory_month' + j).append(defaultoption1);
  for (var i = 1; i <= 12; i++) {
    var option = $('<option></option>');
    var sMonth = getMonth_IntegettoString(i);
    option.val(i);
    option.text(sMonth);
    $('#multiple_statutory_month' + j).append(option);
  }
}
$('#days').hide();
$('#hours').show();
$('#trigger_every').show();
//initialization & load date,month dynamically in statutory date selectbox
$(document).ready(function () {
  for (var j = 1; j <= 12; j++) {
    $('#multiple_statutory_month' + j).change(function () {
      var getVal = $(this).attr('id');
      var currentId = getVal.substring(getVal.lastIndexOf('h') + 1);
      var selectedMonth = $(this).val();
      var maxDate = load_date(selectedMonth);
      $('#multiple_statutory_date' + currentId).empty();
      var defaultoption = $('<option></option>');
      defaultoption.val('');
      defaultoption.text('');
      $('#multiple_statutory_date' + currentId).append(defaultoption);
      for (var i = 1; i <= maxDate; i++) {
        var option = $('<option></option>');
        option.val(i);
        option.text(i);
        $('#multiple_statutory_date' + currentId).append(option);
      }
      if ($('input[name="repeatby"]:checked').val() == 'enddayofmonth') {
        var selectedMonth = $('#multiple_statutory_month' + currentId).val();
        var monthDate = load_date(selectedMonth);
        $('#multiple_statutory_date' + currentId).val(monthDate);
      }
    });
  }
  getStatutoryMappings();
  getStatutoryMappingsMastersList();



});
//create tool tip
$(document).tooltip({
  position: {
    my: 'center bottom-20',
    at: 'center top',
    using: function (position, feedback) {
      $(this).css(position);
      $('<div>').addClass('arrow').addClass(feedback.vertical).addClass(feedback.horizontal).appendTo(this);
    }
  }
});
$('#statutory_provision').on('input', function (e) {
  this.value = isCommon($(this));
});
$('#compliance_task').on('input', function (e) {
  this.value = isCommon($(this));
});
$('#compliance_description').on('input', function (e) {
  this.value = isCommon($(this));
});
$('#compliance_document').on('input', function (e) {
  this.value = isCommon($(this));
});
$('#penal_consequences').on('input', function (e) {
  this.value = isCommon($(this));
});
$('#repeats_every').on('input', function (e) {
  this.value = isNumbers($(this));
});
$('#duration').on('input', function (e) {
  this.value = isNumbers($(this));
});
$('.trigger').on('input', function (e) {
  this.value = isNumbers($(this));
});