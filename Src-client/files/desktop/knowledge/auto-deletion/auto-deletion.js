var LEGAL_ENTITIES = '';
var CLIENT_GROUPS = '';
var UNITS = '';
var edit_client_id = '';
var edit_legal_entity_id = '';

var client_map = {};
var entity_map = {};
var unit_map = {};

var deletion_details = [];

function initialize(type_of_form){
    showPage(type_of_form);
    clearMessage();
    if(type_of_form == "list"){
        edit_id = null;
        clearFields();
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
        if(edit_client_id != ''){
            $("#group").val(edit_client_id);
            loadLegalEntities();
        }
        if(edit_legal_entity_id != ''){
            $("#legal-entity").val(edit_legal_entity_id);
            loadUnits();
        }
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
    $("#group").empty();
    $("#legal-entity").empty();
    $(".numeric").val("");
    $(".tbody-unit-auto-deletion").empty();
    $(".tbody-auto-deletion").empty();
    edit_client_id = '';
    edit_legal_entity_id = '';
}

$(".btn-client-server-add").click(function(){
    initialize("add");
});

$(".btn-cancel").click(function(){
    initialize("list");
});

$(".btn-submit").click(function(){
    saveAutoDeletion();
});

$("#group").change(function(){
    loadLegalEntities();
});

$("#legal-entity").change(function(){
    loadUnits();
});

$('.numeric').keypress(function (e) {
    var regex = new RegExp("^[0-9|\b]+$");
    var str = String.fromCharCode(!e.charCode ? e.which : e.charCode);
    if (regex.test(str)) {
        $.each(UNITS, function(key, value){
            var old_value = $(".numeric").val();
            $(".deletion-year-"+value.unit_id).val(old_value+str);
        });
        return true;
    }
    e.preventDefault();
    return false;
});

function generateMaps(){
    $.each(CLIENT_GROUPS, function(key, value){
        client_map[value.client_id] = value.group_name
    });
    $.each(LEGAL_ENTITIES, function(key, value){
        entity_map[value.legal_entity_id] = value.legal_entity_name
    });
    $.each(UNITS, function(key, value){
        unit_map[value.unit_id] = value.unit_code + " - " + value.unit_name
    })
}

function loadList(){
    $(".tbody-auto-deletion").empty();
    var row = $("#templates .table-row");
    var sno = 0;
    $.each(LEGAL_ENTITIES, function(key, value){
        if(value.deletion_period != null){
            ++ sno;
            var clone = row.clone();
            $(".sno", clone).text(sno);
            $(".group", clone).text(client_map[value.client_id]);
            $(".le", clone).text(value.legal_entity_name);
            $(".no-of-units", clone).text(value.unit_count);
            $(".deletion-period", clone).text(value.deletion_period);   
            $(".edit-icon", clone).click(function(){
                edit_client_id = value.client_id;
                edit_legal_entity_id = value.legal_entity_id;
                initialize("edit");
            });
            $(".tbody-auto-deletion").append(clone);
        }
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

    selected_group = parseInt($("#group").val());
    $.each(LEGAL_ENTITIES, function(key, value){
        if(value.client_id == selected_group){
            var clone = le_option.clone();
            clone.text(value.legal_entity_name);
            clone.val(value.legal_entity_id);
            $("#legal-entity").append(clone);
        }
    });
}

function loadUnits(){
    $(".grid-table").show();
    $(".submit-button-container").show();

    var unit_row = $("#templates .unit_row tr");
    $(".tbody-unit-auto-deletion").empty();

    selected_entity = parseInt($("#legal-entity").val());
    var count = 0;
    $.each(UNITS, function(key, value){
        if(value.legal_entity_id == selected_entity){
            ++ count;
            var clone = unit_row.clone();
            $(".unit-name", clone).text(unit_map[value.unit_id]);
            var deletion_year_class = "deletion-year-"+value.unit_id;
            $(".deletion-year input", clone).addClass(deletion_year_class);
            $(".deletion-year", clone).keypress(function (e) {
                var regex = new RegExp("^[0-9|\b]+$");
                var str = String.fromCharCode(!e.charCode ? e.which : e.charCode);
                if (regex.test(str)) {
                    return true;
                }

                e.preventDefault();
                return false;
            });
            console.log("deletion year:"+value.deletion_year);
            $(".deletion-year input", clone).val(value.deletion_year);
            $(".tbody-unit-auto-deletion").append(clone);    
        }
    });
    if(count == 0){
        var clone = unit_row.clone();
        $(".unit-name", clone).text("No Units Found");
        $(".deletion-year", clone).hide();
        $(".tbody-auto-deletion").append(clone);    
    }
}

function getDeletionDetails(client_id, legal_entity_id, unit_id, deletion_year){
    return {
        "client_id": client_id,
        "legal_entity_id": legal_entity_id,
        "unit_id": unit_id,
        "deletion_year": deletion_year
    }
}

function validateAutoDeletion(){
    var result = true;
    deletion_details = [];
    $.each(UNITS, function(key, value){
        var unit_id = parseInt(value.unit_id);
        var deletion_year = parseInt($(".deletion-year-"+value.unit_id).val())
        if(deletion_year == '' || deletion_year == '0' || deletion_year == 'undefined'){
            displayMessage(message.deletion_year_required)
            result = false;
        }else{
            deletion_details.push(
                getDeletionDetails(
                    value.client_id, value.legal_entity_id,
                    unit_id, deletion_year
                )
            );
        }
    });
    return result
}

function saveAutoDeletion(){
    if(validateAutoDeletion() == true){
        function onSuccess(data) {
            displayMessage(message.save_auto_deletion_success);
            initialize("list");
        }
        function onFailure(error) {
            custom_alert(error);
        }
        mirror.saveAutoDeletion(deletion_details, function (error, response) {
            if (error == null) {
                onSuccess(response);
            } else {
                onFailure(error);
            }
        });
    }
}

//initialization
$(function () {
  initialize("list");
});