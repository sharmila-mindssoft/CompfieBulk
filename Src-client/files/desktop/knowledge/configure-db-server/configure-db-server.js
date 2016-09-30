var DBSERVERS = '';
var edit_ip = '';
var FILTERED_LIST = '';

var db_server_name = '';
var ip = '';
var port = '';
var username = '';
var password = '';

function initialize(type_of_form){
    showPage(type_of_form);
    clearMessage();
    clearFields();
    if(type_of_form == "list"){
        function onSuccess(data) {
            DBSERVERS = data.db_servers;
            FILTERED_LIST = DBSERVERS
            loadDBServers();
        }
        function onFailure(error) {
            custom_alert(error);
        }
        mirror.getDbServerList(function (error, response) {
            if (error == null) {
                onSuccess(response);
            } else {
                onFailure(error);
            }
        });
    }else if(type_of_form == "edit"){
        loadEditForm();
    }
}

function showPage(type_of_form){
    if(type_of_form == "list"){
        $("#country-view").show();
        $("#country-add").hide();
    }else{
        $("#country-view").hide();
        $("#country-add").show();
    }
}

function clearFields(){
    $("#db-server-name").val("");
    $("#ip").val("");
    $("#port").val("");
    $("#username").val("");
    $("#pwd").val("");
    db_server_name = "";
    ip = "";
    port = "";
    username = "";
    password = "";
}

$(".btn-db-server-add").click(function(){
    initialize("add")
});

$(".btn-submit").click(function(){
    saveDBServer();
});

$(".btn-cancel").click(function(){
    initialize("list")
});

function loadDBServers(){
    $(".tbody-db-server-list").empty();
    var db_server_row = $("#templates .table-row");
    var sno = 0;
    $.each(FILTERED_LIST, function(key, value){
        ++ sno;
        var clone = db_server_row.clone();
        $(".sno", clone).text(sno);
        $(".db-server", clone).text(value.db_server_name);
        $(".ip", clone).text(value.ip);
        $(".port", clone).text(value.port);
        $(".username", clone).text(value.username);
        $(".no-of-clients", clone).text(value.no_of_clients);
        $(".edit-icon", clone).click(function(){
            edit_ip = value.ip;
            initialize("edit");
        });
        $(".tbody-db-server-list").append(clone);
    });
}

function validateDBServer(){
    result = true;
    db_server_name = $("#db-server-name").val();
    ip = $("#ip").val();
    port = $("#port").val();
    username = $("#username").val();
    password = $("#pwd").val();
    if(db_server_name == ''){
        displayMessage(message.db_server_name_required);
        result = false;
    }else if(validateLength(db_server_name, 50) == false){
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
    }else if(validateLength(username, 50) == false){
        displayMessage(message.username_length_error);
        result = false;
    }else if(password == ''){
        displayMessage(message.password_required)
        result = false;
    }else if(validateLength(password, 50) == false){
        displayMessage(message.password_length_error);
        result = false;
    }else{
        return result
    }
}

function saveDBServer(){
    if(validateDBServer() == true){
        clearMessage();
        function onSuccess(data) {
            displayMessage(message.db_server_save_success);
            initialize("list");
        }
        function onFailure(error) {
            custom_alert(error);
        }
        mirror.saveDBServer(
            db_server_name, ip, parseInt(port), username, password, 
            function (error, response) {
            if (error == null) {
                onSuccess(response);
            } else {
                onFailure(error);
            }
        });
    }
}

function loadEditForm(){
    $.each(DBSERVERS, function(key, value){
        if(edit_ip == value.ip){
            $("#db-server-name").val(value.db_server_name);
            $("#ip").val(value.ip);
            $("#port").val(value.port);
            $("#username").val(value.username);
            $("#pwd").val(value.password);
        }
    });
}

$(".filter-text-box").keyup(function(){
    var server_name_filter = $('#search-db-server').val().toLowerCase();
    var ip_filter = $('#search-ip').val().toLowerCase();
    var port_filter = $('#search-port').val().toLowerCase();
    var username_filter = $('#search-username').val().toLowerCase();
    var no_of_clients_filter = $('#search-no-clients').val().toLowerCase();
    FILTERED_LIST = [];
    $.each(DBSERVERS, function(key, value){
        var db_server_name = value.db_server_name.toLowerCase();
        var ip_add = value.ip.toLowerCase();
        var port = value.port+"";
        var username = value.username.toLowerCase();
        var no_of_clients = value.no_of_clients+"";
        if (
            ~db_server_name.indexOf(server_name_filter) && 
            ~ip_add.indexOf(ip_filter) &&
            ~port.indexOf(port_filter) && 
            ~username.indexOf(username_filter) && 
            ~no_of_clients.indexOf(no_of_clients_filter) 
        ){
            FILTERED_LIST.push(value);
      }
    });
    loadDBServers();
});

//initialization
$(function () {
  initialize("list");
});