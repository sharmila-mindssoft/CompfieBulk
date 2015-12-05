var groupList;
var countryList;
var domainList;
var businessGroupList;
var legalEntitiesList;
var divisionList;
var countryFulList;
var countc=0;
var industryList;
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
		loadClientsList(data);
	}
	function failure(status, data){
		$(".error-message").html(status);
	}
	mirror.getClients("TechnoAPI", success, failure);
}
//Load Get Client List -----------------------------------------------------------------------------------------
function loadClientsList(clientunitsList){
 	$(".tbody-clientunit-list").find("tr").remove();
  	var sno=0;
	var imageName, title;	
	//console.log(groupList);
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
								$('.edit', clone).html('<img src="/images/icon-edit.png" id="editid" onclick="clientunit_edit('+divisionid+')"/>');
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
 	$(".error-message").html('');
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
$("#group-select").change(function() {
	$('#businessgroup-select').find('option:gt(0)').remove();
	var groupId=$(this).val();
	for (var i in businessGroupList){
		if(businessGroupList[i]['client_id']==groupId){
			var bgroupId=businessGroupList[i]['business_group_id'];
			var bgroupName=businessGroupList[i]['business_group_name'];
			$('#businessgroup-select').append($('<option value="'+bgroupId+'">'+bgroupName+'</option>'));
		}
	}
});
//Load LegalEntities ---------------------------------------------------------------------------------------------
$("#businessgroup-select").change(function() {
	$('#entity-select').find('option:gt(0)').remove();
	var busgroupId=$(this).val();
	for (var i in legalEntitiesList){
		if(legalEntitiesList[i]['business_group_id']==busgroupId){
			var lentityId=legalEntitiesList[i]['legal_entity_id'];
			var lentityName=legalEntitiesList[i]['legal_entity_name'];
			$('#entity-select').append($('<option value="'+lentityId+'">'+lentityName+'</option>'));
		}
	}
});

//Load Divisions ---------------------------------------------------------------------------------------------
$("#entity-select").change(function() {
	$('#division-select').find('option:gt(0)').remove();
	var lentityId=$(this).val();
	for (var i in divisionList){
		if(divisionList[i]['legal_entity_id']==lentityId){
			var divisionId=divisionList[i]['division_id'];
			var divisionName=divisionList[i]['division_name'];
			$('#division-select').append($('<option value="'+divisionId+'">'+divisionName+'</option>'));
		}
	}
});
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
			$('#countryval', clone).addClass('countryval-'+countryArray[countc]);
			$('#country', clone).addClass('country-'+countryArray[countc]);
			$('#autocompleteview', clone).addClass('autocompleteview-'+countryArray[countc]);
			$('#ulist-text', clone).addClass('ulist-text-'+countryArray[countc]);			
			$('.geography-levels', clone).addClass('glevel-'+countryArray[countc]+'-'+1);
			$('.unit-location', clone).addClass('unitlocation-'+countryArray[countc]+'-'+1);
			$('.unit-location-ids', clone).addClass('unitlocation-ids-'+countryArray[countc]+'-'+1);
			$('.auto-complete-unit-location', clone).addClass('auto-complete-unit-location-'+countryArray[countc]+'-'+1);
			$('.unitlocationlist-text', clone).addClass('unitlocationlist-text-'+countryArray[countc]+'-'+1);
			$('.full-location-list', clone).addClass('full-location-list-'+countryArray[countc]+'-'+1);
			$('.unitcode_checkbox', clone).addClass('unitcode_checkbox-'+countryArray[countc]);
			$('.unit-code', clone).addClass('unit-code-'+countryArray[countc]+'-'+1);
			$('.unit-name', clone).addClass('unit-name-'+countryArray[countc]+'-'+1);
			$('.industry', clone).addClass('industry-'+countryArray[countc]+'-'+1);
			$('.unit-address', clone).addClass('unit-address-'+countryArray[countc]+'-'+1);
			$('.postal-code', clone).addClass('postal-code-'+countryArray[countc]+'-'+1);
			$('.domain-list', clone).addClass('domain-list-'+countryArray[countc]+'-'+1);
			$('.domain-selected', clone).addClass('domain-selected-'+countryArray[countc]+'-'+1);
			$('.domain', clone).addClass('domain-'+countryArray[countc]+'-'+1);
			$('.domain-selectbox-view', clone).addClass('domain-selectbox-view-'+countryArray[countc]+'-'+1);
			$('.ul-domain-list', clone).addClass('ul-domain-list-'+countryArray[countc]+'-'+1);		
			$('.add-unit-row img', clone).addClass('table-addunit-'+countryArray[countc]);
			$('.tbody-unit-list', clone).addClass('tbody-unit-'+countryArray[countc]);
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
	var lastclassname=$('.'+tbodyclasses[1]).find('tr:last-child .geography-levels').attr('class');
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
	$('.unitcode_checkbox', clone1).addClass('unitcode_checkbox-'+countval);
	$('.unit-code', clone1).addClass('unit-code-'+countval+'-'+(lastClassval+1));
	$('.unit-name', clone1).addClass('unit-name-'+countval+'-'+(lastClassval+1));
	$('.industry', clone1).addClass('industry-'+countval+'-'+(lastClassval+1));
	$('.unit-address', clone1).addClass('unit-address-'+countval+'-'+(lastClassval+1));
	$('.postal-code', clone1).addClass('postal-code-'+countval+'-'+(lastClassval+1));
	$('.domain-list', clone1).addClass('domain-list-'+countval+'-'+(lastClassval+1));
	$('.domain-selected', clone1).addClass('domain-selected-'+countval+'-'+(lastClassval+1));
	$('.domain', clone1).addClass('domain-'+countval+'-'+(lastClassval+1));
	$('.domain-selectbox-view', clone1).addClass('domain-selectbox-view-'+countval+'-'+(lastClassval+1));
	$('.ul-domain-list', clone1).addClass('ul-domain-list-'+countval+'-'+(lastClassval+1));
	$('.'+tbodyclasses[1]).append(clone1);
}
	
