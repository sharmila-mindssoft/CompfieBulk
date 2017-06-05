var CLIENTSERVERS = '';
var edit_id = null;
var FILTERED_LIST = '';

var client_server_name = '';
var ip = '';
var port = '';

var PasswordSubmitButton = $('#password-submit');
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
    console.log("type:"+type_of_form)
    showPage(type_of_form);
    clearMessage();
    clearFields();
    if(type_of_form == "list"){
        edit_id = null;
        function onSuccess(data) {
            CLIENTSERVERS = data.client_servers;
            FILTERED_LIST = CLIENTSERVERS
            loadClientServers();
            hideLoader();
        }
        function onFailure(error) {
            displayMessage(error);
        }
        displayLoader();
        mirror.getClientServerList(function (error, response) {
            if (error == null) {
                onSuccess(response);
            } else {
                onFailure(error);
                hideLoader();
            }
        });
    }else if(type_of_form == "edit"){
        loadEditForm();
    }else{
        edit_id = null;
    }
}

function showPage(type_of_form){
    if(type_of_form == "list"){
        $("#application-server-view").show();
        $("#application-server-add").hide();
    }else{
        $("#application-server-view").hide();
        $("#application-server-add").show();
    }
}

function clearFields(){
    $("#application-server-name").val("");
    $("#application-server-ip").val("");
    $("#application-server-port").val("");
    db_server_name = "";
    ip = "";
    port = "";
    $("#application-server-name").focus();
}

$(".btn-client-server-add").click(function(){
    initialize("add")
});

$(".btn-submit").on('click', function(e) {
    if(validateClientServer() == true){
        CurrentPassword.val('');
        Custombox.open({
            target: '#custom-modal',
            effect: 'contentscale',
            complete: function() {
                CurrentPassword.val('');
                CurrentPassword.focus();
                isAuthenticate = false;
            },
            close: function() {
                if (isAuthenticate) {
                    saveClientServer();
                }
            },
        });
    }
});

$(".btn-cancel").click(function(){
    initialize("list")
});

function loadClientServers(){
    $(".tbody-client-server-list").empty();
    var client_server_row = $("#templates .table-row");
    var sno = 0;
    $.each(FILTERED_LIST, function(key, value){
        ++ sno;
        var clone = client_server_row.clone();
        $(".sno", clone).text(sno);
        $(".client-server", clone).text(value.client_server_name);
        $(".ip", clone).text(value.ip);
        $(".port", clone).text(value.port);
        $(".no-of-clients", clone).text(value.no_of_clients);
        if(value.no_of_clients == 0 || value.no_of_clients == "0"){
            $(".edit-icon", clone).show();
            //edit icon
            $('.edit').attr('title', 'Click Here to Edit');
            $('.edit', clone).addClass('fa-pencil text-primary');
            $('.edit', clone).on('click', function () {
                edit_id = value.client_server_id;
                initialize("edit");
            });
        }
        else{
            $(".edit-icon", clone).hide();
        }
        $(".tbody-client-server-list").append(clone);
    });
}

function validateClientServer(){
    result = true;
    client_server_name = $("#application-server-name").val().trim();
    ip = $("#application-server-ip").val().trim();
    port = $("#application-server-port").val().trim();
    if(client_server_name == ''){
        displayMessage(message.client_server_name_required);
        result = false;
    }else if(validateMaxLength("application_server", client_server_name, "Application Server") == false) {
        result = false;
    }else if(ip == ''){
        displayMessage(message.ip_required);
        result = false;
    }else if(validateMaxLength("ip", ip, "IP") == false){
        result = false;
    }else if(ValidateIPAddress(ip) == false){
        displayMessage(message.not_a_valid_ip);
        result = false;
    }else if(port == ''){
        displayMessage(message.port_required);
        result = false;
    }else if(validateMaxLength("port", port, "Port") == false){
        result = false;
    }else if(parseInt(port) < 1 || parseInt(port) > 65535){
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
function saveClientServer(){
    clearMessage();
    function onSuccess(data) {
        if(edit_id != null){
            displaySuccessMessage(message.client_server_update_success);
        }
        else{
            cl_name = "\""+client_server_name+"\"";
            displaySuccessMessage(message.client_server_save_success.replace('client_server_name', cl_name));
        }
        initialize("list");
        hideLoader();
    }
    function onFailure(error) {
        if (error == "ClientServerNameAlreadyExists")
            displayMessage(message.ClientServerNameAlreadyExists);
        else
            displayMessage(error);
    }
    displayLoader();
    mirror.saveClientServer(
        edit_id, client_server_name, ip, parseInt(port),
        function (error, response) {
        console.log(error, response)
        if (error == null) {
            onSuccess(response);
        } else {
            onFailure(error);
            hideLoader();
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
            if(error == "InvalidPassword")
                displayMessage(message.invalid_password);
            else
                displayMessage(error);
            hideLoader();
        }
    });
}

function loadEditForm(){
    $.each(CLIENTSERVERS, function(key, value){
        if(edit_id == value.client_server_id){
            $("#application-server-name").val(value.client_server_name);
            $("#application-server-ip").val(value.ip);
            $("#application-server-port").val(value.port);
        }
    });
}


//initialization
$(function () {
  initialize("list");

  //key press for IP address
    $("#application-server-ip").on('keypress', function (e) {
        var k = e.which || e.keyCode;
        var ok = k >= 48 && k <= 57 || k == 46 || k ==8 || k == 9 || k == Key.LEFT ||
                k == Key.RIGHT;

      if (!ok){
          e.preventDefault();
      }
    });

    //key press for IP address
    $("#application-server-port").on('keypress', function (e) {
        var k = e.which || e.keyCode;
        var ok = k >= 48 && k <= 57 || k == 46 || k ==8 || k == 9 || k == Key.LEFT ||
                k == Key.RIGHT;

      if (!ok){
          e.preventDefault();
      }
    });
});

$("#application-server-ip").on('input', function (e) {
  this.value = isNumbersWithDot($(this));
});
$("#application-server-port").on('input', function (e) {
  this.value = isNumbers($(this));
});
$('#application-server-name').on('input', function (e) {
  this.value = isAlphanumeric($(this));
});
PasswordSubmitButton.click(function() {
    validateAuthentication();
});
$(document).find('.js-filtertable').each(function(){
    $(this).filtertable().addFilter('.js-filter');
});