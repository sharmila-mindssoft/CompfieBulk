var allocate_server_list = [];
var application_server_list = [];
var database_server_list = [];
var file_server_list = [];
var edit_id = null;
var client_ids = null;
var client_id = null;
var legal_entity_id = null;
var legal_entity_ids = null;
var le_legal_entity_ids = null;
var f_legal_entity_ids = null;
var old_grp_app_id = null;
var old_grp_db_s_id = null;
var old_le_db_s_id = null;
var old_le_f_s_id = null;
var old_grp_le_ids = null;
var old_le_le_ids = null;
var old_f_le_ids = null;
var old_cl_ids = null;

var group_application_server_name = $('#group-application-server-name');
var AC_group_application_server = $('#ac-appliaction-server');
var group_application_server_id = $('#application_id');

var group_db_server_name = $('#group-database-server-name');
var AC_group_db_server = $('#ac-grp-database-server');
var group_db_server_id = $('#database_server_id');

var le_application_server_name = $('#le-application-server-name');
var le_db_server_name = $('#le-database-server-name');
var AC_le_db_server = $('#ac-le-database-server');
var le_db_server_id = $('#le_database_server_id');

var le_file_server_name = $('#le-file-server-name');
var AC_le_file_server = $('#ac-le-file-server');
var le_file_server_id = $('#le_file_server_id');

var btn_cancel = $('.btn-cancel');
var btn_submit = $('#submit');

var PasswordSubmitButton = $('#password-submit');
var CurrentPassword = $('#current-password');
var isAuthenticate;

function displayLoader() {
  $('.loading-indicator-spin').show();
}
function hideLoader() {
  $('.loading-indicator-spin').hide();
}

function initialize(){
    clearMessage();
    edit_id = null;
    function onSuccess(data) {
    	allocate_server_list = data.client_dbs;
    	application_server_list = data.client_server_name_and_id;
    	database_server_list = data.db_server_name_and_id;
    	file_server_list = data.file_server_list;
    	loadAllocateDbEnvData();
        hideLoader();
    }
    function onFailure(error) {
        displayMessage(error);
    }
    displayLoader();
    mirror.getAllocatedDBEnv(function (error, response) {
        if (error == null) {
            onSuccess(response);
        } else {
            onFailure(error);
        	hideLoader();
        }
    });
}

function loadAllocateDbEnvData(){
	$(".tbody-allocate-server-list").empty();
    var table_row = $("#templates .table-row");
    var sno = 0;
    $.each(allocate_server_list, function(key, value){
        ++ sno;
        var clone = table_row.clone();
        $(".sno", clone).text(sno);
        $(".group", clone).text(value.group_name);
        $(".le", clone).text(value.legal_entity_name);
        $(".application-server", clone).text(value.machine_name);
        $(".db-server", clone).text(value.db_server_name);
        $(".file-server", clone).text(value.file_server_name);

        if(value.is_created == "0" || value.is_created == 0 || value.is_created == false){
        	$('.edit', clone).hide();
        	$('.btn-create', clone).show();
        	$('.btn-create', clone).on('click', function () {
	           loadCreateForm(value.client_id, value.legal_entity_id);
            });
        }
        else
        {
        	$('.edit', clone).show();
        	$('.btn-create', clone).hide();
        	$('.edit').attr('title', 'Click Here to Edit');
            $('.edit', clone).addClass('fa-pencil text-primary');
        	$('.edit', clone).on('click', function () {
                loadEditForm(allocate_server_list[key]);
            });

        }

        $(".tbody-allocate-server-list").append(clone);
    });
}

btn_cancel.click(function(){
	$('#allocate-server-view').show();
    $('#allocate-server-add').hide();
});

btn_submit.on('click', function(e) {
	if(validateMandatory() == true){
		CurrentPassword.val('');
        Custombox.open({
            target: '#custom-modal',
            effect: 'contentscale',
            complete: function() {
                CurrentPassword.focus();
                isAuthenticate = false;
            },
            close: function() {
                if (isAuthenticate) {
                    SaveAllocatedDB();
                }
            },
        });
	}
});

