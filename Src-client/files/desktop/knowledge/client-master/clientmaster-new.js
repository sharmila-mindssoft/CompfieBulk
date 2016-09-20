var le_count = 0;
var edit_id = null;
var organization_details = {}
var country_domain_id_map = {}
var selected_textbox = '';
var logoFile = {};
var industry_id_map = {}

var COUNTRIES = '';
var DOMAINS = '';
var INDUSTRIES = '';
var USERS = '';


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
            $.each(INDUSTRIES, function(key, value){
                industry_id_map[value.industry_name] = parseInt(value.industry_id)
            });
            USERS = data.users;
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

  }else{
    // Invalid initialization Do nothing
  }
}

function showPage(type_of_initialization){
  if(type_of_initialization == "list"){
    $("#clientgroup-view").show();
    $("#clientgroup-add").hide();
  }else{
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
        var passStatus = null;
        var classValue = null;
        // if (isActive == true) {
        passStatus = false;
        classValue = 'active-icon';
        // } else {
        //   passStatus = true;
        //   classValue = 'inactive-icon';
        // }
        var tableRow = $('#templates .table-clientgroup-list .table-row');
        var clone = tableRow.clone();
        sno = sno + 1;
        $('.sno', clone).text(sno);
        $('.country_names', clone).text(value.country_names);
        $('.group_name', clone).text(value.group_name);
        $('.no_of_entities', clone).text(value.no_of_legal_entities);
        $('.edit-icon').attr('title', 'Edit');
        $('.edit-icon', clone).on('click', function () {
            
        });
        $('.status', clone).addClass(classValue);
        $('.active-icon').attr('title', 'Deactivate');
        $('.inactive-icon').attr('title', 'Activate');
        $('.status', clone).on('click', function () {
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
    saveOrUpdateClient();
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

function saveOrUpdateClient(){
    if(edit_id == null){
        saveClient();
    }else{
        updateClient();
    }
}

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
            var uploadLogoVal = le_table.find('#upload-logo').val().trim();
            var logo = logoFile[i]
            var ext = uploadLogoVal.split('.').pop().toLowerCase();
            var licenceVal = le_table.find('#no-of-user-licence').val().trim();
            var fileSpaceVal = le_table.find('#file-space').val().trim();
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
                displayMessage(message.legalentity_required);
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
            console.log("Adding to legal entity");
            console.log(logo);
            legal_entities.push(
                mirror.getLegalEntityRow(
                    parseInt(country_id), parseInt(business_group_id), business_group_name,
                    le_name, inchargePersonVal, logo, parseInt(licenceVal),
                    parseInt(fileSpaceVal), subscribeSmsVal, contractFromVal, contractToVal, domains
                )
            )
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
            callSaveClientApi(group_name, username, legal_entities, date_configurations)
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

function activateUsers(element) {
  var chkstatus = $(element).attr('class');
  if (chkstatus == 'active_selectbox_users') {
    $(element).removeClass('active_selectbox_users');
  } else {
    $(element).addClass('active_selectbox_users');
  }
  activateUsers_user();
}

function activateUsers_user() {
  var selids = '';
  var totalcount = $('.active_selectbox_users').length;
  $('.active_selectbox_users').each(function (index, el) {
    if (index === totalcount - 1) {
      selids = selids + el.id;
    } else {
      selids = selids + el.id + ',';
    }
  });
  $('#usersSelected').val(totalcount + ' Selected');
  $('#users').val(selids);
}

function updateClient(){
    collectValues();
    if(validateValues() == true){
        alert("Going to update");
    }
}
/*
  Handling Add
*/
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
    $('#usersSelected', clone).addClass(incharge_class);
    $("#ulist-user", clone).addClass(user_list_class);
    $('.'+incharge_class).click(function(){
        loadUsers(incharge_class, user_list_class)
    });
    loadUsers(incharge_class, user_list_class);

    $('#upload-logo', clone).change(function (e) {
        console.log("uploading logo");
        mirror.uploadFile(e, le_count, function result_data(data, le_count) {
            if (
                data != 'File max limit exceeded' ||
                data != 'File content is empty' ||
                data != 'Invalid file format'
              ) {
                console.log(data);
                logoFile[le_count] = data;
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

function hidemenu(type) {
    if(type == "org"){
        $("#ac-org").hide();
    }else{
        $("#selectboxview-users").hide();      
    }
}

function showmenu(type) {
    if(type == "org"){
        $("#ac-org").show();
    }else{
        $("#selectboxview-users").show();      
    }
}

function loadUsers(incharge_class, user_list_class) {
    $("."+ incharge_class).css("display", "block");
    $('.'+user_list_class).empty();
    var str = '';
    var selectedUsers = [];
    $.each(USERS, function(key, value){
        str += '<li id="' + value.user_id + '" onclick="activateUsers(this)" >' + value.employee_name + '</li> ';
    });
    $('.'+user_list_class).append(str);
    $('.'+incharge_class).val(selectedUsers.length + ' Selected');
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
}

function closePopup(){
    $('.overlay').css('visibility', 'hidden');
    $('.overlay').css('opacity', '0');
}

$(document).ready(function () {
    initialize("list");
});
