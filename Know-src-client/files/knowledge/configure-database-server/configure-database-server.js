var DatabaseServers = '';
var edit_id = null;

var ViewDbServer = $('#config-db-view');
var AddDbServer = $('#config-db-add');

var btnDbServerAdd = $('.btn-db-server-add');
var btnDbServerCancel = $('.btn-cancel');
var btnDbServerSubmit = $('.btn-submit');

var db_svr_name = $('#db-server-name');
var db_server_ip = $('#db-server-ip');
var db_server_port = $('#db-server-port');
var db_server_uname = $('#db-server-username');
var db_server_pwd = $('#db-server-pwd');

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
            DatabaseServers = data.db_servers;
            loadDatabaseServers();
        }
        function onFailure(error) {
            displayMessage(error);
        }
        displayLoader();
        mirror.getDatabaseServerList(function (error, response) {
            console.log(error, response)
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
        ViewDbServer.show();
        AddDbServer.hide();
    }else{
        ViewDbServer.hide();
        AddDbServer.show();
    }
}

function clearFields(){
    db_svr_name.val("");
    db_server_ip.val("");
    db_server_port.val("");
    db_server_uname.val("");
    db_server_pwd.val("");
    db_svr_name.focus();
}

btnDbServerAdd.click(function(){
    initialize("add")
});

btnDbServerSubmit.click(function(){
    saveDBServer();
});

btnDbServerCancel.click(function(){
    initialize("list")
});


function loadDatabaseServers(){
    $(".tbody-db-server-list").empty();
    var db_server_row = $("#templates .table-row");
    var sno = 0;
    $.each(DatabaseServers, function(key, value){
        ++ sno;
        var clone = db_server_row.clone();
        $(".sno", clone).text(sno);
        $(".db-server", clone).text(value.db_server_name);
        $(".ip", clone).text(value.ip);
        $(".port", clone).text(value.port);
        $(".username", clone).text(value.username);
        $(".no-of-clients", clone).text(value.no_of_clients);
        if(value.no_of_clients == 0 || value.no_of_clients == "0"){
            console.log("Edit:"+value.db_server_id);
            $(".edit-icon", clone).show();
            //edit icon
            $('.edit').attr('title', 'Click Here to Edit');
            $('.edit', clone).addClass('fa-pencil text-primary');
            $('.edit', clone).on('click', function () {
                edit_id = value.db_server_id;
                initialize("edit");
            });
        }
        else{
            $(".edit-icon", clone).hide();
        }

        $(".tbody-db-server-list").append(clone);
    });
}

function validateDBServer(){
    result = true;
    db_s_name = db_svr_name.val();
    ip = db_server_ip.val();
    port = db_server_port.val();
    username = db_server_uname.val();
    password = db_server_pwd.val();
    if(db_s_name == ''){
        displayMessage(message.db_server_name_required);
        result = false;
    }else if(validateLength("db_server_name", db_s_name) == false){
        displayMessage(message.db_server_name_length_error);
        result = false;
    }else if(ip == ''){
        displayMessage(message.ip_required);
        result = false;
    }else if(ValidateIPaddress(ip) == false){
        displayMessage(message.not_a_valid_ip);
        result = false;
    }else if(port == ''){
        displayMessage(message.port_required);
        result = false;
    }else if(port.length < 4){
        displayMessage(message.invalid_port);
        result = false;
    }else if(username == ''){
        displayMessage(message.username_required)
        result = false;
    }else if(validateLength("username", username) == false){
        displayMessage(message.username_length_error);
        result = false;
    }else if(password == ''){
        displayMessage(message.password_required)
        result = false;
    }else if(validateLength("password", password) == false){
        displayMessage(message.password_length_error);
        result = false;
    }
    /*else if(validatePassword(password) == false){
        displayMessage(message.invalid_password);
        result = false;
    }*/
    else
    {
        return result
    }
}

function validatePassword(pwd){
    var returnResult = true;
    var special_char_count = 0;
    var special_chars = "!@#$%";
    for(var i=0;i<pwd.length;i++){
        if(special_chars.indexOf(pwd[i]) > 0){
            special_char_count++;
        }
    }
    console.log(special_char_count)
    if(special_char_count == 0 || special_char_count > 1){
        returnResult = false;
    }

    return returnResult;
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

function saveDBServer(){
    db_server_name = db_svr_name.val();
    ip = db_server_ip.val();
    port = db_server_port.val();
    username = db_server_uname.val();
    password = db_server_pwd.val();
    if(validateDBServer() == true){
        clearMessage();
        function onSuccess(data) {
            console.log("edit_id:"+edit_id)
            if(edit_id == null){
                displaySuccessMessage(message.db_server_save_success);
            }else{
                displaySuccessMessage(message.db_server_update_success);
                edit_id = null;
            }
            initialize("list");
        }
        function onFailure(error) {
            displayMessage(error);
        }
        displayLoader();
        mirror.saveDBServer(
            edit_id, db_server_name, ip, parseInt(port), username, password,
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
    $.each(DatabaseServers, function(key, value){
        if(edit_id == value.db_server_id){
            db_svr_name.val(value.db_server_name);
            db_server_ip.val(value.ip);
            db_server_port.val(value.port);
            db_server_uname.val(value.username);
            db_server_pwd.val(value.password);
        }
    });
}

//initialization
$(function () {
  initialize("list");

  //key press for IP address
    db_server_ip.on('keypress', function (e) {
        var k = e.which || e.keyCode;
        var ok = k >= 48 && k <= 57 || k == 46 || k ==8 || k == 9 || k == Key.LEFT ||
                k == Key.RIGHT || k != 37;

      if (!ok){
          e.preventDefault();
      }
    });

    //key press for IP address
    db_server_port.on('keypress', function (e) {
        var k = e.which || e.keyCode;
        var ok = k >= 48 && k <= 57 || k == 46 || k ==8 || k == 9 || k == Key.LEFT ||
                k == Key.RIGHT;

      if (!ok){
          e.preventDefault();
      }
    });

});

db_server_ip.on('input', function (e) {
  this.value = isNumbersWithDot($(this));
});
db_server_port.on('input', function (e) {
  this.value = isNumbers($(this));
});
$('#db-server-name').on('input', function (e) {
  this.value = isAlphanumeric($(this));
});
$(document).find('.js-filtertable').each(function(){
    $(this).filtertable().addFilter('.js-filter');
});