function checkClientIds(client_ids, application_id){
	var splitClientIds = null;
	var client_count = 0;

	if(client_ids != null){
		var splitClientIds = client_ids.split(",");
		for(var i=0;i<splitClientIds.length;i++){
			if(splitClientIds[i] == application_id){
				client_count++;
			}
		}
	}

	if(client_count == 0){
		if(client_ids != null)
			client_ids = client_ids + "," + application_id;
		else
			client_ids = application_id.toString();
	}
	return client_ids;
}

function checkLEIds(legal_entity_ids, db_s_id){
	var splitLEIds = null;
	var le_count = 0;

	if(legal_entity_ids != null && legal_entity_ids != ""){
		splitLEIds = legal_entity_ids.split(",");
		for(var i=0;i<splitLEIds.length;i++){
			if(splitLEIds[i] == db_s_id){
				le_count++;
			}
		}
	}


	if(le_count == 0){
		if(legal_entity_ids != null && legal_entity_ids != "")
			legal_entity_ids = legal_entity_ids + "," + db_s_id;
		else
			legal_entity_ids = db_s_id.toString();
	}
	return legal_entity_ids;
}

function removeCLIds(cl_ids, cl_id){
	var splitCLIds = null;
	var new_cl_ids = null;

	if(cl_ids != null){
		if (cl_ids.indexOf(",") >= 0){
			splitCLIds = cl_ids.split(",");
			for(var i=0;i<splitCLIds.length;i++){
				if(splitCLIds[i] == cl_id){
				}
				else{
					if (new_cl_ids == null)
					{
						new_cl_ids = splitCLIds[i];
					}
					else{
						new_cl_ids = new_cl_ids + "," + splitCLIds[i];
					}
				}
			}
		}
		else
		{
			if (new_cl_ids == null)
			{
				if(cl_ids == cl_id){
					new_cl_ids = "";
				}else{
					new_cl_ids = splitCLIds[i];
				}
			}
		}
	}
	return new_cl_ids;
}

function removeLEIds(legal_entity_ids, le_id){
	var splitLEIds = null;
	var new_le_ids = null;
	var le_count = 0;

	if(legal_entity_ids != null){
		if(legal_entity_ids.indexOf(",") >= 0){
			splitLEIds = legal_entity_ids.split(",");
			for(var i=0;i<splitLEIds.length;i++){
				if(splitLEIds[i] == le_id){
				}
				else{
					if (new_le_ids == null)
						new_le_ids = splitLEIds[i];
					else
						new_le_ids = new_le_ids + "," + splitLEIds[i];
				}
			}
		}else{
			if (new_le_ids == null){
				if (legal_entity_ids == le_id){
					new_le_ids = "";
				}
				else{
					new_le_ids = le_id;
				}
			}
		}
	}
	return new_le_ids;
}

function validateMandatory(){
	var returnMandatory = true;
	if(group_application_server_name.val() == '' || $('#application_id').val() == ""){
		displayMessage(message.client_server_name_required);
		group_application_server_name.val('');
		group_application_server_name.focus();
		returnMandatory = false;
	}
	else if(group_db_server_name.val() == '' || $('#database_server_id').val() == ""){
		displayMessage(message.db_server_name_required);
		group_db_server_name.val('');
		group_db_server_name.focus();
		returnMandatory = false;
	}
	else if(le_db_server_name.val() == '' || $('#le_database_server_id').val() == ""){
		displayMessage(message.le_db_server_name_required);
		le_db_server_name.val('');
		le_db_server_name.focus();
		returnMandatory = false;
	}
	else if(le_file_server_name.val() == '' || $('#le_file_server_id').val() == ""){
		displayMessage(message.le_file_server_name_required);
		le_file_server_name.val('');
		le_file_server_name.focus();
		returnMandatory = false;
	}

	return returnMandatory;
}

