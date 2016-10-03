var LEGAL_ENTITIES = '';
var CLIENT_GROUPS = '';
var UNITS = '';

function initialize(type_of_form){
    showPage(type_of_form);
    clearMessage();
    if(type_of_form == "list"){
        edit_id = null;
        function onSuccess(data) {
            LEGAL_ENTITIES = data.auto_deletion_entities;
            CLIENT_GROUPS = data.client_groups;
            UNITS = data.auto_deletion_units;
            generateMaps();
            loadList();
        }
        function onFailure(error) {
            custom_alert(error);
        }
        mirror.getAutoDeletionList(function (error, response) {
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
}

function loadList(){
    
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


//initialization
$(function () {
  initialize("list");
});