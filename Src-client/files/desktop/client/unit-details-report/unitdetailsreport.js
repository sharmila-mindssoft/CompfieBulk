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
var csv;

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
		displayMessage(message.country_required);
	}
	else{
		function onSuccess(data){
      clearMessage();
			$(".grid-table-rpt").show();         
      if(buttontype == "export"){
        var download_url = data["link"];
        window.open(download_url, '_blank');    
      }
      else{
        loadUnitDetailsList(data['units']);   
      }
		}
		function onFailure(error){
			console.log(error);
		}
    csv = false
    if(buttontype == "export"){
        csv = true
    }
		client_mirror.getClientDetailsReportData(parseInt(countries), businessgroupid,	
			lentityid, divisionid, unitid,  domainsVal, csv, 0, 
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


//retrive country autocomplete value
function onCountrySuccess(val){
  $("#countryval").val(val[1]);
  $("#country").val(val[0]);
}

//load country list in autocomplete text box  
$("#countryval").keyup(function(){
  var textval = $(this).val();
  getCountryAutocomplete(textval, countriesList, function(val){
    onCountrySuccess(val)
  })
});

//retrive domain autocomplete value
function onDomainSuccess(val){
  $("#domainval").val(val[1]);
  $("#domain").val(val[0]);
}
//load domain list in autocomplete textbox  
$("#domainval").keyup(function(){
  var textval = $(this).val();
  getDomainAutocomplete(textval, domainsList, function(val){
    onDomainSuccess(val)
  })
});

//retrive businessgroup form autocomplete value
function onBusinessGroupSuccess(val){
  $("#businessgroupsval").val(val[1]);
  $("#businessgroupid").val(val[0]);
}

//load businessgroup form list in autocomplete text box  
$("#businessgroupsval").keyup(function(){
  var textval = $(this).val();
  getClientBusinessGroupAutocomplete(textval, businessgroupsList, function(val){
    onBusinessGroupSuccess(val)
  })
});

//retrive legelentity form autocomplete value
function onLegalEntitySuccess(val){
  $("#legalentityval").val(val[1]);
  $("#legalentityid").val(val[0]);
}

//load legalentity form list in autocomplete text box  
$("#legalentityval").keyup(function(){
  var textval = $(this).val();
  getClientLegalEntityAutocomplete(textval, legalEntityList, function(val){
    onLegalEntitySuccess(val)
  })
});

//retrive division form autocomplete value
function onDivisionSuccess(val){
  $("#divisionval").val(val[1]);
  $("#divisionid").val(val[0]);
}

//load division form list in autocomplete text box  
$("#divisionval").keyup(function(){
  var textval = $(this).val();
  getClientDivisionAutocomplete(textval, divisionsList, function(val){
    onDivisionSuccess(val)
  })
});

//retrive unit form autocomplete value
function onUnitSuccess(val){
  $("#unitval").val(val[1]);
  $("#unitid").val(val[0]);
}

//load unit  form list in autocomplete text box  
$("#unitval").keyup(function(){
  var textval = $(this).val();
  getUnitAutocomplete(textval, unitList, function(val){
    onUnitSuccess(val)
  })
});


$(function() {
	$(".grid-table-rpt").hide();
	initialize();
});