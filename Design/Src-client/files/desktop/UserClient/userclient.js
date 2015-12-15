var countriesList;
var businessGroupsList;
var legalEntitiesList;
var divisionList;
var domainList;
var unitList;
$(function() {
	$("#user-add").hide();
	initialize();
});
$(function() {
 	$('.service_provider').hide();
	$('#usertype').change(function () {
		if($("#usertype").val()=='Service Provider'){
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
  $(".error-message").html('');  
  $("#user-privilege-id").val('');
  	
	function success(status, data){		
	
	}
	function failure(status, data){
		console.log(status);
	}
	mirror.getClientUsers("ClientAdminAPI", success, failure);
});
$("#btn-user-cancel").click(function(){
	$("#user-add").hide();
	$("#user-view").show();
});
function initialize(){
	function success(status, data){
		countriesList=data['countries'];
		businessGroupsList=data['business_groups'];
		legalEntitiesList=data['legal_entities'];
		divisionList=data['divisions'];
		domainList=data['domains'];
	}
	function failure(status, data){
		console.log(status);
	}
	mirror.getClientUsers("ClientAdminAPI", success, failure);
}

function hidemenu() {
	document.getElementById('selectboxview-country').style.display = 'none';
}

function loadautocountry () {
	document.getElementById('selectboxview-country').style.display = 'block';
	var editcountryval=[];
	if($("#country").val() != ''){
		editcountryval = $("#country").val().split(",");
	}
	//alert(editcountryval[0]+"---"+editcountryval[1]);
	var countries = countriesList;

	$('#selectboxview-country ul').empty();
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
					console.log(editlegalentitiesval.length);
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
	var selNames='';
	var totalcount =  $(".active_selectbox_legal_entities").length;
	$(".active_selectbox_legal_entities").each( function( index, el ) {

		if (index === totalcount - 1) {
			selids = selids+el.id;
			selNames = selNames+$(this).text();
		}else{
			selids = selids+el.id+",";
			selNames = selNames+$(this).text()+",";
		}    
	});
	$("#legal-entities-selected").val(totalcount+" Selected");
	$("#legal-entities").val(selids);
}
// Divisions----------------------------------------------------------------------------------------------------------------------
function hidemenudivision() {
	document.getElementById('selectboxview-division').style.display = 'none';
}
function loadautodivision () {
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