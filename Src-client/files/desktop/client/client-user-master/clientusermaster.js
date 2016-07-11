var countriesList;
var businessGroupsList;
var legalEntitiesList;
var divisionList;
var domainList;
var unitList;
var userGroupsList;
var serviceProviderList;
var userList;
var is_session_user_primary_admin;

$(function() {
    $('.service_provider').hide();
    $('#usertype').change(function () {
        if($("#usertype").val() == 'Service Provider'){
            $('.service_provider').show();
            $('.star').hide();
            $('.seatingunit').hide();
        }
        else{
            $('.service_provider').hide();
            $('.seatingunit').show();
            $('.star').show();
        }
    });
});
$("#btn-user-add").click(function(){
    $("#user-add").show();
    $("#user-view").hide();
    var x=document.getElementsByTagName("input");
    for(i = 0; i<=x.length-1; i++){
        if(x.item(i).type!="submit" ){ x.item(i).value = ""; }
    }

    clearMessage();
    $("#user-privilege-id").val('');
    $("#unitList li:gt(0)").remove();
    $("#email-id").removeAttr("readonly");
    $("#usertype").val("");
    $("#user-level option:selected").removeAttr("selected");
    $("#usergroupval").removeAttr("disabled", "disabled");
    loadautocountry();
    hidemenu();
    loadautobusinessgroups();
    hidemenubgroup();
    loadautolegalentities();
    hidemenulegalentities();
    loadautodivision();
    hidemenudivision();
    loadautodomains();
    hidemenudomains();
});
$("#btn-user-cancel").click(function(){
    $("#user-add").hide();
    $("#user-view").show();
    var x=document.getElementsByTagName("input");
    for(i = 0; i<=x.length-1; i++){
        if(x.item(i).type!="submit" ){ x.item(i).value = ""; }
    }

    clearMessage();
    $("#user-privilege-id").val('');
    $("#unitList li:gt(0)").remove();
    $("#email-id").removeAttr("readonly");
    $("#usertype").val("");
    $("#user-level option:selected").removeAttr("selected");
    $("#usergroupval").removeAttr("disabled", "disabled");
});
function initialize(){
    function onSuccess(data){
        countriesList = data['countries'];
        businessGroupsList = data['business_groups'];
        legalEntitiesList = data['legal_entities'];
        divisionList = data['divisions'];
        domainList = data['domains'];
        unitList = data['units'];
        userGroupsList = data['user_groups'];
        serviceProviderList = data['service_providers'];
        userList = data['users'];
        remaining_licence = data["remaining_licence"]
        is_session_user_primary_admin = data["is_primary_admin"]
        if (parseInt(remaining_licence) <= 0){
        	$(".btn-add").hide();
        }
        loadClientUserList();
    }
    function onFailure(error){
        console.log(error);
    }
    client_mirror.getClientUsers(
        function(error, response){
            if(error == null){
                onSuccess(response);
            }
            else{
                onFailure(error);
            }
        }
    );
}
function getUserGroupName(userGroupId){
    var usergroupname;
    if(userGroupId != null){
        $.each(userGroupsList, function(key, value) {  //usergroupname
            if(userGroupsList[key]['user_group_id'] == userGroupId){
                usergroupname = userGroupsList[key]['user_group_name'];
            }
        });
    }
    return usergroupname;
}
function getUnitNameAndAddress(unitId){
    var unit = {};
    if(unitId != null){
        $.each(unitList, function(key, value) {
            if(value['unit_id'] == unitId){
                unit['unitName'] = value['unit_name'];
                unit['unitAddress'] = value['unit_address'];
            }
        });
    }
    return unit;
}

