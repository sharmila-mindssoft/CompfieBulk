var le_count = 0;
var edit_id = null;
var organization_details = {}
var country_domain_id_map = {}
var selected_textbox = '';
var logoFile = [];
var industry_id_map = {}

var COUNTRIES = '';
var DOMAINS = '';
var INDUSTRIES = '';
var USERS = '';
var GROUPNAME = '';
var USERNAME = '';
var BUSSINESSGROUPS = '';
var LEGALENTITIES = '';
var DATECONFIGURATIONS = '';


function initialize(type_of_initialization){
  showPage(type_of_initialization);
  if(type_of_initialization == "list"){
        function onSuccess(data) {
            GROUPS = data.groups;
            loadGroups();
        }
        function onFailure(error) {
            displayMessage(error);
        }
        mirror.getClientGroups(function (error, response) {
            if (error == null) {
                onSuccess(response);
            }else {
                onFailure(error);
            }
        });
  }else if(type_of_initialization == "add"){
        function onSuccess(data) {
            COUNTRIES = data.countries;
            DOMAINS = data.domains;
            INDUSTRIES = data.industries;
            USERS = data.users;
            $.each(INDUSTRIES, function(key, value){
                industry_id_map[value.industry_name] = parseInt(value.industry_id)
            });
            addClient();
        }
        function onFailure(error) {
            displayMessage(error);
        }
        mirror.getClientGroupFormData(function (error, response) {
            if (error == null) {
                onSuccess(response);
            }else {
                onFailure(error);
            }
        });

  }else if(type_of_initialization == "edit"){
        function onSuccess(data) {
            COUNTRIES = data.countries;
            DOMAINS = data.domains;
            INDUSTRIES = data.industries;
            USERS = data.users;
            BUSSINESSGROUPS = data.business_groups;
            $.each(INDUSTRIES, function(key, value){
                industry_id_map[value.industry_name] = parseInt(value.industry_id)
            });
            GROUPNAME = data.group_name
            USERNAME = data.user_name
            LEGALENTITIES = data.legal_entities
            DATECONFIGURATIONS = data.date_configurations
            editClient();
        }
        function onFailure(error) {
            displayMessage(error);
        }
        mirror.getEditClientGroupFormData(edit_id, function (error, response) {
            if (error == null) {
                onSuccess(response);
            }else {
                onFailure(error);
            }
        });
  }else{
    // Invalid initialization Do nothing
  }
}

function showPage(type_of_initialization){
    le_count = 0;
    organization_details = {};
    logoFile = [];
    country_domain_id_map = {};
    clearMessage();
    if(type_of_initialization == "list"){
        $('.le-body').empty();
        $("#group-text").val("");
        $("#username").val("");
        $("#username").attr("readonly", false);
        $('.tbody-dateconfiguration-list').empty();
        $("#clientgroup-view").show();
        $("#clientgroup-add").hide();
    }else{
        if(type_of_initialization == "add"){
            $("#username").attr("readonly", false);
        }
        $("#clientgroup-view").hide();
        $("#clientgroup-add").show();
    }
}

/*
    Handling List
*/

function loadGroups(){
    $('.tbody-clientgroup-list').find('tr').remove();
    var sno = 0;
    $.each(GROUPS, function (key, value) {
        var clientId = value.group_id;
        var isActive = value.is_active;
        var passStatus = null;
        var classValue = null;
        if (isActive == true) {
            passStatus = false;
            classValue = 'active-icon';
        } else {
          passStatus = true;
          classValue = 'inactive-icon';
        }
        var tableRow = $('#templates .table-clientgroup-list .table-row');
        var clone = tableRow.clone();
        sno = sno + 1;
        $('.sno', clone).text(sno);
        $('.country_names', clone).text(value.country_names);
        $('.group_name', clone).text(value.group_name);
        $('.no_of_entities', clone).text(value.no_of_legal_entities);
        $('.edit-icon', clone).attr('title', 'Edit');
        $('.edit-icon', clone).attr('id', clientId);
        $('.edit-icon', clone).on('click', function () {
            edit_id = parseInt($(this).attr('id'));
            initialize("edit");
        });
        $('.status', clone).addClass(classValue);
        $('.active-icon').attr('title', 'Deactivate');
        $('.inactive-icon').attr('title', 'Activate');
        $('.status', clone).attr('id', clientId);
        $('.status', clone).on('click', function () {
            changeClientStatus(passStatus, $(this).attr("id"));
        });
        $('.tbody-clientgroup-list').append(clone);
    });   
}
/*
  Handling Button Clicks
*/
$(".btn-clientgroup-add").click(function(){
    initialize("add");
});
$(".add-business-group").click(function(){
    addOrSelectBusinessGroup("add");
});
$(".cancel-add-business-group").click(function(){
    addOrSelectBusinessGroup("cancel");
});
$(".cancel-add-business-group").click(function(){
    addOrSelectBusinessGroup("cancel");
});
$(".add-le").click(function(){
    addClient();
});
$(".save").click(function(){
    saveClient();
});
$(".cancel").click(function(){
    initialize("list");
});
$(".org-submit").click(function(){
    saveOrganization();
});
$(".org-cancel, .close").click(function(){
    closePopup();
});
$(".add-organization").click(function(){
    addOrganization();
});
/*
    Handling Save or Update
*/

