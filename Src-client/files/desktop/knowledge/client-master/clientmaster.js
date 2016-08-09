var userList;
var domainsList;
var countriesList;
var dateconfigList;
var uploadFile = [];
var logo_file;
var countriesListequal = null;
var clientcountriesList = null;
var clientdomainList = null;
var clientdata = null;
var usercountryids = null;
var userdomainids = null;

function clearMessage() {
    $(".error-message").hide();
    $(".error-message").text("");
}
function displayMessage(message) {
    $(".error-message").text(message);
    $(".error-message").show();
    hideLoader();
}
function displayLoader() {
    $(".loading-indicator-spin").show();
}
function hideLoader() {
    $(".loading-indicator-spin").hide();
}
$(".btn-clientgroup-add").click(function(){
    $("#clientgroup-view").hide();
    $("#clientgroup-add").show();
    $("#clientgroup-name").focus();

    function onSuccess(data){
        clearMessage();

        userList = data["users"];
        domainsList = data["domains"];
        countriesList = data["countries"];
        clientcountriesList = data["client_countries"];
        clientdomainList = data["client_domains"];

        $("#clientgroup-name").val('');
        $("#clientgroup-id").val('');
        $("#short-name").removeAttr("readonly");
        $("#upload-logo-img").hide();
        $(".shorturl").text('');
        $("#subscribe-sms").prop("checked", "false");
        $("#subscribe-sms").removeProp('checked');

        var x=document.getElementsByTagName("input");
        for(i = 0; i<=x.length-1; i++){
           if(x.item(i).type!="submit" ){ x.item(i).value = ""; }
        }

        $("#username").show();
        $("#labelusername").text('');

        loadautocountry();
        loadauto();
        loadAutoUsers();
        hidemenu();
        $('.tbody-dateconfiguration-list').empty();
    }
    function onFailure(error){
        displayMessage(error);
    }
    mirror.getClientGroups(
        function (error, response) {
            if (error == null){
                onSuccess(response);
            }
            else {
                onFailure(error);
            }
        }
    );


});
$("#btn-clientgroup-cancel").click(function(){
    clearMessage();
    $("#clientgroup-add").hide();
    $("#clientgroup-view").show();
    var x=document.getElementsByTagName("input");
    for(i = 0; i<=x.length-1; i++){
       if(x.item(i).type!="submit" ){ x.item(i).value = ""; }
    }
    loadClientGroupList(clientdata);
});
function initialize(){
    var x=document.getElementsByTagName("input");
    for(i = 0; i<=x.length-1; i++){
       if(x.item(i).type!="submit" ){ x.item(i).value = ""; }
    }
    hideLoader();
    function onSuccess(data){
        clientdata = data['client_list'];
        loadClientGroupList(data['client_list']);
    }
    function onFailure(error){
        custom_alert(error);
    }
    mirror.getClientGroups(
        function (error, response) {
            if (error == null){
                onSuccess(response);
            }
            else {
                onFailure(error);
            }
        }
    );
}


function loadClientGroupList(clientGroupList){
    $(".tbody-clientgroup-list").find("tr").remove();
    var sno = 0;
    $.each(clientGroupList, function(key, value) {
        var clientId = value["client_id"];
        var isActive = value["is_active"];

        var passStatus = null;
        var classValue = null;

        if(isActive == true) {
          passStatus = false;
          classValue = "active-icon";
        }
        else {
          passStatus=true;
          classValue = "inactive-icon";
        }

        var tableRow = $('#templates .table-clientgroup-list .table-row');
        var clone = tableRow.clone();
        sno = sno + 1;
        $('.sno', clone).text(sno);
        $('.clientgroup-name', clone).text(value["client_name"]);

        $('.edit-icon').attr('title', 'Edit');
        $(".edit-icon", clone).on("click", function() {
            clientgroup_edit(clientId);
        });

        $(".status", clone).addClass(classValue);
        $('.active-icon').attr('title', 'Deactivate');
        $('.inactive-icon').attr('title', 'Activate');
        $(".status", clone).on("click", function() {
            clientgroup_active(clientId, passStatus);
        });

        $('.tbody-clientgroup-list').append(clone);
    });
}

function dataconfigurationvalidate(){
    var flag = 0;
    $(".tbody-dateconfiguration-list .tl-from").each(function(){
        if ($(this).val() == "") {
            flag = 1;
        }
    });
    $(".tbody-dateconfiguration-list .tl-to").each(function(){
        if ($(this).val() == "") {
            flag = 1;
        }
    });
    return flag;
}

function convert_date (data){
  var date = data.split("-");
  var months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun','Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
  for(var j=0;j<months.length;j++){
      if(date[1]==months[j]){
           date[1]=months.indexOf(months[j])+1;
       }
  }
  if(date[1]<10){
      date[1]='0'+date[1];
  }
  return new Date(date[2], date[1]-1, date[0]);
}