function loadClientUserList(){
    $(".tbody-users-list").find("tr").remove();
    var sno = 0;
    var imageName, title, usergroupname, seatingunitname, seatingunitaddress, username;
    for(var i in userList){
        var users = userList[i];
        var username = users["email_id"];
        var userId = users["user_id"];
        var isActive = users["is_active"];
        var isAdmin = users["is_admin"];
        var isPrimaryAdmin = users["is_primary_admin"];

        if(isActive == true){
            imageName = "icon-active.png";
            title = "Click here to deactivate"
            statusVal = false;
        }
        else{
            imageName = "icon-inactive.png";
            title = "Click here to Activate"
            statusVal = true;
        }
        if(isAdmin == true || isPrimaryAdmin == true){
            adminstatus = false;
            imageadminName = "promote-active.png";
            admintitle = "Click here to deactivate Promote Admin";
        }
        else{
            adminstatus = true;
            imageadminName = "promote-inactive.png";
            admintitle = "Click here to Promote Admin";
        }

        var seatingUnitId = userList[i]['seating_unit_id'];
        var serviceProviderId = userList[i]['service_provider_id'];
        var userGroupId = userList[i]['user_group_id'];

        //if(users["user_group_id"] != null){
        var tableRow = $('#templates .table-users-list .table-row');
        var clone = tableRow.clone();
        sno = sno + 1;
        $('.sno', clone).text(sno);
        if (isActive == false && isPrimaryAdmin == true){
            $('.employee-code-name', clone).text("Old Administrator");
        }
        else if(isActive == true && isPrimaryAdmin == true){
            $('.employee-code-name', clone).text("Administrator");
        }
        else if(userList[i]["is_service_provider"] == true){
            $('.employee-code-name', clone).text(getServiceProviderName(userList[i]["service_provider_id"])+" - "+users["employee_name"]);
        }
        else{
            $('.employee-code-name', clone).text(users["employee_code"]+" - "+users["employee_name"]);
        }

        $(".username", clone).text(username);
        $('.group-name', clone).text(getUserGroupName(userGroupId));
        $('.level-name', clone).text("Level "+users["user_level"]);
        if(userList[i]["is_service_provider"] == true){
            $('.seating-unit', clone).html("-");
        }
        else if (seatingUnitId != null){
         $('.seating-unit', clone).html('<abbr class="page-load" title="'+getUnitNameAndAddress(seatingUnitId)['unitAddress']+'"><img src="/images/icon-info.png" style="margin-right:10px"/>'+getUnitNameAndAddress(seatingUnitId)['unitName']);
        }
        if (userId != 0){
            $('.edit', clone).html('<img src="/images/icon-edit.png" id="editid" onclick="user_edit('+userId+')"/>');
        }
        if (isPrimaryAdmin == false){
            $('.is-active', clone).html('<img src="/images/'+imageName+'" title="'+title+'" onclick="user_active('+userId+', '+statusVal+')"/>');
            if (is_session_user_primary_admin == true){
                $('.promote-admin', clone).html('<img src="/images/'+imageadminName+'" title="'+admintitle+'" onclick="user_isadmin('+userId+', '+adminstatus+')" />');
            }
        }
        $('.tbody-users-list').append(clone);
        //}
    }
}
function user_edit(userId){
    $("#user-add").show();
    $("#user-view").hide();
    $("#client-user-id").val(userId);
    clearMessage();
    function onSuccess(data){
        loadUserUpdate(userId);
    }
    function onFailure(error){
        console.log(error);
    }
    client_mirror.getClientUsers(
        function(error, response){
            if(error == null){
                onSuccess(response);
            }
            else{
                onFailure(error);
            }
        });
}
function getServiceProviderName(sid){
    var spname = null;
    $.each(serviceProviderList, function(key, val){
        if(val["service_provider_id"] == sid){
            spname = val["service_provider_name"];
        }
    });
    return spname;
}
function loadUserUpdate(userId){
    var bgroups = [];
    var lentities = [];
    var divisions = [];
    var bgroupslist;
    var lentitieslist;
    var divisionlist;
    for(var user in userList){
        if(userList[user]['user_id'] == userId){
            seatingunitname = null
            $.each(userGroupsList, function(key, value) {  //usergroupname
                if(userGroupsList[key]['user_group_id'] == userList[user]['user_group_id']){
                    usergroupname = userGroupsList[key]['user_group_name'];
                }
            });
            $.each(unitList, function(key, value) { //unit name
                if(unitList[key]['unit_id'] == userList[user]['seating_unit_id']){
                    seatingunitname = unitList[key]['unit_name'];
                }
            });
            var contactno = userList[user]['contact_no'].split("-");
            $("#user-id").val(userId);

            if(userList[user]['is_service_provider'] == true){
                //$("#usertype  option[$("div.id_100 select").val("val2");value='Service Provider']").attr("selected", "selected");
                $("#usertype").val("Service Provider");
                $('.service_provider').show();
                $('.star').hide();
                $('.seatingunit').hide();
                $("#serviceproviderval").val(getServiceProviderName(userList[user]['service_provider_id']));
                $("#serviceprovider").val(userList[user]['service_provider_id']);
            }
            if(userList[user]['is_service_provider'] == false){
                //$('#usertype option[value="Inhouse"]').attr("selected", "selected");
                $("#usertype").val("Inhouse");
                $('.service_provider').hide();
                $('.seatingunit').show();
                $('.star').show();
                $("#seatingunitval").val(seatingunitname);
                $("#seatingunit").val(userList[user]['seating_unit_id']);

            }
            $("#employee-name").val(userList[user]['employee_name']);
            $("#employee-id").val(userList[user]['employee_code']);
            $("#country-code").val(contactno[0]);
            $("#area-code").val(contactno[1]);
            $("#mobile-number").val(contactno[2]);
            $("#usergroupval").val(usergroupname);
            $("#usergroup").val(userList[user]['user_group_id']);
            if(userList[user]['is_admin']){
                $("#usergroupval").attr("disabled", "disabled");
            }
            $("#user-level").val(userList[user]['user_level']);
            //$("#user-level option[value = "+userList[user]['user_level']+"]").attr('selected','selected');
            $("#email-id").val(userList[user]['email_id']);            
            $("#email-id").attr("readonly", "readonly");
            $("#country").val(userList[user]['country_ids']);
            $("#units").val(userList[user]['unit_ids']);
            $("#domains").val(userList[user]['domain_ids']);
            for(var units in unitList){
                var unitid = unitList[units]['unit_id'];
                var user_unitids = userList[user]['unit_ids'];
                if ($.inArray(unitid, user_unitids) != -1){
                    bgroups.push(unitList[units]['business_group_id']);
                    lentities.push(unitList[units]['legal_entity_id']);
                    divisions.push(unitList[units]['division_id']);
                }
            }
            function unique(list) {
                var result = [];
                $.each(list, function(i, e) {
                    if ($.inArray(e, result) == -1) result.push(e);
                });
                return result;
            }

            $("#business-groups").val(unique(bgroups));
            $("#legal-entities").val(unique(lentities));
            $("#division").val(unique(divisions));
            loadautocountry();
            hidemenu();
            loadautobusinessgroups();
            hidemenubgroup();
            loadautolegalentities();
            hidemenulegalentities();
            loadautodivision();
            hidemenudivision();
            loadautodomains();
            hidemenudomains();
            unitview();
        }
    }
}
$('#country-code').on('input', function (event) {
    this.value = this.value.replace(/[^0-9]/g, '');
});
$('#area-code').on('input', function (event) {
    this.value = this.value.replace(/[^0-9]/g, '');
});
$('#mobile-number').on('input', function (event) {
    this.value = this.value.replace(/[^0-9]/g, '');
});
function isEmail(email) {
  var regex = /^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/;
  return regex.test(email);
}
$("#submit").click(function(){

    var checkLength = clientUserValidate();

    if(checkLength){
        var userId = $("#user-id").val();
        var usertype = $('#usertype').val().trim();
        var employeename = $('#employee-name').val().trim();
        var employeeid = $('#employee-id').val().trim();
        var countrycode = $('#country-code').val().trim();
        var areacode = $('#area-code').val().trim();
        var mobilenumber = $('#mobile-number').val().trim();
        var usergroup = $('#usergroup').val().trim();
        var userlevel = $('#user-level').val().trim();
        var emailid = $('#email-id').val().trim();
        var country = $('#country').val().trim();
        var businessgroups = $('#business-groups').val().trim();
        var legalentities = $('#legal-entities').val().trim();
        var division = $('#division').val().trim();
        var domains = $('#domains').val().trim();
        var units = $('#units').val().trim();
        var isserviceprovider, serviceprovider;

        if(usertype == "Inhouse"){
            isserviceprovider = false;
            serviceprovider = null;
            var seatingunit = $('#seatingunit').val().trim();
            var seatingunitname = $('#seatingunitval').val().trim();
            if(seatingunit == ""){
                displayMessage(message.seatingunit_required);
                return;
            }
            if(seatingunitname == ""){
                displayMessage(message.seatingunit_required);
                return;
            }
            if(employeeid == ""){
                displayMessage(message.employeecode_required);
                return;
            }
        }
        if(usertype == "Service Provider"){
            isserviceprovider = true;
            serviceprovider = parseInt($('#serviceprovider').val());
            if(serviceprovider.length == 0){
                displayMessage(message.spname_required);
                return;
            }
        }

        if(usertype == ""){
            displayMessage(message.usertype_required);
            return;
        }
        else if(employeename == ''){
            displayMessage(message.employeename_required);
        }
        else if(usergroup == ''){
            displayMessage(message.usergroup_required);
        }
        else if(userlevel == ''){
            displayMessage(message.userlevel_required);
        }
        else if(emailid == ''){
            displayMessage(message.emailid_required);
        }
        else if(!isEmail(emailid)){
            displayMessage(message.invalid_emailid);
        }
        else if(country == ''){
            displayMessage(message.country_required);
        }
        else if(legalentities == ''){
            displayMessage(message.legalentity_required);
        }
        else if(domains == ''){
            displayMessage(message.domain_required);
        }
        else if(units == ''){
            displayMessage(message.unit_required)
        }
        else if($('#client-user-id').val() == ''){
            var isAdmin = false;

            var arrayCountriesVal = country.split(",");
            var arrayCountries = [];
            for(var i = 0; i<arrayCountriesVal.length; i++){
                arrayCountries[i] = parseInt(arrayCountriesVal[i]);
            }

            var arrayDomainsVal = domains.split(",");
            var arrayDomains = [];
            for(var j = 0; j<arrayDomainsVal.length; j++){
                arrayDomains[j] = parseInt(arrayDomainsVal[j]);
            }

            var arrayUnitVal = units.split(",");

            var arrayUnits = [];
            for(var k = 0; k<arrayUnitVal.length; k++){
                if(arrayUnitVal[k]){
                    arrayUnits[k] = parseInt(arrayUnitVal[k]);
                }
            }
            arrayUnits = arrayUnits.filter(function(n){ return n != undefined });

            var clientUserDetail = [];
            var contactNo = countrycode+"-"+areacode+"-"+mobilenumber;

            clientUserDetail = [emailid, parseInt(usergroup), employeename,
                    employeeid, contactNo, parseInt(seatingunit), parseInt(userlevel),
                    arrayCountries, arrayDomains, arrayUnits, isAdmin, isserviceprovider,
                    serviceprovider];
            var clientUserDetailDict = client_mirror.getSaveClientUserDict(clientUserDetail);

            function onSuccess(data){
                $("#user-add").hide();
                $("#user-view").show();
                $(".filter-text-box").val('');
                initialize();
            }
            function onFailure(error){
                if(error == "EmailIdAlreadyExists"){
                    displayMessage(message.emailid_exists);
                }
                else{
                    displayMessage(error);
                }

            }
            client_mirror.saveClientUser(clientUserDetailDict,
                function(error, response){
                    if(error == null){
                        onSuccess(response);
                    }
                    else{
                        onFailure(error);
                    }
                }
            );
        }
        else if($('#client-user-id').val() != ''){
            var userId = $('#client-user-id').val();
            var isAdmin = false;

            var arrayCountriesVal = country.split(",");
            var arrayCountries = [];
            for(var i=0; i<arrayCountriesVal.length; i++){ arrayCountries[i] = parseInt(arrayCountriesVal[i]); }

            var arrayDomainsVal = domains.split(",");
            var arrayDomains = [];
            for(var j=0; j<arrayDomainsVal.length; j++){ arrayDomains[j] = parseInt(arrayDomainsVal[j]); }

            var arrayUnitVal = units.split(",");

            var arrayUnits = [];
            for(var k=0; k<arrayUnitVal.length; k++){
                if(arrayUnitVal[k]){
                    arrayUnits[k] = parseInt(arrayUnitVal[k]);
                }
            }
            arrayUnits = arrayUnits.filter(function(n){ return n != undefined });
            var contactNo = countrycode+"-"+areacode+"-"+mobilenumber;

            function onSuccess(data){
                $("#usergroupval").removeAttr("disabled", "disabled");
                $("#user-add").hide();
                $("#user-view").show();
                $(".filter-text-box").val('');
                initialize();
            }
            function onFailure(status, data){
                displayMessage(status);
            }
            var clientUserDetail = [parseInt(userId),  parseInt(usergroup), employeename,
                      employeeid, contactNo, parseInt(seatingunit), parseInt(userlevel),
                      arrayCountries, arrayDomains, arrayUnits, isAdmin, isserviceprovider,
                      serviceprovider];

            var clientUserDetailDict = client_mirror.getUpdateClientUserDict(clientUserDetail);
            client_mirror.updateClientUser(clientUserDetailDict,
                function(error, response){
                    if(error == null){
                        onSuccess(response);
                    }
                    else{
                        onFailure(error);
                    }
                }
            );
        }
        else{
            console.log("All fails.. Something Wrong");
        }
    }
    
});
function user_active(userId, isActive){
    var msgstatus='deactivate';
    if(isActive){
        msgstatus='activate';
    }
    var answer = confirm('Are you sure want to '+msgstatus+ '?');
    if (answer)
    {
        function onSuccess(data){
            initialize();
        }
        function onFailure(error){
            if (error == "CannotChangePrimaryAdminStatus"){
                alert(message.cant_deactivate_primaryadmin);
            }
            else if(error == "ReassignCompliancesBeforeDeactivate"){
                alert(message.reassign_compliance_before_user_deactivate)
            }else{
                alert(error)
            }
        }
        client_mirror.changeClientUserStatus(userId, isActive,
            function(error, response){
                if(error == null){
                    onSuccess(response);
                }
                else{
                    onFailure(error);
                }
            }
        );
    }
}
function user_isadmin(userId, isAdmin){
    var msgstatus;
    if(isAdmin == 1){
        msgstatus='activate promote admin';
    }
    if(isAdmin == 0){
        msgstatus='deactivate promote admin';
    }
    var answer = confirm('Are you sure to '+msgstatus+ '?');
    if (answer)
    {
        function onSuccess(data){
            initialize();
        }
        function onFailure(error){
            if (error == "CannotPromoteServiceProvider"){
                alert("Cannot promote a service provider as admin");
            }else if (error == "CannotChangePrimaryAdminStatus"){
                alert("Only Techno team can change status of primary admin");
            }
        }
        client_mirror.changeAdminStatus(userId, isAdmin,
            function(error, response){
                if(error == null){
                    onSuccess(response);
                }
                else{
                    onFailure(error);
                }
            });
    }
}