function saveOrganization(){
    org_count = $("#o-cnt").val();
    le_cnt = $("#le-cnt").val();
    d_cnt = $("#d-cnt").val(); 
    for(var i=1; i<=org_count; i++){
        var org_selected_class = "org-selected-"+le_cnt+"-"+d_cnt+"-"+i
        selected_org = $("."+org_selected_class).val();
        no_of_units_class = "no-of-units-"+le_cnt+"-"+d_cnt+"-"+i
        no_of_units = $("." + no_of_units_class).val();
        if(selected_org == '' || selected_org == null){
            displayMessage(message.organization_required);
            organization_details = {};
            break;
        }else if(no_of_units == '' || no_of_units == 0 || no_of_units == '0' ){
            displayMessage(message.no_of_units_required);
            organization_details = {};
            break;
        }else{
            if(!(le_cnt in organization_details)){
                organization_details[le_cnt] = {}
            }
            if(!(d_cnt in organization_details[le_cnt])){
                organization_details[le_cnt][d_cnt] = {} 
            }
            if(selected_org in organization_details[le_cnt][d_cnt]){
                displayMessage(message.duplicate_industry);
                organization_details = {};
            }else{
                organization_details[
                    le_cnt][d_cnt][
                        parseInt(industry_id_map[selected_org])
                    ] = parseInt(no_of_units)
                clearMessage();
                closePopup();
            }
        }
    }
}