$("#btn-clientgroup-submit").click(function(){
    var checkLength = clientMasterValidate();
    if(checkLength){
        var dateConfigurations = [];
        var countryList = $('#country').val();
        var domainsList = $('#domain').val();
        if(countryList != '' && domainsList != ''){
            if(countryList != ''){
                var arrayCountries = countryList.split(",");
                if(domainsList != ''){
                    var arrayDomains = domainsList.split(",");
                }
                for(var ccount = 0;ccount < arrayCountries.length; ccount++){
                    for(var dcount = 0;dcount < arrayDomains.length; dcount++){
                        var configuration;
                        configuration = mirror.getDateConfigurations(
                            parseInt(arrayCountries[ccount]), parseInt(arrayDomains[dcount]),
                            parseInt($(".tl-from-"+arrayCountries[ccount]+"-"+arrayDomains[dcount]).val()),
                            parseInt($(".tl-to-"+arrayCountries[ccount]+"-"+arrayDomains[dcount]).val())
                        );
                        dateConfigurations.push(configuration);
                    }
                }
            }
        }
        var clientGroupIdVal = $("#clientgroup-id").val();
        var clientGroupNameVal = $("#clientgroup-name").val().trim();
        var arrayCountriesVal = $("#country").val().split(",");
        var arrayCountries = [];
        for(var i = 0; i < arrayCountriesVal.length; i++){ arrayCountries[i] = parseInt(arrayCountriesVal[i]); }
        var countriesVal = arrayCountries;
        var arrayDomainsVal = $("#domain").val().split(",");
        var arrayDomains = [];
        for(var j = 0; j < arrayDomainsVal.length; j++){ arrayDomains[j] = parseInt(arrayDomainsVal[j]); }
        var domainsVal = arrayDomains;
        var contractFromVal = $("#contract-from").val().trim();
        var contractToVal = $("#contract-to").val().trim();
        var usernameVal = $("#username").val().trim();
        var uploadLogoVal = $("#upload-logo").val().trim();
        var licenceVal =$("#no-of-user-licence").val().trim();
        var fileSpaceVal = $("#file-space").val().trim();
        var inchargePersonVal = $("#users").val().trim();
        //var subscribeSmsVal = $("#subscribe-sms").val();
        if ($('#subscribe-sms').is(":checked")){
            var subscribeSmsVal = true;
        }
        else{
            var subscribeSmsVal = false;
        }
        var shortname = $("#short-name").val().trim();

        var d = new Date();
        var month = d.getMonth()+1;
        var day = d.getDate();
        var output = d.getFullYear() + '/' + month + '/' + day;
        var currentDate = new Date(output);
        var convertDate = null;

        if(contractToVal != ''){
          convertDate = convert_date(contractToVal);
        }
        if(clientGroupNameVal == ''){
            displayMessage(message.group_required);
        }
        else if(clientGroupNameVal.length > 50){
            displayMessage(message.group_50);
        }
        else if(countryList == ''){
            displayMessage(message.country_required);
        }
        else if(domainsList == ''){
            displayMessage(message.domain_required);
        }
        else if(contractFromVal == ''){
            displayMessage(message.contractfrom_required);
        }
        else if(contractToVal == ''){
            displayMessage(message.contractto_required);
        }
        else if (convertDate != null && convertDate < currentDate) {
            displayMessage(message.invalid_contractto);
        }
        else if(usernameVal == '' && clientGroupIdVal == ''){
            displayMessage(message.username_required);
        }
        else if(validateEmail(usernameVal) == ''){
            displayMessage(message.username_invalid);
        }
        else if(licenceVal == ''){
            displayMessage(message.licence_required);
        }
        else if(licenceVal == "0" || licenceVal == "1"){
            displayMessage(message.licence_invalid);
        }
        else if(isNaN(licenceVal)){
            displayMessage(message.licence_invalid);
        }
        else if(licenceVal.length > 3){
            displayMessage(message.licence_max3);
        }
        else if(fileSpaceVal == ''){
            displayMessage(message.filespace_required);
        }
        else if(fileSpaceVal == '0'){
            displayMessage(message.filespace_invalid);
        }
        else if(!$.isNumeric(fileSpaceVal)){
            displayMessage(message.filespace_invalid);
        }
        else if(fileSpaceVal.length > 3){
            displayMessage(message.filespace_max3);
        }
        else if(inchargePersonVal == ''){
            displayMessage(message.inchargeperson_required);
        }
        else if(shortname == ''){
            displayMessage(message.shortname_required);
            gototop();
        }
        else if(dataconfigurationvalidate() == 1){
            displayMessage(message.dateconfig_required);
        }
        else if(clientGroupIdVal == ''){
            var arrayinchargePersonVal = inchargePersonVal.split(",");
            var arrayinchargePerson = [];
            for(var k = 0; k < arrayinchargePersonVal.length; k++) { arrayinchargePerson[k] = parseInt(arrayinchargePersonVal[k]); }
            inchargePersonVal = arrayinchargePerson;
            if($("#upload-logo").val() == ''){
                displayMessage(message.logo_required);
                return false;
            }
            var ext = $('#upload-logo').val().split('.').pop().toLowerCase();
            if($.inArray(ext, ['gif','png','jpg','jpeg']) == -1) {
                displayMessage(message.logo_invalid);
            }

            function onSuccess(data){
                hideLoader();
                $("#clientgroup-add").hide();
                $("#clientgroup-view").show();
                initialize();
            }
            function onFailure(error){
                hideLoader();
                if(error == 'GroupNameAlreadyExists'){
                    displayMessage(message.groupname_exists);
                }
                else if(error == 'UsernameAlreadyExists'){
                    displayMessage(message.username_exists);
                }
                else if(error == 'ClientCreationFailed'){
                    displayMessage(message.client_creation_failed);
                }
                else if(error == "NotAnImageFile"){
                    displayMessage(message.logo_invalid);
                }
                else if(error == "ServerIsFull"){
                    displayMessage(message.server_full);
                }
                else{
                    displayMessage(error);
                }

            }

            var clientGroupDetails = mirror.getSaveClientGroupDict(
                clientGroupNameVal, countriesVal, domainsVal, logo_file,
                contractFromVal, contractToVal, inchargePersonVal,  parseInt(licenceVal),
                parseFloat(Number(fileSpaceVal*100/100)), subscribeSmsVal,
                usernameVal, dateConfigurations, shortname);
            displayLoader();
            mirror.saveClientGroup(clientGroupDetails,
                function (error, response) {
                    if (error == null){
                        onSuccess(response);
                    }
                    else {
                        onFailure(error);
                    }
                }
            );
        }
        else if(clientGroupIdVal!=''){
            var arrayinchargePersonVal = inchargePersonVal.split(",");
            var arrayinchargePerson = [];
            for(var k = 0; k < arrayinchargePersonVal.length; k++) { arrayinchargePerson[k] = parseInt(arrayinchargePersonVal[k]); }
            inchargePersonVal = arrayinchargePerson;
            if($("#upload-logo").val() == ''){
                logo_file = null;
            }
            if($("#upload-logo").val() != ''){
                var ext = $('#upload-logo').val().split('.').pop().toLowerCase();
                if($.inArray(ext, ['gif','png','jpg','jpeg']) == -1) {
                    displayMessage(message.logo_invalid);
                    return false;
                }
            }
            function onUpdateSuccess(data){
                $("#clientgroup-add").hide();
                $("#clientgroup-view").show();
                initialize();
            }
            function onUpdateFailure(error){
                if(error == 'GroupNameAlreadyExists'){
                    displayMessage(message.groupname_exists);
                }
                else if(error == 'UsernameAlreadyExists'){
                    displayMessage(message.username_exists);
                }
                else if(error == 'CannotDeactivateCountry'){
                    displayMessage(message.cannot_unselect_country);
                }
                else if(error == 'CannotDeactivateDomain'){
                    displayMessage(message.cannot_unselect_domain);
                }
                else if(error == 'InvalidNoOfLicence'){
                    displayMessage(message.invalid_no_of_licence);
                }
                else if(error == 'InvalidFileSpace'){
                    displayMessage(message.invalid_file_space);
                }
                else if(error == 'ServerIsFull'){
                    displayMessage(message.server_full);
                }
                else{
                    displayMessage(error);
                }
            }
            var clientGroupDetails = mirror.getUpdateClientGroupDict(
                parseInt(clientGroupIdVal), clientGroupNameVal, countriesVal, domainsVal, logo_file,
                contractFromVal, contractToVal,inchargePersonVal, parseInt(licenceVal),
                parseFloat(Number(fileSpaceVal*100/100)), subscribeSmsVal, dateConfigurations);

            mirror.updateClientGroup( clientGroupDetails,
                function (error, response) {
                    if (error == null){
                        onUpdateSuccess(response);
                    }
                    else {
                        onUpdateFailure(error);
                    }
                }
            );
        }
        else{
            console.log("all fails");
        }

    }
});
function validateEmail($email) {
    var emailReg = /^([\w-\.]+@([\w-]+\.)+[\w-]{2,4})?$/;
    return emailReg.test( $email );
}