function checkdomainids(arrayunitdomain, arrayalldomain ){
    var found = false;
    for (var i = 0; i < arrayalldomain.length; i++) {
        if (arrayunitdomain.indexOf(arrayalldomain[i]) > -1) {
            found = true;
            break;
        }
    }
    return found;
}

//country Selection
function hidemenu() {
    document.getElementById('selectboxview-country').style.display = 'none';
}

function loadautocountry () {
    document.getElementById('selectboxview-country').style.display = 'block';
    var editcountryval = [];
    if($("#country").val() != ''){
        editcountryval = $("#country").val().split(",");
    }
    //alert(editcountryval[0]+"---"+editcountryval[1]);
    var countries = countriesList;

    $('#selectboxview-country ul').empty();
    var str = '';
    for(var i in countries){
        var selectcountrystatus='';
        for(var j=0; j<editcountryval.length; j++){
            if(editcountryval[j]==countries[i]["country_id"]){
                selectcountrystatus='checked';
            }
        }
        var countryId=parseInt(countries[i]["country_id"]);
        var countryName=countries[i]["country_name"];
        if(selectcountrystatus == 'checked'){
            str += '<li id="'+countryId+'" class="active_selectbox_country" onclick="activateCountry(this)" >'+countryName+'</li> ';
        }else{
            str += '<li id="'+countryId+'" onclick="activateCountry(this)" >'+countryName+'</li> ';
        }
    }
  $('#selectboxview-country ul').append(str);
  $("#countryselected").val(editcountryval.length+" Selected");

}
//check & uncheck process
function activateCountry(element){
  var chkstatus = $(element).attr('class');
  if(chkstatus == 'active_selectbox_country'){
        $(element).removeClass("active_selectbox_country");
  }
  else{
    $(element).addClass("active_selectbox_country");
  }
    var selids='';
    var selNames='';
    var totalcount =  $(".active_selectbox_country").length;
    $(".active_selectbox_country").each( function( index, el ) {

        if (index === totalcount - 1) {
            selids = selids+el.id;
            selNames = selNames+$(this).text();
        }else{
            selids = selids+el.id+",";
            selNames = selNames+$(this).text()+",";
        }
    });
    $("#countryselected").val(totalcount+" Selected");
    $("#country").val(selids);
    unitview();

}
// business group --------------------------------------------------------------------------------------------------------
function hidemenubgroup() {
    document.getElementById('selectboxview-businessgroup').style.display = 'none';
}
function loadautobusinessgroups () {
    document.getElementById('selectboxview-businessgroup').style.display = 'block';
    var editbgroupsval=[];
    if($("#business-groups").val() != ''){
        editbgroupsval = $("#business-groups").val().split(",");
    }
    var businessgroups = businessGroupsList;

    $('#selectboxview-businessgroup ul').empty();
    var str='';
    for(var i in businessgroups){
        var selectbgroupstatus='';
        for(var j=0; j<editbgroupsval.length; j++){
            if(editbgroupsval[j]==businessgroups[i]["business_group_id"]){
                selectbgroupstatus='checked';
            }
        }
        var bgroupId=parseInt(businessgroups[i]["business_group_id"]);
        var bgroupName=businessgroups[i]["business_group_name"];
        if(selectbgroupstatus == 'checked'){
            str += '<li id="'+bgroupId+'" class="active_selectbox_bgroups" onclick="activatebgroups(this)" >'+bgroupName+'</li> ';
        }else{
            str += '<li id="'+bgroupId+'" onclick="activatebgroups(this)" >'+bgroupName+'</li> ';
        }
    }
  $('#selectboxview-businessgroup ul').append(str);
  $("#bgroupsselected").val(editbgroupsval.length+" Selected");
}
//check & uncheck process
function activatebgroups(element){
  var chkstatus = $(element).attr('class');
  if(chkstatus == 'active_selectbox_bgroups'){
        $(element).removeClass("active_selectbox_bgroups");
  }
  else{
    $(element).addClass("active_selectbox_bgroups");
  }
    var selids='';
    var selNames='';
    var totalcount =  $(".active_selectbox_bgroups").length;
    $(".active_selectbox_bgroups").each( function( index, el ) {

        if (index === totalcount - 1) {
            selids = selids+el.id;
            selNames = selNames+$(this).text();
        }else{
            selids = selids+el.id+",";
            selNames = selNames+$(this).text()+",";
        }
    });
    $("#bgroupsselected").val(totalcount+" Selected");
    $("#business-groups").val(selids);
    $('#selectboxview-legal-entities ul').empty();
    $("#legal-entities-selected").val("0 Selected");
    $("#legal-entities").val("");
    unitview();

}
// Legal Entity----------------------------------------------------------------------------------------------------------------------
function hidemenulegalentities() {
    document.getElementById('selectboxview-legal-entities').style.display = 'none';
}
function loadautolegalentities () {
    document.getElementById('selectboxview-legal-entities').style.display = 'block';
    var bgroupsValue = $("#business-groups").val();
    var arraybusinessgroups = bgroupsValue.split(',');
    $('#selectboxview-legal-entities ul').empty();
    if(arraybusinessgroups.length != 0){

        $.each(arraybusinessgroups,function(count, values){
            var editlegalentitiesval = [];
            if($("#legal-entities").val() != ''){
                editlegalentitiesval = $("#legal-entities").val().split(",");
            }
            var legalentities = legalEntitiesList;

            var str = '';
            if(arraybusinessgroups.length != 0){
                $.each(businessGroupsList, function(k, val){
                    if(val['business_group_id'] == arraybusinessgroups[count]){
                        str += '<li class="li-heading">'+val['business_group_name']+'</li> ';
                    }
                });
            }
            $.each(legalEntitiesList, function(k, val){
                if(arraybusinessgroups[count] == val['business_group_id']){
                    var selectlentitystatus='';
                    for(var j = 0; j < editlegalentitiesval.length; j++){
                        if(editlegalentitiesval[j] == val["legal_entity_id"]){
                            selectlentitystatus = 'checked';
                        }
                    }
                    var lentityId = parseInt(val["legal_entity_id"]);
                    var lentityName = val["legal_entity_name"];
                    if(selectlentitystatus == 'checked'){
                        str += '<li id="'+lentityId+'" class="active_selectbox_legal_entities" onclick="activatelegalentities(this)" >'+lentityName+'</li> ';
                    }else{
                        str += '<li id="'+lentityId+'" onclick="activatelegalentities(this)" >'+lentityName+'</li> ';
                    }
                }
            });
            $('#selectboxview-legal-entities ul').append(str);
            $("#legal-entities-selected").val(editlegalentitiesval.length+" Selected");
        });
    }
    if(bgroupsValue == ""){

        var editlegalentitiesval = [];
        if($("#legal-entities").val() != ''){
            editlegalentitiesval = $("#legal-entities").val().split(",");
        }
        var legalentities = legalEntitiesList;
        var str = '';
        $.each(legalEntitiesList, function(k, val){
            if(val['business_group_id'] == null){
                var selectlentitystatus='';
                for(var j = 0; j < editlegalentitiesval.length; j++){
                    if(editlegalentitiesval[j] == val["legal_entity_id"]){
                        selectlentitystatus = 'checked';
                    }
                }
                var lentityId = parseInt(val["legal_entity_id"]);
                var lentityName = val["legal_entity_name"];
                if(selectlentitystatus == 'checked'){
                    str += '<li id="'+lentityId+'" class="active_selectbox_legal_entities" onclick="activatelegalentities(this)" >'+lentityName+'</li> ';
                }else{
                    str += '<li id="'+lentityId+'" onclick="activatelegalentities(this)" >'+lentityName+'</li> ';
                }
            }
        });
        $('#selectboxview-legal-entities ul').append(str);
        $("#legal-entities-selected").val(editlegalentitiesval.length+" Selected");
    }
}
//check & uncheck process
function activatelegalentities(element){
    var chkstatus = $(element).attr('class');
    if(chkstatus == 'active_selectbox_legal_entities'){
        $(element).removeClass("active_selectbox_legal_entities");
    }
    else{
        $(element).addClass("active_selectbox_legal_entities");
    }
    var selids='';
    var totalcount =  $(".active_selectbox_legal_entities").length;
    $(".active_selectbox_legal_entities").each( function( index, el ) {
        if (index === totalcount - 1) {
            selids = selids+el.id;
        }else{
            selids = selids+el.id+",";
        }
    });
    $("#legal-entities-selected").val(totalcount+" Selected");
    $("#legal-entities").val(selids);
    unitview();
}
// Divisions----------------------------------------------------------------------------------------------------------------------
function hidemenudivision() {
    document.getElementById('selectboxview-division').style.display = 'none';
}
function loadautodivision() {
    document.getElementById('selectboxview-division').style.display = 'block';
    var lentityValue=$("#legal-entities").val();
    var arraylentity=lentityValue.split(',');
    $('#selectboxview-division ul').empty();
    $.each(arraylentity,function(count, values){
        var editdivisionval=[];
        if($("#division").val() != ''){
            editdivisionval = $("#division").val().split(",");
        }
        var divisions = divisionList;

        var str='';
        if(arraylentity.length != 0){ //for heading
            $.each(legalEntitiesList, function(key, value){
                if(value['legal_entity_id']==arraylentity[count]){
                    var dcount = 0;

                    $.each(divisionList, function(k, val){
                        if(arraylentity[count]==val['legal_entity_id']){
                            if(dcount == 0){
                                str+='<li class="li-heading">'+value['legal_entity_name']+'</li> ';
                            }
                            var selectdivisionstatus='';
                            for(var j=0; j<editdivisionval.length; j++){
                                if(editdivisionval[j]==val["division_id"]){
                                    selectdivisionstatus='checked';
                                }
                            }
                            var divisionId=parseInt(val["division_id"]);
                            var divisionName=val["division_name"];
                            if(selectdivisionstatus == 'checked'){
                                str += '<li id="'+divisionId+'" class="active_selectbox_division" onclick="activateDivision(this)" >'+divisionName+'</li> ';
                            }else{
                                str += '<li id="'+divisionId+'" onclick="activateDivision(this)" >'+divisionName+'</li> ';
                            }
                            dcount++;
                        }
                    });
                }
            });
        }

        $('#selectboxview-division ul').append(str);
        $("#division-selected").val(editdivisionval.length+" Selected");
    });


}
//check & uncheck process
function activateDivision(element){
  var chkstatus = $(element).attr('class');
  if(chkstatus == 'active_selectbox_division'){
        $(element).removeClass("active_selectbox_division");
  }
  else{
    $(element).addClass("active_selectbox_division");
  }
    var selids='';
    var selNames='';
    var totalcount =  $(".active_selectbox_division").length;
    $(".active_selectbox_division").each( function( index, el ) {
        if (index === totalcount - 1) {
            selids = selids+el.id;
        }else{
            selids = selids+el.id+",";
        }
    });
    $("#division-selected").val(totalcount+" Selected");
    $("#division").val(selids);
    unitview();
}
//Unit List -----------------------------------------------------------------------------------------------------
function unitview(){
    var unitids = [];
    var arrunits = [];
    if($("#client-user-id").val() != ""){
        unitids = $("#units").val().split(",");
    }
    var isNoUnit = true;
    var str = '<li id="0" onclick="activateUnit(this)" > Select All</li> ';

    $('#unitList ul li:gt(0)').remove();
    var countryid = $("#country").val();
    var countryarray = countryid.split(',');
    var arrayCountries = [];
    var selectunitstatusl = null;
    var selectunitstatusd = null;
    for(var i = 0; i < countryarray.length; i++){ arrayCountries[i] = parseInt(countryarray[i]); }
    if($("#domains").val() !=''){
        var domainid = $("#domains").val();
        var arrayDomainsVal = domainid.split(',');
        var arrayDomains = [];
        for(var j = 0; j < arrayDomainsVal.length; j++){ arrayDomains[j] = parseInt(arrayDomainsVal[j]); }

        var divisionIds = $("#division").val();
        var arraydivision = divisionIds.split(',');
        if(divisionIds != ""){
            $.each(arraydivision, function(count, values){
                var divcount = 0;
                var editunitvaldiv = [];
                if($("#units").val() != ''){
                    editunitvaldiv = $("#units").val().split(",");
                }

                if(arraydivision.length != 0)
                {
                    $.each(divisionList, function(key, value){
                        if(value['division_id'] == arraydivision[count]){
                            $.each(unitList, function(k, val){
                                if(arraydivision[count]==val['division_id'] &&  $.inArray(val['country_id'], arrayCountries) != -1 && checkdomainids(val['domain_ids'], arrayDomains) == true){
                                    if(divcount == 0) {
                                        str+='<li class="li-heading">'+value['division_name']+'</li> ';
                                    }
                                    var unitId = parseInt(val["unit_id"]);
                                    var unitName = val["unit_name"];
                                    isNoUnit = false;
                                    selectunitstatusd = '';
                                    for(var j=0; j<editunitvaldiv.length; j++){
                                        if(editunitvaldiv[j] == val["unit_id"]){
                                            selectunitstatusd = "active";
                                        }
                                    }
                                    if(selectunitstatusd == "active"){
                                        str += '<li id="'+unitId+'" class="active" onclick="activateUnit(this)" >'+unitName+'</li> ';
                                    }
                                    else{
                                        str += '<li id="'+unitId+'" onclick="activateUnit(this)" >'+unitName+'</li> ';
                                    }

                                    for(var j=0; j<unitids.length; j++){
                                        if(unitids[j]==unitId){
                                            arrunits.push(unitId);
                                        }
                                    }
                                    divcount++;
                                }
                            });
                        }
                    });
                }

            });
        }
        if(divisionIds == ""){
            var leIds = $("#legal-entities").val();
            var arrayle = leIds.split(',');
            $.each(arrayle, function(count, values){
                var lecount = 0;
                var editunitvallegal=[];
                if($("#units").val() != ''){
                    editunitvallegal = $("#units").val().split(",");
                }
                if(arrayle.length != 0){
                    $.each(legalEntitiesList, function(key, value){
                        $.each(unitList, function(k, val){
                            if(arrayle[count] == val['legal_entity_id'] && val['division_id'] == null && value['legal_entity_id'] == arrayle[count] &&  $.inArray(val['country_id'], arrayCountries) != -1 && checkdomainids(val['domain_ids'], arrayDomains) == true){
                                if(lecount == 0){
                                   str+='<li class="li-heading">'+value['legal_entity_name']+'</li>';
                                }
                                var unitId = parseInt(val["unit_id"]);
                                var unitName = val["unit_name"];
                                isNoUnit = false;
                                selectunitstatusl = "";
                                for(var j=0; j<editunitvallegal.length; j++){
                                    if(editunitvallegal[j]==val["unit_id"]){
                                        selectunitstatusl = "active";
                                    }
                                }
                                if(selectunitstatusl == "active"){
                                    str += '<li id="'+unitId+'" onclick="activateUnit(this)" class= "active" >'+unitName+'</li> ';
                                }
                                else{
                                    str += '<li id="'+unitId+'" onclick="activateUnit(this)" >'+unitName+'</li> ';
                                }
                                for(var j=0; j<unitids.length; j++){
                                    if(unitids[j]==unitId){
                                        arrunits.push(unitId);
                                    }
                                }
                                lecount++;
                            }
                        });
                    });
                }
            });
        }
    }

    if(isNoUnit) str = '';

    $('#unitList ul').append(str);
    for(var k = 0;  k < arrunits.length; k++){
        $("#"+arrunits[k]).addClass("active");
    }
}
function activateUnit(element){

    var chkstatus = $(element).attr('class');
    if(chkstatus == "active"){
        $(element).removeClass("active");
        if($(element).attr('id') == 0){
            $("#unitList li.active").each( function( index, el ) {
                $(el).removeClass("active");
            });
        }
    }
    else{
        $(element).addClass("active");
        if($(element).attr('id') == 0){
            $("#unitList li").each( function( index, el ) {
                if($(el).attr('class') == '' || $(el).attr('class') == undefined){
                    $(el).addClass("active");
                }
            });
        }
    }
    
    var selids='';
    var totalcount =  $("#unitList li.active").length;
    $("#unitList li.active").each( function( index, el ) {
        if (index === totalcount - 1) {
            if(el.id != 0) selids = selids+el.id;
        }
        else{
            if(el.id != 0) selids = selids+el.id+",";
        }
    });
    $("#units").val(selids);
}




