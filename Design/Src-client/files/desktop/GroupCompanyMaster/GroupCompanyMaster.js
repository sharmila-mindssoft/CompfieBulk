var groupList;
var countryList;
var domainList;
var businessGroupList;
var legalEntitiesList;
var divisionList;
var countryFulList;
var countc=0;
var industryList;
var unitList;
var geographyList;
var geographyLevelList;
var unitcodecount=1001;
$(function() {
	$("#clientunit-add").hide();
	initialize();
});
function initialize(){
	function success(status, data){
		groupList=data['group_companies'];
		businessGroupList=data['business_groups'];
		legalEntitiesList=data['legal_entities'];
		divisionList=data['divisions'];
		countryFulList=data['countries'];
		geographyLevelList=data['geography_levels'];		
		geographyList=data['geographies'];
		industryList=data['industries'];
		domainList=data['domains'];
		loadClientsList(data);

	}
	function failure(status, data){
		console.log(status);
		$(".error-message").html(status);
	}
	mirror.getClients("TechnoAPI", success, failure);
}
//Load Get Client List -----------------------------------------------------------------------------------------
function loadClientsList(clientunitsList){
 	$(".tbody-clientunit-list").find("tr").remove();
  var sno=0;
	var imageName, title;	
	for(var clients in groupList){
		var clientname=groupList[clients]['group_name'];
		var clientid=groupList[clients]['client_id'];
		var isActive=groupList[clients]['is_active'];
		for (var bgroups in businessGroupList){
			var bgclientid=businessGroupList[bgroups]['client_id'];
			if(clientid==bgclientid){
				var bgroupid=businessGroupList[bgroups]['business_group_id'];
				var bgroupsname=businessGroupList[bgroups]['business_group_name'];
				for (var lentity in legalEntitiesList){
					var lebgroupid=legalEntitiesList[lentity]['business_group_id'];
					if(lebgroupid==bgroupid){
						var lentitiesname=legalEntitiesList[lentity]['legal_entity_name'];
						var lentitiesid=legalEntitiesList[lentity]['legal_entity_id'];	
						for(var division in divisionList){
							var dlentityid=divisionList[division]['legal_entity_id'];
							var divisionname=divisionList[division]['division_name'];
							var divisionid=divisionList[division]['division_id'];

							if(lentitiesid==dlentityid){
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
								var tableRow=$('#templates .table-clientunit-list .table-row');
								var clone=tableRow.clone();
								sno = sno + 1;
								$('.sno', clone).text(sno);
								$('.group-name', clone).text(clientname);
								$('.business-group-name', clone).text(bgroupsname);
								$('.legal-entity-name', clone).text(lentitiesname);
								$('.division-name', clone).text(divisionname);
								$('.edit', clone).html('<img src="/images/icon-edit.png" id="editid" onclick="clientunit_edit('+clientid+','+bgroupid+','+lentitiesid+','+divisionid+')"/>');
								$('.is-active', clone).html('<img src="/images/'+imageName+'" title="'+title+'" onclick="clientunit_active('+clientid+', '+divisionid+', '+statusVal+')"/>');
								$('.tbody-clientunit-list').append(clone);	
							}
						}
					}
				}	
			}			
		}
	}
}
//Add Button-------------------------------------------------------------------------------------------------
$("#btn-clientunit-add").click(function(){
	$("#clientunit-add").show();
	$("#clientunit-view").hide();
	$("#client-unit-id").val('');	
 	$(".error-message").html('');
 	var x=document.getElementsByTagName("input");
 	for(i = 0; i<=x.length-1; i++){
  	if(x.item(i).type!="submit" ){ x.item(i).value = ""; }
  }
  $('#group-select:gt(0)').empty();
  $('#businessgroup-select:gt(0)').empty();
  $('#entity-select:gt(0)').empty();
  $('#division-select:gt(0)').empty();
  $('.industry').empty();
  loadClientGroups(groupList);

});

//Cancel Button ----------------------------------------------------------------------------------------------
$("#btn-clientunit-cancel").click(function(){
	$("#clientunit-add").hide();
	$("#clientunit-view").show();
});

//Load All Groups---------------------------------------------------------------------------------------------
function loadClientGroups(groupsList){
	for(var groupList in groupsList){
		var groupId=groupsList[groupList]['client_id'];
		var groupName=groupsList[groupList]['group_name'];
		$('#group-select').append($('<option value="'+groupId+'">'+groupName+'</option>'));
	}
}