function clientgroup_active(clientId, isActive){

    var msgstatus = message.deactive_message;
    if(isActive){
        msgstatus = message.active_message;
    }
    $( ".warning-confirm" ).dialog({
        title: message.title_status_change,
        buttons: {
            Ok: function() {
                $( this ).dialog( "close" );

                $("#clientgroup-id").val(clientId);
                function onSuccess(data){
                  initialize();
                }
                function onFailure(error){
                    if(error == "CannotDeactivateClient"){
                        custom_alert(message.cannot_deactivate_client);
                    }
                    else{
                        custom_alert(error);
                    }
                }
                mirror.changeClientGroupStatus( parseInt(clientId), isActive,
                    function (error, response){
                        if(error == null){
                            onSuccess(response);
                        }
                        else{
                            onFailure(error);
                        }
                    }
                );
            },
            Cancel: function() {
                $( this ).dialog( "close" );
            }
        },
        open: function ()  {
            $(".warning-message").html(msgstatus);
        }
    });
}
function clientgroup_edit(clientGroupId){
    clearMessage();
    $("#clientgroup-view").hide();
    $("#clientgroup-add").show();
    $("#clientgroup-id").val(clientGroupId);
    function onSuccess(data){
        countriesList = '';
        clientcountriesList = '';
        countriesListequal = '';
        userList = data["users"];
        domainsList = data["domains"];
        countriesList = data["countries"];
        clientcountriesList = data["client_countries"];
        clientdomainList = data["client_domains"];
        countriesListequal = data["countries"];
        loadFormListUpdate(data['client_list'], clientGroupId);
    }
    function onFailure(error){
        displayMessage(error);
    }
    mirror.getClientGroups(
        function (error, response){
            if(error == null){
                onSuccess(response);
            }
            else{
                onFailure(error);
            }
        });
}
function loadFormListUpdate(clientListData, clientGroupId){
    $("#upload-logo-img").show();
    for(clientList in clientListData){
        if(clientGroupId == clientListData[clientList]['client_id']){
            $("#clientgroup-name").val(clientListData[clientList]['client_name']);
            var countriesListArray = clientListData[clientList]['country_ids'];
            // var totalCountriesArray = countriesListArray
            // $.each(countriesList, function (key, value){
            //     totalCountriesArray.push(value['country_id']);
            // });
            // console.log("totalCountriesArray:"+totalCountriesArray);
            $("#country").val(countriesListArray);
            $("#countryselected").val(countriesListArray.length+" Selected");

            var domainsListArray = clientListData[clientList]['domain_ids'];
            $("#domain").val(domainsListArray);
            $("#domainselected").val(domainsListArray.length+" Selected");

            $("#contract-from").val(clientListData[clientList]['contract_from']);
            $("#contract-to").val(clientListData[clientList]['contract_to']);
            $("#username").val(clientListData[clientList]['username']);
            $("#username").hide();
            $("#labelusername").text(clientListData[clientList]['username']);
            var logoimgsrc = clientListData[clientList]['logo'];

            $("#upload-logo-img").attr("src", logoimgsrc);

            $("#no-of-user-licence").val(clientListData[clientList]['no_of_user_licence']);
            $("#file-space").val(clientListData[clientList]['total_disk_space']);
            if(clientListData[clientList]['is_sms_subscribed'] == true){
                $('#subscribe-sms').prop("checked", true);
            }
            var userListArray = clientListData[clientList]['incharge_persons'];
            $("#users").val(userListArray);
            $("#usersSelected").val(userListArray.length+" Selected");
            $("#short-name").val(clientListData[clientList]['short_name']);
            $("#short-name").attr("readonly", "true");
            $(".shorturl").text(clientListData[clientList]['short_name']);
            dateconfigList = clientListData[clientList]['date_configurations'];
        }
    }
    dateConfigurations(dateconfigList);
}