//Domains---------------------------------------------------------------------------------------
function hidemenudomains() {
    document.getElementById('selectboxview-domains').style.display = 'none';
}
function loadautodomains () {
    document.getElementById('selectboxview-domains').style.display = 'block';
    var editdomainsval=[];
    if($("#domains").val() != ''){
        editdomainsval = $("#domains").val().split(",");
    }
    //alert(editdomainsval[0]+"---"+editdomainsval[1]);
    var domains = domainList;

    $('#selectboxview-domains ul').empty();
    var str='';
    for(var i in domainList){
        var selectdomainsstatus='';
        for(var j=0; j<editdomainsval.length; j++){
            if(editdomainsval[j]==domainList[i]["domain_id"]){
                selectdomainsstatus='checked';
            }
        }
        var domainsId=parseInt(domainList[i]["domain_id"]);
        var domainsName=domainList[i]["domain_name"];
        if(selectdomainsstatus == 'checked'){
            str += '<li id="'+domainsId+'" class="active_selectbox_domains" onclick="activatedomains(this)" >'+domainsName+'</li> ';
        }else{
            str += '<li id="'+domainsId+'" onclick="activatedomains(this)" >'+domainsName+'</li> ';
        }
    }
  $('#selectboxview-domains ul').append(str);
  $("#domainsselected").val(editdomainsval.length+" Selected");
}
//check & uncheck process
function activatedomains(element){
  var chkstatus = $(element).attr('class');
  if(chkstatus == 'active_selectbox_domains'){
        $(element).removeClass("active_selectbox_domains");
  }
  else{
    $(element).addClass("active_selectbox_domains");
  }
    var selids='';
    var selNames='';
    var totalcount =  $(".active_selectbox_domains").length;
    $(".active_selectbox_domains").each( function( index, el ) {

        if (index === totalcount - 1) {
            selids = selids+el.id;
            selNames = selNames+$(this).text();
        }else{
            selids = selids+el.id+",";
            selNames = selNames+$(this).text()+",";
        }
    });
    $("#domainsselected").val(totalcount+" Selected");
    $("#domains").val(selids);
    unitview();
}

