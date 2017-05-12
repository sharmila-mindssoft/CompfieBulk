var groupList;
var countryList;
var groupadminList;

//Pagination variable declaration
var ItemsPerPage = $('#items_per_page');
var PaginationView = $('.pagination-view');
var Pagination = $('#pagination-rpt');
var CompliacneCount = $('.compliance_count');
var on_current_page = 1;
var sno = 0;
var totalRecord;
var ReportData;
var csv = false;

function displayLoader() {
  $('.loading-indicator-spin').show();
}
function hideLoader() {
  $('.loading-indicator-spin').hide();
}

function processGroupAdminReportData()
{
	function onSuccess(data) {
		groupList = data.groupadmin_clients;
		countryList = data.group_admin_countries;
		groupadminList = data.group_admin_list;
		//sfillGroupAdmingroupData();
	}
	function onFailure(error) {
		displayMessage(error);
	}
	mirror.getGroupAdminReportData(function (error, response) {
		if (error == null) {
	  		onSuccess(response);
		} else {
  			onFailure(error);
		}
	});
}

$('#btn-show').click(function () {
	totalrecords = 0;
	csv = false;
	on_current_page = 1;
    sno = 0;

	var client_id = $('#group-id').val();

	totalRecord = groupadminList.length;

	if(client_id > 0 && totalRecord > 0)
	{
		$('.details').show();
		$('#compliance_animation')
			.removeClass().addClass('bounceInLeft animated')
			.one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend', function(){
			$(this).removeClass();
		});

    	processPaging();
		//loadGroupAdminReportData();
	}
	else
	{
		displayMessage(message.group_required);
		$('.grid-table-rpt').hide();
		$('.tbody-client-admin-regn-list').find('tr').remove();
	}
});

$('#btn-export').click(function () {
	csv = true;
	var client_id = $('#group-id').val();
	var country_id = $('#country-id').val();
	if (country_id == "")
		country_id = 0;

	if(parseInt(client_id) > 0){
		mirror.exportGroupAdminReportData(parseInt(client_id), parseInt(country_id), csv, function (error, response) {
			if (error == null) {
				if(csv){
	                document_url = response.link;
	                $(location).attr('href', document_url);
	            }
			} else {
	  			if (error == "ExportToCSVEmpty") {
			        displayMessage(message.empty_export);
			    }else {
					displayMessage(error);
				}
			}
		});
	}else{
		displayMessage(message.group_required);
		groupsval.focus();
	}

});

function loadGroupAdminReportData(data)
{
	$('.grid-table-rpt').show();
	$('.tbody-client-admin-regn-list').find('tr').remove();
	var j=1;
	var client_id = $('#group-id').val();
	var client_name = $('#groupsval').val();
	var country_id = $('#country-id').val();
	var country_name = null;
	if(country_id != '')
	{
		country_name = $('#countryval').val();
	}
	else
	{
		country_name = "--";
	}

	$('.countrynameval').text(country_name);
	$('.groupsval').text(client_name);

	var tableheading = $('#templates .tr-heading');
	var cloneheading = tableheading.clone();
	$('.tbody-client-admin-regn-list').append(cloneheading);
	for (var i=0;i<data.length;i++)
	{
		is_null = false;
		sno = sno + 1;
		$('.countrynameval').text(data[i].registration_email_date);
		$('.resenddate').text(data[i].resend_email_date);
		var tablerow = $('#templates .table-row');
		var clonedata = tablerow.clone();
		$('.sno', clonedata).text(sno);
		$('.country-name', clonedata).text(data[i].country_name);
		$('.le-name', clonedata).text(data[i].legal_entity_name);
		$('.no-of-units', clonedata).text(data[i].unit_count);
		if(data[i].unit_email_date != "" || data[i].unit_email_date != null)
			$('.unit-email', clonedata).text(data[i].unit_email_date);
		else
			$('.unit-email', clonedata).text(" -- ");

		if(data[i].statutory_email_date != "" || data[i].statutory_email_date != null)
			$('.statu-email', clonedata).text(data[i].statutory_email_date);
		else
			$('.statu-email', clonedata).text(" -- ");
		$('.tbody-client-admin-regn-list').append(clonedata);
	}
}

//pagination - functions
function showPagePan(showFrom, showTo, total) {
    var showText = 'Showing ' + showFrom + ' to ' + showTo +  ' of ' + total + ' entries ';
    CompliacneCount.text(showText);
    PaginationView.show();
};

function hidePagePan() {
    CompliacneCount.text('');
    PaginationView.hide();
}

function createPageView(total_records) {
    perPage = parseInt(ItemsPerPage.val());
    Pagination.empty();
    Pagination.removeData('twbs-pagination');
    Pagination.unbind('page');

    Pagination.twbsPagination({
        totalPages: Math.ceil(total_records/perPage),
        visiblePages: visiblePageCount,
        onPageClick: function(event, page) {
            cPage = parseInt(page);
            if (parseInt(on_current_page) != cPage) {
                on_current_page = cPage;
                processPaging();
            }
        }
    });
};

