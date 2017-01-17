var allocate_server_list = [];
var application_server_list = [];
var database_server_list = [];
var file_server_list = [];
var edit_id = null;
var client_ids = null;
var client_id = null;
var legal_entity_id = null;
var legal_entity_ids = null;

var group_application_server_name = $('#group-application-server-name');
var group_db_server_name = $('#group-database-server-name');
var le_application_server_name = $('#le-application-server-name');
var le_db_server_name = $('#le-database-server-name');
var le_file_server_name = $('#le-file-server-name');

var btn_cancel = $('.btn-cancel');
var btn_submit = $('#submit');

function initialize(){
    clearMessage();
    edit_id = null;
    function onSuccess(data) {
    	allocate_server_list = data.client_dbs;
    	application_server_list = data.client_server_name_and_id;
    	database_server_list = data.db_server_name_and_id;
    	file_server_list = data.file_server_list;
    	loadAllocateDbEnvData();
    }
    function onFailure(error) {
        displayMessage(error);
    }
    mirror.getAllocatedDBEnv(function (error, response) {
    	console.log(error,response);
        if (error == null) {
            onSuccess(response);
        } else {
            onFailure(error);
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
	                loadCreateForm(
	                value.client_id, value.legal_entity_id
	            );
            });
        }
        else
        {
        	$('.edit', clone).show();
        	$('.btn-create', clone).hide();
        	$('.edit').attr('title', 'Click Here to Edit');
            $('.edit', clone).addClass('fa-pencil text-primary');
            edit_id = value.client_database_id;
            client_id = value.client_id
            legal_entity_id = value.legal_entity_id
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

btn_submit.click(function(){
	if(validateMandatory() == true){
		client_ids = checkClientIds(client_ids,client_id);
		legal_entity_ids = checkLEIds(legal_entity_ids, legal_entity_id);
		function onSuccess(data) {
            initialize();
            $('#allocate-server-view').show();
    		$('#allocate-server-add').hide();
        }
        function onFailure(error) {
            displayMessage(error);
        }
        console.log(edit_id,client_ids, legal_entity_ids);
    	mirror.saveDBEnv(edit_id, client_id, legal_entity_id, parseInt($('#application_id').val()),
    		parseInt($('#database_server_id').val()), parseInt($('#le_database_server_id').val()),
    		parseInt($('#le_file_server_id').val()), client_ids, legal_entity_ids, function (error, response) {
            if (error == null) {
        		displaySuccessMessage(message.allocated_db_env);
                onSuccess(response);
            } else {
                onFailure(error);
            }
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

	if(legal_entity_ids != null){
		splitLEIds = legal_entity_ids.split(",");
		for(var i=0;i<splitLEIds.length;i++){
			if(splitLEIds[i] == db_s_id){
				le_count++;
			}
		}
	}


	if(le_count == 0){
		if(legal_entity_ids != null)
			legal_entity_ids = legal_entity_ids + "," + db_s_id;
		else
			legal_entity_ids = db_s_id.toString();
	}
	return legal_entity_ids;
}

function validateMandatory(){
	var returnMandatory = true;
	if(group_application_server_name.val() == ''){
		displayMessage(message.client_server_name_required);
		returnMandatory = false;
	}
	else if(group_db_server_name.val() == ''){
		displayMessage(message.db_server_name_required);
		returnMandatory = false;
	}
	else if(le_db_server_name.val() == ''){
		displayMessage(message.le_db_server_name_required);
		returnMandatory = false;
	}
	else if(le_file_server_name.val() == ''){
		displayMessage(message.le_file_server_name_required);
		returnMandatory = false;
	}

	return returnMandatory;
}

function loadCreateForm(cl_id, legal_e_id) {
	// body...
	client_id = cl_id;
	legal_entity_id = legal_e_id;
	console.log(client_id, legal_entity_id)
	$('#allocate-server-add').show();
    $('#allocate-server-view').hide();
	resetFields();
	console.log(getFieldNames("group",client_id))
	$('.group-name').text(getFieldNames("group",client_id));
	$('.le-name').text(getFieldNames("le",legal_entity_id));
}

function loadEditForm(indexValues){
	//edit_id = 1;
	$('#allocate-server-add').show();
    $('#allocate-server-view').hide();
	$('.group-name').text(indexValues.group_name);
	$('.le-name').text(indexValues.legal_entity_name);
	group_application_server_name.val(indexValues.machine_name);
	$('#application_id').val(indexValues.machine_id);
	$('.appl-grp-ip-port').text(loadApplicationIpAndPort(indexValues.machine_id));
	group_db_server_name.val(indexValues.client_db_server_name);
	$('#database_server_id').val(indexValues.client_db_server_id);
	$('.db-grp-ip-port').text(loadDatabaseIpAndPort(indexValues.client_db_server_id));
	$('.le-appl-server-name').text(indexValues.machine_name);
	$('.le-appl-server-ip-port').text($('.appl-grp-ip-port').text());
	le_db_server_name.val(indexValues.db_server_name);
	$('#le_database_server_id').val(indexValues.db_server_id);
	$('.db-le-ip-port').text(loadDatabaseIpAndPort(indexValues.db_server_id));
	le_file_server_name.val(indexValues.file_server_name);
	$('#le_file_server_id').val(indexValues.file_server_id);
	$('.file-le-ip-port').text(loadFileIpAndPort(indexValues.file_server_id));
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
	group_db_server_name.val('');
	le_application_server_name.val('');
	le_db_server_name.val('');
	le_file_server_name.val('');
	edit_id = null;
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
			returnIP = "IP: "+value.database_server_ip+", Port: "+value.port;
		}
	});

	return returnIP;
}

function loadFileIpAndPort(file_server_id){
	var returnIP = null;
	$.each(file_server_list, function(key, value){
		if(file_server_id == value.file_server_id){
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
        e, $('#ac-appliaction-server'), $('#application_id'), text_val,
        application_server_list, "machine_name", "machine_id", function (val) {
            onAutoCompleteSuccess(group_application_server_name, $('#application_id'), val);
    });
});

group_db_server_name.keyup(function(e){
    var text_val = $(this).val();
    commonAutoComplete(
        e, $('#ac-grp-database-server'), $('#database_server_id'), text_val,
        database_server_list, "db_server_name", "db_server_id", function (val) {
            onAutoCompleteSuccess(group_db_server_name, $('#database_server_id'), val);
    });
});

le_db_server_name.keyup(function(e){
    var text_val = $(this).val();
    commonAutoComplete(
        e, $('#ac-le-database-server'), $('#le_database_server_id'), text_val,
        database_server_list, "db_server_name", "db_server_id", function (val) {
            onAutoCompleteSuccess(le_db_server_name, $('#le_database_server_id'), val);
    });
});

le_file_server_name.keyup(function(e){
    var text_val = $(this).val();
    commonAutoComplete(
        e, $('#ac-le-file-server'), $('#le_file_server_id'), text_val,
        file_server_list, "file_server_name", "file_server_id", function (val) {
            onAutoCompleteSuccess(le_file_server_name, $('#le_file_server_id'), val);
    });
});

//initialization
$(function () {
  initialize();
  $('#allocate-server-view').show();
  $('#allocate-server-add').hide();
});

$(document).find('.js-filtertable').each(function(){
    $(this).filtertable().addFilter('.js-filter');
});