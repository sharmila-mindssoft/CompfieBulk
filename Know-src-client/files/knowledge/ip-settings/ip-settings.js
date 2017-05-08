var ViewIPSettings = $('#ip-settings-view');
var AddIPSettings = $('#ip-settings-add');

var btnAdd = $('.btn-add');
var btnCancel = $('.btn-cancel');
var btnSubmit = $('.btn-submit');

var GroupVal = $('#groupval');
var Group = $('#group');
var ACGroup = $('#ac-group');


var CLIENT_GROUPS = '';
var FORMS_LIST = '';
var IPS_LIST = '';
var GROUP_IPS_LIST = '';
var form_map = {};

function initialize(type_of_form){
    $(".form-view").hide();
    btnSubmit.hide();
    showPage(type_of_form);
    clearFields();
    if(type_of_form == "list"){
        function onSuccess(data) {
            FORMS_LIST = data.ip_setting_forms;
            CLIENT_GROUPS = data.client_groups;
            IPS_LIST = data.ips_list;
            loadList();
        }
        function onFailure(error) {
            displayMessage(error);
        }
        mirror.getIPSettingsList(function (error, response) {
            if (error == null) {
                onSuccess(response);
            } else {
                onFailure(error);
            }
        });
    }
}


function showPage(type_of_form){
    if(type_of_form == "list"){
        ViewIPSettings.show();
        AddIPSettings.hide();
    }else{
        ViewIPSettings.hide();
        AddIPSettings.show();
    }
}

function clearFields(){
    GroupVal.val("");
    Group.val("");
    form_map = {};
}

function generateMaps(){
    $.each(GROUP_IPS_LIST, function(key, value){
        form_map[value.form_id] = value.ip
    });
}

function callEditAPI(client_id){
    mirror.getGroupIPDetails(parseInt(client_id), function (error, response) {
        if (error == null) {
            GROUP_IPS_LIST = response.group_ips_list;
            generateMaps();
            loadForms();
        } else {
            displayMessage(error);
        }
    });
}

//retrive  autocomplete value
function onAutoCompleteSuccess(value_element, id_element, val) {
    value_element.val(val[1]);
    id_element.val(val[0]);
    value_element.focus();
    
    if(val[1] != ''){
        callEditAPI(val[0]);
    }
}

function pageControls() {

    btnAdd.click(function(){
        initialize("add")
    });

    btnSubmit.click(function(){
        saveIPSettings();
    });

    btnCancel.click(function(){
        initialize("list")
    });

    //load group list in autocomplete text box
    GroupVal.keyup(function(e) {
        $(".form-view").hide();
        btnSubmit.hide();

        var text_val = $(this).val();
        commonAutoComplete(
            e, ACGroup, Group, text_val,
            CLIENT_GROUPS, "group_name", "client_id",
            function(val) {
                onAutoCompleteSuccess(GroupVal, Group, val);
        });
    });
}

function loadEdit(cId, gName){
    showPage("edit");
    Group.val(cId)
    GroupVal.val(gName);
    callEditAPI(cId)
}

function deleteProcess(cId){
    mirror.deleteIPSettings(parseInt(cId), function (error, response) {
        if (error == null) {
            displaySuccessMessage(message.delete_ip_setting_success);
            initialize("list");
        } else {
            displayMessage(error);
        }
    });
}

function loadList(){
    $(".tbody-ip-settings-list").empty();
    var row_ = $("#templates .table-ip-settings-list .table-row");
    var sno = 0;
    $.each(IPS_LIST, function(key, value){
        ++ sno;
        var clone = row_.clone();
        $(".sno", clone).text(sno);
        $(".group-name", clone).text(value.group_name);
        $(".edit-icon", clone).click(function(){
            loadEdit(value.client_id, value.group_name)
        });
        $(".delete-icon", clone).click(function(){
            deleteProcess(value.client_id)
        });
        $(".tbody-ip-settings-list").append(clone);
        
    });

    if(sno == 0){
        var no_record_row = $("#templates .table-no-record tr");
        var clone = no_record_row.clone();
        $(".tbody-ip-settings-list").append(clone);
    }
}

function loadForms(){
    $(".form-view").show();
    btnSubmit.show();
    $(".tbody-form-list").empty();
    var g_row = $("#templates .table-form-list .table-row");
    var count = 0;
    $.each(FORMS_LIST, function(key, value){
        ++ count;
        var clone = g_row.clone();
        $(".form-name", clone).text(value.form_name);

        $('.ip-address', clone).attr('id', 'ip_'+value.form_id);
        $(".ip-address", clone).val(form_map[value.form_id]);

        $(".ip-address", clone).on('input', function(e) {
            this.value = isNumbers_Dot_Comma($(this));
        });
        $(".tbody-form-list").append(clone);  
        
    });
    if(count == 0){
        var clone = g_row.clone();
        $(".form-name", clone).text("No Forms Found");
        $(".ip-address", clone).hide();
        $(".tbody-form-list").append(clone);    
    }
}

function saveIPSettings(){
   ip_details = [];
   var valid_ip = true;
    $.each(FORMS_LIST, function(key, value){
        var form_id = parseInt(value.form_id);
        var ip = $("#ip_"+value.form_id).val();
        var g_id = parseInt(Group.val());

        if(ip != '' && ip != '0'){
            var returnVal = true;
            var ips = ip.split(",");
            for(var i=0; i<ips.length; i++){
                var split_ip = ips[i].split(".");
                if(ips[i].indexOf(".") < 0){
                    displayMessage(message.not_a_valid_ip);
                    returnVal = false;
                    valid_ip = false;
                }
                else if(split_ip.length < 4 || split_ip.length > 4){
                    displayMessage(message.not_a_valid_ip);
                    returnVal = false;
                    valid_ip = false;
                }
                else
                {   
                    for(var j=0;j<split_ip.length;j++){
                        if(parseInt(split_ip[j]) > 255){
                            displayMessage(message.not_a_valid_ip);
                            returnVal = false;
                            valid_ip = false;
                            break;
                        }
                    }
                }
            }
            if(returnVal){
                ip_details.push(
                    mirror.getIPSettingsDetails(
                        form_id, ip, g_id
                    )
                );
            }
        }
    });

    if(valid_ip == false){
        displayMessage(message.not_a_valid_ip);
        return false;
    }
    else if(ip_details.length > 0){
        function onSuccess(data) {
            displaySuccessMessage(message.save_ip_setting_success);
            initialize("list");
        }
        function onFailure(error) {
            displayMessage(error);
        }
        mirror.saveIPSettings(ip_details, function (error, response) {
            if (error == null) {
                onSuccess(response);
            } else {
                onFailure(error);
            }
        });
    }else{
        displayMessage(message.atleast_one_form_have_ip_address);
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