//Load Business Groups  ---------------------------------------------------------------------------------------------
function getBusinessGroups(groupId) {
	$('#businessgroup-select').find('option:gt(0)').remove();
	for (var i in businessGroupList){
		if(businessGroupList[i]['client_id']==groupId){
			var bgroupId=businessGroupList[i]['business_group_id'];
			var bgroupName=businessGroupList[i]['business_group_name'];
			$('#businessgroup-select').append($('<option value="'+bgroupId+'">'+bgroupName+'</option>'));
		}
	}
	$('#entity-select').find('option:gt(0)').remove();	
	for (var i in legalEntitiesList){
		if(legalEntitiesList[i]['client_id']==groupId){
			var lentityId=legalEntitiesList[i]['legal_entity_id'];
			var lentityName=legalEntitiesList[i]['legal_entity_name'];
			$('#entity-select').append($('<option value="'+lentityId+'">'+lentityName+'</option>'));
		}
	}
}
//Load LegalEntities ---------------------------------------------------------------------------------------------
function getLegalEntity(busgroupId) {
	$('#entity-select').find('option:gt(0)').remove();
	for (var i in legalEntitiesList){
		if(legalEntitiesList[i]['business_group_id']==busgroupId){
			var lentityId=legalEntitiesList[i]['legal_entity_id'];
			var lentityName=legalEntitiesList[i]['legal_entity_name'];
			$('#entity-select').append($('<option value="'+lentityId+'">'+lentityName+'</option>'));
		}
	}
}

//Load Divisions ---------------------------------------------------------------------------------------------
function getDivision(lentityId) {
	$('#division-select').find('option:gt(0)').remove();
	for (var i in divisionList){
		if(divisionList[i]['legal_entity_id']==lentityId){
			var divisionId=divisionList[i]['division_id'];
			var divisionName=divisionList[i]['division_name'];
			$('#division-select').append($('<option value="'+divisionId+'">'+divisionName+'</option>'));
		}
	}
}
//Add Country Wise List ----------------------------------------------------------------------------------------
$("#add-country-row").click(function(){
	var groupId=$("#group-select").val();
	if(groupId==''){
		$(".error-message").html("Select Group First");
	}
	else{
		for (var i in groupList){
			if(groupList[i]['client_id']==groupId){ countryList=groupList[i]['country_ids'];
			}
		}
		var countryArray=[];
		var countrySplit=countryList.split(',');
		var countryCount=countryList.split(',').length;
		countryArray = countryArray.concat(countrySplit); 
		
		if(countryCount>countc){			
			var divCountryAddRow=$('#templates .grid-table');
			var clone=divCountryAddRow.clone();	
			$('.btable', clone).addClass('table-'+countryArray[countc]);
			$('.countryval', clone).addClass('countryval-'+countryArray[countc]);
			$('.country', clone).addClass('country-'+countryArray[countc]);
			$('.autocompleteview', clone).addClass('autocompleteview-'+countryArray[countc]);
			$('.ulist-text', clone).addClass('ulist-text-'+countryArray[countc]);			
			$('.geography-levels', clone).addClass('glevel-'+countryArray[countc]+'-'+1);
			$('.unit-location', clone).addClass('unitlocation-'+countryArray[countc]+'-'+1);
			$('.unit-location-ids', clone).addClass('unitlocation-ids-'+countryArray[countc]+'-'+1);
			$('.auto-complete-unit-location', clone).addClass('auto-complete-unit-location-'+countryArray[countc]+'-'+1);
			$('.unitlocationlist-text', clone).addClass('unitlocationlist-text-'+countryArray[countc]+'-'+1);
			$('.full-location-list', clone).addClass('full-location-list-'+countryArray[countc]+'-'+1);
			$('.unitcode-checkbox', clone).addClass('unitcode-checkbox-'+countryArray[countc]);
			$('.unit-code', clone).addClass('unit-code-'+countryArray[countc]);
			$('.unit-code', clone).addClass('unit-code-'+countryArray[countc]+'-'+1);
			$('.unit-name', clone).addClass('unit-name-'+countryArray[countc]+'-'+1);
			$('.industry', clone).addClass('industry-'+countryArray[countc]+'-'+1);
			$('.unit-address', clone).addClass('unit-address-'+countryArray[countc]+'-'+1);
			$('.postal-code', clone).addClass('postal-code-'+countryArray[countc]+'-'+1);
			$('.domain-list', clone).addClass('domain-list-'+countryArray[countc]+'-'+1);
			$('.domainselected', clone).addClass('domainselected-'+countryArray[countc]+'-'+1);
			$('.domain', clone).addClass('domain-'+countryArray[countc]+'-'+1);
			$('.domain-selectbox-view', clone).addClass('domain-selectbox-view-'+countryArray[countc]+'-'+1);
			$('.ul-domain-list', clone).addClass('ul-domain-list-'+countryArray[countc]+'-'+1);		
			$('.add-unit-row img', clone).addClass('table-addunit-'+countryArray[countc]);
			$('.tbody-unit-list', clone).addClass('tbody-unit-'+countryArray[countc]);
			$('.no-of-units', clone).addClass('no-of-units-'+countryArray[countc]);
			$('.no-of-units-'+countryArray[countc], clone).val(1);
			$('.add-country-unit-list').append(clone);			
			countc++;
		}
		else{
			$(".error-message").html(countryCount+" Countries Are Allowed for this group");
		}
	}
});
//Add Unit for individual Rows---------------------------------------------------------------------------------