function saveClient(){
    var group_id = edit_id;
    var group_name = $('#group-text').val();
    var username = $("#username").val();
    if(group_name == ''){
      displayMessage(message.group_required);
    }else if(group_name.length > 50){
      displayMessage(message.group_50);
    }else if(username == ''){
      displayMessage(message.username_required);
    }else if(validateEmail(username) == ''){
      displayMessage(message.username_invalid);
    }else{
        var is_valid = false
        var legal_entities = [];
        for (var i = 1; i <= le_count; i++) {
            var le_table = $(".le-table-"+i);
            var domains = [];
            var country_id = le_table.find(".country").val();
            var business_group_id = null;
            var business_group_name = null;
            if(le_table.find(".business-group").is(":visible")){
                business_group_id = le_table.find(".business-group").val();
            }else{
                business_group_name = le_table.find(".business-group-text").val();
            }
            var le_name = le_table.find("#legal_entity_text").val();
            var inchargePersonVal = le_table.find('#users').val();
            var logo = logoFile[i-1]
            if(typeof logo == 'string'){
                var ext = logo.split('.').pop().toLowerCase();
            }else{
                var ext = logo.file_name.split('.').pop().toLowerCase();
            }
            var licenceVal = le_table.find('#no-of-user-licence').val();
            var fileSpaceVal = le_table.find('#file-space').val();
            if (le_table.find('#subscribe-sms').is(':checked')) {
              var subscribeSmsVal = true;
            } else {
              var subscribeSmsVal = false;
            }
            var contractFromVal = le_table.find('.contract-from').val();
            var contractToVal = le_table.find('.contract-to').val();
            var domain_count = le_table.find('.domain-count').val();
            var d = new Date();
            var month = d.getMonth() + 1;
            var day = d.getDate();
            var output = d.getFullYear() + '/' + month + '/' + day;
            var currentDate = new Date(output);
            var convertDate = null;
            if (contractToVal != '') {
              convertDate = convert_date(contractToVal);
            }
            if(
                country_id == 0 || country_id == '0' || country_id == null
            ){
                displayMessage(message.country_required);
                break;
            }else if(le_name == '') {
                displayMessage(mbessage.legalentity_required);
                break;
            }else if(le_name.length > 50) {
                displayMessage(message.le_50);
                break;
            }else if (inchargePersonVal == '') {
                displayMessage(message.inchargeperson_required);
                break;
            }else if(logo == '') {
                displayMessage(message.logo_required);
                break;
            }else if ($.inArray(ext, ['gif', 'png', 'jpg', 'jpeg']) == -1) {
                displayMessage(message.logo_invalid);
                break;
            }else if (fileSpaceVal == '') {
                displayMessage(message.filespace_required);
                break;
            }else if (fileSpaceVal == '0') {
                displayMessage(message.filespace_invalid);
                break;
            }else if (!$.isNumeric(fileSpaceVal)) {
                displayMessage(message.filespace_invalid);
                break;
            }else if (fileSpaceVal.length > 3) {
                displayMessage(message.filespace_max3);
                break;
            }else if (contractFromVal == '') {
                displayMessage(message.contractfrom_required);
                break;
            }else if (contractToVal == '') {
                displayMessage(message.contractto_required);
                break;
            }else if (convertDate != null && convertDate < currentDate) {
                displayMessage(message.invalid_contractto);
                break;
            }else if (licenceVal == '') {
                displayMessage(message.licence_required);
                break;
            }else if (licenceVal == '0' || licenceVal == '1') {
                displayMessage(message.licence_invalid);
                break;
            }else if (isNaN(licenceVal)) {
                displayMessage(message.licence_invalid);
                break;
            }else if (licenceVal.length > 3) {
                displayMessage(message.licence_max3);
                break;
            }else if (domain_count <= 0){
                displayMessage(message.domain_required + " for "+le_name);
                break;
            }else{
                var inner_is_valid = false;
                var domain_ids = []
                for (var j = 1; j <= domain_count; j++) {
                    var domain_id = $(".domain-"+i+"-"+j+" option:selected").val();
                    if(domain_ids.indexOf(domain_id) > -1){
                        displayMessage(message.duplicate_domain + " for "+le_name);
                        break;
                    }else if(domain_id == 0 || domain_id == '0' || domain_id == null){
                        displayMessage(message.domain_required + " for "+le_name);
                        break;
                    }else if(!(i in organization_details)){
                        displayMessage(message.organization_required + " for "+le_name);
                        break;
                    }else if(!(j in organization_details[i])){
                        displayMessage(message.organization_required + " for "+le_name);
                        break;
                    }else if(Object.keys(organization_details[i][j]).length <= 0 ){
                        displayMessage(message.organization_required + " for "+le_name);
                        break;
                    }else if(j == domain_count){
                        inner_is_valid = true;
                    }
                    domain_ids.push(domain_id);
                    domains.push(
                        mirror.getDomainRow(
                            parseInt(domain_id), organization_details[i][j]
                        )
                    )
                }
                if(inner_is_valid == false){
                    break;
                }
            }
            if(i == le_count){
                is_valid = true
            }
            var arrayinchargePersonVal = inchargePersonVal.split(',');
            var arrayinchargePerson = [];
            for (var k = 0; k < arrayinchargePersonVal.length; k++) {
                arrayinchargePerson[k] = parseInt(arrayinchargePersonVal[k]);
            }
            inchargePersonVal = arrayinchargePerson;
            console.log("le_count:"+i);
            legal_entity_id = legal_entity_id_map[i]
            var new_logo = null;
            console.log("legal_entity_id:"+legal_entity_id+", type:"+typeof legal_entity_id);
            if(typeof legal_entity_id == 'string' || typeof legal_entity_id == 'number'){
                legal_entity_id = legal_entity_id;
            }else{
                legal_entity_id = null;
            }
            var new_logo = null
            if(typeof logo == 'string'){
                new_logo = null
            }else{
                new_logo = logo;
                logo = null;
            }
            if(edit_id == null){
                legal_entities.push(
                    mirror.getLegalEntityRow(
                        parseInt(country_id), parseInt(business_group_id), business_group_name,
                        le_name, inchargePersonVal, logo, parseInt(licenceVal),
                        parseInt(fileSpaceVal), subscribeSmsVal, contractFromVal, contractToVal, domains
                    )
                )    
            }else{
                legal_entities.push(
                    mirror.getLegalEntityUpdateRow(
                        parseInt(country_id), parseInt(business_group_id), 
                        business_group_name, legal_entity_id, le_name, 
                        inchargePersonVal, logo, new_logo, parseInt(licenceVal),
                        parseInt(fileSpaceVal), subscribeSmsVal, contractFromVal,
                        contractToVal, domains
                    )
                )
            }
            
        }
        if(is_valid == true){
            date_configurations = []
            $.each(country_domain_id_map, function (key, value) {
                var country_id = key;
                $.each(value["domain_names"], function (name_key, name_value) {
                    var domain_id = value["domains"][name_key];
                    var from = $('.tl-from-' + country_id + '-' + domain_id).val();
                    var to = $('.tl-to-' + country_id + '-' + domain_id).val();
                    date_configurations.push(
                        mirror.getDateConfigurations(
                            parseInt(country_id), parseInt(domain_id),
                            parseInt(from), parseInt(to)
                        )
                    )
                });
            });
            if(edit_id == null){
                callSaveClientApi(group_name, username, legal_entities, date_configurations);   
            }else{
                callUpdateClientApi(edit_id, group_name, username, legal_entities, date_configurations); 
            }
            
        }
    }
}

