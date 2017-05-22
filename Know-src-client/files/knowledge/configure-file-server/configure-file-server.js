var FileServerList = '';
var edit_id = null;

var file_server_name = $('#file-server-name');
var file_server_ip = $('#file-server-ip');
var file_server_port = $('#file-server-port');

var btnSubmit = $('.btn-submit');
var btnCancel = $('.btn-cancel');
var btnAdd = $('.btn-file-server-add');

var PasswordSubmitButton = $('#password-submit');
var Remark = $('#remark');
var RemarkView = $('.remark-view');
var CurrentPassword = $('#current-password');
var isAuthenticate;

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

btnSubmit.on('click', function(e) {
    if(validateFileServer() == true){
        CurrentPassword.val('');
        Remark.val('');
        RemarkView.hide();
        statusmsg = "Password Verification"
        confirm_alert(statusmsg, function(isConfirm) {
            if (isConfirm) {
                Custombox.open({
                    target: '#custom-modal',
                    effect: 'contentscale',
                    complete: function() {
                        CurrentPassword.focus();
                        isAuthenticate = false;
                    },
                    close: function() {
                        if (isAuthenticate) {
                            saveFileServer();
                        }
                    },
                });
                e.preventDefault();
            }
        });
    }
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
    if(file_server_name.val().trim() == ''){
        displayMessage(message.file_server_name_required);
        result = false;
    }else if(validateMaxLength("file_server", file_server_name.val(), "File Server") == false) {
        result = false;
    }else if(file_server_ip.val().trim() == ''){
        displayMessage(message.ip_required);
        result = false;
    }else if(validateMaxLength("ip", file_server_ip.val(), "IP") == false) {
        result = false;
    }else if(ValidateIPAddress(file_server_ip.val().trim()) == false){
        displayMessage(message.not_a_valid_ip);
        result = false;
    }else if(file_server_port.val().trim() == ''){
        displayMessage(message.port_required);
        result = false;
    }else if(validateMaxLength("port", file_server_port.val(), "Port") == false) {
        result = false;
    }else if(parseInt(file_server_port.val().trim()) < 1 || parseInt(file_server_port.val().trim()) > 65535){
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
        //displayMessage(message.not_a_valid_ip);
        returnVal = false;
    }
    else if(split_ip.length < 4 || split_ip.length > 4){
        //displayMessage(message.not_a_valid_ip);
        returnVal = false;
    }
    else
    {
        for(var i=0;i<split_ip.length;i++){
            if (i == 0){
                if (split_ip[i] == "0") {
                    returnVal = false;
                    break;
                }
            }
            else if(parseInt(split_ip[i]) > 255){
                //displayMessage(message.not_a_valid_ip);
                returnVal = false;
                break;
            }
        }
    }
    return returnVal;
}

function saveFileServer(){
    clearMessage();
    function onSuccess(data) {
        if(edit_id != '' && edit_id != null){
            cl_name = "\""+file_server_name.val().trim()+"\"";
            displaySuccessMessage(message.file_server_update_success.replace('file_name',cl_name));
        }
        else{
            cl_name = "\""+file_server_name.val().trim()+"\"";
            displaySuccessMessage(message.file_server_save_success.replace('file_name',cl_name));
        }
        initialize("list");
    }
    function onFailure(error) {
        displayMessage(error);
    }
    displayLoader();
    mirror.fileServerEntry(
        edit_id, file_server_name.val().trim(), file_server_ip.val().trim(), parseInt(file_server_port.val().trim()),
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
    mirror.verifyPassword(password, function(error, response) {
        if (error == null) {
            isAuthenticate = true;
            Custombox.close();
        } else {
            displayMessage(error);
        }
    });
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
file_server_ip.on('input', function (e) {
  this.value = isNumbersWithDot($(this));
});
file_server_port.on('input', function (e) {
  this.value = isNumbers($(this));
});
$('#file-server-name').on('input', function (e) {
  this.value = isAlphanumeric($(this));
});
PasswordSubmitButton.click(function() {
    validateAuthentication();
});
$(document).find('.js-filtertable').each(function(){
    $(this).filtertable().addFilter('.js-filter');
});