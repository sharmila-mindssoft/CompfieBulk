var LegalEntityNameLabel = $(".legal-entity-name");
var LegalEntityNameAC = $(".legal-entity-name-ac");

var LegalEntityName = $("#legal-entity");
var LegalEntityId = $("#legal-entity-id");
var ACLegalEntity = $("#ac-legal-entity");

var AssigneeReminder = $("#assignee_reminder");
var Cc_App_Reminder = $("#conc_app_reminder");
var Ass_App_Cc_reminder = $("#ass_app_conc_days");
var Sp_Compl_Reminder = $("#sp_compl_reminder");

var btnSubmit = $(".btn-submit");

var _entities = [];
var _settings_info = [];
var _le_domains = [];
var _le_users = [];

function displayLoader() {
  $('.loading-indicator-spin').show();
}
function hideLoader() {
  $('.loading-indicator-spin').hide();
}

function loadEntityDetails() {
    if(_entities.length > 1) {
        LegalEntityNameLabel.hide();
        LegalEntityNameAC.show();
        $('.hr-1').hide();
        $('.reminder_1').hide();
        $('.reminder_2').hide();
        $('.reminder_3').hide();
        $('.reminder_4').hide();
        $('.btn-submit').hide();
        $('.hr-2').hide();
        $('.grp-details').hide();
        $('.domain-org').hide();
        $('.file-space').hide();
        $('.license-list').hide();
        $('.user-details').hide();
    } else {
        le_name = _entities[0]["le_name"];
        le_id = _entities[0]["le_id"];
        LegalEntityNameLabel.show();
        LegalEntityNameAC.hide();
        LegalEntityNameLabel.text(le_name);
        LegalEntityName.val(le_name);
        LegalEntityId.val(le_id);
        $('.hr-1').show();
        $('.reminder_1').show();
        $('.reminder_2').show();
        $('.reminder_3').show();
        $('.reminder_4').show();
        $('.btn-submit').show();
        $('.hr-2').show();
        $('.grp-details').show();
        $('.domain-org').show();
        $('.file-space').show();
        $('.license-list').show();
        $('.user-details').show();
		getSettingsForm(le_id);
    }
}

function getSettingsForm(le_id) {
	if (le_id !== undefined){
		displayLoader();
		client_mirror.getSettingsFormDetails(parseInt(le_id), function(error, response) {
	        console.log(error, response)
	        if (error == null) {
	        	_settings_info = response.settings_details;
	        	_le_users = response.settings_users;
	        } else {
	            displayMessage(error);
	        }
	    });
	    client_mirror.getLegalEntityDomains(parseInt(le_id), function(error, response) {
	        console.log(error, response)
	        if (error == null) {
	        	_le_domains = response.settings_domains;
	        	loadSettingDetails();
	        	hideLoader();
	        } else {
	            displayMessage(error);
	            hideLoader();
	        }
	    });
	}
}
// page load
function initialize() {
	_entities = [];
	_settings_info = [];
	_le_domains = [];
	_le_users = [];
	_entities = client_mirror.getSelectedLegalEntity();
	LegalEntityName.val('');
	LegalEntityName.focus();
	loadEntityDetails();
	PageControls();
}

function PageControls() {
	LegalEntityName.keyup(function(e) {
        var text_val = LegalEntityName.val().trim();
        if(text_val != ""){
        	var legalEntityList = _entities;
	        console.log(legalEntityList)
	        if (legalEntityList.length == 0 && text_val != '')
	            displayMessage(message.legalentity_required);
	        commonAutoComplete(e, ACLegalEntity, LegalEntityId, text_val, legalEntityList, "le_name", "le_id", function(val) {
	            onLegalEntityAutoCompleteSuccess(val);
	        });
        }
    });
}

onLegalEntityAutoCompleteSuccess = function(val) {
    LegalEntityName.val(val[1]);
    LegalEntityId.val(val[0]);
    LegalEntityName.focus();
    $("#assignee_reminder").val('');
    $("#conc_app_reminder").val('');
    $("#ass_app_conc_days").val('');
    $("#sp_compl_reminder").val('');
    $('.hr-1').show();
    $('.reminder_1').show();
    $('.reminder_2').show();
    $('.reminder_3').show();
    $('.reminder_4').show();
    $('.btn-submit').show();
    $('.hr-2').show();
    $('.grp-details').show();
    $('.domain-org').show();
    $('.file-space').show();
    $('.license-list').show();
    $('.user-details').show();
    getSettingsForm(val[0]);
}

