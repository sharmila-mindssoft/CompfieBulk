
var assignLegalEntitiesList = '';
var userList = '';
var CLIENT_ID = 0;

$('.btn-cancel').click(function () {
  $('#assign-le-add').hide();
  $('#assign-le-view').hide();
  $('#assign-le-list').show();
  resetValues();
});

function assignLE(cId, cName, gName){
	CLIENT_ID = cId;
	function onSuccess(data) {
		$('#assign-le-list').hide();
		$('#assign-le-view').hide();
		$('#assign-le-add').show();
		$('.group-label').text(gName);
		$('.country-label').text(cName);
		assignLegalEntitiesList = data.unassign_legal_entities;
		userList = data.techno_users;
        loadAddList(assignLegalEntitiesList);
    }
    function onFailure(error) {
        custom_alert(error);
    }
    mirror.getEditAssignLegalEntity(cId, function (error, response) {
        if (error == null) {
            onSuccess(response);
        }else {
            onFailure(error);
        }
    });
}

function viewLE(cId, cName, gName){
	CLIENT_ID = cId;
	function onSuccess(data) {
		$('#assign-le-list').hide();
		$('#assign-le-add').hide();
		$('#assign-le-view').show();
		$('.group-label').text(gName);
		$('.country-label').text(cName);
		assignLegalEntitiesList = data.assigned_legal_entities;
        loadView(assignLegalEntitiesList);
    }
    function onFailure(error) {
        custom_alert(error);
    }
    mirror.viewAssignLegalEntity(cId, function (error, response) {
        if (error == null) {
            onSuccess(response);
        }else {
            onFailure(error);
        }
    });
}

function loadList(assignLegalEntitiesList) {
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

function loadAddList(assignLegalEntitiesList) {
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

function loadView(assignLegalEntitiesList) {
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

function checkuser(userid, usercountryids) {
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

$('#userval').keyup(function (e) {
  	var textval = $(this).val();
  	$('#ac-user').show();
	$('#userid').val('');
	var users = userList;
	var suggestions = [];
	$('#ac-user ul').empty();
	if (textval.length > 0) {
	    for (var i in users) {
	      	if (~users[i].employee_name.toLowerCase().indexOf(textval.toLowerCase()) && users[i].is_active == true){
	      		if (checkuser(users[i].user_id, users[i].country_ids) == 1) {
			      suggestions.push([
		          users[i].user_id,
		          users[i].employee_name
		        ]);
			    }
	      	}
	    }
	    var str = '';
	    for (var i in suggestions) {
	      str += '<li id="' + suggestions[i][0] + '"onclick="activate_text(this)">' + suggestions[i][1] + '</li>';
	    }
	    $('#ac-user ul').append(str);
	} else {
	    $('.ac-textbox').hide();
	}
});

function activate_text(element) {
  $('.ac-textbox').hide();
  var ac_id = $(element).attr('id');
  var ac_name = $(element).text();
  $('#userval').val(ac_name);
  $('#userid').val(ac_id);
}

function validateMandatory(){
	if($('.form_checkbox:checked').length == 0){
		displayMessage(message.no_legal_entity_selected);
		return false;
	}
	else if ($('#userid').val().length == 0){
		displayMessage(message.no_user_selected);
		return false;
	}else{
		return true;
	}
}

$('#save').click(function () {
	if(validateMandatory()){
		var s_users = [];
		var s_le = [];
		s_users.push(parseInt($('#userid').val()));

		$('input[name="le"]:checked').each(function() {
			var splitIds = (this.value).split(',');
			s_le.push(parseInt(splitIds[1]));
		});

		function onSuccess(data) {
			$('#assign-le-add').hide();
			$('#assign-le-list').show();
			$('#assign-le-view').hide();
			initialize();
	    }
	    function onFailure(error) {
	        custom_alert(error);
	    }
	    mirror.saveAssignLegalEntity(CLIENT_ID, s_le, s_users, function (error, response) {
	        if (error == null) {
	            onSuccess(response);
	        }else {
	            onFailure(error);
	        }
	    });
	}
});

//filter process
$('.list-filter').keyup(function () {
  var countryfilter = $('#list-filter-country').val().toLowerCase();
  var groupfilter = $('#list-filter-group').val().toLowerCase();
  var filteredList = [];
  for (var entity in assignLegalEntitiesList) {
    var countryName = assignLegalEntitiesList[entity].country_name;
    var groupName = assignLegalEntitiesList[entity].group_name;
    if (~countryName.toLowerCase().indexOf(countryfilter) && ~groupName.toLowerCase().indexOf(groupfilter)) {
      filteredList.push(assignLegalEntitiesList[entity]);
    }
  }
  loadList(filteredList);
});

$('.add-filter').keyup(function () {
  var countryfilter = $('#add-filter-country').val().toLowerCase();
  var bgfilter = $('#add-filter-bg').val().toLowerCase();
  var lefilter = $('#add-filter-le').val().toLowerCase();

  var filteredList = [];
  for (var entity in assignLegalEntitiesList) {
    var countryName = assignLegalEntitiesList[entity].c_name;
    var bgName = assignLegalEntitiesList[entity].business_group_name;
    var leName = assignLegalEntitiesList[entity].legal_entity_name;
    if (~countryName.toLowerCase().indexOf(countryfilter) && ~bgName.toLowerCase().indexOf(bgfilter) && ~leName.toLowerCase().indexOf(lefilter)) {
      filteredList.push(assignLegalEntitiesList[entity]);
    }
  }
  loadAddList(filteredList);
});

function resetValues(){
	displayMessage('');  
	$('.filter-text-box').val('');
	$('.group-label').text('');
	$('.country-label').text('');
	$('#usersSelected').val('');
}
function initialize(){
		resetValues();
        function onSuccess(data) {
            assignLegalEntitiesList = data.assign_le_list;
            loadList(assignLegalEntitiesList);
        }
        function onFailure(error) {
            custom_alert(error);
        }
        mirror.getAssignLegalEntityList(function (error, response) {
            if (error == null) {
                onSuccess(response);
            }else {
                onFailure(error);
            }
        });
}

$(document).ready(function () {
    initialize();
});