//retrive unit with condition form autocomplete value
function onUnitSuccess(val){
  $("#seatingunitval").val(val[1]);
  $("#seatingunit").val(val[0]);
  clearMessage();
}

//load unit with conditionform list in autocomplete text box
$("#seatingunitval").keyup(function(){
    var textval = $(this).val();
    if($("#usertype option:selected").val() == "")
    {
        displayMessage(message.usertype_required);
        return false;
    }
    //getUnitNoConditionAutocomplete(textval, unitList, function(val){
    getUnitAutocomplete(textval, unitList, function(val){
        onUnitSuccess(val)
    })
});

//retrive usergroup autocomplete value
function onUserGroupSuccess(val){
  $("#usergroupval").val(val[1]);
  $("#usergroup").val(val[0]);
}

//load usergroup list in autocomplete text box
$("#usergroupval").keyup(function(){
  var textval = $(this).val();
  getUserGroupAutocomplete(textval, userGroupsList, function(val){
    onUserGroupSuccess(val)
  })
});

//service provider====================================================================================

function hidemenuserviceprovider(){
    document.getElementById('serviceproviderview').style.display = 'none';
}
//load usergroup list in autocomplete text box
function loadauto_serviceprovider (textval) {
  document.getElementById('serviceproviderview').style.display = 'block';
  var serviceprovider = serviceProviderList;
  var suggestions = [];
  $('#serviceproviderview ul').empty();
  if(textval.length>0){
    for(var i in serviceprovider){
        if(serviceprovider[i]["is_active"] == true){
            if (~serviceprovider[i]["service_provider_name"].toLowerCase().indexOf(textval.toLowerCase())) suggestions.push([serviceprovider[i]["service_provider_id"],serviceprovider[i]["service_provider_name"]]);
        }
    }
    var str='';
    for(var i in suggestions){
        str += '<li id="'+suggestions[i][0]+'"onclick="activate_text_sp(this,\''+suggestions[i][0]+'\',\''+suggestions[i][1]+'\')">'+suggestions[i][1]+'</li>';
    }
    $('#serviceproviderview ul').append(str);
    $("#serviceprovider").val('');
    }
}
//set selected autocomplte value to textbox
function activate_text_sp (element,checkval,checkname) {
  $("#serviceproviderval").val(checkname);
  $("#serviceprovider").val(checkval);
}

$("#search-units").keyup(function() {
    var count = 0;
    var value = this.value.toLowerCase();
    $("#unitList ul").find("li").each(function(index) {
        if (index === 0) return;
        var id = $(this).text().toLowerCase();
        $(this).toggle(id.indexOf(value) !== -1);;
    });
});

$(function() {
    initialize();
});
$(document).find('.js-filtertable').each(function(){
    $(this).filtertable().addFilter('.js-filter');
});

$( document ).tooltip({
    position: {
        my: "center bottom-20",
        at: "center top",
        using: function( position, feedback ) {
            $( this ).css( position );
            $( "<div>" )
                .addClass( "arrow" )
                .addClass( feedback.vertical )
                .addClass( feedback.horizontal )
                .appendTo( this );
        }
    }
});
