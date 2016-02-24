var countriesList;
var businessGroupsList;
var legalEntitiesList;
var divisionList;
var domainList;
var unitList;
var userGroupsList;
var serviceProviderList;
var userList;

function clearMessage() {
    $(".error-message").hide();
    $(".error-message").text("");
}
function displayMessage(message) {
    $(".error-message").text(message);
    $(".error-message").show();
}
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
	clearMessage();
	$("#user-privilege-id").val('');
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
		$.each(unitList, function(key, value) { //unit name
			if(unitList[key]['unit_id'] == unitId){
				unit['unitName'] = unitList[key]['unit_name'];
				unit['unitAddress'] = unitList[key]['unit_address'];
			}
		});	
	}
	return unit;
}

function loadClientUserList(){
	$(".tbody-users-list").find("tr").remove();
	var sno = 0;
	var imageName, title, usergroupname, seatingunitname, seatingunitaddress;	
	for(var i in userList){
		var users = userList[i];
		var userId = users["user_id"];
		var isActive = users["is_active"];
		var isAdmin = users["is_admin"];

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
		if(isAdmin == true){ 
			adminstatus = false;
			imageadminName = "promote-active.png";
			admintitle = "Click here to deactivate Promote Admin";
		}
		else{
			adminstatus = true;
			imageadminName = "promote-inactive.png";
			admintitle = "Click here to Promote Admin";
		}
		
		var seatingUnitId = userList[i]['seating_unit_id']
		var userGroupId = userList[i]['user_group_id'];

		if(users["user_group_id"] != null){
			var tableRow = $('#templates .table-users-list .table-row');
			var clone = tableRow.clone();
			sno = sno + 1;
			$('.sno', clone).text(sno);
			$('.employee-code-name', clone).text(users["employee_code"]+" - "+users["employee_name"]);
			$('.group-name', clone).text(getUserGroupName(userGroupId));
			$('.level-name', clone).text("Level "+users["user_level"]);
			$('.seating-unit', clone).html('<abbr class="page-load tipso_style" title="'+getUnitNameAndAddress(seatingUnitId)['unitAddress']+'"><img src="/images/icon-info.png" style="margin-right:10px"/>'+getUnitNameAndAddress(seatingUnitId)['unitName']);
			
			$('.edit', clone).html('<img src="/images/icon-edit.png" id="editid" onclick="user_edit('+userId+')"/>');
			$('.is-active', clone).html('<img src="/images/'+imageName+'" title="'+title+'" onclick="user_active('+userId+', '+statusVal+')"/>');
			$('.promote-admin', clone).html('<img src="/images/'+imageadminName+'" title="'+admintitle+'" onclick="user_isadmin('+userId+', '+adminstatus+')" />');
			$('.tbody-users-list').append(clone);				
		}		
	}
}
function user_edit(userId){
	$("#user-add").show();
	$("#user-view").hide();
	$("#client-user-id").val(userId);  
	function onSuccess(data){
		loadUserUpdate(userId);  
	}
	function onFailure(error){
		console.log(status);
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
function loadUserUpdate(userId){
	var bgroups = [];
	var lentities = [];
	var divisions = [];
	var bgroupslist;
	var lentitieslist;
	var divisionlist;
	for(var user in userList){
		if(userList[user]['user_id'] == userId){
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
			$("#service-provider").val(userList[user]['service_provider']);
			$("#employee-name").val(userList[user]['employee_name']);
			$("#employee-id").val(userList[user]['employee_code']);
			$("#country-code").val(contactno[0]);
			$("#area-code").val(contactno[1]);
			$("#mobile-number").val(contactno[2]);
			$("#usergroupval").val(usergroupname);
			$("#usergroup").val(userList[user]['user_group_id']);
			$("#user-level option[value = "+userList[user]['user_level']+"]").attr('selected','selected');
			$("#seatingunitval").val(seatingunitname);
			$("#seatingunit").val(userList[user]['seating_unit_id']);
			$("#service-provider").val(userList[user]['service_provider']);
			$("#email-id").val(userList[user]['email_id']);
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

$("#submit").click(function(){
	var usertype = $('#usertype').val();
	var employeename = $('#employee-name').val();	
	var employeeid = $('#employee-id').val();
	var countrycode = $('#country-code').val();
	var areacode = $('#area-code').val();
	var mobilenumber = $('#mobile-number').val();
	var usergroup = $('#usergroup').val();
	var userlevel = $('#user-level').val();
	var emailid = $('#email-id').val();
	var country = $('#country').val();
	var businessgroups = $('#business-groups').val();
	var legalentities = $('#legal-entities').val();
	var division = $('#division').val();
	var domains = $('#domains').val();
	var units = $('#units').val();
	var isserviceprovider, serviceprovider;
	if(usertype == 'Inhouse'){
		isserviceprovider = false;
		serviceprovider = null;
		var seatingunit = $('#seatingunit').val();	
		var seatingunitname = $('#seatingunitval').val();		
		if(seatingunit == ''){
			displayMessage("Enter seating Unit");	
		}	
		if(employeeid == ''){
			displayMessage("Enter Employee Code");	
		}	
		if(seatingunitname == ''){
			displayMessage("Enter seating Unit");	
		}
	}
	if(usertype == 'Service Provider'){
		isserviceprovider = true;
		serviceprovider = $('#serviceprovider').val();
		if(serviceprovider.length == 0){
			displayMessage("Enter service provider");	
		}
	}	
	if(employeename == ''){
		displayMessage("Enter Employee Name");
	}
	if(countrycode == ''){
		displayMessage("Enter Country Code");
	}
	if(mobilenumber == ''){
		displayMessage("Enter Mobile Number");
	}
	if(usergroup == ''){
		displayMessage("Enter usergroup");
	}
	if(userlevel == ''){
		displayMessage("Select User Level");
	}
	if(emailid == ''){
		displayMessage("Enter Email Id");
	}
	if(country == ''){
		displayMessage("select Country");
	}
	if(businessgroups == ''){
		displayMessage("Select businessgroups");
	}
	if(legalentities == ''){
		displayMessage("select legalentities");
	}
	if(division == ''){
		displayMessage("select division");
	}
	if(domains == ''){
		displayMessage("select domains");
	}
	if(units == ''){
		displayMessage("Select Units")
	}

	if($('#client-user-id').val() == ''){
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
  			initialize();
  	    }
		function onFailure(error){
			displayMessage(error);
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
			$("#user-add").hide();
			$("#user-view").show();
			initialize();
    	}
		function onFailure(status, data){
			displayMessage(status);
		}
		var clientUserDetail = [userId,  parseInt(usergroup), employeename, 
			      employeeid, contactNo, parseInt(seatingunit), parseInt(userlevel), 
			      arrayCountries, arrayDomains, arrayUnits, isAdmin, isserviceprovider,
			      serviceprovider];
		var clientUserDetailDict = client_mirror.getUpdateClientUserDict(clientUserDetail)
		
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
});
function user_active(userId, isActive){
	function onSuccess(data){
		initialize();
	}
	function onFailure(error){
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
function user_isadmin(userId, isAdmin){
	function onSuccess(data){
		initialize();
	}
	function onFailure(error){
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
	
}
// Legal Entity----------------------------------------------------------------------------------------------------------------------
function hidemenulegalentities() {
	document.getElementById('selectboxview-legal-entities').style.display = 'none';
}
function loadautolegalentities () {
	document.getElementById('selectboxview-legal-entities').style.display = 'block';
	var bgroupsValue=$("#business-groups").val();
	var arraybusinessgroups=bgroupsValue.split(',');
	$('#selectboxview-legal-entities ul').empty();
	$.each(arraybusinessgroups,function(count, values){
		var editlegalentitiesval=[];
		if($("#legal-entities").val() != ''){
			editlegalentitiesval = $("#legal-entities").val().split(",");
		}
		var legalentities = legalEntitiesList;

		var str='';
		if(values.length!=0){
			for(var bgroup in businessGroupsList){		
				if(businessGroupsList[bgroup]['business_group_id']==arraybusinessgroups[count]){
					str+='<li class="li-heading">'+businessGroupsList[bgroup]['business_group_name']+'</li> ';
				}
			}
		}
		for(var i in legalEntitiesList){
			if(arraybusinessgroups[count]==legalEntitiesList[i]['business_group_id']){			
				var selectlentitystatus='';
				for(var j=0; j<editlegalentitiesval.length; j++){
					if(editlegalentitiesval[j]==legalEntitiesList[i]["legal_entity_id"]){
						selectlentitystatus='checked';
					}
				}
				var lentityId=parseInt(legalEntitiesList[i]["legal_entity_id"]);
				var lentityName=legalEntitiesList[i]["legal_entity_name"];
				if(selectlentitystatus == 'checked'){	
					str += '<li id="'+lentityId+'" class="active_selectbox_legal_entities" onclick="activatelegalentities(this)" >'+lentityName+'</li> ';
				}else{
					str += '<li id="'+lentityId+'" onclick="activatelegalentities(this)" >'+lentityName+'</li> ';
				}
			}				
		}
		$('#selectboxview-legal-entities ul').append(str);
		$("#legal-entities-selected").val(editlegalentitiesval.length+" Selected");  
	});
 
  
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

		if(values.length!=0){ //for heading
			for(var lentity in legalEntitiesList){						
				if(legalEntitiesList[lentity]['legal_entity_id']==arraylentity[count]){
					str+='<li class="li-heading">'+legalEntitiesList[lentity]['legal_entity_name']+'</li> ';
				}
			}
		}
		for(var i in divisionList){
			if(arraylentity[count]==divisionList[i]['division_id']){			
				var selectdivisionstatus='';
				for(var j=0; j<editdivisionval.length; j++){
					if(editdivisionval[j]==divisionList[i]["division_id"]){
						selectdivisionstatus='checked';
					}
				}
				var divisionId=parseInt(divisionList[i]["division_id"]);
				var divisionName=divisionList[i]["division_name"];
				if(selectdivisionstatus == 'checked'){	
					str += '<li id="'+divisionId+'" class="active_selectbox_division" onclick="activateDivision(this)" >'+divisionName+'</li> ';
				}else{
					str += '<li id="'+divisionId+'" onclick="activateDivision(this)" >'+divisionName+'</li> ';
				}
			}				
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
			selNames = selNames+$(this).text();
		}else{
			selids = selids+el.id+",";
			selNames = selNames+$(this).text()+",";
		}    
	});
	$("#division-selected").val(totalcount+" Selected");
	$("#division").val(selids);
	unitview();
}
//Unit List -----------------------------------------------------------------------------------------------------
function unitview(){	
	$('#unitList ul li:not(:first)').empty();
	var divisionIds=$('#division').val();
	var arraydivision=divisionIds.split(',');
	$.each(arraydivision,function(count, values){
		var editunitval=[];
		if($("#units").val() != ''){
			editunitsval = $("#units").val().split(",");
		}

		var str='';
		for(var division in divisionList){						
			if(divisionList[division]['division_id']==arraydivision[count]){
				str+='<li class="li-heading">'+divisionList[division]['division_name']+'</li> ';
			}
		}
		for(var i in unitList){
			if(arraydivision[count]==unitList[i]['division_id']){			
				var unitId=parseInt(unitList[i]["unit_id"]);
				var unitName=unitList[i]["unit_name"];
				str += '<li id="'+unitId+'" onclick="activateUnit(this)" >'+unitName+'</li> ';
			}				
		}
		$('#unitList ul').append(str);
	});
}

function activateUnit(element){
  var chkstatus = $(element).attr('class');
  if(chkstatus == 'active'){
	 	$(element).removeClass("active");
  }
  else{
    $(element).addClass("active");
  }  
	var selids='';	
	var totalcount =  $(".active").length;
	$(".active").each( function( index, el ) {
		if (index === totalcount - 1) {
			selids = selids+el.id;			
		}else{
			selids = selids+el.id+",";
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
}
function hidemenuseatingunit(){
	document.getElementById('autocompleteview').style.display = 'none';
}
function loadauto_text (textval) {
  document.getElementById('autocompleteview').style.display = 'block';
  var units = unitList;
  var suggestions = [];
  $('#autocompleteview ul').empty();
  if(textval.length>0){
    for(var i in units){
      if (~units[i]["unit_name"].toLowerCase().indexOf(textval.toLowerCase())) suggestions.push([units[i]["unit_id"],units[i]["unit_name"]]); 
    }
    var str='';
    for(var i in suggestions){
              str += '<li id="'+suggestions[i][0]+'"onclick="activate_text(this,\''+suggestions[i][0]+'\',\''+suggestions[i][1]+'\')">'+suggestions[i][1]+'</li>';
    }
    $('#autocompleteview ul').append(str);
    $("#seatingunit").val('');
    }
}
//set selected autocomplte value to textbox
function activate_text (element,checkval,checkname) {
  $("#seatingunitval").val(checkname);
  $("#seatingunit").val(checkval);
}
//USergroup====================================================================================

function hidemenuusergroup(){
	document.getElementById('usergroupview').style.display = 'none';
}
//load usergroup list in autocomplete text box  
function loadauto_usergroup (textval) {
  document.getElementById('usergroupview').style.display = 'block';
  var usergroups = userGroupsList;
  var suggestions = [];
  $('#usergroupview ul').empty();
  if(textval.length>0){
    for(var i in usergroups){
      if (~usergroups[i]["user_group_name"].toLowerCase().indexOf(textval.toLowerCase())) suggestions.push([usergroups[i]["user_group_id"],usergroups[i]["user_group_name"]]); 
    }
    var str='';
    for(var i in suggestions){
              str += '<li id="'+suggestions[i][0]+'"onclick="activate_text1(this,\''+suggestions[i][0]+'\',\''+suggestions[i][1]+'\')">'+suggestions[i][1]+'</li>';
    }
    $('#usergroupview ul').append(str);
    $("#usergroup").val('');
    }
}
//set selected autocomplte value to textbox
function activate_text1 (element,checkval,checkname) {
  $("#usergroupval").val(checkname);
  $("#usergroup").val(checkval);
}
//service provider====================================================================================

function hidemenuserviceprovider(){
	document.getElementById('serviceproviderview').style.display = 'none';
}
//load usergroup list in autocomplete text box  
function loadauto_serviceprovider (textval) {
  document.getElementById('serviceproviderview').style.display = 'block';
  var serviceprovider = serviceProviderList;
  console.log(serviceProviderList);
  var suggestions = [];
  $('#serviceproviderview ul').empty();
  if(textval.length>0){
    for(var i in serviceprovider){
      if (~serviceprovider[i]["service_provider_name"].toLowerCase().indexOf(textval.toLowerCase())) suggestions.push([serviceprovider[i]["service_provider_id"],serviceprovider[i]["service_provider_name"]]); 
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
$(function() {
	initialize();
});