function loadSettingDetails() {
	if(_settings_info.length > 0){
		if (_settings_info[0].two_level_approve == false) {
			$("#approvallevel_no").prop("checked", true);
		}
		else{
			$("#approvallevel_yes").prop("checked", true);
		}
		$("#assignee_reminder").val(_settings_info[0].assignee_reminder);
		$('#conc_app_reminder').val(_settings_info[0].advance_escalation_reminder);
		$('#ass_app_conc_days').val(_settings_info[0].escalation_reminder);
		$('#sp_compl_reminder').val(_settings_info[0].reassign_sp);
		$('.country-name').text(_settings_info[0].country_name);
		$('.bg-name').text(_settings_info[0].business_group_name);
		$('.le-name').text(_settings_info[0].legal_entity_name);
		$('.contract-from').text(_settings_info[0].contract_from);
		$('.contract-to').text(_settings_info[0].contract_to);
		var totaldiskspace = _settings_info[0].file_space_limit;
		var useddiskspace =  _settings_info[0].used_file_space;
		var free_space = (totaldiskspace - useddiskspace).toFixed(2);
		var calculate = (useddiskspace / totaldiskspace * 100).toFixed(2);
		var balance = 100 - calculate;
		if (calculate != '0.00') {
			$('.usedspace').show();
			$('.usedspace').css('width', calculate + '%');
			$('.totalspace').css('width', balance + '%');
			$('.totalspace').html(balance + '%');
			$('.usedspace').html(calculate + '%');
		} else {
			$('.usedspace').hide();
			$('.totalspace').css('width', balance + '%');
			$('.totalspace').html(balance + '%');
		}

		u_l = parseInt(_settings_info[0].used_licence);
		r_l = parseInt(_settings_info[0].total_licence) - parseInt(_settings_info[0].used_licence);
		$('.licence-details').text("Total Licence(s): "+_settings_info[0].total_licence+" - Used: "+ u_l+" | Remaining: "+r_l);

		// load domain, orgn.
		loadLeDomainOrgn();

		// load users details
		loadLeUsers();
	}
	else{
		displayMessage("No Reminders Exists")
	}
}

function loadLeDomainOrgn(){
	if(_le_domains.length > 0){
		var data = _le_domains;
		$('.table-le-domain-organization-list').find('tr').remove();
		var d_name = null;
		$.each(data, function(k, v) {
			if(d_name != v.domain_name){
				var clonethree = $('#templates #le-domain .table-row').clone();
				$('.domain-name', clonethree).text(v.domain_name);
	            $('.activation-date', clonethree).text(v.activity_date);
	            var o_name = "NA";
	            for (var i=0;i<data.length;i++){
	            	if(v.domain_name == data[i].domain_name){
	            		if(o_name == "NA"){
	            			o_name = data[i].organisation_name + " - "+data[i].org_count;
	            		}
	            		else
	            		{
	            			o_name = o_name + "<br />"+data[i].organisation_name + " - "+data[i].org_count;
	            		}
	            	}
	            }
	            $('.organisation-name', clonethree).append($.parseHTML(o_name));
	            $('.table-le-domain-organization-list').append(clonethree);
	            d_name = v.domain_name;
			}
		});
	}
	else{
		$('.table-le-domain-organization-list').empty();
        var tableRow4 = $('#no-record-templates .table-no-content .table-row-no-content');
        var clone4 = tableRow4.clone();
        $('.no_records', clone4).text('No Records Found');
        $('.table-le-domain-organization-list').append(clone4);
	}
}

function loadLeUsers() {
	if(_le_users.length > 0) {
		var data = _le_users;
		var j = 1;
    	$('.table-user-details').find('tr').remove();
		$.each(data, function(k, v) {
			var clonethree = $('#templates #user-details .table-row').clone();
			$('.sno', clonethree).text(j);
            $('.employee-name', clonethree).text(v.employee_name);
            // $('.user-id', clonethree).text(v.user_name);
            $('.user-level', clonethree).text(v.user_level_name);
            $('.user-category', clonethree).text(v.category_name);
            if(v.unit_code_name == null){
            	$('.seating-unit', clonethree).text(" - ");
            }else{
            	var unit_addr = v.address
	        	var unit_ctrl = "<i class='zmdi zmdi-info address-title' data-toggle='tooltip' title='"+unit_addr+"'></i>&nbsp;&nbsp;"+v.unit_code_name;
	            $('.seating-unit', clonethree).append($.parseHTML(unit_ctrl));
            }

            $('.table-user-details').append(clonethree);
            j = j + 1
		});
	}
	else{
		$('.table-user-details').empty();
        var tableRow4 = $('#no-record-templates .table-no-content .table-row-no-content');
        var clone4 = tableRow4.clone();
        $('.no_records', clone4).text('No Records Found');
        $('.table-user-details').append(clone4);
	}
}