function dateConfigurations(dateconfigList){
    $('.tbody-dateconfiguration-list').empty();
    var countryarr = [];
    var usercountryarr = [];
    var domainarr = [];
    var userdomainarr = [];
    var cl = countryunionclientcountry();
    var dl = domainunionclientdomain();

    var usercl = countriesList;
    var userdl = domainsList;
    $.each(usercl, function(k, val){
         usercountryarr.push(val["country_id"]);
    });
    $.each(userdl, function(k, val){
         userdomainarr.push(val["domain_id"]);
    });
    $.each(cl, function(k, val){
         countryarr.push(val["country_id"]);
    });
    $.each(dl, function(k, val){
         domainarr.push(val["domain_id"]);
    });

    var countriesValue = $('#country').val();
    var domainsValue = $('#domain').val();
    if(countriesValue != '' && domainsValue != ''){
        if(countriesValue != ''){
            var arrayCountries = countriesValue.split(",");
            if(domainsValue != ''){
                var arrayDomains = domainsValue.split(",");
            }
            for(var ccount = 0; ccount < arrayCountries.length; ccount++){
                var tableRow = $('#templates .table-dconfig-list .table-dconfig-countries-row');
                var clone = tableRow.clone();
                $('.inputCountry', clone).val(arrayCountries[ccount]);
                $('.dconfig-country-name', clone).text(getClientCountriesNameunion(arrayCountries[ccount]));
                $('.dconfig-country-name', clone).addClass("heading");
                $('.tbody-dateconfiguration-list').append(clone);

                for(var dcount = 0;dcount < arrayDomains.length; dcount++){
                    var tableRowDomains = $('#templates .table-dconfig-list .table-dconfig-domain-row');
                    var clone1 = tableRowDomains.clone();
                    $('.inputDomain', clone1).val(arrayDomains[dcount]);
                    $('.dconfig-domain-name', clone1).text(getdomainunionclientdomainname(arrayDomains[dcount]));
                    $('.tl-from', clone1).addClass('tl-from-'+arrayCountries[ccount]+'-'+arrayDomains[dcount]);
                    $('.tl-to', clone1).addClass('tl-to-'+arrayCountries[ccount]+'-'+arrayDomains[dcount]);
                    $('.tbody-dateconfiguration-list').append(clone1);
                    $('.tl-from-'+arrayCountries[ccount]+'-'+arrayDomains[dcount]).attr('disabled', true);
                    $('.tl-to-'+arrayCountries[ccount]+'-'+arrayDomains[dcount]).attr('disabled', true);
                }
            }
        }
    }
    $.each(dateconfigList, function (key, value){
        var fromMonth = dateconfigList[key]['period_from'];
        var toMonth = dateconfigList[key]['period_to'];
        var countryIdDateConfig = dateconfigList[key]['country_id'];
        var domainIdDateConfig = dateconfigList[key]['domain_id'];
        $(".tl-from-"+countryIdDateConfig+"-"+domainIdDateConfig+" [value="+fromMonth+"]" ).prop("selected", true);
        $(".tl-to-"+countryIdDateConfig+"-"+domainIdDateConfig+" [value="+toMonth+"]" ).prop("selected", true);
    });
    for(var c = 0; c < countryarr.length; c++ ){
        for(var d = 0; d < domainarr.length; d++ ){
            if($.inArray(countryarr[c], usercountryarr) != -1 && $.inArray(domainarr[d], userdomainarr) != -1){
                $('.tl-from-'+countryarr[c]+'-'+domainarr[d]).attr('disabled', false);
                $('.tl-to-'+countryarr[c]+'-'+domainarr[d]).attr('disabled', false);
            }
        }
    }
}
function getCountriesName(countryId){
    var countryName;
    $.each(countriesList, function (key, value){
        if(value['country_id'] == countryId){
            countryName = value['country_name'];
            return false;
        }
    });
    return countryName;
}
function getDomainName(doaminId){
    var domainName;
    $.each(domainsList, function (key, value){
        if(value['domain_id'] == doaminId){
            domainName = value['domain_name'];
            return false;
        }
    });
    return domainName;
}
function getClientCountriesName(countryId){
    var countryName;
    $.each(clientcountriesList, function (key, value){
        if(value['country_id'] == countryId){
            countryName = value['country_name'];
            return false;
        }
    });
    return countryName;
}
function getClientDomainName(doaminId){
    var domainName;
    $.each(clientdomainList, function (key, value){
        if(value['domain_id'] == doaminId){
            domainName = value['domain_name'];
            return false;
        }
    });
    return domainName;
}
$("#upload-logo").on("change", function(e) {
    mirror.uploadFile(e, function result_data(data) {
        if(data != 'File max limit exceeded' || data != 'File content is empty'){
            uploadFile = data;
            logo_file = data
        }
        else{
          custom_alert(data);
        }
     });
});
// $("#search-clientgroup-name").keyup(function() {
//     var count = 0;
//     var value = this.value.toLowerCase();
//     $("table").find("tr:not(:first)").each(function(index) {
//         if (index === 0) return;
//         var id = $(this).find(".clientgroup-name").text().toLowerCase();
//         $(this).toggle(id.indexOf(value) !== -1);;
//     });
// });

