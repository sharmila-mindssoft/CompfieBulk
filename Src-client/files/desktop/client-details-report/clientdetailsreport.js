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
		groupList = data['group_companies'];
		legalEntityList = data['legal_entities'];
		unitList = data['units'];
		loadCountries(countriesList);
	}
	function onFailure(error){
		console.log(error);
	}
	mirror.getClientDetailsReportFilters(
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
	var groupid = $("#group-id").val();
	groupsval = $("#groupsval").val();
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
		displayMessage("Please Select Country");
	}
	else if(groupid == ""){
		displayMessage("Please Enter Groups");	
	}
	else{
		function onSuccess(data){
			$(".grid-table-rpt").show();
			$(".countryval").text(countriesText);
			$(".groupsval").text(groupsval);
			$(".bgroupsval").text(businessgroupsval);
			$(".lentityval").text(legalentityval);
			$(".divisionval").text(divisionval);
			loadClientDetailsList(data['units']);		
		}
		function onFailure(error){
			console.log(error);
		}
		mirror.getClientDetailsReport(parseInt(countries), parseInt(groupid), businessgroupid,	
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
});
function loadClientDetailsList(data){
	$('.tbody-clientdetails-list tr').remove();
	var sno = 0;
	$.each(data, function(key, value) {
	  	var list = data[key]['units'];
	  	$.each(list, function(k, val) { 
		  	var arr = [];
			var tableRow = $('#templates .table-clientdetails-list .table-row');
			var clone = tableRow.clone();
			sno = sno + 1;
			$('.sno', clone).text(sno);
			$('.unit-name', clone).html(list[k]['unit_name']);
			var domainsNames = '';
			arr = list[k]['domain_ids'];
			$.each(domainsList, function(key, value){
				var domianid = domainsList[key]['domain_id'];
				var domainname = domainsList[key]['domain_name']
				if(jQuery.inArray(domianid, arr ) > -1){
					domainsNames += domainname + ", ";
				}
			});					
			$('.domain-name', clone).html(domainsNames);
			$('.unit-address', clone).text(list[k]['unit_address']+", "+list[k]['geography_name']);
			$('.pincode', clone).html(list[k]['postal_code']);
			$('.tbody-clientdetails-list').append(clone);
		});
	});
	$(".total-records").html("Total : "+sno+" records")
}

//Countries---------------------------------------------------------------------------------------------------------------
function loadCountries(countriesList){
	$.each(countriesList, function(key, values){
		var countryId = countriesList[key]['country_id'];
		var countryName = countriesList[key]['country_name'];
		$('#countries').append($('<option value="'+countryId+'">'+countryName+'</option>'));
	});
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
      str += '<li id="'+suggestions[i][0]+'" onclick="activate_text(this,\''+suggestions[i][0]+'\',\''+suggestions[i][1]+'\')">'+suggestions[i][1]+'</li>';
    }
    $('#autocompleteview ul').append(str);
    $("#group-id").val('');
    }
}
//set selected autocomplte value to textbox
function activate_text (element,checkval,checkname) {
  $("#groupsval").val(checkname);
  $("#group-id").val(checkval);  
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
//Domains------------------------------------------------------------------------------------------------


function hidedomainmenu() {
	document.getElementById('selectboxview-domains').style.display = 'none';
}

function loadauto_domains() {
	document.getElementById('selectboxview-domains').style.display = 'block';
	var editdomainval=[];
	if($("#domain").val() != ''){
		editdomainval = $("#domain").val().split(",");
	}
	var domains = domainsList;
	$('#selectboxview-domains ul').empty();
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
  $('#selectboxview-domains ul').append(str);
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
	
}

$(function() {
	$(".grid-table-rpt").hide();
	initialize();
});