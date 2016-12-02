
var assignLegalEntitiesList = '';
var userList = '';
var CLIENT_ID = 0;

// Add screen fields
var AddScreen = $('#assign-le-add');
var ViewScreen =  $('#assign-le-view');
var ListScreen =  $('#assign-le-list');
var ListFilterBox = $('.list-filter');
var AddFilterBox = $('.add-filter');
var SaveButton = $('#save');
var CancelButton = $('.btn-cancel');

var User_id = $('#userid');
var User_val = $('#userval');
var Group_Label = $('.group-label');
var Country_Label = $('.country-label');

var ListFilterCountry = $('#list-filter-country');
var ListFilterGroup = $('#list-filter-group');
var AddFilterCountry = $('#add-filter-country');
var AddFilterBG = $('#add-filter-bg');
var AddFilterLE = $('#add-filter-le');

var AC_User = $('#ac-user');
var AC_Textbox = $('.ac-textbox');

function resetValues(){
  ListFilterBox.val('');
  AddFilterBox.val('');
  Group_Label.text('');
  Country_Label.text('');
  User_val.val('');
  User_id.val('');
}

function processCancel (){
  AddScreen.hide();
  ViewScreen.hide();
  ListScreen.show();
  resetValues();
}

function processSave (){
  if(validateMandatory()){
    var s_users = [];
    var s_le = [];
    s_users.push(parseInt(User_id.val()));
    $('input[name="le"]:checked').each(function() {
      var splitIds = (this.value).split(',');
      s_le.push(parseInt(splitIds[1]));
    });
    mirror.saveAssignLegalEntity(CLIENT_ID, s_le, s_users, function (error, response) {
        if (error == null) {
          AddScreen.hide();
          ListScreen.show();
          ViewScreen.hide();
          initialize();
        }else {
          custom_alert(error);
        }
    });
  }
}

function assignLE(cId, cName, gName){
	  CLIENT_ID = cId
    mirror.getEditAssignLegalEntity(cId, function (error, data) {
        if (error == null) {
          ListScreen.hide();
          AddScreen.hide();
          AddScreen.show();
          Group_Label.text(gName);
          Country_Label.text(cName);
          assignLegalEntitiesList = data.unassign_legal_entities;
          userList = data.techno_users;
          loadLegalEntityList(assignLegalEntitiesList);
        }else {
            custom_alert(error);
        }
    });
}

function viewLE(cId, cName, gName){
	CLIENT_ID = cId;
  mirror.viewAssignLegalEntity(cId, function (error, data) {
    if (error == null) {
        ListScreen.hide();
        AddScreen.hide();
        ViewScreen.show();
        Group_Label.text(gName);
        Country_Label.text(cName);
        assignLegalEntitiesList = data.assigned_legal_entities;
        loadUserList(assignLegalEntitiesList);
    }else {
        custom_alert(error);
    }
  });
}

function loadGroupList(assignLegalEntitiesList) {
  var j = 1;
  $('.tbody-list').find('tr').remove();
  $.each(assignLegalEntitiesList, function (key, value) {
  	var assignedLE = 0;
  	var client_id = value.client_id;
    var groupName = value.group_name;
    var countryName = value.country_name;
    var legalEntityCount = value.no_of_legal_entities;
    if(value.no_of_assigned_legal_entities != null) assignedLE =  value.no_of_assigned_legal_entities;
    var unAssignedLE =  (legalEntityCount - assignedLE);

    var tableRow = $('#templates .table-assign-le-list .table-row');
    var clone = tableRow.clone();
    $('.sno', clone).text(j);
    $('.country', clone).text(countryName);
    $('.group', clone).text(groupName);
    $('.unassigned-le', clone).text(unAssignedLE + ' / ' +legalEntityCount);
    if(unAssignedLE > 0){
    	$('.assign', clone).on('click', function () {
	      assignLE(client_id, countryName, groupName);
	    });
    }
    if(unAssignedLE != legalEntityCount){
	    $('.view', clone).on('click', function () {
	      viewLE(client_id, countryName, groupName);
	    });
	}
    $('.tbody-list').append(clone);
    j = j + 1;
  });
}

function loadLegalEntityList(assignLegalEntitiesList) {
  var j = 1;
  $('.tbody-add-list').find('tr').remove();
  $.each(assignLegalEntitiesList, function (key, value) {
  	var assignedLE = 0;
    var leId = value.legal_entity_id;
    var leName = value.legal_entity_name;
    var bgName = '-';
    if(value.business_group_name != null) bgName = value.business_group_name;
    var cName = value.c_name;
    var cId = value.c_id;
    var combileId = cId + ',' +leId;
  
    var tableRow = $('#templates .table-assign-le-add .table-row');
    var clone = tableRow.clone();
    $('.ck-box', clone).attr('id', 'legalentity' + j);
    $('.ck-box', clone).val(combileId);
    $('.add-country', clone).text(cName);
    $('.add-bgroup', clone).text(bgName);
    $('.add-le', clone).text(leName);

    $('.tbody-add-list').append(clone);
    j = j + 1;
    $('.form_checkbox').on('click', function (e) {
      $('#usersSelected').val('');
      var che = $('.form_checkbox:checked');
      $('.selected_checkbox_count').html(che.length);
      $('.form_checkbox').closest('tr').removeClass('checked_row');
      che.closest('tr').addClass('checked_row');
    });
  });
}

