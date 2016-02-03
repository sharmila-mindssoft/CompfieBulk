var countriesList;
var domainsList;
var businessgroupsList;
var legalEntityList;
var divisionsList;
var unitList;
var level1List;
var countriesText;
var domainval;

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
		domainsList = data['domains'];
		businessgroupsList = data['businessgroups'];
		legalEntityList = data['legalentity'];
		divisionsList = data['divisions'];
		unitList = data['units'];
		level1List = data['level_1_statutories'];
		//loadCountries(countriesList);
	}
	function onFailure(error){
		console.log(error);
	}
	client_mirror.getStatutoryNotificationsListFilters(
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
	var countries = $("#country").val();
	var countriesNameVal = $("#countriesval").val();
	//Domain	
	var domain = $("#domain").val();
	var domainNameVal = $("#domainval").val();
	//Level 1 Statutories
	var level1id = $("#level1id").val();
	if(level1id == ''){
		level1id = null;
	}
	else{
		level1id = parseInt(level1id);
	}
	var level1NameVal = $("#level1idval").val();
	if(countries == ""){
		displayMessage("Please Enter Country");
	}
	else if(domain == ""){
		displayMessage("Please Enter Domain");	
	}
	else{
		function onSuccess(data){
			console.log(data);
			$(".grid-table-rpt").show();
			$(".snCountryVal").text(countriesNameVal);
			$(".snDomainVal").text(domainNameVal);
			loadStatutoryNotificationsList(data['country_wise_notifications']);		
		}
		function onFailure(error){
			console.log(error);
		}
		
		client_mirror.getStatutoryNotificationsReportData(parseInt(countries), parseInt(domain), level1id,
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
function getDomainName(domainId){
	var domainName;
	$.each(domainsList, function(key, value){
		if(domainsList[key]['domain_id'] == domainId){
			domainName = domainsList[key]['domain_name'];
		}
	});
	return domainName;
}

function loadStatutoryNotificationsList(data){
	$('.tbody-statutory-notifications-list tr').remove();
	var sno = 0;
	console.log(data);
	$.each(data, function(key, value) {
		var tableRowHeading = $('#templates .table-statutory-notifications-list .table-row-heading');
		var cloneHeading = tableRowHeading.clone();
		var domainId = data[key]['domain_id'];
		$('.heading', cloneHeading).text(getDomainName(domainId));
		$('.tbody-statutory-notifications-list').append(cloneHeading);
	  	var list = data[key]['notifications'];
	  	$.each(list, function(k, val) { 
		  	var arr = [];
			var tableRow = $('#templates .table-statutory-notifications-list .table-row-values');
			var clone = tableRow.clone();
			sno = sno + 1;
			$('.sno', clone).text(sno);
			$('.statutory-provision', clone).html(list[k]['statutory_provision']);
			$('.statutory-notificaions', clone).html(list[k]['notification_text']);
			$('.date-time', clone).html(list[k]['date_and_time']);
			$('.tbody-statutory-notifications-list').append(clone);
		});
	});
	$(".total-records").html("Total : "+sno+" records")
}


//Country----------------------------------------------------------------------------------------------------------------------
function hidecountrylist(){
	document.getElementById('selectboxview-country').style.display = 'none';
}
function loadauto_country (textval) {
  document.getElementById('selectboxview-country').style.display = 'block';
  var countries = countriesList;
  var suggestions = [];
  $('#selectboxview-country ul').empty();
  if(textval.length>0){
    for(var i in countries){
      if (~countries[i]['country_name'].toLowerCase().indexOf(textval.toLowerCase())) suggestions.push([countries[i]["country_id"],countries[i]["country_name"]]); 
    }
    var str='';
    for(var i in suggestions){
      str += '<li id="'+suggestions[i][0]+'" onclick="activate_text(this,\''+suggestions[i][0]+'\',\''+suggestions[i][1]+'\')">'+suggestions[i][1]+'</li>';
    }
    $('#selectboxview-country ul').append(str);
    $("#country").val('');
    }
}
//set selected autocomplte value to textbox
function activate_text (element,checkval,checkname) {
  $("#countryval").val(checkname);
  $("#country").val(checkval);  
}

//Domains---------------------------------------------------------------------------------------------------------------
function hidedomainslist(){
	document.getElementById('selectboxview-domains').style.display = 'none';
}
function loadauto_domains (textval) {
  document.getElementById('selectboxview-domains').style.display = 'block';
  var domains = domainsList;
  var suggestions = [];
  $('#autocompleteview-domains ul').empty();
  if(textval.length>0){
    for(var i in domains){
    	if (~domains[i]['domain_name'].toLowerCase().indexOf(textval.toLowerCase())) suggestions.push([domains[i]["domain_id"],domains[i]["domain_name"]]); 	
    }
    var str='';
    for(var i in suggestions){
      str += '<li id="'+suggestions[i][0]+'" onclick="activate_domains(this,\''+suggestions[i][0]+'\',\''+suggestions[i][1]+'\')">'+suggestions[i][1]+'</li>';
    }
    $('#selectboxview-domains ul').append(str);
    $("#domain").val('');
    }
}
function activate_domains (element,checkval,checkname) {
  $("#domainval").val(checkname);
  $("#domain").val(checkval);
}
//Level1 Statutory---------------------------------------------------------------------------------------------------------------
function hidedomainslist(){
	document.getElementById('selectboxview-domains').style.display = 'none';
}
function loadauto_domains (textval) {
  document.getElementById('selectboxview-domains').style.display = 'block';
  var domains = domainsList;
  var suggestions = [];
  $('#autocompleteview-domains ul').empty();
  if(textval.length>0){
    for(var i in domains){
    	if (~domains[i]['domain_name'].toLowerCase().indexOf(textval.toLowerCase())) suggestions.push([domains[i]["domain_id"],domains[i]["domain_name"]]); 	
    }
    var str='';
    for(var i in suggestions){
      str += '<li id="'+suggestions[i][0]+'" onclick="activate_domains(this,\''+suggestions[i][0]+'\',\''+suggestions[i][1]+'\')">'+suggestions[i][1]+'</li>';
    }
    $('#selectboxview-domains ul').append(str);
    $("#domain").val('');
    }
}
function activate_domains (element,checkval,checkname) {
  $("#domainval").val(checkname);
  $("#domain").val(checkval);
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

//Level 1 Statutory---------------------------------------------------------------------------------------------------------------
function hidelevel1list(){
	document.getElementById('autocompleteview-level1').style.display = 'none';
}
function loadauto_level1 (textval) {
	if($("#level1val").val() == ''){
		$("#level1id").val('');
	}
  document.getElementById('autocompleteview-level1').style.display = 'block';
  var countryId = $("#country").val();
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
	initialize();
});
