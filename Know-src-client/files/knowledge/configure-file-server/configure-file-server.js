var FileServerList = '';
var edit_id = null;

var file_server_name = $('#file-server-name');
var file_server_ip = $('#file-server-ip');
var file_server_port = $('#file-server-port');

var btnSubmit = $('.btn-submit');
var btnCancel = $('.btn-cancel');
var btnAdd = $('.btn-file-server-add');

var Key = {
  LEFT:   37,
  UP:     38,
  RIGHT:  39,
  DOWN:   40
};

function displayLoader() {
  $('.loading-indicator-spin').show();
}
function hideLoader() {
  $('.loading-indicator-spin').hide();
}

function initialize(type_of_form){
	showPage(type_of_form);
  clearFields();
	if(type_of_form == "list"){
    edit_id = null;
    function onSuccess(data) {
        FileServerList = data.file_servers;
        loadFileServers();
    }
    function onFailure(error) {
        displayMessage(error);
    }
    displayLoader();
    mirror.getFileServerList(function (error, response) {
        if (error == null) {
            hideLoader();
            onSuccess(response);
        } else {
            hideLoader();
            onFailure(error);
        }
    });
	}
	else if(type_of_form == "edit"){
        loadEditForm();
	}else{
        edit_id = null;
    }
}

function showPage(type_of_form){
    if(type_of_form == "list"){
        $("#file-server-view").show();
        $("#file-server-add").hide();
    }else{
        $("#file-server-view").hide();
        $("#file-server-add").show();
    }
}

function clearFields(){
    file_server_name.val("");
    file_server_ip.val("");
    file_server_port.val("");
    file_server_name.focus();
}

btnAdd.click(function(){
    initialize("add")
});

btnSubmit.click(function(){
    saveFileServer();
});

btnCancel.click(function(){
    initialize("list")
});

function loadFileServers(){
    $(".tbody-configure-file-server-list").empty();
    var file_server_row = $("#templates .table-row");
    var sno = 0;
    $.each(FileServerList, function(key, value){
        ++ sno;
        var clone = file_server_row.clone();
        $(".sno", clone).text(sno);
        $(".file-server-name", clone).text(value.file_server_name);
        $(".ip", clone).text(value.ip);
        $(".port", clone).text(value.port);
        $(".no-of-clients", clone).text(value.no_of_clients);
        if(value.no_of_clients == 0 || value.no_of_clients == "0"){
            console.log("Edit:"+value.file_server_id);
            $(".edit-icon", clone).show();
            //edit icon
            $('.edit').attr('title', 'Click Here to Edit');
            $('.edit', clone).addClass('fa-pencil text-primary');
            $('.edit', clone).on('click', function () {
                edit_id = value.file_server_id;
                initialize("edit");
            });
        }
        else{
            $(".edit-icon", clone).hide();
        }
        $(".tbody-configure-file-server-list").append(clone);
    });
}

function validateFileServer(){
    result = true;
    if(file_server_name.val() == ''){
        displayMessage(message.file_server_name_required);
        result = false;
    }else if(validateLength(file_server_name.val(), 50) == false){
        displayMessage(message.file_server_name_length_error);
        result = false;
    }else if(file_server_ip.val() == ''){
        displayMessage(message.ip_required);
        result = false;
    }else if(ValidateIPAddress(file_server_ip.val()) == false){
        displayMessage(message.not_a_valid_ip);
        result = false;
    }else if(file_server_port.val() == ''){
        displayMessage(message.port_required);
        result = false;
    }else if(file_server_port.val().length < 4){
        displayMessage(message.invalid_port);
        result = false;
    }else{
        return result
    }
}

function ValidateIPAddress(IPAddress){
    var ip = IPAddress;
    var split_ip = ip.split(".");
    var returnVal = true;
    if(ip.indexOf(".") < 0){
        displayMessage(message.not_a_valid_ip);
        returnVal = false;
    }
    else if(split_ip.length < 4 || split_ip.length > 4){
        displayMessage(message.not_a_valid_ip);
        returnVal = false;
    }
    else
    {
        for(var i=0;i<split_ip.length;i++){
            if(parseInt(split_ip[i]) > 255){
                displayMessage(message.not_a_valid_ip);
                returnVal = false;
                break;
            }
        }
    }
    return returnVal;
}

function saveFileServer(){
    if(validateFileServer() == true){
        clearMessage();
        function onSuccess(data) {
            if(edit_id != '' && edit_id != null){
                displaySuccessMessage(message.file_server_update_success);
            }
            else{
                displaySuccessMessage(message.file_server_save_success);
            }
            initialize("list");
        }
        function onFailure(error) {
            displayMessage(error);
        }
        displayLoader();
        mirror.fileServerEntry(
            edit_id, file_server_name.val(), file_server_ip.val(), parseInt(file_server_port.val()),
            function (error, response) {
            if (error == null) {
                hideLoader();
                onSuccess(response);
            } else {
                hideLoader();
                onFailure(error);
            }
        });
    }
}

function loadEditForm(){
    $.each(FileServerList, function(key, value){
        if(edit_id == value.file_server_id){
            console.log("matched")
            file_server_name.val(value.file_server_name);
            file_server_ip.val(value.ip);
            file_server_port.val(value.port);
        }
    });
}

//initialization
$(function () {
  initialize("list");

  //key press for IP address
    file_server_ip.on('keypress', function (e) {
        var k = e.which || e.keyCode;
        var ok = k >= 48 && k <= 57 || k == 46 || k ==8 || k == 9 || k == Key.LEFT ||
                k == Key.RIGHT;

      if (!ok){
          e.preventDefault();
      }
    });

    //key press for IP address
    file_server_port.on('keypress', function (e) {
        var k = e.which || e.keyCode;
        var ok = k >= 48 && k <= 57 || k == 46 || k ==8 || k == 9 || k == Key.LEFT ||
                k == Key.RIGHT;

      if (!ok){
          e.preventDefault();
      }
    });
});

$(document).find('.js-filtertable').each(function(){
    $(this).filtertable().addFilter('.js-filter');
});