function addNewUnitRow(str){
	var tableclassname=$(str).parents('table').attr('class');
	var tableclass=tableclassname.split(" ");
	var countval=tableclass[1].split("-").pop();
	var tbodyclassname=$('.'+tableclass[1]).find('tbody:eq(1)').attr('class');
	var tbodyclasses=tbodyclassname.split(" ");
	var lastclassname=$('.'+tbodyclasses[1]).find('tr:last .geography-levels').attr('class');
	var lastClass = lastclassname.split(' ').pop();
	var lastClassval = parseInt(lastClass.split('-').pop());
	var divUnitAddRow=$('#templatesUnitRow .table-UnitRow-list .table-row');
	var clone1=divUnitAddRow.clone();	
	$('.geography-levels', clone1).addClass('glevel-'+countval+'-'+(lastClassval+1));
	$('.unit-location', clone1).addClass('unitlocation-'+countval+'-'+(lastClassval+1));
	$('.unit-location-ids', clone1).addClass('unitlocation-ids-'+countval+'-'+(lastClassval+1));
	$('.auto-complete-unit-location', clone1).addClass('auto-complete-unit-location-'+countval+'-'+(lastClassval+1));
	$('.unitlocationlist-text', clone1).addClass('unitlocationlist-text-'+countval+'-'+(lastClassval+1));
	$('.full-location-list', clone1).addClass('full-location-list-'+countval+'-'+(lastClassval+1));
	$('.unit-code', clone1).addClass('unit-code-'+countval);
	$('.unit-code', clone1).addClass('unit-code-'+countval+'-'+(lastClassval+1));
	$('.unit-name', clone1).addClass('unit-name-'+countval+'-'+(lastClassval+1));
	$('.industry', clone1).addClass('industry-'+countval+'-'+(lastClassval+1));
	$('.unit-address', clone1).addClass('unit-address-'+countval+'-'+(lastClassval+1));
	$('.postal-code', clone1).addClass('postal-code-'+countval+'-'+(lastClassval+1));
	$('.domain-list', clone1).addClass('domain-list-'+countval+'-'+(lastClassval+1));
	$('.domainselected', clone1).addClass('domainselected-'+countval+'-'+(lastClassval+1));
	$('.domain', clone1).addClass('domain-'+countval+'-'+(lastClassval+1));
	$('.domain-selectbox-view', clone1).addClass('domain-selectbox-view-'+countval+'-'+(lastClassval+1));
	$('.ul-domain-list', clone1).addClass('ul-domain-list-'+countval+'-'+(lastClassval+1));
	$('.no-of-units-'+countval).val(parseInt($('.no-of-units-'+countval).val())+1);
	$('.'+tbodyclasses[1]).append(clone1);
}
//Auto Generate Unit Code------------------------------------------------------------------------------------------
function autoGenerateUnitCode(classval){
	var className = classval.split(' ');
	var groupId=$("#group-select :selected").val();
	var groupname=$.trim($("#group-select :Selected").text());	
	var get3Chars=groupname.slice(0, 3);	
	var getLastNumber=className[1].split('-').pop();
	var countryname=$('.country-'+getLastNumber).val();
	var totUnitcode=$('.unit-code-'+getLastNumber).length
	if($('.'+className[1]).prop("checked")==true){
		for(var i=1;i<=totUnitcode; i++){
			$('.unit-code-'+getLastNumber+'-'+i).val(get3Chars+unitcodecount);	
			unitcodecount++;
		}		
	}
	if($('.'+className[1]).prop("checked")==false){
		$('.unit-code-'+getLastNumber).val('');
	}

}

