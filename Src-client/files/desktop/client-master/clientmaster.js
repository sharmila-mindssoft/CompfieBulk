var userList;
var domainsList;
var countriesList;
function clearMessage() {
    $(".error-message").hide();
    $(".error-message").text("");
}
function displayMessage(message) {
    $(".error-message").text(message);
    $(".error-message").show();
}
$(".btn-clientgroup-add").click(function(){
	$("#clientgroup-view").hide();
	$("#clientgroup-add").show();
	$("#clientgroup-name").val('');
 	$("#clientgroup-id").val('');
 	clearMessage();
 	$("#short-name").removeAttr("readonly");
 	$("#upload-logo-img").hide();
 	var x=document.getElementsByTagName("input");
 	for(i = 0; i<=x.length-1; i++){
 		if(x.item(i).type!="submit" ){ x.item(i).value = ""; }
 	}
 	loadautocountry();
 	loadauto();
	loadAutoUsers(); 	
 	hidemenu();
 	$('.tbody-dateconfiguration-list').empty();
	function onSuccess(data){
		userList = data["users"];
		domainsList = data["domains"];
		countriesList = data["countries"];  	
	}	
	function onFailure(error){	
		console.log(error);
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
	$("#clientgroup-add").hide();
	$("#clientgroup-view").show();
});
function initialize(){	
	function onSuccess(data){
		loadClientGroupList(data['client_list']);
	}
	function onFailure(error){	
		console.log(error);
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
	var imageName, title;	
	for(var i in clientGroupList){
		var clientGroups = clientGroupList[i];
		var clientId = clientGroups["client_id"];
		var isActive = clientGroups["is_active"];
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
		var tableRow = $('#templates .table-clientgroup-list .table-row');
		var clone = tableRow.clone();
		sno = sno + 1;
		$('.sno', clone).text(sno);
		$('.clientgroup-name', clone).text(clientGroups["client_name"]);
		$('.edit', clone).html('<img src="/images/icon-edit.png" id="editid" onclick="clientgroup_edit('+clientId+')"/>');
		$('.is-active', clone).html('<img src="/images/'+imageName+'" title="'+title+'" onclick="clientgroup_active('+clientId+', '+statusVal+')"/>');
		$('.tbody-clientgroup-list').append(clone);			
	}
	//$("#total-records").html('Total : '+sno+' records');
}

$("#btn-clientgroup-submit").click(function(){
	var dateConfigurations = [];	
	var countriesList = $('#country').val();
	var domainsList = $('#domain').val();
	if(countriesList != '' && domainsList != ''){
		if(countriesList != ''){ 
			var arrayCountries = countriesList.split(",");
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
	var clientGroupNameVal = $("#clientgroup-name").val();
	var arrayCountriesVal = $("#country").val().split(",");
	var arrayCountries = [];
	for(var i = 0; i < arrayCountriesVal.length; i++){ arrayCountries[i] = parseInt(arrayCountriesVal[i]); } 
	var countriesVal = arrayCountries;
	var arrayDomainsVal = $("#domain").val().split(",");
	var arrayDomains = [];
	for(var j = 0; j < arrayDomainsVal.length; j++){ arrayDomains[j] = parseInt(arrayDomainsVal[j]); } 
	var domainsVal = arrayDomains;
	var contractFromVal = $("#contract-from").val();
	var contractToVal = $("#contract-to").val();	
	var usernameVal = $("#username").val();
	var uploadLogoVal = $("#upload-logo").val();
	var licenceVal = parseInt($("#no-of-user-licence").val());
	var fileSpaceVal = parseFloat(Number($("#file-space").val()*100)/100).toFixed(2);
	
	//var subscribeSmsVal = $("#subscribe-sms").val();
	var arrayinchargePersonVal = $("#users").val().split(",");
	var arrayinchargePerson = [];
	for(var k = 0; k < arrayinchargePersonVal.length; k++) { arrayinchargePerson[k] = parseInt(arrayinchargePersonVal[k]); } 
	var inchargePersonVal = arrayinchargePerson;
	if ($('#subscribe-sms').is(":checked")){
		var subscribeSmsVal = true;	 
	}
	else{ 
		var subscribeSmsVal = false;
	}
	var shortname = $("#short-name").val();
	if(clientGroupNameVal == ''){
		displayMessage('Group Required');
	}
	else if(countriesList == ''){
		displayMessage('Country Required');
	}
	else if(domainsList == ''){
		displayMessage('Domain Required');
	}
	else if(contractFromVal == ''){
		displayMessage('Contract From Required');		
	}
	else if(contractToVal == ''){
		displayMessage('Contract To Required');		
	}
	else if(usernameVal == ''){
		displayMessage('Username Required');		
	}
	else if(validateEmail(usernameVal) == ''){
		displayMessage('Username Invalid Format');		
	}
	else if(licenceVal == ''){
		displayMessage('No. Of User Licence Required');
	}
	else if(isNaN(licenceVal)){
		displayMessage('Invalid No. Of User Licence');
	}
	else if(fileSpaceVal == ''){
		displayMessage('File Space Required');
	}
	else if(!$.isNumeric(fileSpaceVal)){
		displayMessage('File Space Value Invalid');
	}
	else if(inchargePersonVal == ''){
		displayMessage('Incharge Person Required');
	}
	else if(shortname == ''){
		displayMessage('Short Name Required');
		gototop();
	}
	else if(clientGroupIdVal == ''){	
		if(uploadLogoVal == ''){
			displayMessage('Logo Required');	
			return false;	
		}	
		function onSuccess(data){
	    	$("#clientgroup-add").hide();
  			$("#clientgroup-view").show();
  			initialize();
	    }
		function onFailure(error){
			if(error == 'GroupNameAlreadyExists'){
				displayMessage('Group Name Already Exists');	
			}
			if(error == 'UsernameAlreadyExists'){
				displayMessage('Username Already Exists');	
			}
		}
		
		var clientGroupDetails = mirror.getSaveClientGroupDict(
			clientGroupNameVal, countriesVal, domainsVal, uploadLogoVal,
			contractFromVal, contractToVal,inchargePersonVal, licenceVal, 
			parseFloat(Number(fileSpaceVal*100/100)), subscribeSmsVal, 
			usernameVal, dateConfigurations, shortname);
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
		function onSuccess(data){
		    $("#clientgroup-add").hide();
	  		$("#clientgroup-view").show();
	  		initialize();
	    }
		function onFailure(error){
			if(error == 'GroupNameAlreadyExists'){
				displayMessage('Group Name Already Exists');
			}
			if(error == 'UsernameAlreadyExists'){
				displayMessage('Username Already Exists');	
			}
		}
	
		var clientGroupDetails = mirror.getUpdateClientGroupDict(
			clientGroupIdVal, clientGroupNameVal, countriesVal, domainsVal, uploadLogoVal,
			contractFromVal, contractToVal,inchargePersonVal, licenceVal,
			parseFloat(Number(fileSpaceVal*100/100)), subscribeSmsVal,
			 usernameVal, dateConfigurations, shortname);
		mirror.updateClientGroup( clientGroupDetails, 
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
	else{
		console.log("all fails");
	}
});
function validateEmail($email) {
	var emailReg = /^([\w-\.]+@([\w-]+\.)+[\w-]{2,4})?$/;
	return emailReg.test( $email );
}

function clientgroup_active(clientId, isActive){
  	$("#clientgroup-id").val(clientId);
  	function onSuccess(data){
	  initialize();
  	}
  	function onFailure(error){
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
}
function clientgroup_edit(clientGroupId){
	$("#clientgroup-view").hide();
	$("#clientgroup-add").show();
	$("#clientgroup-id").val(clientGroupId);
	function onSuccess(data){
		userList = data["users"];
		domainsList = data["domains"];	
		countriesList = data["countries"];  	
		loadFormListUpdate(data['client_list'],clientGroupId);
	}
	function onFailure(error){
		console.log(error);
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
	var dateconfigList;
	for(clientList in clientListData){
		if(clientGroupId == clientListData[clientList]['client_id']){
			$("#clientgroup-name").val(clientListData[clientList]['client_name']);

			var countriesListArray = clientListData[clientList]['country_ids'];
			$("#country").val(countriesListArray);
			$("#countryselected").val(countriesListArray.length+" Selected");

			var domainsListArray = clientListData[clientList]['domain_ids'];
			$("#domain").val(domainsListArray);
			$("#domainselected").val(domainsListArray.length+" Selected");

			$("#contract-from").val(clientListData[clientList]['contract_from']);
			$("#contract-to").val(clientListData[clientList]['contract_to']);
			$("#username").val(clientListData[clientList]['username']);
			//$("#upload-logo-img").attr("src",clientListData[clientList]['logo']);
			$("#upload-logo-img").show();
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
			var dateconfigList=clientListData[clientList]['date_configurations'];
		}
	}	
	var countryNamesList = '';
	for (var countryselect in countriesList){
		for(var i = 0;i < countriesListArray.length;i++){
			if(countriesList[countryselect]['country_id'] == countriesListArray[i]){
				countryNamesList = countryNamesList + countriesList[countryselect]['country_name'] + ',';
			}
		}
	}
	$("#countryNames").val(countryNamesList);
	var domainNamesList = '';
	for (var domainselect in domainsList){
		for(var i = 0;i < domainsListArray.length;i++){
			if(domainsList[domainselect]['domain_id'] == domainsListArray[i]){
				domainNamesList = domainNamesList + domainsList[domainselect]['domain_name'] + ',';
			}
		}
	}
	$("#domainNames").val(domainNamesList);
	var value;
	dateconfig(dateconfigList);	
}

function dateconfig(dateconfigList){
	alert("hi");
	$('.tbody-dateconfiguration-list').empty();
	var countriesList = $('#country').val();
	var domainsList = $('#domain').val();
	alert("hi2");
	console.log("list===="+dateconfigList);
	alert("hi3");
	if(countriesList != '' && domainsList != ''){
		if(countriesList != ''){ 
			var arrayCountries = countriesList.split(",");
			if(domainsList != ''){
				var arrayDomains = domainsList.split(",");
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
function getCountriesName(countryId){
	var countryName;
	$.each(countriesList, function (key, value){
		if(countriesList[key]['country_id'] == countryId){
			countryName = countriesList[key]['country_name'];
			return false;
		}
	});
	return countryName;
}
function getDomainName(doaminId){
	var domainName;
	$.each(domainsList, function (key, value){
		if(domainList[key][domain_id] == doaminId){
			domainName = domainList[key]['domain_name'];
			return false;
		}
	});
	return domainName;
}
$("#search-clientgroup-name").keyup(function() { 
	var count = 0;
    var value = this.value.toLowerCase();
    $("table").find("tr:not(:first)").each(function(index) {
        if (index === 0) return;
        var id = $(this).find(".clientgroup-name").text().toLowerCase();       
        $(this).toggle(id.indexOf(value) !== -1);;
    });
   
});

//Autocomplete Script Starts and Hide list items after select
function hidemenu() {
	document.getElementById('selectboxview').style.display = 'none';
	document.getElementById('selectboxview-country').style.display = 'none';
	document.getElementById('selectboxview-users').style.display = 'none';
}
//load domain list in multi select box
function loadauto() {
	document.getElementById('selectboxview').style.display = 'block';
	var editdomainval = [];
	if($("#domain").val() != ''){
		editdomainval = $("#domain").val().split(",");
	}
//if($("#domainselected").val() == ''){
	var domains = domainsList;
	$('#ulist').empty();
	var str = '';
	for(var i in domains){
		var selectdomainstatus='';
		for(var j = 0; j < editdomainval.length; j++){
			if(editdomainval[j] == domains[i]["domain_id"]){
				selectdomainstatus = 'checked';
			}
		}
		var domainId=parseInt(domains[i]["domain_id"]);
		var domainName=domains[i]["domain_name"];
		if(selectdomainstatus == 'checked'){
			str += '<li id = "'+domainId+'" class = "active_selectbox" onclick = "activate(this)" >'+domainName+'</li> ';
		}else{
			str += '<li id = "'+domainId+'" onclick = "activate(this)" >'+domainName+'</li> ';
		}
	}
  $('#ulist').append(str);
  $("#domainselected").val(editdomainval.length+" Selected")
 // }
}
//check & uncheck process
function activate(element){
	var chkStatus = $(element).attr('class');
	if(chkStatus == 'active_selectbox'){
		$(element).removeClass("active_selectbox");
	}else{
		$(element).addClass("active_selectbox");
	}  
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
	dateconfig();
}

function loadautocountry () {
	document.getElementById('selectboxview-country').style.display = 'block';
	var editcountryval = [];
	if($("#country").val() != ''){
		editcountryval = $("#country").val().split(",");
	}
	//alert(editcountryval[0]+"---"+editcountryval[1]);
	var countries = countriesList;

	$('#ulist-country').empty();
	var str = '';
	for(var i in countries){
		var selectcountrystatus = '';
		for(var j = 0; j < editcountryval.length; j++){
			if(editcountryval[j] == countries[i]["country_id"]){
				selectcountrystatus = 'checked';
			}
		}
		var countryId = parseInt(countries[i]["country_id"]);
		var countryName = countries[i]["country_name"];
		
		if(selectcountrystatus == 'checked'){	
			str += '<li id = "'+countryId+'" class="active_selectbox_country" onclick="activateCountry(this)" >'+countryName+'</li> ';
		}else{
			str += '<li id="'+countryId+'" onclick="activateCountry(this)" >'+countryName+'</li> ';
		}
	}
  $('#ulist-country').append(str);
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
  	dateconfig();
}
function dateconfig(){
	$('.tbody-dateconfiguration-list').empty();
	var countriesList = $('#country').val();
	var countriesNamesList = $('#countryNames').val();
	var domainsList = $('#domain').val();
	var domainNamesList = $('#domainNames').val();
	//console.log(countriesList+"==="+domainsList);
	if(countriesList != '' && domainsList != ''){
		if(countriesList != ''){ 
			var arrayCountries = countriesList.split(",");
			var arrayCountriesName = countriesNamesList.split(",");
			if(domainsList != ''){
				var arrayDomains = domainsList.split(",");
				var arrayDomainName = domainNamesList.split(",");
			}
			for(var ccount = 0;ccount < arrayCountries.length; ccount++){
				var tableRow = $('#templates .table-dconfig-list .table-dconfig-countries-row');
				var clone = tableRow.clone();
				$('.inputCountry', clone).val(arrayCountries[ccount]);
				$('.dconfig-country-name', clone).text(arrayCountriesName[ccount]);
				$('.dconfig-country-name', clone).addClass("heading");
				$('.tbody-dateconfiguration-list').append(clone);

				for(var dcount = 0;dcount < arrayDomains.length; dcount++){
					var tableRowDomains = $('#templates .table-dconfig-list .table-dconfig-domain-row');
					var clone1 = tableRowDomains.clone();
					$('.inputDomain', clone1).val(arrayDomains[dcount]);
					$('.dconfig-domain-name', clone1).text(arrayDomainName[dcount]);

					$('.tl-from', clone1).addClass('tl-from-'+arrayCountries[ccount]+'-'+arrayDomains[dcount]);
					$('.tl-to', clone1).addClass('tl-to-'+arrayCountries[ccount]+'-'+arrayDomains[dcount]);
					$('.tbody-dateconfiguration-list').append(clone1);
				}
			}
		}
	}
}
function loadAutoUsers () {
	document.getElementById('selectboxview-users').style.display = 'block';
	var editusersval = [];
	if($("#users").val() != ''){
		editusersval = $("#users").val().split(",");
	}
	var users = userList;
	$('#ulist-users').empty();
	var str = '';
	for(var i in users){		
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
  $('#ulist-users').append(str);
  $("#usersSelected").val(editusersval.length+" Selected")
}
//check & uncheck process
function activateUsers(element){
  var chkstatus = $(element).attr('class');
  if(chkstatus == 'active_selectbox_users'){
	 	$(element).removeClass("active_selectbox_users");
  }
  else{
    $(element).addClass("active_selectbox_users");
  }  
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
function gototop(){
	$("html, body").animate({ scrollTop: 0 }, "slow");
}
$(function() {
	initialize();
});
