var countriesList;
var businessgroupsList;
var divisionsList;
var domainsList;
var groupList;
var legalEntityList;
var unitList;
var countriesText;
var groupsval;
var businessgroupsval;
var legalentityval;
var divisionval;
var unitval;
var level1val;
var applicableStatus;

function clearMessage() {
    $(".error-message").hide();
    $(".error-message").text("");
}
function displayMessage(message) {
    $(".error-message").text(message);
    $(".error-message").show();
}

function initialize(){
	function onSuccess(data){
		console.log(data);
		countriesList = data['countries'];
		businessgroupsList = data['business_groups'];
		divisionsList = data['divisions'];
		domainsList = data['domains'];
		groupList = data['groups'];
		legalEntityList = data['legal_entities'];
		unitList = data['units'];
		level1List = data['level_1_statutories'];
		loadCountries(countriesList);
	}
	function onFailure(error){
		console.log(error);
	}
	mirror.getAssignedStatutoryReportFilters(
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
$("#show-button").click(function(){	
	var countries = $("#countries").val();
	countriesText = $("#countries  option:selected").text();
	//Domain
	
	var domain = $("#domain").val();
	if(domain != ''){ 
		var domainsVal = parseInt(domain);
	}
	else{
		var domainsVal = null;
	}	
	var domainName = $("#domainval").val();
	//Groups
	var groups = $("#group-id").val();
	if(groups != ''){ 
		var groupid = parseInt(groups);
	}
	else{
		var groupid = null;
	}
	groupsval = $("#groupsval").val();

	//Business Groups
	var bgroups = $("#businessgroupid").val();
	if(bgroups != ''){ 
		var businessgroupid = parseInt(bgroups);
	}
	else{
	 var businessgroupid = null;
	}
	businessgroupsval = $("#businessgroupsval").val();
	//Legal Entity
	var legalentity = $("#legalentityid").val();
	if(legalentity != ''){
		var lentityid = parseInt(legalentity);
	}
	else{
		var lentityid = null;
	}
	legalentityval = $("#legalentityval").val();
	//division
	var division = $("#divisionid").val();
	if(division != ''){
		var divisionid = parseInt(division);
	}
	else{
		var divisionid = null;
	}
	divisionval = $("#divisionval").val();
	//Units
	var units = $("#unitid").val();
	if(units != ''){
		var unitid = parseInt(units);
	}
	else{
		var unitid = null;
	}
	unitval = $("#unitval").val();
	//Level1Statutory
	var level1Statutory = $("#level1id").val();
	if(level1Statutory != ''){
		var level1Statutoryid = parseInt(level1Statutory);
	}
	else{
		var level1Statutoryid = null;
	}
	level1val = $("#level1val").val();

	applicableStatus = $("#appliability-status option:selected").val();
	if(applicableStatus == "null"){
		applicableStatus = null;
	}
	if(applicableStatus == 1){
		applicableStatus = true;
	}
	if(applicableStatus == 0){
		applicableStatus = false;
	}
	if(countries == ""){
		displayMessage("Please Select Country");
		$(".grid-table-rpt").hide();
	}
	else if(domain == ""){
		displayMessage("Please Enter Domain");	
		$(".grid-table-rpt").hide();
	}
	else if(domainName == ""){
		displayMessage("Please Enter Domain");	
		$(".grid-table-rpt").hide();
	}	
	else{

		function onSuccess(data){
			clearMessage();
			$(".grid-table-rpt").show();
			$(".countryval").text(countriesText);
			$(".groupsval").text(groupsval);
			$(".domainval").text(domainName);
			$(".bgroupsval").text(businessgroupsval);
			$(".lentityval").text(legalentityval);
			$(".divisionval").text(divisionval);
			loadAssignedStatutoryList(data['unit_wise_assigned_statutories']);		
		}
		function onFailure(error){
			console.log(error);
		}
		//countryId, domainId,  clientId, businessGroupId, legalEntityId, divisionId, unitId, level1StatutoryId, applicableStatus,
		mirror.getAssignedStatutoryReport(parseInt(countries),  domainsVal,  groupid, businessgroupid, 
			lentityid, divisionid, unitid,  level1Statutoryid, applicableStatus,
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
});

function loadAssignedStatutoryList(data){
	$('.grid-table-rpt').show();
	$('.tbody-assigned-statutory-list tr').remove();
	var sno = 0;
	var gname;
	var bgname;
	var lename;
	var dname;
	
	$.each(data, function(key, value) {
		var tablefilter = $('#statutory-list .tr-filter');
		var clonefilter = tablefilter.clone();
	
		$('.groupsval').text(value["group_name"]);	
		$('.bgroupsval').text(value["business_group_name"]);	
		$('.lentityval').text(value["legal_entity_name"]);	
		$('.divisionval').text(value["division_name"]);	
		$('.tbody-assigned-statutory-list').append(clonefilter);
		
		var tableheading = $('#statutory-list .tr-heading');
		var cloneheading = tableheading.clone();
		$('.tbody-assigned-statutory-list').append(cloneheading);

	  	var list = data[key];
	  	var tableRow = $('#unit-details-list .table-unit-details-list .tablerow');
		var clone = tableRow.clone();
		var unitNameAddress = list['unit_name']+", "+list['address'];
		$('.unit-name-address', clone).text(unitNameAddress);
		$('.tbody-assigned-statutory-list').append(clone);
		var assignedList = list['assigned_statutories'];
		//Assigned Act List
	  	$.each(assignedList, function(k, val) { 
	  		var asImageName;
	  		var optedImageName;
	  		var tableRowAssigned = $('#act-heading .table-act-heading-list .tablerow');
			var cloneAssigned = tableRowAssigned.clone();
			var appStatus = assignedList[k]['applicable_status']
			if(appStatus == true){
				asImageName = "<img src='/images/tick1bold.png'>";
			}
			else{
				asImageName = "<img src='/images/deletebold.png'>";  
			}
			var optedStatus = assignedList[k]['compliance_opted_status']
			if(optedStatus == true){
				optedImageName = "<img src='/images/tick1bold.png'>";
			}
			else if(optedStatus == false){
				optedImageName = "<img src='/images/deletebold.png'>";  
			}
			else{
				optedImageName = "Nil";
			}
			var remarks = assignedList[k]['compliance_remarks'];
			if(remarks == null){
				remarks = "Nil";
			}
			$('.heading', cloneAssigned).text(assignedList[k]['level_1_statutory_name']);
			$('.act-applicable', cloneAssigned).html(asImageName);
			$('.act-opted', cloneAssigned).html(optedImageName);
			$('.act-remarks', cloneAssigned).text(remarks);
			var assignedRecord = assignedList[k]['compliances']; 
			$('.tbody-assigned-statutory-list').append(cloneAssigned);		
			$.each(assignedRecord, function(ke, valu) {
				var appStatus = assignedRecord[ke]['compliance_applicable_status']
				if(appStatus == true){
					asImageName = "<img src='/images/tick1bold.png'>";
				}
				else{
					asImageName = "<img src='/images/deletebold.png'>";  
				}
				var optedStatus = assignedRecord[ke]['compliance_opted_status']
				if(optedStatus == true){
					optedImageName = "<img src='/images/tick1bold.png'>";
				}
				else if(optedStatus == false){
					optedImageName = "<img src='/images/deletebold.png'>";  
				}
				else{
					optedImageName = "Nil";
				}
				var remarks = assignedRecord[ke]['compliance_remarks'];
				if(remarks == null){
					remarks = "Nil";
				}
				sno++; 
		  		var tableRowAssignedRecord = $('#statutory-list .table-statutory-list .tablerow');
				var cloneAssignedRecord = tableRowAssignedRecord.clone();
				$('.sno', cloneAssignedRecord).text(sno);
				$('.statutory-provision', cloneAssignedRecord).text(assignedRecord[ke]['statutory_provision']);
				$('.compliance-task', cloneAssignedRecord).text(assignedRecord[ke]['compliance_name']);
				$('.compliance-description', cloneAssignedRecord).text(assignedRecord[ke]['description']);
				$('.statutory-nature', cloneAssignedRecord).text(assignedRecord[ke]['statutory_nature']);
				$('.applicability-status', cloneAssignedRecord).html(asImageName);
				$('.opted', cloneAssignedRecord).html(optedImageName);
				$('.remarks', cloneAssignedRecord).text(remarks);
				$('.tbody-assigned-statutory-list').append(cloneAssignedRecord);

			});				
		});
	});
	$(".total-records").html("Total : "+sno+" records")
}

//Countries---------------------------------------------------------------------------------------------------------------
function loadCountries(countriesList){
	$.each(countriesList, function(key, values){
		var countryId = values['country_id'];
		var countryName = values['country_name'];
		$('#countries').append($('<option value="'+countryId+'">'+countryName+'</option>'));
	});
}
//Domains------------------------------------------------------------------------------------------------
function hidedomainslist(){
	document.getElementById('selectboxview-domains').style.display = 'none';
}
function loadauto_domains (textval) {
  document.getElementById('selectboxview-domains').style.display = 'block';
  var domains = domainsList;
  var suggestions = [];
  $('#selectboxview-domains ul').empty();
  if(textval.length>0){
    for(var i in domains){
      if (~domains[i]['domain_name'].toLowerCase().indexOf(textval.toLowerCase())) suggestions.push([domains[i]["domain_id"],domains[i]["domain_name"]]); 
    }
    var str='';
    for(var i in suggestions){
      str += '<li id="'+suggestions[i][0]+'" onclick="activate_text(this,\''+suggestions[i][0]+'\',\''+suggestions[i][1]+'\')">'+suggestions[i][1]+'</li>';
    }
    $('#selectboxview-domains ul').append(str);
    $("#domains").val('');
    }
}
//set selected autocomplte value to textbox
function activate_text (element,checkval,checkname) {
  $("#domainval").val(checkname);
  $("#domain").val(checkval);  
}
//Groups----------------------------------------------------------------------------------------------------------------------
function hidegroupslist(){
	document.getElementById('autocompleteview').style.display = 'none';
}
function loadauto_text (textval) {

  document.getElementById('autocompleteview').style.display = 'block';
  var groups = groupList;
  var suggestions = [];
  $('#autocompleteview ul').empty();
  if(textval.length>0){
    for(var i in groups){
      if (~groups[i]['group_name'].toLowerCase().indexOf(textval.toLowerCase())) suggestions.push([groups[i]["client_id"],groups[i]["group_name"]]); 
    }
    var str='';
    for(var i in suggestions){
      str += '<li id="'+suggestions[i][0]+'" onclick="activate_groups(this,\''+suggestions[i][0]+'\',\''+suggestions[i][1]+'\')">'+suggestions[i][1]+'</li>';
    }
    $('#autocompleteview ul').append(str);
    $("#group-id").val('');
    }
}
//set selected autocomplte value to textbox
function activate_groups (element,checkval,checkname) {
  $("#groupsval").val(checkname);
  $("#group-id").val(checkval);  
}

//businessgroups---------------------------------------------------------------------------------------------------------------
function hidebgroupslist(){
	document.getElementById('autocompleteview-bgroups').style.display = 'none';
}
function loadauto_businessgroups (textval) {
	if($("#businessgroupsval").val() == ''){
		$("#businessgroupid").val('');
	}
  document.getElementById('autocompleteview-bgroups').style.display = 'block';
  var bgroups = businessgroupsList;
  var suggestions = [];
  $('#autocompleteview-bgroups ul').empty();
  if(textval.length>0){
    for(var i in bgroups){
    	if(bgroups[i]['client_id']==$("#group-id").val()){
    		if (~bgroups[i]['business_group_name'].toLowerCase().indexOf(textval.toLowerCase())) suggestions.push([bgroups[i]["business_group_id"],bgroups[i]["business_group_name"]]); 	
    	}      
    }
    var str='';
    for(var i in suggestions){
      str += '<li id="'+suggestions[i][0]+'" onclick="activate_businessgroups(this,\''+suggestions[i][0]+'\',\''+suggestions[i][1]+'\')">'+suggestions[i][1]+'</li>';
    }
    $('#autocompleteview-bgroups ul').append(str);
    $("#businessgroupid").val('');
    }
}
function activate_businessgroups (element,checkval,checkname) {
  $("#businessgroupsval").val(checkname);
  $("#businessgroupid").val(checkval);
}
//Legal Entity---------------------------------------------------------------------------------------------------------------
function hidelentitylist(){
	document.getElementById('autocompleteview-lentity').style.display = 'none';
}
function loadauto_lentity (textval) {
	if($("#legalentityval").val() == ''){
		$("#legalentityid").val('');
	}
  document.getElementById('autocompleteview-lentity').style.display = 'block';
  var lentity = legalEntityList;
  var suggestions = [];
  $('#autocompleteview-lentity ul').empty();
  if(textval.length>0){
    for(var i in lentity){
    	if($("#businessgroupid").val()!=''){
    		if(lentity[i]['business_group_id']==$("#businessgroupid").val()){
    			if (~lentity[i]['legal_entity_name'].toLowerCase().indexOf(textval.toLowerCase())) suggestions.push([lentity[i]["legal_entity_id"],lentity[i]["legal_entity_name"]]); 	
    		}      
    	}
    	else{
    		if(lentity[i]['client_id']==$("#group-id").val()){
    			if (~lentity[i]['legal_entity_name'].toLowerCase().indexOf(textval.toLowerCase())) suggestions.push([lentity[i]["legal_entity_id"],lentity[i]["legal_entity_name"]]); 	
    		}     
    	}
    	
    }
    var str='';
    for(var i in suggestions){
      str += '<li id="'+suggestions[i][0]+'" onclick="activate_lentity(this,\''+suggestions[i][0]+'\',\''+suggestions[i][1]+'\')">'+suggestions[i][1]+'</li>';
    }
    $('#autocompleteview-lentity ul').append(str);
    $("#legalentityid").val('');
    }
}
//set selected autocomplte value to textbox
function activate_lentity (element,checkval,checkname) {
  $("#legalentityval").val(checkname);
  $("#legalentityid").val(checkval);
}
//Division---------------------------------------------------------------------------------------------------------------
function hidedivisionlist(){
	document.getElementById('autocompleteview-division').style.display = 'none';
}
function loadauto_division (textval) {
	if($("#divisionval").val() == ''){
		$("#divisionid").val('');
	}
  document.getElementById('autocompleteview-division').style.display = 'block';
  var division = divisionsList;
  var suggestions = [];
  $('#autocompleteview-division ul').empty();
  if(textval.length>0){
    for(var i in division){
    	if(division[i]['legal_entity_id']==$("#legalentityid").val()){
    		if (~division[i]['division_name'].toLowerCase().indexOf(textval.toLowerCase())) suggestions.push([division[i]["division_id"],division[i]["division_name"]]); 	
    	}      
    }
    var str='';
    for(var i in suggestions){
      str += '<li id="'+suggestions[i][0]+'" onclick="activate_division(this,\''+suggestions[i][0]+'\',\''+suggestions[i][1]+'\')">'+suggestions[i][1]+'</li>';
    }
    $('#autocompleteview-division ul').append(str);
    $("#divisionid").val('');
    }
}
function activate_division (element,checkval,checkname) {
  $("#divisionval").val(checkname);
  $("#divisionid").val(checkval);
}

//Units---------------------------------------------------------------------------------------------------------------
function hideunitlist(){
	document.getElementById('autocompleteview-unit').style.display = 'none';
}
function loadauto_unit (textval) {
	if($("#unitval").val() == ''){
		$("#unitid").val('');
	}
  document.getElementById('autocompleteview-unit').style.display = 'block';
  var unit = unitList;
  var suggestions = [];
  $('#autocompleteview-unit ul').empty();
  if(textval.length>0){
    for(var i in unit){
    	var getunitidname = unit[i]['unit_code']+"-"+unit[i]['unit_name'];
    	if($("#divisionid").val()==''){

    		if(unit[i]['legal_entity_id']==$("#legalentityid").val()){
    			if (~getunitidname.toLowerCase().indexOf(textval.toLowerCase())) suggestions.push([unit[i]["unit_id"],unit[i]["unit_name"],unit[i]["unit_code"]]); 	
    		}      	
    	}
    	else{
    		if(unit[i]['division_id']==$("#divisionid").val()){
    			if (~getunitidname.toLowerCase().indexOf(textval.toLowerCase())) suggestions.push([unit[i]["unit_id"],unit[i]["unit_name"],unit[i]["unit_code"]]); 	
    		}      	
    	}
    	
    }
    var str='';
    for(var i in suggestions){
      str += '<li id="'+suggestions[i][0]+'" onclick="activate_unit(this,\''+suggestions[i][0]+'\',\''+suggestions[i][1]+'\', \''+suggestions[i][2]+'\')">'+suggestions[i][2]+'-'+suggestions[i][1]+'</li>';
    }
    $('#autocompleteview-unit ul').append(str);
    $("#unitid").val('');
    }
}
function activate_unit (element,checkval,checkname, concatunit) {
  $("#unitval").val(concatunit+'-'+checkname);
  $("#unitid").val(checkval);
}
//Level 1 Statutories

function hidelevel1list(){
	document.getElementById('autocompleteview-level1').style.display = 'none';
}
function loadauto_level1 (textval) {
	if($("#level1val").val() == ''){
		$("#level1id").val('');
	}
  document.getElementById('autocompleteview-level1').style.display = 'block';
  var countryId = $("#countries").val();
  var domainId = $("#domain").val();
  var level1 = level1List[countryId][domainId];
  var suggestions = [];
  $('#autocompleteview-level1 ul').empty();
  if(textval.length>0){
    $.each(level1, function(i, value){    
    	if (~level1[i]['statutory_name'].toLowerCase().indexOf(textval.toLowerCase())) suggestions.push([level1[i]["statutory_id"],level1[i]["statutory_name"]]); 	
    });
    var str='';
    for(var i in suggestions){
      str += '<li id="'+suggestions[i][0]+'" onclick="activate_level1(this,\''+suggestions[i][0]+'\',\''+suggestions[i][1]+'\')">'+suggestions[i][1]+'</li>';
    }
    $('#autocompleteview-level1 ul').append(str);
    $("#legalentityid").val('');
    }
}
function activate_level1 (element,checkval,checkname) {
  $("#level1val").val(checkname);
  $("#level1id").val(checkval);
}
$(function() {
	// $( "#accordion" ).accordion({
	// 	heightStyle: "content"
	// });
	initialize();
});

