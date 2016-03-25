var countriesList;
var businessgroupsList;
var divisionsList;
var domainsList;
var legalEntityList;
var unitList;

var countriesText;
var businessgroupsval;
var legalentityval;
var divisionval;
var unitval;

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
		countriesList = data['countries'];
		businessgroupsList = data['business_groups'];
		divisionsList = data['divisions'];
		domainsList = data['domains'];
		legalEntityList = data['legal_entities'];
		unitList = data['units'];
	}
	function onFailure(error){
		console.log(error);
	}
	client_mirror.getClientDetailsReportFilters(
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
    loadunitdetailsreport("show");
});
$("#export-button").click(function(){ 
    loadunitdetailsreport("export");
});
function loadunitdetailsreport(buttontype){
	var countries = $("#country").val();
	countriesText = $("#countryval").val();
	
	var bgroups = $("#businessgroupid").val();
	if(bgroups != ''){ 
		var businessgroupid = parseInt(bgroups);
	}
	else{
		var businessgroupid = null;
	}
	businessgroupsval = $("#businessgroupsval").val();
	var legalentity = $("#legalentityid").val();
	if(legalentity != ''){
		var lentityid = parseInt(legalentity);
	}
	else{
		var lentityid = null;
	}
	legalentityval = $("#legalentityval").val();
	var division = $("#divisionid").val();
	if(division != ''){
		var divisionid = parseInt(division);
	}
	else{
		var divisionid = null;
	}
	divisionval = $("#divisionval").val();
	var units = $("#unitid").val();
	if(units != ''){
		var unitid = parseInt(units);
	}
	else{
		var unitid = null;
	}
	unitval = $("#unitval").val();
	var domain = $("#domain").val();
	if(domain != ''){
		var arrayDomainsVal = domain.split(",");
		var arrayDomains = [];
		for(var j = 0; j < arrayDomainsVal.length; j++){
			arrayDomains[j] = parseInt(arrayDomainsVal[j]);
		} 
		var domainsVal = arrayDomains;
	}
	if(domain == ''){
		var domainsVal = null;
	}	

	if(countries == ""){
		displayMessage("Select Country");
	}
	else{
		function onSuccess(data){
      clearMessage();
			$(".grid-table-rpt").show();
			loadUnitDetailsList(data['units']);		
      if(buttontype == "export"){
        client_mirror.exportToCSV(data, 
          function (error, response) {
              if (error == null){
                  var download_url = response["link"];
                  window.open(download_url, '_blank');
              }
              else {
                  displayMessage(error);
              }
          }
        );
      }
		}
		function onFailure(error){
			console.log(error);
		}
		client_mirror.getClientDetailsReportData(parseInt(countries), businessgroupid,	
			lentityid, divisionid, unitid,  domainsVal,
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
}
function getdomainnames(list){
	var domainsNames = '';
	$.each(domainsList, function(key, value){
		var domainid = domainsList[key]['domain_id'];
		var domainname = domainsList[key]['domain_name'];
		
		if(jQuery.inArray(domainid, list ) > -1){
			domainsNames += domainname + ", ";
		}
	});				
	return domainsNames;
}
function getBusinessGroupsName(businessgroupid){
	var businessGroupName;
	if(businessgroupid != null){
		$.each(businessgroupsList, function(key, value){
			if(businessgroupsList[key]['business_group_id'] == businessgroupid){
				businessGroupName = businessgroupsList[key]['business_group_name'];
			}
		});	
	}
	else{
		businessGroupName = '';
	}
	return businessGroupName;
}

function getLegalEntityName(legalentityid){
	var legalEntityName;
	if(legalentityid != null){
		$.each(legalEntityList, function(key, value){
			if(legalEntityList[key]['legal_entity_id'] == legalentityid){
				legalEntityName = legalEntityList[key]['legal_entity_name'];
			}
		});	
	}
	else{
		legalEntityName = '';
	}
	return legalEntityName;
}
function getDivisionName(divisionid){
	var divisionName;
	if(divisionid != null){
		$.each(divisionsList, function(key, value){
			if(divisionsList[key]['division_id'] == divisionid){
				divisionName = divisionsList[key]['division_name'];
			}
		});	
	}
	else{
		divisionName = '';
	}
	return divisionName;
}

function loadUnitDetailsList(data){

    $('.tbody-unitdetails-list tr').remove();
    var sno = 0;
    
    $.each(data, function(key, value) {
        var tableRowHeading = $('#templates .table-unitdetails-list .filter-heading-list');
        var cloneHeading = tableRowHeading.clone();
        $('.filter-country-name', cloneHeading).text(countriesText);
        $('.filter-business-group-name', cloneHeading).text(getBusinessGroupsName(data[key]['business_group_id']));
        $('.filter-legal-entity-name', cloneHeading).text(getLegalEntityName(data[key]['legal_entity_id']));
        $('.filter-division-name', cloneHeading).text(getDivisionName(data[key]['division_id']));
        $('.unitdetails-list .tbody-unitdetails-list').append(cloneHeading);

        var tableRowHeadingth = $('#templates .table-unitdetails-list .heading-list');
        var cloneHeadingth = tableRowHeadingth.clone();
        $('.unitdetails-list .tbody-unitdetails-list').append(cloneHeadingth);

        var list = data[key]['units'];
        $.each(list, function(k, valu) { 
            var tableRowvalues = $('#templates .table-unitdetails-list .table-row');
            var cloneval = tableRowvalues.clone();
            sno = sno + 1;
            $('.sno', cloneval).text(sno);
            $('.unit-name', cloneval).html(list[k]['unit_code']+" - "+list[k]['unit_name']);
            $('.domain-name', cloneval).html(getdomainnames(list[k]['domain_ids']));
            $('.unit-address', cloneval).html(list[k]['unit_address']);
            $('.unit-location', cloneval).html(list[k]['geography_name']);
            $('.pincode', cloneval).html(list[k]['postal_code']);
            $('.unitdetails-list .tbody-unitdetails-list').append(cloneval);        
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

//businessgroups---------------------------------------------------------------------------------------------------------------
function hidebgroupslist(){
	document.getElementById('autocompleteview-bgroups').style.display = 'none';
}
function loadauto_businessgroups (textval) {
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
  document.getElementById('autocompleteview-unit').style.display = 'block';
  var unit = unitList;
  var suggestions = [];
  $('#autocompleteview-unit ul').empty();
  if(textval.length>0){
    for(var i in unit){
    	if($("#divisionid").val()==''){
    		if(unit[i]['legal_entity_id']==$("#legalentityid").val()){
    			if (~unit[i]['unit_name'].toLowerCase().indexOf(textval.toLowerCase())) suggestions.push([unit[i]["unit_id"],unit[i]["unit_name"]]); 	
    		}      	
    	}
    	else{
    		if(unit[i]['division_id']==$("#divisionid").val()){
    			if (~unit[i]['unit_name'].toLowerCase().indexOf(textval.toLowerCase())) suggestions.push([unit[i]["unit_id"],unit[i]["unit_name"]]); 	
    		}      	
    	}
    	
    }
    var str='';
    for(var i in suggestions){
      str += '<li id="'+suggestions[i][0]+'" onclick="activate_unit(this,\''+suggestions[i][0]+'\',\''+suggestions[i][1]+'\')">'+suggestions[i][1]+'</li>';
    }
    $('#autocompleteview-unit ul').append(str);
    $("#unitid").val('');
    }
}
function activate_unit (element,checkval,checkname) {
  $("#unitval").val(checkname);
  $("#unitid").val(checkval);
}
//Domains---------------------------------------------------------------------------------------------------------------
function hidemenudomains(){
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


$(function() {
	$(".grid-table-rpt").hide();
	initialize();
});