//Autocomplete Script Starts and Hide list items after select

var chosen_clientmaster = "";

function onArrowKeyUser(e, ac_item){
  if (e.keyCode != 40 && e.keyCode != 38 && e.keyCode != 32) {
    chosen_clientmaster = "";
  }
  if (e.keyCode == 40) {
      if(chosen_clientmaster === "") {
          chosen_clientmaster = 0;
      } else if((chosen_clientmaster+1) < $('#' + ac_item + ' li').length) {
          chosen_clientmaster++;
      }
      $('#' + ac_item + ' li').removeClass('auto-selected');
      $('#' + ac_item + ' li:eq('+chosen_clientmaster+')').addClass('auto-selected');

      return false;
  }
  if (e.keyCode == 38) {
      if(chosen_clientmaster === "") {
          chosen_clientmaster = 0;
      } else if(chosen_clientmaster > 0) {
          chosen_clientmaster--;
      }
      $('#' + ac_item + ' li').removeClass('auto-selected');
      $('#' + ac_item + ' li:eq('+chosen_clientmaster+')').addClass('auto-selected');
      return false;
  }
  if (e.keyCode == 32) {
    $('#' + ac_item + ' li:eq('+chosen_clientmaster+')').removeClass('auto-selected');
    var ms_id = $('#' + ac_item + ' li:eq('+chosen_clientmaster+')').attr('id');
    var chkstatus = $('#' + ac_item + ' li:eq('+chosen_clientmaster+')').attr('class');

    if(ac_item == 'ulist'){
        if(chkstatus == 'active_selectbox'){
            $('#' + ac_item + ' li:eq('+chosen_clientmaster+')').removeClass("active_selectbox");
        }else{
            $('#' + ac_item + ' li:eq('+chosen_clientmaster+')').addClass("active_selectbox");
        }
        activate_domain();
    }else if(ac_item == 'ulist-country'){
        if(chkstatus == 'active_selectbox_country'){
            $('#' + ac_item + ' li:eq('+chosen_clientmaster+')').removeClass("active_selectbox_country");
        }else{
            $('#' + ac_item + ' li:eq('+chosen_clientmaster+')').addClass("active_selectbox_country");
        }
        activateCountry_country();
    }else{
        if(chkstatus == 'active_selectbox_users'){
            $('#' + ac_item + ' li:eq('+chosen_clientmaster+')').removeClass("active_selectbox_users");
        }else{
            $('#' + ac_item + ' li:eq('+chosen_clientmaster+')').addClass("active_selectbox_users");
        }
        activateUsers_user();
    }
    return false;
  }
}

function hidemenu() {
    chosen_clientmaster = "";
    document.getElementById('selectboxview').style.display = 'none';
    document.getElementById('selectboxview-country').style.display = 'none';
    document.getElementById('selectboxview-users').style.display = 'none';
}

/*$(".icon-autocomplete").focusout(function(){
    chosen_clientmaster = "";
    $("#selectboxview").hide();
    $("#selectboxview-country").hide();
    $("#selectboxview-users").hide();
});*/

$("#domainselected").keyup(function(e){
    onArrowKeyUser(e, 'ulist')
});

$("#countryselected").keyup(function(e){
    onArrowKeyUser(e, 'ulist-country')
});

$("#usersSelected").keyup(function(e){
    onArrowKeyUser(e, 'ulist-user')
});

//load domain list in multi select box
function loadauto() {
    document.getElementById('selectboxview').style.display = 'block';
    var editdomainval = [];
    if($("#domain").val() != ''){
        editdomainval = $("#domain").val().split(",");
    }
//if($("#domainselected").val() == ''){
    if($("#clientgroup-id").val() == ''){
        var domains = domainsList;
    }
    if($("#clientgroup-id").val() != ''){
        var domains = domainunionclientdomain();
    }

    $('#ulist').empty();
    var str = '';
    for(var i in domains){
        var selectdomainstatus='';
        for(var j = 0; j < editdomainval.length; j++){
            if(editdomainval[j] == domains[i]["domain_id"]){
                selectdomainstatus = 'checked';
            }
        }
        var domainId = parseInt(domains[i]["domain_id"]);
        var domainName = domains[i]["domain_name"];

        var ccdd =checkclientdomain(domainId);
        var cdd = checkdomain(domainId);

        if(ccdd == 1 && cdd == 1){
            if(selectdomainstatus == 'checked'){
                str += '<li id = "'+domainId+'" class="active_selectbox" onclick="activate(this)" >'+domainName+'</li> ';
            }else{
               str += '<li id="'+domainId+'" onclick="activate(this)" >'+domainName+'</li> ';
            }
        }
        else if(ccdd != 1 && cdd == 1){
            str += '<li id="'+domainId+'" onclick="activate(this)" >'+domainName+'</li> ';

        }
        else if(ccdd == 1 && cdd != 1){
            if(selectdomainstatus == 'checked'){
                str += '<li id="'+domainId+'" class="active_selectbox deactivate" >'+domainName+'</li> ';
            }
            else{
                str += '<li id="'+domainId+'" class="deactivate" >'+domainName+'</li> ';
            }
        }

    }
  $('#ulist').append(str);
  $("#domainselected").val(editdomainval.length+" Selected")
 // }
}
//check & uncheck process

