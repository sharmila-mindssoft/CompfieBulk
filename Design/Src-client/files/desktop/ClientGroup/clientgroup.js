var usersList;
var domainsList;
var countriesList;
$(function() {
	$("#clientgroup-add").hide();
	initialize();
});
$(".btn-clientgroup-add").click(function(){
	$("#clientgroup-add").show();
	$("#clientgroup-view").hide();
	$("#clientgroup-name").val('');
  	$("#clientgroup-id").val('');
 	$(".error-message").html('');
 	$("#upload-logo-img").hide();
 	var x=document.getElementsByTagName("input");
 	for(i = 0; i<=x.length-1; i++){
  		if(x.item(i).type!="submit" ){ x.item(i).value = ""; }
  	}
  	
  	$('.tbody-dateconfiguration-list').empty();
  	function success(status, data){
  		userList = data["users"];
		domainsList = data["domains"];
		countriesList = data["countries"];  	
  	}
  	function failure(status, data){
  		console.log(status);
  	}
  	mirror.getClientGroups("TechnoAPI", success, failure);
});
$("#btn-clientgroup-cancel").click(function(){
	$("#clientgroup-add").hide();
	$("#clientgroup-view").show();
});
function initialize(){	
	function success(status, data){
		loadClientGroupList(data['client_list']);
	}
	function failure(status, data){	
	}
	mirror.getClientGroups("TechnoAPI", success, failure);
}
function clientgroup_edit(clientGroupId){
	$("#clientgroup-add").show();
	$("#clientgroup-view").hide();
	$("#clientgroup-id").val(clientGroupId);
	function success(status, data){
		if(status=="GetClientGroupsSuccess"){
			userList = data["users"];
			domainsList = data["domains"];	
			countriesList = data["countries"];  	
			loadFormListUpdate(data['client_list'],clientGroupId);
		}
	}
	function failure(status, data){
	}
	mirror.getClientGroups("TechnoAPI", success, failure);
}
function loadFormListUpdate(clientListData, clientGroupId){
	for(clientList in clientListData){
		if(clientGroupId==clientListData[clientList]['client_id']){
			$("#clientgroup-name").val(clientListData[clientList]['client_name']);

			var countriesListArray=clientListData[clientList]['country_ids'];
			$("#country").val(countriesListArray);
			$("#countryselected").val(countriesListArray.length+" Selected");

			var domainsListArray=clientListData[clientList]['domain_ids'];
			$("#domain").val(domainsListArray);
			$("#domainselected").val(domainsListArray.length+" Selected");

			$("#contract-from").val(clientListData[clientList]['contract_from']);
			$("#contract-to").val(clientListData[clientList]['contract_to']);
			$("#username").val(clientListData[clientList]['username']);
			//$("#upload-logo-img").attr("src",clientListData[clientList]['logo']);
			$("#upload-logo-img").show();
			$("#no-of-user-licence").val(clientListData[clientList]['no_of_user_licence']);
			$("#file-space").val(clientListData[clientList]['file_space']);
			console.log(clientListData[clientList]['is_sms_subscribed']);
			if(clientListData[clientList]['is_sms_subscribed']==1){ $('#subscribe-sms').prop("checked", true); }
			var userListArray=clientListData[clientList]['incharge_persons'];
			$("#users").val(userListArray);
			$("#usersSelected").val(userListArray.length+" Selected");
		}
	}	
	var countryNamesList='';
	for (var countryselect in countriesList){
		for(var i=0;i<countriesListArray.length;i++){
			if(countriesList[countryselect]['country_id']==countriesListArray[i]){
				countryNamesList = countryNamesList + countriesList[countryselect]['country_name'] + ',';
			}
		}
	}
	$("#countryNames").val(countryNamesList);
	var domainNamesList='';
	for (var domainselect in domainsList){
		for(var i=0;i<domainsListArray.length;i++){
			if(domainsList[domainselect]['domain_id']==domainsListArray[i]){
				domainNamesList = domainNamesList + domainsList[domainselect]['domain_name'] + ',';
			}
		}
	}
	$("#domainNames").val(domainNamesList);
	dateconfig();	
}
function loadClientGroupList(clientGroupList){
	$(".tbody-clientgroup-list").find("tr").remove();
  	var sno=0;
	var imageName, title;	
	for(var i in clientGroupList){
		var clientGroups=clientGroupList[i];
		var clientId=clientGroups["client_id"];
		var isActive=clientGroups["is_active"];
		if(isActive==1){
			imageName="icon-active.png";
			title="Click here to deactivate"
			statusVal=0;
		}
		else{
			imageName="icon-inactive.png";	
			title="Click here to Activate"
			statusVal=1;
		}
		var tableRow=$('#templates .table-clientgroup-list .table-row');
		var clone=tableRow.clone();
		sno = sno + 1;
		$('.sno', clone).text(sno);
		$('.clientgroup-name', clone).text(clientGroups["client_name"]);
		$('.edit', clone).html('<img src="/images/icon-edit.png" id="editid" onclick="clientgroup_edit('+clientId+')"/>');
		$('.is-active', clone).html('<img src="/images/'+imageName+'" title="'+title+'" onclick="clientgroup_active('+clientId+', '+statusVal+')"/>');
		$('.tbody-clientgroup-list').append(clone);			
	}
	$("#total-records").html('Total : '+sno+' records');
}