function callSaveClientApi(
    group_name, username, legal_entities, date_configurations
){
    clearMessage();
    function onSuccess(data){
        displayMessage(message.client_save_success);
        initialize("list");
    }
    function onFailure(error){
        displayMessage(error);
    }
    mirror.saveClientGroup(group_name, username, legal_entities,
        date_configurations,
        function (error, response){
            if (error == null) {
                onSuccess(response);
            }else {
                onFailure(error);
            }
        }
    );
}

function callUpdateClientApi(
    group_id, group_name, username, legal_entities, date_configurations
){
    clearMessage();
    function onSuccess(data){
        displayMessage(message.client_update_success);
        initialize("list");
    }
    function onFailure(error){
        displayMessage(error);
    }
    mirror.updateClientGroup(group_id, group_name, username, legal_entities,
        date_configurations,
        function (error, response){
            if (error == null) {
                onSuccess(response);
            }else {
                onFailure(error);
            }
        }
    );
}

function convert_date(data) {
  var date = data.split('-');
  var months = [
    'Jan',
    'Feb',
    'Mar',
    'Apr',
    'May',
    'Jun',
    'Jul',
    'Aug',
    'Sep',
    'Oct',
    'Nov',
    'Dec'
  ];
  for (var j = 0; j < months.length; j++) {
    if (date[1] == months[j]) {
      date[1] = months.indexOf(months[j]) + 1;
    }
  }
  if (date[1] < 10) {
    date[1] = '0' + date[1];
  }
  return new Date(date[2], date[1] - 1, date[0]);
}

function activateUsers(element, incharge_class, user_list_class, hidden_user_class) {
    var chkstatus = $(element).attr('class');
    if (chkstatus == 'active_selectbox_users') {
        $(element).removeClass('active_selectbox_users');
    } else {
        $(element).addClass('active_selectbox_users');
    }
    activateUsers_user(incharge_class, user_list_class, hidden_user_class);
}

function activateUsers_user(incharge_class, user_list_class, hidden_user_class) {
  var selids = '';
  var totalcount = $('.'+user_list_class+' .active_selectbox_users').length;
  $('.'+user_list_class+' .active_selectbox_users').each(function (index, el) {
    if (index === totalcount - 1) {
      selids = selids + el.id;
    } else {
      selids = selids + el.id + ',';
    }
  });
  $('.'+incharge_class).val(totalcount + ' Selected');
  $('.'+hidden_user_class).val(selids);
}

/*
  Handling Add & Edit
*/