function SaveAllocatedDB() {
	var new_grp_le_ids = null, new_le_le_ids = null, new_f_le_ids = null, new_grp_cl_ids = null;
	client_ids = checkClientIds(client_ids,client_id);
	legal_entity_ids = checkLEIds(legal_entity_ids, legal_entity_id);
	le_legal_entity_ids = checkLEIds(le_legal_entity_ids, legal_entity_id);
	f_legal_entity_ids = checkLEIds(f_legal_entity_ids, legal_entity_id);
	if (old_grp_app_id != $('#application_id').val()){
		new_grp_cl_ids = removeCLIds(old_cl_ids, client_id);
	}else{
		new_grp_cl_ids = old_cl_ids;
	}

	if (old_grp_db_s_id != $('#database_server_id').val()){
		new_grp_le_ids = removeLEIds(old_grp_le_ids, legal_entity_id);
	}else{
		new_grp_le_ids = old_grp_le_ids;
	}

	if (old_le_db_s_id != $('#le_database_server_id').val()){
		new_le_le_ids = removeLEIds(old_le_le_ids, legal_entity_id);
	}else{
		new_le_le_ids = old_le_le_ids;
	}
	if (old_le_f_s_id != $('#le_file_server_id').val()){
		new_f_le_ids = removeLEIds(old_f_le_ids, legal_entity_id);
	}else{
		new_f_le_ids = old_f_le_ids;
	}

	function onSuccess(data) {
        initialize();
        $('#allocate-server-view').show();
		$('#allocate-server-add').hide();
        hideLoader();
    }
    function onFailure(error) {
        displayMessage(error);
        hideLoader();
    }
    displayLoader();

	mirror.saveDBEnv(edit_id, client_id, legal_entity_id, parseInt($('#application_id').val()),
		parseInt($('#database_server_id').val()), parseInt($('#le_database_server_id').val()),
		parseInt($('#le_file_server_id').val()), client_ids, legal_entity_ids, f_legal_entity_ids, le_legal_entity_ids,
		parseInt(old_grp_app_id), parseInt(old_grp_db_s_id), parseInt(old_le_db_s_id), parseInt(old_le_f_s_id),
		new_grp_cl_ids, new_grp_le_ids, new_le_le_ids, new_f_le_ids, function (error, response) {
        if (error == null) {
        	if (edit_id != null){
        		displaySuccessMessage(message.allocated_db_env_update);
        	}else{
	        	app_name = "\""+group_application_server_name.val().trim()+"\"";
	    		displaySuccessMessage(message.allocated_db_env_save.replace('app_name', app_name));
    		}
    		edit_id = null;
            onSuccess(response);
        } else {
            onFailure(error);
        }
    });
}

//validate
function validateAuthentication() {
    var password = CurrentPassword.val().trim();

    if (password.length == 0) {
        displayMessage(message.password_required);
        CurrentPassword.focus();
        return false;
    } else {
        if (validateMaxLength('password', password, "Password") == false) {
            return false;
        }
    }
    displayLoader();
    mirror.verifyPassword(password, function(error, response) {
        if (error == null) {
            isAuthenticate = true;
            Custombox.close();
        	hideLoader();
        } else {
        	hideLoader();
            if(error == "InvalidPassword")
                displayMessage(message.invalid_password);
            else
                displayMessage(error);
        }
    });
}

function loadCreateForm(cl_id, legal_e_id) {
	// body...
	client_id = cl_id;
	legal_entity_id = legal_e_id;
	$('#allocate-server-add').show();
    $('#allocate-server-view').hide();
	resetFields();
	$('.group-name').text(getFieldNames("group",client_id));
	$('.le-name').text(getFieldNames("le",legal_entity_id));
	for(var i=0;i<allocate_server_list.length;i++){
		indexValues = allocate_server_list[i];
		if(indexValues.client_id == cl_id && indexValues.client_database_id != null){
			group_application_server_name.val(indexValues.machine_name);
			$('#application_id').val(indexValues.machine_id);
			old_grp_app_id = $('#application_id').val();
			$('.appl-grp-ip-port').text(loadApplicationIpAndPort(indexValues.machine_id));
			group_db_server_name.val(indexValues.client_db_server_name);
			$('#database_server_id').val(indexValues.client_db_server_id);
			old_grp_db_s_id = $('#database_server_id').val();
			$('.db-grp-ip-port').text(loadDatabaseIpAndPort(indexValues.client_db_server_id));
			$('.le-appl-server-name').text(indexValues.machine_name);
			$('.le-appl-server-ip-port').text($('.appl-grp-ip-port').text());
		}
	}
}