function activate_domain(){
    var selIds='';
    var selNames='';
    var totalCount =  $(".active_selectbox").length;
    $(".active_selectbox").each( function( index, el ) {
        if (index === totalCount - 1) {
            selIds = selIds + el.id;
            selNames = selNames + $(this).text();
        }else{
            selIds = selIds + el.id+",";
            selNames = selNames + $(this).text() + ",";
        }
    });
    $("#domainselected").val(totalCount+" Selected");
    $("#domain").val(selIds);
    $("#domainNames").val(selNames);
    if($("#clientgroup-id").val() == ''){
        dateconfig();
    }
    else{
        dateConfigurations(dateconfigList);
    }
}
function activate(element){
    var chkStatus = $(element).attr('class');
    if(chkStatus == 'active_selectbox'){
        $(element).removeClass("active_selectbox");
    }else{
        $(element).addClass("active_selectbox");
    }
    activate_domain();
}
// function domainunionclientdomains(){
//     var d = domainsList;
//     var cd = clientdomainList;
//     var result = {};

//     for(var key in d) result[key] = d[key];
//     for(var key in cd) result[key] = cd[key];

//     var finalObj = $.extend(result, d, cd);
//     return finalObj;
// }
function checkingcountry(countryid){
    var returnval = null;
    $.each(countriesListequal, function(key, value){
        if(value['country_id'] == countryid){
            returnval = 1;
        }
    });
    return returnval;
}
function getClientCountriesNameunion(countryid){
    var c = '';
    var cc = '';
    var ccnew = '';
    var editcountryval = [];
    var countryname;

    c = countriesList;
    cc = clientcountriesList;

    if($("#country").val() != ''){
        editcountryval = $("#country").val().split(",");
    }

    var result = {};
    ccnew = [];
    var arrayCountries = [];
    for(var i = 0; i < editcountryval.length; i++){ arrayCountries[i] = parseInt(editcountryval[i]); }

    $.each(cc, function(key){
        if($.inArray(cc[key]['country_id'], arrayCountries) != -1){
            ccnew[key] = cc[key];
        }
    });
    var finalObj1 = [];

    finalObj1 = c.concat(ccnew);
    var dupes = {};
    var finalObj = [];
    if(finalObj1.length != 0){
        $.each(finalObj1, function(i, el) {
            if(el != null){
                if (!dupes[el['country_id']]) {
                    dupes[el['country_id']] = true;
                    finalObj.push(el);
                }
            }
        });
    }

    $.each(finalObj, function(key, val){
        if(val['country_id'] == countryid){
            countryname = val['country_name'];
        }
    });
    return countryname;
}

function countryunionclientcountry(){
    var c = '';
    var cc = '';
    var ccnew = '';
    var editcountryval = [];

    c = countriesList;
    cc = clientcountriesList;

    if($("#country").val() != ''){
        editcountryval = $("#country").val().split(",");
    }

    var result = {};
    ccnew = [];
    var arrayCountries = [];
    for(var i = 0; i < editcountryval.length; i++){ arrayCountries[i] = parseInt(editcountryval[i]); }

    $.each(cc, function(key){
        if($.inArray(cc[key]['country_id'], arrayCountries) != -1){
            ccnew[key] = cc[key];
        }
    });
    var finalObj1 = [];

    finalObj1 = c.concat(ccnew);
    var dupes = {};
    var finalObj = [];
    if(finalObj1.length != 0){
        $.each(finalObj1, function(i, el) {
            if(el != null){
                if (!dupes[el['country_id']]) {
                    dupes[el['country_id']] = true;
                    finalObj.push(el);
                }
            }
        });
    }
    return finalObj;
}
function domainunionclientdomain(){
    var d = '';
    var cd = '';
    var cdnew = '';
    var editdomainval = [];

    d = domainsList;
    cd = clientdomainList;

    if($("#domains").val() != ''){
        editdomainval = $("#domain").val().split(",");
    }

    var result = {};
    cdnew = [];
    var arrayDomains = [];
    for(var i = 0; i < editdomainval.length; i++){ arrayDomains[i] = parseInt(editdomainval[i]); }

    $.each(cd, function(key){
        if($.inArray(cd[key]['domain_id'], arrayDomains) != -1){
            cdnew[key] = cd[key];
        }
    });
    var finalObj1 = [];

    finalObj1 = d.concat(cdnew);

    var dupes = {};
    var finalObj = [];
    if(finalObj1.length != 0){
        $.each(finalObj1, function(i, el) {
            if(el != null){
                if (!dupes[el['domain_id']]) {
                    dupes[el['domain_id']] = true;
                    finalObj.push(el);
                }
            }
        });
    }
    return finalObj;
}
function getdomainunionclientdomainname(domainid){
    var d = '';
    var cd = '';
    var cdnew = '';
    var editdomainval = [];
    var domainname = '';

    d = domainsList;
    cd = clientdomainList;

    if($("#domains").val() != ''){
        editdomainval = $("#domain").val().split(",");
    }

    var result = {};
    cdnew = [];
    var arrayDomains = [];
    for(var i = 0; i < editdomainval.length; i++){ arrayDomains[i] = parseInt(editdomainval[i]); }

    $.each(cd, function(key){
        if($.inArray(cd[key]['domain_id'], arrayDomains) != -1){
            cdnew[key] = cd[key];
        }
    });
    var finalObj1 = [];

    finalObj1 = d.concat(cdnew);

    var dupes = {};
    var finalObj = [];

    $.each(finalObj1, function(i, el) {
        if(el != null){
            if (!dupes[el['domain_id']]) {
                dupes[el['domain_id']] = true;
                finalObj.push(el);
            }
        }
    });
    $.each(finalObj, function(key, val){
        if(val['domain_id'] == domainid){
            domainname = val['domain_name'];
        }
    });
    return domainname;
}

