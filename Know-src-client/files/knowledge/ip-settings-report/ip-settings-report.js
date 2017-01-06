
var btnShow = $('.btn-show');
var btnExport = $('.btn-export');

var IPAddress = $('#ip-address');
var GroupVal = $('#groupval');
var Group = $('#group');
var ACGroup = $('#ac-group');


var CLIENT_GROUPS = '';
var FORMS_LIST = '';

var GROUP_IPS_LIST = '';
var form_map = {};

function initialize(){
    $(".details").hide();
    clearFields();
    
    function onSuccess(data) {
        FORMS_LIST = data.ip_setting_forms;
        CLIENT_GROUPS = data.client_groups;
        generateMaps();
        //loadList();
    }
    function onFailure(error) {
        displayMessage(error);
    }
    mirror.getIPSettingsReportFilter(function (error, response) {
        if (error == null) {
            onSuccess(response);
        } else {
            onFailure(error);
        }
    });
    
}

function clearFields(){
    GroupVal.val("");
    Group.val("");
    form_map = {};
}

function generateMaps(){
    $.each(FORMS_LIST, function(key, value){
        form_map[value.form_id] = value.form_name
    });
}

function getResult(){
    var g_id = null;
    var ip_address = null;
    var f_count = 1;
    var t_count = 100;
    if(Group.val() != ''){
        g_id = parseInt(Group.val());
    }
    if(IPAddress.val() != ''){
        ip_address = IPAddress.val();
    }
    mirror.getIPSettingsReport(g_id, ip_address, f_count, t_count, function (error, response) {
        if (error == null) {
            GROUP_IPS_LIST = response.group_ips_list;
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
}

function pageControls() {

    btnShow.click(function(){
        $('.details').show();
        $('#compliance_animation')
          .removeClass().addClass('bounceInLeft animated')
          .one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend', function(){
          $(this).removeClass();
        });

        getResult();
    });

    btnExport.click(function(){
        //saveIPSettings();
    });

    //load group list in autocomplete text box
    GroupVal.keyup(function(e) {
        var text_val = $(this).val();
        commonAutoComplete(
            e, ACGroup, Group, text_val,
            CLIENT_GROUPS, "group_name", "client_id",
            function(val) {
                onAutoCompleteSuccess(GroupVal, Group, val);
        });
    });
}


function loadForms(){
    
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
            this.value = isNumbers_Dot($(this));
        });
        $(".tbody-form-list").append(clone);  
        
    });
    if(count == 0){
        var clone = unit_row.clone();
        $(".form-name", clone).text("No Forms Found");
        $(".ip-address", clone).hide();
        $(".tbody-form-list").append(clone);    
    }
}

//initialization
$(function () {
  initialize("list");
  pageControls();
});
