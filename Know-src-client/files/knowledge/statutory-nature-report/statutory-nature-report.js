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
var searchList = [];

var Key = {
  LEFT:   37,
  UP:     38,
  RIGHT:  39,
  DOWN:   40
};

function displayLoader() {
  $('.loading-indicator-spin').show();
}
function hideLoader() {
  $('.loading-indicator-spin').hide();
}

// get statutory nature list from api
function getStatutorynature() {
	function onSuccess(data) {
		statutorynatureList = data.statutory_natures;
		totalRecord = statutorynatureList.length;
    processPaging();
    hideLoader();
	}
	function onFailure(error) {
		displayMessage(error);
	}
  displayLoader();
	mirror.getStatutoryNatureList(function (error, response) {
		if (error == null) {
		  onSuccess(response);
		} else {
      hideLoader();
		  onFailure(error);
		}
	});
}

function processSearch()
{
  searchList = [];
  nature_status = $('.search-status-li.active').attr('value');

  for(var i in statutorynatureList){
    data = statutorynatureList[i];
    data_is_active = data.is_active;

    if ((nature_status == 'all' || Boolean(parseInt(nature_status)) == data.is_active)){
        searchList.push(data);
    }
  }
  totalRecord = searchList.length;
  //loadStatNatureData(searchList);
  processPaging();
}

//display statutory nature list in view page
function loadStatNatureData(data) {
  var j = 1;
  viewTable.find('tr').remove();

  $.each(data, function (key, value) {
    sno = sno + 1;
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
    $('.sno', clone).text(sno);
    $('.country-name', clone).text(country_name);
    $('.statutory-nature-name', clone).text(statutory_nature_name);

    if (isActive == true){
      $('.status', clone).text("Active")
    }
    else{
      $('.status', clone).text("In active")
    }


    viewTable.append(clone);
    //j = j + 1;
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

		var currentClass = $(event.target).html();
    Search_status.html(currentClass);
		/*Search_status.removeClass();
		if(currentClass != undefined){
		  Search_status.addClass(currentClass);
		  Search_status.text('');
		}else{
		  Search_status.addClass('fa');
		  Search_status.text('All');
		}*/
		processSearch();
	});

	FilterBox.keyup(function() {
	    processSearch();
	});

	Search_status.change(function() {
	    processSearch();
	});

  $('input').on('keypress', function (e) {
    /*var regex = new RegExp("^[a-zA-Z0-9]+$");
    var key = String.fromCharCode(!event.charCode ? event.which : event.charCode);
    if (!regex.test(key)) {
       event.preventDefault();
       return false;
    }*/
    if($(this).attr('id') == "search-country-name"){
      var k = e.which || e.keyCode;
      var ok = k >= 65 && k <= 90 || // A-Z
          k >= 97 && k <= 122 || k == 46 || k ==8 || k == 9 || k == Key.LEFT ||
                k == Key.RIGHT; // a-z
          //k >= 48 && k <= 57; // 0-9

      if (!ok){
          e.preventDefault();
      }
    }
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
  //totalRecord = statutorynatureList.length;
  if (totalRecord == 0) {
    viewTable.find('tr').remove();
    var tableRow4 = $('#no-record-templates .table-no-content .table-row-no-content');
    var clone4 = tableRow4.clone();
    $('.no_records', clone4).text('No Records Found');
    viewTable.append(clone4);
    PaginationView.hide();
    //hideLoader();
  } else {
    if(sno==0){
      createPageView(totalRecord);
    }
    ReportData = pageData(on_current_page);

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
  if(searchList.length > 0)
  {
    recordData = searchList;
  }
  else
  {
    recordData = statutorynatureList;
  }
  totalRecord = recordData.length;
  for(i=sno;i<recordData.length;i++)
  {
    is_null = false;
    data.push(recordData[i]);
    if(i == (recordLength-1))
    {
      break;
    }
  }
  //totalRecord = data.length;
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
$(document).find('.js-filtertable').each(function(){
    $(this).filtertable().addFilter('.js-filter');
});