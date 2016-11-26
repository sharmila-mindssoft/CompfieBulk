var statutorynatureList;

//filter controls initialized
var FilterBox = $('.filter-text-box');
var FilterCountry = $('#search-country-name');
var FilterStatutorynature = $('#search-statutory-nature-name');

//search status controls
var Search_status = $('#search-status');
var Search_status_ul = $('.search-status-list');
var Search_status_li = $('.search-status-li');

//table controls
var viewTable = $('.tbody-statutory-nature-list');

//Pagination variable declaration
var ItemsPerPage = $('#items_per_page');
var PaginationView = $('.pagination-view');
var Pagination = $('#pagination-rpt');
var CompliacneCount = $('.compliance_count');
var on_current_page = 1;
var sno = 0;
var totalRecord;
var ReportData;

// get statutory nature list from api
function getStatutorynature() {
	function onSuccess(data) {
		statutorynatureList = data.statutory_natures;
		totalRecord = statutorynatureList.length;
    processPaging();
	}
	function onFailure(error) {
		custom_alert(error);
	}
	mirror.getStatutoryNatureList(function (error, response) {
		if (error == null) {
		  onSuccess(response);
		} else {
		  onFailure(error);
		}
	});
}

function processSearch()
{
  c_name = FilterCountry.val().toLowerCase();
  s_n_name = FilterStatutorynature.val().toLowerCase();

  nature_status = $('.search-status-li.active').attr('value');

  searchList = []

  for(var i in statutorynatureList){
    data = statutorynatureList[i];

    data_c_name = data.country_name.toLowerCase();
    data_s_n_name = data.statutory_nature_name.toLowerCase();
    data_is_active = data.is_active;

    if ((~data_c_name.indexOf(c_name)) && (~data_s_n_name.indexOf(s_n_name)))
    {
      if ((nature_status == 'all' || Boolean(parseInt(nature_status)) == data.is_active)){
        searchList.push(data);
      }
    }
  }
  loadStatNatureData(searchList);
}

//display statutory nature list in view page
function loadStatNatureData(data) {
  var j = 1;
  viewTable.find('tr').remove();

  $.each(data, function (key, value) {
    var country_id = value.country_id;
    var country_name = value.country_name;
    var statutory_nature_id = value.statutory_nature_id;
    var statutory_nature_name = value.statutory_nature_name;
    var isActive = value.is_active;
    var passStatus = null;

    if (isActive == true) {
      passStatus = false;
    } else {
      passStatus = true;
    }

    var tableRow = $('#templates .table-statutory-nature-report .table-row');
    var clone = tableRow.clone();
    $('.sno', clone).text(j);
    $('.country-name', clone).text(country_name);
    $('.statutory-nature-name', clone).text(statutory_nature_name);

    if (isActive == true){
      $('.status', clone).removeClass('fa-times text-danger');
      $('.status', clone).addClass('fa-check text-success');
    }
    else{
      $('.status', clone).removeClass('fa-check text-success');
      $('.status', clone).addClass('fa-times text-danger');
    }

    $('.status').hover(function(){
      showTitle(this);
    });
    viewTable.append(clone);
    j = j + 1;
  });
}

//Status Title
function showTitle(e){
  if(e.className == "fa c-pointer status fa-times text-danger"){
    e.title = 'Active';
  }
  else if(e.className == "fa c-pointer status fa-check text-success")
  {
    e.title = 'Inactive';
  }
}

//render controls
function renderControls(){
	getStatutorynature();

  ItemsPerPage.on('change', function (e) {
    perPage = parseInt($(this).val());
      sno = 0;
      on_current_page = 1;
      createPageView(totalRecord);
      processPaging();
  });


	//status of the list
	Search_status_ul.click(function (event) {
		Search_status_li.each(function (index, el) {
		  $(el).removeClass('active');
		});
		$(event.target).parent().addClass('active');

		var currentClass = $(event.target).find('i').attr('class');
		Search_status.removeClass();
		if(currentClass != undefined){
		  Search_status.addClass(currentClass);
		  Search_status.text('');
		}else{
		  Search_status.addClass('fa');
		  Search_status.text('All');
		}
		processSearch();
	});

	FilterBox.keyup(function() {
	    processSearch();
	});

	Search_status.change(function() {
	    processSearch();
	});
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
    sno = 0
  }
  else {
    sno = (on_current_page - 1) *  _page_limit;
  }
  sno  = sno;
  totalRecord = statutorynatureList.length;
  ReportData = pageData(on_current_page);
  if (totalRecord == 0) {
    $('.table-statutory-nature-list').empty();
    var tableRow4 = $('#no-record-templates .table-no-content .table-row-no-content');
    var clone4 = tableRow4.clone();
    $('.no_records', clone4).text('No Records Found');
    $('.table-statutory-nature-list').append(clone4);
    PaginationView.hide();
    hideLoader();
  } else {
    if(sno==0){
      createPageView(totalRecord);
    }
    PaginationView.show();
    loadStatNatureData(ReportData);
  }
}

function pageData(on_current_page){
  data = [];
  _page_limit = parseInt(ItemsPerPage.val());
  recordLength = (parseInt(on_current_page) * _page_limit);
  var showFrom = sno + 1;
  var is_null = true;
  for(i=sno;i<statutorynatureList.length;i++)
  {
    is_null = false;
    data.push(statutorynatureList[i]);
    if(i == (recordLength-1))
    {
      break;
    }
  }
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

//loading controls
function initialize()
{
	renderControls();
}

//initialization
$(document).ready(function () {
	initialize();
  loadItemsPerPage();
});