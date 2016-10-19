var CLIENT_LEGAL_ENTITIES = '';
var CLIENT_DBS = '';
var CLIENT_SERVER_NAME_AND_ID = '';
var CLIENT_GROUPS = '';
var DB_SERVER_NAME_AND_ID = '';
var FILTERED_LIST = [];

var legal_entities_map = {};
var client_server_map = {};
var client_group_map = {};
var db_server_map = {};

var selected_client_group = '';
var selected_legal_entity = '';
var selected_db_server = '';
var selected_client_server = '';

function initialize(type_of_form){
    showPage(type_of_form);
    clearMessage();
    if(type_of_form == "list"){
        edit_id = null;
        function onSuccess(data) {
            CLIENT_LEGAL_ENTITIES = data.client_legal_entities;
            CLIENT_DBS = data.client_dbs;
            CLIENT_SERVER_NAME_AND_ID = data.client_server_name_and_id;
            CLIENT_GROUPS = data.client_groups;
            DB_SERVER_NAME_AND_ID = data.db_server_name_and_id;
            generateMaps();
            FILTERED_LIST = CLIENT_DBS;
            loadClientDatabaseList();
        }
        function onFailure(error) {
            custom_alert(error);
        }
        mirror.getAllocatedDBEnv(function (error, response) {
            if (error == null) {
                onSuccess(response);
            } else {
                onFailure(error);
            }
        });
    }else{
        loadGroups();
        loadLegalEntities();
        loadDatabaseServers();
        loadClientServers();
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

$(".btn-client-server-add").click(function(){
    initialize("add");
});

$(".btn-cancel").click(function(){
    initialize("list");
});

$(".btn-submit").click(function(){
    saveDBEnv();
});

function generateMaps(){
    $.each(CLIENT_LEGAL_ENTITIES, function(key, value){
        legal_entities_map[value.legal_entity_id] = value.legal_entity_name;
    });
    $.each(CLIENT_SERVER_NAME_AND_ID, function(key, value){
        client_server_map[value.machine_id] = value.machine_name;
    });
    $.each(CLIENT_GROUPS, function(key, value){
        client_group_map[value.client_id] = value.group_name;
    });
    $.each(DB_SERVER_NAME_AND_ID, function(key, value){
        db_server_map[value.ip] = value.db_server_name;
    });
}

function loadClientDatabaseList(){
    $(".tbody-client-server-list").empty();
    var table_row = $("#templates .table-row");
    var sno = 0;
    $.each(FILTERED_LIST, function(key, value){
        ++ sno;
        var clone = table_row.clone();
        $(".sno", clone).text(sno);
        $(".group", clone).text(client_group_map[value.client_id]);
        $(".le", clone).text(legal_entities_map[value.legal_entity_id]);
        $(".db-server", clone).text(db_server_map[value.database_server_ip]);
        $(".client-server", clone).text(client_server_map[value.machine_id]);
        $(".tbody-client-server-list").append(clone);
        $(".edit-icon", clone).click(function(){
            initialize("edit");
            loadEditForm(
                value.client_id, value.legal_entity_id,
                value.database_server_ip, value.machine_id
            );
        });
    });
}

function loadGroups(){
    var group_option = $("#templates .drop-down-option option");
    $("#group").empty();
    var select_clone = group_option.clone();
    select_clone.text("Select Group");
    select_clone.val("0");
    $("#group").append(select_clone);
    $.each(CLIENT_GROUPS, function(key, value){
        var clone = group_option.clone();
        clone.text(value.group_name);
        clone.val(value.client_id);
        $("#group").append(clone);
    });
}

function loadLegalEntities(){
    var le_option = $("#templates .drop-down-option option");
    $("#legal-entity").empty();
    var select_clone = le_option.clone();
    select_clone.text("Select Legal Entity");
    select_clone.val("0");
    $("#legal-entity").append(select_clone);
    $.each(CLIENT_LEGAL_ENTITIES, function(key, value){
        var clone = le_option.clone();
        clone.text(value.legal_entity_name);
        clone.val(value.legal_entity_id);
        $("#legal-entity").append(clone);
    });
}

function loadDatabaseServers(){
    var db_server_option = $("#templates .drop-down-option option");
    $("#db-server").empty();
    var select_clone = db_server_option.clone();
    select_clone.text("Select Database Server");
    select_clone.val("0");
    $("#db-server").append(select_clone);
    $.each(DB_SERVER_NAME_AND_ID, function(key, value){
        var clone = db_server_option.clone();
        clone.text(value.db_server_name);
        clone.val(value.ip);
        $("#db-server").append(clone);
    });
}
        
function loadClientServers(){
    var client_server_option = $("#templates .drop-down-option option");
    $("#client-server").empty();
    var select_clone = client_server_option.clone();
    select_clone.text("Select Client Server");
    select_clone.val("0");
    $("#client-server").append(select_clone);
    $.each(CLIENT_SERVER_NAME_AND_ID, function(key, value){
        var clone = client_server_option.clone();
        clone.text(value.machine_name);
        clone.val(value.machine_id);
        $("#client-server").append(clone);
    });
} 

function validateDBEnv(){
    result = true;
    selected_client_group = $("#group").val();
    selected_legal_entity = $("#legal-entity").val();
    selected_db_server = $("#db-server").val();
    selected_client_server = $("#client-server").val();
    if(selected_client_group == '0'){
        displayMessage(message.client_required);
        result = false;
    }else if(selected_legal_entity == '0'){
        displayMessage(message.legalentity_required);
        result = false;
    }else if(selected_db_server == '0'){
        displayMessage(message.db_server_name_required);
        result = false;
    }else if(selected_client_server == '0'){
        displayMessage(message.client_server_name_required);
        result = false;
    }
    return result
}

function saveDBEnv(){
    if(validateDBEnv() == true){
        function onSuccess(data) {
            displayMessage(message.allocated_db_env);
            initialize("list")
        }
        function onFailure(error) {
            custom_alert(error);
        }
        mirror.saveDBEnv(parseInt(selected_client_group), parseInt(selected_legal_entity),
            selected_db_server, parseInt(selected_client_server), function (error, response) {
            if (error == null) {
                onSuccess(response);
            } else {
                onFailure(error);
            }
        });
    }
}

function loadEditForm(
    client_id, legal_entity_id, database_server_ip, machine_id
){
    $("#group").val(client_id);
    $("#legal-entity").val(legal_entity_id);
    $("#db-server").val(database_server_ip);
    $("#client-server").val(machine_id);
}

$(".filter-text-box").keyup(function(){
    var client_group_filter = $('#search-group').val().toLowerCase();
    var legal_entity_filter = $('#search-legal-entity').val().toLowerCase();
    var db_server_filter = $('#search-db-server').val().toLowerCase();
    var client_server_filter = $('#search-client-server').val().toLowerCase();
    FILTERED_LIST = [];
    $.each(CLIENT_DBS, function(key, value){
        var client_group_name = client_group_map[value.client_id].toLowerCase();
        var legal_entity_name = legal_entities_map[value.legal_entity_id].toLowerCase();
        var db_server_name = db_server_map[value.database_server_ip].toLowerCase();
        var client_server_name = client_server_map[value.machine_id].toLowerCase();
        if (
            ~client_group_name.indexOf(client_group_filter) && 
            ~legal_entity_name.indexOf(legal_entity_filter) &&
            ~db_server_name.indexOf(db_server_filter) && 
            ~client_server_name.indexOf(client_server_filter) 
        ){
            FILTERED_LIST.push(value);
      }
    });
    loadClientDatabaseList();
});


//initialization
$(function () {
  initialize("list");
});