function loadEditForm(indexValues){
	//edit_id = 1;
	resetFields();
	$('#allocate-server-add').show();
    $('#allocate-server-view').hide();
    edit_id = indexValues.client_database_id;
    client_id = indexValues.client_id;
    legal_entity_id = indexValues.legal_entity_id;
	$('.group-name').text(indexValues.group_name);
	$('.le-name').text(indexValues.legal_entity_name);
	group_application_server_name.val(indexValues.machine_name);
	$('#application_id').val(indexValues.machine_id);
	old_grp_app_id = $('#application_id').val();
	$('.appl-grp-ip-port').text(loadApplicationIpAndPort(indexValues.machine_id));
	group_db_server_name.val(indexValues.client_db_server_name);
	$('#database_server_id').val(indexValues.client_db_server_id);
	old_grp_db_s_id = $('#database_server_id').val();
	$('.db-grp-ip-port').text(loadDatabaseIpAndPort(indexValues.client_db_server_id));
	$('.le-appl-server-name').text(indexValues.machine_name);
	$('.le-appl-server-ip-port').text($('.appl-grp-ip-port').text());
	le_db_server_name.val(indexValues.db_server_name);
	$('#le_database_server_id').val(indexValues.db_server_id);
	old_le_db_s_id = $('#le_database_server_id').val();
	$('.db-le-ip-port').text(loadDatabaseIpAndPort(indexValues.db_server_id));
	le_file_server_name.val(indexValues.file_server_name);
	$('#le_file_server_id').val(indexValues.file_server_id);
	old_le_f_s_id = $('#le_file_server_id').val();
	$('.file-le-ip-port').text(loadFileIpAndPort(indexValues.file_server_id));

	old_cl_ids = loadClIDS(old_grp_app_id);
	old_grp_le_ids = loadLEIDS(old_grp_db_s_id);
	old_le_le_ids = loadLEIDS(old_le_db_s_id);
	old_f_le_ids = loadFileLEIDS(old_le_f_s_id);
}

function getFieldNames(item, id){
	var returnString = null;
	if(item == "group"){
		$.each(allocate_server_list, function(key, value){
			if(id == value.client_id){
				returnString = value.group_name;
			}
		});
	}
	else if(item == "le"){
		$.each(allocate_server_list, function(key, value){
			if(id == value.legal_entity_id){
				returnString = value.legal_entity_name;
			}
		});
	}
	else if(item == "a_server_name"){
		$.each(allocate_server_list, function(key, value){
			if(id == value.machine_id){
				returnString = value.machine_name;
			}
		});
	}
	else if(item == "d_server_name"){
		$.each(allocate_server_list, function(key, value){
			if(id == value.db_server_id){
				returnString = value.db_server_name;
			}
		});
	}
	else if(item == "f_server_name"){
		$.each(allocate_server_list, function(key, value){
			if(id == value.file_server_id){
				returnString = value.file_server_name;
			}
		});
	}
	return returnString;

}

function resetFields(){
	group_application_server_name.val('');
	$('#application_id').val('');
	group_db_server_name.val('');
	$('#database_server_id').val('');
	le_application_server_name.val('');
	$('#le_database_server_id').val('');
	le_db_server_name.val('');
	le_file_server_name.val('');
	$('#le_file_server_id').val('');
	$('.le-appl-server-name').text('');
	$('.le-appl-server-ip-port').text('');
	edit_id = null;
	group_application_server_name.focus();
}

function loadApplicationIpAndPort(application_id){
	var returnIP = null;
	$.each(application_server_list, function(key, value){
		if(application_id == value.machine_id){
			client_ids = value.console_cl_ids;
			returnIP = "IP: "+value.ip+", Port: "+value.port;
		}
	});

	return returnIP;
}

function loadClIDS(app_server_id){
	var CL_IDs = null;
	$.each(application_server_list, function(key, value){
		if(app_server_id == value.machine_id){
			CL_IDs = value.console_cl_ids;
		}
	});
	return CL_IDs;
}