function editClient(){
    $('#group-text').val(GROUPNAME);
    $("#username").val(USERNAME);
    $("#username").attr("readonly", "readonly");
    le_count = 0
    logoFile = [];
    legal_entity_id_map = {}
    organization_details = {}
    $.each(LEGALENTITIES, function(key, value){
        addClient();
        var le_table = $(".le-table-"+le_count);
        legal_entity_id_map[parseInt(le_count)] = value.l_e_id
        var domains = [];
        le_table.find(".country").val(value.c_id);
        if(value.b_g){
            le_table.find(".business-group").val(value.business_group.b_g_id);
        }
        le_table.find("#legal_entity_text").val(value.l_e_name);
        var incharge_class = "incharge-"+le_count;
        var user_list_class = "ulist-"+le_count;
        var hidden_user_class = "users-"+le_count
        loadUsers(incharge_class, user_list_class, hidden_user_class, value.inc_p)
        le_table.find('#usersSelected').val(value.inc_p.length + ' Selected');
        le_table.find('#no-of-user-licence').val(value.n_o_l);
        le_table.find('#file-space').val(value.f_s);
        if(value.sms == true){
            le_table.find('#subscribe-sms').attr("checked", "checked");   
        }else{
            le_table.find('#subscribe-sms').attr("checked", false);   
        }
        le_table.find('.contract-from').val(value.c_f);
        le_table.find('.contract-to').val(value.c_t);
        logoFile.push(value.logo);
        le_table.find("#upload-logo-img").attr("src","http://"+window.location.host+"/knowledge/clientlogo/"+value.logo);
        for(var i=1; i<=value.d.length; i++){
            var domain_list_class = "domain-list-"+le_count;
            var domain_count_class = "domain-count-"+le_count; 
            var domain_class = "domain-"+le_count+"-"+i
            addDomain(domain_list_class, domain_count_class)
            $("."+domain_class).val(value.d[i-1].d_id);
            orgs = value.d[i-1].org
            console.log("domain_list_class: "+ domain_list_class);
            console.log("le_count:"+le_count+", i : "+i);
            console.log(orgs);
            console.log(organization_details);
            organization_details[le_count] = {}
            organization_details[le_count][i] = orgs   
            console.log(organization_details);    
        }
    });
    generateDateConfigurationList();
    $.each(DATECONFIGURATIONS, function(key, value){
        var country_id = value.country_id
        var domain_id = value.domain_id
        $('.tl-from-' + country_id + '-' + domain_id).val(value.period_from)
        $('.tl-to-' + country_id + '-' + domain_id).val(value.period_to)
    });
}

function addClient(){
    var le_row = $('.legal-entity-config-template .grid-table');
    var clone = le_row.clone();
    le_count ++;
    clone.find(".contract-from, .contract-to")
        .removeClass('hasDatepicker')
        .removeAttr('id')
        .datepicker({
            changeMonth: false,
            changeYear: false,
            numberOfMonths: 1,
            dateFormat: "dd-M-yy",
            monthNames: ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
            "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
        });
    $(".le-no", clone).val(le_count);
    $('.le-body').prepend(clone);

    var le_table_class = "le-table-"+le_count
    $('.letable', clone).addClass(le_table_class);

    var country_class = "country-"+le_count
    $('.country', clone).addClass(country_class);
    loadCountries(country_class);

    var bg_class = "bg-"+le_count
    $(".business-group", clone).addClass(bg_class);
    loadBusinessGroups(bg_class);

    var incharge_class = "incharge-"+le_count;
    var user_list_class = "ulist-"+le_count;
    var selectboxview_class = "selectboxview-users-"+le_count
    var hidden_user_class = "users-"+le_count
    $('#usersSelected', clone).addClass(incharge_class);
    $("#ulist-user", clone).addClass(user_list_class);
    $("#selectboxview-users", clone).addClass(selectboxview_class)
    $("#users", clone).addClass(hidden_user_class)
    $('.'+incharge_class).click(function(){
        showHideUserMenu(selectboxview_class, true)
    });
    $("."+user_list_class).on('mouseleave', function(){
        showHideUserMenu(selectboxview_class, false)
    });
    loadUsers(incharge_class, user_list_class, hidden_user_class, [])

    $('#upload-logo', clone).change(function (e) {
        mirror.uploadFile(e, le_count, function result_data(data, le_count) {
            if (
                data != 'File max limit exceeded' ||
                data != 'File content is empty' ||
                data != 'Invalid file format'
              ) {
                console.log(le_count);
                console.log(data);
                console.log(logoFile);
                logoFile[le_count-1]= data;
                console.log(logoFile);
            } else {
                alert(data);
                custom_alert(data);
            }
        });
    });

    var add_domain_class = "domain-"+le_count;
    var domain_list_class = "domain-list-"+le_count;
    var domain_count_class = "domain-count-"+le_count; 
    $(".add-domain", clone).addClass(add_domain_class);
    $(".domain-list", clone).addClass(domain_list_class);
    $(".domain-count", clone).addClass(domain_count_class);
    $("."+domain_count_class).val(0);
    $("."+add_domain_class).click(function(){
        addDomain(domain_list_class, domain_count_class)
    });
}