//Load Geography Levels -------------------------------------------------------------------------------------------
function loadglevels(classval){
	var lastClass = classval.split(' ').pop();
	var checkval=lastClass.split('-');	
	var countryvalue=$('.countryval-'+checkval[1]).val();
	var countryid=$('.country-'+checkval[1]).val();
	if(countryvalue==''){
		$('.error-message').html('Enter Country First');
	}
	else{
		$('.'+lastClass).empty();
		for(var glevel in geographyLevelList[countryid]){
			var glevellist = geographyLevelList[countryid][glevel];
	 		$('.'+lastClass).append($('<option value="'+glevellist['level_id']+'">'+glevellist['level_name']+'</option>'));
		}	
	}
}

//load industry type--------------------------------------------------------------------------------------------------
function industrytype(classval){
	var lastClass = classval.split(' ').pop();
	var checkval=lastClass.split('-');
	$('.'+lastClass).empty();
	for(var industry in industryList){
		$('.'+lastClass).append($('<option value="'+industryList[industry]['industry_id']+'">'+industryList[industry]['industry_name']+'</option>'));
	}
}

//Submit Record -----------------------------------------------------------------------------------------
$("#btn-clientunit-submit").click(function(){
	var clientunitIdValue = $("#client-unit-id").val();
	var groupNameValue = $("#group-select").val();
	var businessgrouptextValue = $("#businessgroup-text").val();		
	var businessgroupValue = $("#businessgroup-select").val();	
	var businessgroupName = $("#businessgroup-select :selected").text();
	var lentitytextValue = $("#entity-text").val();			
	var legalEntityValue = $("#entity-select").val();
	var legalEntityName = $("#entity-select :selected").text();
	var divisiontextValue = $("#division-text").val();		
	var divisionValue = $("#division-select").val();
	var divisionName = $("#division-select :selected").text();
	if(groupNameValue==''){
		$(".error-message").html("Please Select Group");
	}
	//else if(legalEntityValue=='' && lentitytextValue==''){
			//$(".error-message").html("Please Select Legal Entity or Create New One");
	//}
	else if(clientunitIdValue==''){		
		function success(status, data){
			if(status == 'SaveClientSuccess') {
		    	$("#clientunit-add").hide();
	  			$("#clientunit-view").show();
	  			initialize();
	  		}
	  		 else {
      			$(".error-message").html(status);
      		}	
	    }
		function failure(status, data){
			$(".error-message").html(status);
		}

	 	var businessGroup = {}
	 	if(businessgrouptextValue==''){
	 		businessGroup["business_group_id"] = parseInt(businessgroupValue);
    	if(businessgroupValue!=''){
    		businessGroup["business_group_name"] = businessgroupName;	
    	}
	    else{
	    	businessGroup["business_group_name"] = '';	
	    }	
	 	}
	 	else{
	 		businessGroup["business_group_id"] = '';
     	businessGroup["business_group_name"] = businessgrouptextValue;   
	 	}
	 	var legalEntity = {}
	 	if(lentitytextValue==''){
	 		legalEntity["legal_entity_id"] = parseInt(legalEntityValue);
    	if(legalEntityValue!=''){
    		legalEntity["legal_entity_name"] = legalEntityName;	
    	}
	    else{
	    	legalEntity["legal_entity_name"] = '';	
	    }	
	 	}
	 	else{
	 		legalEntity["legal_entity_id"] = '';
     	legalEntity["legal_entity_name"] = lentitytextValue;   
	 	}
	 	var division = {}
	 	if(divisiontextValue==''){
	 		division["division_id"] = parseInt(divisionValue);
    	if(divisionValue!=''){
    		division["division_name"] = divisionName;	
    	}
	    else{
	    	division["division_name"] = '';	
	    }	
	 	}
	 	else{
	 		division["division_id"] = '';
     	division["division_name"] = divisiontextValue;   
	 	}

    var countryWiseUnits = [];
    var numItemsCountry = $('.country').length;
    for(var i=1; i<numItemsCountry;i++){
    	var countryUnits = {};
    	if($('.country-'+i).val()!=''){
	    	countryUnits["country_id"] = parseInt($('.country-'+i).val());
	    	var unitcount=$('.no-of-units-'+i).val();
	    	var units = [];
	    	for(var j=1;j<=unitcount;j++){
	    		var arrayDomainsVal=$('.domain-'+i+'-'+j).val().split(",");
					var arrayDomains= [];
					for(var m=0; m<arrayDomainsVal.length; m++){ arrayDomains[m] = parseInt(arrayDomainsVal[m]); } 
					var domainsVal = arrayDomains;
	    		var unit = {};
		      unit["unit_id"] = '';
		      unit["unit_code"] =  $('.unit-code-'+i+'-'+j).val();
		      unit["unit_name"] = $('.unit-name-'+i+'-'+j).val();
		      unit["unit_address"] = $('.unit-address-'+i+'-'+j).val();
		      unit["postal_code"] = $('.postal-code-'+i+'-'+j).val();
		      unit["geography_id"] = parseInt($('.unitlocation-ids-'+i+'-'+j).val());
		      unit["unit_location"] = $('.unitlocation-'+i+'-'+j).val();
		      unit["industry_id"] = parseInt($('.industry-'+i+'-'+j).val());
		      unit["industry_name"] = $('.industry-'+i+'-'+j+' option:selected').text();
		      unit["domain_ids"] = domainsVal;
		      units.push(unit);
	    	}
	    	countryUnits["units"] = units;	
	    	countryWiseUnits.push(countryUnits)
	    }
    } 

    mirror.saveClient("TechnoAPI", parseInt(groupNameValue), businessGroup, legalEntity, division, countryWiseUnits, success, failure);
	}
	else if(clientunitIdValue!=''){		
		function success(status, data){
			if(status == 'UpdateClientSuccess') {
		    	$("#clientunit-add").hide();
	  			$("#clientunit-view").show();
	  			initialize();
	  		}
	  		 else {
      			$(".error-message").html(status);
      		}	
	    }
		function failure(status, data){
			$(".error-message").html(status);
		}

	 	var businessGroup = {}
	 	if(businessgrouptextValue==''){
	 		businessGroup["business_group_id"] = parseInt(businessgroupValue);
    	if(businessgroupValue!=''){
    		businessGroup["business_group_name"] = businessgroupName;	
    	}
	    else{
	    	businessGroup["business_group_name"] = '';	
	    }	
	 	}
	 	else{
	 		businessGroup["business_group_id"] = '';
     	businessGroup["business_group_name"] = businessgrouptextValue;   
	 	}
	 	var legalEntity = {}
	 	if(lentitytextValue==''){
	 		legalEntity["legal_entity_id"] = parseInt(legalEntityValue);
    	if(legalEntityValue!=''){
    		legalEntity["legal_entity_name"] = legalEntityName;	
    	}
	    else{
	    	legalEntity["legal_entity_name"] = '';	
	    }	
	 	}
	 	else{
	 		legalEntity["legal_entity_id"] = '';
     	legalEntity["legal_entity_name"] = lentitytextValue;   
	 	}
	 	var division = {}
	 	if(divisiontextValue==''){
	 		division["division_id"] = parseInt(divisionValue);
    	if(divisionValue!=''){
    		division["division_name"] = divisionName;	
    	}
	    else{
	    	division["division_name"] = '';	
	    }	
	 	}
	 	else{
	 		division["division_id"] = '';
     	division["division_name"] = divisiontextValue;   
	 	}

    var countryWiseUnits = [];
    var numItemsCountry = $('.country').length;
    for(var i=1; i<numItemsCountry;i++){
    	var countryUnits = {};
    	if($('.country-'+i).val()!=''){
	    	countryUnits["country_id"] = parseInt($('.country-'+i).val());
	    	var unitcount=$('.no-of-units-'+i).val();
	    	var units = [];
	    	for(var j=1;j<=unitcount;j++){
	    		var arrayDomainsVal=$('.domain-'+i+'-'+j).val().split(",");
					var arrayDomains= [];
					for(var m=0; m<arrayDomainsVal.length; m++){ arrayDomains[m] = parseInt(arrayDomainsVal[m]); } 
					var domainsVal = arrayDomains;
	    		var unit = {};
		      unit["unit_id"] = '';
		      unit["unit_code"] =  $('.unit-code-'+i+'-'+j).val();
		      unit["unit_name"] = $('.unit-name-'+i+'-'+j).val();
		      unit["unit_address"] = $('.unit-address-'+i+'-'+j).val();
		      unit["postal_code"] = $('.postal-code-'+i+'-'+j).val();
		      unit["geography_id"] = parseInt($('.unitlocation-ids-'+i+'-'+j).val());
		      unit["unit_location"] = $('.unitlocation-'+i+'-'+j).val();
		      unit["industry_id"] = parseInt($('.industry-'+i+'-'+j).val());
		      unit["industry_name"] = $('.industry-'+i+'-'+j+' option:selected').text();
		      unit["domain_ids"] = domainsVal;
		      units.push(unit);
	    	}
	    	countryUnits["units"] = units;	
	    	countryWiseUnits.push(countryUnits)
	    }
    } 

    mirror.updateClient("TechnoAPI", parseInt(groupNameValue), businessGroup, legalEntity, division, countryWiseUnits, success, failure);
	}
	else{
		console.log("Fails All");
	}
});

