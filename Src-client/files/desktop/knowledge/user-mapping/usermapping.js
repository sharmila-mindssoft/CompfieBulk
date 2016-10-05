var COUNTRIES = '';
var DOMAINS = '';
var CCMANAGERS = '';
var CCUSERS = '';
var TECHNOMANAGERS = '';
var MAPPINGS = '';

var ACTIVE_CC_USERS = [];
var ACTIVE_TECHNO_MANAGERS = [];
var selected_country = '';
var selected_domain = '';
var selected_cc_manager = '';

function initialize(type_of_form){
    showPage(type_of_form);
    clearMessage();
    if(type_of_form == "list"){
        function onSuccess(data) {
            COUNTRIES = data.countries;
            DOMAINS = data.domains;
            CCMANAGERS = data.cc_managers;
            CCUSERS = data.cc_users;
            TECHNOMANAGERS = data.techno_managers;
            MAPPINGSs = data.user_mappings;
        }
        function onFailure(error) {
            custom_alert(error);
        }
        mirror.getUserMappings(function (error, response) {
            if (error == null) {
                onSuccess(response);
            } else {
                onFailure(error);
            }
        });
    }else{
        
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

$(".btn-user-mapping-add").click(function(){
    initialize("add");
});

$(".btn-cancel").click(function(){
    initialize("list");
});

$("#show").click(function(){
    if(validateFilters()){
        $(".user-grid").show();
        $(".submit-button-container").show();
        ACTIVE_CC_USERS = [];
        ACTIVE_TECHNO_MANAGERS = [];
        loadCCUsers();
        loadTechnoManagers();
    }
});

$(".btn-submit").click(function(){
    saveUserMapping();
});

function validateFilters(){
    result = true;
    selected_country = parseInt($("#country").val());
    selected_country_text = $("#countryval").val();
    selected_domain = parseInt($("#domain").val());
    selected_domain_text = $("#domainval").val();
    selected_cc_manager = parseInt($("#user").val());
    selected_cc_manager_text = $("#userval").val();
    if(selected_country == '' || selected_country_text == ''){
        displayMessage(message.country_required);
        result = false;
    }else if(selected_domain == '' || selected_domain_text == ''){
        displayMessage(message.domain_required);
        result = false;
    }else if (selected_cc_manager == '' || selected_cc_manager_text == ''){
        displayMessage(message.cc_manager_required);
        result = false;
    }
    return result
}

//retrive country autocomplete value
function onCountrySuccess(val) {
  $('#countryval').val(val[1]);
  $('#country').val(val[0]);
}
//load country list in autocomplete text box  
$('#countryval').keyup(function (e) {
  function callback(val) {
    onCountrySuccess(val);
  }
  var textval = $(this).val();
  getCountryAutocomplete(e, textval, COUNTRIES, callback, flag = true);
});

//retrive domain autocomplete value
function onDomainSuccess(val) {
  $('#domainval').val(val[1]);
  $('#domain').val(val[0]);
}
//load country list in autocomplete text box  
$('#domainval').keyup(function (e) {
  function callback(val) {
    onDomainSuccess(val);
  }
  var textval = $(this).val();
  getDomainAutocomplete(e, textval, DOMAINS, callback, flag = true);
});

//retrive user autocomplete value
function onUserSuccess(val) {
  $('#userval').val(val[1]);
  $('#user').val(val[0]);
}
//load user list in autocomplete text box  
$('#userval').keyup(function (e) {
  function callback(val) {
    onUserSuccess(val);
  }
  var textval = $(this).val();
  selected_country = parseInt($("#country").val());
  selected_domain = parseInt($("#domain").val());
  FILTERED_CCMANAGER_LIST = [];
  $.each(CCMANAGERS, function(key, value){
        index_of_selected_country = value.country_ids.indexOf(selected_country);
        index_of_selected_domain = value.domain_ids.indexOf(selected_domain);
        if(index_of_selected_country != -1 && index_of_selected_domain != -1){
            FILTERED_CCMANAGER_LIST.push(value)
        }
  });
  getUserAutocomplete(e, textval, FILTERED_CCMANAGER_LIST, callback, flag = true);
});

function loadCCUsers(){
    $(".cc-user-list ul").empty();
    selected_country = parseInt($("#country").val());
    selected_domain = parseInt($("#domain").val());
    var cc_user_row = $("#templates .drop-down-option li");
    $.each(CCUSERS, function(key, value){
        index_of_selected_country = value.country_ids.indexOf(selected_country);
        index_of_selected_domain = value.domain_ids.indexOf(selected_domain);
        if(index_of_selected_country != -1 && index_of_selected_domain != -1){
            var clone = cc_user_row.clone();
            clone.text(value.employee_name);
            $(".cc-user-list ul").append(clone);
            clone.click(function(){
                activateCCUser(this, value.user_id);
            });
        }
    });
}

function loadTechnoManagers(){
    $(".techno-manager-list ul").empty();
    selected_country = parseInt($("#country").val());
    selected_domain = parseInt($("#domain").val());
    var techno_manager_row = $("#templates .drop-down-option li");
    $.each(TECHNOMANAGERS, function(key, value){
        index_of_selected_country = value.country_ids.indexOf(selected_country);
        index_of_selected_domain = value.domain_ids.indexOf(selected_domain);
        if(index_of_selected_country != -1 && index_of_selected_domain != -1){
            var clone = techno_manager_row.clone();
            clone.text(value.employee_name);
            $(".techno-manager-list ul").append(clone);
            clone.click(function(){
                activateTechnoManager(this, value.user_id);
            });
        }
    });
}

function activateCCUser(element, user_id){
    var chkstatus = $(element).attr('class');
    if (chkstatus == 'active') {
        $(element).removeClass('active');
        ACTIVE_CC_USERS.splice(index, 1);
    }else{
        $(element).addClass('active');
        index = ACTIVE_CC_USERS.indexOf(user_id)
        ACTIVE_CC_USERS.push(user_id);
    }
}

function activateTechnoManager(element, user_id){
    var chkstatus = $(element).attr('class');
    if (chkstatus == 'active'){
        $(element).removeClass('active');
        ACTIVE_TECHNO_MANAGERS.splice(index, 1);
    }else{
        $(element).addClass('active');
        index = ACTIVE_TECHNO_MANAGERS.indexOf(user_id)
        ACTIVE_TECHNO_MANAGERS.push(user_id);
    }
}

function validateUserMapping(){
    result = true;
    if(validateFilters() == true){
        if(ACTIVE_CC_USERS.length == 0){
            displayMessage(message.cc_user_required);
            result = false;
        }else if(ACTIVE_TECHNO_MANAGERS.length == 0){
            displayMessage(message.techno_manager_required);
            result = false;
        }
    }else{
        result = false;
    }
    return result;
}

function saveUserMapping(){
    if(validateUserMapping() == true){
        function onSuccess(data) {
            displayMessage(message.mapping_save_success);
            initialize("list");
        }
        function onFailure(error) {
            custom_alert(error);
        }
        mirror.saveUserMappings(selected_cc_manager,
            ACTIVE_TECHNO_MANAGERS, ACTIVE_CC_USERS,
            function (error, response) {
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