function loadLEIDS(database_server_id){
	var LE_IDs = null;
	$.each(database_server_list, function(key, value){
		if(database_server_id == value.db_server_id){
			LE_IDs = value.console_le_ids;
		}
	});

	return LE_IDs;
}

function loadFileLEIDS(f_server_id){
	var LE_IDs = null;
	$.each(file_server_list, function(key, value){
		if(f_server_id == value.file_server_id){
			LE_IDs = value.console_le_ids;
		}
	});

	return LE_IDs;
}

function loadDatabaseIpAndPort(database_server_id){
	var returnIP = null;
	$.each(database_server_list, function(key, value){
		if(database_server_id == value.db_server_id){
			legal_entity_ids = value.console_le_ids;
			returnIP = "IP: "+value.database_server_ip+", Port: "+value.port;
		}
	});

	return returnIP;
}

function loadLEDatabaseIpAndPort(database_server_id){
	var returnIP = null;
	$.each(database_server_list, function(key, value){
		if(database_server_id == value.db_server_id){
			le_legal_entity_ids = value.console_le_ids;
			returnIP = "IP: "+value.database_server_ip+", Port: "+value.port;
		}
	});

	return returnIP;
}

function loadFileIpAndPort(file_server_id){
	var returnIP = null;
	$.each(file_server_list, function(key, value){
		if(file_server_id == value.file_server_id){
			f_legal_entity_ids = value.console_le_ids;
			returnIP = "IP: "+value.ip+", Port: "+value.port;
		}
	});

	return returnIP;
}

//callback for autocomplete success
function onAutoCompleteSuccess(value_element, id_element, val) {
    value_element.val(val[1]);
    id_element.val(val[0]);
    var current_id = id_element[0].id;
    if(current_id == 'application_id'){
    	$('.appl-grp-ip-port').text(loadApplicationIpAndPort(val[0]));
    	$('.le-appl-server-name').text(val[1]);
    	$('.le-appl-server-ip-port').text($('.appl-grp-ip-port').text());
    }
    else if(current_id == 'database_server_id'){
    	$('.db-grp-ip-port').text(loadDatabaseIpAndPort(val[0]));
    }
    else if(current_id == 'le_database_server_id'){
    	$('.db-le-ip-port').text(loadLEDatabaseIpAndPort(val[0]));
    }
    else if(current_id == 'le_file_server_id'){
    	$('.file-le-ip-port').text(loadFileIpAndPort(val[0]));
    }
    value_element.focus();
}

group_application_server_name.keyup(function(e){
    var text_val = $(this).val();
    commonAutoComplete(
        e, AC_group_application_server, group_application_server_id, text_val,
        application_server_list, "machine_name", "machine_id", function (val) {
            onAutoCompleteSuccess(group_application_server_name, group_application_server_id, val);
        }
    );
});

group_db_server_name.keyup(function(e){
    var text_val = $(this).val();
    // alert(group_db_server_id)
    commonAutoComplete(
        e, AC_group_db_server, group_db_server_id, text_val,
        database_server_list, "db_server_name", "db_server_id", function (val) {
            onAutoCompleteSuccess(group_db_server_name, group_db_server_id, val);
        }
    );
});

le_db_server_name.keyup(function(e){
    var text_val = $(this).val();
    // alert(le_database_server_id);
    commonAutoComplete(
        e, AC_le_db_server, le_db_server_id, text_val,
        database_server_list, "db_server_name", "db_server_id", function (val) {
            onAutoCompleteSuccess(le_db_server_name, le_db_server_id, val);
        }
    );
});

le_file_server_name.keyup(function(e){
    var text_val = $(this).val();
    commonAutoComplete(
        e, AC_le_file_server, le_file_server_id, text_val,
        file_server_list, "file_server_name", "file_server_id", function (val) {
            onAutoCompleteSuccess(le_file_server_name, le_file_server_id, val);
        }
    );
});

//initialization
$(function () {
	resetFields();
  initialize();
  $('#allocate-server-view').show();
  $('#allocate-server-add').hide();
});

PasswordSubmitButton.click(function() {
    validateAuthentication();
});

$(document).find('.js-filtertable').each(function(){
    $(this).filtertable().addFilter('.js-filter');
});
