var assignedStatutoriesList;
var complianceStatutoriesList;
var searchedStatutoryList = []


//filter controls initialized
var FilterBox = $('.filter-text-box');
var FilterCountry = $('#search-country-name');
var FilterGroup = $('#search-group-name');
var FilterBG = $('#search-bg-name');
var FilterLE = $('#search-le-name');
var FilterDivision = $('#search-division-name');
var FilterCategory = $('#search-category-name');
var FilterUnit = $('#search-unit-name');
var FilterDomain = $('#search-domain-name');

function initialize() {
	function onSuccess(data) {
		console.log("data:"+data)
		assignedStatutoriesList = data.approve_assigned_statutories;
		loadAssignedStatutoriesList();
	}
	function onFailure(error) {
		displayMessage(status);
	}
	mirror.getAssignedStatutoriesList(function (error, response) {
		if (error == null) {
	  		onSuccess(response);
		} else {
  			onFailure(error);
		}
	});
}

function loadAssignedStatutoriesList()
{
	var sno = 0;
	$('.tbody-approved-assigned-statutories-list').find('tr').remove();
	for (var i in assignedStatutoriesList) {
		var list = assignedStatutoriesList[i];
	    var tableRow = $('#templates .table-approved-assigned-statutories .table-row');
	    var clone = tableRow.clone();

	    sno = sno + 1;
    	$('.sno', clone).text(sno);
    	$('.country-name', clone).text(list.country_name);
    	$('.group-name', clone).text(list.group_name);
    	$('.bg-name', clone).text(list.business_group_name);
    	$('.le-name', clone).text(list.legal_entity_name);
    	$('.division-name', clone).text(list.division_name);
    	$('.category-name', clone).text(list.category_name);
    	$('.unit-name', clone).text(list.unit_name);
    	$('.domain-name', clone).text(list.domain_name);
    	$('#btn-view', clone);
    	$('#btn-view', clone).on('click', function() {
            displayComplianceStatutoryList(v.unit_id, v.domain_id);
        });
    	$('.tbody-approved-assigned-statutories-list').append(clone);
	}
	if (assignedStatutoriesList.length == 0) {
	    $('.tbody-approved-assigned-statutories-list').empty();
	    var tableRow4 = $('#no-record-templates .table-no-content .table-row-no-content');
	    var clone4 = tableRow4.clone();
	    $('.no_records', clone4).text('No Records Found');
	    $('.tbody-approved-assigned-statutories-list').append(clone4);
	}
}

function displayComplianceStatutoryList(unitId, domainId){
	function onSuccess(data) {
		console.log("data:"+data)
		complianceStatutoriesList = data.compliance_statutories;

	}
	function onFailure(error) {
		displayMessage(status);
	}
	if(statutoryId != '')
	{
		mirror.getComplianceStatutoriesList(parseInt(unitId), parseInt(domainId), function (error, response) {
			if (error == null) {
					onSuccess(response);
			} else {
					onFailure(error);
			}
		});
	}
	else
	{
		displayMessage("Invalid Request");
	}

}

function processSearch()
{

}

function renderControls(){
	initialize();
	FilterBox.keyup(function() {
		searchList = [];
		processSearch();
	});

}


$(function () {
	renderControls();
});
