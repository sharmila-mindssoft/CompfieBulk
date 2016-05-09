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

var sno = 0;
var totalRecord;
var lastBG = '';
var lastLE = '';
var lastDV = '';

function displayLoader() {
    $(".loading-indicator-spin").show();
}
function hideLoader() {
    $(".loading-indicator-spin").hide();
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
	sno = 0;
	lastBG = '';
	lastLE = '';
	lastDv = '';
	$('.tbody-unitdetails-list tr').remove();
    loadunitdetailsreport("show");
});
$("#export-button").click(function(){ 
	sno = 0;
	lastBG = '';
	lastLE = '';
	lastDv = '';
	$('.tbody-unitdetails-list tr').remove();
    loadunitdetailsreport("export");
});

//pagination process
$('#pagination').click(function(){
  loadunitdetailsreport("show");
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
		displayLoader();
		function onSuccess(data){
	        clearMessage();
			$(".grid-table-rpt").show();         
		    if(buttontype == "export"){
		        var download_url = data["link"];
		        window.open(download_url, '_blank');    
		    }
		    else{
		    	totalRecord = data["total_count"];
		        loadUnitDetailsList(data['units']);  
		    }
		    hideLoader();
		}
		function onFailure(error){
			console.log(error);
			hideLoader();
		}
	    csv = false
	    if(buttontype == "export"){
	        csv = true
	    }
		client_mirror.getClientDetailsReportData(parseInt(countries), businessgroupid,	
			lentityid, divisionid, unitid,  domainsVal, csv, sno, 
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

function loadUnitDetailsList(data){
    $.each(data, function(key, value) {
    	var bg = '-';
		if(data["business_group_name"] != null) bg = data["business_group_name"];
		var dv = '-';
		if( data["division_name"] != null) dv = data["division_name"];
		var le = data["legal_entity_name"];

    	if(lastBG != bg || lastLE != le || lastDv != dv){
    		var tableRowHeading = $('#templates .table-unitdetails-list .filter-heading-list');
	        var cloneHeading = tableRowHeading.clone();
	        $('.filter-country-name', cloneHeading).text(countriesText);
	        $('.filter-business-group-name', cloneHeading).text(bg);
	        $('.filter-legal-entity-name', cloneHeading).text(le);
	        $('.filter-division-name', cloneHeading).text(dv);
	        $('.unitdetails-list .tbody-unitdetails-list').append(cloneHeading);

	        var tableRowHeadingth = $('#templates .table-unitdetails-list .heading-list');
	        var cloneHeadingth = tableRowHeadingth.clone();
	        $('.unitdetails-list .tbody-unitdetails-list').append(cloneHeadingth);
	        lastBG = bg;
		    lastDv = dv;
		    lastLE = le;
    	}    
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
	
	if(totalRecord == 0){	
	    var tableRow4=$('#no-record-templates .table-no-content .table-row-no-content');
	    var clone4=tableRow4.clone();
	    $('.no_records', clone4).text('No Compliance Found');
	    $('.tbody-unitdetails-list').append(clone4);
	    $('#pagination').hide();
	    $('.compliance_count').text('');
	}else{
	    $('.compliance_count').text("Showing " + 1 + " to " + sno + " of " + totalRecord);
	    if(sno >= totalRecord){
	      $('#pagination').hide();
	    }else{
	      $('#pagination').show();
	    }
	}
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

//domain selet box
function hidemenudomains() {
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