function checkclientcountry(countryid){
    var returnval = null;
    var arrayCountries = [];
    var editcountryval;
    editcountryval = $("#country").val().split(",");
    for(var i = 0; i < editcountryval.length; i++){ arrayCountries[i] = parseInt(editcountryval[i]); }
    if($.inArray(countryid, arrayCountries) != -1){
        returnval = 1;
    }
    return returnval;
}


function checkclientdomain(domainid){
    var returnval = null;
    var arrayDomains = [];
    var editdomainval;
    editdomainval = $("#domain").val().split(",");
    for(var i = 0; i < editdomainval.length; i++){ arrayDomains[i] = parseInt(editdomainval[i]); }
    if($.inArray(domainid, arrayDomains) != -1){
        returnval = 1;
    }
    return returnval;
}

function checkdomain(domainid){
    var returnval = null;
    $.each(domainsList, function(key, value){
        if(value['domain_id'] == domainid){
            returnval = 1;
        }
    });
    return returnval;
}
// function unioncountryids(){
//     var c = [];
//     var cc = [];
//     var concatArraysUniqueWithSort = function (thisArray, otherArray) {
//         var newArray = thisArray.concat(otherArray).sort(function (a, b) {
//             return a > b ? 1 : a < b ? -1 : 0;
//         });

//         return newArray.filter(function (item, index) {
//             return newArray.indexOf(item) === index;
//         });
//     };
//     $.each(clientcountriesList, function(key, value){
//         cc.push(value['country_id']);
//     });
//     $.each(countriesList, function(key, value){
//         c.push(value['country_id']);
//     });
//     return concatArraysUniqueWithSort(c, cc);
// }

function loadautocountry() {
    document.getElementById('selectboxview-country').style.display = 'block';
    var editcountryval = [];
    if($("#country").val() != ''){
        editcountryval = $("#country").val().split(",");
    }

    if($("#clientgroup-id").val().trim() == ""){
        var countries = countriesList;
        $('#ulist-country').empty();
        var str = '';
        for(var i in countries){
            selectcountrystatus = '';
            for(var j = 0; j < editcountryval.length; j++){
                if(editcountryval[j] ==  countries[i]["country_id"]){
                    selectcountrystatus = 'checked';
                }
            }
            var countryId = parseInt(countries[i]["country_id"]);
            var countryName = countries[i]["country_name"];
            if(selectcountrystatus == 'checked'){
                str += '<li id="'+countryId+'" class="active_selectbox_country" onclick="activateCountry(this)" >'+countryName+'</li> ';
            }
            else{
                str += '<li id="'+countryId+'" onclick="activateCountry(this)" >'+countryName+'</li> ';
            }

        }

    }
    if($("#clientgroup-id").val().trim() != ""){
        var countries = countryunionclientcountry();
        $('#ulist-country').empty();
        var str = '';
        for(var i in countries){
            var selectcountrystatus = '';
            for(var j = 0; j < editcountryval.length; j++){
                if(editcountryval[j] ==  countries[i]["country_id"]){
                    selectcountrystatus = 'checked';
                }
            }
            var countryId = parseInt(countries[i]["country_id"]);
            var countryName = countries[i]["country_name"];

            var cclientc = checkclientcountry(countryId);
            var ccc = checkingcountry(countryId);

            if( cclientc == 1 &&  ccc == 1){
                if(selectcountrystatus == 'checked'){
                   str += '<li id = "'+countryId+'" class="active_selectbox_country" onclick="activateCountry(this)" >'+countryName+'</li> ';
                }else{
                   str += '<li id="'+countryId+'" onclick="activateCountry(this)" >'+countryName+'</li> ';
                }
            }
            else if(cclientc != 1 && ccc == 1){
                str += '<li id="'+countryId+'" onclick="activateCountry(this)" >'+countryName+'</li> ';

            }
            else if(cclientc == 1 && ccc != 1){
                if(selectcountrystatus == 'checked'){
                    str += '<li id="'+countryId+'" class="active_selectbox_country deactivate" >'+countryName+'</li> ';
                }
                else{
                    str += '<li id="'+countryId+'" class="deactivate" >'+countryName+'</li> ';
                }
            }

        }
    }


    $('#ulist-country').append(str);
    $("#countryselected").val(editcountryval.length+" Selected");
}

