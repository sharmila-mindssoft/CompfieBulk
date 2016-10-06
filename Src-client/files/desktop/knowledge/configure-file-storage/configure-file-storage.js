var CLIENT_LEGAL_ENTITIES = '';
var FILESTORAGES = '';
var CLIENT_SERVER_NAME_AND_ID = '';
var CLIENT_GROUPS = '';
var FILTERED_LIST = [];

var legal_entities_map = {};
var client_server_map = {};
var client_group_map = {};

var selected_client_group = '';
var selected_legal_entity = '';
var selected_client_server = '';

function initialize(type_of_form){
    showPage(type_of_form);
    clearMessage();
    if(type_of_form == "list"){
        edit_id = null;
        function onSuccess(data) {
            CLIENT_LEGAL_ENTITIES = data.client_legal_entities;
            FILESTORAGES = data.file_storages;
            CLIENT_SERVER_NAME_AND_ID = data.client_server_name_and_id;
            CLIENT_GROUPS = data.client_groups;
            generateMaps();
            FILTERED_LIST = FILESTORAGES;
            loadFileStorageList();
        }
        function onFailure(error) {
            custom_alert(error);
        }
        mirror.getFileStorage(function (error, response) {
            if (error == null) {
                onSuccess(response);
            } else {
                onFailure(error);
            }
        });
    }else{
        loadGroups();
        loadLegalEntities();
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
    saveFileStorage();
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
}

function loadFileStorageList(){
    $(".tbody-client-server-list").empty();
    var table_row = $("#templates .table-row");
    var sno = 0;
    $.each(FILTERED_LIST, function(key, value){
        ++ sno;
        var clone = table_row.clone();
        $(".sno", clone).text(sno);
        $(".group", clone).text(client_group_map[value.client_id]);
        $(".le", clone).text(legal_entities_map[value.legal_entity_id]);
        $(".client-server", clone).text(client_server_map[value.machine_id]);
        $(".tbody-client-server-list").append(clone);
        $(".edit-icon", clone).click(function(){
            initialize("edit");
            loadEditForm(
                value.client_id, value.legal_entity_id,
                value.machine_id
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

function validateFileStorage(){
    result = true;
    selected_client_group = $("#group").val();
    selected_legal_entity = $("#legal-entity").val();
    selected_client_server = $("#client-server").val();
    if(selected_client_group == '0'){
        displayMessage(message.client_required);
        result = false;
    }else if(selected_legal_entity == '0'){
        displayMessage(message.legalentity_required);
        result = false;
    }else if(selected_client_server == '0'){
        displayMessage(message.client_server_name_required);
        result = false;
    }
    return result
}

function saveFileStorage(){
    if(validateFileStorage() == true){
        function onSuccess(data) {
            displayMessage(message.file_storage_saved);
            initialize("list")
        }
        function onFailure(error) {
            custom_alert(error);
        }
        mirror.saveFileStorage(
            parseInt(selected_client_group), parseInt(selected_legal_entity),
            parseInt(selected_client_server), function (error, response) {
            if (error == null) {
                onSuccess(response);
            } else {
                onFailure(error);
            }
        });
    }
}

function loadEditForm(
    client_id, legal_entity_id, machine_id
){
    $("#group").val(client_id);
    $("#legal-entity").val(legal_entity_id);
    $("#client-server").val(machine_id);
}

$(".filter-text-box").keyup(function(){
    var client_group_filter = $('#search-group').val().toLowerCase();
    var legal_entity_filter = $('#search-legal-entity').val().toLowerCase();
    var client_server_filter = $('#search-client-server').val().toLowerCase();
    FILTERED_LIST = [];
    $.each(FILESTORAGES, function(key, value){
        var client_group_name = client_group_map[value.client_id].toLowerCase();
        var legal_entity_name = legal_entities_map[value.legal_entity_id].toLowerCase();
        var client_server_name = client_server_map[value.machine_id].toLowerCase();
        if (
            ~client_group_name.indexOf(client_group_filter) && 
            ~legal_entity_name.indexOf(legal_entity_filter) &&
            ~client_server_name.indexOf(client_server_filter) 
        ){
            FILTERED_LIST.push(value);
      }
    });
    loadFileStorageList();
});

//initialization
$(function () {
  initialize("list");
});