//Edit client Unit -----------------------------------------------------------------------------------------------
function clientunit_edit(clientunitId, businessgroupId, legalentityId, divisionId){
	$("#clientunit-add").show();
	$("#clientunit-view").hide();	
  $("#client-unit-id").val(clientunitId);
  var x=document.getElementsByTagName("input");
 	for(i = 0; i<=x.length-1; i++){
  	if(x.item(i).type!="submit" ){ x.item(i).value = ""; }
  }
  $('#group-select:gt(0)').empty();
  $('#businessgroup-select').empty();
  $('#entity-select').empty();
  $('#division-select').empty();
  $('.industry').empty();
  function success(status, data){
		if(status=="GetClientsSuccess"){
			groupList=data['group_companies'];
			businessGroupList=data['business_groups'];
			legalEntitiesList=data['legal_entities'];
			divisionList=data['divisions'];
			countryFulList=data['countries'];
			geographyLevelList=data['geography_levels'];		
			geographyList=data['geographies'];
			industryList=data['industries'];
			domainList=data['domains'];
			unitList=data['units'];
			loadFormListUpdate(clientunitId, businessgroupId, legalentityId, divisionId);
		}
	}
	function failure(status, data){
		console.log(status);
	}
	mirror.getClients("TechnoAPI", success, failure);
}
//Update load form cal------------------------------------------------------------------------------------------
function loadFormListUpdate(clientunitId, businessgroupId, legalEntityId, divisionId){
	loadClientGroups(groupList);
	for(var clients in groupList){
		if(groupList[clients]['client_id']==clientunitId){
			$('#group-select option[value='+clientunitId+']').attr('selected','selected');
			getBusinessGroups(clientunitId);
			$('#businessgroup-select option[value='+businessgroupId+']').attr('selected','selected');
			getLegalEntity(clientunitId);
			$('#entity-select option[value='+legalEntityId+']').attr('selected','selected');
			getDivision(legalEntityId);
			$('#division-select option[value='+divisionId+']').attr('selected','selected');
		}			
	}
	for(units in unitList){
		var countryid=unitList[units]['country_id'];
		if(divisionId==''){
			if(clientunitId==unitList[units]['client_id'] && legalEntityId==unitList[units]['legal_entity_id']){
			}	
		}
		if(divisionId!=''){
			if(clientunitId==unitList[units]['client_id'] && legalEntityId==unitList[units]['legal_entity_id'] && divisionId==unitList[units]['division_id']){
				for(var country in countryFulList){
					if(countryFulList[country]['country_id']==unitList[units]['country_id']){
						$("#add-country-row").trigger('click');
						$('.countryval-'+countc).val(countryFulList[country]['country_name']);
						$('.country-'+countc).val(countryid);
						for(var geography in geographyList[countryid]){
							var glist = geographyList[countryid][geography];
							if(glist['geography_id']==unitList[units]['geography_id']){
								$('.unitlocation-ids-'+countc+'-'+1).val(glist['geography_id']);
								$('.unitlocation-'+countc+'-'+1).val(glist['geography_name']);
								var levelid=glist['level_id'];
								for(var glevel in geographyLevelList){
									var glevelList=geographyLevelList[glevel];
									for(var gllist in glevelList){
										$('.glevel-'+countc+'-'+1).append($('<option value="'+glevelList[gllist]['level_id']+'">'+glevelList[gllist]['level_name']+'</option>'));
										$('.glevel-'+countc+'-'+1+' option[value='+levelid+']').attr('selected','selected');
									}
								}
							}
						}
						$('.unit-code-'+countc+'-'+1).val(unitList[units]['unit_code']);
						$('.unit-name-'+countc+'-'+1).val(unitList[units]['unit_name']);
						for(var industry in industryList){
							$('.industry-'+countc+'-'+1).append($('<option value="'+industryList[industry]['industry_id']+'">'+industryList[industry]['industry_name']+'</option>'));
							if(industryList[industry]['industry_id']==unitList[units]['industry_id']){
								$('.industry-'+countc+'-'+1+' option[value='+unitList[units]['industry_id']+']').attr('selected','selected');
							}
						}
						$('.industry-'+countc).val();
						$('.unit-address-'+countc+'-'+1).val(unitList[units]['unit_address']);
						$('.postal-code-'+countc+'-'+1).val(unitList[units]['postal_code']);

						var domainsVal=unitList[units]['domain_ids'];
						var arrayDomains=domainsVal.split(",");
						console.log(arrayDomains.length);
						$('.domain-'+countc+'-'+1).val(arrayDomains);
						$('.domainselected-'+countc+'-'+1).val(arrayDomains.length+" Selected");
					}
				}
			}
		}
	}
}

