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
$(".btn-clientgroup-cancel").click(function(){
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
		$('.edit', clone).html('<img src="/images/icon-edit.png" id="editid" onclick="clientgroup_edit('+clientId+',\''+isActive+'\')"/>');
		$('.is-active', clone).html('<img src="/images/'+imageName+'" title="'+title+'" onclick="clientgroup_active('+clientId+', '+statusVal+')"/>');
		$('.tbody-clientgroup-list').append(clone);			
	}
	$("#total-records").html('Total : '+sno+' records');
}

$("#btn-clientgroup-submit").click(function(){
	var clientGroupIdVal = $("#clientgroup-id").val();
	var clientGroupNameVal = $("#clientgroup-name").val();
	var countriesVal = $("#countries").val();
	var domainsVal = $("#domains").val();
	var contractFromVal = $("#contract-from").val();
	var contractToVal = $("#contract-to").val();
	var usernameVal = $("#username").val();
	var uploadLogoVal = $("#upload-logo").val();
	var licenceVal = $("#no-of-user-licence").val();
	var fileSpaceVal = $("#file-space").val();
	var subscribeSmsVal = $("#subscribe-sms").val();
	var inchargePersonVal = $("#incharge-person").val();

	
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
	else if(uploadLogoVal==''){
		$(".error-message").html('Logo Required');
	}
	else if(licenceVal==''){
		$(".error-message").html('No. Of User Licence Required');
	}
	else if(validateDigit(licenceVal)){
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
	else if(countryIdValue==''){		
		function success(status, data){
			if(status == 'success') {
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
		mirror.saveClientGroup("TechnoAPI", clientGroupDetails, dateConfigurations,success, failure);
	}
});
function validateDigit($numb) {
  if (e.which != 8 && e.which != 0 && (e.which < 48 || e.which > 57)) {
    $(".error-message").html("Invaild Number");
    return false;
  }
}
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
    $("table").find("tr:not(:first):not(:last)").each(function(index) {
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
function loadauto () {
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
			str += '<li id="'+domainId+'" class="active_selectbox" onclick="activate(this,\''+domainId+'\',\''+domainName+'\')" >'+domainName+'</li> ';
		}else{
			str += '<li id="'+domainId+'" onclick="activate(this,\''+domainId+'\',\''+domainName+'\')" >'+domainName+'</li> ';
		}
	}
  $('#ulist').append(str);
  $("#domainselected").val(editdomainval.length+" Selected")
 // }
}
//check & uncheck process
function activate(element, domainId, domainName){
	var chkstatus = $(element).attr('class');
	if(chkstatus == 'active_selectbox'){
		$(element).removeClass("active_selectbox");
	}else{
		$(element).addClass("active_selectbox");
	}  
	var selids='';
	var totalcount =  $(".active_selectbox").length;
	$(".active_selectbox").each( function( index, el ) {
		if (index === totalcount - 1) {
			selids = selids+el.id;
		}else{
			selids = selids+el.id+",";
		}    
	});
	$("#domainselected").val(totalcount+" Selected");
	$("#domain").val(selids);
	dateconfigdomains(domainId, domainName);
}

function loadautocountry () {
	document.getElementById('selectboxview-country').style.display = 'block';
	var editcountryval=[];
	if($("#country").val() != ''){
		editcountryval = $("#country").val().split(",");
	}
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
			str += '<li id="'+countryId+'" class="active_selectbox_country" onclick="activatecountry(this,countryId,'+countryName+')" >'+countryName+'</li> ';
		}else{
			str += '<li id="'+countryId+'" onclick="activatecountry(this,\''+countryId+'\',\''+countryName+'\')" >'+countryName+'</li> ';
		}
	}
  $('#ulist-country').append(str);
  $("#countryselected").val(editcountryval.length+" Selected");
  
}
//check & uncheck process
function activatecountry(element, countryId, countryName){
  var chkstatus = $(element).attr('class');
  if(chkstatus == 'active_selectbox_country'){
	 	$(element).removeClass("active_selectbox_country");
  }
  else{
    $(element).addClass("active_selectbox_country");
  }  
	var selids='';
	var totalcount =  $(".active_selectbox_country").length;
	$(".active_selectbox_country").each( function( index, el ) {
		if (index === totalcount - 1) {
			selids = selids+el.id;
		}else{
			selids = selids+el.id+",";
		}    
	});
	$("#countryselected").val(totalcount+" Selected");
	$("#country").val(selids);
	//Add date configuration
//	$('.tbody-dateconfiguration-list').empty();
  dateconfigcountries(countryId,countryName);
}
function dateconfigcountries(countryId, countryName){
  var tableRow=$('#templates .table-dconfig-countries-list .table-dconfig-countries-row');
	var clone=tableRow.clone();
	$('.country-name', clone).text(countryName);
	$('.tbody-dateconfiguration-list').append(clone);
	$('.country-name').addClass("heading");
}
function dateconfigdomains(domainId, domainName){
	console.log(domainId+"-------"+domainName);
  var tableRowDomain=$('#templates .table-dconfig-domains-list .table-dconfig-domain-row');
	var cloneDomain=tableRowDomain.clone();
	$('.domain-name', cloneDomain).text(domainName);
	$('.tbody-dateconfiguration-list').append(cloneDomain);
	
}
//--------------------------------------------------------------------------------------------------------



//------------------------------------------------------------------------------------------------------
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