function activateCountry_country(){
    var selids = '';
    var selNames = '';
    var totalcount =  $(".active_selectbox_country").length;
    $(".active_selectbox_country").each( function( index, el ) {
        if (index === totalcount - 1) {
            selids = selids + el.id;
            selNames = selNames + $(this).text();
        }else{
            selids = selids + el.id + ",";
            selNames = selNames + $(this).text() + ",";
        }
    });
    $("#countryselected").val(totalcount+" Selected");
    $("#country").val(selids);
    $("#countryNames").val(selNames);
    if($("#clientgroup-id").val() == ''){
        dateconfig();
    }
    else{
        dateConfigurations(dateconfigList);
    }
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
    activateCountry_country();
}

function dateconfig(){
    $('.tbody-dateconfiguration-list').empty();
    var countriesvalList = $('#country').val();
    var countriesNamesList = $('#countryNames').val();
    var domainsList = $('#domain').val();
    var domainNamesList = $('#domainNames').val();
    if(countriesvalList != '' && domainsList != ''){
        if(countriesvalList != ''){
            var arrayCountries = countriesvalList.split(",");
            var arrayCountriesName = countriesNamesList.split(",");
            if(domainsList != ''){
                var arrayDomains = domainsList.split(",");
                var arrayDomainName = domainNamesList.split(",");
            }
            for(var ccount = 0;ccount < arrayCountries.length; ccount++){
                var tableRow = $('#templates .table-dconfig-list .table-dconfig-countries-row');
                var clone = tableRow.clone();
                $('.inputCountry', clone).val(arrayCountries[ccount]);
                $('.dconfig-country-name', clone).text(getCountriesName(arrayCountries[ccount]));
                $('.dconfig-country-name', clone).addClass("heading");
                $('.tbody-dateconfiguration-list').append(clone);

                for(var dcount = 0;dcount < arrayDomains.length; dcount++){
                    var tableRowDomains = $('#templates .table-dconfig-list .table-dconfig-domain-row');
                    var clone1 = tableRowDomains.clone();
                    $('.inputDomain', clone1).val(arrayDomains[dcount]);
                    $('.dconfig-domain-name', clone1).text(getDomainName(arrayDomains[dcount]));

                    $('.tl-from', clone1).addClass('tl-from-'+arrayCountries[ccount]+'-'+arrayDomains[dcount]);
                    $('.tl-to', clone1).addClass('tl-to-'+arrayCountries[ccount]+'-'+arrayDomains[dcount]);
                    $('.tbody-dateconfiguration-list').append(clone1);
                }
            }
        }
    }
}

function checkuser(userid, usercountryids, userdomainids){
    var returnval = 0;
    var arrc = [];
    var arrd = [];
    var countryids = $("#country").val();
    var domainids = $("#domain").val();

    for(var mc = 0;  mc <  countryids.length; mc++){
        for(var m = 0;  m < usercountryids.length; m++){
            if(usercountryids[m] == countryids[mc]){
                arrc.push(usercountryids[m]);
            }
        }
    }
    for(var md = 0;  md <  domainids.length; md++){
        for(var n = 0;  n < userdomainids.length; n++){
            if(userdomainids[n] == domainids[md]){
                arrd.push(userdomainids[n]);
            }
        }
    }

    if(arrc.length > 0 && arrd.length >0){
        returnval = 1;
    }
    return returnval;
}

function loadAutoUsers () {
    document.getElementById('selectboxview-users').style.display = 'block';
    var editusersval = [];
    if($("#users").val() != ''){
        editusersval = $("#users").val().split(",");
    }
    var users = userList;
    $('#selectboxview-users ul').empty();
    var str = '';
    for(var i in users){
        if(checkuser(users[i]["user_id"], users[i]["countries"], users[i]["domains"]) == 1){
            var selectUserStatus = '';
            for(var j = 0; j<editusersval.length; j++){
                if(editusersval[j] == users[i]["user_id"]){
                    selectUserStatus = 'checked';
                }
            }
            if(selectUserStatus == 'checked'){
                str += '<li id="'+users[i]["user_id"]+'" class="active_selectbox_users" onclick="activateUsers(this)" >'+users[i]["employee_name"]+'</li> ';
            }else{
                str += '<li id="'+users[i]["user_id"]+'" onclick="activateUsers(this)" >'+users[i]["employee_name"]+'</li> ';
            }
        }

    }
  $('#selectboxview-users ul').append(str);
  $("#usersSelected").val(editusersval.length+" Selected")
}
//check & uncheck process
function activateUsers_user(){
    var selids = '';
    var totalcount =  $(".active_selectbox_users").length;
    $(".active_selectbox_users").each( function( index, el ) {
        if (index === totalcount - 1) {
            selids = selids+el.id;
        }else{
            selids = selids+el.id+",";
        }
    });
    $("#usersSelected").val(totalcount+" Selected");
    $("#users").val(selids);
}
function activateUsers(element){
  var chkstatus = $(element).attr('class');
  if(chkstatus == 'active_selectbox_users'){
        $(element).removeClass("active_selectbox_users");
  }
  else{
    $(element).addClass("active_selectbox_users");
  }
  activateUsers_user();  
}

function gototop(){
    $("html, body").animate({ scrollTop: 0 }, "slow");
}
$(function() {
    initialize();
});
$(document).find('.js-filtertable').each(function(){
    $(this).filtertable().addFilter('.js-filter');
});

$('#clientgroup-name').on('input', function (e) {
    this.value = isCommon($(this));
});

$('#no-of-user-licence').on('input', function (e) {
    this.value = isNumbers($(this));
});

$('#file-space').on('input', function (e) {
    this.value = isNumbers($(this));
});

$('#short-name').on('input', function (e) {
    this.value = isAlphanumeric_Shortname($(this));
});

$("#short-name").on('keyup', function(){
    $(".shorturl").text($(this).val());
});