function loadUserList(assignLegalEntitiesList) {
  var j = 1;
  $('.tbody-view-list').find('tr').remove();
  $.each(assignLegalEntitiesList, function (key, value) {
    var leName = value.legal_entity_name;
    var bgName = '-';
    if(value.business_group_name != null) bgName = value.business_group_name;
    var cName = value.c_name;
    
    var tableRow = $('#templates .table-assign-le-view .table-row');
    var clone = tableRow.clone();
    $('.view-country', clone).text(cName);
    $('.view-bgroup', clone).text(bgName);
    $('.view-le', clone).text(leName);
    $('.tbody-view-list').append(clone);
    j = j + 1;
  });
}

function checkusercountries(userid, usercountryids) {
	var returnval = 0;
	var arrc = [];
	var countryids = [];
	$('input[name="le"]:checked').each(function() {
		var splitIds = (this.value).split(',');
		countryids.push(parseInt(splitIds[0]));
	});
  for (var mc = 0; mc < countryids.length; mc++) {
    for (var m = 0; m < usercountryids.length; m++) {
      if (usercountryids[m] == countryids[mc]) {
        arrc.push(usercountryids[m]);
      }
    }
  }
	if (arrc.length > 0) {
	  returnval = 1;
	}
	return returnval;
}

function validateMandatory(){
	if($('.form_checkbox:checked').length == 0){
		displayMessage(message.no_legal_entity_selected);
		return false;
	}
	else if (User_id.val().length == 0){
		displayMessage(message.no_user_selected);
		return false;
	}else{
		return true;
	}
}

//filter process
function processListFilter(){
  var countryfilter = ListFilterCountry.val().toLowerCase();
  var groupfilter = ListFilterGroup.val().toLowerCase();
  var filteredList = [];
  for (var entity in assignLegalEntitiesList) {
    var countryName = assignLegalEntitiesList[entity].country_name;
    var groupName = assignLegalEntitiesList[entity].group_name;
    if (~countryName.toLowerCase().indexOf(countryfilter) && ~groupName.toLowerCase().indexOf(groupfilter)) {
      filteredList.push(assignLegalEntitiesList[entity]);
    }
  }
  loadGroupList(filteredList);
}

function processAddFilter(){
  var addcountryfilter = AddFilterCountry.val().toLowerCase();
  var bgfilter = AddFilterBG.val().toLowerCase();
  var lefilter = AddFilterLE.val().toLowerCase();

  var filteredList = [];
  for (var entity in assignLegalEntitiesList) {
    var countryName = assignLegalEntitiesList[entity].c_name;
    var bgName = assignLegalEntitiesList[entity].business_group_name;
    var leName = assignLegalEntitiesList[entity].legal_entity_name;
    if (~countryName.toLowerCase().indexOf(addcountryfilter) && ~bgName.toLowerCase().indexOf(bgfilter) && ~leName.toLowerCase().indexOf(lefilter)) {
      filteredList.push(assignLegalEntitiesList[entity]);
    }
  }
  loadLegalEntityList(filteredList);
}

function initialize(){
		resetValues();
    mirror.getAssignLegalEntityList(function (error, data) {
        if (error == null) {
          assignLegalEntitiesList = data.assign_le_list;
          loadGroupList(assignLegalEntitiesList);
        }else {
          custom_alert(error);
        }
    });
}

function activate_technouser(element) {
  AC_Textbox.hide();
  var ac_id = $(element).attr('id');
  var ac_name = $(element).text();
  User_val.val(ac_name);
  User_id.val(ac_id);
}

function pageControls() {

  CancelButton.click(function () {
    processCancel();
  });

  SaveButton.click(function () {
    processSave();
  });

  ListFilterBox.keyup(function() {
    processListFilter();
  });

  AddFilterBox.keyup(function() {
    processAddFilter();
  });

  User_val.keyup(function (e) {
    var textval = $(this).val();
    AC_User.show();
    User_id.val('');
    var users = userList;
    var suggestions = [];
    $('#ac-user ul').empty();
    if (textval.length > 0) {
        for (var i in users) {
            if (~users[i].employee_name.toLowerCase().indexOf(textval.toLowerCase()) && users[i].is_active == true){
              if (checkusercountries(users[i].user_id, users[i].country_ids) == 1) {
              suggestions.push([
                users[i].user_id,
                users[i].employee_name
              ]);
            }
            }
        }
        var str = '';
        for (var i in suggestions) {
          str += '<li id="' + suggestions[i][0] + '"onclick="activate_technouser(this)">' + suggestions[i][1] + '</li>';
        }
        $('#ac-user ul').append(str);
    } else {
        AC_Textbox.hide();
    }
  });
}
$(document).ready(function () {
    initialize();
    pageControls();
});