btnSubmit.click(function() {
	if(validateMandatory() == true){
		var le_id = parseInt(LegalEntityId.val());
		var le_name = LegalEntityName.val();
		var app_opt = null;
		if ($("#approvallevel_no").prop("checked") == true) {
			app_opt = false;
		}
		else{
			app_opt = true;
		}
		var a_r = parseInt($("#assignee_reminder").val().trim());
		var c_a_r = parseInt($("#conc_app_reminder").val().trim());
		var a_a_c_r = parseInt($("#ass_app_conc_days").val().trim());
		var sp_r = parseInt($("#sp_compl_reminder").val().trim());
		console.log(le_id, le_name, app_opt, a_r, c_a_r, a_a_c_r, sp_r)
		client_mirror.saveSettingsFormDetails(le_id, le_name, app_opt, a_r, c_a_r, a_a_c_r, sp_r, function(error, response) {
        console.log(error, response)
        if (error == null) {
        	displaySuccessMessage(message.action_selection_success);
        } else {
            displayMessage(error);
        }
    });
	}
});

function validateMandatory(){
	if(LegalEntityId.val() == "" || LegalEntityName.val() == ""){
		displayMessage(message.legalentity_required);
		LegalEntityName.focus();
		return false;
	}
	else if ($("#assignee_reminder").val() == ""){
		displayMessage(message.reminder_assignee_required);
		$("#assignee_reminder").focus();
		return false;
	}
	else if(parseInt($("#assignee_reminder").val().trim()) > 99 || parseInt($("#assignee_reminder").val().trim()) <= 0){
		displayMessage(message.invalid_duration+" for AssigneeReminder");
		$("#assignee_reminder").focus();
		return false;
	}
	else if($("#conc_app_reminder").val() == ""){
		displayMessage(message.escalationreminder_concurrence_approval_required);
		$("#conc_app_reminder").focus();
		return false;
	}
	else if(parseInt($("#conc_app_reminder").val().trim()) > 99 || parseInt($("#conc_app_reminder").val().trim()) <= 0){
		displayMessage(message.invalid_duration+" for concurrence & approval person");
		$("#conc_app_reminder").focus();
		return false;
	}
	else if($("#ass_app_conc_days").val() == ""){
		displayMessage(message.escalationreminder_all);
		$("#ass_app_conc_days").focus();
		return false;
	}
	else if(parseInt($("#ass_app_conc_days").val().trim()) > 99 || parseInt($("#ass_app_conc_days").val().trim()) <= 0){
		displayMessage(message.invalid_duration+" for assignee, concurrence & approval person");
		$("#ass_app_conc_days").focus();
		return false;
	}
	else if($("#sp_compl_reminder").val() == ""){
		displayMessage(message.reassignreminder_all);
		$("#sp_compl_reminder").focus();
		return false;
	}
	else if(parseInt($("#sp_compl_reminder").val().trim()) > 99 || parseInt($("#sp_compl_reminder").val().trim()) <= 0){
		displayMessage(message.invalid_duration+" for service provider's reminder");
		$("#sp_compl_reminder").focus();
		return false;
	}
	else{
		return true;
	}
}

$("#assignee_reminder").on('input', function (e) {
  this.value = isNumbers($(this));
});

$("#conc_app_reminder").on('input', function (e) {
  this.value = isNumbers($(this));
});

$("#ass_app_conc_days").on('input', function (e) {
  this.value = isNumbers($(this));
});

$("#sp_compl_reminder").on('input', function (e) {
  this.value = isNumbers($(this));
});

$(document).ready(function() {
    initialize();

    $(document).find('.js-filtertable').each(function() {
        $(this).filtertable().addFilter('.js-filter');
    });
});