var groupAdmin_GroupList;
var groupAdmin_UnitList;

function getGroupAdmin_Group()
{
	function onSuccess(data) {
		groupAdmin_GroupList = data.groupadmin_groupList;
		groupAdmin_UnitList = data.groupadmin_unitList;
		fillGroupAdmingroupData(groupAdmin_GroupList);
	}
	function onFailure(error) {
		displayMessage(error);
	}
	mirror.getGroupAdminGroupList(function (error, response) {
		if (error == null) {
	  		onSuccess(response);
		} else {
  			onFailure(error);
		}
	});
}
function processGroupAdminFilters()
{
	var search_1, search_2, search_3;
	searchList = [];
	var grp_admin_table = $('#table-group-admin-group-list').attr('style');
	var grp_admin_unit_table = $('#table-grp-admin-unit-list').attr('style');
	if(grp_admin_table == "display: block;")
	{
		search_1 = $('#search-country-name').val().toLowerCase();
		search_2 = $('#search-Group-name').val().toLowerCase();
		search_3 = $('#search-no-legal-entity').val();

		for(var i in groupAdmin_GroupList)
		{
			row_data = groupAdmin_GroupList[i];
			var flg = false;
			for (var c in row_data.c_names) {
	          if (~row_data.c_names[c].toLowerCase().indexOf(search_1)){
	              flg = true;
	              continue;
	          }
	        }

			if((~row_data.group_name.toLowerCase().indexOf(search_2)) &&
			(~row_data.no_of_legal_entities.toString().indexOf(search_3)) && (flg == true))
			{
				searchList.push(row_data);
			}
		}
		fillGroupAdmingroupData(searchList);
	}
	else if(grp_admin_table == "display: none;")
	{
		search_1 = $('#search-unit-country-name').val().toLowerCase();
		search_2 = $('#search-legal_entity-name').val().toLowerCase();
		search_3 = $('#search-no-of-units').val();
		table_ctrl = $('.tbody-grp-admin-unit-email-list');
		table_tr = table_ctrl.find('tr');
		for(var i=0;i<table_tr.length;i++)
		{
			var table_ctry = table_tr[i].childNodes[3].innerText.toLowerCase();
			var table_le = table_tr[i].childNodes[5].innerText.toLowerCase();
			var table_lecnt = table_tr[i].childNodes[7].innerText.toLowerCase();
			if((~table_ctry.indexOf(search_1)) &&
			(~table_le.toLowerCase().indexOf(search_2)) &&
			(~table_lecnt.indexOf(search_3)))
			{
				searchList.push(groupAdmin_UnitList[i]);
			}
		}
		bindsearchedUnitList(searchList);
	}
}
function fillGroupAdmingroupData(groupAdminList)
{
	var i=1;
	var data = groupAdminList;
	$('.tbody-grp-admin-email-list').find('tr').remove();
	$.each(data, function(k, v) {
		var tableRow = $('#templates .table-group-admin-regn-master .table-row');
        var rowClone = tableRow.clone();
        $('.sno', rowClone).text(i);
        $('.client-id', rowClone).addClass('client-id-'+i);
        $('.Country', rowClone).text(v.c_names);
        $('.Group',rowClone).html(v.group_name);
        $('.No-of-legalentity', rowClone).html(v.no_of_legal_entities);
        if (v.ug_name == null && v.registration_email_date == null){
        	$('.btn-send', rowClone).show();
        	$('.btn-resend', rowClone).hide();
          	$('.btn-send', rowClone).on('click', function() {
            	sendCredentials(v.client_id, v.email_id, "send");
          	});
        }
        else if(v.ug_name == null && v.registration_email_date != null){
        	$('.btn-send', rowClone).hide();
        	$('.btn-resend', rowClone).show();
          	$('.btn-resend', rowClone).on('click', function() {
            	sendCredentials(v.client_id, v.email_id, "resend");
          	});
        }
        else if(v.ug_name != null && v.registration_email_date != null){
        	$('.btn-send', rowClone).hide();
          	$('#btnResend', rowClone).hide();
        }
        else if(v.ug_name != null && v.registration_email_date == null){
        	$('.btn-send', rowClone).hide();
          	$('.btn-resend', rowClone).hide();
        }
        $('#btnView', rowClone).on('click', function() {
            displayLegalEntityList(v.client_id, v.group_name);
        });

        $('.tbody-grp-admin-email-list').append(rowClone);
        i++;
	});
}
function sendCredentials(_cl_id, _e_id, mode) {
  req_dict = {
    'user_id': _cl_id,
    'email_id': _e_id,
    'grp_mode': mode
  };
  mirror.resendGroupAdminRegnmail(req_dict, function(error, response) {

    if (error == null) {
    	if(mode == "send")
      		displaySuccessMessage(message.send);
      	else
      		displaySuccessMessage(message.resend);
    }
    else {
      displayMessage(error);
    }
  });
}
function bindsearchedUnitList(data)
{
	$('#table-group-admin-group-list').hide();
	$('#table-grp-admin-unit-list').show();
	$('.tbody-grp-admin-unit-email-list').find('tr').remove();
	$('#btn-back').show();
	var i = 1;
	$.each(data, function(k, v) {
		var tableRow = $('#templates .table-group-admin-unit-master .table-row');
        var rowClone = tableRow.clone();

        $('.sno', rowClone).text(i);
        $('.Country', rowClone).html(v.country_name);
        $('.Legal-Entity',rowClone).html(v.legal_entity_name);
        $('.No-of-units', rowClone).html(v.unit_count);
        if (v.unit_creation_informed == 0){
      		$('#btnunit', rowClone).show();
      		if(v.unit_count == 0)
      		{
      			$('#btnunit', rowClone).css("background", "#999");
      			$('#btnunit', rowClone).attr('title', "Unit(s) not yet created");
      			$('#btnunit', rowClone).on('click', function() {
      				displayEmptyMsg("Unit(s) not yet created");
  				});
      		}
      		else
      		{
      			$('#btnunit', rowClone).on('click', function() {
            		sendmail('unit', v.user_id, v.emp_code_name, v.email_id, v.client_id,
        			group_name, v.legal_entity_id, v.legal_entity_name);
          		});
      		}
        }
        else {
          $('#btnunit', rowClone).hide();
        }
        if (v.statutory_assigned_informed == 0){
        	$('#btnstatutory', rowClone).show();
        	if(v.statutory_count == 0)
        	{
        		$('#btnstatutory', rowClone).css("background", "#999");
      			$('#btnstatutory', rowClone).attr('title', "Statutory(s) not yet assigned");
      			$('#btnstatutory', rowClone).on('click', function() {
      				displayEmptyMsg("Statutory(s) not yet assigned");
      			});
        	}
    		else
    		{
    			$('#btnstatutory', rowClone).on('click', function() {
					sendmail('statutory', v.user_id, v.emp_code_name, v.email_id, v.client_id,
        			group_name, v.legal_entity_id, v.legal_entity_name);
				});
    		}

        }
        else
        { v.client_id, v.legal_entity_id
        	$('#btnstatutory', rowClone).hide();
        }

        $('.tbody-grp-admin-unit-email-list').append(rowClone);
        i++;
	});
}
function displayEmptyMsg(msgText){
	displayMessage(msgText)
}
function displayLegalEntityList(client_id, group_name)
{
	$('#table-group-admin-group-list').hide();
	$('#table-grp-admin-unit-list').show();
	$('.tbody-grp-admin-unit-email-list').find('tr').remove();
	$('#btn-back').show(groupAdmin_UnitList.length);
	var i = 1;
	$.each(groupAdmin_UnitList, function(k, v) {
		if(v.client_id == client_id)
		{
			var tableRow = $('#templates .table-group-admin-unit-master .table-row');
	        var rowClone = tableRow.clone();

	        $('.sno', rowClone).text(i);
	        $('.Country', rowClone).html(v.country_name);
	        $('.Legal-Entity',rowClone).html(v.legal_entity_name);
	        $('.No-of-units', rowClone).html(v.unit_count);
	        if (v.unit_creation_informed == 0){
          		$('#btnunit', rowClone).show();
          		if(v.unit_count == 0)
          		{
          			$('#btnunit', rowClone).css("background", "#999");
          			$('#btnunit', rowClone).attr('title', "Unit(s) not yet created");
          			$('#btnunit', rowClone).on('click', function() {
	      				displayEmptyMsg("Unit(s) not yet created");
	  				});
          		}
          		else
          		{
          			$('#btnunit', rowClone).on('click', function() {
	            		sendmail('unit', v.emp_code_name, v.email_id, v.client_id,
            			group_name, v.legal_entity_id, v.legal_entity_name);
	          		});
          		}
	        }
	        else {
	          $('#btnunit', rowClone).hide();
	        }
	        if (v.statutory_assigned_informed == 0){
	        	$('#btnstatutory', rowClone).show();
	        	if(v.statutory_count == 0)
	        	{
	        		$('#btnstatutory', rowClone).css("background", "#999");
          			$('#btnstatutory', rowClone).attr('title', "Statutory(s) not yet assigned");
          			$('#btnstatutory', rowClone).on('click', function() {
	      				displayEmptyMsg("Statutory(s) not yet assigned");
	      			});
	        	}
        		else
        		{
        			$('#btnstatutory', rowClone).on('click', function() {
						sendmail('statutory', v.emp_code_name, v.email_id, v.client_id,
            			group_name, v.legal_entity_id, v.legal_entity_name);
					});
        		}

	        }
	        else
	        { v.client_id, v.legal_entity_id
	        	$('#btnstatutory', rowClone).hide();
	        }

	        $('.tbody-grp-admin-unit-email-list').append(rowClone);
	        i++;
		}
	});
}
function sendmail(_mode, _u_name, _e_id, _cl_id, _cl_name, _le_id, _le_name) {
	req_dict = {
		'grp_mode': _mode,
	    'username': _u_name,
	    'email_id': _e_id,
	    'client_id': _cl_id,
	    'group_name': _cl_name,
	    'legal_entity_id': _le_id,
	    'legal_entity_name': _le_name
	  };
	mirror.sendGroupAdminRegnmail(req_dict, function(error, response) {

    if (error == null) {
      displaySuccessMessage(message.send);
    }
    else {
      displayMessage(error);
    }
  });
}

function initialize_form()
{
	$('.table-grp-admin-unit-list').hide();
	$('.tbody-grp-admin-unit-email-list').find('tr').remove();
	$('#btn-back').hide();
	getGroupAdmin_Group();
}

$('#btn-back').click(function() {
    $('#table-group-admin-group-list').show();
	$('#table-grp-admin-unit-list').hide();
	$('.tbody-grp-admin-unit-email-list').find('tr').remove();
	$('#btn-back').hide();
});

$('.filter-text-box').keyup(function() {
    //processGroupAdminFilters();
  });

// page load
function initialize() {
	clearMessage();
  	initialize_form();
}

$(document).ready(function () {
  initialize();
});

$(document).find('.js-filtertable').each(function(){
    $(this).filtertable().addFilter('.js-filter');
});
$(document).find('.js-filtertable-le').each(function(){
    $(this).filtertable().addFilter('.js-filter-le');
});