var countriesList;

//filter controls initialized
var FilterBox = $('.filter-text-box');
var FilterCountry = $('#search-country-name');

//search status controls
var Search_status = $('#search-status');
var Search_status_ul = $('.search-status-list');
var Search_status_li = $('.search-status-li');

//Pagination variable declaration
var ItemsPerPage = $('#items_per_page');
var PaginationView = $('.pagination-view');
var Pagination = $('#pagination-rpt');
var CompliacneCount = $('.compliance_count');
var on_current_page = 1;
var sno = 0;
var totalRecord;
var ReportData;

function initialize() {
  function success(status, data) {
    countriesList = data.countries;
    totalRecord = countriesList.length;
    processPaging();
  }
  function failure(status, data) {
  }
  mirror.getCountryReport(success, failure);
}

function processSearch()
{
  c_name = FilterCountry.val().toLowerCase();

  usr_status = $('.search-status-li.active').attr('value');

  searchList = []

  for(var i in countriesList){
    data = countriesList[i];

    data_c_name = data.country_name.toLowerCase();
    data_is_active = data.is_active;

    if (
      (~data_c_name.indexOf(c_name)))
    {
      if ((usr_status == 'all' || Boolean(parseInt(usr_status)) == data.is_active)){
        searchList.push(data);
      }
    }
  }
  loadCountriesList(searchList);
}

function loadCountriesList(countriesList) {
  var sno = 0;
  var title;
  $('.tbody-country-list').find('tr').remove();
  for (var i in countriesList) {
    var countries = countriesList[i];
    var isActive = countries.is_active;

    var tableRow = $('#templates .table-country-report .table-row');
    var clone = tableRow.clone();
    sno = sno + 1;
    $('.sno', clone).text(sno);
    $('.country-name', clone).text(countries.country_name);
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
    $('.tbody-country-list').append(clone);
  }
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
  initialize();

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
  totalRecord = countriesList.length;
  ReportData = pageData(on_current_page);
  if (totalRecord == 0) {
    $('.table-country-list').empty();
    var tableRow4 = $('#no-record-templates .table-no-content .table-row-no-content');
    var clone4 = tableRow4.clone();
    $('.no_records', clone4).text('No Records Found');
    $('.table-country-list').append(clone4);
    PaginationView.hide();
    hideLoader();
  } else {
    if(sno==0){
      createPageView(totalRecord);
    }
    PaginationView.show();
    //ReportView.show();
    loadCountriesList(ReportData);
  }
}

function pageData(on_current_page){
  data = [];
  _page_limit = parseInt(ItemsPerPage.val());
  recordLength = (parseInt(on_current_page) * _page_limit);
  var showFrom = sno + 1;
  var is_null = true;
  for(i=sno;i<countriesList.length;i++)
  {
    is_null = false;
    data.push(countriesList[i]);
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

/*$('#search-country-name').keyup(function () {
  var count = 0;
  var value = this.value.toLowerCase();
  $('table').find('tr:not(:first):not(:last)').each(function (index) {
    if (index === 0)
      return;
    var id = $(this).find('.country-name').text().toLowerCase();
    $(this).toggle(id.indexOf(value) !== -1);
  });
  count = $('tr:visible').length - 3;
  $('#total-records').html('Total : ' + count + ' records');
});*/

$(function () {
  renderControls();
  loadItemsPerPage();
});