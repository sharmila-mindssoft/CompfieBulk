var ViewAutoDeletion = $('#auto-deletion-view');
var AddAutoDeletion = $('#auto-deletion-add');

var btnAdd = $('.btn-add');
var btnCancel = $('.btn-cancel');
var btnSubmit = $('.btn-submit');

var GroupVal = $('#groupval');
var Group = $('#group');
var ACGroup = $('#ac-group');

var LegalEntityVal = $('#legalentityval');
var LegalEntity = $('#legalentity');
var ACLegalEntity = $('#ac-legalentity');

var deletion_period = $('#deletion-period');

var LEGAL_ENTITIES = '';
var CLIENT_GROUPS = '';
var UNITS = '';
var FILTERED_LIST = [];

var client_map = {};

var PasswordSubmitButton = $('#password-submit');
var CurrentPassword = $('#current-password');
var isAuthenticate;

var isEdit = false;

/*var entity_map = {};
var unit_map = {};
*/
function initialize(type_of_form){
    $(".tbody-unit-list").empty();
    btnSubmit.hide();
    $(".unit-view").hide();

    showPage(type_of_form);
    clearFields();
    if(type_of_form == "list"){
        function onSuccess(data) {
            LEGAL_ENTITIES = data.auto_deletion_entities;
            CLIENT_GROUPS = data.client_groups;
            UNITS = data.auto_deletion_units;
            FILTERED_LIST = LEGAL_ENTITIES;
            generateMaps();
            loadList();
        }
        function onFailure(error) {
            displayMessage(error);
        }
        mirror.getAutoDeletionList(function (error, response) {
            if (error == null) {
                onSuccess(response);
            } else {
                onFailure(error);
            }
        });
    }
}

function generateMaps(){
    $.each(CLIENT_GROUPS, function(key, value){
        client_map[value.client_id] = value.group_name
    });
}

function showPage(type_of_form){
    if(type_of_form == "list"){
        ViewAutoDeletion.show();
        AddAutoDeletion.hide();
    }else{
        ViewAutoDeletion.hide();
        AddAutoDeletion.show();
    }
}

function clearFields(){
    GroupVal.val("");
    Group.val("");
    LegalEntityVal.val("");
    LegalEntity.val("");
    deletion_period.val("");
    isEdit = false;
}

//retrive  autocomplete value
function onAutoCompleteSuccess(value_element, id_element, val) {
    value_element.val(val[1]);
    id_element.val(val[0]);
    value_element.focus();
    var current_id = id_element[0].id;
    if (current_id == 'group') {
        LegalEntityVal.val('');
        LegalEntity.val('');
    }else{
        loadUnits();
    }
}

function pageControls() {

    btnAdd.click(function(){
        initialize("add")
    });

    btnSubmit.click(function(){
        saveAutoDeletion();
    });

    btnCancel.click(function(){
        initialize("list")
    });

    //load group list in autocomplete text box
    GroupVal.keyup(function(e) {
        $(".unit-view").hide();
        btnSubmit.hide();

        var text_val = $(this).val();
        commonAutoComplete(
            e, ACGroup, Group, text_val,
            CLIENT_GROUPS, "group_name", "client_id",
            function(val) {
                onAutoCompleteSuccess(GroupVal, Group, val);
        });
    });

    //load legalentity list in autocomplete text box
    LegalEntityVal.keyup(function(e) {
        $(".unit-view").hide();
        btnSubmit.hide();

        if (Group.val() != '') {
            var condition_fields = ["client_id", "is_closed"];
            var condition_values = [Group.val(), false];

            var text_val = $(this).val();
            commonAutoComplete(
                e, ACLegalEntity, LegalEntity, text_val,
                LEGAL_ENTITIES, "legal_entity_name", "legal_entity_id",
                function(val) {
                    onAutoCompleteSuccess(LegalEntityVal, LegalEntity, val);
                }, condition_fields, condition_values);
        }
    });

    deletion_period.on('input', function(e) {
        this.value = isNumbers($(this));
        $('.unit-deletion-period').val(this.value)
    });

    PasswordSubmitButton.click(function() {
        validateAuthentication();
    });

}