function addOrganization(){
    var le_cnt = $("#le-cnt").val();
    var d_cnt = $("#d-cnt").val();
    var o_cnt = $("#o-cnt").val();
    $("#o-cnt").val(++o_cnt);
    var org_row = $('.organization-template .org-row');
    var clone = org_row.clone();

    var org_class = "org-"+le_cnt+"-"+d_cnt+"-"+o_cnt
    $(".org", clone).addClass(org_class)

    var org_selected_class = "org-selected-"+le_cnt+"-"+d_cnt+"-"+o_cnt
    $('#orgselected', clone).addClass(org_selected_class);

    var ac_class = "ac-industry-"+le_cnt+"-"+d_cnt+"-"+o_cnt;
    $("#ac-industry", clone).addClass(ac_class);

    var val_class = "industry-"+le_cnt+"-"+d_cnt+"-"+o_cnt;
    $("#industry", clone).addClass(val_class);

    var no_of_units_class = "no-of-units-"+le_cnt+"-"+d_cnt+"-"+o_cnt; 
    $(".no-of-units", clone).addClass(no_of_units_class);

    var org_list_class = "org-list-"+le_cnt+"-"+d_cnt+"-"+o_cnt
    $("#ulist-org", clone).addClass(org_list_class);
    $(".organization-list").append(clone);
    $('.'+org_selected_class).keyup(function (e) {
        var textval = $(this).val();
        selected_textbox = $(this);
        getOrgAutocomplete(e, textval, INDUSTRIES, ac_class, val_class,
            function (val) {
            onOrgSuccess(val);
        });
    });
}

function addDomain(domain_list_class, domain_count_class){
    domain_count = $("."+domain_count_class).val();
    $("."+domain_count_class).val(++domain_count);

    var domain_row = $('.domain_row_template tr');
    var clone = domain_row.clone();

    var remove_class = "remove-domain-"+le_count+"-"+domain_count;
    $(".domain_row", clone).addClass(remove_class);

    var domain_class = "domain-"+le_count+"-"+domain_count
    $(".domain", clone).addClass(domain_class)
    $(".domain", clone).change(function(){
        generateDateConfigurationList();
    });

    $(".addOrganizationType", clone).click(function(){
        var le_cnt = le_count;
        var d_cnt = domain_count;
        displayPopup(le_cnt, d_cnt);
    });

    $(".remove-domain", clone).click(function(e){
        e.preventDefault();
        $(this).parent().parent().remove();
    });
    $('.'+domain_list_class).append(clone);

    loadDomains(domain_class);
}

function prepareCountryDomainMap(){
    for (var i = 1; i <= le_count; i++) {
        var country_id = $(".country-"+i+" option:selected").val();
        if(country_id != 'undefined' && country_id != '0' && country_id != null){
            var country_name = $(".country-"+i+"  option:selected").text();
            if(!(country_id in country_domain_id_map)){
                country_domain_id_map[country_id] = {
                    "country_name": country_name,
                    "domains": [],
                    "domain_names": [],
                    "from":[],
                    "to":[]
                }
            }
            for (var j = 1; j <= domain_count; j++) {
                var domain_id = $(".domain-"+i+"-"+j+" option:selected").val();
                if(domain_id != 'undefined' && domain_id != '0' && domain_id != null){
                    var domain_name = $(".domain-"+i+"-"+j+" option:selected").text();
                    if(country_domain_id_map[country_id]["domains"].indexOf(domain_id) == -1){
                        country_domain_id_map[country_id]["domains"].push(domain_id);
                        country_domain_id_map[country_id]["domain_names"].push(domain_name);
                    }
                }
            }
        }
    }
}

function generateDateConfigurationList(){
    $('.tbody-dateconfiguration-list').empty();
    prepareCountryDomainMap();
    $.each(country_domain_id_map, function (key, value) {
        var tableRow = $('.dconfig-templates .table-dconfig-list .table-dconfig-countries-row');
        var clone = tableRow.clone();
        var country_id = key;
        $('.dconfig-country-name', clone).text(value["country_name"]);
        $('.dconfig-country-name', clone).addClass('heading');
        $('.inputCountry', clone).text(country_id);
        $('.tbody-dateconfiguration-list').append(clone);
        $.each(value["domain_names"], function (name_key, name_value) {
            var domain_id = value["domains"][name_key];
            var tableRowDomains = $('.dconfig-templates .table-dconfig-list .table-dconfig-domain-row');
            var clone1 = tableRowDomains.clone();
            $('.inputDomain', clone1).text(domain_id);
            $('.dconfig-domain-name', clone1).text(value["domain_names"][name_key]);
            $('.tl-from', clone1).addClass('tl-from-' + country_id + '-' + domain_id);
            $('.tl-to', clone1).addClass('tl-to-' + country_id + '-' + domain_id);
            $('.tbody-dateconfiguration-list').append(clone1);
        });
    });
}