$("#btn-clientgroup-submit").click(function(){
	var dateConfigurations=[];	
	var countriesList=$('#country').val();
	var domainsList=$('#domain').val();
	if(countriesList!='' && domainsList!=''){
		if(countriesList!=''){ 
			var arrayCountries=countriesList.split(",");
			if(domainsList!=''){
				var arrayDomains=domainsList.split(",");
			}
			for(var ccount=0;ccount < arrayCountries.length; ccount++){
				for(var dcount=0;dcount < arrayDomains.length; dcount++){
					var configuration = {};
					configuration["country_id"] =parseInt(arrayCountries[ccount]);
					configuration["domain_id"] = parseInt(arrayDomains[dcount]);
					configuration["period_from"] = parseInt($(".tl-from-"+arrayCountries[ccount]+"-"+arrayDomains[dcount]).val());
					configuration["period_to"] = parseInt($(".tl-to-"+arrayCountries[ccount]+"-"+arrayDomains[dcount]).val());
					dateConfigurations.push(configuration);
				}
			}
		}
	}
	var clientGroupIdVal = $("#clientgroup-id").val();
	var clientGroupNameVal = $("#clientgroup-name").val();
	var arrayCountriesVal=$("#country").val().split(",");
	var arrayCountries= [];
	for(var i=0; i<arrayCountriesVal.length; i++){ arrayCountries[i] = parseInt(arrayCountriesVal[i]); } 
	var countriesVal = arrayCountries;
	var arrayDomainsVal=$("#domain").val().split(",");
	var arrayDomains= [];
	for(var j=0; j<arrayDomainsVal.length; j++){ arrayDomains[j] = parseInt(arrayDomainsVal[j]); } 
	var domainsVal = arrayDomains;
	var contractFromVal = $("#contract-from").val();
	var contractToVal = $("#contract-to").val();	
	var usernameVal = $("#username").val();
	var uploadLogoVal = $("#upload-logo").val();
	var licenceVal = parseInt($("#no-of-user-licence").val());
	var intFilesSpace=Number($("#file-space").val());
	var fileSpaceVal =parseFloat(intFilesSpace);
	//var subscribeSmsVal = $("#subscribe-sms").val();
	var arrayinchargePersonVal=$("#users").val().split(",");
	var arrayinchargePerson= [];
	for(var k=0; k<arrayinchargePersonVal.length; k++) { arrayinchargePerson[k] = parseInt(arrayinchargePersonVal[k]); } 
	var inchargePersonVal = arrayinchargePerson;
	if ($('#subscribe-sms').is(":checked")){
	 var subscribeSmsVal=1;	 
	}
	else{ var subscribeSmsVal=0; }
	if(clientGroupNameVal==''){
		$(".error-message").html('Group Required');
	}
	else if(countriesVal==''){
		$(".error-message").html('Country Required');
	}
	else if(domainsVal==''){
		$(".error-message").html('Domain Required');
	}
	else if(contractFromVal==''){
		$(".error-message").html('Contract From Required');		
	}
	else if(contractToVal==''){
		$(".error-message").html('Contract To Required');		
	}
	else if(usernameVal==''){
		$(".error-message").html('Username Required');		
	}
	else if(validateEmail(usernameVal)==''){
		$(".error-message").html('Username Invalid Format');		
	}
	else if(licenceVal==''){
		$(".error-message").html('No. Of User Licence Required');
	}
	else if(isNaN(licenceVal)){
		$(".error-message").html('Invalid No. Of User Licence');
	}
	else if(fileSpaceVal==''){
		$(".error-message").html('File Space Required');
	}
	else if(!$.isNumeric(fileSpaceVal)){
		$(".error-message").html('File Space Value Invalid');
	}
	else if(inchargePersonVal==''){
		$(".error-message").html('Incharge Person Required');
	}
	else if($('#clientgroup-id').val()==''){	
		if(uploadLogoVal==''){
			$(".error-message").html('Logo Required');	
			return false;	
		}	
		function success(status, data){
			if(status == 'SaveClientGroupSuccess') {
		    	$("#clientgroup-add").hide();
	  			$("#clientgroup-view").show();
	  			initialize();
	  		}
	  		 else {
      			$(".error-message").html(status);
      		}	
	    }
		function failure(status, data){
			$(".error-message").html(status);
		}
		
		var clientGroupDetails = {}
		clientGroupDetails["group_name"] = clientGroupNameVal ;
        clientGroupDetails["country_ids"] = countriesVal;
        clientGroupDetails["domain_ids"] = domainsVal;
        clientGroupDetails["logo"] = uploadLogoVal;
        clientGroupDetails["contract_from"] = contractFromVal;
        clientGroupDetails["contract_to"] = contractToVal;
        clientGroupDetails["incharge_persons"] = inchargePersonVal;
        clientGroupDetails["no_of_user_licence"] = licenceVal;
        clientGroupDetails["file_space"] = fileSpaceVal;
        clientGroupDetails["is_sms_subscribed"] = subscribeSmsVal;
        clientGroupDetails["email_id"] = usernameVal;
		//console.log(dateConfigurations);
		//console.log(clientGroupDetails);
		mirror.saveClientGroup("TechnoAPI", clientGroupDetails, dateConfigurations,success, failure);
	}
	else if($('#clientgroup-id').val()!=''){		
		function success(status, data){
			if(status == 'UpdateClientGroupSuccess') {
		    	$("#clientgroup-add").hide();
	  			$("#clientgroup-view").show();
	  			initialize();
	  		}
	  		 else {
      			$(".error-message").html(status);
      		}
	    }
		function failure(status, data){
			$(".error-message").html(status);
		}
		
		var clientGroupDetails = {}
		clientGroupDetails["client_id"] = parseInt(clientGroupIdVal);
		clientGroupDetails["group_name"] = clientGroupNameVal ;
        clientGroupDetails["country_ids"] = countriesVal;
        clientGroupDetails["domain_ids"] = domainsVal;
        clientGroupDetails["logo"] = uploadLogoVal;
        clientGroupDetails["contract_from"] = contractFromVal;
        clientGroupDetails["contract_to"] = contractToVal;
        clientGroupDetails["incharge_persons"] = inchargePersonVal;
        clientGroupDetails["no_of_user_licence"] = licenceVal;
        clientGroupDetails["file_space"] = fileSpaceVal;
        clientGroupDetails["is_sms_subscribed"] = subscribeSmsVal;
        clientGroupDetails["email_id"] = usernameVal;
		//console.log(dateConfigurations);
		//console.log(clientGroupDetails);
		mirror.updateClientGroup("TechnoAPI", clientGroupDetails, dateConfigurations,success, failure);
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
  	function success(status, data){
	  initialize();
  	}
  	function failure(status, data){
  	}
  	mirror.changeClientGroupStatus("TechnoAPI", parseInt(clientId), isActive, success, failure);
}


$("#search-clientgroup-name").keyup(function() { 
	var count=0;
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
	var editdomainval=[];
	if($("#domain").val() != ''){
		editdomainval = $("#domain").val().split(",");
	}
//if($("#domainselected").val() == ''){
	var domains = domainsList;
	$('#ulist').empty();
	var str='';
	for(var i in domains){
		var selectdomainstatus='';
		for(var j=0; j<editdomainval.length; j++){
			if(editdomainval[j]==domains[i]["domain_id"]){
				selectdomainstatus='checked';
			}
		}
		var domainId=parseInt(domains[i]["domain_id"]);
		var domainName=domains[i]["domain_name"];
		if(selectdomainstatus == 'checked'){
			str += '<li id="'+domainId+'" class="active_selectbox" onclick="activate(this)" >'+domainName+'</li> ';
		}else{
			str += '<li id="'+domainId+'" onclick="activate(this)" >'+domainName+'</li> ';
		}
	}
  $('#ulist').append(str);
  $("#domainselected").val(editdomainval.length+" Selected")
 // }
}
//check & uncheck process
function activate(element){
	var chkstatus = $(element).attr('class');
	if(chkstatus == 'active_selectbox'){
		$(element).removeClass("active_selectbox");
	}else{
		$(element).addClass("active_selectbox");
	}  
	var selids='';
	var selNames='';
	var totalcount =  $(".active_selectbox").length;
	$(".active_selectbox").each( function( index, el ) {
		if (index === totalcount - 1) {
			selids = selids+el.id;
			selNames = selNames+$(this).text();
		}else{
			selids = selids+el.id+",";
			selNames = selNames+$(this).text()+",";			
		}    
	});
	$("#domainselected").val(totalcount+" Selected");
	$("#domain").val(selids);
	$("#domainNames").val(selNames);
	dateconfig();
}

function loadautocountry () {
	document.getElementById('selectboxview-country').style.display = 'block';
	var editcountryval=[];
	if($("#country").val() != ''){
		editcountryval = $("#country").val().split(",");
	}
	//alert(editcountryval[0]+"---"+editcountryval[1]);
	var countries = countriesList;

	$('#ulist-country').empty();
	var str='';
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
	$("#countryNames").val(selNames);
	//Add date configuration
//	$('.tbody-dateconfiguration-list').empty();
  	dateconfig();
}
function dateconfig(){
	$('.tbody-dateconfiguration-list').empty();
	var countriesList=$('#country').val();
	var countriesNamesList=$('#countryNames').val();
	var domainsList=$('#domain').val();
	var domainNamesList=$('#domainNames').val();
	//console.log(countriesList+"==="+domainsList);
	if(countriesList!='' && domainsList!=''){
		if(countriesList!=''){ 
			var arrayCountries=countriesList.split(",");
			var arrayCountriesName=countriesNamesList.split(",");
			if(domainsList!=''){
				var arrayDomains=domainsList.split(",");
				var arrayDomainName=domainNamesList.split(",");
			}
			for(var ccount=0;ccount < arrayCountries.length; ccount++){
				var tableRow=$('#templates .table-dconfig-list .table-dconfig-countries-row');
				var clone=tableRow.clone();
				$('.inputCountry', clone).val(arrayCountries[ccount]);
				$('.dconfig-country-name', clone).text(arrayCountriesName[ccount]);
				$('.dconfig-country-name', clone).addClass("heading");
				$('.tbody-dateconfiguration-list').append(clone);

				for(var dcount=0;dcount < arrayDomains.length; dcount++){
					var tableRowDomains=$('#templates .table-dconfig-list .table-dconfig-domain-row');
					var clone1=tableRowDomains.clone();
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
	var editusersval=[];
	if($("#users").val() != ''){
		editusersval = $("#users").val().split(",");
	}
	var users = userList;
	$('#ulist-users').empty();
	var str='';
	for(var i in users){		
		var selectUserStatus='';
		for(var j=0; j<editusersval.length; j++){
			if(editusersval[j]==users[i]["user_id"]){
				selectUserStatus='checked';
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
	var selids='';
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