function processPaging(){
  _page_limit = parseInt(ItemsPerPage.val());
  if (on_current_page == 1) {
    sno = 0;
  }
  else {
    sno = (on_current_page - 1) *  _page_limit;
  }
  sno  = sno;
  ReportData = pageData(on_current_page);
  if (totalRecord == 0) {
    $('.tbody-client-admin-regn-list').find('tr').remove();
    var tableRow4 = $('#no-record-templates .table-no-content .table-row-no-content');
    var clone4 = tableRow4.clone();
    $('.no_records', clone4).text('No Records Found');
    $('.tbody-client-admin-regn-list').append(clone4);
    PaginationView.hide();
    hideLoader();
  } else {
    if(sno==0){
      createPageView(totalRecord);
    }
    PaginationView.show();
    //ReportView.show();
    loadGroupAdminReportData(ReportData);
  }
}

function pageData(on_current_page){
  data = [];
  _page_limit = parseInt(ItemsPerPage.val());
  recordLength = (parseInt(on_current_page) * _page_limit);
  var showFrom = sno + 1;
  var is_null = true;
  var country_id = $('#country-id').val();
  for(i=sno;i<groupadminList.length;i++)
  {
  	is_null = false;
  	var ctry_check = true;
	if(country_id>0 && (country_id != groupadminList[i].country_id)){
		ctry_check =false;
	}
    if($('#group-id').val() == groupadminList[i].client_id && ctry_check == true){
    	data.push(groupadminList[i]);
    	if(i == (recordLength-1))
	    {
	      break;
	    }
    }

  }
  totalRecord = data.length;
  if (is_null == true) {
    hidePagePan();
  }
  else {
    if(recordLength < totalRecord)
      showPagePan(showFrom, recordLength, totalRecord);
    else
      showPagePan(showFrom, totalRecord, totalRecord);
  }
  return data;
}

//callback for autocomplete success
function onAutoCompleteSuccess(value_element, id_element, val) {
    value_element.val(val[1]);
    id_element.val(val[0]);
    value_element.focus();
}

//load group form list in autocomplete text box
$('#groupsval').keyup(function (e) {
  var textval = $(this).val();
  commonAutoComplete(
      e, $('#ac-group'), $('#group-id'), textval,
      groupList, "group_name", "client_id", function (val) {
          onAutoCompleteSuccess($('#groupsval'), $('#group-id'), val);
	});
});

//retrive country autocomplete value
function onCountrySuccess(val) {
  $('#countryval').val(val[1]);
  $('#country-id').val(val[0]);
  resetFilter();
}

//load country list in autocomplete textbox
$('#countryval').keyup(function (e) {
  var textval = $(this).val();
  var ctry_grp = [];
  var client_id = $('#group-id').val();

  if(client_id > 0)
  {
  	var condition_fields = ["is_active"];
    var condition_values = [true];
  	for(var i=0;i<countryList.length;i++)
	{
		if(client_id == countryList[i].client_id)
		{
			var occur = -1;
			for(var j=0;j<ctry_grp.length;j++){
				if(ctry_grp[j].country_id == countryList[i].country_id){
					occur = 1;
					break;
				}
			}
			if(occur < 0){
				ctry_grp.push({
					"country_id": countryList[i].country_id,
					"country_name": countryList[i].country_name,
					"is_active": countryList[i].is_active
				})
			}
		}
	}
	commonAutoComplete(
      e, $('#ac-country'), $('#country-id'), textval,
      ctry_grp, "country_name", "country_id", function (val) {
          onAutoCompleteSuccess($('#countryval'), $('#country-id'), val);
	}, condition_fields, condition_values);
  }
  else
  {
  	displayMessage(message.group_required);
  }
});

function resetAllFilter()
{
	$('#groupsval').val('');
	$('#group-id').val('');
	$('#countryval').val('');
	$('#country-id').val('');
	totalrecords = 0;
	$('#groupsval').focus();
}

function resetFilter()
{
	$('#groupsval').val('');
	$('#group-id').val('');
}

function initialize_form()
{
	$('.grid-table-rpt').hide();
	$('.tbody-client-admin-regn-list').find('tr').remove();
	resetAllFilter();
	ItemsPerPage.on('change', function (e) {
	    perPage = parseInt($(this).val());
	      sno = 0;
	      on_current_page = 1;
	      createPageView(totalRecord);
	      processPaging();
	});
	processGroupAdminReportData();
}

// page load
function initialize() {
	clearMessage();
	resetAllFilter();
  	initialize_form();
}

$(document).ready(function () {
  initialize();
  loadItemsPerPage();
});