function loadCountries(country_class){
    $('.' + country_class + "  option:gt(0)").remove();
    country_html = "<option value = '0'>(Select Country)</option>"
    $.each(COUNTRIES, function(key, value){
        country_html += "<option value = "+value.country_id+">"+value.country_name+"</option>"
    });
    $('.' + country_class).html(country_html);
}

function loadDomains(domain_class){
    $('.' + domain_class + "  option:gt(0)").remove();
    domain_html = "<option value = '0'>(Select Domain)</option>"
    $.each(DOMAINS, function(key, value){
        domain_html += "<option value = "+value.domain_id+">"+value.domain_name+"</option>"
    });
    $('.' + domain_class).html(domain_html);
}
 
function loadBusinessGroups(bg_class){
    $('.' + bg_class + "  option:gt(0)").remove();
    bg_html = "<option value ='0'>(Select Business Group)</option>"
    $('.' + bg_class).html(bg_html);
}

// function hidemenu(type) {
//     $("#ac-org").hide();
// }

// function showmenu(type) {
//     $("#ac-org").show();
// }

function showHideUserMenu(selectboxview_class, is_active) {
    if(is_active == true){
        $("."+selectboxview_class).show();          
    }else{
        $("."+selectboxview_class).hide();          
    }
}

function loadUsers(incharge_class, user_list_class, hidden_user_class, selectedUsers) {
    $("."+ incharge_class).css("display", "block");
    $('.'+user_list_class).empty();
    var selids = '';
    $.each(USERS, function(key, value){
        var obj = $(".user-list-drop-down li");
        var clone = obj.clone();
        clone.attr("id", value.user_id);
        clone.click(function(){
            activateUsers(this, incharge_class, user_list_class, hidden_user_class);
        });
        clone.text(value.employee_name);
        if(selectedUsers.indexOf(value.user_id) > -1){
            clone.addClass("active_selectbox_users");
        }
        $('.'+user_list_class).append(clone);
    });
    $('.'+incharge_class).val(selectedUsers.length + ' Selected');
    $("."+hidden_user_class).val(selectedUsers.join(","));
}

function onOrgSuccess(val) {
    selected_textbox.val(val[1]);
}

function addOrSelectBusinessGroup(type_of_icon){
    if(type_of_icon == "add"){
        $(".input_business_group").show();
        $(".select_business_group").hide();
    }else if(type_of_icon == "cancel"){
        $(".input_business_group").hide();
        $(".select_business_group").show();
    }
}

function displayPopup(le_cnt, d_cnt) {
    $('.overlay').css('visibility', 'visible');
    $('.overlay').css('opacity', '1');
    $("#le-cnt").val(le_cnt);
    $("#d-cnt").val(d_cnt);
    $("#o-cnt").val(0);
    $('.organization-list').empty();
    if(le_cnt in organization_details){
        if(d_cnt in organization_details[le_cnt]){
            o_cnt = 0;
            $.each(organization_details[le_cnt][d_cnt], function(key, value){
                ++ o_cnt;
                addOrganization();
                $(".org-selected-"+le_cnt+"-"+d_cnt+"-"+o_cnt).val(key);
                $(".no-of-units-"+le_cnt+"-"+d_cnt+"-"+o_cnt).val(value);
            });
            $("#o-cnt").val(o_cnt);
        }
    }
    
}

function closePopup(){
    $('.overlay').css('visibility', 'hidden');
    $('.overlay').css('opacity', '0');
}

function changeClientStatus(pass_value, group_id){
    function onSuccess(data) {
        displayMessage(message.client_change_status_success);
        initialize("list");
    }
    function onFailure(error) {
        displayMessage(error);
    }
    mirror.changeClientGroupStatus(
        parseInt(group_id), pass_value ,function (error, response) {
        if (error == null) {
            onSuccess(response);
        }else {
            onFailure(error);
        }
    });
}

$(document).ready(function () {
    initialize("list");
});