function loadEdit(cId, leId, dPeriod, leName, gName){
    showPage("edit");
    Group.val(cId)
    GroupVal.val(gName);
    LegalEntity.val(leId);
    LegalEntityVal.val(leName);
    deletion_period.val(dPeriod);
    isEdit = true;
    loadUnits();
}

function loadList(){
    $(".tbody-auto-deletion-list").empty();
    var row_ = $("#templates .table-auto-deletion-list .table-row");
    var sno = 0;
    $.each(FILTERED_LIST, function(key, value){
        if(value.deletion_period != null){
            ++ sno;
            var clone = row_.clone();
            $(".sno", clone).text(sno);
            $(".group-name", clone).text(client_map[value.client_id]);
            $(".le-name", clone).text(value.legal_entity_name);
            $(".unit-count", clone).text(value.unit_count);
            $(".deletion-period", clone).text(value.deletion_period);   
            $(".edit-icon", clone).click(function(){
                loadEdit(value.client_id, value.legal_entity_id, value.deletion_period, 
                    value.legal_entity_name, client_map[value.client_id])
            });

            $(".tbody-auto-deletion-list").append(clone);
        }
    });

    if (sno == 0) {
        var no_record_row = $("#templates .table-no-record tr");
        var no_clone = no_record_row.clone();
        $(".tbody-auto-deletion-list").append(no_clone);
    }
}

function loadUnits(){
    $(".unit-view").show();
    btnSubmit.show();

    $(".tbody-unit-list").empty();
    var unit_row = $("#templates .table-unit-list .table-row");
    
    selected_entity = parseInt(LegalEntity.val());
    var count = 0;
    $.each(UNITS, function(key, value){
        if(value.legal_entity_id == selected_entity){
            ++ count;
            var clone = unit_row.clone();
            $(".unit-name", clone).text(value.unit_code + '-' + value.unit_name);
            $(".unit-address", clone).attr('title', value.address);

            var d_p = '';
            if(value.deletion_period != null){
                d_p = value.deletion_period;
            }
            $('.unit-deletion-period', clone).val(d_p);
            $('.unit-deletion-period', clone).attr('id', 'dp_'+value.unit_id);
            
            $(".unit-deletion-period", clone).on('input', function(e) {
                this.value = isNumbers($(this));
            });
            $(".tbody-unit-list").append(clone);  
        }
    });

    if(count == 0){
        var clone = unit_row.clone();
        $(".unit-name", clone).text("No Units Found");
        $(".unit-deletion-period", clone).hide();
        $(".tbody-unit-list").append(clone); 
        btnSubmit.hide();   
    }
}

function validate(){    
    var result = true;
    deletion_details = [];
    $.each(UNITS, function(key, value){
        if(value.legal_entity_id == parseInt(LegalEntity.val())){
            var unit_id = parseInt(value.unit_id);
            if($("#dp_"+value.unit_id).val() == ''){
                displayMessage(message.deletion_period_required)
                result = false;
                return false;
            }
            else if($("#dp_"+value.unit_id).val() == '0' || $("#dp_"+value.unit_id).val() == '00'){
                displayMessage(message.invalid_deletion_period)
                result = false;
                return false;
            }
            else{
                var deletion_period = parseInt($("#dp_"+value.unit_id).val());
                deletion_details.push(
                    mirror.getDeletionDetails(
                        value.client_id, value.legal_entity_id,
                        unit_id, deletion_period
                    )
                );
            }
        }
    });
    return result;
}

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
            if (error == 'InvalidPassword') {
                displayMessage(message.invalid_password);
            }else{
                displayMessage(error);
            }
        }
    });
}

function saveAutoDeletion(){
   
    if(validate() == true){

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
                    function onSuccess(data) {
                        if(isEdit){
                            displaySuccessMessage(message.auto_deletion_update_success);
                        }else{
                            displaySuccessMessage(message.auto_deletion_create_success);
                        }
                        initialize("list");
                    }
                    function onFailure(error) {
                        displayMessage(error);
                    }
                    mirror.saveAutoDeletion(deletion_details, function (error, response) {
                        if (error == null) {
                            onSuccess(response);
                        } else {
                            onFailure(error);
                        }
                    });
                }
            },
        });
    }
}

//initialization
$(function () {
  initialize("list");
  pageControls();
});

$(document).find('.js-filtertable').each(function(){
    $(this).filtertable().addFilter('.js-filter');
});