//Load Geography Levels -------------------------------------------------------------------------------------------
function loadglevels(classval){
	var lastClass = classval.split(' ').pop();
	var checkval=lastClass.split('-');	
	var countryvalue=$('.countryval-'+checkval[1]).val();
	if(countryvalue==''){
		$('.error-message').html('Enter Country First');
	}
	else{
		$('.'+lastClass).empty();
		for(var glevel in geographyLevelList[checkval[1]]){
			var glevellist = geographyLevelList[checkval[1]][glevel];
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
	var clientunitIdValue = $("#clientunit-id").val();
	var clientunitNameValue = $("#clientunit-name").val();
	if(clientunitNameValue=='' || clientunitNameValue==null){
		$(".error-message").html('clientunit Name Required');
	}
	else if(clientunitIdValue==''){		
		function success(status, data){
			if(status == 'success') {
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
		mirror.saveclientunit("Saveclientunit", clientunitNameValue, success, failure);
	}
	else{		
		function success(status, data){
			if(status == 'success') {
				$("#clientunit-add").hide();
	  			$("#clientunit-view").show();
	  			initialize();
  			}
  			if(status == 'clientunitNameAlreadyExists') {
  				$(".error-message").html(status);
  			}	
		}
		function failure(status, data){
		}
		mirror.updateclientunit("updateclientunit", parseInt(clientunitIdValue), clientunitNameValue, success, failure);
	}
});

//Edit client Unit -----------------------------------------------------------------------------------------------
function clientunit_edit(clientunitId, clientunitName){
	$("#clientunit-add").show();
	$("#clientunit-view").hide();
	$("#clientunit-name").val(clientunitName);
  $("#clientunit-id").val(clientunitId);
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
	document.getElementsByClassName('autocompleteview-'+ccount)[0].style.display = 'none';
}
function loadauto_text (textval, classval) {
	var lastClass = classval.split(' ').pop();
	var ccount=lastClass.split('-').pop();	
 	document.getElementsByClassName('autocompleteview-'+ccount)[0].style.display = 'block';
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
					if (~geolist[glist]["geography_name"].toLowerCase().indexOf(textval.toLowerCase()) && geolist[glist]["is_active"] == 1) suggestions.push([geolist[glist]["geography_id"],geolist[glist]["geography_name"]]); 	
				}		
			}
		}
		var str='';
		for(var i in suggestions){
		    str += '<li id="'+suggestions[i][0]+'" onclick="activate_unitlocaion(this,\''+suggestions[i][0]+'\',\''+suggestions[i][1]+'\', \''+countval+'\')">'+suggestions[i][1]+'</li>';
		}
		$('.unitlocationlist-text'+countval).append(str);
		$('.unit-location-ids'+countval).val('');
	}
}
function activate_unitlocaion (element,checkval,checkname, ccount) {
	$(".unit-location"+ccount).val(checkname);
	$(".unit-location-ids"+ccount).val(checkval);
}