//Active or inactive Client Unit List --------------------------------------------------------------------------
function clientunit_active(clientunitId, divisionId, isActive){
  function success(status, data){
 	 	console.log(status);
	  initialize();
  }
  function failure(status, data){
  		console.log("fails----"+status);	
  }
  mirror.changeClientStatus("TechnoAPI",  parseInt(clientunitId), parseInt(divisionId), parseInt(isActive), success, failure);
}

//Search Client name ----------------------------------------------------------------------------------------------
$("#search-clientunit-name").keyup(function() { 
	var count=0;
  var value = this.value.toLowerCase();
  $("table").find("tr:not(:first)").each(function(index) {
      if (index === 0) return;
      var id = $(this).find(".clientunit-name").text().toLowerCase();       
      $(this).toggle(id.indexOf(value) !== -1);;
  });
});
function hidemenu(classname) {
	var lastClass = classname.split(' ').pop();
	var ccount=lastClass.split('-').pop();
	$('.autocompleteview-'+ccount).css("display", "none");
}


function loadauto_text (textval, classval) {
	var lastClass = classval.split(' ').pop();
	var ccount=lastClass.split('-').pop();	
	$('.autocompleteview-'+ccount).css("display", "block");
 	var groupId=$("#group-select").val();
	if(groupId==''){
		$(".error-message").html("Select Group First");
	}
	else{
		var arrayCountry=[];
  	for (var i in groupList){
			if(groupList[i]['client_id']==groupId){
				countryList=groupList[i]['country_ids'];
				arrayCountry=countryList.split(",");
			}
		}
	}

	var countries = countryFulList;
	var suggestions = [];
	$('.ulist-text-'+ccount).empty();
	if(textval.length>0){
		for(var i in countries){
			for(var j=0;j<arrayCountry.length;j++){
				if(arrayCountry[j]==countries[i]['country_id']){
					if (~countries[i]["country_name"].toLowerCase().indexOf(textval.toLowerCase()) && countries[i]["is_active"] == 1) suggestions.push([countries[i]["country_id"],countries[i]["country_name"]]); 	
				}		
			}
		}
		var str='';
		for(var i in suggestions){
		    str += '<li id="'+suggestions[i][0]+'" onclick="activate_text(this,\''+suggestions[i][0]+'\',\''+suggestions[i][1]+'\', '+ccount+')">'+suggestions[i][1]+'</li>';
		}
		$('.ulist-text-'+ccount).append(str);
		$(".country-"+ccount).val('');
	}
}
//set selected autocomplte value to textbox and geographylevel list ---------------------------------------------------
function activate_text (element,checkval,checkname, ccount) {
	$(".countryval-"+ccount).val(checkname);
	$(".country-"+ccount).val(checkval);
	$('.glevel-'+checkval).empty();
}
function hideunitlocation(classname) {
	var lastClass = classname.split(' ').pop();
	$('.'+lastClass).css("display", "none");

}
//autocomplete location -----------------------------------------------------------------------------------------------
function loadlocation(textval, classval){
	var lastClass = classval.split(' ').pop();
	var ccount=lastClass.split('-');
	var countval='-'+ccount[1]+'-'+ccount[2];
	var glevelval=$('.glevel'+countval).val();
	$('.auto-complete-unit-location'+countval).css("display", "block");
	var suggestions = [];
	$('.unitlocationlist-text'+countval).empty();
	
	if(textval.length>0){
		for(var geography in geographyList){
			var geolist=geographyList[geography];
			for(var glist in geolist){
				if(geolist[glist]['level_id']==glevelval){
					if (~geolist[glist]["geography_name"].toLowerCase().indexOf(textval.toLowerCase()) && geolist[glist]["is_active"] == 1) suggestions.push([geolist[glist]["geography_id"],geolist[glist]["geography_name"], geolist[glist]["mapping"]]); 	
				}		
			}
		}
		var str='';
		for(var i in suggestions){
		    str += '<li id="'+suggestions[i][0]+'" onclick="activate_unitlocaion(this,\''+suggestions[i][0]+'\',\''+suggestions[i][1]+'\', \''+countval+'\', \''+suggestions[i][2]+'\')">'+suggestions[i][1]+'</li>';
		}
		$('.unitlocationlist-text'+countval).append(str);		
		$('.unitlocation-ids'+countval).val('');
	}
}
function activate_unitlocaion (element,checkval,checkname, ccount, mappingname) {
	console.log('.unit-location-ids'+ccount);
	$('.unitlocation'+ccount).val(checkname);
	$('.unitlocation-ids'+ccount).val(checkval);
	$('.full-location-list'+ccount).html(mappingname);
}
function hidedomain(classval){
	var lastClass = classval.split(' ').pop();
	var ccount=lastClass.split('-');
	var countval='-'+ccount[3]+'-'+ccount[4];
	$('.domain-selectbox-view'+countval).css("display", "none");	
}
//Load Domain  for Unit------------------------------------------------------------------------------------------------
function loaddomain(classval){
	var lastClass = classval.split(' ').pop();
	var ccount=lastClass.split('-');
	var countval='-'+ccount[1]+'-'+ccount[2];
	$('.domain-selectbox-view'+countval).css("display", "block");	
	var editdomainval=[];
	if($('.domain'+countval).val() != ''){
		editdomainval = $('.domain'+countval).val().split(",");
	}
	var domains=domainList;
	$('.ul-domain-list'+countval).empty();
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
			str += '<li id="'+domainId+'" class="active_selectbox'+countval+' active" onclick="activate(this,\''+countval+'\' )" >'+domainName+'</li> ';
		}else{
			str += '<li id="'+domainId+'" onclick="activate(this,\''+countval+'\')" >'+domainName+'</li> ';
		}
	}
	$('.ul-domain-list'+countval).append(str);
  $('.domainselected'+countval).val(editdomainval.length+" Selected")
}

