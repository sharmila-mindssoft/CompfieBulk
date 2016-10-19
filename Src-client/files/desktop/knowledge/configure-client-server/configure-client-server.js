var CLIENTSERVERS = '';
var edit_id = null;
var FILTERED_LIST = '';

var client_server_name = '';
var ip = '';
var port = '';

function initialize(type_of_form){
    showPage(type_of_form);
    clearMessage();
    clearFields();
    if(type_of_form == "list"){
        edit_id = null;
        function onSuccess(data) {
            CLIENTSERVERS = data.client_servers;
            FILTERED_LIST = CLIENTSERVERS
            loadClientServers();
        }
        function onFailure(error) {
            custom_alert(error);
        }
        mirror.getClientServerList(function (error, response) {
            if (error == null) {
                onSuccess(response);
            } else {
                onFailure(error);
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
        $("#view").show();
        $("#add").hide();
    }else{
        $("#view").hide();
        $("#add").show();
    }
}

function clearFields(){
    $("#client-server-name").val("");
    $("#ip").val("");
    $("#port").val("");
    db_server_name = "";
    ip = "";
    port = "";
}

$(".btn-client-server-add").click(function(){
    initialize("add")
});

$(".btn-submit").click(function(){
    saveClientServer();
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
        $(".edit-icon", clone).click(function(){
            edit_id = value.client_server_id;
            initialize("edit");
        });
        $(".tbody-client-server-list").append(clone);
    });
}

function validateClientServer(){
    result = true;
    client_server_name = $("#client-server-name").val();
    ip = $("#ip").val();
    port = $("#port").val();
    if(client_server_name == ''){
        displayMessage(message.client_server_name_required);
        result = false;
    }else if(validateLength(client_server_name, 50) == false){
        displayMessage(message.client_server_name_length_error);
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
    }else{
        return result
    }
}

function saveClientServer(){
    if(validateClientServer() == true){
        clearMessage();
        function onSuccess(data) {
            displayMessage(message.client_server_save_success);
            initialize("list");
        }
        function onFailure(error) {
            custom_alert(error);
        }
        mirror.saveClientServer(
            edit_id, client_server_name, ip, parseInt(port),
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
    $.each(CLIENTSERVERS, function(key, value){
        if(edit_id == value.client_server_id){
            $("#client-server-name").val(value.client_server_name);
            $("#ip").val(value.ip);
            $("#port").val(value.port);
        }
    });
}

$(".filter-text-box").keyup(function(){
    var server_name_filter = $('#search-client-server').val().toLowerCase();
    var ip_filter = $('#search-ip').val().toLowerCase();
    var port_filter = $('#search-port').val().toLowerCase();
    var no_of_clients_filter = $('#search-no-clients').val().toLowerCase();
    FILTERED_LIST = [];
    $.each(CLIENTSERVERS, function(key, value){
        var client_server_name = value.client_server_name.toLowerCase();
        var ip_add = value.ip.toLowerCase();
        var port = value.port+"";
        var no_of_clients = value.no_of_clients+"";
        if (
            ~client_server_name.indexOf(server_name_filter) && 
            ~ip_add.indexOf(ip_filter) &&
            ~port.indexOf(port_filter) && 
            ~no_of_clients.indexOf(no_of_clients_filter) 
        ){
            FILTERED_LIST.push(value);
      }
    });
    loadClientServers();
});

//initialization
$(function () {
  initialize("list");
});