//check & uncheck process
function activate(element, count){
	var chkstatus = $(element).attr('class');
	if(chkstatus == 'active_selectbox'){
		$(element).removeClass("active_selectbox"+count);
		$(element).removeClass("active");
		
	}else{
		$(element).addClass("active_selectbox"+count);
		$(element).addClass("active");
	}  
	var selids='';
	var selNames='';
	var totalcount =  $(".active_selectbox"+count).length;
	$(".active_selectbox"+count).each( function( index, el ) {
		if (index === totalcount - 1) {
			selids = selids+el.id;
			selNames = selNames+$(this).text();
		}else{
			selids = selids+el.id+",";
			selNames = selNames+$(this).text()+",";			
		}    
	});
	$(".domainselected"+count).val(totalcount+" Selected");
	$(".domain"+count).val(selids);
}
$("#division-new").click(function(){
	if($(this).text()=="New"){
		$("#division-text").show();
  	$("#division-select").hide();
 		$("#division-new").hide();	
 		$("#division-existing").show();	
	}
});
$("#division-existing").click(function(){
	if($(this).text()=="Cancel"){
		$("#division-text").hide();
  	$("#division-select").show();
 		$("#division-new").show();
 		$("#division-existing").hide();		
	}
});
$("#entity-new").click(function(){
	if($(this).text()=="New"){
	  $("#entity-text").show();
	  $("#entity-select").hide();
	  $("#entity-new").hide();
	  $("#entity-existing").show();
	  $("#division-text").show();
	  $("#division-select").hide();
 		$("#division-new").hide();
 		$("#division-existing").hide();	
	}
});
$("#entity-existing").click(function(){
	if($(this).text()=="Cancel"){
	  $("#entity-text").hide();
	  $("#entity-select").show();
	  $("#entity-new").show();
	  $("#entity-existing").hide();
	  $("#division-text").hide();
	  $("#division-select").show();
 		$("#division-new").show();
 		$("#division-existing").hide();	
	}
});
$("#businessgroup-new").click(function(){
	if($(this).text()=="New"){
		$("#businessgroup-text").show();
  	$("#businessgroup-select").hide();
	  $("#businessgroup-new").hide();
	  $("#businessgroup-existing").show();
	  $("#entity-text").show();
	  $("#entity-select").hide();
	  $("#entity-new").hide();
	  $("#entity-existing").hide();
	  $("#division-text").show();
	  $("#division-select").hide();
 		$("#division-new").hide();
 		$("#division-existing").hide();	
	}
});
$("#businessgroup-existing").click(function(){
	if($(this).text()=="Cancel"){
	  $("#businessgroup-text").hide();
	  $("#businessgroup-select").show();
	  $("#businessgroup-new").show();
	  $("#businessgroup-existing").hide();
	  $("#entity-text").hide();
	  $("#entity-select").show();
	  $("#entity-new").show();
	  $("#entity-existing").hide();
	  $("#division-text").hide();
	  $("#division-select").show();
 		$("#division-new").show();
 		$("#division-existing").hide();	
	}
});